#!/usr/bin/env python3
"""E8 — fee-abolition event study with verified dates and a staggered-adoption-robust estimator.

Main specification uses the 8 dates verified by the independent audit (novelty-review, task-49,
research/codex-source-verification-2026-11-25 @ bfb8c6f): MWI 1994, ETH 1995, UGA 1997, LSO 2000,
TZA 2001, KEN 2003, MOZ 2004, GHA 2005. The 4 unresolved countries (CMR, ZMB, RWA, BDI) enter only the
all-dates sensitivity and are flagged.

Provenance note (see ERRATUM.md §B): fee_dates.csv is byte-identical (sha256
1a08d4652371f7a3c79a54725b79c48429a793e3d88252d170715018ddd8e2ab) between bfb8c6f (the fee-date commit cited
above) and the verified branch head 9a0fd69; the papers cite 9a0fd69. No data changes.

Estimators: Callaway–Sant'Anna with universal base period g-1 and not-yet-treated controls (never-treated
allowed), event time -5..+6, cohort-size-aggregated, country-cluster bootstrap (500). TWFE event study
(country and year FE, binned endpoints) for comparison. Pre-trends ATT(g,g-2), ATT(g,g-3).
Outcomes: WDI primary GER (SE.PRM.ENRR), annual; secondary GER (SE.SEC.ENRR) as a labelled proxy for the
lower-secondary outcome (WDI does not publish annual lower-secondary GER).
Sensitivity: all dates +1 / -1, leave-one-country-out, placebo dates 6 years earlier, all-12-dates set.
"""
import json, os, sys
import numpy as np
import pandas as pd
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RES = os.path.join(HERE, "..", "results")
os.makedirs(RES, exist_ok=True)

SSA = None

def load_region():
    folder = os.path.join(DATA, "wdi_SE.PRM.ENRR")
    meta = [f for f in os.listdir(folder) if f.startswith("Metadata_Country")][0]
    m = pd.read_csv(os.path.join(folder, meta))
    return m[["Country Code", "Region"]].rename(columns={"Country Code": "iso3"})

def load_wdi_outcome(code):
    folder = os.path.join(DATA, f"wdi_{code}")
    csv = [f for f in os.listdir(folder) if f.startswith("API_")][0]
    raw = pd.read_csv(os.path.join(folder, csv), skiprows=4)
    year_cols = [c for c in raw.columns if str(c).strip().isdigit()]
    long = raw.melt(id_vars=["Country Code"], value_vars=year_cols, var_name="year", value_name="value")
    long = long.dropna(subset=["value"]).copy()
    long["year"] = long["year"].astype(int)
    long = long.rename(columns={"Country Code": "iso3"})[["iso3", "year", "value"]]
    return long

def load_fee_dates():
    d = pd.read_csv(os.path.join(DATA, "fee_dates.csv"))
    d["preferred_year"] = pd.to_numeric(d["preferred_year"], errors="coerce")
    return d

def build_panel(code, years):
    y = load_wdi_outcome(code)
    y = y[(y.year >= years[0]) & (y.year <= years[1])]
    return y

def Ymat(panel, countries, years):
    """dict country -> dict year -> value"""
    out = {}
    for iso, g in panel.groupby("iso3"):
        if iso in countries:
            out[iso] = dict(zip(g.year.astype(int), g.value.astype(float)))
    return out

def att_cs(Y, cohort_years, years, event_min=-5, event_max=6, control_rule="not_yet"):
    """Callaway–Sant'Anna ATT(g,t) with universal base g-1, aggregated by event time.

    Y: country -> year -> value. cohort_years: country -> adoption year (only treated).
    Returns (att_gt rows, event-time aggregated rows).
    """
    treated = dict(cohort_years)
    all_years = set(years)
    rows = []
    for g, g_year in treated.items():
        b = g_year - 1
        for e in range(event_min, event_max + 1):
            t = g_year + e
            if t == b or t not in all_years or b not in all_years:
                continue
            # treated change
            if g not in Y or t not in Y[g] or b not in Y[g]:
                continue
            dy_g = Y[g][t] - Y[g][b]
            # controls: never treated or not yet treated at max(t,b)
            ctrls = []
            for c in Y:
                if c == g or (c in treated):
                    continue
                ctrls.append(c)
            for c in Y:
                if c != g and c in treated and treated[c] > max(t, b):
                    ctrls.append(c)
            ctrls = [c for c in ctrls if t in Y[c] and b in Y[c]]
            if len(ctrls) < 3:
                continue
            dy_c = np.mean([Y[c][t] - Y[c][b] for c in ctrls])
            rows.append(dict(g=g, g_year=g_year, t=t, event=e, att=dy_g - dy_c,
                             n_treated=1, n_controls=len(ctrls)))
    df = pd.DataFrame(rows)
    if df.empty:
        return df, pd.DataFrame()
    # cohort sizes (countries) for weighting
    sizes = df.groupby("g_year")["g"].nunique()
    df["w"] = df["g_year"].map(sizes) / df["g_year"].map(sizes).sum()
    ev = df.groupby("event").apply(
        lambda d: pd.Series(dict(att=np.average(d.att, weights=d.w), n=int(len(d)),
                                 n_treated=int(d.n_treated.sum()),
                                 n_controls=int(d.n_controls.mean())))).reset_index()
    return df, ev

