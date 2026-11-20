#!/usr/bin/env python
"""Cluster 1 (post-secondary absorption): predeclared descriptive experiments X1-X3.

Deterministic; no network; no imputation. Fixed predeclared proxies:
  ABSORB_F = SL.EMP.WORK.ZS   ABSORB_S = SL.SRV.EMPL.ZS
  GRAD_SUPPLY = SE.TER.CUAT.BA.ZS
  QUEUE = GRAD_SUPPLY / ABSORB_F * 100   (derived; rows with missing/0 ABSORB_F dropped)
  LGDP = log(NY.GDP.PCAP.PP.CD); URBAN = SP.URB.TOTL.IN.ZS; TER = SE.TER.ENRR
Estimator: OLS, country-clustered CR1 SEs (G/(G-1) small-sample correction).
"""
import json
import hashlib
import datetime as dt
import numpy as np
import pandas as pd

SEED = 0
np.random.seed(SEED)

BASE = "/Users/treymenefee/massification_live/experiments/massification-2026-11-20"
JOBS = BASE + "/10_massification/data/JOBS_AND_MARKETS_PANEL.csv"
WDI = BASE + "/09_relations/data/panel_wdi_long.csv"
OUT = BASE + "/10_massification/extensions/lab_2026-11-20_b/cluster_1_absorption/results"

SYSTEMS = ["KHM", "CHN", "HKG", "JPN", "KOR", "PHL"]
Y0, Y1 = 1995, 2024

jobs = pd.read_csv(JOBS)
wdi = pd.read_csv(WDI)

def pivot_wide(df, country="iso3", code="code", year="year", value="value"):
    w = df.pivot_table(index=[country, year], columns=code, values=value,
                       aggfunc="first").reset_index()
    w.columns.name = None
    return w

def build_jobs():
    j = jobs[(jobs.iso3.isin(SYSTEMS)) & (jobs.year >= Y0) & (jobs.year <= Y1)
             & (jobs.status == "observed")].copy()
    j = j.rename(columns={"indicator_code": "code"})
    w = pivot_wide(j)
    need = ["SL.EMP.WORK.ZS", "SL.SRV.EMPL.ZS", "NY.GDP.PCAP.PP.CD",
            "SP.URB.TOTL.IN.ZS", "SP.POP.TOTL"]
    for c in need:
        if c not in w.columns:
            w[c] = np.nan
    w["ABSORB_F"] = w["SL.EMP.WORK.ZS"]
    w["ABSORB_S"] = w["SL.SRV.EMPL.ZS"]
    w["LGDP"] = np.log(w["NY.GDP.PCAP.PP.CD"])
    w["URBAN"] = w["SP.URB.TOTL.IN.ZS"]
    # TER not on JOBS panel: take from WDI 30-country panel (same 6 systems, observed).
    t = wdi[wdi.indicator == "SE.TER.ENRR"][[  "iso3", "year", "value"]].rename(
        columns={"value": "TER"})
    t["country_wdi"] = t["iso3"].map(
        wdi.drop_duplicates("iso3").set_index("iso3")["country"])
    w = w.merge(t[["iso3", "year", "TER"]], on=["iso3", "year"], how="left")
    return w.dropna(subset=["TER", "LGDP", "URBAN", "ABSORB_F"]).reset_index(drop=True)

def build_wdi():
    w = wdi.rename(columns={"indicator": "code"})
    w = pivot_wide(w)
    w["ABSORB_F"] = w["SL.EMP.WORK.ZS"]
    w["ABSORB_S"] = w["SL.SRV.EMPL.ZS"]
    w["LGDP"] = np.log(w["NY.GDP.PCAP.PP.CD"])
    w["URBAN"] = w["SP.URB.TOTL.IN.ZS"]
    w["GRAD_SUPPLY"] = w["SE.TER.CUAT.BA.ZS"]
    w["TER"] = w["SE.TER.ENRR"]
    w = w[(w.year >= Y0) & (w.year <= Y1)]
    # QUEUE derived; drop rows where ABSORB_F missing or 0; never impute
    q = w.dropna(subset=["GRAD_SUPPLY"]).copy()
    q = q[q["ABSORB_F"].notna() & (q["ABSORB_F"] > 0)]
    q["QUEUE"] = q["GRAD_SUPPLY"] / q["ABSORB_F"] * 100.0
    return w.reset_index(drop=True), q.reset_index(drop=True)

