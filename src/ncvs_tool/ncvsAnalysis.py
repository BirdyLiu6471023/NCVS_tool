from ncvsTool import NCVStool
import visualizationTool as vt
import pandas as pd
import numpy as np


def year_series(dataname, start=1993, end=2021, group2count=None, colname4group="victimization_freq", output_pct=True,
                output_picture=False):
    """
    Function giving a time series dataset for your wanted group

    :param dataname: string, your wanted dataset, e.g. dataname = "Personal Victimization";
    :param start: integer, start year;
    :param end: integer, end year;
    :param group2count: string, wanted group in timeseries, e.g. group2count = "ager>2";
    :param colname4group: string, your defined name for the column for number of each year of this group;
    :param output_pct: boolean, True if output percent of your group in dataframe;
    :param output_picture: boolean, True if output time series graph;
    :return: Time Series DataFrame (time series graph if output_picture is True).
    """

    # transform the year range into acceptable format
    year_range = range(start, end + 1)
    year_list = tuple([str(x) for x in year_range])

    # request data
    dt = NCVStool(dataname)
    query_str = f"year in {year_list}" if not group2count else f"year in {year_list} AND {group2count}"
    full_data = dt.NCVS_query(limit=70000, where=query_str)

    # frequency of your defined group in victimization survey dataset
    frequency = pd.DataFrame(full_data.groupby("year").idper.count()).reset_index()
    frequency.year = frequency.year.astype(int).astype(str)

    # get sample size of each year, this is the total amount of interviewer
    sample_size = dt.get_sample_size()
    sample_size.Year = sample_size.Year.astype(int).astype(str)

    # create year_series dataframe
    year_series_ = frequency.merge(sample_size, left_on="year", right_on="Year").drop("Year", axis=1)
    year_series_.columns = ["year", colname4group, "sample_size"]

    if output_pct:
        year_series_["pct"] = year_series_[colname4group] / year_series_["sample_size"]

    if output_picture:
        vt.basic_visual_series(year_series_.year, year_series_.pct, f"Tendency of {colname4group}", xlabel="year",
                            ylabel=f"{colname4group}_rate")

    return year_series_


def ncvs_report(dataname, year, group, target="notify", target_range=2, pivot=False, encode=False, output_pct=True,
                output_picture=True):
    # request data:
    dt = NCVStool(dataname)
    df_y = dt.NCVS_query(limit=10000, encode = encode, year=year)

    # group data
    df_t = pd.DataFrame(df_y.groupby([group, target]).idper.count()).reset_index().astype(int)
    df_t.columns = [group, target, "count"]

    df_t = df_t[df_t[target] <= target_range]

    df_pivot = pd.pivot_table(df_t, values="count", index=group, columns=target, aggfunc=np.sum)


    if output_picture:
        vt.group_bar(df_pivot, xlabel=group, ylabel=f"count of {target}")

    if pivot:
        if output_pct:
            for i in range(len(df_pivot)):
                total = sum(df_pivot.iloc[i, :])
                for j in range(len(df_pivot.iloc[0])):
                    df_pivot.iloc[i, j] = df_pivot.iloc[i, j] / total
            return df_pivot

        return df_pivot
    else:
        return df_t





