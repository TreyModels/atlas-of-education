#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIM_V1_3 -- SYNTHETIC generator v1.3: v1.2 + SHADOW EDUCATION AT THE GATES.

EVERYTHING THIS SCRIPT EMITS IS SYNTHETIC. It is a declared-assumption simulator: not an
estimate, not evidence about any country, not a forecast, and it licenses no causal or
direction claim. Country labels are synthetic ("SYN28", "SYN00_PHL_LIKE", ...); no real
country is modelled or measured.

Implements, on top of the frozen v1.2 generator (code/sim_v1_2.py, unchanged arithmetic),
the FROZEN shadow-module specification in shadow_module/PRE_DECLARATIONS.md (sha256
cf8c61cb...) and its binding controller note PRE_DECLARATIONS_S1_NOTE.md (sha256
af49a616...):

  * household tutoring demand at a gate, ONE behavioural rule for every country
    (a_g, b_Z, b_V, b_D, b_y, b_F, delta_g), country variation only through the declared
    input bundle (phi, s, sigma, nu);
  * gate pressure R built mechanically from v1.2's own queue/transition/rank state;
  * V the positional credential value; Delta-pi = delta_g (1 - pi0);
  * feedback: Pi replaces pi0 as the realised advance rate, one-year lag, bounded
    |Pi - pi0| <= delta_g (1 - pi0), touching nothing else in v1.2;
  * no passive "neither" sink (v1.2's out-of-school => work default is inherited);
  * g0 is the structural near-zero control, never scored as a gate, never in D*.

Frozen checks c1-c6 are scored exactly as PRE_DECLARATIONS.md sec.8 states. A FAIL is
reported as a FAIL; no parameter or threshold is ever adjusted to rescue one.

Determinism: one numpy PCG64 stream, seed 20261120 (inherited from v1.2), v1.2 draw order,
shadow block draws nothing, floats written at %.10g. Two clean runs into separate output
directories are byte-identical.

REFUSES TO RUN if the frozen shadow predeclaration, the S1 note, the inherited v1.2
predeclaration, the local verbatim copy, or PARAMS.md no longer match their frozen hashes.

Usage:  python sim_v1_3.py [--out DIR] [--manifest FILE] [--smoke] [--no-sensitivity]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import inspect
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np

LABEL = "SYNTHETIC"

# ======================================================================================
# 0. FROZEN IDENTITY, PANEL SHAPE AND PATHS
# ======================================================================================
SEED = 20261120
N_C = 30
YEAR_START, YEAR_END = 1970, 2025
YEARS = np.arange(YEAR_START, YEAR_END + 1)
T = YEARS.size
LEVELS = ("primary", "lower_secondary", "upper_secondary", "tertiary")
NL = 4
DVEC = np.array([6.0, 3.0, 3.0, 4.0])          # declared level durations (years)

ROOT = Path(__file__).resolve().parent.parent   # generator_v1_3/
CODE = Path(__file__).resolve()
SYNTH = ROOT.parent                             # synthetic_2026-11-20/
V12_DIR = SYNTH / "generator_v1_2"              # frozen v1.2 (read-only)
PREDECL = SYNTH / "v1_2" / "PRE_DECLARATIONS.md"          # frozen v1.2 spec (inherited)
SHADOW_DIR = SYNTH / "shadow_module"                      # frozen v1.3 spec (read-only)
SHADOW_PREDECL = SHADOW_DIR / "PRE_DECLARATIONS.md"
SHADOW_S1 = SHADOW_DIR / "PRE_DECLARATIONS_S1_NOTE.md"
LOCAL_PREDECL = ROOT / "PRE_DECLARATIONS.md"              # verbatim copy of both
PARAMS_MD = ROOT / "PARAMS.md"
V12_PANEL = V12_DIR / "results" / "synthetic_panel_v1_2.csv"
MASS = ROOT.parents[2]                          # 10_massification/
PROG = ROOT.parents[3]                          # massification-2026-11-20/
DATA = MASS / "data"
ECI_PATH = PROG / "09_relations" / "data" / "economic_complexity_panel_30ctys.csv"

# sha256 of v1_2/PRE_DECLARATIONS.md at freeze time (2026-11-20). If the file changes,
# the code refuses to run: the predeclaration is not edited after results are seen.
EXPECTED_PREDECL_SHA = "fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16"

# sha256 of the FROZEN v1.3 shadow spec and its binding controller note. These are the
# values recorded when the module was frozen, before any v1.3 run. A mismatch refuses.
EXPECTED_SHADOW_PREDECL_SHA = "cf8c61cb818cd63acfb2ada594bc9541bfcb0711f801e13b7eee3b86508f94f2"
EXPECTED_SHADOW_S1_SHA = "af49a616a7b57c4ef23a693c155d022cd17817f66f5acafba4dc6798dedb65eb"

# sha256 of PARAMS.md (the declared parameter table delivered with this module). Frozen
# before the scored run; DRY_RUN_PLAN.md sec.1.4 requires the run to re-hash it.
EXPECTED_PARAMS_SHA = "2b144985aa5b53a426afec0b9df8646ff3f49d803744dc0f2ae73778f22ff84d"

# Borrowed structural elements ONLY (no values, no priors, no posteriors, no targets):
BORROW = {
    "source": "engine/childworld.py at parent-repo HEAD "
              "(`git -C /Users/treymenefee/massification_live show HEAD:engine/childworld.py`)",
    "sha256": "ae73adb2a6d9c75d59966390e4304437479ff310a8724093e9108e9d26a23cab",
    "taken": ("the four-state set (school/both/work/neither), the household utility "
              "comparison and its parameter NAMES: y_med, w_child, farm, compat, v0, "
              "decay, cost, neither, girl_care, haz"),
    "not_taken": ("no childworld prior, posterior, calibrated value, country target or "
                  "output number enters as a parameter; its observation equation is NOT "
                  "the ILO child-labour definition and is not claimed to be"),
}

# ======================================================================================
# 1. DECLARED PARAMETERS  (human-readable mirror: PARAMS.md; authoritative copy is
#    dumped into RUN_MANIFEST.json at run time)
# ======================================================================================
P = {
    # ---- panel ---------------------------------------------------------------------
    "seed": SEED,
    "band_share": (0.42, 0.21, 0.20, 0.17),   # split of school-age cohort across levels
    # ---- Layer 1c: capacity, congestion, quality ------------------------------------
    "init_cover": (0.90, 0.55, 0.30, 0.08),   # 1970 adequate places / cohort, by level
    "seat_lag": (4, 5, 5, 6),                 # years: capacity responds to lagged base
    "seat_resp": (0.45, 0.40, 0.35, 0.30),    # annual convergence of seats to desired
    "cover_lo": (0.72, 0.55, 0.45, 0.10),     # adequate places / cohort, 1970 (declared)
    "cover_hi": (0.90, 1.25, 1.00, 0.85),     # adequate places / cohort, 2025 (declared)
    "seat_t50": (2003.0, 2024.0, 2010.0, 2000.0),  # declared build-out centre by level
    "seat_width": (12.0, 5.0, 10.0, 12.0),    # declared build-out width (logistic)
    "phys_cap": 1.15,                         # max pupils per adequate place (double shifts)
    "overage_cap": 1.05,                      # GER hard cap (Z1 gate)
    "oa_rate": (0.08, 0.06, 0.05, 0.04),      # over-age applicants / cohort
    "gamma": 0.55,                            # Q = exp(-gamma*max(0,q-1))
    "surv_max": (0.96, 0.91, 0.90, 0.90),     # survival at zero congestion
    "surv_theta": (1.0, 1.0, 1.0, 0.80),      # survival elasticity to Q
    "learn_theta": (1.0, 1.0, 1.0, 0.80),     # learning elasticity to Q
    "class_target": (40.0, 42.0, 42.0, 30.0),  # declared class size at q<=1
    # ---- teachers (reported PTR is a genuine stock ratio, built with a lag) ---------
    "ptr0": (24.0, 26.0, 26.0, 18.0),         # 1970 pupils per teacher
    "ptr_target": (33.0, 35.0, 34.0, 24.0),   # declared planning norm
    "teach_resp": (0.35, 0.30, 0.25, 0.20),   # annual convergence
    "teach_lag": (4, 5, 5, 6),                # hiring responds to lagged enrolment
    "teach_delivery_base": 0.35,
    "teach_delivery_gain": 0.65,
    # ---- Layer 2b: borrowed four-state block, DECLARED parameter ranges -------------
    "cost_base": (0.05, 0.14, 0.22),          # schooling cost by level (childworld form)
    "ration_work_share": 0.90,                # rationed children defaulting to work
    "hh_noise_sd": 0.015,                      # declared household-income shock (log)
    # ---- pipeline ------------------------------------------------------------------
    "pool_retain": 0.50,                      # carry-over of completed/over-age pool
    "init_pipe": (0.95, 0.75, 0.50, 0.15),    # 1970 eligible-pool size / cohort
    "init_comp": (0.55, 0.35, 0.15, 0.05),    # burn-in completion (cohort-flow)
    # ---- measurement convention (check d) ------------------------------------------
    "meas_completion_factor": 1.10,           # single declared constant m, all levels
    # ---- Layer 3: education -> complexity (Amendment A1) ---------------------------
    "x_income_coef": 0.55,
    "x_urban_coef": 0.55,
    "x_urban_ref": 0.40,
    "x_edu_level": 0.40,                      # X per unit lagged completion (level term)
    "x_edu_delta": 0.15,                      # X per unit change in completion (flow term)
    "x_persist": 0.50,                        # persistence of X around income/urban base
    "x_min": 0.0, "x_max": 2.40,
    "edu_lag": 10,                            # declared education->X lag (5-10)
    "x_off_sd": 0.16,
    # ---- literacy / takeoff (v1) ---------------------------------------------------
    "lit_learn": 0.05, "lit_lag": 12,
    "takeoff_lit": 0.60, "takeoff_income": 1500.0,
    "div_x": 0.95, "div_income": 6000.0,
    # ---- tertiary demand (adult, not part of the child block) ----------------------
    "t3_a": -2.02, "t3_b": 0.45, "t3_c": 0.60,
    "ter_pool_retain": 0.35,
    # ---- Layer 0/3 economy (ported from v1, declared) ------------------------------
    "lf_share_of_pop": 0.52,
    "sec_ag_base": 0.500, "sec_ag_x": -0.450,
    "sec_inf_base": 0.240, "sec_inf_x": -0.080,
    "sec_man_base": 0.130, "sec_man_x": 0.090,
    "sec_floors": (0.02, 0.05, 0.03, 0.05),
    "rung_a": (0.90, 0.40, -0.30, -1.30),
    "rung_b": (-0.65, 0.20, 1.00, 2.20),
    "x_open": (0.00, 0.08, 0.26, 0.48),
    "office_u_coef": (0.0, 0.35, 0.0, -0.20),
    "mfg_u_coef": (0.0, -0.10, 0.30, 0.10),
    "phi_formal": 0.82,
    "sep": (0.10, 0.07, 0.05, 0.04),
    "seek": (0.15, 0.35, 0.60, 0.80),
    "queue_retain": 0.50,
    "queue_max_lf": 0.20,
    "rank_gain": 0.20,
    "rung_mult": (2.20, 3.20, 4.60, 6.40),
    "cred_prem": 0.10,
    "psi_pre": 0.02, "psi_ind": 0.22, "psi_div": 0.12,
    "gp": (0.012, 0.008, 0.030, 0.022),
    "accel_ind": (1.0, 1.0, 1.6, 1.3),
    "accel_div": (1.0, 1.0, 1.3, 1.5),
    "comp_step": (0.10, 0.18, 0.32, 0.50),
    "lit_ag_growth": 0.010,
    "g_floor": 0.0, "g_cap": 0.090,
    "g_noise_sd": 0.006,
}

# Geometry constants of the borrowed household block (structural, not values).
NEED = 0.85
UTIL_SCALE = 0.3
GIRL_SHARE = 0.5
TASTE = 0.0
ABILITY = 0.0
OUT_YEARS = 0.0
AGE_W = (0.25, 0.70, 1.00)          # child earnings capacity by level age band
OFF = 16                            # history padding for lags


def sig(x):
    x = max(-30.0, min(30.0, float(x)))
    return 1.0 / (1.0 + math.exp(-x))


def clip(x, lo, hi):
    return max(lo, min(hi, float(x)))


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ======================================================================================
# 5b. SHADOW-EDUCATION DEMAND AT THE GATES  (v1.3 block)
#     Frozen spec: shadow_module/PRE_DECLARATIONS.md (sha256 cf8c61cb...) + S1 note.
#     LABEL: SYNTHETIC. ONE behavioural rule for every country; country variation enters
#     ONLY through the declared input bundle (phi, s, sigma, nu) from PARAMETERS.csv
#     C01-C12. No country-specific coefficient exists anywhere in this block (c4c audits
#     exactly that).
# ======================================================================================
GATES = (0, 1, 2, 3, 4)
GATE_NAMES = {0: "g0_PRE", 1: "g1_LS", 2: "g2_US", 3: "g3_TER", 4: "g4_JOB"}
GATE_LABEL = {0: "PRE-GATE (control, no positional good)",
              1: "GATE-LS lower-secondary entry",
              2: "GATE-US upper-secondary entry",
              3: "GATE-TER tertiary entry",
              4: "GATE-JOB credential -> formal rung"}
TYPE_ORDER = ("SYN_HKG_LIKE", "SYN_PHL_LIKE", "SYN_KHM_LIKE")
DECLARED_COMPARISON_YEAR = 2020          # t* (PRE_DECLARATIONS.md sec.8 c4a)

# Frozen central values, PRE_DECLARATIONS.md sec.6 / PARAMETERS.csv B01-B23.
# Keys are gates (0-4) only. A country key here would be the c4c violation.
SHADOW_BEHAV = dict(
    a_0=-4.80,
    a_g=-2.80,
    b_Z=2.00, b_V=1.00, b_D=2.00, b_y=0.60, b_F=0.80,
    delta={0: 0.02, 1: 0.30, 2: 0.30, 3: 0.25, 4: 0.20},
    w_Q=0.40, w_pi=0.40, w_kappa=0.20,
    r_EAP=0.087, H=20.0,
    dS={0: 0.0, 1: 3.0, 2: 3.0, 3: 4.0, 4: 0.0},
    omega=(0.20, 0.20, 0.20, 0.20, 0.20),
    zq=(-1.2816, -0.5244, 0.0, 0.5244, 1.2816),
)

# Declared country input bundles, PRE_DECLARATIONS.md sec.7 / PARAMETERS.csv C01-C12.
# These are the ONLY country-varying quantities. Same a, b, delta for every type.
SHADOW_COUNTRY_INPUTS = {
    "SYN_HKG_LIKE": dict(phi=0.940, s=0.0305, sigma=0.55,
                         nu={1: 0.10, 2: 0.62, 3: 0.22}, oos_upper=5.428),
    "SYN_PHL_LIKE": dict(phi=0.677, s=0.0400, sigma=0.80,
                         nu={1: 0.30, 2: 0.35, 3: 0.10}, oos_upper=24.737),
    "SYN_KHM_LIKE": dict(phi=0.464, s=0.0210, sigma=0.75,
                         nu={1: 0.28, 2: 0.13, 3: 0.02}, oos_upper=56.987),
}


def shadow_inputs_named():
    """Deep copy of the declared input bundles (so a sensitivity run cannot mutate them)."""
    return {k: {kk: (dict(vv) if isinstance(vv, dict) else vv) for kk, vv in v.items()}
            for k, v in SHADOW_COUNTRY_INPUTS.items()}


def shadow_beh_variant(**over):
    """One-at-a-time variant of the frozen block (pre-declared sensitivity only)."""
    beh = dict(SHADOW_BEHAV)
    beh["delta"] = dict(SHADOW_BEHAV["delta"])
    beh["dS"] = dict(SHADOW_BEHAV["dS"])
    beh["omega"] = tuple(SHADOW_BEHAV["omega"])
    beh["zq"] = tuple(SHADOW_BEHAV["zq"])
    for k, v in over.items():
        if k == "delta" and isinstance(v, dict):
            beh["delta"].update(v)
        else:
            beh[k] = v
    return beh


def resolve_hosts(results):
    """Declared, shadow-blind host rule (IMPLEMENTATION_NOTE.md sec.1).

    SYN_HKG_LIKE <- the synthetic country with the highest 2020 GDP per capita
    SYN_PHL_LIKE <- v1.2's own declared PHL-informed country (PARAMS.md sec.9)
    SYN_KHM_LIKE <- the synthetic country with the lowest 2020 GDP per capita

    GDP per capita is a v1.2 state variable and is NOT an argument of the demand
    equation (SHADOW_MODULE.md sec.4). The rule never reads D, R or any check value.
    """
    t20 = int(np.where(YEARS == DECLARED_COMPARISON_YEAR)[0][0])
    gdp = [(float(r["Y"][t20]), i, r["cp"]["name"]) for i, r in enumerate(results)]
    hi = max(gdp, key=lambda x: (x[0], -x[1]))
    lo = min(gdp, key=lambda x: (x[0], x[1]))
    hosts = {"SYN_HKG_LIKE": hi[2], "SYN_PHL_LIKE": "SYN00_PHL_LIKE", "SYN_KHM_LIKE": lo[2]}
    if len(set(hosts.values())) != 3:
        raise SystemExit("REFUSING: host rule produced non-distinct countries: %r" % (hosts,))
    return hosts, {n: v for v, _, n in gdp}


def gate_numbers(beh, cand, cap, adv, kappa):
    """Frozen R definition (PRE_DECLARATIONS.md sec.4.1): Q, pi0, kappa, R + components."""
    Q = min(max(float(cand) / max(float(cap), 1e-9), 0.0), 10.0)
    pi0 = min(max(float(adv) / max(float(cand), 1e-9), 0.01), 0.999)
    k = min(max(float(kappa), 1.0), 5.0)
    R = (1.0 + Q) ** beh["w_Q"] * (1.0 / pi0) ** beh["w_pi"] * k ** beh["w_kappa"]
    R = min(max(R, 1.0), 20.0)
    return dict(Q=Q, pi0=pi0, kappa=k, R=R, candidates=float(cand),
                capacity=float(cap), advances=float(adv))


def gate_state(cand_c, cap_c, grads, enrol, rankf, queue_r, vac, hires, beh):
    """Gate-state contract, DRY_RUN_PLAN.md sec.1.3 mapped onto v1.2 state.

    g0 pre-gate : candidates = primary cohort, capacity = primary seats, advances =
                  primary official-age admissions, kappa = 1 (no credential rank).
    g1..g3      : candidates = graduates of the level below, capacity = the model's own
                  physical admission capacity phys = min(phys_cap*seats, overage_cap*C),
                  advances = admissions (enrol), kappa = rank factor at the rung.
    g4 job gate : candidates = queue + hires over rungs 1-3, capacity = vacancies,
                  advances = hires, kappa = hires-weighted mean rank factor.
    """
    gs = {}
    gs[1] = gate_numbers(beh, grads[0], cap_c[1], enrol[1], rankf[0])
    gs[2] = gate_numbers(beh, grads[1], cap_c[2], enrol[2], rankf[1])
    gs[3] = gate_numbers(beh, grads[2], cap_c[3], enrol[3], rankf[2])
    cand4 = sum(float(queue_r[i]) + float(hires[i]) for i in (1, 2, 3))
    cap4 = sum(float(vac[i]) for i in (1, 2, 3))
    adv4 = sum(float(hires[i]) for i in (1, 2, 3))
    wh = sum(float(hires[i]) for i in (1, 2, 3))
    if wh > 1e-12:
        k4 = sum(float(hires[i]) * float(rankf[i]) for i in (1, 2, 3)) / wh
    else:
        k4 = 1.0
    gs[4] = gate_numbers(beh, cand4, cap4, adv4, k4)
    gs[0] = gate_numbers(beh, cand_c[0], cap_c[0], enrol[0], 1.0)
    return gs


def gate_state_from_run(r, t, beh):
    """Convenience wrapper for the checks: gate state of a stored run at year index t."""
    C = r["C"]
    cap_c = [min(P["phys_cap"] * r["seats"][L, t], P["overage_cap"] * C[L, t])
             for L in range(NL)]
    return gate_state(C[:, t], cap_c, r["grads"][:, t], r["enrol"][:, t],
                      r["rankf"][:, t], r["queue_r"][:, t], r["vac"][:, t],
                      r["hires"][:, t], beh)


def credential_value(beh, phi, gate, w_for_t=None, w_inf_t=None):
    """Frozen V (PRE_DECLARATIONS.md sec.4.2): positional value of the credential."""
    if gate == 0:
        return 0.0                      # no gate, no positional good (sec.4.2, c3)
    if gate == 4:
        G = math.log(max(float(w_for_t[1]), 1e-12) / max(float(w_inf_t), 1e-12))
        return phi * G * beh["H"]       # formal-rung wage-gap form (PARAMETERS.csv B21)
    return phi * beh["r_EAP"] * beh["dS"][gate] * beh["H"]


def shadow_quintile_income(beh, sigma):
    """Declared lognormal lay-out at the five quintile midpoints, mean-normalised."""
    raw = [math.exp(sigma * z) for z in beh["zq"]]
    m = sum(raw) / len(raw)
    return [x / m for x in raw]


def shadow_demand(beh, phi, s, sigma, R, V, dpi, gate, lnR_shift=0.0, V_mult=1.0):
    """The FROZEN demand equation (PRE_DECLARATIONS.md sec.4). Pure, no I/O, no RNG.

    p_q = sigma( a_g + b_Z ln R + b_V ln(1+V) + b_D ln(1+dpi) + b_y ln(y_q/ybar)
                 - b_F ln(1 + s/(y_q/ybar)) )
    D   = sum_q omega_q p_q
    """
    a = beh["a_0"] if gate == 0 else beh["a_g"]
    Vv = max(0.0, float(V)) * float(V_mult)
    lnR = math.log(max(float(R), 1e-12)) + float(lnR_shift)
    ln1pV = math.log1p(Vv)
    ln1pd = math.log1p(max(float(dpi), 0.0))
    ys = shadow_quintile_income(beh, sigma)
    ps, ths = [], []
    for yq in ys:
        th = (a + beh["b_Z"] * lnR + beh["b_V"] * ln1pV + beh["b_D"] * ln1pd
              + beh["b_y"] * math.log(yq) - beh["b_F"] * math.log1p(float(s) / yq))
        ths.append(th)
        ps.append(sig(th))
    D = sum(w * p for w, p in zip(beh["omega"], ps))
    return D, ps, ths, ys


def shadow_block(beh, ci, gs, w_for_t, w_inf_t):
    """One country-year of the shadow block: D, S, pi0, pi1, Pi, R, V, s, p_q.

    Pure: reads the gate state and the declared input bundle, returns numbers.
    """
    out = {}
    for g in GATES:
        Vraw = credential_value(beh, ci["phi"], g, w_for_t, w_inf_t)
        V = max(0.0, Vraw)
        pi0 = gs[g]["pi0"]
        pi1 = min(0.999, pi0 + beh["delta"][g] * (1.0 - pi0))
        dpi = pi1 - pi0
        D, ps, ths, ys = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"],
                                       gs[g]["R"], V, dpi, g)
        Pi = (1.0 - D) * pi0 + D * pi1
        out[g] = dict(D=D, ps=ps, thetas=ths, ys=ys, V=V, V_raw=Vraw,
                      V_clipped=(Vraw < 0.0), pi0=pi0, pi1=pi1, dpi=dpi, Pi=Pi,
                      R=gs[g]["R"], Q=gs[g]["Q"], kappa=gs[g]["kappa"],
                      S=D * ci["s"], ratio=Pi / max(pi0, 1e-12),
                      candidates=gs[g]["candidates"], capacity=gs[g]["capacity"],
                      advances=gs[g]["advances"])
    return out


