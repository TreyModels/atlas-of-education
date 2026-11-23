import os
#!/usr/bin/env python3
"""Designs 6c and 6d, plus E-values.

6d  LEAD TEST.  Does FUTURE electricity predict CURRENT schooling change?
                If yes, the "effect" is a pre-trend and the design is broken.
6c  NEGATIVE CONTROLS.  Electricity should not move tax collection or farm
                value added within a decade. If it does, the association is
                state capacity, not electricity.
6a  E-VALUES.   How strong would an unmeasured confounder have to be?
"""
import json, os, gzip
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUT = ["lsc", "sec", "ter"]
NEG = ["tax", "agri_va"]


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG}
     for k in ["electricity", "wage_emp", "lsc", "sec", "ter", "gdppc_log", "urban"] + NEG}


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def fit(outcome, xname, shift=0, ctrls=("gdppc_log", "urban")):
    """shift = 0 standard, +10 uses X measured at t+10 (a lead), -10 uses t-10."""
    rows = []
    for (i, t), v in S[outcome].items():
        if (i, t + 10) not in S[outcome]:
            continue
        if (i, t) not in S["electricity"] and xname == "electricity":
            continue
        xk = (i, t + shift)
        if xk not in S[xname]:
            continue
        rec = [i, t, S[outcome][(i, t + 10)] - v, v, S[xname][xk]]
        ok = all((i, t) in S[c] for c in ctrls)
        if not ok:
            continue
        rec += [S[c][(i, t)] for c in ctrls]
        rows.append(rec)
    if len(rows) < 150:
        return None
    iso = [r[0] for r in rows]
    ui = {v2: n for n, v2 in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v2] for v2 in iso]); gy = np.array([(r[1] // 10) * 10 for r in rows])
    y = np.array([r[2] for r in rows])
    cols = [np.array([r[4] for r in rows], float), np.array([r[3] for r in rows])]
    cols += [np.array([r[5 + j] for r in rows], float) for j in range(len(ctrls))]
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
    return float(b[1]), se, len(y), len(ui), cols[0].std(), Y.std()


print("=" * 84)
print("6d  LEAD TEST — does FUTURE electricity predict CURRENT schooling change?")
print("=" * 84)
print(f"{'outcome':10s}{'standard X(t)':>18s}{'lead X(t+10)':>18s}{'ratio':>9s}   verdict")
lead_store = {}
for o in OUT:
    r0 = fit(o, "electricity", 0)
    r1 = fit(o, "electricity", 10)
    if not r0 or not r1:
        print(f"{o:10s} insufficient data")
        continue
    ratio = r1[0] / r0[0] if r0[0] else float("nan")
    v = "PRE-TREND" if abs(ratio) > 0.5 else ("some" if abs(ratio) > 0.25 else "clean")
    print(f"{o:10s}{r0[0]:+9.3f}±{r0[1]:.2f}{r1[0]:+12.3f}±{r1[1]:.2f}{ratio:9.2f}   {v}")
    lead_store[o] = (r0, r1, ratio)

print("\n  same test for paid employment -> tertiary:")
r0 = fit("ter", "wage_emp", 0)
r1 = fit("ter", "wage_emp", 10)
if r0 and r1:
    print(f"    standard {r0[0]:+.3f}±{r0[1]:.2f}   lead {r1[0]:+.3f}±{r1[1]:.2f}   "
          f"ratio {r1[0]/r0[0] if r0[0] else float('nan'):.2f}")

print("\n" + "=" * 84)
print("6c  NEGATIVE CONTROLS — should be nothing")
print("=" * 84)
for o in NEG:
    r = fit(o, "electricity", 0, ctrls=("gdppc_log", "urban"))
    if r:
        print(f"  electricity -> {o:10s} {r[0]:+9.4f} (±{r[1]:.4f})"
              f"{'  *** SIGNIFICANT — warning' if abs(r[0]/r[1]) > 1.96 else '  clean'}  n={r[2]}")

print("\n" + "=" * 84)
print("6a  E-VALUES — how strong must a confounder be to explain this away?")
print("=" * 84)


def evalue(d):
    rr = np.exp(0.91 * abs(d))
    return rr + np.sqrt(rr * (rr - 1))


rows = [("electricity -> lower-sec", "lsc", "electricity"),
        ("electricity -> upper-sec", "sec", "electricity"),
        ("paid jobs -> tertiary", "ter", "wage_emp")]
for lab, o, x in rows:
    r = fit(o, x, 0)
    if not r:
        continue
    b, se, n, nc, sdx, sdy = r
    d = b * sdx / sdy
    dlo = (b - 1.96 * se) * sdx / sdy
    print(f"  {lab:26s} standardised d = {d:+.3f}   "
          f"E-value (point) {evalue(d):5.2f}   E-value (CI bound) {evalue(dlo):5.2f}")
print("\n  Reading: the E-value is the factor by which an unmeasured confounder would")
print("  have to be associated with BOTH the predictor and the outcome, above the")
print("  measured covariates, to reduce the estimate to zero. The CI-bound column is")
print("  the honest one.")
