#!/usr/bin/env python3
"""Every defensible specification, all at once.

Focus: does girls' lower-secondary completion predict the subsequent fall in births?
Varies: measurement lag, control set (all 64 subsets of 6), fixed effects,
        sample, start period, transform.  Reports the distribution of the answer.
"""
import json, os, gzip, itertools, random, statistics
from multiprocessing import Pool
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

CTRL = ["gdppc_log", "urban", "u5mr", "ter", "flfp", "electricity"]
LAGS = [0, 5, 10, 15, 20, 25]
FES = ["none", "country", "country+decade", "country+year"]
STARTS = [0, 1970, 1980, 1990]
TRANS = ["level", "log"]


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}

S = {k: load(k) for k in ["fertility", "lsc"] + CTRL}
for k in S:
    S[k] = {kk: vv for kk, vv in S[k].items() if kk[0] in REG}
F = S["fertility"]

REGIONS = sorted(set(REG.values()))
SAMPLES = [("all", None), ("no rich", "no_rich")] + [("only " + r.split("&")[0].strip(), r) for r in REGIONS]

# pre-extract fertility series per country
FERT = {}
for (i, t), v in F.items():
    FERT.setdefault(i, {})[t] = v
for i in FERT:
    FERT[i] = dict(sorted(FERT[i].items()))


def build(
    lag=10, ctrls=("gdppc_log", "urban"), fe="country", start=0, transform="level",
    sample="all", horizon=10,
):
    rows = []
    for iso, ser in FERT.items():
        if sample == "no_rich" and REG[iso] in ("North America", "Europe & Central Asia"):
            continue
        if sample not in ("all", "no_rich") and REG[iso] != sample:
            continue
        for t, v0 in ser.items():
            if (t - lag) < start or (t + horizon) not in ser:
                continue
            bx = S["lsc"].get((iso, t - lag))
            if bx is None:
                continue
            cs = []
            ok = True
            for c in ctrls:
                val = S[c].get((iso, t - lag))
                if val is None:
                    ok = False
                    break
                cs.append(val)
            if not ok:
                continue
            y = ser[t + horizon] - v0
            if transform == "log":
                a, b = max(ser[t + horizon], 0.05), max(v0, 0.05)
                y = np.log(b) - np.log(a)
            rows.append((iso, t, y, bx, cs))
    return rows


def fit(rows, fe):
    n = len(rows)
    if n < 80:
        return None
    iso = [r[0] for r in rows]
    yr = [r[1] for r in rows]
    y = np.array([r[2] for r in rows], float)
    x = np.array([r[3] for r in rows], float)
    cs = np.array([r[4] for r in rows], float) if rows[0][4] else np.zeros((n, 0))
    ui = {v: k for k, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    cols = [np.ones(n), x]
    if cs.shape[1]:
        cols += [cs[:, j] for j in range(cs.shape[1])]
    if fe in ("country", "country+decade", "country+year"):
        nd = n - len(set(iso))
        if nd < 60:
            return None
        for c in sorted(set(iso))[1:]:
            cols.append((gi == ui[c]).astype(float))
    if fe == "country+year":
        uy = {v: k for k, v in enumerate(sorted(set(yr)))}
        gy = np.array([uy[v] for v in yr])
        for c in sorted(set(yr))[1:]:
            cols.append((gy == uy[c]).astype(float))
    elif fe == "country+decade":
        gy = np.array([y2 // 10 for y2 in yr])
        for c in sorted(set(gy))[1:]:
            cols.append((gy == c).astype(float))
    X = np.column_stack(cols)
    if X.shape[1] >= n - 20:
        return None
    XtX = X.T @ X
    b = np.linalg.lstsq(XtX, X.T @ y, rcond=None)[0]
    u = y - X @ b
    # cluster by country
    meat = np.zeros_like(XtX)
    order = np.argsort(gi, kind="stable")
    Xs, us, gs = X[order], u[order], gi[order]
    bounds = np.flatnonzero(np.diff(gs)) + 1
    for block in np.split(np.arange(n), bounds):
        s = Xs[block].T @ us[block]
        meat += np.outer(s, s)
    try:
        XtXi = np.linalg.pinv(XtX)
        V = XtXi @ meat @ XtXi
        se = float(np.sqrt(max(V[1, 1], 0)))
    except Exception:
        return None
    return float(b[1]), se, n, len(set(iso))


def one(spec):
    lag, ctrls, fe, start, transform, sample = spec
    rows = build(lag=lag, ctrls=ctrls, fe=fe, start=start, transform=transform, sample=sample)
    out = fit(rows, fe)
    if out is None:
        return None
    b, se, n, nc = out
    return (lag, len(ctrls), fe, start, transform, sample, b, se, n, nc)


if __name__ == "__main__":
    specs = []
    for lag in LAGS:
        for k in range(7):
            for sub in itertools.combinations(CTRL, k):
                for fe in FES:
                    for start in STARTS:
                        for tr in TRANS:
                            for nm, sm in SAMPLES[:2]:
                                specs.append((lag, sub, fe, start, tr, sm))
    print("specifications to run:", len(specs), flush=True)
    with Pool(48) as p:
        res = [r for r in p.map(one, specs, chunksize=20) if r]
    print("usable:", len(res), flush=True)
    json.dump(res, open("/root/spec_results.json", "w"))

    b = np.array([r[6] for r in res])
    se = np.array([r[7] for r in res])
    z = b / se
    print()
    print("=" * 70)
    print("THE ANSWER, ACROSS EVERY DEFENSIBLE SPECIFICATION")
    print("=" * 70)
    print(f"  specifications run:        {len(b):,}")
    print(f"  median estimate:           {np.median(b):+.4f}")
    print(f"  middle 50% of estimates:   {np.percentile(b,25):+.4f} to {np.percentile(b,75):+.4f}")
    print(f"  negative in:               {100*np.mean(b<0):.1f}% of specifications")
    print(f"  significant (either way):  {100*np.mean(np.abs(z)>1.96):.1f}%")
    print(f"  significant AND negative:  {100*np.mean((b<0)&(z<-1.96)):.1f}%")
    print(f"  significant AND positive:  {100*np.mean((b>0)&(z>1.96)):.1f}%")

    print()
    print("  distribution of the estimate (each column = 2% of specs)")
    lo, hi = np.percentile(b, 1), np.percentile(b, 99)
    edges = np.linspace(lo, hi, 51)
    counts, _ = np.histogram(b, bins=edges)
    for i, c in enumerate(counts):
        if c:
            print(f"   {edges[i]:+.3f} |" + "#" * int(60 * c / counts.max()))
    print()

    print("=" * 70)
    print("WHICH ANALYST CHOICES MOVE THE ANSWER")
    print("=" * 70)
    labels = ["lag", "controls", "fixed effects", "start year", "transform", "sample"]
    for j, lab in enumerate(labels):
        print(f"\n  {lab}:")
        vals = {}
        for r in res:
            vals.setdefault(str(r[j]), []).append(r[6])
        for k2 in sorted(vals, key=lambda z: -np.median(vals[z])):
            v = np.array(vals[k2])
            print(f"    {k2:22s} median {np.median(v):+.4f}   n={len(v):,}")
