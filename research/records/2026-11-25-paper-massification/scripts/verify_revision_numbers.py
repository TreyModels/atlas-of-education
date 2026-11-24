#!/usr/bin/env python3
"""Recompute the numbers quoted in the 2026-11-25 revision of Paper M.

Inputs are verbatim copies of the committed source records:
  data/e6_summary.json          <- research/e6e8-sequencing-2026-11-25 @ 2d19da7
  data/e8_results.json          <- research/e6e8-sequencing-2026-11-25 @ 2d19da7
  data/n3_recommendation.json   <- research/e6e8-sequencing-2026-11-25 @ 2d19da7
  data/fee_dates.csv            <- research/codex-source-verification-2026-11-25 @ 9a0fd69
  data/supply_demand_963e5e5.*  <- research/supply-demand-2026-11-23 @ 963e5e5
  data/event_dates_subsistence_v2.csv <- research/subsistence-v2-2026-11-23 @ ce66cfc

Output: data/revision_verification.json. Every number the revised paper quotes from
these families is recomputed here; failures are printed loudly.
"""
import csv
import json
import statistics

import numpy as np

OUT = "data/revision_verification.json"
checks = []


def check(family, claim, value, expected, source, note=""):
    ok = expected is None or value == expected
    checks.append(dict(family=family, claim=claim, recomputed=value,
                       paper_claim=expected, source=source, pass_=bool(ok), note=note))


# ---------------------------------------------------------------- E6
e6 = json.load(open("data/e6_summary.json"))
by_proxy = {}
for row in e6:
    if row["window"] != "1900-2012":
        continue
    proxy = row["proxy"]
    n_win = row["n_in_window"]
    identified = row["forward"] + row["reverse"] + row["forward_or_tie"]
    share = 100.0 * row["forward"] / identified
    lo = 100.0 * row["forward"] / n_win
    hi = 100.0 * (row["forward"] + row["undetermined"]) / n_win
    tie = 100.0 * row["forward_or_tie"] / n_win
    by_proxy[proxy] = dict(share=round(share, 1), lo=round(lo, 1), hi=round(hi, 1),
                           tie=round(tie, 1), forward=row["forward"], reverse=row["reverse"],
                           forward_or_tie=row["forward_or_tie"], undetermined=row["undetermined"],
                           n_in_window=n_win, n_all=row["n_all"],
                           schooling_first_share=round(100.0 * row["reverse"] / identified, 1))
check("E6", "demand-first share, GGDC non-agricultural employment (1900-2012)",
      by_proxy["ggdc_nonag_emp"]["share"], 10.0, "e6_summary.json:forward_share_identified")
check("E6", "demand-first share, urbanisation", by_proxy["urban"]["share"], 15.4,
      "e6_summary.json:forward_share_identified")
check("E6", "demand-first share, industry value added", by_proxy["ind_va"]["share"], 24.1,
      "e6_summary.json:forward_share_identified")
check("E6", "demand-first share, agricultural value added", by_proxy["agri_va"]["share"], 18.8,
      "e6_summary.json:forward_share_identified")
los = [v["lo"] for v in by_proxy.values()]
his = [v["hi"] for v in by_proxy.values()]
check("E6", "bounds over all countries (lower/upper)", [min(los), max(his)], [6.7, 53.0],
      "e6_summary.json:forward_lower/upper_bound_all")
ties = [v["tie"] for v in by_proxy.values()]
check("E6", "weak forward-or-tie share (in-window)", [round(min(ties)), round(max(ties))],
      [21, 43], "e6_summary.json:forward_or_tie / n_in_window")
check("E6", "strict schooling-first share (identifiable, range)",
      [min(v["schooling_first_share"] for v in by_proxy.values()),
       max(v["schooling_first_share"] for v in by_proxy.values())], None,
      "e6_summary.json:reverse / identifiable", "not quoted as a single percentage in paper")
# full-overlap identifiable range: 10.0-24.1
check("E6", "demand-first range across proxies",
      [min(v["share"] for v in by_proxy.values()), max(v["share"] for v in by_proxy.values())],
      [10.0, 24.1], "e6_summary.json")

# ---------------------------------------------------------------- N3
n3 = json.load(open("data/n3_recommendation.json"))
check("N3", "definitions with >=20 countries", n3["n_with_20plus"], 54, "n3_recommendation.json")
check("N3", "demand-first strict range across definitions",
      n3["forward_share_range_identified"], [0.0, 30.8], "n3_recommendation.json")
check("N3", "demand-first strict median across definitions", n3["forward_share_median"], 10.45,
      "n3_recommendation.json")
q1 = n3["q1_default"][0]
n_q1 = q1["n"]
check("N3", "q1 default: strict demand-first / weak tie / schooling-first",
      [q1["forward_share_identified"],
       round(100.0 * q1["forward_or_tie"] / n_q1, 1),
       round(100.0 * q1["reverse"] / n_q1, 1)],
      [6.2, 70.6, 17.6], "n3_recommendation.json:q1_default (weak tie = 24/34; schooling-first = 6/34)")

