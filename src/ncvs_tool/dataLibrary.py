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

    return dataname2url


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
    return df


# this function could not be used because of unable to access the pdf.
def extract_personal_victimization_cookbook():
    # read tables in pdf files and wrangling data:
    df = tabula.read_pdf("docs/NCVS_Select_person_level_codebook.pdf", pages=[6, 7, 8, 9, 10], lattice=True,
                         guess=False, stream=True)
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
    # cv, failed = extract_personal_victimization_cookbook()
    cv = {'idper': {'Unique identifier': 'N A'}, 'yearq': {'YYYY.Q': 'N A'}, 'year': {'1993-2021': 'N A'},
          'ager': {'1': '12-17',
                   '2': '18-24',
                   '3': '25-34',
                   '4': '35-49',
                   '5': '50-64',
                   '6': '65 or older'}, 'sex': {'1': 'Male', '2': 'Female'},
          'hispanic': {'1': 'Hispanic', '2': 'Non-Hispanic', '88': 'Residue'}, 'race': {'1': 'White',
                                                                                        '2': 'Black',
                                                                                        '3': 'American Indian Alaska Native',
                                                                                        '4': 'Asian NativeHawaiian OtherPacific Islander',
                                                                                        '5': 'More than one race'},
          'race_ethnicity': {'1': 'Non-Hispanic white',
                             '2': 'Non-Hispanic black',
                             '3': 'Non-HispanicAmerican Indian Alaska Native',
                             '4': 'Non-Hispanic Asian Native Hawaiian Other Pacific Islander',
                             '5': 'Non-Hispanic morethan one race',
                             '6': 'Hispanic'}, 'hincome2': {'-1': 'Invalid until 2017 Q1',
                                                            '1': 'Less than $25,000',
                                                            '2': '$25,000 to $49,999',
                                                            '3': '$50,000 to $99,999',
                                                            '4': '$100,000 to $199,999',
                                                            '5': '$200,000 or more'}, 'marital': {'1': 'Never married',
                                                                                                  '2': 'Married',
                                                                                                  '3': 'Widowed',
                                                                                                  '4': 'Divorced',
                                                                                                  '5': 'Separated',
                                                                                                  '88': 'Residue'},
          'popsize': {'-1': 'Invalid until 1995 Q3',
                      '0': 'Not a place',
                      '1': 'Under 100,000',
                      '2': '100,000-249,999',
                      '3': '250,000-499,999',
                      '4': '500,000-999,999',
                      '5': '1 million or more'}, 'region': {'-1': 'Invalid until 1995 Q3',
                                                            '1': 'Northeast',
                                                            '2': 'Midwest',
                                                            '3': 'South',
                                                            '4': 'West'}, 'msa': {'1': 'Principal city withinMSA',
                                                                                  '2': 'Not part of principalcity within MSA',
                                                                                  '3': 'Outside MSA'},
          'locality': {'-1': 'Invalid until 2020 Q1',
                       '1': 'Urban',
                       '2': 'Suburban',
                       '3': 'Rural'}, 'educatn2': {'-1': 'Invalid until 2003 Q1',
                                                   '1': 'No schooling',
                                                   '2': 'Grade school',
                                                   '3': 'Middle school',
                                                   '4': 'Some high school',
                                                   '5': 'High school graduate',
                                                   '6': 'Some college andassociate degree',
                                                   '7': 'Bachelor’s degree',
                                                   '8': 'Advanced degree',
                                                   '98': 'Residue'}, 'veteran': {'-2': 'Invalid until 2017 Q1',
                                                                                 '-1': 'Under age 18',
                                                                                 '0': 'Not a veteran',
                                                                                 '1': 'Veteran',
                                                                                 '8': 'Residue'},
          'citizen': {'-1': 'Invalid until 2017 Q1',
                      '1': 'Born U.S. citizen',
                      '2': 'Naturalized citizen',
                      '3': 'Non-U.S. Citizen',
                      '8': 'Residue'}, 'newcrime': {'1': 'Violent crime', '2': 'Personal theft larceny'},
          'newoff': {'1': 'Rape sexual assault',
                     '2': 'Robbery',
                     '3': 'Aggravated assault',
                     '4': 'Simple assault',
                     '5': 'Personal theft larceny'}, 'seriousviolent': {'1': 'Violent crimeexcluding simple',
                                                                        '2': 'assaultSimple assault',
                                                                        '3': 'Personal theft larceny'},
          'vicservices': {'1': 'Yes', '2': 'No', '3': 'Don’t know', '8': 'Residue'},
          'locationr': {'1': 'At or near victim’shome',
                        '2': 'At or near friend’s,neighbor’s, orrelative’s home',
                        '3': 'Commercial place,parking lot, otherpublic area',
                        '4': 'School',
                        '5': 'Other location'}, 'direl': {'1': 'Intimates',
                                                          '2': 'Other relatives',
                                                          '3': 'Well known casualacquaintance',
                                                          '4': 'Strangers',
                                                          '5': 'Do not knowrelationship',
                                                          '6': 'Do not know number'},
          'weapon': {'1': 'Yes', '2': 'No', '3': 'Do not know if'}, 'weapcat': {'0': 'No weapon',
                                                                                '1': 'Firearm',
                                                                                '2': 'Knife',
                                                                                '3': 'Other type weapon',
                                                                                '4': 'Type weaponunknown',
                                                                                '5': 'Do not know if'},
          'injury': {'0': 'Not injured', '1': 'Injured'}, 'treatment': {'0': 'Not injured',
                                                                        '1': 'Not treated',
                                                                        '2': 'Treated at scene,',
                                                                        '3': 'home, medical office,',
                                                                        '88': 'or other location'},
          'offenderage': {'1': '11 or younger',
                          '2': '12-17',
                          '3': '18-29',
                          '4': '30 or older',
                          '5': 'Multiple offenders ofvarious ages',
                          '88': 'Residue'}, 'offendersex': {'1': 'Male',
                                                            '2': 'Female',
                                                            '3': 'Both male and femaleoffenders',
                                                            '4': 'Unknown',
                                                            '88': 'Residue'},
          'offtrace': {'-1': 'Invalid until 2012 Q1',
                       '1': 'Non-Hispanic white',
                       '2': 'Non-Hispanic black',
                       '3': 'Non-HispanicAmerican Indian Alaska Native',
                       '4': 'Non-Hispanic Asian Native Hawaiian Other Pacific Islander',
                       '5': 'Non-Hispanic morethan one race',
                       '6': 'Hispanic',
                       '7': 'Unknown race ethnicity',
                       '10': 'Mixed race group ofoffenders',
                       '11': 'Unknown number of'}, 'wgtviccy': {'numeric': 'N A'},
          'series': {'1': 'Not a series crime', '2': 'Series crime'}, "hincome1": {"1": "Less than $7,500",
                                                                                   "2": "$7,500 to $14,999",
                                                                                   "3": "$15,000 to $24,999",
                                                                                   "4": "$25,000 to $34,999",
                                                                                   "5": "$35,000 to $49,999",
                                                                                   "6": "$50,000 to $74,999",
                                                                                   "7": "$75,000 or more",
                                                                                   "88": 'Unknown'},
          "educatn1": {"1": "No schooling",
                       "2": "Grade school",
                       "3": "Middle school",
                       "4": "High school",
                       "5": "College",
                       "88": "Residue"}, "notify": {"1": "Yes",
                                                    "2": "No",
                                                    "3": "Do not know",
                                                    "8": "Residue"}, "serious": {"1": 'No injury',
                                                                                 "2": "Serious injury",
                                                                                 "3": "Minor injury",
                                                                                 "4": "Rape w/o other injuries",
                                                                                 "88": "Residue"},
          "newwgt": {"numeric": "N/A"}}


    return cv

# create_personal_victimization_dictionary()
