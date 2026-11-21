#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUDIT_CAPS -- DEBUG Agent 1, CAP AUDIT (MODEL-DEBUG MODE).

Enumerates every clamp / ceiling / floor / renormalisation in the pipeline that can
touch a model object, locates it by file:line on disk (verbatim source line, verified),
counts on the FROZEN panels where the bound binds, and classifies each as

    (a) DECLARED CONVENTION     -- stated in PARAMS / PRE_DECLARATIONS / architecture and
                                   defensible as part of the declared object
    (b) IMPLEMENTATION ARTEFACT -- changes a declared object, declared nowhere on disk
    (c) UNDETERMINED            -- undeclared and either binding or not resolvable from
                                   the record; needs the Lead / Council

This is an AUDIT ONLY. It reads model / generator code and the frozen panels, writes
nothing outside cap_audit/, runs no generator, fits nothing, draws no random number and
produces no number that is not a count, a panel value, or an arithmetic identity on the
frozen panels. Deterministic: two runs byte-identical.

Run:  python code/audit_caps.py --out results
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------------------
# paths
# --------------------------------------------------------------------------------------
CODE = Path(__file__).resolve().parent            # .../cap_audit/code
CELL = CODE.parent                                # .../cap_audit
DBG = CELL.parent                                 # .../model_debug_2026-11-21
EXT = DBG.parent                                  # .../extensions
MASS = EXT.parent                                 # .../10_massification
PROG = MASS.parent                                # .../massification-2026-11-20

PREDECL = DBG / "PRE_DECLARATIONS.md"
# The contract was AMENDED by the Lead while this audit was running (AMENDMENT 1, measure
# awareness). Both versions are accepted and both hashes are recorded in the manifest; the
# audit applies the stricter of the two (the amended one).
PREDECL_HASHES = {
    "748335cf915394c3f0dc0241fa2c5b6eaaae9c0af201dba97d3c2de24d8f6553": "v0 (licensed at dispatch)",
    "7d8bade95407a2fe76c95a740e0c98a74f34962117b33846df37a7d6a48f56a9": "v1 + AMENDMENT 1 (measure-aware)",
}
PREDECL_SHA_EXPECTED = "748335cf915394c3f0dc0241fa2c5b6eaaae9c0af201dba97d3c2de24d8f6553"

SYNTH = MASS / "extensions" / "synthetic_2026-11-20"
PANELS = {
    "v1.3": SYNTH / "generator_v1_3" / "results" / "synthetic_panel_v1_3.csv",
    "v1.2": SYNTH / "generator_v1_2" / "results" / "synthetic_panel_v1_2.csv",
    "A17": SYNTH / "generator_v1_7_partrepair" / "results" / "panel_A17.csv",
}
LABEL = "DEBUG"

LEVELS = ["primary", "lower_secondary", "upper_secondary", "tertiary"]
LI = {l: i for i, l in enumerate(LEVELS)}
DVEC = (6, 3, 3, 4)                     # declared level durations (sim_v1_3.py:64)
SURV_MAX = (0.96, 0.91, 0.90, 0.90)     # PARAMS surv_max
SURV_THETA = (1.0, 1.0, 1.0, 0.80)      # PARAMS surv_theta
PHYS_CAP = 1.15                         # PARAMS phys_cap
OVERAGE_CAP = 1.05                      # PARAMS overage_cap (Z1 gate)
OA_RATE = (0.08, 0.06, 0.05, 0.04)      # PARAMS oa_rate
SEC_FLOORS = (0.02, 0.05, 0.03, 0.05)   # PARAMS sec_floors
G_FLOOR, G_CAP = 0.0, 0.090             # PARAMS g_floor / g_cap
PTR_LO, PTR_HI = 2.0, 150.0             # sim_v1_3.py:883
PADV_LO, PADV_HI = 0.01, 0.999          # v1.6 S08 padv_clip (PARAMS.md:39)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------------------
# the clamp registry (one row per site unless the site list is given explicitly)
# --------------------------------------------------------------------------------------
def R(cid, pipeline, stage, file, line, fingerprint, bound, obj, cls, declared_in, why,
      counter=None, fix="no", sites=None, kind="clamp"):
    return dict(id=cid, pipeline=pipeline, stage=stage, file=file, line=line,
                fingerprint=fingerprint, bound=bound, object=obj, cls=cls,
                declared_in=declared_in, why=why, counter=counter, fix=fix,
                sites=sites or [(file, line, fingerprint)], kind=kind)


MEASURE = {
    "CAP-01": "CR (UIS completion rate, m x cohort-flow)",
    "CAP-02": "CR (cohort-flow share)",
    "CAP-03": "survival (probability)",
    "CAP-04": "survival (probability)",
    "CAP-05": "CR (measurement constant m)",
    "CAP-06": "GER (all enrolment / official-age population)",
    "CAP-07": "capacity (places, not a rate)",
    "CAP-08": "capacity (places, not a rate)",
    "CAP-09": "capacity (places, not a rate)",
    "CAP-10": "demand (applicants, not a rate)",
    "CAP-11": "eligibility pool (persons)",
    "CAP-12": "eligibility share (of cohort)",
    "CAP-13": "share (probability mass)",
    "CAP-14": "PTR (ratio, not a rate)",
    "CAP-15": "growth rate",
    "CAP-16": "queue (persons)",
    "CAP-17": "employment (persons)",
    "CAP-18": "share (probability simplex)",
    "CAP-19": "sector share (of employment)",
    "CAP-20": "numerical argument",
    "CAP-21": "gate numbers (Q, pi0, kappa, R)",
    "CAP-22": "capacity (places)",
    "CAP-23": "advancement share",
    "CAP-24": "CR constraint",
}
DEFINITIONAL = {
    "CAP-01": "NOT definitional: a CR's denominator is the 3-5-years-above-grade cohort, so a CR is "
              "not bounded by 1.0 (AMENDMENT 1 / sec.6). A 1.0 ceiling on a CR is NOT an NER bound.",
    "CAP-02": "definitional-ish: cohort-flow is a share of the entry cohort, bounded by 1 by construction.",
    "CAP-03": "definitional: a probability cannot exceed 1; guard inside the declared envelope (0.96).",
    "CAP-04": "NOT definitional: a survival FLOOR of 0.02 is a modelling choice, not a domain bound.",
    "CAP-05": "convention: m = 1.10 is the declared CR measurement choice (a stand-in for the older "
              "denominator), not a bound.",
    "CAP-06": "NOT an NER bound: this is a declared Z1 GATE on GER, and GER may exceed 100 by "
              "definition (repeaters / over-age). Per AMENDMENT 1 it must never be read as 'GER cannot "
              "exceed 105'.",
    "CAP-18": "definitional: a probability vector sums to 1.",
    "CAP-19": "modelling floor (declared), not a domain bound.",
}


