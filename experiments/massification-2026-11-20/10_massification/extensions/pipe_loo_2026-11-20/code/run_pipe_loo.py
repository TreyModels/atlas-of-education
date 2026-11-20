#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-6 PIPE-LOO -- is the lower->upper one-stage transition ratio a system object?

Deterministic. No RNG, no network, no clock-dependent output in any result file.
Reads ONLY:
  10_massification/data/UNIVERSALIZATION_SERIES.csv   (observed completion series)
  08_council/brief_022/SYNTHESIS_022.md               (verbatim-source verification only)
Writes ONLY inside this experiment directory.

Implements PRE_DECLARATIONS.md exactly:
  S2 pairing rule      : t-3 exact, else nearest within +/-1 y (ties -> earlier year), else drop
  S3 LOO construction  : predict upper_t = median(other pairs' ratios of the same country) * lower_i
  S4 thresholds        : per country pass iff median|LOO err| <= 3.0 pp AND >=75% of pairs within +/-5 pp
                         PREDICTIVE iff >=3/4 countries pass; NOT PREDICTIVE iff <=2/4
  S5 secondary leg     : declared, NON-VERDICT-BEARING screens (S1/S2/S3)
  S7                   : no threshold change after results, no re-fit, no second estimand

Usage:
  python run_pipe_loo.py [--outdir results]
"""
import csv

import os
import statistics
import sys

# ======================================================================================
# 0. Frozen constants (hashed before the run; a mismatch is a reported BLOCK, not a rerun)
# ======================================================================================
EXPERIMENT = "EXP-6 PIPE-LOO"
WORKER = "PL"
BRIEF = "Council brief 022 (D122 #1); SYNTHESIS_022.md section 6, EXP-6 PIPE-LOO, rank #1"

PREDECL_SHA256 = "97033df0c5693f50784bac52f6373b5f04dfebe964d0d6334dca0d5ffc0ed278"
INPUT_SHA256 = {
    "10_massification/data/UNIVERSALIZATION_SERIES.csv":
        "85bc869396ebfcb39e3e1a21a31af219e75a07326c738a51d2bfdbe536737ddb",
    "08_council/brief_022/SYNTHESIS_022.md":
        "9508dd55be8dd64da8322a8277c8342a4f50be6790a3d287e39e7004537c109b",
}

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))       # experiment dir
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))           # .../massification-2026-11-20

# ---- declared country set (PRE_DECLARATIONS.md S0) -----------------------------------
COUNTRIES = ["PHL", "KOR", "KHM", "CHN"]
NON_ENTRANTS = ["HKG", "JPN"]
COUNTRY_NAME = {
    "PHL": "Philippines", "KOR": "Korea, Rep.", "KHM": "Cambodia",
    "CHN": "China", "HKG": "Hong Kong SAR, China", "JPN": "Japan",
}

# ---- declared pairing rule (S2) -------------------------------------------------------
LAG = 3            # years, declared one-stage transition lag
TOL_YEARS = 1      # +/-1 y tolerance, as EXP-1
# ties -> earlier year: min(cands, key=(|y-target|, y))  (EXP-1 build_pairs(), line 216)

# ---- declared thresholds (S4) ---------------------------------------------------------
BAR_MEDIAN_ABS_PP = 3.0
BAR_WITHIN_SHARE = 0.75
BAND_PP = 5.0
PASS_NEEDED = 3
N_COUNTRIES = 4

# ---- declared reference figures from the brief (item 5), recorded as text, never used
#      to choose a rule. "pre-freeze calibration of the bars, not a result".
BRIEF_CALIBRATION = {
    "PHL": "1.50 (7/8)", "KOR": "0.48 (17/19)", "KHM": "2.17 (10/11)", "CHN": "14.48 (0/5)",
}
BRIEF_PAIR_COUNTS = {"PHL": 8, "KOR": 19, "KHM": 11, "CHN": 5}
BRIEF_TOTAL_PAIRS = 43

# ---- secondary leg (S5), declared non-verdict-bearing ---------------------------------
PHL_LATE_WINDOW = (2022, 2024)
PHL_EARLY_WINDOW = (2003, 2017)


# ======================================================================================
# 1. Guards
# ======================================================================================
def sha256_of(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def guard_inputs():
    """Refuse to run if the predeclaration or a frozen input changed."""
    predecl = os.path.join(HERE, "PRE_DECLARATIONS.md")
    got = sha256_of(predecl)
    if got != PREDECL_SHA256:
        print(f"[BLOCKED] PRE_DECLARATIONS.md sha256 {got} != declared {PREDECL_SHA256}")
        return False, [("PRE_DECLARATIONS.md", PREDECL_SHA256, got, False)]
    checks = [("PRE_DECLARATIONS.md", PREDECL_SHA256, got, True)]
    for rel, want in INPUT_SHA256.items():
        path = os.path.join(ROOT, rel)
        got = sha256_of(path)
        ok = (got == want)
        checks.append((rel, want, got, ok))
        if not ok:
            print(f"[BLOCKED] input {rel} sha256 {got} != declared {want}")
            return False, checks
    return True, checks


# ======================================================================================
# 2. Load observed completion series (OBSERVED, status=observed only)
# ======================================================================================
def load_series():
    path = os.path.join(ROOT, "10_massification/data/UNIVERSALIZATION_SERIES.csv")
    upper, lower = {}, {}
    rows = 0
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows += 1
            if r["status"] != "observed":
                continue
            ind = r["indicator"]
            if ind not in ("completion_upper_secondary", "completion_lower_secondary"):
                continue
            if r["iso3"] not in COUNTRIES + NON_ENTRANTS:
                continue
            y = int(r["year"])
            v = float(r["value"])
            tgt = upper if ind == "completion_upper_secondary" else lower
            tgt.setdefault(r["iso3"], {})[y] = v
    return upper, lower, rows


# ======================================================================================
# 3. Pairing rule (S2) -- identical convention to EXP-1 build_pairs()
# ======================================================================================
def build_pairs(upper_c, lower_c):
    pairs, dropped = [], []
    for t in sorted(upper_c):
        target = t - LAG
        if target in lower_c:
            use, flag = target, "EXACT"
        else:
            cands = [y for y in lower_c if abs(y - target) <= TOL_YEARS]
            if not cands:
                dropped.append(dict(upper_year=t, target_year=target,
                                    reason="DROPPED_NO_LOWER_WITHIN_1Y"))
                continue
            use = min(cands, key=lambda y: (abs(y - target), y))   # ties -> earlier year
            flag = "NEAREST_1Y"
        pairs.append(dict(upper_year=t, lower_year=use, pairing_flag=flag,
                          year_offset_used=use - target,
                          upper=upper_c[t], lower=lower_c[use],
                          ratio=upper_c[t] / lower_c[use]))
    return pairs, dropped


# ======================================================================================
# 4. LOO (S3)
# ======================================================================================
def add_loo(pairs):
    n = len(pairs)
    for i, p in enumerate(pairs):
        others = [q["ratio"] for j, q in enumerate(pairs) if j != i]
        if not others:                                  # n=1 -> declare N/A by rule
            p["loo_kappa"] = None
            p["prediction"] = None
            p["error"] = None
            p["abs_error"] = None
            p["within_5pp"] = None
            continue
        k = statistics.median(others)
        pred = k * p["lower"]
        p["loo_kappa"] = k
        p["prediction"] = pred
        p["error"] = pred - p["upper"]
        p["abs_error"] = abs(pred - p["upper"])
        p["within_5pp"] = (p["abs_error"] <= BAND_PP + 1e-9)
    return pairs


def country_stats(pairs):
    scored = [p for p in pairs if p["abs_error"] is not None]
    if not scored:
        return dict(n_pairs=len(pairs), n_scored=0, n_within=None,
                    median_abs=None, pct_within=None,
                    bar_median=False, bar_share=False, passed=False,
                    kappa_median=None)
    n = len(scored)
    n_in = sum(1 for p in scored if p["within_5pp"])
    med = statistics.median([p["abs_error"] for p in scored])
    pct = 100.0 * n_in / n
    bar_med = (med <= BAR_MEDIAN_ABS_PP + 1e-9)
    bar_share = (n_in / n >= BAR_WITHIN_SHARE - 1e-12)
    return dict(n_pairs=len(pairs), n_scored=n, n_within=n_in,
                median_abs=med, pct_within=pct,
                bar_median=bar_med, bar_share=bar_share,
                passed=bool(bar_med and bar_share),
                kappa_median=statistics.median([p["ratio"] for p in pairs]))


# ======================================================================================
# 5. Secondary leg (S5) -- declared, NON-VERDICT-BEARING
# ======================================================================================
def phl_lower_deltas(lower_phl):
    years = sorted(lower_phl)
    out = []
    for a, b in zip(years, years[1:]):
        span = b - a
        out.append(dict(year_from=a, year_to=b, span_years=span,
                        lower_from=lower_phl[a], lower_to=lower_phl[b],
                        delta_pp_per_year=(lower_phl[b] - lower_phl[a]) / span))
    return out


# ======================================================================================
# 6. Writers (fixed-width formatting -> byte-identical reruns)
# ======================================================================================
def f4(x):
    return "" if x is None else f"{x:.4f}"


def f2(x):
    return "" if x is None else f"{x:.2f}"


def yn(b):
    return "TRUE" if b else "FALSE"


def write_pairs_csv(path, all_pairs):
    cols = ["country", "iso3", "upper_year", "lower_year_used", "pairing_flag",
            "year_offset_used", "upper_value_pp", "lower_value_pp", "ratio",
            "loo_kappa", "predicted_upper_pp", "error_pp", "abs_error_pp",
            "within_5pp", "label"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for iso in COUNTRIES:
            for p in all_pairs[iso]:
                w.writerow([COUNTRY_NAME[iso], iso, p["upper_year"], p["lower_year"],
                            p["pairing_flag"], p["year_offset_used"],
                            f4(p["upper"]), f4(p["lower"]), f4(p["ratio"]),
                            f4(p["loo_kappa"]), f4(p["prediction"]),
                            f4(p["error"]), f4(p["abs_error"]),
                            yn(p["within_5pp"]),
                            "OBSERVED values / DERIVED ratio,LOO prediction,error"])


def write_results_csv(path, stats, verdict):
    cols = ["row_type", "entity", "iso3", "n_pairs", "n_dropped_upper_years",
            "n_within_5pp", "median_abs_loo_error_pp", "pct_within_5pp",
            "bar_median_abs_le_3.0pp", "bar_pct_within_5pp_ge_75",
            "country_pass", "kappa_median_ratio",
            "n_countries_pass", "n_countries_total", "verdict",
            "brief_calibration", "label", "note"]
    rows = []
    for iso in COUNTRIES:
        s = stats[iso]
        rows.append([
            "COUNTRY", COUNTRY_NAME[iso], iso, s["n_pairs"], s["n_dropped"],
            s["n_within"], f2(s["median_abs"]), f2(s["pct_within"]),
            yn(s["bar_median"]), yn(s["bar_share"]),
            "PASS" if s["passed"] else "FAIL", f4(s["kappa_median"]),
            "", "", "", BRIEF_CALIBRATION[iso], "DERIVED",
            "median|LOO error| and share within +/-5 pp over this country's own pairs"])
    for iso in NON_ENTRANTS:
        rows.append([
            "NON-ENTRANT", COUNTRY_NAME[iso], iso, 0, 0, "", "", "", "", "",
            "NON-ENTRANT", "", "", "", "", "n/a", "OBSERVED (absence)",
            "zero completion_lower/upper_secondary rows in the frozen file; cannot enter; "
            "no proxy numerator (D118); never imputed"])
    npass = sum(1 for iso in COUNTRIES if stats[iso]["passed"])
    allp = [p for iso in COUNTRIES for p in stats[iso]["pairs"]]
    pooled_med = statistics.median([p["abs_error"] for p in allp])
    pooled_in = sum(1 for p in allp if p["within_5pp"])
    rows.append([
        "OVERALL", "ALL", "", len(allp), sum(stats[i]["n_dropped"] for i in COUNTRIES),
        pooled_in, f2(pooled_med), f2(100.0 * pooled_in / len(allp)),
        "", "", "", "", npass, N_COUNTRIES, verdict, "",
        "DERIVED (verdict) / DERIVED-DESCRIPTIVE (pooled medians)",
        f"verdict = count of per-country passes ({npass}/{N_COUNTRIES}); pooled columns are "
        "DESCRIPTIVE only and carry no verdict; 'PREDICTIVE' iff >=3/4, 'NOT PREDICTIVE' iff <=2/4"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        w.writerows(rows)


def write_secondary_csv(path, stats, deltas, phl_subset):
    cols = ["screen_id", "entity", "item", "value", "unit",
            "verdict_bearing", "label", "note"]
    rows = []
    # S1 -- per-country pair counts
    tot = 0
    for iso in COUNTRIES:
        s = stats[iso]
        tot += s["n_pairs"]
        rows.append(["S1", COUNTRY_NAME[iso], "n_pairs", s["n_pairs"], "count",
                     "NO", "DERIVED", "pairs built from observed completion series"])
        rows.append(["S1", COUNTRY_NAME[iso], "n_upper_years_dropped",
                     s["n_dropped"], "count", "NO", "DERIVED",
                     "upper years with no lower observation within +/-1 y of t-3"])
    rows.append(["S1", "ALL", "n_pairs_total", tot, "count", "NO", "DERIVED",
                 f"brief declares {BRIEF_TOTAL_PAIRS}"])
    for iso in NON_ENTRANTS:
        rows.append(["S1", COUNTRY_NAME[iso], "n_pairs", 0, "count", "NO",
                     "OBSERVED (absence)",
                     "zero completion pairs; declared non-entrant, cannot enter"])
    # S2 -- PHL annualised lower-completion deltas
    for d in deltas:
        rows.append(["S2", "Philippines",
                     f"lower_annualised_delta_{d['year_from']}_{d['year_to']}",
                     f2(d["delta_pp_per_year"]), "pp/year", "NO", "DERIVED",
                     f"({f2(d['lower_to'])} - {f2(d['lower_from'])}) / {d['span_years']}y; "
                     "lower-secondary completion"])
    vals = [d["delta_pp_per_year"] for d in deltas]
    rows.append(["S2", "Philippines", "lower_annualised_delta_mean",
                 f2(sum(vals) / len(vals)), "pp/year", "NO", "DERIVED",
                 f"mean over {len(vals)} consecutive intervals"])
    rows.append(["S2", "Philippines", "lower_annualised_delta_sd_sample",
                 f2(statistics.stdev(vals)), "pp/year", "NO", "DERIVED",
                 "sample SD (ddof=1)"])
    # S3 -- PHL pair-year composition descriptor (descriptive only)
    rows.append(["S3", "Philippines", "n_pairs_upper_2022_2024",
                 phl_subset["n_late"], "count", "NO", "DERIVED-DESCRIPTIVE-NOT-VERDICT",
                 "pairs whose UPPER year is in 2022-2024"])
    rows.append(["S3", "Philippines", "n_pairs_upper_2003_2017",
                 phl_subset["n_early"], "count", "NO", "DERIVED-DESCRIPTIVE-NOT-VERDICT",
                 "pairs whose UPPER year is in 2003-2017"])
    rows.append(["S3", "Philippines", "loo_median_abs_error_2003_2017_subset",
                 f2(phl_subset["median_abs"]), "pp", "NO",
                 "DERIVED-DESCRIPTIVE-NOT-VERDICT",
                 "LOO recomputed on the 2003-2017 upper-year subset only; NO threshold applied, "
                 "NO verdict derived; the verdict uses all 8 PHL pairs only"])
    rows.append(["S3", "Philippines", "loo_pct_within_5pp_2003_2017_subset",
                 f2(phl_subset["pct_within"]), "percent", "NO",
                 "DERIVED-DESCRIPTIVE-NOT-VERDICT",
                 f"{phl_subset['n_within']}/{phl_subset['n_scored']} within +/-5 pp on that subset; "
                 "descriptive only"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        w.writerows(rows)


# ======================================================================================
# 7. Main
# ======================================================================================
def main():
    outdir = "results"
    argv = sys.argv[1:]
    if "--outdir" in argv:
        outdir = argv[argv.index("--outdir") + 1]
    outdir = outdir if os.path.isabs(outdir) else os.path.join(HERE, outdir)
    os.makedirs(outdir, exist_ok=True)

    lines = []
    def say(s=""):
        print(s)
        lines.append(s)

    say("=" * 100)
    say(f"{EXPERIMENT}  |  worker {WORKER}  |  {BRIEF}")
    say(f"predeclaration sha256 : {PREDECL_SHA256}")
    say("=" * 100)

    ok, checks = guard_inputs()
    say("")
    say("[guards] before any computation")
    for name, want, got, good in checks:
        say(f"  {'OK  ' if good else 'FAIL'} {name}")
        say(f"        declared {want}")
        say(f"        on-disk  {got}")
    if not ok:
        say("")
        say("STATUS: BLOCKED-FROZEN-INPUT (terminal for this run; not a result, not a country finding)")
        with open(os.path.join(outdir, "console.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return 2

    upper, lower, nrows = load_series()
    say("")
    say(f"[data] UNIVERSALIZATION_SERIES.csv parsed: {nrows} data rows total; "
        "completion_*_secondary status=observed subset:")

    all_pairs, stats = {}, {}
    for iso in COUNTRIES:
        up = upper.get(iso, {})
        lo = lower.get(iso, {})
        pairs, dropped = build_pairs(up, lo)
        add_loo(pairs)
        s = country_stats(pairs)
        s["n_dropped"] = len(dropped)
        s["pairs"] = pairs
        s["dropped"] = dropped
        all_pairs[iso], stats[iso] = pairs, s

    # ---- report the built pairs (all of them, one line each) --------------------------
    say("")
    say("[pairs] built under the declared rule (t-3 exact, else nearest within +/-1 y, else drop):")
    for iso in COUNTRIES:
        up, lo = upper.get(iso, {}), lower.get(iso, {})
        say("")
        say(f"  {iso}  {COUNTRY_NAME[iso]}   upper years: {sorted(up)}")
        say(f"       lower years: {sorted(lo)}")
        say(f"       pairs: {len(all_pairs[iso])}   dropped upper years: "
            f"{[d['upper_year'] for d in stats[iso]['dropped']]}")
        for p in all_pairs[iso]:
            say(f"       t={p['upper_year']}  lower@{p['lower_year']} ({p['pairing_flag']}, "
                f"offset {p['year_offset_used']:+d}y)  upper={p['upper']:.2f} "
                f"lower={p['lower']:.2f}  ratio={p['ratio']:.4f}  "
                f"LOO kappa={p['loo_kappa']:.4f}  pred={p['prediction']:.2f}  "
                f"err={p['error']:+.2f}  |err|={p['abs_error']:.2f}  "
                f"in5={yn(p['within_5pp'])}")

    total_pairs = sum(len(all_pairs[i]) for i in COUNTRIES)
    say("")
    say(f"[counts] total pairs = {total_pairs}  "
        f"(brief expects {BRIEF_TOTAL_PAIRS}; "
        f"{'MATCH' if total_pairs == BRIEF_TOTAL_PAIRS else 'MISMATCH'})  "
        f"| per country: " + ", ".join(f"{i} {len(all_pairs[i])}" for i in COUNTRIES))
    for iso in COUNTRIES:
        if len(all_pairs[iso]) != BRIEF_PAIR_COUNTS[iso]:
            say(f"  [MISMATCH] {iso}: built {len(all_pairs[iso])} vs brief {BRIEF_PAIR_COUNTS[iso]}")

    # ---- verdict ---------------------------------------------------------------------
    say("")
    say("[verdict] per-country bars: median|LOO err| <= 3.0 pp AND >= 75% of pairs within +/-5 pp")
    say(f"  {'iso':4s} {'n':>3s} {'n_in5':>6s} {'median|err|':>12s} {'pct_in5':>8s} "
        f"{'bar_T1':>7s} {'bar_T2':>7s} {'pass':>5s}  {'brief_calibration':>18s}")
    for iso in COUNTRIES:
        s = stats[iso]
        say(f"  {iso:4s} {s['n_pairs']:3d} {s['n_within']:6d} {s['median_abs']:12.2f} "
            f"{s['pct_within']:7.1f}% {yn(s['bar_median']):>7s} {yn(s['bar_share']):>7s} "
            f"{'PASS' if s['passed'] else 'FAIL':>5s}  {BRIEF_CALIBRATION[iso]:>18s}")
        brief_med = float(BRIEF_CALIBRATION[iso].split()[0])
        say(f"       brief pre-freeze calibration median {brief_med:.2f} vs recomputed "
            f"{s['median_abs']:.2f} -> "
            f"{'AGREE' if abs(brief_med - s['median_abs']) <= 0.005 else 'DISAGREE (reported)'}")
    npass = sum(1 for iso in COUNTRIES if stats[iso]["passed"])
    verdict = "PREDICTIVE" if npass >= PASS_NEEDED else "NOT PREDICTIVE"
    say("")
    say(f"  countries passing: {npass}/{N_COUNTRIES}  ->  VERDICT: {verdict}")
    say(f"  rule: PREDICTIVE iff >= 3/4 countries pass; NOT PREDICTIVE iff <= 2/4")

    # ---- secondary leg (declared, non-verdict-bearing) -------------------------------
    deltas = phl_lower_deltas(lower.get("PHL", {}))
    phl_pairs = all_pairs["PHL"]
    early = [p for p in phl_pairs
             if PHL_EARLY_WINDOW[0] <= p["upper_year"] <= PHL_EARLY_WINDOW[1]]
    late = [p for p in phl_pairs
            if PHL_LATE_WINDOW[0] <= p["upper_year"] <= PHL_LATE_WINDOW[1]]
    phl_subset = dict(
        n_late=len(late), n_early=len(early),
        n_scored=len(early),
        n_within=sum(1 for p in early if p["within_5pp"]),
        median_abs=statistics.median([p["abs_error"] for p in early]),
        pct_within=100.0 * sum(1 for p in early if p["within_5pp"]) / len(early),
    )
    say("")
    say("[secondary] declared NON-VERDICT-BEARING screens")
    say(f"  S1 pair counts: " + ", ".join(f"{i} {len(all_pairs[i])}" for i in COUNTRIES)
        + f", total {total_pairs}; non-entrants HKG 0, JPN 0 (zero completion pairs)")
    say(f"  S2 PHL lower-secondary annualised deltas (pp/yr), {len(deltas)} intervals:")
    say("       " + " / ".join(f"{d['delta_pp_per_year']:.2f}" for d in deltas))
    say(f"       mean {sum(d['delta_pp_per_year'] for d in deltas)/len(deltas):.2f}  "
        f"SD(sample) {statistics.stdev([d['delta_pp_per_year'] for d in deltas]):.2f}")
    say(f"  S3 PHL pair-year composition: {len(late)} pairs with upper year 2022-2024 "
        f"{[p['upper_year'] for p in late]}, {len(early)} with upper year 2003-2017 "
        f"{[p['upper_year'] for p in early]}")
    say(f"     2003-2017 subset LOO (DESCRIPTIVE-NOT-VERDICT, no threshold applied): "
        f"median|err| {phl_subset['median_abs']:.2f} pp, "
        f"{phl_subset['n_within']}/{phl_subset['n_scored']} within +/-5 pp")
    say(f"     kappa medians (DERIVED, descriptive, NOT fitted): "
        + ", ".join(f"{i} {stats[i]['kappa_median']:.4f}" for i in COUNTRIES))

    # ---- write -----------------------------------------------------------------------
    write_pairs_csv(os.path.join(outdir, "PIPE_LOO_PAIRS.csv"), all_pairs)
    write_results_csv(os.path.join(outdir, "PIPE_LOO_RESULTS.csv"), stats, verdict)
    write_secondary_csv(os.path.join(outdir, "PIPE_LOO_SECONDARY.csv"), stats, deltas, phl_subset)
    say("")
    say(f"[out] PIPE_LOO_PAIRS.csv      {total_pairs} pair rows + header")
    say(f"[out] PIPE_LOO_RESULTS.csv    {len(COUNTRIES)} country rows + "
        f"{len(NON_ENTRANTS)} non-entrant rows + 1 overall row")
    say(f"[out] PIPE_LOO_SECONDARY.csv  non-verdict-bearing screens S1/S2/S3")

    with open(os.path.join(outdir, "console.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
