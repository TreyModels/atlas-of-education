#!/usr/bin/env python3
"""Data-level test bench, v2 — REWRITTEN 25 Nov 2026 after the line audit.

What was wrong with the first version (kept in git history as `test_bench2.py` v1):

1. **F9 joined on the wrong lag and returned n = 0.** The cached long-run panel has annual rows but
   `mean_years_schooling` is only populated on ~5-year marks; v1 used `build(lag=1)`, so the join
   asked for schooling in `y-1`, which is missing almost everywhere -> **0 usable rows** and an F9
   verdict computed from nothing. The lag is a property of the data: with the schooling-observation
   spacing (5 years) the join gives ~1,560 rows (~1,495 with controls). This version derives the lag
   from the data, reports n / countries / folds for every fit, and refuses to emit a verdict on an
   empty join.
2. **Singular normal equations.** `np.linalg.inv(X.T @ X)` raised `LinAlgError: Singular matrix`
   when a control was constant/collinear in the estimation window. Now an SVD rank guard drops
   collinear control columns (never the intercept or the schooling column) and records
   `dropped_controls`; if the design is still rank-deficient the fit is `not identifiable`.
3. The permutation control ran the same build twice (copy-paste), and E8/PHL were silently absent.
   E8 fee dates can be supplied with `--e8-dir` (they live on `research/e6e8-sequencing-2026-11-25`
   and `research/paper-massification-2026-11-25`; copy with SHA-256 provenance); PHL K-12 is
   **UNTESTABLE** unless a series is supplied with `--phl-series`.

Nothing here is a causal test: descriptive OOS prediction on observational panels. Verdict vocabulary
is deliberately weak: SUPPORTED / REJECTED / NOT IDENTIFIED / UNTESTABLE.
"""
import argparse
import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter

import numpy as np

COLS = ("mean_years_schooling", "tfr_observed_1950plus", "effective_fertility",
        "urban_share_pct", "gdp_pc_maddison_1990int", "child_mortality_per100")
CONTROLS = ("urban_share_pct", "gdp_pc_maddison_1990int")
HERE = os.path.dirname(os.path.abspath(__file__))


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_panel(data_dir):
    path = os.path.join(data_dir, "long_run_panel.csv")
    rows = list(csv.DictReader(open(path)))
    panel = {}
    for r in rows:
        panel.setdefault(r["iso3"], {})[int(r["year"])] = {k: fnum(r[k]) for k in COLS}
    return panel, path, len(rows)


def native_lag(panel):
    """Spacing between consecutive observations of the *schooling* series (the sparse one)."""
    gaps = []
    for ys in panel.values():
        yrs = sorted(y for y, v in ys.items() if v.get("mean_years_schooling") is not None)
        gaps += [b - a for a, b in zip(yrs, yrs[1:]) if b > a]
    if not gaps:
        return 1
    return int(Counter(gaps).most_common(1)[0][0])


def build(panel, lag, controls=True, logx=False, dependent="tfr_observed_1950plus"):
    """Lagged long difference: Δoutcome(y-lag → y) on Δschooling(y-lag → y) (+ Δcontrols)."""
    out = []
    for iso, ys in panel.items():
        for y in sorted(ys):
            if y - lag not in ys:
                continue
            a, b = ys[y - lag], ys[y]
            if a.get(dependent) is None or b.get(dependent) is None:
                continue
            if a.get("mean_years_schooling") is None or b.get("mean_years_schooling") is None:
                continue
            dy = b[dependent] - a[dependent]
            if logx:
                dx = math.log(max(b["mean_years_schooling"], 0.01)) - math.log(max(a["mean_years_schooling"], 0.01))
            else:
                dx = b["mean_years_schooling"] - a["mean_years_schooling"]
            cs = []
            if controls:
                for k in CONTROLS:
                    if a.get(k) is None or b.get(k) is None:
                        cs = []
                        break
                    cs.append(b[k] - a[k])
                if not cs:
                    continue
            out.append((iso, y, dy, dx, cs))
    return out