# ======================================================================================
# 2. DECLARED INPUTS (observed paths enter ONLY here; never fitted at runtime)
# ======================================================================================
def load_observed_phl_paths():
    """Read the observed PHL cohort/population path (Layer 1b declared input) and the
    observed capacity/PTR series (rationale + benchmark only)."""
    import csv

    def read_csv(path):
        with open(path, newline="") as fh:
            return list(csv.DictReader(fh))

    uni = read_csv(DATA / "UNIVERSALIZATION_SERIES.csv")
    phl = [r for r in uni if r.get("iso3") == "PHL"]
    def series(ind):
        d = {}
        for r in phl:
            if r["indicator"] == ind:
                try:
                    d[int(float(r["year"]))] = float(r["value"])
                except (ValueError, TypeError):
                    pass
        return d

    coh = series("cohort_population_0_14")
    pop = series("population_total")
    if min(coh) > 1995 or max(coh) < 2024:
        raise SystemExit("REFUSING: observed PHL cohort series missing expected coverage")
    # declared backward/forward extrapolation of the observed path (inputs, not fits)
    S = np.empty(T)
    for i, y in enumerate(YEARS):
        if y in coh:
            S[i] = coh[y]
        elif y < min(coh):
            S[i] = coh[min(coh)] / (1.0245 ** (min(coh) - y))
        else:
            S[i] = coh[max(coh)] * (1.0 - 0.008) ** (y - max(coh))
    Ppop = np.empty(T)
    for i, y in enumerate(YEARS):
        if y in pop:
            Ppop[i] = pop[y]
        elif y < min(pop):
            Ppop[i] = pop[min(pop)] / (1.025 ** (min(pop) - y))
        else:
            Ppop[i] = pop[max(pop)] * (1.0 + 0.010) ** (y - max(pop))

    # observed PTR / spending benchmarks (diagnostic only -- never encoded)
    sc = read_csv(DATA / "STATE_CAPACITY.csv")
    ptr_obs = {}
    spend_obs = {}
    for r in sc:
        if r.get("iso3") != "PHL":
            continue
        try:
            y = int(float(r["year"])); v = float(r["value"])
        except (ValueError, TypeError):
            continue
        if r["indicator"] == "pupil-teacher ratio, primary":
            ptr_obs[y] = v
        elif r["indicator"] == "education spending (% of GDP), WDI":
            spend_obs[y] = v
    return S, Ppop, coh, ptr_obs, spend_obs


# ======================================================================================
# 3. SYNTHETIC COUNTRY PARAMETERISATION
# ======================================================================================
def draw_countries(rng):
    cps = []
    for i in range(N_C):
        y0 = float(math.exp(rng.normal(math.log(2500.0), 0.80)))
        base = math.log(max(y0, 400.0) / 1000.0)
        lit0 = float(np.clip(0.10 + 0.60 * (base / 1.6) + rng.normal(0.0, 0.08), 0.05, 0.96))
        cps.append(dict(
            idx=i, name=f"SYN{i:02d}", y0=y0,
            pop0=float(math.exp(rng.normal(math.log(18e6), 0.70))),
            npop=float(np.clip(rng.normal(0.016, 0.005), 0.002, 0.032)),
            S0=float(math.exp(rng.normal(math.log(14e6), 0.70))),
            g0=float(np.clip(rng.normal(0.022, 0.005), 0.004, 0.042)),
            g1=float(np.clip(rng.normal(0.015, 0.006), 0.000, 0.034)),
            g2=float(np.clip(rng.normal(0.008, 0.007), -0.016, 0.026)),
            u0=float(np.clip(rng.uniform(0.12, 0.78), 0.05, 0.95)),
            ug=float(rng.uniform(0.001, 0.007)),
            lit0=lit0,
            xoff=float(rng.normal(0.0, P["x_off_sd"])),
            ag_off=float(rng.normal(0.0, 0.06)),
            inf_off=float(rng.normal(0.0, 0.05)),
            man_off=float(rng.normal(0.0, 0.04)),
            office_bias=float(rng.normal(0.0, 0.55)),
            mfg_bias=float(rng.normal(0.0, 0.55)),
            cap0=float(np.clip(rng.normal(1.0, 0.08), 0.80, 1.20)),
            dshift=float(rng.normal(0.0, 6.0)),
            y_med=float(rng.uniform(0.90, 1.80)),
            w_child=float(rng.uniform(0.10, 0.35)),
            farm=float(rng.uniform(0.10, 0.60)),
            compat=float(rng.uniform(0.25, 0.75)),
            v0=float(rng.uniform(1.20, 2.20)),
            decay=float(rng.uniform(0.62, 0.80)),
            cost=float(rng.uniform(0.80, 1.80)),
            neither=float(rng.uniform(-1.20, -0.60)),
            girl_care=float(rng.uniform(0.05, 0.35)),
            haz=float(rng.uniform(0.10, 0.40)),
        ))
    return cps


def apply_declared(cps):
    """Declared country traits. These are NOT supply-rule overrides: every country,
    including SYN00, passes through the same supply functions. Only traits that also
    exist (drawn) for the other 27 countries are set here."""
    phl = cps[0]
    phl.update(dict(
        name="SYN00_PHL_LIKE", y0=2000.0, pop0=35.8e6, npop=0.0173,
        u0=0.33, ug=0.0045, lit0=0.83, xoff=0.10,
        ag_off=-0.03, inf_off=0.08, man_off=-0.03,
        office_bias=-1.20, mfg_bias=-0.80,
        cap0=1.00, dshift=0.0,
        y_med=1.30, w_child=0.28, farm=0.25, compat=0.50,
        v0=1.70, decay=0.68, cost=1.00, neither=-0.90, girl_care=0.20, haz=0.25,
    ))
    twin_common = dict(
        y0=2600.0, pop0=20e6, npop=0.014, S0=18e6,
        g0=0.018, g1=0.014, g2=0.009,
        u0=0.42, ug=0.004, lit0=0.72, xoff=0.05, cap0=1.00, dshift=0.0,
        y_med=1.35, w_child=0.28, farm=0.30, compat=0.50,
        v0=1.70, decay=0.68, cost=1.00, neither=-0.90, girl_care=0.20, haz=0.25,
    )
    cps[1].update(twin_common)
    cps[1].update(dict(name="SYN01_TWIN_MFG", ag_off=0.0, inf_off=-0.03, man_off=0.07,
                       office_bias=-0.30, mfg_bias=0.80))
    cps[2].update(twin_common)
    cps[2].update(dict(name="SYN02_TWIN_OFFICE", ag_off=0.0, inf_off=0.02, man_off=-0.06,
                       office_bias=0.80, mfg_bias=-0.30))
    variant_common = dict(
        y0=2200.0, pop0=20e6, npop=0.014, S0=20e6, g0=0.020, g1=0.015, g2=0.008,
        u0=0.35, ug=0.004, lit0=0.70, xoff=0.00, cap0=1.00, dshift=0.0,
        ag_off=0.0, inf_off=0.0, man_off=0.0, office_bias=0.0, mfg_bias=0.0,
        y_med=1.35, w_child=0.28, farm=0.30, compat=0.50,
        v0=1.70, decay=0.68, cost=1.00, neither=-0.90, girl_care=0.20, haz=0.25,
    )
    for k, nm in ((10, "SYN10_BOOM"), (11, "SYN11_FLAT"), (12, "SYN12_DECLINE")):
        cps[k].update(variant_common)
        cps[k]["name"] = nm
    return cps


def cohort_path(cp, phl_S):
    name = cp["name"]
    if name == "SYN00_PHL_LIKE":
        return phl_S.copy()
    if name == "SYN10_BOOM":
        return cp["S0"] * (phl_S / phl_S[0])
    if name == "SYN11_FLAT":
        return np.full(T, cp["S0"], dtype=float)
    if name == "SYN12_DECLINE":
        return cp["S0"] * (1.0 - 0.009) ** np.arange(T, dtype=float)
    s = np.empty(T)
    s[0] = cp["S0"]
    for t in range(1, T):
        y = YEARS[t]
        g = cp["g0"] if y < 1985 else (cp["g1"] if y < 2005 else cp["g2"])
        s[t] = s[t - 1] * (1.0 + g)
    return s


def pop_path(cp, phl_P):
    if cp["name"] == "SYN00_PHL_LIKE":
        return phl_P.copy()
    return cp["pop0"] * (1.0 + cp["npop"]) ** np.arange(T, dtype=float)


# ======================================================================================
# 4. THE SINGLE SUPPLY RULE (no country identity enters this code)
# ======================================================================================
def coverage_target(lo, hi, buildout):
    """Declared coverage target as a function of the country's build-out level."""
    return lo + (hi - lo) * buildout


def desired_capacity(cover, base):
    """Desired adequate places: coverage target times the declared capacity base."""
    return cover * base


def update_seats(seats_prev, desired, resp):
    """Seats adjust partially toward the desired level (the declared lag)."""
    return max(0.0, seats_prev + resp * (desired - seats_prev))


# ======================================================================================
# 5. LAYER 2b -- BORROWED FOUR-STATE HOUSEHOLD BLOCK (structure only)
# ======================================================================================
def state_shares(cp, level, y_shock):
    """Shares over {school, both, work, neither}. Utility form and parameter names are
    BORROWED-FROM-ATLAS / structural (childworld). Values are our declared draws.
    Representative household: ability=0, taste=0, half girls."""
    y = cp["y_med"] * math.exp(y_shock)

    def util(c):
        x = c - 0.6 * NEED
        if x > 0.05:
            return math.log(max(x, 1e-9))
        return math.log(0.05) + (x - 0.05) / 0.05

    earn = 0.32 * AGE_W[level] * max(cp["w_child"] / 0.32, 0.55 * cp["farm"])
    cost = cp["cost"] * P["cost_base"][level]
    v_l = cp["v0"] * cp["decay"] ** level + 0.25 * ABILITY - 1.3 * min(OUT_YEARS, 3) / 3.0
    U = np.array([
        util(y - cost) + v_l,
        util(y - cost + 0.5 * (1.0 + cp["compat"]) * earn)
        + v_l * (0.72 + 0.2 * cp["compat"]) + 0.4 * cp["compat"] - 0.25,
        util(y + earn) - 0.2 * TASTE,
        util(y) + cp["neither"] + cp["girl_care"] * GIRL_SHARE,
    ])
    Pr = np.exp((U - U.max()) / UTIL_SCALE)
    Pr /= Pr.sum()
    return Pr


