"""Plain lake-model null for the China youth unemployment series (review item 1.8).

One labour-force pool, no categories, no wages, no firms, no demand series. Monthly flows with CONSTANT rates:
  job-finding f, separation s (both per month), exit a (fixed at 1/27, the graduate age-out rate in the engine).
  U_{t+1} = (1 - f - a) U_t + s E_t + I_{t+1}        E_{t+1} = (1 - s - a) E_t + f U_t
  rate_t = 100 U_t / (U_t + E_t)
Entrants I follow the same observed inflow as the engine (psi_g x graduates + psi_n x non-graduate leavers, the engine's
DEFAULTS psi values), with one fitted July share q and the rest spread over August-December. Method offset delta is
added to old-method observations (students counted), fitted. Free parameters: f, s, q, delta (4), against 11 in the headline. An entrant-scale parameter was tried and dropped:
the system is linear in the inflow, so the scale is not identified (the rate does not depend on it). Scored with calibrate_china.pairs_for / obs_pairs, the same residuals as the full model.

Run: python lake_null.py   -> results/lake_null.json
"""
import json, math, os, sys
import numpy as np
from scipy.optimize import least_squares
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import K, M, D, dump  # noqa: E402

A_EXIT = 1 / 27
PSI_G, PSI_N = M.DEFAULTS['psi_g'], M.DEFAULTS['psi_n']
MONTHS = [(y, m) for y in range(2010, 2027) for m in range(1, 13)]


def simulate(f, s, q, delta):
    U, E = 0.0, 0.0
    R = dict(year=[], month=[], rate_old=[], rate_new=[])
    for y, m in MONTHS:
        annual = PSI_G * D.graduates(y) + PSI_N * D.nongrad_school_leavers(y)
        inflow = annual * (q if m == 7 else ((1 - q) / 5 if m >= 8 else 0.0))
        U, E = (1 - f - A_EXIT) * U + s * E + inflow, (1 - s - A_EXIT) * E + f * U
        rate = 100 * U / (U + E) if U + E > 0 else float('nan')
        R['year'].append(y); R['month'].append(m); R['rate_new'].append(rate); R['rate_old'].append(rate + delta)
    return R


def resid_fn(window):
    def resid(th):
        R = simulate(*th)
        pr = K.pairs_for(R, window)
        r = np.array([mod - ob for *_, ob, mod, _ in pr])
        return r if np.all(np.isfinite(r)) else np.full(len(r), 50.0)
    return resid


def run(window):
    # f + a <= 1 and s + a <= 1 keep both stocks non-negative (the U update has coefficient 1 - f - a)
    lo = np.array([0.001, 0.0005, 0.05, -5.0]); hi = np.array([1 - A_EXIT - 1e-3, 1 - A_EXIT - 1e-3, 1.0, 5.0])
    rng = np.random.default_rng(1)
    starts = [np.array([0.05, 0.02, 0.7, 0.0])] + [rng.uniform(lo, hi) for _ in range(9)]
    best = None
    for st in starts:
        r = least_squares(resid_fn(window), st, bounds=(lo, hi), diff_step=1e-3, max_nfev=400)
        if best is None or r.cost < best.cost:
            best = r
    th = best.x
    R = simulate(*th)
    rec = dict(window=window, params=dict(f=th[0], s=th[1], q=th[2], delta=th[3]), cost=float(best.cost),
               steady_state_rate_new=100 * th[1] / (th[0] + th[1]) if th[0] + th[1] > 0 else None,
               fit_early=K.stats(K.obs_pairs(R, 2018, 2022, 'old')),
               holdout_old_2023H1=K.stats(K.obs_pairs(R, 2023, 2023, 'old')),
               new_verified=K.stats(K.obs_pairs(R, 2023, 2026, 'new', flags=('v',))),
               whole_record=K.stats(K.pairs_for(R, 'full')))
    return rec


if __name__ == '__main__':
    out = {w: run(w) for w in ('early', 'full')}
    dump('lake_null.json', out)
    for w, r in out.items():
        print(w, {k: round(v, 4) for k, v in r['params'].items()}, 'cost', round(r['cost'], 2),
              'fit MAE', round(r['fit_early']['mae'], 3) if r['fit_early'].get('n') else None,
              'holdout 2023H1 MAE', round(r['holdout_old_2023H1']['mae'], 3),
              'new MAE', round(r['new_verified']['mae'], 3), flush=True)
