# FEASIBILITY — GPU port of `engine/eduengine/contest_math.py`

**Task:** shared `task-2` (Gate-1 analysis), teammate `feasibility`. **Date:** 2026-11-25.
**Worktree:** `wt5/gpuport`, branch `research/gpu-port-2026-11-25`, base `e0508f3`.
**Target:** `engine/eduengine/contest_math.py` (672 L) — the dominant cost of the repaired education-engine
baseline run (PL share ≈93–97 % depending on basis: `CONTEST_MATH_PERF.md:97` reports 93.6 % on its 19.8 s
cProfile basis; 368 cold calls × ≈50 ms against the shipped 18.904 s wall time is ≈97 %; the briefing's
92.7 % figure is consistent with a slightly longer run). **Proposed hardware:** RTX 3080 Ti 12 GB (AutoDL;
`torch 2.7.1+cu118` verified).
**Evidence class:** deterministic numerical engineering — performance + bit-compatibility. No
empirical or calibration claim. **No box access was used** (the AutoDL CPU side is off-limits to this
lane; the GPU was idle but no SSH was made). All numerical demonstrations below were run locally on
the Mac with the venv (`/Users/treymenefee/neon-boot/venv/bin/python`, NumPy 2.2.6, read-only), against
copies of the module's private helpers; `engine/` and `tests/` were not modified.

---

## 0. BOTTOM LINE

**Verdict: NO-GO under the binding criterion as written.** The campaign's own written admission test is
*"CPU allocation unchanged until a ≥3× @≤1e-12 prototype result justifies moving the gate grid to GPU"*
(`docs/audit/COMPUTE_SCHEDULE.md:527`). The ≤1e-12 half of that test is **not achievable by any real GPU
port** of this module: the CPU reference stores its dynamic programme in **float32**
(`engine/eduengine/contest_math.py:376`), and ≤1e-12 therefore requires bit-identical reproduction of
NumPy's private float32 reduction order. Measured on the real algorithm, changing **only one** reduction's
association (the `cumsum`) already moves the output by **2.3e-9 – 1.9e-8**; a realistic reordered
GPU implementation lands at **8.8e-9 – 1.1e-7**; and a *more accurate* all-float64 implementation lands at
**6.5e-8 – 6.1e-7**. That is **3.3–5 orders of magnitude above 1e-12** (2,300× at the absolute best,
8,800–110,000× realistic). The repo's own practice is stricter still: a float64 re-association that moved outputs
by ≤1.4e-15 was **reverted for not being bit-identical** (`docs/audit/CONTEST_MATH_PERF.md:16-20`;
`docs/audit/code/contest_math_bench_results.json:64-68`).

**The deviation is small and scientifically irrelevant, but it must be declared, not assumed.** The engine
contract's accuracy requirement for this path is max |P − P_MC| ≤ **0.01**, mean ≤ **0.002**, |ΣP − seats| ≤
**1e-6** (`docs/audit/ENGINE_INTERFACE_CONTRACT.md:111-113,118-123`); the quadrature's own documented
truncation+Simpson bound is **2e-3** (`contest_math.py:115`); and the legacy approximation that the repair
replaced was only acceptable below **≈2 percentage points** of individual error
(`docs/audit/CONTEST_MATH_APPROX_ERROR.md:8-10`). A ≤1e-6 declared equivalence is therefore **10⁴× inside** the
contract's max tolerance, **2×10³× inside** its mean tolerance, and **2×10⁴× below** the approximation error the
repair exists to remove — but it is **not** ≤1e-12. Corroboration from the repo: the perf-tasking lane already
concluded that *"any reduction of this work … changes the float32 result by ~1e-7, which **fails the ≤1e-12
equivalence acceptance**"* (`CONTEST_MATH_PERF.md:101-104`).

**Conditional path.** If (and only if) the Lead amends the criterion to **≥3× @≤1e-6**, the port is
technically feasible and worth building: predicted **≈19–30× end-to-end** (central ≈20×) against an Amdahl
ceiling of **24–38×** (contest_math is ≈97 % of the 18.904 s shipped run; §4.3). The one prototype and the
one first experiment are specified in §6. **Absent that amendment: do not build it.**

| decisive quantity | value | source |
|---|---|---|
| gate as written | max abs diff ≤ **1e-12** (and ≥3× speed-up) | `docs/audit/COMPUTE_SCHEDULE.md:526-528`; `docs/audit/code/contest_math_bench.py:13,174-177` |
| reference DP precision | **float32** (`dt = np.float32`) | `engine/eduengine/contest_math.py:372-378` |
| best-case reorder deviation (cumsum association only) | **2.3e-9 – 1.9e-8** | §2.3 (measured, this task) |
| realistic reordered-GPU deviation | **8.8e-9 – 1.1e-7** | §2.3 (measured) |
| more-accurate float64 deviation | **6.5e-8 – 6.1e-7** | §2.3 (measured) |
| repo's own GPU-vs-CPU precedent | max abs **8.9e-15** — but on **float64** numerics | `~neon-boot/wt3/gpu/research/records/2026-11-25-gpu-rtx3080ti/RUN_REPORT.md:11,181` |
| engine contract tolerance (this path) | **0.01** max / **0.002** mean | `ENGINE_INTERFACE_CONTRACT.md:111-113` |
| shipped baseline | **18.904 s/run**, 405 PL calls, 368 cold | `contest_math_bench_results.json:70-76,95-100` |
| Amdahl ceiling | **24–38×** (non-PL 0.5–0.8 s of the 18.904 s run) | §4.3 |