# ======================================================================================
# 6. ONE COUNTRY, 1970-2025
# ======================================================================================
def simulate_country(cp, gnoise, hhnoise, S_path, Pop_path, sh_in=None, beh=None):
    band = np.array(P["band_share"])
    floors = np.array(P["sec_floors"])
    rung_a = np.array(P["rung_a"]); rung_b = np.array(P["rung_b"])
    off_u = np.array(P["office_u_coef"]); mfg_u = np.array(P["mfg_u_coef"])
    sepr = np.array(P["sep"]); seek = np.array(P["seek"])
    mult = np.array(P["rung_mult"]); comp_step = np.array(P["comp_step"])
    gp = np.array(P["gp"])
    cap = cp["cap0"]
    beh = SHADOW_BEHAV if beh is None else beh
    ratio_prev = np.ones(5)          # v1.3: Pi/pi0 carried to the next year's pool (lag 1)

    C = band[:, None] * S_path[None, :] / DVEC[:, None]
    U = np.clip(cp["u0"] + cp["ug"] * np.arange(T), 0.05, 0.95)
    Pop = Pop_path

    buildout = np.zeros((NL, T))
    for L in range(NL):
        buildout[L] = 1.0 / (1.0 + np.exp(
            -(YEARS - (P["seat_t50"][L] + cp["dshift"])) / P["seat_width"][L]))

    # ---- storage -------------------------------------------------------------------
    out = dict(
        seats=np.zeros((NL, T)), teachers=np.zeros((NL, T)), ptr=np.zeros((NL, T)),
        q=np.zeros((NL, T)), Q=np.zeros((NL, T)), cls=np.zeros((NL, T)),
        ger=np.zeros((NL, T)), intake_off=np.zeros((NL, T)), intake_oa=np.zeros((NL, T)),
        enrol=np.zeros((NL, T)), oos=np.zeros((NL, T)), oos_rate=np.zeros((NL, T)),
        comp_coh=np.zeros((NL, T)), comp_uis=np.zeros((NL, T)), surv=np.zeros((NL, T)),
        grads=np.zeros((NL, T)), demand_share=np.zeros((NL, T)),
        demand_off=np.zeros((NL, T)), demand_oa=np.zeros((NL, T)),
        rationed=np.zeros((NL, T)), elig=np.zeros((NL, T)), pool=np.zeros((NL, T)),
        p_school=np.zeros((NL, T)), p_both=np.zeros((NL, T)),
        p_work=np.zeros((NL, T)), p_neither=np.zeros((NL, T)),
        work_final=np.zeros((NL, T)), neither_final=np.zeros((NL, T)),
        both_final=np.zeros((NL, T)), child_labour=np.zeros((NL, T)),
        Y=np.zeros(T), X=np.zeros(T), lit=np.zeros(T), Tstate=np.zeros(T, dtype=np.int8),
        sec=np.zeros((4, T)), J=np.zeros((4, T)), sh=np.zeros((4, T)),
        E=np.zeros((4, T)), vac=np.zeros((4, T)), queue_r=np.zeros((4, T)),
        queue_tot=np.zeros(T), rankf=np.zeros((4, T)), w_inf=np.zeros(T),
        w_for=np.zeros((4, T)), g=np.zeros(T), yos=np.zeros(T), att=np.zeros((NL, T)),
        public_ptr=np.zeros(T),
        # ---- v1.3 shadow block stores (diagnostics/state; no v1.2 quantity above changes)
        hires=np.zeros((4, T)),
        D_sh=np.zeros((5, T)), S_sh=np.zeros((5, T)), R_sh=np.zeros((5, T)),
        Q_sh=np.zeros((5, T)), pi0_sh=np.zeros((5, T)), pi1_sh=np.zeros((5, T)),
        Pi_sh=np.zeros((5, T)), kappa_sh=np.zeros((5, T)), V_sh=np.zeros((5, T)),
        dpi_sh=np.zeros((5, T)), ratio_sh=np.ones((5, T)), p_sh=np.zeros((5, 5, T)),
        cand_sh=np.zeros((5, T)), cap_sh=np.zeros((5, T)), adv_sh=np.zeros((5, T)),
    )

    # ---- initial state -------------------------------------------------------------
    Y = cp["y0"]
    lit = cp["lit0"]
    Tcur = 1 if (lit >= P["takeoff_lit"] and Y >= P["takeoff_income"]) else 0
    X = clip(P["x_income_coef"] * math.log(Y / 1000.0)
             + P["x_urban_coef"] * (U[0] - P["x_urban_ref"]) + cp["xoff"],
             P["x_min"], P["x_max"])
    X_prev = X
    xbase_prev = X

    def sectors_of(x):
        a = P["sec_ag_base"] + P["sec_ag_x"] * (x - 0.6) + cp["ag_off"]
        i = P["sec_inf_base"] + P["sec_inf_x"] * (x - 0.6) + cp["inf_off"]
        m = P["sec_man_base"] + P["sec_man_x"] * (x - 0.6) + cp["man_off"]
        s = 1.0 - a - i - m
        v = np.maximum(np.array([a, i, m, s]), floors)
        for _ in range(60):
            d = 1.0 - v.sum()
            if abs(d) < 1e-14:
                break
            if d > 0:
                v = v + d * (v / v.sum())
            else:
                slack = v - floors
                tot = slack.sum()
                if tot <= 1e-14:
                    break
                v = v - min(-d, tot) * (slack / tot)
            v = np.maximum(v, floors)
        return v / v.sum()

    LF0 = P["lf_share_of_pop"] * Pop[0]
    sec0 = sectors_of(X)
    u0v = rung_a + rung_b * (X - 0.6) + off_u * cp["office_bias"] + mfg_u * cp["mfg_bias"]
    for r in range(4):
        if X < P["x_open"][r]:
            u0v[r] = -1e9
    w0 = np.exp(u0v - u0v.max()); w0 = w0 / w0.sum()
    E_r = 0.85 * P["phi_formal"] * (sec0[2] + sec0[3]) * LF0 * w0
    prevE = E_r.copy()
    queue_carry = np.zeros(4)

    seats = np.array([P["init_cover"][L] * cap * C[L, 0] for L in range(NL)])
    teachers = np.array([max(1.0, seats[L] / P["ptr0"][L]) for L in range(NL)])
    pools = np.array([P["init_pipe"][L] * C[L, 0] for L in range(NL)])

    # history buffers (prefilled at the declared initial steady state)
    adm_hist = np.zeros((NL, T + OFF))
    adm_p_hist = np.zeros((NL, T + OFF))
    grads_hist = np.zeros((NL, T + OFF))
    enrol_hist = np.zeros((NL, T + OFF))
    comp_hist = np.zeros(T + OFF)
    for L in range(NL):
        for k in range(OFF):
            adm_hist[L, k] = P["init_comp"][L]
            adm_p_hist[L, k] = P["init_comp"][L] * C[L, 0]
            grads_hist[L, k] = P["init_comp"][L] * C[L, 0]
            enrol_hist[L, k] = P["init_cover"][L] * C[L, 0]
    for k in range(OFF):
        comp_hist[k] = P["init_comp"][0]

    for t in range(T):
        # ---- X: education -> complexity channel (Amendment A1) ---------------------
        lag_idx = OFF + t - P["edu_lag"]
        flow = comp_hist[lag_idx]
        dflow = comp_hist[lag_idx] - comp_hist[lag_idx - 1]
        xbase = (P["x_income_coef"] * math.log(max(Y, 100.0) / 1000.0)
                 + P["x_urban_coef"] * (U[t] - P["x_urban_ref"]) + cp["xoff"])
        X = clip(xbase + P["x_edu_level"] * flow
                 + P["x_edu_delta"] * dflow
                 + P["x_persist"] * (X_prev - xbase_prev),
                 P["x_min"], P["x_max"])

        # ---- takeoff -----------------------------------------------------------------
        if Tcur == 0 and lit >= P["takeoff_lit"] and Y >= P["takeoff_income"]:
            Tcur = 1
        elif Tcur == 1 and X >= P["div_x"] and Y >= P["div_income"]:
            Tcur = 2
        sec = sectors_of(X)

        # ---- capacity: one declared supply rule, lagged ---------------------------
        for L in range(NL):
            base = C[L, max(0, t - P["seat_lag"][L])]
            cover = coverage_target(P["cover_lo"][L], P["cover_hi"][L], buildout[L, t])
            desired = desired_capacity(cover * cap, base)
            seats[L] = update_seats(seats[L], desired, P["seat_resp"][L])
        out["seats"][:, t] = seats
        q = np.maximum(C[:, t], 1e-9) / np.maximum(seats, 1e-9)
        Qq = np.exp(-P["gamma"] * np.maximum(0.0, q - 1.0))
        out["q"][:, t] = q
        out["Q"][:, t] = Qq
        out["cls"][:, t] = np.array(P["class_target"]) * np.maximum(1.0, q)

        # ---- household demand ------------------------------------------------------
        for L in range(NL):
            if L < 3:
                Pr = state_shares(cp, L, hhnoise[t])
                p_s, p_b, p_w, p_n = Pr
                ds = p_s + p_b
                elig = 1.0 if L == 0 else min(1.0, pools[L] / max(C[L, t], 1e-9))
                D_off = ds * elig * C[L, t]
                D_oa = P["oa_rate"][L] * C[L, t]
            else:
                pool3 = grads_hist[2, OFF + t] + P["ter_pool_retain"] * pools[3]
                p3 = sig(P["t3_a"] + P["t3_b"] * math.log(max(Y, 100.0) / 1000.0)
                         + P["t3_c"] * (X - 0.6))
                elig = min(1.0, pools[3] / max(C[3, t], 1e-9))
                ds = p3
                D_off = p3 * min(pools[3], 1.05 * C[3, t])
                D_oa = P["oa_rate"][3] * C[3, t]
                p_s = p_b = p_w = p_n = 0.0
            out["p_school"][L, t] = p_s; out["p_both"][L, t] = p_b
            out["p_work"][L, t] = p_w; out["p_neither"][L, t] = p_n
            out["elig"][L, t] = elig
            out["pool"][L, t] = pools[L]
            out["demand_share"][L, t] = ds
            out["demand_off"][L, t] = D_off
            out["demand_oa"][L, t] = D_oa

            # ---- rationing: official age first, then over-age --------------------
            phys = min(P["phys_cap"] * seats[L], P["overage_cap"] * C[L, t])
            adm_off = min(D_off, phys)
            adm_oa = min(D_oa, max(0.0, phys - adm_off))
            admitted = adm_off + adm_oa
            out["intake_off"][L, t] = adm_off
            out["intake_oa"][L, t] = adm_oa
            out["enrol"][L, t] = admitted
            out["rationed"][L, t] = max(0.0, D_off - adm_off)
            out["ger"][L, t] = clip(100.0 * admitted / max(C[L, t], 1e-9), 0.0, P["overage_cap"] * 100.0)
            out["oos"][L, t] = max(0.0, C[L, t] - adm_off)
            out["oos_rate"][L, t] = out["oos"][L, t] / max(C[L, t], 1e-9)
            out["demand_share"][L, t] = ds
            adm_hist[L, OFF + t] = adm_off / max(C[L, t], 1e-9)
            adm_p_hist[L, OFF + t] = adm_off
            enrol_hist[L, OFF + t] = admitted

            # ---- quality feeds survival/completion (not just intake) -----------
            surv = clip(P["surv_max"][L] * Qq[L] ** P["surv_theta"][L], 0.02, 0.995)
            a_entry = adm_hist[L, OFF + t - int(round(DVEC[L]))]
            comp_coh = clip(a_entry * surv, 0.0, 1.0)
            gr = adm_p_hist[L, OFF + t - int(round(DVEC[L]))] * surv
            out["surv"][L, t] = surv
            out["comp_coh"][L, t] = comp_coh
            out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)
            out["grads"][L, t] = gr
            grads_hist[L, OFF + t] = gr

            # ---- out-of-school composition: default to WORK, bounded neither ----
            if L < 3:
                denom = max(1e-9, 1.0 - ds)
                w_nd = p_w / denom if denom > 1e-6 else p_w
                n_nd = p_n / denom if denom > 1e-6 else p_n
                rationed = out["rationed"][L, t]
                base_oos = C[L, t] - D_off
                work_f = (P["ration_work_share"] * rationed
                          + w_nd * max(0.0, base_oos))
                neither_f = ((1.0 - P["ration_work_share"]) * rationed
                             + n_nd * max(0.0, base_oos))
                both_f = p_b * elig * C[L, t] * min(1.0, adm_off / max(D_off, 1e-9))
                out["work_final"][L, t] = work_f
                out["neither_final"][L, t] = neither_f
                out["both_final"][L, t] = both_f
                cl = work_f
                if L == 2:
                    cl = cp["haz"] * work_f
                if L == 0:
                    cl += both_f
                out["child_labour"][L, t] = cl
            else:
                # tertiary is an adult decision: the four-state child block does not
                # apply, so work/neither are 0 here (not a residual). Non-enrolment is
                # carried by out_of_school.
                out["work_final"][L, t] = 0.0
                out["neither_final"][L, t] = 0.0
                out["both_final"][L, t] = 0.0
                out["child_labour"][L, t] = 0.0

        # ---- pools (pipeline eligibility for next levels) -------------------------
        # v1.3 (frozen spec sec.5, DRY_RUN_PLAN sec.1.2): the realised advance rate Pi
        # replaces pi0 for the ONE-YEAR-LAGGED pool, and nothing else. With the shadow
        # block off, pool_mult == 1.0 exactly and this line is arithmetically v1.2's.
        for L in range(1, NL):
            pool_mult = float(ratio_prev[L]) if sh_in is not None else 1.0
            newpool = out["grads"][L - 1, t] * pool_mult + P["pool_retain"] * pools[L]
            pools[L] = min(newpool, 1.05 * C[L, t])

        # ---- teachers: reported PTR is a stock ratio built with a lag -------------
        for L in range(NL):
            desired_t = enrol_hist[L, OFF + t - P["teach_lag"][L]] / P["ptr_target"][L]
            factor = P["teach_delivery_base"] + P["teach_delivery_gain"] * buildout[L, t]
            teachers[L] = max(1.0, teachers[L] + P["teach_resp"][L] * factor
                              * (desired_t - teachers[L]))
        out["teachers"][:, t] = teachers
        ptr = np.maximum(out["enrol"][:, t], 1e-9) / np.maximum(teachers, 1e-9)
        out["ptr"][:, t] = np.clip(ptr, 2.0, 150.0)

        # ---- literacy stock (lagged primary completion; v1 convention) -----------
        lit = clip(lit + P["lit_learn"]
                   * (comp_hist[OFF + t - P["lit_lag"]] - lit), 0.02, 0.995)
        comp_hist[OFF + t] = out["comp_coh"][0, t]

        # ---- attainment / years-of-schooling proxy --------------------------------
        for L in range(NL):
            prev = 0.0 if t == 0 else out["att"][L, t - 1]
            out["att"][L, t] = clip(prev + (out["comp_coh"][L, t] - prev) / 25.0, 0.0, 1.0)
        out["yos"][t] = float((DVEC * out["att"][:, t]).sum())

        # ---- Layer 3 economy: rungs, matching, wages, growth (ported from v1) ----
        LF = P["lf_share_of_pop"] * Pop[t]
        eform = P["phi_formal"] * (sec[2] + sec[3]) * LF
        u = rung_a + rung_b * (X - 0.6) + off_u * cp["office_bias"] + mfg_u * cp["mfg_bias"]
        open_mask = np.array([X >= P["x_open"][r] for r in range(4)])
        u = np.where(open_mask, u, -1e9)
        w = np.exp(u - u.max()); w = w / w.sum()
        J = eform * w
        vac = np.clip(J - E_r * (1.0 - sepr), 0.0, J)

        grads_vec = out["grads"][:, t]
        cand = grads_vec * seek + queue_carry
        remaining = cand.copy()
        hires = np.zeros(4)
        qr = np.zeros(4)
        rf = np.ones(4)
        for r in (3, 2, 1, 0):
            poolv = float(remaining[r:].sum())
            v = float(vac[r])
            hire = min(v, poolv)
            if hire > 0:
                tight = hire / max(poolv, 1e-9)
                rf[r] = 1.0 + P["rank_gain"] * (1.0 - tight) if r >= 1 else 1.0
                qr[r] = max(0.0, poolv - hire)
                left = hire
                for L in range(NL - 1, r - 1, -1):
                    if left <= 1e-12:
                        break
                    take = min(remaining[L], left)
                    remaining[L] -= take
                    left -= take
                hires[r] = hire
            else:
                rf[r] = 1.0
                qr[r] = poolv
        queue_carry = np.minimum(P["queue_retain"] * np.maximum(remaining, 0.0),
                                 P["queue_max_lf"] * LF)
        E_r = np.maximum(E_r + hires - sepr * E_r, 0.0)
        E_r = np.minimum(E_r, J)

        psi = (P["psi_pre"], P["psi_ind"], P["psi_div"])[Tcur]
        w_inf = (Y / 1000.0) * (1.0 + psi * lit)
        w_for = np.array([(Y / 1000.0) * mult[r] * (1.0 + P["cred_prem"] * r) * rf[r]
                          for r in range(4)])
        accel = (P["accel_ind"], P["accel_div"])[Tcur - 1] if Tcur >= 1 else np.ones(4)
        gs = float((sec * gp * accel).sum())
        if Tcur >= 1:
            gs += sec[0] * P["lit_ag_growth"] * lit
        comp_term = float((comp_step * np.maximum(0.0, (E_r - prevE) / max(LF, 1e-9))).sum())
        g = clip(gs + comp_term + gnoise[t], P["g_floor"], P["g_cap"])
        prevE = E_r.copy()

        # ---- shadow block (H4): household tutoring demand at the gates --------------
        # Frozen equation, frozen parameters, declared country inputs. Pure: reads state,
        # writes only the shadow stores. No RNG, no v1.2 parameter, no v1.2 state.
        if sh_in is not None:
            cap_c = [min(P["phys_cap"] * seats[L], P["overage_cap"] * C[L, t])
                     for L in range(NL)]
            gate_gs = gate_state(C[:, t], cap_c, out["grads"][:, t], out["enrol"][:, t],
                                 rf, qr, vac, hires, beh)
            sb = shadow_block(beh, sh_in, gate_gs, w_for, w_inf)
            # NOTE: loop names must not shadow v1.2 locals (g = growth rate, q = congestion,
            # gs = sector growth). Renamed deliberately; see TUNE_LOG.md D3.
            for gg in GATES:
                out["D_sh"][gg, t] = sb[gg]["D"]
                out["S_sh"][gg, t] = sb[gg]["S"]
                out["R_sh"][gg, t] = sb[gg]["R"]
                out["Q_sh"][gg, t] = sb[gg]["Q"]
                out["pi0_sh"][gg, t] = sb[gg]["pi0"]
                out["pi1_sh"][gg, t] = sb[gg]["pi1"]
                out["Pi_sh"][gg, t] = sb[gg]["Pi"]
                out["kappa_sh"][gg, t] = sb[gg]["kappa"]
                out["V_sh"][gg, t] = sb[gg]["V"]
                out["dpi_sh"][gg, t] = sb[gg]["dpi"]
                out["ratio_sh"][gg, t] = sb[gg]["ratio"]
                out["cand_sh"][gg, t] = sb[gg]["candidates"]
                out["cap_sh"][gg, t] = sb[gg]["capacity"]
                out["adv_sh"][gg, t] = sb[gg]["advances"]
                for qq in range(5):
                    out["p_sh"][gg, qq, t] = sb[gg]["ps"][qq]
            ratio_prev = out["ratio_sh"][:, t].copy()

        # ---- store -----------------------------------------------------------------
        out["Y"][t] = Y; out["X"][t] = X; out["lit"][t] = lit
        out["Tstate"][t] = Tcur; out["sec"][:, t] = sec
        out["J"][:, t] = J; out["sh"][:, t] = w; out["E"][:, t] = E_r
        out["vac"][:, t] = vac; out["queue_r"][:, t] = qr; out["queue_tot"][t] = qr.sum()
        out["rankf"][:, t] = rf; out["w_inf"][t] = w_inf; out["w_for"][:, t] = w_for
        out["hires"][:, t] = hires
        out["g"][t] = g
        X_prev = X
        xbase_prev = xbase
        Y *= (1.0 + g)

    out["cp"] = cp
    out["shadow_in"] = sh_in
    out["beh"] = beh
    out["S"] = S_path
    out["U"] = U
    out["Pop"] = Pop
    out["C"] = C
    return out


