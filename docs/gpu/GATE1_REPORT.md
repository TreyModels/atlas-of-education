# GATE1_REPORT — GPU port of the PL hot path: verdict, decisive experiment, and what it buys

**Owner:** commander (`deepseek-gpu`). **Date:** 2026-11-25. **Branch:** `research/gpu-port-2026-11-25`,
base `e0508f3`. **Evidence class:** deterministic numerical engineering + measured performance. No empirical claim.
**Status:** Gate 1 CLOSED. **Amendment A-GPU-1 approved** by the human (2026-11-25): GPU path allowed at
max abs diff **≤1e-7** for the gate grid / sensitivity runs only; Paper B's preregistered primary stays CPU.

Inputs: `docs/gpu/SEARCH.md`, `docs/gpu/FEASIBILITY.md`, the box audit, `docs/audit/CONTEST_MATH_PERF.md`,
`CONTEST_MATH_VALIDATION.md`, `CONTEST_MATH_APPROX_ERROR.md`, `ENGINE_INTERFACE_CONTRACT.md` §1.3.

---

## 0. TL;DR (one screen)

| question | answer |
|---|---|
| Does the GPU port clear the amended gate? | **PASS.** max abs ΔP = **2.56e-8** on the 405 real HK-Baseline call shapes; **5.32e-8** on the 130 fixtures. Gate is 1e-7. |
| Does it clear the speed bar? | **PASS, with margin.** PL path **19.8×** (18.4 s → 1.0 s per run); end-to-end HK **7.4×** (21.8 s → 2.9 s). |
| How does it work? | torch float32, the 9 tutoring grid points batched into one DP, and the ~3000-op DP captured once per shape as a **CUDA graph** then replayed. The CPU cost was 50 % Python dispatch — the graph removes it. |
| Does this make the 5,000-run gate grid finish sooner? | **Only with Phase-3 cross-replicate batching.** Single-run GPU makes one run 7.4× faster but still runs one run at a time: 48 CPU-h → ~6.5 h wall on one GPU, i.e. a wash vs ~6 h at 8–10 CPU workers. Hybrid (1 GPU worker + 9 CPU workers) ≈ 2.9 h. Cross-replicate batching (B≈420) → **~10–20 min (estimated, not yet measured)**. |
| Cheapest alternative? | None beats it on effort/reward. DE-ICM (unreleased code, 1–2 days) might give 2–4× on CPU; the GPU port already gives 7.4× e2e and is the foundation for the batching path. |
| Decision taken | Build the full GPU port (G2). The open question is whether to fund Phase-3 cross-replicate batching, which is where the wall-clock win is. |

---

## 1. Verdict

**GO — under amendment A-GPU-1 (≤1e-7, gate grid / sensitivity only). The decisive experiment passed both
legs: deviation 2.56e-8 ≤ 1e-7, and PL-path speedup 19.8× (end-to-end 7.4×).**

This supersedes Gate 1's original framing. The original handoff gate (≤1e-12) was **not** a tolerance but a
bit-equality gate on float32 arithmetic, and is correctly rejected: see §2. The human accepted the declared
deviation on 2026-11-25. The remaining judgement is not numerical, it is economic (§4.4): a single-run port
saves CPU-hours but barely moves wall-clock on a 10-CPU box; cross-replicate batching is what moves it.

---

## 2. Why the original ≤1e-12 gate was wrong (record, not a pending decision)

The engine's DP storage is `float32` (`contest_math.py:376–402`), so `1e-12` is ~5 orders below float32
granularity and can only be met by reproducing the CPU's exact float32 rounding sequence. Measured facts:

| reduction | test | result |
|---|---|---|
| `np.cumsum(A, axis=1)` float32 (301,69,267) | vs explicit sequential accumulate | **bitwise equal** — reproducible |
| `np.einsum('am,am->m')` float32, a=0..68 | vs sequential / vs `np.sum` | **not equal**: 1.9e-6 abs, 1.2e-7 rel |
| final `np.dot(sw, kernel*G)` float64, len 267 | reorder risk | ~3.6e-15 — harmless |

