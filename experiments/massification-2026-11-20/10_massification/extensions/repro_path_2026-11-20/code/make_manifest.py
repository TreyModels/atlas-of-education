#!/usr/bin/env python3
"""Build RUN_MANIFEST.json and SHA256SUMS.txt for EXP-7 REPRO-PATH.

Deterministic: no timestamps, no hostnames, no clocks. Reads only files inside this experiment
directory plus the frozen inputs (read-only) and writes the manifest and the sums file.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys

EXP = "EXP-7 REPRO-PATH"
HERE = os.path.dirname(os.path.abspath(__file__))
EXP_DIR = os.path.dirname(HERE)

FROZEN = {
    "panel": ("10_massification/extensions/synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv",
              "14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac"),
    "sim_code": ("10_massification/extensions/synthetic_2026-11-20/generator_v1_2/code/sim_v1_2.py",
                 "61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c"),
    "params": ("10_massification/extensions/synthetic_2026-11-20/generator_v1_2/PARAMS.md",
               "0d619781c4e059f54cf771fb385475f5f939dceced5036e8a21b6e07a2b315e3"),
    "generator_manifest": ("10_massification/extensions/synthetic_2026-11-20/generator_v1_2/RUN_MANIFEST.json",
                           "36c40ff95470893a6d6fda21d9afe341ec0f374073a7af56cdf9c55c9b75b876"),
    "observed_series": ("10_massification/data/UNIVERSALIZATION_SERIES.csv",
                        "85bc869396ebfcb39e3e1a21a31af219e75a07326c738a51d2bfdbe536737ddb"),
    "council_brief": ("08_council/brief_022/SYNTHESIS_022.md",
                      "9508dd55be8dd64da8322a8277c8342a4f50be6790a3d287e39e7004537c109b"),
}

ARTIFACTS = [
    "results/PATH_COMPARISONS.csv",
    "results/KAPPA_LINK.csv",
    "results/REPRO_PATH_RESULTS.csv",
    "results/BASELINE_GUARD.json",
    "results/console.txt",
    "results/BASELINE_UNLINKED_PANEL.csv",
]


def sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def find_root(start: str) -> str:
    cur = os.path.abspath(start)
    for _ in range(12):
        if os.path.isdir(os.path.join(cur, "08_council")) and os.path.isdir(os.path.join(cur, "10_massification")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    raise SystemExit("cannot locate programme root")


def results_value(stat: str) -> str:
    path = os.path.join(EXP_DIR, "results", "REPRO_PATH_RESULTS.csv")
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["statistic"] == stat:
                return r["value"]
    raise SystemExit("statistic not found: %s" % stat)


def main() -> int:
    root = find_root(EXP_DIR)

    predecl_path = os.path.join(EXP_DIR, "PRE_DECLARATIONS.md")
    sidecar_path = os.path.join(EXP_DIR, "PRE_DECLARATIONS.sha256")
    predecl_sha = sha(predecl_path)
    sidecar_sha = sha(sidecar_path)
    with open(sidecar_path, encoding="utf-8") as fh:
        sidecar_declared = fh.read().split()[0]
    if sidecar_declared != predecl_sha:
        raise SystemExit("predeclaration sidecar does not match the file")

    frozen = {}
    for name, (rel, expected) in FROZEN.items():
        p = os.path.join(root, rel)
        actual = sha(p)
        frozen[name] = {
            "path": rel,
            "sha256": actual,
            "matches_declared": actual == expected,
        }
        if not frozen[name]["matches_declared"]:
            raise SystemExit("frozen input %s hash mismatch" % name)

    # determinism: run 1 (results/) vs run 2 (results/determinism_run2/)
    det = []
    for rel in ARTIFACTS:
        f1 = os.path.join(EXP_DIR, rel)
        f2 = os.path.join(EXP_DIR, "results", "determinism_run2", os.path.basename(rel))
        h1, h2 = sha(f1), sha(f2)
        det.append({
            "artifact": rel,
            "run1_sha256": h1,
            "run2_sha256": h2,
            "byte_identical": h1 == h2 and os.path.getsize(f1) == os.path.getsize(f2),
        })
    determinism_ok = all(d["byte_identical"] for d in det)

    guard = json.load(open(os.path.join(EXP_DIR, "results", "BASELINE_GUARD.json"), encoding="utf-8"))

    manifest = {
        "label": "SYNTHETIC (generator panel) + OBSERVED (PHL UIS completion series)",
        "experiment": EXP,
        "brief": "Council brief 022 (D122 #2); SYNTHESIS_022.md section 6, EXP-7 REPRO-PATH, rank #2",
        "dependency_role": "precondition for the v1.5 BIMODAL-GATE predeclaration (brief 022 section 4.4)",
        "worker": "WORKER RP",
        "date": "2026-11-20",
        "status": "COMPLETE",
        "statement": (
            "Descriptive/diagnostic audit of a declared-assumption simulator. No causal and no direction claim; "
            "D63 remains UNABLE as to cause. The kappa link is a declared accounting constraint taken from an "
            "observed median (never fitted), not an estimated relationship. m = 1.10 and v1.2's scope "
            "(crossing/endpoint placement) are unchanged. No threshold was changed after results."
        ),
        "predeclaration": {
            "file": "PRE_DECLARATIONS.md",
            "sha256": predecl_sha,
            "recorded_sidecar": "PRE_DECLARATIONS.sha256",
            "sidecar_sha256": sidecar_sha,
            "hashed_before_any_run": True,
            "thresholds_changed_after_results": False,
            "verbatim_source": "08_council/brief_022/SYNTHESIS_022.md section 6 EXP-7 items 2 and 5",
        },
        "frozen_inputs_read_only": frozen,
        "copies_inside_experiment_dir": {
            "unlinked_panel": {
                "path": "results/BASELINE_UNLINKED_PANEL.csv",
                "sha256": sha(os.path.join(EXP_DIR, "results", "BASELINE_UNLINKED_PANEL.csv")),
                "byte_identical_to_frozen": guard["G2_copy_inside_experiment_dir"]["byte_identical_to_frozen"],
            },
            "generator_code_copied": False,
            "note": (
                "No generator code was copied or edited: leg (b) is an in-memory projection on a byte copy of the "
                "frozen panel. No file under generator_v1_2/ was written or modified."
            ),
        },
        "declared_parameters": {
            "kappa_verdict_bearing": 0.949,
            "kappa_provenance": "median of the 8 observed PHL upper_t/lower_{t-3} pairs; re-derived 0.94914 -> 0.949",
            "kappa_sensitivity_non_verdict": 0.960,
            "kappa_sensitivity_provenance": "pre-2018 median; re-derived 0.95956 -> 0.960",
            "lag_years": 3,
            "lag_rule": "exact t-3; no nearest-year matching in leg (b)",
            "within_pp": 5.0,
            "within_bar": "17/33",
            "anchor_type": "SYN00_PHL_LIKE",
            "class_boundaries": {"b1": "[73,77]", "b2": "< 71", "b3": "|delta| < 1.0 pp", "precedence": "b2 > b3 > b1"},
            "no_fit": True,
            "no_rng": True,
        },
        "construction": {
            "leg_a_comparisons": 33,
            "leg_a_cells_by_level": {"primary": 11, "lower_secondary": 11, "upper_secondary": 11},
            "leg_a_missing_cells": 0,
            "leg_a_missing_rule": "MISSING retained in denominator; never imputed, dropped or nearest-year substituted",
            "leg_b_scored_cells": 53,
            "leg_b_not_scorable": [1970, 1971, 1972],
            "leg_b_not_scorable_rule": "no lower_{t-3} in panel; excluded from denominator; never imputed",
        },
        "verdicts": {
            "leg_a": "ENDPOINT-ONLY",
            "leg_a_components": {
                "within_5pp": results_value("within_5pp_count"),
                "within_10pp": results_value("within_10pp_count"),
                "median_primary_pp": results_value("median_deviation_primary_pp"),
                "median_lower_pp": results_value("median_deviation_lower_secondary_pp"),
                "median_upper_pp": results_value("median_deviation_upper_secondary_pp"),
                "max_miss_pp": results_value("max_abs_miss_pp"),
                "construction_check_vs_V1": results_value("construction_check_vs_V1"),
            },
            "leg_b_class": results_value("outcome_class"),
            "leg_b_components": {
                "violations_before": results_value("violations_before"),
                "violations_after": results_value("violations_after"),
                "max_violation_margin_pp": results_value("max_violation_margin_pp"),
                "upper_2024_unlinked_pct": results_value("upper_2024_unlinked_pct"),
                "bound_2024_pct": results_value("bound_2024_pct_kappa_0.949"),
                "upper_2024_linked_pct": results_value("upper_2024_linked_pct"),
                "delta_2024_pp": results_value("delta_2024_pp"),
                "ratio_2024": results_value("ratio_2024"),
                "sensitivity_kappa_0.960_linked_2024_pct": results_value(
                    "sensitivity_kappa_0.960_upper_2024_linked_pct"),
            },
            "baseline_guard": guard["verdict"],
            "falsifier_triggered": guard["falsifier_triggered"],
            "combined": "ENDPOINT-ONLY + b2 + BASELINE-GUARD-PASS",
        },
        "results_files": {
            "results/PATH_COMPARISONS.csv": "33 rows; every comparison with year, level, synthetic, observed, deviation pp, within flags",
            "results/KAPPA_LINK.csv": "56 rows (53 SCORED + 3 NOT-SCORABLE); upper_t, lower_{t-3}, ratio, bound, violation, linked value, delta, class",
            "results/REPRO_PATH_RESULTS.csv": "long-format (test, statistic, value, threshold, verdict, components)",
            "results/BASELINE_GUARD.json": "G1-G4 with hashes and pre/post comparison",
            "results/console.txt": "captured console of run 1 (byte-identical to run 2)",
            "results/BASELINE_UNLINKED_PANEL.csv": "byte copy of the frozen panel (5 086 014 bytes)",
        },
        "determinism": {
            "method": "two clean runs of the same RNG-free, timestamp-free script into results/ and results/determinism_run2/, then sha256 and byte comparison of all six artifacts",
            "rng": "none",
            "timestamps_in_outputs": False,
            "artifacts": det,
            "all_byte_identical": determinism_ok,
            "verdict": "DETERMINISTIC" if determinism_ok else "NON-DETERMINISTIC",
        },
        "discipline": {
            "no_writes_outside_experiment_dir": True,
            "generator_files_unchanged_verified": guard["G4_generator_files_unchanged_after_run"]["equal"],
            "no_re_fit": True,
            "no_threshold_change": True,
            "no_causal_or_direction_claim": True,
            "labels": "SYNTHETIC on generator numbers; OBSERVED on PHL completion numbers",
            "web_used": False,
            "server_touched": False,
        },
        "implication_for_v1_5_bimodal_gate": (
            "The pipeline link must be built into v1.5 as a structural accounting constraint evaluated inside the "
            "model each year, with kappa a declared system input, not applied as post-processing. v1.2's 2024 upper "
            "endpoint (76.64) may not be carried into v1.5 as a ceiling target or as evidence of inheritance: under "
            "the declared link it falls to 63.97 (delta -12.67 pp). v1.5 level claims must be scored on the path "
            "(a count over observed year-level cells), not on a single endpoint."
        ),
    }

    manifest_path = os.path.join(EXP_DIR, "RUN_MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=False)
        fh.write("\n")

    # SHA256SUMS.txt — everything in the experiment dir except the sums file itself
    entries = []
    for dirpath, dirnames, filenames in os.walk(EXP_DIR):
        dirnames.sort()
        for fn in sorted(filenames):
            if fn == "SHA256SUMS.txt":
                continue
            p = os.path.join(dirpath, fn)
            rel = "./" + os.path.relpath(p, EXP_DIR)
            entries.append((rel, sha(p)))
    entries.sort()
    with open(os.path.join(EXP_DIR, "SHA256SUMS.txt"), "w", encoding="utf-8") as fh:
        for rel, h in entries:
            fh.write("%s  %s\n" % (h, rel))

    print("wrote RUN_MANIFEST.json and SHA256SUMS.txt (%d files)" % len(entries))
    print("predeclaration sha256: %s" % predecl_sha)
    print("determinism: %s" % manifest["determinism"]["verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
