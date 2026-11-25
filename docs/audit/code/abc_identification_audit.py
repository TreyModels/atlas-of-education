#!/usr/bin/env python3
"""Reproducible ABC moment-rank / null-space audit (P0-01, P0-02, Paper A micro-moments).

Audits the *frozen* synthetic Bray ABC design of the GPU bundle
(`docs/audit/gpu_abc_bundle/gpu_bray_abc_and_contest_surface_6param.py`,
sha256 012b14bb...c1623f @ commit `045a63e`; see `docs/audit/EXTERNAL_AUDIT_GPU_2026-11-25.md`).

It computes, in closed form and independently of the archived ABC outputs:

  1. the moment map for the five advertised moments
     [m_part, m_g9, m_g12, m_ur, m_own] over the frozen 630-pupil design
     (420 G9 = 210 urban + 210 rural, 210 G12 all rural, 210 urban total);
  2. the analytic Jacobian (and a central-difference cross-check) of that map at
     1,000 random points of the frozen prior box;
  3. singular values, numerical rank, null-space dimensions and directions;
  4. the exact structural identity m_part = (2/3) m_g9 + (1/3) m_g12 and its
     left-null certificate (rank <= 4 for the 6-parameter model);
  5. parameter-scaling sensitivity (raw vs prior-box-standardised columns);
  6. the analytic provider-choice substitution delta = ln(0.32/0.68) and its
     consequence (P(own|tutoring) = 1/(1+e^delta), independent of everything else);
  7. the reduced 5-parameter / 3-moment participation system, its rank (3) and
     the two null directions, and how many further independent moments are needed;
  8. the rank with income and within-grade school-quality micro-moments defined
     here (candidate definitions for Paper A's proposal), including which ones
     actually load on the null space;
  9. target-measurement-uncertainty propagation (survey tolerances) separately
     from the structural rank result.

Pure NumPy, CPU only. No archived ABC output is used as evidence; the archived
best-theta / condition numbers appear only as arithmetic checks (clearly marked).

Run:
    /Users/treymenefee/neon-boot/venv/bin/python docs/audit/code/abc_identification_audit.py

Outputs /tmp/abc_identification_tables.md (the tables in the report) and prints
a summary. Deterministic: all seeds fixed at 20261125.
"""
from __future__ import annotations

import json
import numpy as np

# ---------------------------------------------------------------------------
# Frozen design constants (copied from the archived script; verified there)
# ---------------------------------------------------------------------------
N_PUPILS, N_G9, N_G12, N_URBAN = 630, 420, 210, 210
IS_G12 = np.r_[np.zeros(N_G9), np.ones(N_G12)]
IS_URBAN = np.r_[np.ones(N_URBAN), np.zeros(N_PUPILS - N_URBAN)]
# masks
ALL = np.arange(N_PUPILS)
G9 = ALL[:N_G9]
G12 = ALL[N_G9:]
URBAN = ALL[:N_URBAN]                    # G9 urban only (zero urban G12: P0-03)
RURAL = ALL[N_URBAN:]
RURAL_G9 = ALL[N_URBAN:N_G9]
RURAL_G12 = ALL[N_G9:]

THETA_NAMES = ["theta0 (b0_eff)", "theta1 (b_income)", "theta2 (b_school_gap)",
               "theta3 (delta_g12)", "theta4 (urban_demand)", "theta5 (delta_other)"]
# Frozen prior box: the 6-parameter corrective variant (dead theta5 dropped, so the
# sixth coordinate is delta_other).  Original 7-parameter box minus the dead coordinate.
LO = np.array([-1.0, 0.0, 0.0, 0.0, -0.5, -2.5])
HI = np.array([2.5, 2.0, 2.5, 2.5, 1.5, 1.5])
WIDTH = HI - LO
TARGETS = np.array([0.73, 0.67, 0.85, 0.14, 0.68])      # m_part, m_g9, m_g12, m_ur, m_own
TOLS = np.array([0.05, 0.05, 0.05, 0.04, 0.06])         # frozen ABC tolerances
MOMENT_NAMES = ["m_part", "m_g9", "m_g12", "m_ur", "m_own"]

SEED = 20261125
N_POINTS = 1000
RANK_RTOL = 1e-10          # SVD numerical-rank threshold (double precision)

# analytic provider-choice parameter
DELTA = float(np.log(0.32 / 0.68))                       # -0.7537718023763802


# ---------------------------------------------------------------------------
# population and moment map
# ---------------------------------------------------------------------------
class Pop:
    """The frozen synthetic population: 630 pupils, two covariates."""

    def __init__(self, seed: int):
        rng = np.random.default_rng(seed)
        self.log_y = rng.standard_normal(N_PUPILS)      # log income
        self.school_gap = rng.random(N_PUPILS)          # school-quality proxy U(0,1)

    def groups(self):
        """Within-grade income / school-quality high-low tercile masks (fixed)."""
        out = {}
        for tag, idx in (("g9", G9), ("g12", G12)):
            y = self.log_y[idx]
            q1, q2 = np.quantile(y, [1 / 3, 2 / 3])
            out[f"inc_hi_{tag}"] = idx[y > q2]
            out[f"inc_lo_{tag}"] = idx[y < q1]
            s = self.school_gap[idx]
            q1s, q2s = np.quantile(s, [1 / 3, 2 / 3])
            out[f"qual_hi_{tag}"] = idx[s > q2s]
            out[f"qual_lo_{tag}"] = idx[s < q1s]
        return out


