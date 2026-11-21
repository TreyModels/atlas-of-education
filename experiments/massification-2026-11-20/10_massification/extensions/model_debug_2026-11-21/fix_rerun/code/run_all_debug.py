#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEBUG orchestrator -- repaired panels, CAP-01 fix table, repaired EXP-21 register, determinism.

LABEL: DEBUG. Runs, in order and twice for the determinism check:

  1. `run_repaired.py` for v1.3 and v1.2  -> repaired panels (byte-identical on re-run)
  2. `uncap_cells.py`                     -> CAP_FIX_CELLS.csv (35 cells per panel, before/after)
  3. `run_conv_reg_repaired.py`           -> repaired register + m-constancy + verdict

The second run's panels go to `determinism_run2/panels/` and are compared byte-for-byte with
the first run's panels; the register is then run a second time against the SAME canonical panel
bytes, so every register artifact (including its `panel_path` provenance column) is byte-identical.
No clock in outputs; no RNG change; no writes outside this cell.

Usage:
  python run_all_debug.py --run1 results --run2 determinism_run2
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.dirname(CODE_DIR)
DEBUGDIR = os.path.dirname(FIXDIR)          # model_debug_2026-11-21
EXT = os.path.dirname(DEBUGDIR)             # extensions
MASS = os.path.dirname(EXT)                 # 10_massification
ROOT = os.path.dirname(MASS)                # experiments/massification-2026-11-20

SYNTH = "10_massification/extensions/synthetic_2026-11-20"
D = SYNTH + "/generator_v1_3/results/synthetic_panel_v1_3.csv"
D12 = SYNTH + "/generator_v1_2/results/synthetic_panel_v1_2.csv"
DA17 = SYNTH + "/generator_v1_7_partrepair/results/panel_A17.csv"
REG = "10_massification/extensions/conv_reg_2026-11-20"
GEN13 = SYNTH + "/generator_v1_3/code/sim_v1_3.py"
GEN12 = SYNTH + "/generator_v1_2/code/sim_v1_2.py"

DELIVERED_FILES = [
    D, D12, DA17,
    REG + "/PRE_DECLARATIONS.md",
    REG + "/code/run_conv_reg.py",
    REG + "/results/CONV_REG.csv",
    REG + "/results/M_CONSTANCY.csv",
    GEN13, GEN12,
    "10_massification/lit/PHASE_WRITEUP.md",
    "10_massification/extensions/model_debug_2026-11-21/PRE_DECLARATIONS.md",
    "10_massification/extensions/model_debug_2026-11-21/cap_audit/results/CAP_AUDIT.md",
]

REGISTER_ARTIFACTS = ["CONV_REG.csv", "CONV_REG_DETAIL.csv", "CONV_REG_SYSTEM.csv",
                      "M_CONSTANCY.csv", "VERDICT.json", "console.txt", "INPUT_HASHES.json"]
