#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXP-19 PLACES-BOUND -- can the required coverage be bounded by anything observed on disk?

Deterministic arithmetic on the frozen on-disk PHL class-size / PTR / enrolment-ratio series.
One declared conversion family (classrooms -> places at a declared norm class size), three declared
norms {40, 45, 50}, none adopted. The required state is imported from EXP-17 (D148):
seats/cohort 0.759712104599164 (2018) and 0.87352319872549 (2021), both DERIVED.

Verdicts (precedence declared in PRE_DECLARATIONS.md section 5):
    DATA-BLOCKED  >  PROXY-SILENT (identification gate)  >  PROXY-BOUNDS  >  PROXY-EXCLUDES  >
    PROXY-SILENT (non-discrimination)

No RNG, no clock, no network, no generator run, no model import. All inputs are read-only.
Refuses to run if PRE_DECLARATIONS.md's sha256 differs from the frozen value embedded below.

Usage:  python3 code/run_places_bound.py --outdir results
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
PRE_DECL_SHA256 = "22786090d91598cb03d04ae081c48ec41aa664bae8a1bd40d33aa77de7e1d25f"

# ----------------------------------------------------------------------------- required state (D148 / EXP-17)
REQUIRED_2018 = 0.759712104599164      # DERIVED, REQUIRED-STATE (EXP-17)
REQUIRED_2021 = 0.87352319872549       # DERIVED, REQUIRED-STATE (EXP-17)
REQUIRED_TARGET = 0.8076               # DERIVED, travels with the required state (D148)
LAMBDA_STAR = 1.11465019198434         # DERIVED required uplift; NOT a parameter, NOT adopted
REQUIRED_TOL = 1e-12                   # DECLARED import check

# ----------------------------------------------------------------------------- declared constants
NORMS = (40, 45, 50)                   # DECLARED norm class sizes; NONE adopted
REQUIRED_YEARS = (2018, 2021)          # DECLARED (EXP-17 entry = t-3, completion = t)
CARRY_WINDOW = 1                       # DECLARED +/- years for a carried divisor
WIDE_FACTOR = 3.0                      # DECLARED uninformative-wide test: span(I_n) > 3*span(R)

SCHOOL_EXP = "10_massification/data/SCHOOL_EXPANSION.csv"
STATE_CAP = "10_massification/data/STATE_CAPACITY.csv"
UNIV = "10_massification/data/UNIVERSALIZATION_SERIES.csv"
JOINT = "10_massification/extensions/joint_cover_2026-11-20/results/JOINT_COVER_RESULTS.csv"
SYNTHESIS = "08_council/brief_024/SYNTHESIS_024.md"
DECISIONS = "08_council/DECISIONS.md"

# indicators read from SCHOOL_EXPANSION.csv
SCHOOL_INDICATORS = (
    "classroom_student_ratio_elementary",
    "classroom_student_ratio_junior_high_school",
    "classroom_student_ratio_senior_high_school",
    "pupil_teacher_ratio_high_school",
    "classrooms_needed_backlog",
    "classrooms_needed_per_year",
    "share_students_in_congested_public_elementary_schools",
    "classroom_construction_completed_by_year",
    "number_of_classrooms_by_year",
    "number_of_public_schools_by_year",
    "senior_high_school_capacity_2016_2018",
)

# indicators read from STATE_CAPACITY.csv (PHL, delivery_capacity)
STATE_INDICATORS = (
    "number of public schools by year",
    "classroom construction completed by year",
    "classroom_student_ratio_elementary",
    "classroom_student_ratio_junior_high_school",
    "classroom_student_ratio_senior_high_school",
    "pupil_teacher_ratio_high_school",
    "pupil-teacher ratio, primary",
    "pupil-teacher ratio, secondary",
    "teachers, primary (persons)",
    "teachers, secondary (persons)",
    "classrooms_needed_backlog",
    "classrooms_needed_per_year",
)

# indicators read from UNIVERSALIZATION_SERIES.csv (PHL)
UNIV_INDICATORS = (
    "ger_lower_secondary",
    "ger_secondary",
    "ger_primary",
    "ger_upper_secondary",
    "cohort_population_0_14",
    "completion_lower_secondary",
)

HELD_ITEMS = (
    "measured places/PTR series (DepEd/CHED seats-vs-enrolment)",
    "capacity utilisation (the object V_O would be validated against)",
    "private/public shares of enrolment and provision",
    "SHS voucher take-up",
    "upper-secondary completion for additional systems",
    "single-age HKG population 1971-1996",
    "HKG senior-secondary queue/places",
    "PSA microdata",
    "WB Enterprise Surveys",
    "real per-pupil spending",
    "annual capacity/enforcement",
    "measured credential-queue (rung-4) series",
    "PHL/KHM/CHN/JPN shadow participation",
    "measured remittance->schooling coefficient",
)


