import pickle
import requests
import pandas as pd
import numpy as np
import tabula


def dataname2url():
    dataname2url = {}

    dataname2url["Personal Victimization"] = "https://data.ojp.usdoj.gov/resource/gcuy-rt5g"
    dataname2url["Personal Population"] = "https://data.ojp.usdoj.gov/resource/r4j4-fdwx"
    dataname2url["Household Victimization"] = "https://data.ojp.usdoj.gov/resource/gkck-euys"
    dataname2url["Household Population"] = "https://data.ojp.usdoj.gov/resource/ya4e-n9zp"

    with open("src/ncvs_tool/dataname2url.json", "wb") as f:
        pickle.dump(dataname2url, f)


def get_survey_sample_size():
    # non-structured data, need to manually update year to year:
    url = "https://bjs.ojp.gov/bjs.ojp.gov/samplesize.xlsx"
    s = requests.get(url).content
    xl = pd.ExcelFile(s)
    df = xl.parse('NCVS participation rates')
    df = df.dropna(how='all').dropna(how='all', axis=1)
    df.columns = ["Year", "Households(Eligible)", "Households(Interviewed)", "Participation(Rate)",
                  "units", "Persons(Eligible)", "Persons(Interviewed)", "Participation(Rate)", "units%"]
    for i in range(1, len(df.Year)):
        if np.isnan(df.Year[i]):
            df = df.drop(i, axis=0)
        else:
            break
    df = df.reset_index().drop("index", axis=1)
    df.to_csv("src/ncvs_tool/sample_size.csv")

def extract_personal_victimization_cookbook():
    # read tables in pdf files and wrangling data:
    df = tabula.read_pdf("src/ncvs_tool/NCVS_Select_person_level_codebook.pdf", pages=[6,7,8,9,10], lattice=True, guess=False, stream=True)
    pv_cb = {}
    all_features = set()
    for p in range(5):
        for j in range(len(df[p])):
            all_features.add(df[p].iloc[j, 2])
            try:
                num = df[p].iloc[j, 3].split("\r")
                label = df[p].iloc[j, 4].split("\r")
                map_t = {}
                i = 0
                while i < len(num):
                    cur = i
                    map_t[num[cur]] = label[cur].replace("/", " ")
                    i = i + 1
                    while i < len(num) and not num[i]:
                        map_t[num[cur]] += label[i].replace("/", " ")
                        i = i + 1
                pv_cb[df[p].iloc[j, 2]] = map_t
            except:
                pass
    failed = all_features - set(pv_cb.keys())
    return [pv_cb, failed]

def create_personal_victimization_dictionary():
    # dealing with the variable that failed in extracting pdf file...
    # and create a json file to store the file:
    cv, failed = extract_personal_victimization_cookbook()
    if "hincome1" in failed:
        cv["hincome1"] = {"1": "Less than $7,500",
                      "2": "$7,500 to $14,999",
                      "3": "$15,000 to $24,999",
                      "4": "$25,000 to $34,999",
                      "5": "$35,000 to $49,999",
                      "6": "$50,000 to $74,999",
                      "7": "$75,000 or more",
                      "88": 'Unknown'}
        failed.remove("hincome1")

    if "educatn1" in failed:
        cv["educatn1"] = {"1": "No schooling",
                      "2": "Grade school",
                      "3": "Middle school",
                      "4": "High school",
                      "5": "College",
                      "88": "Residue"}
        failed.remove("educatn1")

    if "notify" in failed:
        cv["notify"] = {"1": "Yes",
                        "2": "No",
                        "3": "Do not know",
                        "8": "Residue"}
        failed.remove("notify")

    if "serious" in failed:
        cv["serious"] = {"1": 'No injury',
                         "2": "Serious injury",
                         "3": "Minor injury",
                         "4": "Rape w/o other injuries",
                         "88": "Residue"}
        failed.remove("serious")

    if "newwgt" in failed:
        cv["newwgt"] = {"numeric": "N/A"}
        failed.remove("newwgt")

    if not failed:
        with open("src/ncvs_tool/personal_victimization_dictionary.json", "wb") as f:
            pickle.dump(cv, f)


#create_personal_victimization_dictionary()