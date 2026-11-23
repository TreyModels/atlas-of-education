#!/usr/bin/env python3
"""Prove the 17-measure baseline links are unchanged when the marriage measures
enter the matrix.

Recomputes the handoff matrix (research/records/2026-11-23-handoff-run/scripts/
full_matrix_trends.py) for all 17 x 16 ordered pairs with the original edge()
function, then compares every value against out/matrix20.json for the same pair.
Because the marriage measures are an enlarged variable set (never a control), the
coefficients, standard errors, samples and country counts must be identical to
machine precision.  Any difference is a bug and is reported.
"""
import json
import numpy as np
from multiprocessing import Pool
import full_matrix_trends as F

# Session rule: the income file holds levels. The handoff run entered it in
# levels (its 126/45/25 counts are the levels bug); panel-matrix's corrected
# logged baseline is 127 significant with country effects, 42 with trends,
# 24 surviving both. Log it here, in the same way as edge_marriage.py, so the
# validation compares like with like.
F.S["gdppc_log"] = {k: float(np.log(max(v, 1.0))) for k, v in F.S["gdppc_log"].items()}

PANEL17 = ["electricity", "wage_emp", "lsc", "sec", "ter", "prm_cmp",
           "gdppc_log", "urban", "tax", "agri_va", "emp_agri", "flfp",
           "life_exp", "u5mr", "gpi_sec", "gpi_ter", "fertility"]


def run(job):
    x, y, t = job
    return (x, y, t, F.edge(job))


if __name__ == "__main__":
    jobs = [(x, y, t) for x in PANEL17 for y in PANEL17 if x != y for t in (False, True)]
    with Pool(2) as p:
        res = p.map(run, jobs, chunksize=4)
    base = {(x, y, t): r for x, y, t, r in res}
    m = json.load(open("out/matrix20.json"))
    diffs = []
    missing_base = missing_new = 0
    for (x, y, t), r in base.items():
        key = f"{x}->{y}"
        setting = "trend" if t else "fe"
        if r is None:
            if key in m and m[key][setting] is not None:
                missing_base += 1
            continue
        if key not in m or m[key][setting] is None:
            missing_new += 1
            continue
        n = m[key][setting]
        diffs.append((abs(r[3] - n["b"]), abs(r[4] - n["se"]),
                      abs(r[5] - n["n"]), abs(r[6] - n["nc"]), x, y, setting))
    arr = np.array([[d[0], d[1], d[2], d[3]] for d in diffs])
    out = dict(n_compared=len(diffs), n_missing_baseline=missing_base,
               n_missing_new=missing_new,
               max_abs_b=float(arr[:, 0].max()) if len(arr) else None,
               max_abs_se=float(arr[:, 1].max()) if len(arr) else None,
               max_abs_n=float(arr[:, 2].max()) if len(arr) else None,
               max_abs_countries=float(arr[:, 3].max()) if len(arr) else None,
               n_exact=(int(np.sum((arr[:, 0] < 1e-10) & (arr[:, 1] < 1e-10))) if len(arr) else 0))
    json.dump(out, open("out/baseline_compare.json", "w"), indent=1)
    print(json.dumps(out, indent=1))
    # also verify the baseline survivor count (should be 25, as in the handoff run)
    def sig(k, trend):
        r = base[k]
        return r is not None and r[4] > 0 and abs(r[3] / r[4]) > 1.96
    fe_keys = [k for k in base if k[2] is False]
    sig_fe = [k for k in fe_keys if sig(k, False)]
    sig_tr = [k for k in fe_keys if sig((k[0], k[1], True), True)]
    both = [k for k in sig_fe
            if sig((k[0], k[1], True), True) and
            (base[k][3] > 0) == (base[(k[0], k[1], True)][3] > 0)]
    print(f"handoff baseline: significant with FE {len(sig_fe)}, with trends {len(sig_tr)}, "
          f"survivors both {len(both)} (corrected logged baseline expected: 127 / 42 / 24; "
          f"the handoff README's 126 / 45 / 25 came from income entered in levels)")
    out["handoff_counts"] = dict(sig_fe=len(sig_fe), sig_trends=len(sig_tr),
                                 survivors_both=len(both))
    json.dump(out, open("out/baseline_compare.json", "w"), indent=1)
