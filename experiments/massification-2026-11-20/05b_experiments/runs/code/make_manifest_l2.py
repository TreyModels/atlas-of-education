"""Build loop2/SUMMARY_L2.csv and RUN_MANIFEST_L2.json from the loop-2 run artefacts."""
import csv
import hashlib
import json
import os
import platform
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
L2 = os.path.abspath(os.path.join(HERE, '..'))
B = os.path.abspath(os.path.join(L2, '..'))


def sha(p):
    h = hashlib.sha256(); h.update(open(p, 'rb').read()); return h.hexdigest()[:16]


def read_csv(p):
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []


def f(x):
    try:
        v = float(x); return f'{v:.6f}' if np.isfinite(v) else 'nan'
    except Exception:
        return str(x)


def main():
    cps = read_csv(os.path.join(L2, 'runs', 'L2', 'l2_checkpoints.csv'))
    keys = ['completion', 'college_entry', 'degree_share', 'formal_share', 'complex_share',
            'take_S', 'take_C', 'price', 'n_cm', 'n_tt', 'R_C', 'H']
    rows = []
    for c in cps:
        for k in keys:
            rows.append(dict(cell_id='L2', experiment='Loop 2 two-way education-economy + shadow sector',
                             country=c['country'], regime=c['regime'], year=c['year'],
                             estimand=k, estimate=f(c.get(k)), seed_sd=f(c.get(k + '_sd')),
                             n_ok=c['n'], source='runs/L2/l2_checkpoints.csv'))
    hdr = ['cell_id', 'experiment', 'country', 'regime', 'year', 'estimand', 'estimate', 'seed_sd', 'n_ok', 'source']
    with open(os.path.join(L2, 'SUMMARY_L2.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=hdr); w.writeheader()
        for r in rows:
            w.writerow(r)

    meta = json.load(open(os.path.join(L2, 'runs', 'L2', 'run_meta.json')))
    manifest = dict(loop='2', owner='experiment-runner-2', scope='05b_experiments/loop2 only',
                    module='code/twoway.py (NEW; not massabm/floorworld/triad/paper reproduction)',
                    environment=dict(python=sys.version.split()[0], platform=platform.platform(),
                                     numpy=np.__version__, executable=sys.executable,
                                     policy='numpy-only, no multiprocessing; PYTHONDONTWRITEBYTECODE=1'),
                    predeclaration='PRE_DECLARATIONS_L2.md',
                    data_targets=dict(
                        gmr_observed='../04_data/data/gmr_observed_6countries_1970_2024.csv',
                        national_headlines='../04_data/data/national_headline_figures.csv',
                        rule='only observed cells used as targets; no imputed cell cited'),
                    code_sha={p: sha(os.path.join(L2, p)) for p in ['code/twoway.py', '../code/bcommon.py',
                                                                   'code/make_manifest_l2.py']
                              if os.path.exists(os.path.join(L2, p))},
                    meta=meta)
    outputs, logs = [], []
    for run_dir in ['runs/L2', 'runs/L2_uncalibrated']:
        for root, _, files in os.walk(os.path.join(L2, run_dir)):
            for fn in sorted(files):
                fp = os.path.join(root, fn)
                outputs.append(dict(path=os.path.relpath(fp, L2), sha16=sha(fp), bytes=os.path.getsize(fp)))
    for fn in sorted(os.listdir(os.path.join(L2, 'logs'))) if os.path.isdir(os.path.join(L2, 'logs')) else []:
        fp = os.path.join(L2, 'logs', fn)
        logs.append(dict(path=f'logs/{fn}', sha16=sha(fp), bytes=os.path.getsize(fp)))
    manifest['outputs'] = outputs
    manifest['logs'] = logs
    json.dump(manifest, open(os.path.join(L2, 'RUN_MANIFEST_L2.json'), 'w'), indent=1)
    print(f'wrote SUMMARY_L2.csv ({len(rows)} rows) and RUN_MANIFEST_L2.json ({len(outputs)} outputs)')


if __name__ == '__main__':
    main()
