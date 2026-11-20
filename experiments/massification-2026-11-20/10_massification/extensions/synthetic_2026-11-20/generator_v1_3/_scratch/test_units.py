#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DESIGN-PHASE UNIT TESTS for the v1.3 shadow block (DRY_RUN_PLAN.md steps 2-3 gates).

LABEL: SYNTHETIC. These are code tests, not results. They use hand-computed values that are
independent of the implementation's own algebra (written out longhand below).
"""
import importlib.util
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT13 = HERE.parent
spec = importlib.util.spec_from_file_location("sim_v1_3", ROOT13 / "code" / "sim_v1_3.py")
m = importlib.util.module_from_spec(spec)
sys.modules["sim_v1_3"] = m
spec.loader.exec_module(m)

BEH = m.SHADOW_BEHAV
fails = []


def check(name, got, want, tol=1e-12):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    print("%-58s got %.12g  want %.12g  %s" % (name, got, want, "OK" if ok else "FAIL"))
    if not ok:
        fails.append(name)


# ---- T1: gate_numbers closed form, hand arithmetic ------------------------------------
# Q = 100/200 = 0.5 ; pi0 = 50/100 = 0.5 ; kappa = 2
# R = (1.5)^0.4 * (1/0.5)^0.4 * 2^0.2 = 1.176079... * 1.319508... * 1.148698... = 1.782602...
g = m.gate_numbers(BEH, 100.0, 200.0, 50.0, 2.0)
check("T1 Q", g["Q"], 0.5)
check("T1 pi0", g["pi0"], 0.5)
r_hand = math.exp(0.4 * math.log(1.5)) * math.exp(0.4 * math.log(2.0)) * math.exp(0.2 * math.log(2.0))
check("T1 R closed form", g["R"], r_hand)

# ---- T2: clips ------------------------------------------------------------------------
g = m.gate_numbers(BEH, 1e12, 1.0, 1.0, 99.0)
check("T2 Q clipped at 10", g["Q"], 10.0)
check("T2 kappa clipped at 5", g["kappa"], 5.0)
check("T2 R clipped at 20", g["R"], 20.0)
g = m.gate_numbers(BEH, 0.0, 1.0, 0.0, 0.0)
check("T2b pi0 floor 0.01", g["pi0"], 0.01)
check("T2b kappa floor 1.0", g["kappa"], 1.0)

# ---- T3: golden demand cell, computed longhand ----------------------------------------
phi, s, sigma = 0.940, 0.0305, 0.55
R, V, dpi, gate = 1.2146, 0.940 * 0.087 * 3.0 * 20.0, 0.30 * (1.0 - 0.901), 2
zs = [-1.2816, -0.5244, 0.0, 0.5244, 1.2816]
raw = [math.exp(sigma * z) for z in zs]
mean_raw = sum(raw) / 5.0
ys = [x / mean_raw for x in raw]
th = []
for yq in ys:
    th.append(-2.80
              + 2.00 * math.log(R)
              + 1.00 * math.log(1.0 + V)
              + 2.00 * math.log(1.0 + dpi)
              + 0.60 * math.log(yq)
              - 0.80 * math.log(1.0 + s / yq))
ps = [1.0 / (1.0 + math.exp(-t)) for t in th]
D_hand = sum(0.2 * p for p in ps)
D, ps_impl, th_impl, ys_impl = m.shadow_demand(BEH, phi, s, sigma, R, V, dpi, gate)
check("T3 D golden cell", D, D_hand)
check("T3 Theta_q3 golden cell", th_impl[2], th[2])
check("T3 p_q1 golden cell", ps_impl[0], ps[0])
print("     Theta_q3 = %.10f (a=-2.80, bZlnR=%.6f, bVln1pV=%.6f, bDln1pdpi=%.6f, byln_y=0.0, fee=%.6f)"
      % (th[2], 2.0 * math.log(R), math.log(1.0 + V), 2.0 * math.log(1.0 + dpi),
         -0.80 * math.log(1.0 + s / 1.0)))

# ---- T4: credential value -------------------------------------------------------------
check("T4 V(g0) = 0 by definition", m.credential_value(BEH, phi, 0), 0.0)
check("T4 V(g2) = phi*r*3*H", m.credential_value(BEH, phi, 2), phi * 0.087 * 3.0 * 20.0)
check("T4 V(g3) = phi*r*4*H", m.credential_value(BEH, phi, 3), phi * 0.087 * 4.0 * 20.0)
w_for = [3.2, 3.52, 4.6, 6.4]
w_inf = 1.1
check("T4 V(g4) = phi*ln(w_for2/w_inf)*H",
      m.credential_value(BEH, phi, 4, w_for, w_inf), phi * math.log(3.52 / 1.1) * 20.0)

# ---- T5: Pi >= pi0 and the bound |Pi - pi0| <= delta*(1-pi0) --------------------------
ci = dict(m.SHADOW_COUNTRY_INPUTS["SYN_KHM_LIKE"])
gs = {0: m.gate_numbers(BEH, 100.0, 90.0, 90.0, 1.0),
      1: m.gate_numbers(BEH, 100.0, 200.0, 90.0, 1.0),
      2: m.gate_numbers(BEH, 100.0, 120.0, 30.0, 1.2),
      3: m.gate_numbers(BEH, 100.0, 90.0, 15.0, 1.3),
      4: m.gate_numbers(BEH, 100.0, 20.0, 5.0, 1.4)}
sb = m.shadow_block(BEH, ci, gs, w_for, w_inf)
for g_ in range(5):
    d = sb[g_]
    ok = (d["Pi"] >= d["pi0"] - 1e-15) and (abs(d["Pi"] - d["pi0"]) <= BEH["delta"][g_] * (1.0 - d["pi0"]) + 1e-15)
    print("     g%d pi0=%.6f pi1=%.6f Pi=%.6f |Pi-pi0|=%.6f bound=%.6f  %s" % (
        g_, d["pi0"], d["pi1"], d["Pi"], abs(d["Pi"] - d["pi0"]),
        BEH["delta"][g_] * (1.0 - d["pi0"]), "OK" if ok else "FAIL"))
    if not ok:
        fails.append("T5 g%d" % g_)

# ---- T6: one behavioural rule (no country key anywhere in the behavioural block) ------
ok6, info6 = m.shadow_code_audit()
print("T6 code audit: ok=%s, forbidden=%r, country_keys=%r" % (
    ok6, info6["forbidden_tokens_found"], info6["country_specific_behavioural_keys"]))
if not ok6:
    fails.append("T6 code audit")

# ---- T7: g0 is not a gate: V=0 and delta_0=0.02 --------------------------------------
check("T7 delta_0", BEH["delta"][0], 0.02)
check("T7 delta_g2", BEH["delta"][2], 0.30)

print()
print("RESULT:", "ALL UNIT TESTS PASS" if not fails else "FAILURES: %r" % (fails,))
sys.exit(0 if not fails else 1)
