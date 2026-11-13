"""Strict information-set forecast for the China youth model (TODO §5, P1: out-of-sample test against the naive benchmark).

The existing early-window exercise (calibrate_china.py, window='early') fits 2018-22 but builds the demand index from the
WHOLE record: the adult unemployment rate after 2022 is observed, it is backed out using observed youth unemployment,
and the seasonal adjustment uses all years. That is a conditional extrapolation, not a forecast
(docs/UPDATE_2026_11_04.md).

Here everything the model sees is what was available at the cutoff (end of December 2022):
  * youth and urban unemployment: truncated at the cutoff;
  * demand index A_t: computed and seasonally adjusted on data up to the cutoff only; after it, a prespecified rule;
  * graduates: the MoE announces each year's expected class in the preceding autumn, so the next year (2023: 11.58m)
    is known at the cutoff; later years follow a prespecified rule;
  * tertiary entrants (non-graduate leavers): held at the last known year; births are already known;
  * real-estate investment: level held at its last known value.
Rules for the future are fixed below BEFORE scoring and every rule is reported. The point is to separate model error
from input-forecast error: a second information set, 'strict+realised inputs', feeds the realised graduates and
demand into the vintage-fitted parameters, which is the cleanest test of the model's structure.

Run from engine/:  python -m firms.forecast_strict [--starts N]  -> firms/results/forecast_strict.{json,md}
"""
import argparse, json, math, os, sys
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firms import model as M, data_china as D
from firms import calibrate_china as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'results')
CUTOFF = (2022, 12)
FIT = (2018, 2022)


class Vintage:
    """data_china as known at `cutoff`, with prespecified rules for later inputs."""

    def __init__(self, cutoff=CUTOFF, grad_rule='trend3', known_grad_years=1):
        self.cutoff, self.grad_rule = cutoff, grad_rule
        last = cutoff[0] + known_grad_years                  # 2023 class announced autumn 2022
        self.G = {y: v for y, v in D.GRADUATES.items() if y <= last}
        self.last_g = last
        ks = sorted(self.G)
        self.g_step = (self.G[ks[-1]] - self.G[ks[-4]]) / 3   # mean annual change over the last three known years
        self.TE = {y: v for y, v in D.TERTIARY_ENTRANTS.items() if y <= cutoff[0]}
        self.PG = {y: v for y, v in D.PROPERTY_GROWTH.items() if y <= cutoff[0]}

    def youth(self, y, m):
        return D.youth(y, m) if (y, m) <= self.cutoff else None

    def urban(self, y, m):
        return D.urban(y, m) if (y, m) <= self.cutoff else None

    def graduates(self, y):
        if y <= self.last_g:
            return D._interp(self.G, y)
        if self.grad_rule == 'flat':
            return self.G[self.last_g]
        return self.G[self.last_g] + self.g_step * (y - self.last_g)  # 'trend3'

    def nongrad_school_leavers(self, y):
        c18 = D._interp(D.BIRTHS, y - 18)
        return max(c18 - D._interp(self.TE, y), 0.0)

    def property_index(self, y, m):
        saved = D.PROPERTY_GROWTH
        try:
            D.PROPERTY_GROWTH = self.PG                      # property_index reads the module global
            return D.property_index(y, m)
        finally:
            D.PROPERTY_GROWTH = saved


def fill_demand(A, cutoff, rule):
    """Extend a demand dict past the cutoff with a prespecified rule."""
    known = sorted(k for k in A if k <= cutoff)
    last12 = float(np.mean([A[k] for k in known[-12:]]))
    out = {k: v for k, v in A.items() if k <= cutoff}
    y, m = cutoff
    while (y, m) < (2026, 12):
        m += 1
        if m > 12:
            y, m = y + 1, 1
        out[(y, m)] = last12 if rule == 'last12' else A[known[-1]]
    return out


REF = C.REF          # S_ref, g_H, g_N: from a flat-demand pass whose drift uses 2010-2018 only (pre-cutoff)


def run(theta, info, over=None):
    """info: 'strict' | 'realised_inputs' | 'leaky' (the existing early-window setup)."""
    kw = dict(REF)
    kw.update({n: float(v) for (n, *_), v in zip(C.FREE, theta)})
    kw.update(over or {})
    if info == 'leaky':
        return M.YouthMarket(D, **kw).run()
    V = Vintage()
    if info == 'strict':
        ym = M.YouthMarket(V, **kw)
        ym.A = fill_demand(ym.A, CUTOFF, 'last12')           # graduates, leavers and property also come from V
    else:                                                    # realised inputs, vintage-fitted parameters
        ym = M.YouthMarket(D, **kw)
    return ym.run()


