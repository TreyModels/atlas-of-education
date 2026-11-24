#!/usr/bin/env python3
"""Independent audit of Codex's synthetic MASSENG timing/staging experiment.

Reads the committed branch `research/codex-masseng-staging-2026-11-24` @ bac3a7c via
`git show` (read-only; no re-run, no server compute) and recomputes:

  * design/config claims (160 runs, N=400, T=70, 10 seeds, elapsed ~16.5 s) from full.json;
  * intervention semantics per row (events, years, values) against DESIGN.md and run_staging.py;
  * the stored summary means/SDs from the raw rows (reproduction check);
  * the two DESIGN contrasts (school_first - jobs_first; simultaneous - none) with
    seed-level paired differences, seed bootstrap CIs, sign stability and leave-one-out checks;
  * the gate comparison (quota - bar) and the education-to-jobs feedback comparison
    (job_elasticity 1 - 0) that DESIGN asks for but the stored summary does not compute;
  * seed sensitivity (between-seed spread, how often a conclusion is sign-unstable);
  * mechanical cumulative-exposure arithmetic for the education share and vacancy rate
    (arms are not exposure-matched by construction), plus the engine's one-year fiscal lag.

Writes machine-readable tables under audit_tables/. No causal claims; simulation only.
"""
import itertools
import json
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audit_tables")
BRANCH = "origin/research/codex-masseng-staging-2026-11-24"
FULL = "engine/experiments_codex_sequence/results/full.json"
CODE = "engine/experiments_codex_sequence/run_staging.py"
DESIGN = "engine/experiments_codex_sequence/DESIGN.md"

SCALARS = ["completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
           "tut_rate", "mpl_primary", "q_pub", "formal_share_gdp", "edu_gdp",
           "parity_location_lower", "parity_wealth_lower", "parity_location_upper", "parity_wealth_upper"]
SCHEDULES = ["none", "school_first", "jobs_first", "simultaneous"]


def show(path):
    p = subprocess.run(["git", "show", f"{BRANCH}:{path}"], capture_output=True)
    if p.returncode != 0:
        raise FileNotFoundError(f"{BRANCH}:{path}: {p.stderr.decode()[:300]}")
    return p.stdout.decode()


def boot_ci(diffs, rng, B=4000):
    diffs = np.asarray(diffs, float)
    bs = np.mean(rng.choice(diffs, size=(B, len(diffs)), replace=True), axis=1)
    return [float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))]


