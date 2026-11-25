#!/usr/bin/env python3
"""Vietnam DHS/AIS: secondary completion by wealth quintile, cohorts 20-24 / 25-29."""
import os, json, hashlib
import numpy as np, pandas as pd, pyreadstat

BASE = os.path.expanduser("~/neon-boot/pulled/dhs/vietnam")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)
PR = {"1997": BASE+"/1997/VNPR31DT/VNPR31FL.DTA",
      "2002": BASE+"/2002/VNPR41DT/VNPR41FL.DTA",
      "2005ais": BASE+"/2005ais/VNPR53DT/VNPR53FL.DTA"}
WI = {"1997": BASE+"/1997/VNWI31DT/VNWI31FL.DTA",
      "2002": BASE+"/2002/VNWI41DT/VNWI41FL.DTA"}

def norm(s):
    return " ".join(str(s).split())

def read(f):
    df, _ = pyreadstat.read_dta(f)
    df.columns = [c.upper() for c in df.columns]
    return df

def wmean(df, y):
    if len(df) == 0: return float("nan")
    w = df["w"].to_numpy(float); y = np.asarray(y, float)
    return float((w*y).sum()/w.sum())

rows=[]; catalog=[]
for wave, prf in PR.items():
    df = read(prf)
    df["w"] = df["HV005"]/1e6
    df["HHID_N"] = df["HHID"].map(norm) if "HHID" in df.columns else None
    if wave in WI:
        wi = read(WI[wave])
        wi["HHID_N"] = wi["WHHID"].map(norm)
        wi = wi[["HHID_N","WLTHIND5"]].rename(columns={"WLTHIND5":"q"})
        df = df.merge(wi, on="HHID_N", how="left")
    else:
        df["q"] = df["HV270"]
    df["completed_sec"] = np.where(df["HV109"].isin([4,5]), 1.0,
                           np.where(df["HV109"].isin([0,1,2,3]), 0.0, np.nan))
    catalog.append(dict(wave=wave, path=prf, sha256=hashlib.sha256(open(prf,"rb").read()).hexdigest(),
                        n_rows=int(len(df)), q_missing=int(df["q"].isna().sum()),
                        completed_sec_missing=int(np.isnan(df["completed_sec"]).sum())))
    for cohort, lo, hi in [("20-24",20,24),("25-29",25,29)]:
        d = df[(df["HV105"]>=lo)&(df["HV105"]<=hi)&df["q"].notna()&df["completed_sec"].notna()].copy()
        if len(d)==0: continue
        rec = {"wave":wave,"cohort":cohort,"n":len(d),
               "completed_sec_pct":round(100*wmean(d,d["completed_sec"]),1)}
        for qq in range(1,6):
            g=d[d.q==qq]; rec[f"q{qq}_n"]=len(g)
            rec[f"q{qq}_comp_pct"]=round(100*wmean(g,g["completed_sec"]),1) if len(g) else None
        non=d[d.completed_sec==0]
        bot=non[non.q<=2]
        rec["noncompleters_n"]=len(non)
        rec["bottom40_share_of_noncompleters_pct"]=round(100*float(bot["w"].sum()/non["w"].sum()),1) if len(non) else None
        rows.append(rec)
        print(wave, cohort, rec)
pd.DataFrame(rows).to_csv(os.path.join(OUT,"vn_completion_by_quintile.csv"), index=False)
json.dump(catalog, open(os.path.join(OUT,"catalog.json"),"w"), indent=2)
print("\nwrote", OUT)
