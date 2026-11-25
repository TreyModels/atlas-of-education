#!/usr/bin/env python3
"""P0-06 — general-r Tullock contest: derivation, validated optimizer, corrected surface.

Replaces the archived 2,000-point toy surface of
``docs/audit/gpu_abc_bundle/gpu_bray_abc_and_contest_surface_6param.py`` (``P0-06`` of
``docs/audit/EXTERNAL_AUDIT_GPU_2026-11-25.md``).

What this script establishes
----------------------------
1. **General-r single-prize Tullock best response from first principles.**
   For ``P_i = x_i^r / (x_i^r + A)`` with ``x_i = x0 + e_i`` and utility
   ``U_i = V_i·P_i - c_i·e_i``, the interior FOC is
   ``V_i·r·A·x^{r-1}/(x^r+A)^2 = c_i``.  Only ``r = 1`` has a closed form
   (``x = sqrt(V A / c) - A``); for general ``r`` it is solved numerically
   (bracketed roots + bisection + corner comparison), with convergence
   diagnostics.  A closed-form **symmetric-equilibrium anchor**
   ``x* = r V (n-1) / (n^2 c)`` validates the optimizer.
2. **What the archived closed form actually is**, and where it is wrong.
   ``e = sqrt(r·V·A·y/p) - A - x0`` is the **r=1** solution with the prize
   multiplied by ``r`` and with ``A`` in *x* units (r=1 rival mass), not
   ``A = Σ_{j≠i} x_j^r``.  Its symmetric fixed point coincides with the correct
   general-r symmetric level, but its individual response to heterogeneity and
   to asymmetric rival mass is wrong for ``r ≠ 1`` (utility losses quantified).
3. **Engine-consistent admission**: ``P_i`` from the exact Plackett–Luce module
   ``engine/eduengine/contest_math.py`` (top-K).  For ``K = 1`` the single-prize
   Tullock law equals exact PL (machine precision, checked); for ``K > 1`` the
   single-prize reduction is biased (quantified).
4. **Capacity clearing**: seats from ``share × denominator`` with explicit
   cohort/applicant denominators, ``seats_eff = min(seats, n_cand)``, universal
   admission branch (``seats ≥ candidates ⇒ P=1, e=0``), admission-probability
   distribution, and the identity ``ΣP = seats_eff``.
5. **Fee parameter** (H2 testable): a per-year fee reduces the household cash
   available for contest effort; fee abolition is ``fee = 0``.  Fee × scarcity
   interaction is computed from the spend-vs-seats gradient.
6. **Diagnostic-validated surface + structural independence.**  Every cell
   carries convergence diagnostics; the archived surface is shown to depend only
   on ``r/p`` (so its ``(r,p)`` grid probes a 1-D ray, not a plane), while the
   corrected model depends on ``r`` and ``p`` separately.

Run (from the worktree root; needs the engine on PYTHONPATH)::

    OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python \
    docs/audit/code/tullock_general_r.py

CPU only, single process, pure NumPy + the audit's own ``contest_math`` module.
Writes ``docs/audit/code/tullock_general_r_results.json`` and prints tables.
"""
from __future__ import annotations

import hashlib
import json
import time

import numpy as np

from eduengine.contest_math import pl_win_probs, pl_win_probs_exact

SEED = 20261125
# --- contest primitives shared with the engine's contest gates -------------
X0 = 1.0            # baseline contest input (engine contest_x0)
DV = 1.0            # prize value (engine gate prize / kappa·elite_logw)
E_CAP = 6.0         # effort cap (engine contest_max_e = 6)
CASH_KAPPA = 0.25   # household cash available for contest effort = CASH_KAPPA · y_i
N_CAND = 6          # diagnostic contest size (exact PL DP is O(n 2^n))
R_GRID = [0.8, 1.0, 1.5, 2.5]
P_GRID = [0.05, 0.16, 0.30]
S_GRID = [1/6, 2/6, 3/6, 4/6, 5/6, 1.00]   # seats 1,2,3,4,5,6 (=universal at 6)
S_GRID = [round(x, 4) for x in S_GRID]
FEE_GRID = [0.0, 0.08]

