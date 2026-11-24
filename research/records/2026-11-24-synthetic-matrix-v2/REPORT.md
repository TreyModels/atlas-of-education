# REPORT — heterogeneity matrix v2 (task-21, server region-42)

**Branch** `research/synthetic-matrix-2026-11-24`; record `research/records/2026-11-24-synthetic-matrix-v2/`.
**SIMULATION only; no causal language; no tuning toward a wall.** Server: region-42, 96 cores, RTX 2080 Ti
(GPU not used — no equivalence gate yet), NumPy 1.24.1, `multiprocessing.Pool(96)`, per-worker BLAS threads=1.
**Wall 155.3 s**; 6,720 cells.

## Headline numbers

| statistic | v2 | v1 (`be7e499`) | comparison |
|---|---|---|---|
| cross-world indistinguishable share | **1,752/6,720 = 26.07 %** | 55.6 % | E1 robust-travel 5/272 = 1.8 %; pre-declared wall rule ≥ 75 % |
| **dose ladder** (0× / 1× / 2× measurement error) | **22.5 % / 25.4 % / 30.4 %** | — | measurement error blurs worlds monotonically, but never approaches the 75 % wall |
| robust-across-groupings (link×spec×dose) | **P 71/84 (84.5 %), S 59/84, C 59/84, R 59/84, Rm 59/84 (70.2 %)** | P/S/C/R 14–15/21 | synthetic robustness remains far above E1's 1.8 % — the Q3 trap holds |

**Verdict: separable (wall not generable in this design).** Adding 256 typed-heterogeneous countries, a
measurement-error ladder and a misspecified Pritchett world (Rm, omitted tutoring channel) *lowers* the
cross-world indistinguishable share to 26.1 % — i.e. the opposite of the wall. Measurement error moves blur in
the expected direction (22.5 → 30.4 %) but cannot manufacture a 75 % wall. The synthetic multiverse still
labels most links "robust across groupings" (70–85 %), confirming that within-world robustness is not evidence
of a real link (E1's 1.8 % is the benchmark).

**Misspecification check:** Rm's robust share (59/84) equals the correctly specified R/C/S worlds; misspecifying
one channel does not collapse the worlds.

## Status / caveats

- Aggregation ran in one process after the 96-worker cell phase; the single-core robust scan is a driver
  inefficiency (fixed in the v2b driver design; v2 wall 155.3 s total).
- GPU not used: cupy 14.2.0 imports but no fixed-seed NumPy-vs-CUDA equivalence had been run at v2 time; no GPU
  number is reported.
- v2b (scale/replication: N=100,000, 512 countries, 10 blocks, 80 groupings, 6 specs, 504k regressions) is
  pre-registered (`PRE_REGISTRATION_v2b.md`) and queued.

## Files

`PRE_REGISTRATION.md`, `PRE_REGISTRATION_v2b.md`, `REPORT.md`,
`results/{matrix_v2_summary,matrix_v2_cells,run_manifest_v2}.json`, `synth_loop/run_matrix_v2.py`.
