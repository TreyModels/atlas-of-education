#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXP-9 RUNG-PROB -- is the ceiling demand-derivable from either probability?

EVERYTHING THIS SCRIPT EMITS IS SYNTHETIC. It is a declared-assumption bracket test of a
declared-assumption generator: not an estimate, not evidence about any country, not a forecast,
and it licenses no causal or direction claim. Country labels are synthetic ("SYN28",
"SYN00_PHL_LIKE", ...); no real country is modelled or measured.

What it does
------------
Two arms, each ONE declared substitution into the SAME frozen v1.4 demand block, all else frozen:

  arm A : P(advance at L=2) = pi0(g2)                  (~0.999; the frozen v1.4 arm, unchanged)
  arm B : P(advance at L=2) = rung4_emp / rung4_demand (~0.151 anchor median; from the frozen v1.2
                                                       panel, same country and calendar year)

`DEMAND-DERIVABLE` iff an arm's upper 2024 lands in [71, 79] AND that arm's ablation moves upper
2024 by >= 3.0 pp (D81). Falsifier: both arms outside [71, 79] -> `NOT DEMAND-DERIVABLE`; the A3
line is KILLED, not parked. A negative is the expected outcome and is reported as such.

The frozen v1.4 code is copied byte-for-byte into `code/frozen_v1_4/`; NO line of it is edited. The
arm-B substitution is applied at run time by replacing the module's `demand_values` symbol with a
wrapper that changes exactly one argument (gs[2]["pi0"]); the frozen text is never touched. The
substitution draws no RNG. The base run uses one numpy PCG64 stream, seed 20261120 (inherited).

REFUSES TO RUN if this module's PRE_DECLARATIONS.md, the frozen v1.4 code copy or the v1.3 base
code copy no longer match the hashes frozen before the scored run.

Usage:  python run_rung_prob.py [--out DIR] [--manifest FILE]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import platform
import sys
from pathlib import Path

import numpy as np

LABEL = "SYNTHETIC"
SEED = 20261120

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                       # rung_prob_2026-11-20/
SYNTH = ROOT.parent / "synthetic_2026-11-20"   # frozen sibling extensions
MASS = ROOT.parents[1]                   # 10_massification/
DATA = MASS / "data"

FROZEN14 = SYNTH / "generator_v1_4_demand"
V12_DIR = SYNTH / "generator_v1_2"
V13_DIR = SYNTH / "generator_v1_3"
FROZEN_COPY = HERE / "frozen_v1_4" / "sim_v1_4_demand.py"
BASE_COPY = HERE / "frozen_v1_4" / "base_v1_3_sim.py"
V12_PANEL = V12_DIR / "results" / "synthetic_panel_v1_2.csv"
V14_ON_PANEL = FROZEN14 / "results" / "synthetic_panel_v1_4_demand.csv"
V14_OFF_PANEL = FROZEN14 / "results" / "_ablation" / "synthetic_panel_v1_4_demand_off.csv"

# Frozen before the scored run. Do not edit after any result is seen.
EXPECTED_PREDECL_SHA = "1cd399dd07a5ad1bc1e1d47637f36dde2a9dcf3ed7c46beca02550f6608bb8be"
EXPECTED_FROZEN_CODE_SHA = "6e4a6761fa32325c61f138037a1e5c8d5e578e19f8a2ee2519e73e8f2332b2d1"
EXPECTED_BASE_CODE_SHA = "70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877"
EXPECTED_V13_PANEL_SHA = "47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3"
EXPECTED_V14_ON_SHA = "ffecd450514cf8259512647db4e78bcd058639c208a1a2057bbac8b506ddbdaa"
EXPECTED_V12_PANEL_SHA = "14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac"
EXPECTED_V14_PREDECL_SHA = "9ed0cae353c9a3dfba00582ff47d19ca8b761d8dd7b7ce5f9a8a8e4c5c5f49b3"

BAND_LO, BAND_HI = 71.0, 79.0
ABL_MIN_PP = 3.0
ANCHOR = "SYN00_PHL_LIKE"
SCORE_YEAR = 2024

