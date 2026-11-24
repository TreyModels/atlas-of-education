#!/usr/bin/env python3
"""E11 change-on-change placebo ladder (Frisch-Waugh-Lovell implementation).

Design and decision rules: ../PRE_REGISTRATION.md §3. Committed before this script existed.
Usage: python3 -I e11_ladder.py <project_data_dir> <raw_dir> > e11_ladder.txt

FE modes:
  country_decade          country FE + decade FE (baseline)
  country_trend_decade    country FE + country-specific linear trend + decade FE
Both are implemented by residualising the outcome, the key regressors and the controls on the FE design
(np.linalg.lstsq, rank-deficiency safe), then OLS of residualised y on residualised x with country-clustered SEs.
This is exactly the full-model estimator by FWL and avoids singular design matrices.
"""
import sys, json, os
import numpy as np
import pandas as pd
import statsmodels.api as sm

DATA = sys.argv[1].rstrip("/") + "/"
RAW = sys.argv[2].rstrip("/") + "/"

meta = json.load(open(DATA + "meta.json"))
ISOS = sorted(i for i, m in meta.items() if len(i) == 3 and (m.get("region") or "").strip() != "Aggregates")


def load_json(name):
    d = {}
    for r in json.load(open(DATA + name + ".json")):
        if r[2] is None:
            continue
        iso, yr, v = r[0], int(r[1]), float(r[2])
        if iso in ISOS and 1960 <= yr <= 2024:
            d[(iso, yr)] = v
    return d


def load_csv(path, col):
    d = {}
    if not os.path.exists(path):
        return d
    for r in pd.read_csv(path).to_dict("records"):
        try:
            iso, yr, v = r["code"], int(float(r["year"])), r[col]
            if iso in ISOS and v == v and 1960 <= yr <= 2024:
                d[(iso, yr)] = float(v)
        except (KeyError, TypeError, ValueError):
            pass
    return d


SER = {m: load_json(m) for m in ["fertility", "gdppc_log", "urban", "sec", "lsc",
                                 "prm_cmp", "ter", "gpi_sec", "gpi_ter"]}
SER["gdppc_log"] = {k: np.log(v) if v > 0 else np.nan for k, v in SER["gdppc_log"].items()}
SER["mys_total"] = load_csv(RAW + "mys_total.csv",
                            "mf_youth_and_adults__15_64_years__average_years_of_education")
SER["mys_female"] = load_csv(RAW + "mys_female.csv", "mys__sex_female")

years = list(range(1960, 2025, 5))
P = pd.DataFrame([dict(iso3=iso, year=yr) for iso in ISOS for yr in years])
for m, d in SER.items():
    P[m] = [d.get((r.iso3, r.year), np.nan) for r in P.itertuples()]
IND = [m for m in ["mys_total", "mys_female", "sec", "lsc", "prm_cmp", "ter", "gpi_sec", "gpi_ter"]
       if P[m].notna().sum() > 0]
