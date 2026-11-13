"""Review item 5.3: history match of simple population and settled-area paths to the Klassen et al.
period table in public/engines/provisioning.js (parsed directly from that file, not retyped).

Model (illustrative, not a causal model):
  P(t) = K / (1 + (K/P0 - 1) * exp(-r (t - t0)))          logistic population, t0 = midpoint of first period
  A(t) = Amax * (1 - q * P(t) / K)                          settled area in km2; q may be negative
Free parameters (uniform priors): P0 in [20000, 30000], r in [0.002, 0.04] per year, K in [1.5e5, 1.5e6],
  Amax in [1200, 1400] km2, q in [-0.2, 0.2].
Each period is compared at its midpoint year. A draw is accepted when, for every period,
  |P_model - P_data| / P_data <= tol_pop   and   |A_model - A_data| / A_data <= tol_area.
Run from the repo root:  python3 experiments/angkor-review/calibrate_provisioning.py
"""
import json, random, re, math, statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = (ROOT / 'public/engines/provisioning.js').read_text()
pat = re.compile(r'\{begin:(\d+),end:(\d+),communities:(\d+),population:(\d+),areaKm2:(\d+)\}')
periods = [dict(begin=int(a), end=int(b), population=int(d), area=int(e)) for a, b, _, d, e in pat.findall(SRC)]
assert len(periods) == 6, periods
for p in periods:
    p['mid'] = (p['begin'] + p['end']) / 2
T0 = periods[0]['mid']
N = 400000
SEED = 20261113
TOLS = [(.10, .05), (.10, .10), (.20, .10), (.25, .15), (.30, .20)]   # (population tolerance, area tolerance)


def predict(th, t):
    P0, r, K, Amax, q = th
    P = K / (1 + (K / P0 - 1) * math.exp(-r * (t - T0)))
    A = Amax * (1 - q * P / K)
    return P, A


rng = random.Random(SEED)
draws = []
for _ in range(N):
    th = (rng.uniform(20000, 30000), rng.uniform(.002, .04), rng.uniform(1.5e5, 1.5e6),
          rng.uniform(1200, 1400), rng.uniform(-.2, .2))
    preds = [predict(th, p['mid']) for p in periods]
    pe = [abs(P - d['population']) / d['population'] for (P, _), d in zip(preds, periods)]
    ae = [abs(A - d['area']) / d['area'] for (_, A), d in zip(preds, periods)]
    draws.append((th, preds, pe, ae))

out = {'seed': SEED, 'draws': N, 'periods': periods, 'priors': dict(P0=[20000, 30000], r=[.002, .04], K=[1.5e5, 1.5e6], Amax=[1200, 1400], q=[-.2, .2]),
       'tolerances': []}
names = ['P0', 'r', 'K', 'Amax', 'q']
md = []
md.append(f'Draws: {N} (seed {SEED}). Periods: {len(periods)} from provisioning.js; t0 = {T0}.\n')
# Diagnostic (no sampling): growth rate implied by the table between successive period midpoints.
md.append('Implied growth rate between successive midpoints (ln ratio / years), a shape check on the table:\n')
md.append('| Interval | Years | Implied r per year |')
md.append('|---|---|---|')
for a_, b_ in zip(periods[:-1], periods[1:]):
    dt = b_['mid'] - a_['mid']
    md.append(f"| {a_['begin']}–{a_['end']} to {b_['begin']}–{b_['end']} | {dt:.1f} | {math.log(b_['population']/a_['population'])/dt:.5f} |")
md.append('')
best = min(draws, key=lambda d: max(max(d[2]), max(d[3])))
min_pop=min(max(d[2]) for d in draws); min_area=min(max(d[3]) for d in draws)
out_min=dict(min_worst_population_error=min_pop, min_worst_area_error=min_area)
md.append(f'Smallest worst-case population error over all draws: {min_pop:.3f}; smallest worst-case area error (over draws with that same population error bound not required): {min_area:.3f}.\n')
md.append('Best single draw (smallest worst-case relative error): '
          + ', '.join(f'{n}={v:.4g}' for n, v in zip(names, best[0]))
          + f'; worst population error {max(best[2]):.3f}, worst area error {max(best[3]):.3f}.\n')
for tp, ta in TOLS:
    acc = [d for d in draws if all(e <= tp for e in d[2]) and all(e <= ta for e in d[3])]
    rate = len(acc) / N
    entry = dict(tol_population=tp, tol_area=ta, accepted=len(acc), acceptance_rate=rate)
    md.append(f'### Tolerance: population ±{tp*100:.0f}%, area ±{ta*100:.0f}%\n')
    md.append(f'Accepted {len(acc)} of {N} draws (acceptance rate {rate*100:.3f}%).\n')
    if acc:
        md.append('| Parameter | Prior | Accepted min | 5th pct | Median | 95th pct | Accepted max |')
        md.append('|---|---|---|---|---|---|---|')
        pri = {'P0': '20000–30000', 'r': '0.002–0.04', 'K': '1.5e5–1.5e6', 'Amax': '1200–1400', 'q': '−0.2–0.2'}
        post = {}
        for i, n in enumerate(names):
            xs = sorted(d[0][i] for d in acc)
            q = lambda pp: xs[min(len(xs) - 1, int(pp * (len(xs) - 1) + .5))]
            post[n] = dict(min=xs[0], p5=q(.05), median=q(.5), p95=q(.95), max=xs[-1])
            md.append(f'| {n} | {pri[n]} | {xs[0]:.4g} | {q(.05):.4g} | {q(.5):.4g} | {q(.95):.4g} | {xs[-1]:.4g} |')
        entry['posterior'] = post
        md.append('\nAccepted-run predictions at each period midpoint (min to max across accepted runs):\n')
        md.append('| Period | Data population | Model population range | Data area km2 | Model area range |')
        md.append('|---|---|---|---|---|')
        for j, p in enumerate(periods):
            Ps = [d[1][j][0] for d in acc]; As = [d[1][j][1] for d in acc]
            md.append(f"| {p['begin']}–{p['end']} | {p['population']} | {min(Ps):.0f}–{max(Ps):.0f} | {p['area']} | {min(As):.0f}–{max(As):.0f} |")
    else:
        md.append('No accepted draws at this tolerance.\n')
    # which period binds: fraction of draws failing each period (population or area)
    fails = [sum(1 for d in draws if d[2][j] > tp or d[3][j] > ta) / N for j in range(len(periods))]
    entry['fraction_failing_period'] = fails
    md.append('\nFraction of all draws that fail each period (population or area outside tolerance): '
              + ', '.join(f"{p['begin']}–{p['end']}: {f:.3f}" for p, f in zip(periods, fails)) + '\n')
    out['tolerances'].append(entry)
(HERE / 'results/calibration-provisioning.json').write_text(json.dumps(out, indent=2))
(HERE / 'results/calibration-provisioning.md').write_text('\n'.join(md) + '\n')
print('\n'.join(md))
