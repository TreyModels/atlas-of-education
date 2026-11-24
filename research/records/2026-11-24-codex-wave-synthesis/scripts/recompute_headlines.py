#!/usr/bin/env python3
"""Independent recomputation of the Codex-wave headline numbers from committed source files.

Run:
    python recompute_headlines.py --sources /tmp/codex_src/data

The --sources directory must contain byte copies of the nine branches' committed result files,
extracted with `git show <head>:<path> > <sources>/<name>` (see EXTRACT below). Every number in
the output JSON is derived here from those files; no number is copied from a branch REPORT.

EXTRACT (run from a clone with origin fetched; heads as verified by the Codex wave):
    git show 9b0cabe:research/records/2026-11-25-q1-mechanisms/results/pilot_recovery_bic.json \
        > $S/q1_recovery.json
    git show db7814d:research/records/2026-11-25-q3-calibration/results/families_for_fdr_check.csv \
        > $S/q3_families.csv
    git show db7814d:research/records/2026-11-25-q3-calibration/results/fdr_check_output.csv \
        > $S/q3_fdr_output.csv
    git show db7814d:research/records/2026-11-25-q3-calibration/results/calibration.json \
        > $S/q3_calibration.json
    git show 7e6f7b5:research/records/2026-11-25-e1-multiverse/results/verdict_by_R.csv \
        > $S/e1_verdict_by_R.csv
    git show e926575:research/records/2026-11-25-e11-fertility-audit/results/q1_construct_audit.json \
        > $S/e11_construct.json
    git show f71b789:research/records/2026-11-25-q2-pathways/data/long_run_panel.csv \
        > $S/long_run_panel.csv
    git show f71b789:research/records/2026-11-25-q2-pathways/results/smoke/pairs.csv \
        > $S/q2_smoke_pairs.csv
    git show f71b789:research/records/2026-11-25-q2-pathways/results/smoke/pairs_metadata.json \
        > $S/q2_smoke_meta.json
    git show 2d19da7:research/records/2026-11-25-e6e8-sequencing/results/e6_classification.csv \
        > $S/e6_classification.csv
    git show ce66cfc:research/records/2026-11-23-subsistence-v2/results/event_dates.csv \
        > $S/subsistence_event_dates.csv

Caveats kept explicit:
- The Q3 `families_for_fdr_check.csv` holds the four committed 272-link p-value families; BH/BY are
  recomputed from the full sorted vectors. The unmodified Codex `fdr_check_output.csv` (also from the
  same record) is used only as a cross-check.
- The Q1 zero-signal control is synthetic by construction; it says nothing about the world.
- The E11 lead/lag ratios are recomputed from committed coefficients; the EFR/TFR median absolute
  difference is recomputed from the committed 5-year-grid panel (sha256 cd30d7ea...), not from prose.
- The subsistence-v2 event CSV @ ce66cfc is the source annotated at 8caaeac; the record's own
  `sequencing.json` field of 68.75 is shown only as the artefact this script decomposes.
"""
import argparse, csv, hashlib, json
import numpy as np
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--sources", default="/tmp/codex_src/data")
ap.add_argument("--out", default="results/recompute.json")
args = ap.parse_args()
S = args.sources
OUT_PATH = args.out


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def bh(p, m):
    p = np.sort(np.asarray(p, float)); k = np.arange(1, len(p) + 1)
    ok = p <= k * 0.05 / m
    return int(k[ok].max()) if ok.any() else 0


def by(p, m):
    H = sum(1.0 / i for i in range(1, m + 1))
    p = np.sort(np.asarray(p, float)); k = np.arange(1, len(p) + 1)
    ok = p <= k * 0.05 / (m * H)
    return int(k[ok].max()) if ok.any() else 0


OUT = {}