# ---------------------------------------------------------------- E8
e8 = json.load(open("data/e8_results.json"))
primary = e8["results"]["SE.PRM.ENRR_verified8"]["event_table"]
rows = {r["event"]: r for r in primary}
posts = {ev: rows[ev] for ev in (1, 2, 3, 4, 5, 6)}
post_atts = [round(rows[ev]["att"], 1) for ev in posts]
post_lo = [round(rows[ev]["ci_lo"], 2) for ev in posts]
post_hi = [round(rows[ev]["ci_hi"], 2) for ev in posts]
check("E8", "CS post ATT range, event +1..+6", [min(post_atts), max(post_atts)], [22.1, 28.6],
      "e8_results.json:event_table")
check("E8", "all post +1..+6 CIs exclude zero", all(lo > 0 for lo in post_lo), True,
      "e8_results.json:ci_lo")
check("E8", "on-impact ATT and CI", [round(rows[0]["att"], 1),
                                     round(rows[0]["ci_lo"], 2), round(rows[0]["ci_hi"], 2)],
      [12.4, -2.36, 27.24], "e8_results.json:event 0")
twfe_post = [round(rows[ev]["att_twfe"], 1) for ev in posts]
check("E8", "TWFE post ATT range, event +1..+6", [min(twfe_post), max(twfe_post)], [21.0, 27.6],
      "e8_results.json:att_twfe")
pre = {ev: rows[ev] for ev in (-5, -4, -3, -2)}
check("E8", "pre-trend ATT at -2 / -3 / -4",
      [round(pre[-2]["att"], 2), round(pre[-3]["att"], 2), round(pre[-4]["att"], 2)],
      [-0.03, -0.13, 1.35], "e8_results.json:pre_trend_rows")
check("E8", "earliest pre-trend horizon is imprecise and only 6 cohorts",
      [round(pre[-5]["att"], 2), int(pre[-5]["n"])], [6.39, 6],
      "e8_results.json:event -5")
sens = {s["spec"]: s for s in e8["sensitivity"]}
check("E8", "placebo -6 mean post ATT", round(sens["placebo-6"]["mean_att_post"], 2), -0.39,
      "e8_results.json:sensitivity")
loo = [s["mean_att_post"] for s in e8["sensitivity"] if s["spec"].startswith("drop-")]
check("E8", "leave-one-out mean post range", [round(min(loo), 2), round(max(loo), 2)],
      [18.17, 26.16], "e8_results.json:sensitivity")
check("E8", "all-12-dates mean post ATT", round(sens["all12"]["mean_att_post"], 2), 20.80,
      "e8_results.json:sensitivity")
sec = {r["event"]: r for r in e8["results"]["SE.SEC.ENRR_verified8"]["event_table"]}
sec_ci_includes_zero = all(sec[ev]["ci_lo"] <= 0 <= sec[ev]["ci_hi"] for ev in (1, 2, 3, 4, 5, 6))
check("E8", "secondary GER proxy: post CIs include zero (no clear detected effect)",
      sec_ci_includes_zero, True, "e8_results.json:SE.SEC.ENRR_verified8")
check("E8", "primary GER post effect significant from +1; treated n = 7 at +1",
      [rows[1]["ci_lo"] > 0, int(rows[1]["n_treated"])], [True, 7],
      "e8_results.json")
fees = list(csv.DictReader(open("data/fee_dates.csv")))
verified = [r for r in fees if r["status"] == "VERIFIED"]
unresolved = [r for r in fees if r["status"] != "VERIFIED"]
check("E8", "verified fee dates (ISO3:year)",
      {r["iso3"]: int(r["preferred_year"]) for r in verified},
      {"MWI": 1994, "ETH": 1995, "UGA": 1997, "LSO": 2000, "TZA": 2001,
       "KEN": 2003, "MOZ": 2004, "GHA": 2005}, "fee_dates.csv")
check("E8", "unresolved fee dates excluded from main", sorted(r["iso3"] for r in unresolved),
      ["BDI", "CMR", "RWA", "ZMB"], "fee_dates.csv")

# ---------------------------------------------------------------- sequencing (subsistence-v2 ce66cfc)
ev_rows = list(csv.DictReader(open("data/event_dates_subsistence_v2.csv")))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


complete = [r for r in ev_rows if all(num(r.get(c)) is not None
                                      for c in ("schooling", "release", "fertility"))]
pairs = [(num(r["schooling"]), num(r["release"]), num(r["fertility"])) for r in complete]
n = len(pairs)
forward = sum(1 for s, r, f in pairs if s < r)
reverse = sum(1 for s, r, f in pairs if r < s)
gap = np.array([r - s for s, r, f in pairs])
# Bootstrap exactly as the source record's script: pandas sample with a fresh
# integer seed drawn from default_rng(20261123) on each of 1,000 resamples.
import pandas as pd  # noqa: E402

