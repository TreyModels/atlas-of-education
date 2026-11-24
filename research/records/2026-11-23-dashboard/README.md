# Research dashboard — 23 November 2026

**Status: FINAL — first wave plus second wave, all verified.** All thirteen first-wave jobs are complete, verified and pushed to origin. The methods paper is pushed and verified (f9673a9); its public visibility remains Dr. Menefee's decision. A second wave of jobs (tasks 15–29) was run later the same evening to test the theory at the level it claims: those records are summarised in the "Second wave" and "Final tranche" sections at the end, each with a pre-registration as its first commit, and the full verified branch list (10 records) was recomputed from committed files by the run lead. Every number below is traceable to the results file named in the job's own record. Plain words, no variable names.


**Server note.** Two rented boxes were used; one is retained. All remaining work and data are on box2
(`ssh autodl2`): `/root/work/data`, `/root/work/dose_gpu`, `/root/work/impute`, `/root/work/controls`,
`/root/work/undata`, `/root/work/matrix_marriage`, and the migrated artefacts (imputed panel, raw multiverse
replicates, UN workbooks) under `/root/autodl-tmp/migrated/`. Box1 is retired; nothing depends on it.

The two questions this session is answering:
1. **Fertility collapse.** Is schooling a "dose" of individuation that delays births, and that deepens with each
   generation through weaker kin childcare, money flowing up to parents, and a longer search for an equally
   educated husband?
2. **Massification.** What actually drives schooling for everyone — electricity, wage jobs, farm mechanisation,
   or just general development?

---

## The jobs and where they stand

| Job (task id) | What it tests | Branch | Status |
|---|---|---|---|
| 1 (task-1) | GPU rewrite of the dose model, then a converged fit and the A-vs-B test | research/dose-gpu-2026-11-23 | **DONE and verified** (774085c): individuation does **not** beat development-only out of sample |
| 2 (task-2) | Lead-lag matrix on the gap-filled panel | research/imputed-matrix-2026-11-23 | **DONE and verified** (5e4602b) |
| 3 (task-3) | Grouping multiverse at 400 random groupings (was 74) | research/grouping-multiverse-400-2026-11-23 | **DONE and verified** (1152cec; 38,420,908 regressions) |
| 4 (task-5) | Added controls: child mortality, women's work | research/controls-2026-11-23 | **DONE and verified** (5ea58af) |
| 5 (task-4) | UN marriage and living-arrangements data, merged and tested | research/un-marriage-2026-11-23 | **DONE and verified** (b2b18d5) |
| 6 (task-7) | Marriage age inside the 20-measure matrix (380 links) | research/matrix-marriage-2026-11-23 | **DONE and verified** (559a4e9) |
| 7 (task-8) | Why fertility tracks child survival: literature review + experiment plan | research/mechanisms-2026-11-23 | **DONE and verified** (28479c1) |
| 8 (task-9) | E1: child-mortality level versus volatility | research/level-volatility-2026-11-23 | **DONE and verified** (935632e) |
| 9 (task-10) | Dose tolerance ladder: is the strength identifiable? | research/dose-tolerance-2026-11-23 | **DONE and verified** (baadfe6): identification limit, not a tolerance artefact |
| 10 (task-11) | GPU engine scale and robustness audit | research/cuda-scale-2026-11-23 | **DONE and verified** (e600763): 66.8M women per launch; batch-layout dependence documented |
| 11 (task-12) | Full transition: pre-antibiotic equilibrium to fertility collapse | research/transition-2026-11-23 | **DONE and verified** (b13fde8): mortality leads fertility by ~12 years; schooling follows |
| 12 (task-14) | Novelty literature review: is any of this actually new? | research/novelty-2026-11-23 | **DONE and verified** (390db8d): 4 new / 8 incremental / 11 known |
| 13 (task-13) | Full transition in the GPU ABM: holds fertility up without the mortality decline? | research/transition-gpu-2026-11-23 | **DONE and verified** (f9f2f18): collapse survives without mortality decline (in this model) |
| - (task-6) | Methodology paper on the multiverse method — "Which Countries Does the Coefficient Describe? A Grouping Multiverse for Cross-National Panel Claims" | research/methods-multiverse-paper-2026-11-23 | **DONE, pushed and verified** (f9673a9; paper.md 12.3k words / 468 lines; claims→files map; refs with per-entry Crossref status; 400-draw record merged in so every number is traceable from one branch; run-lead recomputed the resolution arithmetic and class counts; situating patch applied in 45b2ad5 — §2.1 cites the vibration-of-effects/cross-national multiverse neighbourhood, §2.8 names and answers the two fair attacks, nine references Crossref-verified). Publishable after Dr. Menefee's read. Public visibility decision pending Dr. Menefee |

Job numbers follow the project brief; the shared task board uses task ids (given in brackets).

---

## (1) Fertility

### What we knew coming in (previous session)
- Country-level births track **child survival and life expectancy**, not schooling. That held in about 80–95% of
  country groups.
- Once income is logged correctly, income beats schooling as a predictor of births; in model averaging schooling's
  inclusion probability was 0.45 against income's 0.97.
- An individual-level dose model slightly favoured the individuation story over "development only" on held-out
  countries, but the fit was poor (typical errors ~3 standard deviations of the targets) and the kin and cohort
  strengths were not pinned down.
- The "not luck" result weakened under a harder null: 6 of 20,000 shifted worlds reached it.

### The dose model on the GPU (job 1) — DONE
- **The GPU rewrite succeeded**: a hand-written CUDA kernel through CuPy on a Tesla T4, about 23x per CPU core
  (487 life-course runs per second against 19.5), up to ~1,900/s at larger batches. For the same random numbers
  the GPU reproduces the rewritten CPU reference exactly: per-woman states identical, all four fitted targets
  differ by 0.0, arithmetic aggregates within 1e-15. It never bit-matches the *published* model, because the
  published marriage market is a serial random permutation; the GPU market is a deterministic priority market, so
  it is a slightly different model (a documented deviation, not a correctable offset).
- **Headline engine is the exact published model on CPU, and the out-of-sample answer is negative.** Scenario A,
  B and an independent A replicate were run with rejection ABC (equal weights) after particle-filter ABC was
  abandoned - see the methods finding below.
- **A valid posterior exists at last.** Scenario A accepted 1,044 of 5,000 prior draws (20.9%); the independent
  replicate accepted 1,003 (20.1%). Effective sample size equals the number accepted (all weights equal). The two
  independent runs agree closely, which is the convergence evidence the previous session lacked:
  kin-support loss per full dose of schooling median 2.80 (90% 0.34-4.74) in run 1 and 2.73 (0.37-4.78) in the
  replicate; downward money flow per full dose 2.62 (0.30-4.77) and 2.46 (0.26-4.78); cohort deepening 1.58
  (0.15-2.85) and 1.62 (0.22-2.87); career-first delay 5.32 years (1.10-7.71) and 5.14 (0.98-7.67); marriage-market
  pickiness 2.41 (0.25-4.70) and 2.54 (0.33-4.77). Every strength agrees across the two independent runs to a
  tenth of a standard deviation, and all intervals overlap.
- **The data identify direction, not strength - and that is now tested, not assumed.** The priors span 0-5 and 0-3
  on those strengths; the 90% intervals are only slightly narrower than the priors. The tolerance ladder (job 9)
  re-ran the same fit at the 20th, 10th and 5th prior-predictive percentiles, with 1,044, 1,012 and 660 accepted
  draws respectively. Four of the five strengths stay at **0.80-0.91 of the prior width at every tolerance**, with
  no monotone improvement: kin-support loss 0.88 / 0.89 / 0.87, downward money flow 0.89 / 0.89 / 0.91, cohort
  deepening 0.90 / 0.85 / 0.80, pickiness 0.89 / 0.89 / 0.90. Only career delay narrows (0.82 / 0.64 / 0.76) and
  it partly widens again at the tightest tolerance. So the identification limit is real, not an artefact of a
  loose tolerance. Scenario B at the 5th percentile accepted only 32 of 4,000 draws (0.8%) and is reported as
  **not interpretable at that tolerance**, not quoted. The 10th-percentile run is the cleaner comparison.
- **Methods finding worth its own paragraph:** particle-filter ABC was producing a degenerate posterior - the
  largest importance weight 0.995 and an effective sample size of about 1 of 600, and it stayed at 2.5 of 600
  even after an attempt at log-space weighting. So last session's "posterior looks like the prior, search has not
  converged" was at least partly a broken estimator, not a fact about the data. The fix was to abandon importance
  weights and use plain rejection sampling.
- **The out-of-sample verdict goes against the individuation story.** With valid equal-weight posteriors on the
  exact published model, the held-out error is 24.43 for the individuation scenario (A) and 21.10 for
  development-only (B): a difference of +3.32 against A, 95% interval -3.76 to +11.14, with A better in only 3 of
  the 6 held-out countries. So A does **not** beat B out of sample; if anything the point estimate favours
  development-only, and the uncertainty is large. Last session's "A 16.8 vs B 19.9, A better in 4 of 6" does not
  replicate on the exact model, and given that last session's importance weights were broken, that earlier
  advantage should be treated as not established.
