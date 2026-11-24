# REPORT — CUDA → Apple Silicon port of the unified GPU suite

**Task 50.** Branch `research/apple-silicon-gpu-2026-11-24`; record
`research/records/2026-11-24-apple-silicon-gpu/`. Machine: Apple M1 (arm64), macOS 26.6.2.
**This is a portability job, not a research claim.** No number produced by the port is reported as a research
result; upstream outputs are relabelled **PORT-SMOKE / PORT-PRODUCTION**. Pre-registration (scope, API
inventory, tolerances, RNG mapping, smoke/scale decision) was committed before the layer was coded
(`3d65715`).

## Status in one paragraph

The suite now runs on Apple Silicon with the upstream scripts **byte-for-byte unmodified**, through a CuPy
import shim backed by MLX (preferred) or NumPy. The CuPy/CUDA surface used is tiny except for one thing:
both GPU scripts compile an embedded CUDA C kernel via `cp.RawModule`. CUDA C cannot be compiled on macOS, so
the port transcribes that one kernel (`sim_step`, used by exp1 and exp3) line-by-line into NumPy and MLX and
recognises it by source fingerprint; arbitrary `RawModule` code is refused with a clear error. Fixed-seed
equivalence tests pass: NumPy reference vs MLX backend are **bit-identical on the kernel** (0 state
mismatches, max abs difference 0.0 on all five outputs), equal within `9.5e-7` end-to-end, and experiment 3's
small-run identifiability output is identical. The full production configuration was projected to be
time-bounded and was run; wall time and outputs are recorded below. **The kernel transcription is additionally
verified against the real CUDA kernel**: the T4 capture replayed through both backends gives 0 integer
mismatches and max abs 3.8e-6 on 10 launches (`results/cuda_vs_transcription.json`). **CUDA bit-equivalence of
the data-generation stream is not claimed**: under CuPy 13.6 the real `default_rng` is XORWOW with no
`.normal`, so the port's NumPy-Philox stream is the port's own definition (§3b).

## 1. Exact CuPy API surface used (from grep, not assumption)

`cp.RawModule(code)` and `.get_function("sim_step")` (2 uses); `cp.random.default_rng(seed).normal(loc,
scale, size=, dtype=)` (2); `cp.exp` (2); `cp.clip` (2); `cp.empty(size, dtype=)` (10); `cp.asnumpy` (6);
`cp.cuda.Stream.null.synchronize()` (2); dtype constants `cp.float32` (10) and `cp.int32` (4). No
`cp.array`, `cp.zeros`, `cp.arange`, no arithmetic on CuPy arrays, no indexing, reductions or dtype casts
appear in the two GPU scripts. exp2/exp4 are CPU scripts (numpy/pandas/sklearn/statsmodels) and run
unchanged.

## 2. Backend mapping

| CuPy API | MLX backend (preferred) | NumPy fallback | Notes |
|---|---|---|---|
| `cp.float32`, `cp.int32` | `mx.float32`, `mx.int32` | `np.float32`, `np.int32` | dtype constants |
| `cp.empty(n, dtype)` | `mx.zeros` wrapped in `Array` | `np.zeros` | zeros, not uninitialised, for deterministic pre-fill |
| `cp.exp`, `cp.clip` | `mx.exp`, `mx.clip` | `np.exp`, `np.clip` | on host/MLX arrays |
| `cp.asnumpy` | `np.array(mx.array)` | view | materialises to host |
| `cp.random.default_rng(seed).normal` | NumPy `Generator(np.random.Philox(seed))` → MLX array | same → NumPy array | explicit mapping; see §3 |
| `cp.cuda.Stream.null.synchronize()` | `mx.synchronize()` | no-op | |
| `cp.RawModule` / `get_function("sim_step")` | `kernels_np_mlx._compute_mlx` | `kernels_np_mlx._compute_numpy` | kernel transcription, fingerprint-checked |
| backend selection | `APPLE_GPU_BACKEND=mlx` (default) | `APPLE_GPU_BACKEND=numpy` | `torch`/`mps` accepted but PyTorch is **not installed**; falls back to NumPy with a message |

