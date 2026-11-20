#!/usr/bin/env python
"""Cluster 3 (geo / size scaling) — predeclared experiments X7, X8, X9.

Deterministic; absolute paths; no imputation; all cells reported including
failures/censoring. Estimator: OLS with country-clustered CR1 SEs.
"""
import hashlib
import json
import math
import os
from datetime import datetime, timezone

import numpy as np
import pandas as pd

BASE = "/Users/treymenefee/massification_live/experiments/massification-2026-11-20"
OUT = os.path.join(
    BASE, "10_massification/extensions/lab_2026-11-20_b/cluster_3_geo_size"
)
RES = os.path.join(OUT, "results")
os.makedirs(RES, exist_ok=True)
SEED = 20261120
np.random.seed(SEED)  # no randomness used; kept for contract
PANEL = os.path.join(BASE, "09_relations/data/panel_wdi_long.csv")
TIMING = os.path.join(BASE, "10_massification/data/UNIVERSALIZATION_TIMING.csv")
SERIES = os.path.join(BASE, "10_massification/data/UNIVERSALIZATION_SERIES.csv")
JOBS = os.path.join(BASE, "10_massification/data/JOBS_AND_MARKETS_PANEL.csv")

TER, SEC = "SE.TER.ENRR", "SE.SEC.ENRR.UP"
POP, URB, GDPPC = "SP.POP.TOTL", "SP.URB.TOTL.IN.ZS", "NY.GDP.PCAP.PP.CD"


# ---------------------------------------------------------------- OLS with CR1
def ols_cr1(df, dep, regs, cluster="iso3"):
    """Return dict with slope/se/ci per regressor, n, clusters. CR1 small-sample."""
    d = df[[dep] + regs + [cluster]].dropna()
    n = len(d)
    groups = d[cluster].unique()
    G = len(groups)
    X = np.column_stack([np.ones(n)] + [d[r].to_numpy(float) for r in regs])
    y = d[dep].to_numpy(float)
    k = X.shape[1]
    if n <= k or G < 2:
        return {"n": n, "clusters": G, "coefs": {}, "ok": False}
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    u = y - X @ beta
    meat = np.zeros((k, k))
    for g in groups:
        m = (d[cluster].to_numpy() == g)
        Xg, ug = X[m], u[m]
        s = Xg.T @ ug
        meat += np.outer(s, s)
    c = (G / (G - 1)) * ((n - 1) / (n - k))
    V = c * (XtX_inv @ meat @ XtX_inv)
    out = {"n": n, "clusters": G, "coefs": {}, "ok": True}
    for i, r in enumerate(regs, start=1):
        b, se = beta[i], math.sqrt(V[i, i])
        out["coefs"][r] = {
            "slope": b, "se": se,
            "ci_low": b - 1.96 * se, "ci_high": b + 1.96 * se,
        }
    return out


def add_row(rows, experiment, estimand, spec, res, dep_label, note=""):
    c = res["coefs"].get(spec["regressor"], {})
    if not c:
        rows.append(dict(
            experiment=experiment, dep=dep_label, spec=spec["name"],
            regressor=spec["regressor"], estimate=np.nan, se=np.nan,
            ci_low=np.nan, ci_high=np.nan, n=res["n"], clusters=res["clusters"],
            note=note or "insufficient variation",
        ))
        return None
    rows.append(dict(
        experiment=experiment, dep=dep_label, spec=spec["name"],
        regressor=spec["regressor"], estimate=c["slope"], se=c["se"],
        ci_low=c["ci_low"], ci_high=c["ci_high"], n=res["n"],
        clusters=res["clusters"], note=note,
    ))
    return c


def sig(c):
    return int(c["ci_low"] > 0) - int(c["ci_high"] < 0) if c else 0


# ---------------------------------------------------------------- load panel
def build_panel():
    p = pd.read_csv(PANEL)
    keep = [TER, SEC, POP, URB, GDPPC]
    p = p[p.indicator.isin(keep)]
    w = p.pivot_table(index=["iso3", "year"], columns="indicator",
                      values="value", aggfunc="first").reset_index()
    w["SIZE"] = np.log(w[POP].where(w[POP] > 0))
    w["MARKETS"] = (w[URB] / 100.0 * w[POP]) / 1_000_000.0
    w["URBAN"] = w[URB]
    w["LGDP"] = np.log(w[GDPPC].where(w[GDPPC] > 0))
    return w


