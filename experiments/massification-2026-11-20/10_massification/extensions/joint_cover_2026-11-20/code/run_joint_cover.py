#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXP-17 JOINT-COVER -- is there ONE declared coverage path that satisfies BOTH lower channels?

Deterministic arithmetic on the frozen v1.2 panel plus the declared laws:

    F(lam) = m * min(1.15*lam*seats(2018), 1.05*cohort(2018)) / cohort(2018)
                * 0.91 * exp(-0.55 * max(0, cohort(2021)/(lam*seats(2021)) - 1))

Solve F(lam) = 0.8076 for lam in [0.5, 2.0], m = 1.10 frozen.
Verdicts (precedence in PRE_DECLARATIONS.md section 5.1):
    UNDETERMINED  >  MULTIPLE  >  LAW-INCOMPATIBLE  >  SINGLE-LEVER-IDENTIFIED

No RNG, no clock, no network, no generator run. All inputs are read-only.
Refuses to run if PRE_DECLARATIONS.md's sha256 differs from the frozen value embedded below.

Usage:  python3 code/run_joint_cover.py --outdir results
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys

# ----------------------------------------------------------------------------- frozen identity
PRE_DECL_SHA256 = "3394e3f4f085d73e62fa5b07e11270dcc53357516935f2f6975129d3c15ee271"

# ----------------------------------------------------------------------------- declared constants
M_FACTOR = 1.10          # CONVENTION  meas_completion_factor   sim_v1_2.py:133
PHYS_CAP = 1.15          # DECLARED    phys_cap                sim_v1_2.py:109
OVERAGE_CAP = 1.05       # CONVENTION  overage_cap             sim_v1_2.py:110
SURV_MAX = 0.91          # DECLARED    surv_max[lower]         sim_v1_2.py:113
GAMMA = 0.55             # DECLARED    gamma                   sim_v1_2.py:112
SURV_THETA = 1.0         # DECLARED    surv_theta[lower]       sim_v1_2.py:114
DVEC_LOWER = 3           # DECLARED    duration, lower         sim_v1_2.py:65
SURV_CLIP_LO = 0.02      # DECLARED    survival clip           PARAMS.md 4.1
SURV_CLIP_HI = 0.995

TARGET = 0.8076                  # DERIVED  76.6391/0.949 -> 80.7577 -> 80.76 at 2 dp (D133/D140)
LAM_LO, LAM_HI = 0.5, 2.0        # DECLARED (block clause 5)
FALSIFIER_TOL = 1e-9             # DECLARED (block clause 5)

GRID_N = 6001                    # DECLARED here
GRID_STEP = (LAM_HI - LAM_LO) / (GRID_N - 1)
ROOT_TOL = 1e-12                 # DECLARED here, absolute residual
WIDTH_TOL = 1e-12                # DECLARED here, bracket width
METHOD_TOL = 1e-9                # DECLARED here, bisection vs Newton in lam
BISECT_MAX_ITER = 300
NEWTON_MAX_ITER = 100
NEWTON_X0 = 1.2                  # numerical seed, declared in section 4.4

COUNTRY = "SYN00_PHL_LIKE"
LEVEL = "lower_secondary"
YEAR_COMPLETION = 2021
YEAR_ENTRY = YEAR_COMPLETION - DVEC_LOWER

CONTEXT_YEARS = (2017, 2019, 2020, 2022, 2023, 2024)   # section 6.2 item 4, non-verdict-bearing
TARGET_OBSERVED_REF = 0.808960494995                    # OBSERVED, reference only (section 6.2 item 5)
PROVENANCE_DELTA_PP = 0.136049                          # D142: observed minus internal


# ----------------------------------------------------------------------------- helpers
def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt(x, sig=12) -> str:
    if x is None:
        return ""
    if isinstance(x, bool):
        return "TRUE" if x else "FALSE"
    if isinstance(x, (int,)):
        return str(x)
    if isinstance(x, str):
        return x
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return repr(x)
        return f"{x:.{sig}g}"
    return str(x)


def find_programme_root(start: str) -> str:
    d = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "08_council", "DECISIONS.md")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("CAPABILITY-LINT-FAIL: programme root (08_council/DECISIONS.md) not found above %s" % start)


# ----------------------------------------------------------------------------- the declared law
def gate_term(lam: float, seats_entry: float, cohort_entry: float):
    """min(phys_cap*lam*seats, overage_cap*cohort)/cohort and the binding branch."""
    phys = PHYS_CAP * lam * seats_entry
    over = OVERAGE_CAP * cohort_entry
    term = phys if phys <= over else over
    branch = "phys_cap" if phys <= over else "overage_cap"
    return term / cohort_entry, branch


def survival_term(lam: float, cohort_completion: float, seats_completion: float):
    """0.91*exp(-0.55*max(0, q-1)) with q = cohort/(lam*seats); plus clip status."""
    q = cohort_completion / (lam * seats_completion)
    quality = math.exp(-GAMMA * max(0.0, q - 1.0))
    s = SURV_MAX * (quality ** SURV_THETA)
    s_clipped = min(max(s, SURV_CLIP_LO), SURV_CLIP_HI)
    clip_active = (s_clipped != s)
    return q, quality, s, s_clipped, clip_active


