"""Fresh-world check: do calibrated parameter sets fit in school systems they were not calibrated on?

For each posterior particle (all of them), runs the baseline and the own-pupil tutoring ban in each fresh world
(seeds 9,800,000 + j, disjoint from the calibration worlds 5,000,000+ and from the earlier check's 9,700,000+).
Reports:
  pair_fit_rate     share of (particle, fresh world) pairs with all seven patterns inside tolerance
                    (comparable with the earlier 11-18% figure, which used one world per pair)
  particle_survival share of particles that fit in at least 70% of the fresh worlds (14 of 20)
Usage: python fresh_check.py --posterior-dir results --out results/fresh_check.csv
"""
import argparse
import json
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path
import numpy as np
import pandas as pd
from calibrate import distances
from model import World
from smc import to_params

FRESH_WORLDS = [9_800_000 + j for j in range(20)]


def job(args):
    variant, i, names, x, seed = args
    p = to_params(names, x)
    base = World(p, seed).solve().outcomes()
    ban = World(replace(p, ban_own=True), seed).solve().outcomes()
    z = max(distances(base).values())
    return {"variant": variant, "particle": i, "world": seed, "max_z": z, "fit": int(z <= 1),
            "converged": int(base["converged"]), "participation": base["participation"],
            "withholding_mean": base["withholding_mean"],
            "ban_participation": ban["participation"] - base["participation"],
            "ban_nonbuyer_instr": ban["nonbuyer_class_instruction"] - base["nonbuyer_class_instruction"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--posterior-dir", type=Path, default=Path("results"))
    ap.add_argument("--out", type=Path, default=Path("results/fresh_check.csv"))
    ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--variants", nargs="*", default=["thin", "diversion", "favour", "full"])
    a = ap.parse_args()
    jobs, parts = [], {}
    for v in a.variants:
        f = a.posterior_dir / f"posterior_{v}.json"
        if not f.exists():
            print("skip (missing):", f); continue
        d = json.loads(f.read_text())
        parts[v] = len(d["particles"])
        for i, row in enumerate(d["particles"]):
            x = [row[n] for n in d["free"]]
            for s in FRESH_WORLDS:
                jobs.append((v, i, d["free"], x, s))
    with Pool(a.procs) as pool:
        rows = pool.map(job, jobs, chunksize=20)
    df = pd.DataFrame(rows)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.out, index=False)
    summ = []
    for v in parts:
        g = df[df.variant == v]
        per = g.groupby("particle")["fit"].sum()
        summ.append({"variant": v, "particles": parts[v], "worlds": len(FRESH_WORLDS),
                     "pair_fit_rate": round(g["fit"].mean(), 4),
                     "particle_survival_70pct": round((per >= 14).mean(), 4),
                     "converged_share": round(g["converged"].mean(), 4),
                     "ban_participation_median": round(g["ban_participation"].median(), 4),
                     "ban_nonbuyer_instr_median": round(g["ban_nonbuyer_instr"].median(), 5)})
    print(pd.DataFrame(summ).to_string(index=False))
    pd.DataFrame(summ).to_csv(a.out.with_name(a.out.stem + "_summary.csv"), index=False)


if __name__ == "__main__":
    main()