**PyTorch/MPS:** `torch 2.0.1` with `torch.backends.mps.is_available() == True` is installed in the system
Python 3.10 framework interpreter, but **not** in either port venv (`/private/tmp/apple_venv`,
`apple-venv310`), so a `mps`/`torch` request resolves to the NumPy fallback with a printed message. Declared
unimplemented (pre-registration backend preference #2). MLX 0.32.4 (pinned port venv) is the backend used for
all reported runs; the NumPy path is fully functional (equivalence reference and fallback if MLX is absent).

## 3. RNG mapping — explicit, no silent substitution

**(a) Kernel uniforms.** The CUDA `sim_step` generates its own uniforms with Philox4x32-10 keyed on
`(counter=(i, year, 0, 1), key=(seed0, seed1))` and `(raw+0.5)/2^32`. The port transcribes Philox exactly
(uint32 multiply-high/low, 10 rounds, constants `M0=0xD2511F53`, `M1=0xCD9E8D57`, `W0=0x9E3779B9`,
`W1=0xBB67AE85`). The vectorised transcription is verified against an independent scalar transcription
(`tests/test_components.py` → `philox_vector_equals_scalar: true`); the C source is the specification. The
**same uniform bits** are fed to both backends, so backend comparisons isolate arithmetic, not RNG.

**(b) Data-generation stream** (`cp.random.default_rng(seed).normal` for `base_y` and `ability`). Mapped to
NumPy's Philox generator: `np.random.Generator(np.random.Philox(seed))`, normal drawn in float64 and cast to
float32 as the scripts request. **This mapping was checked against CuPy 13.6.0 on a T4 (2026-11-24) and the
pre-registration's assumption does not hold:** `cupy.random.default_rng(seed)` returns a
`cupy.random._generator_api.Generator` backed by **XORWOW**, that object has **no `.normal` method**, and
`cupy.random` exposes **no Philox**. The upstream scripts therefore *fail as shipped* on that CuPy
(`AttributeError: 'Generator' object has no attribute 'normal'`; both tracebacks preserved in
`cuda_reference/run_as_shipped.log`). The port's NumPy-Philox mapping is consequently **the port's definition of
the data stream**, not an emulation of a CuPy stream that does not exist: a CUDA run and a port run at the same
seed consume different data draws unless the CUDA side also uses this mapping. What *can* be tested — the
kernel — is tested against real CUDA output in §4a. See `ADDENDUM_2026-11-24_env.md` §B, and §E for the
correction to the addendum's own first version.

## 4. Equivalence results (fixed seed, same transcribed kernel; NumPy = reference)

Declared tolerances (pre-registered): integer state arrays must match **exactly** (0 mismatches); continuous
float32 arrays `max_abs ≤ 1e-5` and `max_rel ≤ 1e-4`; anything else is a real state change/failure.
Evidence: `results/equivalence.json`, `results/kernel_probe_{numpy,mlx}.npz`, `results/smoke_exp1_*.json`,
`results/smoke_exp3_*.json`.

| test | result |
|---|---|
| kernel-level, N=2,000, year 3, seed (20261125, 34) | `state` mismatches **0**, `tutor` mismatches **0**; `learn`, `work`, `y_hh` max abs **0.0**, max rel **0.0** |
| exp1 smoke end-to-end (450 rows: 2 seeds × 5 DGPs × 3 arms × 15 years) | all six integer-state metrics (`ger`, `study_work`, `work_only`, `hidden_work`, `cl_total`, `tutoring`) **exact**; continuous metrics max abs: `enrolled_work_hrs_p90` **9.54e-7**, `tutor_income_corr` **8.04e-8**, `mean_learn` **0.0**, `q_pub` **0.0** — **equivalent** |
| exp3 small run (draws=20, batch_n=2,000; World Bank API reachable) | identifiability `width_ratio` differences **0.0** for all four parameters; `identified` flags identical — **equivalent** |

Interpretation: the kernel comparison is *bit-identical* here, so there is no float32 reduction-order
difference to separate; the small end-to-end continuous differences (≤9.5e-7) are float32 rounding in the
host-side summary statistics (percentiles/correlations), not state changes. If a future MLX version changes a
reduction order, the declared tolerance classifies that as noise; any integer mismatch would be reported as
a real state change.

### 4a. CUDA kernel verification — against the real GPU kernel, 10 launches

The T4 capture (`cuda_reference/cuda_kernel_dump.npz`) holds 10 launches of the **unmodified CUDA `sim_step`**
(5 DGPs × t=0 and t=12; seed 20261125; N=10,000; threads=256; blocks=40) *with the inputs it received*. Feeding
those saved inputs to the NumPy and MLX transcriptions isolates the kernel. `tests/verify_cuda_kernel.py`
replays all 10 launches on both backends and compares the five output arrays:

| run | int mismatches (`state`,`tutor`) | float max abs | float max rel | verdict |
|---|---|---|---|---|
| NumPy transcription vs CUDA, 10 launches | **0** | **3.815e-06** | **1.192e-07** | pass |
| MLX transcription vs CUDA, 10 launches | **0** | **3.815e-06** | **1.192e-07** | pass |

Evidence: `results/cuda_vs_transcription.json` (20/20 comparisons pass; per-launch numbers; port environment).
This upgrades the claim from "equivalent to a NumPy transcription" to **"transcription verified against the
real CUDA kernel on 10 launches"**. The residual 3.8e-6 is float32 arithmetic ordering (FMA contraction in the
CUDA compiler), inside the pre-registered 1e-5 abs / 1e-4 rel band. It does **not** make the data-generation
stream CUDA-equivalent (§3b).

