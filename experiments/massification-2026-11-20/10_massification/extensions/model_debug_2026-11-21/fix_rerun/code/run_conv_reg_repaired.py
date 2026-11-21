#!/usr/bin/env python3
"""
EXP-21 CONV-REG — descriptive conversion register.

DEBUG RE-RUN (model_debug_2026-11-21/fix_rerun): the delivered runner is reused verbatim except
that the two capped panels are replaced by the REPAIRED copies (CAP-01 one-sided floor) and the
cell label is marked DEBUG. Thresholds, T definition, observed inputs and A17 are unchanged.

Reads on-disk observed series and three frozen synthetic panels; writes the register.
No model run, no re-fit, no RNG, no clock in outputs, no network, no writes outside this cell.

Frozen by PRE_DECLARATIONS.md (sha256 in PRE_DECLARATIONS.sha256). The runner's first act is to
enforce that hash (D158(1)); its last act before writing the verdict is to enforce it again.
Every threshold below is copied from PRE_DECLARATIONS.md section 0/4 and has no CLI override.
"""

import argparse
import csv
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CELL = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(CELL))))
PREDECL = os.path.join(CELL, "PRE_DECLARATIONS.md")
PREDECL_HASH_FILE = os.path.join(CELL, "PRE_DECLARATIONS.sha256")

# ---------------------------------------------------------------- frozen constants
BAND_LO = 0.85              # PRE_DECLARATIONS 4.3 (closed interval)
BAND_HI = 1.15
MIN_IN_BAND_SHARE = 0.80    # PRE_DECLARATIONS 4.4
MAX_RANGE = 0.30
MIN_PAIRS = 3               # identification gate (THIN)
M_DECLARED = 1.10           # generator_v1_2/PARAMS.md section 7
TOL_M = 1e-9                # PRE_DECLARATIONS 4.6

FROZEN_SYSTEMS = ["PHL", "KOR", "KHM", "CHN"]     # block item 5
EXTRA_SYSTEMS = ["HKG", "JPN"]                    # 4.8: reported, no verdict path
ALL_SYSTEMS = FROZEN_SYSTEMS + EXTRA_SYSTEMS

LEVELS = [
    ("primary", "completion_primary", "ger_primary"),
    ("lower_secondary", "completion_lower_secondary", "ger_lower_secondary"),
    ("upper_secondary", "completion_upper_secondary", "ger_upper_secondary"),
]

SERIES_REL = "10_massification/data/UNIVERSALIZATION_SERIES.csv"
PANELS_DIR = os.path.abspath(os.environ.get(
    "FIX_PANELS_DIR", os.path.join(CELL, "results", "panels")))
PANELS = [
    ("v1.3", os.path.relpath(os.path.join(PANELS_DIR, "synthetic_panel_v1_3_repaired.csv"), ROOT)),
    ("v1.2", os.path.relpath(os.path.join(PANELS_DIR, "synthetic_panel_v1_2_repaired.csv"), ROOT)),
    ("A17", "10_massification/extensions/synthetic_2026-11-20/generator_v1_7_partrepair/results/panel_A17.csv"),
]
PARAMS_REL = "10_massification/extensions/synthetic_2026-11-20/generator_v1_2/PARAMS.md"
# inherited THRESHOLD predeclaration of the delivered register (read-only; re-hashed at run time)
REGISTER_CELL = os.path.join(ROOT, "10_massification", "extensions", "conv_reg_2026-11-20")
REGISTER_PREDECL = os.path.join(REGISTER_CELL, "PRE_DECLARATIONS.md")
EXPECTED_REGISTER_PREDECL_SHA = (
    "1dd86bd139a81c22e0ba2918728818fe7184775d925211a28fdd2be00b975410")

CONVENTION_PAIR = "UIS completion (pop 3-5y above grade) / GER (official age band)"

CONSOLE = []


