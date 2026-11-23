"""Robustness audit of the GPU dose engine (RTX 2080 Ti, box2).

A. Determinism: identical seed, different batch sizes / launch configurations / allocations
   must give bit-identical aggregates.
B. Thermal/clock stability: repeat one benchmark three times, report variance, and check the
   results are bit-identical across repeats.
C. Capability: 10^8 women as two batched launches (measured, not extrapolated).
"""
import os, sys, time, json, gc
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cupy as cp
from benchlib import (log, gpu_stat, build_specs, state_bytes, mem, free_pool, dump, compare,
                      array_digest, PAN, FIT, NW, WPR, TMAX, RESULTS)
import dosecore as dc
from engine import GPUDose, make_spec
import abm_dose

audit = dict(job="cuda-scale robustness audit", host="box2 (AutoDL)",
             gpu="NVIDIA RTX 2080 Ti 11GB", nW=NW, women_per_run=WPR,
             gpu_at_start=gpu_stat())

# ---------------------------------------------------------------- A. determinism
log("=== A. determinism ===")
rng = np.random.default_rng(0)
theta = dc.LO + rng.random((3, dc.D_)) * (dc.HI - dc.LO)
countries = FIT[:4]                                # 3 draws x 4 countries = 12 runs
nruns = theta.shape[0] * len(countries)


def run_batch(batch):
    r = abm_dose.simulate(theta, countries, scen=0, nW=NW, seed=7, batch=batch)
    return r


ref = run_batch(1)
det = dict(config=dict(draws=3, countries=countries, nruns=nruns, nW=NW, seed=7),
           batch_size_tests=[], graph_tests=[], allocation_tests=[])
for b in (1, 5, 7, 12, 500):
    r = run_batch(b)
    rec = dict(requested_batch=b, effective_batch=min(b, nruns))
    for g in ("tfr", "asfr1519", "smam", "m18", "afb", "coh"):
        rec[g] = compare(ref[g], r[g])
    det["batch_size_tests"].append(rec)
    log("batch", b, "bitwise identical:",
        all(rec[g]["bitwise_identical"] for g in ("tfr", "asfr1519", "smam", "m18", "afb", "coh")))

# same 12 runs, but launched with/without CUDA graph, and with a much larger allocation
iso_specs = []
for i in range(theta.shape[0]):
    for k, iso in enumerate(countries):
        pc = PAN["countries"][iso]
        iso_specs.append(make_spec(pc, theta[i], 0, 0.0, pc["age_gap"], 7, i * len(countries) + k))

eng_g = GPUDose(nW=NW, seed=7, max_runs=nruns, tmax=TMAX)
eng_g.load(iso_specs); acc_g = eng_g.run(0, use_graph=True)
eng_p = GPUDose(nW=NW, seed=7, max_runs=nruns, tmax=TMAX)
eng_p.load(iso_specs); acc_p = eng_p.run(0, use_graph=False)
graph_rec = dict(name="CUDA graph replay vs plain launches (same seed, same batch)")
for g in ("births", "expo", "sing", "afb_s", "afb_n", "m18n", "m18d", "coh"):
    graph_rec[g] = compare(acc_g[g], acc_p[g])
det["graph_tests"].append(graph_rec)
log("graph vs plain bitwise identical:",
    all(graph_rec[g]["bitwise_identical"] for g in ("births", "expo", "sing", "afb_s",
                                                    "afb_n", "m18n", "m18d", "coh")))

eng_big = GPUDose(nW=NW, seed=7, max_runs=4096, tmax=TMAX)
eng_big.load(iso_specs); acc_big = eng_big.run(0, use_graph=True)
alloc_rec = dict(name="max_runs=12 vs max_runs=4096 engine allocation (same 12 runs)")
for g in ("births", "expo", "sing", "afb_s", "afb_n", "m18n", "m18d", "coh"):
    alloc_rec[g] = compare(acc_g[g], acc_big[g])
det["allocation_tests"].append(alloc_rec)
log("allocation invariance bitwise identical:",
    all(alloc_rec[g]["bitwise_identical"] for g in ("births", "expo", "sing", "afb_s",
                                                    "afb_n", "m18n", "m18d", "coh")))
det["all_identical"] = bool(
    all(all(t[g]["bitwise_identical"] for g in ("tfr", "asfr1519", "smam", "m18", "afb", "coh"))
        for t in det["batch_size_tests"])
    and all(graph_rec[g]["bitwise_identical"] for g in ("births", "expo", "sing", "afb_s",
                                                        "afb_n", "m18n", "m18d", "coh"))
    and all(alloc_rec[g]["bitwise_identical"] for g in ("births", "expo", "sing", "afb_s",
                                                        "afb_n", "m18n", "m18d", "coh")))
det["gpu_after"] = gpu_stat()
dump("determinism.json", det)
log("DETERMINISM all_identical =", det["all_identical"])
del eng_g, eng_p, eng_big; free_pool(); gc.collect()

# ---------------------------------------------------------------- B. repeat 3x
log("=== B. repeat x3 (thermal/clock stability + seed determinism) ===")
n = 5952                                    # 5952 runs = 9,999,360 women (~1e7)
specs = build_specs(n, seed=3)
rep = dict(runs=n, women=n * WPR, target_women=1e7,
           note="three independent engine instances, same 5952 specs, seed=5; "
                "each: load, one warm launch (includes capture), then 3 timed replays",
           reps=[], gpu_telemetry=[])
