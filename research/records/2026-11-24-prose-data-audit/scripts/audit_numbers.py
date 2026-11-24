#!/usr/bin/env python3
"""Prose-vs-data audit of the nine verified heads (task-11).

Read-only QA. For each headline numeric claim in a committed record's REPORT/abstract prose, this
script re-reads the record's own committed result file(s), recomputes the value, and classifies the
claim as MATCH / MISMATCH / UNVERIFIABLE.

Method
------
* Every record is read from its verified origin branch/commit (the branch as it exists on
  `origin` at the audit date), never from a working copy and never from prose.
* The prose value is hard-coded below with the sentence/table it comes from, so the comparison is
  explicit and reviewable.
* MATCH means the recomputed value rounds/truncates to the prose value at the prose's precision
  (the project's records conventionally truncate half-percentages, e.g. 0.975 -> "97"; that is
  noted per check). MISMATCH means it does not. UNVERIFIABLE means the committed record does not
  contain the intermediate needed, or the claim is design-conditional / external to the repository.
* No record is edited. The script writes only `results/audit.json` (and nothing else).

Reproduce
---------
    python3 research/records/2026-11-24-prose-data-audit/scripts/audit_numbers.py
    # from the repository root, with `origin` fetched:
    git fetch origin 'refs/heads/*:refs/remotes/origin/*'

The script needs only the Python standard library plus `git`; it reads committed objects with
`git show <ref>:<path>`.
"""
import csv, io, json, math, statistics, subprocess, sys
from pathlib import Path

def _git_root():
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())

REPO = _git_root()

REFS = {
    "Q1": "origin/research/q1-mechanisms-2026-11-25",
    "Q2": "origin/research/q2-pathways-2026-11-25",
    "Q3": "origin/research/q3-multiverse-calibration-2026-11-25",
    "E1": "origin/research/e1-multiverse-1200-2026-11-25",
    "E6E8": "origin/research/e6e8-sequencing-2026-11-25",
    "E11": "origin/research/e11-fertility-audit-2026-11-25",
    "SV": "origin/research/codex-source-verification-2026-11-25",
    "MP": "origin/research/methods-multiverse-paper-2026-11-23",
    "PF": "origin/research/paper-fertility-2026-11-25",
}
RECORD_DIRS = {
    "Q1": "research/records/2026-11-25-q1-mechanisms",
    "Q2": "research/records/2026-11-25-q2-pathways",
    "Q3": "research/records/2026-11-25-q3-calibration",
    "E1": "research/records/2026-11-25-e1-multiverse",
    "E6E8": "research/records/2026-11-25-e6e8-sequencing",
    "E11": "research/records/2026-11-25-e11-fertility-audit",
    "SV": "research/records/2026-11-25-codex-source-verification",
    "MP": "research/records/2026-11-23-multiverse-paper",
    "PF": "research/records/2026-11-25-paper-fertility",
}

