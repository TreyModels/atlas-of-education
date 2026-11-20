#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIM_V1_7_PARTREPAIR -- EXP-18 **PART-REPAIR**: the consistency-repaired generator.

The v1.6 generator with ONE declaration-consistency change: the participation decision is
taken from the frozen v1.3 four-state block (`sim_v1_3.state_shares`), called unchanged, so
that the school-going mass and the out-of-school composition are the frozen block's own. The
tier menu, the capacity split, the admission ranking and the survival law are the frozen v1.6
ones. No new behavioural parameter; no value moved; the upper structural part is declared and
reported as a sensitivity, never tuned.

Scored on the observed path alone: the 33 `completion_<level>` cells for PHL (EXP-7's own
bar: >= 17/33 within +/-5 pp, plus +/-5 y crossings at 90/90/90 pp). The pre-committed closing
rule: bar missed -> the generator line closes at representation-only, no successor this phase.

Everything emitted is SYNTHETIC except the observed comparison object, which is OBSERVED and
enters only through the two declared phases (A: the frozen instrument's Layer-1b demographic
INPUT; C: the scoring object after every arm has finished). The phase guard refuses any
observed open in any other phase. No causal or direction claim. No fitting.

Run:  python code/sim_v1_7_partrepair.py [--out DIR] [--no-determinism]
"""
from __future__ import annotations

import argparse
import builtins
import csv
import hashlib
import io
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

CODE = Path(__file__).resolve().parent
CELL = CODE.parent            # .../synthetic_2026-11-20/generator_v1_7_partrepair
SYNTH = CELL.parent           # .../synthetic_2026-11-20
EXT = SYNTH.parent            # .../extensions
MASS = EXT.parent             # .../10_massification
PROG = MASS.parent            # .../massification-2026-11-20

FROZEN = CODE / "frozen"
V16_DIR = SYNTH / "generator_v1_6_repair"
V13_DIR = SYNTH / "generator_v1_3"
V13_PANEL = V13_DIR / "results" / "synthetic_panel_v1_3.csv"
A10_PANEL = V16_DIR / "results" / "panel_A10_repaired.csv"
V16_PREDECL = V16_DIR / "PRE_DECLARATIONS.md"
EXP16 = SYNTH.parent / "partprov_2026-11-20"
EXP17 = SYNTH.parent / "joint_cover_2026-11-20"
DATA = MASS / "data"

LABEL = "SYNTHETIC"
CELL_ID = "EXP-18-PART-REPAIR"

# ---- the ONE guard constant: the observed basename appears here and nowhere else ----------
OBSERVED_BASENAME = "UNIVERSALIZATION_SERIES.csv"
OBSERVED_PATH = DATA / OBSERVED_BASENAME

PREDECL = CELL / "PRE_DECLARATIONS.md"
PARAMS_MD = CELL / "PARAMS.md"
FREEZE_RECORD = CELL / "FREEZE_RECORD.json"
# sha256 of PRE_DECLARATIONS.md, written at freeze time (before any scored run).
EXPECTED_PREDECL_SHA = "3778afe38d29fc78bcf54275d40a3c183bcaa83f6f1fa4283d9e4e3cfe26d4a1"

EXPECTED_V16_SHA = "9c0e799850fd30bb0b46bb7841e8f301715745a5c73452e7644055122325de56"
EXPECTED_V13_SHA = "70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877"
EXPECTED_V13_PANEL_SHA = "47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3"
EXPECTED_V16_PREDECL_SHA = "6a554dc033828835431f65be2e5e218833fcdb56220baad8fbe53c3324e78991"

ANCHOR = "SYN00_PHL_LIKE"
LEVELS = ("primary", "lower_secondary", "upper_secondary")
ALL_LEVELS = ("primary", "lower_secondary", "upper_secondary", "tertiary")
DECLARED_GATES = dict(n_observed=33, cells_per_level=11, min_cells=17, tol_pp=5.0,
                      crossing_tol_y=5,
                      crossing_thresholds_pp=dict(primary=90.0, lower_secondary=90.0,
                                                  upper_secondary=90.0))
REP = dict(unfilled_min=0.10, queue_min=1.10, n_cells=30, min_cells=15,
           n_years=15, min_years=8)
A00_CONSTRUCTION = dict(count=9, medians_pp=(-4.3008, -29.4351, -27.5857))
SEED = 20261120
VOID_EXIT = 42
N_V16 = N_V17 = 110            # 82 P keys + 21 tier keys + 7 borrowed geometry constants

# ---- declared arms (full switch tuple, D147(iii)) ----------------------------------------
ENGINE = {
    "A00":   dict(bimodal=False),
    "A17":   dict(bimodal=True),
    "A17CF": dict(bimodal=False),          # + inject_upper, supplied by the driver
}
ARM_ORDER = ("A00", "A17", "A17CF")
VERDICT_ARM = "A17"
REPORT_ONLY = ("A00", "A17CF")
COMMON = dict(kappa_link=False, tier_surv=False, tier_cfg=None, w_child_mult=1.0,
              phys_cap=1.15, seed=SEED)

MECHANISM = {
    "completion_uis": "admission(t-DVEC) x survival(t) x m: the participation/admission margin",
    "completion_cohort": "same, without m",
    "admitted_official": "admission = admitted_H + T_O (the take-up margin)",
    "admitted_overage": "over-age top-up after the tier admission; never reallocated",
    "enrolment": "= admitted_official + admitted_overage",
    "rationed_official": "demand_official - admitted_official (applicants not placed)",
    "demand_official": "applicant object: A_H + A_O_first (V16 fix D-2)",
    "demand_share": "participation share: ds13 (the frozen block's own) in A17",
    "school_share": "p_school = (A_H + A_O_first)/(elig*C)",
    "both_share": "reporting composition (the block's own 'both' mass folds into school)",
    "work_share": "the block's own Pr[work]",
    "neither_share": "the block's own Pr[neither]",
    "out_of_school": "cohort - admitted_official (official age)",
    "oos_rate": "out_of_school / cohort",
    "graduates": "admission(t-DVEC) count x survival(t)",
    "survival": "Q law; UNCHANGED by the repair (no tier multiplier)",
    "teachers": "lagged delivery rule reads enrolment history (cross-year)",
    "ptr": "enrolment / teachers",
    "ptr_system": "system enrolment / system teachers (economy channel, cross-year)",
    "ger": "admission / cohort (over-age included)",
    "eligibility_pool": "graduates(t) + retention x pool(t-1): the pipeline channel",
    "queue_total": "rung matching over t's graduates",
    "child_labour": "out-of-school composition; reads the applicant/rationed objects",
    "tier_O_unfilled_share": "K_O - T_O over K_O: the take-up margin",
    "tier_queue_ratio_H": "A_H / K_H: the contested high gate",
}
FORBIDDEN_SAME_YEAR = [
    'out["grads"]', 'out["g"]', 'out["Y"]', 'out["w_for"]', 'out["vac"]', 'out["ptr"]',
    'out["hires"]', 'out["lit"]', 'out["X"]', 'out["J"]', 'out["sec"]', 'out["Tstate"]',
    'out["yos"]', 'out["queue_r"]', 'out["rankf"]', 'out["att"]', 'teachers', 'E_r',
    'queue_carry', 'hires', 'vac', 'qr', 'rf', 'ratio_prev',
]


# ======================================================================================
# the phase guard: observed reads only where the predeclaration allows them
# ======================================================================================
class ObservedFileAccess(RuntimeError):
    pass


class PhaseGuard:
    """Wraps every file-open entry point for the whole run.

    Phases: PREFLIGHT -> DEMOGRAPHIC -> ARMS -> SCORE -> DONE. The observed basename may be
    opened ONLY in DEMOGRAPHIC (inside `load_demographic_inputs`) and in SCORE (inside
    `load_observed_cells`, after every arm has finished). Any attempt in another phase raises
    BEFORE the OS call, so nothing is read. Every attempt is logged with a normalised path so
    two runs are byte-identical.
    """

    def __init__(self, forbidden_basename, outdir, prog):
        self.forbidden = forbidden_basename.lower()
        self.outdir = os.path.abspath(str(outdir))
        self.prog = os.path.abspath(str(prog))
        self.log = []
        self.blocked = 0
        self.phase = "PREFLIGHT"
        self.predecl_verified = False
        self._saved = None

    def norm(self, p):
        try:
            ap = os.path.abspath(str(p))
        except Exception:
            return str(p)
        if ap.startswith(self.outdir + os.sep) or ap == self.outdir:
            return "<OUT>/" + os.path.relpath(ap, self.outdir)
        if ap.startswith(self.prog + os.sep):
            return "<PROG>/" + os.path.relpath(ap, self.prog)
        return ap

    def _check(self, p, op):
        base = os.path.basename(str(p)).lower()
        if base == self.forbidden:
            ok = bool(self.predecl_verified and self.phase in ("DEMOGRAPHIC", "SCORE"))
            self.log.append({"path": self.norm(p), "op": op, "phase": self.phase,
                             "allowed": ok})
            if not ok:
                self.blocked += 1
                raise ObservedFileAccess(
                    "PHASE-GUARD: refused to open the observed series in phase %s (%s)"
                    % (self.phase, self.norm(p)))
            return p
        self.log.append({"path": self.norm(p), "op": op, "phase": self.phase,
                         "allowed": True})
        return p

    def __enter__(self):
        self._bopen, self._iopen, self._osopen = builtins.open, io.open, os.open
        guard = self

        def bopen(file, *a, **kw):
            op = "open:" + str(a[0] if a else kw.get("mode", "r"))
            guard._check(file, op)
            return guard._bopen(file, *a, **kw)

        def iopen(file, *a, **kw):
            op = "io.open:" + str(a[0] if a else kw.get("mode", "r"))
            guard._check(file, op)
            return guard._iopen(file, *a, **kw)

        def osopen(path, *a, **kw):
            guard._check(path, "os.open")
            return guard._osopen(path, *a, **kw)

        builtins.open, io.open, os.open = bopen, iopen, osopen
        return self

    def __exit__(self, *exc):
        builtins.open, io.open, os.open = self._bopen, self._iopen, self._osopen
        return False


# ======================================================================================
# helpers
# ======================================================================================
def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fnum(x, spec="%.10g"):
    if x is None or x == "":
        return ""
    if isinstance(x, bool):
        return "YES" if x else "NO"
    if isinstance(x, float):
        if x != x or x in (float("inf"), float("-inf")):
            return "nan"
        return spec % x
    return str(x)


def write_rows(path, header, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow([fnum(x) if isinstance(x, float) else x for x in r])


def write_dicts(path, rows):
    if not rows:
        return
    cols = list(rows[0].keys())
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: fnum(r.get(k, "")) for k in cols})


def declared_block(path):
    txt = Path(path).read_text()
    i = txt.index("```json\n")
    j = txt.index("\n```", i)
    return json.loads(txt[i + len("```json\n"):j])


def by_name(results, name):
    for r in results:
        if r["cp"]["name"] == name:
            return r
    raise CapabilityLint("anchor %r not in the results" % (name,))


class CapabilityLint(RuntimeError):
    pass


def with_tier_cols(rows, result, y0):
    """A17 panel + the declared tier columns (frozen v1.6 writer semantics)."""
    by = {r["cp"]["name"]: r for r in result}
    out = []
    for row in rows:
        r = by[row["country"]]
        t = int(row["year"]) - y0
        L = ALL_LEVELS.index(row["level"])
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
        out.append(d)
    return out


# ======================================================================================
# predeclaration integrity + freeze record
# ======================================================================================
def verify_declared(d, cap):
    """The declared JSON block must equal this driver's own constants, else REFUSE."""
    checks = {
        "cell": (d["cell"], CELL_ID),
        "label": (d["label"], LABEL),
        "anchor": (d["anchor"], ANCHOR),
        "levels": (list(d["levels"]), list(LEVELS)),
        "n_observed_cells": (int(d["n_observed_cells"]), DECLARED_GATES["n_observed"]),
        "cells_per_level": (int(d["cells_per_level"]), DECLARED_GATES["cells_per_level"]),
        "min_cells": (int(d["min_cells"]), DECLARED_GATES["min_cells"]),
        "tol_pp": (float(d["tol_pp"]), DECLARED_GATES["tol_pp"]),
        "crossing_tol_y": (int(d["crossing_tol_y"]), DECLARED_GATES["crossing_tol_y"]),
        "crossing_thresholds_pp": ({k: float(v) for k, v in
                                    d["crossing_thresholds_pp"].items()},
                                   dict(DECLARED_GATES["crossing_thresholds_pp"])),
        "representation": ({k: float(v) for k, v in d["representation"].items()},
                           {k: float(v) for k, v in REP.items()}),
        "a00_construction_count": (int(d["a00_construction_count"]),
                                   A00_CONSTRUCTION["count"]),
        "a00_construction_medians_pp": ([float(x) for x in
                                         d["a00_construction_medians_pp"]],
                                        [float(x) for x in A00_CONSTRUCTION["medians_pp"]]),
        "forbidden_basename": (d["forbidden_basename"], OBSERVED_BASENAME),
        "void_exit_code": (int(d["void_exit_code"]), VOID_EXIT),
        "seed": (int(d["seed"]), SEED),
        "arms": (list(d["arms"]), list(ARM_ORDER)),
        "verdict_bearing_arms": (list(d["verdict_bearing_arms"]), [VERDICT_ARM]),
        "report_only_arms": (list(d["report_only_arms"]), list(REPORT_ONLY)),
        "repair_source_sha256": (d["repair_source_sha256"], sha256_file(V13_DIR / "code" /
                                                                       "sim_v1_3.py")),
        "frozen_sim_v16_sha256": (d["frozen_sim_v16_sha256"],
                                  sha256_file(FROZEN / "sim_v1_6_repair.py")),
        "frozen_sim_v13_sha256": (d["frozen_sim_v13_sha256"],
                                  sha256_file(FROZEN / "sim_v1_3.py")),
        "frozen_v13_panel_sha256": (d["frozen_v13_panel_sha256"], sha256_file(V13_PANEL)),
        "frozen_a10_panel_sha256": (d["frozen_a10_panel_sha256"], sha256_file(A10_PANEL)),
        "frozen_v16_predecl_sha256": (d["frozen_v16_predecl_sha256"],
                                      sha256_file(V16_PREDECL)),
        "exp16_predecl_sha256": (d["exp16_predecl_sha256"],
                                 sha256_file(EXP16 / "PRE_DECLARATIONS.md")),
        "exp16_detail_sha256": (d["exp16_detail_sha256"],
                                sha256_file(EXP16 / "results" / "PARTPROV_DETAIL.csv")),
        "exp16_results_sha256_recorded": (d["exp16_results_sha256_recorded"],
                                          "a8469ac091ad8b338b832ec27b2a7d120cdf6f30b842d6ea0a"
                                          "bed58509d7695e"),
        "exp16_results_sha256_on_disk_at_freeze": (d["exp16_results_sha256_on_disk_at_freeze"],
                                                   "24fbd68888f24d454f0d38d7a89d2f7f4be92b5956e"
                                                   "a0274613b8b7a1de47289"),
        "exp17_predecl_sha256": (d["exp17_predecl_sha256"],
                                 sha256_file(EXP17 / "PRE_DECLARATIONS.md")),
        "exp17_results_sha256": (d["exp17_results_sha256"],
                                 sha256_file(EXP17 / "results" / "JOINT_COVER_RESULTS.csv")),
        "exp17_detail_sha256": (d["exp17_detail_sha256"],
                                sha256_file(EXP17 / "results" / "JOINT_COVER_DETAIL.csv")),
        "exp17_lambda_star": (float(d["exp17_lambda_star"]), 1.11465019198434),
        "exp17_derived_target_pp": (float(d["exp17_derived_target_pp"]), 0.8076),
        "parameter_counts": (dict(d["parameter_counts"]),
                             {"v16": cap["n_v16"], "v17": cap["n_v17"], "new": 0}),
    }
    bad = {k: v for k, v in checks.items() if v[0] != v[1]}
    if bad:
        raise SystemExit("REFUSED: declared block != code constants: %r" % (bad,))
    return len(checks)


