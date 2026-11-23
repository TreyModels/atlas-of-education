# Schooling as a dose of individuation: GPU port and rerun (23 November 2026)

## What this job did
1. Rewrote the life-course model from `research/records/2026-11-23-dose-model/` for GPU (T4, 16 GB): a
   standalone engine, documented callable interface and scale benchmarks, delivered as an artefact for the
   agent-based model in its own right.
2. Refitted on the **exact published CPU engine** with 5,000 prior draws per scenario at a fixed tolerance
   (948-1,044 equally weighted accepted draws each, plus an independent replicate of scenario A).
3. Found and fixed a **serious arithmetic defect in the previous fitting code** that very likely explains
   last session's "posterior looks like the prior" conclusion.

**Headline reversal:** on the exact engine with valid equal weights, the individuation scenario does **not**
beat development-only out of sample. Last session's "A better out-of-sample, 4 of 6 countries" does **not**
replicate here, and that earlier advantage is not established.

## (1) Fertility

### Does the individuation scenario beat development-only out of sample on held-out countries?
**No, and if anything the reverse.** Six held-out countries, 150 equally weighted accepted parameter draws
per scenario, prediction error against the observed series:

| | mean error (lower is better) | better in |
|---|---|---|
| individuation (scenario A) | 24.4 | 3 of 6 countries |
| development-only (scenario B) | 21.1 | 3 of 6 countries |

Difference (A minus B) **+3.3, 95% interval -3.8 to +11.1** — the interval spans zero, so the honest
statement is that the individuation scenario shows no out-of-sample advantage, not that it is worse.
Test designed to kill it: out of sample on countries never fitted, country effect predicted from the region
average, uncertainty from bootstrapping the 6 held-out countries. It kills the claim. Caveats: both scenarios fit badly in absolute terms (held-out errors 3.4 for
B to 56.9 for A in the worst country), and the tolerance is coarse, so this is a comparison of two poor
models. In-sample, by contrast, individuation fits better: best error 10.96 (replicate 10.72) against 14.39
for development-only, at equal tolerance. In-sample fit and out-of-sample prediction therefore disagree,
which is itself the finding: the individuation scenario's extra machinery buys in-sample flexibility, not
predictive accuracy.

### How strong is the kin-support effect?
**Not pinned down; the data cannot separate a trivial effect from a very strong one.** Equal-weight ABC
interval at the coarse tolerance: median **2.80, 90% interval 0.34 to 4.74** on a prior range of 0 to 5
(1,044 accepted draws of 5,000). The scale is the loss of kin support at a full dose of schooling, so the
median means a full dose keeps about **6% of kin support** (the interval runs from 71% kept to essentially
none). Test designed to kill it: an independent replicate fit on a different seed gives 2.73 with interval
0.37 to 4.78 — the two runs agree to a tenth of a standard deviation, so the search is *stable*, it simply
is not *informative*: the fitted spread is 0.96 of the prior spread. The same near-prior result appears in
the development-only scenario (2.73, 0.39 to 4.68), so the schooling channel is not what carries the
information. Reported honestly: this is a near-null identification result, not an estimate.

### How strong is cohort deepening?
**Same story.** Median **1.58, 90% interval 0.15 to 2.85** on a prior range of 0 to 3 (accepted sample as
above), replicate 1.62 (0.22 to 2.87), fitted spread 0.98 of the prior spread. Nothing here distinguishes
"no deepening" from "strong deepening inside the prior"; development-only gives 1.45 (0.12 to 2.85), which
is the same because that channel is nearly uninformative in both scenarios.