def evaluate(lam, cell):
    g, branch = gate_term(lam, cell["seats_entry"], cell["cohort_entry"])
    q, quality, s, s_clipped, clip_active = survival_term(lam, cell["cohort_completion"], cell["seats_completion"])
    f = M_FACTOR * g * s_clipped
    return {
        "lam": lam, "gate": g, "branch": branch, "q": q, "quality": quality,
        "survival": s_clipped, "clip_active": clip_active, "F": f, "residual": f - cell["target"],
    }


def newton_root(cell):
    """Newton on the smooth binding branch: F' = F*(1 + 0.55*q/lam)/lam."""
    q = cell["cohort_completion"] / cell["seats_completion"]
    lam = NEWTON_X0
    trace = []
    for it in range(1, NEWTON_MAX_ITER + 1):
        e = evaluate(lam, cell)
        f = e["F"]
        deriv = f * (1.0 + GAMMA * q / lam) / lam
        step = (f - cell["target"]) / deriv
        lam_new = lam - step
        trace.append((it, lam, step, f - cell["target"]))
        if abs(f - cell["target"]) <= 1e-15 or abs(lam_new - lam) <= 1e-15:
            lam = lam_new
            break
        lam = lam_new
    return lam, trace, evaluate(lam, cell)


def bisect_root(lo, hi, cell):
    f_lo = evaluate(lo, cell)["residual"]
    f_hi = evaluate(hi, cell)["residual"]
    trace = []
    mid = 0.5 * (lo + hi)
    for it in range(1, BISECT_MAX_ITER + 1):
        mid = 0.5 * (lo + hi)
        f_mid = evaluate(mid, cell)["residual"]
        width = hi - lo
        trace.append((it, lo, hi, f_lo, f_hi, mid, f_mid, width))
        if width <= 1e-13 or abs(f_mid) <= 1e-15:
            break
        if f_lo * f_mid <= 0.0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    width = hi - lo
    return mid, width, f_mid, trace


def scan(cell):
    """Grid scan over the declared bracket: sign changes, exact zeros, plateau intervals."""
    xs, fs = [], []
    for i in range(GRID_N):
        lam = LAM_LO + (LAM_HI - LAM_LO) * i / (GRID_N - 1)
        xs.append(lam)
        fs.append(evaluate(lam, cell)["residual"])
    brackets, zeros, plateaus = [], [], []
    for i in range(GRID_N - 1):
        a, b, fa, fb = xs[i], xs[i + 1], fs[i], fs[i + 1]
        if fa * fb < 0.0:
            brackets.append((a, b, fa, fb))
        elif fa == 0.0:
            zeros.append(a)
        if abs(fa) <= ROOT_TOL and abs(fb) <= ROOT_TOL:
            plateaus.append((a, b))
    if abs(fs[-1]) == 0.0:
        zeros.append(xs[-1])
    # de-duplicate exact zeros adjacent to a sign-change bracket (counted once, inside the bracket)
    dedup = []
    for z in zeros:
        if any(abs(z - b[0]) <= GRID_STEP or abs(z - b[1]) <= GRID_STEP for b in brackets):
            continue
        dedup.append(z)
    decreases = sum(1 for i in range(GRID_N - 1) if (fs[i] - fs[i + 1]) > 1e-12)
    return {"x": xs, "f": fs, "brackets": brackets, "zeros": dedup,
            "plateaus": plateaus, "decreases": decreases}


def solve_cell(cell, want_newton=True):
    sc = scan(cell)
    nb, nz, npl = len(sc["brackets"]), len(sc["zeros"]), len(sc["plateaus"])
    if npl > 0:
        root_count = 2
    else:
        root_count = nb + nz
    roots = []
    for (a, b, fa, fb) in sc["brackets"]:
        mid, width, f_mid, trace = bisect_root(a, b, cell)
        roots.append({"lam": mid, "width": width, "residual": f_mid, "lo": a, "hi": b, "trace": trace})
    for z in sc["zeros"]:
        roots.append({"lam": z, "width": 0.0, "residual": evaluate(z, cell)["residual"],
                      "lo": z, "hi": z, "trace": []})
    out = {"scan": sc, "root_count": root_count, "brackets": nb, "zeros": nz,
           "plateaus": npl, "roots": roots, "decreases": sc["decreases"]}
    if want_newton and len(roots) == 1:
        lam_n, ntrace, e_n = newton_root(cell)
        out["newton"] = {"lam": lam_n, "trace": ntrace, "residual": e_n["residual"],
                         "diff": abs(lam_n - roots[0]["lam"])}
    return out


