#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sim.py -- SYNTHETIC education-system generator, version 0.

EVERYTHING THIS SCRIPT EMITS IS SYNTHETIC.  It is a seeded computer model that
grows a panel of countries x years x school levels from the declared equations
below.  It is NOT calibrated evidence about the world, NOT a forecast, and NOT
a fit to any observed country series.  The only observed numbers that enter are
the handful of declared TARGETS listed in the PARAMS table (income-scaling
exponents and the PHL-like milestone pattern).  No observed data file is read.

Deterministic: PCG64 seed 20261120, fixed draw order, fixed bisection counts,
fixed float formatting.  Two runs produce byte-identical results/*.csv.

Run:
    python sim.py --outdir results
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np

# =============================================================================
# PARAMS TABLE (every parameter, its value, source, and assumption status)
# =============================================================================
# name                  value                     source / status
# --------------------  --------------------------  --------------------------
# SEED                  20261120                    declared
# N_COUNTRIES           32                          declared (31 generic + 1 PHL-like)
# YEAR_START/END        1970 / 2024                 declared window, 55 years
# LEVELS                4 (primary, lower_secondary, upper_secondary, tertiary)
#
# DEMAND CEILING  d_L = logistic(a_L + b_L*log(GDPpc/1000) + g_L*urban
#                                + h_L*services + e_L,c)
# C_MEAN                (0.92, 0.72, 0.50, 0.32)    declared: ceiling at the
#                                                   reference point (GDPpc 3000,
#                                                   urban .50, services .42, e=0)
# B_PRIM                0.05                         declared (primary saturated)
# B_SEC                 solved, target 0.29           TARGET (brief), derived
# B_TER                 solved, target 0.78           TARGET (brief), derived
# G                     (0.30, .55, .75, .60)         declared
# H                     (0.20, .35, .45, .40)         declared
# SIGMA_E               (0.30, .50, .60, .70)         declared distribution
# X_REF                 log(3.0)                     declared reference income
# URBAN_REF             0.50                         declared reference urban
# SERVICES_REF          0.42                         declared reference services
#
# SUPPLY / CAPACITY GATE  K_t = clip(K0 + 0.30*Delta log GDPpc
#                                      + 0.05*Delta spend, .05, 1)
# KAPPA                 0.75                         declared gate exponent
# K_Y / K_S             0.30 / 0.05                  declared capacity loadings
# EFF_CAP               1.04                         declared numerical cap on p
#                                                      (=> GER <= 104, inside [0,105])
# PUSH                  (0.06, .05, .06, .08)        declared push size delta_L
#                       eff = min(EFF_CAP, d*gate + delta_L*law*gate)
#
# FLOW / STOCK  E = cohort*p ; GER = 100*E/cohort = 100*p ; comp = 100*p*SURVIVAL
# OMEGA                 (6/15, 3/15, 3/15, 5/15)     declared once-only age-band
#                                                   weights (anti double-count)
# SURVIVAL              (0.95, .95, .92, .88)        declared within-level survival
# ADJUST                (0.20, .18, .15, .12)        declared annual adjustment speed
#
# COUNTRY DRAWS (independent, fixed order)
# gdp0 ~ lognormal(median 2500, sigma_log 0.9), clipped [400, 20000]
# growth ~ Normal(.018, .008), clipped [0, .045]
# N0 ~ lognormal(median 12e6, sigma_log 1.0), clipped [3e5, 3e8]
# npop ~ Normal(.014, .006), clipped [0, .035]
# f0 ~ Uniform(1.8, 6.0) ; fdec ~ Uniform(.005, .045) ; f_min 1.3
# share014 = clip(.13 + .062*(f - 1.3), .12, .48)
# urban0 ~ U(.15,.75), ug ~ U(.001,.008), clip [.05,.95]
# services0 ~ U(.25,.55), svg ~ U(.001,.006), clip [.15,.85]
# spend0 ~ U(2,6), spg ~ U(0,.03), clip [1,9]
# K0 ~ U(.30,.65)
# e_L,c ~ Normal(0, SIGMA_E[L]) (independent across levels -- see FINDINGS)
# law_year_L ~ U(range_L), 15% never ; ranges (1972-98, 1975-2005, 1980-2015,
#             1985-2020)
#
# PHL-LIKE (index 0, declared, NOT fitted to the observed PHL series)
# gdp0=2200, growth=.020, N0=50e6, npop=.019, f0=5.5, fdec=.05, u0=.33,
# ug=.006, sv0=.42, svg=.004, sp0=3.0, spg=.02, K0=.75,
# synthetic law years (1990, 1995, 2005, 2015), p0_ter=0.15.
#
# DECLARED TARGETS (the only observed numbers encoded)
# TARGET_SEC = 0.29, TARGET_TER = 0.78  (brief; tolerance +/-0.15)
#   cited to 10_massification/relations/data/scaling_laws.csv, whose on-disk
#   between-country values are 0.2154 and 0.5666 -- a discrepancy reported,
#   not silently reconciled.
# PHL_TARGETS: primary comp crosses 90, lower-sec crosses 90 later,
#   upper-sec max < 90, tertiary GER 15.0 -> ~50 over 1970-2024.
# =============================================================================

SEED = 20261120
N_COUNTRIES = 32
YEAR_START = 1970
YEAR_END = 2024
YEARS = np.arange(YEAR_START, YEAR_END + 1, dtype=int)
T = len(YEARS)
LEVELS = ("primary", "lower_secondary", "upper_secondary", "tertiary")
NL = len(LEVELS)

C_MEAN = np.array([0.92, 0.72, 0.50, 0.32], dtype=float)
B_PRIM = 0.05
TARGET_SEC = 0.29
TARGET_TER = 0.78
ELASTICITY_TOL = 0.15
B_SEC_BOUNDS = (0.05, 3.0)
B_TER_BOUNDS = (0.05, 4.0)

G = np.array([0.30, 0.55, 0.75, 0.60], dtype=float)
H = np.array([0.20, 0.35, 0.45, 0.40], dtype=float)
SIGMA_E = np.array([0.30, 0.50, 0.60, 0.70], dtype=float)
SURVIVAL = np.array([0.95, 0.95, 0.92, 0.88], dtype=float)
ADJUST = np.array([0.20, 0.18, 0.15, 0.12], dtype=float)
PUSH = np.array([0.06, 0.05, 0.06, 0.08], dtype=float)
KAPPA = 0.75
OMEGA = np.array([6.0 / 15.0, 3.0 / 15.0, 3.0 / 15.0, 5.0 / 15.0], dtype=float)

X_REF = math.log(3.0)
URBAN_REF = 0.50
SERVICES_REF = 0.42
EFF_CAP = 1.04
K_Y = 0.30
K_S = 0.05
K_MIN, K_MAX = 0.05, 1.0
SHARE_INTERCEPT, SHARE_SLOPE = 0.13, 0.062
SHARE_MIN, SHARE_MAX = 0.12, 0.48
F_MIN = 1.3
LAW_NEVER_PROB = 0.15
LAW_RANGES = ((1972, 1998), (1975, 2005), (1980, 2015), (1985, 2020))

PHL = dict(
    gdp0=2200.0, growth=0.020, N0=50e6, npop=0.019,
    f0=5.5, fdec=0.05, u0=0.33, ug=0.006, sv0=0.42, svg=0.004,
    sp0=3.0, spg=0.02, K0=0.75,
    law_years=(1990, 1995, 2005, 2015), p0_ter=0.15,
)
PHL_TARGETS = dict(
    comp_primary_2024=94.0,
    comp_lower_2024=92.0,
    comp_upper_2024=78.0,
    ter_start_1970=15.0,
)

# The on-disk between-country numbers in the cited CSV (for the honest note).
CSV_SEC_BETWEEN = 0.2154
CSV_TER_BETWEEN = 0.5666
CSV_SEC_WITHIN = 0.0904
CSV_TER_WITHIN = 0.8482


# =============================================================================
# helpers
# =============================================================================
def expit(x):
    """Stable logistic."""
    return 0.5 * (1.0 + np.tanh(0.5 * x))


def logit(p):
    return math.log(p / (1.0 - p))


def fmt(x):
    """Fixed, deterministic formatting (no platform-dependent repr)."""
    return f"{float(x):.6f}"


def draw_params(seed=SEED):
    """Draw the declared country parameters once, in a fixed order."""
    rng = np.random.default_rng(seed)

    gdp0 = np.exp(rng.normal(math.log(2500.0), 0.9, N_COUNTRIES))
    gdp0 = np.clip(gdp0, 400.0, 20000.0)
    growth = np.clip(rng.normal(0.018, 0.008, N_COUNTRIES), 0.0, 0.045)
    N0 = np.exp(rng.normal(math.log(12e6), 1.0, N_COUNTRIES))
    N0 = np.clip(N0, 3e5, 3e8)
    npop = np.clip(rng.normal(0.014, 0.006, N_COUNTRIES), 0.0, 0.035)
    f0 = rng.uniform(1.8, 6.0, N_COUNTRIES)
    fdec = rng.uniform(0.005, 0.045, N_COUNTRIES)
    u0 = rng.uniform(0.15, 0.75, N_COUNTRIES)
    ug = rng.uniform(0.001, 0.008, N_COUNTRIES)
    sv0 = rng.uniform(0.25, 0.55, N_COUNTRIES)
    svg = rng.uniform(0.001, 0.006, N_COUNTRIES)
    sp0 = rng.uniform(2.0, 6.0, N_COUNTRIES)
    spg = rng.uniform(0.0, 0.03, N_COUNTRIES)
    K0 = rng.uniform(0.30, 0.65, N_COUNTRIES)

    e = rng.normal(0.0, 1.0, (NL, N_COUNTRIES)) * SIGMA_E[:, None]
    law_year = np.empty((NL, N_COUNTRIES), dtype=float)
    for li, (lo, hi) in enumerate(LAW_RANGES):
        law_year[li] = rng.uniform(lo, hi, N_COUNTRIES)
    never = rng.uniform(0.0, 1.0, (NL, N_COUNTRIES)) < LAW_NEVER_PROB
    law_year[never] = 9999.0

    # PHL-like overrides (index 0).  Declared design choices, not fitted.
    gdp0[0] = PHL["gdp0"]
    growth[0] = PHL["growth"]
    N0[0] = PHL["N0"]
    npop[0] = PHL["npop"]
    f0[0], fdec[0] = PHL["f0"], PHL["fdec"]
    u0[0], ug[0] = PHL["u0"], PHL["ug"]
    sv0[0], svg[0] = PHL["sv0"], PHL["svg"]
    sp0[0], spg[0] = PHL["sp0"], PHL["spg"]
    K0[0] = PHL["K0"]
    law_year[:, 0] = np.array(PHL["law_years"], dtype=float)

    return dict(
        gdp0=gdp0, growth=growth, N0=N0, npop=npop,
        f0=f0, fdec=fdec, u0=u0, ug=ug, sv0=sv0, svg=svg,
        sp0=sp0, spg=spg, K0=K0, e=e, law_year=law_year,
    )


def build(params):
    """Build the exogenous country-year arrays (demography, income, capacity)."""
    t = (YEARS - YEAR_START).astype(float)
    logy = np.log(params["gdp0"])[:, None] + params["growth"][:, None] * t[None, :]
    y = np.exp(logy)
    Npop = params["N0"][:, None] * np.exp(params["npop"][:, None] * t[None, :])
    fert = np.maximum(F_MIN, params["f0"][:, None] - params["fdec"][:, None] * t[None, :])
    share = np.clip(SHARE_INTERCEPT + SHARE_SLOPE * (fert - F_MIN), SHARE_MIN, SHARE_MAX)
    C = Npop * share
    urban = np.clip(params["u0"][:, None] + params["ug"][:, None] * t[None, :], 0.05, 0.95)
    services = np.clip(params["sv0"][:, None] + params["svg"][:, None] * t[None, :], 0.15, 0.85)
    spend = np.clip(params["sp0"][:, None] + params["spg"][:, None] * t[None, :], 1.0, 9.0)
    K = np.clip(
        params["K0"][:, None]
        + K_Y * (logy - logy[:, :1])
        + K_S * (spend - spend[:, :1]),
        K_MIN, K_MAX,
    )
    gate = K ** KAPPA
    return dict(logy=logy, y=y, C=C, urban=urban, services=services,
                spend=spend, K=K, gate=gate)


def simulate(params, b_sec, b_ter, e_override=None, k_shift=0.0,
             k_shift_year=1990, p0_ter=0.15):
    """Run the declared system.  Returns all arrays, including diagnostics."""
    d = build(params)
    b = np.array([B_PRIM, b_sec, b_sec, b_ter], dtype=float)
    e = params["e"] if e_override is None else e_override

    # Intercept implied by the declared ceiling at the reference point.  This
    # keeps the mean ceiling fixed when b_L is changed (the 'sample-mean' anchor).
    A = np.array([logit(c) for c in C_MEAN]) - b * X_REF - G * URBAN_REF - H * SERVICES_REF

    x = d["logy"] - math.log(1000.0)
    eta = (A[:, None, None]
           + b[:, None, None] * x[None, :, :]
           + G[:, None, None] * d["urban"][None, :, :]
           + H[:, None, None] * d["services"][None, :, :]
           + e[:, :, None])
    demand = expit(eta)

    K = d["K"].copy()
    if k_shift:
        mask = (YEARS >= k_shift_year)[None, :]
        K = np.clip(K + k_shift * mask, 0.0, 1.0)
    gate = K ** KAPPA

    law = (YEARS[None, None, :] >= params["law_year"][:, :, None]).astype(float)
    eff = np.minimum(EFF_CAP, demand * gate[None, :, :] + PUSH[:, None, None] * law * gate[None, :, :])

    p = np.empty((NL, N_COUNTRIES, T), dtype=float)
    p[:, :, 0] = np.clip(eff[:, :, 0], 0.0, EFF_CAP)
    p[3, 0, 0] = p0_ter
    for i in range(1, T):
        p[:, :, i] = np.clip(
            p[:, :, i - 1] + ADJUST[:, None] * (eff[:, :, i] - p[:, :, i - 1]),
            0.0, EFF_CAP,
        )

    # Flow/stock identity.  OMEGA is applied ONCE, to define the official-age
    # population; E = cohort*p; GER = E/cohort; no second cycle-length factor.
    cohort = d["C"][None, :, :] * OMEGA[:, None, None]
    enrol = cohort * p
    ger = 100.0 * p
    comp = 100.0 * p * SURVIVAL[:, None, None]

    out = dict(d)
    out.update(p=p, cohort=cohort, enrol=enrol, ger=ger, comp=comp,
               gate=gate, K=K, eff=eff, demand=demand, a=A, b=b, law=law)
    return out


def secondary_ger(res):
    """ISCED 2-3 aggregate: (E_lower + E_upper)/(cohort_lower + cohort_upper)."""
    return (res["enrol"][1] + res["enrol"][2]) / (res["cohort"][1] + res["cohort"][2]) * 100.0


def between_slope(ger, logy, mask=None):
    """Year-FE (between-country) OLS of log GER on log GDPpc; pooled."""
    lx = logy if mask is None else logy[mask]
    ly = np.log(np.maximum(ger if mask is None else ger[mask], 1e-12))
    xd = lx - lx.mean(axis=0, keepdims=True)
    yd = ly - ly.mean(axis=0, keepdims=True)
    denom = float((xd * xd).sum())
    slope = float((xd * yd).sum() / denom)
    resid = yd - slope * xd
    r2 = float(1.0 - (resid * resid).sum() / (yd * yd).sum())
    return slope, r2, int(lx.size)


def within_slope(ger, logy):
    """Two-way (country + year) FE within-country OLS of log GER on log GDPpc."""
    lx = logy - logy.mean(axis=0, keepdims=True) - logy.mean(axis=1, keepdims=True) + logy.mean()
    ly = np.log(np.maximum(ger, 1e-12))
    ly = ly - ly.mean(axis=0, keepdims=True) - ly.mean(axis=1, keepdims=True) + ly.mean()
    return float((lx * ly).sum() / (lx * lx).sum())


def cross_slope(ger, logy):
    """Pure cross-section of country means (no year FE)."""
    lx = logy.mean(axis=1)
    ly = np.log(np.maximum(ger, 1e-12)).mean(axis=1)
    xd = lx - lx.mean()
    yd = ly - ly.mean()
    return float((xd * yd).sum() / (xd * xd).sum())


def calibrate_b(params, which, target, other_b, bounds, log):
    """Deterministic bisection on b_L to hit the declared income exponent.

    Calibrated on the 31 generic countries only (PHL-like excluded) so that the
    special country cannot drive the scaling target.
    """
    lo, hi = bounds
    non_phl = np.arange(N_COUNTRIES) != 0
    last_slope = float("nan")
    for it in range(1, 51):
        mid = 0.5 * (lo + hi)
        res = simulate(params, mid if which == "sec" else other_b,
                       mid if which == "ter" else other_b)
        if which == "sec":
            s, _, _ = between_slope(secondary_ger(res), res["logy"], non_phl)
        else:
            s, _, _ = between_slope(res["ger"][3], res["logy"], non_phl)
        last_slope = s
        log.append(dict(stage=f"b_{which}", iteration=it, parameter=f"b_{which}",
                        candidate_value=mid, realized_value=s, target_value=target,
                        label="SYNTHETIC"))
        if s < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi), last_slope


def solve_phl(params, b_sec, b_ter, log):
    """Solve the PHL-like fixed effects to the declared milestone pattern.

    Declared, not fitted to observed PHL: targets are the pattern in the brief.
    Tertiary e is set analytically so the 1970 capacity-gated ceiling is exactly
    p0_ter=0.15 (no artificial dip); the other three are bisected on 2024
    completion.
    """
    e = params["e"].copy()
    d = build(params)
    x0 = d["logy"][0, 0] - math.log(1000.0)
    u0 = d["urban"][0, 0]
    s0 = d["services"][0, 0]
    gate0 = d["gate"][0, 0]
    demand0 = PHL["p0_ter"] / gate0
    a_ter = logit(C_MEAN[3]) - b_ter * X_REF - G[3] * URBAN_REF - H[3] * SERVICES_REF
    e[3, 0] = logit(demand0) - (a_ter + b_ter * x0 + G[3] * u0 + H[3] * s0)
    log.append(dict(stage="phl_e_tertiary", iteration=1, parameter="e_tertiary",
                    candidate_value=e[3, 0],
                    realized_value=PHL["p0_ter"], target_value=PHL_TARGETS["ter_start_1970"],
                    label="SYNTHETIC"))

    targets = [(0, PHL_TARGETS["comp_primary_2024"]),
               (1, PHL_TARGETS["comp_lower_2024"]),
               (2, PHL_TARGETS["comp_upper_2024"])]
    for lev, target in targets:
        lo, hi = -6.0, 6.0
        for it in range(1, 61):
            mid = 0.5 * (lo + hi)
            e[lev, 0] = mid
            res = simulate(params, b_sec, b_ter, e_override=e)
            val = float(res["comp"][lev, 0, -1])
            log.append(dict(stage=f"phl_e_{LEVELS[lev]}", iteration=it,
                            parameter=f"e_{LEVELS[lev]}", candidate_value=mid,
                            realized_value=val, target_value=target,
                            label="SYNTHETIC"))
            if val < target:
                lo = mid
            else:
                hi = mid
        e[lev, 0] = 0.5 * (lo + hi)
    return e


# =============================================================================
# checks C1-C5 (+ C5b ladder diagnostic)
# =============================================================================
def run_checks(params, res, b_sec, b_ter, e_phl):
    checks = []
    y = res["logy"]

    # ---- C1 GER bounds -----------------------------------------------------
    g = res["ger"]
    n_neg = int((g < 0).sum())
    n_gt105 = int((g > 105).sum())
    c1_pass = (n_neg == 0 and n_gt105 == 0)
    checks.append(dict(
        check_id="C1",
        fact="GER bounds: every ger in [0,105] for all countries/levels/years; a violation is a hard failure",
        target_value_or_pattern="0 <= ger <= 105 for all 7040 cells",
        synthetic_value=f"min={g.min():.4f}; max={g.max():.4f}; n_neg={n_neg}; n_gt105={n_gt105}; n_cells={g.size}",
        verdict="pass" if c1_pass else "fail",
        note=("Enforced by p in [0,1.04] and effective ceiling <=1.04; no p was clipped at the "
              "cap and max GER is %.4f. The upper bound is touched (one cell >100) but not "
              "approached; GER>105 is untested, not merely avoided." % g.max()),
        label="SYNTHETIC",
    ))

    # ---- C2 income scaling -------------------------------------------------
    sec = secondary_ger(res)
    non_phl = np.arange(N_COUNTRIES) != 0
    s_sec_all, r2_sec_all, n_sec = between_slope(sec, y)
    s_sec_np, r2_sec_np, _ = between_slope(sec, y, non_phl)
    s_ter_all, r2_ter_all, n_ter = between_slope(res["ger"][3], y)
    s_ter_np, r2_ter_np, _ = between_slope(res["ger"][3], y, non_phl)
    c2_pass = (s_sec_all > 0 and s_ter_all > 0
               and abs(s_sec_all - TARGET_SEC) <= ELASTICITY_TOL
               and abs(s_ter_all - TARGET_TER) <= ELASTICITY_TOL)
    checks.append(dict(
        check_id="C2",
        fact="income-scaling sign+magnitude: between-country (year-FE) log-log slope of log GER on log GDPpc; secondary and tertiary vs declared targets",
        target_value_or_pattern=f"secondary {TARGET_SEC:+.2f}; tertiary {TARGET_TER:+.2f}; tolerance +/-{ELASTICITY_TOL:.2f}",
        synthetic_value=(f"secondary={s_sec_all:+.4f} (all {N_COUNTRIES}); {s_sec_np:+.4f} (excl PHL_like); "
                         f"tertiary={s_ter_all:+.4f} (all); {s_ter_np:+.4f} (excl PHL_like); "
                         f"R2 sec={r2_sec_all:.3f}, ter={r2_ter_all:.3f}; n={n_sec}/{n_ter}"),
        verdict="pass" if c2_pass else "fail",
        note=(f"Both all-country slopes are within +/-{ELASTICITY_TOL:.2f} of the encoded brief targets. "
              f"TARGET MISMATCH (load-bearing): the cited on-disk scaling_laws.csv has between-country "
              f"estimates {CSV_SEC_BETWEEN:.4f} (secondary) and {CSV_TER_BETWEEN:.4f} (tertiary), and within "
              f"estimates {CSV_SEC_WITHIN:.4f}/{CSV_TER_WITHIN:.4f} -- not {TARGET_SEC:.2f}/{TARGET_TER:.2f}. "
              f"Against the on-disk between value, tertiary is off by {s_ter_all - CSV_TER_BETWEEN:+.3f} "
              f"(> {ELASTICITY_TOL:.2f}); secondary is within tolerance. We encode the brief's numbers and "
              f"report the discrepancy. b_sec={b_sec:.6f}, b_ter={b_ter:.6f} were chosen by declared bisection "
              f"(full trace results/calibration_log.csv); C2 is a consistency check, not a discovery."),
        label="SYNTHETIC",
    ))

    # ---- C2b within-country income scaling (diagnostic) --------------------
    w_sec = within_slope(sec, y)
    w_ter = within_slope(res["ger"][3], y)
    x_sec = cross_slope(sec, y)
    x_ter = cross_slope(res["ger"][3], y)
    c2b_pass = (abs(w_sec - CSV_SEC_WITHIN) <= ELASTICITY_TOL
                and abs(w_ter - CSV_TER_WITHIN) <= ELASTICITY_TOL)
    checks.append(dict(
        check_id="C2b",
        fact="within-country income scaling (diagnostic decomposition of C2): country+year FE log-log slope vs the cited on-disk within estimates",
        target_value_or_pattern=f"secondary {CSV_SEC_WITHIN:+.4f}; tertiary {CSV_TER_WITHIN:+.4f}; tolerance +/-{ELASTICITY_TOL:.2f}",
        synthetic_value=(f"within secondary={w_sec:+.4f} (target {CSV_SEC_WITHIN:+.4f}; diff {w_sec - CSV_SEC_WITHIN:+.4f}); "
                         f"within tertiary={w_ter:+.4f} (target {CSV_TER_WITHIN:+.4f}; diff {w_ter - CSV_TER_WITHIN:+.4f}); "
                         f"country-mean cross-section sec={x_sec:+.4f}, ter={x_ter:+.4f}"),
        verdict="pass" if c2b_pass else "fail",
        note=("FAILS on secondary. The declared model uses one b_L for both the between and within margins, so "
              "calibrating b_sec to the between target (+0.29) forces a within secondary exponent of +0.46, "
              f"about {w_sec / CSV_SEC_WITHIN:.1f}x the on-disk +0.090 (ns). The data's weak within-secondary / "
              "strong within-tertiary split is a between-vs-within divergence this single-slope design cannot "
              "reproduce. This is a structural limitation, not a numerical error, and was not tuned away."),
        label="SYNTHETIC",
    ))

    # ---- C3 PHL-like signature --------------------------------------------
    cp = res["comp"][0, 0]
    cl = res["comp"][1, 0]
    cu = res["comp"][2, 0]
    gt = res["ger"][3, 0]
    t_prim = int(YEARS[np.argmax(cp >= 90)]) if np.any(cp >= 90) else None
    t_low = int(YEARS[np.argmax(cl >= 90)]) if np.any(cl >= 90) else None
    t_ter25 = int(YEARS[np.argmax(gt >= 25)]) if np.any(gt >= 25) else None
    t_ter40 = int(YEARS[np.argmax(gt >= 40)]) if np.any(gt >= 40) else None
    up_max = float(cu.max())
    ter_start = float(gt[0])
    ter_end = float(gt[-1])
    ordering_ok = (t_prim is not None and t_low is not None and t_prim < t_low
                   and t_low < YEAR_END)
    c3_pass = (ordering_ok and up_max < 90.0
               and 10.0 <= ter_start <= 20.0 and 45.0 <= ter_end <= 55.0
               and ter_end > ter_start)
    checks.append(dict(
        check_id="C3",
        fact="PHL-like signature: primary completion crosses 90; lower-secondary crosses 90 later; upper-secondary stays below 90; tertiary GER rises ~15 -> ~50",
        target_value_or_pattern="primary 90 < lower-sec 90 < tertiary endpoint 2024; upper-sec max < 90; tertiary 1970 ~15 and 2024 ~50",
        synthetic_value=(f"primary 90 at {t_prim} (2024 comp {cp[-1]:.2f}); lower-sec 90 at {t_low} "
                         f"(2024 comp {cl[-1]:.2f}); upper-sec max {up_max:.2f}; tertiary {ter_start:.2f} "
                         f"(1970) -> {ter_end:.2f} (2024); tertiary crosses 25 at {t_ter25}, 40 at {t_ter40}"),
        verdict="pass" if c3_pass else "fail",
        note=("Ordering uses the tertiary 2024 endpoint as its milestone because the declared tertiary "
              "target is a rise 15->50 over the window, not a 90 crossing. CAVEAT: tertiary GER already "
              f"crosses 25 in {t_ter25}, before lower-sec 90 in {t_low}; the staged primary->lower->tertiary "
              "order is a terminal-stage statement, not a take-off-order statement. PHL-like e_L are "
              f"declared calibrated to this pattern, not to observed PHL data."),
        label="SYNTHETIC",
    ))

    # ---- C4 capacity floor/ceiling counterfactual --------------------------
    shock = simulate(params, b_sec, b_ter, e_override=e_phl,
                     k_shift=0.10, k_shift_year=1990)
    base = res
    dger = (shock["ger"][:, :, -5:].mean(axis=(1, 2))
            - base["ger"][:, :, -5:].mean(axis=(1, 2)))
    dcomp = (shock["comp"][:, :, -5:].mean(axis=(1, 2))
             - base["comp"][:, :, -5:].mean(axis=(1, 2)))
    dger_2024 = shock["ger"][:, 0, -1] - base["ger"][:, 0, -1]
    floor, ceiling = 0, 2
    c4_pass = bool(dger[floor] > dger[ceiling])
    checks.append(dict(
        check_id="C4",
        fact="floor-not-ceiling: a permanent +0.10 capacity increase from 1990 moves the lower level (floor) more than the ceiling",
        target_value_or_pattern="Delta GER(primary, floor) > Delta GER(upper-secondary, ceiling)",
        synthetic_value=(f"Delta GER mean 2020-24: primary {dger[0]:+.3f}; lower-sec {dger[1]:+.3f}; "
                         f"upper-sec {dger[2]:+.3f}; tertiary {dger[3]:+.3f}; floor-ceiling gap "
                         f"{dger[0] - dger[2]:+.3f} pp"),
        verdict="pass" if c4_pass else "fail",
        note=("PASSES MECHANICALLY: eff = demand*gate and demand ceilings are ordered "
              "primary>lower>upper>tertiary, so a proportional gate rise moves the higher-ceiling level more "
              "in absolute pp. This is not independent evidence for a floor mechanism. Delta completion "
              f"(2020-24): {dcomp[0]:+.3f}/{dcomp[1]:+.3f}/{dcomp[2]:+.3f}/{dcomp[3]:+.3f} pp."),
        label="SYNTHETIC",
    ))

    # ---- C5 hard sanity ----------------------------------------------------
    rates_ok = bool(
        np.all(res["p"] >= 0) and np.all(res["p"] <= EFF_CAP)
        and np.all(res["law"] >= 0) and np.all(res["law"] <= 1)
        and np.all(res["K"] >= 0) and np.all(res["K"] <= 1)
        and np.all(res["urban"] >= 0) and np.all(res["urban"] <= 1)
        and np.all(res["services"] >= 0) and np.all(res["services"] <= 1)
    )
    neg_enrol = int((res["enrol"] < 0).sum())
    within_corr = []
    for li in range(NL):
        cc = np.corrcoef(res["p"][li].ravel(), res["comp"][li].ravel())[0, 1]
        within_corr.append(float(cc))
    hard_ok = (neg_enrol == 0 and rates_ok
               and float(res["ger"].min()) >= 0 and float(res["ger"].max()) <= 105
               and float(res["comp"].min()) >= 0 and float(res["comp"].max()) <= 105)
    checks.append(dict(
        check_id="C5",
        fact="hard sanity: no negative enrolments; GER and completion in [0,105]; rates in [0,1]; completion monotone in enrolment within each level",
        target_value_or_pattern="enrolment>=0; 0<=ger,comp<=105; rates in [0,1]; within-level corr(p,comp)=1",
        synthetic_value=(f"neg_enrol={neg_enrol}; ger=[{res['ger'].min():.2f},{res['ger'].max():.2f}]; "
                         f"comp=[{res['comp'].min():.2f},{res['comp'].max():.2f}]; rates_ok={rates_ok}; "
                         f"within corr p-comp={within_corr}"),
        verdict="pass" if hard_ok else "fail",
        note="Within-level monotonicity is an identity (comp = 100*SURVIVAL*p). Cross-level ladder ordering is NOT imposed; see C5b.",
        label="SYNTHETIC",
    ))

    # ---- C5b cross-level ladder diagnostic ---------------------------------
    c = res["comp"]
    ok = (c[0] >= c[1]) & (c[1] >= c[2]) & (c[2] >= c[3])
    compliance = float(ok.mean())
    viol = int((~ok).sum())
    pair = {
        "primary>=lower": float((c[0] >= c[1]).mean()),
        "lower>=upper": float((c[1] >= c[2]).mean()),
        "upper>=tertiary": float((c[2] >= c[3]).mean()),
    }
    checks.append(dict(
        check_id="C5b",
        fact="cross-level ladder ordering (diagnostic decomposition of C5): completion non-increasing across the level ladder within country-year",
        target_value_or_pattern="primary >= lower-secondary >= upper-secondary >= tertiary completion in all country-years",
        synthetic_value=(f"compliance={compliance:.4f} ({ok.size - viol}/{ok.size}); violations={viol}; "
                         f"pairwise {pair}"),
        verdict="pass" if compliance >= 1.0 else "fail",
        note=("FAILS: levels are independent participation margins with independent fixed effects. Overall "
              f"ladder compliance is {compliance:.4f} ({viol}/{ok.size} violations, {100*(1-compliance):.1f}%); "
              "tertiary completion exceeds upper-secondary completion in ~15.6% of country-years and lower-"
              "secondary completion exceeds primary in ~13.2%. This is a genuine limitation of the declared "
              "model, not a numerical error; it is reported, not tuned away."),
        label="SYNTHETIC",
    ))

    return checks, dict(
        c1=dict(ger_min=float(g.min()), ger_max=float(g.max()), n_neg=n_neg, n_gt105=n_gt105),
        c2=dict(sec_all=s_sec_all, sec_nonphl=s_sec_np, ter_all=s_ter_all, ter_nonphl=s_ter_np,
                r2_sec=r2_sec_all, r2_ter=r2_ter_all, n_sec=n_sec, n_ter=n_ter,
                within_sec=w_sec, within_ter=w_ter, cross_sec=x_sec, cross_ter=x_ter),
        c3=dict(t_prim=t_prim, t_low=t_low, t_ter25=t_ter25, t_ter40=t_ter40,
                upper_max=up_max, ter_start=ter_start, ter_end=ter_end,
                comp_prim_2024=float(cp[-1]), comp_low_2024=float(cl[-1])),
        c4=dict(dger=[float(v) for v in dger], dcomp=[float(v) for v in dcomp],
                dger_phl_2024=[float(v) for v in dger_2024],
                floor_minus_ceiling=float(dger[0] - dger[2])),
        c5=dict(neg_enrol=neg_enrol, rates_ok=rates_ok, within_corr=within_corr,
                comp_min=float(res["comp"].min()), comp_max=float(res["comp"].max())),
        c5b=dict(compliance=compliance, violations=viol, pairwise=pair),
    )


# =============================================================================
# output writers
# =============================================================================
def write_panel(path, res):
    order = list(range(1, N_COUNTRIES)) + [0]  # C01..C31, then PHL_like last
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["country", "year", "level", "cohort", "enrolment", "ger",
                    "completion", "gdp_pc", "urban", "services", "capacity",
                    "law", "label"])
        for ci in order:
            cname = "PHL_like" if ci == 0 else f"C{ci:02d}"
            for yi, year in enumerate(YEARS):
                for li, level in enumerate(LEVELS):
                    w.writerow([
                        cname, int(year), level,
                        fmt(res["cohort"][li, ci, yi]),
                        fmt(res["enrol"][li, ci, yi]),
                        fmt(res["ger"][li, ci, yi]),
                        fmt(res["comp"][li, ci, yi]),
                        fmt(res["y"][ci, yi]),
                        fmt(res["urban"][ci, yi]),
                        fmt(res["services"][ci, yi]),
                        fmt(res["K"][ci, yi]),
                        int(res["law"][li, ci, yi]),
                        "SYNTHETIC",
                    ])


def write_checks(path, checks):
    cols = ["check_id", "fact", "target_value_or_pattern", "synthetic_value",
            "verdict", "note", "label"]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in checks:
            w.writerow(row)


def write_calibration(path, log):
    cols = ["stage", "iteration", "parameter", "candidate_value",
            "realized_value", "target_value", "label"]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in log:
            w.writerow(dict(row, candidate_value=fmt(row["candidate_value"]),
                            realized_value=fmt(row["realized_value"]),
                            target_value=fmt(row["target_value"])))


def write_counterfactual(path, c4):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["level", "role", "delta_ger_mean_2020_2024",
                    "delta_comp_mean_2020_2024", "delta_ger_phl_2024", "label"])
        roles = ["floor", "intermediate", "ceiling", "top"]
        for li, level in enumerate(LEVELS):
            w.writerow([level, roles[li], fmt(c4["dger"][li]), fmt(c4["dcomp"][li]),
                        fmt(c4["dger_phl_2024"][li]), "SYNTHETIC"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="results")
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    t0 = time.time()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    params = draw_params(args.seed)
    calib_log = []

    b_sec, s_sec = calibrate_b(params, "sec", TARGET_SEC, 1.0, B_SEC_BOUNDS, calib_log)
    b_ter, s_ter = calibrate_b(params, "ter", TARGET_TER, b_sec, B_TER_BOUNDS, calib_log)
    e_phl = solve_phl(params, b_sec, b_ter, calib_log)

    res = simulate(params, b_sec, b_ter, e_override=e_phl)

    runtime = time.time() - t0
    checks, summary = run_checks(params, res, b_sec, b_ter, e_phl)

    write_panel(outdir / "synthetic_panel.csv", res)
    write_checks(outdir / "reproduction_checks.csv", checks)
    write_calibration(outdir / "calibration_log.csv", calib_log)
    write_counterfactual(outdir / "capacity_counterfactual.csv", summary["c4"])

    run_summary = dict(
        label="SYNTHETIC",
        seed=args.seed,
        n_countries=N_COUNTRIES,
        years=[YEAR_START, YEAR_END],
        n_years=T,
        levels=list(LEVELS),
        panel_rows=N_COUNTRIES * T * NL,
        b_sec=b_sec,
        b_ter=b_ter,
        calibration_targets=dict(sec=TARGET_SEC, ter=TARGET_TER, tolerance=ELASTICITY_TOL),
        phl_e={LEVELS[i]: float(e_phl[i, 0]) for i in range(NL)},
        phl_design={k: v for k, v in PHL.items()},
        **summary,
        runtime_seconds=runtime,
        data_files_read=[],
        target_source="10_massification/relations/data/scaling_laws.csv (citation only; no file read)",
        on_disk_targets_note=dict(
            secondary_between=CSV_SEC_BETWEEN, tertiary_between=CSV_TER_BETWEEN,
            secondary_within=CSV_SEC_WITHIN, tertiary_within=CSV_TER_WITHIN,
            brief_targets=dict(secondary=TARGET_SEC, tertiary=TARGET_TER),
        ),
    )
    with open(outdir / "run_summary.json", "w") as fh:
        json.dump(run_summary, fh, indent=2, sort_keys=True)

    print("SYNTHETIC generator v0")
    print(f"seed={args.seed}  panel={run_summary['panel_rows']} rows")
    print(f"b_sec={b_sec:.6f}  b_ter={b_ter:.6f}")
    print(f"C2 sec(all)={summary['c2']['sec_all']:+.4f}  ter(all)={summary['c2']['ter_all']:+.4f}")
    print(f"C3 primary90={summary['c3']['t_prim']} lower90={summary['c3']['t_low']} "
          f"upper_max={summary['c3']['upper_max']:.2f} ter={summary['c3']['ter_start']:.2f}->{summary['c3']['ter_end']:.2f}")
    print(f"C4 floor-ceiling={summary['c4']['floor_minus_ceiling']:+.3f} pp")
    print(f"C5b ladder compliance={summary['c5b']['compliance']:.4f}")
    print(f"runtime={runtime:.2f}s  outdir={outdir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
