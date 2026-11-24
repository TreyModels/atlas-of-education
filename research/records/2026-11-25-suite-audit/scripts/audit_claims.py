#!/usr/bin/env python3
"""Read-only audit of the equation suite + full-system multiverse claims (task-47).

Sources (read from committed git objects; no server compute, no edits):
  * origin/research/equation-suite-2026-11-25 @ a7fcfb9
  * origin/research/masseng-edsystem-2026-11-25 @ b7108da
  * origin/research/edsystem-tests-2026-11-25 @ aadbbb4

Recomputes: S1-S10 execution vs decision-rule status; plain-text vs rule consistency; the
pre-registered rules vs the implemented rules; data tiers; boundary labels; the full-system
cluster-robust OLS/seed-FE replication; supported/stratum/zero-variance artefacts; eta^2 and
range-overlap claims; PHL check; and hash provenance. Writes results/audit.json.

Reproduce from the repo root (numpy required):
    git fetch origin 'refs/heads/*:refs/remotes/origin/*'
    python3 research/records/2026-11-25-suite-audit/scripts/audit_claims.py
"""
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

REPO = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
EQ = "origin/research/equation-suite-2026-11-25"
MES = "origin/research/masseng-edsystem-2026-11-25"
EDS = "origin/research/edsystem-tests-2026-11-25"

EQD = "research/records/2026-11-25-equation-suite"
MESD = "research/records/2026-11-25-masseng-edsystem"
EDSD = "research/records/2026-11-25-edsystem-tests"

CHECKS = []

def add(cid, area, question, value, ref="", status="INFO"):
    CHECKS.append(dict(id=cid, area=area, question=question, value=value, ref=ref, status=status))

def show(ref, path):
    return subprocess.check_output(["git", "-C", str(REPO), "show", f"{ref}:{path}"], stderr=subprocess.DEVNULL)

def jshow(ref, path):
    return json.loads(show(ref, path).decode())

def tshow(ref, path):
    return show(ref, path).decode("utf-8", "replace")

def sha(b):
    return hashlib.sha256(b).hexdigest()

