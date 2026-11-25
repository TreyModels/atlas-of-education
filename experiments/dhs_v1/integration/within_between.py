#!/usr/bin/env python3
"""Held-out + within/between extension of the L1→M6 prototype (EXPLORATORY, host-only).

Every L1 cell is a descriptive survey-wave domain mean; every M6 indicator is a PUBLIC
country-year aggregate. The indicator is CONTEXT, NOT AN EXPOSURE: nothing here is a causal
or policy effect, and country-level covariates are not household measurements (ecological
fallacy guard). With four countries the between-country component is a 4-point description,
not an estimate of a population slope (effective N = number of countries).

Outputs (all non-disclosive aggregates):
  within_between_results.csv  -- weighted pooled vs within/between decomposition per series
  heldout_results.csv         -- leave-one-country-out and last-wave holdout RMSE vs baseline
  extension_manifest.json     -- inputs/sha256, method, guardrails
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROTO = ROOT / "integration" / "prototype_l1_m6_final.csv"
OUT = ROOT / "integration"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def wls(y, X, w):
    """Weighted least squares; returns beta and naive (WLS) SEs. X includes intercept."""
    W = np.diag(w)
    XtWX = X.T @ W @ X
    beta = np.linalg.pinv(XtWX) @ (X.T @ W @ y)
    resid = y - X @ beta
    dof = max(int(np.sum(w > 0)) - X.shape[1], 1)
    sigma2 = float((w * resid**2).sum() / dof)
    cov = sigma2 * np.linalg.pinv(XtWX)
    return beta, np.sqrt(np.maximum(np.diag(cov), 0))


def rmse(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float(np.sqrt(np.mean((a - b) ** 2))) if len(a) else float("nan")


def main() -> int:
    d = pd.read_csv(PROTO)
    d = d[(d["lag"] == "same_year") & d["indicator_value"].notna() & d["estimate"].notna()]
    d["w"] = 1.0 / np.maximum(pd.to_numeric(d["se"], errors="coerce").fillna(1.0), 1e-6) ** 2
    rows, hold = [], []
    groups = d.groupby(["experiment", "indicator", "indicator_edu_level"], dropna=False)
    for (exp, ind, edu), g in groups:
        g = g.dropna(subset=["estimate", "indicator_value", "se"])
        # collapse to country-wave-group means is already one row per cell
        if len(g) < 8 or g["country"].nunique() < 3:
            continue
        y = g["estimate"].to_numpy(float); x = g["indicator_value"].to_numpy(float); w = g["w"].to_numpy(float)
        c = g["country"].to_numpy()
        # between/within components (unweighted country means, descriptive)
        xb = pd.Series(x).groupby(c).transform("mean").to_numpy(float)
        yb = pd.Series(y).groupby(c).transform("mean").to_numpy(float)
        try:
            b_pool, se_pool = wls(y, np.column_stack([np.ones_like(x), x]), w)
            b_wb, se_wb = wls(y, np.column_stack([np.ones_like(x), x - xb, xb]), w)
        except np.linalg.LinAlgError:
            continue
        rows.append({
            "experiment": exp, "indicator": ind, "indicator_edu_level": edu,
            "n_obs": int(len(g)), "n_countries": int(g["country"].nunique()),
            "n_waves": int(g.groupby("country")["wave"].nunique().sum()),
            "pooled_beta": float(b_pool[1]), "pooled_se": float(se_pool[1]),
            "within_beta": float(b_wb[1]), "within_se": float(se_wb[1]),
            "between_beta": float(b_wb[2]), "between_se": float(se_wb[2]),
            "context_not_exposure": True, "exploratory": True, "causal_claim": False,
        })
        # leave-one-country-out predictive check (pooled linear context model)
        for ctry in sorted(set(c)):
            tr, te = g["country"] != ctry, g["country"] == ctry
            if tr.sum() < 6 or te.sum() < 1:
                continue
            try:
                b, _ = wls(y[tr], np.column_stack([np.ones(tr.sum()), x[tr]]), w[tr])
            except np.linalg.LinAlgError:
                continue
            pred = b[0] + b[1] * x[te]
            base = np.average(y[tr], weights=w[tr])
            hold.append({"scheme": "leave_one_country_out", "experiment": exp, "indicator": ind,
                         "indicator_edu_level": edu, "held_out": ctry, "n_test": int(te.sum()),
                         "rmse_model": rmse(pred, y[te]), "rmse_baseline": rmse(np.full(te.sum(), base), y[te]),
                         "rmse_baseline_train_mean": rmse(np.full(te.sum(), base), y[te]),
                         "context_not_exposure": True, "causal_claim": False})
        # last-wave holdout per country with >=3 waves
        for ctry, gc in g.groupby("country"):
            waves = sorted(gc["wave"].astype(str).unique())
            if len(waves) < 3:
                continue
            last = waves[-1]
            tr = g["wave"].astype(str) != last
            te = g["wave"].astype(str) == last
            if tr.sum() < 6 or te.sum() < 1:
                continue
            try:
                b, _ = wls(y[tr], np.column_stack([np.ones(tr.sum()), x[tr]]), w[tr])
            except np.linalg.LinAlgError:
                continue
            pred = b[0] + b[1] * x[te]
            base = np.average(y[tr], weights=w[tr])
            hold.append({"scheme": "last_wave_holdout", "experiment": exp, "indicator": ind,
                         "indicator_edu_level": edu, "held_out": f"{ctry}:{last}", "n_test": int(te.sum()),
                         "rmse_model": rmse(pred, y[te]), "rmse_baseline": rmse(np.full(te.sum(), base), y[te]),
                         "context_not_exposure": True, "causal_claim": False})
    wb = pd.DataFrame(rows); ho = pd.DataFrame(hold)
    wb.to_csv(OUT / "within_between_results.csv", index=False)
    ho.to_csv(OUT / "heldout_results.csv", index=False)
    summ = {}
    if len(ho):
        for scheme, g in ho.groupby("scheme"):
            summ[scheme] = {"n_tests": int(len(g)),
                            "median_rmse_model": float(g["rmse_model"].median()),
                            "median_rmse_baseline": float(g["rmse_baseline"].median()),
                            "share_model_better": float((g["rmse_model"] < g["rmse_baseline"]).mean())}
    manifest = {
        "version": "l1-m6-extension-v0.1",
        "inputs": {"prototype": {"path": str(PROTO), "sha256": sha256(PROTO)}},
        "method": {
            "unit": "L1 survey-wave domain-mean cell matched to same-year public DHS-API indicator",
            "models": "inverse-variance WLS: pooled y~x; within-between y ~ (x-country_mean) + country_mean",
            "holdouts": "leave-one-country-out and last-wave holdout; baseline = training weighted mean",
            "effective_n": "number of countries (4) for cross-country statements; cells are not independent",
        },
        "guardrails": {"context_not_exposure": True, "causal_claim": False,
                       "ecological_fallacy": "country-level indicator is not a household measurement",
                       "no_interpolation": True, "descriptive_only": True},
        "counts": {"series": int(len(wb)), "holdout_tests": int(len(ho))},
        "summary": summ,
    }
    (OUT / "extension_manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"[extension] {len(wb)} series, {len(ho)} holdout tests")
    if len(wb):
        print(wb.sort_values("within_beta", key=lambda s: s.abs(), ascending=False)
              .head(10)[["experiment", "indicator", "indicator_edu_level", "n_obs", "n_countries",
                         "pooled_beta", "within_beta", "between_beta"]].to_string(index=False))
    for k, v in summ.items():
        print(k, v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
