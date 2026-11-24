#!/usr/bin/env python3
"""Observed-core full-system model (task-42).

Reduced-form predictive panel system at country-year level, built only from observed
WDI/EdStats series (see PRE_REGISTRATION.md + Amendments 01-03). Nothing here is
causal; learning/gates/jobs/migration/borrowing are declared assumptions and are not
fitted.

Outputs (to --out):
  predictive.csv    every multiverse cell (folds, FE, controls, transform)
  transmission.csv  pre-declared 5/10-year long-difference associations
  verdicts.csv      pre-declared PASS/WEAK/FAIL per outcome x horizon
  summary.json      machine-readable summary
  RUN_LOG.txt       command, host, versions, wall time, hashes
"""
import argparse, csv, hashlib, json, math, os, platform, socket, sys, time, datetime
from itertools import product
import numpy as np

# ---------------------------------------------------------------- data spec
OUTCOMES = [
    # name, indicator code, level
    ("ger_primary", "SE.PRM.ENRR", "primary"),
    ("ger_secondary", "SE.SEC.ENRR", "secondary"),
    ("cmpt_primary", "SE.PRM.CMPT.ZS", "primary"),
    ("cmpt_lower_sec", "SE.SEC.CMPT.LO.ZS", "secondary"),
    ("ptr_primary", "SE.PRM.ENRL.TC.ZS", "primary"),
    ("ptr_lower_sec", "SE.SEC.ENRL.LO.TC.ZS", "secondary"),
]
LEVEL_ENROL = {"primary": "SE.PRM.ENRR", "secondary": "SE.SEC.ENRR"}
LEVEL_PERSTUD = {"primary": "SE.XPD.PRIM.PC.ZS", "secondary": "SE.XPD.SECO.PC.ZS"}
RANGE = {"ger_primary": (0, 150), "ger_secondary": (0, 150),
         "cmpt_primary": (0, 100), "cmpt_lower_sec": (0, 100),
         "ptr_primary": (0, 100), "ptr_lower_sec": (0, 100)}

CANDIDATES = ["lag_outcome", "lngdp", "spend", "perstudent", "urban", "childemp",
              "agri", "enrol_lag"]
CONTROLS = {
    "base": ["lag_outcome", "lngdp"],
    "supply": ["lag_outcome", "lngdp", "spend", "perstudent"],
    "full": ["lag_outcome", "lngdp", "spend", "perstudent", "urban", "childemp",
             "agri", "enrol_lag"],
}
# 'enrol_lag' is only used for completion/PTR outcomes (for GER it duplicates lag_outcome)

FE_LOO = ["none", "year", "decade", "region_decade"]
FE_REGION = ["none", "year", "decade", "region_decade"]
FE_TIMEBLOCK = ["country", "country+region", "country+trend", "country+region_trend"]
FORMS = ["level", "log", "logit"]

CACHE = {}


# ---------------------------------------------------------------- loading
def load_data(data_dir):
    if "panel" in CACHE:
        return CACHE["panel"], CACHE["countries"], CACHE["meta"]
    countries = {}
    with open(os.path.join(data_dir, "countries.csv")) as f:
        for r in csv.DictReader(f):
            countries[r["iso3"]] = r
    panel = {}
    with open(os.path.join(data_dir, "wdi_long.csv")) as f:
        for r in csv.DictReader(f):
            k = (r["iso3"], int(r["year"]))
            panel.setdefault(k, {})[r["indicator"]] = float(r["value"])
    CACHE.update(panel=panel, countries=countries, meta={"data_dir": data_dir})
    return panel, countries, CACHE["meta"]


def get_rows(panel, countries, outcome, code, level, h):
    key = ("rows", outcome, h)
    if key not in CACHE:
        CACHE[key] = build_rows(panel, countries, outcome, code, level, h)
    return CACHE[key]


