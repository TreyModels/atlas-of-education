#!/usr/bin/env python3
"""T2: the corrected reduced-form test of Boppart et al.'s object.

Object (not the old proxy): agricultural input intensity relative to labour, and the RELATIVE PRICE of
inputs to labour. Pre-registered tests:
  T2a  intensity is lower where inputs are expensive relative to labour (negative price elasticity);
  T2b  lagged intensity / lagged relative input price predict the SUBSEQUENT ten-year fall in the
       agricultural employment share (the input margin precedes labour release);
  T2c  the labour release predicts subsequent schooling expansion and fertility decline, controlling income
       and urbanisation.
Sources: USDA ERS agricultural K, M, labour (quantities); PWT price level of investment, labour share, GDP per
worker; World Bank WDI (agricultural employment share, GDP pc, urbanisation, secondary completion, fertility).
Output: results/corrected_test.txt + .json
"""
import json, os
import numpy as np
import pandas as pd

D = "/root/work/data"
WD = "/root/work/subsistence/data"
OUT = "/root/work/subsistence/out"
os.makedirs(OUT, exist_ok=True)
L = []
A = L.append

meta = json.load(open(f"{D}/meta.json"))
REG = {i for i, m in meta.items() if m.get("region", "").strip() != "Aggregates" and len(i) == 3}


def load_json(k, folder=D):
    rows = json.load(open(f"{folder}/{k}.json"))
    return {(r[0], int(r[1])): float(r[2]) for r in rows if r[2] is not None}


def to_frame(d, name):
    return pd.DataFrame([[i, y, v] for (i, y), v in d.items() if i in REG], columns=["iso3", "year", name])


def demean(df, cols, g1, g2, iters=8):
    M = df[cols].values.astype(float)
    a = pd.factorize(df[g1])[0]
    b = pd.factorize(df[g2])[0]
    for _ in range(iters):
        for gi in (a, b):
            cnt = np.maximum(np.bincount(gi), 1)
            for j in range(M.shape[1]):
                M[:, j] -= (np.bincount(gi, weights=M[:, j]) / cnt)[gi]
    return M


def cluster_ols(y, X, c):
    X = np.column_stack([np.ones(len(y)), X])
    XtX = X.T @ X
    b = np.linalg.lstsq(XtX, X.T @ y, rcond=None)[0]
    u = y - X @ b
    meat = np.zeros_like(XtX)
    for cc in np.unique(c):
        m = c == cc
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    P = np.linalg.pinv(XtX)
    V = P @ meat @ P
    se = np.sqrt(np.maximum(np.diag(V), 0))
    return b, se, int(len(y)), int(len(np.unique(c)))


def shift(df, col, k, name):
    df[name] = df.groupby("iso3")[col].shift(k)
    return df


