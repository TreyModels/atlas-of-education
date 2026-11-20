#!/usr/bin/env python3
"""Rebuilds RUN_MANIFEST.json from the files on disk (deterministic, no timestamps of its own).

Records: predeclaration sha256, code sha256, every input sha256, every result sha256, the seed
(none), the frozen thresholds, and the two-run determinism evidence (byte-identical outputs).
"""
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd

WTDIR = Path(__file__).resolve().parent.parent
ROOT = WTDIR.parents[2]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


INPUTS = [
    "09_relations/data/panel_wdi_long.csv",
    "10_massification/data/UNIVERSALIZATION_SERIES.csv",
    "09_relations/data/economic_complexity_panel_30ctys.csv",
    "09_relations/data/shadow_gradients.csv",
    "04_data/TARGETS_SHADOW.csv",
]
CODE = ["code/run_wt.py", "code/build_predeclarations.py", "code/build_manifest.py"]
OUT_A = ["results/RESULTS.csv", "results/DETAIL.csv", "results/run_info.json"]
OUT_B = ["_determinism/run_b/RESULTS.csv", "_determinism/run_b/DETAIL.csv",
         "_determinism/run_b/run_info.json"]


def main() -> int:
    pre = WTDIR / "PRE_DECLARATIONS.md"
    info = json.loads((WTDIR / "results/run_info.json").read_text(encoding="utf-8"))

    det = {}
    for a, b in zip(OUT_A, OUT_B):
        ha, hb = sha256(WTDIR / a), sha256(WTDIR / b)
        det[a] = {
            "run_a": f"results/{Path(a).name}",
            "run_a_sha256": ha,
            "run_b": f"_determinism/run_b/{Path(b).name}",
            "run_b_sha256": hb,
            "byte_identical": ha == hb,
        }

    res = pd.read_csv(WTDIR / "results/RESULTS.csv", dtype=str).fillna("")
    manifest = {
        "manifest_version": "WT-1",
        "worker": "WT",
        "battery": "WT1-WT5 (brief_019 section C; D98-D101, D89 standing order)",
        "programme_root": "massification-2026-11-20",
        "write_scope": "10_massification/extensions/wt_2026-11-20/ (only)",
        "predeclaration": {
            "path": rel(pre),
            "sha256": sha256(pre),
            "statement": "written before any run; hash recorded in RUN_MANIFEST.json; "
                         "no threshold change after results",
            "verbatim_source": "08_council/brief_019/SYNTHESIS_019.md lines 105-232 and 234-238 "
                               "(extracted by line range; blocks byte-equal to the source)",
            "blocks_verified_verbatim": True,
        },
        "code": {rel(WTDIR / c): sha256(WTDIR / c) for c in CODE},
        "inputs": {p: sha256(ROOT / p) for p in INPUTS},
        "outputs": {rel(WTDIR / p): sha256(WTDIR / p) for p in OUT_A},
        "seed": None,
        "rng": "none (no bootstrap, no Monte Carlo)",
        "thresholds": info["thresholds"],
        "verdicts": info["verdicts"],
        "determinism": {
            "method": "code/run_wt.py run twice into separate output directories; outputs compared "
                      "byte-for-byte (sha256) and with cmp",
            "run_a_dir": "results/",
            "run_b_dir": "_determinism/run_b/",
            "files": det,
            "all_byte_identical": all(v["byte_identical"] for v in det.values()),
            "environment": {
                "python": sys.version.split()[0],
                "pandas": pd.__version__,
                "numpy": np.__version__,
                "platform": platform.platform(),
            },
            "guarantees": "no RNG; fixed sorts (kind=mergesort); %.6f formatting; no dependence on "
                          "dict/hash order; single-threaded pandas groupby with sort=True/False stated "
                          "explicitly in code",
        },
        "labels": {
            "policy": "OBSERVED / DERIVED / HELD on every row; HELD cells carry no number and are never "
                      "imputed, interpolated, back-cast or forecast",
            "held": {
                "HELD-1": "credential wage-premium series (PSA FIES/LFS; WB Enterprise Surveys) - not on disk",
                "HELD-2": "PHL/KHM/CHN/JPN shadow participation rates - TARGETS_SHADOW rows 'unresolved'",
                "HELD-3": "de facto enforcement; individual competence data; withdrawal episodes - out of scope",
            },
        },
        "scope_discipline": {
            "causal_claims": "none",
            "direction_claims": "none (no push/pull)",
            "c1_c4_reopened": "no",
            "toy_or_synthetic_data": "none",
            "external_data_requests": "none",
            "web_access": "none",
            "writes_outside_scope": "none",
            "wt_pass_means": "a descriptive footprint on disk - NOT validation of the hysteresis paper",
        },
        "rows_reported": int(len(res)),
        "cells_reported_including_nulls": True,
        "result_files": [rel(WTDIR / p) for p in
                         ("results/RESULTS.csv", "results/DETAIL.csv", "results/run_info.json",
                          "RUN_MANIFEST.json", "FINDINGS.md", "RESULTS_README.md")],
    }
    out = WTDIR / "RUN_MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("wrote", out)
    print("predeclaration sha256:", manifest["predeclaration"]["sha256"])
    print("all_byte_identical:", manifest["determinism"]["all_byte_identical"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