ARM_A = "arm_A_pi0_g2"
ARM_B = "arm_B_rung4_absorption"


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fnum(x):
    """The frozen formatting convention (%.10g); blank for None."""
    return "" if x is None else f"{float(x):.10g}"


def load_frozen():
    """Import the byte-identical frozen v1.4 copy and point its data path at the frozen data."""
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("rung_prob_frozen_v1_4", FROZEN_COPY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.DATA = DATA                     # the only path the run-time functions actually read
    return mod


def load_rung4_lookup():
    """p4 = rung4_emp / rung4_demand from the frozen v1.2 panel, upper-secondary rows.

    V8's own object and window. Defined where rung4_demand > 0; 100/1680 country-years are
    undefined (all pre-2006, none in SYN00_PHL_LIKE) and are handled by the declared fallback.
    """
    with open(V12_PANEL, newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["level"] == "upper_secondary"]
    lookup = {}
    total = 0
    for r in rows:
        total += 1
        d = float(r["rung4_demand"])
        e = float(r["rung4_emp"])
        if d > 0.0:
            lookup[(r["country"], int(float(r["year"])))] = e / d
    return lookup, total


class ArmBSubstitution:
    """The ONE declared substitution: gs[2]['pi0'] -> rung4_emp/rung4_demand.

    Calls the frozen demand_values() with an otherwise identical argument list. The calendar year
    is inferred from the deterministic once-per-country-per-year call order (1970..2025) and is
    asserted against the stored D_padv after the run. No RNG. Where the rung-4 ratio is undefined
    the model's own pi0(g2) is left in place (declared fallback).
    """

    def __init__(self, mod, lookup, orig):
        self.mod = mod
        self.lookup = lookup
        self.orig = orig
        self.calls = {}
        self.fallback_cells = set()
        self.substituted_cells = 0

    def __call__(self, cp, w_for, w_inf, J, hires, queue, gs, cfg=None, **kw):
        name = cp["name"]
        k = self.calls.get(name, 0)
        year = int(self.mod.YEAR_START) + k
        self.calls[name] = k + 1
        r = self.lookup.get((name, year))
        if r is None:
            self.fallback_cells.add((name, year))
            return self.orig(cp, w_for, w_inf, J, hires, queue, gs, cfg, **kw)
        gs2 = {g: dict(v) for g, v in gs.items()}
        gs2[2]["pi0"] = float(r)
        self.substituted_cells += 1
        return self.orig(cp, w_for, w_inf, J, hires, queue, gs2, cfg, **kw)


def run_off(mod, inputs, hosts):
    res, ptr_obs, spend_obs, S_phl, P_phl = mod.run_all(
        seed=SEED, shadow=True, inputs=inputs, hosts=hosts, dem=False)
    rows = mod.build_panel_v13(res, hosts, inputs)
    return res, rows


def run_on(mod, inputs, hosts, substitution=None):
    orig = mod.demand_values
    if substitution is not None:
        mod.demand_values = substitution
    try:
        res, *_ = mod.run_all(seed=SEED, shadow=True, inputs=inputs, hosts=hosts, dem=True)
    finally:
        mod.demand_values = orig
    rows = mod.build_panel_v14(res, hosts, inputs, demand=True)
    return res, rows


def anchor_components(mod, res, year=SCORE_YEAR):
    """L=2 components at the scored year for the anchor type; None where the block is OFF."""
    if not res or not res[0].get("dem_on"):
        return {k: None for k in (
            "p_adv", "R_gate", "access", "w_dest", "w_inf", "ER", "ER_hh", "ER_mig",
            "ER_net", "ER_P", "v_D", "v_baseline", "demand_share")}
    t = int(year) - int(mod.YEAR_START)
    r = next(x for x in res if x["cp"]["name"] == ANCHOR)
    return dict(
        p_adv=float(r["D_padv"][2, t]),
        R_gate=float(r["D_Rg"][2, t]),
        access=float(r["D_access"][2, t]),
        w_dest=float(r["D_wdest"][2, t]),
        w_inf=float(r["w_inf"][t]),
        ER=float(r["D_ER"][2, t]),
        ER_hh=float(r["D_ER_hh"][2, t]),
        ER_mig=float(r["D_ER_mig"][2, t]),
        ER_net=float(r["D_ER_hh"][2, t] + r["D_ER_mig"][2, t]),
        ER_P=float(r["D_ER_P"][2, t]),
        v_D=float(r["D_vD"][2, t]),
        v_baseline=float(r["D_v2"][2, t]),
        demand_share=float(r["demand_share"][2, t]),
    )


def band_info(upper):
    if upper < BAND_LO:
        return (BAND_LO - upper, "below", False)
    if upper > BAND_HI:
        return (upper - BAND_HI, "above", False)
    return (0.0, "inside", True)


def arm_verdict(upper, ablat):
    inside = BAND_LO <= upper <= BAND_HI
    nondec = abs(ablat) >= ABL_MIN_PP
    return ("DEMAND-DERIVABLE" if (inside and nondec) else "NOT DEMAND-DERIVABLE",
            inside, nondec)


def write_csv(rows, path):
    cols = list(rows[0].keys())
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: (fnum(v) if isinstance(v, float) else v) for k, v in row.items()})


