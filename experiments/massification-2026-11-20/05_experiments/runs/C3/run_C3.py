"""C3: Philippines calibration of massabm to OBSERVED-only GER targets (1980-2020).
CALIBRATION, not validation: same targets are used to fit and to report residuals."""
import argparse, csv, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import write_rows, write_text
from massabm import make_params, run_model

DATA = '/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20/04_data/data/gmr_observed_6countries_1970_2024.csv'
LEVELS = ['ger_primary', 'ger_secondary', 'ger_tertiary']
BOUNDS = {  # declared in PRE_DECLARATIONS_C.md
    'cost_col': (0.3, 1.0), 'cost_shs': (0.02, 0.15), 'bar_college': (-1.8, 0.2),
    'bar_basic': (-2.4, -1.2), 'apex_mult': (0.5, 2.0), 'hc_school': (0.0, 0.10)}
KEYS = list(BOUNDS)


def observed():
    out = {}
    for r in csv.DictReader(open(DATA)):
        if r['iso3'] != 'PHL' or r['indicator'] not in LEVELS:
            continue
        y = int(r['year'])
        if not (1980 <= y <= 2020):
            continue
        try:
            out.setdefault(r['indicator'], {})[y] = float(r['value'])
        except (TypeError, ValueError):
            pass
    return out


def model_ger(S, N):
    y = S['year'].astype(int)
    e = S['enrol']
    ref = S['reformed'] if 'reformed' in S else np.zeros(len(y))
    dur = 4.0 + 2.0 * np.clip(ref, 0, 1)
    return {'ger_primary': 100.0 * e[:, 0] / (N * 6.0),
            'ger_secondary': 100.0 * e[:, 1] / (N * dur),
            'ger_tertiary': 100.0 * e[:, 2] / (N * 4.0)}, y


def params_from(z, N, seed):
    d = {k: BOUNDS[k][0] + z[k] * (BOUNDS[k][1] - BOUNDS[k][0]) for k in KEYS}
    from massabm.params import DEFAULTS
    ap = [(yr, v * d['apex_mult']) for yr, v in DEFAULTS['apex_path']]
    return make_params(seed=seed, N=N, cost_col=d['cost_col'], cost_shs=d['cost_shs'],
                       bar_college=d['bar_college'], bar_basic=d['bar_basic'],
                       apex_path=ap, hc_school=d['hc_school'])


def _common(mod, y, obs, lv):
    myrs = dict(zip(np.asarray(y).astype(int).tolist(), np.asarray(mod[lv]).tolist()))
    return sorted(set(myrs) & set(obs[lv])), myrs


def loss(mod, y, obs):
    tot, n = 0.0, 0
    for lv in LEVELS:
        yrs, myrs = _common(mod, y, obs, lv)
        if not yrs:
            continue
        m = np.array([myrs[yy] for yy in yrs]); o = np.array([obs[lv][yy] for yy in yrs])
        tot += float(np.mean((m - o) ** 2)); n += 1
    return tot / max(n, 1)


_Z = None; _OBS = None; _N = 2000