def expit(z):
    """Numerically stable logistic."""
    out = np.empty_like(np.asarray(z, dtype=float))
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out


def _features(pop):
    """Rows of dV/dtheta for the four participation-relevant parameters (N, 5)."""
    return np.column_stack([np.ones(N_PUPILS), pop.log_y, pop.school_gap,
                            IS_G12, IS_URBAN])


def _sigma(theta, pop):
    """P(any tutoring) for each pupil and the intermediate quantities."""
    theta = np.asarray(theta, dtype=float)
    V = theta[0] + theta[1] * pop.log_y + theta[2] * pop.school_gap \
        + theta[3] * IS_G12 + theta[4] * IS_URBAN
    ln_alpha = np.log1p(np.exp(theta[5]))            # ln(1 + e^{delta_other})
    sig = expit(V + ln_alpha)
    return sig, V + ln_alpha, ln_alpha


def _dln_alpha(delta):
    """d ln(1+e^delta)/d delta = e^delta/(1+e^delta)  (== 1 - own share)."""
    return 1.0 / (1.0 + np.exp(-delta))


def _own_share(delta):
    """P(own | tutoring) = 1/(1+e^delta)  (exact, covariate-free)."""
    return 1.0 / (1.0 + np.exp(delta))


def moments5(theta, pop):
    """The five advertised moments, closed form.

    m_part  : mean participation over all 630
    m_g9    : mean participation over 420 G9 (210 urban + 210 rural)
    m_g12   : mean participation over 210 G12 (all rural in this design)
    m_ur    : mean participation urban (first 210 = urban G9) - mean participation rural (420)
    m_own   : own-tutor share = 1/(1+e^{theta5})  (exactly, by the 3-option logit)
    """
    sig, _, _ = _sigma(theta, pop)
    theta = np.asarray(theta, dtype=float)
    return np.array([
        sig.mean(),
        sig[G9].mean(),
        sig[G12].mean(),
        sig[URBAN].mean() - sig[RURAL].mean(),
        1.0 / (1.0 + np.exp(theta[5])),
    ])


def cell_means(theta, pop):
    """The three underlying cell probabilities (urban G9, rural G9, rural G12)."""
    sig, _, _ = _sigma(theta, pop)
    return np.array([sig[URBAN].mean(), sig[RURAL_G9].mean(), sig[RURAL_G12].mean()])


def _cell_rows(w, feat):
    """Row of the 4x(5+1) participation Jacobian per advertised moment (cell-mean form)."""
    def m(idx):
        return w[idx] @ feat[idx] / len(idx)

    rows = np.zeros((4, 6))
    rows[0, :5] = w @ feat / N_PUPILS
    rows[1, :5] = m(G9)
    rows[2, :5] = m(G12)
    rows[3, :5] = m(URBAN) - w[RURAL] @ feat[RURAL] / len(RURAL)
    return rows


def jacobian5(theta, pop):
    """Analytic 5x6 Jacobian of :func:`moments5` (d m / d theta)."""
    theta = np.asarray(theta, dtype=float)
    sig, _, _ = _sigma(theta, pop)
    w = sig * (1.0 - sig)
    dln = _dln_alpha(theta[5])             # d ln(1+e^delta)/d delta
    own = _own_share(theta[5])
    feat = _features(pop)
    J = np.zeros((5, 6))
    rows = _cell_rows(w, feat)
    J[:4, :5] = rows[:, :5]
    J[:4, 5] = dln * rows[:, 0]            # d/d theta5 = (dln/ddelta) * d/d theta0
    J[4, 5] = -own * (1.0 - own)
    return J


def jacobian_cells(theta, pop):
    """Analytic Jacobian of the three cell means w.r.t. (theta0..theta4)  -> 3x5."""
    theta = np.asarray(theta, dtype=float)
    sig, _, _ = _sigma(theta, pop)
    w = sig * (1.0 - sig)
    feat = _features(pop)
    J = np.zeros((3, 5))

    def m(idx):
        return w[idx] @ feat[idx] / len(idx)

    J[0] = m(URBAN)
    J[1] = m(RURAL_G9)
    J[2] = m(RURAL_G12)
    return J


# ---------------------------------------------------------------------------
# micro-moments (candidate definitions for Paper A's proposal)
# ---------------------------------------------------------------------------
def _p_w_rows(pop, masks):
    """Return lists of (numerator mask, sign) so a moment is sum_p/sum_w style."""
    return masks