`FEASIBILITY.md` sharpens this: NumPy routes that float32 einsum to **CPU BLAS sgemm**, whose reduction order
is CPU/build-specific, so the reference is not portable even between CPU machines. A bit-exact port would have
to emulate a BLAS build's order — unprovable and version-fragile. Meanwhile the *science* is nowhere near this
tight: the contract's accuracy spec is `max |P−P_mc| ≤ 1e-2`, `mean ≤ 2e-3`; the quadrature's own documented
truncation+Simpson error is **2e-3**. A 2.6e-8 deviation is ~5 orders inside the method's own error bar.
**The 1e-12 gate was measuring reproducibility, not correctness.**

---

## 3. Amendment A-GPU-1 (approved) and the numbers it is certified on

> GPU-backend runs are numerically equivalent to the CPU reference within **max abs 1e-7** and are declared
> *not bit-identical*. Allowed for gate-grid / sensitivity runs only; Paper B's preregistered primary and all
> headline numbers stay on the CPU path. Every GPU run manifest records: backend, deviation bound, measured max
> deviation, CPU/GPU comparison hash, fixture table.

**Acceptance ladder (human-approved 2026-11-25):** target **≤1e-7**; fallback **≤1e-6** only if the worst-case
fixture lands between the two (1e-6 is ~2,000× inside the module's own 2e-3 quadrature error and ~10,000×
inside the contract's 1e-2 spec); **>1e-6 is a stop-and-report**. Measured worst fixture is **5.32e-8**
(n=400, seats=196, dispersion 1.5) and 2.56e-8 on the 405 real call shapes — **the target was met and the
fallback was not used.** This binds FEASIBILITY.md's warning that a realistic reordered fp32 kernel can land in
8.8e-9–1.1e-7: measured is inside that range, near its good end.

Measured under this gate (box: RTX 3080 Ti, torch 2.7.1+cu118, 1 process, `nice -n 10`, BLAS/OMP=1):

| suite | scope | max abs ΔP | mean abs ΔP | gate |
|---|---|---|---|---|
| 130 fixtures (bench harness generator: n 12–600, all seats, disp 0–6) | 112 quadrature + 18 exact-DP (unchanged) | **5.32e-8** | 1.70e-8 | 1e-7 PASS |
| 405 real HK-Baseline call shapes (`perf_calls.json`: n 300/600, seats 69, m 130–152) | 405/405 | **2.56e-8** | 1.53e-8 | 1e-7 PASS |

The 68-test suite is run against the integrated backend in G2 (`EQUIVALENCE.md`); the mechanism is identical
(only `_quadrature_win_probs` is replaced; exact DP, `pl_realize`, `pl_win_probs_mc` untouched).

---

## 4. Speed: measured envelope

### 4.1 Where the CPU time went (why a GPU helps at all)

Per `CONTEST_MATH_PERF.md` §3.2, the PL path (405 calls = 18.37 s of 19.82 s) is **≈50 % Python dispatch**
(`_quadrature_win_probs` tottime 10.14 s: ~300 sequential item steps × ~6 array ops) and ≈50 % NumPy internals
(cumsum 4.75 s, einsum 2.69 s, clip 1.68 s). The arithmetic is trivial (~11 M float32 mul-adds/call); the cost is
dispatch plus intermediate-array traffic. That is exactly what batching + CUDA graphs remove.

### 4.2 Decisive experiment — measured, PASS

One HK Baseline run's real call shapes (`perf_calls.json`), same weights to CPU and GPU, same process, box:

| metric | CPU reference | GPU (batched-9 + CUDA graphs) |
|---|---|---|
| 405 PL calls | **19.87 s** | **1.005 s** (prep 0.249 + graph replay 0.756) |
| PL-path speedup | — | **19.8×** |
| end-to-end HK (PL + 1.93 s non-PL) | 21.80 s | **2.94 s** |
| **end-to-end speedup** | — | **7.4×** |
| max abs ΔP | — | **2.56e-8** |

Mechanism: two CUDA graphs (n=300 and n=600, d=68, padded m+1=169), batch of 9 calls per replay, 46 replays per
run. Sequential float32 scan preserved (matches the reference; costs nothing inside a graph), float64 `exp/expm1`
preprocessing on CPU (identical to the reference), torch's own fast float32 contraction for the tail sum (that is
where the 2.6e-8 comes from — allowed by the amendment).

