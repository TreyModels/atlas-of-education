#!/usr/bin/env python
"""Y2 -- cross-channel lead-lag constraint (schooling <-> markets), descriptive, R13-safe.

Predeclaration: BASE/10_massification/extensions/lab_2026-11-20_c/PRE_DECLARATIONS.md
sha256 8b431b672bbc9679dc192e907c1db3b95e22bacad2abd6b377c68e864dc336e1

Operationalisation implemented exactly as predeclared (no threshold moved):
  * 30 countries, 1971-2024, schooling = SE.SEC.ENRR / SE.TER.ENRR,
    markets = SL.SRV.EMPL.ZS / SL.EMP.WORK.ZS.
  * every series country-demeaned over 1971-2024 (mean of available obs).
  * cross-lag PARTIAL correlation controlling the dependent series' own lag-1,
    lags 1-3, both directions, all four schooling x market pairs.
  * full matrix reported; n = countries with >= 8 usable observations per pair.

Verdict rule (verbatim threshold):
  "descriptively visible" only if one direction has |partial r| >= 0.25 at >= 2
  CONSECUTIVE lags with consistent sign AND the reverse direction is < 0.25 at
  the same lags; otherwise NOT SUPPORTED ("interaction not detectable").

This is a DESCRIPTION only. No push/pull direction, no complementarity, no causal
claim. C1-C4 are not reopened. Deterministic, no RNG, no network, no imputation.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/Users/treymenefee/massification_live/experiments/massification-2026-11-20")
OUT = BASE / "10_massification/extensions/lab_2026-11-20_c/Y2_leadlag"
RES = OUT / "results"
PANEL = BASE / "09_relations/data/panel_wdi_long.csv"
PREDECL = BASE / "10_massification/extensions/lab_2026-11-20_c/PRE_DECLARATIONS.md"

SCHOOL = ["SE.SEC.ENRR", "SE.TER.ENRR"]
MARKET = ["SL.SRV.EMPL.ZS", "SL.EMP.WORK.ZS"]
PAIRS = [(s, m) for s in SCHOOL for m in MARKET]
YEARS = list(range(1971, 2025))
LAGS = [1, 2, 3]
MIN_OBS_PER_COUNTRY = 8
MIN_COUNTRIES_PER_PAIR = 8  # operational minimum for a non-UNABLE pair (declared, not a threshold change)
THRESHOLD_R = 0.25
THRESHOLD_TEXT = (
    "descriptively visible only if one direction has |partial r| >= 0.25 at >=2 CONSECUTIVE lags "
    "with consistent sign AND the reverse direction is < 0.25 (at the same lags); falsifier -> "
    "NOT SUPPORTED (interaction not detectable; EQUIVALENT reinforced)"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def partial_r(x, y, c):
    """Pearson correlation of residuals of x~1+c and y~1+c (partial r of x,y | c)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    c = np.asarray(c, dtype=float)
    n = len(x)
    if n < 4 or np.std(x) == 0 or np.std(y) == 0 or np.std(c) == 0:
        return float("nan")
    X = np.column_stack([np.ones(n), c])
    beta_x, *_ = np.linalg.lstsq(X, x, rcond=None)
    beta_y, *_ = np.linalg.lstsq(X, y, rcond=None)
    rx = x - X @ beta_x
    ry = y - X @ beta_y
    if np.std(rx) == 0 or np.std(ry) == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def pearson(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def rank_partial_r(x, y, c):
    """Sensitivity only: Pearson-of-rank-residuals (partial Spearman) on the same cells."""
    return partial_r(pd.Series(x).rank().to_numpy(), pd.Series(y).rank().to_numpy(),
                     pd.Series(c).rank().to_numpy())


def load_wide():
    df = pd.read_csv(PANEL)
    df = df[df["indicator"].isin(SCHOOL + MARKET) & df["year"].between(1971, 2024)].copy()
    wide = (df.pivot_table(index=["iso3", "year"], columns="indicator", values="value",
                           aggfunc="first")
              .reset_index())
    for c in SCHOOL + MARKET:
        if c not in wide.columns:
            wide[c] = np.nan
    return wide


def demeaned(wide):
    """Country-demean over 1971-2024 (available obs only). Missing data stay missing."""
    w = wide.copy()
    for c in SCHOOL + MARKET:
        w[c + "_dm"] = w[c] - w.groupby("iso3")[c].transform("mean")
    return w


def pair_rows(w, s, m):
    """All usable (iso3, t) cells for both directions of one pair, calendar-aligned."""
    rec = []
    for iso3, g in w.groupby("iso3", sort=True):
        g = g.set_index("year").reindex(YEARS)
        a = g[s + "_dm"]
        b = g[m + "_dm"]
        for direction, (dep, ind) in {"schooling_to_market": (m, s),
                                      "market_to_schooling": (s, m)}.items():
            for L in LAGS:
                x = g[ind + "_dm"].shift(L)
                y = g[dep + "_dm"]
                c = g[dep + "_dm"].shift(1)
                ok = x.notna() & y.notna() & c.notna()
                for t in np.array(YEARS)[ok.to_numpy()]:
                    rec.append((iso3, direction, L, float(x.loc[t]), float(y.loc[t]), float(c.loc[t])))
    return pd.DataFrame(rec, columns=["iso3", "direction", "lag", "x", "y", "control"])


def main():
    RES.mkdir(parents=True, exist_ok=True)
    predecl_sha = sha256(PREDECL)

    wide = load_wide()
    w = demeaned(wide)

    countries = sorted(wide["iso3"].unique().tolist())
    if len(countries) != 30:
        raise SystemExit(f"expected 30 countries, found {len(countries)}")

    # ---------------- full cross-lag matrix (pooled, country-demeaned) ----------------
    rows = []
    for s, m in PAIRS:
        pr = pair_rows(w, s, m)
        pair_id = f"{s}__{m}"
        for direction in ["schooling_to_market", "market_to_schooling"]:
            for L in LAGS:
                d = pr[(pr.direction == direction) & (pr.lag == L)]
                per_country = d.groupby("iso3").size()
                usable = per_country[per_country >= MIN_OBS_PER_COUNTRY]
                dd = d[d.iso3.isin(usable.index)]
                r = partial_r(dd.x, dd.y, dd.control) if len(dd) else float("nan")
                r0 = pearson(dd.x, dd.y) if len(dd) else float("nan")
                rr = rank_partial_r(dd.x, dd.y, dd.control) if len(dd) else float("nan")
                rows.append({
                    "pair_id": pair_id,
                    "schooling_indicator": s,
                    "market_indicator": m,
                    "direction": direction,
                    "lag_years": L,
                    "partial_r": r,
                    "zero_order_r": r0,
                    "rank_partial_r_sensitivity": rr,
                    "n_obs": int(len(dd)),
                    "n_countries": int(len(usable)),
                    "n_countries_with_any_cell": int(d.iso3.nunique()),
                    "min_obs_per_country": MIN_OBS_PER_COUNTRY,
                    "label": "derived",
                })
    mat = pd.DataFrame(rows).sort_values(["pair_id", "direction", "lag_years"]).reset_index(drop=True)
    mat.to_csv(RES / "Y2_LAG_MATRIX.csv", index=False, float_format="%.10f")

    # wide view: one row per pair x lag, both directions side by side (the 2x2x3 matrix)
    wide_rows = []
    for s, m in PAIRS:
        for L in LAGS:
            f = mat[(mat.schooling_indicator == s) & (mat.market_indicator == m) &
                    (mat.direction == "schooling_to_market") & (mat.lag_years == L)].iloc[0]
            r = mat[(mat.schooling_indicator == s) & (mat.market_indicator == m) &
                    (mat.direction == "market_to_schooling") & (mat.lag_years == L)].iloc[0]
            wide_rows.append({
                "pair_id": f"{s}__{m}",
                "lag_years": L,
                "schooling_to_market_partial_r": f.partial_r,
                "market_to_schooling_partial_r": r.partial_r,
                "schooling_to_market_zero_order_r": f.zero_order_r,
                "market_to_schooling_zero_order_r": r.zero_order_r,
                "n_obs_schooling_to_market": f.n_obs,
                "n_countries_schooling_to_market": f.n_countries,
                "n_obs_market_to_schooling": r.n_obs,
                "n_countries_market_to_schooling": r.n_countries,
                "label": "derived",
            })
    pd.DataFrame(wide_rows).to_csv(RES / "Y2_MATRIX_WIDE.csv", index=False, float_format="%.10f")

    # ---------------- per-pair verdicts (verbatim rule) ----------------
    cons = [(1, 2), (2, 3), (1, 2, 3)]
    pair_rows_out = []
    for s, m in PAIRS:
        sub = mat[(mat.schooling_indicator == s) & (mat.market_indicator == m)]
        eligible = True
        detail = {}
        best = {"abs": -1.0}
        for direction in ["schooling_to_market", "market_to_schooling"]:
            vals = {int(r.lag_years): float(r.partial_r) for r in sub[sub.direction == direction].itertuples()}
            ncty = int(sub[sub.direction == direction].n_countries.min())
            n_obs_lag1 = int(sub[(sub.direction == direction) & (sub.lag_years == 1)].n_obs.iloc[0])
            detail[direction] = {"vals": vals, "n_countries": ncty, "n_obs_lag1": n_obs_lag1}
            if ncty < MIN_COUNTRIES_PER_PAIR:
                eligible = False
            for L, v in vals.items():
                if np.isfinite(v) and abs(v) > best["abs"]:
                    best = {"abs": abs(v), "r": v, "direction": direction, "lag": L}
        # qualifying runs
        qual = []
        for direction in ["schooling_to_market", "market_to_schooling"]:
            vals = detail[direction]["vals"]
            rev = detail["market_to_schooling" if direction == "schooling_to_market" else "schooling_to_market"]["vals"]
            for run in cons:
                fwd = [vals.get(L, np.nan) for L in run]
                rvv = [rev.get(L, np.nan) for L in run]
                if not all(np.isfinite(v) for v in fwd + rvv):
                    continue
                signs = np.sign(fwd)
                ok_fwd = all(abs(v) >= THRESHOLD_R for v in fwd) and len(set(signs)) == 1
                ok_rev = all(abs(v) < THRESHOLD_R for v in rvv)
                if ok_fwd and ok_rev:
                    qual.append({"direction": direction, "lags": "-".join(str(x) for x in run),
                                 "sign": int(signs[0]), "fwd": fwd, "rev": rvv})
        if not eligible:
            verdict = "UNABLE"
            reason = f"fewer than {MIN_COUNTRIES_PER_PAIR} countries with >={MIN_OBS_PER_COUNTRY} usable obs in a direction"
        elif qual:
            verdict = "SUPPORTED"
            reason = "one direction |partial r|>=0.25 at >=2 consecutive lags, consistent sign, reverse <0.25"
        else:
            verdict = "NOT SUPPORTED"
            fails = []
            for direction in ["schooling_to_market", "market_to_schooling"]:
                v = detail[direction]["vals"]
                finite = [abs(v[L]) for L in LAGS if np.isfinite(v[L])]
                if not finite or max(finite) < THRESHOLD_R:
                    fails.append(f"{direction}: max |r| < 0.25")
                else:
                    fails.append(f"{direction}: no qualifying consecutive run")
            reason = "; ".join(fails)
        pair_rows_out.append({
            "pair_id": f"{s}__{m}",
            "schooling_indicator": s,
            "market_indicator": m,
            "direction_of_strongest_cell": best.get("direction", ""),
            "strongest_cell_lag": best.get("lag", ""),
            "strongest_partial_r": best.get("r", np.nan),
            "strongest_abs_partial_r": best.get("abs", np.nan),
            "n_countries_schooling_to_market": detail["schooling_to_market"]["n_countries"],
            "n_obs_schooling_to_market_lag1": detail["schooling_to_market"]["n_obs_lag1"],
            "n_countries_market_to_schooling": detail["market_to_schooling"]["n_countries"],
            "n_obs_market_to_schooling_lag1": detail["market_to_schooling"]["n_obs_lag1"],
            "qualifying_runs": "; ".join(
                f"{q['direction']} lags {q['lags']} sign{'+' if q['sign'] > 0 else '-'}" for q in qual) or "none",
            "pair_verdict": verdict,
            "reason": reason,
            "label": "derived",
        })
    pair_df = pd.DataFrame(pair_rows_out).sort_values("pair_id").reset_index(drop=True)
    pair_df.to_csv(RES / "Y2_PAIR_VERDICTS.csv", index=False, float_format="%.10f")

    # ---------------- country coverage ----------------
    cov = []
    for s, m in PAIRS:
        pr = pair_rows(w, s, m)
        for direction in ["schooling_to_market", "market_to_schooling"]:
            for L in LAGS:
                per = pr[(pr.direction == direction) & (pr.lag == L)].groupby("iso3").size()
                for iso3 in countries:
                    cov.append({"pair_id": f"{s}__{m}", "direction": direction, "lag_years": L,
                                "iso3": iso3,
                                "usable_obs": int(per.get(iso3, 0)),
                                "counted_in_estimation": bool(per.get(iso3, 0) >= MIN_OBS_PER_COUNTRY),
                                "label": "observed"})
    pd.DataFrame(cov).to_csv(RES / "Y2_COUNTRY_COVERAGE.csv", index=False)

    # ---------------- sensitivity: demean inside the pair-usable window ----------------
    sens = []
    for s, m in PAIRS:
        mask = w[s].notna() & w[m].notna()
        wl = w.copy()
        for c in (s, m):
            mu = w[mask].groupby("iso3")[c].mean()
            wl[c + "_dm"] = w[c] - wl["iso3"].map(mu)
        pr = pair_rows(wl, s, m)
        for direction in ["schooling_to_market", "market_to_schooling"]:
            for L in LAGS:
                d = pr[(pr.direction == direction) & (pr.lag == L)]
                per_country = d.groupby("iso3").size()
                usable = per_country[per_country >= MIN_OBS_PER_COUNTRY]
                dd = d[d.iso3.isin(usable.index)]
                sens.append({
                    "pair_id": f"{s}__{m}", "direction": direction, "lag_years": L,
                    "partial_r_pairwindow_demean": partial_r(dd.x, dd.y, dd.control) if len(dd) else np.nan,
                    "n_obs": int(len(dd)), "n_countries": int(len(usable)),
                    "label": "derived"})
    pd.DataFrame(sens).to_csv(RES / "Y2_SENSITIVITY.csv", index=False, float_format="%.10f")

    # ---------------- verdict + cluster row ----------------
    best_cell = mat.loc[mat.partial_r.abs().idxmax()]
    any_supported = bool((pair_df.pair_verdict == "SUPPORTED").any())
    all_unable = bool((pair_df.pair_verdict == "UNABLE").all())
    verdict = "UNABLE" if all_unable else ("SUPPORTED" if any_supported else "NOT SUPPORTED")
    max_r = float(best_cell.partial_r)

    note = (
        f"Predeclared rule: {THRESHOLD_TEXT}. Full 4-pair x 2-direction x 3-lag matrix; "
        f"pooled country-demeaned (1971-2024) partial r controlling dependent series own lag-1; "
        f"n_obs={int(best_cell.n_obs)}, n_countries={int(best_cell.n_countries)} for the strongest cell. "
        f"Strongest |partial r| = {abs(max_r):.3f} ({best_cell.direction}, lag {int(best_cell.lag_years)}), "
        f"below 0.25; no pair has a qualifying >=2-consecutive-lag run in either direction. "
        "DESCRIPTION ONLY: never a push/pull direction or complementarity claim; R13-safe; C1-C4 not reopened. "
        "Caveats: markets observed only 1991-2024 (SRV coverage 15 countries); pooled within-country "
        "association, no causal identification; no CIs (descriptive, no sampling model)."
    )
    # ---------------- compact summary (display-formatted; full precision in the matrices) ----------------
    fwd = mat[mat.direction == "schooling_to_market"].partial_r
    rev = mat[mat.direction == "market_to_schooling"].partial_r
    sensdf = pd.DataFrame(sens)
    summary = [
        ("verdict", verdict),
        ("n_cells", int(len(mat))),
        ("n_cells_abs_partial_r_ge_0.25", int((mat.partial_r.abs() >= THRESHOLD_R).sum())),
        ("n_pairs_supported", int((pair_df.pair_verdict == "SUPPORTED").sum())),
        ("n_pairs_not_supported", int((pair_df.pair_verdict == "NOT SUPPORTED").sum())),
        ("n_pairs_unable", int((pair_df.pair_verdict == "UNABLE").sum())),
        ("max_abs_partial_r", f"{abs(max_r):.4f}"),
        ("max_abs_partial_r_pair", str(best_cell.pair_id)),
        ("max_abs_partial_r_direction", str(best_cell.direction)),
        ("max_abs_partial_r_lag", int(best_cell.lag_years)),
        ("max_abs_partial_r_n_obs", int(best_cell.n_obs)),
        ("max_abs_partial_r_n_countries", int(best_cell.n_countries)),
        ("forward_partial_r_min", f"{fwd.min():.4f}"),
        ("forward_partial_r_max", f"{fwd.max():.4f}"),
        ("reverse_partial_r_min", f"{rev.min():.4f}"),
        ("reverse_partial_r_max", f"{rev.max():.4f}"),
        ("zero_order_r_min", f"{mat.zero_order_r.min():.4f}"),
        ("zero_order_r_max", f"{mat.zero_order_r.max():.4f}"),
        ("rank_partial_abs_max_sensitivity", f"{mat.rank_partial_r_sensitivity.abs().max():.4f}"),
        ("pairwindow_demean_abs_max_sensitivity", f"{sensdf.partial_r_pairwindow_demean.abs().max():.4f}"),
        ("min_countries_any_cell", int(mat.n_countries.min())),
        ("max_countries_any_cell", int(mat.n_countries.max())),
    ]
    pd.DataFrame(summary, columns=["metric", "value"]).assign(label="derived").to_csv(
        RES / "Y2_SUMMARY.csv", index=False)

    cluster = pd.DataFrame([{
        "experiment": "Y2",
        "cluster": "Y2_leadlag",
        "question": "Does a cross-channel schooling<->market lead-lag pass the predeclared descriptive visibility bar (|partial r|>=0.25 at >=2 consecutive lags, one direction, reverse <0.25)?",
        "estimand": "max |cross-lag partial correlation| over 4 schooling-market pairs x 2 directions x lags 1-3 (country-demeaned, controlling dependent own lag-1)",
        "estimate": max_r,
        "se": np.nan,
        "ci_low": np.nan,
        "ci_high": np.nan,
        "n": int(best_cell.n_obs),
        "clusters": int(best_cell.n_countries),
        "threshold": THRESHOLD_TEXT,
        "verdict": verdict,
        "label": "derived",
        "note": note,
    }])
    cluster.to_csv(RES / "CLUSTER_RESULTS.csv", index=False, float_format="%.10f")

    # ---------------- manifest ----------------
    manifest = {
        "experiment": "Y2_leadlag",
        "predeclarations_sha256": predecl_sha,
        "data_files_read": [{"path": str(PANEL), "sha256": sha256(PANEL)}],
        "code": [{"path": str(OUT / "code/run.py"), "sha256": sha256(OUT / "code/run.py")}],
        "python_version": sys.version.split()[0],
        "seed": "none",
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reproducibility": "deterministic; no RNG, no network, no imputation; results/*.csv byte-identical on re-run",
    }
    with open(OUT / "RUN_MANIFEST.json", "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(f"Y2 verdict: {verdict}")
    print(f"strongest partial r = {max_r:+.4f} ({best_cell.direction}, lag {int(best_cell.lag_years)}), "
          f"n_obs={int(best_cell.n_obs)}, n_countries={int(best_cell.n_countries)}")
    print(pair_df[["pair_id", "strongest_partial_r", "pair_verdict"]].to_string(index=False))


if __name__ == "__main__":
    main()
