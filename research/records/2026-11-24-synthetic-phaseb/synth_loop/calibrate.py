"""Moment-matching calibration (prereg §3.2).

M* is a rule, not a result: the theta_0 model at the default nuisance, averaged over the five
calibration seeds. Worlds at s=1 then search four nuisance parameters for a cell that matches M*
within +/-0.02 absolute on all six moments.
"""
import numpy as np

import model

M_STAR_SEEDS = [20261125 + 100 * k for k in range(5)]
# Phase A target moments (declared constants, anchored to WDI children-in-employment 31.4%
# for the 8 E8 countries; the model's aggregate is a share of children, not a labour rate).
M_STAR = np.array([0.60, 0.55, 0.27, 0.77, 0.47, 0.50])
DESIGN_NUIS = {"sigma_y": 0.55, "sigma_a": 0.20, "mu_y": 0.0, "mu_a": 1.0,
               "f_pub_pre": 0.15, "y_sub0": 0.85, "w_child": 0.15, "shadow_cost": 0.32}
CALIB_SEEDS = (20261125, 20261225)  # k = 0, 1
TOL = 0.10  # Phase A design tolerance (see PRE_REGISTRATION Amendment A1)
N_CANDIDATES = 300
SEARCH_RNG_SEED = 424242
RANGES = {  # Phase A nuisance (q_pub0 is a world parameter, not a nuisance)
    "sigma_y": (0.30, 0.90),
    "sigma_a": (0.10, 0.40),
    "mu_y": (-0.30, 0.40),
    "mu_a": (0.80, 1.45),
    "f_pub_pre": (0.00, 0.40),
    "y_sub0": (0.60, 1.20),
    "w_child": (0.02, 0.55),
    "shadow_cost": (0.10, 0.60),
}


def compute_m_star(seed_log):
    """M* is a fixed, declared target vector (not estimated); return it with provenance."""
    seed_log.append({"stage": "m_star", "rule": "declared constants", "value": M_STAR.tolist()})
    return M_STAR.copy(), M_STAR.reshape(1, -1)


def _candidates(rng, n):
    names = list(RANGES)
    out = []
    for _ in range(n):
        out.append({k: float(rng.uniform(*RANGES[k])) for k in names})
    return out


def calibrate(world, s, m_star, seed_log, n_candidates=N_CANDIDATES):
    """Random search; returns every evaluated cell so failures are preserved."""
    rng = np.random.default_rng(SEARCH_RNG_SEED)
    cands = _candidates(rng, n_candidates)
    rows = []
    for i, cand in enumerate(cands):
        mom = np.mean([model.moments(model.run_unit(world, s, seed, **cand))
                       for seed in CALIB_SEEDS], axis=0)
        resid = mom - m_star
        rows.append({"candidate_index": i, "nuisance": cand,
                     "moments": [float(x) for x in mom],
                     "residual": [float(x) for x in resid],
                     "max_abs_residual": float(np.max(np.abs(resid))),
                     "matched": bool(np.all(np.abs(resid) <= TOL))})
        if (i + 1) % 25 == 0:
            seed_log.append({"stage": "calibration", "world": world, "s": s,
                             "candidates_done": i + 1})
    matched = [r for r in rows if r["matched"]]
    chosen = min(matched, key=lambda r: (r["max_abs_residual"], r["candidate_index"])) \
        if matched else min(rows, key=lambda r: (r["max_abs_residual"], r["candidate_index"]))
    return {
        "world": world, "s": s, "n_candidates": n_candidates,
        "n_matched": len(matched), "matched": bool(matched),
        "chosen": chosen, "tolerance": TOL, "search_rng_seed": SEARCH_RNG_SEED,
        "calibration_seeds": list(CALIB_SEEDS),
        "table": rows if not matched else None,   # full table only on failure (keeps JSON small)
        "n_evaluated": len(rows),
    }