Without graphs the same batched implementation is **3.37×** on the PL path (6.03 s) — a thin pass, and exactly
the margin problem the Lead flagged. **CUDA graphs are mandatory, not optional.**
Artifacts: `docs/gpu/exp/exp1.py`, `exp2.py`, logs `docs/gpu/exp/*.log` (hash-recorded).

**Reconciliation of the two speedup figures on record.** One Amdahl model, PL share 92.7 %:

```
e2e_speedup = (PL_cpu + nonPL) / (PL_cpu/S_pl + nonPL)
```

- PL-path-only speedup `S_pl` has **no ceiling** from Amdahl; the end-to-end speedup does.
- With `PL_cpu = 18.37 s` (cProfile) and `nonPL = 1.93 s` (20.3 − 18.37), `S_pl = 19.8` ⇒ **e2e 7.4×**;
  hard ceiling as `S_pl→∞` is **13.7×** (= 1/(1−0.927)). Using the memo build's smaller `nonPL ≈ 0.53 s`
  gives **e2e 12.3×**, still capped at 13.7×.
- FEASIBILITY.md's "19–30× e2e, Amdahl ceiling 24–38×" is **not attainable** on this call mix: 24× e2e would
  require `nonPL ≤ 0.42 s` *and* PL essentially free. Its 19–30× figure is a **PL-path** number, or it assumed
  a different non-PL split. We print only the model-consistent range: **PL 19.8× measured, e2e 7.4–12.3×,
  Amdahl cap 13.7×.** The decisive experiment arbitrates: measured **7.4×**.

### 4.3 Amdahl ceiling

PL is 92.7 % of the run, so even free PL caps at **13.7×** end-to-end. Measured 7.4× leaves ~1.9 s/run of
non-PL work as the next target; that is engine-side and out of scope for this lane.

### 4.4 The number that matters: wall-clock for the ≥5,000-run gate grid

The grid is ~5,000 runs ≈ **48 CPU-h** (prereg: 5,000 × 35 CPU-s, "≈6 h at 8 workers",
`GATE2_PREREGISTRATION.md` L63–68). Three options:

| option | wall for 5,000 runs | vs today |
|---|---|---|
| **A. today: 8–10 CPU workers** | **4.8–6.0 h** | 1× |
| **B. single-run GPU** — one GPU-assisted worker at 7.4× (=7.4 CPU-equivalents), 9 CPUs left | alone 6.5 h (**worse**); **hybrid 1 GPU + 9 CPU ≈ 2.9 h** | ~1.7× |
| **C. cross-replicate batched GPU** — B≈420 replicas × 9 grid = 3,780-way kernels | **≈10–20 min (estimated)** | **~20–35×** |

Memory bound for C: the suffix array is `(n+1)(d+1)(m+1)·4 B ≈ 22.2 MB/replica`; on 12 GB with 2 GB headroom
**B_max ≈ 420**; feasibility's memory model gives **8.3 runs/s at B=100** (B=100 → 12 s/100 runs), so 5,000 runs
= ~10 min at that throughput, ~20 min allowing for our measured dispatch floor. **C is estimated, not measured.**

**Plainly: the single-run port saves CPU-hours (48 CPU-h freed from the shared 10-CPU budget), not wall-clock.
Only cross-replicate batching beats the CPU box on wall-clock, and it is a bigger engineering job (vectorise
`core.py` over a replicate axis, or interleave independent runs at the PL call boundary). If we build only one
more thing, build that driver — the kernel it needs is already measured working.**

