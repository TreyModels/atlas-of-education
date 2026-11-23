# Pre-registration — subsistence model v2: calibration repair + cohort sequencing

Committed **before** any v2 data pull, code or estimate. Date: 23 Nov 2026. Task `task-26`.
Branch `research/subsistence-v2-2026-11-23` (off `research/subsistence-2026-11-23`, task-22 @ 41f6429);
record `research/records/2026-11-23-subsistence-v2/`; box2 `/root/work/subsistence_v2`.

## What v1 (task-22) failed at, to be repaired
1. Agricultural employment share falls too fast: model 8.1% in 2020 vs data 19.4% (1960 anchor 31% vs 30.6%).
2. Population grows too fast: model index 4.4 vs data 2.9 (1960 = 1).
3. Recovery identified 2 of 3 parameters; the wage-premium weight was not identified.
The repair hypothesis to be tested: (1) and (2) are partly one problem — labour release is tied too tightly
to mechanisation and the absorbing wage sector is not explicit, while the mortality/fertility block lets the
population run ahead of the data.

## v2 design (fixed now)
- **Agriculture:** Boppart-style labour demand. Productivity = agricultural TFP path x input intensity^0.5,
  with the CES elasticity sigma = 1.5 carried over from the task-22 estimate. Observed relative input prices
  drive intensity. Two repairs: (i) the TFP growth rate becomes a **free calibrated parameter** instead of
  being imposed from USDA (so the model's ag-share path is fitted, not mechanically driven); (ii) food demand's
  income elasticity becomes a **free calibrated parameter**.
- **Absorbing sector, explicit:** a wage/formal sector whose job stock grows at a rate J(t+1)=J(t)(1+gJ)+
  creation from non-agricultural capital; released labour either enters formal jobs or the schooling/credential
  queue (queue = labour supply - ag labour - formal jobs). The queue and the wage premium feed enrolment;
  schooling lowers desired fertility (quantity-quality). No released worker "vanishes".
- **Demography:** child-mortality and life-expectancy paths from the transition record; a **mortality-timing
  shift** parameter allows the mortality decline to be earlier/later so the population path can be fitted.
  Desired surviving children at zero schooling and the schooling effect on desired fertility are calibrated
  directly from the TFR/survival/schooling endpoints (not free), as in v1.
- **Free parameters: exactly 5** (GATE satisfied): queue weight in schooling, formal-job creation rate,
  agricultural TFP growth, food income elasticity, mortality-timing shift. Everything else is calibrated,
  estimated (sigma 1.5) or assumed, and labelled in the output.
- **Fit targets:** 1960-2020 stylised-country medians for agricultural employment share, TFR, mean years of
  schooling, wage-employment share, and the population index (1960 = 1).

## Pre-registered tests and predicted outcomes
- **C1 calibration repair:** v2 should reduce the two failures (ag share ~19% and population ~2.9 by 2020
  rather than 8% / 4.4) without worse fits on TFR/schooling. Failure = either target still off by more than
  5 percentage points (ag share) or 0.5 index points (population) at 2020, or a much worse TFR/schooling fit.
- **C2 parameter recovery:** re-simulate from known parameters and re-fit all five. Predicted: parameters
  whose data influence is strong (job creation, TFP growth, mortality timing) recover within 10%; weakly
  identified ones must be reported as such rather than claimed.
- **C3 counterfactuals:** (a) freeze mechanisation after 1960 (v1 result: ag share 17.9% vs 8.1%, schooling
  5.6 vs 8.2, TFR 2.52 vs 2.19); (b) freeze the schooling pipeline (no expansion) — predicted: released labour
  cannot be absorbed into schooling, the queue grows, fertility stays higher, and the model matches history
  worse; (c) freeze the mortality decline (hold child mortality at its 1800 level) — predicted: no population
  explosion, so the schooling pipeline does not need to universalise and fertility stays higher. Which
  counterfactual is furthest from history is the model's implicit claim about the first mover.

## C4 cohort-level sequencing test (pre-registered definitions)
Data: transition-record long-run panel (child mortality, life expectancy, TFR, schooling, income, urban share)
merged with WDI agricultural employment share (1960-2020) and the project panel.
- Country-level event dates, all defined before estimation:
  - **agricultural labour release onset** = first year (1950-2020) after which the agricultural employment
    share falls by at least 3 percentage points within 10 years and does not recover above its starting value;
  - **schooling take-off** = first year the mean years of schooling rises by at least 1.0 year within 10 years;
  - **fertility decline onset** = first year TFR falls by at least 1.0 birth within 10 years (using the
    observed TFR series, not the derived one).
  - Each date is also expressed as the **birth cohort entering the labour market then** (year - 20) to state
    the claim in cohort terms, with the caveat that the data are period series, not linked cohort histories.
- **Sequencing statistic:** share of countries where release onset <= schooling take-off onset and
  schooling take-off <= fertility onset; median gaps with bootstrap CIs clustered by country. Predicted (the
  theory's claim): release first, schooling second, fertility third in a majority of countries.
- **Falsifiers:** if schooling take-off or fertility decline precedes agricultural labour release in a
  majority of countries; if the release-to-schooling gap is indistinguishable from zero; or if the ordering
  is driven by a handful of countries. All reported plainly.
- Cohort caveat stated up front: with period data the strongest defensible statement is about event ordering
  within countries, not about a linked cohort's own outcomes.

## C5 US historical laboratory (the sharper test)
Data: OWID long-run series (agricultural employment share, fertility, mean years of schooling, agricultural
output per worker) pulled from box2 with browser UA; the pull is network-bound and runs regardless of CPU.
- Same onset definitions applied to the US; predicted ordering: farm-employment decline onset (mechanisation/
  tractor adoption era) before the high-school movement before the fertility decline. If the US order is
  schooling first or fertility first, the theory's "floor falls first" claim fails in the one country where
  all three dates are observable and the record must say so.
- **Falsifier:** US schooling or fertility onset earlier than farm-employment onset by more than 5 years.

## Reporting
Plain words, both headings "(1) Fertility" and "(2) Massification", <140 lines, every number with sample and
uncertainty, every parameter labelled estimated/calibrated/assumed, failures kept, and the answer to the
repair-hypothesis test stated explicitly.
