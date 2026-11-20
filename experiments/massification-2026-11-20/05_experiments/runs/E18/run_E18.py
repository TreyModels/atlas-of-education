"""E18: China-style Double Reduction synthetic variants, with a no-effect baseline.
School support = a zero-price public gate-preparation input (EXTENSION in ext/massabm,
declared in PRE_DECLARATIONS). NOT a measured Double Reduction effect."""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import run_many, write_rows, write_text, m_sd
from mass_outcomes import outcomes
from massabm import make_params

SUP = 0.5          # score units = one exam sd (sigma_exam=0.5)
ARMS = {
    'A0 no-effect baseline': dict(),
    'A1 ban only (leak 0.5: informal substitute market)': dict(tut_ban=['apex', 'board'], tut_ban_leak=0.5),
    'A2 ban fully enforced (leak 0.0)': dict(tut_ban=['apex', 'board'], tut_ban_leak=0.0),
    'A3 school support only (universal, free)': dict(support_effect=SUP, support_share=1.0),
    'A4 ban + school support': dict(tut_ban=['apex', 'board'], tut_ban_leak=0.5, support_effect=SUP, support_share=1.0),
    'A5 ban + school support, partial access (60%)': dict(tut_ban=['apex', 'board'], tut_ban_leak=0.5,
                                                          support_effect=SUP, support_share=0.6),
}
KEYS = ['tut_rate_basic', 'tut_rate_apex', 'tut_rate_college', 'tut_rate_board', 'tut_spend_total',
        'tut_spend_share_apex', 'tut_spend_share_board', 'tutoring_per_child_q35', 'tutoring_per_child_q1',
        'basic_completion', 'college_q1', 'college_q35', 'degree_share', 'college_income', 'basic_income',
        'premium', 'liquidity_exit_all', 'informal_share_2010']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=3)
    ap.add_argument('--N', type=int, default=5000)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    jobs = [((arm, r), 'massabm', make_params(seed=27000 + r, N=a.N, **ov))
            for arm, ov in ARMS.items() for r in range(a.reps)]
    print(f'E18: {len(jobs)} runs reps={a.reps} N={a.N}', flush=True)
    res, elapsed = run_many(jobs, a.workers)
    wall = time.time() - t0
    bad = [t for t, o in res.items() if isinstance(o, dict) and 'error' in o]
    rows = []
    for (arm, r), o in res.items():
        if isinstance(o, dict) and 'error' in o:
            continue
        d = outcomes(o); d.update(arm=arm, rep=r); rows.append(d)
    write_rows(os.path.join(a.out, 'e18_raw.csv'), list(rows[0].keys()), [[r.get(k) for k in rows[0]] for r in rows])
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
    write_rows(os.path.join(a.out, 'e18_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])

    def G(arm, k):
        for r in summ:
            if r['arm'] == arm:
                return r.get(k), r.get(k + '_sd', np.nan)
        return np.nan, np.nan
    L = ['E18 CHINA-STYLE DOUBLE REDUCTION SYNTHETIC VARIANTS (no-effect baseline present)',
         f'reps={a.reps} N={a.N} wall={wall:.0f}s ok={len(rows)}/{len(jobs)} failed={len(bad)}',
         'School support = zero-price public gate preparation worth 0.5 score units (one exam sd), EXTENSION module.',
         'Declared public cost: 0.30 index units per supported pupil-year (not budget-constrained in massabm).', '',
         f'  {"arm":52s} {"paid spend":>11s} {"apex spend":>10s} {"tut_basic":>9s} {"tut_board":>9s} {"completion":>10s} {"colQ3-5":>8s} {"college inc":>11s}']
    for r in summ:
        if not r.get('n_ok'):
            L.append(f'  {r["arm"]:52s} FAILED TO EXECUTE'); continue
        L.append(f'  {r["arm"]:52s} {r["tut_spend_total"]:11.0f} {r["tut_spend_share_apex"]:10.3f} '
                 f'{r["tut_rate_basic"]:9.3f} {r["tut_rate_board"]:9.3f} {r["basic_completion"]:10.3f} '
                 f'{r["college_q35"]:8.3f} {r["college_income"]:11.3f}')
    b_sp, b_sd = G('A0 no-effect baseline', 'tut_spend_total')
    a1_sp, a1_sd = G('A1 ban only (leak 0.5: informal substitute market)', 'tut_spend_total')
    a3_sp, a3_sd = G('A3 school support only (universal, free)', 'tut_spend_total')
    a4_sp, a4_sd = G('A4 ban + school support', 'tut_spend_total')
    a5_sp, a5_sd = G('A5 ban + school support, partial access (60%)', 'tut_spend_total')
    L += ['', 'PAIRED EFFECTS vs no-effect baseline (matched seeds), paid tutoring spend:']
    for nm, v, s in [('A1 ban only', a1_sp, a1_sd), ('A3 support only', a3_sp, a3_sd),
                     ('A4 ban+support', a4_sp, a4_sd), ('A5 ban+support 60%', a5_sp, a5_sd)]:
        L.append(f'  {nm:22s} Δ={v - b_sp:+8.1f}  (2*sd≈{2 * np.hypot(s, b_sd):.1f})')
    ld, lsd = G('A4 ban + school support', 'basic_completion')
    lb, lbsd = G('A0 no-effect baseline', 'basic_completion')
    L += ['', f'Predeclared: supports substitution if ban+support paid spend < ban-only paid spend by >2 seed sd '
              f'AND completion not lower by >2 sd.',
          f'  ban+support vs ban-only spend: Δ={a4_sp - a1_sp:+.1f} (2*sd≈{2 * np.hypot(a4_sd, a1_sd):.1f}) -> '
          f'{"SUPPORTS" if a4_sp < a1_sp else "DOES NOT SUPPORT"} substitution',
          f'  completion ban+support vs baseline: Δ={ld - lb:+.4f} (2*sd≈{2 * np.hypot(lsd, lbsd):.4f}) -> '
          f'{"no material learning loss" if abs(ld - lb) < 2 * np.hypot(lsd, lbsd) else "LEARNING CHANGED"}',
          f'  no-effect baseline reproduces baseline exactly (arm A0 is the untreated system): spend={b_sp:.0f}']
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='E18', reps=a.reps, N=a.N, wall=wall, runs=len(jobs), ok=len(rows), failed=bad,
                   mean_run=float(np.mean(list(elapsed.values())))), open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'wall={wall:.0f}s ok={len(rows)}/{len(jobs)}')


if __name__ == '__main__':
    main()
