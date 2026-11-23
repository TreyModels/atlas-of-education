#!/usr/bin/env python3
"""Extra robustness checks that do not need the slow permutation loop.

1. Drop the UN's model-based "Estimate" rows (31% of the marriage observations)
   and re-run the headline edges on censuses/surveys only.  This is the test
   designed to kill a mechanical link: the UN's own marriage estimates are
   partly model-based, so they could correlate with fertility by construction.
2. Same edge with income genuinely logged (session rule) instead of in levels
   (what the handoff estimator does, since gdppc_log.json holds levels).
3. Heterogeneity: does the schooling -> fertility edge differ between countries
   with low and high never-married shares (a split sample, never a control)?
"""
import csv, json, os
import numpy as np
from edge_marriage import S, build_rows, fit, CTRL

OUT = "/root/work/undata/out"
EDGES = [("smam_f", "fertility", "grid10"),
         ("smam_gap", "fertility", "grid10"),
         ("nevermar_f_4549", "fertility", "grid10")]


if __name__ == "__main__":
    out = {}
    # ---- 1. census/survey-only variant -------------------------------------
    # The provenance CSV carries country names, the series carry ISO3.  We
    # rebuild the filtered series directly from the workbook instead of trying
    # to join on names.
    import extract_un as X

    def filtered(name, rows, keep_pred):
        d = {}
        for iso, yr, val, proc in rows:
            if iso is None or val is None or yr is None:
                continue
            if not keep_pred(proc):
                continue
            d.setdefault((iso, int(yr)), float(val))
        old = S[name]
        S[name] = {k: v for k, v in d.items()}
        return old

    # smam: reuse the extractor's own logic
    fem, male = [], []
    for idx, r in X.rows_from((X.WMD, "SMAM"), 3):
        if not r or not r[idx["Country or area"]]:
            continue
        code = r[idx["ISO code"]]
        iso = X.NUM2ISO.get(int(float(code))) if code not in (None, "") else None
        sex = str(r[idx["Sex"]]).strip()
        val = X.num(r[idx["DataValue"]])
        yr = X.midyear(r[idx["YearStart"]], r[idx["YearEnd"]])
        proc = str(r[idx["DataProcess"]] or "")
        if sex in ("Women", "Female"):
            fem.append((iso, yr, val, proc))
        elif sex in ("Men", "Male"):
            male.append((iso, yr, val, proc))
    not_est = lambda p: p.strip() and "estimat" not in p.lower()
    old_f = filtered("smam_f", fem, not_est)
    try:
        out["smam_f_census_survey_only"] = fit(build_rows("smam_f", "fertility", "grid10"),
                                               True, "smam_f", "fertility")
    finally:
        S["smam_f"] = old_f

    # never-married: from the ever-married sheet, same filter
    ever = []
    for idx, r in X.rows_from((X.WMD, "EVER_MARRIED"), 3):
        if not r or not r[idx["Country or area"]]:
            continue
        if str(r[idx["AgeGroup"]]).strip() != "[45-49]":
            continue
        if str(r[idx["Sex"]]).strip() not in ("Women",):
            continue
        code = r[idx["ISO code"]]
        iso = X.NUM2ISO.get(int(float(code))) if code not in (None, "") else None
        e = X.num(r[idx["DataValue"]])
        if iso is None or e is None:
            continue
        ever.append((iso, X.midyear(r[idx["YearStart"]], r[idx["YearEnd"]]),
                     100.0 - e, str(r[idx["DataProcess"]] or "")))
    old_n = filtered("nevermar_f_4549", ever, not_est)
    try:
        out["nevermar_f_4549_census_survey_only"] = fit(
            build_rows("nevermar_f_4549", "fertility", "grid10"), True,
            "nevermar_f_4549", "fertility")
    finally:
        S["nevermar_f_4549"] = old_n

    # ---- 2. income logged ---------------------------------------------------
    old_g = S["gdppc_log"]
    S["gdppc_log"] = {k: float(np.log(max(v, 1.0))) for k, v in old_g.items()}
    try:
        out["smam_f_fertility_log_income"] = fit(
            build_rows("smam_f", "fertility", "grid10"), True, "smam_f", "fertility")
        out["nevermar_f_fertility_log_income"] = fit(
            build_rows("nevermar_f_4549", "fertility", "grid10"), True,
            "nevermar_f_4549", "fertility")
    finally:
        S["gdppc_log"] = old_g

    # ---- 3. heterogeneity by marriage regime --------------------------------
    first = {}
    for (i, t), v in S["nevermar_f_4549"].items():
        if i not in first or t < first[i][0]:
            first[i] = (t, v)
    vals = sorted(v for _, v in first.values())
    cut = vals[len(vals) // 2]
    low = {i for i, (t, v) in first.items() if v <= cut}
    rows = build_rows("sec", "fertility", "grid10")
    h = {}
    for name, keep in (("low_never_married", low), ("high_never_married", set(first) - low)):
        h[name] = fit([r for r in rows if r[0] in keep], True, "sec", "fertility")
    out["heterogeneity"] = dict(cut=cut, groups=h)

    json.dump(out, open("/root/work/undata/results_robust_extra.json", "w"), indent=1)
    for k, v in out.items():
        if isinstance(v, dict) and "b" in v:
            print(f"{k:46s} b={v['b']:+.4f} se={v['se']:.4f} n={v['n']} countries={v['nc']}")
        elif k == "heterogeneity":
            print(f"heterogeneity split at never-married {v['cut']:.1f}%")
            for kk, vv in v["groups"].items():
                print(f"  {kk:20s} " + (f"b={vv['b']:+.4f} se={vv['se']:.4f} n={vv['n']}"
                                        if vv else "not estimable"))
    print("wrote /root/work/undata/results_robust_extra.json")