---

## 1. ALGORITHM MAP (Q1)

### 1.1 Call path and call pattern

`core.py` imports `pl_win_probs`/`pl_realize` (`engine/eduengine/core.py:24`). The expected-probability path is

```
values()/gate_prize_dv() → _gate_expected_P()            core.py:486-535
      └ contest_weights() → _contest_w()  (w = x_eff**r) core.py:415-435, 394-404
      └ _pl_probs(w_pool, seats)                         core.py:437-462
            └ pl_win_probs(w, seats, method='auto')      core.py:448-449
                  └ _dispatch → _quadrature_win_probs    contest_math.py:483-560, 342-415
```

The expected-probability **pool is cached per `(year, gate, pool weight bytes)`**
(`core.py:513-522`), and `contest_math` adds a result LRU keyed
`(method, seats, w.tobytes())` (`contest_math.py:498-516,553-557`). On the shipped HK-Baseline run the
measured counts are **405 total `pl_win_probs` calls, 368 cold quadrature + 37 memo hits**
(`contest_math_bench_results.json:70-76`). The 405 calls are organised as **45 gate-year groups × 9 calls**
(405 / 9 = 45 exactly): a 9-point proportional prep-effort grid
(`engine/eduengine/modules/tutoring.py:45-48`) evaluates `_pl_win_probs` once per grid point
(`tutoring.py:338-350`, call at `:345`). Within a group the 9 calls differ only by the stock override
vector, hence by the weight vector; **all 9 are independent and batchable** — that is the batching unit
the CPU batch variant used and lost on (`CONTEST_MATH_PERF.md:16-20,103-104,115`).

The realised path is a different function and is *not* hot: `pl_realize` is O(n) `argpartition`+
O(k log k) sort (`contest_math.py:620-672`, score at `:668-670`, selection at `:670-671`), called once per
gate per year (`core.py:962`). The exact subset DP (`contest_math.py:223-299`) is only used for `n ≤ 20`
(`:92-94,524-527`) and is not on the engine's n=300 path at all.

### 1.2 Exact op sequence of `_quadrature_win_probs` (`contest_math.py:342-415`)

| # | step | line | dtype | shape / size | order-sensitive reduction? |
|---|---|---|---|---|---|
| 1 | normalise weights `wn = exp(logw−max)`; floor | `:354-360` | f64 | (n,) | no |
| 2 | Simpson grid in `u=log t`; `t`, `sw`, `m` (cached by `w_min`) | `:305-339`, call `:363` | f64 | (m+1,) | no (fixed) |
| 3 | pick cheaper tail: `below`, `d = min(K−1, n−K−1)` | `:368-370` | int | 68 @ n=300,K=69 | no |
| 4 | `p_below = −expm1(−wn·t)`; `q_above = exp(−wn·t)`; both **cast to float32** | `:376-378` | f64→**f32** | (n, m+1) ≈ 300×267 | no (elementwise) — but f64 `expm1/exp` is libm |
| 5 | suffix DP over the **sequential item axis** `i = n−1 … 0`: `Suf[i]=Suf[i+1]·f_stay + shift(f_inc·Suf[i+1])` | `:383-394` | **f32** | `Suf` `(n+1,d+1,m+1)` | no (per-element) |
| 6 | **`np.cumsum(Suf, axis=1, out=Suf)`** — one vectorised call over the `d` axis | `:395-397` | **f32** | in-place, 5.5 M elems | **YES** — sequential scan over `a=0..d` |
| 7 | prefix DP + contraction over the **sequential item axis** `i = 0 … n−1` | `:399-414` | **f32** | `Pre`,`tmp` `(d+1,m+1)` | |
| 7a | **`np.einsum('am,am->m', Pre, Suf[i+1][::-1])`** then `.astype(float64)` | `:406-407` | **f32** | (69,267)→(267,) | **YES** — 69-term f32 dot per node |
| 7b | `G = clip(offset + sign·tail)` | `:408` | f64 | (m+1,) | no |
| 7c | `kernel = wn[i]·t·q_above[i]` (f64); **`P[i] = np.dot(sw, kernel·G)`** | `:409-410` | f64 | (267,) | YES — f64 BLAS `ddot` (but harmless, see §2.2) |
| 7d | advance prefix DP | `:412-414` | **f32** | (69,267) | no |
| 8 | `_renormalize_to_seats`: `p.sum()` (f64) then water-fill | `:192-217` (call `:537`) | f64 | (300,) | YES — `p.sum()` is f64 pairwise (harmless) |

`m` is data-dependent: the grid is `t ∈ [1e-5, 14/w_min]` with `h=0.1` in `log t`, even, capped at 1600
nodes (`contest_math.py:305-339,101-105`). Measured node counts at n=300 are **143–501** across
dispersion 0–6 (`CONTEST_MATH_VALIDATION.md:96-105`); this task measured 201–383. The perf doc's "m≈266"
is a representative value, not a constant. `d=68` for n=300,K=69 is exact:
`min(69−1, 300−69−1)=min(68,230)=68` ✔.