def contrast_stats(diffs, rng, label):
    d = np.asarray(diffs, float)
    n = len(d)
    means = d.mean()
    sd = d.std(ddof=1) if n > 1 else 0.0
    loo = [float(np.delete(d, i).mean()) for i in range(n)]
    out = {
        "label": label, "n_seeds": n, "mean": float(means), "sd": float(sd),
        "se": float(sd / np.sqrt(n)) if n else None,
        "min": float(d.min()), "max": float(d.max()),
        "ci95_seed_bootstrap": boot_ci(d, rng),
        "n_positive": int((d > 0).sum()), "n_negative": int((d < 0).sum()), "n_zero": int((d == 0).sum()),
        "sign_stable_across_seeds": bool((d > 0).all() or (d < 0).all()),
        "sign_stable_leave_one_out": bool(len(set(np.sign(loo))) == 1) if n > 1 else None,
        "loo_mean_min": float(min(loo)) if loo else None, "loo_mean_max": float(max(loo)) if loo else None,
        "max_abs_loo_shift": float(max(abs(x - means) for x in loo)) if loo else None,
        "ci95_includes_zero": bool(out_lo <= 0 <= out_hi) if False else None,
    }
    lo, hi = out["ci95_seed_bootstrap"]
    out["ci95_includes_zero"] = bool(lo <= 0 <= hi)
    out["seed_sensitive_conclusion"] = bool(not out["sign_stable_across_seeds"] or out["ci95_includes_zero"])
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    design_txt = show(DESIGN)
    code_txt = show(CODE)
    d = json.loads(show(FULL))
    rows, config, summary = d["rows"], d["config"], d["summary"]
    rng_master = np.random.default_rng(20261125)

    # ---------------- dataset-level checks ----------------
    by_cond = {}
    for r in rows:
        by_cond.setdefault((r["feedback"], r["gates"]), []).append(r)
    combos = {}
    for r in rows:
        combos.setdefault((r["schedule"], r["feedback"], r["gates"]), []).append(r["seed"])
    seeds_ok = all(sorted(v) == list(range(10)) for v in combos.values())
    per_condition = {}
    for (fb, g) in by_cond.keys():
        sch = {}
        for r in by_cond[(fb, g)]:
            sch[r["schedule"]] = []
        per_condition[f"feedback_{fb:g}_gates_{g}"] = {
            "rows": len(by_cond[(fb, g)]),
            "schedule_counts": {s: sum(1 for r in by_cond[(fb, g)] if r["schedule"] == s) for s in SCHEDULES},
            "seeds_per_cell": {s: sorted(r["seed"] for r in by_cond[(fb, g)] if r["schedule"] == s)
                               for s in SCHEDULES},
        }

    expected_events = {
        "none": [],
        "school_first": [{"year": 15, "set": {"edu_share": 0.30}, "label": "education_share"},
                         {"year": 30, "set": {"vac0": 0.16}, "label": "formal_vacancies"}],
        "jobs_first": [{"year": 15, "set": {"vac0": 0.16}, "label": "formal_vacancies"},
                       {"year": 30, "set": {"edu_share": 0.30}, "label": "education_share"}],
        "simultaneous": [{"year": 15, "set": {"edu_share": 0.30}, "label": "education_share"},
                         {"year": 15, "set": {"vac0": 0.16}, "label": "formal_vacancies"}],
    }
    event_ok = 0
    event_bad = []
    for r in rows:
        got = r.get("events", [])
        exp = expected_events[r["schedule"]]
        norm = [{"year": e[0], "label": e[1], "set": e[2]} if isinstance(e, (list, tuple)) else e for e in got]
        if norm == exp:
            event_ok += 1
        else:
            event_bad.append({"schedule": r["schedule"], "seed": r["seed"], "got": norm, "expected": exp})
    # annual series integrity
    annual_lens, annual_none, annual_missing = set(), 0, 0
    annual_keys = set()
    for r in rows:
        a = r.get("annual", {})
        annual_keys |= set(a.keys())
        for k, v in a.items():
            annual_lens.add(len(v))
            annual_none += sum(1 for x in v if x is None)
    metrics_none = sum(1 for r in rows for k in SCALARS if r["metrics"].get(k) is None)
    design_checks = {
        "claimed_vs_actual": {
            "runs_claimed_160": {"claimed": 160, "actual": len(rows), "ok": len(rows) == 160},
            "cohort_N_claimed_400": {"claimed": 400, "actual": config["cohort_N"],
                                     "ok": config["cohort_N"] == 400},
            "years_claimed_70": {"claimed": 70, "actual": config["years"], "ok": config["years"] == 70},
            "seeds_claimed_10": {"claimed": 10, "actual": len(config["seeds"]),
                                 "ok": len(config["seeds"]) == 10},
            "elapsed_claimed_16.5s": {"claimed": 16.5, "actual": d["elapsed_s"],
                                      "ok": abs(d["elapsed_s"] - 16.5) <= 0.05},
        },
        "grid": {"schedules": config["schedules"], "feedback": config["feedback"],
                 "gates": config["gate"], "cohort_N": config["cohort_N"],
                 "years": config["years"], "seeds": config["seeds"], "runs": config["runs"]},
        "per_condition": per_condition,
        "every_cell_has_10_seeds_0_to_9": bool(seeds_ok),
        "events_per_row_match_design_and_code": {"n_ok": event_ok, "n_bad": len(event_bad),
                                                 "examples_bad": event_bad[:3]},
        "annual_series": {"keys": sorted(annual_keys), "lengths": sorted(annual_lens),
                          "n_none_entries": annual_none},
        "metrics_none_entries": metrics_none,
        "recorded_but_missing_provenance": [
            "worker count is not recorded in full.json (DESIGN claims 16.5 s but not the machine/parallelism)",
            "no code/engine/site-packages hashes or versions are recorded in full.json",
            "seed->run mapping is recorded (seed column) but the RNG implementation version is not pinned",
            "no event log beyond per-row `events`; the engine's `event_log` is not exported in full.json",
        ],
        "consistency_with_design_text": {
            "observed_from_design": [
                "uses modular eduengine worlds.formal_loop (not national v5 regression model): DESIGN states this; "
                "code imports `worlds`, builds worlds.make('formal_loop', ...)",
                "T=70, N=400, measure_from=35 (cohorts 35-44 scored): code passes T=70, N=400, measure_from=35; "
                "engine SDG4 uses last_cohort = T-26 = 44",
                "no country enrolment anchors: run_staging.py passes no enrol_targets; engine default {}",
                "gate sets: bar [3.0,5.5,8.0,11.5]; quota [bar 3.0, quota .55 cut0 7.0, quota .45 cut0 10.0, bar 11.5]",
                "intervention values: edu_share 0.18->0.30; vac0 0.08->0.16",
                "fiscal lag: FiscalState computes budget after the labour market and supplies it next year; "
                "QueueLabour vacancies apply in the event year (asymmetric by construction, stated in DESIGN)",
                "bootstrap: stored summary bootstraps seed-level differences (rng seed 7321, B=2000); "
                "matched seeds are not exact common random numbers after paths diverge (stated in DESIGN)",
            ],
            "not_implemented_per_design": [
                "rural/urban migration: no migration flow in engine or experiment (rural is a household attribute + cost)",
                "realistic data fit / historical event dates / observed places: not attempted",
                "tutoring cost/distribution and employer credential requirements as estimated quantities: not estimated",
                "country enrolment anchors: deliberately off",
            ],
        },
    }

    # ---------------- reproduce stored summary ----------------
    repro = {}
    max_abs = 0.0
    n_mismatch = 0
    for cond, block in summary.items():
        fb = float(cond.split("_")[1])
        g = cond.split("_")[3]
        for sched in SCHEDULES:
            vals = {m: np.array([r["metrics"][m] for r in by_cond[(fb, g)] if r["schedule"] == sched
                                 and r["metrics"][m] is not None], float) for m in SCALARS}
            for m in SCALARS:
                st = block["groups"][sched][m]
                mean = float(vals[m].mean()) if len(vals[m]) else None
                sd = float(vals[m].std(ddof=1)) if len(vals[m]) > 1 else None
                dm = 0.0 if (mean is None and st["mean"] is None) else (
                    abs(mean - st["mean"]) if mean is not None and st["mean"] is not None else 9e9)
                ds = 0.0 if (sd is None and st["sd"] is None) else (
                    abs(sd - st["sd"]) if sd is not None and st["sd"] is not None else 9e9)
                max_abs = max(max_abs, dm, ds)
                n_mismatch += int(dm > 1e-9 or ds > 1e-9)
    repro = {"max_abs_difference_stored_vs_recomputed": max_abs,
             "n_group_metric_mismatches": n_mismatch,
             "n_group_metric_cells_checked": len(summary) * len(SCHEDULES) * len(SCALARS)}

    # ---------------- recompute DESIGN contrasts + gate/feedback contrasts ----------------
    def seed_diffs(cond_key, a, b, m):
        left = {r["seed"]: r["metrics"][m] for r in by_cond[cond_key] if r["schedule"] == a}
        right = {r["seed"]: r["metrics"][m] for r in by_cond[cond_key] if r["schedule"] == b}
        return [left[s] - right[s] for s in sorted(left.keys() & right.keys())
                if left[s] is not None and right[s] is not None], left, right

    design_contrasts = {}
    stored_vs_recomputed = {}
    for fb, g in sorted(by_cond.keys()):
        cond_key = (fb, g)
        cond_name = f"feedback_{fb:g}_gates_{g}"
        design_contrasts[cond_name] = {}
        stored_vs_recomputed[cond_name] = {}
        for a, b in (("school_first", "jobs_first"), ("simultaneous", "none")):
            design_contrasts[cond_name][f"{a}_minus_{b}"] = {}
            stored = summary[cond_name]["contrasts"].get(f"{a}_minus_{b}")
            for m in SCALARS:
                diffs, left, right = seed_diffs(cond_key, a, b, m)
                if len(diffs) < 2:
                    design_contrasts[cond_name][f"{a}_minus_{b}"][m] = {"n_seeds": len(diffs), "status": "insufficient"}
                    continue
                st = contrast_stats(diffs, rng_master, f"{cond_name}:{a}-{b}:{m}")
                # standardised effect vs pooled across-arm SD of the metric
                pooled_sd = float(np.sqrt((left.__len__() and np.var([v for v in left.values() if v is not None], ddof=1)) * 0 +
                                          0) ) if False else None
                allv = [v for v in list(left.values()) + list(right.values()) if v is not None]
                pooled_sd = float(np.std(allv, ddof=1)) if len(allv) > 1 else None
                st["standardised_effect_pooled_sd"] = (float(st["mean"] / pooled_sd) if pooled_sd else None)
                st["arm_means"] = {a: float(np.mean([v for v in left.values() if v is not None])),
                                   b: float(np.mean([v for v in right.values() if v is not None]))}
                st["per_seed_differences"] = [float(x) for x in diffs]
                design_contrasts[cond_name][f"{a}_minus_{b}"][m] = st
            # stored-vs-recomputed for this contrast
            if stored:
                for m in SCALARS:
                    if m in stored and stored[m].get("mean") is not None and m in design_contrasts[cond_name][f"{a}_minus_{b}"]:
                        rec = design_contrasts[cond_name][f"{a}_minus_{b}"][m].get("mean")
                        stored_vs_recomputed[cond_name][f"{a}_minus_{b}|{m}"] = {
                            "stored_mean": stored[m]["mean"], "recomputed_mean": rec,
                            "abs_diff": (abs(stored[m]["mean"] - rec) if rec is not None else None)}

    # gate contrast (quota - bar), paired by (schedule, feedback, seed)
    gate_contrasts = {}
    for fb in (0.0, 1.0):
        for sched in SCHEDULES:
            bar = {(r["seed"]): r["metrics"] for r in by_cond[(fb, "bar")] if r["schedule"] == sched}
            qua = {(r["seed"]): r["metrics"] for r in by_cond[(fb, "quota")] if r["schedule"] == sched}
            gate_contrasts[f"feedback_{fb:g}:{sched}"] = {}
            for m in SCALARS:
                diffs = [qua[s][m] - bar[s][m] for s in sorted(set(bar) & set(qua))
                         if bar[s][m] is not None and qua[s][m] is not None]
                if len(diffs) < 2:
                    gate_contrasts[f"feedback_{fb:g}:{sched}"][m] = {"n_seeds": len(diffs), "status": "insufficient"}
                    continue
                st = contrast_stats(diffs, rng_master, f"quota-bar:fb{fb:g}:{sched}:{m}")
                st["arm_means"] = {"bar": float(np.mean([bar[s][m] for s in bar if bar[s][m] is not None])),
                                   "quota": float(np.mean([qua[s][m] for s in qua if qua[s][m] is not None]))}
                st["per_seed_differences"] = [float(x) for x in diffs]
                gate_contrasts[f"feedback_{fb:g}:{sched}"][m] = st

    # feedback contrast (job_elasticity 1 - 0), paired by (schedule, gates, seed)
    feedback_contrasts = {}
    for g in ("bar", "quota"):
        for sched in SCHEDULES:
            f0 = {r["seed"]: r["metrics"] for r in by_cond[(0.0, g)] if r["schedule"] == sched}
            f1 = {r["seed"]: r["metrics"] for r in by_cond[(1.0, g)] if r["schedule"] == sched}
            feedback_contrasts[f"{g}:{sched}"] = {}
            for m in SCALARS:
                diffs = [f1[s][m] - f0[s][m] for s in sorted(set(f0) & set(f1))
                         if f0[s][m] is not None and f1[s][m] is not None]
                if len(diffs) < 2:
                    feedback_contrasts[f"{g}:{sched}"][m] = {"n_seeds": len(diffs), "status": "insufficient"}
                    continue
                st = contrast_stats(diffs, rng_master, f"feedback1-0:{g}:{sched}:{m}")
                st["arm_means"] = {"feedback0": float(np.mean([f0[s][m] for s in f0 if f0[s][m] is not None])),
                                   "feedback1": float(np.mean([f1[s][m] for s in f1 if f1[s][m] is not None]))}
                st["per_seed_differences"] = [float(x) for x in diffs]
                feedback_contrasts[f"{g}:{sched}"][m] = st

    # ---------------- seed sensitivity ----------------
    seed_sens = {"group_spread": {}, "schedule_ordering_stability": {}}
    key_metrics = ["completion_lower", "completion_upper", "completion_tertiary",
                   "formal_share_gdp", "tut_rate", "parity_wealth_lower", "q_pub"]
    for cond_name, block in summary.items():
        fb = float(cond_name.split("_")[1]); g = cond_name.split("_")[3]
        seed_sens["group_spread"][cond_name] = {}
        for sched in SCHEDULES:
            seed_sens["group_spread"][cond_name][sched] = {}
            for m in key_metrics:
                vals = np.array([r["metrics"][m] for r in by_cond[(fb, g)] if r["schedule"] == sched
                                 and r["metrics"][m] is not None], float)
                seed_sens["group_spread"][cond_name][sched][m] = {
                    "n": int(len(vals)), "mean": float(vals.mean()),
                    "sd": float(vals.std(ddof=1)) if len(vals) > 1 else None,
                    "min": float(vals.min()), "max": float(vals.max()),
                    "range": float(vals.max() - vals.min()),
                    "cv": float(vals.std(ddof=1) / abs(vals.mean())) if len(vals) > 1 and vals.mean() != 0 else None,
                }
        # ordering of schedules by each key metric, per seed
        ords = []
        for seed in range(10):
            per_seed = {}
            for sched in SCHEDULES:
                rr = [r for r in by_cond[(fb, g)] if r["schedule"] == sched and r["seed"] == seed]
                per_seed[sched] = rr[0]["metrics"] if rr else None
            for m in key_metrics:
                ranked = tuple(s for s in sorted(SCHEDULES, key=lambda s: -per_seed[s][m])
                               if per_seed[s][m] is not None)
                ords.append((m, ranked))
        counts = {}
        for m in key_metrics:
            ordered = [r for mm, r in ords if mm == m]
            counts[m] = {"n_distinct_orderings_across_10_seeds": len(set(ordered)),
                         "most_common": list(max(set(ordered), key=ordered.count))}
        seed_sens["schedule_ordering_stability"][cond_name] = counts

    # ---------------- mechanical exposure arithmetic ----------------
    def exposure(schedule, event_param, base, treat):
        edu, jobs = config["schedules"][schedule]
        year = edu if event_param == "edu_share" else jobs
        raw = 0.0
        for t in range(config["years"]):
            v = treat if (year is not None and t >= year) else base
            raw += v
        # fiscal lag: education share event affects the *budget* one year later
        lag = 0.0
        for t in range(config["years"]):
            eff = (year is not None and t >= year + 1)
            lag += treat if eff else base
        return {"sum_raw": raw, "sum_with_fiscal_lag_one_year": lag}

    mech = {"education_share_0.18_to_0.30": {s: exposure(s, "edu_share", 0.18, 0.30) for s in SCHEDULES},
            "vacancy_rate_0.08_to_0.16": {s: exposure(s, "vac0", 0.08, 0.16) for s in SCHEDULES},
            "note": ("Both interventions are absent in `none` and both are eventually on in all three intervention "
                     "arms, so the arms differ in CUMULATIVE EXPOSURE as well as order: school_first has more "
                     "education-share-years and fewer vacancy-years than jobs_first by construction, and "
                     "simultaneous has the most of both. The engine also lags the fiscal channel by one year "
                     "(budget from this year's revenue is spent next year) while vacancies act in the event year, "
                     "so 'simultaneous' is not simultaneous in effect."),
            "arm_exposure_differences_vs_none": {
                "school_first": {
                    "extra_edu_share_years": exposure("school_first", "edu_share", 0.18, 0.30)["sum_raw"]
                    - exposure("none", "edu_share", 0.18, 0.30)["sum_raw"],
                    "extra_vacancy_years": exposure("school_first", "vac0", 0.08, 0.16)["sum_raw"]
                    - exposure("none", "vac0", 0.08, 0.16)["sum_raw"]},
                "jobs_first": {
                    "extra_edu_share_years": exposure("jobs_first", "edu_share", 0.18, 0.30)["sum_raw"]
                    - exposure("none", "edu_share", 0.18, 0.30)["sum_raw"],
                    "extra_vacancy_years": exposure("jobs_first", "vac0", 0.08, 0.16)["sum_raw"]
                    - exposure("none", "vac0", 0.08, 0.16)["sum_raw"]},
            }}
    # empirical annual series: mean total edu_budget and mean formal_share_gdp around events
    series = {}
    for sched in SCHEDULES:
        arrs = np.array([r["annual"].get("edu_budget") for r in rows if r["schedule"] == sched
                         and r["annual"].get("edu_budget") is not None], float)
        fs = np.array([r["annual"].get("formal_share_gdp") for r in rows if r["schedule"] == sched
                       and r["annual"].get("formal_share_gdp") is not None], float)
        series[sched] = {
            "n_annual_runs": int(arrs.shape[0]),
            "mean_edu_budget_years_0_14": float(np.nanmean(arrs[:, :15])) if arrs.size else None,
            "mean_edu_budget_years_15_29": float(np.nanmean(arrs[:, 15:30])) if arrs.size else None,
            "mean_edu_budget_years_30_69": float(np.nanmean(arrs[:, 30:])) if arrs.size else None,
            "total_edu_budget_sum_mean_seed": float(np.nanmean(arrs.sum(axis=1))) if arrs.size else None,
            "mean_formal_share_gdp_years_0_14": float(np.nanmean(fs[:, :15])) if fs.size else None,
            "mean_formal_share_gdp_years_15_29": float(np.nanmean(fs[:, 15:30])) if fs.size else None,
            "mean_formal_share_gdp_years_30_69": float(np.nanmean(fs[:, 30:])) if fs.size else None,
        }

    out = {
        "label": "STAGING AUDIT — independent recomputation from committed full.json; simulation only",
        "audited_branch": BRANCH,
        "audited_files": {DESIGN: "DESIGN.md", CODE: "run_staging.py", FULL: "results/full.json"},
        "design_checks": design_checks,
        "stored_summary_reproduction": repro,
        "design_contrasts": design_contrasts,
        "stored_vs_recomputed_contrast_means": stored_vs_recomputed,
        "gate_contrasts_quota_minus_bar": gate_contrasts,
        "feedback_contrasts_elasticity1_minus_0": feedback_contrasts,
        "seed_sensitivity": seed_sens,
        "mechanical_exposure": mech,
        "empirical_annual_series": series,
        "causal_language": ("No causal claim: schedules are stipulated changes in a synthetic model; the arms are "
                            "not exposure-matched; time order is not identified; migration is not simulated."),
    }
    with open(os.path.join(OUT, "staging_audit.json"), "w") as f:
        json.dump(out, f, indent=1)

    # console summary
    print(json.dumps({
        "runs": len(rows), "elapsed_s": d["elapsed_s"],
        "stored_summary_max_abs_diff": repro["max_abs_difference_stored_vs_recomputed"],
        "stored_summary_mismatches": repro["n_group_metric_mismatches"],
        "events_ok": event_ok, "events_bad": len(event_bad),
        "design_contrasts": {
            k: {c: {m: {"mean": v[m]["mean"], "ci95": v[m]["ci95_seed_bootstrap"],
                        "sign_stable": v[m]["sign_stable_across_seeds"],
                        "ci_includes_0": v[m]["ci95_includes_zero"]}
                    for m in ("completion_lower", "formal_share_gdp", "tut_rate")}
                for c, v in block.items()}
            for k, block in design_contrasts.items()},
        "gate_contrasts": {k: {m: {"mean": v[m]["mean"], "sign_stable": v[m]["sign_stable_across_seeds"]}
                               for m in ("completion_lower", "tut_rate", "parity_wealth_lower")}
                           for k, v in gate_contrasts.items()},
        "feedback_contrasts": {k: {m: {"mean": v[m]["mean"], "sign_stable": v[m]["sign_stable_across_seeds"]}
                                   for m in ("formal_share_gdp", "completion_lower")}
                               for k, v in feedback_contrasts.items()},
        "exposure": mech["arm_exposure_differences_vs_none"],
    }, indent=1, default=str))


if __name__ == "__main__":
    main()
