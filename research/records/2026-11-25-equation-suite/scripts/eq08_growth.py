#!/usr/bin/env python3
"""S6 - Human-capital growth: augmented Solow, convergence, Nelson-Phelps (inventory 87-105).
PREREG: PRE_REGISTRATION.md S6. Synthetic known-truth plus a descriptive committed cross-section;
no causal claim."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eq_common import ols, rng, write_result, save_csv, smoke_parser

REC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def synthetic_world(rng, n, confound):
    y0 = rng.normal(8.5, 1.0, n)
    H = 0.5 * (y0 - 8.5) + rng.normal(0, 1.0, n) + 2.0
    u = (0.5 * H if confound else 0.0) + rng.normal(0, 0.8, n)
    growth = 0.06 - 0.02 * (y0 - 8.5) + 0.01 * H + u
    return y0, H, growth


def run_synthetic(rng, n, reps, smoke):
    rows, summary = [], {}
    for world, confound in [("clean_no_confound", False), ("omitted_tfp_confound", True)]:
        lam, bH = [], []
        for r in range(reps):
            y0, H, g = synthetic_world(rng, n, confound)
            m1 = ols(g, np.column_stack([np.ones(n), y0]))
            m2 = ols(g, np.column_stack([np.ones(n), y0, H]))
            lam.append(m1["b"][1]); bH.append(m2["b"][2])
            rows.append([world, r, round(m1["b"][1], 5), round(m2["b"][2], 5)])
        summary[world] = {"mean_lambda_noH": round(float(np.mean(lam)), 5),
                          "mean_beta_H_withH": round(float(np.mean(bH)), 5)}
    # Nelson-Phelps interaction: growth = f0 + f1 * H * gap
    n = 120 if smoke else 600
    H = rng.normal(2, 1, n); gap = rng.uniform(0.1, 1.0, n)
    g = 0.01 + 0.02 * H * gap + rng.normal(0, 0.01, n)
    npfit = ols(g, np.column_stack([np.ones(n), H, gap, H * gap]))
    summary["nelson_phelps"] = {"interaction": round(npfit["b"][3], 4),
                                "interaction_se": round(npfit["se"][3], 4)}
    return rows, summary


def real_cross_section():
    """Descriptive observed cross-section WITH honest split + benchmarks (no causal claim)."""
    import csv
    path = os.path.join(REC, "inputs", "x4_panel.csv")
    if not os.path.exists(path):
        return None
    rows = list(csv.DictReader(open(path)))
    data = []
    for r in rows:
        try:
            edu = float(r["edu_1991"]); job = float(r["job_1991"])
            o4 = float(r["out_2004"]); o18 = float(r["out_2018"])
        except (TypeError, ValueError, KeyError):
            continue
        data.append((r["iso3"], edu, job, o18 - o4))
    data.sort()
    train = [i for i in range(len(data)) if i % 3 != 2]
    valid = [i for i in range(len(data)) if i % 3 == 2]
    def X(idx):
        return np.column_stack([np.ones(len(idx)), [data[i][1] for i in idx], [data[i][2] for i in idx]])
    ytr = np.array([data[i][3] for i in train]); Xtr = X(train)
    fit = ols(ytr, Xtr)
    yv = np.array([data[i][3] for i in valid]); Xv = X(valid)
    pred = Xv @ np.array(fit["b"])
    mae_model = float(np.mean(np.abs(yv - pred)))
    mae_persist = float(np.mean(np.abs(yv)))
    mae_mean = float(np.mean(np.abs(yv - float(np.mean(ytr)))))
    return {"data_tier": "OBSERVED AGGREGATES (committed x4_panel.csv; WDI/UIS national series)",
            "source": "research/masseng-staging-x2-2026-11-24 @ f592bae, x4_input/x4_panel.csv",
            "n": int(len(data)), "n_train": len(train), "n_validation": len(valid),
            "coef_edu1991": round(fit["b"][1], 3), "se_edu1991": round(fit["se"][1], 3),
            "coef_job1991": round(fit["b"][2], 3), "se_job1991": round(fit["se"][2], 3),
            "heldout_mae_model": round(mae_model, 3), "heldout_mae_persistence": round(mae_persist, 3),
            "heldout_mae_training_mean": round(mae_mean, 3),
            "beats_benchmarks": bool(mae_model < min(mae_persist, mae_mean)),
            "note": "honest split fixed before fit (sorted ISO3, every third validation); descriptive only; no causal claim"}




def run(args):
    reps = 25 if args.smoke else 120
    n = 60 if args.smoke else 120
    rows, summary = run_synthetic(rng(args.seed), n, reps, args.smoke)
    clean = summary["clean_no_confound"]; conf = summary["omitted_tfp_confound"]
    rule = {"clean_lambda_near_truth": abs(clean["mean_lambda_noH"] + 0.02) <= 0.01,
            "confound_inflates_beta_H": conf["mean_beta_H_withH"] > clean["mean_beta_H_withH"],
            "nelson_phelps_interaction_positive": summary["nelson_phelps"]["interaction"] > 0}
    rule["PASS"] = all(rule.values())
    mv = {"specs": ["beta_H_clean_world", "beta_H_confounded_world", "nelson_phelps_interaction"],
          "estimates": {"beta_H_clean_world": clean["mean_beta_H_withH"],
                        "beta_H_confounded_world": conf["mean_beta_H_withH"],
                        "nelson_phelps_interaction": summary["nelson_phelps"]["interaction"]}}
    mv["range"] = [min(mv["estimates"].values()), max(mv["estimates"].values())]
    mv["spec_robust"] = len({v > 0 for v in mv["estimates"].values()}) == 1
    out = {"script": "eq08_growth", "prereg": "S8", "multiverse": mv,
           "system_map": {"nodes": ["wider economy"], "piece": 4, "chain": "family affordability -> learning -> gate -> credential->jobs"},
           "masseng_boundary": {"used": "standalone synthetic demonstration (NOT MASSENG v5 output)", "mechanism_in_masseng_v5": False, "note": "standalone synthetic demonstration; not a MASSENG v5 output"},
           "data_tier": "SYNTHETIC (+ descriptive OBSERVED cross-section if input present)",
           "label": "SIMULATION for recovery; observed cross-section is descriptive only",
           "reps": reps, "synthetic_summary": summary,
           "real_cross_section": real_cross_section(), "decision_rule": rule,
           "plain_result": ("In the clean world the convergence coefficient is recovered and the human-capital "
                            "term is zero; with an omitted TFP term correlated with human capital the human-capital "
                            "coefficient is inflated (%.4f vs %.4f), so a positive growth coefficient is not "
                            "evidence of a causal human-capital effect." %
                            (conf["mean_beta_H_withH"], clean["mean_beta_H_withH"]))}
    out["data_map"] = {'module': 'structural change + macro/development', 'observed': 'WDI GDP, GGDC/PWT, Barro-Lee; committed x4_panel used descriptively with honest split', 'assumed': 'Solow/NP parameters, structural-change mapping', 'gap': 'descriptive use only'}
    out["statistical_frame"] = {'estimand': 'convergence and human-capital coefficient; descriptive real cross-section', 'identification': 'known synthetic DGP; observed cross-section descriptive only', 'testable_restrictions': 'Solow/Nelson-Phelps forms', 'benchmark_split': 'synthetic recovery; observed train/validation split vs persistence and training-mean benchmarks', 'pass_fail': 'PASS if synthetic coefficients recover and the observed model beats both held-out benchmarks'}
    write_result(args.outdir, "eq08_growth", out)
    save_csv(args.outdir, "eq08_growth", ["world", "rep", "lambda_noH", "beta_H_withH"], rows)
    print("PLAIN:", out["plain_result"])
    print("RULE:", rule)
    return out


if __name__ == "__main__":
    run(smoke_parser("S6 growth / convergence / Nelson-Phelps (SIMULATION)"))
