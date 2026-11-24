# PRE-REGISTRATION — CUDA → Apple Silicon port of the unified GPU suite

**Task:** task-50. **Branch:** `research/apple-silicon-gpu-2026-11-24`. **Record:**
`research/records/2026-11-24-apple-silicon-gpu/`. **Written before the compatibility layer was coded and
before any suite run.** Machine: Apple M1 (arm64), macOS 26.6.2. This is a **portability job, not a research
claim**: no output of this port is to be reported as a finding, and the ported suite's numbers are not
comparable to CUDA-run numbers unless the RNG mapping below says they are.

## 1. Exact CuPy API surface used by the suite (from `grep`, not assumption)

`cp.RawModule` (2 uses), `.get_function("sim_step")` (2), `cp.random.default_rng(seed)` (2) with
`.normal(loc, scale, size=, dtype=)` (2), `cp.exp` (2), `cp.clip` (2), `cp.empty(size, dtype=)` (10),
`cp.asnumpy` (6), `cp.cuda.Stream.null.synchronize()` (2), dtype constants `cp.float32` (10), `cp.int32`
(4). No `cp.array`, `cp.zeros`, `cp.arange`, arithmetic operators on CuPy arrays, indexing, reductions or
dtype casts appear in the two CuPy scripts. The CPU scripts (exp2, exp4) use only numpy/pandas/sklearn/
statsmodels and are run unchanged.

## 2. The hard blocker: `cp.RawModule` contains CUDA C

Both CuPy scripts compile an embedded CUDA C kernel (`sim_step`, in `KERNEL_SRC` in
`exp1_unified_gpu_abm.py`; exp3 imports the same source). CUDA C cannot be compiled or executed on Apple
Silicon (no CUDA runtime, no `nvcc`), and no compatibility layer can make `RawModule` execute arbitrary
CUDA. The port therefore does the only honest thing:

1. Provides the CuPy **array/RNG/stream** surface on Apple Silicon (`gpu_compat.py`), so anything written
   against that surface runs unmodified.
2. Provides a **kernel translation for the one specific kernel in this suite**. `gpu_compat.RawModule`
   recognises `sim_step` by source fingerprint/name and dispatches to a line-by-line transcription of the
   CUDA C in NumPy and in MLX. The transcribed semantics are the C source's; the scripts themselves are not
   edited. **Arbitrary `RawModule` code is not supported**: an unrecognised kernel raises
   `PortabilityError` with a clear message. This limitation is reported, not hidden.

Backend preference (one API, selected by `APPLE_GPU_BACKEND`): **MLX** (installed, tested) → **PyTorch MPS**
(if importable; not required) → **NumPy CPU fallback**. Backend actually used is recorded in every result.

## 3. RNG mapping (explicit; no silent stream substitution)

Two independent streams are involved.

**(a) Kernel uniforms (inside `sim_step`).** The CUDA C generates its own uniforms with Philox4x32-10
keyed on `(counter=(i, year, 0, 1), key=(seed0, seed1))`, then `uni = (raw + 0.5) / 2^32`. The port
transcribes that Philox routine exactly (uint32 multiply-high/low, 10 rounds with the same constants
`M0/M1/W0/W1`), vectorised over household index, and feeds the **same uniform bits to both backends**.
This is bit-identical to the C source by construction (the C source is the specification); it is **not**
independently verified against a CUDA GPU, which is unavailable here.

**(b) Data-generation stream (`cp.random.default_rng(seed).normal(...)`).** CuPy's `default_rng` is a
Philox4x32-10 bit generator with NumPy's `Generator` interface, and CuPy aims for NumPy stream compatibility.
The port maps it to NumPy's Philox generator: `numpy.random.Generator(numpy.random.Philox(seed))`, same
`normal` call, drawn in float64 and cast to float32 as the script requests. **This mapping is an explicit
assumption** (CuPy and NumPy use the same documented bit generator and Ziggurat normal), and it **cannot be
verified against CuPy on this machine** because CuPy/CUDA is unavailable. Therefore: the ported suite is
deterministic and reproducible on Apple Silicon, but **CUDA bit-equivalence is not claimed**. Any stream
difference between CuPy and this mapping is a data-generation difference, not a backend difference.