def ols_cluster(rows, wins=False):
    """OLS with cluster-robust SE for the schooling coefficient; rank-guarded. Returns dict."""
    if len(rows) < 100:
        return {"ok": False, "n": len(rows), "reason": "fewer than 100 usable rows"}
    yv = np.array([r[2] for r in rows], float)
    xv = np.array([r[3] for r in rows], float)
    nctrl = len(rows[0][4])
    cols = [np.ones(len(rows)), xv.copy()] + [np.array([r[4][j] for r in rows], float)
                                              for j in range(nctrl)]
    if wins:
        lo, hi = np.percentile(yv, [1, 99])
        yv = np.clip(yv, lo, hi)
        lo, hi = np.percentile(xv, [1, 99])
        cols[1] = np.clip(xv, lo, hi)
    X = np.column_stack(cols)
    if float(np.std(yv)) < 1e-12:
        return {"ok": False, "n": len(rows), "reason": "outcome has no variance"}
    smax = float(np.linalg.svd(X, compute_uv=False)[0])
    tol = 1e-8 * smax * max(X.shape)
    keep = list(range(X.shape[1]))
    dropped = []
    while len(keep) > 2 and np.linalg.matrix_rank(X[:, keep], tol=tol) < len(keep):
        last = max(j for j in keep if j >= 2)
        keep.remove(last)
        dropped.append(last - 2)          # control index
    Xk = X[:, keep]
    rank = np.linalg.matrix_rank(Xk, tol=tol)
    if rank < Xk.shape[1]:
        return {"ok": False, "n": len(rows), "n_countries": len({r[0] for r in rows}),
                "reason": "design not identifiable even after dropping collinear controls",
                "dropped_controls": dropped}
    beta, *_ = np.linalg.lstsq(Xk, yv, rcond=None)
    resid = yv - Xk @ beta
    groups = np.array([r[0] for r in rows])
    meat = np.zeros((Xk.shape[1], Xk.shape[1]))
    for g in set(groups.tolist()):
        m = groups == g
        sc = Xk[m].T @ resid[m]
        meat += np.outer(sc, sc)
    XtX_inv = np.linalg.pinv(Xk.T @ Xk)
    G = len(set(groups.tolist()))
    n = Xk.shape[0]
    corr = (G / (G - 1)) * ((n - 1) / (n - rank)) if G > 1 and n > rank else 1.0
    V = XtX_inv @ meat @ XtX_inv * corr
    beta_j = float(beta[1])
    se = math.sqrt(max(float(V[1, 1]), 0.0))
    return {"ok": True, "n": int(n), "n_countries": int(G), "beta": beta_j, "se": se,
            "ci": [beta_j - 1.96 * se, beta_j + 1.96 * se],
            "dropped_controls": dropped, "rank": int(rank)}


def oos(rows, test_year=2000, min_train=150, min_test=10):
    """5-fold by-country OOS: does the lagged model beat persistence and the training mean?"""
    if len(rows) < 200:
        return {"ok": False, "n": len(rows), "reason": "fewer than 200 usable rows", "n_folds": 0}
    folders = sorted({r[0] for r in rows})
    fold = {c: int(hashlib.md5(c.encode()).hexdigest(), 16) % 5 for c in folders}
    mr, pr, nr = [], [], []
    for k in range(5):
        tr = [r for r in rows if fold[r[0]] != k and r[1] <= test_year]
        te = [r for r in rows if fold[r[0]] == k and r[1] > test_year]
        if len(tr) < min_train or len(te) < min_test:
            continue
        fit = ols_cluster(tr)
        if not fit.get("ok"):
            continue
        keep = [j for j in range(len(tr[0][4])) if j not in fit.get("dropped_controls", [])]
        Xtr = np.column_stack([np.ones(len(tr)), np.array([r[3] for r in tr])] +
                              [np.array([r[4][j] for r in tr], float) for j in keep])
        ytr = np.array([r[2] for r in tr], float)
        b, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
        pred = b[0] + b[1] * np.array([r[3] for r in te]) + sum(
            b[2 + i] * np.array([r[4][j] for r in te]) for i, j in enumerate(keep))
        ty = np.array([r[2] for r in te])
        mr.append(float(np.sqrt(np.mean((ty - pred) ** 2))))
        pr.append(float(np.sqrt(np.mean(ty ** 2))))
        nr.append(float(np.sqrt(np.mean((ty - np.mean(ytr)) ** 2))))
    if not mr:
        return {"ok": False, "n": len(rows), "reason": "no fold had enough train/test rows", "n_folds": 0}
    fit_all = ols_cluster(rows)
    return {"ok": True, "n": len(rows), "n_folds": len(mr),
            "n_countries": int(len({r[0] for r in rows})),
            "model_rmse": float(np.mean(mr)), "persistence_rmse": float(np.mean(pr)),
            "null_rmse": float(np.mean(nr)),
            "folds_beat": int(sum(1 for a_, b_, c_ in zip(mr, pr, nr) if a_ < min(b_, c_))),
            "beta": fit_all.get("beta"), "se": fit_all.get("se"), "ci": fit_all.get("ci"),
            "dropped_controls": fit_all.get("dropped_controls", [])}


