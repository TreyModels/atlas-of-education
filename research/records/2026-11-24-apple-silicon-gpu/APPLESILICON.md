# Running the unified GPU suite on Apple Silicon (M1/M2/M3)

This directory contains a **minimal CuPy compatibility layer** that lets
`unified_gpu_suite_2026_11_24` run on an Apple Silicon Mac without CUDA, **without editing the upstream
scripts**. It is a portability layer, not a CUDA emulator and not a research re-run.

## What you need

- macOS 13+ on Apple Silicon (tested: M1, macOS 26.6.2, arm64).
- Python 3.10–3.13 with `numpy`, `pandas`, `requests`, `scikit-learn`, `statsmodels`, and **`mlx`**
  (preferred backend). The tested environment is pinned in `requirements.txt` (Python 3.10.2, mlx 0.32.4,
  numpy 2.2.6); reproducible interpreter and provenance are in `env_provenance.json`. The committed results
  were produced under `/private/tmp/apple_venv` and reproduced bit-identically under the durable
  `apple-venv310`.
- No CUDA, no CuPy, no GPU toolkit. PyTorch is optional; if installed with MPS it is used only if
  `APPLE_GPU_BACKEND=torch`/`mps` and the layer falls back to NumPy when unavailable.

## Quick start

```bash
cd research/records/2026-11-24-apple-silicon-gpu
APPLE_PY=/path/to/venv/bin/python APPLE_GPU_BACKEND=mlx ./run_apple.sh smoke      # ~4 s
APPLE_PY=/path/to/venv/bin/python APPLE_GPU_BACKEND=numpy ./run_apple.sh smoke    # NumPy fallback
APPLE_PY=/path/to/venv/bin/python APPLE_GPU_BACKEND=mlx ./run_apple.sh production # full config
```

`run_apple.sh` puts this directory, `./shim` and the suite's `scripts/` on `PYTHONPATH`, so
`import cupy as cp` inside the upstream scripts resolves to `shim/cupy/__init__.py` → `gpu_compat.py`.
Nothing in `suite/unified_gpu_suite/` is modified; the suite is kept byte-for-byte as delivered.

## How it works (and what it cannot do)

| CuPy API used by the suite | Apple Silicon implementation |
|---|---|
| `cp.float32`, `cp.int32` | NumPy dtype constants (backend-neutral) |
| `cp.empty(size, dtype)` | backend zeros (MLX `mx.zeros` / `np.zeros`) wrapped in `Array` |
| `cp.exp`, `cp.clip` | `mx.exp`/`mx.clip` or `np.exp`/`np.clip` |
| `cp.asnumpy` | `np.array(mx.array)` / NumPy view |
| `cp.random.default_rng(seed).normal(...)` | NumPy `Generator(Philox(seed))` (documented mapping; see REPORT §RNG) |
| `cp.cuda.Stream.null.synchronize()` | no-op / `mx.synchronize()` |
| `cp.RawModule(code).get_function("sim_step")` | **only** the suite's `sim_step` kernel is transcribed (NumPy + MLX) |

**The hard limit:** `cp.RawModule` compiles CUDA C. CUDA C cannot be compiled or run on macOS. The layer
recognises the suite's one kernel by source fingerprint and dispatches to a line-by-line transcription in
`kernels_np_mlx.py`; **any other CUDA kernel raises `PortabilityError`**. To port a new kernel you must add a
transcription (see "Adding a kernel" below); there is no automatic CUDA→MLX translator.

## Adding a kernel

1. Add a function `run_<name>(backend, args)` to `kernels_np_mlx.py` implementing the C semantics for both
   backends (or a host-vectorised NumPy version and an MLX version).
2. Extend `gpu_compat.RawModule.get_function` to recognise the new kernel name and source markers; raise
   `PortabilityError` for everything else.
3. Add a fixed-seed probe to `tests/` and extend `tests/run_equivalence.py` with the same tolerances
   (integer state exact; float32 continuous `max_abs ≤ 1e-5`). Keep the upstream script unmodified.

## Equivalence and honesty

- `tests/run_equivalence.py` compares the NumPy reference and the MLX backend on the same fixed-seed kernel:
  integer states must match exactly; continuous arrays are checked against `1e-5` abs / `1e-4` rel
  (float32 rounding). `results/equivalence.json` records the outcome.
- **The kernel transcription is verified against the real CUDA kernel.** A T4 capture of 10 unmodified CUDA
  `sim_step` launches (same inputs) is replayed through both transcriptions by
  `tests/verify_cuda_kernel.py`: **0 integer mismatches, max abs 3.815e-6, max rel 1.192e-7** on 10 launches
  x 2 backends (`results/cuda_vs_transcription.json`).
- **CUDA *data-stream* equivalence is not claimed.** Under CuPy 13.6 the real `cp.random.default_rng(seed)` is
  **XORWOW** and has **no `.normal`** (the upstream scripts fail as shipped on that CuPy; failure preserved in
  `cuda_reference/run_as_shipped.log`). The port defines the data stream as NumPy Philox, so a CUDA run and a
  port run at the same seed consume different data draws. Same-seed CUDA-vs-port *end-to-end* numbers are
  therefore not comparable; the kernel-level verification above is.
- Outputs from this layer are labelled **PORT-SMOKE / PORT-PRODUCTION** and are not research results. The
  suite's own audit (`research/suite-lit-review-2026-11-24` @ `4649cae`, `AUDIT.md` §9) shows the shipped exp2
  implements no H1 test and no zero-signal control (H4); the port's exp2/exp3 numbers are construction-implied
  artefacts, not evidence.

## Files

`gpu_compat.py` (CuPy subset + RawModule dispatch), `kernels_np_mlx.py` (kernel transcription),
`shim/cupy/__init__.py` (import shim), `tests/` (equivalence, components, projection, **verify_cuda_kernel**),
`run_apple.sh` (runner), `requirements.txt` + `env_provenance.json` (pinned, durable environment),
`cuda_reference/` (real CUDA kernel ground truth + as-shipped failure), `results/` (evidence), `REPORT.md`
(full report), `PRE_REGISTRATION.md` (scope and tolerances fixed before coding) and
`ADDENDUM_2026-11-24_env.md` (environment and RNG facts, corrections).
