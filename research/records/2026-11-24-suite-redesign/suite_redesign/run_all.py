"""Run the preregistered redesign: calibration -> H1 (macro wall) -> H4 (tie-breakers).

Outputs (all labelled SIMULATION):
  results/calibration.json   M*, per-world matched nuisance, residual table on failures
  results/h1_macro_wall.json country-decade FE slopes, bootstrap CIs, overlap, verdict
  results/h4_tiebreakers.json units, accuracies, placebos, Holm, verdict
  results/run_manifest.json  commit, backend, batch layout, seeds, wall time, environment
"""
import json
import os
import platform
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)
RESULTS = os.path.join(RECORD, "results")
sys.path.insert(0, HERE)

import calibrate  # noqa: E402
import macro  # noqa: E402
import model  # noqa: E402
import tiebreak  # noqa: E402


def git_head():
    try:
        return subprocess.run(["git", "-C", RECORD, "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        return None


def jsonable(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    return o


def main():
    os.makedirs(RESULTS, exist_ok=True)
    t0 = time.time()
    seed_log = []

    # ---- M* and calibration (written before any confirmatory profile) ----
    m_star, m_star_runs = calibrate.compute_m_star(seed_log)
    calib = {"m_star": [float(x) for x in m_star],
             "m_star_rule": "theta_0 model, default nuisance, mean over calibration seeds k=0..4",
             "m_star_seeds": calibrate.M_STAR_SEEDS,
             "m_star_runs": [list(map(float, r)) for r in m_star_runs],
             "default_nuisance": calibrate.DESIGN_NUIS,
             "tolerance": calibrate.TOL,
             "cells": {}}
    nuisances = {}
    for w in model.WORLDS:
        cell = calibrate.calibrate(w, 1, m_star, seed_log)
        calib["cells"][w] = cell
        nuisances[w] = cell["chosen"]["nuisance"]
    s0_cell = calibrate.calibrate(None, 0, m_star, seed_log)
    calib["cells"]["s0"] = s0_cell
    nuisances["s0"] = s0_cell["chosen"]["nuisance"]
    calib["all_worlds_matched"] = all(calib["cells"][w]["matched"] for w in model.WORLDS)
    calib["s0_matched"] = s0_cell["matched"]
    calib["label"] = "SIMULATION"
    with open(os.path.join(RESULTS, "calibration.json"), "w") as f:
        json.dump(jsonable(calib), f, indent=1)
    print(f"[calibrate] M* = {np.round(m_star, 4).tolist()}")
    for w in model.WORLDS:
        c = calib["cells"][w]
        print(f"[calibrate] {w}: matched={c['matched']} max|resid|={c['chosen']['max_abs_residual']:.4f} "
              f"nuisance={c['chosen']['nuisance']}")

    # ---- s=0 identity check (F1) ----
    ident = {"seeds": [], "max_abs_diff": 0.0}
    for k in (0, 1, 2, 3, 4):
        seed = tiebreak.SEED_K(k)
        res = [model.run_unit(w, 0, seed, **nuisances["s0"]) for w in model.WORLDS]
        diff = 0.0
        for a, b in ((0, 1), (0, 2)):
            for key in res[a]:
                diff = max(diff, float(np.max(np.abs(res[a][key].astype(np.float64)
                                                    - res[b][key].astype(np.float64)))))
        ident["seeds"].append({"k": k, "max_abs_diff": diff})
        ident["max_abs_diff"] = max(ident["max_abs_diff"], diff)
    ident["passed"] = bool(ident["max_abs_diff"] == 0.0)
    print(f"[identity] s=0 worlds identical: {ident['passed']} (max abs diff {ident['max_abs_diff']})")

    # ---- H1 ----
    h1 = macro.run_h1(seed_log)
    h1["identity_check"] = ident
    with open(os.path.join(RESULTS, "h1_macro_wall.json"), "w") as f:
        json.dump(jsonable(h1), f, indent=1)
    print("[H1] slopes:", {w: round(v["beta"], 4) for w, v in h1["slopes"].items()})
    print("[H1] joint interaction p =", round(h1["joint_interaction"]["p"], 4),
          "| overlaps:", {k: round(v, 3) for k, v in h1["pair_overlap"].items()})
    print("[H1] verdict:", h1["verdict"])

    # ---- H4 units ----
    calib_units = tiebreak.build_block(tiebreak.CAL_BLOCK, nuisances, s=1, seed_log=seed_log)
    heldout_units = tiebreak.build_block(tiebreak.HELDOUT_BLOCK, nuisances, s=1, seed_log=seed_log)
    repl_units = tiebreak.build_block(tiebreak.REPL_BLOCK, nuisances, s=1, seed_log=seed_log)

    def s0_block(block):
        out = []
        for k in block:
            seed = tiebreak.SEED_K(k)
            base = tiebreak.build_unit("P", 0, seed, nuisances["s0"])
            for label in model.WORLDS:
                u = dict(base)
                u["world"] = label
                out.append(u)
        return out

    s0_units = {"calibration": s0_block(tiebreak.CAL_BLOCK),
                "heldout": s0_block(tiebreak.HELDOUT_BLOCK)}

    h4 = tiebreak.run_h4(calib_units, heldout_units, repl_units, s0_units, nuisances, seed_log)
    h4["f2_matched"] = {w: calib["cells"][w]["matched"] for w in model.WORLDS}
    h4["macro_matching"] = {w: {"matched": calib["cells"][w]["matched"],
                                "max_abs_residual": calib["cells"][w]["chosen"]["max_abs_residual"],
                                "residual": calib["cells"][w]["chosen"]["residual"]}
                            for w in model.WORLDS}
    h4["macro_only_control_note"] = ("the macro-only control accuracy above measures residual macro "
                                     "separation after matching; if it is far above chance, the "
                                     "'conditional on matched macro moments' premise is only partially "
                                     "satisfied and is reported as a limitation")
    h4["identity_check"] = ident
    if not all(h4["f2_matched"].values()):
        h4["verdict_code"] = "cannot_test"
        h4["verdict"] = "cannot test (F2: a world could not be macro-matched)"
    with open(os.path.join(RESULTS, "h4_tiebreakers.json"), "w") as f:
        json.dump(jsonable(h4), f, indent=1)
    for key, r in h4["tiebreakers"].items():
        print(f"[H4] {key}: heldout acc={r['heldout']['accuracy']:.3f} "
              f"(n={r['heldout']['n_test']}), rep={r['replication']['accuracy']:.3f}, "
              f"holm p={r['holm_adjusted_p']:.4f}, rejected={r['admissibility']['rejected']}")
    print("[H4] placebos: s0 within band =", h4["placebos"]["s0_control"]["within_band"],
          "| algebraic pass =", h4["algebraic_equivalence_placebo"]["pass"],
          "| macro-only acc =", round(h4["placebos"]["macro_only_control_accuracy"], 3))
    print("[H4] verdict:", h4["verdict"])

    # ---- backend cross-check (port: NumPy and MLX kernel are bit-identical) ----
    mlx_check = {}
    try:
        import mlx.core  # noqa: F401
        for w in model.WORLDS:
            a = model.run_unit(w, 1, tiebreak.SEED_K(0), backend="numpy", **nuisances[w])
            b = model.run_unit(w, 1, tiebreak.SEED_K(0), backend="mlx", **nuisances[w])
            mlx_check[w] = {k: float(np.max(np.abs(a[k].astype(np.float64)
                                                 - b[k].astype(np.float64)))) for k in a}
        print("[backend] NumPy vs MLX max abs diff:", mlx_check)
    except Exception as exc:
        mlx_check = {"error": f"{type(exc).__name__}: {exc}"}

    # ---- manifest ----
    manifest = {
        "task": "task-8",
        "preregistration": "research/records/2026-11-24-suite-redesign/PRE_REGISTRATION.md",
        "commit": git_head(),
        "started_local": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "wall_s": None,
        "backend": model.BACKEND,
        "batch_layout": model.LAYOUT,
        "theta0": model.THETA0, "deltas": model.DELTAS,
        "seed_blocks": {"calibration": [tiebreak.SEED_K(0), tiebreak.SEED_K(19)],
                        "heldout": [tiebreak.SEED_K(20), tiebreak.SEED_K(79)],
                        "replication": [tiebreak.SEED_K(80), tiebreak.SEED_K(139)]},
        "h1_country_seeds": [macro.H1_SEED_BASE, macro.H1_SEED_BASE + 100 * (macro.N_COUNTRIES - 1)],
        "python": {"executable": sys.executable, "version": sys.version.split()[0],
                   "numpy": np.__version__},
        "platform": platform.platform(),
        "mechanism_scale_K": model.K_STRENGTH,
        "theta0": model.THETA0, "deltas": model.DELTAS,
        "backend_cross_check_numpy_vs_mlx": mlx_check,
        "label": "SIMULATION",
        "seed_log_entries": len(seed_log),
    }
    try:
        import mlx.core as mx
        manifest["python"]["mlx"] = mx.__version__
    except Exception:
        pass
    manifest["wall_s"] = round(time.time() - t0, 1)
    manifest["verdicts"] = {"H1": h1["verdict_code"], "H4": h4["verdict_code"]}
    with open(os.path.join(RESULTS, "run_manifest.json"), "w") as f:
        json.dump(jsonable(manifest), f, indent=1)
    print(f"[done] {manifest['wall_s']} s -> {RESULTS}")


if __name__ == "__main__":
    main()
