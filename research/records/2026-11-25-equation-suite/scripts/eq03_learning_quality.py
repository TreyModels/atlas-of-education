#!/usr/bin/env python3
"""S2 - Education production: Cobb-Douglas vs CES, complementarity (inventory 26-41).
PREREG: PRE_REGISTRATION.md S2. SIMULATION ONLY; no causal claim."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eq_common import ols, rng, write_result, save_csv, smoke_parser

OMEGA = 0.6


def ces(S, T, rho):
    return (OMEGA * np.power(S, rho) + (1 - OMEGA) * np.power(T, rho)) ** (1.0 / rho)


def gen(rng, n, rho_world):
    a = rng.normal(size=n)
    S = 5.0 + 1.2 * a + 0.8 * rng.normal(size=n)
    T = 2.0 + 1.0 * a + 1.0 * rng.normal(size=n)
    S = np.clip(S, 0.5, None); T = np.clip(T, 0.1, None)
    if rho_world == 1.0:
        tech = OMEGA * S + (1 - OMEGA) * T
    else:
        tech = ces(S, T, rho_world)
    A = np.clip(1.0 * tech + 0.4 * a + 0.2 * rng.normal(size=n), 0.05, None)
    return S, T, a, A


def interaction(A, S, T, a=None):
    X = [np.ones_like(S), S, T, S * T]
    if a is not None:
        X.append(a)
    return ols(A, np.column_stack(X))["b"][3]


def fit_ces_rho(A, S, T, grid):
    best = None
    for rho in grid:
        y = np.power(np.clip(A, 1e-6, None), rho)
        X = np.column_stack([np.ones_like(S), np.power(np.clip(S, 1e-6, None), rho),
                             np.power(np.clip(T, 1e-6, None), rho)])
        fit = ols(y, X)
        sse = float(np.sum((y - X @ np.array(fit["b"])) ** 2))
        if best is None or sse < best[1]:
            best = (float(rho), sse)
    return best[0]


def cobb_douglas_rmse(A, S, T):
    fit = ols(np.log(np.clip(A, 1e-6, None)),
              np.column_stack([np.ones_like(S), np.log(S), np.log(T)]))
    pred = np.exp(np.column_stack([np.ones_like(S), np.log(S), np.log(T)]) @ np.array(fit["b"]))
    return float(np.sqrt(np.mean((A - pred) ** 2)))


def run(args):
    reps = 30 if args.smoke else 150
    n = 800 if args.smoke else 4000
    grid = np.round(np.arange(0.2, 1.0001, 0.05), 2)
    out = {"script": "eq03_learning_quality", "prereg": "S3", "data_tier": "SYNTHETIC",
           "label": "SIMULATION - stipulated CES production DGP; no causal claim",
           "reps": reps, "n": n, "omega": OMEGA}
    rows, summary = [], {}
    for world, rho in [("linear_null_rho1", 1.0), ("ces_complementary_rho0.5", 0.5)]:
        ic_naive, ic_oracle, rho_hat, cd_rmse, ces_rmse = [], [], [], [], []
        for r in range(reps):
            S, T, a, A = gen(rng(args.seed + (1 if rho == 1.0 else 2) * 10000 + r), n, rho)
            ic_naive.append(interaction(A, S, T))
            ic_oracle.append(interaction(A, S, T, a))
            rh = fit_ces_rho(A, S, T, grid)
            rho_hat.append(rh)
            cd_rmse.append(cobb_douglas_rmse(A, S, T))
            Xr = np.column_stack([np.ones_like(S), np.power(S, rh), np.power(T, rh)])
            pred = np.power(np.clip(Xr @ np.linalg.lstsq(Xr, np.power(A, rh), rcond=None)[0], 1e-6, None),
                            1.0 / rh)
            ces_rmse.append(float(np.sqrt(np.mean((A - pred) ** 2))))
            rows.append([world, r, round(ic_naive[-1], 4), round(ic_oracle[-1], 4), rh,
                         round(cd_rmse[-1], 4), round(ces_rmse[-1], 4)])
        summary[world] = {
            "true_rho": rho,
            "mean_interaction_ability_omitted": round(float(np.mean(ic_naive)), 4),
            "mean_interaction_ability_controlled": round(float(np.mean(ic_oracle)), 4),
            "median_rho_hat": float(np.median(rho_hat)),
            "share_rho_hat_within_0.10": round(float(np.mean(np.abs(np.array(rho_hat) - rho) <= 0.10)), 2),
            "mean_rmse_cobb_douglas": round(float(np.mean(cd_rmse)), 4),
            "mean_rmse_ces": round(float(np.mean(ces_rmse)), 4),
        }
    lin, comp = summary["linear_null_rho1"], summary["ces_complementary_rho0.5"]
    rule = {
        "linear_world_interaction_oracle_CI_includes_0": abs(lin["mean_interaction_ability_controlled"]) <= 2 * 0.02,
        "complementary_world_interaction_oracle_positive": comp["mean_interaction_ability_controlled"] > 0,
        "rho_recovered_within_0.10_in_half_reps": comp["share_rho_hat_within_0.10"] >= 0.5,
        "ces_beats_cd_rmse_in_complementary_world": comp["mean_rmse_ces"] < comp["mean_rmse_cobb_douglas"],
    }
    rule["PASS"] = all(rule.values())
    mv = {"specs": ["linear_interaction_ability_omitted", "linear_interaction_ability_controlled"],
          "estimates": {"linear_interaction_ability_omitted": comp["mean_interaction_ability_omitted"],
                        "linear_interaction_ability_controlled": comp["mean_interaction_ability_controlled"]},
          "fit_specs": {"ces_rho_hat": comp["median_rho_hat"], "cobb_douglas_implied_rho": 1.0,
                        "linear_null_rho": 1.0},
          "range_interaction": [min(comp["mean_interaction_ability_omitted"], comp["mean_interaction_ability_controlled"]),
                                max(comp["mean_interaction_ability_omitted"], comp["mean_interaction_ability_controlled"])]}
    mv["spec_robust"] = (comp["mean_interaction_ability_controlled"] > 0) == (comp["mean_interaction_ability_omitted"] > 0)
    out.update({"summary": summary, "multiverse": mv, "decision_rule": rule,
                "system_map": {"nodes": ["learning", "schools-state"], "piece": 2, "chain": "family affordability -> learning -> gate -> credential->jobs"},
           "masseng_boundary": {"used": "standalone synthetic demonstration (NOT MASSENG v5 output)", "mechanism_in_masseng_v5": False, "note": "standalone synthetic demonstration; not a MASSENG v5 output"},
                "plain_result": ("In the CES world the ability-controlled interaction is positive (%.3f) and the "
                                 "CES fit beats Cobb-Douglas on RMSE (%.3f vs %.3f); in the linear null world the "
                                 "controlled interaction is near zero (%.3f). This is a demonstration about "
                                 "estimators, not evidence about any school system." %
                                 (comp["mean_interaction_ability_controlled"], comp["mean_rmse_ces"],
                                  comp["mean_rmse_cobb_douglas"], lin["mean_interaction_ability_controlled"]))})
    out["data_map"] = {'module': 'learning/quality', 'observed': 'PISA/TIMSS/PIRLS/SACMEQ anchors available (not fitted)', 'assumed': 'production technology and parameters', 'gap': 'task-41 top gap 2'}
    out["statistical_frame"] = {'estimand': 'input returns and CES-vs-Cobb-Douglas fit', 'identification': 'known synthetic DGP; ability control vs omission', 'testable_restrictions': 'CES/CD functional forms', 'benchmark_split': 'Monte Carlo; no observed split', 'pass_fail': 'PASS if ability-controlled interaction positive in the CES world and rho recovered'}
    write_result(args.outdir, "eq03_learning_quality", out)
    save_csv(args.outdir, "eq03_learning_quality",
             ["world", "rep", "interaction_naive", "interaction_oracle", "rho_hat", "rmse_cd", "rmse_ces"], rows)
    print("PLAIN:", out["plain_result"])
    print("RULE:", rule)
    return out


if __name__ == "__main__":
    run(smoke_parser("S2 production functions / CES complementarity (SIMULATION)"))
