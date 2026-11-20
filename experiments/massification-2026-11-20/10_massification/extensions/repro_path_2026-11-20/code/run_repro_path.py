#!/usr/bin/env python3
"""EXP-7 REPRO-PATH — deterministic audit of the frozen v1.2 panel against observed PHL completion.

LABEL: SYNTHETIC (generator side) / OBSERVED (PHL UIS completion side).
No RNG. No timestamps. No writes outside this experiment directory. The frozen generator and the
frozen panel are read-only inputs and are never written, here or anywhere.

Leg (a): 33 observed (year, level) cells (11 per level) vs SYN00_PHL_LIKE completion_uis x 100.
Leg (b): declared constraint upper_t <= kappa * lower_{t-3}, kappa = 0.949, applied in memory as a
         projection (min) on a byte-identical copy of the frozen panel.

Every threshold, cell set, class boundary and verdict word is fixed in PRE_DECLARATIONS.md, whose
sha256 is embedded below; the script refuses to run if the file on disk does not match.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import statistics
import sys

# ---------------------------------------------------------------------------------------------
# Frozen constants. These are the predeclared values; they are NOT parameters of a fit.
# ---------------------------------------------------------------------------------------------
PREDECL_SHA256 = "74f9d0e0ece9680eaba470f3979f5d1e6042d7851585962cb1cdf7d365b3db12"
PREDECL_NAME = "PRE_DECLARATIONS.md"

PANEL_REL = "10_massification/extensions/synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv"
PANEL_SHA256 = "14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac"
SIM_REL = "10_massification/extensions/synthetic_2026-11-20/generator_v1_2/code/sim_v1_2.py"
SIM_SHA256 = "61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c"
PARAMS_REL = "10_massification/extensions/synthetic_2026-11-20/generator_v1_2/PARAMS.md"
GEN_MANIFEST_REL = "10_massification/extensions/synthetic_2026-11-20/generator_v1_2/RUN_MANIFEST.json"
OBS_REL = "10_massification/data/UNIVERSALIZATION_SERIES.csv"
OBS_SHA256 = "85bc869396ebfcb39e3e1a21a31af219e75a07326c738a51d2bfdbe536737ddb"

ANCHOR = "SYN00_PHL_LIKE"
LEVELS = ("primary", "lower_secondary", "upper_secondary")
OBS_INDICATOR = {
    "primary": "completion_primary",
    "lower_secondary": "completion_lower_secondary",
    "upper_secondary": "completion_upper_secondary",
}
KAPPA = 0.949          # verdict-bearing: median of the 8 observed PHL pairs (declared, never fitted)
KAPPA_SENS = 0.960     # non-verdict-bearing sensitivity: pre-2018 median
TOL_PP = 5.0           # inclusive
WITHIN10_PP = 10.0
WITHIN_BAR = 17        # >= 17/33 -> PATH-REPRODUCED
N_COMPARISONS = 33
YEAR_MIN, YEAR_MAX = 1970, 2025
LAG = 3
B1_LO, B1_HI = 73.0, 77.0
B2_HI_EXCL = 71.0
B3_ABS_DELTA = 1.0

FLOAT_FORMAT = "%.10g"
EXPERIMENT = "EXP-7 REPRO-PATH"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_root(start: str) -> str:
    """Walk up until the directory that contains 08_council/ and 10_massification/."""
    cur = os.path.abspath(start)
    for _ in range(12):
        if os.path.isdir(os.path.join(cur, "08_council")) and os.path.isdir(
            os.path.join(cur, "10_massification")
        ):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    raise SystemExit("could not locate programme root from %s" % start)


def fmt(x, nd=4):
    if x is None:
        return "MISSING"
    return f"{x:.{nd}f}"


def write_csv(path: str, header, rows) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


# ---------------------------------------------------------------------------------------------
# inputs
# ---------------------------------------------------------------------------------------------
def read_observed(root: str):
    """PHL observed completion cells: (year, level) -> value in percent. Exactly 33 keys."""
    path = os.path.join(root, OBS_REL)
    cells = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["iso3"] != "PHL":
                continue
            if r["status"] != "observed":
                continue
            for lvl, ind in OBS_INDICATOR.items():
                if r["indicator"] == ind:
                    key = (int(r["year"]), lvl)
                    if key in cells:
                        raise SystemExit("duplicate observed cell %r" % (key,))
                    cells[key] = float(r["value"])
    return cells


def read_panel(path: str):
    """Anchor-type completion_uis as fractions; plus the file's own row count for reporting."""
    vals = {}
    rows = 0
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows += 1
            if r["country"] != ANCHOR:
                continue
            lvl = r["level"]
            if lvl not in ("primary", "lower_secondary", "upper_secondary", "tertiary"):
                continue
            try:
                v = float(r["completion_uis"])
            except (TypeError, ValueError):
                v = None
            vals[(int(r["year"]), lvl)] = v
    return vals, rows


