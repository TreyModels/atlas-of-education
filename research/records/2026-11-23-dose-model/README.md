# Schooling dose and fertility: an individual-level simulation (23 Nov 2026)

## What this is
A simulation of individual women's lives from age 15 to 49, built to test the hypothesis that schooling works like a dose of
individuation: each level of schooling loosens ties to kin, turns the flow of money from "up to parents" toward "down to
children", lengthens the career-first phase and makes women pickier about a mate. Low-dose women stay embedded in kin who
share childcare, so many births are cheap; high-dose women carry childcare themselves and must find a similarly educated
partner, so births are delayed and some never happen.

**Status: a working, tested pipeline, but the fit to real data is poor. Treat every number below as provisional.**

## How it works
- **Populations.** For 14 countries and 14 five-year birth cohorts (1930 to 1999), women are split into urban/rural and five
  wealth groups. Their schooling (none, some primary, primary, lower secondary, upper secondary, some tertiary, tertiary)
  comes from Barro-Lee attainment by age group (World Bank mirror; men are recovered from the both-sex and female tables).
  National shares are spread across urban/rural and wealth cells with a latent-schooling model. Its uncertainty is drawn anew
  for every parameter set: measurement noise in the Barro-Lee shares, how much of schooling differences sits in urban/rural
  and wealth, and how far the panel's primary and lower-secondary completion rates pull the youngest cohorts.
  The youngest cohorts (born 1990+) are extrapolated, and recent tertiary completion is understated. This is a real weakness.
- **Dose.** The weights for each level are drawn from priors (some primary about 0.2 to 0.9, primary 1, lower secondary 3 to 5,
  upper secondary 6 to 8, tertiary 9 to 11).
- **Life course, yearly.** School, then a career phase whose length grows with individuation, then the marriage market.
  The market is two-sided: men have their own schooling, are removed from the pool when they marry, and both sides have
  preferences over the education gap (women dislike marrying down; men dislike a better-educated wife; selectivity rises with
  individuation). Families also arrange early marriages, more readily where kin ties are strong. Births depend on marriage,
  on how many children she wants (smaller when money flows downward), and on the cost of childcare, which kin support cuts.
  Separated women keep having children only in proportion to kin support.
- **Scenario A** (the hypothesis): kin support, the direction of money flows, career length and pickiness all depend on dose,
  and the same dose gives more independence in later cohorts as the economy and the cohort's average schooling rise.
  The strength of each of these is estimated.
- **Scenario B** (the rival): the same machinery, but every one of those channels is driven by income level instead, and
  schooling only takes up time and shapes who is available to marry.
- **Country trait.** Each country has one free "family-system strength" that moves baseline kin support, early arranged
  marriage and desired family size. For held-out countries it is the average of fitted countries in the same world region
  (Kenya, Brazil and Mexico get the all-country average).

## Fitting
Eight fit countries (Philippines, Thailand, China, Indonesia, Vietnam, India, Bangladesh, Egypt); six held out (Korea,
Malaysia, Kenya, Brazil, Turkey, Mexico). Targets: total fertility every five years 1980 to 2010, fertility at 15 to 19,
average age at first marriage, and share married by 18. Mean age at first birth could not be obtained, so the marriage age
stands in for tempo. Method: approximate Bayesian computation with a particle population (about 11,000 simulated parameter
sets per scenario at about 25 simulated life-course runs each), followed by an evolution-strategy polish of the best sets.
GDP per head is taken in logs by us from levels.

## Results (details in results/summary.md and results/analysis.json)
- **Fit.** Neither scenario fits well. Typical errors are about three standard deviations of the tolerances used. A fits
  better in-sample (best distance 9.6 against 12.8 for B).
- **Out of sample.** A has lower average held-out error than B (16.8 against 19.9) and a lower error on the held-out
  fertility paths (RMSE 1.2 against 1.7 births per woman). The gap is not statistically clear (bootstrap interval for the
  difference -9.4 to +3.1), A wins in 4 of 6 countries, and B wins Korea and Turkey. Kenya is badly missed by both.
  Caution: both scenarios fit poorly, so this is a comparison of two poor models.
- **Kin support and cohort deepening.** Real-data posteriors are close to the priors. Median kin-support loss per full dose is
  about 3.4 (90% range 0.0 to 5.0; a full dose keeps roughly 3% of kin support at the median); cohort deepening is about 0.3
  (0.0 to 2.0). The data neither confirm nor rule out either strength.
- **Tempo and quantum.** Between the 1940 and 1980 cohorts, almost all of the fall in births is quantum (never-born children):
  about 1.4 births per woman nationally, with delay beyond age 35 contributing close to zero (slightly negative). This is a
  built-in feature of the model, in which delayed births are mostly recovered or lost, and it is not a robust finding.
  Dose-group splits are noisy and are in the results file.
- **Which countries fit.** Best: China, Thailand, Indonesia, India. Worst: Philippines (fertility too low in the early
  years), Egypt, Bangladesh (adolescent fertility too low), Vietnam and Indonesia (too many early marriages).
- **Recovery check.** Data simulated from known values were refitted. The right scenario was preferred both ways (distance
  3.4 against 4.8 when A is true; 2.8 against 5.0 when B is true), so the scenarios are distinguishable in principle. Individual
  strengths were not recovered well (see results/summary.md): the search is not converging enough, and its reported
  intervals are too narrow. The recovery run is itself a warning that the strengths above are not pinned down.

## What is weak
The search over about 30 parameters has not converged, so the posterior is not a true posterior. The model cannot reach early
Philippine fertility and adolescent fertility together. Barro-Lee is coarse and extrapolated for recent cohorts. Country
effects are crude. Becker-style time costs are absent in both scenarios. Marriage markets are closed within a cohort. The
sample of held-out countries is small. Next steps: a proper emulator-based fit, fewer free parameters, age-specific
fertility targets, and education-specific fertility from household surveys.

## Files
scripts/ (fetch and build the data, the simulation, the fitting, the analysis), data/ (raw downloads, panel, known truths),
results/ (fits, analysis, recovery, figures, summary). Run order: fetch_data, fetch_total, build_panel, make_truth, fit_abc
(for A and B), es_refine, analyze, summarize, make_figures. The computing was done on a rented server.