# ======================================================================================
# 7. PANEL CONSTRUCTION + WRITING
# ======================================================================================
def build_panel(results):
    rows = []
    for r in results:
        cp = r["cp"]
        for t in range(T):
            ptr_sys = float(r["enrol"][:, t].sum() / max(r["teachers"][:, t].sum(), 1e-9))
            for L in range(NL):
                c = float(r["C"][L, t])
                oos = float(r["oos"][L, t])
                wf = float(r["work_final"][L, t])
                nf = float(r["neither_final"][L, t])
                rows.append(dict(
                    country=cp["name"], country_id=cp["idx"], year=int(YEARS[t]),
                    level=LEVELS[L], label=LABEL,
                    cohort=c,
                    band_population=c * DVEC[L],
                    seats=float(r["seats"][L, t]),
                    seat_coverage=float(r["seats"][L, t] / max(c, 1e-9)),
                    congestion_q=float(r["q"][L, t]),
                    quality_q=float(r["Q"][L, t]),
                    class_size=float(r["cls"][L, t]),
                    teachers=float(r["teachers"][L, t]),
                    ptr=float(r["ptr"][L, t]),
                    ptr_system=ptr_sys,
                    enrolment=float(r["enrol"][L, t]),
                    ger=float(r["ger"][L, t]),
                    demand_share=float(r["demand_share"][L, t]),
                    demand_official=float(r["demand_off"][L, t]),
                    demand_overage=float(r["demand_oa"][L, t]),
                    admitted_official=float(r["intake_off"][L, t]),
                    admitted_overage=float(r["intake_oa"][L, t]),
                    rationed_official=float(r["rationed"][L, t]),
                    out_of_school=oos,
                    oos_rate=float(r["oos_rate"][L, t]),
                    eligibility_pool=float(r["pool"][L, t]),
                    school_share=float(r["p_school"][L, t]),
                    both_share=float(r["p_both"][L, t]),
                    work_share=float(r["p_work"][L, t]),
                    neither_share=float(r["p_neither"][L, t]),
                    oos_work_share=float(wf / max(oos, 1e-9)),
                    oos_neither_share=float(nf / max(oos, 1e-9)),
                    child_labour=float(r["child_labour"][L, t]),
                    child_labour_rate=float(r["child_labour"][L, t] / max(c, 1e-9)),
                    survival=float(r["surv"][L, t]),
                    dropout_rate=float(1.0 - r["surv"][L, t]),
                    completion_cohort=float(r["comp_coh"][L, t]),
                    completion_uis=float(r["comp_uis"][L, t]),
                    measurement_factor=float(P["meas_completion_factor"]),
                    graduates=float(r["grads"][L, t]),
                    s_ag=float(r["sec"][0, t]), s_inf=float(r["sec"][1, t]),
                    s_man=float(r["sec"][2, t]), s_srv=float(r["sec"][3, t]),
                    complexity_x=float(r["X"][t]), gdppc=float(r["Y"][t]),
                    urban=float(r["U"][t]), literacy=float(r["lit"][t]),
                    yos_proxy=float(r["yos"][t]),
                    takeoff_state=("pre-industrial", "industrializing", "diversified")[
                        int(r["Tstate"][t])],
                    population=float(r["Pop"][t]),
                    rung1_demand=float(r["J"][0, t]), rung2_demand=float(r["J"][1, t]),
                    rung3_demand=float(r["J"][2, t]), rung4_demand=float(r["J"][3, t]),
                    rung1_emp=float(r["E"][0, t]), rung2_emp=float(r["E"][1, t]),
                    rung3_emp=float(r["E"][2, t]), rung4_emp=float(r["E"][3, t]),
                    queue_total=float(r["queue_tot"][t]),
                    queue_pressure=float(r["queue_tot"][t]
                                         / max(P["lf_share_of_pop"] * r["Pop"][t], 1e-9)),
                    wage_informal=float(r["w_inf"][t]),
                    wage_formal_rung1=float(r["w_for"][0, t]),
                    wage_formal_rung2=float(r["w_for"][1, t]),
                    formal_share=float(r["E"][:, t].sum()
                                       / max(P["lf_share_of_pop"] * r["Pop"][t], 1e-9)),
                    informal_share=float(max(0.0, 1.0 - r["E"][:, t].sum()
                                             / max(P["lf_share_of_pop"] * r["Pop"][t], 1e-9))),
                    growth=float(r["g"][t]),
                ))
    return rows


def write_panel(rows, path):
    import csv
    cols = list(rows[0].keys())
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v)
                        for k, v in row.items()})


# ======================================================================================
# 8. CHECKS (frozen scoring rules, PRE_DECLARATIONS.md section 5)
# ======================================================================================
def ols(y, Xs, names):
    X = np.column_stack([np.ones(len(y))] + list(Xs))
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = max(1, len(y) - X.shape[1])
    s2 = float(resid @ resid / dof)
    try:
        cov = s2 * np.linalg.inv(X.T @ X)
    except np.linalg.LinAlgError:
        cov = s2 * np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.clip(np.diag(cov), 0.0, None))
    tt = beta / np.where(se > 0, se, np.nan)
    pv = 2.0 * (1.0 - 0.5 * (1.0 + np.vectorize(math.erf)(np.abs(tt) / math.sqrt(2.0))))
    return dict(beta=dict(zip(["const"] + names, beta)),
                se=dict(zip(["const"] + names, se)),
                t=dict(zip(["const"] + names, tt)),
                p=dict(zip(["const"] + names, pv)), n=len(y))


def first_cross(series, threshold=90.0):
    idx = np.where(np.asarray(series) >= threshold)[0]
    return int(YEARS[idx[0]]) if len(idx) else None


def supply_code_audit():
    """Code inspection for check (a): one declared supply rule, no country branch, no
    per-level year-interpolated anchor array. Returns (found_forbidden, info)."""
    src = (inspect.getsource(coverage_target) + inspect.getsource(desired_capacity)
           + inspect.getsource(update_seats))
    forbidden = ["SYN00", "PHL", "seat_override", "surv_override", "np.interp",
                 "anchor", "country ==", "cp[", "name =="]
    found = [tok for tok in forbidden if tok in src]
    info = {
        "functions_audited": ["coverage_target", "desired_capacity", "update_seats"],
        "source_lines": len(src.strip().splitlines()),
        "country_branches": 0,
        "year_indexed_anchor_arrays": 0,
        "forbidden_tokens_found": found,
    }
    return found, info


def check_A(res):
    r = res[0]
    cu = r["comp_uis"] * 100.0
    cc = r["comp_coh"] * 100.0
    ger = r["ger"]
    pri = first_cross(cu[0]); low = first_cross(cu[1])
    up = cu[2]
    upto24 = YEARS <= 2024
    up_max = float(up[upto24].max())
    up24 = float(up[YEARS == 2024][0])
    low23 = float(cu[1][YEARS == 2023][0])
    ter25 = float(ger[3][YEARS == 2025][0])
    found, info = supply_code_audit()
    a1 = (pri is not None and 2014 <= pri <= 2020)
    a2 = (low is not None and 2021 <= low <= 2027 and low23 < 90.0)
    a3 = (up_max < 90.0 and 73.0 <= up24 <= 77.0)
    a4 = (48.1 <= ter25 <= 54.1)
    a5 = (len(found) == 0)
    sub = {
        "A1_primary_uis_first_ge90_2014_2020": (a1, pri),
        "A2_lower_uis_first_ge90_2021_2027_and_2023_lt90": (a2, (low, round(low23, 2))),
        "A3_upper_uis_never_ge90_by_2024_and_2024_in_73_77": (a3, (round(up_max, 2), round(up24, 2))),
        "A4_tertiary_ger_2025_in_48_1_54_1": (a4, round(ter25, 2)),
        "A5_single_supply_rule_code_inspection": (a5, "no forbidden token" if a5 else found),
    }
    ok = all(v[0] for v in sub.values())
    val = (f"UIS completion: primary first>=90 {pri}; lower first>=90 {low} "
           f"(2023={low23:.2f}); upper max<=2024 {up_max:.2f}, 2024 {up24:.2f}; "
           f"tertiary GER 2025 {ter25:.2f}; supply-rule audit {info}")
    note = (
        "Check (a) is scored on the UIS-convention completion series (m x cohort-flow, m = "
        f"{P['meas_completion_factor']:.2f}, one declared constant), because the declared "
        "on-disk PHL targets are UIS completion rates. The cohort-flow series is reported "
        f"too: its first>=90 years are primary {first_cross(cc[0])}, lower "
        f"{first_cross(cc[1])} (it is the identity-bound series used in check d). "
        "CODE INSPECTION: the supply rule is a single equation implemented in three "
        "functions; no country identity, no per-level year-interpolated anchor array, no "
        "override variable enters it. Country differences are declared traits "
        "(cohort path, income, sector, one delivery-timing shift) passed through the same "
        "functions. This is the v1.2 requirement that v1 failed.")
    return dict(check_id="A", expected_pattern=(
        "PHL-like: primary UIS completion first >=90 within +/-3 of 2017; lower-secondary "
        "first >=90 within +/-3 of 2024 with 2023<90; upper-secondary never >=90 by 2024 "
        "with 2024 in [73,77]; tertiary GER 2025 in [48.1,54.1]; AND code inspection shows "
        "one declared supply rule for every country and level."),
        synthetic_value=val, verdict="PASS" if ok else "FAIL", note=note,
        sub=sub, audit=info, cohort_dates=(first_cross(cc[0]), first_cross(cc[1])))


def check_B(res, rows):
    # (b1) PHL-like primary out-of-school rate 2005-2015
    phl = [x for x in rows if x["country"] == "SYN00_PHL_LIKE" and x["level"] == "primary"
           and 2005 <= x["year"] <= 2015]
    phl_oos = float(np.mean([x["oos_rate"] for x in phl])) * 100.0
    b1 = 5.0 <= phl_oos <= 20.0
    # (b2) work/child-labour share of out-of-school >= 0.50 in every country-year
    agg = {}
    for x in rows:
        if x["level"] == "tertiary":
            continue
        key = (x["country"], x["year"])
        a = agg.setdefault(key, [0.0, 0.0])
        a[0] += x["out_of_school"]
        a[1] += x["out_of_school"] * x["oos_work_share"]
    worst = min((w / max(o, 1e-9), k) for k, (o, w) in agg.items())
    b2 = worst[0] >= 0.50
    cl_agg = {}
    for x in rows:
        if x["level"] == "tertiary":
            continue
        key = (x["country"], x["year"])
        a = cl_agg.setdefault(key, [0.0, 0.0])
        a[0] += x["out_of_school"]; a[1] += x["child_labour"]
    cl_worst = min((w / max(o, 1e-9), k) for k, (o, w) in cl_agg.items())
    # (b3) boom vs flat/decline mean OOS 1990-2015
    def mean_oos(name):
        vals = [x["out_of_school"] for x in rows
                if x["country"] == name and 1990 <= x["year"] <= 2015
                and x["level"] in ("primary", "lower_secondary")]
        coh = [x["cohort"] for x in rows
               if x["country"] == name and 1990 <= x["year"] <= 2015
               and x["level"] in ("primary", "lower_secondary")]
        return float(np.sum(vals) / max(np.sum(coh), 1e-9)) * 100.0
    boom = mean_oos("SYN10_BOOM")
    flat = mean_oos("SYN11_FLAT")
    decl = mean_oos("SYN12_DECLINE")
    b3 = (boom - max(flat, decl)) >= 2.0
    sub = {
        "B1_phl_primary_oos_2005_2015_in_5_20pct": (b1, round(phl_oos, 2)),
        "B2_work_or_cl_share_of_oos_ge50_every_country_year": (b2, round(worst[0], 3)),
        "B3_boom_oos_minus_flat_decline_ge2pp_1990_2015": (b3, round(boom - max(flat, decl), 2)),
        "B3_means_boom_flat_decline": (True, (round(boom, 2), round(flat, 2), round(decl, 2))),
        "B2b_childlabour_share_of_oos_min_info": (True, round(cl_worst[0], 3)),
    }
    ok = b1 and b2 and b3
    val = (f"PHL primary OOS 2005-2015 mean {phl_oos:.2f}%; worst country-year work share of "
           f"OOS {worst[0]:.3f} ({worst[1]}); mean OOS 1990-2015 boom {boom:.2f} vs flat "
           f"{flat:.2f} vs decline {decl:.2f} pp (boom - max = {boom - max(flat, decl):+.2f})")
    note = (
        "Out-of-school children default to work by construction (declared rationing rule: "
        f"{P['ration_work_share']:.0%} of rationed children to work, the rest to a bounded "
        "'neither' category). 'neither' is reported separately and never absorbs a residual. "
        "The cohort-responsiveness test compares the three otherwise-identical declared "
        "cohort-path variants; it is a property of this synthetic world, not evidence about "
        "any real demography.")
    return dict(check_id="B", expected_pattern=(
        "PHL-like primary OOS 2005-2015 in [5%,20%]; work/child-labour share of OOS >=0.50 "
        "in every country-year; boom countries' mean OOS exceeds flat/decline by >=2pp "
        "over 1990-2015."),
        synthetic_value=val, verdict="PASS" if ok else "FAIL", note=note, sub=sub,
        worst=worst, means=(boom, flat, decl))


