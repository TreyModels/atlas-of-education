import csv, numpy as np, json
OUT="/root/work/care_cred"
def load(p): return list(csv.DictReader(open(p)))
def num(x):
    try:
        v=float(x); return v if np.isfinite(v) else np.nan
    except Exception: return np.nan
def ols(y,X):
    y=np.asarray(y,float); X=np.asarray(X,float)
    ok=np.isfinite(y)&np.all(np.isfinite(X),axis=1); y,X=y[ok],X[ok]; n,k=X.shape
    inv=np.linalg.pinv(X.T@X); b=inv@X.T@y; e=y-X@b
    covh=inv@(X.T*e**2)@X@inv*(n/(n-k)); se=np.sqrt(np.maximum(np.diag(covh),0))
    r2=1-(e@e)/max(((y-y.mean())**2).sum(),1e-12)
    return dict(n=int(n),b=b.tolist(),se=se.tolist(),t=[float(b[i]/se[i]) for i in range(k)],r2=float(r2))
def z(v):
    v=np.asarray(v,float); s=np.nanstd(v); return (v-np.nanmean(v))/(s if s>0 else 1.0)
allr=load(f"{OUT}/panel_all.csv"); cs=load(f"{OUT}/panel_cross_section.csv")
R={}
# A2: change in fertility vs early care share
by={}
for r in allr: by.setdefault(r["iso"],[]).append(r)
P=[]
for iso,rs in by.items():
    rs=sorted(rs,key=lambda r:int(r["year"]))
    if len(rs)<2: continue
    y0,y1=rs[0],rs[-1]
    c0,t0,t1=(num(y0.get("care_f","")),num(y0.get("tfr","")),num(y1.get("tfr","")))
    if np.isfinite(c0) and np.isfinite(t0) and np.isfinite(t1):
        P.append(dict(iso=iso,care0=c0,dtfr=t1-t0,tfr0=t0,y0=int(y0["year"]),y1=int(y1["year"]),gdp=num(y0.get("gdp_pc",""))))
X=np.column_stack([np.ones(len(P)), z([p["care0"] for p in P])])
R["A2_raw"]=ols(z([p["dtfr"] for p in P]),X)
lg=np.log(np.maximum([p["gdp"] for p in P],1.0))
X2=np.column_stack([np.ones(len(P)), z([p["care0"] for p in P]), z(lg)])
R["A2_with_gdp"]=ols(z([p["dtfr"] for p in P]),X2)
print("A2 (n=%d): care coefficient b=%.3f t=%.2f | with log GDP b=%.3f t=%.2f" % (
    R["A2_raw"]["n"], R["A2_raw"]["b"][1], R["A2_raw"]["t"][1], R["A2_with_gdp"]["b"][1], R["A2_with_gdp"]["t"][1]))
# B2: saturation split, clean
att=np.array([num(r.get("edu_ter_f","")) for r in cs]); gap=np.array([num(r.get("gap","")) for r in cs]); tfr=np.array([num(r.get("tfr","")) for r in cs])
ok=np.isfinite(att)&np.isfinite(gap)&np.isfinite(tfr); print("B2 usable countries:", int(ok.sum()))
med=np.nanmedian(att[ok])
for lab,m in (("above_median",ok&(att>=med)),("below_median",ok&(att<med))):
    X=np.column_stack([np.ones(m.sum()), z(att[m]), z(gap[m])])
    f=ols(z(tfr[m]),X)
    print("  %-13s n=%2d  attainment b=%+.3f t=%+.2f | gap b=%+.3f t=%+.2f | R2=%.3f" % (
        lab, f["n"], f["b"][1], f["t"][1], f["b"][2], f["t"][2], f["r2"]))
    R[f"B2_{lab}"]=f
# clean horse race on the same rows
X=np.column_stack([np.ones(ok.sum()), z(att[ok]), z(gap[ok])])
R["B1_horse_race_clean"]=ols(z(tfr[ok]),X)
print("B1 horse race (n=%d): attainment b=%+.3f t=%+.2f | gap b=%+.3f t=%+.2f R2=%.3f" % (
    ok.sum(), R["B1_horse_race_clean"]["b"][1], R["B1_horse_race_clean"]["t"][1],
    R["B1_horse_race_clean"]["b"][2], R["B1_horse_race_clean"]["t"][2], R["B1_horse_race_clean"]["r2"]))
json.dump(R, open(f"{OUT}/results_fixes.json","w"), indent=1)
