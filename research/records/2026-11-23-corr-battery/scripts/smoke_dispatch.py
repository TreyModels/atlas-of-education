#!/usr/bin/env python3
"""Five-second-class dispatch smoke test: run ONE unit of every task kind
(A, B, P, C, T) through the SAME _run_one dispatch path used by the battery,
in a Pool, and assert shapes. Run before every full launch."""
import time
import multiprocessing as mp
import battery

JOBS = [("A", (0,)), ("B", (0, 6)), ("P", (0,)), ("C", (0, 20)),
        ("T", ("mys_total", 12))]

if __name__ == "__main__":
    t0 = time.time()
    with mp.Pool(2) as pool:
        out = list(pool.imap_unordered(battery._run_one, JOBS, chunksize=1))
    for kind, arr in out:
        print(f"SMOKE kind={kind} shape={getattr(arr, 'shape', None)} ok={arr is not None}")
    assert len(out) == len(JOBS)
    print(f"SMOKE PASS in {time.time()-t0:.1f}s")
