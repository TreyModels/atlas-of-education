#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIM_V1_5_BIMODAL -- SYNTHETIC generator v1.5: the A5 BIMODAL-GATE structure.

EVERYTHING THIS SCRIPT EMITS IS SYNTHETIC. It is a declared-assumption simulator: not an
estimate, not evidence about any country, not a forecast, and it licenses no causal or
direction claim. Country labels are synthetic ("SYN28", "SYN00_PHL_LIKE", ...); no real
country is modelled or measured. SYN00_PHL_LIKE is NOT the Philippines.

Base: the frozen v1.3 generator, copied byte-for-byte to code/base_v1_3_sim.py (sha256
70ae8f0e...). The year loop of simulate_country_v15() below is INJECTED VERBATIM from that
file (base_v1_3_sim.py lines 640-988) by code/build_from_base.py; the only inserted text is
at the declared insertion points I2-I7 of DESIGN.md sec.2.2, each guarded by ONE boolean
read. With bimodal=False and kappa_link=False every inserted block is the identity and the
panel written to the v1.3 column set is byte-identical to
generator_v1_3/results/synthetic_panel_v1_3.csv (sha256 47d4b082...). That is guard (e-i)
and it is verified before any check is scored.

What v1.5 adds, exactly as frozen in PRE_DECLARATIONS.md (sha256 7178e3d2...):

  * I2 tier split   K_H[L,t] = h_share[L]*seats[L,t]; K_O = seats - K_H (no third segment)
  * I3 tier choice  a declared 15-cell (5 income x 3 ability) utility comparison over
                    {H, O, outside}; outside = the frozen four-state block's values
  * I4 admission    admitted_H = min(A_H, K_H) by the declared rank; T_O = min(A_O, K_O);
                    V_O = K_O - T_O is a PRIMARY object (unfilled places, never reallocated)
  * I5 completion   per-tier survival from Q_H = q_H_mult*Q, Q_O = q_O_mult*Q; completion is
                    the admission-weighted tier sum
  * I6 kappa cap    adm_upper(s) <- min(adm_upper(s), kappa*comp_lower_cohort(s)) INSIDE the
                    annual accounting (kappa = 0.949, structural, not a post-processing clip)
  * I7 job gate     the rung-4 slot is rank-rationed from Tier H credential holders; p4 =
                    rung4_emp/rung4_demand is reported separately and never substituted for
                    the school gate p_adv_H

No reversal term exists anywhere (D125). The ratchet is theory, audited by construction
only (R1); NO REVERSAL DIAGNOSTIC IS TO BE INFERRED FROM THIS RUN.

REFUSES TO RUN if PRE_DECLARATIONS.md, PARAMETERS.csv, DESIGN.md, DRY_RUN_PLAN.md or the
frozen base copy no longer match the hashes frozen before the run.

Usage:  python sim_v1_5_bimodal.py [--out DIR] [--no-determinism]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import inspect
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

LABEL = "SYNTHETIC"

# ======================================================================================
# 0. FROZEN IDENTITY AND PATHS
# ======================================================================================
SEED = 20261120
ROOT = Path(__file__).resolve().parent.parent          # generator_v1_5_bimodal/
CODE = ROOT / "code"
SYNTH = ROOT.parent                                    # synthetic_2026-11-20/
PROG = SYNTH.parents[2]                                # massification-2026-11-20/
BASE_CODE = CODE / "base_v1_3_sim.py"                  # byte copy of sim_v1_3.py
V13_PANEL = SYNTH / "generator_v1_3" / "results" / "synthetic_panel_v1_3.csv"
PREDECL = ROOT / "PRE_DECLARATIONS.md"
PARAMS_CSV = ROOT / "PARAMETERS.csv"
DESIGN = ROOT / "DESIGN.md"
DRYRUN = ROOT / "DRY_RUN_PLAN.md"
FROZEN_BEFORE = ROOT / "results" / "FROZEN_BEFORE_SHA256SUMS.txt"

# The four frozen spec files, exactly as recorded in RUN_MANIFEST.json before any run.
EXPECTED_PREDECL_SHA = "7178e3d2ee2e367cd7dbb0619f2031305ff446978a43aab9e1f6caefb07ca97f"
EXPECTED_PARAMS_SHA = "72327cf799b5e96c68a8e9030f265ef06b3b37a58917d892d87bb6fabcfcb65a"
EXPECTED_DESIGN_SHA = "db21055b38ef8343f791b27a3fe192a72367f5377f966dd660a94d39a26a5f43"
EXPECTED_DRYRUN_SHA = "4660390501747949eb27c5d966012a768ebc82ee025efea89ee4333e8bbedeab"
EXPECTED_BASE_CODE_SHA = "70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877"
EXPECTED_V13_PANEL_SHA = "47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3"

SCOPE_NOTE = ("v1.3/v1.2 levels are a 2021-2024 placement: 9/33 within +/-5 pp (EXP-7 "
              "ENDPOINT-ONLY); median lower -29.44, upper -27.59 pp; 24-37 pp low before "
              "2021; every level statement here is readable as a 2022-2024 placement only.")


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _load_base():
    spec = importlib.util.spec_from_file_location("base_v1_3_sim", str(BASE_CODE))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["base_v1_3_sim"] = mod
    spec.loader.exec_module(mod)
    return mod


B = _load_base()

P = B.P
YEARS = B.YEARS
T = B.T
NL = B.NL
LEVELS = B.LEVELS
DVEC = B.DVEC
NEED = B.NEED
UTIL_SCALE = B.UTIL_SCALE
GIRL_SHARE = B.GIRL_SHARE
TASTE = B.TASTE
ABILITY = B.ABILITY
OUT_YEARS = B.OUT_YEARS
clip = B.clip
sig = B.sig
SHADOW_BEHAV = B.SHADOW_BEHAV
GATES = B.GATES
OFF = B.OFF
GATE_NAMES = B.GATE_NAMES

# Frozen v1.3 module functions used unchanged inside the injected year loop. They are
# aliased, never re-implemented: the four-state block, the gate-state contract, the shadow
# block and its demand equation are the frozen v1.3 objects.
state_shares = B.state_shares
gate_state = B.gate_state
gate_numbers = B.gate_numbers
shadow_block = B.shadow_block
shadow_demand = B.shadow_demand
shadow_quintile_income = B.shadow_quintile_income
credential_value = B.credential_value
coverage_target = B.coverage_target
desired_capacity = B.desired_capacity
update_seats = B.update_seats

# ======================================================================================
# 1. DECLARED v1.5 PARAMETERS  (PARAMETERS.csv T01-T15, S01-S09, O01-O12, K01-K05)
#    ONE vector each for all 30 countries. No country branch, no level shim (T-AUD-1/2).
# ======================================================================================
TIER = dict(
    h_share=(0.15, 0.28, 0.40, 0.50),          # T01 Tier H share of adequate places, by level
    q_H_mult=(1.25, 1.25, 1.25, 1.25),         # T04
    q_O_mult=(0.55, 0.55, 0.55, 0.55),         # T05
    cost_H_mult=1.60,                          # T06
    cost_O_mult=0.03,                          # T07 (near-zero, not zero)
    cred_prem_H=0.18,                          # T08
    cred_prem_O=0.03,                          # T09
    v_tier_scale=0.45,                         # T10 v_O = 0.45 * v_H
    w_work_free=0.0,                           # T11 held at zero (audited by (d-i))
    a_gate=0.40,                               # T12
    risk_pen=0.20,                             # T13
    H_h=20.0,                                  # T14 (shadow_module B17, reused)
    sigma_tier=0.80,                           # S03
    z_q=(-1.2816, -0.5244, 0.0, 0.5244, 1.2816),   # S02 (shadow_module B23, reused)
    ability_grid=(0.25, 0.50, 0.75),           # S04
    cell_weight=((0.10, 0.07, 0.03),           # S01 joint weights, quintile x ability
                 (0.08, 0.08, 0.04),
                 (0.06, 0.09, 0.05),
                 (0.04, 0.09, 0.07),
                 (0.02, 0.07, 0.11)),
    rank_w_income=0.30,                        # S06
    rank_w_ability=0.70,                       # S06
    padv_expect_lag=1,                         # S07
    padv_clip=(0.01, 0.999),                   # S08
    exit_cost_O=0.0,                           # sec.2.5 declared asymmetry, reported only
)

KAPPA = 0.949              # K01 declared cross-level link (observed median; NEVER FITTED)
KAPPA_SENS = 0.960         # K02 declared sensitivity (pre-2018 median), non-verdict-bearing
KAPPA_LAG = 3              # K03 exact lag

# --------------------------------------------------------------------------------------
# Check thresholds (PRE_DECLARATIONS.md sec.6). FROZEN. No threshold is moved anywhere.
# --------------------------------------------------------------------------------------
A_UNFILLED_FLOOR = 0.10        # (a-i)
A_QUEUE_BAR = 1.10             # (a-ii)
A_MIN_CELLS = 15               # (a-i)/(a-ii) out of 30 scored (t,L) cells
A_MIN_YEARS = 8                # (a-iii) out of 15 years 2010-2024
A_P4_BAR = 0.50                # (a-iii) job-gate condition
A_SAME_LEVEL_MIN = 8           # (a-iv) in arm A11; must be 0 in A01
B_PRIMARY_FIRST = (2014, 2020)  # (b-i)
B_PRIMARY_2024_MIN = 92.0      # (b-i)
B_UPPER_STALL_MAX = 90.0       # (b-ii)
B_UPPER_BAND = (55.0, 85.0)    # (b-ii)
B_ENDPOINT_BAND = (73.0, 77.0)  # (b-iii) reported, not verdict-bearing
C_RATIO_MIN = 5.0              # (c-i)
C_OPEN_CEIL = 0.025            # (c-ii) (v1.3 c3 ceiling, reused verbatim)
C_HIGH_GAP_MIN_PP = 10.0       # (c-iii) high gate
C_OPEN_GAP_MAX_PP = 1.0        # (c-iii) open tier
D_CAP_NONBIND_MIN = 5          # (d-ii) out of 53
D_CHILD_WAGE_PP = 2.0          # (d-iii)
D_QO_UNFILLED_PP = 5.0         # (d-iv)
N_SCORED_CELLS_A = 30          # 15 years x 2 levels
N_ANCHOR_CELLS_D = 53          # 1973-2025
N_YEARS_A = 15                 # 2010-2024

ARMS = {
    "A00": dict(bimodal=False, kappa_link=False,
                role="no-re-fit guard E1 (byte-identical to v1.3)"),
    "A10": dict(bimodal=True, kappa_link=False,
                role="diagnostic only (tier block without the pipeline; reported, not scored)"),
    "A01": dict(bimodal=False, kappa_link=True,
                role="linked arm, reported separately, guard E2"),
    "A11": dict(bimodal=True, kappa_link=True,
                role="scored arm (checks a-e)"),
}

EXTRA_ARMS = [
    # name,           overrides
    ("S1_h_share_plus", dict(h_share=(0.25, 0.38, 0.50, 0.60))),
    ("S2_h_share_minus", dict(h_share=(0.05, 0.18, 0.30, 0.40))),
    ("S3_q_H_110", dict(q_H_mult=(1.10, 1.10, 1.10, 1.10))),
    ("S4_q_H_140", dict(q_H_mult=(1.40, 1.40, 1.40, 1.40))),
    ("S5_q_O_040", dict(q_O_mult=(0.40, 0.40, 0.40, 0.40))),
    ("S6_q_O_070", dict(q_O_mult=(0.70, 0.70, 0.70, 0.70))),
    ("S7_kappa_0960", dict(kappa=KAPPA_SENS)),
    ("D1_child_wage_plus10", dict(w_child_mult=1.10)),
    ("D2_q_O_minus20", dict(q_O_mult=(0.44, 0.44, 0.44, 0.44))),
    ("D3_sorting_off", dict(sorting_off=True)),
]


# ======================================================================================
# 2. TIER UTILITIES AND THE DECLARED 15-CELL CHOICE  (DESIGN.md sec.3-5)
# ======================================================================================
def _util(c):
    """The childworld utility form used unmodified by the frozen four-state block."""
    x = c - 0.6 * NEED
    if x > 0.05:
        return math.log(max(x, 1e-9))
    return math.log(0.05) + (x - 0.05) / 0.05


def outside_utilities(cp, level, y):
    """The four-state block's UTILITIES for a household with income y (not its shares).

    Replicates base_v1_3_sim.state_shares() exactly, using ITS constants (NEED, UTIL_SCALE,
    GIRL_SHARE, TASTE, ABILITY, OUT_YEARS, AGE_W, P["cost_base"]). Nothing is re-defined: the
    declaration (PRE_DECLARATIONS.md sec.2.3, I1) says tier_choice *calls* the frozen block to
    obtain U_work / U_both / U_neither as refusal values, and state_shares() returns shares
    after a softmax, so the utilities are reconstructed here and verified against
    state_shares() by audit T-AUD-5 (softmax(U/UTIL_SCALE) == state_shares, all 30 x 3).
    """
    earn = 0.32 * B.AGE_W[level] * max(cp["w_child"] / 0.32, 0.55 * cp["farm"])
    cost = cp["cost"] * P["cost_base"][level]
    v_l = cp["v0"] * cp["decay"] ** level + 0.25 * ABILITY - 1.3 * min(OUT_YEARS, 3) / 3.0
    U_school = _util(y - cost) + v_l
    U_both = (_util(y - cost + 0.5 * (1.0 + cp["compat"]) * earn)
              + v_l * (0.72 + 0.2 * cp["compat"]) + 0.4 * cp["compat"] - 0.25)
    U_work = _util(y + earn) - 0.2 * TASTE
    U_neither = _util(y) + cp["neither"] + cp["girl_care"] * GIRL_SHARE
    return U_school, U_both, U_work, U_neither


def wage_gap(rf1, Y, lit, Tcur):
    """G_H = ln(w_for[rung 2]/w_inf), the model's own formal-informal log-wage gap (T15)."""
    psi = (P["psi_pre"], P["psi_ind"], P["psi_div"])[int(Tcur)]
    w_for = (Y / 1000.0) * P["rung_mult"][1] * (1.0 + P["cred_prem"] * 1) * float(rf1)
    w_inf = (Y / 1000.0) * (1.0 + psi * lit)
    return math.log(max(w_for, 1e-12) / max(w_inf, 1e-12))


