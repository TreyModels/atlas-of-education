"""GPU Plackett-Luce backend port checks (Gate-1 amendment A-GPU-1).

Owner: qa-verifier (``tests/**`` lane). These tests live on the GPU-port branch
(``research/gpu-pl-port-auditv2-2026-11-25``, engine port commit ``59fd249``) and deliberately do not
modify engine code.

Scope
-----
* backend registration/selection contract (default OFF, torch-free import, graceful CPU fallback);
* ``pl_win_probs_batch`` ≡ per-row ``pl_win_probs`` on the CPU path (bit-identical);
* GPU-vs-CPU parity on the canonical 130 fixtures, max abs dP <= 1e-7 (amendment A-GPU-1);
* boundary / seat-capacity cases (n in {1,2,12,20,21}, seats 0/1/n-1/n, equal & extreme weights);
* discrete-winner flips are *reported*, never failed (equivalence is declared on probabilities).

The GPU tests skip cleanly on hosts without torch/CUDA; the CPU tests are the default gate.
"""
from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
ENGINE_DIR = ROOT / "engine"
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from eduengine import contest_math as cm  # noqa: E402

# Canonical fixtures: EXACT copy of docs/gpu/port_verify.py (defines the central CPU digest).
FIXTURE_SEED = 20261125
N_FIXTURES = 130
TOL = 1e-7


def fixtures():
    rng = np.random.default_rng(FIXTURE_SEED)
    fx = []
    for _ in range(N_FIXTURES):
        n = int(rng.choice([12, 20, 21, 40, 60, 80, 120, 200, 300, 300, 300, 400, 600]))
        seats = int(rng.integers(1, n))
        disp = float(rng.choice([0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]))
        w = np.ones(n) if disp == 0.0 else np.exp(disp * rng.standard_normal(n))
        fx.append((n, seats, disp, w))
    return fx


def _subset(step=5):
    """Representative CPU-cost subset (26 fixtures) for the default CUDA-free test runs."""
    return fixtures()[::step]


def _cpu():
    cm.set_pl_backend("cpu")
    return cm


def _gpu_available():
    try:
        import eduengine.contest_gpu as cg  # noqa: F401
        return bool(cg.available())
    except Exception:
        return False


def _register_gpu():
    import eduengine.contest_gpu as cg
    if cm._get_gpu_module() is None:      # package-level registration happens only with env flag at import
        cm.register_gpu_backend(cg)
    return cg


requires_gpu = pytest.mark.skipif(not _gpu_available(), reason="torch/CUDA backend not available on this host")


# --------------------------------------------------------------------------------------------- backend contract
def test_default_backend_is_cpu_and_torch_free():
    """Default import (no ATLAS_PL_BACKEND) must be CPU and must not import torch or contest_gpu."""
    code = textwrap.dedent(
        """
        import sys
        from eduengine import contest_math as cm
        import numpy as np
        assert cm.pl_backend() == 'cpu', cm.pl_backend()
        assert 'torch' not in sys.modules, 'torch imported on default CPU path'
        assert 'eduengine.contest_gpu' not in sys.modules, 'GPU module imported on default CPU path'
        p = cm.pl_win_probs(np.array([4.0, 1.0, 1.0]), 1)
        assert p.shape == (3,) and abs(p.sum() - 1.0) < 1e-12
        print('OK', cm.pl_backend())
        """
    )
    env = {k: v for k, v in os.environ.items() if k != "ATLAS_PL_BACKEND"}
    env["PYTHONPATH"] = str(ENGINE_DIR)
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, cwd=str(ROOT))
    assert out.returncode == 0, out.stderr[-2000:]
    assert "OK cpu" in out.stdout


