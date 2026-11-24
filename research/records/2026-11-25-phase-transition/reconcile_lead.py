#!/usr/bin/env python3
"""Reconcile the Lead's fee-axis sharpness with the pre-registered boundary statistic — SIMULATION ONLY.

The Lead's phase_boundary.py reports, for the fee (Y) axis only:
  J_max      = raw max |adjacent-cell delta|            (not noise-normalised)
  sharpness  = |J_max| / median(|metric level|)         (relative to level, not to noise)
The pre-registration (PREREGISTRATION_PHASE_SWEEP.md §4) defines:
  J_edge     = |delta| / sigma_med, sigma_med = median seed SD of the metric
  sharpness  = J_max / median(J_edge)                   (both axes, X and Y)
  gate contrast C = median J(bar) / median J(quota)

This script recomputes all measures on the same CSVs so the two are directly comparable, and checks
whether the verdict changes. numpy only; reads only pulled CSVs, no runs.
"""
import csv
import json
import os
import statistics as st

import numpy as np

PULL = os.path.expanduser("~/neon-boot/pulled")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results")
SIGMA_FLOOR = 0.002
METRICS = ["tut_q5_q1_gap", "tut_rate", "liq_share", "gate_fail_share",
           "completion_lower", "completion_lower_q_gap"]

SOURCES = {
    "bar_5seed_mine": (os.path.join(HERE, "results", "box_quick", "phase_sweep_quick_bar_summary.csv"), "bar"),
    "quota_5seed_mine": (os.path.join(HERE, "results", "box_quick", "phase_sweep_quick_quota_summary.csv"), "quota"),
    "bar_20seed_lead": (os.path.join(PULL, "phase-sweep-dense", "phase_sweep_quick_summary.csv"), "bar"),
    "quota_5seed_lead": (os.path.join(PULL, "phase-sweep-quota", "phase_sweep_quick_summary.csv"), "quota"),
}


def load(path, gate):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            if r.get("gate") != gate:
                continue
            d = {}
            for k, v in r.items():
                if k == "gate":
                    continue
                d[k] = float(v) if v not in ("", None) else None
            rows.append(d)
    return rows


def axis_edges(rows, key, axis):
    """Adjacent cell pairs along `axis` ('X' -> x_vac0, 'Y' -> fee_primary'), within fixed other level."""
    col = {"X": "x_vac0", "Y": "fee_primary"}[axis]
    other = "fee_primary" if axis == "X" else "x_vac0"
    by = {}
    for r in rows:
        by.setdefault(r[other], []).append(r)
    out = []
    for o, rs in by.items():
        rs = sorted(rs, key=lambda r: r[col])
        vals = [(r[col], r[key], r) for r in rs if r.get(key) is not None]
        for (a0, v0, r0), (a1, v1, r1) in zip(vals, vals[1:]):
            if a1 == a0:
                continue
            out.append(dict(axis=axis, other=o, from_=a0, to=a1, delta=v1 - v0, a=r0, b=r1))
    return out


def measures(rows, key):
    """Pre-registered J/sharpness (both axes) + Lead-style measures (fee axis only)."""
    # pre-registered: sigma_med from the sd_ columns of the same cells
    sds = [r.get(f"sd_{key}") for r in rows if r.get(f"sd_{key}") is not None]
    sigma = max(float(np.median(sds)) if sds else 0.0, SIGMA_FLOOR)
    edges = axis_edges(rows, key, "X") + axis_edges(rows, key, "Y")
    for e in edges:
        e["J"] = abs(e["delta"]) / sigma
    Js = np.array([e["J"] for e in edges])
    mx = max(edges, key=lambda e: e["J"])
    medJ = float(np.median(Js))
    prereg = dict(sigma_med=sigma, J_max=float(mx["J"]), J_median=medJ,
                  sharpness=float(mx["J"] / medJ) if medJ > 0 else None,
                  max_axis=mx["axis"], max_from=mx["from_"], max_to=mx["to"],
                  max_dM=float(mx["delta"]), J_max_X=float(max((e["J"] for e in edges if e["axis"] == "X"), default=0)),
                  J_max_Y=float(max((e["J"] for e in edges if e["axis"] == "Y"), default=0)))
    # Lead-style: fee axis only, raw delta / median level
    yedges = axis_edges(rows, key, "Y")
    lmx = max(yedges, key=lambda e: abs(e["delta"]))
    base = abs(st.median([r[key] for r in rows if r.get(key) is not None])) or 1e-9
    lead = dict(J_max_raw=float(lmx["delta"]), at=[lmx["from_"], lmx["to"]],
                sharpness_level_normalised=abs(lmx["delta"]) / base, median_level=float(
                    st.median([r[key] for r in rows if r.get(key) is not None])))
    return {"pre_registered": prereg, "lead_style": lead, "n_cells": len(rows)}