for trial in range(3):
    g0 = gpu_stat()
    t0 = time.time(); eng = GPUDose(nW=NW, seed=5, max_runs=n, tmax=TMAX)
    alloc_sec = time.time() - t0
    t0 = time.time(); eng.load(specs); load_sec = time.time() - t0
    t0 = time.time(); acc = eng.run(0); cp.cuda.Stream.null.synchronize()
    warm_sec = time.time() - t0
    times = []
    for _ in range(3):
        t0 = time.time(); acc = eng.run(0); cp.cuda.Stream.null.synchronize(); times.append(time.time() - t0)
    rec = dict(trial=trial, alloc_sec=round(alloc_sec, 3), load_sec=round(load_sec, 3),
               warm_sec=round(warm_sec, 3), replay_sec=[round(t, 4) for t in times],
               replay_median_sec=round(float(np.median(times)), 4),
               women_per_sec=int(n * WPR / float(np.median(times))),
               births_digest=array_digest(acc["births"]),
               expo_digest=array_digest(acc["expo"]),
               gpu_before=g0, gpu_after=gpu_stat())
    rep["reps"].append(rec); rep["gpu_telemetry"].append(dict(before=g0, after=rec["gpu_after"]))
    log("REP", rec["trial"], "median", rec["replay_median_sec"], "s  digest", rec["births_digest"],
        " gpu", rec["gpu_after"])
    del eng, acc; free_pool(); gc.collect()

all_times = [t for r in rep["reps"] for t in r["replay_sec"]]
meds = [r["replay_median_sec"] for r in rep["reps"]]
rep["replay_sec_all9"] = all_times
rep["replay_mean_sec"] = round(float(np.mean(all_times)), 4)
rep["replay_sd_sec"] = round(float(np.std(all_times, ddof=1)), 4)
rep["replay_cv_pct"] = round(float(np.std(all_times, ddof=1) / np.mean(all_times) * 100), 2)
rep["rep_median_sec"] = meds
rep["rep_median_mean_sec"] = round(float(np.mean(meds)), 4)
rep["rep_median_sd_sec"] = round(float(np.std(meds, ddof=1)), 4)
rep["max_minus_min_sec"] = round(float(max(all_times) - min(all_times)), 4)
rep["births_digests"] = [r["births_digest"] for r in rep["reps"]]
rep["expo_digests"] = [r["expo_digest"] for r in rep["reps"]]
rep["same_aggregates_across_repeats"] = bool(len(set(rep["births_digests"])) == 1 and
                                             len(set(rep["expo_digests"])) == 1)
log("REPEAT summary:", {k: rep[k] for k in ("replay_mean_sec", "replay_sd_sec", "replay_cv_pct",
                                            "rep_median_mean_sec", "rep_median_sd_sec",
                                            "same_aggregates_across_repeats")})
dump("repeat3.json", rep)

# ---------------------------------------------------------------- C. 1e8 women batched
log("=== C. 10^8 women as two batched launches ===")
B = 30000                                    # runs per launch = 50.4M women
# memory check before committing
bpr = state_bytes(GPUDose(nW=NW, seed=5, max_runs=10, tmax=TMAX))[0] / 10.0
free_pool()
big = dict(batch_runs=B, batches=2, planned_women=2 * B * WPR,
           bytes_per_run=round(bpr, 1),
           per_batch_state_bytes=int(bpr * B),
           free_bytes_before=int(mem()["free_bytes"]),
           gpu_before=gpu_stat(), batches_run=[],
           note="each batch = 14 cohorts x 2 x 5 x 12 women = 1680 women per run; "
                "50.4M women per launch, two launches = 100.8M women; 6,000 distinct prepared "
                "parameter draws cycled over the 60,000 runs (timing does not depend on values)")
# Building 60k prepared specs is the slow part (~4 ms each).  Throughput does not depend on the
# parameter values, so build 6,000 distinct draws and cycle them over the 60,000 runs; every run
# still simulates its own 1,680 women through the full life course (documented in the JSON note).
BASE = build_specs(6000, seed=8)
specs2 = [BASE[j % len(BASE)] for j in range(2 * B)]
wall_total = 0.0
for bi in range(2):
    t0 = time.time(); eng = GPUDose(nW=NW, seed=5, max_runs=B, tmax=TMAX)
    alloc_sec = time.time() - t0
    sl = specs2[bi * B:(bi + 1) * B]
    t0 = time.time(); eng.load(sl); load_sec = time.time() - t0
    sb, _, _ = state_bytes(eng)
    t0 = time.time(); acc = eng.run(0); cp.cuda.Stream.null.synchronize()
    first_sec = time.time() - t0
    t0 = time.time(); acc = eng.run(0); cp.cuda.Stream.null.synchronize()
    replay_sec = time.time() - t0
    women = B * WPR
    rec = dict(batch=bi, runs=B, women=women, alloc_sec=round(alloc_sec, 3),
               load_sec=round(load_sec, 3), first_run_incl_capture_sec=round(first_sec, 3),
               replay_sec=round(replay_sec, 3),
               women_per_sec=int(women / replay_sec),
               state_bytes=int(sb), births=int(acc["births"].sum()),
               gpu=gpu_stat())
    big["batches_run"].append(rec)
    wall_total += alloc_sec + load_sec + first_sec + replay_sec
    log("BATCH100M", rec)
    del eng, acc; free_pool(); gc.collect()
big["women_total"] = 2 * B * WPR
big["steady_state_launch_sec_sum"] = round(sum(b["replay_sec"] for b in big["batches_run"]), 3)
big["steady_state_women_per_sec"] = int(big["women_total"] / big["steady_state_launch_sec_sum"])
big["end_to_end_wall_sec"] = round(wall_total, 2)   # alloc + load + warm/capture + 1 replay each
big["gpu_after"] = gpu_stat()
log("BATCH100M summary:", {k: big[k] for k in ("women_total", "steady_state_launch_sec_sum",
                                               "steady_state_women_per_sec", "end_to_end_wall_sec")})
dump("batch100m.json", big)
log("DONE audit; gpu:", gpu_stat())
