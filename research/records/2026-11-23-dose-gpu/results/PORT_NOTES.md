# GPU port: what it is, what the equivalence test proves, and how it differs from the published model

## Engine status (decision of record)
The **headline engine is the published CPU model** (`research/records/2026-11-23-dose-model/scripts/model.py`,
the original numba code, untouched). This GPU engine is a **second engine** that runs the same
A-and-B protocol so the paper can show whether the A-versus-B verdict depends on the engine. It is
**not a rerun of the published model** and must never be described as one.

## Structure
`kernel.cu` + `engine.py`: parallelism over women; a "run" is one parameter vector x country x
country-effect (14 cohorts x 2 urban/rural x 5 wealth quintiles x nW women); 192 runs batched per launch;
years stepped sequentially. Randomness is counter-based (Philox4x32-10) keyed on (woman, run, year), so
no draw depends on execution order, and `exp`/`log` are small Horner routines used identically on both
sides, because libm and CUDA device math differ in the last bit and that can flip a birth decision.

The marriage market is where this engine differs from the published model. The published model visits
the 60 women of a cohort x urban cell in a random permutation, one at a time, and each woman's search
sees the men already taken. The GPU engine instead lets every unmatched woman draw a priority, claim
one man, and the highest-priority claimant wins (`atomicMax` on a packed key, so ties are a total order
and the result is independent of thread scheduling). Later claim rounds let losers re-enter the market;
the family's arranged-marriage attempt happens once per year, as in the published model. The published
model's retry structure is reproduced exactly: the arranged path retries up to 8 times for an eligible
man, and the market samples up to three times the candidate count to assemble that many available men.

## What the equivalence test proves (scripts/test_port.py, results/port_test.json)
- numpy Philox versus CUDA Philox: identical bits (max difference 0 over 20,000 streams x 6 blocks).
- software exp/log: identical bits on both sides; both agree with libm to ~3e-16.
- 6 configurations (scenario A and B x seeds 1,2,3), same parameter vector: per-woman discrete state
  (married/separated, parity, age at marriage, births by 30 and by 35, age at first birth) maximum
  absolute difference **0, zero mismatched women**; all four fitted target series differ by **0.0**;
  aggregate arrays by at most 4.4e-15, which is the summation-order noise of `atomicAdd` on doubles.
- CUDA-graph replay is bit-identical to plain launches (<=3.6e-15), so the graphs used to remove launch
  overhead do not change the model.
This proves kernel == the numpy reference of the *same* algorithm. It does not, by itself, prove that
algorithm == the published model; that comparison is distributional and is the subject of the next
section.

## How far this engine is from the published model (200 seeds, same parameter vector)
Same prepared inputs, 3 countries, 200 seeds each, difference = GPU minus published CPU, with
t-statistics from the seed spread. Positive marriage age means the GPU engine marries women **later**.

Round-2 configuration, per country and period (mean age at first marriage, years):

| country | 1980 | 1985 | 1990 | 1995 | 2000 | 2005 | 2010 |
|---|---|---|---|---|---|---|---|
| Philippines | -0.19 | -0.25 | -0.26 | -0.27 | -0.29 | -0.58 | -0.33 |
| China | -0.04 | -0.12 | -0.10 | -0.18 | -0.22 | -0.17 | -0.12 |
| Egypt | -0.23 | -0.22 | -0.08 | -0.23 | -0.18 | -0.19 | -0.16 |

Pooled over the three countries, GPU minus published: mean marriage age **-0.21 years** (t = -5.4);
share married by 18 **+0.6 percentage points** (t = +1.7); total fertility **+0.07 births per woman**
(t = +1.7); adolescent fertility **+0.002** (t = +0.5). So total and adolescent fertility are
indistinguishable, and the difference sits in marriage timing.

The configuration matters. One claim round, which is the closest in spirit to the published model's
single visit per woman per year, gives marriage age **+0.09 years** (t = +3.5) and share married by 18
**-2.7 points** (t = -6.6). Two rounds give the row above. Three and four rounds are the same as two
(-0.22), so the value is not a convergence knob that can be wound to zero; it settles at a constant
that depends on which market configuration is chosen.

**Therefore: this is a different engine, not a measurement offset.** The deviation is a property of the
market semantics, it changes sign between configurations, it varies by country and period, and it does
not shrink with more claim rounds. It follows that (a) no single-offset bias correction is valid and
none is applied anywhere in this job, and (b) any number produced by this engine is a number about this
engine. The headline numbers come from the published CPU model; this engine's role is to test whether
the A-versus-B conclusion survives an engine whose marriage market is mechanically different.

## Throughput (bench.json, 23 Nov 2026, Tesla T4)
192 runs per batch: 0.10 s per batch, about 1,900 runs/s; one parameter draw (8 countries x 3
country-effects = 24 runs) costs 12.5 ms. The published numba model on one CPU core costs 9.5 ms per run
when the box is quiet and 20-70 ms when it is contended, i.e. 19-105 runs/s, so the port is about 18-98x
faster per CPU core and about 3-17x against the six cores this job was allotted.
