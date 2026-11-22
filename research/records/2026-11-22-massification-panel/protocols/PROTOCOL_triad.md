# Protocol triad: households, employers, state, in three countries

**Written 2026-11-22, about 15:40 CST, before any Triad result was scored.** Two smoke-test fits ran (KHM HS seed 0, HKG HE seed 0) and only their training costs were seen. Status: retrospective and inspected, not blind.

## Question

Menefee and Nordtveit's surplus motor says massification is driven by three actors:
- **households**, who want income ("rice");
- **employers**, who want formatted, credentialed workers;
- **the state**, which wants surplus and capacity ("F-16s").

Using the same cohort engine and the same enrolment-only targets in the Philippines, Cambodia and Hong Kong, does adding the employer or state term improve held-out enrolment forecasts over households alone? And where?

## Measured drivers (`countries/triad_drivers.json`)

- **Employer (`b_e`):** non-agricultural share of employment, computed as 100 minus the agricultural share. WDI/ILO values are used from 1991. Before that, national series are spliced in: Philippines 1956–89 (Chiba, Hi-Stat DP304; a secondary source with a break at 1964/65); Hong Kong census 1961 and 1971. Cambodia has only 1991 onward.
- **State (`b_s`):** government education expenditure, % of GDP (WDI). Coverage is sparse: Philippines from 1980, Hong Kong from 1971, Cambodia from 1998. Between data years the series is interpolated linearly; outside them it is held flat.
- Military spending (the literal "F-16s") was collected but is **not** used. Hong Kong has none, so it can't be compared across the three cases. It is reserved for a later Philippines/Cambodia check.

## Models

All four Triad specs share the same engine, with five level intercepts fitted. Cost scale is fixed at 1, the income gradient at 0, and private-sector settings at their defaults.

| Spec | Actors | Behavioural settings |
|---|---|---|
| H | households | `eta` (income), `kappa` (cost) |
| HE | + employers | + `b_e` ≥ 0 |
| HS | + state | + `b_s` ≥ 0 |
| HES | all three | + `b_e`, `b_s` |

Comparison models:
- logistic S-curve per series (diffusion);
- persistence;
- linear trend;
- Page ensemble (mean of H, HE, HS, HES and logistic);
- Silver blend (0.5 × persistence + 0.5 × ensemble).

Six starts per spec; the best training cost is kept.

## Split and metric

| Country | Training years | Held-out years |
|---|---|---|
| Philippines | ≤1995 | 1996–2024 |
| Cambodia | ≤2010 | 2011–2024 |
| Hong Kong | ≤2011 | 2012–2024 |

- Hong Kong's held-out years are the DSE era. Its training includes the 1970s NER rows.
- **Primary metric:** pooled held-out RMSE over primary NER, secondary NER and tertiary GER. Where a level has no held-out NER, its GER is used instead.

## Decision rules

1. Losses first. A model "beats naive" only if it beats both persistence and trend.
2. An actor is **supported in a country** only if its spec (HE or HS) meets all three conditions:
   - beats H;
   - beats logistic;
   - has its dial off the bound.
3. **Tilly comparison:** a mechanism counts as a **recurring** mechanism only if it is supported in at least two of the three countries. Supported in exactly one country, it is **case-specific**.

## Monte Carlo 1: can the data tell the actors apart?

For each country and each true spec:
- simulate training data from that spec's real-data fit, plus 1 percentage point of noise;
- refit all four specs and choose by AIC;
- repeat 20 times.

The result is a 4×4 confusion matrix per country, plus parameter recovery under the boundary-censoring rule from v6_phl. **If the true structure is chosen in fewer than 60% of replicates, that country's actor verdicts are labelled "not identifiable from these data", whatever rules 1–3 say.**

## Monte Carlo 2: is the simulated Triad's necessity result robust?

The agent-based Triad (`code/triad`) is run with:
- a Latin hypercube of 2,000 samples over 23 parameters, each varied over a declared range around its default;
- 2 seeds per sample;
- baseline plus three single-actor knockouts.

An actor is "necessary" in a sample if removing it cuts end-state tertiary share by half or more. We report the share of the parameter space where each actor is necessary, and which parameters govern that. This is a theory-robustness check, not an empirical test.

## Known limits

- Driver coverage is thin before 1991 except for the Philippines' employment series.
- Cambodia's training window starts after its 1970s collapse.
- Hong Kong has no tertiary data before 2003 in the targets.
- None of this is blind.
