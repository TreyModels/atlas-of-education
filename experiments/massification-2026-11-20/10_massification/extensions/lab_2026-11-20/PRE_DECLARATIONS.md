# Lab battery 2026-11-20 — predeclared secondary & post-secondary experiments (geo scale × economy)

**Status:** predeclared before running; **observed/derived rows only as labelled**; descriptive/associational; no
causal or direction claims. Data: `10_massification/data/`, `09_relations/data/panel_wdi_wide.csv`, ECI panels.
Each experiment states its estimand, threshold and falsifier; all cells reported including nulls.
Background: closed phase at `4ba958c` (PARTIAL/DESCRIPTIVE/EQUIVALENT). This battery does not reopen C1–C4.

## E1 — income/urban/services gradient in upper-secondary enrolment
Unit: country-year. Sample: 6 systems, 1995–2024 (observed). Dep: upper-secondary GER (SE.SEC.ENRR.UP).
Regressors: log GDP p.c. PPP, urban share, services employment share. Estimand: within (country-demeaned) and
between partial slopes, cluster-robust 95% CI. **Threshold:** association present if CI excludes 0 in BOTH within
and between; "strong" if within slope ≥ 3 GER pp per log-GDP point. **Falsifier:** neither CI excludes 0.

## E2 — structure at milestone crossings
Unit: country × milestone (crossing year). Sample: 6 systems; milestones from UNIVERSALIZATION_TIMING.
Estimand: median [IQR] of income p.c., urban share, agri share at the crossing year. **Threshold:** a milestone is
"structure-typical" if ≥4/6 countries with a dated crossing fall inside the cross-country IQR. **Falsifier:** ≤3/6.

## E3 — regional equalization (PHL, 17 regions)
Unit: region × cohort. Sample: PIDS/Psa 2010 aggregates, cohorts 1960–64 and 1990–94. Dep: education Gini.
Regressors: mean years of schooling; cohort. Estimand: cross-region slope of Gini on MYS by cohort; Δslope.
**Threshold:** "equalizing" if Gini falls ≥0.02 in ≥10/17 regions AND slope is negative in both cohorts.
**Falsifier:** fewer than 10 regions improve or slope non-negative.

## E4 — city-state vs large-country shape
Unit: system. Sample: HKG (city-state/autonomous) vs CHN, PHL, KHM (large). Dep: duration between lower-secondary
(≥90) and tertiary (≥50) crossings; volatility = SD of annual secondary GER changes. Estimand: medians; ratios.
**Threshold:** "faster" if duration ratio ≥1.5; "smoother" if volatility ratio ≥2. **Falsifier:** ratios <1.2.
(n ≤ 3 per group; descriptive only.)

## E5 — structure and tertiary expansion (30 countries)
Unit: country-year. Sample: 30-country WDI panel (1960–2024, unbalanced; 1995–2024 primary). Dep: tertiary GER.
Regressors: services share, log GDP p.c., urban share, ECI (eci_hs92). Estimand: within (country FE) and between
slopes, cluster CIs. **Threshold:** association if within CI excludes 0 and sign is stable with eci_sitc.
**Falsifier:** CI includes 0 or sign flips.

## E6 — formalisation and upper-secondary completion
Unit: country-year. Sample: 6 systems, 1995–2024. Dep: upper-secondary completion (observed/derived flagged).
Regressor: wage-and-salaried share. Estimand: within-country correlation at lags 0 and 5. **Threshold:**
association if |within r| ≥ 0.4 at lag 5. **Falsifier:** |r| < 0.2 at both lags.

## E7 — state capacity around secondary crossings
Unit: country-year in a ±5-year window around a dated crossing. Sample: 6 systems. Dep: standardised capacity
dimensions (fiscal, delivery, enforcement). Estimand: post-minus-pre mean difference in SD units.
**Threshold:** "capacity-linked" if |Δ| ≥ 0.25 SD in ≥2 of 3 dimensions. **Falsifier:** <2 dimensions.

## E8 — PHL infrastructure strain during secondary expansion
Unit: PHL year. Dep: secondary PTR (WDI). Regressor: annual change in secondary GER. Estimand: OLS slope.
**Threshold:** "strain" if PTR rises > 1.0 per 1 pp GER growth sustained ≥3 consecutive years.
**Falsifier:** slope ≤ 0.

## E9 — remittances, spending and enrolment growth
Unit: country-year. Sample: 6 systems (PHL/KHM exposed). Dep: education spending %GDP; secondary/tertiary GER growth.
Regressor: remittances %GDP (lag 1). Estimand: within-country partial association. **Threshold:** flagged if CI
excludes 0 with consistent sign across spending and GER specs. **Falsifier:** CI includes 0.

## E10 — external replication of E1 (30 countries)
Unit: country-year. Dep: upper-secondary GER (SE.SEC.ENRR.UP). Regressors as E1. Estimand: pooled/between slope.
**Threshold:** replication if the E1 within slope lies inside the 30-country 95% CI (and sign agrees).
**Falsifier:** outside CI or sign disagrees.

**Reporting rules:** all specifications run and reported; status `observed`/`derived`/`check` carried; n and clusters
always reported; labels OBSERVED/SIMULATED; no causal language. Thresholds fixed before results.
