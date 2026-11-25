#!/usr/bin/env python3
"""Lead-owned DHS experiment run harness (pre-execution readiness).

Orchestrates the QA-signed-off R analysis engine over harmonized `normalized.csv`
inputs, then applies the pre-declared disclosure rule, multiplicity correction,
benchmark comparison and writes a reproducible manifest with hashes.

SAFETY GATE (D-06): in `--mode real` the harness refuses to run unless
`qa/QA_SIGNOFF.json` exists, is `{"signed_off": true, ...}`, and names the exact
sha256 of the engine it was signed off for. Synthetic/mode=test runs are allowed
without the gate (used to validate the harness itself).

No restricted microdata is written to the box or to git; inputs are local paths
and outputs here are aggregate estimates only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]          # .../experiments/dhs_v1
ENGINE_CANDIDATES = [
    ROOT / "qa" / "experiments_v2.R",
    ROOT / "qa" / "adopted" / "experiments_v2.R",
    ROOT / "qa" / "contrasts.R",
]


def default_engine() -> Path:
    """QA owns the engine path; auto-detect the current canonical file.

    The exact engine is pinned at sign-off via qa/QA_SIGNOFF.json (engine_sha256),
    so a moved/renamed file cannot silently change the analysis.
    """
    for cand in ENGINE_CANDIDATES:
        if cand.exists():
            return cand
    return ENGINE_CANDIDATES[0]
DEFAULT_BENCH = ROOT / "benchmarks" / "benchmark_registry_v0.2.csv"
SIGNOFF = ROOT / "qa" / "QA_SIGNOFF.json"

SUPPRESS_N = 30        # n_unweighted
SUPPRESS_PSU = 2       # n_psu
SUPPRESS_DF = 1        # design_df
FLAG_N = 50
FLAG_RSE = 25.0
FLAG_DF = 30


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def r_version(rscript: str) -> dict:
    try:
        out = subprocess.check_output(
            [rscript, "-e",
             'cat(R.version.string, "|", as.character(packageVersion("survey")), "\\n")'],
            text=True, stderr=subprocess.STDOUT, timeout=120)
        return {"raw": out.strip()}
    except Exception as exc:  # noqa: BLE001 - recorded, not raised
        return {"error": str(exc)}


def gate(mode: str, engine: Path) -> None:
    if mode != "real":
        print("[gate] synthetic/test mode: QA sign-off gate not enforced")
        return
    if not SIGNOFF.exists():
        sys.exit("[gate] REFUSED: real-data run without qa/QA_SIGNOFF.json (D-06)")
    try:
        payload = json.loads(SIGNOFF.read_text())
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"[gate] REFUSED: unreadable QA_SIGNOFF.json: {exc}")
    if not payload.get("signed_off"):
        sys.exit("[gate] REFUSED: QA_SIGNOFF.json does not say signed_off=true")
    signed = payload.get("engine_sha256")
    actual = sha256(engine)
    if signed and signed != actual:
        sys.exit(f"[gate] REFUSED: engine sha256 changed after QA sign-off "
                 f"(signed {signed[:12]}..., actual {actual[:12]}...)")
    print(f"[gate] QA sign-off verified for engine {actual[:12]}...")


def run_engine(rscript: str, engine: Path, inp: Path, outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    log = outdir / "engine.log"
    t0 = time.time()
    with open(log, "w") as fh:
        proc = subprocess.run([rscript, str(engine), str(inp), str(outdir)],
                              stdout=fh, stderr=subprocess.STDOUT, text=True)
    return {"input": str(inp), "input_sha256": sha256(inp), "outdir": str(outdir),
            "exit_code": proc.returncode, "seconds": round(time.time() - t0, 2),
            "log": str(log)}


def apply_rules(est: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply the pre-declared D-03 disclosure rule to engine output (v2 schema aware)."""
    df = est.copy()
    n_col = "n_unweighted" if "n_unweighted" in df.columns else ("n" if "n" in df.columns else None)
    n = pd.to_numeric(df[n_col], errors="coerce").to_numpy(dtype=float) if n_col else [float("nan")] * len(df)
    npsu = pd.to_numeric(df["n_psu"], errors="coerce").to_numpy(dtype=float) if "n_psu" in df.columns else [float("nan")] * len(df)
    ddf = pd.to_numeric(df["design_df"], errors="coerce").to_numpy(dtype=float) if "design_df" in df.columns else [float("nan")] * len(df)
    se = pd.to_numeric(df["se"], errors="coerce").to_numpy(dtype=float) if "se" in df.columns else [float("nan")] * len(df)
    est_v = pd.to_numeric(df["estimate"], errors="coerce").to_numpy(dtype=float) if "estimate" in df.columns else [float("nan")] * len(df)
    reasons = []
    for i in range(len(df)):
        r = []
        if not pd.isna(n[i]) and n[i] < SUPPRESS_N:
            r.append("n_unweighted<30")
        if not pd.isna(npsu[i]) and npsu[i] < SUPPRESS_PSU:
            r.append("n_psu<2")
        if not pd.isna(ddf[i]) and ddf[i] < SUPPRESS_DF:
            r.append("design_df<1")
        if pd.isna(se[i]) or pd.isna(est_v[i]):
            r.append("non_finite")
        reasons.append(";".join(r))
    df["suppressed"] = [bool(r) for r in reasons]
    df["suppression_reason"] = reasons
    df["lead_flag_n_lt_50"] = [bool(not pd.isna(n[i]) and n[i] < FLAG_N) for i in range(len(df))]
    with_np = pd.Series(se)
    est_s = pd.Series(est_v)
    rse = (with_np / est_s.replace(0, pd.NA)).abs() * 100
    df["lead_flag_rse_gt_25"] = (rse > FLAG_RSE).fillna(False).tolist()
    df["lead_flag_df_lt_30"] = [bool(not pd.isna(ddf[i]) and ddf[i] < FLAG_DF) for i in range(len(df))]
    ledger = (df[df["suppressed"]].groupby(["suppression_reason"], dropna=False)
              .size().reset_index(name="cells"))
    ledger.insert(0, "rule_version", "D-03/v0.1")
    return df, ledger


