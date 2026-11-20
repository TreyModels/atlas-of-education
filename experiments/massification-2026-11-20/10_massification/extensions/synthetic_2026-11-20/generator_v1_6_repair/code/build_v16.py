#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BUILD_V16 -- assemble code/sim_v1_6_repair.py from the frozen v1.3 base + declared insertions.

Mechanical, verified, and refusal-based. The base copy is byte-identical to
generator_v1_3/code/sim_v1_3.py (sha256 70ae8f0e...). The year loop is NOT retyped: it is taken
from the base text and only the declared insertion points are spliced in. With bimodal=False,
kappa_link=False, tier_surv=False every inserted block is the identity, which is what guard G1
(A00 panel == 47d4b082...) certifies.

Insertions (each anchored on an exact, count-checked base string):
  I0  module docstring
  I1  declared V16 switches / parameters / tier helpers            (before `def sig(x):`)
  I2  signature + per-run tier config                              (the def line)
  I3  tier/kappa/one-way stores                                    (after the history buffers)
  I4  tier allocation, I6 kappa cap in completion units, injection (after the rationing block)
  I5  per-tier survival branch (tier_surv arms only)               (after `gr = ...`)
  I7  expectation state (p_adv_H lag, wage gap)                    (after `Y *= (1.0 + g)`)
  I8  entry point is code/run_v16.py, not this module

Run:  python code/build_v16.py
"""
import hashlib
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
BASE = CODE / "base_v1_3_sim.py"
OUT = CODE / "sim_v1_6_repair.py"
PREDECL = ROOT / "PRE_DECLARATIONS.md"

BASE_SHA_EXPECTED = "70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877"

DOCSTRING = '''"""SIM_V1_6_REPAIR -- EXP-14 **V16-REPAIR**: the repaired bimodal generator.

EVERYTHING THIS SCRIPT EMITS IS SYNTHETIC. It is a declared-assumption simulator: not an
estimate, not evidence about any country, not a forecast, and it licenses no causal or
direction claim. SYN00_PHL_LIKE is NOT the Philippines.

Base instrument: the frozen v1.3 generator, copied byte-for-byte to code/base_v1_3_sim.py
(sha256 70ae8f0e...). This file is assembled from that base by code/build_v16.py, which
splices the V16 blocks at the declared insertion points and nowhere else. With
bimodal=False, kappa_link=False, tier_surv=False every inserted block is the identity and
the 89-column panel is byte-identical to generator_v1_3/results/synthetic_panel_v1_3.csv
(sha256 47d4b082...). That is guard G1; it is checked before any check is scored.

What V16 repairs (PRE_DECLARATIONS.md sec.3, binding):
  R1  kappa bounded in COMPLETION UNITS with the survival allowance explicit and in ONE
      register: e(s) = m * a_upper(s) * surv_upper(s) <= kappa * comp_uis_lower(s-3).
      Enforced object == audited object. (D134(1))
  R2  declared projection order O1..O5 + propagation ledger + one-way order audit; the
      only within-year cross-level carry-forward (tertiary tier composition) now reads the
      ENTRY cohort (t-DVEC[2]) instead of the same-year upper choice shares. (D134(2))
  R3  the guard is a COUNTERFACTUAL IDENTITY (A01D's upper admission vector injected into
      A00 accounting must reproduce A01D cell-for-cell) + two exact checks. No whole-panel
      identity guard. (D134(3))
  R4  Tier O quality acts at the RETURN/TAKE-UP margin (q_O on v_O in U_O), ONE discount,
      no tier survival penalty (surv_pen = 1.000, declared separately, own sensitivity);
      the (b) family of level bars is retired. (D134(3))
  R5  child-wage +10% scored in A10 (kappa OFF) on upper completion with the sign derived
      before the run; the capped arm tests the PRE-CAP object. (D134(2))
  R6  kappa is WINDOW-ONLY: dropped from the projection; A01D is a diagnostic, never a
      projection and never scored. (D138)
  R8  phys_cap sensitivity reported; the floor is conditional on the declared 1.15. (D139)
  R7  lower target in both registers (80.76 internal / 80.896 observed), both channels
      together, m=1.10 frozen, scored on 2021, survival ceiling and clip boundaries
      declared. (D140)

