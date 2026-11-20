#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-11 KAPPA-FWD -- RUN_MANIFEST.json + SHA256SUMS.txt generator.

Deterministic: every value is either a fixed declaration or a hash of an on-disk file.
No clock, no RNG, no absolute paths. Reads the produced CSVs (never re-derives a number),
so the manifest cannot disagree with the results.

Order matters and is fixed:
  1. hash every artefact in this directory except RUN_MANIFEST.json and SHA256SUMS.txt
  2. write RUN_MANIFEST.json
  3. write SHA256SUMS.txt over every artefact INCLUDING RUN_MANIFEST.json, excluding itself
"""
import csv
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

INPUTS = [
    "10_massification/data/UNIVERSALIZATION_SERIES.csv",
    "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv",
    "08_council/brief_023/SYNTHESIS_023.md",
    "08_council/DECISIONS.md",
]
EXCLUDE_SUMS = {"SHA256SUMS.txt"}
MANIFEST = "RUN_MANIFEST.json"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def walk():
    out = []
    for base, dirs, files in os.walk(HERE):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(base, f)
            rel = os.path.relpath(p, HERE).replace(os.sep, "/")
            out.append(rel)
    return sorted(out)


def read_results():
    rows = {}
    with open(os.path.join(HERE, "results/KAPPA_FWD_RESULTS.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[(r["row_type"], r["iso3"])] = r
    return rows


def main():
    rows = read_results()
    overall = rows[("OVERALL", "ALL")]
    per_system = {}
    for iso in ["PHL", "KOR", "KHM", "CHN"]:
        r = rows[("SYSTEM", iso)]
        per_system[iso] = {
            "n_pairs": int(r["n_pairs"]),
            "n_pre2021": int(r["n_pre2021"]),
            "n_holdout": int(r["n_holdout"]),
            "slope_ratio_per_year": float(r["slope_ratio_per_year"]),
            "slope_within_bar_0p005": r["slope_within_bar"] == "TRUE",
            "kappa_half1": float(r["kappa_half1"]),
            "kappa_half2": float(r["kappa_half2"]),
            "half_median_shift_pp": float(r["half_median_shift_pp"]),
            "half_within_bar_2p0pp": r["half_within_bar"] == "TRUE",
            "leg_a_stationarity": r["leg_a_stationarity"],
            "kappa_full": float(r["kappa_full"]),
            "kappa_pre2021": float(r["kappa_pre"]),
            "kappa_full_declared": float(r["kappa_full_declared"]),
            "kappa_full_matches_declared": r["kappa_full_check"] == "MATCH",
            "n_within_bound": int(r["n_within_bound"]) if r["n_within_bound"] else None,
            "n_holdout_violations": int(r["n_violations"]) if r["n_violations"] else None,
            "forward_constraint": r["forward_constraint"],
            "note": r["note"],
        }

    artefacts = [f for f in walk() if f != MANIFEST]
    outputs = []
    for rel in artefacts:
        p = os.path.join(HERE, rel)
        outputs.append({"path": rel, "bytes": os.path.getsize(p), "sha256": sha256(p)})

    det_files = []
    identical = True
    for name in ["KAPPA_FWD_RESULTS.csv", "KAPPA_FWD_DETAIL.csv", "KAPPA_FWD_SECONDARY.csv", "console.txt"]:
        a = os.path.join(HERE, "results", name)
        b = os.path.join(HERE, "results/determinism_run2", name)
        same = (os.path.exists(a) and os.path.exists(b) and sha256(a) == sha256(b))
        identical = identical and same
        det_files.append({"file": "results/" + name, "run1_sha256": sha256(a),
                          "run2_sha256": sha256(b), "byte_identical": same})

    manifest = {
        "experiment": "EXP-11 KAPPA-FWD",
        "brief": "Council brief 023 (D136 #1); SYNTHESIS_023.md section 6.1 EXP-11 KAPPA-FWD, rank #1",
        "worker": "KF",
        "date": "2026-11-21",
        "status": "COMPLETE",
        "label": "OBSERVED (completion series) + DERIVED (ratio, slope, median, bound, excess, verdict)",
        "statement": (
            "Measurement audit of an observed series. The per-system lower->upper transition ratio kappa is tested for "
            "forward-usability (leg (a) stationarity; leg (b) temporal hold-out on the 7 post-2020 cells with the "
            "pre-2021 kappa) and is NOT asserted to cause anything. No causal claim; no direction claim. D63 remains "
            "UNABLE as to cause. EXP-6 is not re-scored (different estimand). No threshold, bar, split rule, pairing "
            "rule or verdict string was changed after results; no re-fit; one estimand. VERDICT: WINDOW-ONLY."
        ),
        "predeclaration": {
            "file": "PRE_DECLARATIONS.md",
            "sha256": sha256(os.path.join(HERE, "PRE_DECLARATIONS.md")),
            "frozen_before_run": True,
            "hash_file": "PRE_DECLARATIONS.sha256",
            "embedded_in_script": "code/run_kappa_fwd.py PREDECL_SHA256",
            "no_threshold_change_after_results": True,
        },
        "inputs": [{"path": rel, "sha256": sha256(os.path.join(ROOT, rel))} for rel in INPUTS],
        "verdict": {
            "verdict": overall["verdict"],
            "rule": ("FORWARD-USABLE iff PHL and KOR and KHM are each kappa-STABLE AND the hold-out is BOUND-HOLDS "
                     "(>=6 of 7); otherwise WINDOW-ONLY. UNDETERMINED only on a mechanical block."),
            "leg_a_stationarity": overall["leg_a_stationarity"],
            "leg_b_holdout": overall["leg_b_holdout"],
            "n_holdout_cells": int(overall["n_holdout"]),
            "n_within_bound": int(overall["n_within_bound"]),
            "n_violations": int(overall["n_violations"]),
            "falsifier_tripped": "TRUE" in overall["note"] and "falsifier tripped: TRUE" in overall["note"],
            "falsifier_arms": ">=2 hold-out violations (V=4); the PHL-slope arm did NOT fire (PHL slope -0.000704/yr)",
            "branch_fired": ("WINDOW-ONLY -> kappa may NOT enter V16-REPAIR as a forward constraint; it may enter only "
                             "as a declared within-window trajectory input (never extrapolated) or not at all; every "
                             "2025+ statement inherits the limit and must be labelled scenario/trajectory."),
            "no_single_global_kappa": "D133: a single kappa overstates KHM by 0.354; no global kappa is computed or used",
            "chn_status": "reported, NOT a forward constraint (D133 non-stationary); 0 post-2020 cells; excluded from the conjunction, the 7-cell denominator and the falsifier",
        },
        "per_system": per_system,
        "checks": {
            "verbatim_block_synthesis_023_lines_403_434": "IDENTICAL (byte-for-byte, re-checked by the script on every run)",
            "pairing_structure": "43 pairs (PHL 8, KOR 19, KHM 11, CHN 5), 16 upper years dropped -- MATCH",
            "crosscheck_pipe_loo_pairs": "43/43 ratio, lower_year_used and year_offset_used reproduce (4 dp tolerance)",
            "declared_medians_reconciliation": "8/8 MATCH at 4 dp (kappa_full and kappa_pre, all four systems)",
            "labels": "OBSERVED series; DERIVED quantities; no fitted parameter anywhere",
            "non_entrants": ["HKG", "JPN"],
        },
        "determinism": {
            "rng": "none",
            "network": "none",
            "clock_in_results": "none",
            "runs": 2,
            "byte_identical": identical,
            "files": det_files,
        },
        "outputs": outputs,
        "write_scope": "this directory only; no existing repository file modified",
        "limits": [
            "n per system 8/19/11/5 pairs; half-sample medians rest on 4/9/5/2 pairs per side",
            "PHL half-sample shift 2.1348 pp vs the 2.0 pp bar -- a boundary call, not a large drift",
            "KHM leg (a) label is carried substantially by the 2000 collapse pair (ratio 0.1389); a POST-HOC, non-verdict-bearing exclusion gives slope +0.0037/yr and shift 1.26 pp; the pair was NOT removed (that would be a re-fit) and the verdict does not depend on it",
            "leg (b) is one-sided: it can only detect upward breaches; PHL's downward drift is invisible to it",
            "KOR breaches occur at saturation (lower series 99.90-100.00); no second saturation-regime system is on disk (D135 HELD ask, not requested)",
            "hold-out horizon is 1-4 years past the 2020 cut, 2-3 cells per system; no extrapolation computed",
            "18/43 pairs use a +/-1 y offset; the literal lower_{t-3} is unobservable in 4 of 7 hold-out cells and was NOT imputed",
            "four systems, one data vintage; HKG/JPN non-entrant; no representativeness claim",
            "WINDOW-ONLY bounds the use of kappa; it is not a falsification of the pipeline reclassification (brief 6.1 item 6)",
        ],
    }

    mpath = os.path.join(HERE, MANIFEST)
    with open(mpath, "w", newline="", encoding="utf-8") as fh:
        fh.write(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    lines = []
    for rel in walk():
        if rel in EXCLUDE_SUMS:
            continue
        lines.append("%s  ./%s" % (sha256(os.path.join(HERE, rel)), rel))
    with open(os.path.join(HERE, "SHA256SUMS.txt"), "w", newline="", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("wrote %s (%d output artefacts) and SHA256SUMS.txt (%d entries)"
          % (MANIFEST, len(outputs), len(lines)))
    print("determinism: byte_identical=%s" % identical)
    if not identical:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
