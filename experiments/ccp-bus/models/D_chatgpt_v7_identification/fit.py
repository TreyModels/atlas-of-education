"""Simulated minimum-distance fitting. This module never opens holdout files."""
from common import *
from concurrent.futures import ProcessPoolExecutor,as_completed
from collections import Counter
import argparse,time,platform

def run_candidate(job):
    family,index,theta,seeds=job;series=[]
    for seed in seeds:
        rows,_=simulate(theta,family,seed)
        series.append([r['cases_filed_civilian'] for r in rows if 2013<=r['year']<=2019])
    simulated=np.asarray(series).mean(axis=0)
    target=pd.read_csv(P/'data/train_cases.csv').value.to_numpy()
    result=dict(family=family,candidate=index,theta=theta,seeds=seeds,simulated_training_cases=simulated.tolist(),**profile(target,simulated))
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--draws',type=int,default=64);ap.add_argument('--workers',type=int,default=6);a=ap.parse_args()
    out=P/'results';out.mkdir(exist_ok=True)
    design=dict(candidates=candidates(a.draws),bounds=BOUNDS,training_years=list(range(2013,2020)),
        calibration_agents=12500,screening_seeds=[1101,1102],refinement_seeds=list(range(2101,2109)),source_hashes=source_hashes(),
        train_hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (P/'data').glob('train_*.csv')},
        estimator='Profiled log-count simulated minimum distance; no posterior claim',environment=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__))
    design['hash']=digest(design)
    manifest=out/'fit_design.json'
    if manifest.exists() and json.loads(manifest.read_text())['hash']!=design['hash']:raise SystemExit('Design changed; choose a fresh results directory')
    if not manifest.exists():atomic(manifest,design)
    raw=out/'fit_candidates';raw.mkdir(exist_ok=True);jobs=[];results=[]
    for family in FAMILIES:
        for i,theta in enumerate(design['candidates']):
            path=raw/f'{family}_{i}.json'
            if path.exists():
                r=json.loads(path.read_text());assert r['design_hash']==design['hash'];results.append(r)
            else:jobs.append((family,i,theta,design['screening_seeds']))
    started=time.time();print(f'{len(jobs)} candidate evaluations remaining; two simulations per evaluation',flush=True)
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futures={pool.submit(run_candidate,j):j for j in jobs}
        for done,future in enumerate(as_completed(futures),1):
            r=future.result();r['design_hash']=design['hash'];atomic(raw/f'{r["family"]}_{r["candidate"]}.json',r);results.append(r)
            if done%24==0 or done==len(jobs):print(f'Screened {done}/{len(jobs)}, {time.time()-started:.1f}s',flush=True)
    # Further candidate ranking uses only training data with a larger independent seed set.
    selected=[];refine=[]
    for family in FAMILIES:
        best=sorted([r for r in results if r['family']==family],key=lambda x:x['log_rmse'])[:4]
        refine += [(family,r['candidate'],r['theta'],design['refinement_seeds']) for r in best]
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for r in pool.map(run_candidate,refine):selected.append(r)
    selected.sort(key=lambda r:(r['family'],r['log_rmse']))
    atomic(out/'frozen_fits.json',dict(design_hash=design['hash'],source_hashes=design['source_hashes'],selected=selected,
        selection_information='2013–2019 filed cases and training land only',fit_elapsed_seconds=time.time()-started))
    pd.DataFrame([dict(family=r['family'],candidate=r['candidate'],log_rmse=r['log_rmse'],scale=r['scale'],**r['theta']) for r in selected]).to_csv(out/'fitted_parameters.csv',index=False)
    print(json.dumps(dict(fitted_candidates=len(results),refined_candidates=len(selected),elapsed_seconds=time.time()-started,best_training={f:min(r['log_rmse'] for r in selected if r['family']==f) for f in FAMILIES}),indent=2),flush=True)
if __name__=='__main__':main()
