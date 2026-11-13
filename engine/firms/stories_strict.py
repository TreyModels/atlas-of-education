"""The China story-tournament winner under the strict protocol (TODO §R, P1).

firms/stories.py is explanatory: every story sees 2018-26. Its winner is the 'everything' story (all mechanisms
together: property loading, the Aug 2021 regulatory step, credential inflation, automation, the consumption loop,
and queuing with 11-month entry). Here that story is refitted using only what was public in December 2024, with the
same protocol as forecast_2024.py and seasonal_2024.py, and scored on verified new-method months Jan 2025 - Sep 2026.

Evidence in the fit (all dated on or before the Dec 2024 cutoff):
  youth      old method 2018-01..2023-06 and new method 2023-12..2024-12, new months weighted as in forecast_2024.py
  wages      MyCOS graduate starting pay relative to the NBS urban wage, classes 2019-23 (published by mid-2024)
  adult      consistency with the adult labour market, 2019-24 (aggregate demand is backed out of adult unemployment)
  queue      civil-service applicants passing review, 2024 against 2023 (2.60 -> 3.03 m)
Evidence the tournament used that is NOT available at the cutoff, and is therefore reported as out-of-sample scores
instead: graduate postings H1 2025 (-22%), the 2025 and 2026 exam queues, and adult consistency for 2025-26.

Benchmarks: naive same month of 2024 (like-for-like definition), and the spread-out-entry model of seasonal_2024.py.
This is a forecast test, not a blind one: the story set and the 11-month spread were chosen after the test months had
been seen (see seasonal_2024.md, point 4). The blind test remains the Oct-Dec 2026 releases.

Run from engine/:  python -m firms.stories_strict [--starts N]  -> firms/results/stories_strict.{json,md}
"""
import argparse, json, math, os, sys
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mc as MC
from firms import calibrate_china as C, data_china as D, forecast_strict as F, forecast_2024 as F4, stories as ST, wage_anchor as W

ST_LABEL = dict(e_prop='property loading', dr_drop='regulatory step (Aug 2021)', cred_k='credential inflation',
                auto_a='automation', cons_c='consumption loop', delay_k='queuing / delayed entry')
OUT = F.OUT
CUT = F4.CUT
STORY = 'everything'
W_NEW = math.sqrt(66 / 13)
SPEC = ST.spec(STORY)
LO = np.array([f[1] for f in SPEC]); HI = np.array([f[2] for f in SPEC])
WAGE_YEARS = [y for y in (2019, 2020, 2021, 2022, 2023)
              if y in D.STARTING_WAGE_BA and D.STARTING_WAGE_PUBLISHED[y] <= CUT and y in D.URBAN_WAGE]
ADULT_YEARS = tuple(range(2019, 2025))
QUEUE_FIT = (2024,)


def build(x):
    kw = dict(C.REF, sigma_A=5.0, e_prop=0.0, dr_drop=0.0)
    kw.update(ST.STORIES[STORY][2]); kw.update({f[0]: float(v) for f, v in zip(SPEC, x)})
    ym = ST.StoryMarket(F.Vintage(cutoff=CUT, known_grad_years=1), **kw)
    ym.A = F.fill_demand(ym.A, CUT, 'last12')
    return ym


def run(x):
    ym = build(x)
    return ym.run(), ym


def _residuals(x):
    R, ym = run(x)
    old, new = F4.fit_pairs(R)
    ry = [mod - ob for *_, ob, mod, _ in old] + [W_NEW * (mod - ob) for *_, ob, mod, _ in new]
    n = len(ry)
    wp, wo = W.model_wage_path(R, [2018] + WAGE_YEARS), W.observed_path([2018] + WAGE_YEARS)
    rw = [math.sqrt(n / len(WAGE_YEARS)) * 100 * (wp[y] - wo[y]) / 4 for y in WAGE_YEARS]
    ra = [math.sqrt(n / len(ADULT_YEARS)) * 16 * (np.mean(ym.dmult.get(y, [1.0])) - 1) / 2 for y in ADULT_YEARS]
    rq = []
    for y in QUEUE_FIT:
        d, d0 = ym.delay.get(y, 0.0), ym.delay.get(2023, 0.0)
        md = math.log(max(d, 1e-3) / max(d0, 1e-3)) if (d0 > 0 and d > 0) else 0.0
        rq.append(math.sqrt(n / len(QUEUE_FIT)) * 10 * (md - math.log(ST.QUEUE[y] / ST.QUEUE[2023])) / 4)
    r = ry + rw + ra + rq
    return np.array(r) if all(map(math.isfinite, r)) else np.full(len(r), 50.0)


