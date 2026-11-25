#!/usr/bin/env python3
"""Tiny CPU-only stub experiment used by the corrected harness dry-run.

No CUDA, no torch, tiny n (default 8): it exists only to exercise the harness
machinery (unique output dirs, atomic JSON writes, exit-code propagation).
The result file is written atomically (tmp + fsync + os.replace).
"""
from __future__ import annotations

import argparse
import json
import os
import random


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--job-id", default="stub")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()

    os.makedirs(a.out_dir, exist_ok=True)
    rng = random.Random(a.seed)
    xs = [rng.random() for _ in range(a.n)]
    res = {
        "stub": "ok",
        "job_id": a.job_id,
        "n": a.n,
        "seed": a.seed,
        "sum": sum(xs),
        "sum_sq": sum(x * x for x in xs),
        "note": "dry-run stub; not a scientific experiment",
    }
    out = os.path.join(a.out_dir, "result.json")
    tmp = out + f".tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, out)  # atomic rename
    print(json.dumps(res, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
