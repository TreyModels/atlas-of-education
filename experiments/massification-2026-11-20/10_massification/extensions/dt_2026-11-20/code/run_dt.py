#!/usr/bin/env python3
"""
DT1-DT5 predeclared battery (Council brief 020; D102-D105, D89).

Deterministic. No RNG, no sampling, no network, no writes outside the directory given
as argv[1]. Reads observed on-disk series only; HELD series are never proxied or fabricated.

Predeclaration: ../PRE_DECLARATIONS.md (sha256 recorded in RUN_MANIFEST.json).
DT3 is design-only / HELD: it is emitted as an UNABLE row and never scored.

Usage:
    python run_dt.py <output_dir>
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata

# ----------------------------------------------------------------------------- paths
HERE = Path(__file__).resolve()
DT_DIR = HERE.parents[1]                       # .../dt_2026-11-20
ROOT = HERE.parents[4]                         # programme root
DATA_REL = ROOT / "09_relations" / "data"
DATA_MASS = ROOT / "10_massification" / "data"
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DT_DIR / "results"
OUT.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------------- constants
Y0, Y1 = 1995, 2024
DT1_MIN_YEARS = 12
DT1_RHO = 0.40
DT2_COEF_SUPPORT = 1.0
DT2_COEF_FALSIFY = 0.5
DT2_GAP_RATIO = 0.5
DT4_RHO = 0.40
DT4_DROP_PP = 3.0
DT4_TOP_ZERO = 0.80
DT4_BOTTOM_REV = 0.40
DT5_CEIL = 90.0
DT5_REV_PP = 5.0
DT5_JOINT = 0.50
DT5_PHL_Z = -1.0


# ----------------------------------------------------------------------------- helpers
def _ranks(a) -> np.ndarray:
    return rankdata(np.asarray(a, dtype=float), method="average")


def spearman(x, y) -> float:
    rx, ry = _ranks(x), _ranks(y)
    return float(np.corrcoef(rx, ry)[0, 1])


def partial_spearman(x, y, controls) -> float:
    """Rank-residual partial Spearman: residualize ranks on ranks of controls + intercept."""
    rx, ry = _ranks(x), _ranks(y)
    R = np.column_stack([_ranks(c) for c in controls] + [np.ones(len(rx))])
    bx = np.linalg.lstsq(R, rx, rcond=None)[0]
    by = np.linalg.lstsq(R, ry, rcond=None)[0]
    ex, ey = rx - R @ bx, ry - R @ by
    den = math.sqrt(float(ex @ ex) * float(ey @ ey))
    if den == 0.0:
        return float("nan")
    return float((ex @ ey) / den)


def zscore(s: pd.Series) -> pd.Series:
    sd = float(s.std(ddof=1))
    return (s - s.mean()) / sd if sd > 0 else s * np.nan


def _demean_twoway(M: np.ndarray, gid: np.ndarray, tid: np.ndarray,
                   iters: int = 200, tol: float = 1e-12) -> np.ndarray:
    """Alternating projections (country demean, time demean), as in 09_relations/scripts/panel_lib.py."""
    M = M.astype(float).copy()
    for _ in range(iters):
        old = M.copy()
        M = M - pd.DataFrame(M).groupby(gid).transform("mean").to_numpy()
        M = M - pd.DataFrame(M).groupby(tid).transform("mean").to_numpy()
        if np.nanmax(np.abs(M - old)) < tol:
            break
    return M


def _norm_p(t: float) -> float:
    return float(math.erfc(abs(t) / math.sqrt(2.0)))


def fe_ols(df: pd.DataFrame, y: str, xs: list[str], entity: str = "iso3", time: str = "year",
           cluster: str = "iso3", min_n: int = 40, min_cty: int = 8) -> dict:
    """Two-way FE OLS, country-clustered CR1 SE, normal two-sided p (panel_lib.py spec)."""
    cols = [y] + list(xs)
    dd = df[[entity, time] + cols].dropna().copy()
    n = len(dd)
    nent = int(dd[entity].nunique())
    if n < min_n or nent < min_cty:
        return {"error": f"insufficient obs (n={n}, ctys={nent})", "n": n, "n_cty": nent}
    yv = dd[[y]].to_numpy(float)
    X = dd[list(xs)].to_numpy(float)
    gid = dd[entity].to_numpy()
    tid = dd[time].to_numpy()
    Xw = _demean_twoway(X, gid, tid)
    yw = _demean_twoway(yv, gid, tid).reshape(-1, 1)
    if not np.all(np.std(Xw, axis=0) > 1e-9):
        return {"error": "no within variation", "n": n, "n_cty": nent}
    XtX = Xw.T @ Xw
    try:
        b = np.asarray(np.linalg.solve(XtX, Xw.T @ yw)).ravel()
    except np.linalg.LinAlgError:
        return {"error": "singular XtX", "n": n, "n_cty": nent}
    e = yw.ravel() - Xw @ b
    G = int(dd[cluster].nunique())
    nyr = int(dd[time].nunique())
    k = X.shape[1]
    dof = max(n - k - (nent - 1) - (nyr - 1), 1)
    inv = np.linalg.pinv(XtX)
    meat = np.zeros((k, k))
    cvals = dd[cluster].to_numpy()
    for g in np.unique(cvals):
        m = cvals == g
        s = Xw[m].T @ e[m]
        meat += np.outer(s, s)
    scale = (G / (G - 1)) * ((n - 1) / dof)
    V = inv @ meat @ inv * scale
    se = np.sqrt(np.diag(V))
    out = {"n": n, "n_cty": nent, "n_yr": nyr, "dof": dof,
           "r2_within": 1.0 - float(e @ e) / max(float((yw.T @ yw).ravel()[0]), 1e-12),
           "terms": {}}
    for i, x in enumerate(xs):
        t = float(b[i] / se[i]) if se[i] > 0 else float("nan")
        out["terms"][x] = {"coef": float(b[i]), "se": float(se[i]), "t": t, "p": _norm_p(t)}
    return out


def load_long() -> pd.DataFrame:
    d = pd.read_csv(DATA_REL / "panel_wdi_long.csv")
    d = d[["iso3", "indicator", "year", "value"]].dropna(subset=["value"])
    return d.sort_values(["iso3", "indicator", "year"]).reset_index(drop=True)


def pivot_long(d: pd.DataFrame) -> pd.DataFrame:
    return (d.pivot_table(index=["iso3", "year"], columns="indicator", values="value")
            .reset_index().sort_values(["iso3", "year"]).reset_index(drop=True))


def row(test, estimand, statistic, stat_value, threshold, verdict, block_term,
        n, n_countries, label, components, notes) -> dict:
    return dict(test=test, estimand=estimand, statistic=statistic, stat_value=stat_value,
                threshold=threshold, verdict=verdict, block_term=block_term,
                n=n, n_countries=n_countries, label=label, components=components, notes=notes)


def det(test, level, unit, metric, value, n="", note="") -> dict:
    return dict(test=test, level=level, unit=unit, metric=metric, value=value, n=n, note=note)


# ----------------------------------------------------------------------------- DT1
def run_dt1(long: pd.DataFrame):
    p = pivot_long(long)
    need = ["SE.ADT.1524.LT.ZS", "NY.GDP.PCAP.KD", "SP.URB.TOTL.IN.ZS"]
    m = p[["iso3", "year"] + need].dropna().copy()
    cmp5 = p[["iso3", "year", "SE.PRM.CMPT.ZS"]].dropna().copy()
    cmp5["year"] = cmp5["year"] + 5
    m = m.merge(cmp5, on=["iso3", "year"], how="inner")
    m = m.dropna(subset=["SE.ADT.1524.LT.ZS", "SE.PRM.CMPT.ZS",
                         "NY.GDP.PCAP.KD", "SP.URB.TOTL.IN.ZS"])
    m = m.sort_values(["iso3", "year"]).reset_index(drop=True)
    m["log_gdp"] = np.log(m["NY.GDP.PCAP.KD"].clip(lower=1e-3))

    per, details = [], []
    for iso, g in m.groupby("iso3", sort=True):
        if len(g) < DT1_MIN_YEARS:
            continue
        rho_p = partial_spearman(g["SE.ADT.1524.LT.ZS"], g["SE.PRM.CMPT.ZS"],
                                 [g["log_gdp"], g["SP.URB.TOTL.IN.ZS"]])
        rho_r = spearman(g["SE.ADT.1524.LT.ZS"], g["SE.PRM.CMPT.ZS"])
        per.append({"iso3": iso, "n": int(len(g)), "rho_partial": rho_p, "rho_raw": rho_r})
        details.append(det("DT1", "country", iso, "rho_partial_income_urban", rho_p, len(g),
                           "youth literacy vs primary completion lagged 5y, partial on log income + urban"))
        details.append(det("DT1", "country", iso, "rho_raw", rho_r, len(g), "uncontrolled Spearman"))
        details.append(det("DT1", "country", iso, "n_country_years", len(g), len(g),
                           "years meeting the >=12-year eligibility rule"))
    if not per:
        return row("DT1", "income-partial association: youth literacy vs primary completion lagged 5y",
                   "no country meets the >=12-year eligibility rule", "", "median partial rho >= +0.40",
                   "DATA LIMITED", "positive", 0, 0, "DERIVED",
                   "SE.ADT.1524.LT.ZS(OBSERVED); SE.PRM.CMPT.ZS lag5(OBSERVED); NY.GDP.PCAP.KD(OBSERVED); SP.URB.TOTL.IN.ZS(OBSERVED)",
                   "no eligible country; block threshold unreachable"), details

    per = pd.DataFrame(per).sort_values("iso3").reset_index(drop=True)
    med_p = float(per.rho_partial.median())
    med_r = float(per.rho_raw.median())
    k = int((per.rho_partial >= DT1_RHO).sum())
    sign_retained = (med_r > 0) and (med_p > 0)
    if len(per) < 2:
        verdict, block_term = "DATA LIMITED", "positive"
    elif med_p >= DT1_RHO and sign_retained:
        verdict, block_term = "NON-NULL (positive)", "positive"
    else:
        verdict, block_term = "NULL (negative)", "negative"
    details.append(det("DT1", "headline", "eligible countries", "median_rho_partial", med_p, len(per),
                       f"range {per.rho_partial.min():+.4f}..{per.rho_partial.max():+.4f}"))
    details.append(det("DT1", "headline", "eligible countries", "median_rho_raw", med_r, len(per), ""))
    details.append(det("DT1", "headline", "eligible countries", "n_countries_rho_ge_0.40", k, len(per),
                       f"share {k/len(per):.4f} (secondary, non-verdict)"))
    stat = (f"median partial rho = {med_p:+.4f} (raw median {med_r:+.4f}); "
            f"{k}/{len(per)} countries >= +0.40")
    notes = (f"{len(per)} of 30 countries meet the >=12-year overlap rule; "
             "coverage is thin, but the block's per-country eligibility rule is met. "
             "Sign retained = median raw and partial both positive.")
    return row("DT1", "income-partial association: youth literacy vs primary completion lagged 5y",
               stat, med_p, "median partial rho >= +0.40 with sign retained", verdict, block_term,
               int(per.n.sum()), len(per), "DERIVED",
               "SE.ADT.1524.LT.ZS(OBSERVED); SE.PRM.CMPT.ZS lag5(OBSERVED); NY.GDP.PCAP.KD(OBSERVED); SP.URB.TOTL.IN.ZS(OBSERVED)",
               notes), details


# ----------------------------------------------------------------------------- DT2
def run_dt2(long: pd.DataFrame):
    dec = pd.read_csv(DATA_REL / "literacy_cohort_decomposition.csv")
    gdp = long[long.indicator == "NY.GDP.PCAP.KD"][["iso3", "year", "value"]].rename(
        columns={"value": "gdp"})
    dec = dec.merge(gdp, left_on=["iso3", "y1"], right_on=["iso3", "year"], how="left")
    dec["log_gdp"] = np.log(dec["gdp"].clip(lower=1e-3))

    r_d1 = fe_ols(dec, "dlit", ["E_entrant"], time="y1")
    r_m1 = fe_ols(dec, "dlit", ["E_entrant", "log_gdp"], time="y1")
    r_m2 = fe_ols(dec, "dlit", ["E_entrant", "gap0", "log_gdp"], time="y1")
    details = []
    for name, r, terms in [("D1_crosscheck", r_d1, ["E_entrant"]),
                           ("M1_income_control", r_m1, ["E_entrant", "log_gdp"]),
                           ("M2_joint_income_control", r_m2, ["E_entrant", "gap0", "log_gdp"])]:
        if "error" in r:
            details.append(det("DT2", "model", name, "error", r["error"], r.get("n", ""), "model not estimable"))
            continue
        details.append(det("DT2", "model", name, "n", r["n"], r["n"], ""))
        details.append(det("DT2", "model", name, "n_cty", r["n_cty"], r["n"], ""))
        details.append(det("DT2", "model", name, "within_r2", r["r2_within"], r["n"], ""))
        for t in terms:
            a = r["terms"][t]
            details.append(det("DT2", "model", name, f"coef_{t}", a["coef"], r["n"], ""))
            details.append(det("DT2", "model", name, f"se_{t}", a["se"], r["n"], ""))
            details.append(det("DT2", "model", name, f"p_{t}", a["p"], r["n"], ""))
    off = pd.read_csv(DATA_REL / "literacy_decomposition_regressions.csv")
    d1_on_disk = float(off.loc[off.test == "D1", "coef"].iloc[0])
    if "error" not in r_d1:
        details.append(det("DT2", "crosscheck", "on_disk_D1", "coef", d1_on_disk, 241,
                           "09_relations/data/literacy_decomposition_regressions.csv"))
        details.append(det("DT2", "crosscheck", "reproduced_D1", "abs_diff",
                           abs(r_d1["terms"]["E_entrant"]["coef"] - d1_on_disk), 241,
                           "reproduction check only; not a DT2 result"))

    if "error" in r_m2 or "error" in r_m1:
        err = r_m2.get("error", r_m1.get("error"))
        return row("DT2", "income-controlled entrant-share driver of adult-literacy change",
                   f"model not estimable: {err}", "", "E_entrant >= +1.0 & p<0.05; gap0 <= 0.5x E_entrant",
                   "DATA LIMITED", "support", r_m2.get("n", 0), r_m2.get("n_cty", 0), "DERIVED",
                   "literacy_cohort_decomposition.csv(DERIVED on-disk); NY.GDP.PCAP.KD(OBSERVED)",
                   "insufficient observations/countries for two-way FE"), details

    b_e = r_m2["terms"]["E_entrant"]["coef"]
    p_e = r_m2["terms"]["E_entrant"]["p"]
    b_g = r_m2["terms"]["gap0"]["coef"]
    ratio = b_g / b_e if b_e != 0 else float("nan")
    d1_coef = r_d1["terms"]["E_entrant"]["coef"] if "error" not in r_d1 else float("nan")
    cond_a = (b_e >= DT2_COEF_SUPPORT) and (p_e < 0.05)
    cond_b = b_g <= DT2_GAP_RATIO * b_e
    if b_e < DT2_COEF_FALSIFY or p_e >= 0.05:
        verdict, block_term = "NULL (falsifier)", "falsifier"
    elif cond_a and cond_b:
        verdict, block_term = "NON-NULL (support)", "support"
    elif b_g >= b_e:
        verdict, block_term = "NULL (falsifier)", "falsifier"
    else:
        verdict, block_term = "INDETERMINATE (support gap)", "support"
    stat = (f"M2: E_entrant b={b_e:+.4f} (p={p_e:.4g}); gap0 b={b_g:+.4f}; "
            f"gap0/E={ratio:+.3f}; M1 E_entrant b={r_m1['terms']['E_entrant']['coef']:+.4f}")
    notes = (f"(a)={'met' if cond_a else 'not met'}; (b)={'met' if cond_b else 'not met'}. "
             f"Cross-check D1 coefficient {d1_coef:+.6f} "
             f"vs on-disk {d1_on_disk:+.6f}. Cohort replacement is partly arithmetic; "
             "the discriminating part is income-controlled survival + gap0 subordination.")
    return row("DT2", "income-controlled entrant-share driver of adult-literacy change",
               stat, b_e, "E_entrant >= +1.0 & p<0.05; gap0 <= 0.5x E_entrant", verdict, block_term,
               r_m2["n"], r_m2["n_cty"], "DERIVED",
               "literacy_cohort_decomposition.csv(DERIVED on-disk); NY.GDP.PCAP.KD(OBSERVED)", notes), details


# ----------------------------------------------------------------------------- DT4
def run_dt4(long: pd.DataFrame):
    d = long[(long.year >= Y0) & (long.year <= Y1)]
    wide = pivot_long(d)
    need = ["SE.PRM.CMPT.ZS", "SE.PRM.DURS", "SE.SEC.DURS", "SE.ADT.LITR.ZS", "NY.GDP.PCAP.KD"]
    w = wide[["iso3", "year"] + need].copy()
    w["duration"] = w["SE.PRM.DURS"] + w["SE.SEC.DURS"]
    w["log_gdp"] = np.log(w["NY.GDP.PCAP.KD"].clip(lower=1e-3))
    means = w.groupby("iso3", sort=True).agg(
        cmpt=("SE.PRM.CMPT.ZS", "mean"), duration=("duration", "mean"),
        dur_primary=("SE.PRM.DURS", "mean"), lit=("SE.ADT.LITR.ZS", "mean"),
        log_inc=("log_gdp", "mean"), n_dur=("duration", "count"),
        n_lit=("SE.ADT.LITR.ZS", "count"), n_cmpt=("SE.PRM.CMPT.ZS", "count")).reset_index()
    means = means.dropna(subset=["cmpt", "duration", "lit", "log_inc"])
    means["z_cmpt"] = zscore(means["cmpt"])
    means["z_duration"] = zscore(means["duration"])
    means["depth"] = means["z_cmpt"] * means["z_duration"]
    means["depth_primary"] = (means["z_cmpt"] * zscore(means["dur_primary"]))
    means = means.sort_values("iso3").reset_index(drop=True)

    details = []
    lit = d[d.indicator == "SE.ADT.LITR.ZS"][["iso3", "year", "value"]].sort_values(["iso3", "year"])
    rev = {}
    for iso, g in lit.groupby("iso3", sort=True):
        g = g.sort_values("year")
        yrs = g.year.to_numpy()
        vals = g.value.to_numpy()
        deltas = [float(vals[i] - vals[i - 1]) for i in range(1, len(g)) if yrs[i] - yrs[i - 1] == 1]
        rev[iso] = {"n_delta": len(deltas), "n_rev": int(sum(x <= -DT4_DROP_PP for x in deltas)),
                    "min_delta": min(deltas) if deltas else float("nan")}

    def data_limited(msg):
        return row("DT4", "installation depth orders literacy after income; depth predicts persistence",
                   msg, "", "rho >= +0.40; top>=80% zero reversal; bottom>=40% >=1 reversal",
                   "DATA LIMITED", "support", len(means), len(means), "DERIVED",
                   "SE.PRM.CMPT.ZS(OBSERVED); SE.PRM.DURS+SE.SEC.DURS(OBSERVED); SE.ADT.LITR.ZS(OBSERVED); NY.GDP.PCAP.KD(OBSERVED)",
                   msg), details

    if len(means) < 10:
        return data_limited(f"cross-section n={len(means)} below the n=10 floor")

    rho = partial_spearman(means["lit"], means["depth"], [means["log_inc"]])
    rho_primary = partial_spearman(means["lit"], means["depth_primary"], [means["log_inc"]])
    med = float(means.depth.median())
    means["half"] = np.where(means.depth >= med, "top", "bottom")
    top = means[means.half == "top"]
    bot = means[means.half == "bottom"]

    def share(frame, predicate):
        elig = [i for i in frame.iso3 if rev.get(i, {}).get("n_delta", 0) > 0]
        if not elig:
            return float("nan"), 0
        return sum(1 for i in elig if predicate(rev[i]["n_rev"])) / len(elig), len(elig)

    top_zero, top_n = share(top, lambda k: k == 0)
    bot_rev, bot_n = share(bot, lambda k: k >= 1)
    if top_n < 5 or bot_n < 5:
        return data_limited(f"depth halves too small (top n={top_n}, bottom n={bot_n})")

    cond_a = rho >= DT4_RHO
    cond_b = (top_zero >= DT4_TOP_ZERO) and (bot_rev >= DT4_BOTTOM_REV)
    if cond_a and cond_b:
        verdict, block_term = "NON-NULL (support)", "support"
    else:
        verdict, block_term = "NULL (falsifier)", "falsifier"

    for _, r in means.iterrows():
        details.append(det("DT4", "country", r.iso3, "cmpt_mean_1995_2024", r.cmpt, int(r.n_cmpt), ""))
        details.append(det("DT4", "country", r.iso3, "duration_mean_total", r.duration, int(r.n_dur), ""))
        details.append(det("DT4", "country", r.iso3, "z_cmpt", r.z_cmpt, int(r.n_cmpt), ""))
        details.append(det("DT4", "country", r.iso3, "z_duration", r.z_duration, int(r.n_dur), ""))
        details.append(det("DT4", "country", r.iso3, "depth", r.depth, int(r.n_dur), ""))
        details.append(det("DT4", "country", r.iso3, "lit_mean_1995_2024", r.lit, int(r.n_lit), ""))
        details.append(det("DT4", "country", r.iso3, "reversal_events_ge3pp",
                           rev.get(r.iso3, {}).get("n_rev", 0), rev.get(r.iso3, {}).get("n_delta", 0),
                           "consecutive-year adult-literacy Delta <= -3.0 pp"))
        details.append(det("DT4", "country", r.iso3, "min_annual_delta",
                           rev.get(r.iso3, {}).get("min_delta", float("nan")),
                           rev.get(r.iso3, {}).get("n_delta", 0), ""))
        details.append(det("DT4", "country", r.iso3, "depth_half", r.half, "", ""))
    details.append(det("DT4", "headline", "cross-section", "partial_rho", rho, len(means), ""))
    details.append(det("DT4", "headline", "top half", "zero_reversal_share", top_zero, top_n, ""))
    details.append(det("DT4", "headline", "bottom half", "at_least_one_reversal_share", bot_rev, bot_n, ""))
    details.append(det("DT4", "sensitivity", "cross-section", "rho_primary_duration_only",
                       rho_primary, len(means), "primary-duration depth sensitivity; never verdict-changing"))
    details.append(det("DT4", "diagnostic", "cross-section", "corr_depth_vs_zcmpt",
                       float(np.corrcoef(means.depth, means.z_cmpt)[0, 1]), len(means),
                       "duration contributes little cross-country variation"))

    stat = (f"partial rho={rho:+.4f}; top-half zero-reversal {int(round(top_zero*top_n))}/{top_n} "
            f"({top_zero:.1%}); bottom-half >=1 reversal {int(round(bot_rev*bot_n))}/{bot_n} ({bot_rev:.1%})")
    notes = (f"n={len(means)} country cross-section; income-confounded and low power (Y1 lesson). "
             "Descriptive only, never a law. Primary-duration sensitivity: "
             f"rho={rho_primary:+.4f} (never verdict-changing).")
    return row("DT4", "installation depth orders literacy after income; depth predicts persistence",
               stat, rho, "rho >= +0.40; top>=80% zero reversal; bottom>=40% >=1 reversal", verdict,
               block_term, len(means), len(means), "DERIVED",
               "SE.PRM.CMPT.ZS(OBSERVED); SE.PRM.DURS+SE.SEC.DURS(OBSERVED); SE.ADT.LITR.ZS(OBSERVED); NY.GDP.PCAP.KD(OBSERVED)",
               notes), details


# ----------------------------------------------------------------------------- DT5
def run_dt5(long: pd.DataFrame):
    d = long[(long.year >= Y0) & (long.year <= Y1)]
    wide = pivot_long(d)
    lit = wide[["iso3", "year", "SE.ADT.LITR.ZS"]].dropna().sort_values(["iso3", "year"])
    lit_latest = lit.groupby("iso3", sort=True).tail(1).set_index("iso3")
    lit_latest = lit_latest[lit_latest.year >= 2015]

    up = wide[["iso3", "year", "SE.SEC.CUAT.UP.ZS"]].dropna().sort_values(["iso3", "year"])
    up_stats = {}
    for iso, g in up.groupby("iso3", sort=True):
        g = g.sort_values("year")
        vals = g["SE.SEC.CUAT.UP.ZS"].to_numpy(float)
        runmax = np.maximum.accumulate(vals)
        streak = 0
        sustained = False
        for i in range(len(vals)):
            if vals[i] <= runmax[i] - DT5_REV_PP:
                streak += 1
                if streak >= 2:
                    sustained = True
            else:
                streak = 0
        up_stats[iso] = {"max": float(g["SE.SEC.CUAT.UP.ZS"].max()),
                         "min": float(g["SE.SEC.CUAT.UP.ZS"].min()),
                         "last": float(g["SE.SEC.CUAT.UP.ZS"].iloc[-1]),
                         "last_year": int(g.year.iloc[-1]),
                         "n": int(len(g)), "sustained_5pp_reversal": bool(sustained)}

    inc = wide[["iso3", "year", "NY.GDP.PCAP.KD"]].dropna()
    inc_latest = inc.sort_values(["iso3", "year"]).groupby("iso3", sort=True).tail(1).set_index("iso3")
    cmp_ = wide[["iso3", "year", "SE.PRM.CMPT.ZS"]].dropna()
    cmp_latest = cmp_.sort_values(["iso3", "year"]).groupby("iso3", sort=True).tail(1).set_index("iso3")

    rows, details = [], []
    for iso in sorted(set(lit_latest.index) & set(up_stats)):
        lit_v = float(lit_latest.loc[iso, "SE.ADT.LITR.ZS"])
        uni = lit_v >= DT5_CEIL
        u = up_stats[iso]
        ceil = (u["max"] < DT5_CEIL) and (not u["sustained_5pp_reversal"])
        rows.append({"iso3": iso, "lit_latest": lit_v, "lit_year": int(lit_latest.loc[iso, "year"]),
                     "universalized": uni, "up_max": u["max"], "up_last": u["last"],
                     "up_last_year": u["last_year"], "sustained_rev": u["sustained_5pp_reversal"],
                     "ceiling_persistent": ceil, "both": uni and ceil})
    joint = pd.DataFrame(rows).sort_values("iso3").reset_index(drop=True)
    if len(joint) == 0:
        return row("DT5", "joint induced-competence + asymmetric-exit signature", "no country has both series",
                   "", "joint >= 50%; PHL residual z <= -1.0", "DATA LIMITED", "support", 0, 0, "DERIVED",
                   "SE.ADT.LITR.ZS(OBSERVED); SE.SEC.CUAT.UP.ZS(OBSERVED)", "denominator empty"), details

    joint_share = float(joint.both.mean())
    n = len(joint)

    # PHL cross-country check: upper-sec attainment ~ log income + primary completion
    reg = joint[["iso3"]].copy()
    reg["up"] = [up_stats[i]["last"] for i in reg.iso3]
    reg["log_inc"] = [float(np.log(max(inc_latest.loc[i, "NY.GDP.PCAP.KD"], 1e-3)))
                      if i in inc_latest.index else np.nan for i in reg.iso3]
    reg["cmpt"] = [float(cmp_latest.loc[i, "SE.PRM.CMPT.ZS"]) if i in cmp_latest.index else np.nan
                   for i in reg.iso3]
    reg = reg.dropna()
    phl_z = float("nan")
    if len(reg) >= 10 and "PHL" in set(reg.iso3):
        X = np.column_stack([np.ones(len(reg)), reg.log_inc.to_numpy(float), reg.cmpt.to_numpy(float)])
        y = reg.up.to_numpy(float)
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        resid = y - X @ beta
        sd = float(np.std(resid, ddof=X.shape[1]))
        phl_r = float(resid[list(reg.iso3).index("PHL")])
        phl_z = phl_r / sd if sd > 0 else float("nan")
        details.append(det("DT5", "regression", "up_attainment", "intercept", beta[0], len(reg), ""))
        details.append(det("DT5", "regression", "up_attainment", "coef_log_inc", beta[1], len(reg), ""))
        details.append(det("DT5", "regression", "up_attainment", "coef_primary_cmpt", beta[2], len(reg), ""))
        details.append(det("DT5", "regression", "up_attainment", "resid_sd", sd, len(reg), ""))
        details.append(det("DT5", "regression", "PHL", "residual", phl_r, len(reg), ""))
        details.append(det("DT5", "regression", "PHL", "residual_z", phl_z, len(reg),
                           "fixed operational cut: not explained iff z <= -1.0"))

    cond_joint = joint_share >= DT5_JOINT
    if math.isnan(phl_z):
        verdict, block_term = "DATA LIMITED", "support"
    else:
        phl_ok = bool(phl_z <= DT5_PHL_Z)
        verdict = "NON-NULL (support)" if (cond_joint and phl_ok) else "NULL (falsifier)"
        block_term = "support" if verdict.startswith("NON-NULL") else "falsifier"

    for _, r in joint.iterrows():
        details.append(det("DT5", "country", r.iso3, "lit_latest", r.lit_latest, "", f"year {r.lit_year}"))
        details.append(det("DT5", "country", r.iso3, "universalized_ge90", int(r.universalized), "", ""))
        details.append(det("DT5", "country", r.iso3, "up_attainment_max", r.up_max, "", ""))
        details.append(det("DT5", "country", r.iso3, "ceiling_persistent", int(r.ceiling_persistent), "",
                           f"sustained_5pp_reversal={r.sustained_rev}"))
        details.append(det("DT5", "country", r.iso3, "joint_signature", int(r.both), "", ""))
    details.append(det("DT5", "headline", "denominator", "joint_share", joint_share, n,
                       f"{int(joint.both.sum())}/{n} countries"))
    details.append(det("DT5", "headline", "denominator", "universalized_share", float(joint.universalized.mean()), n, ""))
    details.append(det("DT5", "headline", "denominator", "ceiling_persistent_share",
                       float(joint.ceiling_persistent.mean()), n, ""))

    # PHL universalization series corroboration (block names it; descriptive only)
    try:
        us = pd.read_csv(DATA_MASS / "UNIVERSALIZATION_SERIES.csv")
        phl_series = us[(us.iso3 == "PHL") & (us.indicator == "completion_upper_secondary")]["value"].dropna()
        if len(phl_series):
            details.append(det("DT5", "corroboration", "PHL", "completion_upper_secondary_peak",
                               float(phl_series.max()), len(phl_series),
                               "UNIVERSALIZATION_SERIES.csv; descriptive corroboration only"))
    except FileNotFoundError:
        pass

    stat = (f"joint signature {int(joint.both.sum())}/{n} = {joint_share:.1%}; "
            + ("PHL z=NA" if math.isnan(phl_z) else f"PHL z={phl_z:+.3f}"))
    notes = ("Near-circular at n~24-30 (D63 ceiling already known); weakest diagnostic. "
             "Does not re-score WT2/WT4 or reopen C1-C4."
             + (" PHL residual not estimable -> DATA LIMITED on the second condition."
                if math.isnan(phl_z) else ""))
    return row("DT5", "joint induced-competence + asymmetric-exit signature", stat, joint_share,
               "joint >= 50%; PHL residual z <= -1.0", verdict, block_term, n, n, "DERIVED",
               "SE.ADT.LITR.ZS(OBSERVED); SE.SEC.CUAT.UP.ZS(OBSERVED); NY.GDP.PCAP.KD(OBSERVED); SE.PRM.CMPT.ZS(OBSERVED)",
               notes), details


# ----------------------------------------------------------------------------- DT3 design-only
def run_dt3():
    r = row("DT3", "reform-associated behavioural shift (schedule-discipline syndrome)",
            "UNABLE - no behavioural/reform series on disk; design-only, no number produced", "",
            "behavioural shift >= 5% of within-series SD with pre-declared parallel-trends check",
            "UNABLE (HELD, design-only)", "UNABLE", "", "", "HELD",
            "reform/grade-discontinuity microdata matched to a behavioural outcome (HELD)",
            "Design-only: DiD/RD on a compulsory-schooling reform or grade discontinuity; behavioural outcome "
            "(punctuality, arrest/incarceration, evaluative orientation); pre-declared parallel-trends check. "
            "No data on disk; never fabricated. Drop-first per D103.")
    details = [det("DT3", "design_only", "n/a", "status", "HELD", "",
                   "no run; behavioural/reform series absent. Support iff reform-associated behavioural shift "
                   ">= 5% of within-series SD and survives a pre-declared parallel-trends check.")]
    return r, details


# ----------------------------------------------------------------------------- main
def main() -> int:
    long = load_long()
    results, details = [], []

    r, d = run_dt1(long); results.append(r); details.extend(d)
    r, d = run_dt2(long); results.append(r); details.extend(d)
    r, d = run_dt3(); results.append(r); details.extend(d)
    r, d = run_dt4(long); results.append(r); details.extend(d)
    r, d = run_dt5(long); results.append(r); details.extend(d)

    res = pd.DataFrame(results, columns=["test", "estimand", "statistic", "stat_value", "threshold",
                                         "verdict", "block_term", "n", "n_countries", "label",
                                         "components", "notes"])
    det = pd.DataFrame(details, columns=["test", "level", "unit", "metric", "value", "n", "note"])

    # Deterministic ordering and formatting: no timestamps, no RNG, fixed float precision.
    res = res.sort_values("test").reset_index(drop=True)
    det = det.reset_index(drop=True)
    res.to_csv(OUT / "RESULTS.csv", index=False, float_format="%.12g", lineterminator="\n")
    det.to_csv(OUT / "DETAIL.csv", index=False, float_format="%.12g", lineterminator="\n")

    print(res[["test", "statistic", "verdict", "n", "n_countries"]].to_string(index=False))
    print(f"\nwrote {OUT/'RESULTS.csv'} ({len(res)} rows) and {OUT/'DETAIL.csv'} ({len(det)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
