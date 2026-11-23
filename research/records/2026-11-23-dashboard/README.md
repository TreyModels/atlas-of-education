# Research dashboard — 23 November 2026

**Status: FINAL for this session** (the methods paper is still being drafted separately). Every number below is
traceable to the results file named in the job's own record. Plain words, no variable names.

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

| Job | What it tests | Branch | Status |
|---|---|---|---|
| 1 | GPU rewrite of the individual-level dose model, then a converged fit | research/dose-gpu-2026-11-23 | PORT DONE (exact vs rewritten reference); valid rejection-ABC posterior; A-vs-B pending |
| 2 | Lead-lag matrix rerun on the gap-filled panel | research/imputed-matrix-2026-11-23 | **DONE and verified** (commit 18404e3) |
| 3 | Grouping multiverse with 400 random groupings (was 74) | research/grouping-multiverse-400-2026-11-23 | **DONE and verified** (commit 1152cec; 38,420,908 regressions) |
| 4 | Added controls: child mortality, women's work | research/controls-2026-11-23 | **DONE and verified** (commit e18fc5a) |
| 5 | UN marriage and living-arrangements data, merged and tested | research/un-marriage-2026-11-23 | **DONE and verified** (b5c5335, 78ac50b, f3309e3) |
| 6 | Marriage age added to the matrix (20 measures, 380 links) | research/matrix-marriage-2026-11-23 | **DONE and verified** (commit 383acd8) |
| 8 | Why fertility tracks child survival and life expectancy: review + experiment plan | research/mechanisms-2026-11-23 | **DONE and verified** (commit ff2b18c) |
| — | Methodology paper on the multiverse method | research/methods-multiverse-paper-2026-11-23 | DRAFTING (held by Dr. Menefee) |

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

### The dose model on the GPU (job 1) — DONE for the fit; A-vs-B pending
- **The GPU rewrite succeeded**: a hand-written CUDA kernel through CuPy on a Tesla T4, about 23x per CPU core
  (487 life-course runs per second against 19.5), up to ~1,900/s at larger batches. For the same random numbers
  the GPU reproduces the rewritten CPU reference exactly: per-woman states identical, all four fitted targets
  differ by 0.0, arithmetic aggregates within 1e-15. It never bit-matches the *published* model, because the
  published marriage market is a serial random permutation; the GPU market is a deterministic priority market, so
  it is a slightly different model (a documented deviation, not a correctable offset).
- **Headline engine is the exact published model on CPU.** Scenario A, B and an independent A replicate were run
  with rejection ABC (equal weights) after particle-filter ABC was abandoned - see the methods finding below.
- **A valid posterior exists at last.** Scenario A accepted 1,044 of 5,000 prior draws (20.9%); the independent
  replicate accepted 1,003 (20.1%). Effective sample size equals the number accepted (all weights equal). The two
  independent runs agree closely, which is the convergence evidence the previous session lacked:
  kin-support loss per full dose of schooling median 2.80 (90% 0.34-4.74) in run 1 and 2.73 (0.37-4.78) in the
  replicate; downward money flow per full dose 2.62 (0.30-4.77) and 2.46 (0.26-4.78); cohort deepening 1.58
  (0.15-2.85) and 1.62 (0.22-2.87); career-first delay 5.32 years (1.10-7.71) and 5.14 (0.98-7.67); marriage-market
  pickiness 2.41 (0.25-4.70) and 2.54 (0.33-4.77). Every strength agrees across the two independent runs to a
  tenth of a standard deviation, and all intervals overlap.
- **But the data identify direction, not strength.** The priors span 0-5 and 0-3 on those strengths; the 90%
  intervals are only slightly narrower than the priors. These are coarse rejection-ABC intervals at a loose,
  pre-set tolerance (the prior-predictive 20th percentile), and must be labelled coarse.
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
  verdict as the exact engine. So the reversal is not an artefact of either engine.
- **Recovery: scenario choice recovers, parameter strengths do not.** Synthetic data generated from known A
  values are predicted better by the A posterior (15.4 against 17.6, difference -2.2, 95% -6.5 to +1.7); synthetic
  data from known B values are predicted clearly better by the B posterior (12.1 against 18.3, +6.2, +4.5 to +7.9).
  The right scenario wins both ways. But a true simulate-from-known-values-and-refit run puts all five known
  numbers inside the 90% intervals only because the intervals are nearly as wide as the priors - a test that could
  hardly have failed. It is reported as passed trivially, not passed; recovery of the strengths is not
  demonstrated.
