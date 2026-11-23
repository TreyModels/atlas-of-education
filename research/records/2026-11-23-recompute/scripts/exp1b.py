import os
#!/usr/bin/env python3
"""Experiment 1b: chain vs common cause, with the dynamics actually built in.

World A (chain):    factor prices -> wage level -> higher ed adjusts toward a target
World B (common):   one random-walk modernisation factor drives both increments

Estimator: change in higher ed over 10 years on the level of paid employment,
with higher ed's own starting level and country + decade effects.
"""
import json, os, gzip
from multiprocessing import Pool
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
T = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in ["ter", "wage_emp"]}

# country -> sorted years with higher-ed data
SER = {}
for (i, t) in T["ter"]:
    SER.setdefault(i, []).append(t)
for i in SER:
    SER[i] = sorted(SER[i])

PAIRS = [(i, t) for i in SER for t in SER[i]
         if (i, t + 10) in T["ter"] and (i, t + 10) in T["wage_emp"]
         and (i, t) in T["wage_emp"]]
PAIRS.sort()
ISO = [p[0] for p in PAIRS]
YR = np.array([p[1] for p in PAIRS])
UI = {v: n for n, v in enumerate(sorted(set(ISO)))}
GI = np.array([UI[v] for v in ISO])
GY = (YR // 10) * 10


def real_sd():
    a = np.array([T["ter"][p] for p in PAIRS])
    b = np.array([T["wage_emp"][p] for p in PAIRS])

    def w(v, g):
        s = np.bincount(g, weights=v); c = np.bincount(g)
        return v - (s / c)[g]
    return w(a, GI).std(), w(b, GI).std()


SD_T, SD_W = real_sd()


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def fit(y, x, own):
    X = np.column_stack([np.ones(len(y)), x, own])
    X = np.column_stack([dm(X[:, j], GI) for j in range(3)])
    X = np.column_stack([dm(X[:, j], GY) for j in range(3)])
    Y = dm(dm(y, GI), GY)
    b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(GI):
        m = GI == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0)))


def build(world, seed):
    """simulate ter and wage on every country-year we actually observe"""
    rng = np.random.default_rng(seed)
    ter = {}; wag = {}
    for iso, years in SER.items():
        n = len(years)
        D = np.cumsum(rng.normal(0, 1, n))          # random-walk modernisation
        F = np.zeros(n)                              # factor-price push
        v = 0.0
        for k in range(n):
            v = 0.9 * v + rng.normal(0, 1)
            F[k] = v
        w = np.zeros(n); e_ = np.zeros(n)
        if world == "A":
            for k in range(n):
                target_w = 0.55 * F[k]
                w[k] = (w[k - 1] if k else 0.0) + 0.35 * (target_w * 4 - (w[k - 1] if k else 0.0)) + rng.normal(0, 1.2)
                tgt = 3.2 * (w[k] / 4.0) * SD_T
                e_[k] = (e_[k - 1] if k else 0.0) + 0.20 * (tgt - (e_[k - 1] if k else 0.0)) + rng.normal(0, SD_T * 0.5)
        else:
            for k in range(n):
                dD = D[k] - (D[k - 1] if k else 0.0)
                w[k] = (w[k - 1] if k else 0.0) + SD_W * 0.45 * dD + rng.normal(0, SD_W * 0.3)
                e_[k] = (e_[k - 1] if k else 0.0) + SD_T * 0.020 * dD + rng.normal(0, SD_T * 0.3)
        for k, y in enumerate(years):
            ter[(iso, y)] = e_[k]
            wag[(iso, y)] = w[k]
    return ter, wag


def run_one(arg):
    world, seed = arg
    ter, wag = build(world, seed)
    yt = np.array([ter[p] for p in PAIRS]); yw = np.array([wag[p] for p in PAIRS])
    yt10 = np.array([ter[(i, t + 10)] for (i, t) in PAIRS])
    yw10 = np.array([wag[(i, t + 10)] for (i, t) in PAIRS])
    f = fit(yt10 - yt, yw, yt)
    b = fit(yw10 - yw, yt, yw)
    return world, f[0], f[1], b[0], b[1]


if __name__ == "__main__":
    yt = np.array([T["ter"][p] for p in PAIRS]); yw = np.array([T["wage_emp"][p] for p in PAIRS])
    yt10 = np.array([T["ter"][(i, t + 10)] for (i, t) in PAIRS])
    yw10 = np.array([T["wage_emp"][(i, t + 10)] for (i, t) in PAIRS])
    of, os_ = fit(yt10 - yt, yw, yt)
    ob, obs_ = fit(yw10 - yw, yt, yw)
    print(f"{len(PAIRS)} country-decades, {len(UI)} countries")
    print(f"within-country sd: higher ed {SD_T:.2f}, paid jobs {SD_W:.2f}")
    print(f"\nOBSERVED: paid jobs -> higher ed {of:+.3f} (±{os_:.3f})"
          f"   |   higher ed -> paid jobs {ob:+.3f} (±{obs_:.3f})")

    tasks = [(w, s) for w in ("A", "B") for s in range(1200)]
    with Pool(48) as p:
        res = p.map(run_one, tasks, chunksize=16)
    for w, name in (("A", "chain"), ("B", "common cause")):
        R = np.array([[r[1], r[2], r[3], r[4]] for r in res if r[0] == w])
        fz = R[:, 0]
        print(f"\n--- World {name}  ({len(R)} panels)")
        print(f"  forward:  median {np.median(fz):+.3f}   5-95% {np.percentile(fz,5):+.3f} to {np.percentile(fz,95):+.3f}")
        print(f"  backward: median {np.median(R[:,2]):+.3f}   5-95% {np.percentile(R[:,2],5):+.3f} to {np.percentile(R[:,2],95):+.3f}")
        inside = np.mean((fz > of - 1.96 * os_) & (fz < of + 1.96 * os_))
        print(f"  share of panels inside the observed 95% interval: {100*inside:.1f}%")
    A = np.array([r[1] for r in res if r[0] == "A"])
    B = np.array([r[1] for r in res if r[0] == "B"])
    lo = max(np.percentile(A, 5), np.percentile(B, 5))
    hi = min(np.percentile(A, 95), np.percentile(B, 95))
    print("\n" + "=" * 70)
    print(f"  chain mean {A.mean():+.3f}   common-cause mean {B.mean():+.3f}")
    print(f"  overlap of 5-95% ranges: {max(hi - lo, 0):.3f}")
    print("  => the level " + ("CANNOT" if hi > lo else "CAN") + " separate the two worlds")