def obs_pairs(R, y0, y1, method, flags=('v', 'm')):
    return C.obs_pairs(R, y0, y1, method, flags)


def resid(theta, over):
    R = run(theta, 'strict', over)
    pr = obs_pairs(R, *FIT, 'old')
    r = [mod - ob for *_, ob, mod, _ in pr]
    return np.array(r) if all(map(math.isfinite, r)) else np.full(len(pr), 50.0)


def fit(over, nstarts, seed=1):
    lo = [f[1] for f in C.FREE]; hi = [f[2] for f in C.FREE]
    rng = np.random.default_rng(seed)
    starts = [np.array([f[3] for f in C.FREE])] + [rng.uniform(lo, hi) for _ in range(nstarts - 1)]
    best = None
    for s in starts:
        try:
            r = least_squares(resid, s, bounds=(lo, hi), diff_step=1e-3, max_nfev=300, args=(over,))
        except ValueError:
            continue
        if best is None or r.cost < best.cost:
            best = r
    return best


def naive(kind):
    """Benchmarks using only pre-cutoff youth data: same calendar month of 2022, or the 2022 annual mean."""
    v22 = {m: D.youth(2022, m)[0] for m in range(1, 13)}
    mean22 = float(np.mean(list(v22.values())))
    return (lambda y, m: v22[m]) if kind == 'same_month_2022' else (lambda y, m: mean22)


def score(R=None, f=None):
    """MAE etc. on the test sets: 2023 H1 (old method) and Dec 2023 - Sep 2026 verified (new method)."""
    out = {}
    for name, (y0, y1, meth, flags) in {'old_2023H1': (2023, 2023, 'old', ('v',)),
                                        'new_verified': (2023, 2026, 'new', ('v',))}.items():
        if R is not None:
            pr = obs_pairs(R, y0, y1, meth, flags)
        else:
            pr = [(y, m, o[0], f(y, m), o[2]) for y in range(y0, y1 + 1) for m in range(1, 13)
                  if (o := D.youth(y, m)) and o[1] == meth and o[2] in flags]
        out[name] = C.stats(pr)
    return out


def demand_leak_check():
    """The strict demand index must not move when post-cutoff youth data move (it moved in the leaky version)."""
    V = Vintage()
    base = M.demand_index(dict(M.DEFAULTS), V)[0]
    saved = dict(D._NEW)
    try:
        for k in list(D._NEW):
            D._NEW[k] = (D._NEW[k][0] + 1.0, D._NEW[k][1])
        bumped = M.demand_index(dict(M.DEFAULTS), Vintage())[0]
    finally:
        D._NEW.clear(); D._NEW.update(saved)
    return max(abs(base[k] - bumped[k]) for k in base)