### 1.3 Confirming `CONTEST_MATH_PERF.md`'s split and shape

* **Confirmed in kind.** The box cProfile lists `_quadrature_win_probs` tottime **10.139 s / 405 calls**,
  `cumsum` **4.749 s**, `c_einsum` **2.685 s**, clip helpers **1.683 s** (`CONTEST_MATH_PERF.md:72-81`).
  These are *self* times; they sum to 19.256 s = 81.4 % of the profiled 23.663 s total. A local cProfile of
  one real call in this task reproduced the same ranking (numpy 2.2.6, n=300, K=69): `cumsum` was the single
  largest item (0.068 s of 0.123 s), then `_quadrature_win_probs` self (0.041 s), then `c_einsum` (0.008 s).
  The **proportions are machine-dependent** (cumsum 55 % locally vs 25 % on the box) because the strided
  `cumsum(axis=1)` is cache/BLAS-path-sensitive; the *attribution* is correct.
* **One correction.** The 10.14/4.75/2.69 split is cProfile self-time and does **not** sum to the run. The
  unprofiled cost accounting is: 368 cold calls × ≈50 ms = **18.40 s**, plus ≈0.5 s non-PL = 18.904 s
  (0.5–0.8 s within the ±5 % run variance; §4.3) (`CONTEST_MATH_PERF.md:80-93`,
  `contest_math_bench_results.json:95-100`). Per-call benchmarks at the
  contract size are 35.71 ms (n=300,K=36) and 51.58 ms (n=300,K=69) (`CONTEST_MATH_PERF.md:87-90`,
  `contest_math_bench_results.json:10-47`).
* **Shape confirmed** for n=300 and d=68; m+1 is node-count dependent (above). The PL share is
  ≈96–97 % of the shipped run on the attribution used here (18.40/18.904 = 97.3 %; ≈96 % at non-PL 0.8 s,
  §4.3); the perf doc's 93.6 % is against its profiled 19.8 s figure.

### 1.4 Per-call byte and FLOP counts

Formulas and exact values (n=300, d=68; `m+1` = 201 at dispersion 1, 267 at the perf doc's representative
grid). 4 bytes per float32, 8 per float64; bytes counted as the working-set traffic the current code
actually touches (one read + one write per element per ufunc pass):

| quantity | formula | nodes=201 | nodes=267 |
|---|---|---|---|
| suffix array `Suf` | `(n+1)(d+1)(m+1)·4` | **16,698,276 B** (15.9 MiB) | **22,181,292 B** (21.2 MiB) |
| tail factors `p_below`,`q_above` | `2·n·(m+1)·4` | 0.48 MB | 0.64 MB |
| suffix-DP traffic | `n·(2(d+1)(m+1)·4 + 8(m+1))` | 33.8 MB | 44.9 MB |
| `cumsum` traffic (in place) | `2·Suf` | 33.4 MB | 44.4 MB |
| prefix-loop traffic (DP + einsum + f64 outer) | `n·(≈30·(m+1)·4)` | 118.4 MB | 157.3 MB |
| **total bytes / call** | | **186.1 MB** | **247.2 MB** |
| **FLOPs / call** | 3 suffix + 1 cumsum-add + 3 prefix + 2 einsum + 2 dot per element | **37.4 MFLOP** | **49.7 MFLOP** |

Per shipped run: **368 cold calls × 247 MB ≈ 100 GB** of effective traffic (node-count weighted;
75 GB at the low-node count), and **≈20 GFLOP** of FP32 arithmetic (15 GFLOP at low nodes). The
FP64 outer products (`dot`, `renormalize`) are negligible. The key roofline fact: **≈4–5 GB/s is the CPU's
effective rate** (247 MB / 50 ms), and only **0.6 ms/run** of the run is FP32 arithmetic at the GPU's
34 TFLOP/s — the algorithm is **memory/overhead-bound, not FLOP-bound** (§4).

---

## 2. THE 1e-12 GATE (Q2 — the crux)

### 2.1 What the gate compares

The gate is stated in the equivalence harness: 130 randomised fixtures over `n ∈ {12…600}`, all seats,
dispersion 0–6, comparing `max |P_new − P_ref|` against **`acceptance <= 1e-12`**
(`docs/audit/code/contest_math_bench.py:13,58-77,174-177`), and operationally in the GPU-lane admission
criterion **"≥3× @≤1e-12"** (`docs/audit/COMPUTE_SCHEDULE.md:526-528`). The repo's own fixtures show what
the gate achieved in practice: **`max_abs_diff = 0.0` over 130 fixtures — bit-identical**
(`contest_math_bench_results.json:4-7`; `CONTEST_MATH_PERF.md:22,45-53`); the 68-test suite passes on the box
(`CONTEST_MATH_PERF.md:23`; `CODE_CHANGES.md:88`). A float64 re-association that moved outputs by
**≤1.4e-15** was *within* 1e-12 yet **reverted**, because the Gate-1 record demanded bit-identity
(`CONTEST_MATH_PERF.md:16-20`; `contest_math_bench_results.json:64-68`).

### 2.2 Which operations are order-sensitive (measured on this stack)

