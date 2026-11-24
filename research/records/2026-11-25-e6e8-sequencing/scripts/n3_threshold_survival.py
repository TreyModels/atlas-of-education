#!/usr/bin/env python3
"""N3 — threshold smoothing and left-truncated survival dating of schooling take-off.

Variants (pre-registered): schooling threshold Δ_s ∈ {0.5, 1.0, 1.5} (5-year grid, as q1); demand threshold
Δ_r ∈ {2, 3, 5} pp/10y; demand smoothing windows 3, 5, 7 years (centred moving average); schooling is on a
5-year grid, so 3/5/7-year windows collapse to the same points and this is stated, not faked. Dating variants:
q1 unsmoothed; smoothed demand; left-truncated survival dating of schooling onset (observed onset, or for
left-censored countries the empirical median onset among observed onsets ≤ first observable year; lower/upper
bounds of the censoring interval reported for the range). Ties are weak inequalities ("forward_or_tie"), never
called reverse (Codex F14).

Output: n3_table.csv, n3_recommendation.json
"""
import json, os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RES = os.path.join(HERE, "..", "results")
os.makedirs(RES, exist_ok=True)

def load_schooling():
    d = pd.read_csv(os.path.join(DATA, "long_run_panel.csv"))
    d = d.dropna(subset=["mean_years_schooling"])
    return {i: dict(zip(g.year.astype(int), g.mean_years_schooling.astype(float)))
            for i, g in d.groupby("iso3")}

def load_demand():
    g = pd.read_stata(os.path.join(DATA, "ggdc_10sd_2014", "10SD_jan15.dta"))
    e = g[g["Variable"] == "EMP"].copy()
    e["nonag"] = 100.0 * (1.0 - e["AGR"] / e["SUM"].replace(0, np.nan))
    return {i: dict(zip(g2["Year"].astype(int), g2.nonag.astype(float)))
            for i, g2 in e.dropna(subset=["nonag"]).groupby("Country")}

