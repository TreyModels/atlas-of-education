# EQUIVALENCE — GPU backend vs the float32 CPU reference (amendment A-GPU-1)

**Owner:** commander (`deepseek-gpu`). **Date:** 2026-11-25. **Branch:** `research/gpu-port-2026-11-25`,
base `e0508f3`. **Evidence class:** deterministic numerical equivalence, measured on the AutoDL box.

**Declared deviation (human-approved 2026-11-25).** The GPU backend is **not bit-identical** to the CPU
reference. Its declared equivalence bound is **max abs diff <= 1e-7** on the probability vector, with a
human-approved fallback of **<=1e-6** if the worst case had landed between them; **>1e-6 stops the lane**.
The measured worst case is **4.832e-08**, so the fallback was **not used**.
**Scope: gate-grid / sensitivity runs only.** Paper B's preregistered primary computations and any headline
number stay on the CPU path.

Context for why this bound is scientifically safe: the module's own documented quadrature error is **2e-3**
(truncation + Simpson), the contract's accuracy spec is `max |P-P_mc| <= 1e-2`, `mean <= 2e-3`
(`ENGINE_INTERFACE_CONTRACT.md` §1.3), and the approximation the repair removed was <=2 pp. The declared bound
is **~2e4 inside** the method's own error, i.e. the GPU and CPU are two numerical realizations of the same
model, not two models.

## 1. Result summary

| check | result | bound | verdict |
|---|---|---|---|
| 130-fixture sweep, integrated engine, GPU batch path vs CPU reference | **max abs dP = 4.832e-08**, mean = 1.698e-08 | 1e-7 | **PASS** |
| fixtures exceeding 1e-7 | **0 / 130** | 0 | PASS |
| fixtures exceeding 1e-6 | **0 / 130** | 0 | PASS (fallback unused) |
| worst fixture | **n=400, seats=159, dispersion=2.0, dP=4.832e-08** | 1e-7 | PASS |
| 68-test contract suite, CPU backend | **68 passed** (13.49 s, box) | all pass | PASS |
| contract suite + GPU tests, GPU backend (`ATLAS_PL_BACKEND=gpu`) | **74 passed** (68 contract + 6 new GPU/batch tests, 17.14 s, box) | all pass | PASS |
| CPU batch path vs per-row loop | **bit-identical** (`np.array_equal`, 3 parametrisations) | bit-identical | PASS |
| 405 real HK call shapes (experiment harness, `GATE1_REPORT.md` §4.2) | max abs dP = 2.56e-8 | 1e-7 | PASS |

The GPU path is exercised by dedicated tests in `tests/test_contest_math_gpu.py` (skipped if torch/CUDA is
absent): one asserts the CPU batch is bit-identical to the per-row loop, the other asserts
`max|dP| <= 1e-7` and the `sum(P) = seats` invariant for the GPU batch at (300,36), (300,69), (600,69).

## 2. Run-level effect (what a deviation of ~2e-8 does to a whole simulation)

The declared bound is on `P`. A whole run also contains discrete decisions, so run-level scalars can differ
slightly more than `P` does — they are **not** covered by the 1e-7 bound and must be reported as such:

| run (seed 0, HK/KR Baseline) | CPU `k12_spend` | GPU `k12_spend` | run-level abs diff |
|---|---:|---:|---:|
| HK | 156.50693492937242 | 156.506934857395 | **7.2e-8** |
| KR | 134.8723207581624 | 134.87232060431376 | **1.5e-7** |

Both are below any reported precision (values are reported at 3–6 significant digits) and ~1e4–1e5 inside the
method's own 2e-3 error. A GPU run manifest records the per-run observed `max|dP|` (see `INTEGRATION.md`); the
run-level scalars are recorded alongside the CPU reference for any GPU run that is compared.

## 3. Why the deviation exists (one paragraph)