def check_C(res, ptr_obs):
    r = res[0]
    ptr = r["ptr"][0]
    m = (YEARS >= 1990) & (YEARS <= 2010)
    peak_year = int(YEARS[m][int(np.argmax(ptr[m]))])
    peak = float(ptr[m].max())
    p24 = float(ptr[YEARS == 2024][0])
    c1 = 1990 <= peak_year <= 2010
    c2 = peak >= 1.10 * p24
    c3 = p24 < peak
    # system PTR (all levels) diagnostic
    ptr_sys = r["enrol"].sum(axis=0) / np.maximum(r["teachers"].sum(axis=0), 1e-9)
    sys_peak_year = int(YEARS[int(np.argmax(ptr_sys[(YEARS >= 1990) & (YEARS <= 2010)]))])
    obs_txt = ""
    if ptr_obs:
        yrs = sorted(y for y in ptr_obs if 1995 <= y <= 2017)
        if yrs:
            obs_txt = (f" observed benchmark (not encoded): {ptr_obs[yrs[0]]:.1f} "
                       f"({yrs[0]}) -> {ptr_obs[yrs[-1]]:.1f} ({yrs[-1]})")
    ok = c1 and c2 and c3
    val = (f"PHL primary PTR peak {peak:.2f} in {peak_year}; 2024 {p24:.2f}; "
           f"ratio peak/2024 {peak / max(p24, 1e-9):.3f}; system PTR peak year {sys_peak_year}")
    note = ("PTR is a genuine stock ratio (enrolment / teacher stock), and the teacher stock "
            "is built with a declared lag and a declared delivery build-out; it is not a "
            "direct function of q. Congestion q = cohort/seats drives quality and completion. "
            "The observed PHL primary PTR series is read only as a declared benchmark for this "
            "shape test and is never encoded." + obs_txt)
    return dict(check_id="C", expected_pattern=(
        "PHL-like pupil-teacher ratio peaks 1990-2010 at least 10% above its 2024 value, "
        "and 2024 is below the peak."),
        synthetic_value=val, verdict="PASS" if ok else "FAIL", note=note,
        sub={"C1_peak_year_1990_2010": (c1, peak_year),
             "C2_peak_ge_110pct_of_2024": (c2, round(peak / max(p24, 1e-9), 3)),
             "C3_2024_below_peak": (c3, (round(p24, 2), round(peak, 2)))})


def check_D(rows):
    worst = -1e9
    worst_key = None
    viol = 0
    for x in rows:
        lhs = x["completion_cohort"]
        rhs = (x["ger"] / 100.0) * (1.0 + 1e-9)
        d = lhs - rhs
        if d > 0:
            viol += 1
        if d > worst:
            worst = d; worst_key = (x["country"], x["year"], x["level"])
    ok = (viol == 0)
    val = (f"cohort-flow completion <= GER x (1+1e-9): violations {viol}, max excess "
           f"{worst:.3e} at {worst_key}; measurement factor m = "
           f"{P['meas_completion_factor']:.2f} (single declared constant)")
    note = ("Disclosed measurement issue: UIS completion is measured on children 3-5 years "
            "above grade age, so observed PHL completion can exceed GER. The model reports "
            "BOTH the identity-bound cohort-flow completion (check d scored here) and a "
            "UIS-convention series = m x cohort-flow with ONE declared constant m; no "
            "per-level or per-country factor exists. Check (a) uses the UIS series; check "
            "(d) is scored on the cohort-flow series.")
    return dict(check_id="D", expected_pattern=(
        "In cohort-flow accounting, model completion <= GER x (1+1e-9) in every "
        "country-year-level; if a UIS-convention series is reported, its factor m is one "
        "declared constant and both series are written out."),
        synthetic_value=val, verdict="PASS" if ok else "FAIL", note=note,
        sub={"D1_no_completion_above_ger": (ok, viol),
             "D2_single_declared_m": (True, P["meas_completion_factor"])})


def check_E(rows):
    # country-year panel: X and lagged primary UIS completion flow
    by = {}
    for x in rows:
        if x["level"] == "primary":
            by.setdefault((x["country"], x["year"]), {})["flow"] = x["completion_uis"]
        by.setdefault((x["country"], x["year"]), {})["x"] = x["complexity_x"]
    lag = P["edu_lag"]
    recs = []
    for (cn, y), d in by.items():
        if "flow" not in d:
            continue
        src = by.get((cn, y - lag))
        if src is None or "flow" not in src:
            continue
        recs.append((cn, y, d["x"], src["flow"]))
    recs.sort()
    yv = np.array([r[2] for r in recs])
    xv = np.array([r[3] for r in recs])
    ctry = [r[0] for r in recs]; yr = [r[1] for r in recs]
    cs = sorted(set(ctry))[1:]
    ys = sorted(set(yr))[1:]
    fe_c = [np.array([1.0 if v == c else 0.0 for v in ctry]) for c in cs]
    fe_y = [np.array([1.0 if v == q else 0.0 for v in yr]) for q in ys]
    names = [f"c_{c}" for c in cs] + [f"y_{q}" for q in ys]
    r1 = ols(yv, [xv] + fe_c + fe_y, ["flow_lag"] + names)
    b1 = float(r1["beta"]["flow_lag"]); p1 = float(r1["p"]["flow_lag"])
    c1 = (b1 > 0 and p1 < 0.05)

    # 5-year block spec
    blocks = {}
    for (cn, y, x, f) in recs:
        blk = (y - YEAR_START) // 5
        d = blocks.setdefault((cn, blk), [0.0, 0.0, 0])
        d[0] += x; d[1] += f; d[2] += 1
    brows = [(k[0], k[1], v[0] / v[2], v[1] / v[2]) for k, v in blocks.items()]
    brows.sort()
    yv2 = np.array([b[2] for b in brows]); xv2 = np.array([b[3] for b in brows])
    c2n = [b[0] for b in brows]; b2n = [b[1] for b in brows]
    cs2 = sorted(set(c2n))[1:]; bs2 = sorted(set(b2n))[1:]
    fe_c2 = [np.array([1.0 if v == c else 0.0 for v in c2n]) for c in cs2]
    fe_b2 = [np.array([1.0 if v == q else 0.0 for v in b2n]) for q in bs2]
    r2 = ols(yv2, [xv2] + fe_c2 + fe_b2,
             ["flow_lag"] + [f"c_{c}" for c in cs2] + [f"b_{q}" for q in bs2])
    b2 = float(r2["beta"]["flow_lag"]); p2 = float(r2["p"]["flow_lag"])
    c2 = (b2 > 0)
    ok = c1 and c2
    val = (f"two-way FE (country+year) X on primary completion flow lag {lag}: b={b1:+.3f} "
           f"(se {r1['se']['flow_lag']:.3f}, p={p1:.4g}, n={r1['n']}); 5-year-block FE: "
           f"b={b2:+.3f} (p={p2:.4g}, n={r2['n']})")
    note = ("The education -> complexity channel is declared, not fitted: X_t = "
            "xbase(Y,U) + x_edu_level*flow_{t-10} + x_edu_delta*delta_flow_{t-10} + "
            "x_persist*(X_{t-1} - xbase_{t-1}). 'flow' is the cohort-flow primary "
            "completion rate (the flow object of Amendment A1 / the observed E5 regressor), "
            "NOT the literacy stock. This check asks whether the declared channel is "
            "present and identifiable in the synthetic panel; it is not a causal test.")
    return dict(check_id="E", expected_pattern=(
        "In the synthetic panel the two-way FE coefficient of lagged primary-completion "
        "flow on X is positive with p<0.05 at the declared lag (5-10y), and the same sign "
        "holds in the 5-year-block spec."),
        synthetic_value=val, verdict="PASS" if ok else "FAIL", note=note,
        sub={"E1_two_way_fe_positive_p_lt_05": (c1, (round(b1, 4), round(p1, 6))),
             "E2_five_year_block_same_sign": (c2, (round(b2, 4), round(p2, 6)))},
        detail=dict(b1=b1, p1=p1, b2=b2, p2=p2, n1=r1["n"], n2=r2["n"], lag=lag))


# ======================================================================================
# 9. V1.3 RUN, FROZEN CHECKS c1-c6, AND OUTPUTS
#    Scored exactly as shadow_module/PRE_DECLARATIONS.md sec.8 says. A FAIL is reported
#    as a FAIL; no threshold or parameter is ever adjusted to rescue one.
# ======================================================================================
C1_GAP = 0.10          # sec.8 c1: R doubling at g2 must raise D by >= +10.0 pp
C2_GAP = 0.02          # sec.8 c2: +25% on phi at g2 must raise D by >= +2.0 pp
C3_MAX_D0 = 0.025      # sec.8 c3(i)
C3_RATIO = 0.20        # sec.8 c3(ii)
C4A_LO, C4A_HI = 0.75, 0.95   # sec.8 c4a
C4B_GAP1, C4B_GAP2 = 0.10, 0.05  # sec.8 c4b
SAT_LO, SAT_HI = 0.05, 0.90      # DRY_RUN_PLAN.md sec.7.2 (pre-declared informative range)
DERIV_H = 1e-4                    # numerical step for the derivative components


def run_all(seed=SEED, beh=None, shadow=True, inputs=None, hosts=None):
    """v1.2 run with the shadow block layered on the gate/queue machinery.

    The RNG draws are unchanged from v1.2 (same stream, same order, same count), so the
    30 synthetic countries and their shocks are identical to the frozen v1.2 run.
    """
    beh = SHADOW_BEHAV if beh is None else beh
    inputs = shadow_inputs_named() if inputs is None else inputs
    S_phl, P_phl, coh_obs, ptr_obs, spend_obs = load_observed_phl_paths()
    rng = np.random.default_rng(seed)
    cps = apply_declared(draw_countries(rng))
    gnoise = rng.normal(0.0, P["g_noise_sd"], (T, N_C))
    hhnoise = rng.normal(0.0, P["hh_noise_sd"], (T, N_C))
    # Declared controlled comparisons (unchanged from v1.2).
    for j in (2,):
        gnoise[:, j] = gnoise[:, 1]; hhnoise[:, j] = hhnoise[:, 1]
    for j in (11, 12):
        gnoise[:, j] = gnoise[:, 10]; hhnoise[:, j] = hhnoise[:, 10]
    by_host = {}
    if shadow and hosts:
        for tname, hname in hosts.items():
            by_host[hname] = tname
    results = []
    for i, cp in enumerate(cps):
        S = cohort_path(cp, S_phl)
        Pop = pop_path(cp, P_phl)
        sh_in = None
        if cp["name"] in by_host:
            tname = by_host[cp["name"]]
            sh_in = dict(inputs[tname], type=tname)
        results.append(simulate_country(cp, gnoise[:, i], hhnoise[:, i], S, Pop,
                                        sh_in=sh_in, beh=beh))
    return results, ptr_obs, spend_obs, S_phl, P_phl


def required_R_for_D(beh, ci, g, V, dpi, target, lo_lnR=0.0, hi_lnR=6.0):
    """NOT-SCORED diagnostic: the gate pressure a target demand would need, all else fixed.

    D is strictly increasing in ln R (b_Z > 0), so bisection is exact to machine precision.
    """
    for _ in range(200):
        mid = 0.5 * (lo_lnR + hi_lnR)
        D, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"],
                                   math.exp(mid), V, dpi, g)
        if D < target:
            lo_lnR = mid
        else:
            hi_lnR = mid
    return math.exp(0.5 * (lo_lnR + hi_lnR))


def shadow_world(res, hosts, inputs, beh):
    """Per-type view of the stored run: demand, R, D* and the declared inputs."""
    by = {r["cp"]["name"]: r for r in res}
    w = {}
    for tname in TYPE_ORDER:
        r = by[hosts[tname]]
        ci = dict(inputs[tname])
        D = r["D_sh"]
        dstar = np.array([sum(ci["nu"][g] * D[g, t] for g in (1, 2, 3)) for t in range(T)])
        w[tname] = dict(r=r, ci=ci, host=hosts[tname], D=D, Dstar=dstar,
                        R=r["R_sh"], V=r["V_sh"], dpi=r["dpi_sh"], pi0=r["pi0_sh"],
                        pi1=r["pi1_sh"], Pi=r["Pi_sh"], p=r["p_sh"], Q=r["Q_sh"],
                        kappa=r["kappa_sh"], ratio=r["ratio_sh"], S=r["S_sh"],
                        cand=r["cand_sh"], cap=r["cap_sh"], adv=r["adv_sh"],
                        exposure=float(sum(ci["nu"].values())))
    return w


def build_panel_v13(results, hosts, inputs):
    """v1.2 panel rows (identical objects) + shadow columns for the designated types."""
    rows = build_panel(results)
    by = {r["cp"]["name"]: r for r in results}
    host_of = {h: t for t, h in hosts.items()}
    gate_of_level = {0: 0, 1: 1, 2: 2, 3: 3}
    for row in rows:
        cname = row["country"]
        trow = int(row["year"]) - YEAR_START
        L = LEVELS.index(row["level"])
        g = gate_of_level[L]
        row["shadow_type"] = host_of.get(cname, "")
        row["shadow_gate_status"] = "designated" if cname in host_of else "not_designated"
        row["shadow_gate"] = GATE_NAMES[g]
        r = by[cname]
        if cname in host_of:
            tname = host_of[cname]
            ci = inputs[tname]
            row["D_gate"] = float(r["D_sh"][g, trow])
            row["D_cohort"] = float(sum(ci["nu"][gg] * r["D_sh"][gg, trow]
                                        for gg in (1, 2, 3)))
            row["cohort_exposure"] = float(sum(ci["nu"].values()))
            row["R"] = float(r["R_sh"][g, trow])
            row["ln_R"] = float(math.log(max(r["R_sh"][g, trow], 1e-12)))
            row["Q_gate"] = float(r["Q_sh"][g, trow])
            row["pi0"] = float(r["pi0_sh"][g, trow])
            row["pi1"] = float(r["pi1_sh"][g, trow])
            row["Pi"] = float(r["Pi_sh"][g, trow])
            row["kappa"] = float(r["kappa_sh"][g, trow])
            row["V"] = float(r["V_sh"][g, trow])
            row["s_g"] = float(ci["s"])
            row["spend_share"] = float(r["S_sh"][g, trow])
            row["Pi_over_pi0"] = float(r["ratio_sh"][g, trow])
            for q in range(5):
                row["p_q%d" % (q + 1)] = float(r["p_sh"][g, q, trow])
        else:
            for k in ("D_gate", "D_cohort", "cohort_exposure", "R", "ln_R", "Q_gate",
                      "pi0", "pi1", "Pi", "kappa", "V", "s_g", "spend_share",
                      "Pi_over_pi0", "p_q1", "p_q2", "p_q3", "p_q4", "p_q5"):
                row[k] = ""
    return rows


def write_panel_v13(rows, path):
    cols = list(rows[0].keys())
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v)
                        for k, v in row.items()})


# --------------------------------------------------------------------------------------
# check helpers
# --------------------------------------------------------------------------------------
def _f(x):
    return f"{x:.10g}" if isinstance(x, float) else str(x)


def _verdict_fail(cond):
    return "PASS" if cond else "FAIL"


def check_c1(w, beh):
    """c1 gate pressure: sign in every scored cell + R-doubling at g2 >= +10 pp."""
    fails = []
    n_scored = n_sat = 0
    min_deriv = float("inf")
    max_abs_err = 0.0
    for tname in TYPE_ORDER:
        d = w[tname]; ci = d["ci"]
        for g in (1, 2, 3, 4):
            for t in range(T):
                D = float(d["D"][g, t])
                if not (SAT_LO <= D <= SAT_HI):
                    n_sat += 1
                    continue
                n_scored += 1
                R = float(d["R"][g, t]); V = float(d["V"][g, t]); dpi = float(d["dpi"][g, t])
                Dp, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g,
                                            lnR_shift=+DERIV_H)
                Dm, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g,
                                            lnR_shift=-DERIV_H)
                der = (Dp - Dm) / (2.0 * DERIV_H)
                ana = beh["b_Z"] * sum(wq * pq * (1.0 - pq)
                                       for wq, pq in zip(beh["omega"], d["p"][g, :, t]))
                max_abs_err = max(max_abs_err, abs(der - ana))
                if der < 0.0:
                    fails.append((tname, g, int(YEARS[t]), der))
                min_deriv = min(min_deriv, der)
    gaps = {}
    i20 = DECLARED_COMPARISON_YEAR - YEAR_START
    for tname in TYPE_ORDER:
        d = w[tname]; ci = d["ci"]
        R = float(d["R"][2, i20]); V = float(d["V"][2, i20]); dpi = float(d["dpi"][2, i20])
        D2, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], 2.0 * R, V, dpi, 2)
        gaps[tname] = float(D2 - d["D"][2, i20])
    gap_ok = all(v >= C1_GAP for v in gaps.values())
    sign_ok = (len(fails) == 0) and n_scored > 0
    sub = {
        "c1_i_sign_nonneg_all_scored_cells": (sign_ok, f"{n_scored} scored, {n_sat} saturated/NOT-SCORED, "
                                                         f"min dD/dlnR = {_f(min_deriv)}"),
        "c1_i_cells_scored": (None, n_scored),
        "c1_i_cells_saturated_not_scored": (None, n_sat),
        "c1_i_max_abs_numeric_minus_analytic": (None, max_abs_err),
    }
    for tname in TYPE_ORDER:
        sub["c1_ii_R_doubled_g2_gap_" + tname] = (gaps[tname] >= C1_GAP, gaps[tname])
    ok = sign_ok and gap_ok
    return dict(
        check_id="c1",
        expected_pattern=("dD/dlnR >= 0 in every scored (c,g,t) cell AND R->2R at g2 (t*=2020) raises D "
                          "by >= +10.0 pp in all three country types."),
        synthetic_value=(f"sign: {n_scored} scored cells, min dD/dlnR {min_deriv:+.4g} "
                         f"({n_sat} saturated cells NOT-SCORED per DRY_RUN_PLAN 7.2); "
                         f"R-doubling gap at g2: " +
                         ", ".join(f"{k} {v*100:+.2f} pp" for k, v in gaps.items())),
        verdict=_verdict_fail(ok), note=(
            "Numerical central difference in ln R (h=1e-4); the analytic value b_Z*sum(w p(1-p)) is "
            "reported beside it (max |numeric-analytic| = %.3g). Saturated cells (D outside [0.05,0.90]) "
            "are NOT-SCORED as pre-declared in DRY_RUN_PLAN sec.7.2, not counted as passes." % max_abs_err),
        sub=sub, fails=fails, gaps=gaps, n_scored=n_scored, n_sat=n_sat)


