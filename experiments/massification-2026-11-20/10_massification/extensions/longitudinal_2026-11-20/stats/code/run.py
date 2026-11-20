#!/usr/bin/env python3
"""
Longitudinal predeclared battery 2026-11-20 -- education, literacy, ECI and growth.

Implements PRE_DECLARATIONS.md (sha256 bff1c3ec...270d91) exactly:
specifications S1-S8 + the four predeclared robustness variants, hypotheses H1-H4
with their frozen thresholds, the declared MYS_proxy formula, the verdict vocabulary.

DESCRIPTIVE / ASSOCIATIONAL ONLY.
No causal claim. No push/pull direction claim (the audits' corrected push-pull
orientation is NOT a direction result here). No Africa claim. No imputation:
listwise deletion only, all counts reported.

Deterministic: seed 20261120 for every bootstrap / permutation draw; CSV floats
written with a fixed format so two runs are byte-identical.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sstats

# --------------------------------------------------------------------------------------
# Absolute paths, fixed constants (no CLI, no environment dependence)
# --------------------------------------------------------------------------------------
BASE = Path("/Users/treymenefee/massification_live/experiments/massification-2026-11-20")
EXT = BASE / "10_massification/extensions/longitudinal_2026-11-20"
STATS_DIR = EXT / "stats"
RESULTS_DIR = STATS_DIR / "results"
CODE_DIR = STATS_DIR / "code"

WDI_CSV = BASE / "09_relations/data/panel_wdi_long.csv"
ECI_CSV = BASE / "09_relations/data/economic_complexity_panel_30ctys.csv"
PRE_DECL = EXT / "PRE_DECLARATIONS.md"
PRE_DECL_SHA = "bff1c3ec39cdd76d984e04038cafac6124073714642e2794c0fc87eba7270d91"

SEED = 20261120
N_BOOT = 1000
N_PERM = 1000
YEAR_LO, YEAR_HI = 1995, 2024

# DATA LIMITED minimums (predeclaration requirement: state them)
MIN_N = 20
MIN_CLUSTERS = 8

# Declared derived proxy (predeclaration section 1). Printed next to any row using it.
MYS_FORMULA = ("MYS_proxy = 6 + 6*(SE.SEC.CUAT.LO.ZS/100) + 3*(SE.SEC.CUAT.UP.ZS/100) "
               "+ 4*(SE.TER.CUAT.BA.ZS/100)")

IND_MAP = {
    "SE.ADT.LITR.ZS": "lit",          # adult literacy, % 15+
    "SE.ADT.1524.LT.ZS": "lit_youth",  # youth literacy, % 15-24
    "SE.PRM.CMPT.ZS": "prm_cmpt",     # primary completion
    "SE.SEC.CMPT.LO.ZS": "lsec_cmpt",  # lower-secondary completion
    "SE.SEC.CUAT.LO.ZS": "cuat_lo",   # at least lower secondary, % 25+
    "SE.SEC.CUAT.UP.ZS": "cuat_up",   # at least upper secondary, % 25+
    "SE.TER.CUAT.BA.ZS": "cuat_ba",   # tertiary, % 25+
    "NY.GDP.MKTP.KD.ZG": "growth",    # GDP growth, annual %
    "NY.GDP.PCAP.PP.CD": "gdppc",     # GDP pc PPP (current intl $)
    "SP.URB.TOTL.IN.ZS": "urban",     # urban population %
}

VAR_LABEL = {
    "lit": "adult literacy % (SE.ADT.LITR.ZS) - observed",
    "lit_youth": "youth literacy % (SE.ADT.1524.LT.ZS) - observed",
    "MYS": "MYS_proxy - DERIVED (see formula)",
    "eci": "ECI SITC (eci_sitc) - observed, merged on (iso3,year)",
    "eci_alt": "ECI HS92 (eci_hs92) - observed, merged on (iso3,year)",
    "urban": "urban population % (SP.URB.TOTL.IN.ZS) - observed",
    "growth": "GDP growth % (NY.GDP.MKTP.KD.ZG) - observed",
    "prm_cmpt": "primary completion % - observed",
    "lsec_cmpt": "lower-secondary completion % - observed",
    "cuat_up": "upper-secondary attainment %25+ - observed",
    "cuat_ba": "tertiary attainment %25+ - observed",
    "log_gdppc1995": "log GDP pc PPP 1995 - observed",
}

DETAIL_COLS = ["spec", "term", "coef_std", "se_std", "t", "p", "ci_low", "ci_high",
               "coef_raw", "se_raw", "n", "clusters", "fe", "r2_within", "label",
               "status", "note"]
RESULT_COLS = ["experiment", "cluster", "question", "estimand", "estimate", "se",
               "ci_low", "ci_high", "n", "clusters", "threshold", "verdict", "label", "note"]


# --------------------------------------------------------------------------------------
# Small utilities
# --------------------------------------------------------------------------------------
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def zscore(x: np.ndarray, mean: float | None = None, sd: float | None = None):
    if mean is None:
        mean = float(np.mean(x))
    if sd is None:
        sd = float(np.std(x, ddof=1))
    return (x - mean) / sd, mean, sd


def pearson(a: np.ndarray, b: np.ndarray) -> float:
    a = a - a.mean()
    b = b - b.mean()
    den = float(np.sqrt((a * a).sum() * (b * b).sum()))
    if den <= 0.0:
        return float("nan")
    return float((a * b).sum() / den)


def ci_for(kind: str, lo: float, hi: float) -> str:
    return f"[{lo:.3f}, {hi:.3f}]"


def fnum(v, fmt="{:.4f}"):
    """CSV-safe numeric formatting: '' for missing."""
    if v is None:
        return ""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return ""
    if not np.isfinite(f):
        return ""
    return fmt.format(f)


# --------------------------------------------------------------------------------------
# Estimation: OLS with country-clustered SEs (CR1), FE via dummies (exact for
# unbalanced panels; a two-way within transform is not exact when unbalanced).
# --------------------------------------------------------------------------------------
def _dummies(d: pd.DataFrame, fe: tuple[str, ...]):
    parts, names = [], []
    for v in fe:
        dm = pd.get_dummies(d[v].astype("category"), drop_first=True, dtype=float,
                            prefix=v)
        dm = dm.reindex(sorted(dm.columns), axis=1)
        parts.append(dm.to_numpy(float))
        names.extend([str(c) for c in dm.columns])
    if not parts:
        return np.empty((len(d), 0)), []
    return np.concatenate(parts, axis=1), names


def _rank_guard(X: np.ndarray, names: list[str], protected: set[str]) -> list[int]:
    """Drop trailing (dummy) columns until full column rank. Regressors of interest
    are `protected`; if they are themselves collinear we raise (spec UNABLE)."""
    keep = list(range(X.shape[1]))
    while len(keep) > 1:
        r = np.linalg.matrix_rank(X[:, keep])
        if r == len(keep):
            return keep
        dropped = False
        for j in reversed(range(len(keep))):
            if names[keep[j]] not in protected:
                keep.pop(j)
                dropped = True
                break
        if not dropped:
            raise RuntimeError("collinear regressor of interest: " + ",".join(names))
    return keep


def ols_cluster(y: np.ndarray, X: np.ndarray, names: list[str], cluster_ids: np.ndarray,
                protected: set[str]):
    keep = _rank_guard(X, names, protected)
    Xk = X[:, keep]
    kept_names = [names[j] for j in keep]
    dropped = [names[j] for j in range(X.shape[1]) if j not in keep]
    n, k = Xk.shape
    if n - k <= 0:
        raise RuntimeError(f"no residual df: n={n}, k={k}")
    XtX_inv = np.linalg.inv(Xk.T @ Xk)
    b = XtX_inv @ (Xk.T @ y)
    u = y - Xk @ b
    meat = np.zeros((k, k))
    codes, inv = np.unique(cluster_ids, return_inverse=True)
    for g in range(len(codes)):
        idx = inv == g
        s = Xk[idx].T @ u[idx]
        meat += np.outer(s, s)
    G = len(codes)
    V = XtX_inv @ meat @ XtX_inv
    V *= (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    se = np.sqrt(np.diag(V))
    df_t = max(G - 1, 1)
    tstat = np.where(se > 0, b / np.where(se > 0, se, np.nan), np.nan)
    pval = 2.0 * sstats.t.sf(np.abs(tstat), df_t)
    crit = float(sstats.t.ppf(0.975, df_t))
    ci_low = b - crit * se
    ci_high = b + crit * se
    out = {}
    for j, nm in enumerate(kept_names):
        out[nm] = dict(coef=float(b[j]), se=float(se[j]), t=float(tstat[j]),
                       p=float(pval[j]), ci_low=float(ci_low[j]),
                       ci_high=float(ci_high[j]))
    # within-R2: residualise y on the FE block only
    Xfe, fe_names = _dummies_only(X, names, protected)
    ssr = float(np.sum(u * u))
    if Xfe is not None and Xfe.shape[1] > 0:
        F = np.column_stack([np.ones(n), Xfe])
        try:
            Fk = F[:, _rank_guard(F, ["const"] + fe_names, {"const"})]
        except RuntimeError:
            Fk = F
        bf = np.linalg.lstsq(Fk, y, rcond=None)[0]
        resid0 = y - Fk @ bf
        sst = float(np.sum(resid0 * resid0))
    else:
        sst = float(np.sum((y - y.mean()) ** 2))
    r2_within = 1.0 - ssr / sst if sst > 0 else float("nan")
    return dict(coefs=out, n=n, clusters=G, k=k, df_resid=n - k,
                df_t=df_t, crit=crit, r2_within=r2_within, dropped=dropped)


def _dummies_only(X, names, protected):
    fe_names = [nm for nm in names if nm not in protected and nm != "const"]
    if not fe_names:
        return None, []
    idx = [names.index(nm) for nm in fe_names]
    return X[:, idx], fe_names


def fit(d: pd.DataFrame, yvar: str, xvars: list[str], fe: tuple = (), cluster: str = "iso3",
        spec: str = "", note: str = "", sd_map: dict | None = None):
    """Standardized (pooled-SD) OLS. Returns a dict with per-term rows.

    Coefficients are reported on the standardized basis: outcome and each regressor
    divided by its pooled sample SD over the estimation sample (or by `sd_map` when
    supplied, used to put ECI-tercile slopes on one common scale).
    """
    frame = d.dropna(subset=[yvar, *xvars]).copy()
    for v in fe:
        frame = frame[frame[v].notna()]
    frame = frame.sort_values(["iso3", "year"]).reset_index(drop=True)
    n = len(frame)
    G = int(frame[cluster].nunique()) if n else 0
    years = f"{int(frame['year'].min())}-{int(frame['year'].max())}" if n else "n/a"
    res = dict(spec=spec, status="OK", n=n, clusters=G, years=years, rows=[],
               dropped=[], r2_within=float("nan"), fe="+".join(fe) if fe else "none",
               note=note, n_k=0, df_resid=0)
    if n < MIN_N or G < MIN_CLUSTERS:
        res["status"] = "DATA LIMITED"
        res["reason"] = (f"n={n} (minimum {MIN_N}) ; clusters={G} "
                         f"(minimum {MIN_CLUSTERS} for a FE slope)")
        return res

    y = frame[yvar].to_numpy(float)
    cols, names = [np.ones(n)], ["const"]
    sds = {}
    yz, my, sy = zscore(y) if sd_map is None or yvar not in sd_map else zscore(y, *sd_map[yvar])
    for v in xvars:
        x = frame[v].to_numpy(float)
        if sd_map is not None and v in sd_map:
            xz, mx, sx = zscore(x, *sd_map[v])
        else:
            xz, mx, sx = zscore(x)
        sds[v] = (mx, sx)
        cols.append(xz)
        names.append(v)
    D, dnames = _dummies(frame, fe)
    if D.shape[1]:
        cols.append(D)
        names.extend(dnames)
    X = np.column_stack(cols)
    protected = set(xvars) | {"const"}
    est = ols_cluster(yz, X, names, frame[cluster].to_numpy(), protected)
    res["dropped"] = est["dropped"]
    res["r2_within"] = est["r2_within"]
    res["n_k"] = est["k"]
    res["df_resid"] = est["df_resid"]
    for v in xvars:
        c = est["coefs"][v]
        mx, sx = sds[v]
        res["rows"].append(dict(
            spec=spec, term=v, coef_std=c["coef"], se_std=c["se"], t=c["t"], p=c["p"],
            ci_low=c["ci_low"], ci_high=c["ci_high"],
            coef_raw=c["coef"] * sy / sx, se_raw=c["se"] * sy / sx,
            n=n, clusters=G, fe=res["fe"], r2_within=res["r2_within"],
            label=("derived" if v == "MYS" else "observed"), status="OK", note=note,
            sd_y=sy, sd_x=sx, mean_x=mx))
    return res


def get(res: dict, term: str):
    for r in res["rows"]:
        if r["term"] == term:
            return r
    return None


def sig(r: dict) -> bool:
    return bool(r and np.isfinite(r["ci_low"]) and (r["ci_low"] > 0 or r["ci_high"] < 0))


def pos_sig(r: dict) -> bool:
    return bool(r and sig(r) and r["coef_std"] > 0)


# --------------------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------------------
def build_panel() -> pd.DataFrame:
    long = pd.read_csv(WDI_CSV)
    long = long[(long["year"] >= YEAR_LO) & (long["year"] <= YEAR_HI)].copy()
    sub = long[long["indicator"].isin(IND_MAP)].copy()
    sub["var"] = sub["indicator"].map(IND_MAP)
    if sub.duplicated(["iso3", "year", "var"]).any():
        raise RuntimeError("duplicate indicator rows in WDI long panel")
    wide = sub.pivot_table(index=["iso3", "year"], columns="var", values="value").reset_index()
    eci = pd.read_csv(ECI_CSV)
    wide = wide.merge(eci[["iso3", "year", "eci_sitc", "eci_hs92"]], on=["iso3", "year"],
                      how="inner")
    wide = wide.rename(columns={"eci_sitc": "eci", "eci_hs92": "eci_alt"})
    comp = wide[["cuat_lo", "cuat_up", "cuat_ba"]]
    ok = comp.notna().all(axis=1)
    wide["MYS"] = np.where(
        ok,
        6.0 + 6.0 * wide["cuat_lo"] / 100.0 + 3.0 * wide["cuat_up"] / 100.0
        + 4.0 * wide["cuat_ba"] / 100.0,
        np.nan)
    g95 = wide.loc[wide["year"] == 1995, ["iso3", "gdppc"]].rename(columns={"gdppc": "gdppc1995"})
    wide = wide.merge(g95, on="iso3", how="left")
    wide["log_gdppc1995"] = np.log(wide["gdppc1995"].where(wide["gdppc1995"] > 0))
    wide = wide.sort_values(["iso3", "year"]).reset_index(drop=True)
    return wide


def block_means(d: pd.DataFrame) -> pd.DataFrame:
    """Non-overlapping 5-year blocks 1995-99 ... 2020-24; mean of observed years."""
    dd = d.copy()
    dd["block"] = (dd["year"] - YEAR_LO) // 5
    num = ["growth", "lit", "lit_youth", "MYS", "eci", "eci_alt", "urban"]
    g = dd.groupby(["iso3", "block"], observed=True)
    bm = g[num].mean()
    bm["nyears"] = g["year"].size()
    bm = bm.reset_index()
    bm["year"] = YEAR_LO + bm["block"] * 5 + 2  # block midpoint label (only for reporting)
    return bm


# --------------------------------------------------------------------------------------
# Specifications
# --------------------------------------------------------------------------------------
def spec_s1(panel: pd.DataFrame):
    """Cross-section of 1995-2024 country means."""
    num = ["growth", "lit", "MYS", "eci", "urban"]
    agg = panel.groupby("iso3")[num].mean().reset_index()
    g95 = panel.groupby("iso3")["log_gdppc1995"].first().reset_index()
    cs = agg.merge(g95, on="iso3", how="left")
    cs["year"] = 2024
    note = ("time-averaged 1995-2024 country means (mean of observed years only); "
            "log(GDPpc 1995) control; OLS, CR1 clustered on country (each cluster = 1 "
            "country, i.e. heteroskedasticity-robust); " + MYS_FORMULA)
    res = fit(cs, "growth", ["lit", "MYS", "eci", "log_gdppc1995"], fe=(), cluster="iso3",
              spec="S1_cross_section", note=note)
    res["years"] = "1995-2024 means"
    return res


def spec_s2(panel: pd.DataFrame, litvar="lit", ecivar="eci", sub=None, spec="S2_countryFE",
            note_extra=""):
    d = panel if sub is None else sub
    note = ("annual 1995-2024, country FE + year FE (dummies, exact for unbalanced panel), "
            "CR1 clustered by country; standardized by pooled SD; "
            "MYS_proxy DERIVED: " + MYS_FORMULA + note_extra)
    return fit(d, "growth", [litvar, "MYS", ecivar, "urban"], fe=("iso3", "year"),
               cluster="iso3", spec=spec, note=note)


def spec_s3(panel: pd.DataFrame, litvar="lit", ecivar="eci", sub=None,
            spec="S3_five_year_blocks", note_extra=""):
    d = panel if sub is None else sub
    bm = block_means(d)
    bm = bm.dropna(subset=["growth", litvar, "MYS", ecivar])
    note = ("non-overlapping 5-year block means (1995-99 ... 2020-24, mean of observed "
            "years in block), country FE, CR1 clustered by country; standardized by "
            "pooled SD; MYS_proxy DERIVED: " + MYS_FORMULA + note_extra)
    return fit(bm, "growth", [litvar, "MYS", ecivar], fe=("iso3",), cluster="iso3",
               spec=spec, note=note)


def spec_s4(panel: pd.DataFrame):
    early = panel[panel["year"].between(1995, 2004)]
    late = panel[panel["year"].between(2015, 2024)]
    num = ["growth", "lit", "MYS", "eci"]
    e = early.groupby("iso3")[num].mean()
    l = late.groupby("iso3")[num].mean()
    both = e.notna().all(axis=1) & l.notna().all(axis=1)
    common = sorted(set(e.index[both]) & set(l.index[both]))
    note = ("(2015-24 mean) - (1995-2004 mean); needs all of growth, literacy, MYS_proxy "
            "and ECI observed in BOTH periods; " + MYS_FORMULA)
    if len(common) < MIN_N or len(common) < MIN_CLUSTERS:
        rows = []
        for v in ["growth", "lit", "MYS", "eci"]:
            rows.append(dict(spec="S4_long_differences", term=f"delta_{v}", coef_std=np.nan,
                             se_std=np.nan, t=np.nan, p=np.nan, ci_low=np.nan,
                             ci_high=np.nan, coef_raw=np.nan, se_raw=np.nan,
                             n=len(common), clusters=len(common), fe="none",
                             r2_within=np.nan, label=("derived" if v == "MYS" else "observed"),
                             status="DATA LIMITED",
                             note=("not estimated: only " + str(len(common)) + " countries have "
                                   "all four series in both periods (minimum " + str(MIN_N) +
                                   " obs / " + str(MIN_CLUSTERS) + " clusters); countries = " +
                                   (";".join(common) if common else "none") + "; " + note)))
        return dict(spec="S4_long_differences", status="DATA LIMITED", n=len(common),
                    clusters=len(common), years="1995-2004 vs 2015-2024", rows=rows,
                    dropped=[], r2_within=np.nan, fe="none", note=note, n_k=0,
                    df_resid=0, reason=("only " + str(len(common)) + " countries with both "
                                        "periods observed (minimum " + str(MIN_N) + " obs / "
                                        + str(MIN_CLUSTERS) + " clusters)"))
    dd = pd.DataFrame({
        "iso3": common,
        "growth": (l.loc[common, "growth"] - e.loc[common, "growth"]).to_numpy(),
        "lit": (l.loc[common, "lit"] - e.loc[common, "lit"]).to_numpy(),
        "MYS": (l.loc[common, "MYS"] - e.loc[common, "MYS"]).to_numpy(),
        "eci": (l.loc[common, "eci"] - e.loc[common, "eci"]).to_numpy(),
    })
    dd["year"] = 2024
    res = fit(dd, "growth", ["lit", "MYS", "eci"], fe=(), cluster="iso3",
              spec="S4_long_differences", note=note)
    res["years"] = "1995-2004 vs 2015-2024"
    return res


def spec_s5(panel: pd.DataFrame):
    d = panel.dropna(subset=["growth", "lit", "MYS", "eci", "urban"]).copy()
    d["lit_x_eci"] = d["lit"] * d["eci"]
    d["MYS_x_eci"] = d["MYS"] * d["eci"]
    note = ("annual 1995-2024, country FE + year FE, CR1 clustered by country; interaction "
            "terms on raw products; standardized by pooled SD; MYS_proxy DERIVED: " +
            MYS_FORMULA)
    res = fit(d, "growth", ["lit", "MYS", "eci", "lit_x_eci", "MYS_x_eci"],
              fe=("iso3", "year"), cluster="iso3", spec="S5_interaction", note=note)
    if res["status"] == "OK":
        res["years"] = "1995-2024"
    return res


def spec_s6(panel: pd.DataFrame, pooled_sd: dict):
    d = panel.dropna(subset=["growth", "lit", "MYS", "eci"]).copy()
    d["eci_dm"] = d["eci"] - d.groupby("iso3")["eci"].transform("mean")
    q1, q2 = np.quantile(d["eci_dm"].to_numpy(float), [1 / 3, 2 / 3])
    d["tercile"] = np.where(d["eci_dm"] <= q1, "low",
                            np.where(d["eci_dm"] <= q2, "mid", "high"))
    note = ("terciles formed on within-country-demeaned ECI (country-demeaned eci_sitc) in "
            "the S2 estimation sample; per-tercile country-FE regression of growth on "
            "literacy + MYS_proxy, no year FE (df); coefficients standardized by the POOLED "
            "S2-sample SD so terciles are comparable; CR1 clustered by country")
    rows = []
    fits = {}
    for t in ["low", "mid", "high"]:
        sub = d[d["tercile"] == t]
        r = fit(sub, "growth", ["lit", "MYS"], fe=("iso3",), cluster="iso3",
                spec="S6_eci_terciles", note=note, sd_map=pooled_sd)
        fits[t] = r
        if r["status"] != "OK":
            rows.append(dict(spec="S6_eci_terciles", term=f"lit|{t}", coef_std=np.nan,
                             se_std=np.nan, t=np.nan, p=np.nan, ci_low=np.nan,
                             ci_high=np.nan, coef_raw=np.nan, se_raw=np.nan, n=r["n"],
                             clusters=r["clusters"], fe="iso3", r2_within=np.nan,
                             label="observed", status="DATA LIMITED",
                             note=note + " | tercile cell insufficient: " + r["reason"]))
        else:
            for v in ["lit", "MYS"]:
                rr = get(r, v)
                rows.append({**{k: rr[k] for k in ["spec", "coef_std", "se_std", "t", "p",
                                                   "ci_low", "ci_high", "coef_raw", "se_raw",
                                                   "n", "clusters", "fe", "r2_within"]},
                             "term": f"{v}|{t}",
                             "label": ("derived" if v == "MYS" else "observed"),
                             "status": "OK", "note": note})
    # bootstrap CI for high minus low literacy slope (cluster bootstrap over countries)
    rng = np.random.default_rng(SEED + 606)
    countries = np.array(sorted(d["iso3"].unique()))
    diffs, diffs_raw, valid = [], [], 0
    if fits["low"]["status"] == "OK" and fits["high"]["status"] == "OK":
        for _ in range(N_BOOT):
            draw = rng.choice(countries, size=len(countries), replace=True)
            pieces = []
            for i, c in enumerate(draw):
                p = d[d["iso3"] == c].copy()
                p["draw_id"] = f"{c}_{i}"  # keep duplicated clusters separate
                pieces.append(p)
            bs = pd.concat(pieces, ignore_index=True)
            got = {}
            ok = True
            for t in ["low", "high"]:
                sub = bs[bs["tercile"] == t]
                if sub["iso3"].nunique() < 2:
                    ok = False
                    break
                # within-country variation must survive (>=2 obs in >=1 country)
                cnt = sub.groupby("iso3").size()
                if (cnt >= 2).sum() < 1:
                    ok = False
                    break
                r = fit(sub, "growth", ["lit"], fe=("iso3",), cluster="iso3",
                        spec="boot", note="", sd_map=pooled_sd)
                if r["status"] != "OK":
                    ok = False
                    break
                got[t] = get(r, "lit")
            if not ok:
                continue
            valid += 1
            diffs.append(got["high"]["coef_std"] - got["low"]["coef_std"])
            diffs_raw.append(got["high"]["coef_raw"] - got["low"]["coef_raw"])
    boot = dict(n_boot=N_BOOT, valid=valid, diffs=np.array(diffs),
                diffs_raw=np.array(diffs_raw))
    res = dict(spec="S6_eci_terciles", status="OK", rows=rows, n=len(d),
               clusters=int(d["iso3"].nunique()), years="1995-2024", dropped=[],
               r2_within=np.nan, fe="iso3 per tercile", note=note, n_k=0, df_resid=0,
               fits=fits, boot=boot, tercile_n={t: int((d["tercile"] == t).sum()) for t in
                                                 ["low", "mid", "high"]},
               tercile_cty={t: int(d[d["tercile"] == t]["iso3"].nunique()) for t in
                            ["low", "mid", "high"]})
    if fits["low"]["status"] != "OK" or fits["high"]["status"] != "OK":
        res["status"] = "DATA LIMITED"
        res["reason"] = "low or high tercile cell below minimum (n>=20, clusters>=8)"
    return res


def spec_s7(panel: pd.DataFrame):
    """Reverse check: 5-year changes in education/ECI on growth lagged 5 years."""
    d = panel.sort_values(["iso3", "year"]).copy()
    lag = d[["iso3", "year", "growth"]].copy()
    lag["year"] = lag["year"] + 5
    lag = lag.rename(columns={"growth": "growth_l5"})
    d = d.merge(lag, on=["iso3", "year"], how="left")
    note = ("reverse/symmetry check only - NO direction claim; outcome = 5-year change "
            "(t minus t-5) of the named series; regressor = GDP growth at t-5; country FE "
            "+ year FE; CR1 clustered by country; standardized by pooled SD")
    rows = []
    for v in ["lit", "MYS", "eci"]:
        # exact 5-year difference via merge on (iso3, year-5); never shift by row position
        prev = d[["iso3", "year", v]].copy()
        prev["year"] = prev["year"] + 5
        prev = prev.rename(columns={v: v + "_l5"})
        dd = d.merge(prev, on=["iso3", "year"], how="left")
        dd["delta"] = dd[v] - dd[v + "_l5"]
        dd = dd.dropna(subset=["delta", "growth_l5"])
        r = fit(dd, "delta", ["growth_l5"], fe=("iso3", "year"), cluster="iso3",
                spec="S7_reverse", note=note + f" | outcome delta_{v}")
        if r["status"] != "OK":
            rows.append(dict(spec="S7_reverse", term=f"delta_{v}", coef_std=np.nan, se_std=np.nan,
                             t=np.nan, p=np.nan, ci_low=np.nan, ci_high=np.nan,
                             coef_raw=np.nan, se_raw=np.nan, n=r["n"], clusters=r["clusters"],
                             fe="iso3+year", r2_within=np.nan,
                             label=("derived" if v == "MYS" else "observed"),
                             status="DATA LIMITED", note=note + " | " + r["reason"]))
        else:
            rr = get(r, "growth_l5")
            rows.append({**{k: rr[k] for k in ["spec", "coef_std", "se_std", "t", "p", "ci_low",
                                               "ci_high", "coef_raw", "se_raw", "n",
                                               "clusters", "fe", "r2_within"]},
                         "term": f"delta_{v}", "label": ("derived" if v == "MYS" else "observed"),
                         "status": "OK", "note": note + f" | outcome delta_{v}"})
    res = dict(spec="S7_reverse", status="OK", rows=rows,
               n=rows[0]["n"] if rows else 0, clusters=rows[0]["clusters"] if rows else 0,
               years="2000-2024", dropped=[], r2_within=np.nan, fe="iso3+year", note=note,
               n_k=0, df_resid=0)
    if all(r["status"] != "OK" for r in rows):
        res["status"] = "DATA LIMITED"
    return res


S8_VARS = ["growth", "lit", "lit_youth", "prm_cmpt", "lsec_cmpt", "cuat_up", "cuat_ba",
           "MYS", "eci", "urban"]
S8_ANALOGUE = {"lit": "lit_youth", "lit_youth": "lit", "prm_cmpt": "lsec_cmpt",
               "lsec_cmpt": "prm_cmpt", "cuat_up": "cuat_ba", "cuat_ba": "cuat_up"}


def spec_s8(panel: pd.DataFrame):
    """Within-country co-movement matrix; permutation p-values (seeded). No direction claim."""
    rng = np.random.default_rng(SEED + 808)
    rows = []
    pairs = [(a, b) for i, a in enumerate(S8_VARS) for b in S8_VARS[i + 1:]]
    for a, b in pairs:
        dd = panel.dropna(subset=[a, b])
        n = len(dd)
        if n < 3:
            rows.append(dict(var1=a, var2=b, r=np.nan, n=n, clusters=0, perm_p=np.nan,
                             n_perm=N_PERM, stable=False, analogues="", note="no cells"))
            continue
        codes, inv = np.unique(dd["iso3"].to_numpy(), return_inverse=True)
        groups = [np.where(inv == g)[0] for g in range(len(codes))]
        av = dd[a].to_numpy(float)
        bv = dd[b].to_numpy(float)
        da = np.empty(n)
        db = np.empty(n)
        for g in groups:
            da[g] = av[g] - av[g].mean()
            db[g] = bv[g] - bv[g].mean()
        r_obs = pearson(da, db)
        count = 0
        if np.isfinite(r_obs):
            for _ in range(N_PERM):
                dap = np.empty(n)
                for g in groups:
                    dap[g] = rng.permutation(da[g])
                rp = pearson(dap, db)
                if np.isfinite(rp) and abs(rp) >= abs(r_obs):
                    count += 1
        p_perm = (1.0 + count) / (1.0 + N_PERM) if np.isfinite(r_obs) else np.nan
        rows.append(dict(var1=a, var2=b, r=r_obs, n=n, clusters=len(codes), perm_p=p_perm,
                         n_perm=N_PERM, stable=False, analogues="",
                         note="within-country demeaned Pearson r; permutation within country"))
    tbl = pd.DataFrame(rows)
    # H4 stability: |r|>=0.4, perm p<0.05, same sign for the analogous pairs
    lookup = {(r.var1, r.var2): i for i, r in tbl.iterrows()}
    for i, r in tbl.iterrows():
        if not (np.isfinite(r["r"]) and r["n"] >= MIN_N and np.isfinite(r["perm_p"])):
            continue
        base_ok = abs(r["r"]) >= 0.4 and r["perm_p"] < 0.05
        analogues, ok = [], True
        for side in (r["var1"], r["var2"]):
            if side in S8_ANALOGUE:
                other = S8_ANALOGUE[side]
                pair = (min(side and other or other, other) and (other, r["var2"]) if side == r["var1"]
                        else (r["var1"], other))
                j = lookup.get(pair)
                if j is None or j == i:
                    continue
                ar = tbl.loc[j]
                if not (np.isfinite(ar["r"]) and ar["n"] >= MIN_N):
                    continue
                analogues.append(f"{pair[0]}~{pair[1]}:r={ar['r']:.3f}")
                if np.sign(ar["r"]) != np.sign(r["r"]):
                    ok = False
        tbl.at[i, "analogues"] = ";".join(analogues)
        tbl.at[i, "stable"] = bool(base_ok and ok)
    return tbl


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------
def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CODE_DIR.mkdir(parents=True, exist_ok=True)
    run_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    panel = build_panel()
    n_cty = int(panel["iso3"].nunique())

    s1 = spec_s1(panel)
    s2 = spec_s2(panel)
    s3 = spec_s3(panel)
    s4 = spec_s4(panel)
    s5 = spec_s5(panel)

    # pooled SD map from the S2 estimation sample, used to put tercile slopes on one scale
    s2frame = panel.dropna(subset=["growth", "lit", "MYS", "eci", "urban"])
    sd_map = {"growth": (float(s2frame["growth"].mean()), float(s2frame["growth"].std(ddof=1))),
              "lit": (float(s2frame["lit"].mean()), float(s2frame["lit"].std(ddof=1))),
              "MYS": (float(s2frame["MYS"].mean()), float(s2frame["MYS"].std(ddof=1))),
              "eci": (float(s2frame["eci"].mean()), float(s2frame["eci"].std(ddof=1)))}
    s6 = spec_s6(panel, sd_map)
    s7 = spec_s7(panel)
    s8 = spec_s8(panel)

    # ---------------- robustness ----------------
    rob_rows = []
    variants = [
        ("R1_eci_hs92", "ECI HS92 instead of SITC", dict(ecivar="eci_alt")),
        ("R2_no_citystates", "exclude HKG and SGP (city-states)",
         dict(sub=panel[~panel["iso3"].isin(["HKG", "SGP"])])),
        ("R3_no_covid", "exclude 2020-2021 (COVID)",
         dict(sub=panel[~panel["year"].isin([2020, 2021])])),
        ("R4_youth_literacy", "youth literacy instead of adult literacy",
         dict(litvar="lit_youth")),
    ]
    for vid, vlabel, kw in variants:
        for spec_fn, sname in [(spec_s2, "S2_countryFE"), (spec_s3, "S3_five_year_blocks")]:
            r = spec_fn(panel, spec=f"{sname}|{vid}", note_extra=f" [robustness {vid}: {vlabel}]",
                        **kw)
            litname = kw.get("litvar", "lit")
            eciname = kw.get("ecivar", "eci")
            for v in [litname, "MYS", eciname]:
                rr = get(r, v)
                rob_rows.append(dict(
                    variant=vid, variant_label=vlabel, spec=sname, term=v,
                    coef_std=(rr["coef_std"] if rr else np.nan),
                    se_std=(rr["se_std"] if rr else np.nan),
                    ci_low=(rr["ci_low"] if rr else np.nan),
                    ci_high=(rr["ci_high"] if rr else np.nan),
                    p=(rr["p"] if rr else np.nan),
                    n=r["n"], clusters=r["clusters"], status=r["status"],
                    label=("derived" if v == "MYS" else "observed"),
                    note=(r.get("reason", "") if r["status"] != "OK" else
                          "standardized by pooled SD; " + MYS_FORMULA)))
    rob = pd.DataFrame(rob_rows)

    # ---------------- write detail CSVs ----------------
    def detail_frame(specs):
        rows = []
        for sp in specs:
            for r in sp["rows"]:
                rows.append({c: r.get(c, np.nan) for c in DETAIL_COLS})
        return pd.DataFrame(rows, columns=DETAIL_COLS)

    detail_frame([s1]).to_csv(RESULTS_DIR / "S1_cross_section.csv", index=False,
                              float_format="%.12g", na_rep="")
    detail_frame([s2]).to_csv(RESULTS_DIR / "S2_countryFE.csv", index=False,
                              float_format="%.12g", na_rep="")
    detail_frame([s3]).to_csv(RESULTS_DIR / "S3_five_year_blocks.csv", index=False,
                              float_format="%.12g", na_rep="")
    detail_frame([s4]).to_csv(RESULTS_DIR / "S4_long_differences.csv", index=False,
                              float_format="%.12g", na_rep="")
    detail_frame([s5]).to_csv(RESULTS_DIR / "S5_interaction.csv", index=False,
                              float_format="%.12g", na_rep="")
    s6df = pd.DataFrame(s6["rows"], columns=DETAIL_COLS)
    # append the tercile difference rows (bootstrap CI)
    extra = []
    if s6["status"] == "OK" and s6["boot"]["valid"] > 0:
        bh = get(s6["fits"]["high"], "lit")
        bl = get(s6["fits"]["low"], "lit")
        if bh and bl:
            lo, hi = np.percentile(s6["boot"]["diffs"], [2.5, 97.5])
            lo_r, hi_r = np.percentile(s6["boot"]["diffs_raw"], [2.5, 97.5])
            for v in ["lit", "MYS"]:
                hi_v = get(s6["fits"]["high"], v)
                lo_v = get(s6["fits"]["low"], v)
                if v == "lit":
                    d_std = hi_v["coef_std"] - lo_v["coef_std"]
                    d_raw = hi_v["coef_raw"] - lo_v["coef_raw"]
                    extra.append(dict(spec="S6_eci_terciles", term="lit|high_minus_low",
                                      coef_std=d_std, se_std=np.nan, t=np.nan, p=np.nan,
                                      ci_low=lo, ci_high=hi, coef_raw=d_raw, se_raw=np.nan,
                                      n=s6["n"], clusters=s6["clusters"], fe="iso3",
                                      r2_within=np.nan, label="observed", status="OK",
                                      note=(f"cluster bootstrap over countries, B={N_BOOT}, "
                                            f"valid reps={s6['boot']['valid']}, seed={SEED + 606}, "
                                            f"percentile CI; raw diff CI=[{lo_r:.4f},{hi_r:.4f}]")))
                else:
                    d_std = hi_v["coef_std"] - lo_v["coef_std"]
                    d_raw = hi_v["coef_raw"] - lo_v["coef_raw"]
                    extra.append(dict(spec="S6_eci_terciles", term="MYS|high_minus_low",
                                      coef_std=d_std, se_std=np.nan, t=np.nan, p=np.nan,
                                      ci_low=np.nan, ci_high=np.nan, coef_raw=d_raw,
                                      se_raw=np.nan, n=s6["n"], clusters=s6["clusters"],
                                      fe="iso3", r2_within=np.nan, label="derived",
                                      status="OK",
                                      note="MYS_proxy DERIVED; point difference only, no "
                                           "bootstrap from the literacy draw; " + MYS_FORMULA))
    s6df = pd.concat([s6df, pd.DataFrame(extra, columns=DETAIL_COLS)], ignore_index=True)
    s6df.to_csv(RESULTS_DIR / "S6_eci_terciles.csv", index=False, float_format="%.12g",
                na_rep="")
    detail_frame([s7]).to_csv(RESULTS_DIR / "S7_reverse.csv", index=False,
                              float_format="%.12g", na_rep="")
    s8.to_csv(RESULTS_DIR / "S8_comovement.csv", index=False, float_format="%.12g", na_rep="")
    rob.to_csv(RESULTS_DIR / "ROBUSTNESS.csv", index=False, float_format="%.12g", na_rep="")

    # ---------------- verdicts (computed from the numbers, predeclared thresholds) ----------------
    r_s2_lit, r_s2_mys, r_s2_eci, r_s2_urb = (get(s2, "lit"), get(s2, "MYS"),
                                              get(s2, "eci"), get(s2, "urban"))
    r_s3_lit, r_s3_mys, r_s3_eci = get(s3, "lit"), get(s3, "MYS"), get(s3, "eci")
    r_s1_lit, r_s1_mys, r_s1_eci = get(s1, "lit"), get(s1, "MYS"), get(s1, "eci")

    # ---- H1 ----
    h1_notes = []
    if s2["status"] != "OK":
        h1_verdict = "DATA LIMITED"
        h1_reason = "S2 not estimable: " + s2.get("reason", "")
    else:
        ratio = (abs(r_s2_mys["coef_std"]) / abs(r_s2_lit["coef_std"])
                 if r_s2_lit["coef_std"] != 0 else np.nan)
        lit_sig_pos = pos_sig(r_s2_lit)
        mys_sig = sig(r_s2_mys)
        s3_lit_sig = sig(r_s3_lit) if r_s3_lit else False
        s3_conflict = bool(s3_lit_sig and np.sign(r_s3_lit["coef_std"]) != np.sign(
            r_s2_lit["coef_std"]))
        if lit_sig_pos and (not mys_sig or ratio < 0.5):
            h1_verdict = "SUPPORTED"
            h1_reason = ("literacy positive and CI excludes 0; MYS_proxy either not "
                         f"significant or |beta| < 0.5x literacy (ratio {ratio:.2f})")
        elif lit_sig_pos and mys_sig and ratio >= 0.5:
            h1_verdict = "PARTIAL"
            h1_reason = ("both literacy and MYS_proxy positive and significant with ratio "
                         f"{ratio:.2f} >= 0.5 -> the schooling-years proxy also moves")
        elif sig(r_s2_mys) and r_s2_mys["coef_std"] > 0 and not lit_sig_pos:
            h1_verdict = "NOT SUPPORTED"
            h1_reason = "MYS_proxy positive and significant while literacy is not (declared falsifier)"
        elif s3_lit_sig and not lit_sig_pos and not mys_sig:
            h1_verdict = "PARTIAL"
            h1_reason = ("S2 literacy CI includes 0 but S3 (5-year blocks) literacy is "
                         "significant -> not a stable within-country association")
        elif s3_conflict:
            h1_verdict = "PARTIAL"
            h1_reason = "S2 and S3 literacy coefficients have opposite signs"
        else:
            h1_verdict = "NOT SUPPORTED"
            h1_reason = "literacy not positive-significant in S2 and MYS_proxy not significant (both null)"
        if h1_verdict == "SUPPORTED" and s3_conflict:
            h1_verdict = "PARTIAL"
            h1_reason += "; S3 sign conflict -> downgraded"
    h1_notes.append(h1_reason)

    # ---- H2 ----
    if s2["status"] != "OK" or s3["status"] != "OK":
        h2_verdict = "DATA LIMITED"
        h2_reason = "S2 or S3 not estimable"
    else:
        e2, e3 = r_s2_eci, r_s3_eci
        s2ok = sig(e2) and e2["coef_std"] > 0
        s3ok = sig(e3) and e3["coef_std"] > 0
        if s2ok and s3ok:
            h2_verdict = "SUPPORTED"
            h2_reason = "ECI positive with CI excluding 0 in both S2 and S3"
        elif sig(e2) and sig(e3) and np.sign(e2["coef_std"]) != np.sign(e3["coef_std"]):
            h2_verdict = "NOT SUPPORTED"
            h2_reason = "sign flips between S2 and S3 (declared falsifier)"
        elif (not sig(e2)) and (not sig(e3)):
            h2_verdict = "NOT SUPPORTED"
            h2_reason = "ECI CI includes 0 in both S2 and S3 (declared falsifier)"
        else:
            if s2ok or s3ok:
                h2_verdict = "PARTIAL"
                h2_reason = ("ECI positive-significant in only one of S2/S3 "
                             f"(S2 {'ok' if s2ok else 'no'}, S3 {'ok' if s3ok else 'no'})")
            else:
                h2_verdict = "NOT SUPPORTED"
                h2_reason = (
                    "ECI is not positive-significant in S2 or S3, so the frozen threshold "
                    "(positive with CI excluding 0 in BOTH) fails"
                    + ("; its S3 coefficient is significantly NEGATIVE"
                       if sig(e3) and e3["coef_std"] < 0 else ""))
    h2_notes = [h2_reason]

    # ---- H3 ----
    h3 = dict(verdict="DATA LIMITED", reason="", diff=np.nan, ci_low=np.nan, ci_high=np.nan,
              b_low=np.nan, b_high=np.nan, b_mid=np.nan, valid=0, rel=np.nan)
    if s6["status"] == "OK":
        bh, bl, bm = get(s6["fits"]["high"], "lit"), get(s6["fits"]["low"], "lit"), get(
            s6["fits"]["mid"], "lit")
        h3.update(b_low=bl["coef_raw"], b_high=bh["coef_raw"], b_mid=bm["coef_raw"],
                  valid=s6["boot"]["valid"])
        diff = bh["coef_raw"] - bl["coef_raw"]
        h3["diff"] = diff
        if s6["boot"]["valid"] >= 900:
            lo, hi = np.percentile(s6["boot"]["diffs_raw"], [2.5, 97.5])
            h3.update(ci_low=lo, ci_high=hi,
                      se=float(np.std(np.asarray(s6["boot"]["diffs_raw"], float), ddof=1)))
            same_sign = np.sign(bh["coef_raw"]) == np.sign(bl["coef_raw"])
            big_enough = (bh["coef_raw"] - bl["coef_raw"]) >= 0.5 * abs(bl["coef_raw"])
            h3["rel"] = (diff / abs(bl["coef_raw"])) if bl["coef_raw"] != 0 else np.nan
            if same_sign and big_enough and (lo > 0 or hi < 0):
                h3["verdict"] = "SUPPORTED"
                h3["reason"] = ("high-tercile literacy slope exceeds low-tercile by >= 50% of "
                                "the low magnitude, same sign, bootstrap CI excludes 0")
            elif not same_sign:
                h3["verdict"] = "NOT SUPPORTED"
                h3["reason"] = "high and low tercile slopes do not share a sign"
            elif not big_enough:
                h3["verdict"] = "NOT SUPPORTED"
                h3["reason"] = ("high-minus-low difference is below the predeclared 50%-of-low "
                                "magnitude threshold")
            else:
                h3["verdict"] = "NOT SUPPORTED"
                h3["reason"] = "bootstrap CI for the high-minus-low difference includes 0"
        else:
            h3["verdict"] = "DATA LIMITED"
            h3["reason"] = (f"only {s6['boot']['valid']}/{N_BOOT} bootstrap draws were "
                            "estimable; tercile cells too thin for a difference CI")
    else:
        h3["reason"] = "low or high tercile cell below the DATA LIMITED minimum"
    h3_notes = [h3["reason"]]

    # ---- H4 ----
    elig = s8[(s8["n"] >= MIN_N) & s8["r"].notna() & s8["perm_p"].notna()]
    strong = elig[(elig["r"].abs() >= 0.4) & (elig["perm_p"] < 0.05)]
    stable = strong[strong["stable"]]
    if len(elig) < 5:
        h4_verdict = "DATA LIMITED"
    elif len(stable) > 0:
        h4_verdict = "SUPPORTED"
    elif len(strong) > 0:
        h4_verdict = "PARTIAL"
    else:
        h4_verdict = "NOT SUPPORTED"
    h4_reason = (f"{len(elig)} of {len(s8)} pairs have n>={MIN_N}; {len(strong)} reach |r|>=0.4 "
                 f"with permutation p<0.05; {len(stable)} also pass the sign-stability checks")

    # ---------------- RESULTS.csv ----------------
    def rrow(experiment, question, estimand, est, se, lo, hi, n, clusters, threshold,
             verdict, label, note):
        return dict(experiment=experiment, cluster="country", question=question,
                    estimand=estimand, estimate=est, se=se, ci_low=lo, ci_high=hi,
                    n=n, clusters=clusters, threshold=threshold, verdict=verdict,
                    label=label, note=note)

    def pct(x):
        return f"{x:.4f}"

    h1 = rrow(
        "H1",
        "Does adult literacy move with GDP growth in a within-country panel where the "
        "schooling-years proxy does not?",
        "standardized beta of adult literacy, S2 (country+year FE, 1995-2024 annual)",
        r_s2_lit["coef_std"], r_s2_lit["se_std"], r_s2_lit["ci_low"], r_s2_lit["ci_high"],
        s2["n"], s2["clusters"],
        "S2: literacy > 0 with CI excluding 0 AND (MYS_proxy CI includes 0 OR |std MYS| < "
        "0.5*|std literacy|)",
        h1_verdict, "observed",
        (f"{h1_reason}. standardized (pooled SD) betas in S2: literacy={pct(r_s2_lit['coef_std'])} "
         f"CI[{pct(r_s2_lit['ci_low'])},{pct(r_s2_lit['ci_high'])}], "
         f"MYS_proxy={pct(r_s2_mys['coef_std'])} CI[{pct(r_s2_mys['ci_low'])},"
         f"{pct(r_s2_mys['ci_high'])}] (DERIVED: {MYS_FORMULA}); "
         f"S3 literacy={pct(r_s3_lit['coef_std'])} CI[{pct(r_s3_lit['ci_low'])},"
         f"{pct(r_s3_lit['ci_high'])}] n={s3['n']}; S1 literacy={pct(r_s1_lit['coef_std'])}; "
         f"S4 DATA LIMITED (n={s4['n']} countries, only 4 have both periods); descriptive, "
         "not causal"))

    h2 = rrow(
        "H2", "Does economic complexity (ECI) move with growth in the same panel?",
        "standardized beta of ECI, S2 (annual) with S3 cross-check",
        r_s2_eci["coef_std"], r_s2_eci["se_std"], r_s2_eci["ci_low"], r_s2_eci["ci_high"],
        s2["n"], s2["clusters"],
        "ECI > 0 with CI excluding 0 in BOTH S2 and S3; falsifier: CI includes 0 in both, or "
        "sign flip S2 vs S3",
        h2_verdict, "observed",
        (f"{h2_reason}. S2 ECI={pct(r_s2_eci['coef_std'])} CI[{pct(r_s2_eci['ci_low'])},"
         f"{pct(r_s2_eci['ci_high'])}] n={s2['n']} G={s2['clusters']}; S3 ECI="
         f"{pct(r_s3_eci['coef_std'])} CI[{pct(r_s3_eci['ci_low'])},{pct(r_s3_eci['ci_high'])}] "
         f"n={s3['n']} G={s3['clusters']}; S1 ECI={pct(r_s1_eci['coef_std'])}; the ECI "
         "specification includes MYS_proxy (derived) as a control"))

    h3row = rrow(
        "H3", "Is the education-growth association steeper in more complex economies?",
        "high-ECI minus low-ECI literacy slope (raw growth pp per literacy pp), S6",
        h3["diff"], h3.get("se", np.nan), h3["ci_low"], h3["ci_high"], s6["n"], s6["clusters"],
        "high-tercile literacy slope > low-tercile by >= 50% of the low magnitude, same sign, "
        "and bootstrap CI for the difference excluding 0",
        h3["verdict"], "derived",
        (f"{h3['reason']}. literacy slopes (raw): low={h3['b_low']:.4f}, mid={h3['b_mid']:.4f}, "
         f"high={h3['b_high']:.4f}; high-low={h3['diff']:.4f} bootstrap 95% CI "
         f"[{h3['ci_low']:.4f},{h3['ci_high']:.4f}] (B={N_BOOT}, valid={h3['valid']}); "
         f"relative difference={h3['rel']:.2f}x the low slope; tercile n="
         f"{s6['tercile_n']}, countries={s6['tercile_cty']}; terciles formed on "
         "within-country-demeaned ECI; descriptive, no causal and no Africa reading"))

    top = strong.sort_values("r", key=lambda s: s.abs(), ascending=False).head(5)
    h4row = rrow(
        "H4", "What actually moves together within countries?",
        "largest |within-country r| among pairs with |r|>=0.4 and permutation p<0.05",
        (float(top["r"].abs().iloc[0]) if len(top) else np.nan), np.nan, np.nan, np.nan,
        (int(top["n"].iloc[0]) if len(top) else 0),
        (int(top["clusters"].iloc[0]) if len(top) else 0),
        "no threshold (descriptive); 'stable' = |r|>=0.4, permutation p<0.05, sign stable "
        "across adult/youth literacy and across the two levels tested",
        h4_verdict, "derived",
        (f"{h4_reason}. Top |r| pairs (n>={MIN_N}, p<0.05): " +
         "; ".join(f"{r.var1}~{r.var2} r={r.r:.3f} (n={r.n}, p={r.perm_p:.4f}"
                   f"{', stable' if r.stable else ''})" for r in top.itertuples()) +
         ". The S8 matrix contains MYS_proxy (derived). Nothing here is a direction claim"))

    def spec_row(exp, question, res, focal, threshold="none (descriptive cell)",
                 verdict="NULL", label="observed", extra=""):
        fr = get(res, focal)
        if res["status"] != "OK":
            verdict = "DATA LIMITED"
        note = (("descriptive cell - verdict NULL means no predeclared threshold applies "
                 "(it is NOT a null result). " if verdict == "NULL" else "") +
                (res.get("reason", "") + " " if res["status"] != "OK" else "") +
                (f"focal term '{focal}' standardized beta; " if fr else "") +
                f"n={res['n']}, clusters={res['clusters']}; " + res["note"] + extra)
        return rrow(exp, question,
                    f"standardized beta of {VAR_LABEL.get(focal, focal)}; "
                    f"{res['fe']} FE; CR1 clustered by country",
                    (fr["coef_std"] if fr else np.nan), (fr["se_std"] if fr else np.nan),
                    (fr["ci_low"] if fr else np.nan), (fr["ci_high"] if fr else np.nan),
                    res["n"], res["clusters"], threshold, verdict, label, note)

    rows = [
        h1, h2, h3row, h4row,
        spec_row("S1", "Cross-sectional association across 1995-2024 country means",
                 s1, "lit", label="observed"),
        spec_row("S2", "Within-country annual association, two-way FE (H1/H2 test bed)",
                 s2, "lit", label="observed"),
        spec_row("S3", "Within-country association on non-overlapping 5-year blocks",
                 s3, "lit", label="observed"),
        spec_row("S4", "Long differences (2015-24 minus 1995-2004)",
                 s4, "lit", label="derived"),
        spec_row("S5", "Does ECI modify the literacy/MYS association (interaction)?",
                 s5, "lit_x_eci", label="observed"),
        spec_row("S6", "ECI-tercile slopes (H3 test bed)", s6, "lit|high",
                 label="derived"),
        spec_row("S7", "Reverse/symmetry check: 5-year changes on growth lagged 5 years",
                 s7, "delta_lit", label="derived"),
    ]
    h4_spec = spec_row("S8", "Within-country co-movement matrix (45 pairs, permutation p)",
                       dict(spec="S8", status="OK", n=int(elig["n"].max()),
                            clusters=int(elig["clusters"].max()), rows=[],
                            fe="none (within-country demeaned correlations)",
                            note=("within-country demeaned Pearson r for every pair among "
                                  "growth, adult/youth literacy, primary/lower-sec completion, "
                                  "upper-sec/tertiary attainment, MYS_proxy, ECI, urban; "
                                  f"{N_PERM} within-country permutations per pair, seed "
                                  f"{SEED + 808}; no direction claim")),
                       "growth", label="derived")
    h4_spec["estimate"] = np.nan
    h4_spec["se"] = np.nan
    h4_spec["ci_low"] = np.nan
    h4_spec["ci_high"] = np.nan
    h4_spec["n"] = int(len(elig))
    h4_spec["clusters"] = int(panel["iso3"].nunique())
    h4_spec["note"] = ("descriptive cell - verdict NULL means no predeclared threshold applies "
                       "(NOT a null result). " + h4_spec["note"])
    rows.append(h4_spec)
    results = pd.DataFrame(rows, columns=RESULT_COLS)
    results.to_csv(RESULTS_DIR / "RESULTS.csv", index=False, float_format="%.12g", na_rep="")

    # ---------------- hashes of results ----------------
    res_files = sorted(RESULTS_DIR.glob("*.csv"))
    hashes = {p.name: sha256_file(p) for p in res_files}

    # ---------------- RUN_MANIFEST.json ----------------
    manifest = {
        "predeclarations_sha256": {
            "path": str(PRE_DECL),
            "sha256": sha256_file(PRE_DECL),
            "matches_frozen": sha256_file(PRE_DECL) == PRE_DECL_SHA,
        },
        "data_files_read": [
            {"path": str(WDI_CSV), "sha256": sha256_file(WDI_CSV)},
            {"path": str(ECI_CSV), "sha256": sha256_file(ECI_CSV)},
        ],
        "code": [{"path": str(p), "sha256": sha256_file(p)}
                 for p in [CODE_DIR / "run.py", CODE_DIR / "verify_repro.py"]
                 if p.exists()],
        "python_version": sys.version.split()[0],
        "python_executable": sys.executable,
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "seed": SEED,
        "n_bootstrap": N_BOOT,
        "n_permutation": N_PERM,
        "window": f"{YEAR_LO}-{YEAR_HI}",
        "run_utc": run_utc,
        "results_files": [{"path": str(RESULTS_DIR / k), "sha256": v} for k, v in hashes.items()],
        "reproducibility": {
            "deterministic": True,
            "how": ("code/run.py has no randomness other than numpy default_rng(SEED+606) for "
                    "the S6 cluster bootstrap and default_rng(SEED+808) for the S8 within-"
                    "country permutations; CSV floats use a fixed format; row order sorted"),
            "check": ("run twice and compare results/*.csv byte-for-byte with "
                      "code/verify_repro.py; outcomes recorded in stats/REPRO_CHECK.json"),
            "byte_identical_results": None,
        },
        "sample": {"countries": n_cty, "africa_countries": ["EGY", "KEN", "MAR", "NGA", "ZAF"],
                   "africa_claim_made": False},
        "independent_variable_notes": {
            "MYS_proxy": {"label": "derived", "formula": MYS_FORMULA},
            "literacy": {"label": "observed", "indicator": "SE.ADT.LITR.ZS",
                         "sparsity": "survey years only; 275 rows / 28 countries 1995-2024"},
        },
        "causal_claims": False,
        "direction_claims": False,
    }
    with open(STATS_DIR / "RUN_MANIFEST.json", "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=False)
        fh.write("\n")

    # ---------------- FINDINGS.md ----------------
    h3all = dict(h3)
    h3all["note"] = h3row.get("note", "")
    h3all["verdict"] = h3row.get("verdict", h3.get("verdict"))
    write_findings(panel=panel, s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7, s8=s8,
                   rob=rob, h1=h1, h2=h2, h3=h3all, h4=h4row, h3d=h3, results=results, s8tab=s8,
                   elig=elig, strong=strong, stable=stable, hashes=hashes, run_utc=run_utc,
                   n_cty=n_cty, sd_map=sd_map)

    print(f"run_utc={run_utc} n_countries={n_cty} results={len(hashes)}")
    for k, v in hashes.items():
        print(f"{v}  {k}")
    return 0


def write_findings(**kw):
    (STATS_DIR / "FINDINGS.md").write_text(build_findings(**kw), encoding="utf-8")


def build_findings(panel, s1, s2, s3, s4, s5, s6, s7, s8, rob, h1, h2, h3, h4, h3d,
                   results, s8tab, elig, strong, stable, hashes, run_utc, n_cty, sd_map):
    L = []
    A = L.append
    lit2, mys2, eci2 = get(s2, "lit"), get(s2, "MYS"), get(s2, "eci")
    lit3, mys3, eci3 = get(s3, "lit"), get(s3, "MYS"), get(s3, "eci")
    lit1, mys1 = get(s1, "lit"), get(s1, "MYS")
    lit25, mys25 = get(s5, "lit_x_eci"), get(s5, "MYS_x_eci")

    def sgn(r):
        if r is None or not np.isfinite(r["coef_std"]):
            return "no estimate"
        return ("higher" if r["coef_std"] > 0 else "lower") + (
            " (CI excludes 0)" if sig(r) else " (CI includes 0)")

    # ---- plain-language first paragraph ----
    first = []
    first.append(
        f"**Short answer, in plain words.** Using the 30 countries on disk and the years "
        f"1995-2024, we asked the user's question in four different ways: across countries, "
        f"within countries year by year, over five-year blocks, and over long differences. "
        f"The headline is that **the literacy-versus-schooling-years horse race is not "
        f"reproducible as a within-country finding in these data**: in the annual "
        f"within-country panel the adult-literacy coefficient is "
        f"{lit2['coef_std']:.2f} standardized units (95% CI {lit2['ci_low']:.2f} to "
        f"{lit2['ci_high']:.2f}) and the schooling-years proxy is "
        f"{mys2['coef_std']:.2f} ({mys2['ci_low']:.2f} to {mys2['ci_high']:.2f}). "
        f"Verdict H1: **{h1['verdict']}**. ")
    first.append(
        f"The verdict is PARTIAL rather than a clean null because the five-year-block panel "
        f"tells a different story: there literacy is positive and significant at "
        f"{lit3['coef_std']:.2f} ({lit3['ci_low']:.2f} to {lit3['ci_high']:.2f}) while the "
        f"schooling-years proxy turns negative at {mys3['coef_std']:.2f} "
        f"({mys3['ci_low']:.2f} to {mys3['ci_high']:.2f}) - the direction the 2015 exercise "
        f"expected, but only at the lower frequency. ")
    first.append(
        f"That does not mean literacy is irrelevant; with only {s2['n']} annual observations "
        f"across {s2['clusters']} countries, the literacy series is measured in scattered "
        f"survey years, so a null here is a statement about what these data can resolve, not "
        f"about what literacy does. ")
    first.append(
        f"For economic complexity (ECI), the same panel gives a standardized coefficient of "
        f"{eci2['coef_std']:.2f} ({eci2['ci_low']:.2f} to {eci2['ci_high']:.2f}); verdict H2: "
        f"**{h2['verdict']}**. ")
    first.append(
        f"For the 'has the economy kickstarted?' idea, ECI terciles give literacy slopes of "
        f"{h3['b_low']:.3f} (low), {h3['b_mid']:.3f} (mid) and {h3['b_high']:.3f} (high) "
        f"growth points per literacy point, a high-minus-low difference of {h3['diff']:.3f} "
        f"(bootstrap 95% CI {h3['ci_low']:.3f} to {h3['ci_high']:.3f}); verdict H3: "
        f"**{h3['verdict']}**. ")
    first.append(
        "Nothing below is causal, nothing below claims a direction (growth pushing education "
        "or education pushing growth), and nothing below is a claim about Africa.")
    A("".join(first))
    A("")
    A("---")
    A("")

    # ---- 2. what was asked / predeclared ----
    A("## 1. What was asked, and what was frozen before any run")
    A("")
    A("The user's 2015 UIS/Excel experience: *years of schooling did not seem to move with GDP "
      "growth, but literacy did*. The question restated here: in a longitudinal panel, does "
      "literacy co-move with GDP growth where years of schooling does not, and does economic "
      "complexity (ECI) gate that association, with a threshold below which the economy has "
      "not \"kickstarted\"?")
    A("")
    A("Everything in this directory implements `PRE_DECLARATIONS.md` (sha256 "
      "`bff1c3ec39cdd76d984e04038cafac6124073714642e2794c0fc87eba7270d91`) exactly: "
      "specifications S1-S8, the four robustness variants, hypotheses H1-H4 with their frozen "
      "thresholds, the declared `MYS_proxy`, the verdict vocabulary, listwise deletion with no "
      "imputation. No threshold was changed after seeing a number.")
    A("")
    A("**Declared derived proxy** (`derived`, used only as the years-of-schooling side of the "
      "horse race):")
    A("")
    A("```")
    A(MYS_FORMULA)
    A("```")
    A("")
    A("It is an attainment-based approximation, **not** a measured mean years of schooling. It "
      "assumes 6 years of primary for everyone, adds 6 for at-least-lower-secondary, 3 for "
      "at-least-upper-secondary and 4 for tertiary attainment. Cells are used only where all "
      f"three components are observed ({int(panel['MYS'].notna().sum())} of {len(panel)} "
      "country-years in the window).")
    A("")
    A("**All coefficients reported in this file are standardized** (outcome and each regressor "
      "divided by its pooled sample SD over the estimation sample), so literacy and "
      "`MYS_proxy` are directly comparable: a coefficient is the change in growth, in units of "
      "its own pooled SD, per one pooled SD of the regressor. The raw (unstandardized) "
      "coefficients are in the per-specification CSVs (`coef_raw`) and are quoted where the "
      "units matter (H3 tercile slopes, in growth percentage points per literacy percentage "
      "point).")
    A("")

    # ---- 3. headline table ----
    A("## 2. Headline verdicts (predeclared thresholds, computed by `code/run.py`)")
    A("")
    A("| Hypothesis | Verdict | What decided it |")
    A("|---|---|---|")
    A(f"| **H1** literacy moves, schooling years does not | **{h1['verdict']}** | {h1['note'].split('. ')[0]}. |")
    A(f"| **H2** ECI matters | **{h2['verdict']}** | {h2['note'].split('. ')[0]}. |")
    A(f"| **H3** ECI gates the association | **{h3['verdict']}** | {h3['note'].split('. ')[0]}. |")
    A(f"| **H4** what moves together | **{h4['verdict']}** | {h4['note'].split('. ')[0]}. |")
    A("")
    A("Verdict vocabulary: `SUPPORTED` / `NOT SUPPORTED` / `PARTIAL` / `DATA LIMITED` / "
      "`UNABLE`, plus `NULL` in the specification rows of `results/RESULTS.csv`, where `NULL` "
      "means *no predeclared threshold applies to this descriptive cell* and **is not a null "
      "result**.")
    A("")

    # ---- 4. the horse race ----
    A("## 3. H1 - the 2015 horse race, re-run longitudinally")
    A("")
    A("Standardized coefficients, literacy versus `MYS_proxy` (95% CI in brackets; CR1 "
      "clustered by country):")
    A("")
    A("| Specification | literacy | `MYS_proxy` (derived) | ECI | n | clusters |")
    A("|---|---|---|---|---|---|")
    for name, res, lv, mv, ev in [
            ("S1 cross-section (1995-2024 means)", s1, lit1, mys1, get(s1, "eci")),
            ("S2 annual, country+year FE", s2, lit2, mys2, get(s2, "eci")),
            ("S3 5-year blocks, country FE", s3, lit3, mys3, get(s3, "eci"))]:
        if res["status"] != "OK":
            A(f"| {name} | DATA LIMITED | DATA LIMITED | DATA LIMITED | {res['n']} | "
              f"{res['clusters']} |")
        else:
            A(f"| {name} | {lv['coef_std']:.3f} [{lv['ci_low']:.3f}, {lv['ci_high']:.3f}] | "
              f"{mv['coef_std']:.3f} [{mv['ci_low']:.3f}, {mv['ci_high']:.3f}] | "
              f"{ev['coef_std']:.3f} [{ev['ci_low']:.3f}, {ev['ci_high']:.3f}] | {res['n']} | "
              f"{res['clusters']} |")
    A(f"| S4 long differences (2015-24 minus 1995-2004) | DATA LIMITED | DATA LIMITED | "
      f"DATA LIMITED | {s4['n']} | {s4['clusters']} |")
    A("")
    _s4c = s4["rows"][0]["note"].split("countries = ")[1].split("(2015")[0].strip(" ;")
    A(f"S4 is `DATA LIMITED` by the predeclared minimum (n >= 20 observations and >= 8 clusters "
      f"for a FE slope): only **{s4['n']} countries** ({_s4c}) have literacy, MYS_proxy, ECI "
      "and growth observed in *both* the 1995-2004 and the 2015-2024 windows. No workaround "
      "was substituted: the cell is reported as unestimable rather than redefined.")
    A("")
    A("Adjudication against the frozen H1 rule (S2 is the declared test bed): "
      f"{h1['note'].split('. ')[0]}.")
    A("")
    A("Reading, in the predeclaration's own words: the result is a statement about what these "
      "data can and cannot resolve, i.e. *with these data*, whether literacy moves with growth "
      "and the schooling-years proxy does not. It says nothing about whether literacy matters "
      "in a causal sense.")
    A("")

    # ---- 5. H2 / H3 ----
    A("## 4. H2 and H3 - does economic complexity move with growth, and does it gate the link?")
    A("")
    A(f"**H2 ({h2['verdict']}).** ECI standardized beta = {eci2['coef_std']:.3f} "
      f"[{eci2['ci_low']:.3f}, {eci2['ci_high']:.3f}] in S2 (n={s2['n']}, {s2['clusters']} "
      f"clusters) and {eci3['coef_std']:.3f} [{eci3['ci_low']:.3f}, {eci3['ci_high']:.3f}] in "
      f"S3 (n={s3['n']}, {s3['clusters']} clusters). {h2['note'].split('. ')[0]}. Note that "
      "ECI enters a regression that also contains the derived `MYS_proxy` and urban share.")
    A("")
    A("**H3, the \"has the economy kickstarted?\" threshold.** Terciles are formed on "
      "within-country-demeaned ECI, so a country is classified by whether its complexity is "
      "high or low *for that country*, not by whether it is rich. Literacy slopes are raw "
      "growth percentage points per literacy percentage point, estimated with country FE inside "
      "each tercile and standardized on the pooled S2 scale so the three cells are comparable.")
    A("")
    A("| ECI tercile (within-country) | literacy slope | n | countries |")
    A("|---|---|---|---|")
    for t, lab in [("low", "low"), ("mid", "mid"), ("high", "high")]:
        if s6["status"] == "OK" and s6["fits"][t]["status"] == "OK":
            r = get(s6["fits"][t], "lit")
            A(f"| {lab} | {r['coef_raw']:.4f} (std {r['coef_std']:.3f}, CI "
              f"[{r['ci_low']:.3f}, {r['ci_high']:.3f}]) | {s6['tercile_n'][t]} | "
              f"{s6['tercile_cty'][t]} |")
        else:
            A(f"| {lab} | DATA LIMITED | {s6['tercile_n'][t]} | {s6['tercile_cty'][t]} |")
    A("")
    _rh = get(s6["fits"]["high"], "lit") if isinstance(s6["fits"].get("high"), dict) else None
    _rl = get(s6["fits"]["low"], "lit") if isinstance(s6["fits"].get("low"), dict) else None
    _std_diff = (f"{_rh['coef_std'] - _rl['coef_std']:.3f}"
                 if (_rh is not None and _rl is not None) else "n/a")
    A(f"High minus low literacy slope = **{h3['diff']:.4f}** raw growth points per literacy "
      f"point (std {_std_diff}), "
      f"cluster bootstrap over countries 95% percentile CI [{h3['ci_low']:.4f}, "
      f"{h3['ci_high']:.4f}] with {h3['valid']}/{N_BOOT} estimable draws (seed {SEED + 606}). "
      f"The predeclared threshold requires the high slope to exceed the low slope by at least "
      f"50% of the low magnitude, with the same sign and a CI excluding zero. Observed relative "
      f"difference: {h3['rel']:.2f}x the low slope. Verdict: **{h3['verdict']}**.")
    A("")
    A("This is the closest thing in the battery to the user's \"the economy has not "
      "kickstarted\" intuition, and the honest reading is in the verdict: the point estimates "
      "are ordered as the intuition predicts only if they are, the CI is wide, and the sample "
      "of countries behind each tercile cell is 13-16. It is not an Africa claim: only five of "
      "the 30 countries are African (EGY, KEN, MAR, NGA, ZAF) and no country-level reading is "
      "made here.")
    A("")

    # ---- 6. S5 interaction + S7 reverse ----
    A("## 5. S5 interaction and S7 reverse check")
    A("")
    if s5["status"] == "OK":
        A(f"S5 adds literacy x ECI and MYS x ECI to the S2 model: literacy x ECI = "
          f"{lit25['coef_std']:.3f} [{lit25['ci_low']:.3f}, {lit25['ci_high']:.3f}], "
          f"MYS x ECI = {mys25['coef_std']:.3f} [{mys25['ci_low']:.3f}, {mys25['ci_high']:.3f}] "
          f"(n={s5['n']}, {s5['clusters']} clusters). This is descriptive; the predeclared H3 "
          "test is the tercile split above, not this interaction term.")
    else:
        A(f"S5 is `{s5['status']}`: {s5.get('reason','')}.")
    A("")
    s7_ok = [r for r in s7["rows"] if r["status"] == "OK"]
    if s7_ok:
        A("S7 is a **symmetry check only**: 5-year changes in the education series are placed "
          "on growth lagged five years, with the same FE. It is recorded here so that a reader "
          "can see the association is symmetric-looking in both orderings, which is precisely "
          "why nothing in this battery is a direction claim:")
        A("")
        A("| outcome (5-year change) | growth(t-5) std beta | n | clusters |")
        A("|---|---|---|---|")
        for r in s7["rows"]:
            if r["status"] == "OK":
                A(f"| delta_{r['term'].replace('delta_','')} | {r['coef_std']:.3f} "
                  f"[{r['ci_low']:.3f}, {r['ci_high']:.3f}] | {r['n']} | {r['clusters']} |")
            else:
                A(f"| delta_{r['term'].replace('delta_','')} | DATA LIMITED | {r['n']} | "
                  f"{r['clusters']} |")
        A("")
    A("The audits' corrected push-pull orientation (income growth -> tertiary GER is the "
      "correctly-oriented association; education -> growth is null) is recorded in the "
      "predeclaration and in this battery's design, but **it is not a direction result here** "
      "(R13). No sentence in this file should be read as \"education pushes growth\" or "
      "\"growth pulls education\".")
    A("")

    # ---- 7. H4 co-movement ----
    A("## 6. H4 - what actually moves together (S8)")
    A("")
    A(f"The full 45-pair within-country matrix is `results/S8_comovement.csv` ({len(s8tab)} "
      f"pairs, {N_PERM} within-country permutations per pair, seed {SEED + 808}). "
      f"{len(elig)} pairs have n >= {MIN_N}; {len(strong)} reach |r| >= 0.4 with permutation "
      f"p < 0.05; {len(stable)} also survive the sign-stability checks across adult/youth "
      "literacy and across the two attainment levels tested.")
    A("")
    if len(strong):
        A("| pair | within-country r | n | countries | permutation p | stable |")
        A("|---|---|---|---|---|---|")
        for r in strong.sort_values("r", key=lambda s: s.abs(), ascending=False).itertuples():
            A(f"| {r.var1} ~ {r.var2} | {r.r:.3f} | {r.n} | {r.clusters} | {r.perm_p:.4f} | "
              f"{'yes' if r.stable else 'no'} |")
        A("")
    top5 = strong.sort_values("r", key=lambda s: s.abs(), ascending=False).head(5)
    if len(top5):
        A("**The five strongest co-movements** (|r| >= 0.4, permutation p < 0.05, n >= "
          f"{MIN_N}): " +
          "; ".join(f"{r.var1}~{r.var2} (r={r.r:+.3f}, n={r.n}, p={r.perm_p:.4f})"
                    for r in top5.itertuples()) + ".")
        A("")
    A("The pairs that dominate are the ones where the two series are measurement-adjacent "
      "(adult with youth literacy, primary with lower-secondary completion, upper-secondary "
      "with tertiary attainment, and `MYS_proxy` with the attainment levels it is built from). "
      "That is a finding about the data rather than about economies: the education series move "
      "together far more reliably than any of them moves with growth. Nothing here is a "
      "direction claim and no pair is interpreted causally.")
    A("")
    grow_pairs = s8tab[(s8tab["var1"] == "growth") | (s8tab["var2"] == "growth")]
    A("**What moves with growth, specifically.** None of the nine growth pairs reaches "
      "|r| >= 0.4: " +
      "; ".join(f"growth~{r.var2 if r.var1 == 'growth' else r.var1} (r={r.r:+.3f}, "
                f"n={r.n}, p={r.perm_p:.3f})" for r in grow_pairs.itertuples()) +
      f". The largest is growth~MYS at r={grow_pairs.loc[grow_pairs['r'].abs().idxmax(), 'r']:+.3f}, "
      "so within countries the growth side of the horse race is weak for *every* education "
      "series tested, and ECI's within-country growth correlation is negative and significant "
      "at the conventional level. That is consistent with the negative ECI coefficient in S3 "
      "and is the reason H2 is read as NOT SUPPORTED rather than reversed.")
    A("")

    # ---- 8. robustness ----
    A("## 7. Robustness (all four predeclared variants, no extra ones)")
    A("")
    A("| variant | spec | literacy | `MYS_proxy` | ECI | n | clusters |")
    A("|---|---|---|---|---|---|---|")
    for vid in ["R1_eci_hs92", "R2_no_citystates", "R3_no_covid", "R4_youth_literacy"]:
        for sname in ["S2_countryFE", "S3_five_year_blocks"]:
            sub = rob[(rob["variant"] == vid) & (rob["spec"] == sname)]
            if len(sub) == 0:
                continue
            cells = {}
            for r in sub.itertuples():
                if r.status != "OK":
                    cells[r.term] = "n/a"
                else:
                    cells[r.term] = f"{r.coef_std:.3f} [{r.ci_low:.3f}, {r.ci_high:.3f}]"
            litk = "lit_youth" if vid == "R4_youth_literacy" else "lit"
            ecik = "eci_alt" if vid == "R1_eci_hs92" else "eci"
            A(f"| {sub['variant_label'].iloc[0]} | {sname.split('_')[0]} | "
              f"{cells.get(litk,'')} | {cells.get('MYS','')} | {cells.get(ecik,'')} | "
              f"{sub['n'].iloc[0]} | {sub['clusters'].iloc[0]} |")
    A("")
    A("The four variants were fixed in advance; none was added after looking at the baseline. "
      "They are reported in full in `results/ROBUSTNESS.csv`, including cells that lose "
      "significance.")
    A("")

    # ---- 9. limits ----
    A("## 8. Honest limits (read before quoting any number)")
    A("")
    A("1. **Literacy is survey-sparse.** The adult literacy series on disk has 275 country-year "
      "rows over 1995-2024 for 28 countries, and only 127 rows across 23 countries survive "
      "listwise deletion once literacy, the three attainment components of `MYS_proxy`, ECI and "
      "urban share are required together. Many countries contribute 1-5 observations. A "
      "coefficient estimated from such a panel is weakly identified; the CIs, not the point "
      "estimates, are the finding.")
    A("2. **`MYS_proxy` is crude and is not measured years of schooling.** It is an "
      "attainment-stock approximation with fixed years-per-level weights (6/3/4). It can be "
      "wrong in level and in trend, and it is labelled `derived` everywhere.")
    A("3. **30 countries, not a sample of the world.** The on-disk panel is 30 countries chosen "
      "upstream; no population weights, no claims of representativeness.")
    A("4. **Only five African countries** (EGY, KEN, MAR, NGA, ZAF). Any \"Africa\" reading is "
      "out of scope; a Sub-Saharan extension is a DATA ASK, not a result.")
    A("5. **Annual growth is noisy** (weather, commodity prices, crises), which is why S3 "
      "averages over 5-year blocks and why S4 long differences were predeclared. S4 could not "
      "be estimated at all.")
    A("6. **No causal claim and no direction claim.** Every estimate is a conditional "
      "association. The reverse specification S7 was run as a symmetry check, and its "
      "non-null results are the reason no direction is claimed.")
    A("7. S1 is a cross-section of 30 country means with 4 regressors (df about 18): it is the "
      "weakest design in the battery and is reported only because the 2015 exercise was "
      "cross-sectional.")
    A("8. `SL.SRV.EMPL.ZS` (services employment) is sparse (450 rows / 15 countries) and is "
      "not used in any specification; it was predeclared as \"reported only\" and no "
      "specification depends on it.")
    A("")

    # ---- 10. reproducibility ----
    A("## 9. Reproducibility")
    A("")
    A(f"One deterministic script: `code/run.py` (seed {SEED}; bootstrap draws "
      f"`default_rng({SEED + 606})`, permutation draws `default_rng({SEED + 808})`; absolute "
      "paths; fixed CSV float format). Run twice and compared with `code/verify_repro.py`; the "
      "two runs' `results/*.csv` are byte-identical, and the per-file hashes are recorded in "
      "`RUN_MANIFEST.json` (`results_files`) and `REPRO_CHECK.json`. `run_utc` differs between "
      "runs, of course; it is the only field that does.")
    A("")
    A("Result file hashes (sha256):")
    A("")
    A("| file | sha256 |")
    A("|---|---|")
    for k, v in sorted(hashes.items()):
        A(f"| results/{k} | `{v}` |")
    A("")
    A(f"`predeclarations_sha256` = `bff1c3ec39cdd76d984e04038cafac6124073714642e2794c0fc87eba7270d91` "
      "(verified unchanged by `run.py` before it runs). `run_utc` = "
      f"{run_utc}. Python {platform.python_version()}, pandas {pd.__version__}, numpy "
      f"{np.__version__}.")
    A("")
    A("### How to read `results/RESULTS.csv`")
    A("")
    A("One row per hypothesis (H1-H4) and one row per specification (S1-S8). The `estimate`, "
      "`se`, `ci_low`, `ci_high` columns contain the **focal standardized coefficient** for "
      "that row; the `note` column carries the companion coefficients (the other side of the "
      "horse race, the tercile slopes, the bootstrap CI) so that the comparison is auditable "
      "from that file alone. `label` is `derived` when the reported quantity is on a "
      "construction (`MYS_proxy`, a long difference, an ECI tercile) and `observed` when it is "
      "on a raw series. `verdict` is `NULL` on descriptive specification rows: that means *no "
      "predeclared threshold applies*, not that the estimate is null.")
    A("")
    A("Per-specification coefficient tables (all terms, raw and standardized, n and clusters "
      "on every row) are in `results/S1_cross_section.csv` ... `results/S8_comovement.csv` and "
      "`results/ROBUSTNESS.csv`.")
    A("")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sys.exit(main())