The reference stores the Poisson-binomial DP in **float32** (`contest_math.py:390–402`) and contracts with
`np.einsum("am,am->m")`, which NumPy routes to **CPU BLAS sgemm**; its float32 reduction order is a
CPU/build-specific implementation detail (`FEASIBILITY.md` §2). The GPU backend keeps the reference's float64
preprocessing (normalisation, Simpson grid, `expm1`/`exp` then cast to float32) **on the CPU**, keeps the
sequential float32 scan, and reorders only that one contraction (torch's float32 sum). The result differs by the
order of ~69 float32 additions — measured 1.7e-8 mean, 4.8e-8 max. Reproducing it bit-for-bit would mean
emulating a BLAS build, which is version-fragile and unprovable across a 5,000-run grid (`GATE1_REPORT.md` §2).
That is why the human accepted a declared bound instead.

## 4. Reproduce

On the box (1 process, `nice -n 10`, BLAS/OMP=1; runs occurred at box load 23–30 on the 10-CPU cgroup):

```bash
cd /root/work/gpuport/e2e           # engine + tests deployed from the worktree
# 68-test contract suite, CPU backend (bit-identical reference path)
PYTHONPATH=$PWD/engine OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  nice -n 10 /root/miniconda3/bin/python -m pytest tests/test_contest_math.py tests/test_contest_math_gpu.py -q
# contract suite + GPU/batch tests with the GPU backend registered
ATLAS_PL_BACKEND=gpu PYTHONPATH=$PWD/engine OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  nice -n 10 /root/miniconda3/bin/python -m pytest tests/test_contest_math.py tests/test_contest_math_gpu.py -q
# 130-fixture equivalence sweep (writes EQ2_JSON on stdout)
ATLAS_PL_BACKEND=gpu PYTHONPATH=$PWD/engine OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  nice -n 10 /root/miniconda3/bin/python eq_check2.py | tail -1 | sed 's/^EQ2_JSON //' > eq2.json
```

Artifact (box `/root/work/gpuport/e2e/eq2.json`): sha256
`0bb75933334537938f60f0fa993d50a5903e319a14ecfc2186d0e0b8d4d35915`.

## 5. Full per-fixture table (130 fixtures, integrated engine, GPU batch vs CPU reference)

Generator: identical to `docs/audit/code/contest_math_bench.py::fixtures` (seed 20261125;
`n` in {12,20,21,40,60,80,120,200,300,300,300,400,600}, random seats, dispersion
{0,0.25,0.5,1,1.5,2,3,4,6}). Rows with `n <= 20` use the unchanged exact-DP CPU path (dP = 0).

| n | seats | disp | max abs dP |
|---:|---:|---:|---:|
| 80 | 29 | 0.25 | 1.480e-08 |
| 12 | 7 | 6.0 | 0.000e+00 |
| 300 | 176 | 0.5 | 2.710e-08 |
| 20 | 16 | 4.0 | 0.000e+00 |
| 21 | 3 | 1.0 | 5.551e-17 |
| 80 | 57 | 0.25 | 1.844e-08 |
| 300 | 215 | 6.0 | 3.186e-08 |
| 60 | 50 | 0.25 | 8.292e-09 |
| 600 | 192 | 4.0 | 4.345e-08 |
| 120 | 4 | 4.0 | 5.551e-17 |
| 300 | 124 | 3.0 | 2.818e-08 |
| 40 | 31 | 0.25 | 1.119e-08 |
| 600 | 553 | 4.0 | 2.200e-08 |
| 300 | 122 | 2.0 | 3.196e-08 |
| 12 | 1 | 0.5 | 0.000e+00 |
| 60 | 33 | 2.0 | 1.966e-08 |
| 21 | 15 | 0.5 | 9.914e-09 |
| 40 | 35 | 3.0 | 1.839e-09 |
| 12 | 4 | 4.0 | 0.000e+00 |
| 20 | 9 | 3.0 | 0.000e+00 |
| 200 | 183 | 3.0 | 1.511e-08 |
| 80 | 69 | 1.5 | 1.375e-08 |
| 300 | 86 | 3.0 | 2.679e-08 |
| 120 | 19 | 2.0 | 2.478e-08 |
| 20 | 8 | 3.0 | 0.000e+00 |
| 600 | 534 | 4.0 | 1.805e-08 |
| 300 | 52 | 0.5 | 1.332e-08 |
| 120 | 92 | 3.0 | 2.329e-08 |
| 20 | 11 | 6.0 | 0.000e+00 |
| 40 | 26 | 2.0 | 2.073e-08 |
| 120 | 19 | 3.0 | 9.580e-09 |
| 12 | 4 | 1.0 | 0.000e+00 |
| 200 | 36 | 0.5 | 1.485e-08 |
| 200 | 89 | 1.0 | 3.240e-08 |
| 20 | 17 | 3.0 | 0.000e+00 |
| 600 | 406 | 1.0 | 3.582e-08 |
| 60 | 35 | 3.0 | 2.813e-08 |
| 120 | 79 | 4.0 | 1.696e-08 |
| 300 | 28 | 4.0 | 2.423e-08 |
| 600 | 66 | 0.5 | 1.327e-08 |
| 400 | 229 | 2.0 | 3.770e-08 |
| 120 | 48 | 1.5 | 2.363e-08 |
| 400 | 113 | 2.0 | 2.282e-08 |
| 120 | 92 | 0.0 | 1.893e-08 |
| 120 | 81 | 6.0 | 1.259e-08 |
| 300 | 244 | 0.0 | 2.566e-08 |
| 300 | 50 | 6.0 | 3.588e-08 |
| 12 | 7 | 6.0 | 0.000e+00 |
| 21 | 11 | 2.0 | 8.541e-09 |
| 300 | 194 | 0.5 | 2.532e-08 |
| 300 | 87 | 1.0 | 3.517e-08 |
| 60 | 16 | 1.0 | 1.192e-08 |
| 40 | 26 | 4.0 | 1.306e-08 |
| 200 | 195 | 4.0 | 5.198e-09 |
| 200 | 181 | 2.0 | 9.583e-09 |
| 120 | 81 | 0.25 | 2.207e-08 |
| 300 | 53 | 1.5 | 2.862e-08 |
| 120 | 110 | 1.0 | 1.234e-08 |
| 40 | 6 | 0.25 | 3.880e-09 |
| 80 | 35 | 6.0 | 1.345e-08 |
| 60 | 38 | 6.0 | 1.918e-08 |
| 12 | 11 | 0.0 | 0.000e+00 |
| 400 | 196 | 1.5 | 4.697e-08 |
| 600 | 60 | 4.0 | 2.689e-08 |
| 21 | 6 | 0.5 | 6.910e-09 |
| 200 | 131 | 1.5 | 2.965e-08 |
| 300 | 2 | 3.0 | 2.776e-17 |
| 120 | 34 | 1.0 | 2.120e-08 |
| 40 | 19 | 1.5 | 1.192e-08 |
| 300 | 100 | 6.0 | 2.886e-08 |
| 300 | 18 | 1.5 | 1.024e-08 |
| 600 | 107 | 3.0 | 3.597e-08 |
| 300 | 182 | 2.0 | 2.915e-08 |
| 40 | 18 | 4.0 | 1.738e-08 |
| 300 | 168 | 2.0 | 2.862e-08 |
| 80 | 43 | 0.0 | 2.298e-08 |
| 300 | 263 | 0.25 | 1.833e-08 |
| 200 | 192 | 0.5 | 6.443e-09 |
| 300 | 288 | 0.5 | 1.115e-08 |
| 200 | 126 | 0.0 | 2.582e-08 |
| 300 | 179 | 4.0 | 2.386e-08 |
| 300 | 16 | 3.0 | 2.054e-08 |
| 400 | 45 | 0.5 | 1.636e-08 |
| 300 | 60 | 0.0 | 1.263e-08 |
| 60 | 26 | 0.5 | 3.654e-08 |
| 200 | 159 | 4.0 | 2.700e-08 |
| 300 | 56 | 0.0 | 1.139e-08 |
| 200 | 175 | 0.0 | 9.024e-09 |
| 400 | 268 | 2.0 | 3.634e-08 |
| 120 | 63 | 2.0 | 2.386e-08 |
| 600 | 66 | 2.0 | 2.506e-08 |
| 300 | 218 | 0.0 | 3.359e-08 |
| 300 | 198 | 4.0 | 1.922e-08 |
| 21 | 12 | 0.0 | 1.336e-08 |
| 40 | 22 | 0.5 | 2.416e-08 |
| 60 | 39 | 2.0 | 1.505e-08 |
| 80 | 22 | 3.0 | 2.248e-08 |
| 60 | 36 | 3.0 | 6.862e-09 |
| 40 | 28 | 2.0 | 1.535e-08 |
| 600 | 37 | 1.0 | 1.218e-08 |
| 80 | 42 | 2.0 | 2.138e-08 |
| 21 | 7 | 2.0 | 1.934e-08 |
| 12 | 2 | 3.0 | 0.000e+00 |
| 12 | 7 | 4.0 | 0.000e+00 |
| 120 | 63 | 6.0 | 2.287e-08 |
| 200 | 21 | 6.0 | 2.190e-08 |
| 120 | 108 | 3.0 | 1.094e-08 |
| 21 | 2 | 4.0 | 1.388e-17 |
| 200 | 144 | 1.5 | 3.598e-08 |
| 300 | 146 | 1.0 | 3.153e-08 |
| 21 | 16 | 2.0 | 4.307e-09 |
| 120 | 18 | 1.5 | 1.025e-08 |
| 200 | 70 | 3.0 | 2.640e-08 |
| 12 | 9 | 2.0 | 0.000e+00 |
| 80 | 14 | 1.5 | 1.077e-08 |
| 12 | 4 | 4.0 | 0.000e+00 |
| 300 | 55 | 1.5 | 2.890e-08 |
| 200 | 14 | 6.0 | 2.298e-08 |
| 400 | 159 | 2.0 | 4.832e-08 |
| 20 | 8 | 4.0 | 0.000e+00 |
| 12 | 5 | 1.0 | 0.000e+00 |
| 400 | 201 | 0.5 | 3.712e-08 |
| 300 | 245 | 3.0 | 2.508e-08 |
| 21 | 6 | 0.5 | 9.941e-09 |
| 200 | 15 | 0.0 | 3.865e-09 |
| 80 | 49 | 6.0 | 1.502e-08 |
| 40 | 4 | 6.0 | 1.110e-16 |
| 300 | 248 | 2.0 | 2.701e-08 |
| 20 | 9 | 3.0 | 0.000e+00 |
| 60 | 7 | 1.5 | 5.422e-09 |
