#!/usr/bin/env python3
"""Trend-on-trend check for the fertility page.

The page's levels models regress period TFR on trending covariates (life expectancy,
log GDP per capita). This script asks whether that relation survives:

  (a) first differences: regress change in TFR on change in each covariate, per place
      and pooled;
  (b) Engle-Granger cointegration: regress TFR on each covariate in levels, then test
      the residuals for a unit root (statsmodels coint if installed, otherwise an
      ADF on the residuals with asymptotic MacKinnon N=2 critical values);
  (c) unit-root checks on TFR and the covariates (prerequisite for (b));
  (d) leave-one-place-out spread of the page's stored development ("dev") and
      "full" series, recomputed from fertility-series.json.

Inputs (read-only, from the repo):
  public/research/fertility/fertility-series.json       TFR (obs), page series
  public/research/fertility/fertility-research-full.zip life_asia.json and
                                                        asia_panel_data.json (covariates,
                                                        cross-check of TFR)
Covariates are World Bank series via FRED, 1961-2024. Period TFR, not cohort fertility.

numpy, scipy and pandas are required. statsmodels is used when installed.
Run:  python3 check.py            (writes results.json next to this file)
      python3 check.py --no-statsmodels   (forces the numpy fallback; writes results_fallback.json)
"""
import argparse
import json
import os
import sys
import warnings
import zipfile

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SERIES = os.path.join(REPO, "public", "research", "fertility", "fertility-series.json")
BUNDLE = os.path.join(REPO, "public", "research", "fertility", "fertility-research-full.zip")
PLACES = ["PHL", "THA", "KOR", "JPN", "HKG", "CHN"]
HAC_LAGS = 2
SENS_START = 1964   # sensitivity sample: drops the 1961-63 TFR swings (CHN 3.86 -> 6.09 -> 7.51)

# MacKinnon (1990) asymptotic critical values, used only by the numpy fallback.
EG_CRIT_N2_C = {"1%": -3.90, "5%": -3.34, "10%": -3.04}   # Engle-Granger, 2 variables, constant
ADF_CRIT_C = {"1%": -3.43, "5%": -2.86, "10%": -2.57}     # single series, constant

parser = argparse.ArgumentParser()
parser.add_argument("--no-statsmodels", action="store_true", help="force the numpy/scipy fallback")
args = parser.parse_args()

HAVE_SM = False
if not args.no_statsmodels:
    try:
        import statsmodels
        warnings.filterwarnings("ignore", category=FutureWarning)
        from statsmodels.tsa.stattools import adfuller, coint
        HAVE_SM = True
    except ImportError:
        HAVE_SM = False


# ----------------------------------------------------------------- loading
def load_page_series():
    d = json.load(open(SERIES))
    years = np.array(d["years"], dtype=int)
    obs = {p: np.array(d["places"][p]["obs"], float) for p in PLACES}
    dev = {p: np.array(d["places"][p]["dev"], float) for p in PLACES}
    full = {p: np.array(d["places"][p]["full"], float) for p in PLACES}
    return years, obs, dev, full


def load_covariates(years):
    with zipfile.ZipFile(BUNDLE) as z:
        life = json.loads(z.read("fertility_handoff/life_asia.json"))
        panel = json.loads(z.read("fertility_handoff/asia_panel_data.json"))
    yr = [str(y) for y in years]
    le = {p: np.array([float(life[p]["values"][y]) for y in yr]) for p in PLACES}
    gdp = {p: np.array([float(panel[f"gdp_{p}"]["values"][y]) for y in yr]) for p in PLACES}
    tfr_panel = {p: np.array([float(panel[f"tfr_{p}"]["values"][y]) for y in yr]) for p in PLACES}
    lgdp = {p: np.log(gdp[p]) for p in PLACES}
    return le, lgdp, tfr_panel


# ----------------------------------------------------------------- regression (numpy)
def ols(y, x):
    """OLS of y on [1, x]. Returns classical and Newey-West (Bartlett, HAC_LAGS) inference."""
    X = np.column_stack([np.ones_like(x), x])
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    s2 = float(e @ e) / (n - k)
    se = np.sqrt(np.diag(XtX_inv) * s2)
    S = (X * e[:, None]).T @ (X * e[:, None])
    for lag in range(1, HAC_LAGS + 1):
        w = 1 - lag / (HAC_LAGS + 1)
        G = (X[lag:] * e[lag:, None]).T @ (X[:-lag] * e[:-lag, None])
        S = S + w * (G + G.T)
    V = XtX_inv @ S @ XtX_inv
    se_h = np.sqrt(np.diag(V))
    ssy = float(((y - y.mean()) ** 2).sum())
    return dict(
        n=int(n),
        slope=float(b[1]), intercept=float(b[0]),
        se=float(se[1]), p=float(2 * stats.t.sf(abs(b[1] / se[1]), n - k)),
        se_hac=float(se_h[1]), p_hac=float(2 * stats.norm.sf(abs(b[1] / se_h[1]))),
        r2=float(1 - (e @ e) / ssy), durbin_watson=float(np.sum(np.diff(e) ** 2) / (e @ e)),
    )


