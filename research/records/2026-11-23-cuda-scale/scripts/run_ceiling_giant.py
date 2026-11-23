"""Memory ceiling + one giant ABM demonstration, in a clean process.

The first attempt (run_ladder.py) hit two mechanics that this script fixes:
  * engine.load() stages host arrays onto the device, so peak memory = engine state + one
    staging buffer (the largest is n*980 doubles); the ceiling must reserve for it;
  * a half-built engine must be dropped before the CuPy pool is released, otherwise the next
    attempt fails even though memory was freed.
Probing is allocation+load only (that is what actually fails); the winner is then given one
full life course as the giant demonstration.
"""
import os, sys, time, gc
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cupy as cp
from benchlib import (log, gpu_stat, build_specs, state_bytes, mem, free_pool, dump,
                      NW, WPR, TMAX, YEARS, array_digest, GPUDose, targets_array)

# one prepared draw set, cycled to fill the launch (timing/allocation do not depend on values)
BASE_N = 4000
BASE = build_specs(BASE_N, seed=3)
log("built", BASE_N, "distinct prepared draws; gpu:", gpu_stat())

eng = GPUDose(nW=NW, seed=5, max_runs=100, tmax=TMAX)
bpr = state_bytes(eng)[0] / 100.0
del eng; gc.collect(); free_pool()
free0 = mem()["free_bytes"]
out = dict(job="cuda-scale ceiling + giant ABM", gpu=gpu_stat(), nW=NW, women_per_run=WPR,
           tmax=TMAX, years=YEARS, bytes_per_run=round(bpr, 1),
           bytes_per_woman=round(bpr / WPR, 2), free_bytes_at_start=int(free0),
           distinct_prepared_draws=BASE_N,
           note="load() stages host arrays on the device; ceiling reserves for the staging buffer")
log(f"free={free0/1e6:.0f}MB bytes/run={bpr:.0f} reserve-based candidate below")

STAGING = 700 * 1024 * 1024            # largest staging buffer (n*980*8) + allocator slack
cand = int((free0 - STAGING) / bpr)
log("candidate", cand, "runs =", cand * WPR / 1e6, "M women")


def probe(n):
    """Allocate engine and load n specs; return record. Always cleans up."""
    a = dict(runs=n, women=n * WPR)
    eng = None
    try:
        t0 = time.time(); eng = GPUDose(nW=NW, seed=5, max_runs=n, tmax=TMAX)
        a["alloc_sec"] = round(time.time() - t0, 3)
        sb, big1, _ = state_bytes(eng)
        a["state_bytes"] = int(sb); a["largest_array_bytes"] = int(big1)
        a["free_after_alloc_bytes"] = int(mem()["free_bytes"])
        sp = [BASE[j % BASE_N] for j in range(n)]
        t0 = time.time(); eng.load(sp); a["load_sec"] = round(time.time() - t0, 3)
        a["free_after_load_bytes"] = int(mem()["free_bytes"])
        a["ok"] = True
        return a
    except Exception as e:
        a["ok"] = False
        a["error"] = ("%s: %s" % (type(e).__name__, e))[:300]
        a["free_after_error_bytes"] = int(mem()["free_bytes"]) if True else None
        return a
    finally:
        del eng
        gc.collect(); free_pool()


attempts = []
rec = None
n = cand
for _ in range(5):                      # step down until a load succeeds
    a = probe(n); attempts.append(a); log("PROBE", n, "ok=", a.get("ok"), a.get("error", ""))
    if a["ok"]:
        rec = a; break
    n -= 1000
if rec is not None:                     # then walk up in 250-run steps until it fails
    n = rec["runs"]
    for _ in range(6):
        a = probe(n + 250); attempts.append(a); log("PROBE", n + 250, "ok=", a.get("ok"),
                                                     a.get("error", ""))
        if not a["ok"]:
            break
        rec = a; n = a["runs"]
nmax = rec["runs"]
out["attempts"] = attempts
out["max_runs"] = nmax
out["max_women"] = nmax * WPR
out["state_bytes"] = rec["state_bytes"]
out["bytes_per_woman"] = round(rec["state_bytes"] / (nmax * WPR), 2)
out["free_after_alloc_bytes"] = rec["free_after_alloc_bytes"]
out["free_after_load_bytes"] = rec["free_after_load_bytes"]
out["staging_reserve_bytes"] = STAGING
log("CEILING", {k: out[k] for k in ("max_runs", "max_women", "state_bytes", "bytes_per_woman")})

# ---------------------------------------------------------------- giant ABM at the ceiling
eng = None
try:
    t0 = time.time(); eng = GPUDose(nW=NW, seed=11, max_runs=nmax, tmax=TMAX)
    giant = dict(runs=nmax, women=nmax * WPR, cohorts_per_run=14,
                 cohorts_total=nmax * 14, years=YEARS, tmax=TMAX, seed=11, nW=NW,
                 women_per_run=WPR, alloc_sec=round(time.time() - t0, 3),
                 distinct_prepared_draws=BASE_N,
                 note="one launch; %d distinct prepared parameter x country draws cycled over "
                      "%d runs (scale demonstration, not parameter diversity)" % (BASE_N, nmax))
    sp = [BASE[j % BASE_N] for j in range(nmax)]
    t0 = time.time(); eng.load(sp); giant["load_sec"] = round(time.time() - t0, 3)
    sb, big1, _ = state_bytes(eng)
    giant["state_bytes"] = int(sb); giant["bytes_per_woman"] = round(sb / (nmax * WPR), 2)
    giant["free_before_run_bytes"] = int(mem()["free_bytes"])
    t0 = time.time(); acc = eng.run(0); cp.cuda.Stream.null.synchronize()
    giant["first_run_sec_incl_capture"] = round(time.time() - t0, 3)
    t0 = time.time(); acc = eng.run(0); cp.cuda.Stream.null.synchronize()
    giant["run_sec_replay"] = round(time.time() - t0, 3)
    giant["women_per_sec"] = int(nmax * WPR / giant["run_sec_replay"])
    giant["woman_years_simulated"] = int(nmax * WPR) * YEARS
    giant["total_births"] = int(round(float(acc["births"].sum())))
    giant["total_exposure_weight"] = float(acc["expo"].sum())
    giant["aggregate_digest_births"] = array_digest(acc["births"])
    small = {k: acc[k][:1000] for k in ("births", "expo", "sing", "afb_s", "afb_n", "m18n", "m18d")}
    S = targets_array(small)
    yrs = np.array(sorted(S["tfr"])); col = lambda y: int(np.where(yrs == y)[0][0])
    tfr = np.array([[S["tfr"][y][j] for y in yrs] for j in range(1000)])
    giant["mean_tfr_first1000_runs_2012"] = round(float(np.nanmean(tfr[:, col(2012)])), 4)
    giant["mean_tfr_first1000_runs_1980"] = round(float(np.nanmean(tfr[:, col(1980)])), 4)
    giant["gpu"] = gpu_stat()
    out["giant"] = giant
    log("GIANT", {k: giant[k] for k in ("runs", "women", "run_sec_replay", "women_per_sec",
                                         "state_bytes", "woman_years_simulated", "total_births")})
finally:
    del eng
    gc.collect(); free_pool()
out["gpu_at_end"] = gpu_stat()
dump("ceiling_giant.json", out)
log("DONE ceiling+giant; gpu:", gpu_stat())
