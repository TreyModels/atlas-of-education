#!/usr/bin/env python3
"""Write RUN_MANIFEST.json and SHA256SUMS.txt for EXP-8 GATE-LOCUS.

Deterministic: no clock, no RNG. Verifies determinism (cmp) and the verbatim predeclaration
before writing, and aborts if either fails.
"""

import hashlib
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
EXP_DIR = HERE.parent
PROGRAMME_ROOT = EXP_DIR.parents[2]
RESULTS = EXP_DIR / "results"

PANEL = (PROGRAMME_ROOT / "10_massification" / "extensions" / "synthetic_2026-11-20"
         / "generator_v1_2" / "results" / "synthetic_panel_v1_2.csv")
GATES = (PROGRAMME_ROOT / "10_massification" / "extensions" / "synthetic_2026-11-20"
         / "generator_v1_3" / "results" / "shadow_gates_v1_3.csv")
BRIEF = PROGRAMME_ROOT / "08_council" / "brief_022" / "SYNTHESIS_022.md"

DECLARED = {
    "panel": "14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac",
    "gates": "df3cab007ce5fbe9a48d58b0701d04e6d762591848ca1517a634c8f897edb351",
    "brief": "9508dd55be8dd64da8322a8277c8342a4f50be6790a3d287e39e7004537c109b",
}
DECLARED_PREDECL = "a8566fbfbca5cc5231ef78c35adffbf62264f82bbefe830683616105434c547d"

RESULT_FILES = [
    "GATE_LOCUS_RESULTS.csv",
    "GATE_LOCUS_ANCHOR.csv",
    "GATE_LOCUS_FALSIFIER.json",
    "GATE_LOCUS_SECONDARY_S1.csv",
    "GATE_LOCUS_SECONDARY_S1B.csv",
    "GATE_LOCUS_SECONDARY_S2.csv",
    "GATE_LOCUS_SECONDARY_S3.csv",
]
AUX_FILES = ["console.txt"]

SUMMED_DIRS = ["code", "results"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path):
    return "./" + str(path.relative_to(EXP_DIR))


