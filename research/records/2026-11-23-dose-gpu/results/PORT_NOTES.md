# GPU port: shape of the thing and what the equivalence test proves

## Structure
`kernel.cu` + `engine.py` run the identical life-course model as
`research/records/2026-11-23-dose-model/scripts/model.py`, with two changes forced by the hardware:

1. The unit of parallelism is a woman.  A "run" is one parameter vector x country x country-effect
   (14 cohorts x 2 urban/rural x 5 wealth quintiles x nW women).  Runs are batched onto the card, so
   one launch serves every parameter draw in the batch.
2. The marriage market is serial in the original (a random permutation of the 60 women of a
   cohort x urban cell, one at a time).  Here every unmatched woman draws a 32-bit priority, claims one
   man, and the highest-priority claimant wins via `atomicMax` on a packed key.  The key packs
   (year, arranged-vs-market flag, priority, woman index inside the cell), so ties are a total order and
   the result does not depend on thread scheduling.  Two claim rounds give losers a second chance,
   which is what the original gets by re-sampling at their turn.

Randomness is counter-based (Philox4x32-10) keyed on (woman, run x 1024 + purpose, block), so no draw
depends on execution order.  `exp`/`log` are small Horner implementations used identically on both sides,
because libm and CUDA's device math differ in the last bit and that can flip a birth decision.

## What the test proves (scripts/test_port.py, results in port_test.json)
- numpy Philox vs CUDA Philox: identical bits (max difference 0 over 20,000 streams x 6 blocks).
- software exp/log: identical bits on both sides (0 difference); both agree with libm to ~3e-16.
- 6 configurations (scenario A and B x seeds 1,2,3), same parameter vector:
  per-woman discrete state (married/separated, parity, age at marriage, births by 30 and 35, age at first
  birth) max absolute difference = 0, zero mismatched women;
  the four fitted target series (total fertility, adolescent fertility, mean marriage age, share married
  by 18) differ by 0.0 (largest 7e-15, which is double-rounding);
  aggregate arrays differ by at most 4.4e-15, the summation-order noise of `atomicAdd` on doubles.
- CUDA-graph replay is bit-identical to plain launches (<=3.6e-15), so the graphs used to remove launch
  overhead do not change the model.

## What it does NOT prove
The new engine cannot match the ORIGINAL cpu model draw-for-draw: the original consumes one numpy stream
in a data-dependent order and visits women in a random permutation, so any parallel rewrite must re-key
the randomness.  The comparison is therefore distributional (12 seeds, 3 countries, 3 country-effects):
total fertility and adolescent fertility differences are within Monte Carlo noise (|t| <= 1.0); mean
marriage age retains a small positive bias of +0.2 to +0.45 years (t up to 2.1 for Egypt) because a
woman whose claim is lost still marries somewhat later than in the serial market.  This is a known,
bounded residual, not a porting error, and it is reported with the fitted results.

## Throughput (bench.json, 21 Nov 2026, Tesla T4)
- 192 runs per batch: 0.10 s per batch => ~1,900 runs/s; one parameter draw (8 countries x 3
  country-effects = 24 runs) costs 12.5 ms.
- The original numba model on one CPU core: 9.5 ms per run when the box is quiet, 19-72 ms when it is
  contended, i.e. 19-105 runs/s -> the port is ~18-98x faster per CPU core; ~3-17x against the 6 CPU
  cores this job was allotted.
