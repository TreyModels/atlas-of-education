import gzip,json,os,numpy as np
SRC="/var/minis/workspace/atlas/research/records/2026-11-22-massification-panel/sources/wdi_sweep"
REG=json.load(open("/var/minis/workspace/wb_regions.json")); REAL=set(REG)
def load(n):
    p=os.path.join(SRC,n+".json.gz")
    if not os.path.exists(p): p=os.path.join(SRC,n+".json")
    op=gzip.open(p) if p.endswith(".gz") else open(p)
    return {(r[0],int(r[1])):float(r[2]) for r in json.load(op) if r[2] is not None}
V={k:load(k) for k in ["electricity","tax","gov_xpn","birth_reg","gdppc_log","sec","lsc","ter","child_work","urban","life_exp"]}

def reg(y_key, x_keys, own_key=None, fe=True):
    y=V[y_key]; own=V[own_key] if own_key else y
    rows=[]
    for (i,t),v in y.items():
        if i not in REAL or (i,t+10) not in y: continue
        if (i,t) not in V["electricity"]: continue
        d=dict(iso=i,t=t,dv=y[(i,t+10)]-v,own=own.get((i,t),v))
        ok=True
        for k in x_keys:
            if (i,t) not in V[k]: ok=False; break
            d[k]=V[k][(i,t)]
        if ok: rows.append(d)
    if len(rows)<80: return None
    for k in x_keys:
        a=np.array([r[k] for r in rows]); s=a.std()
        for r in rows: r["z"+k]=(r[k]-a.mean())/s if s>0 else 0.0
    D=np.array([r["dv"] for r in rows]); OWN=np.array([r["own"] for r in rows])
    decs=sorted({(r["t"]//10)*10 for r in rows})
    cols=[np.ones(len(rows)),OWN]+[np.array([1.0 if (r["t"]//10)*10==d else 0.0 for r in rows]) for d in decs[1:]]
    isos=sorted({r["iso"] for r in rows}); II={c:i for i,c in enumerate(isos[1:])}
    if fe:
        cols+=[np.array([1.0 if r["iso"]==c else 0.0 for r in rows]) for c in isos[1:]]
    cols+=[np.array([r["z"+k] for r in rows]) for k in x_keys]
    X=np.column_stack(cols)
    b=np.linalg.lstsq(X,D,rcond=None)[0]; u=D-X@b
    XtX=X.T@X; g=np.array([II.get(r["iso"],0) for r in rows]); meat=np.zeros_like(XtX)
    for c in set(g.tolist()):
        m=(g==c); s=X[m].T@u[m]; meat+=np.outer(s,s)
    Vb=np.linalg.pinv(XtX)@meat@np.linalg.pinv(XtX); se=np.sqrt(np.maximum(np.diag(Vb),0))
    off=X.shape[1]-len(x_keys)
    return {k:(b[off+j],se[off+j]) for j,k in enumerate(x_keys)}, len(rows), len(isos), X.shape[1]

print("=== Does electricity predict STATE-ARRIVAL outcomes with no technological channel?")
print("    (10-yr changes, country FE, decade dummies, own level, cluster SE)")
for yk,lab in (("tax","tax revenue/GDP"),("gov_xpn","government expenditure/GDP"),("birth_reg","birth registration")):
    r=reg(yk,["electricity"])
    if r:
        b,s=r[0]["electricity"]; n,nc=r[1],r[2]; print(f"  electricity -> {lab:28s} {b:+.3f} ({s:.3f}) t={b/s:+5.2f}  n={n}, cty={nc}")
print("\n=== Does electricity predict TECHNOLOGY outcomes?")
for yk,lab in (("child_work","child labour"),):
    r=reg(yk,["electricity"])
    if r: b,s=r[0]["electricity"]; print(f"  electricity -> {lab:28s} {b:+.3f} ({s:.3f}) t={b/s:+5.2f}  n={r[1]}, cty={r[2]}")
print("\n=== Horse race WITH country FE (regression now):")
for yk,lab in (("sec","secondary completion"),("lsc","lower-secondary"),("ter","tertiary GER")):
    r=reg(yk,["electricity","tax","gov_xpn","birth_reg","gdppc_log"])
    if not r: continue
    print(f"  {lab} (n={r[1]}, cty={r[2]}, k={r[3]})")
    for k in ["electricity","tax","gov_xpn","birth_reg","gdppc_log"]:
        b,s=r[0][k]; print(f"     {k:12s} {b:+6.2f} ({s:5.2f}) t={b/s:+5.2f}")