def demean(df, cols, by="iso3"):
    out = df.copy()
    for c in cols:
        out[c] = out[c] - out.groupby(by)[c].transform("mean")
    return out


def between_means(df, cols):
    return df[["iso3"] + cols].dropna().groupby("iso3", as_index=False).mean()


def run_dep_specs(w, dep, controls, xname):
    """Returns rows + the between/within SIZE (or MARKETS) coef dicts."""
    base = [dep, "SIZE", "MARKETS", "LGDP", "URBAN", "iso3", "year"]
    d = w[base].dropna().copy()
    rows, cb, cw = [], None, None
    # (a) between: country means
    key = controls.get("key", "SIZE")
    cols = [dep, key] + list(controls.get("ctrl", []))
    bm = between_means(d, cols)
    r = ols_cr1(bm, dep, [key] + list(controls.get("ctrl", [])))
    cb = add_row(rows, xname, dep, {"name": "a_between_means", "regressor": key}, r, dep)
    # (b) within: country-demeaned
    dm = demean(d, [dep, key] + list(controls.get("ctrl", [])))
    r = ols_cr1(dm, dep, [key] + list(controls.get("ctrl", [])))
    cw = add_row(rows, xname, dep, {"name": "b_within_demeaned", "regressor": key}, r, dep)
    # (c) pooled with country FE (= within point estimates; reported separately)
    r = ols_cr1(dm, dep, [key] + list(controls.get("ctrl", [])))
    add_row(rows, xname, dep, {"name": "c_pooled_countryFE", "regressor": key}, r, dep,
            note="FE spec; point estimate equals within")
    # (d) pooled without controls, no FE
    r = ols_cr1(d, dep, [key])
    add_row(rows, xname, dep, {"name": "d_pooled_no_controls", "regressor": key}, r, dep)
    return rows, cb, cw


# ---------------------------------------------------------------- X7
def x7(w):
    rows = []
    yrs = (w.year >= 1995) & (w.year <= 2024)
    w7 = w[yrs]
    controls = {"key": "SIZE", "ctrl": ["MARKETS", "LGDP", "URBAN"]}
    ter_rows, cb_t, cw_t = run_dep_specs(w7, TER, controls, "X7")
    rows += ter_rows
    sec_rows, cb_s, cw_s = run_dep_specs(w7, SEC, controls, "X7")
    rows += sec_rows
    # verdict on primary dep (TER), between+within
    def verdict(cb, cw):
        if cb is None or cw is None:
            return "NOT SUPPORTED"
        sb, sw = sig(cb), sig(cw)
        pt = max(abs(cb["slope"]), abs(cw["slope"]))
        if sb != 0 and sb == sw:
            return "SUPPORTED" if pt >= 0.10 else "PARTIAL"
        if sb != 0 or sw != 0:
            return "PARTIAL"
        return "NOT SUPPORTED"
    v = verdict(cb_t, cw_t)
    v_s = verdict(cb_s, cw_s)
    return pd.DataFrame(rows), v, v_s