def say(msg):
    CONSOLE.append(msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def enforce_inherited_register_predecl(where):
    """The delivered register's THRESHOLD predeclaration is inherited verbatim: re-hash it."""
    actual = sha256_file(REGISTER_PREDECL)
    if actual != EXPECTED_REGISTER_PREDECL_SHA:
        sys.stderr.write(
            "INHERITED REGISTER PREDECLARATION HASH MISMATCH at %s: recorded %s, actual %s -- no verdict written\n"
            % (where, EXPECTED_REGISTER_PREDECL_SHA, actual)
        )
        raise SystemExit(2)
    say("inherited register predeclaration hash ENFORCED at %s: %s" % (where, actual))
    return actual


def enforce_predecl_hash(where):
    """D158(1): the hash is checked by the runner at the moment the verdict is written."""
    with open(PREDECL_HASH_FILE, encoding="utf-8") as fh:
        recorded = fh.read().split()[0].strip().lower()
    actual = sha256_file(PREDECL)
    if recorded != actual:
        sys.stderr.write(
            "PREDECLARATION HASH MISMATCH at %s: recorded %s, actual %s -- no verdict written\n"
            % (where, recorded, actual)
        )
        raise SystemExit(2)
    say("predeclaration hash ENFORCED at %s: %s" % (where, actual))
    return actual



def prov(indicator):
    """Provenance string for a long-format cell: the object is named by `indicator`,
    the number is carried in column `value`."""
    return "value[indicator=%s]" % indicator


def f6(x):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "UNABLE"
    return "%.6f" % x


def b(x):
    return "TRUE" if x else "FALSE"


# ---------------------------------------------------------------- input readers
def read_observed_series():
    """Return {(iso3, column): {year: value}} for status == observed, finite, > 0."""
    path = os.path.join(ROOT, SERIES_REL)
    wanted = set()
    for _, cc, gc in LEVELS:
        wanted.add(cc)
        wanted.add(gc)
    series = {}
    with open(path, newline="", encoding="utf-8") as fh:
        rdr = csv.DictReader(fh)
        header = rdr.fieldnames
        # long format: one row per (iso3, indicator, year); the numeric cell is `value`,
        # the object is named by `indicator`. Provenance is therefore indicator+value.
        for col in ("iso3", "indicator", "year", "value", "status"):
            if col not in header:
                sys.stderr.write("missing column %s in %s\n" % (col, SERIES_REL))
                raise SystemExit(2)
        for row in rdr:
            if row["indicator"] not in wanted:
                continue
            if row["status"] != "observed":
                continue
            try:
                val = float(row["value"])
            except (TypeError, ValueError):
                continue
            if not math.isfinite(val) or val <= 0:
                continue
            key = (row["iso3"], row["indicator"])
            series.setdefault(key, {})[int(row["year"])] = val
    return series


def read_panel(rel):
    path = os.path.join(ROOT, rel)
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit(2)
    header = rows[0].keys()
    for col in ("completion_uis", "completion_cohort", "measurement_factor"):
        if col not in header:
            sys.stderr.write("missing column %s in %s\n" % (col, rel))
            raise SystemExit(2)
    return rows


# ---------------------------------------------------------------- register core
def crossings(years, tvals):
    """PRE_DECLARATIONS 4.5: consecutive-pair sign changes, or arrival at 1.0."""
    out = []
    for i in range(1, len(years)):
        t0, t1 = tvals[i - 1], tvals[i]
        s0 = 0 if t0 == 1.0 else (-1 if t0 < 1.0 else 1)
        s1 = 0 if t1 == 1.0 else (-1 if t1 < 1.0 else 1)
        if s0 * s1 < 0:
            out.append((years[i - 1], years[i]))
        elif s0 != 0 and s1 == 0:
            out.append((years[i - 1], years[i]))
    return out


def tracecheck(series, iso3, col, year, value):
    fresh = read_observed_series()
    got = fresh.get((iso3, col), {}).get(year)
    if got is None:
        return "UNTRACEABLE: no observed row at %s %s %s" % (iso3, col, year)
    if got != value:
        return "UNTRACEABLE: value mismatch at %s %s %s" % (iso3, col, year)
    return "TRACEABLE"


def build_register(series, sha12):
    reg_rows, detail_rows = [], []
    for system in ALL_SYSTEMS:
        for level, ccol, gcol in LEVELS:
            cyears = series.get((system, ccol), {})
            gyears = series.get((system, gcol), {})
            pairs = sorted(set(cyears) & set(gyears))
            union_years = set(cyears) | set(gyears)
            n_not_comparable = len(union_years) - len(pairs)

            tvals = [cyears[y] / gyears[y] for y in pairs]
            n_pairs = len(pairs)
            n_in_band = sum(1 for t in tvals if BAND_LO <= t <= BAND_HI)
            share = (n_in_band / n_pairs) if n_pairs else None
            t_min = min(tvals) if tvals else None
            t_max = max(tvals) if tvals else None
            rng = (t_max - t_min) if tvals else None
            band_ok = (share is not None) and (share >= MIN_IN_BAND_SHARE)
            range_ok = (rng is not None) and (rng <= MAX_RANGE)

            if n_pairs < 2:
                cx = []
            else:
                cx = crossings(pairs, tvals)
            if n_pairs < 2:
                crossing_year = "UNABLE"
                crossing_interval = "UNABLE"
            elif cx:
                crossing_year = ";".join(str(p[1]) for p in cx)
                crossing_interval = "%d->%d" % cx[0]
            else:
                crossing_year = "NONE"
                crossing_interval = "NONE"

            if not cyears:
                verdict = "NO-COMPLETION-SERIES"
            elif n_pairs < MIN_PAIRS:
                verdict = "THIN"
            elif band_ok and range_ok:
                verdict = "INTERCHANGEABLE"
            else:
                verdict = "NOT-INTERCHANGEABLE"

            # traceability: re-read every pair from the named file + column
            tc = "TRACEABLE"
            for y in pairs:
                chk = tracecheck(series, system, ccol, y, cyears[y])
                if chk != "TRACEABLE":
                    tc = chk
                    break
                chk = tracecheck(series, system, gcol, y, gyears[y])
                if chk != "TRACEABLE":
                    tc = chk
                    break

            reg_rows.append({
                "system": system,
                "level": level,
                "convention_pair": CONVENTION_PAIR,
                "n_pairs": n_pairs,
                "n_not_comparable_years": n_not_comparable,
                "T_min": f6(t_min),
                "T_max": f6(t_max),
                "range": f6(rng),
                "in_band_share": f6(share),
                "n_in_band": n_in_band,
                "band_ok": b(band_ok),
                "range_ok": b(range_ok),
                "crossing_year": crossing_year,
                "crossing_interval": crossing_interval,
                "n_crossings": len(cx),
                "verdict": verdict,
                "label": "DERIVED",
                "frozen_system": b(system in FROZEN_SYSTEMS),
                "completion_column": prov(ccol),
                "ger_column": prov(gcol),
                "source_path": SERIES_REL,
                "traceable": tc,
                "predecl_sha256_12": sha12,
            })

            for y, t in zip(pairs, tvals):
                detail_rows.append({
                    "system": system,
                    "level": level,
                    "year": y,
                    "completion_value": f6(cyears[y]),
                    "ger_value": f6(gyears[y]),
                    "T": f6(t),
                    "in_band": b(BAND_LO <= t <= BAND_HI),
                    "source_path": SERIES_REL,
                    "completion_column": prov(ccol),
                    "ger_column": prov(gcol),
                    "status_completion": "observed",
                    "status_ger": "observed",
                    "label": "DERIVED",
                    "traceable": tc,
                })
    return reg_rows, detail_rows


def build_system_summary(reg_rows):
    out = []
    for system in ALL_SYSTEMS:
        cells = [r for r in reg_rows if r["system"] == system]
        measured = [r for r in cells if r["T_min"] != "UNABLE"]
        thin = [r for r in cells if r["verdict"] == "THIN"]
        if not measured:
            out.append({
                "system": system,
                "n_levels_measured": 0,
                "n_levels_thin": len(thin),
                "min_T_over_levels": "UNABLE",
                "max_T_over_levels": "UNABLE",
                "level_range_intersection": "UNABLE",
                "spread_across_levels": "UNABLE",
                "label": "DERIVED",
                "frozen_system": b(system in FROZEN_SYSTEMS),
            })
            continue
        t_mins = [float(r["T_min"]) for r in measured]
        t_maxs = [float(r["T_max"]) for r in measured]
        inter = "NONEMPTY" if max(t_mins) <= min(t_maxs) else "EMPTY"
        out.append({
            "system": system,
            "n_levels_measured": len(measured),
            "n_levels_thin": len(thin),
            "min_T_over_levels": f6(min(t_mins)),
            "max_T_over_levels": f6(max(t_maxs)),
            "level_range_intersection": inter,
            "spread_across_levels": f6(max(t_maxs) - min(t_mins)),
            "label": "DERIVED",
            "frozen_system": b(system in FROZEN_SYSTEMS),
        })
    return out


def build_m_constancy():
    rows = []
    for name, rel in PANELS:
        panel = read_panel(rel)
        n_rows = len(panel)
        n_tested = 0
        n_not_testable = 0
        max_dev_ratio = None
        max_dev_factor = None
        max_rel_resid = None
        for r in panel:
            try:
                uis = float(r["completion_uis"])
                coh = float(r["completion_cohort"])
            except (TypeError, ValueError):
                n_not_testable += 1
                continue
            if not (math.isfinite(uis) and math.isfinite(coh)) or coh == 0:
                n_not_testable += 1
                continue
            n_tested += 1
            ratio = uis / coh
            d = abs(ratio - M_DECLARED)
            max_dev_ratio = d if max_dev_ratio is None else max(max_dev_ratio, d)
            try:
                mf = float(r["measurement_factor"])
                df = abs(mf - M_DECLARED)
                max_dev_factor = df if max_dev_factor is None else max(max_dev_factor, df)
            except (TypeError, ValueError):
                pass
            resid = abs(uis - M_DECLARED * coh) / max(1.0, abs(uis))
            max_rel_resid = resid if max_rel_resid is None else max(max_rel_resid, resid)

        ratio_ok = (max_dev_ratio is not None) and (max_dev_ratio <= TOL_M)
        factor_ok = (max_dev_factor is not None) and (max_dev_factor <= TOL_M)
        if not ratio_ok or not factor_ok:
            verdict = "NOT-CONSTANT"
        elif n_not_testable > 0:
            verdict = "CONSTANT-ON-TESTABLE-SUBSET"
        else:
            verdict = "CONSTANT"

        # diagnostic (console only, not a register field): where does the 1.10 identity fail?
        n_ceiling = 0
        n_would_exceed = 0
        for r in panel:
            try:
                uis = float(r["completion_uis"])
                coh = float(r["completion_cohort"])
            except (TypeError, ValueError):
                continue
            if coh == 0:
                continue
            if M_DECLARED * coh > 1.0:
                n_would_exceed += 1
            if uis == 1.0 and M_DECLARED * coh > 1.0:
                n_ceiling += 1
        say("  %s: cells where 1.10*completion_cohort > 1.0: %d; of those, completion_uis == 1.0 exactly (capped): %d"
            % (name, n_would_exceed, n_ceiling))

        rows.append({
            "panel": name,
            "panel_path": rel,
            "n_rows": n_rows,
            "n_tested": n_tested,
            "n_not_testable": n_not_testable,
            "completion_uis_column": "completion_uis",
            "completion_cohort_column": "completion_cohort",
            "measurement_factor_column": "measurement_factor",
            "declared_m": "%.2f" % M_DECLARED,
            "tolerance": "%.0e" % TOL_M,
            "max_abs_dev_ratio": ("%.10e" % max_dev_ratio) if max_dev_ratio is not None else "UNABLE",
            "max_abs_dev_factor": ("%.10e" % max_dev_factor) if max_dev_factor is not None else "UNABLE",
            "max_abs_rel_residual": ("%.10e" % max_rel_resid) if max_rel_resid is not None else "UNABLE",
            "verdict": verdict,
            "label": "SYNTHETIC",
            "traceable": "TRACEABLE",
        })
        say("m-constancy %s: n_rows=%d tested=%d not_testable=%d max_dev_ratio=%s max_dev_factor=%s -> %s"
            % (name, n_rows, n_tested, n_not_testable,
               rows[-1]["max_abs_dev_ratio"], rows[-1]["max_abs_dev_factor"], verdict))
    return rows


# ---------------------------------------------------------------- verdict
def overall_verdict(reg_rows, m_rows):
    frozen = [r for r in reg_rows if r["frozen_system"] == "TRUE"]
    untraceable = [r["system"] + "/" + r["level"] for r in reg_rows if r["traceable"] != "TRACEABLE"]
    untraceable += [r["panel"] for r in m_rows if r["traceable"] != "TRACEABLE"]

    not_inter = [r["system"] + "/" + r["level"] for r in frozen if r["verdict"] == "NOT-INTERCHANGEABLE"]
    crossing = [r["system"] + "/" + r["level"] for r in frozen if int(r["n_crossings"]) > 0]
    thin = [r["system"] + "/" + r["level"] for r in frozen if r["verdict"] in ("THIN", "NO-COMPLETION-SERIES")]
    uniform_cells = [r["system"] + "/" + r["level"] for r in frozen if r["verdict"] == "INTERCHANGEABLE"]

    trace = []
    if untraceable:
        verdict, fired = "UNVERIFIED", 1
    elif not_inter or crossing:
        verdict, fired = "REGISTER-BINDING", 2
    elif len(uniform_cells) == len(frozen) and not thin:
        verdict, fired = "REGISTER-UNIFORM", 3
    else:
        verdict, fired = "REGISTER-UNIFORM-PARTIAL", 4

    trace = [
        {"clause": 1, "label": "UNVERIFIED", "test": "any register line untraceable to a named file+column",
         "fired": fired == 1, "evidence": untraceable},
        {"clause": 2, "label": "REGISTER-BINDING",
         "test": "any frozen cell NOT-INTERCHANGEABLE, or any T crosses 1.0",
         "fired": fired == 2,
         "evidence": {"not_interchangeable": sorted(not_inter), "crossing_1_0": sorted(crossing)}},
        {"clause": 3, "label": "REGISTER-UNIFORM",
         "test": "all 12 frozen cells INTERCHANGEABLE and no crossing",
         "fired": fired == 3, "evidence": uniform_cells},
        {"clause": 4, "label": "REGISTER-UNIFORM-PARTIAL",
         "test": "no UNVERIFIED, no NOT-INTERCHANGEABLE, no crossing, >=1 frozen cell THIN",
         "fired": fired == 4, "evidence": thin},
    ]
    return verdict, trace, {
        "cells_total": len(reg_rows),
        "cells_frozen": len(frozen),
        "cells_interchangeable": len(uniform_cells),
        "cells_not_interchangeable": len(not_inter),
        "cells_thin": len([r for r in frozen if r["verdict"] == "THIN"]),
        "cells_no_completion_series": len([r for r in frozen if r["verdict"] == "NO-COMPLETION-SERIES"]),
        "cells_with_crossing": len(crossing),
        "cells_untraceable": len(untraceable),
    }


# ---------------------------------------------------------------- writers
def write_csv(path, rows, columns):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in columns})


