"""Locked evaluation of original and training-selected settings; never tunes."""
from pathlib import Path
import importlib, json, os, platform, sys
from multiprocessing import Pool
import numpy as np
import scipy
from eduengine import ledger as LG
from history_match import COUNTRIES, training_metrics
ROOT=Path(__file__).resolve().parent.parent
SEEDS=(7,19,43)


def job(task):
    country, version, seed, anchored, prm=task
    C=importlib.import_module('countries.'+country)
    E=C.make(seed=seed,anchored=anchored,anchor_until=2015,**prm); E.run()
    rows=LG.ledger(E,country)
    splits={}
    for split in ('train','test'):
        rr=[r for r in rows if r['split']==split]
        verified=[r for r in rr if r['status'] not in ('unverified','stylised')]
        splits[split]=dict(within=sum(r['within'] for r in rr),n=len(rr),
            verified_within=sum(r['within'] for r in verified),verified_n=len(verified),
            mae=float(np.mean([abs(r['gap']) for r in rr])),
            completion_mae=float(np.mean([abs(r['gap']) for r in rr if r['instrument']=='completion_cohort'])))
    return dict(country=country,version=version,seed=seed,anchored=anchored,
                training_loss=training_metrics(rows)['loss'],score=splits,rows=rows)


def main():
    previous=json.loads((ROOT/'results/archive_v0.3.1/context_map.json').read_text())
    current=json.loads((ROOT/'engine/results/context_map.json').read_text())
    tasks=[(c,name,seed,anchored,J[c]['runs'][0]['prm']) for c in COUNTRIES
           for name,J in [('original',previous),('tuned',current)]
           for anchored in (True,False) for seed in SEEDS]
    with Pool(min(8,os.cpu_count() or 1)) as pool: runs=pool.map(job,tasks)
    result=dict(seeds=SEEDS,protocol=json.loads((ROOT/'engine/tune_protocol.json').read_text()),runs=runs)
    (ROOT/'results/tuning_evaluation.json').write_text(json.dumps(result,indent=2,default=float,allow_nan=False))
    L=['# Education Atlas 0.3.2: tuning results','',
       'Parameters selected using observations through 2015 and seeds 0 through 5. Evaluation seeds: 7, 19, 43. Each setting used 1,000 children per entering cohort. Original and tuned parameters use the same corrected pupil-weighted measurement, unchanged observations and unchanged tolerances.', '',
       'Post-2015 outcomes have been inspected before this work. These are retrospective temporal checks conditional on coded historical paths and events. Completion in anchored training runs is partly imposed by S0. First-pass seed sensitivity motivated the recorded six-seed refinement. Post-2015 errors did not select candidates or parameters. The original incumbent was included in refinement despite its historical selection using all years; that provenance remains a limit. No data-source verification was performed.', '',
       '| Country | Mode | Parameters | Train, mean passing / rows | After 2015, mean passing / rows | After 2015 completion MAE, pp |',
       '|---|---|---|---:|---:|---:|']
    for c in COUNTRIES:
        for anchored in (True,False):
            for version in ('original','tuned'):
                rr=[r for r in runs if (r['country'],r['anchored'],r['version'])==(c,anchored,version)]
                mean=lambda split,k: float(np.mean([r['score'][split][k] for r in rr]))
                L.append(f'| {c} | {"2015 anchors" if anchored else "Mechanism only"} | {version} | {mean("train","within"):.1f} / {rr[0]["score"]["train"]["n"]} | {mean("test","within"):.1f} / {rr[0]["score"]["test"]["n"]} | {100*mean("test","completion_mae"):.1f} |')
    L+=['','## Selection and uncertainty','',
        'The first pass sampled 256 identical Latin-hypercube settings per country in the original nine-dimensional ranges, design seed 32, on seeds 0 and 1. The recorded refinement then evaluated 21 candidates per country on six seeds (0 through 5), including the incumbent, four global leaders and local perturbations (seed 3202). Acceptance requires the second-largest training gap to stay within 2.5 tolerances on every training seed. Ranking uses mean Huber loss with equal weight per indicator. Unverified and stylised observations remain visible but do not select settings. Missing predictions fail the score and receive infinite selection loss.','',
        'Survivor counts and training objective:','']
    for c in COUNTRIES:
        d=current[c]; best=d['runs'][0]
        L.append(f'- {c}: {d["kept"]}/{d["samples"]} refined candidates survive; selected training loss {best["train_loss"]:.4f}; training indicators: '+', '.join(best['training_indicators'])+'.')
    L+=['', '## Training objective on other simulation seeds', '', '| Country | Original Huber loss | Selected Huber loss |', '|---|---:|---:|']
    for c in COUNTRIES:
        values=[]
        for v in ('original','tuned'):
            rr=[r for r in runs if r['country']==c and r['version']==v and r['anchored']]
            values.append(float(np.mean([r['training_loss'] for r in rr])))
        L.append(f'| {c} | {values[0]:.4f} | {values[1]:.4f} |')
    L+=['', '## Selected parameters', '', '| Parameter | Cambodia, old to new | Philippines, old to new | China, old to new |', '|---|---:|---:|---:|']
    for key in current['cambodia']['runs'][0]['prm']:
        vals=[f"{previous[c]['runs'][0]['prm'][key]:.4f} to {current[c]['runs'][0]['prm'][key]:.4f}" for c in COUNTRIES]
        L.append('| '+key+' | '+' | '.join(vals)+' |')
    L+=['','Surviving ranges are finite sampled envelopes, with no posterior probability or confidence-level interpretation. Country differences are not identified by gaps between sampled extrema. China has no pre-2016 tutoring observation in this registry, so this search cannot establish its tutoring mechanism from training data.', '',
        'Policy comparisons use one selected parameter vector, a frozen completion wedge and three paired seeds. That seed spread omits structural and parameter uncertainty. Branch-dependent draws can diverge across policy arms even when seeds match. Policy levels continue to drift after anchoring ends.','',
        'The tutoring indicator now weights grades by enrolled pupils; closed grades carry zero weight. The historical-replay view uses completion anchors after 2015 and represents reconstruction. Temporal-test mode uses anchors through 2015. Later country paths and policy events remain coded in both modes.','',
        'Detailed per-observation and per-seed comparisons: `results/tuning_evaluation.json`. Original parameters: `results/archive_v0.3.1/`.']
    (ROOT/'results/TUNING_REPORT.md').write_text('\n'.join(L)+'\n')
    env=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform())
    (ROOT/'results/tuning_environment.json').write_text(json.dumps(env,indent=2))
    print('\n'.join(L))

if __name__=='__main__': main()
