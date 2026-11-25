"""GPU-backend equivalence tests (Gate-1 amendment A-GPU-1; docs/gpu/EQUIVALENCE.md).

These tests are skipped unless torch+CUDA is available. The CPU-backend batch path is always
tested (it must be bit-identical to the per-row loop); the GPU batch path must be within the
declared bound of 1e-7 max abs difference.
"""
import numpy as np
import pytest

from eduengine import contest_math as cm

SEED = 20261125
BOUND = 1e-7


def _grid_rows(n, seats, disp, seed):
    rng = np.random.default_rng(seed)
    return np.array([np.exp(disp * rng.standard_normal(n)) for _ in range(9)])


def _gpu_available():
    """True iff torch+CUDA is usable AND the optional backend can be registered/selected."""
    try:
        from eduengine import contest_gpu
        if not contest_gpu.available():
            return False
        cm.register_gpu_backend(contest_gpu)          # idempotent; documented in INTEGRATION.md
        cm.set_pl_backend("gpu")
        cm.set_pl_backend("cpu")
        return True
    except Exception:
        return False


@pytest.mark.parametrize("n,seats,disp", [(300, 36, 1.0), (300, 69, 2.0), (600, 69, 1.0)])
def test_cpu_batch_is_bit_identical_to_per_row(n, seats, disp):
    cm.set_pl_backend("cpu")
    W = _grid_rows(n, seats, disp, SEED)
    P = np.asarray(cm.pl_win_probs_batch(W, seats), float)
    ref = np.stack([np.asarray(cm.pl_win_probs(row, seats), float) for row in W])
    assert np.array_equal(P, ref), "CPU batch path must be bit-identical to the per-row loop"


@pytest.mark.skipif(not _gpu_available(), reason="torch/CUDA unavailable")
@pytest.mark.parametrize("n,seats,disp", [(300, 36, 1.0), (300, 69, 2.0), (600, 69, 1.0)])
def test_gpu_batch_within_declared_deviation(n, seats, disp):
    W = _grid_rows(n, seats, disp, SEED)
    cm.set_pl_backend("cpu")
    ref = np.asarray(cm.pl_win_probs_batch(W, seats), float)
    cm.set_pl_backend("gpu")
    try:
        got = np.asarray(cm.pl_win_probs_batch(W, seats), float)
    finally:
        cm.set_pl_backend("cpu")
    d = float(np.max(np.abs(got - ref)))
    assert d <= BOUND, f"max|dP|={d:.3e} exceeds the declared bound {BOUND:.0e}"
    assert got.shape == ref.shape
    for row in got:
        assert abs(float(row.sum()) - min(seats, n)) <= 1e-6