def write_arms_detail(mod, path, off_res, res_by_arm, lookup):
    """Per-country / per-year L=2 cells behind the aggregates, for OFF and both arms."""
    cols = ["label", "arm", "country", "country_id", "year", "level", "p_adv", "p_rule",
            "p_fallback", "R_gate", "access", "w_dest", "w_inf", "ER", "ER_hh", "ER_mig",
            "ER_net", "ER_P", "v_D", "v_baseline", "demand_share", "admitted_official",
            "completion_uis"]
    out = []

    def base_row(r, t, arm, p_rule, p_fallback):
        return dict(label=LABEL, arm=arm, country=r["cp"]["name"],
                    country_id=int(r["cp"]["idx"]), year=int(mod.YEARS[t]),
                    level="upper_secondary", p_adv=None, p_rule=p_rule,
                    p_fallback=p_fallback, R_gate=None, access=None, w_dest=None,
                    w_inf=None, ER=None, ER_hh=None, ER_mig=None, ER_net=None, ER_P=None,
                    v_D=None, v_baseline=None,
                    demand_share=float(r["demand_share"][2, t]),
                    admitted_official=float(r["intake_off"][2, t]),
                    completion_uis=float(r["comp_uis"][2, t]))

    for r in off_res:
        for t in range(int(mod.T)):
            out.append(base_row(r, t, "OFF_baseline", "demand block OFF", ""))

    for arm, res in res_by_arm:
        for r in res:
            name = r["cp"]["name"]
            for t in range(int(mod.T)):
                year = int(mod.YEARS[t])
                row = base_row(r, t, arm,
                               "pi0(g2)" if arm == ARM_A else "rung4_emp/rung4_demand",
                               0 if (name, year) in lookup or arm == ARM_A else 1)
                row.update(
                    p_adv=float(r["D_padv"][2, t]),
                    R_gate=float(r["D_Rg"][2, t]),
                    access=float(r["D_access"][2, t]),
                    w_dest=float(r["D_wdest"][2, t]),
                    w_inf=float(r["w_inf"][t]),
                    ER=float(r["D_ER"][2, t]),
                    ER_hh=float(r["D_ER_hh"][2, t]),
                    ER_mig=float(r["D_ER_mig"][2, t]),
                    ER_net=float(r["D_ER_hh"][2, t] + r["D_ER_mig"][2, t]),
                    ER_P=float(r["D_ER_P"][2, t]),
                    v_D=float(r["D_vD"][2, t]),
                    v_baseline=float(r["D_v2"][2, t]),
                )
                out.append(row)
    write_csv(out, path)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "results"))
    ap.add_argument("--manifest", default=str(ROOT / "RUN_MANIFEST.json"))
    args = ap.parse_args(argv)

    # ---- 0. integrity / predeclaration freeze --------------------------------------
    predecl_sha = sha256_file(ROOT / "PRE_DECLARATIONS.md")
    if predecl_sha != EXPECTED_PREDECL_SHA:
        raise SystemExit("REFUSING: PRE_DECLARATIONS.md changed (%s != %s)"
                         % (predecl_sha, EXPECTED_PREDECL_SHA))
    if sha256_file(FROZEN_COPY) != EXPECTED_FROZEN_CODE_SHA:
        raise SystemExit("REFUSING: frozen v1.4 code copy is not byte-identical")
    if sha256_file(BASE_COPY) != EXPECTED_BASE_CODE_SHA:
        raise SystemExit("REFUSING: v1.3 base code copy is not byte-identical")

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    panel_dir = outdir / "panels"; panel_dir.mkdir(parents=True, exist_ok=True)

    mod = load_frozen()
    inputs = mod.shadow_inputs_named()
    lookup, n_cells = load_rung4_lookup()
    n_fallback = n_cells - len(lookup)

    # ---- 1. OFF run (unmodified; the ablation base and guard G1) -------------------
    res_base, *_ = mod.run_all(seed=SEED, shadow=False)
    hosts, gdp = mod.resolve_hosts(res_base)
    off_res, rows_off = run_off(mod, inputs, hosts)
    off_panel = panel_dir / "synthetic_panel_v1_4_demand_off.csv"
    mod.write_panel_v13(rows_off, off_panel)
    off_sha = sha256_file(off_panel)
    off_upper = mod.upper_uis_2024(rows_off)
    g1 = (off_sha == EXPECTED_V13_PANEL_SHA)

    # ---- 2. arm A: frozen v1.4 ON arm, no substitution -----------------------------
    a_res, rows_a = run_on(mod, inputs, hosts)
    a_panel = panel_dir / "synthetic_panel_v1_4_demand_on_armA.csv"
    mod.write_rows(rows_a, a_panel)
    a_sha = sha256_file(a_panel)
    a_upper = mod.upper_uis_2024(rows_a)
    g2 = (a_sha == EXPECTED_V14_ON_SHA)

    # ---- 3. arm B: the ONE declared substitution ----------------------------------
    sub = ArmBSubstitution(mod, lookup, mod.demand_values)
    b_res, rows_b = run_on(mod, inputs, hosts, substitution=sub)
    b_panel = panel_dir / "synthetic_panel_v1_4_demand_on_armB.csv"
    mod.write_rows(rows_b, b_panel)
    b_sha = sha256_file(b_panel)
    b_upper = mod.upper_uis_2024(rows_b)

    # ---- 4. arm-B self-checks (hard errors, not reportable values) -----------------
    if set(sub.calls) != {r["cp"]["name"] for r in b_res}:
        raise SystemExit("arm-B: country set mismatch")
    if set(sub.calls.values()) != {int(mod.T)}:
        raise SystemExit("arm-B: call count is not T for every country: %r"
                         % sorted(set(sub.calls.values())))
    bad = 0
    for r in b_res:
        name = r["cp"]["name"]
        for t in range(int(mod.T)):
            exp = lookup.get((name, int(mod.YEARS[t])))
            if exp is not None and abs(float(r["D_padv"][2, t]) - exp) > 1e-12:
                bad += 1
    if bad:
        raise SystemExit("arm-B: %d substituted p_adv cells do not match the panel ratio" % bad)
    if any(c == ANCHOR for (c, y) in sub.fallback_cells):
        raise SystemExit("arm-B: fallback used in the anchor type; this is not allowed")
    if len(sub.fallback_cells) != n_fallback:
        raise SystemExit("arm-B: fallback count %d != expected %d"
                         % (len(sub.fallback_cells), n_fallback))

    # ---- 5. ablation + arm verdicts ------------------------------------------------
    guard = "PASS" if (g1 and g2) else "guard-fail"
    abl_a = a_upper - off_upper
    abl_b = b_upper - off_upper
    v_a, in_a, nondec_a = arm_verdict(a_upper, abl_a)
    v_b, in_b, nondec_b = arm_verdict(b_upper, abl_b)
    dist_a, dir_a, _ = band_info(a_upper)
    dist_b, dir_b, _ = band_info(b_upper)

    if guard != "PASS":
        overall = "guard-fail"
    elif v_a == "DEMAND-DERIVABLE" or v_b == "DEMAND-DERIVABLE":
        overall = "DEMAND-DERIVABLE"
    else:
        overall = "NOT DEMAND-DERIVABLE"
    both_outside = (not in_a) and (not in_b)
    falsifier = bool(both_outside and guard == "PASS")

    ca = anchor_components(mod, a_res)
    cb = anchor_components(mod, b_res)

    rows = [
        dict(label=LABEL, row="baseline_OFF", arm="OFF_baseline",
             probability_rule="none (demand block OFF; v1.3 world)",
             upper_uis_2024=off_upper, band_lo=BAND_LO, band_hi=BAND_HI,
             in_band=(BAND_LO <= off_upper <= BAND_HI),
             distance_from_band_pp=0.0, direction="inside",
             ablation_upper_off_pp=off_upper, ablation_delta_pp=None,
             ablation_abs_pp=None, ablation_bar_pp=ABL_MIN_PP, ablation_verdict="INFO",
             arm_verdict="INFO", p_adv_anchor_2024=None, v_D_anchor_2024=None,
             v_baseline_anchor_2024=None, demand_share_anchor_2024=float(
                 next(r for r in off_res if r["cp"]["name"] == ANCHOR)["demand_share"][
                     2, SCORE_YEAR - int(mod.YEAR_START)]),
             guard=guard, note="ablation base and guard G1"),
        dict(label=LABEL, row=ARM_A, arm=ARM_A, probability_rule="P = pi0(g2) (~0.999)",
             upper_uis_2024=a_upper, band_lo=BAND_LO, band_hi=BAND_HI, in_band=in_a,
             distance_from_band_pp=dist_a, direction=dir_a,
             ablation_upper_off_pp=off_upper, ablation_delta_pp=abl_a,
             ablation_abs_pp=abs(abl_a), ablation_bar_pp=ABL_MIN_PP,
             ablation_verdict=("NON-DECORATIVE" if nondec_a else "DECORATIVE"),
             arm_verdict=v_a, p_adv_anchor_2024=ca["p_adv"], v_D_anchor_2024=ca["v_D"],
             v_baseline_anchor_2024=ca["v_baseline"],
             demand_share_anchor_2024=ca["demand_share"], guard=guard,
             note=("frozen v1.4 ON arm, unchanged" if g2 else "G2 MISMATCH")),
        dict(label=LABEL, row=ARM_B, arm=ARM_B,
             probability_rule="P = rung4_emp / rung4_demand (~0.151 anchor median)",
             upper_uis_2024=b_upper, band_lo=BAND_LO, band_hi=BAND_HI, in_band=in_b,
             distance_from_band_pp=dist_b, direction=dir_b,
             ablation_upper_off_pp=off_upper, ablation_delta_pp=abl_b,
             ablation_abs_pp=abs(abl_b), ablation_bar_pp=ABL_MIN_PP,
             ablation_verdict=("NON-DECORATIVE" if nondec_b else "DECORATIVE"),
             arm_verdict=v_b, p_adv_anchor_2024=cb["p_adv"], v_D_anchor_2024=cb["v_D"],
             v_baseline_anchor_2024=cb["v_baseline"],
             demand_share_anchor_2024=cb["demand_share"], guard=guard,
             note="single declared substitution gs[2]['pi0']; R_gate unchanged; "
                  "%d/%d country-years use the pi0 fallback (none in anchor)"
                  % (len(sub.fallback_cells), n_cells)),
        dict(label=LABEL, row="overall", arm="both_arms", probability_rule="both",
             upper_uis_2024=None, band_lo=BAND_LO, band_hi=BAND_HI, in_band=None,
             distance_from_band_pp=None, direction="", ablation_upper_off_pp=off_upper,
             ablation_delta_pp=None, ablation_abs_pp=None, ablation_bar_pp=ABL_MIN_PP,
             ablation_verdict="", arm_verdict=overall, p_adv_anchor_2024=None,
             v_D_anchor_2024=None, v_baseline_anchor_2024=None,
             demand_share_anchor_2024=None, guard=guard,
             note=("both arms outside [71,79] -> A3 line KILLED, not parked"
                   if falsifier else "falsifier not triggered")),
    ]
    # full anchor components in the aggregate (the ARMS file carries every cell)
    comp_keys = ["R_gate", "access", "w_dest", "w_inf", "ER", "ER_hh", "ER_mig",
                 "ER_net", "ER_P"]
    for r in rows:
        for k in comp_keys:
            r[k + "_anchor_2024"] = None
    for r, comp in ((rows[1], ca), (rows[2], cb)):
        for k in comp_keys:
            r[k + "_anchor_2024"] = comp[k]
    write_csv(rows, outdir / "RUNG_PROB_RESULTS.csv")

    detail = write_arms_detail(mod, outdir / "RUNG_PROB_ARMS.csv", off_res,
                               [(ARM_A, a_res), (ARM_B, b_res)], lookup)

    guard_doc = dict(
        label=LABEL,
        statement=("The unmodified arm must reproduce the frozen v1.4 panel byte-for-byte; the "
                   "demand-OFF run must reproduce the frozen v1.3 panel byte-for-byte."),
        guard_verdict=guard,
        G1_off=dict(what="demand-OFF panel vs frozen v1.3 panel",
                    written="panels/synthetic_panel_v1_4_demand_off.csv",
                    sha256=off_sha, expected=EXPECTED_V13_PANEL_SHA,
                    byte_identical=bool(g1)),
        G2_on_unmodified=dict(what="arm A (no substitution) ON panel vs frozen v1.4 ON panel",
                              written="panels/synthetic_panel_v1_4_demand_on_armA.csv",
                              sha256=a_sha, expected=EXPECTED_V14_ON_SHA,
                              byte_identical=bool(g2)),
        arm_B_panel=dict(written="panels/synthetic_panel_v1_4_demand_on_armB.csv",
                         sha256=b_sha),
        frozen_inputs=dict(
            v14_code_sha256=sha256_file(FROZEN14 / "code" / "sim_v1_4_demand.py"),
            v13_base_code_sha256=sha256_file(FROZEN14 / "code" / "base_v1_3_sim.py"),
            v14_on_panel_sha256=sha256_file(V14_ON_PANEL),
            v14_off_panel_sha256=sha256_file(V14_OFF_PANEL),
            v13_panel_sha256=sha256_file(V13_DIR / "results" / "synthetic_panel_v1_3.csv"),
            v12_panel_sha256=sha256_file(V12_PANEL),
            v14_predecl_sha256=sha256_file(FROZEN14 / "PRE_DECLARATIONS.md"),
        ),
        v12_rung4_lookup=dict(country_years=n_cells, defined=len(lookup),
                              fallback=n_fallback, anchor_fallback=0),
    )
    (outdir / "BASELINE_GUARD.json").write_text(
        json.dumps(guard_doc, indent=2, sort_keys=True) + "\n")

    # ---- 6. manifest ---------------------------------------------------------------
    res_files = {p.name: sha256_file(p) for p in sorted(outdir.glob("*.csv"))}
    panel_files = {"panels/" + p.name: sha256_file(p) for p in sorted(panel_dir.glob("*.csv"))}
    guard_file = {"BASELINE_GUARD.json": sha256_file(outdir / "BASELINE_GUARD.json")}
    manifest = dict(
        label=LABEL,
        experiment="EXP-9 RUNG-PROB",
        statement=("Synthetic data from declared assumptions only. Not evidence, not an "
                   "estimate, not a forecast, no causal or direction claim, no real country "
                   "modelled. A negative result is the expected outcome and is reported as "
                   "such; no parameter, band, bar or arm was changed after any result was seen."),
        predeclaration=dict(path="PRE_DECLARATIONS.md", sha256=predecl_sha),
        code=dict(path="code/run_rung_prob.py",
                  sha256=sha256_file(HERE / "run_rung_prob.py"),
                  frozen_copy="code/frozen_v1_4/sim_v1_4_demand.py",
                  frozen_copy_sha256=sha256_file(FROZEN_COPY),
                  frozen_copy_status="byte-identical copy of frozen v1.4 code; not edited",
                  base_copy="code/frozen_v1_4/base_v1_3_sim.py",
                  base_copy_sha256=sha256_file(BASE_COPY)),
        frozen_spec=dict(v14_predecl_sha256=sha256_file(FROZEN14 / "PRE_DECLARATIONS.md"),
                         v14_on_panel_sha256=sha256_file(V14_ON_PANEL),
                         v14_off_panel_sha256=sha256_file(V14_OFF_PANEL),
                         v12_panel_sha256=sha256_file(V12_PANEL),
                         v13_panel_sha256=sha256_file(V13_DIR / "results" / "synthetic_panel_v1_3.csv")),
        seed=SEED,
        rng=("numpy PCG64 (np.random.default_rng), single stream, v1.2 draw order; neither the "
             "shadow block nor the demand block nor the arm-B substitution draws a random number"),
        arms=dict(
            A=dict(probability="pi0(g2)", substitution="none (frozen v1.4 ON arm)"),
            B=dict(probability="rung4_emp / rung4_demand from synthetic_panel_v1_2.csv",
                   substitution="gs[2]['pi0'] replaced inside demand_values only; R_gate unchanged",
                   fallback="pi0(g2) where rung4_demand == 0 (100/1680 cells, none in anchor)",
                   anchor_median_2010_plus=0.15103225591118347),
        ),
        host_mapping=hosts,
        scored_object=dict(country=ANCHOR, level="upper_secondary", year=SCORE_YEAR,
                           object="UIS-convention completion (completion_uis x 100)"),
        thresholds=dict(band=[BAND_LO, BAND_HI], ablation_bar_pp=ABL_MIN_PP),
        results=dict(
            upper_2024=dict(off=off_upper, arm_A=a_upper, arm_B=b_upper),
            ablation_pp=dict(arm_A=abl_a, arm_B=abl_b),
            in_band=dict(arm_A=bool(in_a), arm_B=bool(in_b)),
            arm_verdict=dict(arm_A=v_a, arm_B=v_b),
            overall=overall,
            both_arms_outside_band=bool(both_outside),
            falsifier_triggered=bool(falsifier),
        ),
        baseline_guard=dict(verdict=guard, G1_byte_identical=bool(g1),
                            G2_byte_identical=bool(g2),
                            off_panel_sha256=off_sha, armA_panel_sha256=a_sha,
                            armB_panel_sha256=b_sha),
        determinism=dict(method=("two clean runs into separate output directories; cmp on every "
                                 "result CSV, the guard JSON and the manifest"),
                         floats="%.10g", wall_clock_in_outputs=False),
        python=platform.python_version(), numpy=np.__version__,
        files=dict(**res_files, **panel_files, **guard_file),
        arms_detail_rows=len(detail),
    )
    Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    print("[rung-prob] hosts: " + ", ".join("%s<-%s" % (k, v) for k, v in hosts.items()))
    print("[rung-prob] guard G1 OFF %s -> %s | G2 ON(A) %s -> %s"
          % (off_sha[:16], g1, a_sha[:16], g2))
    print("[rung-prob] upper 2024: OFF %.10f  A %.10f  B %.10f" % (off_upper, a_upper, b_upper))
    print("[rung-prob] ablation pp: A %+.10f  B %+.10f  (bar %.1f)"
          % (abl_a, abl_b, ABL_MIN_PP))
    print("[rung-prob] in band: A %s  B %s | arms: %s / %s | overall: %s"
          % (in_a, in_b, v_a, v_b, overall))
    print("[rung-prob] falsifier both-outside: %s | detail rows %d" % (falsifier, len(detail)))
    return manifest


if __name__ == "__main__":
    main()
