"""E5: memory, learning and decision horizons. belief_decay = memory of observed outcomes."""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import run_many, write_rows, write_text, m_sd
from mass_outcomes import outcomes
from massabm import make_params

ARMS = {
    'M0 very short memory (decay 0.0)': dict(belief_decay=0.0),
    'M1 short memory (decay 0.5)': dict(belief_decay=0.5),
    'M2 baseline memory (decay 0.88, ~5yr)': dict(),
    'M3 long memory (decay 0.99)': dict(belief_decay=0.99),
    'M4 selection-corrected learning': dict(belief_mode='selection_corrected'),
}
KEYS = ['basic_completion', 'college_q35', 'college_q1', 'degree_share', 'tutoring_per_child_q35',
        'basic_income', 'college_income', 'premium', 'liquidity_exit_all']


def belief_speed(S):
    b = S['belief_ce']                       # T,5,NC
    d = np.abs(np.diff(b, axis=0))
    w = (S['year'][1:] >= 1980) & (S['year'][1:] <= 2030)
    return float(np.nanmean(d[w]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=3)
    ap.add_argument('--N', type=int, default=5000)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    jobs = [((arm, r), 'massabm', make_params(seed=22000 + r, N=a.N, **ov))
            for arm, ov in ARMS.items() for r in range(a.reps)]
    print(f'E5: {len(jobs)} runs reps={a.reps} N={a.N}', flush=True)
    res, elapsed = run_many(jobs, a.workers)
    wall = time.time() - t0
    bad = [t for t, o in res.items() if isinstance(o, dict) and 'error' in o]
    rows = []
    for (arm, r), o in res.items():
        if isinstance(o, dict) and 'error' in o:
            continue
        d = outcomes(o); d.update(arm=arm, rep=r, belief_speed=belief_speed(o)); rows.append(d)
    write_rows(os.path.join(a.out, 'e5_raw.csv'), list(rows[0].keys()), [[r.get(k) for k in rows[0]] for r in rows])
    summ = []
    for arm in ARMS:
        R = [r for r in rows if r['arm'] == arm]
        if not R:
            summ.append(dict(arm=arm, n_ok=0)); continue
        row = dict(arm=arm, n_ok=len(R))
        for k in KEYS + ['belief_speed']:
            row[k], row[k + '_sd'] = m_sd([r[k] for r in R])
        summ.append(row)
    hdr = ['arm', 'n_ok'] + [x for k in KEYS + ['belief_speed'] for x in (k, k + '_sd')]
    write_rows(os.path.join(a.out, 'e5_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])
    L = ['E5 MEMORY, LEARNING AND DECISION HORIZONS',
         f'reps={a.reps} N={a.N} wall={wall:.0f}s ok={len(rows)}/{len(jobs)} failed={len(bad)}',
         'belief_decay = weight kept each year on older observations; 0.88 ~ 5-year memory; 1.0 = infinite (reported as a limit,',
         'not a plausible parameter). belief_speed = mean |one-year change| in believed CE income 1980-2030.', '',
         f'  {"arm":42s} {"basic":>7s} {"colQ3-5":>8s} {"degree":>7s} {"tut/q35":>8s} {"belief speed":>13s}']
    for r in summ:
        if not r.get('n_ok'):
            L.append(f'  {r["arm"]:42s} FAILED TO EXECUTE'); continue
        L.append(f'  {r["arm"]:42s} {r["basic_completion"]:7.3f} {r["college_q35"]:8.3f} {r["degree_share"]:7.3f} '
                 f'{r["tutoring_per_child_q35"]:8.4f} {r["belief_speed"]:8.5f}(±{r["belief_speed_sd"]:.5f})')
    def G(arm, k):
        for r in summ:
            if r['arm'] == arm:
                return r.get(k), r.get(k + '_sd', np.nan)
        return np.nan, np.nan
    b, bs = G('M2 baseline memory (decay 0.88, ~5yr)', 'belief_speed')
    s, ss = G('M0 very short memory (decay 0.0)', 'belief_speed')
    l, ls = G('M3 long memory (decay 0.99)', 'belief_speed')
    L += ['', 'PREDECLARED THRESHOLD (monotone memory effect on response speed and investment):']
    L.append(f'  belief speed: decay0={s:.5f}  0.88={b:.5f}  0.99={l:.5f}  (2*sd between extremes ≈ {2 * np.hypot(ss, ls):.5f})')
    L.append(f'  monotone? {"YES" if s > b > l else "NO"} -> {"SUPPORTS a memory effect" if (s > b > l and abs(s - l) > 2 * np.hypot(ss, ls)) else "DOES NOT CLEAR THRESHOLD"}')
    c0, cs0 = G('M0 very short memory (decay 0.0)', 'college_q35'); c1, cs1 = G('M3 long memory (decay 0.99)', 'college_q35')
    L.append(f'  college Q3-5: decay0={c0:.3f} 0.99={c1:.3f} Δ={c1 - c0:+.4f} (2*sd≈{2 * np.hypot(cs0, cs1):.4f})')
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='E5', reps=a.reps, N=a.N, wall=wall, runs=len(jobs), ok=len(rows), failed=bad,
                   mean_run=float(np.mean(list(elapsed.values())))), open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'wall={wall:.0f}s ok={len(rows)}/{len(jobs)}')


if __name__ == '__main__':
    main()
