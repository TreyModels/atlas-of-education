"""Sample the prior for each mechanism variant, simulate across K calibration worlds, and screen against
Siem Reap patterns.

A parameter set is scored on K = 10 random school systems ("worlds"; same world seeds for every parameter set).
Per world, z_k = largest standardized deviation across patterns; the set's distance D is the 7th smallest z_k
(FIT_RANK = 6), so D <= 1 exactly when at least 7 of the 10 worlds fit every pattern ("fit in most").
"""
import argparse
import csv
from dataclasses import asdict
from multiprocessing import Pool
from pathlib import Path
import numpy as np
from model import VARIANTS, draw_params, run

# Published patterns (Bray et al. 2016; Bray et al. 2018). Each has a tolerance band.
TARGETS = {
    "participation":       (0.819, 0.03),   # 1,274 Grade 9 and 12 pupils, six schools
    "participation_g9":    (0.747, 0.04),
    "participation_g12":   (0.898, 0.04),
    "urban_rural_gap":     (0.026, 0.04),   # 83.5% urban vs 80.9% semi-urban and rural
    "own_purchase_share":  (0.577, 0.07),   # tutored pupils naming their own teacher (three schools)
    "other_purchase_share": (0.409, 0.07),  # another teacher in their school; the two sum to 98.6%
    "teacher_tutor_share": (0.54, 0.20),    # 13 of 24 interviewed teachers offered tutoring
}
COM_MAX = 0.05                              # remaining 1.4% of answers; commercial provision "still small"

# Calibration worlds: fixed seeds shared by all parameter sets (common random numbers).
# Fresh-world checks use other seed ranges (see fresh_check.py).
CAL_WORLDS = [5_000_000 + k for k in range(10)]
K_WORLDS = len(CAL_WORLDS)
FIT_RANK = 6                                # 0-based index of the 7th smallest of 10 world distances


def distances(o):
    o = dict(o, urban_rural_gap=o["participation_urban"] - o["participation_rural"])
    z = {k: abs(o[k] - v) / tol for k, (v, tol) in TARGETS.items()}
    z["com_purchase_share"] = max(0.0, o["com_purchase_share"] - COM_MAX) / 0.05
    return z


def score_worlds(params, worlds=CAL_WORLDS):
    """Run one parameter set in each world. Returns (D, mean outcomes over worlds, per-world max z)."""
    outs, zs = [], []
    for w in worlds:
        o = run(params, int(w))
        outs.append(o)
        zs.append(max(distances(o).values()))
    zs = np.array(zs)
    D = float(np.sort(zs)[FIT_RANK])
    mean_out = {k: float(np.mean([o[k] for o in outs])) for k in outs[0]}
    return D, mean_out, zs


def job(args):
    variant, index, seed = args
    rng = np.random.default_rng(seed)
    params = draw_params(rng, variant)
    D, mean_out, zs = score_worlds(params)
    row = {"variant": variant, "index": index, "seed": seed, **asdict(params), **mean_out,
           "max_z": D, "fit_worlds": int((zs <= 1).sum()), "accepted": int(D <= 1)}
    row.update({f"world_max_z_{k}": float(v) for k, v in enumerate(zs)})
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=25000, help="prior draws per variant")
    ap.add_argument("--out", type=Path, default=Path("results/prior_runs.csv"))
    ap.add_argument("--procs", type=int, default=2)
    a = ap.parse_args()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    jobs = [(v, i, 1_000_000 * (j + 1) + i) for j, v in enumerate(VARIANTS) for i in range(a.n)]
    with Pool(a.procs) as pool, a.out.open("w", newline="") as f:
        writer = None
        for row in pool.imap(job, jobs, chunksize=50):
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=list(row))
                writer.writeheader()
            writer.writerow(row)


if __name__ == "__main__":
    main()
