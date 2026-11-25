# INTEGRATION — flag, call sites, run commands, manifest, rollback

**Owner:** commander (`deepseek-gpu`). **Date:** 2026-11-25. **Branch:** `research/gpu-port-2026-11-25`,
base `e0508f3`. Gate: `GATE1_REPORT.md`. Equivalence: `EQUIVALENCE.md`. Numbers: `BENCHMARK.md`.

## 1. The flag

The GPU backend is **OFF by default**. Enable it for a process at import time:

```bash
export ATLAS_PL_BACKEND=gpu          # 'cpu' (default) or 'gpu'
```

`eduengine/__init__.py` then imports `eduengine.contest_gpu`, warms the CUDA context, and registers the backend
with `eduengine.contest_math`. A CPU-only deployment never imports torch.

Programmatic equivalent (already-imported process):

```python
from eduengine import contest_gpu
from eduengine import contest_math as cm
assert contest_gpu.available()
cm.register_gpu_backend(contest_gpu)      # idempotent
cm.set_pl_backend("gpu")                  # raises if torch/CUDA is unavailable
assert cm.pl_backend() == "gpu"
```

**Scope (declared limitation, human-approved 2026-11-25):** GPU runs are permitted for the **≥5,000-run gate
grid and sensitivity runs only**. Paper B's preregistered primary computations and any headline number must run
with the default CPU backend. A GPU run is *not bit-identical*; the declared bound is **max abs diff ≤ 1e-7**
on the probability vector (measured 4.83e-8 worst over 130 fixtures; fallback ≤1e-6 unused).

## 2. Call sites

| site | what it does with the flag |
|---|---|
| `engine/eduengine/contest_math.py::pl_win_probs` | **unchanged, CPU only.** The contract function and its ≤50 ms/call target keep the bit-identical reference algorithm. |
| `engine/eduengine/contest_math.py::pl_win_probs_batch` | new public API. CPU backend: loops `pl_win_probs` (bit-identical to before). GPU backend: one batch through `contest_gpu.dp_batch`. |
| `engine/eduengine/modules/tutoring.py` (prep grid) | builds the 9 weight vectors, **one** `pl_win_probs_batch` call instead of 9 sequential calls; same per-point results on CPU. |
| `engine/eduengine/core.py::Engine._pl_probs` | single gate call goes through `pl_win_probs_batch(w[None, :], seats)` so the same GPU engine serves it (padded to the 9-wide graph). |
| `tests/test_contest_math.py` | untouched (sha256 below); passes on both backends. |
| `tests/test_contest_math_gpu.py` | new: CPU-batch bit-identity, GPU-batch deviation ≤1e-7, seat-sum invariant; GPU tests skip when CUDA is absent. |

Behaviour that does **not** change: exact subset DP (n ≤ 20), `pl_realize`, `pl_win_probs_mc`, the seat-sum
invariant, determinism on the `auto`/`exact` paths, all RNG keying.

## 3. Commands

```bash
# 68-test contract suite, CPU backend (must be bit-identical to pre-G2 behaviour)
cd /root/work/gpuport/e2e
PYTHONPATH=$PWD/engine OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  nice -n 10 /root/miniconda3/bin/python -m pytest tests/test_contest_math.py tests/test_contest_math_gpu.py -q

# same suite with the GPU backend registered
ATLAS_PL_BACKEND=gpu PYTHONPATH=$PWD/engine OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  nice -n 10 /root/miniconda3/bin/python -m pytest tests/test_contest_math.py tests/test_contest_math_gpu.py -q

# one HK/KR Baseline run, CPU then GPU (cold + warm in one process)
cd /root/work/contest
PYTHONPATH=/root/work/gpuport/e2e/engine nice -n 10 /root/miniconda3/bin/python /root/work/gpuport/e2e/bench_e2e2.py
ATLAS_PL_BACKEND=gpu PYTHONPATH=/root/work/gpuport/e2e/engine nice -n 10 /root/miniconda3/bin/python /root/work/gpuport/e2e/bench_e2e2.py
```