- **GPU engine as a deliverable**: reproduces its own CPU reference exactly; 5.8 million simulated women per second
  and 10.08 million women in a single launch on the RTX 2080 Ti (2.0 million/s on the T4); deterministic for a
  seed; callable interface. This is the ABM engine for larger runs, with the market-semantics deviation documented.
- One check previously labelled "parameter recovery" compared the real-data intervals with the numbers used to
  generate synthetic data; it refits nothing. It has been relabelled in the results file so it cannot be mistaken
  for recovery evidence.

### Why fertility tracks child survival and life expectancy (new analysis) — DONE (review + plan, not experiments)
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
  detectable effect and identifying assumptions. The one separable with data already in hand is **level versus
  volatility** of child mortality (run first, nearly free); the highest identification value is **replacement vs
  insurance in birth spacing after a child death** (needs DHS/WFS micro data; minimum detectable effect about 3
  percentage points in the chance of a next birth); mortality shocks are most convincing in principle but
  underpowered for a 10-point mortality fall.

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

### Marriage age inside the full matrix (job 7) — DONE
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
- Child mortality and women's work added to the matrix, with a mediator table and a rule that a link is never tested
  with a control that sits on its own causal path. Not started; depends on job 2.

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

### Marriage age as an outcome of schooling (job 7) — DONE
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

## What would change our minds (falsifiers to watch)

- **Dose model**: the recovery test. Data simulated from a known kin effect of zero and a known large kin effect must
  be refitted and the search must recover which is which and prefer the right scenario. If it cannot, the dose model
  cannot be said to test the hypothesis. Also the permutation test: shuffling schooling across women within
  country-cohorts must destroy the fit gain.
- **Massification nulls**: the power simulation must keep showing the trend test can see a real effect of plausible
  size. "Dies under country trends" is only readable as "cannot be separated from development", never as "is zero".
- **Multiverse**: the strict 400-draw test cannot certify anything (resolution), so the honest claim is about
  stability across groupings, not statistical certification.
- **Marriage data**: the change-on-change test is what killed the positive timing result; any future "marriage
  timing matters" claim must survive it.

## Branches produced this session
- research/un-marriage-2026-11-23 (complete)
- research/dose-gpu-2026-11-23 (complete, commit cfb448e)
- research/imputed-matrix-2026-11-23 (complete, commit 18404e3)
- research/grouping-multiverse-400-2026-11-23 (complete, commit 1152cec)
- research/controls-2026-11-23 (complete, commit e18fc5a)
- research/matrix-marriage-2026-11-23 (complete, commit 383acd8)
- research/mechanisms-2026-11-23 (complete, commit ff2b18c)
- research/methods-multiverse-paper-2026-11-23 (drafting, held by Dr. Menefee)

## Still not known (honest list)
- **The individuation mechanism.** The dose model now has a valid posterior and does NOT beat development-only out
  of sample; its strengths are stable across runs but no narrower than the priors, and parameter recovery is
  passed only trivially. So the mechanism is neither supported nor excluded: the data identify its direction, not
  its size. The decisive test is micro data (birth spacing after a child death), not another country panel.
- **Why fertility tracks child survival and life expectancy.** The association is robust; the mechanisms are
  observationally equivalent at country level. The first experiment to run is level versus volatility of child
  mortality, which needs no new data.
- **Whether the schooling-fertility null is a measurement limit or a real absence.** No country-level test so far
  can tell these apart; the marriage-timing channel is not visible at all.
- **Whether electricity or wage jobs matter with country trends at a feasible sample size.** So far inseparable
  from development, with power to detect large effects; wage jobs is a clean null at every grouping.
- **The methods paper's central claim.** The resolution arithmetic was corrected: certification depends on how many
  links share the p-value ceiling (a lone link needs ~5,440 draws; a cluster of 30 needs ~182), and 400 draws did
  certify 35 links. That corrected statement, not the earlier "400 can certify nothing", is the paper's novelty.