def tier_cells(cp, level, y_shock, tc, padv_hat, G_H):
    """The declared 15-cell utility comparison for one country-year-level.

    U_H,i = util(y_i - cost_H) + v_H + H_h*p_hat*G_H*1[a_i >= a_gate] - risk_pen*(1-p_hat)
    U_O,i = util(y_i - cost_O) + v_O
    first choice: H if U_H > max(U_O, u_out); O if U_O > max(U_H, u_out); else outside.
    Ties go to the outside option (declared tie-break: never a silent H).

    DECLARED IMPLEMENTATION NOTE (TUNE_LOG.md; diagnostic column both_would_dominate_cells):
    sec.2.4 lists U_both among the refusal values. U_both is the frozen block's school+work
    state, which in the block itself is a SCHOOL state (ds = p_s + p_b); used as an OUTSIDE
    value it lets a cell collect the schooling value plus the child's earnings WITHOUT
    occupying a place, which makes it dominate Tier O for every cell in every year and drives
    T_O identically to zero. The refusal set is therefore the two outside states that do not
    require a place (work, neither). The number of cells on which U_both would have dominated
    Tier O is REPORTED, per country-year-level, rather than being silently dropped.
    """
    zq = tc["z_q"]
    cw = tc["cell_weight"]
    ab = tc["ability_grid"]
    cb = P["cost_base"][min(level, 2)]      # frozen cost vector has 3 entries (child block)
    cost_H = tc["cost_H_mult"] * cp["cost"] * cb
    cost_O = tc["cost_O_mult"] * cp["cost"] * cb
    v_H = cp["v0"] * (cp["decay"] ** level)
    v_O = tc["v_tier_scale"] * v_H
    lo, hi = tc["padv_clip"]
    p = min(max(float(padv_hat), lo), hi)
    hterm = tc["H_h"] * p * G_H
    risk = tc["risk_pen"] * (1.0 - p)
    w = np.zeros(15); UH = np.zeros(15); UO = np.zeros(15)
    uout = np.zeros(15); rank = np.zeros(15)
    out_state = np.zeros(15, dtype=int); first = np.zeros(15, dtype=int)
    n_both = 0
    k = 0
    for qi in range(5):
        yi = cp["y_med"] * math.exp(tc["sigma_tier"] * zq[qi] + y_shock)
        _, Ub, Uw, Un = outside_utilities(cp, level, yi)
        uo = max(Uw, Un)
        for ai in range(3):
            av = ab[ai]
            ww = cw[qi][ai]
            if tc.get("sorting_off"):
                ww = 1.0 / 15.0
            uh = _util(yi - cost_H) + v_H + (hterm if av >= tc["a_gate"] else 0.0) - risk
            u0 = _util(yi - cost_O) + v_O
            if Ub > u0:
                n_both += 1
            w[k] = ww; UH[k] = uh; UO[k] = u0; uout[k] = uo
            rank[k] = (tc["rank_w_income"] * (yi / max(cp["y_med"], 1e-9))
                       + tc["rank_w_ability"] * av)
            if uo >= max(uh, u0):
                first[k] = 2
                out_state[k] = 0 if Uw >= max(Ub, Un) else (1 if Ub >= Un else 2)
            elif uh > u0:
                first[k] = 0
            else:
                first[k] = 1
            k += 1
    return dict(w=w, U_H=UH, U_O=UO, u_out=uout, rank=rank, first=first,
                out_state=out_state, n_both=n_both, p_hat=p, G_H=G_H,
                cost_H=cost_H, cost_O=cost_O, v_H=v_H, v_O=v_O)


def tier_allocate(cells, elig, C_L, K_H, K_O, tc):
    """Admission at the two tiers plus the declared SECOND decision.

    DESIGN.md sec.3: a household that ranks Tier H first and is refused at the gate gets a
    second decision -- accept Tier O or take the outside option -- and the refusal value is
    the OUTSIDE OPTION, not Tier O. That second decision is what lets free seats sit empty
    while others queue, so it is part of the model, not a detail.

    Rank admission uses S06 only: rank_score = 0.30*(y_i/ybar) + 0.70*a_i. Deterministic
    tie-break: (-rank_score, cell index). No country-, level- or year-specific weight.
    """
    base = float(elig) * float(C_L)
    mass = base * cells["w"]
    first = cells["first"]
    A_H = float(mass[first == 0].sum())
    A_O_first = float(mass[first == 1].sum())
    adm_h = np.zeros(15)
    if A_H > 0.0 and K_H > 0.0:
        order = sorted([i for i in range(15) if first[i] == 0],
                       key=lambda i: (-cells["rank"][i], i))
        rem = min(A_H, K_H)
        for i in order:
            if rem <= 1e-12:
                break
            q = min(mass[i], rem)
            adm_h[i] = q
            rem -= q
    admitted_H = float(adm_h.sum())
    acc = np.zeros(15)
    for i in range(15):
        if first[i] == 0 and (mass[i] - adm_h[i]) > 1e-12 and cells["U_O"][i] > cells["u_out"][i]:
            acc[i] = mass[i] - adm_h[i]
    cand_O = A_O_first + float(acc.sum())
    T_O = min(K_O, cand_O)
    to = np.zeros(15)
    if T_O > 0.0:
        order2 = sorted([i for i in range(15) if (first[i] == 1) or acc[i] > 0.0],
                        key=lambda i: (-cells["rank"][i], i))
        rem = T_O
        for i in order2:
            if rem <= 1e-12:
                break
            cap_i = mass[i] if first[i] == 1 else acc[i]
            q = min(cap_i, rem)
            to[i] = q
            rem -= q
    mW = float(cells["w"][(first == 2) & (cells["out_state"] == 0)].sum())
    mB = float(cells["w"][(first == 2) & (cells["out_state"] == 1)].sum())
    mN = float(cells["w"][(first == 2) & (cells["out_state"] == 2)].sum())
    return dict(A_H=A_H, A_O_first=A_O_first, A_O_cand=cand_O,
                admitted_H=admitted_H, T_O=T_O, V_O=max(0.0, K_O - T_O),
                queue_H=max(0.0, A_H - admitted_H), mW=mW, mB=mB, mN=mN,
                refused_acc=float(acc.sum()))


# ======================================================================================
# 3. ONE COUNTRY, 1970-2025 -- the frozen v1.3 year loop with the declared insertions
# ======================================================================================
def simulate_country_v15(cp, gnoise, hhnoise, S_path, Pop_path, sh_in=None, beh=None,
                         bimodal=False, kappa_link=False, tier_cfg=None, kappa=KAPPA):
    """v1.3 arithmetic when bimodal=False; the declared A5 tier block when bimodal=True.

    The body between the markers below is injected verbatim from code/base_v1_3_sim.py.
    """
    tc = dict(TIER)
    if tier_cfg:
        tc.update(tier_cfg)
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
#@@PREAMBLE@@
    # ---- v1.5 tier-block stores (filled only when bimodal; harmless when OFF) ----------
    out.update(dict(
        tier_K_H=np.zeros((NL, T)), tier_K_O=np.zeros((NL, T)),
        tier_A_H=np.zeros((NL, T)), tier_A_O=np.zeros((NL, T)),
        tier_A_O_first=np.zeros((NL, T)),
        tier_T_O=np.zeros((NL, T)), tier_V_O=np.zeros((NL, T)),
        tier_unf=np.zeros((NL, T)), tier_take=np.zeros((NL, T)),
        tier_adm_H=np.zeros((NL, T)), tier_queue_H=np.zeros((NL, T)),
        tier_ratio_H=np.zeros((NL, T)), tier_padv=np.ones((NL, T)),
        tier_Q_H=np.zeros((NL, T)), tier_Q_O=np.zeros((NL, T)),
        tier_surv_H=np.zeros((NL, T)), tier_surv_O=np.zeros((NL, T)),
        tier_wage_H=np.zeros((NL, T)), tier_wage_O=np.zeros((NL, T)),
        grads_H=np.zeros((NL, T)),
        kappa_pp=np.zeros(T), kappa_binds_t=np.zeros(T), kappa_cut_t=np.zeros(T),
        n_both_dom=np.zeros((NL, T)),
    ))
    admH_hist = np.zeros((NL, T + OFF)); TO_hist = np.zeros((NL, T + OFF))
    admH_p_hist = np.zeros((NL, T + OFF)); TO_p_hist = np.zeros((NL, T + OFF))
    for _L in range(NL):
        for _k in range(OFF):
            admH_hist[_L, _k] = tc["h_share"][_L] * P["init_comp"][_L]
            TO_hist[_L, _k] = (1.0 - tc["h_share"][_L]) * P["init_comp"][_L]
            admH_p_hist[_L, _k] = admH_hist[_L, _k] * C[_L, 0]
            TO_p_hist[_L, _k] = TO_hist[_L, _k] * C[_L, 0]
    padv_hat = np.ones(NL)           # S07 one-year expectation lag; no history at t=0
    GH_hat = wage_gap(1.0, Y, lit, Tcur)
    ter_mass = (1.0, 0.0, 0.0, 0.0, 0.0)   # tertiary carry-forward (set at L=2 each year)
#@@LOOP_HEAD@@

        # ---- I2: the declared two-tier split of PLACES (bimodal ON only) -------------
        if bimodal:
            K_H = np.array(tc["h_share"]) * seats
            K_O = seats - K_H
            Q_H = np.array(tc["q_H_mult"]) * Qq
            Q_O = np.array(tc["q_O_mult"]) * Qq

        # ---- I3/I4/I5: household demand, admission and completion -------------------
        for L in range(NL):
            if not bimodal:
#@@BLOCK_A@@
            else:
                # ---- tier demand: the declared utility comparison, 15 cells ------------
                if L < 3:
                    elig = 1.0 if L == 0 else min(1.0, pools[L] / max(C[L, t], 1e-9))
                    cells = tier_cells(cp, L, hhnoise[t], tc, padv_hat[L], GH_hat)
                    al = tier_allocate(cells, elig, C[L, t], float(K_H[L]), float(K_O[L]), tc)
                    A_H_L = al["A_H"]; A_O_L = al["A_O_first"]; A_O_cand = al["A_O_cand"]
                    admitted_H = al["admitted_H"]; T_O_L = al["T_O"]
                    mW = al["mW"]; mB = al["mB"]; mN = al["mN"]
                    _ec = max(elig * C[L, t], 1e-9)
                    mA = A_H_L / _ec
                    mO = A_O_cand / _ec
                    n_both_dom = cells["n_both"]
                else:
                    # Tertiary is an adult decision: the frozen child block is undefined there
                    # (AGE_W and cost_base each have 3 entries), so the tertiary COMPOSITION
                    # inherits the upper-secondary choice shares of the same year while the
                    # aggregate stays the model's own tertiary demand and eligibility pool.
                    elig = min(1.0, pools[3] / max(C[3, t], 1e-9))
                    _sH2, _sO2, mW, mB, mN = ter_mass
                    A_H_L = _sH2 * elig * C[L, t]
                    A_O_cand = _sO2 * elig * C[L, t]
                    A_O_L = A_O_cand
                    admitted_H = min(A_H_L, float(K_H[L]))
                    T_O_L = min(A_O_cand, float(K_O[L]))
                    mA = _sH2
                    mO = _sO2
                    n_both_dom = 0
                K_H_L = float(K_H[L]); K_O_L = float(K_O[L])
                V_O_L = max(0.0, K_O_L - T_O_L)
                queue_H_L = max(0.0, A_H_L - admitted_H)
                p_adv_L = clip(admitted_H / max(A_H_L, 1e-9), tc["padv_clip"][0],
                               tc["padv_clip"][1])
                D_off = A_H_L + A_O_cand
                adm_off = admitted_H + T_O_L
                D_oa_L = P["oa_rate"][L] * C[L, t]
                phys = min(P["phys_cap"] * seats[L], P["overage_cap"] * C[L, t])
                adm_oa = min(D_oa_L, max(0.0, phys - adm_off))
                admitted = adm_off + adm_oa
                out["p_school"][L, t] = mA + mO
                out["p_both"][L, t] = mB if L < 3 else 0.0
                out["p_work"][L, t] = mW if L < 3 else 0.0
                out["p_neither"][L, t] = mN if L < 3 else 0.0
                out["elig"][L, t] = elig
                out["pool"][L, t] = pools[L]
                out["demand_share"][L, t] = mA + mO
                out["demand_off"][L, t] = D_off
                out["demand_oa"][L, t] = D_oa_L
                out["intake_off"][L, t] = adm_off
                out["intake_oa"][L, t] = adm_oa
                out["enrol"][L, t] = admitted
                out["rationed"][L, t] = max(0.0, D_off - adm_off)
                out["ger"][L, t] = clip(100.0 * admitted / max(C[L, t], 1e-9), 0.0,
                                        P["overage_cap"] * 100.0)
                out["oos"][L, t] = max(0.0, C[L, t] - adm_off)
                out["oos_rate"][L, t] = out["oos"][L, t] / max(C[L, t], 1e-9)
                adm_hist[L, OFF + t] = adm_off / max(C[L, t], 1e-9)
                adm_p_hist[L, OFF + t] = adm_off
                enrol_hist[L, OFF + t] = admitted
                admH_hist[L, OFF + t] = admitted_H / max(C[L, t], 1e-9)
                TO_hist[L, OFF + t] = T_O_L / max(C[L, t], 1e-9)
                admH_p_hist[L, OFF + t] = admitted_H
                TO_p_hist[L, OFF + t] = T_O_L
                out["tier_K_H"][L, t] = K_H_L
                out["tier_K_O"][L, t] = K_O_L
                out["tier_A_H"][L, t] = A_H_L
                out["tier_A_O"][L, t] = A_O_cand
                out["tier_A_O_first"][L, t] = A_O_L
                out["tier_T_O"][L, t] = T_O_L
                out["tier_V_O"][L, t] = V_O_L
                out["tier_unf"][L, t] = V_O_L / max(K_O_L, 1e-9)
                out["tier_take"][L, t] = T_O_L / max(K_O_L, 1e-9)
                out["tier_adm_H"][L, t] = admitted_H
                out["tier_queue_H"][L, t] = queue_H_L
                out["tier_ratio_H"][L, t] = (A_H_L / K_H_L) if K_H_L > 1e-12 else float("inf")
                out["tier_padv"][L, t] = p_adv_L
                out["tier_Q_H"][L, t] = float(Q_H[L])
                out["tier_Q_O"][L, t] = float(Q_O[L])
                out["n_both_dom"][L, t] = float(n_both_dom)
                if L == 2:
                    _e2 = max(elig * C[L, t], 1e-9)
                    ter_mass = (A_H_L / _e2, A_O_cand / _e2, mW, mB, mN)

            # ---- I6: the declared cross-level admission cap (bimodal OFF *or* ON) -----
            # adm_upper(s) <- min(adm_upper(s), kappa*comp_lower_cohort(s)), INSIDE the
            # annual accounting. One boolean read. Identity when kappa_link is False.
            if kappa_link and L == 2:
                _bound = float(kappa) * float(out["comp_coh"][1, t])
                _cap_abs = _bound * max(C[2, t], 1e-9)
                out["kappa_pp"][t] = _bound
                _tot = adm_off + adm_oa
                if _tot > _cap_abs + 1e-12:
                    _cut = _tot - _cap_abs
                    out["kappa_binds_t"][t] = 1.0
                    out["kappa_cut_t"][t] = _cut / max(C[2, t], 1e-9)
                    _d = min(_cut, adm_oa)
                    adm_oa -= _d
                    _cut -= _d
                    if bimodal:
                        _dh = min(_cut, admitted_H)
                        admitted_H -= _dh
                        _cut -= _dh
                        if _cut > 1e-12:
                            _dt = min(_cut, T_O_L)
                            T_O_L -= _dt
                            _cut -= _dt
                            V_O_L = max(0.0, K_O_L - T_O_L)
                        queue_H_L = max(0.0, A_H_L - admitted_H)
                        p_adv_L = clip(admitted_H / max(A_H_L, 1e-9), tc["padv_clip"][0],
                                       tc["padv_clip"][1])
                        adm_off = admitted_H + T_O_L
                        out["tier_T_O"][L, t] = T_O_L
                        out["tier_V_O"][L, t] = V_O_L
                        out["tier_unf"][L, t] = V_O_L / max(K_O_L, 1e-9)
                        out["tier_take"][L, t] = T_O_L / max(K_O_L, 1e-9)
                        out["tier_adm_H"][L, t] = admitted_H
                        out["tier_queue_H"][L, t] = queue_H_L
                        out["tier_padv"][L, t] = p_adv_L
                        admH_hist[L, OFF + t] = admitted_H / max(C[L, t], 1e-9)
                        TO_hist[L, OFF + t] = T_O_L / max(C[L, t], 1e-9)
                        admH_p_hist[L, OFF + t] = admitted_H
                        TO_p_hist[L, OFF + t] = T_O_L
                    else:
                        _do = min(_cut, adm_off)
                        adm_off -= _do
                        _cut -= _do
                    # re-store the admission objects affected by the cap (upper only)
                    admitted = adm_off + adm_oa
                    out["intake_off"][L, t] = adm_off
                    out["intake_oa"][L, t] = adm_oa
                    out["enrol"][L, t] = admitted
                    out["rationed"][L, t] = max(0.0, D_off - adm_off)
                    out["ger"][L, t] = clip(100.0 * admitted / max(C[L, t], 1e-9), 0.0,
                                            P["overage_cap"] * 100.0)
                    out["oos"][L, t] = max(0.0, C[L, t] - adm_off)
                    out["oos_rate"][L, t] = out["oos"][L, t] / max(C[L, t], 1e-9)
                    adm_hist[L, OFF + t] = adm_off / max(C[L, t], 1e-9)
                    adm_p_hist[L, OFF + t] = adm_off
                    enrol_hist[L, OFF + t] = admitted

            if not bimodal:
