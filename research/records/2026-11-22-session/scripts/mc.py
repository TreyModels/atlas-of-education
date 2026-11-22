"""Monte Carlo battery (fast version)."""
import json, os, gzip
import numpy as np
import battery as B

V, F = B.V, B.F
KEY = ["lsc", "sec", "ter", "gpi_ter", "u5mr", "gdppc_log", "flfp", "electricity"]
NAME = B.NAME


def pairs(c):
    out = []
    for (i, t), v in F.items():
        if (i, t + 10) in F and (i, t) in V[c]:
            out.append((i, t, F[(i, t + 10)] - v, V[c][(i, t)]))
    return out


def prep(rows):
    iso = [r[0] for r in rows]; yr = [r[1] for r in rows]
    ui = {v: k for k, v in enumerate(sorted(set(iso)))}
    uy = {v: k for k, v in enumerate(sorted(set(yr)))}
    gi = np.array([ui[v] for v in iso]); gy = np.array([uy[v] for v in yr])
    return gi, gy


def dm(a, g):
    s = np.bincount(g, weights=a); n = np.bincount(g)
    return a - (s / n)[g]


def r2(y, x, gi, gy):
    if len(y) < 100 or x.std() == 0:
        return 0.0
    xw = dm(dm(x, gi), gy); yw = dm(dm(y, gi), gy)
    if xw.std() == 0:
        return 0.0
    return float(np.corrcoef(xw, yw)[0, 1] ** 2) * 100


rows = pairs("lsc")
obs = r2(np.array([r[2] for r in rows]), np.array([r[3] for r in rows]), *prep(rows))
print("=" * 72)
print("MC 1  LUCK TEST — shift each country's education series in time")
print("=" * 72)
print(f"  actual share of the fall explained: {obs:.1f}%")

byc = {}
for r in rows:
    byc.setdefault(r[0], []).append(r)
blocks = []
for iso, rs in byc.items():
    rs = sorted(rs, key=lambda z: z[1])
    blocks.append((np.array([r[1] for r in rs]), np.array([r[2] for r in rs]), np.array([r[3] for r in rs])))
rng = np.random.default_rng(7)
nulls = []
for rep in range(500):
    Y, X, I, T = [], [], [], []
    for k, (yrs, dv, xv) in enumerate(blocks):
        sh = rng.integers(len(xv))
        X.append(np.roll(xv, sh)); Y.append(dv)
        I.append(np.full(len(dv), k)); T.append(yrs)
    y = np.concatenate(Y); x = np.concatenate(X)
    gi = np.concatenate(I); gy = np.concatenate(T)
    nulls.append(r2(y, x, gi, gy))
nulls = np.array(nulls)
print(f"  with no link at all you'd usually get {np.median(nulls):.1f}%")
print(f"  95% of runs fell between {np.percentile(nulls,2.5):.1f}% and {np.percentile(nulls,97.5):.1f}%")
print(f"  pure luck reached {obs:.1f}% in {100*np.mean(nulls>=obs):.1f}% of 500 runs")

print()
print("=" * 72)
print("MC 2  NOISE TEST — if part of the education figure is measurement error")
print("=" * 72)
y = np.array([r[2] for r in rows]); x = np.array([r[3] for r in rows])
for frac in (0.2, 0.4, 0.6):
    sims = []
    for rep in range(200):
        xn = x + np.random.default_rng(rep).normal(0, frac * x.std(), len(x))
        sims.append(r2(y, xn, *prep(rows)))
    print(f"  {int(frac*100)}% noise -> {np.mean(sims):5.1f}% explained  (5th-95th: {np.percentile(sims,5):.1f}-{np.percentile(sims,95):.1f})")

print()
print("=" * 72)
print("MC 3  COUNTRY LUCK TEST — redraw the countries, 300 times")
print("=" * 72)
data = {}
for c in KEY:
    rr = pairs(c)
    data[c] = (np.array([r[2] for r in rr]), np.array([r[3] for r in rr]),
               np.array([r[0] for r in rr]), np.array([r[1] for r in rr]))
isos = sorted({r[0] for r in rows})
idx = {c: {v: k for k, v in enumerate(sorted({r[0] for r in data[c][2]}))} for c in KEY}
tally = {c: 0 for c in KEY}; top3 = {c: 0 for c in KEY}
rng2 = np.random.default_rng(11)
for rep in range(300):
    pick = set(rng2.choice(isos, size=len(isos), replace=True).tolist())
    sc = {}
    for c in KEY:
        Y, X, I, T = data[c]
        m = np.array([v in pick for v in I])
        if m.sum() < 100:
            sc[c] = 0.0; continue
        gi, gy = prep([(v, t) for v, t in zip(I[m], T[m])])
        sc[c] = r2(Y[m], X[m], gi, gy)
    order = sorted(sc, key=lambda k: -sc[k])
    tally[order[0]] += 1
    for c in order[:3]:
        top3[c] += 1
for c in sorted(KEY, key=lambda k: -tally[k]):
    print(f"  {NAME[c]:32s} first {100*tally[c]/300:4.0f}%    top three {100*top3[c]/300:4.0f}%")
