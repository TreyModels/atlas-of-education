"""Independent top-K Gumbel-max Plackett-Luce reference for the Atlas contest audit.

Binding interface: ``docs/audit/ENGINE_INTERFACE_CONTRACT.md`` §1.3 (contract v1.0 +
amendments A5/A6).  This module is the *one and only* expected-probability function
and the *one and only* contest realisation function for the repaired engine;
``core.py`` imports it, nothing else may re-implement Plackett-Luce.

Model
-----
``seats`` winners are the ``seats`` largest scores

    s_i = log(w_i) + G_i,   G_i ~ Gumbel(0, 1) = -log(-log(U_i)),   U_i ~ U(0,1),

the top-K set of a Plackett-Luce ranking with positive weights ``w_i``.  The engine
uses ``w_i = x_eff_i ** r`` (optionally times ``track_bonus``).  Ties have probability
zero for continuous ``U``; ``pl_realize`` is deterministic given the caller's ``u``.

Methods
-------
``method='exact'``
    Exact subset dynamic programme over selection sets, machine precision, ``O(n 2^n)``.
    Exact for all ``n <= EXACT_MAX_N = 20``; **raises ValueError** beyond the cap
    (amendment A6: never silently approximate).
``method='auto'``  (engine default, deterministic)
    Exact DP for ``n <= 20``; deterministic Poisson-binomial / exponential-race
    quadrature for larger ``n`` (no RNG, no Monte-Carlo noise — amendment A5).
    Probabilities are then renormalised to the hard invariant ``sum_i P_i = seats``.
``method='mc'``
    Validation only (never the engine decision path).  Requires a caller-supplied
    seeded generator; returns ``(p, se)`` with ``se = sqrt(p(1-p)/n_mc)``.

Deterministic large-n algorithm (``method='auto'``, ``n > 20``)
---------------------------------------------------------------
Condition on ``T_i = t``, with ``T_i = E_i / w_i`` (``E_i ~ Exp(1)``) the exponential
race that generates the same top-K set as the Gumbel-max rule.  The probability that
item ``i`` is in the top K is

    P_i = integral_0^inf  w_i exp(-w_i t) * G_i(t) dt,

where ``G_i(t) = P(at most K-1 of the other items have T_j < t)`` (equivalently
``G_i(t) = P(at least n-K of the others have T_j > t)``; the cheaper of the two
Poisson-binomial tails is used).  ``G_i(t)`` is computed for every item in
``O(n K)`` per node by prefix/suffix Poisson-binomial DPs (stable: no
leave-one-out division, so no cancellation when a p -> 1).  The integral is
evaluated with composite Simpson's rule in ``u = log t`` on
``t in [t_lo, C / w_min]`` with ``t_lo = 1e-5`` and ``C = 14``; the omitted mass is
bounded by ``max_i (w_i t_lo + exp(-C w_i / w_min)) <= ~1e-5`` plus the Simpson
error, so the total truncation error is ``<~2e-3`` for the contract grid
(measured against 400k-sample Monte Carlo: max ``|diff| <= 2e-3``).  Weights are
normalised by their maximum first (scale invariance), the DP is kept to
``O(n * min(K, n-K) * nodes)`` time, and ``sum_i P_i`` is renormalised to ``seats``.

Design rules
------------
* Pure NumPy.  **No imports from ``eduengine``** — independence is the point.
* Log-space where sensible; no NaN/inf for finite positive weights.
* ``pl_realize`` is O(n) selection (``np.argpartition``) plus O(k log k) to order the
  chosen block — fast for n up to a few thousand.

Exact method
------------
Let ``g(S)`` be the probability that the *set* of the first ``|S|`` selected items is
exactly ``S``.  Then ``g(empty)=1`` and

    g(S) = sum_{i in S} g(S \\ {i}) * w_i / sum_{j not in S \\ {i}} w_j .

The denominator is a sum of positive terms only (computed directly by a subset-sum
DP, no cancellation), so the recursion is numerically stable; ``P(i in top-K)`` is
the sum of ``g(S)`` over size-K sets ``S`` containing ``i``.
"""

