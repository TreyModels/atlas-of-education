# CONTEST_MATH_PERF — task-12: optimisation of `engine/eduengine/contest_math.py`

**Lane:** `contest-math`. **Date:** 2026-11-25. **Branch:** `research/contest-audit-v2-2026-11-25`.
**Deliverables:** optimised `engine/eduengine/contest_math.py` (commit `d1acdf3`), harness
`docs/audit/code/contest_math_bench.py`, results `docs/audit/code/contest_math_bench_results.json`, this report.
**Evidence class:** deterministic numerical engineering — performance + bit-compatibility, no empirical claim.

---

## 0. SHIP DECISION (explicit, as required)

**KEEP-MEMO-ONLY.** Retained: (i) bounded **result LRU** memoisation keyed by
`(method, seats, exact weight bytes)` (64 entries, returns copies), (ii) **Simpson-grid memoisation** keyed by
the exact `w_min` float (bit-identical arrays), (iii) `pl_stats()` observability.

**Reverted and NOT shipped:** (a) the forward-pass float64 re-association (it changed outputs by ≤1.4e-15 —
  within the contract's 1e-12, but **not bit-identical**; reverted so the module is exactly output-compatible
  with Gate-1 evidence); (b) `pl_win_probs_batch` and its vectorised core (**measured 0.87–0.96× — slower**;
  "do not ship a slower engine"). The public single-call API is unchanged and the code path is the pre-existing
  algorithm; the only behavioural difference is that repeated identical deterministic calls are memoised.

**Result: outputs are BIT-IDENTICAL to the pre-task-12 module (max |diff| = 0.000e+00 over 130 fixtures).**
The unchanged 68-test suite passes on the box (`68 passed, 14.05 s`). The Gate-1 540 evidence used commit
`98baf6b` and is therefore **unaffected**; and because this shipped module is bit-identical, any future Gate-1
run on the repaired engine is also numerics-unchanged — this is a pure performance memoisation.

**Speed-up, plainly stated: 2–5× is UNPROVEN. Measured end-to-end speed-up is 1.11×** (clean same-core pair,
box: reference 21.036 CPU-s → memo-only 18.904 CPU-s = **1.113×**). The independent compute-controller
measurement of the earlier (superseded) build was 22.183 → 18.550 = 1.196×; the batched variant was 21.088 =
1.052× vs reference (i.e. slower than memo-only). The gain comes entirely from the 37/405 repeated weight
vectors (9.1 %) that the engine re-computes.

## 1. What is shipped (bit-compatible)

1. **Result LRU** at `_dispatch` for `method in {'auto','exact'}`, keyed by `(method, seats, w.tobytes())`,
   64 entries, hit returns a copy of the previously computed array. Hit rate in one HK Baseline run:
   **result_hit = 37, result_miss = 368 (9.1 %)**. The exact-cap guard (A6) runs **before** the cache lookup and
   the key includes the method, so an `auto` entry can never satisfy a `method='exact'` call (hardening
   `fceca3b`). Deterministic by construction; no RNG.
2. **Simpson-grid memo** `_simpson_grid(w_min)` (64 entries): identical `t`/`sw` arrays, zero hits in the HK
   run (grid changes every call), free insurance for callers with repeated grids.
3. **`pl_stats()`**: hit/miss counters (observability only).
4. `pl_realize`, `pl_win_probs_mc`, the exact subset DP and the quadrature algorithm are untouched.

## 2. Equivalence evidence

| check | result |
|---|---|
| 130 randomised fixtures `(n ∈ {12…600}, all seats, dispersion 0–6)`, shipped vs frozen pre-task-12 module (`0f56621`) | **max abs diff = 0.000e+00 — bit-identical** |
| determinism (repeated identical call) | bit-identical |
| unchanged 68-test suite, box | **68 passed in 14.05 s** |
| `method='exact'` beyond n=20 raises (A6) even with a cached `auto` result present | raises ✓ |
| batch API | removed (was ≤3.1e-15-equivalent but slower) |

## 3. Measurements

### 3.1 End-to-end, HK Baseline seed-0 (`run_hk_korea_comparative._run_single`), box, 1 process

| variant | CPU-s | ratio |
|---|---|---|
| reference (pre-task-12 module) | 21.036 | 1.000× |
| **shipped memo-only (this report)** | **18.904** | **1.113×** |
| earlier forward-opt build, independent controller measurement | 18.550 (ref 22.183) | 1.196× (superseded) |
| earlier forward-opt + batched tutoring (measurement only) | 21.088 | 1.052× vs reference — slower than memo-only |

Run-to-run box variance (shared 10-CPU cgroup with the 540 replication) is ±5 %; the shipped 1.113× is a
same-core adjacent pair. Instrumented shipped run: 18.90 s,
`cache_stats = {result_hit: 37, result_miss: 368, grid_hit: 0, grid_miss: 368}`.

### 3.2 cProfile (reference build, same box)

