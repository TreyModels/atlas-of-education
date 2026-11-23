import os
#!/usr/bin/env python3
"""Experiment 2: run every candidate driver through the common-cause filter."""
import json, os, gzip
from multiprocessing import Pool
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
XK = ["wage_emp", "urban", "electricity", "gdppc_log", "u5mr",
      "prm_cmp", "lsc", "sec", "flfp", "life_exp"]


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in XK + ["ter"]}
TER = S["ter"]

SER = {}
for (i, t) in TER:
    SER.setdefault(i, []).append(t)
for i in SER:
    SER[i] = sorted(SER[i])


def within_sd(vals, gi):
    s = np.bincount(gi, weights=vals); c = np.bincount(gi)
    return (vals - (s / c)[gi]).std()


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


SCAFF = {}
for x in XK:
    pr = [(i, t) for i in SER for t in SER[i]
          if (i, t + 10) in TER and (i, t + 10) in S[x] and (i, t) in S[x]]
    pr.sort()
    if len(pr) < 300:
        continue
    iso = [p[0] for p in pr]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    gy = np.array([(p[1] // 10) * 10 for p in pr])
    yt = np.array([TER[p] for p in pr])
    yt10 = np.array([TER[(p[0], p[1] + 10)] for p in pr])
    xv = np.array([S[x][p] for p in pr])
    sdT, sdX = within_sd(yt, gi), within_sd(xv, gi)
    if sdX == 0:
        continue
    obs = fit(yt10 - yt, (xv - xv.mean()) / sdX, yt, gi, gy)
    SCAFF[x] = dict(pr=pr, gi=gi, gy=gy, yt=yt, yt10=yt10, sdT=sdT, sdX=sdX,
                    obs=obs, ser={i: SER[i] for i in set(iso)})


def simulate(arg):
    x, world, seed = arg
    D0 = SCAFF[x]
    rng = np.random.default_rng(seed)
    sdT, sdX = D0["sdT"], D0["sdX"]
    tval, xval = {}, {}
    for iso, years in D0["ser"].items():
        n = len(years)
        if world == "B":
            Dv = np.cumsum(rng.normal(0, 1, n))
            e = np.zeros(n); w = np.zeros(n)
            for k in range(n):
                dD = Dv[k] - (Dv[k - 1] if k else 0.0)
                w[k] = (w[k - 1] if k else 0.0) + sdX * 0.45 * dD + rng.normal(0, sdX * 0.3)
                e[k] = (e[k - 1] if k else 0.0) + sdT * 0.020 * dD + rng.normal(0, sdT * 0.3)
        else:
            v = 0.0; F = np.zeros(n)
            for k in range(n):
                v = 0.9 * v + rng.normal(0, 1)
                F[k] = v
            w = np.zeros(n); e = np.zeros(n)
            for k in range(n):
                tgt = 0.9 * F[k] * sdX
                w[k] = (w[k - 1] if k else 0.0) + 0.35 * (tgt - (w[k - 1] if k else 0.0)) + rng.normal(0, sdX * 0.3)
                tt = 1.6 * (w[k] / (sdX + 1e-9)) * sdT
                e[k] = (e[k - 1] if k else 0.0) + 0.20 * (tt - (e[k - 1] if k else 0.0)) + rng.normal(0, sdT * 0.45)
        for k, y in enumerate(years):
            tval[(iso, y)] = e[k]
            xval[(iso, y)] = w[k]
    pr = D0["pr"]
    yt = np.array([tval[p] for p in pr]); yt10 = np.array([tval[(p[0], p[1] + 10)] for p in pr])
    xv = np.array([xval[p] for p in pr])
    sx = (xv - xv.mean()) / (np.std(xv) + 1e-9)
    b, se = fit(yt10 - yt, sx, yt, D0["gi"], D0["gy"])
    return x, world, b


if __name__ == "__main__":
    tasks = [(x, w, s) for x in SCAFF for w in ("A", "B") for s in range(400)]
    print("tasks:", len(tasks), flush=True)
    with Pool(48) as p:
        res = p.map(simulate, tasks, chunksize=20)
    store = {}
    for x, w, b in res:
        store.setdefault((x, w), []).append(b)
    print("\n" + "=" * 92)
    print("EVERY CANDIDATE DRIVER vs A PURE COMMON CAUSE")
    print("(points of higher-ed growth per SD of the driver)")
    print("=" * 92)
    print(f"{'driver':16s}{'observed':>12s}{'common-cause 95%':>24s}{'chain 95%':>22s}   verdict")
    for x in SCAFF:
        obs, se = SCAFF[x]["obs"]
        cc = np.array(store.get((x, "B"), [np.nan]))
        ch = np.array(store.get((x, "A"), [np.nan]))
        lo, hi = np.percentile(cc, 5), np.percentile(cc, 95)
        clo, chi = np.percentile(ch, 5), np.percentile(ch, 95)
        v = ("indistinguishable from trend" if lo <= obs <= hi
             else ("DIRECTIONAL" if clo <= obs <= chi else "outside both"))
        print(f"{x:16s}{obs:>+8.3f}±{se:.2f}{lo:>+10.2f} to {hi:+.2f}{clo:>+10.2f} to {chi:+.2f}   {v}")
