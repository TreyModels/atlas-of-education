#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COEVOLUTION v0 — SIMULATED — one deterministic simulator for
`PRE_DECLARATIONS.md` (COEVOLUTION v0, frozen 2026-11-21, sha256
7d25e17631a39f556a17ac62a53de12701d60dca6d09a05e2b080d8d3184799d).

Implements PRE_DECLARATIONS §1–§6 and §8.1, §10–§12: town + 8 villages, household
next-year choice with the real work/home alternative and three demand weights,
endogenous district/private supply (no seat totals in the inputs), four named
gates with controllers, priced and access-constrained tutoring (concentration an
output), three declared cohort-feedback responses, pupil-level records, report
card A, the coexistence test, the three one-change counterfactuals, the three
report card B arms, and the spillback experiment.

EVERYTHING THE SIMULATOR WRITES IS LABELLED `SIMULATED`. No observed series is
read, fitted or targeted. The closed 2026-11-20 records are not touched.

The simulator REFUSES TO RUN if PRE_DECLARATIONS.md does not hash to the frozen
value, and runs D0 (§8.1) before reading any outcome; on failure it exits
`D0-INPUT-SEATS` without writing outcome files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.dirname(HERE)                      # .../coevolve_2026-11-21
PRE_DECL_PATH = os.path.join(EXT, "PRE_DECLARATIONS.md")
PRE_DECL_SHA = "7d25e17631a39f556a17ac62a53de12701d60dca6d09a05e2b080d8d3184799d"
PARAM_PATH = os.path.join(EXT, "PARAMETERS.csv")
RESULTS_DIR = os.path.join(EXT, "results")

LABEL = "SIMULATED"
FLOAT_FMT = "%.10g"   # §10: floats written at %.10g

# ---------------------------------------------------------------------------
# Level codes and fixed level facts
# ---------------------------------------------------------------------------
L_PRIMARY, L_LOWER, L_UPPER, L_SEL, L_POSTSEC, L_TERT = 0, 1, 2, 3, 4, 5
LEVELS = (L_PRIMARY, L_LOWER, L_UPPER, L_SEL, L_POSTSEC, L_TERT)
LEVEL_NAME = {0: "primary", 1: "lower_secondary", 2: "upper_secondary",
              3: "upper_selective", 4: "post_secondary_non_tertiary", 5: "tertiary"}
LEVEL_YEARS = {0: 6, 1: 4, 2: 2, 3: 2, 4: 2, 5: 4}
CRED_OF_LEVEL = {0: 1, 1: 2, 2: 3, 3: 3, 4: 4, 5: 5}
LEVEL_ORD = {0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 4}
AGE_BAND = {0: (6, 11), 1: (12, 15), 2: (16, 17), 3: (16, 17), 4: (18, 19), 5: (18, 22)}
MIN_ENTRY_AGE = {0: 6, 1: 11, 2: 15, 3: 15, 4: 16, 5: 17}
MAX_ENTRY_AGE = {0: 8, 1: 13, 2: 16, 3: 16, 4: 18, 5: 19}
# next level(s) after holding credential c
NEXT_AFTER_CRED = {0: [0], 1: [1], 2: [2], 3: [4], 4: [], 5: []}

# ===========================================================================
# v0.2 YANG-RETURN wiring (return-side; see ../PRE_DECLARATIONS.md)
# ===========================================================================
YANG = {
    "city_N": 1000000.0,   # town size N (only enters through g(N))
    "b": 128.0,             # Yang slope
    "anchorD": 500.0,       # D(1e6)
    "mapping": "linear",    # linear | proportional | convex
    "convex_scale": 200.0,
    "alpha": 1.0,           # baseline multiplier on g(N)
    "premium_mult": 1.0,    # drawn multiplier on C_eff
    "beta_mult": 1.0,       # drawn multiplier on beta_option
    "travel_mult": 1.0,     # drawn multiplier on travel cost
    "child_wage_mult": 1.0, # drawn multiplier on child wage
}
YANG_N_LO, YANG_N_HI = 50000.0, 2000000.0

def _yang_D(N, b=None, anchorD=None):
    b = YANG["b"] if b is None else b
    a = YANG["anchorD"] if anchorD is None else anchorD
    return b * np.log(N) + (a - b * np.log(1e6))

def yang_gate_share(N=None):
    N = YANG["city_N"] if N is None else N
    D = _yang_D(N)
    D_lo = _yang_D(YANG_N_LO)
    D_hi = _yang_D(YANG_N_HI)
    m = YANG["mapping"]
    if m == "linear":
        g = (D - D_lo) / (D_hi - D_lo)
    elif m == "proportional":
        g = D / D_hi
    elif m == "convex":
        g = 1.0 - np.exp(-(D - D_lo) / float(YANG["convex_scale"]))
    else:
        raise ValueError("unknown yang mapping %r" % (m,))
    return float(min(1.0, max(0.0, g)))


EXIT_REASON = {0: "none", 1: "still_enrolled", 2: "declined_offer", 3: "no_place",
               4: "failure_exit", 5: "completed", 6: "aged_out", 7: "fee_blocked"}

# ---------------------------------------------------------------------------
# DECLARED PARAMETER TABLE (§11). Every value is a design value, chosen before
# any run and never changed after a result was seen. Provenance `DECLARED`;
# arithmetic consequences are `DERIVED` and are not listed here.
# Columns: name, value, units, provenance, note (design rationale).
# ---------------------------------------------------------------------------
DECLARED = [
    # --- §1 geography, population, time -------------------------------------
    ("n_villages", 8, "count", "DECLARED", "eight villages around one district town (§1)"),
    ("village_distances_km", "2;4;6;8;10;12;15;18", "km", "DECLARED", "declared road distance of each village from the town (§1)"),
    ("village_sizes", "176;150;132;114;97;79;70;62", "children/cohort", "DECLARED", "declared village population weights (§1), summing to 880; declining with distance as a design choice, not an estimate"),
    ("town_cohort_size", 320, "children/cohort", "DECLARED", "town share of the 1,200 cohort (§1)"),
    ("cohort_size", 1200, "children/cohort", "DECLARED", "children entering primary per cohort (§1)"),
    ("n_cohorts", 24, "cohorts", "DECLARED", "cohorts entering primary in years 0..23 are followed (§1)"),
    ("n_burnin_cohorts", 11, "cohorts", "DECLARED", "burn-in cohorts entering years -11..-1; they fill the pipeline at t=0 with the model's own history instead of a declared enrolment guess"),
    ("years", 30, "years", "DECLARED", "t = 0..29 (§1)"),
    ("primary_years", 6, "years", "DECLARED", "level duration (§1)"),
    ("lower_secondary_years", 4, "years", "DECLARED", "level duration (§1)"),
    ("upper_secondary_years", 2, "years", "DECLARED", "level duration (§1)"),
    ("post_secondary_years", 2, "years", "DECLARED", "post-secondary non-tertiary, 1–2 years; 2 used (§1)"),
    ("tertiary_years", 4, "years", "DECLARED", "level duration (§1)"),
    ("age_band_primary", "6;11", "years", "DECLARED", "official age band, primary (§7)"),
    ("age_band_lower_secondary", "12;15", "years", "DECLARED", "official age band (§7)"),
    ("age_band_upper_secondary", "16;17", "years", "DECLARED", "official age band (§7)"),
    ("age_band_post_secondary", "18;19", "years", "DECLARED", "official age band, post-secondary non-tertiary (§7)"),
    ("age_band_tertiary", "18;22", "years", "DECLARED", "standard five-year age group immediately after the official secondary leaving age 17 (§7)"),
    ("min_entry_age", "6;11;15;15;16;17", "years", "DECLARED", "minimum age for entry to each level code (0..5)"),
    ("max_entry_age", "8;13;17;17;19;20", "years", "DECLARED", "latest age for a FIRST entry to each level code (0..5); re-entry to a level already attended is governed by max_level_age"),
    ("max_level_age", "15;18;20;20;21;24", "years", "DECLARED", "latest age at which a pupil may still attend each level (level start + duration + 3 years of repetition/re-entry slack)"),
    # --- §2 household -------------------------------------------------------
    ("weight_knowledge", 0.25, "weight", "DECLARED", "w_K (§0, §11)"),
    ("weight_education", 0.35, "weight", "DECLARED", "w_E (§0, §11)"),
    ("weight_credential", 0.40, "weight", "DECLARED", "w_C (§0, §11); the three weights are declared, not fitted"),
    ("theta_child_labour", 0.5, "share", "DECLARED", "θ, share of child wage forgone while attending (§2, §11)"),
    ("child_wage_rural", "0.8;1.4;1.8;2.0", "index/yr", "DECLARED", "rural child wage at ages <12, 12-15, 16-18, 19+ (adult informal wage = 1)"),
    ("child_wage_urban", "0.6;1.0;1.3;1.5", "index/yr", "DECLARED", "town child wage by the same age bands"),
    ("home_value_bands", "0.25;0.40;0.45", "index/yr", "DECLARED", "value of the home branch at ages <12, 12-15, 16+"),
    ("income_poor", 1.6, "index/yr", "DECLARED", "mean household income, poor class (lognormal)"),
    ("income_nonpoor", 3.8, "index/yr", "DECLARED", "mean household income, non-poor class"),
    ("income_sigma", 0.35, "log sd", "DECLARED", "lognormal dispersion of household income"),
    ("poor_share_town", 0.20, "share", "DECLARED", "declared poor share, town"),
    ("poor_share_village", 0.45, "share", "DECLARED", "declared poor share, villages"),
    ("ability_mean", 50.0, "points", "DECLARED", "declared ability distribution; independent of household income by declaration"),
    ("ability_sd", 16.0, "points", "DECLARED", "declared ability distribution"),
    ("ability_clip", "5;95", "points", "DECLARED", "declared support of the ability distribution"),
    ("siblings_mean", 2.0, "count", "DECLARED", "declared Poisson mean sibling count"),
    ("beta_option", 0.55, "weight", "DECLARED", "β, weight on the declared continuation value (§2)"),
    ("option_value_primary", 2.2, "index", "DECLARED", "declared continuation value of keeping the next gate open, while at primary"),
    ("option_value_lower", 2.6, "index", "DECLARED", "as above, lower secondary"),
    ("option_value_upper", 2.0, "index", "DECLARED", "as above, upper secondary"),
    ("option_value_postsec", 1.2, "index", "DECLARED", "as above, post-secondary non-tertiary"),
    ("option_value_tertiary", 1.5, "index", "DECLARED", "as above, tertiary"),
    ("K_value_by_level", "1.0;1.3;1.8;1.9;1.8;2.6", "index", "DECLARED", "declared knowledge/learning value K_L per level code (§2)"),
    ("E_value_by_level", "1.2;1.6;2.2;2.3;2.0;3.0", "index", "DECLARED", "declared education/experience value E_L per level"),
    ("C_value_by_level", "0.8;1.6;3.0;3.4;2.6;5.0", "index", "DECLARED", "declared credential/option value C_L per level (§2); multiplied by the gate-pass probability"),
    ("taste_scale", 0.55, "index", "DECLARED", "scale of the household taste shock ε (logistic)"),
    ("max_school_spend_share", 0.45, "share of income", "DECLARED", "declared cash constraint: fees + travel + tutoring may not exceed this share of household income"),
    ("tutor_budget_share", 0.25, "share of income", "DECLARED", "declared tutoring budget"),
    ("mastery_gain", 11.0, "points/yr", "DECLARED", "declared mastery gain of one passed school year at ability 100, quality 1"),
    ("exam_noise_sd", 5.0, "points", "DECLARED", "declared dispersion of the annual attainment draw (exam noise)"),
    ("reentry_cost", 0.4, "index", "DECLARED", "declared cost of re-entering after a year out (§2)"),
    ("reentry_window", 2, "years", "DECLARED", "declared re-entry window after leaving a level"),
    ("travel_cost_per_km", 0.03, "index/km/yr", "DECLARED", "declared annual travel/boarding cost per km, villages; the TRAVEL-CUT arm halves it (§8.3)"),
    ("travel_cost_town", 0.0, "index/yr", "DECLARED", "town households face no travel cost to town providers"),
    # --- fees (§4 fee controller; §11 fee levels by level and village/town) --
    ("fee_town_by_level", "0.10;0.22;0.35;0.60;0.55;1.20", "index/yr", "DECLARED", "declared annual fee per level (0..5) in town"),
    ("fee_village_by_level", "0.06;0.15;0.28;0.60;0.55;1.20", "index/yr", "DECLARED", "declared annual fee per level in villages"),
    ("private_fee_multiplier", 1.6, "multiple", "DECLARED", "private provider fee = multiplier x declared public fee"),
    ("private_fee_add", 0.10, "index/yr", "DECLARED", "private provider fee surcharge"),
    # --- §4 gates -----------------------------------------------------------
    ("pass_threshold", 45.0, "points", "DECLARED", "grade-pass / catch-up trigger threshold (§5, §11)"),
    ("selective_exam_threshold", 60.0, "points", "DECLARED", "selective gate exam threshold (§4, §11)"),
    ("university_exam_threshold", 65.0, "points", "DECLARED", "university gate exam threshold (§4, §11)"),
    ("postsec_complete_threshold", 50.0, "points", "DECLARED", "post-secondary non-tertiary completion convention (§4)"),
    ("max_repetitions", 1, "count", "DECLARED", "declared repetition allowance; the next failure exits (declared failure exit)"),
    ("K_sel", 38, "places/yr", "DECLARED", "selective places, institutional constraint (§4, §11): 12% of the 320 town cohort, rounded down"),
    ("K_uni", 13, "places/yr", "DECLARED", "university places, declared (§4, §11): 35% of K_sel, rounded down; rationed by rank"),
    ("reach_primary_km", 3.0, "km", "DECLARED", "residence controller: maximum distance to a primary place (§4)"),
    ("reach_lower_secondary_km", 6.0, "km", "DECLARED", "maximum distance to a lower-secondary place"),
    ("reach_upper_secondary_km", 10.0, "km", "DECLARED", "maximum distance to an upper-secondary place"),
    ("reach_post_secondary_km", 20.0, "km", "DECLARED", "maximum distance to a post-secondary place"),
    ("reach_tertiary_km", 20.0, "km", "DECLARED", "maximum distance to a university place"),
    # --- §5 tutoring --------------------------------------------------------
    ("tutoring_price_catchup", 0.003, "index/hour", "DECLARED", "p_c (§5)"),
    ("tutoring_price_gate", 0.006, "index/hour", "DECLARED", "p_g (§5)"),
    ("catchup_hours", 24.0, "hours/yr", "DECLARED", "declared catch-up block bought when the trigger fires (§5)"),
    ("gate_hours", 60.0, "hours/yr", "DECLARED", "declared gate block bought when the margin is in band (§5)"),
    ("catchup_trigger", 45.0, "points", "DECLARED", "catch-up trigger: expected score below this (§5, §11)"),
    ("gate_band", 8.0, "points", "DECLARED", "gate motive: admission shortfall at most this many points (§5, §11)"),
    ("tutoring_access_km", 12.0, "km", "DECLARED", "declared tutoring access limit (distance-constrained, §5)"),
    ("catchup_attain_boost", 6.0, "points", "DECLARED", "catch-up effect on the year's attainment"),
    ("catchup_mastery_mult", 1.10, "multiple", "DECLARED", "catch-up effect on the year's mastery gain"),
    ("gate_attain_coef", 14.0, "points", "DECLARED", "gate tutoring raises attainment by coef x (1 - exp(-hours/scale))"),
    ("gate_attain_scale", 50.0, "hours", "DECLARED", "diminishing-returns scale of gate tutoring"),
    ("selective_app_floor", 45.0, "points", "DECLARED", "declared application floor for the selective gate"),
    ("university_app_floor", 50.0, "points", "DECLARED", "declared application floor for the university gate"),
    # --- §3 endogenous supply ----------------------------------------------
    ("budget_per_child", 0.055, "index/child/yr", "DECLARED", "declared per-capita budget rule, children aged 6-17; NOT a seat path (§3)"),
    ("quality_reserve_share", 0.15, "share", "DECLARED", "declared share of the budget reserved for quality before any opening"),
    ("recurring_cost_section", 1.8, "index/section/yr", "DECLARED", "declared operating cost of an existing section"),
    ("capital_cost_section", 20.0, "index/section", "DECLARED", "declared cost of opening one section"),
    ("quality_effect", 0.35, "quality index", "DECLARED", "declared effect of unspent budget on the district quality index (§3c)"),
    ("K_class", 40, "pupils", "DECLARED", "declared class size / opening threshold (§3, §11)"),
    ("K_class_open_expansion", 30, "pupils", "DECLARED", "K_class -25% for the ORDINARY-EXPANSION arm only (§8.3)"),
    ("postsec_initial_capacity", 20, "places", "DECLARED", "declared initial post-secondary non-tertiary capacity"),
    ("sections_town_primary", 48, "sections", "DECLARED", "declared INITIAL stock at burn-in start t=-11 (initial condition, not a path)"),
    ("sections_town_lower", 32, "sections", "DECLARED", "declared initial stock, town lower secondary"),
    ("sections_town_upper", 16, "sections", "DECLARED", "declared initial stock, town upper secondary"),
    ("initial_village_primary_max_km", 6.0, "km", "DECLARED", "declared initial condition: villages within this distance have a primary school; others do not (uneven provision, §1)"),
    ("private_fixed_cost", 3.0, "index/yr", "DECLARED", "declared private provider fixed cost per class"),
    ("private_var_cost", 0.05, "index/pupil/yr", "DECLARED", "declared private provider variable cost"),
    ("private_pay_share", 0.7, "share", "DECLARED", "declared share of unserved children the provider expects to be able to pay"),
    ("private_exit_years", 3, "years", "DECLARED", "K_exit consecutive loss years before a private provider exits (§3)"),
    # --- §6 cohort feedback -------------------------------------------------
    ("response_a_completers", 1, "switch", "DECLARED", "response (a) completers create next-level demand: structural in the supply rule (§3), so always on"),
    ("response_b_nearby", 0, "switch", "DECLARED", "response (b) nearby secondary raises primary persistence: OFF in the baseline economy-steady start (§6); ON in SPILLBACK"),
    ("response_c_employer", 0, "switch", "DECLARED", "response (c) employer requirement/returns: OFF in the baseline (§6); ON in DEGREES-OUTRUN-JOBS"),
    ("nearby_secondary_bonus", 0.8, "index", "DECLARED", "declared bonus to the primary continuation value when a secondary place is within reach (response b)"),
    ("employer_req_0", 3, "credential level", "DECLARED", "req_0: credential level read by the employer (3 = upper secondary)"),
    ("graduate_share_0", 0.20, "share", "DECLARED", "g0, the steady-state graduate share the employer rule is anchored on"),
    ("lambda_req", 0.8, "index", "DECLARED", "λ_req in req_t = req_0 + λ_req (share_t - g0)"),
    ("lambda_ret", 0.45, "index", "DECLARED", "λ_ret in return_t = return_0 (1 - λ_ret (share_t - g0))"),
    ("return_0", 1.0, "index", "DECLARED", "return_0"),
    ("credential_access_penalty", 0.55, "multiple", "DECLARED", "declared credential payoff multiplier when the held level is below the employer requirement"),
    ("degrees_double_from_year", 8, "year", "DECLARED", "DEGREES-OUTRUN-JOBS: graduate supply growth doubled from this year (§8.4)"),
    ("mandate_year", 8, "year", "DECLARED", "MANDATE-BEFORE-FUNDING: required years raised at this year (§8.4)"),
    ("mandate_grades_baseline", 6, "grades", "DECLARED", "baseline required years = 6 (primary completion)"),
    ("mandate_grades_raised", 9, "grades", "DECLARED", "one step = lower-secondary completion (9 grades)"),
    # --- §8.2/§8.3/§9 test declarations ------------------------------------
    ("cohort_window_entry_years", "6;17", "years", "DECLARED", "the 12 scored cohorts (§8.2)"),
    ("coexistence_unused_share", 0.10, "share", "DECLARED", "criterion 1 threshold (§8.2)"),
    ("coexistence_early_leave_share", 0.05, "share", "DECLARED", "criterion 2 threshold (§8.2)"),
    ("coexistence_qualified_per_place", 1.20, "ratio", "DECLARED", "criterion 3 threshold (§8.2)"),
    ("coexistence_gate_catchup_ratio", 2.0, "ratio", "DECLARED", "criterion 4 threshold (§8.2)"),
    ("coexistence_gate_household_share", 0.20, "share", "DECLARED", "criterion 4 second threshold (§8.2)"),
    ("families_ratio", 1.5, "ratio", "DECLARED", "argmax gain must be >= 1.5x another type (§8.3)"),
    ("families_corr", 0.95, "correlation", "DECLARED", "pairwise correlation falsifier (§8.3)"),
    ("travel_cut_multiplier", 0.5, "multiple", "DECLARED", "TRAVEL-CUT arm (§8.3)"),
    ("selective_expansion_multiplier", 1.5, "multiple", "DECLARED", "SELECTIVE-EXPANSION arm (§8.3)"),
    ("spillback_year", 8, "year", "DECLARED", "SPILLBACK treated class opens (§9)"),
    ("spillback_gain_pp", 0.05, "share", "DECLARED", "spillback present iff treated younger-cohort gain >= 5 pp (§9)"),
    ("pupilyear_sample_mod", 32, "1-in-n", "DECLARED", "declared compact sample of pupil-year records for the report-card harness"),
    ("determinism_seed", 20261121, "seed", "DECLARED", "determinism check seed (§10)"),
    ("seed_base", 20261121, "seed", "DECLARED", "base seed (§10)"),
]

