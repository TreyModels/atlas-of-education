"""Pattern-oriented ABC for bus_v3 (Grimm et al. 2005): a draw must reproduce qualitative patterns
P2-P5 before its fit to the case series (P1) counts.
P1 CCDI cases filed 2013-2025, log shape normalised to 2018-2021 (distance = RMSE)
P2 leader's network nearly exempt: removal rate of core members < 0.3 x targeted (Lorentzen & Lu; Zeng & Yang)
P3 contagion: removal hazard after a tied official is removed is >= 1.5x (Wang et al., encircling)
P4 networks go covert: hidden share of ties in 2025 >= 0.10 (Ruan, Lu & Ruan 2026)
P5 the leader's own cliques: a split-off 'adjacent' faction is targeted between 2018 and 2026 (PLA 2023-26)
Then, among accepted runs: what predicts removal 2013-2025?"""
import numpy as np, pandas as pd, sys
from dataclasses import replace
from multiprocessing import Pool
import bus_v3 as W
YRS=list(range(2013,2026)); obs=W.V.DATA.ccdi_cases_filed_10k
obs_s=np.log(obs.loc[YRS]/obs.loc[2018:2021].mean()).to_numpy()
PRIOR=dict(r0=(-2.5,2.5),beta=(0,1.5),c_fin=(0.05,0.5),bP=(0,1.5),F=(3,8),e_scale=(0.6,1.4),kappa0=(0.01,0.08),
           m2018=(1,2.5),m2024=(1,2.5),xi=(0.3,0.95),gamma=(0,5),c_vis=(0,0.4),pi_pol=(0,0.03),
           eta=(0,1),b_wagon=(0,0.6),s_threat=(0.05,0.2))
def auc(score,y):
    o=np.argsort(score,kind='mergesort'); r=np.empty(len(score)); r[o]=np.arange(1,len(score)+1)
    # average ranks for ties
    s=pd.Series(score); r=s.rank().to_numpy(); n1=y.sum(); n0=len(y)-n1
    return (r[y==1].sum()-n1*(n1+1)/2)/max(n1*n0,1)
def evaluate(args):
    model,i,th=args
    p=replace(W.P3(),**th); p={'A':W.A3,'K':W.K3}.get(model,lambda q:q)(p)
    d,rec=W.simulate3(p,seed=5000+i,end=2025,keep_records=True); d=d.set_index('year')
    c=d.cases_civ.astype(float)+0.5; sim=np.log(c.loc[YRS]/c.loc[2018:2021].mean()).to_numpy()
    R=[];S=[];ST=[];DEG=[];H=[]
    for y in YRS:
        rem,s,stat,deg,hs=rec[y]; R.append(rem);S.append(s);ST.append(stat);DEG.append(deg);H.append(hs)
    R=np.concatenate(R).astype(int);S=np.concatenate(S).astype(int);ST=np.concatenate(ST);DEG=np.concatenate(DEG);H=np.concatenate(H)
    rate=lambda m: R[m].mean() if m.any() else np.nan
    core=rate(ST=='core'); tg=rate(ST=='targeted')
    st_rate=pd.Series(R).groupby(ST).transform('mean').to_numpy()
    ev=d.attrs['events']
    p5=any(e[2]=='targeted_adjacent' and 2018<=e[0]<=2026 for e in ev)
    hr=np.nanmean(d.contagion_hr.loc[YRS].replace([np.inf],np.nan))
    return dict(model=model,draw=i,**th,dist=float(np.sqrt(np.mean((sim-obs_s)**2))),
        rr_core_tgt=core/tg if tg>0 else np.nan,contagion_hr=hr,hidden2025=d.hidden_share.loc[2025],p5=p5,
        x2012=d.x.loc[2012],x2025=d.x.loc[2025],political_share=R[(S==0)].sum()/max(R.sum(),1),
        auc_faction=auc(st_rate,R),auc_corrupt=auc(S.astype(float),R),auc_degree=auc(-DEG,R),auc_hidden=auc(-H,R),
        rr_tgt_vs_rest=tg/max(rate(ST!='targeted'),1e-9),rr_corrupt=rate(S==1)/max(rate(S==0),1e-9),
        **{f'sim{y}':v for y,v in zip(YRS,sim)})
MODELS={'C':300,'A':150,'K':150}
if __name__=='__main__':
    rng=np.random.default_rng(7); jobs=[]
    for m,n in MODELS.items():
        for i in range(n): jobs.append((m,i,{k:float(rng.uniform(*v)) for k,v in PRIOR.items()}))
    with Pool(2) as pool: res=pool.map(evaluate,jobs,chunksize=3)
    df=pd.DataFrame(res); df.to_csv('abc_v3_all.csv',index=False)
    df['P0']=df.x2012.between(0.05,0.60); df['P2']=df.rr_core_tgt<0.3; df['P3']=df.contagion_hr>=1.5
    df['P4']=df.hidden2025>=0.10; df['P5']=df.p5
    print('share passing each pattern:'); print(df.groupby('model')[['P0','P2','P3','P4','P5']].mean().round(2))
    ok=df[df[['P0','P2','P3','P4','P5']].all(axis=1)]
    print('passing all patterns:',ok.model.value_counts().to_dict())
    print('best case-series distance among pattern-passers:',ok.groupby('model').dist.min().round(3).to_dict())
    tol=ok.dist.quantile(0.25) if len(ok) else np.nan; acc=ok[ok.dist<=tol]; acc.to_csv('abc_v3_accepted.csv',index=False)
    print(f'accepted (pattern-passers within 25th pct distance, tol={tol:.3f}):',acc.model.value_counts().to_dict())
    cols=['auc_faction','auc_corrupt','auc_degree','auc_hidden','rr_tgt_vs_rest','rr_corrupt','rr_core_tgt','contagion_hr','political_share','hidden2025','x2012','x2025']
    print(acc.groupby('model')[cols].median().round(3).T)
    q=acc[acc.model=='C'][list(PRIOR)].quantile([.1,.5,.9]).T; print(q.round(3))
