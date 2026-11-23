#!/usr/bin/env python3
"""Added-controls matrix: the 272 ordered links with child mortality and women's work added.

Estimator = the handoff-run full_matrix_trends.py (17 measures, ten-year changes, country effects,
decade effects, clustered errors), with income logged correctly (the handoff copy used income in
levels; the session contract and the recompute branch require the log).  Four control variants:
none (baseline), + child mortality, + women's work, + both; each with and without a straight-line
country trend.  Every variant is computed for every link; the mediator rule then decides which
added-control results may be reported.

Also returns, for each added control: its own coefficient and standard error, the OVB constant
a = (x-residual . c-residual)/(x-residual . x-residual) and SE(change) = |a| * SE(control
coefficient).  That is the exact standard error of "how much the x estimate would move if this
control were dropped", which gives the power check for unchanged links.

output: /root/work/controls/out/controls_results.json    usage: controls_matrix.py [NPROC]
"""
import sys, json, os
import numpy as np
from multiprocessing import Pool

DATA = "/root/work/data"
OUT = "/root/work/controls/out"
BASE = ["gdppc_log", "urban"]
VARS = ["electricity", "wage_emp", "lsc", "sec", "ter", "prm_cmp", "gdppc_log", "urban", "tax", "agri_va",
        "emp_agri", "flfp", "life_exp", "u5mr", "gpi_sec", "gpi_ter", "fertility"]
PAIRS = [(x, y) for x in VARS for y in VARS if x != y]
ADDONS = [(), ("u5mr",), ("flfp",), ("u5mr", "flfp")]

# ---- direct, plausible causal edges (one step) among the 17 measures; used only to apply the
# "a control that lies on the x -> y path is a mediator and must not be used" rule.  Deliberately
# conservative: only well-established development channels, not every correlation.
DIRECT = {
    "electricity": ["lsc", "sec", "ter", "prm_cmp", "gpi_sec", "gpi_ter", "wage_emp", "gdppc_log", "urban", "u5mr", "life_exp", "flfp"],
    "wage_emp": ["gdppc_log", "urban", "flfp", "fertility"],
    "lsc": ["sec", "prm_cmp", "gpi_sec", "gpi_ter", "wage_emp", "flfp", "fertility", "u5mr", "life_exp", "gdppc_log"],
    "sec": ["ter", "wage_emp", "flfp", "fertility", "u5mr", "life_exp", "gdppc_log"],
    "ter": ["wage_emp", "flfp", "fertility", "u5mr", "life_exp", "gdppc_log"],
    "prm_cmp": ["sec", "ter", "gpi_sec", "gpi_ter", "wage_emp", "flfp", "fertility", "u5mr", "life_exp"],
    "gpi_sec": ["gpi_ter", "sec", "ter", "wage_emp", "flfp", "fertility", "u5mr", "life_exp"],
    "gpi_ter": ["wage_emp", "flfp", "fertility", "u5mr", "life_exp"],
    "gdppc_log": ["urban", "life_exp", "u5mr", "fertility", "electricity", "wage_emp", "flfp", "lsc", "sec", "ter", "agri_va"],
    "urban": ["electricity", "wage_emp", "lsc", "sec", "ter", "gdppc_log", "flfp", "u5mr", "life_exp", "fertility"],
    "tax": ["electricity", "lsc", "sec", "ter", "gdppc_log", "u5mr", "life_exp"],
    "agri_va": ["emp_agri", "gdppc_log", "urban", "u5mr", "life_exp", "fertility", "wage_emp"],
    "emp_agri": ["agri_va", "gdppc_log", "urban", "u5mr", "life_exp", "wage_emp"],
    "flfp": ["fertility", "gdppc_log", "u5mr", "life_exp"],
    "life_exp": ["fertility", "u5mr", "gdppc_log"],
    "u5mr": ["fertility", "life_exp"],
    "fertility": ["lsc", "sec", "ter", "gdppc_log", "urban", "u5mr", "life_exp", "flfp", "electricity"],
}