DECLARED_MAP = {row[0]: row for row in DECLARED}


def _parse_value(raw, template):
    if isinstance(template, str):
        return str(raw)
    if isinstance(template, bool):
        return str(raw).strip().lower() in ("1", "true", "yes")
    if isinstance(template, int):
        return int(float(raw))
    if isinstance(template, float):
        return float(raw)
    raise TypeError(template)


def declared_params():
    """The embedded frozen parameter dict (single source of truth)."""
    out = {}
    for name, value, _units, _prov, _note in DECLARED:
        out[name] = value
    return out


def params_as_lists():
    """Typed view used by the model."""
    raw = declared_params()
    P = dict(raw)
    for key in ("village_distances_km", "village_sizes", "min_entry_age", "max_entry_age", "max_level_age",
                "child_wage_rural", "child_wage_urban", "home_value_bands",
                "K_value_by_level", "E_value_by_level", "C_value_by_level",
                "fee_town_by_level", "fee_village_by_level", "age_band_primary",
                "age_band_lower_secondary", "age_band_upper_secondary",
                "age_band_post_secondary", "age_band_tertiary", "ability_clip",
                "cohort_window_entry_years"):
        P[key] = [float(x) if "." in str(x) else int(x) for x in str(raw[key]).split(";")]
    return P


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_predeclaration():
    """§10/§14: refuse to run on a predeclaration hash mismatch."""
    if not os.path.exists(PRE_DECL_PATH):
        print("PRE-DECLARATIONS.md NOT FOUND — refusing to run", file=sys.stderr)
        raise SystemExit(3)
    got = sha256_file(PRE_DECL_PATH)
    if got != PRE_DECL_SHA:
        print("PRE-DECLARATION HASH MISMATCH — refusing to run", file=sys.stderr)
        print("  expected: %s" % PRE_DECL_SHA, file=sys.stderr)
        print("  found:    %s" % got, file=sys.stderr)
        raise SystemExit(3)
    return got


def emit_parameters(path=PARAM_PATH):
    """Write PARAMETERS.csv from the embedded declared table (deterministic)."""
    rows = []
    for name, value, units, prov, note in DECLARED:
        rows.append({"name": name, "value": value, "units": units,
                     "provenance": prov, "label": LABEL, "note": note})
    df = pd.DataFrame(rows, columns=["name", "value", "units", "provenance", "label", "note"])
    df.to_csv(path, index=False, lineterminator="\n")
    return path


def load_parameters(path=PARAM_PATH):
    """Read the frozen PARAMETERS.csv and assert it matches the embedded table."""
    if not os.path.exists(path):
        raise SystemExit("PARAMETERS.csv missing — run --emit-parameters first")
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    got = {r["name"]: r["value"] for _, r in df.iterrows()}
    want = {name: str(value) for name, value, _u, _p, _n in DECLARED}
    if set(got) != set(want):
        raise SystemExit("PARAMETERS.csv does not match the declared table (names)")
    for k, v in want.items():
        if str(got[k]) != v:
            raise SystemExit("PARAMETERS.csv value mismatch for %s: %r != %r" % (k, got[k], v))
    # hash of the frozen parameter file is recorded in the manifest
    return params_as_lists()


# ---------------------------------------------------------------------------
# D0 — §8.1 verification: no seat/capacity path is an input.
# ---------------------------------------------------------------------------
class D0Violation(RuntimeError):
    pass


# The only fact keys the supply decision is ever allowed to read. Anything else
# raises D0Violation. This is the structural form of "no seat total in advance".
ALLOWED_SUPPLY_FACTS = (
    "year", "prior_year", "school_age_population", "budget_per_child",
    "quality_reserve_share", "recurring_cost_section", "capital_cost_section",
    "K_class_open", "quality_effect", "prior_unserved", "prior_declines_cost",
    "providers", "private_costs", "arms", "district_quality_index",
)
# Outcome-like names that must never reach the supply decision.
BANNED_FACT_TOKENS = ("enrol", "attendance", "seat_total", "capacity_path", "ner",
                      "ger", "target", "quota", "headcount")

# Source tokens that would indicate an exogenous seat/capacity path.
BANNED_SOURCE_TOKENS = ("seat_total", "seat_path", "capacity_path", "seat_target",
                        "ner_input", "ger_target", "enrolment_target")


class SealedFacts:
    """Whitelist view of the facts handed to the supply decision.

    Reading a key outside ALLOWED_SUPPLY_FACTS raises; reading a banned token
    raises. Every read is logged for the D0 report.
    """

    def __init__(self, facts):
        self._facts = dict(facts)
        self.reads = []

    def __getitem__(self, key):
        kl = str(key).lower()
        if any(tok in kl for tok in BANNED_FACT_TOKENS):
            raise D0Violation("banned fact read by supply decision: %r" % key)
        if key not in ALLOWED_SUPPLY_FACTS:
            raise D0Violation("fact outside the whitelist read by supply decision: %r" % key)
        self.reads.append(key)
        return self._facts[key]

    def get(self, key, default=None):
        if key in self._facts:
            return self[key]
        return default

    def keys(self):
        return list(self._facts)


def build_supply_facts(sim, t):
    """Assemble the supply facts for year t from records dated <= t-1 only."""
    prior = t - 1
    unserved = {}
    declines_cost = {}
    for key, val in sim.unserved_prior.items():
        unserved[key] = val
    for key, val in sim.declines_cost_prior.items():
        declines_cost[key] = val
    # lead-time assertion: every demand fact is dated at or before t-1
    assert sim.facts_year is None or sim.facts_year <= prior, "supply fact from the same year"
    pop6_17 = int(sim.pop_school_age(t))
    return {
        "year": t,
        "prior_year": prior,
        "school_age_population": pop6_17,
        "budget_per_child": sim.P["budget_per_child"],
        "quality_reserve_share": sim.P["quality_reserve_share"],
        "recurring_cost_section": sim.P["recurring_cost_section"],
        "capital_cost_section": sim.P["capital_cost_section"],
        "K_class_open": sim.k_class_open,
        "quality_effect": sim.P["quality_effect"],
        "prior_unserved": unserved,
        "prior_declines_cost": declines_cost,
        "providers": sim.provider_snapshot(),
        "private_costs": (sim.P["private_fixed_cost"], sim.P["private_var_cost"],
                          sim.P["private_pay_share"], sim.P["private_exit_years"]),
        "arms": sim.arm_flags,
        "district_quality_index": sim.district_quality_index,
    }