Determinism: one numpy PCG64 stream, seed 20261120, the frozen v1.2 draw order, no
wall-clock, no hostname, floats written at %.10g. Two clean runs are byte-identical.

REFUSES TO RUN if PRE_DECLARATIONS.md no longer matches the sha256 embedded at build time,
if the declared parameter block in it differs from the code, or if PARAMS.md is missing.

Usage:  python code/run_v16.py [--out DIR] [--no-determinism]
"""'''

I1 = r'''
# ======================================================================================
# 1b. V16-REPAIR -- DECLARED SWITCHES, PARAMETERS AND TIER HELPERS
#     (PRE_DECLARATIONS.md sec.3-5; one boolean read per insertion point)
# ======================================================================================
EXPECTED_PREDECL_V16 = "@@PREDECL_SHA@@"      # embedded at build time; mismatch refuses
EXPECTED_V13_PANEL_SHA = "47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3"
EXPECTED_BASE_SHA = "70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877"
KAPPA_V16 = 0.949          # K01, PHL observed median, DIAGNOSTIC ONLY (D138)
KAPPA_LAG_V16 = 3          # K03
CHILD_WAGE_MULT = 1.10     # R5a

TIER16 = dict(
    h_share=(0.15, 0.28, 0.40, 0.50),      # T01 Tier H share of adequate places
    q_H_mult=1.0, q_O_mult=1.0,            # R4c: NO tier survival multiplier (repair)
    cost_H_mult=1.60,                      # T06
    cost_O_mult=0.03,                      # T07
    q_O=0.55,                              # T05, now at the RETURN/TAKE-UP margin (R4a)
    v_tier_scale=None,                     # T10 RETIRED (R4b: one discount, one place)
    surv_pen_H=1.0, surv_pen_O=1.0,        # R4c declared: no retained survival penalty
    H_h=20.0,                              # T14
    a_gate=0.40,                           # T12
    risk_pen=0.20,                         # T13
    sigma_tier=0.80,                       # S03
    z_q=(-1.2816, -0.5244, 0.0, 0.5244, 1.2816),   # S02
    ability_grid=(0.25, 0.50, 0.75),       # S04
    cell_weight=((0.10, 0.07, 0.03),       # S01 joint weights, quintile x ability
                 (0.08, 0.08, 0.04),
                 (0.06, 0.09, 0.05),
                 (0.04, 0.09, 0.07),
                 (0.02, 0.07, 0.11)),
    cred_prem_H=0.18, cred_prem_O=0.03,    # T08/T09 (wage objects, not the choice block)
    rank_w_income=0.30,                    # S06
    rank_w_ability=0.70,                   # S06
    padv_clip=(0.01, 0.999),               # S08
)

# v1.5-faithful RECONSTRUCTION settings (arm A11V15, diagnostic only, never scored):
# v_O = 0.45 v_H (T10), Q_H = 1.25 Q and Q_O = 0.55 Q feeding PER-TIER SURVIVAL (T04/T05),
# the duplicated demand object (A_H + A_O_cand) and the same-year tertiary carry-forward.
V15_RECON = dict(v_O_scale=0.45, q_H_mult=1.25, q_O_mult=0.55,
                 dup_demand=True, same_year_ter=True)

DECLARED_GATES = dict(
    n_cells=33, min_cells=17, tol_pp=5.0, crossing_tol_y=5,
    obs_bar=dict(n_cells=33, min_cells=17, tol_pp=5.0),
    crossing_thresholds_pp=dict(primary=90.0, lower_secondary=90.0, upper_secondary=90.0),
)


def _util16(c):
    """The frozen childworld utility form (unchanged)."""
    x = c - 0.6 * NEED
    if x > 0.05:
        return math.log(max(x, 1e-9))
    return math.log(0.05) + (x - 0.05) / 0.05


def outside_utilities16(cp, level, y):
    """The frozen four-state block's UTILITIES at income y (not its shares)."""
    earn = 0.32 * AGE_W[level] * max(cp["w_child"] / 0.32, 0.55 * cp["farm"])
    cost = cp["cost"] * P["cost_base"][level]
    v_l = cp["v0"] * cp["decay"] ** level + 0.25 * ABILITY - 1.3 * min(OUT_YEARS, 3) / 3.0
    U_school = _util16(y - cost) + v_l
    U_both = (_util16(y - cost + 0.5 * (1.0 + cp["compat"]) * earn)
              + v_l * (0.72 + 0.2 * cp["compat"]) + 0.4 * cp["compat"] - 0.25)
    U_work = _util16(y + earn) - 0.2 * TASTE
    U_neither = _util16(y) + cp["neither"] + cp["girl_care"] * GIRL_SHARE
    return U_school, U_both, U_work, U_neither


