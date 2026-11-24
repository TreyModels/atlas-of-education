# ADDENDUM — environment facts and declared deviations

**Append-only addendum to `PRE_REGISTRATION.md`** (which is not edited). Branch
`research/apple-silicon-gpu-2026-11-24`. Written on 2026-11-24 after the
pre-registration (`3d65715`) and **before any port code was written**; the CUDA
reference capture described below was completed before the code, and is the only
work done between the pre-registration and this addendum.

The pre-registration's hypotheses, tolerances, smoke/scale decision and rule that
"the NumPy backend is the reference" are unchanged. This file records where the
environment did not match the pre-registration's factual statements.

## A. Correction — MLX was not installed when the pre-registration was written

Pre-registration §2 says: *"MLX (installed, tested) → PyTorch MPS (if importable;
not required) → NumPy CPU fallback."*

On this machine at 2026-11-24 17:54 local, MLX was **not installed**:
`import mlx.core` failed under every interpreter present
(`/Library/Frameworks/Python.framework/Versions/3.10`, Homebrew 3.9/3.11/3.15,
`/usr/bin/python3`, and the only existing venv). The *"installed, tested"* claim in
the pre-registration is therefore **false**; it is corrected here, not silently
overwritten.

**Resolution.** A dedicated venv was created and populated:

- interpreter: `/opt/homebrew/bin/python3.11` → Python 3.11.17 (arm64)
- venv: `/Users/treymenefee/atlas-work-2026-11-23/apple-venv` (outside the repo)
- installed and verified: **mlx 0.32.4** (`mx.default_device()` → `Device(gpu, 0)`,
  matmul/eval confirmed), numpy 2.4.6, pandas 3.1.1, scikit-learn 1.9.1,
  statsmodels 0.15.0, scipy 1.17.1, requests 2.34.2.

**Backend ladder as actually implemented** (selected by `APPLE_GPU_BACKEND`, one API):

1. **MLX** — available and verified here; this is the backend used for the runs.
2. **PyTorch MPS** — *not implemented in the port venv*. torch 2.0.1 with
   `torch.backends.mps.is_available() == True` exists only in the system Python
   3.10 interpreter, not in the 3.11 port venv. The pre-registration marks MPS
   "if importable; not required", so this is a declared non-implementation, not a
   silent substitution: requesting `APPLE_GPU_BACKEND=mps` raises a clear error.
3. **NumPy CPU** — always available; this is the equivalence **reference**.

No silent backend substitution: the backend actually used is recorded in every
result file and in `REPORT.md`.

## B. Correction — the data-generation RNG assumption in §3(b) does not hold under CuPy 13.6

Pre-registration §3(b) assumed *"CuPy's `default_rng` is a Philox4x32-10 bit
generator with NumPy's `Generator` interface"*, and proposed mapping it to
`numpy.random.Generator(numpy.random.Philox(seed))`.

Verified on the T4 (CuPy **13.6.0**, NumPy 2.2.6, 2026-11-24):

- `cupy.random.default_rng(seed)` returns
  `cupy.random._generator_api.Generator`, and
  `type(g.bit_generator).__name__ == "XORWOW"` — **XORWOW, not Philox**.
- That `Generator` has **no `normal` method** (it exposes `standard_normal`,
  `random`, `integers`, …). The upstream suite calls `.normal(...)`, so
  **the upstream CuPy scripts do not run as shipped**:
  `AttributeError: 'Generator' object has no attribute 'normal'`.
  Both tracebacks are preserved verbatim in
  `cuda_reference/run_as_shipped.log` (`exp1 --smoke` and `exp3`).
- `cupy.random` exposes **no `Philox`** at all in this install.

Consequences, declared:

1. The port's data-generation stream is **defined by the port**, not inherited
   from CuPy: `numpy.random.Generator(numpy.random.Philox(seed))`, drawn in
   float64 and cast to float32 when the suite asks for float32. It is
   deterministic and documented, but it is **not claimed to equal any CuPy
   stream** — under CuPy 13.6 there is no Philox stream to equal.