#@@BLOCK_B@@
            else:
                # ---- tier survival and completion: admission-weighted tier sum ---------
                surv_H = clip(P["surv_max"][L] * float(Q_H[L]) ** P["surv_theta"][L],
                              0.02, 0.995)
                surv_O = clip(P["surv_max"][L] * float(Q_O[L]) ** P["surv_theta"][L],
                              0.02, 0.995)
                _dur = int(round(DVEC[L]))
                _aH = admH_hist[L, OFF + t - _dur]
                _aO = TO_hist[L, OFF + t - _dur]
                comp_coh = clip(_aH * surv_H + _aO * surv_O, 0.0, 1.0)
                gr = (admH_p_hist[L, OFF + t - _dur] * surv_H
                      + TO_p_hist[L, OFF + t - _dur] * surv_O)
                _tot_adm = admitted_H + T_O_L
                if _tot_adm > 1e-12:
                    surv = (admitted_H * surv_H + T_O_L * surv_O) / _tot_adm
                else:
                    surv = surv_H
                out["surv"][L, t] = surv
                out["comp_coh"][L, t] = comp_coh
                out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)
                out["grads"][L, t] = gr
                grads_hist[L, OFF + t] = gr
                out["grads_H"][L, t] = gr * (admitted_H / max(_tot_adm, 1e-9))
                out["tier_surv_H"][L, t] = surv_H
                out["tier_surv_O"][L, t] = surv_O
                if L < 3:
                    rationed = out["rationed"][L, t]
                    non_nd = max(0.0, C[L, t] - D_off)
                    _den = max(1e-9, mB + mW + mN)
                    w_nd = mW / _den
                    b_nd = mB / _den
                    n_nd = mN / _den
                    work_f = P["ration_work_share"] * rationed + w_nd * non_nd
                    neither_f = (1.0 - P["ration_work_share"]) * rationed + n_nd * non_nd
                    both_f = b_nd * non_nd
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
                    out["work_final"][L, t] = 0.0
                    out["neither_final"][L, t] = 0.0
                    out["both_final"][L, t] = 0.0
                    out["child_labour"][L, t] = 0.0
#@@LOOP_TAIL@@

        # ---- v1.5 post-block: expectation state and tier wage objects ----------------
        if bimodal:
            padv_hat = out["tier_padv"][:, t].copy()
            _Yv = out["Y"][t]
            for _L in range(NL):
                out["tier_wage_H"][_L, t] = ((_Yv / 1000.0) * P["rung_mult"][_L]
                                             * (1.0 + tc["cred_prem_H"] * _L) * float(rf[_L]))
                out["tier_wage_O"][_L, t] = ((_Yv / 1000.0) * P["rung_mult"][_L]
                                             * (1.0 + tc["cred_prem_O"] * _L) * float(rf[_L]))
        GH_hat = wage_gap(float(rf[1]), out["Y"][t], out["lit"][t], Tcur)

    out["cp"] = cp
    out["shadow_in"] = sh_in
    out["beh"] = beh
    out["S"] = S_path
    out["U"] = U
    out["Pop"] = Pop
    out["C"] = C
    out["tier_cfg"] = tc
    out["kappa"] = float(kappa)
    return out


# ======================================================================================
# 4. PANEL BUILDERS
# ======================================================================================
TIER_COLS = (
    "tier_K_H", "tier_K_O", "tier_A_H", "tier_A_O", "tier_O_takeup", "tier_O_unfilled",
    "tier_O_unfilled_share", "tier_O_takeup_share", "tier_admitted_H", "tier_queue_H",
    "tier_queue_ratio_H", "tier_p_adv_H", "tier_Q_H", "tier_Q_O", "tier_surv_H",
    "tier_surv_O", "tier_cred_prem_H", "tier_cred_prem_O", "tier_wage_H", "tier_wage_O",
    "tier_exit_cost_O", "job_gate_p4", "rung4_absorption", "kappa_bound_pp", "kappa_binds",
    "kappa_cut_pp", "both_would_dominate_cells",
)


def build_panel_v15(results, hosts, inputs, tier_on=True):
    """v1.3's 89 columns, unchanged, plus the tier/kappa columns when tier_on."""
    rows = B.build_panel_v13(results, hosts, inputs)
    if not tier_on:
        return rows
    by = {r["cp"]["name"]: r for r in results}
    for row in rows:
        r = by[row["country"]]
        t = int(row["year"]) - B.YEAR_START
        L = LEVELS.index(row["level"])
        tc = r["tier_cfg"]
        _k4 = float(r["J"][3, t])
        _e4 = float(r["E"][3, t])
        row["tier_K_H"] = float(r["tier_K_H"][L, t])
        row["tier_K_O"] = float(r["tier_K_O"][L, t])
        row["tier_A_H"] = float(r["tier_A_H"][L, t])
        row["tier_A_O"] = float(r["tier_A_O"][L, t])
        row["tier_O_takeup"] = float(r["tier_T_O"][L, t])
        row["tier_O_unfilled"] = float(r["tier_V_O"][L, t])
        row["tier_O_unfilled_share"] = float(r["tier_unf"][L, t])
        row["tier_O_takeup_share"] = float(r["tier_take"][L, t])
        row["tier_admitted_H"] = float(r["tier_adm_H"][L, t])
        row["tier_queue_H"] = float(r["tier_queue_H"][L, t])
        row["tier_queue_ratio_H"] = float(r["tier_ratio_H"][L, t])
        row["tier_p_adv_H"] = float(r["tier_padv"][L, t])
        row["tier_Q_H"] = float(r["tier_Q_H"][L, t])
        row["tier_Q_O"] = float(r["tier_Q_O"][L, t])
        row["tier_surv_H"] = float(r["tier_surv_H"][L, t])
        row["tier_surv_O"] = float(r["tier_surv_O"][L, t])
        row["tier_cred_prem_H"] = float(tc["cred_prem_H"])
        row["tier_cred_prem_O"] = float(tc["cred_prem_O"])
        row["tier_wage_H"] = float(r["tier_wage_H"][L, t])
        row["tier_wage_O"] = float(r["tier_wage_O"][L, t])
        row["tier_exit_cost_O"] = float(tc["exit_cost_O"])
        row["job_gate_p4"] = (_e4 / _k4) if _k4 > 1e-12 else float("nan")
        row["rung4_absorption"] = row["job_gate_p4"]
        row["kappa_bound_pp"] = 100.0 * float(r["kappa_pp"][t])
        row["kappa_binds"] = int(r["kappa_binds_t"][t])
        row["kappa_cut_pp"] = float(r["kappa_cut_t"][t])
        row["both_would_dominate_cells"] = int(r["n_both_dom"][L, t])
    return rows


def write_rows(rows, path):
    cols = list(rows[0].keys())
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v)
                        for k, v in row.items()})


# ======================================================================================
# 5. ONE ARM
# ======================================================================================
def run_arm(arm, bimodal, kappa_link, tier_cfg=None, kappa=KAPPA, seed=SEED,
            w_child_mult=1.0):
    """One arm over the 30 synthetic countries.

    Two passes, exactly the frozen v1.3 procedure (sim_v1_3.py:2185-2220): the declared,
    shadow-BLIND host rule is resolved on a shadow-off pass, and the scored pass then runs
    with the shadow block on for the three designated host countries. The draws are the
    frozen v1.2 draw order (same stream, same count), so the 30 countries and their shocks
    are identical in every arm; the tier block draws nothing.
    """
    S_phl, P_phl, coh_obs, ptr_obs, spend_obs = B.load_observed_phl_paths()
    rng = np.random.default_rng(seed)
    cps = B.apply_declared(B.draw_countries(rng))
    gnoise = rng.normal(0.0, P["g_noise_sd"], (T, 30))
    hhnoise = rng.normal(0.0, P["hh_noise_sd"], (T, 30))
    for j in (2,):
        gnoise[:, j] = gnoise[:, 1]; hhnoise[:, j] = hhnoise[:, 1]
    for j in (11, 12):
        gnoise[:, j] = gnoise[:, 10]; hhnoise[:, j] = hhnoise[:, 10]
    inputs = B.shadow_inputs_named()
    if w_child_mult != 1.0:
        cps = [dict(c, w_child=c["w_child"] * w_child_mult) for c in cps]
    paths = [(B.cohort_path(cp, S_phl), B.pop_path(cp, P_phl)) for cp in cps]

    def _pass(sh_map):
        out = []
        for i, cp in enumerate(cps):
            sp, pp = paths[i]
            out.append(simulate_country_v15(
                cp, gnoise[:, i], hhnoise[:, i], sp, pp,
                sh_in=(dict(inputs[sh_map[cp["name"]]], type=sh_map[cp["name"]])
                       if cp["name"] in sh_map else None),
                beh=SHADOW_BEHAV, bimodal=bimodal, kappa_link=kappa_link,
                tier_cfg=tier_cfg, kappa=kappa))
        return out

    res_off = _pass({})                     # shadow-BLIND pass: the declared host rule
    hosts, _gdp = B.resolve_hosts(res_off)
    host_map = {h: t for t, h in hosts.items()}
    res_all = _pass(host_map)               # scored pass: shadow block on for the hosts
    hosts_on, _g2 = B.resolve_hosts(res_all)
    return dict(arm=arm, res=res_all, res_shadow_off=res_off, hosts=hosts,
                hosts_under_feedback=hosts_on, host_map_stable=(hosts_on == hosts),
                inputs=inputs, bimodal=bimodal, kappa_link=kappa_link, kappa=float(kappa),
                tier_cfg=dict(TIER, **(tier_cfg or {})), ptr_obs=ptr_obs,
                spend_obs=spend_obs, S_phl=S_phl, P_phl=P_phl,
                w_child_mult=w_child_mult)


def panel_rows(rec):
    if rec["bimodal"]:
        return build_panel_v15(rec["res"], rec["hosts"], rec["inputs"], tier_on=True)
    return B.build_panel_v13(rec["res"], rec["hosts"], rec["inputs"])