def _demean2(a, g1, g2, iters=25):
    """Iterative (alternating-projection) two-way demeaning."""
    a = a.astype(float).copy()
    f1 = pd.factorize(g1)[0]; f2 = pd.factorize(g2)[0]
    c1 = np.bincount(f1); c2 = np.bincount(f2)
    for _ in range(iters):
        a -= (np.bincount(f1, weights=a) / c1)[f1]
        a -= (np.bincount(f2, weights=a) / c2)[f2]
    return a

def twfe_event(Y, cohort_years, years):
    """TWFE event study: country + year FE by alternating projections, event dummies, cluster by country."""
    rows = []
    for c, yy in Y.items():
        g = cohort_years.get(c)
        for t, v in yy.items():
            e = (t - g) if g is not None else -99
            e = max(min(e, 6), -5) if e != -99 else -99
            rows.append(dict(iso3=c, year=t, y=v, event=e))
    d = pd.DataFrame(rows)
    _yrs = sorted(set(years))
    d = d[d.year.between(min(_yrs), max(_yrs))].copy()
    ev_levels = [-5, -4, -3, -2, 0, 1, 2, 3, 4, 5, 6]
    X = np.column_stack([(d.event == e).astype(float).values for e in ev_levels])
    y = _demean2(d.y.values, d.iso3.values, d.year.values)
    Xd = np.column_stack([_demean2(X[:, j], d.iso3.values, d.year.values) for j in range(X.shape[1])])
    XtX = Xd.T @ Xd
    # solve on the design directly (normal equations are badly conditioned here because event dummies are
    # nearly collinear across the few cohorts)
    b = np.linalg.lstsq(Xd, y, rcond=None)[0]
    u = y - Xd @ b
    cl = pd.factorize(d.iso3.values)[0]
    S = np.column_stack([np.bincount(cl, weights=Xd[:, j] * u, minlength=cl.max() + 1) for j in range(Xd.shape[1])])
    V = np.linalg.pinv(XtX) @ (S.T @ S) @ np.linalg.pinv(XtX)
    out = [dict(event=e, att_twfe=float(b[j]), se_twfe=float(np.sqrt(max(V[j, j], 0))))
           for j, e in enumerate(ev_levels)]
    return pd.DataFrame(out)


def boot_rep(args):
    Y, cohort_years, years, seed = args
    rng = np.random.default_rng(seed)
    countries = list(Y)
    draw = rng.choice(countries, size=len(countries), replace=True)
    Yb = {}
    for k, c in enumerate(draw):
        Yb[f"{c}_{k}"] = Y[c]
    coh = {}
    for k, c in enumerate(draw):
        if c in cohort_years:
            coh[f"{c}_{k}"] = cohort_years[c]
    _, ev = att_cs(Yb, coh, years)
    return dict(zip(ev.event, ev.att)) if len(ev) else {}

