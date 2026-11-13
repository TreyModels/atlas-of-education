"""Required-demand inversion (TODO §5 P1; also the graduate-vacancy failure).

Every strict specification expects the 2022 spike to fade (forecast_strict.md, wage_anchor.md, tilly_strict.md). Here
the question is turned round: keep the parameters fitted to data as of Dec 2022, and ask what demand path after 2022
would make the model reproduce 2023-26 youth unemployment. Then check that path against evidence the inversion never
saw. Two versions:
  graduate   a multiplier on graduate-job demand only (one value per half-year, 2023 H1 .. 2026 H2), aggregate
             demand held at its prespecified rule (mean of 2022);
  aggregate  a multiplier on aggregate demand A_t instead (affects all youth and, in the model's own logic, adults).
Checks (none used in the inversion):
  1. graduate postings, H1 2025 vs H1 2024: observed -22% (Caixin, 19 Sep 2025, job-board data);
  2. adult labour market: the model maps A_t to adult unemployment through free entry; the observed overall urban
     rate stayed at 5.0-5.4% in 2023-26, so a large fall in aggregate A_t is contradicted;
  3. graduate relative starting wages, classes 2022-23 (MyCOS / NBS), held out;
  4. plausibility of the size: the required graduate-demand fall, compared with what the graduate postings show.

Run from engine/:  python -m firms.demand_inversion  -> firms/results/demand_inversion.{json,md}
"""
import json, math, os, sys
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firms import model as M, data_china as D, calibrate_china as C, forecast_strict as F, wage_anchor as W

OUT = F.OUT
HALVES = [(y, h) for y in range(2023, 2027) for h in (1, 2)]


def path_fn(mult):
    """Piecewise-constant multiplier by half-year from Jan 2023, 1 before."""
    d = dict(zip(HALVES, mult))
    return lambda y, m: d.get((y, 1 if m <= 6 else 2), 1.0) if y >= 2023 else 1.0


def run(theta, mult=None, kind='graduate', over=None):
    kw = dict(C.REF); kw.update({n: float(v) for (n, *_), v in zip(C.FREE, theta)}); kw.update(over or {})
    if mult is not None and kind == 'graduate':
        kw['grad_shift'] = path_fn(mult)
    V = F.Vintage()
    ym = M.YouthMarket(V, **kw)
    ym.A = F.fill_demand(ym.A, F.CUTOFF, 'last12')
    if mult is not None and kind == 'aggregate':
        f = path_fn(mult)
        ym.A = {k: v * f(*k) for k, v in ym.A.items()}
    return ym.run()


def targets(R):
    return F.obs_pairs(R, 2023, 2023, 'old') + F.obs_pairs(R, 2023, 2026, 'new')


def resid(logm, theta, kind):
    R = run(theta, np.exp(logm), kind)
    r = [mod - ob for *_, ob, mod, _ in targets(R)]
    smooth = list(0.5 * np.diff(logm) * 10)            # light penalty on half-year jumps (10% jump = 0.5 pt)
    return np.array(r + smooth) if all(map(math.isfinite, r)) else np.full(len(r) + len(smooth), 50.0)


def invert(theta, kind):
    lo, hi = (math.log(0.3), math.log(2.0)) if kind == 'graduate' else (math.log(0.7), math.log(1.3))
    best = None
    for s in (0.0, -0.2, 0.15):
        x0 = np.full(len(HALVES), float(np.clip(s, lo + 1e-3, hi - 1e-3)))
        r = least_squares(resid, x0, bounds=([lo] * len(HALVES), [hi] * len(HALVES)), diff_step=1e-3,
                          max_nfev=200, args=(theta, kind))
        if best is None or r.cost < best.cost:
            best = r
    return np.exp(best.x)


