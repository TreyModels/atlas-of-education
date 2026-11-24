import json,urllib.request,math,hashlib,sys
import numpy as np
API="https://api.worldbank.org/v2"
def wb(path):
    out=[]; page=1
    while True:
        sep="&" if "?" in path else "?"
        url=API+"/"+path+sep+"format=json&per_page=1000&page="+str(page)
        d=None
        for attempt in range(3):
            try:
                d=json.load(urllib.request.urlopen(url,timeout=45)); break
            except Exception as e:
                print("retry",attempt,type(e).__name__,flush=True)
        if d is None: break
        if len(d)<2 or d[1] is None: break
        out+=d[1]
        if page>=(d[0].get("pages") or 1): break
        page+=1
    return out
codes={"ger":"SE.PRM.ENRR","cmpt":"SE.PRM.CMPT.ZS","ptr":"SE.PRM.ENRL.TC.ZS","priv":"SE.PRM.PRIV.ZS","xpd":"SE.XPD.TOTL.GD.ZS","child":"SL.TLF.0714.ZS","gdppc":"NY.GDP.PCAP.KD","urb":"SP.URB.TOTL.IN.ZS","secf":"SE.SEC.ENRR.FE","tfr":"SP.DYN.TFRT.IN","gini":"SI.POV.GINI","sec":"SE.SEC.ENRR"}
ctry=set()
try:
    for c in wb("country"):
        if c.get("region",{}).get("value")!="Aggregates": ctry.add(c["id"])
except Exception as e:
    print("country fetch failed",repr(e)); sys.exit(1)
D={}
for k,code in codes.items():
    try:
        rows=wb("country/all/indicator/"+code+"?date=1990:2022")
    except Exception as e:
        print("skip",k,repr(e),flush=True); continue
    n=0
    for r in rows:
        iso=r.get("countryiso3code")
        if iso in ctry and r.get("value") is not None:
            D.setdefault((iso,int(r["date"])),{})[k]=float(r["value"]); n+=1
    print("pulled",k,n,flush=True)
def panel(y,x,ctrl=()):
    rows=[]
    for iso in ctry:
        ys=sorted([yy for (i,yy) in D if i==iso])
        for a,b in zip(ys,ys[1:]):
            if b-a!=1: continue
            ra,rb=D[(iso,a)],D[(iso,b)]
            if y not in ra or y not in rb or x not in ra or x not in rb: continue
            if any(c not in ra or c not in rb for c in ctrl): continue
            yy=(math.log(max(rb["gdppc"],1e-6))-math.log(max(ra["gdppc"],1e-6))) if y=="log_gdppc" else rb[y]-ra[y]
            xx=(math.log(max(rb["ptr"],1e-6))-math.log(max(ra["ptr"],1e-6))) if x=="log_ptr" else rb[x]-ra[x]
            rows.append((iso,b,yy,xx,[rb[c]-ra[c] for c in ctrl]))
    return rows
def fit(rows,ctrl,wins):
    if len(rows)<200: return None
    X=[np.ones(len(rows)),np.array([r[3] for r in rows])]
    for j in range(len(ctrl)): X.append(np.array([r[4][j] for r in rows]))
    X=np.column_stack(X); y=np.array([r[2] for r in rows],float); x=X[:,1].copy(); yv=y.copy()
    if wins:
        lo,hi=np.percentile(yv,[1,99]); yv=np.clip(yv,lo,hi); lo,hi=np.percentile(x,[1,99]); x=np.clip(x,lo,hi); X[:,1]=x
    b,*_=np.linalg.lstsq(X,yv,rcond=None); e=yv-X@b; G=np.array([r[0] for r in rows]); Xi=np.linalg.pinv(X.T@X); m=np.zeros((X.shape[1],X.shape[1]))
    for g in set(G.tolist()):
        z=G==g; s=X[z].T@e[z]; m+=np.outer(s,s)
    V=Xi@m@Xi; return b,float(np.sqrt(max(V[1,1],0)))