def main():
    global SSA
    reg = load_region()
    SSA = set(reg.loc[reg.Region.str.contains("Sub-Saharan", na=False), "iso3"])
    fee = load_fee_dates()
    verified = fee[fee.status == "VERIFIED"].copy()
    unresolved = fee[fee.status == "UNRESOLVED"].copy()
    main_coh = dict(zip(verified.iso3, verified.preferred_year.astype(int)))
    all_coh = dict(main_coh)
    # unresolved enter only the all-dates sensitivity, at their script (unverified) date
    for _, r in unresolved.iterrows():
        d = pd.to_numeric(pd.Series([r["script_date"]]), errors="coerce").iloc[0]
        if pd.notna(d):
            all_coh[r["iso3"]] = int(d)
    results = {}
    for outcome, years in [("SE.PRM.ENRR", (1990, 2015)), ("SE.SEC.ENRR", (1990, 2015))]:
        panel = build_panel(outcome, years)
        countries = set(panel.iso3) & SSA
        Y = Ymat(panel, countries, range(years[0], years[1] + 1))
        for label, coh in [("verified8", main_coh), ("all12", all_coh)]:
            coh = {c: g for c, g in coh.items() if c in Y}
            att_gt, ev = att_cs(Y, coh, range(years[0], years[1] + 1))
            pre = ev[ev.event < 0][["event", "att", "n"]] if len(ev) else pd.DataFrame()
            # bootstrap
            with Pool(8) as pool:
                boots = pool.map(boot_rep, [(Y, coh, range(years[0], years[1] + 1), 1000 + i) for i in range(500)])
            bdf = pd.DataFrame(boots)
            ev["se_boot"] = [float(np.std(bdf[e].dropna())) if e in bdf.columns and len(bdf[e].dropna()) else np.nan
                             for e in ev.event]
            ev["ci_lo"] = ev["att"] - 1.96 * ev["se_boot"]
            ev["ci_hi"] = ev["att"] + 1.96 * ev["se_boot"]
            tw = twfe_event(Y, coh, range(years[0], years[1] + 1))
            ev = ev.merge(tw, on="event", how="outer").sort_values("event")
            ev["outcome"] = outcome; ev["dates"] = label
            att_gt["outcome"] = outcome; att_gt["dates"] = label
            ev.to_csv(os.path.join(RES, f"e8_event_{outcome}_{label}.csv"), index=False)
            att_gt.to_csv(os.path.join(RES, f"e8_att_gt_{outcome}_{label}.csv"), index=False)
            results[f"{outcome}_{label}"] = dict(
                n_treated=len(coh), pre_trend_rows=pre.to_dict(orient="records"),
                event_table=ev.to_dict(orient="records"))
            print(f"\n{outcome} {label}: treated {len(coh)}; event study:\n", ev.to_string(index=False))
    # sensitivity: all dates +1, -1; leave-one-out; placebo -6 (primary outcome, verified8)
    panel = build_panel("SE.PRM.ENRR", (1990, 2015))
    countries = set(panel.iso3) & SSA
    Y = Ymat(panel, countries, range(1990, 2016))
    sens = []
    base_coh = {c: g for c, g in main_coh.items() if c in Y}
    base_att, base_ev = att_cs(Y, base_coh, range(1990, 2016))
    base_post = base_ev[base_ev.event >= 0]
    for label, coh in [("all+1", {c: g + 1 for c, g in base_coh.items()}),
                       ("all-1", {c: g - 1 for c, g in base_coh.items()}),
                       ("placebo-6", {c: g - 6 for c, g in base_coh.items()}),
                       ("all12", {c: g for c, g in all_coh.items() if c in Y})]:
        _, ev = att_cs(Y, coh, range(1990, 2016))
        post = ev[ev.event >= 0]
        sens.append(dict(spec=label, n_treated=len(coh),
                         mean_att_post=float(post.att.mean()) if len(post) else None,
                         att_t0=float(ev.loc[ev.event == 0, "att"].iloc[0]) if (ev.event == 0).any() else None))
    for c in base_coh:
        coh = {k: v for k, v in base_coh.items() if k != c}
        _, ev = att_cs(Y, coh, range(1990, 2016))
        post = ev[ev.event >= 0]
        sens.append(dict(spec=f"drop-{c}", n_treated=len(coh),
                         mean_att_post=float(post.att.mean()) if len(post) else None,
                         att_t0=float(ev.loc[ev.event == 0, "att"].iloc[0]) if (ev.event == 0).any() else None))
    sens = pd.DataFrame(sens)
    sens.to_csv(os.path.join(RES, "e8_sensitivity.csv"), index=False)
    print("\nSENSITIVITY\n", sens.to_string(index=False))
    json.dump({"results": results, "sensitivity": sens.to_dict(orient="records")},
              open(os.path.join(RES, "e8_results.json"), "w"), indent=1, default=str)
    print("\nwrote E8 outputs")

if __name__ == "__main__":
    main()
