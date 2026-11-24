#!/usr/bin/env python3
"""Recompute the numbers quoted in the 2026-11-25 revision of Paper N1.

Inputs are committed in this record or are verbatim copies of the source records:
  results/event_dates.csv        <- research/subsistence-v2-2026-11-23 @ ce66cfc
  data/e6_summary.json           <- research/e6e8-sequencing-2026-11-25 @ 2d19da7
  data/e8_results.json           <- research/e6e8-sequencing-2026-11-25 @ 2d19da7
  data/n3_recommendation.json    <- research/e6e8-sequencing-2026-11-25 @ 2d19da7
  data/fee_dates.csv             <- research/codex-source-verification-2026-11-25 @ 9a0fd69
  data/supply_demand_963e5e5.json <- research/supply-demand-2026-11-23 @ 963e5e5

Output: results/revision_verification.json. Every number the revised paper quotes from these
families is recomputed here; failures are printed loudly. Requires pandas for the bootstrap
(the project's bundled runtime python has it).
"""
import csv
import json

import numpy as np
import pandas as pd

OUT = "results/revision_verification.json"
checks = []


def check(family, claim, value, expected, source):
    checks.append(dict(family=family, claim=claim, recomputed=value,
                       paper_claim=expected, source=source,
                       pass_=bool(expected is None or value == expected)))


# ---------------------------------------------------------------- sequencing (subsistence-v2)
rows = list(csv.DictReader(open("results/event_dates.csv")))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


complete = [r for r in rows if all(num(r.get(c)) is not None
                                   for c in ("schooling", "release", "fertility"))]
pairs = [(num(r["schooling"]), num(r["release"]), num(r["fertility"])) for r in complete]
n = len(pairs)
forward = sum(1 for s, r, f in pairs if s < r)
reverse = sum(1 for s, r, f in pairs if r < s)
gap = np.array([r - s for s, r, f in pairs])

# bootstrap exactly as the source record's script: pandas sample with a fresh integer seed
df = pd.DataFrame(pairs, columns=["schooling", "release", "fertility"])
rng = np.random.default_rng(20261123)
boot = []
for _ in range(1000):
    smp = df.sample(len(df), replace=True, random_state=int(rng.integers(1e9)))
    boot.append([(smp.release <= smp.schooling).mean(),
                 (smp.schooling - smp.release).median()])
boot = np.array(boot)

check("sequencing", "countries with all three events", n, 64, "results/event_dates.csv @ ce66cfc")
check("sequencing", "schooling first / release first", [forward, reverse], [61, 3],
      "results/event_dates.csv")
check("sequencing", "forward share (per cent)", round(100.0 * forward / n, 1), 95.3,
      "results/event_dates.csv")
check("sequencing", "median lead (years)", float(np.median(gap)), 26.0, "results/event_dates.csv")
import statistics as st  # noqa: E402  (same quartile method as scripts/sequencing_stats.py)

fwd_leads = sorted(r - s for s, r, f in pairs if s < r)
fq = st.quantiles(fwd_leads, n=4)
check("sequencing", "interquartile range of the lead (forward cases)",
      [round(fq[0], 1), round(fq[2], 1)], [16.5, 29.5],
      "results/event_dates.csv, forward cases, statistics.quantiles (as sequencing_stats.py)")
check("sequencing", "share of forward cases exceeding 10 / 15 years",
      [round(100.0 * sum(1 for s, r, f in pairs if s < r and r - s > 10) / forward, 1),
       round(100.0 * sum(1 for s, r, f in pairs if s < r and r - s > 15) / forward, 1)],
      [93.4, 85.2], "results/event_dates.csv")
check("sequencing", "share of all 64 still forward after +15-year error on schooling dates",
      round(100.0 * sum(1 for s, r, f in pairs if s + 15 < r) / n, 2), 81.25,
      "results/event_dates.csv")