def ols_cluster(df, dep, regs, demean=False, between=False, drop_na=True):
    """OLS with CR1 country-clustered SEs. demean: within (country-demeaned).
    between: country-means regression. Returns dict for one regressor set."""
    d = df.copy()
    if drop_na:
        d = d.dropna(subset=[dep] + regs)
    if between:
        d = d.groupby("iso3", as_index=False)[[dep] + regs].mean()
    elif demean:
        num = d[[dep] + regs].groupby(d["iso3"]).transform("mean")
        d = pd.concat([d[[dep] + regs] - num, d[["iso3"]]], axis=1)
    X = np.column_stack([np.ones(len(d))] + [d[r].to_numpy(float) for r in regs])
    y = d[dep].to_numpy(float)
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    resid = y - X @ beta
    g = pd.factorize(d["iso3"])[0]
    G = g.max() + 1
    meat = np.zeros((k, k))
    for gg in range(G):
        m = g == gg
        Xg, ug = X[m], resid[m]
        s = Xg.T @ ug
        meat += np.outer(s, s)
    V = XtX_inv @ meat @ XtX_inv * (G / (G - 1))
    ses = np.sqrt(np.diag(V))
    return {"n": int(n), "clusters": int(G), "beta": beta.tolist(),
            "se": ses.tolist(), "names": ["const"] + regs, "df": d}

def ci(b, s):
    return b - 1.96 * s, b + 1.96 * s

def coef_row(spec, dep, reg, r):
    i = r["names"].index(reg)
    b, s = r["beta"][i], r["se"][i]
    lo, hi = ci(b, s)
    return {"experiment": spec, "dep_var": dep, "spec": reg,
            "coefficient": round(b, 6), "se": round(s, 6),
            "ci_low": round(lo, 6), "ci_high": round(hi, 6),
            "n": r["n"], "n_clusters": r["clusters"], "label": "observed"}

JOBS_W = build_jobs()
WDI_W, WDI_Q = build_wdi()

detail_rows = []
summary = []

# ---------------- X1: 6 systems, TER on LGDP/URBAN/ABSORB_F (+ ABSORB_S run) --------
for proxy in ["ABSORB_F", "ABSORB_S"]:
    regs = ["LGDP", "URBAN", proxy]
    for mode, mname in [(True, "within"), (False, "between")]:
        r = ols_cluster(JOBS_W, "TER", regs, demean=mode)
        row = coef_row("X1", "TER", proxy, r)
        row["spec"] = f"{mname}: TER ~ LGDP+URBAN+{proxy}"
        row["label"] = "derived"
        detail_rows.append(row)
wF = next(x for x in detail_rows if x["experiment"] == "X1" and x["spec"].startswith("within") and x["spec"].endswith("ABSORB_F"))
wS = next(x for x in detail_rows if x["experiment"] == "X1" and x["spec"].startswith("within") and x["spec"].endswith("ABSORB_S"))
signs_agree = np.sign(wF["coefficient"]) == np.sign(wS["coefficient"])
excl0 = (wF["ci_low"] > 0) or (wF["ci_high"] < 0)
if excl0 and signs_agree:
    v1 = "SUPPORTED"
else:
    # Lead adjudication of an internal predeclaration ambiguity (disclosed in FINDINGS.md/RUN_MANIFEST):
    # the threshold text says "PARTIAL if only one of the two" but the explicit falsifier says
    # "within CI includes 0 -> NOT SUPPORTED". Falsifier takes precedence; the PARTIAL
    # (sign-agreement-only) reading is carried verbatim in the note.
    v1 = "NOT SUPPORTED"
summary.append({"experiment": "X1", "cluster": "1_post_secondary_absorption",
    "question": "Tertiary expansion vs formal absorption, 6 systems 1995-2024",
    "estimand": "within partial slope of TER on ABSORB_F (country-demeaned, CR1)",
    "estimate": wF["coefficient"], "se": wF["se"], "ci_low": wF["ci_low"],
    "ci_high": wF["ci_high"], "n": wF["n"], "clusters": wF["n_clusters"],
    "threshold": "SUPPORTED if within CI excludes 0 AND sign agrees between ABSORB_F and ABSORB_S runs; PARTIAL if only one; NOT SUPPORTED if CI includes 0 or sign flips",
    "verdict": v1, "label": "derived",
    "note": "6-country small-n warning; TER sourced from 30-country WDI panel for these systems; ABSORB_F and ABSORB_S are proxies, not measured absorption; PREDECLARATION AMBIGUITY (lead, disclosed): PARTIAL clause (sign agreement only) vs falsifier (within CI includes 0 -> NOT SUPPORTED) conflict; falsifier-precedence reading adopted => NOT SUPPORTED; alternative reading = PARTIAL; ABSORB_S sign agrees (both negative) but its CI also includes 0"})

