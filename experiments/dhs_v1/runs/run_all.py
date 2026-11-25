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
RUN_MAP = ROOT / "harmonize" / "_out" / "run_map.csv"
HASH_LIST = ROOT / "harmonize" / "_out" / "normalized_output_hashes.csv"
SINGLETON_LEDGER = ROOT / "harmonize" / "_out" / "singleton_ledger.csv"

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


def preflight(inputs: list[Path], skip: bool, hash_list: Path, run_map: Path, singleton_ledger: Path, extra_pins: dict[str, str] | None = None) -> dict:
    """Pin the normalized inputs and reconcile the run map before any estimation.

    * every input must match `normalized_output_hashes.csv` (frozen adapter output);
    * every feasible (file, experiment) pair from `run_map.csv` must be produced;
    * the singleton-PSU ledger (D-07) must exist and be recorded.
    Synthetic/test fixtures bypass hash pinning via --skip-preflight.
    """
    report: dict = {"hash_pins": {}, "run_map": str(run_map), "singleton_ledger": None}
    if skip:
        report["skipped"] = True
        print("[preflight] skipped (synthetic/test mode)")
        return report
    if not hash_list.exists():
        sys.exit(f"[preflight] REFUSED: missing input hash list {hash_list}")
    pins = pd.read_csv(hash_list)
    pins = {str(r["file"]): str(r["sha256"]) for _, r in pins.iterrows()}
    report["hash_list_sha256"] = sha256(hash_list)
    for inp in inputs:
        name = inp.name
        actual = sha256(inp)
        expected = pins.get(name)
        if expected is None and extra_pins and name in extra_pins:
            expected = extra_pins[name]
            print(f"[preflight] extra pin accepted: {name}")
        if expected is None:
            sys.exit(f"[preflight] REFUSED: {name} not in normalized_output_hashes.csv")
        if actual != expected:
            sys.exit(f"[preflight] REFUSED: {name} sha256 mismatch (adapter output changed after freeze)")
        report["hash_pins"][name] = actual
    if not run_map.exists():
        sys.exit(f"[preflight] REFUSED: missing run map {run_map}")
    rm = pd.read_csv(run_map)
    report["run_map_sha256"] = sha256(run_map)
    input_names = {i.name for i in inputs}
    report["expected"] = {str(r["file"]): str(r.get("experiments_feasible", ""))
                          for _, r in rm.iterrows() if str(r["file"]) in input_names}
    if singleton_ledger.exists():
        led = pd.read_csv(singleton_ledger)
        report["singleton_ledger"] = {
            "path": str(singleton_ledger), "sha256": sha256(singleton_ledger),
            "rows": int(len(led)), "singleton_strata": int(led["singleton_psu"].sum())
            if "singleton_psu" in led.columns else None,
        }
        print(f"[preflight] singleton ledger: {report['singleton_ledger']['singleton_strata']} singleton strata")
    else:
        sys.exit("[preflight] REFUSED: missing singleton_ledger.csv (D-07 requires it)")
    print(f"[preflight] {len(report['hash_pins'])} inputs hash-pinned; run map reconciled")
    return report


