#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXP-1 CEIL-ATTRIB -- declared ablations on an unmodified copy of the frozen v1.2
generator, plus the Test B pipeline ratio on the observed PHL UIS series.

LABEL: SYNTHETIC (generator side) / OBSERVED (PHL UIS side).

Determinism. This driver introduces **no RNG of its own**. The only randomness is the
frozen generator's single seeded PCG64 stream (seed 20261120), drawn in the frozen
order; every variant draws exactly the same country parameters and the same shocks, so
every difference between variants is due only to the declared switch. Two runs produce
byte-identical result files.

Discipline. Nothing outside this experiment directory is written. The frozen
`generator_v1_2/` is copied here byte-identically (same relative layout, so the copy's
own frozen-hash guard and path resolution are preserved) and read-only; the scored run
is unchanged. Ablations are declared in-memory variants, never a re-fit.

Reads:  PRE_DECLARATIONS.md (hashed against PRE_DECLARATIONS.sha256)
        generator_v1_2/code/sim_v1_2.py  (sha must equal frozen code sha)
        v1_2/PRE_DECLARATIONS.md         (the v1.2 spec the copy guards)
        ../synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv
        ../../data/UNIVERSALIZATION_SERIES.csv
        ../../../09_relations/data/panel_wdi_long.csv
Usage:  python code/run_ceil_attrib.py [--out results]
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np

MYROOT = Path(__file__).resolve().parent.parent
FROZEN_ROOT = MYROOT / "generator_v1_2"
FROZEN_CODE = FROZEN_ROOT / "code" / "sim_v1_2.py"
FROZEN_PARAMS = FROZEN_ROOT / "PARAMS.md"
V12_SPEC = MYROOT / "v1_2" / "PRE_DECLARATIONS.md"
PREDECL = MYROOT / "PRE_DECLARATIONS.md"
PREDECL_SHA_FILE = MYROOT / "PRE_DECLARATIONS.sha256"

SYNTH_ROOT = MYROOT.parent / "synthetic_2026-11-20" / "generator_v1_2"
FROZEN_PANEL = SYNTH_ROOT / "results" / "synthetic_panel_v1_2.csv"
FROZEN_MANIFEST = SYNTH_ROOT / "RUN_MANIFEST.json"

FROZEN_CODE_SHA = "61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c"
FROZEN_PARAMS_SHA = "0d619781c4e059f54cf771fb385475f5f939dceced5036e8a21b6e07a2b315e3"
FROZEN_PANEL_SHA = "14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac"
V12_SPEC_SHA = "fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16"
FROZEN_MANIFEST_SHA = "36c40ff95470893a6d6fda21d9afe341ec0f374073a7af56cdf9c55c9b75b876"
EXPECTED_PREDECL_SHA = "ed9b31b9cfa24ffa3a2285cb769ad9ecae899e392f77ac648e3c55b7dbfef64f"

YEAR = 2024
LAG = 3
TOL = 1
BAND_LO, BAND_HI = 0.90, 1.10
PP = 2.0
CAL_TOL = 1.0
FRAC = 2.0 / 3.0


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fmt(x):
    if isinstance(x, str):
        return x
    if isinstance(x, bool):
        return "TRUE" if x else "FALSE"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    return f"{float(x):.6f}"


def write_csv(path, cols, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n",
                           extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: fmt(r.get(k, "")) for k in cols})


