#!/usr/bin/env python3
"""Build the country x survey x education panel from the cached DHS API pull.

Reads ../data/raw/<INDICATOR>.json (produced by pull_dhs_api.py), writes:
  ../data/panel_edu4_<INDICATOR>.csv   four education categories (No education = reference)
  ../data/panel_edu2_<INDICATOR>.csv   two groups (No education or primary = reference)
  ../data/panel_survey.csv             survey-level panel (completed fertility, child deaths,
                                       surviving children, TFR, wanted TFR, pipeline density)
  ../data/panel_checks.json            structural checks + national-vs-cell consistency

Rules are those pre-registered in ../PRE_REGISTRATION.md (committed 88073d0, before the pull):
cells with DenominatorUnweighted >= 20, exact label sets, one row per survey x education,
values never imputed.
"""
import json
import os
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
RAW = os.path.join(DATA, "raw")

CELL_INDS = ["FE_FRTY_W_MNC", "FE_FRTR_W_TFR", "PR_WTFR_W_WFR", "PR_DESL_W_WNM",
             "FE_AAFB_W_M25", "FE_FRTR_W_GFR"]
SURVEY_INDS = ["FE_CEBA_W_MNC", "FE_CEBA_W_MND"]
PIPE_IND = "ED_EDUC_W_SEH"

EDU4 = ["No education", "Primary", "Secondary", "Higher"]
EDU2 = ["No education or primary", "Secondary or higher"]
MIN_N = 20


def load(ind):
    d = json.load(open(os.path.join(RAW, f"{ind}.json")))
    return d["records"]


def num(x):
    try:
        v = float(x)
        return v
    except (TypeError, ValueError):
        return None


def tidy(recs, category):
    """Keep cells with a published value. Denominators are kept when DHS publishes them; the API does
    NOT publish denominators for rate/median indicators (TFR, GFR, wanted TFR, median age at first
    birth) -- see AMENDMENT_01.md. Those cells carry n=0 and has_denom=0 and enter unweighted models."""
    rows = []
    for r in recs:
        if r.get("CharacteristicCategory") != category:
            continue
        v, n = num(r.get("Value")), num(r.get("DenominatorUnweighted"))
        if v is None:
            continue
        if n is not None and n < MIN_N:
            continue
        rows.append({
            "indicator": r["IndicatorId"], "country": r["DHS_CountryCode"],
            "country_name": r["CountryName"], "survey": r["SurveyId"],
            "year": int(float(r["SurveyYear"])), "survey_type": r.get("SurveyType", ""),
            "edu": r["CharacteristicLabel"], "value": v,
            "n": 0 if n is None else n, "has_denom": 0 if n is None else 1,
            "n_weighted": num(r.get("DenominatorWeighted")),
            "ci_low": num(r.get("CILow")), "ci_high": num(r.get("CIHigh")),
        })
    return rows


def complete_panel(rows, levels):
    by = defaultdict(dict)
    meta = {}
    for r in rows:
        if r["edu"] in levels:
            by[r["survey"]][r["edu"]] = r
            meta[r["survey"]] = (r["country"], r["country_name"], r["year"], r["survey_type"])
    out = []
    for s, d in by.items():
        if len(d) != len(levels):
            continue
        c, cn, y, st = meta[s]
        for i, e in enumerate(levels):
            r = d[e]
            rec = dict(r, edu_level=i, edu_ref=int(i > 0))
            out.append(rec)
    return out


def write_csv(path, rows, cols):
    with open(path, "w") as f:
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join(str(r[c]) for c in cols) + "\n")


