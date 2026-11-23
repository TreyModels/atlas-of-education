"""Scale ladder + memory ceiling + one giant ABM demonstration (RTX 2080 Ti, 11 GB).

Section 1  throughput vs population: 1e5, 1e6, 1e7 women, 3 timed replays each.
Section 2  memory ceiling: largest population whose full engine state fits in device memory,
           confirmed by actually loading and running one full life course.
Section 3  giant ABM: the largest safe population, with end-to-end accounting.

Every number is written to results/*.json; nothing is extrapolated unless labelled so.
"""
import os, sys, time, gc
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cupy as cp
from benchlib import (log, gpu_stat, build_specs, state_bytes, mem, free_pool, dump,
                      NW, WPR, TMAX, YEARS, RESULTS, array_digest, GPUDose, targets_array)

out = dict(
    job="cuda-scale", host="box2 (AutoDL)", gpu="NVIDIA RTX 2080 Ti 11GB",
    nW=NW, women_per_run=WPR, tmax=TMAX, years=YEARS,
    free_bytes_at_start=mem()["free_bytes"], total_bytes=mem()["total_bytes"],
    gpu_at_start=gpu_stat(),
    note="A run = 14 cohorts x 2 urban/rural x 5 wealth quintiles x 12 women. "
         "Times include the device->host collection that eng.run() performs unless stated.",
)
log("GPU at start:", out["gpu_at_start"])
log("free/total bytes:", out["free_bytes_at_start"], out["total_bytes"])

# ---------------------------------------------------------------- bytes per run
eng = GPUDose(nW=NW, seed=5, max_runs=100, tmax=TMAX)
bpr, biggest, n_arr = state_bytes(eng)
out["bytes_per_run"] = bpr / 100.0
out["bytes_per_woman"] = bpr / 100.0 / WPR
out["engine_arrays"] = n_arr
log(f"state: {bpr/100.0:.0f} bytes/run, {bpr/100.0/WPR:.1f} bytes/woman, {n_arr} device arrays")
del eng; free_pool(); gc.collect()

# ---------------------------------------------------------------- Section 1: ladder
specs_all = build_specs(60000)          # built once, sliced; identical specs across sizes
log("built 60000 specs, gpu:", gpu_stat())
ladder = []
for target_women in (1e5, 1e6, 1e7):
    n = int(round(target_women / WPR))
    t0 = time.time()
    eng = GPUDose(nW=NW, seed=5, max_runs=n, tmax=TMAX)
    alloc_sec = time.time() - t0
    t0 = time.time(); eng.load(specs_all[:n]); load_sec = time.time() - t0
    t0 = time.time(); eng.run(0); cp.cuda.Stream.null.synchronize()
    first_sec = time.time() - t0          # includes warm-up + CUDA-graph capture (2 life courses)
    times = []
    for _ in range(3):
        t0 = time.time(); eng.run(0); cp.cuda.Stream.null.synchronize(); times.append(time.time() - t0)
    sb, big1, _ = state_bytes(eng)
    women = n * WPR
    rec = dict(
        target_women=int(target_women), runs=n, women=women,
        alloc_sec=round(alloc_sec, 3), load_sec=round(load_sec, 3),
        first_run_sec=round(first_sec, 3),
        replay_sec=[round(t, 4) for t in times],
        replay_median_sec=round(float(np.median(times)), 4),
        women_per_sec=int(women / float(np.median(times))),
        state_bytes=int(sb), bytes_per_woman=round(sb / women, 2),
        free_after_alloc_bytes=mem()["free_bytes"], gpu=gpu_stat(),
    )
    ladder.append(rec); log("LADDER", rec)
    dump("scale_ladder.json", dict(**out, results=ladder))
    del eng; free_pool(); gc.collect()

# ---------------------------------------------------------------- Section 2: ceiling
log("=== ceiling search ===")
free_before = mem()["free_bytes"]
reserve = 220 * 1024 * 1024            # keep ~220 MB headroom for CUDA/graph machinery
cand = int((free_before - reserve) / (bpr / 100.0))
log(f"free={free_before/1e6:.0f}MB, bytes/run={bpr/100:.0f}, candidate={cand} runs "
    f"({cand*WPR/1e6:.2f}M women)")
ceiling = dict(free_bytes_before=int(free_before), reserve_bytes=reserve,
               bytes_per_run=bpr / 100.0, first_candidate=cand, attempts=[])


