#!/usr/bin/env python3
"""S8 - Inequality, Theil decomposition, intergenerational mobility (inventory 123-137).
PREREG: PRE_REGISTRATION.md S8. SIMULATION ONLY; no causal claim."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eq_common import ols, rng, write_result, save_csv, smoke_parser

REC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x); c = np.cumsum(x)
    return float((2 * np.sum(np.arange(1, n + 1) * x) / (n * c[-1])) - (n + 1) / n)


def theil(y):
    y = np.asarray(y, float); m = y.mean()
    return float(np.mean((y / m) * np.log(y / m))) if m > 0 else 0.0


def theil_decomp(y, group):
    y = np.asarray(y, float); group = np.asarray(group)
    mu = y.mean(); out = {"within": 0.0, "between": 0.0}
    for g in np.unique(group):
        m = group == g
        pg = m.mean(); mug = y[m].mean()
        out["within"] += pg * (mug / mu) * theil(y[m])
        out["between"] += pg * (mug / mu) * np.log(mug / mu)
    return out


def gen(rng, n, persistence):
    pe = rng.normal(size=n)                       # parent education z
    py = 1.0 * pe + rng.normal(size=n)            # parent income (log)
    child_edu = 8.0 + (1.0 if persistence else 0.0) * pe + rng.normal(size=n)
    child_y = 2.0 + 0.10 * child_edu + (0.4 if persistence else 0.0) * py + rng.normal(size=n)
    return pe, py, child_edu, child_y


def dashboard_real():
    """Descriptive dashboard check on the committed long-run panel (OBSERVED/RECONSTRUCTED). No causal claim."""
    import csv
    path = os.path.join(REC, "inputs", "long_run_panel.csv")
    if not os.path.exists(path):
        return None
    rows = list(csv.DictReader(open(path)))
    data = []
    for r in rows:
        try:
            yr = int(float(r["year"]))
        except (TypeError, ValueError):
            continue
        if yr < 1950 or yr > 2020 or yr % 5 != 0:
            continue
        try:
            d = {"iso3": r["iso3"], "year": yr, "s": float(r["mean_years_schooling"]),
                 "g": float(r["gdp_pc_maddison_1990int"]), "u": float(r["urban_share_pct"]),
                 "ef": float(r["effective_fertility"]), "tfr": float(r["tfr_observed_1950plus"])}
        except (TypeError, ValueError):
            continue
        data.append(d)
    def fe(outcome, placebo=False):
        use = [d for d in data if np.isfinite(d[outcome])]
        iso = sorted({d["iso3"] for d in use}); yrs = sorted({d["year"] for d in use})
        X = [np.ones(len(use)), [d["s"] for d in use], [np.log(max(d["g"], 1e-9)) for d in use],
             [d["u"] for d in use]]
        for v in iso[1:]:
            X.append([1.0 if d["iso3"] == v else 0.0 for d in use])
        for v in yrs[1:]:
            X.append([1.0 if d["year"] == v else 0.0 for d in use])
        y = np.array([d[outcome] for d in use])
        cl = np.array([iso.index(d["iso3"]) for d in use])
        f = ols(y, np.column_stack(X), cluster=cl)
        return {"n": int(len(use)), "countries": len(iso),
                "schooling_coef": round(f["b"][1], 4), "schooling_se": round(f["se"][1], 4)}
    return {"data_tier": "OBSERVED/RECONSTRUCTED descriptive (committed long_run_panel.csv @ 9a4f586)",
            "effective_fertility": fe("ef"), "tfr_observed": fe("tfr"),
            "note": "country+year FE associations; effective fertility is NOT TFR; no causal claim"}


def run(args):
    reps = 10 if args.smoke else 40
    n = 5000 if args.smoke else 50000
    out = {"script": "eq07_inequality_dashboard", "prereg": "S7", "data_tier": "SYNTHETIC",
           "label": "SIMULATION - stipulated two-generation DGP; no causal claim",
           "n": n, "reps": reps}
    rows, summary = [], {}
    for world, persistence in [("null_no_persistence", False), ("persistent", True)]:
        els, ginis, theils, rankr, diag = [], [], [], [], []
        for r in range(reps):
            pe, py, ce, cy = gen(rng(args.seed + (1 if persistence else 2) * 1000 + r), n, persistence)
            ige = ols(cy, np.column_stack([np.ones(n), py]))["b"][1]
            els.append(ige)
            ginis.append(gini(cy)); theils.append(theil(cy))
            rk = ols(np.argsort(np.argsort(cy)) / n,
                     np.column_stack([np.ones(n), np.argsort(np.argsort(py)) / n]))["b"][1]
            rankr.append(rk)
            q = np.argsort(np.argsort(py)) // (n // 5)
            cq = np.argsort(np.argsort(cy)) // (n // 5)
            M = np.zeros((5, 5))
            for i in range(5):
                m = q == i
                for j in range(5):
                    M[i, j] = np.mean(cq[m] == j)
            diag.append(float(np.trace(M) / 5))
            td = theil_decomp(cy, np.where(pe <= np.quantile(pe, 1 / 3), 0,
                                          np.where(pe <= np.quantile(pe, 2 / 3), 1, 2)))
            rows.append([world, r, round(ige, 4), round(ginis[-1], 4), round(theils[-1], 4),
                         round(td["within"], 4), round(td["between"], 4), round(rk, 4), round(diag[-1], 4)])
        # Oaxaca: high vs low parent-education tercile child income, explained by child education
        pe, py, ce, cy = gen(rng(args.seed + 999), n, persistence)
        hi = pe > np.quantile(pe, 2 / 3); lo = pe <= np.quantile(pe, 1 / 3)
        bce = ols(cy, np.column_stack([np.ones(n), ce]))["b"][1]
        gap = cy[hi].mean() - cy[lo].mean()
        explained = (ce[hi].mean() - ce[lo].mean()) * bce
        summary[world] = {"mean_intergen_elasticity": round(float(np.mean(els)), 4),
                          "elasticity_ci90": [round(float(np.percentile(els, 5)), 4),
                                              round(float(np.percentile(els, 95)), 4)],
                          "mean_gini_child_income": round(float(np.mean(ginis)), 4),
                          "mean_theil_within": round(float(np.mean([row[5] for row in rows if row[0] == world])), 4),
                          "mean_theil_between": round(float(np.mean([row[6] for row in rows if row[0] == world])), 4),
                          "mean_rank_rank": round(float(np.mean(rankr)), 4),
                          "mean_transition_diagonal": round(float(np.mean(diag)), 4),
                          "oaxaca_gap": round(float(gap), 4),
                          "oaxaca_explained_by_child_edu": round(float(explained), 4),
                          "oaxaca_unexplained": round(float(gap - explained), 4)}
    null_s, per_s = summary["null_no_persistence"], summary["persistent"]
    rule = {"null_elasticity_ci_includes_0": null_s["elasticity_ci90"][0] <= 0 <= null_s["elasticity_ci90"][1],
            "persistent_elasticity_positive": per_s["mean_intergen_elasticity"] > 0.1,
            "theil_between_positive": per_s["mean_theil_between"] > 0}
    rule["PASS"] = all(rule.values())
    mv = {"specs": ["intergenerational_elasticity", "rank_rank_slope"],
          "estimates": {"intergenerational_elasticity": per_s["mean_intergen_elasticity"],
                        "rank_rank_slope": per_s["mean_rank_rank"]},
          "null_world": {"intergenerational_elasticity": null_s["mean_intergen_elasticity"],
                         "rank_rank_slope": null_s["mean_rank_rank"]},
          "other_summaries": {"gini": per_s["mean_gini_child_income"],
                              "theil_within": per_s["mean_theil_within"],
                              "theil_between": per_s["mean_theil_between"],
                              "oaxaca_explained": per_s["oaxaca_explained_by_child_edu"],
                              "oaxaca_unexplained": per_s["oaxaca_unexplained"]}}
    mv["range"] = [min(mv["estimates"].values()), max(mv["estimates"].values())]
    mv["spec_robust"] = all(v > 0 for v in mv["estimates"].values())
    dash = dashboard_real()
    if dash:
        mv["dashboard_real"] = {"fe_schooling_efr": dash["effective_fertility"]["schooling_coef"],
                                "fe_schooling_tfr": dash["tfr_observed"]["schooling_coef"]}
    out.update({"summary": summary, "multiverse": mv, "dashboard_real": dash, "decision_rule": rule,
                "system_map": {"nodes": ["inequality", "dashboard"], "piece": 4, "chain": "family affordability -> learning -> gate -> credential->jobs"},
           "masseng_boundary": {"used": "standalone synthetic demonstration (NOT MASSENG v5 output)", "mechanism_in_masseng_v5": False, "note": "standalone synthetic demonstration; not a MASSENG v5 output"},
                "plain_result": ("In the null world the intergenerational elasticity is indistinguishable from zero "
                                 "(90%% CI %.2f to %.2f); in the persistent world it is %.2f and the Theil "
                                 "decomposition puts %.2f of inequality between parent-education groups. The "
                                 "elasticity, the Gini and the transition matrix are different summaries of the "
                                 "same synthetic process, not interchangeable evidence." %
                                 (null_s["elasticity_ci90"][0], null_s["elasticity_ci90"][1],
                                  per_s["mean_intergen_elasticity"], per_s["mean_theil_between"]))})
    write_result(args.outdir, "eq07_inequality_dashboard", out)
    save_csv(args.outdir, "eq07_inequality_dashboard",
             ["world", "rep", "ige", "gini", "theil", "theil_within", "theil_between", "rank_rank", "diag"], rows)
    print("PLAIN:", out["plain_result"])
    print("RULE:", rule)
    return out


if __name__ == "__main__":
    run(smoke_parser("S8 inequality / decomposition / mobility (SIMULATION)"))
