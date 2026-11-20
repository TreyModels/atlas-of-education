"""E13b (Council priority): matched-elasticity rival for the graduate-supply shock.

Both worlds now have a formal/informal margin, the same households, the same graduate-supply
shock and the SAME formal vacancy path:
  - surplus world      : mode='full' (credential floors + ranked hiring)
  - matched rival      : mode='hc_fair_slots' (CES skill prices, sigma in {0.5,1,2}; hiring by
                         expected productivity; no credential floor, no rank-by-credential)
Estimands (paired vs 'no shock', matched seeds): change in diploma holders' ABSOLUTE income and
change in diploma holders' FORMAL-EMPLOYMENT PROBABILITY.
Decision rule (predeclared from Council guidance): C3's claim is CONTRADICTED if at any sigma the
rival reproduces a fall in diploma holders' absolute income (delta <= 0); CONDITIONALLY SUPPORTED
if the fall appears only in the surplus world across the whole sigma range.
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import run_many, write_rows, write_text, m_sd
from massabm import make_params
from massabm.experiments8 import BASE, SHOCKS, _outcomes

SIGMAS = [0.5, 1.0, 2.0]
WORLDS = {'surplus (slots+floors+rank)': dict(mode='full'),
          'competitive CES + slots (matched rival)': dict(mode='hc_fair_slots')}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=6)
    ap.add_argument('--N', type=int, default=5000)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    jobs = []
    for w, wo in WORLDS.items():
        for sg in (SIGMAS if 'matched' in w else [None]):
            for sh, tp in SHOCKS.items():
                for r in range(a.reps):
                    ov = dict(wo)
                    if sg is not None:
                        ov['fair_sigma'] = sg
                    jobs.append(((w, sg, sh, r), 'massabm',
                                 make_params(seed=20000 + r, N=a.N, tuition_path=tp,
                                             macro_elasticity=0.0, **BASE, **ov)))
    print(f'E13b: {len(jobs)} runs reps={a.reps} N={a.N}', flush=True)
    res, elapsed = run_many(jobs, a.workers)
    wall = time.time() - t0
    bad = [t for t, o in res.items() if isinstance(o, dict) and 'error' in o]
    rows = []
    for (w, sg, sh, r), o in res.items():
        if isinstance(o, dict) and 'error' in o:
            continue
        B = res.get((w, sg, 'no shock', r))
        if B is None or (isinstance(B, dict) and 'error' in B):
            continue
        Aa, Bb = _outcomes(o), _outcomes(B)
        rows.append(dict(world=w, sigma=sg if sg is not None else np.nan, shock=sh, rep=r,
                         diploma_income=Aa['basic_income'],
                         d_diploma_income=Aa['basic_income'] - Bb['basic_income'],
                         formal_rate_diploma=Aa['formal_rate_diploma'],
                         d_formal_rate_diploma=Aa['formal_rate_diploma'] - Bb['formal_rate_diploma'],
                         degree_income=Aa['degree_income'], d_degree_income=Aa['degree_income'] - Bb['degree_income'],
                         ratio=Aa['basic_income'] / Aa['degree_income'],
                         d_ratio=Aa['basic_income'] / Aa['degree_income'] - Bb['basic_income'] / Bb['degree_income'],
                         degree_share=Aa['degree_share'], d_degree_share=Aa['degree_share'] - Bb['degree_share']))
    write_rows(os.path.join(a.out, 'e13b_raw.csv'), list(rows[0].keys()), [[r.get(k) for k in rows[0]] for r in rows])
    summ = []
    for w in WORLDS:
        for sg in (SIGMAS if 'matched' in w else [None]):
            for sh in SHOCKS:
                R = [r for r in rows if r['world'] == w and ((r['sigma'] == sg) or (sg is None and np.isnan(r['sigma'])))
                     and r['shock'] == sh]
                if not R:
                    summ.append(dict(world=w, sigma=sg, shock=sh, n_ok=0)); continue
                row = dict(world=w, sigma=sg, shock=sh, n_ok=len(R))
                for k in ['diploma_income', 'd_diploma_income', 'formal_rate_diploma', 'd_formal_rate_diploma',
                          'degree_income', 'd_degree_income', 'ratio', 'd_ratio']:
                    row[k], row[k + '_sd'] = m_sd([r[k] for r in R])
                summ.append(row)
    KEYS = ['diploma_income', 'd_diploma_income', 'formal_rate_diploma', 'd_formal_rate_diploma',
            'degree_income', 'd_degree_income', 'ratio', 'd_ratio']
    hdr = ['world', 'sigma', 'shock', 'n_ok'] + [x for k in KEYS for x in (k, k + '_sd')]
    write_rows(os.path.join(a.out, 'e13b_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])
    L = ['E13b MATCHED-ELASTICITY RIVAL FOR THE GRADUATE-SUPPLY SHOCK (Council priority)',
         f'reps={a.reps} N={a.N} wall={wall:.0f}s ok={len(rows)}/{len(jobs)} failed={len(bad)}',
         'Same households, same 1995 tuition shock, SAME formal vacancy path. Surplus world hires by',
         'credential floor + rank; rival uses CES skill prices with sigma in {0.5,1,2} and hires by',
         'expected productivity (no credential floor). Both have a formal/informal margin.', '',
         f'  {"world":38s} {"sigma":>5s} {"shock":30s} {"d dip inc":>15s} {"d formal|dip":>16s} {"d ratio":>9s}']
    for r in summ:
        if not r.get('n_ok'):
            L.append(f'  {r["world"]:38s} FAILED'); continue
        if r['shock'] == 'no shock':
            continue
        sgv = r["sigma"] if r["sigma"] is not None else 0.0
        L.append(f'  {r["world"]:38s} {sgv:5.1f} {r["shock"]:30s} '
                 f'{r["d_diploma_income"]:+11.4f}({r["d_diploma_income_sd"]:.3f}) '
                 f'{r["d_formal_rate_diploma"]:+12.4f}({r["d_formal_rate_diploma_sd"]:.3f}) {r["d_ratio"]:+9.4f}')
    # predeclared decision rule
    violations = [r for r in summ if 'matched' in r['world'] and r.get('n_ok') and r['shock'] != 'no shock'
                  and np.isfinite(r['d_diploma_income']) and r['d_diploma_income'] <= 0]
    L += ['', 'PREDECLARED DECISION RULE (Council): rival contradicts C3 if at ANY sigma the rival reproduces a',
          "fall in diploma holders' absolute income (delta <= 0)."]
    if violations:
        for r in violations:
            L.append(f'  VIOLATION at sigma={r["sigma"]}: Δdip income={r["d_diploma_income"]:+.4f} '
                     f'(±{r["d_diploma_income_sd"]:.4f}), Δformal|dip={r["d_formal_rate_diploma"]:+.4f}')
        L.append('  -> C3 (the competitive world cannot reproduce diploma-holder losses) is CONTRADICTED.')
    else:
        L.append('  no sigma reproduces a diploma-holder income fall in the matched rival ->')
        L.append('  -> C3 is CONDITIONALLY SUPPORTED (the fall appears only in the surplus account).')
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='E13b', reps=a.reps, N=a.N, wall=wall, runs=len(jobs), ok=len(rows), failed=bad,
                   mean_run=float(np.mean(list(elapsed.values()))), sigmas=SIGMAS,
                   decision='contradicted if rival d_diploma_income<=0 at any sigma'),
              open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'wall={wall:.0f}s ok={len(rows)}/{len(jobs)}')


if __name__ == '__main__':
    main()