def try_build_runs(n):
    """Build engine + load + one full life course. Returns (ok, record)."""
    a = dict(runs=n, women=n * WPR)
    try:
        t0 = time.time()
        eng = GPUDose(nW=NW, seed=5, max_runs=n, tmax=TMAX)
        a["alloc_sec"] = round(time.time() - t0, 3)
        sb, big1, _ = state_bytes(eng)
        a["state_bytes"] = int(sb); a["free_after_alloc_bytes"] = mem()["free_bytes"]
        a["largest_array_bytes"] = int(big1)
        t0 = time.time(); eng.load(specs_all[:n]); a["load_sec"] = round(time.time() - t0, 3)
        t0 = time.time(); eng.run(0); cp.cuda.Stream.null.synchronize()
        a["first_run_sec"] = round(time.time() - t0, 3)
        t0 = time.time(); eng.run(0); cp.cuda.Stream.null.synchronize()
        a["replay_sec"] = round(time.time() - t0, 3)
        a["women_per_sec"] = int(n * WPR / a["replay_sec"])
        a["gpu"] = gpu_stat()
        a["ok"] = True
        del eng; free_pool(); gc.collect()
        return True, a
    except Exception as e:                 # OOM or anything else: record and step down
        a["ok"] = False; a["error"] = ("%s: %s" % (type(e).__name__, e))[:300]
        a["gpu"] = gpu_stat()
        try:
            free_pool(); gc.collect()
        except Exception:
            pass
        return False, a


# step down from the candidate until something builds, then step up by 250 to find the edge
n = cand
rec = None
for _ in range(6):
    ok, a = try_build_runs(n)
    ceiling["attempts"].append(a); log("CEILING try", a.get("runs"), "ok=", ok, a.get("error", ""))
    if ok:
        rec = a; break
    n -= 500
if rec is not None:
    # walk up in 250-run steps while it still builds+runs
    n = rec["runs"]
    for _ in range(3):
        ok, a = try_build_runs(n + 250)
        ceiling["attempts"].append(a); log("CEILING try", a.get("runs"), "ok=", ok, a.get("error", ""))
        if not ok: break
        rec = a; n = a["runs"]
ceiling["max_runs"] = rec["runs"] if rec else None
ceiling["max_women"] = rec["runs"] * WPR if rec else None
ceiling["state_bytes"] = rec["state_bytes"] if rec else None
ceiling["bytes_per_woman"] = round(rec["state_bytes"] / (rec["runs"] * WPR), 2) if rec else None
ceiling["gpu_at_end"] = gpu_stat()
log("CEILING RESULT", {k: ceiling[k] for k in
    ("max_runs", "max_women", "state_bytes", "bytes_per_woman")})
dump("ceiling.json", ceiling)

# ---------------------------------------------------------------- Section 3: giant ABM
if rec is not None:
    n = rec["runs"]
    log(f"=== giant ABM: {n} runs / {n*WPR/1e6:.2f}M women ===")
    t0 = time.time(); eng = GPUDose(nW=NW, seed=11, max_runs=n, tmax=TMAX)
    giant = dict(runs=n, women=n * WPR, cohorts_total=n * 14, cohorts_per_run=14,
                 years=YEARS, tmax=TMAX, seed=11, nW=NW,
                 women_per_run=WPR, alloc_sec=round(time.time() - t0, 3))
    t0 = time.time(); eng.load(specs_all[:n]); giant["load_sec"] = round(time.time() - t0, 4)
    sb, big1, _ = state_bytes(eng)
    giant["state_bytes"] = int(sb)
    giant["bytes_per_woman"] = round(sb / (n * WPR), 2)
    t0 = time.time(); acc = eng.run(0); cp.cuda.Stream.null.synchronize()
    giant["run_sec_incl_capture"] = round(time.time() - t0, 3)
    t0 = time.time(); acc = eng.run(0); cp.cuda.Stream.null.synchronize()
    giant["run_sec_replay"] = round(time.time() - t0, 3)
    giant["women_per_sec"] = int(n * WPR / giant["run_sec_replay"])
    giant["woman_years_simulated"] = int(n * WPR) * YEARS
    giant["total_births"] = int(acc["births"].sum())
    giant["total_exposure"] = int(acc["expo"].sum())
    giant["aggregate_digest_births"] = array_digest(acc["births"])
    S = targets_array({k: (acc[k][:1000] if k in ("births", "expo", "sing") else acc[k][:1000])
                       for k in ("births", "expo", "sing", "afb_s", "afb_n", "m18n", "m18d")})
    yrs = np.array(sorted(S["tfr"]))
    col = lambda y: int(np.where(yrs == y)[0][0])
    tfr = np.array([[S["tfr"][y][j] for y in yrs] for j in range(1000)])
    giant["mean_tfr_first1000_runs_2012"] = round(float(np.nanmean(tfr[:, col(2012)])), 4)
    giant["mean_tfr_first1000_runs_1980"] = round(float(np.nanmean(tfr[:, col(1980)])), 4)
    giant["gpu"] = gpu_stat()
    log("GIANT", {k: giant[k] for k in ("runs", "women", "run_sec_replay", "women_per_sec",
                                         "state_bytes", "woman_years_simulated", "total_births")})
    dump("giant_abm.json", giant)
    del eng; free_pool(); gc.collect()

log("DONE ladder+ceiling+giant; gpu:", gpu_stat())