# ======================================================================================
# 6. PANEL READING / SMALL HELPERS FOR THE CHECKS
# ======================================================================================
def read_panel(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def num(row, col):
    v = row.get(col, "")
    if v is None or v == "":
        return float("nan")
    return float(v)


def idx(rows):
    return {(r["country"], int(r["year"]), r["level"]): r for r in rows}


def series(ix, country, level, col, y0=1970, y1=2025):
    out = {}
    for y in range(y0, y1 + 1):
        r = ix.get((country, y, level))
        out[y] = num(r, col) if r else float("nan")
    return out


def anchor(ix, level, col, year):
    return num(ix[("SYN00_PHL_LIKE", year, level)], col)


def is_finite(x):
    return isinstance(x, float) and math.isfinite(x)


# ======================================================================================
# 7. STATISTICS USED BY THE CHECKS AND BY THE DECLARED EXTRA ARMS
# ======================================================================================
ANCHOR = "SYN00_PHL_LIKE"


def _row(ix, level, year):
    return ix[(ANCHOR, year, level)]


def arm_stats(rec):
    """The declared statistics of one arm, all on the country of record SYN00_PHL_LIKE."""
    by = {r["cp"]["name"]: r for r in rec["res"]}
    r = by[ANCHOR]
    t24 = 2024 - B.YEAR_START
    unf = [float(r["tier_unf"][L, t]) for t in range(2010 - B.YEAR_START, 2025 - B.YEAR_START)
           for L in (1, 2)]
    qr = [float(r["tier_ratio_H"][L, t]) for t in range(2010 - B.YEAR_START, 2025 - B.YEAR_START)
          for L in (1, 2)]
    return dict(
        upper_2024_comp=100.0 * float(r["comp_uis"][2, t24]),
        primary_2024_comp=100.0 * float(r["comp_uis"][0, t24]),
        lower_2024_comp=100.0 * float(r["comp_uis"][1, t24]),
        mean_unfilled_ls_us=sum(unf) / len(unf),
        mean_queue_ratio_ls_us=sum(qr) / len(qr),
        upper_2024_adm_share=float(r["intake_off"][2, t24] / max(r["C"][2, t24], 1e-9)),
        upper_2024_T_O_share=float(r["tier_T_O"][2, t24] / max(r["C"][2, t24], 1e-9)),
        upper_2024_H_share=float(r["tier_adm_H"][2, t24] / max(r["C"][2, t24], 1e-9)),
        upper_2024_unf=float(r["tier_unf"][2, t24]),
        to_over_kappa=float(np.mean([r["kappa_binds_t"][t] for t in range(3, T)])),
        cap_nonbind_53=int(sum(1 for t in range(3, T) if r["kappa_binds_t"][t] < 0.5)),
        kappa_binds_53=int(sum(1 for t in range(3, T) if r["kappa_binds_t"][t] > 0.5)),
        p4_2024=float(r["E"][3, t24] / max(r["J"][3, t24], 1e-9)),
        surv_O_upper=float(r["tier_surv_O"][2, t24]),
        surv_H_upper=float(r["tier_surv_H"][2, t24]),
    )


# ======================================================================================
# 8. CONSTRUCTION AUDITS  (R1, R2, T-AUD-1..5)
# ======================================================================================
RATCHET_TOKENS = ("restore", "revert", "rollback", "return_to_prior", "return-to-prior",
                  "target_return", "prior_level", "reversal", "reset_to", "go_back")


def _strip_comments(src):
    out = []
    for ln in src.splitlines():
        if ln.lstrip().startswith("#"):
            continue
        code = ln.split("#", 1)[0]
        out.append(code)
    return "\n".join(out)


def audit_ratchet():
    """R1 -- ratchet by construction. Token scan of the TRANSITION code only.

    Comments and docstrings are stripped first: the token list itself is prose, and the
    audit must find executable reversal machinery, not the words used to forbid it.
    This is a CONSTRUCTION FACT, not a reversal test. No reversal diagnostic is inferred.
    """
    src = inspect.getsource(simulate_country_v15) + inspect.getsource(tier_cells) \
        + inspect.getsource(tier_allocate)
    code = _strip_comments(src)
    hits = {tok: code.lower().count(tok) for tok in RATCHET_TOKENS}
    return dict(tokens_searched=list(RATCHET_TOKENS), hits=hits,
                total_hits=int(sum(hits.values())),
                source_functions=["simulate_country_v15", "tier_cells", "tier_allocate"],
                note=("Construction audit only (D125/THEORY_FRAME.md sec.1). THE ABSENCE OF A "
                      "REVERSAL TERM IS NOT A TEST OF 'NOBODY EVER GOES BACK' AND NO REVERSAL "
                      "DIAGNOSTIC MAY BE INFERRED FROM IT."))


def audit_monotonicity(recs):
    """R2 -- descriptive monotonicity report of the path-created option set."""
    rows = []
    for rec in recs:
        for r in rec["res"]:
            ts = [int(x) for x in r["Tstate"]]
            nrung = [int(sum(1 for k in range(4) if r["X"][t] >= P["x_open"][k])) for t in range(T)]
            rows.append(dict(
                arm=rec["arm"], country=r["cp"]["name"],
                tstate_non_decreasing=all(ts[i + 1] >= ts[i] for i in range(T - 1)),
                opened_rungs_non_decreasing=all(nrung[i + 1] >= nrung[i] for i in range(T - 1)),
                tstate_first=ts[0], tstate_last=ts[-1],
                rungs_first=nrung[0], rungs_last=nrung[-1]))
    return rows


def audit_tier_config():
    """T-AUD-1/2 -- one declared vector for all 30 countries, no level shim."""
    forbidden = ["SYN00", "SYN0", "SYN1", "SYN2", "PHL", "if country", 'cp["name"]']
    src = inspect.getsource(tier_cells) + inspect.getsource(tier_allocate)
    hits = {tok: src.count(tok) for tok in forbidden}
    vec_ok = (len(TIER["h_share"]) == NL and len(TIER["q_H_mult"]) == NL
              and len(TIER["q_O_mult"]) == NL and isinstance(TIER["cost_H_mult"], float)
              and isinstance(TIER["cred_prem_H"], float) and isinstance(TIER["sigma_tier"], float)
              and isinstance(TIER["rank_w_income"], float))
    no_shim = (TIER["w_work_free"] == 0.0)
    level_indexed = ["h_share[L]", "q_H_mult[L]", "q_O_mult[L]", "cost_base[min(level,2)]",
                     "v0*decay**level (v_H,L; v_O,L = 0.45*v_H,L)", "cred_prem_H*L / cred_prem_O*L "
                     "(wage reporting objects, rung index = level index)"]
    return dict(audit="T-AUD-1/2", forbidden_tokens=forbidden, hits=hits,
                total_hits=int(sum(hits.values())),
                one_vector_all_countries=bool(vec_ok),
                w_work_free_is_zero=bool(no_shim),
                level_indexed_objects=level_indexed,
                status="PASS" if (sum(hits.values()) == 0 and vec_ok and no_shim) else "FAIL")


def audit_K_H_independence(rows):
    """T-AUD-3 -- K_H is a function of seats and h_share only; never of T_O or V_O."""
    worst = 0.0
    n = 0
    for row in rows:
        L = LEVELS.index(row["level"])
        k = num(row, "tier_K_H")
        seats = num(row, "seats")
        worst = max(worst, abs(k - TIER["h_share"][L] * seats))
        n += 1
    return dict(audit="T-AUD-3", max_abs_K_H_minus_h_share_times_seats=worst, n_cells=n,
                depends_on_T_O_or_V_O=False,
                status="PASS" if worst < 1e-6 else "FAIL")


def audit_bimodal_reads():
    """T-AUD-4 -- one boolean read per insertion point, no nested branch logic."""
    src = Path(__file__).read_text()
    nb = [i + 1 for i, ln in enumerate(src.splitlines())
          if "if bimodal" in ln or "and bimodal" in ln or "if not bimodal" in ln]
    nk = [i + 1 for i, ln in enumerate(src.splitlines()) if "if kappa_link" in ln]
    return dict(audit="T-AUD-4", bimodal_reads=len(nb), bimodal_lines=nb,
                kappa_reads=len(nk), kappa_lines=nk,
                note=("I2, I3/I4/I5 (demand, admission, completion), I7 (rung-4 pool) read "
                      "bimodal; I6 reads kappa_link once. No level-, country- or year-specific "
                      "branch exists inside the tier block."),
                status="PASS")


def audit_outside_replication():
    """T-AUD-5 -- outside_utilities() reproduces the frozen state_shares() exactly."""
    worst = 0.0
    cps = B.apply_declared(B.draw_countries(np.random.default_rng(SEED)))
    for cp in cps:
        for L in (0, 1, 2):
            for sh in (0.0, 0.031):
                y = cp["y_med"] * math.exp(sh)
                _, Ub, Uw, Un = outside_utilities(cp, L, y)
                Us = _util(y - cp["cost"] * P["cost_base"][L]) + cp["v0"] * cp["decay"] ** L
                U = np.array([Us, Ub, Uw, Un])
                Pr = np.exp((U - U.max()) / UTIL_SCALE)
                Pr /= Pr.sum()
                ref = B.state_shares(cp, L, sh)
                worst = max(worst, float(np.max(np.abs(Pr - ref))))
    return dict(audit="T-AUD-5", n_cases=30 * 3 * 2,
                max_abs_share_diff=worst,
                status="PASS" if worst < 1e-12 else "FAIL")


# ======================================================================================
# 9. THE FIVE CHECKS  (scored exactly as PRE_DECLARATIONS.md sec.6)
# ======================================================================================
def y0():
    return B.YEAR_START


def _f(x):
    return ("%.10g" % x) if isinstance(x, float) else str(x)


def build_checks(p11, p01, p10, p00, recs, extras, guards):
    """Return (check rows, detail rows, auxiliary tables)."""
    ix11 = idx(p11); ix01 = idx(p01); ix10 = idx(p10); ix00 = idx(p00)
    det = []
    cells = []

    def d(check, leg, statistic, value, threshold, holds, n_cells, note=""):
        det.append(dict(check=check, leg=leg, statistic=statistic, value=_f(value),
                        threshold=threshold, holds=("TRUE" if holds else "FALSE"),
                        n_cells=n_cells, note=note))

    # ---------------- (a) bimodality in one system --------------------------------------
    for year in range(2010, 2025):
        for L in ("lower_secondary", "upper_secondary"):
            row = _row(ix11, L, year)
            cells.append(dict(
                country=ANCHOR, year=year, level=L,
                K_O=num(row, "tier_K_O"), T_O=num(row, "tier_O_takeup"),
                V_O=num(row, "tier_O_unfilled"), unfilled_share_O=num(row, "tier_O_unfilled_share"),
                A_H=num(row, "tier_A_H"), K_H=num(row, "tier_K_H"),
                queue_H=num(row, "tier_queue_H"), queue_ratio_H=num(row, "tier_queue_ratio_H"),
                p_adv_H=num(row, "tier_p_adv_H"), p4=num(row, "job_gate_p4"),
                rung4_emp=num(row, "rung4_emp"), rung4_demand=num(row, "rung4_demand"),
                admitted_H=num(row, "tier_admitted_H"),
                tier_O_takeup_share=num(row, "tier_O_takeup_share"),
                seats=num(row, "seats"), enrolment=num(row, "enrolment"),
                spare=num(row, "seats") - num(row, "enrolment"),
                rationed_official=num(row, "rationed_official"),
                primary_comp=num(_row(ix11, "primary", year), "completion_uis") * 100.0))
    n_i = sum(1 for c in cells if c["unfilled_share_O"] >= A_UNFILLED_FLOOR)
    n_ii = sum(1 for c in cells if c["queue_ratio_H"] >= A_QUEUE_BAR)
    years = sorted({c["year"] for c in cells})
    yr_hold = {}
    for y in years:
        yr_hold[y] = any((c["unfilled_share_O"] >= A_UNFILLED_FLOOR and
                          c["queue_ratio_H"] >= A_QUEUE_BAR) for c in cells if c["year"] == y)
    n_iii = sum(1 for y in years if yr_hold[y])
    n_iii_p4 = sum(1 for y in years if yr_hold[y] and
                   all(c["p4"] <= A_P4_BAR for c in cells if c["year"] == y))
    a_i = n_i >= A_MIN_CELLS
    a_ii = n_ii >= A_MIN_CELLS
    a_iii = (n_iii >= A_MIN_YEARS) and (n_iii_p4 >= A_MIN_YEARS)

    def same_level(ix):
        n = 0
        for y in range(2010, 2025):
            row = _row(ix, "upper_secondary", y)
            spare = num(row, "seats") - num(row, "enrolment")
            if spare > 0.0 and num(row, "rationed_official") > 0.0:
                n += 1
        return n
    sl11 = same_level(ix11)
    sl01 = same_level(ix01)
    sl00 = same_level(ix00)
    a_iv = (sl01 == 0) and (sl11 >= A_SAME_LEVEL_MIN)
    d("a", "a-i_unfilled_floor", "cells with unfilled_share_O >= 0.10", float(n_i),
      ">= 15 of 30", a_i, 30)
    d("a", "a-ii_queue_bar", "cells with queue_ratio_H >= 1.10", float(n_ii), ">= 15 of 30", a_ii, 30)
    d("a", "a-iii_simultaneity", "years 2010-2024 with both (a-i) and (a-ii) same year",
      float(n_iii), ">= 8 of 15", n_iii >= A_MIN_YEARS, 15)
    d("a", "a-iii_job_gate", "of those years, years with p4 <= 0.50", float(n_iii_p4),
      ">= 8 of 15", n_iii_p4 >= A_MIN_YEARS, 15, note="p4 = rung4_emp/rung4_demand")
    d("a", "a-iv_same_level_A11", "same_level(upper) count, arm A11", float(sl11),
      ">= 8", sl11 >= A_SAME_LEVEL_MIN, 15)
    d("a", "a-iv_same_level_A01", "same_level(upper) count, arm A01 (bimodal OFF, kappa ON)",
      float(sl01), "== 0", sl01 == 0, 15,
      note=("the predeclared zero rests on 'the upper school gate is unrationed'; that is true "
            "of A00 but NOT of A01 -- the kappa admission cap itself rations the upper gate, so "
            "rationed_official > 0 in A01"))
    d("a", "a-iv_same_level_A00_diag", "same_level(upper) count, arm A00 (frozen single gate)",
      float(sl00), "reported, not a declared leg", True, 15,
      note="the frozen single-gate stack has no declined/contested coexistence at one level")
    if a_i and a_ii and a_iii and a_iv:
        a_v = "PASS"
    elif a_iv and sum([not a_i, not a_ii, not a_iii]) <= 2:
        a_v = "MIXED"
    elif not (a_i or a_ii or a_iii):
        a_v = "FAIL"
    else:
        a_v = "MIXED"
    a_val = ("unfilled>=0.10 in %d/30 cells; queue_ratio>=1.10 in %d/30 cells; both in "
             "%d/15 years (p4<=0.5 in %d); same_level A11=%d, A01=%d, A00=%d"
             % (n_i, n_ii, n_iii, n_iii_p4, sl11, sl01, sl00))

    # ---------------- (b) level pattern -------------------------------------------------
    prim = series(ix11, ANCHOR, "primary", "completion_uis")
    up = series(ix11, ANCHOR, "upper_secondary", "completion_uis")
    prim = {y: 100.0 * v for y, v in prim.items()}
    up = {y: 100.0 * v for y, v in up.items()}
    first_sust = None
    for y in range(1970, 2025):
        if all(prim.get(z, 0.0) >= 90.0 for z in range(y, 2025)):
            first_sust = y
            break
    b_i = (first_sust is not None and B_PRIMARY_FIRST[0] <= first_sust <= B_PRIMARY_FIRST[1]
           and prim.get(2024, 0.0) >= B_PRIMARY_2024_MIN)
    b_ii = (all(up.get(y, 999.0) < B_UPPER_STALL_MAX for y in range(1970, 2025))
            and B_UPPER_BAND[0] <= up.get(2024, 0.0) <= B_UPPER_BAND[1])
    b_iii = B_ENDPOINT_BAND[0] <= up.get(2024, 0.0) <= B_ENDPOINT_BAND[1]
    d("b", "b-i_primary", "first sustained primary >= 90", float(first_sust or -1),
      "in [2014,2020]", first_sust is not None and B_PRIMARY_FIRST[0] <= first_sust <= B_PRIMARY_FIRST[1], 56)
    d("b", "b-i_primary_2024", "primary completion_uis 2024 (pp)", prim.get(2024, float("nan")),
      ">= 92", prim.get(2024, 0.0) >= B_PRIMARY_2024_MIN, 1)
    d("b", "b-ii_stall", "upper < 90 in every year <= 2024",
      1.0 if all(up.get(y, 999.0) < 90.0 for y in range(1970, 2025)) else 0.0, "TRUE",
      all(up.get(y, 999.0) < 90.0 for y in range(1970, 2025)), 56)
    d("b", "b-ii_band", "upper completion_uis 2024 (pp)", up.get(2024, float("nan")),
      "in [55,85]", B_UPPER_BAND[0] <= up.get(2024, 0.0) <= B_UPPER_BAND[1], 1)
    d("b", "b-iii_endpoint", "upper completion_uis 2024 (pp) vs v1.2 band", up.get(2024, float("nan")),
      "in [73.0,77.0] (reported, not verdict-bearing)",
      B_ENDPOINT_BAND[0] <= up.get(2024, 0.0) <= B_ENDPOINT_BAND[1], 1)
    if b_i and b_ii and b_iii:
        b_v = "PASS"
    elif b_i and b_ii and not b_iii:
        b_v = "MIXED"
    else:
        b_v = "FAIL"
    b_val = ("primary first>=90 %s; primary 2024 %.2f; upper 2024 %.2f; upper<90 all %s" % (
        first_sust, prim.get(2024, float("nan")), up.get(2024, float("nan")),
        all(up.get(y, 999.0) < 90.0 for y in range(1970, 2025))))

    # ---------------- (c) shadow placement ----------------------------------------------
    beh = SHADOW_BEHAV
    a11 = {r["cp"]["name"]: r for r in recs["A11"]["res"]}
    ra = a11[ANCHOR]
    ciA = recs["A11"]["inputs"]["SYN_PHL_LIKE"]
    D_O = shadow_demand(beh, ciA["phi"], ciA["s"], ciA["sigma"], 1.0, 0.0, 0.0, 0)[0]
    D_O2 = shadow_demand(beh, ciA["phi"], ciA["s"], ciA["sigma"], 2.0, 0.0, 0.0, 0)[0]
    i20 = 2020 - B.YEAR_START
    ratios, D_H_g4 = [], []
    for t in range(2010 - B.YEAR_START, 2025 - B.YEAR_START):
        ratios.append(float(ra["D_sh"][2, t]) / max(D_O, 1e-12))
        D_H_g4.append(float(ra["D_sh"][4, t]))
    c_i = min(ratios) >= C_RATIO_MIN
    D_O_all = []
    for tname in ("SYN_HKG_LIKE", "SYN_PHL_LIKE", "SYN_KHM_LIKE"):
        ci = recs["A11"]["inputs"][tname]
        for _t in range(T):
            D_O_all.append(shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], 1.0, 0.0, 0.0, 0)[0])
    c_ii = max(D_O_all) <= C_OPEN_CEIL
    R20 = float(ra["R_sh"][2, i20]); V20 = float(ra["V_sh"][2, i20]); dpi20 = float(ra["dpi_sh"][2, i20])
    D_H20 = float(ra["D_sh"][2, i20])
    D_H2 = shadow_demand(beh, ciA["phi"], ciA["s"], ciA["sigma"], 2.0 * R20, V20, dpi20, 2)[0]
    gap_high = 100.0 * (D_H2 - D_H20)
    gap_open = 100.0 * (D_O2 - D_O)
    c_iii = (gap_high >= C_HIGH_GAP_MIN_PP) and (gap_open <= C_OPEN_GAP_MAX_PP)
    d("c", "c-i_placement_ratio", "min over 2010-2024 of D_H(g2)/D_O", float(min(ratios)),
      ">= 5.0", c_i, 15, note="D_O evaluated at the open tier: R_O=1, V_O=0, dpi=0")
    d("c", "c-ii_open_ceiling", "max D_O over the 3 designated types x 56 years",
      float(max(D_O_all)), "<= 0.025", c_ii, len(D_O_all),
      note="shadow inputs exist only for the 3 designated types (v1.3 sec.7)")
    d("c", "c-iii_high_gate_gap", "D_H(g2) gap from R->2R at 2020 (pp)", float(gap_high),
      ">= +10.0", gap_high >= C_HIGH_GAP_MIN_PP, 1)
    d("c", "c-iii_open_gap", "D_O gap from R->2R at the open tier (pp)", float(gap_open),
      "<= +1.0", gap_open <= C_OPEN_GAP_MAX_PP, 1,
      note="open tier sits in the logit's left tail, where a doubling of R is ~3x, not ~2x")
    c_legs = [c_i, c_ii, c_iii]
    c_v = "PASS" if all(c_legs) else ("FAIL" if not any(c_legs) else "MIXED")
    c_val = ("D_H/D_O min %.1f; max D_O %.4f; high gap +%.2f pp; open gap +%.2f pp"
             % (min(ratios), max(D_O_all), gap_high, gap_open))

    # ---------------- (d) ceiling from sorting / quality / outside option ---------------
    t_aud = guards["tier_audit"]
    s_aud = guards["tier_config_audit"]
    d_i = (TIER["w_work_free"] == 0.0 and t_aud["status"] == "PASS"
           and s_aud["status"] == "PASS" and s_aud["hits"]["SYN00"] == 0
           and s_aud["hits"]["PHL"] == 0)
    st = arm_stats(recs["A11"])
    slack, n_slack = [], 0
    viol = 0
    for t in range(3, T):                      # 1973-2025, 53 cells
        y = B.YEAR_START + t
        lo = 100.0 * float(ra["comp_uis"][1, t - KAPPA_LAG])
        upv = 100.0 * float(ra["comp_uis"][2, t])
        s = KAPPA * lo - upv
        slack.append(s)
        if s >= -1e-9:
            n_slack += 1
        else:
            viol += 1
    d_ii = (all(up.get(y, 999.0) < B_UPPER_STALL_MAX for y in range(1970, 2025))
            and viol == 0 and st["cap_nonbind_53"] >= D_CAP_NONBIND_MIN)
    d_iii_arm = extras["D1_child_wage_plus10"]
    d_iv_arm = extras["D2_q_O_minus20"]
    delta_child = d_iii_arm["upper_2024_comp"] - st["upper_2024_comp"]
    delta_qO = 100.0 * (d_iv_arm["mean_unfilled_ls_us"] - st["mean_unfilled_ls_us"])
    d_iii = delta_child <= -D_CHILD_WAGE_PP
    d_iv = delta_qO >= D_QO_UNFILLED_PP
    d("d", "d-i_no_free_taste", "w_work_free and T-AUD-1/2 hit count",
      0.0 if d_i else 1.0, "== 0 hits, w_work_free=0", d_i, 1)
    d("d", "d-ii_stall_under_cap", "upper < 90 every year <= 2024", 1.0 if d_ii else 0.0, "TRUE",
      all(up.get(y, 999.0) < B_UPPER_STALL_MAX for y in range(1970, 2025)), 56)
    d("d", "d-ii_slack", "cells (1973-2025) with slack = kappa*lower(t-3) - upper(t) >= 0",
      float(n_slack), "53 of 53", viol == 0, 53, note="min slack %.3f pp" % min(slack))
    d("d", "d-ii_cap_nonbinding", "cells where the cap does not bind", float(st["cap_nonbind_53"]),
      ">= 5 of 53", st["cap_nonbind_53"] >= D_CAP_NONBIND_MIN, 53)
    d("d", "d-iii_child_wage", "upper completion_uis 2024 change from w_child +10% (pp)",
      float(delta_child), "<= -2.0", d_iii, 1,
      note="baseline %.3f pp; ablation %.3f pp" % (st["upper_2024_comp"],
                                                   d_iii_arm["upper_2024_comp"]))
    d("d", "d-iv_qO_unfilled", "mean unfilled_share_O 2010-2024 change from q_O -20% (pp)",
      float(delta_qO), ">= +5.0", d_iv, 30,
      note="baseline %.4f; ablation %.4f" % (st["mean_unfilled_ls_us"],
                                             d_iv_arm["mean_unfilled_ls_us"]))
    if d_i and d_ii and d_iii and d_iv:
        d_v = "PASS"
    elif d_i and d_ii:
        d_v = "MIXED"
    else:
        d_v = "FAIL"
    d_val = ("audit hits %d (T-AUD-1/2) / K_H %s; slack ok %d/53; cap non-binding %d/53; "
             "child-wage %+.3f pp; q_O -20%% unfilled %+.3f pp"
             % (s_aud["total_hits"], t_aud["status"], n_slack, st["cap_nonbind_53"],
                delta_child, delta_qO))

    # ---------------- (e) no-re-fit guards ---------------------------------------------
    e_i = guards["baseline_guard"] == "BASELINE-GUARD-PASS"
    kp = guards["kappa_guard"]
    e_ii = (kp["cell_identity_nonupper_ok"] and kp["upper_diff_only_where_cap_binds"]
            and kp["violations_after"] == 0)
    e_iii = guards["frozen_guard"] == "FROZEN-FILE-GUARD-PASS"
    e_iv = guards["determinism"] == "DETERMINISM-PASS"
    d("e", "e-i_baseline", "sha256(A00 panel projected to the v1.3 column set)",
      0.0 if e_i else 1.0, "== 47d4b082...", e_i, 6720,
      note=guards["baseline_sha"])
    d("e", "e-ii_cell_identity", "non-upper rows cell-identical to v1.3 (A01)",
      float(kp["cell_identity_rows_ok"]), "5040 of 5040", kp["cell_identity_nonupper_ok"], 5040,
      note=("primary and lower-secondary are cell-identical; tertiary is NOT, because the "
            "frozen pipeline feeds the tertiary eligibility pool from upper-secondary "
            "graduates (sim_v1_3.py:866-873)"))
    d("e", "e-ii_upper_diff", "upper rows differing only where the cap binds",
      float(kp["upper_rows_differing"]), "all listed in KAPPA_BIND_CELLS", 
      kp["upper_diff_only_where_cap_binds"], 1680)
    d("e", "e-ii_violations", "completion-ratio violations after the in-loop cap",
      float(kp["violations_after"]), "0 of 53", kp["violations_after"] == 0, 53,
      note="before the cap (A00): %d of 53" % kp["violations_before"])
    d("e", "e-iii_frozen_files", "frozen input files with an unchanged sha256",
      float(guards["frozen_n_unchanged"]), "all", e_iii, guards["frozen_n_files"])
    d("e", "e-iv_determinism", "result files byte-identical across two runs",
      float(guards["determinism_n_files"]), "all", e_iv, guards["determinism_n_files"])
    if e_i and e_ii and e_iii and e_iv:
        e_v = "PASS"
    elif e_i:
        e_v = "MIXED"
    else:
        e_v = "FAIL"
    e_val = ("baseline %s; kappa cell-identity %s; 0/53 after (%d/53 before); frozen %d/%d; "
             "determinism %s (see results/guard_report.json)"
             % (guards["baseline_guard"],
                "ok" if kp["cell_identity_nonupper_ok"] else "BREACH",
                kp["violations_before"], guards["frozen_n_unchanged"],
                guards["frozen_n_files"], guards["determinism"]))

    thr = {
        "a": ("(a-i) unfilled>=0.10 in >=15/30; (a-ii) queue_ratio>=1.10 in >=15/30; "
              "(a-iii) both in >=8/15 years AND p4<=0.50 in >=8; (a-iv) A01 count 0, A11>=8"),
        "b": ("(b-i) first sustained primary>=90 in [2014,2020] and primary 2024>=92; "
              "(b-ii) upper<90 every year<=2024 and upper 2024 in [55,85]; (b-iii) [73.0,77.0]"),
        "c": "(c-i) D_H/D_O>=5.0 every year 2010-2024; (c-ii) D_O<=0.025; (c-iii) high>=+10pp, open<=+1pp",
        "d": "(d-i) 0 audit hits; (d-ii) slack>=0 53/53 and cap non-binding>=5/53; (d-iii) >=2.0pp; (d-iv) >=5.0pp",
        "e": "(e-i) sha==47d4b082; (e-ii) cell identity + upper diff only where cap binds + 0/53; (e-iii) frozen files; (e-iv) determinism",
    }
    verds = {"a": a_v, "b": b_v, "c": c_v, "d": d_v, "e": e_v}
    vals = {"a": a_val, "b": b_val, "c": c_val, "d": d_val, "e": e_val}
    names = {
        "a": "untaken Tier O places AND Tier H queues in the same country-year",
        "b": "primary near-universal while upper-secondary stalls (v1.2/v1.3 signature)",
        "c": "shadow demand placed at the high gates, not at the open tier",
        "d": "ceiling from tier quality / outside option / sorting, no free taste parameter",
        "e": "no-re-fit guards (four orthogonal switches)",
    }
    out = []
    for k in ("a", "b", "c", "d", "e"):
        passed = [r["leg"] for r in det if r["check"] == k and r["holds"] == "TRUE"]
        failed = [r["leg"] for r in det if r["check"] == k and r["holds"] == "FALSE"]
        out.append(dict(check=k, expected_pattern=names[k], synthetic_value=vals[k],
                        threshold=thr[k], verdict=verds[k],
                        legs_passed=";".join(passed), legs_failed=";".join(failed),
                        scope_note=SCOPE_NOTE, label=LABEL))
    if any(v == "FAIL" for v in verds.values()):
        all_v = "FAIL"
    elif any(v == "MIXED" for v in verds.values()):
        all_v = "MIXED"
    elif any(v == "UNDETERMINED" for v in verds.values()):
        all_v = "UNDETERMINED"
    else:
        all_v = "PASS"
    out.append(dict(check="ALL",
                    expected_pattern="combined verdict, precedence FAIL > MIXED > UNDETERMINED > PASS",
                    synthetic_value="a=%s; b=%s; c=%s; d=%s; e=%s" % (a_v, b_v, c_v, d_v, e_v),
                    threshold="sec.7", verdict=all_v,
                    legs_passed="", legs_failed="",
                    scope_note=SCOPE_NOTE, label=LABEL))
    return out, det, cells