check("sequencing", "bootstrap 95% CI release-before-schooling (per cent)",
      [round(100 * float(np.percentile(boot[:, 0], 2.5))),
       round(100 * float(np.percentile(boot[:, 0], 97.5)))], [0, 11],
      "bootstrap, 1000 country resamples, seed 20261123")
check("sequencing", "bootstrap 95% CI median lead (years)",
      [round(float(-np.percentile(boot[:, 1], 97.5))),
       round(float(-np.percentile(boot[:, 1], 2.5)))], [22, 26],
      "bootstrap, 1000 country resamples, seed 20261123")

# wider 81-country sample
two = [(num(r["schooling"]), num(r["release"])) for r in rows
       if num(r.get("schooling")) is not None and num(r.get("release")) is not None]
check("sequencing", "wider 81-country sample: n / forward share / median lead",
      [len(two),
       round(100.0 * sum(1 for s, r in two if s < r) / len(two), 1),
       float(np.median([r - s for s, r in two]))], [81, 93.8, 26.0],
      "results/event_dates.csv")

# fertility ordering (strict)
sf = sum(1 for s, r, f in pairs if s < f)
ties = sum(1 for s, r, f in pairs if s == f)
ff = sum(1 for s, r, f in pairs if f < s)
check("fertility ordering", "strict schooling-first / simultaneous / fertility-first (of 64)",
      [sf, ties, ff], [24, 20, 20], "results/event_dates.csv")
check("fertility ordering", "strict schooling-first share (per cent)", round(100.0 * sf / n, 1),
      37.5, "results/event_dates.csv")
all_pairs = [(num(r["schooling"]), num(r["fertility"])) for r in rows
             if num(r.get("schooling")) is not None and num(r.get("fertility")) is not None]
check("fertility ordering", "all 81 with both dates / schooling-first share",
      [len(all_pairs),
       round(100.0 * sum(1 for s, f in all_pairs if s < f) / len(all_pairs), 1)], [81, 35.8],
      "results/event_dates.csv")

# ---------------------------------------------------------------- E6 / N3 / E8
e6 = json.load(open("data/e6_summary.json"))
by_proxy = {}
for row in e6:
    if row["window"] != "1900-2012":
        continue
    n_win = row["n_in_window"]
    identified = row["forward"] + row["reverse"] + row["forward_or_tie"]
    by_proxy[row["proxy"]] = dict(
        share=round(100.0 * row["forward"] / identified, 1),
        lo=round(100.0 * row["forward"] / n_win, 1),
        hi=round(100.0 * (row["forward"] + row["undetermined"]) / n_win, 1),
        tie=round(100.0 * row["forward_or_tie"] / n_win, 1))
check("E6", "demand-first share: GGDC / urban / industry / agriculture (per cent)",
      [by_proxy["ggdc_nonag_emp"]["share"], by_proxy["urban"]["share"],
       by_proxy["ind_va"]["share"], by_proxy["agri_va"]["share"]], [10.0, 15.4, 24.1, 18.8],
      "data/e6_summary.json")
check("E6", "bounds over all countries (lower / upper, per cent)",
      [min(v["lo"] for v in by_proxy.values()), max(v["hi"] for v in by_proxy.values())],
      [6.7, 53.0], "data/e6_summary.json")
check("E6", "weak forward-or-tie share (in-window, per cent)",
      [round(min(v["tie"] for v in by_proxy.values())),
       round(max(v["tie"] for v in by_proxy.values()))], [21, 43], "data/e6_summary.json")

n3 = json.load(open("data/n3_recommendation.json"))
check("N3", "strict demand-first range / median across 54 definitions",
      [n3["forward_share_range_identified"], n3["forward_share_median"]],
      [[0.0, 30.8], 10.45], "data/n3_recommendation.json")
q1 = n3["q1_default"][0]
check("N3", "q1 default: strict demand-first / weak tie / schooling-first (per cent)",
      [q1["forward_share_identified"], round(100.0 * q1["forward_or_tie"] / q1["n"], 1),
       round(100.0 * q1["reverse"] / q1["n"], 1)], [6.2, 70.6, 17.6],
      "data/n3_recommendation.json:q1_default")

