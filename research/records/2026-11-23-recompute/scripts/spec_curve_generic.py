import os
#!/usr/bin/env python3
"""The specification curve: every defensible way to run the headline test.

Headline: paid employment -> 10-year change in tertiary enrolment.
Varies: lag, control set (all subsets of five), fixed effects, sample, transform.
Also: leave-one-country-out jackknife, and an out-of-sample forecast test.
"""
import json, os, gzip, itertools
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
XV = os.environ.get("XV", "wage_emp"); YV = os.environ.get("YV", "ter")
CTRL = [c for c in ["gdppc_log", "urban", "electricity", "wage_emp", "lsc", "ter", "u5mr"] if c not in (XV, YV)][:5]
K = sorted(set([XV, YV, "gdppc_log"] + CTRL))
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in K}
TER = S[YV]
LAGS = [0, 5, 10, 15]
FES = ["country", "country+decade", "country+trend"]
SAMPLES = ["all", "non-rich", "post1980"]
TRANS = ["level", "log"]

SER = {}
for (i, t) in TER:
    SER.setdefault(i, []).append(t)
for i in SER:
    SER[i] = sorted(SER[i])


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
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(y), len(np.unique(gi))


def run(spec):
    lag, ctrls, fe, sample, trans, drop = spec
    rows = []
    for i in SER:
        if drop is not None and i == drop:
            continue
        if sample == "non-rich" and REG[i] in ("North America", "Europe & Central Asia"):
            continue
        for t in SER[i]:
            if t < 1980 and sample == "post1980":
                continue
            if (i, t + 10) not in TER or (i, t - lag) not in S[XV]:
                continue
            ok = True
            for c in ctrls:
                if (i, t - lag) not in S[c]:
                    ok = False
                    break
            if not ok:
                continue
            y0, y1 = TER[(i, t)], TER[(i, t + 10)]
            if trans == "log":
                if y0 <= 0.05 or y1 <= 0.05:
                    continue
                dy = np.log(y1) - np.log(y0)
            else:
                dy = y1 - y0
            rows.append((i, t, dy, S[XV][(i, t - lag)], y0,
                         [S[c][(i, t - lag)] for c in ctrls]))
    if len(rows) < 150:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    gy = np.array([(r[1] // 10) * 10 for r in rows])
    y = np.array([r[2] for r in rows]); x = np.array([r[3] for r in rows])
    own = np.array([r[4] for r in rows])
    extra = [np.array([r[5][j] for r in rows]) for j in range(len(ctrls))]
    cols = [x, own] + extra
    n = len(y)
    X = np.column_stack([np.ones(n)] + cols)
    X = np.column_stack([dm(X[:, j], gi) for j in range(X.shape[1])])
    if fe == "country+trend":
        yr = np.array([r[1] for r in rows], float)
        T = np.column_stack([((gi == j) * yr) for j in range(len(ui))]).astype(float)
        X = np.column_stack([X, np.column_stack([dm(T[:, j], gi) for j in range(T.shape[1])])])
        Y = dm(y, gi)
    elif fe == "country+decade":
        X = np.column_stack([dm(X[:, j], gy) for j in range(X.shape[1])])
        Y = dm(dm(y, gi), gy)
    else:
        Y = dm(y, gi)
    b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), n, len(ui)


def task(spec):
    r = run(spec)
    return None if r is None else (spec, r)


if __name__ == "__main__":
    specs = []
    for lag in LAGS:
        for k in range(6):
            for sub in itertools.combinations(CTRL, k):
                for fe in FES:
                    for sample in SAMPLES:
                        for tr in TRANS:
                            specs.append((lag, sub, fe, sample, tr, None))
    print(f"X={XV} Y={YV} controls={CTRL}\nspecifications defined:", len(specs), flush=True)
    with Pool(int(os.environ.get("NP","24"))) as p:
        res = [r for r in p.map(task, specs, chunksize=10) if r]

    b = np.array([r[1][0] for r in res]); se = np.array([r[1][1] for r in res])
    print("\n" + "=" * 74)
    print("THE HEADLINE RESULT ACROSS EVERY DEFENSIBLE SPECIFICATION")
    print("=" * 74)
    print(f"  specifications estimable: {len(b):,} of {len(specs):,} defined")
    print(f"  median estimate:       {np.median(b):+.3f}")
    print(f"  middle 50%:            {np.percentile(b,25):+.3f} to {np.percentile(b,75):+.3f}")
    print(f"  range (5-95%):         {np.percentile(b,5):+.3f} to {np.percentile(b,95):+.3f}")
    print(f"  positive in:           {100*np.mean(b>0):.1f}% of specifications")
    print(f"  significant & positive:{100*np.mean((b>0)&(b/se>1.96)):.1f}%")
    print(f"  significant & negative:{100*np.mean((b<0)&(b/se<-1.96)):.1f}%")

    for fe_ in FES:
        bb=np.array([r[1][0] for r in res if r[0][2]==fe_]); ss=np.array([r[1][1] for r in res if r[0][2]==fe_])
        print(f"  [{fe_:15s}] n={len(bb):4d} median {np.median(bb):+.3f}  sig&pos {100*np.mean((bb>0)&(bb/ss>1.96)):.1f}%  sig&neg {100*np.mean((bb<0)&(bb/ss<-1.96)):.1f}%")
    print("  (units: 'level' specs are in outcome points per point of X; 'log' specs are in log points per point of X, so medians must not be pooled across transforms; t-statistics are unit-free)")
    for tr_ in TRANS:
        sel = [(r[1][0], r[1][1]) for r in res if r[0][4] == tr_]
        bb = np.array([a for a, _ in sel]); ss = np.array([c for _, c in sel])
        tt = bb / np.where(ss > 0, ss, np.nan)
        print(f"  [transform {tr_:5s}] n={len(bb):4d} median b {np.median(bb):+.3f}  median t {np.nanmedian(tt):+.2f}  sig&pos {100*np.mean((bb>0)&(tt>1.96)):.1f}%  sig&neg {100*np.mean((bb<0)&(tt<-1.96)):.1f}%")
    for tr_ in TRANS:
        for fe_ in FES:
            sel = [(r[1][0], r[1][1]) for r in res if r[0][4] == tr_ and r[0][2] == fe_]
            bb = np.array([a for a, _ in sel]); ss = np.array([c for _, c in sel]); tt = bb / np.where(ss > 0, ss, np.nan)
            print(f"  [{tr_:5s} x {fe_:15s}] n={len(bb):4d} median b {np.median(bb):+.3f}  sig&pos {100*np.mean((bb>0)&(tt>1.96)):.1f}%  sig&neg {100*np.mean((bb<0)&(tt<-1.96)):.1f}%")
    print("\n  which analyst choices move the answer:")
    labels = ["lag", "controls", "fixed effects", "sample", "transform"]
    for j, lab in enumerate(labels):
        vals = {}
        for spec, r in res:
            key = str(spec[j]) if j != 1 else f"{len(spec[1])} controls"
            vals.setdefault(key, []).append(r[0])
        line = "   ".join(f"{k}: {np.median(v):+.2f}" for k, v in sorted(vals.items()))
        print(f"    {lab:14s} {line}")

    # ---- jackknife ----
    print("\n" + "=" * 74)
    print("LEAVE-ONE-COUNTRY-OUT")
    print("=" * 74)
    base = run((0, ("gdppc_log", "urban"), "country+decade", "all", "level", None))
    print(f"  full sample: {base[0]:+.3f} (±{base[1]:.3f})")
    jk = []
    for iso in sorted(SER):
        r = run((0, ("gdppc_log", "urban"), "country+decade", "all", "level", iso))
        if r:
            jk.append((iso, r[0]))
    jk.sort(key=lambda z: z[1])
    print(f"  dropping one country changes it to: {jk[0][1]:+.3f} ({jk[0][0]}) "
          f"to {jk[-1][1]:+.3f} ({jk[-1][0]})")
    print("  most influential (largest upward pull when dropped):")
    for iso, v in jk[-3:][::-1]:
        print(f"    drop {iso}: {v:+.3f}")
    print("  most influential (largest downward pull when dropped):")
    for iso, v in jk[:3]:
        print(f"    drop {iso}: {v:+.3f}")
    print(f"  share of the {len(jk)} jackknife estimates that stay positive: "
          f"{100*np.mean([v>0 for _, v in jk]):.1f}%")
