from ncvs_tool import ncvsAnalysis
import os


# 1) test required files in source:
def test_dicfile_exist():
    assert (os.path.exists("src/ncvs_tool/dataname2url.json") or os.path.exists("src/ncvs_tool/sample_size.csv")
            or os.path.exists("src/ncvs_tool/personal_victimization_dictionary.json"))


# 2) test ncvs analysis function ncvs_report:
def test_enlabel_work():
    a = ncvsAnalysis.ncvs_report("Personal Victimization", year=2021, group="sex", pivot=False, output_pct=False,
                                 output_picture=False)
    assert isinstance(a.iloc[0, 0], str)





