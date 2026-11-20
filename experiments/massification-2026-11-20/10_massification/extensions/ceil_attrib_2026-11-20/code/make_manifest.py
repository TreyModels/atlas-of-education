#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble RUN_MANIFEST.json for EXP-1 CEIL-ATTRIB from the files on disk.

Run after the two determinism runs. Pure file hashing; no RNG, no network. The manifest
records the predeclaration, the experiment code, the frozen v1.2 objects this experiment
copied/read, every input, every result, and the two-run byte-identity evidence.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

MYROOT = Path(__file__).resolve().parent.parent
MAIN = MYROOT / "results"
DET = MAIN / "determinism_run2"


def sha(rel):
    return hashlib.sha256((MYROOT / rel).read_bytes()).hexdigest()


def main():
    ev = json.load(open(MAIN / "EVIDENCE.json"))
    res_files = ["CEIL_ATTRIB_RESULTS.csv", "CEIL_ATTRIB_DETAIL.csv",
                 "ABLATION_PANEL.csv", "EVIDENCE.json"]
    det_files = {}
    for f in res_files:
        a, b = sha(f"results/{f}"), sha(f"results/determinism_run2/{f}")
        det_files[f] = {"run1_sha256": a, "run2_sha256": b, "byte_identical": a == b}
    a = sha("results/baseline_reproduction/synthetic_panel_v1_2.csv")
    b = sha("results/determinism_run2/baseline_reproduction/synthetic_panel_v1_2.csv")
    det_files["baseline_reproduction/synthetic_panel_v1_2.csv"] = {
        "run1_sha256": a, "run2_sha256": b, "byte_identical": a == b}

    manifest = {
        "label": "SYNTHETIC (generator) + OBSERVED (PHL UIS series)",
        "experiment": "EXP-1 CEIL-ATTRIB",
        "brief": "Council brief 021 (D112 #1); SYNTHESIS_021.md section 4, EXP-1, rank #1",
        "worker": "WORKER CA",
        "date": "2026-11-20",
        "status": "COMPLETE",
        "statement": ("Synthetic generator numbers come from declared assumptions only and "
                      "are not evidence, not an estimate, not a forecast, and license no "
                      "causal or direction claim. Test B uses the observed PHL UIS "
                      "completion series and is labelled OBSERVED. D63 is reclassified, "
                      "not explained."),
        "predeclaration": {
            "file": "PRE_DECLARATIONS.md",
            "sha256": sha("PRE_DECLARATIONS.md"),
            "recorded_sidecar": "PRE_DECLARATIONS.sha256",
            "sidecar_sha256": sha("PRE_DECLARATIONS.sha256"),
            "hashed_before_any_run": True,
            "thresholds_changed_after_results": False,
            "verbatim_source": ("08_council/brief_021/SYNTHESIS_021.md section 4 EXP-1 "
                                "items 2, 5, 6"),
        },
        "frozen_objects_read_only": {
            "code": {"file": "../synthetic_2026-11-20/generator_v1_2/code/sim_v1_2.py",
                     "sha256": "61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c"},
            "params": {"file": "../synthetic_2026-11-20/generator_v1_2/PARAMS.md",
                       "sha256": "0d619781c4e059f54cf771fb385475f5f939dceced5036e8a21b6e07a2b315e3"},
            "panel": {"file": "../synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv",
                      "sha256": "14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac"},
            "v12_spec": {"file": "../synthetic_2026-11-20/v1_2/PRE_DECLARATIONS.md",
                         "sha256": "fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16"},
            "v12_manifest": {"file": "../synthetic_2026-11-20/generator_v1_2/RUN_MANIFEST.json",
                             "sha256": "36c40ff95470893a6d6fda21d9afe341ec0f374073a7af56cdf9c55c9b75b876"},
            "frozen_untouched_verified_after_run": True,
        },
        "copies_inside_experiment_dir": {
            "code": {"path": "generator_v1_2/code/sim_v1_2.py",
                     "sha256": sha("generator_v1_2/code/sim_v1_2.py"),
                     "byte_identical_to_frozen": sha("generator_v1_2/code/sim_v1_2.py") ==
                     "61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c"},
            "params": {"path": "generator_v1_2/PARAMS.md",
                       "sha256": sha("generator_v1_2/PARAMS.md"),
                       "byte_identical_to_frozen": sha("generator_v1_2/PARAMS.md") ==
                       "0d619781c4e059f54cf771fb385475f5f939dceced5036e8a21b6e07a2b315e3"},
            "v12_spec": {"path": "v1_2/PRE_DECLARATIONS.md",
                         "sha256": sha("v1_2/PRE_DECLARATIONS.md"),
                         "byte_identical_to_frozen": sha("v1_2/PRE_DECLARATIONS.md") ==
                         "fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16"},
        },
        "experiment_code": {
            "run_script": {"path": "code/run_ceil_attrib.py",
                           "sha256": sha("code/run_ceil_attrib.py")},
            "manifest_builder": {"path": "code/make_manifest.py",
                                 "sha256": sha("code/make_manifest.py")},
        },
        "findings": {"path": "FINDINGS.md", "sha256": sha("FINDINGS.md")},
        "inputs": {
            "UNIVERSALIZATION_SERIES.csv": sha("../../data/UNIVERSALIZATION_SERIES.csv"),
            "panel_wdi_long.csv": sha("../../../09_relations/data/panel_wdi_long.csv"),
            "STATE_CAPACITY.csv": sha("../../data/STATE_CAPACITY.csv"),
            "SCHOOL_EXPANSION.csv": sha("../../data/SCHOOL_EXPANSION.csv"),
            "economic_complexity_panel_30ctys.csv": sha("../../../09_relations/data/economic_complexity_panel_30ctys.csv"),
            "gmr_observed_6countries_1970_2024.csv": sha("../../../data/gmr_observed_6countries_1970_2024.csv"),
        },
        "baseline_invariance": {
            "requirement": ("unmodified copy reproduces results/synthetic_panel_v1_2.csv "
                            "byte-for-byte"),
            "reproduced_panel": "results/baseline_reproduction/synthetic_panel_v1_2.csv",
            "reproduced_panel_sha256": sha("results/baseline_reproduction/synthetic_panel_v1_2.csv"),
            "frozen_panel_sha256": "14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac",
            "byte_identical": ev["baseline_invariance"]["byte_identical"],
            "driver_with_no_switch_byte_identical": ev["baseline_invariance"]["driver_baseline_byte_identical"],
            "resolved": ev["baseline_invariance"]["resolved"],
            "checks_csv_sha256": {
                "reproduction_checks_v1_2.csv": sha("results/baseline_reproduction/reproduction_checks_v1_2.csv"),
                "reproduction_checks_detail_v1_2.csv": sha("results/baseline_reproduction/reproduction_checks_detail_v1_2.csv"),
            },
        },
        "results": {
            "CEIL_ATTRIB_RESULTS.csv": sha("results/CEIL_ATTRIB_RESULTS.csv"),
            "CEIL_ATTRIB_DETAIL.csv": sha("results/CEIL_ATTRIB_DETAIL.csv"),
            "ABLATION_PANEL.csv": sha("results/ABLATION_PANEL.csv"),
            "EVIDENCE.json": sha("results/EVIDENCE.json"),
            "console_run1": sha("results/run1_console.txt"),
            "console_run2": sha("results/determinism_run2/console.txt"),
        },
        "determinism": {
            "method": ("two full runs (results/ and results/determinism_run2/), byte "
                       "comparison of every result file"),
            "files": det_files,
            "all_byte_identical": all(v["byte_identical"] for v in det_files.values()),
            "driver_adds_rng": False,
            "generator_rng": ("numpy PCG64, single stream, seed 20261120, fixed draw "
                              "order; identical across variants"),
            "wall_clock_or_os_entropy_in_outputs": False,
        },
        "verdicts": {
            "test_A": ev["test_A"]["verdict"],
            "test_B": ev["test_B"]["lag3"]["verdict"],
            "overall_ceil_attrib": ev["overall_decision"],
            "matrix_cell": ("(a) pipeline-consistent: residual reclassified as "
                            "lower-pipeline inheritance; D63 stays UNABLE as to cause; "
                            "no demand/exit-cost claim"),
            "test_A_component": {
                "baseline_upper_uis_2024": ev["test_A"]["baseline_upper_uis_2024"],
                "mech_hits": ev["test_A"]["mech_hits"],
                "calib_absmax_pp": ev["test_A"]["calib_absmax_pp"],
                "calib_ge_2pp": ev["test_A"]["calib_ge_2pp"],
                "calib_all_lt_1pp": ev["test_A"]["calib_all_lt_1pp"],
                "mech_all_lt_2pp": ev["test_A"]["mech_all_lt_2pp"],
            },
            "test_B_component": {
                "lag": ev["test_B"]["declared_lag"],
                "n_pairs": ev["test_B"]["lag3"]["n"],
                "in_band": ev["test_B"]["lag3"]["inband"],
                "below_0_90": ev["test_B"]["lag3"]["below"],
                "share_in_band": ev["test_B"]["lag3"]["frac_in"],
            },
        },
        "ablation_variants": ev["variants"],
        "environment": {"python": ev["python"], "numpy": ev["numpy"], "platform": "macOS"},
        "discipline": {
            "writes_outside_experiment_dir": False,
            "web_used": False,
            "external_data_used": False,
            "server_touched": False,
            "re_fit_or_parameter_change_after_freeze": False,
            "c1_c4_reopened": False,
            "wt4_rescored": False,
            "direction_or_causal_claim": False,
        },
    }
    (MYROOT / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("manifest written; all_byte_identical =", manifest["determinism"]["all_byte_identical"])
    print("A =", manifest["verdicts"]["test_A"], "| B =", manifest["verdicts"]["test_B"],
          "| overall =", manifest["verdicts"]["overall_ceil_attrib"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