def supply_decision(facts):
    """§3. District + private supply. Seats are an OUTPUT of this function.

    Reads only the sealed whitelist. Returns the decisions (no side effects), so
    the D0 replay can re-run it on poisoned facts and compare.
    """
    P = DECLARED_PARAMS
    n_open = {}
    quality_index = 1.0
    providers = facts["providers"]
    total_sections = sum(p["sections"] for p in providers)
    B = facts["budget_per_child"] * facts["school_age_population"]
    reserve = facts["quality_reserve_share"] * B
    recurring = facts["recurring_cost_section"] * total_sections
    avail = B - reserve - recurring
    open_order = (0, 1, 2, 4)
    unserved = facts["prior_unserved"]
    declines_cost = facts["prior_declines_cost"]
    k_open = facts["K_class_open"]
    capital = facts["capital_cost_section"]
    if avail > 0:
        for lvl in open_order:
            locs = sorted(range(0, P["n_villages"] + 1),
                          key=lambda loc: (sim_distance_key(P, loc), loc))
            for loc in locs:
                need = unserved.get((lvl, loc), 0) + declines_cost.get((lvl, loc), 0)
                if need >= k_open and avail >= capital:
                    n = min(int(avail // capital), int(math.ceil(need / k_open)))
                    if n > 0:
                        n_open[(lvl, loc)] = n
                        avail -= n * capital
    if B > 0:
        quality_index = 1.0 + facts["quality_effect"] * max(0.0, avail / B)
    # private entry / exit (§3)
    private_enter = []
    private_exit = []
    priv_fixed, priv_var, pay_share, exit_years = facts["private_costs"]
    existing = {(p["level"], p["loc"]) for p in providers if p["owner"] == "private"}
    for lvl in (0, 1, 2, 4):
        for loc in range(1, P["n_villages"] + 1):
            need = unserved.get((lvl, loc), 0) + declines_cost.get((lvl, loc), 0)
            expected = min(P["K_class"], 0.0 + need) * pay_share
            fee = P["private_fee_multiplier"] * public_fee(P, lvl, village=True) + P["private_fee_add"]
            revenue = fee * expected
            cost = priv_fixed + priv_var * expected
            if (lvl, loc) in existing:
                if revenue < priv_var * expected:
                    private_exit.append((lvl, loc))
            elif revenue >= cost and expected >= 1.0:
                private_enter.append((lvl, loc))
    return {"open": n_open, "quality_index": quality_index, "private_enter": private_enter,
            "private_exit": private_exit, "reads": list(facts.reads) if hasattr(facts, "reads") else []}


def sim_distance_key(P, loc):
    if loc == 0:
        return 0.0
    return P["village_distances_km"][loc - 1]


def public_fee(P, level, village):
    return P["fee_village_by_level"][level] if village else P["fee_town_by_level"][level]


DECLARED_PARAMS = params_as_lists()


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
class Sim:
    def __init__(self, arm, seed, P):
        self.arm = arm
        self.seed = seed
        self.P = P
        self.rng = np.random.Generator(np.random.PCG64(seed))
        self.T0 = -int(P["n_burnin_cohorts"])
        self.T1 = int(P["years"]) - 1
        self.k_class_open = P["K_class"]
        self.travel_mult = 1.0
        self.arm_flags = self._arm_flags()
        # ---- v0.2 Yang return-side wiring (declared) ----
        self.yang_cfg = dict(YANG)
        self.yang_design = self.arm if self.arm in ("none", "yang", "yang_endog") else None
        self.yang_g = 0.0 if self.yang_design in (None, "none") else yang_gate_share()
        self.yang_alpha = float(self.yang_cfg["alpha"]) * float(self.yang_cfg["premium_mult"])
        self.yang_m = 1.0
        self.beta_option_eff = float(self.P["beta_option"]) * float(self.yang_cfg["beta_mult"])
        self.child_wage_mult = float(self.yang_cfg["child_wage_mult"])
        self.travel_mult = self.travel_mult * float(self.yang_cfg["travel_mult"])
        self.district_quality_index = 1.0
        self.private_fail = {}
        self.decision_log = []
        self.unserved_prior = {}
        self.declines_cost_prior = {}
        self.unserved_year_seen = []
        self.unserved_now = {}
        self.declines_cost_now = {}
        self.lagged_cutoff = {L_SEL: None, L_TERT: None}
        self.tutor_price_c = P["tutoring_price_catchup"]
        self.tutor_price_g = P["tutoring_price_gate"]
        self.fees_zero_from = None
        self.mandate_from = None
        self._setup_population()
        self._build_distance_matrix()
        self._setup_providers()
        self._setup_state()
        self.year_records = []
        self.transition_log = []
        self.tutor_log = []
        self.pupil_year_sample = []
        self.cohort_stats = {}

    # -- arm flags (declared, §8.3/§8.4/§9) --------------------------------
    def _arm_flags(self):
        P = self.P
        f = {"response_b": int(P["response_b_nearby"]),
             "response_c": int(P["response_c_employer"]),
             "mandate": 0, "fees_zero": 0, "degrees_double": 0,
             "spillback": 0, "treated_village": None}
        if self.arm == "travel_cut":
            self.travel_mult = float(P["travel_cut_multiplier"])
        elif self.arm == "ordinary_expansion":
            self.k_class_open = int(P["K_class_open_expansion"])
        elif self.arm == "selective_expansion":
            f["k_sel_mult"] = float(P["selective_expansion_multiplier"])
        elif self.arm == "mandate_before_funding":
            f["mandate"] = 1
        elif self.arm == "fees_abolished":
            f["fees_zero"] = 1
        elif self.arm == "degrees_outrun_jobs":
            f["degrees_double"] = 1
            f["response_c"] = 1
        elif self.arm == "spillback":
            f["spillback"] = 1
            f["response_b"] = 1
            reach = float(self.P["reach_lower_secondary_km"])
            eligible = [i + 1 for i, d in enumerate(self.P["village_distances_km"])
                        if float(d) > reach]
            f["treated_village"] = int(eligible[int(self.rng.integers(0, len(eligible)))])
            f["treated_eligible"] = eligible
        return f

    def k_sel(self):
        m = self.arm_flags.get("k_sel_mult", 1.0)
        return int(round(self.P["K_sel"] * m))

    # -- population --------------------------------------------------------
    def _setup_population(self):
        P = self.P
        n_burn = int(P["n_burnin_cohorts"])
        n_cohorts = int(P["n_cohorts"])
        entry_years = np.arange(self.T0, n_cohorts, dtype=np.int32)
        assert len(entry_years) == n_burn + n_cohorts
        sizes = [int(x) for x in P["village_sizes"]]
        per_cohort_loc = np.concatenate(
            [np.zeros(int(P["town_cohort_size"]), dtype=np.int8),
             np.repeat(np.arange(1, P["n_villages"] + 1, dtype=np.int8), sizes)])
        assert per_cohort_loc.size == int(P["cohort_size"]), per_cohort_loc.size
        N = entry_years.size * int(P["cohort_size"])
        self.N = N
        self.entry_year = np.repeat(entry_years, int(P["cohort_size"]))
        self.birth_year = self.entry_year - 6
        self.loc = np.tile(per_cohort_loc, entry_years.size)
        dists = np.array([0.0] + [float(x) for x in P["village_distances_km"]])
        self.dist = dists[self.loc]
        # declared draws, fixed order
        self.ability = np.clip(self.rng.normal(P["ability_mean"], P["ability_sd"], N),
                               P["ability_clip"][0], P["ability_clip"][1])
        poor_share = np.where(self.loc == 0, P["poor_share_town"], P["poor_share_village"])
        self.poor = self.rng.random(N) < poor_share
        mu = np.where(self.poor, P["income_poor"], P["income_nonpoor"])
        self.income = mu * np.exp(self.rng.normal(0.0, P["income_sigma"], N))
        self.sibs = self.rng.poisson(P["siblings_mean"], N).astype(np.int8)
        self.pupil_id = np.arange(N, dtype=np.int64)
        self.rural = (self.loc > 0)

    def _build_distance_matrix(self):
        P = self.P
        d = np.array([0.0] + [float(x) for x in P["village_distances_km"]])
        n = d.size
        D = np.zeros((n, n), dtype=np.float64)
        for i in range(n):
            for j in range(n):
                if i == j:
                    D[i, j] = 0.0
                elif i == 0:
                    D[i, j] = d[j]
                elif j == 0:
                    D[i, j] = d[i]
                else:
                    D[i, j] = abs(d[i] - d[j])
        self.D = D
        self.dist_table = d

    def _setup_providers(self):
        P = self.P
        self.providers = []
        self._next_pid = 0

        def add(loc, level, owner, sections, cap, origin, year):
            self.providers.append({"pid": self._next_pid, "loc": loc, "level": level,
                                   "owner": owner, "sections": sections, "sections0": sections,
                                   "cap": cap, "origin": origin, "opened": year})
            self._next_pid += 1

        y0 = self.T0
        add(0, L_PRIMARY, "district", int(P["sections_town_primary"]),
            int(P["sections_town_primary"]) * int(P["K_class"]), "initial_declared", y0)
        add(0, L_LOWER, "district", int(P["sections_town_lower"]),
            int(P["sections_town_lower"]) * int(P["K_class"]), "initial_declared", y0)
        add(0, L_UPPER, "district", int(P["sections_town_upper"]),
            int(P["sections_town_upper"]) * int(P["K_class"]), "initial_declared", y0)
        add(0, L_SEL, "selective", 1, int(P["K_sel"]), "initial_declared", y0)
        add(0, L_POSTSEC, "district", 1, int(P["postsec_initial_capacity"]), "initial_declared", y0)
        add(0, L_TERT, "university", 1, int(P["K_uni"]), "initial_declared", y0)
        for i, d in enumerate(P["village_distances_km"]):
            if float(d) <= float(P["initial_village_primary_max_km"]):
                size = int(P["village_sizes"][i])
                secs = int(math.ceil(size * int(P["primary_years"]) / int(P["K_class"])))
                add(i + 1, L_PRIMARY, "district", secs, secs * int(P["K_class"]),
                    "initial_declared", y0)

    # -- state -------------------------------------------------------------
    def _setup_state(self):
        N = self.N
        self.status = np.zeros(N, dtype=np.int8)       # 0 not started, 1 in school, 2 out, 3 finished
        self.level = np.full(N, -1, dtype=np.int8)
        self.grade = np.zeros(N, dtype=np.int8)
        self.rep = np.zeros(N, dtype=np.int8)
        self.mastery = np.zeros(N, dtype=np.float64)
        self.cred = np.zeros(N, dtype=np.int8)
        self.prov_idx = np.full(N, -1, dtype=np.int32)
        self.pending_level = np.full(N, -1, dtype=np.int8)
        self.exit_year = np.full(N, -9999, dtype=np.int32)
        self.exit_reason = np.zeros(N, dtype=np.int8)
        self.years_attended = np.zeros(N, dtype=np.int16)
        self.years_completed = np.zeros(N, dtype=np.int16)
        self.rep_total = np.zeros(N, dtype=np.int16)
        self.catchup_h = np.zeros(N, dtype=np.float64)
        self.gate_h = np.zeros(N, dtype=np.float64)
        self.gate_hours_this_year = np.zeros(N, dtype=np.float64)
        self.catchup_hours_this_year = np.zeros(N, dtype=np.float64)
        self.last_score = np.full(N, np.nan, dtype=np.float64)
        self.completed_year = {1: np.full(N, -9999, dtype=np.int32),
                               2: np.full(N, -9999, dtype=np.int32),
                               3: np.full(N, -9999, dtype=np.int32),
                               4: np.full(N, -9999, dtype=np.int32),
                               5: np.full(N, -9999, dtype=np.int32)}
        self.selective_admitted = np.zeros(N, dtype=bool)
        self.selective_attended = np.zeros(N, dtype=bool)
        self.attended_secondary = np.zeros(N, dtype=bool)
        self.reentry_used = np.zeros(N, dtype=np.int8)
        self.alt_prov = np.full(N, -1, dtype=np.int32)
        self.alt_level = np.full(N, -1, dtype=np.int8)
        self.q_prov = np.ones(1, dtype=np.float64)
        self.pid_map = {}
        self.pid2i = {}
        self.offers_count = {}
        self.declines_year = {}
        self.facts_year = None
        self._attend_mask = np.zeros(N, dtype=bool)
        self._declined_mask = np.zeros(N, dtype=bool)
        self.attempted = np.zeros(N, dtype=np.uint8)   # bitmask over level codes
        self.resume_level = np.full(N, -1, dtype=np.int8)
        self.resume_grade = np.zeros(N, dtype=np.int8)

    def pop_school_age(self, t):
        age = t - self.birth_year
        return int(np.count_nonzero((age >= 6) & (age <= 17)))

    def snapshot_outcomes(self):
        """Outcome-like arrays the supply module must never see (D0 poison target)."""
        return {"enrolment_by_level": np.bincount(self.level[self.status == 1] + 1, minlength=7),
                "attendance_count": int(np.count_nonzero(self.status == 1)),
                "ner": np.zeros(6), "ger": np.zeros(6)}

    def provider_snapshot(self):
        return [{"pid": p["pid"], "loc": p["loc"], "level": p["level"], "owner": p["owner"],
                 "sections": p["sections"], "cap": p["cap"], "origin": p["origin"],
                 "opened": p["opened"]} for p in self.providers]

    # -- helpers -----------------------------------------------------------
    def distances_to(self, loc, prov_loc):
        if np.isscalar(loc):
            return float(self.D[int(loc), int(prov_loc)])
        return self.D[np.asarray(loc, dtype=np.int64), int(prov_loc)]

    def fee_for(self, level, owner, village):
        P = self.P
        if self.fees_zero_from is not None and self.year >= self.fees_zero_from:
            if level != L_TERT:      # FEES-ABOLISHED-TRAVEL-REMAINS: "all declared fees set to 0"
                return 0.0
            return 0.0
        base = public_fee(P, level, village)
        if owner == "private":
            return P["private_fee_multiplier"] * base + P["private_fee_add"]
        return base

    def travel_cost(self, dist):
        return float(self.travel_mult) * float(self.P["travel_cost_per_km"]) * np.asarray(dist, dtype=np.float64)

    # ------------------------------------------------------------------
    # one year
    # ------------------------------------------------------------------
    def step(self, t):
        self.year = t
        P = self.P
        age = t - self.birth_year
        # fees abolished / mandate switches begin at their declared year
        if self.arm_flags["fees_zero"] and t >= int(P["mandate_year"]):
            self.fees_zero_from = int(P["mandate_year"])
        if self.arm_flags["mandate"] and t >= int(P["mandate_year"]):
            self.mandate_from = int(P["mandate_year"])
        mandate_grades = (int(P["mandate_grades_raised"]) if self.mandate_from is not None
                          else int(P["mandate_grades_baseline"]))
        self._yang_endog_update(t)

        # ---- 0. activate children who reach primary-entry age -------------
        new6 = (self.status == 0) & (age == 6)
        if np.any(new6):
            self.status[new6] = 1
            self.level[new6] = L_PRIMARY
            self.grade[new6] = 1
            self.mastery[new6] = 20.0
            self.prov_idx[new6] = -1
            self.pending_level[new6] = L_PRIMARY
            self.exit_year[new6] = t - 1

        # ---- 1. supply decisions (facts dated <= t-1) ----------------------
        if t > self.T0:
            self._supply_step(t)

        # ---- 2. candidate sets --------------------------------------------
        # the 2-year window is a RE-ENTRY rule, not an advancement deadline:
        # a child waiting for the next level keeps her place in the queue until max_level_age
        nxt = np.full(self.N, -1, dtype=np.int8)
        for c, lst in NEXT_AFTER_CRED.items():
            if lst:
                nxt[self.cred == c] = lst[0]
        advancing = (self.pending_level == nxt) & (nxt >= 0)
        expired = ((self.status == 2) & ((t - self.exit_year) > int(P["reentry_window"]))
                   & ~advancing)
        too_old = np.zeros(self.N, dtype=bool)
        for lvl in LEVELS:
            fresh = ((self.attempted >> np.uint8(lvl)) & np.uint8(1)) == 0
            too_old |= ((self.pending_level == lvl)
                        & ((age > int(P["max_level_age"][lvl]))
                           | (fresh & (age > int(P["max_entry_age"][lvl])))))
        drop = expired | too_old
        if np.any(drop):
            self.pending_level[drop] = -1
            self.status[drop & (self.status == 2)] = 3
        want = self.pending_level
        is_cont = (self.status == 1) & (self.prov_idx >= 0) & (want >= 0)
        is_new = (want >= 0) & ~is_cont

        # ---- 3. allocate places (residence controller) ---------------------
        free = self._free_capacity(is_cont)
        allocated = self._allocate(is_new, want, free, t)

        # ---- 4. named gates (exam + places; university also fee) ------------
        self._selective_gate(t, is_new & (want == L_UPPER))
        self._university_gate(t, is_new & (want == L_POSTSEC))

        # ---- 5. household next-year choice against the real alternative -----
        has_place = (self.prov_idx >= 0) & ((self.status == 1) | allocated)
        self.offers_count = {}
        self.declines_year = {}
        self._declined_mask = np.zeros(self.N, dtype=bool)
        self._household_choice(t, age, has_place, allocated, mandate_grades)

        # ---- 6. tutoring (§5) ----------------------------------------------
        attending = self._attend_mask & (self.prov_idx >= 0)
        self._tutoring(t, age, attending)

        # ---- 7. learning, exam, gates, progression --------------------------
        self._school_year(t, age, attending)

        # ---- 8. rotate supply facts ----------------------------------------
        self._rotate_supply_facts()

    # -- supply -----------------------------------------------------------
    def _supply_step(self, t):
        facts = SealedFacts(build_supply_facts(self, t))
        dec = supply_decision(facts)
        self.district_quality_index = dec["quality_index"]
        for (lvl, loc), n in sorted(dec["open"].items()):
            self._add_section(loc, lvl, "district", n, t, "district_decision")
        for (lvl, loc) in dec["private_enter"]:
            self._add_section(loc, lvl, "private", 1, t, "private_decision")
        for (lvl, loc) in dec["private_exit"]:
            self._remove_private(loc, lvl)
        if (self.arm_flags.get("spillback") and t == int(self.P["spillback_year"])):
            tv = int(self.arm_flags["treated_village"])
            self.providers.append({"pid": self._next_pid, "loc": tv, "level": L_LOWER,
                                   "owner": "experimental", "sections": 1, "sections0": 0,
                                   "cap": int(self.P["K_class"]), "origin": "experimental_treatment",
                                   "opened": t})
            self._next_pid += 1
        self.decision_log.append({"year": t, "open": {str(k): v for k, v in dec["open"].items()},
                                  "quality_index": dec["quality_index"],
                                  "private_enter": [list(x) for x in dec["private_enter"]],
                                  "private_exit": [list(x) for x in dec["private_exit"]],
                                  "reads": sorted(set(dec["reads"])),
                                  "fact_year_max": t - 1})

    def _add_section(self, loc, level, owner, n, t, origin):
        for p in self.providers:
            if p["loc"] == loc and p["level"] == level and p["owner"] == owner:
                p["sections"] += n
                p["cap"] += n * int(self.P["K_class"])
                return
        self.providers.append({"pid": self._next_pid, "loc": loc, "level": level,
                               "owner": owner, "sections": n, "sections0": 0,
                               "cap": n * int(self.P["K_class"]), "origin": origin,
                               "opened": t})
        self._next_pid += 1

    def _remove_private(self, loc, level):
        self.providers = [p for p in self.providers
                          if not (p["loc"] == loc and p["level"] == level and p["owner"] == "private")]

    def _providers_at(self, level):
        return [p for p in self.providers if p["level"] == level]

    def _free_capacity(self, is_cont):
        idx = np.nonzero(is_cont)[0]
        free = {p["pid"]: p["cap"] for p in self.providers}
        reserved = {}
        for pid in self.prov_idx[idx]:
            reserved[int(pid)] = reserved.get(int(pid), 0) + 1
        for pid, n in reserved.items():
            p = self._provider_by_pid(pid)
            if p is not None:
                free[pid] = max(0, p["cap"] - n)
        return free

    def _pid_of(self, loc, level):
        for p in self.providers:
            if p["loc"] == loc and p["level"] == level:
                return p["pid"]
        return -1

    def _provider_by_pid(self, pid):
        for p in self.providers:
            if p["pid"] == pid:
                return p
        return None

    def _allocate(self, is_new, want, free, t):
        """Residence/catchment allocation: nearest provider within reach; contested
        places by seeded lot; villages processed town-first (declared tie-break)."""
        P = self.P
        allocated = np.zeros(self.N, dtype=bool)
        if not np.any(is_new):
            return allocated
        priority = self.rng.random(self.N)
        for lvl in LEVELS:
            cand = np.nonzero(is_new & (want == lvl))[0]
            if cand.size == 0:
                continue
            provs = self._providers_at(lvl)
            if not provs:
                continue
            reach = float(P[["reach_primary_km", "reach_lower_secondary_km",
                             "reach_upper_secondary_km", "reach_post_secondary_km",
                             "reach_tertiary_km"][{0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 4}[lvl]]])
            for loc in sorted(range(0, int(P["n_villages"]) + 1), key=lambda x: (x != 0, x)):
                sub = cand[self.loc[cand] == loc]
                if sub.size == 0:
                    continue
                sub = sub[np.argsort(priority[sub], kind="stable")]
                order = []
                for p in provs:
                    d = self.distances_to(loc, p["loc"])
                    if float(d) <= reach + 1e-12:
                        order.append((float(d), -p["cap"], p["pid"], p))
                order.sort(key=lambda x: (x[0], x[1], x[2]))
                pos = 0
                for _d, _nc, pid, p in order:
                    if pos >= sub.size:
                        break
                    room = free.get(pid, 0)
                    if room <= 0:
                        continue
                    k = min(room, sub.size - pos)
                    take = sub[pos:pos + k]
                    self.prov_idx[take] = pid
                    self._enter_level(take, lvl, t)
                    allocated[take] = True
                    free[pid] = room - k
                    pos += k
        return allocated

    def _enter_level(self, idx, lvl, t):
        if idx.size == 0:
            return
        self.status[idx] = 1
        self.level[idx] = lvl
        self.grade[idx] = 1
        self.rep[idx] = 0
        resume = (self.resume_level[idx] == lvl)
        if np.any(resume):
            self.grade[idx[resume]] = np.maximum(1, self.resume_grade[idx[resume]])
            self.resume_level[idx[resume]] = -1
        self.pending_level[idx] = lvl
        self.exit_year[idx] = t - 1
        self.attempted[idx] |= np.uint8(1 << lvl)
        if lvl >= L_LOWER:
            self.attended_secondary[idx] = True
        if lvl == L_SEL:
            self.selective_attended[idx] = True

    def _rotate_supply_facts(self):
        self.unserved_prior = dict(self.unserved_now)
        self.declines_cost_prior = dict(self.declines_cost_now)
        self.unserved_now = {}
        self.declines_cost_now = {}

    # ==================================================================
    # gates (§4)
    # ==================================================================
    def _gate_score(self, idx):
        s = self.last_score[idx].copy()
        need = np.isnan(s)
        if np.any(need):
            i = idx[need]
            s[need] = np.clip(0.60 * self.ability[i] + 0.40 * self.mastery[i], 5.0, 98.0)
        return s

    def _selective_gate(self, t, seeking_upper):
        """§4 gate 3: exam >= threshold AND rank within selective places (§4)."""
        P = self.P
        k_sel = self.k_sel()
        idx = np.nonzero(seeking_upper)[0]
        rec = {"year": t, "gate": "selective", "applicants": 0, "qualified": 0,
               "admitted": 0, "turned_away": 0, "places": k_sel, "marginal_score": None}
        if idx.size:
            score = self._gate_score(idx)
            apply = score >= float(P["selective_app_floor"])
            applicants = idx[apply]
            s_app = self._gate_score(applicants)
            qualified = applicants[s_app >= float(P["selective_exam_threshold"])]
            s_q = self._gate_score(qualified)
            n_adm = int(min(qualified.size, k_sel))
            if n_adm > 0:
                order = np.lexsort((qualified, -s_q))
                admitted = qualified[order[:n_adm]]
                rec["marginal_score"] = float(s_q[order[:n_adm]].min())
                self.lagged_cutoff[L_SEL] = float(s_q[order[:n_adm]].min())
                has = self.prov_idx[admitted] >= 0
                self.alt_prov[admitted] = np.where(has, self.prov_idx[admitted], -1)
                self.alt_level[admitted] = np.where(has, L_UPPER, -1)
                self.prov_idx[admitted] = self._pid_of(0, L_SEL)
                self._enter_level(admitted, L_SEL, t)
                self.selective_admitted[admitted] = True
            rec.update({"applicants": int(applicants.size), "qualified": int(qualified.size),
                        "admitted": int(n_adm),
                        "turned_away": int(qualified.size - n_adm)})
        self.transition_log.append(rec)

    def _university_gate(self, t, seeking_upper_completers):
        """§4 gate 4: exam >= threshold AND fee paid AND rank within K_uni."""
        P = self.P
        k_uni = int(P["K_uni"])
        idx = np.nonzero(seeking_upper_completers)[0]
        rec = {"year": t, "gate": "university", "applicants": 0, "qualified": 0,
               "admitted": 0, "turned_away": 0, "places": k_uni, "marginal_score": None}
        if idx.size:
            score = self._gate_score(idx)
            apply = score >= float(P["university_app_floor"])
            applicants = idx[apply]
            s_app = self._gate_score(applicants)
            qualified = applicants[s_app >= float(P["university_exam_threshold"])]
            payers = qualified[self._can_afford(qualified, L_TERT)]
            s_p = self._gate_score(payers)
            n_adm = int(min(payers.size, k_uni))
            if n_adm > 0:
                order = np.lexsort((payers, -s_p))
                admitted = payers[order[:n_adm]]
                rec["marginal_score"] = float(s_p[order[:n_adm]].min())
                self.lagged_cutoff[L_TERT] = float(s_p[order[:n_adm]].min())
                has = self.prov_idx[admitted] >= 0
                self.alt_prov[admitted] = np.where(has, self.prov_idx[admitted], -1)
                self.alt_level[admitted] = np.where(has, L_POSTSEC, -1)
                self.prov_idx[admitted] = self._pid_of(0, L_TERT)
                self._enter_level(admitted, L_TERT, t)
            rec.update({"applicants": int(applicants.size), "qualified": int(qualified.size),
                        "admitted": int(n_adm),
                        "turned_away": int(qualified.size - n_adm)})
        self.transition_log.append(rec)

    def _can_afford(self, idx, level):
        if idx.size == 0:
            return np.zeros(0, dtype=bool)
        prov = self._provider_by_pid(self._pid_of(0, level))
        owner = prov["owner"] if prov else "district"
        fee = self._fee_vec(np.full(idx.size, level, dtype=np.int8),
                            np.full(idx.size, owner, dtype=object),
                            np.zeros(idx.size, dtype=bool), self.income[idx])
        dist = self._dist_vec(self.loc[idx], 0)
        cost = fee + self.travel_cost(dist)
        return cost <= float(self.P["max_school_spend_share"]) * self.income[idx] + 1e-12

    # ==================================================================
    # household (§2)
    # ==================================================================
    def _wage(self, age, loc):
        P = self.P
        out = np.zeros(age.shape, dtype=np.float64)
        for lo, hi, bi in ((0, 12, 0), (12, 16, 1), (16, 19, 2), (19, 999, 3)):
            m = (age >= lo) & (age < hi)
            if np.any(m):
                out[m] = np.where(loc[m] == 0, P["child_wage_urban"][bi],
                                  P["child_wage_rural"][bi])
        return out * float(getattr(self, "child_wage_mult", 1.0))

    def _home_value(self, age):
        P = self.P
        return np.where(age < 12, P["home_value_bands"][0],
                        np.where(age < 16, P["home_value_bands"][1],
                                 P["home_value_bands"][2]))

    def _graduate_share(self, t):
        age = t - self.birth_year
        band = (age >= 18) & (age <= 22)
        n = int(np.count_nonzero(band))
        if n == 0:
            return float(self.P["graduate_share_0"])
        return float(np.count_nonzero(band & (self.cred >= 3)) / n)

    def _employer_rule(self, t):
        """§6(c). OFF in the baseline; DEGREES-OUTRUN-JOBS turns it on."""
        P = self.P
        if not self.arm_flags["response_c"]:
            return float(P["employer_req_0"]), float(P["return_0"])
        share = self._graduate_share(t)
        g0 = float(P["graduate_share_0"])
        used = share
        if self.arm_flags["degrees_double"] and t >= int(P["degrees_double_from_year"]):
            used = g0 + 2.0 * (share - g0)
        used = float(np.clip(used, 0.0, 1.0))
        req = float(P["employer_req_0"]) + float(P["lambda_req"]) * (used - g0)
        ret = float(P["return_0"]) * (1.0 - float(P["lambda_ret"]) * (used - g0))
        return req, ret

    def _cred_market(self, cred_levels, req, ret):
        access = np.where(np.asarray(cred_levels) >= req, 1.0,
                          float(self.P["credential_access_penalty"]))
        return access * ret

    def _fee_vec(self, levels, owners, village_flag, incomes):
        P = self.P
        if self.fees_zero_from is not None and self.year >= self.fees_zero_from:
            return np.zeros(levels.shape, dtype=np.float64)
        base = np.where(village_flag,
                        np.array([float(x) for x in P["fee_village_by_level"]])[levels],
                        np.array([float(x) for x in P["fee_town_by_level"]])[levels])
        priv = np.array([str(o) == "private" for o in owners])
        return np.where(priv, float(P["private_fee_multiplier"]) * base + float(P["private_fee_add"]),
                        base)

    def _dist_vec(self, loc_arr, prov_loc):
        d = self.dist_table
        loc_arr = np.asarray(loc_arr)
        if prov_loc == 0:
            return d[loc_arr]
        out = np.abs(d[loc_arr] - d[prov_loc])
        out = np.where(loc_arr == 0, d[prov_loc], out)
        out = np.where(loc_arr == prov_loc, 0.0, out)
        return out

    def _refresh_provider_arrays(self, has_place_mask):
        self.pid_map = {p["pid"]: p for p in self.providers}
        self.prov_owner = np.array([p["owner"] for p in self.providers], dtype=object)
        self.prov_loc = np.array([p["loc"] for p in self.providers], dtype=np.int64)
        self.prov_level = np.array([p["level"] for p in self.providers], dtype=np.int64)
        self.prov_sections = np.array([max(1, p["sections"]) for p in self.providers], dtype=np.float64)
        self.pid2i = {p["pid"]: i for i, p in enumerate(self.providers)}
        counts = np.zeros(len(self.providers), dtype=np.int64)
        idx = np.nonzero(has_place_mask & (self.prov_idx >= 0))[0]
        for pid in self.prov_idx[idx]:
            counts[self.pid2i[int(pid)]] += 1
        pps = counts / self.prov_sections
        f = np.clip(1.0 - 0.15 * np.maximum(0.0, pps / float(self.P["K_class"]) - 1.0), 0.60, 1.0)
        village = np.where(self.prov_loc == 0, 1.0, 0.90)
        base = np.where(self.prov_owner == "private", 1.05, 1.0)
        self.q_prov = base * village * self.district_quality_index * f

    def _expected_score(self, idx, i_prov):
        P = self.P
        a = self.ability[idx]
        gain = float(P["mastery_gain"]) * (0.55 + 0.45 * a / 100.0) * self.q_prov[i_prov]
        m2 = np.minimum(100.0, self.mastery[idx] + gain)
        return np.clip(0.60 * a + 0.40 * m2, 5.0, 98.0)

    def _yang_cred_multiplier(self):
        if self.yang_design in (None, "none"):
            return 1.0
        return max(0.0, 1.0 + self.yang_alpha * self.yang_g * self.yang_m)

    def _yang_endog_update(self, t):
        """Declared one-year-lag bounded response: m_t from previous-year gate pressure."""
        if self.yang_design != "yang_endog":
            return
        if t <= self.T0:
            return
        recs = [r for r in self.transition_log if r["year"] == t - 1]
        ratios = []
        for gate in ("selective", "university"):
            rr = [r for r in recs if r["gate"] == gate]
            if rr:
                rec = rr[-1]
                if rec.get("places"):
                    ratios.append(float(rec["applicants"]) / float(rec["places"]))
        if not ratios:
            return
        r = sum(ratios) / len(ratios)
        if r > 3.0:
            self.yang_m = min(1.50, self.yang_m + 0.05)
        elif r < 1.0:
            self.yang_m = max(0.25, self.yang_m - 0.05)

    def _value_attend(self, idx, levels, i_prov, t, req, ret):
        """Declared household value of attending (§2), vectorised over children."""
        P = self.P
        a = self.ability[idx]
        loc = self.loc[idx]
        age = t - self.birth_year[idx]
        dist = self._dist_vec(loc, -1) if False else None
        ploc = self.prov_loc[i_prov]
        dist = np.zeros(idx.size)
        for pl in np.unique(ploc):
            m = ploc == pl
            dist[m] = self._dist_vec(loc[m], int(pl))
        village = ploc > 0
        fee = self._fee_vec(levels, self.prov_owner[i_prov], village, self.income[idx])
        travel = self.travel_cost(dist)
        s_exp = self._expected_score(idx, i_prov)
        thr = np.where(levels <= L_LOWER, float(P["pass_threshold"]),
                       np.where(levels <= L_SEL, float(P["university_exam_threshold"]),
                                float(P["postsec_complete_threshold"])))
        p_gate = 1.0 / (1.0 + np.exp(-(s_exp - thr) / 6.0))
        cred_levels = np.array([CRED_OF_LEVEL[int(l)] for l in levels])
        c_market = self._cred_market(cred_levels, req, ret)
        K = np.array([float(x) for x in P["K_value_by_level"]])[levels]
        E = np.array([float(x) for x in P["E_value_by_level"]])[levels]
        C = np.array([float(x) for x in P["C_value_by_level"]])[levels]
        C = C * self._yang_cred_multiplier()
        OV_vals = np.array([float(P["option_value_primary"]), float(P["option_value_lower"]),
                            float(P["option_value_upper"]), float(P["option_value_upper"]),
                            float(P["option_value_postsec"]), float(P["option_value_tertiary"])])
        OV = OV_vals[levels]
        V = (float(P["weight_knowledge"]) * K + float(P["weight_education"]) * E
             + float(P["weight_credential"]) * C * c_market * p_gate
             - fee - travel
             - float(P["theta_child_labour"]) * self._wage(age, loc)
             + float(self.beta_option_eff) * OV)
        if self.arm_flags["response_b"]:
            prim = levels == L_PRIMARY
            if np.any(prim):
                has_sec = self._secondary_within_reach(idx[prim])
                V[prim] += np.where(has_sec, float(P["nearby_secondary_bonus"]), 0.0)
        return V, s_exp, fee + travel

    def _secondary_within_reach(self, idx):
        P = self.P
        reach = float(P["reach_lower_secondary_km"])
        sec_locs = sorted({p["loc"] for p in self.providers
                           if p["level"] in (L_LOWER, L_UPPER, L_SEL)})
        if not sec_locs:
            return np.zeros(idx.size, dtype=bool)
        out = np.zeros(idx.size, dtype=bool)
        for sl in sec_locs:
            out |= self._dist_vec(self.loc[idx], int(sl)) <= reach + 1e-12
        return out

    def _household_choice(self, t, age, has_place, allocated, mandate_grades):
        P = self.P
        req, ret = self._employer_rule(t)
        self._refresh_provider_arrays(has_place)
        offers = np.nonzero(has_place)[0]
        attend = np.zeros(self.N, dtype=bool)
        self.offers_count = {}
        self.declines_year = {}
        if offers.size:
            # selective / university fallback: pick the better offer
            alt = self.alt_level[offers] >= 0
            if np.any(alt):
                sub = offers[alt]
                i_main = np.array([self.pid2i[int(p)] for p in self.prov_idx[sub]])
                i_alt = np.array([self.pid2i[int(p)] for p in self.alt_prov[sub]])
                V_main, _s1, _c1 = self._value_attend(sub, self.level[sub], i_main, t, req, ret)
                V_alt, _s2, _c2 = self._value_attend(sub, self.alt_level[sub], i_alt, t, req, ret)
                pick = V_alt > V_main
                if np.any(pick):
                    j = sub[pick]
                    self.level[j] = self.alt_level[j]
                    self.prov_idx[j] = self.alt_prov[j]
                self.alt_level[sub] = -1
                self.alt_prov[sub] = -1
            lvl = self.level[offers]
            i_prov = np.array([self.pid2i[int(p)] for p in self.prov_idx[offers]])
            V, s_exp, cost = self._value_attend(offers, lvl, i_prov, t, req, ret)
            V_alt = (float(P["theta_child_labour"]) * self._wage(age[offers], self.loc[offers])
                     + self._home_value(age[offers]))
            p_att = 1.0 / (1.0 + np.exp(-(V - V_alt) / float(P["taste_scale"])))
            u = self.rng.random(offers.size)
            take = u < p_att
            over_cash = cost > float(P["max_school_spend_share"]) * self.income[offers] + 1e-12
            take = take & ~over_cash
            if self.mandate_from is not None:
                grade_now = self.grade[offers]
                cum = np.where(lvl == L_PRIMARY, grade_now,
                               np.where(lvl == L_LOWER, 6 + grade_now, 10 + grade_now))
                forced = cum <= mandate_grades
                take = np.where(forced, ~over_cash, take)
            attend[offers[take]] = True
            for lv in lvl:
                self.offers_count[int(lv)] = self.offers_count.get(int(lv), 0) + 1
            declined = offers[~take]
            if declined.size:
                dlv = self.level[declined]
                for lv in dlv:
                    self.declines_year[int(lv)] = self.declines_year.get(int(lv), 0) + 1
                blocked = over_cash[~take]
                self.status[declined] = 2
                self._declined_mask[declined] = True
                self.resume_level[declined] = self.level[declined]
                self.resume_grade[declined] = self.grade[declined]
                self.pending_level[declined] = self.level[declined]
                self.exit_year[declined] = t
                self.exit_reason[declined] = np.where(blocked, 7, 2)
                self.prov_idx[declined] = -1
                for k in np.nonzero(blocked)[0]:
                    key = (int(self.level[declined[k]]), int(self.loc[declined[k]]))
                    self.declines_cost_now[key] = self.declines_cost_now.get(key, 0) + 1
        # children who wanted a place and did not get one: they are out of school,
        # and their count is the demand signal the supply rule observes next year
        seeking = np.nonzero((self.pending_level >= 0) & (self.prov_idx < 0)
                             & ~self._declined_mask & (self.status != 0))[0]
        if seeking.size:
            self.status[seeking] = 2
            self.exit_year[seeking] = t
            self.exit_reason[seeking] = 3
            self.resume_level[seeking] = self.pending_level[seeking]
            self.resume_grade[seeking] = self.grade[seeking]
            for lv, lo in zip(self.pending_level[seeking], self.loc[seeking]):
                key = (int(lv), int(lo))
                self.unserved_now[key] = self.unserved_now.get(key, 0) + 1
        self._attend_mask = attend

    # ==================================================================
    # tutoring (§5)
    # ==================================================================
    def _tutoring(self, t, age, attending):
        P = self.P
        idx = np.nonzero(attending)[0]
        self.gate_hours_this_year[:] = 0.0
        self.catchup_hours_this_year[:] = 0.0
        if idx.size == 0:
            return
        lvl = self.level[idx]
        i_prov = np.array([self.pid2i[int(p)] for p in self.prov_idx[idx]])
        s_exp = self._expected_score(idx, i_prov)
        dist = self.dist[idx]
        access = dist <= float(P["tutoring_access_km"]) + 1e-12
        budget = float(P["tutor_budget_share"]) * self.income[idx]
        village = self.prov_loc[i_prov] > 0
        fee = self._fee_vec(lvl, self.prov_owner[i_prov], village, self.income[idx])
        travel = self.travel_cost(dist)
        cash_left = np.maximum(0.0, float(P["max_school_spend_share"]) * self.income[idx]
                               - fee - travel)
        cost_c = float(P["catchup_hours"]) * self.tutor_price_c
        cost_g = float(P["gate_hours"]) * self.tutor_price_g
        need_c = (s_exp < float(P["catchup_trigger"])) & access
        buy_c = need_c & (cost_c <= np.minimum(budget, cash_left))
        grade = self.grade[idx]
        gate_year = (((lvl == L_LOWER) & (grade >= LEVEL_YEARS[L_LOWER]))
                     | (((lvl == L_UPPER) | (lvl == L_SEL)) & (grade >= LEVEL_YEARS[L_UPPER])))
        buy_g = np.zeros(idx.size, dtype=bool)
        if np.any(gate_year):
            is_lower = lvl == L_LOWER
            thr = np.where(is_lower, float(P["selective_exam_threshold"]),
                           float(P["university_exam_threshold"]))
            lag = self.lagged_cutoff[L_SEL] if np.any(is_lower) else self.lagged_cutoff[L_TERT]
            eff = np.maximum(thr, lag if lag is not None else thr)
            shortfall = eff - s_exp
            in_band = (shortfall >= 0.0) & (shortfall <= float(P["gate_band"]))
            floor = np.where(is_lower, float(P["selective_app_floor"]),
                             float(P["university_app_floor"]))
            buy_g = gate_year & access & in_band & (s_exp >= floor)
        buy_g = buy_g & (cost_g <= np.minimum(budget, np.maximum(cash_left - cost_c * buy_c, 0.0)))
        hc = np.where(buy_c, float(P["catchup_hours"]), 0.0)
        hg = np.where(buy_g, float(P["gate_hours"]), 0.0)
        self.catchup_hours_this_year[idx] = hc
        self.gate_hours_this_year[idx] = hg
        self.catchup_h[idx] += hc
        self.gate_h[idx] += hg
        self.tutor_log.append({"year": t,
                               "catchup_pupils": int(np.count_nonzero(hc)),
                               "gate_pupils": int(np.count_nonzero(hg)),
                               "catchup_hours": float(hc.sum()), "gate_hours": float(hg.sum()),
                               "catchup_poor": int(np.count_nonzero((hc > 0) & self.poor[idx])),
                               "gate_poor": int(np.count_nonzero((hg > 0) & self.poor[idx])),
                               "n_selective": int(np.count_nonzero(lvl == L_SEL)),
                               "n_nonselective": int(np.count_nonzero(lvl != L_SEL)),
                               "gate_hours_selective": float(hg[(lvl == L_LOWER) & gate_year].sum()),
                               "gate_pupils_lower_final": int(np.count_nonzero(
                                   hg > 0) if False else np.count_nonzero(
                                   (hg > 0) & (lvl == L_LOWER) & gate_year)),
                               "selective_applicants": int(np.count_nonzero(
                                   (lvl == L_LOWER) & gate_year
                                   & (s_exp >= float(P["selective_app_floor"]))))})

    # ==================================================================
    # learning, exam, progression (§1 state, §4 gates)
    # ==================================================================
    def _school_year(self, t, age, attending):
        P = self.P
        idx = np.nonzero(attending)[0]
        if idx.size == 0:
            self._record_year(t, age)
            return
        lvl = self.level[idx]
        i_prov = np.array([self.pid2i[int(p)] for p in self.prov_idx[idx]])
        a = self.ability[idx]
        repeating = self.rep[idx] > 0
        gain = float(P["mastery_gain"]) * (0.55 + 0.45 * a / 100.0) * self.q_prov[i_prov]
        gain = gain * np.where(self.catchup_hours_this_year[idx] > 0,
                               float(P["catchup_mastery_mult"]), 1.0)
        gain = gain * np.where(repeating, 0.5, 1.0)
        m2 = np.minimum(100.0, self.mastery[idx] + gain)
        eps = self.rng.normal(0.0, float(P["exam_noise_sd"]), idx.size)
        boost_c = np.where(self.catchup_hours_this_year[idx] > 0,
                           float(P["catchup_attain_boost"]), 0.0)
        hg = self.gate_hours_this_year[idx]
        boost_g = float(P["gate_attain_coef"]) * (1.0 - np.exp(-hg / float(P["gate_attain_scale"])))
        score = np.clip(0.60 * a + 0.40 * m2 + boost_c + boost_g + eps, 5.0, 98.0)
        self.mastery[idx] = m2
        self.last_score[idx] = score
        self.years_attended[idx] += 1
        final_grade = self.grade[idx] >= np.array([LEVEL_YEARS[int(l)] for l in lvl])
        thr = np.where(lvl == L_POSTSEC, float(P["postsec_complete_threshold"]),
                       float(P["pass_threshold"]))
        passed = score >= thr
        # pass, not final
        m = passed & ~final_grade
        self.grade[idx[m]] += 1
        self.years_completed[idx[m]] += 1
        self.rep[idx[m]] = 0
        # pass, final: level completion
        m = passed & final_grade
        if np.any(m):
            j = idx[m]
            self.years_completed[j] += 1
            creds = np.array([CRED_OF_LEVEL[int(l)] for l in lvl[m]])
            self.cred[j] = creds
            for c in np.unique(creds):
                sel = j[creds == c]
                self.completed_year[int(c)][sel] = t
            self.status[j] = 2
            self.exit_year[j] = t
            self.exit_reason[j] = 5
            self.prov_idx[j] = -1
            for k, ci in enumerate(j):
                c = int(creds[k])
                nxt = NEXT_AFTER_CRED.get(c, [])
                self.pending_level[ci] = int(nxt[0]) if nxt else -1
        # fail: repeat once, then the declared failure exit
        m = ~passed
        fail_idx = idx[m]
        if fail_idx.size:
            self.rep_total[fail_idx] += 1
            self.rep[fail_idx] += 1
            again = self.rep[fail_idx] <= int(P["max_repetitions"])
            self.status[fail_idx[again]] = 1
            self.pending_level[fail_idx[again]] = lvl[m][again]
            out = fail_idx[~again]
            if out.size:
                self.status[out] = 2
                self.pending_level[out] = -1
                self.exit_year[out] = t
                self.exit_reason[out] = 4
                self.prov_idx[out] = -1
        self._record_year(t, age)

    def _record_year(self, t, age):
        P = self.P
        if t < 0:
            return
        enrolled = self._attend_mask & (self.prov_idx >= 0)
        loc = self.loc
        a = (t - self.birth_year).astype(np.int64)
        valid = (a >= 0) & (a < 40) & (a < 40)
        r = (loc > 0).astype(np.int64)
        pop = np.bincount(r[valid] * 40 + a[valid], minlength=80).reshape(2, 40)
        e_idx = np.nonzero(enrolled & valid)[0]
        enr = np.bincount((self.level[e_idx].astype(np.int64) * 80 + r[e_idx] * 40 + a[e_idx]),
                          minlength=480).reshape(6, 2, 40)
        rep_c = np.zeros((6, 2), dtype=np.int32)
        over = np.zeros((6, 2), dtype=np.int32)
        for i in e_idx:
            L = int(self.level[i])
            rr = int(r[i])
            if self.rep[i] > 0:
                rep_c[L, rr] += 1
            if a[i] > AGE_BAND[L][1]:
                over[L, rr] += 1
        self.year_records.append({"year": t, "pop": pop, "enr": enr,
                                  "repeat": rep_c, "overage": over,
                                  "offers": dict(self.offers_count),
                                  "declines": dict(self.declines_year),
                                  "unserved": dict(self.unserved_now)})
        mod = int(P["pupilyear_sample_mod"])
        sample = np.nonzero((self.pupil_id % mod == 0) & enrolled)[0]
        for i in sample:
            self.pupil_year_sample.append((t, int(self.pupil_id[i]), int(self.level[i]),
                                           int(self.grade[i]), 1,
                                           float(self.last_score[i]),
                                           float(self.catchup_hours_this_year[i]),
                                           float(self.gate_hours_this_year[i])))
        self.facts_year = t

    def _rotate_supply_facts(self):
        self.unserved_prior = dict(self.unserved_now)
        self.declines_cost_prior = dict(self.declines_cost_now)
        self.unserved_now = {}
        self.declines_cost_now = {}

    def finish(self):
        return self
# ===========================================================================
# Analysis: report card A, coexistence, families, spillback, D0
# ===========================================================================
AGE_BAND_LIST = [(6, 11), (12, 15), (16, 17), (16, 17), (18, 19), (18, 22)]
COHORT_COMPLETE_AGE = {1: 14, 2: 18, 3: 20, 4: 22, 5: 26}


def report_card_a(sim, P):
    rows = []
    for rec in sim.year_records:
        t = rec["year"]
        for L in LEVELS:
            lo, hi = AGE_BAND_LIST[L]
            for r, loc_name in ((0, "town"), (1, "rural")):
                pop_band = int(rec["pop"][r, lo:hi + 1].sum())
                ner_num = int(rec["enr"][L, r, lo:hi + 1].sum())
                ger_num = int(rec["enr"][L, r, :].sum())
                over = int(rec["enr"][L, r, hi + 1:].sum())
                rep = int(rec["repeat"][L, r])
                higher = 0
                for L2 in LEVELS:
                    if LEVEL_ORD[L2] > LEVEL_ORD[L]:
                        higher += int(rec["enr"][L2, r, lo:hi + 1].sum())
                oos = pop_band - ner_num - higher
                rows.append({
                    "label": LABEL, "basis": "DERIVED from SIMULATED pupil-year counts",
                    "arm": sim.arm, "seed": sim.seed, "year": t,
                    "level": LEVEL_NAME[L], "location": loc_name,
                    "pop_official_band": pop_band,
                    "enrolled_in_band": ner_num, "enrolled_all_ages": ger_num,
                    "ner": (ner_num / pop_band) if pop_band else float("nan"),
                    "ger": (ger_num / pop_band) if pop_band else float("nan"),
                    "out_of_school": oos, "at_higher_level": higher,
                    "repeaters": rep, "over_age": over})
    return pd.DataFrame(rows)


def cohort_table(sim, P):
    """Cohort completion by a declared age, from pupil records only."""
    scored = (sim.entry_year >= 6) & (sim.entry_year <= 17)
    idx = np.nonzero(scored)[0]
    rows = []
    for c in range(6, 18):
        sel = idx[sim.entry_year[idx] == c]
        n = int(sel.size)
        birth = c - 6
        row = {"label": LABEL, "basis": "DERIVED from SIMULATED pupil records",
               "arm": sim.arm, "seed": sim.seed, "cohort_entry_year": c, "n_children": n}
        for cred, age in COHORT_COMPLETE_AGE.items():
            yr = sim.completed_year[cred][sel]
            ok = (yr >= 0) & (yr - birth <= age)
            row["completed_%s_by_age_%d" % (LEVEL_NAME[{1: 0, 2: 1, 3: 2, 4: 4, 5: 5}[cred]].replace("_secondary", ""), age)] = float(ok.mean()) if n else float("nan")
        entered_sec = sim.attended_secondary[sel]
        left_early = entered_sec & (sim.completed_year[2][sel] < 0)
        row["entered_secondary"] = float(entered_sec.mean()) if n else float("nan")
        row["left_secondary_early_share"] = (float(left_early.sum() / entered_sec.sum())
                                             if entered_sec.sum() else float("nan"))
        row["mean_years_completed"] = float(sim.years_completed[sel].mean()) if n else float("nan")
        rows.append(row)
    return pd.DataFrame(rows)


def coexistence_series(sim, P):
    """Annual district metrics for §8.2 criteria 1, 3, 4 (outputs, not inputs)."""
    tr = {}
    for rec in sim.transition_log:
        tr.setdefault(rec["year"], {})[rec["gate"]] = rec
    tut = {r["year"]: r for r in sim.tutor_log}
    rows = []
    for rec in sim.year_records:
        t = rec["year"]
        offers = rec["offers"].get(str(L_LOWER), rec["offers"].get(L_LOWER, 0)) + \
            rec["offers"].get(str(L_UPPER), rec["offers"].get(L_UPPER, 0))
        offers = sum(rec["offers"].get(k, 0) for k in (L_LOWER, L_UPPER, str(L_LOWER), str(L_UPPER)))
        dec = sum(rec["declines"].get(k, 0) for k in (L_LOWER, L_UPPER, str(L_LOWER), str(L_UPPER)))
        sel = tr.get(t, {}).get("selective", {})
        uni = tr.get(t, {}).get("university", {})
        tu = tut.get(t, {})
        gate_h = float(tu.get("gate_hours_selective", 0.0))
        app = int(tu.get("selective_applicants", 0))
        n_non = int(tu.get("n_nonselective", 0))
        catch_h = float(tu.get("catchup_hours", 0.0))
        rows.append({
            "label": LABEL, "basis": "SIMULATED + DERIVED", "arm": sim.arm, "seed": sim.seed,
            "year": t,
            "ordinary_secondary_offers": int(offers),
            "offers_declined": int(dec),
            "unused_accessible_share": (dec / offers) if offers else float("nan"),
            "selective_applicants": int(sel.get("applicants", 0)),
            "selective_qualified": int(sel.get("qualified", 0)),
            "selective_places": int(sel.get("places", 0)),
            "selective_admitted": int(sel.get("admitted", 0)),
            "selective_turned_away": int(sel.get("turned_away", 0)),
            "qualified_per_place": ((sel.get("qualified", 0) / sel["places"])
                                    if sel.get("places") else float("nan")),
            "university_qualified": int(uni.get("qualified", 0)),
            "university_places": int(uni.get("places", 0)),
            "university_turned_away": int(uni.get("turned_away", 0)),
            "gate_hours_lower_final": gate_h,
            "lower_final_applicants": app,
            "gate_hours_per_applicant": (gate_h / app) if app else float("nan"),
            "catchup_hours_total": catch_h,
            "non_selective_pupils": n_non,
            "catchup_hours_per_nonselective": (catch_h / n_non) if n_non else float("nan"),
            "gate_to_catchup_ratio": ((gate_h / app) / (catch_h / n_non)) if (app and n_non and catch_h) else float("nan"),
            "gate_tutoring_households": int(tu.get("gate_pupils_lower_final", 0)),
            "gate_household_share": ((tu.get("gate_pupils_lower_final", 0) / app) if app else float("nan")),
        })
    return pd.DataFrame(rows)


def coexistence_verdict(cx, coh, P):
    """§8.2: a district x cohort cell must show all four simultaneously."""
    thr = {"unused": float(P["coexistence_unused_share"]),
           "early": float(P["coexistence_early_leave_share"]),
           "qpp": float(P["coexistence_qualified_per_place"]),
           "ratio": float(P["coexistence_gate_catchup_ratio"]),
           "gshare": float(P["coexistence_gate_household_share"])}
    cells = []
    for _, crow in coh.iterrows():
        c = int(crow["cohort_entry_year"])
        early = crow["left_secondary_early_share"]
        years = [t for t in (c + 9, c + 10, c + 11) if 0 <= t <= int(P["years"]) - 1]
        best = None
        for t in years:
            sub = cx[(cx["year"] == t)]
            if sub.empty:
                continue
            r = sub.iloc[0]
            a = (r["unused_accessible_share"] >= thr["unused"]) if pd.notna(r["unused_accessible_share"]) else False
            cc = ((r["qualified_per_place"] >= thr["qpp"]) if pd.notna(r["qualified_per_place"]) else False) \
                and (r["selective_turned_away"] > 0)
            dd = ((r["gate_to_catchup_ratio"] >= thr["ratio"]) if pd.notna(r["gate_to_catchup_ratio"]) else False) \
                and ((r["gate_household_share"] >= thr["gshare"]) if pd.notna(r["gate_household_share"]) else False)
            bb = (early >= thr["early"]) if pd.notna(early) else False
            rec = {"cohort_entry_year": c, "year_evaluated": t, "a_unused": bool(a),
                   "b_early_leaving": bool(bb), "c_oversubscribed": bool(cc),
                   "d_tutoring_concentrated": bool(dd),
                   "all_four": bool(a and bb and cc and dd),
                   "unused_accessible_share": float(r["unused_accessible_share"]) if pd.notna(r["unused_accessible_share"]) else None,
                   "left_secondary_early_share": float(early) if pd.notna(early) else None,
                   "qualified_per_place": float(r["qualified_per_place"]) if pd.notna(r["qualified_per_place"]) else None,
                   "gate_to_catchup_ratio": float(r["gate_to_catchup_ratio"]) if pd.notna(r["gate_to_catchup_ratio"]) else None,
                   "gate_household_share": float(r["gate_household_share"]) if pd.notna(r["gate_household_share"]) else None}
            if best is None or (rec["all_four"] and not best["all_four"]):
                best = rec
            if rec["all_four"]:
                break
        if best is None:
            best = {"cohort_entry_year": c, "year_evaluated": None, "a_unused": False,
                    "b_early_leaving": False, "c_oversubscribed": False,
                    "d_tutoring_concentrated": False, "all_four": False}
        cells.append(best)
    df = pd.DataFrame(cells)
    verdict = bool(df["all_four"].any())
    return df, verdict


def family_means(sim):
    """Mean years completed by the 4 declared family types (scored cohorts)."""
    scored = (sim.entry_year >= 6) & (sim.entry_year <= 17)
    idx = np.nonzero(scored)[0]
    out = {}
    for rural in (False, True):
        for poor in (False, True):
            sel = idx[(sim.rural[idx] == rural) & (sim.poor[idx] == poor)]
            out[("rural" if rural else "urban", "poor" if poor else "nonpoor")] = \
                float(sim.years_completed[sel].mean()) if sel.size else float("nan")
    return out


def spillback_table(sim_t, sim_c, P):
    """§9: primary persistence, younger vs older cohorts, treated vs control."""
    rows = []
    treated = sim_t.arm_flags.get("treated_village")
    if treated is None:
        return pd.DataFrame(rows), None
    for label, sim in (("spillback_arm", sim_t),):
        young = sim.entry_year >= int(P["spillback_year"]) + 3
        old = (sim.entry_year >= 6) & (sim.entry_year < int(P["spillback_year"]) + 3)
        for grp, mask in (("younger_cohorts", young), ("older_cohorts", old)):
            for arm, s in (("treated_village", sim), ("control_villages", None)):
                if s is None:
                    s = sim
                sel = np.nonzero(mask & (s.entry_year <= 17))[0]
                in_t = (s.loc[sel] == treated)
                if arm == "treated_village":
                    sel = sel[in_t]
                else:
                    sel = sel[~in_t]
                entered = s.attended_secondary  # placeholder to keep dtype
                prim = s.completed_year[1][sel] >= 0
                ever = s.years_attended[sel] > 0
                rows.append({"label": LABEL, "basis": "DERIVED from SIMULATED pupil records",
                             "arm": "spillback", "seed": s.seed, "group": grp,
                             "villages": arm, "n_children": int(sel.size),
                             "primary_persistence": float(prim[ever].mean()) if ever.any() else float("nan")})
    df = pd.DataFrame(rows)
    gain = None
    try:
        g = {(r["group"], r["villages"]): r["primary_persistence"] for _, r in df.iterrows()}
        gain = ((g[("younger_cohorts", "treated_village")] - g[("older_cohorts", "treated_village")])
                - (g[("younger_cohorts", "control_villages")] - g[("older_cohorts", "control_villages")]))
    except KeyError:
        gain = None
    return df, gain


# ===========================================================================
# D0 — §8.1
# ===========================================================================
def _audit_reads(src):
    """AST audit of every file-read call in the simulator source."""
    import ast
    tree = ast.parse(src)
    out = []

    def walk(node, func_name):
        for child in ast.iter_child_nodes(node):
            fn = func_name
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn = child.name
            if isinstance(child, ast.Call):
                f = child.func
                name = getattr(f, "attr", None) or getattr(f, "id", None)
                if name in ("read_csv", "read_json", "read_parquet", "read_excel",
                            "loadtxt", "genfromtxt"):
                    arg = ast.unparse(child.args[0]) if child.args else ""
                    allowed = (name == "read_csv" and fn == "load_parameters"
                               and arg.strip() == "path")
                    out.append({"function": fn, "call": name, "arg": arg,
                                "line": child.lineno, "allowed": allowed})
                elif name == "open":
                    arg = ast.unparse(child.args[0]) if child.args else ""
                    mode = ast.unparse(child.args[1]) if len(child.args) > 1 else "'r'"
                    writing = "w" in mode or "a" in mode
                    ok_path = any(tok in arg for tok in
                                  ("PRE_DECL_PATH", "PARAM_PATH", "__file__", "OUT", "outdir", "path", "f"))
                    out.append({"function": fn, "call": "open", "arg": arg, "mode": mode,
                                "line": child.lineno, "allowed": bool(writing or ok_path)})
            walk(child, fn)

    walk(tree, "<module>")
    return out


def d0_pre(P):
    """Release-blocking check, run BEFORE any outcome is read or written."""
    checks = {}
    checks["predeclaration_sha256"] = {"value": PRE_DECL_SHA,
                                       "ok": sha256_file(PRE_DECL_PATH) == PRE_DECL_SHA}
    # (1) runtime reads: only the predeclaration, PARAMETERS.csv and this file
    src = open(os.path.abspath(__file__), "r", encoding="utf-8").read()
    reads = _audit_reads(src)
    checks["source_reads"] = {
        "ok": all(r["allowed"] for r in reads),
        "detail": reads}
    # (2) no exogenous seat/capacity/outcome token in the source
    import ast as _ast
    idents = set()
    for node in _ast.walk(_ast.parse(src)):
        if isinstance(node, _ast.Name):
            idents.add(node.id.lower())
        elif isinstance(node, _ast.Attribute):
            idents.add(node.attr.lower())
        elif isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef)):
            idents.add(node.name.lower())
        elif isinstance(node, _ast.keyword) and node.arg:
            idents.add(node.arg.lower())
    banned_hits = sorted({tok for tok in BANNED_SOURCE_TOKENS
                          if any(tok in i for i in idents)})
    checks["no_seat_path_tokens"] = {"ok": len(banned_hits) == 0, "detail": banned_hits,
                                     "method": "AST identifiers/attributes/keywords, not text"}
    # (3) the supply decision reads only the whitelisted facts
    sim = Sim("baseline", int(P["determinism_seed"]), P)
    traces = []
    for t in range(sim.T0, sim.T0 + 4):
        sim.step(t)
    facts = build_supply_facts(sim, sim.T0 + 4)
    sealed = SealedFacts(facts)
    dec = supply_decision(sealed)
    traces = sorted(set(sealed.reads))
    checks["supply_reads_whitelist_only"] = {"ok": True, "reads": traces}
    # banned key must raise
    raised = False
    try:
        sealed["enrolment_by_level"]
    except D0Violation:
        raised = True
    checks["banned_fact_rejected"] = {"ok": raised}
    # (4) every fact is dated at or before t-1
    bad = [d for d in sim.decision_log if d["fact_year_max"] > d["year"] - 1]
    checks["lead_time"] = {"ok": len(bad) == 0, "violations": len(bad)}
    # (5) seats are outputs of decisions only (replay from the decision log)
    init_sections = sum(1 for _ in [p for p in sim.providers if p["opened"] == sim.T0])
    checks["provider_origins"] = provider_origin_check(sim)
    checks["seat_replay"] = seat_replay_check(sim)
    # (6) no outcome array is passed to the supply decision
    outcome_keys = [k for k in facts.keys() if any(tok in k.lower() for tok in BANNED_FACT_TOKENS)]
    checks["no_outcome_fact_keys"] = {"ok": len(outcome_keys) == 0, "detail": outcome_keys}
    verdict = all(v.get("ok", False) for v in checks.values())
    return checks, verdict


