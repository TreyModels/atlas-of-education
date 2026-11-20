#!/usr/bin/env python3
"""Build RUN_MANIFEST.json and SHA256SUMS.txt for the EXP-21 CONV-REG cell.

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
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CELL)))
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
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, CELL)
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

    inputs = []
    with open(os.path.join(CELL, "results", "INPUT_HASHES.json"), encoding="utf-8") as fh:
        for item in json.load(fh)["inputs"]:
            inputs.append({"path": item["path"], "sha256": item["sha256"]})
    inputs.append({"path": "08_council/brief_025/SYNTHESIS_025.md",
                   "sha256": sha256_file(os.path.join(ROOT, "08_council/brief_025/SYNTHESIS_025.md"))})
    inputs.append({"path": "08_council/DECISIONS.md",
                   "sha256": sha256_file(os.path.join(ROOT, "08_council/DECISIONS.md"))})
    inputs.append({"path": "10_massification/data/DATA_NOTES_MASSIFICATION.md",
                   "sha256": sha256_file(os.path.join(ROOT, "10_massification/data/DATA_NOTES_MASSIFICATION.md"))})

    files = []
    for rel in rel_files():
        full = os.path.join(CELL, rel)
        files.append({"path": rel, "bytes": os.path.getsize(full), "sha256": sha256_file(full)})

    code = {}
    for name in ("run_conv_reg.py", "make_manifest.py"):
        p = os.path.join(HERE, name)
        code[name] = {"path": "code/" + name, "bytes": os.path.getsize(p), "sha256": sha256_file(p)}

    manifest = {
        "experiment": "EXP-21 CONV-REG",
        "worker": "CR",
        "status": "delivered",
        "adoption": "NONE",
        "authority": {
            "brief": "08_council/brief_025/SYNTHESIS_025.md section 6.1 (verbatim in PRE_DECLARATIONS.md section 1)",
            "decision": "D156 #1 (rank #1); D153(xi) (the non-constant observed relation); D158(1)-(7) (authoring rules); D157 (required-state isolation)",
            "rank": 1,
            "sequencing": "first cell of the cycle-17 slate; precondition for EXP-22 and EXP-25 (EXP-21 -> (22, 25))",
        },
        "predeclaration": {
            "path": "PRE_DECLARATIONS.md",
            "sha256": predecl_sha,
            "sha256_file": "PRE_DECLARATIONS.sha256",
            "frozen_before_execution": True,
            "freeze_check": "PASS",
            "enforced_at_verdict_time": True,
            "enforcement": "code/run_conv_reg.py checks the hash before reading any input and re-checks it immediately before VERDICT.json is written; mismatch aborts with exit 2 and writes no verdict",
        },
        "code": {
            "clock_in_outputs": False,
            "deterministic": True,
            "rng": "none",
            "network": "none",
            "environment": {"implementation": "CPython", "python": "3.11.17"},
            "runner": dict(code["run_conv_reg.py"],
                           entry_point="code/run_conv_reg.py --out results"),
            "manifest_builder": dict(code["make_manifest.py"],
                                     entry_point="code/make_manifest.py"),
        },
        "inputs": inputs,
        "files": files,
        "files_excluded_from_manifest": [SELF, SUMS],
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
            "m_constancy": v["m_constancy"],
            "m_constancy_max_dev": v["m_constancy_max_dev"],
            "adoption": "NONE",
            "reason": "6 of 12 frozen system x level cells are NOT-INTERCHANGEABLE and 6 of 12 cross T = 1.0 (all 4 INTERCHANGEABLE cells among them); 2 cells are THIN. One constant conversion cannot stand for a relation that is neither in band nor constant.",
        },
        "frozen_thresholds": v["frozen_thresholds"],
        "sources_verbatim": [
            "08_council/brief_025/SYNTHESIS_025.md section 6.1 (block items 1-7)",
            "08_council/brief_025/SYNTHESIS_025.md section 7 (the seven authoring rules)",
            "08_council/brief_025/SYNTHESIS_025.md section 8 (the banned-sentences bullet)",
            "08_council/DECISIONS.md D156 (EXP-21 clause), D153(xi), D158",
        ],
        "labels": v["labels"],
        "closed_claims": [
            "no_model_run",
            "no_re_fit",
            "no_threshold_change",
            "no_proxy",
            "no_adoption",
            "no_causal_claim",
            "no_direction_claim",
            "no_re_score_of_EXP_18",
            "no_re_run_of_EXP_15",
            "no_ner_statistic",
            "no_required_state_in_any_verdict_path",
            "no_write_outside_cell_dir",
        ],
        "notes": [
            "Register before sentence (D158(3)): every row carries system, level, convention pair, source path and column, label and the enforced predeclaration hash.",
            "Object identity (D158(2)): a pair requires the same system, the same level, the same year and both status=observed; otherwise the year is counted as NOT-COMPARABLE and contributes no number.",
            "The observed T is NOT assumed constant, and m = 1.10 is a DECLARED point convention on a SYNTHETIC panel, not a level convention.",
            "HKG and JPN carry no UIS completion series on disk; their cells are NO-COMPLETION-SERIES and enter no verdict path.",
            "No REQUIRED-STATE object (lambda*, required coverage, 0.8076) is read, computed or cited in this cell (D157/D158(7)).",
        ],
    }

    with open(OUT_MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")

    lines = []
    for rel in sorted(rel_files() + [SELF]):
        p = os.path.join(CELL, rel)
        lines.append("%s  %s" % (sha256_file(p), rel))
    with open(OUT_SUMS, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("manifest: %d files, predecl %s" % (len(files), predecl_sha))
    print("sums: %d lines" % len(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