_LEN = [0]


def residuals(x):
    try:
        r = _residuals(x)
        _LEN[0] = len(r)
        return r
    except (ZeroDivisionError, ValueError, OverflowError, FloatingPointError):
        return np.full(_LEN[0] or 100, 50.0)


def leak_check():
    """The residual vector must not move when post-cutoff observations move. Returns the largest change."""
    x = np.array([f[3] for f in SPEC])
    base = residuals(x)
    saved = dict(D._NEW)
    try:
        for k in list(D._NEW):
            if k > CUT:
                D._NEW[k] = (D._NEW[k][0] + 3.0, D._NEW[k][1])
        bumped = residuals(x)
    finally:
        D._NEW.clear(); D._NEW.update(saved)
    return float(np.max(np.abs(base - bumped)))


def _fit_one(s):
    try:
        r = least_squares(residuals, s, bounds=(LO, HI), diff_step=1e-3, max_nfev=200)
        return float(r.cost), list(map(float, r.x))
    except ValueError:
        return math.inf, None


def starts(n):
    warm = json.load(open(os.path.join(OUT, 'seasonal_2024.json')))['rows']['spread11']['params']   # a Dec 2024-protocol fit
    r = MC.rng(17)
    S0 = [np.clip([warm.get(f[0], f[3]) for f in SPEC], LO + 1e-6, HI - 1e-6), np.array([f[3] for f in SPEC])]
    return S0 + [r.uniform(LO, HI) for _ in range(max(0, n - 2))]


def out_of_sample(R, ym):
    """Evidence the tournament fitted but the cutoff hides: reported as scores."""
    d0 = ym.delay.get(2023, 0.0)
    return dict(
        postings_H1_2025_pct=C.vg_check(R), postings_observed_pct=-22.0,
        queue={y: dict(model=(ym.delay.get(y, 0.0) / d0 if d0 > 0 else float('nan')), observed=ST.QUEUE[y] / ST.QUEUE[2023])
               for y in (2025, 2026)},
        adult_demand_multiplier={y: float(np.mean(ym.dmult.get(y, [1.0]))) for y in (2025, 2026)})


def ablate(x):
    """Diagnostic, not a forecast: switch one mechanism off at the fitted parameters (no refit) and score the test months."""
    idx = {f[0]: i for i, f in enumerate(SPEC)}
    out = {}
    for name, off in ST.MECH_OFF.items():
        xo = np.array(x, float); xo[idx[name]] = off
        if name == 'delay_k':
            xo[idx['delay0']] = 0.0
        R, _ = run(xo)
        out[name] = C.stats(F4.test_pairs(R))
    return out


