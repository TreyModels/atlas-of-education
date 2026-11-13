"""Refits for review items 1.1 (fixed data-based step), 1.2 (widened bounds), 1.3 (lam_g pinned).

Usage (from anywhere):
  python run_fits.py baseline    # score the parameter sets currently on disk
  python run_fits.py bounds      # old vs new bounds, window full and early (old bounds reproduce the on-disk fit)
  python run_fits.py step        # dr_drop fixed at the data-based values, others free (new bounds)
  python run_fits.py lam         # lam_g pinned at the data-derived values, others free (new bounds)
Each writes results/<name>.json. Parameter sets are at sigma_A = 5 (the headline), as in calibrate_china.
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (K, OLD_BOUNDS, NEW_BOUNDS, free_list, fit, summarise, dump, RES)

ENGINE_FIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine', 'firms', 'results', 'china_fit.json')


def at_bounds(params, bounds, tol=1e-3):
    out = []
    for k, v in params.items():
        lo, hi = bounds[k]
        span = hi - lo
        if abs(v - lo) < tol * span or abs(v - hi) < tol * span:
            out.append(k)
    return out


NEW_A08 = dict(NEW_BOUNDS, f_n_ref=(0.05, 0.76))   # doubled f_n_ref bound; needs the application rate a raised to 0.80


def ondisk(window):
    """The engine's current optimum for this window (china_fit.json, sigma_A = 5), used as a warm start."""
    key = 'full|sigma_A=5.0' if window == 'full' else 'early|sigma_A=5.0'
    return json.load(open(ENGINE_FIT))['profiles'][key]['params']


def run_fit(name, bounds, fixed, window, drop=(), warm=True):
    t = time.time()
    free = free_list(bounds, drop=drop)
    best, costs, names = fit(free, fixed, window, warm=ondisk(window) if warm else None)
    params = dict(zip(names, best.x))
    s = summarise(params, fixed, window, cost=float(best.cost),
                  extra=dict(start_costs=costs, winning_start=int(best.winning_start), warm_start_used=warm,
                             n_resid=int(len(best.fun)), at_bounds=at_bounds(params, bounds),
                             seconds=round(time.time() - t, 1)))
    dump(name + '.json', s)
    print(name, 'cost', round(best.cost, 3), 'MAE early', round(s['fit_early']['mae'], 3),
          'holdout 2023H1', round(s['holdout_old_2023H1'].get('mae', float('nan')), 3),
          'new MAE', round(s['new_verified'].get('mae', float('nan')), 3),
          'rise', round(s['rate_change'], 2), 'at bounds', s['at_bounds'], flush=True)
    return s


def baseline():
    fj = json.load(open(ENGINE_FIT))
    for key in ('full|sigma_A=5.0', 'early|sigma_A=5.0'):
        p = fj['profiles'][key]['params']
        free_names = [f[0] for f in K.FREE]
        R_params = {k: p[k] for k in free_names}
        window = 'full' if key.startswith('full') else 'early'
        r = K.resid(np.array([p[k] for k in free_names]), window)
        s = summarise(R_params, {}, window, cost=float(0.5 * np.sum(r ** 2)),
                      extra=dict(source='engine/firms/results/china_fit.json', at_bounds=at_bounds(R_params, OLD_BOUNDS)))
        dump('baseline_' + key.split('|')[0] + '.json', s)
        print(key, 'cost', round(0.5 * np.sum(r ** 2), 3), 'rise', round(s['rate_change'], 2),
              'early MAE', round(s['fit_early']['mae'], 3), 'at bounds (old)', s['at_bounds'], flush=True)


def bounds():
    for window in ('full', 'early'):
        run_fit(f'bounds_old_{window}', OLD_BOUNDS, {}, window)
        run_fit(f'bounds_new_{window}', NEW_BOUNDS, {}, window)
        run_fit(f'bounds_new_a08_{window}', NEW_A08, {'a': 0.80}, window)


def step():
    d = json.load(open(os.path.join(RES, 'derived_inputs.json')))['dr_step']
    for lvl, tag in (('low', 'low'), ('central', 'central'), ('high', 'high')):
        run_fit(f'step_{tag}_full', NEW_BOUNDS, {'dr_drop': d[lvl]['dr']}, 'full', drop=('dr_drop',))
    run_fit('step_central_early', NEW_BOUNDS, {'dr_drop': d['central']['dr']}, 'early', drop=('dr_drop',))


def lam():
    L = json.load(open(os.path.join(RES, 'derived_inputs.json')))['lam_g']
    for tag, v in (('review', L['review_value']), ('data_central', L['data_central']), ('data_fast', L['data_fast_12m_halflife'])):
        run_fit(f'lam_{tag}_full', NEW_BOUNDS, {'lam_g': v}, 'full', drop=('lam_g',))


JOBS = {
    'bounds_old_full': (OLD_BOUNDS, {}, 'full', ()), 'bounds_new_full': (NEW_BOUNDS, {}, 'full', ()),
    'bounds_new_a08_full': (NEW_A08, {'a': 0.80}, 'full', ()),
    'bounds_old_early': (OLD_BOUNDS, {}, 'early', ()), 'bounds_new_early': (NEW_BOUNDS, {}, 'early', ()),
    'bounds_new_a08_early': (NEW_A08, {'a': 0.80}, 'early', ()),
}


def one(name):
    """Run one named fit as its own process (the batch runs them in parallel)."""
    if name.startswith('step_'):
        d = json.load(open(os.path.join(RES, 'derived_inputs.json')))['dr_step']
        lvl, window = (name.split('_')[1], name.split('_')[2])
        key = 'central' if lvl == 'central' else lvl
        run_fit(name, NEW_BOUNDS, {'dr_drop': d[key]['dr']}, window, drop=('dr_drop',))
    elif name.startswith('lam_'):
        L = json.load(open(os.path.join(RES, 'derived_inputs.json')))['lam_g']
        v = {'lam_review_full': L['review_value'], 'lam_data_central_full': L['data_central'],
             'lam_data_fast_full': L['data_fast_12m_halflife']}[name]
        run_fit(name, NEW_BOUNDS, {'lam_g': v}, 'full', drop=('lam_g',))
    else:
        bnd, fixed, window, drop = JOBS[name]
        run_fit(name, bnd, fixed, window, drop=drop, warm=not name.endswith('old_full') and not name.endswith('old_early'))


if __name__ == '__main__':
    if sys.argv[1] == 'one':
        one(sys.argv[2])
    else:
        {'baseline': baseline, 'bounds': bounds, 'step': step, 'lam': lam}[sys.argv[1]]()
