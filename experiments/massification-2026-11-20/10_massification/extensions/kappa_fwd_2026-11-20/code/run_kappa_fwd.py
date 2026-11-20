#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-11 KAPPA-FWD -- is the per-system lower->upper transition ratio forward-usable?

Deterministic. No RNG, no network, no clock-dependent output in any result file.
Reads ONLY (read-only):
  10_massification/data/UNIVERSALIZATION_SERIES.csv            (observed completion series)
  10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv   (cross-check only)
  08_council/brief_023/SYNTHESIS_023.md                        (verbatim-source verification)
  08_council/DECISIONS.md                                      (D133/D136 verbatim verification)
Writes ONLY inside this experiment directory.

Implements PRE_DECLARATIONS.md exactly:
  S2  pairing rule     : t-3 exact, else nearest within +/-1 y (ties -> earlier year), else drop
  S3  kappa            : median of ratios; LOO kappa recomputed for the declared secondary checks only
  S4  leg (a)          : kappa-STABLE iff |OLS slope of ratio on upper_year| <= 0.005/yr
                         AND |median_ratio(half2) - median_ratio(half1)| * 100 <= 2.0 pp
  S5  leg (b)          : kappa_pre = median of pairs with upper_year <= 2020;
                         bound = kappa_pre * lower_used; violation iff upper - bound > 1e-9 pp;
                         BOUND-HOLDS iff <=1 violation of 7; BOUND-BREAKS iff >=2
  S6  CHN              : reported, EXCLUDED from the forward conjunction / 7-cell denominator / falsifier (D133)
  S7  verdict          : FORWARD-USABLE iff PHL & KOR & KHM all kappa-STABLE AND BOUND-HOLDS; else WINDOW-ONLY
  S8  no threshold change, no re-fit, one estimand

Usage:
  python run_kappa_fwd.py [--outdir results]
