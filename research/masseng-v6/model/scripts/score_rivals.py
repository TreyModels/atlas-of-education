#!/usr/bin/env python3
"""Score every fitted rival on the test rows (PROTOCOL.md sections 3, 5, 6, 7). Writes outputs/<ISO>/scores.json."""
import glob, json, os, sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import masseng as m
from masseng import targets as T, calibrate as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISO = sys.argv[1] if len(sys.argv) > 1 else 'PHL'
VERSION = sys.argv[2] if len(sys.argv) > 2 else 'v2'


def change(res, series, y0, y1):
    yrs = list(res.years)
    s = res.ind[series]
    return float(s[yrs.index(y1)] - s[yrs.index(y0)])


def obs_change(c, code, y0, y1):
    s = c.wdi(code).observed()
    return float(s[y1] - s[y0]) if y0 in s and y1 in s else None


def main():
    c = m.Country(ISO)
    rows = T.build(c)
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, 'outputs', ISO, VERSION, 'fit_*.json'))):
        f = json.load(open(path))
        res, table, pred = C.score(c, f, rows)
        key = f"{f['demand_form']}|{f['supply_rule']}"
        ger = [table[s]['model'] for s in ('ger_primary', 'ger_secondary', 'ger_tertiary') if s in table]
        entry = dict(train_cost=f['cost'], params={k: f['params'][k] for k in f['fitted']}, table=table,
                     mean_test_rmse_ger=float(np.mean(ger)))
        sep = {}
        if ISO == 'PHL':
            for (a, b) in ((1983, 1987), (1997, 1999), (2009, 2016)):
                for s, code in (('ger_secondary', 'SE.SEC.ENRR'), ('ger_tertiary', 'SE.TER.ENRR')):
                    sep[f'{s} {a}->{b}'] = dict(model=change(res, s, a, b), observed=obs_change(c, code, a, b))
            ched = c.config['targets']['ched_tertiary']
            yrs = list(res.years)
            # CHED headcount ratio vs model tertiary enrolment (GER x band population) ratio
            def enrol(y):
                lo, hi = res_band(res, c, y)
                return None
            sep['ched_total_2018_vs_2016'] = dict(observed=ched['2017-18']['total'] / ched['2015-16']['total'])
            sep['ched_total_2020_vs_2016'] = dict(observed=ched['2019-20']['total'] / ched['2015-16']['total'])
        if ISO == 'KHM':
            for (a, b) in ((2013, 2015), (2013, 2017)):
                sep[f'ger_tertiary {a}->{b}'] = dict(model=change(res, 'ger_tertiary', a, b),
                                                     observed=obs_change(c, 'SE.TER.ENRR', a, b))
        entry['separating'] = sep
        # income gradient: richest / poorest decile participation (model) vs survey ratio
        tg = c.config.get('targets', {})
        grad = tg.get('income_gradient_2019') or tg.get('income_gradient_2012')
        gy = 2019 if 'income_gradient_2019' in tg else 2012
        if grad and gy in res.extra['deciles']:
            dp = res.extra['deciles'][gy]
            g = {}
            for lev, v in grad.items():
                if lev.startswith('_') or dp.get(lev) is None:
                    continue
                g[lev] = dict(model_ratio=dp[lev][9] / max(dp[lev][0], 1e-9),
                              survey_ratio=v['richest'] / v['poorest'])
            entry['income_gradient'] = g
        out[key] = entry
    json.dump(out, open(os.path.join(ROOT, 'outputs', ISO, VERSION, 'scores.json'), 'w'), indent=1, default=float)
    for k, v in out.items():
        print(f"\n== {k}  train cost {v['train_cost']:.2f}  mean test RMSE (GER) {v['mean_test_rmse_ger']:.2f}")
        for s, t in v['table'].items():
            bms = [x for x in (t['persistence'], t['trend']) if x == x]
            flag = '  - ' if not bms else ('WIN ' if t['model'] < min(bms) else 'loss')
            print(f"   {flag} {s:22s} n={t['n']:2d} model {t['model']:6.2f}  persistence {t['persistence']:6.2f}  trend {t['trend']:6.2f}")
        for s, t in v['separating'].items():
            print('   sep', s, {kk: (round(x, 2) if isinstance(x, float) else x) for kk, x in t.items()})
        for s, t in v.get('income_gradient', {}).items():
            print('   gradient', s, {kk: round(x, 2) for kk, x in t.items()})


def res_band(res, c, y):
    return None, None


if __name__ == '__main__':
    main()
