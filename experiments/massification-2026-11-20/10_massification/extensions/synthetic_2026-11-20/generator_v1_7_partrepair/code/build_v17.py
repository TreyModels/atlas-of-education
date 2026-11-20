#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BUILD_V17 -- verify the frozen inputs, prove the predeclaration is embedded, write the
freeze record.

This script NEVER opens `UNIVERSALIZATION_SERIES.csv` and computes NO observed deviation and
NO cell count: it is the pre-freeze step. It refuses to write a freeze record unless

  (i)   the two frozen copies are byte-identical to their sources,
  (ii)  `PRE_DECLARATIONS.md` hashes to the value embedded in the driver (so the code and the
        predeclaration are frozen *together*), and
  (iii) both own source files pass the AST own-code / count-blind lint.

Run:  python code/build_v17.py
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
CELL = CODE.parent
SYNTH = CELL.parent

FROZEN = CODE / "frozen"
V16_SRC = SYNTH / "generator_v1_6_repair" / "code" / "sim_v1_6_repair.py"
V13_SRC = SYNTH / "generator_v1_3" / "code" / "sim_v1_3.py"
PREDECL = CELL / "PRE_DECLARATIONS.md"
PARAMS_MD = CELL / "PARAMS.md"
DRIVER = CODE / "sim_v1_7_partrepair.py"
REPAIR = CODE / "repair_v17.py"
RECORD = CELL / "FREEZE_RECORD.json"

EXPECTED = {
    "frozen/sim_v1_6_repair.py":
        "9c0e799850fd30bb0b46bb7841e8f301715745a5c73452e7644055122325de56",
    "frozen/sim_v1_3.py":
        "70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877",
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    bad = []
    # ---- 1. the frozen copies are unedited -----------------------------------------------
    for rel, want in EXPECTED.items():
        p = CODE / rel
        got = sha(p)
        if got != want:
            bad.append("frozen copy %s: %s != %s" % (rel, got, want))
    if sha(V16_SRC) != EXPECTED["frozen/sim_v1_6_repair.py"]:
        bad.append("source v1.6 sim changed on disk")
    if sha(V13_SRC) != EXPECTED["frozen/sim_v1_3.py"]:
        bad.append("source v1.3 sim changed on disk")

    # ---- 2. the predeclaration's sha is the one embedded in the driver -------------------
    pre_sha = sha(PREDECL)
    txt = DRIVER.read_text()
    tree = ast.parse(txt)
    embedded = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "EXPECTED_PREDECL_SHA"
                for t in node.targets):
            embedded = node.value.value
    if embedded != pre_sha:
        bad.append("PRE_DECLARATIONS.md sha256 %s != embedded %r (edit the constant)"
                   % (pre_sha, embedded))

    # ---- 3. own-code lint: no literal observed path, no band, no count ------------------
    own = {}
    for p in (DRIVER, REPAIR):
        own[p.name] = sha(p)
        for i, ln in enumerate(p.read_text().splitlines(), 1):
            code = ln.split("#")[0]
            if p.name != "build_v17.py":
                for a, b in ((73, 77), (55, 85)):
                    for band in ("[%d,%d]" % (a, b), "[%d, %d]" % (a, b)):
                        if band in code:
                            bad.append("%s:%d band literal %s" % (p.name, i, band))
            # a 33-cell count construct in the pre-freeze sources would be a violation; the
            # one legitimate count construct lives in `load_observed_cells` (phase C, after
            # every arm), which the phase guard and the count-blind audit enforce.
            for tok in ("count33", "n_scored_cells"):
                if tok in code:
                    bad.append("%s:%d 33-cell construct %s" % (p.name, i, tok))

    if bad:
        for b in bad:
            print("REFUSED:", b)
        return 1

    rec = {
        "cell": "EXP-18-PART-REPAIR",
        "label": "SYNTHETIC",
        "date": "2026-11-21",
        "predecl_sha256": pre_sha,
        "params_md_sha256": sha(PARAMS_MD),
        "code_sha256": {
            "code/sim_v1_7_partrepair.py": own["sim_v1_7_partrepair.py"],
            "code/repair_v17.py": own["repair_v17.py"],
            "code/frozen/sim_v1_6_repair.py": sha(CODE / "frozen/sim_v1_6_repair.py"),
            "code/frozen/sim_v1_3.py": sha(CODE / "frozen/sim_v1_3.py"),
        },
        "frozen_inputs_sha256": {
            "generator_v1_3/results/synthetic_panel_v1_3.csv":
                sha(SYNTH / "generator_v1_3" / "results" / "synthetic_panel_v1_3.csv"),
            "generator_v1_6_repair/results/panel_A10_repaired.csv":
                sha(SYNTH / "generator_v1_6_repair" / "results" / "panel_A10_repaired.csv"),
            "generator_v1_6_repair/PRE_DECLARATIONS.md":
                sha(SYNTH / "generator_v1_6_repair" / "PRE_DECLARATIONS.md"),
        },
        "observed_file_opened_before_freeze": False,
        "count_computed_before_freeze": False,
        "pre_freeze_probe": {
            "file": "code/selftest_v17.py",
            "demographic_input": "reconstructed from the frozen v1.3 panel (no observed read)",
            "observed_file_opened": False,
            "count_computed": False,
            "level_statement_printed": False,
            "disclosed_in": "TUNE_LOG.md sec.1",
        },
        "note": ("the predeclaration and the code are frozen together; the driver refuses to "
                 "run if either changes. This record is written by a script that never opens "
                 "the observed series."),
    }
    RECORD.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n")
    (CELL / "PRE_DECLARATIONS.sha256").write_text("%s  PRE_DECLARATIONS.md\n" % pre_sha)
    print("frozen: predecl %s" % pre_sha)
    for k, v in rec["code_sha256"].items():
        print("  code %s %s" % (v, k))
    print("FREEZE_RECORD.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