def check_c2(w, beh):
    """c2 expected returns: sign in every scored cell + V->1.25V at g2 >= +2.0 pp."""
    fails = []
    n_scored = n_sat = 0
    min_deriv = float("inf")
    max_abs_err = 0.0
    for tname in TYPE_ORDER:
        d = w[tname]; ci = d["ci"]
        for g in (1, 2, 3, 4):
            for t in range(T):
                D = float(d["D"][g, t])
                if not (SAT_LO <= D <= SAT_HI):
                    n_sat += 1
                    continue
                n_scored += 1
                V = float(d["V"][g, t])
                u = math.log1p(max(V, 0.0))
                R = float(d["R"][g, t]); dpi = float(d["dpi"][g, t])
                if u <= 1e-12:
                    continue
                Vp = math.expm1((1.0 + DERIV_H) * u)
                Vm = math.expm1(max(1e-12, (1.0 - DERIV_H)) * u)
                Dp, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g,
                                            V_mult=Vp / V)
                Dm, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g,
                                            V_mult=Vm / V)
                # the perturbation is +-(h*u) in u = ln(1+V); divide by the actual shift
                der = (Dp - Dm) / (2.0 * DERIV_H * u)
                ana = beh["b_V"] * sum(wq * pq * (1.0 - pq)
                                       for wq, pq in zip(beh["omega"], d["p"][g, :, t]))
                max_abs_err = max(max_abs_err, abs(der - ana))
                if der < 0.0:
                    fails.append((tname, g, int(YEARS[t]), der))
                min_deriv = min(min_deriv, der)
    gaps = {}
    i20 = DECLARED_COMPARISON_YEAR - YEAR_START
    for tname in TYPE_ORDER:
        d = w[tname]; ci = d["ci"]
        R = float(d["R"][2, i20]); V = float(d["V"][2, i20]); dpi = float(d["dpi"][2, i20])
        D25, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], R, V, dpi, 2,
                                     V_mult=1.25)
        gaps[tname] = float(D25 - d["D"][2, i20])
    gap_ok = all(v >= C2_GAP for v in gaps.values())
    sign_ok = (len(fails) == 0) and n_scored > 0
    sub = {
        "c2_i_sign_nonneg_all_scored_cells": (sign_ok, f"{n_scored} scored, {n_sat} saturated/NOT-SCORED, "
                                                         f"min dD/dln(1+V) = {_f(min_deriv)}"),
        "c2_i_cells_scored": (None, n_scored),
        "c2_i_cells_saturated_not_scored": (None, n_sat),
        "c2_i_max_abs_numeric_minus_analytic": (None, max_abs_err),
    }
    for tname in TYPE_ORDER:
        sub["c2_ii_V_plus25pct_g2_gap_" + tname] = (gaps[tname] >= C2_GAP, gaps[tname])
    ok = sign_ok and gap_ok
    return dict(
        check_id="c2",
        expected_pattern=("dD/dln(1+V) >= 0 in every scored cell AND V->1.25V (+25% on phi) at g2 "
                          "(t*=2020) raises D by >= +2.0 pp in all three country types."),
        synthetic_value=(f"sign: {n_scored} scored cells, min dD/dln(1+V) {min_deriv:+.4g} "
                         f"({n_sat} saturated NOT-SCORED); +25% phi gap at g2: " +
                         ", ".join(f"{k} {v*100:+.2f} pp" for k, v in gaps.items())),
        verdict=_verdict_fail(ok), note=(
            "Numerical central difference in ln(1+V) (h=1e-4); analytic b_V*sum(w p(1-p)) beside it "
            "(max |numeric-analytic| = %.3g). The return channel is a declared prior (PARAMETERS.csv B04); "
            "this is a comparative static, not an estimate." % max_abs_err),
        sub=sub, fails=fails, gaps=gaps, n_scored=n_scored, n_sat=n_sat)


def check_c3(w, beh):
    """c3 near-zero pre-gate demand (STRUCTURAL consistency check, not a prediction)."""
    d0 = []; ratios = []
    worst_d0 = (-1.0, "", 0); worst_ratio = (-1.0, "", 0)
    for tname in TYPE_ORDER:
        d = w[tname]
        for t in range(T):
            v = float(d["D"][0, t]); d0.append(v)
            if v > worst_d0[0]:
                worst_d0 = (v, tname, int(YEARS[t]))
            d1 = float(d["D"][1, t])
            if d1 > 1e-12:
                rt = v / d1
                ratios.append(rt)
                if rt > worst_ratio[0]:
                    worst_ratio = (rt, tname, int(YEARS[t]))
    c1ok = worst_d0[0] <= C3_MAX_D0
    c2ok = (len(ratios) == len(d0)) and worst_ratio[0] <= C3_RATIO
    sub = {
        "c3_i_max_D_g0_le_0.025": (c1ok, f"{worst_d0[0]:.6f} at {worst_d0[1]} {worst_d0[2]}"),
        "c3_ii_max_Dg0_over_Dg1_le_0.20": (c2ok, f"{worst_ratio[0]:.6f} at {worst_ratio[1]} {worst_ratio[2]}"),
        "c3_country_years_checked": (None, len(d0)),
    }
    ok = c1ok and c2ok
    return dict(
        check_id="c3",
        expected_pattern=("D(g0) <= 0.025 in every country-year AND D(g0) <= 0.20*D(g1) in every "
                          "country-year. DECLARED STRUCTURAL / CONSISTENCY CHECK, not an empirical "
                          "prediction (PRE_DECLARATIONS.md sec.8 c3 + S1 note item 3)."),
        synthetic_value=(f"max D(g0) = {worst_d0[0]:.6f} at {worst_d0[1]} {worst_d0[2]} (<= 0.025); "
                         f"max D(g0)/D(g1) = {worst_ratio[0]:.6f} at {worst_ratio[1]} "
                         f"{worst_ratio[2]} (<= 0.20)"),
        verdict=_verdict_fail(ok), note=(
            "Structural, not empirical: V(g0)=0 by definition, delta_0=0.02, kappa(g0)=1, and the "
            "pre-gate state is the primary seat/admission ratio. Observed primary-stage tutoring "
            "(PHL 23.8%, KHM 41.3%) is OUT OF THIS MODULE'S SCOPE and is not explained here."),
        sub=sub)


def check_c4a(w, beh):
    i20 = DECLARED_COMPARISON_YEAR - YEAR_START
    v = float(w["SYN_HKG_LIKE"]["D"][2, i20])
    ok = (C4A_LO <= v <= C4A_HI)
    path = [float(w["SYN_HKG_LIKE"]["D"][2, t]) for t in range(T)]
    return dict(
        check_id="c4a",
        expected_pattern="D_HKG_like(g2, t*=2020) in [0.75, 0.95] (85% +/- 10 pp, widened for source caveats).",
        synthetic_value=f"D_HKG_like(g2, 2020) = {v:.6f} (band [0.75, 0.95]); 1970-2025 range "
                        f"[{min(path):.4f}, {max(path):.4f}]",
        verdict=_verdict_fail(ok), note=(
            "The 85% anchor is senior-secondary-only, second-hand and of low survey robustness "
            "(PRE_DECLARATIONS.md sec.7); the band is wide on purpose. This is a reproduction of a "
            "declared level, not a validation."),
        sub={"c4a_D_HKG_g2_2020_in_band": (ok, v),
             "c4a_D_HKG_g2_path_min": (None, min(path)),
             "c4a_D_HKG_g2_path_max": (None, max(path))})


def check_c4b(w, beh):
    i20 = DECLARED_COMPARISON_YEAR - YEAR_START
    ds = {k: float(w[k]["Dstar"][i20]) for k in TYPE_ORDER}
    g1 = ds["SYN_HKG_LIKE"] - ds["SYN_PHL_LIKE"]
    g2 = ds["SYN_PHL_LIKE"] - ds["SYN_KHM_LIKE"]
    ok = (g1 >= C4B_GAP1) and (g2 >= C4B_GAP2)
    i20_ = DECLARED_COMPARISON_YEAR - YEAR_START
    gd = "; ".join("%s g1..g3 = %.4f/%.4f/%.4f, nu = %.2f/%.2f/%.2f, D* = %.4f" % (
        k.replace("SYN_", "").replace("_LIKE", ""),
        float(w[k]["D"][1, i20_]), float(w[k]["D"][2, i20_]), float(w[k]["D"][3, i20_]),
        w[k]["ci"]["nu"][1], w[k]["ci"]["nu"][2], w[k]["ci"]["nu"][3],
        float(w[k]["Dstar"][i20_])) for k in TYPE_ORDER)
    sub = {
        "c4b_channel_decomposition_2020": (None, gd),
        "c4b_gap_Dstar_HKG_minus_PHL_ge_0.10": (g1 >= C4B_GAP1, g1),
        "c4b_gap_Dstar_PHL_minus_KHM_ge_0.05": (g2 >= C4B_GAP2, g2),
        "c4b_Dstar_HKG_2020": (None, ds["SYN_HKG_LIKE"]),
        "c4b_Dstar_PHL_2020": (None, ds["SYN_PHL_LIKE"]),
        "c4b_Dstar_KHM_2020": (None, ds["SYN_KHM_LIKE"]),
    }
    return dict(
        check_id="c4b",
        expected_pattern=("D*_HKG - D*_PHL >= 0.10 AND D*_PHL - D*_KHM >= 0.05 at t*=2020, on the "
                          "cohort-incidence statistic D* = sum_g nu_g D_g (g1-g3)."),
        synthetic_value=(f"D*(2020): HKG {ds['SYN_HKG_LIKE']:.4f}, PHL {ds['SYN_PHL_LIKE']:.4f}, "
                         f"KHM {ds['SYN_KHM_LIKE']:.4f}; gaps {g1:+.4f} and {g2:+.4f}"),
        verdict=_verdict_fail(ok), note=(
            "DECLARED SYNTHETIC-REPRODUCTION CHECK (S1 note item 2): the on-disk headline rates "
            "(HKG 85% senior-secondary, PHL 46.5% all-basic, KHM 68.4% two-school Grade-9) do NOT "
            "establish this ordering; they are different stages and sampling frames. D* is driven by "
            "observed out-of-school exposure (nu), so a PASS would say the declared exposure weights "
            "reproduce the ordering, not that any country's incidence orders that way."),
        sub=sub, ds=ds, gaps=(g1, g2))


def shadow_code_audit():
    """c4c: code inspection for any country-specific behavioural parameter."""
    fns = [shadow_demand, credential_value, gate_state, gate_numbers,
           shadow_quintile_income, shadow_block]
    src = "".join(inspect.getsource(f) for f in fns)
    forbidden = ["SYN_HKG_LIKE", "SYN_PHL_LIKE", "SYN_KHM_LIKE", "SYN00", "HKG", "PHL",
                 "KHM", "cp[", "country ==", "name ==", "phi_dict", "delta_HKG"]
    found = [t for t in forbidden if t in src]
    beh_keys = set(SHADOW_BEHAV.keys())
    country_keys = [k for k in beh_keys
                    if k in ("SYN_HKG_LIKE", "SYN_PHL_LIKE", "SYN_KHM_LIKE", "HKG", "PHL", "KHM")]
    delta_keys = sorted(SHADOW_BEHAV["delta"].keys())
    input_keys = sorted({kk for v in SHADOW_COUNTRY_INPUTS.values() for kk in v})
    behavioural = {"a_0", "a_g", "b_Z", "b_V", "b_D", "b_y", "b_F", "delta", "w_Q", "w_pi",
                   "w_kappa", "r_EAP", "H", "dS", "omega", "zq"}
    extra_beh = sorted(beh_keys - behavioural)
    info = dict(functions_audited=[f.__name__ for f in fns],
                source_lines=len(src.strip().splitlines()),
                forbidden_tokens_found=found,
                behavioural_keys=sorted(beh_keys),
                behavioural_keys_not_declared=extra_beh,
                country_specific_behavioural_keys=country_keys,
                delta_keys=delta_keys,
                country_input_keys=input_keys,
                country_types=sorted(SHADOW_COUNTRY_INPUTS.keys()))
    ok = (not found and not country_keys and not extra_beh
          and delta_keys == [0, 1, 2, 3, 4]
          and info["country_input_keys"] == ["nu", "oos_upper", "phi", "s", "sigma"])
    return ok, info


def check_c4c(w, beh):
    ok, info = shadow_code_audit()
    return dict(
        check_id="c4c",
        expected_pattern=("Code inspection: NO country-specific value of a_g, b_Z, b_V, b_D, b_y, b_F, "
                          "delta_g. Every country-varying quantity is in the declared input table and in "
                          "results/shadow_country_inputs_audit.csv. If any exists, c4 is VOID."),
        synthetic_value=(f"behavioural keys {len(info['behavioural_keys'])} (gate-indexed only), "
                         f"country-specific behavioural keys: {len(info['country_specific_behavioural_keys'])}, "
                         f"forbidden tokens in behavioural functions: {len(info['forbidden_tokens_found'])}, "
                         f"declared country inputs: {info['country_input_keys']}"),
        verdict="PASS" if ok else "FAIL",
        note=("VOID rule (sec.8 c4c): a single country-specific behavioural parameter makes the whole of "
              "c4 VOID. The host-country assignment (which v1.2 country carries which declared bundle) is "
              "DATA, is recorded in the audit CSV, and is not a behavioural coefficient."),
        sub={"c4c_no_country_specific_behavioural_coefficient": (ok, "none") if ok else (
            False, ",".join(info["forbidden_tokens_found"] + info["country_specific_behavioural_keys"]))},
        info=info)


