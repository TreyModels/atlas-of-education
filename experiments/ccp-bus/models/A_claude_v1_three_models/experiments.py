"""Discriminating experiments for the three observationally-equivalent mechanism families.
E1 hysteresis sweep; E2 policy interventions; E3 critical slowing down; E4 robustness (LHS)."""
import json, sys, numpy as np, pandas as pd
from dataclasses import replace
from multiprocessing import Pool
from bus_mm import World, MODELS
R=json.load(open('calibrated_r.json'))
M={k:replace(v,r=R[k]) for k,v in MODELS.items()}
E0,EHI,BURN,H=0.35,0.70,150,40

def e1(args):
    name,seed=args; P=M[name]; w=World(replace(P,e=0.0),seed,x0=0.6); rows=[]
    for _ in range(BURN): w.step(replace(P,e=0.0))
    grid=np.round(np.r_[np.arange(0,0.901,0.03),np.arange(0.87,-0.001,-0.03)],3)
    for k,e in enumerate(grid):
        q=replace(P,e=float(e)); xs=[w.step(q)['x'] for _ in range(25)]
        rows.append(dict(model=name,seed=seed,e=e,leg='up' if k<=30 else 'down',x=np.mean(xs[-10:])))
    return rows

SCEN={'Status quo':lambda P,t:P,
      '5-yr campaign':lambda P,t:replace(P,e=EHI) if t<5 else P,
      '15-yr campaign':lambda P,t:replace(P,e=EHI) if t<15 else P,
      'Capacity x2.5':lambda P,t:replace(P,kappa=min(1.0,P.kappa*2.5)),
      'Open entry':lambda P,t:replace(P,rho=0.0,delta=0.0),
      'Open entry + 5-yr campaign':lambda P,t:replace(P,rho=0.0,delta=0.0,e=EHI if t<5 else P.e)}
def e2(args):
    name,seed,scen=args; P=replace(M[name],e=E0); w=World(P,seed,x0=0.6); rows=[]
    for _ in range(BURN): w.step(P)
    for t in range(H):
        st=w.step(SCEN[scen](P,t)); st.update(model=name,seed=seed,scenario=scen,year=t+1,cum_purged=w.cum_purged); rows.append(st)
    return rows

def e3(args):
    name,seed,e=args; P=replace(M[name],e=E0); w=World(P,seed,x0=0.6)
    for _ in range(BURN): w.step(P)
    q=replace(P,e=e); xs=np.array([w.step(q)['x'] for _ in range(350)])[150:]
    stayed=xs.mean()>0.1; d=xs-xs.mean()
    return dict(model=name,seed=seed,e=e,mean=xs.mean(),sd=xs.std(),ac1=(d[1:]*d[:-1]).mean()/d.var() if d.var()>0 else np.nan,stayed_high=stayed)

def lhs(n,seed=3):
    rng=np.random.default_rng(seed); u=(rng.permuted(np.tile(np.arange(n),(9,1)),axis=1).T+rng.random((n,9)))/n
    lo=np.array([-.5,4,.25,.5,.3,.03,.4,.2,.1]); hi=np.array([.5,8,.5,1.5,.9,.08,.9,.8,.5]); return lo+u*(hi-lo)
def e4(args):
    name,i,v,seed=args; P=M[name]
    q=replace(P,r=P.r+v[0],F=v[1],tau=v[2],e=E0)
    if name!='A: principal-agent': q=replace(q,h=v[3],phi=v[4],kappa=v[5])
    if name=='C: bus': q=replace(q,rho=v[6],delta=v[7],w=v[8])
    res={}
    for scen in ('Status quo','5-yr campaign'):
        w=World(q,seed,x0=0.6)
        for _ in range(BURN): w.step(q)
        xs=[w.step(SCEN[scen](q,t))['x'] for t in range(30)]; res[scen]=(np.mean(xs[-5:]),xs)
    sq=res['Status quo'][0]; ca=res['5-yr campaign'][0]
    return dict(model=name,draw=i,seed=seed,x_sq=sq,x_campaign_y30=ca,x_campaign_y5=res['5-yr campaign'][1][4],
                memory=(ca-sq)/max(sq,1e-3))

if __name__=='__main__':
    which=sys.argv[1:] or ['e1','e2','e3','e4']
    with Pool(2) as pool:
        if 'e1' in which:
            rows=sum(pool.map(e1,[(m,s) for m in M for s in range(4)]),[]); pd.DataFrame(rows).to_csv('e1_hysteresis.csv',index=False); print('e1 done')
        if 'e2' in which:
            rows=sum(pool.map(e2,[(m,s,sc) for m in M for s in range(12) for sc in SCEN]),[]); pd.DataFrame(rows).to_csv('e2_interventions.csv',index=False); print('e2 done')
        if 'e3' in which:
            rows=pool.map(e3,[(m,s,float(e)) for m in M for s in range(4) for e in np.round(np.arange(0.30,0.62,0.02),2)]); pd.DataFrame(rows).to_csv('e3_slowing.csv',index=False); print('e3 done')
        if 'e4' in which:
            X=lhs(48); rows=pool.map(e4,[(m,i,X[i],s) for m in M for i in range(48) for s in (101,102)]); pd.DataFrame(rows).to_csv('e4_robustness.csv',index=False); print('e4 done')
