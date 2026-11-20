"""E18b: fair substitution test for the school-support / Double Reduction hypothesis (Council brief 002).
Declared in PRE_DECLARATIONS_E18b_E13c.md. tut_suppress = support damps tutoring's marginal effect."""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import run_many, write_rows, write_text, m_sd
from mass_outcomes import outcomes
from massabm import make_params

SUP = 0.5
BAN = dict(tut_ban=['apex', 'board'], tut_ban_leak=0.5)
ARMS = {
    'A0 untreated baseline': dict(),
    'C0 ban only': dict(**BAN),
    'C1 ban+support universal, suppress=1 (halves tutoring value at s=.5)': dict(**BAN, support_effect=SUP, support_share=1.0, tut_suppress=1.0),
    'C2 ban+support universal, suppress=2 (full displacement at s=.5)': dict(**BAN, support_effect=SUP, support_share=1.0, tut_suppress=2.0),
    'C3 ban+support targeted Q1-Q2 (40%), suppress=2': dict(**BAN, support_effect=SUP, support_share=0.40, support_target_q=[0, 1], tut_suppress=2.0),
    'C4 ban+support capacity-limited 25%, suppress=2': dict(**BAN, support_effect=SUP, support_share=0.25, tut_suppress=2.0),
}
KEYS = ['tut_spend_total', 'tut_spend_basic', 'tut_spend_apex', 'tut_spend_college', 'tut_spend_board',
        'tut_spend_share_apex', 'tut_rate_basic', 'tut_rate_apex', 'tut_rate_college', 'tut_rate_board',
        'basic_completion', 'college_q35', 'college_q1', 'degree_share', 'informal_share_2010']


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
    print(f'E18b: {len(jobs)} runs reps={a.reps} N={a.N}', flush=True)
    res, elapsed = run_many(jobs, a.workers)
    wall = time.time() - t0
    bad = [t for t, o in res.items() if isinstance(o, dict) and 'error' in o]
    rows = []
    for (arm, r), o in res.items():
        if isinstance(o, dict) and 'error' in o:
            continue
        d = outcomes(o); d.update(arm=arm, rep=r); rows.append(d)
    write_rows(os.path.join(a.out, 'e18b_raw.csv'), list(rows[0].keys()), [[r.get(k) for k in rows[0]] for r in rows])
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
    write_rows(os.path.join(a.out, 'e18b_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])

    def G(arm, k):
        for r in summ:
            if r['arm'] == arm:
                return r.get(k), r.get(k + '_sd', np.nan)
        return np.nan, np.nan
    L = ['E18b FAIR SUBSTITUTION TEST (Council brief 002, follow-up)',
         f'reps={a.reps} N={a.N} wall={wall:.0f}s ok={len(rows)}/{len(jobs)} failed={len(bad)}',
         'tut_suppress = support damps the marginal effect of paid tutoring: effect x clip(1 - ts*s,0,1), s=0.5 sd.',
         'ts=0 is the stock additive E18 behaviour; ts=1 halves tutoring value; ts=2 fully displaces it.',
         'Decision rule: if any C1-C4 arm has paid spend below ban-only (C0) by >2 seed sd, C10 is WITHDRAWN.', '',
         f'  {"arm":72s} {"paid spend":>11s} {"vs C0":>9s} {"vs A0":>9s} {"apex share":>10s} {"board":>7s} {"completion":>10s}']
    c0, c0sd = G('C0 ban only', 'tut_spend_total'); a0, a0sd = G('A0 untreated baseline', 'tut_spend_total')
    for r in summ:
        if not r.get('n_ok'):
            L.append(f'  {r["arm"]:72s} FAILED TO EXECUTE'); continue
        L.append(f'  {r["arm"]:72s} {r["tut_spend_total"]:11.0f} {r["tut_spend_total"] - c0:+9.1f} '
                 f'{r["tut_spend_total"] - a0:+9.1f} {r["tut_spend_share_apex"]:10.3f} {r["tut_rate_board"]:7.3f} '
                 f'{r["basic_completion"]:10.3f}')
    L += ['', 'PAIRED CONTRASTS vs ban-only C0 (matched seeds, 2 seed sd in brackets):']
    viol = []
    for arm in list(ARMS)[2:]:
        sp, sd = G(arm, 'tut_spend_total'); comp, compsd = G(arm, 'basic_completion')
        d = sp - c0; two = 2 * np.hypot(sd, c0sd)
        L.append(f'  {arm[:60]:60s} d_spend={d:+8.1f} (2sd≈{two:7.1f}) -> {"BELOW C0 by >2sd" if d < -two else "not below C0"}')
        if d < -two:
            viol.append((arm, d, two))
        L.append(f'    learning guard: completion {comp:.4f} vs C0 {G("C0 ban only","basic_completion")[0]:.4f} '
                 f'(2sd≈{2 * np.hypot(compsd, G("C0 ban only","basic_completion_sd")[1]):.4f})')
    L += ['', 'DECISION:']
    if viol:
        L.append('  C10 is WITHDRAWN: substitution is possible in at least one fair arm:')
        for arm, d, two in viol:
            L.append(f'    {arm}: {d:+.1f} (2sd {two:.1f})')
    else:
        L.append('  No C1-C4 arm puts paid spend below ban-only by >2 seed sd ->')
        L.append('  C10 remains unsupported and "the race absorbs the subsidy" is defensible as a model-class claim.')
    # the Council's correction must be visible
    a5 = None
    L += ['', 'Council correction recorded: in E18, arm A5 (ban + ADDITIVE support, 60% access) already had',
          'paid spend 3,855 vs 4,092 untreated (-236.5). E18b therefore also reports "vs A0" above, not only "vs C0".']
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='E18b', reps=a.reps, N=a.N, wall=wall, runs=len(jobs), ok=len(rows), failed=bad,
                   decision='withdraw C10 if any C1-C4 < C0 by >2 seed sd'),
              open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'wall={wall:.0f}s ok={len(rows)}/{len(jobs)}')


if __name__ == '__main__':
    main()
