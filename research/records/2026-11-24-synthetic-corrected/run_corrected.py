#!/usr/bin/env python3
"""Exploratory synthetic matrix; never interprets simulations as real-world findings."""
import os
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):
    os.environ[key]='1'
os.environ.setdefault('REDESIGN_BACKEND','numpy')
import argparse, hashlib, itertools, json, math, multiprocessing as mp, pathlib, time
import numpy as np
import model

WORLDS=('P','S','C','R','null')
LINKS=('cl','sw','wo','hw','tut','learn','inc')
SPECS=('S1','S2','S3','S4','S5','S6')
TYPES=[(.45,.18,-.10,.95,.10,.25,.12,.75),(.65,.25,.10,1.05,.20,.35,.20,.85),(.35,.15,-.20,.90,.05,.20,.08,.70),(.75,.30,.20,1.10,.30,.45,.30,.95)]
RANGES=dict(sigma_y=(.25,.95),sigma_a=(.08,.45),mu_y=(-.4,.5),mu_a=(.7,1.5),w_child=(.02,.5),shadow_cost=(.1,.7),f_pub_pre=(0.,.45),y_sub0=(.55,1.25))
# Two-sided 90% t quantiles, df 1..30; conservative step-down thereafter.
T90=[6.314,2.920,2.353,2.132,2.015,1.943,1.895,1.860,1.833,1.812,1.796,1.782,1.771,1.761,1.753,1.746,1.740,1.734,1.729,1.725,1.721,1.717,1.714,1.711,1.708,1.706,1.703,1.701,1.699,1.697]
T95=[12.706,4.303,3.182,2.776,2.571,2.447,2.365,2.306,2.262,2.228,2.201,2.179,2.160,2.145,2.131,2.120,2.110,2.101,2.093,2.086,2.080,2.074,2.069,2.064,2.060,2.056,2.052,2.048,2.045,2.042]
def t95(df):
    if df<1: return None
    if df<=30:return T95[df-1]
    if df<40:return T95[-1]
    if df<60:return 2.021
    if df<120:return 2.000
    return 1.980

def t90(df):
    if df<1: return None
    if df<=30:return T90[df-1]
    if df<40:return T90[-1]
    if df<60:return 1.684
    if df<120:return 1.671
    return 1.658

def seed(*parts):
    return int.from_bytes(hashlib.sha256('|'.join(map(str,parts)).encode()).digest()[:4],'big')

def generate(task):
    block,c,world,n=task
    group=c%4
    g=np.random.Generator(np.random.Philox(seed('country',block,c)))
    p={k:float(np.clip(v+g.normal(0,.05),*RANGES[k])) for k,v in zip(RANGES,TYPES[group])}
    # country attributes shared between worlds for paired contrasts; household draws independent.
    res=model.run_unit(None if world=='null' else world,0 if world=='null' else 1,
                       seed('households',block,c,world),n=n,years=25,backend='numpy',**p)
    s=res['state']
    z={'ger':(s<=1).mean(1),'cl':np.isin(s,(1,2)).mean(1),'sw':(s==1).mean(1),
       'wo':(s==2).mean(1),'hw':(s==3).mean(1),'tut':res['tutor'].mean(1),
       'learn':res['learn'].mean(1),'inc':res['y_hh'].mean(1)}
    return block,c,world,group,z