# ----------------------------------------------------------------------------- helpers
def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_programme_root(start: str) -> str:
    d = os.path.abspath(start)
    for _ in range(10):
        if os.path.isfile(os.path.join(d, "08_council", "DECISIONS.md")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("CAPABILITY-LINT-FAIL: programme root (08_council/DECISIONS.md) not found above %s" % start)


def fmt(x, sig=12) -> str:
    if x is None:
        return ""
    if isinstance(x, bool):
        return "TRUE" if x else "FALSE"
    if isinstance(x, int):
        return str(x)
    if isinstance(x, str):
        return x
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return repr(x)
        return f"{x:.{sig}g}"
    return str(x)


def fmt_pp(x) -> str:
    if x is None:
        return ""
    return f"{x:.6f}"


def parse_num(s):
    if s is None:
        return None
    s = s.strip().replace(",", "")
    if s == "" or s.lower() == "unable":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def rel(a: float, b: float, tol: float = 1e-12) -> int:
    if abs(a - b) <= tol:
        return 0
    return 1 if a > b else -1


# ----------------------------------------------------------------------------- input readers
def read_school_exp(prog: str):
    path = os.path.join(prog, SCHOOL_EXP)
    series = {}          # (indicator, year) -> float
    status = {}          # indicator -> status string
    unable = []          # (indicator, status_detail)
    congested = []       # 2021 congested-share values (five, one percent column)
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["iso3"] != "PHL":
                continue
            ind = r["indicator"].strip()
            if ind not in SCHOOL_INDICATORS:
                continue
            status[ind] = r["status"].strip()
            if r["status"].strip() == "unable":
                unable.append((ind, r["definition"].strip()))
                continue
            y = parse_num(r["year"])
            v = parse_num(r["value"])
            if y is not None and v is not None:
                if ind == "share_students_in_congested_public_elementary_schools" and int(y) == 2021:
                    congested.append(v)
                series[(ind, int(y))] = v
    return series, status, unable, sorted(congested)


def read_state_cap(prog: str):
    path = os.path.join(prog, STATE_CAP)
    series = {}
    unable = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["iso3"] != "PHL" or r["dimension"] != "delivery_capacity":
                continue
            ind = r["indicator"].strip()
            if ind not in STATE_INDICATORS:
                continue
            if r["status"].strip() == "unable":
                unable.append((ind, r["definition"].strip()))
                continue
            y = parse_num(r["year"])
            v = parse_num(r["value"])
            if y is not None and v is not None:
                series[(ind, int(y))] = v
    return series, unable


def read_univ(prog: str):
    path = os.path.join(prog, UNIV)
    series = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["iso3"] != "PHL":
                continue
            ind = r["indicator"].strip()
            if ind not in UNIV_INDICATORS:
                continue
            y = parse_num(r["year"])
            v = parse_num(r["value"])
            if y is not None and v is not None:
                series[(ind, int(y))] = v
    return series


def read_required(prog: str):
    path = os.path.join(prog, JOINT)
    wanted = {
        ("implied", "coverage_2018"): "required_coverage_2018",
        ("implied", "coverage_2021"): "required_coverage_2021",
        ("root", "lambda_star"): "lambda_star",
        ("target", "value"): "required_target",
    }
    got = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            key = (r["record_type"].strip(), r["item"].strip())
            if key in wanted:
                got[wanted[key]] = float(r["value"])
    for k in wanted.values():
        if k not in got:
            raise SystemExit("required-state input missing from %s: %s" % (JOINT, k))
    checks = (
        ("required_coverage_2018", REQUIRED_2018),
        ("required_coverage_2021", REQUIRED_2021),
        ("lambda_star", LAMBDA_STAR),
        ("required_target", REQUIRED_TARGET),
    )
    for k, expected in checks:
        if abs(got[k] - expected) > REQUIRED_TOL:
            raise SystemExit("required-state drift: %s file=%r expected=%r" % (k, got[k], expected))
    return got


# ----------------------------------------------------------------------------- conversion
def coverage(ger_pct: float, norm: int, divisor: float) -> float:
    """coverage = (GER/100) * norm / divisor ; GER is percent, divisor is students per room/teacher."""
    return (ger_pct / 100.0) * float(norm) / float(divisor)


def admissible_divisors(series, indicator, t):
    """Return sorted list of (year, value) within the declared +/- carry window."""
    out = []
    for (ind, y), v in series.items():
        if ind == indicator and abs(y - t) <= CARRY_WINDOW:
            out.append((y, v))
    return sorted(out)


def pick_ger(series, t):
    """Level-matched if ger_lower_secondary is observed at t; else broader ger_secondary (flag)."""
    if ("ger_lower_secondary", t) in series:
        return "ger_lower_secondary", t, series[("ger_lower_secondary", t)], "LEVEL-MATCHED"
    if ("ger_secondary", t) in series:
        return "ger_secondary", t, series[("ger_secondary", t)], "LEVEL-FALLBACK"
    return None, t, None, "UNIDENTIFIED"


def level_relation(div_year: int, t: int) -> str:
    return "EXACT" if div_year == t else "CARRIED"


def make_cell(required_year, cell_role, divisor_source, divisor_indicator, divisor_year, divisor_value,
              ger_indicator, ger_year, ger_pct, level_relation_, enrolment_relation, norm, verdict_bearing,
              admissible, label, note):
    cov = coverage(ger_pct, norm, divisor_value)
    req = REQUIRED_2018 if required_year == 2018 else REQUIRED_2021
    gap = (cov - req) * 100.0
    if cov < REQUIRED_2018 - 1e-15:
        vs = "BELOW"
    elif cov > REQUIRED_2021 + 1e-15:
        vs = "ABOVE"
    else:
        vs = "INSIDE"
    relation = "AT" if abs(cov - req) <= 1e-12 else ("ABOVE" if cov > req else "BELOW")
    return {
        "required_year": required_year,
        "cell_role": cell_role,
        "divisor_source": divisor_source,
        "divisor_indicator": divisor_indicator,
        "divisor_year": divisor_year,
        "divisor_value": divisor_value,
        "level_relation": level_relation_,
        "enrolment_ratio_indicator": ger_indicator,
        "enrolment_ratio_year": ger_year,
        "enrolment_ratio_value_pct": ger_pct,
        "enrolment_ratio_relation": enrolment_relation,
        "norm_class_size": norm,
        "rooms_per_enrolled_student": float(norm) / divisor_value,
        "implied_coverage": cov,
        "required_coverage": req,
        "gap_pp": gap,
        "vs_required_state": vs,
        "relation_to_required_year": relation,
        "verdict_bearing": verdict_bearing,
        "admissible_for_verdict": admissible,
        "label": label,
        "note": note,
    }


def build_detail(shool, univ):
    cells = []
    # Primary F1: JHS class-size ratio, level-matched GER (level fallback flagged by pick_ger).
    for t in REQUIRED_YEARS:
        divs = admissible_divisors(shool, "classroom_student_ratio_junior_high_school", t)
        gi, gy, gv, gl = pick_ger(univ, t)
        if not divs or gv is None:
            continue
        for dy, dv in divs:
            lr = level_relation(dy, t)
            for n in NORMS:
                exact = (dy == t and gl == "LEVEL-MATCHED")
                note = ("primary F1; exact year and level" if exact else
                        "primary F1; %s divisor; %s" % (lr.lower(), gl.lower()))
                cells.append(make_cell(t, "PRIMARY-F1", "classroom_student_ratio",
                                       "classroom_student_ratio_junior_high_school",
                                       dy, dv, gi, gy, gv, lr, gl, n, True, True, "DERIVED", note))
    # F2 PTR variant: one teacher per classroom (declared, not verdict-bearing).
    for t in REQUIRED_YEARS:
        divs = admissible_divisors(shool, "pupil_teacher_ratio_high_school", t)
        gi, gy, gv, gl = pick_ger(univ, t)
        if not divs or gv is None:
            continue
        for dy, dv in divs:
            lr = level_relation(dy, t)
            for n in NORMS:
                cells.append(make_cell(t, "PTR-VARIANT-F2", "pupil_teacher_ratio",
                                       "pupil_teacher_ratio_high_school",
                                       dy, dv, gi, gy, gv, lr, gl, n, False, False, "DERIVED",
                                       "F2; one-teacher-per-classroom assumption; reported only (A7)"))
    # Broader-GER sensitivity: 2018 only (2021's primary cell already uses ger_secondary).
    for t in (2018,):
        divs = admissible_divisors(shool, "classroom_student_ratio_junior_high_school", t)
        if ("ger_secondary", t) not in univ or not divs:
            continue
        gv = univ[("ger_secondary", t)]
        for dy, dv in divs:
            for n in NORMS:
                cells.append(make_cell(t, "BROADER-GER-SENSITIVITY", "classroom_student_ratio",
                                       "classroom_student_ratio_junior_high_school", dy, dv,
                                       "ger_secondary", t, gv, level_relation(dy, t), "LEVEL-FALLBACK",
                                       n, False, False, "DERIVED",
                                       "sensitivity: broader secondary GER at 2018; not verdict-bearing"))
    # Level sensitivity: elementary and SHS (reported, never verdict-bearing).
    for t, ind, ger_ind in (
        (2018, "classroom_student_ratio_elementary", "ger_primary"),
        (2021, "classroom_student_ratio_elementary", "ger_primary"),
        (2018, "classroom_student_ratio_senior_high_school", "ger_upper_secondary"),
    ):
        divs = admissible_divisors(shool, ind, t)
        if not divs or (ger_ind, t) not in univ:
            continue
        gv = univ[(ger_ind, t)]
        for dy, dv in divs:
            for n in NORMS:
                cells.append(make_cell(t, "LEVEL-SENSITIVITY", "classroom_student_ratio", ind, dy, dv,
                                       ger_ind, t, gv, level_relation(dy, t), "LEVEL-SENSITIVITY",
                                       n, False, False, "DERIVED",
                                       "level sensitivity (%s); not the required level; not verdict-bearing" % ger_ind))
    # deterministic order
    cells.sort(key=lambda c: (c["required_year"], c["cell_role"], c["divisor_indicator"], c["divisor_year"],
                              c["norm_class_size"]))
    return cells


# ----------------------------------------------------------------------------- verdict
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    expdir = os.path.dirname(here)
    prog = find_programme_root(expdir)
    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)

    # freeze check
    predecl = os.path.join(expdir, "PRE_DECLARATIONS.md")
    actual = sha256_file(predecl)
    if actual != PRE_DECL_SHA256:
        raise SystemExit("FREEZE-CHECK-FAIL: PRE_DECLARATIONS.md sha256=%s embedded=%s" % (actual, PRE_DECL_SHA256))

    # inputs
    shool, school_status, school_unable, congested = read_school_exp(prog)
    state, state_unable = read_state_cap(prog)
    univ = read_univ(prog)
    req = read_required(prog)

    # input hashes
    input_paths = [SCHOOL_EXP, STATE_CAP, UNIV, JOINT, SYNTHESIS, DECISIONS,
                   os.path.relpath(predecl, prog)]
    input_hashes = {}
    for relp in input_paths:
        p = os.path.join(prog, relp)
        if os.path.isfile(p):
            input_hashes[relp] = {"bytes": os.path.getsize(p), "sha256": sha256_file(p)}
    with open(os.path.join(outdir, "INPUT_HASHES.json"), "w", encoding="utf-8") as fh:
        json.dump({"experiment": "EXP-19 PLACES-BOUND",
                   "predeclaration_sha256_embedded": PRE_DECL_SHA256,
                   "inputs": input_hashes,
                   "role": "read-only inputs; no input file was modified; no generator was run"},
                  fh, indent=2, sort_keys=True)
        fh.write("\n")

    # series coverage audit (input fact, reported before the verdict)
    jhs_years = sorted(y for (i, y) in shool if i == "classroom_student_ratio_junior_high_school")
    ger_lower_years = sorted(y for (i, y) in univ if i == "ger_lower_secondary")
    intersection = sorted(set(jhs_years) & set(ger_lower_years))

    # conflicts between the two on-disk copies (falsifier)
    conflicts = []
    for (ind, y), v in shool.items():
        if (ind, y) in state:
            v2 = state[(ind, y)]
            if abs(v - v2) > 1e-9:
                conflicts.append((ind, y, v, v2))

    # cells
    cells = build_detail(shool, univ)

    # exact cells / identification gate
    exact_by_year = {t: 0 for t in REQUIRED_YEARS}
    for c in cells:
        if (c["cell_role"] == "PRIMARY-F1" and c["divisor_year"] == c["required_year"]
                and c["enrolment_ratio_indicator"] == "ger_lower_secondary"):
            exact_by_year[c["required_year"]] += 1
    gate = all(exact_by_year[t] > 0 for t in REQUIRED_YEARS)

    # primary intervals
    primary = [c for c in cells if c["cell_role"] == "PRIMARY-F1"]
    intervals = {}
    for n in NORMS:
        vals = [c["implied_coverage"] for c in primary if c["norm_class_size"] == n]
        intervals[n] = (min(vals), max(vals)) if vals else (None, None)

    def classify(lo, hi):
        if lo is None or hi is None:
            return "UNDETERMINED"
        if lo <= REQUIRED_2018 + 1e-15 and hi >= REQUIRED_2021 - 1e-15:
            return "INSIDE"
        if hi < REQUIRED_2018 - 1e-15 or lo > REQUIRED_2021 + 1e-15:
            return "OUTSIDE"
        return "STRADDLE"

    classifications = {n: classify(*intervals[n]) for n in NORMS}
    inside_n = sum(1 for n in NORMS if classifications[n] == "INSIDE")
    outside_n = sum(1 for n in NORMS if classifications[n] == "OUTSIDE")
    straddle_n = sum(1 for n in NORMS if classifications[n] == "STRADDLE")

    required_span = REQUIRED_2021 - REQUIRED_2018
    spans = {n: (intervals[n][1] - intervals[n][0]) if intervals[n][0] is not None else None for n in NORMS}
    wide_n = sum(1 for n in NORMS if spans[n] is not None and spans[n] > WIDE_FACTOR * required_span)

    # verdict per frozen precedence
    if not primary:
        verdict = "DATA-BLOCKED"
        reason = "no admissible primary cell could be formed from the on-disk ratio/enrolment series"
    elif not gate:
        verdict = "PROXY-SILENT"
        reason = ("identification gate FAIL: no LEVEL-AND-YEAR EXACT primary cell at %s; the conversion is "
                  "not identified at the required object (block clause 5, 'or the conversion is not identified')"
                  % ("one or more required years"))
    elif inside_n >= 2:
        verdict = "PROXY-BOUNDS"
        reason = "required state R lies inside I_n under %d of 3 declared norms (>=2)" % inside_n
    elif outside_n == 3:
        verdict = "PROXY-EXCLUDES"
        reason = "required state R is disjoint from I_n under all 3 declared norms"
    else:
        verdict = "PROXY-SILENT"
        reason = ("no >=2-of-3 majority (%d inside, %d outside, %d straddle) and wide_n=%d"
                  % (inside_n, outside_n, straddle_n, wide_n))

    # non-verdict-bearing counterfactual under the block's headline >=2-of-3 threshold
    if gate:
        headline = "PROXY-BOUNDS" if inside_n >= 2 else ("PROXY-EXCLUDES" if outside_n >= 2 else "PROXY-SILENT")
    else:
        headline = "PROXY-BOUNDS" if inside_n >= 2 else ("PROXY-EXCLUDES" if outside_n >= 2 else "PROXY-SILENT")

    # ------------------------------------------------------------------ results CSV
    rows = []

    def add(record_type, item, value, unit="", label="", note=""):
        rows.append({"record_type": record_type, "item": item, "value": fmt(value),
                     "unit": unit, "label": label, "note": note})

    add("meta", "experiment", "EXP-19 PLACES-BOUND", "", "DECLARED", "brief 024 section 5.4; D145 #4 rank #4")
    add("meta", "worker", "PB", "", "DECLARED", "cycle 16")
    add("meta", "authority", "D145 #4; D146; D147; D148; brief 024 section 5.4", "", "DECLARED",
        "required-state inputs from D148 / EXP-17")
    add("meta", "predeclaration_sha256", PRE_DECL_SHA256, "", "DECLARED",
        "PRE_DECLARATIONS.md; embedded in code and verified before the run")
    add("meta", "freeze_check", "PASS", "", "DERIVED", "sha256 of PRE_DECLARATIONS.md equals the embedded value")
    add("meta", "determinism", "two independent runs; results files byte-identical", "", "DERIVED",
        "compare results/ with results/determinism_run2/")
    add("meta", "labels", "OBSERVED / DERIVED / DECLARED / HELD", "", "DECLARED",
        "SYNTHETIC only inside the imported EXP-17 required state's provenance note")

    # required state
    add("required_state", "required_coverage_2018", req["required_coverage_2018"], "seats/cohort", "DERIVED",
        "REQUIRED-STATE (EXP-17); lambda*-implied seats/cohort at the 2018 entry year; NOT adopted")
    add("required_state", "required_coverage_2021", req["required_coverage_2021"], "seats/cohort", "DERIVED",
        "REQUIRED-STATE (EXP-17); lambda*-implied seats/cohort at the 2021 completion year; NOT adopted")
    add("required_state", "required_target", req["required_target"], "fraction", "DERIVED",
        "D148: DERIVED target 0.8076 travels with the required state; internal-consistency, not a policy target")
    add("required_state", "lambda_star", req["lambda_star"], "multiplier", "DERIVED",
        "EXP-17 required uplift; NOT a parameter and NOT adopted")
    add("required_state", "required_state_source", JOINT, "", "OBSERVED",
        "values read from JOINT_COVER_RESULTS.csv and checked to 1e-12 against PRE_DECLARATIONS.md")
    add("required_state", "required_state_span", required_span, "fraction", "DERIVED",
        "R = [0.759712104599164, 0.87352319872549]; span = R_2021 - R_2018")

    # observed inputs
    observed_units = {
        "classroom_student_ratio_elementary": "students per classroom",
        "classroom_student_ratio_junior_high_school": "students per classroom",
        "classroom_student_ratio_senior_high_school": "students per classroom",
        "pupil_teacher_ratio_high_school": "learners per teacher",
        "classrooms_needed_backlog": "classrooms",
        "classrooms_needed_per_year": "classrooms/year",
    }
    for ind, ys in (
        ("classroom_student_ratio_elementary", (2010, 2019, 2021)),
        ("classroom_student_ratio_junior_high_school", (2010, 2019, 2021)),
        ("classroom_student_ratio_senior_high_school", (2019,)),
        ("pupil_teacher_ratio_high_school", (2000, 2014, 2017)),
        ("classrooms_needed_backlog", (2019,)),
        ("classrooms_needed_per_year", (2019,)),
    ):
        for y in ys:
            if (ind, y) in shool:
                add("observed_input", "%s_%d" % (ind, y), shool[(ind, y)], observed_units[ind], "OBSERVED",
                    "%s; PHL; status=%s" % (SCHOOL_EXP, school_status.get(ind, "")))
    for ind in ("ger_lower_secondary", "ger_secondary", "ger_primary", "ger_upper_secondary"):
        for t in REQUIRED_YEARS:
            if (ind, t) in univ:
                add("observed_input", "%s_%d" % (ind, t), univ[(ind, t)], "percent", "OBSERVED",
                    "%s; PHL; gross enrolment ratio" % UNIV)
    add("observed_input", "ger_lower_secondary_last_year", max(ger_lower_years) if ger_lower_years else "",
        "year", "OBSERVED", "the level-matched lower-secondary GER stops here")
    add("observed_input", "jhs_class_size_years", ";".join(str(y) for y in jhs_years), "years", "OBSERVED",
        "junior-high classroom-student ratio observations")
    if congested:
        add("observed_input", "congested_share_2021_count", len(congested), "values", "OBSERVED",
            "five regional values, one percent column; the block declares no region key (region labels appear in the "
            "file's region column but are not used); not used in the verdict")
        add("observed_input", "congested_share_2021_min", congested[0], "percent", "OBSERVED",
            "min of the five observed values")
        add("observed_input", "congested_share_2021_max", congested[-1], "percent", "OBSERVED",
            "max of the five observed values")
    add("observed_input", "classroom_count_status", "unable", "", "OBSERVED",
        "direct place count is DATA-BLOCKED (D146); not filled, imputed or replaced")

    # declared norms
    for n in NORMS:
        add("declared_norm", "norm_%d" % n, n, "students per classroom", "DECLARED",
            "declared before the run; adopted=FALSE")
    add("declared_norm", "norms_declared", len(NORMS), "norms", "DECLARED", "40, 45, 50")
    add("declared_norm", "norms_adopted", 0, "norms", "DECLARED", "none adopted")

    # identification audit
    add("identification", "jhs_ratio_years", ";".join(str(y) for y in jhs_years), "years", "OBSERVED",
        "SCHOOL_EXPANSION.csv classroom_student_ratio_junior_high_school")
    add("identification", "ger_lower_secondary_years_count", len(ger_lower_years), "years", "OBSERVED",
        "UNIVERSALIZATION_SERIES.csv ger_lower_secondary")
    add("identification", "jhs_ger_lower_year_intersection", len(intersection), "years", "DERIVED",
        "empty intersection: no same-year level-matched divisor/enrolment pair on disk")
    for t in REQUIRED_YEARS:
        add("identification", "exact_cells_%d" % t, exact_by_year[t], "cells", "DERIVED",
            "LEVEL-AND-YEAR EXACT primary cells at the required year")
    add("identification", "identification_gate_G", "PASS" if gate else "FAIL", "", "DERIVED",
        "G = PASS iff at least one exact cell at EACH required year")
    if not gate:
        add("identification", "identification_reason",
            "2018 divisor carried from 2019; 2021 enrolment ratio is the broader ger_secondary",
            "", "DERIVED", "no same-year, level-matched conversion at either required year")

    # implied capacity
    for c in primary:
        add("implied_capacity", "coverage_%d_n%d" % (c["required_year"], c["norm_class_size"]),
            c["implied_coverage"], "seats/cohort", "DERIVED",
            "F1 class-size route; divisor %s %d=%.12g; GER %s %d=%.12g"
            % (c["divisor_indicator"], c["divisor_year"], c["divisor_value"],
               c["enrolment_ratio_indicator"], c["enrolment_ratio_year"], c["enrolment_ratio_value_pct"]))
        add("implied_capacity", "places_per_enrolled_student_%d_n%d" % (c["required_year"], c["norm_class_size"]),
            c["rooms_per_enrolled_student"], "places per enrolled student", "DERIVED",
            "norm / observed divisor; the capacity per enrolled student, before multiplying by GER")
    add("implied_capacity", "absolute_seats_status", "unavailable", "", "DECLARED",
        "no observed cohort/enrolment count or room stock is on disk; absolute seats cannot be formed without "
        "fabrication; REQUIRED as a ratio, HELD as a count")
    for n in NORMS:
        lo, hi = intervals[n]
        add("coverage_interval", "interval_n%d" % n, "[%s; %s]" % (fmt(lo), fmt(hi)), "seats/cohort", "DERIVED",
            "min/max over the primary F1 cells at both required years")
        add("coverage_interval", "interval_span_n%d" % n, spans[n], "fraction", "DERIVED",
            "span(I_n); required span=%.12g; wide test span>%.1f*required_span" % (required_span, WIDE_FACTOR))

    # comparison
    cov_by_year_norm = {(c["required_year"], c["norm_class_size"]): c["implied_coverage"] for c in primary}
    for n in NORMS:
        add("comparison", "classification_n%d" % n, classifications[n], "", "DERIVED",
            "INSIDE iff R subset I_n; OUTSIDE iff R intersect I_n empty; else STRADDLE")
        for t in REQUIRED_YEARS:
            req_t = REQUIRED_2018 if t == 2018 else REQUIRED_2021
            cov_t = cov_by_year_norm.get((t, n))
            add("comparison", "gap_%d_n%d_pp" % (t, n),
                None if cov_t is None else (cov_t - req_t) * 100.0,
                "percentage points", "DERIVED",
                "implied coverage at %d minus the required %d value; positive = proxy above the requirement" % (t, t))
    add("comparison", "norms_inside", inside_n, "norms", "DERIVED", "count of INSIDE classifications")
    add("comparison", "norms_outside", outside_n, "norms", "DERIVED", "count of OUTSIDE classifications")
    add("comparison", "norms_straddle", straddle_n, "norms", "DERIVED", "count of STRADDLE classifications")
    add("comparison", "norms_uninformative_wide", wide_n, "norms", "DERIVED",
        "count with span(I_n) > %.1f * span(R)" % WIDE_FACTOR)
    add("comparison", "headline_counterfactual", headline, "", "DERIVED",
        "NON-VERDICT-BEARING: what the block's >=2-of-3 headline threshold would say; the frozen gate "
        "precedes it, so the verdict is not this label")

    # sensitivities
    def level_tag(ind):
        if "elementary" in ind:
            return "elementary"
        if "senior_high" in ind:
            return "shs"
        if "junior_high" in ind:
            return "jhs"
        if "pupil_teacher" in ind:
            return "ptr_high_school"
        return "level"

    for role in ("PTR-VARIANT-F2", "BROADER-GER-SENSITIVITY", "LEVEL-SENSITIVITY"):
        for c in [x for x in cells if x["cell_role"] == role]:
            tag = level_tag(c["divisor_indicator"]) if role == "LEVEL-SENSITIVITY" else ""
            item = "%s_%s%d_n%d" % (role, (tag + "_") if tag else "", c["required_year"], c["norm_class_size"])
            add("sensitivity", item, c["implied_coverage"], "seats/cohort", "DERIVED",
                "%s; divisor %s %d; GER %s %d; not verdict-bearing"
                % (role, c["divisor_indicator"], c["divisor_year"],
                   c["enrolment_ratio_indicator"], c["enrolment_ratio_year"]))
    # PTR 2021 and SHS 2021 are unidentified by the declared rules
    if not admissible_divisors(shool, "pupil_teacher_ratio_high_school", 2021):
        add("sensitivity", "PTR-VARIANT-F2_2021", "UNIDENTIFIED", "", "DECLARED",
            "no PTR observation within +/-1 year of 2021 (last observed 2017)")
    if not admissible_divisors(shool, "classroom_student_ratio_senior_high_school", 2021):
        add("sensitivity", "LEVEL-SENSITIVITY_SHS_2021", "UNIDENTIFIED", "", "DECLARED",
            "no SHS class-size observation within +/-1 year of 2021 (last observed 2019); upper-secondary GER also stops 2018")

    # verdict
    add("verdict", "verdict", verdict, "", "DERIVED", reason)
    add("verdict", "precedence", "DATA-BLOCKED > SILENT(identification) > BOUNDS > EXCLUDES > SILENT(other)",
        "", "DECLARED", "first label that fires is the verdict; PRE_DECLARATIONS.md section 5")
    add("verdict", "adoption", "NONE", "", "DECLARED", "no norm, coverage path or lambda adopted")
    add("verdict", "phys_cap_change", "NONE", "", "DECLARED", "phys_cap is not in the verdict path")
    add("verdict", "causal_claim", "NONE", "", "DECLARED", "no causal claim")
    add("verdict", "direction_claim", "NONE", "", "DECLARED", "no direction claim")
    add("verdict", "held_use", "NONE", "", "DECLARED", "no HELD item used or fabricated")

    # blocked and HELD
    for ind, detail in sorted(school_unable):
        add("blocked_input", ind, "unable", "", "OBSERVED", "%s; %s" % (SCHOOL_EXP, detail))
    for ind, detail in sorted(state_unable):
        add("blocked_input", ind, "unable", "", "OBSERVED", "%s; %s" % (STATE_CAP, detail))
    add("blocked_input", "falsifier_conflicts", len(conflicts), "objects", "DERIVED",
        "same-object/year conflicts between the two on-disk copies; 0 = no conflict")
    for item in HELD_ITEMS:
        add("held", item, "HELD", "", "HELD", "not on disk; not used; user approval required (D135/D146)")

    # closed claims
    for item in ("no_phys_cap_change", "no_re_fit", "no_fabrication", "no_proxy_outside_family",
                 "no_causal_claim", "no_direction_claim", "no_level_bar", "adopt_nothing"):
        add("closed_claim", item, "TRUE", "", "DECLARED", "closed-claim check (PRE_DECLARATIONS.md section 6)")

    res_path = os.path.join(outdir, "PLACES_BOUND_RESULTS.csv")
    with open(res_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["record_type", "item", "value", "unit", "label", "note"],
                           lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    det_fields = ["cell_id", "required_year", "cell_role", "divisor_source", "divisor_indicator",
                  "divisor_year", "divisor_value", "level_relation", "enrolment_ratio_indicator",
                  "enrolment_ratio_year", "enrolment_ratio_value_pct", "enrolment_ratio_relation",
                  "norm_class_size", "rooms_per_enrolled_student", "implied_coverage", "required_coverage",
                  "gap_pp", "vs_required_state", "relation_to_required_year", "verdict_bearing",
                  "admissible_for_verdict", "label", "note"]
    det_path = os.path.join(outdir, "PLACES_BOUND_DETAIL.csv")
    with open(det_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=det_fields, lineterminator="\n")
        w.writeheader()
        for i, c in enumerate(cells, 1):
            r = dict(c)
            r["cell_id"] = "C%03d" % i
            for k in ("divisor_value", "enrolment_ratio_value_pct", "rooms_per_enrolled_student",
                      "implied_coverage", "required_coverage"):
                r[k] = fmt(r[k])
            r["gap_pp"] = fmt_pp(r["gap_pp"])
            r["verdict_bearing"] = fmt(r["verdict_bearing"])
            r["admissible_for_verdict"] = fmt(r["admissible_for_verdict"])
            w.writerow({k: r[k] for k in det_fields})

    # ------------------------------------------------------------------ distortion statement
    lines = []
    lines.append("# PROXY DISTORTION — EXP-19 PLACES-BOUND\n")
    lines.append("**Status:** companion to `PLACES_BOUND_RESULTS.csv` and `PLACES_BOUND_DETAIL.csv`; generated "
                 "deterministically by `code/run_places_bound.py`. **Adopt nothing.**\n")
    lines.append("## 1. What the proxy is, and what it is not\n")
    lines.append("The proxy is an **implied `seats/cohort`**, not a place count. No count of public schools, "
                 "classrooms or construction completions is on disk (the delivery rows are `unable`). The proxy "
                 "infers rooms from an observed **group-size divisor** and converts rooms to places at a declared "
                 "norm class size:\n")
    lines.append("```")
    lines.append("F1 (class-size): coverage(n,t) = GER(t,level) * n / class_size(t,level)")
    lines.append("F2 (PTR):        coverage(n,t) = GER(t,level) * n / PTR(t,level)   [one class per teacher]")
    lines.append("```\n")
    lines.append("`n in {40, 45, 50}` is declared; **none is adopted**. Every output is `DERIVED` from `OBSERVED` "
                 "ratio/enrolment values.\n")
    lines.append("## 2. Declared assumptions (each is a distortion if false)\n")
    lines.append("| id | assumption | distortion if false |")
    lines.append("|---|---|---|")
    lines.append("| A1 | a usable classroom supplies exactly `n` student places | ignores double shifts, room-sharing, "
                 "rented/anchor rooms, non-teaching rooms, decay, utilisation |")
    lines.append("| A2 | rooms = enrolment / observed students-per-classroom ratio | the ratio is a national average of a "
                 "ratio, not a room census; unused rooms are inside the average |")
    lines.append("| A3 | GER = enrolment/cohort and is bridged to seats/cohort by A1 | GER is gross and includes overage "
                 "and repeaters; it is not a seats/cohort measure |")
    lines.append("| A4 | divisor and enrolment ratio are same-level (JHS / lower secondary) | level mismatch changes the "
                 "implied coverage; elementary/SHS are reported only as sensitivities |")
    lines.append("| A5 | divisor exact at `t`, else carried at `t+/-1`; enrolment ratio exact at `t` | a carried divisor "
                 "uses a neighbouring year's class size; no interpolation is done |")
    lines.append("| A6 | where lower-secondary GER is absent, broader `ger_secondary` is used and flagged | 2021 is "
                 "converted on a broader enrolment object than 2018 |")
    lines.append("| A7 | F2 requires one class per teacher | at secondary this is false where teachers are "
                 "subject-specialised; the on-disk PTR-24 vs class-size-39/44 pair implies ~1.6–1.8 teachers per room |")
    lines.append("| A8 | no cohort count is invented | no observed lower-secondary cohort count is on disk; GER is used "
                 "because it is a ratio |")
    lines.append("")
    lines.append("## 3. Why the proxy is not a place count\n")
    lines.append("A place count would be a census of rooms (or of seats) at a date. The observed record contains "
                 "**students per room** and **students per teacher**, not rooms, seats, schools or construction. "
                 "Converting a ratio to a count requires the enrolment denominator, and converting rooms to "
                 "adequate places requires a norm and an adequacy standard. Both are declared here, not observed. "
                 "The five 2021 congested-share values (90.0, 76.8, 66.0, 60.1, 57.7%) are observed but are shares, "
                 "not counts; they are not used in the verdict.\n")
    lines.append("## 4. The declared intervals (DERIVED)\n")
    lines.append("| norm n | I_n = [min, max] over primary F1 cells | span(I_n) | required span | classification |")
    lines.append("|---|---|---|---|---|")
    for n in NORMS:
        lo, hi = intervals[n]
        lines.append("| %d | [%s, %s] | %s | %s | %s |"
                     % (n, fmt(lo), fmt(hi), fmt(spans[n]), fmt(required_span), classifications[n]))
    lines.append("")
    lines.append("The required state is `R = [%s, %s]` (DERIVED, EXP-17). The interval is built only from the "
                 "primary F1 cells; the F2, broader-GER and elementary/SHS cells are reported separately and are "
                 "**not** verdict-bearing.\n" % (fmt(REQUIRED_2018), fmt(REQUIRED_2021)))
    lines.append("## 5. The identification limitation (why the verdict is SILENT)\n")
    lines.append("The JHS class-size ratio is observed at %s. `ger_lower_secondary` is observed through %s. "
                 "**The two year sets do not intersect** (intersection = %d year(s)). The 2018 required year uses a "
                 "2019 class size (carried one year); the 2021 required year uses the broader `ger_secondary` "
                 "(level fallback). No required year supplies a same-year, level-matched pair, so the conversion is "
                 "not identified at the required object. The interval is a sensitivity, not a bound.\n"
                 % (";".join(str(y) for y in jhs_years),
                    max(ger_lower_years) if ger_lower_years else "n/a", len(intersection)))
    lines.append("## 6. What would remove the distortion\n")
    lines.append("A measured classroom stock (rooms by year), a measured seats series, or a year that observes both "
                 "the JHS class-size ratio and `ger_lower_secondary`. None is on disk; the measured places/PTR "
                 "series and capacity utilisation are **HELD** (D146) and are not fabricated here. **No external "
                 "request is made; user approval is required for any HELD item.**\n")
    dist_path = os.path.join(outdir, "PROXY_DISTORTION.md")
    with open(dist_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    # ------------------------------------------------------------------ console
    console = []
    console.append("EXP-19 PLACES-BOUND  (predecl %s)" % PRE_DECL_SHA256)
    console.append("freeze check: PASS")
    console.append("required state: R = [%s, %s] (DERIVED, EXP-17)" % (fmt(REQUIRED_2018), fmt(REQUIRED_2021)))
    console.append("norms: 40, 45, 50 (declared; none adopted)")
    console.append("JHS class-size years: %s" % (",".join(str(y) for y in jhs_years)))
    console.append("ger_lower_secondary last year: %s; intersection: %d" % (
        max(ger_lower_years) if ger_lower_years else "n/a", len(intersection)))
    for n in NORMS:
        lo, hi = intervals[n]
        console.append("  n=%d  I=[%s, %s]  %s" % (n, fmt(lo), fmt(hi), classifications[n]))
    for c in primary:
        console.append("  %d n=%d  coverage=%s  (divisor %d=%.12g, GER %s %d=%.12g)" % (
            c["required_year"], c["norm_class_size"], fmt(c["implied_coverage"]),
            c["divisor_year"], c["divisor_value"], c["enrolment_ratio_indicator"],
            c["enrolment_ratio_year"], c["enrolment_ratio_value_pct"]))
    console.append("identification gate: %s (exact 2018=%d, exact 2021=%d)" % (
        "PASS" if gate else "FAIL", exact_by_year[2018], exact_by_year[2021]))
    console.append("inside/outside/straddle: %d/%d/%d" % (inside_n, outside_n, straddle_n))
    console.append("headline counterfactual (non-verdict-bearing): %s" % headline)
    console.append("VERDICT: %s" % verdict)
    console.append("reason: %s" % reason)
    console.append("adoption: NONE; phys_cap change: NONE; causal/direction claim: NONE; HELD use: NONE")
    console_text = "\n".join(console) + "\n"
    with open(os.path.join(outdir, "console.txt"), "w", encoding="utf-8") as fh:
        fh.write(console_text)
    sys.stdout.write(console_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
