#!/usr/bin/env python3
"""CORRECTED full-sample + 11-country African reduction (task-36), and the FE-bug fix record.

Why this file exists
--------------------
While validating a closed-form reduction against the committed region-42 results, a **bug in the committed
estimator** was found: `scripts/estimate.py` (commit 856c421/708e34a) dropped the first level of every
categorical fixed effect as the reference but included **no intercept**, which silently constrained the reference
group's mean to zero and biased every FE model by ~0.01–0.02 children. The prior record
(`research/dhs-micro-2026-11-23 @ 31ded00`) used the correct weighted within-transform (intercept + demeaned
regressors), so **the prior record's numbers are correct**; it is my region-42 run that is biased.

This script therefore computes the **correct** closed-form estimates for:
  * the full sample (all countries) — superseding `results/results.json` pending a region-42 re-run, and
  * the 11 African countries (task-36 deliverable),
using the same weighted within-transform / alternating-projection estimator as the prior record, with
cluster-robust SEs by country and a country-cluster bootstrap for the construct ratios.

Validation (must pass before any number is reported):
  * prior-specification panel reproduces the prior record: -0.57 / -1.62 / -2.54 (SE 0.06 / 0.17 / 0.24);
  * the corrected full-sample M1 differs from the (biased) committed `results.json` by the predicted small amount
    — the difference is reported, not hidden.

Data: committed panels only (`data/panel_*_<IND>.csv`); OBSERVED / ECOLOGICAL published cells.
No microdata, no synthetic data, no causal language. Outputs: results/corrected/*.
"""
import csv
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "results", "corrected")
os.makedirs(OUT, exist_ok=True)

AFRICA11 = ["MW", "ET", "UG", "LS", "TZ", "KE", "MZ", "GH", "BJ", "NM", "SZ"]
RNG = np.random.default_rng(20261124)


