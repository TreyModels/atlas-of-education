#!/usr/bin/env python3
"""EXP-8 GATE-LOCUS: where do the generator's gates actually bind?

Read-only census on the frozen synthetic panel. Every threshold is transcribed from
Council brief 022 (SYNTHESIS_022.md, section 6, EXP-8) and is frozen in PRE_DECLARATIONS.md
(sha256 a8566fbf...4c547d) before this script was first run.

No RNG. No clock. No environment-dependent ordering. Deterministic by construction:
all aggregations run over explicitly ordered lists, all float output is format-pinned,
and every emitted row is sorted on an explicit key.

Outputs (all under <experiment>/results/):
  GATE_LOCUS_RESULTS.csv        per level, both bars, verdicts, components
  GATE_LOCUS_ANCHOR.csv         SYN00_PHL_LIKE x 2000/2010/2020/2024 x 4 levels + p4
  GATE_LOCUS_FALSIFIER.json     the p_off < 0.50 / > 20% check and its consequence
  GATE_LOCUS_SECONDARY_S1.csv   gate-panel leg (non-verdict-bearing)
  GATE_LOCUS_SECONDARY_S2.csv   anchor trajectory (non-verdict-bearing)
  GATE_LOCUS_SECONDARY_S3.csv   upper/tertiary rationing by country and by year
"""

import csv
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
EXP_DIR = HERE.parent
PROGRAMME_ROOT = EXP_DIR.parents[2]

PANEL = (PROGRAMME_ROOT / "10_massification" / "extensions" / "synthetic_2026-11-20"
         / "generator_v1_2" / "results" / "synthetic_panel_v1_2.csv")
GATES = (PROGRAMME_ROOT / "10_massification" / "extensions" / "synthetic_2026-11-20"
         / "generator_v1_3" / "results" / "shadow_gates_v1_3.csv")
# Output directory: "results" by default; an argument is accepted only so that the
# determinism re-run can write to results/determinism_run2/ with the SAME script.
RESULTS = (EXP_DIR / sys.argv[1]) if len(sys.argv) > 1 else (EXP_DIR / "results")

# ---------------------------------------------------------------- frozen constants
# PRE_DECLARATIONS.md sections 4-7. Changing any of these voids the predeclaration.
PANEL_SHA256 = "14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac"
GATES_SHA256 = "df3cab007ce5fbe9a48d58b0701d04e6d762591848ca1517a634c8f897edb351"
PREDECL_SHA256 = "a8566fbfbca5cc5231ef78c35adffbf62264f82bbefe830683616105434c547d"
LEVELS = ("primary", "lower_secondary", "upper_secondary", "tertiary")
BAR_PRIMARY = 0.95          # bar-95, the bar the brief names first
BAR_SECONDARY = 0.99        # bar-99, the bar the Council re-derived calibration on
GATE_BINDS_AT = 0.50        # share >= 50%  -> GATE BINDS
UNRATIONED_AT = 0.10        # share <= 10%  -> UNRATIONED
DEEP_BAR = 0.50             # falsifier: p_off < 0.50
DEEP_SHARE_MAX = 0.20       # falsifier: in > 20% of years (strict)
ANCHOR_ID = "0"
ANCHOR_NAME = "SYN00_PHL_LIKE"
ANCHOR_YEARS = ("2000", "2010", "2020", "2024")
V8_WINDOW_FROM = 2010

EXPERIMENT = "EXP-8 GATE-LOCUS"
LABEL = "SYNTHETIC"
COUNCIL_CALIBRATION = {"primary": 87.4, "lower_secondary": 93.3,
                       "upper_secondary": 6.5, "tertiary": 0.0}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def num(row, key):
    raw = row[key]
    if raw is None or raw == "":
        sys.exit(f"FATAL: empty cell {key!r} in row {row.get('country_id')}/{row.get('level')}/{row.get('year')}")
    try:
        val = float(raw)
    except ValueError:
        sys.exit(f"FATAL: non-numeric {key!r}={raw!r}")
    if val != val or val in (float("inf"), float("-inf")):
        sys.exit(f"FATAL: non-finite {key!r}={raw!r}")
    return val


