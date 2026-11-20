#!/usr/bin/env python3
"""Consolidate lab_2026-11-20_c (Y1-Y5) into battery-level artefacts + verify determinism.

Lead-owned tool. Reads each experiment's results/CLUSTER_RESULTS.csv, validates the predeclared schema,
re-runs each code/run.py to test byte-level reproducibility, concatenates RESULTS.csv, and writes
RUN_MANIFEST.json + SHA256SUMS.txt. Never changes any result by hand.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
# ROOT = .../experiments/massification-2026-11-20/10_massification/extensions/lab_2026-11-20_c
PKG = ROOT.parents[2]  # .../experiments/massification-2026-11-20
PY = "/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python"

CLUSTERS = [
    ("Y1_ceiling_residual", "Y1_ceiling_residual", ["Y1"]),
    ("Y2_leadlag", "Y2_leadlag", ["Y2"]),
    ("Y3_capacity_floor", "Y3_capacity_floor", ["Y3"]),
    ("Y4_worldsociety", "Y4_worldsociety", ["Y4"]),
    ("Y5_portability_audit", "Y5_portability_audit", ["Y5"]),
]

COLS = ["experiment", "cluster", "question", "estimand", "estimate", "se", "ci_low", "ci_high",
        "n", "clusters", "threshold", "verdict", "label", "note"]

VERDICT_OK = {"SUPPORTED", "NOT SUPPORTED", "UNABLE", "DISTINGUISHED", "NOT DISTINGUISHED",
              "DATA-COMPLETE", "BLOCKED-ON-DATA"}
LABEL_OK = {"observed", "derived", "check"}

DATA_FILES = [
    "10_massification/data/UNIVERSALIZATION_SERIES.csv",
    "10_massification/data/UNIVERSALIZATION_TIMING.csv",
    "10_massification/data/JOBS_AND_MARKETS_PANEL.csv",
    "10_massification/data/STATE_CAPACITY.csv",
    "10_massification/data/SCHOOL_EXPANSION.csv",
    "10_massification/data/POLICY_TIMELINE.csv",
    "09_relations/data/panel_wdi_long.csv",
    "09_relations/data/panel_wdi_wide.csv",
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def result_files(cdir):
    return sorted((cdir / "results").rglob("*.csv"))


def main():
    errors = []
    pre_sha = sha256(ROOT / "PRE_DECLARATIONS.md")

    frames = []
    cluster_meta = {}
    for cdir_name, ckey, exps in CLUSTERS:
        cdir = ROOT / cdir_name
        cr = cdir / "CLUSTER_RESULTS.csv"
        if not cr.exists():
            cr = cdir / "results" / "CLUSTER_RESULTS.csv"
        meta = {"experiments": exps, "results_files": {}, "code": {}, "manifest": None}
        if not cr.exists():
            errors.append(f"{cdir_name}: missing CLUSTER_RESULTS.csv")
            cluster_meta[cdir_name] = meta
            continue
        df = pd.read_csv(cr)
        df = df.loc[:, ~df.columns.duplicated()]
        missing = [c for c in COLS if c not in df.columns]
        if missing:
            errors.append(f"{cdir_name}: CLUSTER_RESULTS.csv missing columns {missing}")
        df = df[[c for c in COLS if c in df.columns]]
        df["cluster"] = ckey
        frames.append(df)
        for _, row in df.iterrows():
            if str(row.get("verdict")) not in VERDICT_OK:
                errors.append(f"{cdir_name}: bad verdict {row.get('verdict')!r} for {row.get('experiment')}")
            if str(row.get("label")) not in LABEL_OK:
                errors.append(f"{cdir_name}: bad label {row.get('label')!r} for {row.get('experiment')}")
        found = set(df["experiment"].astype(str))
        for e in exps:
            if e not in found:
                errors.append(f"{cdir_name}: missing predeclared experiment {e}")
        for rf in result_files(cdir):
            meta["results_files"][str(rf.relative_to(ROOT))] = sha256(rf)
        for cf in sorted((cdir / "code").glob("*.py")):
            meta["code"][str(cf.relative_to(ROOT))] = sha256(cf)
        mf = cdir / "RUN_MANIFEST.json"
        if mf.exists():
            try:
                meta["manifest"] = json.loads(mf.read_text())
            except Exception as e:  # noqa
                errors.append(f"{cdir_name}: unreadable RUN_MANIFEST.json ({e})")
        cluster_meta[cdir_name] = meta

    if frames:
        results = pd.concat(frames, ignore_index=True)
        # one row per experiment in RESULTS.csv; per-estimand rows stay in each cluster's detail CSVs.
        # (workers may emit one row per measured estimand; the verdict is experiment-level and identical.)
        results = results.drop_duplicates(subset=["experiment"], keep="first")
        results["_o"] = results["experiment"].astype(str).str.extract(r"(\d+)").astype(float)
        results = results.sort_values(["_o", "experiment"]).drop(columns="_o").reset_index(drop=True)
        results.to_csv(ROOT / "RESULTS.csv", index=False)
        n_experiments = int(len(results))
        verdicts = results.groupby("verdict").size().to_dict()
    else:
        n_experiments, verdicts = 0, {}
        errors.append("no cluster result frames collected")

    # --- determinism re-run
    repro = {}
    for cdir_name, _, _ in CLUSTERS:
        cdir = ROOT / cdir_name
        run = cdir / "code" / "run.py"
        if not run.exists():
            repro[cdir_name] = {"status": "NO_CODE"}
            continue
        before = {str(p.relative_to(cdir)): sha256(p) for p in result_files(cdir)}
        t0 = time.time()
        proc = subprocess.run([PY, str(run)], cwd=str(cdir), capture_output=True, text=True, timeout=900)
        after = {str(p.relative_to(cdir)): sha256(p) for p in result_files(cdir)}
        same = before == after and bool(before)
        repro[cdir_name] = {"status": "BYTE_IDENTICAL" if same else "DIFFERS_OR_EMPTY",
                            "exit_code": proc.returncode, "seconds": round(time.time() - t0, 1),
                            "files": sorted(before)}
        if not same:
            errors.append(f"{cdir_name}: re-run not byte-identical; exit={proc.returncode}")
            if proc.stderr:
                repro[cdir_name]["stderr_tail"] = proc.stderr[-800:]
        for rf in result_files(cdir):
            cluster_meta[cdir_name].setdefault("results_files", {})[str(rf.relative_to(ROOT))] = sha256(rf)

    data_hashes = {}
    for rel in DATA_FILES:
        p = PKG / rel
        data_hashes[rel] = sha256(p) if p.exists() else None
        if data_hashes[rel] is None:
            errors.append(f"missing data file {rel}")

    manifest = {
        "battery": "lab_2026-11-20_c",
        "status": "DESCRIPTIVE / DESIGN-ONLY; no causal or direction claims; Y5 design-only",
        "phase_state": "CLOSED at PARTIAL/DESCRIPTIVE/EQUIVALENT (D76); C1-C4 not reopened",
        "authority": "Synthetic Council-2 brief 017 (SYNTHESIS_017.md, D88-D92); standing order D89 = 5 anchored experiments per delivered results batch",
        "run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": sys.version.split()[0],
        "python_path": PY,
        "pandas": pd.__version__,
        "predeclarations_sha256": pre_sha,
        "data_sha256": data_hashes,
        "clusters": cluster_meta,
        "determinism_rerun": repro,
        "n_experiments": n_experiments,
        "verdict_counts": verdicts,
        "verification_errors": errors,
        "labels": {"observed": "on-disk measured series", "derived": "computed from observed series (proxy)"},
        "council_ranking": {"Y1": 1, "Y4": 2, "Y3": 3, "Y2": 4, "Y5": "5 (drop-first)"},
    }
    (ROOT / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")

    # --- SHA256SUMS last so every file verifies
    sums = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in ("__pycache__",))
        for fn in sorted(filenames):
            if fn in ("SHA256SUMS.txt",) or fn.endswith((".pyc", ".bak")):
                continue
            p = Path(dirpath) / fn
            sums.append(f"{sha256(p)}  {p.relative_to(ROOT)}")
    (ROOT / "SHA256SUMS.txt").write_text("\n".join(sorted(sums)) + "\n")

    print(json.dumps({"n_experiments": n_experiments, "verdicts": verdicts,
                      "determinism": {k: v.get("status") for k, v in repro.items()},
                      "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
