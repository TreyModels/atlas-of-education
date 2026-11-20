#!/usr/bin/env python3
"""run_m1_ner.py — EXP-3 M1-NER: construct equivalence of the cohort-flow NER analogue.

LABEL: SYNTHETIC / DERIVED. Reads the delivered v1.2.1 NER panel read-only and
computes:

  flow(c,L,t)  = the panel's `ner` column (100 * admitted_official / cohort)
  stock(c,L,t) = 100 * mean over the last dur_L years of admitted_official / cohort
  diff         = stock - flow   [pp]

and decides H1 on the predeclared verdict series SYN00_PHL_LIKE / primary:
  Condition B (band): |diff| <= 2.0 pp in every year with flow in [85, 95]
  Condition C (crossing): first-sustained 5-year crossing years at 90 and 95
                          differ by <= 1 y
  ADMISSIBLE iff B and C both hold.

Observed HKG/PHL series are computed separately and labelled
OBSERVED-REFERENCE-ONLY. They are construct references, not validation, and are
never compared with the synthetic targets.

Deterministic: no RNG, no clock, no network, no environment dependence.
Two runs must be byte-identical.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# frozen declarations
# ---------------------------------------------------------------------------

LEVELS = ("primary", "lower_secondary", "upper_secondary", "tertiary")
DUR = {"primary": 6, "lower_secondary": 3, "upper_secondary": 3, "tertiary": 4}

YEAR_START, YEAR_END = 1970, 2025
BAND_LO, BAND_HI = 85.0, 95.0
PP_BAR = 2.0
FLOAT_TOL = 1e-9
SUSTAINED_YEARS = 5
THRESHOLDS = (90.0, 95.0)

VERDICT_COUNTRY = "SYN00_PHL_LIKE"
VERDICT_LEVEL = "primary"

HKG_WINDOW = (1971, 1996)

EXPECTED_PREDECL_SHA = "9eb35a92c8f3f12b723bc0a7bf1240e61bd48580d463b7dc90240512f938d78f"
EXPECTED_PANEL_SHA = "c6d1f9b059b5a48cbd5a4aaf7e1c4611cad781819b74987988897e8d35e40294"

LABEL_SYN = "SYNTHETIC"
PROV_DERIVED = "DERIVED"
LABEL_REF = "OBSERVED-REFERENCE-ONLY"
PROV_OBS = "OBSERVED"

ROOT = Path(__file__).resolve().parent.parent
PROG = ROOT.parents[2]
SYNTH = ROOT.parent / "synthetic_2026-11-20"
PANEL = SYNTH / "generator_v1_2_addendum" / "results" / "synthetic_panel_v1_2_ner.csv"
OBS_GMR = PROG / "data" / "gmr_observed_6countries_1970_2024.csv"
UNIV = PROG / "10_massification" / "data" / "UNIVERSALIZATION_SERIES.csv"

REQUIRED_PANEL_COLUMNS = (
    "country", "year", "level", "label", "cohort", "admitted_official",
    "enrolment", "ger", "ner", "ner_primary",
)


def fail(message: str) -> "NoReturn":  # type: ignore[name-defined]
    raise SystemExit(f"run_m1_ner.py REFUSING: {message}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def f6(value: float) -> str:
    return f"{value:.6f}"


def f10(value: float) -> str:
    return f"{value:.10g}"


def year_str(value) -> str:
    return "none_by_2025" if value is None else str(int(value))


# ---------------------------------------------------------------------------
# panel input
# ---------------------------------------------------------------------------

def load_panel(path: Path):
    if not path.exists():
        fail(f"panel not found: {path}")
    actual = sha256_file(path)
    if actual != EXPECTED_PANEL_SHA:
        fail(f"panel sha256 mismatch: expected {EXPECTED_PANEL_SHA}, got {actual}")

    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        fields = list(reader.fieldnames or [])
        raw = list(reader)

    missing = [c for c in REQUIRED_PANEL_COLUMNS if c not in fields]
    if missing:
        fail(f"missing required panel columns: {missing}")
    if len(raw) != 6720:
        fail(f"expected 6720 panel rows, found {len(raw)}")

    panel: dict = {}
    for r in raw:
        if r.get("label") != LABEL_SYN:
            fail(f"non-SYNTHETIC label: {r.get('label')!r}")
        level = r.get("level")
        if level not in LEVELS:
            fail(f"unexpected level: {level!r}")
        try:
            year = int(r["year"])
            flow = float(r["ner"])
            admitted = float(r["admitted_official"])
            cohort = float(r["cohort"])
        except (TypeError, ValueError) as exc:
            fail(f"malformed row ({exc}): {r!r}")
        if cohort <= 0.0:
            fail(f"non-positive cohort at {r['country']} {year} {level}")
        if admitted < 0.0:
            fail(f"negative admitted_official at {r['country']} {year} {level}")
        # The panel prints floats at %.10g; 1e-6 is display-rounding tolerance.
        rederived = 100.0 * admitted / cohort
        if abs(rederived - flow) > 1e-6 * max(1.0, abs(flow)):
            fail(f"flow identity violated at {r['country']} {year} {level}: "
                 f"ner={flow!r} vs 100*a/c={rederived!r}")
        key = (r["country"], level)
        if year in panel.get(key, {}):
            fail(f"duplicate row at {key} {year}")
        panel.setdefault(key, {})[year] = {
            "flow": flow,
            "admitted": admitted,
            "cohort": cohort,
        }

    years = set(range(YEAR_START, YEAR_END + 1))
    if len(panel) != 120:
        fail(f"expected 120 country-level series, found {len(panel)}")
    for key, series in panel.items():
        if set(series) != years:
            fail(f"series {key} is not the contiguous 1970-2025 range")
    return panel


def stock_series(series: dict, dur: int):
    """Return [(year, stock)] where the full dur-year window exists, ascending."""
    out = []
    for year in sorted(series):
        window = range(year - dur + 1, year + 1)
        if any(y not in series for y in window):
            continue
        stock = 100.0 * sum(series[y]["admitted"] / series[y]["cohort"]
                            for y in window) / dur
        out.append((year, stock))
    return out


def stock_at(series: dict, year: int, dur: int):
    window = range(year - dur + 1, year + 1)
    if any(y not in series for y in window):
        return None
    return 100.0 * sum(series[y]["admitted"] / series[y]["cohort"]
                       for y in window) / dur


def band_rows(panel: dict, key):
    """All in-band years for a series, including years where stock is undefined."""
    series = panel[key]
    dur = DUR[key[1]]
    rows = []
    for year in sorted(series):
        flow = series[year]["flow"]
        if not (BAND_LO <= flow <= BAND_HI):
            continue
        stock = stock_at(series, year, dur)
        prev = series.get(year - 1)
        if prev is None:
            direction = "unknown"
        elif flow > prev["flow"]:
            direction = "expanding"
        elif flow < prev["flow"]:
            direction = "contracting"
        else:
            direction = "flat"
        rows.append({
            "country": key[0],
            "level": key[1],
            "year": year,
            "flow": flow,
            "stock": stock,
            "diff": None if stock is None else stock - flow,
            "direction": direction,
        })
    return rows


def series_id(key) -> str:
    return f"{key[0]}/{key[1]}"


def first_at_or_above(pairs, threshold: float):
    for year, value in pairs:
        if value >= threshold:
            return year
    return None


def first_sustained(pairs, threshold: float, run: int = SUSTAINED_YEARS):
    values = [v for _, v in pairs]
    for i in range(len(values) - run + 1):
        if all(v >= threshold for v in values[i:i + run]):
            return pairs[i][0]
    return None


def crossing_summary(pairs, threshold: float):
    return {
        "first_at": first_at_or_above(pairs, threshold),
        "sustained": first_sustained(pairs, threshold),
    }


def plus_years(pairs) -> str:
    return "+".join(str(y) for y, _ in pairs)


# ---------------------------------------------------------------------------
# results rows
# ---------------------------------------------------------------------------

def result_row(test, statistic, threshold, verdict, n, series, note):
    return {
        "test": test,
        "statistic": statistic,
        "threshold": threshold,
        "verdict": verdict,
        "n": str(n),
        "label": LABEL_SYN,
        "provenance": PROV_DERIVED,
        "series": series,
        "note": note,
    }


def build_results(panel: dict):
    key = (VERDICT_COUNTRY, VERDICT_LEVEL)
    rows = band_rows(panel, key)
    complete = [r for r in rows if r["stock"] is not None]
    incomplete = [r for r in rows if r["stock"] is None]

    result_rows = []

    if complete:
        worst = max(complete, key=lambda r: (abs(r["diff"]), -r["year"]))
        max_abs = abs(worst["diff"])
        violations = [r for r in complete if abs(r["diff"]) > PP_BAR + FLOAT_TOL]
        band_met = not violations
        result_rows.append(result_row(
            "band_agreement", f6(max_abs), "2.0",
            "MET" if band_met else "NOT MET", len(complete), series_id(key),
            f"max |stock-flow| in the 85-95 band at {worst['year']} "
            f"(stock={f6(worst['stock'])}, flow={f6(worst['flow'])})"))
        result_rows.append(result_row(
            "band_agreement_violations", str(len(violations)), "0",
            "MET" if not violations else "NOT MET", len(complete), series_id(key),
            "years with |stock-flow| > 2.0 pp: "
            + (", ".join(str(r["year"]) for r in violations) or "none")))
        result_rows.append(result_row(
            "band_agreement_max_abs_diff_year", str(worst["year"]), "",
            "REPORTED", 1, series_id(key), "year of the maximum |stock-flow|"))
        result_rows.append(result_row(
            "band_agreement_years_excluded", str(len(incomplete)), "",
            "REPORTED", len(incomplete), series_id(key),
            "in-band years excluded because the 6-year stock window is incomplete "
            "(1970-1974): " + (", ".join(str(r["year"]) for r in incomplete) or "none")
            + "; predeclared exclusion, predecl section 4.1"))
    else:
        band_met = False
        result_rows.append(result_row(
            "band_agreement", "undefined", "2.0", "UNDETERMINED", 0,
            series_id(key), "no complete-window in-band year"))

    flow_pairs = [(y, panel[key][y]["flow"]) for y in sorted(panel[key])]
    stock_pairs = stock_series(panel[key], DUR[VERDICT_LEVEL])
    flow_cross = {t: crossing_summary(flow_pairs, t) for t in THRESHOLDS}
    stock_cross = {t: crossing_summary(stock_pairs, t) for t in THRESHOLDS}

    crossing_met = {}
    for threshold in THRESHOLDS:
        f = flow_cross[threshold]["sustained"]
        s = stock_cross[threshold]["sustained"]
        label = f"crossing_{int(threshold)}"
        if f is None and s is None:
            crossing_met[threshold] = True
            result_rows.append(result_row(
                label, "undefined", "1", "MET", 1, series_id(key),
                "both analogues have no 5-year sustained crossing by 2025; "
                "declared as MET (neither crosses)"))
        elif f is None or s is None:
            crossing_met[threshold] = False
            missing = "flow" if f is None else "stock"
            result_rows.append(result_row(
                label, "undefined", "1", "NOT MET", 1, series_id(key),
                f"{missing} has no 5-year sustained crossing by 2025; "
                "an undefined difference cannot meet the <= 1 y bar"))
        else:
            delta = abs(s - f)
            crossing_met[threshold] = delta <= 1
            result_rows.append(result_row(
                label, str(delta), "1",
                "MET" if crossing_met[threshold] else "NOT MET", 1,
                series_id(key),
                f"flow first-sustained {f}, stock first-sustained {s}"))
        result_rows.append(result_row(
            f"{label}_flow_year", year_str(f), "", "REPORTED", 1,
            series_id(key), "flow analogue first-sustained 5-year crossing"))
        result_rows.append(result_row(
            f"{label}_stock_year", year_str(s), "", "REPORTED", 1,
            series_id(key), "stock analogue first-sustained 5-year crossing"))

    overall = band_met and all(crossing_met.values())
    failed = []
    if not band_met:
        failed.append("Condition B (band)")
    if not all(crossing_met.values()):
        failed.append("Condition C (crossing)")
    result_rows.append(result_row(
        "h1_overall", "1" if overall else "0", "B and C",
        "ADMISSIBLE" if overall else "NOT ADMISSIBLE",
        len(complete), series_id(key),
        "both conditions hold" if overall else "failed: " + "; ".join(failed)))

    # declared expected sign (descriptive)
    expansion = [r for r in complete
                 if r["year"] - 1 in panel[key]
                 and panel[key][r["year"]]["flow"] > panel[key][r["year"] - 1]["flow"]]
    if expansion:
        lead = sum(1 for r in expansion if r["diff"] <= 0.0)
        counter = [r for r in expansion if r["diff"] > 0.0]
        mean_diff = sum(r["diff"] for r in expansion) / len(expansion)
        result_rows.append(result_row(
            "expected_sign_share_expansion", f6(lead / len(expansion)), "",
            "DESCRIPTIVE", len(expansion), series_id(key),
            "share of band expansion years with flow >= stock (diff <= 0); "
            f"counter-sign years: "
            + (", ".join(str(r["year"]) for r in counter) or "none")))
        result_rows.append(result_row(
            "expected_sign_mean_diff_expansion", f6(mean_diff), "",
            "DESCRIPTIVE", len(expansion), series_id(key),
            "mean stock-flow (pp) over band expansion years; negative = flow leads"))
        result_rows.append(result_row(
            "expected_sign_counter_years", str(len(counter)), "",
            "DESCRIPTIVE", len(expansion), series_id(key),
            "band expansion years with flow < stock (counter to declared sign)"))
    else:
        result_rows.append(result_row(
            "expected_sign_share_expansion", "undefined", "",
            "DESCRIPTIVE", 0, series_id(key), "no band expansion years"))

    # panel-wide sensitivity (descriptive, not verdict-bearing)
    sens = []
    sens_cross = {t: [] for t in THRESHOLDS}
    for skey in sorted(panel, key=lambda k: (k[0], LEVELS.index(k[1]))):
        for r in band_rows(panel, skey):
            if r["stock"] is not None:
                sens.append(r)
        fp = [(y, panel[skey][y]["flow"]) for y in sorted(panel[skey])]
        sp = stock_series(panel[skey], DUR[skey[1]])
        for t in THRESHOLDS:
            sens_cross[t].append((skey, crossing_summary(fp, t),
                                  crossing_summary(sp, t)))

    if sens:
        sworst = max(sens, key=lambda r: (abs(r["diff"]), r["country"], r["level"]))
        sviol = [r for r in sens if abs(r["diff"]) > PP_BAR + FLOAT_TOL]
        by_series = {}
        for r in sviol:
            by_series.setdefault((r["country"], r["level"]), 0)
            by_series[(r["country"], r["level"])] += 1
        result_rows.append(result_row(
            "sensitivity_max_abs_diff", f6(abs(sworst["diff"])), "2.0",
            "DESCRIPTIVE", len(sens), "all_series",
            f"panel-wide max at {sworst['country']}/{sworst['level']} "
            f"{sworst['year']}; descriptive only, not verdict-bearing"))
        result_rows.append(result_row(
            "sensitivity_violation_series_years", str(len(sviol)), "0",
            "DESCRIPTIVE", len(sens), "all_series",
            "panel-wide series-years with |stock-flow| > 2.0 pp"))
        result_rows.append(result_row(
            "sensitivity_series_with_violation", str(len(by_series)), "0",
            "DESCRIPTIVE", len(sens), "all_series",
            "series with at least one > 2.0 pp band year: "
            + (", ".join(f"{c}/{l}" for c, l in sorted(by_series)) or "none")))

    for t in THRESHOLDS:
        both = 0
        within = 0
        ge2 = 0
        one_missing = 0
        both_missing = 0
        for _, fc, sc in sens_cross[t]:
            f = fc["sustained"]
            s = sc["sustained"]
            if f is None and s is None:
                both_missing += 1
            elif f is None or s is None:
                one_missing += 1
            else:
                both += 1
                delta = abs(s - f)
                if delta <= 1:
                    within += 1
                if delta >= 2:
                    ge2 += 1
        result_rows.append(result_row(
            f"sensitivity_crossing_{int(t)}_both_defined_within_1y",
            str(within), "1", "DESCRIPTIVE", both, "all_series",
            f"of {both} series with both crossings defined; "
            f"{ge2} differ by >= 2 y; {one_missing} have exactly one missing; "
            f"{both_missing} have both missing"))
        result_rows.append(result_row(
            f"sensitivity_crossing_{int(t)}_diff_ge_2y", str(ge2), "1",
            "DESCRIPTIVE", both, "all_series",
            "series with both crossings defined and |difference| >= 2 y"))

    return result_rows, complete, incomplete, flow_cross, stock_cross, sens


# ---------------------------------------------------------------------------
# writers
# ---------------------------------------------------------------------------

COMPARISON_FIELDS = [
    "label", "provenance", "window_role", "series_id", "country", "level",
    "year", "flow_ner", "stock_ner", "stock_minus_flow_pp", "abs_diff_pp",
    "bar_2pp_met", "flow_direction", "stock_window_years", "note",
]

CROSSING_FIELDS = [
    "label", "provenance", "window_role", "series_id", "country", "level",
    "threshold", "flow_first_at_or_above", "flow_first_sustained_5y",
    "stock_first_at_or_above", "stock_first_sustained_5y",
    "abs_crossing_difference_y", "bar_1y_met", "note",
]

RESULT_FIELDS = [
    "test", "statistic", "threshold", "verdict", "n", "label", "provenance",
    "series", "note",
]

REFERENCE_FIELDS = [
    "row_type", "label", "provenance", "reference_id", "country", "iso3",
    "indicator", "threshold", "year", "value", "contiguous_block",
    "n_obs_in_block", "first_at_or_above", "first_sustained_5y", "note",
]


def write_csv(path: Path, fields, rows) -> None:
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def comparison_row(role, r, window_complete):
    key = (r["country"], r["level"])
    dur = DUR[r["level"]]
    if window_complete:
        bar = "MET" if abs(r["diff"]) <= PP_BAR + FLOAT_TOL else "NOT MET"
        note = ""
        stock = f6(r["stock"])
        diff = f6(r["diff"])
        absdiff = f6(abs(r["diff"]))
    else:
        bar = ""
        stock = ""
        diff = ""
        absdiff = ""
        note = ("flow in band but stock window incomplete (needs "
                f"{dur} years from {r['year'] - dur + 1}); excluded from the band "
                "test per predeclaration section 4.1")
    return {
        "label": LABEL_SYN,
        "provenance": PROV_DERIVED,
        "window_role": role,
        "series_id": series_id(key),
        "country": key[0],
        "level": key[1],
        "year": str(r["year"]),
        "flow_ner": f6(r["flow"]),
        "stock_ner": stock,
        "stock_minus_flow_pp": diff,
        "abs_diff_pp": absdiff,
        "bar_2pp_met": bar,
        "flow_direction": r["direction"],
        "stock_window_years": f"{r['year'] - dur + 1}-{r['year']}",
        "note": note,
    }


def crossing_row(role, key, threshold, fc, sc):
    f = fc["sustained"]
    s = sc["sustained"]
    if f is None and s is None:
        delta = ""
        bar = "BOTH-NONE"
        note = "neither analogue has a 5-year sustained crossing by 2025"
    elif f is None or s is None:
        delta = ""
        bar = "ONE-NONE"
        note = ("flow" if f is None else "stock") + " has no 5-year sustained crossing"
    else:
        delta = str(abs(s - f))
        bar = "MET" if abs(s - f) <= 1 else "NOT MET"
        note = ""
    return {
        "label": LABEL_SYN,
        "provenance": PROV_DERIVED,
        "window_role": role,
        "series_id": series_id(key),
        "country": key[0],
        "level": key[1],
        "threshold": str(int(threshold)),
        "flow_first_at_or_above": year_str(fc["first_at"]),
        "flow_first_sustained_5y": year_str(f),
        "stock_first_at_or_above": year_str(sc["first_at"]),
        "stock_first_sustained_5y": year_str(s),
        "abs_crossing_difference_y": delta,
        "bar_1y_met": bar,
        "note": note,
    }


# ---------------------------------------------------------------------------
# observed references (REFERENCE-ONLY)
# ---------------------------------------------------------------------------

def read_observed():
    if not OBS_GMR.exists():
        fail(f"observed GMR file not found: {OBS_GMR}")
    if not UNIV.exists():
        fail(f"UNIVERSALIZATION_SERIES not found: {UNIV}")

    hkg = {}
    with open(OBS_GMR, newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("iso3") != "HKG":
                continue
            ind = r.get("indicator")
            if ind not in ("ner_primary", "aner_primary"):
                continue
            year = int(r["year"])
            if not (HKG_WINDOW[0] <= year <= HKG_WINDOW[1]):
                continue
            hkg.setdefault(ind, []).append((year, float(r["value"])))

    phl = []
    with open(UNIV, newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("iso3") == "PHL" and r.get("indicator") == "ner_primary":
                phl.append((int(r["year"]), float(r["value"])))

    return (sorted(hkg.get("ner_primary", [])),
            sorted(hkg.get("aner_primary", [])),
            sorted(phl))


def contiguous_blocks(pairs):
    blocks = []
    current = []
    for year, value in pairs:
        if current and year == current[-1][0] + 1:
            current.append((year, value))
        else:
            if current:
                blocks.append(current)
            current = [(year, value)]
    if current:
        blocks.append(current)
    return blocks


def build_reference_rows(hkg_ner, hkg_aner, phl):
    rows = []

    def emit_series(reference_id, country, iso3, indicator, pairs):
        blocks = contiguous_blocks(pairs)
        for block in blocks:
            block_id = f"{block[0][0]}-{block[-1][0]}"
            for year, value in block:
                rows.append({
                    "row_type": "observation",
                    "label": LABEL_REF,
                    "provenance": PROV_OBS,
                    "reference_id": reference_id,
                    "country": country,
                    "iso3": iso3,
                    "indicator": indicator,
                    "threshold": "",
                    "year": str(year),
                    "value": f6(value),
                    "contiguous_block": block_id,
                    "n_obs_in_block": str(len(block)),
                    "first_at_or_above": "",
                    "first_sustained_5y": "",
                    "note": "observed; no interpolation",
                })
        overall = {}
        for threshold in THRESHOLDS:
            # Crossings must be computed within contiguous observed blocks: a
            # "5 consecutive years" run may not jump an unobserved gap.
            block_first_at = [first_at_or_above(b, threshold) for b in blocks]
            block_sustained = [first_sustained(b, threshold) for b in blocks]
            first_at = min((y for y in block_first_at if y is not None),
                           default=None)
            sustained = min((y for y in block_sustained if y is not None),
                            default=None)
            overall[threshold] = {
                "first_at": first_at,
                "sustained": sustained,
            }
            for block in blocks:
                block_id = f"{block[0][0]}-{block[-1][0]}"
                rows.append({
                    "row_type": "crossing",
                    "label": LABEL_REF,
                    "provenance": PROV_OBS,
                    "reference_id": reference_id,
                    "country": country,
                    "iso3": iso3,
                    "indicator": indicator,
                    "threshold": str(int(threshold)),
                    "year": "",
                    "value": "",
                    "contiguous_block": block_id,
                    "n_obs_in_block": str(len(block)),
                    "first_at_or_above": year_str(first_at_or_above(block, threshold)),
                    "first_sustained_5y": year_str(first_sustained(block, threshold)),
                    "note": ("within this contiguous observed block; "
                             "5 consecutive observed years required"),
                })
            rows.append({
                "row_type": "crossing",
                "label": LABEL_REF,
                "provenance": PROV_OBS,
                "reference_id": reference_id,
                "country": country,
                "iso3": iso3,
                "indicator": indicator,
                "threshold": str(int(threshold)),
                "year": "",
                "value": "",
                "contiguous_block": "ALL",
                "n_obs_in_block": str(len(pairs)),
                "first_at_or_above": year_str(overall[threshold]["first_at"]),
                "first_sustained_5y": year_str(overall[threshold]["sustained"]),
                "note": ("earliest across contiguous observed blocks; "
                         "REFERENCE-ONLY, not validation"),
            })

    emit_series("HKG_ner_primary", "Hong Kong SAR, China", "HKG", "ner_primary", hkg_ner)
    emit_series("HKG_aner_primary", "Hong Kong SAR, China", "HKG", "aner_primary", hkg_aner)
    emit_series("PHL_ner_primary", "Philippines", "PHL", "ner_primary", phl)
    return rows


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="EXP-3 M1-NER construct-equivalence test.")
    parser.add_argument("--out-dir", default=str(ROOT / "results"),
                        help="output directory (default: results/)")
    args = parser.parse_args(argv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    predecl = ROOT / "PRE_DECLARATIONS.md"
    if not predecl.exists():
        fail(f"predeclaration not found: {predecl}")
    actual_predecl = sha256_file(predecl)
    if actual_predecl != EXPECTED_PREDECL_SHA:
        fail(f"predeclaration sha256 mismatch: expected {EXPECTED_PREDECL_SHA}, "
             f"got {actual_predecl}")

    panel = load_panel(PANEL)
    results, complete, incomplete, flow_cross, stock_cross, sens = build_results(panel)

    write_csv(out_dir / "M1_NER_RESULTS.csv", RESULT_FIELDS, results)

    comparison = []
    for r in band_rows(panel, (VERDICT_COUNTRY, VERDICT_LEVEL)):
        comparison.append(comparison_row("VERDICT", r, r["stock"] is not None))
    for r in sens:
        comparison.append(comparison_row("SENSITIVITY", r, True))
    write_csv(out_dir / "M1_NER_COMPARISON.csv", COMPARISON_FIELDS, comparison)

    crossings = []
    key = (VERDICT_COUNTRY, VERDICT_LEVEL)
    for threshold in THRESHOLDS:
        crossings.append(crossing_row("VERDICT", key, threshold,
                                      flow_cross[threshold], stock_cross[threshold]))
    for skey in sorted(panel, key=lambda k: (k[0], LEVELS.index(k[1]))):
        fp = [(y, panel[skey][y]["flow"]) for y in sorted(panel[skey])]
        sp = stock_series(panel[skey], DUR[skey[1]])
        for threshold in THRESHOLDS:
            crossings.append(crossing_row(
                "SENSITIVITY", skey, threshold,
                crossing_summary(fp, threshold),
                crossing_summary(sp, threshold)))
    write_csv(out_dir / "M1_NER_CROSSINGS.csv", CROSSING_FIELDS, crossings)

    hkg_ner, hkg_aner, phl = read_observed()
    reference = build_reference_rows(hkg_ner, hkg_aner, phl)
    write_csv(out_dir / "M1_NER_REFERENCE.csv", REFERENCE_FIELDS, reference)

    overall = next(r for r in results if r["test"] == "h1_overall")
    band = next(r for r in results if r["test"] == "band_agreement")
    print(f"[m1_ner] verdict series: {series_id(key)}")
    print(f"[m1_ner] band years (complete window): {band['n']}; "
          f"max |stock-flow| = {band['statistic']} pp "
          f"({band['verdict']} the 2.0 pp bar)")
    for threshold in THRESHOLDS:
        row = next(r for r in results if r["test"] == f"crossing_{int(threshold)}")
        print(f"[m1_ner] crossing {int(threshold)}: difference = "
              f"{row['statistic']} y ({row['verdict']} the 1 y bar)")
    print(f"[m1_ner] H1 = {overall['verdict']}")
    print(f"[m1_ner] reference rows: {len(reference)} (OBSERVED-REFERENCE-ONLY)")
    print(f"[m1_ner] wrote 4 CSVs to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