df = pd.DataFrame(pairs, columns=["schooling", "release", "fertility"])
rng = np.random.default_rng(20261123)
boot = []
for _ in range(1000):
    smp = df.sample(len(df), replace=True, random_state=int(rng.integers(1e9)))
    boot.append([(smp.release <= smp.schooling).mean(),
                 (smp.schooling - smp.release).median()])
boot = np.array(boot)
check("sequencing", "countries with all three events", n, 64,
      "event_dates_subsistence_v2.csv @ ce66cfc")
check("sequencing", "schooling before release / release before schooling", [forward, reverse], [61, 3],
      "event_dates_subsistence_v2.csv")
check("sequencing", "forward share", round(100.0 * forward / n, 1), 95.3,
      "event_dates_subsistence_v2.csv")
check("sequencing", "median lead (years)", float(np.median(gap)), 26.0,
      "event_dates_subsistence_v2.csv")
check("sequencing", "bootstrap 95% CI release-before-schooling share",
      [round(100 * float(np.percentile(boot[:, 0], 2.5))),
       round(100 * float(np.percentile(boot[:, 0], 97.5)))], [0, 11],
      "bootstrap, 1000 country resamples, seed 20261123 (source script method)")
check("sequencing", "bootstrap 95% CI median lead (years)",
      [round(float(-np.percentile(boot[:, 1], 97.5))),
       round(float(-np.percentile(boot[:, 1], 2.5)))], [22, 26],
      "bootstrap, 1000 country resamples, seed 20261123 (source script method)")
# fertility ordering (strict)
sf = sum(1 for s, r, f in pairs if s < f)
ties = sum(1 for s, r, f in pairs if s == f)
ff = sum(1 for s, r, f in pairs if f < s)
check("fertility ordering", "strict schooling-first / simultaneous / fertility-first (of 64)",
      [sf, ties, ff], [24, 20, 20], "data/recompute_fertility_ordering.json")
check("fertility ordering", "strict schooling-first share", round(100.0 * sf / n, 1), 37.5,
      "data/recompute_fertility_ordering.json")
all_pairs = [(num(r["schooling"]), num(r["fertility"])) for r in ev_rows
             if num(r.get("schooling")) is not None and num(r.get("fertility")) is not None]
check("fertility ordering", "all countries with both dates / schooling-first share",
      [len(all_pairs), round(100.0 * sum(1 for s, f in all_pairs if s < f) / len(all_pairs), 1)],
      [81, 35.8], "data/recompute_fertility_ordering.json")

# ---------------------------------------------------------------- supply vs demand (963e5e5)
sd = json.load(open("data/supply_demand_963e5e5.json"))
check("supply-demand", "countries with both onsets", sd["n_both"], 89,
      "supply_demand.json:n_both")
check("supply-demand", "supply / demand onset before schooling (%)",
      [round(sd["supply_before_schooling_pct"], 1), round(sd["demand_before_schooling_pct"], 1)],
      [28.1, 73.0], "supply_demand.json")
hr = sd["event_ordering"]["horse race"]
comp = sd["event_ordering"]["composite"]
check("supply-demand", "horse-race composite supply (coef, SE)",
      [round(comp["supply"][0], 3), round(comp["supply"][1], 3)], [0.456, 0.174],
      "supply_demand.json:composite")
check("supply-demand", "horse-race composite demand (coef, SE)",
      [round(comp["demand"][0], 3), round(comp["demand"][1], 3)], [0.006, 0.203],
      "supply_demand.json:composite")
check("supply-demand", "horse-race n", comp["n"], 78, "supply_demand.json:composite")
check("supply-demand", "enrolment / spending coefficients (SE)",
      [[round(hr["d_supply_ger"][0], 3), round(hr["d_supply_ger"][1], 3)],
       [round(hr["d_supply_spend"][0], 3), round(hr["d_supply_spend"][1], 3)]],
      [[0.307, 0.146], [0.125, 0.058]], "supply_demand.json:horse race")
check("supply-demand", "demand-only specification n", sd["event_ordering"]["demand only"]["n"], 300,
      "supply_demand.json:demand only")

# ---------------------------------------------------------------- summary
out = dict(
    paper="Paper M, revision of 2026-11-25",
    sources={
        "e6_e8": "research/e6e8-sequencing-2026-11-25 @ 2d19da7",
        "fee_dates": "research/codex-source-verification-2026-11-25 @ 9a0fd69",
        "supply_demand": "research/supply-demand-2026-11-23 @ 963e5e5",
        "sequencing": "research/subsistence-v2-2026-11-23 @ ce66cfc",
        "fertility_ordering": "this branch: scripts/recompute_fertility_ordering.py",
    },
    e6_by_proxy=by_proxy,
    checks=checks,
    n_pass=sum(1 for c in checks if c["pass_"]),
    n_fail=sum(1 for c in checks if not c["pass_"]),
)
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps(dict(n_pass=out["n_pass"], n_fail=out["n_fail"]), indent=1))
for c in checks:
    if not c["pass_"]:
        print("FAIL:", c)
print("wrote", OUT)