def main():
    checks = {}
    for ind in CELL_INDS:
        recs = load(ind)
        p4 = complete_panel(tidy(recs, "Education"), EDU4)
        p2 = complete_panel(tidy(recs, "Education (2 groups)"), EDU2)
        cols = ["indicator", "country", "country_name", "survey", "year", "survey_type",
                "edu", "edu_level", "edu_ref", "value", "n", "has_denom", "n_weighted",
                "ci_low", "ci_high"]
        write_csv(os.path.join(DATA, f"panel_edu4_{ind}.csv"), p4, cols)
        write_csv(os.path.join(DATA, f"panel_edu2_{ind}.csv"), p2, cols)
        # national consistency: weighted mean of the 4 education cells vs published total.
        # Uses DenominatorWeighted when published (unweighted counts are not population-proportional);
        # skipped for indicators without denominators (AMENDMENT_01.md).
        tot = {r["SurveyId"]: num(r.get("Value")) for r in recs
               if r.get("CharacteristicCategory") == "Total"}
        diffs = []
        by_survey = defaultdict(list)
        for r in p4:
            by_survey[r["survey"]].append(r)
        for s, rs in by_survey.items():
            if s in tot and tot[s] is not None and all(r["has_denom"] for r in rs):
                vals = np.array([r["value"] for r in rs])
                w = np.array([(r["n_weighted"] if r["n_weighted"] else r["n"]) for r in rs], float)
                if w.sum() > 0:
                    diffs.append(abs(float((vals * w).sum() / w.sum()) - tot[s]))
        checks[ind] = {
            "surveys_edu4": len(by_survey), "surveys_edu2": len({r["survey"] for r in p2}),
            "countries": len({r["country"] for r in p4}),
            "cells_edu4": len(p4),
            "national_vs_cell_weighted_mean_abs_max": round(max(diffs), 4) if diffs else None,
            "national_vs_cell_n": len(diffs),
        }
        print(ind, checks[ind])

    # ---------- prior-specification panel (all available education cells, no completeness rule) ----------
    recs = load("FE_FRTY_W_MNC")
    allrows = tidy(recs, "Education")
    for r in allrows:
        r["edu_level"] = EDU4.index(r["edu"])
        r["edu_ref"] = int(r["edu_level"] > 0)
    cols_all = ["indicator", "country", "country_name", "survey", "year", "survey_type",
                "edu", "edu_level", "edu_ref", "value", "n", "has_denom", "n_weighted",
                "ci_low", "ci_high"]
    write_csv(os.path.join(DATA, "panel_prior_FE_FRTY_W_MNC.csv"), allrows, cols_all)
    checks["prior_spec_panel"] = {
        "cells": len(allrows), "surveys": len({r["survey"] for r in allrows}),
        "countries": len({r["country"] for r in allrows}),
        "cells_with_all_levels": None,
    }

    # ---------- survey-level panel ----------
    ceb = load("FE_CEBA_W_MNC")
    dead = load("FE_CEBA_W_MND")
    tfr = {r["SurveyId"]: r for r in load("FE_FRTR_W_TFR")
           if r.get("CharacteristicCategory") == "Total"}
    wtfr = {r["SurveyId"]: num(r.get("Value")) for r in load("PR_WTFR_W_WFR")
            if r.get("CharacteristicCategory") == "Total"}
    wnm = {r["SurveyId"]: num(r.get("Value")) for r in load("PR_DESL_W_WNM")
           if r.get("CharacteristicCategory") == "Total"}
    fert40 = {r["SurveyId"]: num(r.get("Value")) for r in load("FE_FRTY_W_MNC")
              if r.get("CharacteristicCategory") == "Total"}
    pipe = {r["SurveyId"]: num(r.get("Value")) for r in load(PIPE_IND)
            if r.get("CharacteristicCategory") == "Total"}

    def by_survey(recs):
        d = defaultdict(dict)
        for r in recs:
            if r.get("CharacteristicCategory") != "Age (5-year groups)":
                continue
            v = num(r.get("Value"))
            if v is not None:
                d[r["SurveyId"]][r["CharacteristicLabel"]] = (v, num(r.get("DenominatorUnweighted")),
                                                              r["CountryName"],
                                                              r["DHS_CountryCode"],
                                                              int(float(r["SurveyYear"])),
                                                              r.get("SurveyType", ""))
        return d

    C, Dd = by_survey(ceb), by_survey(dead)
    rows = []
    for s in sorted(set(C) & set(Dd)):
        if not {"40-44", "45-49"} <= set(C[s]) or not {"40-44", "45-49"} <= set(Dd[s]):
            continue
        w = np.array([C[s]["40-44"][1] or 0, C[s]["45-49"][1] or 0], float)
        if w.sum() <= 0:
            continue
        ceb40 = float((np.array([C[s]["40-44"][0], C[s]["45-49"][0]]) * w).sum() / w.sum())
        dead40 = float((np.array([Dd[s]["40-44"][0], Dd[s]["45-49"][0]]) * w).sum() / w.sum())
        metal = C[s]["40-44"]
        rec = {
            "survey": s, "country": metal[3], "country_name": metal[2], "year": metal[4],
            "survey_type": metal[5], "ceb40_agecells": round(ceb40, 4),
            "deaths40_agecells": round(dead40, 4),
            "surviving40": round(ceb40 - dead40, 4),
            "ceb40_published_total": fert40.get(s),
            "tfr": num(tfr.get(s, {}).get("Value")),
            "wanted_tfr": wtfr.get(s), "want_no_more": wnm.get(s),
            "pipeline_sec_plus": pipe.get(s),
        }
        rows.append(rec)
    cols = ["survey", "country", "country_name", "year", "survey_type", "ceb40_agecells",
            "deaths40_agecells", "surviving40", "ceb40_published_total", "tfr",
            "wanted_tfr", "want_no_more", "pipeline_sec_plus"]
    write_csv(os.path.join(DATA, "panel_survey.csv"), rows, cols)
    checks["panel_survey"] = {
        "surveys": len(rows), "countries": len({r["country"] for r in rows}),
        "with_tfr": sum(r["tfr"] is not None for r in rows),
        "with_published_ceb40": sum(r["ceb40_published_total"] is not None for r in rows),
        "with_pipeline": sum(r["pipeline_sec_plus"] is not None for r in rows),
        "years": [min(r["year"] for r in rows), max(r["year"] for r in rows)],
    }
    json.dump(checks, open(os.path.join(DATA, "panel_checks.json"), "w"), indent=1)
    print("panel_survey", checks["panel_survey"])


if __name__ == "__main__":
    main()