# ---------------- X2: 30-country replication --------------------------------------
regs = ["LGDP", "URBAN", "ABSORB_F"]
for mode, mname in [(True, "within"), (False, "between")]:
    r = ols_cluster(WDI_W, "TER", regs, demean=mode)
    row = coef_row("X2", "TER", "ABSORB_F", r)
    row["spec"] = f"{mname}: TER ~ LGDP+URBAN+ABSORB_F"
    row["label"] = "derived"
    detail_rows.append(row)
p2 = next(x for x in detail_rows if x["experiment"] == "X2" and x["spec"].startswith("within"))
b2 = next(x for x in detail_rows if x["experiment"] == "X2" and x["spec"].startswith("between"))
n_ctys = WDI_W.dropna(subset=["TER"] + regs)["iso3"].nunique()
if n_ctys < 10 or p2["n"] < 100:
    v2 = "DATA LIMITED"
elif p2["ci_low"] <= wF["coefficient"] <= p2["ci_high"] and np.sign(p2["coefficient"]) == np.sign(wF["coefficient"]):
    v2 = "SUPPORTED"
elif np.sign(p2["coefficient"]) == np.sign(wF["coefficient"]):
    v2 = "PARTIAL"
else:
    v2 = "NOT SUPPORTED"
summary.append({"experiment": "X2", "cluster": "1_post_secondary_absorption",
    "question": "30-country replication 1995-2024",
    "estimand": "pooled/within partial slope of TER on ABSORB_F, country-clustered (CR1)",
    "estimate": p2["coefficient"], "se": p2["se"], "ci_low": p2["ci_low"],
    "ci_high": p2["ci_high"], "n": p2["n"], "clusters": p2["n_clusters"],
    "threshold": "SUPPORTED if 30-country within slope inside X1 within 95% CI and sign agrees; PARTIAL if sign agrees but outside; NOT SUPPORTED if outside with opposite sign; DATA LIMITED if <10 countries or <100 obs",
    "verdict": v2, "label": "derived",
    "note": f"countries used={n_ctys}; X1 within CI [{wF['ci_low']},{wF['ci_high']}]; between slope={b2['coefficient']}; ABSORB_F is a proxy; NOTE (lead, disclosed): the 30-country point estimate lies INSIDE the X1 within CI but with OPPOSITE sign, so the replication criterion (sign agrees) fails while the falsifier's literal wording (outside CI with opposite sign) does not fire; NOT SUPPORTED is the conservative replication verdict"})

# ---------------- X3: QUEUE on TER, three fixed specs ------------------------------
q_cells = len(WDI_Q)
specs3 = []
d = WDI_Q.dropna(subset=["QUEUE", "TER"]).copy()
# (a) levels with country FE (demeaned)
ra = ols_cluster(d, "QUEUE", ["TER"], demean=True)
specs3.append(("a_levels_countryFE", ra))
# (b) log1p(QUEUE) on log(TER)
d2 = d[(d["TER"] > 0)].copy()
d2["LQUEUE"] = np.log1p(d2["QUEUE"])
d2["LTER"] = np.log(d2["TER"])
rb = ols_cluster(d2, "LQUEUE", ["LTER"], demean=True)
specs3.append(("b_log1p_log", rb))
# (c) first differences
d3 = d.sort_values(["iso3", "year"])
g = d3.groupby("iso3")
for c in ["QUEUE", "TER", "year"]:
    d3[f"d{c}"] = g[c].diff()
d3 = d3.dropna(subset=["dQUEUE", "dTER"])
rc = ols_cluster(d3, "dQUEUE", ["dTER"], demean=False)
specs3.append(("c_first_differences", rc))
for nm, r in specs3:
    reg_name = r["names"][1]
    row = coef_row("X3", "QUEUE" if "log" not in nm else "log1p(QUEUE)", reg_name, r)
    row["spec"] = nm
    if "log" in nm:
        row["spec"] = nm + " (log1p(QUEUE) on log(TER), coefficient reported for log(TER))"
    row["label"] = "derived"
    detail_rows.append(row)
