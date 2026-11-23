# Pre-registration — no-off-switch and alternatives-foreclosure tests, 23 Nov 2026

Frozen before any analysis script is written or any result computed. This file is the first
commit on branch `research/policy-foreclosure-2026-11-23`. Deviations, if any, will be
reported as deviations with the reason.

## A. No-off-switch (prediction 1)
**Claim under test.** Pipeline-compatible pronatalist policy (cash benefits, parental leave,
childcare subsidies) cannot restore *sustained* total fertility above about 1.6 in countries
already saturated below that level. "Saturated" = TFR below 1.6 in the year the policy is
introduced, or in the last pre-introduction year with data.

**Pre-specified predictions**
- P1a (bound test): among pronatalist introductions in saturated countries, the share of
  country-years with TFR above 1.6 at any point within 10 years of introduction is below
  10%. If the observed count is zero, report the exact one-sided 95% upper bound.
- P1b (event study): with country and year fixed effects and country-specific trends, the
  event-time coefficients 0..10 years after introduction show no *sustained* positive level
  shift; any positive point estimate is expected below 0.15 births per woman and to decay
  within 3 years.
- P1c (persistence): no country sustains TFR above 1.6 for 3 or more consecutive years
  within 10 years of introduction.

**Falsifiers (what would refute the prediction).** Any of:
1. At least one saturated country sustains TFR above 1.6 for 3+ consecutive years within 10
   years of a pronatalist introduction.
2. The event-study coefficient at 5 years after introduction is above 1.6 in level, or the
   estimated positive effect exceeds the minimum detectable effect below.
3. Recovery persists after controlling for the income cycle, urbanisation and net migration.

**Power.** The claim is an absence, so we state in advance how large an effect the design
could detect. With country and year fixed effects, α = 0.05, power = 0.80, the minimum
detectable post-introduction change in TFR is about 2.8 × the standard error of the
event-time coefficient; the realised standard error is reported with every estimate. The
design is also described by the number of introductions and countries. A claim of "no
sustained recovery" is only counted as a result if the detectable effect is smaller than
+0.15 births per woman.

**Rivals tested.** Income cycle (change in log GDP per head), urbanisation change, and net
migration per 1,000 people. Housing costs are not available in the local panel; that is a
stated limitation, not a test we can run.

## B. Alternatives foreclosure (prediction 2)
**Claim under test.** The credential pipeline's negative association with fertility is
strong where non-credentialed livelihoods (subsistence farming, informal employment, rural
life) have been absorbed, and weak where they survive. Pipeline coverage = secondary
completion at the start of a 10-year window (robustness: tertiary completion).

**Pre-specified predictions**
- P2a (primary model): 10-year-change panel; outcome = change in TFR over the next 10
  years; regressors = pipeline coverage at window start, its interaction with farm
  employment share at window start, the farm share, and controls; country fixed effects,
  decade fixed effects, country-specific linear trends, errors clustered by country.
  **Pre-registered sign: the coefficient on coverage × farm share is POSITIVE** (the
  negative coverage–fertility association is attenuated where farming livelihoods survive).
- P2b (gradient): the negative coverage–fertility association in the bottom tercile of farm
  employment is at least twice as large as in the top tercile.
- P2c (random-split null, reusing the grouping-multiverse logic): split countries into
  high/low foreclosure groups, compare with 400 random splits of the same sizes; the real
  high-versus-low difference in the coverage coefficient must exceed the 95th percentile of
  the random-split null.

**Falsifiers (what would refute the prediction).** Any of:
1. The interaction is zero, or negative (a *larger* negative association where farming
   livelihoods survive).
2. The interaction vanishes once coverage × log income and coverage × urbanisation are
   included (the classic masquerade).
3. The real high-versus-low gradient does not exceed the random-split null.

**Rivals tested.** Development level (log income) and urbanisation as alternative
moderators; the interaction term is reported with its standard error and confidence
interval, not just a significance marker. Informal employment (ILOSTAT) is included if
fetchable; otherwise farm employment and rural share are the two foreclosure measures.

## Data and code plan (fixed)
- Fertility and covariates: `/root/work/data/*.json` (World Bank/WPP panel, same construction
  as the grouping multiverse); income is stored in levels and is logged.
- Policy: an event list of pronatalist introductions compiled from public sources with a
  source note for each country/year, plus OECD Family Database intensity indicators if the
  API is fetchable from the server (family benefits as % of GDP, paid leave weeks, childcare
  enrolment). Policy intensity = number of active pronatalist instruments; primary test uses
  the event list, intensity is descriptive.
- Rivals: World Bank GDP per head, urban share, net migration.
- Samples: A = saturated low-fertility countries (OECD/EU/East Asia plus any country below
  1.6 with a documented pronatalist introduction), 1960–2023. B = all countries with data.
- No selective reporting: the full grid of models (primary, rivals, robustness, subsamples)
  is reported in one results table.

## Reporting
Plain words, under both headings, every headline with estimate, uncertainty (standard error
or confidence interval), sample and the test designed to kill it. Nulls reported prominently.
A data availability table lists every variable, source, coverage and what is missing.