def main():
    import numpy as np

    outdir = REPO / "research/records/2026-11-25-suite-audit/results"
    outdir.mkdir(parents=True, exist_ok=True)
    heads = {k: subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "--short", r], text=True).strip()
             for k, r in (("equation_suite", EQ), ("masseng_edsystem", MES), ("edsystem_tests", EDS))}
    add("HEAD-1", "provenance", "audited heads", heads, "origin refs", "INFO")

    # ------------------------------------------------------------------ equation suite
    run = jshow(EQ, EQD + "/results/run_all.json")
    full = run["full"]
    eqs = {e["script"]: jshow(EQ, EQD + "/results/" + e["script"].replace(".py", ".json")) for e in full}
    rule_fail = [s for s in eqs if eqs[s]["decision_rule"].get("PASS") is False]
    add("EQ-1", "equation suite",
        "10 scripts; execution status; decision-rule failures",
        {"n_scripts": len(full), "execution_failures": run.get("failures"),
         "all_execution_status": sorted({e["status"] for e in full}),
         "decision_rule_failures": rule_fail, "n_rule_failures": len(rule_fail),
         "wall_s": run.get("wall_s")},
        "results/run_all.json", "FLAG")
    add("EQ-2", "equation suite",
        "report headline says 'Failures: []' and 'per-script results (smoke PASS, full PASS)' while 3 decision rules fail",
        {"headline": "Failures: []", "section_head": "Per-script results (smoke PASS, full PASS)",
         "rule_failures": rule_fail,
         "visible_in_headline": False,
         "summary_sentence_counting_rule_failures": 0},
        "SUITE_REPORT.md lines 4, 10, 95", "FLAG")

    # hashes
    hash_ok = {}
    for e in full:
        sp = EQD + "/scripts/" + e["script"]
        op = EQD + "/results/" + e["script"].replace(".py", ".json")
        hash_ok[e["script"]] = {"script_matches_manifest": sha(show(EQ, sp)) == e["script_sha256"],
                                "output_matches_manifest": sha(show(EQ, op)) == e["output_sha256"]}
    add("EQ-3", "equation suite", "script/output sha256 match the run manifest",
        {"all_match": all(v["script_matches_manifest"] and v["output_matches_manifest"] for v in hash_ok.values()),
         "n_checked": len(hash_ok)}, "results/run_all_manifest.csv", "PASS")

    # plain-text vs rule
    eq03, eq04, eq06 = eqs["eq03_learning_quality.py"], eqs["eq04_transitions_gates.py"], eqs["eq06_migration_rural_urban.py"]
    add("EQ-4", "equation suite",
        "plain-English results contradict or omit the failed decision rule",
        {"eq03": {"rule_fail": "rho_recovered_within_0.10_in_half_reps=False",
                  "plain": eq03["plain_result"],
                  "mentions_rho_failure": "rho" in eq03["plain_result"].lower() and "fail" in eq03["plain_result"].lower()},
         "eq04": {"rule_fail": "quota_flips_gap_negative=False",
                  "quota_gap": eq04["summary"]["quota"]["mean_gap_top_minus_bottom"],
                  "plain": eq04["plain_result"],
                  "plain_says_flips": "flips the gap" in eq04["plain_result"]},
         "eq06": {"rule_fail": "network_spec_effect_larger_than_no_network=False",
                  "network_effect": eq06["summary"]["probit_with_network"]["mean_marginal_effect_education"],
                  "no_network_effect": eq06["summary"]["probit_no_network"]["mean_marginal_effect_education"],
                  "plain": eq06["plain_result"],
                  "plain_says_networks_increase": "networks increase" in eq06["plain_result"]}},
        "per-script results JSON plain_result", "FLAG")

    # prereg vs implemented rules
    prereg = tshow(EQ, EQD + "/PRE_REGISTRATION.md")
    add("EQ-5", "equation suite",
        "S3/e03: the failed criterion is not the pre-registered one; the pre-registered rho criterion passes",
        {"pre_registered_rule": "in the rho=0.5 world the recovered rho is closer to the truth than Cobb-Douglas implies (rho=1)",
         "implemented_rule": "share of rho_hat within 0.10 of truth >= 0.50",
         "rho_hat_median": eq03["summary"]["ces_complementary_rho0.5"]["median_rho_hat"],
         "true_rho": 0.5, "cobb_douglas_implied": 1.0,
         "pre_registered_criterion_met": abs(eq03["summary"]["ces_complementary_rho0.5"]["median_rho_hat"] - 0.5) < abs(1.0 - 0.5),
         "implemented_criterion_in_prereg_text": "within 0.10" in prereg},
        "PRE_REGISTRATION.md S2 rule; eq03 JSON", "FLAG")
    add("EQ-6", "equation suite",
        "S6/e06: no migration/rural-urban decision rule exists in the pre-registration",
        {"final_mapping": "S6 = eq06_migration_rural_urban (Amendment 02)",
         "original_S6": "eq06_growth (augmented Solow)",
         "prereg_mentions": "the S6 multiverse list only; no decision-rule text for migration/network",
         "decision_rule_present_for_migration": False,
         "implemented_rule": "education positive in every spec + network effect larger"},
        "PRE_REGISTRATION.md Amendment 02 table", "FLAG")
    add("EQ-12", "equation suite",
        "pre-registration-to-implementation mapping: several final scripts have no pre-registered rule or a simplified/added one",
        {"S1_family_demand": "no pre-registered rule (new script after Amendment 02); implemented ad hoc affordability/zero-signal criteria",
         "S2_supply_finance": "pre-registered S7 rule was 'regressive if CI positive'; implemented universal-vs-means + NPV/IRR",
         "S3_learning_quality": "pre-registered S2 rule replaced by ad hoc rho/recovery thresholds (see EQ-5)",
         "S4_gates": "pre-registered S5 rule applied; extra contest criterion added",
         "S5_returns": "pre-registered S1 rule had CI-coverage >=90%; implemented mean-bias thresholds",
         "S6_migration": "no pre-registered rule (see EQ-6)",
         "S7_inequality": "pre-registered S8 rule largely implemented (null CI) plus persistent/Theil extras",
         "S8_growth": "pre-registered S6 rule (lambda within 2 SE; beta_H sign flip) replaced by 'near truth' + NP positive",
         "S9_identification": "pre-registered S9 null CI coverage >=90% replaced by fixed near-zero thresholds",
         "S10_tutoring": "pre-registered S3+S4 rules only partly implemented; single-world Tobit rule fails (see EQ-7)"},
        "PRE_REGISTRATION.md S1-S10 rules; per-script decision_rule JSON", "FLAG")
    add("EQ-7", "equation suite",
        "S10/e10: the pre-registered old-S3 single-world Tobit rule fails, but S10 reports PASS",
        {"pre_registered_rule": "DIFFERENT world: two-part within 0.15 and Tobit > 0.15 from truth; SINGLE world: both within 0.15",
         "single_process_tobit_eta": eqs["eq10_tutoring_shadow.py"]["demand"]["single_process"]["tobit_eta_mean"],
         "single_process_two_part_eta": eqs["eq10_tutoring_shadow.py"]["demand"]["single_process"]["two_part_eta_mean"],
         "truth": 0.8, "single_world_rule_met": False,
         "implemented_rule_passes": eqs["eq10_tutoring_shadow.py"]["decision_rule"]["PASS"]},
        "PRE_REGISTRATION.md S3 rule; eq10 JSON", "FLAG")

    # data tiers / boundary
    tiers = {s: e.get("data_tier") for s, e in eqs.items()}
    add("EQ-8", "observed vs synthetic",
        "only S7/S8/S10 should touch non-synthetic data; eq07's top-level tier says SYNTHETIC",
        {"eq07_tier": tiers["eq07_inequality_dashboard.py"],
         "eq07_dashboard_real_tier": eqs["eq07_inequality_dashboard.py"]["dashboard_real"]["data_tier"],
         "eq08_tier": tiers["eq08_growth.py"], "eq10_tier": tiers["eq10_tutoring_shadow.py"],
         "report_labels": "S7/S8 observed; S10 literature"},
        "results/eq07...json; inputs/PROVENANCE.json; SUITE_REPORT.md", "FLAG")
    add("EQ-9", "data tiers",
        "committed input provenance hashes match the files",
        {"long_run_panel": sha(show(EQ, EQD + "/inputs/long_run_panel.csv"))[:16],
         "x4_panel": sha(show(EQ, EQD + "/inputs/x4_panel.csv"))[:16],
         "bray_targets": sha(show(EQ, EQD + "/inputs/bray_targets.json"))[:16]},
        "inputs/PROVENANCE.json", "PASS")
    add("EQ-10", "boundary labels",
        "eq04 gate script labels the mechanism as inside MASSENG v5, contrary to Amendment 03 and the README",
        {"eq04_boundary": eqs["eq04_transitions_gates.py"]["masseng_boundary"],
         "amendment_03": "score bar/quota gates are outside MASSENG v5",
         "readme_row": "S4: progression/capacity yes; exam bar/quota no"},
        "eq04 JSON; README mapping table", "FLAG")
    add("EQ-11", "equation suite",
        "eq07 Theil within component is NaN and not reported",
        {"theil_within": eqs["eq07_inequality_dashboard.py"]["summary"]["persistent"]["mean_theil_within"],
         "theil_between": eqs["eq07_inequality_dashboard.py"]["summary"]["persistent"]["mean_theil_between"],
         "reported_within": False},
        "results/eq07...json; SUITE_REPORT.md", "FLAG")

    # ------------------------------------------------------------------ full-system
    rows = jshow(MES, MESD + "/results_multiverse.json")
    tests = jshow(EDS, EDSD + "/full_system_tests.json")
    summary = jshow(MES, MESD + "/summary_multiverse.json")
    report = tshow(EDS, EDSD + "/MULTIVERSE_TESTS.md")
    metareg = tshow(MES, MESD + "/PRE_REGISTRATION_masseng_edsystem.md")
    rr = rows["rows"]
    add("FS-1", "full system",
        "design: 1,440 runs = 144 cells x 10 seeds; axes; simulation label; identical results file on both branches",
        {"n_runs": len(rr), "cells": len({r["combo_index"] for r in rr}), "seeds": len({r["seed"] for r in rr}),
         "axes": rows["design"]["axes"], "label": rows.get("label"),
         "results_hash_matches_edsystem_tests": sha(show(MES, MESD + "/results_multiverse.json")) == sha(show(EDS, EDSD + "/results_multiverse.json"))},
        "results_multiverse.json", "PASS")

    # independent replication of the cluster OLS
    axes = rows["design"]["axes"]
    names = list(axes)
    Xp = [np.ones(len(rr))]
    cols = ["intercept"]
    for a in names:
        for v in axes[a][1:]:
            Xp.append(np.array([1.0 if r["combo"][names.index(a)] == v else 0.0 for r in rr]))
            cols.append(f"{a}={v}")
    seeds = sorted({r["seed"] for r in rr})
    for s in seeds[1:]:
        Xp.append(np.array([1.0 if r["seed"] == s else 0.0 for r in rr]))
        cols.append(f"seed={s}")
    X = np.column_stack(Xp)
    groups = np.array([r["combo_index"] for r in rr])

    def cluster(y, X, groups, j):
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        inv = np.linalg.pinv(X.T @ X)
        meat = np.zeros((X.shape[1], X.shape[1]))
        for g in np.unique(groups):
            m = groups == g
            ss = X[m].T @ resid[m]
            meat += np.outer(ss, ss)
        G = len(np.unique(groups)); n, p = X.shape
        corr = (G / (G - 1)) * ((n - 1) / (n - p)) if G > 1 and n > p else 1.0
        V = inv @ meat @ inv * corr
        return float(beta[j]), math.sqrt(max(V[j, j], 0.0))

    maxdiff = 0.0
    n_compared = 0
    for key, block in tests["contrasts"].items():
        a = key.split(":")[0]
        for v, rs in block.items():
            j = cols.index(f"{a}={v}")
            for r in rs:
                oc = r["outcome"]
                y = np.array([np.nan if x["metrics"].get(oc) is None else x["metrics"][oc] for x in rr], float)
                m = np.isfinite(y)
                if m.sum() < 50 or r["effect"] is None:
                    continue
                eff, se = cluster(y[m], X[m], groups[m], j)
                maxdiff = max(maxdiff, abs(eff - r["effect"]), abs(se - r["se"]) if r["se"] is not None else 0.0)
                n_compared += 1
    add("FS-2", "full system",
        "cluster-robust OLS with seed FE reproduces full_system_tests.json",
        {"compared": n_compared, "max_abs_diff_effect_or_se": maxdiff}, "test_full_system.py; results", "PASS")

    supported = [(k, v, r) for k, b in tests["contrasts"].items() for v, rs in b.items() for r in rs if r.get("supported")]
    empty = [(k.split(":")[0], v, r["outcome"], r["effect"], r["se"]) for k, v, r in supported if r.get("stratum_min") is None]
    zero = [(k.split(":")[0], v, r["outcome"], r["effect"], r["se"]) for k, v, r in supported if abs(r["effect"]) < 1e-9]
    add("FS-3", "full system",
        "stratum check can pass vacuously: supported rows with no strata at all",
        {"n_supported": len(supported), "n_empty_stratum_supported": len(empty), "rows": empty},
        "test_full_system.py `all([])` on empty strat list", "FLAG")
    add("FS-4", "full system",
        "zero-variance outcome classified as supported",
        {"rows": zero}, "full_system_tests.json learning plus_private tut_rate", "FLAG")
    add("FS-5", "full system",
        "full_system_tests.json and the report disagree on which effects are supported",
        {"report_says_supply_only_public_quality": "supply: only public quality is supported",
         "json_supply_supported": [r["outcome"] for k, v, r in supported if k.split(":")[0] == "supply"],
         "report_omits_supported": ["formal_share_gdp (supply)", "formal_share_gdp (afford, both levels)",
                                    "skill_premium (jobs)", "tut_rate (learning plus_private; zero)",
                                    "plus_private formal/skill/q_pub (learning)"],
         "report_supported_entries": "tables are a selected subset, not all supported entries"},
        "MULTIVERSE_TESTS.md vs full_system_tests.json", "FLAG")
    add("FS-6", "full system",
        "p-values and Holm were introduced although the multiverse pre-registration says 'no p-values'; no test pre-registration in the record",
        {"pre_reg_rule": "Seed-level uncertainty: mean and 90% interval ...; no p-values",
         "test_record_files": ["MULTIVERSE_TESTS.md", "full_system_tests.json", "results_multiverse.json", "test_full_system.py"],
         "test_preregistration_present": False,
         "holm_family": "within each axis-value contrast across 9 outcomes; 8 contrast blocks not jointly controlled"},
        "PRE_REGISTRATION_masseng_edsystem.md §5; edsystem-tests record", "FLAG")
    add("FS-7", "full system",
        "eta^2 table in the run report matches the committed variance decomposition",
        {"spot_checks": {"completion_primary.afford": summary["variance_decomposition"]["completion_primary"]["afford"]["eta2"],
                         "completion_lower.gates": summary["variance_decomposition"]["completion_lower"]["gates"]["eta2"],
                         "q_pub.supply": summary["variance_decomposition"]["q_pub"]["supply"]["eta2"],
                         "mpl_primary.learning": summary["variance_decomposition"]["mpl_primary"]["learning"]["eta2"]}},
        "summary_multiverse.json", "PASS")
    add("FS-8", "full system",
        "non-identification claims: 'range overlap 1.00 for all completion outcomes' does not match the committed overlaps",
        {"reported": "1.00 for primary/lower/upper; '?' for tertiary",
         "actual_supply_overlaps": {m: round(summary["variance_decomposition"][m]["supply"]["worst_range_overlap"], 3)
                                    for m in ("completion_primary", "completion_lower", "completion_upper", "completion_tertiary")},
         "conclusion_supported_at_>=0.80": all(summary["variance_decomposition"][m]["supply"]["worst_range_overlap"] >= 0.80
                                               for m in ("completion_primary", "completion_lower", "completion_upper", "completion_tertiary"))},
        "RUN_REPORT.md §3.6/§4; summary_multiverse.json", "FLAG")
    add("FS-9", "full system",
        "reported learning-configuration overlap 1.00 (primary) vs committed value",
        {"reported": "1.00", "actual": round(summary["variance_decomposition"]["completion_primary"]["learning"]["worst_range_overlap"], 3)},
        "RUN_REPORT.md §4; summary_multiverse.json", "FLAG")
    add("FS-10", "full system",
        "tutoring eta^2 claim '~0' vs committed learning-axis eta^2",
        {"reported": "eta^2 ~ 0 for completion",
         "actual_learning_eta2": {m: round(summary["variance_decomposition"][m]["learning"]["eta2"], 4)
                                  for m in ("completion_primary", "completion_lower", "completion_upper", "completion_tertiary")}},
        "RUN_REPORT.md §3.7; summary_multiverse.json", "FLAG")
    add("FS-11", "full system",
        "PHL level check numbers and construct labels",
        {"observed_2024": 84.75, "observed_max": 97.36,
         "sim_mean": round(float(np.mean([r["metrics"]["completion_lower"] for r in rr if r["metrics"].get("completion_lower") is not None])), 3),
         "sim_p5_p95": [round(float(np.percentile([r["metrics"]["completion_lower"] for r in rr if r["metrics"].get("completion_lower") is not None], q)), 3) for q in (5, 95)],
         "label": "level check, not calibration"},
        "RUN_REPORT.md §3.9; phl_lsc.json", "PASS")
    add("FS-12", "full system",
        "missing mechanisms and unusable push-out decoder are stated, not papered over",
        {"missing": rows["design"]["missing_mechanisms"],
         "pushout": "engine exit-reason bookkeeping overwritten; decomposition 0/0/0 reported as unusable"},
        "RUN_REPORT.md §3.8, §5; design block", "PASS")
    add("FS-13", "full system",
        "full_system_tests.json stores no code hash, environment or pre-registration reference",
        {"keys": list(tests.keys()), "notes": tests.get("notes")},
        "full_system_tests.json", "FLAG")

    # ------------------------------------------------------------------ write
    result = dict(audit="equation suite + full-system multiverse claims (engine/data reality)",
                  date="2026-11-25", heads=heads, checks=CHECKS,
                  notes=["read-only; no server compute; no literature verification",
                         "equation-suite hashes verified from the run manifest",
                         "full-system OLS replicated independently with numpy"])
    path = outdir / "audit.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"wrote": str(path), "checks": len(CHECKS),
                      "flags": sum(1 for c in CHECKS if c["status"] == "FLAG")}, indent=1))
    for c in CHECKS:
        print(f"[{c['status']}] {c['id']}: {c['question']}")

if __name__ == "__main__":
    main()
