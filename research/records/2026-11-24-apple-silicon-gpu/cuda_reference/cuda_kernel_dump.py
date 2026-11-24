"""Dump per-household CUDA sim_step outputs for bit-level port comparison.

For a fixed seed and fixed scalar configuration, launch the *upstream, unmodified*
CUDA kernel (KERNEL_SRC imported from the suite) and save the five output arrays,
plus the input arrays, to an .npz. The Apple port regenerates the same inputs from
NumPy Philox (its declared mapping) and compares its NumPy/MLX transcription
against these arrays, household by household.
"""
import hashlib
import json
import os
import sys
import time

import numpy as np
import cupy as cp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "scripts"))
from exp1_unified_gpu_abm import KERNEL_SRC, DGPS  # noqa: E402

RESULTS = os.path.join(HERE, "results")
os.makedirs(RESULTS, exist_ok=True)

N = 10000
SEED = 20261125
THREADS = 256
BLOCKS = (N + THREADS - 1) // THREADS


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    mod = cp.RawModule(code=KERNEL_SRC)
    kern = mod.get_function("sim_step")

    # Input recipe = the port's declared data stream (NumPy Philox, float64 draw
    # then float32 cast, exactly as the suite asks CuPy for float32).
    g = np.random.Generator(np.random.Philox(SEED))
    base_y_np = g.normal(0.0, 0.55, size=N).astype(np.float32)
    ability_np = np.clip(g.normal(1.0, 0.20, size=N).astype(np.float32),
                         np.float32(0.3), np.float32(1.8)).astype(np.float32)
    base_y = cp.asarray(base_y_np)
    ability = cp.asarray(ability_np)

    state_out = cp.empty(N, dtype=cp.int32)
    tutor_out = cp.empty(N, dtype=cp.int32)
    learn_out = cp.empty(N, dtype=cp.float32)
    work_out = cp.empty(N, dtype=cp.float32)
    y_hh_out = cp.empty(N, dtype=cp.float32)

    meta = {
        "n": N, "seed": SEED, "threads": THREADS, "blocks": int(BLOCKS),
        "batch_N": N, "cupy": cp.__version__, "numpy": np.__version__,
        "cuda_device": cp.cuda.runtime.getDeviceProperties(0)["name"].decode(),
        "kernel_sha256": hashlib.sha256(KERNEL_SRC.encode()).hexdigest(),
        "data_stream": "numpy Philox(seed) -> float64 normal -> float32 (port mapping)",
        "launches": [],
    }

    arrays = {"base_y": base_y_np, "ability": ability_np}
    t0 = time.perf_counter()
    for dgp, p in DGPS.items():
        for t in (0, 12):
            f_pub = 0.45 if t < 10 else 0.0
            h_hid = 0.35
            psi = 0.45
            ban = 0.0
            y_sub = 0.90 * (0.985 ** t)
            launch = dict(
                dgp=dgp, year=t, seed0=SEED, seed1=t + 17, f_pub=f_pub,
                h_hidden=h_hid, psi=psi, ban=ban, q_pub=0.65,
                diversion_beta=p["div"], w_child=0.55, y_sub=y_sub,
                shadow_cost=0.32, w_pov=p["w_pov"], w_push=p["w_push"],
                w_tutor=p["w_tutor"],
            )
            kern((BLOCKS,), (THREADS,), (
                np.int32(N), np.int32(t), np.uint32(SEED), np.uint32(t + 17),
                np.float32(f_pub), np.float32(h_hid), np.float32(psi), np.float32(ban),
                np.float32(0.65), np.float32(p["div"]), np.float32(0.55),
                np.float32(y_sub), np.float32(0.32),
                np.float32(p["w_pov"]), np.float32(p["w_push"]), np.float32(p["w_tutor"]),
                base_y, ability, state_out, tutor_out, learn_out, work_out, y_hh_out,
            ))
            cp.cuda.Stream.null.synchronize()
            key = f"{dgp}_t{t}"
            arrays[f"state_{key}"] = cp.asnumpy(state_out)
            arrays[f"tutor_{key}"] = cp.asnumpy(tutor_out)
            arrays[f"learn_{key}"] = cp.asnumpy(learn_out)
            arrays[f"work_{key}"] = cp.asnumpy(work_out)
            arrays[f"y_hh_{key}"] = cp.asnumpy(y_hh_out)
            launch["key"] = key
            meta["launches"].append(launch)
    meta["wall_s"] = round(time.perf_counter() - t0, 3)

    out_npz = os.path.join(RESULTS, "cuda_kernel_dump.npz")
    np.savez_compressed(out_npz, **arrays)
    meta["npz_sha256"] = sha256(out_npz)
    meta["npz_bytes"] = os.path.getsize(out_npz)
    meta["array_shapes"] = {k: list(v.shape) for k, v in arrays.items()}
    with open(os.path.join(RESULTS, "cuda_kernel_dump_manifest.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"dumped {len(meta['launches'])} launches -> {out_npz} "
          f"({meta['npz_bytes']} bytes, {meta['wall_s']}s)")


if __name__ == "__main__":
    main()