from __future__ import annotations

import time

import numpy as np

__all__ = [
    "pl_log_weights",
    "pl_win_probs",
    "pl_win_probs_detail",
    "pl_win_probs_exact",
    "pl_win_probs_mc",
    "pl_stats",
    "pl_realize",
    "AUTO_EXACT_N",
    "EXACT_MAX_N",
]

#: ``method="exact"`` (and ``"auto"``) use the exact subset DP at or below this n.
#: Contract: exact to machine precision for n <= 12; the DP is genuinely exact to 20.
EXACT_MAX_N = 20
#: ``method="auto"`` uses the exact DP at or below this n, quadrature above.
AUTO_EXACT_N = EXACT_MAX_N

#: Uniform draws are clipped to this distance from {0,1} so Gumbel(u) stays finite.
_U_CLIP = 1e-12
#: Element cap for one Monte-Carlo chunk (memory bound, ~16 MB).
_MC_CHUNK_ELEMS = 2_000_000

# ---- deterministic quadrature constants (documented, fixed: no tuning at runtime) ----
_QUAD_H = 0.1              # Simpson step in u = log t
_QUAD_T_LO = 1e-5          # lower truncation: omitted mass <= w_max * t_lo = 1e-5
_QUAD_TAIL_C = 14.0        # t_hi = C / w_min: omitted mass <= exp(-C) ~ 8e-7
_QUAD_MAX_NODES = 1600     # hard cap; h is coarsened beyond it (documented)
#: Bounded caches (task-12).  Both are *pure* memoisation of deterministically
#: computed arrays, keyed by exact float bytes, so they cannot change results.
_STATS = {"grid_hit": 0, "grid_miss": 0, "result_hit": 0, "result_miss": 0}
_GRID_CACHE = {}           # w_min (float) -> (t, sw, m)
_GRID_CACHE_MAX = 64
_RESULT_CACHE = {}         # (method, seats, w.tobytes()) -> p
_RESULT_CACHE_MAX = 64
_BATCH_TARGET_BYTES = 64_000_000
_QUAD_W_FLOOR = 1e-30      # weights below floor*max are "never win" (P < ~1e-28)
_QUAD_EST_ERR = 2e-3       # documented conservative truncation+Simpson bound
_EXACT_EST_ERR = 1e-13     # documented floating-point bound for the subset DP


# ---------------------------------------------------------------------------
# validation helpers
# ---------------------------------------------------------------------------
def _as_weights(weights):
    """Validate and return weights as a 1-D float64 array."""
    w = np.asarray(weights, dtype=np.float64)
    if w.ndim == 0:
        w = w.reshape(1)
    if w.ndim != 1:
        raise ValueError("weights must be one-dimensional")
    if w.size and not np.all(np.isfinite(w)):
        raise ValueError("weights must be finite")
    if np.any(w <= 0.0):
        raise ValueError("weights must be strictly positive")
    return w


def _as_seats(seats, n):
    """Validate and return ``seats`` as a Python int clamped to ``[0, n]``."""
    try:
        s = int(seats)
    except (TypeError, ValueError):
        raise TypeError("seats must be an integer")
    if s != seats:
        raise ValueError("seats must be a whole number")
    return 0 if s < 0 else (n if s > n else s)


def _check_method(method, allowed):
    if method not in allowed:
        raise ValueError(f"method must be one of {sorted(allowed)}; got {method!r}")


def pl_log_weights(weights):
    """Natural log of positive contest weights, computed defensively.

    Parameters
    ----------
    weights : array_like
        Strictly positive weights ``w_i > 0`` (the engine's ``x_eff ** r``,
        optionally times ``track_bonus``).  Any finite positive scale is accepted.

    Returns
    -------
    numpy.ndarray
        ``log(w)`` as float64, shape ``(n,)``.

    Raises
    ------
    ValueError
        If any weight is non-finite or non-positive.
    """
    w = _as_weights(weights)
    if w.size == 0:
        return np.zeros(0, dtype=np.float64)
    return np.log(w)


