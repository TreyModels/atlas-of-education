#!/usr/bin/env python3
"""S1 - Family budgets and schooling demand (inventory 11-25; massification, piece 1).
PREREG: PRE_REGISTRATION.md S1 + Amendments 01-03. SYNTHETIC demonstration only - NOT a MASSENG v5 output.
No causal claim."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eq_common import ols, rng, write_result, save_csv, smoke_parser

DEMAND = lambda z, a, wc, credit: np.clip(9.0 + 1.2 * z + 0.8 * a - 0.5 * wc - (2.0 if credit else 0.0), 0, None)


def gen(rng, n, spec, strength):
    z = rng.normal(size=n)
    y = np.exp(z)
    a = 0.4 * z + rng.normal(size=n)
    wc = np.exp(0.3 * z + rng.normal(scale=0.3, size=n))       # child wage (forgone earnings)
    if spec == "income_only":
        S = DEMAND(z, a, 0.0, False)
    elif spec == "forgone_earnings":
        S = DEMAND(z, a, wc, False)
    else:  # credit_constrained
        S = np.minimum(DEMAND(z, a, 0.0, False), np.maximum(0.0, (y - 1.0) / 1.0))
    births = np.clip(6.0 - strength * S - 0.6 * z + 0.3 * rng.normal(size=n), 0, None)
    return z, y, S, births


def estimates(z, y, S, births, spec, strength):
    ln_y = z
    # income elasticity of schooling: dS/dln y / mean S
    m = ols(S, np.column_stack([np.ones_like(z), ln_y]))
    elas = m["b"][1] / max(float(np.mean(S)), 1e-9)
    naive = ols(births, np.column_stack([np.ones_like(z), S]))["b"][1]
    ctrl = ols(births, np.column_stack([np.ones_like(z), S, ln_y]))["b"][1]
    return {"spec": spec, "strength": strength, "mean_schooling": round(float(np.mean(S)), 3),
            "income_elasticity_schooling": round(float(elas), 4),
            "births_on_schooling_naive": round(float(naive), 4),
            "births_on_schooling_income_control": round(float(ctrl), 4)}


def run(args):
    reps = 12 if args.smoke else 50
    n = 3000 if args.smoke else 15000
    out = {"script": "eq01_family_demand", "prereg": "S1",
           "system_map": {"nodes": ["families"], "piece": 1,
                          "chain": "family affordability -> learning -> gate -> credential->jobs"},
           "masseng_boundary": {"used": "standalone synthetic demonstration (NOT MASSENG v5 output)",
                                "mechanism_in_masseng_v5": True,
                                "note": "affordability/progression are inside MASSENG v5; these numbers are an equation demonstration, not a MASSENG run. Borrowing is NOT implemented in MASSENG v5; the credit-constrained spec is synthetic only."},
           "data_tier": "SYNTHETIC",
           "label": "SIMULATION - stipulated household demand DGP; no causal claim",
           "reps": reps, "n": n}
    rows, mv = [], {}
    for spec in ["income_only", "forgone_earnings", "credit_constrained"]:
        for strength in [0.0, 0.35]:
            elas, ctrl = [], []
            for r in range(reps):
                z, y, S, births = gen(rng(args.seed + 100 * (["income_only", "forgone_earnings", "credit_constrained"].index(spec)) + r), n, spec, strength)
                e = estimates(z, y, S, births, spec, strength)
                elas.append(e["income_elasticity_schooling"])
                ctrl.append(e["births_on_schooling_income_control"])
                rows.append(["%s_s%.2f" % (spec, strength), r, e["income_elasticity_schooling"],
                             e["births_on_schooling_naive"], e["births_on_schooling_income_control"]])
            mv["%s_s%.2f" % (spec, strength)] = {
                "mean_income_elasticity_schooling": round(float(np.mean(elas)), 4),
                "mean_births_coef_income_control": round(float(np.mean(ctrl)), 4)}
    income_elasts = [v["mean_income_elasticity_schooling"] for k, v in mv.items()]
    zero_ctrl = [v["mean_births_coef_income_control"] for k, v in mv.items() if k.endswith("s0.00")]
    rule = {"affordability_positive_across_specs": all(x > 0 for x in income_elasts),
            "forgone_earnings_reduces_schooling": mv["forgone_earnings_s0.35"]["mean_income_elasticity_schooling"]
                                                   < mv["income_only_s0.35"]["mean_income_elasticity_schooling"],
            "zero_signal_association_absorbed_by_income": all(abs(x) < 0.1 for x in zero_ctrl)}
    rule["PASS"] = all(rule.values())
    out.update({"multiverse": {"specs": ["income_only", "forgone_earnings", "credit_constrained"],
                               "estimates": mv,
                               "income_elasticity_range": [min(income_elasts), max(income_elasts)],
                               "spec_robust": all(x > 0 for x in income_elasts)},
                "summary": mv, "decision_rule": rule,
                "plain_result": ("Family income raises schooling demand in every budget specification (income "
                                 "elasticity range %.2f-%.2f), forgone earnings reduce it, and at zero schooling "
                                 "effect on births the raw schooling-births association is absorbed once income is "
                                 "controlled. This is a demonstration of budget arithmetic, not an estimate of any "
                                 "country's demand." % (min(income_elasts), max(income_elasts)))})
    out["data_map"] = {'module': 'household demand/affordability', 'observed': 'no usable public household demand micro panel (DHS IR gated; no fees/forgone panel)', 'assumed': 'all budget/credit parameters', 'gap': 'task-41 top gap 1'}
    out["statistical_frame"] = {'estimand': 'income elasticity of schooling demand by level; schooling-births association', 'identification': 'none (simulation); zero-signal control separates strength from income', 'testable_restrictions': 'budget adds up; credit binds only in that spec', 'benchmark_split': 'Monte Carlo reps; no observed split', 'pass_fail': 'PASS if income elasticity positive across specs and zero-signal absorbed by income control'}
    write_result(args.outdir, "eq01_family_demand", out)
    save_csv(args.outdir, "eq01_family_demand", ["spec", "rep", "income_elasticity", "births_naive", "births_income_ctrl"], rows)
    print("PLAIN:", out["plain_result"])
    print("RULE:", rule)
    return out


if __name__ == "__main__":
    run(smoke_parser("S1 family budgets/demand (SIMULATION)"))