def fit(series,spec,link,dose,block,group):
    if spec == 'S4' and link == 'inc':
        return {'error':'income outcome cannot be adjusted for itself'}
    rows=[]
    for (c,w),item in series.items():
        if group!='all' and item['group']!=int(group):continue
        z=item['values']; y=np.array(z[link],float); x=np.array(z['ger'],float)
        if dose:
            rng=np.random.Generator(np.random.Philox(seed('error',block,c,w,link,spec)))
            y=y*np.exp(rng.normal(0,dose,len(y))); x=x*np.exp(rng.normal(0,dose,len(x)))
        income=np.array(z['inc'],float)
        lag={'S1':10,'S2':5,'S3':0,'S4':10,'S5':5,'S6':1}[spec]
        for t in range(lag,25):
            a=y[t]-y[t-lag] if lag else y[t]; b=x[t]-x[t-lag] if lag else x[t]
            v=income[t]-income[t-lag] if lag else income[t]
            rows.append((c,t,a,b,v,item['group']))
    if not rows:return {'error':'no observations'}
    a=np.asarray(rows); countries=np.unique(a[:,0]); times=np.unique(a[:,1]); groups=np.unique(a[:,5]);
    # Omit one category from each dummy family; S3 includes country and year effects.
    X=[np.ones(len(a)),a[:,3]]
    if spec=='S3':
        X.extend((a[:,0]==i).astype(float) for i in countries[1:])
        X.extend((a[:,1]==i).astype(float) for i in times[1:])
    elif spec in ('S1','S4'):
        bins=(a[:,1]//10).astype(int); X.extend((bins==i).astype(float) for i in np.unique(bins)[1:])
    elif spec in ('S2','S5'):
        bins=(a[:,1]//5).astype(int); X.extend((bins==i).astype(float) for i in np.unique(bins)[1:])
    if spec=='S4':X.append(a[:,4])
    if spec=='S5':X.extend((a[:,5]==i).astype(float) for i in groups[1:])
    X=np.column_stack(X); y=a[:,2]; n,k=X.shape; G=len(countries)
    if G<2 or n<=k or np.linalg.matrix_rank(X)<k:
        return {'error':'insufficient independent clusters or rank deficient','clusters':G,'n':n,'rank':int(np.linalg.matrix_rank(X)),'columns':k}
    beta=np.linalg.lstsq(X,y,rcond=None)[0]; resid=y-X@beta
    bread=np.linalg.pinv(X.T@X); meat=np.zeros((k,k))
    for c in countries:
        v=X[a[:,0]==c].T@resid[a[:,0]==c];meat+=np.outer(v,v)
    cov=bread@meat@bread*(G/(G-1))*((n-1)/(n-k))
    se=float(np.sqrt(max(cov[1,1],0)))
    return {'slope':float(beta[1]),'cluster_se':se,'clusters':G,'n':n,'ci90':[float(beta[1]-t90(G-1)*se),float(beta[1]+t90(G-1)*se)],'ci95':[float(beta[1]-t95(G-1)*se),float(beta[1]+t95(G-1)*se)]}

def summarize(estimates,margin):
    valid=[x for x in estimates if x is not None and np.isfinite(x)]
    n=len(valid)
    if n<2:return {'blocks':n,'error':'fewer than two estimable blocks'}
    avg=float(np.mean(valid)); se=float(np.std(valid,ddof=1)/np.sqrt(n)); q=t90(n-1)
    ci=[avg-q*se,avg+q*se]
    return {'blocks':n,'mean_difference':avg,'se_across_independent_blocks':se,'ci90':ci,
            'margin_provisional':margin,'tost_equivalent_exploratory':bool(ci[0]>-margin and ci[1]<margin)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--smoke',action='store_true');ap.add_argument('--workers',type=int,default=4)
    ap.add_argument('--output',required=True);args=ap.parse_args(); started=time.time()
    n,ct,blocks=(300,8,2) if args.smoke else (10000,64,10)
    if args.workers<1:raise ValueError('workers must be >= 1')
    tasks=[(b,c,w,n) for b in range(blocks) for c in range(ct) for w in WORLDS]
    with mp.Pool(args.workers) as pool: generated=pool.map(generate,tasks,chunksize=1)
    data={}
    for b,c,w,g,z in generated:data.setdefault((b,w),{})[(c,w)]={'group':g,'values':z}
    fits=[]; indices={}
    for b,w,group,spec,dose,link in itertools.product(range(blocks),WORLDS,('all','0','1','2','3'),SPECS,(0.,.05),LINKS):
        v=fit(data[b,w],spec,link,dose,b,group)
        item={'block':b,'world':w,'group':group,'spec':spec,'dose':dose,'outcome':link,'predictor':'ger',**v};fits.append(item)
        indices[b,w,group,spec,dose,link]=v.get('slope')
    comparisons=[]
    for a,b,group,spec,dose,link in itertools.product(WORLDS,WORLDS,('all','0','1','2','3'),SPECS,(0.,.05),LINKS):
        if WORLDS.index(a)>=WORLDS.index(b):continue
        vals=[]
        for block in range(blocks):
            x=indices[block,a,group,spec,dose,link];y=indices[block,b,group,spec,dose,link]
            vals.append(None if x is None or y is None else x-y)
        comparisons.append({'world_a':a,'world_b':b,'group':group,'spec':spec,'dose':dose,'outcome':link,**summarize(vals,.05)})
    output={'label':'SIMULATION — EXPLORATORY, not empirical or confirmatory','smoke':args.smoke,'config':{'households':n,'countries_per_block':ct,'blocks':blocks,'worlds':WORLDS,'workers':args.workers,'types':'four fixed synthetic nuisance-parameter archetypes; subgroup c % 4','links':'outcome ~ GER, raw units','seed_scheme':'SHA-256 namespaces, first 32 bits','margin':'0.05 slope units, provisional and unvalidated'},'fits':fits,'comparisons':comparisons,'elapsed_s':time.time()-started}
    path=pathlib.Path(args.output)
    with path.open('x') as f:json.dump(output,f,indent=2,allow_nan=False)
    print(json.dumps({'output':str(path),'fits':len(fits),'estimable':sum('slope' in f for f in fits),'comparisons':len(comparisons),'elapsed_s':round(time.time()-started,2)}))
if __name__=='__main__':main()