- Caveats to carry with it: both scenarios fit badly in absolute terms (Kenya alone has errors of 57 for A and 65
  for B), and the tolerance is coarse, so this is a comparison of two poorly fitting models.
- **The delayed-versus-never-born split is model-dependent, not a finding.** Scenario A attributes 2.09 births per
  woman (90% 1.33-3.00) of the fall to never-born children in the fitting countries, 2.55 (1.72-3.56) in the
  held-out countries, with a negative "tempo" component (-0.34 and -0.42). Development-only attributes less to
  never-born (1.69 and 0.69) and its tempo term changes sign between samples (-0.26 fitting, +0.11 held-out). So
  the split cannot be read as "most of the fall is never-born"; it says more about the model than about the world.
- **The permutation falsifier gives a modest supporting signal.** Randomly reshuffling schooling across women
  within country-cohorts makes the fit worse in 66.6% of simulated parameter particles (the average distance
  rises by 0.31 to 1.07), and in 7 of the 8 fitting countries. So the real schooling assignment carries some
  information the model uses; it is a modest signal, not proof of the mechanism.
- **The engine-dependence kill test passes the other way round too.** The GPU near-port is a different engine by
  construction (deterministic priority marriage market instead of a serial random permutation; measured at -0.21
  years of marriage age on average over 200 seeds, disclosed, not corrected). Running the identical A-versus-B
  protocol on it gives A 25.5 against B 21.7, difference +3.8 (95% -2.6 to +12.0), A better in 3 of 6 - the same
  verdict as the exact engine. **One scope limit:** in that comparison the GPU engine fitted the parameters but the
  held-out predictions were made by the published CPU model in both arms, so it shows that the **fitted answer does
  not depend on which engine did the fitting** - ruling out the worry that the GPU market semantics drove the
  result - **not** that prediction on the GPU engine itself was tested. The GPU engine's own predictions are
  exercised in job 13.
- **Recovery: scenario choice recovers, parameter strengths do not.** Synthetic data generated from known A
  values are predicted better by the A posterior (15.4 against 17.6, difference -2.2, 95% -6.5 to +1.7); synthetic
  data from known B values are predicted clearly better by the B posterior (12.1 against 18.3, +6.2, +4.5 to +7.9).
  The right scenario wins both ways. But a true simulate-from-known-values-and-refit run puts all five known
  numbers inside the 90% intervals only because the intervals are nearly as wide as the priors - a test that could
  hardly have failed. It is reported as passed trivially, not passed; recovery of the strengths is not
  demonstrated.
- **GPU engine as a deliverable**: reproduces its own CPU reference exactly; about 5.1-5.3 million simulated women
  per second at scale, and a measured ceiling of **66.8 million women in a single launch** on the 11 GB card
  (12.7 seconds, 4.54 billion woman-years); 100 million women in two launches takes 18.4 seconds of compute
  (51 seconds end-to-end); memory is a flat 164.6 bytes per woman. It is deterministic for a fixed batch size and
  seed, and CUDA-graph replay and allocation size do not change results.
- **One real engine limitation, disclosed:** results **depend on the launch batch size** - total fertility can move
  by up to 1.13 births and mean marriage age by 1.74 years - because the random-number streams are keyed on a
  woman's position within the launch and on the total women in it. The fix is operational: pin the batch size and
  report it. This contradicts an earlier docstring claim of full determinism; the interface note is being corrected and the
dose record must state which batch size the GPU A-vs-B comparison used.
- One check previously labelled "parameter recovery" compared the real-data intervals with the numbers used to
  generate synthetic data; it refits nothing. It has been relabelled in the results file so it cannot be mistaken
  for recovery evidence.

### Why fertility tracks child survival and life expectancy (job 7) — DONE (review + plan; the level-vs-volatility test is job 8)
- The two fertility links robust in every kind of country are higher child mortality -> higher fertility and
  higher life expectancy -> lower fertility. A literature review and experiment plan now explain why that is hard
  to model: at country level the rival mechanisms are **observationally equivalent** - replacement of dead
  children, insurance/hoarding against uncertainty, quantity-quality with human capital, life-history strategy,
  birth timing, and a common development cause all predict the same two signs.
- Two honest flags from the review. First, the two links are not independent evidence: child mortality is a
  component of life expectancy (the matrix shows child mortality -> shorter life expectancy). Second, the
  reverse-direction links are null in our matrix (fertility -> child mortality -0.83 +/- 1.84; fertility -> life
  expectancy -0.11 +/- 0.23), so the association is a one-way lead-lag pattern, not a feedback loop.
- Seven ranked, pre-registered experiments were designed, each with estimand, data gap, falsifier, minimum
  detectable effect and identifying assumptions. The one separable with data already in hand - **level versus
  volatility** of child mortality - has now been run (job 8): the level matters and the volatility does not, which
  favours replacement/quantity-quality stories at country level without excluding a common development cause. The
  highest remaining identification value is **replacement vs insurance in birth spacing after a child death**
  (needs DHS/WFS micro data; minimum detectable effect about 3 percentage points in the chance of a next birth);
  mortality shocks are most convincing in principle but underpowered for a 10-point mortality fall.

### The full transition, pre-antibiotic equilibrium to collapse (job 11) — DONE and verified (b13fde8)
- **The corners of the arc, quantified.** In 1800-1850 the typical country had **41.6 child deaths per 100 live births**
  (interquartile range 38.0-44.4, 184 countries) and life expectancy of **39.7 years**. By 1980-2024 it was
  **2.8 child deaths per 100** and **70.7 years**, with effective fertility of 2.55 surviving children per woman.
- **Mortality decline leads fertility decline.** Using real observation years only, the mortality turning point comes a
  median of **12 years before** the fertility turning point (interquartile range 3-19; 78% of countries positive;
  190 countries; 81% among late transitioners). Around each country's own mortality onset, fertility falls to 0.85 of
  its pre-onset level after 20 years, 0.66 after 30 and 0.59 after 40. The long-run reconstruction version implies a
  52-year lead and is documented as an artefact of the reconstruction, not used.
- **What it cannot say.** The antibiotic era is dated (penicillin mass production 1944-45, streptomycin 1947, DDT
  mid-1940s, WHO 1948, measles vaccine 1963, oral rehydration in the 1970s-80s) but it arrives entangled with
  sanitation, income, schooling and state capacity, so it is **not** treated as an identified causal break. This is a
  description of the sequence, not a causal estimate of antibiotics.
- **Where schooling sits: behind, not ahead.** Two years of schooling precedes the fertility decline by a median of
  15 years in 67% of countries, while six years of schooling *follows* it by 18 years in 81% of countries. Mass
  schooling is a follower of the fertility collapse, not its trigger - which is consistent with the country-level
  finding that schooling does not drive births once development is allowed for.
- Four figures are committed on the branch (mortality-fertility phase diagram with country trajectories, long-run
  time series for early and late transitioners, the distribution of mortality-to-fertility lags, and the annotated
  pre-antibiotic/collapse corners).

### The mortality counterfactual in the GPU ABM (job 13) — DONE and verified (f9f2f18)
- **Design.** Eight countries, cohorts 1930-1995 (reproductive years 1945-2045). Both arms use exactly the same
  history of schooling, income and urbanisation; the only difference is child survival. Arm 1 lets child survival
  follow history; arm 2 freezes it at the pre-antibiotic level (42 child deaths per 100 instead of 3). Scale:
  **10.08 million simulated women, 353 million woman-years, 48 runs, 3.03 seconds** on the 2080 Ti (3.3 million
  women/s; a 3.36-million-woman version gives identical results).
- **The mortality channel is calibrated to our own estimate, not assumed.** Desired births rise by 0.0067 per point
  of child mortality per 100 (the country-level estimate from job 8), so the whole 40-point mortality fall accounts
  for about 0.25 births - not the ad-hoc ~1.6x multiplier first proposed.
- **Result: the collapse survives without the mortality decline.** Historical arm: fertility falls 1.36 births per
  woman (means 4.96 to 3.60). Frozen-mortality arm: falls 1.31 (5.01 to 3.70). **Freezing the mortality decline
  removes only 3.2% of the fall** (country range -1.8% to +8.2%), and raises the *level* by only about 0.05-0.06
  births. (These are the committed means; earlier drafts of the worker's report quoted levels about 0.06 higher -
  the changes are identical and the dashboard uses the committed numbers.) Falsifiers: plus or minus
  50% on the calibrated coefficient moves the answer by 1-5%; a 4.5x power check reaches only 10%; two population
  sizes agree. So no plausible calibration of that channel flips the verdict.
- **The verdict is not scenario-specific.** Running the same frozen-mortality counterfactual on the development-only
  scenario removes 2.0% of *its* collapse (from 5.2 to 2.1 births), against 3.2% under individuation. So whichever
  scenario is fitted, freezing mortality does not stop the fall - the mortality channel is small in both.
