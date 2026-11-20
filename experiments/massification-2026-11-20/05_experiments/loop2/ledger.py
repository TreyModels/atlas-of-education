"""loop2 longitudinal cohort ledger 1980-2040 with balancing flow accounting, per country.
Predeclared in 05_experiments/PRE_DECLARATIONS_loop2.md.

Balance checks:
  B1 stock identity: stock_t = stock_{t-1} + entrants_t - exits_t holds exactly; exits_t >= 0
  B2 cohort conservation: final exits by category + still enrolled = cohort entrants
  B3 no negative stock, no rate outside [0,1]
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, '/tmp/massrun/work/loop2')
sys.path.insert(0, '/tmp/massrun/work/exp')
from common import write_rows, write_text
from massabm import make_params, run_model
from massabm.model import PRI, JHS, BASIC
import configs as CFG

ISO = ['PHL', 'KHM', 'HKG', 'CHN']
HORIZON = [1980, 1990, 2000, 2010, 2020, 2030, 2040]


def best_params(iso):
    """Read the selected calibration point written by calibrate2 (brief-004 parameter set)."""
    z = None
    for fn in ('/tmp/massrun/work/loop2/out/run_meta.json', '/tmp/massrun/work/loop2/out/best_by_country.json'):
        try:
            d = json.load(open(fn))
            if iso in d.get('best', {}):
                z = d['best'][iso]['z']; break
            if iso in d:
                z = d[iso]['z']; break
        except Exception:
            continue
    if z is None:
        z = dict(cost_col=0.53, prov_capacity=0.3, teacher_capacity=0.15, prov_elasticity=1.0)
    return dict(cost_col=z['cost_col'], prov_capacity=z['prov_capacity'],
                teacher_capacity=z['teacher_capacity'], prov_elasticity=z['prov_elasticity'])


def ledger(S, iso, N):
    y = S['year'].astype(int)
    entrants = S['c_n'].sum((1, 2)).astype(float)
    stock = S['enrol'].sum(1).astype(float)
    exits = np.zeros_like(stock)
    prev = 0.0
    for i in range(len(y)):
        exits[i] = prev + entrants[i] - stock[i]
        prev = stock[i]
    # B1
    b1 = float(np.max(np.abs(stock - (np.concatenate([[0.0], stock[:-1]]) + entrants - exits))))
    b1_neg = float((exits < -1e-6).sum())
    # B2 per cohort
    cat = S['c_cat']; cn = S['c_n'].sum((1, 2)).astype(float)
    final = cat.sum((1, 2, 3))
    still = np.maximum(cn - final, 0.0)
    b2 = float(np.max(np.abs(still + final - cn)))
    # shares by cohort
    n = np.maximum(cn, 1)
    prim = cat[:, :, :, PRI:].sum((1, 2, 3)) / n
    lowsec = cat[:, :, :, JHS:].sum((1, 2, 3)) / n
    upsec = cat[:, :, :, BASIC:].sum((1, 2, 3)) / n
    deg = cat[:, :, :, [4, 5, 6, 7]].sum((1, 2, 3)) / n
    # B3
    b3 = []
    for nm, v in [('prim', prim), ('lowsec', lowsec), ('upsec', upsec), ('deg', deg)]:
        if np.nanmin(v) < -1e-9 or np.nanmax(v) > 1 + 1e-9:
            b3.append(nm)
    if (stock < -1e-9).any() or (exits < -1e-6).any():
        b3.append('stock/exits')
    pc = S['pool_cat']
    formal = pc[:, [1, 2, 4], :].sum((1, 2)) / np.maximum(pc.sum((1, 2)), 1)
    informal = pc[:, 5, :].sum(1) / np.maximum(pc.sum((1, 2)), 1)
    return dict(year=y, entrants=entrants, stock=stock, exits=exits, prim=prim, lowsec=lowsec,
                upsec=upsec, deg=deg, formal=formal, informal=informal,
                b1=b1, b1_neg=b1_neg, b2=b2, b3=b3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--N', type=int, default=3000)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    rows, hrows, checks, txt = [], [], [], []
    for iso in ISO:
        p = make_params(**CFG.build(iso, best_params(iso)))
        p['N'] = a.N; p['seed'] = 33000; p['t1'] = 2040
        S = run_model(p)
        L = ledger(S, iso, a.N)
        checks.append(dict(iso=iso, b1_max_abs_identity_error=L['b1'], b1_negative_exit_years=int(L['b1_neg']),
                           b2_max_cohort_conservation_error=L['b2'],
                           b3_violations=','.join(L['b3']) if L['b3'] else 'none',
                           entrants_total=float(L['entrants'].sum()), exits_total=float(L['exits'].sum()),
                           stock_2040=float(L['stock'][-1])))
        # annual ledger CSV (1980-2040)
        for i, yy in enumerate(L['year']):
            if 1980 <= yy <= 2040:
                rows.append(dict(iso=iso, year=int(yy), entrants=float(L['entrants'][i]), enrolled_stock=float(L['stock'][i]),
                                 exits=float(L['exits'][i]), primary_enrolled=float(S['enrol'][i, 0]),
                                 secondary_enrolled=float(S['enrol'][i, 1]), tertiary_enrolled=float(S['enrol'][i, 2]),
                                 formal_share=float(L['formal'][i]), informal_share=float(L['informal'][i])))
        # completion series mapped to year (entry+10, or +12 for PHL entry>=2006)
        add = np.where((iso == 'PHL') & (L['year'] >= 2006), 12, 10)
        cy = L['year'] + add
        for i, yy in enumerate(cy):
            if 1980 <= yy <= 2040 and yy in HORIZON:
                hrows.append(dict(iso=iso, year=int(yy), entrants=float(L['entrants'][i]),
                                  completion_primary=float(L['prim'][i]),
                                  completion_lower_secondary=float(L['lowsec'][i]),
                                  completion_upper_secondary=float(L['upsec'][i]),
                                  degree=float(L['deg'][i]),
                                  formal_share=float(L['formal'][min(i, len(L['formal']) - 1)]),
                                  informal_share=float(L['informal'][min(i, len(L['informal']) - 1)])))
    write_rows(os.path.join(a.out, 'cohort_ledger_annual.csv'), list(rows[0].keys()), [[r[k] for k in rows[0]] for r in rows])
    write_rows(os.path.join(a.out, 'cohort_horizon_table.csv'), list(hrows[0].keys()), [[r[k] for k in hrows[0]] for r in hrows])
    write_rows(os.path.join(a.out, 'balance_checks.csv'), list(checks[0].keys()), [[c[k] for k in checks[0]] for c in checks])
    # 10/20/30/40-year deltas from 2000
    dtxt = []
    for iso in ISO:
        base = [r for r in hrows if r['iso'] == iso and r['year'] == 2000]
        if not base:
            continue
        b = base[0]
        for h in (2010, 2020, 2030, 2040):
            r = [x for x in hrows if x['iso'] == iso and x['year'] == h]
            if not r:
                continue
            r = r[0]
            dtxt.append(f'  {iso} +{h - 2000:2d}y: upsec {b["completion_upper_secondary"]:.3f}->{r["completion_upper_secondary"]:.3f} '
                        f'({r["completion_upper_secondary"] - b["completion_upper_secondary"]:+.3f}); degree '
                        f'{b["degree"]:.3f}->{r["degree"]:.3f}; formal {b["formal_share"]:.3f}->{r["formal_share"]:.3f}')
    L = ['LOOP2 LONGITUDINAL COHORT LEDGER 1980-2040 (simulated system, not observed flows)',
         f'N={a.N}, seed 33000, per-country best calibration point; wall={time.time() - t0:.0f}s', '',
         'BALANCE CHECKS (must hold exactly):']
    for c in checks:
        L.append(f'  {c["iso"]}: B1 stock-identity max abs error {c["b1_max_abs_identity_error"]:.2e} '
                 f'(negative-exit years {c["b1_negative_exit_years"]}); B2 cohort conservation max error '
                 f'{c["b2_max_cohort_conservation_error"]:.2e}; B3 violations: {c["b3_violations"]}; '
                 f'entrants {c["entrants_total"]:.0f} exits {c["exits_total"]:.0f}')
    L += ['', '10/20/30/40-YEAR TABLE (deltas from the year-2000 cohort):'] + dtxt
    L += ['', 'Definitions (declared): completion_* are shares of the school-entry cohort with at least that final',
          'credential, indexed by entry year + 10 (+12 for PHL cohorts entering >=2006). formal_share is the share of',
          'that year\'s labour-market entrants in elite/mid/routine domestic pools; informal_share is the pool-5 share.',
          'These are model states, not observed country values. Rates are bounded in [0,1] and checked.']
    write_text(os.path.join(a.out, 'findings_ledger.txt'), '\n'.join(L) + '\n')
    json.dump(dict(N=a.N, wall=time.time() - t0, horizon=HORIZON, checks=checks),
              open(os.path.join(a.out, 'run_meta_ledger.json'), 'w'), indent=1)
    print('done', time.time() - t0)


if __name__ == '__main__':
    main()
