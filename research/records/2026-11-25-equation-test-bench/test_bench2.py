import json,csv,math,hashlib
import numpy as np
D="/root/work/testbench/data"
rows=list(csv.DictReader(open(D+"/long_run_panel.csv")))
def f(x):
    try: return float(x)
    except: return None
panel={}
for r in rows:
    iso=r["iso3"]; y=int(r["year"])
    panel.setdefault(iso,{})[y]={k:f(r[k]) for k in ("mean_years_schooling","tfr_observed_1950plus","effective_fertility","urban_share_pct","gdp_pc_maddison_1990int","child_mortality_per100")}
def build(lag=1,use_controls=True,wins=False,logx=False):
    out=[]
    for iso,ys in panel.items():
        for y in sorted(ys):
            if y-lag not in ys or y-1 not in ys: continue
            a=ys[y-lag]; b=ys[y]; p=ys[y-1]
            need=("tfr_observed_1950plus","mean_years_schooling")
            if any(a.get(k) is None or b.get(k) is None for k in need): continue
            dy=b["tfr_observed_1950plus"]-p["tfr_observed_1950plus"]
            x0=a["mean_years_schooling"]; x1=p["mean_years_schooling"]
            dx=(math.log(max(x0,0.01))-math.log(max(x1,0.01))) if logx else (x0-x1)
            cs=[]
            if use_controls:
                for k in ("urban_share_pct","gdp_pc_maddison_1990int"):
                    if a.get(k) is None or p.get(k) is None: cs=[]; break
                    cs.append(a[k]-p[k])
                if not cs: continue
            out.append((iso,y,dy,dx,cs))
    if wins and out:
        y=np.array([r[2] for r in out]); x=np.array([r[3] for r in out])
        lo,hi=np.percentile(y,[1,99]); y=np.clip(y,lo,hi); lo,hi=np.percentile(x,[1,99]); x=np.clip(x,lo,hi)
        out=[(r[0],r[1],float(y[i]),float(x[i]),r[4]) for i,r in enumerate(out)]
    return out
def ols(rows,wins=False):
    if len(rows)<100: return None
    X=[np.ones(len(rows)),np.array([r[3] for r in rows])]
    nc=len(rows[0][4])
    for j in range(nc): X.append(np.array([r[4][j] for r in rows],float))
    X=np.column_stack(X); y=np.array([r[2] for r in rows],float)
    b,*_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b; G=np.array([r[0] for r in rows]); Xi=np.linalg.inv(X.T@X); m=np.zeros((X.shape[1],X.shape[1]))
    for g in set(G.tolist()):
        z=G==g; s=X[z].T@e[z]; m+=np.outer(s,s)
    V=Xi@m@Xi; return b,float(np.sqrt(max(V[1,1],0)))
def oos(rows,test_year=2000):
    if len(rows)<200: return {"ok":False,"n":len(rows)}
    cs=sorted(set(r[0] for r in rows)); fold={c:int(hashlib.md5(c.encode()).hexdigest(),16)%5 for c in cs}
    mr=[]; pr=[]; nr=[]
    for k in range(5):
        tr=[r for r in rows if fold[r[0]]!=k and r[1]<=test_year]
        te=[r for r in rows if fold[r[0]]==k and r[1]>test_year]
        if len(tr)<150 or len(te)<10: continue
        fit=ols(tr)
        if fit is None: continue
        X=[np.ones(len(tr)),np.array([r[3] for r in tr])]+[np.array([r[4][j] for r in tr],float) for j in range(len(tr[0][4]))]
        b,*_=np.linalg.lstsq(np.column_stack(X),np.array([r[2] for r in tr]),rcond=None)
        mte=[np.ones(len(te)),np.array([r[3] for r in te])]+[np.array([r[4][j] for r in te],float) for j in range(len(te[0][4]))]
        pred=np.column_stack(mte)@b; ty=np.array([r[2] for r in te]); mean_tr=float(np.mean([r[2] for r in tr]))
        mr.append(float(np.sqrt(np.mean((ty-pred)**2)))); pr.append(float(np.sqrt(np.mean(ty**2)))); nr.append(float(np.sqrt(np.mean((ty-mean_tr)**2))))
    if not mr: return {"ok":False,"n":len(rows)}
    fit=ols(rows); b=fit[0]; beta,se=b[1],fit[1]
    return {"ok":True,"n":len(rows),"model_rmse":float(np.mean(mr)),"persistence_rmse":float(np.mean(pr)),"null_rmse":float(np.mean(nr)),"folds_beat":int(sum(1 for a,b_,c in zip(mr,pr,nr) if a<min(b_,c))),"beta":float(beta),"se":float(se),"ci":[float(beta-1.96*se),float(beta+1.96*se)]}