- A figure with the counterfactual lines overlaid on observed fertility is committed on the branch.
- **Read it as a decomposition of this model, not a causal finding.** The published model was calibrated to reproduce
  the fertility decline through its own schooling/income/development channels; a small calibrated mortality term
  cannot overturn that structure. So "schooling-led" here means "in this model, the schooling and income channels
  carry the fall". It does **not** show that mortality decline was unimportant in the world. It also sits in real
  tension with the country-level evidence, where the child-survival link is the most robust fertility relationship in
  the project - either the model is mis-specified (attributing to schooling what is really survival), or the
  country-level link is not causal. That tension is unresolved and is the most important thing the counterfactual
  surfaced.
- **Honest negative: the pre-antibiotic arc is unreachable.** On cohorts 1890-1955 the model produces no transition
  at all (fertility 4.01, then 4.94, then 4.64 - a rise), and the highest simulated level is 5.20 births (5.42 in
  the forced-band run) against a historical ~5, so even the model's ceiling is too low. The model has no mechanism
  for the early high-fertility plateau. **The historical
  arc from 1800 is shown by job 11's data and figures; the simulation only covers 1930 onward.**
- Labels: model extension, not the published model; with the mortality channel off and the published cohort base the
  engine reproduces the published model exactly (state difference 0, target series 0.0), and that check is in the
  record. Pre-1950 schooling and the income rescale are documented assumptions; the engine's market-semantics
  deviation stays labelled.

### Country-level fertility links after gap-filling (job 2) — DONE
- Seven fertility-block cells change significance. **Four are precision-only, not new effects**: urbanisation
  to births (-0.014 to -0.017, standard error 0.007 to 0.006), the secondary gender-parity gap to births,
  births to wage jobs, and schooling to births all keep essentially the same estimate and become better powered
  with the larger sample. None of these should be reported as the gap-filling having found something.
- **One is coverage-driven and mechanically entangled**: births to child mortality moves from -0.56 (SE 1.84,
  not significant) to -3.70 (SE 1.53, significant), identical across all 20 imputations because the extra rows
  come from a long-run source shared by every imputation. Births and child deaths are definitionally entangled,
  so this is not a discovery.
- **One is unreliable**: births to primary completion loses significance because the 20 imputations genuinely
  disagree (between-imputation spread 0.56 against an estimate of -2.0), so it is labelled unreliable rather than
  newly null.
- **One is a genuine estimate movement**: births to the tertiary gender-parity gap.
- Reading for the fertility question: gap-filling does not create a schooling-to-fertility link, does not remove
  the child-survival dominance, and the links it does move are either mechanical or better-powered versions of
  what was already there.
- The gap-filled panel raises sample sizes 1.8–3×. Raw significance flips would mislead: 61 of 544 links change
  significance but zero flip sign, and the report must separate "more rows" from "the estimate moved".
- Dashboard check (independently confirmed): observed panel 127 links significant with country effects, 42 with
  country trends, 24 both; gap-filled panel 127 / 45 / 35.
- Flagged for the report: "more births → higher child mortality" moves from −0.83 (SE 1.84, not significant) to
  −3.20 (SE 1.58, significant) and is identical across all 20 imputations, so the shift comes from newly covered
  long-run rows, not from imputation noise — and the relation is mechanically contaminated.

### Marriage timing and co-residence: the UN data (job 5) — DONE
- **Data obtained from the UN's own workbooks**: UN World Marriage Data 2019 and the UN Households and Living
  Arrangements of Older Persons 2026. The reported 403 was a user-agent block, not an access block.
- Coverage, survey years only, never interpolated: women's mean age at marriage 2,073 observations / 210 countries /
  1960–2019; share never married at 45–49 2,060 / 211; the gap between women's and men's marriage age 1,845 / 209;
  co-residence of someone aged 60+ with adult children only 705 rows / 143 countries (402 rows / 70 countries used).
- **A killing test killed the interesting positive result**: later female marriage age appeared to predict a smaller
  future fall in births (+0.020 births per woman per year of age, SE 0.006), which passed permutation and jackknife.
  Put changes on both sides — change in births on change in marriage age — and it reverses to −0.027 (SE 0.010,
  1,360 rows, 196 countries). It is a levels-versus-change artefact, not a timing effect. Demoted.
- **Honest nulls and undetermined results**: the never-married share's link to later fertility change is
  **undetermined** — −0.0045 ± 0.0027 at conventional levels is not significant, it is not established as exactly
  zero, and its sign is not robust across specifications. A year-shuffle permutation had made it look significant
  (p < 0.005), but that test destroys serial correlation; a circular-shift permutation that keeps the series'
  autocorrelation gives p = 0.08. More schooling did not predict later marriage (−0.036 years per point of
  secondary enrolment, SE 0.022, permutation p = 0.22) or more never-married women (sign flips).
- **What the data describe, plainly** (from the one-page summary): women's mean age at marriage rose from about
  19 in the earliest 1960s surveys to about 26 in the 2010s; later marriage and lower fertility go together across
  countries (−0.65) but not decade to decade within them (+0.007 over 1,339 windows), so marriage age is a marker
  of where a country sits in its transition, not a short-run lever. Never marrying by 45–49 is a minority outcome:
  median country 7.2%, above 20% in about one country in six. The age gap at marriage is universal (women younger
  in every country, median 3.3 years); its narrowing co-moves with faster fertility decline (−0.10 ± 0.03, 190
  countries) but the sign changes under one defensible specification, so it is a lead, not a finding.
- **The school → fertility edge itself remains null**: −0.0015 births per point of secondary enrolment (SE 0.0016,
  4,535 rows, 191 countries with country trends), reproducing the earlier matrix exactly. Marriage timing cannot
  rescue an edge that is already zero, and using it as a control would violate the causal-path rule — so it was
  never used as one.
- Living arrangements add nothing measurable (thin data; permutation p = 0.23); the marriage-gap edge is
  provisional because its sign moves with the starting-level control.
- What this supports: **nothing causal about marriage age and fertility**. The fraction of births that never happen
  is not explained by marriage-timing data at country level.

### Marriage age inside the full matrix (job 6) — DONE
- The 17-measure matrix was extended to 20 measures by adding women's mean age at marriage, the never-married
  share at 45-49, and the female-minus-male marriage-age gap: 380 ordered links, each run with country effects
  and with country trends.
- **The old matrix is unchanged, proved not asserted**: all 272 old links reproduce bit-identically once income
  is logged (544 comparisons, maximum difference 0.0; 127 significant with country effects, 42 with trends, 24
  surviving both). The older handoff counts of 126/45/25 came from income entered in levels, a real bug now
  corrected and labelled.
- **No marriage-to-fertility link survives.** The best one, later female marriage age "predicting" a smaller
  future fall in births (+0.020, SE 0.006, BH q = 0.02), reverses to -0.027 (SE 0.010) when changes are put on
  both sides: the same levels-versus-change artefact found earlier, reported as an artefact, not a finding. The
  narrowing marriage-age gap (-0.035 +/- 0.016) passes the strict permutation but is not multiple-testing
  significant and its sign flips under one defensible specification, so it stays provisional. The never-married
  share is a null.
- After Benjamini-Hochberg across 380 links, only 16 links survive country trends, about the 19 expected by
  chance if nothing were real, so the trend-surviving set must be read link by link.

### Level versus volatility of child mortality (job 8, experiment E1) — DONE
- **The direct test of why births track child survival.** Child mortality was split into its slow level and its
  year-to-year volatility, and both were put into the same within-country lead-lag design (observed panel only,
  income logged, country and decade effects, clustered errors, with and without country trends).
- **The level matters; the volatility does not.** Level: +0.0067 births per woman per point of child mortality
  (SE 0.0015, 7,531 country-years, 193 countries) with country trends, +0.0072 (SE 0.0007) with country effects -
  replicating the matrix's raw link. Volatility: +0.0020 (SE 0.0020), not significant alone or jointly (the joint
  estimate is -0.0022 with a level estimate of +0.0070). The level and volatility measures correlate only 0.29, so
  the joint model can separate them.
- **Falsifiers:** circular-shift permutation gives p < 0.005 for the level and p = 0.29 for volatility; the
  cluster-preserving country placebo for volatility is p = 0.12 (inside its null). A minimum detectable effect of
  0.0046 for the level and 0.0056 for volatility means a volatility effect as large as the level effect would have
  been detected; roughly half that size would not.
- **Reading:** the number of children who die moves fertility, not the riskiness of child survival. At country
  level that favours replacement and quantity-quality stories over a pure insurance/uncertainty story - but it
  does **not** exclude a common development cause, and a country-level null on volatility cannot rule out
  household-level insurance.
- **Methodological lesson logged:** a naive value-scramble placebo for the volatility series looked significant
  but is invalid because it breaks the clustering of the series; the correct cluster-preserving placebo is the one
  reported. This belongs with the circular-shift lesson in the methods paper.

### Added controls (job 4) — DONE
- Adding child mortality and women's work as controls changes 217 cells, but **120 of those are pure sample
  composition** (the control is missing for some countries, so the sample changes) and only **94 are genuine
  control effects** (79 estimate moves, 15 precision changes). Child mortality mostly acts as a test (53 of 59);
  women's work mostly changes the sample (63 of 71).
- The main conclusions are unchanged or strengthened: the electricity-to-schooling and fertility-to-schooling
  links hold; income-to-secondary weakens under trends; three sign flips are collinearity artefacts (variance
  inflation factor 33 under trends) rather than real.