"""
import argparse
import csv
import hashlib
import os
import sys

# ======================================================================================
# 0. Frozen constants (hashed before the run; a mismatch is a reported BLOCK, not a rerun)
# ======================================================================================
EXPERIMENT = "EXP-11 KAPPA-FWD"
WORKER = "KF"
BRIEF = "Council brief 023 (D136 #1); SYNTHESIS_023.md section 6.1, EXP-11 KAPPA-FWD, rank #1"

PREDECL_SHA256 = "bda79ac4c58306f8dcb1f41dd69d1f301e4d780cbecec8c70341e7aa8cac71b2"
INPUT_SHA256 = {
    "10_massification/data/UNIVERSALIZATION_SERIES.csv":
        "85bc869396ebfcb39e3e1a21a31af219e75a07326c738a51d2bfdbe536737ddb",
    "08_council/brief_023/SYNTHESIS_023.md":
        "39e666cffbe3950d43460ba177a36501d53fd0ec8083cd5c9abcbd1c7aeed44c",
    "08_council/DECISIONS.md":
        "15c564cffb1d9994386873b7daf9793407745da5477d437ef3adcb9efba8771c",
    "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv":
        "692ca7c01b8b3a7105e84339a87f97029b6a50e277681bdcdbe0f02bf027600f",
}

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))       # experiment dir
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))           # .../massification-2026-11-20
PREDECL_PATH = os.path.join(HERE, "PRE_DECLARATIONS.md")

# ---- declared system set (PRE_DECLARATIONS.md S0) -------------------------------------
COUNTRIES = ["PHL", "KOR", "KHM", "CHN"]
FORWARD_SET = ["PHL", "KOR", "KHM"]          # S6: CHN reported, never a forward constraint
NON_ENTRANTS = ["HKG", "JPN"]
COUNTRY_NAME = {
    "PHL": "Philippines", "KOR": "Korea, Rep.", "KHM": "Cambodia",
    "CHN": "China", "HKG": "Hong Kong SAR, China", "JPN": "Japan",
}

# ---- declared pairing rule (S2) -------------------------------------------------------
LAG = 3
TOL_YEARS = 1
IND_UPPER = "completion_upper_secondary"
IND_LOWER = "completion_lower_secondary"

# ---- declared thresholds (S4/S5), frozen before the run -------------------------------
SLOPE_BAR = 0.005            # ratio units per year, inclusive on |slope|
HALF_SHIFT_BAR_PP = 2.0      # pp, inclusive
HOLDOUT_CUTOFF = 2020        # train: upper_year <= 2020; hold-out cells: upper_year >= 2021
BOUND_EPS_PP = 1e-9          # floating-point guard only; the brief's bound is strict
WITHIN_NEEDED = 6            # of 7
N_HOLDOUT_DECLARED = 7
SLACK_BAND_PP = 5.0          # S-B1, declared NON-VERDICT-BEARING (EXP-6's own band)

# ---- declared reference values (text, recorded BEFORE the run; agreement is a check,
#      never a target). Source: DECISIONS.md D133 register + SYNTHESIS_023.md S6.1 item 4.
DECLARED = {
    "PHL": {"kappa_full": 0.9491, "kappa_pre": 0.9596, "n_pairs": 8,  "n_holdout": 2},
    "KOR": {"kappa_full": 0.9898, "kappa_pre": 0.9887, "n_pairs": 19, "n_holdout": 3},
    "KHM": {"kappa_full": 0.5950, "kappa_pre": 0.5950, "n_pairs": 11, "n_holdout": 2},
    "CHN": {"kappa_full": 0.7222, "kappa_pre": 0.7222, "n_pairs": 5,  "n_holdout": 0},
}
N_PAIRS_DECLARED = 43
N_DROPPED_DECLARED = 16
MATCH_TOL_4DP = 5e-5         # declared medians carry 4 dp
CROSSCHECK_TOL = 5e-5        # PIPE_LOO_PAIRS.csv carries 4 dp

LOG = []


def say(msg=""):
    LOG.append(msg)
    print(msg)


def fmt(x, nd=6):
    """Fixed-precision, locale-free, no negative zero. '' for None."""
    if x is None:
        return ""
    s = "%.*f" % (nd, x)
    if s.startswith("-") and float(s) == 0.0:
        s = s[1:]
    return s


def tf(b):
    return "TRUE" if b else "FALSE"


def sha256_path(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ======================================================================================
# 1. Pre-flight: predeclaration and input hashes (S11). Abort -> UNDETERMINED, no re-cut.
# ======================================================================================
def preflight():
    say("=" * 100)
    say("%s -- worker %s" % (EXPERIMENT, WORKER))
    say("brief: %s" % BRIEF)
    say("=" * 100)
    say()
    say("[PRE-FLIGHT] predeclaration + input hash verification (S11)")
    got = sha256_path(PREDECL_PATH)
    say("  PRE_DECLARATIONS.md sha256 : %s" % got)
    say("  embedded constant          : %s" % PREDECL_SHA256)
    if got != PREDECL_SHA256:
        say("  BLOCK: predeclaration hash mismatch -> UNDETERMINED (no rule may be re-cut).")
        sys.exit(3)
    say("  OK (predeclaration is the one this script implements)")
    for rel, want in sorted(INPUT_SHA256.items()):
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            say("  BLOCK: missing input %s -> UNDETERMINED" % rel)
            sys.exit(3)
        have = sha256_path(p)
        say("  %-78s %s %s" % (rel, have[:16] + "...", "OK" if have == want else "MISMATCH"))
        if have != want:
            say("  BLOCK: input hash mismatch on %s -> UNDETERMINED (inputs changed)." % rel)
            sys.exit(3)
    say()


def check_verbatim():
    """S1: the fenced EXP-11 block must be byte-identical to SYNTHESIS_023.md lines 403-434."""
    src = open(os.path.join(ROOT, "08_council/brief_023/SYNTHESIS_023.md"), encoding="utf-8").read().split("\n")
    block = "\n".join(src[402:434])
    t = open(PREDECL_PATH, encoding="utf-8").read()
    i = t.index("### 1.1")
    start = t.index("````\n", i) + len("````\n")
    end = t.index("\n````", start)
    body = t[start:end]
    ok = (body == block)
    say("[VERBATIM CHECK] PRE_DECLARATIONS.md fence body vs SYNTHESIS_023.md lines 403-434: %s (32 lines)"
        % ("IDENTICAL" if ok else "MISMATCH -- BLOCK"))
    if not ok:
        say("  BLOCK: verbatim block mismatch -> UNDETERMINED (predeclaration defect, reported not repaired).")
        sys.exit(3)
    say()


# ======================================================================================
# 2. Data: observed series only (S0)
# ======================================================================================
def load_series():
    path = os.path.join(ROOT, "10_massification/data/UNIVERSALIZATION_SERIES.csv")
    upper, lower = {}, {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["status"] != "observed":
                continue
            iso, ind = r["iso3"], r["indicator"]
            if ind not in (IND_UPPER, IND_LOWER):
                continue
            y, v = int(r["year"]), float(r["value"])
            (upper if ind == IND_UPPER else lower).setdefault(iso, {})[y] = v
    return upper, lower


def build_pairs(upper, lower):
    """S2 pairing rule, per country and independently. Every upper year is paired or logged."""
    out, dropped = [], {}
    for iso in COUNTRIES:
        u = upper.get(iso, {})
        l = lower.get(iso, {})
        pairs, drops = [], []
        for t in sorted(u):
            target = t - LAG
            if target in l:
                pairs.append({"iso3": iso, "upper_year": t, "lower_year_used": target, "offset": 0,
                              "flag": "EXACT", "upper": u[t], "lower": l[target]})
                continue
            cands = [y for y in l if abs(y - target) <= TOL_YEARS]
            if not cands:
                drops.append((t, "DROPPED_NO_LOWER_WITHIN_1Y"))
                continue
            y = min(cands, key=lambda yy: (abs(yy - target), yy))
            pairs.append({"iso3": iso, "upper_year": t, "lower_year_used": y, "offset": y - target,
                          "flag": "NEAREST_1Y", "upper": u[t], "lower": l[y]})
        for p in pairs:
            p["ratio"] = p["upper"] / p["lower"]
        out.append((iso, pairs, drops))
    return out


# ======================================================================================
# 3. Estimators (S3, S4)
# ======================================================================================
def median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return None
    if n % 2:
        return s[n // 2]
    return 0.5 * (s[n // 2 - 1] + s[n // 2])


def ols_slope(xs, ys):
    n = len(xs)
    if n < 2:
        return None, None
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return None, None
    slope = num / den
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - (my + slope * (x - mx))) ** 2 for x, y in zip(xs, ys))
    r2 = (1.0 - ss_res / ss_tot) if ss_tot > 0 else None
    return slope, r2


def loo_kappas(pairs):
    """S2.3: median of the other pairs' ratios. Secondary/cross-check only."""
    out = {}
    for i, p in enumerate(pairs):
        others = [q["ratio"] for j, q in enumerate(pairs) if j != i]
        out[p["upper_year"]] = median(others) if others else None
    return out


