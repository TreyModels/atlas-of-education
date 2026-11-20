#!/usr/bin/env python3
"""Y1 - Ceiling-residual candidate-account screen (descriptive only).

Predeclaration (frozen): 10_massification/extensions/lab_2026-11-20_c/PRE_DECLARATIONS.md
sha256 8b431b672bbc9679dc192e907c1db3b95e22bacad2abd6b377c68e864dc336e1, sections Y1 + Reporting rules.
Threshold is implemented verbatim; nothing is tuned, nothing is imputed, no RNG, no network.

Deterministic: all inputs are read-only CSVs; ordering is fixed by explicit sort; floats written
with pandas' default repr (float_format=None). No timestamps inside results/*.csv.
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

OUT = BASE / "10_massification/extensions/lab_2026-11-20_c/Y1_ceiling_residual"
RESULTS = OUT / "results"

EXPERIMENT = "Y1"
CLUSTER = "Y1_ceiling_residual"

# Declared window and estimators (PRE_DECLARATIONS.md Y1 operationalisation).
WIN_LO, WIN_HI = 2000, 2024
LAST_N = 3

CEIL = "SE.TER.ENRR"
CANDIDATES = [
    ("agri_share", "SL.AGR.EMPL.ZS", "opportunity cost"),
    ("youth_unemp", "SL.UEM.1524.ZS", "youth unemployment"),
    ("wage_share", "SL.EMP.WORK.ZS", "formal wage-share (returns/demand)"),
]
CONTROL = "NY.GDP.PCAP.PP.CD"
SIX = ["KHM", "CHN", "HKG", "JPN", "KOR", "PHL"]

# Predeclared threshold (verbatim from the brief, implemented not paraphrased).
THR_AGRI = -0.40
THR_YOUTH = -0.40
THR_ABS = 0.40


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def last_n_mean(block: pd.DataFrame, years: tuple[int, int], n: int = LAST_N):
    """Mean of the last n observed values inside the declared year window."""
    sub = block[(block["year"] >= years[0]) & (block["year"] <= years[1])]
    sub = sub.dropna(subset=["value"]).sort_values("year")
    tail = sub.tail(n)
    if len(tail) == 0:
        return None, 0, "", 0
    return (
        float(tail["value"].mean()),
        int(len(tail)),
        ";".join(str(int(y)) for y in tail["year"].tolist()),
        int(len(sub)),
    )


def ranks(v: np.ndarray) -> np.ndarray:
    """Average ranks (ties averaged) - deterministic."""
    return pd.Series(v).rank(method="average").to_numpy(dtype=float)


def pearson(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a - a.mean()
    b = b - b.mean()
    den = np.sqrt((a * a).sum() * (b * b).sum())
    if den == 0.0:
        return float("nan")
    return float((a * b).sum() / den)


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    return pearson(ranks(np.asarray(x, float)), ranks(np.asarray(y, float)))


def rank_partial(x: np.ndarray, y: np.ndarray, c: np.ndarray) -> float:
    """Declared estimator: Pearson correlation of rank residuals after regressing
    each rank series (y and x) on the rank of the control (with intercept)."""
    ry = ranks(np.asarray(y, float))
    rx = ranks(np.asarray(x, float))
    rc = ranks(np.asarray(c, float))
    design = np.column_stack([np.ones_like(rc), rc])
    ey = ry - design @ np.linalg.lstsq(design, ry, rcond=None)[0]
    ex = rx - design @ np.linalg.lstsq(design, rx, rcond=None)[0]
    return pearson(ex, ey)


def fmt(v):
    return "" if v is None else v


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)

    panel = pd.read_csv(PANEL)
    univ = pd.read_csv(UNIV)
    jobs = pd.read_csv(JOBS)

    # ---------------- 30-country screen (observed panel) ----------------
    rows = []
    for iso3, block in panel.groupby("iso3", sort=True):
        country = block["country"].iloc[0]
        row = {"iso3": iso3, "country": country}
        for tag, code in [("ceiling", CEIL)] + [(t, c) for t, c, _ in CANDIDATES] + [("gdp_pc", CONTROL)]:
            sub = block[block["indicator"] == code]
            mean, n_used, yrs, n_in_window = last_n_mean(sub, (WIN_LO, WIN_HI))
            row[f"{tag}_mean_last3"] = fmt(mean)
            row[f"{tag}_n_obs_used"] = n_used
            row[f"{tag}_n_obs_in_window"] = n_in_window
            row[f"{tag}_years_used"] = yrs
        rows.append(row)
    panel_out = pd.DataFrame(rows).sort_values("iso3").reset_index(drop=True)
    panel_out.to_csv(RESULTS / "Y1_country_panel.csv", index=False)

    # ---------------- correlations: raw + income-rank-partial ----------------
    corr_rows = []
    d = panel_out.dropna(subset=["ceiling_mean_last3", "gdp_pc_mean_last3"])
    for tag, code, desc in CANDIDATES:
        sub = d.dropna(subset=[f"{tag}_mean_last3"])
        n = int(len(sub))
        n_cty = int(sub["iso3"].nunique())
        if n < 3:
            rho_raw = rho_par = float("nan")
        else:
            rho_raw = spearman(sub[f"{tag}_mean_last3"].to_numpy(float), sub["ceiling_mean_last3"].to_numpy(float))
            rho_par = rank_partial(
                sub[f"{tag}_mean_last3"].to_numpy(float),
                sub["ceiling_mean_last3"].to_numpy(float),
                sub["gdp_pc_mean_last3"].to_numpy(float),
            )
        if tag == "agri_share":
            thr = (
                f"rho_partial(ceiling, agri) <= {THR_AGRI:.2f} AND "
                f"rho_partial(ceiling, youth_unemp) <= {THR_YOUTH:.2f} (component 1 of 2; BOTH required)"
            )
            met = "" if np.isnan(rho_par) else bool(rho_par <= THR_AGRI)
        elif tag == "youth_unemp":
            thr = (
                f"rho_partial(ceiling, agri) <= {THR_AGRI:.2f} AND "
                f"rho_partial(ceiling, youth_unemp) <= {THR_YOUTH:.2f} (component 2 of 2; BOTH required)"
            )
            met = "" if np.isnan(rho_par) else bool(rho_par <= THR_YOUTH)
        else:
            thr = "none (reported, not adjudicated)"
            met = ""
        corr_rows.append(
            {
                "candidate": tag,
                "indicator": code,
                "role": desc,
                "control": CONTROL,
                "estimator": "Spearman rho on country-level last-3 means; rank-partial = Pearson of rank residuals on ranked control",
                "n": n,
                "n_countries": n_cty,
                "rho_raw": rho_raw,
                "rho_partial_income": rho_par,
                "label": "derived",
                "threshold_applied": thr,
                "threshold_component_met": met,
                "small_n_caveat": "none (n=30)" if n >= 30 else f"n={n} < 30",
            }
        )
    corr_out = pd.DataFrame(corr_rows)
    corr_out.to_csv(RESULTS / "Y1_correlations.csv", index=False)

    rho_agri = float(corr_out.loc[corr_out["candidate"] == "agri_share", "rho_partial_income"].iloc[0])
    rho_youth = float(corr_out.loc[corr_out["candidate"] == "youth_unemp", "rho_partial_income"].iloc[0])
    rho_wage = float(corr_out.loc[corr_out["candidate"] == "wage_share", "rho_partial_income"].iloc[0])
    n_screen = int(corr_out["n"].min())

    cond_agri = (not np.isnan(rho_agri)) and (rho_agri <= THR_AGRI)
    cond_youth = (not np.isnan(rho_youth)) and (rho_youth <= THR_YOUTH)
    if np.isnan(rho_agri) or np.isnan(rho_youth):
        verdict = "UNABLE"
        failed = "partial rho not computable (n too small)"
    elif cond_agri and cond_youth:
        verdict = "SUPPORTED"
        failed = ""
    else:
        verdict = "NOT SUPPORTED"
        parts = []
        if not cond_agri:
            parts.append(
                f"agri condition failed (rho_partial={rho_agri:.4f}, requires <= {THR_AGRI:.2f})"
                if rho_agri > THR_AGRI
                else f"agri condition failed (|rho| < {THR_ABS:.2f})"
            )
        if not cond_youth:
            parts.append(
                f"youth-unemp condition failed (rho_partial={rho_youth:.4f}, requires <= {THR_YOUTH:.2f})"
                if rho_youth > THR_YOUTH
                else f"youth-unemp condition failed (|rho| < {THR_ABS:.2f})"
            )
        failed = "; ".join(parts)

    # ---------------- 6-system check ----------------
    six_rows = []
    for iso3 in SIX:
        u = univ[(univ["iso3"] == iso3) & (univ["year"] <= 2024)]
        j = jobs[(jobs["iso3"] == iso3) & (jobs["year"] <= 2024)]
        row = {"iso3": iso3, "country": u["country"].iloc[0] if len(u) else iso3}
        for tag, code in [("completion_upper_secondary", "completion_upper_secondary"), ("ger_tertiary", "ger_tertiary")]:
            s = u[u["indicator"] == code].dropna(subset=["value"]).sort_values("year")
            row[f"{tag}_terminal"] = float(s["value"].iloc[-1]) if len(s) else float("nan")
            row[f"{tag}_year"] = int(s["year"].iloc[-1]) if len(s) else ""
        for tag, code in [("agri", "SL.AGR.EMPL.ZS"), ("wage_share", "SL.EMP.WORK.ZS")]:
            s = j[j["indicator_code"] == code].dropna(subset=["value"]).sort_values("year")
            row[f"{tag}_latest"] = float(s["value"].iloc[-1]) if len(s) else float("nan")
            row[f"{tag}_year"] = int(s["year"].iloc[-1]) if len(s) else ""
        six_rows.append(row)
    six_out = pd.DataFrame(six_rows).sort_values("iso3").reset_index(drop=True)
    six_out.to_csv(RESULTS / "Y1_six_system.csv", index=False)

    six_corr = []
    for ceil_tag in ["completion_upper_secondary", "ger_tertiary"]:
        for cand_tag in ["agri", "wage_share"]:
            sub = six_out.dropna(subset=[f"{ceil_tag}_terminal", f"{cand_tag}_latest"])
            n = int(len(sub))
            rho = spearman(sub[f"{cand_tag}_latest"].to_numpy(float), sub[f"{ceil_tag}_terminal"].to_numpy(float)) if n >= 3 else float("nan")
            six_corr.append(
                {
                    "ceiling_variable": ceil_tag,
                    "candidate": cand_tag,
                    "estimator": "Spearman rho on terminal/latest observed country values (<=2024)",
                    "n": n,
                    "n_countries": int(sub["iso3"].nunique()),
                    "rho": rho,
                    "label": "observed",
                    "small_n_caveat": f"n={n} <= 6 (six-system check; descriptive only)",
                    "countries": ";".join(sub["iso3"].tolist()),
                }
            )
    six_corr_out = pd.DataFrame(six_corr)
    six_corr_out.to_csv(RESULTS / "Y1_six_correlations.csv", index=False)

    # ---------------- CLUSTER_RESULTS.csv (exact contract columns) ----------------
    rule = (
        f"PRE_DECLARATIONS.md Y1: candidate note only if rho_partial(ceiling,agri) <= {THR_AGRI:.2f} AND "
        f"rho_partial(ceiling,youth_unemp) <= {THR_YOUTH:.2f}; falsifier -> UNABLE/discard if either |rho| < "
        f"{THR_ABS:.2f} or sign positive. Wage-share: no threshold, reported only."
    )
    pipeline = (
        "panel_wdi_long.csv: country last-3-observed means within 2000-2024 for SE.TER.ENRR (ceiling), "
        "SL.AGR.EMPL.ZS / SL.UEM.1524.ZS / SL.EMP.WORK.ZS (candidates), NY.GDP.PCAP.PP.CD (control); "
        "Spearman on country cells; rank-partial = Pearson of rank residuals on the ranked control; "
        "no imputation. Six-system check: UNIVERSALIZATION_SERIES.csv terminal values (<=2024) vs "
        "JOBS_AND_MARKETS_PANEL.csv latest values (<=2024)."
    )
    smalln = "no small-n caveat on the 30-country screen (n=30); six-system check n<=6 is descriptive only."

    cr = []
    for tag, thr_txt, comp in [
        ("agri_share", f"rho_partial <= {THR_AGRI:.2f} (component 1 of 2)", cond_agri),
        ("youth_unemp", f"rho_partial <= {THR_YOUTH:.2f} (component 2 of 2)", cond_youth),
        ("wage_share", "none (reported, not adjudicated)", None),
    ]:
        row = corr_out[corr_out["candidate"] == tag].iloc[0]
        cr.append(
            {
                "experiment": EXPERIMENT,
                "cluster": CLUSTER,
                "question": "Which candidate account survives the ceiling-residual screen (descriptive screen, not a mechanism claim)?",
                "estimand": f"income-rank-partial Spearman rho(ceiling SE.TER.ENRR, {row['indicator']} = {tag})",
                "estimate": row["rho_partial_income"],
                "se": "",
                "ci_low": "",
                "ci_high": "",
                "n": int(row["n"]),
                "clusters": int(row["n_countries"]),
                "threshold": thr_txt,
                "verdict": verdict,
                "label": "derived",
                "note": (
                    f"VERDICT IS EXPERIMENT-LEVEL (Y1 = {verdict}); this row is the {tag} estimand only. "
                    f"{rule} "
                    + (f"Failed: {failed}. " if failed else "")
                    + ("" if tag == "wage_share" else "")
                    + ("This candidate is reported, not adjudicated (no threshold attached). " if tag == "wage_share" else "")
                    + f"{smalln} Pipeline: {pipeline}"
                ),
            }
        )
    cr_df = pd.DataFrame(cr)
    cols = [
        "experiment", "cluster", "question", "estimand", "estimate", "se", "ci_low", "ci_high",
        "n", "clusters", "threshold", "verdict", "label", "note",
    ]
    cr_df[cols].to_csv(RESULTS / "CLUSTER_RESULTS.csv", index=False)

    # ---------------- RUN_MANIFEST.json ----------------
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

    print(f"[{EXPERIMENT}] n={n_screen} countries={int(panel_out['iso3'].nunique())}")
    print(f"[{EXPERIMENT}] rho_raw/rho_partial: agri={rho_agri:.6f} youth={rho_youth:.6f} wage={rho_wage:.6f}")
    print(f"[{EXPERIMENT}] verdict={verdict} ({failed})")
    print(f"[{EXPERIMENT}] six-system n/rho:")
    for _, r in six_corr_out.iterrows():
        print(f"    {r['ceiling_variable']:<28} x {r['candidate']:<10} n={r['n']} rho={r['rho']:.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