def wage_gap16(rf1, Y, lit, Tcur):
    """G_H = ln(w_for[rung2]/w_inf), the model's own formal-informal log-wage gap (T15)."""
    psi = (P["psi_pre"], P["psi_ind"], P["psi_div"])[int(Tcur)]
    w_for = (Y / 1000.0) * P["rung_mult"][1] * (1.0 + P["cred_prem"] * 1) * float(rf1)
    w_inf = (Y / 1000.0) * (1.0 + psi * lit)
    return math.log(max(w_for, 1e-12) / max(w_inf, 1e-12))


def tier_cells(cp, level, y_shock, tc, padv_hat, G_H):
    """The declared 15-cell (5 income x 3 ability) utility comparison for one cell.

    U_H,i = util(y_i - cost_H) + v_H + H_h*p_hat*G_H*1[a_i >= a_gate] - risk_pen*(1-p_hat)
    U_O,i = util(y_i - cost_O) + q_O * v_H            <-- R4a: quality at the RETURN margin
    outside refusal value = max(U_work, U_neither)    (declared: U_both is a SCHOOL state;
                                                        the count it would have dominated is
                                                        reported, not dropped)
    Ties go to the outside option (declared: never a silent H).
    """
    zq = tc["z_q"]
    cw = tc["cell_weight"]
    ab = tc["ability_grid"]
    cb = P["cost_base"][min(level, 2)]
    cost_H = tc["cost_H_mult"] * cp["cost"] * cb
    cost_O = tc["cost_O_mult"] * cp["cost"] * cb
    v_H = cp["v0"] * (cp["decay"] ** level)
    _vs = tc.get("v_O_scale")
    v_O = (tc["q_O"] if _vs is None else float(_vs)) * v_H
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
        _, Ub, Uw, Un = outside_utilities16(cp, level, yi)
        uo = max(Uw, Un)
        for ai in range(3):
            av = ab[ai]
            ww = cw[qi][ai]
            if tc.get("sorting_off"):
                ww = 1.0 / 15.0
            uh = _util16(yi - cost_H) + v_H + (hterm if av >= tc["a_gate"] else 0.0) - risk
            u0 = _util16(yi - cost_O) + v_O
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
    """Admission at the two tiers plus the declared SECOND decision (accept O or exit).

    Rank admission: rank_score = 0.30*(y_i/ybar) + 0.70*a_i, deterministic tie-break.
    Unfilled Tier O places V_O = K_O - T_O are a PRIMARY object and are never reallocated.
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


# --------------------------------------------------------------------------------------
# Predeclaration integrity (G6): the file's sha256 was embedded at build time; its declared
# JSON block must equal these parameters. Any mismatch REFUSES to run.
# --------------------------------------------------------------------------------------
def declared_block(path=None):
    p = Path(path) if path else (ROOT / "PRE_DECLARATIONS.md")
    txt = p.read_text()
    i = txt.index("```json\n")
    j = txt.index("\n```", i)
    return json.loads(txt[i + len("```json\n"):j])


def verify_predecl(path=None, expected_sha=None):
    p = Path(path) if path else (ROOT / "PRE_DECLARATIONS.md")
    exp = EXPECTED_PREDECL_V16 if expected_sha is None else expected_sha
    got = sha256_file(p)
    if got != exp:
        raise SystemExit("REFUSING: PRE_DECLARATIONS.md sha256 %s != frozen %s" % (got, exp))
    d = declared_block(p)
    checks = {
        "seed": (int(d["seed"]), SEED),
        "base_code_sha256": (d["base_code_sha256"], EXPECTED_BASE_SHA),
        "v13_panel_sha256": (d["v13_panel_sha256"], EXPECTED_V13_PANEL_SHA),
        "measurement_factor": (float(d["measurement_factor"]), float(P["meas_completion_factor"])),
        "kappa_diagnostic": (float(d["kappa_diagnostic"]), float(KAPPA_V16)),
        "kappa_lag": (int(d["kappa_lag"]), int(KAPPA_LAG_V16)),
        "h_share": (list(d["h_share"]), list(TIER16["h_share"])),
        "cost_H_mult": (float(d["cost_H_mult"]), float(TIER16["cost_H_mult"])),
        "cost_O_mult": (float(d["cost_O_mult"]), float(TIER16["cost_O_mult"])),
        "q_O_return": (float(d["q_O_return"]), float(TIER16["q_O"])),
        "v_tier_scale": (d["v_tier_scale"], TIER16["v_tier_scale"]),
        "surv_pen_O": (float(d["surv_pen_O"]), float(TIER16["surv_pen_O"])),
        "surv_pen_H": (float(d["surv_pen_H"]), float(TIER16["surv_pen_H"])),
        "H_h": (float(d["H_h"]), float(TIER16["H_h"])),
        "a_gate": (float(d["a_gate"]), float(TIER16["a_gate"])),
        "risk_pen": (float(d["risk_pen"]), float(TIER16["risk_pen"])),
        "sigma_tier": (float(d["sigma_tier"]), float(TIER16["sigma_tier"])),
        "ability_grid": ([float(x) for x in d["ability_grid"]],
                         [float(x) for x in TIER16["ability_grid"]]),
        "cell_weight": ([[float(x) for x in r] for r in d["cell_weight"]],
                        [[float(x) for x in r] for r in TIER16["cell_weight"]]),
        "rank_w_income": (float(d["rank_w_income"]), float(TIER16["rank_w_income"])),
        "rank_w_ability": (float(d["rank_w_ability"]), float(TIER16["rank_w_ability"])),
        "padv_clip": ([float(x) for x in d["padv_clip"]],
                      [float(x) for x in TIER16["padv_clip"]]),
        "obs_bar": (dict(d["obs_bar"]), dict(DECLARED_GATES["obs_bar"])),
        "crossing_tol_y": (int(d["crossing_tol_y"]), int(DECLARED_GATES["crossing_tol_y"])),
        "crossing_thresholds_pp": ({k: float(v) for k, v in d["crossing_thresholds_pp"].items()},
                                   {k: float(v) for k, v in
                                    DECLARED_GATES["crossing_thresholds_pp"].items()}),
        "child_wage_mult": (float(d["child_wage_mult"]), float(CHILD_WAGE_MULT)),
    }
    bad = {k: v for k, v in checks.items() if v[0] != v[1]}
    if bad:
        raise SystemExit("REFUSING: declared block != code parameters: %r" % (bad,))
    return dict(sha256=got, declared=d, n_checked=len(checks))


# --------------------------------------------------------------------------------------
# Arm runner (v1.6): the frozen v1.2 draw order + the declared V16 switches. No new draws.
# --------------------------------------------------------------------------------------
def run_arm(seed=SEED, bimodal=False, kappa_link=False, tier_surv=False, tier_cfg=None,
            inject_upper=None, kappa=KAPPA_V16, w_child_mult=1.0, phys_cap=None,
            shadow=True, hosts=None, inputs=None):
    """One arm over the 30 synthetic countries, draws identical to the frozen v1.3 run."""
    if phys_cap is not None:
        P["phys_cap"] = float(phys_cap)
    inputs = shadow_inputs_named() if inputs is None else inputs
    S_phl, P_phl, _coh, _ptr, _spend = load_observed_phl_paths()
    rng = np.random.default_rng(seed)
    cps = apply_declared(draw_countries(rng))
    gnoise = rng.normal(0.0, P["g_noise_sd"], (T, N_C))
    hhnoise = rng.normal(0.0, P["hh_noise_sd"], (T, N_C))
    for j in (2,):
        gnoise[:, j] = gnoise[:, 1]; hhnoise[:, j] = hhnoise[:, 1]
    for j in (11, 12):
        gnoise[:, j] = gnoise[:, 10]; hhnoise[:, j] = hhnoise[:, 10]
    if w_child_mult != 1.0:
        cps = [dict(c, w_child=c["w_child"] * w_child_mult) for c in cps]
    by_host = {}
    if shadow and hosts:
        for tname, hname in hosts.items():
            by_host[hname] = tname
    results = []
    for i, cp in enumerate(cps):
        Sp = cohort_path(cp, S_phl)
        Pp = pop_path(cp, P_phl)
        sh_in = None
        if cp["name"] in by_host:
            tname = by_host[cp["name"]]
            sh_in = dict(inputs[tname], type=tname)
        results.append(simulate_country(cp, gnoise[:, i], hhnoise[:, i], Sp, Pp,
                                        sh_in=sh_in, beh=SHADOW_BEHAV,
                                        bimodal=bimodal, kappa_link=kappa_link,
                                        tier_surv=tier_surv, tier_cfg=tier_cfg,
                                        inject_upper=inject_upper, kappa=kappa))
    return results


def run_arm_full(**kw):
    """Two passes, exactly the frozen v1.3 procedure: shadow-BLIND hosts, then the run."""
    off = run_arm(shadow=False, **kw)
    hosts, _gdp = resolve_hosts(off)
    res = run_arm(shadow=True, hosts=hosts, **kw)
    return res, hosts
'''

I2 = r'''def simulate_country(cp, gnoise, hhnoise, S_path, Pop_path, sh_in=None, beh=None,
                    bimodal=False, kappa_link=False, tier_surv=False, tier_cfg=None,
                    inject_upper=None, kappa=KAPPA_V16):
    """Frozen v1.3 arithmetic, plus the declared V16 switches (identity when all OFF).

    bimodal      : the A5 two-tier block (I2-I4). OFF -> the frozen single gate.
    kappa_link   : the completion-unit kappa constraint (I6). DIAGNOSTIC ONLY (D138).
    tier_surv    : per-tier survival mapping (v1.5 defect; used only by the reconstruction
                   arm A11V15 and by the declared retained-penalty sensitivity).
    inject_upper : counterfactual replay (R3): the upper official-age admission rate vector.
    """'''

I3 = r'''
    # ---- V16 stores (filled only when a block is ON; harmless when OFF) -----------------
    out.update(dict(
        tier_K_H=np.zeros((NL, T)), tier_K_O=np.zeros((NL, T)),
        tier_A_H=np.zeros((NL, T)), tier_A_O=np.zeros((NL, T)),
        tier_A_O_first=np.zeros((NL, T)), tier_T_O=np.zeros((NL, T)),
        tier_V_O=np.zeros((NL, T)), tier_unf=np.zeros((NL, T)), tier_take=np.zeros((NL, T)),
        tier_adm_H=np.zeros((NL, T)), tier_queue_H=np.zeros((NL, T)),
        tier_ratio_H=np.zeros((NL, T)), tier_padv=np.ones((NL, T)),
        tier_Q_H=np.zeros((NL, T)), tier_Q_O=np.zeros((NL, T)),
        tier_surv_H=np.zeros((NL, T)), tier_surv_O=np.zeros((NL, T)),
        tier_wage_H=np.zeros((NL, T)), tier_wage_O=np.zeros((NL, T)),
        n_both_dom=np.zeros((NL, T)),
        kappa_bound_pp=np.zeros(T), kappa_binds=np.zeros(T), kappa_cut_pp=np.zeros(T),
        kappa_slack_pp=np.zeros(T),
        adm_in_C=np.zeros((NL, T)), adm_in_seats=np.zeros((NL, T)),
        adm_in_Doff=np.zeros((NL, T)), adm_in_phys=np.zeros((NL, T)),
    ))
    admH_hist = np.zeros((NL, T + OFF)); TO_hist = np.zeros((NL, T + OFF))
    admH_p_hist = np.zeros((NL, T + OFF)); TO_p_hist = np.zeros((NL, T + OFF))
    for _L in range(NL):
        for _k in range(OFF):
            admH_hist[_L, _k] = tc["h_share"][_L] * P["init_comp"][_L]
            TO_hist[_L, _k] = (1.0 - tc["h_share"][_L]) * P["init_comp"][_L]
            admH_p_hist[_L, _k] = admH_hist[_L, _k] * C[_L, 0]
            TO_p_hist[_L, _k] = TO_hist[_L, _k] * C[_L, 0]
    ter_hist = [None] * (T + OFF)
    for _k in range(T + OFF):
        ter_hist[_k] = (tc["h_share"][2], 1.0 - tc["h_share"][2],
                        tc["h_share"][2], 1.0 - tc["h_share"][2])
    padv_hat = np.ones(NL)      # S07 one-year expectation lag; no history at t=0
    GH_hat = wage_gap16(1.0, Y, lit, Tcur)
'''

I4 = r'''
            # @@V16_TIER_BEGIN@@
            # ---- I2-I4: declared two-tier allocation (identity when bimodal is FALSE) ----
            if bimodal:
                K_H_L = tc["h_share"][L] * seats[L]
                K_O_L = seats[L] - K_H_L
                Q_H_L = tc["q_H_mult"] * float(Qq[L])
                Q_O_L = tc["q_O_mult"] * float(Qq[L])
                if L < 3:
                    cells = tier_cells(cp, L, hhnoise[t], tc, padv_hat[L], GH_hat)
                    al = tier_allocate(cells, elig, C[L, t], K_H_L, K_O_L, tc)
                    A_H_L = al["A_H"]; A_O_L = al["A_O_first"]; A_O_cand = al["A_O_cand"]
                    admitted_H = al["admitted_H"]; T_O_L = al["T_O"]
                    mW = al["mW"]; mB = al["mB"]; mN = al["mN"]
                    n_both_dom = cells["n_both"]
                else:
                    _del = 0 if tc.get("same_year_ter") else int(round(DVEC[2]))
                    _th = ter_hist[OFF + t - _del]
                    if tc.get("same_year_ter"):
                        _sH2, _sO2 = _th[2], _th[3]
                    else:
                        _sH2, _sO2 = _th[0], _th[1]
                    mW = mB = mN = 0.0
                    A_H_L = _sH2 * elig * C[L, t]
                    A_O_L = _sO2 * elig * C[L, t]
                    A_O_cand = A_O_L
                    admitted_H = min(A_H_L, K_H_L)
                    T_O_L = min(A_O_L, K_O_L)
                    n_both_dom = 0
                V_O_L = max(0.0, K_O_L - T_O_L)
                queue_H_L = max(0.0, A_H_L - admitted_H)
                p_adv_L = clip(admitted_H / max(A_H_L, 1e-9),
                               tc["padv_clip"][0], tc["padv_clip"][1])
                # V16 FIX D-2: demand_official is the UNDUPLICATED applicant object
                # (A_H + A_O_first); v1.5 reported A_H + A_O_cand, double-counting the
                # refused Tier H applicants who accept Tier O. Declared in TUNE_LOG C3.
                D_off = A_H_L + (A_O_cand if tc.get("dup_demand") else A_O_L)
                adm_off = admitted_H + T_O_L
                adm_oa = min(D_oa, max(0.0, phys - adm_off))
                admitted = adm_off + adm_oa
                _ecL = max(elig * C[L, t], 1e-9)
                p_s = (A_H_L + A_O_L) / _ecL
                p_b = mB; p_w = mW; p_n = mN
                ds = p_s + p_b
                out["p_school"][L, t] = p_s
                out["p_both"][L, t] = p_b
                out["p_work"][L, t] = p_w
                out["p_neither"][L, t] = p_n
                out["demand_share"][L, t] = ds
                out["demand_off"][L, t] = D_off
                out["demand_oa"][L, t] = D_oa
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
                out["tier_ratio_H"][L, t] = ((A_H_L / K_H_L) if K_H_L > 1e-12
                                             else float("inf"))
                out["tier_padv"][L, t] = p_adv_L
                out["tier_Q_H"][L, t] = Q_H_L
                out["tier_Q_O"][L, t] = Q_O_L
                out["n_both_dom"][L, t] = float(n_both_dom)
                admH_hist[L, OFF + t] = admitted_H / max(C[L, t], 1e-9)
                TO_hist[L, OFF + t] = T_O_L / max(C[L, t], 1e-9)
                admH_p_hist[L, OFF + t] = admitted_H
                TO_p_hist[L, OFF + t] = T_O_L
                if L == 2:
                    _e2 = max(elig * C[L, t], 1e-9)
                    ter_hist[OFF + t] = (admitted_H / _e2, T_O_L / _e2,
                                         A_H_L / _e2, A_O_cand / _e2)
            # @@V16_TIER_END@@

            # @@V16_KAPPA_BEGIN@@
            # ---- I6: the kappa constraint in COMPLETION UNITS, ONE register (R1) --------
            # Enforced object:  e(s) = m * a_upper(s) * surv_upper(s)  <=  kappa*comp_lower(s-3)
            # Enforced == audited: the audit recomputes e(s) from the panel, same m, same surv.
            out["adm_in_C"][L, t] = float(C[L, t])
            out["adm_in_seats"][L, t] = float(seats[L])
            out["adm_in_Doff"][L, t] = float(D_off)
            out["adm_in_phys"][L, t] = float(phys)
            if kappa_link and L == 2 and t >= KAPPA_LAG_V16:
                _m = float(P["meas_completion_factor"])
                _surv_u = clip(P["surv_max"][2] * float(Qq[2]) ** P["surv_theta"][2],
                               0.02, 0.995)
                _lower = float(out["comp_uis"][1, t - KAPPA_LAG_V16])
                _bound_e = float(kappa) * _lower
                _cap_rate = clip(_bound_e / max(_m * _surv_u, 1e-12), 0.0, 1.0)
                out["kappa_bound_pp"][t] = 100.0 * _bound_e
                out["kappa_slack_pp"][t] = 100.0 * (_m * _cap_rate * _surv_u - _bound_e)
                _cap_abs = _cap_rate * float(C[2, t])
                if adm_off > _cap_abs + 1e-12:
                    out["kappa_binds"][t] = 1.0
                    out["kappa_cut_pp"][t] = 100.0 * (adm_off - _cap_abs) / max(C[2, t], 1e-9)
                    adm_off = _cap_abs
                    admitted = adm_off + adm_oa
            if inject_upper is not None and L == 2:
                # R3 counterfactual replay: the ONLY input is A01D's upper admission rate,
                # PER COUNTRY (a dict keyed by country name).
                _inj = (inject_upper.get(cp["name"]) if isinstance(inject_upper, dict)
                        else inject_upper)
                if _inj is not None:
                    # the vector is a COUNTS vector (the A01D admitted_official column), so
                    # the replay is bit-exact: no rate->count round-trip is performed.
                    adm_off = float(_inj[t])
                    admitted = adm_off + adm_oa
            # @@V16_KAPPA_END@@
'''

I5 = r'''
            # @@V16_SURV_BEGIN@@
            out["tier_surv_H"][L, t] = float(surv)
            out["tier_surv_O"][L, t] = float(surv)
            if tier_surv:
                # Per-tier survival (the v1.5 defect). Used ONLY by the reconstruction arm
                # A11V15 and by the declared retained-penalty sensitivity R4c.
                _spH = float(tc["surv_pen_H"]); _spO = float(tc["surv_pen_O"])
                _QH = Q_H_L if bimodal else float(Qq[L])
                _QO = Q_O_L if bimodal else float(Qq[L])
                surv_H_t = clip(P["surv_max"][L] * _QH ** P["surv_theta"][L] * _spH,
                                0.02, 0.995)
                surv_O_t = clip(P["surv_max"][L] * _QO ** P["surv_theta"][L] * _spO,
                                0.02, 0.995)
                _durS = int(round(DVEC[L]))
                _aH_s = admH_hist[L, OFF + t - _durS]
                _aO_s = TO_hist[L, OFF + t - _durS]
                _pH_s = admH_p_hist[L, OFF + t - _durS]
                _pO_s = TO_p_hist[L, OFF + t - _durS]
                comp_coh = clip(_aH_s * surv_H_t + _aO_s * surv_O_t, 0.0, 1.0)
                gr = _pH_s * surv_H_t + _pO_s * surv_O_t
                _tot = _pH_s + _pO_s
                surv = (((_pH_s * surv_H_t + _pO_s * surv_O_t) / _tot)
                        if _tot > 1e-12 else surv_H_t)
                out["tier_surv_H"][L, t] = float(surv_H_t)
                out["tier_surv_O"][L, t] = float(surv_O_t)
            # @@V16_SURV_END@@
'''

I7 = r'''
        # ---- V16 I7: expectation state for the next year's tier choice (one-year lag) ---
        if bimodal:
            padv_hat = out["tier_padv"][:, t].copy()
            _Yv = out["Y"][t]
            for _L in range(NL):
                out["tier_wage_H"][_L, t] = ((_Yv / 1000.0) * P["rung_mult"][_L]
                                             * (1.0 + tc["cred_prem_H"] * _L) * float(rf[_L]))
                out["tier_wage_O"][_L, t] = ((_Yv / 1000.0) * P["rung_mult"][_L]
                                             * (1.0 + tc["cred_prem_O"] * _L) * float(rf[_L]))
        GH_hat = wage_gap16(float(rf[1]), out["Y"][t], out["lit"][t], Tcur)
'''

SETUP_ANCHOR = '''    gp = np.array(P["gp"])
    cap = cp["cap0"]
    beh = SHADOW_BEHAV if beh is None else beh
    ratio_prev = np.ones(5)          # v1.3: Pi/pi0 carried to the next year's pool (lag 1)
'''
SETUP_NEW = SETUP_ANCHOR + '''    tc = dict(TIER16)
    if tier_cfg:
        tc.update(tier_cfg)
'''

SIG_OLD = "def simulate_country(cp, gnoise, hhnoise, S_path, Pop_path, sh_in=None, beh=None):\n"
RAT_OLD = '''            phys = min(P["phys_cap"] * seats[L], P["overage_cap"] * C[L, t])
            adm_off = min(D_off, phys)
            adm_oa = min(D_oa, max(0.0, phys - adm_off))
            admitted = adm_off + adm_oa
'''
RAT_NEW = RAT_OLD + I4

GR_OLD = "            gr = adm_p_hist[L, OFF + t - int(round(DVEC[L]))] * surv\n"
GR_NEW = GR_OLD + I5

TAIL_ANCHOR = '''        X_prev = X
        xbase_prev = xbase
        Y *= (1.0 + g)
'''
TAIL_NEW = TAIL_ANCHOR + I7

HIST_ANCHOR = '''    for k in range(OFF):
        comp_hist[k] = P["init_comp"][0]
'''
HIST_NEW = HIST_ANCHOR + I3

MAIN_OLD = '''if __name__ == "__main__":
    main()
'''
MAIN_NEW = '''if __name__ == "__main__":
    raise SystemExit("sim_v1_6_repair.py is a module; run code/run_v16.py")
'''


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def splice(src, old, new, name, count=1):
    if src.count(old) != count:
        raise SystemExit("REFUSING: anchor %s occurs %d times (expected %d)"
                         % (name, src.count(old), count))
    return src.replace(old, new, count)


def main():
    base_sha = sha(BASE)
    if base_sha != BASE_SHA_EXPECTED:
        raise SystemExit("REFUSING: base_v1_3_sim.py sha256 mismatch: %s" % base_sha)
    pre_sha = sha(PREDECL)
    src = BASE.read_text()

    # I0 docstring
    i = src.index('"""SIM_V1_3')
    j = src.index('\n"""\n', i)
    src = src[:i] + DOCSTRING + "\n" + src[j + len('\n"""\n'):]

    # I1 parameters + helpers
    src = splice(src, "def sig(x):\n", I1.replace("@@PREDECL_SHA@@", pre_sha) + "\n\ndef sig(x):\n",
                 "I1 params")

    # I2 signature
    src = splice(src, SIG_OLD, I2 + "\n", "I2 signature")

    # setup: tier config
    src = splice(src, SETUP_ANCHOR, SETUP_NEW, "setup")

    # I3 stores
    src = splice(src, HIST_ANCHOR, HIST_NEW, "I3 stores")

    # I4 tier block + I6 kappa + injection
    src = splice(src, RAT_OLD, RAT_NEW, "I4 tier block")

    # I5 survival branch
    src = splice(src, GR_OLD, GR_NEW, "I5 surv block")

    # I7 expectation state
    src = splice(src, TAIL_ANCHOR, TAIL_NEW, "I7 expectation")

    # entry point
    src = splice(src, MAIN_OLD, MAIN_NEW, "entry point")

    OUT.write_text(src)
    print("wrote %s" % OUT)
    print("  lines        : %d" % len(src.splitlines()))
    print("  sha256       : %s" % sha(OUT))
    print("  base sha256  : %s" % base_sha)
    print("  predecl sha  : %s" % pre_sha)


if __name__ == "__main__":
    main()
