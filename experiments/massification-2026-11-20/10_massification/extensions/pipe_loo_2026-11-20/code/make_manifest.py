#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds RUN_MANIFEST.json and SHA256SUMS.txt for EXP-6 PIPE-LOO.

Read-only over the experiment directory: it only hashes files that already exist and then
writes the two manifest artifacts. The deterministic *result* hashes are compared between
results/ and results/determinism_run2/ and the comparison outcome is recorded, so the
determinism claim is verified by the manifest rather than asserted by it.

Usage: python code/make_manifest.py
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

EXPERIMENT = "EXP-6 PIPE-LOO"
WORKER = "PL"
DATE = "2026-11-20"
BRIEF = "Council brief 022 (D122 #1); SYNTHESIS_022.md section 6, EXP-6 PIPE-LOO, rank #1"

RESULT_FILES = ["PIPE_LOO_PAIRS.csv", "PIPE_LOO_RESULTS.csv", "PIPE_LOO_SECONDARY.csv", "console.txt"]

INPUTS = {
    "observed_series": "10_massification/data/UNIVERSALIZATION_SERIES.csv",
    "council_brief": "08_council/brief_022/SYNTHESIS_022.md",
}

# declared before the run in PRE_DECLARATIONS.md section 1/4
DECLARED_INPUT_SHA256 = {
    "observed_series": "85bc869396ebfcb39e3e1a21a31af219e75a07326c738a51d2bfdbe536737ddb",
    "council_brief": "9508dd55be8dd64da8322a8277c8342a4f50be6790a3d287e39e7004537c109b",
}


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p):
    return os.path.relpath(p, HERE)