def oos(y,x,ctrl):
    rows=panel(y,x,ctrl)
    if len(rows)<400: return {"ok":False,"n":len(rows),"reason":"insufficient"}
    cs=sorted(set(r[0] for r in rows)); fold={c:int(hashlib.md5(c.encode()).hexdigest(),16)%5 for c in cs}
    mr=[]; pr=[]; nr=[]; br=[]
    for k in range(5):
        tr=[r for r in rows if fold[r[0]]!=k and r[1]<=2010]; te=[r for r in rows if fold[r[0]]==k and r[1]>2010]
        if len(tr)<200 or len(te)<10: continue
        f=fit(tr,ctrl,False)
        if f is None: continue
        b=f[0]; ty=np.array([r[2] for r in te]); tx=np.array([r[3] for r in te]); mean_tr=float(np.mean([r[2] for r in tr]))
        prd=b[0]+b[1]*tx
        mr.append(float(np.sqrt(np.mean((ty-prd)**2)))); pr.append(float(np.sqrt(np.mean(ty**2)))); nr.append(float(np.sqrt(np.mean((ty-mean_tr)**2)))); br.append(b[1])
    if not mr: return {"ok":False,"n":len(rows),"reason":"no folds"}
    f=fit(rows,ctrl,False); beta,se=f
    return {"ok":True,"n":len(rows),"model_rmse":float(np.mean(mr)),"persistence_rmse":float(np.mean(pr)),"null_rmse":float(np.mean(nr)),"folds_beat":int(sum(1 for a,b_,c in zip(mr,pr,nr) if a<min(b_,c))),"beta":float(beta[1]),"se":float(se),"ci":[float(beta[1]-1.96*se),float(beta[1]+1.96*se)]}
FAM={"F2_supply":("ger","log_ptr",("priv","xpd")),"F6_growth":("log_gdppc","ger",("child","urb")),"F7_inequality":("gini","sec",()),"F9_fertility":("tfr","secf",()),"F10_measurement":("cmpt","ger",())}
res={"data":{"countries":len(ctry),"obs":len(D)},"families":{},"tierB":{},"tierC":{}}
for name,(y,x,ctrl) in FAM.items():
    r=oos(y,x,ctrl)
    signs=[]
    if r.get("ok"):
        for wins in (False,True):
            for cs in ((),ctrl,tuple(ctrl)+("urb",)):
                rr=oos(y,x,cs)
                if rr.get("ok"): signs.append(np.sign(rr["beta"]))
    share=float(np.mean([1 if s==np.sign(r.get("beta",0)) else 0 for s in signs])) if signs else 0.0
    beats=bool(r.get("folds_beat",0)>=3 and r.get("model_rmse",9e9)<min(r.get("persistence_rmse",9e9),r.get("null_rmse",9e9)))
    ci=r.get("ci",[0,0]); excl=bool(ci[0]>0 or ci[1]<0)
    v="SUPPORTED" if (r.get("ok") and beats and excl and share>=0.8) else ("NOT IDENTIFIED" if not r.get("ok") else "REJECTED")
    res["families"][name]=dict(r,spec_share=share,n_variants=len(signs),verdict=v)
    print(name,v,{k:(round(r[k],4) if isinstance(r.get(k),float) else r.get(k)) for k in ("model_rmse","persistence_rmse","null_rmse","folds_beat","n","beta","se")},"spec",round(share,2),flush=True)
def recovery(btrue=0.30,nrep=100):
    rng=np.random.default_rng(7); cov=0; bias=[]
    for rep in range(nrep):
        C=120; T=30; rows=[]
        for c in range(C):
            for t in range(T):
                xx=rng.normal(); yy=btrue*xx+rng.normal(0,1); rows.append(("C"+str(c),t,yy,xx))
        X=np.column_stack([np.ones(len(rows)),np.array([r[3] for r in rows])]); yv=np.array([r[2] for r in rows])
        b,*_=np.linalg.lstsq(X,yv,rcond=None); e=yv-X@b; G=np.array([r[0] for r in rows]); Xi=np.linalg.inv(X.T@X); m=np.zeros((2,2))
        for g in set(G.tolist()):
            z=G==g; s=X[z].T@e[z]; m+=np.outer(s,s)
        se=math.sqrt(max((Xi@m@Xi)[1,1],0)); bias.append(b[1]-btrue); cov+=int(abs(b[1]-btrue)<=1.96*se)
    return {"btrue":btrue,"mean_bias":float(np.mean(bias)),"coverage":cov/nrep,"n_rep":nrep}
rb=recovery(); ok=abs(rb["mean_bias"])<0.05 and rb["coverage"]>=0.85
res["tierB"]["F5_credentials_synthetic"]=dict(rb,verdict="RECOVERED" if ok else "NOT IDENTIFIED")
print("TierB F5_credentials",res["tierB"]["F5_credentials_synthetic"]["verdict"],"bias",round(rb["mean_bias"],3),"coverage",round(rb["coverage"],3),flush=True)
res["tierC"]={"F1_demand":"micro affordability UNTESTABLE (no public fees/income)","F3_learning":"grade-level annual profile UNTESTABLE","F4_gates":"exam/admission rules UNTESTABLE","F8_shadow":"causal claim UNTESTABLE"}
json.dump(res,open("/root/work/testbench/results.json","w"),indent=1)
print("DONE_JSON_WRITTEN",flush=True)
