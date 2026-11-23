import csv, numpy as np, json
OUT="/root/work/care_cred"
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
    return dict(n=int(n),b=b.tolist(),t=[float(b[i]/se[i]) if se[i]>0 else np.nan for i in range(k)],r2=float(r2))
def z(v):
    v=np.asarray(v,float); s=np.nanstd(v); return (v-np.nanmean(v))/(s if s>0 else 1.0)
cs=list(csv.DictReader(open(f"{OUT}/panel_cross_section.csv")))
att=np.array([num(r.get("edu_ter_f","")) for r in cs]); isco=np.array([num(r.get("isco12_f","")) for r in cs])
tfr=np.array([num(r.get("tfr","")) for r in cs]); urb=np.array([num(r.get("urban","")) for r in cs])
gdp=np.array([num(r.get("gdp_pc","")) for r in cs]); upsec=np.array([num(r.get("edu_upsec_f","")) for r in cs])
gap=att-isco
ok=np.isfinite(att)&np.isfinite(isco)&np.isfinite(tfr)
print("B sample: usable countries", int(ok.sum()))
def run(y,xs,lab,sub=None,names=("att","gap")):
    m=ok.copy() if sub is None else (ok&sub)
    X=[np.ones(m.sum())]+[z(x[m]) for x in xs]
    f=ols(z(y[m]),np.column_stack(X)); print("  %-28s n=%2d  " % (lab,f["n"]) + "  ".join(
        "%s b=%+.3f t=%+.2f" % (n,f["b"][i+1],f["t"][i+1]) for i,n in enumerate(names)) + " R2=%.3f"%f["r2"])
    return f
R={}
R["B1_att_only"]=run(tfr,[att],"attainment only",names=("att",))
R["B1_gap_only"]=run(tfr,[gap],"gap only",names=("gap",))
R["B1_race"]=run(tfr,[att,gap],"horse race")
R["B1_race_ctrl"]=run(tfr,[att,gap,gdp,urb],"horse race + gdp + urban")
med=np.nanmedian(att[ok]); print("B2 median tertiary attainment: %.1f%%" % med)
R["B2_high"]=run(tfr,[att,gap],"high-attainment (saturated)",sub=(att>=med))
R["B2_low"]=run(tfr,[att,gap],"low-attainment",sub=(att<med))
np.save("/tmp/gapdummy.npy",np.array([0]))
json.dump(R,open(f"{OUT}/results_B_clean.json","w"),indent=1)
# also: does attainment or gap predict better by R2 (B2 in the predictive sense)?
print("B2 R2 comparison: high %.3f vs low %.3f (gap-only: )" % (R["B2_high"]["r2"], R["B2_low"]["r2"]))
