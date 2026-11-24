#!/usr/bin/env python3
"""Stipulated event-order sensitivity using the existing modular education engine."""
import argparse, hashlib, itertools, json, multiprocessing as mp, os, pathlib, sys, time
os.environ['OPENBLAS_NUM_THREADS']='1'; os.environ['OMP_NUM_THREADS']='1'; os.environ['MKL_NUM_THREADS']='1'
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import worlds

GATES_BAR=[dict(kind='bar',bar=x) for x in (3.0,5.5,8.0,11.5)]
GATES_QUOTA=[dict(kind='bar',bar=3.0),dict(kind='quota',share=.55,cut0=7.0),dict(kind='quota',share=.45,cut0=10.0),dict(kind='bar',bar=11.5)]
SCHEDULES={'none':(None,None),'school_first':(15,30),'jobs_first':(30,15),'simultaneous':(15,15)}
SCALARS=['completion_primary','completion_lower','completion_upper','completion_tertiary','tut_rate','mpl_primary','q_pub','formal_share_gdp','edu_gdp','parity_location_lower','parity_wealth_lower','parity_location_upper','parity_wealth_upper']
ARRAYS=['tut_by_grade','tut_by_q','completion_lower_q','completion_upper_q','completion_tertiary_q']
SERIES=['year','formal_share_gdp','edu_budget','q_pub','tut_rate']

def clean(v):
    if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(list,tuple,np.ndarray)):return [clean(x) for x in v]
    if isinstance(v,(int,np.integer)):return int(v)
    if isinstance(v,(float,np.floating)):return float(v) if np.isfinite(v) else None
    if isinstance(v,(str,bool)) or v is None:return v
    return str(v)

def one(args):
    schedule,feedback,gates,seed,N=args
    school,jobs=SCHEDULES[schedule];ev=[]
    if school is not None:ev.append({'year':school,'set':{'edu_share':.30},'label':'education_share'})
    if jobs is not None:ev.append({'year':jobs,'set':{'vac0':.16},'label':'formal_vacancies'})
    engine=worlds.make('formal_loop',seed=seed,N=N,T=70,measure_from=35,job_elasticity=feedback,
                       gates=GATES_QUOTA if gates=='quota' else GATES_BAR,events=ev)
    result=engine.run()
    return clean({'schedule':schedule,'feedback':feedback,'gates':gates,'seed':seed,
                  'events':engine.event_log,'metrics':{k:result.get(k) for k in SCALARS+ARRAYS},
                  'annual':{k:engine.R.get(k) for k in SERIES}})

def scalar_summary(vals):
    v=[x for x in vals if x is not None and np.isfinite(x)]
    return {'n':len(v),'mean':float(np.mean(v)) if v else None,'sd':float(np.std(v,ddof=1)) if len(v)>1 else None}

def summarize(rows,boot=2000):
    result={}
    for fb,g in itertools.product((0.,1.),('bar','quota')):
        subset=[r for r in rows if r['feedback']==fb and r['gates']==g]
        group={s:{k:scalar_summary([r['metrics'][k] for r in subset if r['schedule']==s]) for k in SCALARS} for s in SCHEDULES}
        contrasts={}
        for a,b in [('school_first','jobs_first'),('simultaneous','none')]:
            left={r['seed']:r for r in subset if r['schedule']==a};right={r['seed']:r for r in subset if r['schedule']==b}; diffs={}
            for k in SCALARS:
                v=np.array([left[s]['metrics'][k]-right[s]['metrics'][k] for s in sorted(left.keys()&right.keys()) if left[s]['metrics'][k] is not None and right[s]['metrics'][k] is not None],float)
                if len(v)<2:diffs[k]={'n':len(v),'mean':None,'seed_bootstrap_95':None};continue
                rng=np.random.default_rng(7321); bs=np.mean(rng.choice(v,size=(boot,len(v)),replace=True),axis=1)
                diffs[k]={'n':len(v),'mean':float(v.mean()),'seed_bootstrap_95':[float(x) for x in np.quantile(bs,[.025,.975])]}
            contrasts[a+'_minus_'+b]=diffs
        result[f'feedback_{fb:g}_gates_{g}']={'groups':group,'contrasts':contrasts}
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--smoke',action='store_true');p.add_argument('--workers',type=int,default=8);p.add_argument('--out',required=True)
    a=p.parse_args();out=pathlib.Path(a.out)
    if out.exists():raise FileExistsError(out)
    seeds=range(2 if a.smoke else 10);N=80 if a.smoke else 400
    tasks=list(itertools.product(SCHEDULES,(0.,1.),('bar','quota'),seeds,(N,)))
    start=time.time()
    with mp.Pool(a.workers) as pool:rows=pool.map(one,tasks,chunksize=1)
    data={'label':'SIMULATION ONLY — synthetic scenario, not empirical; no causal claims','config':{'cohort_N':N,'seeds':list(seeds),'years':70,'runs':len(rows),'education_event':'0.18 to 0.30 share of modeled tax revenue','job_event':'vac0 0.08 to 0.16 vacancies per entrant','feedback':[0,1],'schedules':SCHEDULES,'measurement':'cohorts 35–44','gate':['bar','quota'],'design_file':'DESIGN.md'},'rows':rows,'summary':summarize(rows),'elapsed_s':round(time.time()-start,3)}
    with out.open('x') as f:json.dump(data,f,indent=2,allow_nan=False)
    print(json.dumps({'runs':len(rows),'cohort_N':N,'elapsed_s':data['elapsed_s'],'output':str(out)}))
if __name__=='__main__':main()