def build_rows(panel, countries, outcome, code, level, h):
    """Rows for y at t and candidate predictors at t-h. Complete cases handled per spec."""
    enrol_code = LEVEL_ENROL[level]
    pers_code = LEVEL_PERSTUD[level]
    rows = []
    for (iso, t), d in panel.items():
        if code not in d:
            continue
        prev = panel.get((iso, t - h))
        if not prev or code not in prev:
            continue
        y = d[code]
        lag = prev[code]
        lngdp = math.log(prev["NY.GDP.PCAP.KD"]) if prev.get("NY.GDP.PCAP.KD", 0) > 0 else None
        rows.append({
            "iso": iso, "year": t, "region": countries[iso]["region"],
            "y": y, "lag_outcome": lag, "lngdp": lngdp,
            "spend": prev.get("SE.XPD.TOTL.GD.ZS"),
            "perstudent": prev.get(pers_code),
            "urban": prev.get("SP.URB.TOTL.IN.ZS"),
            "childemp": prev.get("SL.TLF.0714.ZS"),
            "agri": prev.get("SL.AGR.EMPL.ZS"),
            "enrol_lag": prev.get(enrol_code),
        })
    rows.sort(key=lambda r: (r["iso"], r["year"]))
    return rows


# ---------------------------------------------------------------- design / OLS
def transform(y, form):
    y = np.asarray(y, float)
    if form == "level":
        return y, (lambda p: p)
    if form == "log":
        if np.any(y <= 0) or np.all(~np.isfinite(y)):
            return None, None
        return np.log(y), (lambda p: np.exp(np.clip(p, -50, 50)))
    s = np.clip(y / 100.0, 1e-3, 1 - 1e-3)
    z = np.log(s / (1 - s))
    return z, (lambda p: 100.0 / (1.0 + np.exp(-np.clip(p, -50, 50))))