def test_backend_registration_flag_contract():
    """The registration/selection contract: set('cpu') works, set('gpu') raises when unregistered."""
    if cm._get_gpu_module() is not None and cm.pl_backend() == "gpu":
        cm.set_pl_backend("cpu")
    assert cm.pl_backend() == "cpu"
    assert cm.set_pl_backend("cpu") == "cpu"
    if cm._get_gpu_module() is None:
        with pytest.raises(RuntimeError, match="GPU backend requested but none is registered"):
            cm.set_pl_backend("gpu")
    else:                                  # on a GPU host the backend is registered by the package import flag
        assert cm.set_pl_backend("gpu") == "gpu"
        assert cm.pl_backend() == "gpu"
        with pytest.raises(Exception):
            cm.set_pl_backend("nonsense")
        cm.set_pl_backend("cpu")
    assert cm.pl_backend() == "cpu"


def test_gpu_flag_without_torch_falls_back_gracefully(tmp_path):
    """ATLAS_PL_BACKEND=gpu on a torch-less host imports fine and stays on the CPU backend."""
    blocker = tmp_path / "torch.py"
    blocker.write_text("raise ImportError('torch deliberately blocked for fallback test')\n")
    code = textwrap.dedent(
        """
        import sys
        import numpy as np
        from eduengine import contest_math as cm
        assert cm.pl_backend() == 'cpu', f'expected graceful CPU fallback, got {cm.pl_backend()}'
        assert cm._get_gpu_module() is None
        p = cm.pl_win_probs(np.array([2.0, 1.0]), 1)
        assert abs(p.sum() - 1.0) < 1e-12
        print('FALLBACK-OK')
        """
    )
    env = dict(os.environ, ATLAS_PL_BACKEND="gpu", PYTHONPATH=f"{tmp_path}{os.pathsep}{ENGINE_DIR}")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, cwd=str(ROOT))
    assert out.returncode == 0, out.stderr[-2000:]
    assert "FALLBACK-OK" in out.stdout


# --------------------------------------------------------------------------------------------- CPU batch semantics
def test_cpu_batch_is_bit_identical_to_per_row():
    """CPU ``pl_win_probs_batch`` must reproduce the per-row reference exactly (no tolerance)."""
    fx = _subset()
    for n, seats, disp, w in fx:
        ref = np.asarray(cm.pl_win_probs(w, seats, method="auto"), float)
        got = np.asarray(cm.pl_win_probs_batch(np.asarray([w]), seats, method="auto")[0], float)
        assert np.array_equal(ref, got), f"CPU batch != per-row for n={n} seats={seats} disp={disp}"
        assert abs(got.sum() - min(seats, n)) < 1e-12


def test_seat_capacity_and_boundaries():
    """Boundary/capacity cases: seat sums, [0,1] support, finite values, batch == per-row."""
    cases = []
    for n in (1, 2, 12, 20, 21):
        for seats in sorted({0, 1, max(n - 1, 0), n}):
            cases.append((n, seats, np.ones(n)))
    cases += [(20, 1, np.array([1e-200] * 10 + [1e200] * 10)),
              (21, 10, np.geomspace(1e-12, 1e12, 21)),
              (40, 3, np.ones(40))]
    for n, seats, w in cases:
        p = np.asarray(cm.pl_win_probs(w, seats), float)
        assert p.shape == (n,)
        assert np.all(np.isfinite(p)), f"non-finite probabilities for n={n} seats={seats}"
        assert np.all(p >= 0.0) and np.all(p <= 1.0 + 1e-12), f"probability outside [0,1] for n={n} seats={seats}"
        assert abs(p.sum() - min(seats, n)) < 1e-9, f"seat-sum {p.sum()} != {min(seats, n)} for n={n} seats={seats}"
        b = np.asarray(cm.pl_win_probs_batch(np.asarray([w]), seats)[0], float)
        assert np.array_equal(p, b), f"batch != per-row boundary case n={n} seats={seats}"
    # Multi-row batch: independent rows never interact, and each row follows the same contract.
    n, seats = 21, 7
    W = np.vstack([np.geomspace(1e-12, 1e12, n), np.ones(n), np.linspace(0.5, 2.0, n)])
    B = np.asarray(cm.pl_win_probs_batch(W, seats), float)
    assert B.shape == (3, n)
    for i in range(3):
        ref = np.asarray(cm.pl_win_probs(W[i], seats), float)
        assert np.array_equal(B[i], ref), f"multi-row batch row {i} != per-row reference"
        assert abs(B[i].sum() - seats) < 1e-9


