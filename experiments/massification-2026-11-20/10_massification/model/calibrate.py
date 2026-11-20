"""Calibration + rival comparison for the push-pull cohort-flow model (task-37), under Council brief 013.

Declared design (PREDECLARATION_AMENDMENT_013.md):
- FIT series: completion primary/lower/upper, PHL 1980-2010 (observed target rows only; status=='target').
- HOLDOUT PERIOD: 2011-2024 (same series, no refit).
- HOLDOUT COUNTRY: KHM (all observed years; never fitted).
- Check-only: sector shares (ECONOMY_SERIES, 1995-2024) and GER/transition; never fitted.
- Rivals: demand_led (e_s=0), education_led (e_d=0), complementary; each fitted on the SAME fit window.
- Naive benchmarks: persistence, linear trend. Tolerances from brief 013 §3.
- Nothing imputed; missing years skipped and counted.
"""
import csv, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20/10_massification/model')
import pushpull as M

ROOT = '/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20'
FLOW = os.path.join(ROOT, '04_data', 'TARGETS_FLOW.csv')
ECON = os.path.join(ROOT, '04_data', 'ECONOMY_SERIES.csv')
IND = {'primary completion rate': 'completion_primary', 'lower-secondary completion rate': 'completion_lower',
       'upper-secondary completion rate': 'completion_upper'}
FIT_Y = (1980, 2010); HOLD_Y = (2011, 2024)
LEVEL_KEYS = list(IND.values())
KEYS = ['p_pri0', 'p_low0', 'p_up0', 'g_pri', 'g_low', 'g_up', 'u_pri', 'u_low', 'u_up',
        'e_s', 'e_d', 'lag_s', 'lag_d', 'g0']
BOUNDS = {'p_pri0': (0.5, 0.99), 'p_low0': (0.3, 0.98), 'p_up0': (0.2, 0.97),
          'g_pri': (0.0, 0.25), 'g_low': (0.0, 0.3), 'g_up': (0.0, 0.3),
          'u_pri': (0.0, 0.2), 'u_low': (0.0, 0.2), 'u_up': (0.0, 0.2),
          'e_s': (0.0, 0.6), 'e_d': (0.0, 0.6), 'lag_s': (1, 6), 'lag_d': (0, 3), 'g0': (0.005, 0.045)}


def load_completion():
    out = {}
    for r in csv.DictReader(open(FLOW)):
        if r['status'] != 'target' or r['indicator'] not in IND or not r['value']:
            continue
        try:
            y = int(r['year']); v = float(r['value'])
        except (TypeError, ValueError):
            continue
        out.setdefault(r['iso3'], {}).setdefault(IND[r['indicator']], {})[y] = v
    return out


def load_sector():
    out = {}
    for r in csv.DictReader(open(ECON)):
        if r['indicator'] not in ('Employment in agriculture (% of total employment)',
                                  'Employment in industry (% of total employment)',
                                  'Employment in services (% of total employment)'):
            continue
        try:
            out.setdefault(r['iso3'], {}).setdefault(r['indicator'], {})[int(r['year'])] = float(r['value'])
        except (TypeError, ValueError):
            continue
    return out


def simulate(iso, rival, theta):
    return M.run(iso, rival=rival, priors=theta)


def series_from(hist, key):
    return {h['year']: h[key] for h in hist}


def metrics(sim, obs, years):
    """MAE/corr over observed years in window; returns dict and n."""
    errs = []
    for k in LEVEL_KEYS:
        so, sobs = sim[k], obs.get(k, {})
        for y in sobs:
            if years[0] <= y <= years[1]:
                errs.append(sim_key_err(so, sobs, y))
    errs = [e for e in errs if e is not None]
    return float(np.mean(errs)) if errs else float('nan'), len(errs)


def sim_key_err(sim_series, obs_series, y):
    if y not in obs_series or y not in sim_series:
        return None
    return abs(sim_series[y] - obs_series[y])


def fit_metrics(sim, obs, years):
    rows = []
    for k in LEVEL_KEYS:
        so, sobs = sim[k], obs.get(k, {})
        for y in sorted(sobs):
            if years[0] <= y <= years[1] and y in so:
                rows.append((k, y, so[y], sobs[y], abs(so[y] - sobs[y])))
    return rows


def corr_of(sim, obs, years):
    xs, ys = [], []
    for k in LEVEL_KEYS:
        for y in sorted(obs.get(k, {})):
            if years[0] <= y <= years[1] and y in sim[k]:
                xs.append(sim[k][y]); ys.append(obs[k][y])
    if len(xs) < 3:
        return float('nan')
    return float(np.corrcoef(xs, ys)[0, 1])