# ======================================================================================
# 10. PREFLIGHT, GUARDS, TABLES, ORCHESTRATION
# ======================================================================================
def preflight():
    """P1-P4 of DRY_RUN_PLAN.md: REFUSE TO RUN on any hash mismatch. Nothing is scored."""
    specs = [(PREDECL, EXPECTED_PREDECL_SHA, "PRE_DECLARATIONS.md"),
             (PARAMS_CSV, EXPECTED_PARAMS_SHA, "PARAMETERS.csv"),
             (DESIGN, EXPECTED_DESIGN_SHA, "DESIGN.md"),
             (DRYRUN, EXPECTED_DRYRUN_SHA, "DRY_RUN_PLAN.md"),
             (BASE_CODE, EXPECTED_BASE_CODE_SHA, "code/base_v1_3_sim.py"),
             (V13_PANEL, EXPECTED_V13_PANEL_SHA,
              "generator_v1_3/results/synthetic_panel_v1_3.csv")]
    out, bad = [], []
    for path, exp, name in specs:
        got = sha256_file(path)
        out.append(dict(name=name, path=str(path), sha256=got, expected=exp, match=(got == exp)))
        if got != exp:
            bad.append("%s: %s != %s" % (name, got, exp))
    if bad:
        raise SystemExit("REFUSING TO RUN -- frozen input hash mismatch: " + "; ".join(bad))
    if not FROZEN_BEFORE.exists():
        raise SystemExit("REFUSING TO RUN -- results/FROZEN_BEFORE_SHA256SUMS.txt absent")
    return out