- Falsifiers: the mediator rule was applied programmatically to all 272 links (child mortality usable for 212,
  women's work for 198, both for 172; every schooling-to-fertility link excluded); a deliberate negative control
  that controls a known mediator collapses the result as predicted; and an exact power/minimum-detectable-change
  figure is given for every unchanged link, so a null can be read as "no change" only where the test could have
  seen one.

---

## (2) Massification

### What we knew coming in (previous session)
- Electricity and wage jobs line up with schooling **only** when countries are pooled. Once each country's own
  trend is controlled, both vanish.
- That is not "zero": a power simulation shows a true 20-point electricity effect is caught 91% of the time with
  trends (false positives 2–4%), so the reading is "cannot be separated from development at this sample size".
- The famous electricity estimate of +16.05 comes from a single specification. With country trends it is
  +0.05 ± 0.19 on the sample that estimate came from, and about +0.07 on the full matrix.
- Wage jobs: null in every grouping. Farm inputs: null on paid jobs and births once income is logged.
- The wage/price elasticity of 0.43 is a within-country number, so it does not test Boppart's cross-country figure;
  in a cross-section setup the estimate is 1.4–1.6, close to theirs.

### The gap-filled panel (job 2) — DONE
- The gap-filled panel raises sample sizes about 1.8-3x. Raw significance flips would mislead: 61 of 544 cells
  change significance over 55 links, and **zero flip sign**.
- Each change is labelled: **6 unreliable** (the 20 imputations disagree more than their standard errors allow,
  listed in the report), **13 coverage-driven** (all 20 imputations give the same answer because the extra rows
  come from a long-run source shared by every imputation), **18 precision-only** (same estimate, better powered),
  **24 genuine estimate movements**.
- The headline comparison: observed panel 127 significant with country effects / 42 with trends / 24 both;
  gap-filled 127 / 45 / 35. So gap-filling adds eleven trend-surviving links - but the labels above decide which
  of them mean anything.
- Falsifiers: a wrong-country permutation null gives 21.7% significant on the observed panel and 22.4-24.6% on
  the gap-filled one, so the gap-filling does not manufacture links; mechanical entanglements (births and child
  mortality, life expectancy and child mortality, the schooling ladder) are flagged; and the report warns
  loudly that naive mean-imputation would have given a badly over-significant matrix (158/80 against 127/45).

### The grouping multiverse at 400 draws (job 3) — DONE
- Design: 50 ways of splitting countries into groups (8 families), the whole within-country lead-lag matrix rerun
  inside every group, and 400 random repartitions with the same group sizes as the yardstick for chance.
- **The substantive answers do not move.** 46 of 272 links beat random groupings with trends (43 at 74 draws):
  of the old 43, 42 survive, 1 dies (farm employment to the gender gap in higher education), and 4 are new.
  20 of the old 21 still do worse than random, 32 of the old 36 still flip sign more than random, and the same
  **5 links are robust in every kind of grouping**. The run reproduced the old 74 draws bit-for-bit, so every
  change is a better-estimated yardstick, not code drift.
- **Massification: still nothing robust everywhere.** Wage jobs remain the cleanest null (no link to any
  schooling outcome beats random groupings in any kind of country). Electricity keeps its earlier status: zero
  once country trends are allowed, patchy in slices, and it flips sign more than any other driver (11 of its 32
  links). Farm change to higher education weakens from "beats random" to group-specific.
- **Fertility: two links travel everywhere** - child mortality and life expectancy leading to fewer births; they
  are indistinguishable from what random slices show, which is exactly what a uniform effect looks like. A
  further 3 beat random without a clear group, 13 hold only in particular kinds of country, and 14 are no better
  than random.
- **Resolution analysis - and a correction to our own earlier claim.** The floor logic is right for a LONE link:
  with 400 random draws the smallest attainable p-value is 1/401 = 0.0025, while a 5% correction across 272 links
  needs 0.00018, so a single link needs about 5,440 draws to be certified. But Benjamini-Hochberg is a step-up
  rule, not a Bonferroni rule: when many links pile up on the floor, the cluster clears the line. Here
  **35 links are certified going up and 19 going down** (30 pinned at the ceiling). The required draws scale with
  cluster size: a lone link needs ~5,440, a cluster of 5 needs ~1,088, a cluster of 30 needs ~182. So the earlier
  statement "400 draws can certify nothing" was wrong; the corrected statement - certification depends on how many
  links share the ceiling - is the methods paper's real contribution.
- **Falsifiers:** determinism is exact (independent re-runs of draws 7, 250, 400 and the real pass are
  bit-identical); the halves-split test shows the verdicts are stable link by link (p-value rank correlation
  0.994; 267-269 of 272 links agree between the full set and a half), so 400 draws is enough; normal and t fits
  of the yardstick agree on 42 of 46 links.

### Marriage age as an outcome of schooling (job 6) — DONE
- The strongest "schooling -> later marriage" link from the enlarged matrix, more tertiary schooling going with
  a later rise in women's marriage age (+0.071 years per point, SE 0.021, BH q = 0.02), **dies under the correct
  test**: a circular-shift permutation that preserves each country's series gives p = 0.50, and dropping the
  UN's model-based estimates flips its sign. It is not a finding.
- The only stable association involving marriage is an outcome, not a driver: economies that were more agrarian
  saw a slower rise in the share of women never married by 45-49 (-0.126 +/- 0.045, 827 rows / 92 countries,
  permutation p = 0.017). It still misses the multiple-testing threshold (q = 0.09), so it is a lead.
- Marriage age is on the causal path from schooling to fertility and was never used as a control in any link.

### Added controls (job 4) — DONE
See the paragraph above the massification section: the same control exercise, sorted there.

---

## Novelty check — what is actually new (job 12)

An external literature review tested every candidate claim against prior work. The blunt answer: **most of today's
findings are known, one is a genuine methods increment, and one potential new demonstration is still running.**

| Claim | Verdict | Closest prior work / what is actually new |
|---|---|---|
| "Electricity stops predicting schooling once country trends are allowed" | **KNOWN** | Textbook panel econometrics on trending regressors and common factors (Pesaran's common correlated effects; Eberhardt & Teal on growth empirics). The micro literature on electricity and education is large and mostly positive. Our increment is the **power-calibrated interval reading** ("cannot separate from development at this power", not "zero") and the single-specification +16.05 case study. |
| Multiverse resolution arithmetic (lone link ~5,440 draws; cluster of 30 ~182; 35 certified at 400) | **INCREMENTAL, border-NEW** | The two ingredients are textbook (the 1/(R+1) permutation floor, and Benjamini-Hochberg's step-up rule), but the **stated design rule** - how many random groupings a transportability multiverse needs depends on how many links sit on the p-value ceiling - appears unstated in this form. This is the session's strongest novelty candidate, publishable as a methods note. |
| Child-mortality level vs volatility | **INCREMENTAL** | The level effect is the 1976 "child survival hypothesis" (Population Studies); insurance/uncertainty is old (Cain 1981; Kalemli-Ozcan 2003). The **country-level level-versus-volatility discrimination** is a new application, not a new theory, and the caveats (common cause, household insurance) stand. |
| Individuation does not beat development-only out of sample | **INCREMENTAL (project result, not field result)** | That is a result about **one model with poor fit and unidentified strengths**, not a field verdict on Caldwell's wealth flows or Henrich's WEIRD thesis. The weight-collapse correction is a valuable internal audit of a known ABC pathology, not a new method. |
| Full transition in the GPU ABM with a no-mortality-decline counterfactual | **potentially NEW** | The transition question and individual-level microsimulation are decades old (SOCSIM; unified growth theory; FLAME GPU). The plausible novelty is the **combination**: an individual-level model calibrated to a real country panel, run across the pre-antibiotic-to-collapse arc at millions of women, with the mortality counterfactual. A new demonstration, not a new theory. |
| Engine capability (5 million women/s; 66.8 million per launch) | **NEW capability (engineering, not science)** | Genuinely useful; not a scientific claim. |

**Do not present as discoveries:** that electricity does not drive schooling; that child survival drives fertility;
that individuation is refuted; that the engine is a bit-exact rerun of the published model; or any causal
identification. Use "we are not aware of", never "first".

**The honest paper from this session** is: (i) the multiverse resolution methods note; (ii) a power-calibrated
fragility audit of cross-country education-development links, with +16.05 as the cautionary case; (iii) if it
validates, the GPU full-transition counterfactual as a demonstration; optionally (iv) the level-versus-volatility
result, framed as suggestive and limited.

## What would change our minds (falsifiers to watch)

- **Dose model (now run).** Scenario recovery passes both ways: data generated from individuation are predicted
  better by the individuation posterior (15.4 against 17.6) and data generated from development-only clearly better
  by the development-only posterior (12.1 against 18.3). Parameter recovery, however, passes only trivially - the
  intervals are nearly as wide as the priors - so the strengths are not identified, and the out-of-sample test
  says individuation does not beat development-only. The permutation test passes modestly: scrambling schooling
  across women worsens prediction (by 0.67, 7 of 8 countries). What would still change our minds is a
  tighter-tolerance fit that narrows those intervals (job 9 is testing exactly that).
- **Massification nulls**: the power simulation must keep showing the trend test can see a real effect of plausible
  size. "Dies under country trends" is only readable as "cannot be separated from development", never as "is zero".
- **Multiverse**: certification depends on how many links share the p-value ceiling. A lone link needs about 5,440
  draws, a cluster of 30 needs about 182 - and at 400 draws **35 links were certified going up** because a cluster
  of 30 sat on the floor. The honest claim is therefore both about stability across groupings and about that
  ceiling-cluster logic, not "nothing can be certified".
- **Marriage data**: the change-on-change test is what killed the positive timing result; any future "marriage
  timing matters" claim must survive it.

## Branches produced this session

### First wave (all on origin)
- research/dose-gpu-2026-11-23 (774085c)
- research/dose-tolerance-2026-11-23 (baadfe6)
- research/imputed-matrix-2026-11-23 (5e4602b)
- research/controls-2026-11-23 (5ea58af)
- research/grouping-multiverse-400-2026-11-23 (1152cec)
- research/un-marriage-2026-11-23 (b2b18d5)
- research/matrix-marriage-2026-11-23 (559a4e9)
- research/mechanisms-2026-11-23 (28479c1)
- research/level-volatility-2026-11-23 (935632e)
- research/transition-2026-11-23 (b13fde8)
- research/transition-gpu-2026-11-23 (f9f2f18)
- research/cuda-scale-2026-11-23 (e600763)
- research/novelty-2026-11-23 (390db8d)
- research/dashboard-2026-11-23 (this report)
- research/methods-multiverse-paper-2026-11-23 (f9673a9; pushed — paper.md 12.3k words, traceability merged from the 400-draw record; public visibility pending Dr. Menefee's decision)

### Second wave (all on origin; every record pre-registration-first unless marked as a run log)

- research/corr-rebuild-2026-11-23 (161b563)
- research/dhs-micro-2026-11-23 (31ded00)
- research/care-credential-2026-11-23 (e626cb8)
- research/policy-foreclosure-2026-11-23 (63691a2)
- research/scaling-2026-11-23 (fd691a6)
- research/subsistence-2026-11-23 (41f6429)
- research/subsistence-v2-2026-11-23 (ce66cfc)
- research/supply-demand-2026-11-23 (963e5e5)
- research/sfi-scan-2026-11-23 (fd4cfd2)
- research/scaling-laws-catalogue-2026-11-23 (cfe372f)
- research/corr-battery-2026-11-23 (9363079)
- research/early-warning-2026-11-23 (7e64f61)
- research/historical-sequence-2026-11-23 (ab658c7)
- research/scaling-data-hunt-2026-11-23 (9e15b6d)
- research/handoff-run-2026-11-23 (7efcb81; status/audit run log, contract-exempt)
- research/recompute-2026-11-23 (1a82f94; recompute log, contract-exempt)
- research/theta-gamma-2026-11-23 — no branch: task-24 closed as superseded by the θ/γ section of research/scaling-2026-11-23 (fd691a6), honestly absent rather than proxied

## Still not known (honest list)
- **The individuation mechanism.** The dose model now has a valid posterior and does NOT beat development-only out
  of sample; its strengths are stable across runs but no narrower than the priors, and parameter recovery is
  passed only trivially. So the mechanism is neither supported nor excluded: the data identify its direction, not
  its size. The decisive test is micro data (birth spacing after a child death), not another country panel.
- **Why fertility tracks child survival and life expectancy.** The association is robust; the full-transition
  record (job 11) shows mortality decline leading the fertility decline by about 12 years across 190 countries; the
  level-versus-volatility test (job 8) shows the level matters, not the riskiness. But the individual-level
  counterfactual (job 13) says the model's own schooling/income channels can generate the collapse without the
  mortality decline - which is either a mis-specification of the model or evidence that the country-level link is
  not causal. Resolving that tension needs micro data, not another panel. - which favours replacement/quantity-quality
  over pure insurance at country level. But a common development cause predicts the same pattern and is not
  excluded, and the decisive household test (birth spacing after a child death) needs micro data we do not have.
- **Whether the schooling-fertility null is a measurement limit or a real absence.** No country-level test so far
  can tell these apart; the marriage-timing channel is not visible at all.
- **Whether electricity or wage jobs matter with country trends at a feasible sample size.** So far inseparable
  from development, with power to detect large effects; wage jobs is a clean null at every grouping.
- **The methods paper's central claim.** The resolution arithmetic was corrected: certification depends on how many
  links share the p-value ceiling (a lone link needs ~5,440 draws; a cluster of 30 needs ~182), and 400 draws did
  certify 35 links. That corrected statement, not the earlier "400 can certify nothing", is the paper's novelty.

---

## Second wave — testing the Networked Domus theory directly (evening, 23 November)

**Why.** The first wave tested corollaries at the wrong level: decade changes with country fixed effects remove the
between-country and between-cohort variation the theory is about. This wave rebuilt the tests at the levels the
theory claims, and added the dynamics it names (care work, credential inflation, pronatalist policy, subsistence
transition, scaling). Pre-registration was the first commit on every branch.

### (1) Fertility

**The correlation is real and was mis-tested before (task-15, 161b563).** In levels, female attainment predicts
**−0.129 births per woman per year of schooling** (SE 0.029; 5,915 observations; 192 countries); total attainment
−0.228; secondary enrolment −0.0213 per point. Of 288 period specifications **99.7% are negative and 91.3%
negative-significant**, 0% positive-significant. In decade changes the sign flips (female **+0.111**): the earlier
null was a level-of-analysis artefact. Threshold: the slope is −0.33 below six years of schooling, −0.09 between
six and nine, and +0.11 above nine — most of the association is the move from minimal schooling to lower-secondary.
**Honest caveat:** the pre-registered future-schooling placebo fails (schooling ten years later predicts current
fertility 24/24, median −0.68), so this is a between-country **development gradient, not identified causality**.

**The gradient is global, not regional (ad-hoc levels multiverse, 2.89M regressions).** Across 100 random
re-partitions of countries, the schooling–fertility relation is significant in **90–95%** of groupings; the real
geographic/income groupings do not beat random (secondary 89.8% vs 94.5% ± 1.7%). Country-specific trends cut it to
19% (secondary). By contrast, income, tax capacity, female participation, child mortality and life expectancy show
**real grouping heterogeneity** (z up to +10.8) — the development context is heterogeneous; schooling is the
uniform part.

**DHS: the individual-level test could not be run (task-16, 31ded00).** Individual Recode files are login-gated
(2,005 records listed, no download; IPUMS 403; Zenodo 403). Published ecological cells (81,962 cells, 377 surveys,
87 countries) show a large gradient — completed fertility **−0.57 primary, −1.62 secondary, −2.54 higher**
children; **99% of 346 survey gradients negative**, median −1.90 — but two pre-registered predictions are
**contradicted**: the gradient attenuates in later cohorts (1940s −2.50 → 1970s −1.80) and is shallower where the
pipeline is denser. Present as ecological, not individual.

**Care work and credential inflation are null (task-17, e626cb8).** The care share of female employment is large
(18.3%, vs 5.9% for men, 148 countries) and rises with attainment (8.1/19.0/28.4% by tercile), but that association
is fully absorbed by income and urbanisation (attainment +0.009, t 0.17); placebos are decisive (male care +0.18,
t 2.1; manufacturing −0.19, t −3.5). The credential–occupation gap correlates −0.15 with fertility vs −0.62 for
attainment, and predicts worse in high-attainment countries. What survives is the plain attainment channel.

**No off-switch: strong form falsified, weak form supported (task-18, 63691a2).** Across 38 pronatalist
introductions, 8.6% of post-introduction years exceed 1.6 (95% upper 11.3%), but the persistence falsifier fires:
5/38 show 3+ consecutive years above 1.6 within ten years (Bulgaria ten straight years to 1.81). Average effect
+0.035 (SE 0.025); the highest fertility reached anywhere is **1.83**, nowhere near replacement; Thailand's 1997
reversal was followed by decline (1.84 → 1.21). Alternatives-foreclosure interaction is a clean null (−0.01, SE
0.02; strict sample opposite sign), with only the 2000/2010 decades usable.

### (2) Massification

**Scaling: no new law (task-19, 8243dd9).** Most education/income "scaling laws" are **between-country
regularities** (secondary enrolment 0.215 between vs 0.090 within, SE 0.124; education stock 1.176 vs 0.051); only
tertiary enrolment, lower-secondary completion, services share and urban share survive both layers. The
rarefaction-corrected Heaps exponent is **0.333 (SE 0.011)** — sublinear but below the 0.4–0.6 literature band
(10-category ISCO depth is the binding limit); there is curvature (−0.058, SE 0.002) but **no universalisation
threshold break** (p = 0.22). The "universal fertility collapse with female attainment" curve is **rejected**:
pooled R² 0.78 but country effects explain 72% of the residual and slopes differ (F = 46.4).

**SFI scan (task-20/23, fd4cfd2).** Catalogue of 13 sources and the three most promising leads: estimate the
θ/γ diversity formalism rather than invoke it; Ortman's archaeological settlement scaling as a deep-time test; and
early-warning/collapse signatures for "terminal enclosure". Running now as tasks 24 and 25.

**Subsistence transition: the earlier test was wrong; the correction is in (task-22, 41f6429).** The old test used
a world commodity-price index × farm-employment share — it measured exposure to a common world price, not
Boppart et al.'s object. Rebuilt from USDA/PWT/WDI: elasticities **1.24/1.11** OLS (**1.73/1.76** at the
development extremes) vs the paper's 1.90/1.75; input intensity rises **570×/637×**; inputs explain **55–69%** of
the agricultural labour-productivity gap (paper ~2/3). The corrected reduced form confirms input price → intensity
and intensity → agricultural employment share, but the **dynamic lead-lag is not identified** (reverse stronger),
and labour release → schooling/fertility is a **precise ten-year-panel null** (n = 503, MDE 0.016 births). The
three-parameter joint demography–agriculture–absorber model reproduces fertility (5.3→2.2 vs 6.0→2.1) and
schooling (0.5→8.2 vs 0.4→9.6) but **fails on agricultural employment (8.1% vs 19.4% in 2020) and population
growth (4.4 vs 2.9)**; the mechanisation-freeze counterfactual leaves agriculture at 17.9%, schooling at 5.6 years
and fertility at 2.52 (vs 8.1%, 8.2 years, 2.19). Model labelled a demonstration, not history; v2 queued to repair
the absorber and test the sequencing at cohort level and in the historical US.

### Second-wave branches

- research/corr-rebuild-2026-11-23 (c077672 pre-reg → 366214a results → 161b563 labels)
- research/dhs-micro-2026-11-23 (283e34c pre-reg → 31ded00)
- research/care-credential-2026-11-23 (7356e76 pre-reg → e626cb8)
- research/policy-foreclosure-2026-11-23 (7ad44d5 pre-reg → 63691a2)
- research/scaling-2026-11-23 (f8f782f pre-reg → 8243dd9)
- research/scaling-laws-catalogue-2026-11-23 (d78a623 → cfe372f cross-ref)
- research/sfi-scan-2026-11-23 (fd4cfd2)
- research/subsistence-2026-11-23 (d47e5ed pre-reg → 41f6429)
- research/corr-battery-2026-11-23 (task-21: 772650a, 6a1927f pre-reg; results 9363079, verified)

**What the second wave changes.** The thesis is now sharper and more falsifiable: schooling and fertility are
bound by a large, global, level-based gradient that was previously hidden by the change specification; but the
gradient is a development relationship, not a demonstrated causal lever, and the specific dynamics the theory
names — care work, credential inflation, pronatalist escape, agricultural labour release — either do not show up
in the available data or cannot be ordered in time by it. The decisive next tests are the cohort-level and
historical sequencing tests, not more country panels.

---

## Final tranche — the evening's remaining tests

### Battery: 57.3 million regressions (task-21)

The pre-registered battery executed **57,291,101 regressions in 3,018 seconds** (50.3 min) at 10 cores — 10,447,698 recorded result rows from a **13,800-partition** transportability design (each partition × 6 groups × 342 pairs × 2 relations = 56.1M) plus the 936,657-cell grid, bootstraps, thresholds and placebos — after resuming from a midpoint checkpoint (a dispatch-signature bug cost wall time, not work). The real grouping pass versus the 13,800 random country re-partitions:

- **Transportability:** the schooling–fertility pairs reproduce a negative-significant estimate in **71–99%** of random partitions in levels and **0–7%** in decade changes. Matrix-wide the shares are **22.7% [21.4–23.9]** vs **11.1% [10.3–12.0]** — so the global between-country property is specific to the schooling–fertility relation, not to all 342 links. That is an honest nuance, not a weakening of the headline.
- **The relation itself:** all eight schooling measures are negative-significant in levels (women's years **−0.129 ± 0.029**; total **−0.227 ± 0.042**; secondary **−0.0213 ± 0.0037**); every decade-change estimate flips positive (women's **+0.115 ± 0.046**; total's +0.189 ± 0.054) with **no** negative-significant change cell. Threshold: **−0.326 [−0.405, −0.248]** below 6 years, −0.092 [−0.175, −0.013] at 6–9, +0.112 [0.057, 0.171] above 9.
- **The placebo is not null:** future schooling predicts current fertility **52.9%** of the time versus **58.8%** at the correct time — about 90% as strong. The development-gradient caveat therefore survives the larger grid: the level relation stays descriptive, and a causal reading is rejected.

So the schooling–fertility relation in levels is a **global property** present in essentially any partition of the world, while the change relation is absent in essentially all of them — and the causal claim remains unsupported.

### θ/γ estimation attempt (task-24, fd691a6)

**Not estimable, and the test that was possible is negative.** θ and γ are model primitives, not measured variables; income and region are not relabelled as θ/γ. The observable the formalism implies — the rarefied diversity–size curve — gives a Heaps exponent of **0.349 (95% CI 0.331–0.368)**, with no income-group difference (0.010, CI −0.043 to 0.062), no regional difference (Kruskal p = 0.26), and negative curvature in every group. No two-regime pattern; but also no real test of the θ/γ mechanism. Both statements belong together.

### Early-warning / tipping-point test (task-25, 7e64f61)

**No tipping-point signature survives.** 80 countries with dated fertility transitions and usable pre-event windows: lag-1 autocorrelation **falls** before the event (−0.025, SE 0.008, t = −3.3 — the wrong sign for critical slowing down); variance rises slightly (+0.079, SE 0.034) but 42% of 16,000 surrogates match it; MDE 0.095. The one positive: diminishing returns is real (marginal effect of schooling on fertility **−0.0099 at p10, +0.0214 at p90**, turning point ~39 of 100 completion) — but a concave response and an arithmetic floor are observationally equivalent, so it is a boundary condition, not a ratchet.

### Subsistence v2 (task-26, ce66cfc)

The agricultural-share failure is repaired (**17.6% vs 19.4%** in 2020, v1 8.1%); the population failure flips (**1.58 vs 2.92**, still too slow); only 2 of 5 parameters are identified. Counterfactuals: freeze mechanisation → agriculture 39.9%, schooling 0.2 years, fertility 3.29; freeze the pipeline → schooling 3.0, fertility 2.94; freeze the mortality decline → population 0.39, fertility 3.96. In the model the **mortality decline is the first mover**, mechanisation empties agriculture, and the pipeline converts the release into schooling and lower fertility.

The sharper test fired against "the floor falls first": **schooling take-off precedes agricultural labour release in 61 of 64 countries** (release-first 5%, bootstrap 95% CI 0–11%), median gap 26 years; schooling before fertility in 69% (58–80%). The twentieth-century US ordering (farm decline 1910 → schooling 1955 → fertility 1957) is consistent, but 19th-century US/UK series were not obtainable and are documented as gaps.

### Supply-led or demand-led? (task-28, 963e5e5)

Raw timing looks demand-led (**73%** demand-first) but the demand dates come from broad development proxies (income, urbanisation); **labour-market demand** (wage premia, paid employment) precedes schooling in only **7%**. In the fair sample (33 countries) supply precedes schooling in **76%** and demand in **79%** — they turn together. Horse race on ten-year changes: supply block **+0.456 (SE 0.174)**, demand **+0.006 (0.203)**; enrolment +0.307 (0.146), education spending +0.125 (0.058); every demand measure null (n = 78, 51 countries). Verdict: **supply-led is the better description**; not a causal claim (policy, state capacity and income are jointly determined).

### Historical sequencing (task-29, ab658c7)

Split verdict, and the split is the finding. **Prussia** supply-led: the 1763/1812 school regulations precede industrialisation and the farm exodus by **80–120 years**, half the school-age population enrolled by 1800. **France** statute-led but attainment demand-following: Guizot 1833 creates the schools, attainment takes off with Ferry 1881–82, arriving with the exodus. **Britain** is the counterexample that matters: the industrial revolution and the farm exodus precede mass schooling by **40–90 years** (1870 Act; near-universal attendance only by 1900). **US North** supply-led in the local-public-goods sense, community-demand-driven. Implication: the 61/64 panel result is a **late-industrialiser regularity, not a universal law** — evidence about who built the pipeline and when. Literature dates in the record are marked **unverified**; our own long-run series cannot adjudicate (schooling data start 1870).

### Data hunt for the canonical scaling laws (task-27, 9e15b6d)

Two of five unlocked, no proxies used. **Zipf/rank-size**: median exponent **0.859** (bootstrap 95% CI 0.746–0.978), Wilcoxon against 1 p = 0.23 — consistent with Zipf, weakly (crowdsourced places, large-country selection). **Gravity**: PPML with origin and destination fixed effects gives distance **−0.970 (SE 0.076)**, OLS FE −1.306 (0.053), n = 8,020 pairs; size elasticities 0.46–0.64, below the conventional ~1. **Still blocked with exact errors: Bettencourt's superlinear urban exponent (BEA zips unavailable, WUP 404) and the credential:occupation ratio (BLS 403, Credential Engine Cloudflare 403).**

### Branches added in this tranche

- research/corr-battery-2026-11-23 (task-21: 772650a, 6a1927f pre-reg; results pushed after)
- research/theta-gamma-2026-11-23 (fd691a6)
- research/early-warning-2026-11-23 (e12249b pre-reg → 7e64f61)
- research/subsistence-v2-2026-11-23 (62730fc pre-reg → ce66cfc)
- research/supply-demand-2026-11-23 (f7b38f3 pre-reg → 963e5e5)
- research/historical-sequence-2026-11-23 (74e0fe2 → ab658c7)
- research/scaling-data-hunt-2026-11-23 (5e0b11a pre-reg → 9e15b6d)

**What the final tranche changes.** The theory's "pipeline first" claim survives as a **state-led-moderniser regularity** (Prussia, France, US North) and fails where demand led (Britain); its "floor falls first" version is refuted in the late-industrialiser panel. The schooling–fertility relation is a **global level gradient**, not a change mechanism. The tipping-point version of "terminal enclosure" fails; the θ/γ mechanism is untested (not supported, not refuted); the canonical scaling laws are weakly consistent (Zipf, gravity) or out of reach (Bettencourt, credential ratio). The two decisive open tests remain cohort-level sequencing and the historical lead/lag with proper 19th-century series.

---

## Papers produced after the dashboard (25 November 2026)

Seven manuscripts were mined from the verified branches, each with a claim-by-claim prior-art file (DOI + Crossref status, new-vs-replicated), a claims-to-source map, and a pre-registration where new analysis was needed. The literature review on every claim was independently audited by a separate reviewer, and a Synthetic Council of Experts adjudicated novelty across the whole programme.

| Paper | Branch @ head | Words | Status |
|---|---|---|---|
| Methods — "Which Countries Does the Coefficient Describe?" | research/methods-multiverse-paper-2026-11-23 @ 1fef07e | 12.6k | Ready to submit; dependence + BY revision with the FDR family defined (four separate BH procedures over the 272-link family — up 35, down 19, flip 15, het 53; **BY certifies 0 in every procedure at 400 draws**, rank ≥84 needed vs 30/19/15/53 at floor; lone-link budget ~33,650 BY; the 68-link hypothetical giving BY=35 is recorded as not the committed family); claim conditional, no wording strengthens |
| Paper F — fertility omnibus (levels-vs-changes centrepiece) | research/paper-fertility-2026-11-25 @ 6f4d6fb | 18.0k | Signed off (auditor); §3.5 pre-reg pointer added |
| Paper M — massification omnibus (sequencing centrepiece) | research/paper-massification-2026-11-25 @ 76d929a | 17.4k | Signed off; two declared opens |
| N1 — schools before factories (sequencing, standalone) | research/paper-sequencing-novel-2026-11-25 @ 7f73ff1 | 6.0k | Verified |
| N2 — the level-of-analysis trap (standalone) | research/paper-levels-novel-2026-11-25 @ 4ebe07b | 6.0k | Verified |
| N3 — agricultural floor / subsistence transition (ag-dev) | research/paper-agdev-2026-11-25 @ 12df7c1 | 7.4k | Verified |
| N4 — shape of the demographic transition | research/paper-shape-2026-11-25 @ 3b73bc1 | 7.7k | Signed off |

**Synthetic Council verdict (research/council-novelty-2026-11-25 @ 810506b; 42 claims inventoried, 9 killed):** the programme has **no new correlation**. It has **one conditional method contribution** — the multiverse draw-count arithmetic, which counts as a rule only once the dependence / effective-number-of-tests correction is formalised (methodologist score 4/5, down from 5; panel mean 2.2; closest prior Simonsohn et al. specification-curve inference, Patel et al. vibration of effects, Klau et al. sampling uncertainty) — two new assemblies (schools-before-factories sequencing, 3.8/5; the levels-vs-changes audit, 3.2/5), and one model-based demonstration (the GPU transition counterfactual, 3.2/5, publishable only around the negative result and the identification limit). The GPU determinism audit (batch-layout dependence; TFR up to 1.13 births, marriage age 1.74 years; fix = pin batch size) is inventoried as a negative methodological result for the engine note, not a paper-carrying novelty. Killed: electricity→schooling as a driver; "child survival drives fertility"; "individuation refuted"; credential inflation; threshold hinges as a discovery; care/tipping nulls as findings; the scaling/Heaps audit; the marriage-age data; and the retracted 69% ordering figure.

**Corrections made during the wave (all documented):** the 68.75%-vs-37.5% schooling-before-fertility figure (a tie-counting artefact; strict ordering is 37.5%, CI 26.6–50.0%) in Paper M and its source record; four wrong world-polity DOIs and book-as-article DOIs in Paper M; wrong-title references in Paper F; the release-vs-fertility ordering (6.25% release-first) verified separate from schooling-vs-fertility; and a commit-message overclaim in Paper F, corrected by rebuilding and grepping the assembled draft.

**Open for the next session:** DHS Individual Recode acquisition (the biggest available upgrade to Paper F); the GPU negative-result paper (the only paper-carrying candidate without a draft); Paper M's alternative-threshold recoding and date-by-source table (blocked by the downed box); Part C DOI re-verification; and the auditor's request to stress-test the multiverse draw-count rule before the methods paper goes out.

---

## Codex wave addendum (24 November 2026) — closed and verified

**This addendum is the current status.** The sections above describe the 23 November waves and are left unchanged (no rewrite). Where an earlier sentence is superseded by the closed Codex wave, the supersession is listed below; read those sentences through this list. Full provenance, the recomputation script and every UNVERIFIED mark are in the synthesis record:
`research/records/2026-11-24-codex-wave-synthesis/SYNTHESIS.md` on `research/codex-wave-synthesis-2026-11-24`.

### The nine verified heads

| Item | Branch | Head |
|---|---|---|
| Q1 mechanisms (synthetic known-truth pilot + GPU gate) | `research/q1-mechanisms-2026-11-25` | `9b0cabe` |
| Q2 country pathways (pair benchmark, audit, cases; erratum on `f71b789`) | `research/q2-pathways-2026-11-25` | `9a4f586` |
| Q3 multiverse calibration + full BH/BY | `research/q3-multiverse-calibration-2026-11-25` | `db7814d` |
| E1 multiverse at R = 1,200 (erratum on `7e6f7b5`) | `research/e1-multiverse-1200-2026-11-25` | `6a452a4` |
| E6/E8 sequencing repairs (errata on `2d19da7`) | `research/e6e8-sequencing-2026-11-25` | `bd782be` |
| E11 fertility audit (EFR vs TFR) | `research/e11-fertility-audit-2026-11-25` | `e926575` |
| Source verification (fee dates, demand series, prior art; metadata erratum on `9a0fd69`) | `research/codex-source-verification-2026-11-25` | `ea6bc61` |
| Methods paper | `research/methods-multiverse-paper-2026-11-23` | `d7e8f9f` |
| Paper F (rounding correction applied; erratum commits `4f8a61c` + `23928e0`; data unchanged) | `research/paper-fertility-2026-11-25` | `23928e0` |

Verification ledger: `research/records/2026-11-24-handoff/codex_wave_ledger.md` @ `51f9f02`. The dashboard's "Papers produced" table is stale on two heads: the methods paper is now `d7e8f9f` (was `1fef07e`) and Paper F is `23928e0` (was `6f4d6fb` in this table; wave head `ec899cc`, then rounding erratum `4f8a61c`, applied at `23928e0`). Paper M and N1 revisions remain open on their branches.

**Record heads advanced after the consolidated errata pass (25 Nov 2026):** Q2 `f71b789 → 9a4f586`; E1 `7e6f7b5 → 6a452a4`; E6/E8 `59d31d7 → bd782be`; source verification `9a0fd69 → ea6bc61`; Paper F `ec899cc → 4f8a61c → 23928e0` (draft correction applied; erratum commits `4f8a61c` + `23928e0`; data unchanged) — each an additive erratum commit. The E6/E8 erratum corrects one E6 prose range to strict schooling-first **21.5–46.3%** of identifiable countries (**58.3–71.4%** of strict orderings) and notes the fee-date provenance (`bfb8c6f` is an ancestor of the verified head `9a0fd69`; `fee_dates.csv` sha256-identical at both); the E6 demand-first shares below are unaffected. Other erratum corrections (E1 136-parity, E6 control/mean-post ranges, N3 weak-tie range, SV metadata, Paper F rounding applied at `23928e0`) are recorded in the synthesis record §3.

### What the wave established (numbers recomputed from committed files)

- **The macro wall:** only **5 of 272** within-country links are robust in every grouping; the other 267 fall under the remaining verdicts (group-specific, beats-random-without-a-clear-group, or no better than random) under this estimator. This is a transportability description, not a causal claim.
- **Q2 pair benchmark (yardstick corrected at `9a4f586`):** matched-pair medians are **0.620** (schooling) and **0.2375** (TFR), against random-pair medians 0.825 / 0.7728; **96.1% / 100.0%** of random draws are at least as divergent. Matching on 1980 similarity made pairs *less* divergent than random pairing, so the direction of Q2's honest null survives, but the earlier all-pairs 0.82 / 0.77 comparison and its 52.4% / 50.3% shares must not be quoted.
- **The selection criteria fail their own control (synthetic):** on the pre-registered zero-signal control, raw held-out MSE picks the flexible kernel in **97.5%** of W1 and W2 replicates and BIC picks the parsimonious one in **100%** of every world. A "model winner" is a complexity artefact. Simulation, not history.
- **"Robust everywhere" is not a homogeneity certificate:** in known-truth calibration it labels a minority-effect world robust **87.0%** of the time (348/400 replicates) while localising the planted group only **42.0%**. The null false-positive rate is 4.25% and a strong uniform effect is found 97.5% of the time.
- **"BY certifies zero" is a draw-budget statement:** dependence-robust BY certifies **0/0/0/0** at R = 400 and stays 0 at R = 800; at R = 1,200 it certifies **32 heterogeneity links** only, while up/down/sign-flip stay 0. Nominal BH is **35/19/15/53** at 400 and **41/23/20/53** at 1,200.
- **No identified causal schooling→fertility effect, no mechanism winner, and no claim that demand is ruled out.** The three candidate mechanisms remain observationally equivalent at the aggregate level; the E11 change ladder returns "does not discriminate".
- **Effective fertility is not TFR:** surviving children vs births differ by median **0.3042** (max **4.2677**) and flip the schooling lead/lag (**0.541** vs **1.555**). The two constructs are not interchangeable and neither corrects the other.
- **The 68.75%/69% figure was a tie-counting artefact:** strict schooling-before-fertility is **37.5%** (24/64; bootstrap 95% CI **26.6–50.0%**), with **31.25% simultaneous** and **31.25% fertility-first**; the old figure counted the ties as schooling-first.
- **The 7% labour-demand figure is retracted** (1991+ data start). E6's replacement on pre-1990 series: demand-first **10.0%** (GGDC non-ag employment), **15.4%** (urbanisation), **24.1%** (industry VA), **18.8%** (agriculture VA), bounds **6.7–53.0%**, ties/censoring **21.1–43.3%** → **"schooling and structural change move together"**, with schooling typically but not universally first. Strict schooling-first is the larger strict ordering — **21.5–46.3%** of identifiable countries (**58.3–71.4%** of strict orderings) — but not a majority of identifiable countries; the branch's earlier strict-range prose did not reproduce (erratum @ `bd782be`, Issue A at `59d31d7`; data unchanged).
- **Source verification:** 8 of 12 fee-abolition dates verified (4 unresolved: CMR, ZMB, RWA, BDI); **no pre-1990 wage-employment series exists** in the standard public sources checked (WDI/ILO modelled wage series begin 1991); prior art verified with DOI status.
- **E8 event study (design-conditional):** fee abolition shows a large positive primary-GER post effect with flat −2/−3/−4 pre-trends (on-impact +12.44 [−2.36, 27.24]; +6 25.92 [8.64, 43.20]); placebo −0.39; leave-one-out 18.17–26.16. **"Consistent with"** a fee-abolition effect; no causal claim. The secondary-GER proxy shows no clear effect.

### Superseded text in this dashboard (do not quote the earlier sentences without this list)

1. **"schooling before fertility in 69% (58–80%)"** (Subsistence v2, line 614) — retracted; use 37.5% strict (24/64, CI 26.6–50.0). The corrections note in the Papers section records the 68.75-vs-37.5 fix, but the finding sentence was not rewritten.
2. **"labour-market demand … precedes schooling in only 7%"** (Supply-led or demand-led?, line 618) — retracted as a 1991+ artefact; use the E6 numbers above. Do not use it as evidence against demand.
3. **"supply-led is the better description"** (line 618) — softened; the defensible statement is "schooling and structural change move together".
4. **"BY certifies 0 in every procedure at 400 draws"** (Papers table, line 648) — true at 400 and 800 draws, not universal: at 1,200 BY certifies 32 heterogeneity links.
5. **"a causal reading is rejected" / "development gradient, not identified causality"** (lines 513, 598; and Codex F11) — too strong; the level association is consistent with a common development gradient, anticipation/quantity-quality, and a long-lag schooling effect, and the design cannot reject a schooling effect.
6. **"robust everywhere" as an effect-homogeneity claim** (lines 136, 356, 358, 362) — it is a descriptive significance-share rule; the minority-world calibration above is the reason.
7. **The 61/64 "schooling precedes agricultural labour release" result** (line 614) is a *separate ordering* from the retracted schooling-vs-fertility 69%; the Codex wave does not re-examine it, so it retains its existing descriptive late-industrialiser panel status (the 19th-century US/UK gaps remain), and the two orderings must not be merged.
8. **Header status (line 3)** describes the 23 November dashboard; current status is this addendum.

### Recompute status

The addendum's headline numbers were recomputed from committed source files before being quoted (synthesis record §6: R1–R8 and R10 recomputed, R9 UNVERIFIED). This includes the 5/272 wall, the 97.5%/100% zero-signal control, the 87.0%/42.0% minority calibration, the BH/BY counts at R = 400/800/1,200, the EFR/TFR lead-lag and |diff| figures, the E6 demand-first shares, bounds and strict schooling-first range (21.5–46.3% of identifiable; 58.3–71.4% of strict orderings; erratum @ `bd782be`, data unchanged), the Q2 105/52/1/52, the 37.5% strict ordering, and the corrected Q2 yardstick (matched-pair medians 0.620 / 0.2375; shares 96.1% / 100.0% — **RECOMPUTED-AT-ERRATUM** at `9a4f586`). Numbers that were not recomputed — the E8 event ATTs, the Q2 matching-sensitivity shares, the Q3 design grid, and the methods-paper 76/161 counts — are marked **UNVERIFIED (committed field only)** in the synthesis record §7; do not quote them as established.

### Forward programme

The aggregate regression route is exhausted at this resolution. Next: **micro-simulation** with explicit simulation-vs-history labels (the GPU suite, Apple Silicon port first); **micro tie-breakers** that separate observationally equivalent mechanisms; and **DHS Individual Recode microdata** (individual schooling → children-ever-born, cohort comparisons, EFR/TFR construct split). Keep the EFR-vs-TFR labels and the draw-budget/dependence caveats attached to every "robust" or "BY" statement.

> **Status: needs redesign per the 24 Nov 2026 suite audit — see "Suite audit (24 Nov 2026)" below.**

### Suite audit (24 Nov 2026)

**The forward programme above needs redesign per audit: the shipped suite cannot test its own pre-registered hypotheses.** The audited payload (`research/records/2026-11-24-gpu-suite/` @ `51f9f02`) does not implement H1 or H4. `exp2` is a logistic classifier on pre/post means — there is no macro fixed-effects regression, no country dimension and no cross-DGP overlap statistic, so H1's ">75% macro-slope overlap" is undefined. `strength` appears only inside a docstring, so H4's zero-signal control cannot execute; the four "micro signatures" are transforms of the same state mix, so exp2's classifier recovery is **construction-implied and is not evidence**. `exp4` raises `IndexError` on its first World Bank API call, and WDI `SL.TLF.0714.ZS` is "Children in employment", **not** child labour, so the series cannot carry a child-labour claim. Any exp2/exp3 output, including the PORT-PRODUCTION run, inherits these defects.

The **ten claims in AUDIT §9 must not be published** in their current form: the macro wall demonstrated; binary bans backfire; protective capacity reduces child labour while fees-only does not; a micro tie-breaker passes the Q1 zero-signal control; rejection-ABC calibrates and identifies; fee abolition reduces child employment; learning-per-grade slope tested; faithful DGP mapping to Basu–Van / Baland–Robinson / Nordtveit / Bray / Jayachandran / Dang–Rogers / Pritchett; hidden work measured; the mixed DGP as a mixed-mechanism world. The honest labels are "simulation", "reduced form" and "consistent with" — nothing stronger.

The **Apple Silicon work is portability only**: the port reproduces the CuPy subset and the `sim_step` kernel bit-identically (NumPy vs MLX) and its full run is labelled **PORT-PRODUCTION, not research results** (`research/apple-silicon-gpu-2026-11-24`, port complete at `fd933d9`; branch head `be42c4d`). It does not repair the inferential objects.

Therefore the **"macro wall" and the "micro tie-breaker" remain UNTESTED by simulation.** In progress is a **strength-separable, macro-moment-matched redesign with a survey measurement layer**, pre-registered as design only (no run) at `research/records/2026-11-24-suite-tiebreakers/PRE_REGISTRATION.md` @ `e526c94` on `research/suite-tiebreakers-2026-11-24`: worlds `θ_w(s) = θ_0 + s·Δ_w` that are identical at `s = 0`; per-world nuisance search to a common macro vector `M*`; measured-variable tie-breakers with sampling, non-response, heaping, reference-period and under-reporting layers; algebraic-equivalence and label-permutation placebos; out-of-seed, out-of-parameter-region and mixture-world validation. Audit source: `research/records/2026-11-24-suite-lit-review/AUDIT.md` @ `4649cae` on `research/suite-lit-review-2026-11-24`. Until the redesign runs and passes its pre-registered controls, no suite output may be cited as evidence for the wall or for a tie-breaker.
