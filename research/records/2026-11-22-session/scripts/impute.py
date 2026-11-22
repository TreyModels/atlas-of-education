#!/usr/bin/env python3
"""Longitudinal imputation, then re-run the bundle test.

Coverage problem: water and sanitation start in 2000, so a bundle test on complete
cases throws away most of the transition. Here each component is linearly
interpolated within country between observed points (never extrapolated), and
multiple imputation (M=20) adds noise calibrated to the real interpolation error,
so the pooled estimates carry imputation uncertainty as well as sampling error.
"""
import json, os, gzip
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
COMP = ["electricity", "water", "sanit", "internet"]
OUT = ["lsc", "sec", "ter", "pov_215"]
CTRL = ["gdppc_log", "urban"]
M = 20


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in COMP + OUT + CTRL}


def series(c, iso):
    return sorted((y, v) for (i, y), v in S[c].items() if i == iso)


# ---------- calibrate interpolation error from countries with dense data ----------
def loo_error(c, min_obs=20):
    errs = []
    for iso in {i for (i, t) in S[c]}:
        s = series(c, iso)
        if len(s) < min_obs:
            continue
        for k in range(1, len(s) - 1):
            y0, v0 = s[k - 1]; y1, v1 = s[k + 1]
            if y1 == y0:
                continue
            pred = v0 + (v1 - v0) * (s[k][0] - y0) / (y1 - y0)
            errs.append(s[k][1] - pred)
    return float(np.std(errs)) if len(errs) > 50 else None, len(errs)


SIGMA = {}
print("interpolation error, estimated leave-one-out on dense series:")
for c in COMP:
    sd, n = loo_error(c)
    SIGMA[c] = sd
    print(f"  {c:12s} sd = {sd:.3f}  (from {n} held-out observations)" if sd
          else f"  {c:12s} too few dense series")


def impute(c, rng):
    """linear interpolation within country, plus calibrated noise on filled years"""
    out = {}
    for iso in {i for (i, t) in S[c]}:
        s = series(c, iso)
        if len(s) < 2:
            continue
        for k in range(len(s) - 1):
            (y0, v0), (y1, v1) = s[k], s[k + 1]
            if y1 - y0 > 25:
                continue
            for y in range(y0, y1 + 1):
                if y in (y0, y1):
                    out[(iso, y)] = [v0, v1][y == y1]
                else:
                    v = v0 + (v1 - v0) * (y - y0) / (y1 - y0)
                    if SIGMA[c]:
                        v = v + rng.normal(0, SIGMA[c] * 0.5)
                    out[(iso, y)] = min(max(v, 0.0), 100.0)
    return out


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def fit(outcome, xmap, zmap=None):
    rows = []
    for (i, t), v in S[outcome].items():
        if (i, t + 10) not in S[outcome] or (i, t) not in xmap:
            continue
        rec = [i, t, S[outcome][(i, t + 10)] - v, v, xmap[(i, t)]]
        ok = True
        for c in CTRL:
            if (i, t) in S[c]:
                rec.append(S[c][(i, t)])
            else:
                ok = False
                break
        if ok:
            rows.append(rec)
    if len(rows) < 150:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    gy = np.array([(r[1] // 10) * 10 for r in rows])
    y = np.array([r[2] for r in rows])
    own = np.array([r[3] for r in rows])
    xx = np.array([r[4] for r in rows], float)
    cols = [xx, own] + [np.array([r[5 + j] for r in rows]) for j in range(len(CTRL))]
    X = np.column_stack([np.ones(len(y))] + cols)
    X = np.column_stack([dm(X[:, j], gi) for j in range(X.shape[1])])
    X = np.column_stack([dm(X[:, j], gy) for j in range(X.shape[1])])
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
    se = float(np.sqrt(max(Vb[1, 1], 0)))
    return float(b[1]), se, len(rows), len(ui), xx.std()


def zscores(d, mu, sd):
    return {k: (v - mu) / sd for k, v in d.items()}


print("\n" + "=" * 84)
print("COMPLETE CASES vs MULTIPLE IMPUTATION (M=20), lower-secondary completion")
print("=" * 84)
for out in OUT:
    row_cc, row_mi = [], []
    for label, c in (("electricity", "electricity"), ("bundle", None)):
        if c:
            xm = zscores(S[c], np.mean(list(S[c].values())), np.std(list(S[c].values())))
            r = fit(out, xm)
            row_cc.append((label, r))
        else:
            vals = {}
            for k in set().union(*[set(S[x]) for x in COMP]):
                vs = [S[x][k] for x in COMP if k in S[x]]
                if len(vs) >= 2:
                    vals[k] = np.mean(vs)
            xm = zscores(vals, np.mean(list(vals.values())), np.std(list(vals.values())))
            r = fit(out, xm)
            row_cc.append((label, r))
    # imputed
    rng = np.random.default_rng(11)
    acc = {k: [] for k in ("electricity", "bundle")}
    for m in range(M):
        imps = {c: impute(c, rng) for c in COMP}
        xe = zscores(imps["electricity"], np.mean(list(imps["electricity"].values())),
                     np.std(list(imps["electricity"].values())))
        r = fit(out, xe)
        if r:
            acc["electricity"].append(r)
        bundles = {}
        for k in set().union(*[set(imps[x]) for x in COMP]):
            vs = [imps[x][k] for x in COMP if k in imps[x]]
            if len(vs) >= 2:
                bundles[k] = np.mean(vs)
        xb = zscores(bundles, np.mean(list(bundles.values())), np.std(list(bundles.values())))
        r = fit(out, xb)
        if r:
            acc["bundle"].append(r)
    print(f"\n  {out}")
    for label, r in row_cc:
        if r:
            print(f"    complete cases  {label:12s} {r[0]:+8.3f} (±{r[1]:.3f})  "
                  f"n={r[2]:5d}, {r[3]:3d} countries")
    for label in ("electricity", "bundle"):
        lst = acc[label]
        if not lst:
            continue
        b = np.array([x[0] for x in lst]); se = np.array([x[1] for x in lst])
        qbar = b.mean()
        within = (se ** 2).mean()
        between = b.var(ddof=1) if len(b) > 1 else 0.0
        total = within + (1 + 1 / len(b)) * between
        t = qbar / np.sqrt(total) if total > 0 else 0
        print(f"    imputed (M={len(b):2d}) {label:12s} {qbar:+8.3f} (±{np.sqrt(total):.3f}) "
              f"{'*' if abs(t) > 1.96 else ' '}  n={lst[0][2]:5d}, {lst[0][3]:3d} countries")
