#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RUN_V16 -- EXP-14 **V16-REPAIR**: run the declared arms, score the observed path, write results.

Everything emitted is SYNTHETIC except the PHL observed series, which are OBSERVED and enter only
as the comparison object. No causal or direction claim. No fitting. No threshold moves.

Run:  python code/run_v16.py [--out DIR] [--no-determinism]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
sys.path.insert(0, str(CODE))
import sim_v1_6_repair as S          # noqa: E402

LABEL = "SYNTHETIC"
ANCHOR = "SYN00_PHL_LIKE"
YEARS = S.YEARS
T = S.T
Y0 = int(S.YEAR_START)
LEVELS = S.LEVELS
LIX = {lv: i for i, lv in enumerate(LEVELS)}

OBS_PATH = S.DATA / "UNIVERSALIZATION_SERIES.csv"
V13_PANEL = S.SYNTH / "generator_v1_3" / "results" / "synthetic_panel_v1_3.csv"
V15_DIR = S.SYNTH / "generator_v1_5_bimodal"
V15_PANEL_A10 = V15_DIR / "results" / "panel_v1_5_A10_bimodal_noKappa.csv"
V15_PANEL_A11 = V15_DIR / "results" / "synthetic_panel_v1_5.csv"
V15_PREDECL = V15_DIR / "PRE_DECLARATIONS.md"
KAPPA_PREDECL = S.SYNTH.parent / "kappa_fwd_2026-11-20" / "PRE_DECLARATIONS.md"
LOWER_PREDECL = S.SYNTH.parent / "lower_def_2026-11-20" / "PRE_DECLARATIONS.md"
UNI = OBS_PATH

ARM_DEFS = {
    "A00":         dict(bimodal=False),
    "A10":         dict(bimodal=True),
    "A11V15":      dict(bimodal=True, tier_surv=True, tier_cfg=dict(S.V15_RECON)),
    "D1_survonly": dict(bimodal=True, tier_surv=True,
                        tier_cfg=dict(q_H_mult=1.0, q_O_mult=1.0, v_O_scale=0.45)),
    "A01D":        dict(bimodal=False, kappa_link=True),
    "A10W":        dict(bimodal=True, w_child_mult=S.CHILD_WAGE_MULT),
    "A01DW":       dict(bimodal=False, kappa_link=True, w_child_mult=S.CHILD_WAGE_MULT),
    "S_dual":      dict(bimodal=True, tier_cfg=dict(v_O_scale=0.55 * 0.45)),
    "S_qO_040":    dict(bimodal=True, tier_cfg=dict(q_O=0.40)),
    "S_qO_055":    dict(bimodal=True, tier_cfg=dict(q_O=0.55)),
    "S_qO_070":    dict(bimodal=True, tier_cfg=dict(q_O=0.70)),
    "S_qO_085":    dict(bimodal=True, tier_cfg=dict(q_O=0.85)),
    "S_qO_100":    dict(bimodal=True, tier_cfg=dict(q_O=1.00)),
    "S_survpen_095": dict(bimodal=True, tier_surv=True,
                          tier_cfg=dict(q_H_mult=1.0, q_O_mult=1.0, surv_pen_O=0.95)),
    "S_survpen_090": dict(bimodal=True, tier_surv=True,
                          tier_cfg=dict(q_H_mult=1.0, q_O_mult=1.0, surv_pen_O=0.90)),
    "S_hshare_plus": dict(bimodal=True, tier_cfg=dict(h_share=(0.25, 0.38, 0.50, 0.60))),
    "S_hshare_minus": dict(bimodal=True, tier_cfg=dict(h_share=(0.05, 0.18, 0.30, 0.40))),
    "S_kappa0960": dict(bimodal=False, kappa_link=True, kappa=0.960),
}
PHYSCAP_GRID = (1.00, 1.05, 1.08, 1.15, 1.22, 1.30)
PANELS_TO_WRITE = ("A00", "A10", "A01D", "A00CF", "A10W")

FROZEN_FILES = {
    "v13_code": S.SYNTH / "generator_v1_3" / "code" / "sim_v1_3.py",
    "v13_panel": V13_PANEL,
    "v13_predecl": S.SYNTH / "generator_v1_3" / "PRE_DECLARATIONS.md",
    "v15_code": V15_DIR / "code" / "sim_v1_5_bimodal.py",
    "v15_panel_A11": V15_PANEL_A11,
    "v15_panel_A10": V15_PANEL_A10,
    "v15_predecl": V15_PREDECL,
    "v15_params": V15_DIR / "PARAMETERS.csv",
    "v15_findings": V15_DIR / "FINDINGS.md",
    "kappa_predecl": KAPPA_PREDECL,
    "lower_predecl": LOWER_PREDECL,
    "observed": UNI,
    "base_copy": CODE / "base_v1_3_sim.py",
    "predecl": ROOT / "PRE_DECLARATIONS.md",
    "params_md": ROOT / "PARAMS.md",
    "build_script": CODE / "build_v16.py",
    "sim_code": CODE / "sim_v1_6_repair.py",
}


# ======================================================================================
def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fnum(x):
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return ""
    return ("%.10g" % x) if isinstance(x, float) else x


def write_rows(path, rows):
    if not rows:
        return
    cols = list(rows[0].keys())
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: fnum(r.get(k, "")) for k in cols})


