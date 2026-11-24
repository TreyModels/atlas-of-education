"""CuPy import shim for the Apple Silicon port.

Placed ahead of site-packages on PYTHONPATH by `run_apple.sh`, this package satisfies `import cupy as cp` in
the upstream scripts without editing them. It re-exports the minimal CuPy subset implemented in
`gpu_compat.py` (MLX or NumPy backend). The real CuPy is not imported; CUDA is unavailable on macOS.
"""
import os
import sys

_RECORD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _RECORD not in sys.path:
    sys.path.insert(0, _RECORD)

import gpu_compat as _gc
from gpu_compat import (Array, asnumpy, array, clip, empty, exp, mean, sqrt, sum,  # noqa: F401
                        float32, float64, int32, uint32, uint64,
                        RawModule, PortabilityError, backend)

random = _gc.random
cuda = _gc.cuda
