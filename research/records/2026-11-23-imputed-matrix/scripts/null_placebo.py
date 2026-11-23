#!/usr/bin/env python3
"""Wrong-country permutation negative control ("the placebo that really should be null").

The treatment series x is replaced by the same-year value of a randomly matched DIFFERENT
country (one fixed derangement). The supposed cause then cannot have any causal path to the
outcome, and after country effects + decade effects + country trends the association should be
at the nominal rate (~5%). Run on the observed panel and on several imputed panels: if the
gap-filling manufactures links, the imputed panels will show more significant placebo links.
Output: <OUT>/null_placebo.json and prints a table.   usage: null_placebo.py [NPROC]
"""
import json, os, sys
import numpy as np
from multiprocessing import Pool
from common import *
import matrix_ext as ME

VARS, PAIRS, OUT, IMPDIR = ME.VARS, ME.PAIRS, ME.OUT, ME.IMPDIR
REG = ME.REG


def load_flags():
    return ME.load_flags()


def make_perm(seed=20261123):
    rng = np.random.default_rng(seed)
    C = list(REG)
    while True:
        perm = rng.permutation(len(C))
        if all(perm[k] != k for k in range(len(C))):
            break
    return {C[k]: C[perm[k]] for k in range(len(C))}


S_OWN = {}


def edge_null(args):
    """same estimator as matrix_ext.edge, but the treatment is the same-year value of a
    randomly matched DIFFERENT country; the outcome and controls stay own-country."""
    ds, x, y, trend = args
    S = S_OWN[ds]
    perm = PERM
    ctrls = [c for c in ME.CTRL if c not in (x, y)]
    rows = []
    for (i, t), v in S[y].items():
        if (i, t + 10) not in S[y]:
            continue
        j = perm.get(i)
        if j is None:
            continue
        xv = S[x].get((j, t))
        if xv is None:
            continue
        if not all((i, t) in S[c] for c in ctrls):
            continue
        rows.append([i, t, S[y][(i, t + 10)] - v, v, xv] + [S[c][(i, t)] for c in ctrls])
    if trend:
        cnt = {}
        for r in rows:
            cnt[r[0]] = cnt.get(r[0], 0) + 1
        rows = [r for r in rows if cnt[r[0]] >= 4]
    if len(rows) < 150 or len({r[0] for r in rows}) < 10:
        return None
    iso = [r[0] for r in rows]
    ui = {v2: n for n, v2 in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v2] for v2 in iso]); yr = np.array([r[1] for r in rows])
    gy = (yr // 10) * 10
    yv = np.array([r[2] for r in rows])
    cols = [np.array([r[4] for r in rows], float), np.array([r[3] for r in rows])] + \
           [np.array([r[5 + j2] for r in rows], float) for j2 in range(len(ctrls))]
    if trend:
        for j2 in range(len(ui)):
            cols.append(((gi == j2) * yr).astype(float))
    X = np.column_stack([np.ones(len(yv))] + cols)
    X = np.column_stack([ME.dm(X[:, k], gi) for k in range(X.shape[1])])
    X = np.column_stack([ME.dm(X[:, k], gy) for k in range(X.shape[1])])
    Y = ME.dm(ME.dm(yv, gi), gy)
    XtX = X.T @ X
    b = np.linalg.lstsq(XtX, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        mm = gi == c
        sc = X[mm].T @ u[mm]
        meat += np.outer(sc, sc)
    P = np.linalg.pinv(XtX)
    Vb = P @ meat @ P
    return (ds, x, y, trend, (float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(yv), len(ui)))


def verdict(b, se):
    if se is None or se <= 0:
        return "n/a"
    t = b / se
    return "sig+" if t > 1.96 else ("sig-" if t < -1.96 else "null")


if __name__ == "__main__":
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    perm = make_perm()
    print("permutation fixed points:", sum(1 for k, v in perm.items() if k == v), flush=True)
    S = {"obs": ME.loadset(DATA), "mean": ME.loadset(f"{IMPDIR}/mean")}
    for m in (1, 2, 3):
        S[f"m{m:02d}"] = ME.loadset(f"{IMPDIR}/m{m:02d}")
    PERM = perm
    S_OWN = {f"{k}_null": v for k, v in S.items()}
    ME.DS = S_OWN
    jobs = [(ds, x, y, t) for ds in S_OWN for (x, y) in PAIRS for t in (False, True)]
    print("jobs", len(jobs), flush=True)
    with Pool(nproc) as p:
        res = p.map(edge_null, jobs, chunksize=8)
    RES = {(ds, x, y, int(t)): r for ds, x, y, t, r in res if r}
    out = {"perm_seed": 20261123, "datasets": {}, "cells": {}}
    for ds in S_OWN:
        sig = {0: 0, 1: 0}; tot = {0: 0, 1: 0}
        for (x, y) in PAIRS:
            for t in (False, True):
                r = RES.get((ds, x, y, int(t)))
                if r is None:
                    continue
                tot[int(t)] += 1
                v = verdict(r[0], r[1])
                if v != "null":
                    sig[int(t)] += 1
                out["cells"][f"{ds}|{x}|{y}|{int(t)}"] = list(r) + [v]
        out["datasets"][ds] = {"sig": sig, "tot": tot}
        print(f"{ds}: country effects {sig[0]}/{tot[0]} significant ({100*sig[0]/max(tot[0],1):.1f}%), "
              f"country trends {sig[1]}/{tot[1]} significant ({100*sig[1]/max(tot[1],1):.1f}%)", flush=True)
    json.dump(out, open(f"{OUT}/null_placebo.json", "w"), separators=(",", ":"))
    # specific pre-registered negative-control link: another country's child mortality -> own lsc change
    print("\npre-registered negative-control link: other country's child mortality -> own change in lower-secondary")
    for t in (0, 1):
        for ds in S_OWN:
            r = RES.get((ds, "u5mr", "lsc", t))
            if r:
                print(f"  {ds:9s} {'country effects' if t == 0 else 'country trends ':15s} b={r[0]:+.4f} se={r[1]:.4f} "
                      f"n={r[2]} countries={r[3]} -> {verdict(r[0], r[1])}")
    print("wrote", f"{OUT}/null_placebo.json")