2. To keep the CUDA comparison meaningful, the CUDA reference run replaces
   **exactly that one call** (`cp.random.default_rng`) with the same NumPy-Philox
   mapping and returns `cp.asarray` device arrays (`cuda_reference/ref_shim.py`).
   The kernel source (`KERNEL_SRC` imported from the unmodified suite script),
   launch configuration, scalars, per-year loop and statistics are upstream code,
   unmodified, on the GPU. The upstream scripts themselves are **not edited**.
3. Therefore the CUDA-vs-port comparison isolates **kernel transcription
   fidelity**, not the data-generation stream. The pre-registration's §4
   equivalence test ("NumPy reference vs Apple backend") is unchanged; the CUDA
   comparison is an additional, stronger check on the same uniforms and inputs.

Note for the record: the pre-registration §3(b) mapping (NumPy Philox) remains the
correct choice given the suite's intent, because the suite's *kernel* Philox
(`sim_step`, seed0/seed1) is independent and is transcribed exactly; only the
host-side data stream had to be defined. The suite's own comment ("CuPy aims for
NumPy stream compatibility") is not true for CuPy 13.6's default generator.

## C. CUDA reference capture — completed, instance shut down (关机, not release)

- T4 instance was powered on no later than **2026-11-24 13:14 local** (container
  boot time) and was idle on arrival: GPU 0 % utilisation, 1 MiB used, no compute
  processes (only supervisord/tensorboard/jupyter).
- All reference work was done between **17:59 and 18:03 local**; `shutdown -h now`
  was issued at **18:03:06 local**, and SSH (`Connection closed`) and the MCP
  `server_status` (`reachable: false`) both confirm the box is down. Total
  powered-on window ≤ 4 h 49 min; the exact AutoDL charge is not recorded here
  (no invoice data accessible from the instance). No jobs were running at
  shutdown. **关机, not release** — data disk preserved.
- Captured artifacts (in `cuda_reference/`):
  - `cuda_manifest.json` — nvidia-smi (Tesla T4, 16 GB, driver 565.57.01,
    CUDA 12.7), Python 3.10.8, CuPy 13.6.0, NumPy 2.2.6, pip list subset,
    sha256 of all four suite scripts, the RNG probe (XORWOW vs NumPy PCG64 vs
    NumPy Philox first draws), run wall times and output hashes.
  - `cuda_smoke_exp1.json` — upstream `exp1 --smoke`: 450 rows, `batch_N=10000`,
    seeds `20261125` and `20261225`; script-internal time 0.84 s.
  - `cuda_exp3_small.json` — upstream `exp3 --draws 20 --batch-n 2000`: pulls 14
    WDI countries, wall 2.47 s. **Smoke statistic only**: 20 draws give
    `accepted = max(10, int(0.1*20)) = 10`, so the width ratios are not
    inference: `w_pov` 0.8208 (**UNIDENTIFIED** at the 0.80 gate), `w_push`
    0.6935, `w_tutor` 0.4728, `div_beta` 0.7239.
  - `cuda_kernel_dump.npz` (+ manifest, sha256) — 10 launches of the **real CUDA
    `sim_step`** (5 DGPs × t=0 and t=12), fixed seed `20261125`, `N=10000`,
    `threads=256`, `blocks=40`, all five output arrays per launch, plus the input
    `base_y`/`ability` arrays generated from the port's NumPy-Philox stream.
    This is the household-level ground truth for the port's transcription.
  - `run_as_shipped.log` — the two as-shipped failures (preserved, not hidden).
  - `ref_run.log`, `ref_run.py`, `ref_shim.py`, `cuda_kernel_dump.py` — the
    reference drivers, kept so the capture is reproducible from the artifacts.
- Script provenance: the four suite scripts on the T4 had exactly the sha256s of
  the copies committed on `research/handoff-2026-11-24`
  (`33cd60c6…` exp1, `847607ed…` exp2, `646de67f…` exp3, `5809aced…` exp4).

## D. Declared deviations log