def observed_pairs(cells):
    """V4/V5 pair rule: lower at t-3 exact, else nearest observed lower year within +/-1 y of t-3,
    else drop. Deterministic tie-break: earlier year first (no tie occurs on these data; recorded
    in the manifest as an implementation detail that is never exercised)."""
    lower = {y: v for (y, l), v in cells.items() if l == "lower_secondary"}
    upper = {y: v for (y, l), v in cells.items() if l == "upper_secondary"}
    pairs = []
    for t in sorted(upper):
        target = t - LAG
        if target in lower:
            pairs.append((t, target, upper[t] / lower[target]))
            continue
        cands = [y for y in lower if abs(y - target) <= 1]
        if not cands:
            continue
        y = sorted(cands)[0]
        pairs.append((t, y, upper[t] / lower[y]))
    return pairs


# ---------------------------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="EXP-7 REPRO-PATH (deterministic, no RNG)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results"))
    args = ap.parse_args(argv)
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)

    here = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.dirname(here)
    root = find_root(exp_dir)

    # ---- predeclaration guard: refuse to run against a changed spec -------------------------
    predecl_path = os.path.join(exp_dir, PREDECL_NAME)
    predecl_sha = sha256_file(predecl_path)
    if predecl_sha != PREDECL_SHA256:
        print("REFUSING TO RUN: %s sha256 %s != declared %s" % (PREDECL_NAME, predecl_sha, PREDECL_SHA256))
        return 2

    # ---- input hashes (G1 / G4 side) -------------------------------------------------------
    panel_path = os.path.join(root, PANEL_REL)
    sim_path = os.path.join(root, SIM_REL)
    params_path = os.path.join(root, PARAMS_REL)
    gen_manifest_path = os.path.join(root, GEN_MANIFEST_REL)
    obs_path = os.path.join(root, OBS_REL)

    before = {
        "panel": sha256_file(panel_path),
        "sim_code": sha256_file(sim_path),
        "params": sha256_file(params_path),
        "generator_manifest": sha256_file(gen_manifest_path),
        "observed": sha256_file(obs_path),
    }
    if before["panel"] != PANEL_SHA256:
        print("REFUSING TO RUN: frozen panel sha256 %s != declared %s" % (before["panel"], PANEL_SHA256))
        return 2
    if before["sim_code"] != SIM_SHA256:
        print("REFUSING TO RUN: frozen sim_v1_2.py sha256 %s != declared %s" % (before["sim_code"], SIM_SHA256))
        return 2
    if before["observed"] != OBS_SHA256:
        print("REFUSING TO RUN: observed series sha256 %s != declared %s" % (before["observed"], OBS_SHA256))
        return 2

    # ---- G2: byte-identical unlinked arm (the copy that everything downstream reads) -------
    copy_path = os.path.join(out, "BASELINE_UNLINKED_PANEL.csv")
    shutil.copyfile(panel_path, copy_path)
    copy_sha = sha256_file(copy_path)
    g2 = copy_sha == PANEL_SHA256

    cells = read_observed(root)
    if len(cells) != N_COMPARISONS:
        print("REFUSING TO SCORE: observed universe is %d cells, declared %d" % (len(cells), N_COMPARISONS))
        return 3

    panel_vals, panel_rows = read_panel(panel_path)      # frozen original
    copy_vals, copy_rows = read_panel(copy_path)         # the arm actually analysed

    # =========================================================================================
    # LEG (a) — 33 observed cells vs anchor-type synthetic
    # =========================================================================================
    comp_rows = []
    devs = []
    n_within5 = 0
    n_within10 = 0
    n_missing = 0
    n_above = 0
    per_level_within5 = {l: 0 for l in LEVELS}
    per_level_n = {l: 0 for l in LEVELS}
    per_level_devs = {l: [] for l in LEVELS}

    for lvl in LEVELS:
        for y in sorted(yy for (yy, ll) in cells if ll == lvl):
            obs = cells[(y, lvl)]
            syn_frac = copy_vals.get((y, lvl))
            per_level_n[lvl] += 1
            if syn_frac is None:
                n_missing += 1
                comp_rows.append(
                    [EXPERIMENT, "SYNTHETIC", "OBSERVED", ANCHOR, lvl, lvl, y, "MISSING", f"{obs:.{4}f}",
                     "MISSING", "NO", "NO", "MISSING", "MISSING_CELL_NO_IMPUTATION"]
                )
                continue
            syn = syn_frac * 100.0
            d = syn - obs
            within5 = abs(d) <= TOL_PP
            within10 = abs(d) <= WITHIN10_PP
            n_within5 += int(within5)
            n_within10 += int(within10)
            per_level_within5[lvl] += int(within5)
            per_level_devs[lvl].append(d)
            devs.append((d, y, lvl))
            if d > 0:
                n_above += 1
            comp_rows.append(
                [EXPERIMENT, "SYNTHETIC", "OBSERVED", ANCHOR, lvl, lvl, y,
                 f"{syn:.{4}f}", f"{obs:.{4}f}", f"{d:.{4}f}", "YES" if within5 else "NO",
                 "YES" if within10 else "NO", f"{abs(d):.{4}f}", "COMPARED"]
            )

    write_csv(
        os.path.join(out, "PATH_COMPARISONS.csv"),
        ["experiment", "label_synthetic", "label_observed", "synthetic_country", "level_observed",
         "level_synthetic", "year", "synthetic_completion_pct", "observed_completion_pct",
         "deviation_pp", "within_5pp", "within_10pp", "abs_deviation_pp", "comparison_status"],
        comp_rows,
    )

    verdict_a = "PATH-REPRODUCED" if n_within5 >= WITHIN_BAR else "ENDPOINT-ONLY"
    medians = {}
    for lvl in LEVELS:
        medians[lvl] = statistics.median(per_level_devs[lvl]) if per_level_devs[lvl] else None
    worst = min(devs, key=lambda t: t[0]) if devs else None
    v1_check = (
        n_within5 == 9 and n_within10 == 13
        and abs(medians["primary"] - (-4.30)) < 0.005
        and abs(medians["lower_secondary"] - (-29.44)) < 0.005
        and abs(medians["upper_secondary"] - (-27.59)) < 0.005
        and worst is not None and abs(worst[0] - (-36.62)) < 0.005
        and worst[1] == 1999 and worst[2] == "upper_secondary"
    )

    # =========================================================================================
    # LEG (b) — declared kappa link, in memory, on the byte-identical copy
    # =========================================================================================
    upper = {y: v for (y, l), v in copy_vals.items() if l == "upper_secondary"}
    lower = {y: v for (y, l), v in copy_vals.items() if l == "lower_secondary"}

    link_rows = []
    scored = 0
    viol_before = 0
    viol_after = 0
    max_viol = None          # (margin_pp, year)
    anchor_ratio_gt_110 = []
    delta_2024 = None
    after_2024 = None
    ratio_2024 = None
    bound_2024 = None
    upper_2024 = None
    after_960_2024 = None
    delta_960_2024 = None

    def project(t, kappa):
        u = upper.get(t)
        lo = lower.get(t - LAG)
        if u is None or lo is None:
            return None
        bound = kappa * lo
        return min(u, bound), bound

    for y in sorted(upper):
        u = upper[y]
        lo = lower.get(y - LAG)
        if lo is None:
            link_rows.append(
                [ANCHOR, y, "NOT-SCORABLE", fmt(u * 100.0), "", "NA", "NA", fmt(KAPPA, 3), "NA", "NA",
                 "NA", fmt(u * 100.0), "0.0000", "NO", fmt(KAPPA, 3), "NA",
                 "NA", "NA", "NA", "no lower_{t-3} in panel (panel starts %d); not imputed" % YEAR_MIN]
            )
            continue
        scored += 1
        ratio = u / lo
        bound = KAPPA * lo
        viol = u > bound
        margin = (u - bound) * 100.0
        linked = min(u, bound)
        delta = (linked - u) * 100.0
        linked_after_viol = linked > bound
        bound_s = KAPPA_SENS * lo
        linked_s = min(u, bound_s)
        delta_s = (linked_s - u) * 100.0
        viol_s = u > bound_s
        if viol:
            viol_before += 1
        if linked_after_viol:
            viol_after += 1
        if viol and (max_viol is None or margin > max_viol[0]):
            max_viol = (margin, y)
        if ratio > 1.10:
            anchor_ratio_gt_110.append(y)
        if y == 2024:
            upper_2024 = u * 100.0
            bound_2024 = bound * 100.0
            after_2024 = linked * 100.0
            delta_2024 = delta
            ratio_2024 = ratio
            after_960_2024 = linked_s * 100.0
            delta_960_2024 = delta_s
        link_rows.append(
            [ANCHOR, y, "SCORED", fmt(u * 100.0), y - LAG, fmt(lo * 100.0), f"{ratio:.6f}",
             fmt(KAPPA, 3), fmt(bound * 100.0), "YES" if viol else "NO", f"{margin:.4f}",
             fmt(linked * 100.0), f"{delta:.4f}", "YES" if linked_after_viol else "NO",
             fmt(KAPPA_SENS, 3), fmt(bound_s * 100.0), fmt(linked_s * 100.0), f"{delta_s:.4f}",
             "YES" if viol_s else "NO", ""]
        )

    # class assignment (predeclared: b2 > b3 > b1; residual b-UNCLASSIFIED)
    def classify(after, delta):
        if after is None or delta is None:
            return "b-UNCLASSIFIED"
        if after < B2_HI_EXCL:
            return "b2"
        if abs(delta) < B3_ABS_DELTA:
            return "b3"
        if B1_LO <= after <= B1_HI:
            return "b1"
        return "b-UNCLASSIFIED"

    class_949 = classify(after_2024, delta_2024)
    class_960 = classify(after_960_2024, delta_960_2024)

    # per-row class column (the 2024 row carries the verdict-bearing class; others carry "-")
    for row in link_rows:
        if row[1] == 2024 and row[2] == "SCORED":
            row[19] = class_949
        elif row[19] == "":
            row[19] = "-"

    write_csv(
        os.path.join(out, "KAPPA_LINK.csv"),
        ["synthetic_country", "year", "status", "upper_t_pct", "lower_t_minus_3_year",
         "lower_t_minus_3_pct", "ratio_upper_over_lower_t3", "kappa_verdict", "bound_pct_kappa_0.949",
         "violation_before", "violation_margin_pp", "upper_linked_pct", "delta_pp", "violation_after",
         "kappa_sensitivity", "bound_pct_kappa_0.960", "upper_linked_0.960_pct", "delta_0.960_pp",
         "violation_before_0.960", "outcome_class"],
        link_rows,
    )

    # kappa provenance: median of the 8 observed PHL pairs must round to 0.949 (sensitivity 0.960)
    pairs = observed_pairs(cells)
    pair_med = statistics.median([p[2] for p in pairs])
    pre2018 = [p[2] for p in pairs if p[0] < 2018]
    pair_med_pre = statistics.median(pre2018) if pre2018 else None
    provenance_ok = len(pairs) == 8 and round(pair_med, 3) == 0.949 and round(pair_med_pre, 3) == 0.960

    # =========================================================================================
    # G3 — the unlinked arm's scored cells equal the frozen original, cell for cell
    # =========================================================================================
    g3 = True
    for y in sorted(upper):
        for l in ("upper_secondary", "lower_secondary"):
            if copy_vals.get((y, l)) != panel_vals.get((y, l)):
                g3 = False
                break

    # ---- G4: generator files unchanged after the run ---------------------------------------
    after = {
        "panel": sha256_file(panel_path),
        "sim_code": sha256_file(sim_path),
        "params": sha256_file(params_path),
        "generator_manifest": sha256_file(gen_manifest_path),
        "observed": sha256_file(obs_path),
    }
    g4 = before == after and after["panel"] == PANEL_SHA256 and after["sim_code"] == SIM_SHA256

    guard_pass = bool(g2 and g3 and g4 and before["panel"] == PANEL_SHA256)
    guard_verdict = "BASELINE-GUARD-PASS" if guard_pass else "BASELINE-GUARD-FAIL"

    guard = {
        "experiment": EXPERIMENT,
        "label": "SYNTHETIC (panel) / OBSERVED (PHL series)",
        "statement": "Descriptive/diagnostic. No causal and no direction claim. The unlinked arm must "
                     "reproduce the frozen panel byte-for-byte; this is the block's falsifier for leg (b).",
        "declared_panel_sha256": PANEL_SHA256,
        "G1_frozen_panel_hash_equals_declared": before["panel"] == PANEL_SHA256,
        "G1_observed_sha256": before["observed"],
        "G2_copy_inside_experiment_dir": {
            "path": "results/BASELINE_UNLINKED_PANEL.csv",
            "sha256": copy_sha,
            "byte_identical_to_frozen": g2,
            "bytes": os.path.getsize(copy_path),
            "rows_including_header": copy_rows + 1,
        },
        "G3_unlinked_arm_cells_equal_frozen_cells": {
            "cells_compared": sum(1 for y in upper if (y, "upper_secondary") in copy_vals)
            + sum(1 for y in lower if (y, "lower_secondary") in copy_vals),
            "match": g3,
            "note": "values used in KAPPA_LINK.csv are read from the byte-identical copy, then checked "
                    "cell-by-cell against the frozen original",
        },
        "G4_generator_files_unchanged_after_run": {
            "before": before,
            "after": after,
            "equal": g4,
            "generator_sim_sha256_expected": SIM_SHA256,
        },
        "generator_files_written_by_this_experiment": [],
        "writes_outside_experiment_dir": [],
        "verdict": guard_verdict,
        "falsifier_triggered": not guard_pass,
    }
    with open(os.path.join(out, "BASELINE_GUARD.json"), "w", encoding="utf-8") as fh:
        json.dump(guard, fh, indent=2, sort_keys=False)
        fh.write("\n")

    # =========================================================================================
    # results table
    # =========================================================================================
    def row(test, stat, value, threshold, verdict, components):
        return [EXPERIMENT, test, stat, value, threshold, verdict, components]

    rows = [
        row("leg_a", "comparisons_reported", str(len(comp_rows)), "= 33; all reported; no subset",
            verdict_a, "11 observed year-level cells per level x 3 levels = 33"),
        row("leg_a", "cells_by_level", "primary 11; lower_secondary 11; upper_secondary 11", "= 33",
            "ENDPOINT-ONLY", "year sets differ by level (2003 upper only; 2021 primary+lower only)"),
        row("leg_a", "within_5pp_count", "%d/%d" % (n_within5, N_COMPARISONS), ">= 17/33 (51.5%)",
            verdict_a, "primary %d/11; lower_secondary %d/11; upper_secondary %d/11"
            % (per_level_within5["primary"], per_level_within5["lower_secondary"],
               per_level_within5["upper_secondary"])),
        row("leg_a", "within_5pp_share_pct", f"{100.0 * n_within5 / N_COMPARISONS:.2f}", ">= 51.5",
            verdict_a, "V1's published count is 9/33 = 27.3%; re-derived here"),
        row("leg_a", "within_10pp_count", "%d/%d" % (n_within10, N_COMPARISONS), "descriptive (no bar)",
            "-", "V1 companion statistic"),
        row("leg_a", "median_deviation_primary_pp", f"{medians['primary']:.4f}", "descriptive (no bar)",
            "-", "SYNTHETIC minus OBSERVED; signed"),
        row("leg_a", "median_deviation_lower_secondary_pp", f"{medians['lower_secondary']:.4f}",
            "descriptive (no bar)", "-", "SYNTHETIC minus OBSERVED; signed"),
        row("leg_a", "median_deviation_upper_secondary_pp", f"{medians['upper_secondary']:.4f}",
            "descriptive (no bar)", "-", "SYNTHETIC minus OBSERVED; signed"),
        row("leg_a", "max_abs_miss_pp", f"{worst[0]:.4f}", "descriptive (no bar)", "-",
            "%s %d (largest negative deviation)" % (worst[2], worst[1])),
        row("leg_a", "comparisons_above_observed", str(n_above), "descriptive (no bar)", "-",
            "count of cells where SYNTHETIC > OBSERVED"),
        row("leg_a", "missing_synthetic_cells", str(n_missing), "0 expected; MISSING kept in denominator 33",
            "-", "no imputation and no nearest-year substitution"),
        row("leg_a", "construction_check_vs_V1", "MATCH" if v1_check else "MISMATCH",
            "9/33; 13/33; medians -4.30/-29.44/-27.59; worst -36.62 upper 1999",
            "-", "independent re-derivation reproduces the Council's V1 construction" if v1_check
            else "construction differs from V1; verdict stands on the declared construction"),
        row("leg_b", "scored_cells", str(scored), "= 53 (t = 1973..2025)", "-",
            "anchor type %s; exact 3-year lag; no nearest-year matching" % ANCHOR),
        row("leg_b", "not_scorable_cells", "3 (1970-1972)", "declared NOT-SCORABLE, not imputed",
            "-", "no lower_{t-3} inside the panel"),
        row("leg_b", "violations_before", "%d/%d" % (viol_before, scored), "descriptive; zero not required",
            "-", "upper_t > 0.949*lower_{t-3}, strict, no tolerance"),
        row("leg_b", "violations_after", "%d/%d" % (viol_after, scored), "must be 0/53 (implementation check)",
            "-" if viol_after == 0 else "LINK-IMPLEMENTATION-FAIL",
            "projection min(upper_t, bound) applied in memory; no other change"),
        row("leg_b", "max_violation_margin_pp", f"{max_viol[0]:.4f}" if max_viol else "NA",
            "descriptive (no bar)", "-", "largest excess above the bound, year %d" % max_viol[1]
            if max_viol else "no violations"),
        row("leg_b", "anchor_years_ratio_gt_1.10", str(len(anchor_ratio_gt_110)), "descriptive (no bar)", "-",
            "V2 re-derived: years " + ",".join(str(y) for y in anchor_ratio_gt_110)),
        row("leg_b", "kappa_0.949", f"{KAPPA:.3f}", "declared = median of 8 observed PHL pairs", "-",
            "provenance check: n_pairs=%d median=%.5f pre2018_median=%.5f -> %s"
            % (len(pairs), pair_med, pair_med_pre, "MATCH" if provenance_ok else "KAPPA-PROVENANCE-MISMATCH")),
        row("leg_b", "upper_2024_unlinked_pct", f"{upper_2024:.4f}", "baseline value (frozen panel)",
            "-", "SYN00_PHL_LIKE completion_uis x 100"),
        row("leg_b", "bound_2024_pct_kappa_0.949", f"{bound_2024:.4f}", "0.949 * lower_2021", "-",
            "lower_2021 = %.4f pct" % (lower.get(2021, float("nan")) * 100.0)),
        row("leg_b", "upper_2024_linked_pct", f"{after_2024:.4f}", "b1 in [73..77] / b2 < 71", class_949,
            "after = min(%.4f, %.4f) under the declared projection" % (upper_2024, bound_2024)),
        row("leg_b", "delta_2024_pp", f"{delta_2024:.4f}", "b3 if |delta| < 1.0", "-",
            "linked minus unlinked at 2024"),
        row("leg_b", "ratio_2024", f"{ratio_2024:.6f}", "descriptive (no bar)", "-",
            "upper_2024 / lower_2021"),
        row("leg_b", "outcome_class", class_949, "b1 [73..77] / b2 < 71 / b3 |delta|<1.0; precedence b2>b3>b1",
            class_949, "components: unlinked %.4f; bound %.4f; linked %.4f; delta %.4f; ratio %.6f"
            % (upper_2024, bound_2024, after_2024, delta_2024, ratio_2024)),
        row("leg_b", "sensitivity_kappa_0.960_upper_2024_linked_pct", f"{after_960_2024:.4f}",
            "non-verdict-bearing", "-", "delta %.4f pp; class %s (sensitivity, NOT the verdict)"
            % (delta_960_2024, class_960)),
        row("leg_b", "baseline_guard", guard_verdict,
            "copy sha256 == 14729c51...acf5ac; generator files unchanged", guard_verdict,
            "G1 %s; G2 %s; G3 %s; G4 %s" % (before["panel"] == PANEL_SHA256, g2, g3, g4)),
        row("leg_b", "verdict_b", guard_verdict if not guard_pass else class_949,
            "class plus guard", guard_verdict if not guard_pass else class_949,
            "link %s; %d/%d violations before, %d/%d after"
            % ("INVALID" if not guard_pass else "VALID", viol_before, scored, viol_after, scored)),
    ]
    write_csv(
        os.path.join(out, "REPRO_PATH_RESULTS.csv"),
        ["experiment", "test", "statistic", "value", "threshold", "verdict", "components"],
        rows,
    )

    # ---- console (identical across runs; no paths, no clocks) -------------------------------
    print("%s — deterministic run" % EXPERIMENT)
    print("label: SYNTHETIC (panel) / OBSERVED (PHL completion series)")
    print("predeclaration sha256: %s (verified)" % PREDECL_SHA256)
    print("frozen panel sha256:   %s (verified)" % before["panel"])
    print("")
    print("LEG (a) — 33 observed cells vs %s" % ANCHOR)
    print("  within +/-5 pp: %d/%d  -> %s" % (n_within5, N_COMPARISONS, verdict_a))
    print("  within +/-10 pp: %d/%d" % (n_within10, N_COMPARISONS))
    print("  medians (pp): primary %.4f | lower %.4f | upper %.4f"
          % (medians["primary"], medians["lower_secondary"], medians["upper_secondary"]))
    print("  worst miss: %.4f pp (%s %d)" % (worst[0], worst[2], worst[1]))
    print("  construction check vs V1: %s" % ("MATCH" if v1_check else "MISMATCH"))
    print("")
    print("LEG (b) — declared link upper_t <= %.3f * lower_{t-3}" % KAPPA)
    print("  scored cells: %d (NOT-SCORABLE: 1970-1972)" % scored)
    print("  violations before: %d/%d" % (viol_before, scored))
    print("  violations after:  %d/%d" % (viol_after, scored))
    if max_viol:
        print("  max violation margin: %.4f pp (%d)" % max_viol)
    print("  kappa provenance: n_pairs=%d median=%.5f pre2018=%.5f %s"
          % (len(pairs), pair_med, pair_med_pre, "MATCH" if provenance_ok else "MISMATCH"))
    print("  upper 2024: unlinked %.4f | bound %.4f | linked %.4f | delta %.4f | ratio %.6f"
          % (upper_2024, bound_2024, after_2024, delta_2024, ratio_2024))
    print("  class (kappa 0.949, verdict-bearing): %s" % class_949)
    print("  class (kappa 0.960, sensitivity only): %s (linked %.4f)" % (class_960, after_960_2024))
    print("  baseline guard: %s (G1 %s G2 %s G3 %s G4 %s)"
          % (guard_verdict, before["panel"] == PANEL_SHA256, g2, g3, g4))
    print("")
    print("VERDICT: %s + %s + %s" % (verdict_a, class_949 if guard_pass else "INVALID", guard_verdict))
    return 0


if __name__ == "__main__":
    sys.exit(main())
