"""Second-stage, training-only local search; preserves the first-stage map.

21 candidates per country: 4 first-pass leaders, the incumbent, 8 local
perturbations around each of the first-pass winner and incumbent. Six seeds.
The incumbent's inclusion does not restore blind status to historical outcomes.
"""
from pathlib import Path
import json, os
from multiprocessing import Pool
import numpy as np
from history_match import SPACE, COUNTRIES, job, rank_runs
ROOT=Path(__file__).resolve().parent.parent
SEEDS=(0,1,2,3,4,5)


def candidates(first,original):
    # Identical normalized perturbations for every country; preserve original ranges.
    z=np.random.default_rng(3202).uniform(-.10,.10,(8,len(SPACE)))
    points=[r['prm'] for r in first['runs'][:4]]+[original['runs'][0]['prm']]
    for centre in (first['runs'][0]['prm'],original['runs'][0]['prm']):
        for offsets in z:
            points.append({k:float(np.clip(centre[k]+d*(hi-lo),lo,hi))
                           for (k,(lo,hi)),d in zip(SPACE.items(),offsets)})
    return points


def main():
    first=json.loads((ROOT/'results/first_pass_v0.3.2/context_map.json').read_text())
    old=json.loads((ROOT/'results/archive_v0.3.1/context_map.json').read_text())
    tasks=[(c,p,SEEDS) for c in COUNTRIES for p in candidates(first[c],old[c])]
    with Pool(min(8,os.cpu_count() or 1)) as pool:
        results=[]
        for i,r in enumerate(pool.imap(job,tasks),1):
            results.append(r)
            if i%7==0: print(f'{i}/{len(tasks)} refined candidates evaluated on six seeds',flush=True)
    J={}
    L=['CONTEXT MAP (21 samples per country in local refinement after 256 global samples; training <=2015 only; six seeds 0-5)',
       'Selection: same indicator-balanced Huber objective and per-seed acceptance as stage one.',
       'Candidate inclusion and ranking do not use post-2015 errors. Retrospective results are not newly blind.', '']
    for c in COUNTRIES:
        kept,use=rank_runs([r for r in results if r['country']==c])
        J[c]=dict(kept=len(kept),samples=21,global_samples=256,train_until=2015,
                  training_seeds=list(SEEDS),design_seed=3202,
                  selection='training-only Huber loss; six-seed local refinement; incumbent included',runs=use)
        L.append(f'=== {c}: {len(kept)}/21 refined candidates not ruled out on every training seed')
        for k in SPACE:
            v=[r['prm'][k] for r in use]
            L.append(f'    {k:13s} {min(v):.4f} - {max(v):.4f}')
        r=use[0]
        L.append(f'    selected loss {r["train_loss"]:.4f}; worst-seed second-max {r["second_max"]:.3f}')
        for ind,y,v,m,w,split in r['rows']:
            L.append(f'    {ind:24s} {y} observed {v:.3f} model {m:.3f} {"ok" if w else "TICKET"} ({split})')
        L.append('')
    dest=ROOT/'engine/results'
    (dest/'context_map.json').write_text(json.dumps(J,default=float,allow_nan=False))
    (dest/'context_map.txt').write_text('\n'.join(L)+'\n')
    (ROOT/'results/refinement_candidates.json').write_text(json.dumps(results,default=float,allow_nan=False))
    print('\n'.join(L))

if __name__=='__main__': main()