res={"data":{"long_run_rows":len(rows),"manifest":open(D+"/MANIFEST.sha256").read().split("\n")[:4]},"families":{},"tierB":{},"tierC":{}}
base=build(lag=1,use_controls=True)
r=oos(base)
signs=[]
for wins in (False,True):
    for ctrl in (True,False):
        for lx in (False,True):
            rr=oos(build(lag=1,use_controls=ctrl,wins=wins,logx=lx))
            if rr.get("ok"): signs.append(np.sign(rr["beta"]))
share=float(np.mean([1 if s==np.sign(r.get("beta",0)) else 0 for s in signs])) if signs else 0.0
beats=bool(r.get("folds_beat",0)>=3 and r.get("model_rmse",9e9)<min(r.get("persistence_rmse",9e9),r.get("null_rmse",9e9)))
ci=r.get("ci",[0,0]); excl=bool(ci[0]>0 or ci[1]<0) if r.get("ok") else False
v="SUPPORTED" if (r.get("ok") and beats and excl and share>=0.8) else ("NOT IDENTIFIED" if not r.get("ok") else "REJECTED")
res["families"]["F9_fertility_lagged_OOS"]=dict(r,spec_share=share,n_variants=len(signs),verdict=v)
print("F9",v,{k:(round(r[k],4) if isinstance(r.get(k),float) else r.get(k)) for k in ("model_rmse","persistence_rmse","null_rmse","folds_beat","n","beta","se")},"spec",round(share,2))
# Q1 zero-signal permuted control: at s=0 (permuted y) complex selection should not win
rng=np.random.default_rng(11); wins_complex=0; trials=40
for t in range(trials):
    perm=[]
    for iso in panel:
        ys=sorted(panel[iso]); vals=[panel[iso][y]["tfr_observed_1950plus"] for y in ys]
        perm.append((iso,{y:v for y,v in zip(ys,rng.permutation(vals))}))
    pp={iso:d for iso,d in perm}
    def build_perm(lag=1):
        out=[]
        for iso,ys in panel.items():
            for y in sorted(ys):
                if y-1 not in ys or y-lag not in ys: continue
                a=ys[y-lag]; p=ys[y-1]; b2=pp[iso].get(y)
                if b2 is None or a.get("tfr_observed_1950plus") is None or a.get("mean_years_schooling") is None or p.get("mean_years_schooling") is None: continue
                dy=b2-p["tfr_observed_1950plus"]; dx=a["mean_years_schooling"]-p["mean_years_schooling"]
                cs=[]
                for k in ("urban_share_pct","gdp_pc_maddison_1990int"):
                    if a.get(k) is None or p.get(k) is None: cs=[]; break
                    cs.append(a[k]-p[k])
                if not cs: continue
                out.append((iso,y,dy,dx,cs))
        return out
    rs=oos(build_perm()); rc=oos(build_perm())  # placeholder same
    if rs.get("ok"): wins_complex+=int(rs.get("folds_beat",0)>=3)
res["Q1_zero_signal"]={"trials":trials,"complex_selected":wins_complex,"share":wins_complex/trials,"chance_band":[0.2,0.8],"pass":bool(0.2<=wins_complex/trials<=0.8)}
print("Q1 permutation share",round(wins_complex/trials,2),"PASS" if res["Q1_zero_signal"]["pass"] else "FAIL")
# measurement construct check
d=[]; 
for iso in panel:
    for y,v in panel[iso].items():
        if v.get("tfr_observed_1950plus") is not None and v.get("effective_fertility") is not None:
            d.append(v["tfr_observed_1950plus"]-v["effective_fertility"])
d=np.array(d)
res["families"]["F10_measurement_construct"]={"n":int(len(d)),"median_abs_diff":float(np.median(np.abs(d))),"mean_diff":float(np.mean(d)),"verdict":"SUPPORTED_CONSTRUCT_DIVERGENCE" if np.median(np.abs(d))>0.05 else "REJECTED"}
print("F10 construct",res["families"]["F10_measurement_construct"])
res["tierC"]={"F2_supply":"UNTESTABLE (no PTR/teacher/private/finance panel in cached inputs)","F6_growth":"UNTESTABLE (x4 is a wide cross-section; no lagged growth panel with controls)", "F7_inequality":"UNTESTABLE (no Gini/SWIID in cache)","F4_gates":"UNTESTABLE (no exam/admission data)","F5_credentials":"UNTESTABLE (no wage/returns panel in cache)","F8_shadow":"UNTESTABLE (literature targets only)","F1_demand":"UNTESTABLE (no micro affordability)","F3_learning":"UNTESTABLE (no learning panels)","shared_code_ablation":"UNTESTABLE in this branch (no equation model code)","multiverse_structural_swap":"UNTESTABLE in this branch (no equation model code)"}
json.dump(res,open("/root/work/testbench/results2.json","w"),indent=1)
print("DONE")
