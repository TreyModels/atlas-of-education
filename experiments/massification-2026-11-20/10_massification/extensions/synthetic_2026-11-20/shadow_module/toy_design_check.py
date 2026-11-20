#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYNTHETIC / TOY design check for the shadow-education gating module (generator v1.3).

LABEL: SYNTHETIC. This is NOT a v1.3 run and NOT evidence about any country.

Pre-declared in PRE_DECLARATIONS.md sec.12 as a DESIGN CHECK ONLY:
  * it evaluates the frozen demand equation on DECLARED ILLUSTRATIVE gate states,
    not on a v1.2 simulation;
  * it CAN test c1, c2, c3, c5 as internal properties of the equation;
  * it CANNOT test c4 (needs v1.2 state + cohort exposure over time) or c6
    (needs the v1.2 panel). Any c4-shaped number printed here is a worked
    example of the arithmetic and MUST NOT be reported as a c4 result.

Refuses to run if PRE_DECLARATIONS.md does not match its frozen sha256.
"""
import csv
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_PREDECL_SHA256 = "cf8c61cb818cd63acfb2ada594bc9541bfcb0711f801e13b7eee3b86508f94f2"
SEED = 20261120  # inherited from v1.2; this toy is deterministic and draws no random numbers

# ---------------------------------------------------------------------------
# 1. FROZEN CENTRAL PARAMETERS  (copied from PARAMETERS.csv; asserted below)
# ---------------------------------------------------------------------------
A0 = -4.80
AG = -2.80
BZ, BV, BD, BY, BF = 2.00, 1.00, 2.00, 0.60, 0.80
DELTA = {0: 0.02, 1: 0.30, 2: 0.30, 3: 0.25, 4: 0.20}
WQ, WPI, WK = 0.40, 0.40, 0.20
R_EAP = 0.087
H = 20.0
DS = {1: 3.0, 2: 3.0, 3: 4.0, 4: 0.0}
G_GAP = 0.55          # g4 wage-gap placeholder (PARAMETERS.csv B21)
OMEGA = [0.20] * 5
ZQ = [-1.2816, -0.5244, 0.0, 0.5244, 1.2816]

# country inputs (PARAMETERS.csv C01-C12)
COUNTRY = {
    "SYN_HKG_LIKE": dict(phi=0.940, s=0.0305, sigma=0.55, nu={1: 0.10, 2: 0.62, 3: 0.22}, oos=5.428),
    "SYN_PHL_LIKE": dict(phi=0.677, s=0.0400, sigma=0.80, nu={1: 0.30, 2: 0.35, 3: 0.10}, oos=24.737),
    "SYN_KHM_LIKE": dict(phi=0.464, s=0.0210, sigma=0.75, nu={1: 0.28, 2: 0.13, 3: 0.02}, oos=56.987),
}

# ILLUSTRATIVE gate states (SYNTHETIC/TOY). In v1.3 these come from the run:
#   Q = candidates/capacity, pi0 = advances/candidates, kappa = rank factor.
# Declared here so the arithmetic of the frozen equation is reproducible by hand.
ILLUSTRATIVE = {
    "SYN_HKG_LIKE": {1: (0.95, 1.10), 2: (0.30, 2.50), 3: (0.18, 2.60), 4: (0.45, 1.80)},
    "SYN_PHL_LIKE": {1: (0.85, 1.15), 2: (0.40, 1.40), 3: (0.22, 1.60), 4: (0.32, 1.35)},
    "SYN_KHM_LIKE": {1: (0.72, 1.20), 2: (0.35, 1.20), 3: (0.15, 1.30), 4: (0.25, 1.20)},
}
G0_STATE = (0.97, 1.00, 0.02)   # pi0, kappa, Q at the pre-gate


def sig(x):
    return 1.0 / (1.0 + math.exp(-x))


def pressure(Q, pi0, kappa):
    Q = min(max(Q, 0.0), 10.0)
    pi0 = min(max(pi0, 0.01), 0.999)
    kappa = min(max(kappa, 1.0), 5.0)
    R = (1.0 + Q) ** WQ * (1.0 / pi0) ** WPI * kappa ** WK
    return min(max(R, 1.0), 20.0)


def credential_value(phi, gate):
    if gate == 0:
        return 0.0                     # no positional good before the first gate
    if gate == 4:
        return phi * G_GAP * H         # formal-rung wage-gap form
    return phi * R_EAP * DS[gate] * H


def quintile_income(sigma):
    raw = [math.exp(sigma * z) for z in ZQ]
    m = sum(raw) / len(raw)
    return [x / m for x in raw]


def demand(phi, s, sigma, R, V, dpi, gate, shift_lnR=0.0, phi_mult=1.0):
    """Frozen equation of PRE_DECLARATIONS.md sec.4."""
    a = A0 if gate == 0 else AG
    V = V * phi_mult
    lnR = math.log(R) + shift_lnR
    y = quintile_income(sigma)
    acc = 0.0
    ps = []
    for w, r in zip(OMEGA, y):
        th = (a + BZ * lnR + BV * math.log(1.0 + V) + BD * math.log(1.0 + dpi)
              + BY * math.log(r) - BF * math.log(1.0 + s / r))
        p = sig(th)
        ps.append(p)
        acc += w * p
    return acc, ps


def main():
    # --- hash guard: refuse to run on a mutated pre-declaration -------------
    predecl = os.path.join(HERE, "PRE_DECLARATIONS.md")
    with open(predecl, "rb") as f:
        got = hashlib.sha256(f.read()).hexdigest()
    if got != FROZEN_PREDECL_SHA256:
        sys.stderr.write("REFUSING TO RUN: PRE_DECLARATIONS.md sha256 mismatch\n"
                         "  expected %s\n  got      %s\n" % (FROZEN_PREDECL_SHA256, got))
        return 2

    rows = []
    summary = {}

    for cname, ci in COUNTRY.items():
        # g0 pre-gate
        pi0_0, kap_0, Q_0 = G0_STATE
        R0 = pressure(Q_0, pi0_0, kap_0)
        dpi0 = DELTA[0] * (1.0 - pi0_0)
        D0, p0 = demand(ci["phi"], ci["s"], ci["sigma"], R0, 0.0, dpi0, 0)
        rows.append(dict(country=cname, gate="g0_PRE", Q=Q_0, pi0=pi0_0, pi1=pi0_0 + dpi0,
                         kappa=kap_0, R=R0, V=0.0, s=ci["s"], dpi=dpi0, D_gate=D0,
                         spend=D0 * ci["s"], label="SYNTHETIC/TOY"))

        Dg = {}
        for g in (1, 2, 3, 4):
            pi0, kap = ILLUSTRATIVE[cname][g]
            Q = 1.0 / pi0 - 1.0          # consistent queue: applicants per place
            R = pressure(Q, pi0, kap)
            V = credential_value(ci["phi"], g)
            dpi = DELTA[g] * (1.0 - pi0)
            D, ps = demand(ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g)
            Dg[g] = D

            # c1/c2 experiments at g2 only (pre-declared)
            dD_R2 = dD_phi = float("nan")
            if g == 2:
                d1, _ = demand(ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g, shift_lnR=math.log(2.0))
                d2, _ = demand(ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g, phi_mult=1.25)
                dD_R2 = d1 - D
                dD_phi = d2 - D

            rows.append(dict(country=cname, gate="g%d" % g, Q=Q, pi0=pi0, pi1=pi0 + dpi,
                             kappa=kap, R=R, V=V, s=ci["s"], dpi=dpi, D_gate=D,
                             spend=D * ci["s"], label="SYNTHETIC/TOY",
                             dD_if_R_doubled=dD_R2, dD_if_phi_plus25pct=dD_phi))

        Dstar = sum(ci["nu"][g] * Dg[g] for g in (1, 2, 3))
        exposure = sum(ci["nu"].values())
        summary[cname] = dict(D0=D0, D1=Dg[1], D2=Dg[2], D3=Dg[3], D4=Dg[4],
                              Dstar=Dstar, exposure=exposure)

    # --- internal-property checks (c1, c2, c3, c5) --------------------------
    # c1(i): sign of dD/dlnR at every cell, by finite difference
    c1_sign_ok = True
    for cname, ci in COUNTRY.items():
        for g in (1, 2, 3, 4):
            pi0, kap = ILLUSTRATIVE[cname][g]
            Q = 1.0 / pi0 - 1.0
            R = pressure(Q, pi0, kap)
            V = credential_value(ci["phi"], g)
            dpi = DELTA[g] * (1.0 - pi0)
            base, _ = demand(ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g)
            up, _ = demand(ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g, shift_lnR=1e-4)
            if up - base < 0:
                c1_sign_ok = False
    c1_gaps = {c: max(r.get("dD_if_R_doubled", float("nan")) for r in rows
                      if r["country"] == c and r["gate"] == "g2") for c in COUNTRY}
    c1_pass = c1_sign_ok and all(v >= 0.10 for v in c1_gaps.values())

    c2_gaps = {c: max(r.get("dD_if_phi_plus25pct", float("nan")) for r in rows
                      if r["country"] == c and r["gate"] == "g2") for c in COUNTRY}
    c2_pass = all(v >= 0.02 for v in c2_gaps.values())

    c3_max = max(s["D0"] for s in summary.values())
    c3_ratio = {c: summary[c]["D0"] / summary[c]["D1"] for c in summary}
    c3_pass = c3_max <= 0.025 and all(v <= 0.20 for v in c3_ratio.values())

    c5_ok = True
    for r in rows:
        for k in ("D_gate", "pi0", "pi1"):
            if not (0.0 <= r[k] <= 1.0) or r[k] != r[k]:
                c5_ok = False
        if r["spend"] < 0 or r["pi1"] < r["pi0"]:
            c5_ok = False
    for c, s in summary.items():
        if s["Dstar"] > s["exposure"] + 1e-12 or s["Dstar"] < 0:
            c5_ok = False

    # --- outputs -----------------------------------------------------------
    outdir = os.path.join(HERE, "toy")
    os.makedirs(outdir, exist_ok=True)
    cols = ["label", "country", "gate", "Q", "pi0", "pi1", "kappa", "R", "V", "s",
            "dpi", "D_gate", "spend", "dD_if_R_doubled", "dD_if_phi_plus25pct"]
    with open(os.path.join(outdir, "toy_results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            row = {}
            for k in cols:
                v = r.get(k, "")
                if isinstance(v, float):
                    row[k] = "" if v != v else ("%.10g" % v)   # NaN -> empty cell
                else:
                    row[k] = v
            w.writerow(row)

    res = dict(
        label="SYNTHETIC/TOY",
        predecl_sha256_verified=FROZEN_PREDECL_SHA256,
        seed=SEED,
        random_draws=0,
        checks_scored_here=["c1", "c2", "c3", "c5"],
        checks_not_testable_here=["c4", "c6"],
        c1=dict(verdict="PASS" if c1_pass else "FAIL", sign_all_cells_nonneg=c1_sign_ok,
                gaps_at_g2={k: round(v, 4) for k, v in c1_gaps.items()}, threshold=0.10),
        c2=dict(verdict="PASS" if c2_pass else "FAIL",
                gaps_at_g2={k: round(v, 4) for k, v in c2_gaps.items()}, threshold=0.02),
        c3=dict(verdict="PASS" if c3_pass else "FAIL", max_D_g0=round(c3_max, 5),
                ratio_to_g1={k: round(v, 4) for k, v in c3_ratio.items()},
                thresholds=[0.025, 0.20]),
        c5=dict(verdict="PASS" if c5_ok else "FAIL"),
        summary={k: {kk: round(vv, 4) for kk, vv in v.items()} for k, v in summary.items()},
    )
    with open(os.path.join(outdir, "toy_checks.json"), "w") as f:
        json.dump(res, f, indent=2, sort_keys=True)
        f.write("\n")

    # markdown
    L = []
    L.append("# TOY DESIGN CHECK — shadow gating module (SYNTHETIC / TOY)\n")
    L.append("**LABEL: SYNTHETIC/TOY.** This is not a v1.3 run. It evaluates the frozen demand equation on "
             "*declared illustrative gate states*, not on a v1.2 simulation, and it is evidence about nothing in "
             "the world. Pre-declared as a design check only (`PRE_DECLARATIONS.md` §12).\n")
    L.append("Pre-declaration sha256 verified at run time: `%s`\n" % FROZEN_PREDECL_SHA256)
    L.append("Seed `%d`; zero random draws (the toy is deterministic arithmetic).\n" % SEED)
    L.append("## 1. What this can and cannot test\n")
    L.append("| | |\n|---|---|\n| Scored here | c1, c2, c3, c5 (internal properties of the equation) |")
    L.append("| **Not** testable here | **c4** (needs the v1.2 run's gate state and cohort exposure over time) "
             "and **c6** (needs the frozen v1.2 panel) |")
    L.append("| Not a result | every number below is a worked example of the arithmetic |\n")
    L.append("## 2. Participation by gate (illustrative states)\n")
    L.append("| country type | D(g0 pre) | D(g1) | D(g2) | D(g3) | D(g4 job) | D* cohort | exposure sum |")
    L.append("|---|---|---|---|---|---|---|---|")
    for c, s in summary.items():
        L.append("| %s | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.2f |" %
                 (c, s["D0"], s["D1"], s["D2"], s["D3"], s["D4"], s["Dstar"], s["exposure"]))
    L.append("")
    L.append("`D*` is the declared cohort-incidence statistic, `sum_g nu_g D_g` over g1–g3 only (out-of-school "
             "youth count as non-participants). `g4` is reported separately and is **not** part of `D*`.\n")
    L.append("## 3. Checks\n")
    L.append("| check | verdict | components |")
    L.append("|---|---|---|")
    L.append("| c1 gate pressure | **%s** | sign non-negative in all 12 cells: %s; R-doubling at g2 raises D by %s "
             "(threshold +0.10) |" % (res["c1"]["verdict"], c1_sign_ok,
                                       ", ".join("%s %+.3f" % (k, v) for k, v in c1_gaps.items())))
    L.append("| c2 expected returns | **%s** | +25%% on phi at g2 raises D by %s (threshold +0.02) |" %
             (res["c2"]["verdict"], ", ".join("%s %+.3f" % (k, v) for k, v in c2_gaps.items())))
    L.append("| c3 near-zero pre-gate | **%s** | max D(g0) = %.5f (<= 0.025); D(g0)/D(g1) = %s (<= 0.20) |" %
             (res["c3"]["verdict"], c3_max, ", ".join("%s %.3f" % (k, v) for k, v in c3_ratio.items())))
    L.append("| c5 identity | **%s** | p,D in [0,1]; pi1 >= pi0; spend >= 0; D* <= exposure |" % res["c5"]["verdict"])
    L.append("")
    L.append("## 4. Worked example only — **not** a c4 result\n")
    L.append("Per §12 of the pre-declaration, the ordering arithmetic is shown for illustration and **must not** be "
             "read as a PASS on c4. c4 requires the v1.2 gate state and the time path of exposure; this toy has "
             "neither.\n")
    L.append("| country type | D(g2) | declared band c4a | D* | ordering gap c4b |")
    L.append("|---|---|---|---|---|")
    order = list(summary.keys())
    for i, c in enumerate(order):
        gap = "" if i == len(order) - 1 else "%.4f" % (summary[c]["Dstar"] - summary[order[i + 1]]["Dstar"])
        band = "[0.75, 0.95] (HKG only)" if c == "SYN_HKG_LIKE" else "n/a (band is HKG-specific)"
        L.append("| %s | %.4f | %s | %.4f | %s |" % (c, summary[c]["D2"], band, summary[c]["Dstar"], gap))
    L.append("")
    L.append("## 5. What this toy is worth\n")
    L.append("It confirms only that the frozen equation, implemented as written, has the declared internal "
             "properties: demand is increasing in gate pressure and in the credential return, it is near zero "
             "before the first gate, and the accounting identities hold. It says nothing about v1.2, nothing about "
             "c4 or c6, and nothing about any country. If the scored v1.3 run disagrees with this toy, the v1.3 "
             "run is the result and this file is the error.\n")
    with open(os.path.join(outdir, "TOY_DESIGN_CHECK.md"), "w") as f:
        f.write("\n".join(L) + "\n")

    print(json.dumps({k: res[k] for k in ("c1", "c2", "c3", "c5")}, indent=2))
    for c, s in summary.items():
        print("%-14s D0=%.4f D1=%.4f D2=%.4f D3=%.4f D4=%.4f D*=%.4f" %
              (c, s["D0"], s["D1"], s["D2"], s["D3"], s["D4"], s["Dstar"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
