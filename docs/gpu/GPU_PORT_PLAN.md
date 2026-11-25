# GPU_PORT_PLAN — design, batching, memory, and the Phase-3 one-pager

**Owner:** commander (`deepseek-gpu`). **Date:** 2026-11-25. **Branch:** `research/gpu-port-2026-11-25`,
base `e0508f3`. Gate 1 evidence: `GATE1_REPORT.md`. Equivalence: `EQUIVALENCE.md`. Numbers: `BENCHMARK.md`.

## 1. What was built

| file | role |
|---|---|
| `engine/eduengine/contest_gpu.py` | optional torch/CUDA backend: static-buffer batched DP, **one captured CUDA graph per shape**, LRU of replay engines. Default OFF; torch never imported unless the backend is selected. |
| `engine/eduengine/contest_math.py` | flag/registration hook (`register_gpu_backend`, `pl_backend`, `set_pl_backend`) + public `pl_win_probs_batch`; the single-call reference path is **unchanged** and stays CPU. |
| `engine/eduengine/__init__.py` | registers the backend when `ATLAS_PL_BACKEND=gpu` at import; pays the one-time torch/CUDA-init cost there. |
| `engine/eduengine/core.py` | `Engine._pl_probs` sends its single gate call through `pl_win_probs_batch(w[None,:], seats)` so the same GPU engine serves it. |
| `engine/eduengine/modules/tutoring.py` | the 9-point prep grid is built first and evaluated in **one batched call** instead of 9 sequential calls. |
| `tests/test_contest_math_gpu.py` | CPU batch bit-identity, GPU batch deviation <= 1e-7, seat-sum invariant. |

**Design rule kept intact:** `contest_math.py` still imports nothing from `eduengine` (the
`test_reference_module_does_not_import_the_engine` contract test passes); the backend is *injected*.

## 2. Where the time goes and what is batched

One HK Baseline run (seed 0) makes **405 PL calls in 368 dispatch events**: **333 rows in 37 tutoring
9-point grids** (90 %) plus **72 single gate calls** (from `Engine._pl_probs`, 10 %). The CPU cost was ~50 %
Python dispatch / ~50 % NumPy (`CONTEST_MATH_PERF.md` §3.2), so the win is batching, not FLOPs.

| path | unit | how it runs |
|---|---|---|
| tutoring prep grid | 9 independent weight vectors per gate | **one batch of 9** → one CUDA-graph replay |
| engine single gate call | 1 vector | one-row batch, **padded to the 9-wide graph** so it reuses the same engine (no extra capture) |
| reference `pl_win_probs` | 1 vector | **CPU, unchanged** — the contract function and its 50 ms/call target are untouched |

Element vectors in a batch never interact (all DP/scan/contraction ops are per-lane), so a lane's arithmetic is
identical to a single call; the only deviation is the reordered float32 contraction measured in `EQUIVALENCE.md`.

## 3. CUDA graphs are the mechanism (not an optimisation detail)

A single quadrature call is a ~300-step dependent chain of ~1,800 tiny ops. Eager torch dispatch costs ~15 ms per
call — a **3.37x** PL speedup. Capturing the chain once per shape and replaying it costs ~1 ms → **19.8x** on the
405-call micro-benchmark. Without graphs the port is a thin pass and the e2e number misses 3x.

Shape key: `(n, d, below, M1q, B_graph, use_graph)`, where `M1q` (padded Simpson-node count) is rounded up to a
multiple of 32 and narrow calls use `B_graph = 9`. One HK run therefore needs ~2–9 captures (measured: 9 across
HK+KR cold runs, ~650 ms each under box load 24–30); a 5,000-run gate-grid **process amortises them once**.

## 4. Memory

Per-lane suffix array `Suf = (n+1)(d+1)(m+1) x 4 B`:

| shape | m+1 (padded 160) | per lane | 9 lanes (one graph) |
|---|---:|---:|---:|
| n=300, d=68 | 160 | 13.2 MB | **119 MB** |
| n=600, d=68 | 160 | 26.2 MB | **236 MB** |

