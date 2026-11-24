#!/usr/bin/env python3
"""Falsifier: determinism of the random-partition draws.

(a) Recompute three replicates (1, 250, 400) and the real pass from scratch in this
    process and require bit-for-bit identical output.
(b) Cross-run check: the earlier 74-replicate run used the same seeds (1000+r), so every
    overlapping replicate must be numerically identical to this run's version. This is
    what makes the 74-draw and 400-draw results comparable.

Writes out/results/determinism.txt.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, pickle, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_multiverse400 as rm

FINAL = os.environ.get("GM_FINAL", "out/final400.pkl")
OLD = os.environ.get("GM_OLD", "out/final75.pkl")
D = pickle.load(open(FINAL, "rb")); res = D["res"]
L = []
t0 = time.time()
L.append("DETERMINISM CHECKS (falsifier a)")
L.append("(a) same code, same seed, fresh process -> identical output?")
for r in (7, 250, 400):
    t = time.time(); rr, out = rm.job(r); dt = time.time() - t
    st = res[r]
    dz = float(np.nanmax(np.abs(out["z"] - st["z"])))
    dq = float(np.nanmax(np.abs(out["Qp"] - st["Qp"])))
    df = int((out["flip"] != st["flip"]).sum())
    ident = bool(np.array_equal(out["z"], st["z"], equal_nan=True)
                 and np.array_equal(out["Qp"], st["Qp"], equal_nan=True)
                 and np.array_equal(out["flip"], st["flip"]))
    L.append(f"  replicate {r}: recomputed in {dt:.1f}s  identical={ident}  "
             f"max|dz|={dz:.2e}  max|dQp|={dq:.2e}  flip mismatches={df}")
t = time.time(); _, out0 = rm.job(0); dt = time.time() - t
st0 = res[0]
cells_ok = all(np.array_equal(np.asarray(out0["full"][c][i]), np.asarray(st0["full"][c][i]), equal_nan=True)
               for c in range(len(st0["full"])) for i in range(4))
L.append(f"  real-grouping pass: recomputed in {dt:.1f}s  pooled b identical="
         f"{np.array_equal(out0['pooled'][0], st0['pooled'][0], equal_nan=True)}  all 179 cells identical={cells_ok}")
L.append("")
L.append("(b) cross-run: earlier 74-replicate run, same seeds (1000+r)")
Do = pickle.load(open(OLD, "rb"))
common = sorted(set(k for k in res if k != 0) & set(k for k in Do["res"] if k != 0))
mism = 0; maxz = 0.0; maxq = 0.0; fl = 0
for r in common:
    a = Do["res"][r]["z"]; b = res[r]["z"]
    if not np.array_equal(a, b, equal_nan=True):
        mism += 1
    maxz = max(maxz, float(np.nanmax(np.abs(a - b))))
    maxq = max(maxq, float(np.nanmax(np.abs(Do["res"][r]["Qp"] - res[r]["Qp"]))))
    fl += int((Do["res"][r]["flip"] != res[r]["flip"]).sum())
L.append(f"  overlapping replicates: {len(common)}  z mismatches: {mism}  max|dz|={maxz:.2e}  "
         f"max|dQp|={maxq:.2e}  flip mismatches: {fl}")
L.append(f"  real-grouping pass identical to old run: "
         f"{np.array_equal(Do['res'][0]['z'], res[0]['z'], equal_nan=True)}")
L.append("")
L.append(f"total check time {time.time() - t0:.0f}s")
txt = "\n".join(L)
print(txt)
os.makedirs("out/results", exist_ok=True)
open(os.path.join(os.environ.get("GM_OUTDIR", "out/results"), "determinism.txt"), "w").write(txt + "\n")
