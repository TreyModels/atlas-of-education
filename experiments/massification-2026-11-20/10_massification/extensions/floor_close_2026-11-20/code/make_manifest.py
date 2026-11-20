#!/usr/bin/env python3
"""Write RUN_MANIFEST.json and SHA256SUMS.txt for EXP-12 FLOOR-CLOSE.

Deterministic: files are walked and written in sorted path order; no clock, no RNG.
RUN_MANIFEST.json and SHA256SUMS.txt are excluded from their own hash list, and
SHA256SUMS.txt is written last (it covers every other file, including the manifest).
"""

import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
EXP_DIR = HERE.parent
PROGRAMME_ROOT = EXP_DIR.parents[2]
MANIFEST = EXP_DIR / "RUN_MANIFEST.json"
SUMS = EXP_DIR / "SHA256SUMS.txt"
EXCLUDE = {MANIFEST, SUMS, HERE / "__pycache__"}

DETERMINISM_FILES = (
    "FLOOR_CLOSE_RESULTS.csv",
    "FLOOR_CLOSE_SHAPLEY.csv",
    "FLOOR_CLOSE_DETAIL.csv",
    "FLOOR_CLOSE_SENSITIVITY.csv",
    "FLOOR_CLOSE_PANEL.json",
)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    files = sorted(
        (p for p in EXP_DIR.rglob("*")
         if p.is_file() and p not in EXCLUDE and "__pycache__" not in p.parts),
        key=lambda p: p.relative_to(EXP_DIR).as_posix())

    entries = {}
    for p in files:
        rel = p.relative_to(EXP_DIR).as_posix()
        entries[rel] = {"sha256": sha256(p), "bytes": p.stat().st_size}

    panel = json.loads((EXP_DIR / "results" / "FLOOR_CLOSE_PANEL.json").read_text())
    pairs = {}
    for name in DETERMINISM_FILES:
        a = EXP_DIR / "results" / name
        b = EXP_DIR / "results" / "determinism_run2" / name
        pairs[name] = sha256(a) == sha256(b)
    if not all(pairs.values()):
        sys.exit("FATAL: determinism pair mismatch")

    inputs = {
        "panel": {
            "path": "10_massification/extensions/synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv",
            "sha256": panel["inputs"]["panel_sha256"]},
        "params": {
            "path": "10_massification/extensions/synthetic_2026-11-20/generator_v1_2/PARAMS.md",
            "sha256": "0d619781c4e059f54cf771fb385475f5f939dceced5036e8a21b6e07a2b315e3"},
        "generator_code": {
            "path": "10_massification/extensions/synthetic_2026-11-20/generator_v1_2/code/sim_v1_2.py",
            "sha256": "61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c"},
        "council_brief": {
            "path": "08_council/brief_023/SYNTHESIS_023.md",
            "sha256": "39e666cffbe3950d43460ba177a36501d53fd0ec8083cd5c9abcbd1c7aeed44c"},
        "council_decisions": {
            "path": "08_council/DECISIONS.md",
            "sha256": "15c564cffb1d9994386873b7daf9793407745da5477d437ef3adcb9efba8771c"},
    }

    manifest = {
        "experiment": "EXP-12 FLOOR-CLOSE",
        "label": "SYNTHETIC",
        "date": "2026-11-21",
        "worker": "WORKER FC",
        "verdict": panel["verdict"],
        "closing_cells": panel["closing_cells"],
        "falsifier_min_cells": panel["falsifier_min_cells"],
        "predeclaration": {
            "path": "PRE_DECLARATIONS.md",
            "sha256": panel["inputs"]["predecl_sha256"]},
        "inputs": inputs,
        "read_only": True,
        "no_web": True,
        "no_external_request": True,
        "no_model_rerun": True,
        "no_refit": True,
        "no_phys_cap_change": True,
        "write_scope": "10_massification/extensions/floor_close_2026-11-20/",
        "run_commands": [
            "python code/run_floor_close.py",
            "python code/run_floor_close.py results/determinism_run2",
        ],
        "determinism": {
            "pairs": pairs,
            "all_byte_identical": all(pairs.values()),
            "method": "two full executions, byte comparison of all five outputs",
        },
        "files": entries,
    }

    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")

    lines = [f"{sha256(p)}  {p.relative_to(EXP_DIR).as_posix()}"
             for p in sorted(
                 (q for q in EXP_DIR.rglob("*")
                  if q.is_file() and q != SUMS and "__pycache__" not in q.parts),
                 key=lambda q: q.relative_to(EXP_DIR).as_posix())]
    SUMS.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(f"wrote {MANIFEST.relative_to(PROGRAMME_ROOT)} ({len(entries)} files listed)")
    print(f"wrote {SUMS.relative_to(PROGRAMME_ROOT)} ({len(lines)} lines)")
    print(f"determinism all_byte_identical={all(pairs.values())}")
    print(f"verdict={panel['verdict']} N={panel['closing_cells']}")


if __name__ == "__main__":
    main()