def verdict_of(sol, cell, falsifier_pass, method_ok, monotone_ok, lam_star=None):
    """Precedence: UNDETERMINED > MULTIPLE > LAW-INCOMPATIBLE > SINGLE-LEVER-IDENTIFIED."""
    flags = []
    if not falsifier_pass:
        return "UNDETERMINED", ["FALSIFIER-FIRED"]
    if not monotone_ok:
        return "UNDETERMINED", ["MONOTONICITY-AUDIT-FAILED"]
    if not method_ok:
        return "UNDETERMINED", ["METHOD-DISAGREEMENT"]
    if sol["root_count"] > 1:
        if sol["plateaus"] > 0:
            flags.append("PLATEAU-ROOT")
        return "MULTIPLE", flags
    if sol["root_count"] == 0:
        f_lo = evaluate(LAM_LO, cell)["F"]
        f_hi = evaluate(LAM_HI, cell)["F"]
        if f_hi < cell["target"]:
            flags.append("ROOT-OUTSIDE-RANGE-LOW")
        if f_lo > cell["target"]:
            flags.append("ROOT-OUTSIDE-RANGE-HIGH")
        if max(sol["scan"]["f"]) < 0.0:
            flags.append("LAW-MAX-BELOW-TARGET")
        return "LAW-INCOMPATIBLE", flags
    return "SINGLE-LEVER-IDENTIFIED", flags


# ----------------------------------------------------------------------------- inputs
def load_cell(rows, year_completion: int, target: float):
    entry = year_completion - DVEC_LOWER
    try:
        C_e = rows[(COUNTRY, LEVEL, str(entry))]
        C_c = rows[(COUNTRY, LEVEL, str(year_completion))]
    except KeyError as exc:  # capability lint
        raise SystemExit("CAPABILITY-LINT-FAIL: missing panel row %s" % (exc,))
    required_cols = ("cohort", "seats", "seat_coverage", "congestion_q", "survival",
                     "completion_uis", "admitted_official", "demand_official")
    for col in required_cols:
        if col not in C_e or col not in C_c:
            raise SystemExit("CAPABILITY-LINT-FAIL: missing column %r" % col)
    cell = {
        "year_completion": year_completion, "year_entry": entry, "target": target,
        "cohort_entry": float(C_e["cohort"]), "seats_entry": float(C_e["seats"]),
        "cohort_completion": float(C_c["cohort"]), "seats_completion": float(C_c["seats"]),
        "coverage_entry": float(C_e["seat_coverage"]), "coverage_completion": float(C_c["seat_coverage"]),
        "q_completion": float(C_c["congestion_q"]), "survival_panel": float(C_c["survival"]),
        "completion_uis": float(C_c["completion_uis"]),
        "demand_official_entry": float(C_e["demand_official"]),
        "admitted_official_entry": float(C_e["admitted_official"]),
        "row_entry": C_e, "row_completion": C_c,
    }
    # declared anchors of PRE_DECLARATIONS.md 2.4 must reproduce
    if abs(cell["coverage_entry"] - cell["seats_entry"] / cell["cohort_entry"]) > 1e-9:
        raise SystemExit("CAPABILITY-LINT-FAIL: seat_coverage != seats/cohort at the entry year")
    if abs(cell["coverage_completion"] - cell["seats_completion"] / cell["cohort_completion"]) > 1e-9:
        raise SystemExit("CAPABILITY-LINT-FAIL: seat_coverage != seats/cohort at the completion year")
    return cell


