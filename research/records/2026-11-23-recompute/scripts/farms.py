import os
#!/usr/bin/env python3
"""Did the fall of farm employment kill fertility?

Tests: does the farm share predict the 10-year change in births, does it survive
controls, which direction does it run, and is the edge outside the common-cause band?
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
K = ["fertility", "emp_agri", "agri_va", "urban", "gdppc_log", "lsc", "u5mr", "wage_emp"]
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in K}
F = S["fertility"]


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def fit(y, x, own, gi, gy, extra=None):
    cols = [np.ones(len(y)), x, own] + ([e for e in extra] if extra else [])
    X = np.column_stack(cols)
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
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(y), len(np.unique(gi))


def panel(x, y, ctrls=()):
    rows = []
    for (i, t), v in S[y].items():
        if (i, t + 10) not in S[y] or (i, t) not in S[x]:
            continue
        r = [i, t, S[y][(i, t + 10)] - v, S[x][(i, t)], v]
        ok = True
        for c in ctrls:
            if (i, t) in S[c]:
                r.append(S[c][(i, t)])
            else:
                ok = False
                break
        if ok:
            rows.append(r)
    return rows


def run(x, y, ctrls=()):
    rows = panel(x, y, ctrls)
    if len(rows) < 100:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso]); gy = np.array([(r[1] // 10) * 10 for r in rows])
    yy = np.array([r[2] for r in rows]); xx = np.array([r[3] for r in rows])
    own = np.array([r[4] for r in rows])
    extra = [np.array([r[5 + j] for r in rows]) for j in range(len(ctrls))]
    return fit(yy, xx, own, gi, gy, extra)


print("=" * 78)
print("1. DOES THE FARM SHARE PREDICT THE FALL IN BIRTHS?")
print("   (positive = more farming goes with a SLOWER fall)")
print("=" * 78)
for lab, ctrls in (("nothing", ()),
                   ("+ income", ("gdppc_log",)),
                   ("+ cities", ("gdppc_log", "urban")),
                   ("+ schooling", ("gdppc_log", "urban", "lsc")),
                   ("+ child survival", ("gdppc_log", "urban", "lsc", "u5mr")),
                   ("+ paid jobs", ("gdppc_log", "urban", "lsc", "u5mr", "wage_emp"))):
    r = run("emp_agri", "fertility", ctrls)
    if r:
        print(f"  farm employment share   {lab:18s} {r[0]:+7.4f} (±{r[1]:.4f})"
              f"{'**' if abs(r[0]/r[1])>1.96 else '  '}  n={r[2]}, {r[3]} countries")

print()
print("  farm OUTPUT share (value added) instead:")
for lab, ctrls in (("nothing", ()), ("+ income & cities", ("gdppc_log", "urban")),
                   ("+ schooling & survival", ("gdppc_log", "urban", "lsc", "u5mr"))):
    r = run("agri_va", "fertility", ctrls)
    if r:
        print(f"  farm output share       {lab:18s} {r[0]:+7.4f} (±{r[1]:.4f})"
              f"{'**' if abs(r[0]/r[1])>1.96 else '  '}  n={r[2]}, {r[3]} countries")

print()
print("=" * 78)
print("2. WHICH DIRECTION?")
print("=" * 78)
a = run("emp_agri", "fertility")
b = run("fertility", "emp_agri")
print(f"  farm share -> births:     {a[0]:+8.4f} (±{a[1]:.4f})")
print(f"  births -> farm share:     {b[0]:+8.4f} (±{b[1]:.4f})")

print()
print("=" * 78)
print("3. DOES IT BEAT THE OTHER CANDIDATES? (all in one model)")
print("=" * 78)
rows = panel("emp_agri", "fertility")
keep = []
for r in rows:
    i, t = r[0], r[1]
    if all((i, t) in S[c] for c in ("gdppc_log", "urban", "lsc", "u5mr", "wage_emp")):
        keep.append(r + [S["gdppc_log"][(i, t)], S["urban"][(i, t)],
                         S["lsc"][(i, t)], S["u5mr"][(i, t)], S["wage_emp"][(i, t)]])
if len(keep) > 100:
    iso = [r[0] for r in keep]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso]); gy = np.array([(r[1] // 10) * 10 for r in keep])
    yy = np.array([r[2] for r in keep])
    names = ["farm share", "own births", "income", "cities", "schooling", "child survival", "paid jobs"]
    cols = [np.array([r[3 + j] for r in keep]) for j in range(7)]
    X = np.column_stack([np.ones(len(yy))] + cols)
    Xd = np.column_stack([dm(X[:, j], gi) for j in range(X.shape[1])])
    Xd = np.column_stack([dm(Xd[:, j], gy) for j in range(Xd.shape[1])])
    Y = dm(dm(yy, gi), gy)
    bb = np.linalg.lstsq(Xd.T @ Xd, Xd.T @ Y, rcond=None)[0]
    u = Y - Xd @ bb
    XtX = Xd.T @ Xd
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = Xd[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    se = np.sqrt(np.maximum(np.diag(Vb), 0))
    print(f"  n={len(keep)}, {len(np.unique(gi))} countries")
    for j, nm in enumerate(names):
        k = 1 + j
        print(f"    {nm:16s} {bb[k]:+9.4f}  (±{se[k]:.4f}) {'**' if abs(bb[k]/se[k])>1.96 else ''}")