| op | location | reference order | order-sensitive at 1e-12? |
|---|---|---|---|
| `np.cumsum(f32, axis=1)` | `contest_math.py:397` | **sequential left-to-right per `(i,m)` lane** — verified `np.array_equal` against a manual f32 loop, both 1-D and on the full strided `(301,69,267)` array | **YES** — f32 |
| `np.einsum('am,am->m')` f32 | `:407` | **not** a sequential loop, **not** `np.sum(axis=0)` pairwise, **not** f64-accumulate-then-cast — all three measured different. It is bit-identical to **`diag(P.T @ S)`**, i.e. NumPy routes it to the **CPU BLAS sgemm** accumulation order (verified for (a,m) = (69,30),(69,267),(35,201),(68,5), `optimize` on/off, f32 and f64) | **YES** — f32 |
| `np.dot(sw, kernel·G)` f64 | `:410` | BLAS `ddot` (not sequential/reversed) | **NO** — reordering it moves `P` by only **1.1e-16** (reversed) / **3.3e-16** (sequential f64) |
| `p.sum()` f64 in renormalise | `:202` | NumPy pairwise | **NO** — f64, ~1e-16 |
| `np.expm1`/`np.exp` f64 then cast f32 | `:377-378` | host libm (box: glibc; Mac: Accelerate) | **Marginal** — a 1-ulp f64 difference flips the f32 cast only if within 1 ulp64 of an f32 midpoint, P≈2⁻²⁹ per element ⇒ ≈0.12 expected flips/run (≈0.03 per 130-fixture gate). Cannot be *proved* equal across CUDA libdevice vs host libm. |

So the float64 stages of the computation are harmless to the gate (≤3.3e-16), and the **float32 DP is the
only blocker**.

### 2.3 Measured deviation of reordered implementations (decisive numbers)

When a sub-op's *association* is changed and everything else is held identical, the output moves as follows
(n=300; 300 outputs; weights `exp(disp·N(0,1))`; `renorm` = after the engine's `_renormalize_to_seats`;
measured in this task, NumPy 2.2.6, seed 20261125):

| variant (only this changed) | K=36,disp=1 | K=69,disp=2 | K=69,disp=1 | K=36,disp=4 |
|---|---|---|---|---|
| **cumsum 2-block f32 association** (a GPU scan) | **2.44e-09** | **1.89e-08** | **1.45e-08** | **2.27e-09** |
| cumsum computed in f64 then cast | 1.01e-08 | 2.85e-08 | 2.98e-08 | 2.43e-08 |
| einsum replaced by `np.sum(axis=0)` (pairwise) | 8.77e-09 | 1.47e-08 | 1.13e-08 | 1.79e-08 |
| einsum computed in f64 then cast | 1.73e-08 | 2.60e-08 | 3.75e-08 | 2.08e-08 |
| **realistic GPU reorder (cumsum block + einsum pairwise)** | **8.78e-09** | **2.09e-08** | **1.60e-08** | **1.79e-08** |
| float32 `expm1/exp` shortcut | 5.98e-08 | 7.71e-08 | 7.62e-08 | 1.08e-07 |
| **all-float64 DP ("more accurate")** | **6.30e-08** | **2.09e-07** | **1.25e-07** | **6.09e-07** |
| entries violating 1e-12 (realistic reorder) | 297/300 | 297/300 | 298/300 | 224/300 |

Reading:

* **Even the most conservative possible GPU implementation** — one that keeps the suffix DP, prefix DP,
  einsum semantics and everything else identical and changes *only* how the 69-element `cumsum` is
  associated (the one reduction that is trivially parallelisable on GPU) — is **2.3e-9**, i.e. **2,300×
  above the gate**, with 41–212 of 300 entries violating it.
* A realistic reordered f32 kernel is **1e-8–1e-7**, **10⁴–10⁵× above** the gate.
* A **float64** implementation (the natural "fix" for GPU numerics) is *worse*, **6.5e-8–6.1e-7**, because it
  is measured against a float32 reference whose own truncation error it exposes.
* This matches the task's `eps32·√n` estimate order-of-magnitude (ε₃₂≈6e-8; √69≈8.3 ⇒ ≈5e-7 relative on
  accumulated DP values, ≈1e-8–1e-7 absolute on `P`). It also matches the perf lane's own conclusion, which
  it reached without measuring: *"any reduction of this work … changes the float32 result by ~1e-7, which
  fails the ≤1e-12 equivalence acceptance"* (`CONTEST_MATH_PERF.md:101-104`).

For calibration: the repo's own GPU-vs-CPU precedent (the recovered ABC/wild-cluster suite) achieved
**max abs diff 8.9e-15** — but its numerics are explicitly **float64** ("float64 for numerical
stability", `~neon-boot/wt3/gpu/research/records/2026-11-25-gpu-rtx3080ti/scripts/gpu_e1_q3_wild_cluster_ri.py:45,184-186`;
`RUN_REPORT.md:11,181`). The 1e-12 tolerance was calibrated on float64 quantities; it is **not** a
meaningful tolerance for a float32 DP.

### 2.4 Is bit-identity a "port", or "not at all"?

Achieving ≤1e-12 requires reproducing, bit-for-bit, every float32 op of the reference:

1. `cumsum` — **emulable**: a GPU kernel can assign one lane per `(i,m)` and do 69 sequential f32 adds,
   which is exactly NumPy's order (verified). Costs little.
