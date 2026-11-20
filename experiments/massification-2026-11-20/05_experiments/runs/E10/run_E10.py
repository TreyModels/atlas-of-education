"""E10: learning vs test performance (Yang-style omega split), via the EXTENSION tut_hc_equiv.
Productive share omega of the tutoring effect is credited as schooling-year equivalents."""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import run_many, write_rows, write_text, m_sd
from mass_outcomes import outcomes
from massabm import make_params

OMEGAS = [0.0, 0.5, 1.0]
TUT_EFFECT = 0.25
COLLEGE = {'full cost': None, 'half cost from 1995': [(1994, 1.0), (1995, 0.5), (2035, 0.5)]}
KEYS = ['basic_completion', 'college_q1', 'college_q35', 'degree_share', 'licensed', 'tutoring_per_child_q35',
        'tut_rate_basic', 'tut_rate_board', 'tut_spend_total', 'college_income', 'basic_income', 'premium']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=2)
    ap.add_argument('--N', type=int, default=5000)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    jobs = []
    for om in OMEGAS:
        for cn, tp in COLLEGE.items():
            for r in range(a.reps):
                ov = dict(tut_hc_equiv=om * TUT_EFFECT)
                if tp is not None:
                    ov['tuition_path'] = tp
                jobs.append(((om, cn, r), 'massabm', make_params(seed=23000 + r, N=a.N, **ov)))
    print(f'E10: {len(jobs)} runs reps={a.reps} N={a.N}', flush=True)
    res, elapsed = run_many(jobs, a.workers)
    wall = time.time() - t0
    bad = [t for t, o in res.items() if isinstance(o, dict) and 'error' in o]
    rows = []
    for (om, cn, r), o in res.items():
        if isinstance(o, dict) and 'error' in o:
            continue
        d = outcomes(o); d.update(omega=om, cost=cn, rep=r); rows.append(d)
    write_rows(os.path.join(a.out, 'e10_raw.csv'), list(rows[0].keys()), [[r.get(k) for k in rows[0]] for r in rows])
    summ = []
    for om in OMEGAS:
        for cn in COLLEGE:
            R = [r for r in rows if r['omega'] == om and r['cost'] == cn]
            if not R:
                summ.append(dict(omega=om, cost=cn, n_ok=0)); continue
            row = dict(omega=om, cost=cn, n_ok=len(R))
            for k in KEYS:
                row[k], row[k + '_sd'] = m_sd([r[k] for r in R])
            summ.append(row)
    hdr = ['omega', 'cost', 'n_ok'] + [x for k in KEYS for x in (k, k + '_sd')]
    write_rows(os.path.join(a.out, 'e10_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])
    L = ['E10 LEARNING vs TEST PERFORMANCE (Yang-style omega)',
         f'reps={a.reps} N={a.N} wall={wall:.0f}s ok={len(rows)}/{len(jobs)} failed={len(bad)}',
         f'omega = productive share of the tutoring effect, credited as tut_hc_equiv = omega*{TUT_EFFECT} schooling-year',
         'equivalents per tutored gate-year. omega=0 = the stock massabm (test-only boost). EXTENSION module.', '',
         f'  {"omega":>5s} {"college":>20s} {"pass basic":>11s} {"colQ3-5":>8s} {"degree":>7s} {"college inc":>11s} {"basic inc":>10s} {"tut spend":>10s}']
    for r in summ:
        if not r.get('n_ok'):
            L.append(f'  {r["omega"]:5.1f} {r["cost"]:20s} FAILED'); continue
        L.append(f'  {r["omega"]:5.1f} {r["cost"]:20s} {r["basic_completion"]:11.3f} {r["college_q35"]:8.3f} '
                 f'{r["degree_share"]:7.3f} {r["college_income"]:11.3f} {r["basic_income"]:10.3f} {r["tut_spend_total"]:10.0f}')
    def G(om, cn, k):
        for r in summ:
            if r['omega'] == om and r['cost'] == cn:
                return r.get(k), r.get(k + '_sd', np.nan)
        return np.nan, np.nan
    L += ['', 'SEPARABILITY TEST at full college cost (omega 0 -> 1):']
    for k in ['basic_completion', 'college_q35', 'tut_spend_total', 'college_income', 'basic_income']:
        v0, s0 = G(0.0, 'full cost', k); v1, s1 = G(1.0, 'full cost', k)
        L.append(f'  {k:20s} {v0:.4f} -> {v1:.4f}  Δ={v1 - v0:+.4f} (2*sd≈{2 * np.hypot(s0, s1):.4f})')
    p0, ps0 = G(0.0, 'full cost', 'basic_completion'); p1, ps1 = G(1.0, 'full cost', 'basic_completion')
    flat = abs(p1 - p0) < 2 * np.hypot(ps0, ps1)
    L += ['', f'Predeclared: supports separability if PASS RATES stay flat while later income responds. '
              f'Pass rates {"flat" if flat else "MOVE"} -> '
              f'{"SUPPORTS" if flat else "NOT IDENTIFIED (mechanical pass-rate movement)"}']
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='E10', reps=a.reps, N=a.N, wall=wall, runs=len(jobs), ok=len(rows), failed=bad,
                   mean_run=float(np.mean(list(elapsed.values())))), open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'wall={wall:.0f}s ok={len(rows)}/{len(jobs)}')


if __name__ == '__main__':
    main()