| metric | reference |
|---|---|
| total | 23.663 s / 5,449,091 calls |
| `_quadrature_win_probs` tottime (calls) | 10.139 s (405) |
| `cumsum` | 4.749 s |
| `c_einsum` | 2.685 s |
| clip helpers | 1.683 s |

The shipped build executes **368** quadrature calls instead of 405 (the 37 memoised ones return in 0.022 ms
instead of ~50 ms), which accounts for the ~2.1 s saved — matching the measured 21.04 → 18.90 s.

### 3.3 Per-call (shipped code path is the reference algorithm, so cold cost is unchanged)

| size | reference ms | shipped cold ms | memoised repeat ms |
|---|---|---|---|
| n=300, k=69, disp 1.0 | 51.58 | 52.80 (ratio 0.98, noise) | **0.022** |
| n=300, k=69, disp 2.0 | 61.07 | 63.73 (0.96) | **0.022** |
| n=300, k=36, disp 1.0 | 35.71 | 36.02 (0.99) | **0.022** |
| n=600, k=69, disp 1.0 | 125.10 | 126.92 (0.99) | **0.025** |

Cold per-call speed-up is **1.00×** by construction (same arithmetic). All speed-up is memoisation.
9-call gate-year group (cold, sequential): 475 ms — i.e. the engine's call pattern is inherently ~9 × 50 ms.

## 4. Why ≥2× is not reachable within the binding constraint

The run is 93.6 % `pl_win_probs` (405 calls ≈ 18.4 s of 19.8 s under cProfile). Per call the cost is the
element-wise float32 dynamic programme: n=300 items × d=min(K−1, n−K−1)=68 coefficients × m≈266 Simpson nodes,
with (i) a **sequential** suffix DP over items (~45 %), (ii) one `cumsum` over the `(n+1,d+1,m+1)` suffix array
(~25 %), (iii) the forward prefix DP + `einsum` contraction (~30 %). Only `(d, m)` are vectorisable — the item
axis is inherently sequential. Any reduction of this work (coarser grid, float64 re-association,
cumulative-form recurrence, deconvolution) changes the float32 result by ~1e-7, which **fails the ≤1e-12
equivalence acceptance**. Measured cold-call optimisation of the loop within those constraints: 0.96–1.18×
(noise-dominated at engine size); the 9-call batch was 0.87–0.96× (memory-bandwidth bound) and is reverted.
Hence the only shipped gain is memoisation of the 9.1 % duplicate calls.

## 5. Levers that would reach ≥2× (decisions for Commander/Lead)

| lever | owner | projected effect | cost/risk |
|---|---|---|---|
| **(a) tutoring prep grid 9 → 5 points** (keep 3-point parabola refinement) | engine-tutoring | calls 405 → ~225 ⇒ total ≈ 12.2 s ⇒ **1.7×** | tutoring grid resolution change; `contest_grid_bound` must be reported |
| **(a′) grid 9 → 4 points** | engine-tutoring | calls ≈ 180 ⇒ ≈ 10.0 s ⇒ **2.0×** | larger tutoring change; re-verify prize/effort checks |
| **(b) relax equivalence to ~1e-3** on the expected-probability path (coarser Simpson grid) | contract amendment + Lead | ≈1.8× on PL ⇒ ~1.7× end-to-end; combines with (a) to >3× | breaks bit-equality with Gate-1 records; AFTER re-run required |
| **(c) compiled kernel** (Cython/Numba/C) | Committer | est. 5–10× | violates "pure NumPy"; build dependency |
| (d) 9-call batching | this lane | measured **0.87–0.96× (loss)** | rejected/reverted |

Recommendation: lever (a) is cheap and reversible but is a tutoring-numerics decision; lever (b) is the only
module-local route toward 2× and requires an explicit amendment. Neither is taken unilaterally here.

## 6. Gate-1 impact statement

* The 540 cross-env replication and all Gate-1 evidence used **`98baf6b`** — this lane's commits (`fceca3b`,
  `d1acdf3`) do not alter any deployed artifact used by that evidence.
* The shipped module is **bit-identical** to the pre-task-12 module (0.000e+00 over 130 fixtures), so future
  runs on the repaired engine produce identical numbers; only wall time changes (≈1.11× faster on HK Baseline).
* No RNG, no API change, no change to `pl_realize`/exact/MC paths.

## 7. Reproduction

```bash
cd /Users/treymenefee/neon-boot/wt4/auditv2
export OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD/engine"
python docs/audit/code/contest_math_bench.py --quick    # equivalence + microbench (git reference)
# box A/B pair (read-only deploy from d1acdf3):
#   PYTHONPATH=<ref_engine> python -c '<HK Baseline _run_single>'  -> 21.036 CPU-s
#   PYTHONPATH=<shipped_engine> python -c '<same>'                 -> 18.904 CPU-s
```

Box provenance: `/root/work/contest`, commit `d1acdf3`, Python 3.10.8 / NumPy 1.24.1 (below host floor —
recorded), 1 process, `nice -n 10`, BLAS/OMP=1, 10-CPU cgroup shared with the 540 replication (timing
variance ±5 %); host authoritative for correctness (130 fixtures + 68 tests).
