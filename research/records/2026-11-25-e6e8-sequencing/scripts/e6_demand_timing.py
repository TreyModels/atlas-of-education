#!/usr/bin/env python3
"""E6 — demand-timing on pre-1990 series (task-47), pre-registered design.

Demand proxies (labelled): GGDC 10-Sector non-agricultural employment share (OBSERVED, 42 countries,
1947-2012); WDI urbanisation (OBSERVED, 1960+); WDI industry value-added share (OBSERVED, 1960+); WDI
agricultural value-added share (OBSERVED, 1960+, selection reported); WDI agricultural employment share
(SENSITIVITY ONLY, 1991+, labelled RECONSTRUCTED/modelled).

Onset rules (pre-registered): demand = first year y in window with s(y+10)-s(y) >= +3.0 pp (for shares that
rise), or <= -3.0 pp for agricultural VA share (falls); schooling = first 5-year-grid year with
mean years schooling(y+10)-(y) >= +1.0. A date equal to the first observable year of the series in the window
is left-censored. Classification follows the pre-registered sequencing code (both_exact / schooling_censored /
demand_censored / both_censored), with "reverse_or_tie" a weak inequality, never called reverse.

Outputs: e6_classification.csv (row per country x proxy), e6_summary.csv, e6_inputs_and_hashes.csv,
e6_selection.csv.
"""
import hashlib, json, os, sys
import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
os.makedirs(RES, exist_ok=True)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# ---------------- inputs ----------------
def load_longrun():
    d = pd.read_csv(os.path.join(DATA, "long_run_panel.csv"))
    d = d.dropna(subset=["mean_years_schooling"])
    return d

def load_ggdc():
    g = pd.read_stata(os.path.join(DATA, "ggdc_10sd_2014", "10SD_jan15.dta"))
    e = g[g["Variable"] == "EMP"].copy()
    e["nonag_emp_share"] = 100.0 * (1.0 - e["AGR"] / e["SUM"].replace(0, np.nan))
    e["iso3"] = e["Country"]
    return e[["iso3", "Year", "nonag_emp_share"]].rename(columns={"Year": "year"}).dropna()

WDI = {
    "urban": ("SP.URB.TOTL.IN.ZS", +1, "OBSERVED"),
    "ind_va": ("NV.IND.TOTL.ZS", +1, "OBSERVED"),
    "agri_va": ("NV.AGR.TOTL.ZS", -1, "OBSERVED"),
    "agri_emp": ("SL.AGR.EMPL.ZS", -1, "RECONSTRUCTED/modelled (sensitivity only, 1991+)"),
}

def load_wdi(code):
    folder = os.path.join(DATA, f"wdi_{code}")
    csv = [f for f in os.listdir(folder) if f.startswith("API_")][0]
    raw = pd.read_csv(os.path.join(folder, csv), skiprows=4)
    id_col = "Country Code"
    year_cols = [c for c in raw.columns if c.strip().isdigit()]
    long = raw.melt(id_vars=[id_col], value_vars=year_cols, var_name="year", value_name="value")
    long = long.dropna(subset=["value"])
    long["year"] = long["year"].astype(int)
    long = long.rename(columns={id_col: "iso3"})
    return long[["iso3", "year", "value"]]

def series_from_long(long, value="mean_years_schooling"):
    out = {}
    for iso, g in long.dropna(subset=[value]).groupby("iso3"):
        out[iso] = dict(zip(g["year"].astype(int), g[value].astype(float)))
    return out

def onset(series, delta, direction, w=10, grid=1):
    """First year y in the series (and y+w observable) with change >= delta (up) or <= -delta (down).

    Onsets are searched over the series' full observed range, not only the comparison window, so that a
    take-off before the window is known rather than artificially censored. grid=5 for schooling.
    """
    if not series:
        return None
    ys = sorted(series)
    for y in ys:
        if grid > 1 and y % grid != 0:
            continue
        if (y + w) in series:
            ch = series[y + w] - series[y]
            if direction == "up" and ch >= delta:
                return y
            if direction == "down" and ch <= -delta:
                return y
    return None

def first_observable(series, start, end):
    ys = [y for y in series if start <= y <= end]
    return min(ys) if ys else None

def classify(s, r, s_floor, r_floor):
    """Pre-registered classification, adapted for demand series that start before the window.

    Censoring = onset equals the series' first observable year. Because demand can be censored at its start
    while schooling is observed later, demand-censoring implies demand-first (a WEAK forward inequality), not
    the reverse_or_tie convention of the 1991-start release series; this adaptation is recorded as a deviation.
    """
    if s is None or r is None:
        return "both_censored", "undetermined"
    sc = (s == s_floor)
    rc = (r == r_floor)
    if not sc and not rc:
        return "both_exact", ("forward" if r < s else ("reverse" if s < r else "forward_or_tie" if r == s else "undetermined"))
    if sc and not rc:
        return "schooling_censored", "forward"
    if rc and not sc:
        return "demand_censored", ("forward_or_tie" if s > r_floor else "undetermined")
    return "both_censored", "undetermined"