# ---------------------------------------------------------------------------
# deterministic primitives
# ---------------------------------------------------------------------------
def _gumbel(u):
    """Gumbel(0,1) variates from uniform draws: ``-log(-log(u))``."""
    u = np.clip(np.asarray(u, dtype=np.float64), _U_CLIP, 1.0 - _U_CLIP)
    return -np.log(-np.log(u))


def _normalized_weights(w):
    """Weights rescaled so the maximum is exactly 1 (scale invariance)."""
    logw = pl_log_weights(w)
    return np.exp(logw - logw.max())


def _renormalize_to_seats(p, seats):
    """Enforce the hard invariants ``0 <= p_i <= 1`` and ``sum_i p_i == seats``.

    Water-filling: a deficit is added in proportion to remaining headroom
    ``1 - p_i``, a surplus is removed in proportion to ``p_i``; repeat because
    clipping at 0/1 can re-introduce a small gap.  Converges in a few passes for
    any p in [0,1] with ``sum(p) >= seats - n``.
    """
    p = np.clip(np.asarray(p, dtype=np.float64), 0.0, 1.0)
    for _ in range(12):
        s = p.sum()
        gap = seats - s
        if abs(gap) <= 1e-12:
            break
        if gap > 0.0:
            head = 1.0 - p
            hs = head.sum()
            if hs <= 0.0:
                break
            p = p + gap * head / hs
        else:
            if s <= 0.0:
                break
            p = p * (seats / s)
        p = np.clip(p, 0.0, 1.0)
    return p


# ---------------------------------------------------------------------------
# exact subset-DP path
# ---------------------------------------------------------------------------
def pl_win_probs_exact(weights, seats):
    """Exact individual top-K win probabilities by subset dynamic programming.

    Exact to machine precision for all ``n <= EXACT_MAX_N`` (cost ``O(n 2^n)``):
    it evaluates the Plackett-Luce selection probabilities directly, it does not
    simulate or approximate.

    Parameters
    ----------
    weights : array_like
        Strictly positive weights, shape ``(n,)``.
    seats : int
        Number of winners ``K``; clamped to ``[0, n]``.

    Returns
    -------
    numpy.ndarray
        ``P(win_i) = P(i in top-K)``, shape ``(n,)``, float64, summing to ``K``
        (to floating-point tolerance).

    Raises
    ------
    ValueError
        If ``n > EXACT_MAX_N`` (contract A6: raise, never silently approximate).
    """
    w = _as_weights(weights)
    n = w.size
    if n == 0:
        return np.zeros(0, dtype=np.float64)
    seats = _as_seats(seats, n)
    if seats <= 0:
        return np.zeros(n, dtype=np.float64)
    if seats >= n:
        return np.ones(n, dtype=np.float64)
    if n > EXACT_MAX_N:
        raise ValueError(
            f"exact subset DP supports n <= {EXACT_MAX_N}; got n={n}. "
            "Use method='auto' (deterministic quadrature) or method='mc'."
        )

    w = _normalized_weights(w)          # max == 1; no overflow anywhere below
    size = 1 << n
    idx = np.arange(size, dtype=np.int32)
    full = size - 1

    popcount = np.zeros(size, dtype=np.int16)
    for i in range(n):
        popcount += ((idx >> np.int32(i)) & np.int32(1)).astype(np.int16)

    # wsum[mask] = sum_{j in mask} w_j: subset-sum DP, positive terms only.
    wsum = np.zeros(size, dtype=np.float64)
    for i in range(n):
        bit = np.int32(1 << i)
        has = (idx & bit) != 0
        wsum[has] = wsum[idx[has] ^ bit] + w[i]

    g = np.zeros(size, dtype=np.float64)
    g[0] = 1.0
    for k in range(1, seats + 1):
        masks = np.flatnonzero(popcount == k)
        acc = np.zeros(masks.size, dtype=np.float64)
        for i in range(n):
            bit = np.int32(1 << i)
            sel = (masks & bit) != 0
            if not sel.any():
                continue
            prev = masks[sel] ^ bit
            # complement sum of `prev`: positive, includes w_i, so ratio in (0, 1].
            acc[sel] += g[prev] * (w[i] / wsum[full ^ prev])
        g[masks] = acc

    top = np.flatnonzero(popcount == seats)
    p = np.zeros(n, dtype=np.float64)
    for i in range(n):
        sel = (top & np.int32(1 << i)) != 0
        p[i] = g[top[sel]].sum()
    return p