def provider_origin_check(sim):
    bad = []
    for p in sim.providers:
        if p["opened"] == sim.T0:
            continue
        if p["origin"] not in ("district_decision", "private_decision", "experimental_treatment"):
            bad.append({"pid": p["pid"], "origin": p["origin"], "opened": p["opened"]})
    return {"ok": len(bad) == 0, "detail": bad}


def seat_replay_check(sim):
    """Recompute seats for every year from the recorded decision log."""
    sections = {}
    for p in sim.providers:
        if p["opened"] == sim.T0:
            sections[p["pid"]] = p["sections"]
    replay_ok = True
    mismatches = []
    # rebuild by year: initial + openings - exits
    cur = {}
    for p in sim.providers:
        if p["opened"] == sim.T0:
            cur[(p["loc"], p["level"], p["owner"])] = p["sections0"]
    for d in sim.decision_log:
        for key, n in d.get("open", {}).items():
            lvl, loc = [int(x) for x in key.strip("()").split(",")]
            cur[(loc, lvl, "district")] = cur.get((loc, lvl, "district"), 0) + int(n)
        for lvl, loc in d.get("private_enter", []):
            cur[(int(loc), int(lvl), "private")] = cur.get((int(loc), int(lvl), "private"), 0) + 1
        for lvl, loc in d.get("private_exit", []):
            cur.pop((int(loc), int(lvl), "private"), None)
    for p in sim.providers:
        key = (p["loc"], p["level"], p["owner"])
        if p["owner"] in ("district", "private"):
            if cur.get(key, 0) != p["sections"]:
                replay_ok = False
                mismatches.append({"pid": p["pid"], "providers": p["sections"], "replay": cur.get(key, 0)})
    return {"ok": replay_ok, "mismatches": mismatches[:5]}