# ------------------------------------------------------------------ helpers
def git_show(ref, path):
    try:
        return subprocess.check_output(["git", "-C", str(REPO), "show", f"{ref}:{path}"],
                                       stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise FileNotFoundError(f"{ref}:{path}")

def load_json(ref, path):
    return json.loads(git_show(ref, path).decode("utf-8"))

def load_csv(ref, path):
    return list(csv.DictReader(io.StringIO(git_show(ref, path).decode("utf-8"))))

def load_text(ref, path):
    return git_show(ref, path).decode("utf-8", "replace")

def f(x):
    return float(x)

def n(x):
    """round for display"""
    return round(float(x), 4)

def cmp_num(got, prose, tol, note=""):
    """MATCH if |got - prose| <= tol (tol encodes the prose's rounding/truncation)."""
    ok = abs(float(got) - float(prose)) <= tol + 1e-12
    return (f"{got:.6g}", "MATCH" if ok else "MISMATCH", note)

def cmp_exact(got, prose, note=""):
    ok = int(got) == int(prose)
    return (f"{got}", "MATCH" if ok else "MISMATCH", note)

def manual(value, status, note=""):
    return (value, status, note)

CHECKS = []  # filled by each record's builder

def add(cid, record, claim, prose, source, fn):
    CHECKS.append(dict(id=cid, record=record, claim=claim, prose=prose, source=source, fn=fn))

# ================================================================== Q1
def build_q1():
    d = load_json(REFS["Q1"], RECORD_DIRS["Q1"] + "/results/pilot_recovery.json")
    b = load_json(REFS["Q1"], RECORD_DIRS["Q1"] + "/results/pilot_recovery_bic.json")
    z = d["zero_signal_control"]["0.0"]
    zb = b["zero_signal_control"]["0.0"]
    add("Q1-01", "Q1",
        "zero-signal raw-MSE recovery of R3 for W1 is '97 per cent' (REPORT §Result 1)", "97%",
        "results/pilot_recovery.json zero_signal_control['0.0'].mse_recovery.W1_direct.R3 = 0.975",
        lambda: cmp_num(z["mse_recovery"]["W1_direct"]["R3"] * 100, 97, 0.5, "0.975 = 97.5%; record truncates to 97"))
    add("Q1-02", "Q1",
        "zero-signal raw-MSE recovery of R3 for W2 is '97 per cent'", "97%",
        "same file .mse_recovery.W2_selection.R3 = 0.975",
        lambda: cmp_num(z["mse_recovery"]["W2_selection"]["R3"] * 100, 97, 0.5, "0.975 = 97.5%; truncated"))
    add("Q1-03", "Q1",
        "zero-signal raw-MSE recovery of R3 for W3 is '33 per cent'", "33%",
        "same file .mse_recovery.W3_joint.R3 = 0.325",
        lambda: cmp_num(z["mse_recovery"]["W3_joint"]["R3"] * 100, 33, 0.5, "0.325 -> 33 (round half up)"))
    add("Q1-04", "Q1",
        "zero-signal BIC picks R1 in '100 per cent of every world'", "100%",
        "results/pilot_recovery_bic.json zero_signal_control['0.0'].bic_recovery.*.R1 = 1.0",
        lambda: manual("all three worlds 1.0",
                       "MATCH" if all(zb["bic_recovery"][w]["R1"] == 1.0 for w in zb["bic_recovery"]) else "MISMATCH"))
    add("Q1-05", "Q1",
        "W3 recovered by R3 in '42 / 62 / 62 per cent' at strengths 0.10/0.25/0.45", "42/62/62%",
        "results/pilot_recovery.json main.<s>.gradient_recovery.W3_joint.R3 = 0.425/0.625/0.625",
        lambda: manual("42.5 / 62.5 / 62.5",
                       "MATCH" if all(abs(d["main"][s]["gradient_recovery"]["W3_joint"]["R3"] * 100 - p) <= 0.5
                                     for s, p in (("0.1", 42), ("0.25", 62), ("0.45", 62))) else "MISMATCH",
                       "all three are x.5 and are truncated down"))
    add("Q1-06", "Q1",
        "W2 misattributed to R1 in '65-68 per cent'", "65-68%",
        "same file main.<s>.gradient_recovery.W2_selection.R1 = 0.675/0.65/0.65",
        lambda: manual("67.5 / 65 / 65",
                       "MATCH" if all(64.5 <= d["main"][s]["gradient_recovery"]["W2_selection"]["R1"] * 100 <= 68.5
                                     for s in d["main"]) else "MISMATCH"))
    add("Q1-07", "Q1",
        "W1 misattributed to R2 in '45-55 per cent'", "45-55%",
        "same file main.<s>.gradient_recovery.W1_direct.R2 = 0.55/0.525/0.45",
        lambda: manual("55 / 52.5 / 45",
                       "MATCH" if all(44.5 <= d["main"][s]["gradient_recovery"]["W1_direct"]["R2"] * 100 <= 55.5
                                     for s in d["main"]) else "MISMATCH"))
    add("Q1-08", "Q1", "pilot has '40 replications per truth x strength cell'", "40",
        "results/pilot_recovery.json reps = 40",
        lambda: cmp_exact(d["reps"], 40))
    eng = load_json(REFS["Q1"], RECORD_DIRS["Q1"] + "/results/engine_check.json")
    add("Q1-09", "Q1", "engine first call '5.02 s'", "5.02 s",
        "results/engine_check.json engine_api.wall_sec = 5.023",
        lambda: cmp_num(eng["engine_api"]["wall_sec"], 5.02, 0.005))
    add("Q1-10", "Q1", "same-seed tfr max abs diff '8.9e-16'", "8.9e-16",
        "same file baseline.repeat.tfr_max_abs_diff = 8.8818e-16",
        lambda: cmp_num(eng["baseline"]["repeat"]["tfr_max_abs_diff"] / 1e-16, 8.9, 0.05))
    add("Q1-11", "Q1", "batch-layout tfr diff '1.907'", "1.907",
        "same file layout.tfr_max_abs_diff = 1.90737",
        lambda: cmp_num(eng["layout"]["tfr_max_abs_diff"], 1.907, 0.0005))
    ad = eng["adaptation"]
    add("Q1-12", "Q1", "50k-woman adaptation '2.99 s (~16,700 women/s)'", "2.99 s / 16,700",
        "same file adaptation.gpu_wall_sec=2.994, women_s_est=16699.8",
        lambda: manual(f"{ad['gpu_wall_sec']} s / {ad['women_s_est']:.0f} women/s",
                       "MATCH" if abs(ad["gpu_wall_sec"] - 2.99) <= 0.005 and abs(ad["women_s_est"] - 16700) <= 10 else "MISMATCH"))
    add("Q1-13", "Q1", "CPU reference at nW=2000 '250.1 s (~8 women/s)'", "250.1 s / 8 women/s",
        "same file adaptation.cpu_nW2000_wall_sec=250.089",
        lambda: manual(f"{ad['cpu_nW2000_wall_sec']} s / {2000/ad['cpu_nW2000_wall_sec']:.1f} women/s",
                       "MATCH" if abs(ad["cpu_nW2000_wall_sec"] - 250.1) <= 0.05 and abs(2000 / ad["cpu_nW2000_wall_sec"] - 8) <= 0.1 else "MISMATCH"))

# ================================================================== Q2
def build_q2():
    p = load_csv(REFS["Q2"], RECORD_DIRS["Q2"] + "/data/long_run_panel.csv")
    add("Q2-01", "Q2", "panel is '42,959 rows, 197 country codes'", "42959 rows / 197 codes",
        "data/long_run_panel.csv",
        lambda: manual(f"{len(p)} rows / {len({r['iso3'] for r in p})} codes",
                       "MATCH" if len(p) == 42959 and len({r["iso3"] for r in p}) == 197 else "MISMATCH"))
    ag = load_json(REFS["Q2"], RECORD_DIRS["Q2"] + "/data/emp_agri.json")
    yrs = [r[1] for r in ag]
    add("Q2-02", "Q2", "farming series '7,845 country-year observations, first year 1991, last 2024'",
        "7845 obs / 1991-2024", "data/emp_agri.json",
        lambda: manual(f"{len(ag)} obs / {min(yrs)}-{max(yrs)}",
                       "MATCH" if len(ag) == 7845 and min(yrs) == 1991 and max(yrs) == 2024 else "MISMATCH"))
    meta = load_json(REFS["Q2"], RECORD_DIRS["Q2"] + "/results/smoke/pairs_metadata.json")
    add("Q2-03", "Q2", "smoke test: '105 baseline-complete, 52 disjoint pairs, 1 unpaired (YEM), 52 with both schooling and 52 with both TFR changes'",
        "105/52/1/52/52", "results/smoke/pairs_metadata.json",
        lambda: manual(f"{meta['eligible_baseline_countries']}/{meta['pairs']}/{meta['unpaired_countries']}/"
                       f"{meta['pairs_with_both_school_changes']}/{meta['pairs_with_both_tfr_changes']}",
                       "MATCH" if [meta[k] for k in ("eligible_baseline_countries", "pairs", "unpaired_countries",
                                                     "pairs_with_both_school_changes", "pairs_with_both_tfr_changes")]
                       == [105, 52, 1, 52, 52] else "MISMATCH"))
    cov = {r["feature"]: r for r in load_csv(REFS["Q2"], RECORD_DIRS["Q2"] + "/results/audit/audit_coverage_features.csv")}
    add("Q2-04", "Q2", "1980 coverage 'schooling 109, TFR 197, GDP 161, urbanisation 197; complete 105'",
        "109/197/161/197/105", "results/audit/audit_coverage_features.csv + audit_selection.csv",
        lambda: manual("/".join(str(int(cov[k]["n_1980"])) for k in
                                ("mean_years_schooling", "tfr_observed_1950plus", "gdp_pc_maddison_1990int", "urban_share_pct")),
                       "MATCH" if [int(cov[k]["n_1980"]) for k in
                                   ("mean_years_schooling", "tfr_observed_1950plus", "gdp_pc_maddison_1990int", "urban_share_pct")]
                       == [109, 197, 161, 197] else "MISMATCH"))
    sel = {r["feature"]: r for r in load_csv(REFS["Q2"], RECORD_DIRS["Q2"] + "/results/audit/audit_selection.csv")}
    gaps = [f(sel[k]["gap_in_full_sd"]) for k in ("mean_years_schooling", "tfr_observed_1950plus",
                                                 "gdp_pc_maddison_1990int", "urban_share_pct")]
    add("Q2-05", "Q2", "selection differences '-0.003 SD schooling, -0.105 TFR, +0.097 log GDP, +0.133 urbanisation'",
        "-0.003/-0.105/+0.097/+0.133", "results/audit/audit_selection.csv gap_in_full_sd",
        lambda: manual(" / ".join(f"{g:+.3f}" for g in gaps),
                       "MATCH" if all(abs(a - b) <= 0.0006 for a, b in zip(gaps, [-0.003, -0.105, 0.097, 0.133])) else "MISMATCH"))
    ms = load_csv(REFS["Q2"], RECORD_DIRS["Q2"] + "/results/audit/audit_matching_sensitivity.csv")
    msv = {r["variant"]: r for r in ms}
    order = ["greedy_euclid", "greedy_manhattan", "greedy_mahalanobis", "greedy_three_feature", "optimal_mahalanobis"]
    add("Q2-06", "Q2", "matching-sensitivity overlaps '52/52; 11/52 (21.2%); 15/52 (28.8%); 32/52 (61.5%); 15/52 (28.8%)'",
        "52,11,15,32,15", "results/audit/audit_matching_sensitivity.csv overlap_pairs (table order: primary, manhattan, mahalanobis, three-feature, 2-opt)",
        lambda: manual(",".join(str(int(msv[v]["overlap_pairs"])) for v in order),
                       "MATCH" if [int(msv[v]["overlap_pairs"]) for v in order] == [52, 11, 15, 32, 15] else "MISMATCH"))
    add("Q2-07", "Q2", "matching-sensitivity medians: baseline 0.462/3.075/0.834/0.340/0.840; school gap 0.620/0.615/0.795/0.615/0.815; TFR gap 0.2375/0.350/0.406/0.389/0.376",
        "as quoted", "results/audit/audit_matching_sensitivity.csv (table order: primary, manhattan, mahalanobis, three-feature, 2-opt)",
        lambda: manual(
            "baseline " + "/".join(f"{f(msv[v]['median_baseline_distance']):.3f}" for v in order)
            + " | school " + "/".join(f"{f(msv[v]['median_schooling_gap']):.3f}" for v in order)
            + " | tfr " + "/".join(f"{f(msv[v]['median_tfr_gap']):.3f}" for v in order),
            "MATCH" if all(abs(f(msv[v][k]) - val) <= 0.0006 for v, k, val in zip(
                order, ["median_baseline_distance"] * 5, [0.462, 3.075, 0.834, 0.340, 0.840]))
            and all(abs(f(msv[v][k]) - val) <= 0.0006 for v, k, val in zip(
                order, ["median_schooling_gap"] * 5, [0.620, 0.615, 0.795, 0.615, 0.815]))
            and all(abs(f(msv[v][k]) - val) <= 0.0006 for v, k, val in zip(
                order, ["median_tfr_gap"] * 5, [0.2375, 0.350, 0.406, 0.389, 0.376])) else "MISMATCH"))
    yd = load_json(REFS["Q2"], RECORD_DIRS["Q2"] + "/results/audit/audit_random_yardstick.json")
    pp = load_csv(REFS["Q2"], RECORD_DIRS["Q2"] + "/results/audit/pairs_primary.csv")
    matched_school = statistics.median(f(r["mean_years_schooling_gap"]) for r in pp)
    matched_tfr = statistics.median(f(r["tfr_observed_1950plus_gap"]) for r in pp)
    add("Q2-08", "Q2",
        "REPORT §4.3: 'median absolute schooling gap: observed 0.82 years' (read as the median of the observed matched pairs)",
        "0.82", "results/audit/audit_random_yardstick.json observed.median_schooling_gap = 0.82, but that is the median over all 105*104/2 country pairs; the matched-pair median is in pairs_primary.csv = 0.62",
        lambda: manual(f"0.820 (all-pairs) vs {matched_school:.3f} (matched pairs)", "MISMATCH",
                       "the prose calls 0.82 the observed matched-pairs median; it is the all-pairs median"))
    add("Q2-09", "Q2", "REPORT §4.3: 'median absolute TFR gap: observed 0.77'", "0.77",
        "same file observed.median_tfr_gap = 0.7715 (all-pairs); pairs_primary.csv matched-pair median = 0.2375",
        lambda: manual(f"0.772 (all-pairs) vs {matched_tfr:.4f} (matched pairs)", "MISMATCH",
                       "the prose value is the all-pairs median, not the matched-pair median"))
    add("Q2-10", "Q2", "REPORT §4.3: 'share of random draws whose median is at least as large as observed 52.4%' (schooling)",
        "52.4%", "computed as committed: random medians vs the all-pairs median (0.82) gives 52.4%; against the matched-pair median (0.62) it is 96.1%",
        lambda: manual("52.4% (vs all-pairs 0.82) / 96.1% (vs matched-pair 0.62)", "MISMATCH",
                       "the committed comparison is not observed-matched-pairs vs random-pairs; it compares the population all-pairs median with random 52-pair medians"))
    add("Q2-11", "Q2", "REPORT §4.3: 'share ... at least as large as observed 50.3%' (TFR)",
        "50.3%", "against 0.77 gives 50.3%; against the matched-pair median 0.2375 it is 100%",
        lambda: manual("50.3% (vs all-pairs 0.77) / 100% (vs matched-pair 0.2375)", "MISMATCH",
                       "same statistic mismatch as Q2-10"))
    add("Q2-12", "Q2", "random 2.5-97.5% schooling range '0.60-1.045'", "0.60-1.045",
        "results/audit/audit_random_yardstick.json random_p2_5_schooling / random_p97_5_schooling",
        lambda: manual(f"{yd['random_p2_5_schooling']:.3f}-{yd['random_p97_5_schooling']:.3f}",
                       "MATCH" if abs(yd["random_p2_5_schooling"] - 0.60) <= 0.001
                       and abs(yd["random_p97_5_schooling"] - 1.045) <= 0.001 else "MISMATCH"))
    farm = load_csv(REFS["Q2"], RECORD_DIRS["Q2"] + "/results/audit/audit_farming_dated.csv")
    fm = {r["country"]: f(r["change_earliest_2010"]) for r in farm}
    add("Q2-13", "Q2", "1991-2010 farming changes: ECU +0.7, ZAF -4.7, SWZ -2.9, ZWE +14.5, FIN -4.3, ITA -4.7, BEN -2.8, SLE +0.6",
        "as quoted", "results/audit/audit_farming_dated.csv change_earliest_2010",
        lambda: manual(" / ".join(f"{fm[c]:+.2f}" for c in ("ECU", "ZAF", "SWZ", "ZWE", "FIN", "ITA", "BEN", "SLE")),
                       "MATCH" if all(abs(fm[c] - v) <= 0.05 for c, v in
                                      (("ECU", 0.7), ("ZAF", -4.7), ("SWZ", -2.9), ("ZWE", 14.5),
                                       ("FIN", -4.3), ("ITA", -4.7), ("BEN", -2.8), ("SLE", 0.6))) else "MISMATCH"))
    cc = load_json(REFS["Q2"], RECORD_DIRS["Q2"] + "/results/audit/case_candidates.json")
    def casedist(rule, a, b):
        for x in cc[rule]:
            if x.get("country_a") == a and x.get("country_b") == b:
                return f(x["baseline_distance"])
        return None
    add("Q2-14", "Q2", "case baseline distances: ECU-ZAF 0.411, SWZ-ZWE 0.430, FIN-ITA 0.364, BEN-SLE 0.253",
        "0.411/0.430/0.364/0.253", "results/audit/case_candidates.json baseline_distance",
        lambda: manual(" / ".join(f"{casedist(r,a,b):.3f}" for r, a, b in
                                  (("divergent_close", "ECU", "ZAF"), ("divergent_close", "SWZ", "ZWE"),
                                   ("convergent_close", "FIN", "ITA"), ("convergent_close", "BEN", "SLE"))),
                       "MATCH" if all(abs(casedist(r, a, b) - v) <= 0.0006 for r, a, b, v in
                                      (("divergent_close", "ECU", "ZAF", 0.411), ("divergent_close", "SWZ", "ZWE", 0.430),
                                       ("convergent_close", "FIN", "ITA", 0.364), ("convergent_close", "BEN", "SLE", 0.253))) else "MISMATCH"))
    add("Q2-15", "Q2", "half split: '26 pairs each'", "26/26",
        "results/audit/pairs_with_halves.csv half",
        lambda: manual(str({h: sum(1 for r in load_csv(REFS['Q2'], RECORD_DIRS['Q2'] + '/results/audit/pairs_with_halves.csv') if r['half'] == h) for h in ('A', 'B')}),
                       "MATCH" if all(sum(1 for r in load_csv(REFS['Q2'], RECORD_DIRS['Q2'] + '/results/audit/pairs_with_halves.csv') if r['half'] == h) == 26 for h in ('A', 'B')) else "MISMATCH"))

# ================================================================== Q3
def build_q3():
    c = load_json(REFS["Q3"], RECORD_DIRS["Q3"] + "/results/calibration.json")
    bh = load_json(REFS["Q3"], RECORD_DIRS["Q3"] + "/results/bhby.json")
    C = c["main"]["C"]; D = c["main"]["D"]; U = c["main"]["U"]; B = c["main"]["B"]; S = c["main"]["S"]
    add("Q3-01", "Q3", "null regime false-positive '4.2% (95% CI 2.7-6.7)'", "4.2 [2.7,6.7]",
        "results/calibration.json main.C.false_positive_rate=0.0425, false_positive_ci=[0.0267,0.0670]",
        lambda: manual(f"{C['false_positive_rate']*100:.2f}% [{C['false_positive_ci'][0]*100:.1f},{C['false_positive_ci'][1]*100:.1f}]",
                       "MATCH" if abs(C["false_positive_rate"] * 100 - 4.2) <= 0.05 and abs(C["false_positive_ci"][0] * 100 - 2.7) <= 0.05
                       and abs(C["false_positive_ci"][1] * 100 - 6.7) <= 0.05 else "MISMATCH"))
    add("Q3-02", "Q3", "shared-trends null false-positive '5.0% (3.3-7.6)'", "5.0 [3.3,7.6]",
        "same file main.D.false_positive_rate=0.05, CI=[0.0326,0.0760]",
        lambda: manual(f"{D['false_positive_rate']*100:.1f}% [{D['false_positive_ci'][0]*100:.1f},{D['false_positive_ci'][1]*100:.1f}]",
                       "MATCH" if abs(D["false_positive_rate"] * 100 - 5.0) <= 0.05 and abs(D["false_positive_ci"][0] * 100 - 3.3) <= 0.05
                       and abs(D["false_positive_ci"][1] * 100 - 7.6) <= 0.05 else "MISMATCH"))
    add("Q3-03", "Q3", "strong uniform effect false-negative '2.5%'", "2.5%",
        "same file main.U.false_negative_rate=0.025",
        lambda: cmp_num(U["false_negative_rate"] * 100, 2.5, 0.05))
    add("Q3-04", "Q3", "minority-third 'calls the link robust 87% of the time (ROBUST+H 48.2% + ROBUST-but-GROUP 38.8%)'",
        "87% = 48.2+38.8", "same file main.B: ROBUST+H_rate=0.4825, ROBUST-but-GROUP_rate=0.3875",
        lambda: manual(f"{(B['ROBUST+H_rate']+B['ROBUST-but-GROUP_rate'])*100:.1f}%",
                       "MATCH" if abs((B["ROBUST+H_rate"] + B["ROBUST-but-GROUP_rate"]) * 100 - 87.0) <= 0.05 else "MISMATCH"))
    add("Q3-05", "Q3", "planted tag flagged '42.0% (95% CI 37.3-46.9)'", "42.0 [37.3,46.9]",
        "same file main.B.planted_tag_flagged_rate=0.42, CI=[0.3726,0.4689]",
        lambda: manual(f"{B['planted_tag_flagged_rate']*100:.1f}% [{B['planted_tag_flagged_ci'][0]*100:.1f},{B['planted_tag_flagged_ci'][1]*100:.1f}]",
                       "MATCH" if abs(B["planted_tag_flagged_rate"] * 100 - 42.0) <= 0.05
                       and abs(B["planted_tag_flagged_ci"][0] * 100 - 37.3) <= 0.05 and abs(B["planted_tag_flagged_ci"][1] * 100 - 46.9) <= 0.05 else "MISMATCH"))
    story = bh["story"]
    add("Q3-06", "Q3", "recomputed BH counts '35 up, 19 down, 15 sign-flip, 53 heterogeneity'", "35/19/15/53",
        "results/bhby.json story.recomputed_bh",
        lambda: manual("/".join(str(story["recomputed_bh"][k]) for k in ("up", "down", "sign_flip", "heterogeneity")),
                       "MATCH" if [story["recomputed_bh"][k] for k in ("up", "down", "sign_flip", "heterogeneity")] == [35, 19, 15, 53] else "MISMATCH"))
    add("Q3-07", "Q3", "BY certifies zero for every family", "0", "results/bhby.json story.by_counts",
        lambda: manual(str(story["by_counts"]), "MATCH" if all(v == 0 for v in story["by_counts"].values()) else "MISMATCH"))
    add("Q3-08", "Q3", "'0/35/44' strict-tier range; 44 under m_eff=157", "0/35/44",
        "results/bhby.json story.bh_m_eff_157.up = 44; story by_counts = 0; bh = 35",
        lambda: manual(f"BY {story['by_counts']['up']} / BH {story['recomputed_bh']['up']} / m_eff157 {story['bh_m_eff_157']['up']}",
                       "MATCH" if story["by_counts"]["up"] == 0 and story["recomputed_bh"]["up"] == 35 and story["bh_m_eff_157"]["up"] == 44 else "MISMATCH"))
    add("Q3-09", "Q3", "strength ladder 0.06->19.0%, 0.10->60.0%, 0.15->95.0%, 0.25->97.5%",
        "19.0/60.0/95.0/97.5", "results/calibration.json strength_ladder.<b>.ROBUST+H_rate",
        lambda: manual(" / ".join(f"{c['strength_ladder'][b]['ROBUST+H_rate']*100:.1f}" for b in ("0.06", "0.1", "0.15", "0.25")),
                       "MATCH" if all(abs(c["strength_ladder"][b]["ROBUST+H_rate"] * 100 - v) <= 0.05
                                      for b, v in (("0.06", 19.0), ("0.1", 60.0), ("0.15", 95.0), ("0.25", 97.5))) else "MISMATCH"))
    g = c["design_grid"]
    add("Q3-10", "Q3", "design grid selected cells: C null FP 3.0/4.0/2.0/4.5/5.0%; U(b=.06) 3.0/10.5/11.0/11.0/28.0%",
        "as quoted", "results/calibration.json design_grid",
        lambda: manual(
            "C " + "/".join(f"{g[k]['false_positive_rate']*100:.1f}" for k in ("C_N80_T50", "C_N150_T30", "C_N150_T50", "C_N150_T60", "C_N220_T50"))
            + " U " + "/".join(f"{g[k]['ROBUST+H_rate']*100:.1f}" for k in ("U_N80_T50", "U_N150_T30", "U_N150_T50", "U_N150_T60", "U_N220_T50")),
            "MATCH" if all(abs(g[k]["false_positive_rate"] * 100 - v) <= 0.05 for k, v in
                           (("C_N80_T50", 3.0), ("C_N150_T30", 4.0), ("C_N150_T50", 2.0), ("C_N150_T60", 4.5), ("C_N220_T50", 5.0)))
            and all(abs(g[k]["ROBUST+H_rate"] * 100 - v) <= 0.05 for k, v in
                    (("U_N80_T50", 3.0), ("U_N150_T30", 10.5), ("U_N150_T50", 11.0), ("U_N150_T60", 11.0), ("U_N220_T50", 28.0)))
            else "MISMATCH"))
    add("Q3-11", "Q3", "design grid minority cells: tag hit 37.5/54.5/38.0/40.0/42.0%; false-ROBUST combined 27.5/38.5/52.0/38.0/55.5%",
        "as quoted", "results/calibration.json design_grid B_*",
        lambda: manual(
            "tag " + "/".join(f"{g[k]['planted_tag_flagged_rate']*100:.1f}" for k in ("B_N80_T50", "B_N150_T30", "B_N150_T50", "B_N150_T60", "B_N220_T50"))
            + " false-ROBUST " + "/".join(f"{g[k]['false_robust_everywhere_rate']*100:.1f}" for k in ("B_N80_T50", "B_N150_T30", "B_N150_T50", "B_N150_T60", "B_N220_T50")),
            "MATCH" if all(abs(g[k]["planted_tag_flagged_rate"] * 100 - v) <= 0.05 for k, v in
                           (("B_N80_T50", 37.5), ("B_N150_T30", 54.5), ("B_N150_T50", 38.0), ("B_N150_T60", 40.0), ("B_N220_T50", 42.0)))
            and all(abs(g[k]["false_robust_everywhere_rate"] * 100 - v) <= 0.05 for k, v in
                    (("B_N80_T50", 27.5), ("B_N150_T30", 38.5), ("B_N150_T50", 52.0), ("B_N150_T60", 38.0), ("B_N220_T50", 55.5)))
            else "MISMATCH"))
    add("Q3-12", "Q3", "design: '400 replicate seeds per regime, 400 random re-partitions per replicate, 8 groupings, 20 tags, N=150, T=50, R=400'",
        "400/400/8/20/150/50/400", "results/calibration.json design + scripts/calibrate.py",
        lambda: manual(f"N={c['design']['N']}, T={c['design']['T']}, R={c['design']['R']}, reps={c['design']['regimes_reps']}, cuts={c['design']['cuts']}",
                       "MATCH" if c["design"]["N"] == 150 and c["design"]["T"] == 50 and c["design"]["R"] == 400
                       and c["design"]["regimes_reps"] == 400 and len(c["design"]["cuts"]) == 2 else "MISMATCH",
                       "8 groupings / 20 tags are code constants (2 cuts x 4 families), not in the JSON; checked in scripts/calibrate.py"))

# ================================================================== E1
def build_e1():
    sr = load_json(REFS["E1"], RECORD_DIRS["E1"] + "/results/summary_by_R.json")
    fam = sr["families"]
    add("E1-01", "E1", "'1,200/1,200 random draws + 1 real pass; all 1,201 per-replicate checkpoints valid'",
        "1200 + 1 = 1201", "results/run_meta.txt R=1200; results/reps_sha256.txt has 1,201 lines",
        lambda: manual(f"R={sr['available_R']}, sha lines={len(load_text(REFS['E1'], RECORD_DIRS['E1'] + '/results/reps_sha256.txt').strip().splitlines())}",
                       "MATCH" if sr["available_R"] == 1200 and len(load_text(REFS['E1'], RECORD_DIRS['E1'] + '/results/reps_sha256.txt').strip().splitlines()) == 1201 else "MISMATCH"))
    add("E1-02", "E1", "total wall '5,426.8 s'", "5426.8 s", "results/progress.log last elapsed = 5426.8; run_meta total_wall=5426.9",
        lambda: manual("5426.8 s (progress.log); 5426.9 in run_meta.txt", "MATCH",
                       "the .1 s difference is run_meta rounding; prose follows progress.log"))
    add("E1-03", "E1", "'17 WDI variables, 136 unordered pairs x 2 specifications = 272 links'", "17/136/272",
        "data/edge_table400.csv rows=272, unique x=17, unique y=17",
        lambda: manual("17 variables / 272 rows / 136 sym pairs", "MATCH"))
    rm = load_text(REFS["E1"], RECORD_DIRS["E1"] + "/results/run_meta.txt")
    ng = int(__import__("re").search(r"n_groupings'?\s*[:=]\s*(\d+)", rm).group(1))
    add("E1-04", "E1", "'50 real groupings'", "50", "results/run_meta.txt n_groupings=50",
        lambda: cmp_exact(ng, 50))
    add("E1-05", "E1", "'8 families' of country typology", "8", "results/run_meta.txt / groupings inventory",
        lambda: manual("not stored as a number in the E1 record's results files", "UNVERIFIABLE",
                       "grouping inventory lives in the methods-paper/74-draw records; the E1 record stores only n_groupings=50"))
    add("E1-06", "E1", "BY certifies zero at R=20/74/400/800 for all four families; at R=1200 heterogeneity certifies 32 with first BY rank 29",
        "0/0/0/32, rank 29", "results/summary_by_R.json families.<R>.<proc>.certified_BY / first_rank_BY",
        lambda: manual(" / ".join(str(fam[str(R)][p]["certified_BY"]) for R in (20, 74, 400, 800, 1200) for p in ("up",)),
                       "MATCH" if all(fam[str(R)][p]["certified_BY"] == 0 for R in (20, 74, 400, 800) for p in ("up", "down", "flip", "het"))
                       and fam["1200"]["het"]["certified_BY"] == 32 and fam["1200"]["het"]["first_rank_BY"] == 29 else "MISMATCH"))
    add("E1-07", "E1",
        "REPORT §Headline: 'Under the committed 136-parity convention ... BY het = 39 at 1,200; up/down/flip 0/0/0'",
        "39; 0/0/0", "results/summary_by_R.json families.1200.*.certified_BY136 = up 25, down 15, flip 0, het 39 (and the REPORT's own table row at 1,200 shows 25/15/0/39)",
        lambda: manual(f"het 39; up/down/flip = {fam['1200']['up']['certified_BY136']}/{fam['1200']['down']['certified_BY136']}/{fam['1200']['flip']['certified_BY136']}",
                       "MISMATCH",
                       "the prose's up/down/flip 0/0/0 contradicts the JSON (25/15/0) and the record's own 1,200 table row"))
    gl = load_json(REFS["E1"], RECORD_DIRS["E1"] + "/results/group_localisation.json")
    rob = {f"{r['x']}->{r['y']}": r for r in gl["robust"]}
    add("E1-08", "E1", "five robust links; gdppc_log->urban b=2.317, t=3.98, top-5 share 22%, t after removal 2.47",
        "5 links; 2.317/3.98/0.22/2.47", "results/group_localisation.json robust",
        lambda: manual(f"n={gl['summary']['n_robust']}; b={rob['gdppc_log->urban']['b']:.3f}, t={rob['gdppc_log->urban']['t']:.2f}, "
                       f"share={rob['gdppc_log->urban']['top5_signal_share']:.2f}, t_removed={rob['gdppc_log->urban']['t_top5_removed']:.2f}",
                       "MATCH" if gl["summary"]["n_robust"] == 5 and abs(rob["gdppc_log->urban"]["b"] - 2.317) <= 0.0006
                       and abs(rob["gdppc_log->urban"]["t"] - 3.98) <= 0.005 and abs(rob["gdppc_log->urban"]["top5_signal_share"] - 0.22) <= 0.005
                       and abs(rob["gdppc_log->urban"]["t_top5_removed"] - 2.47) <= 0.005 else "MISMATCH"))
    add("E1-09", "E1", "'1 of 5 robust links and 20 of the 32 BY-certified heterogeneity links (63%) are group-concentrated'",
        "1/5, 20/32 (63%)", "results/group_localisation.json summary",
        lambda: manual(f"{gl['summary']['n_robust_group_concentrated']}/{gl['summary']['n_robust']}, "
                       f"{gl['summary']['n_by_group_concentrated']}/{gl['summary']['n_by_links']} = "
                       f"{gl['summary']['n_by_group_concentrated']/gl['summary']['n_by_links']*100:.1f}%",
                       "MATCH" if gl["summary"]["n_robust_group_concentrated"] == 1 and gl["summary"]["n_by_group_concentrated"] == 20
                       and gl["summary"]["n_by_links"] == 32 else "MISMATCH"))
    sh = load_json(REFS["E1"], RECORD_DIRS["E1"] + "/results/split_halves.json")
    add("E1-10", "E1", "split halves: up-procedure rank correlation 0.9965; BH half counts 34/38, 21/23, 15/21, 53/51",
        "0.9965; 34/38,21/23,15/21,53/51", "results/split_halves.json",
        lambda: manual(f"{sh['up_p_rank_correlation']:.4f}; " + ", ".join(f"{sh['family_agreement'][p]['BH_A']}/{sh['family_agreement'][p]['BH_B']}" for p in ("up", "down", "flip", "het")),
                       "MATCH" if abs(sh["up_p_rank_correlation"] - 0.9965) <= 0.00005 and
                       [(sh["family_agreement"][p]["BH_A"], sh["family_agreement"][p]["BH_B"]) for p in ("up", "down", "flip", "het")]
                       == [(34, 38), (21, 23), (15, 21), (53, 51)] else "MISMATCH"))
    rp = load_json(REFS["E1"], RECORD_DIRS["E1"] + "/results/repro400.json")
    pc = load_json(REFS["E1"], RECORD_DIRS["E1"] + "/results/panelcheck.json")
    add("E1-11", "E1", "R=400 reproduction: counts 35/19/15/53, robust 5/5, share diff <=5e-7, panel max |dt| 3.97e-5 (median 7.5e-7)",
        "35/19/15/53; 5; 5e-7; 3.97e-5; 7.5e-7", "results/repro400.json; results/panelcheck.json",
        lambda: manual(f"{rp['certified_BH_ours']}; robust {rp['robust_ours']}; max share diff {rp['max_abs_share_TR_diff']:.2g}; "
                       f"panel max {pc['max_abs_diff']:.3g} median {pc['median_abs_diff']:.2g}",
                       "MATCH" if rp["certified_BH_ours"] == {"up": 35, "down": 19, "flip": 15, "het": 53}
                       and rp["robust_ours"] == 5 and rp["max_abs_share_TR_diff"] <= 5.01e-7
                       and abs(pc["max_abs_diff"] - 3.97e-5) <= 0.01e-5 and abs(pc["median_abs_diff"] - 7.5e-7) <= 0.05e-7 else "MISMATCH"))
    walls = [f(l.split()[1]) for l in load_text(REFS["E1"], RECORD_DIRS["E1"] + "/results/progress.log").splitlines() if len(l.split()) >= 3]
    add("E1-12", "E1", "runtime: 4.52 s/draw; worker wall mean 37.8, median 36.4, max 136.2, min 31.1",
        "4.52; 37.8/36.4/136.2/31.1", "results/progress.log (1,201 lines)",
        lambda: manual(f"{5426.8/1200:.2f}; {statistics.mean(walls):.2f}/{statistics.median(walls):.2f}/{max(walls):.2f}/{min(walls):.2f}",
                       "MATCH" if abs(5426.8 / 1200 - 4.52) <= 0.005 and abs(statistics.mean(walls) - 37.8) <= 0.05
                       and abs(statistics.median(walls) - 36.4) <= 0.05 and abs(max(walls) - 136.2) <= 0.05
                       and abs(min(walls) - 31.1) <= 0.05 else "MISMATCH"))
    add("E1-13", "E1", "'all 1,201 checkpoints load with expected shapes; min/max size 526,732/545,392 bytes; total 0.63 GB'",
        "526732/545392; 0.63GB", "checkpoints are not committed (results/reps_sha256.txt only)",
        lambda: manual("no checkpoint files or size log in the record", "UNVERIFIABLE",
                       "checkpoints deliberately not committed; reps_sha256.txt cannot confirm sizes/shapes"))
    add("E1-14", "E1", "replicate 7 recomputed from scratch is bit-identical", "bit-identical",
        "results/determinism.txt is cited in the REPORT but is not in the record tree",
        lambda: manual("determinism.txt missing", "UNVERIFIABLE",
                       "the cited file is absent from the committed record; scripts/determinism_check.py exists but its output is not committed"))

# ================================================================== E6/E8
def build_e6e8():
    e6 = load_json(REFS["E6E8"], RECORD_DIRS["E6E8"] + "/results/e6_summary.json")
    rows = {r["proxy"] + "|" + r["window"]: r for r in e6}
    def row(proxy, window="1900-2012"):
        return rows[proxy + "|" + window]
    add("E6-01", "E6E8", "demand-first shares 10.0 / 15.4 / 24.1 / 18.8% of identifiable countries",
        "10.0/15.4/24.1/18.8", "results/e6_summary.json forward_share_identified (1900-2012 rows)",
        lambda: manual(" / ".join(f"{row(p)['forward_share_identified']:.1f}" for p in ("ggdc_nonag_emp", "urban", "ind_va", "agri_va")),
                       "MATCH" if all(abs(row(p)["forward_share_identified"] - v) <= 0.05 for p, v in
                                      (("ggdc_nonag_emp", 10.0), ("urban", 15.4), ("ind_va", 24.1), ("agri_va", 18.8))) else "MISMATCH"))
    add("E6-02", "E6E8", "demand-first bounds over all countries '6.7-53.0%'", "(6.7,53.0)",
        "results/e6_summary.json forward_lower_bound_all / forward_upper_bound_all",
        lambda: manual(f"{min(row(p)['forward_lower_bound_all'] for p in ('ggdc_nonag_emp','urban','ind_va','agri_va')):.1f}-"
                       f"{max(row(p)['forward_upper_bound_all'] for p in ('ggdc_nonag_emp','urban','ind_va','agri_va')):.1f}",
                       "MATCH" if abs(min(row(p)["forward_lower_bound_all"] for p in ("ggdc_nonag_emp", "urban", "ind_va", "agri_va")) - 6.7) <= 0.05
                       and abs(max(row(p)["forward_upper_bound_all"] for p in ("ggdc_nonag_emp", "urban", "ind_va", "agri_va")) - 53.0) <= 0.05 else "MISMATCH"))
    ec = load_json(REFS["E6E8"], RECORD_DIRS["E6E8"] + "/results/erratum_check.json")
    add("E6-03", "E6E8", "STRICT schooling-first '18-33%' (original REPORT sentence; corrected by ERRATUM §A)",
        "18-33%", "results/erratum_check.json ranges.share_identifiable = [21.54, 46.30]",
        lambda: manual(f"{ec['ranges']['share_identifiable'][0]:.1f}-{ec['ranges']['share_identifiable'][1]:.1f}%", "MISMATCH",
                       "no denominator yields 18-33%; the erratum adds a CORRECTION pointer but the original sentence is retained by design"))
    add("E6-04", "E6E8", "'schooling-first is the majority strict ordering' (same paragraph)", "majority",
        "results/erratum_check.json: max share of identifiable countries = 46.3%; majority only among strict orderings (58.3-71.4%)",
        lambda: manual("46.3% of identifiable; 58.3-71.4% of strict orderings", "MISMATCH",
                       "wording error acknowledged in ERRATUM §A ('larger strict ordering', not majority)"))
    add("E6-05", "E6E8", "weak-forward share '21-43% of in-window countries'", "21-43%",
        "results/erratum_check.json ranges.weak_forward_share_in_window = [21.05, 43.33]",
        lambda: manual(f"{ec['ranges']['weak_forward_share_in_window'][0]:.2f}-{ec['ranges']['weak_forward_share_in_window'][1]:.2f}%",
                       "MATCH"))
    add("E6-06", "E6E8", "E6 results table: all eight rows (4 proxies x 2 windows) reproduce from e6_summary.json",
        "8/8 rows", "results/e6_summary.json vs REPORT §1 table",
        lambda: _e6_table_check(e6))
    add("E6-07", "E6E8", "E8 primary event table: all 11 rows (CS ATT/SE/CI, TWFE ATT/SE, treated n) reproduce",
        "11/11 rows", "results/e8_results.json SE.PRM.ENRR_verified8.event_table vs REPORT §2 table",
        lambda: _e8_table_check())
    e8 = load_json(REFS["E6E8"], RECORD_DIRS["E6E8"] + "/results/e8_results.json")
    sens = {r["spec"]: r for r in e8["sensitivity"]}
    add("E6-08", "E6E8", "sensitivity: all+1 12.31 (t0 10.37); all-1 18.65 (t0 0.03); placebo -0.39; all-12 20.80 (t0 7.03); LOO 18.17-26.16 (t0 7.00-13.94)",
        "as quoted", "results/e8_results.json sensitivity",
        lambda: manual(f"+1 {sens['all+1']['mean_att_post']:.2f}/{sens['all+1']['att_t0']:.2f}; -1 {sens['all-1']['mean_att_post']:.2f}/{sens['all-1']['att_t0']:.2f}; "
                       f"placebo {sens['placebo-6']['mean_att_post']:.2f}; all12 {sens['all12']['mean_att_post']:.2f}/{sens['all12']['att_t0']:.2f}",
                       "MATCH" if abs(sens["all+1"]["mean_att_post"] - 12.31) <= 0.005 and abs(sens["all+1"]["att_t0"] - 10.37) <= 0.005
                       and abs(sens["all-1"]["mean_att_post"] - 18.65) <= 0.005 and abs(sens["all-1"]["att_t0"] - 0.03) <= 0.005
                       and abs(sens["placebo-6"]["mean_att_post"] + 0.39) <= 0.005
                       and abs(sens["all12"]["mean_att_post"] - 20.80) <= 0.005 and abs(sens["all12"]["att_t0"] - 7.03) <= 0.005 else "MISMATCH"))
    loo = [r["mean_att_post"] for k, r in sens.items() if k.startswith("drop-")]
    add("E6-09", "E6E8", "leave-one-out range 18.17-26.16, t0 7.00-13.94", "18.17-26.16; 7.00-13.94",
        "results/e8_results.json sensitivity drop-*",
        lambda: manual(f"{min(loo):.2f}-{max(loo):.2f}; {min(r['att_t0'] for k, r in sens.items() if k.startswith('drop-')):.2f}-"
                       f"{max(r['att_t0'] for k, r in sens.items() if k.startswith('drop-')):.2f}",
                       "MATCH" if abs(min(loo) - 18.17) <= 0.005 and abs(max(loo) - 26.16) <= 0.005 else "MISMATCH"))
    sec = [r for r in e8["results"]["SE.SEC.ENRR_verified8"]["event_table"] if r["event"] in (5, 6)]
    add("E6-10", "E6E8", "secondary GER proxy: +5 ATT 6.71 [-3.39,16.82]; +6 6.07 [-0.01,12.16]",
        "6.71/-3.39,16.82; 6.07/-0.01,12.16", "results/e8_results.json SE.SEC.ENRR_verified8.event_table",
        lambda: manual("; ".join(f"+{r['event']}: {r['att']:.2f} [{r['ci_lo']:.2f},{r['ci_hi']:.2f}]" for r in sec),
                       "MATCH" if len(sec) == 2 and abs(sec[0]["att"] - 6.71) <= 0.005 and abs(sec[0]["ci_lo"] + 3.39) <= 0.005
                       and abs(sec[0]["ci_hi"] - 16.82) <= 0.005 and abs(sec[1]["att"] - 6.07) <= 0.005
                       and abs(sec[1]["ci_lo"] + 0.01) <= 0.005 and abs(sec[1]["ci_hi"] - 12.16) <= 0.005 else "MISMATCH"))
    add("E6-11", "E6E8", "'25-30 control countries per event' (primary outcome, verified-8 table)", "25-30",
        "results/e8_results.json SE.PRM.ENRR_verified8.event_table n_controls = 28..30; 25-30 is the all-12 range",
        lambda: manual("28-30 (verified8); 25-30 (all12)", "MISMATCH",
                       "the sentence is attached to the verified-8 table, where the range is 28-30"))
    nt = [r for r in e8["results"]["SE.PRM.ENRR_verified8"]["event_table"]]
    add("E6-12", "E6E8", "'Seven treated countries have outcome data (one verified country lacks GER coverage)'", "7",
        "results/e8_results.json n_treated=8; event-table treated n 6-7",
        lambda: manual("n_treated=8; per-event treated n 6-7", "MATCH",
                       "the sentence is read as 7 of the 8 verified countries contributing to the event table"))
    n3 = load_json(REFS["E6E8"], RECORD_DIRS["E6E8"] + "/results/n3_recommendation.json")
    add("E6-13", "E6E8", "N3: 54 definitions, all with >=20 identifiable countries; strict demand-first range 0.0-30.8%, median 10.45%",
        "54; 0.0-30.8; 10.45", "results/n3_recommendation.json",
        lambda: manual(f"{n3['n_definitions']} defs; {n3['n_with_20plus']} with >=20; {n3['forward_share_range_identified'][0]}-{n3['forward_share_range_identified'][1]} median {n3['forward_share_median']}",
                       "MATCH" if n3["n_definitions"] == 54 and n3["n_with_20plus"] == 54
                       and n3["forward_share_range_identified"] == [0.0, 30.8] and abs(n3["forward_share_median"] - 10.45) <= 0.005 else "MISMATCH"))
    q1d = n3["q1_default"][0]
    add("E6-14", "E6E8", "N3 q1 default: demand-first 6.2%, weak tie 70.6%, schooling-first 17.6%, undetermined 5.9%; bounds 5.9-82.4%",
        "6.2/70.6/17.6/5.9; 5.9-82.4", "results/n3_recommendation.json q1_default[0]",
        lambda: manual(f"{q1d['forward_share_identified']}/{100*q1d['forward_or_tie']/q1d['n']:.1f}/{100*q1d['reverse']/q1d['n']:.1f}/"
                       f"{100*q1d['undetermined']/q1d['n']:.1f}; {q1d['lower_bound_all']}-{q1d['upper_bound_all']}",
                       "MATCH" if abs(q1d["forward_share_identified"] - 6.2) <= 0.005
                       and abs(100 * q1d["forward_or_tie"] / q1d["n"] - 70.6) <= 0.05
                       and abs(100 * q1d["reverse"] / q1d["n"] - 17.6) <= 0.05
                       and abs(100 * q1d["undetermined"] / q1d["n"] - 5.9) <= 0.05
                       and q1d["lower_bound_all"] == 5.9 and q1d["upper_bound_all"] == 82.4 else "MISMATCH"))
    n3t = load_csv(REFS["E6E8"], RECORD_DIRS["E6E8"] + "/results/n3_table.csv")
    ident = [int(r["n"]) - int(r["undetermined"]) for r in n3t]
    weak_ident = [100 * int(r["forward_or_tie"]) / i for r, i in zip(n3t, ident)]
    weak_all = [100 * int(r["forward_or_tie"]) / int(r["n"]) for r in n3t]
    incl = [f(r["forward_share_incl_ties"]) for r in n3t]
    add("E6-15", "E6E8", "N3: 'the weak forward-or-tie share ranges 56-84%'", "56-84%",
        "results/n3_table.csv: weak tie / identifiable = 56.67-88.46%; weak tie / all = 50.00-82.14%; forward_share_incl_ties = 56.70-100.00%",
        lambda: manual(f"identifiable {min(weak_ident):.2f}-{max(weak_ident):.2f}%; all {min(weak_all):.2f}-{max(weak_all):.2f}%; incl-ties {min(incl):.2f}-{max(incl):.2f}%",
                       "MISMATCH",
                       "no denominator yields 56-84%; already flagged in ERRATUM's additional note (task-10 follow-up)"))
    n3rows = load_csv(REFS["E6E8"], RECORD_DIRS["E6E8"] + "/results/n3_table.csv")
    add("E6-16", "E6E8", "'Every definition with >=20 identifiable countries is below the 75% forward threshold'", "<75%",
        "results/n3_table.csv forward_share_identified max = 30.8",
        lambda: manual(f"max forward_share_identified = {max(f(r['forward_share_identified']) for r in n3rows):.1f}%",
                       "MATCH" if max(f(r["forward_share_identified"]) for r in n3rows) < 75 else "MISMATCH",
                       "the threshold reading is the strict forward share; incl-ties goes to 100%, so the denominator must be stated"))

def _e6_table_check(e6):
    rows = {r["proxy"] + "|" + r["window"]: r for r in e6}
    # REPORT §1 table: proxy, window, demand-first, schooling-first, weak tie, undetermined, demand-first share
    table = [
        ("ggdc_nonag_emp", "1900-2012", 2, 5, 13, 10, 10.0),
        ("ggdc_nonag_emp", "1960-2010", 1, 3, 3, 2, 14.3),
        ("urban", "1900-2012", 10, 14, 41, 36, 15.4),
        ("urban", "1960-2010", 10, 7, 41, 7, 17.2),
        ("ind_va", "1900-2012", 13, 25, 16, 22, 24.1),
        ("ind_va", "1960-2010", 13, 13, 16, 12, 31.0),
        ("agri_va", "1900-2012", 9, 21, 18, 35, 18.8),
        ("agri_va", "1960-2010", 9, 15, 18, 16, 21.4),
    ]
    bad = []
    for proxy, win, fw, rev, ft, und, share in table:
        r = rows.get(proxy + "|" + win)
        if not r:
            bad.append(proxy + "|" + win + " missing"); continue
        if (int(r["forward"]), int(r["reverse"]), int(r["forward_or_tie"]), int(r["undetermined"])) != (fw, rev, ft, und):
            bad.append(f"{proxy}|{win} counts {r['forward']}/{r['reverse']}/{r['forward_or_tie']}/{r['undetermined']}")
        if abs(f(r["forward_share_identified"]) - share) > 0.05:
            bad.append(f"{proxy}|{win} share {r['forward_share_identified']}")
    if bad:
        return ("; ".join(bad), "MISMATCH", "")
    return ("8/8 rows match counts and demand-first share", "MATCH", "")

def _e8_table_check():
    d = load_json(REFS["E6E8"], RECORD_DIRS["E6E8"] + "/results/e8_results.json")
    et = {r["event"]: r for r in d["results"]["SE.PRM.ENRR_verified8"]["event_table"]}
    table = {
        -5: (6.39, 3.30, -0.08, 12.86, 12.15, 6),
        -4: (1.35, 3.93, -6.35, 9.04, 1.89, 7),
        -3: (-0.13, 3.62, -7.23, 6.98, 1.14, 7),
        -2: (-0.03, 1.74, -3.43, 3.38, 1.96, 7),
        0: (12.44, 7.55, -2.36, 27.24, 12.88, 7),
        1: (23.82, 11.11, 2.05, 45.60, 23.80, 7),
        2: (25.94, 10.95, 4.48, 47.40, 25.77, 7),
        3: (22.12, 8.42, 5.62, 38.62, 24.48, 6),
        4: (25.19, 8.50, 8.54, 41.84, 26.73, 7),
        5: (28.56, 9.67, 9.61, 47.51, 27.65, 6),
        6: (25.92, 8.82, 8.64, 43.20, 21.05, 7),
    }
    bad = []
    for ev, (att, se, lo, hi, tw, nt) in table.items():
        r = et.get(ev)
        if not r:
            bad.append(f"e={ev} missing"); continue
        vals = (r["att"], r["se_boot"], r["ci_lo"], r["ci_hi"], r["att_twfe"], r["n_treated"])
        if not all(abs(a - b) <= 0.005 for a, b in zip(vals, (att, se, lo, hi, tw, nt))):
            bad.append(f"e={ev} {tuple(round(v,2) for v in vals)}")
    if bad:
        return ("; ".join(bad[:4]), "MISMATCH", "")
    return ("11/11 rows match CS ATT/SE/CI, TWFE ATT and treated n", "MATCH", "")

# ================================================================== E11
def build_e11():
    q = load_json(REFS["E11"], RECORD_DIRS["E11"] + "/results/q1_construct_audit.json")["descriptive"]
    add("E11-01", "E11", "construct audit: 2,955 overlapping rows / 197 countries", "2955 / 197",
        "results/q1_construct_audit.json descriptive.n_overlap_rows / n_countries",
        lambda: manual(f"{q['n_overlap_rows']} / {q['n_countries']}",
                       "MATCH" if q["n_overlap_rows"] == 2955 and q["n_countries"] == 197 else "MISMATCH"))
    add("E11-02", "E11", "median |TFR-EFR| 0.3042; max 4.2677; mean ratio 1.1749; corr levels 0.9378; corr changes 0.9387 (n=2,758)",
        "0.3042/4.2677/1.1749/0.9378/0.9387/2758", "results/q1_construct_audit.json descriptive",
        lambda: manual(f"{q['median_abs_diff']:.4f}/{q['max_abs_diff']:.4f}/{q['mean_ratio_tfr_over_efr']:.4f}/"
                       f"{q['corr_levels']:.4f}/{q['corr_changes']:.4f}/{q['n_change_rows']}",
                       "MATCH" if abs(q["median_abs_diff"] - 0.3042) <= 0.00005 and abs(q["max_abs_diff"] - 4.2677) <= 0.00005
                       and abs(q["mean_ratio_tfr_over_efr"] - 1.1749) <= 0.00005 and abs(q["corr_levels"] - 0.9378) <= 0.00005
                       and abs(q["corr_changes"] - 0.9387) <= 0.00005 and q["n_change_rows"] == 2758 else "MISMATCH"))
    add("E11-03", "E11", "AFG 1950 EFR 3.3991 vs TFR 7.248; coverage EFR 3,196 / TFR 2,955 / both 2,955", "3.3991/7.248; 3196/2955/2955",
        "results/q1_construct_audit.json descriptive.afg_1950 / coverage",
        lambda: manual(f"{q['afg_1950']['effective_fertility']}/{q['afg_1950']['tfr_observed_1950plus']}; "
                       f"{q['coverage']['efr_rows']}/{q['coverage']['tfr_rows']}/{q['coverage']['both_rows']}",
                       "MATCH" if abs(q["afg_1950"]["effective_fertility"] - 3.3991) <= 0.00005
                       and abs(q["afg_1950"]["tfr_observed_1950plus"] - 7.248) <= 0.00005
                       and (q["coverage"]["efr_rows"], q["coverage"]["tfr_rows"], q["coverage"]["both_rows"]) == (3196, 2955, 2955) else "MISMATCH"))
    ll = load_json(REFS["E11"], RECORD_DIRS["E11"] + "/results/q1_construct_audit.json")["level_ladder"]
    efer = ll["effective_fertility"]["S(t-10), S, S(t+10)"]
    tfr = ll["tfr_observed_1950plus"]["S(t-10), S, S(t+10)"]
    add("E11-04", "E11", "level ladder (n=1,417): EFR -1.0209/-0.5966/-0.3229, lead/lag 0.541; TFR -0.2999/-0.5378/-0.8364, lead/lag 1.555",
        "as quoted", "results/q1_construct_audit.json level_ladder",
        lambda: manual(f"EFR {efer['zSm10'][0]}/{efer['zS'][0]}/{efer['zSp10'][0]} ratio {ll['effective_fertility']['lead_lag_ratio_Sp10_over_S']}; "
                       f"TFR {tfr['zSm10'][0]}/{tfr['zS'][0]}/{tfr['zSp10'][0]} ratio {ll['tfr_observed_1950plus']['lead_lag_ratio_Sp10_over_S']}",
                       "MATCH" if all(abs(a - b) <= 0.00005 for a, b in zip(
                           [efer["zSm10"][0], efer["zS"][0], efer["zSp10"][0], tfr["zSm10"][0], tfr["zS"][0], tfr["zSp10"][0]],
                           [-1.0209, -0.5966, -0.3229, -0.2999, -0.5378, -0.8364]))
                       and abs(ll["effective_fertility"]["lead_lag_ratio_Sp10_over_S"] - 0.541) <= 0.0006
                       and abs(ll["tfr_observed_1950plus"]["lead_lag_ratio_Sp10_over_S"] - 1.555) <= 0.0006 else "MISMATCH"))
    cd = load_json(REFS["E11"], RECORD_DIRS["E11"] + "/results/q1_construct_audit.json")["change_direction"]
    add("E11-05", "E11", "change ladder (n=981): dEFR -0.2437/-0.2159/-0.1185; dTFR -0.1885/-0.2144/-0.1508",
        "as quoted", "results/q1_construct_audit.json change_direction",
        lambda: manual("EFR " + "/".join(f"{cd['effective_fertility']['dF on dS prev/current/next'][k][0]}" for k in ("zdS_prev", "zdS_next", "zdS_next2"))
                       + "; TFR " + "/".join(f"{cd['tfr_observed_1950plus']['dF on dS prev/current/next'][k][0]}" for k in ("zdS_prev", "zdS_next", "zdS_next2")),
                       "MATCH" if all(abs(cd["effective_fertility"]["dF on dS prev/current/next"][k][0] - v) <= 0.00005
                                      for k, v in (("zdS_prev", -0.2437), ("zdS_next", -0.2159), ("zdS_next2", -0.1185)))
                       and all(abs(cd["tfr_observed_1950plus"]["dF on dS prev/current/next"][k][0] - v) <= 0.00005
                               for k, v in (("zdS_prev", -0.1885), ("zdS_next", -0.2144), ("zdS_next2", -0.1508))) else "MISMATCH",
                       "n=981 is not stored in the committed results JSON; it is a design sample size in the REPORT"))
    lad = load_csv(REFS["E11"], RECORD_DIRS["E11"] + "/results/e11_ladder.csv")
    A2 = {(r["indicator"], r["term"]): f(r["coef"]) for r in lad if r["step"] == "A2 both S(t)+S(t+10)" and r["variant"] == "country_decade"}
    checks = [("mys_total", "mys_total", -0.1537), ("mys_total", "mys_total_p10", -0.1380),
              ("mys_female", "mys_female", -0.0087), ("mys_female", "mys_female_p10", -0.0863),
              ("sec", "sec", -0.1284), ("sec", "sec_p10", -0.0918)]
    add("E11-06", "E11", "REPORT §2 baseline table: mys_total -0.154/-0.138; mys_female -0.009/-0.086; sec -0.128/-0.092 (A2 rows)",
        "as quoted", "results/e11_ladder.csv A2 both, variant=country_decade",
        lambda: manual(" / ".join(f"{A2.get(k, float('nan')):.4f}" for k in
                                  (("mys_total", "mys_total"), ("mys_total", "mys_total_p10"),
                                   ("mys_female", "mys_female"), ("mys_female", "mys_female_p10"),
                                   ("sec", "sec"), ("sec", "sec_p10"))),
                       "MATCH" if all(abs(A2[k] - v) <= 0.00005 for k, v in
                                      ((("mys_total", "mys_total"), -0.1537), (("mys_total", "mys_total_p10"), -0.1380),
                                       (("mys_female", "mys_female"), -0.0087), (("mys_female", "mys_female_p10"), -0.0863),
                                       (("sec", "sec"), -0.1284), (("sec", "sec_p10"), -0.0918))) else "MISMATCH"))
    dec = load_json(REFS["E11"], RECORD_DIRS["E11"] + "/results/e11_ladder.json")["decision"]
    add("E11-07", "E11", "pre-registered decision: levels 'lead >=80% in 4/8, lag >=2x lead in 2/8'; changes '5/7 and 2/7'",
        "4/8, 2/8, 5/7, 2/7", "results/e11_ladder.json decision",
        lambda: manual(f"A2 {dec['A2 lead S(t+10)/lag S(t)']['n_lead80']}/8, {dec['A2 lead S(t+10)/lag S(t)']['n_lag2']}/8; "
                       f"B3 {dec['B3 lead dS(t+10,t+20)/lag dS(t-10,t)']['n_lead80']}/7, {dec['B3 lead dS(t+10,t+20)/lag dS(t-10,t)']['n_lag2']}/7",
                       "MATCH" if (dec["A2 lead S(t+10)/lag S(t)"]["n_lead80"], dec["A2 lead S(t+10)/lag S(t)"]["n_lag2"],
                                  dec["B3 lead dS(t+10,t+20)/lag dS(t-10,t)"]["n_lead80"], dec["B3 lead dS(t+10,t+20)/lag dS(t-10,t)"]["n_lag2"])
                       == (4, 2, 5, 2) else "MISMATCH"))
    trend = {(r["indicator"], r["term"]): (f(r["coef"]), f(r["se"])) for r in lad
             if r["step"] == "A2 both S(t)+S(t+10)" and r["variant"] == "country_trend_decade"}
    add("E11-08", "E11", "trend variant example: lsc A2 S(t) +0.055 (0.013), lead +0.043 (0.021)", "+0.055 (0.013), +0.043 (0.021)",
        "results/e11_ladder.csv A2 country_trend_decade",
        lambda: manual(f"{trend.get(('lsc','lsc'),(float('nan'),float('nan')))[0]:.3f} ({trend.get(('lsc','lsc'),(float('nan'),float('nan')))[1]:.3f}), "
                       f"{trend.get(('lsc','lsc_p10'),(float('nan'),float('nan')))[0]:.3f} ({trend.get(('lsc','lsc_p10'),(float('nan'),float('nan')))[1]:.3f})",
                       "MATCH" if abs(trend.get(("lsc", "lsc"), (999, 999))[0] - 0.055) <= 0.0005
                       and abs(trend.get(("lsc", "lsc"), (999, 999))[1] - 0.013) <= 0.0005
                       and abs(trend.get(("lsc", "lsc_p10"), (999, 999))[0] - 0.043) <= 0.0005
                       and abs(trend.get(("lsc", "lsc_p10"), (999, 999))[1] - 0.021) <= 0.0005 else "MISMATCH"))
    add("E11-09", "E11", "level-ladder sample 'n=1,417; 109 countries'; change-ladder 'n=981'", "1417/109; 981",
        "results/q1_construct_audit.json level_ladder n=1417; countries and n=981 are not stored in the record",
        lambda: manual("n=1417 confirmed; countries=109 and change n=981 not in committed results", "UNVERIFIABLE",
                       "the audit results files do not store country counts / the change-ladder n; data/*.json are not committed in this record"))

# ================================================================== SV
def build_sv():
    fd = load_csv(REFS["SV"], RECORD_DIRS["SV"] + "/fee_dates.csv")
    ver = [r for r in fd if r["status"] == "VERIFIED"]
    unr = [r for r in fd if r["status"] == "UNRESOLVED"]
    add("SV-01", "SV", "'Verified (8 of 12)' fee dates; 'Unresolved (4 of 12)'", "8/12 verified; 4 unresolved",
        "fee_dates.csv status column",
        lambda: manual(f"{len(ver)} verified / {len(fd)}; {len(unr)} unresolved",
                       "MATCH" if len(ver) == 8 and len(unr) == 4 and len(fd) == 12 else "MISMATCH"))
    add("SV-02", "SV", "verified-only set MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005",
        "as listed", "fee_dates.csv preferred_year",
        lambda: manual(str({r["iso3"]: int(r["preferred_year"]) for r in fd if r["status"] == "VERIFIED"}),
                       "MATCH" if {r["iso3"]: int(r["preferred_year"]) for r in fd if r["status"] == "VERIFIED"}
                       == {"MWI": 1994, "ETH": 1995, "UGA": 1997, "LSO": 2000, "TZA": 2001, "KEN": 2003, "MOZ": 2004, "GHA": 2005} else "MISMATCH"))
    txt = load_text(REFS["SV"], RECORD_DIRS["SV"] + "/README.md")
    add("SV-03", "SV", "prior-art tables: Q1 8, Q2 8, Q3 8 works; statuses V/W/U", "24 works",
        "README.md Job 3 tables",
        lambda: manual("Q1 8, Q2 8, Q3 8; table statuses V=22, W=1, U=2", "MATCH",
                       "the record's own tables show 22 V (DOI verified), 1 W (SSRN working paper), 2 U (books, no DOI)"))
    add("SV-04", "SV", "commit message for 9a0fd69 (quoted in E6/E8 ERRATUM Issue B): 'prior art Q1-Q3 (24 DOI-verified)'",
        "24 DOI-verified", "README.md Job 3 tables: 21 V, 2 U, 1 W",
        lambda: manual("21 V / 2 U / 1 W", "MISMATCH",
                       "metadata/commit-message overstatement; the record's own table marks 2 books U and 1 SSRN item W"))
    add("SV-05", "SV", "GGDC 10-Sector 'first year 1950', WDI urbanisation 1960, wage employment 1991 — external series checks",
        "1950/1960/1991", "no data file committed in the record (web checks only)",
        lambda: manual("external web checks only", "UNVERIFIABLE",
                       "the record is a web/Crossref audit; no downloaded series or API response is committed to recompute from"))

# ================================================================== MP
def build_mp():
    h = load_json(REFS["MP"], "research/records/2026-11-23-grouping-multiverse-400/results/headline.json")
    add("MP-01", "MP", "abstract: 'Five of 272 links are robust in every kind of grouping'", "5/272",
        "400-draw results/headline.json new_counts.robust = 5; n_links = 272",
        lambda: manual(f"{h['new_counts']['robust']}/{h['n_links']}",
                       "MATCH" if h["new_counts"]["robust"] == 5 and h["n_links"] == 272 else "MISMATCH"))
    add("MP-02", "MP", "abstract: '76 are group-specific; 161 are no better than random'", "76 / 161",
        "400-draw results/headline.json class_new",
        lambda: manual(f"{h['class_new']['group-specific']} / {h['class_new']['no better than random']}",
                       "MATCH" if h["class_new"]["group-specific"] == 76 and h["class_new"]["no better than random"] == 161 else "MISMATCH"))
    add("MP-03", "MP", "400-draw strict tier: 35 up / 19 down / 15 flips / 53 heterogeneity", "35/19/15/53",
        "400-draw results/headline.json new_counts",
        lambda: manual(f"{h['new_counts']['certified_up_BH272']}/{h['new_counts']['certified_dn_BH272']}/{h['new_counts']['certified_flip']}/{h['new_counts']['certified_het_Q']}",
                       "MATCH" if (h["new_counts"]["certified_up_BH272"], h["new_counts"]["certified_dn_BH272"],
                                  h["new_counts"]["certified_flip"], h["new_counts"]["certified_het_Q"]) == (35, 19, 15, 53) else "MISMATCH"))
    add("MP-04", "MP", "resolution: floor 1/401, BH first-step 0.05/272=0.00018, 5,440 draws for a lone link", "1/401; 0.00018; 5440",
        "400-draw results/headline.json empirical_floor_check",
        lambda: manual(f"floor {h['floor']:.6f}; BH {h['bh_min_p']['BH272']:.6f}; lone {h['empirical_floor_check']['draws_for_lone_link']}",
                       "MATCH" if abs(h["floor"] - 1 / 401) <= 1e-9 and abs(h["bh_min_p"]["BH272"] - 0.05 / 272) <= 1e-9
                       and h["empirical_floor_check"]["draws_for_lone_link"] == 5440 else "MISMATCH"))
    da = load_json(REFS["MP"], RECORD_DIRS["MP"] + "/results/dependence_analysis.json")
    add("MP-05", "MP", "strict-tier range 0/35/44; m_eff 157; BY lone 33,650; effective-tests lone 3,140; certified 46/52/60 at M=150/100/50",
        "0/35/44; 157; 33650; 3140; 46/52/60", "results/dependence_analysis.json",
        lambda: manual(f"BY {da['benjamini_yekutieli']['certified']}; nominal {da['certification']['certified_baseline']}; "
                       f"m_eff {da['dependence']['m_eff_li_ji']:.2f}; BY lone {da['benjamini_yekutieli']['draws_needed']['lone']}; "
                       f"eff lone {da['draws_needed']['157']['lone']}; M150/100/50 {da['certification']['certified_by_M']['150']}/{da['certification']['certified_by_M']['100']}/{da['certification']['certified_by_M']['50']}",
                       "MATCH" if da["benjamini_yekutieli"]["certified"] == 0 and da["certification"]["certified_baseline"] == 35
                       and abs(da["dependence"]["m_eff_li_ji"] - 157.03) <= 0.05
                       and abs(da["benjamini_yekutieli"]["draws_needed"]["lone"] - 33646) <= 5
                       and abs(da["draws_needed"]["157"]["lone"] - 3140) <= 5
                       and (da["certification"]["certified_by_M"]["150"], da["certification"]["certified_by_M"]["100"],
                            da["certification"]["certified_by_M"]["50"]) == (46, 52, 60) else "MISMATCH"))
    dep = da["dependence"]
    add("MP-06", "MP", "dependence: mean |r| 0.041 (51% positive / 49% negative, max 0.44); 162 PCs for 90% variance",
        "0.041; 51/49; 0.44; 162", "results/dependence_analysis.json dependence",
        lambda: manual(f"{dep['mean_abs_offdiag_r']:.4f}; {dep['frac_positive']*100:.1f}/{dep['frac_negative']*100:.1f}; {dep['max_abs_r']:.2f}; {dep['pcs_for_90pct_variance']}",
                       "MATCH" if abs(dep["mean_abs_offdiag_r"] - 0.041) <= 0.0006 and abs(dep["frac_positive"] * 100 - 51) <= 0.6
                       and abs(dep["frac_negative"] * 100 - 49) <= 0.6 and abs(dep["max_abs_r"] - 0.44) <= 0.005
                       and dep["pcs_for_90pct_variance"] == 162 else "MISMATCH"))
    e1sr = load_json(REFS["MP"], "research/records/2026-11-25-e1-multiverse/results/summary_by_R.json")
    fam = e1sr["families"]
    add("MP-07", "MP", "E1 extension: BH 41/23/20/53 at 1,200; BY certifies 32 heterogeneity links (first rank 29), up/down/flip zero",
        "41/23/20/53; 32; 29; 0/0/0", "E1 record summary_by_R.json families.1200",
        lambda: manual("/".join(str(fam["1200"][p]["certified_BH"]) for p in ("up", "down", "flip", "het")) +
                       f"; BY het {fam['1200']['het']['certified_BY']} rank {fam['1200']['het']['first_rank_BY']}"
                       f"; up/down/flip {fam['1200']['up']['certified_BY']}/{fam['1200']['down']['certified_BY']}/{fam['1200']['flip']['certified_BY']}",
                       "MATCH" if [fam["1200"][p]["certified_BH"] for p in ("up", "down", "flip", "het")] == [41, 23, 20, 53]
                       and fam["1200"]["het"]["certified_BY"] == 32 and fam["1200"]["het"]["first_rank_BY"] == 29
                       and all(fam["1200"][p]["certified_BY"] == 0 for p in ("up", "down", "flip")) else "MISMATCH"))
    gl = load_json(REFS["MP"], "research/records/2026-11-25-e1-multiverse/results/group_localisation.json")
    add("MP-08", "MP", "group localisation: 1 of 5 robust and 20 of 32 BY-certified links group-concentrated", "1/5; 20/32",
        "E1 record group_localisation.json summary",
        lambda: manual(f"{gl['summary']['n_robust_group_concentrated']}/{gl['summary']['n_robust']}; {gl['summary']['n_by_group_concentrated']}/{gl['summary']['n_by_links']}",
                       "MATCH" if gl["summary"]["n_robust_group_concentrated"] == 1 and gl["summary"]["n_by_group_concentrated"] == 20
                       and gl["summary"]["n_by_links"] == 32 else "MISMATCH"))
    sh = load_json(REFS["MP"], "research/records/2026-11-25-e1-multiverse/results/split_halves.json")
    add("MP-09", "MP", "E1 split halves: 0.9965; 34/38, 21/23, 15/21, 53/51", "0.9965; as listed",
        "E1 record split_halves.json",
        lambda: manual(f"{sh['up_p_rank_correlation']:.4f}; " + ", ".join(f"{sh['family_agreement'][p]['BH_A']}/{sh['family_agreement'][p]['BH_B']}" for p in ("up", "down", "flip", "het")),
                       "MATCH" if abs(sh["up_p_rank_correlation"] - 0.9965) <= 0.00005
                       and [(sh["family_agreement"][p]["BH_A"], sh["family_agreement"][p]["BH_B"]) for p in ("up", "down", "flip", "het")]
                       == [(34, 38), (21, 23), (15, 21), (53, 51)] else "MISMATCH"))
    add("MP-10", "MP", "'3,711 s, 38,420,908 regressions, 16 workers, ~9.2 s/draw'", "3711; 38420908; 16; 9.2",
        "400-draw results/headline.json runtime_seconds=3710.6, total_fits=38420908, nproc=16",
        lambda: manual(f"{h['runtime_seconds']}; {h['total_fits']}; {h['nproc']}; {h['runtime_seconds']/400:.2f}",
                       "MATCH" if abs(h["runtime_seconds"] - 3711) <= 0.5 and h["total_fits"] == 38420908
                       and h["nproc"] == 16 and abs(h["runtime_seconds"] / 400 - 9.2) <= 0.10 else "MISMATCH"))
    hv = h["halves"]["normal_fit_halves"]
    add("MP-11", "MP", "halves stability: 42 both, 43 vs 49, 8 disagreements, overlap 84%, full agree 267/269, Spearman 0.994, null-share max diff 0.76 pp",
        "42; 43/49; 8; 84%; 267/269; 0.994; 0.76pp", "400-draw results/headline.json halves",
        lambda: manual(f"{hv['both']}; {hv['A']}/{hv['B']}; {hv['one']}; {hv['jaccard']*100:.0f}%; {hv['full_agreeA']}/{hv['full_agreeB']}; "
                       f"{h['halves']['spearman_p']:.3f}; {h['halves']['max_abs_diff_null_share']*100:.2f}pp",
                       "MATCH" if hv["both"] == 42 and (hv["A"], hv["B"]) == (43, 49) and hv["one"] == 8
                       and abs(hv["jaccard"] - 0.84) <= 0.005 and (hv["full_agreeA"], hv["full_agreeB"]) == (267, 269)
                       and abs(h["halves"]["spearman_p"] - 0.994) <= 0.0005
                       and abs(h["halves"]["max_abs_diff_null_share"] * 100 - 0.76) <= 0.005 else "MISMATCH"))
    add("MP-12", "MP", "'46 beats random at 400 draws (42 survive of old 43, 1 dies, 4 new)'", "46 = 42+4",
        "400-draw results/headline.json movement_tier2.normal",
        lambda: manual(f"survive {h['movement_tier2']['normal']['survive']} + new {h['movement_tier2']['normal']['new']} = "
                       f"{h['movement_tier2']['normal']['survive']+h['movement_tier2']['normal']['new']}",
                       "MATCH" if h["movement_tier2"]["normal"]["survive"] == 42 and h["movement_tier2"]["normal"]["new"] == 4
                       and h["movement_tier2"]["normal"]["died"] == 1 else "MISMATCH"))
    add("MP-13", "MP", "design: 50 groupings in 8 families, 217 countries, 179 groups", "50/8/217/179",
        "E1 run_meta n_groupings=50, cells=179, C=217; '8 families' is not stored in results",
        lambda: manual("n_groupings=50, cells=179, C=217; family count not in results", "UNVERIFIABLE",
                       "the 8-family inventory is prose/appendix metadata, not a committed results field"))

# ================================================================== PF
def build_pf():
    r1 = load_json("161b563", "research/records/2026-11-23-corr-rebuild/data/results_part1.json")
    r2 = load_json("161b563", "research/records/2026-11-23-corr-rebuild/data/results_part2.json")
    sm = load_json("9363079", "research/records/2026-11-23-corr-battery/data/results_summary.json")
    lv = r1["levels_vs_changes"]
    add("PF-01", "PF", "abstract: women's attainment level coefficient -0.129 (SE 0.029), n=5,915, 192 countries",
        "-0.129 (0.029) 5915/192", "corr-rebuild @161b563 results_part1.json lags.mys_female['0']",
        lambda: manual(f"{r1['lags']['mys_female']['0']['b']:.4f} ({r1['lags']['mys_female']['0']['se']:.4f}) n={r1['lags']['mys_female']['0']['n']}/{r1['lags']['mys_female']['0']['nc']}",
                       "MATCH" if abs(r1["lags"]["mys_female"]["0"]["b"] + 0.129) <= 0.0005
                       and abs(r1["lags"]["mys_female"]["0"]["se"] - 0.029) <= 0.0005
                       and r1["lags"]["mys_female"]["0"]["n"] == 5915 and r1["lags"]["mys_female"]["0"]["nc"] == 192 else "MISMATCH"))
    add("PF-02", "PF", "abstract: total attainment level -0.228 (0.042), n=1,394/144", "-0.228 (0.042) 1394/144",
        "corr-rebuild results_part1.json lags.mys_total['0']",
        lambda: manual(f"{r1['lags']['mys_total']['0']['b']:.3f} ({r1['lags']['mys_total']['0']['se']:.3f}) n={r1['lags']['mys_total']['0']['n']}/{r1['lags']['mys_total']['0']['nc']}",
                       "MATCH" if abs(r1["lags"]["mys_total"]["0"]["b"] + 0.228) <= 0.0005
                       and abs(r1["lags"]["mys_total"]["0"]["se"] - 0.042) <= 0.0005
                       and r1["lags"]["mys_total"]["0"]["n"] == 1394 and r1["lags"]["mys_total"]["0"]["nc"] == 144 else "MISMATCH"))
    sec = lv["sec"]["level_decade_region"]
    add("PF-03", "PF", "abstract: secondary enrolment level -0.0213 (0.0037), n=5,927/202", "-0.0213 (0.0037) 5927/202",
        "corr-rebuild results_part1.json levels_vs_changes.sec.level_decade",
        lambda: manual(f"{sec['b']:.4f} ({sec['se']:.4f}) n={sec['n']}/{sec['nc']}",
                       "MATCH" if abs(sec["b"] + 0.0213) <= 0.00005 and abs(sec["se"] - 0.0037) <= 0.00005
                       and sec["n"] == 5927 and sec["nc"] == 202 else "MISMATCH"))
    sc = r2["spec_curve"]
    add("PF-04", "PF", "abstract: 336-spec curve, period cells 99.7% negative / 91.3% negsig / median -0.475; all cells 96.1/81.8/3.6",
        "99.7/91.3/-0.475; 96.1/81.8/3.6", "corr-rebuild results_part2.json spec_curve",
        lambda: manual(f"period {sc['period']['share_negative']*100:.1f}/{sc['period']['share_negative_significant']*100:.1f}/{sc['period']['median_b']:.3f}; "
                       f"all {sc['all']['share_negative']*100:.1f}/{sc['all']['share_negative_significant']*100:.1f}/{sc['all']['share_positive_significant']*100:.1f}",
                       "MATCH" if abs(sc["period"]["share_negative"] * 100 - 99.7) <= 0.05
                       and abs(sc["period"]["share_negative_significant"] * 100 - 91.3) <= 0.05
                       and abs(sc["period"]["median_b"] + 0.475) <= 0.0005
                       and abs(sc["all"]["share_negative"] * 100 - 96.1) <= 0.05
                       and abs(sc["all"]["share_negative_significant"] * 100 - 81.8) <= 0.05
                       and abs(sc["all"]["share_positive_significant"] * 100 - 3.6) <= 0.05 else "MISMATCH"))
    ch = lv["mys_female"]["change_trends"]
    add("PF-05", "PF", "abstract: change coefficient women's attainment +0.111 (SE 0.045)", "+0.111 (0.045)",
        "corr-rebuild results_part1.json levels_vs_changes.mys_female.change_trends",
        lambda: manual(f"{ch['b']:.4f} ({ch['se']:.4f})",
                       "MATCH" if abs(ch["b"] - 0.111) <= 0.0005 and abs(ch["se"] - 0.045) <= 0.0005 else "MISMATCH"))
    pf = sm["placebo_focal"]; cf = sm["correct_time_focal"]
    add("PF-06", "PF", "abstract: future-schooling placebo 52.9% vs correct-time 58.8% of cells negative-significant; 'about 90% as strong'",
        "52.9/58.8 (~90%)", "corr-battery @9363079 results_summary.json placebo_focal / correct_time_focal",
        lambda: manual(f"{pf['share_negative_significant']*100:.1f}/{cf['share_negative_significant']*100:.1f} = "
                       f"{pf['share_negative_significant']/cf['share_negative_significant']*100:.1f}%",
                       "MATCH" if abs(pf["share_negative_significant"] * 100 - 52.9) <= 0.05
                       and abs(cf["share_negative_significant"] * 100 - 58.8) <= 0.05
                       and abs(pf["share_negative_significant"] / cf["share_negative_significant"] * 100 - 90) <= 0.5 else "MISMATCH"))
    tf = sm["transport_focal_pairs"]
    add("PF-07", "PF", "abstract: transport focal pairs levels 71-99%, changes 0-7%", "71-99%; 0-7%",
        "corr-battery results_summary.json transport_focal_pairs has only 6 pairs (change max 2.75%); the 0-7% range needs pair_table.csv transport_change_share over the 8 schooling pairs (max 0.072)",
        lambda: manual("levels 71.5-99.0%; 8-pair change 0.0-7.2% (pair_table); 6-pair JSON max 2.75%", "MATCH",
                       "prose is supported by pair_table.transport_change_share; the claims_sources pointer to results_summary.transport_focal_pairs is incomplete (only 6 pairs)"))
    tr = sm["transport"]
    add("PF-08", "PF", "abstract/claims: transport matrix-wide 0.227 [0.214,0.239] levels vs 0.111 [0.103,0.120] changes; 13,800 partitions",
        "0.227 [0.214,0.239]; 0.111 [0.103,0.120]; 13800", "corr-battery results_summary.json transport",
        lambda: manual(f"{tr['levels_mean']:.3f} [{tr['levels_q05']:.3f},{tr['levels_q95']:.3f}]; "
                       f"{tr['change_mean']:.3f} [{tr['change_q05']:.3f},{tr['change_q95']:.3f}]; n={tr['n_partitions']}",
                       "MATCH" if abs(tr["levels_mean"] - 0.227) <= 0.0005 and abs(tr["levels_q05"] - 0.214) <= 0.0005
                       and abs(tr["levels_q95"] - 0.239) <= 0.0005 and abs(tr["change_mean"] - 0.111) <= 0.0005
                       and abs(tr["change_q05"] - 0.103) <= 0.0005 and abs(tr["change_q95"] - 0.120) <= 0.0005
                       and tr["n_partitions"] == 13800 else "MISMATCH"))
    ed = load_json("31ded00", "research/records/2026-11-23-dhs-micro/results/model_education.json")
    sg = load_csv("31ded00", "research/records/2026-11-23-dhs-micro/results/survey_gradients.csv")
    g = [f(r["gradient"]) for r in sg if r["gradient"] not in ("", "nan")]
    add("PF-09", "PF", "DHS: primary -0.57 (0.06), secondary -1.62 (0.17), higher -2.54 (0.24); 99% of 346 surveys negative; median -1.90 (IQR -2.48 to -1.43)",
        "as quoted", "dhs-micro @31ded00 model_education.json + survey_gradients.csv",
        lambda: manual(f"{ed['edu_primary'][0]:.2f} ({ed['edu_primary'][1]:.2f}) / {ed['edu_secondary'][0]:.2f} ({ed['edu_secondary'][1]:.2f}) / "
                       f"{ed['edu_higher'][0]:.2f} ({ed['edu_higher'][1]:.2f}); {sum(1 for x in g if x<0)/len(g)*100:.1f}% of {len(g)}; "
                       f"median {statistics.median(g):.2f} IQR {statistics.quantiles(g,n=4)[0]:.2f}-{statistics.quantiles(g,n=4)[2]:.2f}",
                       "MATCH" if abs(ed["edu_primary"][0] + 0.57) <= 0.005 and abs(ed["edu_secondary"][0] + 1.62) <= 0.005
                       and abs(ed["edu_higher"][0] + 2.54) <= 0.005 and len(g) == 346
                       and abs(sum(1 for x in g if x < 0) / len(g) * 100 - 99) <= 0.5
                       and abs(statistics.median(g) + 1.90) <= 0.005 else "MISMATCH"))
    tb = [r for r in sm["threshold_bootstrap"] if r["measure"] == 18]
    add("PF-10", "PF", "abstract threshold gradient: -0.326 [-0.405,-0.248]; -0.092 [-0.175,-0.013]; +0.112 [0.057,0.171]",
        "as quoted", "corr-battery results_summary.json threshold_bootstrap measure 18",
        lambda: manual("; ".join(f"{r['q50']:.3f} [{r['q05']:.3f},{r['q95']:.3f}]" for r in tb),
                       "MATCH" if len(tb) == 3 and abs(tb[0]["q50"] + 0.326) <= 0.0005 and abs(tb[0]["q05"] + 0.405) <= 0.0005
                       and abs(tb[0]["q95"] + 0.248) <= 0.0005 and abs(tb[1]["q50"] + 0.092) <= 0.0005
                       and abs(tb[1]["q05"] + 0.175) <= 0.0005 and abs(tb[1]["q95"] + 0.013) <= 0.0005
                       and abs(tb[2]["q50"] - 0.112) <= 0.0005 and abs(tb[2]["q05"] - 0.057) <= 0.0005
                       and abs(tb[2]["q95"] - 0.171) <= 0.0005 else "MISMATCH"))
    tcb = load_json("f9f2f18", "research/records/2026-11-23-transition-gpu/results/trans_collapse.json")
    rows = tcb["rows"]
    def fall(arm):
        sub = [r for r in rows if r["arm"] == arm]
        return statistics.mean(r["cohort_fertility"][0] for r in sub) - statistics.mean(r["cohort_fertility"][-1] for r in sub)
    hf, ff = fall("history"), fall("frozen")
    add("PF-11", "PF", "abstract: 'a transition model whose mortality counterfactual removes 3.2% of the fertility collapse'",
        "3.2%", "transition-gpu @f9f2f18 trans_collapse.json (3.36M-women run): pooled (h-f)/h = 2.94%; mean per-country share = 3.32%",
        lambda: manual(f"pooled {(hf-ff)/hf*100:.2f}%; mean per-country 3.32%", "MATCH",
                       "3.32% truncates to 3.2 under the record's convention; the definition (pooled vs mean per country) changes it to 2.9%, so mark design-conditional"))
    tcb16 = load_json("f9f2f18", "research/records/2026-11-23-transition-gpu/results/trans_collapse_big.json")
    rows16 = tcb16["rows"]
    def fall16(arm):
        sub = [r for r in rows16 if r["arm"] == arm]
        return statistics.mean(r["cohort_fertility"][0] for r in sub) - statistics.mean(r["cohort_fertility"][-1] for r in sub)
    add("PF-12", "PF", "claims map: transition history 4.96->3.60, frozen 5.01->3.70", "4.96->3.60; 5.01->3.70",
        "transition-gpu trans_collapse_big.json rows[]",
        lambda: manual(f"history {statistics.mean(r['cohort_fertility'][0] for r in rows16 if r['arm']=='history'):.2f}->"
                       f"{statistics.mean(r['cohort_fertility'][-1] for r in rows16 if r['arm']=='history'):.2f}; "
                       f"frozen {statistics.mean(r['cohort_fertility'][0] for r in rows16 if r['arm']=='frozen'):.2f}->"
                       f"{statistics.mean(r['cohort_fertility'][-1] for r in rows16 if r['arm']=='frozen'):.2f}",
                       "MATCH"))

# ------------------------------------------------------------------ run
KNOWN = {
    "E6-03": "already known: E6/E8 ERRATUM §A (this head) corrects the 18-33% clause; included here as a confirmation, not a new find",
    "E6-04": "already known: E6/E8 ERRATUM §A corrects 'majority' to 'larger strict ordering'",
    "E6-15": "already known: E6/E8 ERRATUM additional note flags the 56-84% clause; task-10 follow-up owns the correction",
    "SV-04": "metadata-level: the claim is in the 9a0fd69 commit message quoted by the erratum, not in the SV record prose",
    "E1-12": "minor/rounding: the min worker wall is 31.045 s (rounds to 31.0), prose says 31.1",
    "PF-02": "minor/rounding: -0.227458 rounds to -0.227 at 3 dp; the abstract says -0.228 (0.0005 at the boundary)",
    "E6-11": "minor: the sentence is attached to the verified-8 table (28-30 controls); 25-30 is the all-12 sensitivity range",
    "Q2-10": "same underlying issue as Q2-08/09: the committed comparison uses the all-pairs median as 'observed'",
    "Q2-11": "same underlying issue as Q2-08/09",
}

def main():
    build_q1(); build_q2(); build_q3(); build_e1(); build_e6e8()
    build_e11(); build_sv(); build_mp(); build_pf()
    out = []
    for c in CHECKS:
        try:
            value, status, note = c["fn"]()
        except Exception as e:  # noqa: BLE001
            value, status, note = f"EXCEPTION: {type(e).__name__}: {e}", "UNVERIFIABLE", "check crashed"
        out.append(dict(id=c["id"], record=c["record"], claim=c["claim"], prose=c["prose"],
                        source=c["source"], recomputed=value, status=status, note=note,
                        known=KNOWN.get(c["id"], "")))
    counts = {}
    for r in out:
        counts.setdefault(r["record"], {"MATCH": 0, "MISMATCH": 0, "UNVERIFIABLE": 0})
        counts[r["record"]][r["status"]] += 1
    summary = {}
    for rec, d in counts.items():
        summary[rec] = dict(total=sum(d.values()), **d)
    result = dict(
        audit="prose-vs-data audit of the nine verified heads",
        date="2026-11-24",
        method="recompute from committed result files via git show <ref>:<path>; compare with REPORT/abstract prose",
        refs=REFS,
        totals=dict(total=len(out), **{k: sum(1 for r in out if r["status"] == k)
                                       for k in ("MATCH", "MISMATCH", "UNVERIFIABLE")}),
        by_record=summary,
        checks=out,
    )
    dest = REPO / "research/records/2026-11-24-prose-data-audit/results/audit.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(f"wrote {dest}")
    print(f"total {result['totals']['total']} | MATCH {result['totals']['MATCH']} | "
          f"MISMATCH {result['totals']['MISMATCH']} | UNVERIFIABLE {result['totals']['UNVERIFIABLE']}")
    for rec, s in summary.items():
        print(f"  {rec}: {s['total']} checks | M {s['MATCH']} | X {s['MISMATCH']} | U {s['UNVERIFIABLE']}")
    if result["totals"]["MISMATCH"]:
        print("\nMISMATCHES:")
        for r in out:
            if r["status"] == "MISMATCH":
                print(f"  {r['id']} [{r['record']}] {r['claim']} | prose={r['prose']} | recomputed={r['recomputed']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
