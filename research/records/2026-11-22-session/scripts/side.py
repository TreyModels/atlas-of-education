import battery as B
import numpy as np
picks=["THA","PHL","KOR","VNM","IDN","MYS","ETH","NGA","KEN","GHA","ZAF","JPN"]
keys=["fertility","ter","gpi_ter","sec","gpi_sec","flfp","wage_emp","urban","u5mr","gdppc_log","electricity"]
lab={"fertility":"births/woman","ter":"higher ed %","gpi_ter":"women:men higher ed","sec":"secondary completion",
     "gpi_sec":"women:men secondary","flfp":"women in labour force %","wage_emp":"paid jobs %",
     "urban":"city %","u5mr":"child deaths/1000","gdppc_log":"income (log)","electricity":"electricity %"}
def val(k,iso,y):
    return B.V[k].get((iso,y))
print(f"{'country':8s} {'year':6s}"+"".join(f"{lab[k][:12]:>13s}" for k in keys))
for iso in picks:
    for y in (1990,2010,2020):
        r=[val(k,iso,y) for k in keys]
        if all(v is None for v in r): continue
        print(f"{iso:8s} {y:6d}"+"".join(f"{'' if v is None else round(v,1):>13}" for v in r))
    print()
