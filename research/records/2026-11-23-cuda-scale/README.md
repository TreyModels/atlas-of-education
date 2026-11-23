# GPU life-course engine at scale: what it carries, how fast, and where it breaks

**Date:** 23 November 2026. **Hardware:** box2 AutoDL, one NVIDIA RTX 2080 Ti, 11 GB, 12-core
quota shared with other jobs. **Engine:** the GPU dose engine from
`research/records/2026-11-23-dose-gpu/` (kernel untouched; copied to `/root/work/cuda_scale`).
**Branch:** `research/cuda-scale-2026-11-23`. **Every number below is written to a JSON file in
`results/`; the file is named next to each table.**

This is an engineering audit, not a new demographic finding. It does **not** reopen the porting
work and does **not** claim the engine reproduces the published CPU model: that comparison is
distributional, the marriage-market deviation is documented in `2026-11-23-dose-gpu/results/PORT_NOTES.md`,
and every number here is a number about *this* engine.

## What was measured (all on the 2080 Ti)

A "run" is one full life course of 14 birth cohorts × 2 urban/rural × 5 wealth quintiles × 12 women
= **1,680 woman-records**, years 1945–2012 stepped one at a time (68 years). Runs are batched; one
launch serves every run in the batch.

### Speed vs population (`results/scale_ladder.json`; median of 3 graph replays; time includes copying results back to the host)

| population simulated | runs in one launch | per-launch wall time | women per second | engine memory | bytes per woman |
|---|---|---|---|---|---|
| 100,800 women | 60 | 0.049 s | 2.06 M/s | 16.6 MB | 165 B |
| 999,600 women | 595 | 0.212 s | 4.71 M/s | 165 MB | 165 B |
| 9,999,360 women | 5,952 | 1.946 s | 5.14 M/s | 1.65 GB | 165 B |
| 66,771,600 women | 39,745 | 12.70 s | 5.26 M/s | 10.99 GB | 165 B |

Small batches are launch-bound (2.1 M/s at 10^5), large batches saturate at ~5.1–5.5 M/s. Memory is
flat at **164.6 bytes per simulated woman**, so the ceiling is arithmetic: 11 GB ÷ 165 B ≈ 67 M
women. The 100-million figure is reached by batching: two launches of 50.4 M women took **18.35 s**
of pure compute (5.49 M/s) and **51.1 s end to end** including loading and first-launch warm-up
(`results/batch100m.json`).

### Ceiling (`results/ceiling_giant.json`)

The largest single launch that could be loaded and run is **39,745 runs = 66,771,600 women**, holding
**10.99 GB** of engine state. One more step of 250 runs (+420,000 women) fails with an out-of-memory
error while staging inputs, with only 36 MB left free. This is a hard physical limit of the card,
not a tuning choice; it is roughly 64× the whole US cohort of women (about 1.05 M live births per
year) in a single launch.

### The giant demonstration (`results/ceiling_giant.json`, key `giant`)

One launch of **66,771,600 synthetic women**: 556,430 family cohorts, 68 years, **4,540,468,800
(4.54 billion) woman-years simulated**, 10.99 GB of state, **12.70 s** per launch (21.3 s for the
first launch including compilation and capture), 5.26 M women/s. Sanity check: mean total fertility
across the first 1,000 runs is 4.80 in 1980 and 3.33 in 2012, the expected behaviour of draws spread
over the model's plausible range.

## Determinism and robustness (`results/determinism_v2.json`, `results/repeat3.json`)

**What is exactly repeatable.** Two independent engine instances with the same seed and the same
launch layout give **bit-identical per-woman state** (marriage, parity, education, ages at
marriage/first birth, births by 30 and 35): zero differing women. The aggregate arrays differ only
in the last bits (**at most 7.1 × 10^-15**) because they are summed on the device in a
scheduling-dependent order — the same documented property the port reported. CUDA-graph replay
versus plain kernel launches: per-woman state **bit-identical**, aggregates within 5.3 × 10^-15.
Enlarging the pre-allocated engine from 12 to 4,096 runs does not change results either.

**What depends on the layout.** The engine is deterministic given a pinned layout; what changes
with the layout is which random numbers each run receives. Two independent instances with the same
seed and the same batch layout are bit-identical per woman (question 1 above), so this is layout
dependence, not nondeterminism. For the same 12 parameter draws, grouping them differently across
launches changes the answers (`determinism_v2.json`, question 4; each row compared with the
one-run-per-launch layout):

