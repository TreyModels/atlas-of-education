#!/usr/bin/env python3
"""Education -> economic complexity (ECI): predeclared descriptive panel analysis.

Implements PRE_DECLARATIONS.md (sha256 e2a707a9...5bc230) exactly:
specs S1-S6, true calendar-year lags 5/10, control sets C0/C1, the frozen verdict rule,
the declared S6 heterogeneity split, and the declared E5 cross-check.

DESCRIPTIVE / ASSOCIATIONAL ONLY. No causal claim. No direction claim (the reverse-order
spec S5 is reported symmetrically). No imputation: listwise deletion only, all counts reported.
`mys_proxy` is DERIVED and labelled. Deterministic: one PCG64 stream, seed 20261120, floats at
%.10g, so two clean runs write byte-identical results CSVs.

Run:  python run_edu_eci.py
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/Users/treymenefee/massification_live/experiments/massification-2026-11-20")
EXT = BASE / "10_massification/extensions/edu_eci_2026-11-20"
RESULTS = EXT / "results"
CODE = EXT / "code"

WDI_LONG = BASE / "09_relations/data/panel_wdi_long.csv"
WDI_WIDE = BASE / "09_relations/data/panel_wdi_wide.csv"
ECI_CSV = BASE / "09_relations/data/economic_complexity_panel_30ctys.csv"
PRE_DECL = EXT / "PRE_DECLARATIONS.md"
PRE_DECL_SHA = "e2a707a9b67e525a1f483fc42d71555d882af31478f348f22a2943396c5bc230"

SEED = 20261120
YEAR_LO, YEAR_HI = 1995, 2024
MIN_N, MIN_CLUSTERS = 20, 8
LABEL = "observed/derived"

EDU = {
    "lit": "SE.ADT.LITR.ZS",
    "lit_youth": "SE.ADT.1524.LT.ZS",
    "prm_cmpt": "SE.PRM.CMPT.ZS",
    "lsec_cmpt": "SE.SEC.CMPT.LO.ZS",
    "cuat_up": "SE.SEC.CUAT.UP.ZS",
    "cuat_ba": "SE.TER.CUAT.BA.ZS",
}
EDU_ORDER = ["lit", "lit_youth", "prm_cmpt", "lsec_cmpt", "cuat_up", "cuat_ba", "mys_proxy"]
LAGS = (5, 10)
CONTROLS = {"C0": [], "C1": ["log_gdppc", "urban"]}
MYS_FORMULA = ("mys_proxy = 6 + 6*(SE.SEC.CUAT.LO.ZS/100) + 3*(SE.SEC.CUAT.UP.ZS/100) "
               "+ 4*(SE.TER.CUAT.BA.ZS/100)")


# ---------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------
def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fnum(v) -> str:
    if v is None:
        return ""
    try:
        x = float(v)
    except (TypeError, ValueError):
        return str(v)
    if not math.isfinite(x):
        return "NA"
    return "%.10g" % x


def norm_p(t: float) -> float:
    return 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(t) / math.sqrt(2.0))))


def _demean_twoway(M: np.ndarray, gid: np.ndarray, tid: np.ndarray, iters=50, tol=1e-10):
    M = M.copy()
    df = pd.DataFrame(M)
    for _ in range(iters):
        old = M.copy()
        M = M - df.groupby(gid).transform("mean").values
        df = pd.DataFrame(M)
        M = M - df.groupby(tid).transform("mean").values
        df = pd.DataFrame(M)
        if np.max(np.abs(M - old)) < tol:
            break
    return M


def fe_ols(d, y, xs, entity="iso3", time="year", cluster="iso3", min_n=MIN_N, min_cty=MIN_CLUSTERS):
    """Two-way FE OLS, CR1 clustered SE (same algebra as 09_relations/scripts/panel_lib.py)."""
    cols = [entity, time] + [y] + list(xs)
    dd = d[cols].dropna().copy()
    n = len(dd)
    if n < min_n or dd[entity].nunique() < min_cty:
        return {"error": f"insufficient obs (n={n}, ctys={dd[entity].nunique()})", "n": n,
                "n_cty": int(dd[entity].nunique())}
    yv = dd[[y]].values.astype(float)
    X = dd[list(xs)].values.astype(float)
    gid = dd[entity].values
    tid = dd[time].values
    Xw = _demean_twoway(X, gid, tid)
    yw = _demean_twoway(yv, gid, tid).reshape(-1, 1)
    ok = np.std(Xw, axis=0) > 1e-9
    if not ok.all():
        return {"error": "no within variation in " + ",".join(np.array(list(xs))[~ok]),
                "n": n, "n_cty": int(dd[entity].nunique())}
    XtX = Xw.T @ Xw
    try:
        b = np.asarray(np.linalg.solve(XtX, Xw.T @ yw)).ravel()
    except np.linalg.LinAlgError:
        return {"error": "singular XtX", "n": n, "n_cty": int(dd[entity].nunique())}
    e = (yw.ravel() - Xw @ b)
    G = dd[cluster].nunique()
    nent, nyr, k = dd[entity].nunique(), dd[time].nunique(), X.shape[1]
    dof = max(n - k - (nent - 1) - (nyr - 1), 1)
    inv = np.linalg.pinv(XtX)
    meat = np.zeros((k, k))
    cl = dd[cluster].values
    for g in np.unique(cl):
        m = (cl == g)
        s = Xw[m].T @ e[m]
        meat += np.outer(s, s)
    scale = (G / (G - 1)) * ((n - 1) / dof)
    V = inv @ meat @ inv * scale
    se = np.sqrt(np.diag(V))
    out = {"n": n, "n_cty": int(nent), "n_clusters": int(G),
           "period": f"{int(dd[time].min())}-{int(dd[time].max())}",
           "r2_within": 1.0 - float(np.asarray(e @ e).ravel()[0]) / max(float(np.asarray(yw.T @ yw).ravel()[0]), 1e-12)}
    for i, x in enumerate(xs):
        b_i, se_i = float(b[i]), float(se[i])
        out[x] = dict(coef=b_i, se=se_i, t=b_i / se_i if se_i > 0 else math.nan,
                      p=norm_p(b_i / se_i) if se_i > 0 else math.nan,
                      ci_lo=b_i - 1.959963984540054 * se_i,
                      ci_hi=b_i + 1.959963984540054 * se_i)
    return out


def ols_hc1(d, y, xs):
    dd = d[[y] + list(xs)].dropna().copy()
    n = len(dd)
    if n < 8:
        return {"error": f"insufficient obs (n={n})", "n": n, "n_cty": n}
    yv = dd[[y]].values.astype(float).ravel()
    X = np.column_stack([np.ones(n)] + [dd[x].values.astype(float) for x in xs])
    XtX = X.T @ X
    try:
        b = np.linalg.solve(XtX, X.T @ yv)
    except np.linalg.LinAlgError:
        return {"error": "singular XtX", "n": n, "n_cty": n}
    e = yv - X @ b
    k = X.shape[1]
    inv = np.linalg.pinv(XtX)
    V = inv @ (X.T @ np.diag(e ** 2) @ X) @ inv * (n / max(n - k, 1))
    se = np.sqrt(np.diag(V))
    out = {"n": n, "n_cty": n, "n_clusters": n, "period": "", "r2_within": math.nan}
    for i, x in enumerate(xs):
        j = i + 1
        b_i, se_i = float(b[j]), float(se[i])
        out[x] = dict(coef=b_i, se=se_i, t=b_i / se_i if se_i > 0 else math.nan,
                      p=norm_p(b_i / se_i) if se_i > 0 else math.nan,
                      ci_lo=b_i - 1.959963984540054 * se_i,
                      ci_hi=b_i + 1.959963984540054 * se_i)
    return out


def load_wide() -> pd.DataFrame:
    """Pivot the long WDI panel 1995-2024 + merge the Growth Lab ECI file."""
    long = pd.read_csv(WDI_LONG)
    keep = list(EDU.values()) + ["NY.GDP.PCAP.KD", "SP.URB.TOTL.IN.ZS",
                                 "SE.SEC.CUAT.LO.ZS", "SE.SEC.CUAT.UP.ZS", "SE.TER.CUAT.BA.ZS"]
    sub = long[long.indicator.isin(keep) & (long.year >= YEAR_LO) & (long.year <= YEAR_HI)]
    wide = sub.pivot_table(index=["iso3", "year"], columns="indicator", values="value").reset_index()
    for k, v in EDU.items():
        wide[k] = wide[v]
    wide["log_gdppc"] = np.log(wide["NY.GDP.PCAP.KD"].clip(lower=1e-3))
    wide["urban"] = wide["SP.URB.TOTL.IN.ZS"]
    lo, up, ba = "SE.SEC.CUAT.LO.ZS", "SE.SEC.CUAT.UP.ZS", "SE.TER.CUAT.BA.ZS"
    wide["mys_proxy"] = 6 + 6 * (wide[lo] / 100) + 3 * (wide[up] / 100) + 4 * (wide[ba] / 100)
    eci = pd.read_csv(ECI_CSV)[["iso3", "year", "eci_sitc", "eci_hs92"]]
    wide = wide.merge(eci, on=["iso3", "year"], how="left").sort_values(["iso3", "year"]).reset_index(drop=True)
    return wide


def add_year_lag(df: pd.DataFrame, col: str, L: int) -> pd.DataFrame:
    """True calendar-year lag: join value at year t-L onto row year t. No row shifting."""
    right = df[["iso3", "year", col]].copy()
    right["year"] = right["year"] + L
    right = right.rename(columns={col: f"{col}_L{L}"})
    return df.merge(right, on=["iso3", "year"], how="left")


def build_annual(wide: pd.DataFrame) -> pd.DataFrame:
    df = wide.copy()
    for c in EDU_ORDER + ["log_gdppc", "urban", "eci_sitc", "eci_hs92"]:
        for L in LAGS:
            df = add_year_lag(df, c, L)
    return df


def block_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Non-overlapping 5-year block means; education block lag by block_start-L."""
    d = df.copy()
    d["block"] = (d["year"] // 5) * 5
    g = d.groupby(["iso3", "block"], as_index=False).agg(
        {**{"eci_sitc": "mean", "eci_hs92": "mean", "log_gdppc": "mean", "urban": "mean"},
         **{c: "mean" for c in EDU_ORDER}})
    out = g.copy()
    for c in EDU_ORDER + ["log_gdppc", "urban"]:
        for L in LAGS:
            right = g[["iso3", "block", c]].copy()
            right["block"] = right["block"] + L
            right = right.rename(columns={c: f"{c}_L{L}"})
            out = out.merge(right, on=["iso3", "block"], how="left")
    return out


def cell_record(spec, outcome, level, lag, controls, res, label=LABEL, note="", xname=None):
    rec = dict(spec=spec, outcome=outcome, level=level, lag=lag, controls=controls,
               coef=math.nan, se=math.nan, t=math.nan, p=math.nan, ci_lo=math.nan, ci_hi=math.nan,
               n=res.get("n", 0), n_ctry=res.get("n_cty", 0), n_blocks=math.nan,
               period=res.get("period", ""), label=label, note=note)
    if "error" in res:
        rec["note"] = (note + " | " if note else "") + "ERROR: " + res["error"]
        return rec
    a = res[xname or level]
    rec.update(coef=a["coef"], se=a["se"], t=a["t"], p=a["p"], ci_lo=a["ci_lo"], ci_hi=a["ci_hi"])
    if spec == "S3_B5":
        rec["n_blocks"] = res.get("n_blocks", math.nan)
    return rec


def one_way_fe(d, y, xs, min_n=MIN_N, min_cty=MIN_CLUSTERS):
    """Country-FE OLS with CR1 clustered SE (used for the 5-year block spec)."""
    cols = ["iso3", "block"] + [y] + list(xs)
    dd = d[cols].dropna().copy()
    n = len(dd)
    if n < min_n or dd["iso3"].nunique() < min_cty:
        return {"error": f"insufficient obs (n={n}, ctys={dd['iso3'].nunique()})", "n": n,
                "n_cty": int(dd["iso3"].nunique()), "n_blocks": int(dd["block"].nunique())}
    yv = dd[[y]].values.astype(float)
    X = dd[list(xs)].values.astype(float)
    gid = dd["iso3"].values
    dfx = pd.DataFrame(X)
    Xw = X - dfx.groupby(gid).transform("mean").values
    dfy = pd.DataFrame(yv)
    yw = (yv - dfy.groupby(gid).transform("mean").values)
    XtX = Xw.T @ Xw
    try:
        b = np.asarray(np.linalg.solve(XtX, Xw.T @ yw)).ravel()
    except np.linalg.LinAlgError:
        return {"error": "singular XtX", "n": n, "n_cty": int(dd["iso3"].nunique()),
                "n_blocks": int(dd["block"].nunique())}
    e = yw.ravel() - Xw @ b
    G, k = dd["iso3"].nunique(), X.shape[1]
    nent = G
    dof = max(n - k - (nent - 1), 1)
    inv = np.linalg.pinv(XtX)
    meat = np.zeros((k, k))
    for g in np.unique(gid):
        m = (gid == g)
        s = Xw[m].T @ e[m]
        meat += np.outer(s, s)
    V = inv @ meat @ inv * ((G / (G - 1)) * ((n - 1) / dof))
    se = np.sqrt(np.diag(V))
    out = {"n": n, "n_cty": int(G), "n_clusters": int(G),
           "n_blocks": int(dd["block"].nunique()),
           "period": f"{int(dd['block'].min())}-{int(dd['block'].max()) + 4}", "r2_within": math.nan}
    for i, x in enumerate(xs):
        b_i, se_i = float(b[i]), float(se[i])
        out[x] = dict(coef=b_i, se=se_i, t=b_i / se_i if se_i > 0 else math.nan,
                      p=norm_p(b_i / se_i) if se_i > 0 else math.nan,
                      ci_lo=b_i - 1.959963984540054 * se_i,
                      ci_hi=b_i + 1.959963984540054 * se_i)
    return out


# ---------------------------------------------------------------------------------------
# specs
# ---------------------------------------------------------------------------------------
def s1_long_diff(df):
    """S1: country cross-section of long differences (see PRE_DECLARATIONS §3)."""
    rows = []
    for outcome in ("eci_sitc", "eci_hs92"):
        recs = []
        for iso, d in df.groupby("iso3"):
            row = {"iso3": iso}
            for w_lo, w_hi, tag in ((2015, 2024, "post"), (2005, 2014, "mid"), (1995, 2004, "pre")):
                m = (d.year >= w_lo) & (d.year <= w_hi)
                row[f"{outcome}_{tag}"] = d.loc[m, outcome].mean()
                row[f"gdp_{tag}"] = d.loc[m, "log_gdppc"].mean()
                row[f"urb_{tag}"] = d.loc[m, "urban"].mean()
            for c in EDU_ORDER:
                m1 = (d.year >= 2010) & (d.year <= 2019)
                m0 = (d.year >= 2000) & (d.year <= 2009)
                row[f"d_{c}"] = d.loc[m1, c].mean() - d.loc[m0, c].mean()
            row["d_eci"] = row[f"{outcome}_post"] - row[f"{outcome}_mid"]
            recs.append(row)
        ld = pd.DataFrame(recs)
        ld["d_gdp"] = ld["gdp_post"] - ld["gdp_mid"]
        ld["d_urb"] = ld["urb_post"] - ld["urb_mid"]
        for level in EDU_ORDER:
            for ctrl in ("C0", "C1"):
                cols = [f"d_{level}"] + (["d_gdp", "d_urb"] if ctrl == "C1" else [])
                res = ols_hc1(ld, "d_eci", cols)
                r = cell_record("S1_LD", outcome, level, math.nan, ctrl, res, xname=f"d_{level}")
                r["note"] = (f"long differences; OUTCOME change = mean(2015-24)-mean(2005-14); EDU change = "
                             f"mean(2010-19)-mean(2000-09); MYS derived: {MYS_FORMULA}"
                             if level == "mys_proxy" else
                             "long differences; OUTCOME change = mean(2015-24)-mean(2005-14); EDU change = "
                             "mean(2010-19)-mean(2000-09)")
                if level == "mys_proxy":
                    r["label"] = "derived (MYS proxy) / observed (controls)"
                rows.append(r)
    return rows


def s2_annual(df):
    rows = []
    for outcome in ("eci_sitc", "eci_hs92"):
        for level in EDU_ORDER:
            for L in LAGS:
                x = f"{level}_L{L}"
                for ctrl, extra in CONTROLS.items():
                    res = fe_ols(df, outcome, [x] + list(extra))
                    note = "two-way FE (country+year), CR1 clustered on country"
                    if level == "mys_proxy":
                        note += f"; MYS derived: {MYS_FORMULA}"
                    rows.append(cell_record("S2_FE", outcome, level, L, ctrl, res,
                                            note=note, xname=x))
    return rows


def s3_blocks(bf):
    rows = []
    for outcome in ("eci_sitc", "eci_hs92"):
        for level in EDU_ORDER:
            for L in LAGS:
                x = f"{level}_L{L}"
                for ctrl, extra in CONTROLS.items():
                    res = one_way_fe(bf, outcome, [x] + list(extra))
                    note = "5-year non-overlapping block means; country FE; CR1 clustered on country"
                    if level == "mys_proxy":
                        note += f"; MYS derived: {MYS_FORMULA}"
                    rows.append(cell_record("S3_B5", outcome, level, L, ctrl, res, note=note, xname=x))
    return rows


def s4_within_between(df):
    rows = []
    for outcome in ("eci_sitc", "eci_hs92"):
        for level in EDU_ORDER:
            for L in LAGS:
                x = f"{level}_L{L}"
                extra = ["log_gdppc", "urban"]
                dd = df[["iso3", "year", outcome, x] + extra].dropna().copy()
                # between: country means
                btw = dd.groupby("iso3", as_index=False).agg(
                    {outcome: "mean", x: "mean", "log_gdppc": "mean", "urban": "mean"})
                for ctrl, cols in (("C0", [x]), ("C1", [x, "log_gdppc", "urban"])):
                    res = ols_hc1(btw, outcome, cols)
                    r = cell_record("S4_BETWEEN", outcome, level, L, ctrl, res,
                                    note="country means, HC1 robust", xname=x)
                    rows.append(r)
                # within: two-way FE (identical to S2 by construction; reported as the decomposition leg)
                for ctrl, cols in (("C0", [x]), ("C1", [x, "log_gdppc", "urban"])):
                    res = fe_ols(dd, outcome, cols, min_n=MIN_N, min_cty=MIN_CLUSTERS)
                    r = cell_record("S4_WITHIN", outcome, level, L, ctrl, res,
                                    note="within = two-way FE (country+year), CR1 clustered; "
                                         "identical to S2 by construction", xname=x)
                    rows.append(r)
    return rows


def s5_reverse(df):
    rows = []
    for level in EDU_ORDER:
        for L in LAGS:
            x = f"eci_sitc_L{L}"
            res = fe_ols(df, level, [x] + ["log_gdppc", "urban"])
            note = ("reverse-order descriptive check: outcome = education level, regressor = lagged ECI; "
                    "NO direction claim")
            rows.append(cell_record("S5_REVERSE", "eci_sitc", level, L, "C1", res, note=note, xname=x))
    return rows


def s6_heterogeneity(df):
    """S6: baseline-ECI median split; S2(C1) slope by group; country bootstrap difference."""
    rows = []
    base = df[(df.year >= 1995) & (df.year <= 1999)].groupby("iso3")["eci_sitc"].mean()
    base = base.dropna()
    if len(base) < MIN_CLUSTERS:
        return rows, None
    med = float(np.median(base.values))
    group = pd.Series(np.where(base <= med, "LOW", "HIGH"), index=base.index, name="baseline_grp")
    rng = np.random.Generator(np.random.PCG64(SEED))
    codes = np.array(sorted(base.index.tolist()))
    for L in LAGS:
        x = f"cuat_up_L{L}"  # declared focal: upper-secondary attainment (highest-coverage non-derived level)
        out = {}
        for gname in ("LOW", "HIGH"):
            iso = [c for c in codes if group.loc[c] == gname]
            sub = df[df.iso3.isin(iso)]
            res = fe_ols(sub, "eci_sitc", [x, "log_gdppc", "urban"])
            out[gname] = (res, len(iso))
            r = cell_record("S6_HET", "eci_sitc", "cuat_up", L, "C1", res, xname=x,
                            note=f"baseline-ECI group {gname} (median split at {med:.4f}); "
                                 f"S2(C1); NO sign expectation")
            rows.append(r)
        # bootstrap the LOW-HIGH slope difference by resampling countries with replacement
        def _resample(draw_codes):
            parts = []
            for j, c in enumerate(draw_codes):
                s = df[df.iso3 == c].copy()
                s["boot_id"] = f"{c}~{j}"
                parts.append(s)
            return pd.concat(parts) if parts else df.iloc[0:0]

        diffs = []
        for _ in range(1000):
            draw = rng.choice(codes, size=len(codes), replace=True)
            slopes = {}
            for gname in ("LOW", "HIGH"):
                sub_draw = [c for c in draw if group.loc[c] == gname]
                if len(sub_draw) < 6:
                    continue
                sub = _resample(sub_draw)
                r = fe_ols(sub, "eci_sitc", [x, "log_gdppc", "urban"],
                           entity="boot_id", cluster="boot_id", min_cty=5)
                if "error" not in r:
                    slopes[gname] = r[x]["coef"]
            if "LOW" in slopes and "HIGH" in slopes:
                diffs.append(slopes["LOW"] - slopes["HIGH"])
        if len(diffs) >= 100:
            lo = float(np.percentile(diffs, 2.5)); hi = float(np.percentile(diffs, 97.5))
            rows.append(dict(spec="S6_HET_BOOT", outcome="eci_sitc", level="cuat_up", lag=L,
                             controls="C1", coef=float(np.mean(diffs)), se=float(np.std(diffs, ddof=1)),
                             t=math.nan, p=math.nan, ci_lo=lo, ci_hi=hi,
                             n=len(diffs), n_ctry=len(codes), n_blocks=math.nan,
                             period="1995-2024", label="derived (bootstrap)",
                             note=f"LOW-minus-HIGH slope difference; percentile 95% CI; "
                                  f"B=1000 valid={len(diffs)}; no direction claim"))
        else:
            rows.append(dict(spec="S6_HET_BOOT", outcome="eci_sitc", level="cuat_up", lag=L,
                             controls="C1", coef=math.nan, se=math.nan, t=math.nan, p=math.nan,
                             ci_lo=math.nan, ci_hi=math.nan, n=len(diffs), n_ctry=len(codes),
                             n_blocks=math.nan, period="1995-2024", label="derived (bootstrap)",
                             note=f"insufficient valid bootstrap draws ({len(diffs)})"))
    return rows, dict(median=med, groups=group.to_dict())


def crosscheck_existing():
    """Reproduce 09_relations E5 exactly (row-shift lag, full WDI-wide panel, no controls)."""
    out = []
    wide = pd.read_csv(WDI_WIDE)
    wide = wide.sort_values(["iso3", "year"]).reset_index(drop=True)
    eci = pd.read_csv(ECI_CSV)[["iso3", "year", "eci_hs92"]]
    d = wide.merge(eci, on=["iso3", "year"], how="left").sort_values(["iso3", "year"]).reset_index(drop=True)
    d["log_cmpt_p"] = np.log(d["SE.PRM.CMPT.ZS"].clip(lower=1e-3))
    # exact existing implementation: dropna on the pair, then shift 10 ROWS within country
    dd = d[["iso3", "year", "eci_hs92", "log_cmpt_p"]].dropna().copy()
    dd = dd.sort_values(["iso3", "year"]).reset_index(drop=True)
    dd["log_cmpt_p_shift10"] = dd.groupby("iso3")["log_cmpt_p"].shift(10)
    res = fe_ols(dd, "eci_hs92", ["log_cmpt_p_shift10"], min_n=60, min_cty=8)
    rec = dict(check="E5_replication_rows_shift", coef=math.nan, se=math.nan, n=res.get("n", 0),
               n_ctry=res.get("n_cty", 0), period=res.get("period", ""),
               target_coef=0.5932271376436165, target_se=0.17576985830195632, target_n=253, target_ctry=23)
    if "error" not in res:
        a = res["log_cmpt_p_shift10"]
        rec.update(coef=a["coef"], se=a["se"], n=res["n"], n_ctry=res["n_cty"])
    else:
        rec["note"] = res["error"]
    out.append(rec)
    # same spec with TRUE calendar-year 10y lag on the 1995-2024 window
    d2 = d[(d.year >= 1995) & (d.year <= 2024)].copy()
    right = d2[["iso3", "year", "log_cmpt_p"]].copy()
    right["year"] = right["year"] + 10
    right = right.rename(columns={"log_cmpt_p": "log_cmpt_p_L10"})
    d2 = d2.merge(right, on=["iso3", "year"], how="left")
    res2 = fe_ols(d2, "eci_hs92", ["log_cmpt_p_L10"], min_n=20, min_cty=8)
    rec2 = dict(check="E5_true_year_lag_10", coef=math.nan, se=math.nan, n=res2.get("n", 0),
                n_ctry=res2.get("n_cty", 0), period=res2.get("period", ""),
                target_coef=0.5932271376436165, target_se=0.17576985830195632, target_n=253, target_ctry=23)
    if "error" not in res2:
        a = res2["log_cmpt_p_L10"]
        rec2.update(coef=a["coef"], se=a["se"], n=res2["n"], n_ctry=res2["n_cty"])
    else:
        rec2["note"] = res2["error"]
    out.append(rec2)
    return out


# ---------------------------------------------------------------------------------------
# verdicts
# ---------------------------------------------------------------------------------------
def verdict_for(cells, level, lag):
    """cells: dict (spec, controls) -> record dict. Frozen rule, PRE_DECLARATIONS §4."""
    need = [("S2_FE", "C0"), ("S2_FE", "C1"), ("S3_B5", "C0"), ("S3_B5", "C1")]
    recs = [cells.get(k) for k in need]
    if any(r is None or ("ERROR" in str(r.get("note", ""))) or r.get("n", 0) < MIN_N
           or r.get("n_ctry", 0) < MIN_CLUSTERS for r in recs):
        return "DATA LIMITED", 0, []
    sig = [bool(r["coef"] > 0 and r["ci_lo"] > 0) for r in recs]
    c1 = [bool(cells[("S2_FE", "C1")]["coef"] > 0 and cells[("S2_FE", "C1")]["ci_lo"] > 0),
          bool(cells[("S3_B5", "C1")]["coef"] > 0 and cells[("S3_B5", "C1")]["ci_lo"] > 0)]
    if sum(sig) >= 2 and any(c1):
        return "SUPPORTED", sum(sig), [r["coef"] for r in recs]
    if sum(sig) == 1:
        return "PARTIAL", sum(sig), [r["coef"] for r in recs]
    c1_pos = [cells[("S2_FE", "C1")]["coef"] > 0, cells[("S3_B5", "C1")]["coef"] > 0]
    if all(c1_pos) and not any(c1):
        return "PARTIAL", sum(sig), [r["coef"] for r in recs]
    return "NOT SUPPORTED", sum(sig), [r["coef"] for r in recs]


def build_matrices(rows):
    cells = {}
    for r in rows:
        if r["spec"] in ("S2_FE", "S3_B5"):
            cells[(r["outcome"], r["spec"], r["level"], r["lag"], r["controls"])] = r
    matrix = []
    for outcome in ("eci_sitc", "eci_hs92"):
        for level in EDU_ORDER:
            for L in LAGS:
                c = {(k[1], k[4]): v for k, v in cells.items()
                     if k[0] == outcome and k[2] == level and k[3] == L}
                verd, nsig, coefs = verdict_for(c, level, L)
                matrix.append(dict(outcome=outcome, level=level, lag=L, verdict=verd,
                                   n_sig_cells=nsig,
                                   coef_S2_C0=fnum(c[("S2_FE", "C0")]["coef"]),
                                   coef_S2_C1=fnum(c[("S2_FE", "C1")]["coef"]),
                                   coef_S3_C0=fnum(c[("S3_B5", "C0")]["coef"]),
                                   coef_S3_C1=fnum(c[("S3_B5", "C1")]["coef"]),
                                   note="frozen rule PRE_DECLARATIONS §4"))
    return matrix


# ---------------------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------------------
def main():
    got = sha256_file(PRE_DECL)
    if got != PRE_DECL_SHA:
        raise SystemExit(f"PRE_DECLARATIONS.md sha256 mismatch: {got} != frozen {PRE_DECL_SHA}")

    wide = load_wide()
    df = build_annual(wide)
    bf = block_frame(df)

    rows = []
    rows += s1_long_diff(df)
    rows += s2_annual(df)
    rows += s3_blocks(bf)
    rows += s4_within_between(df)
    rows += s5_reverse(df)
    het_rows, het_meta = s6_heterogeneity(df)
    for r in het_rows:
        rows.append(r)
    cross = crosscheck_existing()

    # write RESULTS_ALL (fixed column order, floats at %.10g)
    cols = ["spec", "outcome", "level", "lag", "controls", "coef", "se", "t", "p", "ci_lo", "ci_hi",
            "n", "n_ctry", "n_blocks", "period", "label", "note"]
    lines = [",".join(cols)]
    for r in rows:
        vals = []
        for c in cols:
            v = r.get(c, "")
            vals.append(fnum(v) if c in ("coef", "se", "t", "p", "ci_lo", "ci_hi", "lag", "n_blocks") else
                        str(v).replace(",", ";"))
        lines.append(",".join(vals))
    (RESULTS / "RESULTS_ALL.csv").write_text("\n".join(lines) + "\n")

    mat = build_matrices(rows)
    mcols = ["outcome", "level", "lag", "verdict", "n_sig_cells", "coef_S2_C0", "coef_S2_C1",
             "coef_S3_C0", "coef_S3_C1", "note"]
    lines = [",".join(mcols)]
    for r in mat:
        lines.append(",".join(str(r.get(c, "")).replace(",", ";") for c in mcols))
    (RESULTS / "VERDICT_MATRIX.csv").write_text("\n".join(lines) + "\n")

    prim = [r for r in mat if r["outcome"] == "eci_sitc"]
    rob = [r for r in mat if r["outcome"] == "eci_hs92"]
    rmap = {(r["level"], r["lag"]): r["verdict"] for r in rob}
    lines = ["level,lag,verdict_primary,verdict_hs92,robust"]
    for r in prim:
        v2 = rmap.get((r["level"], r["lag"]), "")
        lines.append(f"{r['level']},{r['lag']},{r['verdict']},{v2},{'ROBUST' if v2 == r['verdict'] else 'NOT ROBUST'}")
    (RESULTS / "ROBUSTNESS_HS92.csv").write_text("\n".join(lines) + "\n")

    # heterogeneity file
    hcols = ["spec", "outcome", "level", "lag", "controls", "coef", "se", "ci_lo", "ci_hi", "n", "n_ctry", "note"]
    lines = [",".join(hcols)]
    for r in het_rows:
        lines.append(",".join(fnum(r.get(c)) if c in ("coef", "se", "ci_lo", "ci_hi") else
                              str(r.get(c, "")).replace(",", ";") for c in hcols))
    (RESULTS / "HETEROGENEITY.csv").write_text("\n".join(lines) + "\n")

    ccols = ["check", "coef", "se", "n", "n_ctry", "period", "target_coef", "target_se", "target_n",
             "target_ctry", "note"]
    lines = [",".join(ccols)]
    for r in cross:
        lines.append(",".join(fnum(r.get(c)) if c in ("coef", "se", "target_coef", "target_se") else
                              str(r.get(c, "")).replace(",", ";") for c in ccols))
    (RESULTS / "CROSSCHECK_EXISTING.csv").write_text("\n".join(lines) + "\n")

    # manifest
    files = ["RESULTS_ALL.csv", "VERDICT_MATRIX.csv", "ROBUSTNESS_HS92.csv",
             "HETEROGENEITY.csv", "CROSSCHECK_EXISTING.csv"]
    man = {
        "analysis": "education -> ECI (descriptive; no causal/direction claim)",
        "predeclarations": {"path": str(PRE_DECL), "sha256": got},
        "seed": SEED,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "data": [{"path": str(p), "sha256": sha256_file(p)} for p in (WDI_LONG, WDI_WIDE, ECI_CSV)],
        "code": [{"path": str(CODE / "run_edu_eci.py"), "sha256": sha256_file(CODE / "run_edu_eci.py")}],
        "results": [{"path": str(RESULTS / f), "sha256": sha256_file(RESULTS / f)} for f in files],
        "windows": "1995-2024; lags true calendar years 5 and 10",
        "verdict_rule": "PRE_DECLARATIONS §4 (frozen)",
        "labels": "education observed WDI/UIS; mys_proxy DERIVED; ECI observed Growth Lab (CC0)",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "derived_into_manifest_only": "generated_utc differs between runs; results CSVs are byte-stable",
    }
    (RESULTS / "RUN_MANIFEST.json").write_text(json.dumps(man, indent=2) + "\n")

    # console summary
    print("S1/S2/S3/S4/S5/S6 rows:", len(rows))
    print("\nPRIMARY VERDICT MATRIX (eci_sitc):")
    for r in prim:
        print(f"  {r['level']:10s} L={r['lag']:2d}  {r['verdict']:14s} sig={r['n_sig_cells']} "
              f"S2C0={r['coef_S2_C0']} S2C1={r['coef_S2_C1']} S3C0={r['coef_S3_C0']} S3C1={r['coef_S3_C1']}")
    print("\nCROSS-CHECK (existing E5 target 0.5932271376, se 0.1757698583, n=253, 23 cty):")
    for r in cross:
        print(f"  {r['check']}: coef={fnum(r['coef'])} se={fnum(r['se'])} n={r['n']} cty={r['n_ctry']}")


if __name__ == "__main__":
    main()