def pct(count, n):
    return 100.0 * count / n if n else 0.0


def verdict(share_pct_value):
    """Three words only, per PRE_DECLARATIONS section 5."""
    if share_pct_value >= 100.0 * GATE_BINDS_AT:
        return "GATE BINDS"
    if share_pct_value <= 100.0 * UNRATIONED_AT:
        return "UNRATIONED"
    return "INTERMEDIATE"


def load_panel():
    if sha256(PANEL) != PANEL_SHA256:
        sys.exit("FATAL: frozen-panel hash mismatch; refusing to run on a non-frozen panel")
    with open(PANEL, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) != 6720:
        sys.exit(f"FATAL: expected 6720 rows, found {len(rows)}")
    levels = sorted({r["level"] for r in rows})
    if tuple(levels) != tuple(sorted(LEVELS)):
        sys.exit(f"FATAL: unexpected level set {levels}")
    return rows


def cell_records(rows):
    """(level, country, year, p_off, rationed>0) with the declared guards."""
    recs = []
    for r in rows:
        demand = num(r, "demand_official")
        admitted = num(r, "admitted_official")
        if demand <= 0:
            sys.exit(f"FATAL: demand_official <= 0 at {r['country']}/{r['level']}/{r['year']}")
        recs.append({
            "level": r["level"],
            "country": r["country"],
            "country_id": r["country_id"],
            "year": int(r["year"]),
            "p_off": admitted / demand,
            "rationed_pos": num(r, "rationed_official") > 0.0,
        })
    return recs


