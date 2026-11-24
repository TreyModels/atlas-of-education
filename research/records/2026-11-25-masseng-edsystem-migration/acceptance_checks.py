#!/usr/bin/env python3
"""Acceptance framing for the migration extension (task-44 follow-up).

Reports, for the migration contrasts:
  1. sign stability without magnitude bounds (strata and seed signs; no effect-size threshold);
  2. naive benchmark (raw mean difference) vs adjusted cluster-robust OLS effect;
  3. Q1 zero-signal control (permute migration labels within design cells; null distribution of the
     naive migration difference; false-positive rate);
  4. cross-margin consistency where data permit: engine tutoring income elasticity vs Dang (2007)
     0.43-0.53 (construct-limited), grade clustering at gates 9/12 from tut_by_grade; study-and-work
     share among the poor is NOT represented in eduengine (reported unavailable).

Simulation only; no causal claims.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "acceptance_migration.json")
RNG = np.random.default_rng(20261126)
N_PERM = 500


def load():
    d = json.load(open(os.path.join(HERE, "results_migration.json")))
    tests = json.load(open(os.path.join(HERE, "migration_tests.json")))
    return d, tests


def metric(r, m):
    v = r["metrics"].get(m)
    return np.nan if v is None else float(v)


def naive_diff(rows, outcome, level):
    vals = {}
    for r in rows:
        mig = r["combo"][-1]  # migration axis is last
        v = metric(r, outcome)
        if np.isfinite(v):
            vals.setdefault(mig, []).append(v)
    a = np.array(vals.get(level, []), float)
    b = np.array(vals.get("closed", []), float)
    if not len(a) or not len(b):
        return None
    return float(a.mean() - b.mean())


def seed_sign_consistency(rows, outcome, level):
    diffs = []
    for sd in sorted({r["seed"] for r in rows}):
        a = [metric(r, outcome) for r in rows if r["seed"] == sd and r["combo"][-1] == level]
        b = [metric(r, outcome) for r in rows if r["seed"] == sd and r["combo"][-1] == "closed"]
        a = [x for x in a if np.isfinite(x)]; b = [x for x in b if np.isfinite(x)]
        if a and b:
            diffs.append(float(np.mean(a) - np.mean(b)))
    if not diffs:
        return None
    return {"n_seeds": len(diffs), "all_same_sign": bool(all(x > 0 for x in diffs) or all(x < 0 for x in diffs)),
            "min": min(diffs), "max": max(diffs)}


def q1_permutation(rows, outcome, level):
    # permute migration labels within each (non-migration combo, seed) cell
    cells = {}
    for i, r in enumerate(rows):
        key = (tuple(r["combo"][:-1]), r["seed"])
        cells.setdefault(key, []).append(i)
    base = [metric(r, outcome) for r in rows]
    obs = naive_diff(rows, outcome, level)
    if obs is None:
        return None
    null = []
    for _ in range(N_PERM):
        a = []; b = []
        for idxs in cells.values():
            labels = [rows[j]["combo"][-1] for j in idxs]
            pl = RNG.permutation(labels)
            for lab, j in zip(pl, idxs):
                v = base[j]
                if not np.isfinite(v):
                    continue
                if lab == level:
                    a.append(v)
                elif lab == "closed":
                    b.append(v)
        if a and b:
            null.append(float(np.mean(a) - np.mean(b)))
    null = np.array(null, float)
    p = float((np.abs(null) >= abs(obs)).mean()) if len(null) else None
    return {"observed": obs, "null_q95_abs": float(np.percentile(np.abs(null), 95)) if len(null) else None,
            "p_perm": p, "n_perm": len(null)}


def auxiliary_income_elasticity():
    """Engine analogue of tutoring expenditure income elasticity: vary y_median, measure per-child
    tutoring spend and mean household income; elasticity across income levels (construct-limited)."""
    sys.path.insert(0, ROOT)
    import worlds  # noqa: E402
    base = dict(afford="cash_only", supply="fixed_budget", learning="plus_private_tutoring",
                gates="bar", jobs="queue", rural="low_penalty", migration="closed")
    out = []
    for ymed in (0.8, 1.0, 1.2):
        spends, incs = [], []
        for seed in range(3):
            mods = dict(private=True, tutoring=True, fiscal=False, labour="queue", migration="closed")
            e = worlds.make("formal_loop", mods=mods, N=400, T=70, measure_from=35, seed=seed,
                            borrow=0.0, need_mode="constant", need_share=0.5, y_median=ymed,
                            gates=[dict(kind="bar", bar=x) for x in (3.0, 5.5, 8.0, 11.5)],
                            budget_per_child=0.06, rural_cost=0.01, urban_share=0.60)
            e.run()
            m = e.p["measure_from"]
            ts = np.array(e.R.get("tut_spend", [])[m:], float)
            spends.append(float(np.nanmean(ts) / e.p["N"]))
            incs.append(float(np.mean(e.kids["y"])))
        out.append({"y_median": ymed, "tut_spend_per_child": float(np.mean(spends)),
                    "mean_income": float(np.mean(incs))})
    xs = np.log([o["mean_income"] for o in out]); ys = np.log([o["tut_spend_per_child"] for o in out])
    slope = float(np.polyfit(xs, ys, 1)[0])
    return {"points": out, "engine_income_elasticity": slope,
            "target_dang_2007": [0.43, 0.53],
            "note": "construct-limited: engine spend per cohort child vs Dang household tutoring-expenditure elasticity; not validation."}


def grade_clustering(rows):
    rates = []
    for r in rows:
        tg = r["arrays"].get("tut_by_grade")
        if tg and len(tg) >= 16:
            rates.append(np.array(tg, float))
    if not rates:
        return None
    m = np.nanmean(np.array(rates, float), 0)
    return {"grade9": float(m[8]), "grade12": float(m[11]),
            "non_gate_mean": float(np.mean(m[[3, 4, 6, 7, 9, 10, 12, 13]])),
            "gate_mean": float(np.mean(m[[5, 8, 11]])),
            "ratio_gate_to_nongate": float(np.mean(m[[5, 8, 11]]) / max(np.mean(m[[3, 4, 6, 7, 9, 10, 12, 13]]), 1e-9))}


def main():
    d, tests = load()
    rows = d["rows"]
    outcomes = ["completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
                "parity_wealth_lower", "tut_rate", "formal_share_gdp", "skill_premium", "q_pub"]
    # adjusted OLS effects from tests file
    adj = {}
    for key, block in tests["contrasts"].items():
        if key.startswith("migration:"):
            for lvl, rs in block.items():
                for r in rs:
                    if r.get("effect") is not None:
                        adj[(lvl, r["outcome"])] = {"effect": r["effect"], "ci": r["ci"],
                                                     "p_holm": r.get("p_holm"),
                                                     "sign_consistent": r.get("sign_consistent")}
    report = {"label": "SIMULATION — migration acceptance framing; toy worlds, no causal claims",
              "naive_vs_adjusted": {}, "sign_stability": {}, "q1_zero_signal": {},
              "cross_margin": {}, "study_and_work": "NOT REPRESENTED in eduengine (child work enters only as forgone-earnings cost)"}
    for lvl in ("low", "high"):
        report["naive_vs_adjusted"][lvl] = {}
        report["sign_stability"][lvl] = {}
        report["q1_zero_signal"][lvl] = {}
        for oc in outcomes:
            nd = naive_diff(rows, oc, lvl)
            report["naive_vs_adjusted"][lvl][oc] = {"naive_diff": nd, "adjusted": adj.get((lvl, oc))}
            report["sign_stability"][lvl][oc] = seed_sign_consistency(rows, oc, lvl)
            report["q1_zero_signal"][lvl][oc] = q1_permutation(rows, oc, lvl)
    report["cross_margin"]["grade_clustering"] = grade_clustering(rows)
    report["cross_margin"]["tutoring_income_elasticity"] = auxiliary_income_elasticity()
    with open(OUT, "w") as f:
        json.dump(report, f, indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "naive_vs_adjusted"}, indent=1, default=str)[:6000])


if __name__ == "__main__":
    main()