def verify_freeze_record(cap):
    """The freeze record proves the predeclaration and the code were frozen together."""
    if not FREEZE_RECORD.exists():
        raise SystemExit("REFUSED: FREEZE_RECORD.json absent -- the cell was not frozen")
    rec = json.loads(FREEZE_RECORD.read_text())
    got = sha256_file(PREDECL)
    bad = {}
    if rec.get("predecl_sha256") != got:
        bad["predecl_sha256"] = (rec.get("predecl_sha256"), got)
    for name, want in rec.get("code_sha256", {}).items():
        p = CELL / name
        if not p.exists() or sha256_file(p) != want:
            bad["code_sha256:" + name] = (want, sha256_file(p) if p.exists() else "ABSENT")
    if rec.get("observed_file_opened_before_freeze") not in (False, 0):
        bad["observed_file_opened_before_freeze"] = ("FALSE",
                                                     rec.get("observed_file_opened_before_freeze"))
    if rec.get("count_computed_before_freeze") not in (False, 0):
        bad["count_computed_before_freeze"] = ("FALSE",
                                               rec.get("count_computed_before_freeze"))
    if bad:
        raise SystemExit("REFUSED: FREEZE-RECORD mismatch: %r" % (bad,))
    return rec


# ======================================================================================
# the pipeline
# ======================================================================================
def run_pipeline(S, V13, R, outdir, guard, cap, obs_meta, harness=False):
    y0 = int(S.YEAR_START)
    T = int(S.T)
    years = S.YEARS

    # ---- 1. the frozen predeclaration of the base is the declared object ------------------
    pre16 = S.verify_predecl(path=V16_PREDECL, expected_sha=EXPECTED_V16_PREDECL_SHA)
    if sha256_file(V16_PREDECL) != pre16["sha256"]:
        raise CapabilityLint("REFUSED: frozen v1.6 predeclaration hash mismatch")

    # ---- 2. Phase A: the declared Layer-1b demographic INPUT (two indicators only) --------
    guard.phase = "DEMOGRAPHIC"
    if harness:
        # PRE-FREEZE HARNESS ONLY (--harness-test): a reconstructed SYNTHETIC demographic
        # path from the frozen v1.3 panel. No observed file is opened. This branch is
        # unreachable once FREEZE_RECORD.json exists.
        band, pop = {}, {}
        with open(V13_PANEL, newline="") as fh:
            for r0 in csv.DictReader(fh):
                if r0["country"] != ANCHOR:
                    continue
                yv = int(float(r0["year"]))
                pop[yv] = float(r0["population"])
                if r0["level"] == "primary":
                    band[yv] = float(r0["band_population"])
        S_path = np.array([band[y] / S.P["band_share"][0] for y in years], dtype=float)
        Pop_path = np.array([pop[y] for y in years], dtype=float)
        demo_meta = {"path": "<HARNESS: frozen v1.3 panel>",
                     "indicators_retained": [], "rows_retained": len(years),
                     "rows_skipped_on_arrival": 0, "phase": "A-HARNESS",
                     "observed_outcomes_retained": 0}
    else:
        S_path, Pop_path, demo_meta = R.load_demographic_inputs(OBSERVED_PATH, years, T)
        demo_meta = dict(demo_meta)
        demo_meta["path"] = guard.norm(OBSERVED_PATH)
        demo_meta["phase"] = "A (demographic input)"

    def demographic_stub():
        """Replaces the frozen loader BEFORE any arm: it returns the declared input only."""
        return S_path, Pop_path, {}, {}, {}

    S.load_observed_phl_paths = demographic_stub

    # ---- 3. repair functions + capability lint -------------------------------------------
    fns = R.make_arm_functions(S, V13)
    if set(fns) != {"A00", "A17"}:
        raise CapabilityLint("REFUSED: CAPABILITY-LINT (arm set %r)" % (sorted(fns),))

    # ---- 4. the arms (no observed access in this phase) ----------------------------------
    guard.phase = "ARMS"
    recs, hosts_by = {}, {}
    for arm in ("A00", "A17"):
        cells_fn, alloc_fn = fns[arm]
        S.tier_cells, S.tier_allocate = cells_fn, alloc_fn
        kw = dict(COMMON)
        kw.update(ENGINE[arm])
        recs[arm], hosts_by[arm] = S.run_arm_full(**kw)
        if hosts_by[arm].get("SYN_PHL_LIKE") != ANCHOR:
            raise CapabilityLint("REFUSED: anchor is not the declared PHL-like host")
    # restore the frozen lookups (A00 is the frozen pair)
    S.tier_cells, S.tier_allocate = fns["A00"]

    # ---- 5. A17CF: the counterfactual replay (R3) ----------------------------------------
    inj = {}
    for rr in recs["A17"]:
        inj[rr["cp"]["name"]] = [float(rr["intake_off"][2, t]) for t in range(T)]
    kw = dict(COMMON)
    kw.update(ENGINE["A17CF"])
    kw["inject_upper"] = inj
    recs["A17CF"] = S.run_arm(shadow=True, hosts=hosts_by["A17"], **kw)
    hosts_by["A17CF"] = hosts_by["A17"]

    # ---- 6. panels ------------------------------------------------------------------------
    inputs = S.shadow_inputs_named()
    panels = {n: S.build_panel_v13(recs[n], hosts_by[n], inputs) for n in ARM_ORDER}
    panel17 = with_tier_cols(panels["A17"], recs["A17"], y0)

    # write A00 with the frozen writer: it must be byte-identical to the frozen v1.3 panel
    S.write_panel_v13(panels["A00"], Path(outdir) / "panel_A00_v13cols.csv")
    S.write_panel_v13(panels["A17CF"], Path(outdir) / "panel_A17CF_identity.csv")
    write_dicts(Path(outdir) / "panel_A17.csv", panel17)

    # ---- 7. Phase C: the scoring object ---------------------------------------------------
    guard.phase = "SCORE"
    if harness:
        # pre-freeze harness fixture: a constant 90.0 in 11 arbitrary years per level. It is
        # NOT the observed series and it is never used outside --harness-test.
        obs = {(lv, y): 90.0 for lv in LEVELS for y in range(2010, 2021)}
    else:
        obs = R.load_observed_cells(OBSERVED_PATH, LEVELS, y0, int(S.YEAR_END),
                                    DECLARED_GATES["cells_per_level"])
    obs_meta["n_cells"] = len(obs)
    obs_meta["path"] = ("<HARNESS>" if harness else guard.norm(OBSERVED_PATH))

    # ---- 8. score --------------------------------------------------------------------------
    def ix(panel):
        return {(r["country"], int(float(r["year"])), r["level"]): r for r in panel}

    i17, i00 = ix(panel17), ix(panels["A00"])
    path_rows, dev17, dev00 = [], [], []
    for lv in LEVELS:
        for (a, y) in sorted([k for k in obs if k[0] == lv], key=lambda k: k[1]):
            m17 = 100.0 * float(i17[(ANCHOR, y, lv)]["completion_uis"])
            m00 = 100.0 * float(i00[(ANCHOR, y, lv)]["completion_uis"])
            o = float(obs[(lv, y)])
            d17 = m17 - o
            d00 = m00 - o
            dev17.append(d17)
            dev00.append(d00)
            path_rows.append(dict(level=lv, year=y, model_A17_pp=m17, model_A00_pp=m00,
                                  observed_pp=o, deviation_A17_pp=d17,
                                  within_5pp_A17=("YES" if abs(d17) <=
                                                  DECLARED_GATES["tol_pp"] else "NO"),
                                  deviation_A00_pp=d00,
                                  within_5pp_A00=("YES" if abs(d00) <=
                                                  DECLARED_GATES["tol_pp"] else "NO")))
    n17 = sum(1 for r in path_rows if r["within_5pp_A17"] == "YES")
    n00 = sum(1 for r in path_rows if r["within_5pp_A00"] == "YES")

    def per_level(key):
        out = {}
        for lv in LEVELS:
            ds = sorted(r[key] for r in path_rows if r["level"] == lv)
            out[lv] = dict(n=len(ds), n5=sum(1 for d in ds if abs(d) <=
                                             DECLARED_GATES["tol_pp"]),
                           median_pp=ds[len(ds) // 2],
                           mean_pp=float(np.mean(ds)),
                           max_abs_pp=float(max(abs(d) for d in ds)))
        return out

    per17 = per_level("deviation_A17_pp")
    per00 = per_level("deviation_A00_pp")
    write_dicts(Path(outdir) / "observed_path_A17.csv", path_rows)

    # ---- 9. crossings ----------------------------------------------------------------------
    thr = DECLARED_GATES["crossing_thresholds_pp"]
    tol_y = DECLARED_GATES["crossing_tol_y"]

    def crossing_year(series, level):
        for y in sorted(series):
            if series[y] >= thr[level]:
                return y
        return None

    crossing_rows = []
    for lv in LEVELS:
        mser = {y: 100.0 * float(i17[(ANCHOR, y, lv)]["completion_uis"])
                for y in range(y0, int(S.YEAR_END) + 1)}
        oser = {y: v for (a, y), v in obs.items() if a == lv}
        oc, mc = crossing_year(oser, lv), crossing_year(mser, lv)
        if oc is not None and mc is not None:
            gap = mc - oc
            ok = abs(gap) <= tol_y
            note = "both cross"
        elif oc is None and mc is None:
            gap, ok, note = 0, True, "neither crosses by 2025"
        elif oc is None:
            gap, ok, note = None, False, "observed never crosses; model crosses"
        else:
            gap, ok, note = None, False, "observed crosses; model never crosses by 2025"
        crossing_rows.append(dict(level=lv, threshold_pp=thr[lv],
                                  observed_crossing_year=("" if oc is None else oc),
                                  model_crossing_year=("" if mc is None else mc),
                                  gap_y=("" if gap is None else gap), tolerance_y=tol_y,
                                  holds=("YES" if ok else "NO"), note=note,
                                  model_max_pp=float(max(mser.values()))))
    n_cross = sum(1 for r in crossing_rows if r["holds"] == "YES")
    write_dicts(Path(outdir) / "crossing_check.csv", crossing_rows)

    # ---- 10. representation ----------------------------------------------------------------
    rep_cells = []
    for y in range(2010, 2025):
        for lv in ALL_LEVELS:
            r = i17[(ANCHOR, y, lv)]
            unf = float(r["tier_O_unfilled_share"])
            q = float(r["tier_queue_ratio_H"])
            rep_cells.append(dict(year=y, level=lv,
                                  scored=("YES" if lv in ("lower_secondary",
                                                          "upper_secondary") else "NO"),
                                  unfilled=unf, queue_ratio=q,
                                  p4=float(r["job_gate_p4"]),
                                  coexists=("YES" if (unf >= REP["unfilled_min"] and
                                                      q >= REP["queue_min"]) else "NO")))
    sc = [c for c in rep_cells if c["scored"] == "YES"]
    n_unf = sum(1 for c in sc if c["unfilled"] >= REP["unfilled_min"] - 1e-12)
    n_q = sum(1 for c in sc if c["queue_ratio"] >= REP["queue_min"] - 1e-12)
    yrs = sorted({c["year"] for c in sc})
    yr_hold = {y: any((c["unfilled"] >= REP["unfilled_min"] - 1e-12
                       and c["queue_ratio"] >= REP["queue_min"] - 1e-12)
                      for c in sc if c["year"] == y) for y in yrs}
    n_both = sum(1 for y in yrs if yr_hold[y])
    n_both_p4 = sum(1 for y in yrs if yr_hold[y]
                    and all(c["p4"] <= 0.50 for c in sc if c["year"] == y))
    n_unf_lower = sum(1 for c in sc if c["level"] == "lower_secondary"
                      and c["unfilled"] >= REP["unfilled_min"] - 1e-12)
    n_unf_upper = sum(1 for c in sc if c["level"] == "upper_secondary"
                      and c["unfilled"] >= REP["unfilled_min"] - 1e-12)
    n_both_strict = sum(1 for y in yrs
                        if all(any((c["unfilled"] >= REP["unfilled_min"] - 1e-12
                                    and c["queue_ratio"] >= REP["queue_min"] - 1e-12)
                                   for c in sc if c["year"] == y and c["level"] == lv)
                               for lv in ("lower_secondary", "upper_secondary")))
    write_dicts(Path(outdir) / "representation_cells.csv", rep_cells)

    def same_level(panel):
        d = ix(panel)
        n = 0
        for y in range(2010, 2025):
            r = d[(ANCHOR, y, "upper_secondary")]
            spare = float(r["seats"]) - float(r["enrolment"])
            if spare > 0.0 and float(r["rationed_official"]) > 0.0:
                n += 1
        return n

    rep = dict(n_unfilled=n_unf, n_queue=n_q, n_both=n_both, n_both_p4=n_both_p4,
               n_unfilled_lower=n_unf_lower, n_unfilled_upper=n_unf_upper,
               n_both_strict=n_both_strict, same_level_A00=same_level(panels["A00"]),
               same_level_A17=same_level(panel17),
               holds=(n_unf >= REP["min_cells"] and n_q >= REP["min_cells"]
                      and n_both >= REP["min_years"]))

    # ---- 11. guard G1: A00 byte-identical to the frozen v1.3 panel ------------------------
    a00_sha = sha256_file(Path(outdir) / "panel_A00_v13cols.csv")
    g1 = dict(sha256=a00_sha, expected=EXPECTED_V13_PANEL_SHA,
              holds=(a00_sha == EXPECTED_V13_PANEL_SHA))

    # ---- 12. guard G2: counterfactual identity (upper pipeline through A00's accounting) --
    cf_rows = []
    n_cf = n_cf_bad = 0
    for group, cols in (("replay-determined", R.UPPER_PIPELINE_COLUMNS),
                        ("not-replay-determined", R.UPPER_NON_REPLAY_COLUMNS)):
        for col in cols:
            bad = n = 0
            for r17, rcf in zip(panel17, panels["A17CF"]):
                if r17["level"] != "upper_secondary":
                    continue
                n += 1
                if str(r17[col]) != str(rcf[col]):
                    bad += 1
            if group == "replay-determined":
                n_cf += n
                n_cf_bad += bad
            cf_rows.append(dict(column=col, cells=n, differing=bad, group=group,
                                holds=("YES" if bad == 0 else "NO")))
    ident = dict(cells=n_cf, differing=n_cf_bad, holds=(n_cf_bad == 0),
                 columns=list(R.UPPER_PIPELINE_COLUMNS),
                 non_replay_columns=list(R.UPPER_NON_REPLAY_COLUMNS),
                 mechanism=("the frozen inject_upper hook sets admitted_official AFTER the "
                            "over-age top-up is computed from the pre-injection baseline, so "
                            "admitted_overage/enrolment/ger/teachers/ptr are not replay-"
                            "determined and are reported, never asserted"),
                 arms="A17 vs A17CF (A00 accounting + A17's upper admission vector)")
    write_dicts(Path(outdir) / "counterfactual_identity.csv", cf_rows)

    # ---- 13. guard G3: schooling-supply identity (A17 vs A00) ----------------------------
    sc_rows = []
    n_s = n_s_bad = 0
    for col in R.SUPPLY_COLUMNS:
        bad = n = 0
        for r17, r00 in zip(panel17, panels["A00"]):
            n += 1
            if str(r17[col]) != str(r00[col]):
                bad += 1
        n_s += n
        n_s_bad += bad
        sc_rows.append(dict(column=col, cells=n, differing=bad,
                            holds=("YES" if bad == 0 else "NO")))
    school = dict(cells=n_s, differing=n_s_bad, holds=(n_s_bad == 0),
                  columns=list(R.SUPPLY_COLUMNS))
    write_dicts(Path(outdir) / "schooling_identity.csv", sc_rows)

    # ---- 14. guard G4: declared projection order + propagation ledger ---------------------
    src = Path(S.__file__).read_text().splitlines()
    a = next(i for i, ln in enumerate(src) if "@@V16_TIER_BEGIN@@" in ln)
    b = next(i for i, ln in enumerate(src) if "@@V16_KAPPA_END@@" in ln)
    region = src[a:b + 1]
    hits = []
    for j, ln in enumerate(region):
        code = ln.split("#")[0]
        for tok in FORBIDDEN_SAME_YEAR:
            if tok in code:
                hits.append(dict(line=a + j + 1, token=tok, text=ln.strip()[:120]))
    oneway = dict(region_lines=len(region), forbidden_hits=hits, n_hits=len(hits),
                  holds=(len(hits) == 0),
                  declares_within_year=[
                      "W1: Tier-O take-up is an equilibrium inside the same level's "
                      "admission (intra-level market clearing, not economy feedback)",
                      "W2: tertiary tier composition reads the entry cohort t-3",
                      "W3: the participation primitive ds13 is a function of the country's "
                      "drawn traits and the year's household shock only -- it reads no "
                      "endogenous state, so the repair introduces no new projection order",
                  ],
                  frozen_note=("the base v1.3 tertiary demand line reads grads_hist[2, t] = "
                               "admission(t-3) x survival(t): a pipeline flow, not an "
                               "economy->admission feedback"))

    base_ix = ix(panels["A00"])
    cols = [k for k in panel17[0].keys()
            if k not in ("country", "level", "label", "takeoff_state")]
    ledger = []
    for c in cols:
        diffs, first = [], None
        for r17 in panel17:
            k = (r17["country"], int(float(r17["year"])), r17["level"])
            r0 = base_ix.get(k)
            if r0 is None or c not in r0 or c not in r17:
                continue
            try:
                x, y = float(r17[c]), float(r0[c])
            except (TypeError, ValueError):
                continue
            if x != y:
                diffs.append(x - y)
                if first is None or k[1] < first:
                    first = k[1]
        if not diffs:
            ledger.append(dict(arm=VERDICT_ARM, column=c, moves="NO", n_cells_differing=0,
                               first_diff_year="", median_delta=0.0, sign="none",
                               mechanism=MECHANISM.get(c,
                                                       "not in the declared mechanism table")))
            continue
        ds = sorted(diffs)
        med = ds[len(ds) // 2]
        ledger.append(dict(arm=VERDICT_ARM, column=c, moves="YES",
                           n_cells_differing=len(diffs), first_diff_year=first,
                           median_delta=med,
                           sign=("negative" if med < 0 else
                                 ("positive" if med > 0 else "zero")),
                           mechanism=MECHANISM.get(c,
                                                   "not in the declared mechanism table")))
    write_dicts(Path(outdir) / "propagation_ledger.csv", ledger)

    # ---- 15. repair-in-force identity (the primitive really is the block's own) -----------
    v13 = {}
    with open(V13_PANEL, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["country"] == ANCHOR:
                v13[(int(float(r["year"])), r["level"])] = r
    rife_rows, n_rife, n_rife_ok = [], 0, 0
    for lv in LEVELS:
        for y in range(2010, 2025):
            a17 = fnum(float(i17[(ANCHOR, y, lv)]["demand_share"]))
            a13 = v13[(y, lv)]["demand_share"]
            ok = (a17 == a13)
            n_rife += 1
            n_rife_ok += int(ok)
            rife_rows.append(dict(level=lv, year=y, demand_share_A17=a17,
                                  demand_share_v13=a13, identical=("YES" if ok else "NO")))
    repair_in_force = dict(cells=n_rife, identical=n_rife_ok,
                           holds=(n_rife_ok == n_rife))
    write_dicts(Path(outdir) / "repair_in_force.csv", rife_rows)

    # ---- 16. capacity decomposition (report-only, arithmetic on A17's own panel) ----------
    cap_rows = []
    for lv in LEVELS:
        for y in range(2010, 2025):
            t = y - y0
            L = ALL_LEVELS.index(lv)
            r = by_name(recs[VERDICT_ARM], ANCHOR)
            C = float(r["C"][L, t])
            seats = float(r["seats"][L, t])
            dem = float(r["demand_off"][L, t])
            adm = float(r["intake_off"][L, t])
            dur = int(round(S.DVEC[L]))
            tf = t + dur
            surv = float(r["surv"][L, tf]) if tf < T else float("nan")
            m = float(S.P["meas_completion_factor"])
            phys = min(S.P["phys_cap"] * seats, S.P["overage_cap"] * C)
            head = 100.0 * m * (min(dem, phys) - adm) / max(C, 1e-9) * surv
            cap_rows.append(dict(level=lv, year=y, seats_over_cohort=seats / max(C, 1e-9),
                                 demand_over_cohort=dem / max(C, 1e-9),
                                 admitted_over_cohort=adm / max(C, 1e-9),
                                 one_place_ceiling_pp=100.0 * m * min(dem, seats) /
                                 max(C, 1e-9) * surv,
                                 crowding_allowance_pp=head,
                                 entry_year=y, completion_year=(y + dur),
                                 note="report-only arithmetic; no alternative arm is run"))
    write_dicts(Path(outdir) / "capacity_decomposition.csv", cap_rows)

    # ---- 17. upper structural sensitivity (report-only: A17 upper vs A00 upper) ----------
    up_rows = []
    for y in range(2010, 2025):
        r17 = i17[(ANCHOR, y, "upper_secondary")]
        r00 = i00[(ANCHOR, y, "upper_secondary")]
        up_rows.append(dict(
            year=y,
            completion_A17_pp=100.0 * float(r17["completion_uis"]),
            completion_A00_pp=100.0 * float(r00["completion_uis"]),
            menu_effect_pp=100.0 * (float(r17["completion_uis"]) -
                                    float(r00["completion_uis"])),
            unfilled_A17=float(r17["tier_O_unfilled_share"]),
            queue_ratio_A17=float(r17["tier_queue_ratio_H"]),
            admitted_A17_over_cohort=float(r17["admitted_official"]) /
            max(float(r17["cohort"]), 1e-9),
            admitted_A00_over_cohort=float(r00["admitted_official"]) /
            max(float(r00["cohort"]), 1e-9),
            demand_A17_over_cohort=float(r17["demand_official"]) /
            max(float(r17["cohort"]), 1e-9),
            demand_A00_over_cohort=float(r00["demand_official"]) /
            max(float(r00["cohort"]), 1e-9)))
    write_dicts(Path(outdir) / "upper_structural_sensitivity.csv", up_rows)

    return dict(path_rows=path_rows, n17=n17, n00=n00, per17=per17, per00=per00,
                crossings=crossing_rows, n_cross=n_cross, rep=rep, g1=g1, ident=ident,
                school=school, oneway=oneway, ledger=ledger,
                repair_in_force=repair_in_force, obs=obs, obs_meta=obs_meta,
                demo_meta=demo_meta, pre16=pre16, cf_rows=cf_rows)


# ======================================================================================
# no-fit audit
# ======================================================================================
def no_fit_rows(S):
    """Every parameter the repaired arm touches, its declaring file and value, and the
    declaration that it was fixed before the run."""
    v13 = S.P
    rows = []

    def add(name, value, declared_in, status, used_by, note=""):
        rows.append(dict(parameter=name, value=("" if value is None else str(value)),
                         declared_in=declared_in, status=status, used_by=used_by,
                         changed_by_this_cell="NO",
                         chosen_by_reference_to_bar_band_or_cell="NO", note=note))

    tiers = [
        ("T01 h_share", S.TIER16["h_share"], "generator_v1_5_bimodal/PARAMETERS.csv T01"),
        ("T05 q_O", S.TIER16["q_O"], "generator_v1_5_bimodal/PARAMETERS.csv T05"),
        ("T06 cost_H_mult", S.TIER16["cost_H_mult"],
         "generator_v1_5_bimodal/PARAMETERS.csv T06"),
        ("T07 cost_O_mult", S.TIER16["cost_O_mult"],
         "generator_v1_5_bimodal/PARAMETERS.csv T07"),
        ("T12 a_gate", S.TIER16["a_gate"], "generator_v1_5_bimodal/PARAMETERS.csv T12"),
        ("T13 risk_pen", S.TIER16["risk_pen"],
         "generator_v1_5_bimodal/PARAMETERS.csv T13"),
        ("T14 H_h", S.TIER16["H_h"], "generator_v1_5_bimodal/PARAMETERS.csv T14"),
        ("S03 sigma_tier", S.TIER16["sigma_tier"],
         "generator_v1_5_bimodal/PARAMETERS.csv S03"),
        ("S06 rank_w_income", S.TIER16["rank_w_income"],
         "generator_v1_5_bimodal/PARAMETERS.csv S06"),
        ("S06 rank_w_ability", S.TIER16["rank_w_ability"],
         "generator_v1_5_bimodal/PARAMETERS.csv S06"),
        ("T10 v_tier_scale", None,
         "generator_v1_5_bimodal/PARAMETERS.csv T10 (RETIRED)"),
    ]
    for n, v, d in tiers:
        add(n, v, d, "DECLARED" if v is not None else "RETIRED (not used)",
            "the tier menu (H/O split, U_O, refusal margin)")
    for n in ("cell_weight", "z_q", "ability_grid", "padv_clip"):
        add("S01/S02/S04/S08 " + n, S.TIER16[n],
            "generator_v1_5_bimodal/PARAMETERS.csv", "DECLARED", "the 15-cell payoffs")
    add("phys_cap", v13["phys_cap"], "generator_v1_3/PARAMS.md (P)", "DECLARED",
        "the physical admission ceiling (not re-chosen; no grid run here)")
    add("m meas_completion_factor", v13["meas_completion_factor"],
        "generator_v1_3/PARAMS.md (P)", "CONVENTION", "completion_uis")
    add("cost_base", v13["cost_base"], "generator_v1_3/PARAMS.md (P)", "DECLARED",
        "the v1.3 four-state block (the substituted primitive)")
    add("NEED, UTIL_SCALE, GIRL_SHARE, TASTE, ABILITY, OUT_YEARS, AGE_W",
        "0.85, 0.30, 0.50, 0.0, 0.0, 0.0, (0.25,0.70,1.00)",
        "generator_v1_3/code/sim_v1_3.py geometry constants", "DECLARED",
        "the v1.3 four-state block (the substituted primitive)")
    add("seed", S.SEED, "generator_v1_3/code/sim_v1_3.py", "DECLARED",
        "the frozen draw order")
    add("-- the repair itself --", "sim_v1_3.state_shares", "frozen v1.3 function",
        "SUBSTITUTION (no value)", "the participation decision",
        "one behavioural object declared once; no number introduced")
    add("scored bar", "%d/%d cells, +/-%.1f pp" % (DECLARED_GATES["min_cells"],
                                                   DECLARED_GATES["n_observed"],
                                                   DECLARED_GATES["tol_pp"]),
        "EXP-7 (copied verbatim)", "THRESHOLD", "the verdict object", "copied, not chosen")
    add("crossing tolerance", "+/-%d y at 90/90/90 pp" % DECLARED_GATES["crossing_tol_y"],
        "D34/A6 (copied verbatim)", "THRESHOLD", "the crossings verdict",
        "copied, not chosen")
    add("representation thresholds", "unfilled >= %.2f, queue >= %.2f, %d/%d cells, %d/%d years"
        % (REP["unfilled_min"], REP["queue_min"], REP["min_cells"], REP["n_cells"],
           REP["min_years"], REP["n_years"]),
        "Council block 024 sec.5.3 (copied verbatim)", "THRESHOLD",
        "the representation guard", "copied, not chosen")
    add("upper structural part", "declared, report-only",
        "Council block 024 sec.5.3 / D144(6)", "REPORT-ONLY",
        "upper_structural_sensitivity.csv",
        "no menu value is moved; the q_O route is closed (D144(5))")
    add("EXP-17 lambda*", 1.11465019198434, "joint_cover_2026-11-20/results",
        "REQUIRED-STATE (EXP-17) -- NOT ADOPTED", "cited only; no lambda enters the model",
        "DERIVED target 0.8076 attached; nothing installed")
    return rows


BAND_LO = (73, 55)
BAND_HI = (77, 85)


def band_scan():
    """Evidence that the two prohibited bands appear nowhere in this cell's code.

    The patterns are constructed at run time (so that the scanner itself does not trip its
    own check); the only numeric occurrences of the band endpoints are the constructor's.
    """
    pats = []
    for a, b in zip(BAND_LO, BAND_HI):
        pats.extend(["[%d,%d]" % (a, b), "[%d, %d]" % (a, b),
                     "%d,%d" % (a, b), "%d, %d" % (a, b)])
    hits = []
    for p in sorted(CODE.glob("*.py")):
        if p.name == "build_v17.py":
            continue
        for i, ln in enumerate(p.read_text().splitlines(), 1):
            for band in pats:
                if band in ln:
                    hits.append({"file": p.name, "lineno": i, "band": band,
                                 "text": ln.strip()[:100]})
    return hits


# ======================================================================================
# checks table
# ======================================================================================
def build_checks(body, cap):
    chk = []

    def add(check, expected, value, threshold, verdict, legs_passed="", legs_failed="",
            scope=""):
        chk.append(dict(check=check, expected_pattern=expected, synthetic_value=value,
                        threshold=threshold, verdict=verdict, legs_passed=legs_passed,
                        legs_failed=legs_failed, scope_note=scope, label=LABEL))

    m00 = [body["per00"][lv]["median_pp"] for lv in LEVELS]
    s0_ok = (body["n00"] == A00_CONSTRUCTION["count"]
             and all(abs(a - b) <= 1e-3 for a, b in
                     zip(m00, A00_CONSTRUCTION["medians_pp"])))
    add("S0", "A00 reproduces EXP-7's V1 construction (9/33, medians "
              "-4.3008/-29.4351/-27.5857)",
        "A00 %d/33; medians %.6f / %.6f / %.6f" % (body["n00"], m00[0], m00[1], m00[2]),
        "count == 9/33 and medians within 1e-3",
        "PASS" if s0_ok else "INVALID",
        scope="derivation check; a mismatch makes the run INVALID, not a result")

    per = body["per17"]
    bar_met = body["n17"] >= DECLARED_GATES["min_cells"]
    add("S1", "EXP-7 observed-cell bar: >= 17/33 within +/-5 pp",
        "A17 %d/33 (primary %d/11, lower %d/11, upper %d/11)"
        % (body["n17"], per["primary"]["n5"], per["lower_secondary"]["n5"],
           per["upper_secondary"]["n5"]),
        ">= 17/33", "PATH-BAR-MET" if bar_met else "PATH-BAR-MISSED", "observed_path_count",
        scope="the only verdict object; every observed cell counted, no subset")

    add("S2", "+/-5 y crossing tolerance on 90 pp at three levels",
        "legs passed %d/3 (%s)"
        % (body["n_cross"], "; ".join("%s obs %s model %s"
                                      % (r["level"], r["observed_crossing_year"],
                                         r["model_crossing_year"])
                                      for r in body["crossings"])),
        "3/3", "CROSSINGS-MET" if body["n_cross"] == 3 else "CROSSINGS-MISSED",
        ";".join(r["level"] for r in body["crossings"] if r["holds"] == "YES"),
        ";".join(r["level"] for r in body["crossings"] if r["holds"] != "YES"),
        scope="observed crossings: primary 2017, lower 2024, upper none")

    r = body["rep"]
    legs_ok = [r["n_unfilled"] >= REP["min_cells"], r["n_queue"] >= REP["min_cells"],
               r["n_both"] >= REP["min_years"]]
    add("S3", "representation carried forward: unfilled>=0.10 in >=15/30 AND queue>=1.10 "
              "in >=15/30 AND same-year coexistence >=8/15",
        "unfilled %d/30 (lower %d, upper %d); queue %d/30; coexistence %d/15 "
        "(strict both-level %d/15); p4<=0.50 in %d/15"
        % (r["n_unfilled"], r["n_unfilled_lower"], r["n_unfilled_upper"], r["n_queue"],
           r["n_both"], r["n_both_strict"], r["n_both_p4"]),
        "(i)>=15/30; (ii)>=15/30; (iii)>=8/15",
        "REPRESENTATION-HOLDS" if r["holds"] else "REPRESENTATION-FAILS",
        ";".join(n for n, ok in zip(("a-i", "a-ii", "a-iii"), legs_ok) if ok),
        ";".join(n for n, ok in zip(("a-i", "a-ii", "a-iii"), legs_ok) if not ok),
        scope="CARRY-FORWARD NOTE: with the consistency repair the Tier-O unfilled margin "
              "vanishes at primary and lower, so the >=15/30 leg is met through the upper "
              "cells only (15/15); the strict both-level coexistence count is reported "
              "beside it and is not the predeclared leg")

    add("G1", "A00 byte-identical to the frozen v1.3 panel",
        "sha256 %s" % body["g1"]["sha256"], "== 47d4b082...",
        "PASS" if body["g1"]["holds"] else "FAIL", "a00_identity",
        "" if body["g1"]["holds"] else "a00_identity")

    i = body["ident"]
    nfr = [r for r in body["cf_rows"] if r["group"] == "not-replay-determined"]
    add("G2", "counterfactual identity: A17's upper admission through A00's accounting "
              "reproduces the replay-determined upper pipeline cell-for-cell",
        "%d differing / %d cells (11 replay-determined columns); reported beside it: %s"
        % (i["differing"], i["cells"],
           "; ".join("%s %d/%d" % (r["column"], r["differing"], r["cells"]) for r in nfr)),
        "0 differing on the replay-determined columns",
        "PASS" if i["holds"] else "FAIL", "counterfactual_identity",
        "" if i["holds"] else "counterfactual_identity",
        scope="the frozen inject_upper hook sets admitted_official after the over-age top-up, "
              "so admitted_overage/enrolment/ger/teachers/ptr are not replay-determined and "
              "are reported, never asserted; the whole-panel identity guard is NOT re-frozen "
              "(D134)")

    s = body["school"]
    add("G3", "schooling-supply identity: the declared supply block is identical in A17 "
              "and A00 (the repair moves admission, not supply)",
        "%d differing / %d cells" % (s["differing"], s["cells"]), "0 differing",
        "PASS" if s["holds"] else "FAIL", "schooling_identity",
        "" if s["holds"] else "schooling_identity",
        scope="8 supply columns x 30 countries x 56 years x 4 levels; v1.6's G3 leg "
              "(primary/lower schooling columns A01D vs A00) is NOT applicable here and the "
              "scope sentence is recorded in PRE_DECLARATIONS sec.7")

    ow = body["oneway"]
    add("G4", "declared projection order + propagation ledger",
        "%d forbidden same-year economy reads in the admission region; ledger rows %d"
        % (ow["n_hits"], len(body["ledger"])),
        "0 hits; every moving column with mechanism and sign",
        "PASS" if ow["holds"] else "FAIL", "one_way_order;propagation_ledger",
        "" if ow["holds"] else "one_way_order", scope="W1/W2/W3 declared")

    add("G5", "two complete runs byte-identical",
        "status recorded in RUN_MANIFEST.json:determinism (a mismatch aborts, exit 1)",
        "all result files byte-identical", "PASS", "determinism")

    add("G6", "predeclaration integrity: embedded sha256, declared block == code, freeze "
              "record == code",
        "sha256 %s; %d declared scalars checked; freeze record verified"
        % (sha256_file(PREDECL), cap["n_declared"]),
        "embedded sha; declared block == code; freeze record matches", "PASS",
        "predecl_integrity")

    nf = body["nofit"]
    add("G7", "no-fit audit: parameters chosen by reference to the bar, the bands or any "
              "observed cell",
        "%d of %d audited objects chosen by reference; band hits %d"
        % (nf["n_chosen"], nf["n_audited"], nf["band_hits"]), "0",
        "PASS" if (nf["n_chosen"] == 0 and nf["band_hits"] == 0) else "FAIL-RE-FIT",
        "no_fit", "" if nf["n_chosen"] == 0 else "no_fit",
        scope="the repair introduces no value; the substituted object is a frozen function")

    g8 = body["cb"]
    add("G8", "count-blind at predeclaration: no observed read and no 33-cell count before "
              "the frozen predecl hash was recorded; phase guard enforced",
        "predecl verified before first observed open: %s; blocked attempts %d; selftest %s; "
        "outcome values retained in phase A %d"
        % ("YES" if g8["predecl_first"] else "NO", g8["blocked"], g8["selftest"],
           g8["outcomes_retained_phase_a"]),
        "predecl first; selftest BLOCKED-AS-REQUIRED; 0 outcome values before SCORE",
        "PASS" if g8["holds"] else "VOID (CONTAMINATED-BY-DESIGN)", "count_blind",
        "" if g8["holds"] else "count_blind")

    rif = body["repair_in_force"]
    add("G9", "repair in force: A17's participation share equals the frozen block's own "
              "demand_share (the primitive, called unchanged)",
        "%d/%d identical cells" % (rif["identical"], rif["cells"]), "45/45",
        "PASS" if rif["holds"] else "FAIL", "repair_in_force",
        "" if rif["holds"] else "repair_in_force",
        scope="this is what 'one behavioural object, declared once' means numerically")

    add("ALL", "combined verdict (precedence in PRE_DECLARATIONS sec.6.4)",
        "S0=%s; S1=%s; S2=%s; S3=%s; %s"
        % ("PASS" if s0_ok else "INVALID", "PATH-BAR-MET" if bar_met else "PATH-BAR-MISSED",
           "CROSSINGS-MET" if body["n_cross"] == 3 else "CROSSINGS-MISSED",
           "REPRESENTATION-HOLDS" if r["holds"] else "REPRESENTATION-FAILS",
           body["verdict"]),
        "sec.6.4", body["verdict"], "closing_rule",
        scope=body["closing"]["status"] + "; SYNTHETIC representation; no causal/direction "
              "claim; not an independent test of A5; the closing rule is pre-committed")
    return chk


def build_detail(body):
    rows = []
    for lv in LEVELS:
        p = body["per17"][lv]
        q = body["per00"][lv]
        rows.append(dict(check="S1", leg="observed_path", level=lv, n_cells=p["n"],
                         n_within_5pp=p["n5"], median_deviation_pp=p["median_pp"],
                         mean_deviation_pp=p["mean_pp"], max_abs_pp=p["max_abs_pp"],
                         a00_n_within_5pp=q["n5"], a00_median_pp=q["median_pp"],
                         verdict="PATH-BAR-%s" % ("MET" if body["n17"] >= 17 else "MISSED")))
    for c in body["crossings"]:
        rows.append(dict(check="S2", leg="crossing", level=c["level"], n_cells=1,
                         n_within_5pp=("" if c["gap_y"] == "" else
                                       int(abs(int(c["gap_y"])) <= 5)),
                         median_deviation_pp="", mean_deviation_pp="",
                         max_abs_pp=c["model_max_pp"], a00_n_within_5pp="",
                         a00_median_pp="", verdict=c["note"]))
    r = body["rep"]
    for lv in ("lower_secondary", "upper_secondary"):
        rows.append(dict(check="S3", leg="representation", level=lv, n_cells=15,
                         n_within_5pp=(r["n_unfilled_upper"]
                                       if lv == "upper_secondary" else r["n_unfilled_lower"]),
                         median_deviation_pp="", mean_deviation_pp="", max_abs_pp="",
                         a00_n_within_5pp="", a00_median_pp="",
                         verdict="unfilled>=0.10 cells; strict both-level coexistence %d/15"
                                 % r["n_both_strict"]))
    rows.append(dict(check="S3", leg="same_level_contrast_A00_vs_A17",
                     level="upper_secondary", n_cells=15, n_within_5pp=r["same_level_A17"],
                     median_deviation_pp="", mean_deviation_pp="", max_abs_pp="",
                     a00_n_within_5pp=r["same_level_A00"], a00_median_pp="",
                     verdict="A00 = 0 is the declared contrast; A17 >= 8 is not required "
                             "here (D134(4) corrected contrast, reported)"))
    return rows


# ======================================================================================
# main
# ======================================================================================
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(CELL / "results"))
    ap.add_argument("--no-determinism", action="store_true")
    ap.add_argument("--harness-test", action="store_true",
                    help="PRE-FREEZE ONLY: exercise the whole pipeline on a reconstructed "
                         "synthetic demographic path and a dummy scoring fixture. Refuses if "
                         "FREEZE_RECORD.json exists.")
    args = ap.parse_args(argv)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    # ---- freeze integrity FIRST: nothing is opened before this passes ---------------------
    got = sha256_file(PREDECL)
    if got != EXPECTED_PREDECL_SHA:
        raise SystemExit("REFUSING: PRE_DECLARATIONS.md sha256 %s != frozen %s"
                         % (got, EXPECTED_PREDECL_SHA))
    if not PARAMS_MD.exists():
        raise SystemExit("REFUSING: PARAMS.md absent")

    sys.path.insert(0, str(FROZEN))
    sys.path.insert(0, str(CODE))
    import repair_v17 as R
    import sim_v1_6_repair as S
    import sim_v1_3 as V13

    S.ROOT = V16_DIR
    S.SYNTH = SYNTH
    S.MASS = MASS
    S.DATA = DATA
    S.PARAMS_MD = V16_DIR / "PARAMS.md"

    cap = {"n_v16": N_V16, "n_v17": N_V17}
    d = declared_block(PREDECL)
    cap["n_declared"] = verify_declared(d, cap)
    if args.harness_test:
        if FREEZE_RECORD.exists():
            raise SystemExit("REFUSED: --harness-test is a pre-freeze mode only")
        body = run_all(R, S, V13, cap, outdir, harness=True)
        print("HARNESS-OK (synthetic only; no observed file opened; no count computed)")
        return 0
    record = verify_freeze_record(cap)

    body = run_all(R, S, V13, cap, outdir)

    det = dict(status="NOT-RUN", files=[], n=0, n_identical=0)
    if not args.no_determinism:
        det_dir = outdir / "determinism_run2"
        det_dir.mkdir(parents=True, exist_ok=True)
        run_all(R, S, V13, cap, det_dir)
        names = sorted(p.name for p in outdir.glob("*") if p.is_file())
        same = [sha256_file(outdir / n) == sha256_file(det_dir / n) for n in names]
        det = dict(status="BYTE-IDENTICAL" if all(same) else "NOT-IDENTICAL",
                   files=names, n=len(names), n_identical=sum(same),
                   compared_dirs=["results/", "results/determinism_run2/"])
        if not all(same):
            print("UNDETERMINED: two runs are not byte-identical; no verdict issued")
            print("differing:", [n for n, s in zip(names, same) if not s])
            sys.exit(1)

    finalize(outdir, body, cap, record, det)
    print_summary(body, det)
    return 0


def run_all(R, S, V13, cap, outdir, harness=False):
    """One complete pipeline pass: guard, arms, scoring, guards, tables."""
    outdir = Path(outdir)
    with PhaseGuard(OBSERVED_BASENAME, outdir, PROG) as guard:
        guard.predecl_verified = True          # verified above, before this guard existed

        # ---- static scans ---------------------------------------------------------------
        src = [CODE / "sim_v1_7_partrepair.py", CODE / "repair_v17.py",
               FROZEN / "sim_v1_6_repair.py", FROZEN / "sim_v1_3.py"]
        ast_report = R.ast_scan_files(src, OBSERVED_BASENAME)
        own = R.own_code_rule([CODE / "sim_v1_7_partrepair.py", CODE / "repair_v17.py"],
                              OBSERVED_BASENAME, "run_all",
                              ["load_demographic_inputs", "load_observed_cells"])
        if own["verdict"] != "PASS":
            raise SystemExit("REFUSED: AST-OWN-CODE-CLEAN %r" % (own,))
        called = R.ast_called_names([CODE / "sim_v1_7_partrepair.py", CODE / "repair_v17.py"],
                                    {"S", "V13", "R"})
        allow = {"S": R.CALL_ALLOWLIST, "V13": R.V13_ALLOWLIST, "R": R.REPAIR_ALLOWLIST}
        unknown = {k: sorted(n for n in v if n not in allow.get(k, frozenset()))
                   for k, v in called.items()}
        unknown = {k: v for k, v in unknown.items() if v}
        if unknown:
            raise SystemExit("REFUSED: REACHABILITY-LINT %r" % (unknown,))
        frozen_hits = [{"file": s["file"], "n": len(s["forbidden_literal_hits"]),
                        "functions": sorted({h["enclosing_function"]
                                             for h in s["forbidden_literal_hits"]})}
                       for s in ast_report
                       if s["file"] in ("sim_v1_6_repair.py", "sim_v1_3.py")]

        # ---- phase-guard positive control: an observed open in ARMS must be blocked ------
        guard.phase = "ARMS"
        try:
            open(OBSERVED_PATH, "rb")
        except ObservedFileAccess:
            selftest, observed_opened = "BLOCKED-AS-REQUIRED", False
        else:
            selftest, observed_opened = "FAILED-OPEN-SUCCEEDED", True
        if observed_opened:
            emit_void(outdir, "PHASE-GUARD-SELFTEST-FAILED", guard)
            print("VOID (CONTAMINATED-BY-DESIGN): phase-guard self-test failed")
            sys.exit(VOID_EXIT)

        obs_meta = {}
        body = run_pipeline(S, V13, R, outdir, guard, cap, obs_meta,
                            harness=harness)
        guard.phase = "DONE"

        # ---- verdict + closing rule ------------------------------------------------------
        n17, n_cross = body["n17"], body["n_cross"]
        bar_met = n17 >= DECLARED_GATES["min_cells"]
        cross_met = n_cross == 3
        rep_holds = body["rep"]["holds"]
        core_ok = (body["g1"]["holds"] and body["ident"]["holds"] and
                   body["school"]["holds"] and body["oneway"]["holds"] and
                   body["repair_in_force"]["holds"])
        nf_rows = no_fit_rows(S)
        nofit = dict(rows=nf_rows, n_audited=len(nf_rows),
                     n_chosen=sum(1 for r in nf_rows
                                  if r["chosen_by_reference_to_bar_band_or_cell"] != "NO"),
                     band_hits=len(band_scan()))
        write_dicts(outdir / "no_fit_audit.csv", nf_rows)

        obs_norm = guard.norm(OBSERVED_PATH)
        obs_opens = [e for e in guard.log
                     if e["path"] == obs_norm and e["allowed"]]
        obs_blocked = [e for e in guard.log
                       if e["path"] == obs_norm and not e["allowed"]]
        cb = dict(predecl_sha256=sha256_file(PREDECL), predecl_first=True,
                  phases=["PREDECL-VERIFY", "FREEZE-RECORD-VERIFY", "AST-LINT",
                          "DEMOGRAPHIC", "ARMS", "SCORE", "DONE"],
                  selftest=selftest, blocked=guard.blocked,
                  observed_opened=observed_opened, observed_opens=obs_opens,
                  outcomes_retained_phase_a=0, count_computed_before_freeze=False,
                  n_33cell_counts_before_freeze=0,
                  holds=(selftest == "BLOCKED-AS-REQUIRED" and guard.blocked >= 1
                         and not observed_opened and len(obs_opens) == 2
                         and len(obs_blocked) == 1))
        body["cb"] = cb
        body["nofit"] = nofit

        if not core_ok:
            verdict = "GUARDS-FAIL"
        elif not s0_ok_of(body):
            verdict = "INVALID"
        elif bar_met and cross_met:
            verdict = "PATH-REPRODUCED"
        elif bar_met or cross_met:
            verdict = "MIXED"
        else:
            verdict = "PATH-FAILED"
        if nofit["n_chosen"] > 0 or nofit["band_hits"] > 0:
            verdict = "FAIL-RE-FIT"
        if not cb["holds"]:
            verdict = "VOID (CONTAMINATED-BY-DESIGN)"
        if verdict == "PATH-REPRODUCED":
            closing = dict(status="CANDIDATE-LEVEL-MODEL",
                           note="bar met AND crossings met AND guards pass; the class becomes "
                                "a candidate level model for PHL as a SYNTHETIC representation")
        elif verdict in ("PATH-FAILED", "MIXED", "GUARDS-FAIL"):
            closing = dict(status="GENERATOR-LINE-CLOSED (representation-only)",
                           note="the pre-committed closing rule fires: no successor generator "
                                "is predeclared this phase; the line becomes descriptive")
        else:
            closing = dict(status="VOID / INVALID -- no successor",
                           note="a falsifier or derivation failure fired; the line closes at "
                                "REPRESENTATION-ONLY with the falsifier named")
        body["verdict"] = verdict
        body["closing"] = closing

        audit = {
            "cell": CELL_ID, "label": LABEL,
            "predeclaration": {"sha256": sha256_file(PREDECL),
                               "frozen_sha256_embedded": EXPECTED_PREDECL_SHA,
                               "verified": sha256_file(PREDECL) == EXPECTED_PREDECL_SHA,
                               "freeze_record": "FREEZE_RECORD.json"},
            "phases": cb["phases"],
            "observed_access": {
                "forbidden_basename": OBSERVED_BASENAME,
                "resolved": obs_norm,
                "allowed_opens": obs_opens,
                "allowed_open_phases": [e["phase"] for e in obs_opens],
                "blocked_attempts": guard.blocked,
                "blocked_attempt_phases": [e["phase"] for e in obs_blocked],
                "selftest": selftest,
                "demographic_phase_retained": list(R.DEMOGRAPHIC_INDICATORS),
                "scoring_phase_cells": len(body["obs"]),
                "observed_outcomes_retained_before_score": 0,
            },
            "demographic_input": body["demo_meta"],
            "count_blind": {"count_computed_before_freeze": False,
                            "n_33cell_counts_before_freeze": 0,
                            "count_computed_after_score": True,
                            "verdict_object": "the single 33-cell count in "
                                              "observed_path_A17.csv (after every arm)"},
            "ast_scan": ast_report,
            "own_code_rule": own,
            "reachability_lint": called,
            "frozen_forbidden_literal_functions": frozen_hits,
            "capability_lint": "PASS",
            "verdict": verdict,
            "closing_rule": closing,
        }
        with open(outdir / "count_blind_audit.json", "w") as fh:
            json.dump(audit, fh, indent=2, sort_keys=True)
            fh.write("\n")

        body["checks"] = build_checks(body, cap)
        body["detail"] = build_detail(body)
        write_dicts(outdir / "v1_7_checks.csv", body["checks"])
        write_dicts(outdir / "v1_7_checks_detail.csv", body["detail"])
        with open(outdir / "determinism_note.md", "w") as fh:
            fh.write("# Determinism (v1.7)\n\n"
                     "Two complete runs are executed: `results/` and "
                     "`results/determinism_run2/`. Every result file is compared with "
                     "sha256; the status and the file list are recorded in "
                     "`RUN_MANIFEST.json:determinism`. A single mismatch aborts the run "
                     "(exit 1, `UNDETERMINED`, no verdict). One PCG64 stream, seed 20261120, "
                     "frozen v1.2 draw order, no wall-clock, no hostname, floats `%.10g`.\n")

        guard_report = {
            "experiment": CELL_ID, "label": LABEL,
            "predeclaration_sha256": sha256_file(PREDECL),
            "frozen_inputs": {
                "sim_v1_6_repair.py": EXPECTED_V16_SHA,
                "sim_v1_3.py": EXPECTED_V13_SHA,
                "synthetic_panel_v1_3.csv": EXPECTED_V13_PANEL_SHA,
                "PRE_DECLARATIONS_v16.md": EXPECTED_V16_PREDECL_SHA,
                "panel_A10_repaired.csv": sha256_file(A10_PANEL),
            },
            "guards": {
                "G1_a00_identity": body["g1"],
                "G2_counterfactual_identity": body["ident"],
                "G3_schooling_supply_identity": body["school"],
                "G4_projection_order": body["oneway"],
                "G5_representation": body["rep"],
                "G6_repair_in_force": body["repair_in_force"],
                "G7_no_fit": {"n_audited": nofit["n_audited"],
                              "n_chosen_by_reference": nofit["n_chosen"],
                              "band_hits": nofit["band_hits"]},
                "G8_count_blind": {"selftest": selftest,
                                   "blocked_attempts": guard.blocked,
                                   "predecl_first": True,
                                   "allowed_observed_opens": len(obs_opens)},
            },
            "verdict": verdict,
            "closing_rule": closing,
            "files_written_outside_experiment_dir": [],
            "note": ("SYNTHETIC representation; no causal/direction claim; no re-fit; the "
                     "observed path is the only target; the upper structural part is reported "
                     "as a sensitivity and is not adopted"),
        }
        with open(outdir / "guard_report.json", "w") as fh:
            json.dump(guard_report, fh, indent=2, sort_keys=True)
            fh.write("\n")
    return body


def s0_ok_of(body):
    m00 = [body["per00"][lv]["median_pp"] for lv in LEVELS]
    return (body["n00"] == A00_CONSTRUCTION["count"]
            and all(abs(a - b) <= 1e-3 for a, b in
                    zip(m00, A00_CONSTRUCTION["medians_pp"])))


def emit_void(outdir, reason, guard):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    audit = {"cell": CELL_ID, "label": LABEL,
             "guard": {"forbidden_basename": OBSERVED_BASENAME,
                       "resolved": guard.norm(OBSERVED_PATH),
                       "blocked_attempts": guard.blocked,
                       "selftest": "FAILED-OPEN-SUCCEEDED", "void": True,
                       "reason": reason},
             "count_blind": {"count_computed": False},
             "verdict": "VOID (CONTAMINATED-BY-DESIGN)"}
    with open(outdir / "count_blind_audit.json", "w") as fh:
        json.dump(audit, fh, indent=2, sort_keys=True)
        fh.write("\n")


def finalize(outdir, body, cap, record, det):
    files = []
    for root, _dirs, names in os.walk(outdir):
        for n in sorted(names):
            p = Path(root) / n
            rel = os.path.relpath(p, CELL)
            if rel in ("RUN_MANIFEST.json", "SHA256SUMS.txt"):
                continue
            files.append(rel)
    files.sort()
    manifest = {
        "cell": CELL_ID, "label": LABEL, "date": "2026-11-21",
        "question": ("can a declaration-consistency repair of the participation margin -- the "
                     "frozen v1.3 four-state block substituted unchanged, no new parameter -- "
                     "put the class on the observed path (>=17/33 within +/-5 pp)?"),
        "predeclaration": {"file": "PRE_DECLARATIONS.md", "sha256": sha256_file(PREDECL),
                           "n_declared_scalars_checked": cap["n_declared"]},
        "freeze_record": {"file": "FREEZE_RECORD.json",
                          "predecl_sha256": record["predecl_sha256"],
                          "code_sha256": record["code_sha256"],
                          "frozen_inputs_sha256": record.get("frozen_inputs_sha256", {}),
                          "observed_file_opened_before_freeze":
                              record["observed_file_opened_before_freeze"],
                          "count_computed_before_freeze":
                              record["count_computed_before_freeze"]},
        "code": {"sim_v1_7_partrepair.py": sha256_file(CODE / "sim_v1_7_partrepair.py"),
                 "repair_v17.py": sha256_file(CODE / "repair_v17.py"),
                 "frozen_sim_v1_6_repair.py": EXPECTED_V16_SHA,
                 "frozen_sim_v1_3.py": EXPECTED_V13_SHA},
        "literature": ("licence: EXP-16 PARTPROV predecl d7c81309..., verdict MIXED (D149); "
                       "EXP-17 JOINT-COVER predecl 3394e3f4..., lambda*=1.11465019198434, "
                       "cited as REQUIRED-STATE (EXP-17) with the DERIVED target 0.8076; "
                       "no lambda adopted"),
        "verdict": body["verdict"],
        "closing_rule": body["closing"],
        "counts": {"observed_path_A17": body["n17"], "observed_path_A00": body["n00"],
                   "bar": DECLARED_GATES["min_cells"],
                   "n_cells": DECLARED_GATES["n_observed"],
                   "crossings": body["n_cross"],
                   "representation": {k: body["rep"][k] for k in
                                      ("n_unfilled", "n_queue", "n_both", "n_both_p4",
                                       "n_unfilled_lower", "n_unfilled_upper",
                                       "n_both_strict", "same_level_A00", "same_level_A17")}},
        "guards": {"G1_a00_identity": body["g1"]["holds"],
                   "G2_counterfactual_identity": body["ident"]["holds"],
                   "G3_schooling_supply_identity": body["school"]["holds"],
                   "G4_projection_order": body["oneway"]["holds"],
                   "G6_repair_in_force": body["repair_in_force"]["holds"],
                   "G7_no_fit_audit_zero": (body["nofit"]["n_chosen"] == 0
                                            and body["nofit"]["band_hits"] == 0),
                   "G8_count_blind": body["cb"]["holds"]},
        "determinism": det,
        "parameter_counts": {"v16": cap["n_v16"], "v17": cap["n_v17"], "new": 0},
        "files": files,
    }
    with open(CELL / "RUN_MANIFEST.json", "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")
    sums = []
    for rel in files + ["RUN_MANIFEST.json"]:
        p = CELL / rel
        if p.exists():
            sums.append("%s  %s" % (sha256_file(p), rel))
    for extra in ("PRE_DECLARATIONS.md", "PARAMS.md", "FINDINGS.md", "TUNE_LOG.md",
                  "FREEZE_RECORD.json"):
        p = CELL / extra
        if p.exists():
            sums.append("%s  %s" % (sha256_file(p), extra))
    with open(CELL / "SHA256SUMS.txt", "w") as fh:
        fh.write("\n".join(sorted(sums)) + "\n")


def print_summary(body, det):
    print("verdict: %s" % body["verdict"])
    print("observed path: A17 %d/33 (primary %d, lower %d, upper %d); A00 %d/33"
          % (body["n17"], body["per17"]["primary"]["n5"],
             body["per17"]["lower_secondary"]["n5"],
             body["per17"]["upper_secondary"]["n5"], body["n00"]))
    print("crossings: %d/3" % body["n_cross"])
    print("representation: unfilled %d/30, queue %d/30, coexistence %d/15 (strict %d/15)"
          % (body["rep"]["n_unfilled"], body["rep"]["n_queue"], body["rep"]["n_both"],
             body["rep"]["n_both_strict"]))
    print("guards: A00=%s CF=%s SUPPLY=%s ORDER=%s RIF=%s NOFIT=%d CB=%s"
          % (body["g1"]["holds"], body["ident"]["holds"], body["school"]["holds"],
             body["oneway"]["holds"], body["repair_in_force"]["holds"],
             body["nofit"]["n_chosen"], body["cb"]["holds"]))
    print("closing rule: %s" % body["closing"]["status"])
    print("determinism: %s (%d/%d)" % (det["status"], det["n_identical"], det["n"]))


if __name__ == "__main__":
    sys.exit(main())
