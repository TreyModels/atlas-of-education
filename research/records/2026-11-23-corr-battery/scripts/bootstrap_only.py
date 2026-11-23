#!/usr/bin/env python3
"""Compute the pre-registered bootstrap pieces separately from the main battery.

The main run's checkpoint intentionally drops the bootstrap draws, so after the
battery finishes this script recomputes them from the cached row tables (cheap:
342 pairs x 500 country-clustered reps on one headline cell + the threshold
bootstrap for four schooling measures) and writes out/final_C.npz / final_T.npz
for process_results.py to merge.
"""
import multiprocessing as mp
import numpy as np
import time
import battery as B

OUT = "/root/work/corr_battery/out"
REPS = 500

if __name__ == "__main__":
    t0 = time.time()
    jobs = [("C", (p, REPS)) for p in range(len(B.PAIRS))]
    jobs += [("T", (m, REPS)) for m in ("mys_total", "mys_female", "lsc", "sec")]
    accC, accT = [], []
    with mp.Pool(10) as pool:
        for kind, res in pool.imap_unordered(B._run_one, jobs, chunksize=1):
            if res is None or not len(res):
                continue
            if kind == "C":
                accC.append(res)
            elif kind == "T":
                accT.append(res)
    C = np.concatenate(accC) if accC else np.zeros((0, 8))
    T = np.concatenate(accT) if accT else np.zeros((0, 6))
    np.savez_compressed(f"{OUT}/final_C.npz", C=C)
    np.savez_compressed(f"{OUT}/final_T.npz", T=T)
    print(f"bootstrap only: C{ C.shape } T{ T.shape } in {time.time()-t0:.0f}s", flush=True)