# ---------------------------------------------------------------------------
# deterministic large-n path: Poisson-binomial / exponential-race quadrature
# ---------------------------------------------------------------------------
def _simpson_grid(w_min):
    """Simpson grid in u = log t for a given normalised minimum weight (cached).

    Depends only on ``w_min`` and the module constants, so caching it by the exact
    float value is pure memoisation: the arrays are identical to recomputing them.
    """
    key = float(w_min)
    hit = _GRID_CACHE.get(key)
    if hit is not None:
        _STATS["grid_hit"] += 1
        return hit
    _STATS["grid_miss"] += 1
    t_hi = _QUAD_TAIL_C / w_min
    u_lo, u_hi = np.log(_QUAD_T_LO), np.log(t_hi)
    span = u_hi - u_lo
    h = _QUAD_H
    m = int(np.ceil(span / h))          # number of Simpson intervals
    if m < 2:
        m = 2
    if m % 2:
        m += 1
    if m + 1 > _QUAD_MAX_NODES:         # documented: coarsen rather than blow up
        m = _QUAD_MAX_NODES - 1
        if m % 2:
            m -= 1
        h = span / m
    u = u_lo + np.arange(m + 1) * h
    t = np.exp(u)
    sw = np.full(m + 1, h / 3.0, dtype=np.float64)
    sw[1:-1:2] = 4.0 * h / 3.0
    sw[2:-1:2] = 2.0 * h / 3.0
    if len(_GRID_CACHE) >= _GRID_CACHE_MAX:
        _GRID_CACHE.clear()
    _GRID_CACHE[key] = (t, sw, m)
    return t, sw, m


def _quadrature_win_probs(w, seats):
    """Deterministic O(n * min(K, n-K) * nodes) top-K win probabilities.

    See the module docstring for the derivation.  ``w`` must be positive.
    Returns ``(p, n_nodes)``.
    """
    n = w.size
    if seats <= 0:
        return np.zeros(n, dtype=np.float64), 0
    if seats >= n:
        return np.ones(n, dtype=np.float64), 0

    wn = _normalized_weights(w)         # max == 1; results are scale invariant
    # Floor the (relative) weight tail: an item with w_i/ w_max < 1e-30 has win
    # probability < ~1e-28, so treating it as an atomically-never-winning item is
    # far below the documented 2e-3 bound; it bounds the t grid (t_hi = C/w_min)
    # and keeps every intermediate finite for arbitrary positive weights.
    wn = np.maximum(wn, _QUAD_W_FLOOR)
    w_min = float(wn.min())

    # Simpson grid in u = log t, spanning [t_lo, C / w_min] (cached by w_min).
    t, sw, m = _simpson_grid(w_min)

    # Choose the cheaper tail: "below" needs coefficients 0..K-1,
    # "above" needs 0..(n-K)-1.  Both use the same DP factors (p=below, q=above):
    # in each mode the DP variable is the cheaper count and q is its "not-p" factor.
    below = (seats - 1) <= (n - seats - 1)
    d = seats - 1 if below else (n - seats - 1)
    d = max(d, 0)

    # float64 inputs for the closed forms, float32 DP storage: the DP carries
    # products of hundreds of probabilities, where float32 relative error ~1e-6 is
    # far below the documented 2e-3 quadrature bound, and halving the memory
    # traffic roughly halves the runtime at the contract size (n=300, K=36).
    dt = np.float32
    p_below = (-np.expm1(-(wn[:, None] * t[None, :]))).astype(dt)   # (n, nodes)
    q_above = np.exp(-(wn[:, None] * t[None, :])).astype(dt)

    # Suffix DP: Suf[i][a] = P(exactly a of items i..n-1 are "below"/"above").
    # The DP variable counts "below" in below mode and "above" in above mode, so
    # the stay/increment factors are (not-success, success) respectively.
    if below:
        f_stay, f_inc = q_above, p_below
    else:
        f_stay, f_inc = p_below, q_above
    Suf = np.empty((n + 1, d + 1, m + 1), dtype=dt)
    Suf[n, :, :] = 0.0
    Suf[n, 0, :] = 1.0
    for i in range(n - 1, -1, -1):
        cur = Suf[i + 1]
        nxt = Suf[i]
        np.multiply(cur, f_stay[i][None, :], out=nxt)
        nxt[1:] += f_inc[i][None, :] * cur[:-1]
    # Convert the suffix blocks to cumulative form in one vectorised call
    # (cum[a] = sum_{b<=a} Suf[b]).
    np.cumsum(Suf, axis=1, out=Suf)

    P = np.zeros(n, dtype=np.float64)
    Pre = np.zeros((d + 1, m + 1), dtype=dt)
    Pre[0, :] = 1.0
    tmp = np.empty((d + 1, m + 1), dtype=dt)
    sign = 1.0 if below else -1.0
    offset = 0.0 if below else 1.0
    for i in range(n):
        # sum_{a=0..d} Pre[a] * cum[d-a] = P(count_others <= d)
        tail = np.einsum("am,am->m", Pre, Suf[i + 1][::-1]).astype(np.float64)
        G = np.clip(offset + sign * tail, 0.0, 1.0)
        kernel = wn[i] * t * q_above[i].astype(np.float64)
        P[i] = float(np.dot(sw, kernel * G))
        # advance prefix DP with the same factors
        np.multiply(Pre, f_stay[i][None, :], out=tmp)
        tmp[1:] += f_inc[i][None, :] * Pre[:-1]
        Pre, tmp = tmp, Pre
    return P, m + 1