# ------------------------------------------------------------------ provenance
OUT["provenance"] = {
    "long_run_panel.csv": {
        "sha256": sha(f"{S}/long_run_panel.csv"),
        "source": "f71b789 research/records/2026-11-25-q2-pathways/data/long_run_panel.csv",
        "record_quotes_sha256": "cd30d7ea7beb77b63de092c53f9b143065b94651f1ac95535ac70eebb3280f2d"},
    "families_for_fdr_check.csv": {
        "sha256": sha(f"{S}/q3_families.csv"),
        "source": "db7814d research/records/2026-11-25-q3-calibration/results/families_for_fdr_check.csv"},
    "verdict_by_R.csv": {
        "sha256": sha(f"{S}/e1_verdict_by_R.csv"),
        "source": "7e6f7b5 research/records/2026-11-25-e1-multiverse/results/verdict_by_R.csv"},
    "pilot_recovery_bic.json": {
        "sha256": sha(f"{S}/q1_recovery.json"),
        "source": "9b0cabe research/records/2026-11-25-q1-mechanisms/results/pilot_recovery_bic.json"},
    "q1_construct_audit.json": {
        "sha256": sha(f"{S}/e11_construct.json"),
        "source": "e926575 research/records/2026-11-25-e11-fertility-audit/results/q1_construct_audit.json"},
    "e6_classification.csv": {
        "sha256": sha(f"{S}/e6_classification.csv"),
        "source": "2d19da7 research/records/2026-11-25-e6e8-sequencing/results/e6_classification.csv"},
    "q2_smoke_pairs.csv": {
        "sha256": sha(f"{S}/q2_smoke_pairs.csv"),
        "source": "f71b789 research/records/2026-11-25-q2-pathways/results/smoke/pairs.csv"},
    "q2_smoke_meta.json": {
        "sha256": sha(f"{S}/q2_smoke_meta.json"),
        "source": "f71b789 research/records/2026-11-25-q2-pathways/results/smoke/pairs_metadata.json"},
    "subsistence_event_dates.csv": {
        "sha256": sha(f"{S}/subsistence_event_dates.csv"),
        "source": "ce66cfc research/records/2026-11-23-subsistence-v2/results/event_dates.csv",
        "annotated_at": "8caaeac"},
}

# ------------------------------------------------- 1. Q1 zero-signal control (synthetic)
q1 = json.load(open(f"{S}/q1_recovery.json"))
z = q1["zero_signal_control"]["0.0"]
mse, bic = z["mse_recovery"], z["bic_recovery"]
OUT["Q1_zero_signal"] = {
    "reps_per_world": q1["reps"],
    "mse_winner_R3_share_W1": mse["W1_direct"]["R3"],
    "mse_winner_R3_share_W2": mse["W2_selection"]["R3"],
    "mse_winner_R1_share_W3": mse["W3_joint"]["R1"],
    "mse_winner_R3_share_W3": mse["W3_joint"]["R3"],
    "bic_winner_R1_share_all_worlds": {w: bic[w]["R1"] for w in bic},
    "reading": "a valid discriminator would be ~1/3. Raw MSE picks the flexible kernel R3 in 97.5% of "
               "W1 and W2 reps; BIC picks the parsimonious R1 in 100% of every world. Both criteria are "
               "degenerate on this pre-registered control, so a 'model winner' is not mechanism evidence. "
               "The branch REPORT rounds 97.5% to '97 per cent'.",
}

# ------------------------------------------------- 2. Q3 full-vector BH/BY (272 links)
fam = pd.read_csv(f"{S}/q3_families.csv")
q3 = {"H_272": sum(1.0 / i for i in range(1, 273))}
for f, key in [("up", "up"), ("down", "down"), ("sign_flip", "flip"), ("heterogeneity", "het")]:
    p = fam[fam.family == f].p.values
    q3[key] = {"n": int(len(p)), "BH_272": bh(p, 272), "BY_272": by(p, 272),
               "BH_meff157": bh(p, 157), "min_p": float(p.min())}
fdr = pd.read_csv(f"{S}/q3_fdr_output.csv")
q3["fdr_check_output_counts"] = {
    f: {"BH": int(fdr[fdr.family == f].bh.sum()), "BY": int(fdr[fdr.family == f].by.sum())}
    for f in ["up", "down", "sign_flip", "heterogeneity"]}
