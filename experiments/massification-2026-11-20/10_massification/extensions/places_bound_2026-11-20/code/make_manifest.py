#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build RUN_MANIFEST.json and SHA256SUMS.txt for EXP-19 PLACES-BOUND.

Deterministic: no clock, no RNG, no network, sorted keys, sorted checksum list.
Every reported value is read back from results/PLACES_BOUND_RESULTS.csv (never re-typed),
so the manifest cannot drift from the delivered artefacts (D113a discipline).

Usage:  python3 code/make_manifest.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform

EXPERIMENT = "EXP-19 PLACES-BOUND"
WORKER = "PB"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_programme_root(start: str) -> str:
    d = os.path.abspath(start)
    for _ in range(10):
        if os.path.isfile(os.path.join(d, "08_council", "DECISIONS.md")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("programme root not found above %s" % start)


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    expdir = os.path.dirname(here)
    prog = find_programme_root(expdir)

    res_path = os.path.join(expdir, "results", "PLACES_BOUND_RESULTS.csv")
    det_path = os.path.join(expdir, "results", "PLACES_BOUND_DETAIL.csv")
    for p in (res_path, det_path):
        if not os.path.isfile(p):
            raise SystemExit("missing result file: %s (run code/run_places_bound.py first)" % p)

    with open(res_path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    idx = {(r["record_type"], r["item"]): r["value"] for r in rows}
    notes = {(r["record_type"], r["item"]): r["note"] for r in rows}

    def raw(rec, item):
        return idx.get((rec, item), "")

    predecl = os.path.join(expdir, "PRE_DECLARATIONS.md")
    predecl_sha = sha256_file(predecl)

    # code hashes
    code = {}
    for name, entry in (("run_places_bound.py", "code/run_places_bound.py"),
                        ("make_manifest.py", "code/make_manifest.py")):
        p = os.path.join(expdir, entry)
        code[name] = {"path": entry, "bytes": os.path.getsize(p), "sha256": sha256_file(p)}

    # determinism: compare the five files between results/ and results/determinism_run2/
    det_files = {}
    for name in ("PLACES_BOUND_RESULTS.csv", "PLACES_BOUND_DETAIL.csv", "PROXY_DISTORTION.md",
                 "INPUT_HASHES.json", "console.txt"):
        a = os.path.join(expdir, "results", name)
        b = os.path.join(expdir, "results", "determinism_run2", name)
        ha = sha256_file(a) if os.path.isfile(a) else None
        hb = sha256_file(b) if os.path.isfile(b) else None
        det_files[name] = {"run1_sha256": ha, "run2_sha256": hb,
                           "byte_identical": bool(ha is not None and ha == hb)}

    # all output files, sorted, for SHA256SUMS (excluding the checksum file itself)
    files = []
    for root, dirs, fnames in os.walk(expdir):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for fn in sorted(fnames):
            if fn in ("SHA256SUMS.txt", "RUN_MANIFEST.json") or fn.endswith(".pyc"):
                continue
            full = os.path.join(root, fn)
            relp = os.path.relpath(full, expdir).replace(os.sep, "/")
            files.append({"path": relp, "bytes": os.path.getsize(full), "sha256": sha256_file(full)})
    files.sort(key=lambda x: x["path"])

    manifest = {
        "experiment": EXPERIMENT,
        "worker": WORKER,
        "status": "delivered",
        "authority": {
            "brief": "08_council/brief_024/SYNTHESIS_024.md section 5.4 (verbatim in PRE_DECLARATIONS.md section 1)",
            "decision": "D145 #4 (rank #4); D146 (coverage/data ruling); D147 (authoring rules); D148 (EXP-17 required state)",
            "rank": 4,
            "sequencing": "after EXP-17 (D145/D148); dependency satisfied",
        },
        "predeclaration": {
            "path": "PRE_DECLARATIONS.md",
            "sha256": predecl_sha,
            "sha256_file": "PRE_DECLARATIONS.sha256",
            "frozen_before_execution": True,
            "freeze_check": raw("meta", "freeze_check"),
        },
        "verdict": {
            "label": raw("verdict", "verdict"),
            "reason": notes.get(("verdict", "verdict"), ""),
            "precedence": raw("verdict", "precedence"),
            "identification_gate": raw("identification", "identification_gate_G"),
            "exact_cells_2018": raw("identification", "exact_cells_2018"),
            "exact_cells_2021": raw("identification", "exact_cells_2021"),
            "norms_inside": raw("comparison", "norms_inside"),
            "norms_outside": raw("comparison", "norms_outside"),
            "norms_straddle": raw("comparison", "norms_straddle"),
            "headline_counterfactual_non_verdict_bearing": raw("comparison", "headline_counterfactual"),
            "adoption": raw("verdict", "adoption"),
        },
        "required_state_derived": {
            "required_coverage_2018": raw("required_state", "required_coverage_2018"),
            "required_coverage_2021": raw("required_state", "required_coverage_2021"),
            "required_target": raw("required_state", "required_target"),
            "lambda_star": raw("required_state", "lambda_star"),
            "source": raw("required_state", "required_state_source"),
            "label": "DERIVED; REQUIRED-STATE (EXP-17); NOT adopted",
        },
        "declared_norms": {
            "values": [40, 45, 50],
            "adopted": 0,
            "label": "DECLARED",
        },
        "implied_capacity_derived": {
            "coverage_2018_n40": raw("implied_capacity", "coverage_2018_n40"),
            "coverage_2018_n45": raw("implied_capacity", "coverage_2018_n45"),
            "coverage_2018_n50": raw("implied_capacity", "coverage_2018_n50"),
            "coverage_2021_n40": raw("implied_capacity", "coverage_2021_n40"),
            "coverage_2021_n45": raw("implied_capacity", "coverage_2021_n45"),
            "coverage_2021_n50": raw("implied_capacity", "coverage_2021_n50"),
        },
        "intervals_derived": {
            "n40": raw("coverage_interval", "interval_n40"),
            "n45": raw("coverage_interval", "interval_n45"),
            "n50": raw("coverage_interval", "interval_n50"),
        },
        "identification": {
            "jhs_ratio_years": raw("identification", "jhs_ratio_years"),
            "ger_lower_secondary_last_year": raw("observed_input", "ger_lower_secondary_last_year"),
            "jhs_ger_lower_year_intersection": raw("identification", "jhs_ger_lower_year_intersection"),
            "reason": raw("identification", "identification_reason"),
        },
        "code": {
            "deterministic": True,
            "rng": "none",
            "network": "none",
            "clock_in_outputs": False,
            "environment": {"implementation": "CPython", "python": platform.python_version()},
            "runner": {"entry_point": "code/run_places_bound.py --outdir results", **code["run_places_bound.py"]},
            "manifest_builder": {"entry_point": "code/make_manifest.py", **code["make_manifest.py"]},
        },
        "inputs": [
            {"path": "10_massification/data/SCHOOL_EXPANSION.csv",
             "sha256": sha256_file(os.path.join(prog, "10_massification/data/SCHOOL_EXPANSION.csv"))},
            {"path": "10_massification/data/STATE_CAPACITY.csv",
             "sha256": sha256_file(os.path.join(prog, "10_massification/data/STATE_CAPACITY.csv"))},
            {"path": "10_massification/data/UNIVERSALIZATION_SERIES.csv",
             "sha256": sha256_file(os.path.join(prog, "10_massification/data/UNIVERSALIZATION_SERIES.csv"))},
            {"path": "10_massification/extensions/joint_cover_2026-11-20/results/JOINT_COVER_RESULTS.csv",
             "sha256": sha256_file(os.path.join(
                 prog, "10_massification/extensions/joint_cover_2026-11-20/results/JOINT_COVER_RESULTS.csv"))},
            {"path": "08_council/brief_024/SYNTHESIS_024.md",
             "sha256": sha256_file(os.path.join(prog, "08_council/brief_024/SYNTHESIS_024.md"))},
            {"path": "08_council/DECISIONS.md",
             "sha256": sha256_file(os.path.join(prog, "08_council/DECISIONS.md"))},
        ],
        "determinism": {
            "method": "sha256 per file between results/ and results/determinism_run2/ (two independent executions)",
            "files": det_files,
            "result": ("byte-identical in all five output files"
                       if all(v["byte_identical"] for v in det_files.values())
                       else "NOT byte-identical in at least one output file"),
        },
        "labels": {
            "observed": "on-disk ratio / enrolment / backlog / flow values",
            "derived": "required state, implied coverage, intervals, comparisons, verdict",
            "declared": "norm class sizes, conversion assumptions, matching rules, verdict precedence",
            "held": "D135/D146 data not on disk and not used",
            "synthetic": "only inside the imported EXP-17 required state's provenance; not used as an observed value",
        },
        "closed_claims": [k for k in (
            "no_phys_cap_change", "no_re_fit", "no_fabrication", "no_proxy_outside_family",
            "no_causal_claim", "no_direction_claim", "no_level_bar", "adopt_nothing")
            if raw("closed_claim", k) == "TRUE"],
        "held_used": "NONE",
        "adoption": "NONE",
        "notes": [
            "D146 stands: the places object is not on disk as a count; the class-size/PTR record is a description.",
            "The proxy is DERIVED and its distortions are stated in results/PROXY_DISTORTION.md; nothing is adopted.",
            "PROXY-SILENT closes the proxy route; the HELD places ask remains HELD.",
        ],
        "files": files,
    }

    manifest_path = os.path.join(expdir, "RUN_MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")

    # SHA256SUMS over every delivered file except the checksum file itself
    lines = []
    files2 = []
    for root, dirs, fnames in os.walk(expdir):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for fn in sorted(fnames):
            if fn == "SHA256SUMS.txt" or fn.endswith(".pyc"):
                continue
            full = os.path.join(root, fn)
            relp = os.path.relpath(full, expdir).replace(os.sep, "/")
            files2.append((relp, sha256_file(full)))
    files2.sort(key=lambda x: x[0])
    for relp, h in files2:
        lines.append("%s  %s" % (h, relp))
    with open(os.path.join(expdir, "SHA256SUMS.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("wrote RUN_MANIFEST.json (%d files) and SHA256SUMS.txt (%d lines)" % (len(files), len(lines)))
    print("verdict: %s" % manifest["verdict"]["label"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
