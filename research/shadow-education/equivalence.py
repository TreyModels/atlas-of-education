"""Is "favour" a different model from "thin"? An exact check.

In model.py a pupil's three options have utilities
    own teacher      b + favour            (b contains base_demand)
    other teacher    b - other_cost
    commercial       b - commercial_cost
so adding favour = f is the same as raising base_demand, other_cost and the commercial cost by f each.
This script takes every fitted "favour" parameter set, rewrites it as a "thin" parameter set that way,
and compares every model output, with and without each policy lever.
"""
import json
from dataclasses import replace
import numpy as np
from common import RESULTS, World, load_particles

POLICIES = {"none": {}, "ban_own": {"ban_own": True}, "cond_pay": {"cond_pay": 0.3},
            "extra_time": {"extra_time": 0.1}, "com_entry": {"com_entry": 0.5}}
WORLDS = [7_100_000, 7_100_001, 7_100_002]


def as_thin(p):
    f = p.favour
    return replace(p, favour=0.0, base_demand=p.base_demand + f, other_cost=p.other_cost + f,
                   com_cost_urban=p.com_cost_urban + f)


def main():
    params, groups = load_particles("favour")
    first = {g: i for i, g in reversed(list(enumerate(groups)))}
    uniq = [params[i] for i in first.values()]
    out = {"n_parameter_sets": len(uniq), "worlds": len(WORLDS), "policies": {}}
    for name, lever in POLICIES.items():
        worst, worst_key, clamp_cases = 0.0, None, 0
        for p in uniq:
            # com_entry floors the commercial cost at zero; the rewrite is exact only when the floor is not hit.
            if name == "com_entry" and p.com_cost_urban - lever["com_entry"] < 0:
                clamp_cases += 1
            for w in WORLDS:
                a = World(replace(p, **lever), w).solve().outcomes()
                b = World(replace(as_thin(p), **lever), w).solve().outcomes()
                for k in a:
                    if np.isnan(a[k]) and np.isnan(b[k]):
                        continue
                    diff = abs(a[k] - b[k])
                    if diff > worst:
                        worst, worst_key = diff, k
        out["policies"][name] = {"worst_abs_difference": worst, "output_with_worst": worst_key,
                                 "floor_hit_sets": clamp_cases}
    out["favour_range_in_fitted_sets"] = [min(p.favour for p in uniq), max(p.favour for p in uniq)]
    # How many rewritten sets fall outside thin's prior box? (This is the only thing that separates the variants.)
    from common import PRIORS
    outside = 0
    for p in uniq:
        q = as_thin(p)
        ok = all(PRIORS[k][0] <= getattr(q, k) <= PRIORS[k][1] for k in ("base_demand", "other_cost", "com_cost_urban"))
        outside += (not ok)
    out["rewritten_sets_outside_thin_prior_box"] = outside
    (RESULTS / "equivalence.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
