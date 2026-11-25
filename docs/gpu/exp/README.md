# Gate-1 / G2 experiment artifacts

Run on the AutoDL box (RTX 3080 Ti, torch 2.7.1+cu118), 1 process, `nice -n 10`,
`OPENBLAS/MKL/OMP=1`, GPU lane. Box load 16–36 on the 10-CPU cgroup throughout (Paper B campaign).

| file | purpose |
|---|---|
| `exp1.py` | torch float32 replica of `_quadrature_win_probs`; 130-fixture equivalence + 405-call unbatched benchmark |
| `exp2.py` | same arithmetic with **CUDA-graph replay**; the decisive G1 experiment (19.77x PL, 2.56e-8) |
| `perf_calls.json` | the real 405-call shape sequence captured from one HK Baseline run |
| `eq_check2.py` | integrated-engine equivalence: CPU reference vs GPU batch over the 130 fixtures |
| `eq2.json` | its output (per-fixture table; sha256 `0bb75933334537938f60f0fa993d50a5903e319a14ecfc2186d0e0b8d4d35915` on the box) |
| `bench_e2e.py` | one HK Baseline run, CPU vs GPU, single process (used for the 18.9 s / 4.9 s / 3.2 s numbers) |
| `bench_e2e2.py` | HK+KR, two runs each, CPU vs GPU in one process (headline table in BENCHMARK.md) |

## Result JSON, verbatim

```
G1 fixtures: n=130 n_quad=112 max_abs_diff=5.315e-08 mean=1.701e-08 t_cpu=8.11s t_gpu=9.04s pass_1e7=true
G1 405-call unbatched : t_cpu=20.348s t_gpu=6.034s speedup=3.37 max_abs_diff=2.557e-08
G1 405-call graphs    : t_cpu=19.872s t_prep=0.249s t_replay=0.756s t_gpu_total=1.005s
                        pl_speedup=19.77 e2e_cpu=21.80s e2e_gpu=2.94s e2e_speedup=7.43
                        max_abs_diff=2.557e-08 pass_dev=true pass_pl_3x=true pass_e2e_3x=true

G2 equivalence (integrated): max_abs_diff=4.832e-08 worst={n:400,seats:159,disp:2.0}
                             mean=1.698e-08 n_gt_1e7=0 n_gt_1e6=0

G2 e2e CPU: HK 18.883/18.942 CPU-s, KR 39.365/39.073 CPU-s
G2 e2e GPU: HK cold 4.909s warm 3.196s; KR rep1 9.664s warm 5.372s
            stats: 672 batches, 2496 rows, feed 1.300s, replay 8.540s, capture 5.866s (9 engines)
            run-level k12_spend: HK 7.2e-8 abs, KR 1.5e-7 abs vs CPU

Tests: CPU backend 101 passed (90.26 s); GPU backend 101 passed (87.25 s)  [whole engine tests/ tree]
```
