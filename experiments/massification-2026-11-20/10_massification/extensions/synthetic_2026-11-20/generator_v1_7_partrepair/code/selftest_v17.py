#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SELFTEST_V17 -- the declared PRE-FREEZE probe (count-blind, synthetic only).

What it checks, and nothing else:
  1. the harness reproduces the frozen v1.3 panel from the **reconstructed** demographic path
     (relative error <= 1e-6) -- i.e. the copied frozen code path is intact;
  2. the repair is **in force**: A17's `demand_share` equals the frozen v1.3 panel's
     `demand_share` (the frozen block's own primitive, called unchanged);
  3. the repaired arm produces the declared tier objects (finite `unfilled_share`, `queue`);
  4. the phase guard **blocks** an observed open in the ARMS phase (positive control).

What it does NOT do: it never opens `UNIVERSALIZATION_SERIES.csv`, never loads a
`completion_*` value, never computes an observed deviation, never forms a 33-cell object and
never prints a level statement. Its demographic input is the frozen v1.3 panel's own path, not
the input the scored run uses.

Run:  python code/selftest_v17.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
CELL = CODE.parent
SYNTH = CELL.parent
FROZEN = CODE / "frozen"
V13_PANEL = SYNTH / "generator_v1_3" / "results" / "synthetic_panel_v1_3.csv"
OUT = CELL / "_scratch" / "SELFTEST.json"

sys.path.insert(0, str(FROZEN))
sys.path.insert(0, str(CODE))

import sim_v1_6_repair as S            # noqa: E402
import sim_v1_3 as V13                 # noqa: E402
import repair_v17 as R                 # noqa: E402
import sim_v1_7_partrepair as D        # noqa: E402

ANCHOR = "SYN00_PHL_LIKE"
TOL_REL = 1e-6
COMPARE_COLUMNS = ("completion_uis", "completion_cohort", "admitted_official", "enrolment",
                   "demand_official", "cohort", "seats", "survival", "survival", "graduates")


def main():
    # ---- predeclaration is the frozen one (hash only; no observed access) ----------------
    pre_sha = hashlib.sha256(D.PREDECL.read_bytes()).hexdigest()
    ok_pre = (pre_sha == D.EXPECTED_PREDECL_SHA)
    report = {"probe": "SELFTEST_V17", "label": "SYNTHETIC",
              "predecl_sha256": pre_sha, "predecl_embedded_ok": ok_pre,
              "observed_file_opened": False, "count_computed": False,
              "level_statement_printed": False,
              "demographic_input": "reconstructed from the frozen v1.3 panel"}

    # ---- the reconstructed demographic path (NO observed read) ---------------------------
    band, pop = {}, {}
    with open(V13_PANEL, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["country"] != ANCHOR:
                continue
            y = int(float(r["year"]))
            pop[y] = float(r["population"])
            if r["level"] == "primary":
                band[y] = float(r["band_population"])
    S_path = S.np.array([band[y] / S.P["band_share"][0] for y in S.YEARS])
    Pop_path = S.np.array([pop[y] for y in S.YEARS])
    S.load_observed_phl_paths = lambda: (S_path, Pop_path, {}, {}, {})

    # ---- 4. phase guard positive control (before anything else) --------------------------
    with D.PhaseGuard(D.OBSERVED_BASENAME, CELL / "_scratch", CELL.parent.parent.parent) as g:
        g.predecl_verified = True
        g.phase = "ARMS"
        try:
            open(D.OBSERVED_PATH, "rb")
        except D.ObservedFileAccess:
            guard_selftest = "BLOCKED-AS-REQUIRED"
        else:
            guard_selftest = "FAILED-OPEN-SUCCEEDED"
    report["phase_guard_selftest"] = guard_selftest

    # ---- run A00 and A17 on the reconstructed synthetic input ---------------------------
    fns = R.make_arm_functions(S, V13)
    recs, hosts = {}, {}
    for arm in ("A00", "A17"):
        cells_fn, alloc_fn = fns[arm]
        S.tier_cells, S.tier_allocate = cells_fn, alloc_fn
        kw = dict(D.COMMON)
        kw.update(D.ENGINE[arm])
        recs[arm], hosts[arm] = S.run_arm_full(**kw)
    S.tier_cells, S.tier_allocate = fns["A00"]

    inputs = S.shadow_inputs_named()
    panels = {a: S.build_panel_v13(recs[a], hosts[a], inputs) for a in ("A00", "A17")}

    # ---- 1. harness identity against the frozen v1.3 panel ------------------------------
    frozen = list(csv.DictReader(open(V13_PANEL, newline="")))
    worst_rel, worst_at, n_cmp, n_bad = 0.0, None, 0, 0
    for mine, ref in zip(panels["A00"], frozen):
        for col in COMPARE_COLUMNS:
            if col not in ref or ref[col] == "":
                continue
            n_cmp += 1
            a = float(mine[col])
            b = float(ref[col])
            rel = abs(a - b) / max(abs(b), 1e-12)
            if rel > worst_rel:
                worst_rel = rel
                worst_at = {"country": ref["country"], "year": ref["year"],
                            "level": ref["level"], "column": col}
            if rel > TOL_REL:
                n_bad += 1
    report["harness_identity"] = {"cells_compared": n_cmp, "differing_gt_tol": n_bad,
                                 "tol_rel": TOL_REL, "max_rel": worst_rel,
                                 "worst": worst_at,
                                 "passes": n_bad == 0}

    # ---- 2. repair in force (A17 demand_share == the frozen block's own) ----------------
    v13 = {(r["country"], int(float(r["year"])), r["level"]): r for r in frozen}
    i17 = {(r["country"], int(float(r["year"])), r["level"]): r for r in panels["A17"]}
    same = n = 0
    for lv in D.LEVELS:
        for y in range(2010, 2025):
            n += 1
            same += int(D.fnum(float(i17[(ANCHOR, y, lv)]["demand_share"])) ==
                        v13[(ANCHOR, y, lv)]["demand_share"])
    report["repair_in_force"] = {"cells": n, "identical": same, "passes": same == n}

    # ---- 3. the tier objects exist and are finite ---------------------------------------
    r = [x for x in recs["A17"] if x["cp"]["name"] == ANCHOR][0]
    t = 2018 - int(S.YEAR_START)
    unf = [float(r["tier_unf"][L, t]) for L in range(3)]
    q = [float(r["tier_ratio_H"][L, t]) for L in range(3)]
    finite = all(x == x and abs(x) < 1e6 for x in unf + q)
    report["tier_objects"] = {"year": 2018, "levels": list(D.LEVELS),
                              "unfilled_share": unf, "queue_ratio": q,
                              "finite": finite,
                              "passes": finite}

    report["passes"] = (ok_pre and guard_selftest == "BLOCKED-AS-REQUIRED"
                        and report["harness_identity"]["passes"]
                        and report["repair_in_force"]["passes"]
                        and report["tier_objects"]["passes"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: report[k] for k in
                      ("predecl_embedded_ok", "phase_guard_selftest", "harness_identity",
                       "repair_in_force", "tier_objects", "passes")}, indent=2,
                     sort_keys=True))
    print("(no observed value read, no cell count computed, no level statement printed)")
    return 0 if report["passes"] else 1


if __name__ == "__main__":
    sys.exit(main())