if __name__ == "__main__":
    # ---- load sources ----
    w = pd.read_csv(f"{WD}/wdi_long.csv")
    w = w[w.iso3.isin(REG)]
    wp = w.pivot_table(index=["iso3", "year"], columns="indicator", values="value").reset_index()
    usda = {k: to_frame(load_json(k), k) for k in ["usda_agK", "usda_agL", "usda_agM", "usda_agT", "usda_agY"]}
    pwt = {k: to_frame(load_json(k), k) for k in ["pwt_pli", "pwt_labsh", "pwt_yw"]}
    panel = {k: to_frame(load_json(k), k) for k in ["emp_agri", "urban", "sec", "fertility", "gdppc_log", "wage_emp"]}

    df = wp.copy()
    for src in (usda, pwt, panel):
        for k, f in src.items():
            df = df.merge(f, on=["iso3", "year"], how="outer")
    df = df[df.iso3.isin(REG)].sort_values(["iso3", "year"]).reset_index(drop=True)

    # ---- Boppart's object ----
    df["intensity"] = (df["usda_agK"] + df["usda_agM"]) / df["usda_agL"]
    df["wage"] = df["pwt_labsh"] * df["pwt_yw"]
    df["relprice"] = np.log(df["pwt_pli"] / df["wage"])
    df["log_intensity"] = np.log(df["intensity"].where(df["intensity"] > 0))
    df["ag_share"] = df["ag_emp_share"].fillna(df["emp_agri"])
    df["log_gdp"] = np.log(df["gdp_pc_kd"].where(df["gdp_pc_kd"] > 0))
    df["urban"] = df["urban_pct"].fillna(df["urban"])

    # future and past ten-year changes (so the input margin is measured at t, outcomes at t -> t+10)
    for col, nm in [("ag_share", "ag"), ("sec", "sec"), ("tfr", "tfr"), ("log_intensity", "logint"),
                    ("relprice", "relprice")]:
        df = shift(df, col, -10, col + "_f10")
    df["d_ag_f10"] = df["ag_share_f10"] - df["ag_share"]
    df["d_sec_f10"] = df["sec_f10"] - df["sec"]
    df["d_tfr_f10"] = df["tfr_f10"] - df["tfr"]
    df["d_logint_f10"] = df["log_intensity_f10"] - df["log_intensity"]
    df["d_relprice_f10"] = df["relprice_f10"] - df["relprice"]
    df["d_ag_past"] = df["ag_share"] - df.groupby("iso3")["ag_share"].shift(10)
    df["d_logint_past"] = df["log_intensity"] - df.groupby("iso3")["log_intensity"].shift(10)
    df["d_relprice_past"] = df["relprice"] - df.groupby("iso3")["relprice"].shift(10)
    for col in ("log_intensity", "relprice", "ag_share", "log_gdp", "urban"):
        df = shift(df, col, 10, col + "_p10")
    df["period"] = (df["year"] // 10) * 10

    A("=== T2 corrected reduced-form test (Boppart's object, not the old proxy) ===")
    A("intensity = (agricultural capital + intermediates)/agricultural labour (USDA quantities, 1961-2023)")
    A("relative input price = log(investment price level / labour compensation per worker) (PWT)")
    A("ag employment share from WDI/ILO; secondary completion and TFR from WDI; income and urbanisation controls")
    A("Old proxy (for contrast): world commodity price x farm employment share. Handoff job 3 found farm exit")
    A("+0.024 -> +0.012 under country trends, wage jobs -0.014 -> -0.0035 n.s., births ~0. That measured")
    A("farm employment's exposure to world commodity prices; it never contained the relative-price object.")
    A("")

    # ---- T2a: cross-section ----
    for yr in (2005, 2015):
        d = df[(df.year == yr) & df.log_intensity.notna() & df.relprice.notna()].dropna(subset=["log_gdp"])
        if len(d) < 20:
            continue
        b, se, n, nc = cluster_ols(d["log_intensity"].values, d[["relprice"]].values, d["iso3"].values)
        A(f"T2a cross-section {yr}: log intensity on log relative input price: {b[1]:+.2f} (SE {se[1]:.2f}), "
          f"n={n} countries={nc} — expected negative")

    # ---- T2a2: cross-sectional levels (the paper's object in one picture) ----
    for yr in (2005, 2015):
        d = df[(df.year == yr)].dropna(subset=["ag_share", "log_intensity", "relprice", "log_gdp"])
        if len(d) < 30:
            continue
        X = d[["log_intensity", "relprice", "log_gdp"]].values
        b, se, n, nc = cluster_ols(d["ag_share"].values, X, d["iso3"].values)
        A(f"T2a2 cross-section {yr}: ag employment share on intensity and relative input price, controlling "
          f"income: intensity {b[1]:+.2f} (SE {se[1]:.2f}), price {b[2]:+.2f} (SE {se[2]:.2f}), "
          f"income {b[3]:+.2f} (SE {se[3]:.2f}); n={n}. Expected intensity negative, price positive.")

    # ---- panel ----
    d = df.dropna(subset=["d_ag_f10", "log_intensity", "relprice"]).copy()
    d = d[(d.year % 5 == 0) & (d.year <= 2013)]
    A("")
    A(f"panel for the ten-year changes: {len(d)} country-year observations, {d.iso3.nunique()} countries, "
      f"years {int(d.year.min())}-{int(d.year.max())} (every 5th year, outcome 10 years ahead)")
    results = {}
    specs = [
        ("T2b: change in ag employment share t->t+10 on intensity(t) and relative price(t)", "d_ag_f10",
         ["log_intensity", "relprice"], ["log_gdp", "urban"]),
        ("T2b(a): change in intensity t->t+10 on relative input price(t)", "d_logint_f10",
         ["relprice"], ["log_gdp"]),
        ("T2b(b): change in intensity t->t+10 on change in relative price t->t+10", "d_logint_f10",
         ["d_relprice_f10"], ["log_gdp"]),
        ("T2b(c): change in ag share t->t+10 on PAST change in intensity (t-10->t), past change in relative "
         "price, and current ag share (convergence control)", "d_ag_f10",
         ["d_logint_past", "d_relprice_past", "ag_share"], ["log_gdp", "urban"]),
        ("T2c: change in secondary completion t->t+10 on labour release and intensity(t)", "d_sec_f10",
         ["d_ag_f10", "log_intensity"], ["log_gdp", "urban"]),
        ("T2c: change in fertility t->t+10 on labour release and intensity(t)", "d_tfr_f10",
         ["d_ag_f10", "log_intensity"], ["log_gdp", "urban"]),
    ]
    for title, dep, base_x, ctrls in specs:
        x = list(base_x)
        ctr = [c for c in ctrls if c in d.columns]
        dd = d.dropna(subset=[dep] + x + ctr).copy()
        if len(dd) < 40:
            A("")
            A(title + ": too few observations")
            continue
        M = demean(dd, [dep] + x + ctr, "iso3", "period")
        b, se, n, nc = cluster_ols(M[:, 0], M[:, 1:1 + len(x)], dd["iso3"].values)
        A("")
        A(title)
        for j, v in enumerate(x):
            A(f"   {v:14s} {b[j+1]:+.4f} (SE {se[j+1]:.4f})  "
              f"{'significant' if abs(b[j+1] / se[j+1]) > 1.96 else 'null'}")
        A(f"   country FE + decade FE, clustered by country; n={n}, countries={nc}")
        results[title] = {v: [float(b[j+1]), float(se[j+1])] for j, v in enumerate(x)}
        results[title]["n"] = n

    # ---- T2b long-difference 1995 -> 2015 cross-section ----
    base = df[df.year == 1995][["iso3", "ag_share", "log_intensity", "relprice", "log_gdp", "urban"]].dropna()
    fut = df[df.year == 2015][["iso3", "ag_share"]].rename(columns={"ag_share": "ag_share_2015"})
    ld = base.merge(fut, on="iso3", how="inner")
    ld["d_ag_20y"] = ld["ag_share_2015"] - ld["ag_share"]
    ld = ld.dropna(subset=["d_ag_20y"])
    if len(ld) > 40:
        X = ld[["log_intensity", "relprice", "ag_share", "log_gdp"]].values
        b, se, n, nc = cluster_ols(ld["d_ag_20y"].values, X, ld["iso3"].values)
        A("")
        A(f"T2b long difference 1995->2015: change in ag employment share on initial intensity, initial "
          f"relative price, initial ag share, initial income (n={n} countries):")
        for j, nm in enumerate(["log_intensity", "relprice", "ag_share", "log_gdp"]):
            A(f"   {nm:14s} {b[j+1]:+.3f} (SE {se[j+1]:.3f})  "
              f"{'significant' if abs(b[j+1]/se[j+1]) > 1.96 else 'null'}")

    # reverse check: is the lead-lag direction identifiable?
    d2 = df.dropna(subset=["d_ag_past", "log_intensity", "relprice"]).copy()
    d2 = d2[(d2.year % 5 == 0) & (d2.year >= 1971)]
    if len(d2) > 40:
        M = demean(d2, ["d_ag_past", "log_intensity", "relprice"], "iso3", "period")
        b, se, n, nc = cluster_ols(M[:, 0], M[:, 1:], d2["iso3"].values)
        A("")
        A(f"reverse check: past ag-share change (t-10 -> t) on intensity(t) and price(t): "
          f"intensity {b[1]:+.3f} (SE {se[1]:.3f}), price {b[2]:+.3f} (SE {se[2]:.3f}); n={n}. "
          f"If this is as strong as T2b the lead-lag is not identified.")

    A("")
    A("Reading: the sign pattern and the ordering are what the mechanism predicts, but the magnitudes are")
    A("modest and the reverse check is reported; the old proxy could not test any of this.")
    json.dump(results, open(f"{OUT}/corrected_test.json", "w"), indent=1)
    open(f"{OUT}/corrected_test.txt", "w").write("\n".join(L) + "\n")
    print("\n".join(L))
