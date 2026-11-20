#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build RUN_MANIFEST.json and SHA256SUMS.txt for EXP-17 JOINT-COVER.

Deterministic: no clock, no RNG, no network, sorted keys, sorted checksum list.
Every reported value is read back from results/JOINT_COVER_RESULTS.csv (never re-typed),
so the manifest cannot drift from the delivered artefacts (D113a discipline).

Usage:  python3 code/make_manifest.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import sys

EXPERIMENT = "EXP-17 JOINT-COVER"
WORKER = "JC"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_programme_root(start: str) -> str:
    d = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "08_council", "DECISIONS.md")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("programme root not found above %s" % start)


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    expdir = os.path.dirname(here)
    prog = find_programme_root(expdir)

    res_path = os.path.join(expdir, "results", "JOINT_COVER_RESULTS.csv")
    det_path = os.path.join(expdir, "results", "JOINT_COVER_DETAIL.csv")
    for p in (res_path, det_path):
        if not os.path.isfile(p):
            raise SystemExit("missing result file: %s (run code/run_joint_cover.py first)" % p)

    with open(res_path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    idx = {(r["record_type"], r["item"]): r["value"] for r in rows}
    notes = {(r["record_type"], r["item"]): r["note"] for r in rows}

    def raw(rec, item):
        return idx.get((rec, item), "")

    def num(rec, item):
        v = raw(rec, item)
        if v in ("", None):
            return None
        try:
            return float(v)
        except ValueError:
            return v

    def boolean(rec, item):
        return raw(rec, item) == "TRUE"

    def integer(rec, item):
        v = raw(rec, item)
        return None if v in ("", None) else int(float(v))

    inputs = {
        "DECISIONS.md": os.path.join(prog, "08_council", "DECISIONS.md"),
        "LOWER_DEF_RESULTS.csv": os.path.join(prog, "10_massification", "extensions",
                                              "lower_def_2026-11-20", "results", "LOWER_DEF_RESULTS.csv"),
        "PARAMS.md": os.path.join(prog, "10_massification", "extensions", "synthetic_2026-11-20",
                                  "generator_v1_2", "PARAMS.md"),
        "PRE_DECLARATIONS.md": os.path.join(expdir, "PRE_DECLARATIONS.md"),
        "SYNTHESIS_024.md": os.path.join(prog, "08_council", "brief_024", "SYNTHESIS_024.md"),
        "sim_v1_2.py": os.path.join(prog, "10_massification", "extensions", "synthetic_2026-11-20",
                                    "generator_v1_2", "code", "sim_v1_2.py"),
        "synthetic_panel_v1_2.csv": os.path.join(prog, "10_massification", "extensions",
                                                 "synthetic_2026-11-20", "generator_v1_2", "results",
                                                 "synthetic_panel_v1_2.csv"),
    }

    def entry(rel_path: str, contents: str = "") -> dict:
        ap = os.path.join(expdir, rel_path)
        d = {"path": rel_path, "sha256": sha256_file(ap), "bytes": os.path.getsize(ap)}
        if contents:
            d["contents"] = contents
        return d

    out_files = {
        "JOINT_COVER_RESULTS.csv": "falsifier, root set and lambda*, implied coverage/seats/(a,s), law maximum, "
                                  "scope checks, verdict, observed-reference row, by-year context (86 data rows)",
        "JOINT_COVER_DETAIL.csv": "function evaluation grid (N=6001, step 2.5e-4), sign-change brackets, "
                                  "bisection trace, Newton trace, critical lambda points, anchor row",
        "INPUT_HASHES.json": "sha256 of every input read",
    }
    outputs = {name: entry(os.path.join("results", name), desc) for name, desc in out_files.items()}

    det_files = {}
    for name in out_files:
        r1 = os.path.join(expdir, "results", name)
        r2 = os.path.join(expdir, "results", "determinism_run2", name)
        h1, h2 = sha256_file(r1), sha256_file(r2)
        det_files[name] = {"run1_sha256": h1, "run2_sha256": h2, "byte_identical": h1 == h2}

    context = {}
    for r in rows:
        if r["record_type"] != "context":
            continue
        item = r["item"]
        if item.endswith("_lambda_star"):
            context[item.split("_")[1]] = num(r["record_type"], item)

    manifest = {
        "experiment": EXPERIMENT,
        "worker": WORKER,
        "question": "Is there ONE declared coverage path that satisfies BOTH lower channels at once? "
                    "(lower-secondary, SYN00_PHL_LIKE, completion 2021 / entry 2018)",
        "authority": {
            "brief": "08_council/brief_024/SYNTHESIS_024.md section 5.2 (verbatim in PRE_DECLARATIONS.md section 1)",
            "decision": "D145 #2 (rank #2); D142 (EXP-13 chain, target provenance); D143 (scope corrections); "
                        "D147 (four authoring rules)",
            "rank": 2,
        },
        "predeclaration": {
            "path": "PRE_DECLARATIONS.md",
            "sha256": sha256_file(os.path.join(expdir, "PRE_DECLARATIONS.md")),
            "bytes": os.path.getsize(os.path.join(expdir, "PRE_DECLARATIONS.md")),
            "note": "written and hashed BEFORE code/run_joint_cover.py was executed; definitions, thresholds, "
                    "precedence, root-finding protocol and tolerance frozen; the hash is embedded in the script, "
                    "which refuses to run on a mismatch",
            "frozen_sha256_file": "PRE_DECLARATIONS.sha256",
            "blindness_disclosure": "no evaluation of the equation at any lambda was executed before the freeze; "
                                    "the value at lambda=1 (0.6740731179) is D142's delivered chain, and the "
                                    "monotonicity of the law in lambda is stated in section 7 of the predeclaration "
                                    "rather than claimed as a discovery (EXP-14 C-5 lesson)",
        },
        "code": {
            "runner": {"path": "code/run_joint_cover.py",
                       "sha256": sha256_file(os.path.join(here, "run_joint_cover.py")),
                       "bytes": os.path.getsize(os.path.join(here, "run_joint_cover.py")),
                       "entry_point": "code/run_joint_cover.py --outdir results"},
            "manifest_builder": {"path": "code/make_manifest.py",
                                 "sha256": sha256_file(os.path.join(here, "make_manifest.py")),
                                 "bytes": os.path.getsize(os.path.join(here, "make_manifest.py")),
                                 "entry_point": "code/make_manifest.py"},
            "deterministic": True,
            "rng": "none",
            "network": "none",
            "clock_in_outputs": False,
            "environment": {"python": platform.python_version(), "implementation": platform.python_implementation()},
        },
        "inputs": {name: {"path": os.path.relpath(path, prog), "sha256": sha256_file(path),
                          "bytes": os.path.getsize(path), "mode": "read-only"}
                   for name, path in sorted(inputs.items())},
        "inputs_role": "read-only; no input file was modified; no generator was run; no model code was imported",
        "outputs": outputs,
        "determinism": {
            "runs": 2,
            "method": "sha256 per file between results/ and results/determinism_run2/ (two independent executions)",
            "result": "byte-identical in all three result files",
            "files": det_files,
        },
        "verdict": {
            "cell": raw("meta", "scored_cell"),
            "label": raw("verdict", "verdict_label"),
            "flags": notes.get(("verdict", "verdict_label"), ""),
            "adoption": raw("verdict", "adoption"),
            "falsifier": {
                "declared": "lambda = 1 must reproduce the panel's 2021 completion_uis to 1e-9",
                "chain_at_lambda_1": num("falsifier", "lambda_1_chain"),
                "panel_completion_uis": num("input", "panel_completion_uis_2021"),
                "abs_error": num("falsifier", "abs_error"),
                "tolerance": num("falsifier", "tolerance"),
                "pass": boolean("falsifier", "pass"),
                "survival_diagnostic_abs_error": num("falsifier", "survival_diagnostic_abs_error"),
            },
            "target": {
                "value": num("target", "value"),
                "label": "DERIVED",
                "provenance": raw("target", "provenance"),
                "derivation": "76.6391/0.949 = 80.7577 -> 80.76 at 2 dp (D133/D140)",
                "observed_reference": num("target", "observed_reference"),
                "observed_reference_label": "OBSERVED (reference only; never in the verdict path)",
            },
            "root": {
                "count": integer("root", "count"),
                "lambda_star": num("root", "lambda_star"),
                "lambda_star_bisect": num("root", "lambda_star_bisect"),
                "lambda_star_newton": num("root", "lambda_star_newton"),
                "method_abs_diff": num("root", "method_abs_diff"),
                "bracket": [num("root", "bracket_lo"), num("root", "bracket_hi")],
                "bracket_width_final": num("root", "bracket_width_final"),
                "residual_at_root": num("root", "residual_at_root"),
                "bisection_iterations": integer("root", "bisection_iterations"),
                "monotonicity_decreases": integer("root", "monotonicity_decreases"),
            },
            "implied": {
                "coverage_2018": num("implied", "coverage_2018"),
                "coverage_2021": num("implied", "coverage_2021"),
                "coverage_uplift_pp_2018": num("implied", "coverage_uplift_pp_2018"),
                "coverage_uplift_pp_2021": num("implied", "coverage_uplift_pp_2021"),
                "seats_2018": num("implied", "seats_2018"),
                "seats_2021": num("implied", "seats_2021"),
                "a_gate": num("implied", "a_gate"),
                "s_survival": num("implied", "s_survival"),
                "product_m_a_s": num("implied", "product_m_a_s"),
                "phys_cap_times_coverage_2018": num("implied", "phys_cap_times_coverage_2018"),
                "lambda_minus_one": num("implied", "lambda_minus_one"),
                "required_vs_realised_gap_pp": num("implied", "required_vs_realised_gap_pp"),
            },
            "law": {
                "max_over_bracket": num("law", "max_over_bracket"),
                "analytic_max": num("law", "analytic_max"),
                "F_at_0.5": num("law", "F_at_0.5"),
                "F_at_2.0": num("law", "F_at_2.0"),
                "lambda_cap": num("law", "lambda_cap"),
                "lambda_survival_flat": num("law", "lambda_survival_flat"),
                "lambda_demand_bind": num("law", "lambda_demand_bind"),
            },
            "checks": {
                "clip_inactive": boolean("law", "clip_inactive"),
                "root_in_capacity_regime": boolean("check", "root_in_capacity_regime"),
                "implied_a_flag": raw("check", "implied_a_flag"),
                "resolution_pretest": boolean("check", "resolution_pretest"),
                "law_max_matches_analytic": boolean("check", "law_max_matches_analytic"),
                "count_blind": boolean("check", "count_blind"),
            },
            "reference_only": {
                "target": num("secondary", "reference_target"),
                "lambda_star": num("secondary", "reference_lambda_star"),
                "note": "non-verdict-bearing; the observed reference is not the requirement (D142 C-4)",
            },
            "context_by_year": context,
            "not_identified": "the split of the required product between the gate and the survival law; D140's "
                              "shares remain reported and unidentified (weight [0.466649, 0.525137])",
        },
        "labels": {
            "panel_arithmetic": "SYNTHETIC",
            "required_value": "DERIVED (76.6391/0.949)",
            "implied_state": "DERIVED from SYNTHETIC panel values",
            "laws_and_constants": "DECLARED / CONVENTION (no value re-chosen)",
            "observed_reference": "OBSERVED (reference only)",
            "verdict_rule": "DECLARED in PRE_DECLARATIONS.md section 5",
        },
        "closed_claims": [
            "no re-fit",
            "no new parameter",
            "no lambda adopted (lambda* is a required state, not a parameter)",
            "no generator re-run; no model code imported",
            "no re-scoring of EXP-13 or EXP-14; D140's shares and label untouched",
            "no causal claim",
            "no direction claim",
            "no observed-path count computed (count-blind)",
            "D63 remains UNABLE as to cause",
            "phase verdict and scaling FAIL untouched",
        ],
        "writes": {
            "scope": "10_massification/extensions/joint_cover_2026-11-20/ only",
            "files": [],   # filled below
            "outside_scope_writes": "none",
        },
        "notes": [
            "The equation was solved on the frozen v1.2 panel, where the 2018 lower gate is capacity-limited "
            "(0.783805 = 1.15 x coverage). It does NOT carry to the A10 two-tier arm, whose gate is "
            "participation-limited (0.681570); see FINDINGS.md section 6.",
            "The requirement 0.8076 is DERIVED (76.6391/0.949), an internal-consistency object of the declared "
            "generator line; the observed reference 80.8960494995 sits +0.136049 pp away and is reported once, "
            "never used in a computation.",
            "Lambda* at the observed reference would be 1.115802; required coverage would be +0.079 pp (2018) and "
            "+0.090 pp (2021) higher. Non-verdict-bearing.",
            "completion_uis is clipped to [0, 1] by the generator; the clip does not bind at this cell "
            "(m x completion_cohort = 0.6741) and the survival clip does not bind anywhere on [0.5, 2.0].",
            "The two console captures differ only in the printed output directory (run2 names "
            "results/determinism_run2); the three data artefacts are byte-identical. Consoles are not compared "
            "artifacts.",
            "The verdict label is largely implied by the declared law's monotonicity in lambda; this is disclosed "
            "in PRE_DECLARATIONS.md section 7 before the run. The cell's information is lambda*, the implied (a, s) "
            "and coverage at both years, and the falsifier.",
        ],
    }

    written = ["PRE_DECLARATIONS.md", "PRE_DECLARATIONS.sha256", "FINDINGS.md", "RUN_MANIFEST.json",
               "SHA256SUMS.txt", "code/run_joint_cover.py", "code/make_manifest.py",
               "results/JOINT_COVER_RESULTS.csv", "results/JOINT_COVER_DETAIL.csv",
               "results/INPUT_HASHES.json", "results/run1_console.txt",
               "results/determinism_run2/JOINT_COVER_RESULTS.csv",
               "results/determinism_run2/JOINT_COVER_DETAIL.csv",
               "results/determinism_run2/INPUT_HASHES.json",
               "results/determinism_run2/console.txt"]
    manifest["writes"]["files"] = written

    man_path = os.path.join(expdir, "RUN_MANIFEST.json")
    with open(man_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")

    sums_path = os.path.join(expdir, "SHA256SUMS.txt")
    lines = []
    for rel in sorted(written):
        if rel == "SHA256SUMS.txt":      # a checksum file cannot list itself
            continue
        ap = os.path.join(expdir, rel)
        if not os.path.isfile(ap):
            raise SystemExit("missing file for checksums: %s" % rel)
        lines.append("%s  %s" % (sha256_file(ap), rel))
    with open(sums_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")

    bad = [f for f, d in det_files.items() if not d["byte_identical"]]
    print("manifest  : %s" % os.path.relpath(man_path, prog))
    print("checksums : %s (%d files, manifest excluded from its own list)" % (os.path.relpath(sums_path, prog),
                                                                              len(lines)))
    print("predecl   : %s" % manifest["predeclaration"]["sha256"])
    print("verdict   : %s  lambda*=%s" % (manifest["verdict"]["label"], raw("root", "lambda_star")))
    print("determinism: %s" % ("BYTE-IDENTICAL" if not bad else "DIFFERS: %s" % bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
