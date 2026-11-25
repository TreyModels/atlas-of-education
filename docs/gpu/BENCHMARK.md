# BENCHMARK — CPU vs GPU, measured on the AutoDL box (RTX 3080 Ti)

**Owner:** commander (`deepseek-gpu`). **Date:** 2026-11-25. **Branch:** `research/gpu-port-2026-11-25`,
base `e0508f3`. **Evidence class:** measured wall/CPU time, single process, GPU lane.

**Box conditions (must be read with every number):** 10-CPU cgroup (`cpu.max = 1000000 100000`) shared with the
Paper B campaign. Load average was **23.98 before** and **30.19 after** the benchmark window (it was 16–18 when
the lane started). Every run is **1 process, `nice -n 10`, `OPENBLAS/MKL/OMP=1`**; the campaign's directories
were never touched. CPU-side numbers are ±5–10 % under this contention; GPU-side replay time is far less
sensitive, but Python-side dispatch is not. `torch 2.7.1+cu118`, GPU cap 8.6, CuPy not installed (not needed).

## 1. End-to-end, one run (HK and KR Baseline, seed 0) — the headline

Same Python process per column; CPU reference vs GPU backend, `_run_single` from
`papers/shadow-education-contest/code/run_hk_korea_comparative.py`:

| run | CPU (s) | GPU cold (s) | GPU warm (s) | cold speedup | **warm speedup** |
|---|---:|---:|---:|---:|---:|
| HK Baseline | 18.883 / 18.942 | 4.909 | **3.196** | 3.85x | **5.93x** |
| KR Baseline | 39.365 / 39.073 | 9.664 | **5.372** | 4.07x | **7.27x** |

*CPU column = two independent runs. "Cold" = first run in the process (pays CUDA-graph capture, ~650 ms/engine
under load); "warm" = subsequent run (capture amortised). **Cold is the honest single-run number; warm is the
number a multi-run gate-grid process sees.** KR's rep-1 is not fully cold because HK already captured the
shared n=300 shapes.*

GPU internals for those four runs (from `pl_stats()`): 672 graph batches, 2,496 call rows, **feed 1.300 s,
replay 8.540 s** (12.7 ms/batch), **capture 5.866 s for 9 engines**. Replay time is launch-bound: ~1,800 graph
nodes per batch at ~6–7 µs/node under load.

## 2. The 405-call micro-benchmark (isolates the hot path)

One HK run's real call shapes (`perf_calls.json`), identical weights and seats to CPU and GPU:

| variant | 405-call wall | PL speedup | max abs dP |
|---|---:|---:|---:|
| CPU reference (same process) | 19.87 s | 1.00x | — |
| GPU, batched-9, **eager torch (no graphs)** | 6.03 s | **3.37x** | 2.56e-8 |
| GPU, batched-9, **CUDA-graph replay** | **1.005 s** (prep 0.249 + replay 0.756) | **19.77x** | 2.56e-8 |

**The 3.37x no-graph number is why graphs are mandatory:** the same code is a thin pass without them, and
`5.93x` e2e would collapse toward the 3x bar. Eager per-call dispatch was 14.9 ms/call; graph replay ~2.5 ms/call.

## 3. Amdahl honesty (accepted model)

PL is 92.7 % of the run. `e2e = (PL+nonPL)/(PL/S_pl + nonPL)`, hard cap **13.7x** as `S_pl → ∞`.
With `S_pl = 19.8` and `nonPL ≈ 1.5 s` the model predicts 7.4x; the measured warm e2e is 5.93x on HK and 7.27x on
KR (the gap is capture + Python-side prep + the engine's own single calls). **Any claim of 19–30x end-to-end is
rejected** (`GATE1_REPORT.md` §4.2).

## 4. What this means for the ≥5,000-run gate grid (48 CPU-h = 172,800 CPU-s)

| option | wall for 5,000 runs | basis |
|---|---|---|
| **A. today: 8–10 CPU workers** | **4.8–6.0 h** | prereg: 5,000 x 35 CPU-s, ~6 h at 8 workers |
| **B. one GPU-assisted worker** | HK-rate 4.44 h; KR-rate 7.46 h; mixed ~7.4 h | warm 5.93x / 7.27x |
| **B'. hybrid: 1 GPU worker + 9 CPUs** | **~3.1 h (estimated)** | GPU ≈ 6.5 CPU-equivalents + 9 |
| **C. cross-replicate batched GPU** | **~10–20 min (estimated, NOT measured)** | `GPU_PORT_PLAN.md` §6 memory model |

So the single-run port **frees CPU-hours but does not beat the CPU box on wall-clock**; the hybrid is ~1.6–1.9x;
only Phase 3 is order-of-magnitude. This table is the decision input, not a sales pitch.

## 5. Reproduce

```bash
cd /root/work/contest                                         # box harness with the 540-param arms
# CPU baseline (two runs per jurisdiction)
PYTHONPATH=/root/work/gpuport/e2e/engine OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  nice -n 10 /root/miniconda3/bin/python /root/work/gpuport/e2e/bench_e2e2.py
# GPU backend (two runs per jurisdiction; first is cold, second warm)
ATLAS_PL_BACKEND=gpu PYTHONPATH=/root/work/gpuport/e2e/engine OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  nice -n 10 /root/miniconda3/bin/python /root/work/gpuport/e2e/bench_e2e2.py
```

## 6. Run manifest fields a GPU run must record

Every GPU-backed run manifest must carry (see `INTEGRATION.md` §4 for the full template):

| field | value |
|---|---|
| `pl_backend` | `"gpu"` |
| `deviation_bound` | `1e-07` (amendment A-GPU-1) |
| `deviation_scope` | `"gate-grid/sensitivity only; not Paper B primary"` |
| `equivalence_artifact_sha256` | sha256 of the 130-fixture `eq2.json` used to certify |
| `cpu_reference_sha256` | sha256 of `engine/eduengine/contest_math.py` in the run's engine tree |
| `observed_max_dp` | max abs dP from the campaign's equivalence check (and a per-run 3-call spot check) |
| `gpu_engine` | `RTX 3080 Ti`, `torch 2.7.1+cu118`, cap 8.6 |
| `graph_engines_built` / `graph_capture_s` | from `pl_stats()["gpu"]` |
| `box_load_before` / `box_load_after` | load average before/after the run |
| `cpu_s` / `wall_s` | measured per run |

`pl_stats()` is the observability hook: `single_calls`, `batch_calls`, `batch_rows`, plus
`gpu.{gpu_batches, gpu_calls, engine_builds, feed_s, replay_s, capture_s}`.