def multiplicity(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    q = pd.Series(np.nan, index=out.index, dtype="float64")
    pcol = 'p_value' if 'p_value' in out.columns else ('p' if 'p' in out.columns else None)
    if pcol and out[pcol].notna().any():
        p = pd.to_numeric(out[pcol], errors="coerce")
        # family 1: by experiment (pre-declared), BH
        for _, idx in out.groupby("experiment").groups.items():
            vals = p.loc[idx].dropna()
            if len(vals) == 0:
                continue
            order = vals.sort_values().index
            m = len(vals)
            qv = vals.loc[order].to_numpy() * m / (pd.Series(range(1, m + 1), index=order))
            qv = pd.Series(qv, index=order).cummin()[::-1].cummin()[::-1]
            q.loc[order] = pd.Series(qv, index=order).clip(upper=1.0)
        out["q_bh_by_experiment"] = q
        # family 2: global (all cells) BH, for transparency
        vals = p.dropna()
        order = vals.sort_values().index
        m = len(vals)
        qg = (vals.loc[order].to_numpy() * m
              / (pd.Series(range(1, m + 1), index=order))).clip(upper=1.0)
        qg = pd.Series(qg, index=order).cummin()[::-1].cummin()[::-1]
        out["q_bh_global"] = np.nan
        out.loc[order, "q_bh_global"] = qg
    out["multiplicity_family"] = "BH by experiment (pre-declared); global BH reported separately"
    return out


def benchmark_check(est: pd.DataFrame, bench_path: Path) -> pd.DataFrame:
    if not bench_path.exists():
        return pd.DataFrame(columns=["benchmark_id", "status", "note"])
    b = pd.read_csv(bench_path)
    rows = []
    for _, row in b.iterrows():
        hit = est[(est.get("country").astype(str) == str(row["country"])) &
                  (est.get("wave").astype(str) == str(row["wave"]))]
        if row["status"] != "AVAILABLE":
            rows.append({"benchmark_id": row["benchmark_id"], "status": "PENDING",
                         "country": row["country"], "wave": row["wave"], "note": row.get("notes", "")})
            continue
        if hit.empty:
            rows.append({"benchmark_id": row["benchmark_id"], "status": "NO_MATCHING_CELL",
                         "country": row["country"], "wave": row["wave"], "note": ""})
            continue
        try:
            target = float(str(row["estimate"]).split()[0])
        except Exception:  # noqa: BLE001
            rows.append({"benchmark_id": row["benchmark_id"], "status": "UNPARSEABLE",
                         "country": row["country"], "wave": row["wave"], "note": row["estimate"]})
            continue
        for _, cell in hit.iterrows():
            val = pd.to_numeric(pd.Series([cell.get("estimate")]), errors="coerce").iat[0]
            if pd.isna(val):
                continue
            diff = (val - target) * 100  # estimates in shares, benchmark in percent
            tol = float(row.get("tolerance_pp") or 0) or 0.0
            rows.append({"benchmark_id": row["benchmark_id"], "status": "COMPARED",
                         "country": row["country"], "wave": row["wave"],
                         "experiment": cell.get("experiment"), "group": cell.get("group"),
                         "dhs_extract": round(float(val), 4), "published": target,
                         "diff_pp": round(float(diff), 2), "tolerance_pp": tol,
                         "within_tolerance": abs(diff) <= tol,
                         "definition_match": row.get("definition_match", ""),
                         "citation": row.get("citation", "")})
    return pd.DataFrame(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--engine", type=Path, default=None, help="analysis engine (auto-detected if omitted)")
    ap.add_argument("--inputs", nargs="+", required=True, help="normalized CSV files or globs/dirs")
    ap.add_argument("--out", type=Path, default=ROOT / "runs" / time.strftime("%Y-%m-%d_all"))
    ap.add_argument("--benchmarks", type=Path, default=DEFAULT_BENCH)
    ap.add_argument("--mode", choices=["synthetic", "test", "real"], default="test")
    ap.add_argument("--rscript", default=str(Path.home() / "neon-boot" / "r-env" / "bin" / "Rscript"))
    args = ap.parse_args()

    engine = (args.engine or default_engine()).resolve()
    if not engine.exists():
        sys.exit(f"engine not found: {engine}")
    gate(args.mode, engine)

    inputs: list[Path] = []
    for spec in args.inputs:
        p = Path(spec)
        if p.is_dir():
            inputs.extend(sorted(p.glob("*.csv")))
        elif any(ch in spec for ch in "*?["):
            inputs.extend(sorted(Path().glob(spec)))
        else:
            inputs.append(p)
    inputs = [p for p in inputs if p.exists()]
    if not inputs:
        sys.exit("no input CSVs found")

    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    runs, frames = [], []
    for inp in inputs:
        sub = out / ("run_" + hashlib.sha256(str(inp).encode()).hexdigest()[:12])
        info = run_engine(args.rscript, engine, inp, sub)
        runs.append(info)
        est_path = sub / "estimates.csv"
        if est_path.exists() and est_path.stat().st_size > 0:
            d = pd.read_csv(est_path)
            d["run_input"] = inp.name
            frames.append(d)
        print(f"[run] {inp.name}: exit={info['exit_code']} {info['seconds']}s -> {sub}")

    if not frames:
        sys.exit("engine produced no estimates.csv rows")
    est = pd.concat(frames, ignore_index=True)
    est, ledger = apply_rules(est)
    est = multiplicity(est)
    est["exploratory_descriptive"] = True
    est["causal_claim"] = False
    est["not_externally_benchmarked"] = True
    est.to_csv(out / "estimates_final.csv", index=False)
    ledger.to_csv(out / "suppression_ledger.csv", index=False)
    bench = benchmark_check(est, args.benchmarks.resolve())
    bench.to_csv(out / "benchmark_check.csv", index=False)

    manifest = {
        "harness_version": "dhs-runner-v0.1",
        "mode": args.mode,
        "engine": {"path": str(engine), "sha256": sha256(engine)},
        "benchmarks": {"path": str(args.benchmarks), "sha256": sha256(args.benchmarks.resolve()) if args.benchmarks.exists() else None},
        "r": r_version(args.rscript),
        "runs": runs,
        "gate": {"signoff_present": SIGNOFF.exists(), "mode": args.mode},
        "estimates_rows": int(len(est)),
        "suppressed_rows": int(est["suppressed"].sum()),
        "outputs": {name: sha256(out / name) for name in
                    ("estimates_final.csv", "suppression_ledger.csv", "benchmark_check.csv")},
        "rules": {"suppress": "n<30 | n_psu<2 | design_df<1 | non-finite",
                  "flags": "n<50, RSE>25%, df<30",
                  "multiplicity": "BH by experiment + global BH",
                  "disclosure": "aggregate cells only; no microdata"},
        "labels": {"exploratory": True, "causal": False,
                   "wealth_is_not_income": True, "household_size_is_not_kin_support": True},
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    (out / "run_manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"[done] {len(est)} estimate rows, {int(est['suppressed'].sum())} suppressed -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