# --------------------------------------------------------------------------------------------- GPU parity
@requires_gpu
def test_gpu_vs_cpu_130_fixture_parity_within_1e7():
    """Amendment A-GPU-1: max abs dP <= 1e-7 over the canonical 130 fixtures; seat sums preserved."""
    cg = _register_gpu()
    fx = fixtures()
    _cpu()
    ref = [np.asarray(cm.pl_win_probs(w, s, method="auto"), float) for n, s, d, w in fx]
    cm.set_pl_backend("gpu")
    assert cm.pl_backend() == "gpu"
    rows = []
    for k, (n, s, d, w) in enumerate(fx):
        p = np.asarray(cm.pl_win_probs_batch(np.asarray([w]), s, method="auto")[0], float)
        delta = float(np.max(np.abs(p - ref[k])))
        rows.append((delta, n, s, d))
        assert abs(float(p.sum()) - min(s, n)) < 1e-6, f"GPU seat-sum violation n={n} seats={s}"
    cm.set_pl_backend("cpu")
    worst = max(rows)
    assert worst[0] <= TOL, f"GPU-vs-CPU max abs dP {worst[0]:.3e} > 1e-7 at n={worst[1]} seats={worst[2]} disp={worst[3]}"
    stats = cm.pl_stats()
    gpu_stats = stats.get("gpu") or {}
    assert stats.get("batch_rows", 0) > 0 or gpu_stats.get("gpu_calls", 0) > 0, f"GPU path not exercised: {stats}" 


@requires_gpu
def test_gpu_boundary_cases_within_1e7():
    """Boundary/capacity cases on the GPU path: same support/seat-sum and <= 1e-7 vs CPU."""
    _register_gpu()
    cases = []
    for n in (1, 2, 12, 20, 21):
        for seats in sorted({0, 1, max(n - 1, 0), n}):
            cases.append((n, seats, np.ones(n)))
    cases += [(20, 1, np.array([1e-200] * 10 + [1e200] * 10)),
              (21, 10, np.geomspace(1e-12, 1e12, 21))]
    _cpu()
    refs = [np.asarray(cm.pl_win_probs(w, s), float) for n, s, w in cases]
    cm.set_pl_backend("gpu")
    worst = 0.0
    for (n, s, w), ref in zip(cases, refs):
        p = np.asarray(cm.pl_win_probs_batch(np.asarray([w]), s)[0], float)
        assert np.all(np.isfinite(p))
        assert abs(float(p.sum()) - min(s, n)) < 1e-6
        worst = max(worst, float(np.max(np.abs(p - ref))))
    cm.set_pl_backend("cpu")
    assert worst <= TOL, f"GPU boundary max abs dP {worst:.3e} > 1e-7"


@requires_gpu
def test_gpu_realize_flips_are_reported_not_failed():
    """Discrete winners may flip on ties/near-ties; collect the count for the record (no failure)."""
    _register_gpu()
    fx = _subset(step=10)                  # 13 fixtures: cheap on GPU
    uniforms = [np.random.default_rng(5000 + i).random(n) for i, (n, s, d, w) in enumerate(fx)]
    _cpu()
    cpu_masks = [np.asarray(cm.pl_realize(w, s, u)) for (n, s, d, w), u in zip(fx, uniforms)]
    cm.set_pl_backend("gpu")
    flips = 0
    for (n, s, d, w), u, ref in zip(fx, uniforms, cpu_masks):
        got = np.asarray(cm.pl_realize(w, s, u))
        assert got.shape == ref.shape and int(got.sum()) == int(ref.sum()) == min(s, n)
        flips += int(np.sum(got != ref))
    cm.set_pl_backend("cpu")
    assert flips >= 0                     # reported, not failed: equivalence is on P, not realisations
    print(f"discrete winner flips CPU-vs-GPU (reported, not failed): {flips}")
