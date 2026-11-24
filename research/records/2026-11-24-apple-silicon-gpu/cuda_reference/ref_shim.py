"""RNG adapter for the CUDA reference run (CUDA ground truth for the Apple port).

Why this exists
---------------
The upstream suite scripts call ``cp.random.default_rng(seed).normal(...)``.
On the T4's CuPy 13.6.0 that call does not work as the suite's pre-registration
assumed:
  * ``cupy.random.default_rng`` returns a ``cupy.random._generator_api.Generator``
    backed by **XORWOW** (its ``bit_generator`` is XORWOW), not Philox4x32-10;
  * that Generator object has **no ``normal`` method** in this install
    (``AttributeError: 'Generator' object has no attribute 'normal'``);
  * ``cupy.random`` exposes **no Philox** at all.

So the upstream scripts cannot run unmodified on this machine
(``results/run_as_shipped.log`` preserves both tracebacks).

To get a CUDA ground truth *without editing the upstream scripts*, this adapter
replaces exactly that one call: ``cp.random.default_rng(seed)`` returns a small
object backed by NumPy's Philox4x32-10 Generator -- which is the data-stream
mapping the Apple port declares in its addendum -- and hands back CuPy device
arrays via ``cp.asarray``. Everything else (kernel, launch config, scalars,
per-year loop, statistics) is the upstream code, unmodified, on the GPU.

What this isolates
------------------
Because the port and this CUDA reference use the *same* NumPy-Philox data
arrays, an end-to-end agreement tests the **CUDA kernel vs its transcribed
NumPy/MLX implementation**, not the data-generation stream. That is the gap the
port's PRE_REGISTRATION declared unclosable on the Mac; the T4 closes it.
"""
import numpy as np
import cupy as cp


class _NpPhiloxGenerator:
    """Minimal stand-in for the suite's ``cp.random.default_rng(seed)``."""

    def __init__(self, seed=None):
        self.seed = int(seed) if seed is not None else None
        self._g = np.random.Generator(np.random.Philox(self.seed))

    def normal(self, loc=0.0, scale=1.0, size=None, dtype=None):
        arr = self._g.normal(loc, scale, size=size)
        dt = np.dtype(dtype).type if dtype is not None else np.float64
        return cp.asarray(arr.astype(dt, copy=False))

    def standard_normal(self, size=None, dtype=None):
        arr = self._g.standard_normal(size=size)
        dt = np.dtype(dtype).type if dtype is not None else np.float64
        return cp.asarray(arr.astype(dt, copy=False))


def install():
    cp.random.default_rng = _NpPhiloxGenerator


install()