# ----------------------------------------------------------------- unit roots and cointegration
def adf_fallback(x, regression="c", lags=1):
    """ADF t-statistic with a fixed lag, numpy only. Critical values are asymptotic."""
    dx = np.diff(x)
    rows, ys = [], []
    for t in range(lags, len(dx)):
        row = [x[t]] + [dx[t - j] for j in range(1, lags + 1)]
        if regression == "c":
            row = [1.0] + row
        rows.append(row)
        ys.append(dx[t])
    X, y = np.array(rows), np.array(ys)
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    s2 = float(e @ e) / (len(y) - X.shape[1])
    cov = s2 * np.linalg.inv(X.T @ X)
    idx = 1 if regression == "c" else 0
    return float(b[idx] / np.sqrt(cov[idx, idx]))


def adf_test(x, regression="c"):
    if HAVE_SM:
        stat, p, lags, nobs, crit, _ = adfuller(x, regression=regression, autolag="AIC")
        return dict(method="statsmodels adfuller (AIC lag)", stat=float(stat), p=float(p),
                    lags=int(lags), crit_5pct=float(crit["5%"]))
    stat = adf_fallback(x, regression)
    return dict(method="numpy ADF, 1 lag, asymptotic crit", stat=stat, p=None, lags=1,
                crit_5pct=ADF_CRIT_C["5%"], reject_5pct=bool(stat < ADF_CRIT_C["5%"]))


def engle_granger(y, x):
    """Engle-Granger: levels regression of y on x, then unit-root test on the residuals."""
    X = np.column_stack([np.ones_like(x), x])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ b
    if HAVE_SM:
        stat, p, crit = coint(y, x.reshape(-1, 1), trend="c", autolag="AIC")[:3]
        return dict(method="statsmodels coint (MacKinnon N=2, constant)", stat=float(stat),
                    p=float(p), crit_1pct=float(crit[0]), crit_5pct=float(crit[1]),
                    crit_10pct=float(crit[2]), reject_5pct=bool(stat < crit[1]),
                    resid_sd=float(resid.std(ddof=1)))
    stat = adf_fallback(resid, regression="n", lags=1)
    return dict(method="numpy Engle-Granger, 1 lag, MacKinnon N=2 crit", stat=stat, p=None,
                crit_1pct=EG_CRIT_N2_C["1%"], crit_5pct=EG_CRIT_N2_C["5%"],
                crit_10pct=EG_CRIT_N2_C["10%"], reject_5pct=bool(stat < EG_CRIT_N2_C["5%"]),
                resid_sd=float(resid.std(ddof=1)))


def block(y, x):
    """Levels OLS, first-difference OLS and Engle-Granger for one place and one covariate."""
    return dict(
        levels=ols(y, x),
        differences=ols(np.diff(y), np.diff(x)),
        engle_granger=engle_granger(y, x),
    )


# ----------------------------------------------------------------- leave-one-place-out summary
def loo_summary(name, obs, pred):
    rows = {}
    for p in PLACES:
        err = obs[p] - pred[p]
        rows[p] = dict(mae_1961_2024=float(np.mean(np.abs(err))),
                       mae_1985_2024=float(np.mean(np.abs(err[-40:]))),
                       err_2024=float(err[-1]))
    mae = np.array([rows[p]["mae_1961_2024"] for p in PLACES])
    return dict(series=name, per_place=rows,
                spread=dict(min=float(mae.min()), max=float(mae.max()), range=float(mae.max() - mae.min()),
                            mean=float(mae.mean()), sd=float(mae.std(ddof=1)),
                            best=PLACES[int(mae.argmin())], worst=PLACES[int(mae.argmax())]))