e8 = json.load(open("data/e8_results.json"))
prim = {r["event"]: r for r in e8["results"]["SE.PRM.ENRR_verified8"]["event_table"]}
posts = [round(prim[ev]["att"], 1) for ev in (1, 2, 3, 4, 5, 6)]
check("E8", "CS post ATT range +1..+6", [min(posts), max(posts)], [22.1, 28.6],
      "data/e8_results.json")
check("E8", "all post +1..+6 CIs exclude zero",
      all(prim[ev]["ci_lo"] > 0 for ev in (1, 2, 3, 4, 5, 6)), True, "data/e8_results.json")
check("E8", "on-impact ATT / CI", [round(prim[0]["att"], 1), round(prim[0]["ci_lo"], 2),
                                   round(prim[0]["ci_hi"], 2)], [12.4, -2.36, 27.24],
      "data/e8_results.json")
check("E8", "pre-trends -2 / -3 / -4",
      [round(prim[-2]["att"], 2), round(prim[-3]["att"], 2), round(prim[-4]["att"], 2)],
      [-0.03, -0.13, 1.35], "data/e8_results.json")
sens = {s["spec"]: s for s in e8["sensitivity"]}
check("E8", "placebo mean post / all-12 mean post",
      [round(sens["placebo-6"]["mean_att_post"], 2), round(sens["all12"]["mean_att_post"], 2)],
      [-0.39, 20.80], "data/e8_results.json")
loo = [s["mean_att_post"] for s in e8["sensitivity"] if s["spec"].startswith("drop-")]
check("E8", "leave-one-out mean post range", [round(min(loo), 2), round(max(loo), 2)],
      [18.17, 26.16], "data/e8_results.json")
fees = list(csv.DictReader(open("data/fee_dates.csv")))
verified = {r["iso3"]: int(r["preferred_year"]) for r in fees if r["status"] == "VERIFIED"}
check("E8", "verified fee dates", verified,
      {"MWI": 1994, "ETH": 1995, "UGA": 1997, "LSO": 2000, "TZA": 2001,
       "KEN": 2003, "MOZ": 2004, "GHA": 2005}, "data/fee_dates.csv")

# ---------------------------------------------------------------- supply vs demand (963e5e5)
sd = json.load(open("data/supply_demand_963e5e5.json"))
comp = sd["event_ordering"]["composite"]
check("supply-demand", "supply / demand composite (coef, SE)",
      [[round(comp["supply"][0], 3), round(comp["supply"][1], 3)],
       [round(comp["demand"][0], 3), round(comp["demand"][1], 3)]],
      [[0.456, 0.174], [0.006, 0.203]], "data/supply_demand_963e5e5.json")
check("supply-demand", "horse-race n", comp["n"], 78, "data/supply_demand_963e5e5.json")
check("supply-demand", "supply / demand onset before schooling (per cent)",
      [round(sd["supply_before_schooling_pct"], 1),
       round(sd["demand_before_schooling_pct"], 1)], [28.1, 73.0],
      "data/supply_demand_963e5e5.json")

out = dict(paper="Paper N1, revision of 2026-11-25",
           sources=dict(e6e8="research/e6e8-sequencing-2026-11-25 @ 2d19da7",
                        fee_dates="research/codex-source-verification-2026-11-25 @ 9a0fd69",
                        supply_demand="research/supply-demand-2026-11-23 @ 963e5e5",
                        sequencing="research/subsistence-v2-2026-11-23 @ ce66cfc"),
           checks=checks, n_pass=sum(1 for c in checks if c["pass_"]),
           n_fail=sum(1 for c in checks if not c["pass_"]))
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps(dict(n_pass=out["n_pass"], n_fail=out["n_fail"]), indent=1))
for c in checks:
    if not c["pass_"]:
        print("FAIL:", c)
print("wrote", OUT)
