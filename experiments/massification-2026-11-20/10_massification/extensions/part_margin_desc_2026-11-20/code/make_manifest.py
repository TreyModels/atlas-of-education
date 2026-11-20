#!/usr/bin/env python3
"""Build RUN_MANIFEST.json and SHA256SUMS.txt for the EXP-22 PART-MARGIN-DESC cell.

Deterministic: no clock, sorted keys, sorted file list. Run last, after FINDINGS.md is final.
The manifest lists every file in the cell except RUN_MANIFEST.json and SHA256SUMS.txt (a file cannot
hash itself); SHA256SUMS.txt covers both of those as well.
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CELL = os.path.dirname(HERE)
OUT_MANIFEST = os.path.join(CELL, "RUN_MANIFEST.json")
OUT_SUMS = os.path.join(CELL, "SHA256SUMS.txt")
SELF = "RUN_MANIFEST.json"
SUMS = "SHA256SUMS.txt"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(CELL):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), CELL)
            if rel in (SELF, SUMS):
                continue
            out.append(rel)
    return sorted(out)


def main():
    verdict_path = os.path.join(CELL, "results", "VERDICT.json")
    det_path = os.path.join(CELL, "results", "DETERMINISM.json")
    if not (os.path.exists(verdict_path) and os.path.exists(det_path)):
        sys.stderr.write("run the runner and the determinism comparison first\n")
        return 2
    with open(verdict_path, encoding="utf-8") as fh:
        v = json.load(fh)
    with open(det_path, encoding="utf-8") as fh:
        det = json.load(fh)
    with open(os.path.join(CELL, "PRE_DECLARATIONS.sha256"), encoding="utf-8") as fh:
        predecl_sha = fh.read().split()[0]
    with open(os.path.join(CELL, "results", "INPUT_HASHES.json"), encoding="utf-8") as fh:
        inputs = json.load(fh)["inputs"]

    files = []
    for rel in rel_files():
        files.append({"path": rel, "sha256": sha256_file(os.path.join(CELL, rel)),
                      "bytes": os.path.getsize(os.path.join(CELL, rel))})

    code = {rel: {"sha256": sha256_file(os.path.join(CELL, rel))}
            for rel in ("code/run_part_margin_desc.py", "code/verify_verbatim.py", "code/make_manifest.py")}

    manifest = {
        "cell": "EXP-22 PART-MARGIN-DESC",
        "cycle": "cycle 17 (post-generator descriptive consolidation, D155)",
        "authority": [
            "08_council/brief_025/SYNTHESIS_025.md section 6.2 (block items 1-7, copied verbatim)",
            "08_council/brief_025/SYNTHESIS_025.md section 7 (the seven authoring rules, copied verbatim)",
            "08_council/brief_025/SYNTHESIS_025.md section 8 (the banned-sentences bullet, copied verbatim)",
            "08_council/DECISIONS.md D156 (EXP-22 clause), D153(xii), D158",
            "08_council/brief_025/VERIFICATION_025.csv V35a-V35c (anchors, copied verbatim)",
        ],
        "question": v["question"],
        "predeclaration": {
            "path": "PRE_DECLARATIONS.md",
            "sha256": predecl_sha,
            "enforced_by_runner": True,
            "enforcement": "checked three ways (file, literal, actual) before any input is read and again immediately before VERDICT.json is written",
            "verbatim_checks": v["verbatim_checks"],
        },
        "code": {
            "clock_in_outputs": False,
            "deterministic": True,
            "rng": "none",
            "network": "none",
            "environment": {"implementation": "CPython", "python": "3.11.17"},
            "runner": dict(code["code/run_part_margin_desc.py"],
                           entry_point="code/run_part_margin_desc.py --out results"),
            "verbatim_checker": dict(code["code/verify_verbatim.py"],
                                     entry_point="code/verify_verbatim.py"),
            "manifest_builder": dict(code["code/make_manifest.py"],
                                     entry_point="code/make_manifest.py"),
        },
        "inputs": inputs,
        "files": files,
        "files_excluded_from_manifest": [SELF, SUMS],
        "scope": {
            "system": "PHL",
            "levels": ["primary", "lower_secondary", "upper_secondary"],
            "why_one_system": "the frozen block's anchors (30 / 4 / 2 pairs) are PHL's and the model's placement subject is its PHL row; other systems' ger/ner rows exist on disk but are not computed here (declared, not widened after results)",
        },
        "observed_spans": {
            r["level"]: {
                "n_pairs": r["n_pairs"], "window": [r["pair_year_min"], r["pair_year_max"]],
                "span_min_pp": r["span_min_pp"], "span_min_year": r["span_min_year"],
                "span_max_pp": r["span_max_pp"], "span_max_year": r["span_max_year"],
                "span_median_pp": r["span_median_pp"], "thin": r["thin"],
            } for r in v["per_level"]
        },
        "identity_test": {
            "against": "10_massification/extensions/conv_reg_2026-11-20/results/CONV_REG.csv",
            "register_overall_verdict": v["register"]["overall_verdict"],
            "register_hash_verified_before_use": True,
            "per_level": v["identity_test"],
            "result": "NO-REGISTERED-COUNTERPART at all three levels: the register's only convention family is completion/GER and it carries no demand_share line and no NER line",
        },
        "model_shares": {
            "label": "SYNTHETIC",
            "class_tags": ["v1.6", "v1.7"],
            "year": "2024",
            "v1.6": v["model_shares_placement_subjects"]["v1.6"],
            "v1.7": v["model_shares_placement_subjects"]["v1.7"],
            "match_predecl_expected": v["model_shares_match_predecl_expected"],
            "placement": "WITHHELD-NO-IDENTITY",
            "verdict_bearing": False,
        },
        "determinism": {
            "method": "sha256 per file between results/ and results/determinism_run2/ (two independent executions of the same code on the same inputs)",
            "files": {a["artifact"]: {"byte_identical": a["byte_identical"],
                                      "run1_sha256": a["sha256_run1"],
                                      "run2_sha256": a["sha256_run2"]} for a in det["artifacts"]},
            "result": det["verdict"].lower() + " in all %d artifacts" % det["n_artifacts"],
        },
        "verdict": {
            "label": v["overall_verdict"],
            "precedence": v["precedence"],
            "clause_fired": [t["clause"] for t in v["precedence_trace"] if t["fired"]],
            "counts": v["counts"],
            "adoption": "NONE",
            "reason": "no observed object on disk carries the model's numerator (a choice probability) or denominator (the model's level cohort); EXP-21's register records no such line; the observed gross - net span is in pp and the model share is a cohort fraction, so no comparison is licensed and the placement is withheld.",
        },
        "frozen_thresholds": v["frozen_thresholds"],
        "labels": v["labels"],
        "closed_claims": [
            "no_model_run",
            "no_re_fit",
            "no_parameter_set",
            "no_33_cell_score",
            "no_9_cell_score",
            "no_deviation",
            "no_within_5pp_hit_count",
            "no_crossing_count",
            "no_observed_path_coverage_count",
            "no_cross_source_arithmetic",
            "no_re_score_of_EXP_18",
            "no_proxy",
            "no_adoption",
            "no_causal_claim",
            "no_direction_claim",
            "no_cross_level_margin",
            "no_required_state_in_any_verdict_path",
            "no_web_access",
            "no_server_touch",
            "no_write_outside_cell_dir",
        ],
        "notes": [
            "Object identity before comparison (D158(2)): the identity test runs against EXP-21's register before the observed series and before either model panel is opened; the event order is in results/COUNT_BLIND_AUDIT.json.",
            "The six model values are printed beside the spans for orientation only; comparison_performed = FALSE and cross_source_arithmetic_ops = 0.",
            "THIN rule (<3 pairs) is applied as a flag, not a verdict; upper secondary has 2 pairs and may carry no placement label. V35b's note saying THIN for lower secondary is recorded as a discrepancy and the rule governs (n=4).",
            "D153(xii) writes the span as net - gross (negative); this cell reports the frozen block's ger - ner (positive) and records the notation difference. No verdict rests on the sign.",
            "Every reported number is re-read from its path + column by a fresh traceability pass before the verdict is written; a mismatch aborts rather than producing a label.",
            "The count-blind audit discloses the only plain opens in the cell: sha256 hashing of the declared inputs and writes to the cell's own output directory. Every content read is guarded and allow-listed, and the hash-before-data gate covers the observed series and both model panels.",
        ],
    }

    with open(OUT_MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")

    lines = []
    for rel in sorted([f["path"] for f in files] + [SELF]):
        p = os.path.join(CELL, rel)
        lines.append("%s  %s" % (sha256_file(p), rel))
    with open(OUT_SUMS, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("manifest: %d files, predecl %s" % (len(files), predecl_sha))
    print("sums: %d lines" % len(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
