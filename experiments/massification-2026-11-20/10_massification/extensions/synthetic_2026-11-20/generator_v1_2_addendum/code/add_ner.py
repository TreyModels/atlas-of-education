#!/usr/bin/env python3
"""add_ner.py — deterministic NER output addendum for the frozen v1.2 panel.

LABEL: SYNTHETIC. The NER columns are DERIVED from the frozen v1.2 panel's own
age split. They are not observed, not estimated, not fitted, and not evidence
about any country.

What it does
------------
Reads  ../generator_v1_2/results/synthetic_panel_v1_2.csv  (read-only) and writes

  results/synthetic_panel_v1_2_ner.csv   same 6 720 rows + NER columns
  results/NER_SMOKE.csv                  SYN00_PHL_LIKE primary NER crossings
  results/INVARIANCE_CHECKS.json         machine-readable pass-through record

Derivation (declared in PRE_DECLARATIONS.md §2):

  ner_L(c,t) = 100 * admitted_official_L(c,t) / cohort_L(c,t)

`cohort` is the model's annual official-age cohort (PARAMS.md §3); the model's
own GER uses the same denominator. `admitted_official` is the official-age
admission flow; `admitted_overage` is excluded. The result is a cohort-flow NER
analogue, not the UIS stock-based NER — see PRE_DECLARATIONS.md §2.1.

No randomness, no wall clock, no host data, no environment-dependent output.
Two runs are byte-identical. The frozen v1.2 directory is never written.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_IN = ROOT.parent / "generator_v1_2" / "results" / "synthetic_panel_v1_2.csv"
DEFAULT_OUT = ROOT / "results"

LEVELS = ("primary", "lower_secondary", "upper_secondary", "tertiary")
BASIS = "derived-from-age-structure"
EXPECTED_ROWS = 6720
EXPECTED_COLS = 67
REQUIRED_COLUMNS = (
    "country", "country_id", "year", "level", "label",
    "cohort", "enrolment", "ger", "demand_official", "demand_overage",
    "admitted_official", "admitted_overage", "out_of_school",
)
NEW_COLUMNS = (
    ["ner", "ner_basis"]
    + [f"ner_{level}" for level in LEVELS]
    + [f"ner_{level}_basis" for level in LEVELS]
)

SMOKE_COUNTRY = "SYN00_PHL_LIKE"
SMOKE_LEVEL = "primary"
SMOKE_THRESHOLDS = (90.0, 95.0)
SUSTAINED_YEARS = 5

# The frozen panel prints floats at %.10g, so recomputing 100*a/c from the
# printed columns can differ from the printed ger by a few 1e-8. 1e-6 is a
# display-rounding tolerance, not a model tolerance.
ROUNDING_TOL = 1e-6


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt(value: float) -> str:
    """v1.2 float convention (%.10g), used for every new numeric value."""
    return f"{value:.10g}"


def fail(message: str) -> "NoReturn":  # type: ignore[name-defined]
    raise SystemExit(f"add_ner.py REFUSING: {message}")


def read_panel(path: Path):
    if not path.exists():
        fail(f"input panel not found: {path}")
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if len(fieldnames) != EXPECTED_COLS:
        fail(f"expected {EXPECTED_COLS} input columns, found {len(fieldnames)}")
    missing = [c for c in REQUIRED_COLUMNS if c not in fieldnames]
    if missing:
        fail(f"missing required input columns: {missing}")
    if len(rows) != EXPECTED_ROWS:
        fail(f"expected {EXPECTED_ROWS} data rows, found {len(rows)}")
    return fieldnames, rows


def compute_ner_rows(fieldnames, rows):
    """Return (out_rows, diagnostics). Pure function of the panel strings."""
    out_rows = []
    ner_by_level = {level: [] for level in LEVELS}
    n_enrolment_bad = 0
    n_ner_gt_ger = 0
    n_cohort_nonpositive = 0
    n_negative_admitted = 0
    n_tertiary_gt_100 = 0

    for row in rows:
        if row.get("label") != "SYNTHETIC":
            fail(f"non-SYNTHETIC label in row: {row.get('label')!r}")
        level = row.get("level", "")
        if level not in LEVELS:
            fail(f"unexpected level {level!r}")
        try:
            cohort = float(row["cohort"])
            admitted = float(row["admitted_official"])
            overage = float(row["admitted_overage"])
            enrolment = float(row["enrolment"])
            ger = float(row["ger"])
            int(row["year"])
        except (TypeError, ValueError) as exc:
            fail(f"non-numeric or malformed row ({exc}): {row!r}")

        if cohort <= 0.0:
            n_cohort_nonpositive += 1
            fail(f"non-positive cohort ({cohort!r}) at {row.get('country')} "
                 f"{row.get('year')} {level}")
        if admitted < 0.0:
            n_negative_admitted += 1
            fail(f"negative admitted_official at {row.get('country')} "
                 f"{row.get('year')} {level}")

        ner = 100.0 * admitted / cohort
        ner_by_level[level].append(ner)
        if level == "tertiary" and ner > 100.0:
            n_tertiary_gt_100 += 1

        # Diagnostics: the frozen panel prints at %.10g, so allow display rounding.
        scale = max(1.0, abs(enrolment))
        if abs(enrolment - (admitted + overage)) > ROUNDING_TOL * scale:
            n_enrolment_bad += 1
        if ner > ger + ROUNDING_TOL:
            n_ner_gt_ger += 1

        new_row = dict(row)
        new_row["ner"] = fmt(ner)
        new_row["ner_basis"] = BASIS
        for target in LEVELS:
            new_row[f"ner_{target}"] = fmt(ner) if level == target else ""
            new_row[f"ner_{target}_basis"] = BASIS if level == target else ""
        out_rows.append(new_row)

    if n_enrolment_bad or n_ner_gt_ger:
        fail(f"panel consistency failure: enrolment_identity_violations="
             f"{n_enrolment_bad}, ner_gt_ger_violations={n_ner_gt_ger}")

    diagnostics = {
        "ner_min_by_level": {level: min(vals) for level, vals in ner_by_level.items()},
        "ner_max_by_level": {level: max(vals) for level, vals in ner_by_level.items()},
        "ner_ge_ger_tolerance": ROUNDING_TOL,
        "ner_ge_ger_violations": n_ner_gt_ger,
        "enrolment_identity_tolerance": ROUNDING_TOL,
        "enrolment_identity_violations": n_enrolment_bad,
        "n_tertiary_ner_gt_100": n_tertiary_gt_100,
        "n_ner_negative": 0 if all(
            v >= 0.0 for vals in ner_by_level.values() for v in vals) else 1,
        "n_cohort_nonpositive": n_cohort_nonpositive,
        "n_negative_admitted": n_negative_admitted,
    }
    return out_rows, diagnostics


def write_panel(out_path: Path, fieldnames, out_rows) -> None:
    out_fields = list(fieldnames) + NEW_COLUMNS
    with open(out_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=out_fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(out_rows)


def verify_pass_through(in_path: Path, out_path: Path, fieldnames) -> dict:
    """Re-read input and output; assert same rows, same order, same old columns."""
    with open(in_path, newline="") as fh:
        in_rows = list(csv.DictReader(fh))
    with open(out_path, newline="") as fh:
        reader = csv.DictReader(fh)
        out_fields = list(reader.fieldnames or [])
        out_rows = list(reader)

    if len(in_rows) != len(out_rows):
        fail(f"row count changed: {len(in_rows)} -> {len(out_rows)}")
    if out_fields[:len(fieldnames)] != list(fieldnames):
        fail("pre-existing column order changed")
    if out_fields[len(fieldnames):] != NEW_COLUMNS:
        fail("appended column order does not match NEW_COLUMNS")

    keys = ("country", "country_id", "year", "level")
    for idx, (old, new) in enumerate(zip(in_rows, out_rows)):
        if tuple(old[k] for k in keys) != tuple(new[k] for k in keys):
            fail(f"row order/key changed at data row {idx + 2}")
        for col in fieldnames:
            if old[col] != new[col]:
                fail(f"pre-existing column {col!r} changed at data row {idx + 2}")

    return {
        "n_rows_input": len(in_rows),
        "n_rows_output": len(out_rows),
        "n_columns_input": len(fieldnames),
        "n_columns_output": len(out_fields),
        "pre_existing_columns_identical": True,
        "row_order_identical": True,
        "all_rows_label_SYNTHETIC": all(
            r.get("label") == "SYNTHETIC" for r in out_rows),
    }


def single_sustained_crossing(series, threshold: float, run: int = SUSTAINED_YEARS):
    """First year y such that every year y..y+run-1 is >= threshold."""
    for i in range(len(series) - run + 1):
        if all(series[i + j][1] >= threshold for j in range(run)):
            return series[i][0]
    return None


def build_smoke_rows(ner_rows) -> list:
    series = sorted(
        (int(r["year"]), float(r["ner"]))
        for r in ner_rows
        if r.get("country") == SMOKE_COUNTRY and r.get("level") == SMOKE_LEVEL
    )
    if len(series) != 56:
        fail(f"smoke series expected 56 years, found {len(series)}")
    years = [y for y, _ in series]
    if years != list(range(1970, 2026)):
        fail("smoke series is not the contiguous 1970-2025 range")

    values = [v for _, v in series]
    min_idx = min(range(len(values)), key=values.__getitem__)
    max_idx = max(range(len(values)), key=values.__getitem__)
    nondecreasing = sum(1 for i in range(1, len(values)) if values[i] >= values[i - 1])
    decreases = sum(1 for i in range(1, len(values)) if values[i] < values[i - 1])
    total_steps = len(values) - 1

    smoke_rows = []
    for threshold in SMOKE_THRESHOLDS:
        first_at = next((y for y, v in series if v >= threshold), None)
        sustained = single_sustained_crossing(series, threshold)
        n_ge = sum(1 for v in values if v >= threshold)
        if sustained is None:
            note = (f"no {SUSTAINED_YEARS}-year sustained crossing by 2025; "
                    "smoke test only; no HKG comparison; no verdict")
        elif first_at is not None and first_at == sustained:
            note = ("first-at-above and first-sustained coincide; "
                    "smoke test only; no HKG comparison; no verdict")
        else:
            note = (f"first-at-above {first_at} is not sustained; "
                    f"first-sustained is {sustained}; "
                    "smoke test only; no HKG comparison; no verdict")

        smoke_rows.append({
            "label": "SYNTHETIC",
            "provenance": "DERIVED",
            "basis": BASIS,
            "country": SMOKE_COUNTRY,
            "level": SMOKE_LEVEL,
            "measure": "ner_primary",
            "threshold": fmt(threshold),
            "first_at_or_above_year": "" if first_at is None else first_at,
            "first_sustained_5y_year": "" if sustained is None else sustained,
            "n_years_ge_threshold": n_ge,
            "pct_years_ge_threshold": fmt(100.0 * n_ge / len(values)),
            "series_start": years[0],
            "series_end": years[-1],
            "min_ner": fmt(values[min_idx]),
            "min_year": years[min_idx],
            "max_ner": fmt(values[max_idx]),
            "max_year": years[max_idx],
            "monotone_non_decreasing_steps": nondecreasing,
            "n_decreases": decreases,
            "is_monotone_non_decreasing": "true" if decreases == 0 else "false",
            "total_year_steps": total_steps,
            "note": note,
        })
    return smoke_rows


def write_smoke(path: Path, smoke_rows: list) -> None:
    fields = [
        "label", "provenance", "basis", "country", "level", "measure",
        "threshold", "first_at_or_above_year", "first_sustained_5y_year",
        "n_years_ge_threshold", "pct_years_ge_threshold",
        "series_start", "series_end",
        "min_ner", "min_year", "max_ner", "max_year",
        "monotone_non_decreasing_steps", "n_decreases",
        "is_monotone_non_decreasing", "total_year_steps", "note",
    ]
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(smoke_rows)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Add NER columns to the frozen v1.2 panel.")
    parser.add_argument("--in", dest="in_path", default=str(DEFAULT_IN),
                        help="frozen v1.2 panel (read-only)")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT),
                        help="output directory (default: addendum/results)")
    args = parser.parse_args(argv)

    in_path = Path(args.in_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    fieldnames, rows = read_panel(in_path)
    out_rows, diagnostics = compute_ner_rows(fieldnames, rows)

    out_path = out_dir / "synthetic_panel_v1_2_ner.csv"
    write_panel(out_path, fieldnames, out_rows)

    pass_through = verify_pass_through(in_path, out_path, fieldnames)

    smoke_path = out_dir / "NER_SMOKE.csv"
    smoke_rows = build_smoke_rows(out_rows)
    write_smoke(smoke_path, smoke_rows)

    record = {
        "label": "SYNTHETIC",
        "provenance": "DERIVED",
        "basis": BASIS,
        "statement": ("NER is derived from the frozen v1.2 panel's official-age "
                      "admission / official-age cohort split. Not observed, not an "
                      "estimate, not a forecast, no causal or direction claim."),
        "input_file": in_path.name,
        "input_sha256": sha256_file(in_path),
        "output_file": out_path.name,
        "output_sha256": sha256_file(out_path),
        "smoke_file": smoke_path.name,
        "smoke_sha256": sha256_file(smoke_path),
        "new_columns": NEW_COLUMNS,
        "smoke_thresholds": [fmt(t) for t in SMOKE_THRESHOLDS],
        "smoke_sustained_rule": f">= {SUSTAINED_YEARS} consecutive years at/above",
        **pass_through,
        **diagnostics,
        "checks": {
            "b_panel_pass_through": "PASS",
            "c_addendum_deterministic_by_construction": "two clean runs compared by sha256",
        },
    }
    record_path = out_dir / "INVARIANCE_CHECKS.json"
    record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")

    print(f"[add_ner] {len(out_rows)} rows; new columns: {', '.join(NEW_COLUMNS)}")
    print(f"[add_ner] panel: {out_path}")
    print(f"[add_ner] smoke: {smoke_path}")
    print(f"[add_ner] record: {record_path}")
    for row in smoke_rows:
        print(f"[add_ner] threshold>={row['threshold']}: first_at="
              f"{row['first_at_or_above_year'] or 'none'} "
              f"sustained5={row['first_sustained_5y_year'] or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
