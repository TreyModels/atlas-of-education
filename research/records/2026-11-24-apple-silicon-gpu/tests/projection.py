#!/usr/bin/env python3
"""Measure the transcribed-kernel cost per call at smoke and production N, and project full-run wall time.

No production run is executed. Projection = measured per-call time x number of calls required by
run_all.sh's production configuration (exp1: 20 seeds x 5 DGPs x 3 arms x 25 years = 7,500 kernel calls at
N=250,000; exp3: 5,000 draws x 1 call at N=50,000). Host RNG data generation is measured separately at the
smoke N and extrapolated linearly.
"""
import json, os, sys, time
import numpy as np
RECORD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RECORD)
import gpu_compat as gc
from kernels_np_mlx import run_sim_step_arrays

out = {"backend": gc.backend(), "calls": {}}


def make_args(N, year, seed0=20261125, seed1=34):
    rng = np.random.Generator(np.random.Philox(20261125))
    base_y = np.exp(rng.normal(0.0, 0.55, size=N)).astype(np.float32)
    ability = np.clip(rng.normal(1.0, 0.20, size=N), 0.3, 1.8).astype(np.float32)
    sc = [np.int32(N), np.int32(year), np.uint32(seed0), np.uint32(seed1),
          np.float32(0.45), np.float32(0.35), np.float32(0.45), np.float32(0.0),
          np.float32(0.65), np.float32(0.12), np.float32(0.55), np.float32(0.90), np.float32(0.32),
          np.float32(1.4), np.float32(1.3), np.float32(1.6)]
    outs = [gc.empty(N, gc.int32), gc.empty(N, gc.int32), gc.empty(N, gc.float32),
            gc.empty(N, gc.float32), gc.empty(N, gc.float32)]
    return tuple(sc) + (gc.array(base_y), gc.array(ability)) + tuple(outs)


for N in (10_000, 50_000, 250_000):
    args = make_args(N, 3)
    run_sim_step_arrays(gc.backend(), args)          # warm-up (compilation/first-call)
    reps = 5 if N <= 10_000 else 3
    times = []
    for _ in range(reps):
        t = time.perf_counter(); run_sim_step_arrays(gc.backend(), args); times.append(time.perf_counter() - t)
    per = float(np.median(times))
    out["calls"][f"N{N}"] = {"median_s": per, "times_s": [round(x, 6) for x in times]}
out["projection"] = dict(
    exp1_production_calls=7500,
    exp1_projection_s=out["calls"]["N250000"]["median_s"] * 7500,
    exp1_projection_hours=out["calls"]["N250000"]["median_s"] * 7500 / 3600,
    exp3_production_calls=5000,
    exp3_projection_s=out["calls"]["N50000"]["median_s"] * 5000,
    exp3_projection_hours=out["calls"]["N50000"]["median_s"] * 5000 / 3600,
    note="kernel-call cost only; excludes host RNG generation, Python overhead and I/O. Production is NOT run.",
)
json.dump(out, open(os.path.join(RECORD, "results", "projection.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
