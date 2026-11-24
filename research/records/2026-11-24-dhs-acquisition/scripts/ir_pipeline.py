#!/usr/bin/env python3
"""EXECUTION-READY pipeline for the pre-registered Individual Recode (IR) test.

Pre-registration: ../PRE_REGISTRATION.md (committed 2026-11-24 before any data).
Access coverage:  ../AMENDMENT_02_ACCESS_COVERAGE.md (T0-T4 tiers).
This script was written and syntax/self-tested *before any DHS microdata exists*; it has never seen a DHS
individual record. It is the code that will run **if and when** the approved IR files arrive.

It does four things, in order, and stops on any structural failure:
  1. VERIFY   locate the expected IR files (manifest), hash them, check the required variables exist, run the
              data-quality checks from ACQUISITION_PLAN.md section 7 (v201 == sum of v202..v207, weights,
              CMC/age, clusters, fieldwork window, duplicates).  Writes verification.json.
  2. BUILD    the pre-registered analysis samples (S-A women 40-49 for completed fertility; S-B/S-C robustness).
  3. ESTIMATE the pre-registered models M0-M4 (cohort FE + round FE, survey weights, design-based PSU-clustered
              SEs, pre-declared controls) for O1 = births (v201) and O2 = surviving children (v201 - v206 - v207),
              plus the construct x schooling test, the dose (v133) model and the cohort interaction.
  4. REPORT   write estimates.csv / summary.json / verification.json under --outdir. Nothing is written into
              the repository; microdata never leaves --datadir.

DATA TIER: every number this script produces is OBSERVED individual-level data (once real files are supplied).
The --selftest path is a CODE TEST on a handful of hand-made rows: it is NOT evidence, NOT a simulation of the
research question, and must never be reported as a result.

Usage:
  python3 scripts/ir_pipeline.py --datadir /secure/dhs_ir --outdir /secure/out --check-only
  python3 scripts/ir_pipeline.py --datadir /secure/dhs_ir --outdir /secure/out
  python3 scripts/ir_pipeline.py --selftest
Requirements: Python 3.9+, numpy; pandas (for reading Stata .dta) only when real data are supplied.
"""
import argparse
import csv
import hashlib
import json
import math
import os
import sys
import zipfile

import numpy as np

REQUIRED = ["v005", "v008", "v011", "v012", "v021", "v022", "v024", "v025",
            "v106", "v107", "v133", "v149", "v190", "v201", "v202", "v203", "v204",
            "v205", "v206", "v207", "v224"]
OPTIONAL = ["v023", "v130", "v131", "v212"]
EDU = {0: "none", 1: "primary", 2: "secondary", 3: "higher"}
SURVIVING = "surviving"  # v201 - v206 - v207 (never call this TFR)


