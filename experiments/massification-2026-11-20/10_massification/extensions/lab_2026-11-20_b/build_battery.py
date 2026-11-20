#!/usr/bin/env python3
"""Consolidate lab_2026-11-20_b cluster outputs into battery-level artefacts + verify determinism.

Lead-owned tool. Reads each cluster's CLUSTER_RESULTS.csv, validates the predeclared schema, re-runs each
cluster's code/run.py to test byte-level reproducibility, concatenates RESULTS.csv, and writes
RUN_MANIFEST.json + SHA256SUMS.txt. Never changes any cluster result by hand.
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
# ROOT = .../experiments/massification-2026-11-20/10_massification/extensions/lab_2026-11-20_b
PKG = ROOT.parents[2]  # .../experiments/massification-2026-11-20
PY = "/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python"

CLUSTERS = [
    ("cluster_1_absorption", "1_post_secondary_absorption", ["X1", "X2", "X3"]),
    ("cluster_2_tertiary_crossings", "2_tertiary_crossing_structure", ["X4", "X5", "X6"]),
    ("cluster_3_geo_size", "3_geo_size_scaling", ["X7", "X8", "X9"]),
    ("cluster_4_regional_proxy", "4_regional_post_secondary_proxy", ["X10", "X11", "X12"]),
    ("cluster_5_fragmentation_sim", "5_geo_fragmentation_sim", ["X13", "X14", "X15"]),
]

COLS = ["experiment", "cluster", "question", "estimand", "estimate", "se", "ci_low", "ci_high",
        "n", "clusters", "threshold", "verdict", "label", "note", "run_tag"]

VERDICT_OK = {"SUPPORTED", "NOT SUPPORTED", "PARTIAL", "DATA LIMITED", "UNABLE",
              "SIMULATED-THRESHOLD-MET", "SIMULATED-THRESHOLD-MISSED"}
LABEL_OK = {"observed", "derived", "check", "simulated"}

DATA_FILES = [
    "10_massification/data/UNIVERSALIZATION_SERIES.csv",
    "10_massification/data/UNIVERSALIZATION_TIMING.csv",
    "10_massification/data/JOBS_AND_MARKETS_PANEL.csv",
    "10_massification/data/BASELINE_SERIES.csv",
    "09_relations/data/panel_wdi_long.csv",
    "09_relations/data/panel_wdi_wide.csv",
    "09_relations/data/economic_complexity_panel_30ctys.csv",
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
    report = {}
    errors = []

    # --- predeclaration hash
    pre = ROOT / "PRE_DECLARATIONS.md"
    pre_sha = sha256(pre)
    report["predeclarations_sha256"] = pre_sha

    # --- collect cluster results
    frames = []
    cluster_meta = {}
    for cdir_name, ckey, exps in CLUSTERS:
        cdir = ROOT / cdir_name
        cr = cdir / "CLUSTER_RESULTS.csv"
        meta = {"experiments": exps, "results_files": {}, "code": {}, "manifest": None}
        if not cr.exists():
            # some workers write CLUSTER_RESULTS.csv under results/
            alt = cdir / "results" / "CLUSTER_RESULTS.csv"
            if alt.exists():
                cr = alt
        if not cr.exists():
            errors.append(f"{cdir_name}: missing CLUSTER_RESULTS.csv")
            cluster_meta[cdir_name] = meta
            continue
        df = pd.read_csv(cr)
        missing = [c for c in COLS if c not in df.columns and c != "run_tag"]  # run_tag is battery-level
        if missing:
            errors.append(f"{cdir_name}: CLUSTER_RESULTS.csv missing columns {missing}")
        df = df.loc[:, ~df.columns.duplicated()]
        df = df[[c for c in COLS if c in df.columns]]
        df["cluster"] = df.get("cluster", ckey)
        df["run_tag"] = "predeclared"
        frames.append(df)
        # optional harness of disclosed post-hoc amendments (e.g. cluster 5 AMENDMENT-B1)
        alt_amend = cdir / "CLUSTER_RESULTS_AMENDMENT_B1.csv"
        if alt_amend.exists():
            adf = pd.read_csv(alt_amend)
            adf = adf.loc[:, ~adf.columns.duplicated()]
            adf = adf[[c for c in COLS if c in adf.columns]]
            if "run_tag" not in adf.columns:
                adf["run_tag"] = "amendment_B1"
            adf["cluster"] = ckey
            frames.append(adf)
        # schema checks
        for _, row in df.iterrows():
            if str(row.get("verdict")) not in VERDICT_OK:
                errors.append(f"{cdir_name}: bad verdict {row.get('verdict')!r} for {row.get('experiment')}")
            if str(row.get("label")) not in LABEL_OK:
                errors.append(f"{cdir_name}: bad label {row.get('label')!r} for {row.get('experiment')}")
        found = set(df["experiment"].astype(str))
        for e in exps:
            if e not in found:
                errors.append(f"{cdir_name}: missing predeclared experiment {e}")
        # hash every results file
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
        # order by experiment number
        results["_o"] = results["experiment"].astype(str).str.extract(r"(\d+)").astype(float)
        results = results.sort_values(["_o", "experiment"]).drop(columns="_o").reset_index(drop=True)
        results.to_csv(ROOT / "RESULTS.csv", index=False)
        report["n_experiments"] = int(len(results))
        report["verdicts"] = results.groupby("verdict").size().to_dict()
    else:
        results = None
        errors.append("no cluster result frames collected")

    # --- determinism re-run (each cluster, compare result hashes; includes disclosed amendments)
    repro = {}
    for cdir_name, _, _ in CLUSTERS:
        cdir = ROOT / cdir_name
        run = cdir / "code" / "run.py"
        if not run.exists():
            repro[cdir_name] = {"status": "NO_CODE"}
            continue
        before = {p.name: sha256(p) for p in result_files(cdir)}
        t0 = time.time()
        proc = subprocess.run([PY, str(run)], cwd=str(cdir), capture_output=True, text=True, timeout=900)
        after = {p.name: sha256(p) for p in result_files(cdir)}
        same = before == after and bool(before)
        repro[cdir_name] = {
            "status": "BYTE_IDENTICAL" if same else "DIFFERS_OR_EMPTY",
            "exit_code": proc.returncode,
            "seconds": round(time.time() - t0, 1),
            "files": sorted(before),
        }
        if not same:
            errors.append(f"{cdir_name}: re-run not byte-identical ({before} vs {after}); exit={proc.returncode}")
            if proc.stderr:
                repro[cdir_name]["stderr_tail"] = proc.stderr[-800:]
        # disclosed post-hoc amendment scripts (e.g. AMENDMENT_B1): separate determinism check
        for amb in sorted((cdir / "code").glob("amendment_*.py")):
            adir = cdir / "results" / ("AMENDMENT_" + amb.stem.split("_", 1)[1].upper())
            if not adir.is_dir():
                continue
            ab = {p.name: sha256(p) for p in sorted(adir.glob("*.csv"))}
            p2 = subprocess.run([PY, str(amb)], cwd=str(cdir), capture_output=True, text=True, timeout=900)
            aa = {p.name: sha256(p) for p in sorted(adir.glob("*.csv"))}
            key = f"{cdir_name}/{amb.name}"
            repro[key] = {"status": "BYTE_IDENTICAL" if (ab == aa and ab) else "DIFFERS_OR_EMPTY",
                          "exit_code": p2.returncode, "files": sorted(ab)}
            if not (ab == aa and ab):
                errors.append(f"{key}: amendment re-run not byte-identical; exit={p2.returncode}")
        # refresh hashes after re-run
        for rf in result_files(cdir):
            cluster_meta[cdir_name].setdefault("results_files", {})[str(rf.relative_to(ROOT))] = sha256(rf)

    # --- data hashes
    data_hashes = {}
    for rel in DATA_FILES:
        p = PKG / rel
        if p.exists():
            data_hashes[rel] = sha256(p)
        else:
            data_hashes[rel] = None
            errors.append(f"missing data file {rel}")

    # --- manifest
    manifest = {
        "battery": "lab_2026-11-20_b",
        "status": "DESCRIPTIVE / ILLUSTRATIVE; cluster 5 SIMULATED; no causal or direction claims",
        "phase_state": "CLOSED at PARTIAL/DESCRIPTIVE/EQUIVALENT (D76); C1-C4 not reopened",
        "run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": sys.version.split()[0],
        "python_path": PY,
        "pandas": pd.__version__,
        "predeclarations_sha256": pre_sha,
        "data_sha256": data_hashes,
        "clusters": cluster_meta,
        "determinism_rerun": repro,
        "n_experiments": report.get("n_experiments"),
        "verdict_counts": report.get("verdicts"),
        "verification_errors": errors,
        "labels": {"observed": "on-disk measured series", "derived": "computed from observed series (proxy)",
                   "check": "constraint/check cell", "simulated": "stipulated toy model — not evidence"},
    }
    (ROOT / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")

    # --- SHA256SUMS.txt over the battery folder (excluding itself); written LAST so every file verifies
    sums = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in ("__pycache__",))
        for fn in sorted(filenames):
            if fn in ("SHA256SUMS.txt",) or fn.endswith((".pyc", ".bak")):
                continue
            p = Path(dirpath) / fn
            sums.append(f"{sha256(p)}  {p.relative_to(ROOT)}")
    (ROOT / "SHA256SUMS.txt").write_text("\n".join(sorted(sums)) + "\n")

    print(json.dumps({"n_experiments": manifest["n_experiments"], "verdicts": manifest["verdict_counts"],
                      "determinism": repro, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