def main(nstarts, saved=False):
    leak = leak_check()
    assert leak == 0.0, f'post-cutoff data leak into the fit: {leak}'
    if saved:
        prev = json.load(open(os.path.join(OUT, 'stories_strict.json')))
        c, x = prev['cost'], [prev['params'][f[0]] for f in SPEC]
    else:
        fits = MC.run_batch(_fit_one, [(s,) for s in starts(nstarts)], chunksize=1)
        c, x = min((c, x) for c, x in fits if x is not None)
    R, ym = run(x)
    old, new = F4.fit_pairs(R)
    tp = F4.test_pairs(R)
    nf = F4.naive('same_month_2024')
    d = np.array([abs(md - ob) - abs(nf(y, m) - ob) for y, m, ob, md, _ in tp])
    t = float(d.mean() / (d.std(ddof=1) / math.sqrt(len(d))))
    prev = json.load(open(os.path.join(OUT, 'seasonal_2024.json')))
    sp = prev['rows']['spread11']
    x11 = [sp['params'][f[0]] for f in C.FREE]
    tp11 = F4.test_pairs(__import__('firms.seasonal_2024', fromlist=['run']).run([sp['params'][f[0]] for f in C.FREE], 'spread11'))
    d11 = np.array([abs(md - ob) - abs(nf(y, m) - ob) for y, m, ob, md, _ in tp11])
    res = dict(cutoff=CUT, story=STORY, starts=nstarts, leak_check=leak, cost=c,
               params={f[0]: v for f, v in zip(SPEC, x)},
               at_bounds=[f[0] for f, v in zip(SPEC, x) if min(v - f[1], f[2] - v) < 1e-2 * (f[2] - f[1])],
               n_params=len(SPEC), fit_old=C.stats(old), fit_new=C.stats(new), test=C.stats(tp),
               naive=F4.score_fn(nf), naive_mean=F4.score_fn(F4.naive('mean_2024')),
               spread11_test=sp['test'], vs_naive=dict(wins=int((d < 0).sum()), n=len(d), mean_diff=float(d.mean()), t=t),
               spread11_vs_naive=dict(wins=int((d11 < 0).sum()), n=len(d11), mean_diff=float(d11.mean())),
               seasonal_test=F4.seasonal(tp), out_of_sample=out_of_sample(R, ym), ablation=ablate(x),
               series={f"{y}-{m:02d}": [ob, md] for y, m, ob, md, _ in new + tp})
    json.dump(res, open(os.path.join(OUT, 'stories_strict.json'), 'w'), indent=1)
    report(res)


