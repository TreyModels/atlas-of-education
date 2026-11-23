#!/usr/bin/env python3
"""Reruns the tight_tests.py within-country lead-lag for chosen pairs only (same code, imported), both ways:
 ORIG  = as run on 22 Nov (outcome in its own units; b_xy per SD of X, in outcome points)
 A2    = outcome standardised (the unit-mismatch fix from apex-v1.2 commit a21bbe6)
 Also prints the plain pooled FE coefficient per percentage point (comparable with the pack matrix)."""
import sys, os, json
import numpy as np
import tight_tests as TT
import sweep as S

PAIRS = [("electricity", "lsc"), ("electricity", "sec"), ("wage_emp", "ter"), ("urban", "lsc")]
rows, names, meta = S.build(); p = S._prep(rows, names); A = p["A"]
for k in names:
    A[f"d_{k}"] = A[f"dx_{k}"]; A[f"{k}_0"] = A[k]
for o in S.OUTCOMES:
    A[o] = A[f"{o}_0"]
g = dict(A=A, iso=p["iso"], dec=p["dec"], t=np.array([r["t"] for r in rows]), region={i: meta[i]["region"] for i in set(p["iso"])})
TT._init(g)
print("panel gdppc_log (true log applied in sweep.build): median %.2f, range %.2f..%.2f" % (np.nanmedian(A["gdppc_log"]), np.nanmin(A["gdppc_log"]), np.nanmax(A["gdppc_log"])))
mode = sys.argv[1]
if mode == "A2":
    orig = TT._pair_data
    def pd(a, b):
        y, x, yl, dec, iso, t = orig(a, b)
        return (y - y.mean()) / (y.std() or 1), x, yl, dec, iso, t
    TT._pair_data = pd
for a, b in PAIRS:
    r = TT._job_pair((a, b))[2]
    d = TT._pair_data(a, b)
    print(f"{mode:4s} {a}->{b}: b_xy={r['b_xy']:+.3f} CI({r['ci_xy'][0]:+.2f},{r['ci_xy'][1]:+.2f}) b_yx={r['b_yx']:+.3f} diffCI({r['ci_diff'][0]:+.2f},{r['ci_diff'][1]:+.2f}) leads={r['x_leads_within']} n={r['n']}  sd(X)={np.nanstd(d[1]):.2f}")
