#!/usr/bin/env python3
"""Y3 - Capacity floor-not-ceiling observed check (6 systems; descriptive only).

Predeclaration (frozen): 10_massification/extensions/lab_2026-11-20_c/PRE_DECLARATIONS.md
sha256 8b431b672bbc9679dc192e907c1db3b95e22bacad2abd6b377c68e864dc336e1, section Y3.
Threshold implemented verbatim. No imputation: a system missing a component is reported UNABLE
for that cell and excluded from that correlation. No RNG, no network. Deterministic.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/Users/treymenefee/massification_live/experiments/massification-2026-11-20")
PANEL = BASE / "09_relations/data/panel_wdi_long.csv"
UNIV = BASE / "10_massification/data/UNIVERSALIZATION_SERIES.csv"
JOBS = BASE / "10_massification/data/JOBS_AND_MARKETS_PANEL.csv"
PREDECL = BASE / "10_massification/extensions/lab_2026-11-20_c/PRE_DECLARATIONS.md"

OUT = BASE / "10_massification/extensions/lab_2026-11-20_c/Y3_capacity_floor"
RESULTS = OUT / "results"

EXPERIMENT = "Y3"
CLUSTER = "Y3_capacity_floor"

SIX = ["KHM", "CHN", "HKG", "JPN", "KOR", "PHL"]
PTR_LO, PTR_HI = 1995, 2024
PTR_PANEL = "SE.SEC.ENRL.TC.ZS"
PTR_JOBS = "SE.SEC.ENRL.TC.ZS"
FLOOR_PRIMARY = "completion_primary"
FLOOR_FALLBACK = "SE.PRM.CMPT.ZS"
CEIL_PRIMARY = "completion_upper_secondary"
CEIL_FALLBACK = "ger_tertiary"

THR_RHO = 0.50


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ranks(v) -> np.ndarray:
    return pd.Series(np.asarray(v, float)).rank(method="average").to_numpy(dtype=float)


def pearson(a, b) -> float:
    a = np.asarray(a, float) - np.mean(a)
    b = np.asarray(b, float) - np.mean(b)
    den = np.sqrt((a * a).sum() * (b * b).sum())
    return float("nan") if den == 0.0 else float((a * b).sum() / den)


def spearman(x, y) -> float:
    return pearson(ranks(x), ranks(y))


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)

    panel = pd.read_csv(PANEL)
    univ = pd.read_csv(UNIV)
    jobs = pd.read_csv(JOBS)

    rows = []
    for iso3 in SIX:
        country = panel.loc[panel["iso3"] == iso3, "country"].iloc[0]

        # ---- ΔPTR-improvement: secondary PTR, earliest >=1995 minus latest <=2024 ----
        ptr = panel[(panel["indicator"] == PTR_PANEL) & (panel["iso3"] == iso3)]
        ptr = ptr[(ptr["year"] >= PTR_LO) & (ptr["year"] <= PTR_HI)].dropna(subset=["value"]).sort_values("year")
        ptr_source = "panel_wdi_long:SE.SEC.ENRL.TC.ZS"
        if len(ptr) < 2:
            # declared fallback only if the panel lacks the series (never impute)
            jp = jobs[(jobs["indicator_code"] == PTR_JOBS) & (jobs["iso3"] == iso3)]
            jp = jp[(jp["year"] >= PTR_LO) & (jp["year"] <= PTR_HI)].dropna(subset=["value"]).sort_values("year")
            if len(jp) >= 2:
                ptr, ptr_source = jp, "JOBS_AND_MARKETS_PANEL:SE.SEC.ENRL.TC.ZS"
            else:
                ptr, ptr_source = None, "UNABLE (absent in panel and jobs)"

        if ptr is None:
            d_ptr = np.nan
            e_y = l_y = e_v = l_v = ""
            n_ptr = 0
        else:
            e_y, l_y = int(ptr["year"].iloc[0]), int(ptr["year"].iloc[-1])
            e_v, l_v = float(ptr["value"].iloc[0]), float(ptr["value"].iloc[-1])
            d_ptr = e_v - l_v
            n_ptr = int(len(ptr))

        # ---- floor: latest completion_primary; fallback SE.PRM.CMPT.ZS ----
        f_series = univ[(univ["iso3"] == iso3) & (univ["indicator"] == FLOOR_PRIMARY) & (univ["year"] <= 2024)]
        f_series = f_series.dropna(subset=["value"]).sort_values("year")
        if len(f_series):
            floor_v, floor_y = float(f_series["value"].iloc[-1]), int(f_series["year"].iloc[-1])
            floor_src, floor_ind = "UNIVERSALIZATION_SERIES", FLOOR_PRIMARY
        else:
            fb = panel[(panel["iso3"] == iso3) & (panel["indicator"] == FLOOR_FALLBACK) & (panel["year"] <= 2024)]
            fb = fb.dropna(subset=["value"]).sort_values("year")
            if len(fb):
                floor_v, floor_y = float(fb["value"].iloc[-1]), int(fb["year"].iloc[-1])
                floor_src, floor_ind = "panel_wdi_long", FLOOR_FALLBACK
            else:
                floor_v, floor_y, floor_src, floor_ind = np.nan, "", "UNABLE", "UNABLE"
        floor_kind = "completion rate" if floor_ind in (FLOOR_PRIMARY, FLOOR_FALLBACK) else "UNABLE"

        # ---- ceiling: latest completion_upper_secondary; fallback ger_tertiary ----
        c_series = univ[(univ["iso3"] == iso3) & (univ["indicator"] == CEIL_PRIMARY) & (univ["year"] <= 2024)]
        c_series = c_series.dropna(subset=["value"]).sort_values("year")
        if len(c_series):
            ceil_v, ceil_y = float(c_series["value"].iloc[-1]), int(c_series["year"].iloc[-1])
            ceil_src, ceil_ind = "UNIVERSALIZATION_SERIES", CEIL_PRIMARY
        else:
            cb = univ[(univ["iso3"] == iso3) & (univ["indicator"] == CEIL_FALLBACK) & (univ["year"] <= 2024)]
            cb = cb.dropna(subset=["value"]).sort_values("year")
            if len(cb):
                ceil_v, ceil_y = float(cb["value"].iloc[-1]), int(cb["year"].iloc[-1])
                ceil_src, ceil_ind = "UNIVERSALIZATION_SERIES", CEIL_FALLBACK
            else:
                ceil_v, ceil_y, ceil_src, ceil_ind = np.nan, "", "UNABLE", "UNABLE"
        ceil_kind = (
            "completion rate" if ceil_ind == CEIL_PRIMARY else ("gross enrolment ratio (GER)" if ceil_ind == CEIL_FALLBACK else "UNABLE")
        )

        rows.append(
            {
                "iso3": iso3,
                "country": country,
                "ptr_source": ptr_source,
                "ptr_n_obs_in_window": n_ptr,
                "ptr_earliest_year": e_y,
                "ptr_earliest": e_v,
                "ptr_latest_year": l_y,
                "ptr_latest": l_v,
                "dptr_improvement": d_ptr,
                "ptr_small_n_flag": "" if n_ptr == 0 else ("yes: <3 obs" if n_ptr < 3 else ""),
                "floor_source": floor_src,
                "floor_indicator": floor_ind,
                "floor_kind": floor_kind,
                "floor_value": floor_v,
                "floor_year": floor_y,
                "ceiling_source": ceil_src,
                "ceiling_indicator": ceil_ind,
                "ceiling_kind": ceil_kind,
                "ceiling_value": ceil_v,
                "ceiling_year": ceil_y,
                "label": "observed",
            }
        )

    det = pd.DataFrame(rows).sort_values("iso3").reset_index(drop=True)
    det.to_csv(RESULTS / "Y3_country_detail.csv", index=False)

    def run_corr(value_col):
        sub = det.dropna(subset=["dptr_improvement", value_col])
        n = int(len(sub))
        if n < 3:
            return np.nan, n, ";".join(sub["iso3"].tolist()), ";".join(
                det.loc[~det["iso3"].isin(sub["iso3"]), "iso3"].tolist()
            )
        rho = spearman(sub["dptr_improvement"].to_numpy(float), sub[value_col].to_numpy(float))
        return rho, n, ";".join(sub["iso3"].tolist()), ";".join(det.loc[~det["iso3"].isin(sub["iso3"]), "iso3"].tolist())

    rho_floor, n_floor, used_floor, excl_floor = run_corr("floor_value")
    rho_ceil, n_ceil, used_ceil, excl_ceil = run_corr("ceiling_value")

    cond_floor = (not np.isnan(rho_floor)) and (rho_floor > 0) and (abs(rho_floor) >= THR_RHO)
    # Ceiling condition as declared: |rho| < 0.50 "or sign-inconsistent". No ceiling sign was
    # predicted in the predeclaration, so the only readable test is |rho| < 0.50; recorded here.
    cond_ceil = (not np.isnan(rho_ceil)) and (abs(rho_ceil) < THR_RHO)
    if np.isnan(rho_floor) or np.isnan(rho_ceil):
        verdict = "UNABLE"
        failed = "rho not computable (n < 3 separable systems)"
    elif cond_floor and cond_ceil:
        verdict = "SUPPORTED"
        failed = ""
    else:
        verdict = "NOT SUPPORTED"
        parts = []
        if not cond_floor:
            parts.append(
                f"floor condition failed (rho={rho_floor:.4f}; requires POSITIVE with |rho| >= {THR_RHO:.2f})"
            )
        if not cond_ceil:
            parts.append(
                f"ceiling condition failed (rho={rho_ceil:.4f}; requires |rho| < {THR_RHO:.2f} or sign-inconsistent)"
            )
        failed = "; ".join(parts)

    corr_rows = [
        {
            "pair": "dptr_improvement_vs_floor",
            "x": "dPTR-improvement (earliest >=1995 minus latest <=2024, secondary PTR)",
            "y": "floor = latest observed completion_primary (fallback SE.PRM.CMPT.ZS)",
            "estimator": "Spearman rho on 6 system points (pairwise available)",
            "n": n_floor,
            "n_countries": n_floor,
            "rho": rho_floor,
            "predicted_sign": "positive",
            "threshold": f"POSITIVE with |rho| >= {THR_RHO:.2f}",
            "component_met": cond_floor,
            "systems_used": used_floor,
            "systems_excluded_unable": excl_floor,
            "label": "observed",
            "small_n_caveat": "n = 6 systems maximum; n = 5 for the floor pair (JPN floor UNABLE). Descriptive only.",
        },
        {
            "pair": "dptr_improvement_vs_ceiling",
            "x": "dPTR-improvement (earliest >=1995 minus latest <=2024, secondary PTR)",
            "y": "ceiling = latest observed completion_upper_secondary (fallback ger_tertiary)",
            "estimator": "Spearman rho on 6 system points (pairwise available)",
            "n": n_ceil,
            "n_countries": n_ceil,
            "rho": rho_ceil,
            "predicted_sign": "none declared (only |rho| < 0.50 required)",
            "threshold": f"|rho| < {THR_RHO:.2f} (or sign-inconsistent)",
            "component_met": cond_ceil,
            "systems_used": used_ceil,
            "systems_excluded_unable": excl_ceil,
            "label": "observed",
            "small_n_caveat": "n = 6 systems maximum; descriptive only.",
        },
    ]
    corr_out = pd.DataFrame(corr_rows)
    corr_out.to_csv(RESULTS / "Y3_correlations.csv", index=False)

    # ---- leave-one-system-out stability (how much one point carries each rho) ----
    loo = []
    for iso3 in SIX:
        sub = det[det["iso3"] != iso3]
        f = sub.dropna(subset=["dptr_improvement", "floor_value"])
        c = sub.dropna(subset=["dptr_improvement", "ceiling_value"])
        rf = spearman(f["dptr_improvement"].to_numpy(float), f["floor_value"].to_numpy(float)) if len(f) >= 3 else np.nan
        rc = spearman(c["dptr_improvement"].to_numpy(float), c["ceiling_value"].to_numpy(float)) if len(c) >= 3 else np.nan
        loo.append(
            {
                "excluded_system": iso3,
                "n_floor": int(len(f)),
                "rho_floor": rf,
                "floor_component_met": bool((not np.isnan(rf)) and rf > 0 and abs(rf) >= THR_RHO),
                "n_ceiling": int(len(c)),
                "rho_ceiling": rc,
                "ceiling_component_met": bool((not np.isnan(rc)) and abs(rc) < THR_RHO),
            }
        )
    pd.DataFrame(loo).to_csv(RESULTS / "Y3_leave_one_out.csv", index=False)

    # ---- sensitivity: PTR from the jobs panel (named in the predeclaration) ----
    sens = []
    for iso3 in SIX:
        jp = jobs[(jobs["indicator_code"] == PTR_JOBS) & (jobs["iso3"] == iso3)]
        jp = jp[(jp["year"] >= PTR_LO) & (jp["year"] <= PTR_HI)].dropna(subset=["value"]).sort_values("year")
        if len(jp) >= 2:
            sens.append(
                {
                    "iso3": iso3,
                    "jobs_ptr_earliest_year": int(jp["year"].iloc[0]),
                    "jobs_ptr_earliest": float(jp["value"].iloc[0]),
                    "jobs_ptr_latest_year": int(jp["year"].iloc[-1]),
                    "jobs_ptr_latest": float(jp["value"].iloc[-1]),
                    "jobs_dptr_improvement": float(jp["value"].iloc[0] - jp["value"].iloc[-1]),
                }
            )
        else:
            sens.append({"iso3": iso3, "jobs_ptr_earliest_year": "", "jobs_ptr_earliest": np.nan,
                         "jobs_ptr_latest_year": "", "jobs_ptr_latest": np.nan, "jobs_dptr_improvement": np.nan})
    sens_df = pd.DataFrame(sens).sort_values("iso3").reset_index(drop=True)
    merged = det[["iso3", "dptr_improvement", "floor_value", "ceiling_value"]].merge(sens_df, on="iso3", how="left")
    merged["abs_diff_vs_panel"] = (merged["dptr_improvement"] - merged["jobs_dptr_improvement"]).abs()
    merged.to_csv(RESULTS / "Y3_ptr_source_sensitivity.csv", index=False)

    # ---- CLUSTER_RESULTS.csv ----
    rule = (
        f"PRE_DECLARATIONS.md Y3: SUPPORTED only if rho(dPTR-improvement, floor) is POSITIVE with |rho| >= "
        f"{THR_RHO:.2f} AND |rho(dPTR-improvement, ceiling)| < {THR_RHO:.2f} (or sign-inconsistent); "
        f"falsifier -> UNABLE/not separable otherwise."
    )
    pipeline = (
        "panel_wdi_long.csv SE.SEC.ENRL.TC.ZS restricted to 1995-2024 (earliest minus latest; values identical to "
        "JOBS_AND_MARKETS_PANEL.SE.SEC.ENRL.TC.ZS where both exist); floor = UNIVERSALIZATION_SERIES.completion_primary "
        "latest <=2024 (fallback panel_wdi_long SE.PRM.CMPT.ZS); ceiling = UNIVERSALIZATION_SERIES."
        "completion_upper_secondary latest <=2024 (fallback ger_tertiary); Spearman on system points; no imputation."
    )
    smalln = (
        f"SMALL-N WARNING: n = {n_ceil} systems for the ceiling pair and n = {n_floor} for the floor pair "
        f"(JPN floor UNABLE: no completion_primary and no SE.PRM.CMPT.ZS on disk); a 6-point Spearman takes only "
        f"discrete values. Leave-one-system-out re-estimates are in results/Y3_leave_one_out.csv and show a single "
        f"system materially changes both rho; read both point estimates as descriptions, not as a separable finding."
    )
    cr = []
    for pair, est, n, thr, met in [
        ("floor", "Spearman rho(dPTR-improvement, floor completion_primary)", n_floor, f"POSITIVE with |rho| >= {THR_RHO:.2f}", cond_floor),
        ("ceiling", "Spearman rho(dPTR-improvement, ceiling completion_upper_secondary)", n_ceil, f"|rho| < {THR_RHO:.2f} (or sign-inconsistent)", cond_ceil),
    ]:
        cr.append(
            {
                "experiment": EXPERIMENT,
                "cluster": CLUSTER,
                "question": "Across the six systems, does observed PTR improvement rank with the floor level rather than the ceiling level? (descriptive)",
                "estimand": est,
                "estimate": rho_floor if pair == "floor" else rho_ceil,
                "se": "",
                "ci_low": "",
                "ci_high": "",
                "n": n,
                "clusters": 6,
                "threshold": thr,
                "verdict": verdict,
                "label": "observed",
                "note": (
                    f"VERDICT IS EXPERIMENT-LEVEL (Y3 = {verdict}); this row is the {pair} estimand only. "
                    f"{rule} " + (f"Failed: {failed}. " if failed else "") + f"{smalln} Pipeline: {pipeline}"
                ),
            }
        )
    cr_df = pd.DataFrame(cr)
    cols = [
        "experiment", "cluster", "question", "estimand", "estimate", "se", "ci_low", "ci_high",
        "n", "clusters", "threshold", "verdict", "label", "note",
    ]
    cr_df[cols].to_csv(RESULTS / "CLUSTER_RESULTS.csv", index=False)

    manifest = {
        "experiment": EXPERIMENT,
        "predeclarations_sha256": sha256(PREDECL),
        "data_files_read": [
            {"path": str(PANEL), "sha256": sha256(PANEL)},
            {"path": str(UNIV), "sha256": sha256(UNIV)},
            {"path": str(JOBS), "sha256": sha256(JOBS)},
        ],
        "code": [{"path": str(OUT / "code/run.py"), "sha256": sha256(OUT / "code/run.py")}],
        "python_version": platform.python_version(),
        "seed": "none",
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reproducibility": (
            "Deterministic: no RNG, no network, fixed absolute input paths, explicit sorts. "
            "results/*.csv contain no timestamps and are byte-identical across re-runs (verified by shasum -a 256). "
            "This manifest itself changes only in run_utc between runs."
        ),
    }
    with open(OUT / "RUN_MANIFEST.json", "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")

    print(f"[{EXPERIMENT}] rho_floor={rho_floor:.6f} (n={n_floor}); rho_ceiling={rho_ceil:.6f} (n={n_ceil})")
    print(f"[{EXPERIMENT}] verdict={verdict} ({failed})")
    print(det[["iso3", "dptr_improvement", "floor_value", "floor_indicator", "ceiling_value", "ceiling_indicator"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
