#!/usr/bin/env python3
"""Erratum check — does the REPORT's "18-33% strict schooling-first" clause reproduce?

Reads the committed `results/e6_summary.json` (produced by `scripts/e6_demand_timing.py`) and
recomputes the strict schooling-first share (the E6 "reverse" category: schooling take-off before
demand take-off) under four denominators, for the four pre-1990 full-overlap proxies used in the
REPORT's "Reading" paragraph. Writes `results/erratum_check.json`.

Definitions taken verbatim from `e6_summary.json`:
  forward            = demand take-off first (strict)
  reverse            = schooling take-off first (strict)  <- the "schooling-first" share
  forward_or_tie     = weak forward ordering (demand at or before schooling, weak inequality)
  undetermined       = no ordering inside the window
  n_in_window        = countries with both series in the window
  n_all              = all countries with both series

Erratum context: REPORT.md line 53 states "(18-33% strict schooling-first, with the remainder weak
ties or undetermined)". This script shows the clause does not reproduce under any of the four
denominators; the paper-facing replacement range is 21.5-46.3% of identifiable countries.

Run: python3 scripts/erratum_check_e6_prose.py   (stdlib only)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.dirname(HERE)
rows = json.load(open(os.path.join(REC, "results", "e6_summary.json")))

proxies = {
    "ggdc_nonag_emp": "GGDC non-agricultural employment",
    "urban": "WDI urbanisation",
    "ind_va": "WDI industry value added",
    "agri_va": "WDI agricultural value added (falling)",
}

out_rows = {}
for r in rows:
    if r["window"] != "1900-2012" or r["proxy"] not in proxies:
        continue
    ident = r["forward"] + r["reverse"] + r["forward_or_tie"]
    strict = r["forward"] + r["reverse"]
    out_rows[r["proxy"]] = dict(
        label=proxies[r["proxy"]],
        n_all=r["n_all"], n_in_window=r["n_in_window"],
        forward=r["forward"], reverse=r["reverse"],
        forward_or_tie=r["forward_or_tie"], undetermined=r["undetermined"],
        identifiable=ident, strict_orderings=strict,
        share_identifiable=round(100.0 * r["reverse"] / ident, 2),
        share_in_window=round(100.0 * r["reverse"] / r["n_in_window"], 2),
        share_all=round(100.0 * r["reverse"] / r["n_all"], 2),
        share_strict_only=round(100.0 * r["reverse"] / strict, 2),
        demand_first_share_identifiable=round(100.0 * r["forward"] / ident, 2),
        weak_forward_share_in_window=round(100.0 * r["forward_or_tie"] / r["n_in_window"], 2),
    )


def rng(key):
    vals = [v[key] for v in out_rows.values()]
    return [min(vals), max(vals)]


out = dict(
    question='Does "(18-33% strict schooling-first)" reproduce from results/e6_summary.json?',
    answer="NO — no denominator below yields a range whose endpoints are 18 and 33.",
    source="results/e6_summary.json (E6, pre-1990 full-overlap 1900-2012 rows)",
    by_proxy=out_rows,
    ranges=dict(
        share_identifiable=rng("share_identifiable"),
        share_in_window=rng("share_in_window"),
        share_all=rng("share_all"),
        share_strict_only=rng("share_strict_only"),
        demand_first_share_identifiable=rng("demand_first_share_identifiable"),
        weak_forward_share_in_window=rng("weak_forward_share_in_window"),
    ),
    corrected_reading=(
        "Schooling-first is the larger strict ordering in all four proxies but not a majority of "
        "identifiable countries: 21.5-46.3% of identifiable countries versus demand-first 10.0-24.1%; "
        "58.3-71.4% of strict orderings; the remainder (21-43% of in-window countries) is weak ties or "
        "left-censored. Correct the REPORT's 'majority' wording to 'larger strict ordering': it is a "
        "majority only among strict orderings (58.3-71.4%), not among identifiable countries."
    ),
    reproduces="scripts/erratum_check_e6_prose.py (this record); cross-checked by "
              "research/paper-massification-2026-11-25 @ fb9f419 "
              "scripts/verify_revision_numbers.py (21.5-46.3% of identifiable countries).",
)

json.dump(out, open(os.path.join(REC, "results", "erratum_check.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
