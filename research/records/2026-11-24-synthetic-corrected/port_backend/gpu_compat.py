"""Minimal CuPy compatibility layer for Apple Silicon (M1/M2/M3), backed by MLX or NumPy.

This is NOT a CuPy reimplementation and NOT a CUDA emulator. It exposes exactly the CuPy subset used by
the `unified_gpu_suite_2026_11_24` scripts (see PRE_REGISTRATION.md §1):

    cp.float32, cp.int32, cp.empty, cp.asnumpy, cp.exp, cp.clip,
    cp.random.default_rng(seed).normal(...), cp.cuda.Stream.null.synchronize(),
    cp.RawModule(code).get_function("sim_step")

`RawModule` cannot execute CUDA C on Apple Silicon. It is supported ONLY for the suite's one kernel
(`sim_step`, recognised by its source fingerprint); that kernel is transcribed line-by-line in
`kernels_np_mlx.py`. Any other kernel raises PortabilityError.

Backend selection (env APPLE_GPU_BACKEND): "mlx" (default if importable), "numpy"; "mps" is accepted and
dispatched through the NumPy path with a deprecation note if PyTorch is absent (documented in REPORT.md).
"""
import hashlib
import os
import sys

import numpy as np

__all__ = [
    "Array", "float32", "float64", "int32", "uint32", "uint64", "backend",
    "empty", "array", "asnumpy", "exp", "clip", "sqrt", "sum", "mean",
    "random", "cuda", "RawModule", "PortabilityError",
]

float32 = np.float32
float64 = np.float64
int32 = np.int32
uint32 = np.uint32
uint64 = np.uint64


class PortabilityError(RuntimeError):
    """Raised when the CuPy surface used cannot be ported (e.g. arbitrary RawModule CUDA C)."""


def _select_backend():
    req = os.environ.get("APPLE_GPU_BACKEND", "").strip().lower()
    if req in ("numpy", "cpu"):
        return "numpy", None
    if req in ("mlx", ""):
        try:
            import mlx.core as mx  # noqa: F401
            return "mlx", mx
        except Exception as exc:
            if req == "mlx":
                print(f"[gpu_compat] APPLE_GPU_BACKEND=mlx requested but MLX unavailable ({exc}); "
                      f"falling back to NumPy", file=sys.stderr)
            return "numpy", None
    if req in ("mps", "torch"):
        try:
            import torch
            if torch.backends.mps.is_available():
                return "mps", torch
        except Exception:
            pass
        print("[gpu_compat] PyTorch MPS requested but unavailable; falling back to NumPy", file=sys.stderr)
        return "numpy", None
    raise ValueError(f"unknown APPLE_GPU_BACKEND={req!r}")


BACKEND, _MX = _select_backend()


def backend():
    return BACKEND


class Array:
    """Thin host-side wrapper around a backend array (MLX/PyTorch/NumPy)."""

    __slots__ = ("data", "backend")

    def __init__(self, data, backend=None):
        self.backend = backend or BACKEND
        self.data = data

    @property
    def shape(self):
        return tuple(self.data.shape)

    @property
    def dtype(self):
        return self.data.dtype

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"gpu_compat.Array(backend={self.backend}, shape={self.shape}, dtype={self.dtype})"


def _as_numpy(x):
    if isinstance(x, Array):
        x = x.data
    if BACKEND == "mlx":
        import mlx.core as mx
        if isinstance(x, mx.array):
            return np.array(x)
    if BACKEND == "mps":
        import torch
        if isinstance(x, torch.Tensor):
            return x.detach().cpu().numpy()
    return np.asarray(x)


def _wrap(np_arr, dtype=None):
    """Host numpy -> backend Array (float32 by default when dtype requested)."""
    a = np.asarray(np_arr)
    if dtype is not None:
        a = a.astype(dtype, copy=False)
    if BACKEND == "mlx":
        import mlx.core as mx
        md = {np.float32: mx.float32, np.float64: mx.float64, np.int32: mx.int32,
              np.uint32: mx.uint32, np.uint64: mx.uint64, np.bool_: mx.bool_}.get(a.dtype, None)
        arr = mx.array(a, dtype=md) if md is not None else mx.array(a)
        mx.eval(arr)
        return Array(arr, "mlx")
    if BACKEND == "mps":
        import torch
        return Array(torch.as_tensor(np.ascontiguousarray(a)), "mps")
    return Array(a, "numpy")


def asnumpy(x):
    """CuPy-style `cp.asnumpy`: materialise a backend array as a host NumPy array."""
    if isinstance(x, Array):
        return _as_numpy(x)
    return _as_numpy(x)


