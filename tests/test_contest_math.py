"""Gate 1c validation tests for the independent Plackett-Luce reference module.

These tests validate ``eduengine.contest_math`` -- a pure-NumPy, engine-independent
top-K Gumbel-max Plackett-Luce reference used by the Atlas contest audit.  They
do not import the engine simulation (only the standalone reference module).

Run (from the worktree root)::

    OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python \
    -m pytest tests/test_contest_math.py -q

Requirements covered:
 (1) n=2, seats=1, weights [4, 1] -> exact P = [0.8, 0.2].
 (2) equal weights, n=3 and n=4, seats 1..n-1 -> exact k/n; MC within 4 sigma.
 (3) sum_i P(win_i) == seats over a weight/scale grid.
 (4) monotonicity: raising one applicant's weight never lowers its own P(win).
 (5) exact-vs-MC agreement table by n / seats / dispersion (max |diff|, sigma).
 (6) pl_realize determinism for fixed u; exactly `seats` winners.
"""

import ast
import inspect

import numpy as np
import pytest

import eduengine.contest_math as cm
from eduengine.contest_math import (
    AUTO_EXACT_N,
    EXACT_MAX_N,
    pl_log_weights,
    pl_win_probs_detail,
    pl_realize,
    pl_win_probs,
    pl_win_probs_exact,
    pl_win_probs_mc,
)

# Seeds are fixed so every reported number in the audit is reproducible.
SEED = 20261125


def _lognormal_weights(n, sigma, seed, mean=1.0):
    """Positive weights with log-dispersion ``sigma`` and arithmetic mean 1."""
    rng = np.random.default_rng(seed)
    w = np.exp(sigma * rng.standard_normal(n))
    return w * (mean / w.mean())


# ---------------------------------------------------------------------------
# (1) analytic anchor: two applicants, one seat, weights 4:1
# ---------------------------------------------------------------------------
def test_two_applicant_anchor():
    """PL with two players is the logistic/Bradley-Terry case: P = w_i / sum(w)."""
    p = pl_win_probs([4.0, 1.0], 1)
    np.testing.assert_allclose(p, [0.8, 0.2], atol=1e-12)
    # Method selection must not change the answer.
    np.testing.assert_allclose(pl_win_probs([4.0, 1.0], 1, method="exact"), p, atol=0)
    np.testing.assert_allclose(pl_win_probs([4.0, 1.0], 1, method="auto"), p, atol=0)
    # Scale invariance: 4:1 in any units is the same contest.
    np.testing.assert_allclose(pl_win_probs([4e-200, 1e-200], 1), p, atol=1e-12)
    np.testing.assert_allclose(pl_win_probs([4e200, 1e200], 1), p, atol=1e-12)


# ---------------------------------------------------------------------------
# (2) equal weights: exact combinatorial values + MC within 4 sigma
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("n", [3, 4])
def test_equal_weights_exact_combinatorial(n):
    """With equal weights every applicant wins K/n by symmetry (exact, not MC)."""
    w = np.ones(n)
    for k in range(1, n):
        p = pl_win_probs(w, k)
        np.testing.assert_allclose(p, np.full(n, k / n), atol=1e-12)
        # Exact path is in use at these n.
        np.testing.assert_allclose(pl_win_probs_exact(w, k), p, atol=0)


@pytest.mark.parametrize("n", [3, 4])
def test_equal_weights_mc_within_4_sigma(n):
    """Monte-Carlo win frequencies agree with K/n within 4 binomial sigma."""
    w = np.ones(n)
    n_mc = 20000
    for k in range(1, n):
        rng = np.random.default_rng(SEED + 100 * n + k)
        p_mc, se = pl_win_probs_mc(w, k, rng=rng, n_mc=n_mc)
        exact = k / n
        assert np.all(np.abs(p_mc - exact) <= 4.0 * se + 1e-15), (
            f"n={n} k={k}: |MC-exact|={np.abs(p_mc - exact)} > 4*se={4 * se}"
        )
        # Documented SE is the exact binomial SE of the marginal frequency.
        np.testing.assert_allclose(se, np.sqrt(exact * (1 - exact) / n_mc), rtol=0.2)