# ----------------------------------------------------------------- main
def main():
    years, tfr, dev, full = load_page_series()
    le, lgdp, tfr_panel = load_covariates(years)

    data_check = {p: float(np.max(np.abs(tfr[p] - tfr_panel[p]))) for p in PLACES}
    assert max(data_check.values()) < 1e-6, f"page TFR differs from panel TFR: {data_check}"

    covars = {"life_expectancy": le, "log_gdp_pc": lgdp}
    per_place = {}
    for p in PLACES:
        y = tfr[p]
        rec = {"n_levels": int(len(y)), "unit_root": {}, "covariates": {}}
        rec["unit_root"]["TFR_levels"] = adf_test(y)
        rec["unit_root"]["TFR_diff"] = adf_test(np.diff(y))
        for cname, cser in covars.items():
            x = cser[p]
            rec["unit_root"][f"{cname}_levels"] = adf_test(x)
            rec["unit_root"][f"{cname}_diff"] = adf_test(np.diff(x))
            rec["covariates"][cname] = block(y, x)
            i0 = int(np.where(years == SENS_START)[0][0])
            rec.setdefault("sensitivity_%d_2024" % SENS_START, {})[cname] = block(y[i0:], x[i0:])
        per_place[p] = rec

    # pooled over the six places (no place effects, classical and HAC on the stacked sample)
    pooled = {}
    for cname, cser in covars.items():
        ys = np.concatenate([tfr[p] for p in PLACES])
        xs = np.concatenate([cser[p] for p in PLACES])
        dys = np.concatenate([np.diff(tfr[p]) for p in PLACES])
        dxs = np.concatenate([np.diff(cser[p]) for p in PLACES])
        # within-place levels: demean each place, so the comparison with differences is fair
        yw = np.concatenate([tfr[p] - tfr[p].mean() for p in PLACES])
        xw = np.concatenate([cser[p] - cser[p].mean() for p in PLACES])
        pooled[cname] = dict(
            levels_pooled=ols(ys, xs),
            levels_within_place=ols(yw, xw),
            differences_pooled=ols(dys, dxs),
        )

    loo = dict(
        note=("Leave-one-place-out fits are the page's stored series (upstream suite). "
              "Errors below are recomputed here from fertility-series.json."),
        dev=loo_summary("dev (development / survival model)", tfr, dev),
        full=loo_summary("full (+ matching + post-2015 period dummy)", tfr, full),
    )

    out = dict(
        script="experiments/fertility-trend-check/check.py",
        backend="statsmodels" if HAVE_SM else "numpy fallback",
        statsmodels_version=statsmodels.__version__ if HAVE_SM else None,
        sources=dict(series=os.path.relpath(SERIES, REPO), covariates=os.path.relpath(BUNDLE, REPO) +
                     " :: fertility_handoff/life_asia.json, asia_panel_data.json"),
        sample="1961-2024 (n=64 per place), period TFR",
        hac_lags=HAC_LAGS,
        data_check_max_abs_diff_tfr_vs_panel=data_check,
        per_place=per_place,
        pooled=pooled,
        leave_one_place_out=loo,
    )

    dest = os.path.join(HERE, "results.json" if HAVE_SM else "results_fallback.json")
    with open(dest, "w") as f:
        json.dump(out, f, indent=2)

    # printed summary
    print(f"backend: {out['backend']}  -> {dest}")
    rows = []
    for p in PLACES:
        for cname in covars:
            c = per_place[p]["covariates"][cname]
            rows.append(dict(place=p, covariate=cname,
                             b_levels=round(c["levels"]["slope"], 4), p_levels_hac=round(c["levels"]["p_hac"], 4),
                             d_diff=round(c["differences"]["slope"], 4), p_diff_hac=round(c["differences"]["p_hac"], 4),
                             r2_levels=round(c["levels"]["r2"], 3), r2_diff=round(c["differences"]["r2"], 3),
                             eg_stat=round(c["engle_granger"]["stat"], 3),
                             eg_p=None if c["engle_granger"]["p"] is None else round(c["engle_granger"]["p"], 4),
                             eg_crit5=round(c["engle_granger"]["crit_5pct"], 3)))
    print(pd.DataFrame(rows).to_string(index=False))
    print()
    prow = []
    for cname in covars:
        for k in ("levels_pooled", "levels_within_place", "differences_pooled"):
            r = pooled[cname][k]
            prow.append(dict(covariate=cname, model=k, slope=round(r["slope"], 4), p_hac=round(r["p_hac"], 4),
                             r2=round(r["r2"], 3)))
    print(pd.DataFrame(prow).to_string(index=False))
    print()
    for key in ("dev", "full"):
        s = loo[key]["spread"]
        print(f"LOO {key}: MAE min {s['min']:.3f} ({s['best']}), max {s['max']:.3f} ({s['worst']}), "
              f"mean {s['mean']:.3f}, sd {s['sd']:.3f}")


if __name__ == "__main__":
    sys.exit(main())
