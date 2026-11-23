# Pre-registration — DHS women's schooling and children ever born

Committed **before** any data download, script or result. Date: 23 Nov 2026. Task: `task-16`.
Branch `research/dhs-micro-2026-11-23`; record `research/records/2026-11-23-dhs-micro/`; box2 `/root/work/dhs`.

## Data, in order of preference (provenance will be recorded)
1. DHS individual recode (women's file) variables: education level (v106), years of schooling (v133), children
   ever born (v201), age (v012), survey weight, urban/rural (v025), wealth quintile (v190), region (v024).
2. If microdata cannot be downloaded in the time available (DHS microdata normally requires a registered
   account), the DHS Program public API (`api.dhsprogram.com/rest/dhs/...`) indicator extracts. Only cells
   that the API actually publishes will be used; no series will be computed from a proxy or fabricated.
3. If the API blocks or carries no usable education-by-fertility breakdown, the record will say exactly what
   was tried and what a manual download needs (account, file names, variables) — with no results claimed.

## Design (fixed now)
- Universe: women age 15–49 (completed-fertility analyses also 35–49 and 30–49). 5-year age groups; cohorts
  defined by birth year (survey year − age), 5-year bins.
- Outcome: children ever born per woman (CEB). Where the API publishes only mean CEB by education and survey,
  the unit is the published cell and cell sample sizes are carried as weights; where microdata are available,
  the unit is the woman.
- Key regressor: education level (none / primary / secondary / higher), with no education as reference;
  report the linear "years of schooling" gradient too if available.
- Fixed effects: country x survey, and in the cohort models country x 5-year cohort. Age-group dummies control
  for the life-cycle. Standard errors clustered on country (and, where microdata allow, on survey primary
  sampling unit).
- Comparison groups: earlier vs later cohorts (split at the median birth year), high- vs low-pipeline
  countries (female secondary attainment measured from the same survey; median split), urban vs rural.
- Wealth: CEB on education **plus** wealth quintile dummies; the question is whether education survives.
- Quantum vs tempo: if parity-specific or age-specific fertility is available, compare the education gradient
  for first births (tempo) with higher-order births (quantum); otherwise report what the published data cannot
  answer.

## Pre-registered expectations (to be confirmed, contradicted, or reported null)
- **E1 (canonical):** within country x survey/cohort and age, more schooling means fewer children ever born.
  Expected sign: negative for primary, secondary and higher relative to none, monotone dose-response.
- **E2 (cohort/generational):** the schooling gradient is steeper in later birth cohorts than earlier ones.
- **E3 (pipeline density):** the gradient is steeper in countries with higher female attainment (later
  pipeline stage) than in countries in the early stage.
- **E4 (not just income):** education survives a wealth control. Expect attenuation (perhaps 20–50%) but a
  still-negative, significant education coefficient.
- **E5 (quantum vs tempo):** education reduces higher-order births more than first births — the effect is
  mainly quantum (stopping) rather than only tempo (delaying).
- **E6 (place and sex):** the gradient is negative in both urban and rural women. Placebo: a measure of
  *other people's* schooling (community/region education, or men's/husband's education where available) should
  not carry a strong gradient on a woman's CEB once her own education is included; if it does, that is
  evidence the association is a community-development artefact, and it will be reported as such.

## Falsifiers, stated in advance
The theory's claim fails if any of the following holds: (i) the within-country/cohort gradient is absent or
positive; (ii) it disappears or reverses once wealth is controlled; (iii) it does not steepen across cohorts
or pipeline stages; (iv) all of the association is carried by the community-level placebo rather than own
schooling. A null or reversed result will be reported with the same prominence as a confirmation.

## Power / precision commitment
Every estimate will carry a clustered standard error and the number of countries, surveys, age groups and
(women or cells); where the sample is too small or the API too coarse to separate a prediction, the record
will say "not testable with these data" rather than substitute a weaker claim.