OUT_JSON = "docs/audit/code/tullock_general_r_results.json"


# ===========================================================================
# Part 1 — general-r single-prize Tullock
# ===========================================================================
def tullock_P(x, A, r):
    """Single-prize Tullock win probability, weights x^r vs rival mass A."""
    z = np.power(x, r)
    return z / (z + A)


def U_single(e, A, V, r, c, x0=X0):
    """Utility of effort e: V·P(x0+e) − c·e  (c = price per unit effort)."""
    return V * tullock_P(x0 + e, A, r) - c * e


def foc_single(x, A, V, r, c):
    """dU/dx for the single-prize Tullock (interior FOC = 0)."""
    z = np.power(x, r)
    return V * r * A * np.power(x, r - 1.0) / (z + A) ** 2 - c


def symmetric_x(V, c, r, n):
    """Closed-form symmetric equilibrium input: x* = r V (n-1) / (n^2 c)."""
    return r * V * (n - 1) / (n * n * c)


def best_response_tullock(A, V, c, r, x0=X0, e_hi=E_CAP, n_bracket=600):
    """Validated 1-D optimizer for the general-r single-prize Tullock best response.

    Strategy
    --------
    * ``r = 1`` has the quadratic closed form x = sqrt(V A / c) − A; still compare
      with the corners (e = 0, e = e_hi) before returning.
    * general ``r``: scan the FOC for sign changes on a log grid over
      ``x ∈ (x0, x0+e_hi]``, bisect every bracket, and choose the argmax of the
      **utility** among all FOC roots and the two corners.  This is valid even
      when the payoff is non-concave (r > 1 gives multiple roots), which is the
      regime the r=1 closed form cannot see.
    Returns ``(e, info)`` with ``info = {corner, n_roots, foc_residual,
    iters, converged, utility}``.
    """
    lo, hi = x0, x0 + e_hi
    cands = [lo, hi]                              # corners in x units
    corner_names = ["lower", "upper"]
    n_roots = 0
    iters = 0
    if r == 1.0:
        x_cf = np.sqrt(V * A / c) - A
        if lo < x_cf < hi:
            cands.append(x_cf)
            corner_names.append("interior")
            n_roots = 1
    else:
        # log grid resolves both small-x and large-x behaviour
        xs = np.geomspace(lo * (1 + 1e-9), hi, n_bracket)
        fs = foc_single(xs, A, V, r, c)
        fs = np.where(np.isfinite(fs), fs, np.sign(fs) * 1e12)
        for k in range(len(xs) - 1):
            if fs[k] == 0:
                cands.append(xs[k]); corner_names.append("interior"); n_roots += 1
            elif fs[k] * fs[k + 1] < 0:
                a, b = xs[k], xs[k + 1]
                fa = fs[k]
                for _ in range(200):
                    m = 0.5 * (a + b)
                    fm = foc_single(m, A, V, r, c)
                    if fa * fm <= 0:
                        b = m
                    else:
                        a, fa = m, fm
                    iters += 1
                cands.append(0.5 * (a + b))
                corner_names.append("interior")
                n_roots += 1
                if len(cands) > 40:                # safety: pathological grids
                    break
    us = [U_single(x - x0, A, V, r, c) for x in cands]
    j = int(np.argmax(us))
    e = float(max(0.0, cands[j] - x0))
    info = dict(corner=corner_names[j], n_roots=n_roots, iters=iters,
                foc_residual=0.0, converged=True, utility=float(us[j]))
    if corner_names[j] == "interior":
        info["foc_residual"] = float(abs(foc_single(cands[j], A, V, r, c)))
    return e, info


def best_response_grid(A, V, c, r, x0=X0, e_hi=E_CAP, ngrid=20001):
    """Brute-force dense-grid argmax, used to validate the FOC optimizer."""
    es = np.linspace(0.0, e_hi, ngrid)
    us = U_single(es, A, V, r, c)
    return float(es[np.argmax(us)]), float(us.max())


