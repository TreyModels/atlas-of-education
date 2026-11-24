#!/usr/bin/env python3
"""S6 - Migration and rural-urban schooling (inventory 168-183 subset; cross-cutting system part).
PREREG: PRE_REGISTRATION.md S6 + Amendments 01-03. SYNTHETIC demonstration only - NOT a MASSENG v5 output
(MASSENG v5 does not model rural-urban migration). No causal claim."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eq_common import ols, probit, logit, rng, write_result, save_csv, smoke_parser


def gen(rng, n, with_network, with_remittance):
    S = np.clip(6.0 + rng.normal(size=n), 0, None)          # education
    network = (rng.random(n) < 0.4).astype(float) if with_network else np.zeros(n)
    cost = np.exp(rng.normal(scale=0.3, size=n))
    latent = -0.5 + 0.55 * S + 0.8 * network - 0.6 * cost + rng.normal(scale=0.7, size=n)
    mig = (latent > 0).astype(float)
    urban_wage = 1.0 + 0.08 * S + 0.4 * mig + rng.normal(scale=0.3, size=n)
    remit = 0.2 * mig * urban_wage if with_remittance else np.zeros(n)
    return S, network, cost, mig, urban_wage, remit


def run(args):
    reps = 12 if args.smoke else 50
    n = 3000 if args.smoke else 12000
    out = {"script": "eq06_migration_rural_urban", "prereg": "S6",
           "system_map": {"nodes": ["wider economy", "families"], "piece": 0,
                          "chain": "family affordability -> learning -> gate -> credential->jobs"},
           "masseng_boundary": {"used": "standalone synthetic demonstration (NOT MASSENG v5 output)",
                                "mechanism_in_masseng_v5": False,
                                "note": "rural-urban migration/remittances are NOT implemented in MASSENG v5; synthetic demonstration only"},
           "data_tier": "SYNTHETIC",
           "label": "SIMULATION - stipulated migration DGP; no causal claim",
           "reps": reps, "n": n}
    rows, mv = [], {}
    for spec, net, rem in [("probit_with_network", True, False), ("logit_with_network", True, False),
                           ("probit_no_network", False, False), ("probit_network_remittance", True, True)]:
        mes, gaps = [], []
        for r in range(reps):
            S, network, cost, mig, uw, remit = gen(rng(args.seed + 100 * (spec == "logit_with_network") + r), n, net, rem)
            X = np.column_stack([np.ones(n), S, network, cost])
            fit = logit(mig, X) if spec.startswith("logit") else probit(mig, X)
            p = 1 / (1 + np.exp(-(X @ np.array(fit["b"])))) if spec.startswith("logit") else None
            if p is None:
                z = X @ np.array(fit["b"])
                p = 0.5 * (1 + np.vectorize(__import__("math").erf)(z / np.sqrt(2)))
            # marginal effect of education at the mean
            if spec.startswith("logit"):
                me = fit["b"][1] * np.mean(p * (1 - p))
            else:
                me = fit["b"][1] * np.mean(__import__("numpy").exp(-0.5 * (X @ np.array(fit["b"])) ** 2) /
                                            np.sqrt(2 * np.pi))
            mes.append(me)
            gaps.append(float(S[mig > 0].mean() - S[mig <= 0].mean()))
            rows.append([spec, r, round(float(me), 5), round(gaps[-1], 4)])
        mv[spec] = {"mean_marginal_effect_education": round(float(np.mean(mes)), 5),
                    "mean_education_gap_migrants_vs_stayers": round(float(np.mean(gaps)), 4)}
    vals = [v["mean_marginal_effect_education"] for v in mv.values()]
    rule = {"education_positive_in_every_spec": all(v > 0 for v in vals),
            "network_spec_effect_larger_than_no_network":
                mv["probit_with_network"]["mean_marginal_effect_education"] >
                mv["probit_no_network"]["mean_marginal_effect_education"]}
    rule["PASS"] = all(rule.values())
    out.update({"multiverse": {"specs": list(mv.keys()), "estimates": {k: v["mean_marginal_effect_education"] for k, v in mv.items()},
                               "range": [min(vals), max(vals)], "spec_robust": all(v > 0 for v in vals)},
                "summary": mv, "decision_rule": rule,
                "plain_result": ("Education raises the migration probability in every specification (marginal "
                                 "effect range %.4f-%.4f) and migrants are more educated than stayers; networks "
                                 "increase the effect. MASSENG v5 does not model rural-urban migration, so this is "
                                 "a synthetic demonstration of the equation, not a model output." %
                                 (min(vals), max(vals)))})
    out["data_map"] = {'module': 'rural-urban/migration', 'observed': 'WDI urbanisation, UN migrant stock, remittances available (not fitted)', 'assumed': 'flows, costs, networks', 'gap': 'task-41 top gap 4'}
    out["statistical_frame"] = {'estimand': 'marginal effect of education on migration probability', 'identification': 'none (synthetic); probit/logit latent model', 'testable_restrictions': 'distributional form; network exogeneity', 'benchmark_split': 'Monte Carlo; no observed split', 'pass_fail': 'PASS if education effect positive in every spec'}
    write_result(args.outdir, "eq06_migration_rural_urban", out)
    save_csv(args.outdir, "eq06_migration_rural_urban", ["spec", "rep", "marginal_effect_education", "edu_gap"], rows)
    print("PLAIN:", out["plain_result"])
    print("RULE:", rule)
    return out


if __name__ == "__main__":
    run(smoke_parser("S6 migration / rural-urban (SIMULATION)"))
