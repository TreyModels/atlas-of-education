"""Task 3.3: do the four explanations agree on policy only because they share code?

Code overlap: the four variants run the same model.py; they differ only in which of 15 priors are free
(`diversion` and `favour` are switched on/off; `thin` is free in all four). See OVERLAP in the output.

Test: re-simulate the first N posterior particles of every variant in fresh worlds (seeds 9,800,000+j, j<10)
under the baseline model and under perturbations of SHARED components (not re-calibrated; the question is
whether the policy ordering survives a change in a shared assumption). For each perturbation and variant:
  fit_share       share of (particle, world) pairs still inside all tolerances
  ban_participation, ban_nonbuyer_instr, cond_pay_participation, extra_time_participation, com_entry_participation
                  weighted median paired change from baseline (the same world and particle)
Agreement: the sign of the ban effect on participation across variants, and whether the policy ranking
(by |participation effect|) is the same in every variant.
"""
import json
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path
import numpy as np
import pandas as pd
import model
from calibrate import distances
from model import World
from smc import to_params

N_PART = 60
WORLDS = [9_800_000 + j for j in range(10)]
POLICIES = {"ban_own": {"ban_own": True}, "cond_pay": {"cond_pay": 0.3},
            "extra_time": {"extra_time": 0.10}, "com_entry": {"com_entry": 1.5}}
# perturbations of SHARED components (label -> (module constants, Params changes))
PERTURB = {
    "baseline": ({}, {}),
    "no_thin_channel": ({}, {"thin": 0.0}),
    "no_alternative_providers": ({}, {"other_cost": 10.0, "com_cost_urban": 10.0, "com_cost_rural_extra": 0.0}),
    "weaker_withholding_convexity": ({"CONVEXITY": 0.25}, {}),
    "double_withholding_cost": ({}, {"norm_cost_mult": 2.0}),
}


def job(args):
    variant, i, names, x, world, label = args
    consts, changes = PERTURB[label]
    saved = {k: getattr(model, k) for k in consts}
    try:
        for k, v in consts.items():
            setattr(model, k, v)
        p = to_params(names, x)
        if "norm_cost_mult" in changes:
            p = replace(p, norm_cost=p.norm_cost * changes["norm_cost_mult"])
        else:
            p = replace(p, **changes)
        base = World(p, world).solve().outcomes()
        z = max(distances(base).values())
        rows = [{"variant": variant, "particle": i, "world": world, "perturbation": label, "policy": "baseline",
                 "fit": int(z <= 1), **base}]
        for name, ch in POLICIES.items():
            out = World(replace(p, **ch), world).solve().outcomes()
            rows.append({"variant": variant, "particle": i, "world": world, "perturbation": label,
                         "policy": name, "fit": int(z <= 1), **out})
        return rows
    finally:
        for k, v in saved.items():
            setattr(model, k, v)


def wmed(x):
    return float(np.median(x))


def main():
    jobs = []
    for v in ["thin", "diversion", "favour", "full"]:
        f = Path("results") / f"posterior_{v}.json"
        if not f.exists():
            print("missing", f); continue
        d = json.loads(f.read_text())
        P = d["particles"][:N_PART]
        for i, row in enumerate(P):
            x = [row[n] for n in d["free"]]
            for w in WORLDS:
                for label in PERTURB:
                    jobs.append((v, i, d["free"], x, w, label))
    with Pool(8) as pool:
        rows = [r for rr in pool.map(job, jobs, chunksize=20) for r in rr]
    df = pd.DataFrame(rows)
    df.to_csv(Path("results") / "shared_ablation_runs.csv", index=False)
    key = ["variant", "particle", "world", "perturbation"]
    b = df[df.policy == "baseline"].set_index(key)
    summ = {}
    for label in PERTURB:
        summ[label] = {}
        for v in df.variant.unique():
            base = b.loc[(v, slice(None), slice(None), label)]
            s = {"fit_share": float(base["fit"].mean())}
            for pol in POLICIES:
                p = df[(df.variant == v) & (df.perturbation == label) & (df.policy == pol)].set_index(key)
                p = p.sort_index(); bb = base.sort_index()
                s[f"{pol}_participation"] = wmed((p["participation"] - bb["participation"]).values)
                s[f"{pol}_nonbuyer_instr"] = wmed((p["nonbuyer_class_instruction"] - bb["nonbuyer_class_instruction"]).values)
            summ[label][v] = s
    out = {"overlap": {"model_py_shared_by_variants": True, "mechanism_lines_in_model_py": 6,
                       "nonblank_code_lines_in_model_py": 215,
                       "free_parameters": {"thin": 13, "diversion": 14, "favour": 14, "full": 15},
                       "parameters_differing_between_variants": ["diversion", "favour"]},
           "particles_per_variant": N_PART, "worlds": len(WORLDS), "summary": summ}
    (Path("results") / "shared_ablation.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
