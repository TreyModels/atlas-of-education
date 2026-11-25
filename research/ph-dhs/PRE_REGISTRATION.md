# Pre-registration — Philippines DHS attendance / wealth-quintile credential-floor test

**Date:** 25 Nov 2026. **Status:** pre-registered before the PH outcome was computed.
**Purpose:** run the same credential-floor test as Cambodia: attendance at ages 14–17 by wealth quintile and the
share of non-attenders from the bottom two quintiles (bottom 40%), compared with model predictions
(human capital ≈65%, relational floor ≈98%). Secondary: attendance by age group/sex/residence for the
observation-equation/calibration work. Descriptive only; no causal claims.

## Data
Philippines DHS PR recodes: 2003 (PHPR41), 2008 (PHPR52), 2013 (PHPR62, Stata), 2017 (PHPR71), 2022 (PHPR82,
Stata). The 1993 and 1998 PR recodes do **not** contain `HV121`/`HV122` (attendance) or `HV270`/`HV271`
(wealth quintile); they carry `HV106–HV109` (education/completion) and have separate WI files (`WHHID`,
`WLTHINDF`, `WLTHIND5`) for a later completion-by-quintile check. The 1993 INDEPTH file is a special
subsample and is excluded. Raw microdata are not committed (DHS terms); only derived tables + hashes are.

## Variables / measurement (fixed before computation)
- `HV105` age; `HV104` sex; `HV121` attended during the current school year; `HV122` current-year level;
  `HV025` residence; `HV024` region; `HV005` weight (`/1e6`); `HV270` wealth quintile (1 poorest–5 richest).
- **Attendance** = `HV121 ∈ {1,2}` (attended during the current school year). Checked against the wave's
  codebook; if a wave uses only 0/1/2, this is the same upper-bound used for Cambodia.
- **Credential-floor statistic:** ages 14–17; weighted attendance by quintile; weighted share of
  non-attenders (`attendance==0`) from the bottom two quintiles.
- Secondary: ages 6–11, 12–14, 15–17 attendance by sex and residence.
- Estimator: weighted percentages (`HV005/1e6`); Taylor-linearized SE with PSU (`HV021`) within strata
  (`HV022`) where available; unweighted n reported.

## Decision rule
Compare the bottom-40 share of 14–17 non-attenders with the model predictions (HC ≈65%, relational ≈98%):
near 98% supports the relational floor; near 65% supports human capital; materially below both rejects both
(as in Cambodia, where it is 47.5–51.6%). Report the full quintile profile; do not tune the
exits/non-attender mapping to rescue a structure.

## Outputs
`results/quintile_attendance_14_17.csv`, `results/attendance_by_wave_sex_res.csv`, `results/catalog.json`,
`REPORT.md`. Scripts + hashes committed; raw SAS/DTA not committed.
