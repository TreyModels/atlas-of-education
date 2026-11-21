#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEBUG -- derive the CAP-01 fix table from the delivered and repaired panels.

LABEL: DEBUG. Reads (a) the delivered v1.3 / v1.2 panels (read-only) and (b) the repaired
copies produced by `run_repaired.py`, and writes every cell whose `completion_uis` moved,
with the delivered value, the declared uncapped identity `1.10 x completion_cohort`, the
repaired value, and the delta. Also re-checks A17 (0 binding cells) read-only.

No model run here, no RNG, no clock. Every number is an arithmetic read of two panels.

Usage:
  python uncap_cells.py --panels-dir results/panels --out results
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.dirname(CODE_DIR)
DEBUGDIR = os.path.dirname(FIXDIR)          # model_debug_2026-11-21
EXT = os.path.dirname(DEBUGDIR)             # extensions
MASS = os.path.dirname(EXT)                 # 10_massification
ROOT = os.path.dirname(MASS)                # experiments/massification-2026-11-20

SYNTH = "10_massification/extensions/synthetic_2026-11-20"
M_DECLARED = 1.10
LABEL = "DEBUG"

DELIVERED = {
    "v1.3": SYNTH + "/generator_v1_3/results/synthetic_panel_v1_3.csv",
    "v1.2": SYNTH + "/generator_v1_2/results/synthetic_panel_v1_2.csv",
    "A17": SYNTH + "/generator_v1_7_partrepair/results/panel_A17.csv",
}
REPAIRED = {
    "v1.3": "synthetic_panel_v1_3_repaired.csv",
    "v1.2": "synthetic_panel_v1_2_repaired.csv",
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return rows, list(rows[0].keys())


def f10(x):
    return float("%.10g" % x)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--panels-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)

    cells = []
    summary = {"label": LABEL, "declared_m": "%.2f" % M_DECLARED, "panels": {}}

    for panel, rel in DELIVERED.items():
        dpath = os.path.join(ROOT, rel)
        drows, dcols = read(dpath)
        entry = {
            "delivered_path": rel,
            "delivered_sha256": sha256_file(dpath),
            "n_rows": len(drows),
            "n_columns": len(dcols),
            "n_cells_where_uncapped_gt_1": 0,
            "n_cells_capped_at_1": 0,
            "max_uncapped": None,
            "max_delivered": None,
        }
        for r in drows:
            coh = float(r["completion_cohort"])
            uis = float(r["completion_uis"])
            unc = M_DECLARED * coh
            if unc > 1.0:
                entry["n_cells_where_uncapped_gt_1"] += 1
                entry["max_uncapped"] = unc if entry["max_uncapped"] is None else max(entry["max_uncapped"], unc)
            if uis == 1.0 and unc > 1.0:
                entry["n_cells_capped_at_1"] += 1
            entry["max_delivered"] = uis if entry["max_delivered"] is None else max(entry["max_delivered"], uis)

        if panel in REPAIRED:
            rpath = os.path.join(args.panels_dir, REPAIRED[panel])
            rrows, rcols = read(rpath)
            if dcols != rcols:
                sys.stderr.write("HEADER MISMATCH %s\n" % panel)
                raise SystemExit(2)
            if len(drows) != len(rrows):
                sys.stderr.write("ROW COUNT MISMATCH %s\n" % panel)
                raise SystemExit(2)
            changed_cols = set()
            max_repaired = None
            n_changed = 0
            for i, (ra, rb) in enumerate(zip(drows, rrows)):
                for c in dcols:
                    if ra[c] != rb[c]:
                        changed_cols.add(c)
                coh = float(ra["completion_cohort"])
                unc = M_DECLARED * coh
                before = float(ra["completion_uis"])
                after = float(rb["completion_uis"])
                max_repaired = after if max_repaired is None else max(max_repaired, after)
                if before != after:
                    n_changed += 1
                    # the repaired value must be the declared identity, one-sided floor
                    if abs(after - max(0.0, unc)) > 1e-9 * max(1.0, abs(unc)):
                        sys.stderr.write("IDENTITY FAIL %s row %d: repaired %r vs m*cohort %r\n"
                                         % (panel, i + 1, after, unc))
                        raise SystemExit(2)
                    ger = float(rb["ger"])
                    cr_pp = 100.0 * after
                    cr_over = cr_pp > ger + 1e-12
                    cells.append({
                        "panel": panel,
                        "cell_id": "%s|%s|%s" % (ra["country"], ra["level"], ra["year"]),
                        "country": ra["country"],
                        "level": ra["level"],
                        "year": ra["year"],
                        "panel_row_1based": i + 1,
                        "delivered_completion_uis": "%.10g" % before,
                        "completion_cohort": "%.10g" % coh,
                        "uncapped_m_x_completion_cohort": "%.10g" % unc,
                        "repaired_completion_uis": "%.10g" % after,
                        "delta_repaired_minus_delivered": "%.10g" % (after - before),
                        "was_capped_at_1": "TRUE" if before == 1.0 else "FALSE",
                        "exceeds_1_after": "TRUE" if after > 1.0 else "FALSE",
                        "ger_at_cell": "%.10g" % ger,
                        "cr_over_ger": "TRUE" if cr_over else "FALSE",
                        "cr_minus_ger_pp": "%.10g" % (cr_pp - ger),
                        "measure_verdict": (
                            "CR > GER: legitimate CR-above-GER case (older-cohort denominator)"
                            if cr_over else
                            "CR <= GER: not a CR-above-GER case; the repaired CR is BELOW the "
                            "model's own GER"),
                        "label": LABEL,
                    })
            # AMENDMENT 1 measure question on the WHOLE panel (not only the fixed cells)
            def n_cr_over_ger(rows_, key):
                n = 0
                for r_ in rows_:
                    if key in r_ and r_[key] not in ("", None):
                        if 100.0 * float(r_["completion_uis"]) > float(r_[key]) + 1e-12:
                            n += 1
                return n
            entry.update({
                "n_panel_cells_cr_over_ger_delivered": n_cr_over_ger(drows, "ger"),
                "n_panel_cells_cr_over_ger_repaired": n_cr_over_ger(rrows, "ger"),
                "repaired_file": REPAIRED[panel],
                "repaired_sha256": sha256_file(rpath),
                "columns_that_differ": sorted(changed_cols),
                "n_completion_uis_cells_changed": n_changed,
                "n_rows_where_uncapped_gt_1": entry["n_cells_where_uncapped_gt_1"],
                "max_repaired": max_repaired,
            })
        summary["panels"][panel] = entry

    out_csv = os.path.join(args.out, "CAP_FIX_CELLS.csv")
    cols = ["panel", "cell_id", "country", "level", "year", "panel_row_1based",
            "delivered_completion_uis", "completion_cohort", "uncapped_m_x_completion_cohort",
            "repaired_completion_uis", "delta_repaired_minus_delivered", "was_capped_at_1",
            "exceeds_1_after", "ger_at_cell", "cr_over_ger", "cr_minus_ger_pp",
            "measure_verdict", "label"]
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in cells:
            w.writerow({k: r[k] for k in cols})

    over = [r for r in cells if r["cr_over_ger"] == "TRUE"]
    summary["measure"] = {
        "question": "do the repaired capped cells have CR > GER? (AMENDMENT 1; audit section 5 item 4)",
        "n_fix_rows": len(cells),
        "n_cr_over_ger": len(over),
        "n_cr_le_ger": len(cells) - len(over),
        "ger_values_at_fixed_cells": sorted({r["ger_at_cell"] for r in cells}),
        "repaired_cr_pp_min": min(float(r["repaired_completion_uis"]) for r in cells) * 100.0,
        "repaired_cr_pp_max": max(float(r["repaired_completion_uis"]) for r in cells) * 100.0,
        "cr_minus_ger_pp_min": min(float(r["cr_minus_ger_pp"]) for r in cells),
        "cr_minus_ger_pp_max": max(float(r["cr_minus_ger_pp"]) for r in cells),
        "verdict": ("LEGITIMATE-CR-ABOVE-GER" if over else
                    "NOT-A-CR-ABOVE-GER-CASE: every repaired capped cell is CR <= the model's own GER"),
    }
    summary["n_fix_rows_total"] = len(cells)
    summary["n_fix_rows_by_panel"] = {
        p: sum(1 for r in cells if r["panel"] == p) for p in REPAIRED}
    summary["a17_binding_cells"] = summary["panels"]["A17"]["n_cells_capped_at_1"]
    with open(os.path.join(args.out, "CAP_FIX_SUMMARY.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print("[%s] CAP_FIX_CELLS.csv rows=%d  %s" % (
        LABEL, len(cells), {p: summary["n_fix_rows_by_panel"][p] for p in REPAIRED}))
    for p, e in summary["panels"].items():
        print("  %s: delivered_sha=%s capped_at_1=%d where_uncapped_gt_1=%d max_delivered=%s"
              % (p, e["delivered_sha256"][:12], e["n_cells_capped_at_1"],
                 e["n_cells_where_uncapped_gt_1"], e["max_delivered"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
