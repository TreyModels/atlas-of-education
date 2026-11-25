#!/usr/bin/env python3
"""Independent validation seeds for the corrected GPU harness (P0-07).

Why this exists
---------------
The archived run used one fixed seed (20261125) for every job, and the
deposited bundle contains no record of how seeds were chosen.  A corrected
harness must not silently re-use the archived seed: validation runs get
**independently generated** seeds, recorded with the run and hashed into its
manifest, so a reader can tell an independent validation run from a replay.

Default source: the OS CSPRNG (`secrets.randbits(31)`), one seed per job.
`--seed N` switches to a deterministic *derived* mode for reproducible tests
(seeds are derived per job from sha256("N:job_id") and are still not the
archived 20261125 unless N is chosen adversarially).

Usage:
    python3 make_seeds.py --out runs/<id>/seeds.json \
        --jobs job_a,job_b[,job_c] [--seed 12345]

Writes atomically (tmp + os.replace).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import time


def derived_seed(base: int, job_id: str) -> int:
    h = hashlib.sha256(f"{base}:{job_id}".encode("utf-8")).digest()
    return int.from_bytes(h[:4], "big") & 0x7FFFFFFF


def atomic_write_json(path: str, payload: dict) -> None:
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)  # atomic rename on POSIX


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, help="output seeds JSON path")
    ap.add_argument("--jobs", required=True, help="comma-separated job ids")
    ap.add_argument("--seed", type=int, default=None,
                    help="optional base seed for deterministic derived mode")
    args = ap.parse_args()

    jobs = [j.strip() for j in args.jobs.split(",") if j.strip()]
    if not jobs:
        raise SystemExit("no jobs given")

    if args.seed is None:
        seeds = {j: secrets.randbits(31) for j in jobs}
        source = "os_csprng"
        base = None
    else:
        seeds = {j: derived_seed(args.seed, j) for j in jobs}
        source = "derived_from_base_seed"
        base = args.seed

    payload = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": source,
        "base_seed": base,
        "archived_seed_not_reused": 20261125,
        "seeds": seeds,
    }
    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    atomic_write_json(args.out, payload)
    print(f"wrote {args.out} ({source}, {len(seeds)} seeds)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
