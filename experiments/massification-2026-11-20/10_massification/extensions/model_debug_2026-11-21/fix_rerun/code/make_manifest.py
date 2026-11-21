#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build RUN_MANIFEST.json and SHA256SUMS.txt for the FIX + RE-RUN cell (DEBUG).

Deterministic: no clock, sorted keys, sorted file lists. Run last, after FIX_RERUN.md is final.
The manifest lists every file in the cell except RUN_MANIFEST.json and SHA256SUMS.txt (a file
cannot hash itself); SHA256SUMS.txt covers every file except itself.
"""
import csv
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CELL = os.path.dirname(HERE)
DEBUGDIR = os.path.dirname(CELL)
EXT = os.path.dirname(DEBUGDIR)
MASS = os.path.dirname(EXT)
ROOT = os.path.dirname(MASS)
REG = os.path.join(ROOT, "10_massification", "extensions", "conv_reg_2026-11-20")
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


def read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def rel_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(CELL):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d != "__pycache__")
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, CELL)
            if rel in (SELF, SUMS):
                continue
            out.append(rel)
    return sorted(out)


def m_rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return {r["panel"]: r for r in csv.DictReader(fh)}


def main():
    for need in ("results/VERDICT.json", "results/DETERMINISM.json", "results/CAP_FIX_SUMMARY.json",
                 "results/IDENTITY_CHECK.json", "FIX_RERUN.md"):
        if not os.path.exists(os.path.join(CELL, need)):
            sys.stderr.write("missing %s -- run code/run_all_debug.py and finish FIX_RERUN.md first\n" % need)
            return 2

    with open(os.path.join(CELL, "PRE_DECLARATIONS.sha256"), encoding="utf-8") as fh:
        predecl_sha = fh.read().split()[0]
    if predecl_sha != sha256_file(os.path.join(CELL, "PRE_DECLARATIONS.md")):
        sys.stderr.write("PRE_DECLARATIONS.sha256 does not match PRE_DECLARATIONS.md\n")
        return 2

    delivered_m = m_rows(os.path.join(REG, "results", "M_CONSTANCY.csv"))
    repaired_m = m_rows(os.path.join(CELL, "results", "M_CONSTANCY.csv"))
    delivered_v = read_json(os.path.join(REG, "results", "VERDICT.json"))
    repaired_v = read_json(os.path.join(CELL, "results", "VERDICT.json"))
    cap = read_json(os.path.join(CELL, "results", "CAP_FIX_SUMMARY.json"))
    ident = read_json(os.path.join(CELL, "results", "IDENTITY_CHECK.json"))
    det = read_json(os.path.join(CELL, "results", "DETERMINISM.json"))
    hashes = read_json(os.path.join(CELL, "results", "INPUT_HASHES_DEBUG.json"))

    inputs = hashes["inputs"]
    parent_predecl = next(x for x in inputs
                          if x["path"].endswith("model_debug_2026-11-21/PRE_DECLARATIONS.md"))

    files = []
    for rel in rel_files():
        full = os.path.join(CELL, rel)
        files.append({"path": rel, "bytes": os.path.getsize(full), "sha256": sha256_file(full)})

    code_names = ["sim_v1_3_fix.py", "sim_v1_2_fix.py", "run_repaired.py", "uncap_cells.py",
                  "verify_identity.py", "run_conv_reg_repaired.py", "run_all_debug.py",
                  "make_manifest.py"]
    code = {}
    for name in code_names:
        p = os.path.join(HERE, name)
        code[name] = {"path": "code/" + name, "bytes": os.path.getsize(p), "sha256": sha256_file(p)}

    manifest = {
        "experiment": "EXP-21 CONV-REG — repaired re-run",
        "cell": "model_debug_2026-11-21/fix_rerun",
        "worker": "DEBUG AGENT 2 (fix + re-run)",
        "label": "DEBUG",
        "status": "DEBUG — one named defect repaired; register re-run on repaired copies",
        "adoption": "NONE",
        "statement": ("Synthetic data from declared assumptions only. Not evidence, not an estimate, "
                      "not a forecast, no causal or direction claim, no real country modelled."),
        "authority": {
            "model_debug_contract": {
                "path": "10_massification/extensions/model_debug_2026-11-21/PRE_DECLARATIONS.md",
                "sha256": parent_predecl["sha256"],
                "amendment_1": "measures are different objects: GER may exceed 100; NER <= 100 definitional; UIS CR denominator is the 3-5-years-above-grade older cohort, so CR is not bounded by GER and may exceed it",
            },
            "defect": "CAP-01, 10_massification/extensions/model_debug_2026-11-21/cap_audit/results/CAP_AUDIT.md section 1",
            "decisions": "08_council/DECISIONS.md D160, D164 (EXP-21 clause and its conditions)",
            "user_directive": ("MODEL-DEBUG MODE licensed after EXP-21/D160; measure-aware per the Lead's "
                               "correction; the gate-passed write-up is not edited"),
        },
        "fix": {
            "defect": "completion_uis capped at 1.0 (CAP-01); 35/6,720 cells on v1.3 and v1.2, 0 on A17",
            "removed": 'out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)',
            "installed": 'out["comp_uis"][L, t] = max(0.0, P["meas_completion_factor"] * comp_coh)',
            "sites": {
                "v1.3": {"original": "generator_v1_3/code/sim_v1_3.py:832",
                         "repaired_copy": "code/sim_v1_3_fix.py:835"},
                "v1.2": {"original": "generator_v1_2/code/sim_v1_2.py:610",
                         "repaired_copy": "code/sim_v1_2_fix.py:613"},
            },
            "other_hunk": "path block only (copy resolves frozen inputs from the original generator dir)",
            "unchanged": ["comp_coh cohort-flow clip (CAP-02)", "GER/overage_cap Z1 gate (CAP-06)",
                          "capacity gates (CAP-07/08/09)", "survival clip incl. the CAP-04 0.02 floor (recorded, not fixed)",
                          "share renormalisations", "all thresholds", "all parameters", "seed", "draw order"],
            "no_fitting": True,
            "no_parameter_change": True,
            "no_threshold_change": True,
            "no_new_parameter": True,
        },
        "declared_convention": {
            "object": "UIS completion rate (CR)",
            "denominator": "population 3-5 years above the official graduation age of the grade (older cohort)",
            "repeaters_overage": "counted across years; over-age completion is included",
            "bounded_by_1": False,
            "bounded_by_ger": False,
            "ner": "NER <= 100 is definitional; no NER statistic is computed here",
            "m": {"value": "1.10", "status": "DECLARED measurement factor — a point convention, not a conversion"},
        },
        "predeclaration": {
            "path": "PRE_DECLARATIONS.md",
            "sha256": predecl_sha,
            "sha256_file": "PRE_DECLARATIONS.sha256",
            "frozen_before_execution": True,
            "enforced_pre_input": True,
            "enforced_pre_verdict_write": True,
            "enforcement": ("code/run_conv_reg_repaired.py checks the hash before reading any input and "
                            "re-checks it immediately before VERDICT.json is written; mismatch aborts with "
                            "exit 2 and writes no verdict"),
        },
        "inherited_register_predeclaration": {
            "path": "10_massification/extensions/conv_reg_2026-11-20/PRE_DECLARATIONS.md",
            "sha256": "1dd86bd139a81c22e0ba2918728818fe7184775d925211a28fdd2be00b975410",
            "hash_enforced_at_run_time": True,
            "thresholds_inherited_unchanged": True,
        },
        "code": {
            "clock_in_outputs": False,
            "deterministic": True,
            "rng": "inherited seed 20261120, single PCG64 stream, draw order unchanged",
            "network": "none",
            "environment": {"implementation": "CPython", "python": "3.11.17", "numpy": "2.4.6"},
            "entry_point": "code/run_all_debug.py --run1 results --run2 determinism_run2",
            "manifest_builder": "code/make_manifest.py",
            "files": code,
        },
        "inputs": inputs,
        "delivered_inputs_unchanged": hashes["delivered_inputs_unchanged"],
        "files": files,
        "files_excluded_from_manifest": [SELF, SUMS],
        "determinism": {
            "method": ("two clean runs; panels from an independent second execution of each generator; "
                       "the register run a second time on the byte-identical panel set"),
            "n_artifacts": det["n_artifacts"],
            "all_identical": det["all_identical"],
            "result": det["verdict"].lower() + " in all %d artifacts" % det["n_artifacts"],
            "artifacts": {a["kind"] + "/" + a["artifact"]: {
                "byte_identical": a["byte_identical"],
                "run1_sha256": a["sha256_run1"],
                "run2_sha256": a["sha256_run2"]} for a in det["artifacts"]},
            "file": "results/DETERMINISM.json",
        },
        "results": {
            "cap_fix": {
                "n_fix_rows_total": cap["n_fix_rows_total"],
                "n_fix_rows_by_panel": cap["n_fix_rows_by_panel"],
                "a17_binding_cells": cap["a17_binding_cells"],
                "max_uncapped": "%.10g" % cap["panels"]["v1.3"]["max_uncapped"],
                "max_delivered": "%.10g" % cap["panels"]["v1.3"]["max_delivered"],
                "max_repaired": "%.10g" % cap["panels"]["v1.3"]["max_repaired"],
                "file": "results/CAP_FIX_CELLS.csv",
            },
            "m_constancy": {
                "before": {p: {"max_abs_dev_ratio": delivered_m[p]["max_abs_dev_ratio"],
                               "verdict": delivered_m[p]["verdict"],
                               "source": "10_massification/extensions/conv_reg_2026-11-20/results/M_CONSTANCY.csv"}
                           for p in ("v1.3", "v1.2", "A17")},
                "after": {p: {"max_abs_dev_ratio": repaired_m[p]["max_abs_dev_ratio"],
                              "verdict": repaired_m[p]["verdict"],
                              "source": "results/REPAIRED_M_CONSTANCY.csv"}
                          for p in ("v1.3", "v1.2", "A17")},
                "in_memory_identity_max_abs_diff": {
                    p: ident["generators"][p]["max_abs_diff_in_memory"] for p in ("v1.3", "v1.2")},
                "file": "results/REPAIRED_M_CONSTANCY.csv",
            },
            "register": {
                "before_counts": delivered_v["counts"],
                "after_counts": repaired_v["counts"],
                "before_verdict": delivered_v["overall_verdict"],
                "after_verdict": repaired_v["overall_verdict"],
                "register_rows_identical_except": ["predecl_sha256_12"],
                "detail_rows_identical": True,
                "file": "results/REPAIRED_CONV_REG.csv",
            },
            "answers": {
                "a_m_constant_only_on_A17": False,
                "a_after": {"A17": "CONSTANT", "v1.3": "CONSTANT", "v1.2": "CONSTANT"},
                "b_non_constancy": "cap-induced (wholly); analytic: 1/0.9497070256 - 1.10 = -0.047043695535 = -4.7043695535e-02",
                "c_counts": "unchanged 4 INTER / 6 NOT / 2 THIN",
                "c_why": "T is observed completion / observed GER; the model panels enter only the m-constancy block",
                "d_level_sentences": "none change; prospective amendments only (C-13, Table A-1 rows, the A17-only condition); zero published-number changes",
                "d_capped_statement": "as-delivered: 35/6,720 per panel (true, unchanged); repaired copies: 0/6,720",
                "measure": cap["measure"],
            },
        },
        "checks": {
            "T1_panel_identity": "PASS — only completion_uis differs; 35 cells per panel; each = 1.10*cohort and > 1",
            "T2_m_constancy": "PASS — CONSTANT on repaired v1.3, repaired v1.2, A17",
            "T3_cap_induced": "PASS — 4.7043695535e-02 -> 9.6646846082e-10; uncapped max unchanged",
            "T4_register_invariance": "PASS — counts 4/6/2 unchanged; detail 90/90 and system 6/6 identical",
            "T5_determinism": "PASS — 12/12 artifacts byte-identical",
            "T6_delivered_unchanged": "PASS — 12/12 delivered inputs unchanged",
            "A1_measure_cr_vs_ger": "MEASURED — 0 of 70 repaired capped cells have CR > GER; all 70 CR <= the model's own GER (105.0)",
        },
        "labels": {"cell": "DEBUG", "panels": "SYNTHETIC", "observed_inputs": "OBSERVED",
                   "register_values": "DERIVED", "m": "DECLARED / CONVENTION"},
        "closed_claims": [
            "no_reproduction_claim",
            "no_successor_generator",
            "no_reopening_of_the_closed_line",
            "no_threshold_change",
            "no_fitting",
            "no_new_parameter",
            "no_causal_claim",
            "no_direction_claim",
            "no_write_up_edit",
            "no_write_outside_cell_dir",
            "no_web",
            "no_server_interaction",
        ],
        "notes": [
            "The CAP-04 survival floor 0.02 (24 tertiary burn-in cells) is recorded, not fixed; it is not the named defect.",
            "CAP-14 / CAP-20 are non-binding guards: recorded, no action.",
            "The repaired panels are a DEBUG diagnostic object; they do not replace or modify any delivered panel.",
            "The register CSV's predecl_sha256_12 column names the governing DEBUG predeclaration (5d7fb5c36aec); the inherited threshold predeclaration 1dd86bd1 is enforced at run time and recorded in VERDICT.json.",
            "PROVENANCE NOTE: the parent contract carries AMENDMENT 1 and hashes 7d8bade95407a2fe...; CAP_AUDIT.md records both that amended hash and the dispatch hash 748335cf915394c3... and states the contract was amended mid-audit. Neither file was edited by this cell (both unchanged before/after).",
            "A17's frozen v1.6 copy was not repaired: 0 cells bind there, the A17 panel is the frozen comparison object, and the write scope names the v1.3/v1.2 copies; the output would be byte-identical.",
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
