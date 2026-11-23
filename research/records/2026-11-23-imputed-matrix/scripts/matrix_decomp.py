#!/usr/bin/env python3
"""Decompose WHERE a changed matrix verdict comes from.

Two extra panels, same estimator:
  eduonly   : the six modelled education series from each of the 20 imputations, every other
              series exactly as observed (so only education gap-filling changes);
  macroonly : the five macro series with the long-run-source fill, education exactly as
              observed (so only the macro splice changes).
Output <OUT>/matrix_decomp.json.   usage: matrix_decomp.py [NPROC]
"""
import sys, json, os
import numpy as np
from multiprocessing import Pool
from common import *
import matrix_ext as ME

M = ME.M
VARS = ME.VARS
EDU = ME.EDU
PAIRS = ME.PAIRS
OUT = ME.OUT
IMPDIR = ME.IMPDIR

def verdict(b, se):
    if se is None or se <= 0:
        return "n/a"
    t = b / se
    return "sig+" if t > 1.96 else ("sig-" if t < -1.96 else "null")


if __name__ == "__main__":
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    # only the cells whose verdict changed need decomposing (keeps the run small)
    SEL = None
    mp = f"{OUT}/matrix_ext.json"
    if os.path.exists(mp):
        MM = json.load(open(mp))["main"]
        SEL = []
        for k, cell in MM.items():
            o, i = cell.get("obs"), cell.get("imp")
            vo = verdict(*o[:2]) if o else None
            vi = verdict(*i[:2]) if i else None
            if o is None or i is None:
                SEL.append(k); continue
            if (vo == "null") != (vi == "null") or (vo != "null" and vi != "null" and (o[0] > 0) != (i[0] > 0)):
                SEL.append(k)
        print("decomposing", len(SEL), "changed cells", flush=True)
    obs = ME.loadset(DATA)
    m01 = ME.loadset(f"{IMPDIR}/m01")
    ME.DS = {}
    ME.DS["macroonly"] = {v: (m01[v] if v not in EDU else obs[v]) for v in VARS}
    for m in range(M):
        dd = ME.loadset(f"{IMPDIR}/m{m + 1:02d}")
        ME.DS[f"m{m + 1:02d}"] = {v: (dd[v] if v in EDU else obs[v]) for v in VARS}
    pairs = PAIRS
    if SEL is not None:
        pairs = [(k.split("|")[0], k.split("|")[1]) for k in SEL]
        pairs = sorted(set(pairs))
    tregs = [0, 1] if SEL is None else sorted({int(k.split("|")[2]) for k in SEL})
    jobs = [(ds, x, y, bool(t), 0) for ds in ME.DS for (x, y) in pairs for t in tregs]
    print("jobs", len(jobs), flush=True)
    with Pool(nproc) as p:
        res = p.map(ME.edge, jobs, chunksize=8)
    RES = {(ds, x, y, int(t), 0): r for ds, x, y, t, xlag, r in res if r}
    out = {"eduonly": {}, "macroonly": {}, "cells": SEL}
    for x, y in pairs:
        for t in tregs:
            k = f"{x}|{y}|{int(t)}"
            per = [RES.get((f"m{m + 1:02d}", x, y, int(t), 0)) for m in range(M)]
            per = [list(pp) for pp in per if pp is not None]
            if len(per) == M:
                out["eduonly"][k] = {"per": per, "imp": list(ME.rubin(per))}
            r = RES.get(("macroonly", x, y, int(t), 0))
            if r:
                out["macroonly"][k] = list(r)
    json.dump(out, open(f"{OUT}/matrix_decomp.json", "w"), separators=(",", ":"))
    print("wrote", f"{OUT}/matrix_decomp.json", os.path.getsize(f"{OUT}/matrix_decomp.json") // 1024, "KB", flush=True)