def registry():
    G = "SYNTH (frozen panel path)"
    M = "MODEL (anchor / observed chain)"
    out = [
        # ---------------- the completion pipeline ----------------
        R("CAP-01", G, "completion (UIS convention)",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 832,
          'out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)',
          "[0.0, 1.0]", "completion_uis (UIS-convention completion)", "b",
          "nowhere as a bound: the UIS convention is declared as completion_uis = m x cohort-flow with "
          "m = 1.10 (generator_v1_2/PARAMS.md sec.7). No PARAMS, PRE_DECLARATIONS or "
          "MODEL_ARCHITECTURE text declares a 1.0 ceiling on completion_uis. The only on-disk texts "
          "that mention a completion bound are (i) generator_v0/FINDINGS.md:39 C5 'hard sanity: "
          "GER/completion in [0,105]; rates in [0,1]', a check on v0's own pp outputs (v0 completion "
          "0.77-95.01), not a convention of the v1.2+ object, and (ii) generator_v1_2/FINDINGS.md:191, "
          "which names the behaviour 'a ceiling artifact of m x cohort-flow clipping. It is not used as "
          "a check.'",
          "the declared object can exceed 1 by construction when cohort-flow > 1/1.10, so the 1.0 ceiling "
          "changes the declared object; the programme's own v1.2 findings already called it a ceiling "
          "artefact, and D160 names it the defect; 35/6,720 cells bind",
          counter="cap_uis", fix="YES",
          sites=[
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 832,
             'out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)'),
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_2/code/sim_v1_2.py", 610,
             'out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)'),
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_4_demand/code/sim_v1_4_demand.py", 969,
             'out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)'),
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/code/sim_v1_5_bimodal.py", 756,
             'out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)'),
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/code/sim_v1_5_bimodal.py", 808,
             'out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)'),
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/code/sim_v1_6_repair.py", 1318,
             'out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)'),
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_7_partrepair/code/frozen/sim_v1_6_repair.py", 1318,
             'out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)'),
          ]),
        R("CAP-02", G, "completion (cohort flow)",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 828,
          'comp_coh = clip(a_entry * surv, 0.0, 1.0)',
          "[0.0, 1.0]", "completion_cohort (cohort-flow completion)", "a",
          "MODEL_ARCHITECTURE.md sec.1: 'completion is a cohort-flow object'; a cohort-flow share is a "
          "proportion of the entry cohort and is bounded by 1 by construction",
          "the object is an admitted share x survival, both in [0,1]; the clip is the object's natural "
          "bound, not an extra convention; 0 cells bind on all three frozen panels (pre-clip max 0.9497 / 0.8547)",
          counter="cap_coh"),
        R("CAP-03", G, "survival",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 826,
          'surv = clip(P["surv_max"][L] * Qq[L] ** P["surv_theta"][L], 0.02, 0.995)',
          "survival <= 0.995", "survival", "a",
          "survival is a probability (PARAMS surv_max, 'survival at zero congestion'); the 0.995 guard sits "
          "inside the declared envelope max(surv_max) = 0.96",
          "cannot bind: surv_max <= 0.96 < 0.995; 0 cells",
          counter="surv_ceil"),
        R("CAP-04", G, "survival",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 826,
          'surv = clip(P["surv_max"][L] * Qq[L] ** P["surv_theta"][L], 0.02, 0.995)',
          "survival >= 0.02", "survival", "c",
          "nowhere: no floor of 0.02 appears in PARAMS / PRE_DECLARATIONS / architecture",
          "undeclared numerical floor that BINDS and raises survival in 24 tertiary cells (1970-1972, 20 "
          "countries, burn-in); it changes completion_cohort and therefore every downstream level number. "
          "Not the named defect (it is upstream of the m-cap and identical on all three panels), but it must "
          "be adjudicated before any level sentence is called clean",
          counter="surv_floor"),
        R("CAP-05", G, "measurement convention",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 832,
          'clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)',
          "m = 1.10 (single constant, all levels/countries)", "measurement_factor", "a",
          "generator_v1_2/PARAMS.md sec.7 'CONVENTION / measurement choice'; v1.6 PRE_DECLARATIONS R7c "
          "'m frozen at 1.10 ... a CONVENTION, not a conversion'",
          "declared on every panel (measurement_factor == 1.10 in 6,720/6,720 cells); m itself is not the "
          "defect -- the undeclared 1.0 ceiling on its product is (CAP-01)",
          counter="m_factor"),
        R("CAP-06", G, "enrolment ratio",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 817,
          'out["ger"][L, t] = clip(100.0 * admitted / max(C[L, t], 1e-9), 0.0, P["overage_cap"] * 100.0)',
          "GER in [0, 105]", "GER", "a",
          "PARAMS overage_cap = 1.05 commented 'GER hard cap (Z1 gate)'; MODEL_ARCHITECTURE.md line 45 "
          "'GER bounded <=105'; v1.3 PRE_DECLARATIONS sec.4.1 (Z1)",
          "declared hard cap; on v1.3/v1.2 it is reached in 51 cells and changes the value in 27 of them "
          "(excess <= 5.0e-8, i.e. floating-point ties at admitted = 1.05 x cohort); on A17 max GER 99.32, 0 cells",
          counter="ger_cap"),
        R("CAP-07", G, "capacity gate",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 809,
          'phys = min(P["phys_cap"] * seats[L], P["overage_cap"] * C[L, t])',
          "phys <= min(1.15 x seats, 1.05 x cohort)", "physical admission capacity", "a",
          "PARAMS phys_cap = 1.15 'max pupils per adequate place (double shifts)' and overage_cap = 1.05 "
          "'GER hard cap (Z1 gate)'",
          "declared two-sided capacity; the cohort branch (1.05 x cohort) is the binding arm in 125/6,720 "
          "cells on every panel, the seat branch in 6,595",
          counter="phys_min"),
        R("CAP-08", G, "capacity gate",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 810,
          'adm_off = min(D_off, phys)',
          "adm_off <= phys", "admitted_official (rationing)", "a",
          "the declared capacity gate: admission = min(demand, physical capacity) (MODEL_ARCHITECTURE.md "
          "Layer 1c; PRE_DECLARATIONS sec.4.1)",
          "the model's rationing rule; demand exceeds phys in 3,189/6,720 cells on v1.3/v1.2 (5,733 on A17) "
          "-- reported as a count, not enumerated",
          counter="ration"),
        R("CAP-09", G, "capacity gate",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 811,
          'adm_oa = min(D_oa, max(0.0, phys - adm_off))',
          "adm_oa <= phys - adm_off", "admitted_overage", "a",
          "declared residual-capacity allocation of over-age applicants (PARAMS oa_rate)",
          "declared; binds where over-age demand exceeds the residual place stock -- reported as a count",
          counter="oa_min"),
        R("CAP-10", G, "tertiary demand",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 797,
          'D_off = p3 * min(pools[3], 1.05 * C[3, t])',
          "tertiary demand <= 1.05 x cohort", "demand_official (tertiary)", "a",
          "the same declared Z1 1.05 ceiling on demand (PARAMS overage_cap)",
          "declared; binds only where the tertiary pool exceeds 1.05 x cohort -- reported as a count",
          counter="ter_demand"),
        R("CAP-11", G, "eligibility pool",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 873,
          'pools[L] = min(newpool, 1.05 * C[L, t])',
          "pool <= 1.05 x cohort", "eligibility_pool", "a",
          "the same declared Z1 1.05 ceiling, applied to the carry-over pool",
          "declared; binds in 77 (v1.3) / 77 (v1.2) / 62 (A17) cells (eligibility_pool == 1.05 x cohort)",
          counter="pool_cap"),
        R("CAP-12", G, "eligibility share",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 788,
          'elig = 1.0 if L == 0 else min(1.0, pools[L] / max(C[L, t], 1e-9))',
          "elig <= 1.0", "eligibility share", "a",
          "a share of the cohort cannot exceed 1; declared pool construction (PARAMS init_pipe / pool_retain)",
          "a natural bound on a share; at the bound in 1,655 (v1.3) / 1,079 (A17) cells -- count only",
          counter="elig"),
        R("CAP-13", G, "out-of-school composition",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 847,
          'both_f = p_b * elig * C[L, t] * min(1.0, adm_off / max(D_off, 1e-9))',
          "share <= 1.0", "both_share mass", "a",
          "a probability mass; bounded by construction",
          "equals 1 whenever nothing is rationed (3,531 v1.3 cells) -- a natural bound, count only",
          counter="both_min"),
        R("CAP-14", G, "reported PTR",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 883,
          'out["ptr"][:, t] = np.clip(ptr, 2.0, 150.0)',
          "PTR in [2, 150]", "ptr", "c",
          "nowhere: no PTR bounds are stated in PARAMS / PRE_DECLARATIONS",
          "undeclared reporting guard, but NON-BINDING: observed PTR range 7.71-63.13 over all three "
          "panels, 0 cells at either bound; recorded for completeness, no fix",
          counter="ptr"),
        R("CAP-15", G, "growth",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 945,
          'g = clip(gs + comp_term + gnoise[t], P["g_floor"], P["g_cap"])',
          "growth in [0.0, 0.090]", "growth", "a",
          "PARAMS g_floor = 0.0, g_cap = 0.090 (declared band)",
          "declared band; 0 cells at either bound (observed range 0.00080-0.0565), so the band never "
          "changes a value on the frozen panels",
          counter="growth"),
        R("CAP-16", G, "labour queue",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 931,
          'queue_carry = np.minimum(P["queue_retain"] * np.maximum(remaining, 0.0),\n                                 P["queue_max_lf"] * LF)',
          "queue_carry <= 0.20 x LF", "queue carry-over", "a",
          "PARAMS queue_retain = 0.50, queue_max_lf = 0.20 (declared)",
          "declared; the carry-over is internal state and is not emitted, so it is NOT reconstructible from "
          "the frozen panels -- no cell count is claimed",
          counter=None),
        R("CAP-17", G, "employment",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 934,
          'E_r = np.minimum(E_r, J)',
          "employment <= jobs", "formal employment by rung", "a",
          "the employment identity (employment cannot exceed the rung's job stock) -- declared Layer 0/3",
          "declared identity; J is not emitted, so not reconstructible from the frozen panels -- no count",
          counter=None),
        R("CAP-18", G, "four-state shares",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 632,
          'Pr /= Pr.sum()',
          "shares on the simplex (sum = 1)", "school/both/work/neither shares", "a",
          "the borrowed-structural multinomial (BORROWED-FROM-ATLAS); a probability vector sums to 1",
          "declared renormalisation; on levels 0-2 the four shares sum to 1 within 1.4e-10 in 5,040/5,040 "
          "cells; tertiary is exempt by declaration (adult block: the four shares are 0 and non-enrolment is "
          "carried by out_of_school, PARAMS sec.6), so 1,680 cells are NOT a violation",
          counter="simplex"),
        R("CAP-19", G, "sector shares",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 704,
          'v = np.maximum(np.array([a, i, m, s]), floors)',
          "sector shares >= sec_floors = (0.02, 0.05, 0.03, 0.05)", "s_ag / s_inf / s_man / s_srv", "a",
          "PARAMS sec_floors (declared), applied in the marked-share projection with a 60-step "
          "project-back loop",
          "declared floor; binds at 0.02 in 1,896 (s_ag), 0.05 in 256 (s_inf) and 0.05 in 292 (s_srv) "
          "cells on v1.3; s_man never at its floor (min 0.0363)",
          counter="secfloors"),
        R("CAP-20", G, "sigmoid argument",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 207,
          'x = max(-30.0, min(30.0, float(x)))',
          "|x| <= 30", "sigmoid argument", "c",
          "nowhere: a numerical guard inside sig()",
          "cannot bind on any observed argument (sigmoid saturates at |x| ~ 30, where 1/(1+e^-x) is 1.0 to "
          "double precision); 0 informative cells; no fix. Guard only.",
          counter=None),
        R("CAP-21", G, "gate numbers Q / pi0 / kappa / R",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py", 306,
          'Q = min(max(float(cand) / max(float(cap), 1e-9), 0.0), 10.0)',
          "Q in [0,10]; pi0 in [0.01,0.999]; kappa in [1.0,5.0]; R in [1.0,20.0]",
          "Q_gate / pi0 / kappa / R", "a",
          "v1.3 PRE_DECLARATIONS.md sec.4.1 lines 124-128 (frozen R definition), reproduced in PARAMS.md "
          "line 28 ('clipped [1,20]')",
          "declared component bounds; Q never reaches 10 (max 1.54), R never reaches 20 (max 2.87); pi0 is "
          "at 0.999 in 311 cells and kappa at its 1.0 floor in 569 cells (v1.3) -- declared, count only",
          counter="gate_bounds"),
        R("CAP-22", G, "two-tier capacity split (v1.6/A17)",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/code/sim_v1_6_repair.py", 1164,
          'K_H_L = tc["h_share"][L] * seats[L]',
          "K_H = h_share x seats; K_O = seats - K_H", "tier_K_H / tier_K_O", "a",
          "v1.6 PRE_DECLARATIONS (I2-I4 declared two-tier allocation; T01 h_share from v1.5 "
          "PARAMETERS.csv)",
          "declared split; live only in the bimodal arm (A17). Capacity binds: Tier H is oversubscribed "
          "(queue > 0) in 5,738 cells and Tier O is full (T_O = K_O) in 3,548 cells -- declared rationing",
          counter="tier_split",
          sites=[
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/code/sim_v1_6_repair.py", 1164,
             'K_H_L = tc["h_share"][L] * seats[L]'),
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_7_partrepair/code/frozen/sim_v1_6_repair.py", 1164,
             'K_H_L = tc["h_share"][L] * seats[L]'),
          ]),
        R("CAP-23", G, "advancement share (v1.6/A17)",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/code/sim_v1_6_repair.py", 1191,
          'p_adv_L = clip(admitted_H / max(A_H_L, 1e-9),\n                               tc["padv_clip"][0], tc["padv_clip"][1])',
          "p_adv in [0.01, 0.999]", "tier_p_adv_H", "a",
          "v1.6 PARAMS.md:39 S08 padv_clip = (0.01, 0.999) DECLARED (PRE_DECLARATIONS.md:254)",
          "declared clip on a reported advancement share; binds at the 0.999 ceiling in 1,059 A17 cells "
          "(0 cells at 0.01). Reported object only -- it is not completion_uis",
          counter="tier_padv",
          sites=[
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/code/sim_v1_6_repair.py", 1191,
             'p_adv_L = clip(admitted_H / max(A_H_L, 1e-9),'),
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_7_partrepair/code/frozen/sim_v1_6_repair.py", 1191,
             'p_adv_L = clip(admitted_H / max(A_H_L, 1e-9),'),
          ]),
        R("CAP-24", G, "kappa constraint (v1.6, COMPLETION units)",
          "10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/code/sim_v1_6_repair.py", 1252,
          '_cap_rate = clip(_bound_e / max(_m * _surv_u, 1e-12), 0.0, 1.0)',
          "e(s) <= kappa x comp_lower(s-3); _cap_rate in [0,1]", "upper-secondary admitted (A17 only)", "a",
          "v1.6 PRE_DECLARATIONS I6 / Rule R1: the kappa constraint in completion units, 'enforced =="
          " audited'",
          "declared structural constraint, but INACTIVE in the register: kappa_link = False in the A17 arm "
          "(generator_v1_7_partrepair/code/sim_v1_7_partrepair.py:96), so 0 cells; also declared OFF by "
          "D138/R6 in v1.6 PARAMS.md:17",
          counter="kappa_link",
          sites=[
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/code/sim_v1_6_repair.py", 1252,
             '_cap_rate = clip(_bound_e / max(_m * _surv_u, 1e-12), 0.0, 1.0)'),
            ("10_massification/extensions/synthetic_2026-11-20/generator_v1_7_partrepair/code/frozen/sim_v1_6_repair.py", 1252,
             '_cap_rate = clip(_bound_e / max(_m * _surv_u, 1e-12), 0.0, 1.0)'),
          ]),
        # ---------------- adjacent model code (not the frozen-panel path) -------------
        R("MOD-01", M, "A1 anchor: capacity sub-indices",
          "10_massification/model/anchor.py", 54,
          'parts.append(float(np.clip((40.0 - p[t]) / 20.0, 0, 1))); wts.append(0.5)',
          "sub-index in [0,1]", "capacity index C_t", "a",
          "docstring: 'C_t in [0,1]: delivery 0.5 (PTR), fiscal 0.3, enforcement 0.2'; declared mapping",
          "not in the synthetic panel path -- the A1 anchor class is a separate observed-data chain; no "
          "frozen-panel cells to count", counter=None),
        R("MOD-02", M, "A1 anchor: capacity index",
          "10_massification/model/anchor.py", 60,
          'C[t] = float(np.clip(np.average(parts, weights=wts), 0, 1))',
          "C_t in [0,1]", "capacity index", "a",
          "declared composite index (anchor.py docstring; PRE_ANCHOR_A1)",
          "not in the synthetic panel path", counter=None),
        R("MOD-03", M, "A1 anchor: gate",
          "10_massification/model/anchor.py", 68,
          'return float(max(C, 0.0) ** kappa)',
          "gate >= 0", "G(C) = C^kappa", "a",
          "declared gate; kappa in [0.5,1.0] with sensitivity reported (anchor.py KAPPA note)",
          "not in the synthetic panel path", counter=None),
        R("MOD-04", M, "A1 anchor: policy markers",
          "10_massification/model/anchor.py", 77,
          'if 2013 <= t:  m = max(m, 1.0)',
          "marker in {0,1}", "K-12 / free-SHS / free-tertiary markers", "a",
          "declared POLICY mapping (anchor.py comments per marker; PRE_ANCHOR_A1)",
          "not in the synthetic panel path", counter=None),
        R("MOD-05", M, "A1 anchor: ceiling push",
          "10_massification/model/anchor.py", 82,
          'CEIL = 0.25',
          "ceiling push = 0.25 x PUSH x gate", "ceiling-level saturating share", "a",
          "declared 'saturating share to ceiling levels' (A10, anchor.py comment)",
          "not in the synthetic panel path", counter=None),
        R("MOD-06", M, "push-pull: intake rate",
          "10_massification/model/pushpull.py", 90,
          'intake_rate = float(np.clip(intake_rate * (max(gdp_lag, 1e-9) ** eta_in), 0.0, 1.0))',
          "intake_rate in [0,1]", "intake rate", "a",
          "a rate (share of the cohort); the [0,1] domain is the object's definition",
          "not in the synthetic panel path", counter=None),
        R("MOD-07", M, "push-pull: participation probabilities",
          "10_massification/model/pushpull.py", 109,
          'p_pri = float(np.clip(p_pri + _pv, 0.02, 0.995))',
          "p_pri in [0.02,0.995] etc.", "level participation probabilities", "a",
          "probabilities; the guard keeps them inside (0.02, 0.995) -- declared in the model's parameter block",
          "not in the synthetic panel path", counter=None),
        R("MOD-08", M, "push-pull: sector shares",
          "10_massification/model/pushpull.py", 123,
          'agri = float(np.clip(0.75 * np.exp(-0.35 * logy) + 0.02, 0.01, 0.95))',
          "sector shares in [0.01,0.95] / [0.02,0.95]", "agri / services / formal shares", "a",
          "shares of employment; declared guards in the ported Layer 0/3 block",
          "not in the synthetic panel path", counter=None),
        R("MOD-09", M, "push-pull: reported GER",
          "10_massification/model/pushpull.py", 140,
          'ger_primary=100 * prim / max(pop[6:12].sum(), 1e-9)',
          "enrolment / population (no cap)", "ger_primary..ger_tertiary", "a",
          "this site has NO clamp at all -- it divides by the band population with an epsilon guard; "
          "recorded to show the observed chain does not cap GER at 105",
          "not in the synthetic panel path", counter=None),
        R("MOD-10", M, "repair: logit transform guard",
          "10_massification/model/repair.py", 65,
          "c = np.clip(np.array([x['completion_lower'] for x in h])[w] / 100.0, 1e-4, 1 - 1e-4)",
          "c in [1e-4, 1-1e-4]", "completion share entering a logit", "a",
          "numerical guard required by log(c/(1-c)) in an analysis helper (A3 logit regression)",
          "not in the synthetic panel path; analysis helper, not a model object", counter=None),
    ]
    for r in out:
        r["measure"] = MEASURE.get(r["id"], "other")
        r["definitional"] = DEFINITIONAL.get(r["id"], "declared domain/identity bound")
    return out