## 4. Run manifest (required for every GPU-backed run)

```json
{
  "pl_backend": "gpu",
  "deviation_bound": 1e-07,
  "deviation_scope": "gate-grid/sensitivity only; NOT Paper B preregistered primary",
  "equivalence_artifact_sha256": "0bb75933334537938f60f0fa993d50a5903e319a14ecfc2186d0e0b8d4d35915",
  "observed_max_dp": 0.0,
  "observed_max_dp_method": "campaign equivalence sweep + per-run 3-call CPU spot check",
  "cpu_reference_sha256": "5fceb4d5094a63249bffdc2f5712801d52e3a83c5ce64c32a85b0f2e805ee944",
  "engine_git_commit": "<commit of the engine tree used>",
  "gpu_engine": "NVIDIA GeForce RTX 3080 Ti (cap 8.6), torch 2.7.1+cu118",
  "graph_engines_built": 0,
  "graph_capture_s": 0.0,
  "box_cpu_cgroup": "1000000 100000",
  "box_load_before": 0.0,
  "box_load_after": 0.0,
  "n_calls": 0,
  "n_batches": 0,
  "cpu_s": 0.0,
  "wall_s": 0.0
}
```

`observed_max_dp` is **not** a per-call CPU-vs-GPU comparison for all 5,000 runs (that would double the compute
and is pointless — the certification is the fixture artifact). It is the campaign-level equivalence sweep plus a
cheap per-run spot check; the declared bound and its artifact hash are what certifies the run.

## 5. Gate-grid run — instructions, currently **HELD**

The Lead has placed the ≥5,000-run grid and the 1-GPU + 9-CPU hybrid on hold while the Paper B campaign is on the
box (box load 24–36 on a 10-CPU cgroup). **Do not start it without the Lead's go-ahead.** When released:

1. Run **one process** for the GPU column (captures amortise across runs; do not fork a process per run).
2. `ATLAS_PL_BACKEND=gpu`, `nice -n 10`, `OPENBLAS/MKL/OMP=1`; nothing else on the GPU.
3. Record `box_load_before`/`box_load_after` around each batch of runs and every manifest field in §4.
4. Hash the inputs and outputs; keep the runner's own checkpointing (it survives pool hangs).
5. A GPU-only **pilot of ≤200 runs** is permitted by the Lead subject to: exactly 1 nice-10 process, load
   recorded before/after, no CPU campaign interference. Its purpose is to validate the hashing + manifest
   pipeline and the run-level deviation distribution, not to produce gate-grid results. *(Not run under G2:
   box load was 24–36 throughout.)*

## 6. Rollback

Unset `ATLAS_PL_BACKEND` (or `cm.set_pl_backend('cpu')`) → the process is back on the bit-identical reference
path with no other change. The G2 code is additive except for three small call-site edits; `git revert` of the
G2 commit restores the pre-G2 tree.

## 6b. Verification: full-run CPU A/B is bit-identical (base `e0508f3` vs HEAD `7c6f9ac`)

