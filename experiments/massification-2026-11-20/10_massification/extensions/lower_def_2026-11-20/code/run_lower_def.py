#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-13 LOWER-DEF — where does the lower-secondary series lose its 13.35 pp?

Frozen arithmetic for Council brief 023 section 6.3 (D136 #3, rank #3).
Implements PRE_DECLARATIONS.md exactly. Read-only on every input.

Determinism: no RNG, no clock, no network, no environment-dependent ordering,
no timestamps in any output. Two executions produce byte-identical CSVs.

Usage:
    python run_lower_def.py --outdir results
"""

import argparse
import csv
import hashlib
import json
import math
import os
import sys

# ---------------------------------------------------------------------------
# 0. Frozen declared constants (predeclaration sections 2-4). Nothing fitted.
# ---------------------------------------------------------------------------
ROOT = ("/Users/treymenefee/massification_live/experiments/"
        "massification-2026-11-20")

PANEL = os.path.join(ROOT, "10_massification/extensions/synthetic_2026-11-20/"
                           "generator_v1_2/results/synthetic_panel_v1_2.csv")
SIM = os.path.join(ROOT, "10_massification/extensions/synthetic_2026-11-20/"
                         "generator_v1_2/code/sim_v1_2.py")
PARAMS = os.path.join(ROOT, "10_massification/extensions/synthetic_2026-11-20/"
                            "generator_v1_2/PARAMS.md")
SERIES = os.path.join(ROOT, "10_massification/data/UNIVERSALIZATION_SERIES.csv")
BRIEF = os.path.join(ROOT, "08_council/brief_023/SYNTHESIS_023.md")
DECISIONS = os.path.join(ROOT, "08_council/DECISIONS.md")

DVEC = {"primary": 6, "lower_secondary": 3, "upper_secondary": 3, "tertiary": 4}
M_FACTOR = 1.10                 # meas_completion_factor, sim_v1_2.py:133  CONVENTION
R_REQUIRED = 0.8076             # 80.76 = 76.6391/0.949  (V12/D133)      DERIVED
SURV_MAX = {"primary": 0.96, "lower_secondary": 0.91,
            "upper_secondary": 0.90, "tertiary": 0.90}      # PARAMS.md 4.1  DECLARED
SURV_THETA = {"primary": 1.0, "lower_secondary": 1.0,
              "upper_secondary": 1.0, "tertiary": 0.80}
GAMMA = 0.55                    # PARAMS.md 4.1                            DECLARED
PHYS_CAP = 1.15                 # PARAMS.md 4.1                            DECLARED
OVERAGE_CAP = 1.05              # PARAMS.md 4.1                            CONVENTION

TOL_IDENTITY = 1e-9             # block clause 5                            DECLARED
TOL_DISPLAY = 5e-7              # predeclared rounding rule (section 2)     DECLARED
THRESH_X_CARRIED = 50.0         # block clause 5                            DECLARED
THRESH_JOINT_PP = 10.0          # block clause 5                            DECLARED

VERDICT_TYPE = "SYN00_PHL_LIKE"
VERDICT_LEVEL = "lower_secondary"
VERDICT_YEAR = 2021
SECONDARY_YEARS = (2017, 2022, 2024)


# ---------------------------------------------------------------------------
# 1. Formatting helpers (stable across runs)
# ---------------------------------------------------------------------------
def g12(x):
    """12 significant digits; stable repr for floats."""
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    if x == int(x) and abs(x) < 1e15:
        return f"{int(x)}.0"
    return f"{x:.12g}"


def f6(x):
    if x is None:
        return ""
    return f"{x:.6f}"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# 2. Inputs (read-only)
# ---------------------------------------------------------------------------
def load_panel():
    """{(country, level, year): row-dict of floats} plus ordered country list."""
    cells, countries = {}, []
    with open(PANEL, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            c, lv, yr = row["country"], row["level"], int(row["year"])
            if c not in countries:
                countries.append(c)
            keep = ("cohort", "admitted_official", "survival", "completion_cohort",
                    "completion_uis", "measurement_factor", "quality_q",
                    "congestion_q", "seat_coverage", "seats", "enrolment", "ger")
            rec = {k: float(row[k]) for k in keep}
            cells[(c, lv, yr)] = rec
    return cells, countries


def load_observed():
    """OBSERVED PHL lower-secondary completion, 2021 status=observed."""
    out = {}
    with open(SERIES, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if (row["iso3"] == "PHL"
                    and row["indicator"] == "completion_lower_secondary"):
                out[int(row["year"])] = (float(row["value"]), row["status"])
    return out


# ---------------------------------------------------------------------------
# 3. The declared chain (predeclaration section 2)
# ---------------------------------------------------------------------------
def chain(cells, country, level, year):
    """Reconstruct m * admission_rate(t-DVEC) * survival(t) and check identity."""
    lag = DVEC[level]
    entry = year - lag
    cur = cells[(country, level, year)]
    rec = {
        "country": country, "level": level, "year": year, "entry_year": entry,
        "dvec": lag, "survival": cur["survival"],
        "measurement_factor": cur["measurement_factor"],
        "completion_cohort": cur["completion_cohort"],
        "completion_uis": cur["completion_uis"],
        "quality_q": cur["quality_q"], "congestion_q": cur["congestion_q"],
        "seat_coverage": cur["seat_coverage"],
        "survival_max": SURV_MAX[level],
        "entry": None, "chain_value": None, "abs_error": None, "passes": None,
    }
    if (country, level, entry) in cells:
        prev = cells[(country, level, entry)]
        adm_rate = prev["admitted_official"] / prev["cohort"]
        rec["entry"] = prev
        rec["admission_rate"] = adm_rate
        val = cur["measurement_factor"] * adm_rate * cur["survival"]
        rec["chain_value"] = val
        rec["abs_error"] = abs(val - cur["completion_uis"])
        rec["passes"] = rec["abs_error"] <= TOL_IDENTITY
        # which term of min(phys_cap*seats, overage_cap*cohort) bound the gate?
        phys = PHYS_CAP * prev["seats"]
        cap = OVERAGE_CAP * prev["cohort"]
        rec["gate_binding_term"] = "phys_cap*seats" if phys <= cap else "overage_cap*cohort"
        rec["gate_capacity"] = min(phys, cap)
        rec["gate_identity_error"] = abs(adm_rate - min(phys, cap) / prev["cohort"]) \
            if prev is not None else None
    return rec


# ---------------------------------------------------------------------------
# 4. Attribution rules (predeclaration section 5)
# ---------------------------------------------------------------------------
def gap_objects(m, a, s, R=R_REQUIRED):
    log_c = math.log(m) + math.log(a) + math.log(s)
    return {
        "G_log": math.log(R) - log_c,
        "G_pp": 100.0 * (R - m * a * s),
        "realised": m * a * s,
    }


def d1_shares(m, a, s, R=R_REQUIRED, w_a=0.5):
    """Declared equal-split (Shapley) attribution. w_a = weight on rationing.

    Convention held at its declared value (m* = m); the residual required log
    product ln(R/m) is split between the two state factors with weight w_a.
    """
    log_target = math.log(R / m)
    a_star = math.exp(w_a * log_target)
    s_star = math.exp((1.0 - w_a) * log_target)
    G = math.log(R) - (math.log(m) + math.log(a) + math.log(s))
    c = {"convention": math.log(m / m),
         "rationing": math.log(a_star / a),
         "survival": math.log(s_star / s)}
    shares = {k: 100.0 * v / G for k, v in c.items()}
    return {"G_log": G, "a_star": a_star, "s_star": s_star,
            "c": c, "shares": shares,
            "sum_residual": sum(c.values()) - G,
            "shares_sum": sum(shares.values())}


def d2_shares(m, a, s, R=R_REQUIRED):
    """Absolute-log shares (non-verdict-bearing)."""
    w = {"convention": abs(math.log(m)), "rationing": abs(math.log(a)),
         "survival": abs(math.log(s))}
    tot = w["convention"] + w["rationing"] + w["survival"]
    return {k: 100.0 * v / tot for k, v in w.items()}


def verdict(shares):
    """Predeclaration section 6.2, in the frozen order."""
    order = sorted(shares.items(), key=lambda kv: (-kv[1], kv[0]))
    top_name, top = order[0]
    second_name, second = order[1]
    delta = top - second
    label, flag = None, ""
    if delta <= THRESH_JOINT_PP:
        label = "JOINT"
    elif top >= THRESH_X_CARRIED:
        label = "%s-CARRIED" % top_name.upper()
    else:
        label = "JOINT"
        flag = "NO-MAJORITY"
    literal = ("%s-CARRIED" % top_name.upper()
               if top >= THRESH_X_CARRIED else "JOINT")
    return {"label": label, "flag": flag, "literal": literal,
            "top": top_name, "top_share": top, "second": second_name,
            "second_share": second, "delta": delta}


def reachability(m, a, s):
    """Predeclaration section 5.3, declared tests only."""
    out = {}
    m_req = R_REQUIRED / (a * s)
    a_req = R_REQUIRED / (m * s)
    s_req = R_REQUIRED / (m * a)
    out["required_m"] = m_req
    out["required_a"] = a_req
    out["required_s"] = s_req
    out["required_cover_entry"] = a_req / PHYS_CAP
    out["m_tag"] = "ARITH-ONLY_DECLARED-EXCLUDED"
    out["a_tag"] = ("REACHABLE-BY-CAPACITY" if a_req / PHYS_CAP <= 1.0
                    else "UNREACHABLE-BY-CAPACITY")
    out["s_tag"] = ("UNREACHABLE-UNDER-DECLARED-LAW" if s_req > SURV_MAX["lower_secondary"]
                    else "REACHABLE-UNDER-DECLARED-LAW")
    out["max_at_surv_max"] = m * a * SURV_MAX["lower_secondary"]
    out["shortfall_at_surv_max_pp"] = 100.0 * (R_REQUIRED - out["max_at_surv_max"])
    return out


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="results")
    ap.add_argument("--root", default=ROOT)
    args = ap.parse_args()
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    cells, countries = load_panel()
    observed = load_observed()

    # ---- 5a. verdict cell + full lower-secondary series identity check -----
    detail = []
    identity_errors = []
    for level in ("primary", "lower_secondary", "upper_secondary", "tertiary"):
        for year in range(1970, 2026):
            rec = chain(cells, VERDICT_TYPE, level, year)
            if rec["chain_value"] is not None:
                rec["gap"] = gap_objects(rec["measurement_factor"],
                                         rec["admission_rate"],
                                         rec["survival"])
                if level == VERDICT_LEVEL:
                    d1 = d1_shares(rec["measurement_factor"],
                                   rec["admission_rate"], rec["survival"])
                    rec["d1"] = d1
                    rec["verdict"] = verdict(d1["shares"])
                    identity_errors.append((rec["year"], rec["abs_error"]))
                else:
                    rec["d1"] = None
                    rec["verdict"] = None
            else:
                rec["gap"] = None
                rec["d1"] = None
                rec["verdict"] = None
            detail.append(rec)

    vc = [r for r in detail
          if r["level"] == VERDICT_LEVEL and r["year"] == VERDICT_YEAR][0]
    m, a, s = (vc["measurement_factor"], vc["admission_rate"], vc["survival"])
    gp = gap_objects(m, a, s)
    d1 = d1_shares(m, a, s)
    vd = verdict(d1["shares"])
    d2 = d2_shares(m, a, s)
    alt25 = d1_shares(m, a, s, w_a=0.25)
    alt75 = d1_shares(m, a, s, w_a=0.75)
    reach = reachability(m, a, s)

    scored = [r for r in detail
              if r["level"] == VERDICT_LEVEL and r["chain_value"] is not None]
    scored_fail = [r for r in scored if not r["passes"]]
    max_err_scored = max(r["abs_error"] for r in scored)
    identity_ok = len(scored_fail) == 0

    # display reproduction with the block's 6-dp constants
    disp = M_FACTOR * 0.783805 * 0.781819
    disp_err = abs(disp - vc["completion_uis"])

    # final overall label (falsifier first, section 6.2 step 1)
    overall = "UNDETERMINED" if not identity_ok else vd["label"]
    literal = "UNDETERMINED" if not identity_ok else vd["literal"]

    # ---- 5b. secondary: all 30 types, 2021 --------------------------------
    types_rows = []
    for idx, c in enumerate(countries):
        rec = chain(cells, c, VERDICT_LEVEL, VERDICT_YEAR)
        row = {
            "country": c, "country_index": idx, "level": VERDICT_LEVEL,
            "year": VERDICT_YEAR, "entry_year": rec["entry_year"],
            "dvec": rec["dvec"],
        }
        if rec["chain_value"] is not None:
            g2 = gap_objects(rec["measurement_factor"], rec["admission_rate"],
                             rec["survival"])
            d1t = d1_shares(rec["measurement_factor"], rec["admission_rate"],
                            rec["survival"])
            vdt = verdict(d1t["shares"])
            row.update({
                "admission_rate": g12(rec["admission_rate"]),
                "survival": g12(rec["survival"]),
                "measurement_factor": g12(rec["measurement_factor"]),
                "seat_coverage_2021": g12(rec["seat_coverage"]),
                "seat_coverage_entry": g12(rec["entry"]["seat_coverage"]),
                "quality_q": g12(rec["quality_q"]),
                "completion_uis": g12(rec["completion_uis"]),
                "chain_reconstruction": g12(rec["chain_value"]),
                "chain_abs_error": g12(rec["abs_error"]),
                "chain_check_pass": "yes" if rec["passes"] else "no",
                "gap_pp_vs_declared_required": f6(g2["G_pp"]),
                "shortfall": "yes" if g2["G_pp"] > 0 else "no",
            })
            if g2["G_pp"] > 0:
                row.update({
                    "share_convention_pct": f6(d1t["shares"]["convention"]),
                    "share_rationing_pct": f6(d1t["shares"]["rationing"]),
                    "share_survival_pct": f6(d1t["shares"]["survival"]),
                    "verdict_label": vdt["label"],
                    "tag": "",
                })
            else:
                row.update({
                    "share_convention_pct": "", "share_rationing_pct": "",
                    "share_survival_pct": "", "verdict_label": "NO-SHORTFALL",
                    "tag": "no shortfall against the common declared yardstick",
                })
        else:
            for k in ("admission_rate", "survival", "measurement_factor",
                      "seat_coverage_2021", "seat_coverage_entry", "quality_q",
                      "completion_uis", "chain_reconstruction", "chain_abs_error",
                      "gap_pp_vs_declared_required", "share_convention_pct",
                      "share_rationing_pct", "share_survival_pct"):
                row[k] = ""
            row.update({"chain_check_pass": "n/a", "shortfall": "n/a",
                        "verdict_label": "NO-CHAIN",
                        "tag": "entry year outside panel"})
        types_rows.append(row)

    types_fail = [r for r in types_rows
                  if r["chain_check_pass"] == "no"]
    types_short = [r for r in types_rows if r["shortfall"] == "yes"]

    # ---- 5c. declared split-weight interval in which D1 still returns JOINT --
    # share_a - share_s = (2w-1)*L + ln(s/a) with L = ln(R/m) < 0.  JOINT iff
    # |that| <= 0.10*G_log.  This bounds how much of the label is the declared
    # normalisation; it is a disclosure of the rule, not a new threshold.
    _L = math.log(R_REQUIRED / m)
    _k = math.log(s) - math.log(a)
    _u_lo = (0.10 * gp["G_log"] - _k) / _L
    _u_hi = (-0.10 * gp["G_log"] - _k) / _L
    _w_lo = (1.0 + min(_u_lo, _u_hi)) / 2.0
    _w_hi = (1.0 + max(_u_lo, _u_hi)) / 2.0
    # cross-check: D1 at the interval edges must straddle the 10 pp window
    _edge_lo = d1_shares(m, a, s, w_a=_w_lo)["shares"]
    _edge_hi = d1_shares(m, a, s, w_a=_w_hi)["shares"]
    _edge_gap_lo = abs(_edge_lo["rationing"] - _edge_lo["survival"])
    _edge_gap_hi = abs(_edge_hi["rationing"] - _edge_hi["survival"])
    no_short = [r["year"] for r in detail
                if r["level"] == VERDICT_LEVEL and r["chain_value"] is not None
                and r["gap"]["G_pp"] <= 0.0]

    # ---- 5d. write LOWER_DEF_DETAIL.csv ----------------------------------
    det_path = os.path.join(outdir, "LOWER_DEF_DETAIL.csv")
    det_cols = ["country", "level", "year", "entry_year", "dvec",
                "admitted_official_entry", "cohort_entry", "admission_rate",
                "survival", "measurement_factor", "quality_q", "congestion_q",
                "seat_coverage", "survival_max_declared", "completion_cohort",
                "m_times_completion_cohort", "completion_uis",
                "chain_reconstruction", "chain_abs_error", "chain_check_pass",
                "gate_binding_term", "gate_identity_abs_error",
                "gap_pp_vs_required", "gap_log_vs_required",
                "share_convention_pct", "share_rationing_pct",
                "share_survival_pct", "verdict_label",
                "verdict_label_literal_order", "share_rule_note",
                "in_verdict_scope"]
    with open(det_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=det_cols, lineterminator="\n")
        w.writeheader()
        for r in detail:
            ent = r["entry"]
            mcc = (r["measurement_factor"] * r["completion_cohort"])
            row = {
                "country": r["country"], "level": r["level"], "year": r["year"],
                "entry_year": r["entry_year"], "dvec": r["dvec"],
                "admitted_official_entry": g12(ent["admitted_official"]) if ent else "",
                "cohort_entry": g12(ent["cohort"]) if ent else "",
                "admission_rate": g12(r.get("admission_rate")),
                "survival": g12(r["survival"]),
                "measurement_factor": g12(r["measurement_factor"]),
                "quality_q": g12(r["quality_q"]),
                "congestion_q": g12(r["congestion_q"]),
                "seat_coverage": g12(r["seat_coverage"]),
                "survival_max_declared": g12(r["survival_max"]),
                "completion_cohort": g12(r["completion_cohort"]),
                "m_times_completion_cohort": g12(mcc),
                "completion_uis": g12(r["completion_uis"]),
                "chain_reconstruction": g12(r["chain_value"]),
                "chain_abs_error": g12(r["abs_error"]),
                "chain_check_pass": ("yes" if r["passes"] else "no") if r["passes"] is not None else "",
                "gate_binding_term": r.get("gate_binding_term", ""),
                "gate_identity_abs_error": g12(r.get("gate_identity_error")),
                "gap_pp_vs_required": f6(r["gap"]["G_pp"]) if r["gap"] and r["level"] == VERDICT_LEVEL else "",
                "gap_log_vs_required": g12(r["gap"]["G_log"]) if r["gap"] and r["level"] == VERDICT_LEVEL else "",
                "share_convention_pct": f6(r["d1"]["shares"]["convention"]) if r["d1"] and r["gap"]["G_pp"] > 0 else "",
                "share_rationing_pct": f6(r["d1"]["shares"]["rationing"]) if r["d1"] and r["gap"]["G_pp"] > 0 else "",
                "share_survival_pct": f6(r["d1"]["shares"]["survival"]) if r["d1"] and r["gap"]["G_pp"] > 0 else "",
                "verdict_label": (r["verdict"]["label"] if r["verdict"] else "") if (r["d1"] and r["gap"]["G_pp"] > 0) else ("NO-SHORTFALL" if r["d1"] else ""),
                "verdict_label_literal_order": (r["verdict"]["literal"] if r["verdict"] else "") if (r["d1"] and r["gap"]["G_pp"] > 0) else ("NO-SHORTFALL" if r["d1"] else ""),
                "share_rule_note": (
                    "ill-conditioned: the D1 required state is year-invariant while the gap is not, "
                    "so a factor's share can exceed 100 % or turn negative near the crossing; "
                    "descriptive only, never a verdict"
                    if r["d1"] and min(r["d1"]["shares"].values()) < 0.0 else ""),
                "in_verdict_scope": ("yes" if (r["level"] == VERDICT_LEVEL) else "no"),
            }
            w.writerow(row)

    # ---- 5d. write LOWER_DEF_TYPES.csv -----------------------------------
    typ_path = os.path.join(outdir, "LOWER_DEF_TYPES.csv")
    typ_cols = ["country", "country_index", "level", "year", "entry_year",
                "dvec", "admission_rate", "survival", "measurement_factor",
                "seat_coverage_2021", "seat_coverage_entry", "quality_q",
                "completion_uis", "chain_reconstruction", "chain_abs_error",
                "chain_check_pass", "gap_pp_vs_declared_required", "shortfall",
                "share_convention_pct", "share_rationing_pct",
                "share_survival_pct", "verdict_label", "tag"]
    with open(typ_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=typ_cols, lineterminator="\n")
        w.writeheader()
        for r in types_rows:
            w.writerow({k: r.get(k, "") for k in typ_cols})

    # ---- 5e. write LOWER_DEF_RESULTS.csv ---------------------------------
    res_path = os.path.join(outdir, "LOWER_DEF_RESULTS.csv")
    res_cols = ["record_type", "factor", "realised_value", "required_value_d1",
                "log_contribution", "share_pct_d1", "share_pct_d2",
                "share_pct_alt_w25", "share_pct_alt_w75",
                "single_lever_required", "single_lever_reachability",
                "verdict_label", "component_name", "component_value",
                "component_unit", "label", "note"]
    rows = []

    def add(**kw):
        base = {k: "" for k in res_cols}
        base.update(kw)
        rows.append(base)

    add(record_type="meta", factor="experiment", component_name="experiment",
        component_value="EXP-13 LOWER-DEF", label="DECLARED",
        note="brief 023 section 6.3; D136 #3 rank #3; predeclaration sha256 in RUN_MANIFEST.json")
    add(record_type="meta", factor="verdict_cell", component_name="verdict_cell",
        component_value=f"{VERDICT_TYPE}|{VERDICT_LEVEL}|{VERDICT_YEAR}",
        label="SYNTHETIC", note="single scored cell; identity scope is the whole lower series 1973-2025")

    for name, lab, note in (
            ("convention", "CONVENTION", "m = meas_completion_factor; declared constant, held at its value by D1"),
            ("rationing", "SYNTHETIC", "admitted_official/cohort at entry year t-3; the lower gate"),
            ("survival", "SYNTHETIC", "panel survival(t) = clip(surv_max*Q^theta); quality/congestion channel")):
        val = {"convention": m, "rationing": a, "survival": s}[name]
        req = {"convention": m, "rationing": d1["a_star"], "survival": d1["s_star"]}[name]
        lev = {"convention": reach["required_m"], "rationing": reach["required_a"],
               "survival": reach["required_s"]}[name]
        tag = {"convention": reach["m_tag"], "rationing": reach["a_tag"],
               "survival": reach["s_tag"]}[name]
        add(record_type="factor", factor=name, realised_value=g12(val),
            required_value_d1=g12(req), log_contribution=g12(d1["c"][name]),
            share_pct_d1=f6(d1["shares"][name]),
            share_pct_d2=f6(d2[name]),
            share_pct_alt_w25=f6(alt25["shares"][name]),
            share_pct_alt_w75=f6(alt75["shares"][name]),
            single_lever_required=g12(lev), single_lever_reachability=tag,
            label=lab, note=note)

    add(record_type="verdict", verdict_label=overall, label="VERDICT",
        component_name="verdict_label", component_value=overall,
        note="frozen rule 6.2 (JOINT tested first); top=%s %.6f%% second=%s %.6f%% delta=%.6f pp; flag=%s"
             % (vd["top"], vd["top_share"], vd["second"], vd["second_share"],
                vd["delta"], vd["flag"] or "none"))
    add(record_type="verdict", verdict_label=literal, label="VERDICT-LITERAL-ORDER",
        component_name="verdict_label_literal_order", component_value=literal,
        note="block lists X-CARRIED first and states no precedence; reported for disclosure only (section 5.2 D4)")

    comps = [
        ("required_lower_2021", g12(R_REQUIRED), "ratio", "DERIVED",
         "80.76 = 76.6391/0.949 = 80.7577; internal-consistency requirement, not a target or forecast"),
        ("realised_chain_2021", g12(gp["realised"]), "ratio", "SYNTHETIC",
         "m * admission_rate(2018) * survival(2021)"),
        ("gap_pp", f6(gp["G_pp"]), "percentage points", "DERIVED",
         "100*(0.8076 - realised); the block's 13.35 pp"),
        ("gap_log", g12(gp["G_log"]), "log points", "DERIVED",
         "ln(0.8076) - ln(realised)"),
        ("identity_abs_error_2021", g12(vc["abs_error"]), "ratio", "SYNTHETIC",
         "|chain reconstruction - panel completion_uis| at the verdict cell; tolerance 1e-9"),
        ("identity_max_abs_error_lower_series", g12(max_err_scored), "ratio", "SYNTHETIC",
         "max over scored cells 1973-2025; tolerance 1e-9"),
        ("identity_cells_scored", str(len(scored)), "cells", "SYNTHETIC",
         "lower_secondary chain years 1973-2025"),
        ("identity_cells_failed", str(len(scored_fail)), "cells", "SYNTHETIC",
         "0 -> chain identity holds; >0 would force UNDETERMINED"),
        ("display_reproduction_6dp", g12(disp), "ratio", "DECLARED-ROUNDED",
         "1.10*0.783805*0.781819 as printed in the block"),
        ("display_reproduction_abs_error", g12(disp_err), "ratio", "DERIVED",
         "print rounding only; tolerance 5e-7; not an identity test"),
        ("declared_chain_constants", "1.10 * 0.783805 * 0.781819 = 0.674073", "expression", "DECLARED",
         "the block's own chain identity, reproduced verbatim"),
        ("m", g12(m), "ratio", "CONVENTION", "meas_completion_factor, sim_v1_2.py:133"),
        ("admission_rate_entry_2018", g12(a), "ratio", "SYNTHETIC",
         "admitted_official(2018)/cohort(2018); equals phys_cap*seat_coverage(2018) while the capacity term binds"),
        ("survival_2021", g12(s), "ratio", "SYNTHETIC", "panel survival(2021)"),
        ("surv_max_lower", g12(SURV_MAX["lower_secondary"]), "ratio", "DECLARED",
         "hard ceiling of the survival channel when Q<=1 (PARAMS.md 4.1)"),
        ("surv_theta_lower", g12(SURV_THETA["lower_secondary"]), "elasticity", "DECLARED",
         "PARAMS.md 4.1"),
        ("gamma", g12(GAMMA), "coefficient", "DECLARED", "quality decay on congestion"),
        ("phys_cap", g12(PHYS_CAP), "pupils per place", "DECLARED", "PARAMS.md 4.1"),
        ("quality_q_2021", g12(vc["quality_q"]), "index", "SYNTHETIC",
         "Q(2021) = exp(-gamma*max(0,q-1)); q = C/seats"),
        ("congestion_q_2021", g12(vc["congestion_q"]), "ratio", "SYNTHETIC", "cohort/seats in 2021"),
        ("seat_coverage_2021", g12(vc["seat_coverage"]), "places per cohort", "SYNTHETIC", "seats(2021)/cohort(2021)"),
        ("seat_coverage_entry_2018", g12(vc["entry"]["seat_coverage"]), "places per cohort", "SYNTHETIC",
         "seats(2018)/cohort(2018), the entry cohort of the 2021 completion"),
        ("gate_binding_term_entry", vc["gate_binding_term"], "term", "SYNTHETIC",
         "which term of min(phys_cap*seats, overage_cap*cohort) set the entry gate"),
        ("gate_identity_abs_error", g12(vc["gate_identity_error"]), "ratio", "DERIVED",
         "|admission_rate - gate_capacity/cohort| at entry; ~0 means the gate, not demand, set admission"),
        ("required_m", g12(reach["required_m"]), "ratio", "DERIVED",
         "m that alone closes the gap; DECLARED-EXCLUDED (FAIL-RE-FIT, D134)"),
        ("required_admission_rate", g12(reach["required_a"]), "ratio", "DERIVED",
         "admission rate that alone closes the gap"),
        ("required_entry_coverage", g12(reach["required_cover_entry"]), "places per cohort", "DERIVED",
         "required_admission_rate/phys_cap"),
        ("required_survival", g12(reach["required_s"]), "ratio", "DERIVED",
         "survival that alone closes the gap; compare surv_max_lower"),
        ("max_completion_at_surv_max", g12(reach["max_at_surv_max"]), "ratio", "DERIVED",
         "m*a*surv_max: the survival channel's ceiling for this cell"),
        ("shortfall_at_surv_max_pp", f6(reach["shortfall_at_surv_max_pp"]), "percentage points", "DERIVED",
         "how far the survival channel alone falls short of 80.76"),
        ("observed_PHL_lower_2021", g12(observed.get(2021, (None,))[0]), "percent", "OBSERVED",
         "UNIVERSALIZATION_SERIES.csv completion_lower_secondary, status=%s; reference only"
         % observed.get(2021, (None, "missing"))[1]),
        ("observed_minus_required_pp", f6(observed[2021][0] - 100.0 * R_REQUIRED), "percentage points", "DERIVED",
         "observed 80.896 against the model-side requirement 80.76; +0.14 pp, reference only"),
        ("share_gap_top_minus_second_pp", f6(vd["delta"]), "percentage points", "DERIVED",
         "%s vs %s" % (vd["top"], vd["second"])),
        ("channel_depth_survival_minus_rationing_pp", f6(100.0 * (s - a)), "percentage points", "DERIVED",
         "the two state channels' depths differ by %.4f pp (%.6f vs %.6f); they are near-equal by construction of the declared rules" % (100.0 * (s - a), s, a)),
        ("joint_split_weight_interval", "[%.6f, %.6f]" % (_w_lo, _w_hi), "weight on a*", "DERIVED",
         "declared weight w_a on rationing in a* for which D1 returns JOINT; outside it the same rule returns X-CARRIED. "
         "Edge cross-check: |share_a-share_s| = %.6f / %.6f pp against the 10 pp window" % (_edge_gap_lo, _edge_gap_hi)),
        ("completion_if_m_removed", g12(a * s), "ratio", "DERIVED",
         "arithmetic on the declared chain with m set to 1.0; NOT a model run and NOT a repair option"),
        ("gap_if_m_removed_pp", f6(100.0 * (R_REQUIRED - a * s)), "percentage points", "DERIVED",
         "if the 1.10 convention were dropped, the gap would widen by %.4f pp: the convention is a net uplift, not the loss"
         % (100.0 * (R_REQUIRED - a * s) - gp["G_pp"])),
        ("years_without_shortfall", ",".join(str(y) for y in no_short) or "none", "years", "DERIVED",
         "lower series chain years at or above the declared required value (no attribution reported for these)"),
        ("flip_condition_abs_log_diff", g12(abs(math.log(s) - math.log(a))), "log points", "DERIVED",
         "|ln surv - ln adm|; JOINT survives only while this is <= 0.10*G_log under D1"),
        ("flip_condition_threshold", g12(0.10 * gp["G_log"]), "log points", "DECLARED",
         "0.10*G_log, from the 10 pp JOINT window"),
        ("d1_share_sum_residual", g12(d1["shares_sum"] - 100.0), "percentage points", "DERIVED",
         "shares sum to 100 %% by construction"),
        ("threshold_x_carried_pct", g12(THRESH_X_CARRIED), "percent", "DECLARED", "block clause 5"),
        ("threshold_joint_pp", g12(THRESH_JOINT_PP), "percentage points", "DECLARED", "block clause 5"),
        ("tolerance_identity", g12(TOL_IDENTITY), "ratio", "DECLARED", "block clause 5"),
        ("gap_2017_pp", f6([r for r in detail if r["level"] == VERDICT_LEVEL and r["year"] == 2017][0]["gap"]["G_pp"]),
         "percentage points", "DERIVED", "secondary: shortfall localisation"),
        ("gap_2022_pp", f6([r for r in detail if r["level"] == VERDICT_LEVEL and r["year"] == 2022][0]["gap"]["G_pp"]),
         "percentage points", "DERIVED", "secondary: shortfall localisation"),
        ("gap_2024_pp", f6([r for r in detail if r["level"] == VERDICT_LEVEL and r["year"] == 2024][0]["gap"]["G_pp"]),
         "percentage points", "DERIVED", "secondary: shortfall localisation"),
        ("types_with_shortfall_2021", str(len(types_short)), "of 30", "SYNTHETIC",
         "types whose 2021 lower chain value is below the common declared yardstick 0.8076"),
        ("types_identity_failures_2021", str(len(types_fail)), "of 30", "SYNTHETIC",
         "secondary; cannot affect the verdict (section 6.3)"),
        ("clip_boundary", "completion_uis clipped to [0,1]", "text", "DECLARED",
         "never binds in lower_secondary; binds in primary 2024-2025 (descriptive rows only)"),
    ]
    for name, val, unit, lab, note in comps:
        add(record_type="component", component_name=name, component_value=val,
            component_unit=unit, label=lab, note=note)

    with open(res_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=res_cols, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # ---- 5f. input hashes -------------------------------------------------
    hashes = {os.path.basename(p): {"path": p, "sha256": sha256(p),
                                    "bytes": os.path.getsize(p)}
              for p in (PANEL, SIM, PARAMS, SERIES, BRIEF, DECISIONS)}
    with open(os.path.join(outdir, "INPUT_HASHES.json"), "w", encoding="utf-8") as fh:
        json.dump(hashes, fh, indent=2, sort_keys=True)
        fh.write("\n")

    # ---- 5g. stdout summary ----------------------------------------------
    print("EXP-13 LOWER-DEF")
    print("  verdict cell         : %s | %s | %d" % (VERDICT_TYPE, VERDICT_LEVEL, VERDICT_YEAR))
    print("  chain                : %.12g = %.12g x %.12g x %.12g (panel %.12g, err %.3g, tol %.0e)"
          % (gp["realised"], m, a, s, vc["completion_uis"], vc["abs_error"], TOL_IDENTITY))
    print("  identity lower 1973-2025 : %d cells, %d failed, max err %.3g"
          % (len(scored), len(scored_fail), max_err_scored))
    print("  required / gap       : %.4f -> gap %.6f pp / %.12g log"
          % (R_REQUIRED, gp["G_pp"], gp["G_log"]))
    print("  D1 shares            : convention %.6f%%  rationing %.6f%%  survival %.6f%%"
          % (d1["shares"]["convention"], d1["shares"]["rationing"], d1["shares"]["survival"]))
    print("  D2 shares            : convention %.6f%%  rationing %.6f%%  survival %.6f%%"
          % (d2["convention"], d2["rationing"], d2["survival"]))
    print("  verdict              : %s (literal order: %s, flag=%s)"
          % (overall, literal, vd["flag"] or "none"))
    print("  single-lever         : m* %.6f [%s]  a* %.6f [%s]  s* %.6f [%s]"
          % (reach["required_m"], reach["m_tag"], reach["required_a"], reach["a_tag"],
             reach["required_s"], reach["s_tag"]))
    print("  writing              : %s" % os.path.abspath(outdir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
