#!/usr/bin/env python3
"""Cambodia DHS wealth-quintile attendance profile, ages 14-17 (credential-floor test).

The relational-floor / credential-floor note needs: attendance by wealth quintile at 14-17 and
the share of non-attenders from the bottom two quintiles (bottom 40%). Model predictions to compare:
human capital ~65% of exits from bottom 40%, relational floor ~98%.
"""
import os, json
import numpy as np, pandas as pd, pyreadstat

BASE = os.path.expanduser("~/neon-boot/pulled/dhs/cambodia")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
WAVES = {"2000":("KHPR42SD","KHPR42FL.SAS7BDAT"),"2005":("KHPR51SD","KHPR51FL.SAS7BDAT"),
         "2010":("KHPR61SD","KHPR61FL.SAS7BDAT"),"2014":("KHPR73SD","KHPR73FL.SAS7BDAT"),
         "2021-22":("KHPR82SD","KHPR82FL.SAS7BDAT")}

def wshare(w, y):
    return float((w*y).sum()/w.sum()) if w.sum()>0 else float("nan")

rows=[]
for wave,(folder,fname) in WAVES.items():
    f=os.path.join(BASE,wave,folder,fname)
    _,meta=pyreadstat.read_sas7bdat(f, metadataonly=True)
    cols=[c.upper() for c in meta.column_names]
    use=["HV105","HV121","HV122","HV005"]+[c for c in ("HV270","HV271") if c in cols]
    df,_=pyreadstat.read_sas7bdat(f, usecols=use)
    w=df["HV005"].to_numpy(float)/1e6
    age=df["HV105"].to_numpy(float); h121=df["HV121"].to_numpy(float); h122=df["HV122"].to_numpy(float)
    att=np.isin(h121,[1,2]).astype(float)          # attended during current school year (upper bound)
    m=(age>=14)&(age<=17)
    if "HV270" not in df.columns:
        print(wave,"no HV270; skipping"); continue
    q=df["HV270"].to_numpy(float)
    rec={"wave":wave,"age_group":"14-17","n":int(m.sum()),
         "attendance_pct":round(100*wshare(w[m],att[m]),1)}
    for qq in range(1,6):
        g=m&(q==qq)
        rec[f"q{qq}_n"]=int(g.sum())
        rec[f"q{qq}_att_pct"]=round(100*wshare(w[g],att[g]),1) if g.sum() else None
    non=m&(att==0)&np.isfinite(q)
    bot=non&(q<=2)
    rec["nonattenders_n"]=int(non.sum())
    rec["bottom40_share_of_nonattenders_pct"]=round(100*float(w[bot].sum()/w[non].sum()),1) if non.sum() else None
    rec["bottom40_share_of_all_pct"]=round(100*float(w[np.isfinite(q)&(q<=2)].sum()/w[np.isfinite(q)].sum()),1)
    rows.append(rec)
    print(wave, rec)

pd.DataFrame(rows).to_csv(os.path.join(OUT,"quintile_attendance_14_17.csv"), index=False)
print("\nwrote", os.path.join(OUT,"quintile_attendance_14_17.csv"))