def equifinal(rows):
    """Lead's declared auditor thresholds: |d completion_lower| < 0.5pp and (|d liq|>25pp or |d tut_rate|>20pp)."""
    pairs = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a, b = rows[i], rows[j]
            if any(a.get(k) is None or b.get(k) is None for k in ("completion_lower", "liq_share", "tut_rate")):
                continue
            dc = abs(a["completion_lower"] - b["completion_lower"])
            dl = abs(a["liq_share"] - b["liq_share"])
            dt = abs(a["tut_rate"] - b["tut_rate"])
            if dc < 0.005 and (dl > 0.25 or dt > 0.20):
                pairs.append(dict(x_a=a["x_vac0"], y_a=a["fee_primary"], x_b=b["x_vac0"], y_b=b["fee_primary"],
                                  d_completion_lower_pp=round(100 * dc, 3), d_liq_pp=round(100 * dl, 2),
                                  d_tut_rate_pp=round(100 * dt, 2),
                                  d_tut_gap_pp=round(100 * abs((a["tut_q5_q1_gap"] or 0) - (b["tut_q5_q1_gap"] or 0)), 2),
                                  completion_a=round(a["completion_lower"], 4), completion_b=round(b["completion_lower"], 4),
                                  tut_a=round(a["tut_rate"], 4), tut_b=round(b["tut_rate"], 4)))
    pairs.sort(key=lambda p: -(p["d_liq_pp"] + p["d_tut_rate_pp"]))
    return pairs


def main():
    out = {"label": "SIMULATION ONLY - reconciliation of boundary statistics; no causal claims",
           "prereg": "PREREGISTRATION_PHASE_SWEEP.md (408aa3e) §4",
           "sources": {}, "equifinal": {}}
    for name, (path, gate) in SOURCES.items():
        rows = load(path, gate)
        rec = {"n_cells": len(rows), "seeds": rows[0].get("n_seeds"), "gate": gate}
        for k in METRICS:
            if sum(1 for r in rows if r.get(k) is not None) < 0.9 * len(rows):
                continue
            rec[k] = measures(rows, k)
        out["sources"][name] = rec
        eq = equifinal(rows)
        out["equifinal"][name] = {"n_pairs": len(eq), "pairs": eq}
    with open(os.path.join(OUT, "lead_reconciliation.json"), "w") as f:
        json.dump(out, f, indent=1)

    print("== pre-registered J (seed-SD normalised, both axes) vs Lead's level-normalised fee-axis number ==")
    for name, rec in out["sources"].items():
        print(f"\n{name}  ({rec['seeds']:.0f} seeds, {rec['n_cells']} cells)")
        for k in METRICS:
            if k not in rec:
                continue
            p, ld = rec[k]["pre_registered"], rec[k]["lead_style"]
            print(f"  {k:22s} pre: Jmax={p['J_max']:6.2f} (axis {p['max_axis']}, dM={p['max_dM']:+.3f}, "
                  f"sig={p['sigma_med']:.4f}) sharp={p['sharpness']:5.2f} | JmaxX={p['J_max_X']:5.2f} JmaxY={p['J_max_Y']:5.2f}"
                  f" || lead: Jmaxraw={ld['J_max_raw']:+.4f} sharp_level={ld['sharpness_level_normalised']:.3f}")
    print("\n== equifinal pairs (Lead's thresholds) ==")
    for name, e in out["equifinal"].items():
        print(f"  {name}: {e['n_pairs']} pairs")
    # cross-check the Lead's exact pairs appear in my 5-seed data too
    eq_mine = out["equifinal"]["bar_5seed_mine"]["pairs"], out["equifinal"]["quota_5seed_mine"]["pairs"]
    print("  top pair mine:", eq_mine[0][0] if eq_mine[0] else None)


if __name__ == "__main__":
    main()
