#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SCRATCH (design phase): inspect the frozen v1.2 state to size the gate block.

READ-ONLY on generator_v1_2/. Writes nothing outside _scratch/.
LABEL: SYNTHETIC. This is not a v1.3 result.
"""
import importlib.util
import sys
import time
from pathlib import Path

ROOT13 = Path(__file__).resolve().parent.parent          # generator_v1_3/
SYNTH = ROOT13.parent                                    # synthetic_2026-11-20/
V12 = SYNTH / "generator_v1_2" / "code" / "sim_v1_2.py"

spec = importlib.util.spec_from_file_location("sim_v1_2", V12)
m = importlib.util.module_from_spec(spec)
sys.modules["sim_v1_2"] = m
spec.loader.exec_module(m)

t0 = time.time()
res, ptr_obs, spend_obs, S_phl, P_phl = m.run_all()
print("run_all: %.2fs, %d countries" % (time.time() - t0, len(res)))

t2020 = int((m.YEARS == 2020).nonzero()[0][0])
print("\n2020 gdppc ranking (all 30):")
rk = sorted(range(len(res)), key=lambda i: -res[i]["Y"][t2020])
for idx in rk:
    r = res[idx]
    print("  %2d %-18s Y=%8.1f X=%.2f lit=%.2f" % (idx, r["cp"]["name"], r["Y"][t2020],
                                                   r["X"][t2020], r["lit"][t2020]))

print("\nGate-state ingredients at 2020 for a few countries:")
for idx in rk[:3] + rk[-3:] + [0]:
    r = res[idx]
    print("  %-18s grads=%s" % (r["cp"]["name"],
          " ".join("%.3g" % (r["grads"][L, t2020] / max(r["C"][L, t2020], 1e-9)) for L in range(4))))
    print("     C0..C3 (x1e6)= %s" % " ".join("%.2f" % (r["C"][L, t2020] / 1e6) for L in range(4)))
    print("     seats/C = %s ; enrol/C = %s" % (
        " ".join("%.3f" % (r["seats"][L, t2020] / max(r["C"][L, t2020], 1e-9)) for L in range(4)),
        " ".join("%.3f" % (r["enrol"][L, t2020] / max(r["C"][L, t2020], 1e-9)) for L in range(4))))
    print("     pool/C  = %s ; rf = %s" % (
        " ".join("%.3f" % (r["pool"][L, t2020] / max(r["C"][L, t2020], 1e-9)) for L in range(4)),
        " ".join("%.3f" % r["rankf"][rr, t2020] for rr in range(4))))
    print("     vac = %s ; hires = %s ; queue_r = %s" % (
        " ".join("%.3g" % (r["vac"][rr, t2020] / 1e6) for rr in range(4)),
        " ".join("%.3g" % (r["hires"][rr, t2020] / 1e6) for rr in range(4)),
        " ".join("%.3g" % (r["queue_r"][rr, t2020] / 1e6) for rr in range(4))))
    print("     w_for=%s w_inf=%.1f" % (
        " ".join("%.1f" % r["w_for"][rr, t2020] for rr in range(4)), r["w_inf"][t2020]))

# primary state 1970 / 2020 for all countries (g0 sizing)
print("\ng0 ingredients (primary): Q0=C0/seats0, pi0=enrol0/C0")
for idx in rk:
    r = res[idx]
    vals = []
    for t in (0, t2020):
        Q0 = r["C"][0, t] / max(r["seats"][0, t], 1e-9)
        pi0 = r["enrol"][0, t] / max(r["C"][0, t], 1e-9)
        vals.append((Q0, pi0))
    print("  %-18s 1970 Q0=%.2f pi0=%.3f | 2020 Q0=%.2f pi0=%.3f" % (
        r["cp"]["name"], vals[0][0], vals[0][1], vals[1][0], vals[1][1]))