2. `einsum('am,am->m')` f32 — **not portably emulable**: it is the CPU BLAS sgemm accumulation order
   (verified `== diag(P.T@S)`). Reproducing it on GPU means reimplementing the *box's* OpenBLAS sgemm
   inner-kernel reduction tree (vector-width and build specific), not porting an algorithm. On CPU it is
   already version/BLAS dependent: the equivalence fixtures were generated on the box with NumPy 1.24.1
   (`CONTEST_MATH_PERF.md:139-141`) while the host validation stack is NumPy 2.2.6
   (`CONTEST_MATH_VALIDATION.md:178-179`). There is **no** published cross-environment float32
   bit-reproducibility guarantee.
3. f64 `expm1`/`exp` libm — residual ~0.1 f32-cast flips per run, unproven equal between CUDA libdevice and
   host libm.
4. f64 `ddot`/`p.sum()` — harmless (§2.2).

So the only way to pass 1e-12 is a **NumPy+BLAS emulator written on the GPU**, whose arithmetic is
deliberately locked to CPU-specific orders. That is not the proposed work (a port), it has no guaranteed
speed-up (it forbids the parallel scans/reductions a GPU is good at), and bit-identity cannot even be
guaranteed across the box's own NumPy/BLAS stack. Note also that **no cross-environment CPU check of the
repaired engine's float32 PL path exists**: the recorded host-vs-box agreement (max abs 7.105e-15,
`CODE_CHANGES.md:22`) is a **Gate-0, pre-repair** comparison, before `contest_math` was in the engine path
(`CODE_CHANGES.md:18,53,73`).

### 2.5 Verdict on the crux

* **(a) Is ≤1e-12 achievable within a single run?** **No.** Any reduction order other than the reference's
  is accepted by neither the gate nor a bit-identity policy. Measured: **2.3e-9 – 1.1e-7**.
* **(b) At all, without a declared deviation?** Only by **bit-identical emulation of NumPy's private
  float32 reduction order plus CPU-BLAS sgemm order plus host libm**, i.e. emulating the CPU stack — not a
  GPU port; not portable; not provably achievable. **Practically: no.**
* The 1e-12 gate is **not an accuracy requirement**; it is an implementation-lock. The engine's actual
  accuracy requirements are 0.01/0.002 (`ENGINE_INTERFACE_CONTRACT.md:111-113`) and the quadrature's own
  error bound is 2e-3 (`contest_math.py:115`). A declared **≤1e-6** equivalence is 10⁴× inside the contract
  and 10³× inside the algorithm's own bound.

---

## 3. BATCHING TOPOLOGY (Q3)

The only available parallelism is the **9 independent calls inside one gate-year group** and/or **across
independent runs**. The sequential item axis (n=300) cannot be split without changing the arithmetic.

### 3.1 Option (i) — within-run 9-call group batch (recommended)

Batch the 9 grid-point calls of one gate-year into one tensor operation. This is exactly the variant that
was built for CPU and **reverted as slower: 0.87–0.96×** (memory-bandwidth-bound;
`CONTEST_MATH_PERF.md:16-20,103-104,115`; `contest_math_bench_results.json:8,64-68`). On GPU the economics
invert: the CPU loss was bandwidth (≈4–5 GB/s effective), while a GPU has **912 GB/s** and its problem at
B=9 is **kernel-launch latency**, which batching directly amortises.

* batch B = **9**; per-batch memory = 9 × 22.18 MB = **0.20 GB** (trivial on 12 GB).
* kernel launches ≈ 2.7×10³ per batched call (`2 passes × 300 item-steps × ~4–6 torch ops + cumsum + fixed`);
  per group ≈ 2.7×10³, per run 45 groups ≈ **1.22×10⁵ launches** vs **1.10×10⁶** unbatched.
* time (torch eager, ~5 µs/launch): **≈0.61 s/run** (launch-bound) → **≈30×** on the PL path; memory floor for
  B=9 is only 45 × 2.2 GB = 0.11 s/run.
* with a CUDA graph per shape bucket (~1 µs/node): **≈0.12 s/run** (memory-bound) → **≈150×** PL; end-to-end
  **≈19–30×** (Amdahl-capped, §4.3).
* cost: `node` count `m` differs call-to-call, so the 9 calls must be **padded to max `m+1`** (padding with
  a zero Simpson weight is exact); graphs need per-shape buckets.

### 3.2 Option (ii) — across-replicate lockstep batch

Run B independent engine replicas in lockstep, one call-column at a time (call *c* for all B runs). Shapes
are identical across runs only up to cohort-size variation, so padding/culling is needed.

* memory per batched call = **B × (Suf + factors + Pre/tmp)**. With `(n+1)(d+1)(m+1)·4` = **22.18 MB** per
  replica (m+1=267; 16.70 MB at m+1=201) plus 0.64 MB factors plus 0.15 MB `Pre/tmp` ⇒ **≈23.0 MB/replica**.
* **B_max** on 12 GB with 2 GB headroom (`10,737,418,240 B` usable): **467** replicas pure-tensor; **≈420**
  after ~1 GiB CUDA context/allocator overhead (≈557 at the low node count). Recommend **B ≤ 400**.
* **B = 100**: 2.22 GB; per-call-batch traffic 27.0 GB ⇒ **29.6 ms/call** at 912 GB/s; 405 call-columns ⇒
  **≈12.0 s for 100 runs (8.3 runs/s)**; launches 405×2.7×10³ ≈ **1.10×10⁶** (5.5 s at 5 µs — under the
  memory time). This is **memory-bound**, so throughput is B-independent at ≈8.3 runs/s.
