#!/usr/bin/env python3
"""Run the transcribed sim_step kernel on one backend and save output arrays (for equivalence comparison)."""
import argparse, os, sys
import numpy as np

RECORD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RECORD)

ap = argparse.ArgumentParser()
ap.add_argument("--backend", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()
os.environ["APPLE_GPU_BACKEND"] = args.backend

import gpu_compat as gc            # noqa: E402
from kernels_np_mlx import run_sim_step_arrays  # noqa: E402

N, year, seed0, seed1 = 2000, 3, 20261125, 34
rng = np.random.Generator(np.random.Philox(20261125))
base_y = np.exp(rng.normal(0.0, 0.55, size=N)).astype(np.float32)
ability = np.clip(rng.normal(1.0, 0.20, size=N), 0.3, 1.8).astype(np.float32)
scalars = [np.int32(N), np.int32(year), np.uint32(seed0), np.uint32(seed1),
           np.float32(0.45), np.float32(0.35), np.float32(0.45), np.float32(0.0),
           np.float32(0.65), np.float32(0.12), np.float32(0.55), np.float32(0.90), np.float32(0.32),
           np.float32(1.4), np.float32(1.3), np.float32(1.6)]
outs = [gc.empty(N, gc.int32), gc.empty(N, gc.int32), gc.empty(N, gc.float32),
        gc.empty(N, gc.float32), gc.empty(N, gc.float32)]
call_args = tuple(scalars) + (gc.array(base_y), gc.array(ability)) + tuple(outs)
res = run_sim_step_arrays(gc.backend(), call_args)
save = {k: gc.asnumpy(v) for k, v in res.items()}
save["backend"] = np.array(gc.backend())
np.savez(args.out, **save)
print("probe", args.backend, "->", {k: np.asarray(v).shape for k, v in save.items() if k != "backend"})