print(f"indicators available ({len(IND)}): {IND}")
print(f"panel rows: {len(P)}, countries: {P.iso3.nunique()}, years {min(years)}-{max(years)}")
P["decade"] = (P.year // 10) * 10
P = P.sort_values(["iso3", "year"]).reset_index(drop=True)
g = P.groupby("iso3")
for v in ["fertility", "gdppc_log", "urban"] + IND:
    P[v + "_m10"] = g[v].shift(2)
    P[v + "_p10"] = g[v].shift(-2)
    P[v + "_p20"] = g[v].shift(-4)
P["dF_prev"] = P.fertility - P.fertility_m10
P["dF_next"] = P.fertility_p10 - P.fertility
P["dF_next2"] = P.fertility_p20 - P.fertility_p10


def design(df, mode):
    n = len(df)
    blocks = [np.ones((n, 1)),
              pd.get_dummies(df.iso3, dtype=float).to_numpy(),
              pd.get_dummies(df.decade, dtype=float).to_numpy()]
    if mode == "country_trend_decade":
        yrs = df.year.to_numpy(float)
        for iso in sorted(df.iso3.unique()):
            m = (df.iso3 == iso).to_numpy()
            yc = yrs - yrs[m].mean()
            blocks.append((m.astype(float) * yc)[:, None])
    return np.column_stack(blocks)


def run(df, y, xs, mode):
    """FWL: residualise y, xs and controls on the FE design, then OLS residual y on residual xs."""
    cols = [y] + xs + ["gdppc_log", "urban"]
    d = df.dropna(subset=cols).copy()
    if len(d) < 30 or d.iso3.nunique() < 8:
        return None
    C = design(d, mode)
    R = {}
    for c in cols:
        b = np.linalg.lstsq(C, d[c].to_numpy(float), rcond=None)[0]
        R[c] = d[c].to_numpy(float) - C @ b
    X = np.column_stack([R[x] for x in xs])
    # standardise within the estimation sample (per-SD coefficients)
    Xs = (X - X.mean(0)) / X.std(0, ddof=1)
    Xs = sm.add_constant(Xs)
    m = sm.OLS(R[y], Xs).fit(cov_type="cluster", cov_kwds={"groups": d.iso3})
    out = {}
    for k, x in enumerate(xs):
        j = k + 1
        ci = m.conf_int()[j]
        out[x] = dict(coef=round(float(m.params[j]), 4), se=round(float(m.bse[j]), 4),
                      ci_lo=round(float(ci[0]), 4), ci_hi=round(float(ci[1]), 4))
    out["n"] = int(m.nobs)
    out["countries"] = int(d.iso3.nunique())
    return out


rows = []
for S in IND:
    Q = P.copy()
    Q["dS_prev"] = Q[S] - Q[S + "_m10"]
    Q["dS_next"] = Q[S + "_p10"] - Q[S]
    Q["dS_next2"] = Q[S + "_p20"] - Q[S + "_p10"]
    A = Q.dropna(subset=["fertility", S, S + "_m10", S + "_p10", "dS_next", "gdppc_log", "urban"]).copy()
    B = Q.dropna(subset=["dF_prev", "dF_next", "dF_next2", "dS_prev", "dS_next", "dS_next2"]).copy()
    specs = {
        "A levels": [("A0 current S(t)", [S]), ("A1 future S(t+10)", [S + "_p10"]),
                     ("A2 both S(t)+S(t+10)", [S, S + "_p10"]), ("A3 lagged S(t-10)", [S + "_m10"]),
                     ("A4 future change dS(t+10,t+20)", ["dS_next"])],
        "B changes (dF)": [("B0 past dS(t-10,t)", ["dS_prev"]), ("B1 concurrent dS(t,t+10)", ["dS_next"]),
                           ("B2 future dS(t+10,t+20)", ["dS_next2"]),
                           ("B3 all three", ["dS_prev", "dS_next", "dS_next2"])],
        "C reverse (dS)": [("C0 past dF(t-10,t)", ["dF_prev"]), ("C1 concurrent dF(t,t+10)", ["dF_next"]),
                           ("C2 future dF(t+10,t+20)", ["dF_next2"]),
                           ("C3 all three", ["dF_prev", "dF_next", "dF_next2"])],
    }
    yvar = {"A levels": "fertility", "B changes (dF)": "dF_next", "C reverse (dS)": "dS_next"}
    for ladder, spec_list in specs.items():
        for lab, xs in spec_list:
            for mode in ("country_decade", "country_trend_decade"):
                r = run(A if ladder == "A levels" else B, yvar[ladder], xs, mode)
                if r is None:
                    rows.append(dict(indicator=S, ladder=ladder, step=lab, term="FAILED", coef=np.nan,
                                     se=np.nan, ci_lo=np.nan, ci_hi=np.nan, n=0, countries=0, variant=mode))
                    continue
                for x in xs:
                    rows.append(dict(indicator=S, ladder=ladder, step=lab, term=x, variant=mode, **r[x],
                                     n=r["n"], countries=r["countries"]))
R = pd.DataFrame(rows)
R.to_csv("e11_ladder.csv", index=False)
print(f"\nrows written: {len(R)} (failures: {int((R.term == 'FAILED').sum())})")

# ---------- compact table + pre-registered decision ----------
def pick(S, ladder, step, term, variant):
    q = R[(R.indicator == S) & (R.ladder == ladder) & (R.step == step) & (R.term == term) & (R.variant == variant)]
    return None if q.empty else q.iloc[0]


print("\n=== E11 compact table (baseline = country+decade FE for levels, country FE for changes; per-SD; clustered SE)")
decisions = {}
for label, ladder, step_lead, term_lead_fn, step_lag, term_lag_fn in [
    ("A2 lead S(t+10)/lag S(t)", "A levels", "A2 both S(t)+S(t+10)", lambda S: S + "_p10",
     "A2 both S(t)+S(t+10)", lambda S: S),
    ("B3 lead dS(t+10,t+20)/lag dS(t-10,t)", "B changes (dF)", "B3 all three", lambda S: "dS_next2",
     "B3 all three", lambda S: "dS_prev")]:
    ratios = {}
    for S in IND:
        lead = pick(S, ladder, step_lead, term_lead_fn(S), "country_decade")
        lag = pick(S, ladder, step_lag, term_lag_fn(S), "country_decade")
        ratios[S] = np.nan if (lead is None or lag is None or lag.coef == 0) else lead.coef / lag.coef
    vals = [v for v in ratios.values() if v == v]
    n80 = sum(1 for v in vals if abs(v) >= 0.8)
    n2 = sum(1 for v in vals if abs(v) <= 0.5)
    if n80 > len(IND) / 2:
        verdict = "does not discriminate between a common development gradient, anticipation/quantity-quality, and a schooling effect"
    elif n2 > len(IND) / 2:
        verdict = "temporal asymmetry present; the causal reading is still untested"
    else:
        verdict = "indeterminate"
    decisions[label] = dict(ratios={k: (None if v != v else round(float(v), 3)) for k, v in ratios.items()},
                            n_lead80=n80, n_lag2=n2, verdict=verdict)
    print(f"  {label}:\n    " + ", ".join(f"{S}={v:+.2f}" if v == v else f"{S}=NA" for S, v in ratios.items()))
    print(f"    |lead|>=0.8|lag| in {n80}/{len(vals)}; |lag|>=2|lead| in {n2}/{len(vals)}")
    print(f"    pre-registered verdict: {verdict}")

print("\n=== future-fertility placebo (C ladder, baseline, future dF term C2)")
for S in IND:
    for term in ("dF_prev", "dF_next", "dF_next2"):
        q = pick(S, "C reverse (dS)", {"dF_prev": "C0 past dF(t-10,t)", "dF_next": "C1 concurrent dF(t,t+10)",
                                       "dF_next2": "C2 future dF(t+10,t+20)"}[term], term, "country_decade")
        if q is not None:
            print(f"  {S:11s} {term:10s} {q.coef:+.3f} ({q.se:.3f}) n={q.n} countries={q.countries}")
    print()

json.dump(dict(indicators=IND, decision=decisions, rows=R.to_dict("records"),
               note="F = project fertility (births per woman, TFR-type); not effective fertility. "
                    "Baseline FE: country+decade (levels), country (changes); trend variant adds country-specific linear trends. "
                    "Controls: log income, urbanisation; country-clustered SEs; 5-year grid, 1960-2024."),
          open("e11_ladder.json", "w"), indent=1)
print("\nINTERPRETATION LIMIT (pre-registered): a future-schooling term as strong as the current term is consistent with "
      "(i) a common development gradient, (ii) anticipation/quantity-quality, and (iii) a schooling effect with a long lag. "
      "The design cannot distinguish these and cannot reject a schooling effect.")