def _cat(row, part):
    if part == "country":
        return row["iso"]
    if part == "year":
        return row["year"]
    if part == "decade":
        return (row["year"] // 10) * 10
    if part == "region":
        return row["region"]
    if part == "region_decade":
        return row["region"] + "_" + str((row["year"] // 10) * 10)
    if part == "region_year":
        return row["region"] + "_" + str(row["year"])
    raise ValueError(part)


def build_design(train, test, cols, fe_spec):
    """Return (Xtr, Xte, n_unseen_cat). Categorical FE from training levels, ref = first."""
    tr_n = len(train)
    te_n = len(test)
    Xtr, Xte = [np.ones(tr_n)], [np.ones(te_n)]
    for c in cols:
        Xtr.append(np.array([r[c] for r in train], float))
        Xte.append(np.array([r[c] for r in test], float))
    unseen = 0
    parts = fe_spec.split("+") if fe_spec != "none" else []
    for part in parts:
        if part == "trend":
            tr = np.array([r["year"] - 2000 for r in train], float)
            te = np.array([r["year"] - 2000 for r in test], float)
            Xtr.append(tr); Xte.append(te)
        elif part == "region_trend":
            tr_y = np.array([r["year"] - 2000 for r in train], float)
            te_y = np.array([r["year"] - 2000 for r in test], float)
            Xtr.append(tr_y); Xte.append(te_y)
            regions = sorted({r["region"] for r in train})
            for g in regions[1:]:
                Xtr.append(tr_y * np.array([1.0 if r["region"] == g else 0.0 for r in train]))
                Xte.append(te_y * np.array([1.0 if r["region"] == g else 0.0 for r in test]))
        else:
            cats = sorted({_cat(r, part) for r in train})
            unseen += sum(1 for r in test if _cat(r, part) not in cats)
            for g in cats[1:]:
                Xtr.append(np.array([1.0 if _cat(r, part) == g else 0.0 for r in train]))
                Xte.append(np.array([1.0 if _cat(r, part) == g else 0.0 for r in test]))
    return np.column_stack(Xtr), np.column_stack(Xte), unseen


def fit_predict(train, test, cols, ycol, fe_spec, form):
    ytr = np.array([r[ycol] for r in train], float)
    yte = np.array([r[ycol] for r in test], float)
    ztr, inv = transform(ytr, form)
    if ztr is None:
        return None
    Xtr, Xte, unseen = build_design(train, test, cols, fe_spec)
    # drop training columns that are constant zero or non-finite (safe)
    good = np.all(np.isfinite(Xtr), axis=0)
    Xtr, Xte = Xtr[:, good], Xte[:, good]
    coef, *_ = np.linalg.lstsq(Xtr, ztr, rcond=None)
    pred = inv(Xte @ coef)
    return np.asarray(pred, float), unseen


# ---------------------------------------------------------------- benchmarks
def trend_prediction(train, test, ycol, kind):
    if kind == "region":
        pred = np.full(len(test), np.nan)
        for reg in sorted({r["region"] for r in test}):
            tr = [r for r in train if r["region"] == reg and np.isfinite(r[ycol])]
            if len(tr) < 30:
                continue
            xs = np.array([r["year"] for r in tr], float)
            ys = np.array([r[ycol] for r in tr], float)
            A = np.column_stack([np.ones(len(xs)), xs])
            coef, *_ = np.linalg.lstsq(A, ys, rcond=None)
            idx = [i for i, r in enumerate(test) if r["region"] == reg]
            pred[idx] = coef[0] + coef[1] * np.array([test[i]["year"] for i in idx], float)
        if np.all(~np.isfinite(pred)):
            return trend_prediction(train, test, ycol, "global")
        # fallback global for rows without a regional fit
        miss = ~np.isfinite(pred)
        if miss.any():
            g = trend_prediction(train, test, ycol, "global")
            if g is not None:
                pred[miss] = g[miss]
        return pred
    if kind == "global":
        ys = np.array([r[ycol] for r in train], float)
        ys = ys[np.isfinite(ys)]
        if len(ys) < 30:
            return None
        xs = np.array([r["year"] for r in train], float)
        A = np.column_stack([np.ones(len(xs)), xs])
        coef, *_ = np.linalg.lstsq(A, ys, rcond=None)
        return np.column_stack([np.ones(len(test)), np.array([r["year"] for r in test], float)]) @ coef
    # country trend from last <=10 training obs, min 3
    by = {}
    for r in train:
        by.setdefault(r["iso"], []).append(r)
    pred = np.full(len(test), np.nan)
    for i, r in enumerate(test):
        obs = sorted(by.get(r["iso"], []), key=lambda q: q["year"])[-10:]
        obs = [q for q in obs if np.isfinite(q[ycol])]
        if len(obs) >= 3:
            xs = np.array([q["year"] for q in obs], float)
            ys = np.array([q[ycol] for q in obs], float)
            A = np.column_stack([np.ones(len(xs)), xs])
            coef, *_ = np.linalg.lstsq(A, ys, rcond=None)
            pred[i] = coef[0] + coef[1] * r["year"]
    return pred


def score(pred, y, clip):
    pred = np.clip(pred, clip[0], clip[1])
    ok = np.isfinite(pred) & np.isfinite(y)
    if ok.sum() < 2:
        return None
    e = pred[ok] - y[ok]
    return {"rmse": float(np.sqrt(np.mean(e ** 2))), "mae": float(np.mean(np.abs(e))),
            "n": int(ok.sum())}


def skill(rmse_model, rmse_bench):
    if not (rmse_bench and rmse_bench > 0):
        return float("nan")
    return float(1.0 - (rmse_model / rmse_bench) ** 2)


# ---------------------------------------------------------------- folds
def make_folds(countries, seed=20261125, k=5):
    isos = sorted(countries)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(isos))
    folds = [[] for _ in range(k)]
    for j, idx in enumerate(perm):
        folds[j % k].append(isos[idx])
    return folds


# ---------------------------------------------------------------- one cell
def cell_worker(args):
    outcome, code, level, h, split, block, fe, controls, form, data_dir = args
    panel, countries, _ = load_data(data_dir)
    rows = get_rows(panel, countries, outcome, code, level, h)
    cols = CONTROLS[controls]
    if outcome.startswith("ger_"):
        cols = [c for c in cols if c != "enrol_lag"]
    # split
    if split == "loo":
        folds = make_folds(countries)
        test_isos = set(folds[block])
        train = [r for r in rows if r["iso"] not in test_isos]
        test = [r for r in rows if r["iso"] in test_isos]
        trend_kind = "region"
    elif split == "region":
        regions = sorted({r["region"] for r in rows})
        reg = regions[block]
        train = [r for r in rows if r["region"] != reg]
        test = [r for r in rows if r["region"] == reg]
        trend_kind = "region"
    else:  # time
        if block == 0:
            start, end = 2001, 2012
        else:
            start, end = 2011, 2023
        if h == 5:
            T = 2000 if block == 0 else 2010
            train = [r for r in rows if r["year"] <= T]
            test = [r for r in rows if r["year"] == T + 5]
        else:
            train = [r for r in rows if r["year"] <= start - 1]
            test = [r for r in rows if start <= r["year"] <= end]
        trend_kind = "country"
    # complete cases
    def complete(r):
        return all(r.get(c) is not None and np.isfinite(r[c]) for c in cols) and np.isfinite(r["y"])
    train = [r for r in train if complete(r)]
    test = [r for r in test if complete(r)]
    rec = {"outcome": outcome, "horizon": h, "split": split, "block": block,
           "fe": fe, "controls": controls, "form": form,
           "n_train": len(train), "n_test": len(test),
           "n_countries_test": len({r["iso"] for r in test})}
    if len(train) < 200 or len(test) < 30:
        rec.update(status="skipped", reason="n_train<200 or n_test<30")
        return rec
    fp = fit_predict(train, test, cols, "y", fe, form)
    if fp is None:
        rec.update(status="skipped", reason="transform not applicable")
        return rec
    pred, unseen = fp
    y = np.array([r["y"] for r in test], float)
    pers = np.array([r["lag_outcome"] for r in test], float)
    mean = float(np.mean([r["y"] for r in train]))
    m = score(pred, y, RANGE[outcome])
    b_p = score(pers, y, RANGE[outcome])
    b_m = score(np.full(len(test), mean), y, RANGE[outcome])
    tp = trend_prediction(train, test, "y", trend_kind)
    b_t = score(tp, y, RANGE[outcome]) if tp is not None else None
    if m is None or b_p is None or b_m is None:
        rec.update(status="skipped", reason="score undefined")
        return rec
    rec.update(status="ok", unseen_cat=unseen,
               rmse_model=m["rmse"], mae_model=m["mae"],
               rmse_persist=b_p["rmse"], rmse_mean=b_m["rmse"],
               rmse_trend=(b_t["rmse"] if b_t else None),
               skill_persist=skill(m["rmse"], b_p["rmse"]),
               skill_trend=(skill(m["rmse"], b_t["rmse"]) if b_t else None),
               skill_mean=skill(m["rmse"], b_m["rmse"]))
    return rec


# ---------------------------------------------------------------- transmission
def _diff_rows(panel, countries, out_code, driver_code, h, extra=None):
    rows = []
    for (iso, t), d in panel.items():
        prev = panel.get((iso, t - h))
        if not prev or out_code not in d or out_code not in prev:
            continue
        if driver_code not in d or driver_code not in prev:
            continue
        row = {"iso": iso, "year": t, "region": countries[iso]["region"],
               "dy": d[out_code] - prev[out_code],
               "dx": d[driver_code] - prev[driver_code]}
        if extra:
            ec = extra
            if ec not in d or ec not in prev or d[ec] <= 0 or prev[ec] <= 0:
                continue
            row["dln"] = math.log(d[ec]) - math.log(prev[ec])
        rows.append(row)
    return rows


def cluster_ols(rows, fe_spec, xcol="dx", extra_col=None, ycol="dy"):
    cols = [xcol] + ([extra_col] if extra_col else [])
    tr = [r for r in rows if all(np.isfinite(r.get(c, np.nan)) for c in cols + [ycol])]
    if len(tr) < 50:
        return None
    X, _, _ = build_design(tr, tr[:1], cols, fe_spec)
    y = np.array([r[ycol] for r in tr], float)
    good = np.all(np.isfinite(X), axis=0)
    X = X[:, good]
    XtX = X.T @ X
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ coef
    # cluster by country
    groups = {}
    for i, r in enumerate(tr):
        groups.setdefault(r["iso"], []).append(i)
    meat = np.zeros_like(XtX)
    for idx in groups.values():
        Xi = X[idx]; ui = resid[idx]
        s = Xi.T @ ui
        meat += np.outer(s, s)
    try:
        XtX_inv = np.linalg.pinv(XtX)
    except np.linalg.LinAlgError:
        return None
    G = len(groups); N = len(tr); K = X.shape[1]
    scale = (G / (G - 1)) * ((N - 1) / (N - K)) if G > 1 and N > K else 1.0
    V = XtX_inv @ meat @ XtX_inv * scale
    se = math.sqrt(max(V[1, 1], 0.0)) if V.shape[0] > 1 else float("nan")
    return {"coef": float(coef[1]), "se": se,
            "t": float(coef[1] / se) if se and se > 0 else float("nan"),
            "n": N, "n_countries": G, "fe": fe_spec,
            "controls": (extra_col or "none")}


TRANSMISSION = [
    ("T1", "ger_primary", "SE.PRM.ENRR", "NY.GDP.PCAP.KD", "ln"),
    ("T2", "ger_secondary", "SE.SEC.ENRR", "NY.GDP.PCAP.KD", "ln"),
    ("T3", "ger_primary", "SE.PRM.ENRR", "SL.TLF.0714.ZS", "level"),
    ("T4", "ger_secondary", "SE.SEC.ENRR", "SL.AGR.EMPL.ZS", "level"),
    ("T5", "ptr_primary", "SE.PRM.ENRL.TC.ZS", "SE.XPD.TOTL.GD.ZS", "level"),
    ("T6", "cmpt_primary", "SE.PRM.CMPT.ZS", "SE.XPD.PRIM.PC.ZS", "level"),
    ("T7", "agri", "SL.AGR.EMPL.ZS", "SE.PRM.CMPT.ZS", "level"),
]
PRED_SIGN = {"T1": "+", "T2": "+", "T3": "-", "T4": "-", "T5": "-", "T6": "+", "T7": "-"}


def transmission_worker(args):
    (tid, driver_code, sign, out_code, h, fe, data_dir) = args
    panel, countries, _ = load_data(data_dir)
    if tid in ("T1", "T2"):
        rows = _diff_rows(panel, countries, out_code, driver_code, h, extra=None)
        # driver is log GDP pc: difference of log, not log of difference
        rows2 = []
        for (iso, t), d in panel.items():
            prev = panel.get((iso, t - h))
            if not prev or out_code not in d or out_code not in prev:
                continue
            if prev.get(driver_code, 0) <= 0 or d.get(driver_code, 0) <= 0:
                continue
            rows2.append({"iso": iso, "year": t, "region": countries[iso]["region"],
                          "dy": d[out_code] - prev[out_code],
                          "dx": math.log(d[driver_code]) - math.log(prev[driver_code])})
        rows = rows2
        extra = None
    elif tid in ("T3", "T4", "T5", "T6"):
        rows = _diff_rows(panel, countries, out_code, driver_code, h, extra="NY.GDP.PCAP.KD")
        extra = "dln"
    else:  # T7: agri employment change on completion change
        rows = _diff_rows(panel, countries, out_code, driver_code, h, extra="NY.GDP.PCAP.KD")
        extra = "dln"
    recs = []
    for use in ([None, extra] if extra else [None]):
        r = cluster_ols(rows, fe, xcol="dx", extra_col=use, ycol="dy")
        if r:
            r.update(t_id=tid, driver=driver_code, outcome=out_code, h=h,
                     expected_sign=sign, extra_control=(use or "none"))
            recs.append(r)
    return recs


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    ap.add_argument("--out", default="results")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--seed", type=int, default=20261125)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    panel, countries, _ = load_data(a.data)

    fe_loo = ["none", "year", "decade", "region_decade"]
    fe_reg = fe_loo
    fe_tb = ["country", "country+region", "country+trend", "country+region_trend"]

    tasks = []
    outs = OUTCOMES
    hs = [1, 5]
    if a.smoke:
        outs = OUTCOMES[:2]; hs = [1]
    for (outcome, code, level) in outs:
        for h in hs:
            if a.smoke:
                for fe in ["none"]:
                    for ctl in ["base"]:
                        for form in ["level"]:
                            tasks.append((outcome, code, level, h, "loo", 0, fe, ctl, form, a.data))
            else:
                for fold in range(5):
                    for fe in fe_loo:
                        for ctl in CONTROLS:
                            for form in FORMS:
                                tasks.append((outcome, code, level, h, "loo", fold, fe, ctl, form, a.data))
                regions = sorted({c["region"] for c in countries.values()})
                for bi, _reg in enumerate(regions):
                    for fe in fe_reg:
                        for ctl in CONTROLS:
                            for form in FORMS:
                                tasks.append((outcome, code, level, h, "region", bi, fe, ctl, form, a.data))
                for block in (0, 1):
                    for fe in fe_tb:
                        for ctl in CONTROLS:
                            for form in FORMS:
                                tasks.append((outcome, code, level, h, "time", block, fe, ctl, form, a.data))

    print(f"prediction cells: {len(tasks)}", flush=True)
    rows_out = []
    if a.workers > 1:
        import multiprocessing as mp
        with mp.Pool(a.workers) as pool:
            for i, rec in enumerate(pool.imap_unordered(cell_worker, tasks, chunksize=8)):
                rows_out.append(rec)
                if (i + 1) % 500 == 0:
                    print(f"  {i+1}/{len(tasks)} cells", flush=True)
    else:
        for i, t in enumerate(tasks):
            rows_out.append(cell_worker(t))
            if (i + 1) % 500 == 0:
                print(f"  {i+1}/{len(tasks)} cells", flush=True)

    fields = ["outcome", "horizon", "split", "block", "fe", "controls", "form",
              "n_train", "n_test", "n_countries_test", "status", "reason",
              "rmse_model", "mae_model", "rmse_persist", "rmse_trend", "rmse_mean",
              "skill_persist", "skill_trend", "skill_mean", "unseen_cat"]
    for r in rows_out:
        for f in fields:
            r.setdefault(f, None)
    with open(os.path.join(a.out, "predictive.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows_out)

    # verdicts from LOO cells
    verdicts = []
    for (outcome, code, level) in outs:
        for h in hs:
            cells = [r for r in rows_out if r["outcome"] == outcome and r["horizon"] == h
                     and r["split"] == "loo" and r["status"] == "ok"]
            if not cells:
                verdicts.append({"outcome": outcome, "horizon": h, "n_cells": 0,
                                 "verdict": "NO_DATA"})
                continue
            # per-cell pass: need fold-level win share >= 0.6 and overall conditions.
            # Fold share is computed across the 5 folds within the same (fe, controls, form) cell.
            cells_by_spec = {}
            for r in cells:
                key = (r["fe"], r["controls"], r["form"])
                cells_by_spec.setdefault(key, []).append(r)
            pass_n = weak_n = fail_n = 0
            for key, cs in cells_by_spec.items():
                if len(cs) < 5:
                    continue
                wins = sum(1 for r in cs if (r["skill_persist"] or -9) > 0)
                # pooled skill approximated by mean of fold skills weighted by n_test
                ws = np.array([r["skill_persist"] for r in cs], float)
                wt = np.array([(r["skill_trend"] if r["skill_trend"] is not None else np.nan) for r in cs], float)
                pooled = float(np.nanmean(ws))
                pooled_t = float(np.nanmean(wt))
                cond = (wins / len(cs) >= 0.6) and pooled >= 0.05 and (np.isfinite(pooled_t) and pooled_t >= 0)
                if cond:
                    pass_n += 1
                elif wins / len(cs) >= 0.6 and pooled >= 0:
                    weak_n += 1
                else:
                    fail_n += 1
            total = pass_n + weak_n + fail_n
            share_pass = pass_n / total if total else 0.0
            share_weak = weak_n / total if total else 0.0
            verdict = ("PASS" if share_pass >= 0.5 else "WEAK" if share_pass + share_weak >= 0.2 else "FAIL")
            sk = np.array([r["skill_persist"] for r in cells], float)
            st = np.array([r["skill_trend"] for r in cells if r["skill_trend"] is not None], float)
            verdicts.append({
                "outcome": outcome, "horizon": h, "n_cells": len(cells),
                "n_specs": total, "share_pass": round(share_pass, 3),
                "share_weak": round(share_weak, 3), "verdict": verdict,
                "median_skill_persist": round(float(np.nanmedian(sk)), 4),
                "median_skill_trend": round(float(np.nanmedian(st)), 4) if len(st) else None,
                "share_cells_beating_persistence": round(float(np.mean(sk > 0)), 3),
            })
    with open(os.path.join(a.out, "verdicts.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(verdicts[0].keys()))
        w.writeheader(); w.writerows(verdicts)

    # transmission
    trows = []
    ttasks = []
    for (tid, outname, out_code, driver_code, kind) in TRANSMISSION:
        for h in ([5] if a.smoke else [5, 10]):
            for fe in (["country+decade"] if a.smoke else ["country+decade", "country+region_decade"]):
                ttasks.append((tid, driver_code, PRED_SIGN[tid], out_code, h, fe, a.data))
    for t in ttasks:
        recs = transmission_worker(t)
        trows.extend(recs)
    tfields = ["t_id", "driver", "outcome", "h", "fe", "extra_control", "coef", "se", "t",
               "n", "n_countries", "expected_sign"]
    if trows:
        with open(os.path.join(a.out, "transmission.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=tfields, extrasaction="ignore")
            w.writeheader(); w.writerows(trows)

    summary = {
        "tier": "OBSERVED core + declared assumptions (learning/gates/jobs/migration/borrowing not fitted)",
        "outcomes": [o[0] for o in outs], "horizons": hs, "n_cells": len(tasks),
        "wall_seconds": round(time.time() - t0, 1),
        "verdicts": verdicts,
        "transmission_rows": len(trows),
        "data_dir": a.data,
    }
    with open(os.path.join(a.out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)

    # run log + manifest
    def sha(p):
        return hashlib.sha256(open(p, "rb").read()).hexdigest()
    log = [
        f"started_utc: {datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}",
        f"host: {socket.gethostname()}", f"platform: {platform.platform()}",
        f"python: {sys.version.split()[0]}", f"numpy: {np.__version__}",
        f"argv: {' '.join(sys.argv)}", f"workers: {a.workers}", f"smoke: {a.smoke}",
        f"data_rows: {sum(len(v) for v in panel.values())}",
        f"wall_seconds: {round(time.time() - t0, 1)}",
    ]
    for p in ["data/wdi_long.csv", "data/countries.csv", "data/MANIFEST.json"]:
        fp = os.path.join(os.path.dirname(a.out.rstrip('/')), p)
        if os.path.exists(fp):
            log.append(f"sha256 {p}: {sha(fp)}")
    here = os.path.abspath(__file__)
    log.append(f"sha256 script: {sha(here)}")
    with open(os.path.join(a.out, "RUN_LOG.txt"), "w") as f:
        f.write("\n".join(log) + "\n")
    man = {os.path.basename(p): sha(p) for p in
           [os.path.join(a.out, x) for x in ("predictive.csv", "verdicts.csv", "summary.json",
                                             "RUN_LOG.txt")]
           if os.path.exists(p)}
    with open(os.path.join(a.out, "MANIFEST.json"), "w") as f:
        json.dump(man, f, indent=2, sort_keys=True)
    print(json.dumps({"verdicts": verdicts, "wall_seconds": summary["wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