### 4.5 Option (c) priced at desk level: the algorithmic route (DE-ICM), no GPU

`SEARCH.md` found the 2026 state of the art: **DE-ICM** (Inariba 2026, arXiv 2610.06028) computes ICM/PL
placement probabilities deterministically in `O(M n²)` by deconvolution, worst abs error 1.1e-14, **0.2 s at
n=1000 on one CPU core; code not released**. The paper's own analysis says deconvolution beats prefix–suffix
when `m >> sqrt(n)` — we are at m=266 vs sqrt(300)≈17, i.e. squarely in that regime. Scaling their 0.2 s at
n=1000 to n=300 gives ≈18 ms/call, ~2.5× our current 45 ms on CPU, and it removes the `(d,m)` DP traffic wall.

| | DE-ICM CPU reimpl | GPU port (measured) |
|---|---|---|
| effort | ~1–2 days, from an unreleased paper (risk: medium) | ~1 day (prototype done) |
| dev vs our float32 reference | ~1e-7 (reference's own error) — same amendment class | 2.6e-8 |
| speed | ~2–4× on one CPU core (est.) | 19.8× PL / 7.4× e2e |
| dependency | none (pure NumPy) | GPU + torch + box |
| verdict | **not first**; useful later to shrink the GPU kernel's traffic further | **build this** |

We legally cannot lift DE-ICM code (none released); its *method* is public. MPL (Knyazev & Oosterhuis, ECIR
2026, Zenodo 17352314, **MIT**) is the one reusable artifact: batched PyTorch, deterministic, GPU-capable, the
same Poisson-binomial/exponential-race integral — the right template for the Phase-3 batched driver, but
validated only at K≤30, so it needs re-validation at our K=69–300.

---

## 4b. Accelerator inventory — "can anything speed up the matrix work, CPU or GPU?"

Scoped to a single engine run, ranked by where the seconds actually are.

**1. Where the matrix time is.** The PL DP tensor chain — `(n+1)×(d+1)×(m+1) = 301×69×267` float32: multiply/add,
`cumsum` axis=1, the `einsum` contraction, the float64 final dot — is **92.7 %** of the run. Everything else in
an HK run is ~1.45–1.93 s (7.3 %). So "matrix speedup" is the PL path first, and any non-PL matmul work is
rounding error.

**2. CPU levers — newly unlocked by the ≤1e-7/≤1e-6 amendment** (all were blocked by the old 1e-12 gate; this is
a real unlock, not a reframing):

| lever | idea | est. speedup | cost / risk |
|---|---|---|---|
| **(a) Deconvolution** (recommended CPU lever) | replace the materialised prefix+suffix DP with an `O(n)` leave-one-out synthetic division per item — no `Pre`/`Suf` tensors, no `cumsum` over 22 MB | **2–4× single-core** (DE-ICM: 0.2 s @ n=1000 ⇒ ~18 ms @ n=300 vs 45 ms today); could be more, since it removes the traffic wall outright | 1–2 box-days; stability needs clamp/deflation direction (p→1 cancellation); deviation vs float32 ref ≈1e-7 class, must be measured on the 130 fixtures |
| **(b) FFT Poisson-binomial** | compute the count distribution by polynomial convolution in float64 FFT, cast back | 1.5–3× on the count step | moderate complexity; float64 FFT error ~1e-15, far inside the 2e-3 method bound; deviation vs the float32 ref ~1e-7 (the ref's own error) |
| **(c) Low-risk cleanups** | `opt_einsum`/`bmm` contraction order, in-place ops and no temporaries, contiguous layouts, keep the DP float32 | 1.1–1.3× | hours; note BLAS threading is already optimal at 8 workers × 1 thread — **do not retune it**, that steals from the campaign |

**3. GPU levers.** Box has torch 2.7.1+cu118 (cuBLAS), PyPI reachable, CuPy absent but installable (not needed).
Relevant pattern: batched GEMV/GEMM across replicates via `torch.bmm`, **CUDA graphs** to remove the ~1,800 small
kernels per call (measured: 3.4× without → **19.8×** with), and Triton/`numba.cuda` fusion into one persistent
kernel if we want more (**est. 2–5× beyond graphs on the PL path**; not built). float32 is mandatory (3080 Ti
fp64 = 1/64). **Explicitly: a single-run GPU port is launch/transfer-bound; the big win needs cross-replicate
batching** (§4.4).

**4. The non-PL 7.3 %.** Even 10× there saves ~6.7 % of a run (≈1.35 s/run, ~1.9 CPU-h over 5,000 runs). There
is no single big matmul to batch — it is household loops in NumPy. Two lines. Drop it.

**5. If we could build only ONE new thing.** Rank:

1. **Cross-replicate batched GPU driver (Phase 3)** — the only option that beats the CPU box on wall-clock
   (5,000-run grid ~10–20 min vs 4.8–6 h). Cost ~3–5 box-days. Its kernel is already measured working.
2. **GPU port** (approved, built, measured 7.4× e2e) — cost already spent (~1 box-day); frees 48 CPU-h of budget.
3. **CPU deconvolution** — 1–2 box-days for 2–4× on a single CPU core; superseded by the GPU on throughput, but
   it is the best option if the GPU must be freed for another project, and it would make the GPU kernel faster too.

---

## 5. Prior art (from `docs/gpu/SEARCH.md`; citations verified by the Lead)

**Recommendation: ADAPT + IMPLEMENT — no drop-in reuse exists.**

| artifact | license | what it is | fit |
|---|---|---|---|
| **MPL**, Knyazev & Oosterhuis, ECIR 2026 — [Zenodo 17352314](https://zenodo.org/records/17352314) | **MIT** | batched PyTorch, deterministic top-K PL placement probs, same integral + prefix/suffix leave-one-out | **ADAPT** for the batched driver; K≤30 validated, needs re-validation |
| **DE-ICM**, Inariba 2026 — [arXiv 2610.06028](https://arxiv.org/abs/2610.06028) | paper CC BY; **code not released** | `O(Mn²)` deterministic deconvolution, 1.1e-14, 0.2 s n=1000 CPU | method worth pricing (§4.5) |
| **LAQI**, Wolters 2026 — [github](https://github.com/curesive/log-age-quadrature-icm) | MIT | deterministic, same integral, equities only | oracle only |
| **Biscarri/Zhao/Brunner 2018** — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0167947318300082) | paper | Poisson-binomial O(n²) DF algorithm MPL/DE-ICM build on | background |
| **FPRev** — [github](https://github.com/peichenxie/FPRev) | (paper/code) | reveals NumPy/PyTorch accumulation order CPU vs GPU | not needed under the amendment |

**What does not exist** (so we do not claim novelty or waste a search): no GPU implementation of this engine's
PL hot path anywhere; no released DE-ICM code; no bit-exact PL/ICM implementation on any hardware; no
NumPy-order-emulation library for GPU. Only three numerical implementations of this integral exist
(DE-ICM, MPL, LAQI). Licensing blockers found and avoided: `torch-choice` and `erdman/plackett-luce` have **no
license file**; `PlackettLuce` (R) is **GPL-3**. The in-repo "recovered CUDA suite" is a CuPy ABM + a PyTorch
ABC/closed-form-Tullock surface for a *sibling* model — nothing reusable kernel-wise; its 8.9e-15 GPU-vs-CPU
agreement was on float64.

---

## 6. What was run (reproducibility)

All on the box, 1 process, `nice -n 10`, `OPENBLAS/MKL/OMP=1`, GPU lane; CPU campaign (`/root/work/newgen`)
untouched and never written:

```bash
cd /root/work/gpuport
nice -n 10 /root/miniconda3/bin/python exp1.py --mode both --seq-scan   # 405 calls + 130 fixtures, unbatched GPU
nice -n 10 /root/miniconda3/bin/python exp2.py                          # 405 calls, batched-9 + CUDA graphs
```

Reference module deployed at `/root/work/gpuport/ref/contest_math.py`,
sha256 `cd7b5ba6cb55d250dfce9479cfd6b3d8dfcd7cf4120208ecd26c4116a0ab38bb` (identical to the worktree file).
`perf_calls.json` = the real 405-call shape sequence captured from one HK Baseline run.

**Artifacts (staged; to be committed under `docs/gpu/exp/` in the G1 commit — they are currently outside this
task's write scope, copies in `/tmp/gpuexp/` on the Mac and `/root/work/gpuport/` on the box):**

| artifact | sha256 |
|---|---|
| `exp1.py` (unbatched GPU replica + 130-fixture equivalence) | `2253b68134b2e4cd1901de1015a8b41a01001417001c256d774b347847f9255b` |
| `exp2.py` (batched-9 + CUDA-graph replay benchmark) | `f0dbb957dd5dbba476470bcdb13884485b7027d21d04bd95003d94feac5e3f05` |
| `perf_calls.json` (405 real call shapes) | `541127840fdb8e6bb4acf304043502371700d04acc8aa4774ecbbcd1af52d765` |

Result JSON, verbatim from the two runs:

```
fixtures: n=130 n_quad=112 max_abs_diff=5.315e-08 mean=1.701e-08 t_cpu=8.11s t_gpu=9.04s pass_1e7=true
bench   : n_calls=405 n_groups=47 M1=169 t_cpu=20.348s t_gpu=6.034s speedup=3.37 max_abs_diff=2.557e-08
bench_graphs: n_calls=405 n_batches=46 t_cpu=19.872s t_prep=0.249s t_replay=0.756s t_gpu_total=1.005s
              pl_speedup=19.77 e2e_cpu=21.80s e2e_gpu=2.94s e2e_speedup=7.43
              max_abs_diff=2.557e-08 mean=1.534e-08 pass_dev=true pass_pl_3x=true pass_e2e_3x=true
```

---

## 7. Risks / unknowns (post-experiment)

| risk | status |
|---|---|
| torch per-op dispatch dominates without graphs | **confirmed and solved** (3.4× → 19.8× with graphs) |
| graph capture per (n,d,m) shape too costly | **not a problem**: 2 shapes per HK run; capture is one-off per shape |
| deviation > 1e-7 on some fixtures | **clear**: worst 5.32e-8 over the 130-fixture sweep, 2.56e-8 on real shapes |
| box contention distorts timing | CPU ref and GPU measured in the same session; CPU ref 19.87 s matches the banked 18.37–20.35 s band |
| cross-replicate batching estimate wrong | **open** — Phase-3 estimate (~10–20 min) is a memory model, not a measurement |
| engine integration changes semantics | low — only `_quadrature_win_probs` is replaced; exact DP/realize/MC untouched; behind a flag, default off |
| integer/float variance across seeds at 1e-7 | low — deviation splits between two independent numerical realizations; aggregate statistics unaffected at the 2e-3 method error |
| worst-case fixture could land in (1e-7, 1e-6] | **human pre-approved the ≤1e-6 fallback** (2026-11-25); measured worst is 5.32e-8, so not used. Anything >1e-6 stops and reports. |

**Abandon criteria:** deviations >1e-7 in the 68-test suite or on a second jurisdiction (KR); any measurable
slowing of the CPU campaign; the batched driver requiring changes to engine semantics rather than call plumbing.

---

## 8. What this report claims and does not

- **Claims:** the GPU backend reproduces the CPU PL path within 2.6e-8 on real HK call shapes and 5.3e-8 on the
  130 fixtures; it is 19.8× faster on the PL path and 7.4× end-to-end on an HK Baseline run; CUDA graphs are
  required; the wall-clock win for the gate grid requires cross-replicate batching.
- **Does not claim:** bit-identity (explicitly refused); any Paper-B-primary use; any measured cross-replicate
  throughput; any change to the CPU reference or to Gate-1 evidence; any empirical/scientific claim.
