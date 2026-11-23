# Schooling as a dose of individuation: GPU port and rerun (23 November 2026)

## What this job did
Two things. First, the individual-level life-course model from
`research/records/2026-11-23-dose-model/` was rewritten to run on the GPU (Tesla T4, 16 GB). Second, the
model was refitted with far more parameter draws than the previous session, and the four questions the
brief asks were answered with uncertainty and with tests designed to kill them.

The **headline engine is the published CPU model, unchanged**. The GPU engine is a second engine: it is
fast, it is exact against its own reference, and it is now a standalone deliverable for the big
agent-based model in its own right — but its marriage market is mechanically different from the
published one, so it tests the A-versus-B conclusion rather than restating it (see "Engines" below).

## (1) Fertility
*[to be completed from the scenario-A and scenario-B fits]*

## (2) Massification
*[to be completed]*

## Engines: what was ported, what it costs, and how the two engines differ
The GPU port keeps the model's structure (14 countries x 14 five-year cohorts x urban/rural x 5 wealth
quintiles, schooling drawn from the panel's attainment shares, a yearly life course from age 15 to 49,
a two-sided marriage market and age-specific birth hazards) and changes two things the hardware forces:
parallelism is over women with years stepped sequentially, and the serial random-permutation marriage
market becomes a deterministic priority claim with two rounds. Randomness is counter-based, so no draw
depends on execution order.

Porting test (`results/port_test.json`): numpy and CUDA random streams are bit-identical; the software
exp/log used on both sides is bit-identical; for the same seed and parameter vector, woman-level discrete
states (married/separated, parity, age at marriage, births by 30 and 35, age at first birth) have
**maximum absolute difference 0 with zero mismatched women**, and all four fitted target series differ by
0.0. That proves kernel == reference. It does **not** prove reference == published model, and the
measured difference is reported in `results/PORT_NOTES.md`: with 200 seeds per country the GPU engine
differs from the published model in marriage timing, pooled -0.21 years at the two-round configuration
(t = -5.4), +0.09 years at one round (t = +3.5), unchanged at three or four rounds, with total and
adolescent fertility indistinguishable. That difference is market semantics, it varies by country and
period, and **no single-offset bias correction is valid or applied anywhere in this job**.

Kernel as a deliverable (`results/bench_scale.json`): ~2 million simulated women per second on one T4
(measured 1.9-2.2 million at 320 thousand to 1.3 million women per launch), one parameter draw (8
countries x 3 country effects = 24 runs = 40 thousand women) in 12.5 ms, and a documented callable
interface in `scripts/abm_dose.py` (parameters in, batched life-course summaries out, deterministic for
a given seed). Memory at 1.3 million women per launch: 141 MB of engine state. The limiting factor for
very large batches is host-side preparation of the schooling imputation, not the card.

## What is weak
*[to be completed: convergence, identifiability, structural weaknesses]*

## Files
`scripts/` — `kernel.cu` and `engine.py` (GPU engine), `dosecore.py` (shared constants, counter RNG,
bit-exact math), `ref_numpy.py` (independent reference for the porting test), `test_port.py` (the porting
test), `test_market.py` (the 200-seed engine-difference measurement), `fit_cpu.py` / `fit_gpu.py` (the ABC
fits), `analyze_cpu.py` (posteriors, diagnostics, held-out comparison, tempo/quantum), `abm_dose.py` (the
callable interface), `bench_scale.py` (throughput at scale).
`results/` — `port_test.json`, `PORT_NOTES.md`, `market_bias_postfix_17-31.json`, `bench_scale.json`,
`cpu_fitA.json`, `cpu_fitB.json`, `analysis_*.json`, `summary_A.md`.