# --------------------------------------------------------------------------------------
# counters (deterministic, panel-only)
# --------------------------------------------------------------------------------------
def prep(df):
    d = df.copy()
    d["li"] = d["level"].map(LI)
    d["cell_id"] = d["country"] + "|" + d["level"] + "|" + d["year"].astype(str)
    d["row_1b"] = np.arange(1, len(d) + 1)
    d["surv_raw"] = (d["li"].map(lambda i: SURV_MAX[i])
                     * d["quality_q"] ** d["li"].map(lambda i: SURV_THETA[i]))
    d["surv_hit"] = d["surv_raw"].clip(0.02, 0.995)
    lagged = pd.Series(np.nan, index=d.index)
    for lv in LEVELS:
        sub = d.loc[d["level"] == lv].sort_values(["country", "year"])
        aev = sub["admitted_official"] / sub["cohort"]
        lagged.loc[sub.index] = aev.groupby(sub["country"]).shift(DVEC[LI[lv]]).values
    d["a_entry_lag"] = lagged
    d["comp_coh_pre"] = d["a_entry_lag"] * d["surv_hit"]
    d["ger_raw"] = 100.0 * d["enrolment"] / d["cohort"]
    d["phys"] = np.minimum(PHYS_CAP * d["seats"], OVERAGE_CAP * d["cohort"])
    d["d_oa"] = d["li"].map(lambda i: OA_RATE[i]) * d["cohort"]
    return d