def _one(arg):
    i, Z, obs, N = arg
    try:
        p = params_from({k: Z[k][i] for k in KEYS}, N, 32000)
        g, y = model_ger(run_model(p), N)
        return i, loss(g, y, obs)
    except Exception as e:
        return i, float('nan')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--draws', type=int, default=96)
    ap.add_argument('--best', type=int, default=8)
    ap.add_argument('--N', type=int, default=2000)
    ap.add_argument('--Nfine', type=int, default=4000)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    obs = observed()
    rng = np.random.default_rng(32000)
    # Latin hypercube over the six parameters
    u = (rng.permuted(np.tile(np.arange(a.draws), (len(KEYS), 1)), axis=1).T + rng.random((a.draws, len(KEYS)))) / a.draws
    Z = {k: u[:, i] for i, k in enumerate(KEYS)}
    scored = []
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=2) as ex:
        for i, l in ex.map(_one, [(i, Z, obs, a.N) for i in range(a.draws)]):
            scored.append((l, i))
    scored = [s for s in scored if np.isfinite(s[0])]
    scored.sort()
    print(f'search done: {len(scored)} ok, best loss {scored[0][0]:.2f}, wall {time.time() - t0:.0f}s', flush=True)
    fine = []
    for l, i in scored[:a.best]:
        p = params_from({k: Z[k][i] for k in KEYS}, a.Nfine, 32000)
        S = run_model(p)
        g, y = model_ger(S, a.Nfine)
        fine.append((loss(g, y, obs), i, g, y))
    fine.sort(key=lambda x: x[0])
    best_loss, best_i, g, y = fine[0]
    z = {k: Z[k][best_i] for k in KEYS}
    fitted = {k: BOUNDS[k][0] + z[k] * (BOUNDS[k][1] - BOUNDS[k][0]) for k in KEYS}
    # residuals
    res = []
    for lv in LEVELS:
        yrs, myrs = _common(g, y, obs, lv)
        m = np.array([myrs[yy] for yy in yrs]); o = np.array([obs[lv][yy] for yy in yrs])
        res.append(dict(level=lv, n=len(yrs), obs_mean=float(o.mean()), model_mean=float(m.mean()),
                        mae=float(np.mean(np.abs(m - o))), bias=float(np.mean(m - o)),
                        corr=float(np.corrcoef(o, m)[0, 1]) if len(yrs) > 2 else np.nan,
                        obs_min=float(o.min()), obs_max=float(o.max())))
        for yy, oo, mm in zip(yrs, o, m):
            res.append(dict(level=lv + '_series', n=yy, obs_mean=oo, model_mean=mm, mae=abs(mm - oo),
                            bias=mm - oo, corr=np.nan, obs_min=np.nan, obs_max=np.nan))
    # pre-fit (default) residuals at the same N for comparison
    S0 = run_model(make_params(seed=32000, N=a.Nfine))
    g0, y0 = model_ger(S0, a.Nfine)
    pre = []
    for lv in LEVELS:
        yrs, myrs = _common(g0, y0, obs, lv)
        m = np.array([myrs[yy] for yy in yrs]); o = np.array([obs[lv][yy] for yy in yrs])
        pre.append(dict(level=lv, mae=float(np.mean(np.abs(m - o))), bias=float(np.mean(m - o)),
                        corr=float(np.corrcoef(o, m)[0, 1])))
    write_rows(os.path.join(a.out, 'c3_residuals.csv'), ['level', 'n', 'obs_mean', 'model_mean', 'mae', 'bias', 'corr', 'obs_min', 'obs_max'],
               [[r[k] for k in ['level', 'n', 'obs_mean', 'model_mean', 'mae', 'bias', 'corr', 'obs_min', 'obs_max']] for r in res])
    write_rows(os.path.join(a.out, 'c3_search.csv'), ['rank', 'loss', 'z'] + KEYS,
               [[j, l, '', *[round(z[k], 3) for k in KEYS]] for j, (l, i) in enumerate(scored[:20])])
    L = ['C3 PHILIPPINES CALIBRATION TO OBSERVED-ONLY GER (calibration, NOT validation)',
         f'draws={a.draws} at N={a.N}, best {a.best} re-evaluated at N={a.Nfine}; wall={time.time() - t0:.0f}s',
         'Data: 04_data/data/gmr_observed_6countries_1970_2024.csv, PHL observed cells only (imputed never used).',
         'Same targets used for fitting and for residuals; no holdout claim.', '',
         'FITTED PARAMETERS:', '  ' + '  '.join(f'{k}={fitted[k]:.3f}' for k in KEYS),
         f'  search-loss (mean squared pp over levels) {best_loss:.1f}', '',
         'PRE-FIT (defaults) vs POST-FIT residuals per level:',
         f'  {"level":14s} {"MAE pre":>8s} {"MAE post":>9s} {"bias pre":>9s} {"bias post":>10s} {"corr pre":>9s} {"corr post":>10s} {"obs mean":>9s} {"model mean":>10s}']
    for r, pr in zip([x for x in res if x['level'] in LEVELS], pre):
        L.append(f'  {r["level"]:14s} {pr["mae"]:8.1f} {r["mae"]:9.1f} {pr["bias"]:+9.1f} {r["bias"]:+10.1f} '
                 f'{pr["corr"]:9.3f} {r["corr"]:10.3f} {r["obs_mean"]:9.1f} {r["model_mean"]:10.1f}')
    L += ['', 'DECISION (predeclared): a level "succeeds" if post-fit MAE < 5 pp and |bias| < 5 pp.']
    for r in [x for x in res if x['level'] in LEVELS]:
        ok = r['mae'] < 5 and abs(r['bias']) < 5
        L.append(f'  {r["level"]:14s} {"FITS" if ok else "UNFIXABLE MISS within these bounds"} '
                 f'(MAE {r["mae"]:.1f} pp, bias {r["bias"]:+.1f} pp, corr {r["corr"]:+.3f})')
    L += ['', 'CAVEAT: the fit is to three aggregate GER series; it is not a structural estimate and cannot identify',
          'mechanisms. A good fit does not validate the model (see 02_modeling_standards.md, quality control 6).']
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='C3', draws=a.draws, N=a.N, Nfine=a.Nfine, best_loss=best_loss,
                   fitted=fitted, wall=time.time() - t0, status='calibration, not validation'),
              open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print('done', time.time() - t0)


if __name__ == '__main__':
    main()
