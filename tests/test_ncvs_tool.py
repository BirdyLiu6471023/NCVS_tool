from ncvs_tool import ncvsTool as nt
from ncvs_tool import ncvsAnalysis as na
from ncvs_tool import dataLibrary
from ncvs_tool import visualizationTool
import os


#na.ncvs_report("Personal Victimization", 2021, group="sex", target="notify", target_range=2, pivot=False, encode=False,
               #output_pct=False, output_picture=False)

print(os.path.exists("src/ncvs_tool/dataname2url.json"))

