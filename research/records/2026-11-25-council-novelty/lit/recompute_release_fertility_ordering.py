#!/usr/bin/env python3
"""Recompute both event orderings from the committed event-dates CSV.

Companion to Paper M's scripts/recompute_fertility_ordering.py: this one adds the
release-vs-fertility ordering on BOTH samples, plus the schooling-vs-fertility
ordering on the 64 three-event sample, so the Council figure has a committed
recompute artefact next to the data (the 68.75% failure mode was an un-committed
recompute).

Source: `research/paper-massification-2026-11-25` @ `76d929a`
        research/records/2026-11-25-paper-massification/data/event_dates_subsistence_v2.csv
Copy:   this record's data/event_dates_subsistence_v2.csv (sha256 recorded in output).

Definitions: strict ordering compares event years; equal years are ties
("simultaneous"); a gap is (second event year - first event year), so a negative
schooling-fertility gap means schooling came first. Wilson 95% intervals.
"""
import csv, hashlib, json, os, statistics
from math import sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "..", "data", "event_dates_subsistence_v2.csv")
OUT = os.path.join(HERE, "release_fertility_ordering.json")

def wilson(k, n):
    if n == 0: return [None, None]
    z = 1.959963984540054
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 4), round(c + h, 4)]

def load():
    rows = list(csv.DictReader(open(CSV)))
    def num(v):
        try: return float(v) if v not in (None, "") else None
        except ValueError: return None
    for r in rows:
        for k in ("release", "schooling", "fertility"):
            r[k] = num(r[k])
    return rows

def ordering(a_name, b_name, rows, label):
    pairs = [r for r in rows if r[a_name] is not None and r[b_name] is not None]
    a_first = [r for r in pairs if r[a_name] < r[b_name]]
    b_first = [r for r in pairs if r[b_name] < r[a_name]]
    ties = [r for r in pairs if r[a_name] == r[b_name]]
    gaps = [r[b_name] - r[a_name] for r in pairs]
    return dict(label=label, n=len(pairs),
                a_first=len(a_first), a_first_share=round(len(a_first) / len(pairs), 4),
                a_first_ci95=wilson(len(a_first), len(pairs)),
                b_first=len(b_first), b_first_share=round(len(b_first) / len(pairs), 4),
                b_first_ci95=wilson(len(b_first), len(pairs)),
                ties=len(ties), ties_share=round(len(ties) / len(pairs), 4),
                median_gap=statistics.median(gaps) if gaps else None,
                iqr_gap=[statistics.quantiles(gaps, n=4)[0], statistics.quantiles(gaps, n=4)[2]] if len(gaps) > 3 else None,
                a_first_countries=sorted(r["iso3"] for r in a_first),
                b_first_countries=sorted(r["iso3"] for r in b_first))

def main():
    rows = load()
    three = [r for r in rows if all(r[k] is not None for k in ("release", "schooling", "fertility"))]
    both_release_fert = [r for r in rows if r["release"] is not None and r["fertility"] is not None]
    both_school_fert = [r for r in rows if r["schooling"] is not None and r["fertility"] is not None]
    out = dict(
        source="research/paper-massification-2026-11-25 @ 76d929a, "
               "research/records/2026-11-25-paper-massification/data/event_dates_subsistence_v2.csv",
        csv_sha256=hashlib.sha256(open(CSV, "rb").read()).hexdigest(),
        n_rows=len(rows),
        samples=dict(three_event=len(three), both_release_fertility=len(both_release_fert),
                     both_schooling_fertility=len(both_school_fert)),
        schooling_vs_fertility_three_event=ordering("schooling", "fertility", three, "schooling vs fertility, 64 three-event"),
        schooling_vs_fertility_both_dates=ordering("schooling", "fertility", both_school_fert, "schooling vs fertility, both dates"),
        release_vs_fertility_three_event=ordering("release", "fertility", three, "release vs fertility, 64 three-event"),
        release_vs_fertility_both_dates=ordering("release", "fertility", both_release_fert, "release vs fertility, both dates"),
        note="Negative gap means the first-named event (schooling or release) came first; ties counted separately.")
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: out[k] for k in ("samples",)}, indent=1))
    for k in ("schooling_vs_fertility_three_event", "schooling_vs_fertility_both_dates",
              "release_vs_fertility_three_event", "release_vs_fertility_both_dates"):
        v = out[k]
        print(f"{k}: n={v['n']} schooling/release-first={v['a_first']} ({v['a_first_share']:.2%}, CI {v['a_first_ci95']}) "
              f"fertility-first={v['b_first']} ({v['b_first_share']:.2%}) ties={v['ties']} median_gap={v['median_gap']}")

if __name__ == "__main__":
    main()