| launch layout | max change in total fertility (births/woman) | max change in mean marriage age (years) |
|---|---|---|
| batches of 5 | 0.92 | 1.36 |
| batches of 7 | 0.95 | 1.42 |
| batches of 12 | **1.13** | **1.74** |

The cause is visible in the kernel: each woman's random stream is keyed on her *within-launch*
position, and each man's stream on the *total number of women in the launch* as well. Change how a
fixed set of draws is grouped, and different random numbers are handed out.

**Correction to the engine's own note.** `abm_dose.py` says "results do not depend on batch
composition". That statement is false and must be read as: **results are exactly reproducible only
if the launch batch size is pinned.** Operational consequence: a reproducible ABM run must fix the
launch batch size and record it in its run configuration; any downstream result produced with this
GPU engine (including runs made by the near-port) must state the batch size it used, because results
computed at different batch sizes are not comparable at the level shown above. Once the batch size
is pinned, everything above is exactly reproducible.

**Clock/thermal stability.** Repeating the 10-million-woman benchmark nine times (three fresh
instances × three timed replays): mean **1.868 s**, standard deviation **0.079 s** (**4.2%**),
range 1.738–1.954 s; the three per-instance medians were 1.906 ± 0.053 s. GPU temperature stayed at
39–46 °C and clocks held boost (1,860 MHz at this size; 1,350 MHz under the heavier 50 M-woman
batch), with no downward drift across repeats. Variance is warm-up and host-side copying, not
thermal throttling; treat throughput as ±4% and comparisons under ~5% as noise.

## (1) Fertility

At this scale the engine can run the individual life course of **tens of millions of women in one
launch, and 100 million in under 20 seconds of compute**, instead of a few hundred thousand. That
makes feasible fertility questions that need a population large enough for stable rates in small
cells: single-year age × parity × education × wealth × urban cells, rare events (very early or very
late births), and many parameter draws evaluated on the same population. It does **not** make the
engine's fertility estimates more *correct*: it is still the same model, and the honest reading of
the engine's own record is that its marriage-timing semantics differ from the published model in a
way that no single offset can repair. Scale buys precision and search width here, not validity.

What would falsify the throughput numbers: the independent repeats above (worst-case spread 4.2%)
and the ceiling probe stepping up until failure. What would falsify the giant demonstration: it is
one launch of synthetic draws — a rerun gives different numbers by construction of the draws; only
the speed, size and memory figures are the reproducible claims.

## (2) Massification

The engine makes feasible a massified ABM: one launch can carry **66.8 million women** (10.99 GB of
state, 12.7 s), and 100 million women fit in **two launches, 18.4 s of compute, 51 s end to end**.
For orchestration it is ready with one condition: the caller must pin the batch size and record it,
because batch size changes the random numbers each run receives (above; e.g. 1.13 births per woman
between the one-run-per-launch and all-in-one-launch layouts). The callable interface
(`abm_dose.simulate`: parameters in, arrays out) is deterministic given a fixed layout and needs no
GPU knowledge from the caller. The limits are honest: one consumer card, one GPU, no checkpointing
mid-run, and the 165 bytes/woman ceiling is hard — larger populations must be batched, not grown.

What would falsify the "ready for orchestration" claim: the batch-size dependence is exactly such a
test, and it fails in that one respect; it is reported, not hidden. No multi-GPU path was tested and
none is claimed.

## Files

`scripts/` — `benchlib.py`, `run_ladder.py` (speed ladder), `run_ceiling_giant.py` (ceiling +
giant ABM), `run_audit.py` (determinism v1, repeats, 10^8 batched), `run_determinism2.py`
(determinism decomposed). `results/` — `scale_ladder.json`, `ceiling_giant.json`, `batch100m.json`,
`determinism_v2.json`, `determinism.json` (superseded v1), `repeat3.json`, `ceiling.json`
(superseded first ceiling attempt, kept for the trace). Server working copy:
`/root/work/cuda_scale` (engine copied from `/root/work/dose_gpu`, untouched). Raw logs:
`run.log`, `run2.log`, `run3.log` on box2. Nothing here is provisional except: the giant-ABM
aggregate means are one synthetic draw set; the 100 M-women figure is two batches, not one launch.
