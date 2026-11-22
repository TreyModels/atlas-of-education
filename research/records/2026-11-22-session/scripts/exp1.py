#!/usr/bin/env python3
"""Experiment 1: can the estimator tell a CHAIN from a COMMON CAUSE?

World A (chain):   factor prices -> wage employment -> higher education
World B (common):  one latent modernisation factor drives both

Both are simulated on the real coverage mask with real variances. Then the same
estimator is run on both, and we see whether the observed value could have come
from either.
"""
import json, os, gzip
from multiprocessing import Pool
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
NEED = ["ter", "wage_emp", "gdppc_log"]


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in NEED}

rows = []
for (i, t), v in S["ter"].items():
    if (i, t + 10) not in S["ter"] or (i, t) not in S["wage_emp"]:
        continue
    rows.append((i, t, v, S["wage_emp"][(i, t)]))
rows.sort()
ISO = [r[0] for r in rows]
YR = np.array([r[1] for r in rows])
TER0 = np.array([r[2] for r in rows])
WAG0 = np.array([r[3] for r in rows])
UI = {v: n for n, v in enumerate(sorted(set(ISO)))}
GI = np.array([UI[v] for v in ISO])
GY = (YR // 10) * 10
N = len(rows)
print(f"panel: {N} country-decades, {len(UI)} countries")

# real moments after removing country means
def within(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / c)[g]

tw, ww = within(TER0, GI), within(WAG0, GI)
SD_T, SD_W = tw.std(), ww.std()
print(f"real within-country sd:  higher ed {SD_T:.2f}   paid jobs {SD_W:.2f}")


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def fit(y, x, own, gi, gy):
    X = np.column_stack([np.ones(len(y)), x, own])
    X = np.column_stack([dm(X[:, j], gi) for j in range(3)])
    X = np.column_stack([dm(X[:, j], gy) for j in range(3)])
    Y = dm(dm(y, gi), gy)
    b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0)))


def ar1(n_countries, rho, sd, rng):
    """AR(1) shock per country, padded to panel rows; returns a level panel."""
    out = np.zeros(N)
    starts = {}
    for j, g in enumerate(GI):
        starts.setdefault(g, []).append(j)
    for g, idx in starts.items():
        v = 0.0
        sub = np.array(idx)
        order = sub[np.argsort(YR[sub])]
        e = rng.normal(0, sd * np.sqrt(1 - rho ** 2), len(order))
        for k, j in enumerate(order):
            v = rho * v + e[k]
            out[j] = v
    return out


def run_one(a):
    return simulate(a[0], a[1])


def simulate(world, seed):
    rng = np.random.default_rng(seed)
    D = ar1(len(UI), 0.95, 1.0, rng)          # latent development factor
    F = ar1(len(UI), 0.90, 1.0, rng)          # exogenous factor-price shift
    if world == "B":                           # common cause
        noise_t = rng.normal(0, 1, N) * SD_T * 0.6
        noise_w = rng.normal(0, 1, N) * SD_W * 0.6
        ter = SD_T * D + noise_t
        wag = SD_W * D + noise_w
    else:                                      # chain: F -> wage -> education
        base_w = 0.85 * ar1(len(UI), 0.85, SD_W, rng) + 0.5 * SD_W * F
        noise_w = rng.normal(0, 1, N) * SD_W * 0.35
        wag = base_w + noise_w
        base_t = 0.85 * ar1(len(UI), 0.85, SD_T, rng) + 0.55 * SD_T * (wag / (SD_W + 1e-9))
        noise_t = rng.normal(0, 1, N) * SD_T * 0.35
        ter = base_t + noise_t
    # build 10-year changes for ter
    idx = {}
    for j, (i, t) in enumerate(zip(ISO, YR)):
        idx[(i, t)] = j
    keep = [(idx[(i, t)], idx.get((i, t + 10))) for (i, t) in zip(ISO, YR)]
    keep = [(a, b) for a, b in keep if b is not None]
    ja = np.array([k[0] for k in keep]); jb = np.array([k[1] for k in keep])
    gi = GI[ja]; gy = (YR[ja] // 10) * 10
    fwd = fit(ter[jb] - ter[ja], wag[ja], ter[ja], gi, gy)      # wage -> change in ter
    bwd = fit(wag[jb] - wag[ja], ter[ja], wag[ja], gi, gy)      # ter -> change in wage
    return fwd[0], fwd[1], bwd[0], bwd[1]


if __name__ == "__main__":
    # observed value from the real data
    idx = {}
    for j, (i, t) in enumerate(zip(ISO, YR)):
        idx[(i, t)] = j
    keep = [(idx[(i, t)], idx.get((i, t + 10))) for (i, t) in zip(ISO, YR)]
    keep = [(a, b) for a, b in keep if b is not None]
    ja = np.array([k[0] for k in keep]); jb = np.array([k[1] for k in keep])
    gi = GI[ja]; gy = (YR[ja] // 10) * 10
    of = fit(TER0[jb] - TER0[ja], WAG0[ja], TER0[ja], gi, gy)
    ob = fit(WAG0[jb] - WAG0[ja], TER0[ja], WAG0[ja], gi, gy)
    print(f"\nOBSERVED:  paid jobs -> higher ed {of[0]:+.3f} (±{of[1]:.3f})"
          f"   |   higher ed -> paid jobs {ob[0]:+.3f} (±{ob[1]:.3f})")

    tasks = [(w, s) for w in ("A", "B") for s in range(1500)]
    with Pool(48) as p:
        res = p.map(run_one, tasks, chunksize=20)
    for w in ("A", "B"):
        R = np.array([r for (ww, r) in zip([t[0] for t in tasks], res) if ww == w])
        f, b = R[:, 0], R[:, 2]
        ratio = f / np.where(np.abs(b) < 1e-9, np.nan, b)
        name = "A (chain)" if w == "A" else "B (common cause)"
        print(f"\n--- World {name}, {len(R)} simulated panels")
        print(f"  forward (paid jobs -> higher ed): median {np.median(f):+.3f}   "
              f"5-95%: {np.percentile(f,5):+.3f} to {np.percentile(f,95):+.3f}")
        print(f"  backward (higher ed -> paid jobs): median {np.median(b):+.3f}   "
              f"5-95%: {np.percentile(b,5):+.3f} to {np.percentile(b,95):+.3f}")
        inside = np.mean((f > of[0] - 1.96*of[1]) & (f < of[0] + 1.96*of[1]))
        print(f"  share of panels within 95% interval of the observed forward value: {100*inside:.1f}%")
        if w == "B":
            sep = R[:, 0]
    fa = np.array([r for (t, r) in zip(tasks, res) if t[0] == "A"])[:, 0]
    fb = np.array([r for (t, r) in zip(tasks, res) if t[0] == "B"])[:, 0]
    print("\n" + "=" * 70)
    print("CAN THE TEST TELL THEM APART?")
    print("=" * 70)
    print(f"  World A forward coefficient: mean {fa.mean():+.3f}")
    print(f"  World B forward coefficient: mean {fb.mean():+.3f}")
    overlap = min(np.percentile(fa, 95), np.percentile(fb, 95)) - max(np.percentile(fa, 5), np.percentile(fb, 5))
    print(f"  overlap of the two 5-95% ranges: {max(overlap,0):.3f}")
    print(f"  => the LEVEL of the coefficient {'cannot' if overlap>0 else 'can'} separate the worlds")