def naive_benchmarks(obs, fit_y, hold_y):
    """Persistence and linear-trend benchmarks on the same holdout years/series."""
    out = {'persistence': [], 'linear_trend': []}
    for k in LEVEL_KEYS:
        so = obs.get(k, {})
        fitpts = [(y, so[y]) for y in sorted(so) if fit_y[0] <= y <= fit_y[1]]
        holdpts = [(y, so[y]) for y in sorted(so) if hold_y[0] <= y <= hold_y[1]]
        if not fitpts or not holdpts:
            continue
        last = fitpts[-1][1]
        for y, v in holdpts:
            out['persistence'].append(abs(last - v))
        if len(fitpts) >= 2:
            xs = np.array([p[0] for p in fitpts], float); yy = np.array([p[1] for p in fitpts], float)
            b, a = np.polyfit(xs, yy, 1)
            for y, v in holdpts:
                out['linear_trend'].append(abs(a + b * y - v))
    return {k: (float(np.mean(v)) if v else float('nan'), len(v)) for k, v in out.items()}


def objective(z, iso, rival):
    theta = {k: (float(round(BOUNDS[k][0] + z[i] * (BOUNDS[k][1] - BOUNDS[k][0])) if k in ('lag_s', 'lag_d')
                 else BOUNDS[k][0] + z[i] * (BOUNDS[k][1] - BOUNDS[k][0]))) for i, k in enumerate(KEYS)}
    h = simulate(iso, rival, theta)
    sim = {k: series_from(h, k) for k in LEVEL_KEYS}
    m, n = metrics(sim, OBS.get(iso, {}), FIT_Y)
    return m if n > 0 else 1e6


OBS = None


def objective_pool(z, rival):
    """Pooled PHL+CHN objective on the brief-013 FIT window (equal weight per country)."""
    tot, n = 0.0, 0
    for iso in ('PHL', 'CHN'):
        try:
            m = objective(z, iso, rival)
        except Exception:
            return 1e6
        if np.isfinite(m):
            tot += m; n += 1
    return tot / n if n else 1e6


def fit_pool(rival, seed=2027, maxiter=40, popsize=10):
    from scipy.optimize import differential_evolution
    def obj(z):
        return objective_pool(z, rival)
    res = differential_evolution(obj, bounds=[(0, 1)] * len(KEYS), seed=seed, maxiter=maxiter,
                                 popsize=popsize, tol=1e-4, polish=False, workers=1)
    theta = {k: (float(round(BOUNDS[k][0] + res.x[i] * (BOUNDS[k][1] - BOUNDS[k][0])) if k in ('lag_s', 'lag_d')
                  else BOUNDS[k][0] + res.x[i] * (BOUNDS[k][1] - BOUNDS[k][0]))) for i, k in enumerate(KEYS)}
    return theta, float(res.fun)


def fit_phl(rival, seed=2026, maxiter=60, popsize=12):
    from scipy.optimize import differential_evolution
    rng = np.random.default_rng(seed)
    def obj(z):
        try:
            return objective(z, 'PHL', rival)
        except Exception:
            return 1e6
    res = differential_evolution(obj, bounds=[(0, 1)] * len(KEYS), seed=seed, maxiter=maxiter,
                                 popsize=popsize, tol=1e-4, polish=False, workers=1)
    theta = {k: (float(round(BOUNDS[k][0] + res.x[i] * (BOUNDS[k][1] - BOUNDS[k][0])) if k in ('lag_s', 'lag_d')
                  else BOUNDS[k][0] + res.x[i] * (BOUNDS[k][1] - BOUNDS[k][0]))) for i, k in enumerate(KEYS)}
    return theta, float(res.fun)


def evaluate(iso, rival, theta, with_sector=True):
    h = simulate(iso, rival, theta)
    sim = {k: series_from(h, k) for k in LEVEL_KEYS}
    out = dict(iso=iso, rival=rival)
    fr = fit_metrics(sim, OBS.get(iso, {}), FIT_Y)
    hr = fit_metrics(sim, OBS.get(iso, {}), HOLD_Y)
    out['fit_mae'] = float(np.mean([r[4] for r in fr])) if fr else float('nan')
    out['fit_n'] = len(fr)
    # restrict holdout evaluation to the fit country only; KHM is handled by the caller
    out['hold_mae'] = float(np.mean([r[4] for r in hr])) if hr else float('nan')
    out['hold_n'] = len(hr)
    out['fit_corr'] = corr_of(sim, OBS.get(iso, {}), FIT_Y)
    out['hold_corr'] = corr_of(sim, OBS.get(iso, {}), HOLD_Y)
    nb = naive_benchmarks(OBS.get(iso, {}), FIT_Y, HOLD_Y)
    out['naive_persistence'] = nb['persistence'][0]
    out['naive_trend'] = nb['linear_trend'][0]
    out['beats_persistence'] = bool(np.isfinite(out['hold_mae']) and np.isfinite(out['naive_persistence'])
                                    and out['hold_mae'] < out['naive_persistence'])
    out['beats_trend'] = bool(np.isfinite(out['hold_mae']) and np.isfinite(out['naive_trend'])
                              and out['hold_mae'] < out['naive_trend'])
    if with_sector:
        sec = load_sector().get(iso, {})
        sim_sec = {h['year']: h for h in h}
        errs = []
        for ind, key in [('Employment in agriculture (% of total employment)', 'agri'),
                         ('Employment in industry (% of total employment)', 'industry'),
                         ('Employment in services (% of total employment)', 'services')]:
            for y, v in sec.get(ind, {}).items():
                if 1995 <= y <= 2024 and y in sim_sec:
                    errs.append(abs(100 * sim_sec[y][key] - v))
        out['sector_check_mae'] = float(np.mean(errs)) if errs else float('nan')
        out['sector_check_n'] = len(errs)
    out['theta'] = theta
    return out