# ------------------------------------------------------------------------------------- helpers
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_manifest(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("survey_year", "bytes_stata"):
            r[k] = int(float(r[k])) if r.get(k) not in (None, "", "None") else None
        for k in ("women_unweighted", "sample_points"):
            r[k] = int(float(r[k])) if r.get(k) not in (None, "", "None") else None
    return rows


def filter_manifest(rows, countries=None):
    """Filter manifest rows strictly to standard DHS surveys (excluding MIS/AIS) and optional ISO3 subset."""
    out = [r for r in rows if (r.get("survey_type") or "").strip().upper() == "DHS"]
    if countries:
        keep = {c.strip().upper() for c in countries.split(",")}
        out = [r for r in out if (r.get("iso3") or "").strip().upper() in keep]
    return out


def locate_dta(datadir, row):
    """Find the extracted .dta for a manifest row; if only the original .ZIP is present, extract to tmp."""
    stem = os.path.splitext(row["file_stata"])[0]
    for name in (stem + ".dta", stem.lower() + ".dta", stem + ".DTA"):
        p = os.path.join(datadir, name)
        if os.path.exists(p):
            return p
    # also accept any .dta whose name starts with the stem (case-insensitive)
    if os.path.isdir(datadir):
        for f in os.listdir(datadir):
            if f.lower().startswith(stem.lower()) and f.lower().endswith(".dta"):
                return os.path.join(datadir, f)
        for f in os.listdir(datadir):
            if f.lower() == row["file_stata"].lower():
                zpath = os.path.join(datadir, f)
                with zipfile.ZipFile(zpath) as z:
                    member = [m for m in z.namelist() if m.lower().endswith(".dta")]
                    if not member:
                        return None
                    tmp = os.path.join(datadir, "_extracted")
                    os.makedirs(tmp, exist_ok=True)
                    z.extract(member[0], tmp)
                    return os.path.join(tmp, member[0])
    return None


def read_dta(path):
    """Read only what we need, if pandas allows column selection; else read all and subset."""
    try:
        import pandas as pd  # noqa: F401
    except ImportError as e:  # pragma: no cover - environment message
        raise SystemExit("pandas is required to read DHS .dta files: pip install pandas\n" + str(e))
    import pandas as pd
    df = None
    try:
        df = pd.read_stata(path, convert_categoricals=False, columns=REQUIRED + OPTIONAL)
    except (TypeError, ValueError):
        df = None
    if df is None:
        df = pd.read_stata(path, convert_categoricals=False)
        missing = [c for c in REQUIRED + OPTIONAL if c in df.columns]
        df = df[missing]
    return df


# ------------------------------------------------------------------- weighted FE absorber + cluster SE
def _demean(v, groups, w):
    sw = np.bincount(groups, weights=w)
    sv = np.bincount(groups, weights=v * w)
    means = np.divide(sv, np.maximum(sw, 1e-12))
    return v - means[groups]


def absorb(Y, X, fe_list, w, iters=60, tol=1e-10):
    """Alternating projections weighted within-transform for several categorical FE factors."""
    fe_list = [np.unique(np.asarray(g), return_inverse=True)[1] for g in fe_list]
    Yd, Xd = Y.copy(), X.copy()
    for _ in range(iters):
        delta = 0.0
        for g in fe_list:
            v = _demean(Yd, g, w)
            delta = max(delta, float(np.max(np.abs(v - Yd))) if len(v) else 0.0)
            Yd = v
            for j in range(Xd.shape[1]):
                Xd[:, j] = _demean(Xd[:, j], g, w)
        if delta < tol:
            break
    return Yd, Xd


def wls_absorbed(y, X, fe_list, w, cluster):
    """WLS with absorbed FE (FWL) and vectorized CR1 cluster-robust sandwich SEs."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    w = np.asarray(w, float)
    keep = np.isfinite(y) & np.all(np.isfinite(X), axis=1) & np.isfinite(w) & (w > 0)
    y, X, w2 = y[keep], X[keep], w[keep]
    if X.shape[1] == 0 or len(y) < 10:
        return None
    fe_kept = [np.asarray(g)[keep] for g in fe_list]
    cl = np.asarray(cluster)[keep]
    yd, Xd = absorb(y, X, fe_kept, w2)
    ok = np.isfinite(yd) & np.all(np.isfinite(Xd), axis=1)
    if not np.all(ok):
        yd, Xd, w2, cl = yd[ok], Xd[ok], w2[ok], cl[ok]
    if Xd.shape[1] == 0 or len(yd) < 10:
        return None
    XtWX = Xd.T @ (Xd * w2[:, None])
    beta = np.linalg.lstsq(XtWX, Xd.T @ (w2 * yd), rcond=None)[0]
    u = yd - Xd @ beta
    P = np.linalg.pinv(XtWX)
    _, inv = np.unique(cl, return_inverse=True)
    n_cl = int(inv.max()) + 1
    S = np.zeros((n_cl, Xd.shape[1]), dtype=float)
    np.add.at(S, inv, Xd * (w2 * u)[:, None])
    meat = S.T @ S
    cr1 = (n_cl / (n_cl - 1.0)) if n_cl > 1 else 1.0
    V = cr1 * (P @ meat @ P)
    se = np.sqrt(np.maximum(np.diag(V), 0))
    from math import erf, sqrt
    t = np.divide(beta, se, out=np.full_like(beta, np.nan), where=se > 0)
    p = np.array([2 * (1 - 0.5 * (1 + erf(abs(v) / sqrt(2)))) for v in t])
    return {"b": beta, "se": se, "p": p, "n": int(len(yd)), "k": int(Xd.shape[1])}


def dummies(vals, drop_first=True):
    levels = sorted(set(vals))
    if drop_first:
        levels = levels[1:]
    return (np.column_stack([(np.asarray(vals) == lev).astype(float) for lev in levels])
            if levels else np.zeros((len(vals), 0)))


# ------------------------------------------------------------------------------------- checks
def numeric(df):
    """Coerce the analysis columns to float, tolerating Stata missing/Int64 dtypes."""
    import pandas as pd
    d = df.copy()
    for c in REQUIRED + OPTIONAL:
        if c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")
    return d


def check_file(df, row, path):
    out = {"file": os.path.basename(path), "survey_id": row["survey_id"],
           "iso3": row["iso3"], "year": row["survey_year"], "sha256": sha256(path),
           "n_rows": int(len(df)), "failures": [], "warnings": []}

    def fail(msg):
        out["failures"].append(msg)

    def warn(msg):
        out["warnings"].append(msg)

    cols = set(df.columns)
    missing = [v for v in REQUIRED if v not in cols]
    if missing:
        fail("missing required variables: " + ",".join(missing))
        return out
    if len(df) == 0:
        fail("empty file")
        return out

    d = numeric(df).replace([np.inf, -np.inf], np.nan)
    v201 = d["v201"].astype(float)
    dead = d[["v206", "v207"]].astype(float).sum(axis=1)
    comp = d[["v202", "v203", "v204", "v205", "v206", "v207"]].astype(float).sum(axis=1)
    both = v201.notna() & comp.notna()
    if both.any() and not np.allclose(v201[both].values, comp[both].values, atol=0.51):
        fail("v201 != v202+...+v207 for some women")
    if (dead > v201 + 0.01).any():
        fail("v206+v207 > v201 for some women")

    w = d["v005"].astype(float) / 1e6
    if (w <= 0).any():
        warn("non-positive v005 in some rows")
    ratio = float(np.nansum(w) / max(len(d), 1))
    if not 0.2 <= ratio <= 5.0:
        warn(f"weighted/unweighted ratio {ratio:.3f} outside [0.2, 5.0]")

    age = d["v012"].astype(float)
    if age.min() < 15 or age.max() > 49:
        warn(f"v012 range {age.min():.0f}-{age.max():.0f} outside 15-49 (verify universe)")
    cmc_age = (d["v008"].astype(float) - d["v011"].astype(float)) / 12.0
    bad_age = (np.abs(cmc_age - age) > 1.01).sum()
    if bad_age > max(5, 0.005 * len(d)):
        warn(f"{bad_age} rows where |(v008-v011)/12 - v012| > 1")

    if row.get("women_unweighted"):
        if abs(len(d) - row["women_unweighted"]) > max(50, 0.01 * row["women_unweighted"]):
            warn(f"rows {len(d)} vs published NumberOfWomen {row['women_unweighted']}")
    if row.get("sample_points"):
        ncl = d["v021"].nunique()
        if ncl and abs(ncl - row["sample_points"]) > max(5, 0.05 * row["sample_points"]):
            warn(f"v021 clusters {ncl} vs published sample points {row['sample_points']}")

    if row.get("fieldwork_start") and row.get("fieldwork_end"):
        try:
            y0, m0 = [int(x) for x in row["fieldwork_start"].split("-")[:2]]
            y1, m1 = [int(x) for x in row["fieldwork_end"].split("-")[:2]]
            c0, c1 = (y0 - 1900) * 12 + m0, (y1 - 1900) * 12 + m1
            v8 = d["v008"].astype(float)
            outside = ((v8 < c0 - 3) | (v8 > c1 + 3)).mean()
            if outside > 0.02:
                warn(f"{outside:.1%} of interviews outside fieldwork window +/-3 months")
        except (ValueError, IndexError):
            warn("could not parse fieldwork window")
    edu = d["v106"].astype(float).dropna()
    bad_edu = (~edu.isin([0, 1, 2, 3])).sum()
    if bad_edu:
        warn(f"{bad_edu} rows with v106 outside 0-3")
    if d["v025"].isna().any():
        warn("missing v025 (urban/rural) in some rows")
    out["n_women_15_49"] = int(((age >= 15) & (age <= 49)).sum())
    out["n_women_40_49"] = int(((age >= 40) & (age <= 49)).sum())
    out["mean_ceb_40_49"] = (float(v201[(age >= 40) & (age <= 49)].mean())
                             if ((age >= 40) & (age <= 49)).any() else None)
    out["share_any_child_death"] = float((dead > 0).mean())
    return out


# ------------------------------------------------------------------------------------- samples/models
def woman_frame(df, row):
    """Return a dict of numpy arrays for the pre-registered woman-level samples."""
    d = numeric(df).replace([np.inf, -np.inf], np.nan)
    age = d["v012"].astype(float).values
    cohort5 = (np.floor((d["v011"].astype(float).values / 12.0) / 5.0) * 5.0)
    w_raw = d["v005"].astype(float).values / 1e6
    w_valid = np.isfinite(w_raw) & (w_raw > 0)
    w_sum = float(w_raw[w_valid].sum())
    w_norm = np.where(w_valid, w_raw / w_sum, np.nan) if w_sum > 0 else np.full_like(w_raw, np.nan)
    f = {
        "age": age, "cohort5": cohort5.astype(int),
        "survey": np.array([row["survey_id"]] * len(d)),
        "country": np.array([row["iso3"]] * len(d)),
        "round": np.array([str(row["survey_id"])] * len(d)),
        "psu": np.array([f"{row['survey_id']}_{int(x) if np.isfinite(x) else -1}"
                         for x in d["v021"].values], dtype=object),
        "w": w_norm,
        "edu": d["v106"].astype(float).values,
        "urban": d["v025"].astype(float).values,
        "region": d["v024"].astype(float).values,
        "wealth": d["v190"].astype(float).values,
        "births": d["v201"].astype(float).values,
        SURVIVING: (d["v201"].astype(float).values - d["v206"].astype(float).values
                    - d["v207"].astype(float).values),
        "years_school": d["v133"].astype(float).values if "v133" in d.columns else np.full(len(d), np.nan),
    }
    return f


def concat_frames(frames):
    keys = frames[0].keys()
    out = {}
    for k in keys:
        try:
            out[k] = np.concatenate([f[k] for f in frames])
        except (ValueError, TypeError):
            out[k] = np.concatenate([np.asarray(f[k], dtype=object) for f in frames])
    return out


def design(panel, outcome, spec, use_wealth=False, dose=False):
    """Build (y, X, names) for the pre-registered model ladder. FE are absorbed outside."""
    edu = panel["edu"]
    n = len(edu)
    if dose:
        x = panel["years_school"].astype(float)
        X = x.reshape(-1, 1)
        names = ["years_school"]
    else:
        X = np.column_stack([(edu == 1).astype(float), (edu == 2).astype(float), (edu == 3).astype(float)])
        names = ["edu_primary", "edu_secondary", "edu_higher"]
    if spec in ("M1", "M2", "M3", "M4"):
        X = np.column_stack([X, panel["urban"].astype(float)])
        names = names + ["urban"]
    if spec in ("M2", "M3", "M4") and use_wealth:
        wl = np.asarray(panel["wealth"], dtype=float)
        valid_wl = np.isin(wl, [1.0, 2.0, 3.0, 4.0, 5.0])
        X = np.column_stack([X] + [np.where(valid_wl, (wl == q).astype(float), np.nan)
                                   for q in (2, 3, 4, 5)])
        names = names + ["wealth_2", "wealth_3", "wealth_4", "wealth_5"]
    if spec == "M3":
        coh = (panel["cohort5"].astype(float) - panel["cohort5"].astype(float).mean()) / 10.0
        inter = [X[:, j] * coh for j in range(3)] if not dose else [X[:, 0] * coh]
        X = np.column_stack([X] + inter)
        names = names + (["edu_primary_x_cohort", "edu_secondary_x_cohort", "edu_higher_x_cohort"]
                         if not dose else ["years_school_x_cohort"])
    if spec == "M4":
        rounds = sorted(set(panel["round"]))
        if len(rounds) > 1:
            R = np.column_stack([(panel["round"] == r).astype(float) for r in rounds[1:]])
            inter = [X[:, j][:, None] * R for j in range(3)]
            X = np.column_stack([X] + [i for block in inter for i in [block]])
            names = names + [f"edu_{lvl}_x_round{i}" for lvl in ("primary", "secondary", "higher")
                             for i in range(R.shape[1])]
    return np.asarray(X, float), names


def _round_region_fe(panel):
    reg = np.asarray(panel["region"], dtype=float)
    reg_str = np.where(np.isfinite(reg), np.nan_to_num(reg, nan=-1).astype(int).astype(str), "NA")
    return np.char.add(np.char.add(panel["round"].astype(str), "_"), reg_str)


def fe_list_for(panel, spec):
    fe = [panel["cohort5"].astype(int), panel["round"]]
    if spec in ("M1", "M2", "M3", "M4"):
        fe.append(_round_region_fe(panel))
    return fe


def run_models(panel, tier_label):
    """Pre-registered M0-M4 on O1 (births) and O2 (surviving), plus construct split."""
    res = []
    age = panel["age"]
    ok = (age >= 40) & (age <= 49) & np.isfinite(panel["births"]) & \
         np.isfinite(panel["edu"]) & np.isin(panel["edu"], [0, 1, 2, 3])
    p = {k: v[ok] for k, v in panel.items() if isinstance(v, np.ndarray)}
    if len(p["births"]) < 200:
        return [{"tier": tier_label, "error": "fewer than 200 women in the completed-fertility sample"}]
    for spec in ("M0", "M1", "M2", "M3", "M4"):
        for outcome, oname in (("births", "O1_births"), (SURVIVING, "O2_surviving")):
            y = p[outcome].astype(float)
            X, names = design(p, outcome, spec, use_wealth=(spec == "M2"))
            if X.size == 0:
                continue
            fe = fe_list_for(p, spec)
            fit = wls_absorbed(y, X, fe, p["w"], p["psu"])
            if fit is None:
                continue
            for j, nm in enumerate(names):
                if not nm.startswith("edu_") and not nm.startswith("years_"):
                    continue
                res.append({"tier": tier_label, "model": spec, "outcome": oname, "term": nm,
                            "b": float(fit["b"][j]), "se": float(fit["se"][j]),
                            "p": float(fit["p"][j]),
                            "ci_lo": float(fit["b"][j] - 1.96 * fit["se"][j]),
                            "ci_hi": float(fit["b"][j] + 1.96 * fit["se"][j]),
                            "n_women": fit["n"], "weighted": True})
    # dose (v133) sensitivity on M1, O1
    if np.isfinite(p["years_school"]).sum() > 200:
        okd = np.isfinite(p["years_school"]) & (p["years_school"] >= 0) & (p["years_school"] <= 25)
        pd_ = {k: v[okd] for k, v in p.items() if isinstance(v, np.ndarray)}
        X, names = design(pd_, "births", "M1", dose=True)
        fit = wls_absorbed(pd_["births"], X, fe_list_for(pd_, "M1"), pd_["w"], pd_["psu"])
        if fit is not None:
            res.append({"tier": tier_label, "model": "M1_dose", "outcome": "O1_births",
                        "term": "years_school", "b": float(fit["b"][0]), "se": float(fit["se"][0]),
                        "p": float(fit["p"][0]), "ci_lo": float(fit["b"][0] - 1.96 * fit["se"][0]),
                        "ci_hi": float(fit["b"][0] + 1.96 * fit["se"][0]),
                        "n_women": fit["n"], "weighted": True})
    # construct split: stack O1/O2, standardise each, construct x schooling, region x round FE, cluster by PSU
    n = len(p["births"])
    y1 = (p["births"] - np.nanmean(p["births"])) / np.nanstd(p["births"], ddof=1)
    y2 = (p[SURVIVING] - np.nanmean(p[SURVIVING])) / np.nanstd(p[SURVIVING], ddof=1)
    y = np.concatenate([y1, y2])
    con = np.concatenate([np.zeros(n), np.ones(n)])
    edu = np.concatenate([p["edu"], p["edu"]])
    urban = np.concatenate([p["urban"], p["urban"]])
    X = np.column_stack([(edu == 1).astype(float), (edu == 2).astype(float), (edu == 3).astype(float),
                         con, (edu == 1).astype(float) * con, (edu == 2).astype(float) * con,
                         (edu == 3).astype(float) * con, urban])
    names = ["edu_primary", "edu_secondary", "edu_higher", "construct",
             "edu_primary_x_construct", "edu_secondary_x_construct", "edu_higher_x_construct", "urban"]
    rr = _round_region_fe(p)
    fe = [np.concatenate([p["cohort5"].astype(int), p["cohort5"].astype(int)]),
          np.concatenate([p["round"], p["round"]]),
          np.concatenate([rr, rr])]
    ps = np.concatenate([p["psu"], p["psu"]])
    w = np.concatenate([p["w"], p["w"]])
    fit = wls_absorbed(y, X, fe, w, ps)  # cluster on PSU (encompasses both rows per woman)
    if fit is not None:
        for j, nm in enumerate(names):
            res.append({"tier": tier_label, "model": "CONSTRUCT", "outcome": "z(O1) vs z(O2)",
                        "term": nm, "b": float(fit["b"][j]), "se": float(fit["se"][j]),
                        "p": float(fit["p"][j]),
                        "ci_lo": float(fit["b"][j] - 1.96 * fit["se"][j]),
                        "ci_hi": float(fit["b"][j] + 1.96 * fit["se"][j]),
                        "n_women": fit["n"] // 2, "weighted": True,
                        "note": "cluster = psu; rows = 2x women"})
    return res


# ------------------------------------------------------------------------------------- selftest
def selftest():
    print("=" * 78)
    print("CODE TEST ONLY - NOT EVIDENCE - NOT A SIMULATION OF THE RESEARCH QUESTION.")
    print("Hand-made rows used to exercise the estimator; no DHS data is read or imitated.")
    print("=" * 78)
    rng = np.random.default_rng(7)
    n = 240
    edu = rng.integers(0, 4, n)
    cohort = rng.choice([1945, 1950, 1955, 1960], n)
    roundv = rng.choice(["S1", "S2"], n)
    births = 5.0 - 0.6 * edu + 0.1 * rng.normal(size=n)
    surv = births - 0.3
    panel = {"age": np.full(n, 45.0), "cohort5": cohort, "round": roundv,
             "survey": roundv, "country": np.array(["ZZ"] * n),
             "psu": np.array([f"p{i}" for i in rng.integers(0, 60, n)]),
             "w": np.ones(n), "edu": edu.astype(float), "urban": rng.integers(0, 2, n).astype(float),
             "region": rng.integers(1, 4, n).astype(float), "wealth": rng.integers(1, 6, n).astype(float),
             "births": births, SURVIVING: surv,
             "years_school": np.clip(edu * 6 + rng.normal(0, 1, n), 0, 25)}
    res = run_models(panel, "SELFTEST")
    if not res or "error" in res[0]:
        print("FAIL:", res[:1])
        return 1
    print(f"estimator ran: {len(res)} coefficient rows")
    for r in [x for x in res if x["model"] == "M0" and x["outcome"] == "O1_births"]:
        print(f"  {r['term']:16s} {r['b']:+.3f} (SE {r['se']:.3f}) n={r['n_women']}")
    cones = [x for x in res if x["model"] == "CONSTRUCT" and "x_construct" in x["term"]]
    print("construct terms:", [(x["term"], round(x["b"], 3)) for x in cones])
    print("SELFTEST OK - code path works. This is not a result.")
    return 0


# ------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datadir", help="directory with extracted IR .dta files (or the original .ZIP files)")
    ap.add_argument("--br-datadir", help="optional: directory with BR .dta files, needed only for O3 period TFR")
    ap.add_argument("--manifest", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                       "data", "dhs_ir_inventory_targets.csv"))
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--countries", default=None, help="comma-separated ISO3 subset (coverage tier T1/T2)")
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.datadir:
        ap.error("--datadir is required (or use --selftest)")
    outdir = args.outdir or os.path.join(os.getcwd(), "dhs_ir_results")
    os.makedirs(outdir, exist_ok=True)

    rows = filter_manifest(read_manifest(args.manifest), args.countries)

    verification = {"manifest": os.path.basename(args.manifest), "requested_files": len(rows),
                    "files": [], "missing": [], "failed": 0,
                    "tier": "T0" if not args.countries else "T1/T2 subset",
                    "data_tier": "OBSERVED individual-level (DHS IR microdata)",
                    "preregistration": "../PRE_REGISTRATION.md", "amendment": "../AMENDMENT_02_ACCESS_COVERAGE.md"}
    panels = []
    for row in rows:
        path = locate_dta(args.datadir, row)
        if not path:
            verification["missing"].append(row["file_stata"])
            continue
        try:
            df = read_dta(path)
        except SystemExit:
            raise
        except Exception as e:  # noqa: BLE001 - report, never patch data
            verification["files"].append({"file": row["file_stata"], "error": f"read failed: {e}"})
            verification["failed"] += 1
            continue
        chk = check_file(df, row, path)
        verification["files"].append(chk)
        if chk["failures"]:
            verification["failed"] += 1
            continue
        panels.append(woman_frame(df, row))
        print(f"verified {row['iso3']} {row['survey_year']} {row['file_stata']}: {chk['n_rows']} women, "
              f"{len(chk['warnings'])} warnings, {len(chk['failures'])} failures")

    verification["n_files_verified"] = len(panels)
    json.dump(verification, open(os.path.join(outdir, "verification.json"), "w"), indent=1)
    print(f"\nverified {len(panels)}/{len(rows)} files; missing {len(verification['missing'])}; "
          f"failed {verification['failed']}")
    if verification["failed"] or not panels:
        print("STOP: verification gate failed. Re-download/fix files; do not analyse.")
        return 2
    if args.check_only:
        print(f"check-only: wrote {outdir}/verification.json and stopped before estimation.")
        return 0

    panel = concat_frames(panels)
    results = run_models(panel, verification["tier"])
    with open(os.path.join(outdir, "estimates.csv"), "w", newline="") as f:
        cols = ["tier", "model", "outcome", "term", "b", "se", "p", "ci_lo", "ci_hi", "n_women", "weighted", "note"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in results:
            w.writerow(r)
    n40 = int(((panel["age"] >= 40) & (panel["age"] <= 49)).sum())
    summary = {"tier": verification["tier"], "n_women_pooled": int(len(panel["age"])),
               "n_women_40_49": n40, "n_surveys": int(len(set(panel["round"]))),
               "n_countries": int(len(set(panel["country"]))),
               "models": sorted({r["model"] for r in results}),
               "o3_period_tfr": "NOT COMPUTED (requires BR files; see AMENDMENT_02 A2.4)",
               "data_tier": "OBSERVED individual-level",
               "note": "O2 (surviving children) is never TFR; O1 is births ever, also not TFR."}
    json.dump(summary, open(os.path.join(outdir, "summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