def main(argv=None):
    ap = argparse.ArgumentParser(description="EXP-17 JOINT-COVER")
    ap.add_argument("--outdir", default="results")
    args = ap.parse_args(argv)

    here = os.path.dirname(os.path.abspath(__file__))
    expdir = os.path.dirname(here)
    prog = find_programme_root(expdir)
    outdir = args.outdir if os.path.isabs(args.outdir) else os.path.join(expdir, args.outdir)

    # ---- freeze check: the build fails if the predeclaration moved --------------------------
    predecl = os.path.join(expdir, "PRE_DECLARATIONS.md")
    if not os.path.isfile(predecl):
        raise SystemExit("CAPABILITY-LINT-FAIL: PRE_DECLARATIONS.md missing")
    actual = sha256_file(predecl)
    if actual != PRE_DECL_SHA256:
        raise SystemExit("FREEZE-FAIL: PRE_DECLARATIONS.md sha256 %s != frozen %s" % (actual, PRE_DECL_SHA256))

    panel = os.path.join(prog, "10_massification", "extensions", "synthetic_2026-11-20",
                         "generator_v1_2", "results", "synthetic_panel_v1_2.csv")
    inputs = {
        "PRE_DECLARATIONS.md": predecl,
        "synthetic_panel_v1_2.csv": panel,
        "sim_v1_2.py": os.path.join(prog, "10_massification", "extensions", "synthetic_2026-11-20",
                                    "generator_v1_2", "code", "sim_v1_2.py"),
        "PARAMS.md": os.path.join(prog, "10_massification", "extensions", "synthetic_2026-11-20",
                                  "generator_v1_2", "PARAMS.md"),
        "SYNTHESIS_024.md": os.path.join(prog, "08_council", "brief_024", "SYNTHESIS_024.md"),
        "DECISIONS.md": os.path.join(prog, "08_council", "DECISIONS.md"),
        "LOWER_DEF_RESULTS.csv": os.path.join(prog, "10_massification", "extensions",
                                              "lower_def_2026-11-20", "results", "LOWER_DEF_RESULTS.csv"),
    }
    for name, path in inputs.items():
        if not os.path.isfile(path):
            raise SystemExit("CAPABILITY-LINT-FAIL: input missing: %s" % name)

    rows = {}
    with open(panel, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[(r["country"], r["level"], r["year"])] = r

    cell = load_cell(rows, YEAR_COMPLETION, TARGET)
    if cell["year_entry"] + DVEC_LOWER != cell["year_completion"]:
        raise SystemExit("CAPABILITY-LINT-FAIL: entry + DVEC != completion")

    # ---- falsifier (block clause 5) --------------------------------------------------------
    e1 = evaluate(1.0, cell)
    fals_err = abs(e1["F"] - cell["completion_uis"])
    falsifier_pass = fals_err <= FALSIFIER_TOL
    surv_err = abs(e1["survival"] - cell["survival_panel"])
    surv_diag_pass = surv_err <= FALSIFIER_TOL
    gap_pp = (cell["target"] - e1["F"]) * 100.0
    gap_log = math.log(cell["target"]) - math.log(e1["F"])

    # ---- solve -----------------------------------------------------------------------------
    sol = solve_cell(cell, want_newton=True)
    method_ok = True
    if "newton" in sol:
        method_ok = sol["newton"]["diff"] <= METHOD_TOL
        root = sol["roots"][0]
        lam_star = root["lam"]
        root_resid = root["residual"]
    else:
        root = None
        lam_star = None
        root_resid = None
    monotone_ok = (sol["decreases"] == 0)

    label, flags = verdict_of(sol, cell, falsifier_pass, method_ok, monotone_ok, lam_star)
    if label != "SINGLE-LEVER-IDENTIFIED":
        # a number may be printed only as an artefact, never as the result
        artefact = lam_star
        lam_star_result = None
    else:
        artefact = None
        lam_star_result = lam_star

    # ---- implied quantities at the root ----------------------------------------------------
    lam_use = lam_star_result if label == "SINGLE-LEVER-IDENTIFIED" else None
    if lam_use is not None:
        er = evaluate(lam_use, cell)
        implied = {
            "coverage_entry": lam_use * cell["coverage_entry"],
            "coverage_completion": lam_use * cell["coverage_completion"],
            "seats_entry": lam_use * cell["seats_entry"],
            "seats_completion": lam_use * cell["seats_completion"],
            "a": er["gate"], "s": er["survival"],
            "product": M_FACTOR * er["gate"] * er["survival"],
            "phys_cap_coverage_entry": PHYS_CAP * lam_use * cell["coverage_entry"],
            "lambda_minus_one": lam_use - 1.0,
            "coverage_uplift_pp_entry": (lam_use - 1.0) * cell["coverage_entry"] * 100.0,
            "coverage_uplift_pp_completion": (lam_use - 1.0) * cell["coverage_completion"] * 100.0,
            "q_completion": er["q"],
        }
    else:
        implied = {k: None for k in ("coverage_entry", "coverage_completion", "seats_entry",
                                     "seats_completion", "a", "s", "product",
                                     "phys_cap_coverage_entry", "lambda_minus_one",
                                     "coverage_uplift_pp_entry", "coverage_uplift_pp_completion",
                                     "q_completion")}

    # ---- critical lambda points ------------------------------------------------------------
    lam_cap = (OVERAGE_CAP * cell["cohort_entry"]) / (PHYS_CAP * cell["seats_entry"])
    q21 = cell["cohort_completion"] / cell["seats_completion"]
    lam_demand = cell["demand_official_entry"] / (PHYS_CAP * cell["seats_entry"])
    f_lo = evaluate(LAM_LO, cell)["F"]
    f_hi = evaluate(LAM_HI, cell)["F"]
    law_max_grid = max(sol["scan"]["f"]) + cell["target"]
    law_max_analytic = M_FACTOR * OVERAGE_CAP * SURV_MAX
    clip_inactive = (not evaluate(LAM_LO, cell)["clip_active"]) and \
                    (not evaluate(LAM_HI, cell)["clip_active"]) and \
                    (lam_use is None or not evaluate(lam_use, cell)["clip_active"])
    root_in_capacity_regime = (lam_use is not None) and (lam_use < lam_demand)

    # resolution pretest (D147 rule ii), evaluated at the root (or 1.2 if no root)
    lam_test = lam_use if lam_use is not None else 1.2
    d_gate = PHYS_CAP * cell["seats_entry"] / cell["cohort_entry"] \
        if gate_term(lam_test, cell["seats_entry"], cell["cohort_entry"])[1] == "phys_cap" else 0.0
    q_t = cell["cohort_completion"] / (lam_test * cell["seats_completion"])
    s_t = SURV_MAX * math.exp(-GAMMA * max(0.0, q_t - 1.0))
    d_surv = s_t * GAMMA * q_t / (lam_test * lam_test) if q_t > 1.0 else 0.0
    fd = abs(evaluate(lam_test + 0.01, cell)["F"] - evaluate(lam_test - 0.01, cell)["F"])
    resolution_pass = (d_gate > 0.0) and (d_surv > 0.0) and (fd > 1e-6)

    # ---- secondary: observed reference (non-verdict-bearing) -------------------------------
    ref_cell = dict(cell)
    ref_cell["target"] = TARGET_OBSERVED_REF
    ref_sol = solve_cell(ref_cell, want_newton=False)
    ref_lam = ref_sol["roots"][0]["lam"] if ref_sol["root_count"] == 1 else None

    # ---- context: the same computation at other years (non-verdict-bearing) ---------------
    context = []
    for yr in CONTEXT_YEARS:
        try:
            c = load_cell(rows, yr, TARGET)
        except SystemExit:
            context.append({"year": yr, "label": "MISSING-ROW"})
            continue
        s = solve_cell(c, want_newton=False)
        rec = {"year": yr, "entry": c["year_entry"], "root_count": s["root_count"],
               "decreases": s["decreases"], "F_at_1": evaluate(1.0, c)["F"]}
        if s["root_count"] == 1:
            r = s["roots"][0]
            e = evaluate(r["lam"], c)
            rec.update({"lam": r["lam"], "a": e["gate"], "s": e["survival"],
                        "product": M_FACTOR * e["gate"] * e["survival"]})
            rec["label"] = "SINGLE-LEVER-IDENTIFIED"
        else:
            rec["label"] = "NO-SINGLE-ROOT"
        context.append(rec)

    # ---- write outputs ---------------------------------------------------------------------
    os.makedirs(outdir, exist_ok=True)
    res_path = os.path.join(outdir, "JOINT_COVER_RESULTS.csv")
    det_path = os.path.join(outdir, "JOINT_COVER_DETAIL.csv")
    hashes_path = os.path.join(outdir, "INPUT_HASHES.json")

    R = []

    def row(rec, item, value=None, unit="", label="", note=""):
        R.append({"record_type": rec, "item": item, "value": value, "unit": unit,
                  "label": label, "note": note})

    # meta
    row("meta", "experiment", "EXP-17 JOINT-COVER", "", "DECLARED", "brief 024 section 5.2; D145 #2 rank #2")
    row("meta", "scored_cell", "%s|%s|%d" % (COUNTRY, LEVEL, YEAR_COMPLETION), "", "SYNTHETIC",
        "single verdict-bearing cell; entry year %d (DVEC lower = %d)" % (YEAR_ENTRY, DVEC_LOWER))
    row("meta", "predeclaration_sha256", PRE_DECL_SHA256, "", "DECLARED",
        "PRE_DECLARATIONS.md; embedded in code and verified before the run")
    row("meta", "panel_sha256", sha256_file(panel), "", "SYNTHETIC", "synthetic_panel_v1_2.csv")
    row("meta", "frozen_identity", "m=1.10, phys_cap=1.15, overage_cap=1.05, surv_max=0.91, gamma=0.55, "
        "theta=1.0, DVEC=3", "", "CONVENTION/DECLARED", "no constant re-chosen; no generator run")

    # target provenance
    row("target", "value", TARGET, "fraction", "DERIVED",
        "76.6391/0.949 = 80.7577 -> 80.76 at 2 dp (D133/D140): the lower-2021 value that would hold the model's "
        "own delivered upper-2024 76.6391 under kappa=0.949")
    row("target", "provenance", "INTERNAL-CONSISTENCY", "", "DERIVED",
        "not an external standard, not a policy target, not a forecast, not the Philippines")
    row("target", "observed_reference", TARGET_OBSERVED_REF, "fraction", "OBSERVED",
        "UNIVERSALIZATION_SERIES.csv completion_lower_secondary PHL 2021; reference only, never in the verdict path")

    # inputs
    row("input", "cohort_entry_%d" % YEAR_ENTRY, cell["cohort_entry"], "persons", "SYNTHETIC", "panel cohort")
    row("input", "seats_entry_%d" % YEAR_ENTRY, cell["seats_entry"], "persons", "SYNTHETIC", "panel seats")
    row("input", "coverage_entry_%d" % YEAR_ENTRY, cell["coverage_entry"], "seats/cohort", "SYNTHETIC",
        "panel seat_coverage")
    row("input", "cohort_completion_%d" % YEAR_COMPLETION, cell["cohort_completion"], "persons", "SYNTHETIC",
        "panel cohort")
    row("input", "seats_completion_%d" % YEAR_COMPLETION, cell["seats_completion"], "persons", "SYNTHETIC",
        "panel seats")
    row("input", "coverage_completion_%d" % YEAR_COMPLETION, cell["coverage_completion"], "seats/cohort",
        "SYNTHETIC", "panel seat_coverage")
    row("input", "q_completion_%d" % YEAR_COMPLETION, cell["q_completion"], "cohort/seats", "SYNTHETIC",
        "panel congestion_q")
    row("input", "panel_survival_%d" % YEAR_COMPLETION, cell["survival_panel"], "fraction", "SYNTHETIC",
        "panel survival")
    row("input", "panel_completion_uis_%d" % YEAR_COMPLETION, cell["completion_uis"], "fraction", "SYNTHETIC",
        "panel completion_uis; the falsifier's reference")
    row("input", "demand_official_entry_pct_cohort", cell["demand_official_entry"] / cell["cohort_entry"] * 100.0,
        "percent", "SYNTHETIC", "used by the capacity-regime scope check only")
    row("input", "admitted_official_entry_pct_cohort",
        cell["admitted_official_entry"] / cell["cohort_entry"] * 100.0, "percent", "SYNTHETIC",
        "realised gate at the entry year (context)")

    # falsifier
    row("falsifier", "lambda_1_chain", e1["F"], "fraction", "SYNTHETIC",
        "m * gate(2018) * surv(2021) at lambda=1")
    row("falsifier", "lambda_1_gate", e1["gate"], "fraction", "SYNTHETIC", "binding branch: %s" % e1["branch"])
    row("falsifier", "lambda_1_survival", e1["survival"], "fraction", "SYNTHETIC",
        "law value; panel stores %s" % fmt(cell["survival_panel"], 12))
    row("falsifier", "abs_error", fals_err, "fraction", "DERIVED", "|chain - panel completion_uis|")
    row("falsifier", "tolerance", FALSIFIER_TOL, "fraction", "DECLARED", "block clause 5")
    row("falsifier", "pass", falsifier_pass, "", "DERIVED", "TRUE = accounting is the one executed")
    row("falsifier", "survival_diagnostic_abs_error", surv_err, "fraction", "DERIVED",
        "law survival vs panel survival at lambda=1; diagnostic only")
    row("falsifier", "survival_diagnostic_pass", surv_diag_pass, "", "DERIVED", "reporting-defect note if FALSE")

    # anchor / gap
    row("anchor", "f_value_at_lambda_1", e1["F"], "fraction", "SYNTHETIC", "D142 delivered chain")
    row("anchor", "gap_pp", gap_pp, "percentage points", "DERIVED", "target - F(1); D142's 13.3527 pp")
    row("anchor", "gap_log", gap_log, "log", "DERIVED", "ln(target) - ln(F(1))")

    # roots
    row("root", "count", sol["root_count"], "roots", "DERIVED",
        "sign changes %d, exact grid zeros %d, plateau intervals %d" %
        (sol["brackets"], sol["zeros"], sol["plateaus"]))
    row("root", "lambda_star", lam_star_result, "multiplier", "DERIVED",
        "required state; NOT a parameter and NOT adopted (section 8)")
    row("root", "lambda_star_bisect", lam_star, "multiplier", "DERIVED", "bisection on the sign-change bracket")
    if "newton" in sol:
        row("root", "lambda_star_newton", sol["newton"]["lam"], "multiplier", "DERIVED",
            "Newton on the binding branch, seed %s" % fmt(NEWTON_X0, 12))
        row("root", "method_abs_diff", sol["newton"]["diff"], "multiplier", "DERIVED",
            "tolerance %s" % fmt(METHOD_TOL, 6))
        row("root", "method_agreement_pass", method_ok, "", "DERIVED", "section 4.4")
    if root is not None:
        row("root", "bracket_lo", root["lo"], "multiplier", "DERIVED", "from the grid scan")
        row("root", "bracket_hi", root["hi"], "multiplier", "DERIVED", "from the grid scan")
        row("root", "bracket_width_final", root["width"], "multiplier", "DERIVED", "tolerance %s" % fmt(WIDTH_TOL, 6))
        row("root", "residual_at_root", root_resid, "fraction", "DERIVED", "tolerance %s" % fmt(ROOT_TOL, 6))
        row("root", "bisection_iterations", len(root["trace"]), "count", "DERIVED", "max %d" % BISECT_MAX_ITER)
    row("root", "monotonicity_decreases", sol["decreases"], "grid intervals", "DERIVED",
        "intervals where F falls by > 1e-12; must be 0")
    if artefact is not None:
        row("root", "artefact_not_a_result", artefact, "multiplier", "NOT-A-RESULT",
            "printed only because the verdict is not SINGLE-LEVER-IDENTIFIED")

    # law
    row("law", "max_over_bracket", law_max_grid, "fraction", "DERIVED", "max of F over [%s, %s]" % (LAM_LO, LAM_HI))
    row("law", "analytic_max", law_max_analytic, "fraction", "DERIVED", "m*overage_cap*surv_max = 1.10*1.05*0.91")
    row("law", "F_at_0.5", f_lo, "fraction", "DERIVED", "bracket end")
    row("law", "F_at_2.0", f_hi, "fraction", "DERIVED", "bracket end")
    row("law", "lambda_cap", lam_cap, "multiplier", "DERIVED",
        "gate reaches overage_cap at or above this lambda")
    row("law", "lambda_survival_flat", q21, "multiplier", "DERIVED",
        "survival reaches surv_max at or above this lambda (q(2021))")
    row("law", "lambda_demand_bind", lam_demand, "multiplier", "DERIVED",
        "implied gate reaches the panel's own 2018 demand share here")
    row("law", "clip_inactive", clip_inactive, "", "DERIVED", "survival clip [0.02, 0.995] never binds on bracket")

    # implied state
    row("implied", "coverage_%d" % YEAR_ENTRY, implied["coverage_entry"], "seats/cohort", "DERIVED",
        "lambda* * panel coverage at the entry year")
    row("implied", "coverage_%d" % YEAR_COMPLETION, implied["coverage_completion"], "seats/cohort", "DERIVED",
        "lambda* * panel coverage at the completion year")
    row("implied", "seats_%d" % YEAR_ENTRY, implied["seats_entry"], "persons", "DERIVED", "lambda* * panel seats")
    row("implied", "seats_%d" % YEAR_COMPLETION, implied["seats_completion"], "persons", "DERIVED",
        "lambda* * panel seats")
    row("implied", "a_gate", implied["a"], "fraction", "DERIVED", "implied entry admission (the gate channel)")
    row("implied", "s_survival", implied["s"], "fraction", "DERIVED", "implied completion survival (the law channel)")
    row("implied", "product_m_a_s", implied["product"], "fraction", "DERIVED", "must equal the target")
    row("implied", "phys_cap_times_coverage_%d" % YEAR_ENTRY, implied["phys_cap_coverage_entry"], "fraction",
        "DERIVED", "1.15 * lambda* * coverage at entry; equals a to print rounding on the phys_cap branch")
    row("implied", "q_completion", implied["q_completion"], "cohort/seats", "DERIVED", "congestion at the root")
    row("implied", "lambda_minus_one", implied["lambda_minus_one"], "multiplier", "DERIVED", "uplift size")
    row("implied", "coverage_uplift_pp_%d" % YEAR_ENTRY, implied["coverage_uplift_pp_entry"],
        "percentage points", "DERIVED", "(lambda*-1) * coverage at entry")
    row("implied", "coverage_uplift_pp_%d" % YEAR_COMPLETION, implied["coverage_uplift_pp_completion"],
        "percentage points", "DERIVED", "(lambda*-1) * coverage at completion")
    row("implied", "required_vs_realised_gap_pp", gap_pp, "percentage points", "DERIVED",
        "target - F(1); the gap lambda* closes by one lever")

    # scope checks
    row("check", "root_in_capacity_regime", root_in_capacity_regime, "", "DERIVED",
        "lambda* < lambda_demand; if FALSE the implied a is an equation artefact")
    row("check", "implied_a_flag", "NONE" if root_in_capacity_regime else "EXCEEDS-DEMAND", "", "DERIVED",
        "non-verdict-bearing scope flag (section 6.2 item 2)")
    row("check", "resolution_pretest", resolution_pass, "", "DECLARED",
        "dG/dlam=%s, dS/dlam=%s, |F(+0.01)-F(-0.01)|=%s" % (fmt(d_gate, 6), fmt(d_surv, 6), fmt(fd, 6)))
    row("check", "law_max_matches_analytic", abs(law_max_grid - law_max_analytic) <= 1e-12, "", "DERIVED",
        "grid max %s vs analytic %s" % (fmt(law_max_grid, 12), fmt(law_max_analytic, 12)))
    row("check", "count_blind", True, "", "DECLARED",
        "no observed-path count computed; no 33-cell object read; observed series appears as one reference row only")

    # verdict
    row("verdict", "verdict_label", label, "", "DECLARED-RULE", "; ".join(flags) if flags else "no flags")
    row("verdict", "verdict_precedence", "UNDETERMINED > MULTIPLE > LAW-INCOMPATIBLE > SINGLE-LEVER-IDENTIFIED",
        "", "DECLARED", "section 5.1; the block stated none")
    row("verdict", "adoption", "NONE", "", "DECLARED",
        "no lambda adopted; lambda* is a REQUIRED STATE, usable only with the DERIVED target 0.8076 attached")

    # secondary: observed reference
    row("secondary", "reference_target", TARGET_OBSERVED_REF, "fraction", "OBSERVED",
        "reference only; NOT the requirement; section 6.2 item 5")
    row("secondary", "reference_lambda_star", ref_lam, "multiplier", "DERIVED",
        "same solve against the observed reference; non-verdict-bearing")
    row("secondary", "reference_provenance_delta_pp", PROVENANCE_DELTA_PP, "percentage points", "OBSERVED",
        "D142: observed minus internal requirement")

    # context by year
    for rec in context:
        if rec.get("label") == "MISSING-ROW":
            row("context", "year_%d" % rec["year"], "", "", "SYNTHETIC", "MISSING-ROW; not scored")
            continue
        row("context", "year_%d_lambda_star" % rec["year"], rec.get("lam"), "multiplier", "DERIVED",
            "context only; %s; F(1)=%s" % (rec["label"], fmt(rec["F_at_1"], 8)))
        if rec.get("lam") is not None:
            row("context", "year_%d_a_s" % rec["year"], "%s / %s" % (fmt(rec["a"], 8), fmt(rec["s"], 8)),
                "fraction", "DERIVED", "implied (a, s) at %d" % rec["year"])

    with open(res_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["record_type", "item", "value", "unit", "label", "note"])
        for r in R:
            w.writerow([r["record_type"], r["item"], fmt(r["value"], 15), r["unit"], r["label"], r["note"]])

    # detail
    with open(det_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["record_type", "iter", "lam", "lam_lo", "lam_hi", "gate_term", "gate_branch",
                    "q_completion", "quality_q", "survival_term", "F", "target", "residual", "sign", "note"])
        for x, f in zip(sol["scan"]["x"], sol["scan"]["f"]):
            e = evaluate(x, cell)
            w.writerow(["grid", "", fmt(x, 12), "", "", fmt(e["gate"], 12), e["branch"],
                        fmt(e["q"], 12), fmt(e["quality"], 12), fmt(e["survival"], 12),
                        fmt(e["F"], 12), fmt(cell["target"], 12), fmt(f, 12),
                        "+" if f > 0 else ("-" if f < 0 else "0"), ""])
        for (a, b, fa, fb) in sol["scan"]["brackets"]:
            w.writerow(["bracket", "", "", fmt(a, 15), fmt(b, 15), "", "", "", "", "", "", fmt(cell["target"], 12),
                        "%s / %s" % (fmt(fa, 12), fmt(fb, 12)), "+-", "sign change; bisected"])
        if root is not None:
            for (it, lo, hi, f_lo_, f_hi_, mid, f_mid, width) in root["trace"]:
                w.writerow(["bisect", it, fmt(mid, 15), fmt(lo, 15), fmt(hi, 15),
                            fmt(evaluate(mid, cell)["gate"], 12), evaluate(mid, cell)["branch"],
                            fmt(evaluate(mid, cell)["q"], 12), fmt(evaluate(mid, cell)["quality"], 12),
                            fmt(evaluate(mid, cell)["survival"], 12), fmt(evaluate(mid, cell)["F"], 15),
                            fmt(cell["target"], 12), fmt(f_mid, 15), "+" if f_mid > 0 else ("-" if f_mid < 0 else "0"),
                            "width=%s" % fmt(width, 12)])
        if "newton" in sol:
            for (it, lam_n, step, resid) in sol["newton"]["trace"]:
                w.writerow(["newton", it, fmt(lam_n, 15), "", "", "", "", "", "", "", "", fmt(cell["target"], 12),
                            fmt(resid, 15), "+" if resid > 0 else ("-" if resid < 0 else "0"),
                            "step=%s" % fmt(step, 12)])
        for name, val in (("lambda_lo", LAM_LO), ("lambda_hi", LAM_HI), ("lambda_cap", lam_cap),
                          ("lambda_survival_flat", q21), ("lambda_demand_bind", lam_demand)):
            e = evaluate(val, cell)
            w.writerow(["critical", "", fmt(val, 15), "", "", fmt(e["gate"], 12), e["branch"],
                        fmt(e["q"], 12), fmt(e["quality"], 12), fmt(e["survival"], 12), fmt(e["F"], 12),
                        fmt(cell["target"], 12), fmt(e["residual"], 12),
                        "+" if e["residual"] > 0 else ("-" if e["residual"] < 0 else "0"), name])
        e = evaluate(1.0, cell)
        w.writerow(["anchor", "", fmt(1.0, 15), "", "", fmt(e["gate"], 15), e["branch"], fmt(e["q"], 12),
                    fmt(e["quality"], 12), fmt(e["survival"], 15), fmt(e["F"], 15), fmt(cell["target"], 12),
                    fmt(e["residual"], 15), "+" if e["residual"] > 0 else "-",
                    "lambda=1 falsifier anchor; panel completion_uis=%s" % fmt(cell["completion_uis"], 12)])
        w.writerow(["note", "", "", "", "", "", "", "", "", "", "", "", "", "",
                    "grid = 2021 scored cell only (N=%d, step=%s); by-year context roots are in RESULTS" %
                    (GRID_N, fmt(GRID_STEP, 6))])

    with open(hashes_path, "w", encoding="utf-8", newline="\n") as fh:
        payload = {
            "experiment": "EXP-17 JOINT-COVER",
            "role": "read-only inputs; no input file was modified; no generator was run",
            "predeclaration_sha256_embedded": PRE_DECL_SHA256,
            "inputs": {name: {"path": os.path.relpath(path, prog), "sha256": sha256_file(path),
                              "bytes": os.path.getsize(path)} for name, path in sorted(inputs.items())},
        }
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")

    # console summary (not part of the compared artifacts)
    print("EXP-17 JOINT-COVER")
    print("  falsifier  : chain(1)=%s panel=%s |err|=%.3e tol=%.0e -> %s"
          % (fmt(e1["F"], 15), fmt(cell["completion_uis"], 15), fals_err, FALSIFIER_TOL,
             "PASS" if falsifier_pass else "FAIL"))
    print("  roots      : count=%d (sign changes %d, zeros %d, plateaus %d)"
          % (sol["root_count"], sol["brackets"], sol["zeros"], sol["plateaus"]))
    print("  lambda*    : %s  (bisect %s / newton %s, diff %s)"
          % (fmt(lam_star_result, 15), fmt(lam_star, 15),
             fmt(sol.get("newton", {}).get("lam"), 15), fmt(sol.get("newton", {}).get("diff"), 6)))
    print("  implied    : coverage %s (%d) / %s (%d); a=%s s=%s; product=%s (blank = no lambda reported)"
          % (fmt(implied["coverage_entry"], 12), YEAR_ENTRY, fmt(implied["coverage_completion"], 12),
             YEAR_COMPLETION, fmt(implied["a"], 12), fmt(implied["s"], 12), fmt(implied["product"], 12)))
    print("  law max    : %s (analytic %s)   F(0.5)=%s F(2.0)=%s"
          % (fmt(law_max_grid, 12), fmt(law_max_analytic, 12), fmt(f_lo, 12), fmt(f_hi, 12)))
    print("  checks     : clip_inactive=%s capacity_regime=%s resolution=%s monotone=%s"
          % (clip_inactive, root_in_capacity_regime, resolution_pass, monotone_ok))
    print("  VERDICT    : %s %s" % (label, ("[" + "; ".join(flags) + "]") if flags else ""))
    print("  outputs    : %s" % os.path.relpath(outdir, prog))
    return 0


if __name__ == "__main__":
    sys.exit(main())