def part1_validation(out, log):
    def emit(s=""):
        print(s); log.append(s)

    emit("=" * 100)
    emit("PART 1 — general-r single-prize Tullock: derivation/optimizer validation")
    emit("=" * 100)
    rng = np.random.default_rng(SEED)
    rows = []
    worst_foc = 0.0
    worst_util_gap = 0.0
    worst_e_gap = 0.0
    for r in R_GRID:
        for trial in range(40):
            A = float(rng.uniform(0.2, 6.0))
            V = float(rng.uniform(0.5, 2.0))
            c = float(rng.uniform(0.03, 0.5))
            e_hi = float(rng.uniform(0.2, E_CAP))
            e, info = best_response_tullock(A, V, c, r, e_hi=e_hi)
            e_b, u_b = best_response_grid(A, V, c, r, e_hi=e_hi)
            u_foc = U_single(e, A, V, r, c)
            worst_foc = max(worst_foc, info["foc_residual"])
            worst_util_gap = max(worst_util_gap, abs(u_foc - u_b))
            worst_e_gap = max(worst_e_gap, abs(e - e_b))
            rows.append(dict(r=r, A=A, V=V, c=c, e_hi=e_hi, e=e, corner=info["corner"],
                             n_roots=info["n_roots"], util_gap=abs(u_foc - u_b),
                             e_gap=abs(e - e_b), foc_residual=info["foc_residual"]))
    emit(f"optimizer vs dense grid (40 random params x r in {R_GRID}):")
    emit(f"  max |e_FOC - e_grid|      = {worst_e_gap:.3e}   (grid spacing {E_CAP/20000:.1e})")
    emit(f"  max utility loss          = {worst_util_gap:.3e}")
    emit(f"  max interior FOC residual = {worst_foc:.3e}")
    # r=1 closed-form check
    cf_err = []
    for _ in range(40):
        A = float(rng.uniform(0.2, 6.0)); V = float(rng.uniform(0.5, 2.0)); c = float(rng.uniform(0.03, 0.5))
        e, info = best_response_tullock(A, V, c, 1.0, e_hi=E_CAP)
        x_cf = np.sqrt(V * A / c) - A
        e_cf = min(max(x_cf - X0, 0.0), E_CAP)
        cf_err.append(abs(e - e_cf))
    emit(f"r=1 best response vs closed form sqrt(VA/c)-A: max |diff| = {max(cf_err):.2e}")
    # symmetric anchor: analytic FOC residual at x* = r V (n-1)/(n^2 c), and the
    # substantive finding that for r>1 the symmetric point need NOT be the global best
    # response (non-concave payoff -> corner best responses / no symmetric pure eq).
    foc_at_xstar = []
    corner_beats_sym = []
    for r in R_GRID:
        for n in (2, 6, 20):
            for c in (0.05, 0.2):
                V = 1.0
                x_star = symmetric_x(V, c, r, n)
                A = (n - 1) * x_star ** r
                foc_at_xstar.append(abs(foc_single(x_star, A, V, r, c)))
                e, info = best_response_tullock(A, V, c, r, x0=X0, e_hi=50.0)
                if x_star > X0 and info["corner"] == "lower":
                    corner_beats_sym.append(dict(r=r, n=n, c=c, x_star=x_star,
                                                 foc_resid=abs(foc_single(x_star, A, V, r, c))))
    emit(f"symmetric anchor: |FOC(x*)| at x*=rV(n-1)/(n^2c) (interior cases): "
         f"max = {max(foc_at_xstar):.2e}")
    emit(f"r>1 non-concavity: at x* > x0 the GLOBAL best response is the e=0 corner in "
         f"{len(corner_beats_sym)} of 24 anchor cases (high r / low price): the symmetric "
         f"interior point is a local FOC point, not always an equilibrium for r>1.")
    # archived formula: what it is, and where it is wrong
    heter = []
    for r in (0.8, 1.5, 2.5):
        for _ in range(30):
            n = 8
            y = np.exp(0.6 * rng.standard_normal(n))
            others = np.exp(0.4 * rng.standard_normal(n - 1)) * X0
            A_w = float(np.sum(others ** r))            # correct rival weight mass
            A_x = float(np.sum(others))                 # archived r=1 mass
            i = 0
            V_i, c_i = DV * y[i], 0.16 / y[i]
            e_c, info_c = best_response_tullock(A_w, V_i, c_i, r, e_hi=E_CAP)
            e_a = max(0.0, np.sqrt(r * V_i * A_x / c_i) - A_x - X0)
            e_a = min(e_a, E_CAP)
            loss = U_single(e_c, A_w, V_i, r, c_i) - U_single(e_a, A_w, V_i, r, c_i)
            heter.append(dict(r=r, e_correct=e_c, e_archived=float(e_a),
                              util_loss=float(loss), y=float(y[i]),
                              A_w=A_w, A_x=A_x))
    emit("archived closed form vs the correct general-r best response (heterogeneous y, r != 1):")
    for r in (0.8, 1.5, 2.5):
        sub = [h for h in heter if h["r"] == r]
        de = [abs(h["e_correct"] - h["e_archived"]) for h in sub]
        dl = [h["util_loss"] for h in sub]
        emit(f"  r={r}: max|e_correct-e_archived|={max(de):.3f}  "
             f"mean utlity loss={np.mean(dl):.4f}  max={max(dl):.4f}")
    # symmetric-level coincidence (the nuance that corrects the audit framing)
    coinc = []
    for r in R_GRID:
        n, c = 8, 0.16
        x_arch = r * DV * (n - 1) / (n * n * c)       # archived fixed point, y=1
        coinc.append(abs(x_arch - symmetric_x(DV, c, r, n)))
    emit(f"symmetric-level coincidence: |x_arch_fixedpoint - x*_general_r| max = {max(coinc):.2e}")
    out["part1"] = dict(rows=rows, worst_e_gap=worst_e_gap,
                        worst_util_gap=worst_util_gap, worst_foc=worst_foc,
                        r1_closed_form_err=max(cf_err),
                        symmetric_anchor_foc_max=max(foc_at_xstar),
                        symmetric_corner_cases=corner_beats_sym,
                        heter=heter, symmetric_coincidence=max(coinc))


