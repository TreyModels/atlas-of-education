# Schooling as a dose of individuation: GPU port and rerun (23 November 2026)

## What this job did
1. Rewrote the individual-level life-course model from `research/records/2026-11-23-dose-model/` to run on a
   GPU (Tesla T4, 16 GB). It is now a standalone engine with a documented callable interface, benchmarked
   below, and delivered as an artefact for the agent-based model in its own right.
2. Refitted the model on the **exact published CPU engine** with far more draws than last session
   (5,000 prior draws per scenario at a fixed tolerance, 948-1,044 equally weighted accepted draws each,
   plus an independent replicate of scenario A), and answered the four questions in the brief.
3. Found and fixed a **serious arithmetic defect in the previous fitting code** that very likely explains
   last session's "posterior looks like the prior, search not converged" conclusion. Evidence below.

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
Test designed to kill it: the comparison is out of sample on countries never fitted, with the country
family-system effect predicted from the region average, and uncertainty from bootstrapping the 6 held-out
countries. It kills the claim. Caveats: both scenarios fit badly in absolute terms (held-out errors 3.4 for
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

**Parameter strengths: covered but not pinned down.** The true recovery test was run: observations were
generated from a known parameter vector, the equal-weight fitter was run against them, and the intervals
checked. All five known values fall inside the 90% intervals (kin 2.2 inside 0.24 to 4.73; downward flow
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
the total and the effective sample size was 1.01 of 600 kept draws** in scenario A, and 4.79 in scenario B.
Cause: the particle density was accumulated in linear space; with a 31-dimensional parameter vector the
exponential underflows to exactly zero for distant particles, every collapsed particle receives the same
maximum weight, and one of them takes all the mass. Recomputing the same quantity in log space did **not**
rescue it (effective sample size 2.5 of 600), because the prior-over-proposal ratio is genuinely explosive
in 31 dimensions. The fix was to abandon importance weights: draw from the prior, keep every draw within a
fixed distance, give every kept draw equal weight (effective sample size = number of accepted draws by
construction). All numbers above come from that equal-weight run. **Implication: last session's
"posterior indistinguishable from the prior" was at least partly this arithmetic failure, so the earlier
posterior intervals should not be read as evidence about the model.**

## The GPU engine
The kernel reproduces its own reference exactly: for the same seed and parameter vector, woman-level states
(married, separated, parity, age at marriage, births by 30 and 35, age at first birth) agree with maximum
absolute difference 0 and zero mismatched women over 6 configurations, and the four fitted target series
differ by 0.0 (`results/port_test.json`). Throughput: on the T4, about **2.0 million simulated women per second** (1.9-2.2 million at 320 thousand
to 1.3 million women per launch); on the RTX 2080 Ti, **5.8 million women per second** at 10.1 million
women in one launch (1.75 s), which is 143 parameter draws per second and 1.1 GB of engine state. One
parameter draw of 24 runs costs 12.5 ms on the T4. Callable interface in `scripts/abm_dose.py`,
deterministic for a given seed (`results/bench_scale_2080ti.log`).

It is a **different engine** from the published one in its marriage market (a deterministic priority claim
instead of a serial random permutation), and that difference is measured, not assumed: with 200 seeds per
country it marries women -0.21 years differently on average (t = -5.4) at the two-round setting, +0.09 at
one round, unchanged at three or four, varying by country and period (Philippines -0.19 to -0.58, China
-0.04 to -0.22, Egypt -0.08 to -0.23), while total and adolescent fertility are indistinguishable
(`results/PORT_NOTES.md`, `results/market_bias_postfix_17-31.json`). It is therefore **not a rerun of the
published model and no bias correction is applied**: it is the second engine that tests whether the
A-versus-B verdict depends on the engine. The identical A/B protocol was then run on this engine as the kill test for the market channel:
it gives **A 25.5 against B 21.7, difference +3.8 with 95% interval -2.6 to +12.0, A better in 3 of 6
held-out countries** — indistinguishable from the exact engine's +3.3 (-3.8 to +11.1, 3 of 6). **The
A-versus-B verdict does not depend on the engine**, so the null in section (1) is not an artefact of the
GPU market's semantics. Both engines' fits are 3,000 and 5,000 prior draws respectively at the same
tolerance, and the comparison is a paired out-of-sample contest on the same six countries.

## What is weak
The fit is poor in absolute terms for every scenario. The tolerance is the prior-predictive 20th percentile
because stricter tolerances returned an empty posterior (zero of 750 prior draws reached the pilot
tolerance), so the posteriors are coarse ABC summaries, not posterior-precision claims. Six held-out
countries is a small sample for the comparison in (1). The delayed-versus-never-born split is a structural
property of the model, not an estimate. The GPU engine's market semantics are disclosed and not corrected.
The equal-weight tolerance is loose by construction, and the individuation posterior's advantage in-sample
does not translate out of sample.

## Files
`scripts/`: `kernel.cu` and `engine.py` (GPU engine), `dosecore.py` (counter RNG, bit-exact math, schooling
imputation), `ref_numpy.py` (independent reference), `test_port.py` (porting test), `test_market.py`
(200-seed engine-difference measurement), `reject_abc.py` (equal-weight ABC, the quoted fitter),
`fit_cpu.py` and `fit_gpu.py` (particle ABC, the broken-weight attempt and the GPU protocol),
`analyze_cpu.py` (posteriors, diagnostics, held-out, tempo/quantum, stability), `falsifiers.py` (recovery and
scenario falsifiers), `falsifier_perm.py` (permutation), `abm_dose.py` (callable interface), `bench_scale.py`.
`results/`: `rej_fitA.json`, `rej_fitB.json`, `rej_fitA_rep.json` (the quoted fits), `port_test.json`,
`PORT_NOTES.md`, `market_bias_postfix_17-31.json`, `bench_scale.json`, `analysis_holdout.json`,
`analysis_decomp.json`, `analysis_stability.json`, `stability_A.md`, `summary_A.md`, `falsifiers.json`,
`falsifier_perm.json`, and the superseded `cpu_fit*.json` / `fix_fit*.json` from the broken-weight attempts.