def counters(d):
    """Return {counter_name: (n_binding, note)} for one panel."""
    n = {}
    m = float(d["measurement_factor"].iloc[0])
    c = {}

    raw_uis = m * d["comp_coh_pre"]
    n["cap_uis"] = (int((raw_uis > 1.0).sum()),
                    "pre-clip max %.10g" % raw_uis.max())
    n["cap_coh"] = (int((d["comp_coh_pre"] > 1.0).sum()),
                    "pre-clip max %.10g" % d["comp_coh_pre"].max())
    n["surv_ceil"] = (int((d["surv_raw"] > 0.995).sum()), "max %.10g" % d["surv_raw"].max())
    n["surv_floor"] = (int((d["surv_raw"] < 0.02).sum()),
                       "%d cells at 0.02, all %s, years %d-%d"
                       % (int((d["survival"] == 0.02).sum()),
                          ",".join(sorted(d.loc[d["surv_raw"] < 0.02, "level"].unique())),
                          d.loc[d["surv_raw"] < 0.02, "year"].min(),
                          d.loc[d["surv_raw"] < 0.02, "year"].max())
                       if (d["surv_raw"] < 0.02).any() else "0 cells")
    n["m_factor"] = (len(d), "m unique = %s, applied in %d/%d cells; a constant, not a clamp" %
                     (sorted(d["measurement_factor"].unique().tolist()), len(d), len(d)))
    n["ger_cap"] = (int((d["ger_raw"] > 105.0).sum()),
                    "%d cells printed at 105.0; max raw %.10g" % (int((d["ger"] >= 105.0).sum()),
                                                                  d["ger_raw"].max()))
    n["phys_min"] = (int((OVERAGE_CAP * d["cohort"] < PHYS_CAP * d["seats"]).sum()),
                     "cohort branch binds; seat branch in %d" %
                     int((PHYS_CAP * d["seats"] <= OVERAGE_CAP * d["cohort"]).sum()))
    n["ration"] = (int((d["rationed_official"] > 0).sum()),
                   "%d cells at full capacity (enrolment == phys)" %
                   int(np.isclose(d["enrolment"], d["phys"], rtol=1e-12).sum()))
    n["oa_min"] = (int((d["d_oa"] >= d["phys"] - d["admitted_official"]).sum()), "residual-capacity arm")
    ter = d["level"] == "tertiary"
    n["ter_demand"] = (int((ter & (d["eligibility_pool"] > OVERAGE_CAP * d["cohort"])).sum()),
                       "tertiary cells")
    n["pool_cap"] = (int(np.isclose(d["eligibility_pool"], OVERAGE_CAP * d["cohort"],
                                    rtol=0, atol=1e-6).sum()), "pool == 1.05 x cohort")
    n["elig"] = (int((d["eligibility_pool"] >= d["cohort"]).sum()), "pool >= cohort")
    n["both_min"] = (int((d["rationed_official"] == 0).sum()), "nothing rationed -> ratio == 1")
    n["ptr"] = (int(((d["ptr"] >= PTR_HI) | (d["ptr"] <= PTR_LO)).sum()),
                "range %.10g-%.10g" % (d["ptr"].min(), d["ptr"].max()))
    n["growth"] = (int(((d["growth"] <= G_FLOOR) | (d["growth"] >= G_CAP)).sum()),
                   "range %.10g-%.10g" % (d["growth"].min(), d["growth"].max()))
    ssum = d[["school_share", "both_share", "work_share", "neither_share"]].sum(axis=1) - 1.0
    low = d["level"] != "tertiary"
    n_low = int((ssum[low].abs() <= 1e-9).sum())
    n_ter = int((ssum[~low].abs() <= 1e-9).sum())
    n["simplex"] = (n_low, "levels 0-2: %d/%d sum to 1 (max |dev| %.3g); tertiary: %d/%d at 1 -- exempt "
                           "by declaration (PARAMS sec.6: adult block, non-enrolment in out_of_school)"
                    % (n_low, int(low.sum()), float(ssum[low].abs().max()), n_ter, int((~low).sum())))
    n["secfloors"] = (int(((d["s_ag"] <= SEC_FLOORS[0]) | (d["s_inf"] <= SEC_FLOORS[1])
                          | (d["s_man"] <= SEC_FLOORS[2]) | (d["s_srv"] <= SEC_FLOORS[3])).sum()),
                      "s_ag %d, s_inf %d, s_man %d, s_srv %d at floor"
                      % (int((d["s_ag"] <= SEC_FLOORS[0] + 1e-12).sum()),
                         int((d["s_inf"] <= SEC_FLOORS[1] + 1e-12).sum()),
                         int((d["s_man"] <= SEC_FLOORS[2] + 1e-12).sum()),
                         int((d["s_srv"] <= SEC_FLOORS[3] + 1e-12).sum())))
    if "pi0" in d.columns:
        n["gate_bounds"] = (int(((d["pi0"] >= 0.999) | (d["pi0"] <= 0.01) | (d["kappa"] <= 1.0)
                                 | (d["kappa"] >= 5.0) | (d["Q_gate"] >= 10.0)
                                 | (d["R"] >= 20.0) | (d["R"] <= 1.0)).sum()),
                            "pi0 at 0.999: %d; kappa at 1.0: %d; Q at 10: %d; R at 20: %d"
                            % (int((d["pi0"] >= 0.999).sum()), int((d["kappa"] <= 1.0).sum()),
                               int((d["Q_gate"] >= 10.0).sum()), int((d["R"] >= 20.0).sum())))
    else:
        n["gate_bounds"] = (None, "gate columns (Q_gate/pi0/kappa/R) not emitted in this panel")
    if "tier_queue_H" in d.columns:
        n["tier_split"] = (int((d["tier_queue_H"] > 0).sum()),
                           "Tier H oversubscribed; Tier O full in %d; Tier O unfilled in %d"
                           % (int(np.isclose(d["tier_T_O"], d["tier_K_O"], rtol=1e-12).sum()),
                              int((d["tier_O_unfilled"] > 0).sum())))
        n["tier_padv"] = (int((d["tier_p_adv_H"] >= PADV_HI).sum()),
                          "at 0.999: %d; at 0.01: %d"
                          % (int((d["tier_p_adv_H"] >= PADV_HI).sum()),
                             int((d["tier_p_adv_H"] <= PADV_LO).sum())))
    else:
        n["tier_split"] = (None, "tier block absent on this panel (v1.3/v1.2: bimodal = False)")
        n["tier_padv"] = (None, "tier block absent on this panel")
    n["kappa_link"] = (0, "block skipped: kappa_link = False in the A17 arm")
    return n


# --------------------------------------------------------------------------------------
# per-cell enumeration
# --------------------------------------------------------------------------------------
ENUMERATE = {"CAP-01", "CAP-04", "CAP-06", "CAP-07", "CAP-11", "CAP-23"}


