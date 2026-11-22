import gzip,json,os,numpy as np
SRC="/var/minis/workspace/atlas/research/records/2026-11-22-massification-panel/sources/wdi_sweep"
REG=json.load(open("/var/minis/workspace/wb_regions.json"))
REAL=set(REG)
def load(n):
    p=os.path.join(SRC,n+".json.gz")
    if not os.path.exists(p): p=os.path.join(SRC,n+".json")
    op=gzip.open(p) if p.endswith(".gz") else open(p)
    return {(r[0],int(r[1])):float(r[2]) for r in json.load(op) if r[2] is not None}
KS=["electricity","tax","gov_xpn","birth_reg","gdppc_log"]
V={k:load(k) for k in KS+["sec","lsc","ter","child_work"]}
print("coverage:",{k:len([1 for (i,y) in v if i in REAL]) for k,v in V.items()})
def panel(outcome):
    o=V[outcome]; rows=[]
    for (i,t),v in o.items():
        if i not in REAL or (i,t+10) not in o: continue
        if (i,t) not in V["electricity"]: continue
        r={"iso":i,"t":t,"d":o[(i,t+10)]-v,"own":v}
        for k in KS:
            r[k]=V[k].get((i,t))
        rows.append(r)
    return rows
def run(outcome,cf=False):
    rows=panel(outcome)
    assert rows
    for k in KS:
        v=np.array([r[k] if r[k] is not None else np.nan for r in rows],float)
        m,s=np.nanmean(v),np.nanstd(v)
        z=np.where(np.isnan(v),0.0,(v-m)/s if s>0 else 0.0)
        for r,x in zip(rows,z): r["z"+k]=x
    D=np.array([r["d"] for r in rows]); OWN=np.array([r["own"] for r in rows])
    decs=sorted({(r["t"]//10)*10 for r in rows})
    DEC=np.array([[1.0 if (r["t"]//10)*10==d else 0.0 for d in decs] for r in rows])
    isos=sorted({r["iso"] for r in rows}); II={c:i for i,c in enumerate(isos[1:])}
    FE=np.array([[1.0 if r["iso"]==c else 0.0 for c in isos[1:]] for r in rows])
    def fit(keys):
        X=np.column_stack([np.ones(len(rows)),OWN,DEC]+([FE] if cf else [])+[[r["z"+k] for r in rows] for k in keys])
        b=np.linalg.lstsq(X,D,rcond=None)[0]; u=D-X@b
        XtX=X.T@X; g=[II.get(r["iso"],-1) for r in rows]; meat=np.zeros_like(XtX)
        for c in set(g):
            m=(np.array(g)==c); s=X[m].T@u[m]; meat+=np.outer(s,s)
        Vb=np.linalg.pinv(XtX)@meat@np.linalg.pinv(XtX); se=np.sqrt(np.maximum(np.diag(Vb),0))
        off=2+len(decs)+(len(isos)-1 if cf else 0)
        return {k:(b[off+j],se[off+j]) for j,k in enumerate(keys)}, len(rows), len(isos)
    return rows,fit
for outcome,lab in (("sec","secondary completion"),("lsc","lower-secondary completion"),("ter","tertiary GER")):
    rows,fit=run(outcome)
    print(f"\n### 10-yr change in {lab}  (n={len(rows)}, {len({r['iso'] for r in rows})} countries)")
    print("   univariate:")
    for k in KS:
        d,_,_=fit([k]); b,s=d[k]; print(f"     {k:12s} {b:+6.2f} ({s:5.2f}) t={b/s:+5.2f}")
    for cf,lab2 in ((False,"all together, pooled"),(True,"all together + country FE")):
        d,_,_=fit(KS); print(f"   {lab2}:")
        for k in KS:
            b,s=d[k]; print(f"     {k:12s} {b:+6.2f} ({s:5.2f}) t={b/s:+5.2f}")
