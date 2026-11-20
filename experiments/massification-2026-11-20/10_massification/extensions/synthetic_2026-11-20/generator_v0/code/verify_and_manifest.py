#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_and_manifest.py -- reproducibility check + RUN_MANIFEST.json for generator v0.

SYNTHETIC.  Runs code/sim.py twice into separate output directories, compares every
results/*.csv byte for byte, then writes RUN_MANIFEST.json with hashes, versions,
parameters, and the determinism record.  No observed data is read.
"""

from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
CODE = BASE / "code" / "sim.py"
VERIFY = Path(__file__).resolve()
PY = sys.executable

sys.path.insert(0, str(CODE.parent))
import sim  # noqa: E402  (module constants only; main is guarded)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def csv_hashes(d: Path) -> dict:
    return {p.name: {"sha256": sha256(p), "bytes": p.stat().st_size}
            for p in sorted(d.glob("*.csv"))}


def run(outdir: Path) -> float:
    t0 = time.time()
    subprocess.run([PY, str(CODE), "--outdir", str(outdir)],
                   check=True, capture_output=True, text=True)
    return time.time() - t0


def main() -> int:
    # Run 1: the delivered results.
    t1 = run(RESULTS)
    h1 = csv_hashes(RESULTS)

    # Run 2: fresh temp directory, compare only the CSVs.
    tmp = BASE / "_verify_run2"
    if tmp.exists():
        shutil.rmtree(tmp)
    try:
        t2 = run(tmp)
        h2 = csv_hashes(tmp)
        identical = (h1 == h2)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    summary = json.loads((RESULTS / "run_summary.json").read_text())

    params = {
        "seed": sim.SEED,
        "n_countries": sim.N_COUNTRIES,
        "years": [sim.YEAR_START, sim.YEAR_END],
        "levels": list(sim.LEVELS),
        "C_MEAN": sim.C_MEAN.tolist(),
        "B_PRIM": sim.B_PRIM,
        "B_SEC": summary["b_sec"],
        "B_TER": summary["b_ter"],
        "G": sim.G.tolist(),
        "H": sim.H.tolist(),
        "SIGMA_E": sim.SIGMA_E.tolist(),
        "SURVIVAL": sim.SURVIVAL.tolist(),
        "ADJUST": sim.ADJUST.tolist(),
        "PUSH": sim.PUSH.tolist(),
        "KAPPA": sim.KAPPA,
        "K_Y": sim.K_Y,
        "K_S": sim.K_S,
        "OMEGA": sim.OMEGA.tolist(),
        "X_REF": sim.X_REF,
        "URBAN_REF": sim.URBAN_REF,
        "SERVICES_REF": sim.SERVICES_REF,
        "EFF_CAP": sim.EFF_CAP,
        "PHL": summary["phl_design"],
        "PHL_E": summary["phl_e"],
    }

    manifest = {
        "label": "SYNTHETIC",
        "warning": ("Synthetic data generated from declared equations. Not calibrated evidence about "
                    "the world. Not a forecast. Not a fit to any observed country series."),
        "generator": "code/sim.py",
        "seed": sim.SEED,
        "panel_shape": [summary["panel_rows"], 13],
        "n_countries": summary["n_countries"],
        "years": summary["years"],
        "levels": summary["levels"],
        "params": params,
        "targets": summary["calibration_targets"],
        "observed_numbers_encoded": {
            "brief_targets": summary["calibration_targets"],
            "phl_milestones": {
                "primary_completion_cross": 90.0,
                "lower_secondary_completion_cross": 90.0,
                "upper_secondary_max_below": 90.0,
                "tertiary_ger_start_1970": 15.0,
                "tertiary_ger_end_2024": 50.0,
            },
            "on_disk_diagnostics_only": summary["on_disk_targets_note"],
        },
        "data_files_read": [],
        "target_source": summary["target_source"],
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
        "code_sha256": sha256(CODE),
        "verify_script_sha256": sha256(VERIFY),
        "outputs": h1,
        "determinism": {
            "method": ("run code/sim.py twice into separate directories; compare every "
                       "results/*.csv byte for byte"),
            "run1_sha256": {k: v["sha256"] for k, v in h1.items()},
            "run2_sha256": {k: v["sha256"] for k, v in h2.items()},
            "byte_identical": bool(identical),
            "run1_seconds": round(t1, 3),
            "run2_seconds": round(t2, 3),
            "note": ("Only results/*.csv are compared. results/run_summary.json contains a runtime "
                     "field and is informational; it is not part of the byte-identity claim."),
        },
        "panel_identity": {
            "ger": "100 * enrolment / cohort (max |error| from 6-dp formatting ~5e-7)",
            "completion": "SURVIVAL[level] * ger (max |error| ~1e-6)",
            "guard": "GER in [0,105]; effective ceiling capped at 1.04",
        },
        "files": {
            "panel": "results/synthetic_panel.csv",
            "checks": "results/reproduction_checks.csv",
            "calibration_log": "results/calibration_log.csv",
            "capacity_counterfactual": "results/capacity_counterfactual.csv",
            "params": "PARAMS.md",
            "findings": "FINDINGS.md",
        },
    }

    out = BASE / "RUN_MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    print("SYNTHETIC generator v0 -- reproduction check")
    print(f"run1={t1:.2f}s run2={t2:.2f}s")
    print(f"byte_identical={identical}")
    for name in sorted(h1):
        print(f"  {name}: {h1[name]['sha256'][:16]}... ({h1[name]['bytes']} bytes)")
    print(f"manifest -> {out}")
    return 0 if identical else 1


if __name__ == "__main__":
    sys.exit(main())
