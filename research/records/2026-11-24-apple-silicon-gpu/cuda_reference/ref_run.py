"""CUDA reference driver for the Apple Silicon port.

Runs the upstream suite scripts *unmodified* under CuPy on the T4, with the one
RNG call adapted by ref_shim.py (see that file for the full rationale). Writes:
  results/cuda_smoke_exp1.json
  results/cuda_exp3_small.json
  results/cuda_manifest.json   (env + hashes + timings + RNG probe)
"""
import hashlib
import json
import os
import platform
import runpy
import socket
import subprocess
import sys
import time

import numpy as np
import cupy as cp

import ref_shim  # noqa: F401  (installs the RNG adapter on import)

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT_DIR = os.path.join(HERE, "scripts")
RESULTS = os.path.join(HERE, "results")
os.makedirs(RESULTS, exist_ok=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def nvidia_smi():
    try:
        return subprocess.run(["nvidia-smi"], capture_output=True, text=True, timeout=30).stdout
    except Exception as e:  # pragma: no cover
        return f"nvidia-smi failed: {e!r}"


def pip_packages():
    try:
        out = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=freeze"],
            capture_output=True, text=True, timeout=60,
        ).stdout
        keep = ("cupy", "numpy", "pandas", "scipy", "statsmodels", "requests")
        return sorted(l for l in out.splitlines() if l.lower().startswith(keep))
    except Exception as e:  # pragma: no cover
        return [f"pip list failed: {e!r}"]


def rng_probe():
    """Document what the RNGs actually are (the pre-registration made a claim)."""
    out = {"cupy_version": cp.__version__, "numpy_version": np.__version__}
    try:
        g = cp.random.default_rng(20261125)
        out["cupy_default_rng_class"] = f"{type(g).__module__}.{type(g).__name__}"
        out["cupy_default_bit_generator"] = type(g.bit_generator).__name__
        out["cupy_has_normal"] = hasattr(g, "normal")
        out["cupy_has_standard_normal"] = hasattr(g, "standard_normal")
        out["cupy_has_philox"] = hasattr(cp.random, "Philox")
        out["cupy_xorwow_first8"] = [float(x) for x in cp.asnumpy(g.standard_normal(size=8))]
    except Exception as e:  # pragma: no cover
        out["cupy_probe_error"] = f"{type(e).__name__}: {e}"
    out["numpy_default_rng_first8"] = [
        float(x) for x in np.random.default_rng(20261125).standard_normal(size=8)
    ]
    out["numpy_philox_first8"] = [
        float(x) for x in np.random.Generator(np.random.Philox(20261125)).normal(size=8)
    ]
    # The port maps CuPy default_rng -> NumPy Philox; these two must therefore be
    # the *same* stream for port/reference comparability. They are recorded, not
    # asserted, because CuPy has no Philox here.
    out["note"] = (
        "CuPy 13.6 default_rng is XORWOW and lacks .normal; cupy.random has no Philox. "
        "The port's data stream is NumPy Philox, so the CUDA reference uses ref_shim "
        "(NumPy Philox -> cp.asarray) to hold the data stream fixed while the kernel runs on CUDA."
    )
    return out


def run_script(name, argv):
    script = os.path.join(SCRIPT_DIR, name)
    old_argv = sys.argv
    old_path = list(sys.path)
    sys.argv = [script] + argv
    sys.path.insert(0, SCRIPT_DIR)
    t0 = time.perf_counter()
    status = "ok"
    err = None
    try:
        runpy.run_path(script, run_name="__main__")
    except BaseException as e:  # preserve failures
        status = "failed"
        err = f"{type(e).__name__}: {e}"
    finally:
        wall = time.perf_counter() - t0
        sys.argv = old_argv
        sys.path[:] = old_path
    return {"status": status, "error": err, "wall_s": round(wall, 3)}


def main():
    manifest = {
        "captured_at_local": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python": sys.version,
        "gpu": nvidia_smi(),
        "pip": pip_packages(),
        "script_sha256": {
            f: sha256(os.path.join(SCRIPT_DIR, f))
            for f in sorted(os.listdir(SCRIPT_DIR)) if f.endswith(".py")
        },
        "rng_probe": rng_probe(),
        "runs": {},
    }
    print("=== CUDA reference capture ===")
    print("cupy", cp.__version__, "| numpy", np.__version__)

    print("--- exp1 --smoke ---")
    manifest["runs"]["exp1_smoke"] = run_script(
        "exp1_unified_gpu_abm.py",
        ["--smoke", "--out", os.path.join(RESULTS, "cuda_smoke_exp1.json")],
    )
    print(json.dumps(manifest["runs"]["exp1_smoke"]))

    print("--- exp3 --draws 20 --batch-n 2000 ---")
    manifest["runs"]["exp3_small"] = run_script(
        "exp3_rejection_abc_realdata.py",
        ["--draws", "20", "--batch-n", "2000",
         "--out", os.path.join(RESULTS, "cuda_exp3_small.json")],
    )
    print(json.dumps(manifest["runs"]["exp3_small"]))

    # hashes of the outputs, written after the runs
    manifest["output_sha256"] = {
        f: sha256(os.path.join(RESULTS, f))
        for f in ("cuda_smoke_exp1.json", "cuda_exp3_small.json")
        if os.path.exists(os.path.join(RESULTS, f))
    }
    manifest["finished_at_local"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with open(os.path.join(RESULTS, "cuda_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print("=== done; manifest written ===")


if __name__ == "__main__":
    main()
