"""Optional torch/CUDA backend for the deterministic top-K Plackett-Luce quadrature.

Gate-1 amendment **A-GPU-1** (approved 2026-11-25): the GPU path is numerically equivalent to
the float32 CPU reference within **max abs diff <= 1e-7** and is declared *not bit-identical*
(measured: 2.56e-8 on one HK run's 405 real call shapes, 5.32e-8 worst over the 130 fixtures).
Allowed for **gate-grid / sensitivity runs only**. Paper B's preregistered primary computations
must run on the CPU path. See ``docs/gpu/GATE1_REPORT.md`` and ``docs/gpu/EQUIVALENCE.md``.

Design
------
* The reference's float64 preprocessing (weight normalisation, Simpson grid, ``expm1``/``exp``
  then cast to float32) is done **in NumPy, identically to the CPU path**, and handed to the GPU.
  Only the float32 DP / scan / contraction runs on the GPU, so the declared deviation comes from
  exactly one reordered float32 reduction — not from changed inputs.
* The DP is a ~300-step chain of tiny ops. Eager torch dispatch costs ~15 ms/call (measured) and
  makes the port a thin 3.4x; the same chain captured once per shape as a **CUDA graph** and
  replayed costs ~1 ms and gives 19.8x. Graphs are therefore mandatory.
* Batch dimension = independent calls (the engine's 9-point tutoring grid). Elements never
  interact, so per-element arithmetic is identical to a single call.
* Engines are cached by ``(n, d, below, M1, B)`` with a small LRU. ``M1`` is rounded up to a
  multiple of 16 so a run does not allocate a graph per Simpson-node count.

Public API (called from :mod:`eduengine.contest_math`, never from engine modules directly):
``get_backend()``, ``set_backend(name)``, ``available()``, ``dp_batch(...)``.
"""

from __future__ import annotations

import os
import time as _time

import numpy as np

__all__ = ["available", "warmup", "get_backend", "set_backend", "dp_batch",
           "B_MAX", "DEVIATION_BOUND"]

#: Declared equivalence bound of the GPU backend (amendment A-GPU-1), max abs diff vs CPU.
DEVIATION_BOUND = 1e-7
#: Largest batch dimension we will form in one graph.
B_MAX = 16
#: Minimum width of a captured graph: single calls are padded up to this so that one engine
#: (one capture) serves both the tutoring grid and the engine's single gate calls.
B_GRAPH_MIN = 9
#: Maximum number of cached replay engines (each holds a CUDA graph + static buffers).
_ENGINE_CACHE_MAX = 12
#: Round the padded Simpson-node axis up to a multiple of this, to bound graph/engine variants.
_M1_QUANTUM = 32
#: Hard cap mirroring ``contest_math._QUAD_MAX_NODES``.
_M1_CAP = 1601

_BACKEND = os.environ.get("ATLAS_PL_BACKEND", "cpu").strip().lower() or "cpu"
_ENGINES = {}
_TORCH = None
_STATS = {"gpu_batches": 0, "gpu_calls": 0, "engine_builds": 0,
          "gpu_s": 0.0, "feed_s": 0.0, "replay_s": 0.0, "capture_s": 0.0}


def _torch():
    global _TORCH
    if _TORCH is None:
        import torch  # noqa: F401  (lazy: CPU-only deployments never import torch)
        torch.backends.cuda.matmul.allow_tf32 = False
        _TORCH = torch
    return _TORCH


def available():
    """True iff torch is importable and a CUDA device is visible. Never raises."""
    try:
        return bool(_torch().cuda.is_available())
    except Exception:
        return False


def warmup():
    """Pay the one-time torch import / CUDA context cost now, not inside a timed first call."""
    t = _torch()
    if not t.cuda.is_available():
        return False
    t.cuda.init()
    t.zeros(1, device="cuda").add_(1.0)
    t.cuda.synchronize()
    return True


def get_backend():
    return _BACKEND