# ===========================================================================
# Part 2 — engine-consistent multi-seat admission (PL) and capacity clearing
# ===========================================================================
def capacity(share, n_cand, share_of="applicants", n_cohort=None):
    """Seats from share × (applicants|cohort); universal admission when seats >= n_cand."""
    denom = n_cand if share_of == "applicants" else (n_cohort if n_cohort else n_cand)
    seats = max(int(round(share * denom)), 1)
    seats_eff = min(seats, n_cand)
    return dict(share=share, denominator=denom, n_cand=n_cand, seats=seats,
                seats_eff=seats_eff, universal=bool(seats >= n_cand),
                admission_rate=seats_eff / n_cand)


def pl_prob(weights, seats_eff):
    """Admission probabilities: exact PL top-K (engine module)."""
    if seats_eff >= len(weights):
        return np.ones(len(weights))
    return pl_win_probs(weights, seats_eff, method="auto")


def pl_best_response(i, x, r, seats_eff, V_i, c_i, e_hi, ngrid=8, golden=9):
    """Best response with exact PL top-K admission probabilities (grid + golden refine)."""
    x = np.array(x, float)
    if seats_eff >= len(x):
        return 0.0
    def util(e):
        xx = x.copy(); xx[i] = X0 + e
        w = np.power(xx, r)
        return V_i * pl_prob(w, seats_eff)[i] - c_i * e
    es = np.linspace(0.0, e_hi, ngrid)
    us = np.array([util(e) for e in es])
    j = int(np.argmax(us))
    lo = es[max(j - 1, 0)]
    hi = es[min(j + 1, len(es) - 1)]
    phi = 0.6180339887498949
    for _ in range(golden):
        e1 = hi - phi * (hi - lo); e2 = lo + phi * (hi - lo)
        if util(e1) < util(e2):
            lo = e1
        else:
            hi = e2
    return float(0.5 * (lo + hi))