def run_proxy(name, series, direction, delta_r, sch, window, school_delta=1.0, school_grid=5):
    start, end = window
    rows = []
    for iso in sorted(set(series) & set(sch)):
        s = onset(sch[iso], school_delta, "up", w=10, grid=school_grid)
        r = onset(series[iso], delta_r, direction, w=10, grid=1)
        s_floor = min(sch[iso]) if sch[iso] else None
        r_floor = min(series[iso]) if series[iso] else None
        c, o = classify(s, r, s_floor, r_floor)
        in_window = (s is not None and r is not None and start <= s <= end and start <= r <= end)
        rows.append(dict(proxy=name, iso3=iso, schooling_onset=s, demand_onset=r,
                         schooling_first=s_floor, demand_first=r_floor,
                         classification=c, order=o, both_events_in_window=in_window,
                         demand_lead=(r - s) if (s is not None and r is not None) else None,
                         series_first_year=min(series[iso]), series_last_year=max(series[iso]),
                         schooling_series_label="RECONSTRUCTED (mean years of schooling, long-run panel)"))
    df = pd.DataFrame(rows)
    if df.empty:
        return df, dict(proxy=name, window=f"{start}-{end}", n=0)
    n_all = len(df)
    dfw = df[df["both_events_in_window"]].copy()
    fw = int((dfw["order"] == "forward").sum())
    rv = int((dfw["order"] == "reverse").sum())
    rt = int((dfw["order"] == "reverse_or_tie").sum())
    fwt = int((dfw["order"] == "forward_or_tie").sum())
    un = int((dfw["order"] == "undetermined").sum())
    ident = fw + rv + rt + fwt
    lead = dfw.loc[dfw["order"] == "forward", "demand_lead"].median()
    summ = dict(proxy=name, window=f"{start}-{end}", delta_demand=delta_r, direction=direction,
                n_all=n_all, n_in_window=len(dfw), excluded_events_outside_window=n_all - len(dfw),
                forward=fw, reverse=rv, reverse_or_tie=rt, forward_or_tie=fwt, undetermined=un,
                forward_share_identified=round(100 * fw / ident, 1) if ident else None,
                share_identifiable=round(100 * ident / len(dfw), 1) if len(dfw) else None,
                forward_lower_bound_all=round(100 * fw / len(dfw), 1) if len(dfw) else None,
                forward_upper_bound_all=round(100 * (fw + un) / len(dfw), 1) if len(dfw) else None,
                median_demand_lead_forward=float(lead) if pd.notna(lead) else None)
    return df, summ

def main():
    sch = series_from_long(load_longrun())
    proxies = {}
    gg = load_ggdc()
    proxies["ggdc_nonag_emp"] = (series_from_long(gg, "nonag_emp_share"), +1, "OBSERVED (GGDC 10-Sector EMP, 42 countries, 1947-2012)")
    for key, (code, direction, label) in WDI.items():
        long = load_wdi(code)
        proxies[key] = (series_from_long(long, "value"), direction, label)
    # Primary: full observed overlap (demand onsets often precede 1960, so a 1960 start selects against
    # demand-first cases); windows are robustness, reported with their selection. This ordering is a
    # documented deviation from the pre-registration (which named 1960-2010 primary) because the diagnostic
    # showed the window itself selects; both are reported.
    windows = [(1900, 2012), (1960, 2010), (1965, 2010), (1970, 2015)]
    all_rows, summaries = [], []
    for name, (series, direction, label) in proxies.items():
        for w in windows:
            if name == "agri_emp" and w[0] < 1991:
                continue
            delta = 3.0
            direction_s = "up" if direction > 0 else "down"
            df, summ = run_proxy(name, series, direction_s, delta, sch, w)
            summ["series_label"] = label
            if len(df):
                df["series_label"] = label
                all_rows.append(df)
            summaries.append(summ)
    cls = pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame()
    cls.to_csv(os.path.join(RES, "e6_classification.csv"), index=False)
    summ = pd.DataFrame(summaries)
    summ.to_csv(os.path.join(RES, "e6_summary.csv"), index=False)
    print(summ.to_string(index=False))

    # selection table: which countries enter each proxy's primary window
    sel = []
    for name, (series, direction, label) in proxies.items():
        for iso in sorted(set(series) & set(sch)):
            ys = [y for y in series[iso] if 1960 <= y <= 2010]
            ss = [y for y in sch[iso] if 1960 <= y <= 2010]
            sel.append(dict(proxy=name, iso3=iso, series_first=min(ys) if ys else None,
                            series_last=max(ys) if ys else None,
                            schooling_first=min(ss) if ss else None, schooling_last=max(ss) if ss else None,
                            in_primary=bool(ys and ss)))
    pd.DataFrame(sel).to_csv(os.path.join(RES, "e6_selection.csv"), index=False)

    # exact input hashes
    files = {
        "ggdc_10sd_2014.zip": "https://www.rug.nl/ggdc/docs/10sd_jan15_2014.zip",
        "ggdc_10sd_2014/10SD_jan15.dta": "https://www.rug.nl/ggdc/docs/10sd_jan15_2014.zip (extracted)",
        "pwt1001.dta": "https://dataverse.nl/api/access/datafile/354098 (PWT 10.01)",
        "long_run_panel.csv": "research/records/2026-11-24-next-tests/data/long_run_panel.csv @ origin/research/assessment-and-next-experiments-2026-11-24",
        "event_dates.csv": "research/records/2026-11-25-paper-sequencing-novel/results/event_dates.csv @ origin/research/paper-sequencing-novel-2026-11-25",
    }
    for key, (code, _, _) in WDI.items():
        z = f"wdi_{code}.zip"
        if os.path.exists(os.path.join(DATA, z)):
            files[z] = f"https://api.worldbank.org/v2/en/indicator/{code}?downloadformat=csv"
    rows = []
    for f, src in files.items():
        p = os.path.join(DATA, f)
        if os.path.exists(p):
            rows.append(dict(file=f, source=src, sha256=sha256(p), size_bytes=os.path.getsize(p)))
    pd.DataFrame(rows).to_csv(os.path.join(RES, "e6_inputs_and_hashes.csv"), index=False)
    print(f"\nwrote {len(cls)} classification rows, {len(summ)} summaries, {len(rows)} input hashes")
    json.dump(summ.to_dict(orient="records"),
              open(os.path.join(RES, "e6_summary.json"), "w"), indent=1, default=str)

if __name__ == "__main__":
    main()
