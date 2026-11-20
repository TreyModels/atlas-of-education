"""Assemble RUN_MANIFEST.json for the Cluster A toy package.

ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence;
no historical test; phase closed; do not cite numbers as estimates.

Records seeds, reps per cell, Python version, the imposed parameter vectors and
the SHA-256 of every delivered artefact (full digest and first 16 hex chars).
Run after run_cluster_a.py, verdicts.py and FINDINGS.md exist.
"""

import csv
import hashlib
import json
import platform
import sys
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABEL = ("ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence; "
         "no historical test; phase closed; do not cite numbers as estimates.")
FILES = [
    "PRE_DECLARATIONS.md",
    "FINDINGS.md",
    "RESULTS.csv",
    "RESULTS_SUMMARY.json",
    "verdicts.json",
    "code/toy_market.py",
    "code/run_cluster_a.py",
    "code/verdicts.py",
    "code/build_manifest.py",
]


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    with (ROOT / "RESULTS_SUMMARY.json").open() as f:
        summary = json.load(f)
    with (ROOT / "verdicts.json").open() as f:
        verdicts = json.load(f)

    cells = Counter()
    seed_sets = {}
    with (ROOT / "RESULTS.csv").open() as f:
        reader = csv.reader(f)
        header = next(reader)
        for experiment, arm, seed, metric, value in reader:
            if seed == "AGG":
                continue
            cells[(experiment, arm)] += 1
            seed_sets.setdefault((experiment, arm), set()).add(int(seed))

    n_seeds = summary["seeds"]["count"]
    files = OrderedDict()
    for rel in FILES:
        path = ROOT / rel
        digest = sha256(path)
        st = path.stat()
        files[rel] = {"sha256": digest, "sha256_16": digest[:16],
                      "bytes": st.st_size,
                      "mtime_local": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%dT%H:%M:%S")}

    manifest = OrderedDict()
    manifest["label"] = LABEL
    manifest["generated_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest["package"] = "extensions_archive/toys_2026-11-20/cluster_A"
    manifest["spec"] = "extensions_archive/codex_2026-11-20/COUNCIL_TOY_SPECS_015.md (Cluster A, #1-#3)"
    manifest["python"] = {
        "version": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "dependencies": "stdlib only (no numpy, no network)",
    }
    manifest["seeds"] = {
        "base": summary["seed_base"],
        "count_per_cell": n_seeds,
        "first": summary["seeds"]["first"],
        "last": summary["seeds"]["last"],
        "rule": "seed_i = 20261120 + i, i = 0..199",
        "list": list(range(summary["seeds"]["first"], summary["seeds"]["last"] + 1)),
        "pairing": "one latent cohort per seed, reused by every arm and counterfactual",
    }
    manifest["reps"] = {
        "runs_per_cell": n_seeds,
        "cells": [
            {"experiment": exp, "arm": arm, "seeds": len(seed_sets[(exp, arm)]),
             "rows": cells[(exp, arm)]}
            for (exp, arm) in sorted(cells)
        ],
        "total_rows": sum(cells.values()),
        "csv_header": header,
    }
    manifest["imposed_parameters"] = {
        "engine_constants": {
            "households": 100,
            "budgets": "50 x 1.5, 50 x 4.0 (shuffled)",
            "opportunity_cost": "U[0, 3.5)",
            "public_fee": 1.0,
            "tuition": 2.0,
            "variable_cost": 1.0,
            "unit_contribution": 1.0,
            "base_premium": 4.0,
            "capacity_rule_primary": "fixed lump of `cap` seats per provider",
            "capacity_rule_robustness": "divisible: min(cap, unmet customers at decision)",
            "entry_rule": "unmet customers >= break-even seats bk = F / unit contribution",
            "exit_rule": "allocated customers < bk, minus one-period installation lock",
            "pipeline": "entrants observe capacity already under construction",
        },
        "experiment_1": summary["exp1"]["params"],
        "experiment_1_paths": summary["exp1"]["paths"],
        "experiment_1_modes": summary["exp1"]["modes"],
        "experiment_2": summary["exp2"]["params"],
        "experiment_3": summary["exp3"]["params"],
        "experiment_3_paths": summary["exp3"]["paths"],
    }
    manifest["verdicts"] = {
        "1_entry_hysteresis": verdicts["exp1"]["overall"],
        "2_public_expansion": verdicts["exp2"]["overall"],
        "3_entry_lag": verdicts["exp3"]["overall"],
        "detail_file": "verdicts.json",
    }
    manifest["files"] = files
    manifest["amendments"] = [
        "Amendment 1 in PRE_DECLARATIONS.md: capacity rule set to fixed lumps (base-toy reading), high-F "
        "break-even standardised at bk = cap, pre-amendment #2 F=$12.00 retained as a reported sensitivity cell. "
        "Thresholds and falsifiers unchanged."
    ]
    manifest["reproduce"] = "cd code && python3 run_cluster_a.py && python3 verdicts.py && python3 build_manifest.py"
    manifest["not_evidence"] = ("No number in this package is an estimate of any real quantity. Nothing here "
                                "reopens the closed massification phase or substitutes for the observed "
                                "provider-entry supply-response test in brief 014 section 3.1.")

    out = ROOT / "RUN_MANIFEST.json"
    with out.open("w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print("wrote", out)
    for rel, meta in files.items():
        print("  {0}  {1}".format(meta["sha256_16"], rel))


if __name__ == "__main__":
    sys.exit(main())
