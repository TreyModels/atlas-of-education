"""Trial functions for the rigor families. Called by research/adapters.py:trial; isolated per process by lab.py.

Each function returns dict(metrics=..., ...). Scalar metrics feed lab.py's REPORT.md; array outputs (reference
tables, forecast errors) are kept in the trial record and read by research/rigor/analyze.py.

Families
  credential_recovery  reference table for mechanism recovery: HC / POS / REL / GATE x observation designs
  shadow_recovery      reference table for mechanism recovery: thin / diversion / favour x field-observation designs
  youth_placebo        placebo-in-time: move the fitted residual step to other months and refit
  youth_rolling        rolling-origin forecasts within the old NBS definition vs naive, seasonal naive and lake null
  fertility_placebo    spurious-regression benchmarks: random-walk null and cross-place covariate swaps
  camchild_validation  (Node) external check of the cash lever against Filmer & Schady (2011), see node_rigor.cjs
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]


# ------------------------------------------------------------------ credential
def credential_recovery(t):
    import numpy as np
    sys.path.insert(0, str(ROOT / 'engine'))
    import relfloor_countries as RC
    import relfloor_gate as G
    s = t['settings']
    cfg = RC.CFG['Cambodia']
    rows, errs, params = [], [], []
    for j in range(s['batch']):
        rng = np.random.default_rng([t['parameter_seed'], j])
        th = G.draw(rng, s['structure'], cfg, smooth_liq=(s['liquidity'] == 'graded'))
        if s['liquidity'] == 'hard':
            th['s_liq'] = 0.0
        summ, err = G.summaries(th, cfg, s['n'], int(t['seed']) + j)
        rows.append([summ[k] for k in G.SUMMARY_NAMES]); errs.append(err)
        params.append({k: float(th[k]) for k in ('b_rel', 'b_pos', 'b_gate', 'prem0', 'gamma', 's_liq', 'mu', 'sig')})
    rows = np.array(rows); errs = np.array(errs)
    metrics = {'share_profile_within_10pts': float(np.mean(errs <= 0.10)),
               'share_profile_within_15pts': float(np.mean(errs <= 0.15)),
               'mean_premium_resp_2030': float(rows[:, G.SUMMARY_NAMES.index('premium_resp_2030')].mean()),
               'mean_gate_resp_2030': float(rows[:, G.SUMMARY_NAMES.index('gate_resp_2030')].mean())}
    return dict(metrics=metrics, table=dict(names=list(G.SUMMARY_NAMES), rows=rows.tolist(), profile_error=errs.tolist(),
                                            params=params),
                evidence_role='synthetic reference table for mechanism recovery; no observed data enter the simulation',
                limitation='gate, access and premium-shock designs are assumed; noise SDs are declared in relfloor_gate.NOISE')


# ------------------------------------------------------------------ shadow education
SHADOW_SIGNATURES = (
    # published targets (corrected observation equation, research/CHANGELOG.md)
    'participation', 'participation_g9', 'participation_g12', 'urban_rural_gap', 'source_own_provider_share',
    'source_other_provider_share', 'teacher_tutor_share',
    # candidate field observations
    'instr_gap_tutoring_teacher',   # regular instruction delivered: classes whose teacher sells to own pupils minus others
    'buy_gap_tutoring_teacher',     # subject purchase rate: same contrast
    'other_gap_tutoring_teacher',   # buying from the parallel-class teacher: same contrast
    'coverage_gap_q5_q1',           # curriculum coverage, richest minus poorest fifth
    'ban_effect_participation', 'ban_effect_class_instruction',          # response to a ban on own-pupil tutoring
    'extra_time_effect_participation',                                     # response to 10 points more class time
)


def _shadow_summary(o):
    return {
        'participation': o['participation'], 'participation_g9': o['participation_g9'],
        'participation_g12': o['participation_g12'],
        'urban_rural_gap': o['participation_urban'] - o['participation_rural'],
        'source_own_provider_share': o['source_own_provider_share'],
        'source_other_provider_share': o['source_other_provider_share'],
        'teacher_tutor_share': o['teacher_tutor_share'],
        'instr_gap_tutoring_teacher': o['instr_tutoring_teacher'] - o['instr_nontutoring_teacher'],
        'buy_gap_tutoring_teacher': o['buy_tutoring_teacher'] - o['buy_nontutoring_teacher'],
        'other_gap_tutoring_teacher': o['other_given_tutoring_teacher'] - o['other_given_nontutoring_teacher'],
        'coverage_gap_q5_q1': o['coverage_q5'] - o['coverage_q1'],
    }


def shadow_recovery(t):
    import math
    import numpy as np
    path = ROOT / 'experiments/shadow-abm/src/tutoring_abm'
    sys.path.insert(0, str(path))
    import model as m
    import calibrate as c
    s = t['settings']
    rows, zmax, conv = [], [], []
    for j in range(s['batch']):
        rng = np.random.default_rng([t['parameter_seed'], j])
        p = m.draw_params(rng, s['variant'])
        seed = int(t['seed']) + j
        w = m.World(p, seed).solve(s['max_sweeps'])
        o = w.outcomes()
        if not o['converged']:
            rows.append([math.nan] * len(SHADOW_SIGNATURES)); zmax.append(math.nan); conv.append(0); continue
        summ = _shadow_summary(o)
        ob = m.World(replace(p, ban_own=True), seed).solve(s['max_sweeps']).outcomes()
        oe = m.World(replace(p, extra_time=0.1), seed).solve(s['max_sweeps']).outcomes()
        ok = ob['converged'] and oe['converged']
        summ['ban_effect_participation'] = ob['participation'] - o['participation'] if ok else math.nan
        summ['ban_effect_class_instruction'] = ob['class_instruction'] - o['class_instruction'] if ok else math.nan
        summ['extra_time_effect_participation'] = oe['participation'] - o['participation'] if ok else math.nan
        rows.append([float(summ[k]) if summ[k] == summ[k] else math.nan for k in SHADOW_SIGNATURES])
        zmax.append(float(max(c.distances(o).values()))); conv.append(int(ok))
    z = np.array(zmax, float)
    metrics = {'converged_share': float(np.mean(conv)),
               'share_within_z3': float(np.nanmean(z <= 3)) if np.isfinite(z).any() else 0.0,
               'share_within_z1': float(np.nanmean(z <= 1)) if np.isfinite(z).any() else 0.0}
    clean = [[None if (isinstance(v, float) and not math.isfinite(v)) else v for v in r] for r in rows]
    return dict(metrics=metrics, table=dict(names=list(SHADOW_SIGNATURES), rows=clean,
                                            max_z=[None if not math.isfinite(v) else v for v in zmax]),
                evidence_role='synthetic reference table for mechanism recovery from prior draws',
                limitation='prior draws rarely match the published patterns; recovery is reported near the data '
                           '(max z <= 3) and over the whole prior separately')


# ------------------------------------------------------------------ China youth unemployment
def _youth_setup():
    sys.path.insert(0, str(ROOT / 'engine'))
    from firms import calibrate_china as K, model as M, data_china as D
    return K, M, D


def _headline_start(K):
    d = json.loads((ROOT / 'engine/firms/results/china_fit.json').read_text())
    p = d['profiles'][d['headline']]['params']
    return [p[name] for name, *_ in K.FREE]


def youth_placebo(t):
    """Refit the full-record model with the residual step placed at another month (placebo in time; cf. Abadie,
    Diamond & Hainmueller 2010). If many placebo months fit as well as August 2021, the data do not single out that
    month and the step should not be read as the Double Reduction policy."""
    import numpy as np
    from scipy.optimize import least_squares
    K, M, D = _youth_setup()
    s = t['settings']
    fixed = dict(sigma_A=5.0)
    if s['date'] is None:
        fixed['dr_drop'] = 0.0
    else:
        fixed['dr_date'] = tuple(s['date'])
    free = [r for r in K.FREE if r[0] not in fixed]
    names = [r[0] for r in free]
    lo = np.array([r[1] for r in free]); hi = np.array([r[2] for r in free])
    head = dict(zip([r[0] for r in K.FREE], _headline_start(K)))
    start = (np.clip([head[n] for n in names], lo, hi) if t['draw'] == 0
             else np.random.default_rng(t['parameter_seed']).uniform(lo, hi))
    window = s['window']
    npairs = len(K.pairs_for(K.run(None, **fixed), window))

    def resid(x):
        try:
            R = K.run(None, **dict(fixed, **dict(zip(names, map(float, x)))))
            r = np.array([mod - ob for *_, ob, mod, _ in K.pairs_for(R, window)])
            return r if np.all(np.isfinite(r)) else np.full(npairs, 50.0)
        except ValueError:
            return np.full(npairs, 50.0)
    fit = least_squares(resid, start, bounds=(lo, hi), diff_step=1e-3, max_nfev=s['max_nfev'])
    R = K.run(None, **dict(fixed, **dict(zip(names, map(float, fit.x)))))
    params = dict(zip(names, map(float, fit.x)))
    metrics = dict(cost=float(fit.cost), mae=K.stats(K.pairs_for(R, window))['mae'],
                   dr_drop=params.get('dr_drop', 0.0), optimizer_success=float(fit.success), nfev=int(fit.nfev),
                   rise_pp=float(K.outcome(R)) if hasattr(K, 'outcome') else None)
    return dict(metrics=metrics, parameters=params, date=s['date'],
                evidence_role='retrospective placebo; all months previously inspected',
                limitation='least-squares cost is not a likelihood; compare dates by cost differences across restarts')


def youth_rolling(t):
    """Fit on old-method months up to the origin, forecast the remaining old-method months (to 2023-06). The definition
    does not change inside the evaluation window. Benchmarks use only information available at the origin."""
    import numpy as np
    from scipy.optimize import least_squares
    K, M, D = _youth_setup()
    sys.path.insert(0, str(ROOT / 'experiments/youth-review'))
    s = t['settings']
    origin = tuple(s['origin'])
    end = (2023, 6)
    obs = {(y, m): D.youth(y, m)[0] for y in range(2018, 2024) for m in range(1, 13)
           if D.youth(y, m) and D.youth(y, m)[1] == 'old' and (y, m) <= end}
    train = sorted(k for k in obs if k <= origin)
    test = sorted(k for k in obs if k > origin)
    fixed = dict(sigma_A=5.0)
    if origin < (2021, 9):
        fixed['dr_drop'] = 0.0          # a forecaster at this origin had no post-step data to fit a step
    free = [r for r in K.FREE if r[0] not in fixed]
    names = [r[0] for r in free]
    lo = np.array([r[1] for r in free]); hi = np.array([r[2] for r in free])
    head = dict(zip([r[0] for r in K.FREE], _headline_start(K)))
    start = (np.clip([head[n] for n in names], lo, hi) if t['draw'] == 0
             else np.random.default_rng(t['parameter_seed']).uniform(lo, hi))

    def series(R):
        return {(y, m): v for y, m, v in zip(R['year'], R['month'], R['rate_old'])}

    def resid(x):
        try:
            S = series(K.run(None, **dict(fixed, **dict(zip(names, map(float, x))))))
            r = np.array([S[k] - obs[k] for k in train])
            return r if np.all(np.isfinite(r)) else np.full(len(train), 50.0)
        except ValueError:
            return np.full(len(train), 50.0)
    fit = least_squares(resid, start, bounds=(lo, hi), diff_step=1e-3, max_nfev=s['max_nfev'])
    S = series(K.run(None, **dict(fixed, **dict(zip(names, map(float, fit.x))))))

    # lake null refit on the same information (old method only, so its method offset is irrelevant)
    import lake_null as L
    def lres(th):
        R = L.simulate(*th)
        Sl = {(y, m): v for y, m, v in zip(R['year'], R['month'], R['rate_old'])}
        r = np.array([Sl[k] - obs[k] for k in train])
        return r if np.all(np.isfinite(r)) else np.full(len(train), 50.0)
    llo = np.array([0.001, 0.0005, 0.05, -5.0]); lhi = np.array([1 - L.A_EXIT - 1e-3, 1 - L.A_EXIT - 1e-3, 1.0, 5.0])
    lbest = None
    for st in [np.array([0.05, 0.02, 0.7, 0.0])] + [np.random.default_rng([t['parameter_seed'], i]).uniform(llo, lhi)
                                                     for i in range(3)]:
        r = least_squares(lres, st, bounds=(llo, lhi), diff_step=1e-3, max_nfev=400)
        if lbest is None or r.cost < lbest.cost:
            lbest = r
    Rl = L.simulate(*lbest.x)
    Sl = {(y, m): v for y, m, v in zip(Rl['year'], Rl['month'], Rl['rate_old'])}

    def months_between(a, b):
        return (b[0] - a[0]) * 12 + (b[1] - a[1])
    last = obs[train[-1]]
    errors = []
    for k in test:
        h = months_between(origin, k)
        prev_year = (k[0] - 1, k[1])
        # seasonal naive must use a month at or before the origin: step back whole years until available
        sn_key = prev_year
        while sn_key > origin:
            sn_key = (sn_key[0] - 1, sn_key[1])
        errors.append(dict(month=list(k), h=h, actual=obs[k], model=S[k] - obs[k], lake=Sl[k] - obs[k],
                           random_walk=last - obs[k], seasonal_naive=(obs.get(sn_key, float('nan')) - obs[k])))
    insample = [obs[k] for k in train]
    e = lambda key: np.array([x[key] for x in errors])
    metrics = dict(n_test=len(errors), train_mae=float(np.mean(np.abs(resid(fit.x)))),
                   mae_model=float(np.mean(np.abs(e('model')))), mae_lake=float(np.mean(np.abs(e('lake')))),
                   mae_random_walk=float(np.mean(np.abs(e('random_walk')))),
                   mae_seasonal_naive=float(np.nanmean(np.abs(e('seasonal_naive')))),
                   optimizer_success=float(fit.success), dr_drop_fixed_zero=float('dr_drop' in fixed))
    return dict(metrics=metrics, errors=errors, insample=insample, origin=list(origin),
                parameters=dict(zip(names, map(float, fit.x))),
                evidence_role='retrospective rolling-origin evaluation; months previously inspected',
                limitation='few origins; overlapping horizons; within-old-definition window ends June 2023')


# ------------------------------------------------------------------ fertility
def fertility_placebo(t):
    """How unusual are the page's levels fits against (a) independent random walks with each covariate's drift and
    volatility (Granger & Newbold 1974) and (b) the same regression run on another place's covariate?"""
    import numpy as np
    from rigor.stats import r2_ols
    s = t['settings']
    page = json.loads((ROOT / 'public/research/fertility/fertility-series.json').read_text())
    with zipfile.ZipFile(ROOT / 'public/research/fertility/fertility-research-full.zip') as z:
        life = json.loads(z.read('fertility_handoff/life_asia.json'))
        panel = json.loads(z.read('fertility_handoff/asia_panel_data.json'))
    years = np.asarray(page['years']); mask = years >= s['start']; years = years[mask]
    places = ('PHL', 'THA', 'KOR', 'JPN', 'HKG', 'CHN')
    tfr = {p: np.asarray(page['places'][p]['obs'], float)[mask] for p in places}
    cov = {'life_expectancy': {p: np.array([life[p]['values'][str(v)] for v in years], float) for p in places},
           'log_gdp': {p: np.log([panel['gdp_' + p]['values'][str(v)] for v in years]) for p in places}}
    rng = np.random.default_rng(t['seed'])
    metrics, details = {}, {}
    for cname, X in cov.items():
        for p in places:
            r2, tt, _ = r2_ols(tfr[p], X[p])
            dx = np.diff(X[p])
            null_r2, null_t = [], []
            for _ in range(s['n_sim']):
                x = X[p][0] + np.concatenate([[0], np.cumsum(rng.normal(dx.mean(), dx.std(ddof=1), dx.size))])
                a, b, _ = r2_ols(tfr[p], x)
                null_r2.append(a); null_t.append(abs(b))
            null_r2 = np.array(null_r2); null_t = np.array(null_t)
            swap = {q: r2_ols(tfr[p], X[q])[0] for q in places if q != p}
            key = f'{p}/{cname}'
            metrics[key + '/r2'] = r2
            metrics[key + '/rw_null_share_r2_ge_obs'] = float(np.mean(null_r2 >= r2))
            metrics[key + '/rw_null_r2_p95'] = float(np.quantile(null_r2, .95))
            metrics[key + '/rw_null_share_abs_t_gt_2'] = float(np.mean(null_t > 2))
            metrics[key + '/swap_max_r2'] = float(max(swap.values()))
            metrics[key + '/swap_share_ge_obs'] = float(np.mean([v >= r2 for v in swap.values()]))
            details[key] = dict(swap_r2=swap)
    return dict(metrics=metrics, details=details,
                evidence_role='exploratory benchmarks for levels fits; all series previously inspected',
                limitation='a random-walk null with Gaussian increments is one benchmark among several; '
                           'it shows what trending alone produces, not that development has no effect')


# ------------------------------------------------------------------ Node families
def node_rigor(t):
    p = subprocess.run(['node', str(ROOT / 'research/rigor/node_rigor.cjs')], input=json.dumps(t),
                       capture_output=True, text=True, cwd=ROOT, check=True)
    return json.loads(p.stdout)


TRIALS = {'credential_recovery': credential_recovery, 'shadow_recovery': shadow_recovery,
          'youth_placebo': youth_placebo, 'youth_rolling': youth_rolling, 'fertility_placebo': fertility_placebo,
          'camchild_validation': node_rigor}
