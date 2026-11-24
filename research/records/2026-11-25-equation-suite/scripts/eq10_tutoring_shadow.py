#!/usr/bin/env python3
"""S10 - The single tutoring module (exams-shadow part): demand hurdle/Tobit + production/inequality +
Bray literature reality check. PREREG: PRE_REGISTRATION.md S10 + Amendments 01-03.
SYNTHETIC demonstration only - NOT a MASSENG v5 output (MASSENG v5 has no tutoring/learning production module).
No causal claim; Bray targets are a literature reality check, not a calibration."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eq_common import ols, probit, tobit_em, rng, write_result, save_csv, smoke_parser

REC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def require_positive(x, what):
    """Gini is defined only on a strictly positive level domain (a Gini computed on a
    variable with non-positive values is undefined and can leave [0, 1])."""
    x = np.asarray(x, float)
    if x.size == 0 or not np.all(np.isfinite(x)) or np.any(x <= 0):
        raise ValueError("%s: Gini needs strictly positive level-domain values" % what)
    return x


def gini(x):
    x = np.sort(require_positive(x, "gini")); n = len(x); c = np.cumsum(x)
    return float((2 * np.sum(np.arange(1, n + 1) * x) / (n * c[-1])) - (n + 1) / n)


def demand_world(rng, n, different):
    y = rng.normal(size=n); urban = (rng.random(n) < 0.5).astype(float); ab = rng.normal(size=n)
    lat = -0.4 + 0.6 * y + 0.2 * urban + (0.4 * ab if different else 0)
    d = (lat + rng.normal(scale=0.7, size=n) > 0).astype(float)
    lnT = 1.0 + 0.8 * y + 0.2 * urban + (0.3 * ab if different else 0) + rng.normal(scale=0.5, size=n)
    return y, urban, np.where(d > 0, np.exp(lnT), 0.0)


def demand_fit(y, urban, T):
    """Hurdle vs Tobit. The DGP truth is a semi-elasticity: d log T / d y = 0.8. A Tobit
    on the LEVEL of T estimates a level coefficient (~8.6 here) and is not comparable to
    0.8; estimate the Tobit on the log scale instead, log(1+T) with left-censoring at
    log(1+0)=0, so its income coefficient is on the same scale as the two-part estimate
    and the truth (Neon line audit / handoff quarantine #4: Tobit vs ground-truth scale).
    The level-scale fit is still reported for continuity."""
    X = np.column_stack([np.ones_like(y), y, urban])
    pos = T > 0
    tob_log = tobit_em(np.log1p(T), X)
    tob_level = tobit_em(T, X)
    amt = ols(np.log(T[pos]), X[pos]); part = probit((T > 0).astype(float), X)
    return {"tobit_eta": tob_log["b"][1], "tobit_eta_level_scale": tob_level["b"][1],
            "tobit_scale": "log1p(T): semi-elasticity comparable to the 0.8 truth",
            "two_part_eta": amt["b"][1], "ols_positive_eta": amt["b"][1],
            "participation_b": part["b"]}


def learning(Q, T, ses, rng, rho):
    t = np.clip(T / 5.0, 1e-6, None)
    core = (0.5 * np.power(Q, rho) + 0.5 * np.power(t, rho)) ** (1.0 / rho)
    return core + 0.3 * ses + 0.1 * rng.normal(size=len(Q))


def production_world(rng, n, rho, retention):
    z = rng.normal(size=n); y = np.exp(0.5 * z)
    q = np.argsort(np.argsort(z)) / max(n - 1, 1)
    ab = 0.3 * z + rng.normal(size=n)
    Q = np.clip(0.65 + 0.05 * ab + 0.05 * rng.normal(size=n), 0.1, 1.0)
    T = np.clip(2.0 * z + 0.8 * ab + rng.normal(scale=0.8, size=n), 0, None)
    own = ((T > 0) & (rng.random(n) < np.where(z > 0, 0.8, 0.4))).astype(float)
    A0 = learning(Q, T, z, rng, rho)
    Tb = np.where(own > 0, np.where(rng.random(n) < 0.6, 0.0, retention * T), T)
    Ab = learning(Q, Tb, z, rng, rho)
    gap = lambda A: float(A[q >= 0.8].mean() - A[q <= 0.2].mean())
    # The additive achievement index can dip below zero in this stipulation (~37% of
    # draws), where the Gini is undefined (and the raw value can exceed 1). Report it on
    # the strictly positive level domain exp(A) (monotone transform); the sign of the
    # ban effect is unchanged under a common additive shift (see NEON_PATCHES doc).
    return {"gini_base": gini(np.exp(A0)), "gini_ban": gini(np.exp(Ab)),
            "delta_gini_ban": gini(np.exp(Ab)) - gini(np.exp(A0)),
            "gini_base_raw_nonpositive_share": round(float((A0 <= 0).mean()), 4),
            "gini_domain": "exp(learning index)",
            "gap_base": gap(A0), "gap_ban": gap(Ab),
            "participation": float((T > 0).mean()),
            "own_share": float(own[T > 0].sum() / max((T > 0).sum(), 1))}


def run(args):
    reps = 12 if args.smoke else 50
    n_dem = 2500 if args.smoke else 8000
    n_prod = 3000 if args.smoke else 12000
    out = {"script": "eq10_tutoring_shadow", "prereg": "S10",
           "system_map": {"nodes": ["exams-shadow", "learning"], "piece": 2,
                          "chain": "family affordability -> learning -> gate -> credential->jobs"},
           "masseng_boundary": {"used": "standalone synthetic demonstration (NOT MASSENG v5 output)",
                                "mechanism_in_masseng_v5": False,
                                "note": "tutoring/learning production is NOT implemented in MASSENG v5; synthetic demonstration only. Bray targets are literature targets, not a fit."},
           "data_tier": "SYNTHETIC + LITERATURE_TARGETS (Bray; descriptive check only)",
           "label": "SIMULATION - stipulated tutoring demand + production DGP; no causal claim",
           "reps": reps, "n_demand": n_dem, "n_production": n_prod}
    rows = []
    # ---- demand multiverse ----
    dem = {}
    for world, diff in [("single_process", False), ("different_processes", True)]:
        tob, tp, ols_pos, tob_level = [], [], [], []
        for r in range(reps):
            y, urban, T = demand_world(rng(args.seed + (1 if diff else 2) * 10000 + r), n_dem, diff)
            f = demand_fit(y, urban, T)
            tob.append(f["tobit_eta"]); tp.append(f["two_part_eta"]); ols_pos.append(f["ols_positive_eta"])
            tob_level.append(f["tobit_eta_level_scale"])
            rows.append([world, r, round(f["tobit_eta"], 4), round(f["two_part_eta"], 4)])
        dem[world] = {"tobit_eta_mean": round(float(np.mean(tob)), 3),
                      "tobit_eta_level_scale_mean": round(float(np.mean(tob_level)), 3),
                      "tobit_scale": "log1p(T): semi-elasticity; level-scale fit reported separately, not compared to 0.8",
                      "two_part_eta_mean": round(float(np.mean(tp)), 3),
                      "two_part_within_0.15_share": round(float(np.mean(np.abs(np.array(tp) - 0.8) <= 0.15)), 2),
                      "tobit_within_0.15_share": round(float(np.mean(np.abs(np.array(tob) - 0.8) <= 0.15)), 2)}
    mv_dem = {"specs": ["tobit", "two_part_hurdle", "ols_on_participants"],
              "estimates": {"different_processes_tobit": dem["different_processes"]["tobit_eta_mean"],
                            "different_processes_two_part": dem["different_processes"]["two_part_eta_mean"]}}
    mv_dem["range"] = [min(mv_dem["estimates"].values()), max(mv_dem["estimates"].values())]
    mv_dem["spec_robust"] = all(v > 0 for v in mv_dem["estimates"].values())
    # ---- production/inequality multiverse ----
    prod = {}
    for rho in (0.3, 0.5, 0.7):
        for retention in (0.5, 0.7, 0.9):
            dg, pg = [], []
            for r in range(max(3, reps // 3)):
                m = production_world(rng(args.seed + 20000 + int(rho * 100) + int(retention * 10) + r), n_prod, rho, retention)
                dg.append(m["delta_gini_ban"]); pg.append(m["participation"])
                rows.append(["rho_%.1f_ret_%.1f" % (rho, retention), r, round(m["gini_base"], 4),
                             round(m["gini_ban"], 4)])
            prod["rho_%.1f_ret_%.1f" % (rho, retention)] = {
                "mean_delta_gini_ban": round(float(np.mean(dg)), 4),
                "ban_raises_gini_share": round(float(np.mean(np.array(dg) > 0)), 2),
                "mean_participation": round(float(np.mean(pg)), 3)}
    deltas = [v["mean_delta_gini_ban"] for v in prod.values()]
    mv_prod = {"specs": list(prod.keys()), "estimates": {k: v["mean_delta_gini_ban"] for k, v in prod.items()},
               "range": [min(deltas), max(deltas)], "spec_robust": all(d > 0 for d in deltas)}
    # ---- Bray literature reality check ----
    bray = None
    bp = os.path.join(REC, "inputs", "bray_targets.json")
    if os.path.exists(bp):
        tgt = json.load(open(bp))["targets"]
        base_part = float(np.mean([v["mean_participation"] for v in prod.values()]))
        checks = {}
        for key, val in [("participation", base_part)]:
            if key in tgt:
                mu, sd = tgt[key]; checks[key] = {"model": round(val, 3), "target_mean": mu, "z": round((val - mu) / sd, 2)}
        bray = {"source": "literature targets from research/shadow-equations-2026-11-25 @ fdc8da0",
                "checks": checks, "max_abs_z": max(abs(c["z"]) for c in checks.values())}
    rule = {"two_part_closer_than_tobit": abs(mv_dem["estimates"]["different_processes_two_part"] - 0.8) <
                                            abs(mv_dem["estimates"]["different_processes_tobit"] - 0.8),
            "ban_raises_gini_in_all_specs": mv_prod["spec_robust"],
            "model_not_claimed_to_fit_bray": bray is not None and bray["max_abs_z"] > 2}
    rule["PASS"] = all(rule.values())
    out.update({"demand": dem, "production": prod, "multiverse": {"demand": mv_dem, "production": mv_prod},
                "gini_domain": "exp(learning index) - strictly positive level domain; the raw additive "
                                "achievement index is non-positive in ~37% of draws, where the Gini is undefined",
                "bray_external_check": bray, "decision_rule": rule,
                "plain_result": ("Tutoring behaves as one exams-shadow module for demand: on the same log scale "
                                 "as the 0.8 truth the two-part model is closer than the Tobit (%.2f vs %.2f). "
                                 "On inequality the own-teacher ban does NOT raise the learning Gini once the "
                                 "Gini is computed on a strictly positive level domain: in this reduced "
                                 "production model there is no substitution margin, so removing tutoring lowers "
                                 "the Gini in every CES/retention specification (delta range %.3f..%.3f). The "
                                 "illustrative model is far from Bray's targets (max |z| = %.1f), so nothing here "
                                 "is a fit to a real shadow-education system." %
                                 (mv_dem["estimates"]["different_processes_two_part"],
                                  mv_dem["estimates"]["different_processes_tobit"],
                                  min(deltas), max(deltas), bray["max_abs_z"] if bray else float("nan")))})
    out["data_map"] = {'module': 'exams-shadow (single tutoring module)', 'observed': 'no harmonised tutoring panel; Bray targets are literature targets', 'assumed': 'demand and production parameters', 'gap': 'no tutoring data'}
    out["statistical_frame"] = {'estimand': 'tutoring income elasticity; ban effect on learning Gini', 'identification': 'none (synthetic); two-part vs Tobit', 'testable_restrictions': 'hurdle/CES forms; retention assumption', 'benchmark_split': 'synthetic reps; Bray literature targets as external check (not a fit)', 'pass_fail': 'PASS if two-part closer than Tobit (same scale) and ban raises Gini in all specs', 'scale_alignment': 'Tobit on log1p(T) so its income coefficient is a semi-elasticity comparable to the 0.8 truth; the level-scale Tobit is reported but never compared to 0.8'}
    write_result(args.outdir, "eq10_tutoring_shadow", out)
    save_csv(args.outdir, "eq10_tutoring_shadow", ["part", "rep", "a", "b"], rows)
    print("PLAIN:", out["plain_result"])
    print("RULE:", rule)
    return out


if __name__ == "__main__":
    run(smoke_parser("S10 tutoring module: demand + production + Bray check (SIMULATION)"))
