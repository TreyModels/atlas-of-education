"""Run the three Cluster E toy experiments and write RESULTS.csv. Stdlib only.

ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence.
"""
import platform
import time
from pathlib import Path

import common
import exp13_migration
import exp14_sector
import exp15_diffusion

N_SEEDS = 200
SEED_BASE = 20261120
EXPERIMENTS = [
    (exp13_migration, SEED_BASE),
    (exp14_sector, SEED_BASE + 200000),
    (exp15_diffusion, SEED_BASE + 400000),
]


def main():
    t0 = time.time()
    rows = []
    for module, base in EXPERIMENTS:
        seeds = [base + i for i in range(N_SEEDS)]
        rows.extend(module.run(seeds))
    out = Path(__file__).resolve().parents[1] / "RESULTS.csv"
    n = common.write_csv(rows, out)
    print(f"wrote {out} ({n} rows, {N_SEEDS} seeds/cell, {time.time()-t0:.1f}s)")
    print("threshold verdicts:")
    for r in rows:
        if r["verdict"]:
            print(f"  {r['experiment']:28s} {r['threshold_id']:10s} "
                  f"value={float(r['value']):9.4f} {r['verdict']}")


if __name__ == "__main__":
    main()