def main():
    global OBS
    OBS = load_completion()
    mode = sys.argv[1] if len(sys.argv) > 1 else '--phl'
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calib')
    os.makedirs(outdir, exist_ok=True)
    rivals = ['demand_led', 'education_led', 'complementary']
    results = []
    if mode in ('--phl', '--all'):
        for rival in rivals:
            theta, loss = fit_phl(rival)
            r = evaluate('PHL', rival, theta)
            r['fit_loss'] = loss
            results.append(r)
            print(f"PHL {rival}: fit MAE {r['fit_mae']:.2f} pp (n={r['fit_n']}), hold MAE {r['hold_mae']:.2f} pp "
                  f"(n={r['hold_n']}), naive persistence {r['naive_persistence']:.2f}, trend {r['naive_trend']:.2f}, "
                  f"sector check {r.get('sector_check_mae', float('nan')):.2f} pp")
    if mode in ('--phl_chn', '--all'):
        for rival in rivals:
            theta, loss = fit_pool(rival)
            for iso in ('PHL', 'CHN'):
                r = evaluate(iso, rival, theta)
                r['role'] = 'fit+holdout-period'
                r['fit_loss'] = loss
                r['theta_note'] = 'pooled PHL+CHN fit on brief-013 FIT window'
                results.append(r)
                print(f"{iso} {rival}: fit MAE {r['fit_mae']:.2f} pp (n={r['fit_n']}), hold MAE {r['hold_mae']:.2f} pp "
                      f"(n={r['hold_n']}), naive persistence {r['naive_persistence']:.2f}, trend {r['naive_trend']:.2f}, "
                      f"sector check {r.get('sector_check_mae', float('nan')):.2f} pp")
            # KHM held-out country: pooled theta, never fitted on KHM
            h = simulate('KHM', rival, theta)
            sim = {k: series_from(h, k) for k in LEVEL_KEYS}
            fr = fit_metrics(sim, OBS.get('KHM', {}), (1980, 2024))
            hr = fit_metrics(sim, OBS.get('KHM', {}), HOLD_Y)
            nb = naive_benchmarks(OBS.get('KHM', {}), FIT_Y, HOLD_Y)
            r = dict(iso='KHM', rival=rival, role='HOLDOUT COUNTRY (never fitted)',
                     hold_mae=float(np.mean([x[4] for x in hr])) if hr else float('nan'), hold_n=len(hr),
                     fit_mae=float(np.mean([x[4] for x in fr])) if fr else float('nan'), fit_n=len(fr),
                     naive_persistence=nb['persistence'][0], naive_trend=nb['linear_trend'][0],
                     beats_persistence=(np.mean([x[4] for x in hr]) < nb['persistence'][0]) if hr else None,
                     beats_trend=(np.mean([x[4] for x in hr]) < nb['linear_trend'][0]) if hr else None,
                     sector_check_mae=float('nan'), sector_check_n=0, theta=theta)
            results.append(r)
            print(f"KHM (held-out country) {rival}: all-years MAE {r['fit_mae']:.2f} pp (n={r['fit_n']}), "
                  f"2011-2024 MAE {r['hold_mae']:.2f} pp (n={r['hold_n']}), naive {nb['persistence'][0]:.2f}/{nb['linear_trend'][0]:.2f}")
    if results:
        keys = sorted({k for r in results for k in r if k != 'theta'})
        with open(os.path.join(outdir, 'calibration_table.csv'), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=keys + ['theta_json']); w.writeheader()
            for r in results:
                row = {k: r.get(k, '') for k in keys}
                row['theta_json'] = json.dumps(r.get('theta', {}))
                w.writerow(row)
        print('wrote', os.path.join(outdir, 'calibration_table.csv'))


if __name__ == '__main__':
    main()
