import os
#!/usr/bin/env python3
"""Boppart's mechanism, tested with measured prices.

Their claim: where investment goods are expensive relative to wages, farms stay
labour-intensive, so agricultural labour productivity is low and employment stays
on the farm. The mechanism variable is the relative price of capital goods, which
the Penn World Table measures directly.

Test: does the relative price of investment goods predict agricultural employment,
within countries, with and without country trends?
"""
import json, os, gzip
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
V = {}
for k in ["pwt_pli", "pwt_tfp", "pwt_labsh", "pwt_hc", "pwt_yw",
          "emp_agri", "agri_va", "wage_emp", "fertility", "lsc", "gdppc_log", "urban"]:
    try:
        V[k] = {kk: vv for kk, vv in load(k).items() if kk[0] in REG}
    except FileNotFoundError:
        print("missing", k)
print({k: len(v) for k, v in V.items()})


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def reg(outcome, xname, trend=False, ctrls=("gdppc_log",), lagx=0):
    rows = []
    for (i, t), v in V[outcome].items():
        if (i, t + 10) not in V[outcome] or (i, t - lagx) not in V[xname]:
            continue
        if not all((i, t) in V[c] for c in ctrls):
            continue
        rows.append([i, t, V[outcome][(i, t + 10)] - v, v, V[xname][(i, t - lagx)]] +
                    [V[c][(i, t)] for c in ctrls])
    if trend:
        cnt = {}
        for r in rows:
            cnt[r[0]] = cnt.get(r[0], 0) + 1
        rows = [r for r in rows if cnt[r[0]] >= 4]
    if len(rows) < 150 or len({r[0] for r in rows}) < 12:
        return None
    iso = [r[0] for r in rows]
    ui = {v2: n for n, v2 in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v2] for v2 in iso]); yr = np.array([r[1] for r in rows])
    gy = (yr // 10) * 10
    yv = np.array([r[2] for r in rows])
    cols = [np.array([r[4] for r in rows], float), np.array([r[3] for r in rows])] + \
           [np.array([r[5 + j] for r in rows], float) for j in range(len(ctrls))]
    if trend:
        for j in range(len(ui)):
            cols.append(((gi == j) * yr).astype(float))
    X = np.column_stack([np.ones(len(yv))] + cols)
    X = np.column_stack([dm(X[:, k], gi) for k in range(X.shape[1])])
    X = np.column_stack([dm(X[:, k], gy) for k in range(X.shape[1])])
    Y = dm(dm(yv, gi), gy)
    b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(yv), len(ui)


def show(tag, r):
    if not r:
        print(f"  {tag:46s} too few observations")
        return
    b, se, n, nc = r
    star = "*" if se > 0 and abs(b / se) > 1.96 else " "
    print(f"  {tag:46s} {b:+9.4f} (±{se:.4f}){star}  n={n:5d}, {nc:3d} countries")


print("\n" + "=" * 88)
print("DOES THE RELATIVE PRICE OF INVESTMENT GOODS PREDICT FARM EMPLOYMENT?")
print("(positive = expensive capital keeps people on the land, as Boppart predicts)")
print("=" * 88)
show("investment price -> farm share, FE only", reg("emp_agri", "pwt_pli", False))
show("investment price -> farm share, + country trends", reg("emp_agri", "pwt_pli", True))

print("\n  and on farm output share:")
show("investment price -> farm output, FE only", reg("agri_va", "pwt_pli", False))
show("investment price -> farm output, + trends", reg("agri_va", "pwt_pli", True))

print("\n" + "=" * 88)
print("THE INPUT-INTENSITY ELASTICITY (the parameter they estimate above unity)")
print("=" * 88)
rows = []
for (i, t), v in V["emp_agri"].items():
    if (i, t) not in V["pwt_pli"] or (i, t) not in V["pwt_yw"] or (i, t) not in V["pwt_labsh"]:
        continue
    p = V["pwt_pli"][(i, t)]
    w = V["pwt_yw"][(i, t)] * V["pwt_labsh"][(i, t)]   # labour income per worker
    if p > 0 and w > 0:
        rows.append([i, np.log(w / p), np.log(v / 100.0)])
if len(rows) > 200:
    iso = [r[0] for r in rows]
    ui = {v2: n for n, v2 in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v2] for v2 in iso])
    x = dm(np.array([r[1] for r in rows]), gi)
    y = dm(np.array([r[2] for r in rows]), gi)
    b = (x @ y) / (x @ x)
    res = y - b * x
    meat = 0.0
    for c in np.unique(gi):
        m = gi == c
        meat += float((x[m] @ res[m]) ** 2)
    se = np.sqrt(meat) / (x @ x)
    print(f"  elasticity of farm-employment share to the wage/capital-price ratio")
    print(f"  {b:+.4f} (±{se:.4f})  n={len(rows)}, {len(ui)} countries")
    print(f"  (a positive value means cheap capital pulls labour off the farm)")