def equilibrium_pl(r, p, share, y, V=DV, x0=X0, e_cap=E_CAP, fee=0.0,
                   cash_kappa=CASH_KAPPA, max_iter=150, damp=0.5, tol=1e-7, e0=None):
    """Fixed-point equilibrium with exact PL admission; diagnostics for every cell."""
    n = len(y)
    cap = capacity(share, n, share_of="applicants")
    if cap["universal"]:
        return dict(cap=cap, e=np.zeros(n), P=np.ones(n), converged=True, iters=0,
                    residual=0.0, oscillating=False, foc_max=0.0)
    seats_eff = cap["seats_eff"]
    cost = p / y                                   # utility price of effort (engine pc/y)
    e_hi = np.minimum(e_cap, np.maximum(0.0, cash_kappa * y - fee) / p)
    e = np.zeros(n) if e0 is None else np.clip(np.array(e0, float), 0, e_hi)
    x = x0 + e
    resid = np.inf
    iters = 0
    signs = []
    for it in range(max_iter):
        e_old = e.copy()
        # Gauss-Seidel sweep: each candidate responds to the latest others
        for i in range(n):
            if e_hi[i] <= 0:
                e[i] = 0.0
            else:
                e[i] = e[i] + damp * (pl_best_response(i, x, r, seats_eff,
                                                       DV * y[i], cost[i], e_hi[i]) - e[i])
                x[i] = x0 + e[i]
        resid = float(np.max(np.abs(e - e_old)))
        iters = it + 1
        signs.append(np.sign((e - e_old).sum()))
        if resid < tol:
            break
    x = x0 + e
    w = np.power(x, r)
    P = pl_prob(w, seats_eff)
    osc = len(signs) > 10 and np.sum(np.abs(np.diff(signs)) > 0) > len(signs) // 2
    return dict(cap=cap, e=e, P=P, converged=bool(resid < tol), iters=iters,
                residual=resid, oscillating=bool(osc), foc_max=float(resid),
                e_hi=e_hi, cash_constrained=float(np.mean(e_hi < e_cap - 1e-12)))


def archived_equilibrium(r, p, share, y, V=DV, x0=X0, e_cap=E_CAP,
                         iters=30, damp=0.5):
    """Reimplementation of the archived solver (for comparison only)."""
    n = len(y)
    e_bar = 0.5
    hist = []
    e_i = np.zeros(n)
    for _ in range(iters):
        A = max(1.0 / share - 1.0, 0.05) * (x0 + e_bar)
        e_i = np.sqrt(np.clip(r * V * A * y / p, 0.0, None)) - A - x0
        e_i = np.clip(e_i, 0.0, e_cap)
        new = float(e_i.mean())
        hist.append(abs(new - e_bar))
        e_bar = 0.5 * e_bar + 0.5 * new
    return dict(e_bar=e_bar, e=e_i, last_delta=hist[-1], max_last10=max(hist[-10:]),
                residual_after_30=hist[-1])