def main():
    # 1. predeclaration frozen and verbatim
    subprocess.run([sys.executable, str(HERE / "verify_predecl_verbatim.py")], check=True)
    predecl = EXP_DIR / "PRE_DECLARATIONS.md"
    predecl_sha = sha256(predecl)
    if predecl_sha != DECLARED_PREDECL:
        sys.exit("FATAL: PRE_DECLARATIONS.md does not match its frozen hash")

    # 2. determinism: every artifact byte-identical between the two runs
    run2 = RESULTS / "determinism_run2"
    identical = {}
    for name in RESULT_FILES + AUX_FILES:
        a, b = RESULTS / name, run2 / name
        ok = a.exists() and b.exists() and a.read_bytes() == b.read_bytes()
        identical[name] = ok
        if not ok:
            sys.exit(f"FATAL: determinism failure on {name}")
    if not all(identical.values()):
        sys.exit("FATAL: nondeterministic output")

    inputs = {}
    for key, path in (("frozen_panel", PANEL), ("shadow_gate_panel", GATES), ("council_brief", BRIEF)):
        actual = sha256(path)
        inputs[key] = {
            "path": str(path.relative_to(PROGRAMME_ROOT)),
            "sha256": actual,
            "matches_declared": actual == DECLARED[
                {"frozen_panel": "panel", "shadow_gate_panel": "gates", "council_brief": "brief"}[key]],
            "read_only": True,
        }
        if not inputs[key]["matches_declared"]:
            sys.exit(f"FATAL: input hash mismatch for {key}")

    falsifier = json.loads((RESULTS / "GATE_LOCUS_FALSIFIER.json").read_text(encoding="utf-8"))
    results_csv = (RESULTS / "GATE_LOCUS_RESULTS.csv").read_text(encoding="utf-8").strip().split("\n")
    levels = []
    for line in results_csv[1:]:
        f = line.split(",")
        levels.append({"level": f[2], "n_cells": int(f[3]),
                       "share_lt095_pct": float(f[11]), "verdict_bar95": f[18],
                       "share_lt099_pct": float(f[13]), "verdict_bar99": f[19],
                       "class_stable": f[20] == "yes", "headline_verdict": f[21]})

    manifest = {
        "label": "SYNTHETIC (generator panels only; no observed series read)",
        "experiment": "EXP-8 GATE-LOCUS",
        "brief": "Council brief 022 (D122 #3); SYNTHESIS_022.md section 6, EXP-8 GATE-LOCUS, rank #3",
        "worker": "WORKER GL",
        "date": "2026-11-20",
        "status": "COMPLETE",
        "statement": (
            "Descriptive census of where the frozen generator's school gates bind, at two predeclared bars, "
            "with the predeclared falsifier. Read-only on frozen panels: no re-fit, no new layer, no re-run of "
            "A3-S, no reopening of A3-D's verdict or A3-S's c4a. No causal claim and no direction claim; D63 "
            "remains UNABLE as to cause. No threshold was changed after results."
        ),
        "predeclaration": {
            "file": "PRE_DECLARATIONS.md",
            "sha256": predecl_sha,
            "recorded_sidecar": "PRE_DECLARATIONS.sha256",
            "sidecar_sha256": sha256(EXP_DIR / "PRE_DECLARATIONS.sha256"),
            "hashed_before_any_run": True,
            "thresholds_changed_after_results": False,
            "verbatim_source": "SYNTHESIS_022.md lines 370-393 (section 6, EXP-8), spliced by code/build_predeclarations.py",
            "verbatim_verified_by": "code/verify_predecl_verbatim.py",
        },
        "dependency_precondition": {
            "rule": "brief section 4.4: EXP-7 -> EXP-6 -> EXP-8 -> EXP-9 -> EXP-10",
            "exp7_returned": True,
            "exp7_verdict": "ENDPOINT-ONLY + b2 + BASELINE-GUARD-PASS",
            "exp6_on_disk_at_freeze": False,
            "note": "EXP-8 consumes no EXP-6 output and shares no estimand with it; no threshold here depends on EXP-6.",
        },
        "frozen_inputs_read_only": inputs,
        "declared_constants": {
            "bar_95": 0.95, "bar_99": 0.99,
            "gate_binds_at_share": 0.50, "unrationed_at_share": 0.10,
            "deep_bar": 0.50, "deep_share_max": 0.20,
            "p_off": "admitted_official / demand_official",
            "levels": ["primary", "lower_secondary", "upper_secondary", "tertiary"],
            "levels_checked_by_falsifier": ["upper_secondary", "tertiary"],
            "country_set": "all 30 country_id values",
            "years": "1970-2025 (56 per country-level)",
            "cells_per_level": 1680,
        },
        "verdicts": levels,
        "falsifier": {
            "outcome": falsifier["primary_reading"]["outcome"],
            "tripped": falsifier["primary_reading"]["tripped"],
            "levels": falsifier["primary_reading"]["levels"],
            "n_country_series_exceeding_20pct": falsifier[
                "secondary_reading_non_verdict_bearing"]["n_series_exceeding_20pct"],
            "architecture_conclusion": falsifier["consequence"]["architecture_conclusion"],
        },
        "branch": {
            "state": "POSITIVE",
            "rule": "upper_secondary and tertiary UNRATIONED at both bars (PRE_DECLARATIONS.md section 7)",
            "consequence": ("the 'ceiling as upper gate' line is CLOSED; any future demand/shadow layer must be "
                            "re-declared at the binding gate or the upper gate must be given a capacity constraint "
                            "first; A3-D and c4a are explained, not rescued"),
        },
        "exp9_rung_prob": {
            "dispatch": "DISPATCH-ELIGIBLE (Lead action; falsifier clean)",
            "conditions_recorded": [
                "arm A's P = pi0(g2) ~ 0.999 is the gate probability both on-disk constructs agree is ~1 for the anchor type",
                "arm B substitutes the absorption ratio 0.151 for a probability: no anchor gate-year has pi0 in [0.14, 0.16]",
            ],
        },
        "determinism": {
            "rng_free": True,
            "clock_free": True,
            "second_run": "results/determinism_run2/",
            "artifacts_compared": len(identical),
            "all_byte_identical": all(identical.values()),
            "per_file": identical,
            "method": "cmp on each artifact; see code/make_manifest.py",
        },
        "results": {},
        "findings": {
            "file": "FINDINGS.md",
            "sha256": sha256(EXP_DIR / "FINDINGS.md"),
            "label": "SYNTHETIC",
        },
        "no_writes_outside_experiment_dir": True,
        "web_used": False,
        "server_touched": False,
    }
    for name in RESULT_FILES + AUX_FILES:
        manifest["results"][name] = {
            "sha256": sha256(RESULTS / name),
            "bytes": (RESULTS / name).stat().st_size,
            "deterministic": identical[name],
        }

    (EXP_DIR / "RUN_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    # SHA256SUMS.txt over everything except itself
    lines = []
    for top in ["PRE_DECLARATIONS.md", "PRE_DECLARATIONS.sha256", "FINDINGS.md", "RUN_MANIFEST.json"]:
        lines.append(f"{sha256(EXP_DIR / top)}  ./{top}")
    for d in SUMMED_DIRS:
        for path in sorted((EXP_DIR / d).rglob("*")):
            if path.is_file():
                lines.append(f"{sha256(path)}  {rel(path)}")
    (EXP_DIR / "SHA256SUMS.txt").write_text("\n".join(sorted(lines, key=lambda s: s.split("  ./")[1])) + "\n",
                                            encoding="utf-8")

    print(f"predecl   {predecl_sha}")
    print(f"manifest  {sha256(EXP_DIR / 'RUN_MANIFEST.json')}")
    print(f"sums      {sha256(EXP_DIR / 'SHA256SUMS.txt')}  ({len(lines)} entries)")
    print("determinism: %d/%d artifacts byte-identical" % (sum(identical.values()), len(identical)))


if __name__ == "__main__":
    main()
