#!/usr/bin/env python3
"""Q1 construct audit: effective_fertility (surviving children) vs tfr_observed_1950plus (births).

Design and decision rules: ../PRE_REGISTRATION.md §2. Committed before this script existed.
Usage: python3 -I q1_construct_audit.py <data_dir_with_long_run_panel.csv> > q1_construct_audit.txt
"""
import sys, json
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

base = sys.argv[1].rstrip("/") + "/"
d = pd.read_csv(base + "long_run_panel.csv")
d = d[d.year % 5 == 0].sort_values(["iso3", "year"]).copy()
out = {}

# ---------- descriptive ----------
ov = d[d.effective_fertility.notna() & d.tfr_observed_1950plus.notna()].copy()
ov = ov[ov.year >= 1950]
diff = (ov.tfr_observed_1950plus - ov.effective_fertility)
desc = dict(
    n_overlap_rows=int(len(ov)), n_countries=int(ov.iso3.nunique()),
    year_min=int(ov.year.min()), year_max=int(ov.year.max()),
    median_abs_diff=float(diff.abs().median()), max_abs_diff=float(diff.abs().max()),
    mean_ratio_tfr_over_efr=float((ov.tfr_observed_1950plus / ov.effective_fertility).mean()),
    corr_levels=float(ov[["effective_fertility", "tfr_observed_1950plus"]].corr().iloc[0, 1]),
    afg_1950=dict(
        effective_fertility=float(d[(d.iso3 == "AFG") & (d.year == 1950)].effective_fertility.iloc[0])
        if len(d[(d.iso3 == "AFG") & (d.year == 1950)]) else None,
        tfr_observed_1950plus=float(d[(d.iso3 == "AFG") & (d.year == 1950)].tfr_observed_1950plus.iloc[0])
        if len(d[(d.iso3 == "AFG") & (d.year == 1950)]) else None,
    ),
)
# changes correlation on common years
ci = d[["iso3", "year", "effective_fertility", "tfr_observed_1950plus"]].copy()
g = ci.groupby("iso3")
for c in ("effective_fertility", "tfr_observed_1950plus"):
    ci["d_" + c] = ci.groupby("iso3")[c].shift(-1) - ci[c]
ch = ci.dropna(subset=["d_effective_fertility", "d_tfr_observed_1950plus"])
desc["corr_changes"] = float(ch[["d_effective_fertility", "d_tfr_observed_1950plus"]].corr().iloc[0, 1])
desc["n_change_rows"] = int(len(ch))
# coverage
desc["coverage"] = {
    "efr_rows": int(d.effective_fertility.notna().sum()),
    "tfr_rows": int(d.tfr_observed_1950plus.notna().sum()),
    "both_rows": int(len(ov)),
    "efr_countries": int(d[d.effective_fertility.notna()].iso3.nunique()),
    "tfr_countries": int(d[d.tfr_observed_1950plus.notna()].iso3.nunique()),
}
print("=== Q1 construct audit: effective_fertility (surviving children) vs tfr_observed_1950plus (births)")
print(json.dumps(desc, indent=1))

# ---------- matched-sample ladders ----------
x = d[["iso3", "year", "effective_fertility", "tfr_observed_1950plus", "mean_years_schooling"]].copy()
x = x.rename(columns={"mean_years_schooling": "S"})
g = x.groupby("iso3")
x["Sm10"] = g["S"].shift(2)    # 5-year rows: t-10
x["Sp10"] = g["S"].shift(-2)   # t+10
x = x[x.year >= 1950]
# identical matched sample for BOTH outcomes and every term
x = x.dropna(subset=["effective_fertility", "tfr_observed_1950plus", "S", "Sm10", "Sp10"])
print(f"\n=== matched level sample: n={len(x)} countries={x.iso3.nunique()} years {int(x.year.min())}-{int(x.year.max())}")
for c in ("S", "Sm10", "Sp10"):
    x["z" + c] = (x[c] - x[c].mean()) / x[c].std()

def fit(f, dat):
    return smf.ols(f, dat).fit(cov_type="cluster", cov_kwds={"groups": dat.iso3})