def mediator(x, y, c):
    """c is on a two-step causal path x -> c -> y (x causes c, c causes y)."""
    return c in DIRECT.get(x, []) and y in DIRECT.get(c, [])


def load(n):
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(open(os.path.join(DATA, n + ".json"))) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i for i, m in meta.items() if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {}
for v in VARS:
    S[v] = {k: x for k, x in load(v).items() if k[0] in REG}
S["gdppc_log"] = {k: float(np.log(x)) for k, x in S["gdppc_log"].items()}   # the file holds LEVELS


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def edge(args):
    x, y, trend, addon = args
    ctrls = [c for c in BASE if c not in (x, y)] + [c for c in addon if c not in (x, y)]
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
        return (x, y, trend, addon, None)
    iso = [r[0] for r in rows]
    ui = {v2: n for n, v2 in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v2] for v2 in iso]); yr = np.array([r[1] for r in rows])
    gy = (yr // 10) * 10
    yv = np.array([r[2] for r in rows], float)
    nctrl = len(ctrls)
    cols = [np.array([r[4] for r in rows], float), np.array([r[3] for r in rows], float)] + \
           [np.array([r[5 + j] for r in rows], float) for j in range(nctrl)]
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
    for cc in np.unique(gi):
        mm = gi == cc
        s = X[mm].T @ u[mm]
        meat += np.outer(s, s)
    P = np.linalg.pinv(XtX)
    Vb = P @ meat @ P

    res = dict(x=x, y=y, trend=bool(trend), addon=list(addon), n=len(yv), nc=len(ui),
               b=float(b[1]), se=float(np.sqrt(max(Vb[1, 1], 0))))
    if addon:
        # column of each added control: [const, x, ownlevel, ctrls...]
        other_addons = [c for c in addon]
        res["add"] = {}
        for c in addon:
            if c not in ctrls:
                continue
            j = ctrls.index(c)
            cb = float(b[3 + j]); cse = float(np.sqrt(max(Vb[3 + j, 3 + j], 0)))
            # OVB constant a: regress c on [x] + all other columns except x and this c
            keep = [k for k in range(X.shape[1]) if k != 1 and k != 3 + j]
            Z = np.column_stack([X[:, 1], X[:, keep]])
            coef = np.linalg.lstsq(Z.T @ Z, Z.T @ X[:, 3 + j], rcond=None)[0]
            a = float(coef[0])            # coefficient on x in c ~ x + other columns
            r2 = 1 - float(((X[:, 3 + j] - Z @ coef) ** 2).sum() / max((X[:, 3 + j] ** 2).sum(), 1e-12))
            res["add"][c] = dict(coef=cb, se=cse, a=a, se_delta=abs(a) * cse,
                                 partial_r2=float(r2), vif=float(1 / max(1 - r2, 1e-6)),
                                 corr_x=float(np.corrcoef(X[:, 1], X[:, 3 + j])[0, 1]) if X[:, 1].std() > 0 else 0.0)
    return (x, y, trend, addon, res)


if __name__ == "__main__":
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    os.makedirs(OUT, exist_ok=True)
    jobs = [(x, y, t, ad) for x, y in PAIRS for t in (False, True) for ad in ADDONS]
    print("jobs", len(jobs), flush=True)
    with Pool(nproc) as p:
        res = p.map(edge, jobs, chunksize=8)
    store = {}
    for x, y, t, ad, r in res:
        if r is not None:
            store[f"{x}|{y}|{int(t)}|{'+'.join(ad) if ad else 'base'}"] = r
    med = {}
    for x, y in PAIRS:
        med[f"{x}|{y}"] = {c: mediator(x, y, c) for c in ("u5mr", "flfp")}
    json.dump({"vars": VARS, "addons": ["+".join(a) if a else "base" for a in ADDONS], "cells": store,
               "mediator": med}, open(f"{OUT}/controls_results.json", "w"), separators=(",", ":"))
    print("wrote", f"{OUT}/controls_results.json", os.path.getsize(f"{OUT}/controls_results.json") // 1024, "KB", flush=True)
