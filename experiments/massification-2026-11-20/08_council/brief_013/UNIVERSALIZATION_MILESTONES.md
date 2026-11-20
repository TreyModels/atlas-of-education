# UNIVERSALIZATION MILESTONES — timing is the outcome for near-universal systems

**User directive, 20 Nov 2026; Council adopted (D34).** For systems already near universal (Japan, Korea, Hong Kong —
and any country/level once it is), the first-order outcome is **when** universalization happened, not the level. This
file defines the milestones, the crossing-year estimand, the censoring rules and the timing tolerances; it is part of
the binding gate (`SUCCESS_CRITERIA.md`, Amendment A4; `STOP_RULES.md`, R19).

## Milestones (declared thresholds)

| ID | Milestone | Threshold | Preferred measure (fallback) |
|---|---|---|---|
| M0 | Massification (expanding systems) | **cohort completion ≥ 50%** | UIS CR observed (PHL/CHN/KHM) |
| M1 | Primary universalization | **NER ≥ 95%** (or **GER ≥ 100%** where NER absent) | UIS NER; GER observed |
| M2 | Lower-secondary universal completion | **completion ≥ 90%** (cohort, CR.2 observed) | UIS CR.2; CR.1 if missing |
| M3 | Upper-secondary universal completion (or transition) | **completion ≥ 90%** (transition ≥ 90% where completion absent) | UIS CR.3; observed transitions |
| M4 | Mass tertiary | **tertiary GER ≥ 50%** | UIS GER tertiary, observed |

A system/level is **near-universal** for the timing regime if the observed series is at/above the threshold for the
first **10 observed years** it covers (i.e., the crossing is at or before the start of observation, or within it).
Milestones are thresholds, not natural constants: any change is an amendment.

## Crossing-year estimand

- **Year of crossing** = first observed year at or above the threshold; the **band** is [last observed year below,
  first observed year above] (bounded by observations; no interpolation beyond adjacent years).
- If only the band's width is >2 years, the point estimate is the band midpoint and the uncertainty is reported with
  the band width.
- **Left-censored** (series begins at/above threshold): the crossing is before the first observed year — the estimand
  is a **boundary constraint** ("crossed at or before year Y0"); the model must cross at or before Y0 and receives no
  point-timing credit.
- **Right-censored** (never crosses by the last observed year): "not reached"; the model must **not** cross
  (false-positive test).
- No imputed/modelled series may create a crossing; observed cells only.

## Timing tolerances (replace level tolerance for near-universal systems)

| Regime | Required | Check-only |
|---|---|---|
| Near-universal (JPN, KOR, HKG; any level at/above threshold for ≥10 observed years) | **crossing year within ±5 years** of the observed year (band midpoint); ±3 years where the band ≤2 years and no definition break within the window; left-censored: cross at or before Y0 | final observed level within ±5 pp (check, never fitted) |
| Expanding (PHL, CHN, KHM levels not yet near-universal) | existing level tolerances (5 pp in-sample, 8 pp out-of-sample, beat persistence and linear trend) | timing reported descriptively |

**Single-curve note:** a fit must reproduce the **crossing/midpoint timing** within tolerance; the functional form
(logistic vs Gompertz vs other bounded forms) may vary and is not required. If the model reproduces levels but not
timing, that is a **structural miss** of the same kind as the wrong-sign scaling law (R19). Supplying the timing
(midpoint as an input) is R4 and invalid.

## What the model must reproduce

1. Observed crossing years for all identifiable milestones, within the timing tolerances (or boundary constraints for
   left-censored cases).
2. No false crossing where the observed series did not cross (false-positive).
3. Levels check-only for near-universal milestones; no level fitting for those cells.
4. Report per country × milestone: observed crossing year (band), simulated crossing year, verdict
   PASS/PARTIAL/FAIL/LEFT-CENSORED/WRONG (timing miss).

## Data status

Observed series: `10_massification/data/UNIVERSALIZATION_SERIES.csv` (2,458 rows) and `04_data` observed cells; JPN
primary/higher-secondary likely left-censored (crossed before the observed window) — record as boundary constraint, do
not invent a crossing. KOR/HKG crossing years to be derived from the observed series; if the series start after the
crossing, left-censored applies. No timing claim may rest on modelled/imputed cells.


## Clarification C1 (2026-11-20 15:10, Council) — requested by executor

- **M0 added:** massification crossing = cohort completion ≥50% for expanding systems (PHL/CHN/KHM); universalization
  milestones remain M1–M4 (95/90/90/50 thresholds as defined). Crossing year = first observed year at/above threshold.
- **N confirmed: ±5 years** (band midpoint), **±3 years** where the observed band ≤2 years and no definition break
  within the window — consistent with §3's midpoint tolerance; this is the timing tolerance for JPN/KOR/HKG and any
  near-universal level.
- **Timing is a HOLDOUT outcome:** crossing years are never fitted; the model must generate them (R4/R5). A fitted or
  supplied crossing/midpoint invalidates the claim.
- **Censored-ratio reconstruction rule (UIS ratios censored from headcounts/population):** reconstruct only from
  observed headcounts and documented population denominators; label the series **"reconstructed (not UIS)"**; record
  method and uncertainty (band from denominator choice and adjacent observations); require sensitivity to two
  denominators; a crossing from a reconstructed series is flagged and can never be presented as an observed UIS
  crossing. No imputation may serve as observation.
- **Slate re-rank:** E6 (timing comparison) rank #2; **E9 (crossing-year reconstruction, data-first) enters at rank
  #3**; E4 Bartik rank #4; E2 rank #5; E1 rank #6 (parked); E3 rank #7 (DATA BLOCKED); E5 rank #8; E7 rank #9; E8 KILL.