# ======================================================================================
# 4. Main computation
# ======================================================================================
def analyse():
    upper, lower = load_series()
    say("[DATA] observed completion series loaded (status=observed only; no interpolation)")
    for iso in COUNTRIES:
        say("  %s  upper years=%2d  lower years=%2d" % (iso, len(upper.get(iso, {})), len(lower.get(iso, {}))))
    say("  NON-ENTRANT (declared, zero completion pairs, never imputed): HKG, JPN")
    say()

    built = build_pairs(upper, lower)
    total_pairs = sum(len(p) for _, p, _ in built)
    total_drops = sum(len(d) for _, _, d in built)
    say("[PAIRING] rule: t-3 exact, else nearest within +/-1 y (ties -> earlier year), else drop")
    for iso, pairs, drops in built:
        say("  %-3s pairs=%2d dropped=%2d  (%s)" % (iso, len(pairs), len(drops),
                                                    ", ".join("u%dy" % t for t, _ in drops) or "none"))
    say("  TOTAL pairs=%d dropped=%d  (declared: %d / %d)" % (total_pairs, total_drops,
                                                              N_PAIRS_DECLARED, N_DROPPED_DECLARED))
    structure_ok = (total_pairs == N_PAIRS_DECLARED and total_drops == N_DROPPED_DECLARED)
    for iso, pairs, _ in built:
        structure_ok = structure_ok and len(pairs) == DECLARED[iso]["n_pairs"]
    say("  structure check: %s" % ("MATCH" if structure_ok else "MISMATCH -- BLOCK (S2.1)"))

    # ---- cross-check against EXP-6's frozen pairs file (S2.4) -------------------------
    exp6 = {}
    with open(os.path.join(ROOT, "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv"),
              newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            exp6[(r["iso3"], int(r["upper_year"]))] = r
    crosscheck_rows, crosscheck_fail = [], 0
    for iso, pairs, _ in built:
        for p in pairs:
            ref = exp6.get((iso, p["upper_year"]))
            if ref is None:
                crosscheck_rows.append((iso, p["upper_year"], "REFERENCE_MISSING", "", "", ""))
                crosscheck_fail += 1
                continue
            d_ratio = p["ratio"] - float(ref["ratio"])
            ok = (abs(d_ratio) <= CROSSCHECK_TOL
                  and int(ref["lower_year_used"]) == p["lower_year_used"]
                  and int(ref["year_offset_used"]) == p["offset"])
            if not ok:
                crosscheck_fail += 1
            crosscheck_rows.append((iso, p["upper_year"], "MATCH" if ok else "DIFFERS",
                                    fmt(d_ratio, 8), ref["lower_year_used"], str(p["lower_year_used"])))
    say("[CROSSCHECK] re-derived pairs vs PIPE_LOO_PAIRS.csv (4 dp tolerance %.0e, years exact): %d/%d match"
        % (CROSSCHECK_TOL, len(crosscheck_rows) - crosscheck_fail, len(crosscheck_rows)))
    say("  the recomputed value stands; this checks the INPUT pairs, it does not re-score EXP-6 (S9).")
    say()

    # ---- per system ----------------------------------------------------------------
    per = {}
    for iso, pairs, drops in built:
        n = len(pairs)
        pairs = sorted(pairs, key=lambda p: p["upper_year"])
        years = [p["upper_year"] for p in pairs]
        ratios = [p["ratio"] for p in pairs]
        kappa_full = median(ratios)
        slope, r2 = ols_slope([float(y) for y in years], ratios)

        h = n // 2
        first = pairs[:h]
        second = pairs[n - h:]
        middle = pairs[h] if (n % 2) else None
        k1 = median([p["ratio"] for p in first]) if h else None
        k2 = median([p["ratio"] for p in second]) if h else None
        shift_pp = abs(k2 - k1) * 100.0 if (k1 is not None and k2 is not None) else None
        half_ok = shift_pp is not None and shift_pp <= HALF_SHIFT_BAR_PP
        slope_ok = slope is not None and abs(slope) <= SLOPE_BAR
        leg_a = "kappa-STABLE" if (slope_ok and half_ok) else "kappa-TRENDING"

        # LOO (recomputed) -- declared secondary only
        loo = loo_kappas(pairs)
        for p in pairs:
            p["loo_kappa"] = loo[p["upper_year"]]
        s_a1 = None
        if h:
            a1 = [loo[p["upper_year"]] for p in first]
            a2 = [loo[p["upper_year"]] for p in second]
            s_a1 = abs(median(a2) - median(a1)) * 100.0
        s_a2 = None
        if h:
            e1 = [abs(p["loo_kappa"] * p["lower"] - p["upper"]) for p in first]
            e2 = [abs(p["loo_kappa"] * p["lower"] - p["upper"]) for p in second]
            s_a2 = abs(median(e2) - median(e1))

        # leg (b)
        pre = [p for p in pairs if p["upper_year"] <= HOLDOUT_CUTOFF]
        hold = [p for p in pairs if p["upper_year"] >= HOLDOUT_CUTOFF + 1]
        kappa_pre = median([p["ratio"] for p in pre]) if pre else None
        for p in pairs:
            p["segment"] = "HOLDOUT" if p["upper_year"] >= HOLDOUT_CUTOFF + 1 else "PRE_2021"
            p["half_member"] = ("FIRST" if p in first else ("SECOND" if p in second else "MIDDLE_EXCLUDED"))
            p["kappa_pre"] = kappa_pre
            if p["segment"] == "HOLDOUT" and kappa_pre is not None:
                p["bound"] = kappa_pre * p["lower"]
                p["excess"] = p["upper"] - p["bound"]
                p["violation"] = p["excess"] > BOUND_EPS_PP
                p["within_slack"] = p["excess"] <= SLACK_BAND_PP
                lit = p["upper_year"] - LAG
                low_series = lower.get(iso, {})
                if lit in low_series:
                    p["literal_lower"] = low_series[lit]
                    p["literal_bound"] = kappa_pre * low_series[lit]
                    p["literal_status"] = "AVAILABLE"
                else:
                    p["literal_lower"] = None
                    p["literal_bound"] = None
                    p["literal_status"] = "UNAVAILABLE_NO_OBSERVED_LOWER_AT_T_MINUS_3"
            else:
                p["bound"] = p["excess"] = p["violation"] = p["within_slack"] = None
                p["literal_lower"] = p["literal_bound"] = None
                p["literal_status"] = ""

        violations = [p for p in hold if p["violation"]]
        within = len(hold) - len(violations)
        per[iso] = {
            "iso3": iso, "pairs": pairs, "drops": drops, "n": n, "n_pre": len(pre), "n_hold": len(hold),
            "kappa_full": kappa_full, "kappa_pre": kappa_pre, "slope": slope, "r2": r2,
            "h": h, "k1": k1, "k2": k2, "shift_pp": shift_pp, "slope_ok": slope_ok, "half_ok": half_ok,
            "leg_a": leg_a, "s_a1": s_a1, "s_a2": s_a2,
            "middle_year": middle["upper_year"] if middle else None,
            "hold": hold, "violations": violations, "within": within,
            "max_excess": max([p["excess"] for p in hold]) if hold else None,
            "mean_excess": (sum(p["excess"] for p in hold) / len(hold)) if hold else None,
            "within_slack": sum(1 for p in hold if p["within_slack"]) if hold else None,
        }

    # ---- aggregate leg (b) (S5.4) ---------------------------------------------------
    all_hold = [p for iso in FORWARD_SET for p in per[iso]["hold"]]
    V = sum(1 for p in all_hold if p["violation"])
    within_all = len(all_hold) - V
    bounds_hold = within_all >= WITHIN_NEEDED
    leg_b = "BOUND-HOLDS" if bounds_hold else "BOUND-BREAKS"
    within_slack_all = sum(1 for p in all_hold if p["within_slack"])

    # ---- verdict (S7.1) + falsifier (S7.2) ------------------------------------------
    all_stable = all(per[iso]["leg_a"] == "kappa-STABLE" for iso in FORWARD_SET)
    verdict = "FORWARD-USABLE" if (all_stable and bounds_hold) else "WINDOW-ONLY"
    falsifier_phl = per["PHL"]["slope"] is not None and per["PHL"]["slope"] > SLOPE_BAR
    falsifier_viol = V >= 2
    falsifier = falsifier_phl or falsifier_viol
    assert (not falsifier) or verdict == "WINDOW-ONLY", "falsifier tripped but verdict is not WINDOW-ONLY"
    arms = []
    if falsifier_phl:
        arms.append("PHL slope > +0.005/yr")
    if falsifier_viol:
        arms.append(">=2 hold-out violations (V=%d)" % V)

    if not structure_ok:
        verdict = "UNDETERMINED"

    say("[LEG (a)] stationarity (both bars conjunctive; slope bar %.3f/yr, half bar %.1f pp)"
        % (SLOPE_BAR, HALF_SHIFT_BAR_PP))
    for iso in COUNTRIES:
        r = per[iso]
        say("  %-3s n=%2d  slope=%+.6f/yr (r2=%s)  |slope|<=bar:%-5s  half h=%d middle=%s  "
            "k1=%s k2=%s shift=%s pp  <=bar:%-5s  -> %s"
            % (iso, r["n"], r["slope"], fmt(r["r2"], 4), tf(r["slope_ok"]), r["h"],
               r["middle_year"] if r["middle_year"] else "n/a", fmt(r["k1"], 6), fmt(r["k2"], 6),
               fmt(r["shift_pp"], 4), tf(r["half_ok"]), r["leg_a"]))
    say()
    say("[LEG (b)] temporal hold-out: train kappa on upper_year<=%d, bound = kappa_pre * lower_used"
        % HOLDOUT_CUTOFF)
    for iso in COUNTRIES:
        r = per[iso]
        say("  %-3s kappa_pre=%s (n_pre=%d)  hold-out cells=%d  within bound=%d  violations=%d%s"
            % (iso, fmt(r["kappa_pre"], 6), r["n_pre"], r["n_hold"], r["within"], len(r["violations"]),
               "" if r["n_hold"] else "  [N/A -- no post-2020 cell]"))
        for p in r["hold"]:
            say("      %d: upper=%10.4f  lower_used=%d=%.4f  bound=%10.4f  excess=%+8.4f  %s"
                % (p["upper_year"], p["upper"], p["lower_year_used"], p["lower"], p["bound"], p["excess"],
                   "VIOLATION" if p["violation"] else "within"))
    say("  AGGREGATE over the %d-cell denominator (PHL+KOR+KHM; CHN contributes 0, D133): within=%d/%d  "
        "violations=%d  -> %s" % (len(all_hold), within_all, len(all_hold), V, leg_b))
    say("  leg (a) all of PHL/KOR/KHM kappa-STABLE: %s" % tf(all_stable))
    say()
    say("[SENSITIVITIES] declared non-verdict-bearing (S4.3, S5.5)")
    for iso in COUNTRIES:
        r = per[iso]
        say("  %-3s S-A1 (LOO-kappa median shift)=%s pp   S-A2 (median|LOO err| shift)=%s pp   "
            "primary half shift=%s pp"
            % (iso, fmt(r["s_a1"], 4), fmt(r["s_a2"], 4), fmt(r["shift_pp"], 4)))
    say("  S-B1 (±%.1f pp slack band, EXP-6 convention): %d/%d cells within -> %s "
        "(primary strict: %d/%d -> %s)"
        % (SLACK_BAND_PP, within_slack_all, len(all_hold), "BOUND-HOLDS" if within_slack_all >= WITHIN_NEEDED
           else "BOUND-BREAKS", within_all, len(all_hold), leg_b))
    say()
    say("[RECONCILIATION] recomputed vs declared medians (4 dp; the RECOMPUTED value stands -- S3)")
    for iso in COUNTRIES:
        r = per[iso]
        d = DECLARED[iso]
        full_ok = abs(r["kappa_full"] - d["kappa_full"]) <= MATCH_TOL_4DP
        pre_ok = abs(r["kappa_pre"] - d["kappa_pre"]) <= MATCH_TOL_4DP
        say("  %-3s kappa_full=%s vs declared %s [%s]   kappa_pre=%s vs declared %s [%s]"
            % (iso, fmt(r["kappa_full"], 4), fmt(d["kappa_full"], 4), "MATCH" if full_ok else "DIFFERS",
               fmt(r["kappa_pre"], 4), fmt(d["kappa_pre"], 4), "MATCH" if pre_ok else "DIFFERS"))
    say()
    say("[VERDICT] %s" % verdict)
    say("  rule: FORWARD-USABLE iff PHL & KOR & KHM all kappa-STABLE AND BOUND-HOLDS (>= %d of %d); "
        "else WINDOW-ONLY (S7.1)" % (WITHIN_NEEDED, N_HOLDOUT_DECLARED))
    say("  legs: leg (a) = %s ; leg (b) = %s" % ("PASS" if all_stable else "FAIL", leg_b))
    say("  falsifier tripped: %s%s" % (tf(falsifier), ("  arms: " + " ; ".join(arms)) if arms else ""))
    say("  consequence (S7.4): kappa may not be a forward constraint in V16-REPAIR; it may enter only as a declared "
        "within-window trajectory input, or not at all." if verdict == "WINDOW-ONLY"
        else "  consequence (S7.4): kappa may enter V16-REPAIR as a declared per-system constant (never fitted), "
             "passed systems only, within the observed window horizon.")
    say("  labels: OBSERVED series; every ratio/slope/median/bound/error is DERIVED. No causal claim, no direction "
        "claim. D63 stays UNABLE as to cause. EXP-6 not re-scored.")
    say()

    return per, dict(total_pairs=total_pairs, total_drops=total_drops, structure_ok=structure_ok,
                     V=V, within_all=within_all, leg_b=leg_b, bounds_hold=bounds_hold,
                     all_stable=all_stable, verdict=verdict, falsifier=falsifier, arms=arms,
                     falsifier_phl=falsifier_phl, falsifier_viol=falsifier_viol,
                     crosscheck_rows=crosscheck_rows, crosscheck_fail=crosscheck_fail,
                     within_slack_all=within_slack_all, n_hold=len(all_hold), lower=lower)


# ======================================================================================
# 5. Writers (fixed precision, explicit order, '\n' newlines -> byte-deterministic)
# ======================================================================================
def mkrow(cols, **vals):
    """Column-safe row builder: unknown keys are impossible, missing keys -> ''."""
    unknown = set(vals) - set(cols)
    assert not unknown, unknown
    return [vals.get(c, "") for c in cols]


def write_results(outdir, per, agg):
    cols = ["row_type", "iso3", "system", "n_pairs", "n_pre2021", "n_holdout",
            "slope_ratio_per_year", "slope_abs", "slope_within_bar", "r2_descriptive",
            "half_n_per_side", "half_middle_upper_year", "kappa_half1", "kappa_half2",
            "half_median_shift_pp", "half_within_bar", "leg_a_stationarity",
            "kappa_full", "kappa_pre", "kappa_full_declared", "kappa_pre_declared",
            "kappa_full_check", "kappa_pre_check",
            "n_within_bound", "n_violations", "max_excess_pp", "mean_excess_pp",
            "leg_b_holdout", "forward_constraint", "verdict", "note"]
    rows = []
    for iso in COUNTRIES:
        r = per[iso]
        d = DECLARED[iso]
        full_ok = abs(r["kappa_full"] - d["kappa_full"]) <= MATCH_TOL_4DP
        pre_ok = abs(r["kappa_pre"] - d["kappa_pre"]) <= MATCH_TOL_4DP
        fc = "FORWARD-CONSTRAINT-ELIGIBLE" if iso in FORWARD_SET else "NOT-A-FORWARD-CONSTRAINT (D133: CHN non-stationary)"
        note = "leg (a) per S4.4; leg (b) per S5.2-S5.4; slope is OLS of ratio on upper_year, unweighted, no pair removed"
        if iso == "CHN":
            note += "; CHN reported in full, excluded from the forward conjunction, the 7-cell denominator and the falsifier (S6)"
        if not r["n_hold"]:
            note += "; leg (b) N/A -- no post-2020 cell"
        if r["n_hold"]:
            leg_b_cell = "%d/%d within (aggregate label in OVERALL)" % (r["within"], r["n_hold"])
        else:
            leg_b_cell = "N/A"
        rows.append(mkrow(
            cols,
            row_type="SYSTEM", iso3=iso, system=COUNTRY_NAME[iso],
            n_pairs=str(r["n"]), n_pre2021=str(r["n_pre"]), n_holdout=str(r["n_hold"]),
            slope_ratio_per_year=fmt(r["slope"], 6), slope_abs=fmt(abs(r["slope"]), 6),
            slope_within_bar=tf(r["slope_ok"]), r2_descriptive=fmt(r["r2"], 4),
            half_n_per_side=str(r["h"]),
            half_middle_upper_year=str(r["middle_year"]) if r["middle_year"] else "none",
            kappa_half1=fmt(r["k1"], 6), kappa_half2=fmt(r["k2"], 6),
            half_median_shift_pp=fmt(r["shift_pp"], 4), half_within_bar=tf(r["half_ok"]),
            leg_a_stationarity=r["leg_a"],
            kappa_full=fmt(r["kappa_full"], 6), kappa_pre=fmt(r["kappa_pre"], 6),
            kappa_full_declared=fmt(d["kappa_full"], 4), kappa_pre_declared=fmt(d["kappa_pre"], 4),
            kappa_full_check="MATCH" if full_ok else "DIFFERS",
            kappa_pre_check="MATCH" if pre_ok else "DIFFERS",
            n_within_bound=str(r["within"]) if r["n_hold"] else "",
            n_violations=str(len(r["violations"])) if r["n_hold"] else "",
            max_excess_pp=fmt(r["max_excess"], 4) if r["n_hold"] else "",
            mean_excess_pp=fmt(r["mean_excess"], 4) if r["n_hold"] else "",
            leg_b_holdout=leg_b_cell, forward_constraint=fc, verdict=agg["verdict"], note=note))
    for iso in NON_ENTRANTS:
        rows.append(mkrow(
            cols, row_type="NON-ENTRANT", iso3=iso, system=COUNTRY_NAME[iso], n_pairs="0",
            n_pre2021="0", n_holdout="0", leg_a_stationarity="NON-ENTRANT", leg_b_holdout="N/A",
            forward_constraint="N/A", verdict=agg["verdict"],
            note="zero completion_lower/upper_secondary rows in the frozen file (V14/D135); cannot enter; "
                 "no proxy numerator (D118); never imputed"))
    rows.append(mkrow(
        cols,
        row_type="OVERALL", iso3="ALL", n_pairs=str(agg["total_pairs"]),
        n_pre2021=str(agg["total_pairs"] - agg["n_hold"]), n_holdout=str(agg["n_hold"]),
        slope_within_bar="PASS" if agg["all_stable"] else "FAIL",
        half_within_bar="PASS" if agg["all_stable"] else "FAIL",
        leg_a_stationarity="PASS (all of PHL/KOR/KHM kappa-STABLE)" if agg["all_stable"]
                           else "FAIL (not all of PHL/KOR/KHM are kappa-STABLE)",
        n_within_bound=str(agg["within_all"]), n_violations=str(agg["V"]),
        leg_b_holdout="%s (%d/%d within)" % (agg["leg_b"], agg["within_all"], agg["n_hold"]),
        forward_constraint="PHL+KOR+KHM only (7 cells; CHN contributes 0)", verdict=agg["verdict"],
        note="verdict = conjunction of leg (a) over PHL/KOR/KHM and leg (b) >=%d/%d; falsifier tripped: %s (%s)"
             % (WITHIN_NEEDED, N_HOLDOUT_DECLARED, tf(agg["falsifier"]),
                "; ".join(agg["arms"]) if agg["arms"] else "no arm fired")))
    path = os.path.join(outdir, "KAPPA_FWD_RESULTS.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        w.writerows(rows)
    return path


def write_detail(outdir, per):
    cols = ["iso3", "upper_year", "lower_year_used", "year_offset_used", "pairing_flag",
            "upper_value_pp", "lower_value_pp", "ratio", "segment", "half_member", "loo_kappa",
            "kappa_pre", "bound_pp", "excess_pp", "violation", "slack_pp", "within_slack_5pp",
            "ratio_vs_kappa_pre", "literal_t_minus_3_lower", "literal_t_minus_3_bound",
            "literal_t_minus_3_status", "label"]
    rows = []
    for iso in COUNTRIES:
        for p in sorted(per[iso]["pairs"], key=lambda q: q["upper_year"]):
            rows.append([
                iso, p["upper_year"], p["lower_year_used"], "%+d" % p["offset"], p["flag"],
                fmt(p["upper"], 4), fmt(p["lower"], 4), fmt(p["ratio"], 6), p["segment"], p["half_member"],
                fmt(p["loo_kappa"], 6),
                fmt(p["kappa_pre"], 6) if (p["kappa_pre"] is not None and p["segment"] == "HOLDOUT") else "",
                fmt(p["bound"], 4) if p["bound"] is not None else "",
                ("%+.4f" % p["excess"]) if p["excess"] is not None else "",
                tf(p["violation"]) if p["violation"] is not None else "",
                fmt(-p["excess"], 4) if p["excess"] is not None else "",
                tf(p["within_slack"]) if p["within_slack"] is not None else "",
                fmt(p["ratio"] - p["kappa_pre"], 6) if (p["kappa_pre"] is not None and p["segment"] == "HOLDOUT") else "",
                fmt(p["literal_lower"], 4) if p["literal_lower"] is not None else "",
                fmt(p["literal_bound"], 4) if p["literal_bound"] is not None else "",
                p["literal_status"],
                "OBSERVED values / DERIVED ratio,bound,excess (no fitted quantity)",
            ])
    path = os.path.join(outdir, "KAPPA_FWD_DETAIL.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        w.writerows(rows)
    return path


def write_secondary(outdir, per, agg):
    cols = ["row_type", "iso3", "entity", "year", "statistic", "value", "unit", "label", "note"]
    rows = []

    # S-A1 / S-A2 / primary half statistics
    for iso in COUNTRIES:
        r = per[iso]
        rows.append(["S-A1", iso, COUNTRY_NAME[iso], "", "median LOO-kappa shift, first vs second half",
                     fmt(r["s_a1"], 4), "pp", "DERIVED (declared non-verdict-bearing)",
                     "S4.3: median of each half's per-pair LOO kappa. DEGENERATE BY CONSTRUCTION: LOO kappa is the "
                     "median of the other n-1 pairs, so it tracks the full-sample kappa in every pair; reported to "
                     "expose the degeneracy, never used for a label"])
        rows.append(["S-A2", iso, COUNTRY_NAME[iso], "", "median |LOO error| shift, first vs second half",
                     fmt(r["s_a2"], 4), "pp", "DERIVED (declared non-verdict-bearing)",
                     "S4.3: accuracy drift over time, NOT kappa's level drift; not the leg (a) object"])
        rows.append(["PRIMARY-HALF", iso, COUNTRY_NAME[iso], "",
                     "|median ratio(second half) - median ratio(first half)| x 100",
                     fmt(r["shift_pp"], 4), "pp", "DERIVED (verdict-bearing, S4.3)",
                     "k1=%s k2=%s | bar %.1f pp | %s" % (fmt(r["k1"], 6), fmt(r["k2"], 6),
                                                         HALF_SHIFT_BAR_PP,
                                                         "PASS" if r["half_ok"] else "FAIL")])

    # S-B1 per cell
    for iso in FORWARD_SET:
        for p in per[iso]["hold"]:
            rows.append(["S-B1", iso, COUNTRY_NAME[iso], p["upper_year"],
                         "excess over kappa_pre bound", "%+.4f" % p["excess"], "pp",
                         "DERIVED (declared non-verdict-bearing)",
                         "strict violation: %s | within +/-%.1f pp slack: %s | primary verdict uses the strict reading"
                         % (tf(p["violation"]), SLACK_BAND_PP, tf(p["within_slack"]))])

    # S-B2 literal t-3 availability
    for iso in FORWARD_SET:
        for p in per[iso]["hold"]:
            rows.append(["S-B2", iso, COUNTRY_NAME[iso], p["upper_year"],
                         "literal t-3 lower observation", p["literal_status"], "",
                         "OBSERVED (availability) / DERIVED",
                         "literal lower=%s literal bound=%s ; primary uses the pairing-rule lower (%d) for every cell; "
                         "an unobserved t-3 is NOT imputed (S5.3)"
                         % (fmt(p["literal_lower"], 4) if p["literal_lower"] is not None else "n/a",
                            fmt(p["literal_bound"], 4) if p["literal_bound"] is not None else "n/a",
                            p["lower_year_used"])])

    # S-B3 ratio vs kappa_pre
    for iso in FORWARD_SET:
        for p in per[iso]["hold"]:
            rows.append(["S-B3", iso, COUNTRY_NAME[iso], p["upper_year"], "ratio - kappa_pre",
                         "%+.6f" % (p["ratio"] - p["kappa_pre"]), "ratio", "DERIVED (descriptive)",
                         "dimensionless; direction of the cell's miss only -- no direction claim about causes"])

    # cross-check
    for iso, yr, status, d, ref_low, our_low in agg["crosscheck_rows"]:
        rows.append(["CROSSCHECK", iso, COUNTRY_NAME[iso], yr, "ratio vs PIPE_LOO_PAIRS.csv", d, "ratio",
                     "DERIVED (reproducibility check; recomputed value stands)",
                     "status=%s ref_lower_year=%s our_lower_year=%s" % (status, ref_low, our_low)])

    # non-entrants
    for iso in NON_ENTRANTS:
        rows.append(["NON-ENTRANT", iso, COUNTRY_NAME[iso], "", "completion pairs on disk", "0", "pairs",
                     "OBSERVED (absence)", "no completion_lower/upper_secondary rows; cannot enter; no proxy (D118)"])
    path = os.path.join(outdir, "KAPPA_FWD_SECONDARY.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        w.writerows(rows)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="results")
    args = ap.parse_args()
    outdir = args.outdir if os.path.isabs(args.outdir) else os.path.join(HERE, args.outdir)
    os.makedirs(outdir, exist_ok=True)

    preflight()
    check_verbatim()
    per, agg = analyse()

    # aggregate hold-out cells kept for the secondary writer
    agg["hold"] = [p for iso in FORWARD_SET for p in per[iso]["hold"]]

    paths = [write_results(outdir, per, agg), write_detail(outdir, per), write_secondary(outdir, per, agg)]
    say("[WRITE] %d result files written to the output directory" % len(paths))
    for p in paths:
        say("  %s" % os.path.basename(p))

    # console transcript (byte-identical across runs: no paths, no clock)
    with open(os.path.join(outdir, "console.txt"), "w", newline="", encoding="utf-8") as fh:
        fh.write("\n".join(LOG) + "\n")
    print("\n[WRITE] console.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
