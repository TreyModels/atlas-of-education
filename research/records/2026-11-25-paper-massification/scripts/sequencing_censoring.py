"""Recompute the sequencing distribution of Paper N1 from the committed event dates, treating boundary dates as censored.

Input:  results/event_dates.csv (copy of research/subsistence-v2-2026-11-23 @ ce66cfc results/event_dates.csv)
Output: results/sequencing_censoring.json
Definitions: lead = release_date - schooling_date, so a positive lead means schooling came first.

REVISION (review 2026-11-24). Event dates are searched in a 1965-2010 window (schooling on a 5-year grid; release
series start 1991). A date equal to the first available observation is LEFT-CENSORED: the event happened at or
before that date. In this file 61 of 108 schooling dates sit at 1965 and 65 of 134 release dates sit at 1991.
Treating those as exact dates (the earlier version) fabricates leads (e.g. 1991 - 1965 = 26 for every pair where
both are censored). Here each pair is classified instead:
  both exact          -> lead exact, order identified
  schooling censored  -> true S <= 1965 < R, so schooling first is identified; lead is only bounded below (>= R - 1965)
  release censored    -> true R <= 1991; order identified only if S >= 1991 (then release first or tie); else undetermined
  both censored       -> S <= 1965 and R <= 1991: order not identified
Ties (R == S, both exact) count as not-forward, as before.
"""
import csv, json, os, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.dirname(HERE)
rows = list(csv.DictReader(open(os.path.join(REC, "results", "event_dates.csv"))))
S_FLOOR, R_FLOOR, F_FLOOR = 1965.0, 1991.0, 1965.0

def num(x):
    try:
        return float(x)
    except Exception:
        return None

def classify(r):
    s, rel = num(r["schooling"]), num(r["release"])
    sc, rc = s == S_FLOOR, rel == R_FLOOR
    if not sc and not rc:
        return "both_exact", ("forward" if rel > s else "reverse")
    if sc and not rc:
        return "schooling_censored", "forward"          # S <= 1965 < 1991 < R
    if rc and not sc:
        return "release_censored", ("reverse_or_tie" if s >= R_FLOOR else "undetermined")
    return "both_censored", "undetermined"

def dist(dat):
    cls = [classify(r) for r in dat]
    n = len(dat)
    cats = {}
    for c, o in cls:
        cats[c] = cats.get(c, 0) + 1
    fwd = sum(1 for c, o in cls if o == "forward")
    rev = sum(1 for c, o in cls if o in ("reverse", "reverse_or_tie"))
    und = sum(1 for c, o in cls if o == "undetermined")
    ident = fwd + rev
    exact = [num(r["release"]) - num(r["schooling"]) for r, (c, o) in zip(dat, cls) if c == "both_exact"]
    exact_fwd = sorted(x for x in exact if x > 0)
    lbounds = [num(r["release"]) - S_FLOOR for r, (c, o) in zip(dat, cls) if c == "schooling_censored"]
    out = dict(
        n=n, categories=cats, identified_forward=fwd, identified_reverse=rev, undetermined=und,
        identified_total=ident,
        forward_share_of_identified_pct=round(100 * fwd / ident, 1) if ident else None,
        forward_share_of_all_lower_bound_pct=round(100 * fwd / n, 1),
        both_exact_n=len(exact), both_exact_forward=len(exact_fwd), both_exact_reverse_or_tie=len(exact) - len(exact_fwd),
        both_exact_median_lead=st.median(exact) if exact else None,
        both_exact_leads_sorted=sorted(exact),
        schooling_censored_lead_lower_bound_median=st.median(lbounds) if lbounds else None)
    # 15-year robustness on the identified pairs only: schooling dates assumed 15 years too early, i.e. true S = S + 15.
    # both_exact: forward iff lead > 15.  schooling_censored: R >= 1992 and true S <= 1965 + 15 = 1980 -> still forward.
    n15 = sum(1 for x in exact if x > 15) + cats.get("schooling_censored", 0)
    out["identified_forward_after_plus15_error"] = n15
    out["identified_forward_after_plus15_share_of_identified_pct"] = round(100 * n15 / ident, 1) if ident else None
    if len(exact) >= 4:
        q = st.quantiles(exact, n=4)
        out["both_exact_lead_q1"], out["both_exact_lead_q3"] = round(q[0], 1), round(q[2], 1)
    return out

all3 = [r for r in rows if num(r["release"]) is not None and num(r["schooling"]) is not None and num(r["fertility"]) is not None]
pair = [r for r in rows if num(r["release"]) is not None and num(r["schooling"]) is not None]
reverse_cases = [(r["iso3"], num(r["schooling"]), num(r["release"])) for r in pair if classify(r)[1] in ("reverse", "reverse_or_tie")]

# Naive (uncensored) numbers kept only for comparison with the earlier version of the paper
def naive(dat):
    leads = [num(r["release"]) - num(r["schooling"]) for r in dat]
    fwd = [x for x in leads if x > 0]
    return dict(n=len(dat), forward=len(fwd), median_lead_forward_only=st.median(fwd),
                share_gt10=round(100 * sum(x > 10 for x in fwd) / len(fwd), 1),
                note="NOT VALID: treats boundary dates as exact. Kept to show what the censoring changes.")

# Schooling vs fertility ordering on the 64-country panel (fertility dates are also left-censored: 50 of 127 sit at 1965).
# This resolves the 68.75 vs 35.8 discrepancy noted in the first draft: 68.75% is "schooling <= fertility" (it counts 20 ties,
# 18 of which are both-at-1965 pairs); strict schooling < fertility is 37.5%; neither is an identified ordering.
def fert_order(dat):
    S = lambda r: num(r["schooling"]); F = lambda r: num(r["fertility"])
    sc = lambda r: S(r) == S_FLOOR; fc = lambda r: F(r) == F_FLOOR
    return dict(
        n=len(dat), strict_schooling_before_fertility=sum(S(r) < F(r) for r in dat),
        ties=sum(S(r) == F(r) for r in dat), strict_fertility_before_schooling=sum(S(r) > F(r) for r in dat),
        both_at_1965_undetermined=sum(sc(r) and fc(r) for r in dat),
        schooling_censored_only_schooling_first=sum(sc(r) and not fc(r) for r in dat),
        fertility_censored_only_fertility_first=sum(fc(r) and not sc(r) for r in dat),
        both_exact=sum(not sc(r) and not fc(r) for r in dat),
        both_exact_schooling_first=sum((not sc(r)) and (not fc(r)) and S(r) < F(r) for r in dat),
        both_exact_fertility_first=sum((not sc(r)) and (not fc(r)) and S(r) > F(r) for r in dat),
        both_exact_ties=sum((not sc(r)) and (not fc(r)) and S(r) == F(r) for r in dat))

out = dict(all_three=dist(all3), schooling_vs_fertility_all_three=fert_order(all3), schooling_and_release=dist(pair),
           identified_reverse_cases=reverse_cases,
           naive_uncensored_for_reference=dict(all_three=naive(all3), schooling_and_release=naive(pair)),
           note="lead = release - schooling; positive = schooling first. all_three is the paper's 64-country panel.")
json.dump(out, open(os.path.join(REC, "results", "sequencing_censoring.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in out.items()}, indent=1))