## 5. Smoke path, wall times, and the production decision

Documented smoke path: `run_apple.sh smoke` = `exp1_unified_gpu_abm.py --smoke` (2 seeds, 5 DGPs, 3 arms,
15 years, N=10,000) + `exp3` at draws=20, batch_n=2,000. Timed (`results/smoke_timings.json`):

| backend | runner wall | shell real | user | sys |
|---|---|---|---|---|
| NumPy | 3 s | 4.04 s | 0.88 s | 0.13 s |
| MLX | 4 s | 3.86 s | 1.32 s | 0.41 s |
| full equivalence suite (6 subprocesses) | — | 7.85 s | — | — |

**Scale decision.** Per-call kernel cost measured at production sizes (`tests/projection.py`): MLX
`N=250,000` 22.7 ms/call; `N=50,000` 3.4 ms/call. Production needs 7,500 exp1 calls (20 seeds × 5 DGPs ×
3 arms × 25 years) → **kernel-only 171 s ≈ 2.8 min**, and 5,000 exp3 calls at N=50,000 → **19 s**, plus host
RNG/statistics overhead. The projection is comfortably time-bounded (order of ten minutes), so—per the
pre-registered rule—the full production configuration **was run**; it is labelled PORT-PRODUCTION and is not
a research result.

**Production outcome — completed.** The full configuration ran to completion on the MLX backend in
**313 s (5 min 13 s)** total: exp1 full (20 seeds × 5 DGPs × 3 arms × 25 years × N=250,000 → **7,500 rows**),
exp2 (macro wall / tie-breaker CSV), and exp3 full (5,000 draws × 50,000 households; **500 accepted**).
Outputs and sha256: `results/exp1_abm_mlx.json`, `results/exp2_macro_wall_mlx.csv`,
`results/exp3_abc_posterior_mlx.json`, `results/SHA256SUMS_production_mlx.txt`,
`results/production_wall_mlx.txt`, log `results/production_mlx.log`. Port-output summary:
`results/production_summary.json` (exp2 macro-only accuracy 0.767 vs micro-signature 1.000; exp3
identifiability width ratios w_pov 0.914/UNIDENTIFIED, w_push 0.53, w_tutor 0.286, div_beta 0.795 — these are
PORT-PRODUCTION numbers, **not** research results).

**These production numbers are construction-implied port outputs, not an H1/H4 test.** The suite audit
(`research/suite-lit-review-2026-11-24` @ `4649cae`, `AUDIT.md` §9 and the withdrawn-claims list) shows that the
shipped exp2 implements no macro FE regression and no overlap statistic (H1 undefined), that `strength` appears
only in a docstring so the Q1 zero-signal control (H4) cannot run, and that the four "micro signatures" are
transforms of the same state mix (classifier recovery is tautological). The `macro_only_accuracy 0.767 /
micro_signature 1.000` pair and the exp3 width ratios must therefore be read as **construction-implied
artefacts of this parameterisation** — not as evidence for H1, H2, H4, or for any mechanism. This port does not
repair the suite; that is the redesign's job (`research/suite-redesign-2026-11-24`).

**Reproduction under the durable environment.** The production configuration was re-run on 2026-11-24 under the
pinned durable venv (`apple-venv310`: Python 3.10.2, same pinned versions as the original
`/private/tmp/apple_venv`): **374 s**, and all three output files are **bit-identical** to the first run (same
sha256: exp1 `dda35da9…`, exp2 `0623cbf2…`, exp3 `9f5ba1cc…`). Smoke and equivalence also reproduce
bit-identically (only wall-time log lines differ).

## 6. Ported vs fallback: what actually ran

- *Ported path:* MLX backend via `shim/cupy` → `gpu_compat` → `kernels_np_mlx._compute_mlx`. All reported
  runs (smoke, equivalence, production) used this path. The full production config completed on the M1 in
  5 min 13 s (313 s; durable-env re-run 374 s, identical outputs), consistent with the 2.8 min kernel-only
  projection plus host RNG/statistics overhead.
- *Reference/fallback path:* NumPy backend, used as the equivalence reference; it is the drop-in path if
  MLX cannot be installed (`APPLE_GPU_BACKEND=numpy`, verified end-to-end at smoke and equivalence).
- *PyTorch MPS:* not installed in the port venvs (`torch 2.0.1` + MPS exists only in the system Python 3.10
  framework); a `mps` request falls back to NumPy with a printed message. Declared unimplemented.
- *CUDA path:* not available, not emulated; `RawModule` for any kernel other than the suite's `sim_step`
  raises `PortabilityError` (tested).

## 7. Limitations

