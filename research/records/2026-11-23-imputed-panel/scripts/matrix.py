#!/usr/bin/env python3
"""Step 5: the corrected lead-lag matrix (research/records/2026-11-23-recompute/scripts/full_matrix_trends.py, with true
log income), with and without country trends, on (a) observed data only and (b) the imputed panel 1950+, pooled
across the 20 imputations with Rubin's rules.  usage: matrix.py [NPROC]"""
import sys, json
import numpy as np
from multiprocessing import Pool
from common import *

IMPDIR = os.environ.get("IMP_DIR", "/root/work/data_imputed")
VARS = ["electricity", "wage_emp", "lsc", "sec", "ter", "prm_cmp", "gdppc_log", "urban", "tax", "agri_va", "emp_agri",
        "flfp", "life_exp", "u5mr", "gpi_sec", "gpi_ter", "fertility"]
CTRL = ["gdppc_log", "urban"]
M = 20
REGS = set(REG)
PAIRS = [(x, y) for x in VARS for y in VARS if x != y]


def loadset(d):
    S = {}
    for v in VARS:
        s = {k: x for k, x in load(v, d).items() if k[0] in REGS}
        if v == "gdppc_log":
            s = {k: float(np.log(x)) for k, x in s.items()}   # the file holds LEVELS
        S[v] = s
    return S


DS = {}


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def edge(args):
    ds, x, y, trend = args
    S = DS[ds]
    ctrls = [c for c in CTRL if c not in (x, y)]
    rows = []
    for (i, t), v in S[y].items():
        if (i, t + 10) not in S[y] or (i, t) not in S[x]:
            continue
        if not all((i, t) in S[c] for c in ctrls):
            continue
        rows.append([i, t, S[y][(i, t + 10)] - v, v, S[x][(i, t)]] + [S[c][(i, t)] for c in ctrls])
    if trend:
        cnt = {}
        for r in rows:
            cnt[r[0]] = cnt.get(r[0], 0) + 1
        rows = [r for r in rows if cnt[r[0]] >= 4]
    if len(rows) < 150 or len({r[0] for r in rows}) < 10:
        return (ds, x, y, trend, None)
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
    XtX = X.T @ X
    b = np.linalg.lstsq(XtX, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        mm = gi == c
        s = X[mm].T @ u[mm]
        meat += np.outer(s, s)
    P = np.linalg.pinv(XtX)
    Vb = P @ meat @ P
    return (ds, x, y, trend, (float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(yv), len(ui)))


if __name__ == "__main__":
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    DS["obs"] = loadset(DATA)
    for m in range(M):
        DS[f"m{m + 1:02d}"] = loadset(f"{IMPDIR}/m{m + 1:02d}")
    jobs = [(d, x, y, t) for d in DS for (x, y) in PAIRS for t in (False, True)]
    with Pool(nproc) as p:
        res = p.map(edge, jobs, chunksize=8)
    R = {(d, x, y, t): r for d, x, y, t, r in res if r}
    out = {"obs": {}, "imp": {}}
    for x, y in PAIRS:
        for t in (False, True):
            k = f"{x}|{y}|{int(t)}"
            r = R.get(("obs", x, y, t))
            if r:
                out["obs"][k] = r
            lst = [R[(f"m{m + 1:02d}", x, y, t)] for m in range(M) if (f"m{m + 1:02d}", x, y, t) in R]
            if len(lst) == M:
                b = np.array([a[0] for a in lst]); se = np.array([a[1] for a in lst])
                W = (se ** 2).mean(); B = b.var(ddof=1)
                T = W + (1 + 1 / M) * B
                lam = (1 + 1 / M) * B / T if T > 0 else 0
                out["imp"][k] = (float(b.mean()), float(np.sqrt(T)), lst[0][2], lst[0][3], float(lam))
    json.dump(out, open(f"{OUT}/matrix_results.json", "w"))
    print("done", len(out["obs"]), len(out["imp"]))
