from ncvs_tool import ncvs_aly
from ncvs_tool import url_store
import numpy as np


# 1) test ncvs analysis function ncvs_report:
def test_enlabel_work():
    a = ncvs_aly.year_report("Personal Victimization", year=2021, group="sex", pivot=False, output_pct=False,
                             output_picture=False)
    assert isinstance(a.iloc[0, 0], str)


# 2) test ncvs analysis function year series:
def test_year_series():
    b = ncvs_aly.year_series("Personal Victimization", start=2018, end=2020)

    assert (not np.isnan(b.iloc[0, 1]) and len(b) == 3)


# 3) test extracting infor from pdf:
def test_get_cook_book():
    c, d = url_store.extract_personal_victimization_cookbook()
    assert (len(c) > 0)

# 4)