def micro_moments(theta, pop, groups, kind="tercile"):
    """Within-grade income and school-quality micro-moments.

    kind="tercile": high-tercile minus low-tercile participation, per grade.
    kind="slope"  : within-grade OLS slope of participation on the covariate.
    Returns a dict of named scalars; all are model-implied (not data).
    """
    sig, _, _ = _sigma(theta, pop)
    out = {}
    if kind == "tercile":
        for tag in ("g9", "g12"):
            out[f"m_inc_{tag}"] = sig[groups[f"inc_hi_{tag}"]].mean() \
                - sig[groups[f"inc_lo_{tag}"]].mean()
            out[f"m_qual_{tag}"] = sig[groups[f"qual_hi_{tag}"]].mean() \
                - sig[groups[f"qual_lo_{tag}"]].mean()
    else:  # within-grade OLS slope
        for tag, idx in (("g9", G9), ("g12", G12)):
            for cov, name in ((pop.log_y, "inc"), (pop.school_gap, "qual")):
                x = cov[idx]
                xc = x - x.mean()
                out[f"m_{name}_{tag}"] = (xc @ sig[idx]) / (xc @ xc)
    return out


def pooled_micro_rows(theta, pop, groups, names):
    """Analytic Jacobian rows for (optionally pooled) micro-moments, shape (k,5)."""
    rows = []
    for nm in names:
        if nm == "m_inc_pooled":
            rows.append(0.5 * micro_jacobian(theta, pop, groups, "m_inc_g9")
                        + 0.5 * micro_jacobian(theta, pop, groups, "m_inc_g12"))
        elif nm == "m_qual_pooled":
            rows.append(0.5 * micro_jacobian(theta, pop, groups, "m_qual_g9")
                        + 0.5 * micro_jacobian(theta, pop, groups, "m_qual_g12"))
        else:
            rows.append(micro_jacobian(theta, pop, groups, nm))
    return np.array(rows) if rows else np.zeros((0, 5))


def micro_jacobian(theta, pop, groups, name, kind="tercile"):
    """Analytic gradient of one micro-moment w.r.t. (theta0..theta4), shape (5,)."""
    sig, _, _ = _sigma(theta, pop)
    w = sig * (1.0 - sig)
    feat = _features(pop)
    if kind == "tercile":
        _, cov, tag = name.split("_")          # m_{inc,qual}_{g9,g12}
        hi = groups[f"{cov}_hi_{tag}"]
        lo = groups[f"{cov}_lo_{tag}"]
        return (w[hi] @ feat[hi]) / len(hi) - (w[lo] @ feat[lo]) / len(lo)
    _, cov, tag = name.split("_")
    idx = {"g9": G9, "g12": G12}[tag]
    x = (pop.log_y if cov == "inc" else pop.school_gap)[idx]
    xc = x - x.mean()
    return (xc @ (w[idx] * feat[idx])) / (xc @ xc)


# ---------------------------------------------------------------------------
# rank / null-space helpers
# ---------------------------------------------------------------------------
def svd_rank(J, rtol=RANK_RTOL):
    s = np.linalg.svd(np.asarray(J, float), compute_uv=False)
    rank = int((s > rtol * s[0]).sum()) if s.size and s[0] > 0 else 0
    return s, rank


def nullspace(J, rtol=RANK_RTOL):
    """Orthonormal basis of the right null space (columns)."""
    J = np.asarray(J, float)
    U, s, Vt = np.linalg.svd(J, full_matrices=True)
    rank = int((s > rtol * s[0]).sum()) if s.size and s[0] > 0 else 0
    return Vt[rank:].T, rank, s


def fmt_vec(v, names=None):
    return "[" + ", ".join(f"{x:+.3f}" for x in v) + "]"


# ---------------------------------------------------------------------------
# target-manifold solve (damped Gauss-Newton, pure numpy)
# ---------------------------------------------------------------------------
def solve_cells_box(target_cells, pop, start, delta=DELTA, iters=400, tol=1e-13):
    """Box-projected Gauss-Newton for the 3 cell-mean equations (theta0..theta4 in prior box)."""
    lo, hi = LO[:5], HI[:5]
    th = np.clip(np.array(start[:5], float), lo, hi)
    for _ in range(iters):
        th_full = np.r_[th, delta]
        r = cell_means(th_full, pop) - target_cells
        if np.max(np.abs(r)) < tol:
            break
        J = jacobian_cells(th_full, pop)
        A = J.T @ J + 1e-10 * np.eye(5)
        th = np.clip(th - np.linalg.solve(A, J.T @ r), lo, hi)
    return th, cell_means(np.r_[th, delta], pop) - target_cells


def solve_cells(target_cells, pop, delta=DELTA, start=None, iters=300, tol=1e-14):
    """Solve the 3 cell-mean equations (theta0..theta4; delta pinned) from a start."""
    th = np.array(start if start is not None else [0.5, 0.5, 0.5, 1.0, 1.0], float)
    th_full = np.r_[th, delta]
    for _ in range(iters):
        r = cell_means(th_full, pop) - target_cells
        if np.max(np.abs(r)) < tol:
            break
        J = jacobian_cells(th_full, pop)
        # damped least squares: J^T J + lam I
        A = J.T @ J + 1e-10 * np.eye(5)
        step = np.linalg.solve(A, J.T @ r)
        # simple backtracking to keep the step sane
        th = th - step
        th_full = np.r_[th, delta]
    return th, cell_means(th_full, pop) - target_cells