def main():
    # ---- determinism check across the two run directories -----------------------------
    det = {}
    for name in RESULT_FILES:
        p1 = os.path.join(HERE, "results", name)
        p2 = os.path.join(HERE, "results", "determinism_run2", name)
        h1 = sha256_of(p1) if os.path.exists(p1) else None
        h2 = sha256_of(p2) if os.path.exists(p2) else None
        det[name] = {"run1_sha256": h1, "run2_sha256": h2,
                     "byte_identical": bool(h1 and h1 == h2)}
    all_identical = all(v["byte_identical"] for v in det.values())

    # ---- result gate: read the verdict back from the results CSV ----------------------
    import csv
    with open(os.path.join(HERE, "results", "PIPE_LOO_RESULTS.csv"), newline="",
              encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    overall = [r for r in rows if r["row_type"] == "OVERALL"][0]
    countries = [r for r in rows if r["row_type"] == "COUNTRY"]
    non_entrants = [r for r in rows if r["row_type"] == "NON-ENTRANT"]
    per_country = {r["iso3"]: dict(
        n_pairs=int(r["n_pairs"]),
        n_within_5pp=int(r["n_within_5pp"]),
        median_abs_loo_error_pp=float(r["median_abs_loo_error_pp"]),
        pct_within_5pp=float(r["pct_within_5pp"]),
        pass_=r["country_pass"],
        kappa_median_ratio=float(r["kappa_median_ratio"]),
    ) for r in countries}

    manifest = {
        "experiment": EXPERIMENT,
        "brief": BRIEF,
        "worker": WORKER,
        "date": DATE,
        "status": "COMPLETE",
        "label": "OBSERVED (completion series) + DERIVED (ratio, LOO prediction, error, median, share)",
        "statement": (
            "Measurement audit of an observed series. The lower->upper one-stage transition ratio is tested as a "
            "PREDICTIVE object (out-of-sample, leave-one-out, within country) and is NOT asserted to cause anything. "
            "No causal claim; no direction claim. D63 remains UNABLE as to cause. No C1-C4 reopening; EXP-1 is not "
            "re-scored (same pairing rule, different estimand). No threshold, bar, pairing rule or verdict string was "
            "changed after results; no re-fit; no second estimand. VERDICT: PREDICTIVE (3/4 countries pass)."
        ),
        "verdict": {
            "verdict": overall["verdict"],
            "n_countries_pass": int(overall["n_countries_pass"]),
            "n_countries_total": int(overall["n_countries_total"]),
            "rule": "per country PASS iff median|LOO error| <= 3.0 pp AND >=75% of pairs within +/-5 pp; "
                    "PREDICTIVE iff >=3/4 countries pass; NOT PREDICTIVE iff <=2/4",
            "n_pairs_total": int(overall["n_pairs"]),
            "branch_fired": "PREDICTIVE -> per-system kappa becomes a declared input (never fitted); "
                            "the ceiling question becomes 'what sets kappa?'; the D115 reclassification is NOT "
                            "downgraded. D63 stays UNABLE as to cause.",
            "per_country": per_country,
            "non_entrants": [r["iso3"] for r in non_entrants],
            "non_entrant_reason": "zero completion_lower_secondary / completion_upper_secondary rows in the frozen "
                                  "file; cannot enter; no proxy numerator (D118); never imputed",
        },
        "predeclaration": {
            "file": "PRE_DECLARATIONS.md",
            "sha256": sha256_of(os.path.join(HERE, "PRE_DECLARATIONS.md")),
            "recorded_sidecar": "PRE_DECLARATIONS.sha256",
            "sidecar_sha256": sha256_of(os.path.join(HERE, "PRE_DECLARATIONS.sha256")),
            "hashed_before_any_run": True,
            "thresholds_changed_after_results": False,
            "script_refuses_to_run_on_hash_mismatch": True,
            "verbatim_source": "08_council/brief_022/SYNTHESIS_022.md section 6 EXP-6, heading and items 1-7, "
                               "quoted character-for-character and verified line-by-line against the source",
        },
        "frozen_inputs_read_only": {},
        "declared_parameters": {
            "lag_years": 3,
            "tolerance_years": 1,
            "tie_break": "nearest lower year to t-3 within +/-1 y, ties toward the earlier year "
                         "(min over (|y-target|, y), the EXP-1 build_pairs convention)",
            "loo_estimator": "median of the country's other pairs' ratios; prediction = that median * the pair's own "
                             "lower value; kappa never fitted, never pooled across countries",
            "bar_median_abs_error_pp": 3.0,
            "bar_share_within_5pp": 0.75,
            "band_pp": 5.0,
            "countries_pass_needed": 3,
            "countries_total": 4,
            "countries": ["PHL", "KOR", "KHM", "CHN"],
            "declared_non_entrants": ["HKG", "JPN"],
            "rng": "none",
        },
        "results": {
            "files": {},
            "n_pairs_reported": int(overall["n_pairs"]),
            "all_pairs_reported": True,
            "brief_pre_freeze_calibration": {
                "PHL": "1.50 (7/8)", "KOR": "0.48 (17/19)", "KHM": "2.17 (10/11)", "CHN": "14.48 (0/5)",
            },
            "brief_calibration_reproduced": True,
            "brief_calibration_note": "all four medians reproduce to 2 dp and all four pair counts reproduce exactly; "
                                      "recorded as agreement about the construction, never used to choose a rule",
        },
        "determinism": {
            "two_runs_byte_identical": all_identical,
            "run1_dir": "results/",
            "run2_dir": "results/determinism_run2/",
            "per_file": det,
            "note": "no RNG, no clock-dependent output in any result file; the only non-deterministic field anywhere "
                    "is the build time of this manifest, which is not a result",
        },
        "declared_limits": [
            "43 pairs across 4 systems; 16 of 59 upper years dropped by the declared pairing rule",
            "verdict sits exactly at the declared boundary (3 of 4 required); no headroom",
            "HKG and JPN have zero completion pairs and cannot enter; no proxy numerator, no imputation",
            "KOR's pass is near an arithmetic identity at saturation (both series ~100%); PHL, KHM and CHN carry "
            "the informative content",
            "PHL's pass rests mainly on 2003-2017 pairs; the two late pairs (2023, 2024) are in band but upper 2022 "
            "is dropped by the rule",
            "completion-only measure (D118, one admissible numerator); no GER substitution",
            "realised lags run 2-4 years under the +/-1 y tolerance, so 'one-stage' is approximate per pair",
            "pooled (all-43) medians in the results CSV are DESCRIPTIVE only and carry no verdict",
        ],
        "closed_claims": [
            "no C1-C4 reopening",
            "does not re-score EXP-1 (out-of-sample prediction, not in-band share)",
            "no causal claim; no direction claim",
            "D63 remains UNABLE as to cause",
            "no re-fit, no re-parameterisation, no second estimand",
            "does not re-test or re-run CEIL-ATTRIB ablations, the generator, or any WT/DT cell",
        ],
        "writes_outside_experiment_dir": "none; all inputs opened read-only",
        "files": {},
    }

    for key, relpath in INPUTS.items():
        path = os.path.join(ROOT, relpath)
        got = sha256_of(path)
        manifest["frozen_inputs_read_only"][key] = {
            "path": relpath,
            "sha256": got,
            "declared_sha256": DECLARED_INPUT_SHA256[key],
            "matches_declared": got == DECLARED_INPUT_SHA256[key],
        }

    # ---- hash every file in the experiment directory (except the two manifest artifacts)
    files = []
    for dirpath, dirnames, filenames in os.walk(HERE):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for fn in sorted(filenames):
            if fn.startswith("."):
                continue
            files.append(os.path.join(dirpath, fn))
    files = sorted(set(files))
    skip = {os.path.join(HERE, "RUN_MANIFEST.json"), os.path.join(HERE, "SHA256SUMS.txt")}
    sums = []
    for p in files:
        if p in skip:
            continue
        h = sha256_of(p)
        sums.append((h, rel(p)))
        manifest["files"][rel(p)] = h
    manifest["results"]["files"] = {k: v for k, v in manifest["files"].items()
                                    if k.startswith("results/")}

    with open(os.path.join(HERE, "RUN_MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(os.path.join(HERE, "SHA256SUMS.txt"), "w", encoding="utf-8") as f:
        for h, name in sorted(sums, key=lambda t: t[1]):
            f.write(f"{h}  ./{name}\n")

    print(f"[manifest] RUN_MANIFEST.json  verdict={overall['verdict']} "
          f"({overall['n_countries_pass']}/{overall['n_countries_total']})  "
          f"n_pairs={overall['n_pairs']}  determinism_two_runs_identical={all_identical}")
    print(f"[manifest] SHA256SUMS.txt     {len(sums)} files hashed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
