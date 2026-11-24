#!/usr/bin/env python3
"""Parallel rejection-ABC reality check for the Bray six-school patterns.

Splits N prior draws across workers; each worker keeps only its best rows and any
rows that fit all seven patterns, so the parent does not receive millions of dicts.
"""
import argparse, heapq, json, multiprocessing as mp, os, sys
from dataclasses import asdict
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bray_reality_check import TARGETS, RANGES, draw, simulate_bray, zscores


def chunk(args):
    seed, count = args
    rng = np.random.default_rng(seed)
    best = []   # heap of (-max_z, counter, row) -> keep smallest max_z
    acc = []
    for i in range(count):
        p = draw(rng)
        out = simulate_bray(p)
        z = zscores(out)
        mz = float(max(z.values()))
        row = {"max_z": mz, **asdict(p), **out, **{f"z_{k}": float(v) for k, v in z.items()}}
        if mz <= 1.0:
            acc.append(row)
        if len(best) < 10:
            heapq.heappush(best, (-mz, i, row))
        elif mz < -best[0][0]:
            heapq.heapreplace(best, (-mz, i, row))
    return {"n": count, "acc": acc, "top": [b[2] for b in best]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000000)
    ap.add_argument("--workers", type=int, default=96)
    ap.add_argument("--out", default="bray_parallel.json")
    a = ap.parse_args()
    per = a.n // a.workers
    tasks = [(20261125 + i * 1000003, per) for i in range(a.workers)]
    print(f"parallel ABC: {a.n} draws / {a.workers} workers ({per} each)", flush=True)
    with mp.Pool(a.workers) as pool:
        parts = pool.map(chunk, tasks)
    n = sum(p["n"] for p in parts)
    acc = [r for p in parts for r in p["acc"]]
    top = [r for p in parts for r in p["top"]]
    top.sort(key=lambda r: r["max_z"])
    top = top[:20]
    print(f"SIMULATION — Bray reality check (parallel), {n} prior draws, {len(acc)} fit all seven "
          f"({100*len(acc)/max(n,1):.3f}%)", flush=True)
    print(f"best max_z: {top[0]['max_z']:.3f}")
    for k in TARGETS:
        print(f"  {k:22s} target {TARGETS[k][0]:.3f}  best {top[0][k]:.3f}")
    acc_ranges = {}
    if acc:
        print("\naccepted parameter ranges (5th-95th pct):")
        for k in RANGES:
            vals = np.array([r[k] for r in acc], float)
            lo, hi = np.percentile(vals, 5), np.percentile(vals, 95)
            acc_ranges[k] = [float(lo), float(hi)]
            print(f"  {k:18s} {lo:.3f} .. {hi:.3f}")
    payload = {"label": "SIMULATION — Bray six-school reality check, parallel rejection ABC",
               "n_draws": n, "n_fit": len(acc), "fit_share": len(acc) / max(n, 1),
               "targets": TARGETS, "best": top[0], "top20": top,
               "accepted_param_ranges": acc_ranges}
    with open(a.out, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