1. **No CUDA data-stream equivalence claim.** The kernel transcription *is* verified against real CUDA output
   (§4a); what cannot match is the data-generation stream, because CuPy 13.6 has no Philox `default_rng` with
   `.normal` (§3b). The port's stream is explicitly the port's own definition.
2. **Only one CUDA kernel is supported.** Arbitrary `RawModule` code requires a hand-written transcription;
   the layer refuses the rest loudly.
3. **MLX bit-identity is empirical, not guaranteed**: it held on this M1 / MLX 0.32.4 for this kernel; other
   kernels/reduction orders/MLX versions may differ by float32 noise (the declared tolerances cover that).
4. **The production run is a portability demonstration**, not a re-run of the research: its outputs are
   labelled PORT-PRODUCTION and should not be quoted as findings.
5. exp3 depends on the live World Bank API (worked in this run); offline runs need cached targets.
6. **The upstream suite is not runnable as shipped on CuPy 13.6**: `cp.random.default_rng(seed).normal` raises
   `AttributeError` on the T4 (preserved in `cuda_reference/run_as_shipped.log`). The CUDA reference therefore
   used a one-call adapter to hold the data stream fixed (`cuda_reference/ref_shim.py`); the upstream scripts
   themselves are byte-identical and unmodified.
7. **The production numbers are construction-implied**, not an H1/H4 test — see §5 and `AUDIT.md` §9.

## 8. Reproduction

**Canonical, durable, pinned environment** (see `env_provenance.json`; `requirements.txt` pins exact versions):

```bash
cd research/records/2026-11-24-apple-silicon-gpu
# Python 3.10.2 arm64 (macOS framework build); durable path, NOT /tmp:
python3.10 -m venv /Users/treymenefee/atlas-work-2026-11-23/apple-venv310
./apple-venv310/bin/pip install -r requirements.txt     # mlx==0.32.4 numpy==2.2.6 pandas==2.3.3 ...
APPLE_PY=/Users/treymenefee/atlas-work-2026-11-23/apple-venv310/bin/python \
  APPLE_GPU_BACKEND=mlx ./run_apple.sh smoke            # ~4 s
APPLE_PY=.../apple-venv310/bin/python tests/run_equivalence.py   # ~8 s
APPLE_PY=.../apple-venv310/bin/python tests/verify_cuda_kernel.py  # CUDA ground truth, ~5 s
APPLE_PY=.../apple-venv310/bin/python APPLE_GPU_BACKEND=mlx ./run_apple.sh production  # 374 s
```

Provenance: the original committed runs were produced under `/private/tmp/apple_venv` (Python 3.10.2, identical
pinned versions; not durable). All smoke/equivalence/production outputs were re-produced bit-identically under
`apple-venv310`; `env_provenance.json` records both and the per-artifact mapping. `/tmp/shape-venv`
(Python 3.12.14, no mlx) never ran any port artifact.

Files: `gpu_compat.py`, `kernels_np_mlx.py`, `shim/cupy/__init__.py`, `tests/{run_equivalence,
kernel_probe,test_components,projection,verify_cuda_kernel}.py`, `run_apple.sh`, `APPLESILICON.md`,
`requirements.txt`, `env_provenance.json`, `results/`, `cuda_reference/`, `suite/unified_gpu_suite/` (upstream,
unmodified). No secrets.

## 9. Declared deviations (append-only)

- The kernel-recognition fingerprint markers were initially too strict (included a Python-side string, not
  present in the CUDA source); corrected before any reported run. No effect on results.
- `torch`/MPS is not installed in the port venvs (it exists only in the system Python 3.10 framework); MLX
  used, NumPy fallback verified.
- **Explicit override of the pre-registration's §5 default decision.** §5 said the default is *not* to run the
  full production configuration on the laptop. It was run (job #2 of the forward programme requires the ported
  run). This is a declared override of that default, not an application of the pre-registered rule; outputs
  remain labelled PORT-PRODUCTION. (The earlier log line in `PRE_REGISTRATION.md` §7 says "per the
  pre-registered rule" — corrected there by an appended note.)
- **CUDA reference captured and used** (T4, 2026-11-24; instance shut down, 关机 not release): kernel verified
  against 10 real CUDA launches, 0 integer mismatches, max abs 3.8e-6 (§4a).
- **Environment provenance corrected**: original runs `/private/tmp/apple_venv` (Python 3.10.2, mlx 0.32.4,
  numpy 2.2.6); all outputs reproduced bit-identically under the durable `apple-venv310`; the wrong
  "3.12.14" string in `results/production_summary.json` fixed. See `ADDENDUM_2026-11-24_env.md` §E.
- **Audit cross-reference added**: the PORT-PRODUCTION exp2/exp3 numbers are construction-implied
  artefacts, not H1/H4 tests (`research/suite-lit-review-2026-11-24` @ `4649cae`, `AUDIT.md` §9).
