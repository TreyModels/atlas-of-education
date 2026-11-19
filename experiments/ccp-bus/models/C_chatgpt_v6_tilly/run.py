"""Reproducible experiment runner. Existing jobs are reusable only under the same design hash."""
import os
for _key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[_key]='1'
from pathlib import Path
from dataclasses import asdict,replace
from concurrent.futures import ProcessPoolExecutor,as_completed
import argparse,hashlib,json,platform,sys,time
import numpy as np
import pandas as pd
from model import Params,SCENARIOS,RANGES,draw_params,World
P=Path(__file__).resolve().parent

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def atomic(path,value):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n');temp.replace(path)
def provenance():
    files=[P/k for k in ('model.py','tilly.py','observation.py','evidence.py','run.py')]+sorted((P/'data').glob('*'))
    return {str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file()}
def design(n=50000,draws=12,seeds=3,trajectories=4):
    jobs=[]
    def add(family,point,p,scenario,seed,burn=30,**metadata):
        job=dict(family=family,point=str(point),params=asdict(p),scenario=scenario,seed=int(seed),burn=burn,start=1998,end=2042,**metadata)
        job['id']=digest(job)[:20];jobs.append(job)
    points=draw_params(n,draws)
    for i,p in enumerate(points):
        for seed in range(seeds):
            for sc in SCENARIOS:add('lhs',i,p,sc,1000+seed)
    for seed in range(8):
        for sc in SCENARIOS:add('reference','default',Params(n=n),sc,1000+seed)
    rng=np.random.default_rng(20261119);keys=list(RANGES);delta=.6
    for tr in range(trajectories):
        direction=rng.choice([-1,1],len(keys));base=rng.integers(0,3,len(keys))/5
        x=np.where(direction>0,base,base+delta);order=rng.permutation(len(keys))
        for step in range(len(keys)+1):
            changed=None;dx=0.
            if step:
                j=order[step-1];dx=float(delta*direction[j]);x[j]+=dx;changed=keys[j]
            pp=Params(n=n,**{k:float(RANGES[k][0]+x[j]*(RANGES[k][1]-RANGES[k][0])) for j,k in enumerate(keys)})
            for seed in range(2):add('morris',f'{tr}:{step}',pp,'campaign',2000+seed,trajectory=tr,step=step,changed=changed,dx=dx)
    for integrity in [1.2,3.2]:
        for seed in range(4):
            for sc in ['campaign','access_reform','strong_oversight']:
                add('integrity',integrity,replace(Params(n=n),cohort_integrity=integrity),sc,1000+seed)
    for size in [10000,100000]:
        for point in range(2):
            for seed in range(2):
                for sc in ['campaign','access_reform','no_replacement']:
                    add('scale',f'{size}:{point}',replace(points[point],n=size),sc,1000+seed,matched_point=point)
    for burn in [10,60]:
        for initial in [.05,.75]:
            for seed in range(2):add('initialization',f'{burn}:{initial}',replace(Params(n=n),initial_corruption=initial),'campaign',3000+seed,burn=burn)
    return jobs
def execute(job,design_hash,out):
    started=time.time();p=Params(**job['params'])
    w=World(p,job['seed'])
    for _ in range(job['burn']):w.step(job['scenario'],1998)
    rows=[w.step(job['scenario'],year) for year in range(job['start'],job['end']+1)]
    result=dict(design_hash=design_hash,job=job,elapsed_seconds=time.time()-started,rows=rows,cohort_records=list(w.cohort.values()))
    atomic(Path(out)/(job['id']+'.json'),result)
    return job['id']
def reusable(path,job,design_hash):
    if not path.exists():return False
    try:r=json.loads(path.read_text())
    except (ValueError,OSError):return False
    return r.get('design_hash')==design_hash and r.get('job')==job and len(r.get('rows',[]))==job['end']-job['start']+1 and 'cohort_records' in r
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--agents',type=int,default=50000);ap.add_argument('--draws',type=int,default=12)
    ap.add_argument('--seeds',type=int,default=3);ap.add_argument('--trajectories',type=int,default=4);ap.add_argument('--workers',type=int,default=6)
    ap.add_argument('--output',type=Path,default=P/'results');ap.add_argument('--design-only',action='store_true');a=ap.parse_args()
    if a.draws<2 or a.seeds<2:ap.error('Use at least two parameter draws and two seeds')
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);raw=out/'runs';raw.mkdir(exist_ok=True)
    jobs=design(a.agents,a.draws,a.seeds,a.trajectories)
    spec=dict(provenance=provenance(),jobs=jobs,environment_key=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__));dh=digest(spec);mp=out/'manifest.json'
    if mp.exists() and json.loads(mp.read_text())['design_hash']!=dh:
        raise SystemExit('Different code, data or design detected. Choose a new --output directory.')
    manifest=dict(design_hash=dh,**spec,environment=dict(python=sys.version,numpy=np.__version__,pandas=pd.__version__,platform=platform.platform()),
                  interpretation='Synthetic explanatory experiments; coefficients uncalibrated; calendar years are scenario labels.')
    if not mp.exists():atomic(mp,manifest)
    if a.design_only:print(f'Design saved: {len(jobs)} jobs, {dh}',flush=True);return
    pending=[j for j in jobs if not reusable(raw/(j['id']+'.json'),j,dh)]
    started=time.time();print(f'{len(jobs)} jobs; {len(jobs)-len(pending)} reusable; {len(pending)} remaining; {a.workers} workers',flush=True)
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futures={pool.submit(execute,j,dh,str(raw)):j for j in pending}
        for done,future in enumerate(as_completed(futures),1):
            future.result()
            if done%24==0 or done==len(pending):print(f'{done}/{len(pending)} completed, {time.time()-started:.1f}s',flush=True)
    atomic(out/'completion.json',dict(design_hash=dh,expected=len(jobs),completed=sum(reusable(raw/(j['id']+'.json'),j,dh) for j in jobs),elapsed_seconds=time.time()-started))
if __name__=='__main__':main()
