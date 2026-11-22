"""Calibration and scoring for engine5 (PROTOCOL_v5.md sections 5-7)."""
import json
import os

import numpy as np
from scipy.optimize import least_squares

from . import targets as T
from .engine5 import Model5, DEFAULTS, SPECS, BASE_FIT

BOUNDS = dict(a_prim=(-4, 16), a_sec=(-4, 16), a_sec_entry=(-10, 14), a_ter=(-4, 16), a_ter_entry=(-12, 12),
              b_h=(-6, 12), b_p=(-6, 12), b_r=(-12, 24), eta=(0, 6), eta_x=(0, 4), kappa=(0, 40), lam=(-6, 12),
              c_scale=(0.05, 8), mu_basic=(-10, 6), mu_ter=(-8, 8), nu=(-6, 8))


def fitted_names(spec):
    return BASE_FIT + SPECS[spec]['fit']


def build_rows(country):
    """v3 rows (enrolment, private shares, gradients) plus v5 rows from targets_v5.json mapped through
    config['v5']['target_map'] = {source_series: {"model": indicator, "train_years": [...], "transform": ...}}."""
    rows = T.build(country)
    lo, hi = country.config['years']['train']
    v5 = country.config.get('v5', {})
    tmap = v5.get('target_map', {})
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'countries', country.iso3,
                        'targets_v5.json')
    if os.path.exists(path) and tmap:
        raw = json.load(open(path)).get('rows', [])
        for r in raw:
            m = tmap.get(r['series'])
            if not m or not isinstance(r.get('value'), (int, float)) or not r.get('verified', False):
                continue
            y = int(r['year'])
            role = 'train' if y in m.get('train_years', []) else ('test' if y > hi or m.get('all_test') else 'diagnostic')
            if m.get('only_years') and y not in m['only_years']:
                continue
            val = r['value'] * r.get('scale', 1.0) * m.get('scale', 1.0)
            if m.get('transform') == 'index_2016':
                bases = [q['value'] * q.get('scale', 1.0) for q in raw
                         if q['series'] == r['series'] and int(q['year']) == 2016 and q.get('verified', False)]
                if len(bases) != 1 or bases[0] == 0:
                    raise ValueError(f"{r['series']}: exactly one verified nonzero 2016 index base is required")
                val /= bases[0]
            rows.append(dict(series=m['model'], year=y, value=val, role=role, source=r.get('source', '')[:160],
                             transform=m.get('transform')))
    return rows


def _pred(res, rows):
    yrs = list(res.years)
    out = []
    for r in rows:
        s = res.ind.get(r['series'])
        if s is None or r['year'] not in yrs:
            out.append(np.nan)
            continue
        v = float(s[yrs.index(r['year'])])
        if r.get('transform') == 'index_2016':          # e.g. CHED headcount relative to AY2015-16
            v = v / float(s[yrs.index(2016)])
        if r['series'] == 'trans_lsec_usec':             # engine fraction; registered target is percent
            v *= 100.0
        out.append(v)
    return np.array(out)


def _w(rows):
    n = {}
    for r in rows:
        n[r['series']] = n.get(r['series'], 0) + 1
    return np.array([1.0 / np.sqrt(n[r['series']]) for r in rows])


def fit(country, train, spec, start=None, max_nfev=250, ftol=1e-7, switches=None):
    assert all(r['role'] == 'train' for r in train), 'fit() received non-training rows'
    fixed = country.config.get('v5', {}).get('fixed_params', {})
    names = [n for n in fitted_names(spec) if n not in fixed]
    base = dict(DEFAULTS)
    base.update({k: v for k, v in fixed.items() if not k.startswith('_')})
    if start:
        base.update({k: v for k, v in start.items() if k in base})
    model = Model5(country, base, spec=spec, switches=switches)
    x0 = np.array([np.clip(base[n], *BOUNDS[n]) for n in names])
    lo = np.array([BOUNDS[n][0] for n in names]); hi = np.array([BOUNDS[n][1] for n in names])
    obs = np.array([r['value'] for r in train])
    # spending and index targets are small numbers: scale so 1 unit of error weighs like 1 pp of enrolment
    scale = np.array([10.0 if r['series'].startswith('edu_share') else (100.0 if r.get('transform') == 'index_2016'
                      else 1.0) for r in train])
    w = _w(train) * scale

    def resid(x):
        prm = dict(base); prm.update(dict(zip(names, x)))
        res = model.set_params(prm).run()
        return np.nan_to_num((_pred(res, train) - obs) * w, nan=50.0)

    sol = least_squares(resid, x0, bounds=(lo, hi), x_scale='jac', max_nfev=max_nfev, diff_step=1e-3, ftol=ftol, xtol=ftol)
    prm = dict(base); prm.update(dict(zip(names, sol.x)))
    return dict(params=prm, fitted=names, cost=float(sol.cost), nfev=int(sol.nfev), spec=spec,
                at_bounds=[n for n, v in zip(names, sol.x) if abs(v - BOUNDS[n][0]) < 1e-3 or abs(v - BOUNDS[n][1]) < 1e-3])


def benchmarks(window, test):
    out = []
    for r in test:
        hist = sorted((q['year'], q['value']) for q in window if q['series'] == r['series'])
        if not hist:
            out.append((np.nan, np.nan)); continue
        n1 = hist[-1][1]
        n2 = float(np.polyval(np.polyfit([h[0] for h in hist], [h[1] for h in hist], 1), r['year'])) if len(hist) >= 3 else n1
        out.append((n1, n2))
    return np.array(out)


def score(country, f, rows):
    res = Model5(country, f['params'], spec=f['spec']).run(record_deciles=True)
    test = [r for r in rows if r['role'] == 'test']
    window = [r for r in rows if r['role'] in ('train', 'diagnostic') and r['year'] <= country.config['years']['train'][1]]
    pred = _pred(res, test)
    bm = benchmarks(window, test)
    table = {}
    for s in sorted({r['series'] for r in test}):
        idx = [i for i, r in enumerate(test) if r['series'] == s]
        o = np.array([test[i]['value'] for i in idx])
        def rmse(p):
            p = np.asarray(p, float); m = ~np.isnan(p)
            return float(np.sqrt(np.mean((p[m] - o[m]) ** 2))) if m.any() else np.nan
        table[s] = dict(n=len(idx), model=rmse(pred[idx]), persistence=rmse(bm[idx, 0]), trend=rmse(bm[idx, 1]),
                        obs=o.tolist(), pred=pred[idx].tolist(), years=[test[i]['year'] for i in idx])
    return res, table