def set_backend(name):
    """Select ``"cpu"`` (default, bit-identical reference path) or ``"gpu"`` (amendment A-GPU-1)."""
    global _BACKEND
    name = str(name).strip().lower()
    if name not in ("cpu", "gpu"):
        raise ValueError("backend must be 'cpu' or 'gpu'; got %r" % (name,))
    if name == "gpu" and not available():
        raise RuntimeError(
            "GPU backend requested but torch/CUDA is unavailable; refusing to change backend. "
            "Install torch with CUDA support and check torch.cuda.is_available()."
        )
    _BACKEND = name
    return _BACKEND


def stats():
    return dict(_STATS)


class _ReplayEngine:
    """Static-buffer batched quadrature with one captured CUDA graph per shape."""

    def __init__(self, n, d, below, sign, offc, M1, B, use_graph=True):
        torch = _torch()
        self.torch = torch
        self.n, self.d, self.B, self.M1 = n, d, B, M1
        self.sign, self.offc = sign, offc
        dev = "cuda"
        f64 = torch.float64
        f32 = torch.float32
        self.WN = torch.zeros((B, n), dtype=f64, device=dev)
        self.T = torch.zeros((B, M1), dtype=f64, device=dev)
        self.SW = torch.zeros((B, M1), dtype=f64, device=dev)
        self.PB = torch.zeros((B, n, M1), dtype=f32, device=dev)
        self.QA = torch.ones((B, n, M1), dtype=f32, device=dev)
        self.Suf = torch.zeros((B, n + 1, d + 1, M1), dtype=f32, device=dev)
        self.PreA = torch.zeros((B, d + 1, M1), dtype=f32, device=dev)
        self.PreB = torch.zeros((B, d + 1, M1), dtype=f32, device=dev)
        self.out = torch.empty((B, n), dtype=f64, device=dev)
        self.f_stay, self.f_inc = (self.QA, self.PB) if below else (self.PB, self.QA)
        self.use_graph = bool(use_graph)
        if self.use_graph:
            self.graph = torch.cuda.CUDAGraph()
            side = torch.cuda.Stream()
            side.wait_stream(torch.cuda.current_stream())
            with torch.cuda.stream(side):
                for _ in range(2):
                    self._run()
            torch.cuda.current_stream().wait_stream(side)
            torch.cuda.synchronize()
            with torch.cuda.graph(self.graph):
                self._run()
        else:
            self.graph = None

    def _run(self):
        n, d, M1 = self.n, self.d, self.M1
        torch = self.torch
        f_stay, f_inc = self.f_stay, self.f_inc
        Suf = self.Suf
        Suf.zero_()
        Suf[:, n, 0, :] = 1.0
        for i in range(n - 1, -1, -1):                      # suffix Poisson-binomial DP
            cur = Suf[:, i + 1]
            nxt = Suf[:, i]
            torch.mul(cur, f_stay[:, i, None, :], out=nxt)
            nxt[:, 1:, :] += f_inc[:, i, None, :] * cur[:, :-1, :]
        for a in range(1, d + 1):                           # sequential scan (reference order)
            Suf[:, :, a, :] += Suf[:, :, a - 1, :]
        Pre, tmp = self.PreA, self.PreB
        Pre.zero_()
        Pre[:, 0, :] = 1.0
        out = self.out
        for i in range(n):                                  # prefix DP + contraction
            tail = (Pre * Suf[:, i + 1, :, :].flip(1)).sum(dim=1)          # float32
            G = torch.clamp(self.offc + self.sign * tail.double(), 0.0, 1.0)
            kernel = self.WN[:, i:i + 1] * self.T * self.QA[:, i, :].double()
            out[:, i] = (self.SW * kernel * G).sum(dim=1)
            torch.mul(Pre, f_stay[:, i, None, :], out=tmp)
            tmp[:, 1:, :] += f_inc[:, i, None, :] * Pre[:, :-1, :]
            Pre, tmp = tmp, Pre

    def feed(self, WN, T, SW, PB, QA):
        """Bulk-copy fully padded host arrays into the static graph buffers (5 copies, not 5*B)."""
        self.WN.copy_(self.torch.from_numpy(np.ascontiguousarray(WN)))
        self.T.copy_(self.torch.from_numpy(np.ascontiguousarray(T)))
        self.SW.copy_(self.torch.from_numpy(np.ascontiguousarray(SW)))
        self.PB.copy_(self.torch.from_numpy(np.ascontiguousarray(PB)))
        self.QA.copy_(self.torch.from_numpy(np.ascontiguousarray(QA)))

    def replay(self):
        if self.use_graph:
            self.graph.replay()
        else:
            self._run()                    # eager: same arithmetic, no graph capture
        return self.out.cpu().numpy()


