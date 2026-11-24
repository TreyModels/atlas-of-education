"""Model layer for the redesign: strength-separable worlds over the verified port kernel.

`theta_w(s) = theta_0 + s * Delta_w`, s in {0, 1}; s = 0 is the shared null control.
The kernel is the port's transcription (`port_backend/kernels_np_mlx.py`, vendored unmodified
from research/apple-silicon-gpu-2026-11-24 @ 52d74ec). Batch layout is pinned in `LAYOUT`.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "port_backend"))

import kernels_np_mlx as _K  # noqa: E402

BACKEND = os.environ.get("REDESIGN_BACKEND", "mlx")
N_HOUSEHOLDS = 10_000
YEARS = 25
THREADS = 256
BLOCKS = (N_HOUSEHOLDS + THREADS - 1) // THREADS
LAYOUT = {"N": N_HOUSEHOLDS, "years": YEARS, "threads": THREADS, "blocks": BLOCKS,
          "backend": BACKEND, "backend_note": "port MLX transcription; NumPy fallback available"}

# Amendment 1 (2026-11-24, committed before the confirmatory run): theta_0 is the equal-weighted
# centroid of the three shipped mechanism vectors, and the shipped deviation is scaled by K = 0.20
# (the shipped strengths put the DGP_SCHOOL_PUSH world outside schooling in the fees-only arm; see
# results/design_probe.json and PRE_REGISTRATION.md section 7).
K_STRENGTH = 0.20
SHIPPED = {
    "P": {"w_pov": 2.2, "w_push": 0.1, "w_tutor": 0.8, "div": 0.02},
    "S": {"w_pov": 0.2, "w_push": 2.0, "w_tutor": 0.8, "div": 0.05},
    "C": {"w_pov": 0.3, "w_push": 0.3, "w_tutor": 2.2, "div": 0.22},
}
THETA0 = {k: sum(SHIPPED[w][k] for w in SHIPPED) / 3.0 for k in SHIPPED["P"]}
DELTAS = {w: {k: K_STRENGTH * (SHIPPED[w][k] - THETA0[k]) for k in THETA0} for w in SHIPPED}
WORLDS = ("P", "S", "C")
FIXED = {"w_child": 0.55, "shadow_cost": 0.32, "q_pub0": 0.65, "cap_scale": 0.30,
         "h_hidden": 0.35, "psi": 0.45}
SHOCK_YEAR = 10


def theta_of(world, s):
    """theta_w(s); s=0 returns the common baseline for every world label."""
    if s == 0 or world is None:
        return dict(THETA0)
    return {k: THETA0[k] + s * DELTAS[world][k] for k in THETA0}


def make_inputs(seed, n, sigma_y, sigma_a, mu_y=0.0, mu_a=1.0):
    """Household inputs: lognormal income (median exp(mu_y)), clipped ability (mean mu_a)."""
    g = np.random.Generator(np.random.Philox(int(seed) & 0xFFFFFFFF))
    base_y = np.exp(g.normal(mu_y, sigma_y, size=n).astype(np.float32)).astype(np.float32)
    ability = np.clip(g.normal(mu_a, sigma_a, size=n).astype(np.float32),
                      np.float32(0.3), np.float32(1.8))
    return base_y, ability


def run_unit(world, s, seed, n=N_HOUSEHOLDS, years=YEARS, sigma_y=0.55, sigma_a=0.20,
             mu_y=0.0, mu_a=1.0, f_pub_pre=0.45, y_sub0=0.90, w_child=None, shadow_cost=None,
             q_pub0=None, ban=0.0, backend=None, keep_years=None):
    """Run one country/unit for `years` years under fee abolition at t=SHOCK_YEAR.

    Returns dict of arrays shaped (years, n) (or the `keep_years` slice).
    """
    backend = backend or BACKEND
    th = theta_of(world, s)
    w_child = FIXED["w_child"] if w_child is None else float(w_child)
    shadow_cost = FIXED["shadow_cost"] if shadow_cost is None else float(shadow_cost)
    q_pub0 = FIXED["q_pub0"] if q_pub0 is None else float(q_pub0)
    base_y, ability = make_inputs(seed, n, sigma_y, sigma_a, mu_y=mu_y, mu_a=mu_a)
    st = np.empty((years, n), dtype=np.int32)
    tut = np.empty((years, n), dtype=np.int8)
    lrn = np.empty((years, n), dtype=np.float32)
    wrk = np.empty((years, n), dtype=np.float32)
    yhh = np.empty((years, n), dtype=np.float32)
    q_pub = q_pub0
    seed_u = int(seed) & 0xFFFFFFFF
    for t in range(years):
        post = t >= SHOCK_YEAR
        f_pub = 0.0 if post else f_pub_pre
        y_sub = y_sub0 * (0.985 ** t)
        args = (
            np.int32(n), np.int32(t), np.uint32(seed_u), np.uint32(t + 17),
            np.float32(f_pub), np.float32(FIXED["h_hidden"]), np.float32(FIXED["psi"]),
            np.float32(ban), np.float32(q_pub), np.float32(th["div"]),
            np.float32(w_child), np.float32(y_sub), np.float32(shadow_cost),
            np.float32(th["w_pov"]), np.float32(th["w_push"]), np.float32(th["w_tutor"]),
            base_y, ability,
        )
        out = _K.run_sim_step_arrays(backend, args)
        st[t] = np.array(out["state"], dtype=np.int32)
        tut[t] = np.array(out["tutor"], dtype=np.int8)
        lrn[t] = np.array(out["learn"], dtype=np.float32)
        wrk[t] = np.array(out["work"], dtype=np.float32)
        yhh[t] = np.array(out["y_hh"], dtype=np.float32)
        enr = float(np.mean(st[t] <= 1))
        q_pub = float(np.clip(q_pub0 - (1.0 - FIXED["cap_scale"])
                              * max(0.0, enr - 0.55) * 0.45, 0.30, 0.80))
    res = {"state": st, "tutor": tut, "learn": lrn, "work": wrk, "y_hh": yhh}
    if keep_years is not None:
        res = {k: v[keep_years] for k, v in res.items()}
    return res


def year_stats(res):
    """Survey-like macro aggregates: GER and observed child employment (hidden excluded)."""
    s = res["state"]
    ger = (s <= 1).mean(axis=1)
    cl_obs = np.isin(s, (1, 2)).mean(axis=1)
    study_work = (s == 1).mean(axis=1)
    return {"ger": ger, "cl_observed": cl_obs, "study_work": study_work}


def moments(res, pre=(0, 10), post=(15, 25)):
    """Six-moment vector: pre/post GER, cl_observed, study_work."""
    ys = year_stats(res)
    a, b = pre
    c, d = post
    return np.array([
        ys["ger"][a:b].mean(), ys["cl_observed"][a:b].mean(), ys["study_work"][a:b].mean(),
        ys["ger"][c:d].mean(), ys["cl_observed"][c:d].mean(), ys["study_work"][c:d].mean(),
    ])