PANEL_ARTIFACTS = ["synthetic_panel_v1_3_repaired.csv", "synthetic_panel_v1_2_repaired.csv"]
CAP_ARTIFACTS = ["CAP_FIX_CELLS.csv", "CAP_FIX_SUMMARY.json", "IDENTITY_CHECK.json"]
LABEL = "DEBUG"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd, env=None):
    print("+ " + " ".join(cmd), flush=True)
    e = dict(os.environ)
    if env:
        e.update(env)
    subprocess.run(cmd, check=True, env=e)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--run1", default="results")
    ap.add_argument("--run2", default="determinism_run2")
    args = ap.parse_args(argv)

    run1 = os.path.join(FIXDIR, args.run1)
    run2 = os.path.join(FIXDIR, args.run2)
    py = sys.executable

    before = {rel: sha256_file(os.path.join(ROOT, rel)) for rel in DELIVERED_FILES}

    for phase, out in (("run1", run1), ("run2", run2)):
        panels = os.path.join(out, "panels")
        os.makedirs(panels, exist_ok=True)
        for gen in ("v1_3", "v1_2"):
            run([py, os.path.join(CODE_DIR, "run_repaired.py"),
                 "--generator", gen, "--out", panels])
        run([py, os.path.join(CODE_DIR, "uncap_cells.py"),
             "--panels-dir", panels, "--out", out])
        run([py, os.path.join(CODE_DIR, "verify_identity.py"), "--out", out])

    # register run 1 on run1 panels; register run 2 on the SAME canonical bytes (run1 panels),
    # because run2 panels are first proven byte-identical to run1 panels.
    for phase, out, pdir in (("run1", run1, os.path.join(run1, "panels")),
                             ("run2", run2, os.path.join(run1, "panels"))):
        run([py, os.path.join(CODE_DIR, "run_conv_reg_repaired.py"), "--out", out],
            env={"FIX_PANELS_DIR": pdir})

    after = {rel: sha256_file(os.path.join(ROOT, rel)) for rel in DELIVERED_FILES}
    unchanged = {rel: (before[rel] == after[rel]) for rel in DELIVERED_FILES}

    # ---- determinism: panels (independent re-run) and register/cap artifacts (byte-identical)
    det = {"label": LABEL, "method": "two runs, SHA-256 per artifact", "artifacts": [],
           "all_identical": True}
    pairs = []
    for name in PANEL_ARTIFACTS:
        pairs.append(("panel", name, os.path.join(run1, "panels", name),
                      os.path.join(run2, "panels", name)))
    for name in REGISTER_ARTIFACTS:
        pairs.append(("register", name, os.path.join(run1, name), os.path.join(run2, name)))
    for name in CAP_ARTIFACTS:
        pairs.append(("cap_fix", name, os.path.join(run1, name), os.path.join(run2, name)))
    for kind, name, pa, pb in pairs:
        ha, hb = sha256_file(pa), sha256_file(pb)
        same = ha == hb
        det["artifacts"].append({"kind": kind, "artifact": name, "sha256_run1": ha,
                                 "sha256_run2": hb, "byte_identical": same})
        det["all_identical"] = det["all_identical"] and same
    det["n_artifacts"] = len(det["artifacts"])
    det["verdict"] = "DETERMINISTIC" if det["all_identical"] else "NON-DETERMINISTIC"
    det["note"] = ("panels are produced by an independent second execution of each generator; "
                   "the register is a second execution on the byte-identical panel set, so its "
                   "panel_path provenance column is also identical")
    det["delivered_inputs_unchanged"] = all(unchanged.values())
    with open(os.path.join(run1, "DETERMINISM.json"), "w", encoding="utf-8") as fh:
        json.dump(det, fh, indent=2, sort_keys=True)
        fh.write("\n")

    # ---- deliverable-name copies of the repaired register outputs
    for src, dst in (("CONV_REG.csv", "REPAIRED_CONV_REG.csv"),
                     ("M_CONSTANCY.csv", "REPAIRED_M_CONSTANCY.csv")):
        data = open(os.path.join(run1, src), "rb").read()
        with open(os.path.join(run1, dst), "wb") as fh:
            fh.write(data)

    # ---- input hashes (delivered + repaired + code)
    hashes = {"label": LABEL, "inputs": [], "delivered_inputs_unchanged": unchanged}
    rels = list(DELIVERED_FILES) + [
        "10_massification/extensions/model_debug_2026-11-21/fix_rerun/PRE_DECLARATIONS.md",
        "10_massification/extensions/model_debug_2026-11-21/fix_rerun/code/sim_v1_3_fix.py",
        "10_massification/extensions/model_debug_2026-11-21/fix_rerun/code/sim_v1_2_fix.py",
        "10_massification/extensions/model_debug_2026-11-21/fix_rerun/code/run_conv_reg_repaired.py",
        "10_massification/extensions/model_debug_2026-11-21/fix_rerun/results/panels/synthetic_panel_v1_3_repaired.csv",
        "10_massification/extensions/model_debug_2026-11-21/fix_rerun/results/panels/synthetic_panel_v1_2_repaired.csv",
    ]
    for rel in rels:
        p = os.path.join(ROOT, rel)
        hashes["inputs"].append({"path": rel, "sha256": sha256_file(p) if os.path.exists(p) else None})
    with open(os.path.join(run1, "INPUT_HASHES_DEBUG.json"), "w", encoding="utf-8") as fh:
        json.dump(hashes, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print("[%s] determinism: %s (%d artifacts); delivered inputs unchanged: %s"
          % (LABEL, det["verdict"], det["n_artifacts"], all(unchanged.values())))
    if not all(unchanged.values()):
        for rel, ok in unchanged.items():
            if not ok:
                print("  CHANGED: %s" % rel)
        raise SystemExit(2)
    if not det["all_identical"]:
        for a in det["artifacts"]:
            if not a["byte_identical"]:
                print("  NON-IDENTICAL: %s/%s" % (a["kind"], a["artifact"]))
        raise SystemExit(2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
