#!/usr/bin/env python3
"""Extended lead-lag matrix on the gap-filled panel.

Runs the same edge estimator as 2026-11-23-imputed-panel/scripts/matrix.py, but keeps
every per-imputation estimate (not only Rubin's pooled answer), adds an
observed-cells-only run and a future-treatment placebo (the supposed cause is measured
20 years AFTER the outcome window, so it cannot cause the change).

Outputs <OUT>/matrix_ext.json.  usage: matrix_ext.py [NPROC]
"""
import sys, json, os
import numpy as np
from multiprocessing import Pool
from common import *

IMPDIR = os.environ.get("IMP_DIR", "/root/work/data_imputed")
OUT = os.environ.get("ATLAS_OUT", "/root/work/impute/out")
VARS = ["electricity", "wage_emp", "lsc", "sec", "ter", "prm_cmp", "gdppc_log", "urban", "tax", "agri_va", "emp_agri",
        "flfp", "life_exp", "u5mr", "gpi_sec", "gpi_ter", "fertility"]
CTRL = ["gdppc_log", "urban"]
M = 20
REGS = set(REG)
PAIRS = [(x, y) for x in VARS for y in VARS if x != y]
EDU = ["lsc", "sec", "ter", "prm_cmp", "gpi_sec", "gpi_ter"]
# series that differ across the 20 imputations (the six modelled education series).
# fertility/life_exp/u5mr/urban/gdppc_log are identical in every imputation (long-run fill only).
MODELED = EDU


def loadset(d):
    S = {}
    for v in VARS:
        s = {k: x for k, x in load(v, d).items() if k[0] in REGS}
        if v == "gdppc_log":
            s = {k: float(np.log(x)) for k, x in s.items()}   # the files hold LEVELS
        S[v] = s
    return S


def load_flags():
    F = {}
    for v in VARS:
        p = f"{IMPDIR}/flags/{v}.json"
        if os.path.exists(p):
            F[v] = {(r[0], int(r[1])) for r in json.load(open(p)) if int(r[2]) == 0}
        else:
            F[v] = None       # series without flags is copied unchanged from observed data
    return F


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def edge(args):
    ds, x, y, trend, xlag = args
    S = DS[ds]
    ctrls = [c for c in CTRL if c not in (x, y)]
    rows = []
    for (i, t), v in S[y].items():
        tt = t + xlag
        if (i, t + 10) not in S[y] or (i, tt) not in S[x]:
            continue
        if not all((i, t) in S[c] for c in ctrls):
            continue
        rows.append([i, t, S[y][(i, t + 10)] - v, v, S[x][(i, tt)]] + [S[c][(i, t)] for c in ctrls])
    if trend:
        cnt = {}
        for r in rows:
            cnt[r[0]] = cnt.get(r[0], 0) + 1
        rows = [r for r in rows if cnt[r[0]] >= 4]
    if len(rows) < 150 or len({r[0] for r in rows}) < 10:
        return (ds, x, y, trend, xlag, None)
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
    return (ds, x, y, trend, xlag, (float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(yv), len(ui)))


DS = {}


def rubin(lst):
    """Rubin's rules over the 20 imputations -> (mean_b, total_se, n, nc, lambda, W, B)"""
    b = np.array([a[0] for a in lst]); se = np.array([a[1] for a in lst])
    W = (se ** 2).mean(); B = b.var(ddof=1); T = W + (1 + 1 / M) * B
    lam = (1 + 1 / M) * B / T if T > 0 else 0.0
    return (float(b.mean()), float(np.sqrt(T)), lst[0][2], lst[0][3], float(lam), float(W), float(B))


if __name__ == "__main__":
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    FLAG = load_flags()
    DS["obs"] = loadset(DATA)
    DS["mean"] = loadset(f"{IMPDIR}/mean")
    DS["obsonly"] = {}
    m01 = loadset(f"{IMPDIR}/m01")
    for v in VARS:
        DS["obsonly"][v] = m01[v] if FLAG[v] is None else {k: x for k, x in m01[v].items() if k in FLAG[v]}
    # share series that do not change across imputations (memory)
    for m in range(M):
        dd = loadset(f"{IMPDIR}/m{m + 1:02d}")
        DS[f"m{m + 1:02d}"] = {v: (dd[v] if v in MODELED else m01[v]) for v in VARS}

    base = [(ds, x, y, t, 0) for ds in DS for (x, y) in PAIRS for t in (False, True)]
    plac = [(ds, x, y, t, 20) for ds in (["obs", "mean"] + [f"m{m + 1:02d}" for m in range(M)])
            for (x, y) in PAIRS for t in (False, True)]
    print(f"jobs: main {len(base)}, placebo {len(plac)}", flush=True)
    with Pool(nproc) as p:
        R1 = p.map(edge, base, chunksize=8)
        print("main done", flush=True)
        R2 = p.map(edge, plac, chunksize=8)
        print("placebo done", flush=True)
    RES = {(ds, x, y, int(t), xlag): r for ds, x, y, t, xlag, r in R1 + R2 if r}

    def get(ds, x, y, t, xlag=0):
        return RES.get((ds, x, y, int(t), xlag))

    out = {"meta": {"M": M, "vars": VARS, "n_proc": nproc}, "main": {}, "placebo": {}}
    for x, y in PAIRS:
        for t in (False, True):
            k = f"{x}|{y}|{int(t)}"
            cell = {}
            for ds in ("obs", "mean", "obsonly"):
                r = get(ds, x, y, t)
                if r: cell[ds] = list(r)
            per = [get(f"m{m + 1:02d}", x, y, t) for m in range(M)]
            per = [list(pp) if pp else None for pp in per]
            if all(pp is not None for pp in per):
                cell["per"] = per
                cell["imp"] = list(rubin(per))
            out["main"][k] = cell
            pcell = {}
            r = get("obs", x, y, t, 20)
            if r: pcell["obs"] = list(r)
            r = get("mean", x, y, t, 20)
            if r: pcell["mean"] = list(r)
            per = [get(f"m{m + 1:02d}", x, y, t, 20) for m in range(M)]
            per = [list(pp) if pp else None for pp in per]
            if all(pp is not None for pp in per):
                pcell["per"] = per
                pcell["imp"] = list(rubin(per))
            out["placebo"][k] = pcell
    json.dump(out, open(f"{OUT}/matrix_ext.json", "w"), separators=(",", ":"))
    print("wrote", f"{OUT}/matrix_ext.json", os.path.getsize(f"{OUT}/matrix_ext.json") // 1024, "KB", flush=True)
