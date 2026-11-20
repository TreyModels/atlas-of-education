#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""INDEPENDENT DELIVERABLE AUDIT for the v1.3 module.

Re-reads the delivered files (does not import the simulator) and checks the contracts the
brief and the frozen spec require. LABEL: SYNTHETIC. Prints PASS/FAIL per item.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SYNTH = ROOT.parent
SHADOW = SYNTH / "shadow_module"
V12 = SYNTH / "generator_v1_2"
fails = []


def ok(name, cond, detail=""):
    print("%-72s %s %s" % (name, "PASS" if cond else "FAIL", detail))
    if not cond:
        fails.append(name)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---- frozen spec integrity ------------------------------------------------------------
ok("frozen PRE_DECLARATIONS.md sha256", sha(SHADOW / "PRE_DECLARATIONS.md") ==
   "cf8c61cb818cd63acfb2ada594bc9541bfcb0711f801e13b7eee3b86508f94f2")
ok("frozen S1 note sha256", sha(SHADOW / "PRE_DECLARATIONS_S1_NOTE.md") ==
   "af49a616a7b57c4ef23a693c155d022cd17817f66f5acafba4dc6798dedb65eb")
txt = (ROOT / "PRE_DECLARATIONS.md").read_text()
ok("local copy contains both frozen files verbatim",
   (SHADOW / "PRE_DECLARATIONS.md").read_text() in txt and (SHADOW / "PRE_DECLARATIONS_S1_NOTE.md").read_text() in txt)
ok("v1.2 code unchanged (sha)", sha(V12 / "code" / "sim_v1_2.py") ==
   "61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c")
ok("v1.2 panel unchanged (sha)", sha(V12 / "results" / "synthetic_panel_v1_2.csv") ==
   "14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac")
ok("PARAMS.md matches the hash frozen in the code",
   sha(ROOT / "PARAMS.md") in (ROOT / "code" / "sim_v1_3.py").read_text())

# ---- c6 ------------------------------------------------------------------------------
ok("c6 ablation sha256 == v1.2 panel sha256",
   sha(ROOT / "results" / "_ablation" / "synthetic_panel_v1_3_shadow_off.csv") ==
   sha(V12 / "results" / "synthetic_panel_v1_2.csv"))

# ---- panel ----------------------------------------------------------------------------
with open(ROOT / "results" / "synthetic_panel_v1_3.csv", newline="") as fh:
    rd = csv.DictReader(fh)
    prow = list(rd)
    pcols = rd.fieldnames
v12_cols = next(csv.reader(open(V12 / "results" / "synthetic_panel_v1_2.csv")))
ok("panel row count 6720", len(prow) == 6720, str(len(prow)))
ok("panel starts with the 67 v1.2 columns in order", pcols[:67] == v12_cols, "%d cols" % len(pcols))
ok("every panel row labelled SYNTHETIC", all(r["label"] == "SYNTHETIC" for r in prow))
ok("3 designated country types in the panel",
   sorted({r["shadow_type"] for r in prow if r["shadow_type"]}) ==
   ["SYN_HKG_LIKE", "SYN_KHM_LIKE", "SYN_PHL_LIKE"])
ok("27 countries carry no shadow columns",
   sum(1 for r in prow if r["shadow_gate_status"] == "not_designated") == 27 * 56 * 4)
des = [r for r in prow if r["shadow_gate_status"] == "designated"]
ok("designated rows populated (D_gate in [0,1])",
   all(0.0 <= float(r["D_gate"]) <= 1.0 for r in des), "%d rows" % len(des))

# ---- gates ----------------------------------------------------------------------------
with open(ROOT / "results" / "shadow_gates_v1_3.csv", newline="") as fh:
    grow = list(csv.DictReader(fh))
ok("gate panel 840 rows (3 x 56 x 5)", len(grow) == 840, str(len(grow)))
ok("R in [1,20] every row", all(1.0 <= float(r["R"]) <= 20.0 for r in grow))
ok("D_gate in [0,1] every row", all(0.0 <= float(r["D_gate"]) <= 1.0 for r in grow))
ok("pi1 >= pi0 every row", all(float(r["pi1"]) >= float(r["pi0"]) - 1e-12 for r in grow))
ok("Pi >= pi0 every row", all(float(r["Pi"]) >= float(r["pi0"]) - 1e-12 for r in grow))
ok("Pi bound |Pi-pi0| <= delta*(1-pi0) every row",
   all(abs(float(r["Pi"]) - float(r["pi0"])) <= float(r["dpi"]) + 1e-12 for r in grow))
ok("no NaN in gate panel", not any(v.lower() == "nan" for r in grow for v in r.values()))

# ---- checks ---------------------------------------------------------------------------
with open(ROOT / "results" / "shadow_checks_v1_3.csv", newline="") as fh:
    chk = list(csv.DictReader(fh))
ids = [r["check_id"] for r in chk]
ok("checks file carries c1,c2,c3,c4,c4a,c4b,c4c,c5,c6", ids ==
   ["c1", "c2", "c3", "c4", "c4a", "c4b", "c4c", "c5", "c6"], str(ids))
ok("every verdict in {PASS,FAIL,VOID,NOT-SCORED}",
   all(r["verdict"] in ("PASS", "FAIL", "VOID", "NOT-SCORED") for r in chk))
with open(ROOT / "results" / "shadow_checks_detail_v1_3.csv", newline="") as fh:
    det = list(csv.DictReader(fh))
ok("detail file has >=30 component rows", len(det) >= 30, str(len(det)))

# ---- sensitivity ----------------------------------------------------------------------
with open(ROOT / "results" / "shadow_sensitivity_v1_3.csv", newline="") as fh:
    sens = list(csv.DictReader(fh))
ok("31 sensitivity cells", len(sens) == 31, str(len(sens)))
ok("central cell is a row and is not replaced", sens[0]["cell_id"] == "central")

# ---- manifest -------------------------------------------------------------------------
man = json.loads((ROOT / "RUN_MANIFEST.json").read_text())
ok("manifest seed 20261120", man["seed"] == 20261120)
ok("manifest records the frozen spec hash",
   man["spec"]["frozen_shadow_predeclaration_sha256"] ==
   "cf8c61cb818cd63acfb2ada594bc9541bfcb0711f801e13b7eee3b86508f94f2")
ok("manifest result hashes match the files on disk",
   all(sha(ROOT / "results" / k) == v for k, v in man["hashes"]["results"].items()))
ok("manifest host mapping recorded", man["host_mapping"] ==
   {"SYN_HKG_LIKE": "SYN28", "SYN_PHL_LIKE": "SYN00_PHL_LIKE", "SYN_KHM_LIKE": "SYN18"})

# ---- no stray writes outside the module ------------------------------------------------
ok("deliverables exist",
   all((ROOT / f).exists() for f in ("code/sim_v1_3.py", "PARAMS.md", "PRE_DECLARATIONS.md", "FINDINGS.md",
                                    "TUNE_LOG.md", "RUN_MANIFEST.json", "IMPLEMENTATION_NOTE.md",
                                    "IMPLEMENTATION_NOTE_N1.md", "results/determinism_note.md")))

print()
print("AUDIT:", "ALL PASS" if not fails else "FAILURES: %r" % (fails,))
raise SystemExit(0 if not fails else 1)
