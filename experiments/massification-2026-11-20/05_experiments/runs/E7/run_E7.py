"""E7: gate density and tutoring clustering. Predeclared in PRE_DECLARATIONS.md."""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import run_many, write_rows, write_text, m_sd
from mass_outcomes import outcomes
from massabm import make_params

BARS = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5]
BANS = {'none': [], 'apex': ['apex'], 'board': ['board'], 'all_formal': ['apex', 'board']}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=3)
    ap.add_argument('--N', type=int, default=5000)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    jobs = [(('bar', b, r), 'massabm', make_params(seed=3000 + r, N=a.N, bar_basic=b))
            for b in BARS for r in range(a.reps)]
    jobs += [(('ban', nm, r), 'massabm', make_params(seed=3000 + r, N=a.N, tut_ban=tb))
             for nm, tb in BANS.items() for r in range(a.reps)]
    print(f'E7: {len(jobs)} runs reps={a.reps} N={a.N}', flush=True)
    res, elapsed = run_many(jobs, a.workers)
    wall = time.time() - t0
    bad = [t for t, o in res.items() if isinstance(o, dict) and 'error' in o]
    rows = []
    for tag, o in res.items():
        if isinstance(o, dict) and 'error' in o:
            rows.append(dict(arm=tag[0], level=tag[1], rep=tag[2], error=o['error']))
            continue
        d = outcomes(o); d.update(arm=tag[0], level=tag[1], rep=tag[2])
        rows.append(d)
    ok = [r for r in rows if 'error' not in r]
    write_rows(os.path.join(a.out, 'e7_raw.csv'), list(ok[0].keys()),
               [[r.get(k) for k in ok[0]] for r in ok])
    summ = []
    for arm, levels in [('bar', BARS), ('ban', list(BANS))]:
        for lv in levels:
            R = [r for r in ok if r['arm'] == arm and r['level'] == lv]
            if not R:
                summ.append(dict(arm=arm, level=lv, n_ok=0)); continue
            row = dict(arm=arm, level=lv, n_ok=len(R))
            for k in ['basic_completion', 'college_q1', 'college_q35', 'tut_rate_basic', 'tut_rate_apex',
                      'tut_rate_college', 'tut_rate_board', 'tut_spend_total', 'tut_spend_share_apex',
                      'tut_spend_share_board', 'tutoring_per_child_q35', 'tut_rate_basic_q1',
                      'tut_rate_basic_q5', 'liquidity_exit_all']:
                row[k], row[k + '_sd'] = m_sd([r[k] for r in R])
            summ.append(row)
    hdr = ['arm', 'level', 'n_ok', 'basic_completion', 'basic_completion_sd', 'college_q1', 'college_q35',
           'tut_rate_basic', 'tut_rate_apex', 'tut_rate_college', 'tut_rate_board',
           'tut_spend_total', 'tut_spend_share_apex', 'tut_spend_share_board',
           'tutoring_per_child_q35', 'tut_rate_basic_q1', 'tut_rate_basic_q5', 'liquidity_exit_all']
    write_rows(os.path.join(a.out, 'e7_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])

    def S_(arm, lv, k):
        for r in summ:
            if r['arm'] == arm and r['level'] == lv:
                return r.get(k), r.get(k + '_sd', np.nan)
        return np.nan, np.nan
    L = ['E7 GATE DENSITY AND TUTORING CLUSTERING', f'reps={a.reps} N={a.N} wall={wall:.0f}s ok={len(ok)}/{len(jobs)} failed={len(bad)}', '',
         'Baseline gate tutoring rates and spend shares (2000-2012):',
         '  ' + '  '.join(f'{g}={S_("ban","none","tut_rate_"+g)[0]:.3f}' for g in ['basic', 'apex', 'college', 'board']),
         '  spend shares: ' + '  '.join(f'{g}={S_("ban","none","tut_spend_share_"+g)[0]:.3f}' for g in ['apex', 'board']),
         '', 'Bar sweep on the basic completion gate (tutoring share at that gate, completion, college Q1):']
    for b in BARS:
        tr, sd = S_('bar', b, 'tut_rate_basic'); bc, _ = S_('bar', b, 'basic_completion'); c1, _ = S_('bar', b, 'college_q1')
        L.append(f'  bar={b:+.1f}  tut_basic={tr:.3f}(±{sd:.3f})  completion={bc:.3f}  college_Q1={c1:.3f}')
    L += ['', 'Tutoring ban arms (spend reroutes or disappears):']
    for nm in BANS:
        tot, _ = S_('ban', nm, 'tut_spend_total')
        L.append(f'  ban={nm:11s} total spend={tot:.0f}  by gate: ' +
                 ' '.join(f'{g}={S_("ban", nm, "tut_spend_"+g)[0]:.0f}' for g in ['basic', 'apex', 'college', 'board']) +
                 f'  completion={S_("ban",nm,"basic_completion")[0]:.3f}  college_Q1={S_("ban",nm,"college_q1")[0]:.3f}')
    lo, _ = S_('bar', BARS[0], 'tut_rate_basic'); hi, _ = S_('bar', BARS[-1], 'tut_rate_basic')
    sdl, _ = S_('bar', BARS[0], 'tut_rate_basic_sd'); sdh, _ = S_('bar', BARS[-1], 'tut_rate_basic_sd')
    L += ['', f'Predeclared threshold: bar sweep must raise basic-gate tutoring by >2 seed sd. '
              f'Observed Δ={hi - lo:+.3f} vs 2*sd≈{2 * np.hypot(sdl, sdh):.3f} -> '
              f'{"SUPPORTS" if (hi - lo) > 2 * np.hypot(sdl, sdh) else "DOES NOT CLEAR THRESHOLD"}']
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='E7', reps=a.reps, N=a.N, wall=wall, runs=len(jobs), ok=len(ok), failed=bad,
                   mean_run=float(np.mean(list(elapsed.values()))), max_run=float(np.max(list(elapsed.values())))),
              open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'wall={wall:.0f}s ok={len(ok)}/{len(jobs)}')


if __name__ == '__main__':
    main()