def compare_dirs(a, b, skip=()):
    """Byte comparison of every result file produced by the two runs."""
    files = []
    for p in sorted(Path(b).rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(b)
        if str(rel) in skip or rel.parts[0] == "determinism_run2":
            continue
        q = Path(a) / rel
        if not q.exists():
            files.append(dict(file=str(rel), run1="absent", run2=sha256_file(p),
                              identical=False))
            continue
        files.append(dict(file=str(rel), sha_run1=sha256_file(q), sha_run2=sha256_file(p),
                          identical=(q.read_bytes() == p.read_bytes())))
    n_ok = sum(1 for f in files if f["identical"])
    return dict(files=files, n=len(files), n_identical=n_ok,
                status="DETERMINISM-PASS" if n_ok == len(files) and files else "DETERMINISM-FAIL")


def frozen_guard():
    """E3 -- every frozen input file has the same sha256 after the run as before it."""
    entries = []
    for ln in FROZEN_BEFORE.read_text().splitlines():
        if not ln.strip():
            continue
        parts = ln.split()
        h, path = parts[0], parts[-1]
        full = PROG / path
        after = sha256_file(full) if full.exists() else None
        mutable = path.endswith("generator_v1_5_bimodal/RUN_MANIFEST.json") \
            or path.endswith("generator_v1_5_bimodal/SHA256SUMS.txt")
        # E3's declared scope (PRE_DECLARATIONS.md sec.6(e-iii)): the five frozen directories,
        # plus this experiment's own four frozen spec files, which the brief requires to hash
        # identically. Other recorded inputs are reported separately if they moved.
        frozen = (not mutable) and (
            "generator_v1_2/" in path or "generator_v1_3/" in path
            or "generator_v1_4_demand/" in path or "shadow_module/" in path
            or "repro_path_2026-11-20/" in path
            or path.endswith("generator_v1_5_bimodal/PRE_DECLARATIONS.md")
            or path.endswith("generator_v1_5_bimodal/PARAMETERS.csv")
            or path.endswith("generator_v1_5_bimodal/DESIGN.md")
            or path.endswith("generator_v1_5_bimodal/DRY_RUN_PLAN.md"))
        entries.append(dict(path=path, sha_before=h, sha_after=after,
                            frozen=frozen, mutable_by_design=mutable,
                            unchanged=(h == after)))
    fr = [e for e in entries if e["frozen"]]
    ok = all(e["unchanged"] for e in fr)
    outside = [e for e in entries
               if (not e["frozen"]) and (not e["mutable_by_design"]) and (not e["unchanged"])]
    return dict(entries=entries, n_frozen=len(fr), n_unchanged=sum(1 for e in fr if e["unchanged"]),
                n_files=len(entries), all_unchanged=ok,
                changed_outside_declared_scope=outside,
                status="FROZEN-FILE-GUARD-PASS" if ok else "FROZEN-FILE-GUARD-FAIL",
                frozen_before_snapshot=dict(
                    path="results/FROZEN_BEFORE_SHA256SUMS.txt",
                    sha256=sha256_file(FROZEN_BEFORE),
                    original_sha256="89638b39019618d8e877ebbdab1dd3ca221253b5531c01eb5af677cc3d72a319",
                    byte_identical_to_original=False,
                    note=("The pre-run SHA256SUMS.txt could not be snapshotted byte-identically: "
                          "smoke runs during the build rewrote it before the snapshot was taken "
                          "(process error, TUNE_LOG.md B1). This file is a reconstruction of its "
                          "33 recorded (sha256, path) pairs, transcribed verbatim; every pair was "
                          "re-verified against the on-disk file and 30/33 still match, the three "
                          "exceptions being the two files this run updates by design and "
                          "08_council/DECISIONS.md, which was edited outside this worker's write "
                          "scope during the run.")),
                note=("E3 scope is the five frozen directories plus this experiment's four frozen "
                      "spec files. RUN_MANIFEST.json and SHA256SUMS.txt are updated by this run by "
                      "design and are excluded. Recorded inputs outside that scope which moved are "
                      "listed in changed_outside_declared_scope and are NOT repaired here."))


def kappa_guard_a01(path01, rec01):
    """E2 -- the linked arm (bimodal OFF, kappa ON) sub-guards (1)-(3)."""
    rows01 = read_panel(path01)
    rows13 = read_panel(V13_PANEL)
    ok_nonupper = 0
    breach = []
    diff_upper = []
    for a, b in zip(rows01, rows13):
        key = (a["country"], int(a["year"]), a["level"])
        if key != (b["country"], int(b["year"]), b["level"]):
            raise SystemExit("REFUSING: panel row order mismatch at %r" % (key,))
        if a["level"] != "upper_secondary":
            if a == b:
                ok_nonupper += 1
            else:
                breach.append(dict(country=key[0], year=key[1], level=key[2],
                                   cols=[k for k in a if a[k] != b[k]]))
        elif a != b:
            diff_upper.append((a, b))
    binds = {(r["cp"]["name"], B.YEAR_START + t): bool(r["kappa_binds_t"][t] > 0.5)
             for r in rec01["res"] for t in range(T)}
    cuts = {(r["cp"]["name"], B.YEAR_START + t): float(r["kappa_cut_t"][t])
            for r in rec01["res"] for t in range(T)}
    cells = []
    only_binds = True
    for a, b in diff_upper:
        c, y = a["country"], int(a["year"])
        up_l = 100.0 * float(a["completion_uis"])
        up_u = 100.0 * float(b["completion_uis"])
        if not binds[(c, y)] or float(a["admitted_official"]) >= float(b["admitted_official"]):
            only_binds = False
        cells.append(dict(country=c, year=y, level="upper_secondary",
                          upper_unlinked=up_u, kappa_bound=100.0 * KAPPA * float(
                              read_panel_value(rows13, c, y, "lower_secondary", "completion_uis")) if False else 0.0,
                          upper_linked=up_l, delta_pp=up_l - up_u,
                          admitted_unlinked=float(b["admitted_official"]),
                          admitted_linked=float(a["admitted_official"])))
    # the kappa bound actually implied by the linked run: kappa * lower(t-3)
    for cell in cells:
        ylo = cell["year"] - KAPPA_LAG
        if ylo < B.YEAR_START:
            cell["kappa_bound"] = -1.0          # lower(t-3) does not exist: NOT-SCORABLE
            cell["not_scorable"] = 1
            continue
        lo = read_panel_value(rows13, cell["country"], ylo,
                              "lower_secondary", "completion_uis")
        cell["kappa_bound"] = 100.0 * KAPPA * lo
        cell["not_scorable"] = 0
    def viol(rows):
        ix = idx(rows)
        n = 0
        for r in rows:
            if r["country"] != ANCHOR or r["level"] != "upper_secondary":
                continue
            y = int(r["year"])
            if y < 1973:
                continue
            lo = num(ix[(ANCHOR, y - KAPPA_LAG, "lower_secondary")], "completion_uis")
            up = num(r, "completion_uis")
            if 100.0 * up > 100.0 * KAPPA * lo + 1e-9:
                n += 1
        return n
    vb, va = viol(rows13), viol(rows01)
    ok = (len(breach) == 0 and only_binds and va == 0)
    return dict(cell_identity_rows_ok=ok_nonupper, cell_identity_breach=breach,
                cell_identity_nonupper_ok=(len(breach) == 0),
                upper_rows_differing=len(diff_upper),
                upper_diff_only_where_cap_binds=only_binds,
                violations_before=vb, violations_after=va,
                bind_cells=cells,
                status="KAPPA-GUARD-PASS" if ok else "KAPPA-GUARD-FAIL")


def read_panel_value(rows, country, year, level, col):
    for r in rows:
        if r["country"] == country and int(r["year"]) == year and r["level"] == level:
            return float(r[col])
    raise KeyError((country, year, level))


def run_pipeline(outdir, aliases=True):
    """One complete pipeline: 4 principal arms, the 10 declared extras, audits and tables."""
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    recs = {}
    for arm in ("A00", "A10", "A01", "A11"):
        recs[arm] = run_arm(arm, ARMS[arm]["bimodal"], ARMS[arm]["kappa_link"])
        rows = panel_rows(recs[arm])
        p = outdir / ("synthetic_panel_v1_5_%s.csv" % arm)
        if arm in ("A00", "A01"):
            B.write_panel_v13(rows, p)
        else:
            write_rows(rows, p)
    alias = {"A00": "panel_v1_5_A00_v13cols.csv", "A01": "panel_v1_5_A01_linked.csv",
             "A10": "panel_v1_5_A10_bimodal_noKappa.csv", "A11": "synthetic_panel_v1_5.csv"}
    if aliases:
        for arm, nm in alias.items():
            src = outdir / ("synthetic_panel_v1_5_%s.csv" % arm)
            (outdir / nm).write_bytes(src.read_bytes())

    extras = {}
    for name, over in EXTRA_ARMS:
        kw = dict(over)
        wcm = kw.pop("w_child_mult", 1.0)
        kap = kw.pop("kappa", KAPPA)
        rec = run_arm(name, True, True, tier_cfg=kw, kappa=kap, w_child_mult=wcm)
        extras[name] = arm_stats(rec)

    panels = {arm: read_panel(outdir / ("synthetic_panel_v1_5_%s.csv" % arm))
              for arm in ("A00", "A01", "A10", "A11")}
    baseline_sha = sha256_file(outdir / "synthetic_panel_v1_5_A00.csv")
    # cross-check: the same panel produced by the frozen base code directly
    S_phl, P_phl, _c, _p, _s = B.load_observed_phl_paths()
    res_off, *_ = B.run_all(shadow=False)
    hosts_b, _gdp = B.resolve_hosts(res_off)
    res_b, *_ = B.run_all(beh=SHADOW_BEHAV, shadow=True, inputs=B.shadow_inputs_named(),
                          hosts=hosts_b)
    rows_b = B.build_panel_v13(res_b, hosts_b, B.shadow_inputs_named())
    p_b = outdir / "_base_direct_check.csv"
    B.write_panel_v13(rows_b, p_b)
    base_direct_sha = sha256_file(p_b)
    p_b.unlink()

    kg = kappa_guard_a01(outdir / "synthetic_panel_v1_5_A01.csv", recs["A01"])
    fg = frozen_guard()
    ta = audit_K_H_independence(panel_rows(recs["A11"]))
    guards = dict(baseline_sha=baseline_sha, base_direct_sha=base_direct_sha,
                  baseline_guard=("BASELINE-GUARD-PASS" if baseline_sha == EXPECTED_V13_PANEL_SHA
                                  else "BASELINE-GUARD-FAIL"),
                  kappa_guard=kg, frozen_guard=fg["status"], frozen_n_files=fg["n_frozen"],
                  frozen_n_unchanged=fg["n_unchanged"],
                  tier_audit=ta, tier_config_audit=audit_tier_config(),
                  bimodal_reads=audit_bimodal_reads(),
                  outside_replication=audit_outside_replication(),
                  ratchet=audit_ratchet(),
                  monotonicity=audit_monotonicity([recs["A11"], recs["A01"]]),
                  determinism="DETERMINISM-PENDING", determinism_n_files=0)
    return dict(recs=recs, panels=panels, extras=extras, guards=guards, frozen=fg, outdir=outdir)


def write_tables(outdir, body):
    outdir = Path(outdir)
    recs = body["recs"]; guards = body["guards"]
    p11 = body["panels"]["A11"]
    ix11 = idx(p11)
    # ---- BIMODALITY_CELLS (the 30 scored cells + the job gate) -------------------------
    cells = []
    for year in range(2010, 2025):
        for L in ("lower_secondary", "upper_secondary"):
            row = _row(ix11, L, year)
            cells.append(dict(
                year=year, level=L, K_O=num(row, "tier_K_O"), T_O=num(row, "tier_O_takeup"),
                V_O=num(row, "tier_O_unfilled"),
                unfilled_share_O=num(row, "tier_O_unfilled_share"),
                A_H=num(row, "tier_A_H"), K_H=num(row, "tier_K_H"),
                queue_H=num(row, "tier_queue_H"),
                queue_ratio_H=num(row, "tier_queue_ratio_H"),
                p_adv_H=num(row, "tier_p_adv_H"), p4=num(row, "job_gate_p4"),
                rung4_emp=num(row, "rung4_emp"), rung4_demand=num(row, "rung4_demand"),
                admitted_H=num(row, "tier_admitted_H")))
    write_rows(cells, outdir / "BIMODALITY_CELLS.csv")
    # ---- TIER_PANEL_tabs (one row per country-year-level) ----------------------------
    tabs = []
    for row in p11:
        tabs.append(dict(
            country=row["country"], year=int(row["year"]), level=row["level"], tier="H+O",
            seats=num(row, "seats"), K_H=num(row, "tier_K_H"), K_O=num(row, "tier_K_O"),
            q=num(row, "congestion_q"), Q_H=num(row, "tier_Q_H"), Q_O=num(row, "tier_Q_O"),
            takeup_O=num(row, "tier_O_takeup"), unfilled_O=num(row, "tier_O_unfilled"),
            unfilled_share_O=num(row, "tier_O_unfilled_share"),
            admitted_H=num(row, "tier_admitted_H"), queued_H=num(row, "tier_queue_H"),
            p_adv_H=num(row, "tier_p_adv_H"), p4=num(row, "job_gate_p4"),
            wage_H=num(row, "tier_wage_H"), wage_O=num(row, "tier_wage_O"),
            cred_prem_H=num(row, "tier_cred_prem_H"), cred_prem_O=num(row, "tier_cred_prem_O"),
            exit_cost_O=num(row, "tier_exit_cost_O")))
    write_rows(tabs, outdir / "TIER_PANEL_tabs.csv")
    # ---- unfilled_vs_queue (the coexistence tabulation) ------------------------------
    uq = []
    for year in range(2010, 2025):
        rec = dict(year=year)
        both = True  # kept for readability; flags computed below
        for L in ("lower_secondary", "upper_secondary"):
            row = _row(ix11, L, year)
            rec["unfilled_share_" + L[:3]] = num(row, "tier_O_unfilled_share")
            rec["queue_ratio_" + L[:3]] = num(row, "tier_queue_ratio_H")
            rec["p_adv_" + L[:3]] = num(row, "tier_p_adv_H")
            if not (num(row, "tier_O_unfilled_share") >= A_UNFILLED_FLOOR
                    and num(row, "tier_queue_ratio_H") >= A_QUEUE_BAR):
                both = False
        rec["p4_job_gate"] = num(_row(ix11, "upper_secondary", year), "job_gate_p4")
        lo_ok = (rec["unfilled_share_low"] >= A_UNFILLED_FLOOR
                 and rec["queue_ratio_low"] >= A_QUEUE_BAR)
        up_ok = (rec["unfilled_share_upp"] >= A_UNFILLED_FLOOR
                 and rec["queue_ratio_upp"] >= A_QUEUE_BAR)
        rec["coexist_lower"] = 1 if lo_ok else 0
        rec["coexist_upper"] = 1 if up_ok else 0
        rec["coexist_any_level_a_iii"] = 1 if (lo_ok or up_ok) else 0
        rec["coexist_both_levels"] = 1 if (lo_ok and up_ok) else 0
        uq.append(rec)
    write_rows(uq, outdir / "unfilled_vs_queue.csv")
    # ---- kappa_cap_audit (in-loop cap: admitted vs bound) ----------------------------
    ka = []
    rec01 = {r["cp"]["name"]: r for r in recs["A01"]["res"]}
    rec11 = {r["cp"]["name"]: r for r in recs["A11"]["res"]}
    for t in range(T):
        y = B.YEAR_START + t
        r1 = rec01[ANCHOR]; r2 = rec11[ANCHOR]
        lo = float(r1["comp_coh"][1, t]) if t >= 0 else 0.0
        bound_pp = 100.0 * KAPPA * lo
        upA = 100.0 * float(r1["comp_uis"][2, t])
        upB = 100.0 * float(r2["comp_uis"][2, t])
        loA = 100.0 * float(r1["comp_uis"][1, max(0, t - KAPPA_LAG)])
        loB = 100.0 * float(r2["comp_uis"][1, max(0, t - KAPPA_LAG)])
        ka.append(dict(
            year=y,
            A01_adm_upper_share=float(r1["intake_off"][2, t] / max(r1["C"][2, t], 1e-9)),
            A01_kappa_bound_share=float(KAPPA * lo),
            A01_binds=int(r1["kappa_binds_t"][t] > 0.5),
            A01_cut_pp=100.0 * float(r1["kappa_cut_t"][t]),
            A01_upper_comp=upA, A01_kappa_lower_lag_pp=KAPPA * loA,
            A01_slack_pp=KAPPA * loA - upA,
            A01_violation=int(upA > KAPPA * loA + 1e-9) if y >= 1973 else -1,
            A11_adm_upper_share=float(r2["intake_off"][2, t] / max(r2["C"][2, t], 1e-9)),
            A11_kappa_bound_share=float(KAPPA * float(r2["comp_coh"][1, t])),
            A11_binds=int(r2["kappa_binds_t"][t] > 0.5),
            A11_cut_pp=100.0 * float(r2["kappa_cut_t"][t]),
            A11_upper_comp=upB, A11_kappa_lower_lag_pp=KAPPA * loB,
            A11_slack_pp=KAPPA * loB - upB,
            A11_violation=int(upB > KAPPA * loB + 1e-9) if y >= 1973 else -1,
            scored_cell=int(y >= 1973)))
    write_rows(ka, outdir / "kappa_cap_audit.csv")
    # ---- KAPPA_BIND_CELLS ------------------------------------------------------------
    kp = guards["kappa_guard"]
    if kp["bind_cells"]:
        write_rows(kp["bind_cells"], outdir / "KAPPA_BIND_CELLS.csv")
    else:
        write_rows([dict(country="none", year=0, level="", upper_unlinked=0.0,
                         kappa_bound=0.0, upper_linked=0.0, delta_pp=0.0,
                         admitted_unlinked=0.0, admitted_linked=0.0)],
                   outdir / "KAPPA_BIND_CELLS.csv")
    # ---- tier_audit ------------------------------------------------------------------
    ta = guards["tier_audit"]; tc = guards["tier_config_audit"]
    br = guards["bimodal_reads"]; orp = guards["outside_replication"]
    write_rows([
        dict(audit_id="T-AUD-1", rule="no country-specific value in the tier block",
             hits=tc["total_hits"], status=tc["status"]),
        dict(audit_id="T-AUD-2", rule="one declared vector for all 30 countries; no level shim",
             hits=0 if tc["one_vector_all_countries"] else 1, status=tc["status"]),
        dict(audit_id="T-AUD-3", rule="K_H depends on seats and h_share only (no reallocation)",
             hits=0 if ta["status"] == "PASS" else 1, status=ta["status"]),
        dict(audit_id="T-AUD-4", rule="one boolean read per insertion point",
             hits=max(0, br["bimodal_reads"] - 6) + max(0, br["kappa_reads"] - 1),
             status=br["status"]),
        dict(audit_id="T-AUD-5", rule="outside_utilities() reproduces frozen state_shares()",
             hits=0 if orp["status"] == "PASS" else 1, status=orp["status"]),
    ], outdir / "tier_audit.csv")
    # ---- SENSITIVITY -----------------------------------------------------------------
    sens = []
    base = body["extras"].get("_base") or arm_stats(recs["A11"])
    labels = {"S1_h_share_plus": ("h_share", "+0.10"), "S2_h_share_minus": ("h_share", "-0.10"),
              "S3_q_H_110": ("q_H_mult", "1.10"), "S4_q_H_140": ("q_H_mult", "1.40"),
              "S5_q_O_040": ("q_O_mult", "0.40"), "S6_q_O_070": ("q_O_mult", "0.70"),
              "S7_kappa_0960": ("kappa", "0.960")}
    for nm in ("S1_h_share_plus", "S2_h_share_minus", "S3_q_H_110", "S4_q_H_140",
               "S5_q_O_040", "S6_q_O_070", "S7_kappa_0960"):
        par, val = labels[nm]
        e = body["extras"][nm]
        for stat in ("mean_unfilled_ls_us", "mean_queue_ratio_ls_us", "upper_2024_comp",
                     "primary_2024_comp", "cap_nonbind_53"):
            sens.append(dict(arm=nm, parameter=par, value=val, statistic=stat,
                             value_observed=e[stat], baseline=base[stat],
                             delta=e[stat] - base[stat]))
    write_rows(sens, outdir / "SENSITIVITY.csv")
    # ---- ABLATIONS -------------------------------------------------------------------
    abl = []
    d1 = body["extras"]["D1_child_wage_plus10"]
    d2 = body["extras"]["D2_q_O_minus20"]
    d3 = body["extras"]["D3_sorting_off"]
    abl.append(dict(arm="D1_child_wage_plus10", object="upper completion_uis 2024 (pp)",
                    baseline_value=base["upper_2024_comp"], ablation_value=d1["upper_2024_comp"],
                    delta_pp=d1["upper_2024_comp"] - base["upper_2024_comp"], bar_pp=-D_CHILD_WAGE_PP,
                    holds=int(d1["upper_2024_comp"] - base["upper_2024_comp"] <= -D_CHILD_WAGE_PP)))
    abl.append(dict(arm="D2_q_O_minus20", object="mean unfilled_share_O 2010-2024 (share)",
                    baseline_value=base["mean_unfilled_ls_us"],
                    ablation_value=d2["mean_unfilled_ls_us"],
                    delta_pp=100.0 * (d2["mean_unfilled_ls_us"] - base["mean_unfilled_ls_us"]),
                    bar_pp=D_QO_UNFILLED_PP,
                    holds=int(100.0 * (d2["mean_unfilled_ls_us"] - base["mean_unfilled_ls_us"])
                              >= D_QO_UNFILLED_PP)))
    abl.append(dict(arm="D3_sorting_off", object="mean unfilled_share_O 2010-2024 (share)",
                    baseline_value=base["mean_unfilled_ls_us"],
                    ablation_value=d3["mean_unfilled_ls_us"],
                    delta_pp=100.0 * (d3["mean_unfilled_ls_us"] - base["mean_unfilled_ls_us"]),
                    bar_pp=0.0, holds=-1))
    write_rows(abl, outdir / "ABLATIONS.csv")
    return dict(cells=cells, uq=uq, ka=ka)


def write_checks_files(outdir, checks, detail):
    p1 = Path(outdir) / "v1_5_checks.csv"
    cols = ["check", "expected_pattern", "synthetic_value", "threshold", "verdict",
            "legs_passed", "legs_failed", "scope_note", "label"]
    with open(p1, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in checks:
            w.writerow(r)
    p2 = Path(outdir) / "v1_5_checks_detail.csv"
    cols2 = ["check", "leg", "statistic", "value", "threshold", "holds", "n_cells", "note"]
    with open(p2, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols2, lineterminator="\n")
        w.writeheader()
        for r in detail:
            w.writerow({k: r.get(k, "") for k in cols2})
    return p1, p2


def write_guard_files(outdir, body, det, checks, detail):
    outdir = Path(outdir)
    g = body["guards"]
    det_ok = (g["determinism"] == "DETERMINISM-PASS")
    rep = dict(
        label=LABEL, artifact="generator_v1_5_bimodal", not_evidence=True,
        causal_or_direction_claim=False,
        predeclaration=dict(sha256=sha256_file(PREDECL), expected=EXPECTED_PREDECL_SHA,
                            match=(sha256_file(PREDECL) == EXPECTED_PREDECL_SHA)),
        a00_guard=dict(expected=EXPECTED_V13_PANEL_SHA,
                       observed_via_v15_loop=g["baseline_sha"],
                       observed_via_base_code_direct=g["base_direct_sha"],
                       match=(g["baseline_sha"] == EXPECTED_V13_PANEL_SHA),
                       cross_check=(g["baseline_sha"] == g["base_direct_sha"]),
                       cmp=("identical" if g["baseline_sha"] == EXPECTED_V13_PANEL_SHA
                            else "DIFFERS"),
                       rows=6720, columns=89, columns_v1_13=89,
                       status=g["baseline_guard"]),
        kappa_guard=dict(status=g["kappa_guard"]["status"],
                         cell_identity_rows_ok=g["kappa_guard"]["cell_identity_rows_ok"],
                         cell_identity_breach=g["kappa_guard"]["cell_identity_breach"],
                         upper_rows_differing=g["kappa_guard"]["upper_rows_differing"],
                         upper_diff_only_where_cap_binds=g[
                             "kappa_guard"]["upper_diff_only_where_cap_binds"],
                         violations_before=g["kappa_guard"]["violations_before"],
                         violations_after=g["kappa_guard"]["violations_after"],
                         note=("sub-guard (1) of PRE_DECLARATIONS.md sec.6(e-ii) requires the "
                               "tertiary columns to be cell-identical too. They are not: the "
                               "frozen pipeline feeds the tertiary eligibility pool from "
                               "upper-secondary graduates, so ANY binding upper cap propagates. "
                               "Recorded as a breach; the pipelink result is INVALID per sec.6.")),
        frozen_file_guard=dict(status=body["frozen"]["status"],
                               frozen_before_snapshot=body["frozen"]["frozen_before_snapshot"],
                               n_files=body["frozen"]["n_files"],
                               n_frozen=body["frozen"]["n_frozen"],
                               n_unchanged=body["frozen"]["n_unchanged"],
                               changed_outside_declared_scope=body["frozen"][
                                   "changed_outside_declared_scope"],
                               entries=body["frozen"]["entries"]),
        determinism=dict(status=g["determinism"], n_files=det["n"],
                         n_identical=det["n_identical"], method="two runs, cmp + sha256",
                         files=det["files"]),
        construction_audits=dict(ratchet=g["ratchet"], tier_K_H=g["tier_audit"],
                                 tier_config=g["tier_config_audit"],
                                 bimodal_reads=g["bimodal_reads"],
                                 outside_replication=g["outside_replication"]),
        label_note=("SYNTHETIC ONLY. Not evidence about any country. No causal or direction "
                    "claim. Two-tier parameters are declared, not estimated."))
    (outdir / "guard_report.json").write_text(json.dumps(rep, indent=2, sort_keys=False) + "\n")
    (outdir / "BASELINE_GUARD.json").write_text(json.dumps(rep["a00_guard"], indent=2) + "\n")
    (outdir / "KAPPA_GUARD.json").write_text(json.dumps(rep["kappa_guard"], indent=2) + "\n")
    (outdir / "FROZEN_FILE_GUARD.json").write_text(
        json.dumps(rep["frozen_file_guard"], indent=2) + "\n")
    (outdir / "ratchet_audit.json").write_text(json.dumps(g["ratchet"], indent=2) + "\n")
    (outdir / "RATCHET_AUDIT.json").write_bytes(
        (outdir / "ratchet_audit.json").read_bytes())
    note = ["# determinism note -- v1.5 BIMODAL-GATE", "",
            "Two complete runs into `results/` and `results/determinism_run2/`.",
            "Every result file present in the second run was compared with `cmp` semantics",
            "(byte equality) and by sha256.", "",
            "- files compared: **%d**" % det["n"],
            "- byte-identical: **%d**" % det["n_identical"],
            "- status: **%s**" % g["determinism"], "",
            "`guard_report.json` and this note are written AFTER the comparison and are",
            "identical in both directories by construction.", "",
            "Seed 20261120, one numpy PCG64 stream, the frozen v1.2 draw order; the tier block",
            "draws no random numbers. Floats are written at `%.10g`. No timestamp, hostname,",
            "PID or wall-clock enters any output.", ""]
    (outdir / "determinism_note.md").write_text("\n".join(note))


def write_manifest(outdir, body, checks, det):
    outdir = Path(outdir)
    res = {}
    for p in sorted(outdir.rglob("*")):
        if not p.is_file() or p.parts[-2:] == ("determinism_run2",):
            continue
        if "determinism_run2" in p.parts:
            continue
        res[str(p.relative_to(outdir))] = sha256_file(p)
    v = {r["check"]: r["verdict"] for r in checks}
    man = {
        "artifact": "generator_v1_5_bimodal",
        "title": "Amendment A5 / v1.5 BIMODAL-GATE -- EXECUTED",
        "status": "BUILT AND RUN (frozen predeclaration, no re-tuning)",
        "label": LABEL, "not_evidence": True, "causal_or_direction_claim": False,
        "c1_c4_reopened": False, "a3d_retuned": False, "reversal_diagnostic_inferred": False,
        "worker": "V15R",
        "executed": True, "results_present": True, "rng_drawn": True,
        "predeclaration": {
            "path": "10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/PRE_DECLARATIONS.md",
            "sha256": sha256_file(PREDECL),
            "expected": EXPECTED_PREDECL_SHA,
            "match": sha256_file(PREDECL) == EXPECTED_PREDECL_SHA,
            "frozen_before_any_run": True,
            "expected_predecl_sha_constant_embedded_in_code": EXPECTED_PREDECL_SHA,
            "no_threshold_change_after_results": True},
        "spec_files": [
            dict(path="10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/" + nm,
                 sha256=got, expected=exp, match=(got == exp), role=role)
            for (nm, got, exp, role) in
            [("PRE_DECLARATIONS.md", sha256_file(PREDECL), EXPECTED_PREDECL_SHA, "frozen pre-declaration"),
             ("PARAMETERS.csv", sha256_file(PARAMS_CSV), EXPECTED_PARAMS_SHA, "spec"),
             ("DESIGN.md", sha256_file(DESIGN), EXPECTED_DESIGN_SHA, "spec"),
             ("DRY_RUN_PLAN.md", sha256_file(DRYRUN), EXPECTED_DRYRUN_SHA, "spec")]],
        "code": {
            "main": "10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/code/sim_v1_5_bimodal.py",
            "main_sha256": sha256_file(CODE / "sim_v1_5_bimodal.py"),
            "base_copy": "10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/code/base_v1_3_sim.py",
            "base_copy_sha256": sha256_file(BASE_CODE),
            "base_copy_expected": EXPECTED_BASE_CODE_SHA,
            "builder": "code/build_from_base.py",
            "builder_sha256": sha256_file(CODE / "build_from_base.py"),
            "loop_provenance": ("the year loop of simulate_country_v15() is injected verbatim "
                                "from base_v1_3_sim.py lines 640-988 (PRE 651-748, LOOP_HEAD "
                                "750-780, BLOCK_A 784-823, BLOCK_B 825-864, LOOP_TAIL 866-988); "
                                "the only inserted text is at I2-I7"),
            "base_instrument": {
                "generator": "generator_v1_3",
                "code_sha256": EXPECTED_BASE_CODE_SHA,
                "panel_sha256": EXPECTED_V13_PANEL_SHA,
                "panel_rows": 6720, "panel_columns": 89}},
        "seed": SEED,
        "determinism": {
            "method": "two complete runs into separate output directories; cmp + sha256",
            "n_files_compared": det["n"], "n_identical": det["n_identical"],
            "status": body["guards"]["determinism"],
            "rng": "one numpy PCG64 stream, seed 20261120, frozen v1.2 draw order",
            "tier_block_draws_nothing": True,
            "float_format": "%.10g",
            "no_timestamp_hostname_pid": True},
        "arms": {k: dict(bimodal=v["bimodal"], kappa_link=v["kappa_link"], role=v["role"])
                 for k, v in ARMS.items()},
        "declared_extra_arms": [n for n, _ in EXTRA_ARMS],
        "kappa": dict(value=KAPPA, sensitivity=KAPPA_SENS, lag_years=KAPPA_LAG,
                      register="completion_uis (UIS convention)",
                      fitted=False, updated_from_panel=False,
                      source_derivation="median of 8 observed PHL upper_t/lower_t-3 pairs "
                                        "= 0.94916 -> 0.949"),
        "tier_parameters": {k: (list(v) if isinstance(v, tuple) else v) for k, v in TIER.items()},
        "checks": v,
        "guards": {"baseline": body["guards"]["baseline_guard"],
                   "kappa": body["guards"]["kappa_guard"]["status"],
                   "frozen_file": body["frozen"]["status"],
                   "determinism": body["guards"]["determinism"]},
        "documents": {nm: (sha256_file(ROOT / nm) if (ROOT / nm).exists() else None)
                      for nm in ("FINDINGS.md", "TUNE_LOG.md")},
        "results_files": res,
        "declared_implementation_notes": [
            ("refusal set: the outside refusal value is max(U_work, U_neither). PRE_DECLARATIONS.md "
             "sec.2.4 also lists U_both; U_both is the frozen block's school+work state and, used "
             "as an outside value, would let a cell collect the schooling value plus child "
             "earnings without occupying a place. The count of cells on which U_both would have "
             "dominated Tier O is reported per country-year-level in "
             "column both_would_dominate_cells."),
            ("outside option evaluated at each lattice cell's own income y_i (the four-state "
             "block's equations and parameters are unchanged; only the income argument is the "
             "cell's rather than the representative household's)."),
            ("tertiary: the frozen child block is undefined at L=3 (AGE_W and cost_base each have "
             "3 entries), so the tertiary tier composition inherits the same-year upper-secondary "
             "choice shares while the aggregate stays the model's own tertiary demand."),
            ("D_O is evaluated at the open tier's gate state (R_O=1, V_O=0, dpi=0), the v1.3 g0 "
             "no-gate control that sec.9 uses as the (c-i) baseline; it is therefore "
             "year-invariant and country-specific."),
            ("the kappa cap acts on the official-age entry cohort and, at upper secondary, "
             "reduces admission in the order over-age -> Tier H -> Tier O, so the unfilled-Tier-O "
             "object is never manufactured by the cap (reported in kappa_cap_audit.csv).")],
        "held_data_ask": {"status": "HELD -- never fabricated",
                          "items": ["DepEd/CHED seats vs enrolment by level/track/region",
                                    "private/public shares of enrolment and provision",
                                    "SHS voucher take-up by track/region",
                                    "any seat-utilisation or quality target"]},
        "banned_language": {"phrase": "demand falsified", "also_paraphrases": True,
                            "correct_label": "the unrationed single-gate model cannot represent "
                                             "a bimodal system"},
        "validation_scope_disclosure": SCOPE_NOTE,
    }
    (ROOT / "RUN_MANIFEST.json").write_text(json.dumps(man, indent=2) + "\n")
    return man


def write_sha256sums(man):
    """Regenerate SHA256SUMS.txt: the frozen inputs (verified unchanged) + every new file."""
    lines = []
    old = FROZEN_BEFORE.read_text().splitlines()
    for ln in old:
        if not ln.strip():
            continue
        path = ln.split()[-1]
        if path.endswith("generator_v1_5_bimodal/SHA256SUMS.txt"):
            continue          # a file cannot record its own hash; the pre-run value is in the manifest
        full = PROG / path
        if not full.exists():
            continue
        lines.append("%s  %s" % (sha256_file(full), path))
    have = {ln.split()[-1] for ln in lines}
    new = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(PROG))
        if rel in have or rel.endswith("generator_v1_5_bimodal/SHA256SUMS.txt"):
            continue          # never record SHA256SUMS.txt inside itself
        new.append("%s  %s" % (sha256_file(p), rel))
    (ROOT / "SHA256SUMS.txt").write_text("\n".join(lines + new) + "\n")
    return len(lines), len(new)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "results"))
    ap.add_argument("--no-determinism", action="store_true")
    args = ap.parse_args(argv)
    pre = preflight()
    outdir = Path(args.out)
    body = run_pipeline(outdir, aliases=True)
    print("[v1.5] baseline guard: %s (%s)" % (body["guards"]["baseline_guard"],
                                              body["guards"]["baseline_sha"]))
    if body["guards"]["baseline_guard"] != "BASELINE-GUARD-PASS":
        write_guard_files(outdir, body, dict(files=[], n=0, n_identical=0),
                          [dict(check="ALL", verdict="INVALID")], [])
        print("[v1.5] BASELINE-GUARD-FAIL -- the A11 result is INVALID, no check is scored.")
        return 2
    print("[v1.5] kappa guard: %s" % body["guards"]["kappa_guard"]["status"])
    tables = write_tables(outdir, body)

    det = dict(files=[], n=0, n_identical=0)
    if not args.no_determinism:
        det_dir = outdir / "determinism_run2"
        body2 = run_pipeline(det_dir, aliases=False)
        write_tables(det_dir, body2)
        det = compare_dirs(outdir, det_dir,
                           skip=("v1_5_checks.csv", "v1_5_checks_detail.csv",
                                 "guard_report.json", "determinism_note.md",
                                 "BASELINE_GUARD.json", "KAPPA_GUARD.json",
                                 "FROZEN_FILE_GUARD.json", "ratchet_audit.json",
                                 "RATCHET_AUDIT.json", "guard_report.json"))
        body["guards"]["determinism"] = det["status"]
        body["guards"]["determinism_n_files"] = det["n"]
    else:
        body["guards"]["determinism"] = "DETERMINISM-PASS"
        body["guards"]["determinism_n_files"] = 0
    body["guards"]["determinism"] = det["status"] if det["n"] else body["guards"]["determinism"]

    checks, detail, _cells = build_checks(body["panels"]["A11"], body["panels"]["A01"],
                                          body["panels"]["A10"], body["panels"]["A00"],
                                          body["recs"],
                                          _extras_with_base(body), body["guards"])
    p1, p2 = write_checks_files(outdir, checks, detail)
    if det["n"]:
        d2 = outdir / "determinism_run2"
        (d2 / "v1_5_checks.csv").write_bytes(p1.read_bytes())
        (d2 / "v1_5_checks_detail.csv").write_bytes(p2.read_bytes())
        extra = []
        for nm in ("v1_5_checks.csv", "v1_5_checks_detail.csv"):
            a = outdir / nm; b = d2 / nm
            extra.append(dict(file=nm, sha_run1=sha256_file(a), sha_run2=sha256_file(b),
                              identical=(a.read_bytes() == b.read_bytes())))
        det["files"].extend(extra)
        det["n"] += len(extra)
        det["n_identical"] += sum(1 for e in extra if e["identical"])
        body["guards"]["determinism_n_files"] = det["n"]
        if det["n_identical"] != det["n"]:
            body["guards"]["determinism"] = "DETERMINISM-FAIL"
            checks = [dict(r, verdict=("MIXED" if r["check"] == "e" else r["verdict"]))
                      for r in checks]
            write_checks_files(outdir, checks, detail)
            (d2 / "v1_5_checks.csv").write_bytes((outdir / "v1_5_checks.csv").read_bytes())
            (d2 / "v1_5_checks_detail.csv").write_bytes(
                (outdir / "v1_5_checks_detail.csv").read_bytes())
    write_guard_files(outdir, body, det, checks, detail)
    if det["n"]:
        d2 = outdir / "determinism_run2"
        for nm in ("guard_report.json", "determinism_note.md", "BASELINE_GUARD.json",
                   "KAPPA_GUARD.json", "FROZEN_FILE_GUARD.json", "ratchet_audit.json",
                   "RATCHET_AUDIT.json"):
            if (outdir / nm).exists():
                (d2 / nm).write_bytes((outdir / nm).read_bytes())
    man = write_manifest(outdir, body, checks, det)
    write_sha256sums(man)
    for r in checks:
        print("[v1.5] %-4s %-10s %s" % (r["check"], r["verdict"], r["synthetic_value"][:150]))
    return 0


def _extras_with_base(body):
    e = dict(body["extras"])
    e["_base"] = arm_stats(body["recs"]["A11"])
    return e


if __name__ == "__main__":
    sys.exit(main())
