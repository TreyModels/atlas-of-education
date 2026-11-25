#!/usr/bin/env python3
"""Philippines DHS: attendance by age/sex/residence and the 14-17 wealth-quintile
credential-floor profile. Reads Stata (.dta) and SAS7BDAT PR recodes via pyreadstat."""
import os, json, hashlib
import numpy as np, pandas as pd, pyreadstat

BASE = os.path.expanduser("~/neon-boot/pulled/dhs/philippines")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)
WAVES = {
    "2003": ("2003/PHPR41SD/PHPR41FL.SAS7BDAT", "sas"),
    "2008": ("2008/PHPR52SD/PHPR52FL.SAS7BDAT", "sas"),
    "2013": ("2013/PHPR62DT/PHPR62FL.DTA", "dta"),
    "2017": ("2017/PHPR71SD/PHPR71FL.SAS7BDAT", "sas"),
    "2022": ("2022/PHPR82DT/PHPR82FL.DTA", "dta"),
}
USE = ["HV021","HV022","HV024","HV025","HV005","HV104","HV105","HV121","HV122","HV270"]

def read(path, fmt):
    if fmt == "dta":
        df, meta = pyreadstat.read_dta(path, usecols=[c.lower() for c in USE])
        df.columns = [c.upper() for c in df.columns]
    else:
        df, meta = pyreadstat.read_sas7bdat(path, usecols=USE)
    return df

def taylor(df, ycol, by):
    rows = []
    for key, g in df.groupby(by, dropna=False):
        w = g["w"].to_numpy(float); y = g[ycol].to_numpy(float)
        sw = w.sum()
        if sw <= 0 or len(g) == 0: continue
        p = float((w*y).sum()/sw)
        z = w*(y-p)/sw
        cl = (pd.DataFrame({"h":g["HV022"].to_numpy(),"c":g["HV021"].to_numpy(),"z":z})
                .groupby(["h","c"], dropna=False)["z"].sum())
        var = 0.0
        for _, gg in cl.groupby(level=0):
            n = len(gg)
            if n > 1: var += n/(n-1)*float(((gg-gg.mean())**2).sum())
        se = float(np.sqrt(var))
        rec = dict(zip(by, key if isinstance(key, tuple) else (key,)))
        rec.update(n=len(g), pct=round(100*p,1), se=round(100*se,2),
                   ci_lo=round(100*(p-1.96*se),1), ci_hi=round(100*(p+1.96*se),1))
        rows.append(rec)
    return rows

frames=[]; catalog=[]
for wave,(rel,fmt) in WAVES.items():
    path=os.path.join(BASE,rel)
    print("reading",wave,"...",flush=True)
    df=read(path,fmt)
    df.columns=[c.upper() for c in df.columns]
    if df["HV121"].isna().all():
        print(f"  SKIP {wave}: HV121 all missing in this release"); continue
    df["w"]=df["HV005"]/1e6
    df=df[(df["HV105"]>=6)&(df["HV105"]<=17)].copy()
    df["att"]=df["HV121"].isin([1,2]).astype(float)
    df["age_group"]=pd.cut(df["HV105"],[5,11,14,17],labels=["6-11","12-14","15-17"])
    df["sex"]=df["HV104"].map({1:"Male",2:"Female"})
    df["res"]=df["HV025"].map({1:"Urban",2:"Rural"})
    df["wave"]=wave
    frames.append(df)
    h=hashlib.sha256(open(path,"rb").read()).hexdigest()
    catalog.append(dict(wave=wave,path=path,sha256=h,n_rows=int(len(df)),
                        hv121=sorted([float(x) for x in df["HV121"].dropna().unique()]),
                        n_missing_hv121=int(df["HV121"].isna().sum()),
                        n_missing_hv270=int(df["HV270"].isna().sum())))
    print(f"  {wave}: {len(df)} aged 6-17; HV121={catalog[-1]['hv121']}",flush=True)

allw=pd.concat(frames,ignore_index=True)
json.dump(catalog,open(os.path.join(OUT,"catalog.json"),"w"),indent=2)

# 14-17 by quintile + bottom-40 share
rows=[]
for wave in WAVES:
    d=allw[(allw.wave==wave)&(allw.HV105>=14)&(allw.HV105<=17)]
    if len(d)==0 or d["HV270"].isna().all(): continue
    rec={"wave":wave,"n":len(d),"attendance_pct":round(100*float((d["w"]*d["att"]).sum()/d["w"].sum()),1)}
    for q in range(1,6):
        g=d[d.HV270==q]
        rec[f"q{q}_n"]=int(len(g))
        rec[f"q{q}_att_pct"]=round(100*float((g["w"]*g["att"]).sum()/g["w"].sum()),1) if len(g) else None
    non=d[(d.att==0)&d.HV270.notna()]; bot=non[non.HV270<=2]
    rec["nonattenders_n"]=int(len(non))
    rec["bottom40_share_pct"]=round(100*float(bot["w"].sum()/non["w"].sum()),1) if len(non) else None
    rows.append(rec)
pd.DataFrame(rows).to_csv(os.path.join(OUT,"quintile_attendance_14_17.csv"),index=False)

# age x sex x residence
rows=[]
for r in taylor(allw,"att",["wave","age_group","sex","res"]):
    rows.append(r)
pd.DataFrame(rows).to_csv(os.path.join(OUT,"attendance_by_wave_sex_res.csv"),index=False)

print("\n=== 14-17 wealth-quintile credential-floor profile ===")
print(pd.DataFrame(rows).to_string() if False else pd.DataFrame(rows).head(0).to_string())
print(pd.read_csv(os.path.join(OUT,"quintile_attendance_14_17.csv")).to_string())
print("\n=== attendance by wave/age (national, both sexes) ===")
d=pd.read_csv(os.path.join(OUT,"attendance_by_wave_sex_res.csv"))
print(d.pivot_table(index="wave",columns="age_group",values="pct",aggfunc="mean").round(1).to_string())
print("\nwrote", OUT)