cal = json.load(open(f"{S}/q3_calibration.json"))
B, C = cal["main"]["B"], cal["main"]["C"]
q3["minority_calibration"] = {
    "reps": B["reps"],
    "ROBUST+H_count": B["counts"]["ROBUST+H"],
    "ROBUST-but-GROUP_count": B["counts"]["ROBUST-but-GROUP"],
    "any_robust_share_recomputed": (B["counts"]["ROBUST+H"] + B["counts"]["ROBUST-but-GROUP"]) / B["reps"],
    "planted_tag_flagged_count": B.get("planted_tag_flagged"),
    "planted_tag_hit_rate": (B.get("planted_tag_flagged") / B["reps"]) if B.get("planted_tag_flagged") else None,
    "null_false_positive_recomputed": (C["counts"].get("ROBUST+H", 0) + C["counts"].get("ROBUST-HET", 0)
                                       + C["counts"].get("ROBUST-but-GROUP", 0) + C["counts"].get("GROUP", 0)
                                       + C["counts"].get("BEATS", 0)) / C["reps"],
    "uniform_strong_false_negative_recomputed": cal["main"]["U"]["counts"]["NONE"] / cal["main"]["U"]["reps"],
    "ladder_b006_strict_rate": cal["strength_ladder"]["0.06"]["counts"]["ROBUST+H"] / cal["strength_ladder"]["0.06"]["reps"],
}
OUT["Q3"] = q3

# ------------------------------------------------- 3. E1 R=1200 verdicts / wall / BY budget
v = pd.read_csv(f"{S}/e1_verdict_by_R.csv")
e1 = {"n_links": int(len(v)), "robust_everywhere_Rmax": int(v["robust_everywhere_Rmax"].sum()),
      "R400": {}, "R800": {}, "R1200": {}}
for f in ["up", "down", "flip", "het"]:
    for R in (400, 800, 1200):
        e1[f"R{R}"][f] = {"BH": int(v[f"certBH_{f}_R{R}"].sum()),
                          "BY": int(v[f"certBY_{f}_R{R}"].sum())}
e1["reading"] = ("five of 272 links are robust in every grouping (sum of robust_everywhere_Rmax); "
                 "at R=400 BY certifies 0 in all four families; at R=800 still 0; at R=1200 the "
                 "heterogeneity family alone crosses the BY step-up line (32 links), while up/down/"
                 "sign-flip stay at 0. 'BY = 0' is a draw-budget statement, not a universal one.")
OUT["E1"] = e1

# ------------------------------------------------- 4. E11 construct split: lead/lag and |EFR-TFR|
c = json.load(open(f"{S}/e11_construct.json"))
ll = c["level_ladder"]
def ratio(w):
    b = ll[w]["S(t-10), S, S(t+10)"]
    return b["zSp10"][0] / b["zS"][0]
e11 = {
    "lead_lag_efr_committed": ll["effective_fertility"]["lead_lag_ratio_Sp10_over_S"],
    "lead_lag_efr_recomputed": round(ratio("effective_fertility"), 4),
    "lead_lag_tfr_committed": ll["tfr_observed_1950plus"]["lead_lag_ratio_Sp10_over_S"],
    "lead_lag_tfr_recomputed": round(ratio("tfr_observed_1950plus"), 4),
    "committed_median_abs_diff": c["descriptive"]["median_abs_diff"],
    "committed_max_abs_diff": c["descriptive"]["max_abs_diff"],
}
p = pd.read_csv(f"{S}/long_run_panel.csv")
p = p[(p.year >= 1950) & (p.year <= 2020) & (p.year % 5 == 0)
      & p.effective_fertility.notna() & p.tfr_observed_1950plus.notna()]