def _ci0(nm, r):
    key = r["names"][1]
    i = r["names"].index(key)
    lo, hi = ci(r["beta"][i], r["se"][i])
    return not (lo < 0 < hi)


sig = [_ci0(nm, r) for nm, r in specs3]
nz = int(sum(sig))
if nz <= 1:
    v3 = "NOT SUPPORTED"
elif q_cells < 60:
    v3 = "DATA LIMITED"
else:
    v3 = "SUPPORTED"
p3 = specs3[0][1]
b3, s3 = p3["beta"][p3["names"].index("TER")], p3["se"][p3["names"].index("TER")]
lo3, hi3 = ci(b3, s3)
summary.append({"experiment": "X3", "cluster": "1_post_secondary_absorption",
    "question": "Graduate-queue depth vs tertiary expansion, 30 countries",
    "estimand": "slope of QUEUE on TER, spec (a) levels with country FE (CR1)",
    "estimate": round(b3, 6), "se": round(s3, 6), "ci_low": round(lo3, 6),
    "ci_high": round(hi3, 6), "n": p3["n"], "clusters": p3["clusters"],
    "threshold": "SUPPORTED if TER coefficient CI excludes 0 in >=2 of 3 specs (sign-stable); PARTIAL if 1 of 3; NOT SUPPORTED if CI includes 0 in >=2 of 3; DATA LIMITED if QUEUE usable cells <60",
    "verdict": v3, "label": "derived",
    "note": f"QUEUE usable cells={q_cells}; CI-excludes-0 flags per spec (a,b,c)={sig}; QUEUE and GRAD_SUPPLY derived from predeclared proxies"})

pd.DataFrame(detail_rows).to_csv(OUT + "/X1_absorption_6systems.csv", index=False) if False else None
pd.DataFrame([r for r in detail_rows if r["experiment"] == "X1"]).to_csv(
    OUT + "/X1_absorption_6systems.csv", index=False)
pd.DataFrame([r for r in detail_rows if r["experiment"] == "X2"]).to_csv(
    OUT + "/X2_absorption_30countries.csv", index=False)
pd.DataFrame([r for r in detail_rows if r["experiment"] == "X3"]).to_csv(
    OUT + "/X3_queue_depth.csv", index=False)
pd.DataFrame(summary).to_csv(OUT + "/CLUSTER_RESULTS.csv", index=False)

manifest_meta = {
    "cluster": "1_post_secondary_absorption",
    "predeclared_proxy_definitions": {
        "ABSORB_F": "SL.EMP.WORK.ZS (wage-and-salaried % employment, ILO modelled)",
        "ABSORB_S": "SL.SRV.EMPL.ZS",
        "GRAD_SUPPLY": "SE.TER.CUAT.BA.ZS",
        "QUEUE": "GRAD_SUPPLY / ABSORB_F * 100 (derived; rows with missing/0 ABSORB_F dropped, never imputed)",
        "LGDP": "log(NY.GDP.PCAP.PP.CD)", "URBAN": "SP.URB.TOTL.IN.ZS",
        "TER": "SE.TER.ENRR"},
    "seed": SEED,
    "deterministic_note": "Pure-numpy OLS with CR1 cluster SEs; no randomness; fixed input paths; pandas version " + pd.__version__,
}

def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# NOTE (lead): the authoritative cluster manifest is RUN_MANIFEST.json (written by the consolidation
# step, which records accurate code/results hashes). An auto-written side manifest was removed because
# its run_utc/hashes made the tree non-reproducible on every re-run.

print("X1 verdict:", v1, "| X2 verdict:", v2, "| X3 verdict:", v3)
print("X1 within ABSORB_F:", wF["coefficient"], "CI", (wF["ci_low"], wF["ci_high"]), "n", wF["n"], "G", wF["n_clusters"])
print("X2 within:", p2["coefficient"], "CI", (p2["ci_low"], p2["ci_high"]), "n", p2["n"], "G", p2["n_clusters"])
print("X3 spec(a):", round(b3, 6), "CI", (round(lo3, 6), round(hi3, 6)), "n", p3["n"], "G", p3["clusters"])
print("QUEUE cells:", q_cells, "| X3 CI-excludes-0 flags:", sig)