* **B = 5000**: 5,000 × 22.18 MB = **111 GB > 12 GB** ⇒ must chunk into **≥12 batches of ≤420**; time
  ≈12 × 48 s = **≈576 s (9.6 min)** for 5,000 runs; total launches ≈ **13.2×10⁶**. Throughput stays
  **≈8.7 runs/s** (memory-bound).
* cost: requires re-architecting the run harness into a lockstep scheduler (stateful, time-sequential engine),
  and it is only ~15× the throughput of the 10-core CPU box. **Not worth it.**

### 3.3 Recommended batching

**Option (i)**, the 9-call within-run batch. It needs no harness re-architecture (the tutoring loop already
has a recorded batched form), trivial memory (0.20 GB), and it delivers the same memory-bound throughput as
option (ii) while being local to two files.

---

## 4. ROOFLINE (Q4)

### 4.1 Why the CPU 9-call batch lost

The CPU variant was **memory-bandwidth bound**: it does not reduce bytes (9× the work is 9× the traffic),
and NumPy already streams the same bytes efficiently enough that batching only added transposes/overhead.
Measured **0.87–0.96×** (`CONTEST_MATH_PERF.md:103-104`). The number that explains it: the current CPU
implementation sustains only **≈4–5 GB/s effective** (247 MB / 50 ms/call) because of the strided
`cumsum(axis=1)` and the 300-step Python/numpy-loop structure. A GPU's 912 GB/s is **~190×** that effective
rate, and batching converts a launch-latency-bound problem on GPU into a bandwidth-bound one.

### 4.2 Roofline of the quadrature

| resource | budget | time for 368–405 calls |
|---|---|---|
| HBM traffic, unfused (same op sequence) | 405 × 247 MB = **100 GB**; 912 GB/s | **110 ms/run** ⇒ **168×** |
| HBM traffic, fused (suffix+cumsum in one pass; one suffix write + one read) | 405 × 45 MB = **18.2 GB** | **20 ms/run** ⇒ **921×** |
| FP32 compute | 20.1 GFLOP; 34 TFLOP/s | **0.6 ms/run** |
| FP64 compute (if DP were f64) | 20.1 GFLOP; 0.53 TFLOP/s (1/64) | **38 ms/run** |
| launch overhead, naive op-by-op torch (B=1) | 405 × 2.7×10³ = 1.1×10⁶ launches × 5 µs | **5.5 s/run** (dominates!) |
| launch overhead, 9-batch CUDA graph | 45 × 2.7×10³ × 1 µs | **0.12 s/run** |

So the **quadrature kernel's theoretical ceiling is ~170× (no fusion) to ~920× (fully fused)** on the PL
path — but that ceiling is unreachable at B=1 without fusion/CUDA graphs, because **kernel-launch latency
dominates everything else**. Realistic tiers: naive torch port B=1 ≈ **3×**; 9-batch eager ≈ **30×**;
9-batch + CUDA graph ≈ **150×**; fused Triton ≈ **370–920×** (all on the PL path).

### 4.3 What fraction of the 18.4 s is removable, and the Amdahl ceiling

PL is **18.40 s** of the shipped **18.904 s**; non-PL work is therefore **0.50 s**. That figure carries the
±5 % measurement variance quoted with the box runs (`CONTEST_MATH_PERF.md:66-68,139-141`), and the
attribution check gives 368 calls × 50 ms = 18.4 s ⇒ non-PL ≈ 0.5 s, while the reference build's
21.036 − 405 × 50 ms = 0.79 s ⇒ non-PL ≈ 0.8 s. So the **end-to-end Amdahl ceiling is
18.904 / (0.5–0.8 s) = 24–38×** (central ≈30×), no matter how fast the kernel is. With the recommended
9-batch+graph prototype (PL ≈ 0.12–0.2 s) the predicted end-to-end is **0.62–1.0 s ⇒ 19–30×**; with a fused
kernel (PL ≈ 0.02–0.05 s) it is **0.52–0.85 s ⇒ 22–36×**. **The binding limit is the remaining 0.5–0.8 s of
non-contest_math engine work, not the GPU.**

---

## 5. IN-REPO PRIOR ART (Q5)

**There is no GPU implementation of `contest_math` / the top-K PL projection anywhere in the reachable
worktrees.** `find` over `wt`, `wt2`, `wt3`, `wt4`, `wt5` for `contest_math*.py` returns only the CPU
module and its bench harness (in `wt4/auditv2` and this worktree); `pl_win_probs` appears only in CPU
Python. No `.cu`/`.cuh`/`.ptx` file exists anywhere under `/Users/treymenefee/neon-boot` (excluding
`node_modules`). So the search task (`docs/gpu/SEARCH.md`) and this one cannot collide on an existing
artefact.