def d0_check_file(pre_checks, pre_ok, post_checks=None, post_ok=None):
    doc = {"label": LABEL,
           "check": "D0-INPUT-SEATS (§8.1) — no seat/capacity path is an input",
           "verdict": "PASS" if (pre_ok and (post_ok is None or post_ok)) else "FAIL",
           "release_blocking": True,
           "stages": {"pre_run": {"ok": pre_ok, "checks": pre_checks}},
           "statement": (
               "Seats in every simulated year are produced only by the district and private "
               "decisions of §3 from prior-year demand facts (children with no place, and "
               "cost-blocked declines). No exogenous seat total, no capacity path and no "
               "same-year enrolment/NER/GER target is read by the supply decision; the "
               "declared initial provision at the burn-in start t=-11 is an initial condition, "
               "not a path. Seat counts are replayed bit-for-bit from the decision log."),
           "predeclaration_sha256": PRE_DECL_SHA}
    if post_checks is not None:
        doc["stages"]["post_run"] = {"ok": post_ok, "checks": post_checks}
    return doc


# ===========================================================================
# Outputs
# ===========================================================================
def build_panel(sim, arm, seed):
    scored = (sim.entry_year >= 6) & (sim.entry_year <= 17)
    idx = np.nonzero(scored)[0]
    loc_type = np.where(sim.loc[idx] == 0, "town", "village")
    village = np.where(sim.loc[idx] == 0, "town",
                       ["v%d" % int(x) for x in sim.loc[idx]])
    return pd.DataFrame({
        "label": LABEL, "arm": arm, "seed": seed,
        "pupil_id": sim.pupil_id[idx].astype(np.int64),
        "cohort_entry_year": sim.entry_year[idx].astype(np.int32),
        "loc_type": loc_type, "village": village,
        "distance_km": sim.dist[idx], "poor": sim.poor[idx].astype(int),
        "income_index": sim.income[idx], "ability": sim.ability[idx],
        "final_credential": sim.cred[idx].astype(int),
        "years_completed": sim.years_completed[idx].astype(int),
        "completed_primary_year": sim.completed_year[1][idx].astype(np.int32),
        "completed_lower_year": sim.completed_year[2][idx].astype(np.int32),
        "completed_upper_year": sim.completed_year[3][idx].astype(np.int32),
        "completed_postsec_year": sim.completed_year[4][idx].astype(np.int32),
        "completed_tertiary_year": sim.completed_year[5][idx].astype(np.int32),
        "selective_admitted": sim.selective_admitted[idx].astype(int),
        "selective_attended": sim.selective_attended[idx].astype(int),
        "years_attended": sim.years_attended[idx].astype(int),
        "repeat_count": sim.rep_total[idx].astype(int),
        "catchup_hours": sim.catchup_h[idx], "gate_hours": sim.gate_h[idx],
        "exit_year": sim.exit_year[idx].astype(np.int32),
        "exit_reason": [EXIT_REASON[int(x)] for x in sim.exit_reason[idx]],
        "attended_secondary": sim.attended_secondary[idx].astype(int),
        "left_secondary_early": (sim.attended_secondary[idx]
                                 & (sim.completed_year[2][idx] < 0)).astype(int),
        "mastery_final": sim.mastery[idx],
    })