The G2 refactor changes how the **default CPU path** is *called* (the 9-point prep grid now goes through
`pl_win_probs_batch`, the engine's gate call through a one-row batch) even though it runs the same arithmetic.
Bit-identity was argued by construction; this is the run-level demonstration.

**Method.** HK Baseline seed 0 **and** KR Baseline seed 0, default CPU backend (`ATLAS_PL_BACKEND` unset), run
from the same box harness (`run_hk_korea_comparative._run_single`) in **separate processes** for the two engine
trees, same discipline (1 process, `nice -n 10`, `OPENBLAS/MKL/OMP=1`). Every value `_run_single` returns is
serialised as `float.hex()` (so signed zero and any NaN would still show), then the two JSON files are compared
**byte-for-byte**. Engines: base worktree at `e0508f3` (`contest_math.py` sha `cd7b5ba6…`), HEAD at `7c6f9ac`
(`contest_math.py` sha `5fceb4d5…`).

**Result: max abs diff = 0.0 — exactly zero. The two output files are byte-identical.**

Fields compared (13 numeric values x 2 jurisdictions): `contest_e_mean`, `elite_q5_share_pct`, `g12_pct`,
`k12_rate_pct`, `k12_spend`, `q5_q1_gap_pp`, `q5_q1_spend_ratio`, the 5-element `k12_rate_by_q` and 5-element
`k12_spend_by_q` vectors, and the `seed`/`arm_id`/`jurisdiction` labels. Coverage: HK and KR, i.e. both contest
jurisdictions and both parameter sets.

**Interpretation.** On the default CPU path the G2 batching refactor is **bit-identical at the run level**, not
merely equivalent; only the GPU backend carries the declared ≤1e-7 deviation. This closes the last verification
item for G2.

**Reproduce (box, ~2 min, 1 CPU process):**

```bash
cd /root/work/contest
export OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1
PYTHONPATH=/root/work/gpuport/base/engine nice -n 10 /root/miniconda3/bin/python \
  /root/work/gpuport/base/ab_run.py /root/work/gpuport/base/ab_base.json
PYTHONPATH=/root/work/gpuport/head/engine nice -n 10 /root/miniconda3/bin/python \
  /root/work/gpuport/base/ab_run.py /root/work/gpuport/head/ab_head.json
cmp /root/work/gpuport/base/ab_base.json /root/work/gpuport/head/ab_head.json && echo BYTE-IDENTICAL
```

Artifacts (`docs/gpu/exp/`): `ab_run.py` sha256
`02e9fe996b3e1fb770c51e12b5b89cfc36b76ed9647aba5378f774ba10161c68`; `ab_base.json` and `ab_head.json` are
**identical**, sha256 `95517cf58d70c6d623d30448f6556e89de5ecb3c54243140acc68e686ca9df3b` both. Box load during the
A/B: 18.7–20.3 (campaign running, untouched).

## 7. Artifact hashes (this commit)

| artifact | sha256 |
|---|---|
| `engine/eduengine/contest_gpu.py` | `ab08a53b188cc645981200f02461994ec179483b493ec520a8aea7d9114c596f` |
| `engine/eduengine/contest_math.py` | `5fceb4d5094a63249bffdc2f5712801d52e3a83c5ce64c32a85b0f2e805ee944` |
| `engine/eduengine/core.py` | `3e6754c99e15761029b2dd4b1a59ab4fe4ed34637f6d70c02e61d0178663bdae` |
| `engine/eduengine/modules/tutoring.py` | `b3d32ceecd7b79c3d7deb2df2d3f44d988a8cab5a18cfa4fe594980ebb9c3fdf` |
| `engine/eduengine/__init__.py` | `2c082d5c9b9bd28f5b5e110e1a3f2f675b693279d2aa790d37348a9f21cb348f` |
| `tests/test_contest_math_gpu.py` | `498c8698e6a069d5308a9e8e02217f33f20c731a7d544f4ecf32da1428c5f960` |
| `tests/test_contest_math.py` (unchanged) | `23e7881e20142d782c7f59752efff25c296217a542696de4d7b5579a6ea7c074` |
| box `eq2.json` (equivalence artifact) | `0bb75933334537938f60f0fa993d50a5903e319a14ecfc2186d0e0b8d4d35915` |
| `docs/gpu/exp/ab_run.py` (A/B harness) | `02e9fe996b3e1fb770c51e12b5b89cfc36b76ed9647aba5378f774ba10161c68` |
| `docs/gpu/exp/ab_base.json` = `ab_head.json` (bit-identical A/B outputs) | `95517cf58d70c6d623d30448f6556e89de5ecb3c54243140acc68e686ca9df3b` |

## 8. What is NOT in this integration

* No GPU code on the reference-only path; `contest_math.py` still imports nothing from `eduengine`.
* No change to `pl_realize`, the exact DP, MC, or any RNG stream.
* No gate-grid run, no cross-replicate refactor (Phase 3, separate approval).
* No paper-number use: the deviation is declared and restricted to gate-grid/sensitivity output.