def report(r):
    nv, t, s11 = r['naive'], r['test'], r['spread11_test']
    oo = r['out_of_sample']
    beats = t['mae'] < nv['mae']
    L = ['# The tournament winner under the strict protocol (Dec 2024 cutoff)', '',
         f"Generated by `python -m firms.stories_strict --starts {r['starts']}`. Story: **{r['story']}** ({r['n_params']} free parameters), refitted to "
         'data public by December 2024 and scored without refitting on verified new-method months Jan 2025 - Sep 2026. '
         f"Leak check (change in the fit residuals when post-cutoff observations are altered): {r['leak_check']:.1f}.", '',
         '| Model | Fit old | Fit new 2024 | Test MAE | Test bias | n |', '|---|---:|---:|---:|---:|---:|',
         f"| Tournament winner (strict refit) | {r['fit_old']['mae']:.2f} | {r['fit_new']['mae']:.2f} | **{t['mae']:.2f}** | {t['bias']:+.2f} | {t['n']} |",
         f"| Spread-out entry only (seasonal_2024.py) | | | {s11['mae']:.2f} | {s11['bias']:+.2f} | {s11['n']} |",
         f"| Naive: same month of 2024 | | | **{nv['mae']:.2f}** | {nv['bias']:+.2f} | {nv['n']} |",
         f"| Naive: 2024 mean | | | {r['naive_mean']['mae']:.2f} | {r['naive_mean']['bias']:+.2f} | {r['naive_mean']['n']} |", '',
         f"Months beating same-month naive: winner {r['vs_naive']['wins']}/{r['vs_naive']['n']} (mean paired difference "
         f"{r['vs_naive']['mean_diff']:+.2f} pts, t {r['vs_naive']['t']:+.2f}); spread-only {r['spread11_vs_naive']['wins']}/{r['spread11_vs_naive']['n']} "
         f"({r['spread11_vs_naive']['mean_diff']:+.2f}).", '',
         '## Evidence the tournament fitted but the cutoff hides (scored, not fitted)', '',
         f"- Graduate postings H1 2025 vs H1 2024: model {oo['postings_H1_2025_pct']:+.0f}% against {oo['postings_observed_pct']:+.0f}% observed.",
         '- Civil-service queue relative to 2023: ' + '; '.join(f"{y} model {v['model']:.2f} vs observed {v['observed']:.2f}" for y, v in oo['queue'].items()) + '.',
         '- Adult-demand multiplier (1.00 = no feedback on aggregate demand): ' + '; '.join(f"{y} {v:.3f}" for y, v in oo['adult_demand_multiplier'].items()) + '.', '',
         '## Test error by calendar month (model minus observed, pts)', '', '| Month | Error |', '|---:|---:|']
    for m in range(1, 13):
        v = r['seasonal_test'].get(m, r['seasonal_test'].get(str(m)))
        L.append(f"| {m} | {'' if v is None else f'{v:+.1f}'} |")
    ab = r['ablation']
    L += ['', '## Which mechanism breaks the forecast? (diagnostic: one mechanism off at the fitted parameters, no refit)', '',
          '| Mechanism off | Test MAE | Test bias |', '|---|---:|---:|']
    L += [f"| {ST_LABEL.get(k, k)} | {v['mae']:.2f} | {v['bias']:+.2f} |" for k, v in ab.items()]
    L += ['', 'Parameters: ' + ', '.join(f'{k} {v:.3g}' for k, v in r['params'].items()) +
          f". At a bound ({len(r['at_bounds'])} of {r['n_params']}): {', '.join(r['at_bounds']) or 'none'}.", '',
          '## What this establishes', '',
          f"1. **Out of sample the tournament winner {'beats' if beats else 'does not beat'} the like-for-like naive benchmark:** "
          f"{t['mae']:.2f} against {nv['mae']:.2f} pts (t {r['vs_naive']['t']:+.2f} over {r['vs_naive']['n']} months).",
          f"2. **Against the simpler spread-out-entry model** ({s11['mae']:.2f}): the extra mechanisms "
          + ('improve the forecast.' if t['mae'] < s11['mae'] - 0.02 else 'do not improve the forecast.' if t['mae'] > s11['mae'] + 0.02
             else 'make no material difference to the forecast.'),
          f"3. **The postings fall is still not reproduced:** {oo['postings_H1_2025_pct']:+.0f}% against {oo['postings_observed_pct']:+.0f}%, "
          'close to the in-sample tournament figure (-10%), so the strict protocol did not change this failure.',
          f"3b. **Why it fails:** the fit is good in sample (2024 new-method MAE {r['fit_new']['mae']:.2f}) and then the youth rate runs away "
          f"(test bias {t['bias']:+.2f}). The ablation shows no single culprit: switching off any one mechanism moves the bias by 2-9 pts, "
          'upward for credential inflation and downward for automation, the consumption loop and the 2021 step. The mechanisms are '
          'individually large and offsetting. The 2018-24 path pins down their sum, not each of them, and the sum stops working '
          'once demand is held at its last-12-month mean and the trending terms (automation, credential inflation) keep compounding.',
          f"4. **Caveat on the optimum:** {r['starts']} starts, {len(r['at_bounds'])} of {r['n_params']} parameters at bounds. Offsetting mechanisms mean the fit surface has long flat valleys; a different point in the valley could forecast differently. The stored result is one honest strict fit, not the best the structure could do. A profile over the valley (the Monte Carlo manager's draws, scored on the test months) is the next step before calling the structure itself rejected.",
          '5. **Not a blind test.** The mechanism set and the 11-month spread were chosen after the test months had been seen. The '
          'blind check is the Oct-Dec 2026 releases, scored with `firms.blind_forecast --score` against forecasts frozen on 5 Nov 2026.']
    open(os.path.join(OUT, 'stories_strict.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--starts', type=int, default=6)
    ap.add_argument('--from-saved', action='store_true', help='reuse the stored fit; recompute scores and ablation only')
    a = ap.parse_args(); main(a.starts, a.from_saved)