def empty(size, dtype=np.float32):
    if isinstance(size, int):
        shape = (size,)
    else:
        shape = tuple(size)
    if BACKEND == "mlx":
        import mlx.core as mx
        dt = {np.float32: mx.float32, np.float64: mx.float64, np.int32: mx.int32,
              np.uint32: mx.uint32, np.uint64: mx.uint64}.get(np.dtype(dtype), mx.float32)
        arr = mx.zeros(shape, dtype=dt)   # zeros, not uninitialised: deterministic before the kernel fills it
        mx.eval(arr)
        return Array(arr, "mlx")
    return Array(np.zeros(shape, dtype=dtype), "numpy")


def array(obj, dtype=None):
    return _wrap(obj, dtype)


def exp(x):
    a = _wrap(_as_numpy(x))
    if BACKEND == "mlx":
        import mlx.core as mx
        out = mx.exp(a.data)
        mx.eval(out)
        return Array(out, "mlx")
    return Array(np.exp(a.data), "numpy")


def clip(x, a_min, a_max):
    a = _wrap(_as_numpy(x))
    if BACKEND == "mlx":
        import mlx.core as mx
        out = mx.clip(a.data, a_min, a_max)
        mx.eval(out)
        return Array(out, "mlx")
    return Array(np.clip(a.data, a_min, a_max), "numpy")


def sqrt(x):
    a = _wrap(_as_numpy(x))
    if BACKEND == "mlx":
        import mlx.core as mx
        out = mx.sqrt(a.data)
        mx.eval(out)
        return Array(out, "mlx")
    return Array(np.sqrt(a.data), "numpy")


def sum(x):
    return float(np.sum(_as_numpy(x)))


def mean(x):
    return float(np.mean(_as_numpy(x)))


class _Generator:
    """CuPy `default_rng(seed)` mapping: NumPy Philox generator (documented assumption)."""

    def __init__(self, seed):
        self.seed = int(seed)
        self._g = np.random.Generator(np.random.Philox(self.seed))

    def normal(self, loc=0.0, scale=1.0, size=None, dtype=np.float32):
        arr = self._g.normal(loc, scale, size=size)
        return _wrap(arr, dtype)

    def uniform(self, low=0.0, high=1.0, size=None, dtype=np.float32):
        arr = self._g.uniform(low, high, size=size)
        return _wrap(arr, dtype)


class _RandomModule:
    @staticmethod
    def default_rng(seed=None):
        return _Generator(0 if seed is None else seed)


random = _RandomModule()


class _Stream:
    def __init__(self, name):
        self.name = name

    def synchronize(self):
        if BACKEND == "mlx":
            import mlx.core as mx
            mx.synchronize()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _StreamEnum:
    null = _Stream("null")


class _Cuda:
    Stream = _StreamEnum


cuda = _Cuda()


# ---------------------------------------------------------------- RawModule
_SUITE_KERNEL_MARKERS = ("__global__ void sim_step", "philox", "uni_from", "tutor_out", "y_hh_out")
_SUITE_KERNEL_NAME = "sim_step"


class _KernelFn:
    """Callable returned by RawModule.get_function for the recognised suite kernel."""

    def __init__(self, name, fingerprint):
        self.name = name
        self.fingerprint = fingerprint

    def __call__(self, grid, block, args):
        if self.name != _SUITE_KERNEL_NAME:
            raise PortabilityError(
                f"kernel {self.name!r} is not supported by the Apple Silicon port; only "
                f"{_SUITE_KERNEL_NAME!r} is transcribed (see REPORT.md)")
        from kernels_np_mlx import run_sim_step
        return run_sim_step(BACKEND, args)


class RawModule:
    """CuPy RawModule subset: recognises the suite kernel, refuses arbitrary CUDA C."""

    def __init__(self, code, *a, **k):
        self.code = code
        self.fingerprint = hashlib.sha256(code.encode("utf-8")).hexdigest()[:16]

    def get_function(self, name):
        if name != _SUITE_KERNEL_NAME:
            raise PortabilityError(
                f"get_function({name!r}): the Apple Silicon port supports only the suite kernel "
                f"{_SUITE_KERNEL_NAME!r}; CUDA C cannot be compiled on macOS")
        if not all(m in self.code for m in _SUITE_KERNEL_MARKERS):
            raise PortabilityError(
                "RawModule source does not match the recognised `unified_gpu_suite` sim_step kernel "
                "(source fingerprint mismatch); arbitrary CUDA C cannot be ported to Apple Silicon. "
                "The source would need a hand-written NumPy/MLX transcription.")
        global LAST_KERNEL_FINGERPRINT
        LAST_KERNEL_FINGERPRINT = self.fingerprint
        return _KernelFn(name, self.fingerprint)


LAST_KERNEL_FINGERPRINT = None