**What the "recovered CUDA suite / sibling model" actually is.** It is the recovered
`unified_gpu_suite_2026_11_24.zip`, a **CuPy / raw-CUDA-kernel agent-based model** (`exp1_unified_gpu_abm.py`,
Philox RNG, N=250k, plus exp2/3/4 and its own PRE_REGISTRATION), being validated in a separate GPU lane at
`/root/work/gpu2` (`docs/audit/COMPUTE_SCHEDULE.md:530-538`). Explicitly: *"It is a **sibling model, not the
repaired gate engine**"* and *"the legacy GPU scripts in `/root/work/gpu` remain quarantined"*
(`COMPUTE_SCHEDULE.md:535,537-538`). The **RTX 3080 Ti numerics run** recorded in
`~neon-boot/wt3/gpu/research/records/2026-11-25-gpu-rtx3080ti/` is a *different* bundle: the PyTorch
`gpu_bray_abc_and_contest_surface*.py` (7-/6-parameter ABC + a 2,000-point **approximate** Tullock/PL
contest surface that uses the closed form `P_i = x_i^r/(x_i^r+A)`, **not** the top-K DP/quadrature;
`scripts/gpu_bray_abc_and_contest_surface.py:124-154`) and a float64 wild-cluster bootstrap
(`gpu_e1_q3_wild_cluster_ri.py`). It established the environment (`torch 2.7.1+cu118`, RTX 3080 Ti 12,288
MiB, cap 8.6, driver 595.71.05; `RUN_REPORT.md:9-11`) and a **GPU-vs-CPU determinism methodology** (referee
CPU-forced rerun, max abs 8.9e-15; `RUN_REPORT.md:11,181`; `docs/audit/gpu_abc_bundle/README.md:34`), and
that GPU conclusions are **quarantined** (`CORRECTED_GPU_EXPERIMENT_MANIFEST.json` `quarantine`;
`EXTERNAL_AUDIT_GPU_2026-11-25.md:113`, P0-07).

**Reusable pattern-wise:** the environment is already verified on the box; the batched-torch idiom
(`torch.Generator(device=...)`, `@torch.no_grad()`, one tensor op per batch) and the GPU-vs-CPU diff harness
are reusable as *templates*; **no kernel, scan, DP or Plackett–Luce code is reusable** — the sibling model's
contest path is a closed-form 2,000-point surface, not the engine's probabilistic object. The Gate-1
lesson to import is that the only GPU precedent passed its determinism comparison at 1e-14 **because it was
float64**; the contest_math path is float32.

---

## 6. RECOMMENDATION (Q6)

### 6.1 Verdict and the single decisive reason

**Verdict: NO-GO (as specified).** The single decisive reason: **the CPU reference's dynamic programme is
float32 (`contest_math.py:376`), so the campaign's ≤1e-12 admission criterion
(`COMPUTE_SCHEDULE.md:527`) forces bit-identical reproduction of NumPy's float32 reduction order; measured on
the real algorithm, changing only the `cumsum` association already moves `P` by 2.3e-9 (2,300× the gate),
a realistic reordered GPU kernel is 1e-8–1e-7 (10⁴–10⁵×), and even a more-accurate float64 kernel is
6.5e-8–6.1e-7. No GPU port can pass 1e-12; the only passing implementation would be a CPU-BLAS/NumPy
emulator, which is not the proposed work.**

**What would change the verdict to GO-WITH-DECLARED-DEVIATION:** a formal amendment of the criterion to
**≥3× @≤1e-6** (10⁴× inside the contract's 0.01/0.002 accuracy, 10³× inside the quadrature's own 2e-3 bound).
That is a Lead/Commander decision, not an analyst's. Under that amendment the port is feasible and the
predicted speed-up clears the 3× bar comfortably (§6.3). Under the current text, do not build it — the
effort would produce an artefact that cannot be admitted to the gate grid.

### 6.2 The one prototype (only under the amendment)

**A 9-call-batched PyTorch/CUDA-graph re-implementation of `_quadrature_win_probs`, wired into the tutoring
grid, CPU reference retained.** Concretely: (1) change the tutoring grid loop (`tutoring.py:338-350`) to form
the 9 weight vectors and call one batched `pl_win_probs_batch`; (2) implement the suffix DP, `cumsum`,
prefix DP, einsum and outer product as `torch` fp32 ops with an explicit **batch dim of 9** and `m`
padded to max-with-zero-Simpson-weight; (3) capture each shape bucket as a CUDA graph to kill the ~1.2×10⁵
launch overhead; (4) keep `pl_win_probs` (single-call) and the CPU path untouched as the oracle. Do **not**
port the exact DP (n≤20, not hot) or `pl_realize` (O(n) `argpartition`, `contest_math.py:620-672`).

### 6.3 Predicted speed-up (confidence range)

| implementation | PL path | end-to-end (18.904 s basis, non-PL 0.5–0.8 s) | confidence |
|---|---|---|---|
| naive torch, B=1, eager | ≈3× | ≈3× | high (launch-bound) |
| 9-batch eager | ≈30× (0.61 s) | **14–18×** | medium-high |
| **9-batch + CUDA graph (recommended)** | ≈130–150× (0.12–0.14 s) | **19–30×** | medium |
| fused Triton, single call | ≈370–920× (0.02–0.05 s) | **22–36×** | low (effort) |

**Predicted maximum achievable: ≈30× end-to-end (range 22–38×; hard Amdahl bound 24–38×); realistic for
the recommended prototype 19–30×; overall confidence range 10–30× (central ≈20×).** The gate's 3× speed-up
bar is met with margin under the amendment. (Note this is a *single-run latency* win on an idle GPU; with
540-replicate campaigns it also frees a contended 10-core CPU — but that is a scheduling benefit, not a
numerical one.)