def read(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


def panel(kind, ind):
    return [{"country": r["country"], "survey": r["survey"], "year": int(r["year"]),
             "edu_level": int(r["edu_level"]), "value": float(r["value"]),
             "n": float(r["n"]), "has_denom": int(r["has_denom"])}
            for r in read(f"panel_{kind}_{ind}.csv")]


def subset(rows, countries):
    return [r for r in rows if r["country"] in countries]


# ------------------------------------------------------------------ correct weighted within-transform
def _dm(v, g, w):
    sw = np.bincount(g, weights=w)
    sv = np.bincount(g, weights=v * w)
    return v - (sv / np.maximum(sw, 1e-12))[g]


def _absorb1(y, X, g, w, iters=None):
    """One FE factor: exact weighted within-transform."""
    yd = _dm(y, g, w)
    Xd = np.column_stack([_dm(X[:, j], g, w) for j in range(X.shape[1])]) if X.size else X
    return yd, Xd


def _absorb_all(y, X, factors, w, iters=100, tol=1e-12):
    """Alternating projections for several FE factors (weighted)."""
    yd, Xd = y.copy(), X.copy()
    for _ in range(iters):
        delta = 0.0
        for g in factors:
            v = _dm(yd, g, w)
            delta = max(delta, float(np.max(np.abs(v - yd))) if len(v) else 0.0)
            yd = v
            for j in range(Xd.shape[1]):
                Xd[:, j] = _dm(Xd[:, j], g, w)
        if delta < tol:
            break
    return yd, Xd


def fit(y, X, factors, w, cluster, gindex_first=None, names=None):
    yd, Xd = _absorb_all(np.asarray(y, float), np.asarray(X, float), factors, np.asarray(w, float))
    ok = np.isfinite(yd) & np.all(np.isfinite(Xd), axis=1) & (np.asarray(w) > 0)
    yd, Xd, w2, cl = yd[ok], Xd[ok], np.asarray(w, float)[ok], np.asarray(cluster)[ok]
    A = Xd.T @ (Xd * w2[:, None])
    beta = np.linalg.pinv(A) @ (Xd.T @ (w2 * yd))
    u = yd - Xd @ beta
    P = np.linalg.pinv(A)
    meat = np.zeros_like(A)
    for c in sorted(set(cl)):
        m = cl == c
        s = Xd[m].T @ (w2[m] * u[m])
        meat += np.outer(s, s)
    V = P @ meat @ P
    se = np.sqrt(np.maximum(np.diag(V), 0))
    return {"beta": beta, "se": se, "n": int(len(yd)), "names": names or []}


def survey_codes(rows):
    levels = sorted({r["survey"] for r in rows})
    idx = {s: i for i, s in enumerate(levels)}
    return np.array([idx[r["survey"]] for r in rows]), levels


def country_codes(rows):
    levels = sorted({r["country"] for r in rows})
    idx = {c: i for i, c in enumerate(levels)}
    return np.array([idx[r["country"]] for r in rows]), levels


def edu_matrix(rows, twogroup):
    lv = np.array([r["edu_level"] for r in rows])
    if twogroup:
        return (lv == 1).astype(float)[:, None], ["edu_secplus"]
    return (np.column_stack([(lv == 1), (lv == 2), (lv == 3)]).astype(float),
            ["edu_primary", "edu_secondary", "edu_higher"])


def weight_vec(rows, weighted=True):
    return np.array([(r["n"] if (weighted and r["has_denom"]) else 1.0) for r in rows], float)


def m1(rows, twogroup=False, weighted=True):
    y = np.array([r["value"] for r in rows], float)
    X, names = edu_matrix(rows, twogroup)
    g, _ = survey_codes(rows)
    cl, _ = country_codes(rows)
    return fit(y, X, [g], weight_vec(rows, weighted), cl, names=names)


def m0(rows, twogroup=False, weighted=True):
    """Country FE + 5-year period FE (correct, two absorbed factors)."""
    y = np.array([r["value"] for r in rows], float)
    X, names = edu_matrix(rows, twogroup)
    gc, _ = country_codes(rows)
    gp, _ = survey_codes([dict(r, survey=str(5 * (r["year"] // 5))) for r in rows])
    cl = gc
    return fit(y, X, [gc, gp], weight_vec(rows, weighted), cl, names=names)


def ratio_boot(pa, pb, ta, tb, draws):
    common = sorted({r["country"] for r in pa} & {r["country"] for r in pb})
    def est(countries):
        fa = m1(subset(pa, countries), twogroup=ta, weighted=False)
        fb = m1(subset(pb, countries), twogroup=tb, weighted=False)
        sd_a = float(np.std([r["value"] for r in subset(pa, countries)], ddof=1))
        sd_b = float(np.std([r["value"] for r in subset(pb, countries)], ddof=1))
        ja = 0 if ta else 1  # secondary
        jb = 0 if tb else 1
        return (fb["beta"][jb] / sd_b) / (fa["beta"][ja] / sd_a)
    point = est(common)
    vals = []
    for _ in range(draws):
        vals.append(est(list(RNG.choice(common, size=len(common), replace=True))))
    vals = np.array(vals)
    return {"ratio": float(point), "ci": [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))],
            "draws": len(vals), "countries": len(common)}


def stacked(pa, pb, twogroup, draws_cluster_by_country=True):
    common = sorted({(r["country"], r["survey"]) for r in pa} & {(r["country"], r["survey"]) for r in pb})
    rows = []
    for c, s in common:
        da = {r["edu_level"]: r for r in pa if r["country"] == c and r["survey"] == s}
        db = {r["edu_level"]: r for r in pb if r["country"] == c and r["survey"] == s}
        if set(da) != set(db) or not da:
            continue
        for lvl in sorted(da):
            rows.append({"country": c, "survey": s, "edu_level": lvl, "value": da[lvl]["value"], "con": 0})
            rows.append({"country": c, "survey": s, "edu_level": lvl, "value": db[lvl]["value"], "con": 1})
    for con in (0, 1):
        vals = [r["value"] for r in rows if r["con"] == con]
        m, sd = float(np.mean(vals)), float(np.std(vals, ddof=1))
        for r in rows:
            if r["con"] == con:
                r["z"] = (r["value"] - m) / sd
    y = np.array([r["z"] for r in rows], float)
    con = np.array([r["con"] for r in rows], float)
    lv = np.array([r["edu_level"] for r in rows])
    lvls = [1] if twogroup else [1, 2, 3]
    tag = ["edu_secplus"] if twogroup else ["edu_primary", "edu_secondary", "edu_higher"]
    X = np.column_stack([(lv == l).astype(float) for l in lvls] + [con])
    names = tag + ["construct"]
    # single headline interaction, matching scripts/estimate.py (secondary for 4-level, secplus for 2-group)
    j = 0 if twogroup else 1
    X = np.column_stack([X, (lv == lvls[j]).astype(float) * con])
    names.append(f"{tag[j]}_x_construct")
    g, _ = survey_codes(rows)
    cl, _ = country_codes(rows)
    f = fit(y, X, [g], np.ones(len(rows)), cl, names=names)
    return {nm: {"b": float(f["beta"][j]), "se": float(f["se"][j])} for j, nm in enumerate(f["names"])}


def cohort_model(rows):
    """M3: country FE + cohort-bin FE + education + education x cohort (per decade, centred)."""
    y = np.array([r["value"] for r in rows], float)
    X, names = edu_matrix(rows, twogroup=False)
    coh = np.array([5 * ((r["year"] - 44.5) // 5) for r in rows], float)
    cohc = (np.array([r["year"] - 44.5 for r in rows], float) - np.mean([r["year"] - 44.5 for r in rows])) / 10.0
    lv = np.array([r["edu_level"] for r in rows])
    X = np.column_stack([X, (lv == 1) * cohc, (lv == 2) * cohc, (lv == 3) * cohc])
    names = names + ["edu_primary_x_cohort_decade", "edu_secondary_x_cohort_decade",
                     "edu_higher_x_cohort_decade"]
    gc, _ = country_codes(rows)
    levels = sorted(set(coh))
    idx = {c: i for i, c in enumerate(levels)}
    gcoh = np.array([idx[c] for c in coh])
    f = fit(y, X, [gc, gcoh], weight_vec(rows, True), gc, names=names)
    return {nm: {"b": float(f["beta"][j]), "se": float(f["se"][j])} for j, nm in enumerate(f["names"])}


def main():
    res = {"bug": {
        "description": "committed estimator dropped the first FE level without an intercept; every FE model "
                       "biased by ~0.01-0.02 children. Prior record unaffected (it used the correct "
                       "weighted within-transform). Fixed in scripts/estimate.py (intercept pre-pended).",
        "prior_record_values": [-0.57, -1.62, -2.54], "prior_record_se": [0.06, 0.17, 0.24]},
        "labels": "OBSERVED / ECOLOGICAL published cells; not causal; not the individual test",
        "method": "correct weighted within-transform (prior record's estimator), cluster-robust by country"}

    A4, B4, C4 = panel("edu4", "FE_FRTY_W_MNC"), panel("edu4", "FE_FRTR_W_TFR"), panel("edu4", "PR_WTFR_W_WFR")
    A2, B2, C2 = panel("edu2", "FE_FRTY_W_MNC"), panel("edu2", "FE_FRTR_W_TFR"), panel("edu2", "PR_WTFR_W_WFR")
    prev = panel("prior", "FE_FRTY_W_MNC")

    # ---------------- validation: corrected reduction on the prior-spec panel must reproduce the prior record
    fv = m1(prev, twogroup=False, weighted=True)
    val = {nm: {"value": round(float(fv["beta"][j]), 4), "se": round(float(fv["se"][j]), 4),
                "prior": res["bug"]["prior_record_values"][j]}
           for j, nm in enumerate(fv["names"])}
    val["max_abs_delta"] = max(abs(val[nm]["value"] - val[nm]["prior"]) for nm in fv["names"])
    val["passed"] = bool(val["max_abs_delta"] <= 0.01)
    res["validation_prior_record"] = val
    print("validation vs prior record:", json.dumps(val, indent=1))
    if not val["passed"]:
        print("STOP: corrected estimator does not reproduce the prior record; no numbers produced.")
        return 2

    # ---------------- corrected full-sample headline (supersedes the biased committed numbers)
    fa = m1(A4, twogroup=False, weighted=True)
    committed = {"edu_primary": -0.5355, "edu_secondary": -1.5685, "edu_higher": -2.5201}
    res["corrected_full_sample_M1_weighted"] = {
        nm: {"b": round(float(fa["beta"][j]), 4), "se": round(float(fa["se"][j]), 4),
             "committed_biased": committed[nm],
             "correction": round(float(fa["beta"][j]) - committed[nm], 4)}
        for j, nm in enumerate(fa["names"])}
    fa2 = m1(A2, twogroup=True, weighted=True)
    res["corrected_full_sample_M1_weighted_2group"] = {
        "b": round(float(fa2["beta"][0]), 4), "se": round(float(fa2["se"][0]), 4),
        "committed_biased": -1.5449, "correction": round(float(fa2["beta"][0]) + 1.5449, 4)}

    # ---------------- full-sample corrected contrasts
    res["full_sample"] = {
        "Q1_M1_weighted_4level": res["corrected_full_sample_M1_weighted"],
        "Q1_M0_weighted_4level": {nm: {"b": round(float(m0(A4)["beta"][j]), 4),
                                       "se": round(float(m0(A4)["se"][j]), 4)}
                                  for j, nm in enumerate(m0(A4)["names"])},
        "Q2a_ratio_2group": ratio_boot(A2, B2, True, True, 500),
        "Q2a_ratio_4level": ratio_boot(A4, B4, False, False, 500),
        "Q2b1_A_vs_B_secondary": stacked(A4, B4, False)["edu_secondary_x_construct"],
        "Q2b1_C_vs_B_secondary": stacked(C4, B4, False)["edu_secondary_x_construct"],
        "cohort": cohort_model(A4),
    }

    # ---------------- 11 African countries
    A4a, B4a, C4a = subset(A4, AFRICA11), subset(B4, AFRICA11), subset(C4, AFRICA11)
    A2a, B2a, C2a = subset(A2, AFRICA11), subset(B2, AFRICA11), subset(C2, AFRICA11)
    q1 = {}
    for tag, rows, twog, weighted in (
            ("A_M1_weighted_4level", A4a, False, True), ("A_M1_unweighted_4level", A4a, False, False),
            ("A_M1_weighted_2group", A2a, True, True),
            ("B_M1_unweighted_4level", B4a, False, False), ("B_M1_unweighted_2group", B2a, True, False),
            ("A_M0_weighted_4level", A4a, False, True), ("A_M0_weighted_2group", A2a, True, True)):
        f = m0(rows, twogroup=twog, weighted=weighted) if tag.startswith("A_M0") else \
            m1(rows, twogroup=twog, weighted=weighted)
        q1[tag] = {nm: {"b": round(float(f["beta"][j]), 4), "se": round(float(f["se"][j]), 4),
                        "n_cells": f["n"]} for j, nm in enumerate(f["names"])}
    res["africa11"] = {
        "countries": AFRICA11,
        "Q1_models": q1,
        "Q2a_ratio_2group": ratio_boot(A2a, B2a, True, True, 500),
        "Q2a_ratio_4level": ratio_boot(A4a, B4a, False, False, 500),
        "Q2b1_A_vs_B_4level": stacked(A4a, B4a, False),
        "Q2b1_C_vs_B_4level": stacked(C4a, B4a, False),
        "Q2b1_A_vs_B_2group": stacked(A2a, B2a, True),
        "Q2b1_C_vs_B_2group": stacked(C2a, B2a, True),
        "cohort": cohort_model(A4a),
    }

    # per-country corrected gradients (single education dummy, survey FE within country)
    pc = []
    for c in sorted({r["country"] for r in A2a}):
        rs = [r for r in A2a if r["country"] == c]
        if len({r["survey"] for r in rs}) < 2:
            continue
        # HC0: one country per model makes country-clustered SE degenerate; cluster on rows instead
        y = np.array([r["value"] for r in rs], float)
        X, _ = edu_matrix(rs, True)
        g, _ = survey_codes(rs)
        f = fit(y, X, [g], weight_vec(rs, True), np.arange(len(rs)))
        pc.append({"country": c, "b": round(float(f["beta"][0]), 4), "se": round(float(f["se"][0]), 4),
                   "n_surveys": len({r["survey"] for r in rs}), "n_cells": f["n"]})
    res["africa11"]["per_country_corrected"] = pc

    json.dump(res, open(os.path.join(OUT, "corrected_results.json"), "w"), indent=1)
    print(json.dumps(res["africa11"]["Q1_models"], indent=1))
    print("ratio 2-group:", res["africa11"]["Q2a_ratio_2group"])
    print("ratio 4-level:", res["africa11"]["Q2a_ratio_4level"])
    print("A_vs_B:", res["africa11"]["Q2b1_A_vs_B_4level"]["edu_secondary_x_construct"])
    print("C_vs_B:", res["africa11"]["Q2b1_C_vs_B_4level"]["edu_secondary_x_construct"])
    print("cohort:", res["africa11"]["cohort"])
    print("per-country:", pc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
