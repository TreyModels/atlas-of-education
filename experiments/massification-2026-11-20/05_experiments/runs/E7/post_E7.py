"""E7 findings + summary from the already-written raw CSV (no rerun)."""
import csv, os, sys, json
import numpy as np
sys.path.insert(0, '/tmp/massrun/work/exp')
from common import write_rows, write_text, m_sd

out = sys.argv[1]
rows = list(csv.DictReader(open(os.path.join(out, 'e7_raw.csv'))))
for r in rows:
    for k, v in list(r.items()):
        if k == 'arm':
            r[k] = v
        elif k == 'level':
            try: r[k] = float(v)
            except ValueError: r[k] = v
        else:
            try: r[k] = float(v)
            except: r[k] = np.nan
BARS = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5]
BANS = ['none', 'apex', 'board', 'all_formal']
KEYS = ['basic_completion', 'college_q1', 'college_q35', 'tut_rate_basic', 'tut_rate_apex',
        'tut_rate_college', 'tut_rate_board', 'tut_spend_total', 'tut_spend_basic', 'tut_spend_apex',
        'tut_spend_college', 'tut_spend_board', 'tut_spend_share_apex', 'tut_spend_share_board',
        'tutoring_per_child_q35', 'tut_rate_basic_q1', 'tut_rate_basic_q5', 'liquidity_exit_all']
summ = []
for arm, levels in [('bar', BARS), ('ban', BANS)]:
    for lv in levels:
        R = [r for r in rows if r['arm'] == arm and r['level'] == lv]
        if not R:
            summ.append(dict(arm=arm, level=lv, n_ok=0)); continue
        row = dict(arm=arm, level=lv, n_ok=len(R))
        for k in KEYS:
            row[k], row[k + '_sd'] = m_sd([r[k] for r in R])
        summ.append(row)
hdr = ['arm', 'level', 'n_ok'] + [x for k in KEYS for x in (k, k + '_sd')]
write_rows(os.path.join(out, 'e7_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])

def G(arm, lv, k):
    for r in summ:
        if r['arm'] == arm and r['level'] == lv:
            return r.get(k), r.get(k + '_sd', np.nan)
    return np.nan, np.nan
L = ['E7 GATE DENSITY AND TUTORING CLUSTERING',
     'reps=3 N=5000; seeds 3000+r; window 2000-2012 for gate rates, cohorts 1995-2012.', '',
     'Baseline gate tutoring rates (share of gate-takers who tutor) and spend shares:',
     '  ' + '  '.join(f'{g}={G("ban","none","tut_rate_"+g)[0]:.3f}' for g in ['basic', 'apex', 'college', 'board']),
     '  spend by gate: ' + '  '.join(f'{g}={G("ban","none","tut_spend_"+g)[0]:.0f}' for g in ['basic', 'apex', 'college', 'board']),
     '  apex share of total spend=' + f'{G("ban","none","tut_spend_share_apex")[0]:.3f}'
     + '  board share=' + f'{G("ban","none","tut_spend_share_board")[0]:.3f}', '',
     'Bar sweep on the BASIC completion gate:', '  ' + f'{"bar":>6s} {"tut_basic":>10s} {"completion":>11s} {"college_Q1":>11s} {"liquidity exit":>14s}']
for b in BARS:
    tr, sd = G('bar', b, 'tut_rate_basic'); bc, _ = G('bar', b, 'basic_completion'); c1, _ = G('bar', b, 'college_q1')
    le, _ = G('bar', b, 'liquidity_exit_all')
    L.append(f'  {b:+6.1f} {tr:10.3f}(±{sd:.3f}) {bc:11.3f} {c1:11.3f} {le:14.4f}')
L += ['', 'Tutoring ban arms (does spend disappear or reroute?):']
for nm in BANS:
    tot, _ = G('ban', nm, 'tut_spend_total')
    L.append(f'  ban={nm:11s} total={tot:6.0f}  by gate: ' +
             ' '.join(f'{g}={G("ban",nm,"tut_spend_"+g)[0]:.0f}' for g in ['basic', 'apex', 'college', 'board']) +
             f'  completion={G("ban",nm,"basic_completion")[0]:.3f}  college_Q1={G("ban",nm,"college_q1")[0]:.3f}')
lo, _ = G('bar', BARS[0], 'tut_rate_basic'); hi, _ = G('bar', BARS[-1], 'tut_rate_basic')
sdl, _ = G('bar', BARS[0], 'tut_rate_basic_sd'); sdh, _ = G('bar', BARS[-1], 'tut_rate_basic_sd')
L += ['', f'Predeclared threshold: bar sweep must raise basic-gate tutoring by > 2 seed sd. '
          f'Observed Δ={hi - lo:+.3f} vs 2*sd≈{2 * np.hypot(sdl, sdh):.3f} -> '
          f'{"SUPPORTS" if (hi - lo) > 2 * np.hypot(sdl, sdh) else "DOES NOT CLEAR THRESHOLD"}',
      '', 'Read: tutoring share should be highest where the payoff is discontinuous (board/apex) and should',
      'move to the basic gate as that gate is pushed toward the median student. The ban arms show whether',
      'closing a gate deletes demand (spend->0) or reroutes it (spend persists at other gates / informal leak).']
write_text(os.path.join(out, 'findings.txt'), '\n'.join(L) + '\n')
print('E7 findings regenerated from raw')
