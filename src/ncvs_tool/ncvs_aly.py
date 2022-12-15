from ncvs_tool.ncvs_tool import NCVStool
import ncvs_tool.visual_tool as vt
import pandas as pd
import numpy as np


def year_series(dataname="Personal Victimization", start=1993, end=2021, group2count=None,
                colname4group="victimization_freq", output_pct=True,
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

    # this is only valid for dataset "Personal Victimization" and "Personal Population"
    if dataname not in ["Personal Victimization", "Personal Population"]:
        raise NotImplementedError

    # transform the year range into acceptable format
    year_range = range(start, end + 1)
    year_list = tuple([str(x) for x in year_range])

    # request data
    dt = NCVStool(dataname)
    query_str = f"year in {year_list}" if not group2count else f"year in {year_list} AND {group2count}"
    full_data = dt.query(limit=70000, where=query_str)

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


def year_report(year, group, target="notify", dataname="Personal Victimization", target_range=2, pivot=False,
                encode=False, output_pct=True, output_picture=True):
    """
    This function output a table that give a statistic comparison between different groups.
    For example, if you want to know the difference of "report to police" of two sexs, different ages or different type
    of crimes. This function would help. It also support output rate/percentage of two group.
    This function could also output a graph.

    :param dataname: string, default "Personal Victimization""
    :param year: int, e.g. year = "2021"
    :param group: string, define how you group victim, vaild params like "age", "sex"
    :param target: string, define your target variables, valid params like "notify", "series"
    :param target_range: int, the target range you interested in
    :param pivot: boolean, if true, output pivot data; if false, output tidy data.
    :param encode: boolean, if true, output numeric labels; if false, output original labels with meaning.
    :param output_pct: boolen, if true, output rate of each group; if false, output number of each group.
    :param output_picture: boolean, if true, output graph of plot.
    :return:
    """

    # request data:
    dt = NCVStool(dataname)
    df_y = dt.query(limit=10000, year=year)

    # groupby data:
    df_t = pd.DataFrame(df_y.groupby([group, target]).idper.count()).reset_index().astype(int)
    # rename data:
    df_t.columns = [group, target, "count"]
    # only retain useful data
    df_t = df_t[df_t[target] <= target_range]
    # transform label back to string, which is consistent to ncvs_tool.NCVStool.label_transform():
    if target:
        df_t[[group, target]] = df_t[[group, target]].astype(str)

    # transform data only if dataname = "Personal Victimization":
    if dataname == "Personal Victimization":
        if not encode:
            df_t = dt.label_transform(df=df_t)

    df_pivot = pd.pivot_table(df_t, values="count", index=group, columns=target, aggfunc=np.sum)

    if output_picture:
        vt.group_bar(df_pivot, xlab=group, ylab=f"count of {target}")

    if pivot:
        if output_pct:  # calculate percent of each group.
            for i in range(len(df_pivot)):
                total = sum(df_pivot.iloc[i, :])
                for j in range(len(df_pivot.iloc[0])):
                    df_pivot.iloc[i, j] = df_pivot.iloc[i, j] / total
            return df_pivot

        return df_pivot
    else:
        return df_t