1. **MLX absent at pre-registration time**; installed 0.32.4 in a dedicated
   Python 3.11.17 arm64 venv (see A).
2. **CuPy 13.6 RNG reality**; port data stream is a port-defined NumPy-Philox
   stream; CUDA reference uses the one-call adapter; upstream scripts remain
   byte-identical and their as-shipped failure is preserved (see B).
3. **PyTorch MPS backend not implemented** (optional per pre-registration;
   not present in the port venv). Ladder used: MLX → NumPy, backend recorded.
4. **T4 used only for the CUDA reference**, then shut down (`关机`, not release).
5. No change to hypotheses, tolerances, smoke/scale decision, or the rule that the
   NumPy backend is the reference.

## E. Correction to §A — the pre-registration was right about MLX; the environment scan was wrong

**§A above is itself incorrect and is corrected here (append-only; §A is not rewritten).** The claim that
MLX was "not installed" when the pre-registration was written was wrong. The Lead's environment scan (and the
Commander's initial scan) checked the standard interpreters and `~/.venvs` but missed **`/tmp/apple_venv`**,
created **2026-11-24 17:51:25 local — before the seam (17:53)**. That venv has Python 3.10.2, **mlx 0.32.4**,
numpy 2.2.6, and `mx.default_device()` → `Device(gpu, 0)`. **That is the environment the pre-registration's
"MLX (installed, tested)" refers to, and the pre-registration was accurate.**

The port venv `/Users/treymenefee/atlas-work-2026-11-23/apple-venv` (Python 3.11.17, mlx 0.32.4, numpy 2.4.6,
pandas 3.1.1, scikit-learn 1.9.1, statsmodels 0.15.0, scipy 1.17.1) exists as a **second, independent
environment** created by the Commander; it was not a repair of a missing dependency and is not the canonical
one.

**Timeline correction.** §A also said this addendum was "written before any port code was written". In commit
order that is not accurate: the port-completion commit `fd933d9` (18:03:52) was produced in parallel from the
pre-registered design, and *then* this addendum was committed (`5ca8b43`, 18:04:41). What is true, and what
matters for the pre-registration's integrity: **no hypothesis, tolerance, smoke/scale rule, backend-selection
rule or decision criterion was changed after seeing results.** The addendum records environment facts and
declared deviations; §B (CuPy 13.6 RNG reality) and §D (MPS unimplemented, T4 use) stand unchanged.

**Which interpreter produced each reported run** (full detail in `env_provenance.json`):

| artifact | interpreter that produced the committed artifact | durable reproduction |
|---|---|---|
| `results/smoke_exp1_{numpy,mlx}.json`, `smoke_exp3_*.json`, `equivalence.json`, `component_tests.json`, `projection.json` | `/private/tmp/apple_venv/bin/python` — Python 3.10.2, mlx 0.32.4, numpy 2.2.6 | re-run under `apple-venv310` (Python 3.10.2, identical pinned versions): **bit-identical outputs**, only wall-time log lines differ |
| `results/exp1_abm_mlx.json`, `exp2_macro_wall_mlx.csv`, `exp3_abc_posterior_mlx.json` (production) | `/private/tmp/apple_venv/bin/python` (313 s) | re-run under `apple-venv310`: **374 s, all three sha256 identical** |
| `results/cuda_vs_transcription.json` | `apple-venv310` (durable) | deterministic given the saved CUDA dump |

The canonical durable environment is therefore
`/Users/treymenefee/atlas-work-2026-11-23/apple-venv310/bin/python` (pinned by `requirements.txt`,
recorded in `env_provenance.json`). `/tmp/apple_venv` is not durable and is documented only as the original run
environment.

**Provenance defect corrected.** `results/production_summary.json` previously said
`"python": "3.12.14 (/tmp/apple_venv)"`. Both parts were wrong: `/tmp/apple_venv` is Python **3.10.2**, and
3.12.14 is `/tmp/shape-venv` (no mlx, created 07:20, predates the port). The summary now records the true
interpreter, the durable re-run, and the audit caveat.