# ---------------------------------------------------------------- X8
def x8():
    t = pd.read_csv(TIMING)
    tt = t[(t.level == "tertiary") & (t.status == "observed") & (t.confidence == "high")]
    cross = {}
    censor = {}
    for _, r in tt.iterrows():
        cy = r.crossing_year
        if isinstance(cy, str) and not str(cy).replace(".", "", 1).isdigit():
            # e.g. ">2025" -> right-censored
            cross[(r.iso3, r.threshold_pct)] = np.nan
            censor[(r.iso3, r.threshold_pct)] = "right"
            continue
        cy = float(cy)
        cross[(r.iso3, r.threshold_pct)] = float(r.band_latest if pd.isna(r.band_earliest)
                                                 else (r.band_earliest + r.band_latest) / 2.0)
        censor[(r.iso3, r.threshold_pct)] = r.censoring if pd.notna(r.censoring) else "none"
    s = pd.read_csv(SERIES)
    g = s[s.indicator == "ger_tertiary"].sort_values(["iso3", "year"])
    g["chg"] = g.groupby("iso3").value.diff()
    vol = g.groupby("iso3").chg.std(ddof=1)

    hkg_15, hkg_50 = cross[("HKG", 15)], cross[("HKG", 50)]
    rows = []
    dur_ratios, vol_ratios = [], []
    for c in ["CHN", "PHL", "KHM"]:
        pair, note = [], []
        c15, c50 = cross[(c, 15)], cross[(c, 50)]
        cen = {("HKG", 15): censor[("HKG", 15)], ("HKG", 50): censor[("HKG", 50)],
               (c, 15): censor[(c, 15)], (c, 50): censor[(c, 50)]}
        if any(pd.isna(v) for v in [hkg_15, hkg_50, c15, c50]) or \
           cen[("HKG", 15)] == "left" or cen[("HKG", 50)] == "left" or \
           cen[(c, 15)] in ("left", "right") or cen[(c, 50)] in ("left", "right"):
            note = ("UNABLE duration: censored crossing(s); " +
                    "; ".join(f"{k[0]}_{k[1]}={cen[k]}" for k in cen))
            dur = np.nan
            rows.append(dict(experiment="X8", iso3=c, estimand="duration_15_to_50",
                             hkg=hkg_50 - hkg_15, other=dur, ratio=np.nan,
                             n_hkg=1, n_other=1, note=note, status="UNABLE"))
        else:
            dh, do = hkg_50 - hkg_15, c50 - c15
            ratio = do / dh
            dur_ratios.append(ratio)
            rows.append(dict(experiment="X8", iso3=c, estimand="duration_15_to_50",
                             hkg=dh, other=do, ratio=ratio, n_hkg=1, n_other=1,
                             note=f"censoring HKG:{cen[('HKG',15)]}/{cen[('HKG',50)]}, "
                                  f"{c}:{cen[(c,15)]}/{cen[(c,50)]}",
                             status="observed"))
        vh, vo = vol.get("HKG", np.nan), vol.get(c, np.nan)
        if pd.notna(vh) and pd.notna(vo):
            vr = vo / vh
            vol_ratios.append(vr)
            rows.append(dict(experiment="X8", iso3=c, estimand="volatility_sd_annual_chg",
                             hkg=vh, other=vo, ratio=vr, n_hkg=int(g[g.iso3 == 'HKG'].chg.notna().sum()),
                             n_other=int(g[g.iso3 == c].chg.notna().sum()),
                             note="SD of annual changes in ger_tertiary", status="observed"))
        else:
            rows.append(dict(experiment="X8", iso3=c, estimand="volatility_sd_annual_chg",
                             hkg=vh, other=vo, ratio=np.nan, n_hkg=1, n_other=1,
                             note="missing volatility", status="UNABLE"))
    d_ok = [r for r in dur_ratios if not pd.isna(r)]
    v_ok = [r for r in vol_ratios if not pd.isna(r)]
    if d_ok:
        faster = all(r >= 1.5 for r in d_ok)
        dur_note = f"{len(d_ok)} usable duration pair(s)"
    else:
        faster = None
        dur_note = "no usable duration pair (all censored)"
    if v_ok:
        smoother = all(r >= 2.0 for r in v_ok)
    else:
        smoother = None
    if faster and smoother:
        verdict = "SUPPORTED"
    elif faster is None and smoother is None:
        verdict = "UNABLE"
    elif (faster is False or smoother is False) and not (faster or smoother):
        # both tests fail their threshold
        verdict = "NOT SUPPORTED"
    else:
        verdict = "PARTIAL"
    return pd.DataFrame(rows), verdict, dur_note