# ---------------------------------------------------------------------------
# (3) probabilities are a proper allocation: sum_i P(win_i) == seats
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("n", [2, 3, 5, 8, 12])
def test_sum_of_win_probs_equals_seats(n):
    """Sum_i P(win_i) = K exactly for every seats/weight pattern in the grid."""
    patterns = {
        "equal": np.ones(n),
        "logspread": np.geomspace(0.2, 5.0, n),
        "lognormal_sigma1": _lognormal_weights(n, 1.0, SEED + n),
        "lognormal_sigma2": _lognormal_weights(n, 2.0, SEED + 7 * n),
    }
    for name, w in patterns.items():
        for k in range(1, n):
            p = pl_win_probs(w, k)
            assert np.isfinite(p).all(), f"{name} n={n} k={k}: non-finite P"
            assert (p >= 0).all() and (p <= 1).all(), f"{name} n={n} k={k}: P outside [0,1]"
            np.testing.assert_allclose(
                p.sum(), k, atol=1e-9, err_msg=f"{name} n={n} k={k}"
            )


# ---------------------------------------------------------------------------
# (4) monotonicity: raising one applicant's weight cannot lower its own P(win)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("n", [4, 7, 11])
@pytest.mark.parametrize("sigma", [0.0, 0.5, 1.0, 2.0])
def test_monotonicity_in_own_weight(n, sigma):
    """P(win_i) is non-decreasing in w_i holding every other weight fixed."""
    base = _lognormal_weights(n, sigma, SEED + 1000 * n + int(10 * sigma))
    seats_grid = sorted({1, 2, max(1, n // 2), n - 1})
    for k in seats_grid:
        prev = pl_win_probs(base, k)[0]
        for mult in (1.5, 2.0, 3.0, 5.0, 10.0):
            w = base.copy()
            w[0] = base[0] * mult
            cur = pl_win_probs(w, k)[0]
            assert cur >= prev - 1e-12, (
                f"n={n} sigma={sigma} k={k} mult={mult}: "
                f"P(win_0) fell {prev:.12f} -> {cur:.12f}"
            )
            prev = cur


def test_monotonicity_other_applicants_unaffected_in_direction():
    """Raising applicant j cannot raise applicant i's win probability (i != j)."""
    n, k = 9, 3
    base = _lognormal_weights(n, 1.0, SEED + 11)
    p0 = pl_win_probs(base, k)
    for j in (0, 4):
        w = base.copy()
        w[j] *= 4.0
        p1 = pl_win_probs(w, k)
        others = [i for i in range(n) if i != j]
        assert np.all(p1[others] <= p0[others] + 1e-12)


# ---------------------------------------------------------------------------
# (5) exact vs Monte-Carlo agreement table by n / seats / weight dispersion
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("n", [2, 3, 5, 8, 12])
@pytest.mark.parametrize("sigma", [0.25, 1.0, 2.0])
def test_exact_vs_mc_agreement_table(n, sigma, capsys):
    """Exact DP vs MC: max |diff| stays inside 5 sigma; table is printed with -s."""
    n_mc = 20000
    w = _lognormal_weights(n, sigma, SEED + 31 * n + int(100 * sigma))
    seats_grid = sorted({1, 2, max(1, n // 2), n - 1})
    for k in seats_grid:
        rng = np.random.default_rng(SEED + 17 * n + k)
        p_exact = pl_win_probs_exact(w, k)
        p_mc, se = pl_win_probs_mc(w, k, rng=rng, n_mc=n_mc)
        max_diff = float(np.max(np.abs(p_exact - p_mc)))
        max_se = float(np.max(se))
        z = max_diff / max_se if max_se > 0 else 0.0
        print(
            f"n={n:2d} sigma={sigma:4.2f} seats={k:2d} "
            f"max|diff|={max_diff:.5f} max_sigma={max_se:.5f} z={z:.2f}"
        )
        assert max_diff <= 5.0 * max_se + 1e-12, (
            f"n={n} sigma={sigma} seats={k}: max|diff|={max_diff} > 5*max_sigma={5 * max_se}"
        )
    capsys.readouterr()


# ---------------------------------------------------------------------------
# (6) pl_realize: determinism, seat count, and agreement with the exact probs
# ---------------------------------------------------------------------------
def test_realize_deterministic_and_exact_seat_count():
    """Fixed u reproduces the same winners; the winner count is exactly `seats`."""
    weights = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    u = np.array([0.11, 0.42, 0.73, 0.94, 0.27])
    for add_scale in (1.0, 1e-150, 1e150):
        w = weights * add_scale
        for k in range(1, len(w)):
            a = pl_realize(w, k, u)
            b = pl_realize(w, k, u)
            assert a.dtype == bool and a.shape == w.shape
            assert np.array_equal(a, b), "pl_realize is not deterministic for fixed u"
            assert int(a.sum()) == k
    # Boundary cases.
    assert pl_realize(weights, 0, u).sum() == 0
    assert pl_realize(weights, len(weights), u).all()
    assert pl_realize(weights, len(weights) + 5, u).all()
    assert pl_realize(np.zeros(0), 2, np.zeros(0)).size == 0


def test_realize_matches_gumbel_max_formula():
    """Winners are exactly the top seats of log(w) + Gumbel(u)."""
    rng = np.random.default_rng(SEED + 5)
    w = _lognormal_weights(200, 1.0, SEED + 6)
    u = rng.random(200)
    score = np.log(w) - np.log(-np.log(u))
    for k in (1, 7, 60):
        mask = pl_realize(w, k, u)
        expected = np.zeros(200, dtype=bool)
        expected[np.argsort(-score)[:k]] = True
        assert np.array_equal(mask, expected)
        assert int(mask.sum()) == k


def test_realize_frequencies_match_exact_probabilities():
    """Empirical winner frequencies over many u draws match the exact DP, < 4 sigma."""
    n, k, n_mc = 6, 2, 20000
    w = _lognormal_weights(n, 1.0, SEED + 41)
    p_exact = pl_win_probs_exact(w, k)
    rng = np.random.default_rng(SEED + 42)
    counts = np.zeros(n, dtype=np.int64)
    for _ in range(n_mc):
        counts += pl_realize(w, k, rng.random(n))
    p_obs = counts / n_mc
    se = np.sqrt(p_exact * (1 - p_exact) / n_mc)
    assert np.all(np.abs(p_obs - p_exact) <= 4.0 * se + 1e-12), (
        f"|obs-exact|={np.abs(p_obs - p_exact)} 4*se={4 * se}"
    )


# ---------------------------------------------------------------------------
# robustness: scale, extreme weights, no NaN/inf, no engine import
# ---------------------------------------------------------------------------
def test_extreme_weight_scale_is_finite():
    """Weights spanning double range give finite probabilities summing to seats."""
    cases = [
        [1e-300, 1.0, 1e300],
        [1e-300, 1e-300, 1.0],
        [1.0, 1e-300],
        [5e-324, 1.0, 1e300],   # smallest positive subnormal
        [1e300, 1e300, 1e-300],
    ]
    for w in cases:
        for k in (1, len(w) - 1):
            p = pl_win_probs(w, k)
            assert np.isfinite(p).all(), f"non-finite P for {w}, k={k}"
            assert (p >= 0).all() and (p <= 1).all()
            np.testing.assert_allclose(p.sum(), k, atol=1e-9)
        p_mc, se = pl_win_probs_mc(w, max(1, len(w) - 1), rng=np.random.default_rng(SEED))
        assert np.isfinite(p_mc).all() and np.isfinite(se).all()


def test_large_n_realize_is_fast_and_valid():
    """The realization path handles thousands of applicants (engine cohort scale)."""
    rng = np.random.default_rng(SEED + 77)
    w = np.exp(0.8 * rng.standard_normal(4000))
    u = rng.random(4000)
    mask = pl_realize(w, 400, u)
    assert int(mask.sum()) == 400
    # MC probabilities at this n (chunked path) are finite and sum to ~seats.
    p, se = pl_win_probs_mc(w, 400, rng=np.random.default_rng(SEED + 78), n_mc=4000)
    assert np.isfinite(p).all() and np.isfinite(se).all()
    assert abs(p.sum() - 400) < 20 * np.sqrt(400)


def test_log_weights_helper():
    np.testing.assert_allclose(pl_log_weights([1.0, np.e, np.e ** 2]), [0.0, 1.0, 2.0])
    assert pl_log_weights([]).shape == (0,)
    for bad in ([0.0, 1.0], [-1.0, 2.0], [np.nan, 1.0], [np.inf, 1.0]):
        with pytest.raises(ValueError):
            pl_log_weights(bad)


def test_argument_validation_and_method_guards():
    with pytest.raises(ValueError):
        pl_win_probs([1.0, 2.0], 1, method="bogus")
    with pytest.raises(ValueError):
        pl_win_probs([0.0, 1.0], 1)
    with pytest.raises(ValueError):
        pl_win_probs_mc([1.0, 2.0], 1, n_mc=10)
    with pytest.raises(ValueError):
        pl_realize([1.0, 2.0], 1, [0.5])          # u length mismatch
    # Exact path is hard-capped (O(n 2^n)); auto falls back to MC above it.
    n_big = EXACT_MAX_N + 1
    w_big = np.exp(0.3 * np.arange(n_big))
    with pytest.raises(ValueError):
        pl_win_probs_exact(w_big, 1)
    with pytest.raises(ValueError):
        pl_win_probs(w_big, 1, method="exact")
    p_auto = pl_win_probs(w_big, 1, method="auto",
                          rng=np.random.default_rng(SEED + 90), n_mc=4000)
    assert p_auto.shape == (n_big,) and abs(p_auto.sum() - 1) < 0.05
    # "auto" is exact at the documented threshold.
    w_at = np.exp(0.2 * np.arange(AUTO_EXACT_N))
    np.testing.assert_array_equal(
        pl_win_probs(w_at, 3, method="auto"), pl_win_probs_exact(w_at, 3)
    )


def test_seats_clamping_and_empty_input():
    assert pl_win_probs([], 1).size == 0
    assert pl_win_probs([1.0, 2.0], 0).tolist() == [0.0, 0.0]
    np.testing.assert_allclose(pl_win_probs([1.0, 2.0, 3.0], 3), [1.0, 1.0, 1.0])
    np.testing.assert_allclose(pl_win_probs([1.0, 2.0, 3.0], 99), [1.0, 1.0, 1.0])
    with pytest.raises(ValueError):
        pl_win_probs([1.0, 2.0], 1.5)


def test_reference_module_does_not_import_the_engine():
    """Independence contract: the module imports nothing from eduengine."""
    tree = ast.parse(inspect.getsource(cm))
    offenders = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            offenders += [a.name for a in node.names if "eduengine" in a.name]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                offenders.append(f"relative:{node.module}")
            elif node.module and "eduengine" in node.module:
                offenders.append(node.module)
    assert not offenders, f"reference module imports the engine: {offenders}"


# ===========================================================================
# Contract v1.0 amendments A5/A6 (deterministic auto path) and §1.3 targets
# ===========================================================================
def test_auto_is_deterministic_and_rng_free():
    """A5: method='auto'/'exact' are pure functions of (weights, seats)."""
    rng = np.random.default_rng(SEED + 501)
    w = np.exp(2.0 * rng.standard_normal(300))
    p1 = pl_win_probs(w, 36, method="auto")
    p2 = pl_win_probs(w, 36, method="auto")
    assert np.array_equal(p1, p2), "auto path is not deterministic"
    # rng/n_mc must be ignored on the deterministic paths.
    p3 = pl_win_probs(w, 36, method="auto", rng=np.random.default_rng(1), n_mc=777)
    p4 = pl_win_probs(w, 36, method="auto", rng=np.random.default_rng(2), n_mc=999)
    assert np.array_equal(p1, p3) and np.array_equal(p1, p4)
    # Same call at small n uses the exact DP and is still deterministic.
    w2 = np.exp(1.5 * rng.standard_normal(9))
    assert np.array_equal(pl_win_probs(w2, 3), pl_win_probs(w2, 3))


@pytest.mark.parametrize("n", [13, 15, 18, 20])
def test_auto_equals_exact_12_lt_n_le_20(n):
    """A5/§1.3: auto must equal the exact DP for 12 < n <= 20 (1e-10)."""
    rng = np.random.default_rng(SEED + 600 + n)
    w = np.exp(1.5 * rng.standard_normal(n))
    for k in (1, 2, n // 3, n // 2, n - 2):
        p_auto = pl_win_probs(w, k, method="auto")
        p_exact = pl_win_probs_exact(w, k)
        np.testing.assert_allclose(p_auto, p_exact, atol=1e-10, rtol=0)


def test_quadrature_matches_exact_at_n20():
    """The deterministic large-n quadrature equals the exact DP at n=20."""
    from eduengine.contest_math import _quadrature_win_probs

    rng = np.random.default_rng(SEED + 700)
    for disp in (0.0, 1.0, 3.0, 6.0):
        w = np.exp(disp * rng.standard_normal(20))
        for k in (1, 4, 10, 19):
            p_quad, _nodes = _quadrature_win_probs(w, k)
            p_exact = pl_win_probs_exact(w, k)
            assert np.max(np.abs(p_quad - p_exact)) <= 1e-3, (disp, k)


@pytest.mark.parametrize("disp", [0.0, 1.0, 2.0, 4.0, 6.0])
def test_large_n_accuracy_vs_mc(disp, capsys):
    """§1.3 target: n=300, seats=36, log-weight dispersion 0..6 vs seeded MC."""
    rng = np.random.default_rng(SEED + 800 + int(10 * disp))
    n, seats = 300, 36
    w = np.ones(n) if disp == 0.0 else np.exp(disp * rng.standard_normal(n))
    p_auto = pl_win_probs(w, seats, method="auto")
    p_mc, se = pl_win_probs_mc(w, seats, rng=np.random.default_rng(SEED + 900), n_mc=60000)
    d = np.abs(p_auto - p_mc)
    print(f"n=300 disp={disp:4.1f}: max|auto-mc|={d.max():.5f} mean={d.mean():.5f} "
          f"max_se={se.max():.5f} |sum-seats|={abs(p_auto.sum()-seats):.2e}")
    assert d.max() <= 0.012, f"n=300 disp={disp}: max|auto-mc|={d.max()} > 0.01 target"
    assert d.mean() <= 0.004, f"n=300 disp={disp}: mean|auto-mc|={d.mean()}"
    assert abs(p_auto.sum() - seats) <= 1e-6, "seat-sum invariant violated"
    assert np.all(p_auto >= 0) and np.all(p_auto <= 1)
    capsys.readouterr()


def test_auto_seat_sum_invariant_grid():
    """§1.3: |sum_i P_i - seats| <= 1e-6 for the deterministic path."""
    rng = np.random.default_rng(SEED + 950)
    for n, seats in [(25, 1), (100, 10), (300, 36), (300, 270), (60, 59)]:
        w = np.exp(2.0 * rng.standard_normal(n))
        p = pl_win_probs(w, seats, method="auto")
        assert abs(p.sum() - seats) <= 1e-6
        np.testing.assert_array_equal(p, pl_win_probs(w, seats, method="auto"))


def test_runtime_target_and_detail_info():
    """§1.3: measured runtime for n=300, seats=36 and pl_win_probs_detail fields."""
    rng = np.random.default_rng(SEED + 990)
    w = np.exp(2.0 * rng.standard_normal(300))
    p, info = pl_win_probs_detail(w, 36, method="auto")
    for key in ("method", "n", "seats", "seats_eff", "max_error_estimate", "runtime_ms"):
        assert key in info, f"missing info key {key!r}"
    assert info["method"] == "quadrature"
    assert info["n"] == 300 and info["seats"] == 36
    assert info["runtime_ms"] <= 50.0, f"runtime {info['runtime_ms']:.1f} ms > 50 ms target"
    assert info["max_error_estimate"] <= 0.01
    print(f"n=300 seats=36 runtime={info['runtime_ms']:.1f}ms "
          f"nodes={info.get('n_quadrature_nodes')} maxerr_est={info['max_error_estimate']}")

    p_exact, info_exact = pl_win_probs_detail(w[:8], 3, method="exact")
    assert info_exact["method"] == "exact" and info_exact["max_error_estimate"] <= 1e-12
    p_mc, info_mc = pl_win_probs_detail(
        w[:30], 5, method="mc", rng=np.random.default_rng(SEED + 991), n_mc=2000)
    assert info_mc["method"] == "mc" and "se" in info_mc and info_mc["se"].shape == (30,)


def test_method_mc_requires_seeded_rng():
    """A5: MC is validation-only and must be caller-seeded."""
    w = np.exp(np.arange(6.0))
    with pytest.raises(ValueError):
        pl_win_probs(w, 2, method="mc")          # no rng -> refused
    p, se = pl_win_probs(w, 2, method="mc", rng=np.random.default_rng(SEED), n_mc=1000)
    assert p.shape == (6,) and se.shape == (6,)
    # Same seed -> identical validation result.
    p2, se2 = pl_win_probs(w, 2, method="mc", rng=np.random.default_rng(SEED), n_mc=1000)
    np.testing.assert_array_equal(p, p2)
    np.testing.assert_array_equal(se, se2)


def test_boundary_seats():
    """seats >= n -> all P=1; seats = 0 -> all P=0 (both methods)."""
    w = np.exp(np.linspace(0, 2, 7))
    np.testing.assert_array_equal(pl_win_probs(w, 7), np.ones(7))
    np.testing.assert_array_equal(pl_win_probs(w, 99), np.ones(7))
    np.testing.assert_array_equal(pl_win_probs(w, 0), np.zeros(7))
    np.testing.assert_array_equal(pl_win_probs_exact(w, 7), np.ones(7))
    assert pl_realize(w, 7, np.zeros(7)).sum() == 7
    assert pl_realize(w, 0, np.zeros(7)).sum() == 0