# ---------------------------------------------------------------------------
# Monte-Carlo validation path
# ---------------------------------------------------------------------------
def pl_win_probs_mc(weights, seats, rng=None, n_mc=20000):
    """Monte-Carlo individual top-K win probabilities and standard errors.

    Each sample is one independent Plackett-Luce top-K draw, so item ``i``'s win
    indicator is Bernoulli and

        SE_i = sqrt(p_i (1 - p_i) / n_mc)

    is the exact binomial standard error of the marginal frequency (winner
    indicators within one sample are multinomially negatively correlated, which
    does not affect the marginal variance).  ``4 * SE`` is a conservative ~95 %
    per-item band; choose ``n_mc = 4 p (1-p) / tol^2`` for a target error.

    Parameters
    ----------
    weights : array_like
        Strictly positive weights, shape ``(n,)``.
    seats : int
        Number of winners.
    rng : numpy.random.Generator or None
        Random source.  ``None`` uses a fresh unseeded generator (not
        reproducible); validation code must pass ``np.random.default_rng(seed)``.
    n_mc : int
        Number of contests simulated, at least 100.

    Returns
    -------
    (p, se) : tuple of numpy.ndarray
        Win probabilities and standard errors, shape ``(n,)`` each.
    """
    w = _as_weights(weights)
    n = w.size
    if n == 0:
        return np.zeros(0), np.zeros(0)
    seats = _as_seats(seats, n)
    if seats <= 0:
        return np.zeros(n), np.zeros(n)
    if seats >= n:
        return np.ones(n), np.zeros(n)
    n_mc = int(n_mc)
    if n_mc < 100:
        raise ValueError("n_mc must be at least 100")
    rng = np.random.default_rng() if rng is None else rng
    logw = pl_log_weights(w)

    counts = np.zeros(n, dtype=np.int64)
    chunk = max(1, min(n_mc, _MC_CHUNK_ELEMS // max(n, 1)))
    done = 0
    while done < n_mc:
        m = min(chunk, n_mc - done)
        scores = logw[None, :] + _gumbel(rng.random((m, n)))
        chosen = np.argpartition(scores, n - seats, axis=1)[:, n - seats:]
        counts += np.bincount(chosen.ravel(), minlength=n)
        done += m
    p = counts / float(n_mc)
    se = np.sqrt(p * (1.0 - p) / float(n_mc))
    return p, se


# ---------------------------------------------------------------------------
# public dispatchers
# ---------------------------------------------------------------------------
def _dispatch(weights, seats, method, rng, n_mc):
    """Return ``(p, info)`` for one method; shared by the public functions."""
    w = _as_weights(weights)
    n = w.size
    if n == 0:
        return np.zeros(0, dtype=np.float64), {
            "method": method, "n": 0, "seats": 0, "seats_eff": 0,
            "max_error_estimate": 0.0, "runtime_ms": 0.0, "sum_p": 0.0,
        }
    seats = _as_seats(seats, n)
    t0 = time.perf_counter()
    info = {"n": n, "seats": seats, "seats_eff": seats}
    # Pure memoisation of the deterministic paths (task-12).  The key contains the
    # exact weight bytes and seats, so a hit returns bit-identical probabilities.
    cache_key = None
    if method in ("auto", "exact") and 0 < seats < n:
        if method == "exact" and n > EXACT_MAX_N:
            raise ValueError(
                f"exact subset DP supports n <= {EXACT_MAX_N}; got n={n}. "
                "Use method='auto' (deterministic quadrature) or method='mc'."
            )
        cache_key = (method, int(seats), w.tobytes())
        hit = _RESULT_CACHE.get(cache_key)
        if hit is not None:
            _STATS["result_hit"] += 1
            p_cached, cached_method = hit
            info.update(method=cached_method,
                        max_error_estimate=(_EXACT_EST_ERR if cached_method == "exact"
                                            else _QUAD_EST_ERR),
                        cached=True)
            p = p_cached.copy()
            info["sum_p"] = float(p.sum())
            info["runtime_ms"] = 1000.0 * (time.perf_counter() - t0)
            return p, info

    if seats <= 0:
        p = np.zeros(n, dtype=np.float64)
        info.update(method="boundary", max_error_estimate=0.0)
    elif seats >= n:
        p = np.ones(n, dtype=np.float64)
        info.update(method="boundary", max_error_estimate=0.0)
    elif method in ("auto", "exact"):
        if n <= AUTO_EXACT_N:
            p = pl_win_probs_exact(w, seats)
            info.update(method="exact", max_error_estimate=_EXACT_EST_ERR)
        elif method == "exact":
            # unreachable (pl_win_probs_exact raises), kept explicit
            raise ValueError(
                f"exact subset DP supports n <= {EXACT_MAX_N}; got n={n}"
            )
        else:
            p, n_nodes = _quadrature_win_probs(w, seats)
            info.update(method="quadrature", max_error_estimate=_QUAD_EST_ERR,
                        n_quadrature_nodes=n_nodes)
        p = _renormalize_to_seats(p, seats)
        if abs(p.sum() - seats) > 1e-9:          # hard invariant (contract: <=1e-6)
            raise RuntimeError(
                f"seat-sum invariant violated: sum(P)={p.sum()} seats={seats}"
            )
    elif method == "mc":
        if rng is None:
            raise ValueError(
                "method='mc' requires a caller-supplied seeded rng; "
                "it is a validation-only path"
            )
        p, se = pl_win_probs_mc(w, seats, rng=rng, n_mc=n_mc)
        info.update(method="mc", max_error_estimate=float(se.max()), se=se)
    else:                                        # pragma: no cover - guarded above
        raise ValueError(f"unknown method {method!r}")

    if cache_key is not None:
        _STATS["result_miss"] += 1
        if len(_RESULT_CACHE) >= _RESULT_CACHE_MAX:
            _RESULT_CACHE.clear()
        _RESULT_CACHE[cache_key] = (p.copy(), info.get("method", method))
    info["sum_p"] = float(p.sum())
    info["runtime_ms"] = 1000.0 * (time.perf_counter() - t0)
    return p, info


def pl_win_probs(weights, seats, method="auto", rng=None, n_mc=20000):
    """Individual top-K win probabilities (binding engine API, contract §1.3).

    ``method``
        ``"auto"`` (default, deterministic): exact subset DP for ``n <= 20``,
        deterministic Poisson-binomial quadrature above; renormalised so that
        ``sum_i P_i == seats``.  ``"exact"``: exact subset DP, raises for
        ``n > EXACT_MAX_N = 20``.  ``"mc"``: validation-only Monte Carlo, requires
        a caller-supplied seeded ``rng`` and returns ``(p, se)``.
    ``rng``, ``n_mc``
        Used by ``method="mc"`` only; ignored on the deterministic paths.

    Returns
    -------
    numpy.ndarray
        ``P(win_i)``, shape ``(n,)``.  For ``method="mc"`` a tuple
        ``(p, se)`` is returned instead (standard errors).

    Raises
    ------
    ValueError
        On invalid weights/seats/method, or ``method='exact'`` with ``n`` beyond
        the documented cap.
    """
    _check_method(method, ("auto", "exact", "mc"))
    p, info = _dispatch(weights, seats, method, rng, n_mc)
    if method == "mc":
        return (p, info["se"])          # validation path: probabilities + errors
    return p


def pl_win_probs_detail(weights, seats, method="auto", rng=None, n_mc=20000):
    """As :func:`pl_win_probs`, plus a diagnostic ``info`` dict.

    Returns
    -------
    (p, info) : tuple
        ``p`` is the ``(n,)`` probability vector.  ``info`` contains
        ``method`` (``"exact"`` | ``"quadrature"`` | ``"mc"`` | ``"boundary"``),
        ``n``, ``seats``, ``seats_eff``, ``max_error_estimate`` (documented bound:
        ``1e-13`` exact, ``2e-3`` quadrature, ``max se`` MC), ``runtime_ms``
        (wall clock for this call), ``sum_p`` and, for quadrature, the number of
        Simpson nodes used.  For ``method='mc'`` ``info['se']`` also carries the
        standard errors.
    """
    _check_method(method, ("auto", "exact", "mc"))
    return _dispatch(weights, seats, method, rng, n_mc)


# ---------------------------------------------------------------------------
# deterministic realisation from caller-supplied uniforms
# ---------------------------------------------------------------------------
def pl_stats():
    """Return (and leave untouched) the cache statistics dict (task-12 observability)."""
    return dict(_STATS)


def pl_realize(weights, seats, u):
    """Realise one top-K Plackett-Luce contest from caller-supplied uniforms.

    Selection rule (Gumbel-max representation of Plackett-Luce)::

        score_i = log(w_i) + Gumbel(u_i),   Gumbel(u) = -log(-log(u))
        winners = the `seats` items with the largest score.

    This is the exact, uncorrupted engine rule.  It is deterministic given ``u``
    (the caller owns randomness); complexity is O(n) to select via
    ``argpartition`` plus O(k log k) to sort the chosen block.

    Parameters
    ----------
    weights : array_like
        Strictly positive weights, shape ``(n,)``.
    seats : int
        Number of winners; clamped to ``[0, n]``.
    u : array_like
        Caller-supplied ``U(0,1)`` draws, shape ``(n,)``, clipped to
        ``[1e-12, 1 - 1e-12]`` internally.

    Returns
    -------
    numpy.ndarray
        Boolean mask, shape ``(n,)``, with exactly ``min(seats, n)`` True.

    Notes
    -----
    Equal scores can only occur for pathological draws (e.g. identical ``u`` at two
    equal weights); the tie is then broken deterministically by NumPy's selection
    order for a given input array, and callers must not rely on which of two
    exactly-tied items is chosen.  Continuous ``u`` makes ties probability zero.
    """
    w = _as_weights(weights)
    n = w.size
    if n == 0:
        return np.zeros(0, dtype=bool)
    seats = _as_seats(seats, n)
    u = np.asarray(u, dtype=np.float64)
    if u.shape != w.shape:
        raise ValueError(f"u must have the same shape as weights ({n},)")
    winners = np.zeros(n, dtype=bool)
    if seats <= 0:
        return winners
    if seats >= n:
        winners[:] = True
        return winners
    logw = pl_log_weights(w)
    score = logw + _gumbel(u)
    order = np.argpartition(score, n - seats)[n - seats:]
    winners[order] = True
    return winners
