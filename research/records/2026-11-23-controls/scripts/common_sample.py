#!/usr/bin/env python3
"""Common-sample baselines for the controls job.

Adding child mortality / women's work as controls also changes the sample (those series are less
complete), so "the estimate moved" could be sample composition rather than the control.  For every
cell whose verdict changed, re-estimate the BASELINE (same estimator, no added control) on exactly
the rows the control variant used.  Then the change splits into:
   sample effect   = baseline(full rows)      -> baseline(same rows)
   control effect  = baseline(same rows)      -> variant
usage: common_sample.py [NPROC]
"""
import sys, json, os, csv
import numpy as np
from multiprocessing import Pool
import controls_matrix as CM

RES = "/root/work/controls/results"
OUT = "/root/work/controls/out"


def build_rows(x, y, trend, addon):
    ctrls = [c for c in CM.BASE if c not in (x, y)] + [c for c in addon if c not in (x, y)]
    rows = []
    for (i, t), v in CM.S[y].items():
        if (i, t + 10) not in CM.S[y] or (i, t) not in CM.S[x]:
            continue
        if not all((i, t) in CM.S[c] for c in ctrls):
            continue
        rows.append([i, t, CM.S[y][(i, t + 10)] - v, v, CM.S[x][(i, t)]] + [CM.S[c][(i, t)] for c in ctrls])
    if trend:
        cnt = {}
        for r in rows:
            cnt[r[0]] = cnt.get(r[0], 0) + 1
        rows = [r for r in rows if cnt[r[0]] >= 4]
    return rows, ctrls


def edge_base_same(args):
    x, y, trend, addon = args
    rows, ctrls = build_rows(x, y, trend, addon)
    ctrls_base = [c for c in ctrls if c not in addon]
    if len(rows) < 150 or len({r[0] for r in rows}) < 10:
        return (x, y, trend, addon, None)
    iso = [r[0] for r in rows]
    ui = {v2: n for n, v2 in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v2] for v2 in iso]); yr = np.array([r[1] for r in rows])
    gy = (yr // 10) * 10
    yv = np.array([r[2] for r in rows], float)
    # row layout: [iso, year, dY, level, x, controls...]; controls are base then added
    base_cols = [r for r in ctrls if r not in addon]
    cols = [np.array([r[4] for r in rows], float), np.array([r[3] for r in rows], float)] + \
           [np.array([r[5 + ctrls.index(c)] for r in rows], float) for c in base_cols]
    if trend:
        for j in range(len(ui)):
            cols.append(((gi == j) * yr).astype(float))
    X = np.column_stack([np.ones(len(yv))] + cols)
    X = np.column_stack([CM.dm(X[:, k], gi) for k in range(X.shape[1])])
    X = np.column_stack([CM.dm(X[:, k], gy) for k in range(X.shape[1])])
    Y = CM.dm(CM.dm(yv, gi), gy)
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
    return (x, y, trend, addon, (float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(yv), len(ui)))


if __name__ == "__main__":
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    jobs = set()
    with open(f"{RES}/changed_verdicts.csv") as f:
        for r in csv.DictReader(f):
            j = r["variant"]
            t = 0 if r["spec"] == "country effects" else 1
            ad = {"u5mr": ("u5mr",), "flfp": ("flfp",), "both": ("u5mr", "flfp")}[j]
            jobs.add((r["x"], r["y"], bool(t), ad))
    jobs = sorted(jobs)
    print("common-sample baseline jobs", len(jobs), flush=True)
    with Pool(nproc) as p:
        res = p.map(edge_base_same, jobs, chunksize=4)
    out = {}
    for x, y, t, ad, r in res:
        if r is not None:
            out[f"{x}|{y}|{int(t)}|{'+'.join(ad)}"] = list(r)
    json.dump(out, open(f"{OUT}/common_sample.json", "w"), separators=(",", ":"))
    print("wrote", len(out), "cells", flush=True)
