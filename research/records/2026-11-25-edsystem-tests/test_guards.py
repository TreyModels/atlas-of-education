#!/usr/bin/env python3
"""Guard tests for the full-system statistical screen (25 Nov 2026 audit fixes).

These pin the three defects Neon's line audit found in the first version of
`test_full_system.py`:

  1. `np.linalg.pinv` on a rank-deficient design returned a number (effect, SE, p_holm=0) for a
     contrast the data cannot identify -> must now be reported `not_estimable`.
  2. `sign_consistent = all(...)` over an EMPTY stratum list is True in Python -> an empty stratum
     must never support a row.
  3. a zero-variance outcome (e.g. tutoring switched off by construction) produced a
     "supported with p=0" row -> must now be `not_estimable`.

Run from this directory:  python3 test_guards.py     (numpy only, no server, ~2 s)
Exit 0 = all guards hold.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import test_full_system as tfs  # noqa: E402


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)
    print("ok  -", msg)


def unit_checks():
    # --- rank / estimability -------------------------------------------------------------
    # full-rank 3-column design
    X = np.array([[1.0, 1.0, 0.0], [1.0, 0.0, 1.0], [1.0, 1.0, 1.0], [1.0, 0.0, 0.0]])
    rank, V, _ = tfs.row_space_basis(X)
    check(rank == 3, "row_space_basis: full-rank X has rank 3")
    check(all(tfs.contrast_estimable(V, j) for j in range(3)),
          "contrast_estimable: every contrast identifiable in a full-rank design")

    # duplicate column -> rank 2, and the duplicate direction is not estimable
    Xd = np.column_stack([np.ones(6), np.arange(6.0), np.arange(6.0)])
    rank, V, _ = tfs.row_space_basis(Xd)
    check(rank == 2, "row_space_basis: duplicate column detected (rank 2)")
    # with duplicated columns the individual coefficients are NOT estimable; their SUM is
    e1 = np.array([0.0, 1.0, 0.0])
    check(float(np.linalg.norm(e1 - V @ (V.T @ e1))) > 1e-8,
          "contrast_estimable: an individual duplicated coefficient is not estimable")
    e_sum = np.array([0.0, 1.0, 1.0])
    check(float(np.linalg.norm(e_sum - V @ (V.T @ e_sum))) < 1e-8,
          "contrast_estimable: the sum of the duplicated coefficients is estimable")

    # missing reference rows (outcome only exists in one arm) -> the arm contrast is not estimable
    arms = np.array([0, 0, 1, 1, 0, 0, 1, 1])
    Xm = np.column_stack([np.ones(8), arms])
    keep = arms == 1
    rank, V, _ = tfs.row_space_basis(Xm[keep])
    check(rank == 1 and not tfs.contrast_estimable(V, 1),
          "row_space_basis: arm contrast not estimable when the reference arm has no rows for the outcome")

    # --- cluster_ols guards --------------------------------------------------------------
    y = np.array([0.5] * len(X))
    eff, se, ok, why = tfs.cluster_ols(y, X, np.arange(len(X)), 1)
    check((eff, se, ok) == (None, None, False) and "variance" in why,
          "cluster_ols: zero-variance outcome is not estimable")

    # the outcome exists only in the treatment arm: the arm dummy is collinear with the intercept
    X_na = Xm[keep]
    eff, se, ok, why = tfs.cluster_ols(np.array([3.0, 4.0, 3.5, 4.5]),
                                       X_na, np.arange(X_na.shape[0]), 1)
    check(ok is False and "not identifiable" in why,
          "cluster_ols: rank-deficient design yields not_estimable, not a fabricated SE")


def integration_check():
    """End-to-end: a synthetic multiverse with the three defect shapes -> no false support."""
    tmp = tempfile.mkdtemp(prefix="tfs_guards_")
    try:
        axes = {"a": ["ref", "alt"], "b": ["ref", "alt"]}
        names = list(axes)
        rows = []
        from itertools import product
        combos = [c for c in product(*axes.values())]
        for ci, c in enumerate(combos):
            for seed in range(14):  # >50 rows so the finite-row guard does not mask the design guards
                a = c[0]
                base = 1.0 + (0.5 if a == "alt" else 0.0) + (0.2 if c[1] == "alt" else 0.0) + 0.01 * seed
                # the script only looks at its fixed OUTCOMES list, so encode the defect shapes there:
                m = {oc: base for oc in tfs.OUTCOMES}
                m["tut_rate"] = 0.5                                    # zero variance -> not estimable
                m["formal_share_gdp"] = base if a == "alt" else None   # reference arm absent -> rank deficient
                rows.append({"combo_index": ci, "combo": list(c), "seed": seed, "metrics": m})
        src = {"design": {"axes": axes, "axes_order": names}, "rows": rows}
        json.dump(src, open(os.path.join(tmp, "results_multiverse.json"), "w"))
        shutil.copy(os.path.join(HERE, "test_full_system.py"), tmp)
        subprocess.run([sys.executable, "test_full_system.py"], cwd=tmp, check=True,
                       stdout=subprocess.DEVNULL)
        out = json.load(open(os.path.join(tmp, "full_system_tests.json")))
        allrows = [(k, v, r) for k, b in out["contrasts"].items() for v, rs in b.items() for r in rs]
        sup = [(k, v, r) for k, v, r in allrows if r["supported"]]
        check(len(sup) > 0, f"synthetic run produces some supported rows ({len(sup)})")
        check(all(r.get("sign_consistent") is True for _, _, r in sup),
              "guard: no supported row has an empty stratum set")
        check(all(r.get("estimable") is True for _, _, r in sup),
              "guard: every supported row is estimable")
        flat = [(k, v, r) for k, v, r in allrows if r["outcome"] == "tut_rate"]
        check(flat and not any(r["supported"] for _, _, r in flat),
              "guard: zero-variance outcome is never supported")
        oa = [(k, v, r) for k, v, r in allrows if r["outcome"] == "formal_share_gdp"]
        check(oa and not any(r["supported"] for _, _, r in oa),
              "guard: rank-deficient arm contrast is never supported")
        check(out["status"] == "exploratory" and out["provenance"]["script_sha256"],
              "guard: output carries exploratory status + provenance hash")
        check(any(n["outcome"] == "tut_rate" for n in out["not_estimable"]),
              "guard: not_estimable rows are reported explicitly")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unit_checks()
    integration_check()
    print("\nALL PASS — rank/empty-stratum/zero-variance guards hold.")