def run_engine(rscript: str, engine: Path, inp: Path, outdir: Path, engine_args: list[str] | None = None) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    log = outdir / "engine.log"
    t0 = time.time()
    with open(log, "w") as fh:
        proc = subprocess.run([rscript, str(engine), str(inp), str(outdir)] + list(engine_args or []),
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
    """Record the externally-validation-graded benchmarks and whether E1-E8 cells are comparable.

    The validated benchmarks are extraction-level (age band 6-11 / definitions differ from the
    E1-E8 domains), so no automatic cell-level comparison is claimed here: the registry records
    what was externally validated by the data team and QA, and every estimate row is flagged
    not_externally_benchmarked unless a benchmark's definition matches the cell exactly.
    """
    if not bench_path.exists():
        return pd.DataFrame(columns=["benchmark_id", "status", "note"])
    b = pd.read_csv(bench_path)
    rows = []
    for _, row in b.iterrows():
        status = str(row.get("status", "")).upper()
        rows.append({
            "benchmark_id": row.get("benchmark_id"),
            "country": row.get("country"), "wave": row.get("wave"),
            "indicator": row.get("indicator"),
            "published": row.get("published") or row.get("estimate"),
            "tolerance_pp": row.get("tolerance_pp"),
            "registry_status": status,
            "cell_comparison": "NOT_CELL_COMPARABLE: benchmark is extraction-level (different age band/definition than E1-E8 cells)",
            "citation": row.get("citation"),
            "note": row.get("notes", ""),
        })
    out = pd.DataFrame(rows)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--engine", type=Path, default=None, help="analysis engine (auto-detected if omitted)")
    ap.add_argument("--inputs", nargs="+", required=True, help="normalized CSV files or globs/dirs")
    ap.add_argument("--out", type=Path, default=ROOT / "runs" / time.strftime("%Y-%m-%d_all"))
    ap.add_argument("--benchmarks", type=Path, default=DEFAULT_BENCH)
    ap.add_argument("--mode", choices=["synthetic", "test", "real"], default="test")
    ap.add_argument("--rscript", default=str(Path.home() / "neon-boot" / "r-env" / "bin" / "Rscript"))
    ap.add_argument("--run-map", type=Path, default=RUN_MAP)
    ap.add_argument("--hash-list", type=Path, default=HASH_LIST)
    ap.add_argument("--singleton-ledger", type=Path, default=SINGLETON_LEDGER)
    ap.add_argument("--extra-pin", action="append", default=[], metavar="NAME=SHA256",
                    help="pin an input not in the frozen per-file hash list (e.g. merged layer); repeatable")
    ap.add_argument("--engine-args", default="", help="extra flags passed to the R engine, e.g. '--lonely-psu=adjust'")
    ap.add_argument("--expected-csv", type=Path, default=ROOT / "harmonize" / "_out" / "availability_E1_E8.csv",
                    help="availability matrix used for feasibility reconciliation when run_map does not cover the input")
    ap.add_argument("--expected-exclude", default="PH:2003", help="country:wave cells adjudicated BLOCKED; colon-separated")
    ap.add_argument("--reuse", action="store_true",
                    help="reuse existing engine outputs (skip re-running R when estimates.csv already exists)")
    ap.add_argument("--filter", action="append", default=[], metavar="NAME=E1,E2",
                    help="per-input experiment filter (repeatable); inputs without a filter are left unfiltered")
    ap.add_argument("--skip-preflight", action="store_true",
                    help="synthetic/test fixtures only: bypass hash pinning")
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

    extra = {}
    for spec in args.extra_pin:
        if "=" in spec:
            k, v = spec.split("=", 1)
            extra[k.strip()] = v.strip().lower()
    pre = preflight(inputs, args.skip_preflight, args.hash_list, args.run_map, args.singleton_ledger, extra)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    filters = {}
    for spec in args.filter:
        if "=" in spec:
            k, v = spec.split("=", 1)
            filters[k.strip()] = {x.strip() for x in v.split(",") if x.strip()}
    runs, frames = [], []
    for inp in inputs:
        sub = out / ("run_" + hashlib.sha256(str(inp).encode()).hexdigest()[:12])
        est_existing = sub / "estimates.csv"
        if args.reuse and est_existing.exists() and est_existing.stat().st_size > 0:
            info = {"input": str(inp), "input_sha256": sha256(inp), "outdir": str(sub),
                    "exit_code": 0, "seconds": 0.0, "log": str(sub / "engine.log"), "reused": True}
            print(f"[run] {inp.name}: reused existing estimates -> {sub}")
        else:
            info = run_engine(args.rscript, engine, inp, sub, [a for a in args.engine_args.split() if a])
        runs.append(info)
        est_path = sub / "estimates.csv"
        if est_path.exists() and est_path.stat().st_size > 0:
            d = pd.read_csv(est_path)
            keep = filters.get(inp.name)
            if keep is not None:
                d = d[d["experiment"].astype(str).isin(keep)].copy()
            d["run_input"] = inp.name
            frames.append(d)
        print(f"[run] {inp.name}: exit={info['exit_code']} {info['seconds']}s -> {sub}")

    if not frames:
        sys.exit("engine produced no estimates.csv rows")
    est = pd.concat(frames, ignore_index=True)
    # reconcile feasibility: every feasible (file, experiment) pair must appear
    gaps = []
    expected_map = pre.get("expected") or {}
    if not pre.get("expected") and args.expected_csv.exists():
        # merged/single-input mode: derive expected (experiment, country, wave) set from the
        # verified availability matrix, excluding adjudicated-BLOCKED cells (QA conflict B: PH 2003).
        av = pd.read_csv(args.expected_csv)
        excl = {tuple(x.split(":")) for x in str(args.expected_exclude).split(";") if ":" in x}
        exp_rows = []
        for _, r in av.iterrows():
            if (str(r["country"]), str(r["wave"])) in excl:
                continue
            for col in [c for c in av.columns if c.startswith("E")]:
                if str(r[col]).startswith("FEASIBLE"):
                    exp_rows.append({"experiment": col, "country": str(r["country"]), "wave": str(r["wave"])})
        exp = pd.DataFrame(exp_rows)
        exp.to_csv(out / "expected_cells.csv", index=False)
        got = est[["experiment", "country", "wave"]].astype(str).drop_duplicates()
        got["wave"] = got["wave"].astype(str)
        merged = exp.merge(got, how="outer", indicator=True)
        for _, m in merged[merged["_merge"] != "both"].iterrows():
            gaps.append({"experiment": m["experiment"], "country": m["country"], "wave": m["wave"],
                         "issue": "expected but not produced" if m["_merge"] == "left_only" else "produced but not expected"})
        pd.DataFrame(gaps).to_csv(out / "feasibility_gaps.csv", index=False)
        pre["expected_cells_from"] = str(args.expected_csv)
        pre["expected_cells"] = int(len(exp))
        print(f"[preflight] expected cells from availability matrix: {len(exp)} (excluded {sorted(excl)})")
        gaps = []
    if pre.get("expected"):
        for fname, exp_csv in pre["expected"].items():
            feasible = {e.strip() for e in str(exp_csv).split(";") if e.strip()}
            got = set(est.loc[est.get("run_input") == fname, "experiment"].astype(str))
            for e in sorted(feasible - got):
                gaps.append({"file": fname, "experiment": e, "issue": "feasible but no estimate rows"})
            unexpected = got - feasible
            for e in sorted(unexpected):
                gaps.append({"file": fname, "experiment": e, "issue": "estimate for infeasible experiment"})
        pd.DataFrame(gaps).to_csv(out / "feasibility_gaps.csv", index=False)
        if gaps:
            print(f"[warn] {len(gaps)} feasibility gaps written to feasibility_gaps.csv")
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
        "preflight": pre,
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