Plus DP factors (~2 MB/lane) and small float64 vectors. Measured run: 9 cached engines across HK+KR, ~1–1.5 GB
resident on 12 GB. Hard limits: engine LRU = 12; `M1_CAP` = 1,601 mirrors the reference's node cap (a call with
`m+1 = 1601` and n=600 × 9 lanes would need ~2.4 GB — still inside 12 GB, but such weights are far outside the
engine's dispersion range).

## 5. Determinism and failure modes

* Same `(weights, seats)` → same output (graph replay is a fixed instruction sequence; no RNG anywhere).
* No CUDA/torch → `set_pl_backend('gpu')` raises with a clear message; the default remains the bit-identical
  CPU path. A CPU-only deployment never imports torch.
* Graph capture failure or OOM → the process fails loudly; there is **no silent fallback to CPU mid-run**
  (a silent fallback would mix two numerical realizations inside one reported statistic).

---

## 6. Phase-3 one-pager (decision-ready, NOT approved, NOT started)

**Goal:** turn the 5,000-run gate grid from hours into minutes by batching *across replicates*, not just within
a gate, and price it.

**Why it is the only option that beats the CPU box on wall-clock.** Measured single-run GPU: HK 3.85x cold /
5.93x warm, KR 4.07x / 7.27x e2e. At those rates one GPU needs **~7.4 h** for the 48-CPU-h grid — *worse* than
the 4.8–6.0 h an 8–10-worker CPU box already achieves. A hybrid (1 GPU worker ≈ 6.5 CPU-equivalents + 9 CPUs)
lands ~3.1 h (~1.6–1.9x). Only cross-replicate batching changes the order of magnitude.

**Memory bound (12 GB, 2 GB headroom):** 22.2 MB/replica at m+1 = 267 (`FEASIBILITY.md`); at our padded 160 it
is 14.2 MB, so **B_max ≈ 420–450**; a safe operating point is **B = 32 replicates x 9 grid = 288 lanes (6.4 GB)**,
with B = 48 x 9 = 432 (9.6 GB) at the edge.

**Kernel/launch count:** ~1,800 graph nodes per call; one replay per (gate, replicate-batch). For 5,000 runs at
B = 32: 157 replicate-batches x 46 gate groups ≈ 7,200 replays x ~1,800 nodes ≈ **13 M graph nodes** — at
~0.5 µs/node ≈ 6.5 s of launch time, plus memory time. Feasibility's memory model gives **8.3 runs/s at B = 100**
→ **~10 min** for 5,000 runs; our allowance is **10–20 min**.

**Integration surface (the real cost): the engine run loop must advance replicates in lockstep.**
Recommended: make `Engine.run()` (or the year-step loop) a generator that *yields* at each PL call, then a
driver holds B engine instances, collects their B weight matrices per gate (B x 9 rows), calls the existing
`pl_win_probs_batch` once, and scatters the results back. Semantics per replicate are unchanged; seeds stay
event-keyed; the deviation per lane is the same as today (lanes do not interact). Alternatives — vectorising
`core.py` over a replicate axis (bigger rewrite, touches every module) or threads (GIL-bound) — are worse.

**Cost:** **3–5 box-days** (generator refactor + driver + resume/hash/manifest + a 200-run equivalence pilot).
**Risk:** medium (engine refactor); the numeric path is already proven.
**Payoff:** gate grid ~10–20 min instead of ~5–7 h; also makes any future multi-seed campaign cheap.
**Decision needed:** separate human approval; do not start under this gate.

---

## 7. What this plan deliberately does NOT do

* No change to the CPU reference algorithm, its 68-test contract, or any Gate-1 evidence.
* No bit-exact emulation of NumPy/BLAS reduction order (rejected in `GATE1_REPORT.md` §2).
* No fp64 on the 3080 Ti (FP64 = 1/64 of FP32; the DP is float32 by design).
* No cross-replicate engine refactor (Phase 3, separate approval).
* No gate-grid run while the Paper B campaign is on the box.