REG_COLUMNS = [
    "system", "level", "convention_pair", "n_pairs", "n_not_comparable_years",
    "T_min", "T_max", "range", "in_band_share", "n_in_band", "band_ok", "range_ok",
    "crossing_year", "crossing_interval", "n_crossings", "verdict", "label",
    "frozen_system", "completion_column", "ger_column", "source_path", "traceable",
    "predecl_sha256_12",
]
DETAIL_COLUMNS = [
    "system", "level", "year", "completion_value", "ger_value", "T", "in_band",
    "source_path", "completion_column", "ger_column", "status_completion", "status_ger",
    "label", "traceable",
]
SYSTEM_COLUMNS = [
    "system", "n_levels_measured", "n_levels_thin", "min_T_over_levels", "max_T_over_levels",
    "level_range_intersection", "spread_across_levels", "label", "frozen_system",
]
M_COLUMNS = [
    "panel", "panel_path", "n_rows", "n_tested", "n_not_testable", "completion_uis_column",
    "completion_cohort_column", "measurement_factor_column", "declared_m", "tolerance",
    "max_abs_dev_ratio", "max_abs_dev_factor", "max_abs_rel_residual", "verdict", "label",
    "traceable",
]
ARTIFACTS = ["CONV_REG.csv", "CONV_REG_DETAIL.csv", "CONV_REG_SYSTEM.csv", "M_CONSTANCY.csv",
             "VERDICT.json", "console.txt"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(CELL, "results"))
    ap.add_argument("--compare", nargs=2, metavar=("RUN1", "RUN2"))
    args = ap.parse_args()

    if args.compare:
        a_dir, b_dir = args.compare
        result = {"cell": "EXP-21 CONV-REG (DEBUG repaired re-run)", "artifacts": [], "all_identical": True}
        for name in ARTIFACTS:
            pa, pb = os.path.join(a_dir, name), os.path.join(b_dir, name)
            ha = sha256_file(pa)
            hb = sha256_file(pb)
            same = (ha == hb)
            result["artifacts"].append({"artifact": name, "sha256_run1": ha, "sha256_run2": hb,
                                        "byte_identical": same})
            result["all_identical"] = result["all_identical"] and same
        result["n_artifacts"] = len(result["artifacts"])
        result["verdict"] = "DETERMINISTIC" if result["all_identical"] else "NON-DETERMINISTIC"
        with open(os.path.join(a_dir, "DETERMINISM.json"), "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print("determinism:", result["verdict"], "(%d artifacts)" % result["n_artifacts"])
        return 0

    sha = enforce_predecl_hash("pre-input")
    inherited_sha = enforce_inherited_register_predecl("pre-input")
    sha12 = sha[:12]
    out = args.out
    os.makedirs(out, exist_ok=True)

    say("EXP-21 CONV-REG -- DEBUG repaired re-run -- descriptive register -- "
        "no model run here, no RNG, no clock")
    say("band [%.2f, %.2f] closed; in-band share >= %.2f of paired cells; range <= %.2f; THIN if n<3"
        % (BAND_LO, BAND_HI, MIN_IN_BAND_SHARE, MAX_RANGE))
    say("series is long-format (iso3,indicator,level,year,value,status): a cell is read as "
        "value where indicator=<object> and status=observed; both sides of every pair name their indicator")
    say("frozen systems: %s; reported outside verdict scope: %s"
        % (",".join(FROZEN_SYSTEMS), ",".join(EXTRA_SYSTEMS)))

    series = read_observed_series()
    reg_rows, detail_rows = build_register(series, sha12)
    system_rows = build_system_summary(reg_rows)
    m_rows = build_m_constancy()

    for r in reg_rows:
        say("register %s/%s pairs=%d share=%s range=%s crossing=%s -> %s"
            % (r["system"], r["level"], r["n_pairs"], r["in_band_share"], r["range"],
               r["crossing_year"], r["verdict"]))
    for r in system_rows:
        say("system %s levels_measured=%d intersection=%s spread=%s"
            % (r["system"], r["n_levels_measured"], r["level_range_intersection"],
               r["spread_across_levels"]))

    verdict, trace, counts = overall_verdict(reg_rows, m_rows)

    verdict_obj = {
        "cell": "EXP-21 CONV-REG (DEBUG repaired re-run)",
        "label": "DEBUG",
        "question": "which object may carry which level statement, and is one constant conversion enough?",
        "adoption": "NONE",
        "overall_verdict": verdict,
        "precedence": "UNVERIFIED > REGISTER-BINDING > REGISTER-UNIFORM",
        "precedence_trace": trace,
        "counts": counts,
        "m_constancy": {r["panel"]: r["verdict"] for r in m_rows},
        "m_constancy_max_dev": {r["panel"]: r["max_abs_dev_ratio"] for r in m_rows},
        "predeclaration_sha256": sha,
        "predeclaration_hash_enforced": True,
        "inherited_register_predecl_sha256": inherited_sha,
        "inherited_register_predecl_hash_enforced": True,
        "panel_substitution": "v1.3 and v1.2 -> repaired copies; A17 unchanged",
        "hash_enforcement": "checked pre-input and re-checked immediately before this verdict was written",
        "frozen_thresholds": {
            "band": [BAND_LO, BAND_HI],
            "min_in_band_share": MIN_IN_BAND_SHARE,
            "max_range": MAX_RANGE,
            "min_pairs": MIN_PAIRS,
            "m_tolerance": TOL_M,
            "declared_m": M_DECLARED,
        },
        "labels": {"observed_inputs": "OBSERVED", "register_values": "DERIVED",
                   "panel_values": "SYNTHETIC", "m": "DECLARED / CONVENTION"},
        "no_model_run": True,
        "no_rng": True,
        "no_clock_in_outputs": True,
        "n_register_rows": len(reg_rows),
        "n_detail_rows": len(detail_rows),
    }

    # last act before the verdict hits disk: enforce the hash again (D158(1))
    sha_again = enforce_predecl_hash("pre-verdict-write")
    assert sha_again == sha
    inherited_sha_again = enforce_inherited_register_predecl("pre-verdict-write")
    assert inherited_sha_again == inherited_sha

    write_csv(os.path.join(out, "CONV_REG.csv"), reg_rows, REG_COLUMNS)
    write_csv(os.path.join(out, "CONV_REG_DETAIL.csv"), detail_rows, DETAIL_COLUMNS)
    write_csv(os.path.join(out, "CONV_REG_SYSTEM.csv"), system_rows, SYSTEM_COLUMNS)
    write_csv(os.path.join(out, "M_CONSTANCY.csv"), m_rows, M_COLUMNS)
    with open(os.path.join(out, "VERDICT.json"), "w", encoding="utf-8") as fh:
        json.dump(verdict_obj, fh, indent=2, sort_keys=True)
        fh.write("\n")

    say("OVERALL VERDICT: %s (clause %d fired)"
        % (verdict, [t["clause"] for t in trace if t["fired"]][0]))
    say("register rows=%d detail rows=%d" % (len(reg_rows), len(detail_rows)))
    with open(os.path.join(out, "console.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(CONSOLE) + "\n")

    inputs = {"series": SERIES_REL, "panels": [p[1] for p in PANELS], "params": PARAMS_REL}
    hashes = {"cell": "EXP-21 CONV-REG", "inputs": []}
    for rel in [SERIES_REL] + [p[1] for p in PANELS] + [PARAMS_REL]:
        hashes["inputs"].append({"path": rel, "sha256": sha256_file(os.path.join(ROOT, rel))})
    with open(os.path.join(out, "INPUT_HASHES.json"), "w", encoding="utf-8") as fh:
        json.dump(hashes, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print("VERDICT:", verdict)
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