def per_level(recs):
    out = []
    for level in LEVELS:
        sub = [c for c in recs if c["level"] == level]
        n = len(sub)
        if n == 0:
            sys.exit(f"FATAL: level {level} has no cells")
        n_rat = sum(1 for c in sub if c["rationed_pos"])
        c95 = sum(1 for c in sub if c["p_off"] < BAR_PRIMARY and c["rationed_pos"])
        c99 = sum(1 for c in sub if c["p_off"] < BAR_SECONDARY and c["rationed_pos"])
        a95 = sum(1 for c in sub if c["p_off"] < BAR_PRIMARY)
        a99 = sum(1 for c in sub if c["p_off"] < BAR_SECONDARY)
        c50 = sum(1 for c in sub if c["p_off"] < DEEP_BAR)
        p_off_sorted = sorted(c["p_off"] for c in sub)
        median = p_off_sorted[n // 2] if n % 2 else 0.5 * (p_off_sorted[n // 2 - 1] + p_off_sorted[n // 2])
        s95, s99 = pct(c95, n), pct(c99, n)
        v95, v99 = verdict(s95), verdict(s99)
        stable = v95 == v99
        out.append({
            "level": level,
            "n": n,
            "n_countries": len({c["country_id"] for c in sub}),
            "years": "%d-%d" % (min(c["year"] for c in sub), max(c["year"] for c in sub)),
            "n_rat": n_rat,
            "c95": c95, "s95": s95,
            "c99": c99, "s99": s99,
            "a95": a95, "a99": a99,
            "c50": c50, "s50": pct(c50, n),
            "v95": v95, "v99": v99,
            "stable": stable,
            "headline": v95 if stable else "BAR-DEPENDENT",
            "min": p_off_sorted[0],
            "median": median,
            "max": p_off_sorted[-1],
            "components": (
                "rationed_official>0 %d/%d; p_off<0.95 alone %d; both %d; "
                "p_off<0.99 alone %d; both %d; p_off<0.50 %d"
                % (n_rat, n, a95, c95, a99, c99, c50)
            ),
        })
    return out


def write_results(levels):
    path = RESULTS / "GATE_LOCUS_RESULTS.csv"
    header = ["experiment", "label", "level", "n_cells", "n_countries", "years",
              "n_rationed_official_gt0", "p_off_min", "p_off_median", "p_off_max",
              "count_p_off_lt095_and_rationed", "share_lt095_and_rationed_pct",
              "count_p_off_lt099_and_rationed", "share_lt099_and_rationed_pct",
              "count_p_off_lt095_only", "count_p_off_lt099_only",
              "count_p_off_lt050", "share_lt050_pct",
              "verdict_bar95", "verdict_bar99", "class_stable", "headline_verdict",
              "components"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for L in levels:
            w.writerow([EXPERIMENT, LABEL, L["level"], L["n"], L["n_countries"], L["years"],
                        L["n_rat"], "%.6f" % L["min"], "%.6f" % L["median"], "%.6f" % L["max"],
                        L["c95"], "%.4f" % L["s95"], L["c99"], "%.4f" % L["s99"],
                        L["a95"], L["a99"], L["c50"], "%.4f" % L["s50"],
                        L["v95"], L["v99"], "yes" if L["stable"] else "no",
                        L["headline"], L["components"]])
    return path


def anchor_rows(panel_rows):
    out = []
    for r in panel_rows:
        if r["country_id"] != ANCHOR_ID or r["year"] not in ANCHOR_YEARS:
            continue
        demand = num(r, "demand_official")
        admitted = num(r, "admitted_official")
        r4d = num(r, "rung4_demand")
        r4e = num(r, "rung4_emp")
        p4 = (r4e / r4d) if r4d else None
        out.append({
            "year": int(r["year"]),
            "level": r["level"],
            "demand_official": demand,
            "admitted_official": admitted,
            "p_off": admitted / demand,
            "rationed_official": num(r, "rationed_official"),
            "congestion_q": num(r, "congestion_q"),
            "seats": num(r, "seats"),
            "ger": num(r, "ger"),
            "rung4_demand": r4d,
            "rung4_emp": r4e,
            "p4": p4,
            "p4_v8_window": "yes" if int(r["year"]) >= V8_WINDOW_FROM else "no",
        })
    out.sort(key=lambda d: (d["year"], LEVELS.index(d["level"])))
    return out


def write_anchor(anchor):
    path = RESULTS / "GATE_LOCUS_ANCHOR.csv"
    header = ["experiment", "label", "country_id", "country", "year", "level",
              "demand_official", "admitted_official", "p_off", "rationed_official",
              "congestion_q", "seats", "ger", "rung4_demand", "rung4_emp", "p4",
              "p4_in_v8_window"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for d in anchor:
            w.writerow([EXPERIMENT, LABEL, ANCHOR_ID, ANCHOR_NAME, d["year"], d["level"],
                        "%.6f" % d["demand_official"], "%.6f" % d["admitted_official"],
                        "%.10f" % d["p_off"], "%.6f" % d["rationed_official"],
                        "%.10f" % d["congestion_q"], "%.6f" % d["seats"], "%.6f" % d["ger"],
                        "%.6f" % d["rung4_demand"], "%.6f" % d["rung4_emp"],
                        "%.10f" % d["p4"], d["p4_v8_window"]])
    return path


def falsifier(levels, recs):
    """Primary reading: per level, share of cells with p_off < 0.50 (no rationing conjunct)."""
    checked = []
    tripped_levels = []
    for level in ("upper_secondary", "tertiary"):
        L = next(x for x in levels if x["level"] == level)
        trips = L["s50"] > 100.0 * DEEP_SHARE_MAX
        if trips:
            tripped_levels.append(level)
        checked.append({
            "level": level,
            "n_cells": L["n"],
            "count_p_off_lt050": L["c50"],
            "share_pct": round(L["s50"], 4),
            "threshold_share_pct": 100.0 * DEEP_SHARE_MAX,
            "comparison": "share > 20% (strict)",
            "trips": trips,
        })

    # Declared secondary reading: per individual country series, non-verdict-bearing.
    per_country = []
    for level in ("upper_secondary", "tertiary"):
        for country_id in sorted({c["country_id"] for c in recs}, key=int):
            sub = [c for c in recs if c["level"] == level and c["country_id"] == country_id]
            n = len(sub)
            c50 = sum(1 for c in sub if c["p_off"] < DEEP_BAR)
            per_country.append({
                "level": level,
                "country_id": country_id,
                "country": sub[0]["country"],
                "n_years": n,
                "count_p_off_lt050": c50,
                "share_pct": round(pct(c50, n), 4),
                "exceeds_20pct": pct(c50, n) > 100.0 * DEEP_SHARE_MAX,
            })
    exceed = [d for d in per_country if d["exceeds_20pct"]]

    tripped = bool(tripped_levels)
    doc = {
        "experiment": EXPERIMENT,
        "label": LABEL,
        "brief": "SYNTHESIS_022.md section 6 EXP-8, threshold + falsifier, item 5",
        "predeclaration": {"file": "PRE_DECLARATIONS.md", "sha256": PREDECL_SHA256,
                           "thresholds_changed_after_freeze": False},
        "falsifier_text_verbatim": (
            "if any upper/tertiary level-year has p_off < 0.50 in >20% of its years, the "
            "architecture conclusion is reversed and RUNG-PROB (EXP-9) is not dispatched"
        ),
        "measure": {
            "p_off": "admitted_official / demand_official",
            "rationed_conjunct": "NONE (the falsifier clause states only p_off < 0.50)",
            "deep_bar": DEEP_BAR,
            "share_threshold": DEEP_SHARE_MAX,
            "levels_checked": ["upper_secondary", "tertiary"],
        },
        "primary_reading": {
            "levels": checked,
            "levels_tripped": tripped_levels,
            "tripped": tripped,
            "outcome": "TRIPPED" if tripped else "NOT TRIPPED",
        },
        "secondary_reading_non_verdict_bearing": {
            "note": ("per-country per-level series; reported for transparency only and it "
                     "cannot change the outcome, the branch or the dispatch record"),
            "n_series_checked": len(per_country),
            "n_series_exceeding_20pct": len(exceed),
            "series_exceeding_20pct": exceed,
            "detail_file": "results/GATE_LOCUS_SECONDARY_S3.csv",
        },
        "consequence": {
            "architecture_conclusion": "REVERSED" if tripped else "NOT REVERSED",
            "statement": (
                "Falsifier tripped: the architecture conclusion is reversed and RUNG-PROB "
                "(EXP-9) is NOT dispatched."
                if tripped else
                "Falsifier does not trip: the architecture conclusion is not reversed by this "
                "clause, and EXP-9 is not blocked by it. Dispatch remains the Lead's action."
            ),
            "exp9_rung_prob": "NOT DISPATCHED (falsifier)" if tripped else "NOT BLOCKED BY FALSIFIER",
        },
    }
    path = RESULTS / "GATE_LOCUS_FALSIFIER.json"
    path.write_text(json.dumps(doc, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    return path, doc


def secondary_s1():
    if sha256(GATES) != GATES_SHA256:
        sys.exit("FATAL: gate-panel hash mismatch")
    with open(GATES, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) != 840:
        sys.exit(f"FATAL: expected 840 gate rows, found {len(rows)}")
    path = RESULTS / "GATE_LOCUS_SECONDARY_S1.csv"
    header = ["experiment", "label", "country_type", "host_country", "gate", "gate_name",
              "n_years", "mean_pi0", "count_pi0_lt095", "share_pi0_lt095_pct",
              "count_pi0_lt050", "share_pi0_lt050_pct", "count_Q_gt1", "share_Q_gt1_pct",
              "mean_Q"]
    rows_out = []
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for ctype in sorted({r["country_type"] for r in rows}):
            for gate in ("g0", "g1", "g2", "g3", "g4"):
                sub = sorted((r for r in rows if r["country_type"] == ctype and r["gate"] == gate),
                             key=lambda r: int(r["year"]))
                n = len(sub)
                pi0s = [num(r, "pi0") for r in sub]
                qs = [num(r, "Q") for r in sub]
                c95 = sum(1 for v in pi0s if v < 0.95)
                c50 = sum(1 for v in pi0s if v < DEEP_BAR)
                q1 = sum(1 for v in qs if v > 1.0)
                rec = [EXPERIMENT, LABEL, ctype, sub[0]["host_country"], gate,
                       sub[0]["gate_name"], n, "%.6f" % (sum(pi0s) / n),
                       c95, "%.4f" % pct(c95, n), c50, "%.4f" % pct(c50, n),
                       q1, "%.4f" % pct(q1, n), "%.6f" % (sum(qs) / n)]
                rows_out.append(rec)
                w.writerow(rec)
    return path, rows_out


def secondary_s1b():
    """Bottom-up rows behind leg S1: the anchor type's own gate series, all 56 years x 5 gates.

    A sub-detail of the declared leg S1 (the rows whose means S1 reports); no verdict weight.
    """
    with open(GATES, newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["host_country"] == ANCHOR_NAME]
    path = RESULTS / "GATE_LOCUS_SECONDARY_S1B.csv"
    header = ["experiment", "label", "host_country", "year", "gate", "gate_name", "Q", "pi0",
              "pi1", "candidates", "capacity", "advances", "advance_ratio"]
    rows.sort(key=lambda r: (int(r["year"]), r["gate"]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            cand = num(r, "candidates")
            w.writerow([EXPERIMENT, LABEL, ANCHOR_NAME, r["year"], r["gate"], r["gate_name"],
                        "%.10f" % num(r, "Q"), "%.10f" % num(r, "pi0"), "%.10f" % num(r, "pi1"),
                        "%.6f" % cand, "%.6f" % num(r, "capacity"),
                        "%.6f" % num(r, "advances"),
                        "%.10f" % (num(r, "advances") / cand if cand else 0.0)])
    return path


def secondary_s2(panel_rows):
    path = RESULTS / "GATE_LOCUS_SECONDARY_S2.csv"
    header = ["experiment", "label", "country", "year", "level", "p_off",
              "rationed_official", "congestion_q", "seats"]
    sub = sorted((r for r in panel_rows if r["country_id"] == ANCHOR_ID),
                 key=lambda r: (int(r["year"]), LEVELS.index(r["level"])))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for r in sub:
            demand = num(r, "demand_official")
            w.writerow([EXPERIMENT, LABEL, ANCHOR_NAME, r["year"], r["level"],
                        "%.10f" % (num(r, "admitted_official") / demand),
                        "%.6f" % num(r, "rationed_official"),
                        "%.10f" % num(r, "congestion_q"), "%.6f" % num(r, "seats")])
    return path


def secondary_s3(recs):
    path = RESULTS / "GATE_LOCUS_SECONDARY_S3.csv"
    header = ["experiment", "label", "view", "level", "key", "n_cells",
              "count_p_off_lt095", "share_lt095_pct", "count_p_off_lt099",
              "share_lt099_pct", "count_p_off_lt050", "share_lt050_pct"]
    countries = sorted({c["country_id"] for c in recs}, key=int)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for view, keyname in (("by_country", "country"), ("by_year", "year")):
            for level in ("upper_secondary", "tertiary"):
                sub = [c for c in recs if c["level"] == level]
                if view == "by_country":
                    keys = [(cid, next(c for c in sub if c["country_id"] == cid)["country"])
                            for cid in countries]
                else:
                    years = sorted({c["year"] for c in sub})
                    keys = [(str(y), str(y)) for y in years]
                for key, label in keys:
                    cells = [c for c in sub if (c["country_id"] == key if view == "by_country"
                                                else str(c["year"]) == key)]
                    n = len(cells)
                    c95 = sum(1 for c in cells if c["p_off"] < BAR_PRIMARY)
                    c99 = sum(1 for c in cells if c["p_off"] < BAR_SECONDARY)
                    c50 = sum(1 for c in cells if c["p_off"] < DEEP_BAR)
                    w.writerow([EXPERIMENT, LABEL, view, level, label, n,
                                c95, "%.4f" % pct(c95, n), c99, "%.4f" % pct(c99, n),
                                c50, "%.4f" % pct(c50, n)])
    return path


def main():
    RESULTS.mkdir(exist_ok=True)
    panel_rows = load_panel()
    recs = cell_records(panel_rows)
    levels = per_level(recs)

    print("=" * 88)
    print("EXP-8 GATE-LOCUS  |  LABEL: SYNTHETIC  |  read-only on frozen panels")
    print("=" * 88)
    print("panel  %s" % PANEL_SHA256)
    print("gates  %s" % GATES_SHA256)
    print("predec %s" % PREDECL_SHA256)
    print("")

    p_res = write_results(levels)
    print("PER-LEVEL RATIONING SHARES (p_off < bar AND rationed_official > 0)")
    print("%-17s %5s %10s %-12s %10s %-12s %-14s" % (
        "level", "n", "<0.95", "verdict", "<0.99", "verdict", "headline"))
    for L in levels:
        print("%-17s %5d %6.2f%% %-12s %6.2f%% %-12s %-14s" % (
            L["level"], L["n"], L["s95"], L["v95"], L["s99"], L["v99"], L["headline"]))
    print("")

    calib_ok = all(abs(L["s99"] - COUNCIL_CALIBRATION[L["level"]]) <= 0.1 for L in levels)
    print("CALIBRATION-REPRODUCED: %s  (bar-99 vs Council V3: primary 87.4, lower 93.3, "
          "upper 6.5, tertiary 0)" % ("YES" if calib_ok else "NO"))
    if not calib_ok:
        sys.exit("FATAL: bar-99 shares do not reproduce the Council's calibration; "
                 "the panel or the definition is not the one predeclared")

    anchor = anchor_rows(panel_rows)
    p_anchor = write_anchor(anchor)
    print("")
    print("ANCHOR TYPE %s — gate state (p_off / rationed_official / congestion_q / p4)" % ANCHOR_NAME)
    print("%5s %-17s %10s %14s %10s %10s" % ("year", "level", "p_off", "rationed", "Q", "p4"))
    for d in anchor:
        print("%5d %-17s %10.6f %14.4f %10.4f %10.4f" % (
            d["year"], d["level"], d["p_off"], d["rationed_official"],
            d["congestion_q"], d["p4"]))

    upper_anchor = [d for d in anchor if d["level"] == "upper_secondary"]
    print("")
    print("anchor upper_gate p_off: " + ", ".join(
        "%d=%.6f" % (d["year"], d["p_off"]) for d in upper_anchor))
    print("anchor upper_gate rationed_official: " + ", ".join(
        "%d=%.4f" % (d["year"], d["rationed_official"]) for d in upper_anchor))

    # V8 reproduction check: p4 on upper-secondary rows, 2010+.
    p4_series = []
    for r in sorted((r for r in panel_rows if r["level"] == "upper_secondary"
                     and int(r["year"]) >= V8_WINDOW_FROM),
                    key=lambda r: (int(r["country_id"]), int(r["year"]))):
        d = num(r, "rung4_demand")
        p4_series.append((r["country"], int(r["country_id"]),
                          num(r, "rung4_emp") / d if d else None))
    vals = sorted(v for _, _, v in p4_series if v is not None)
    median_all = vals[len(vals) // 2] if len(vals) % 2 else 0.5 * (vals[len(vals) // 2 - 1] + vals[len(vals) // 2])

    def median_for(country_id):
        vs = sorted(v for _, cid, v in p4_series if cid == country_id and v is not None)
        m = len(vs) // 2
        return vs[m] if len(vs) % 2 else 0.5 * (vs[m - 1] + vs[m])

    print("")
    print("RUNG-4 ABSORPTION p4 = rung4_emp/rung4_demand (upper-secondary rows, 2010+; n=%d)"
          % len(vals))
    print("  panel median      %.4f" % median_all)
    print("  SYN00_PHL_LIKE    %.4f" % median_for(0))
    print("  SYN28             %.4f" % median_for(28))
    print("  SYN18             %.4f" % median_for(18))
    v8_ok = (abs(median_all - 0.507) <= 0.002 and abs(median_for(0) - 0.151) <= 0.002
             and abs(median_for(28) - 0.177) <= 0.002 and abs(median_for(18) - 1.0) <= 1e-9)
    print("V8-REPRODUCED: %s  (0.507 / 0.151 / 0.177 / 1.000)" % ("YES" if v8_ok else "NO"))
    if not v8_ok:
        sys.exit("FATAL: p4 medians do not reproduce the Council's V8 figures")

    p_fal, fal = falsifier(levels, recs)
    print("")
    print("FALSIFIER (p_off < 0.50 in > 20% of a level's years)")
    for d in fal["primary_reading"]["levels"]:
        print("  %-17s %5d cells  %5d below 0.50  %6.2f%%  trips=%s" % (
            d["level"], d["n_cells"], d["count_p_off_lt050"], d["share_pct"],
            "yes" if d["trips"] else "no"))
    print("  PRIMARY OUTCOME: %s" % fal["primary_reading"]["outcome"])
    print("  secondary per-series reading: %d of %d series exceed 20%%" % (
        fal["secondary_reading_non_verdict_bearing"]["n_series_exceeding_20pct"],
        fal["secondary_reading_non_verdict_bearing"]["n_series_checked"]))

    # Predeclared branch (section 7).
    up = next(L for L in levels if L["level"] == "upper_secondary")
    te = next(L for L in levels if L["level"] == "tertiary")
    if up["v95"] == up["v99"] == "UNRATIONED" and te["v95"] == te["v99"] == "UNRATIONED":
        state = "POSITIVE"
    elif up["v95"] == up["v99"] == "GATE BINDS":
        state = "NEGATIVE"
    else:
        state = "MIXED"
    tripped = fal["primary_reading"]["tripped"]
    if tripped:
        dispatch = "NOT DISPATCHED (falsifier tripped)"
    elif state == "POSITIVE":
        dispatch = "DISPATCH-ELIGIBLE (Lead action; falsifier clean)"
    elif state == "NEGATIVE":
        dispatch = "DISPATCH-ELIGIBLE (Lead action; NEGATIVE branch: g2 re-declaration admissible)"
    else:
        dispatch = "CONDITIONAL (MIXED branch: Council decision)"

    print("")
    print("ARCHITECTURE STATE (predeclared section 7): %s" % state)
    print("EXP-9 RUNG-PROB dispatch: %s" % dispatch)

    p_s1, s1 = secondary_s1()
    p_s1b = secondary_s1b()
    p_s2 = secondary_s2(panel_rows)
    p_s3 = secondary_s3(recs)
    print("")
    print("GATE PANEL (v1.3, secondary S1) — mean pi0 by gate and type:")
    for ctype in ("SYN_HKG_LIKE", "SYN_KHM_LIKE", "SYN_PHL_LIKE"):
        cells = [r for r in s1 if r[2] == ctype]
        print("  %-15s " % ctype + "  ".join("%s=%.3f(<0.95 %5.1f%%)" % (
            r[4], float(r[7]), float(r[9])) for r in cells))
    print("")
    print("GATE PANEL (v1.3, secondary S1B) — anchor type, four anchor years:")
    with open(GATES, newline="", encoding="utf-8") as fh:
        grows = [r for r in csv.DictReader(fh) if r["host_country"] == ANCHOR_NAME
                 and r["year"] in ANCHOR_YEARS]
    grows.sort(key=lambda r: (int(r["year"]), r["gate"]))
    for r in grows:
        print("  %s %-3s Q=%8.4f pi0=%8.4f  cand=%12.1f cap=%12.1f adv=%12.1f" % (
            r["year"], r["gate"], num(r, "Q"), num(r, "pi0"),
            num(r, "candidates"), num(r, "capacity"), num(r, "advances")))
    print("")
    print("wrote:")
    for p in (p_res, p_anchor, p_fal, p_s1, p_s1b, p_s2, p_s3):
        print("  %s  %s" % (sha256(p), p.name))

    return 0


if __name__ == "__main__":
    sys.exit(main())
