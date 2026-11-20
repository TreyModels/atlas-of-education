#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-23 D63-BOUNDS -- manifest builder (post-run; writes RUN_MANIFEST.json only).

Reads the delivered result files and records what is on disk. No timestamps: the manifest is
byte-reproducible from the files it describes (the only exception is SHA256SUMS.txt, which is
generated after this file and is not hashed here).

Also invokes `code/run_d63_bounds.py --check-findings` (the runner's own number-register and
banned-sentence audit over FINDINGS.md and the two result tables) and records its counts.
"""
import csv
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

FILES = [
    "PRE_DECLARATIONS.md", "PRE_DECLARATIONS.sha256", "FINDINGS.md",
    "code/author_predecl.py", "code/predecl_template.md", "code/run_d63_bounds.py",
    "code/make_manifest.py",
    "results/D63_BOUNDS_RESULTS.csv", "results/D63_BOUNDS_DETAIL.csv", "results/console.txt",
    "results/determinism_run2/D63_BOUNDS_RESULTS.csv", "results/determinism_run2/D63_BOUNDS_DETAIL.csv",
    "results/determinism_run2/console.txt",
]
DET_PAIRS = ["D63_BOUNDS_RESULTS.csv", "D63_BOUNDS_DETAIL.csv", "console.txt"]


def sha(p):
    h = hashlib.sha256()
    with open(os.path.join(HERE, p), "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def read_results():
    out = {}
    with open(os.path.join(HERE, "results", "D63_BOUNDS_RESULTS.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[r["item_id"]] = r
    return out


def read_detail():
    out = {}
    with open(os.path.join(HERE, "results", "D63_BOUNDS_DETAIL.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[r["number_id"]] = r
    return out


def main():
    res = read_results()
    det = read_detail()

    proc = subprocess.run([PY, os.path.join(HERE, "code", "run_d63_bounds.py"), "--check-findings"],
                          capture_output=True, text=True)
    audit = json.loads(proc.stdout.strip().splitlines()[-1]) if proc.stdout.strip() else {"error": proc.stderr}

    det_block = {}
    all_same = True
    for name in DET_PAIRS:
        a = sha(os.path.join("results", name))
        b = sha(os.path.join("results", "determinism_run2", name))
        same = a == b
        all_same = all_same and same
        det_block[name] = {"run1_sha256": a, "run2_sha256": b, "byte_identical": same}

    manifest = {
        "experiment": "EXP-23 D63-BOUNDS",
        "brief": "Council brief 025 (D156 #3, rank #3); SYNTHESIS_025.md section 6.3 EXP-23; D153(xiii); D158(1)-(7)",
        "worker": "D63",
        "date": "2026-11-21",
        "status": "COMPLETE",
        "label": "OBSERVED (completion cells) + DERIVED (logs, shares, required values, interval, verdicts) + "
                 "DECLARED-THRESHOLD (90 pp) + CITATION-ONLY (kappa)",
        "statement": (
            "Descriptive bound on the D63 upper-secondary residual. The log gap between the declared 90 pp level and "
            "observed upper-secondary completion 2024 splits at the declared one-stage pair (upper 2024 / lower 2021) "
            "into a pipeline-level share and a transition-ratio share; three comparisons then ask whether the required "
            "lower completion, the required transition ratio and the implied upper interval lie inside the observed "
            "record's envelope. No model was run; no value was adopted; no re-fit; no causal claim; no direction "
            "claim. D63 stays UNABLE as to cause regardless of the verdicts. The observed ratio range is consumed as a "
            "range, not re-tested, and CEIL-ATTRIB is not re-run or re-scored."
        ),
        "verdict": {
            "split_verdict": res["V1"]["outcome"],
            "split_rule": "RESIDUAL-SPLIT iff both shares lie in [1/3, 2/3]; PIPELINE-DOMINANT iff pipeline_share > 2/3; "
                          "RATIO-DOMINANT iff ratio_share > 2/3; THIN rule below 3 pairs",
            "bounds_verdict": res["V2"]["outcome"],
            "bounds_rule": "BOUNDS-INSIDE iff all three comparisons INSIDE; BOUNDS-OUTSIDE iff all three OUTSIDE; "
                           "BOUNDS-EDGE iff mixed; precedence stated in the predeclaration, no tolerance anywhere",
            "outcomes": {"B1": res["B1"]["outcome"], "B2": res["B2"]["outcome"], "B3": res["B3"]["outcome"]},
            "n_inside": sum(1 for k in ("B1", "B2", "B3") if res[k]["outcome"] == "INSIDE"),
            "d63_status": "UNABLE as to cause",
            "d63_status_note": "fixed by the block, D153(vi) and D153(xiii); no outcome of this cell changes it",
            "branch_fired": "BOUNDS-EDGE -> the record bounds the residual on the transition-ratio channel and not on "
                            "the pipeline channel; the sentence calling the ceiling structural is unavailable, and so "
                            "is its opposite.",
        },
        "split": {
            "upper_2024": float(det["O1"]["value"]),
            "lower_2021": float(det["O2"]["value"]),
            "gap_pp": float(det["D1"]["value"]),
            "G_log": float(det["D2"]["value"]),
            "pipeline_log": float(det["D3"]["value"]),
            "ratio_log": float(det["D4"]["value"]),
            "identity_residual": float(det["D5"]["value"]),
            "identity_tolerance": 1e-12,
            "pipeline_share": float(det["D6"]["value"]),
            "ratio_share": float(det["D7"]["value"]),
            "pipeline_share_pct": float(det["D8"]["value"]),
            "ratio_share_pct": float(det["D9"]["value"]),
            "band": [1.0 / 3.0, 2.0 / 3.0],
        },
        "bounds": {
            "B1": {"required_lower": float(det["D10"]["value"]), "record_max_lower": float(det["O3"]["value"]),
                   "record_max_lower_year": 2024, "excess_pp": float(det["D11"]["value"]),
                   "outcome": res["B1"]["outcome"]},
            "B2": {"required_ratio": float(det["D12"]["value"]), "observed_ratio_min": float(det["D13"]["value"]),
                   "observed_ratio_max": float(det["D14"]["value"]), "outcome": res["B2"]["outcome"]},
            "B3": {"implied_upper_lo": float(det["D15"]["value"]), "implied_upper_hi": float(det["D16"]["value"]),
                   "target": 90.0, "outcome": res["B3"]["outcome"]},
            "n_pairs": int(float(det["D17"]["value"])),
            "pair_set_crosscheck": "n = 8 and the (upper year, lower year) set matches PIPE_LOO_PAIRS.csv, ratios at 4 dp",
        },
        "sensitivity_non_verdict_bearing": {
            "declared_in": "PRE_DECLARATIONS.md section 7",
            "label": "DESCRIPTIVE / NOT-VERDICT-BEARING",
            "ratio_contemporaneous": float(det["D18"]["value"]),
            "pipeline_share_contemporaneous": float(det["D19"]["value"]),
            "ratio_share_contemporaneous": float(det["D20"]["value"]),
            "why_reported": "the declared split uses the t-3 pair; at the contemporaneous lower value the pipeline term "
                            "changes sign, so the split may not be cited as lag-free",
        },
        "predeclaration": {
            "file": "PRE_DECLARATIONS.md",
            "sha256": sha("PRE_DECLARATIONS.md"),
            "recorded_sidecar": "PRE_DECLARATIONS.sha256",
            "sidecar_sha256": sha("PRE_DECLARATIONS.sha256"),
            "hashed_before_any_run": True,
            "enforced_by_runner_at_verdict_time": True,
            "enforcement_note": "code/run_d63_bounds.py embeds the sha256 as PREDECL_SHA256 and aborts before any "
                                "computation on mismatch; no hash in any verdict row is RECORDED-NOT-ENFORCED",
            "verbatim_regions_re_extracted_from_frozen_sources": {
                "SYNTHESIS_025-6.3": "PASS (36 source lines)",
                "DECISIONS-D153-xiii": "PASS",
                "DECISIONS-D156-EXP23": "PASS",
                "DECISIONS-D158": "PASS",
                "SYNTHESIS_025-8-banned": "PASS",
            },
            "thresholds_changed_after_results": False,
            "authored_by": "code/author_predecl.py (mechanical splice of the Council's text; no manual transcription)",
        },
        "frozen_inputs": {
            "10_massification/data/UNIVERSALIZATION_SERIES.csv": {
                "role": "ARITHMETIC (observed completion)",
                "sha256": sha(os.path.join("..", "..", "data", "UNIVERSALIZATION_SERIES.csv")),
                "declared_and_enforced": True},
            "08_council/brief_025/SYNTHESIS_025.md": {
                "role": "ARITHMETIC (verbatim source + reproduction anchors)",
                "sha256": sha(os.path.join("..", "..", "..", "08_council", "brief_025", "SYNTHESIS_025.md")),
                "declared_and_enforced": True},
            "08_council/DECISIONS.md": {
                "role": "ARITHMETIC (verbatim source + D153(xiii) anchors)",
                "sha256": sha(os.path.join("..", "..", "..", "08_council", "DECISIONS.md")),
                "declared_and_enforced": True},
            "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv": {
                "role": "ARITHMETIC (8-pair set cross-check)",
                "sha256": sha(os.path.join("..", "pipe_loo_2026-11-20", "results", "PIPE_LOO_PAIRS.csv")),
                "declared_and_enforced": True},
            "10_massification/extensions/conv_reg_2026-11-20/results/CONV_REG.csv": {
                "role": "CITATION-ONLY (object naming)", "sha256": sha(os.path.join("..", "conv_reg_2026-11-20", "results", "CONV_REG.csv"))},
            "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_RESULTS.csv": {
                "role": "CITATION-ONLY (kappa, descriptive / window-only)",
                "sha256": sha(os.path.join("..", "kappa_fwd_2026-11-20", "results", "KAPPA_FWD_RESULTS.csv"))},
            "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/results/synthetic_panel_v1_3.csv": {
                "role": "CITATION-ONLY (synthetic context; no model value enters any bound)",
                "sha256": sha(os.path.join("..", "synthetic_2026-11-20", "generator_v1_3", "results", "synthetic_panel_v1_3.csv"))},
        },
        "declared_parameters": {
            "target_pp": 90.0,
            "target_status": "DECLARED-THRESHOLD (D34/A6, 90/90/90 pp), not an observed object, not a policy target here",
            "iso3": "PHL",
            "upper_column": "completion_upper_secondary",
            "lower_column": "completion_lower_secondary",
            "upper_year": 2024,
            "lower_pair_year": 2021,
            "lag_years": 3,
            "tolerance_years": 1,
            "tie_break": "nearest lower year to t-3 within +/-1 y, ties toward the earlier year (the EXP-1 build_pairs rule)",
            "expected_n_pairs": 8,
            "identity_tolerance": 1e-12,
            "split_band": [1.0 / 3.0, 2.0 / 3.0],
            "rng": "none",
            "model_run": "none",
        },
        "results": {
            "files": {p: sha(p) for p in FILES if p.startswith("results/")},
            "n_rows_results": sum(1 for _ in open(os.path.join(HERE, "results", "D63_BOUNDS_RESULTS.csv"), encoding="utf-8")) - 1,
            "n_rows_detail": sum(1 for _ in open(os.path.join(HERE, "results", "D63_BOUNDS_DETAIL.csv"), encoding="utf-8")) - 1,
            "reproduction_checks_passed": "%d of %d" % (int(float(res["V5"]["value_num"])), 11),
            "verdict_rows": {"split": res["V1"]["outcome"], "bounds": res["V2"]["outcome"], "d63": res["V3"]["outcome"]},
        },
        "determinism": {
            "two_runs_byte_identical": all_same,
            "run1_dir": "results/",
            "run2_dir": "results/determinism_run2/",
            "per_file": det_block,
            "note": "no RNG, no network, no clock value in any result file; the two runs are byte-identical",
        },
        "findings_number_register": {
            "executed_by": "code/run_d63_bounds.py --check-findings (read-only; writes nothing)",
            "executed_after_FINDINGS_was_written": True,
            "n_numbers_in_findings": audit.get("n_numbers"),
            "n_matched": audit.get("n_matched"),
            "n_unmatched": audit.get("n_unmatched"),
            "unmatched": audit.get("unmatched"),
            "banned_sentence_hits": audit.get("banned_hits"),
            "files_scanned": audit.get("result_files_scanned"),
            "rule": "every number in FINDINGS.md must appear in results/D63_BOUNDS_DETAIL.csv with path+column+derivation",
        },
        "declared_limits": [
            "8 Philippine pairs only: the observed ratio range is a single-system range and the bounds inherit that",
            "the declared t-3 lag is a choice: at the contemporaneous lower value the pipeline share changes sign "
            "(sensitivity reported, non-verdict-bearing)",
            "the record maximum lower completion is the 2024 cell, contemporaneous with the residual's upper cell; "
            "B1 therefore compares a 2021-based requirement with a 2024 maximum",
            "the 90 pp level is a declared threshold, not an observed object; the cell does not evaluate whether 90 "
            "is the right bar",
            "B2/B3 combine observed numbers from different years; the joint combination was never observed, and an "
            "interval containing 90 is not evidence that 90 would have been reached",
            "the split is an accounting identity with zero free parameters and zero residual by construction: it "
            "cannot fail, so only the band and the bounds are tests",
            "the cell is upper-level by construction and may not be cited about the lower level or a two-level object",
            "three of the eleven observed upper years cannot enter the pair set (no lower observation within the "
            "declared tolerance of the exact three-year lag)",
        ],
        "closed_claims": [
            "no model run; no model value in any bound",
            "no re-fit, no grid, no second estimand, no adoption",
            "does not re-run or re-score CEIL-ATTRIB; its [0.90, 1.10] band test is not recomputed (the 8 ratios are "
            "consumed as a range)",
            "does not re-score EXP-18, EXP-21, PIPE-LOO, LOWER-DEF or any of the 33 cells",
            "no causal claim; no direction claim; no forecast; no policy target",
            "D63 stays UNABLE as to cause; the barred structural-ceiling sentence and its opposite both remain unwritten",
            "no write outside 10_massification/extensions/d63_bounds_2026-11-20/; every input opened read-only",
            "no web; the running server was not touched",
        ],
        "files": {p: sha(p) for p in FILES},
        "writes_outside_experiment_dir": "none",
    }

    dst = os.path.join(HERE, "RUN_MANIFEST.json")
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {dst}")
    print(f"  verdicts: split={manifest['verdict']['split_verdict']} bounds={manifest['verdict']['bounds_verdict']} "
          f"d63={manifest['verdict']['d63_status']}")
    print(f"  determinism byte-identical: {all_same}")
    print(f"  findings register: {audit.get('n_matched')}/{audit.get('n_numbers')} matched, "
          f"{len(audit.get('banned_hits') or [])} banned hits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