## 4. Equivalence test (fixed seed, same kernel, NumPy reference vs Apple backend)

Test design: for fixed seed/inputs, run the translated `sim_step` on the NumPy backend and on the MLX
backend; compare the five output arrays (state int32, tutor int32, learn float32, work float32, y_hh
float32). Tolerances declared in advance:

- **Integer state arrays (`state`, `tutor`): exact equality required; 0 differing households is the pass
  criterion.** Any mismatch is classified as a **real state change** (not float noise): report the count,
  the max |Δ| of the decision utilities if recoverable, and do not call the backends equivalent.
- **Continuous arrays (`learn`, `work_hrs`, `y_hh`): max absolute difference ≤ 1e-5 and max relative
  difference ≤ 1e-4**; differences at this level are float32 rounding/reduction-order noise. Anything above
  is a failure to be reported.
- **End-to-end exp1 smoke** (both backends): state-derived rows (`ger`, `study_work`, `work_only`,
  `hidden_work`, `cl_total`, `tutoring`) must agree **exactly** (they are means over identical int arrays);
  continuous rows (`enrolled_work_hrs_p90`, `tutor_income_corr`, `mean_learn`, `q_pub`) within the same
  tolerances.
- **End-to-end exp3 smoke** (small draws/batch, both backends): per-candidate `enr`, `cl`, `dist` within
  tolerances; accepted set and identifiability classification must agree.
- The **NumPy backend is the reference** (not the CUDA run). "Equivalent" below means *NumPy-port vs
  MLX-port of the same transcribed kernel*, not *port vs CUDA*.

## 5. Smoke path and decision to scale

Documented smoke path: `run_all.sh`'s first command shape, `exp1_unified_gpu_abm.py --smoke`, plus a small
`exp3` run (draws = 20, batch = 2,000) — both executed through the Apple shim and timed. Only if (i) the
equivalence tests above pass and (ii) the smoke wall time projects to a bounded production run will any
larger run be attempted. **Default decision: do not run the full production configuration** (250,000
households × 25 years × 5 DGPs × 3 arms × 20 seeds for exp1; 5,000 draws × 50,000 households for exp3) on
this laptop; the projection and the reason are reported instead.

## 6. Deliverables and rules

`gpu_compat.py` (CuPy subset: array wrappers, dtype constants, `exp`, `clip`, `empty`, `asnumpy`,
`random.default_rng`, `cuda.Stream`, `RawModule` kernel dispatch), `kernels_np_mlx.py` (transcribed kernel,
both backends), `shim/cupy/__init__.py` (import shim so upstream scripts run unmodified), `tests/`
(equivalence + RNG + shim tests), `run_apple.sh` (Apple runner), `REPORT.md`, `APPLESILICON.md`.
Copy of the upstream suite stays intact in `suite/unified_gpu_suite/`. No secrets. Failures and unsupported
paths are preserved and reported. Rule from the source suite remains binding: its PRE_REGISTRATION is a
research pre-registration; this port does not run or reinterpret any hypothesis test, only reproduces the
computation; smoke outputs are labelled **PORT-SMOKE, not research results**.

## 7. Declared deviations log (append during work)

- (to be filled)

## Declared deviations log (continued)

- Kernel-fingerprint markers were initially too strict (included a Python-side string not present in the CUDA
  source); corrected before any reported run. No effect on results.
- PyTorch/MPS is not installed on this machine (documented blocker for backend preference #2); MLX was used,
  and the NumPy fallback was verified end-to-end.
- **Production decision executed:** measured projection (kernel-only 171 s exp1 + 19 s exp3, host overhead
  bounded) put the full configuration well inside the ~2 h budget, so the full production configuration was
  run once on MLX and completed in **313 s**; its outputs are labelled PORT-PRODUCTION, not research results.
- Final status: MLX and NumPy smoke/equivalence pass; full production completed; CUDA bit-equivalence not
  claimed (CUDA unavailable).