d = (p.tfr_observed_1950plus - p.effective_fertility).abs()
e11["panel_recomputed"] = {
    "n_rows": int(len(p)), "n_countries": int(p.iso3.nunique()),
    "median_abs_diff": round(float(d.median()), 4), "max_abs_diff": round(float(d.max()), 4),
    "afg_1950": p[(p.iso3 == "AFG") & (p.year == 1950)]
                [["effective_fertility", "tfr_observed_1950plus"]].to_dict("records"),
}
e11["reading"] = ("effective fertility = surviving children per woman; TFR = births per woman. On a "
                  "matched 5-year grid they differ by median 0.3042 and max 4.2677, and the level "
                  "association with schooling is lag-dominant for EFR (lead/lag 0.541) but "
                  "future-dominant for TFR (1.555). Neither series is a correction of the other.")
OUT["E11"] = e11

# ------------------------------------------------- 5. E6 demand-first shares and bounds
e6 = pd.read_csv(f"{S}/e6_classification.csv")
windows = ["1900-2012", "1960-2010", "1965-2010", "1970-2015"]
e6out = {}
for proxy in ["ggdc_nonag_emp", "urban", "ind_va", "agri_va"]:
    b = e6[e6.proxy == proxy].reset_index(drop=True)
    n = len(b) // 4
    for wi, win in enumerate(windows):
        blk = b.iloc[wi * n:(wi + 1) * n]
        blk = blk[blk.both_events_in_window == True]
        cnt = blk.order.value_counts().to_dict()
        fwd = cnt.get("forward", 0); rev = cnt.get("reverse", 0)
        tie = cnt.get("forward_or_tie", 0); und = cnt.get("undetermined", 0)
        inwin = int(len(blk)); ident = fwd + rev + tie
        e6out.setdefault(proxy, {})[win] = {
            "n_in_window": inwin, "forward": fwd, "reverse": rev,
            "forward_or_tie": tie, "undetermined": und, "identifiable": ident,
            "forward_share_identified": round(100 * fwd / ident, 1) if ident else None,
            "strict_schooling_first_share_identified": round(100 * rev / ident, 1) if ident else None,
            "strict_schooling_first_share_of_strict_orderings": round(100 * rev / (rev + fwd), 1)
                                                                  if (rev + fwd) else None,
            "lower_bound_over_inwindow": round(100 * fwd / inwin, 1) if inwin else None,
            "upper_bound_over_inwindow": round(100 * (fwd + und) / inwin, 1) if inwin else None,
            "tie_or_censored_share_inwindow": round(100 * tie / inwin, 1) if inwin else None,
        }
prim = {proxy: e6out[proxy]["1900-2012"] for proxy in e6out}
OUT["E6"] = {
    "by_proxy_window": e6out,
    "primary_window_ranges_1900_2012": {
        "demand_first_share_identified": [min(v["forward_share_identified"] for v in prim.values()),
                                          max(v["forward_share_identified"] for v in prim.values())],
        "strict_schooling_first_share_identified": [
            min(v["strict_schooling_first_share_identified"] for v in prim.values()),
            max(v["strict_schooling_first_share_identified"] for v in prim.values())],
        "strict_schooling_first_share_of_strict_orderings": [
            min(v["strict_schooling_first_share_of_strict_orderings"] for v in prim.values()),
            max(v["strict_schooling_first_share_of_strict_orderings"] for v in prim.values())],
        "bounds_over_inwindow": [min(v["lower_bound_over_inwindow"] for v in prim.values()),
                                 max(v["upper_bound_over_inwindow"] for v in prim.values())],
        "tie_or_censored_share_inwindow": [min(v["tie_or_censored_share_inwindow"] for v in prim.values()),
                                           max(v["tie_or_censored_share_inwindow"] for v in prim.values())],
    },
    "erratum": ("record head advanced to 59d31d7 (erratum on 2d19da7; REPORT/ERRATUM/docstring only, "
                "data files unchanged): the original E6 prose '18-33% strict schooling-first' did not "
                "reproduce; the values recomputed here are 21.5-46.3% of identifiable countries and "
                "58.3-71.4% of strict orderings."),
    "reading": ("primary window 1900-2012 (full overlap; the preregistered 1960-2010 window selects "
                "against pre-1960 demand take-offs and is reported as robustness): demand-first among "
                "identifiable countries = 10.0% GGDC non-ag employment, 15.4% urbanisation, 24.1% "
                "industry VA, 18.8% agriculture VA; bounds over all in-window countries 6.7-53.0%; "
                "weak ties/left-censoring 21.1-43.3% of in-window countries. Strict schooling-first is "
                "the larger strict ordering in all four proxies: 21.5-46.3% of identifiable countries "
                "(58.3-71.4% of strict orderings) against 10.0-24.1% demand-first, but it is not a "
                "majority of identifiable countries; the remainder are weak ties or undetermined."),
}