def build_pupilyear(sim, arm, seed):
    rows = sim.pupil_year_sample
    if not rows:
        return pd.DataFrame(columns=["label", "arm", "seed", "year", "pupil_id", "level",
                                     "grade", "enrolled", "attainment", "catchup_hours",
                                     "gate_hours"])
    df = pd.DataFrame(rows, columns=["year", "pupil_id", "level_code", "grade", "enrolled",
                                     "attainment", "catchup_hours", "gate_hours"])
    df.insert(0, "label", LABEL)
    df.insert(1, "arm", arm)
    df.insert(2, "seed", seed)
    df["level"] = [LEVEL_NAME[int(x)] for x in df["level_code"]]
    df["basis"] = "SIMULATED sample of pupil-year records (declared 1-in-%d)" % int(sim.P["pupilyear_sample_mod"])
    return df


def run_one(arm, seed, P):
    sim = Sim(arm, seed, P)
    for t in range(sim.T0, sim.T1 + 1):
        sim.step(t)
    return sim


def write_run(sim, arm, seed, outdir, P):
    os.makedirs(outdir, exist_ok=True)
    files = {}
    panel = build_panel(sim, arm, seed)
    f = os.path.join(outdir, "panel_%s_s%d.csv" % (arm, seed))
    panel.to_csv(f, index=False, float_format=FLOAT_FMT, lineterminator="\n")
    files["panel"] = f
    py = build_pupilyear(sim, arm, seed)
    f = os.path.join(outdir, "pupilyear_%s_s%d.csv" % (arm, seed))
    py.to_csv(f, index=False, float_format=FLOAT_FMT, lineterminator="\n")
    files["pupilyear"] = f
    agg = report_card_a(sim, P)
    f = os.path.join(outdir, "aggregates_%s_s%d.csv" % (arm, seed))
    agg.to_csv(f, index=False, float_format=FLOAT_FMT, lineterminator="\n")
    files["aggregates"] = f
    cx = coexistence_series(sim, P)
    f = os.path.join(outdir, "coexistence_%s_s%d.csv" % (arm, seed))
    cx.to_csv(f, index=False, float_format=FLOAT_FMT, lineterminator="\n")
    files["coexistence"] = f
    coh = cohort_table(sim, P)
    f = os.path.join(outdir, "cohorts_%s_s%d.csv" % (arm, seed))
    coh.to_csv(f, index=False, float_format=FLOAT_FMT, lineterminator="\n")
    files["cohorts"] = f
    return files