def adult_rate_implied(A_ratio, theta):
    """Adult unemployment the model's own free-entry inversion implies for a given A/A_ref (inverse of demand_index)."""
    p = dict(M.DEFAULTS); p.update({n: float(v) for (n, *_), v in zip(C.FREE, theta)})
    s_a, a = 0.012, p['a']
    A, adult = M.demand_index(p, F.Vintage())
    ref = np.mean([v for k, v in adult.items() if k[0] in (2018, 2019)])
    q = lambda u: 1 - math.exp(-M.urn_x_from_f(s_a * (1 - u) / u, a))
    target = q(ref) * p['m_a'] / max(A_ratio - 1 + p['m_a'], 1e-9)       # A = 1 - m_a + m_a q_ref / q(u)
    lo_, hi_ = 0.005, 0.5
    for _ in range(100):
        mid = 0.5 * (lo_ + hi_)
        if q(mid) > target:      # q rises with u (more searchers per vacancy fill faster)
            hi_ = mid
        else:
            lo_ = mid
    return 100 * 0.5 * (lo_ + hi_)


def main():
    fs = json.load(open(os.path.join(OUT, 'forecast_strict.json')))
    theta = [fs['params'][n] for n, *_ in C.FREE]
    over = dict(sigma_A=5.0)
    base = run(theta)
    res = dict(halves=[f"{y} H{h}" for y, h in HALVES], naive=F.score(f=F.naive('same_month_2022')))
    for kind in ('graduate', 'aggregate'):
        mult = invert(theta, kind)
        R = run(theta, mult, kind)
        fit = C.stats(targets(R))
        vg = C.vg_check(R)
        wp = W.model_wage_path(R, W.KNOWN + W.TEST); wo = W.observed_path(W.KNOWN + W.TEST)
        seas = {}
        for y_, m_, ob_, md_, _ in targets(R):
            seas.setdefault(m_, []).append(md_ - ob_)
        entry = dict(mult=list(map(float, mult)), fit=fit, vg_2025H1_pct=vg,
                     seasonal_error={m_: float(np.mean(v)) for m_, v in sorted(seas.items())},
                     wage_err_test={y: wp[y] - wo[y] for y in W.TEST},
                     V_g_index={f"{y}": C.window_mean(R, 'V_g', (y, 1), (y, 12)) / C.window_mean(base, 'V_g', (2022, 1), (2022, 12))
                                for y in range(2022, 2027)})
        if kind == 'aggregate':
            A22 = float(np.mean([v for k, v in M.demand_index(dict(M.DEFAULTS, **{n: float(v) for (n, *_), v in zip(C.FREE, theta)}), F.Vintage())[0].items() if k[0] == 2022]))
            entry['implied_adult_rate'] = {lab: adult_rate_implied(A22 * m_, theta) for lab, m_ in zip(res['halves'], mult)}
            entry['implied_adult_rate_at_2022_mean'] = adult_rate_implied(A22, theta)
        res[kind] = entry
    res['baseline_vg_2025H1_pct'] = C.vg_check(base)
    obs_urban = {y: float(np.mean([D.urban(y, m)[0] for m in range(1, 13) if D.urban(y, m)])) for y in range(2022, 2027)}
    res['observed_urban_rate'] = obs_urban
    json.dump(res, open(os.path.join(OUT, 'demand_inversion.json'), 'w'), indent=1)
    report(res)