def check_c5(w, beh):
    """c5 identities on every scored row (all 3 types x 5 gates x 56 years)."""
    fail = []
    worst = dict(p_lo=1.0, p_hi=0.0, D_lo=1.0, D_hi=0.0, omega=abs(sum(beh["omega"]) - 1.0),
                 pi_lo=1.0, pi_Pi_lo=1.0, Pi_minus_pi0=1e18, S_lo=1e18, dstar_over_expo=0.0,
                 tut_over_cohort_g13=0.0, tut_over_cand_g4=0.0, d0_minus_d1=-1e18, nan=0)
    for tname in TYPE_ORDER:
        d = w[tname]
        for g in GATES:
            for t in range(T):
                for q in range(5):
                    pq = float(d["p"][g, q, t])
                    worst["p_lo"] = min(worst["p_lo"], pq); worst["p_hi"] = max(worst["p_hi"], pq)
                    if not (0.0 <= pq <= 1.0) or pq != pq or pq in (float("inf"), float("-inf")):
                        fail.append((tname, g, int(YEARS[t]), "p_q", pq))
                D = float(d["D"][g, t]); pi0 = float(d["pi0"][g, t])
                pi1 = float(d["pi1"][g, t]); Pi = float(d["Pi"][g, t])
                S = float(d["S"][g, t]); R = float(d["R"][g, t]); Q = float(d["Q"][g, t])
                worst["D_lo"] = min(worst["D_lo"], D); worst["D_hi"] = max(worst["D_hi"], D)
                worst["pi_lo"] = min(worst["pi_lo"], pi0, pi1)
                worst["pi_Pi_lo"] = min(worst["pi_Pi_lo"], Pi)
                worst["Pi_minus_pi0"] = min(worst["Pi_minus_pi0"], Pi - pi0)
                worst["S_lo"] = min(worst["S_lo"], S)
                if not (0.0 <= D <= 1.0):
                    fail.append((tname, g, int(YEARS[t]), "D", D))
                if not (0.01 <= pi0 <= 1.0 and 0.01 <= pi1 <= 1.0 and 0.01 <= Pi <= 1.0):
                    fail.append((tname, g, int(YEARS[t]), "pi_bounds", (pi0, pi1, Pi)))
                if Pi < pi0 - 1e-12:
                    fail.append((tname, g, int(YEARS[t]), "Pi_lt_pi0", (Pi, pi0)))
                if S < 0.0:
                    fail.append((tname, g, int(YEARS[t]), "S_neg", S))
                if not all(np.isfinite([D, pi0, pi1, Pi, S, R, Q])):
                    worst["nan"] += 1
                    fail.append((tname, g, int(YEARS[t]), "nonfinite", None))
    # D* <= exposure, and the tutored-headcount bound
    for tname in TYPE_ORDER:
        d = w[tname]
        for t in range(T):
            ds = float(d["Dstar"][t])
            worst["dstar_over_expo"] = max(worst["dstar_over_expo"], ds / max(d["exposure"], 1e-12))
            if ds > d["exposure"] + 1e-12:
                fail.append((tname, 0, int(YEARS[t]), "Dstar_gt_exposure", ds))
            for g, srcL in ((1, 0), (2, 1), (3, 2)):
                tut = float(d["D"][g, t]) * float(d["cand"][g, t])
                bnd = float(d["r"]["C"][srcL, t])
                rt = tut / max(bnd, 1e-9)
                worst["tut_over_cohort_g13"] = max(worst["tut_over_cohort_g13"], rt)
                if tut > bnd * (1.0 + 1e-12):
                    fail.append((tname, g, int(YEARS[t]), "tutored_gt_cohort", rt))
            tut4 = float(d["D"][4, t]) * float(d["cand"][4, t])
            rt4 = tut4 / max(float(d["cand"][4, t]), 1e-9)
            worst["tut_over_cand_g4"] = max(worst["tut_over_cand_g4"], rt4)
            if tut4 > float(d["cand"][4, t]) * (1.0 + 1e-12):
                fail.append((tname, 4, int(YEARS[t]), "tutored_gt_candidates", rt4))
            worst["d0_minus_d1"] = max(worst["d0_minus_d1"],
                                       float(d["D"][0, t]) - float(d["D"][1, t]))
            if not float(d["D"][0, t]) < float(d["D"][1, t]):
                fail.append((tname, 0, int(YEARS[t]), "Dg0_ge_Dg1", float(d["D"][0, t])))
    omega_ok = abs(sum(beh["omega"]) - 1.0) <= 1e-12
    ok = (len(fail) == 0) and omega_ok
    sub = {
        "c5_p_and_D_in_0_1": (all(f[3] not in ("p_q", "D") for f in fail),
                              f"p in [{worst['p_lo']:.4g},{worst['p_hi']:.4g}], "
                              f"D in [{worst['D_lo']:.4g},{worst['D_hi']:.4g}]"),
        "c5_sum_omega_eq_1": (omega_ok, sum(beh["omega"])),
        "c5_pi0_pi1_Pi_in_bounds": (all(f[3] != "pi_bounds" for f in fail),
                                    f"min pi = {worst['pi_lo']:.6g}"),
        "c5_Pi_ge_pi0": (all(f[3] != "Pi_lt_pi0" for f in fail), worst["Pi_minus_pi0"]),
        "c5_S_ge_0": (worst["S_lo"] >= 0.0, worst["S_lo"]),
        "c5_Dstar_le_exposure": (worst["dstar_over_expo"] <= 1.0 + 1e-12, worst["dstar_over_expo"]),
        "c5_tutored_le_source_cohort_g1_g3": (worst["tut_over_cohort_g13"] <= 1.0 + 1e-12,
                                              worst["tut_over_cohort_g13"]),
        "c5_tutored_le_candidates_g4": (worst["tut_over_cand_g4"] <= 1.0 + 1e-12,
                                        worst["tut_over_cand_g4"]),
        "c5_no_nan_or_inf": (worst["nan"] == 0, worst["nan"]),
        "c5_Dg0_lt_Dg1_every_year": (all(f[3] != "Dg0_ge_Dg1" for f in fail),
                                     worst["d0_minus_d1"]),
    }
    return dict(
        check_id="c5",
        expected_pattern=("Every scored row: p,D in [0,1]; sum omega = 1; pi0,pi1,Pi in [0.01,1] and "
                          "Pi >= pi0; S >= 0; D* <= sum nu; tutored head-count <= cohort at gate; no "
                          "NaN/inf; D(g0) < D(g1)."),
        synthetic_value=(f"{len(fail)} identity violations over {len(TYPE_ORDER) * len(GATES) * T} "
                         f"country-gate-years; p in [{worst['p_lo']:.4g},{worst['p_hi']:.4g}], "
                         f"D in [{worst['D_lo']:.4g},{worst['D_hi']:.4g}], max D*/exposure "
                         f"{worst['dstar_over_expo']:.4g}"),
        verdict=_verdict_fail(ok),
        note=("The tutored-headcount bound uses the source-level cohort C[src] for g1-g3 and the "
              "candidate pool for g4 (no cohort exists at the labour gate); see IMPLEMENTATION_NOTE_N1.md."),
        sub=sub, fails=fail)


def check_c6(ablation_path, v12_path):
    if not Path(v12_path).exists():
        return dict(check_id="c6", expected_pattern="shadow OFF -> v1.3 panel byte-identical to v1.2 panel",
                    synthetic_value="v1.2 panel absent", verdict="VOID",
                    note="c6 is VOID when the frozen v1.2 panel is absent (sec.8).", sub={})
    a = sha256_file(ablation_path)
    b = sha256_file(v12_path)
    ok = (a == b)
    return dict(
        check_id="c6",
        expected_pattern=("With the shadow block switched off the v1.3 panel reproduces "
                          "generator_v1_2/results/synthetic_panel_v1_2.csv byte-for-byte (sha256 equality)."),
        synthetic_value=f"ablation sha256 {a} vs v1.2 sha256 {b}; match={ok}",
        verdict=_verdict_fail(ok),
        note=("The ablation artifact is written with exactly v1.2's 67 columns, row order and %.10g "
              "formatting; a mismatch would mean the shadow block leaked into v1.2 arithmetic."),
        sub={"c6_sha256_byte_identical": (ok, a)}, shas=(a, b))


# --------------------------------------------------------------------------------------
# outputs
# --------------------------------------------------------------------------------------
def write_checks(checks, outdir):
    cols = ["check_id", "expected_pattern", "synthetic_value", "verdict", "note"]
    with open(Path(outdir) / "shadow_checks_v1_3.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols + ["label"], lineterminator="\n")
        w.writeheader()
        for c in checks:
            row = {k: c.get(k, "") for k in cols}
            row["label"] = LABEL
            w.writerow(row)
    # detail
    with open(Path(outdir) / "shadow_checks_detail_v1_3.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["check_id", "component", "value", "component_verdict", "label"])
        for c in checks:
            for k, v in c.get("sub", {}).items():
                val = v[1]
                if isinstance(val, float):
                    val = f"{val:.10g}"
                cv = "INFO" if v[0] is None else ("PASS" if v[0] else "FAIL")
                w.writerow([c["check_id"], k, val, cv, LABEL])
            for f in c.get("fails", []):
                w.writerow([c["check_id"] + "_cell_fail",
                            f"{f[0]}|{f[2]}|g{f[1]}|{f[3]}",
                            (f"{f[4]:.10g}" if isinstance(f[4], float) else f[4]),
                            "FAIL", LABEL])
        w.writerow(["c6_ablation", "artifact", "results/_ablation/synthetic_panel_v1_3_shadow_off.csv",
                    "INFO", LABEL])


def write_gates(w, outdir):
    path = Path(outdir) / "shadow_gates_v1_3.csv"
    cols = ["label", "country_type", "host_country", "year", "gate", "gate_name", "Q", "pi0", "pi1",
            "dpi", "Pi", "kappa", "R", "ln_R", "V", "s_g", "D_gate", "spend_share", "D_cohort",
            "cohort_exposure", "Pi_over_pi0", "candidates", "capacity", "advances",
            "p_q1", "p_q2", "p_q3", "p_q4", "p_q5"]
    with open(path, "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        wr.writeheader()
        for tname in TYPE_ORDER:
            d = w[tname]
            for t in range(T):
                for g in GATES:
                    row = dict(label=LABEL, country_type=tname, host_country=d["host"],
                               year=int(YEARS[t]), gate="g%d" % g, gate_name=GATE_NAMES[g],
                               Q=float(d["Q"][g, t]), pi0=float(d["pi0"][g, t]),
                               pi1=float(d["pi1"][g, t]), dpi=float(d["dpi"][g, t]),
                               Pi=float(d["Pi"][g, t]), kappa=float(d["kappa"][g, t]),
                               R=float(d["R"][g, t]), ln_R=float(math.log(max(d["R"][g, t], 1e-12))),
                               V=float(d["V"][g, t]), s_g=float(d["ci"]["s"]),
                               D_gate=float(d["D"][g, t]), spend_share=float(d["S"][g, t]),
                               D_cohort=float(d["Dstar"][t]), cohort_exposure=d["exposure"],
                               Pi_over_pi0=float(d["ratio"][g, t]),
                               candidates=float(d["cand"][g, t]), capacity=float(d["cap"][g, t]),
                               advances=float(d["adv"][g, t]))
                    for q in range(5):
                        row["p_q%d" % (q + 1)] = float(d["p"][g, q, t])
                    wr.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v)
                                 for k, v in row.items()})


def write_decomposition(w, beh, outdir):
    path = Path(outdir) / "shadow_decomposition_v1_3.csv"
    cols = ["label", "country_type", "host_country", "year", "gate", "a_g", "bZ_lnR", "bV_ln1pV",
            "bD_ln1pdpi", "by_ln_y", "minus_bF_fee", "Theta_median_q", "D_gate",
            "share_lnR", "share_ln1pV", "share_ln1pdpi", "income_median_rel"]
    with open(path, "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        wr.writeheader()
        for tname in TYPE_ORDER:
            d = w[tname]; ci = d["ci"]
            ys = shadow_quintile_income(beh, ci["sigma"])
            ymed = ys[2]
            for t in range(T):
                for g in GATES:
                    V = max(0.0, float(d["V"][g, t]))
                    lnR = math.log(max(float(d["R"][g, t]), 1e-12))
                    ln1pV = math.log1p(V)
                    ln1pd = math.log1p(max(float(d["dpi"][g, t]), 0.0))
                    a = beh["a_0"] if g == 0 else beh["a_g"]
                    t_lnR = beh["b_Z"] * lnR
                    t_V = beh["b_V"] * ln1pV
                    t_d = beh["b_D"] * ln1pd
                    t_y = beh["b_y"] * math.log(ymed)
                    t_f = -beh["b_F"] * math.log1p(float(ci["s"]) / ymed)
                    th = a + t_lnR + t_V + t_d + t_y + t_f
                    tot = abs(t_lnR) + abs(t_V) + abs(t_d) + abs(t_y) + abs(t_f)
                    wr.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in dict(
                        label=LABEL, country_type=tname, host_country=d["host"],
                        year=int(YEARS[t]), gate="g%d" % g, a_g=a, bZ_lnR=t_lnR, bV_ln1pV=t_V,
                        bD_ln1pdpi=t_d, by_ln_y=t_y, minus_bF_fee=t_f, Theta_median_q=th,
                        D_gate=float(d["D"][g, t]),
                        share_lnR=(t_lnR / tot if tot > 1e-12 else 0.0),
                        share_ln1pV=(t_V / tot if tot > 1e-12 else 0.0),
                        share_ln1pdpi=(t_d / tot if tot > 1e-12 else 0.0),
                        income_median_rel=ymed).items()})


def write_country_inputs_audit(w, hosts, beh, outdir):
    path = Path(outdir) / "shadow_country_inputs_audit.csv"
    cols = ["label", "country_type", "host_country", "quantity", "value", "unit", "provenance",
            "enters", "is_behavioural"]
    prov = {
        "phi": ("OBSERVED (WDI/ILO 2019, 1 - vulnerable-employment share; declared interpretation)", "V = phi*..."),
        "s": ("DERIVED / DECLARED fee share of mean monthly household income (PARAMETERS.csv C04-C06)", "-b_F ln(1+s/y)"),
        "sigma": ("DECLARED income dispersion; no Gini series on disk (C07-C09)", "y_q/ybar lay-out"),
        "nu": ("DERIVED from observed UIS out-of-school rates + DECLARED split (C10-C12)", "D* = sum_g nu_g D_g"),
        "oos_upper": ("OBSERVED UIS SDG4 2020 (C13)", "constrains nu"),
    }
    with open(path, "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        wr.writeheader()
        for tname in TYPE_ORDER:
            ci = SHADOW_COUNTRY_INPUTS[tname]
            for q in ("phi", "s", "sigma", "nu", "oos_upper"):
                val = ci[q]
                if isinstance(val, dict):
                    val = "; ".join("g%d=%.2f" % (k, v) for k, v in sorted(val.items()))
                wr.writerow(dict(label=LABEL, country_type=tname, host_country=hosts[tname],
                                 quantity=q, value=(f"{val:.10g}" if isinstance(val, float) else val),
                                 unit={"phi": "probability", "s": "share of mean monthly income",
                                       "sigma": "log units", "nu": "share of cohort",
                                       "oos_upper": "percent"}[q],
                                 provenance=prov[q][0], enters=prov[q][1], is_behavioural="no"))
        for k in ("a_0", "a_g", "b_Z", "b_V", "b_D", "b_y", "b_F", "delta", "w_Q", "w_pi",
                  "w_kappa", "r_EAP", "H", "dS", "omega", "zq"):
            wr.writerow(dict(label=LABEL, country_type="ALL THREE (shared rule)", host_country="",
                             quantity=k, value=_f(SHADOW_BEHAV[k]), unit="logit / declared",
                             provenance="DECLARED, frozen (PARAMETERS.csv B01-B23)",
                             enters="Theta / R / V / D*", is_behavioural="YES-shared-gate-indexed"))
        wr.writerow(dict(label=LABEL, country_type="HOST-MAPPING RULE", host_country="",
                         quantity="host_assignment",
                         value="HKG=highest 2020 gdppc; PHL=SYN00_PHL_LIKE; KHM=lowest 2020 gdppc",
                         unit="rule", provenance="IMPLEMENTATION_NOTE.md sec.1 (shadow-blind income rule)",
                         enters="gate state source only (not a demand-equation term)",
                         is_behavioural="no"))


def sensitivity_cells():
    """Pre-declared one-at-a-time grid (PRE_DECLARATIONS.md sec.6, PARAMETERS.csv B03-B17, C05-C09).

    Each cell is (cell_id, parameter, value, beh_variant, inputs_variant_or_None).
    """
    cells = [("central", "central", "central", shadow_beh_variant(), None)]
    for v in (1.2, 2.0, 2.8):
        cells.append((f"b_Z={v:g}", "b_Z", v, shadow_beh_variant(b_Z=v), None))
    for v in (0.5, 1.0, 1.5):
        cells.append((f"b_V={v:g}", "b_V", v, shadow_beh_variant(b_V=v), None))
    for v in (1.0, 2.0, 3.0):
        cells.append((f"b_D={v:g}", "b_D", v, shadow_beh_variant(b_D=v), None))
    for v in (0.3, 0.6, 0.9):
        cells.append((f"b_y={v:g}", "b_y", v, shadow_beh_variant(b_y=v), None))
    for v in (0.4, 0.8, 1.2):
        cells.append((f"b_F={v:g}", "b_F", v, shadow_beh_variant(b_F=v), None))
    for v in (0.15, 0.30, 0.45):
        cells.append((f"delta_g={v:g}", "delta_g", v,
                      shadow_beh_variant(delta={1: v, 2: v, 3: v, 4: v}), None))
    for v in (10.0, 20.0, 30.0):
        cells.append((f"H={v:g}", "H", v, shadow_beh_variant(H=v), None))
    sig = [("low", (0.40, 0.60, 0.55)), ("central", (0.55, 0.80, 0.75)),
           ("high", (0.70, 1.00, 0.95))]
    for lab, trip in sig:
        cells.append((f"sigma={lab}", "sigma", trip, None, ("sigma", trip)))
    for v in (0.02, 0.04, 0.07):
        cells.append((f"s_PHL={v:g}", "s_PHL", v, None, ("s", "SYN_PHL_LIKE", v)))
    for v in (0.01, 0.021, 0.04):
        cells.append((f"s_KHM={v:g}", "s_KHM", v, None, ("s", "SYN_KHM_LIKE", v)))
    return cells


def run_sensitivity(hosts, outdir):
    rows = []
    for cell in sensitivity_cells():
        cid, par, val, beh, inp = cell
        beh = SHADOW_BEHAV if beh is None else beh
        inputs = shadow_inputs_named()
        if inp is not None:
            if inp[0] == "sigma":
                _, trip = inp
                for k, v in zip(TYPE_ORDER, trip):
                    inputs[k]["sigma"] = float(v)
            elif inp[0] == "s":
                col, k, v = inp
                inputs[k]["s"] = float(v)
        res, *_ = run_all(beh=beh, shadow=True, inputs=inputs, hosts=hosts)
        w = shadow_world(res, hosts, inputs, beh)
        c1 = check_c1(w, beh); c2 = check_c2(w, beh); c3 = check_c3(w, beh)
        c4a = check_c4a(w, beh); c4b = check_c4b(w, beh); c5 = check_c5(w, beh)
        c4c_ok, _ = shadow_code_audit()
        i20 = DECLARED_COMPARISON_YEAR - YEAR_START
        rows.append(dict(
            label=LABEL, cell_id=cid, parameter=par, value=(val if isinstance(val, str) else _f(val)),
            D_HKG_g2_2020=float(w["SYN_HKG_LIKE"]["D"][2, i20]),
            Dstar_HKG=float(w["SYN_HKG_LIKE"]["Dstar"][i20]),
            Dstar_PHL=float(w["SYN_PHL_LIKE"]["Dstar"][i20]),
            Dstar_KHM=float(w["SYN_KHM_LIKE"]["Dstar"][i20]),
            c1=c1["verdict"], c2=c2["verdict"], c3=c3["verdict"], c4a=c4a["verdict"],
            c4b=c4b["verdict"], c4c=("PASS" if c4c_ok else "FAIL"), c5=c5["verdict"],
            c1_gap_min_pp=min(c1["gaps"].values()) * 100.0,
            c2_gap_min_pp=min(c2["gaps"].values()) * 100.0,
            max_D_g0=max(float(w[k]["D"][0, :].max()) for k in TYPE_ORDER),
            gap_HKG_PHL=float(c4b["gaps"][0]),
            gap_PHL_KHM=float(c4b["gaps"][1]),
            max_Pi_over_pi0_g1_g3=float(max(w[k]["ratio"][1:4, :].max() for k in TYPE_ORDER)),
        ))
    with open(Path(outdir) / "shadow_sensitivity_v1_3.csv", "w", newline="") as fh:
        cols = list(rows[0].keys())
        wr = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        wr.writeheader()
        for r in rows:
            wr.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in r.items()})
    return rows