def _get_engine(key, n, d, below, sign, offc, M1, B, use_graph):
    eng = _ENGINES.get(key)
    if eng is None:
        if len(_ENGINES) >= _ENGINE_CACHE_MAX:
            _ENGINES.pop(next(iter(_ENGINES)))
        _t0 = _time.perf_counter()
        eng = _ReplayEngine(n, d, below, sign, offc, M1, B, use_graph)
        _ENGINES[key] = eng
        _STATS["engine_builds"] += 1
        _STATS["capture_s"] += _time.perf_counter() - _t0
    return eng


def dp_batch(wns, PB_list, QA_list, T_list, SW_list, n, d, below, sign, offc, M1,
             use_graph=True):
    """Batched float32 quadrature DP on the GPU. Returns ``(B, n)`` float64 probabilities.

    ``wns`` is float64 ``(B, n)``; ``PB_list``/``QA_list`` are the reference's float32 DP
    factors ``(-expm1(-w t), exp(-w t))`` per call; ``T_list``/``SW_list`` the Simpson nodes and
    weights (float64, length ``m+1`` <= M1; padded with zeros). The caller must renormalise to
    the seat-sum invariant afterwards, exactly as the CPU path does.
    """
    torch = _torch()
    B = len(wns)
    Bg = B if B >= B_GRAPH_MIN else B_GRAPH_MIN     # pad narrow calls up to one graph width
    M1q = min(((M1 + _M1_QUANTUM - 1) // _M1_QUANTUM) * _M1_QUANTUM, _M1_CAP)
    if M1q < M1:
        M1q = M1
    key = (n, d, below, M1q, Bg, bool(use_graph))
    eng = _get_engine(key, n, d, below, sign, offc, M1q, Bg, bool(use_graph))
    # pad each call's arrays to M1q (zeros for t/sw/PB, ones for QA == the t=0 limit)
    WN = np.zeros((B, n), dtype=np.float64)
    T = np.zeros((B, M1q), dtype=np.float64)
    SW = np.zeros((B, M1q), dtype=np.float64)
    PBP = np.zeros((B, n, M1q), dtype=np.float32)
    QAP = np.ones((B, n, M1q), dtype=np.float32)
    for b in range(B):
        m1 = len(T_list[b])
        WN[b] = wns[b]
        T[b, :m1] = T_list[b]
        SW[b, :m1] = SW_list[b]
        PBP[b, :, :m1] = PB_list[b]
        QAP[b, :, :m1] = QA_list[b]
    _t0 = _time.perf_counter()
    if Bg > B:                                      # repeat row 0 into the padded graph lanes
        r = Bg - B
        WN = np.vstack([WN, np.repeat(WN[:1], r, axis=0)])
        T = np.vstack([T, np.repeat(T[:1], r, axis=0)])
        SW = np.vstack([SW, np.repeat(SW[:1], r, axis=0)])
        PBP = np.concatenate([PBP, np.repeat(PBP[:1], r, axis=0)], axis=0)
        QAP = np.concatenate([QAP, np.repeat(QAP[:1], r, axis=0)], axis=0)
    eng.feed(WN, T, SW, PBP, QAP)
    _t1 = _time.perf_counter()
    out = eng.replay()
    _STATS["feed_s"] += _t1 - _t0
    _STATS["replay_s"] += _time.perf_counter() - _t1
    _STATS["gpu_batches"] += 1
    _STATS["gpu_calls"] += B
    return out[:B]
