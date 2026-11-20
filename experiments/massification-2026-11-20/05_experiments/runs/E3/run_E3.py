"""E3: household liquidity, credit and shocks. Predeclared in PRE_DECLARATIONS.md."""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import run_many, write_rows, write_text, m_sd
from mass_outcomes import outcomes
from massabm import make_params

NO_CCT = [(1900, 0.0), (2100, 0.0)]
ARMS = {
    '1 baseline (borrow 0.5, shock sd 0.5)': dict(),
    '2 hard cash cutoff (borrow 0)': dict(borrow=0.0),
    '3 expanded credit (borrow 1.0)': dict(borrow=1.0),
    '4 temporary shock (shock sd 0.9)': dict(shock_sigma=0.9),
    '5 shock + no credit': dict(shock_sigma=0.9, borrow=0.0),
    '6 free basic schooling + CCT': dict(cost_pri=0.0, cost_jhs=0.0, cost_shs=0.0),
}
KEYS = ['basic_completion', 'basic_q1', 'basic_q5', 'basic_gap_q5_q1', 'college_q1', 'college_q35',
        'liquidity_exit_all', 'liquidity_exit_q1', 'choice_exit_prebasic_q1', 'degree_share',
        'tutoring_per_child_q1', 'tutoring_per_child_q35', 'basic_income', 'college_income']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=3)
    ap.add_argument('--N', type=int, default=5000)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    jobs = [((arm, r), 'massabm', make_params(seed=21000 + r, N=a.N, **ov))
            for arm, ov in ARMS.items() for r in range(a.reps)]
    print(f'E3: {len(jobs)} runs reps={a.reps} N={a.N}', flush=True)
    res, elapsed = run_many(jobs, a.workers)
    wall = time.time() - t0
    bad = [t for t, o in res.items() if isinstance(o, dict) and 'error' in o]
    rows = []
    for (arm, r), o in res.items():
        if isinstance(o, dict) and 'error' in o:
            continue
        d = outcomes(o); d.update(arm=arm, rep=r); rows.append(d)
    write_rows(os.path.join(a.out, 'e3_raw.csv'), list(rows[0].keys()), [[r.get(k) for k in rows[0]] for r in rows])
    summ = []
    for arm in ARMS:
        R = [r for r in rows if r['arm'] == arm]
        if not R:
            summ.append(dict(arm=arm, n_ok=0)); continue
        row = dict(arm=arm, n_ok=len(R))
        for k in KEYS:
            row[k], row[k + '_sd'] = m_sd([r[k] for r in R])
        summ.append(row)
    hdr = ['arm', 'n_ok'] + [x for k in KEYS for x in (k, k + '_sd')]
    write_rows(os.path.join(a.out, 'e3_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])
    L = ['E3 HOUSEHOLD LIQUIDITY, CREDIT AND SHOCKS',
         f'reps={a.reps} N={a.N} wall={wall:.0f}s ok={len(rows)}/{len(jobs)} failed={len(bad)}',
         'All arms share matched cohorts and seed list 21000+r; no K-12 reform change; window cohorts 1995-2012.', '',
         f'  {"arm":38s} {"basic":>7s} {"basicQ1":>8s} {"Q5-Q1":>7s} {"colQ3-5":>8s} {"liq exit":>9s} {"liqQ1":>7s} {"choiceQ1":>9s}']
    for r in summ:
        if not r.get('n_ok'):
            L.append(f'  {r["arm"]:38s} FAILED TO EXECUTE'); continue
        L.append(f'  {r["arm"]:38s} {r["basic_completion"]:7.3f} {r["basic_q1"]:8.3f} {r["basic_gap_q5_q1"]:7.3f} '
                 f'{r["college_q35"]:8.3f} {r["liquidity_exit_all"]:9.4f} {r["liquidity_exit_q1"]:7.4f} '
                 f'{r["choice_exit_prebasic_q1"]:9.4f}')
    def G(arm, k):
        for r in summ:
            if r['arm'] == arm:
                return r.get(k), r.get(k + '_sd', np.nan)
        return np.nan, np.nan
    L += ['', 'PREDECLARED CONTRASTS (matched seeds, 2 seed sd in parentheses):']
    for lbl, arm, k in [('hard cutoff vs baseline: Q1 liquidity exits', '2 hard cash cutoff (borrow 0)', 'liquidity_exit_q1'),
                        ('hard cutoff vs baseline: Q5-Q1 completion gap', '2 hard cash cutoff (borrow 0)', 'basic_gap_q5_q1'),
                        ('expanded credit vs baseline: Q5-Q1 gap', '3 expanded credit (borrow 1.0)', 'basic_gap_q5_q1'),
                        ('shock vs baseline: Q1 completion', '4 temporary shock (shock sd 0.9)', 'basic_q1'),
                        ('shock+no credit vs shock: Q1 completion', '5 shock + no credit', 'basic_q1'),
                        ('free+CCT vs baseline: Q1 completion', '6 free basic schooling + CCT', 'basic_q1')]:
        va, sa = G(arm, k); vb, sb = G('1 baseline (borrow 0.5, shock sd 0.5)', k)
        L.append(f'  {lbl:52s} Δ={va - vb:+.4f} (2*sd≈{2 * np.hypot(sa, sb):.4f}) -> '
                 f'{"clears threshold" if abs(va - vb) > 2 * np.hypot(sa, sb) else "within seed noise"}')
    L += ['', 'Caveat: massabm borrow is a quantity (share of income), not a price; no interest rate is modelled.']
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='E3', reps=a.reps, N=a.N, wall=wall, runs=len(jobs), ok=len(rows), failed=bad,
                   mean_run=float(np.mean(list(elapsed.values())))), open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'wall={wall:.0f}s ok={len(rows)}/{len(jobs)}')


if __name__ == '__main__':
    main()