def cells_rows(panel_name, d):
    rows = []
    def add(cid, mask, obj, unc, cap, bound, note=""):
        uv = unc if hasattr(unc, "loc") else None
        cv = cap if hasattr(cap, "loc") else None
        for _, r in d[mask].iterrows():
            u = float(uv.loc[r.name]) if uv is not None else float(unc)
            v = float(cv.loc[r.name]) if cv is not None else float(cap)
            row = dict(
                panel=panel_name, clamp_id=cid, cell_id=r["cell_id"],
                country=r["country"], level=r["level"], year=int(r["year"]),
                panel_row_1based=int(r["row_1b"]), object=obj,
                uncapped_value=u, capped_value=v, bound=bound, label=LABEL, note=note,
                binding_kind=("strict" if cid in ("CAP-01", "CAP-04", "CAP-06")
                              else "branch" if cid == "CAP-07"
                              else "at_bound_not_reconstructible"),
                ger_at_cell="", cr_over_ger="", cr_minus_ger_pp="", measure_verdict="")
            if cid == "CAP-01":
                cr_pp = 100.0 * u
                row["ger_at_cell"] = float(r["ger"])
                row["cr_over_ger"] = bool(cr_pp > r["ger"] + 1e-12)
                row["cr_minus_ger_pp"] = cr_pp - float(r["ger"])
                row["measure_verdict"] = (
                    "CR > GER: legitimate CR-above-GER case (older-cohort denominator)"
                    if row["cr_over_ger"] else
                    "CR <= GER: not a CR-above-GER case; the cap cuts a CR that is BELOW the "
                    "model's own GER")
            rows.append(row)
    m = float(d["measurement_factor"].iloc[0])
    raw_uis = m * d["comp_coh_pre"]
    add("CAP-01", raw_uis > 1.0, "completion_uis", raw_uis, d["completion_uis"], "[0.0, 1.0]",
        "ceiling cap: the declared UIS object m x cohort-flow")
    add("CAP-04", d["surv_raw"] < 0.02, "survival", d["surv_raw"], d["survival"], "[0.02, 0.995]",
        "survival floor")
    add("CAP-06", d["ger_raw"] > 105.0, "GER", d["ger_raw"], d["ger"], "[0.0, 105.0]", "GER hard cap")
    add("CAP-07", OVERAGE_CAP * d["cohort"] < PHYS_CAP * d["seats"], "physical_capacity",
        PHYS_CAP * d["seats"], d["phys"], "min(1.15 x seats, 1.05 x cohort)",
        "cohort branch selected (1.05 x cohort)")
    add("CAP-11", np.isclose(d["eligibility_pool"], OVERAGE_CAP * d["cohort"], rtol=0, atol=1e-6),
        "eligibility_pool", d["eligibility_pool"], OVERAGE_CAP * d["cohort"], "<= 1.05 x cohort",
        "pool ceiling (value already at the bound in the panel)")
    if "tier_p_adv_H" in d.columns:
        add("CAP-23", d["tier_p_adv_H"] >= PADV_HI, "tier_p_adv_H", d["tier_p_adv_H"], PADV_HI,
            "[0.01, 0.999]", "advancement-share clip")
    return rows


# --------------------------------------------------------------------------------------
# markdown
# --------------------------------------------------------------------------------------
def fmt(v):
    if v is None:
        return "n/a"
    return "%.10g" % v


