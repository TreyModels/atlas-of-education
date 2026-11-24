#!/usr/bin/env python3
"""X4 — honest-split aggregate observed-data staging test (NO simulation).

Implements exactly the pre-registered design in PRE_REGISTRATION_masseng_staging_x2_x4.md:
frozen windows, deterministic ISO3-mod-3 country split, training-only z-scored ordering scores,
OLS model vs persistence and pooled-trend benchmarks, paired country-level losses with a
4,000-draw bootstrap (90 % CIs), and the PASS / FAIL / INSUFFICIENT-EVIDENCE decision rule.

Reads the committed derived panel x4_input/x4_panel.csv (see extract_x4_panel.py and
x4_input/provenance.json). Writes results_x4.json with exclusive creation.
"""
import argparse
import csv
import hashlib
import json
import math
import os
import socket
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LABEL = "AGGREGATE OBSERVED-DATA ANALYSIS — exploratory, not causal, not confirmatory"
BOOT_SEED = 20261125
BOOT_B = 4000


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def load_panel():
    with open(os.path.join(HERE, "x4_input", "x4_panel.csv"), newline="") as f:
        rows = list(csv.DictReader(f))
    def val(r, k):
        v = r[k]
        return float(v) if v not in ("", None) else np.nan
    data = {r["iso3"]: {k: val(r, k) for k in r if k != "iso3"} for r in rows}
    return sorted(data), data


def val(data, iso, key):
    return data[iso][key]


def boot_ci_mean(d, rng, B=BOOT_B, q=0.90):
    d = np.asarray(d, float)
    bs = np.mean(rng.choice(d, size=(B, len(d)), replace=True), axis=1)
    return [float(np.quantile(bs, (1 - q) / 2)), float(np.quantile(bs, 1 - (1 - q) / 2))]


def ols(X, y):
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return coef