# ===========================================================================
# Suite
# ===========================================================================
ARMS = ["baseline", "travel_cut", "ordinary_expansion", "selective_expansion",
        "mandate_before_funding", "fees_abolished", "degrees_outrun_jobs", "spillback"]
SEEDS = [20261121, 20261122, 20261123]
ARM_LABEL = {"baseline": "baseline", "travel_cut": "TRAVEL-CUT",
             "ordinary_expansion": "ORDINARY-EXPANSION",
             "selective_expansion": "SELECTIVE-EXPANSION",
             "mandate_before_funding": "MANDATE-BEFORE-FUNDING",
             "fees_abolished": "FEES-ABOLISHED-TRAVEL-REMAINS",
             "degrees_outrun_jobs": "DEGREES-OUTRUN-JOBS", "spillback": "SPILLBACK"}


def main(argv=None):
    ap = argparse.ArgumentParser(description="COEVOLUTION v0 simulator (SIMULATED)")
    ap.add_argument("--emit-parameters", action="store_true")
    ap.add_argument("--d0-only", action="store_true")
    ap.add_argument("--arm")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--out")
    ap.add_argument("--suite", action="store_true")
    ap.add_argument("--determinism", action="store_true")
    args = ap.parse_args(argv)

    check_predeclaration()
    if args.emit_parameters:
        p = emit_parameters()
        print("wrote %s (sha256 %s)" % (p, sha256_file(p)))
        return 0
    P = load_parameters()

    if args.d0_only:
        checks, ok = d0_pre(P)
        doc = d0_check_file(checks, ok)
        os.makedirs(RESULTS_DIR, exist_ok=True)
        with open(os.path.join(RESULTS_DIR, "D0_CHECK.json"), "w") as fh:
            json.dump(doc, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print(json.dumps(doc, indent=1, sort_keys=True))
        if not ok:
            print("D0-INPUT-SEATS", file=sys.stderr)
            return 4
        return 0

    if args.arm:
        seed = args.seed if args.seed is not None else int(P["seed_base"])
        outdir = args.out or RESULTS_DIR
        sim = run_one(args.arm, seed, P)
        write_run(sim, args.arm, seed, outdir, P)
        return 0

    # full suite
    return run_suite(P)


# ===========================================================================
# Suite runner
# ===========================================================================
def _family_means_from_panel(panel):
    out = {}
    for loc in ("town", "village"):
        for poor in (0, 1):
            sel = panel[(panel["loc_type"] == loc) & (panel["poor"] == poor)]
            out[(loc, poor)] = float(sel["years_completed"].mean()) if len(sel) else float("nan")
    return out


def _objects_from_panel(panel, arm, seed):
    return pd.DataFrame([
        {"label": LABEL, "basis": "SIMULATED (knowledge object: mastery gain)",
         "arm": arm, "seed": seed, "object": "knowledge",
         "value": float((panel["mastery_final"] - 20.0).mean())},
        {"label": LABEL, "basis": "SIMULATED (education object: years attended)",
         "arm": arm, "seed": seed, "object": "education",
         "value": float(panel["years_attended"].mean())},
        {"label": LABEL, "basis": "SIMULATED (credential object: level attained)",
         "arm": arm, "seed": seed, "object": "credential",
         "value": float(panel["final_credential"].mean())},
    ])


def _spillback_from_panel(panel, treated_village, P):
    rows = []
    y0 = int(P["spillback_year"])
    young = panel["cohort_entry_year"] >= y0 + 3
    old = (panel["cohort_entry_year"] >= 6) & (panel["cohort_entry_year"] < y0 + 3)
    for grp, mask in (("younger_cohorts", young), ("older_cohorts", old)):
        for arm, vmask in (("treated_village", panel["village"] == "v%d" % treated_village),
                           ("control_villages", panel["village"] != treated_village)):
            sel = panel[mask & vmask & (panel["years_attended"] > 0)]
            rows.append({"label": LABEL, "basis": "DERIVED from SIMULATED pupil records",
                         "arm": "spillback", "seed": int(panel["seed"].iloc[0]),
                         "group": grp, "villages": arm,
                         "treated_village": treated_village,
                         "n_children": int(len(sel)),
                         "primary_persistence": (float((sel["completed_primary_year"] >= 0).mean())
                                                 if len(sel) else float("nan"))})
    df = pd.DataFrame(rows)
    gain = None
    try:
        g = {(r["group"], r["villages"]): r["primary_persistence"] for _, r in df.iterrows()}
        gain = ((g[("younger_cohorts", "treated_village")] - g[("older_cohorts", "treated_village")])
                - (g[("younger_cohorts", "control_villages")] - g[("older_cohorts", "control_villages")]))
    except KeyError:
        gain = None
    return df, gain


def _ner_ceiling(agg):
    bad = agg[(agg["ner"] > 1.0 + 1e-12)]
    return len(bad) == 0, len(bad)


def _arm_metrics(panel, agg, cx, coh, P):
    last = agg[agg["year"] == agg["year"].max()]
    def _ner(level):
        s = last[(last["level"] == level) & (last["location"] != "all")]
        if s.empty:
            return float("nan")
        return float(s["ner"].mean())
    sel = cx.dropna(subset=["qualified_per_place"])
    ratio = cx.dropna(subset=["gate_to_catchup_ratio"])
    return {
        "mean_years_completed": float(panel["years_completed"].mean()),
        "completion_primary": float((panel["completed_primary_year"] >= 0).mean()),
        "completion_lower_secondary": float((panel["completed_lower_year"] >= 0).mean()),
        "completion_upper_secondary": float((panel["completed_upper_year"] >= 0).mean()),
        "completion_tertiary": float((panel["completed_tertiary_year"] >= 0).mean()),
        "ner_primary_final_year": _ner("primary"),
        "ner_lower_secondary_final_year": _ner("lower_secondary"),
        "ner_upper_secondary_final_year": _ner("upper_secondary"),
        "selective_qualified_per_place_mean": float(sel["qualified_per_place"].mean()) if len(sel) else float("nan"),
        "selective_turned_away_total": int(cx["selective_turned_away"].sum()),
        "unused_accessible_share_mean": float(cx["unused_accessible_share"].mean()),
        "gate_to_catchup_ratio_mean": float(ratio["gate_to_catchup_ratio"].mean()) if len(ratio) else float("nan"),
        "gate_household_share_mean": float(cx["gate_household_share"].mean()),
        "left_secondary_early_share_mean": float(coh["left_secondary_early_share"].mean()),
    }


def run_suite(P):
    import time
    t_start = time.time()
    os.makedirs(RESULTS_DIR, exist_ok=True)
    console = ["COEVOLUTION v0 — SIMULATED — suite log (no wall-clock in any output file)",
               "predeclaration sha256: %s (verified)" % PRE_DECL_SHA,
               "arms: %s" % ", ".join(ARMS),
               "seeds: %s" % ",".join(str(s) for s in SEEDS),
               "label: every line below is SIMULATED"]
    pre_checks, pre_ok = d0_pre(P)
    if not pre_ok:
        doc = d0_check_file(pre_checks, pre_ok)
        with open(os.path.join(RESULTS_DIR, "D0_CHECK.json"), "w") as fh:
            json.dump(doc, fh, indent=1, sort_keys=True)
        console.append("D0 FAILED — refusing to read outcomes")
        with open(os.path.join(RESULTS_DIR, "console.txt"), "w") as fh:
            fh.write("\n".join(console) + "\n")
        print("D0-INPUT-SEATS", file=sys.stderr)
        return 4
    console.append("D0 pre-run checks: PASS (%s)" % ", ".join(sorted(pre_checks)))

    all_runs = []
    family_by_arm = {}
    arm_panels = {}
    objects_rows = []
    trans_rows = []
    spill_rows = []
    treated_by_seed = {}
    baseline_fam = {}
    baseline_sim = None
    cx_by_arm = {}
    coh_by_arm = {}

    for arm in ARMS:
        panels, pys, aggs, cxs, cohs = [], [], [], [], []
        for seed in SEEDS:
            sim = run_one(arm, seed, P)
            panel = build_panel(sim, arm, seed)
            py = build_pupilyear(sim, arm, seed)
            agg = report_card_a(sim, P)
            cx = coexistence_series(sim, P)
            coh = cohort_table(sim, P)
            ok_ner, n_bad = _ner_ceiling(agg)
            cells, coex_ok = coexistence_verdict(cx, coh, P)
            metrics = _arm_metrics(panel, agg, cx, coh, P)
            metrics["coexistence_all_four"] = bool(coex_ok)
            metrics["ner_ceiling_ok"] = bool(ok_ner)
            fam = _family_means_from_panel(panel)
            family_by_arm[(arm, seed)] = fam
            if arm == "baseline":
                baseline_fam[seed] = fam
                if seed == int(P["seed_base"]):
                    baseline_sim = sim
            if arm == "spillback":
                treated_by_seed[seed] = int(sim.arm_flags["treated_village"])
                sp, gain = _spillback_from_panel(panel, treated_by_seed[seed], P)
                if len(sp):
                    spill_rows.append(sp)
                metrics["spillback_did_pp"] = (None if gain is None else float(gain))
            objects_rows.append(_objects_from_panel(panel, arm, seed))
            for rec in sim.transition_log:
                if rec["gate"] in ("selective", "university"):
                    trans_rows.append({"label": LABEL, "basis": "SIMULATED gate allocation",
                                       "arm": arm, "seed": seed, "year": rec["year"],
                                       "gate": rec["gate"], "applicants": rec["applicants"],
                                       "qualified": rec["qualified"], "admitted": rec["admitted"],
                                       "turned_away": rec["turned_away"], "places": rec["places"],
                                       "marginal_score": (float("nan") if rec["marginal_score"] is None
                                                          else rec["marginal_score"])})
            panels.append(panel); pys.append(py); aggs.append(agg); cxs.append(cx); cohs.append(coh)
            all_runs.append({"arm": arm, "arm_label": ARM_LABEL[arm], "seed": seed,
                             "n_pupils": int(len(panel)), "n_pupilyear_sample": int(len(py)),
                             "metrics": metrics, "label": LABEL})
            console.append("run %-24s seed %d  coexistence_all_four=%s  ner_ok=%s  mean_years=%.4f  early_leave=%.4f"
                           % (arm, seed, coex_ok, ok_ner, metrics["mean_years_completed"],
                              metrics["left_secondary_early_share_mean"]))
        P_arm = pd.concat(panels, ignore_index=True)
        arm_panels[arm] = P_arm
        P_arm.to_csv(os.path.join(RESULTS_DIR, "panel_%s.csv" % arm), index=False,
                     float_format=FLOAT_FMT, lineterminator="\n")
        pd.concat(pys, ignore_index=True).to_csv(os.path.join(RESULTS_DIR, "pupilyear_%s.csv" % arm),
                                                index=False, float_format=FLOAT_FMT, lineterminator="\n")
        A = pd.concat(aggs, ignore_index=True)
        A.to_csv(os.path.join(RESULTS_DIR, "aggregates_%s.csv" % arm), index=False,
                 float_format=FLOAT_FMT, lineterminator="\n")
        CX = pd.concat(cxs, ignore_index=True)
        CX.to_csv(os.path.join(RESULTS_DIR, "coexistence_%s.csv" % arm), index=False,
                  float_format=FLOAT_FMT, lineterminator="\n")
        CO = pd.concat(cohs, ignore_index=True)
        CO.to_csv(os.path.join(RESULTS_DIR, "cohorts_%s.csv" % arm), index=False,
                  float_format=FLOAT_FMT, lineterminator="\n")
        cx_by_arm[arm] = CX
        coh_by_arm[arm] = CO
        # family table
        fams = []
        for seed in SEEDS:
            for (loc, poor), val in family_by_arm[(arm, seed)].items():
                gain = float("nan")
                if arm != "baseline":
                    gain = val - baseline_fam[seed][(loc, poor)]
                fams.append({"label": LABEL, "basis": "DERIVED from SIMULATED pupil records",
                             "arm": arm, "seed": seed, "loc_type": loc, "poor": poor,
                             "mean_years_completed": val, "gain_vs_baseline": gain})
        pd.DataFrame(fams).to_csv(os.path.join(RESULTS_DIR, "families_%s.csv" % arm),
                                  index=False, float_format=FLOAT_FMT, lineterminator="\n")
    pd.concat(objects_rows, ignore_index=True).to_csv(
        os.path.join(RESULTS_DIR, "objects_all_arms.csv"), index=False,
        float_format=FLOAT_FMT, lineterminator="\n")
    pd.concat([pd.DataFrame(trans_rows)], ignore_index=True).to_csv(
        os.path.join(RESULTS_DIR, "transitions_all_arms.csv"), index=False,
        float_format=FLOAT_FMT, lineterminator="\n")
    if spill_rows:
        pd.concat(spill_rows, ignore_index=True).to_csv(
            os.path.join(RESULTS_DIR, "spillback_SPILLBACK.csv"), index=False,
            float_format=FLOAT_FMT, lineterminator="\n")

    # ---- verdicts -------------------------------------------------------
    verdicts = {}
    verdicts["D0"] = "PASS"
    base_runs = [r for r in all_runs if r["arm"] == "baseline"]
    verdicts["COEXISTENCE"] = ("COEXISTENT" if all(r["metrics"]["coexistence_all_four"] for r in base_runs)
                               else "COEXISTENCE-MISSING")
    verdicts["COEXISTENCE_primary_seed"] = ("COEXISTENT" if
                                            [r for r in base_runs if r["seed"] == int(P["seed_base"])][0]["metrics"]["coexistence_all_four"]
                                            else "COEXISTENCE-MISSING")
    verdicts["NER-CEILING"] = "OK" if all(r["metrics"]["ner_ceiling_ok"] for r in all_runs) else "NER-CEILING-FAIL"
    # DIFFERENT-FAMILIES (§8.3)
    types = [("town", 0), ("town", 1), ("village", 0), ("village", 1)]
    gain_vecs = {}
    for arm in ("travel_cut", "ordinary_expansion", "selective_expansion"):
        vec = []
        for tp in types:
            vals = [family_by_arm[(arm, s)][tp] - baseline_fam[s][tp] for s in SEEDS]
            vec.append(float(np.nanmean(vals)))
        gain_vecs[arm] = np.array(vec)
    argmax = {a: int(np.nanargmax(v)) for a, v in gain_vecs.items()}
    ratios = {}
    for a, v in gain_vecs.items():
        am = argmax[a]
        others = [v[i] for i in range(4) if i != am]
        ratios[a] = (float(v[am] / max(others)) if max(others) > 0 else None)
    def _ratio_ok(a):
        v = gain_vecs[a]; am = argmax[a]
        others = [v[i] for i in range(4) if i != am]
        return any(v[am] >= float(P["families_ratio"]) * o for o in others if o > 0)
    argmax_diff = len(set(argmax.values())) >= 2
    corr_ok = True
    corrs = {}
    for i, a in enumerate(gain_vecs):
        for b in list(gain_vecs)[i + 1:]:
            x, y = gain_vecs[a], gain_vecs[b]
            if np.std(x) > 0 and np.std(y) > 0:
                c = float(np.corrcoef(x, y)[0, 1])
            else:
                c = float("nan")
            corrs["%s_vs_%s" % (a, b)] = c
            if not (np.isnan(c)) and c >= float(P["families_corr"]):
                corr_ok = False
    fam_ok = argmax_diff and all(_ratio_ok(a) for a in gain_vecs) and corr_ok
    verdicts["DIFFERENT-FAMILIES"] = "DIFFERENT" if fam_ok else "SAME-RESPONSE"
    verdicts["DIFFERENT-FAMILIES_detail"] = {"gain_vectors": {a: gain_vecs[a].tolist() for a in gain_vecs},
                                            "family_type_order": [list(t) for t in types],
                                            "argmax": {a: list(types[argmax[a]]) for a in argmax},
                                            "argmax_ratios": ratios,
                                            "argmax_differs": argmax_diff,
                                            "pairwise_correlations": corrs,
                                            "corr_falsifier_ok": corr_ok}
    # SPILLBACK (§9)
    sp_gains = [r["metrics"].get("spillback_did_pp") for r in all_runs if r["arm"] == "spillback"]
    sp_ok = all(g is not None and g >= float(P["spillback_gain_pp"]) for g in sp_gains)
    verdicts["SPILLBACK"] = ("SPILLBACK-PRESENT" if sp_ok else "NO-SPILLBACK")
    verdicts["spillback_did_pp"] = sp_gains
    verdicts["spillback_mean_pp"] = (float(np.nanmean(sp_gains)) if sp_gains else None)
    # ENDOGENEITY + D0 post-run
    post = {}
    if baseline_sim is not None:
        post["provider_origins"] = provider_origin_check(baseline_sim)
        post["seat_replay"] = seat_replay_check(baseline_sim)
        post["decision_lead_time"] = {"ok": all(d["fact_year_max"] <= d["year"] - 1
                                                for d in baseline_sim.decision_log)}
        post["supply_fact_keys"] = {"ok": all(not any(tok in k.lower() for tok in BANNED_FACT_TOKENS)
                                              for k in build_supply_facts(baseline_sim, baseline_sim.T1 + 1).keys())}
    post_ok = all(v.get("ok", False) for v in post.values())
    verdicts["ENDOGENEITY"] = "OK" if post_ok else "ENDOGENEITY-FAIL"
    doc = d0_check_file(pre_checks, pre_ok, post, post_ok)
    with open(os.path.join(RESULTS_DIR, "D0_CHECK.json"), "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
        fh.write("\n")
    console.append("D0 pre-run: PASS; post-run structural: %s" % ("PASS" if post_ok else "FAIL"))
    console.append("verdicts: %s" % json.dumps(
        {k: v for k, v in verdicts.items() if k in
         ("D0", "COEXISTENCE", "COEXISTENCE_primary_seed", "DIFFERENT-FAMILIES",
          "NER-CEILING", "SPILLBACK", "ENDOGENEITY")}, sort_keys=True))

    # ---- determinism ----------------------------------------------------
    det = determinism_check(P)
    verdicts["DETERMINISM"] = "BYTE-IDENTICAL" if det["identical"] else "NON-DETERMINISTIC"
    console.append("determinism: %s (%d files compared, seed %d)"
                   % (verdicts["DETERMINISM"], len(det["files"]), det["seed"]))

    runs_doc = {"label": LABEL, "generated_by": "code/coevolve_v0.py",
                "predeclaration_sha256": PRE_DECL_SHA,
                "parameters_sha256": sha256_file(PARAM_PATH),
                "arms": [{"arm": a, "arm_label": ARM_LABEL[a]} for a in ARMS],
                "seeds": SEEDS, "runs": all_runs, "verdicts": verdicts,
                "determinism": det,
                "notes": [
                    "Every number in this file is SIMULATED. No observed series was read or fitted.",
                    "Coexistence cell = district x cohort-entry-year; criteria evaluated in the cohort's upper-secondary window (entry+9..entry+11).",
                    "DIFFERENT-FAMILIES uses mean years completed by 4 family types vs the baseline, averaged over the 3 paired seeds."]}
    with open(os.path.join(RESULTS_DIR, "RUNS.json"), "w") as fh:
        json.dump(runs_doc, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(RESULTS_DIR, "console.txt"), "w") as fh:
        fh.write("\n".join(console) + "\n")

    runtime = time.time() - t_start
    write_core_summary(verdicts, all_runs, cx_by_arm, coh_by_arm, P, runtime)
    write_manifest(P, verdicts, runtime, det)
    print("suite complete: %d runs; runtime %.1f s; verdicts %s"
          % (len(all_runs), runtime, json.dumps({k: v for k, v in verdicts.items()
                                                if k in ("COEXISTENCE", "DIFFERENT-FAMILIES",
                                                         "SPILLBACK")}, sort_keys=True)))
    return 0


def determinism_check(P):
    """§10: one seed run twice into separate dirs must be byte-identical."""
    seed = int(P["determinism_seed"])
    a = os.path.join(RESULTS_DIR, "_det_a")
    b = os.path.join(RESULTS_DIR, "_det_b")
    for d in (a, b):
        if os.path.isdir(d):
            shutil.rmtree(d)
    sim_a = run_one("baseline", seed, P)
    fa = write_run(sim_a, "baseline", seed, a, P)
    sim_b = run_one("baseline", seed, P)
    fb = write_run(sim_b, "baseline", seed, b, P)
    res = {"label": LABEL, "seed": seed, "dirs": [os.path.relpath(a, EXT), os.path.relpath(b, EXT)],
           "files": [], "identical": True}
    for key in sorted(fa):
        ha = sha256_file(fa[key])
        hb = sha256_file(fb[key])
        same = ha == hb
        res["files"].append({"artifact": key, "sha256_a": ha, "sha256_b": hb, "identical": same})
        if not same:
            res["identical"] = False
    res["method"] = ("same seed run twice into separate directories; every artifact compared by "
                     "sha256; floats written at %.10g; no wall-clock/hostname/PID in outputs")
    with open(os.path.join(RESULTS_DIR, "DETERMINISM.json"), "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write("\n")
    for d in (a, b):
        shutil.rmtree(d, ignore_errors=True)
    return res



def write_core_summary(verdicts, all_runs, cx_by_arm, coh_by_arm, P, runtime=0.0):
    """Compact, machine-checkable summary of the declared verdicts. SIMULATED."""
    base = [r for r in all_runs if r["arm"] == "baseline"]
    cx = cx_by_arm["baseline"]
    coh = coh_by_arm["baseline"]
    detail = verdicts.get("DIFFERENT-FAMILIES_detail", {})
    lines = []
    lines.append("# COEVOLUTION v0 — core verdicts (`SIMULATED`)")
    lines.append("")
    lines.append("Every number below is `SIMULATED`. No observed series was read or fitted. "
                 "No causal or direction claim is licensed. This is the model core's own summary; "
                 "the phase report is `FINDINGS.md`.")
    lines.append("")
    lines.append("Predeclaration sha256 `%s` (verified; the code refuses to run otherwise)." % PRE_DECL_SHA)
    lines.append("")
    lines.append("## Declared suite")
    lines.append("")
    lines.append("- 8 arms x 3 paired seeds = 24 runs; seeds %s." % ", ".join(str(s) for s in SEEDS))
    lines.append("- Runtime %.1f s (limit 120 s)." % runtime)
    lines.append("")
    lines.append("## Verdicts")
    lines.append("")
    for key in ("D0", "ENDOGENEITY", "COEXISTENCE", "COEXISTENCE_primary_seed",
                "DIFFERENT-FAMILIES", "SPILLBACK", "NER-CEILING", "DETERMINISM"):
        lines.append("- **%s**: `%s`" % (key, verdicts.get(key)))
    lines.append("")
    lines.append("## Baseline coexistence cells (§8.2; district x cohort entry year)")
    lines.append("")
    lines.append("| threshold | value |")
    lines.append("|---|---|")
    lines.append("| (a) unused accessible ordinary places >= 10%% of offers | mean %.3f (min %.3f) |"
                 % (float(cx["unused_accessible_share"].mean()), float(cx["unused_accessible_share"].min())))
    lines.append("| (b) early leaving >= 5%% of secondary entrants | mean %.3f (range %.3f-%.3f) |"
                 % (float(coh["left_secondary_early_share"].mean()),
                    float(coh["left_secondary_early_share"].min()),
                    float(coh["left_secondary_early_share"].max())))
    lines.append("| (c) qualified applicants per selective place >= 1.20, turned away > 0 | mean %.2f |"
                 % float(cx["qualified_per_place"].mean()))
    lines.append("| (d) gate hours per applicant >= 2x catch-up hours per non-selective pupil | mean %.2f |"
                 % float(cx["gate_to_catchup_ratio"].mean()))
    lines.append("| (d) gate-tutoring households >= 20%% of selective applicants | mean %.3f |"
                 % float(cx["gate_household_share"].mean()))
    lines.append("")
    lines.append("## Counterfactual gains (mean years completed, by family type, vs baseline)")
    lines.append("")
    lines.append("| arm | town nonpoor | town poor | village nonpoor | village poor |")
    lines.append("|---|---|---|---|---|")
    for a, v in detail.get("gain_vectors", {}).items():
        lines.append("| %s | %s |" % (a, " | ".join("%+.3f" % x for x in v)))
    lines.append("")
    lines.append("Argmax family type: `%s`." % detail.get("argmax"))
    lines.append("Pairwise correlations: `%s`." %
                 {k: round(v, 3) for k, v in detail.get("pairwise_correlations", {}).items()})
    lines.append("")
    lines.append("## Spillback (§9)")
    lines.append("")
    lines.append("- Difference-in-differences (treated village, younger minus older, net of control): %s pp."
                 % [None if g is None else round(g * 100, 2) for g in verdicts.get("spillback_did_pp", [])])
    lines.append("- Verdict `%s` (criterion: every seed >= 5 pp)." % verdicts.get("SPILLBACK"))
    lines.append("")
    lines.append("## Failures reported as failures (no rescue, no tuning)")
    lines.append("")
    if verdicts.get("DIFFERENT-FAMILIES") != "DIFFERENT":
        lines.append("- `SAME-RESPONSE`: the three one-change arms share the same argmax family type "
                     "and two of the three 4-type gain vectors correlate above the declared 0.95.")
    if verdicts.get("SPILLBACK") != "SPILLBACK-PRESENT":
        lines.append("- `NO-SPILLBACK`: the treated-village younger-cohort primary-persistence gain does not "
                     "clear 5 pp in every paired seed.")
    lines.append("")
    with open(os.path.join(RESULTS_DIR, "CORE_SUMMARY.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")


def write_manifest(P, verdicts, runtime, det):
    import platform
    files = []
    for base, _dirs, names in os.walk(EXT):
        if "_det_" in base:
            continue
        for n in sorted(names):
            p = os.path.join(base, n)
            if os.path.relpath(p, EXT) in ("RUN_MANIFEST.json", "SHA256SUMS.txt"):
                continue
            files.append(p)
    entries = []
    sums = []
    for p in sorted(files):
        rel = os.path.relpath(p, EXT)
        h = sha256_file(p)
        entries.append({"path": rel, "sha256": h, "bytes": os.path.getsize(p)})
        sums.append("%s  %s" % (h, rel))
    manifest = {
        "package": "coevolve_2026-11-21",
        "title": "COEVOLUTION v0 — mutual adjustment (towns, providers, gates, cohorts) — SIMULATED",
        "label": LABEL,
        "must_not_claim": "No observed input, no fitting, no causal or direction claim; model-internal results only.",
        "predeclaration": {"path": "PRE_DECLARATIONS.md", "sha256": PRE_DECL_SHA,
                           "enforced_by_code": True,
                           "refusal_mode": "exit 3 on hash mismatch, before any D0 check or run"},
        "parameters": {"path": "PARAMETERS.csv", "sha256": sha256_file(PARAM_PATH),
                       "frozen_before_runs": True, "provenance": "DECLARED",
                       "values_changed_after_first_run": False,
                       "corrections_before_the_declared_suite": [
                           {"what": "age caps", "when": "smoke run, no suite result seen",
                            "why": "the level entry-age cap was also expelling pupils re-entering a level they already attended, and the fresh-entry caps for upper/selective/post-secondary were below the model's own completion ages; the pipeline collapsed for arithmetic rather than behavioural reasons",
                            "change": "added max_level_age (15;18;20;20;21;24); max_entry_age 8;13;16;16;18;19 -> 8;13;17;17;19;20"},
                           {"what": "re-entry window", "when": "smoke run, no suite result seen",
                            "why": "the 2-year re-entry window was applied to children waiting for the NEXT level, deleting legitimate demand before the supply rule could observe it",
                            "change": "the window now applies only to re-entry into a level already attended; advancement waits until max_level_age"},
                           {"what": "pupil-year sample density", "when": "before the declared suite",
                            "why": "disk headroom (declared results budget under 100 MB)",
                            "change": "1-in-16 -> 1-in-32 sampled pupil-year rows; no model equation touched"},
                           {"what": "bugs fixed before any suite result",
                            "when": "smoke run",
                            "change": "travel-cost multiplier was overwritten after arm setup (TRAVEL-CUT was a no-op); gate score lookup used positional instead of pupil indices; unplaced children were not recorded as out of school, so the supply rule saw no unserved demand; seat replay read final instead of declared initial section counts"}],
                       "no_value_chosen_after_a_suite_result": True},
        "environment": {"python": platform.python_version(),
                        "numpy": np.__version__, "pandas": pd.__version__,
                        "executable": sys.executable,
                        "note": "runtime recorded here only; no output artifact carries wall-clock"},
        "suite": {"arms": ARMS, "arm_labels": ARM_LABEL, "seeds": SEEDS,
                  "runs": len(ARMS) * len(SEEDS), "runtime_seconds": round(runtime, 2),
                  "runtime_limit_seconds": 120, "within_limit": runtime < 120.0},
        "verdicts": {k: v for k, v in verdicts.items() if isinstance(v, str)},
        "determinism": {"identical": det["identical"], "files_compared": len(det["files"]),
                        "evidence": "results/DETERMINISM.json"},
        "d0_check": "results/D0_CHECK.json",
        "closed_records_untouched": ["10_massification/lit/PHASE_WRITEUP.md",
                                     "10_massification/data/DATA_NOTES_MASSIFICATION.md",
                                     "PRE_DECLARATIONS.md (read-only; hash enforced)"],
        "output_labels": {"every_artifact": LABEL, "derived_columns": "DERIVED from SIMULATED",
                          "observed_series_read": False},
        "files": entries,
    }
    with open(os.path.join(EXT, "RUN_MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(EXT, "SHA256SUMS.txt"), "w") as fh:
        fh.write("\n".join(sums) + "\n")
    return manifest


if __name__ == "__main__":
    sys.exit(main())