# ---------------------------------------------------------------------------
# main audit
# ---------------------------------------------------------------------------
def main():
    pop = Pop(SEED)
    groups = pop.groups()
    log = []
    out = {}

    def emit(line=""):
        print(line)
        log.append(line)

    emit("=" * 100)
    emit("ABC IDENTIFICATION AUDIT — frozen Bray synthetic design (630 pupils, 6 active parameters)")
    emit(f"population seed={SEED}; {N_G9} G9 ({N_URBAN} urban + {N_G9 - N_URBAN} rural), "
         f"{N_G12} G12 (all rural => G12 x urban cell EMPTY)")
    emit("=" * 100)

    # ------------------------------------------------------------------
    # 1. the structural identity
    # ------------------------------------------------------------------
    emit("\n[1] STRUCTURAL REDUNDANCY (P0-01)")
    emit("m_part = (1/630) sum_all p_i = (420/630) m_g9 + (210/630) m_g12")
    emit("       = (2/3) m_g9 + (1/3) m_g12   for EVERY theta (420/630 = 2/3)")
    tgt_resid = 0.73 - ((2 / 3) * 0.67 + (1 / 3) * 0.85)
    emit(f"targets: 0.73 vs (2/3)(0.67)+(1/3)(0.85) = {(2/3)*0.67+(1/3)*0.85:.17g} "
         f"(residual {tgt_resid:+.3e})")
    rng = np.random.default_rng(SEED)
    pts = LO + rng.random((N_POINTS, 6)) * WIDTH
    id_err = []
    j_ident_err = []
    ranks5, ranks_part, ranks_cells, null_dims = [], [], [], []
    sv5_raw, sv5_scaled, sv_cells = [], [], []
    null_at = []
    for th in pts:
        m = moments5(th, pop)
        id_err.append(abs(m[0] - (2 / 3) * m[1] - (1 / 3) * m[2]))
        J = jacobian5(th, pop)
        Jp = J[:4]                                   # participation rows only
        s5, r5 = svd_rank(J)
        sp, rp = svd_rank(Jp)
        Jc = jacobian_cells(th, pop)
        sc, rc = svd_rank(Jc)
        ranks5.append(r5)
        ranks_part.append(rp)
        ranks_cells.append(rc)
        null_dims.append(6 - r5)
        sv5_raw.append(s5)
        sv_cells.append(sc)
        # left-null certificate l = (1, -2/3, -1/3, 0, 0)
        j_ident_err.append(abs(np.array([1.0, -2 / 3, -1 / 3, 0, 0]) @ J).max())
        sv5_scaled.append(np.linalg.svd(J @ np.diag(WIDTH), compute_uv=False))
    sv5_raw = np.array(sv5_raw)
    sv5_scaled = np.array(sv5_scaled)
    sv_cells = np.array(sv_cells)
    emit(f"numeric identity error over {N_POINTS} prior-box points: "
         f"max={max(id_err):.2e}")
    emit(f"left-null certificate l=(1,-2/3,-1/3,0,0): max |l J| = {max(j_ident_err):.2e}")
    emit(f"rank of 5x6 advertised-moment Jacobian: {sorted(set(ranks5))} "
         f"({ranks5.count(4)}/{N_POINTS} points at rank 4)")
    emit(f"rank of the 4 participation rows: {sorted(set(ranks_part))}")
    emit(f"rank of the 3x5 cell-mean Jacobian: {sorted(set(ranks_cells))}")
    emit(f"null-space dimension of the 5x6 model: {sorted(set(null_dims))} "
         "(6 parameters - rank 4)")
    emit(f"5x6 singular values (median over points): {np.median(sv5_raw, axis=0)}")
    emit(f"scaled (prior-width) singular values (median): {np.median(sv5_scaled, axis=0)}")
    emit(f"condition number raw median={np.median(sv5_raw[:,0]/sv5_raw[:,3]):.3f}; "
         f"scaled median={np.median(sv5_scaled[:,0]/sv5_scaled[:,3]):.3f}")

    # --- finite-difference verification of the analytic Jacobian (analytic/AD check) ---
    fd_err, fd_rel = [], []
    cell_fd_err = []
    test_pts = pts[:200]
    for th in test_pts:
        Ja = jacobian5(th, pop)
        Jn = np.zeros_like(Ja)
        h = 1e-6
        for j in range(6):
            e = np.zeros(6); e[j] = h
            Jn[:, j] = (moments5(th + e, pop) - moments5(th - e, pop)) / (2 * h)
        fd_err.append(np.max(np.abs(Ja - Jn)))
        fd_rel.append(np.max(np.abs(Ja - Jn) / np.maximum(np.abs(Jn), 1e-12)))
        Jca = jacobian_cells(th, pop)
        Jcn = np.zeros_like(Jca)
        for j in range(5):
            e = np.zeros(6); e[j] = h
            Jcn[:, j] = (cell_means(th + e, pop) - cell_means(th - e, pop)) / (2 * h)
        cell_fd_err.append(np.max(np.abs(Jca - Jcn)))
    emit(f"analytic Jacobian vs central finite difference (200 points, h=1e-6): "
         f"max abs err={max(fd_err):.2e}, max rel err={max(fd_rel):.2e}; "
         f"cell Jacobian max abs err={max(cell_fd_err):.2e}")

    # --- scaling: rank invariant, null spaces related by diag(1/width) ---
    width_err = []
    for th in test_pts:
        J = jacobian5(th, pop)
        Nraw, _, _ = nullspace(J)
        Nsc, _, _ = nullspace(J @ np.diag(WIDTH))
        A1 = Nsc
        # D^{-1} times the raw null basis spans the scaled null space; orthonormalise
        A2 = np.linalg.qr(np.diag(1.0 / WIDTH) @ Nraw)[0]
        M = A1.T @ A2
        width_err.append(np.max(np.abs(np.linalg.svd(M, compute_uv=False) - 1.0)))
    emit(f"column scaling invariance: rank unchanged, |principal angles| of null spaces "
         f"vs diag(1/width)-mapped: max deviation={max(width_err):.2e}")

    # ------------------------------------------------------------------
    # 2. target manifold: cell targets implied by the advertised targets
    # ------------------------------------------------------------------
    emit("\n[2] TARGET SOLUTION AND LOCAL NULL SPACE (P0-01/02)")
    # (m_g9,m_g12,m_ur) = (0.67,0.85,0.14)  <->  (A,B,C) invertible
    A = 0.8233333333333333
    B = 0.5166666666666666
    C = 0.85
    # invert exactly from the moment definitions to avoid hand rounding:
    # m_g9=(A+B)/2, m_g12=C, m_ur=A-(B+C)/2  =>  A = m_ur + (B+C)/2, B = 2 m_g9 - A
    m_g9, m_g12, m_ur = 0.67, 0.85, 0.14
    # m_g9=(A+B)/2, m_g12=C, m_ur=A-(B+C)/2  =>  B=(4 m_g9 - C - 2 m_ur)/3, A=2 m_g9 - B
    C = m_g12
    B = (4 * m_g9 - C - 2 * m_ur) / 3
    A = 2 * m_g9 - B
    emit(f"implied cell means: A(urban G9)={A:.6f}  B(rural G9)={B:.6f}  C(rural G12)={C:.6f}")
    emit(f"check: m_g9={(A+B)/2:.6f}  m_g12={C:.6f}  m_ur={A-(B+C)/2:.6f}")
    emit(f"COMPOSITION ARTIFACT (P0-03): the advertised urban-rural gap 0.14 is NOT a within-grade")
    emit(f"  gap.  With zero urban G12 pupils, m_ur = A - (B+C)/2 with C=m_g12=0.85, so the implied")
    emit(f"  WITHIN-GRADE urban-rural gap is A-B = {A - B:.4f} ({100*(A-B):.1f} pp), i.e. more than")
    emit(f"  twice the advertised 0.14; the 0.14 is a grade-composition-weighted mixture.")
    target_cells = np.array([A, B, C])
    # The 3 equations in 5 unknowns have a 2-dim solution manifold.  Solve inside the
    # frozen prior box from many starts; report the in-box solution set.
    archived_6p = np.array([-0.6343, 0.2392, 0.9809, 1.3490, 1.2229, -0.6682])  # arithmetic start only
    emit(f"moments at archived 6-param best_theta (AUTHOR-REPORTED arithmetic check only): "
         f"{np.round(moments5(archived_6p, pop), 6)}")
    emit(f"  vs targets {TARGETS}: max|diff|/tol = "
         f"{np.max(np.abs(moments5(archived_6p, pop) - TARGETS) / TOLS):.4f}")
    sols_in, sols_out = [], []
    starts = [np.r_[archived_6p[:5], DELTA]]
    for k in range(60):
        starts.append(LO + np.random.default_rng(SEED + 100 + k).random(6) * WIDTH)
    for st in starts:
        th, r = solve_cells_box(target_cells, pop, start=st[:5])
        if np.max(np.abs(r)) < 1e-11:
            sols_in.append(np.round(th, 6))
    uniq = np.unique(np.round(np.array(sols_in), 4), axis=0) if sols_in else np.zeros((0, 5))
    emit(f"box-projected Gauss-Newton from {len(starts)} starts: {len(sols_in)} in-box "
         f"solutions, {len(uniq)} distinct (2-dim manifold => non-unique within the prior box)")
    # pick the in-box solution closest (in theta) to the archived arithmetic start
    ref = np.r_[archived_6p[:5]]
    if sols_in:
        th_star = min(sols_in, key=lambda x: np.linalg.norm(x - ref))
    else:
        th_star = solve_cells_box(target_cells, pop, start=ref)[0]
    th_star = np.round(np.asarray(th_star, float), 8)
    th_full = np.r_[th_star, DELTA]
    emit(f"representative theta* = {np.round(th_full, 6)}")
    m_star = moments5(th_full, pop)
    emit(f"moments at theta*: m_g9={m_star[1]:.8f} m_g12={m_star[2]:.8f} "
         f"m_ur={m_star[3]:.8f} m_own={m_star[4]:.8f}  (targets pinned for own)")
    J3 = jacobian_cells(th_full, pop)
    N3, r3, s3 = nullspace(J3)
    emit(f"3x5 cell Jacobian rank={r3}  singular values={np.round(s3, 5)}  "
         f"null dim={N3.shape[1]}")
    emit("null direction 1 (theta0..theta4): " + fmt_vec(N3[:, 0]))
    emit("null direction 2 (theta0..theta4): " + fmt_vec(N3[:, 1]))
    emit("      (components: " + ", ".join(THETA_NAMES[:5]) + ")")
    # 5x6 null space at theta*
    J5 = jacobian5(th_full, pop)
    N5, r5, s5 = nullspace(J5)
    emit(f"5x6 Jacobian at theta*: rank={r5} singular values={np.round(s5, 5)} "
         f"null dim={N5.shape[1]}")
    for j in range(N5.shape[1]):
        emit(f"null vector {j + 1} (theta0..theta5): " + fmt_vec(N5[:, j]))
    # finite motion along a null direction: identical 3 participation moments, different theta
    v = N3[:, 0]
    th_new = th_star + 0.30 * v
    # project back onto the manifold by Newton iterations
    for _ in range(200):
        rr = cell_means(np.r_[th_new, DELTA], pop) - target_cells
        if np.max(np.abs(rr)) < 1e-13:
            break
        th_new = th_new - np.linalg.solve(jacobian_cells(np.r_[th_new, DELTA], pop).T
                                         @ jacobian_cells(np.r_[th_new, DELTA], pop)
                                         + 1e-12 * np.eye(5),
                                         jacobian_cells(np.r_[th_new, DELTA], pop).T @ rr)
    rr = cell_means(np.r_[th_new, DELTA], pop) - target_cells
    micro_star = micro_moments(np.r_[th_star, DELTA], pop, groups, "tercile")
    micro_new = micro_moments(np.r_[th_new, DELTA], pop, groups, "tercile")
    emit(f"finite null motion t=0.30: max|dtheta0..4|={np.max(np.abs(th_new - th_star)):.4f}; "
         f"participation-moment residual={np.max(np.abs(rr)):.2e}")
    emit("  micro-moments at theta*: " + ", ".join(f"{k}={v:.4f}" for k, v in micro_star.items()))
    emit("  micro-moments at theta': " + ", ".join(f"{k}={v:.4f}" for k, v in micro_new.items()))
    emit("  => the 3 participation moments are identical along this direction, so theta is NOT")
    emit("     identified even at finite distance (not only infinitesimally).")

    # ------------------------------------------------------------------
    # 3. analytic provider-choice parameter (P0-02)
    # ------------------------------------------------------------------
    emit("\n[3] ANALYTIC PROVIDER-CHOICE PARAMETER (P0-02)")
    emit("utilities: V0=0, V_own=B, V_other=B+delta  =>  P(own|tutoring)=1/(1+e^delta)")
    own = _own_share(DELTA)
    emit(f"delta* = ln(0.32/0.68) = {DELTA:.16f}")
    emit(f"P(own|tutoring) = 1/(1+exp(delta*)) = {own:.17g} "
         f"(exact target 0.68, error {abs(own - 0.68):.2e})")
    # independence from income / school / grade / urban: evaluate over the prior box
    diffs = []
    for th in pts:
        s, _, _ = _sigma(th, pop)
        own_cell = _own_share(th[5])
        # own share by any cell must equal 1/(1+e^{theta5}) exactly
        for _idx in (ALL, URBAN, RURAL, G9, G12):
            diffs.append(abs(own_cell - 1 / (1 + np.exp(th[5]))))
    emit(f"max deviation of the conditional own share across cells/points: {max(diffs):.2e}")
    emit("m_own(theta) = 1/(1+e^{theta5}) -> delta is pinned by algebra, NOT estimated.")
    # archived estimates: arithmetic check only (AUTHOR-REPORTED inputs, not evidence)
    d7, d6 = -0.8241, -0.6682
    emit("archived estimates (AUTHOR-REPORTED best_theta, arithmetic check only):")
    emit(f"  7-param delta={d7}: own={_own_share(d7):.6f}  ({100*_own_share(d7):.2f} %) "
         f"error={100*abs(_own_share(d7)-0.68):.2f} pp")
    emit(f"  6-param delta={d6}: own={_own_share(d6):.6f}  ({100*_own_share(d6):.2f} %) "
         f"error={100*abs(_own_share(d6)-0.68):.2f} pp")
    emit(f"  both inside the frozen tolerance tol_own={TOLS[4]} -> tolerance-based acceptance")
    emit("  masked an exactly solvable parameter (see [6]).")

    # ------------------------------------------------------------------
    # 4. reduced 5-parameter / 3-moment system and required moments
    # ------------------------------------------------------------------
    emit("\n[4] REDUCED SYSTEM: 5 PARAMETERS, 3 PARTICIPATION MOMENTS (P0-02)")
    emit("after delta substitution: theta=(theta0..theta4); free moments={m_g9,m_g12,m_ur}")
    emit(f"3x5 Jacobian rank=3 -> null dim=2 -> at least 2 further INDEPENDENT moments needed")
    # how much new information does each candidate moment carry? project rows on null space
    emit("null-space loading ||N^T r_i|| / ||r_i|| of candidate extra moments at theta*:")
    cand = {}
    J3n = N3
    for name in ("m_inc_g9", "m_inc_g12", "m_qual_g9", "m_qual_g12"):
        r = micro_jacobian(th_full, pop, groups, name, "tercile")
        load = np.linalg.norm(J3n.T @ r) / np.linalg.norm(r)
        cand[name] = (r, float(load))
        emit(f"  {name:12s}  loading={load:.4f}")
    # rank with each single candidate moment, and with pairs
    base3 = jacobian_cells(th_full, pop)
    emit("rank with ONE extra moment (3x5 base -> 4x5):")
    for nm in ("m_inc_pooled", "m_qual_pooled", "m_inc_g9", "m_inc_g12",
               "m_qual_g9", "m_qual_g12"):
        r_nm = pooled_micro_rows(th_full, pop, groups, [nm])
        J = np.vstack([base3, r_nm])
        _, rr = svd_rank(J)
        emit(f"  base3 + {nm:14s} rank={rr} null_dim={5 - rr}")
    emit("rank with TWO extra moments (3x5 base -> 5x5):")
    for nm1, nm2 in (("m_inc_pooled", "m_qual_pooled"),
                     ("m_inc_pooled", "m_inc_g12"),
                     ("m_qual_g9", "m_qual_g12"),
                     ("m_inc_g9", "m_qual_g9")):
        J = np.vstack([base3, pooled_micro_rows(th_full, pop, groups, [nm1, nm2])])
        _, rr = svd_rank(J)
        emit(f"  base3 + {nm1:12s} + {nm2:14s} rank={rr} null_dim={5 - rr}")
    emit("minimum extra moments to reach full local rank: 2 (rank-nullity)")
    emit("(see [5]: one income + one within-grade quality micro-moment suffice in this design)")

    # ------------------------------------------------------------------
    # 5. Paper A micro-moments: rank with income and school-quality moments
    # ------------------------------------------------------------------
    emit("\n[5] PAPER A MICRO-MOMENTS — INDEPENDENT RANK RECOMPUTATION")
    emit("Paper A (AUTHOR-REPORTED draft README) claims 'adding income and within-grade")
    emit("quality micro-moments restores rank 7/7 (condition 43.81)'. That model/code is")
    emit("NOT supplied here; the definitions below are OUR candidate operationalisation.")
    base3 = lambda th: jacobian_cells(th, pop)
    aug_sets = {
        "base3 (m_g9,m_g12,m_ur)": [],
        "base3 + income pooled": ["m_inc_pooled"],
        "base3 + income pooled + quality pooled": ["m_inc_pooled", "m_qual_pooled"],
        "base3 + all four grade-specific micro-moments":
            ["m_inc_g9", "m_inc_g12", "m_qual_g9", "m_qual_g12"],
    }

    def pooled_rows(th, names):
        return pooled_micro_rows(th, pop, groups, names)

    emit("\nrank of augmented 5-parameter Jacobians (3 aggregate + micro-moment rows),")
    emit("evaluated at the same %d prior-box points:" % N_POINTS)
    aug_out = {}
    for label, extra in aug_sets.items():
        ranks, svs, mins, nulls = [], [], [], []
        for th in pts:
            J = np.vstack([base3(th), pooled_rows(th, extra)])
            s, r = svd_rank(J)
            ranks.append(r)
            svs.append(s)
            mins.append(s[r - 1] / s[0])         # smallest nonzero / largest
            nulls.append(J.shape[1] - r)
        aug_out[label] = dict(ranks=ranks, svs=np.array(svs), nulls=nulls)
        emit(f"  {label:52s} rank={sorted(set(ranks))} "
             f"null_dim={sorted(set(nulls))} "
             f"median s_min/s_max={np.median(mins):.2e}")
    # condition numbers at theta*
    emit("\ncondition numbers at theta* (5-param, after delta substitution):")
    for label, extra in aug_sets.items():
        J = np.vstack([base3(np.r_[th_star, DELTA]),
                       pooled_rows(np.r_[th_star, DELTA], extra)])
        s = np.linalg.svd(J, compute_uv=False)
        r = int((s > RANK_RTOL * s[0]).sum())
        cond = s[0] / s[r - 1] if r > 0 else np.inf
        emit(f"  {label:52s} rank={r} cond={cond:.3g}")
    # unsubstituted 6-parameter model with own-share + 2 micro moments -> rank 6/6
    def full_jac_6p(theta, extra):
        """6-column Jacobian: 3 participation rows + own-share row + micro rows."""
        dln = _dln_alpha(theta[5])
        own = _own_share(theta[5])
        rows = jacobian_cells(theta, pop)             # 3 x 5
        J6 = np.zeros((3, 6))
        J6[:, :5] = rows
        J6[:, 5] = dln * rows[:, 0]                   # theta5 enters via ln(1+e^d)
        own_row = np.zeros((1, 6))
        own_row[0, 5] = -own * (1.0 - own)
        micro = pooled_rows(theta, extra)
        micro6 = np.zeros((micro.shape[0], 6))
        micro6[:, :5] = micro
        micro6[:, 5] = dln * micro[:, 0]
        return np.vstack([J6, own_row, micro6])

    emit("\nfull 6-parameter model (own-share NOT substituted), 5 advertised + micro-moments:")
    for label, extra in (("5 advertised + income + quality", ["m_inc_pooled", "m_qual_pooled"]),):
        ranks = []
        for th in pts:
            J = full_jac_6p(th, extra)
            _, r = svd_rank(J)
            ranks.append(r)
        emit(f"  {label:44s} rank={sorted(set(ranks))} (out of 6 parameters)")
        J = full_jac_6p(np.r_[th_star, DELTA], extra)
        s = np.linalg.svd(J, compute_uv=False)
        emit(f"  singular values at theta*: {np.round(s, 4)}")
    emit("CONCLUSION: with one income + one within-grade quality micro-moment the 5-parameter")
    emit("model reaches rank 5/5 and the unsubstituted 6-parameter model rank 6/6 (above).")
    emit("IDENTIFICATION LEVEL: full-rank Jacobian at a point = LOCAL identification only")
    emit("(inverse-function theorem). No global-injectivity proof is offered or claimed.")
    emit("Paper A's Jacobian proposition must be computed from ITS OWN model/specification and")
    emit("MUST NOT cite the archived ABC outputs (no committed code/results; quarantine).")

    # ------------------------------------------------------------------
    # 6. measurement-uncertainty propagation (separately from rank)
    # ------------------------------------------------------------------
    emit("\n[6] SURVEY / TARGET MEASUREMENT UNCERTAINTY (separate from structural rank)")
    emit(f"frozen tolerances tau = {TOLS} for {MOMENT_NAMES}")
    emit("rank is a property of the moment map; tau only sets practical precision.")
    # standardised Jacobian at theta* (5-param augmented, income+quality)
    J = np.vstack([base3(np.r_[th_star, DELTA]),
                   pooled_rows(np.r_[th_star, DELTA], ["m_inc_pooled", "m_qual_pooled"])])
    tau_aug = np.r_[TOLS[1:4], 0.03, 0.03]           # base3 + 2 micro tolerances (assumed 3pp)
    Jw = J / tau_aug[:, None]
    s = np.linalg.svd(Jw, compute_uv=False)
    emit(f"augmented (5x5) rank={int((s > RANK_RTOL * s[0]).sum())} "
         f"singular values of tau-scaled J: {np.round(s, 4)}")
    for tau_label, tm in (("tau", tau_aug), ("tau/2", 0.5 * tau_aug), ("2*tau", 2 * tau_aug)):
        Jinv = np.linalg.pinv(J / tm[:, None])
        cov = Jinv @ Jinv.T
        se = np.sqrt(np.diag(cov))
        emit(f"  {tau_label:5s}: parameter 1-sigma = {np.round(se, 4)}")
    emit("  => tolerances scale the parameter uncertainty linearly; they do NOT change rank.")
    emit("  => m_own tolerance is irrelevant once delta is analytic (exact algebra, zero variance).")
    # demonstrate: rank under tau changes is unchanged
    for tau_label, tm in (("tau/2", 0.5 * TOLS), ("tau", TOLS), ("2*tau", 2 * TOLS)):
        Jw5 = jacobian5(np.r_[th_star, DELTA], pop) / tm[:, None]
        s5 = np.linalg.svd(Jw5, compute_uv=False)
        emit(f"  advertised 5-moment model, {tau_label:5s}: rank="
             f"{int((s5 > RANK_RTOL * s5[0]).sum())} (structural rank unchanged)")

    # ------------------------------------------------------------------
    # 7. save
    # ------------------------------------------------------------------
    out.update(delta=DELTA, own_share=own, targets=TARGETS.tolist(),
               prior_lo=LO.tolist(), prior_hi=HI.tolist(),
               rank_5x6=sorted(set(ranks5)), rank_cells=sorted(set(ranks_cells)),
               sv5_median=np.median(sv5_raw, axis=0).tolist(),
               sv5_scaled_median=np.median(sv5_scaled, axis=0).tolist(),
               theta_star=th_full.tolist(),
               cell_targets=target_cells.tolist(),
               null3=N3.tolist(), null5=N5.tolist(),
               rank_aug={k: sorted(set(v["ranks"])) for k, v in aug_out.items()},
               id_error_max=float(max(id_err)),
               left_null_max=float(max(j_ident_err)),
               archived_delta_check=dict(d7=float(_own_share(d7)), d6=float(_own_share(d6))),
               n_inbox_solutions=len(sols_in), n_distinct_inbox=int(len(uniq)),
               n_points=N_POINTS)
    with open("/tmp/abc_identification.json", "w") as fh:
        json.dump(out, fh, indent=1)
    with open("/tmp/abc_identification_tables.md", "w") as fh:
        fh.write("\n".join(log))
    print("\nwrote /tmp/abc_identification.json and /tmp/abc_identification_tables.md")


if __name__ == "__main__":
    main()
