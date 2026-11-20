#!/usr/bin/env python
"""Cluster 4 (regional post-secondary proxy): X10 convergence, X11 gini, X12 gradient.

BINDING LIMITATION: regional tertiary enrolment is NOT observed on disk; there is no
PHL regional tertiary GER/participation series. All cells use regional attainment/
inequality proxies and national tertiary GER as CONTEXT ONLY. No causal or
policy-effect claim.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats  # may not exist; fallback below

BASE = Path("/Users/treymenefee/massification_live/experiments/massification-2026-11-20")
DATA = BASE / "10_massification" / "data"
HERE = BASE / "10_massification" / "extensions" / "lab_2026-11-20_b" / "cluster_4_regional_proxy"
RESULTS = HERE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

LIMITATION = ("LIMITATION: regional tertiary enrolment is NOT observed on disk; there is no PHL "
              "regional tertiary GER/participation series. All cells use regional attainment/"
              "inequality proxies and national tertiary GER as CONTEXT ONLY. No causal or "
              "policy-effect claim. Cohort comparison is descriptive.")

COHORTS = ["cohort 1960-1964", "cohort 1990-1994"]
INDS = ["education_gini", "mean_years_of_schooling"]


def spearman(x, y):
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return np.nan, len(x)
    try:
        r, p = stats.spearmanr(x, y)
    except Exception:
        r = pd.Series(x).corr(pd.Series(y), method="spearman")
        p = np.nan
    return float(r), int(len(x))


def build():
    b = pd.read_csv(DATA / "BASELINE_SERIES.csv")
    b["value"] = pd.to_numeric(b["value"], errors="coerce")
    b = b[(b["iso3"] == "PHL") & (b["indicator"].isin(INDS)) & (b["period"].isin(COHORTS))]
    agg = (b.groupby(["region", "indicator", "period"], as_index=False)
             .agg(mean_value=("value", "mean"), n_rows=("value", "size"),
                  n_missing=("value", lambda s: int(s.isna().sum()))))
    w = agg.pivot_table(index="region", columns=["indicator", "period"], values="mean_value")
    cnt = agg.pivot_table(index="region", columns=["indicator", "period"], values="n_rows")
    return b, agg, w, cnt


def main():
    b, agg, w, cnt = build()
    regions = sorted(agg["region"].unique())

    # rename to short keys
    mys0 = w[("mean_years_of_schooling", COHORTS[0])]
    mys1 = w[("mean_years_of_schooling", COHORTS[1])]
    gin0 = w[("education_gini", COHORTS[0])]
    gin1 = w[("education_gini", COHORTS[1])]

    t = pd.DataFrame({
        "region": regions,
        "mys_1960_1964": [mys0.get(r, np.nan) for r in regions],
        "mys_1990_1994": [mys1.get(r, np.nan) for r in regions],
        "gini_1960_1964": [gin0.get(r, np.nan) for r in regions],
        "gini_1990_1994": [gin1.get(r, np.nan) for r in regions],
        "n_sex_rows_mys": [int(cnt.get(("mean_years_of_schooling", COHORTS[0]), {}).get(r, 0) +
                                cnt.get(("mean_years_of_schooling", COHORTS[1]), {}).get(r, 0)) for r in regions],
        "n_sex_rows_gini": [int(cnt.get(("education_gini", COHORTS[0]), {}).get(r, 0) +
                                 cnt.get(("education_gini", COHORTS[1]), {}).get(r, 0)) for r in regions],
    })
    t["dMYS"] = t["mys_1990_1994"] - t["mys_1960_1964"]
    t["dGini"] = t["gini_1990_1994"] - t["gini_1960_1964"]

    # ---- X10 ----
    rho10, n10 = spearman(t["dMYS"], t["mys_1960_1964"])
    improving = int((t["dMYS"] > 0).sum())
    x10_ok = (not np.isnan(rho10)) and rho10 < 0 and improving >= 12
    x10_verdict = "SUPPORTED" if x10_ok else "NOT SUPPORTED"

    # ---- X11 ----
    rho11, n11 = spearman(t["dGini"], t["gini_1960_1964"])
    fall = int((t["dGini"] <= -0.02).sum())
    u = pd.read_csv(DATA / "UNIVERSALIZATION_SERIES.csv")
    u = u[(u["iso3"] == "PHL") & (u["indicator"] == "ger_tertiary")]
    u["value"] = pd.to_numeric(u["value"], errors="coerce")
    ger = {}
    for y in (1971, 2024):
        row = u[u["year"] == y]
        ger[y] = float(row["value"].iloc[0]) if len(row) else np.nan
    x11_ok = fall >= 10 and (not np.isnan(rho11)) and rho11 < 0
    x11_verdict = "SUPPORTED" if x11_ok else "NOT SUPPORTED"

    # ---- X12 ----
    sub = t.dropna(subset=["mys_1960_1964"]).copy()
    sub["q"] = pd.qcut(sub["mys_1960_1964"], q=4, labels=["Q1", "Q2", "Q3", "Q4"])
    cuts = pd.qcut(sub["mys_1960_1964"], q=4, retbins=True)[1]
    med = sub.groupby("q", observed=True)["dMYS"].median()
    ratio = float(med["Q1"] / med["Q4"]) if med.get("Q1", np.nan) == med.get("Q1", np.nan) else np.nan
    if pd.isna(med.get("Q1", np.nan)) or pd.isna(med.get("Q4", np.nan)) or med.get("Q4", np.nan) == 0:
        ratio = np.nan
    x12_verdict = "SUPPORTED" if (not np.isnan(ratio)) and ratio > 1.0 else "NOT SUPPORTED"

    # ---- write per-experiment result files ----
    out = t[["region", "mys_1960_1964", "mys_1990_1994", "dMYS",
             "gini_1960_1964", "gini_1990_1994", "dGini",
             "n_sex_rows_mys", "n_sex_rows_gini"]].copy()
    for c in ["mys_1960_1964", "mys_1990_1994", "dMYS", "gini_1960_1964", "gini_1990_1994", "dGini"]:
        out[c] = out[c].round(6)
    out = out.sort_values("region").reset_index(drop=True)

    x10 = out.copy()
    x10["experiment"] = "X10"
    x10.to_csv(RESULTS / "X10_convergence.csv", index=False, lineterminator="\n")
    with open(RESULTS / "X10_convergence.csv", "a", newline="\n") as f:
        f.write(f"\nX10 summary: spearman_rho_dMYS_vs_MYS_initial={rho10:.6f},n={n10},regions_dMYS_gt_0={improving}/17,"
                f"verdict={x10_verdict}\n{LIMITATION}\n")

    x11 = out.copy()
    x11["experiment"] = "X11"
    x11.to_csv(RESULTS / "X11_gini.csv", index=False, lineterminator="\n")
    with open(RESULTS / "X11_gini.csv", "a", newline="\n") as f:
        f.write(f"\nX11 summary: regions_dGini_le_-0.02={fall}/17,spearman_rho_dGini_vs_Gini_initial={rho11:.6f},n={n11},"
                f"national_PHL_ger_tertiary_1971_CONTEXT_ONLY={ger[1971]},national_PHL_ger_tertiary_2024_CONTEXT_ONLY={ger[2024]},"
                f"verdict={x11_verdict}\n{LIMITATION}\n")

    x12 = sub.sort_values("mys_1960_1964")[["region", "mys_1960_1964", "mys_1990_1994", "dMYS", "q"]].copy()
    x12 = x12.rename(columns={"q": "quartile_cut"})
    x12["quartile_cut"] = x12["quartile_cut"].astype(str)
    for c in ["mys_1960_1964", "mys_1990_1994", "dMYS"]:
        x12[c] = x12[c].round(6)
    bounds = {"Q1": (float(cuts[0]), float(cuts[1])), "Q2": (float(cuts[1]), float(cuts[2])),
              "Q3": (float(cuts[2]), float(cuts[3])), "Q4": (float(cuts[3]), float(cuts[4]))}
    x12["quartile_bounds"] = x12["quartile_cut"].map(lambda q: f"[{bounds[q][0]:.6f},{bounds[q][1]:.6f}]")
    x12["experiment"] = "X12"
    x12["binding_limitation_note"] = LIMITATION
    x12.to_csv(RESULTS / "X12_gradient.csv", index=False, lineterminator="\n")
    with open(RESULTS / "X12_gradient.csv", "a", newline="\n") as f:
        f.write(f"\nX12 summary: quartile cut-offs=" +
                ";".join(f"{q}:[{bounds[q][0]:.6f},{bounds[q][1]:.6f}]" for q in ["Q1", "Q2", "Q3", "Q4"]) +
                f",median_dMYS_Q1={med.get('Q1', float('nan')):.6f},median_dMYS_Q4={med.get('Q4', float('nan')):.6f},"
                f"ratio_Q1_over_Q4={ratio:.6f},verdict={x12_verdict}\n{LIMITATION}\n")

    # ---- CLUSTER_RESULTS.csv ----
    rows = [
        dict(experiment="X10", cluster="4_regional_post_secondary_proxy",
             question="Do regions with lower initial mean years of schooling gain more across cohorts (regional convergence)?",
             estimand="Spearman rho of dMYS vs MYS_initial across 17 regions (sex-aggregated mean of two sex rows)",
             estimate=f"{rho10:.6f}", se="", ci_low="", ci_high="",
             n=n10, clusters="17 regions", threshold="CONVERGENCE if rho<0 AND >=12/17 regions have dMYS>0",
             verdict=x10_verdict, label="derived",
             note=f"regions with dMYS>0: {improving}/17; sex rows aggregated by mean (n_sex_rows reported per region). {LIMITATION}"),
        dict(experiment="X11", cluster="4_regional_post_secondary_proxy",
             question="Did regional education inequality fall, and did it fall more where initial inequality was higher?",
             estimand="(a) count of regions with dGini<=-0.02; (b) Spearman rho of dGini vs Gini_initial; (c) national PHL ger_tertiary 1971/2024 CONTEXT ONLY",
             estimate=f"count={fall}; rho={rho11:.6f}", se="", ci_low="", ci_high="",
             n=n11, clusters="17 regions", threshold="EQUALIZING if dGini<=-0.02 in >=10/17 regions AND rho(dGini, initial)<0",
             verdict=x11_verdict, label="derived",
             note=f"national PHL ger_tertiary 1971={ger[1971]}, 2024={ger[2024]} (CONTEXT ONLY, not regressed). {LIMITATION}"),
        dict(experiment="X12", cluster="4_regional_post_secondary_proxy",
             question="Whose schooling grew more: bottom vs top quartile of initial attainment?",
             estimand="ratio of median dMYS in bottom quartile (Q1) to top quartile (Q4) of MYS_initial across 17 regions",
             estimate=f"{ratio:.6f}" if not np.isnan(ratio) else "",
             se="", ci_low="", ci_high="",
             n=17, clusters="4 quartiles x regions", threshold="PRO-POOR GRADIENT if ratio>1.0",
             verdict=x12_verdict, label="derived",
             note=f"median dMYS Q1={med.get('Q1', float('nan')):.6f}, Q4={med.get('Q4', float('nan')):.6f}; quartile cut-offs on MYS_initial: Q1<= {cuts[1]:.6f}, Q2<= {cuts[2]:.6f}, Q3<= {cuts[3]:.6f}. {LIMITATION}"),
    ]
    cr = pd.DataFrame(rows)
    cr.to_csv(RESULTS / "CLUSTER_RESULTS.csv", index=False, lineterminator="\n")

    print("rho10", rho10, "improving", improving, "x10", x10_verdict)
    print("fall", fall, "rho11", rho11, "x11", x11_verdict)
    print("medQ1", med.get("Q1"), "medQ4", med.get("Q4"), "ratio", ratio, "x12", x12_verdict)
    print("ger1971", ger[1971], "ger2024", ger[2024])


if __name__ == "__main__":
    main()
