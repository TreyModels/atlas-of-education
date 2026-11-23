# Pre-registration: early-warning signals and diminishing returns around the transition (23 November 2026)

Committed before any computation on the country series. Fixes the event definitions, the early-warning
measures, the placebo designs, the diminishing-returns test, and the decision rules. Deviations will be
stated; nothing is silently dropped.

## Event definitions (fixed in advance)
**Primary event: fertility transition onset.** For each country with an annual total-fertility series, the
event year is the first year of the fastest sustained fall: compute the 10-year forward fall
(fertility in year t minus fertility in year t+10) for every t, and take the t that maximises that fall;
require the fall to be at least **1.0 births per woman** or the country is excluded from the event set.
Ties are broken by the earlier year. This is pre-specified so that an "event" is not chosen by looking at the
early-warning signals.
**Secondary event: schooling universalisation onset**, taken as dated in the prior project's
`UNIVERSALIZATION_TIMING.csv`, used only if it covers at least 25 countries and the event year falls inside the
fertility series. It is a secondary check because it comes from a different source with different coverage.

## Early-warning measures (fixed in advance)
For each country, take the **15 years ending 5 years before the event** (so the window ends before the
transition is under way, avoiding mechanical contamination). Detrend by ordinary least squares on a linear
trend within the window and keep residuals. Split the window into three overlapping 10-year sub-windows and
compute, in each:
- **variance** of the detrended series,
- **lag-1 autocorrelation** of the detrended series,
- **skewness** of the detrended series.
The early-warning signal is the **slope of each measure across the sub-windows** (does variance and
autocorrelation rise as the event approaches). Primary measure: lag-1 autocorrelation trend; secondary:
variance trend. Skewness is reported descriptively.

## Placebos and nulls (fixed in advance)
Three nulls, all pre-specified:
1. **Pseudo-events within country**: for each country, 200 pseudo-event years drawn uniformly from its series,
   excluding any year within 10 years of the real event and requiring the same 15-year pre-window to exist.
   The test statistic is the mean early-warning slope at real events minus at pseudo-events.
2. **Placebo transitions**: countries whose fastest 10-year fall is below 0.3 births per woman, treated as
   having no transition; their mean early-warning slope is compared with the event countries.
3. **Detrended surrogates**: for every event window, 200 surrogates built by first-differencing the residuals
   and re-integrating in random order (a phase-randomised-style surrogate), which preserves the autocorrelation
   structure but destroys a systematic approach to the event.
Report **effect sizes with uncertainty** (event-minus-placebo difference with its standard error), not only
p-values, and the **minimum detectable effect** at 80% power given the observed dispersion. A null is not
evidence of absence: the power statement is part of the result.

## Diminishing returns / ratchet (fixed in advance)
Model, for country-year observations with both series:
**10-year change in fertility = a + b1 (schooling completion at t) + b2 (schooling completion at t)^2
+ region fixed effects**, estimated on the sample where completion is observed and the 10-year change is
defined. Pre-registered prediction under diminishing returns: **b1 < 0 and b2 > 0** (a concave response, each
further unit of schooling buys less fertility decline), with the turning point reported and only interpreted if
it lies inside the observed completion range. A ceiling test: the marginal effect at the 90th percentile of
completion versus at the median, with a bootstrap interval. If b2 is not positive, the ratchet claim is
reported as a failure.

## Decision rules agreed in advance
- Early-warning signals are "present" only if the event-minus-placebo difference is positive, at least twice
  its standard error, **and** survives the surrogate null.
- Diminishing returns are "present" only if b2 > 0 with a bootstrap interval excluding zero **and** the
  marginal effect is smaller at high completion; otherwise the result is a null and reported as such.
- Everything measured on annual country series with trend breaks; no claim about individual mechanisms, and
  no causal language. Short series and contested methods are stated in the report's limits, with the MDE.
- If a series covers fewer than 25 countries with a usable event, the headline is labelled a data gap.

## Data (named in advance)
Annual total fertility, child mortality, urbanisation, lower-secondary completion and secondary attainment from
`/root/work/data`; the universalisation timing and series from `/root/work/local_data/10_massification/data`;
the long-run historical panel from `/root/work/transition/out`. No new downloads are planned; if a series is
missing the affected test is dropped and said so.