def decide(r, share, beats, excl):
    if not r.get("ok"):
        return "NOT IDENTIFIED"
    if not beats:
        return "REJECTED (does not beat both benchmarks)"
    if not excl:
        return "NOT IDENTIFIED"
    if share < 0.8:
        return "REJECTED (sign unstable across specifications)"
    return "SUPPORTED"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=os.path.join(HERE, "data"))
    ap.add_argument("--out", default=os.path.join(HERE, "results2.json"))
    ap.add_argument("--lag", type=int, default=None, help="default: schooling spacing in the panel")
    ap.add_argument("--test-year", type=int, default=2000)
    ap.add_argument("--e8-dir", default=None)
    ap.add_argument("--phl-series", default=None)
    ap.add_argument("--trials", type=int, default=20)
    a = ap.parse_args()

    panel, panel_path, nrows = load_panel(a.data_dir)
    lag = a.lag if a.lag is not None else native_lag(panel)
    res = {"label": "data-level test bench (observational; descriptive OOS prediction only; no causal claims)",
           "provenance": {"panel": os.path.basename(panel_path), "panel_sha256": sha256(panel_path),
                          "n_rows": nrows, "n_countries": len(panel),
                          "schooling_spacing_lag": lag, "test_year": a.test_year,
                          "numpy": np.__version__, "python": sys.version.split()[0]},
           "families": {}, "tierB": {}, "tierC": {}}

    base = build(panel, lag, controls=True)
    r = oos(base, a.test_year)
    signs = []
    for wins in (False, True):
        for ctrl in (True, False):
            for logx in (False, True):
                rr = oos(build(panel, lag, controls=ctrl, logx=logx), a.test_year)
                if rr.get("ok"):
                    signs.append(float(np.sign(rr["beta"])))
    share = float(np.mean([1.0 if s == np.sign(r.get("beta") or 0) else 0.0 for s in signs])) if signs else 0.0
    beats = bool(r.get("ok") and r.get("folds_beat", 0) >= 3
                 and r["model_rmse"] < min(r["persistence_rmse"], r["null_rmse"]))
    ci = r.get("ci") or [0, 0]
    excl = bool(ci[0] > 0 or ci[1] < 0) if r.get("ok") else False
    res["families"]["F9_fertility_lagged_OOS"] = dict(
        r, spec_share=share, n_variants=len(signs), verdict=decide(r, share, beats, excl))
    print("F9", res["families"]["F9_fertility_lagged_OOS"]["verdict"],
          {k: (round(r[k], 4) if isinstance(r.get(k), float) else r.get(k))
           for k in ("n", "n_folds", "model_rmse", "persistence_rmse", "null_rmse", "folds_beat", "beta", "se")},
          "spec_share", round(share, 2))

    # permutation control: permute the outcome within country; a saturated search should not win
    rng = np.random.default_rng(11)
    wins_perm, ran = 0, 0
    for _ in range(a.trials):
        pperm = {}
        for iso, ys in panel.items():
            yrs = sorted(ys)
            # permute the OBSERVED values among the observed years only: the missing-data pattern
            # (pre-1950) stays fixed, so the join keeps its n and the null is a true placebo.
            obs = [y for y in yrs if ys[y].get("tfr_observed_1950plus") is not None]
            vals = rng.permutation([ys[y]["tfr_observed_1950plus"] for y in obs])
            pperm[iso] = {}
            for y in yrs:
                d = dict(ys[y])
                pperm[iso][y] = d
            for y, pv in zip(obs, vals):
                pperm[iso][y]["tfr_observed_1950plus"] = float(pv)
        rr = oos(build(pperm, lag, controls=True), a.test_year, min_train=100, min_test=5)
        if rr.get("ok"):
            ran += 1
            wins_perm += int(rr.get("folds_beat", 0) >= 3)
    share_perm = wins_perm / ran if ran else None
    res["Q1_zero_signal"] = {"trials_run": ran, "complex_selected": wins_perm, "share": share_perm,
                             "pass": bool(share_perm is not None and share_perm <= 0.5),
                             "note": "share of permuted-outcome runs where the model beat both benchmarks "
                                     "in >=3 folds; high share = benchmark too weak or leakage"}
    print("Q1 permutation share", share_perm, "PASS" if res["Q1_zero_signal"]["pass"] else "FAIL")

    d = [v["tfr_observed_1950plus"] - v["effective_fertility"]
         for ys in panel.values() for v in ys.values()
         if v.get("tfr_observed_1950plus") is not None and v.get("effective_fertility") is not None]
    d = np.array(d)
    res["families"]["F10_measurement_construct"] = {
        "n": int(len(d)),
        "median_abs_diff": float(np.median(np.abs(d))) if len(d) else None,
        "mean_diff": float(np.mean(d)) if len(d) else None,
        "note": "TFR and effective fertility are different constructs; a large median gap supports "
                "construct divergence only",
        "verdict": "SUPPORTED_CONSTRUCT_DIVERGENCE" if len(d) and np.median(np.abs(d)) > 0.05 else "REJECTED"}
    print("F10 construct", res["families"]["F10_measurement_construct"])

    if a.e8_dir and os.path.isdir(a.e8_dir):
        files = sorted(os.listdir(a.e8_dir))
        res["tierB"]["E8_fee_dates"] = {
            "dir": os.path.abspath(a.e8_dir), "files": files,
            "sha256": {f: sha256(os.path.join(a.e8_dir, f)) for f in files
                       if os.path.isfile(os.path.join(a.e8_dir, f))},
            "note": "copied from e6e8 / paper-massification records",
            "verdict": "DATA AVAILABLE — gate not yet run (next window)"}
    else:
        res["tierB"]["E8_fee_dates"] = {
            "verdict": "UNTESTABLE on this branch",
            "note": "fee_dates.csv exists on research/e6e8-sequencing-2026-11-25 and "
                    "research/paper-massification-2026-11-25; supply --e8-dir with SHA-256 provenance"}

    res["tierB"]["E8_PHL_gate"] = (
        {"series": os.path.abspath(a.phl_series), "sha256": sha256(a.phl_series),
         "verdict": "SERIES SUPPLIED — gate not yet run (next window)"}
        if a.phl_series and os.path.isfile(a.phl_series)
        else {"verdict": "UNTESTABLE",
              "note": "PHL 2013 K-12 lower-secondary completion series not located in the repo branches searched"})

    res["tierC"] = {
        "F2_supply": "UNTESTABLE (no PTR/teacher/private/finance panel in cached inputs)",
        "F6_growth": "UNTESTABLE (x4 is a wide cross-section; no lagged growth panel with controls)",
        "F7_inequality": "UNTESTABLE (no Gini/SWIID in cache)",
        "F4_gates": "UNTESTABLE (no exam/admission data)",
        "F5_credentials": "UNTESTABLE (no wage/returns panel in cache)",
        "F8_shadow": "UNTESTABLE (literature targets only)",
        "F1_demand": "UNTESTABLE (no micro affordability)",
        "F3_learning": "UNTESTABLE (no learning panels)",
        "shared_code_ablation": "UNTESTABLE in this branch (no equation model code)",
        "multiverse_structural_swap": "UNTESTABLE in this branch (no equation model code)",
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
