"""Shared cohort, parameters and CSV plumbing for the Cluster B toy battery.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.

All models are standard-library Python 3 only (numpy is available but NOT used).
Every arm inside a seed consumes the *same* latent draw (budgets, base skill,
opportunity cost, lottery), so counterfactuals are paired and starting
conditions are matched. Seeds are the single reproducibility handle:
    seed = SEED_BASE + rep,  rep in range(REPS)

Nothing here reads or writes outside the cluster_B directory.
"""
import csv
import json
import random

LABEL = "ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence"

# --- Base-model constants (copied from model.py so this battery is standalone) ---
POPULATION = 100
JOBS = 40
PUBLIC_SEATS = 30
PUBLIC_FEE = 1.0
PRIVATE_CAPACITY = 30
PRIVATE_FIXED_COST = 12.0
PRIVATE_SEAT_COST = 1.0
TUITION = 2.0
GROSS_PREMIUM = 4.0          # willingness to pay for a degree before fees
COST_SCALE = 3.5             # opportunity cost uniform on [0, COST_SCALE)
BUDGETS = [1.5, 4.0] * (POPULATION // 2)   # exactly as model.py: not shuffled

# --- Battery protocol ---
SEED_BASE = 20261120
REPS = 500                   # >= 200 per cell; 500 is cheap for these models


def cohort(seed):
    """Identical latent draw order to model.py (seed 41 reproduces model.run).

    budgets: fixed alternating 1.5/4.0 as in model.py (not shuffled).
    base_skill: uniform [0,1); costs: uniform [0,3.5); lottery: a permutation.
    """
    rng = random.Random(seed)
    skill = [rng.random() for _ in range(POPULATION)]
    costs = [COST_SCALE * rng.random() for _ in range(POPULATION)]
    lottery = list(range(POPULATION))
    rng.shuffle(lottery)
    return {
        "seed": seed,
        "budgets": list(BUDGETS),
        "skill": skill,
        "costs": costs,
        "lottery": lottery,
        "rank_pos": {i: k for k, i in enumerate(lottery)},
    }


def seeds(n=REPS):
    return [SEED_BASE + rep for rep in range(n)]


def arm_name(*parts):
    return ":".join(str(p) for p in parts)


def fmt(x):
    """Fixed six-decimal string; empty string for undefined values."""
    if x is None:
        return ""
    return f"{x:.6f}"


RESULT_FIELDS = ["experiment", "arm", "seed", "metric", "value"]


def write_results(path, rows):
    """Write RESULTS.csv: five-column (experiment,arm,seed,metric,value) schema.

    Line 1 is the mandatory label as a '#'-prefixed comment; consumers should
    skip lines starting with '#' (pandas: comment='#') before parsing.
    """
    with open(path, "w", newline="") as f:
        f.write(f"# {LABEL}\n")
        writer = csv.DictWriter(f, fieldnames=RESULT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def write_json(path, payload):
    with open(path, "w") as f:
        json.dump(payload, f, indent=2, sort_keys=False)
        f.write("\n")
