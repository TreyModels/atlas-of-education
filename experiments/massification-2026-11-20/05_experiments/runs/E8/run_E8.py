"""E8: the race and the floor -- 6-arm reproduction.

Question : Does a categorical credential floor (a rule that says "this job needs this
           credential") explain anything that a ranked labour queue does not?
Estimand : arm-level means of (a) basic-diploma completion, all and poorest fifth;
           (b) formal-employment rate of workers below the diploma vs diploma holders;
           (c) college entry of Q3-Q5; (d) slope of Q3-Q5 college entry on degree
           holders' absolute income across formal-demand scales 0/1/2.
Arms     : ranking {on, off} x eligibility rule {none, adaptive employer floor,
           fixed rule-set floor}. Shared seeds (19000+r), shared schedules, no K-12
           reform. Fixed jobs and wage rules comparable across arms.
Reported : mean (sd across matched seeds) at baseline demand; slope (SE) across scales.
"""
import argparse, json, os, sys, time
import numpy as np

sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import run_many, write_rows, write_text, m_sd, slope

from massabm import make_params
from massabm.experiments8 import ARMS, BASE, _outcomes
from massabm.model import BASIC

SCALES = [0.0, 1.0, 2.0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=3)
    ap.add_argument('--N', type=int, default=6000)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', required=True)
    ap.add_argument('--tag', default='full')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    jobs = [((arm, s, r), 'massabm',
             make_params(seed=19000 + r, N=a.N, formal_growth_scale=s, **BASE, **ov))
            for arm, ov in ARMS.items() for s in SCALES for r in range(a.reps)]
    print(f'E8: {len(jobs)} runs, reps={a.reps} N={a.N} workers={a.workers}', flush=True)
    res, elapsed = run_many(jobs, a.workers)
    wall = time.time() - t0
    bad = [t for t, o in res.items() if isinstance(o, dict) and 'error' in o]
    rows, summ = [], []
    for arm in ARMS:
        per = []
        for s in SCALES:
            for r in range(a.reps):
                o = res.get((arm, s, r))
                if o is None or (isinstance(o, dict) and 'error' in o):
                    continue
                d = _outcomes(o)
                d.update(arm=arm, scale=s, rep=r)
                rows.append(d)
                if s == 1.0:
                    per.append(d)
        allr = [d for d in rows if d['arm'] == arm]
        if not per:
            summ.append(dict(arm=arm, n_ok=0))
            continue
        key = ['diploma_all', 'diploma_q1', 'formal_rate_below_diploma', 'formal_rate_diploma',
               'college_q35', 'tutoring_q35', 'degree_income', 'basic_income', 'degree_share']
        row = dict(arm=arm, n_ok=len(per))
        for k in key:
            row[k], row[k + '_sd'] = m_sd([d[k] for d in per])
        b, se = slope([d['degree_income'] for d in allr], [d['college_q35'] for d in allr])
        row['slope_college_on_degree_income'] = b
        row['slope_se'] = se
        summ.append(row)
    write_rows(os.path.join(a.out, 'e8_raw.csv'), list(rows[0].keys()) if rows else ['arm'],
               [[r.get(k) for k in rows[0]] for r in rows] if rows else [])
    hdr = ['arm', 'n_ok', 'diploma_all', 'diploma_all_sd', 'diploma_q1', 'diploma_q1_sd',
           'formal_rate_below_diploma', 'formal_rate_diploma', 'college_q35', 'college_q35_sd',
           'tutoring_q35', 'tutoring_q35_sd', 'degree_income', 'basic_income', 'degree_share',
           'slope_college_on_degree_income', 'slope_se']
    write_rows(os.path.join(a.out, 'e8_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])
    # pairwise floor contributions, holding ranking fixed
    def get(arm, k):
        for r in summ:
            if r['arm'] == arm:
                return r[k], r.get(k + '_sd', np.nan)
        return None, None
    L = ['E8 THE RACE AND THE FLOOR -- 6 arms x formal-demand scale x matched seeds',
         f'reps={a.reps} N={a.N} workers={a.workers} no K-12 reform; cohorts entering 1995-2012, labour 2010-30.',
         f'wall={wall:.0f}s, runs_ok={len(rows)}/{len(jobs)}, failed={len(bad)}', '',
         f'  {"arm":44s} {"diploma":>13s} {"diploma Q1":>13s} {"formal|<dip":>11s} {"formal|dip":>10s} {"colQ3-5":>13s} {"slope":>8s}']
    for r in summ:
        if not r.get('n_ok'):
            L.append(f'  {r["arm"]:44s} FAILED TO EXECUTE'); continue
        L.append(f'  {r["arm"]:44s} {r["diploma_all"]:6.3f}({r["diploma_all_sd"]:.3f}) '
                 f'{r["diploma_q1"]:6.3f}({r["diploma_q1_sd"]:.3f}) {r["formal_rate_below_diploma"]:11.3f} '
                 f'{r["formal_rate_diploma"]:10.3f} {r["college_q35"]:6.3f}({r["college_q35_sd"]:.3f}) '
                 f'{r["slope_college_on_degree_income"]:+8.3f}')
    L += ['', 'FLOOR EFFECTS holding ranking fixed (fixed/adaptive floor minus no floor):']
    for pre in ['ranked', 'unranked']:
        for nm in ['adaptive employer floor (baseline)', 'fixed rule-set floor']:
            a_arm = [k for k in ARMS if k.startswith(pre) and nm in k]
            b_arm = [k for k in ARMS if k.startswith(pre) and 'no floor' in k]
            if not a_arm or not b_arm:
                continue
            for k in ['diploma_all', 'diploma_q1', 'formal_rate_below_diploma', 'college_q35']:
                va, sa = get(a_arm[0], k); vb, sb = get(b_arm[0], k)
                L.append(f'  {pre:9s} {nm:32s} {k:26s} {va - vb:+.4f} (seed sd {np.hypot(sa, sb):.4f})')
    L += ['', 'Read: an eligibility-rule floor should move exclusion (formal|<dip) and persistence;',
          'the intensity of investment (slope < 0 = invest more as degrees pay less) should need',
          'the RANK race, not the floor. A floor arm that shows both is not identified separately.',
          f'elapsed_wall_seconds={wall:.1f} per_run_seconds={np.mean(list(elapsed.values())):.2f} max={np.max(list(elapsed.values())):.2f}']
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    meta = dict(eid='E8', reps=a.reps, N=a.N, workers=a.workers, scales=SCALES, arms=list(ARMS),
                wall_seconds=wall, runs=len(jobs), runs_ok=len(rows), failed=bad,
                mean_run_seconds=float(np.mean(list(elapsed.values()))),
                max_run_seconds=float(np.max(list(elapsed.values()))))
    json.dump(meta, open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'wall={wall:.0f}s runs_ok={len(rows)}/{len(jobs)} failed={len(bad)}', flush=True)


if __name__ == '__main__':
    main()
