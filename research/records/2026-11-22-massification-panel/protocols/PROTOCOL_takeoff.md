# Protocol takeoff: does tertiary massification need all three actors?

**Written 2026-11-22, about 16:05 CST, before any data were downloaded.** This is the cross-national test of the boot-up version of the triad: Trey's spoken version, which goes beyond the October draft.

## Claim tested

Tertiary massification takes off only when three conditions are all present:
- **household means**, measured as log GDP per head;
- **employer demand**, measured as economic complexity (ECI, Harvard Growth Lab, at Trey's request);
- **state capacity**, measured as government final consumption, % of GDP.

One or two conditions alone are not enough.

## Definitions

- **Takeoff:** the first year a country's tertiary GER reaches 15% (Trow's elite-to-mass threshold). The series is interpolated linearly between WDI observations, never extrapolated. A country is at risk only after a first observation below 15%. Countries already at 15% or above when first observed are excluded (left-censored).
- **Timing:** all conditions are measured 5 years before each year at risk.
- **Presence:** a condition is "present" when it is at or above its median among at-risk country-years.
- **Robustness specs:**
  - employer measured as the non-agricultural share of GDP instead of ECI;
  - state measured as tax revenue, % of GDP, instead of government consumption.

## Models

All are discrete-time hazard logits with decade dummies.

| Model | Terms |
|---|---|
| H | household only |
| add | H + E + S, continuous |
| conj | one indicator: all three present |
| add_conj | add + the all-three indicator |
| count | indicators for 1, 2 and 3 conditions present |

## What counts as support for boot-up (all four needed)

1. In 10-fold cross-validation by country, `add_conj` or `count` beats `add` on held-out log loss.
2. The jump in takeoff odds from 2 to 3 conditions is bigger than from 1 to 2, in at least 80% of 2,000 country-cluster bootstrap draws.
3. At least 80% of takeoffs happen with all three conditions present.
4. The conjunction coefficient stays positive in at least 80% of 1,000 Monte Carlo draws of the thresholds (each condition's cut drawn between its 30th and 70th percentile).

## Also reported

- **Lock-in:** after takeoff, how often tertiary GER falls by 25% or more within 5 years, comparing years where a condition dropped below its threshold with years where none did.
- **Case timelines** for the Philippines, Cambodia, Hong Kong, Korea, Thailand, Vietnam, Indonesia, Malaysia, China and India.

## Limits

- This is observational and not blind: these countries' histories are broadly known.
- The ECI series is trade-based and covers only exporting economies.
- Government consumption is a rough proxy for state capacity.
- Thresholds at the median are a convention. That is why they are varied in the Monte Carlo.

## Amendment A1 (2026-11-22, about 16:10 CST)

**Written after a 40-draw smoke run, before the full run.**
- The only ECI series reaching back to the 1960s is the OEC rank series: Our World in Data, 1964–2016. The Harvard SITC ECI in the downloaded file starts in 1995.
- Raw ranks shrink when fewer countries are ranked, which made nearly every country "cross" the employer threshold in 1969.
- Ranks are therefore converted to within-year percentiles (1 = most complex).
- Nothing else changes.