### How much of the fall in births is delayed versus never-born?
Between the 1940 and 1980 cohorts the model attributes the national fall mostly to children never born, and
the split depends on the scenario: individuation gives **2.09 never-born (fit countries) and 2.55 (held-out)
with -0.34 and -0.42 from delay**; development-only gives 1.69 and 0.69 never-born with -0.26 and +0.11
delay. The negative delay terms mean the model says births come slightly *earlier* as fertility falls, so
"delay" contributes nothing and the whole fall is quantum. Sample: 60 posterior draws per scenario, 14
countries, uncertainty widest for the held-out individuation case. **Treat this as a structural property of
the model, not a finding**: it reproduces last session's result, and the previous record already warned that
the model recovers delayed births and therefore cannot produce a delay-led fall. It is not a robust answer
to the question.

## (2) Massification

### The schooling allocation is carrying real signal, but the channel is loose
Test designed to kill the dose story: remove the within-cohort allocation of schooling (make who gets
schooling random inside each country-cohort, so the urban/wealth gradient that the dose channel runs through
is gone) and ask the fitted model to predict the observed data. Prediction gets **worse by 0.67 error units,
95% interval 0.31 to 1.07, in 7 of 8 fit countries** (120 posterior draws, same countries and targets). So
the fitted model can tell the real schooling allocation from a scrambled one. What it cannot do is say how
strong the mechanism is: the intervals in section (1) are as wide as the priors, so the evidence identifies
the direction of the dose channel, not its magnitude.

### Can the mechanism recover a known answer?
**Scenario choice: yes.** Synthetic observations generated from known values were re-predicted by both
scenarios' posteriors (120 draws each, 8 fit countries). Data generated by individuation are predicted
better by the individuation posterior (error 15.4 against 17.6, difference -2.2, 95% interval -6.5 to +1.7)
and data generated by development-only are predicted clearly better by the development-only posterior
(12.1 against 18.3, difference +6.2, interval +4.5 to +7.9). The right scenario wins both ways, so the
scenario comparison is meaningful in principle even though the real-data comparison is a tie.

**Parameter strengths: covered but not pinned down.** Observations were generated from a known parameter
vector, refitted, and the intervals checked. All five known values fall inside them (kin 2.2 inside 0.24 to 4.73; downward flow
2.5 inside 0.27 to 4.72; cohort deepening 1.0 inside 0.15 to 2.86; career delay 3.0 inside 0.38 to 7.62;
pickiness 2.0 inside 0.26 to 4.73; 4,911 accepted draws of 5,000, best error 3.45). The honest reading is
that this test has little power: the intervals are nearly as wide as the priors, so they would cover almost
any value in range, and every point estimate sits high by 0.3 to 1.0 units. Recovery is therefore not
demonstrated; the test is reported as passed-trivially, which is not the same as passed.
Separately, `results/falsifiers.json` also records a check previously labelled parameter recovery which
compares the *real-data* intervals with the numbers used to generate the synthetic data. It does not refit
anything and tests nothing about the estimator; it was relabelled in the file so it cannot be mistaken for
recovery evidence.

### Methods finding: the previous fitting code was arithmetically broken
The particle population's importance weights collapsed to a single draw: the largest weight was **0.995 of
the total and the effective sample size 1.01 of 600 kept draws** in scenario A, 4.79 in scenario B. Cause:
the particle density was accumulated in linear space; with a 31-dimensional parameter vector the exponential
underflows to zero for distant particles, every collapsed particle receives the same maximum weight, and one
takes all the mass. Recomputing in log space did **not** rescue it (2.5 of 600): the prior-over-proposal
ratio is genuinely explosive in 31 dimensions. The fix was to abandon importance weights: draw from the prior, keep every draw within a
fixed distance, give every kept draw equal weight (effective sample size = number of accepted draws by
construction). All numbers above come from that equal-weight run. **Implication: last session's
"posterior indistinguishable from the prior" was at least partly this arithmetic failure, so the earlier
posterior intervals should not be read as evidence about the model.**

