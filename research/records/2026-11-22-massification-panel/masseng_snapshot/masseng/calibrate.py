"""Fit behavioural parameters on training rows only, then score test rows against the model and two naive
benchmarks (persistence, linear trend). See PROTOCOL.md."""
import numpy as np
from scipy.optimize import least_squares

from .engine import Model, DEFAULTS

FITTED = ['eta', 'eta_x', 'kappa', 'a_prim', 'a_sec', 'a_sec_entry', 'a_ter', 'a_ter_entry', 'mu_basic', 'mu_ter', 'nu', 'nu_ter', 'k_ter']
BOUNDS = dict(eta=(0.0, 6.0), eta_x=(0.0, 4.0), kappa=(0.0, 40.0), a_prim=(-2, 16), a_sec=(-2, 16), a_sec_entry=(-8, 14),
              a_ter=(-2, 16), a_ter_entry=(-10, 12), mu_basic=(-10, 6), mu_ter=(-8, 8), nu=(-6, 8), nu_ter=(-6, 8),
              k_ter=(0.005, 0.6), k_growth=(-0.05, 0.25), k_resp=(0.0, 2.0))


def fitted_names(supply_rule, demand_form='income', split=True, split_nu=True):
    names = list(FITTED)
    if not split_nu:
        names.remove('nu_ter')
    if supply_rule == 'trend':
        names.append('k_growth')
    if supply_rule == 'responsive':
        names.append('k_resp')
    if supply_rule == 'unconstrained':
        names.remove('k_ter')
    if demand_form == 'none':
        names.remove('eta')
    if not split:
        names.remove('eta_x')
    return names


def predict(model_result, rows):
    yrs = list(model_result.years)
    out = []
    for r in rows:
        s = model_result.ind.get(r['series'])
        out.append(np.nan if s is None or r['year'] not in yrs else float(s[yrs.index(r['year'])]))
    return np.array(out)


def _weights(rows):
    n = {}
    for r in rows:
        n[r['series']] = n.get(r['series'], 0) + 1
    return np.array([1.0 / np.sqrt(n[r['series']]) for r in rows])


def fit(country, train, supply_rule=None, demand_form='income', start=None, fixed=None, switches=None,
        max_nfev=400, ftol=1e-8, burden_form='log', split_income=True, split_nu=True):
    """Least-squares fit to TRAINING rows only. `train` must contain only rows with role 'train'."""
    assert all(r['role'] == 'train' for r in train), 'fit() received non-training rows'
    supply_rule = supply_rule or country.config['tertiary_public_capacity']['rule']
    names = fitted_names(supply_rule, demand_form, split_income, split_nu)
    base = dict(DEFAULTS)
    if demand_form == 'none':
        base['eta'] = 0.0
    if fixed:
        base.update(fixed)
        names = [n for n in names if n not in fixed]
    if start:
        base.update({k: v for k, v in start.items() if k in base})
    x0 = np.array([np.clip(base[n], *BOUNDS[n]) for n in names])
    lo = np.array([BOUNDS[n][0] for n in names])
    hi = np.array([BOUNDS[n][1] for n in names])
    obs = np.array([r['value'] for r in train])
    w = _weights(train)

    def resid(x):
        prm = dict(base)
        prm.update(dict(zip(names, x)))
        res = Model(country, prm, supply_rule=supply_rule, demand_form=demand_form, switches=switches,
                    burden_form=burden_form, split_income=split_income, split_nu=split_nu).run()
        pred = predict(res, train)
        r = (pred - obs) * w
        return np.nan_to_num(r, nan=50.0)

    sol = least_squares(resid, x0, bounds=(lo, hi), x_scale='jac', max_nfev=max_nfev, diff_step=1e-3,
                        ftol=ftol, xtol=ftol)
    prm = dict(base)
    prm.update(dict(zip(names, sol.x)))
    return dict(params=prm, fitted=names, cost=float(sol.cost), nfev=int(sol.nfev), success=bool(sol.success),
                supply_rule=supply_rule, demand_form=demand_form, switches=switches or {}, burden_form=burden_form,
                split_income=split_income, split_nu=split_nu)


def benchmarks(rows_train_all, test):
    """N1 persistence and N2 linear trend, per series, computed from all training-window observations of that
    series (including diagnostic rows, which are observed but not fitted)."""
    out = []
    for r in test:
        hist = sorted((q['year'], q['value']) for q in rows_train_all if q['series'] == r['series'])
        if len(hist) == 0:
            out.append((np.nan, np.nan))
            continue
        n1 = hist[-1][1]
        if len(hist) >= 3:
            b = np.polyfit([h[0] for h in hist], [h[1] for h in hist], 1)
            n2 = float(np.polyval(b, r['year']))
        else:
            n2 = n1
        out.append((n1, n2))
    return np.array(out)


def score(country, fitres, rows):
    """Test RMSE per series for the model and the two benchmarks."""
    res = Model(country, fitres['params'], supply_rule=fitres['supply_rule'], demand_form=fitres['demand_form'],
                switches=fitres.get('switches'), burden_form=fitres.get('burden_form', 'linear'),
                split_income=fitres.get('split_income', False),
                split_nu=fitres.get('split_nu', False)).run(record_deciles=True)
    test = [r for r in rows if r['role'] == 'test']
    window = [r for r in rows if r['role'] in ('train', 'diagnostic')]
    pred = predict(res, test)
    bm = benchmarks(window, test)
    table = {}
    for s in sorted({r['series'] for r in test}):
        idx = [i for i, r in enumerate(test) if r['series'] == s]
        o = np.array([test[i]['value'] for i in idx])
        def rmse(p):
            p = np.asarray(p, float)
            m = ~np.isnan(p)
            return float(np.sqrt(np.mean((p[m] - o[m]) ** 2))) if m.any() else np.nan
        table[s] = dict(n=len(idx), model=rmse(pred[idx]), persistence=rmse(bm[idx, 0]), trend=rmse(bm[idx, 1]))
    return res, table, pred
