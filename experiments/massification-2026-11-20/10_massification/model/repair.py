"""Income-scaling channel repair — new cell (Council D21/D31; A3 estimator-range rule). Structural change, predeclared.
Repair ON: income-facing participation margin (intake elasticity eta_in + lag_in; progression income-level exponents
m_pri/m_low/m_up/m_ter). Repair OFF = the unrepaired model, retained alongside (R12).
Fit: brief-013 FIT cells only (completion primary/lower/upper, PHL+CHN, observed 1980-2010). Holdout 2011-2024
untouched. Scaling exponents are CHECKS only (never fitted): A3 range containment (within-to-between bounds from
relations/scaling_laws.csv) for >=2 of 3 laws with correct sign for all 3; +/-1 se of A1 as stricter descriptive.
"""
import csv, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pushpull as M
import calibrate as K

BASE_KEYS = list(K.KEYS)
NEW_KEYS = ['eta_in', 'lag_in', 'm_pri', 'm_low', 'm_up', 'm_ter']
KEYS = BASE_KEYS + NEW_KEYS
BOUNDS = dict(K.BOUNDS)
BOUNDS.update({'eta_in': (0.0, 1.5), 'lag_in': (0, 6), 'm_pri': (0.0, 1.5), 'm_low': (0.0, 1.5),
               'm_up': (0.0, 1.5), 'm_ter': (0.0, 1.5)})
# A3 estimator ranges from 10_massification/relations/data/scaling_laws.csv (within-country, between-country)
A3 = {'secondary': dict(within=0.0904, between=0.2154, se_w=0.1238, se_b=0.0349),
      'tertiary': dict(within=0.8482, between=0.5666, se_w=0.1719, se_b=0.0817),
      'completion_low': dict(within=0.2468, between=0.1690, se_w=0.1188, se_b=0.0343)}
A1 = {'secondary': (0.286, 0.045), 'tertiary': (0.776, 0.086)}

OBS = K.load_completion()


def theta_from(z, keys=KEYS, bounds=BOUNDS):
    th = {}
    for i, k in enumerate(keys):
        lo, hi = bounds[k]
        v = lo + z[i] * (hi - lo)
        th[k] = float(round(v)) if k in ('lag_s', 'lag_d', 'lag_in') else float(v)
    return th


def fit_obj(z, rival):
    th = theta_from(z)
    tot, n = 0.0, 0
    for iso in ('PHL', 'CHN'):
        h = M.run(iso, rival=rival, priors=th)
        sim = {k: {x['year']: x[k] for x in h} for k in K.LEVEL_KEYS}
        m, cnt = K.metrics(sim, OBS.get(iso, {}), K.FIT_Y)
        if cnt:
            tot += m; n += 1
    return tot / n if n else 1e6


def fit(rival, seed=3030, maxiter=30, popsize=8):
    from scipy.optimize import differential_evolution
    res = differential_evolution(lambda z: fit_obj(z, rival), bounds=[(0, 1)] * len(KEYS), seed=seed,
                                 maxiter=maxiter, popsize=popsize, tol=1e-4, polish=False, workers=1)
    return theta_from(res.x), float(res.fun)


def exps(iso, rival, th, years=(2011, 2024)):
    h = M.run(iso, rival, priors=th)
    yrs = np.array([x['year'] for x in h]); gdp = np.array([x['gdp'] for x in h])
    w = (yrs >= years[0]) & (yrs <= years[1])
    out = {}
    for key, label in [('ger_lower', 'secondary'), ('ger_tertiary', 'tertiary')]:
        y = np.log(np.array([x[key] for x in h])[w]); x = np.log(gdp[w])
        out[label] = float(np.polyfit(x, y, 1)[0]) if np.std(x) > 1e-12 else float('nan')
    c = np.clip(np.array([x['completion_lower'] for x in h])[w] / 100.0, 1e-4, 1 - 1e-4)
    out['completion_low'] = float(np.polyfit(np.log(gdp[w]), np.log(c / (1 - c)), 1)[0])
    return out


def verdict(e):
    """A3 rule: sign correct for all 3, range containment for >=2 of 3; +/-1se A1 = stricter descriptive only."""
    laws = list(A3)
    signs_ok = sum(1 for k in laws if e[k] > 0)
    contained = {}
    for k in laws:
        lo, hi = sorted((A3[k]['within'], A3[k]['between']))
        contained[k] = bool(lo <= e[k] <= hi)
    n_cont = sum(contained.values())
    a1 = {}
    for k, (v, se) in A1.items():
        a1[k] = bool(abs(e[k] - v) <= se)
    if signs_ok == 3 and n_cont >= 2:
        v = 'PASS'
    elif signs_ok == 3 and n_cont == 1:
        v = 'PARTIAL'
    else:
        v = 'FAIL'
    return dict(verdict=v, signs_ok=signs_ok, n_contained=n_cont, contained=contained, within_1se_A1=a1)


def main():
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calib')
    os.makedirs(outdir, exist_ok=True)
    rivals = ['demand_led', 'education_led', 'complementary']
    rows, ser = [], []
    for rival in rivals:
        th, loss = fit(rival)
        row = dict(rival=rival, fit_loss=loss, theta_json=json.dumps(th))
        for iso in ('PHL', 'CHN'):
            h = M.run(iso, rival, priors=th)
            sim = {k: {x['year']: x[k] for x in h} for k in K.LEVEL_KEYS}
            fr = K.fit_metrics(sim, OBS.get(iso, {}), K.FIT_Y)
            hr = K.fit_metrics(sim, OBS.get(iso, {}), K.HOLD_Y)
            row[f'{iso}_fit_mae'] = float(np.mean([r[4] for r in fr])) if fr else float('nan')
            row[f'{iso}_fit_n'] = len(fr)
            row[f'{iso}_hold_mae'] = float(np.mean([r[4] for r in hr])) if hr else float('nan')
            row[f'{iso}_hold_n'] = len(hr)
        e = exps('PHL', rival, th)
        v = verdict(e)
        row.update({f'exp_{k}': e[k] for k in e})
        row.update({'verdict': v['verdict'], 'signs_ok': v['signs_ok'], 'n_contained': v['n_contained']})
        row['within1se_A1'] = json.dumps(v['within_1se_A1'])
        rows.append(row)
        for k in A3:
            ser.append(dict(rival=rival, law=k, generated=e[k], A3_lo=min(A3[k]['within'], A3[k]['between']),
                            A3_hi=max(A3[k]['within'], A3[k]['between']), contained=v['contained'][k],
                            A1_value=A1.get(k, (float('nan'), float('nan')))[0],
                            A1_se=A1.get(k, (float('nan'), float('nan')))[1],
                            within_1se_A1=v['within_1se_A1'].get(k, None)))
        print(f"{rival}: PHL fit {row['PHL_fit_mae']:.2f}/hold {row['PHL_hold_mae']:.2f}; CHN fit {row['CHN_fit_mae']:.2f}/"
              f"hold {row['CHN_hold_mae']:.2f}; exps sec {e['secondary']:+.3f} ter {e['tertiary']:+.3f} "
              f"comp {e['completion_low']:+.3f} -> {v['verdict']} (signs {v['signs_ok']}/3, contained {v['n_contained']}/3)", flush=True)
    with open(os.path.join(outdir, 'repair_table.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(os.path.join(outdir, 'repair_scaling.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(ser[0])); w.writeheader(); w.writerows(ser)
    print('wrote calib/repair_table.csv, calib/repair_scaling.csv')


if __name__ == '__main__':
    main()