def guard_hashes(require_params=True):
    """Frozen-hash guard: refuse to run on any mismatch (sec.10 rule 3)."""
    problems = []
    if not SHADOW_PREDECL.exists():
        problems.append("frozen shadow predeclaration not found: %s" % SHADOW_PREDECL)
    elif sha256_file(SHADOW_PREDECL) != EXPECTED_SHADOW_PREDECL_SHA:
        problems.append("shadow PRE_DECLARATIONS.md sha256 changed: %s" % sha256_file(SHADOW_PREDECL))
    if not SHADOW_S1.exists():
        problems.append("S1 note not found: %s" % SHADOW_S1)
    elif sha256_file(SHADOW_S1) != EXPECTED_SHADOW_S1_SHA:
        problems.append("S1 NOTE sha256 changed: %s" % sha256_file(SHADOW_S1))
    if not PREDECL.exists():
        problems.append("frozen v1.2 predeclaration not found: %s" % PREDECL)
    elif sha256_file(PREDECL) != EXPECTED_PREDECL_SHA:
        problems.append("v1.2 PRE_DECLARATIONS.md sha256 changed: %s" % sha256_file(PREDECL))
    if not LOCAL_PREDECL.exists():
        problems.append("local PRE_DECLARATIONS.md copy not found")
    else:
        txt = LOCAL_PREDECL.read_text()
        for p in (SHADOW_PREDECL, SHADOW_S1):
            if p.read_text() not in txt:
                problems.append("local copy does not contain %s verbatim" % p.name)
    if require_params:
        if not PARAMS_MD.exists():
            problems.append("PARAMS.md not found")
        elif sha256_file(PARAMS_MD) != EXPECTED_PARAMS_SHA:
            problems.append("PARAMS.md sha256 changed: %s" % sha256_file(PARAMS_MD))
    if problems:
        raise SystemExit("REFUSING TO RUN:\n  " + "\n  ".join(problems))
    return True


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "results"))
    ap.add_argument("--manifest", default=str(ROOT / "RUN_MANIFEST.json"))
    ap.add_argument("--smoke", action="store_true", help="smoke test: stop after the ablation + distributions")
    ap.add_argument("--no-sensitivity", action="store_true")
    args = ap.parse_args(argv)
    t0 = time.time()
    guard_hashes()

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    inputs = shadow_inputs_named()

    # ---- 1. shadow-OFF run: byte-identity guard (c6) and the host mapping rule ------
    res_off, *_ = run_all(shadow=False)
    rows_off = build_panel(res_off)
    abl_dir = outdir / "_ablation"; abl_dir.mkdir(parents=True, exist_ok=True)
    abl_path = abl_dir / "synthetic_panel_v1_3_shadow_off.csv"
    write_panel(rows_off, abl_path)
    hosts, gdp = resolve_hosts(res_off)
    print("[v1.3] hosts: " + ", ".join("%s<-%s" % (k, v) for k, v in hosts.items()))

    # ---- 2. scored (shadow ON) run --------------------------------------------------
    res, ptr_obs, spend_obs, S_phl, P_phl = run_all(beh=SHADOW_BEHAV, shadow=True,
                                                    inputs=inputs, hosts=hosts)
    hosts_on, gdp_on = resolve_hosts(res)
    host_map_stable = (hosts_on == hosts)
    if not host_map_stable:
        # Disclosed, not fatal: the declared rule reads the v1.2 (shadow-off) state. The block's
        # feedback can move a host's 2020 GDPpc enough to change an income ranking; that is a
        # property of the feedback loop and is reported as a diagnostic, not used to re-map.
        print("[v1.3] NOTE: host ranking under feedback differs: %r (declared %r)" % (hosts_on, hosts))
    rows = build_panel_v13(res, hosts, inputs)
    write_panel_v13(rows, outdir / "synthetic_panel_v1_3.csv")
    w = shadow_world(res, hosts, inputs, SHADOW_BEHAV)
    write_gates(w, outdir)
    write_decomposition(w, SHADOW_BEHAV, outdir)
    write_country_inputs_audit(w, hosts, SHADOW_BEHAV, outdir)

    if args.smoke:
        for tname in TYPE_ORDER:
            d = w[tname]
            print("[smoke] %-13s host=%-18s D(g0..g4) 2020 = %s | R(g1..g4) 2020 = %s" % (
                tname, d["host"],
                " ".join("%.4f" % d["D"][g, DECLARED_COMPARISON_YEAR - YEAR_START] for g in GATES),
                " ".join("%.3f" % d["R"][g, DECLARED_COMPARISON_YEAR - YEAR_START] for g in (1, 2, 3, 4))))
            print("            R range over 1970-2025 g1..g4: %s" % (
                " | ".join("g%d [%.3f,%.3f]" % (g, d["R"][g, :].min(), d["R"][g, :].max()) for g in (1, 2, 3, 4))))
        print("[smoke] c6 ablation sha %s vs v1.2 %s match=%s" % (
            sha256_file(abl_path), sha256_file(V12_PANEL) if V12_PANEL.exists() else "absent",
            sha256_file(abl_path) == (sha256_file(V12_PANEL) if V12_PANEL.exists() else None)))
        print("[smoke] %.1fs" % (time.time() - t0))
        return None

    # ---- 3. checks -------------------------------------------------------------------
    c1 = check_c1(w, SHADOW_BEHAV)
    c2 = check_c2(w, SHADOW_BEHAV)
    c3 = check_c3(w, SHADOW_BEHAV)
    c4a = check_c4a(w, SHADOW_BEHAV)
    c4b = check_c4b(w, SHADOW_BEHAV)
    c4c = check_c4c(w, SHADOW_BEHAV)
    c5 = check_c5(w, SHADOW_BEHAV)
    c6 = check_c6(abl_path, V12_PANEL)
    if c4c["verdict"] != "PASS":
        c4_verdict = "VOID"
    elif c4a["verdict"] == "PASS" and c4b["verdict"] == "PASS":
        c4_verdict = "PASS"
    elif c4a["verdict"] == "VOID" or c4b["verdict"] == "VOID":
        c4_verdict = "VOID"
    else:
        c4_verdict = "FAIL"
    c4 = dict(check_id="c4", expected_pattern="c4a AND c4b AND c4c (VOID if c4c fails; sec.8).",
              synthetic_value="c4a %s; c4b %s; c4c %s -> c4 %s" % (
                  c4a["verdict"], c4b["verdict"], c4c["verdict"], c4_verdict),
              verdict=c4_verdict,
              note="Aggregate row only; the components below are the scored objects.", sub={})
    checks = [c1, c2, c3, c4, c4a, c4b, c4c, c5, c6]
    write_checks(checks, outdir)

    # ---- 4. sensitivity ---------------------------------------------------------------
    sens = None if args.no_sensitivity else run_sensitivity(hosts, outdir)

    # ---- 5. diagnostics (NOT-SCORED) --------------------------------------------------
    i20 = DECLARED_COMPARISON_YEAR - YEAR_START
    # feedback-loop magnitude: scored (with Pi) vs a run with the substitution disabled?
    # The substitution cannot be disabled without touching v1.2 arithmetic, so the loop's
    # realised size is reported directly from the stored ratios.
    loop = {}
    for tname in TYPE_ORDER:
        d = w[tname]
        # only g1-g3 carry the pool hook; g4 has NO hook (labour gate) and is excluded
        loop[tname] = dict(max_ratio_g1_g3=float(d["ratio"][1:4, :].max()),
                           mean_ratio_g1_g3_2020=float(d["ratio"][1:4, i20].mean()),
                           ratio_g4_2020_not_used=float(d["ratio"][4, i20]))
    # twin comparison (NOT-SCORED): impossible for g1..g3 without declared inputs for the twins.
    sat_by = {}
    for t in TYPE_ORDER:
        for g in (1, 2, 3, 4):
            Dv = w[t]["D"][g, :]
            sat_by["%s|g%d" % (t, g)] = dict(
                cells_scored=int(((Dv >= SAT_LO) & (Dv <= SAT_HI)).sum()),
                cells_below_lo=int((Dv < SAT_LO).sum()),
                cells_above_hi=int((Dv > SAT_HI).sum()),
                D_min=float(Dv.min()), D_median=float(np.median(Dv)), D_max=float(Dv.max()))
    d_hkg = w["SYN_HKG_LIKE"]
    i20_ = DECLARED_COMPARISON_YEAR - YEAR_START
    R_req = required_R_for_D(SHADOW_BEHAV, d_hkg["ci"], 2, float(d_hkg["V"][2, i20_]),
                             float(d_hkg["dpi"][2, i20_]), C4A_LO)
    c4a_gap = dict(target_D=C4A_LO,
                   realised_D=float(d_hkg["D"][2, i20_]),
                   realised_R=float(d_hkg["R"][2, i20_]),
                   realised_lnR=float(math.log(d_hkg["R"][2, i20_])),
                   required_R=R_req, required_lnR=float(math.log(R_req)),
                   required_over_realised=float(R_req / d_hkg["R"][2, i20_]),
                   required_dlnR=float(math.log(R_req / d_hkg["R"][2, i20_])))
    off_by = {r["cp"]["name"]: r for r in res_off}
    host_delta = {}
    for t in TYPE_ORDER:
        nm = hosts[t]
        a = off_by[nm]; b = by_name_on[nm] if False else [x for x in res if x["cp"]["name"] == nm][0]
        host_delta[t] = dict(host=nm,
                             gdppc_2020_off=float(a["Y"][i20_]),
                             gdppc_2020_on=float(b["Y"][i20_]),
                             gdppc_ratio=float(b["Y"][i20_] / a["Y"][i20_]),
                             enrol_upper_2020_off=float(a["enrol"][2, i20_]),
                             enrol_upper_2020_on=float(b["enrol"][2, i20_]),
                             enrol_upper_ratio=float(b["enrol"][2, i20_] / max(a["enrol"][2, i20_], 1e-12)),
                             completion_upper_2020_off=float(a["comp_coh"][2, i20_]),
                             completion_upper_2020_on=float(b["comp_coh"][2, i20_]),
                             enrolment_primary_2020_off=float(a["enrol"][0, i20_]),
                             enrolment_primary_2020_on=float(b["enrol"][0, i20_]),
                             enrol_tertiary_2020_off=float(a["enrol"][3, i20_]),
                             enrol_tertiary_2020_on=float(b["enrol"][3, i20_]),
                             enrol_tertiary_ratio=float(b["enrol"][3, i20_] / max(a["enrol"][3, i20_], 1e-12)))
    sm = dict(loop=loop)
    Path(outdir / "shadow_diagnostics_v1_3.json").write_text(
        json.dumps(dict(label=LABEL, scored=False, note=(
            "NOT-SCORED diagnostics. Not part of the frozen c1-c6 set."),
            feedback_loop=loop,
            saturation=dict(c1_cells_saturated=c1["n_sat"], c2_cells_saturated=c2["n_sat"],
                            by_type_gate=sat_by),
            d_gate_2020={t: {("g%d" % g): float(w[t]["D"][g, i20]) for g in GATES} for t in TYPE_ORDER},
            R_2020={t: {("g%d" % g): float(w[t]["R"][g, i20]) for g in GATES} for t in TYPE_ORDER},
            exposure={t: w[t]["exposure"] for t in TYPE_ORDER},
            Dstar_2020={t: float(w[t]["Dstar"][i20]) for t in TYPE_ORDER},
            c4a_gap_diagnostic=c4a_gap,
            host_v1_2_columns_2020=host_delta,
            hosts=hosts, hosts_under_feedback=hosts_on, host_map_stable=host_map_stable,
            gdp_2020_shadow_off={t: float(gdp[hosts[t]]) for t in TYPE_ORDER},
            gdp_2020_shadow_on={t: float(gdp_on[hosts[t]]) for t in TYPE_ORDER},
            gdp_2020_ratio={t: float(gdp_on[hosts[t]] / gdp[hosts[t]]) for t in TYPE_ORDER},
            D_ratio_gates_2020={t: {("g%d" % g): float(w[t]["ratio"][g, i20]) for g in GATES}
                                for t in TYPE_ORDER}), indent=2, sort_keys=True) + "\n")

    # ---- 6. manifest -------------------------------------------------------------------
    sha = lambda p: sha256_file(p) if Path(p).exists() else None
    manifest = dict(
        label=LABEL,
        statement=("Synthetic data from declared assumptions only. Not evidence, not an estimate, not a "
                   "forecast, no causal or direction claim, no real country modelled. The shadow block is a "
                   "declared household demand rule evaluated on this generator's own gate/queue state."),
        generator="code/sim_v1_3.py",
        spec=dict(
            frozen_shadow_predeclaration="shadow_module/PRE_DECLARATIONS.md",
            frozen_shadow_predeclaration_sha256=EXPECTED_SHADOW_PREDECL_SHA,
            s1_note="shadow_module/PRE_DECLARATIONS_S1_NOTE.md",
            s1_note_sha256=EXPECTED_SHADOW_S1_SHA,
            local_copy="PRE_DECLARATIONS.md",
            local_copy_sha256=sha(LOCAL_PREDECL),
            inherited_v1_2_predeclaration_sha256=EXPECTED_PREDECL_SHA,
            implementation_note="IMPLEMENTATION_NOTE.md",
            implementation_note_sha256=sha(ROOT / "IMPLEMENTATION_NOTE.md"),
            implementation_note_n1="IMPLEMENTATION_NOTE_N1.md",
            implementation_note_n1_sha256=sha(ROOT / "IMPLEMENTATION_NOTE_N1.md"),
        ),
        seed=SEED,
        rng="numpy PCG64 (np.random.default_rng), single stream, v1.2 draw order, shadow block draws nothing",
        panel=dict(countries=N_C, years=[YEAR_START, YEAR_END], levels=list(LEVELS), rows=len(rows)),
        host_mapping=hosts,
        host_mapping_rule="HKG=highest 2020 gdppc; PHL=SYN00_PHL_LIKE; KHM=lowest 2020 gdppc (shadow-blind)",
        host_gdp_2020={k: float(v) for k, v in gdp.items() if k in hosts.values()},
        host_mapping_stable_under_feedback=bool(host_map_stable),
        host_mapping_under_feedback=hosts_on,
        python=platform.python_version(), numpy=np.__version__,
        hashes=dict(
            code_sha256=sha(CODE),
            params_md_sha256=sha(PARAMS_MD),
            frozen_parameters_csv_sha256=sha(SHADOW_DIR / "PARAMETERS.csv"),
            v1_2_code_sha256=sha(V12_DIR / "code" / "sim_v1_2.py"),
            v1_2_panel_sha256=sha(V12_PANEL),
            results={p.name: sha(p) for p in sorted(outdir.glob("*.csv"))},
            ablation={"_ablation/synthetic_panel_v1_3_shadow_off.csv":
                      sha(outdir / "_ablation" / "synthetic_panel_v1_3_shadow_off.csv")},
        ),
        checks_summary={c["check_id"]: c["verdict"] for c in checks},
        sensitivity=dict(cells=len(sens) if sens else 0,
                         file="results/shadow_sensitivity_v1_3.csv"),
        determinism=dict(method="two clean runs into separate output directories, cmp on every results CSV",
                         floats="%.10g", wall_clock_in_outputs=False),
    )
    Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    dt = time.time() - t0
    print(f"[sim_v1_3] {LABEL}: {len(rows)} rows, {dt:.1f}s, seed {SEED}")
    for c in checks:
        print(f"  {c['check_id']}: {c['verdict']}  {c['synthetic_value'][:200]}")
    return checks


if __name__ == "__main__":
    main()
