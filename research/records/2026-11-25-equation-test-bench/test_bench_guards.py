#!/usr/bin/env python3
"""Guard tests for the rewritten data-level test bench (25 Nov 2026 audit fixes).

Pins the three v1 defects:
  1. F9 join used `lag=1` on a panel whose schooling series is ~5-yearly -> n = 0 and a verdict out of
     nothing. Now the lag comes from the data and an empty/insufficient join is NOT IDENTIFIED.
  2. `np.linalg.inv(X.T @ X)` raised `LinAlgError: Singular matrix` on a constant control. Now a rank
     guard drops collinear controls (never intercept/schooling) and records them.
  3. A design that stays rank-deficient is reported `not identifiable`, never as a number.

Run from this directory: python3 test_bench_guards.py   (numpy only, ~1 s)
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("tb_under_test", os.path.join(HERE, "test_bench2.py"))
tb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tb)


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)
    print("ok  -", msg)


def make_panel():
    """197-style synthetic panel: annual years, schooling only every 5 years, tfr from 1950."""
    panel = {}
    for i in range(30):
        iso = f"C{i:03d}"
        panel[iso] = {}
        for y in range(1950, 2011):
            panel[iso][y] = {"mean_years_schooling": (1.0 + 0.0008 * (y - 1950) ** 2 + 0.01 * i) if y % 5 == 0 else None,
                             "tfr_observed_1950plus": 6.0 - 0.04 * (y - 1950) + 0.01 * i + 0.3 * np.sin(y / 4.0),
                             "effective_fertility": 6.5 - 0.04 * (y - 1950) + 0.01 * i + 0.3 * np.sin(y / 4.0),
                             "urban_share_pct": 20.0 + 0.4 * (y - 1950) + i,
                             "gdp_pc_maddison_1990int": 1000.0 + 20.0 * (y - 1950) + 10.0 * i,
                             "child_mortality_per100": None}
    return panel


def unit_checks():
    panel = make_panel()
    lag = tb.native_lag(panel)
    check(lag == 5, f"native_lag: detects the 5-year schooling spacing (got {lag})")

    rows_lag5 = tb.build(panel, 5, controls=True)
    rows_lag1 = tb.build(panel, 1, controls=True)
    check(len(rows_lag5) > 200, f"build(lag=5): usable rows ({len(rows_lag5)})")
    check(len(rows_lag1) == 0,
          "build(lag=1): reproduces the v1 empty join (schooling is None in y-1) -> must not be used")

    # empty join must never produce a verdict, and the script must say why
    r_empty = tb.oos(rows_lag1, 2000)
    check(r_empty.get("ok") is False and "200" in r_empty.get("reason", ""),
          "oos: empty/insufficient join is not ok and says why")
    check(tb.decide(r_empty, 1.0, False, False) == "NOT IDENTIFIED",
          "decide: no verdict can be emitted from an empty join")

    # a constant control must be dropped, not crash the normal equations (v1: LinAlgError singular)
    rows_const = [(iso, y, dy, dx, [0.0]) for iso, y, dy, dx, cs in rows_lag5]
    fit = tb.ols_cluster(rows_const)
    check(fit.get("ok") is True, "ols_cluster: constant control no longer raises (rank guard)")
    check(fit.get("dropped_controls") == [0], f"ols_cluster: constant control dropped (got {fit.get('dropped_controls')})")

    # two perfectly collinear controls -> keep dropping until rank is full
    rows_dup = [(iso, y, dy, dx, [cs[0], cs[0]]) for iso, y, dy, dx, cs in rows_lag5]
    fit2 = tb.ols_cluster(rows_dup)
    check(fit2.get("ok") is True and len(fit2.get("dropped_controls", [])) >= 1,
          "ols_cluster: duplicate controls dropped, fit still identified")

    # an outcome with no variance is not identifiable
    rows_flat = [(iso, y, 0.0, dx, cs) for iso, y, dy, dx, cs in rows_lag5]
    fit3 = tb.ols_cluster(rows_flat)
    check(fit3.get("ok") is False and "variance" in fit3.get("reason", ""),
          "ols_cluster: zero-variance outcome is not identifiable")


def integration_check():
    """Run the real script on a CSV fixture, once with the data-native lag and once forced to lag=1."""
    tmp = tempfile.mkdtemp(prefix="tb_guards_")
    try:
        os.makedirs(os.path.join(tmp, "data"))
        panel = make_panel()
        cols = ["iso3", "year"] + list(tb.COLS)
        with open(os.path.join(tmp, "data", "long_run_panel.csv"), "w") as f:
            f.write(",".join(cols) + "\n")
            for iso, ys in panel.items():
                for y, v in sorted(ys.items()):
                    f.write(",".join([iso, str(y)] + ["" if v[c] is None else str(v[c]) for c in tb.COLS]) + "\n")
        shutil.copy(os.path.join(HERE, "test_bench2.py"), tmp)
        out = os.path.join(tmp, "results2.json")
        subprocess.run([sys.executable, "test_bench2.py", "--out", out, "--trials", "2"],
                       cwd=tmp, check=True, stdout=subprocess.DEVNULL)
        res = json.load(open(out))
        f9 = res["families"]["F9_fertility_lagged_OOS"]
        check(res["provenance"]["schooling_spacing_lag"] == 5,
              "script: derives lag 5 from the fixture, not 1")
        check(f9["n"] > 200 and f9["n_folds"] >= 3, f"script: F9 has a real join (n={f9['n']})")
        check(f9["verdict"] in ("SUPPORTED", "REJECTED (does not beat both benchmarks)",
                                "REJECTED (sign unstable across specifications)", "NOT IDENTIFIED"),
              f"script: F9 verdict is from the weak vocabulary ({f9['verdict']})")
        check(res["tierB"]["E8_PHL_gate"]["verdict"] == "UNTESTABLE",
              "script: PHL is explicitly UNTESTABLE when no series is supplied")
        check("panel_sha256" in res["provenance"], "script: writes provenance hash")
        # forced bad lag -> no crash, NOT IDENTIFIED
        out2 = os.path.join(tmp, "results_lag1.json")
        subprocess.run([sys.executable, "test_bench2.py", "--out", out2, "--lag", "1", "--trials", "1"],
                       cwd=tmp, check=True, stdout=subprocess.DEVNULL)
        res2 = json.load(open(out2))
        check(res2["families"]["F9_fertility_lagged_OOS"]["verdict"] == "NOT IDENTIFIED",
              "script: a forced empty join yields NOT IDENTIFIED and does not crash")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unit_checks()
    integration_check()
    print("\nALL PASS — lag/join/singular-control guards hold.")