# ======================================================================================
# load the unmodified frozen copy
# ======================================================================================
def load_frozen_module():
    spec = importlib.util.spec_from_file_location("sim_v1_2_frozen", FROZEN_CODE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ======================================================================================
# observed PHL completion series (OBSERVED)
# ======================================================================================
def load_observed(mod):
    path = mod.DATA / "UNIVERSALIZATION_SERIES.csv"
    upper, lower = {}, {}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("iso3") != "PHL":
                continue
            try:
                y = int(float(r["year"]))
                v = float(r["value"])
            except (ValueError, TypeError):
                continue
            if r["indicator"] == "completion_upper_secondary":
                upper[y] = v
            elif r["indicator"] == "completion_lower_secondary":
                lower[y] = v
    return upper, lower, path


# ======================================================================================
# variant driver: exact replica of frozen run_all() with ONE declared switch
# ======================================================================================
def simulate_variant(mod, switch, P_phl, S_phl):
    rng = np.random.default_rng(mod.SEED)
    cps = mod.apply_declared(mod.draw_countries(rng))
    gnoise = rng.normal(0.0, mod.P["g_noise_sd"], (mod.T, mod.N_C))
    hhnoise = rng.normal(0.0, mod.P["hh_noise_sd"], (mod.T, mod.N_C))
    for j in (2,):
        gnoise[:, j] = gnoise[:, 1]
        hhnoise[:, j] = hhnoise[:, 1]
    for j in (11, 12):
        gnoise[:, j] = gnoise[:, 10]
        hhnoise[:, j] = hhnoise[:, 10]

    if switch == "work_off":
        # declared: child market-work earnings term zeroed in the four-state block
        for cp in cps:
            cp["w_child"] = 0.0
            cp["farm"] = 0.0

    results = []
    for i, cp in enumerate(cps):
        S = mod.cohort_path(cp, S_phl)
        if switch == "flat_cohort" and cp["name"] == "SYN00_PHL_LIKE":
            S = np.full(mod.T, float(S[0]), dtype=float)
        Pop = mod.pop_path(cp, P_phl)
        results.append(mod.simulate_country(cp, gnoise[:, i], hhnoise[:, i], S, Pop))
    return results


def apply_switch(mod, pristine, switch):
    mod.P.clear()
    mod.P.update(copy.deepcopy(pristine))
    if switch == "gamma0":
        mod.P["gamma"] = 0.0
    elif switch == "m1.05":
        mod.P["meas_completion_factor"] = 1.05
    elif switch == "m1.10":
        mod.P["meas_completion_factor"] = 1.10
    elif switch == "m1.12":
        mod.P["meas_completion_factor"] = 1.12
    elif switch in ("buildout_m5", "buildout_p5"):
        dt = -5.0 if switch == "buildout_m5" else 5.0
        mod.P["seat_t50"] = tuple(x + dt for x in pristine["seat_t50"])
    elif switch in ("upper_only_m5", "upper_only_p5"):
        dt = -5.0 if switch == "upper_only_m5" else 5.0
        st = list(pristine["seat_t50"])
        st[2] += dt
        mod.P["seat_t50"] = tuple(st)
    elif switch in ("baseline", "work_off", "flat_cohort"):
        pass
    else:
        raise SystemExit(f"unknown switch {switch}")


VARIANTS = [
    ("baseline", "reference", "none"),
    ("gamma0", "mechanism", 'P["gamma"] = 0.0'),
    ("work_off", "mechanism", 'w_child = 0; farm = 0 (child work earnings = 0)'),
    ("flat_cohort", "mechanism", "SYN00 cohort S(t) = S(1970)"),
    ("m1.05", "calibration", 'P["meas_completion_factor"] = 1.05'),
    ("m1.10", "calibration-reference", 'P["meas_completion_factor"] = 1.10 (frozen)'),
    ("m1.12", "calibration", 'P["meas_completion_factor"] = 1.12'),
    ("buildout_m5", "calibration", 'seat_t50_L - 5 (all four levels)'),
    ("buildout_p5", "calibration", 'seat_t50_L + 5 (all four levels)'),
    ("upper_only_m5", "sensitivity", 'seat_t50[upper] - 5 only'),
    ("upper_only_p5", "sensitivity", 'seat_t50[upper] + 5 only'),
]
MECH = ("gamma0", "work_off", "flat_cohort")
CAL = ("m1.05", "m1.12", "buildout_m5", "buildout_p5")


# ======================================================================================
# Test B pair construction (declared rules, PRE_DECLARATIONS.md section 6)
# ======================================================================================
def build_pairs(upper, lower, lag, tol=TOL, unbounded=False):
    out = []
    for t in sorted(upper):
        target = t - lag
        if target in lower:
            use = target
        else:
            if unbounded:
                cands = list(lower)
            else:
                cands = [y for y in lower if abs(y - target) <= tol]
            if not cands:
                continue
            use = min(cands, key=lambda y: (abs(y - target), y))
        out.append(dict(upper_year=t, lower_year=use,
                        upper=upper[t], lower=lower[use],
                        ratio=upper[t] / lower[use]))
    return out


def classify_B(pairs):
    n = len(pairs)
    inband = sum(1 for p in pairs if BAND_LO - 1e-12 <= p["ratio"] <= BAND_HI + 1e-12)
    below = sum(1 for p in pairs if p["ratio"] < BAND_LO)
    frac_in = inband / n if n else float("nan")
    frac_below = below / n if n else float("nan")
    if n and frac_in >= FRAC:
        verdict = "PIPELINE-CONSISTENT"
    elif n and frac_below >= FRAC:
        verdict = "GATE-LOSS"
    else:
        verdict = "UNDETERMINED"
    return dict(n=n, inband=inband, below=below, frac_in=frac_in,
                frac_below=frac_below, verdict=verdict)


# ======================================================================================
# main
# ======================================================================================
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(MYROOT / "results"))
    args = ap.parse_args(argv)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    # ---- predeclaration guard: frozen before the run --------------------------------
    if not PREDECL.exists():
        raise SystemExit("REFUSING: PRE_DECLARATIONS.md missing")
    got_pre = sha256_file(PREDECL)
    recorded = PREDECL_SHA_FILE.read_text().split()[0] if PREDECL_SHA_FILE.exists() else None
    if got_pre != EXPECTED_PREDECL_SHA or (recorded and got_pre != recorded):
        raise SystemExit(
            "REFUSING: PRE_DECLARATIONS.md sha256 changed after the freeze.\n"
            f"  expected {EXPECTED_PREDECL_SHA}\n  sidecar  {recorded}\n  got      {got_pre}")

    # ---- frozen-object guards ------------------------------------------------------
    checks = {
        "code_copy_sha256": sha256_file(FROZEN_CODE),
        "params_copy_sha256": sha256_file(FROZEN_PARAMS),
        "v12_spec_copy_sha256": sha256_file(V12_SPEC),
        "frozen_panel_ref_sha256": sha256_file(FROZEN_PANEL),
        "frozen_manifest_ref_sha256": sha256_file(FROZEN_MANIFEST),
    }
    expect = {
        "code_copy_sha256": FROZEN_CODE_SHA,
        "params_copy_sha256": FROZEN_PARAMS_SHA,
        "v12_spec_copy_sha256": V12_SPEC_SHA,
        "frozen_panel_ref_sha256": FROZEN_PANEL_SHA,
        "frozen_manifest_ref_sha256": FROZEN_MANIFEST_SHA,
    }
    bad = {k: checks[k] for k in checks if checks[k] != expect[k]}
    if bad:
        raise SystemExit(f"REFUSING: frozen object changed: {bad}")

    mod = load_frozen_module()
    PRISTINE = copy.deepcopy(mod.P)

    S_phl, P_phl, _, _, _ = mod.load_observed_phl_paths()

    # ==================================================================================
    # STEP 0 -- baseline invariance: unmodified copy reproduces the frozen panel
    # ==================================================================================
    base_res, _, _, _, _ = mod.run_all()
    base_rows = mod.build_panel(base_res)
    brepro = outdir / "baseline_reproduction"
    brepro.mkdir(parents=True, exist_ok=True)
    panel_out = brepro / "synthetic_panel_v1_2.csv"
    mod.write_panel(base_rows, panel_out)
    base_panel_sha = sha256_file(panel_out)
    invariance_ok = (base_panel_sha == FROZEN_PANEL_SHA)

    # internal check: the variant driver, with no switch, must also reproduce the same
    # panel bytes (so every ablation difference is the switch, not the driver)
    driver_base = simulate_variant(mod, "baseline", P_phl, S_phl)
    tmp_panel = brepro / "_driver_baseline_check.csv"
    mod.write_panel(mod.build_panel(driver_base), tmp_panel)
    driver_panel_sha = sha256_file(tmp_panel)
    tmp_panel.unlink()
    driver_matches_module = (driver_panel_sha == FROZEN_PANEL_SHA)

    if not (invariance_ok and driver_matches_module):
        raise SystemExit(
            "STOP: baseline invariance FAILED -- not issuing Test A/Test B results.\n"
            f"  frozen panel sha     {FROZEN_PANEL_SHA}\n"
            f"  unmodified copy sha  {base_panel_sha}\n"
            f"  driver baseline sha  {driver_panel_sha}")

    i24 = int(np.where(mod.YEARS == YEAR)[0][0])

    # ==================================================================================
    # STEP 1 -- Test A: declared ablations
    # ==================================================================================
    var = {}
    details = []
    for switch, role, desc in VARIANTS:
        apply_switch(mod, PRISTINE, switch)
        res = (base_res if switch == "baseline"
               else simulate_variant(mod, switch, P_phl, S_phl))
        r = res[0]
        up_uis = r["comp_uis"][2, :] * 100.0
        lo_uis = r["comp_uis"][1, :] * 100.0
        up_coh = r["comp_coh"][2, :] * 100.0
        lo_coh = r["comp_coh"][1, :] * 100.0
        upto = mod.YEARS <= YEAR
        var[switch] = dict(
            role=role, desc=desc, res=r,
            upper24=float(up_uis[i24]),
            upper_cohort24=float(up_coh[i24]),
            upper_max=float(up_uis[upto].max()),
            lower24=float(lo_uis[i24]),
            first_ge90=(int(mod.YEARS[np.where(up_uis >= 90.0)[0][0]])
                        if np.any(up_uis >= 90.0) else None),
            ger24=float(r["ger"][2, i24]),
            demand24=float(r["demand_share"][2, i24]),
            quality24=float(r["Q"][2, i24]),
            seatcov24=float(r["seats"][2, i24] / max(r["C"][2, i24], 1e-9)),
            upper_series={int(y): float(up_uis[j]) for j, y in enumerate(mod.YEARS)},
            lower_series={int(y): float(lo_uis[j]) for j, y in enumerate(mod.YEARS)},
        )
        for j, y in enumerate(mod.YEARS):
            details.append(dict(
                series=switch, label="SYNTHETIC", year=int(y),
                upper_uis=float(up_uis[j]), upper_cohort_flow=float(up_coh[j]),
                lower_uis=float(lo_uis[j]), lower_cohort_flow=float(lo_coh[j]),
                upper_ger=float(r["ger"][2, j]),
                demand_share_upper=float(r["demand_share"][2, j]),
                quality_upper=float(r["Q"][2, j]),
                seat_coverage_upper=float(r["seats"][2, j] / max(r["C"][2, j], 1e-9)),
            ))

    base24 = var["baseline"]["upper24"]
    delta = {k: var[k]["upper24"] - base24 for k in var}

    mech_hits = sum(1 for k in MECH if abs(delta[k]) >= PP)
    calib_absmax = max(abs(delta[k]) for k in CAL)
    calib_ge2 = calib_absmax >= PP
    calib_lt1 = all(abs(delta[k]) < CAL_TOL for k in CAL)
    mech_lt2 = all(abs(delta[k]) < PP for k in MECH)

    mech_carried = (mech_hits >= 2) and calib_lt1
    calib_carried = calib_ge2 and mech_lt2
    if mech_carried:
        test_a = "MECHANISM-CARRIED"
    elif calib_carried:
        test_a = "CALIBRATION-CARRIED"
    else:
        test_a = "MIXED"

    # ==================================================================================
    # STEP 2 -- Test B: observed PHL pipeline ratio
    # ==================================================================================
    upper_obs, lower_obs, uni_path = load_observed(mod)
    pairs3 = build_pairs(upper_obs, lower_obs, LAG)
    b3 = classify_B(pairs3)
    pairs3_unb = build_pairs(upper_obs, lower_obs, LAG, unbounded=True)
    b3_unb = classify_B(pairs3_unb)
    b2 = classify_B(build_pairs(upper_obs, lower_obs, 2))
    b4 = classify_B(build_pairs(upper_obs, lower_obs, 4))

    # ==================================================================================
    # overall decision (declared ordered rule, PRE_DECLARATIONS.md section 7)
    # ==================================================================================
    if b3["verdict"] == "PIPELINE-CONSISTENT":
        overall = "PIPELINE-CONSISTENT"
    elif test_a == "MECHANISM-CARRIED" and b3["verdict"] == "GATE-LOSS":
        overall = "MECHANISM-CARRIED"
    elif test_a == "CALIBRATION-CARRIED":
        overall = "CALIBRATION-CARRIED"
    else:
        overall = "UNDETERMINED"

    # ==================================================================================
    # write CEIL_ATTRIB_RESULTS.csv
    # ==================================================================================
    RES_COLS = ["test", "row_id", "variant", "switch", "statistic", "value", "unit",
                "baseline_value", "delta_pp", "threshold", "threshold_rule", "verdict",
                "component_account", "n", "label", "note"]
    res_rows = []
    res_rows.append(dict(
        test="A", row_id="A00", variant="baseline", switch="none",
        statistic="upper_uis_2024_pct", value=base24, unit="percent",
        baseline_value=base24, delta_pp=0.0, threshold="reference",
        threshold_rule="frozen v1.2 parameter block", verdict="", component_account="reference",
        n=1, label="SYNTHETIC",
        note="SYN00_PHL_LIKE UIS-convention upper-secondary completion, 2024"))
    for switch, role, desc in VARIANTS[1:]:
        comp = ("mechanism" if role == "mechanism"
                else "calibration" if role in ("calibration", "calibration-reference")
                else "sensitivity")
        thr = (">= 2.0 pp (mechanism)" if role == "mechanism"
               else "< 1.0 pp (calibration bar, mechanism-carried clause)"
               if role == "calibration" else "sensitivity, not verdict-bearing")
        res_rows.append(dict(
            test="A", row_id=f"A{len(res_rows):02d}", variant=switch, switch=desc,
            statistic="upper_uis_2024_pct", value=var[switch]["upper24"],
            unit="percent", baseline_value=base24, delta_pp=delta[switch],
            threshold=("0.0 (reference)" if role == "calibration-reference"
                       else "2.0"),
            threshold_rule=thr, verdict="", component_account=comp, n=1,
            label="SYNTHETIC",
            note=("absolute deviation compared to 2.0 pp / 1.0 pp as declared"
                  if role != "sensitivity" else
                  "declared sensitivity; cannot change the Test A verdict")))
    res_rows.append(dict(
        test="A", row_id="A20", variant="mech_hits", switch="",
        statistic="n_mechanism_ablations_with_abs_delta_ge_2pp", value=mech_hits,
        unit="count", threshold="2", threshold_rule=">= 2 of 3 mechanism ablations",
        verdict="", component_account="mechanism", n=3, label="SYNTHETIC",
        note="gamma=0, work_off, flat_cohort"))
    res_rows.append(dict(
        test="A", row_id="A21", variant="calib_absmax", switch="",
        statistic="max_abs_calibration_delta_pp", value=calib_absmax,
        unit="pp", threshold="2.0", threshold_rule="calibration bar >= 2.0 pp",
        verdict="", component_account="calibration", n=4, label="SYNTHETIC",
        note="m 1.05/1.12, build-out +/-5 y (m=1.10 is the reference, delta 0)"))
    res_rows.append(dict(
        test="A", row_id="A22", variant="calib_lt1", switch="",
        statistic="all_calibration_moves_lt_1pp", value=calib_lt1,
        unit="boolean", threshold="1.0",
        threshold_rule="mechanism-carried requires every calibration move < 1.0 pp",
        verdict="", component_account="calibration", n=4, label="SYNTHETIC", note=""))
    res_rows.append(dict(
        test="A", row_id="A23", variant="test_A_verdict", switch="",
        statistic="test_A_verdict", value=test_a, unit="verdict",
        threshold="", threshold_rule="frozen three-account Test A bars",
        verdict=test_a, component_account=test_a, n=9, label="SYNTHETIC",
        note=("mechanism-carried bar met" if test_a == "MECHANISM-CARRIED" else
              "calibration-carried bar met" if test_a == "CALIBRATION-CARRIED" else
              "neither the mechanism bar nor the calibration bar is met (MIXED)")))

    # Test B rows
    def b_row(row_id, stat, value, threshold, rule, verdict, n, note, unit=None):
        if unit is None:
            unit = ("pairs" if "n_pairs" in stat else "count" if stat.startswith("n_")
                    else "fraction" if "share" in stat else "verdict")
        res_rows.append(dict(
            test="B", row_id=row_id, variant="observed_phl", switch="",
            statistic=stat, value=value, unit=unit,
            threshold=threshold, threshold_rule=rule, verdict=verdict,
            component_account="observed_pipeline", n=n, label="OBSERVED", note=note))

    b_row("B01", "n_pairs_lag3", b3["n"], "n", "observed upper years with a lower "
          "observation at t-3 or nearest within +/-1 y", "", b3["n"],
          "pairs dropped where no lower observation lies within the window")
    b_row("B02", "n_in_band_lag3", b3["inband"], "n", "ratio in [0.90, 1.10]",
          "", b3["n"], "")
    b_row("B03", "share_in_band_lag3", b3["frac_in"], "2/3",
          ">= 2/3 of observed pairs -> PIPELINE-CONSISTENT", "", b3["n"], "")
    b_row("B04", "n_below_0.90_lag3", b3["below"], "n", "ratio < 0.90", "",
          b3["n"], "")
    b_row("B05", "share_below_0.90_lag3", b3["frac_below"], "2/3",
          ">= 2/3 of observed pairs -> GATE-LOSS", "", b3["n"], "")
    b_row("B06", "test_B_verdict", b3["verdict"], "", "frozen Test B bars",
          b3["verdict"], b3["n"],
          "declared 3-year lag; +/-1 y nearest observation")
    b_row("B07", "n_pairs_lag2", b2["n"], "n", "lag-2 sensitivity", "", b2["n"],
          "sensitivity only, not verdict-changing")
    b_row("B08", "share_in_band_lag2", b2["frac_in"], "2/3",
          "lag-2 sensitivity, not verdict-changing", b2["verdict"], b2["n"],
          "sensitivity only")
    b_row("B09", "n_pairs_lag4", b4["n"], "n", "lag-4 sensitivity", "", b4["n"],
          "sensitivity only, not verdict-changing")
    b_row("B10", "share_in_band_lag4", b4["frac_in"], "2/3",
          "lag-4 sensitivity, not verdict-changing", b4["verdict"], b4["n"],
          "sensitivity only")
    b_row("B11", "n_pairs_lag3_unbounded", b3_unb["n"], "n",
          "nearest lower observation at any distance", "", b3_unb["n"],
          "sensitivity only: no pair dropped")
    b_row("B12", "share_in_band_lag3_unbounded", b3_unb["frac_in"], "2/3",
          "sensitivity, not verdict-changing", b3_unb["verdict"], b3_unb["n"],
          "sensitivity only")

    res_rows.append(dict(
        test="overall", row_id="O01", variant="ceil_attrib", switch="",
        statistic="ceil_attrib_decision", value=overall, unit="verdict",
        threshold="", threshold_rule="declared ordered matrix rule (PRE_DECLARATIONS 7)",
        verdict=overall, component_account=overall, n="",
        label="OBSERVED",
        note=("overall decision token (Test B observed residual; the Test A component "
              "is SYNTHETIC and is MIXED, see rows A*). Matrix (a): residual "
              "reclassified as lower-pipeline inheritance; D63 stays UNABLE as to cause"
              if overall == "PIPELINE-CONSISTENT"
              else "overall decision token; see FINDINGS.md for the matrix cell reached")))

    write_csv(outdir / "CEIL_ATTRIB_RESULTS.csv", RES_COLS, res_rows)

    # ==================================================================================
    # write CEIL_ATTRIB_DETAIL.csv (per-year series)
    # ==================================================================================
    DET_COLS = ["series", "label", "year", "upper_uis", "upper_cohort_flow",
                "lower_uis", "lower_cohort_flow", "upper_ger", "demand_share_upper",
                "quality_upper", "seat_coverage_upper", "observed_upper",
                "observed_lower", "lower_year_used_lag3", "ratio_lag3", "in_band_lag3"]
    det_rows = list(details)
    # observed series rows (one row per observed year, either series)
    for y in sorted(set(upper_obs) | set(lower_obs)):
        det_rows.append(dict(
            series="PHL_observed_completion", label="OBSERVED", year=y,
            observed_upper=upper_obs.get(y, ""),
            observed_lower=lower_obs.get(y, "")))
    # observed pair rows
    for p in pairs3:
        det_rows.append(dict(
            series="PHL_pair_lag3", label="OBSERVED", year=p["upper_year"],
            observed_upper=p["upper"], observed_lower=p["lower"],
            lower_year_used_lag3=p["lower_year"], ratio_lag3=p["ratio"],
            in_band_lag3=(1 if BAND_LO <= p["ratio"] <= BAND_HI else 0)))
    write_csv(outdir / "CEIL_ATTRIB_DETAIL.csv", DET_COLS, det_rows)

    # ==================================================================================
    # write ABLATION_PANEL.csv (2024 upper completion + key series per ablation)
    # ==================================================================================
    ABL_COLS = (["variant", "role", "switch", "upper_uis_2024", "upper_cohort_2024",
                 "lower_uis_2024", "delta_upper_uis_2024_pp", "upper_uis_max_le_2024",
                 "first_year_upper_uis_ge90", "upper_ger_2024", "upper_demand_share_2024",
                 "upper_quality_2024", "upper_seat_coverage_2024", "m", "gamma",
                 "seat_t50_upper"]
                + [f"upper_uis_{y}" for y in range(2015, 2026)])
    abl_rows = []
    for switch, role, desc in VARIANTS:
        v = var[switch]
        row = dict(
            variant=switch, role=role, switch=desc,
            upper_uis_2024=v["upper24"],
            upper_cohort_2024=v["upper_cohort24"],
            lower_uis_2024=v["lower24"],
            delta_upper_uis_2024_pp=delta[switch],
            upper_uis_max_le_2024=v["upper_max"],
            first_year_upper_uis_ge90=(v["first_ge90"] if v["first_ge90"] else "never"),
            upper_ger_2024=v["ger24"], upper_demand_share_2024=v["demand24"],
            upper_quality_2024=v["quality24"],
            upper_seat_coverage_2024=v["seatcov24"],
            m=(1.05 if switch == "m1.05" else 1.12 if switch == "m1.12" else 1.10),
            gamma=(0.0 if switch == "gamma0" else 0.55),
            seat_t50_upper=(2010.0 - 5 if switch in ("buildout_m5", "upper_only_m5")
                            else 2010.0 + 5 if switch in ("buildout_p5", "upper_only_p5")
                            else 2010.0),
        )
        row.update({f"upper_uis_{y}": v["upper_series"][y] for y in range(2015, 2026)})
        abl_rows.append(row)
    # fill cohort-flow 2024 is carried directly in each row above
    write_csv(outdir / "ABLATION_PANEL.csv", ABL_COLS, abl_rows)

    # ==================================================================================
    # evidence json
    # ==================================================================================
    uni_sha = sha256_file(uni_path)
    wdi = mod.PROG / "09_relations" / "data" / "panel_wdi_long.csv"
    evidence = {
        "label": "SYNTHETIC (generator) + OBSERVED (PHL UIS series)",
        "experiment": "EXP-1 CEIL-ATTRIB",
        "predeclaration_sha256": got_pre,
        "predeclaration_sha_matches_recorded": bool(
            recorded is None or got_pre == recorded),
        "frozen_objects": {
            "code_sha256": FROZEN_CODE_SHA,
            "params_sha256": FROZEN_PARAMS_SHA,
            "panel_sha256": FROZEN_PANEL_SHA,
            "v12_spec_sha256": V12_SPEC_SHA,
            "v12_manifest_sha256": FROZEN_MANIFEST_SHA,
        },
        "copies": checks,
        "copies_byte_identical": {k: checks[k] == expect[k] for k in checks},
        "baseline_invariance": {
            "required": ("unmodified copy reproduces results/synthetic_panel_v1_2.csv "
                         "byte-for-byte"),
            "panel_sha256": base_panel_sha,
            "frozen_panel_sha256": FROZEN_PANEL_SHA,
            "byte_identical": invariance_ok,
            "driver_baseline_panel_sha256": driver_panel_sha,
            "driver_baseline_byte_identical": driver_matches_module,
            "resolved": invariance_ok and driver_matches_module,
        },
        "inputs": {
            "UNIVERSALIZATION_SERIES.csv": uni_sha,
            "panel_wdi_long.csv": sha256_file(wdi),
        },
        "variants": {k: {"role": var[k]["role"], "switch": var[k]["desc"],
                         "upper_uis_2024": var[k]["upper24"],
                         "delta_pp": delta[k]} for k in var},
        "test_A": {
            "baseline_upper_uis_2024": base24,
            "mech_hits": mech_hits,
            "calib_absmax_pp": calib_absmax,
            "calib_ge_2pp": calib_ge2,
            "calib_all_lt_1pp": calib_lt1,
            "mech_all_lt_2pp": mech_lt2,
            "verdict": test_a,
        },
        "test_B": {
            "declared_lag": LAG, "tol_years": TOL,
            "lag3": b3, "lag2": b2, "lag4": b4, "lag3_unbounded": b3_unb,
            "pairs_lag3": pairs3,
        },
        "overall_decision": overall,
        "no_writes_outside_experiment_dir": True,
        "rng": ("frozen generator's single seeded PCG64 stream (seed 20261120), fixed "
                "draw order, identical across variants; driver adds no RNG"),
        "python": platform.python_version(),
        "numpy": np.__version__,
    }
    (outdir / "EVIDENCE.json").write_text(json.dumps(evidence, indent=2) + "\n")

    # console summary
    print(f"[ceil_attrib] baseline invariance byte-identical = {invariance_ok}")
    print(f"[ceil_attrib] baseline SYN00 upper UIS {YEAR} = {base24:.4f} pp")
    for k in ("gamma0", "work_off", "flat_cohort", "m1.05", "m1.12",
              "buildout_m5", "buildout_p5"):
        print(f"  {k:12s} upper {YEAR} = {var[k]['upper24']:8.4f}  "
              f"delta = {delta[k]:+7.4f} pp")
    print(f"[ceil_attrib] Test A = {test_a} (mech_hits={mech_hits}, "
          f"calib_absmax={calib_absmax:.4f}, calib_lt1={calib_lt1})")
    print(f"[ceil_attrib] Test B lag3 = {b3['verdict']} "
          f"({b3['inband']}/{b3['n']} in band, {b3['below']} below 0.90)")
    print(f"[ceil_attrib] OVERALL = {overall}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
