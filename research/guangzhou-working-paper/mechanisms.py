"""Mechanism checks on a subset of the principal independently sampled settings."""
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
from sweep import N, SEED, RANGES, gz_v5 as model, rates, spend

ROOT = Path(__file__).resolve().parent

def joint(data, outcome, k):
    z, t, w = data['zk'], data['tal'], data['logw']
    local = data['hukou']
    lo, hi = np.quantile(w[local], [.4,.6])
    top = z >= np.quantile(z,.8)
    def partition(x):
        return np.searchsorted(np.quantile(x[top],np.arange(1,k)/k),x)
    cell = k*partition(z)+partition(t)
    def counts(group):
        mask=top & local & group
        return np.bincount(cell[mask],minlength=k*k),np.bincount(cell[mask & outcome],minlength=k*k)
    nr,ar=counts(w>=hi);np_,ap=counts(w<=lo)
    keep=(nr>=5)&(np_>=5);weight=(nr+np_)[keep]
    return dict(ratio=float(np.sum(weight*ar[keep]/nr[keep])/np.sum(weight*ap[keep]/np_[keep])),
                support=float(weight.sum()/(nr+np_).sum()))

def metrics(data):
    out=data['uni'];w=data['logw'];local=data['hukou'];lo,hi=np.quantile(w[local],[.4,.6])
    result=dict(T=float(rates(data,out,'tal')),S=float(rates(data,out,'zk')),
                U=float(out[local&(w>=hi)].mean()/out[local&(w<=lo)].mean()),
                spend=float(spend(data)),learn=float(data['skill18'][data['acad']].mean()),
                learn_all=float(data['skill18'].mean()))
    for k in [5,10,20]:
        result['joint'+str(k)]=joint(data,out,k)
    ordinary=data['acad']&(data['gk']>=np.sort(data['gk'][data['acad']])[-(N//10)])
    result['ordinary']=dict(T=float(rates(data,ordinary,'tal')),S=float(rates(data,ordinary,'zk')),
                            Sstar=joint(data,ordinary,5)['ratio'])
    return result

def one(i):
    design,cohort=np.random.SeedSequence([SEED,i]).spawn(2)
    rng=np.random.default_rng(design);p={key:rng.uniform(*b) for key,b in RANGES.items()}
    p['HS_TEACH_SD']=p['TEACH_SD'];seed=int(cohort.generate_state(1)[0])
    result=dict(draw=i,seed=seed)
    scenarios=dict(current={},no_post=dict(TERM_SHARE=0,HOL_SHARE=0,FT_SHARE=0,ART_SHARE=0,HK_SHARE=0),
                   no_home=dict(HOME=0),no_zone=dict(TEACH_ZONE=0),no_pre=dict(PRE_EFF=0),
                   no_head=dict(HOME=0,TEACH_ZONE=0,PRE_EFF=0),
                   no_reband=dict(REBAND=False),no_ban=dict(BAN_RED=0),
                   before=dict(BAN_RED=0,REBAND=False))
    for name,changes in scenarios.items():
        result[name]=metrics(model.run(n=N,seed=seed,**{**p,**changes}))
    return result

if __name__=='__main__':
    with ProcessPoolExecutor(4) as pool,(ROOT/'mechanisms.jsonl').open('w') as out:
        for result in pool.map(one,range(150),chunksize=3):
            out.write(json.dumps(result)+'\n')