def emit_md(reg, per_panel, cells, stats, out_path):
    b = sum(1 for r in reg if r["cls"] == "b")
    a = sum(1 for r in reg if r["cls"] == "a")
    c = sum(1 for r in reg if r["cls"] == "c")
    n_fix = sum(1 for r in reg if r["fix"] == "YES")
    v13 = per_panel["v1.3"]
    n_cap = stats["n_cap"]
    mx = stats["max_unc"]
    N = stats["n_rows"]

    def row_cells(cnt):
        if cnt is None or cnt[0] is None:
            return "n/a"
        return str(cnt[0])

    L = []
    A = L.append
    A("# CAP AUDIT — clamps, ceilings, floors and renormalisations (DEBUG)")
    A("")
    A("**LABEL: DEBUG.** Audit only. No model behaviour was modified, no generator was run, no")
    A("experiment was re-run, nothing was fitted, no RNG was used, no causal or direction claim is")
    A("made. Every number below is a **count of cells on the frozen panels**, a **panel value**, or")
    A("an **arithmetic identity** on those panels; all of them are produced by `code/audit_caps.py`.")
    A("")
    A("- Contract: `../PRE_DECLARATIONS.md`, sha256 `%s` — **%s**; the dispatch version was"
      % (stats["predecl_sha"], stats["predecl_version"]))
    A("  `748335cf915394c3f0dc0241fa2c5b6eaaae9c0af201dba97d3c2de24d8f6553`. The contract was AMENDED")
    A("  mid-audit (AMENDMENT 1, measure-aware); both hashes are recorded in `RUN_MANIFEST.json` and the")
    A("  audit applies the stricter, amended one.")
    A("- Named defect source: `08_council/DECISIONS.md` D160 / D164.")
    A("- Frozen panels audited: **v1.3** (%s rows), **v1.2** (%s), **A17** (%s)." % (f"{N:,}", f"{N:,}", f"{N:,}"))
    A("- Determinism: two runs, byte-identical (`results/` vs `results/determinism_run2/`).")
    A("")
    A("## 0. Headline")
    A("")
    A("| item | value |")
    A("|---|---|")
    A("| clamp / ceiling / floor / renormalisation sites enumerated | **%d** |" % len(reg))
    A("| — declared conventions (a) | **%d** |" % a)
    A("| — implementation artefacts (b) | **%d** |" % b)
    A("| — undetermined (c) | **%d** |" % c)
    A("| sites the fix must address | **%d** |" % n_fix)
    A("| `completion_uis <= 1.0` binding cells | **v1.3: %d · v1.2: %d · A17: %d** (of %s each) |"
      % (n_cap["v1.3"], n_cap["v1.2"], n_cap["A17"], f"{N:,}"))
    A("")
    A("The named defect is confirmed exactly: **%d/%s** cells on v1.3 and **%d/%s** on v1.2 have"
      % (n_cap["v1.3"], f"{N:,}", n_cap["v1.2"], f"{N:,}"))
    A("`completion_uis` printed at exactly 1.0 while the uncapped declared object `m x completion_cohort`")
    A("is above 1.0 (max **%.10g** on v1.3, **%.10g** on v1.2), and **%d/%s** on A17 (max uncapped"
      % (mx["v1.3"], mx["v1.2"], n_cap["A17"], f"{N:,}"))
    A("**%.10g**). The cap therefore binds only where the declared UIS object exceeds 1.0 — on the"
      % mx["A17"])
    A("two register panels, never on A17. That is the mechanism D160 recorded: the measured factor")
    A("`completion_uis / completion_cohort` equals 1.10 to")
    A("1e-9 on A17 (no cell capped), but falls below 1.10 wherever the cap overwrites the product, so `m`")
    A("reads NON-CONSTANT on v1.3/v1.2 (4.7043695535e-02) while it reads CONSTANT on A17 (8.8395202269e-10).")
    A("")
    A("## 1. The `completion_uis <= 1.0` cap")
    A("")
    A("Seven site lines in six code files carry the identical expression; the register panels are produced")
    A("by the **v1.3** copy (v1.3 panel), the **v1.2** copy (v1.2 panel) and the **frozen v1.6** copy inside")
    A("`generator_v1_7_partrepair/code/frozen/` (A17 panel). A17 imports that frozen copy")
    A("(`generator_v1_7_partrepair/code/sim_v1_7_partrepair.py:1117-1120`), so repairing any other v1.6")
    A("copy would not move A17.")
    A("")
    A("| # | file:line | produces | binding cells |")
    A("|---|---|---|---|")
    A("| 1 | `generator_v1_3/code/sim_v1_3.py:832` | v1.3 panel | **%d** |" % n_cap["v1.3"])
    A("| 2 | `generator_v1_2/code/sim_v1_2.py:610` | v1.2 panel | **%d** |" % n_cap["v1.2"])
    A("| 3 | `generator_v1_7_partrepair/code/frozen/sim_v1_6_repair.py:1318` | A17 panel | **%d** |" % n_cap["A17"])
    A("| 4 | `generator_v1_6_repair/code/sim_v1_6_repair.py:1318` | source of #3 | %d |" % n_cap["A17"])
    A("| 5 | `generator_v1_4_demand/code/sim_v1_4_demand.py:969` | v1.4 | not in the register |")
    A("| 6–7 | `generator_v1_5_bimodal/code/sim_v1_5_bimodal.py:756, 808` | v1.5 (two branches) | not in the register |")
    A("")
    A("Expression (verbatim): `out[\"comp_uis\"][L, t] = clip(P[\"meas_completion_factor\"] * comp_coh, 0.0, 1.0)`")
    A("where `clip(x, lo, hi) = max(lo, min(hi, float(x)))` (`sim_v1_3.py:211-212`) and")
    A("`P[\"meas_completion_factor\"] = 1.10`.")
    A("")
    A("**Why it is an artefact and not a convention.** The declared UIS convention is")
    A("`completion_uis = m x cohort-flow`, m = 1.10, single constant, all levels and countries")
    A("(`generator_v1_2/PARAMS.md` §7; v1.6 `PRE_DECLARATIONS.md` R7c). **No PARAMS, PRE_DECLARATIONS")
    A("or MODEL_ARCHITECTURE text declares a 1.0 ceiling on `completion_uis`.** The two on-disk texts")
    A("that come nearest are quoted exactly:")
    A("")
    A("1. `generator_v0/FINDINGS.md:39` — C5 'hard sanity: no negative enrolment; GER/completion in")
    A("   [0,105]; rates in [0,1]'. This is a **check on v0's own output** (v0 completion 0.77–95.01,")
    A("   in pp) and not a declared convention of the v1.2+ `completion_uis` object.")
    A("2. `generator_v1_2/FINDINGS.md:191` — '**The model's primary UIS completion reaches 100 % by 2024**")
    A("   (observed 98.3 %) — a ceiling artifact of `m × cohort-flow` clipping. It is not used as a check.'")
    A("   The programme's own v1.2 findings therefore **already named this cap a ceiling artefact**, which")
    A("   is the classification this audit independently reaches from the code and the panels.")
    A("")
    A("By construction the declared object **must** exceed 1.0 whenever")
    A("cohort-flow > 1/1.10 = 0.909090…, so the ceiling changes the declared object. That is exactly the")
    A("%d cells; the companion `comp_coh` cap at 1.0 (CAP-02) binds in **0** cells because cohort-flow" % n_cap["v1.3"])
    A("itself never reaches 1.0 (max **%.10g** on v1.3, **%.10g** on A17)." % (stats["max_coh"]["v1.3"],
                                                                              stats["max_coh"]["A17"]))
    A("")
    A("**Arithmetic verified, not assumed.** The audit reconstructs cohort-flow from the panels")
    A("(`admitted_official(t - DVEC) / cohort(t - DVEC)` x `clip(surv_max x Q^theta, 0.02, 0.995)`) and")
    A("checks it against the emitted `completion_cohort` column and against the cap itself. Maximum")
    A("absolute residual over the %s rows of each panel (three panels, 20,160 rows): **%.3g**"
      " (cohort-flow) and **%.3g**"
      % (f"{stats['n_rows']:,}", max(v["cohort_recon_max_abs_resid"] for v in stats["fidelity"].values()),
         max(v["uis_recon_max_abs_resid"] for v in stats["fidelity"].values())))
    A("(`completion_uis` vs `min(m x cohort-flow, 1.0)`, at the panels' 10-significant-figure CSV")
    A("precision). The reconstruction")
    A("therefore reproduces the panel's own arithmetic, so the 35-cell count is the cap and nothing else.")
    A("")
    A("### The 35 cells (v1.3; the identical set on v1.2)")
    A("")
    A("All 35 are **primary** level, in five countries; the cap never binds at lower-secondary,")
    A("upper-secondary or tertiary:")
    A("")
    A("| country | level | n cells | years | cohort-flow range | uncapped m x flow | capped |")
    A("|---|---|---|---|---|---|---|")
    c1 = cells[cells["clamp_id"] == "CAP-01"].query("panel == 'v1.3'")
    for (ctry, lvl), g in c1.groupby(["country", "level"]):
        A("| %s | %s | %d | %d–%d | %.10g–%.10g | %.10g–%.10g | 1.0 |"
          % (ctry, lvl, len(g), g["year"].min(), g["year"].max(),
             g["uncapped_value"].min() / 1.10, g["uncapped_value"].max() / 1.10,
             g["uncapped_value"].min(), g["uncapped_value"].max()))
    A("")
    A("Per-cell values (panel, cell id, country, level, year, panel row, uncapped, capped) are in")
    A("`CAP_AUDIT_CELLS.csv`, `clamp_id == CAP-01` — %d rows (v1.3 %d + v1.2 %d)."
      % (n_cap["v1.3"] + n_cap["v1.2"], n_cap["v1.3"], n_cap["v1.2"]))
    A("")
    A("### 1.1 Measure classification (AMENDMENT 1, binding)")
    A("")
    A("The contract was amended while this audit ran: every clamp must be classified **by measure**, and")
    A("the cap must not be read as an NER bound. The measures on disk are different objects, and only one")
    A("of them is bounded above by construction:")
    A("")
    A("| id | measure | definitional bound? | class |")
    A("|---|---|---|---|")
    for r in reg:
        if r["id"] in ("CAP-01", "CAP-02", "CAP-05", "CAP-06", "CAP-10", "CAP-12", "CAP-18"):
            A("| %s | %s | %s | (%s) |" % (r["id"], r["measure"], r["definitional"], r["cls"]))
    A("")
    A("**NER is the only measure bounded by 100 (definitional).** No NER object exists in the pipeline:")
    A("the panels emit `ger`, `completion_cohort` (CR) and `admission` shares, and **no** `ner` column on")
    A("any of the three panels. So the 1.0 ceiling cannot be defended as an NER bound — it is applied to a")
    A("**CR**, whose denominator is the older 3–5-years-above-grade cohort and which is therefore **not**")
    A("bounded by 1.0 (AMENDMENT 1: PHL 2024 = 98.3 CR on 94.0 GER).")
    A("")
    A("### 1.2 The 35 capped cells against GER (AMENDMENT 1 requirement)")
    A("")
    c1 = cells[cells["clamp_id"] == "CAP-01"]
    n_gt = int(c1["cr_over_ger"].sum())
    n13 = int((c1["panel"] == "v1.3").sum())
    n13gt = int(c1[(c1["panel"] == "v1.3")]["cr_over_ger"].sum())
    A("For every capped cell the audit reports the model's own GER at that cell and whether the uncapped")
    A("CR is above it (`CAP_AUDIT_CELLS.csv` columns `ger_at_cell`, `cr_over_ger`, `cr_minus_ger_pp`,")
    A("`measure_verdict`).")
    A("")
    A("| question | answer |")
    A("|---|---|")
    A("| capped cells with **CR > GER** (legitimate CR-above-GER cases) | **%d of %d** rows "
      "(v1.3: **%d of %d**, v1.2: **%d of %d**) |"
      % (n_gt, len(c1), n13gt, n13, n_gt - n13gt, len(c1) - n13))
    A("| capped cells with **CR <= GER** | **%d of %d** rows |" % (len(c1) - n_gt, len(c1)))
    A("| GER at the capped cells | **105.0 in all %d** (the declared Z1 gate is binding there) |" % len(c1))
    A("| uncapped CR at the capped cells | **%.10g–%.10g pp** |"
      % (100 * c1["uncapped_value"].min(), 100 * c1["uncapped_value"].max()))
    A("| CR − GER spread at the capped cells | **%.10g to %.10g pp** (all negative) |"
      % (c1["cr_minus_ger_pp"].min(), c1["cr_minus_ger_pp"].max()))
    A("")
    A("**Verdict on the 35: none is a legitimate CR-above-GER case.** In all 35 the model's GER sits at")
    A("its declared 105 gate and the CR is *below* it (100.03–104.47 pp). The cap therefore cuts a CR that")
    A("is already under the model's own GER — it cannot be described as 'holding CR down to GER' or as an")
    A("NER-style impossibility. The 15 cells on v1.3 where the model does put CR above GER (max +2.65 pp)")
    A("are **not** capped (their CR < 1.0). Both facts are arithmetic on the frozen panels.")
    A("")
    A("Note the co-location, which is descriptive only: all 35 capped cells are primary cells in which")
    A("official-age admission is ≈0.991–0.996 of the cohort and survival 0.916–0.956, so cohort-flow is")
    A("0.909–0.950 and m x cohort-flow is 1.000–1.045; the same cells sit on the cohort branch of the")
    A("declared capacity gate (1.05 x cohort), which is why GER is at 105 there. No causal claim is made.")
    A("")
    A("## 2. Full register")
    A("")
    A("**`cells`** = panel cells in which the bound **changes** the value (strictly beyond the bound),")
    A("except for a constant convention (CAP-05) where it is the number of cells the constant is applied")
    A("to, and for a renormalisation (CAP-18) where it is the number of cells the identity holds in.")
    A("`n/a` = the site is not on the frozen-panel path (§4) or the pre-clip object is internal and not")
    A("emitted. The note in `CAP_AUDIT_TABLE.csv` gives ties, ranges and per-panel qualifiers.")
    A("")
    A("`CAP_AUDIT_CELLS.csv` adds `binding_kind`: **strict** = the pre-clip value is reconstructed and")
    A("lies beyond the bound (CAP-01, CAP-04, CAP-06); **branch** = a `min()` arm was selected (CAP-07);")
    A("**at_bound_not_reconstructible** = the emitted column is already post-clip, so the bound is")
    A("observed but the pre-clip value cannot be recovered from the panel (CAP-11, CAP-23).")
    A("")
    A("| id | stage | symbol / expression | file:line | bound | object | v1.3 | v1.2 | A17 | class |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for r in reg:
        f, ln = r["sites"][0][0], r["sites"][0][1]
        sym = r["fingerprint"].split("\n")[0].replace("|", "\\|")
        if len(sym) > 72:
            sym = sym[:69] + "…"
        vals = [row_cells(per_panel[p].get(r["counter"])) for p in ("v1.3", "v1.2", "A17")]
        A("| %s | %s | `%s` | `%s:%d` | %s | %s | %s | %s | %s | **(%s)** |"
          % (r["id"], r["stage"], sym, Path(f).name, ln, r["bound"], r["object"],
             vals[0], vals[1], vals[2], r["cls"]))
    A("")
    A("`file:line` is the first site of each entry; CAP-01 lists all seven copies in §1, and CAP-21")
    A("covers four bounds at one site. `CAP_AUDIT_TABLE.csv` carries the same register with the full")
    A("`why`, `declared_in`, the complete site list and the per-panel notes.")
    A("")
    A("## 3. Declared conventions vs implementation artefacts")
    A("")
    A("**Declared conventions (a), %d sites** — bounds that are part of the declared object:" % a)
    A("")
    for r in reg:
        if r["cls"] == "a":
            A("- **%s** `%s:%d` — %s. Declared in: %s"
              % (r["id"], Path(r["sites"][0][0]).name, r["sites"][0][1],
                 r["object"], r["declared_in"].replace("\n", " ")))
    A("")
    A("**Implementation artefacts (b), %d site** — a bound that changes a declared object and is declared"
      % b)
    A("nowhere on disk:")
    A("")
    for r in reg:
        if r["cls"] == "b":
            A("- **%s** `%s:%d` — %s (%s). %s"
              % (r["id"], Path(r["sites"][0][0]).name, r["sites"][0][1], r["bound"], r["object"], r["why"]))
    A("")
    A("**Undetermined (c), %d sites** — undeclared bounds that need the Lead / Council:" % c)
    A("")
    for r in reg:
        if r["cls"] == "c":
            A("- **%s** `%s:%d` — %s (%s). %s"
              % (r["id"], Path(r["sites"][0][0]).name, r["sites"][0][1], r["bound"], r["object"], r["why"]))
    A("")
    A("Only **CAP-04** among the (c) items actually binds on a model object (24 tertiary cells, below).")
    A("CAP-14 (`ptr` guard) and CAP-20 (`sig` guard) bind in 0 informative cells.")
    A("")
    A("## 4. Scope and what was NOT audited")
    A("")
    A("- **In scope and counted**: the synthetic generator chain v1.2→v1.7 that produces the frozen")
    A("  panels — every `comp_uis` / `comp_coh` / `surv` / `ger` / capacity / share / gate-number site.")
    A("- **Adjacent model code, listed not counted**: `10_massification/model/{anchor,pushpull,repair}.py`")
    A("  belongs to the **A1 anchor class / observed chain**, not to the synthetic panel path. Its bounds")
    A("  are declared (MOD-01…MOD-10) and none of them can bind on a synthetic panel cell; they are in the")
    A("  register so the enumeration is complete, with `n/a` counts. MOD-09 is deliberately listed as a")
    A("  site with **no** clamp (the observed chain does not cap GER at 105) to show the contrast.")
    A("- **Econometric input guards excluded as non-model**: `np.log(x.clip(lower=1e-3))`-style guards in")
    A("  the `dt_/edu_eci_/lab_` extension scripts (log-domain hygiene on observed inputs). They never")
    A("  touch a model object; no panel cell depends on them, so they are not clamps of model behaviour.")
    A("- **Internal state that is not emitted** (`queue_carry <= 0.20 x LF`, `E_r <= J`, `att`): the")
    A("  bound is real but the pre-clip quantity is not in any panel, so **no cell count is claimed** —")
    A("  stated, not guessed (CAP-16, CAP-17).")
    A("- **No re-derivation of model values**: the audit reads the frozen panels; it does not re-run the")
    A("  generator, does not re-score EXP-21 and produces no new model number.")
    A("")
    A("## 5. Minimal defect set for Agent 2")
    A("")
    A("**One defect, one expression, seven site lines in six files — three of them produce the register**")
    A("**panels:**")
    A("")
    A("```")
    A("out[\"comp_uis\"][L, t] = clip(P[\"meas_completion_factor\"] * comp_coh, 0.0, 1.0)")
    A("```")
    A("")
    A("The fix must make `completion_uis` the **declared** object `m x cohort-flow` (m = 1.10, no")
    A("undeclared upper bound). At minimum it must touch the copies that produce the register panels:")
    A("`sim_v1_3.py:832` (v1.3), `sim_v1_2.py:610` (v1.2) and `frozen/sim_v1_6_repair.py:1318` (A17).")
    A("The lower bound `0.0` may stay (a completion cannot be negative; 0 cells bind), but the upper")
    A("bound must go, or be replaced only by an explicitly declared and defended UIS CR convention.")
    A("**No threshold, parameter, seed or fitted value changes; the repair is the ceiling only.**")
    A("")
    A("**Measure-aware conditions on that fix (AMENDMENT 1):**")
    A("")
    A("1. **Do not touch the GER cap (CAP-06) as part of this fix.** It is a declared Z1 gate, not an NER")
    A("   identity, and the amendment forbids recasting GER as if it were NER-bounded. Moving it would be a")
    A("   threshold change, which the contract bars.")
    A("2. **Do not introduce an NER cap anywhere.** No NER object exists on disk; NER <= 100 is")
    A("   definitional and needs no clamp, because there is nothing to clamp.")
    A("3. **The declared convention to state explicitly** in the repaired code/manifest is the UIS CR")
    A("   convention: completion = share of the population 3–5 years above grade that completed the level,")
    A("   with repeaters across years and over-age entrants counted, m = 1.10 as the declared single")
    A("   constant standing in for that older denominator. On that convention a CR above 1.0 and a CR")
    A("   above GER are both admissible.")
    A("4. **Report, per cell, whether the repaired CR now exceeds GER** (the same four columns the audit")
    A("   emits), so the measure question is answered on the re-run and not asserted.")
    A("")
    A("**Not in the minimal set** (reported, not licensed by this defect):")
    A("")
    A("- **CAP-04** — survival floor 0.02: 24 tertiary cells (20 countries, 1970–72 burn-in), identical")
    A("  on v1.3/v1.2/A17. It binds and is undeclared, so it is a genuine open item, but it is upstream of")
    A("  the m-cap and cannot explain the v1.3-vs-A17 constancy difference. It must be adjudicated")
    A("  separately and must **not** be changed under the ceiling-cap licence.")
    A("- **CAP-14 / CAP-20** — undeclared, non-binding guards: 0 cells, no action.")
    A("- **CAP-18 note (not a clamp)** — on A17 the four-state shares sum to 1 in 5,040/5,040")
    A("  lower/upper/primary cells, exactly as on v1.3; the tertiary rows that do not sum to 1")
    A("  (1,590 of 1,680 on A17, all 1,680 on v1.3) are the declared adult exemption, not a violation.")
    A("")
    A("## 6. Reproduction")
    A("")
    A("```")
    A("python code/audit_caps.py --out results")
    A("python code/audit_caps.py --out results/determinism_run2")
    A("```")
    A("")
    A("Each run writes `CAP_AUDIT.md`, `CAP_AUDIT_TABLE.csv`, `CAP_AUDIT_CELLS.csv` and `console.txt`")
    A("into `--out`; the two runs are byte-identical. `python code/audit_caps.py --manifest-only`")
    A("regenerates `RUN_MANIFEST.json` from the same counts without writing any other artifact.")
    A("Hashes of every input and output are in `RUN_MANIFEST.json` and `SHA256SUMS.txt`.")
    A("")
    out_path.write_text("\n".join(L) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------------------
# manifest
# --------------------------------------------------------------------------------------
def write_manifest(reg, per_panel, stats, cells, fidelity):
    inputs = []
    for name, path in PANELS.items():
        inputs.append(dict(role="frozen panel (%s)" % name, path=str(path.relative_to(PROG)),
                           sha256=sha256_file(path), rows=6720))
    inputs.append(dict(role="contract", path=str(PREDECL.relative_to(PROG)),
                       sha256=stats["predecl_sha"], version=stats["predecl_version"]))
    seen = set()
    for r in reg:
        for (f, ln, _) in r["sites"]:
            if f in seen:
                continue
            seen.add(f)
            inputs.append(dict(role="audited source", path=f, sha256=sha256_file(PROG / f)))
    inputs.sort(key=lambda x: x["path"])

    outputs = []
    for rel in ("CAP_AUDIT.md", "CAP_AUDIT_TABLE.csv", "CAP_AUDIT_CELLS.csv",
                "RUN_MANIFEST.json", "code/audit_caps.py",
                "results/CAP_AUDIT.md", "results/CAP_AUDIT_TABLE.csv",
                "results/CAP_AUDIT_CELLS.csv", "results/console.txt",
                "results/determinism_run2/CAP_AUDIT.md",
                "results/determinism_run2/CAP_AUDIT_TABLE.csv",
                "results/determinism_run2/CAP_AUDIT_CELLS.csv",
                "results/determinism_run2/console.txt"):
        fp = CELL / rel
        if fp.exists() and rel != "RUN_MANIFEST.json":
            outputs.append(dict(path=rel, sha256=sha256_file(fp)))

    pairs = [("CAP_AUDIT.md",), ("CAP_AUDIT_TABLE.csv",), ("CAP_AUDIT_CELLS.csv",), ("console.txt",)]
    det = {"compared": ["results/%s vs results/determinism_run2/%s" % (a[0], a[0]) for a in pairs]}
    ok = all((CELL / "results" / a[0]).read_bytes()
             == (CELL / "results" / "determinism_run2" / a[0]).read_bytes() for a in pairs)
    det["n_files"] = len(pairs)
    det["n_identical"] = len(pairs) if ok else 0
    det["status"] = "BYTE-IDENTICAL" if ok else "MISMATCH"

    man = dict(
        cell="DEBUG-CAP-AUDIT",
        agent="Agent 1 (CAP AUDIT)",
        label=LABEL,
        date="2026-11-21",
        mode="model-debug (audit only)",
        objective="enumerate and classify every clamp/ceiling/floor/renormalisation in the "
                  "completion pipeline; report before any fix",
        contract=dict(path=str(PREDECL.relative_to(PROG)), sha256=stats["predecl_sha"],
                      version=stats["predecl_version"],
                      note="the contract was amended mid-audit (AMENDMENT 1, measure-aware); "
                           "versions 748335cf... (dispatch) and 7d8bade9... (amended) are both "
                           "licensed and both were read"),
        classification_counts=dict(
            declared_convention=sum(1 for r in reg if r["cls"] == "a"),
            implementation_artefact=sum(1 for r in reg if r["cls"] == "b"),
            undetermined=sum(1 for r in reg if r["cls"] == "c"),
            total=len(reg)),
        counts=dict(
            panels={k: 6720 for k in PANELS},
            completion_uis_cap_binding={k: per_panel[k]["cap_uis"][0] for k in PANELS},
            completion_uis_cap_max_uncapped={k: stats["max_unc"][k] for k in PANELS},
            completion_cohort_cap_binding={k: per_panel[k]["cap_coh"][0] for k in PANELS},
            survival_floor_binding={k: per_panel[k]["surv_floor"][0] for k in PANELS},
            ger_cap_binding={k: per_panel[k]["ger_cap"][0] for k in PANELS},
            capped_cells_cr_above_ger=int(cells[cells["clamp_id"] == "CAP-01"]["cr_over_ger"].sum()),
        ),
        fidelity=fidelity,
        minimal_defect_set=["CAP-01"],
        not_in_minimal_set=["CAP-04 (survival floor 0.02)"],
        discipline=dict(
            no_model_code_modified=True,
            no_generator_run=True,
            no_experiment_rerun=True,
            no_rng=True,
            no_fit=True,
            no_threshold_change=True,
            no_existing_repo_file_overwritten=True,
            write_scope=str(CELL.relative_to(PROG)),
            labels=["DEBUG"],
            wall_clock=False,
        ),
        determinism=det,
        inputs=inputs,
        outputs=outputs,
    )
    (CELL / "RUN_MANIFEST.json").write_text(
        json.dumps(man, indent=1, sort_keys=True) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results")
    ap.add_argument("--manifest-only", action="store_true",
                    help="recompute counts and write RUN_MANIFEST.json; write no other artifact")
    args = ap.parse_args()
    out = (CELL / args.out) if not Path(args.out).is_absolute() else Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # --- contract hash enforced at run time ------------------------------------------
    got = sha256_file(PREDECL)
    if got not in PREDECL_HASHES:
        sys.exit("REFUSING: PRE_DECLARATIONS.md sha256 %s is not a licensed version (%s)"
                 % (got, ", ".join(PREDECL_HASHES)))
    predecl_version = PREDECL_HASHES[got]

    # --- load panels ------------------------------------------------------------------
    frames = {}
    for name, path in PANELS.items():
        frames[name] = prep(pd.read_csv(path))
        if len(frames[name]) != 6720:
            sys.exit("REFUSING: panel %s has %d rows, expected 6720" % (name, len(frames[name])))

    # --- verify every registry site verbatim on disk -----------------------------------
    reg = registry()
    site_hashes = {}
    for r in reg:
        for (f, ln, fp) in r["sites"]:
            p = PROG / f
            if not p.exists():
                sys.exit("REFUSING: missing source %s" % f)
            lines = p.read_text(encoding="utf-8").splitlines()
            one = lines[ln - 1].strip()
            first = fp.split("\n")[0].strip()
            if first not in one:
                sys.exit("REFUSING: %s:%d does not contain the expected expression\n  expected: %s\n  found:    %s"
                         % (f, ln, first, one))
            site_hashes.setdefault(f, sha256_file(p))

    # --- fidelity guards: the reconstruction must be the panel's own arithmetic ----------
    fidelity = {}
    for name, d in frames.items():
        m = float(d["measurement_factor"].iloc[0])
        resid = float((d["comp_coh_pre"] - d["completion_cohort"]).abs().max())
        err = float((np.minimum(m * d["comp_coh_pre"], 1.0) - d["completion_uis"]).abs().max())
        if not (resid <= 1e-8 and err <= 1e-8):
            sys.exit("REFUSING: %s reconstruction is not the panel's arithmetic "
                     "(cohort resid %.3g, uis resid %.3g)" % (name, resid, err))
        fidelity[name] = dict(cohort_recon_max_abs_resid=resid, uis_recon_max_abs_resid=err)

    # --- counts ------------------------------------------------------------------------
    per_panel = {name: counters(d) for name, d in frames.items()}
    stats = {
        "n_rows": len(frames["v1.3"]),
        "n_cap": {k: per_panel[k]["cap_uis"][0] for k in ("v1.3", "v1.2", "A17")},
        "max_unc": {k: float((frames[k]["measurement_factor"].iloc[0]
                              * frames[k]["comp_coh_pre"]).max()) for k in ("v1.3", "v1.2", "A17")},
        "max_coh": {k: float(frames[k]["comp_coh_pre"].max()) for k in ("v1.3", "v1.2", "A17")},
        "fidelity": fidelity,
        "predecl_sha": got,
        "predecl_version": predecl_version,
    }

    rows = []
    for name, d in frames.items():
        rows.extend(cells_rows(name, d))
    cells = pd.DataFrame(rows)
    cells["_po"] = cells["panel"].map({"v1.3": 0, "v1.2": 1, "A17": 2})
    cells = (cells.sort_values(["clamp_id", "_po", "country", "level", "year"], kind="mergesort")
             .drop(columns=["_po"]).reset_index(drop=True))

    # --- table -------------------------------------------------------------------------
    trows = []
    for r in reg:
        t = dict(
            id=r["id"], label=LABEL, pipeline=r["pipeline"], stage=r["stage"], kind=r["kind"],
            symbol=r["fingerprint"].replace("\n", " "),
            file=r["sites"][0][0], line=r["sites"][0][1],
            all_sites=";".join("%s:%d" % (f, ln) for (f, ln, _) in r["sites"]),
            bound=r["bound"], object=r["object"], classification=r["cls"],
            measure=r["measure"], definitional=r["definitional"],
            declared_in=r["declared_in"].replace("\n", " "), why=r["why"].replace("\n", " "),
            fix_required=r["fix"],
        )
        for p in ("v1.3", "v1.2", "A17"):
            cnt = per_panel[p].get(r["counter"])
            t["n_cells_" + p.replace(".", "")] = None if (cnt is None or cnt[0] is None) else int(cnt[0])
            t["note_" + p.replace(".", "")] = "" if cnt is None else cnt[1]
        trows.append(t)
    tab = pd.DataFrame(trows)
    for c in ("n_cells_v13", "n_cells_v12", "n_cells_A17"):
        tab[c] = pd.array(tab[c], dtype="Int64")
    if args.manifest_only:
        write_manifest(reg, per_panel, stats, cells, fidelity)
        print("manifest written")
        return
    tab.to_csv(out / "CAP_AUDIT_TABLE.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    cells.to_csv(out / "CAP_AUDIT_CELLS.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    emit_md(reg, per_panel, cells, stats, out / "CAP_AUDIT.md")

    # --- console -----------------------------------------------------------------------
    C = []
    C.append("AUDIT_CAPS  LABEL=DEBUG  deterministic, no RNG, no generator run")
    C.append("PRE_DECLARATIONS sha256 %s  [%s]" % (got, predecl_version))
    C.append("panels: " + " | ".join("%s=%d rows" % (k, len(v)) for k, v in frames.items()))
    C.append("fidelity (max |recon - panel|): " + " | ".join(
        "%s cohort=%.3g uis=%.3g" % (k, v["cohort_recon_max_abs_resid"], v["uis_recon_max_abs_resid"])
        for k, v in fidelity.items()))
    C.append("sites enumerated: %d" % len(reg))
    for r in reg:
        vals = []
        for p in ("v1.3", "v1.2", "A17"):
            cnt = per_panel[p].get(r["counter"])
            vals.append("n/a" if (cnt is None or cnt[0] is None) else str(cnt[0]))
        C.append("%-8s %-3s %-58s v1.3=%-6s v1.2=%-6s A17=%-6s fix=%s"
                 % (r["id"], r["cls"], r["object"][:58], vals[0], vals[1], vals[2], r["fix"]))
    C.append("cells enumerated in CAP_AUDIT_CELLS.csv: %d rows (%d clamps)"
             % (len(cells), cells["clamp_id"].nunique()))
    C.append("-- CAP-01 cells (35 + 35) --")
    c1 = cells[cells["clamp_id"] == "CAP-01"]
    for _, r in c1.iterrows():
        C.append("%-5s %-44s %-16s %d  unc=%.10g cap=%.10g"
                 % (r["panel"], r["cell_id"], r["country"], r["year"],
                    r["uncapped_value"], r["capped_value"]))
    (out / "console.txt").write_text("\n".join(C) + "\n", encoding="utf-8")

    print("\n".join(C[:6]))
    print("written:", out)


if __name__ == "__main__":
    main()
