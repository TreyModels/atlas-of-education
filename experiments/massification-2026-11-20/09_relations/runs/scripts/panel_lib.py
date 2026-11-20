"""Two-way fixed-effects OLS with country-clustered SE — small, explicit, no black boxes.
Observed cells only. Within transformation via alternating projections (country demean, year demean) repeated.
"""
from math import erf as _erf
import numpy as np, pandas as pd
_erf = np.vectorize(_erf)

def load_panel(path=None):
    import os
    p = path or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'panel_wdi_wide.csv')
    d = pd.read_csv(p)
    d['country'] = d['iso3']            # entity
    return d.sort_values(['iso3','year']).reset_index(drop=True)

def _demean_twoway(M, gid, tid, iters=50, tol=1e-10):
    """M: (n,k) matrix. Alternating projections within group and time."""
    M = M.copy()
    for _ in range(iters):
        old = M.copy()
        gm = pd.DataFrame(M).groupby(gid).transform('mean').values
        M = M - gm
        tm = pd.DataFrame(M).groupby(tid).transform('mean').values
        M = M - tm
        if np.nanmax(np.abs(M-old)) < tol: break
    return M

def fe_ols(d, y, xs, entity='iso3', time='year', cluster='iso3', lags=None, diff=False,
           min_n=60, min_cty=8):
    """Two-way FE. Returns dict with coef/se/t/N/cty/yrs or {'error':...}.
    lags: dict {x: k} applying k-year lag(s) within entity. diff=True first-differences y and x."""
    cols = [y] + list(xs)
    dd = d[[entity, time] + cols].dropna().copy()
    if lags:
        for x, k in lags.items():
            if x in dd: dd[x] = dd.groupby(entity)[x].shift(k)
        dd = dd.dropna()
    if diff:
        for c in [y] + list(xs):
            dd[c] = dd.groupby(entity)[c].diff()
        dd = dd.dropna()
    n = len(dd)
    if n < min_n or dd[entity].nunique() < min_cty:
        return dict(error=f'insufficient obs (n={n}, ctys={dd[entity].nunique()})')
    yv = dd[[y]].values.astype(float)
    X = dd[list(xs)].values.astype(float)
    gid = dd[entity].values; tid = dd[time].values
    # check variation after within transform
    Xw = _demean_twoway(X, gid, tid)
    yw = _demean_twoway(yv, gid, tid).reshape(-1, 1)
    ok = np.std(Xw, axis=0) > 1e-9
    if not ok.all():
        return dict(error='no within variation in ' + ','.join(np.array(list(xs))[~ok]))
    XtX = Xw.T @ Xw
    try:
        b = np.asarray(np.linalg.solve(XtX, Xw.T @ yw)).ravel()
    except np.linalg.LinAlgError:
        return dict(error='singular XtX')
    e = (yw.ravel() - Xw @ b)
    # dof: n - k - (n_entities-1) - (n_years-1) - 1
    G = dd[cluster].nunique()
    nent = dd[entity].nunique(); nyr = dd[time].nunique()
    k = X.shape[1]
    dof = max(n - k - (nent-1) - (nyr-1), 1)
    # cluster sandwich (CR1)
    inv = np.linalg.pinv(XtX)
    meat = np.zeros((k,k))
    for g in dd[cluster].unique():
        m = (dd[cluster].values == g)
        Xg, eg = Xw[m], e[m]
        s = Xg.T @ eg
        meat += np.outer(s, s)
    scale = (G/(G-1)) * ((n-1)/dof)
    V = inv @ meat @ inv * scale
    se = np.sqrt(np.diag(V))
    tstats = np.asarray(b/se).ravel() if np.all(se > 0) else np.full(k, np.nan)
    p = 2.0 * (1.0 - 0.5 * (1.0 + _erf(np.abs(tstats) / np.sqrt(2.0))))   # two-sided normal
    out = dict(n=n, n_cty=nent, n_yr=nyr, n_clusters=G, dof=dof,
               period=f'{int(dd[time].min())}-{int(dd[time].max())}',
               r2_within=1.0 - float(np.asarray(e@e).ravel()[0])/max(float(np.asarray(yw.T @ yw).ravel()[0]),1e-12))
    for i,x in enumerate(xs):
        out[x] = dict(coef=float(b[i]), se=float(se[i]), t=float(tstats[i]), p=float(p[i]))
    return out

def fmt(res, y=None, x=None):
    if 'error' in res: return f'  ERR {res["error"]}'
    a = res[x]
    return (f'  {x:22s} -> {y:18s} b={a["coef"]:+.4f} (se {a["se"]:.4f}, t {a["t"]:+.2f}, p {a["p"]:.3f})'
            f'  n={res["n"]} ctys={res["n_cty"]} {res["period"]} within-R2={res["r2_within"]:.3f}')

def fe_table(d, y, x, lags=(0,3,5), logy=True, logx=False):
    rows=[]
    for kl in lags:
        dd = d.copy()
        yy = y; xx = x
        if logy: dd['_y'] = np.log(dd[y].clip(lower=1e-3)) if (dd[y]>0).all() or 'GER' in y else dd[y]; yy='_y'
        if logx: dd['_x'] = np.log(dd[x].clip(lower=1e-6)); xx='_x'
        r = fe_ols(dd, yy, [xx], lags={xx:kl} if kl>0 else None)
        rows.append((kl,r))
    return rows
