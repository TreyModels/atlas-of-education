"""Shared helpers for the youth-review experiments. Imports the engine in engine/firms; writes only into results/.

Scoring is identical to engine/firms/calibrate_china.py: residuals are model minus NBS over the observation pairs
returned by calibrate_china.pairs_for(R, window) ('early' = 2018-22 old method; 'full' = 2018-26 old plus 2023-26 new).
"""
import json, math, os, sys
import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, '..', '..', 'engine'))
sys.path.insert(0, ENGINE)
from firms import model as M, calibrate_china as K, data_china as D  # noqa: E402

RES = os.path.join(HERE, 'results')
os.makedirs(RES, exist_ok=True)

# Bounds before this review (copied from the pre-review calibrate_china.py). Used to reproduce the old fit.
OLD_BOUNDS = {'m_g': (0.03, 0.50), 'm_n': (0.03, 0.42), 'f_g_ref': (0.05, 0.38), 'f_n_ref': (0.05, 0.38),
              'lam_g': (0.002, 1.0), 'zeta': (0.0, 1.0), 'm_a': (0.02, 0.6), 'sep_scale': (0.2, 2.5),
              'july_g': (0.2, 1.0), 'e_prop': (0.0, 1.0), 'dr_drop': (0.0, 0.3)}
START = {f[0]: f[3] for f in K.FREE}
NEW_BOUNDS = {f[0]: (f[1], f[2]) for f in K.FREE}   # as now in calibrate_china.py


def free_list(bounds, drop=()):
    """[(name, lo, hi, start)] in the engine's parameter order, without the names in `drop`."""
    return [(n, bounds[n][0], bounds[n][1], START[n]) for n in START if n in bounds and n not in drop]


def model_run(params, fixed=None):
    kw = dict(K.REF); kw.update(fixed or {}); kw.update({k: float(v) for k, v in params.items()})
    return M.YouthMarket(D, **kw).run()


def residuals(R, window):
    pr = K.pairs_for(R, window)
    r = np.array([mod - ob for *_, ob, mod, _ in pr])
    return r


N_PAIRS = {'full': 98, 'early': 60}   # number of observation pairs per window (see calibrate_china.pairs_for)


def fit(free, fixed, window, nstarts=6, seed=1, warm=None):
    """Same multistart as calibrate_china.fit (first start = engine start values, then uniform draws, seed 1).
    warm: optional {name: value} (e.g. the on-disk optimum). It is added as one more start, clipped to the bounds, so a
    widened search can never end above a feasible point it was given. Start index of the winner is recorded."""
    names = [f[0] for f in free]
    lo = np.array([f[1] for f in free]); hi = np.array([f[2] for f in free])

    def resid(th):
        # infeasible points (the model raises, e.g. margin too large for z, or f >= a) get the same penalty as non-finite
        # residuals in the engine, so the optimiser steers away from them instead of aborting the start
        try:
            R = model_run(dict(zip(names, th)), fixed)
            r = residuals(R, window)
        except ValueError:
            return np.full(N_PAIRS[window], 50.0)
        return r if np.all(np.isfinite(r)) else np.full(len(r), 50.0)

    rng = np.random.default_rng(seed)
    starts = [np.array([f[3] for f in free])]
    if warm:
        w = np.array([warm.get(n, f[3]) for n, f in zip(names, free)], dtype=float)
        starts.append(np.clip(w, lo + 1e-9 * (hi - lo), hi - 1e-9 * (hi - lo)))
    starts += [rng.uniform(lo, hi) for _ in range(nstarts - 1)]
    best, costs, best_i = None, [], None
    for i, s in enumerate(starts):
        try:
            r = least_squares(resid, s, bounds=(lo, hi), diff_step=1e-3, max_nfev=300)
        except ValueError:
            costs.append(None)
            continue
        costs.append(float(r.cost))
        if best is None or r.cost < best.cost:
            best, best_i = r, i
    if best is None:
        raise RuntimeError('every start failed')
    best.winning_start = best_i
    return best, costs, names


def vg_safe(R):
    """K.vg_check divides by the 2024 H1 graduate vacancy mean; a variant with no graduate vacancies returns NaN."""
    try:
        return K.vg_check(R)
    except ZeroDivisionError:
        return float('nan')


def summarise(params, fixed, window, cost=None, extra=None):
    """Scores of one parameter set in the same terms the engine uses for the headline."""
    R = model_run(params, fixed)
    E, L = K.EARLY, K.LATE
    out = dict(window=window, fixed=fixed, params={k: float(v) for k, v in params.items()}, cost=cost,
               fit_early=K.stats(K.obs_pairs(R, 2018, 2022, 'old')),
               holdout_old_2023H1=K.stats(K.obs_pairs(R, 2023, 2023, 'old')),
               new_verified=K.stats(K.obs_pairs(R, 2023, 2026, 'new', flags=('v',))),
               whole_record=K.stats(K.pairs_for(R, 'full')),
               rate_change=K.outcome(R), grad_u_change=K.outcome(R, 'u_G'),
               late_rate=K.window_mean(R, 'rate_new', *L), vg_2025H1_pct=vg_safe(R))
    if extra:
        out.update(extra)
    return out


def dump(name, obj):
    path = os.path.join(RES, name)
    with open(path, 'w') as f:
        json.dump(obj, f, indent=1, default=float)
    return path


def fmt(d):
    return json.dumps(d, indent=1, default=float)
