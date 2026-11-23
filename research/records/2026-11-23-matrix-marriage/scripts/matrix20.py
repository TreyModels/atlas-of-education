#!/usr/bin/env python3
"""20-measure within-country lead-lag matrix: the 17 handoff measures plus three
UN marriage measures (women's mean age at marriage, share never married at 45-49,
female-minus-male marriage-age gap).

Estimator: exactly the handoff estimator (research/records/2026-11-23-handoff-run/
scripts/full_matrix_trends.py) -- ten-year change in y regressed on the level of x
at the start year, country effects, decade effects, income and urbanisation
controlled, country-clustered standard errors, optional country-specific linear
trends.  That code path is `edge_marriage.build_rows` + `edge_marriage.fit`, which
reproduces the handoff edge() for panel pairs (verified in validate_baseline.py).

Adaptation for the sparse UN series (survey/census years, no interpolation):
  * if y is a panel measure: start year t = any year where y has t and t+10 and
    x has t  (this is the handoff sample when x is also a panel measure);
  * if y is a marriage measure: start years are real pairs of surveys 8-13 years
    apart; x must be observed at the starting survey year.
Marriage age is NEVER a control: the control set is identical (income,
urbanisation) for every link, and marriage measures only ever appear as x or y.

Outputs: out/matrix20.csv (one row per directed link per trend setting),
out/matrix20.json (nested), BH q-values inside.
"""
import json, sys
from multiprocessing import Pool
import numpy as np
from scipy.stats import norm
from edge_marriage import S, build_rows, fit

# Session rule: the income file holds GDP per head in LEVELS despite its name.
# Log it at load, before any fit, so every link uses a logged income control.
S["gdppc_log"] = {k: float(np.log(max(v, 1.0))) for k, v in S["gdppc_log"].items()}

PANEL17 = ["electricity", "wage_emp", "lsc", "sec", "ter", "prm_cmp",
           "gdppc_log", "urban", "tax", "agri_va", "emp_agri", "flfp",
           "life_exp", "u5mr", "gpi_sec", "gpi_ter", "fertility"]
MARRIAGE = ["smam_f", "nevermar_f_4549", "smam_gap"]
VARS = PANEL17 + MARRIAGE
assert len(VARS) == 20


def mode_for(y):
    return "survey10" if y in MARRIAGE else "grid10"


def one(job):
    x, y = job
    mode = mode_for(y)
    out = {}
    for trend in (False, True):
        r = fit(build_rows(x, y, mode), trend, x, y)
        if r is None:
            out["trend" if trend else "fe"] = None
        else:
            t = r["b"] / r["se"] if r["se"] > 0 else float("nan")
            p = 2.0 * norm.sf(abs(t)) if np.isfinite(t) else None
            out["trend" if trend else "fe"] = dict(
                b=r["b"], se=r["se"], n=r["n"], nc=r["nc"], n10=r["n10"],
                years=r["years"], t=float(t), p=p)
    return (x, y, mode, out)


def bh(pvals):
    """Benjamini-Hochberg q-values; pvals: list of (key, p) with p not None."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i][1])
    q = [None] * m
    prev = 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        val = min(prev, pvals[i][1] * m / rank)
        q[i] = val
        prev = val
    return {pvals[i][0]: q[i] for i in range(m)}


if __name__ == "__main__":
    jobs = [(x, y) for x in VARS for y in VARS if x != y]
    print(f"{len(VARS)} measures, {len(jobs)} ordered links", flush=True)
    with Pool(6) as pool:
        res = pool.map(one, jobs, chunksize=4)
    matrix = {f"{x}->{y}": dict(mode=m, **r) for x, y, m, r in res}

    for setting in ("fe", "trend"):
        pv = [(k, v[setting]["p"]) for k, v in matrix.items()
              if v[setting] and v[setting]["p"] is not None]
        qs = bh(pv)
        for k, v in matrix.items():
            if v[setting]:
                v[setting]["q"] = qs.get(k)

    # verdicts
    def sig(v, setting):
        return bool(v[setting]) and v[setting]["se"] > 0 and \
            abs(v[setting]["t"]) > 1.96

    for k, v in matrix.items():
        fe, tr = v["fe"], v["trend"]
        v["involves_marriage"] = ("->" in k and
                                  (k.split("->")[0] in MARRIAGE or k.split("->")[1] in MARRIAGE))
        v["verdict"] = {
            "estimable_fe": bool(fe is not None),
            "estimable_trend": bool(tr is not None),
            "sig_fe": bool(sig(v, "fe")),
            "sig_trend": bool(sig(v, "trend")),
            "survives_both": bool(sig(v, "fe") and sig(v, "trend") and
                                  ((fe["b"] > 0) == (tr["b"] > 0))),
            "bh_sig_fe": bool(fe is not None and fe.get("q") is not None and fe["q"] < 0.05),
            "bh_sig_trend": bool(tr is not None and tr.get("q") is not None and tr["q"] < 0.05),
        }

    json.dump(matrix, open("out/matrix20.json", "w"), indent=1, default=float)

    import csv
    cols = ["x", "y", "mode", "involves_marriage", "setting", "b", "se", "n",
            "nc", "n10", "year_first", "year_last", "t", "p", "q"]
    with open("out/matrix20.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for k in sorted(matrix):
            x, y = k.split("->")
            v = matrix[k]
            for setting in ("fe", "trend"):
                r = v[setting]
                if r is None:
                    w.writerow([x, y, v["mode"], v["involves_marriage"], setting,
                                None, None, 0, 0, 0, None, None, None, None, None])
                else:
                    w.writerow([x, y, v["mode"], v["involves_marriage"], setting,
                                round(r["b"], 6), round(r["se"], 6), r["n"], r["nc"],
                                r["n10"], r["years"][0], r["years"][1],
                                round(r["t"], 4), r["p"],
                                None if r.get("q") is None else round(r["q"], 6)])

    # summary
    for setting in ("fe", "trend"):
        est = sum(1 for v in matrix.values() if v[setting])
        sg = sum(1 for v in matrix.values() if sig(v, setting))
        bhs = sum(1 for v in matrix.values()
                  if v[setting] and v[setting].get("q") is not None and v[setting]["q"] < 0.05)
        print(f"{setting:6s}: estimable {est}/380, sig {sg}, BH<0.05 {bhs}")
    surv = [k for k, v in matrix.items() if v["verdict"]["survives_both"]]
    print(f"survive both FE and trends (same sign): {len(surv)}")
    mar = [k for k in surv if matrix[k]["involves_marriage"]]
    print(f"  of which marriage-involving: {len(mar)}")
    print("BASELINE 17-measure survivors (income logged; corrected handoff baseline is 24):",
          sum(1 for k in surv if not matrix[k]["involves_marriage"]))
    print("\nmarriage-involving links surviving both, by |t| with trends:")
    for k in sorted(mar, key=lambda k: -abs(matrix[k]["trend"]["t"])):
        tr, fe = matrix[k]["trend"], matrix[k]["fe"]
        print(f"  {k:28s} FE {fe['b']:+.4f}±{fe['se']:.4f}  TR {tr['b']:+.4f}±{tr['se']:.4f} "
              f"n={tr['n']} countries={tr['nc']} BHq={tr['q']}")
