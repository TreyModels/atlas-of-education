#!/usr/bin/env python3
"""Estimate the pre-registered ecological models on the DHS public-API cell panel.

Reads ../data/panel_*.csv (built by build_panel.py), writes ../results/*.csv and ../results/results.json.

Pre-registration: ../PRE_REGISTRATION.md (committed 88073d0, before the pull).
Amendment 1: ../AMENDMENT_01.md (missing denominators for rate indicators; no by-variable issue) --
committed before any estimate. Every estimate below is OBSERVED / ECOLOGICAL: the unit is a published
country x survey x education cell, not a woman. No causal language is supported by these numbers.

Estimator: weighted least squares with absorbed fixed effects as explicit dummies, cluster-robust SEs
by country (sandwich). Outcomes are reported raw and per-SD (standardised within the estimation sample).
"""
import csv
import json
import os
import sys

# Server policy: one BLAS thread per worker; parallelise with multiprocessing instead (region-42, 96 cores).
for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import multiprocessing as mp

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
RES = os.path.join(HERE, "results")
os.makedirs(RES, exist_ok=True)

RNG = np.random.default_rng(20261124)
EDU4 = ["No education", "Primary", "Secondary", "Higher"]
EDU2 = ["No education or primary", "Secondary or higher"]


# --------------------------------------------------------------------------------------- io
def read(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load_panel(kind, ind):
    rows = read(os.path.join(DATA, f"panel_{kind}_{ind}.csv"))
    out = []
    for r in rows:
        out.append({
            "country": r["country"], "survey": r["survey"], "year": int(r["year"]),
            "survey_type": r["survey_type"], "edu": r["edu"],
            "edu_level": int(r["edu_level"]), "value": float(r["value"]),
            "n": float(r["n"]), "has_denom": int(r["has_denom"]),
        })
    return out


# ------------------------------------------------------------------------- OLS + cluster SE
def dummies(vals, drop_first=True):
    levels = sorted(set(vals))
    if drop_first:
        levels = levels[1:]
    return np.column_stack([(np.asarray(vals) == lev).astype(float) for lev in levels]) if levels \
        else np.zeros((len(vals), 0)), levels


def fit(y, X, w, cluster):
    """WLS with cluster-robust sandwich. Returns beta, se, n, k, pvals."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    w = np.asarray(w, float)
    Xw = X * w[:, None]
    XtWX = X.T @ Xw
    XtWy = Xw.T @ y
    beta = np.linalg.lstsq(XtWX, XtWy, rcond=None)[0]
    u = y - X @ beta
    P = np.linalg.pinv(XtWX)
    meat = np.zeros_like(XtWX)
    cl = np.asarray(cluster)
    for g in np.unique(cl):
        m = cl == g
        s = X[m].T @ (w[m] * u[m])
        meat += np.outer(s, s)
    V = P @ meat @ P
    se = np.sqrt(np.maximum(np.diag(V), 0))
    from math import erf, sqrt
    t = np.divide(beta, se, out=np.full_like(beta, np.nan), where=se > 0)
    p = np.array([2 * (1 - 0.5 * (1 + erf(abs(v) / sqrt(2)))) for v in t])
    return dict(beta=beta, se=se, n=len(y), k=X.shape[1], p=p, V=V, t=t)


_W = {}


def _init_worker(panels):
    _W.update(panels)


def _country_task(c):
    rows2 = _W["A2"]
    rs = [r for r in rows2 if r["country"] == c]
    if len({r["survey"] for r in rs}) < 2:
        return None
    y = np.array([r["value"] for r in rs])
    e = np.array([r["edu_level"] for r in rs], float)
    s, _ = dummies([r["survey"] for r in rs])
    X = np.column_stack([e, s])
    w = np.array([r["n"] for r in rs], float)
    f = fit(y, X, w, np.arange(len(rs)))  # HC0: one country per model
    return {"country": c, "b": float(f["beta"][0]), "se": float(f["se"][0]),
            "p": float(f["p"][0]), "n_surveys": len({r["survey"] for r in rs}),
            "n_cells": f["n"]}


def _boot_task(args):
    which, seed = args
    pa, pb, twog_a, twog_b = _W["boot"][which]
    common = sorted(set(r["country"] for r in pa) & set(r["country"] for r in pb))
    rng = np.random.default_rng(seed)
    samp = list(rng.choice(common, size=len(common), replace=True))
    ra = [r for r in pa if r["country"] in samp]
    rb = [r for r in pb if r["country"] in samp]
    oa = run_spec(ra, "M1", twogroup=twog_a, weight=False, standardise=True)
    ob = run_spec(rb, "M1", twogroup=twog_b, weight=False, standardise=True)
    if not oa or not ob:
        return which, None
    ka = "edu_secplus" if twog_a else "edu_secondary"
    kb = "edu_secplus" if twog_b else "edu_secondary"
    return which, ob["coef"][kb]["b"] / oa["coef"][ka]["b"]


def zscore(y):
    y = np.asarray(y, float)
    return (y - y.mean()) / y.std(ddof=1)


# ------------------------------------------------------------------ design matrices per spec
def edu_cols(rows, twogroup=False):
    if twogroup:
        return np.column_stack([(np.array([r["edu_level"] for r in rows]) == 1).astype(float)]), ["edu_secplus"]
    lv = np.array([r["edu_level"] for r in rows])
    return (np.column_stack([(lv == 1).astype(float), (lv == 2).astype(float), (lv == 3).astype(float)]),
            ["edu_primary", "edu_secondary", "edu_higher"])


def spec_matrix(rows, spec, twogroup=False):
    """Return X, names, names_of_interest. FE enter as dummies (reference level dropped)."""
    parts, names = [], []
    e, en = edu_cols(rows, twogroup)
    parts.append(e)
    names += en
    countries = [r["country"] for r in rows]
    surveys = [r["survey"] for r in rows]
    years = [r["year"] for r in rows]
    if spec in ("M0", "M5", "COHORT"):
        c, _ = dummies(countries)
        parts.append(c)
        names += [f"c_{i}" for i in range(c.shape[1])]
    if spec == "M0":
        per = [5 * (y // 5) for y in years]
        p, _ = dummies(per)
        parts.append(p)
        names += [f"per_{i}" for i in range(p.shape[1])]
    if spec == "M5":
        yb, _ = dummies(years)
        parts.append(yb)
        names += [f"yr_{i}" for i in range(yb.shape[1])]
        cy = np.column_stack([(np.array(countries) == c).astype(float) * (np.array(years) - 2000)
                              for c in sorted(set(countries))[1:]])
        parts.append(cy)
        names += [f"trend_{i}" for i in range(cy.shape[1])]
    if spec == "COHORT":
        # cohort proxy = survey year - 44.5 (mean age of the 40-49 group), 5-year bins
        coh = [5 * ((y - 44.5) // 5) for y in years]
        cb, _ = dummies(coh)
        parts.append(cb)
        names += [f"coh_{i}" for i in range(cb.shape[1])]
        cohc = np.array([(y - 44.5) for y in years])
        cohc = (cohc - cohc.mean()) / 10.0  # per decade, centred
        if twogroup:
            parts.append(np.column_stack([e[:, 0] * cohc]))
            names += ["edu_secplus_x_cohort_decade"]
        else:
            parts.append(np.column_stack([e[:, 0] * cohc, e[:, 1] * cohc, e[:, 2] * cohc]))
            names += ["edu_primary_x_cohort_decade", "edu_secondary_x_cohort_decade",
                      "edu_higher_x_cohort_decade"]
    if spec in ("M1", "M2"):
        s, _ = dummies(surveys)
        parts.append(s)
        names += [f"s_{i}" for i in range(s.shape[1])]
    if spec == "M2":
        pipe = np.array([r.get("pipeline", np.nan) for r in rows], float)
        pipe = np.where(np.isfinite(pipe), pipe, np.nanmean(pipe))
        pipe = (pipe - np.nanmean(pipe)) / np.nanstd(pipe)
        lv = np.array([r["edu_level"] for r in rows])
        inter = np.column_stack([(lv == 1).astype(float) * pipe, (lv == 2).astype(float) * pipe,
                                 (lv == 3).astype(float) * pipe])
        parts.append(inter)
        names += ["edu_primary_x_pipe", "edu_secondary_x_pipe", "edu_higher_x_pipe"]
    X = np.column_stack([p for p in parts if p.size]) if parts else np.zeros((len(rows), 0))
    return X, names, en


def run_spec(rows, spec, twogroup=False, weight=True, standardise=False):
    rows = [r for r in rows if r["value"] is not None]
    if len(rows) < 8:
        return None
    y = np.array([r["value"] for r in rows], float)
    if standardise:
        y = zscore(y)
    X, names, interest = spec_matrix(rows, spec, twogroup)
    ok = np.isfinite(X).all(axis=1) & np.isfinite(y)
    rows = [r for i, r in enumerate(rows) if ok[i]]
    X, y = X[ok], y[ok]
    w = np.array([(r["n"] if (weight and r["has_denom"]) else 1.0) for r in rows], float)
    cl = np.array([r["country"] for r in rows])
    f = fit(y, X, w, cl)
    idx = {nm: i for i, nm in enumerate(names)}
    out = {"spec": spec, "n_cells": f["n"], "n_surveys": len({r["survey"] for r in rows}),
           "n_countries": len({r["country"] for r in rows}), "weighted": weight,
           "standardised": standardise, "coef": {}}
    for nm in interest:
        i = idx[nm]
        out["coef"][nm] = {"b": float(f["beta"][i]), "se": float(f["se"][i]),
                           "p": float(f["p"][i]),
                           "ci": [float(f["beta"][i] - 1.96 * f["se"][i]),
                                  float(f["beta"][i] + 1.96 * f["se"][i])]}
    # extra named coefficients (interactions) captured by suffix
    for nm in names:
        if ("x_pipe" in nm or "x_cohort" in nm) and nm not in out["coef"]:
            i = idx[nm]
            out["coef"][nm] = {"b": float(f["beta"][i]), "se": float(f["se"][i]),
                               "p": float(f["p"][i]),
                               "ci": [float(f["beta"][i] - 1.96 * f["se"][i]),
                                      float(f["beta"][i] + 1.96 * f["se"][i])]}
    return out


# ------------------------------------------------------------------------------- pipeline
def pipeline_by_survey():
    recs = json.load(open(os.path.join(DATA, "raw", "ED_EDUC_W_SEH.json")))["records"]
    out = {}
    for r in recs:
        if r.get("CharacteristicCategory") != "Total":
            continue
        v = fnum(r.get("Value"))
        if v is not None:
            out[r["SurveyId"]] = v
    return out


def attach_pipeline(rows, pipe):
    for r in rows:
        r["pipeline"] = pipe.get(r["survey"])
    return rows


# -------------------------------------------------------------------------- prior-spec replicate
def load_prior_panel():
    path = os.path.join(DATA, "panel_prior_FE_FRTY_W_MNC.csv")
    rows = read(path)
    out = []
    for r in rows:
        out.append({"country": r["country"], "survey": r["survey"], "year": int(r["year"]),
                    "survey_type": r["survey_type"], "edu": r["edu"],
                    "edu_level": int(r["edu_level"]), "value": float(r["value"]),
                    "n": float(r["n"]), "has_denom": int(r["has_denom"])})
    return out


# ---------------------------------------------------------------------------- heterogeneity
def per_survey_gradient(rows2):
    by = {}
    for r in rows2:
        by.setdefault(r["survey"], {})[r["edu_level"]] = r
    out = []
    for s, d in by.items():
        if 0 in d and 1 in d:
            out.append({"survey": s, "country": d[0]["country"], "year": d[0]["year"],
                        "gradient": d[1]["value"] - d[0]["value"]})
    return out


def per_country_gradient(rows2):
    out = []
    countries = sorted({r["country"] for r in rows2})
    for c in countries:
        rs = [r for r in rows2 if r["country"] == c]
        if len({r["survey"] for r in rs}) < 2:
            continue
        y = np.array([r["value"] for r in rs])
        e = np.array([r["edu_level"] for r in rs], float)
        s, _ = dummies([r["survey"] for r in rs])
        X = np.column_stack([e, s])
        w = np.array([r["n"] for r in rs], float)
        # one country per model -> cluster-robust SE is degenerate; use heteroskedasticity-robust (HC0)
        f = fit(y, X, w, np.arange(len(rs)))
        out.append({"country": c, "b": float(f["beta"][0]), "se": float(f["se"][0]),
                    "p": float(f["p"][0]), "n_surveys": len({r["survey"] for r in rs}),
                    "n_cells": f["n"]})
    return out


def bh(pvals, q=0.05):
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    m = len(p)
    thresh = q * (np.arange(1, m + 1) / m)
    passed = p[order] <= thresh
    k = int(np.max(np.where(passed)[0]) + 1) if passed.any() else 0
    return k, p[order]


# ------------------------------------------------------------------------------------ main
def main():
    workers = int(os.environ.get("DHS_WORKERS", "48"))
    R = {"provenance": {
        "source": "api.dhsprogram.com public API, no key/no login",
        "pull_date": "2026-11-24", "preregistration_commit": "88073d0",
        "unit": "country x survey x education cell (published DHS aggregate)",
        "tier": "OBSERVED / ECOLOGICAL", "seed": 20261124}}
    pipe = pipeline_by_survey()

    # ---------- Q1: completed fertility, education gradient ----------
    A4 = attach_pipeline(load_panel("edu4", "FE_FRTY_W_MNC"), pipe)
    A2 = attach_pipeline(load_panel("edu2", "FE_FRTY_W_MNC"), pipe)
    rows_out = []
    for spec in ("M0", "M1", "M2", "M5"):
        for std in (False, True):
            for wt, tag in ((True, "weighted"), (False, "unweighted")):
                o = run_spec(A4, spec, weight=wt, standardise=std)
                if o:
                    o["label"] = f"A_completed_fertility_{spec}_{tag}{'_z' if std else ''}"
                    rows_out.append(o)
    for spec in ("M0", "M1"):
        o = run_spec(A2, spec, twogroup=True, weight=True)
        if o:
            o["label"] = f"A2_completed_fertility_{spec}_weighted"
            rows_out.append(o)
    R["Q1_models"] = rows_out

    # ---------- prior-spec replication (R1) ----------
    prior = attach_pipeline(load_prior_panel(), pipe)
    o = run_spec(prior, "M1", weight=True)
    if o:
        o["label"] = "R1_prior_spec_replication_M1"
        R["R1_prior_spec"] = o

    # ---------- Q2a: window/period contrast, A (cumulative) vs B (period TFR) ----------
    B4 = load_panel("edu4", "FE_FRTR_W_TFR")
    B2 = load_panel("edu2", "FE_FRTR_W_TFR")
    R["Q2a"] = {"models": {}}
    R["workers"] = workers
    pool = mp.Pool(workers, initializer=_init_worker,
                   initargs=({"A2": A2,
                              "boot": {"A_vs_B": (A4, B4, False, False),
                                       "A2_vs_B2": (A2, B2, True, True)}},))

    def ratio_boot_par(which, draws=500):
        pa, pb, ta, tb = {"A_vs_B": (A4, B4, False, False),
                          "A2_vs_B2": (A2, B2, True, True)}[which]
        common = sorted(set(r["country"] for r in pa) & set(r["country"] for r in pb))
        # point estimates on the COMMON-country sample so the ratio and its bootstrap CI are
        # computed on the same countries (the bootstrap resamples the common list).
        pa_c = [r for r in pa if r["country"] in common]
        pb_c = [r for r in pb if r["country"] in common]
        oa = run_spec(pa_c, "M1", twogroup=ta, weight=False, standardise=True)
        ob = run_spec(pb_c, "M1", twogroup=tb, weight=False, standardise=True)
        ka = "edu_secplus" if ta else "edu_secondary"
        kb = "edu_secplus" if tb else "edu_secondary"
        point_a, point_b = oa["coef"][ka]["b"], ob["coef"][kb]["b"]
        tasks = [(which, 20261124 + i) for i in range(draws)]
        vals = [v for w, v in pool.map(_boot_task, tasks, chunksize=5) if v is not None]
        vals = np.array(vals)
        return {"beta_A": point_a, "beta_B": point_b,
                "ratio_B_over_A": point_b / point_a,
                "ratio_ci": [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))],
                "draws_requested": draws, "draws_used": int(vals.size),
                "countries": len(common)}
    for nm, panel, twog in (("A_completed", A4, False), ("B_tfr", B4, False),
                            ("A2_completed", A2, True), ("B2_tfr", B2, True)):
        o = run_spec(panel, "M1", twogroup=twog, weight=False, standardise=True)
        if o:
            R["Q2a"]["models"][nm] = o
    # ratio of standardised secondary coefficients, cluster bootstrap by country
    R["Q2a"]["raw_models"] = {}
    for nm, panel in (("A_completed_raw", A4), ("B_tfr_raw", B4)):
        o = run_spec(panel, "M1", weight=(nm.startswith("A")), standardise=False)
        if o:
            R["Q2a"]["raw_models"][nm] = {k: {"b": v["b"], "se": v["se"], "ci": v["ci"]}
                                          for k, v in o["coef"].items()}
    R["Q2a"]["ratio_B_over_A"] = ratio_boot_par("A_vs_B")
    R["Q2a"]["ratio_B2_over_A2"] = ratio_boot_par("A2_vs_B2")

    # ---------- Q2b1: stacked construct contrast (births-based A vs B; wanted vs actual C vs B) ----------
    def stacked(pa, pb, tag, twog=False):
        ka = {}
        for r in pa:
            ka[(r["country"], r["survey"], r["edu_level"])] = r
        rows = []
        for r in pb:
            k = (r["country"], r["survey"], r["edu_level"])
            if k not in ka:
                continue
            rows.append(dict(ka[k], value=ka[k]["value"], construct=0))
            rows.append(dict(r, value=r["value"], construct=1))
        if len(rows) < 20:
            return None
        # standardise within construct
        for c in (0, 1):
            vals = [r["value"] for r in rows if r["construct"] == c]
            m, sd = np.mean(vals), np.std(vals, ddof=1)
            for r in rows:
                if r["construct"] == c:
                    r["z"] = (r["value"] - m) / sd
        y = np.array([r["z"] for r in rows])
        con = np.array([r["construct"] for r in rows], float)
        e, en = edu_cols(rows, twog)
        keep = ["edu_secplus"] if twog else ["edu_secondary"]
        base = [nm for nm in en if nm in (["edu_secplus"] if twog else ["edu_secondary", "edu_higher", "edu_primary"])]
        X = np.column_stack([e, con] + [e[:, (0 if twog else 1)] * con])
        names = en + ["construct"] + [f"{keep[0]}_x_construct"]
        s, _ = dummies([r["survey"] for r in rows])
        X = np.column_stack([X, s])
        names += [f"s_{i}" for i in range(s.shape[1])]
        cl = np.array([r["country"] for r in rows])
        w = np.ones(len(rows))
        f = fit(y, X, w, cl)
        idx = {nm: i for i, nm in enumerate(names)}
        out = {"n_rows": f["n"], "n_surveys": len({r["survey"] for r in rows}),
               "n_countries": len({r["country"] for r in rows}), "coef": {}}
        for nm in (names[:len(en) + 2]):
            i = idx[nm]
            out["coef"][nm] = {"b": float(f["beta"][i]), "se": float(f["se"][i]),
                               "p": float(f["p"][i]),
                               "ci": [float(f["beta"][i] - 1.96 * f["se"][i]),
                                      float(f["beta"][i] + 1.96 * f["se"][i])]}
        R["Q2b1_" + tag] = out
        return out
    stacked(A4, B4, "A_vs_B_births_period_vs_cumulative")
    W4 = load_panel("edu4", "PR_WTFR_W_WFR")
    stacked(W4, B4, "C_vs_B_wanted_vs_actual_tfr")

    # ---------- Q2b2: survey-level construct contrast (surviving children vs TFR) ----------
    sv = read(os.path.join(DATA, "panel_survey.csv"))
    sv = [dict(r) for r in sv]
    for r in sv:
        for k in ("ceb40_agecells", "deaths40_agecells", "surviving40", "ceb40_published_total",
                  "tfr", "wanted_tfr", "want_no_more", "pipeline_sec_plus"):
            r[k] = fnum(r.get(k))
        r["year"] = int(r["year"])
    have = [r for r in sv if r["surviving40"] is not None and r["tfr"] is not None]
    def corr(x, y):
        x, y = np.asarray(x, float), np.asarray(y, float)
        m = np.isfinite(x) & np.isfinite(y)
        return float(np.corrcoef(x[m], y[m])[0, 1]) if m.sum() > 2 else None
    def spearman(x, y):
        x, y = np.asarray(x, float), np.asarray(y, float)
        m = np.isfinite(x) & np.isfinite(y)
        rx = np.argsort(np.argsort(x[m]))
        ry = np.argsort(np.argsort(y[m]))
        return float(np.corrcoef(rx, ry)[0, 1]) if m.sum() > 2 else None
    diffsT = np.array([r["tfr"] - r["surviving40"] for r in have])
    diffsC = np.array([r["tfr"] - r["ceb40_agecells"] for r in have])
    # within-country changes (first vs last survey observed)
    byc = {}
    for r in have:
        byc.setdefault(r["country"], []).append(r)
    chg = []
    for c, rs in byc.items():
        if len(rs) >= 2:
            rs = sorted(rs, key=lambda z: z["year"])
            chg.append({"country": c, "d_surv": rs[-1]["surviving40"] - rs[0]["surviving40"],
                        "d_ceb": rs[-1]["ceb40_agecells"] - rs[0]["ceb40_agecells"],
                        "d_tfr": rs[-1]["tfr"] - rs[0]["tfr"]})
    R["Q2b2_survey_level"] = {
        "n_surveys": len(have), "n_countries": len({r["country"] for r in have}),
        "years": [min(r["year"] for r in have), max(r["year"] for r in have)],
        "corr_surviving_tfr": corr([r["surviving40"] for r in have], [r["tfr"] for r in have]),
        "corr_ceb_tfr": corr([r["ceb40_agecells"] for r in have], [r["tfr"] for r in have]),
        "spearman_surviving_tfr": spearman([r["surviving40"] for r in have], [r["tfr"] for r in have]),
        "corr_surviving_ceb": corr([r["surviving40"] for r in have], [r["ceb40_agecells"] for r in have]),
        "median_abs_TFR_minus_surviving": float(np.median(np.abs(diffsT))),
        "max_abs_TFR_minus_surviving": float(np.max(np.abs(diffsT))),
        "median_abs_TFR_minus_ceb40": float(np.median(np.abs(diffsC))),
        "max_abs_TFR_minus_ceb40": float(np.max(np.abs(diffsC))),
        "mean_ratio_TFR_over_surviving": float(np.mean([r["tfr"] / r["surviving40"] for r in have
                                                        if r["surviving40"] > 0])),
        "n_within_country_changes": len(chg),
        "corr_changes_surv_tfr": corr([c["d_surv"] for c in chg], [c["d_tfr"] for c in chg]),
        "corr_changes_ceb_tfr": corr([c["d_ceb"] for c in chg], [c["d_tfr"] for c in chg]),
        "median_change_gap_surv_minus_tfr": float(np.median([c["d_surv"] - c["d_tfr"] for c in chg]))
        if chg else None,
    }

    # ---------- desired vs actual (D4) ----------
    def std_b(panel, twog=False, weight=False):
        o = run_spec(panel, "M1", twogroup=twog, weight=weight, standardise=True)
        k = "edu_secplus" if twog else "edu_secondary"
        return None if not o else o["coef"][k]
    R["D4_desired_vs_actual"] = {
        "actual_tfr_secondary_z": std_b(B4),
        "wanted_tfr_secondary_z": std_b(W4),
        "actual_tfr_secplus_z": std_b(B2, twog=True),
        "wanted_tfr_secplus_z": std_b(load_panel("edu2", "PR_WTFR_W_WFR"), twog=True),
    }

    # ---------- cohort proxy ----------
    R["cohort_proxy"] = {}
    for twog, tag in ((False, "edu4"), (True, "edu2")):
        o = run_spec(A4 if not twog else A2, "COHORT", twogroup=twog, weight=True)
        if o:
            R["cohort_proxy"][tag] = o

    # ---------- heterogeneity ----------
    g1 = per_survey_gradient(A2)
    order = np.array([r["survey"] for r in g1])
    g1s = sorted(g1, key=lambda r: r["gradient"])
    sv_grad = np.array([r["gradient"] for r in g1])
    # per-period gradients (pre-registered heterogeneity family)
    per_rows = {}
    for r in A2:
        per_rows.setdefault(5 * (r["year"] // 5), []).append(r)
    per_out = []
    for per in sorted(per_rows):
        rs = per_rows[per]
        g = per_survey_gradient(rs)
        if g:
            vals = np.array([x["gradient"] for x in g])
            per_out.append({"period": per, "n_surveys": len(vals),
                            "median_gradient": float(np.median(vals)),
                            "share_negative": float((vals < 0).mean())})
    pc = [x for x in pool.map(_country_task, sorted({r["country"] for r in A2})) if x]
    R["heterogeneity"] = {
        "per_period": per_out,
        "per_survey_2group": {
            "n_surveys": len(sv_grad), "share_negative": float((sv_grad < 0).mean()),
            "median": float(np.median(sv_grad)),
            "iqr": [float(np.percentile(sv_grad, 25)), float(np.percentile(sv_grad, 75))],
            "min": float(sv_grad.min()), "max": float(sv_grad.max()),
        },
        "per_country": pc,
    }
    R["Q1_models_unused"] = []

    # ---------- replication of prior headline magnitudes (D1) ----------
    rep = R.get("R1_prior_spec")
    if rep:
        R["D1_replication"] = {
            "prior_record": {"primary": -0.57, "secondary": -1.62, "higher": -2.54,
                             "n_cells": 1291, "n_countries": 86, "share_surveys_negative": 0.99,
                             "median_per_survey_gradient": -1.90},
            "this_run": {k: v["b"] for k, v in rep["coef"].items()},
            "n_cells": rep["n_cells"], "n_countries": rep["n_countries"],
            "delta_secondary": rep["coef"]["edu_secondary"]["b"] - (-1.62),
            "delta_higher": rep["coef"]["edu_higher"]["b"] - (-2.54),
            "delta_primary": rep["coef"]["edu_primary"]["b"] - (-0.57),
            "reproduced_0p15_secondary": abs(rep["coef"]["edu_secondary"]["b"] - (-1.62)) <= 0.15,
            "reproduced_0p25_higher": abs(rep["coef"]["edu_higher"]["b"] - (-2.54)) <= 0.25,
        }

    # ---------- write ----------
    pool.close()
    pool.join()
    R["Q1_table"] = [{k: v for k, v in o.items() if k != "coef"} for o in rows_out]
    json.dump(R, open(os.path.join(RES, "results.json"), "w"), indent=1)

    # flat model table
    with open(os.path.join(RES, "model_table.csv"), "w") as f:
        f.write("label,coefficient,b,se,p,ci_lo,ci_hi\n")
        for o in rows_out + ([R["R1_prior_spec"]] if R.get("R1_prior_spec") else []):
            for k, v in o.get("coef", {}).items():
                if k.startswith("c_") or k.startswith("s_") or k.startswith("yr_") or \
                        k.startswith("per_") or k.startswith("coh_") or k.startswith("trend_"):
                    continue
                f.write(f"{o['label']},{k},{v['b']:.6f},{v['se']:.6f},{v['p']:.6g},"
                        f"{v['ci'][0]:.6f},{v['ci'][1]:.6f}\n")

    # heterogeneity csv
    with open(os.path.join(RES, "heterogeneity_surveys.csv"), "w") as f:
        f.write("survey,country,year,gradient\n")
        for r in g1s:
            f.write(f"{r['survey']},{r['country']},{r['year']},{r['gradient']:.6f}\n")
    pc = R["heterogeneity"]["per_country"]
    with open(os.path.join(RES, "heterogeneity_countries.csv"), "w") as f:
        f.write("country,b,se,p,n_surveys,n_cells\n")
        for r in pc:
            f.write(f"{r['country']},{r['b']:.6f},{r['se']:.6f},{r['p']:.6g},"
                    f"{r['n_surveys']},{r['n_cells']}\n")
    if pc:
        k, sp = bh([r["p"] for r in pc])
        with open(os.path.join(RES, "heterogeneity_bh.json"), "w") as f:
            json.dump({"q": 0.05, "n_countries": len(pc), "bh_rejections": k,
                       "share_negative": float(np.mean([r["b"] < 0 for r in pc]))}, f, indent=1)

    # survey-level construct table
    with open(os.path.join(RES, "survey_construct.csv"), "w") as f:
        cols = ["survey", "country", "country_name", "year", "ceb40_agecells", "deaths40_agecells",
                "surviving40", "ceb40_published_total", "tfr", "wanted_tfr", "want_no_more",
                "pipeline_sec_plus"]
        f.write(",".join(cols) + "\n")
        for r in sv:
            f.write(",".join("" if r[c] is None else str(r[c]) for c in cols) + "\n")

    print(json.dumps({k: v for k, v in R.items()
                      if k in ("D1_replication", "Q2b2_survey_level", "D4_desired_vs_actual",
                               "cohort_proxy")}, indent=1, default=str))
    print("Q1 headline:", [(o["label"], {k: round(v["b"], 3) for k, v in o["coef"].items()})
                            for o in rows_out if o["label"].startswith("A_completed_fertility_M1_weighted")])
    print("Q2a ratio:", R["Q2a"].get("ratio_B_over_A"), R["Q2a"].get("ratio_B2_over_A2"))
    print("het:", R["heterogeneity"]["per_survey_2group"])
    print("cohort:", {k: {kk: round(vv["b"], 4) for kk, vv in v["coef"].items()}
                      for k, v in R["cohort_proxy"].items()})


if __name__ == "__main__":
    main()