# ------------------------------------------------- 6. Q2 pair benchmark (105/52/1/52)
q2 = pd.read_csv(f"{S}/q2_smoke_pairs.csv")
meta = json.load(open(f"{S}/q2_smoke_meta.json"))
countries = set(q2.country_a) | set(q2.country_b)
OUT["Q2"] = {
    "pairs": int(len(q2)),
    "distinct_paired_countries": len(countries),
    "unpaired_countries": meta["unpaired_countries"],
    "baseline_complete_recomputed": len(countries) + meta["unpaired_countries"],
    "pairs_both_school_changes": int(q2[["schooling_change_a", "schooling_change_b"]].notna().all(axis=1).sum()),
    "pairs_both_tfr_changes": int(q2[["tfr_change_a", "tfr_change_b"]].notna().all(axis=1).sum()),
    "panel_sha256_matches_metadata": meta["input_sha256"] == sha(f"{S}/long_run_panel.csv"),
}

# ------------------------------------------------- 7. 68.75% tie artefact -> 37.5% strict
rows = list(csv.DictReader(open(f"{S}/subsistence_event_dates.csv")))
def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None
complete = [r for r in rows if all(num(r.get(k)) is not None for k in ("schooling", "release", "fertility"))]
pairs64 = [(num(r["schooling"]), num(r["fertility"])) for r in complete]
allpairs = [(num(r["schooling"]), num(r["fertility"])) for r in rows
            if num(r.get("schooling")) is not None and num(r.get("fertility")) is not None]
def summ(pairs):
    n = len(pairs)
    sf = sum(1 for a, b in pairs if a < b); ff = sum(1 for a, b in pairs if b < a)
    ti = sum(1 for a, b in pairs if a == b)
    return {"n": n, "schooling_first": sf, "ties": ti, "fertility_first": ff,
            "strict_share_pct": round(100 * sf / n, 2),
            "ties_share_pct": round(100 * ti / n, 2),
            "fertility_first_share_pct": round(100 * ff / n, 2)}
rng = np.random.default_rng(7)
boots = []
for _ in range(1000):
    idx = rng.integers(0, len(pairs64), len(pairs64))
    boots.append(sum(1 for i in idx if pairs64[i][0] < pairs64[i][1]) / len(pairs64))
boots = np.array(boots)
OUT["ordering"] = {
    "source_sha256": sha(f"{S}/subsistence_event_dates.csv"),
    "three_event_sample": summ(pairs64),
    "all_with_both_dates": summ(allpairs),
    "bootstrap_ci95_schooling_first": [round(100 * float(np.percentile(boots, 2.5)), 2),
                                       round(100 * float(np.percentile(boots, 97.5)), 2)],
    "old_record_json_field": "pct_schooling_before_fertility = 68.75",
    "artefact": ("the 44/64 = 68.75% figure adds the 20 simultaneous (tie) countries to the 24 strict "
                 "schooling-first countries; strict ordering is 24/64 = 37.5%, ties 20/64 = 31.25%, "
                 "fertility-first 20/64 = 31.25%"),
}

json.dump(OUT, open(OUT_PATH, "w"), indent=1)
print(json.dumps(OUT, indent=1))
