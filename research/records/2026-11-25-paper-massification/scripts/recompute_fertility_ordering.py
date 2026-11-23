#!/usr/bin/env python3
"""Recompute the schooling-vs-fertility ordering from the committed subsistence-v2 event CSV.

The source record's JSON reports pct_schooling_before_fertility = 68.75, but its own CSV gives a
different picture because the JSON counts simultaneous take-offs (ties) as "schooling first".
This script recomputes the strict ordering, the tie share, the median gap and bootstrap intervals,
and writes data/recompute_fertility_ordering.json.

Input: data/event_dates_subsistence_v2.csv (verbatim copy of
research/subsistence-v2-2026-11-23:research/records/2026-11-23-subsistence-v2/results/event_dates.csv @ ce66cfc).
"""
import csv, json, numpy as np

SRC = "data/event_dates_subsistence_v2.csv"
OUT = "data/recompute_fertility_ordering.json"

def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None

rows = list(csv.DictReader(open(SRC)))
complete = [r for r in rows if all(num(r.get(c)) is not None for c in ("schooling", "release", "fertility"))]
pairs64 = [(num(r["schooling"]), num(r["fertility"])) for r in complete]
allpairs = [(num(r["schooling"]), num(r["fertility"])) for r in rows
            if num(r.get("schooling")) is not None and num(r.get("fertility")) is not None]

def summarise(pairs, rng, label):
    n = len(pairs)
    sfirst = sum(1 for a, b in pairs if a < b)
    ffirst = sum(1 for a, b in pairs if b < a)
    ties = sum(1 for a, b in pairs if a == b)
    gaps = np.array([b - a for a, b in pairs])
    boots = []
    for _ in range(1000):
        idx = rng.integers(0, n, n)
        boots.append(sum(1 for i in idx if pairs[i][0] < pairs[i][1]) / n)
    boots = np.array(boots)
    return dict(label=label, n=n,
                schooling_first=sfirst, share=round(100 * sfirst / n, 2),
                share_ci95=[round(100 * float(np.percentile(boots, 2.5)), 2),
                            round(100 * float(np.percentile(boots, 97.5)), 2)],
                ties=ties, ties_share=round(100 * ties / n, 2),
                fertility_first=ffirst, fertility_first_share=round(100 * ffirst / n, 2),
                median_gap_fertility_minus_schooling=float(np.median(gaps)),
                iqr_gap=[float(np.percentile(gaps, 25)), float(np.percentile(gaps, 75))])

rng = np.random.default_rng(7)
out = {
    "source_csv": SRC,
    "source_record": "subsistence-v2 @ ce66cfc, results/event_dates.csv",
    "definition": "schooling_first = schooling take-off year < fertility decline year (strict; ties simultaneous)",
    "json_field_in_record": "pct_schooling_before_fertility = 68.75 (44/64; counts the 20 ties as schooling-first)",
    "three_event_sample": summarise(pairs64, rng, "64 countries with all three events"),
    "all_with_both_dates": summarise(allpairs, rng, "all countries with schooling and fertility dates"),
}
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps(out, indent=1))