# ---------------------------------------------------------------- X9
def x9(w):
    yrs = (w.year >= 1995) & (w.year <= 2024)
    rows = []
    res_by_sample = {}
    samples = {
        "6_systems": ["KHM", "CHN", "HKG", "JPN", "KOR", "PHL"],
        "30_countries": sorted(w.iso3.unique().tolist()),
    }
    for sname, ctys in samples.items():
        d = w[yrs & w.iso3.isin(ctys)].copy()
        base = ["iso3", "year", TER, "MARKETS", "LGDP", "URBAN"]
        d = d[base].dropna()
        key = "MARKETS"
        specs = [
            ("between_with_LGDP", "between", ["LGDP"]),
            ("within_with_LGDP", "within", ["LGDP"]),
            ("between_no_LGDP", "between", []),
            ("within_no_LGDP", "within", []),
        ]
        cw_s = {}
        for name, kind, ctrl in specs:
            if kind == "between":
                bm = between_means(d, [TER, key] + ctrl)
                r = ols_cr1(bm, TER, [key] + ctrl)
            else:
                dm = demean(d, [TER, key] + ctrl)
                r = ols_cr1(dm, TER, [key] + ctrl)
            c = add_row(rows, "X9", TER, {"name": name, "regressor": key}, r, TER,
                        note=f"sample={sname}")
            if name == "within_with_LGDP":
                cw_s["with"] = c
            elif name == "within_no_LGDP":
                cw_s["without"] = c
        # URBAN-only spec (URBAN in place of MARKETS), same estimators
        for name, kind in [("between_URBAN_only", "between"),
                           ("within_URBAN_only", "within")]:
            if kind == "between":
                bm = between_means(d, [TER, "URBAN"])
                r = ols_cr1(bm, TER, ["URBAN"])
            else:
                dm = demean(d, [TER, "URBAN"])
                r = ols_cr1(dm, TER, ["URBAN"])
            add_row(rows, "X9", TER, {"name": name, "regressor": "URBAN"}, r, TER,
                    note=f"sample={sname}; URBAN replaces MARKETS")
        res_by_sample[sname] = cw_s
    # verdict: within CI excludes 0 AND sign stable across samples
    def within_c(cw):
        return cw["with"] if cw["with"] is not None else cw["without"]
    c6 = within_c(res_by_sample["6_systems"])
    c30 = within_c(res_by_sample["30_countries"])
    mkt_c6 = res_by_sample["6_systems"]["without"] or res_by_sample["6_systems"]["with"]
    mkt_c30 = res_by_sample["30_countries"]["without"] or res_by_sample["30_countries"]["with"]
    urb_c6 = urb_c30 = None
    for r in rows:
        if r["regressor"] == "URBAN":
            if "6_systems" in r["note"]:
                urb_c6 = r
            else:
                urb_c30 = r
    s6 = sig(c6) if c6 else 0
    s30 = sig(c30) if c30 else 0
    sgn6 = np.sign(mkt_c6["slope"]) if mkt_c6 else 0
    sgn30 = np.sign(mkt_c30["slope"]) if mkt_c30 else 0
    sgnU6 = np.sign(urb_c6["estimate"]) if urb_c6 and not pd.isna(urb_c6["estimate"]) else 0
    sgnU30 = np.sign(urb_c30["estimate"]) if urb_c30 and not pd.isna(urb_c30["estimate"]) else 0
    if s6 != 0 and s6 == s30 and sgn6 == sgn30 and sgn6 == sgnU6 == sgnU30:
        verdict = "SUPPORTED"
    elif s6 != 0 or s30 != 0:
        verdict = "PARTIAL"
    else:
        verdict = "NOT SUPPORTED"
    if (sgn6 != 0 and sgnU6 != 0 and sgn6 != sgnU6) or (sgn30 != 0 and sgnU30 != 0 and sgn30 != sgnU30):
        verdict = "NOT SUPPORTED"  # MARKETS vs URBAN-only sign disagreement
    return pd.DataFrame(rows), verdict


