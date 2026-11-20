"""E21 (new data, user-requested): external enrolment benchmark of the massabm cohort model against
OBSERVED UIS/WDI gross enrolment ratios (data-hunter's gmr_observed_6countries_1970_2024.csv).

Only observed cells are used. Imputed cells are never used as truth; where the observed series has a
gap we simply skip that year (and report the skip in counts). Window 1980-2020.

Model GER is a stock/duration/cohort conversion, declared:
  primary   = enrol_primary   / (N * 6)
  secondary = enrol_secondary / (N * mean_secondary_duration(t))   [4 years pre-K12, 6 after; the
              model's own S['reformed'] flag sets the switch, so this is not tuned to the data]
  tertiary  = enrol_tertiary  / (N * 4)
This is a model-flow benchmark, not a claim that the model is calibrated.
"""
import argparse, csv, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import run_many, write_rows, write_text
from massabm import make_params

DATA = '/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20/04_data/data/gmr_observed_6countries_1970_2024.csv'
WIN = (1980, 2020)
IND = {'ger_primary': ('primary', 6.0), 'ger_secondary': ('secondary', None), 'ger_tertiary': ('tertiary', 4.0)}


def observed():
    out = {}
    for r in csv.DictReader(open(DATA)):
        if r['iso3'] not in ('PHL', 'KOR'):
            continue
        if r['indicator'] not in ('ger_primary', 'ger_secondary', 'ger_tertiary'):
            continue
        y = int(r['year'])
        if not (WIN[0] <= y <= WIN[1]):
            continue
        try:
            v = float(r['value'])
        except (TypeError, ValueError):
            continue
        out.setdefault(r['iso3'], {}).setdefault(r['indicator'], {})[y] = (v, r['source'])
    return out


def model_ger(S, N):
    y = S['year'].astype(int)
    e = S['enrol']
    reform = S['reformed'] if 'reformed' in S else np.zeros(len(y))
    dur_sec = 4.0 + 2.0 * np.clip(reform, 0, 1)
    # observed GER is in PERCENT; the model stock/duration/cohort ratio is a fraction
    return {'ger_primary': 100.0 * e[:, 0] / (N * 6.0),
            'ger_secondary': 100.0 * e[:, 1] / (N * dur_sec),
            'ger_tertiary': 100.0 * e[:, 2] / (N * 4.0)}, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=2)
    ap.add_argument('--N', type=int, default=5000)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    obs = observed()
    jobs = []
    for r in range(a.reps):
        jobs.append((('PHL', 'philippines', r), 'massabm', make_params(seed=31000 + r, N=a.N, preset='philippines')))
        jobs.append((('KOR', 'korea', r), 'massabm', make_params(seed=31000 + r, N=a.N, preset='korea')))
    print(f'E21: {len(jobs)} runs reps={a.reps} N={a.N}', flush=True)
    res, elapsed = run_many(jobs, a.workers)
    wall = time.time() - t0
    bad = [t for t, o in res.items() if isinstance(o, dict) and 'error' in o]
    rows, summ = [], []
    for iso in ('PHL', 'KOR'):
        for ind in ('ger_primary', 'ger_secondary', 'ger_tertiary'):
            mvals = []
            for r in range(a.reps):
                o = res.get((iso, 'philippines' if iso == 'PHL' else 'korea', r))
                if o is None or (isinstance(o, dict) and 'error' in o):
                    continue
                g, y = model_ger(o, a.N)
                mvals.append((g[ind], y))
            if not mvals or ind not in obs.get(iso, {}):
                summ.append(dict(country=iso, indicator=ind, n_obs=0)); continue
            years = sorted(set(obs[iso][ind]) & set(mvals[0][1]))
            if not years:
                summ.append(dict(country=iso, indicator=ind, n_obs=0)); continue
            obs_v = np.array([obs[iso][ind][yy][0] for yy in years])
            mod_v = np.array([np.mean([g[np.where(y == yy)[0][0]] for g, y in mvals]) for yy in years])
            corr = float(np.corrcoef(obs_v, mod_v)[0, 1]) if len(years) > 2 else np.nan
            mae = float(np.mean(np.abs(obs_v - mod_v)))
            bias = float(np.mean(mod_v - obs_v))
            summ.append(dict(country=iso, indicator=ind, n_obs=len(years), years=f'{years[0]}-{years[-1]}',
                             obs_mean=float(obs_v.mean()), model_mean=float(mod_v.mean()),
                             corr=corr, mae_pp=mae, bias_pp=bias,
                             obs_min=float(obs_v.min()), obs_max=float(obs_v.max()),
                             model_min=float(mod_v.min()), model_max=float(mod_v.max())))
            for yy, ov, mv in zip(years, obs_v, mod_v):
                rows.append(dict(country=iso, indicator=ind, year=yy, observed=ov, model=float(mv),
                                 diff=float(mv - ov), obs_source=obs[iso][ind][yy][1]))
    write_rows(os.path.join(a.out, 'e21_series.csv'), ['country', 'indicator', 'year', 'observed', 'model', 'diff', 'obs_source'], [[r[k] for k in ['country', 'indicator', 'year', 'observed', 'model', 'diff', 'obs_source']] for r in rows])
    hdr = ['country', 'indicator', 'n_obs', 'years', 'obs_mean', 'model_mean', 'corr', 'mae_pp', 'bias_pp',
           'obs_min', 'obs_max', 'model_min', 'model_max']
    write_rows(os.path.join(a.out, 'e21_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])
    L = ['E21 EXTERNAL ENROLMENT BENCHMARK vs OBSERVED UIS/WDI GER (new data from data-hunter)',
         f'reps={a.reps} N={a.N} wall={wall:.0f}s ok={len(rows)} series-years; runs failed={len(bad)}',
         'Only OBSERVED cells used; imputed cells never used as truth. Window 1980-2020.',
         'Model GER = model enrolment stock / (N x duration); secondary duration switches 4->6 with the model\'s own',
         'K-12 reform flag (not tuned to the data). This is a flow benchmark, NOT a calibration.', '',
         f'  {"country":7s} {"indicator":14s} {"n":>3s} {"years":>9s} {"obs mean":>8s} {"model mean":>10s} {"corr":>7s} {"MAE pp":>7s} {"bias pp":>8s}']
    for r in summ:
        if not r.get('n_obs'):
            L.append(f'  {r["country"]:7s} {r["indicator"]:14s} no overlapping observed years'); continue
        L.append(f'  {r["country"]:7s} {r["indicator"]:14s} {r["n_obs"]:3d} {r["years"]:>9s} {r["obs_mean"]:8.1f} '
                 f'{r["model_mean"]:10.1f} {r["corr"]:7.3f} {r["mae_pp"]:7.1f} {r["bias_pp"]:+8.1f}')
    L += ['', 'READ: the test is whether the uncalibrated default model reproduces the LEVEL and SHAPE of observed',
          'enrolment. Matching the shape (corr) is weak evidence because both rise; the level (MAE, bias) is the',
          'honest test. The Korea-like preset is a stylised schedule, not a calibrated Korea: a miss there is a',
          'statement about the preset, not about Korea.', '',
          'CAVEAT on data vintage: the observed series come from the data-hunter pull (retrieved 2026-11-20), which',
          'harmonises UIS SDG4 2026-11, UIS EDUNONCORE Feb-2020 and WDI-via-UIS layers; source per point is in',
          'e21_series.csv. Any years where the observed series is absent were skipped, not imputed.']
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='E21', reps=a.reps, N=a.N, wall=wall, status='external benchmark; observed cells only'),
              open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'wall={wall:.0f}s')


if __name__ == '__main__':
    main()
