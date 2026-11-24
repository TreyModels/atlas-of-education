#!/usr/bin/env python3
"""validate_run.py — SIMULATION ONLY (eduengine toy worlds; no empirical/causal claims).

Independent validity checks on the committed sweep outputs (nothing here re-simulates):

  1. EXIT-PARTITION check on every one of the 16,000 raw seed-level rows: the eight exit categories from
     `aggregate_exits()` must sum to 1.0 within 1e-6 (prereg §1, §9).
  2. CELL-MEAN check: recompute the seed mean of ger_sim / liq_share / tut_rate for all 800 cells directly
     from the raw runs CSV and compare with the committed per-cell summary JSON.
  3. GER DECLARATION check: `ger_sim` must equal 1 - never_share in every row (declared simulated
     participation, not an empirical GER).
  4. REPRODUCIBILITY: the 360-run re-run of 18 cells (3 X x 3 Y x 2 gates x seeds 0..19) must reproduce the
     corresponding rows of the full 16,000-run sweep bit-for-bit on every shared numeric field.

Writes data/validity_checks.json. Read-only; no box interaction; no power/watcher actions.
"""
import csv
import json
import os
import sys

import numpy as np

LABEL = "SIMULATION ONLY - eduengine toy worlds; illustrative parameters; no causal/empirical claims"
SHARES = ["liq_share", "gate_fail_share", "finished_share", "never_share", "no_seat_share",
          "not_admitted_share", "choice_share", "censored_share"]
NUM_FIELDS = ["ger_sim", "liq_share", "tut_rate", "tut_q5_q1_gap", "completion_lower", "completion_upper",
              "liq_share_q1", "gate_fail_share_q1", "liq_share_q5", "gate_fail_share_q5",
              "tut_share_q1", "tut_share_q5", "completion_lower_q_gap", "completion_upper_q_gap",
              "parity_wealth_lower", "formal_rate", "formal_hire_q1", "formal_hire_q5", "queue", "grad_unemp",
              "gate_fail_share", "censored_share", "choice_share", "never_share", "no_seat_share",
              "not_admitted_share", "finished_share", "gate_pass_rate_0", "gate_pass_rate_1",
              "gate_pass_rate_2", "gate_pass_rate_3", "cut_0", "cut_1", "cut_2", "cut_3",
              "cut_adm_0", "cut_adm_1", "cut_adm_2", "cut_adm_3", "x_vac_per_lower_complete",
              "x_vac_per_gate_pass", "n_pop_measured", "n_cohorts_measured"] + SHARES


def fnum(s):
    return None if s is None or s == "" else float(s)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(here, "data")
    runs_csv = os.path.join(data, "phase_sweep_full_runs.csv")
    summary_json = os.path.join(data, "phase_sweep_full_summary.json")
    repro_csv = os.path.join(data, "repro_subset_runs.csv")
    out_path = os.path.join(data, "validity_checks.json")

    with open(runs_csv) as f:
        rows = list(csv.DictReader(f))
    with open(summary_json) as f:
        run = json.load(f)
    with open(repro_csv) as f:
        repro = list(csv.DictReader(f))

    res = {"label": LABEL, "inputs": {"runs_csv": runs_csv, "summary_json": summary_json,
                                      "repro_csv": repro_csv}}

    # 1. exit partition on every raw row
    worst = 0.0
    worst_row = None
    for r in rows:
        tot = sum(fnum(r[s]) for s in SHARES)
        d = abs(tot - 1.0)
        if d > worst:
            worst, worst_row = d, {"gate": r["gate"], "x_index": r["x_index"], "y_index": r["y_index"],
                                   "seed": r["seed"], "sum": tot}
    res["exit_partition"] = {"n_rows": len(rows), "max_abs_deviation_from_1": worst,
                             "tolerance": 1e-6, "passed": worst <= 1e-6, "worst_row": worst_row}

    # 2. cell means recomputed from the raw rows vs the committed summary
    cells = {(c["gate"], int(c["x_index"]), int(c["y_index"])): c for c in run["cells"]}
    acc = {}
    for r in rows:
        k = (r["gate"], int(r["x_index"]), int(r["y_index"]))
        d = acc.setdefault(k, {"ger_sim": [], "liq_share": [], "tut_rate": []})
        for m in d:
            v = fnum(r[m])
            if v is not None:
                d[m].append(v)
    worst_cell = 0.0
    worst_cell_key = None
    n_compared = 0
    for k, d in acc.items():
        c = cells[k]
        for m, vals in d.items():
            if not vals or c.get(m) is None:
                continue
            diff = abs(float(np.mean(vals)) - float(c[m]))
            n_compared += 1
            if diff > worst_cell:
                worst_cell, worst_cell_key = diff, {"cell": list(k), "metric": m,
                                                    "raw_mean": float(np.mean(vals)),
                                                    "summary_value": float(c[m])}
    res["cell_means"] = {"n_cells": len(acc), "n_values_compared": n_compared,
                         "max_abs_diff": worst_cell, "tolerance": 1e-6,
                         "passed": worst_cell <= 1e-6, "worst": worst_cell_key}

    # 3. ger_sim == 1 - never_share, every row
    worst_ger = 0.0
    for r in rows:
        g, nv = fnum(r["ger_sim"]), fnum(r["never_share"])
        if g is None or nv is None:
            continue
        worst_ger = max(worst_ger, abs(g - (1.0 - nv)))
    res["ger_sim_definition"] = {"max_abs_diff_from_1_minus_never_share": worst_ger, "tolerance": 1e-8,
                                 "passed": worst_ger <= 1e-8}

    # 4. reproducibility: match repro rows to full-sweep rows on (gate, x_vac0, fee_primary, seed)
    def key(r):
        return (r["gate"], round(float(r["x_vac0"]), 9), round(float(r["fee_primary"]), 9), int(r["seed"]))
    full = {key(r): r for r in rows}
    mism = []
    n_matched = 0
    max_abs = 0.0
    for r in repro:
        k = key(r)
        if k not in full:
            mism.append({"repro_row": k, "reason": "no matching full-sweep row"})
            continue
        n_matched += 1
        for fld in NUM_FIELDS:
            if fld not in r or fld not in full[k]:
                continue
            a, b = fnum(r[fld]), fnum(full[k][fld])
            if a is None and b is None:
                continue
            if a is None or b is None:
                mism.append({"row": k, "field": fld, "repro": a, "full": b, "reason": "None mismatch"})
                continue
            d = abs(a - b)
            max_abs = max(max_abs, d)
            if d > 1e-9:
                mism.append({"row": k, "field": fld, "repro": a, "full": b, "abs_diff": d})
    res["reproducibility"] = {"n_repro_rows": len(repro), "n_matched": n_matched,
                              "n_field_comparisons": n_matched * len(NUM_FIELDS),
                              "n_mismatches": len(mism), "max_abs_diff": max_abs,
                              "passed": len(mism) == 0 and n_matched == len(repro),
                              "first_mismatches": mism[:10]}

    ok = all(res[k]["passed"] for k in ("exit_partition", "cell_means", "ger_sim_definition",
                                        "reproducibility"))
    res["all_passed"] = ok
    with open(out_path, "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items()
                                                             if kk in ("n_rows", "passed", "max_abs_deviation_from_1",
                                                                       "n_cells", "max_abs_diff",
                                                                       "n_matched", "n_mismatches",
                                                                       "max_abs_diff_from_1_minus_never_share")})
                      for k, v in res.items() if k in ("exit_partition", "cell_means", "ger_sim_definition",
                                                       "reproducibility", "all_passed")}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