lvl = {}
for F in ("effective_fertility", "tfr_observed_1950plus"):
    lvl[F] = {}
    for lab, rhs in [("S only", "zS"), ("S(t-10), S, S(t+10)", "zSm10 + zS + zSp10"),
                     ("S(t+10) only (future)", "zSp10"), ("S(t-10) only (lagged)", "zSm10")]:
        m = fit(f"{F} ~ {rhs} + C(year) + C(iso3)", x)
        r = {k: (round(float(m.params[k]), 4), round(float(m.bse[k]), 4)) for k in m.params.index if k.startswith("z")}
        r["n"] = int(m.nobs)
        lvl[F][lab] = r
        print(f"  {F:26s} {lab:26s}", r)
# lead/lag ratio from the both-terms model
for F in ("effective_fertility", "tfr_observed_1950plus"):
    c = lvl[F]["S(t-10), S, S(t+10)"]
    lead, lag = c["zSp10"][0], c["zS"][0]
    lvl[F]["lead_lag_ratio_Sp10_over_S"] = (round(lead / lag, 3) if lag != 0 else None)
print("\n  lead/lag ratios (S(t+10) over S(t)):", {F: lvl[F]["lead_lag_ratio_Sp10_over_S"] for F in lvl})
print("  NOTE: these are different constructs; the level ladder is not a horse race and neither outcome corrects the other.")

# ---------- change-direction test, both outcomes, identical sample ----------
y = d[["iso3", "year", "effective_fertility", "tfr_observed_1950plus", "mean_years_schooling"]].copy()
y = y.rename(columns={"mean_years_schooling": "S"})
g = y.groupby("iso3")
for v in ("effective_fertility", "tfr_observed_1950plus", "S"):
    y[f"d{v}_prev"] = g[v].shift(0) - g[v].shift(2)    # t-10 -> t
    y[f"d{v}_next"] = g[v].shift(-2) - g[v].shift(0)   # t -> t+10
    y[f"d{v}_next2"] = g[v].shift(-4) - g[v].shift(-2) # t+10 -> t+20
y = y[y.year >= 1950]
need = ["dS_prev", "dS_next", "dS_next2"]
y = y.dropna(subset=[c for c in y.columns if c.startswith("d")])
print(f"\n=== matched change sample: n={len(y)} countries={y.iso3.nunique()}")
for c in [c for c in y.columns if c.startswith("d")]:
    y["z" + c] = (y[c] - y[c].mean()) / y[c].std()
chg = {}
for F in ("effective_fertility", "tfr_observed_1950plus"):
    chg[F] = {}
    m = fit(f"zd{F}_next ~ zdS_prev + zdS_next + zdS_next2 + C(iso3)", y)
    chg[F]["dF on dS prev/current/next"] = {k: (round(float(m.params[k]), 4), round(float(m.bse[k]), 4)) for k in m.params.index if k.startswith("zd")}
    print(f"  d{F}(t,t+10) on dS prev/current/next ", chg[F]["dF on dS prev/current/next"], "n=", int(m.nobs))
    m2 = fit(f"zdS_next ~ zd{F}_prev + zd{F}_next + zd{F}_next2 + C(iso3)", y)
    chg[F]["dS on dF prev/current/next"] = {k: (round(float(m2.params[k]), 4), round(float(m2.bse[k]), 4)) for k in m2.params.index if k.startswith("zd")}
    print(f"  dS(t,t+10) on d{F} prev/current/next ", chg[F]["dS on dF prev/current/next"], "n=", int(m2.nobs))
print("\n  INTERPRETATION LIMIT: the two outcomes answer different questions (surviving children vs births).")
print("  Neither can 'correct' the other; a differing lead/lag pattern is expected and is not a data error.")

out = dict(descriptive=desc, level_ladder=lvl, change_direction=chg,
           note="effective_fertility = surviving children per woman (reconstructed pre-1950); "
                "tfr_observed_1950plus = births per woman (UN WPP 2024, 1950+). Different constructs.")
json.dump(out, open("q1_construct_audit.json", "w"), indent=1)
