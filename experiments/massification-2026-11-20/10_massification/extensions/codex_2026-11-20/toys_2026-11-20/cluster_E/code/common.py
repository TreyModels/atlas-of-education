"""Shared helpers for the Cluster E toy experiments (Python 3, stdlib only).

ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence.

Every row written by these scripts carries LABEL. The helper functions only do
arithmetic and CSV plumbing; no model logic lives here.
"""
import csv
import math
import statistics

LABEL = ("ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence; "
         "no historical test; phase closed; do not cite numbers as estimates")

Z_975 = 1.959963984540054

COLUMNS = ["experiment", "cell", "contrast", "metric", "group", "n_seeds", "value",
           "sd", "ci_low", "ci_high", "unit", "threshold_id", "threshold_value",
           "verdict", "label", "definition"]


def mean(xs):
    return sum(xs) / len(xs)


def sd(xs):
    return statistics.stdev(xs) if len(xs) > 1 else 0.0


def summary(xs):
    """Mean, sample sd and a normal-approximation 95% CI of the mean."""
    m = mean(xs)
    s = sd(xs)
    half = Z_975 * s / math.sqrt(len(xs)) if len(xs) > 1 else 0.0
    return m, s, m - half, m + half


def row(experiment, cell, contrast, metric, group, xs, unit, definition,
        threshold_id="", threshold_value="", verdict=""):
    """One RESULTS.csv row from a list of per-seed values."""
    if not xs:
        raise ValueError("empty series")
    m, s, lo, hi = summary(xs)
    return dict(experiment=experiment, cell=cell, contrast=contrast, metric=metric,
                group=group, n_seeds=len(xs), value=f"{m:.6f}", sd=f"{s:.6f}",
                ci_low=f"{lo:.6f}", ci_high=f"{hi:.6f}", unit=unit,
                threshold_id=threshold_id, threshold_value=threshold_value,
                verdict=verdict, label=LABEL, definition=definition)


def verdict(checks):
    """PASS only if every predeclared sub-condition holds."""
    return "PASS" if all(checks) else "FAIL"


def write_csv(rows, path):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)