def report(res):
    g, a = res['graduate'], res['aggregate']
    L = ['# Required-demand inversion', '',
         'Generated by `python -m firms.demand_inversion`. Parameters from the strict fit (data as of Dec 2022). '
         'Half-year demand multipliers after 2022 are solved so the model reproduces 2023-26 youth unemployment, '
         'then checked against evidence the inversion did not use.', '',
         '| Half-year | Graduate-only demand needed | Aggregate demand needed |', '|---|---:|---:|']
    L += [f"| {h} | {x:.2f} | {y:.2f} |" for h, x, y in zip(res['halves'], g['mult'], a['mult'])]
    L += ['', 'Multipliers are relative to the forecast rule (2022 demand held flat). 1.00 = no change.', '',
          '| Check | Graduate-only | Aggregate | Observed |', '|---|---:|---:|---:|',
          f"| Youth unemployment 2023-26 reproduced (MAE, pts) | {g['fit']['mae']:.2f} | {a['fit']['mae']:.2f} | naive {res['naive']['new_verified']['mae']:.2f} |",
          f"| Graduate postings, H1 2025 vs H1 2024 | {g['vg_2025H1_pct']:+.0f}% | {a['vg_2025H1_pct']:+.0f}% | -22% |",
          f"| Relative starting wage error, class 2022 / 2023 (log pts) | {g['wage_err_test'][2022]:+.3f} / {g['wage_err_test'][2023]:+.3f} | {a['wage_err_test'][2022]:+.3f} / {a['wage_err_test'][2023]:+.3f} | 0 |",
          f"| Graduate vacancies 2025 vs 2022 (index) | {g['V_g_index']['2025']:.2f} | {a['V_g_index']['2025']:.2f} | |",
          '', f"Baseline strict forecast (no inversion) predicts graduate postings {res['baseline_vg_2025H1_pct']:+.0f}% in H1 2025.", '',
          '**Adult labour market implied by the aggregate path** (model\'s own free-entry mapping; the observed overall urban rate '
          'includes youth, so it is an upper bound on the adult rate):', '',
          '| Half-year | Adult unemployment implied (%) |', '|---|---:|']
    L += [f"| {h} | {v:.1f} |" for h, v in a['implied_adult_rate'].items()]
    L += ['', f"At 2022 demand the same mapping gives {a['implied_adult_rate_at_2022_mean']:.1f}%. Observed overall urban rate: " +
          ', '.join(f"{y} {v:.1f}%" for y, v in res['observed_urban_rate'].items()) + '.']
    L += ['', '**Error left after the graduate inversion, by calendar month (model minus observed, pts):** ' +
          ', '.join(f"{m_} {v:+.1f}" for m_, v in g['seasonal_error'].items()) + '.', '',
          '## What this establishes', '',
          '1. **A demand story is needed, but it is graduate-specific.** Matching 2023-26 needs graduate-job demand '
          f"about {100 * (1 - g['mult'][0]):.0f}% below the 2022 rule in 2023, falling to {100 * (1 - min(g['mult'])):.0f}% below by "
          '2025-26. The aggregate version needs economy-wide demand 4-8% lower, which through the model\'s own '
          'adult free-entry condition implies adult unemployment rising towards 6%. The observed overall urban rate, '
          'which bounds the adult rate from above, stayed at 5.1-5.2%. The aggregate story is contradicted.',
          '2. **The vacancy failure is explained, not fixed.** In this model vacancies are posted in proportion to '
          'searchers (free entry), so more unemployed graduates mean more postings. A graduate-demand path that matches '
          'unemployment gives postings ' + f"{g['vg_2025H1_pct']:+.0f}%" + ' in H1 2025, against -22% observed. One demand series '
          'cannot fit both, so either job-board postings are not the model\'s vacancies (coverage, platform shifts), or '
          'matching efficiency fell, or more graduates stopped searching (a NEET margin). Each is testable.',
          '3. **Even with demand free, the model loses to naive** (MAE about 2, against 1.61), because of seasonality, not '
          'level. Under the new NBS definition the model overshoots the July graduation jump by about 4 pts and '
          'undershoots spring by 2-3 pts. Graduation-season entry (`july_g`, student search `zeta`) was fitted to '
          'old-method data, where searching students were counted. The new-method seasonal shape is a separate '
          'calibration problem from the demand question.',
          '4. **Wages:** the graduate path leaves held-out 2022-23 starting wages about 10 log points too high. Lower '
          'demand should cut graduate pay, but the model\'s wages respond too little.']
    open(os.path.join(OUT, 'demand_inversion.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