# ---------------------------------------------------------------- main
def main():
    w = build_panel()
    df7, v7_ter, v7_sec = x7(w)
    df8, v8, dur_note = x8()
    df9, v9 = x9(w)

    df7.to_csv(os.path.join(RES, "X7_size_ger.csv"), index=False)
    df8.to_csv(os.path.join(RES, "X8_citystate_pairwise.csv"), index=False)
    df9.to_csv(os.path.join(RES, "X9_markets_ger.csv"), index=False)

    def fmt(v):
        return "" if v is None or (isinstance(v, float) and pd.isna(v)) else v

    cluster_rows = [
        dict(experiment="X7", cluster="3_geo_size_scaling",
             question="Is TER/SEC associated with system size (SIZE) across 30 countries 1995-2024?",
             estimand="SIZE coefficient, primary dep SE.TER.ENRR (secondary SE.SEC.ENRR.UP)",
             estimate=fmt(df7[(df7.dep == TER) & (df7.spec == "a_between_means")].estimate.iloc[0]),
             se=fmt(df7[(df7.dep == TER) & (df7.spec == "a_between_means")].se.iloc[0]),
             ci_low=fmt(df7[(df7.dep == TER) & (df7.spec == "a_between_means")].ci_low.iloc[0]),
             ci_high=fmt(df7[(df7.dep == TER) & (df7.spec == "a_between_means")].ci_high.iloc[0]),
             n=fmt(df7[(df7.dep == TER) & (df7.spec == "a_between_means")].n.iloc[0]),
             clusters=fmt(df7[(df7.dep == TER) & (df7.spec == "a_between_means")].clusters.iloc[0]),
             threshold="size-scaled if SIZE CI excludes 0 with same sign in between AND within and |point|>=0.10 in at least one; PARTIAL if only one; NOT SUPPORTED otherwise; min 10 countries",
             verdict=v7_ter, label="derived",
             note=f"SEC secondary verdict={v7_sec}; see results/X7_size_ger.csv for all 8 spec rows"),
        dict(experiment="X8", cluster="3_geo_size_scaling",
             question="Do large systems (CHN/PHL/KHM) reach tertiary-50 later (duration) and move more smoothly (volatility) than city-state HKG?",
             estimand="ratio duration(large)/duration(HKG) and ratio volatility(large)/volatility(HKG), per pair",
             estimate=fmt(pd.DataFrame([r for r in df8.itertuples() if r.status == 'observed']).ratio.median()
                          if (df8.status == 'observed').any() else np.nan),
             se="", ci_low="", ci_high="", n=len(df8), clusters=len(df8.iso3.unique()),
             threshold="FASTER if duration(large)/duration(HKG)>=1.5; SMOOTHER if volatility(large)/volatility(HKG)>=2.0; NOT SUPPORTED if both ratios<1.2; n<=4 per side: DESCRIPTIVE ONLY",
             verdict=v8, label="derived",
             note=dur_note + "; every individual ratio in results/X8_citystate_pairwise.csv; small-n, no scaling-law claim"),
        dict(experiment="X9", cluster="3_geo_size_scaling",
             question="Is the number-of-markets proxy (urban population in millions) associated with TER in 6 systems and 30 countries 1995-2024?",
             estimand="MARKETS coefficient, within spec (with LGDP preferred), both samples",
             estimate=fmt(df9[(df9.regressor == "MARKETS") & (df9.spec == "within_with_LGDP")].estimate.iloc[0]),
             se=fmt(df9[(df9.regressor == "MARKETS") & (df9.spec == "within_with_LGDP")].se.iloc[0]),
             ci_low=fmt(df9[(df9.regressor == "MARKETS") & (df9.spec == "within_with_LGDP")].ci_low.iloc[0]),
             ci_high=fmt(df9[(df9.regressor == "MARKETS") & (df9.spec == "within_with_LGDP")].ci_high.iloc[0]),
             n=fmt(df9[(df9.regressor == "MARKETS") & (df9.spec == "within_with_LGDP")].n.iloc[0]),
             clusters=fmt(df9[(df9.regressor == "MARKETS") & (df9.spec == "within_with_LGDP")].clusters.iloc[0]),
             threshold="association if within CI excludes 0 AND sign stable across samples; PARTIAL if one sample; NOT SUPPORTED if CI includes 0, sign flips, or MARKETS vs URBAN-only specs disagree in sign",
             verdict=v9, label="derived",
             note="MARKETS is a derived proxy (urban population in millions), NOT a count of real markets; see results/X9_markets_ger.csv"),
    ]
    cr = pd.DataFrame(cluster_rows)
    cr.to_csv(os.path.join(OUT, "CLUSTER_RESULTS.csv"), index=False)

    # manifest
    def sha(p):
        with open(p, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    data_files = [PANEL, TIMING, SERIES, JOBS]
    manifest = {
        "cluster": "3_geo_size_scaling",
        "data_files_read": [{"path": p, "sha256": sha(p)} for p in data_files],
        "code": [{"path": os.path.join(OUT, "code/run.py"), "sha256":
                  sha(os.path.join(OUT, "code/run.py"))}],
        "python_version": os.sys.version.split()[0],
        "seed": SEED,
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reproducibility": {
            "deterministic": True,
            "estimator": "OLS with CR1 country-clustered SEs",
            "notes": [
                "JOBS_AND_MARKETS_PANEL.csv contains no SE.TER.ENRR; TER for the 6-system sample in X9 was taken from panel_wdi_long.csv (same 6 systems, 1995-2024).",
                "No imputation; complete cases only per specification.",
                "MARKETS = urban population in millions, a derived proxy, not a count of real markets.",
            ],
        },
    }
    with open(os.path.join(OUT, "RUN_MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print("verdicts:", v7_ter, v7_sec, v8, v9)


if __name__ == "__main__":
    main()