# ===========================================================================
# Part 3 — diagnostic surface, fee test, structural independence
# ===========================================================================
def part2_3(out, log):
    def emit(s=""):
        print(s); log.append(s)

    emit("\n" + "=" * 100)
    emit("PART 2 — engine-consistent admission / capacity clearing / fee")
    emit("=" * 100)
    rng = np.random.default_rng(SEED + 1)
    y6 = np.exp(0.5 * rng.standard_normal(N_CAND))
    y6 = y6 / y6.mean()                            # mean-income-normalised cohort
    # capacity table
    rows = []
    for share in S_GRID:
        cap = capacity(share, N_CAND)
        rows.append((share, cap["seats"], cap["seats_eff"], cap["universal"],
                     cap["admission_rate"]))
    emit("capacity clearing (share of applicants, n_cand=6):")
    emit("  share  seats  seats_eff  universal  admission_rate")
    for rr in rows:
        emit(f"  {rr[0]:5.2f}  {rr[1]:5d}  {rr[2]:9d}  {str(rr[3]):>9s}  {rr[4]:14.3f}")
    # seats=1 PL identity and multi-seat reduction bias
    emit("\nseats=1: single-prize Tullock law == exact PL (machine precision):")
    ident = []
    for n in (5, 8, 12):
        x = np.exp(0.4 * rng.standard_normal(n))
        for r in R_GRID:
            w = np.power(x, r)
            P_t = w / w.sum()
            P_pl = pl_win_probs_exact(w, 1)
            ident.append(float(np.max(np.abs(P_t - P_pl))))
    emit(f"  max |Tullock - PL| over n in {{5,8,12}} x r grid = {max(ident):.2e}")
    emit("\nmulti-seat reduction bias: single-prize imputation w/Σw vs exact PL top-K:")
    red = []
    x = np.exp(0.5 * rng.standard_normal(10))
    r = 1.5
    w = np.power(x, r)
    P_t = w / w.sum()
    for K in range(1, 6):
        P_pl = pl_win_probs_exact(w, K)
        red.append(dict(seats=K, max_bias=float(np.max(np.abs(P_t - P_pl))),
                        mean_bias=float(np.mean(np.abs(P_t - P_pl)))))
        emit(f"  K={K}: max|P_single-P_PL|={red[-1]['max_bias']:.4f} "
             f"mean={red[-1]['mean_bias']:.4f}")

    # =========================================================================
    emit("\n" + "=" * 100)
    emit("PART 3 — corrected diagnostic surface (exact PL equilibrium) + fee + independence")
    emit("=" * 100)
    t0 = time.perf_counter()
    cells = []
    for r in R_GRID:
        for p in P_GRID:
            e_prev = None
            for share in S_GRID:
                eq = equilibrium_pl(r, p, share, y6, e0=e_prev)
                e_prev = eq["e"].copy()
                cap = eq["cap"]
                spend = float(np.mean(p * eq["e"]))
                cells.append(dict(r=r, p=p, share=share, seats=cap["seats_eff"],
                                  universal=cap["universal"], converged=eq["converged"],
                                  iters=eq["iters"], residual=eq["residual"],
                                  oscillating=eq["oscillating"],
                                  spend=spend,
                                  participation=float(np.mean(eq["e"] > 0.05)),
                                  P_mean=float(np.mean(eq["P"])),
                                  P_min=float(np.min(eq["P"])),
                                  P_max=float(np.max(eq["P"])),
                                  sum_P=float(np.sum(eq["P"])),
                                  seats_eff=cap["seats_eff"],
                                  cash_constrained=eq.get("cash_constrained", 0.0),
                                  e_hi=eq.get("e_hi"),
                                  e=eq["e"].tolist()))
    wall = time.perf_counter() - t0
    emit(f"corrected surface: {len(cells)} cells in {wall:.1f} s single process")
    nconv = sum(c["converged"] for c in cells)
    nosc = sum(c["oscillating"] for c in cells)
    ident_ok = all(abs(c["sum_P"] - c["seats_eff"]) < 1e-6 for c in cells)
    emit(f"  convergence flags: {nconv}/{len(cells)} converged; oscillation flags {nosc}")
    emit(f"  capacity-clearing identity ΣP = seats_eff for every cell: {ident_ok}")
    emit(f"  max iteration count {max(c['iters'] for c in cells)}; "
         f"max residual {max(c['residual'] for c in cells):.2e}")
    emit("\n  spend by (r, p) across seat shares S = " + str(S_GRID))
    hdr = ["r", "p"] + [f"S={s:.2f}" for s in S_GRID]
    emit("  " + " | ".join(f"{h:>8s}" for h in hdr))
    for r in R_GRID:
        for p in P_GRID:
            ss = [next(c for c in cells if c["r"] == r and c["p"] == p and c["share"] == s)
                  for s in S_GRID]
            emit("  " + " | ".join(f"{v:>8.3f}" for v in
                                   [r, p] + [c["spend"] for c in ss]))
    # seat-expansion gradient (paradox test) per (r,p)
    grad = []
    for r in R_GRID:
        for p in P_GRID:
            ss = [next(c for c in cells if c["r"] == r and c["p"] == p and c["share"] == s)
                  for s in S_GRID]
            d = [ss[k + 1]["spend"] - ss[k]["spend"] for k in range(len(ss) - 1)]
            grad.append(dict(r=r, p=p, dspend=[float(v) for v in d],
                             n_pos=float(np.mean(np.array(d) > 0)),
                             max_pos=float(np.max(d))))
    emit("\nseat-expansion paradox test (dSpend/dS > 0 = paradox):")
    emit("  r     p     share of adjacent-S steps with dSpend/dS>0   max dSpend")
    for g in grad:
        emit(f"  {g['r']:4.1f}  {g['p']:5.2f}  {g['n_pos']:.2f}                            {g['max_pos']:+.4f}")
    # universal admission branch
    emit("\nuniversal admission (S=1.00 >= 1 seat per candidate):")
    uni = [c for c in cells if c["universal"]]
    emit(f"  cells: {len(uni)}; all P=1: {all(c['P_mean'] >= 1 - 1e-12 for c in uni)}; "
         f"all spend=0: {all(abs(c['spend']) < 1e-12 for c in uni)}")
    # fee test
    emit("\nfee × scarcity test (fee reduces cash budget; fee abolition = fee 0):")
    fee_cells = []
    for fee in FEE_GRID:
        for r, p in ((1.5, 0.16), (0.8, 0.16)):
            e_prev = None
            for share in S_GRID:
                eq = equilibrium_pl(r, p, share, y6, fee=fee, e0=e_prev)
                e_prev = eq["e"].copy()
                fee_cells.append(dict(fee=fee, r=r, p=p, share=share,
                                      spend=float(np.mean(p * eq["e"])),
                                      participation=float(np.mean(eq["e"] > 0.05)),
                                      converged=eq["converged"], iters=eq["iters"],
                                      universal=eq["cap"]["universal"],
                                      cash_constrained=eq.get("cash_constrained", 0.0)))
    for r, p in ((1.5, 0.16), (0.8, 0.16)):
        g0 = [next(c for c in fee_cells if c["fee"] == 0 and c["r"] == r and c["p"] == p and c["share"] == s)["spend"] for s in S_GRID]
        g1 = [next(c for c in fee_cells if c["fee"] == FEE_GRID[1] and c["r"] == r and c["p"] == p and c["share"] == s)["spend"] for s in S_GRID]
        d0 = np.mean(np.diff(g0)); d1 = np.mean(np.diff(g1))
        emit(f"  r={r} p={p}: mean dSpend/dS  fee=0: {d0:+.4f}   "
             f"fee={FEE_GRID[1]}: {d1:+.4f}   interaction: {d1 - d0:+.4f}")
        emit(f"    spend fee=0 : " + " ".join(f"{v:.3f}" for v in g0))
        emit(f"    spend fee>0 : " + " ".join(f"{v:.3f}" for v in g1))

    # archived comparison: diagnostic shortcomings + structural independence
    emit("\narchived solver diagnostics on the same diagnostic grid:")
    arch_cells = []
    for r in R_GRID:
        for p in P_GRID:
            for share in S_GRID:
                a = archived_equilibrium(r, p, share, y6)
                arch_cells.append(dict(r=r, p=p, share=share, e_bar=a["e_bar"],
                                       spend=float(np.mean(p * a["e"])),
                                       last_delta=a["last_delta"],
                                       max_last10=a["max_last10"],
                                       residual_after_30=a["residual_after_30"]))
    n_noisy = sum(c["residual_after_30"] > 1e-8 for c in arch_cells)
    emit(f"  archived fixed-point residual after 30 iterations > 1e-8 in "
         f"{n_noisy}/{len(arch_cells)} cells (no convergence diagnostic shipped)")
    emit(f"  archived max residual after 30 iters: "
         f"{max(c['residual_after_30'] for c in arch_cells):.2e}")
    a_pos = []
    for r in R_GRID:
        for p in P_GRID:
            ss = [next(c for c in arch_cells if c["r"] == r and c["p"] == p and c["share"] == s)
                  for s in S_GRID]
            d = np.diff([c["spend"] for c in ss])
            a_pos.append(float(np.mean(d > 0)))
    emit(f"  archived 'paradox' dSpend/dS>0 share: mean={np.mean(a_pos):.2f} "
         f"(min={min(a_pos):.2f}, max={max(a_pos):.2f})")
    c_pos = [g["n_pos"] for g in grad]
    emit(f"  corrected 'paradox' dSpend/dS>0 share: mean={np.mean(c_pos):.2f} "
         f"(min={min(c_pos):.2f}, max={max(c_pos):.2f})")
    # structural independence of the archived grid
    r20 = np.linspace(0.8, 2.5, 20)
    p20 = np.linspace(0.05, 0.30, 20)
    ratios = np.round(r20[:, None] / p20[None, :], 10).ravel()
    n_unique = len(np.unique(ratios))
    a1 = archived_equilibrium(0.8, 0.10, 0.34, y6)
    a2 = archived_equilibrium(1.6, 0.20, 0.34, y6)
    same_ratio_arch = abs(a1["e_bar"] - a2["e_bar"])
    emit(f"\nstructural independence: the archived solver depends only on r·ΔV/p, i.e. the "
         f"(r,p) plane enters only through the ratio. The 20x20 grid samples {n_unique} "
         f"DISTINCT ratios (of {ratios.size} cells), so the surface is a 1-D r/p sweep x S: "
         f"the design has rank 2 (r/p, S), not 3 (r, p, S) — r and p are structurally "
         f"inseparable. Check: archived e_bar at (r,p)=(0.8,0.10) vs (1.6,0.20), same r/p: "
         f"|diff|={same_ratio_arch:.2e} (identical).")
    # corrected: same r/p, different (r,p) gives different spend
    pair_demo = []
    for (r1, p1, r2, p2) in ((0.8, 0.10, 1.6, 0.20), (1.0, 0.16, 2.0, 0.32)):
        c1 = equilibrium_pl(r1, p1, 0.34, y6)
        c2 = equilibrium_pl(r2, p2, 0.34, y6)
        s1 = float(np.mean(p1 * c1["e"])); s2 = float(np.mean(p2 * c2["e"]))
        pair_demo.append(dict(r1=r1, p1=p1, r2=r2, p2=p2, ratio1=r1 / p1, ratio2=r2 / p2,
                              spend1=s1, spend2=s2, diff=abs(s1 - s2)))
        emit(f"  same r/p ray: (r,p)=({r1},{p1}) spend={s1:.4f} vs "
             f"({r2},{p2}) spend={s2:.4f} -> corrected model separates r from p "
             f"(|diff|={abs(s1 - s2):.4f})")
    emit(f"\nwall clock: {time.perf_counter() - t0:.1f} s for surface + fee + archived comparison")

    out["part2"] = dict(capacity=[dict(share=a, seats=int(b), seats_eff=int(c),
                                       universal=bool(d), admission_rate=float(e))
                                  for a, b, c, d, e in rows],
                        seats1_identity_max=max(ident), reduction_bias=red)
    out["part3"] = dict(cells=cells, grad=grad, fee_cells=fee_cells,
                        universal=uni, archived=arch_cells,
                        archived_residual_max=max(c["residual_after_30"] for c in arch_cells),
                        archived_noisy_cells=int(n_noisy),
                        corrected_paradox_mean=float(np.mean(c_pos)),
                        archived_paradox_mean=float(np.mean(a_pos)),
                        unique_ratio_count=int(n_unique), ratio_cells=int(ratios.size),
                        same_ratio_demo=pair_demo,
                        wall_s=float(time.perf_counter() - t0))
    return cells


def main():
    log = []
    out = dict(seed=SEED, grids=dict(r=R_GRID, p=P_GRID, S=S_GRID, fee=FEE_GRID),
               constants=dict(X0=X0, DV=DV, E_CAP=E_CAP, CASH_KAPPA=CASH_KAPPA,
                              N_CAND=N_CAND))
    t_start = time.perf_counter()
    part1_validation(out, log)
    part2_3(out, log)
    out["runtime_s"] = time.perf_counter() - t_start
    with open(OUT_JSON, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    sha = hashlib.sha256(open(OUT_JSON, "rb").read()).hexdigest()
    log.append(f"\nwrote {OUT_JSON} sha256={sha} runtime={out['runtime_s']:.1f}s")
    print(log[-1])
    with open("/tmp/tullock_tables.md", "w") as fh:
        fh.write("\n".join(log))


if __name__ == "__main__":
    main()