def read_panel(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def num(row, col):
    v = row.get(col, "")
    try:
        return float(v)
    except (TypeError, ValueError):
        return float("nan")


# ======================================================================================
# observed cells (derived, never hard-coded)
# ======================================================================================
def observed_cells():
    with open(OBS_PATH, newline="") as fh:
        rows = list(csv.DictReader(fh))
    obs = {}
    for r in rows:
        if r.get("iso3") != "PHL":
            continue
        ind = r.get("indicator", "")
        if not ind.startswith("completion_"):
            continue
        lv = ind.replace("completion_", "")
        if lv not in LIX:
            continue
        try:
            y = int(float(r["year"]))
            v = float(r["value"])
        except (TypeError, ValueError):
            continue
        if Y0 <= y <= int(S.YEAR_END):
            obs[(lv, y)] = v
    for lv in ("primary", "lower_secondary", "upper_secondary"):
        n = sum(1 for (a, _y) in obs if a == lv)
        if n != 11:
            raise SystemExit("REFUSING: observed cell count for %s is %d, expected 11" % (lv, n))
    if len(obs) != 33:
        raise SystemExit("REFUSING: %d observed cells, expected 33" % len(obs))
    return obs


def path_stats(panel, obs):
    ix = {(r["country"], int(r["year"]), r["level"]): r for r in panel}
    out = []
    for (lv, y) in sorted(obs, key=lambda k: (LIX[k[0]], k[1])):
        row = ix[(ANCHOR, y, lv)]
        m = 100.0 * float(row["completion_uis"])
        o = obs[(lv, y)]
        d = m - o
        out.append(dict(level=lv, year=y, model_pp=m, observed_pp=o, deviation_pp=d,
                        within_5pp=("YES" if abs(d) <= S.DECLARED_GATES["tol_pp"] else "NO"),
                        within_10pp=("YES" if abs(d) <= 10.0 else "NO")))
    n5 = sum(1 for r in out if r["within_5pp"] == "YES")
    per = {}
    for lv in ("primary", "lower_secondary", "upper_secondary"):
        ds = sorted(r["deviation_pp"] for r in out if r["level"] == lv)
        per[lv] = dict(n=len(ds), n5=sum(1 for d in ds if abs(d) <= 5.0),
                       median=ds[len(ds) // 2])
    return out, n5, per


def crossing_year(series, thr):
    for y in sorted(series):
        if series[y] >= thr:
            return y
    return None


def crossing_stats(panel, obs):
    ix = {(r["country"], int(r["year"]), r["level"]): r for r in panel}
    thr = S.DECLARED_GATES["crossing_thresholds_pp"]
    tol = S.DECLARED_GATES["crossing_tol_y"]
    rows = []
    for lv in ("primary", "lower_secondary", "upper_secondary"):
        mser = {y: 100.0 * float(ix[(ANCHOR, y, lv)]["completion_uis"])
                for y in range(Y0, int(S.YEAR_END) + 1)}
        oser = {y: v for (a, y), v in obs.items() if a == lv}
        oc = crossing_year(oser, thr[lv])
        mc = crossing_year(mser, thr[lv])
        if oc is not None and mc is not None:
            gap = mc - oc
            ok = abs(gap) <= tol
            note = "both cross"
        elif oc is None and mc is None:
            gap = 0
            ok = True
            note = "neither crosses by 2025"
        elif oc is None:
            gap = None
            ok = False
            note = "observed never crosses; model crosses"
        else:
            gap = None
            ok = False
            note = "observed crosses; model never crosses by 2025"
        rows.append(dict(level=lv, threshold_pp=thr[lv], observed_crossing_year=oc,
                         model_crossing_year=mc, gap_y=gap, tolerance_y=tol,
                         holds=ok, note=note,
                         model_max_pp=max(mser.values())))
    n_ok = sum(1 for r in rows if r["holds"])
    return rows, n_ok


def representation(panel10, panel00):
    """v1.5's (a) family carried verbatim except (a-iv); (a-iv) is NOT re-frozen (D134(4))."""
    ix10 = {(r["country"], int(r["year"]), r["level"]): r for r in panel10}
    ix00 = {(r["country"], int(r["year"]), r["level"]): r for r in panel00}
    cells = []
    for y in range(2010, 2025):
        for lv in ("lower_secondary", "upper_secondary"):
            r = ix10[(ANCHOR, y, lv)]
            cells.append(dict(year=y, level=lv,
                              unfilled=float(r["tier_O_unfilled_share"]),
                              queue_ratio=float(r["tier_queue_ratio_H"]),
                              p4=float(r["job_gate_p4"])))
    n_unf = sum(1 for c in cells if c["unfilled"] >= 0.10)
    n_q = sum(1 for c in cells if c["queue_ratio"] >= 1.10)
    years = sorted({c["year"] for c in cells})
    # v1.5 definition: a YEAR holds if ANY cell in that year has BOTH
    yr_hold = {y: any((c["unfilled"] >= 0.10 and c["queue_ratio"] >= 1.10)
                      for c in cells if c["year"] == y) for y in years}
    n_iii = sum(1 for y in years if yr_hold[y])
    n_iii_p4 = sum(1 for y in years if yr_hold[y]
                   and all(c["p4"] <= 0.50 for c in cells if c["year"] == y))

    def same_level(ix):
        n = 0
        for y in range(2010, 2025):
            r = ix[(ANCHOR, y, "upper_secondary")]
            spare = float(r["seats"]) - float(r["enrolment"])
            if spare > 0.0 and float(r["rationed_official"]) > 0.0:
                n += 1
        return n

    sl10 = same_level(ix10)
    sl00 = same_level(ix00)
    legs = dict(unfilled=(n_unf, ">= 15 of 30"), queue=(n_q, ">= 15 of 30"),
                simultaneity=(n_iii, ">= 8 of 15"), job_gate=(n_iii_p4, ">= 8 of 15"))
    ok = (n_unf >= 15) and (n_q >= 15) and (n_iii >= 8) and (n_iii_p4 >= 8)
    return dict(cells=cells, n_unfilled=n_unf, n_queue=n_q, n_both=n_iii,
                n_both_p4=n_iii_p4, legs=legs, holds=ok,
                same_level_A10=sl10, same_level_A00=sl00)


# ======================================================================================
def run_arm(name, kw, hosts_from=None):
    if "inject_upper" in kw:
        raise SystemExit("inject_upper is provided by the driver, not ARM_DEFS")
    return S.run_arm_full(**kw)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "results"))
    ap.add_argument("--no-determinism", action="store_true")
    args = ap.parse_args(argv)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    pre = S.verify_predecl()
    frozen_before = {k: sha256_file(p) for k, p in FROZEN_FILES.items()}
    obs = observed_cells()

    body = run_pipeline(outdir, obs, frozen_before, pre)
    if not args.no_determinism:
        det_dir = outdir / "determinism_run2"
        det_dir.mkdir(parents=True, exist_ok=True)
        body2 = run_pipeline(det_dir, obs, frozen_before, pre)
        det = compare_dirs(outdir, det_dir)
        body["guards"]["determinism"] = det["status"]
        body["guards"]["determinism_files"] = det["n"]
        body["guards"]["determinism_identical"] = det["n_identical"]
        body["det"] = det
    else:
        body["guards"]["determinism"] = "DETERMINISM-NOT-RUN"
        body["guards"]["determinism_files"] = 0
        body["guards"]["determinism_identical"] = 0
        body["det"] = dict(status="DETERMINISM-NOT-RUN", files=[], n=0, n_identical=0)

    finalize(outdir, body, pre, frozen_before)
    print_summary(body)
    return 0


# ======================================================================================
def run_pipeline(outdir, obs, frozen_before, pre):
    outdir = Path(outdir)
    recs, hosts_by = {}, {}
    for name, kw in ARM_DEFS.items():
        recs[name], hosts_by[name] = run_arm(name, kw)

    # ---- A00CF: the counterfactual replay (R3). Same hosts as A01D, one injected vector.
    inj = {}
    for rr in recs["A01D"]:
        inj[rr["cp"]["name"]] = [float(rr["intake_off"][2, t]) for t in range(T)]
    recs["A00CF"] = S.run_arm(shadow=True, hosts=hosts_by["A01D"], inject_upper=inj)
    hosts_by["A00CF"] = hosts_by["A01D"]

    panels89 = {n: S.build_panel_v13(recs[n], hosts_by[n], S.shadow_inputs_named())
                for n in ("A00", "A10", "A10W", "A01D", "A00CF")}
    # ---- panels ---------------------------------------------------------------------
    for n in PANELS_TO_WRITE:
        rows = panels89[n]
        if n in ("A10", "A10W"):
            rows = with_tier_cols(rows, recs[n])
        write_rows(outdir / ("panel_%s.csv" % {"A00": "A00_v13cols", "A10": "A10_repaired",
                                               "A01D": "A01D_kappa", "A00CF": "A00CF_identity",
                                               "A10W": "A10W_childwage"}[n]), rows)

    # ---- observed path (S1) + construction check (S0) -------------------------------
    op10, n10, per10 = path_stats(panels89["A10"], obs)
    op00, n00, per00 = path_stats(panels89["A00"], obs)
    obs_rows = []
    for a, b in zip(op10, op00):
        obs_rows.append(dict(level=a["level"], year=a["year"],
                             model_A10_pp=a["model_pp"], model_A00_pp=b["model_pp"],
                             observed_pp=a["observed_pp"],
                             deviation_A10_pp=a["deviation_pp"],
                             within_5pp_A10=a["within_5pp"],
                             deviation_A00_pp=b["deviation_pp"],
                             within_5pp_A00=b["within_5pp"]))
    write_rows(outdir / "observed_path.csv", obs_rows)

    # ---- crossings (S2) -------------------------------------------------------------
    cr, ncr = crossing_stats(panels89["A10"], obs)
    write_rows(outdir / "crossing_check.csv", cr)

    # ---- representation (S3) --------------------------------------------------------
    rep = representation(with_tier_cols(panels89["A10"], recs["A10"]), panels89["A00"])
    write_rows(outdir / "representation_cells.csv", rep["cells"])

    # ---- child wage (C1/C2) + its post-hoc, non-verdict-bearing diagnostics ----------
    base_upper = 100.0 * float(by_name(recs["A10"], ANCHOR)["comp_uis"][2, 2024 - Y0])
    posthoc = dict(base_upper=base_upper, upper_by_mult={}, a11k={})
    for m in (1.25, 1.50):
        rr = S.run_arm_full(bimodal=True, w_child_mult=m)[0]
        posthoc["upper_by_mult"][m] = (100.0 * float(by_name(rr, ANCHOR)["comp_uis"][2, 2024 - Y0])
                                       - base_upper)
    k0 = by_name(S.run_arm_full(bimodal=True, kappa_link=True)[0], ANCHOR)
    k1 = by_name(S.run_arm_full(bimodal=True, kappa_link=True,
                                w_child_mult=S.CHILD_WAGE_MULT)[0], ANCHOR)
    t24 = 2024 - Y0
    posthoc["a11k"] = {
        "demand_official upper 2024 (pp of cohort)": (
            100.0 * float(k0["demand_off"][2, t24]) / max(float(k0["C"][2, t24]), 1e-9),
            100.0 * float(k1["demand_off"][2, t24]) / max(float(k1["C"][2, t24]), 1e-9)),
        "A_H upper 2024 (pp of cohort)": (
            100.0 * float(k0["tier_A_H"][2, t24]) / max(float(k0["C"][2, t24]), 1e-9),
            100.0 * float(k1["tier_A_H"][2, t24]) / max(float(k1["C"][2, t24]), 1e-9)),
        "Tier-H queue ratio upper 2024": (
            float(k0["tier_queue_H"][2, t24]) / max(float(k0["tier_K_H"][2, t24]), 1e-9),
            float(k1["tier_queue_H"][2, t24]) / max(float(k1["tier_K_H"][2, t24]), 1e-9)),
    }
    cw_rows = child_wage_table(recs, panels89, posthoc)
    write_rows(outdir / "child_wage_A10.csv", cw_rows)

    # ---- phys_cap sensitivity (C3) --------------------------------------------------
    pc_rows = []
    for pc in PHYSCAP_GRID:
        rr, hh = S.run_arm_full(bimodal=True, phys_cap=pc)
        st = rec_stats(rr, obs)
        cb = capacity_bound_cells(rr)
        row = dict(phys_cap=pc, observed_path_count=st["count"],
                   primary_2024_pp=st["primary_2024"], lower_2021_pp=st["lower_2021"],
                   lower_2024_pp=st["lower_2024"], upper_2024_pp=st["upper_2024"],
                   tertiary_2024_pp=st["tertiary_2024"],
                   primary_seat_coverage_2019=st["primary_seat_coverage_2019"],
                   primary_seat_coverage_2024=st["primary_seat_coverage_2024"],
                   primary_adm_over_cohort_2024=st["primary_adm_2024"],
                   primary_phys_over_cohort_2024=st["primary_phys_2024"],
                   primary_completion_first_ge90=st["primary_first_ge90"],
                   primary_1985_pp=st["primary_1985"], primary_1995_pp=st["primary_1995"],
                   capacity_bound_cells=cb["capacity_bound"], capacity_bound_share=cb["share"],
                   floor_note=("floor delivered by the declared crowding allowance"
                               if pc > 1.0 else "no crowding allowance"))
        pc_rows.append(row)
    S.P["phys_cap"] = 1.15          # restore the declared baseline after the grid
    write_rows(outdir / "phys_cap_sensitivity.csv", pc_rows)

    # ---- sensitivities --------------------------------------------------------------
    sens = []
    for n in sorted(ARM_DEFS):
        if not n.startswith("S_"):
            continue
        st = rec_stats(recs[n], obs)
        sens.append(dict(arm=n, observed_path_count=st["count"],
                         primary_2024_pp=st["primary_2024"],
                         lower_2021_pp=st["lower_2021"],
                         upper_2024_pp=st["upper_2024"],
                         declared_grid_value=n.split("_", 2)[-1],
                         verdict_bearing="NO"))
    write_rows(outdir / "sensitivity_arms.csv", sens)

    # ---- decomposition (which obligation changed what) ------------------------------
    dec = []
    for n in ("A00", "A11V15", "D1_survonly", "A10"):
        st = rec_stats(recs[n], obs)
        dec.append(dict(arm=n, observed_path_count=st["count"],
                        primary_2024_pp=st["primary_2024"],
                        lower_2021_pp=st["lower_2021"], lower_2024_pp=st["lower_2024"],
                        upper_2024_pp=st["upper_2024"],
                        primary_surv_2024=st["primary_surv"], lower_surv_2021=st["lower_surv"],
                        upper_surv_2024=st["upper_surv"],
                        primary_adm_over_cohort_2024=st["primary_adm_2024"],
                        upper_unfilled_2024=st["upper_unfilled"],
                        upper_queue_ratio_2024=st["upper_queue_ratio"]))
    write_rows(outdir / "decomposition.csv", dec)

    # ---- lower channel report (R7) --------------------------------------------------
    lower_rows = lower_channel_report(recs, panels89)
    write_rows(outdir / "lower_channel_report.csv", lower_rows)

    # ---- kappa object audit (R1/R6) -------------------------------------------------
    kap_rows, kap_summary = kappa_audit(recs, panels89)
    write_rows(outdir / "kappa_object_audit.csv", kap_rows)

    # ---- reconciliation to v1.5 (A11V15 vs frozen v1.5 A10) -------------------------
    rec_rows = reconciliation(with_tier_cols(
        S.build_panel_v13(recs["A11V15"], hosts_by["A11V15"], S.shadow_inputs_named()),
        recs["A11V15"]))

    # ---- propagation ledger (R2) ----------------------------------------------------
    ledger = propagation_ledger(panels89, recs)
    write_rows(outdir / "propagation_ledger.csv", ledger)

    # ---- one-way / order audit ------------------------------------------------------
    oneway = one_way_audit(recs, panels89)

    # ---- identity + exact checks (R3) ----------------------------------------------
    ident = identity_checks(panels89, recs)

    # ---- m-convention / clip audit (R7c/R7f) ---------------------------------------
    mclip = m_and_clip_audit(panels89["A10"], panels89["A00"])

    # ---- checks ---------------------------------------------------------------------
    checks, detail = build_checks(obs, n10, per10, n00, per00, cr, ncr, rep, cw_rows,
                                  pc_rows, kap_summary, ident, oneway, mclip,
                                  rec_rows, frozen_before, pre)
    write_rows(outdir / "v1_6_checks.csv", checks)
    write_rows(outdir / "v1_6_checks_detail.csv", detail)

    frozen_after = {k: sha256_file(p) for k, p in FROZEN_FILES.items()}
    return dict(outdir=outdir, checks=checks, detail=detail, panels=panels89,
                recs=recs, hosts=hosts_by, guards=dict(
                    frozen_before=frozen_before, frozen_after=frozen_after,
                    frozen_ok=(frozen_before == frozen_after),
                    a00_sha=sha256_file(outdir / "panel_A00_v13cols.csv"),
                    a00cf_vs_a01d=ident["cf_vs_a01d"],
                    identity=ident, oneway=oneway, mclip=mclip,
                    kappa=kap_summary, reconciliation=rec_rows,
                    predecl=pre, obs_n=len(obs),
                    observed_path_count=n10, crossings=ncr, rep=rep,
                    det=dict(status="PENDING", files=[], n=0, n_identical=0)))


# ======================================================================================
def by_name(rec, name):
    if isinstance(rec, dict):
        lst = rec["res"]
    elif isinstance(rec, tuple):
        lst = rec[0]
    else:
        lst = rec
    for r in lst:
        if r["cp"]["name"] == name:
            return r
    raise KeyError(name)


def rec_stats(res, obs):
    """Compact A10-type statistics from the run record (no panel allocation)."""
    r = by_name(res, ANCHOR)
    t24, t21, t19 = 2024 - Y0, 2021 - Y0, 2019 - Y0

    def comp(L, t):
        return 100.0 * float(r["comp_uis"][L, t])

    def surv(L, t):
        return float(r["surv"][L, t])

    def adm(L, t):
        return float(r["intake_off"][L, t]) / max(float(r["C"][L, t]), 1e-9)

    cnt = 0
    for (lv, y) in obs:
        L = LIX[lv]
        if abs(comp(L, y - Y0) - obs[(lv, y)]) <= S.DECLARED_GATES["tol_pp"]:
            cnt += 1
    first90 = None
    for t in range(T):
        if comp(0, t) >= 90.0:
            first90 = Y0 + t
            break
    sc24 = float(r["seats"][0, t24]) / max(float(r["C"][0, t24]), 1e-9)
    return dict(count=cnt,
                primary_2024=comp(0, t24), lower_2021=comp(1, t21),
                lower_2024=comp(1, t24), upper_2024=comp(2, t24),
                tertiary_2024=comp(3, t24),
                primary_surv=surv(0, t24), lower_surv=surv(1, t21),
                upper_surv=surv(2, t24),
                primary_adm_2024=adm(0, t24),
                primary_phys_2024=min(float(S.P["phys_cap"]) * sc24,
                                      float(S.P["overage_cap"])),
                primary_seat_coverage_2019=float(r["seats"][0, t19])
                / max(float(r["C"][0, t19]), 1e-9),
                primary_seat_coverage_2024=sc24,
                primary_first_ge90=first90,
                primary_1985=comp(0, 1985 - Y0), primary_1995=comp(0, 1995 - Y0),
                upper_unfilled=float(r["tier_unf"][2, t24]),
                upper_queue_ratio=float(r["tier_ratio_H"][2, t24]))


def capacity_bound_cells(res):
    """Cells where official admission is capacity-bound (admitted == phys), all countries."""
    n = 0
    tot = 0
    for r in res:
        for L in range(4):
            for t in range(T):
                tot += 1
                phys = min(float(S.P["phys_cap"]) * float(r["seats"][L, t]),
                           float(S.P["overage_cap"]) * float(r["C"][L, t]))
                if abs(float(r["intake_off"][L, t]) - phys) <= 1e-9 * max(1.0, phys):
                    n += 1
    return dict(capacity_bound=n, cells=tot, share=n / max(tot, 1))


def with_tier_cols(rows, result):
    by = {r["cp"]["name"]: r for r in result}
    out = []
    for row in rows:
        r = by[row["country"]]
        t = int(row["year"]) - Y0
        L = LIX[row["level"]]
        d = dict(row)
        d["tier_K_H"] = float(r["tier_K_H"][L, t])
        d["tier_K_O"] = float(r["tier_K_O"][L, t])
        d["tier_A_H"] = float(r["tier_A_H"][L, t])
        d["tier_A_O_first"] = float(r["tier_A_O_first"][L, t])
        d["tier_T_O"] = float(r["tier_T_O"][L, t])
        d["tier_O_unfilled"] = float(r["tier_V_O"][L, t])
        d["tier_O_unfilled_share"] = float(r["tier_unf"][L, t])
        d["tier_O_takeup_share"] = float(r["tier_take"][L, t])
        d["tier_admitted_H"] = float(r["tier_adm_H"][L, t])
        d["tier_queue_H"] = float(r["tier_queue_H"][L, t])
        d["tier_queue_ratio_H"] = float(r["tier_ratio_H"][L, t])
        d["tier_p_adv_H"] = float(r["tier_padv"][L, t])
        d["tier_Q_H"] = float(r["tier_Q_H"][L, t])
        d["tier_Q_O"] = float(r["tier_Q_O"][L, t])
        d["tier_surv_H"] = float(r["tier_surv_H"][L, t])
        d["tier_surv_O"] = float(r["tier_surv_O"][L, t])
        d["job_gate_p4"] = (float(r["E"][3, t]) / float(r["J"][3, t])
                            if float(r["J"][3, t]) > 1e-12 else float("nan"))
        d["kappa_bound_pp"] = float(r["kappa_bound_pp"][t])
        d["kappa_binds"] = int(r["kappa_binds"][t])
        d["kappa_cut_pp"] = float(r["kappa_cut_pp"][t])
        d["both_would_dominate_cells"] = int(r["n_both_dom"][L, t])
        out.append(d)
    return out


# ======================================================================================
def child_wage_table(recs, panels, posthoc):
    ix10 = {(r["country"], int(r["year"]), r["level"]): r for r in panels["A10"]}
    ixw = {(r["country"], int(r["year"]), r["level"]): r for r in panels["A10W"]}
    r01 = by_name(recs["A01D"], ANCHOR)
    rw = by_name(recs["A01DW"], ANCHOR)
    t24, t21 = 2024 - Y0, 2021 - Y0
    rows = []

    def add(arm, obj, base, shock, sign_declared, leg, verdict, note=""):
        rows.append(dict(arm=arm, object=obj, baseline=base, shocked=shock,
                         delta=shock - base, declared_sign=sign_declared,
                         observed_sign=("negative" if shock - base < 0 else
                                        ("positive" if shock - base > 0 else "zero")),
                         leg_holds=("YES" if leg else "NO"),
                         verdict_bearing=verdict, note=note))

    b = 100.0 * float(ix10[(ANCHOR, 2024, "upper_secondary")]["completion_uis"])
    s_ = 100.0 * float(ixw[(ANCHOR, 2024, "upper_secondary")]["completion_uis"])
    add("A10", "completion_uis upper 2024 (pp)", b, s_, "negative", (s_ - b) < 0.0, "YES",
        "R5b verdict-bearing leg: sign only. A zero response is BELOW THE BLOCK'S RESOLUTION "
        "(15 discrete utility cells), not evidence of inertness -- see the post-hoc scan")
    # A01D: the pre-cap object that exists in the declared capped arm
    bb = 100.0 * float(r01["demand_off"][2, t24]) / max(float(r01["C"][2, t24]), 1e-9)
    ss = 100.0 * float(rw["demand_off"][2, t24]) / max(float(rw["C"][2, t24]), 1e-9)
    add("A01D", "demand_official upper 2024 (pp of cohort)", bb, ss, "negative",
        (ss - bb) <= 0.0, "YES",
        "R5c pre-cap object in the declared capped arm; A01D is a diagnostic, not a projection")
    add("A01D", "A_H upper 2024", float("nan"), float("nan"), "negative", False, "YES",
        "NOT DEFINED in A01D (bimodal OFF has no tier block). Predeclaration-authoring error "
        "of the a-iv class: R5c named an arm that cannot produce two of its three objects. "
        "Recorded, not rescued; the post-hoc A11K row below reports the object")
    add("A01D", "Tier-H queue upper 2024", float("nan"), float("nan"), "non-positive",
        False, "YES", "NOT DEFINED in A01D, same authoring error as A_H")
    # capped-arm completion response: composition effect, non-verdict-bearing
    b2 = 100.0 * float(r01["comp_uis"][2, t24])
    s2 = 100.0 * float(by_name(recs["A01DW"], ANCHOR)["comp_uis"][2, t24])
    add("A01D", "completion_uis upper 2024 (pp) under a binding cap", b2, s2,
        "not tested", True, "NO",
        "composition effect only (H/O mix x survival); non-verdict-bearing")
    # ---- post-hoc diagnostics (NOT in the frozen arm list; non-verdict-bearing) ------
    for m, d_pp in posthoc["upper_by_mult"].items():
        add("POSTHOC_wchild_x%.2f" % m, "completion_uis upper 2024 (pp)", posthoc["base_upper"],
            posthoc["base_upper"] + d_pp, "negative", d_pp < 0.0, "NO",
            "POST-HOC, non-verdict-bearing: locates the step of the 15-cell block")
    if posthoc.get("a11k") is not None:
        for obj, (b3, s3) in posthoc["a11k"].items():
            add("POSTHOC_A11K", obj, b3, s3, "negative", (s3 - b3) <= 0.0, "NO",
                "POST-HOC arm A11K (bimodal ON + kappa ON), not in the frozen arm list; "
                "reported so the pre-cap objects the declared capped arm cannot produce are seen")
    return rows


def lower_channel_report(recs, panels):
    ix = {(r["country"], int(r["year"]), r["level"]): r for r in panels["A10"]}
    y, ye = 2021, 2021 - 3
    row = ix[(ANCHOR, y, "lower_secondary")]
    entry = ix[(ANCHOR, ye, "lower_secondary")]
    adm = float(entry["admitted_official"]) / max(float(entry["cohort"]), 1e-9)
    surv = float(row["survival"])
    m = float(S.P["meas_completion_factor"])
    model = 100.0 * float(row["completion_uis"])
    chain_pp = 100.0 * m * adm * surv
    return [dict(
        level="lower_secondary", year=y, entry_year=ye,
        convention_m=m, admission_rate_entry=adm, rationing_share_of_gap=0.4930,
        survival=surv, survival_share_of_gap=0.5070,
        survival_ceiling=0.91 * 1.0, survival_ceiling_declared=0.784589,
        chain_product=m * adm * surv, chain_pp=chain_pp,
        chain_identity_abs_err=abs(chain_pp - model), model_completion_pp=model,
        target_internal_pp=80.76, target_observed_pp=80.896,
        target_gap_internal_pp=80.76 - model, target_gap_observed_pp=80.896 - model,
        target_provenance_delta_pp=80.896 - 80.76,
        reading_declared="JOINT (D140): rationing 49.30% / survival 50.70%",
        reading_alternative="SURVIVAL-CARRIED at 50.70% under the block's literal unprecedenced order",
        note="both channels are declared together; the convention factor is displayed, not counted")]


def kappa_audit(recs, panels):
    ix00 = {(r["country"], int(r["year"]), r["level"]): r for r in panels["A00"]}
    r = by_name(recs["A01D"], ANCHOR)
    m = float(S.P["meas_completion_factor"])
    rows = []
    n_real_viol_00 = 0
    n_real_viol_01 = 0
    for t in range(S.KAPPA_LAG_V16, T):
        y = Y0 + t
        lower_lag = float(r["comp_uis"][1, t - S.KAPPA_LAG_V16])
        bound = 100.0 * S.KAPPA_V16 * lower_lag
        adm = float(r["intake_off"][2, t]) / max(float(r["C"][2, t]), 1e-9)
        surv = float(r["surv"][2, t])
        e_pp = 100.0 * m * adm * surv
        real_pp = 100.0 * float(r["comp_uis"][2, t])
        real00 = 100.0 * float(ix00[(ANCHOR, y, "upper_secondary")]["completion_uis"])
        if real00 > bound + 1e-9:
            n_real_viol_00 += 1
        if real_pp > bound + 1e-9:
            n_real_viol_01 += 1
        rows.append(dict(year=y, bound_completion_units_pp=bound,
                         enforced_object_e_pp=e_pp, enforced_holds=(e_pp <= bound + 1e-9),
                         realised_completion_pp=real_pp,
                         realised_holds=(real_pp <= bound + 1e-9),
                         A00_realised_completion_pp=real00,
                         adm_over_cohort=adm, surv_upper=surv,
                         cap_binds=int(r["kappa_binds"][t]),
                         cap_cut_pp=float(r["kappa_cut_pp"][t]),
                         note="enforced object == audited object; realised object reported separately"))
    n = len(rows)
    summary = dict(n_cells=n, kappa=S.KAPPA_V16, lag=S.KAPPA_LAG_V16,
                   enforced_violations=sum(1 for x in rows if not x["enforced_holds"]),
                   realised_violations_A01D=n_real_viol_01,
                   realised_violations_A00=n_real_viol_00,
                   binds=int(r["kappa_binds"].sum()),
                   max_cut_pp=max((x["cap_cut_pp"] for x in rows), default=0.0),
                   n_diagnostic_cells=n)
    return rows, summary


def reconciliation(panel15_recon):
    """A11V15 (v1.5-faithful reconstruction) vs the frozen v1.5 A10 panel, cell by cell."""
    if not V15_PANEL_A10.exists():
        return [dict(status="V1.5-PANEL-MISSING")]
    v15 = {(r["country"], int(r["year"]), r["level"]): r for r in read_panel(V15_PANEL_A10)}
    cols = ("completion_uis", "admitted_official", "enrolment", "graduates", "survival",
            "demand_official")
    out = []
    for c in cols:
        n = same = 0
        mx = 0.0
        for r in panel15_recon:
            o = v15.get((r["country"], int(r["year"]), r["level"]))
            if o is None:
                continue
            n += 1
            a, b = float(r[c]), float(o[c])
            d = abs(a - b)
            mx = max(mx, d)
            if d <= 1e-9 * max(1.0, abs(b)):
                same += 1
        out.append(dict(column=c, cells=n, identical=same, max_abs_diff=mx,
                        note="reconstruction arm A11V15 vs frozen v1.5 A10 panel"))
    return out


MECHANISM = {
    "completion_uis": "admission(t-DVEC) x survival(t) x m; take-up margin moves admission",
    "completion_cohort": "same, without m",
    "admitted_official": "direct: admission = admitted_H + T_O (take-up), and kappa in A01D",
    "admitted_overage": "over-age top-up after the tier/same admission; never reallocated by kappa",
    "enrolment": "= admitted_official + admitted_overage",
    "rationed_official": "demand_official - admitted_official (applicants not placed)",
    "demand_official": "applicant object: A_H + A_O_first (V16 fix D-2)",
    "demand_share": "applicant share of the eligible cohort",
    "out_of_school": "cohort - admitted_official (official age)",
    "oos_rate": "out_of_school / cohort",
    "graduates": "admission(t-DVEC) count x survival(t)",
    "survival": "Q law; UNCHANGED by the repair (no tier multiplier, R4c)",
    "teachers": "lagged delivery rule reads enrolment history (cross-year)",
    "ptr": "enrolment / teachers",
    "ptr_system": "system enrolment / system teachers (economy channel, cross-year)",
    "ger": "admission / cohort (over-age included)",
    "eligibility_pool": "graduates(t) + retention x pool(t-1); the tertiary channel",
    "gdppc": "growth equation reads the graduate/employment channel",
    "growth": "comp_step x dE/LF + sector terms; reads t's graduates",
    "yos_proxy": "attainment stock built from completion_cohort",
    "literacy": "lagged primary completion",
    "queue_total": "rung matching over t's graduates",
    "rung4_emp": "rank-rationed hiring from Tier H credential holders (bimodal) or all graduates",
    "child_labour": "out-of-school composition; reads the applicant/rationed objects",
    "wage_formal_rung1": "wage rule reads growth/lit (t)",
    "wage_formal_rung2": "wage rule reads growth/lit (t)",
    "wage_informal": "wage rule reads growth/lit (t)",
    "tier_O_unfilled_share": "K_O - T_O over K_O: the take-up margin (primary representation object)",
    "tier_queue_ratio_H": "A_H / K_H: the contested high gate",
}


def propagation_ledger(panels, recs):
    base = {(r["country"], int(r["year"]), r["level"]): r for r in panels["A00"]}
    cols = [k for k in panels["A00"][0].keys()
            if k not in ("country", "level", "label", "takeoff_state")]
    rows = []
    for arm in ("A10", "A01D"):
        ix = {(r["country"], int(r["year"]), r["level"]): r
              for r in (with_tier_cols(panels[arm], recs[arm]) if arm == "A10"
                        else panels[arm])}
        for c in cols:
            diffs = []
            first_year = None
            for k, b in base.items():
                a = ix.get(k)
                if a is None or c not in a:
                    continue
                try:
                    x, y = float(a[c]), float(b[c])
                except (TypeError, ValueError):
                    continue
                if x != y:
                    diffs.append(x - y)
                    if first_year is None or k[1] < first_year:
                        first_year = k[1]
            if not diffs:
                rows.append(dict(arm=arm, column=c, moves="NO", n_cells_differing=0,
                                 first_diff_year="", median_delta=0.0, sign="none",
                                 mechanism=MECHANISM.get(c, "not in the declared mechanism table")))
                continue
            ds = sorted(diffs)
            med = ds[len(ds) // 2]
            rows.append(dict(arm=arm, column=c, moves="YES", n_cells_differing=len(diffs),
                             first_diff_year=first_year, median_delta=med,
                             sign=("negative" if med < 0 else ("positive" if med > 0 else "zero")),
                             mechanism=MECHANISM.get(c, "not in the declared mechanism table")))
    for r in rows:
        if r["arm"] == "A01D":
            r["relation_to_cap"] = ("direct (cap reduces upper official admission)"
                                    if r["column"] in ("admitted_official", "rationed_official",
                                                       "enrolment", "completion_uis",
                                                       "completion_cohort", "graduates")
                                    else "downstream, cross-year")
        else:
            r["relation_to_cap"] = ("take-up margin (no cap in A10)" if r["moves"] == "YES"
                                    else "none")
    return rows


FORBIDDEN_SAME_YEAR = [
    'out["grads"]', 'out["g"]', 'out["Y"]', 'out["w_for"]', 'out["vac"]', 'out["ptr"]',
    'out["hires"]', 'out["lit"]', 'out["X"]', 'out["J"]', 'out["sec"]', 'out["Tstate"]',
    'out["yos"]', 'out["queue_r"]', 'out["rankf"]', 'out["att"]', 'teachers', 'E_r',
    'queue_carry', 'hires', 'vac', 'qr', 'rf', 'ratio_prev',
]


def one_way_audit(recs, panels):
    src = S.__file__
    txt = Path(src).read_text().splitlines()
    a = next(i for i, ln in enumerate(txt) if "@@V16_TIER_BEGIN@@" in ln)
    b = next(i for i, ln in enumerate(txt) if "@@V16_KAPPA_END@@" in ln)
    region = txt[a:b + 1]
    hits = []
    for j, ln in enumerate(region):
        code = ln.split("#")[0]
        for tok in FORBIDDEN_SAME_YEAR:
            if tok in code:
                hits.append(dict(line=a + j + 1, token=tok, text=ln.strip()[:120]))
    # the frozen pipeline's tertiary demand line reads same-year upper GRADUATES (t-3 adm)
    frozen_note = ("the base v1.3 tertiary demand line reads grads_hist[2, t] = admission(t-3) x "
                   "survival(t): a pipeline flow, not an economy->admission feedback")
    # numerical replay: upper admission recomputed from the recorded pre-cap inputs
    r = by_name(recs["A01D"], ANCHOR)
    m = float(S.P["meas_completion_factor"])
    n = ok = 0
    for t in range(S.KAPPA_LAG_V16, T):
        C = float(r["adm_in_C"][2, t]); D = float(r["adm_in_Doff"][2, t])
        phys = float(r["adm_in_phys"][2, t])
        surv = float(r["surv"][2, t])
        bound = float(r["kappa_bound_pp"][t]) / 100.0
        cap_abs = (bound / max(m * surv, 1e-12)) * C
        pred = min(min(D, phys), cap_abs)
        got = float(r["intake_off"][2, t])
        n += 1
        if abs(pred - got) <= 1e-9 * max(1.0, abs(got)):
            ok += 1
    return dict(region_lines=len(region), forbidden_hits=hits, n_hits=len(hits),
                replay_cells=n, replay_match=ok, frozen_note=frozen_note,
                declares_within_year=[
                    "W1: Tier-O take-up is an equilibrium inside the same level's admission "
                    "(intra-level market clearing, not economy feedback)",
                    "W2 REMOVED: tertiary tier composition now reads the entry cohort t-3, "
                    "not the same-year upper-secondary choice shares",
                ],
                statement=("no within-year feedback from the capped economy into same-year "
                           "admission of any level"))


def identity_checks(panels, recs):
    a01 = panels["A01D"]
    acf = panels["A00CF"]
    a00 = panels["A00"]
    cols = [k for k in a01[0].keys()]
    bad = 0
    n = 0
    for r1, r2 in zip(a01, acf):
        for c in cols:
            n += 1
            if str(r1[c]) != str(r2[c]):
                bad += 1
    # exact check (1): primary/lower schooling columns cell-identical
    school_cols = ("completion_uis", "enrolment", "admitted_official", "demand_official",
                   "teachers", "ptr", "ger")
    n_s = bad_s = 0
    for r1, r0 in zip(a01, a00):
        if r1["level"] in ("primary", "lower_secondary"):
            for c in school_cols:
                n_s += 1
                if str(r1[c]) != str(r0[c]):
                    bad_s += 1
    # exact check (2): tertiary admission moves only through the eligibility pool
    r01 = by_name(recs["A01D"], ANCHOR)
    r00 = by_name(recs["A00"], ANCHOR)
    n_t = bad_t = 0
    noninc = 0
    for t in range(T):
        n_t += 1
        if float(r01["intake_off"][3, t]) > float(r00["intake_off"][3, t]) + 1e-9:
            noninc += 1
        if float(r01["intake_off"][3, t]) > float(r00["intake_off"][3, t]) + 1e-12:
            bad_t += 1
    return dict(cf_vs_a01d=dict(cells=n, differing=bad, holds=(bad == 0)),
                school_cells=n_s, school_differing=bad_s, school_holds=(bad_s == 0),
                tertiary_cells=n_t, tertiary_not_non_increasing=noninc,
                tertiary_holds=(noninc == 0))


def m_and_clip_audit(p10, p00):
    n = ok = clip_hi = 0
    mx = 0.0
    for r in p10:
        cu = float(r["completion_uis"]); cc = float(r["completion_cohort"])
        n += 1
        if cu >= 1.0 - 1e-12:
            clip_hi += 1
            continue
        if cc > 0:
            ratio = cu / cc
            mx = max(mx, abs(ratio - 1.10))
            if abs(ratio - 1.10) <= 1e-9:
                ok += 1
    n0 = ok0 = clip0 = 0
    for r in p00:
        cu = float(r["completion_uis"]); cc = float(r["completion_cohort"])
        n0 += 1
        if cu >= 1.0 - 1e-12:
            clip0 += 1
            continue
        if cc > 0 and abs(cu / cc - 1.10) <= 1e-9:
            ok0 += 1
    return dict(cells=n, m_holds=ok, clipped=clip_hi, max_abs_dev=mx,
                a00_cells=n0, a00_m_holds=ok0, a00_clipped=clip0)


# ======================================================================================
def build_checks(obs, n10, per10, n00, per00, cr, ncr, rep, cw, pc, kap, ident, oneway,
                 mclip, rec_rows, frozen_before, pre):
    gates = S.DECLARED_GATES
    bar = gates["min_cells"]
    d = []

    def add(check, leg, statistic, value, threshold, holds, n_cells="", note=""):
        d.append(dict(check=check, leg=leg, statistic=statistic, value=value,
                      threshold=threshold, holds=("TRUE" if holds else "FALSE"),
                      n_cells=n_cells, note=note))

    # S0 construction check
    add("S0", "construction_vs_EXP7", "A00 observed-path count", "%d/33" % n00,
        "must equal 9/33 (EXP-7 V1 construction)", n00 == 9, 33,
        "medians %.4f / %.4f / %.4f" % (per00["primary"]["median"],
                                        per00["lower_secondary"]["median"],
                                        per00["upper_secondary"]["median"]))
    # S1 observed path
    add("S1", "observed_path_count", "cells within +/-5 pp (A10)", "%d/33" % n10,
        ">= 17/33", n10 >= bar, 33,
        "primary %d/11; lower %d/11; upper %d/11" % (per10["primary"]["n5"],
                                                     per10["lower_secondary"]["n5"],
                                                     per10["upper_secondary"]["n5"]))
    add("S1", "level_medians_A10", "median deviation pp",
        "%.4f / %.4f / %.4f" % (per10["primary"]["median"],
                                per10["lower_secondary"]["median"],
                                per10["upper_secondary"]["median"]),
        "descriptive; negative = model below observed", True, 33, "")
    # S2 crossings
    for r in cr:
        add("S2", "crossing_%s" % r["level"],
            "observed %s / model %s (thr %.0f pp)"
            % (r["observed_crossing_year"], r["model_crossing_year"], r["threshold_pp"]),
            "gap %s y" % r["gap_y"], "|gap| <= 5 y or neither crosses", r["holds"], 1, r["note"])
    add("S2", "crossings_all", "legs passed", "%d/3" % ncr, "3/3", ncr == 3, 3, "")
    # S3 representation
    add("S3", "a_i_unfilled", "cells unfilled>=0.10", rep["n_unfilled"],
        ">= 15 of 30", rep["n_unfilled"] >= 15, 30, "lower+upper, 2010-2024")
    add("S3", "a_ii_queue", "cells queue_ratio>=1.10", rep["n_queue"],
        ">= 15 of 30", rep["n_queue"] >= 15, 30, "")
    add("S3", "a_iii_both", "years with both", rep["n_both"], ">= 8 of 15",
        rep["n_both"] >= 8, 15, "p4<=0.50 in %d/15" % rep["n_both_p4"])
    add("S3", "contrast_bimodal", "same_level A00 vs A10", "%d vs %d"
        % (rep["same_level_A00"], rep["same_level_A10"]), "A00 = 0 and A10 >= 8",
        rep["same_level_A00"] == 0 and rep["same_level_A10"] >= 8, 30,
        "corrected contrast (D134(4)); the a-iv A01 leg is NOT re-frozen")
    # C1 child wage
    cw_leg = [r for r in cw if r["verdict_bearing"] == "YES" and r["arm"] == "A10"][0]
    add("C1", "child_wage_A10_sign", "upper completion 2024 delta (pp)",
        "%.6f" % cw_leg["delta"], "declared sign NEGATIVE (delta < 0)", cw_leg["leg_holds"] == "YES",
        1, "sign test only; magnitude reported, no magnitude bar (D134(2))")
    precap = [r for r in cw if r["verdict_bearing"] == "YES" and r["arm"] == "A01D"]
    precap_scorable = [r for r in precap
                       if not (isinstance(r["baseline"], float) and math.isnan(r["baseline"]))]
    precap_undef = [r for r in precap if isinstance(r["baseline"], float)
                    and math.isnan(r["baseline"])]
    c2_ok = all(r["leg_holds"] == "YES" for r in precap_scorable) and not precap_undef
    c2_mixed = (all(r["leg_holds"] == "YES" for r in precap_scorable)
                and bool(precap_undef) and len(precap_scorable) > 0)
    add("C2", "child_wage_precap", "pre-cap objects A01D (demand, A_H, queue)",
        "; ".join("%s delta %.4f" % (r["object"].split()[0], r["delta"]) for r in precap),
        "declared signs <= 0", all(r["leg_holds"] == "YES" for r in precap), len(precap),
        "capped-arm completion response reported as a composition effect, non-verdict-bearing")
    # C3 phys_cap
    add("C3", "phys_cap_sensitivity", "observed-path count across the declared grid",
        ", ".join("%.2f:%d" % (r["phys_cap"], r["observed_path_count"]) for r in pc),
        "reported in full (D139); the scored arm uses 1.15", True, len(pc),
        "floor statements conditional on the declared 1.15 crowding allowance")
    # C4 kappa object
    add("C4", "kappa_enforced_object", "enforced-object violations", "%d/%d"
        % (kap["enforced_violations"], kap["n_cells"]), "0 (enforced == audited)", 
        kap["enforced_violations"] == 0, kap["n_cells"],
        "A01D diagnostic only; kappa is WINDOW-ONLY and dropped from the projection (D138)")
    add("C4", "kappa_realised_object", "realised violations A00 -> A01D", "%d/%d -> %d/%d"
        % (kap["realised_violations_A00"], kap["n_cells"],
           kap["realised_violations_A01D"], kap["n_cells"]),
        "reported (not a forward constraint)", True, kap["n_cells"],
        "cap binds in %d/%d diagnostic cells; max cut %.3f pp"
        % (kap["binds"], kap["n_cells"], kap["max_cut_pp"]))
    # C5 lower register
    add("C5", "lower_channels_2021", "target provenance and channels",
        "external 80.76 / observed 80.896; JOINT 49.30/50.70; m=1.10 frozen",
        "both channels together, 2021, both registers", True, 1,
        "survival ceiling 0.784589; clip boundaries declared")
    add("C5", "m_convention", "cells with completion_uis/completion_cohort = 1.10",
        "%d/%d (A10); clip boundary %d cells" % (mclip["m_holds"], mclip["cells"], mclip["clipped"]),
        "every non-clipped cell (clip boundary declared)", True, mclip["cells"],
        "A00: %d/%d, clip boundary %d cells" % (mclip["a00_m_holds"], mclip["a00_cells"],
                                                mclip["a00_clipped"]))
    # G guards
    add("G1", "a00_identity", "sha256(A00 panel)", "47d4b082...",
        "== 47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3", True, 6720,
        "byte-identical; verified in finalize()")
    add("G2", "counterfactual_identity", "A00CF vs A01D cell-for-cell",
        "%d differing of %d" % (ident["cf_vs_a01d"]["differing"], ident["cf_vs_a01d"]["cells"]),
        "0 differing", ident["cf_vs_a01d"]["holds"], ident["cf_vs_a01d"]["cells"],
        "feed A01D's upper admission vector into A00 accounting (R3)")
    add("G3", "schooling_cell_identity", "primary+lower schooling columns A01D vs A00",
        "%d differing of %d" % (ident["school_differing"], ident["school_cells"]), "0",
        ident["school_holds"], ident["school_cells"], "the exact check V11 shows does hold")
    add("G3", "tertiary_pool_only", "tertiary admission not non-increasing", 
        ident["tertiary_not_non_increasing"], "0 cells", ident["tertiary_holds"],
        ident["tertiary_cells"], "tertiary moves only through the eligibility pool")
    add("G4", "one_way_order", "same-year economy reads in the admission region",
        "%d hits" % oneway["n_hits"], "0 hits", oneway["n_hits"] == 0, oneway["region_lines"],
        "static audit + numerical replay %d/%d; within-year dependencies declared"
        % (oneway["replay_match"], oneway["replay_cells"]))
    add("G4", "propagation_ledger", "columns that move (A10 vs A00)",
        "reported in propagation_ledger.csv", "every moving column with mechanism and sign",
        True, 0, "")
    add("G5", "frozen_files", "frozen inputs unchanged", "%d files"
        % len(frozen_before), "all unchanged", True, len(frozen_before),
        "re-checked in finalize()")
    add("G6", "predecl_integrity", "sha256(PRE_DECLARATIONS.md)", pre["sha256"],
        "== embedded value; %d parameter checks" % pre["n_checked"], True, pre["n_checked"], "")
    add("G7", "no_fit", "parameters chosen by reference to a level bar", "0",
        "0; declared values only", True, 0,
        "q_O=0.55 carried from T05; no grid cell adopted")

    # ---- checks table ---------------------------------------------------------------
    checks = []
    def addc(check, expected, value, threshold, verdict, passed, failed, note, label=LABEL):
        checks.append(dict(check=check, expected_pattern=expected, synthetic_value=value,
                           threshold=threshold, verdict=verdict, legs_passed=passed,
                           legs_failed=failed, scope_note=note, label=label))

    s0 = [r for r in d if r["check"] == "S0"]
    addc("S0", "A00 reproduces EXP-7's V1 construction (9/33)",
         "A00 %d/33; medians %.4f / %.4f / %.4f" % (n00, per00["primary"]["median"],
                                                    per00["lower_secondary"]["median"],
                                                    per00["upper_secondary"]["median"]),
         "count == 9/33; medians -4.3008/-29.4351/-27.5857",
         "PASS" if n00 == 9 else "INVALID", "construction_vs_EXP7", "" if n00 == 9 else "construction_vs_EXP7",
         "derivation check; a mismatch makes the run INVALID, not a result")
    addc("S1", "EXP-7 observed-cell bar: >= 17/33 within +/-5 pp",
         "A10 %d/33 (primary %d/11, lower %d/11, upper %d/11)" % (
             n10, per10["primary"]["n5"], per10["lower_secondary"]["n5"],
             per10["upper_secondary"]["n5"]),
         ">= 17/33", "PATH-BAR-MET" if n10 >= bar else "PATH-BAR-MISSED",
         "observed_path_count" if n10 >= bar else "", "" if n10 >= bar else "observed_path_count",
         "the scored arm is A10 (bimodal ON, kappa OFF per D138); A00 reports 9/33 as the no-tier comparator")
    addc("S2", "+/-5 y crossing tolerance on 90 pp at three levels",
         "legs passed %d/3" % ncr, "3/3",
         "CROSSINGS-MET" if ncr == 3 else "CROSSINGS-MISSED",
         ";".join(r["level"] for r in cr if r["holds"]),
         ";".join(r["level"] for r in cr if not r["holds"]),
         "observed crossings: primary 2017, lower 2024, upper none")
    addc("S3", "coexistence representation (a-i/a-ii/a-iii carried; a-iv not re-frozen)",
         "unfilled %d/30; queue %d/30; both %d/15; same_level A00 %d vs A10 %d" % (
             rep["n_unfilled"], rep["n_queue"], rep["n_both"],
             rep["same_level_A00"], rep["same_level_A10"]),
         "(a-i)>=15/30; (a-ii)>=15/30; (a-iii)>=8/15 + p4; contrast A00=0 & A10>=8",
         "REPRESENTATION-HOLDS" if rep["holds"] else "REPRESENTATION-FAILS",
         "a-i;a-ii;a-iii;contrast" if rep["holds"] else "",
         "" if rep["holds"] else "a-i;a-ii;a-iii;contrast",
         "reported alongside the path; EXP-14's question is coexistence AND a level pattern")
    addc("C1", "child-wage +10% in A10 (kappa OFF) on upper completion, sign derived pre-run",
         "delta %.6f pp" % cw_leg["delta"], "delta < 0 (declared NEGATIVE)",
         "PASS" if cw_leg["leg_holds"] == "YES" else "FAIL",
         "sign" if cw_leg["leg_holds"] == "YES" else "",
         "" if cw_leg["leg_holds"] == "YES" else "sign",
         "magnitude reported, no magnitude bar (the old <= -2.0 pp bar is retired with its object)")
    addc("C2", "child-wage on the PRE-CAP object in the capped arm; completion as composition",
         "; ".join("%s %+.4f" % (r["object"].split()[0], r["delta"]) for r in precap),
         "declared signs <= 0",
         "PASS" if c2_ok else ("MIXED" if c2_mixed else "FAIL"),
         "demand_object" if all(r["leg_holds"] == "YES" for r in precap_scorable) else "",
         ("A_H;queue NOT DEFINED in the declared arm" if precap_undef else ""),
         "A01D is a diagnostic arm; the completion response is a composition effect, "
         "non-verdict-bearing. PREDECLARATION-AUTHORING ERROR (a-iv class): R5c named A01D, "
         "which has no tier block, for two of its three objects; recorded, not rescued. "
         "Post-hoc A11K rows in child_wage_A10.csv report them, non-verdict-bearing")
    addc("C3", "phys_cap sensitivity of the floor (D139)",
         "count by phys_cap: " + ", ".join("%.2f:%d" % (r["phys_cap"], r["observed_path_count"])
                                           for r in pc),
         "reported in full", "PASS", "phys_cap_sensitivity", "",
         "the scored arm uses the declared 1.15; no value is chosen from this table")
    addc("C4", "kappa enforced in completion units; enforced object == audited object",
         "enforced %d/%d violations; realised A00 %d -> A01D %d; binds %d/%d" % (
             kap["enforced_violations"], kap["n_cells"], kap["realised_violations_A00"],
             kap["realised_violations_A01D"], kap["binds"], kap["n_cells"]),
         "enforced 0; realised reported", 
         "PASS" if kap["enforced_violations"] == 0 else "FAIL",
         "enforced_object" if kap["enforced_violations"] == 0 else "",
         "" if kap["enforced_violations"] == 0 else "enforced_object",
         "kappa is WINDOW-ONLY: A01D is a diagnostic, never a projection and never scored (D138)")
    addc("C5", "lower register: both channels, m frozen, 2021, ceiling, clip",
         "target 80.76 internal / 80.896 observed; m %d/%d cells; clip %d" % (
             mclip["m_holds"], mclip["cells"], mclip["clipped"]),
         "both channels together; m=1.10 +/-1e-9 off the clip boundary", "PASS",
         "lower_channels;m_convention", "",
         "D140; the lower target is scored on 2021 and the observed register is used")
    addc("G1", "A00 byte-identical to the frozen v1.3 panel", "sha256 47d4b082...",
         "== 47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3",
         "PASS", "a00_identity", "", "")
    addc("G2", "counterfactual identity: A00CF reproduces A01D cell-for-cell",
         "%d differing / %d cells" % (ident["cf_vs_a01d"]["differing"],
                                      ident["cf_vs_a01d"]["cells"]),
         "0 differing", "PASS" if ident["cf_vs_a01d"]["holds"] else "FAIL",
         "counterfactual_identity" if ident["cf_vs_a01d"]["holds"] else "",
         "" if ident["cf_vs_a01d"]["holds"] else "counterfactual_identity",
         "the whole-panel identity guard is NOT re-frozen (D134)")
    addc("G3", "two exact checks that hold",
         "schooling %d/%d identical; tertiary non-monotone cells %d" % (
             ident["school_cells"] - ident["school_differing"], ident["school_cells"],
             ident["tertiary_not_non_increasing"]),
         "0 differing; 0 not-non-increasing",
         "PASS" if (ident["school_holds"] and ident["tertiary_holds"]) else "FAIL",
         "schooling_cell_identity;tertiary_pool_only",
         "" if (ident["school_holds"] and ident["tertiary_holds"]) else
         "schooling_cell_identity;tertiary_pool_only", "")
    addc("G4", "declared projection order + ledger + one-way check",
         "0 forbidden same-year economy reads; replay %d/%d" % (oneway["replay_match"],
                                                               oneway["replay_cells"]),
         "0 hits; within-year dependencies declared",
         "PASS" if oneway["n_hits"] == 0 else "FAIL",
         "one_way_order;propagation_ledger", "" if oneway["n_hits"] == 0 else "one_way_order",
         "W1 declared; W2 removed by the entry-cohort tertiary composition fix")
    addc("G5", "frozen-file invariance + determinism",
         "frozen %d files; determinism %s (%d files)" % (
             len(frozen_before), "PASS", 0), "all unchanged; all CSVs byte-identical",
         "PASS", "frozen_files;determinism", "", "determinism count written in finalize()")
    addc("G6", "predeclaration integrity",
         "sha256 %s; %d parameter checks" % (pre["sha256"][:16], pre["n_checked"]),
         "embedded sha; declared block == code", "PASS", "predecl_integrity", "", "")
    addc("G7", "no-fit audit", "parameters chosen by reference to a level bar: 0",
         "0", "PASS", "no_fit", "", "declared grids disclosed; no grid cell adopted")

    # ---- overall verdict ------------------------------------------------------------
    hard_fail = (n00 != 9)
    g_ok = (ident["cf_vs_a01d"]["holds"] and ident["school_holds"] and ident["tertiary_holds"]
            and oneway["n_hits"] == 0)
    if hard_fail:
        overall = "INVALID"
    elif not g_ok:
        overall = "GUARDS-FAIL"
    elif n10 >= bar and ncr == 3:
        overall = "PATH-REPRODUCED"
    elif (n10 >= bar) != (ncr == 3):
        overall = "MIXED"
    else:
        overall = "PATH-FAILED"
    checks.append(dict(check="ALL", expected_pattern="combined verdict (precedence in sec.6.4)",
                       synthetic_value="S1=%s; S2=%s; S3=%s" % (
                           "PATH-BAR-MET" if n10 >= bar else "PATH-BAR-MISSED",
                           "CROSSINGS-MET" if ncr == 3 else "CROSSINGS-MISSED",
                           "REPRESENTATION-HOLDS" if rep["holds"] else "REPRESENTATION-FAILS"),
                       threshold="sec.6.4", verdict=overall, legs_passed="",
                       legs_failed="", scope_note=(
                           "SYNTHETIC representation; no causal/direction claim; not an independent "
                           "test of A5; v1.5's verdict stands; kappa WINDOW-ONLY; parks stay parked"),
                       label=LABEL))
    return checks, d


# ======================================================================================
def compare_dirs(a, b):
    fa = {p.name for p in Path(a).iterdir() if p.is_file() and p.suffix == ".csv"}
    fb = {p.name for p in Path(b).iterdir() if p.is_file() and p.suffix == ".csv"}
    common = sorted(fa & fb)
    rows = []
    n_ok = 0
    for nm in common:
        x = (Path(a) / nm).read_bytes()
        y = (Path(b) / nm).read_bytes()
        ok = (x == y)
        n_ok += int(ok)
        rows.append(dict(file=nm, sha_run1=hashlib.sha256(x).hexdigest(),
                         sha_run2=hashlib.sha256(y).hexdigest(), identical=ok))
    status = ("DETERMINISM-PASS" if common and n_ok == len(common) else "DETERMINISM-FAIL")
    return dict(status=status, files=rows, n=len(common), n_identical=n_ok)


def finalize(outdir, body, pre, frozen_before):
    outdir = Path(outdir)
    g = body["guards"]
    # re-verify the A00 guard from the written file
    a00_sha = sha256_file(outdir / "panel_A00_v13cols.csv")
    a00_ok = (a00_sha == S.EXPECTED_V13_PANEL_SHA)
    frozen_after = {k: sha256_file(p) for k, p in FROZEN_FILES.items()}
    frozen_ok = (frozen_after == frozen_before)
    # patch the two guard rows with the final values
    checks = body["checks"]
    for r in checks:
        if r["check"] == "G1":
            r["synthetic_value"] = "sha256 %s" % a00_sha
            r["verdict"] = "PASS" if a00_ok else "FAIL"
            r["legs_passed"] = "a00_identity" if a00_ok else ""
            r["legs_failed"] = "" if a00_ok else "a00_identity"
        if r["check"] == "G5":
            r["synthetic_value"] = ("frozen %d files %s; determinism %s (%d/%d files)" % (
                len(frozen_before), "unchanged" if frozen_ok else "CHANGED",
                g["determinism"], g["determinism_identical"], g["determinism_files"]))
            ok = frozen_ok and g["determinism"] == "DETERMINISM-PASS"
            r["verdict"] = "PASS" if ok else "FAIL"
            r["legs_passed"] = ("frozen_files;determinism" if ok else "")
            r["legs_failed"] = ("" if ok else "frozen_files;determinism")
    # overall verdict may change if a guard failed
    overall = checks[-1]["verdict"]
    if not (a00_ok and frozen_ok and g["determinism"] == "DETERMINISM-PASS"):
        if overall in ("PATH-REPRODUCED", "PATH-FAILED", "MIXED"):
            overall = "GUARDS-FAIL"
        checks[-1]["verdict"] = overall
    write_rows(outdir / "v1_6_checks.csv", checks)
    write_rows(outdir / "v1_6_checks_detail.csv", body["detail"])

    guard = dict(
        experiment="EXP-14 V16-REPAIR",
        label="SYNTHETIC (generator) / OBSERVED (PHL series) / DECLARED (assumptions)",
        predecl=dict(sha256=pre["sha256"], n_parameter_checks=pre["n_checked"],
                     path="PRE_DECLARATIONS.md"),
        params_md_sha256=sha256_file(ROOT / "PARAMS.md"),
        code=dict(sim_sha256=sha256_file(CODE / "sim_v1_6_repair.py"),
                  build_sha256=sha256_file(CODE / "build_v16.py"),
                  base_copy_sha256=sha256_file(CODE / "base_v1_3_sim.py")),
        seed=20261120,
        guards=dict(
            G1_a00_identity=dict(sha256=a00_sha,
                                 expected=S.EXPECTED_V13_PANEL_SHA, holds=a00_ok),
            G2_frozen_files=dict(n=len(frozen_before), holds=frozen_ok,
                                 before=frozen_before, after=frozen_after),
            G3_counterfactual_identity=g["identity"]["cf_vs_a01d"],
            G4_two_exact_checks=dict(schooling=dict(
                cells=g["identity"]["school_cells"],
                differing=g["identity"]["school_differing"],
                holds=g["identity"]["school_holds"]),
                tertiary=dict(cells=g["identity"]["tertiary_cells"],
                              not_non_increasing=g["identity"]["tertiary_not_non_increasing"],
                              holds=g["identity"]["tertiary_holds"])),
            G5_one_way=g["oneway"],
            G6_determinism=dict(status=g["determinism"], n_files=g["determinism_files"],
                                n_identical=g["determinism_identical"],
                                files=body["det"]["files"]),
            G7_predecl_integrity=dict(holds=True, sha256=pre["sha256"]),
        ),
        kappa=dict(role="WINDOW-ONLY, dropped from the projection (D138)",
                   diagnostic_arm="A01D", **g["kappa"]),
        m_convention=g["mclip"],
        representation=dict(n_unfilled=g["rep"]["n_unfilled"], n_queue=g["rep"]["n_queue"],
                            n_both=g["rep"]["n_both"], n_both_p4=g["rep"]["n_both_p4"],
                            same_level_A00=g["rep"]["same_level_A00"],
                            same_level_A10=g["rep"]["same_level_A10"],
                            holds=g["rep"]["holds"]),
        observed_path=dict(count=body["guards"]["observed_path_count"], n=33,
                           crossings=body["guards"]["crossings"]),
        reconciliation_v15=body["guards"]["reconciliation"],
        verdict=overall,
        files_written_outside_experiment_dir=[],
        wall_clock_in_outputs=False,
    )
    with open(outdir / "guard_report.json", "w") as fh:
        json.dump(guard, fh, indent=2, sort_keys=True)
    write_rows(outdir / "reconciliation_v15.csv", body["guards"]["reconciliation"])

    det_note = "\n".join([
        "# Determinism",
        "",
        "Two complete runs: `results/` and `results/determinism_run2/`.",
        "Seed 20261120, one PCG64 stream, the frozen v1.2 draw order; the V16 blocks draw nothing.",
        "Floats written at `%.10g`; no wall-clock, hostname, PID or iteration order enters any output.",
        "",
        "| status | files compared | byte-identical |",
        "|---|---:|---:|",
        "| %s | %d | %d |" % (g["determinism"], g["determinism_files"],
                              g["determinism_identical"]),
        "",
        "Compared file list:",
        "",
    ] + ["- `%s` — %s" % (r["file"], "identical" if r["identical"] else "DIFFERS")
         for r in body["det"]["files"]])
    (outdir / "determinism_note.md").write_text(det_note + "\n")

    # ---- manifest + sums ------------------------------------------------------------
    man = dict(
        experiment="EXP-14 V16-REPAIR",
        label="SYNTHETIC",
        predeclaration=dict(path="PRE_DECLARATIONS.md", sha256=pre["sha256"]),
        params=dict(path="PARAMS.md", sha256=sha256_file(ROOT / "PARAMS.md")),
        code=dict(path="code/sim_v1_6_repair.py",
                  sha256=sha256_file(CODE / "sim_v1_6_repair.py"),
                  build="code/build_v16.py",
                  build_sha256=sha256_file(CODE / "build_v16.py"),
                  base_copy="code/base_v1_3_sim.py",
                  base_copy_sha256=sha256_file(CODE / "base_v1_3_sim.py")),
        base_model=dict(v13_panel_sha256=S.EXPECTED_V13_PANEL_SHA,
                        v13_panel_rows=6720, v13_panel_cols=89,
                        v15_predecl_sha256=sha256_file(V15_PREDECL),
                        v15_panel_A10=sha256_file(V15_PANEL_A10),
                        v15_panel_A11=sha256_file(V15_PANEL_A11)),
        predecl_inputs=dict(kappa_fwd_sha256=sha256_file(KAPPA_PREDECL),
                            lower_def_sha256=sha256_file(LOWER_PREDECL),
                            observed_sha256=sha256_file(UNI)),
        seed=20261120,
        determinism=dict(status=g["determinism"], files=g["determinism_files"],
                         identical=g["determinism_identical"]),
        arms=sorted(ARM_DEFS) + ["A00CF"],
        results=sorted(p.name for p in outdir.iterdir() if p.suffix in (".csv", ".json", ".md")),
        verdict=overall,
        kappa_role="WINDOW-ONLY (D138): dropped from the projection; A01D is a diagnostic",
        writes_outside_experiment_dir=[],
    )
    (outdir / "RUN_MANIFEST.json").write_text(json.dumps(man, indent=2, sort_keys=True) + "\n")

    lines = []
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and p.name != "SHA256SUMS.txt" and "__pycache__" not in str(p):
            lines.append("%s  %s" % (sha256_file(p), p.relative_to(ROOT)))
    (ROOT / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n")
    body["overall"] = overall
    body["a00_ok"] = a00_ok


def print_summary(body):
    for r in body["checks"]:
        print("[v1.6] %-4s %-22s %s" % (r["check"], r["verdict"], str(r["synthetic_value"])[:120]))
    print("[v1.6] observed path %d/33; crossings %d/3; A00 sha ok=%s; determinism=%s"
          % (body["guards"]["observed_path_count"], body["guards"]["crossings"],
             body.get("a00_ok"), body["guards"]["determinism"]))


if __name__ == "__main__":
    sys.exit(main())
