#!/usr/bin/env python
"""Y4 -- world-society rival false-positive check (descriptive null model).

Predeclaration: BASE/10_massification/extensions/lab_2026-11-20_c/PRE_DECLARATIONS.md
sha256 8b431b672bbc9679dc192e907c1db3b95e22bacad2abd6b377c68e864dc336e1

Operationalisation implemented exactly as predeclared (no threshold moved):
  * null = "each level crosses its 90% threshold at the cross-system MEDIAN crossing
    year for that level", from band midpoints of DATED NON-CENSORED crossings only;
    censored rows are excluded from the median and listed with their exclusion reason.
  * "never crossed" = the observed record shows no >=90 crossing: observed final
    value < 90 AND no dated crossing row, or the 90% timing row is right-censored /
    absent (per-row rule recorded in the audit).
  * score = systems where the null implies a >=90 crossing but the observed record
    shows none.

Verdict rule (verbatim threshold): the rival is DISTINGUISHED on the upper-secondary
margin only if the null generates an upper-secondary >=90 crossing for >= 1 system
that never crossed; otherwise NOT DISTINGUISHED.

Descriptive null-model scoring only. No direction claim, no C1-C4 reopening.
Deterministic, no RNG, no network, no imputation.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/Users/treymenefee/massification_live/experiments/massification-2026-11-20")
OUT = BASE / "10_massification/extensions/lab_2026-11-20_c/Y4_worldsociety"
RES = OUT / "results"
TIMING = BASE / "10_massification/data/UNIVERSALIZATION_TIMING.csv"
SERIES = BASE / "10_massification/data/UNIVERSALIZATION_SERIES.csv"
PREDECL = BASE / "10_massification/extensions/lab_2026-11-20_c/PRE_DECLARATIONS.md"

LEVEL_ORDER = ["primary", "lower secondary", "secondary", "upper secondary", "tertiary"]
# observed series used to read each level's final value (the measure carried by every
# 90% timing row at that level is the gross enrolment ratio, GER)
OBS_SERIES = {
    "primary": "ger_primary",
    "lower secondary": "ger_lower_secondary",
    "secondary": "ger_secondary",
    "upper secondary": "ger_upper_secondary",
    "tertiary": "ger_tertiary",
}
COMPLETION_SERIES = {
    "primary": "completion_primary",
    "lower secondary": "completion_lower_secondary",
    "upper secondary": "completion_upper_secondary",
}
THRESHOLD_TEXT = (
    "the rival is DISTINGUISHED on the upper-secondary margin only if the null generates an "
    "upper-secondary >=90 crossing for >=1 system that never crossed; falsifier -> NOT DISTINGUISHED"
)
MIN_FP = 1  # predeclared: >= 1 system


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_timing():
    t = pd.read_csv(TIMING, dtype={"crossing_year": str, "censoring": str})
    t["cross_num"] = pd.to_numeric(t["crossing_year"], errors="coerce")
    both = t["band_earliest"].notna() & t["band_latest"].notna()
    t["band_midpoint"] = np.where(both, (t["band_earliest"] + t["band_latest"]) / 2.0, t["cross_num"])
    return t


def span_midpoint(row):
    """Band midpoint; fall back to the crossing year when a band bound is missing."""
    if pd.notna(row["band_earliest"]) and pd.notna(row["band_latest"]):
        return (float(row["band_earliest"]) + float(row["band_latest"])) / 2.0
    if pd.notna(row["cross_num"]):
        return float(row["cross_num"])
    return float("nan")


def load_series():
    s = pd.read_csv(SERIES)
    s = s[s["value"].notna()].sort_values(["iso3", "indicator", "year"])
    g = s.groupby(["iso3", "indicator"]).agg(
        final_value=("value", "last"),
        final_year=("year", "max"),
        first_year=("year", "min"),
        n_obs=("value", "count"),
    ).reset_index()
    return g


def main():
    RES.mkdir(parents=True, exist_ok=True)
    predecl_sha = sha256(PREDECL)

    t = load_timing()
    gser = load_series()
    countries = (t[["iso3", "country"]].drop_duplicates()
                 .sort_values("iso3").reset_index(drop=True))
    if len(countries) != 6:
        raise SystemExit(f"expected 6 systems in timing file, found {len(countries)}")

    rows90 = t[t["threshold_pct"] == 90].copy().sort_values(["level", "iso3", "measure"])

    # ---------------- median inputs: every 90% row, included or excluded ----------------
    mi = []
    for r in rows90.itertuples(index=False):
        censored = r.censoring in ("left", "right")
        dated = pd.notna(r.cross_num)
        if censored:
            included, reason = False, f"{r.censoring}_censored_excluded (bound only, no band midpoint)"
        elif not dated:
            included, reason = False, "no_crossing_year (status unable/absent)"
        elif pd.notna(r.band_earliest) and pd.notna(r.band_latest):
            included, reason = True, "included: band midpoint"
        else:
            included, reason = True, "included: band bound missing, crossing year used"
        mi.append({
            "country": r.country,
            "iso3": r.iso3,
            "level": r.level,
            "threshold_pct": int(r.threshold_pct),
            "measure": r.measure,
            "crossing_year": r.crossing_year if pd.notna(r.crossing_year) else "",
            "band_earliest": r.band_earliest,
            "band_latest": r.band_latest,
            "censoring": r.censoring if pd.notna(r.censoring) else "",
            "status": r.status,
            "midpoint": span_midpoint(pd.Series(r._asdict())) if included else np.nan,
            "included_in_median": bool(included),
            "exclusion_reason": reason,
        })
    midf = pd.DataFrame(mi).sort_values(["level", "iso3", "measure"]).reset_index(drop=True)
    midf.to_csv(RES / "Y4_MEDIAN_INPUTS.csv", index=False, float_format="%.10f")

    # ---------------- per-level medians (primary + sensitivity) ----------------
    level_rows = []
    for level in LEVEL_ORDER:
        sub = midf[midf.level == level]
        inc = sub[sub.included_in_median]
        n_dated_rows = int(len(inc))
        n_dated_systems = int(inc.iso3.nunique())
        # system-collapsed: one midpoint per system (median across that system's dated rows)
        if n_dated_rows:
            sys_vals = inc.groupby("iso3").midpoint.median()
            med_sys = float(sys_vals.median())
            med_all = float(inc.midpoint.median())
        else:
            sys_vals = pd.Series(dtype=float)
            med_sys = med_all = float("nan")
        # sensitivity: include dated LEFT-censored rows (crossing year as an upper bound)
        left = sub[(sub.censoring == "left") & (sub.crossing_year != "")]
        sens_vals = pd.concat([inc[["iso3", "midpoint"]],
                               left.assign(midpoint=pd.to_numeric(left.crossing_year, errors="coerce"))
                              [["iso3", "midpoint"]]])
        sens_vals = sens_vals.dropna(subset=["midpoint"])
        med_sens = float(sens_vals.groupby("iso3").midpoint.median().median()) if len(sens_vals) else float("nan")
        censored = sub[~sub.included_in_median]
        level_rows.append({
            "level": level,
            "n_90_rows_total": int(len(sub)),
            "n_dated_non_censored_rows": n_dated_rows,
            "n_systems_dated_non_censored": n_dated_systems,
            "median_year_system_collapsed": med_sys,
            "median_year_all_rows": med_all,
            "median_year_incl_left_censored_sensitivity": med_sens,
            "n_censored_rows_excluded": int(len(censored)),
            "censored_rows_listed": "; ".join(sorted(
                f"{r.iso3}:{r.measure}:{r.crossing_year}({r.censoring})" for r in censored.itertuples())),
            "null_defined": bool(np.isfinite(med_sys)),
            "label": "derived",
        })
    lev = pd.DataFrame(level_rows)
    lev.to_csv(RES / "Y4_LEVEL_SUMMARY.csv", index=False, float_format="%.10f")

    # ---------------- full audit: every country x level ----------------
    audit = []
    for level in LEVEL_ORDER:
        med = float(lev.loc[lev.level == level, "median_year_system_collapsed"].iloc[0])
        null_defined = bool(np.isfinite(med))
        sub90 = t[(t.threshold_pct == 90) & (t.level == level)]
        for c in countries.itertuples(index=False):
            oser = OBS_SERIES[level]
            fr = gser[(gser.iso3 == c.iso3) & (gser.indicator == oser)]
            final = float(fr.final_value.iloc[0]) if len(fr) else np.nan
            last_year = int(fr.final_year.iloc[0]) if len(fr) else np.nan
            n_obs = int(fr.n_obs.iloc[0]) if len(fr) else 0
            comp_ser = COMPLETION_SERIES.get(level)
            cf = gser[(gser.iso3 == c.iso3) & (gser.indicator == comp_ser)] if comp_ser else gser.iloc[0:0]
            comp_final = float(cf.final_value.iloc[0]) if len(cf) else np.nan
            comp_last = int(cf.final_year.iloc[0]) if len(cf) else np.nan

            tr = sub90[sub90.iso3 == c.iso3]
            n_timing = int(len(tr))
            if n_timing:
                prio = {"GER": 0, "GER_reconstructed": 1, "NER": 2, "completion": 3}
                tr = tr.assign(_p=tr.measure.map(lambda x: prio.get(x, 9))).sort_values("_p")
                canon = tr.iloc[0]
            else:
                canon = None
            dated_cross = bool(len(tr) and ((tr.censoring == "none") & tr.cross_num.notna()).any())
            right_cens = bool(len(tr) and (tr.censoring == "right").any())
            final_ge90 = bool(pd.notna(final) and final >= 90)

            shows_crossing = bool(final_ge90 or dated_cross)
            if final_ge90 and dated_cross:
                basis = "final_ge_90_and_dated_crossing"
            elif final_ge90:
                basis = "final_ge_90"
            elif dated_cross:
                basis = "dated_crossing_final_below_90"
            elif pd.notna(final):
                basis = "final_below_90"
            else:
                basis = "absent_no_series_no_dated_crossing"
            never = not shows_crossing
            if never:
                if pd.isna(final) and n_timing == 0:
                    ev = "absent_series_and_timing_row"
                elif pd.isna(final):
                    ev = "absent_series"
                elif right_cens:
                    ev = "final_below_90_and_right_censored"
                else:
                    ev = "final_below_90"
            else:
                ev = "not_applicable"

            null_after_last = bool(null_defined and (pd.isna(last_year) or last_year < med))
            null_gen = bool(null_defined)  # null predicts a crossing for every system at that level
            fp_evidence = bool(never and null_gen and pd.notna(final) and not null_after_last)
            fp_incl = bool(never and null_gen)

            audit.append({
                "country": c.country,
                "iso3": c.iso3,
                "level": level,
                "observed_series": oser,
                "observed_final_value": final,
                "observed_final_year": last_year,
                "observed_n_obs": n_obs,
                "completion_series": comp_ser if comp_ser else "",
                "completion_final_value": comp_final,
                "completion_final_year": comp_last,
                "completion_series_present": bool(len(cf)),
                "completion_final_ge_90": bool(pd.notna(comp_final) and comp_final >= 90),
                "completion_channel_disagrees": bool(
                    pd.notna(comp_final) and pd.notna(final)
                    and ((comp_final >= 90) != (final >= 90))),
                "timing_rows_at_90": n_timing,
                "timing_measure": canon.measure if canon is not None else "",
                "timing_crossing_year": (canon.crossing_year if canon is not None else ""),
                "timing_censoring": (canon.censoring if canon is not None else ""),
                "timing_band_earliest": (canon.band_earliest if canon is not None else np.nan),
                "timing_band_latest": (canon.band_latest if canon is not None else np.nan),
                "observed_final_ge_90": final_ge90,
                "observed_dated_crossing": dated_cross,
                "observed_record_shows_crossing": shows_crossing,
                "observed_crossing_basis": basis,
                "never_crossed": never,
                "never_crossed_evidence": ev,
                "null_median_year": med if null_defined else np.nan,
                "null_generates_crossing": null_gen,
                "null_year_after_last_obs": null_after_last,
                "null_false_positive_evidence_backed": fp_evidence,
                "null_false_positive_including_absent": fp_incl,
                "label": "derived",
            })
    aud = pd.DataFrame(audit).sort_values(["level", "iso3"]).reset_index(drop=True)
    aud.to_csv(RES / "Y4_AUDIT.csv", index=False, float_format="%.10f")

    # ---------------- per-level scores ----------------
    scores = []
    for level in LEVEL_ORDER:
        a = aud[aud.level == level]
        lv = lev[lev.level == level].iloc[0]
        n_never = int(a.never_crossed.sum())
        n_never_series = int((a.never_crossed & a.observed_final_value.notna()).sum())
        n_fp_ev = int(a.null_false_positive_evidence_backed.sum())
        n_fp_in = int(a.null_false_positive_including_absent.sum())
        if not lv.null_defined:
            verdict = "UNABLE"
        elif n_fp_in >= MIN_FP:
            verdict = "DISTINGUISHED"
        else:
            verdict = "NOT DISTINGUISHED"
        scores.append({
            "level": level,
            "null_median_year": lv.median_year_system_collapsed,
            "n_systems": int(len(a)),
            "n_never_crossed": n_never,
            "n_never_crossed_with_series": n_never_series,
            "n_null_false_positive_evidence_backed": n_fp_ev,
            "n_null_false_positive_including_absent": n_fp_in,
            "n_never_crossed_testable_at_null_year": int(
                (a.never_crossed & a.observed_final_value.notna() & a.null_generates_crossing
                 & ~a.null_year_after_last_obs).sum()),
            "level_verdict": verdict,
            "label": "derived",
        })
    sc = pd.DataFrame(scores)
    sc.to_csv(RES / "Y4_LEVEL_SCORE.csv", index=False, float_format="%.10f")

    # ---------------- verdict on the predeclared upper-secondary margin ----------------
    upper = sc[sc.level == "upper secondary"].iloc[0]
    upper_aud = aud[(aud.level == "upper secondary") & aud.null_false_positive_including_absent]
    testable = aud[(aud.level == "upper secondary") & aud.null_false_positive_evidence_backed]
    verdict = "DISTINGUISHED" if int(upper.n_null_false_positive_including_absent) >= MIN_FP else "NOT DISTINGUISHED"
    if not lev.loc[lev.level == "upper secondary", "null_defined"].iloc[0]:
        verdict = "UNABLE"

    # ---------------- compact summary (display-formatted; full precision in the audit) ----------------
    def fmt(x):
        if pd.isna(x):
            return "NA"
        xf = float(x)
        if abs(xf - round(xf)) < 1e-9:
            return str(int(round(xf)))
        return f"{xf:.4f}".rstrip("0").rstrip(".")

    upper_row = sc[sc.level == "upper secondary"].iloc[0]
    summary = [
        ("verdict", "DISTINGUISHED" if int(upper_row.n_null_false_positive_including_absent) >= MIN_FP else "NOT DISTINGUISHED"),
        ("upper_secondary_null_year", fmt(upper_row.null_median_year)),
        ("upper_secondary_n_dated_non_censored_rows",
         int(lev.loc[lev.level == "upper secondary", "n_dated_non_censored_rows"].iloc[0])),
        ("upper_secondary_n_systems_dated",
         int(lev.loc[lev.level == "upper secondary", "n_systems_dated_non_censored"].iloc[0])),
        ("upper_secondary_n_never_crossed", int(upper_row.n_never_crossed)),
        ("upper_secondary_n_never_crossed_with_series", int(upper_row.n_never_crossed_with_series)),
        ("upper_secondary_n_fp_incl_absent", int(upper_row.n_null_false_positive_including_absent)),
        ("upper_secondary_n_fp_evidence_backed", int(upper_row.n_null_false_positive_evidence_backed)),
        ("upper_secondary_n_testable_at_null_year", int(upper_row.n_never_crossed_testable_at_null_year)),
        ("all_levels_n_fp_incl_absent", int(sc.n_null_false_positive_including_absent.sum())),
        ("all_levels_n_fp_evidence_backed", int(sc.n_null_false_positive_evidence_backed.sum())),
        ("primary_n_fp_incl_absent", int(sc.loc[sc.level == "primary", "n_null_false_positive_including_absent"].iloc[0])),
        ("lower_secondary_n_fp_incl_absent", int(sc.loc[sc.level == "lower secondary", "n_null_false_positive_including_absent"].iloc[0])),
        ("secondary_n_fp_incl_absent", int(sc.loc[sc.level == "secondary", "n_null_false_positive_including_absent"].iloc[0])),
        
        ("tertiary_null_defined", "NA"),
        ("upper_secondary_null_year_incl_left_censored_sensitivity", fmt(
            lev.loc[lev.level == "upper secondary", "median_year_incl_left_censored_sensitivity"].iloc[0])),
    ]

    def audit_val(iso3, level, col):
        v = aud[(aud.iso3 == iso3) & (aud.level == level)][col]
        v = v.iloc[0] if len(v) else np.nan
        return "NA" if pd.isna(v) else f"{float(v):.2f}"

    for iso3 in ["CHN", "HKG", "JPN", "KHM", "KOR", "PHL"]:
        summary.append((f"upper_secondary_ger_final_{iso3}",
                        audit_val(iso3, "upper secondary", "observed_final_value")))
    for iso3 in ["CHN", "KHM", "KOR", "PHL"]:
        summary.append((f"upper_secondary_completion_final_{iso3}",
                        audit_val(iso3, "upper secondary", "completion_final_value")))
    pd.DataFrame(summary, columns=["metric", "value"]).assign(label="derived").to_csv(
        RES / "Y4_SUMMARY.csv", index=False)


    note = (
        f"Predeclared rule: {THRESHOLD_TEXT}. Null = each level crosses 90 at that level's cross-system "
        f"median of band midpoints (dated non-censored crossings only; censored rows excluded and listed). "
        f"Upper-secondary null year = {upper.null_median_year:.1f} from n=1 dated non-censored crossing (HKG); "
        f"never-crossed systems at upper secondary = {int(upper.n_never_crossed)} "
        f"({', '.join(upper_aud.iso3)}); null false crossings = "
        f"{int(upper.n_null_false_positive_including_absent)} incl. absent, of which "
        f"{int(upper.n_null_false_positive_evidence_backed)} testable against a record reaching the null year "
        f"({', '.join(testable.iso3)}). Across all four 90% levels the null falsely crosses "
        f"{int(sc.n_null_false_positive_including_absent.sum())} system-level cells "
        f"({int(sc.n_null_false_positive_evidence_backed.sum())} evidence-backed). "
        "Descriptive null-model scoring only; no direction claim; C1-C4 not reopened. "
        "Caveat: with one dated non-censored upper-secondary crossing the null is thin; "
        "data-absent (JPN) cases are data absence, not evidence of non-crossing."
    )
    cluster = pd.DataFrame([{
        "experiment": "Y4",
        "cluster": "Y4_worldsociety",
        "question": "Does the predeclared world-society null (every system crosses 90 at the level's cross-system median year) generate an upper-secondary >=90 crossing for a system that never crossed?",
        "estimand": "count of systems with a null-generated upper-secondary >=90 crossing but no observed crossing (predeclared rule incl. right-censored/absent)",
        "estimate": int(upper.n_null_false_positive_including_absent),
        "se": np.nan,
        "ci_low": np.nan,
        "ci_high": np.nan,
        "n": int(upper.n_systems),
        "clusters": int(upper.n_systems),
        "threshold": THRESHOLD_TEXT,
        "verdict": verdict,
        "label": "derived",
        "note": note,
    }])
    cluster.to_csv(RES / "CLUSTER_RESULTS.csv", index=False, float_format="%.10f")

    # ---------------- manifest ----------------
    manifest = {
        "experiment": "Y4_worldsociety",
        "predeclarations_sha256": predecl_sha,
        "data_files_read": [
            {"path": str(TIMING), "sha256": sha256(TIMING)},
            {"path": str(SERIES), "sha256": sha256(SERIES)},
        ],
        "code": [{"path": str(OUT / "code/run.py"), "sha256": sha256(OUT / "code/run.py")}],
        "python_version": sys.version.split()[0],
        "seed": "none",
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reproducibility": "deterministic; no RNG, no network, no imputation; results/*.csv byte-identical on re-run",
    }
    with open(OUT / "RUN_MANIFEST.json", "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(f"Y4 verdict: {verdict}")
    print(sc.to_string(index=False))
    print(f"upper-secondary null year: {upper.null_median_year}")


if __name__ == "__main__":
    main()
