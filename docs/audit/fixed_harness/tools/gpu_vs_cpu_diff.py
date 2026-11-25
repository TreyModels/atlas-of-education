#!/usr/bin/env python3
"""Derived GPU-vs-CPU arithmetic comparison for the corrected harness (real mode).

Reads the two selftest JSONs produced earlier in the same run and writes a diff
artifact atomically. This reproduces the *shape* of the archived
results_gpu_vs_cpu_diff.json, but as an explicit, hashed, first-class job rather
than an ad-hoc artifact (P0-07 fix).

Scope: ARITHMETIC ONLY. Deterministic quantities share identical inputs, so their
difference measures float64 agreement. RNG-dependent quantities differ because
CUDA and CPU generators produce different streams; they are reported separately
and are NOT numerical-error evidence.

Usage:
    gpu_vs_cpu_diff.py --gpu <json> --cpu <json> --out-dir <dir>
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time


def atomic_write_json(path: str, payload: dict) -> None:
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def flatten(d, prefix=""):
    if isinstance(d, dict):
        for k, v in d.items():
            yield from flatten(v, f"{prefix}.{k}" if prefix else k)
    else:
        yield prefix, d


# Quantities that share identical numeric inputs on GPU and CPU (deterministic).
DETERMINISTIC = {
    "wild_cluster.beta1",
    "wild_cluster.se_cr1",
    "wild_cluster.t_obs",
    "block_perm.beta_obs",
}
# Quantities depending on the RNG stream (reported for completeness only).
RNG_DEPENDENT = {
    "wild_cluster.p_wild_cluster",
    "wild_cluster.t_boot_q025",
    "wild_cluster.t_boot_q975",
    "block_perm.p_block_perm",
    "block_perm.perm_mean",
    "block_perm.perm_sd",
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gpu", required=True)
    ap.add_argument("--cpu", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--out-name", default="results_gpu_vs_cpu_diff.json")
    args = ap.parse_args()

    gpu = dict(flatten(json.load(open(args.gpu, encoding="utf-8"))))
    cpu = dict(flatten(json.load(open(args.cpu, encoding="utf-8"))))

    deterministic, rng_dependent = [], []
    for key in sorted(set(gpu) & set(cpu)):
        a, b = gpu[key], cpu[key]
        if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
            continue
        rec = {"stat": key, "gpu": a, "cpu": b, "abs_diff": abs(a - b),
               "rel_diff": (abs(a - b) / max(abs(a), abs(b))) if max(abs(a), abs(b)) else 0.0}
        if key in DETERMINISTIC:
            deterministic.append(rec)
        elif key in RNG_DEPENDENT:
            rng_dependent.append(rec)

    max_abs = max((r["abs_diff"] for r in deterministic), default=0.0)
    max_rel = max((r["rel_diff"] for r in deterministic), default=0.0)
    res = {
        "note": ("Derived GPU-vs-CPU arithmetic comparison (corrected harness). "
                 "Deterministic quantities share identical inputs; their diff measures float64 "
                 "agreement only. RNG-dependent bootstrap/permutation quantities differ by design "
                 "(CUDA vs CPU generator streams) and are not numerical-error evidence."),
        "scope": "ARITHMETIC ONLY - not a scientific validation",
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "inputs": {"gpu": os.path.abspath(args.gpu), "cpu": os.path.abspath(args.cpu)},
        "deterministic_quantities": deterministic,
        "deterministic_max_abs_diff": max_abs,
        "deterministic_max_rel_diff": max_rel,
        "rng_dependent_quantities": rng_dependent,
        "p_wild_cluster_equal": gpu.get("wild_cluster.p_wild_cluster") == cpu.get("wild_cluster.p_wild_cluster"),
        "p_block_perm_equal": gpu.get("block_perm.p_block_perm") == cpu.get("block_perm.p_block_perm"),
    }
    os.makedirs(args.out_dir, exist_ok=True)
    out = os.path.join(args.out_dir, args.out_name)
    atomic_write_json(out, res)
    print(f"wrote {out} (deterministic max abs diff {max_abs:.3e})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