def smooth(series, w):
    if w <= 1:
        return series
    ys = sorted(series)
    out = {}
    for y in ys:
        vals = [series[y2] for y2 in range(y - w // 2, y + w // 2 + 1) if y2 in series]
        if len(vals) >= max(2, w // 2):
            out[y] = float(np.mean(vals))
    return out

def onset(series, delta, direction, w=10, grid=1):
    if not series:
        return None
    for y in sorted(series):
        if grid > 1 and y % grid != 0:
            continue
        if (y + w) in series:
            ch = series[y + w] - series[y]
            if direction == "up" and ch >= delta:
                return y
            if direction == "down" and ch <= -delta:
                return y
    return None

def classify(s, r, s_first, r_first):
    if s is None or r is None:
        return "undetermined"
    if s == s_first and r == r_first:
        return "undetermined"
    if s == s_first:
        return "forward_or_tie"
    if r == r_first:
        return "forward_or_tie"
    if r < s:
        return "forward"
    if s < r:
        return "reverse"
    return "forward_or_tie"

def survival_dating(sch, ds=1.0, grid=5, how="median"):
    """Left-truncated survival dating of schooling take-off.

    Observed onsets from countries whose first grid year is not already above the threshold; left-censored
    countries get the empirical median observed onset conditional on onset <= first_grid_year (median), or the
    interval endpoints (lower = first_year-10, upper = first_year).
    """
    obs = {}
    left = {}
    for iso, s in sch.items():
        first = min(s)
        on = onset(s, ds, "up", w=10, grid=grid)
        if on is None:
            continue
        if on == first:
            left[iso] = first
        else:
            obs[iso] = on
    med = np.median(list(obs.values())) if obs else None
    out = dict(obs)
    for iso, first in left.items():
        if how == "median":
            cand = [v for v in obs.values() if v <= first]
            out[iso] = float(np.median(cand)) if cand else med
        elif how == "lower":
            out[iso] = first - 10
        else:
            out[iso] = first
    return out

def forward_table(sch_date, sch_first, dem, dr, label):
    r_first = {i: min(dem[i]) for i in dem}
    rows = []
    for iso in sorted(set(sch_date) & set(dem)):
        s = sch_date[iso]
        r = onset(dem[iso], dr, "up", w=10, grid=1)
        cls = classify(s, r, sch_first[iso], r_first[iso])
        rows.append(dict(iso3=iso, schooling_onset=s, demand_onset=r, classification=cls,
                         lead=(r - s) if (r is not None) else None))
    d = pd.DataFrame(rows)
    if d.empty:
        return dict(definition=label, n=0)
    fw = int((d.classification == "forward").sum())
    ft = int((d.classification == "forward_or_tie").sum())
    rv = int((d.classification == "reverse").sum())
    un = int((d.classification == "undetermined").sum())
    ident = fw + ft + rv
    lead = d.loc[d.classification == "forward", "lead"].median()
    return dict(definition=label, n=len(d), forward=fw, forward_or_tie=ft, reverse=rv, undetermined=un,
                forward_share_identified=round(100 * fw / ident, 1) if ident else None,
                forward_share_incl_ties=round(100 * (fw + ft) / ident, 1) if ident else None,
                lower_bound_all=round(100 * fw / len(d), 1),
                upper_bound_all=round(100 * (fw + ft + un) / len(d), 1),
                share_identifiable=round(100 * ident / len(d), 1),
                median_lead_forward=float(lead) if pd.notna(lead) else None)

def main():
    sch_raw = load_schooling()
    sch_first = {i: min(s) for i, s in sch_raw.items()}
    dem_raw = load_demand()
    rows = []
    for ds in (0.5, 1.0, 1.5):
        sch = survival_dating(sch_raw, ds=ds, how="median")
        sch_low = survival_dating(sch_raw, ds=ds, how="lower")
        sch_high = survival_dating(sch_raw, ds=ds, how="upper")
        for dr in (2.0, 3.0, 5.0):
            for w in (1, 3, 5, 7):
                dem = {i: smooth(s, w) for i, s in dem_raw.items()}
                rows.append(forward_table(sch, sch_first, dem, dr, f"q1 Δs={ds} Δr={dr} smooth={w}"))
                if w == 1:
                    rows.append(forward_table(sch_low, sch_first, dem, dr, f"survival-lower Δs={ds} Δr={dr}"))
                    rows.append(forward_table(sch_high, sch_first, dem, dr, f"survival-upper Δs={ds} Δr={dr}"))
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(RES, "n3_table.csv"), index=False)
    big = t[t.n >= 20]
    fwd = big.forward_share_identified.dropna()
    rec = dict(
        n_definitions=len(t), n_with_20plus=len(big),
        forward_share_range_identified=[float(fwd.min()), float(fwd.max())] if len(fwd) else None,
        forward_share_median=float(fwd.median()) if len(fwd) else None,
        share_below_75=float((fwd < 75).mean()) if len(fwd) else None,
        q1_default=big[big.definition == "q1 Δs=1.0 Δr=3.0 smooth=1"].to_dict(orient="records"),
        recommendation=("Report the forward share as an interval with its selection and threshold definition; "
                        "never a bare percentage. If the abstract needs one number, give the q1-default share "
                        "with its all-country bounds and state the threshold/smoothing dependence (the range "
                        "across definitions is the honest summary)."),
    )
    json.dump(rec, open(os.path.join(RES, "n3_recommendation.json"), "w"), indent=1, default=str)
    print(t.head(20).to_string(index=False))
    print("\nRANGE among definitions with n>=20:", rec["forward_share_range_identified"],
          "median", rec["forward_share_median"], "share of definitions below 75%:", rec["share_below_75"])
    print("\nQ1 DEFAULT:", rec["q1_default"])

if __name__ == "__main__":
    main()
