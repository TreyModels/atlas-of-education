#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SCRATCH (design phase) #2: gate-state extents in frozen v1.2.

READ-ONLY on generator_v1_2/. LABEL: SYNTHETIC. Not a v1.3 result.
"""
import importlib.util
import math
import sys
from pathlib import Path

ROOT13 = Path(__file__).resolve().parent.parent
SYNTH = ROOT13.parent
V12 = SYNTH / "generator_v1_2" / "code" / "sim_v1_2.py"

spec = importlib.util.spec_from_file_location("sim_v1_2", V12)
m = importlib.util.module_from_spec(spec)
sys.modules["sim_v1_2"] = m
spec.loader.exec_module(m)
P = m.P

res, *_ = m.run_all()
t20 = int((m.YEARS == 2020).nonzero()[0][0])


def gate_state(r, t):
    """v1.3 gate contract on v1.2 state (design-phase probe)."""
    C = r["C"][:, t]
    L = [0, 1, 2, 3]
    phys = [min(P["phys_cap"] * r["seats"][l, t], P["overage_cap"] * C[l]) for l in L]
    cand = {1: r["grads"][0, t], 2: r["grads"][1, t], 3: r["grads"][2, t]}
    cap = {1: phys[1], 2: phys[2], 3: phys[3]}
    adv = {1: r["enrol"][1, t], 2: r["enrol"][2, t], 3: r["enrol"][3, t]}
    kap = {1: r["rankf"][0, t], 2: r["rankf"][1, t], 3: r["rankf"][2, t]}
    # g4: labour pool / vacancies / hires reconstructed from E and sep
    out = {}
    for g in (1, 2, 3):
        Q = min(max(cand[g] / max(cap[g], 1e-9), 0.0), 10.0)
        pi0 = min(max(adv[g] / max(cand[g], 1e-9), 0.01), 0.999)
        k = min(max(kap[g], 1.0), 5.0)
        R = min(max((1 + Q) ** 0.40 * (1 / pi0) ** 0.40 * k ** 0.20, 1.0), 20.0)
        out[g] = (Q, pi0, k, R)
    # g4
    sep = P["sep"]
    E = r["E"][:, t]
    Ep = r["E"][:, t - 1] if t > 0 else r["E"][:, t]
    hires = [max(0.0, E[i] - (Ep[i] - sep[i] * Ep[i])) for i in range(4)]
    cand4 = sum(r["queue_r"][i, t] + hires[i] for i in (1, 2, 3))
    cap4 = sum(r["vac"][i, t] + hires[i] for i in (1, 2, 3))
    Q4 = min(max(cand4 / max(cap4, 1e-9), 0.0), 10.0)
    pi4 = min(max(sum(hires[1:]) / max(cand4, 1e-9), 0.01), 0.999)
    w = [hires[i] for i in (1, 2, 3)]
    sw = sum(w) if sum(w) > 1e-9 else 1.0
    k4 = min(max(sum(w[j] * r["rankf"][i, t] for j, i in enumerate((1, 2, 3))) / sw, 1.0), 5.0)
    R4 = min(max((1 + Q4) ** 0.40 * (1 / pi4) ** 0.40 * k4 ** 0.20, 1.0), 20.0)
    out[4] = (Q4, pi4, k4, R4)
    # g0
    Q0 = min(max(C[0] / max(r["seats"][0, t], 1e-9), 0.0), 10.0)
    pi00 = min(max(r["enrol"][0, t] / max(C[0], 1e-9), 0.01), 0.999)
    R0 = min(max((1 + Q0) ** 0.40 * (1 / pi00) ** 0.40, 1.0), 20.0)
    out[0] = (Q0, pi00, 1.0, R0)
    return out


print("country             gate: Q/pi0/kappa/R  at 2020")
for r in res:
    gs = gate_state(r, t20)
    txt = " ".join("g%d %.2f/%.3f/%.2f/%.2f" % (g, gs[g][0], gs[g][1], gs[g][2], gs[g][3])
                   for g in (0, 1, 2, 3, 4))
    print("%-18s %s" % (r["cp"]["name"], txt))

print("\n--- g0 extremes over ALL country-years (c3 exposure) ---")
worst = []
for r in res:
    for t in range(m.T):
        gs = gate_state(r, t)
        worst.append((gs[0][3], r["cp"]["name"], int(m.YEARS[t]), gs[0][0], gs[0][1]))
worst.sort(reverse=True)
print("top R0:", [(round(w[0], 2), w[1], w[2], round(w[3], 2), round(w[4], 2)) for w in worst[:6]])
print("min R0:", [(round(w[0], 2), w[1], w[2]) for w in worst[-3:]])

print("\n--- g2 R over all country-years: quantiles ---")
Rs = []
for r in res:
    for t in range(m.T):
        Rs.append(gate_state(r, t)[2][3])
Rs.sort()
import statistics
print("q05 %.2f q50 %.2f q95 %.2f max %.2f" % (Rs[int(.05 * len(Rs))], Rs[len(Rs) // 2],
                                               Rs[int(.95 * len(Rs))], Rs[-1]))

print("\n--- 2020: R and D-proxy (V-term, Delta-pi term) for the 3 candidate types ---")
for name in ("SYN28", "SYN00_PHL_LIKE", "SYN18"):
    r = [x for x in res if x["cp"]["name"] == name][0]
    gs = gate_state(r, t20)
    print(name, "gdppc %.0f" % r["Y"][t20])
    for g in (0, 1, 2, 3, 4):
        print("   g%d Q=%.3f pi0=%.3f k=%.3f R=%.3f lnR=%.3f" % (
            g, gs[g][0], gs[g][1], gs[g][2], gs[g][3], math.log(gs[g][3])))
