# import package
import requests
import pandas as pd
import re
import numpy as np
from ncvs_tool import url_store


class NCVStool:

    def __init__(self, dataname="Personal Victimization", api_token=None, username=None, password=None):
        """
        Description
        ---------------
        This class could query data and also store your requested data from same dataset.
        Government dataset does not require api_token or username and password.

        Parameters
        _______________
        :dataname: string, default = "Personal Victimization"
        :api_token: string
        :username: string
        :password: string

        """
        self.dataname2url = url_store.dataname2url()
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
        """
        Usage:
        ---------------
        This function check if user provid both username and password.
        used in self.__init__()

        Parameters
        ---------------
        :username
        :password

        """

        if (not username and password) or (username and not password):
            raise Exception("Please input BOTH username AND password!")

    def get_valid_params(self, output_valid_params=True):
        """
        Description
        ----------------
        This function would help to check if user entered params are vaild,
        which also could provide users vaild params in self.NCVS_query()
        ----------------
        :param output_valid_params: boolean
        :return:
        if output_valid_params True, output a set with vaild params that could be entered in self.NCVS_query()
        """
        global error_message
        try:
            limit = {"$limit": 100}
            test = self.s.get(self.dataname2url[self.dataname], params=limit)
            if test.status_code >= 400:
                error_message = f"Request Error: {test.status_code}"
                raise requests.exceptions.HTTPError(error_message, response=test)
            else:
                test = test.json()
                test_df = pd.DataFrame.from_records(test)
                self.valid_params = set(test_df.columns)
                if output_valid_params:
                    return list(self.valid_params)
        except:
            print(error_message)

    def query(self, limit=100000, encode=True, **kwargs):
        """
        Description
        --------------
        This a function that could query your wanted group of dataset.
        * Note: The original data requested from API is encoded data,
         which is all numbers without original label meaning. This query
         provide user option to output encoded dataset or dataset with original
         meaning label, developer could also refer the NCVS_cook book in docs/ in github.

        Parameters
        --------------
        :limit: the number of records output.

        :encode: if True, output dataset from requests that is encoded as number; if false, transform the
        requested data into original label.

        :kwargs:
        >> simple query: if your query is "=" then input directly, e.g. weapon = 1
        >> complex query:
        1) if your query is "<",">" "<=",">=" with logic computation, use where,e.g. 1 where = "weapon>1"; 2 where =
        "ager>2 OR weapon>1" 3 where = "ager>2 AND weapon=1"
        2) if you need to limit the amount of output, use limit, e.g. limit = 1000
        3) if you only need subset of the columns, use select, e.g. select = "idper,ager"

        :return: r_df: pandas.DataFrame
        """

        if not self.valid_params:
            self.get_valid_params(output_valid_params=False)

        other_params = {"limit", "where", "select"}

        kwargs["limit"] = limit
        params = {}
        for key, value in kwargs.items():
            if key in self.valid_params:
                params[key] = value
            elif key in other_params:
                # insert an valid params check here:
                if key == "where":
                    where_list = set(re.findall("[a-z]+", value)) - set(["in"])
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
            raise requests.exceptions.HTTPError(f"Request Error: {r.status_code}", response=r)
        else:
            self.request_times += 1

        r = r.json()
        r_df = pd.DataFrame.from_records(r)
        self.requested_data[f"request{self.request_times}"] = {"condition": kwargs, "data": r_df}

        if not encode:
            r_df_transform = self.label_transform(r_df)
            return r_df_transform  # transform original data

        return r_df

    def get_sample_size(self, output=True):
        """
        Description:
        --------------
        This function is to get survey sample size for each year.

        :param output: boolean, if True, output sample size for each survey year.
        :return: sample_size: pd.DataFrame
        """
        # get_sample_size for the dataset you requested
        sample_size = url_store.get_survey_sample_size()
        if self.dataname == "Personal Victimization":
            self.sample_size = sample_size[["Year", "Persons(Interviewed)"]]
        elif self.dataname == "Household Victimization":
            self.sample_size = sample_size[["Year", "Households(Interviewed)"]]
        else:
            raise NotImplementedError

        if output:
            return self.sample_size

    def label_transform(self, df):
        """
        Usage:
        This functions is to transfer the encoded dataframe to dataset with original label meaning.
        :param df: pd.DataFrame need to do label transfer
        :return: df
        """

        if self.dataname != "Personal Victimization":
            raise NotImplementedError

        data_dic = url_store.create_personal_victimization_dictionary()

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

    def get_valid_label(self, param):
        if self.dataname != "Personal Victimization":
            raise NotImplementedError

        data_dic = url_store.create_personal_victimization_dictionary()
        label = data_dic[param]
        return label

