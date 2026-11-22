#!/usr/bin/env python3
"""Does the top-down edge survive roads, marriage age, income, power, cities?

Progressive controls, within countries, 10-year changes.
"""
import json, os, gzip
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
V = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG}
     for k in ["ter", "sec", "lsc", "prm_cmp", "gdppc_log", "urban", "electricity",
               "wage_emp", "u5mr", "roads_paved", "married18", "pop"]}

BLOCKS = [("nothing", []),
          ("+ income", ["gdppc_log"]),
          ("+ power & cities", ["gdppc_log", "electricity", "urban"]),
          ("+ paid jobs", ["gdppc_log", "electricity", "urban", "wage_emp"]),
          ("+ child survival", ["gdppc_log", "electricity", "urban", "wage_emp", "u5mr"]),
          ("+ MARRIAGE AGE", ["gdppc_log", "electricity", "urban", "wage_emp", "u5mr", "married18"]),
          ("+ ROADS", ["gdppc_log", "electricity", "urban", "wage_emp", "u5mr", "roads_paved"]),
          ("+ everything", ["gdppc_log", "electricity", "urban", "wage_emp", "u5mr",
                            "married18", "roads_paved"])]


def near(v, iso, y, tol=5):
    for d in range(tol + 1):
        for yy in (y - d, y + d):
            if (iso, yy) in v:
                return v[(iso, yy)]
    return None


def run(outcome, ctrls):
    rows = []
    for (i, t), v in V[outcome].items():
        if (i, t + 10) not in V[outcome] or (i, t) not in V["ter"]:
            continue
        rec = [i, t, V[outcome][(i, t + 10)] - v, V["ter"][(i, t)], v]
        ok = True
        for c in ctrls:
            x = V[c].get((i, t))
            if x is None:
                x = near(V[c], i, t, tol=12)
            if x is None:
                vals = [vv for (ii, yy), vv in V[c].items() if ii == i]
                x = float(np.mean(vals)) if vals else None
            if x is None:
                ok = False
                break
            rec.append(x)
        if ok:
            rows.append(rec)
    if len(rows) < 60:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    gy = np.array([(r[1] // 10) * 10 for r in rows])
    y = np.array([r[2] for r in rows])
    cols = [np.array([r[3] for r in rows]), np.array([r[4] for r in rows])]
    cols += [np.array([r[5 + j] for r in rows]) for j in range(len(ctrls))]
    X = np.column_stack([np.ones(len(y))] + cols)

    def dm(a, g):
        s = np.bincount(g, weights=a); c = np.bincount(g)
        return a - (s / np.maximum(c, 1))[g]

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
    return float(b[1]), se, len(rows), len(ui)


for outcome, label in (("prm_cmp", "PRIMARY completion"),
                       ("lsc", "LOWER-secondary completion"),
                       ("sec", "UPPER-secondary completion")):
    print("\n" + "=" * 78)
    print(f"EFFECT OF HIGHER-ED GROWTH ON {label}")
    print("=" * 78)
    for name, ctrls in BLOCKS:
        r = run(outcome, ctrls)
        if r is None:
            print(f"  {name:20s} (too few observations)")
            continue
        b, se, n, nc = r
        star = "**" if abs(b / se) > 1.96 else "  "
        print(f"  {name:20s} {b:+7.3f} (±{se:.3f}){star}  n={n:5d}, {nc:3d} countries")