def main(nstarts):
    os.makedirs(OUT, exist_ok=True)
    over = dict(sigma_A=5.0)
    best = fit(over, nstarts)
    th = best.x
    stored = json.load(open(os.path.join(OUT, 'china_fit.json')))
    th_leaky = [stored['profiles'][stored['early']]['params'][n] for n, *_ in C.FREE]
    rows = {
        'strict (vintage Dec 2022, rules for future inputs)': score(run(th, 'strict', over)),
        'strict fit + realised inputs (structure test)': score(run(th, 'realised_inputs', over)),
        'existing early-window fit (leaky, for reference)': score(run(th_leaky, 'leaky', over)),
        'naive: same month of 2022': score(f=naive('same_month_2022')),
        'naive: 2022 annual mean': score(f=naive('mean_2022')),
    }
    Rs = run(th, 'strict', over)
    probe = {}
    for lam in (0.005, 0.01, 0.03):                     # sensitivity, NOT a forecast: chosen after seeing the test
        o = dict(over, lam_g=lam); b = fit(o, max(2, nstarts // 2)); R = run(b.x, 'strict', o)
        probe[str(lam)] = dict(fit_mae=C.stats(obs_pairs(R, *FIT, 'old'))['mae'], **score(R))
    res = dict(cutoff=CUTOFF, over=over, nstarts=nstarts, cost=float(best.cost),
               params={n: float(v) for (n, *_), v in zip(C.FREE, th)},
               at_bounds=[n for (n, lo, hi, _), v in zip(C.FREE, th) if min(v - lo, hi - v) < 1e-2 * (hi - lo)],
               fit_2018_22=C.stats(obs_pairs(Rs, *FIT, 'old')), scores=rows,
               demand_leak_max_abs=demand_leak_check(), wage_speed_probe=probe,
               rules=dict(demand='mean of the last 12 seasonally adjusted months (2022)',
                          graduates='2023 as announced (11.58m); then +mean annual change 2020-23 per year',
                          tertiary_entrants='held at 2022', property='level held at end-2022',
                          seasonal_adjustment='calendar-month means over 2018-01..2022-12 only'))
    json.dump(res, open(os.path.join(OUT, 'forecast_strict.json'), 'w'), indent=1)
    report(res)
    return res


def report(res):
    L = ['# Strict information-set forecast (China youth unemployment)', '',
         'Generated by `python -m firms.forecast_strict`. Fitted to 2018-01..2022-12 (old NBS method) using only data '
         'available at the end of December 2022. Scored without refitting on 2023 H1 (old method) and on verified '
         'new-method months, Dec 2023 - Sep 2026. MAE in percentage points.', '',
         '| Information set | 2023 H1 MAE | 2023 H1 bias | New-method MAE | New-method bias | n new |',
         '|---|---:|---:|---:|---:|---:|']
    for k, s in res['scores'].items():
        a, b = s['old_2023H1'], s['new_verified']
        L.append(f"| {k} | {a['mae']:.2f} | {a['bias']:+.2f} | {b['mae']:.2f} | {b['bias']:+.2f} | {b['n']} |")
    L += ['', f"Fit to 2018-22: MAE {res['fit_2018_22']['mae']:.2f}, correlation {res['fit_2018_22']['corr']:.2f}. "
          f"Parameters at a bound: {', '.join(res['at_bounds']) or 'none'}.", '',
          f"Leak check: raising every post-cutoff youth observation by 1 point moves the strict demand index by at most "
          f"{res['demand_leak_max_abs']:.1e} (the leaky index moved by up to 6.3e-3).", '', '## Prespecified rules', '']
    L += [f"- **{k}**: {v}" for k, v in res['rules'].items()]
    L += ['', '## Why it fails: graduate wage speed (sensitivity, not a forecast)', '',
          'With demand held flat after 2022, the strict model still has graduate job-finding nearly double in 2023: '
          'the 2022 graduate surge is absorbed as graduate wages catch up. The fitted wage speed lam_g '
          f"({res['params']['lam_g']:.3f} per month) is weakly identified by 2018-22. Refitting with lam_g held slower:", '',
          '| lam_g | 2018-22 fit MAE | 2023 H1 MAE | New-method MAE | New-method bias |', '|---:|---:|---:|---:|---:|']
    L += [f"| {k} | {v['fit_mae']:.2f} | {v['old_2023H1']['mae']:.2f} | {v['new_verified']['mae']:.2f} | "
          f"{v['new_verified']['bias']:+.2f} |" for k, v in res['wage_speed_probe'].items()]
    L += ['', 'In-sample fit barely changes while the forecast error roughly halves, so the forecast is decided by a '
          'parameter the fitting window cannot pin down. Choosing lam_g from this table would use the test data. '
          'The honest route is an outside measure of graduate starting-wage adjustment (MyCOS starting salaries, '
          'TODO §1 P2) fixed before the forecast is scored. Even the best row loses to naive on 2023 H1.']
    L += ['', '## Parameters (strict fit)', '', '| Parameter | Value |', '|---|---:|']
    L += [f"| {k} | {v:.4f} |" for k, v in res['params'].items()]
    L += ['', '## Reading it', '',
          'The new-method naive benchmark compares a 2022 old-method value with a new-method observation; the two '
          'definitions differ (searching students counted vs excluded), and the model applies the right observation '
          'rule while the naive forecast cannot. That asymmetry favours the model, so a model that still loses to '
          'naive has failed cleanly. Old/new definition-compatible benchmarks need a published overlap series, which '
          'NBS has not released.']
    open(os.path.join(OUT, 'forecast_strict.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--starts', type=int, default=6)
    main(ap.parse_args().starts)
