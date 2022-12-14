# import package
import requests
import pickle
import pandas as pd
import re
import numpy as np
import json
import os
if not os.path.exists("src/ncvs_tool/dataname2url.json"):
    from ncvs_tool.dataLibrary import dataname2url
    dataname2url()

if not os.path.exists("src/ncvs_tool/sample_size.csv"):
    from ncvs_tool.dataLibrary import get_survey_sample_size
    get_survey_sample_size()

if not os.path.exists("src/ncvs_tool/personal_victimization_dictionary.json"):
    import ncvs_tool.dataLibrary
    ncvs_tool.dataLibrary.create_personal_victimization_dictionary()

class NCVStool:

    def __init__(self, dataname, api_token = None, username = None, password = None):
        # dic store the datasetname and its url:
        with open("src/ncvs_tool/dataname2url.json", "rb") as f:
            self.dataname2url = pickle.load(f)
        self.dataname = dataname
        self.sample_size = None

        self.request_times = 0
        self.requested_data = {}
        self.valid_params = {}

        self.s = requests.Session()
        # This function trys to request the data and get valid params for user to query:
        # setting the access authority:
        # 1) method 1: API token
        if api_token:
            self.s.headers.update({"X-App-token": api_token})
        # 2) method 2: Username & password
        self.identification_match(username, password)
        if username and password:
            self.s.auth = (username, password)


    def identification_match(self, username, password):
        if (not username and password) or (username and not password):
            raise Exception("Please input BOTH username AND password!")

    def get_valid_params(self, output_valid_params = True):

        # try to access the data and get the columns of the dataset
        try:
            limit = {"$limit":100}
            test = self.s.get(self.dataname2url[self.dataname], params = limit)
            if test.status_code >= 400:
                error_message = f"Request Error: {test.status_code}"
                raise requests.exceptions.HTTPError(error_message, response = test)
            else:
                test = test.json()
                test_df = pd.DataFrame.from_records(test)
                self.valid_params = set(test_df.columns)
                if output_valid_params:
                    return self.valid_params
        except:
            print(error_message)

    def NCVS_query(self, limit = 100000, encode = True, **kwargs):
        """


        :param encode:
        if True, output dataset from requests that is encoded as number;
        if false, transform the requested data into original label.

        :param kwargs:
        >> simple query:
        if your query is "=" then input directly, e.g. weapon = 1

        >> complex query:
        1) if your query is "<",">" "<=",">=" with logic computation, use where,
        e.g. 1 where = "weapon>1"; 2 where = "ager>2 OR weapon>1" 3 where = "ager>2 AND weapon=1"
        2) if you need to limit the amount of output, use limit, e.g. limit = 1000
        3) if you only need subset of the columns, use select, e.g. select = "idper,ager"

        :return:
        r_df: pandas.DataFrame
        """
        if not self.valid_params:
            self.get_valid_params(output_valid_params = False)

        other_params = set(["limit", "where", "select"])

        kwargs["limit"] = limit
        params = {}
        for key, value in kwargs.items():
            if key in self.valid_params:
                params[key] = value
            elif key in other_params:
                # insert an valid params check here:
                if key == "where":
                    where_list = set(re.findall("[a-z]+", value))-set(["in"])
                    for i in where_list:
                        if i not in self.valid_params:
                            raise Exception(f"Query param in where {i} invalid")
                if key == "select":
                    select_list = re.findall("[a-z]+", value)
                    for i in select_list:
                        if i not in self.valid_params:
                            raise Exception(f"Query param in select {i} invalid")
                params["$" + key] = value

            else:
                raise Exception(f"Query param {key} invalid")

        r = self.s.get(self.dataname2url[self.dataname], params=params)

        if r.status_code >= 400:
            raise requests.exceptions.HTTPError(f"Request Error: {r.status_code}", response = r)
        else:
            self.request_times += 1

        r = r.json()
        r_df = pd.DataFrame.from_records(r)
        self.requested_data[f"request{self.request_times}"] = {"condition": kwargs, "data": r_df}

        if not encode:
            r_df_transform = self.label_transform(r_df)
            return r_df_transform # transform original data

        return r_df

    def get_sample_size(self, output = True):
        """
        This function is to get survey sample size for each year.

        :param output: boolean, if True, output sample size for each survey year.
        :return: sample_size: pd.DataFrame
        """
        # get_sample_size for the dataset you requested
        sample_size = pd.read_csv("src/ncvs_tool/sample_size.csv")
        if self.dataname == "Personal Victimization":
            self.sample_size = sample_size[["Year", "Persons(Interviewed)"]]
        elif self.dataname == "Household Victimization":
            self.sample_size = sample_size[["Year", "Households(Interviewed)"]]

        if output:
            return self.sample_size

    def label_transform(self, df):
        with open("src/ncvs_tool/personal_victimization_dictionary.json", "rb") as f:
            data_dic = pickle.load(f)

        label_map = {}
        for key, value in data_dic.items():
            if len(value.keys()) > 1:
                label_map[key] = value
        label_map["offtracenew"] = label_map["offtrace"]
        df_transform = df.copy()
        for key, value in label_map.items():
            try:
                df_transform[key] = df[key].map(value)
            except:
                pass

        return df_transform