def run_spec(isos, data, spec, rng, split):
    """spec: dict with score, edu_years(3), job_years(3), out_years(2), job_series, outcome."""
    edu = [f"edu_{y}" for y in spec["edu_years"]]
    job = [f"{spec['job_series']}_{y}" for y in spec["job_years"]]
    out = [f"{spec['outcome']}_{y}" for y in spec["out_years"]]
    def complete(iso):
        vals = [val(data, iso, k) for k in edu + job + out]
        return all(np.isfinite(v) for v in vals)
    usable = [i for i in isos if complete(i)]
    train = [i for i in usable if not split[i]]
    valid = [i for i in usable if split[i]]
    res = {"spec": spec["name"], "n_complete": len(usable), "n_train": len(train), "n_valid": len(valid)}
    if len(train) < 20 or len(valid) < 10:
        res["status"] = "INSUFFICIENT_EVIDENCE"
        return res
    def vals(iso):
        return ([val(data, iso, k) for k in edu], [val(data, iso, k) for k in job],
                [val(data, iso, k) for k in out])
    # scores (training-only z standardisation)
    raw = {}
    for iso in usable:
        e, j, o = vals(iso)
        if spec["score"] == "order":
            raw[iso] = ((e[1] - e[0]) - (e[2] - e[1])) - ((j[1] - j[0]) - (j[2] - j[1]))
        elif spec["score"] == "net":
            raw[iso] = (e[2] - e[0]) - (j[2] - j[0])
        elif spec["score"] == "net_alt_job":
            raw[iso] = (e[2] - e[0]) - (j[2] - j[0])   # job series already the alt proxy
        else:
            raise ValueError(spec["score"])
    tr = np.array([raw[i] for i in train], float)
    mu, sd = float(tr.mean()), float(tr.std(ddof=0))
    sd = sd if sd > 0 else 1.0
    def z(x):
        return (x - mu) / sd
    Xtr = np.column_stack([np.ones(len(train)), [z(raw[i]) for i in train],
                           [val(data, i, out[1]) for i in train]])
    # outcome = out(t3) - out(t2)
    ytr = np.array([val(data, i, out[1]) - val(data, i, out[0]) for i in train])
    coef = ols(Xtr, ytr)
    Xva = np.column_stack([np.ones(len(valid)), [z(raw[i]) for i in valid],
                           [val(data, i, out[1]) for i in valid]])
    pred = Xva @ coef
    yva = np.array([val(data, i, out[1]) - val(data, i, out[0]) for i in valid])
    persist = np.zeros(len(valid))
    pooled = np.full(len(valid), float(ytr.mean()))
    def losses(p):
        e = np.abs(p - yva)
        return e, float(e.mean()), float(np.sqrt(np.mean(e ** 2)))
    err_m, mae_m, rmse_m = losses(pred)
    err_p, mae_p, rmse_p = losses(persist)
    err_t, mae_t, rmse_t = losses(pooled)
    d_m_p = err_m - err_p
    d_m_t = err_m - err_t
    # bootstrap CI for b1 (training-country resample)
    b1s = []
    for _ in range(BOOT_B):
        pick = rng.integers(0, len(train), size=len(train))
        Xb = Xtr[pick]
        yb = ytr[pick]
        try:
            b1s.append(float(ols(Xb, yb)[1]))
        except Exception:
            pass
    res.update({
        "status": "tested",
        "coef": [float(c) for c in coef],
        "b1": float(coef[1]),
        "b1_ci90_bootstrap": [float(np.quantile(b1s, 0.05)), float(np.quantile(b1s, 0.95))] if b1s else None,
        "mae": {"model": mae_m, "persistence": mae_p, "pooled_trend": mae_t},
        "rmse": {"model": rmse_m, "persistence": rmse_p, "pooled_trend": rmse_t},
        "paired_MAE_model_minus_persistence": {"mean": float(d_m_p.mean()),
                                               "ci90": boot_ci_mean(d_m_p, rng)},
        "paired_MAE_model_minus_pooled_trend": {"mean": float(d_m_t.mean()),
                                                "ci90": boot_ci_mean(d_m_t, rng)},
        "n_pos_persistence": int((d_m_p < 0).sum()), "n_pos_trend": int((d_m_t < 0).sum()),
        "train_outcome_mean": float(ytr.mean()),
        "validation": [{"iso3": i, "score": float(z(raw[i])), "actual": float(yva[k]),
                        "pred_model": float(pred[k]), "pred_persistence": 0.0,
                        "pred_pooled_trend": float(pooled[k])} for k, i in enumerate(valid)],
    })
    lo_p, hi_p = res["paired_MAE_model_minus_persistence"]["ci90"]
    lo_t, hi_t = res["paired_MAE_model_minus_pooled_trend"]["ci90"]
    b1lo, b1hi = res["b1_ci90_bootstrap"] if res["b1_ci90_bootstrap"] else (None, None)
    passes = (hi_p < 0) and (hi_t < 0) and (b1lo is not None and b1lo > 0)
    res["decision"] = "PASS" if passes else "FAIL_NO_EVIDENCE"
    res["decision_parts"] = {"beats_persistence": bool(hi_p < 0), "beats_pooled_trend": bool(hi_t < 0),
                             "b1_positive_ci_excludes_zero": bool(b1lo is not None and b1lo > 0)}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out_path = os.path.abspath(a.out)
    if os.path.exists(out_path):
        raise FileExistsError(out_path)
    t0 = time.time()
    isos, data = load_panel()
    # deterministic split: the national ISO3 codes with any lsc observation (all panel rows, sorted),
    # every third validation. The panel is built from the lsc series' national ISO3 set.
    lsc_isos = sorted(isos)
    split = {iso: (n % 3 == 0) for n, iso in enumerate(lsc_isos)}
    rng = np.random.default_rng(BOOT_SEED)
    specs = [
        {"name": "primary_S_order", "score": "order",
         "edu_years": [1991, 1998, 2004], "job_years": [1991, 1998, 2004],
         "out_years": [2004, 2018], "outcome": "out", "job_series": "job"},
        {"name": "robust_S_net", "score": "net",
         "edu_years": [1991, 1998, 2004], "job_years": [1991, 1998, 2004],
         "out_years": [2004, 2018], "outcome": "out", "job_series": "job"},
        {"name": "robust_windowC", "score": "order",
         "edu_years": [1995, 1998, 2005], "job_years": [1995, 1998, 2005],
         "out_years": [2005, 2019], "outcome": "out", "job_series": "job"},
        {"name": "robust_outcome_sec_ner", "score": "order",
         "edu_years": [1991, 1998, 2004], "job_years": [1991, 1998, 2004],
         "out_years": [2004, 2018], "outcome": "out_alt", "job_series": "job"},
        {"name": "robust_job_emp_agri_neg", "score": "order",
         "edu_years": [1991, 1998, 2004], "job_years": [1991, 1998, 2004],
         "out_years": [2004, 2018], "outcome": "out", "job_series": "job_alt_neg"},
    ]
    # emp_agri: use negative change as structural-transformation expansion -> precomputed in extractor? no:
    # inject a helper series "job_alt_neg_<year>" = -emp_agri_<year> on the fly
    for iso in isos:
        for y in (1991, 1998, 2004):
            data[iso][f"job_alt_neg_{y}"] = -data[iso].get(f"job_alt_{y}", np.nan)
    results = {}
    for spec in specs:
        results[spec["name"]] = run_spec(isos, data, spec, rng, split)
    out = {"label": LABEL, "experiment": "x4", "no_simulation": True,
           "design": {"windows": "train 1991-2004 (midpoint 1998); outcome 2004-2018 for primary",
                      "split": "national ISO3 with any lsc observation sorted; rank%3==0 validation",
                      "bootstrap": {"seed": BOOT_SEED, "draws": BOOT_B, "level": 0.90},
                      "primary_score": "S_order = z(dE_early-dE_late) - z(dJ_early-dJ_late), training-only z",
                      "model": "OLS: d lsc(2004->2018) ~ 1 + S_order + lsc(2004)",
                      "benchmarks": ["persistence (delta=0)", "pooled trend (training mean delta)"],
                      "decision": "PASS iff paired MAE diff vs persistence AND vs pooled trend both <0 with 90% CI upper<0, and b1>0 with 90% CI excluding 0; FAIL/NO_EVIDENCE otherwise; INSUFFICIENT_EVIDENCE if <20 train or <10 validation"},
           "n_national_iso3": len(lsc_isos),
           "split": {"validation": sorted([i for i in split if split[i]]),
                     "training": sorted([i for i in split if not split[i]])},
           "results": results, "elapsed_s": round(time.time() - t0, 3),
           "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
           "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "host": socket.gethostname(), "python": sys.version.split()[0], "numpy": np.__version__,
           "inputs": {"x4_panel.csv": sha(os.path.join(HERE, "x4_input", "x4_panel.csv")),
                      "provenance.json": sha(os.path.join(HERE, "x4_input", "provenance.json")),
                      "run_x4.py": sha(os.path.abspath(__file__))}}
    with open(out_path, "x") as f:
        json.dump(out, f)
    print(json.dumps({"experiment": "x4", "primary": {k: results["primary_S_order"].get(k) for k in
                      ("n_train", "n_valid", "b1", "b1_ci90_bootstrap", "mae",
                       "paired_MAE_model_minus_persistence", "paired_MAE_model_minus_pooled_trend",
                       "decision", "decision_parts", "status")}}, indent=1, default=str))


if __name__ == "__main__":
    main()
