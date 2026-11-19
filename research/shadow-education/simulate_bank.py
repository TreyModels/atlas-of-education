"""Simulate every fitted parameter set of every explanation in fresh school systems and keep ALL outputs.

One row = one fitted parameter set run in one fresh six-school system (a "world"). The published Siem Reap data
are one such system, so each row is one pretend dataset whose true explanation we know.
World seeds start at 7,200,000: disjoint from calibration (5,000,000+) and the repo's fresh checks (9,700,000+, 9,800,000+).
"""
import sys
import pandas as pd
from common import RESULTS, VARIANT_NAMES, World, load_particles, with_gap

WORLDS_PER_SET = int(sys.argv[1]) if len(sys.argv) > 1 else 30


def main():
    rows, seed = [], 7_200_000
    for v in VARIANT_NAMES:
        params, groups = load_particles(v)
        for i, (p, g) in enumerate(zip(params, groups)):
            for j in range(WORLDS_PER_SET):
                o = with_gap(World(p, seed).solve().outcomes())
                rows.append({"variant": v, "particle": i, "group": g, "world": seed, **o})
                seed += 1
        print(v, "done", flush=True)
    pd.DataFrame(rows).to_csv(RESULTS / "bank.csv.gz", index=False)


if __name__ == "__main__":
    main()