### 6.4 The one experiment to run first (if told GO)

**A ~half-day, throwaway pure-PyTorch single-call port of `_quadrature_win_probs` (same op sequence, fp32,
no batching, no graphs), run through the existing 130-fixture equivalence harness** (`contest_math_bench.py`)
to measure **max |ΔP| vs the CPU reference** and its distribution, plus per-call GPU wall time and the
launch-vs-memory split. Expected outcome: max |ΔP| ≈ 1e-8–1e-7 (confirming §2.3 and *formally killing*
1e-12), per-call time ≈ 10–30 ms (confirming that B=1 is launch-bound and batching is mandatory). If
max |ΔP| lands >1e-6, stop and re-derive; if the launch split is not as predicted, the prototype design
(§6.2) changes before any CUDA-graph work.

### 6.5 Risks / exit criteria

1. **Numerics (decisive):** the amendment is a *policy* change; the deviation itself (≤1e-6) is
   scientifically inert against the 2e-3 quadrature bound and the 0.01/0.002 contract, but it breaks
   bit-equality with Gate-1 records (`CONTEST_MATH_PERF.md:113`) ⇒ any GPU campaign is a **new evidence set**
   with its own recorded environment and a mandatory re-run, not a re-computation of the existing one.
2. **Determinism (A5):** the GPU path must be deterministic (`ENGINE_INTERFACE_CONTRACT.md:106-117`); a
   fixed-order batched kernel is, but no atomics, no multi-stream reductions, and the shape-padding must be
   deterministic.
3. **Shape dynamism:** `m` varies per call (143–501 nodes), so batch padding + graph shape buckets are
   required; graph capture with dynamic shapes is the main engineering risk of the recommended prototype.
4. **Seat-sum invariant:** unaffected — `_renormalize_to_seats` (`contest_math.py:192-217`) and the engine's
   rescale (`core.py:452-461`; contract `:121-123`) make ΣP seats exact regardless of the ≤1e-6 deviation in
   individual `p_i`.
5. **Exit criteria:** abandon the port if the first experiment shows |ΔP| >1e-6 without an obvious fix, or
   if the amendment is refused.

---

## 7. SCRATCH / REPRODUCTION (the exact experiments behind §2.3; run locally, read-only)

All run with `/Users/treymenefee/neon-boot/venv/bin/python` (Python 3.10.2, NumPy 2.2.6) on the Mac; no
repo file is written. The harness copies the private helpers of `contest_math.py:305-415` verbatim and
perturbs exactly one reduction at a time; the full script is reproducible from the recipe below.

```python
# order probes (all measured True/False as stated in §2.2)
x = rng.random(69).astype(np.float32)*0.5+0.25
assert np.array_equal(np.cumsum(x), manual_sequential_f32(x))          # cumsum IS sequential
A,B = rng.random((69,267)).astype(np.float32), rng.random((69,267)).astype(np.float32)
e = np.einsum('am,am->m', A, B)
assert np.array_equal(e, np.diag(A.T @ B))                             # einsum IS BLAS matmul
assert not np.array_equal(e, np.sum(A*B, axis=0, dtype=np.float32))    # not pairwise
# deviation experiment (per config): build the reference P, then re-run with
#   (i) 2-block f32 cumsum association, (ii) np.sum for einsum, (iii) f64 DP,
#   (iv) float32 expm1/exp; report max|P_variant - P_ref| before and after renormalise.
# Results are the table in §2.3 (2.3e-9 .. 6.1e-7 vs gate 1e-12).
```

Command list actually used: `python feas2.py` (deviation table), `python feas3.py` (f64-dot reorder +
local cProfile), `python feas4.py` (bytes/FLOPs/memory budget), `python feas5.py`/`feas6.py` (cumsum order,
einsum==BLAS-diag). Scratch files live only under `/tmp`; nothing outside `docs/gpu/FEASIBILITY.md` was
written in the worktree.

---

## 8. VERDICT

> **NO-GO under the criterion as written (≥3× @≤1e-12, `COMPUTE_SCHEDULE.md:527`).**
> **Single decisive reason:** the CPU reference's dynamic programme is **float32**
> (`contest_math.py:376`), so ≤1e-12 can only mean *bit-identical* reproduction of NumPy's float32
> reduction order; measured on the real algorithm, the cheapest possible reorder (cumsum association alone)
> is **2.3e-9** and a realistic GPU reorder is **1e-8–1e-7** — **2,300× to 10⁵× above the gate**, while
> even a more-accurate all-float64 kernel is **6.5e-8–6.1e-7** above it. Only a NumPy+CPU-BLAS emulator
> could pass, which is not a GPU port.
>
> **Conditional:** if the Lead formally amends the criterion to **≥3× @≤1e-6** — a deviation 10⁴× inside the
> engine contract's own 0.01/0.002 accuracy target and 10³× inside the quadrature's 2e-3 error bound — then
> **GO-WITH-DECLARED-DEVIATION**, prototype = 9-call-batched PyTorch + CUDA graphs (§6.2), predicted
> **19–30× end-to-end (central ≈20×; Amdahl ceiling 24–38×)**, first experiment = single-call pure-torch
> port through the 130-fixture harness (§6.4). Without that amendment, do not build it.