## The GPU engine
The kernel reproduces its own reference exactly: for the same seed and parameter vector, woman-level states
(married, separated, parity, age at marriage, births by 30 and 35, age at first birth) agree with maximum
absolute difference 0, zero mismatched women over 6 configurations, and target series differing by 0.0. Throughput: on the T4, about **2.0 million simulated women per second** (1.9-2.2 million at 320 thousand
to 1.3 million women per launch); on the RTX 2080 Ti, **5.8 million women per second** at 10.1 million
women in one launch (1.75 s), which is 143 parameter draws per second and 1.1 GB of engine state. One
parameter draw of 24 runs costs 12.5 ms on the T4. Callable interface in `scripts/abm_dose.py`,
deterministic for a given seed (`results/bench_scale_2080ti.log`).

It is a **different engine** in its marriage market (a deterministic priority claim instead of a serial
random permutation), and the difference is measured, not assumed: with 200 seeds per country it marries
women -0.21 years differently on average (t = -5.4) at the two-round setting, +0.09 at one round, unchanged
at three or four, varying by country and period, while total and adolescent fertility are indistinguishable
(`results/PORT_NOTES.md`). It is **not a rerun of the published model and no bias correction is applied**;
its role is to test whether the A-versus-B verdict depends on the engine. The same A-and-B protocol was then run with the GPU engine *fitting* the parameters (batches of 8 parameter
draws = 192 runs per launch, `fit_gpu.py --batch 8`, 3,000 prior draws per scenario), and its fitted
populations were scored out of sample: **A 25.5 against B 21.7, difference +3.8 with 95% interval -2.6 to
+12.0, A better in 3 of 6 held-out countries**, against the exact engine's +3.3 (-3.8 to +11.1, 3 of 6).
**Precision about what this tests:** those held-out predictions were computed with the published CPU model in
both arms, so this shows that *the fitted population* and the A-versus-B verdict do not depend on which engine
did the fitting; it does not test prediction on the GPU engine itself (the transition record does that,
separately). What it does rule out is the worry that the GPU market's semantics were driving the fitted
answer. Both fits used the same tolerance and the same target protocol.

**Batch layout matters.** The engine is deterministic for a fixed seed *and a fixed batch layout*: each
woman's random stream is keyed on her position in the launch, so regrouping the same runs changes their
draws (up to 1.13 births and 1.74 years between one 12-run launch and batches of 5, 7, 12; audit in the
cuda-scale record's `determinism_v2.json`). The fits above pin and record `--batch 8`.

## Limits
The fit is poor in absolute terms and the tolerance is the prior-predictive 20th percentile (stricter cut the
posterior empty: zero of 750 prior draws reached the pilot tolerance), so these are coarse ABC summaries, not
precision claims; six held-out countries is a small sample; the delayed-versus-never-born split is structural.
## Files
`scripts/`: `kernel.cu`, `engine.py`, `dosecore.py`, `abm_dose.py`, `bench_scale.py` (GPU engine, interface,
scale benchmark), `ref_numpy.py` + `test_port.py` (porting test), `test_market.py` (engine-difference
measurement), `reject_abc.py` + `recover_coverage.py` (the quoted equal-weight fitter and its coverage check),
`falsifiers.py`, `falsifier_perm.py`, `analyze_cpu.py`, and the superseded `fit_cpu.py` / `fit_gpu.py`.
`results/`: quoted fits (`rej_fitA/B/A_rep.json`, `rec_fitA.json`), engine artefacts (`port_test.json`,
`PORT_NOTES.md`, `market_bias_postfix_17-31.json`, `bench_scale.json`, `bench_scale_2080ti.log`), analyses
(`analysis_holdout.json`, `analysis_holdout_gpuengine.json`, `analysis_decomp.json`, `analysis_stability.json`,
`stability_A.md`, `summary_A.md`), falsifiers (`falsifiers.json`, `falsifier_perm.json`), and the superseded
`cpu_fit*` / `fix_fit*` / `market_bias_prefix_17-30_superseded.json` kept so the methods trail is auditable.
