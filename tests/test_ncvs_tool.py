from ncvs_tool import ncvsAnalysis
from ncvs_tool import dataLibrary
import os
import numpy as np


# 1) test required files in source:
def test_dicfile_exist():
    assert (os.path.exists("docs/dataname2url.json") or os.path.exists("docs/sample_size.csv")
            or os.path.exists("docs/personal_victimization_dictionary.json"))


# 2) test ncvs analysis function ncvs_report:
def test_enlabel_work():
    a = ncvsAnalysis.ncvs_report("Personal Victimization", year=2021, group="sex", pivot=False, output_pct=False,
                                 output_picture=False)
    assert isinstance(a.iloc[0, 0], str)


# 3) test ncvs analysis function year series:
def test_year_series():
    b = ncvsAnalysis.year_series("Personal Victimization", start=2018, end=2020)

    assert (not np.isnan(b.iloc[0, 1]) and len(b) == 3)


# 4) test extracting infor from pdf:
def test_get_cook_book():
    c, d = dataLibrary.extract_personal_victimization_cookbook()
    assert (len(c) > 0)
