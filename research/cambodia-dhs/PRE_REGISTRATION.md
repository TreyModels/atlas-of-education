# Pre-registration — Cambodia DHS school attendance / out-of-school by age, sex, residence

**Date:** 25 Nov 2026. **Analyst:** DeepSeek lead. **Status:** pre-registered before any estimate was computed.
**Purpose:** settle the observation-equation question in `docs/engine/cambodia_observation_equation.md` —
does the model calibrate out-of-school to a household *attendance* concept (census 2019) or to the
administrative UIS enrolment concept? The memo's decision was to use household attendance and to add
DHS 2021–22 attendance tables when available. These are descriptive measurements, not causal estimates.

## Data
Cambodia DHS household/person recodes (PR): KHPR42 (2000), KHPR51 (2005), KHPR61 (2010), KHPR73 (2014),
KHPR82 (2021–22). Files on this machine under `~/neon-boot/pulled/dhs/cambodia/`; raw microdata not committed
(DHS terms); only derived aggregates + hashes are committed. The 1998 National Health Survey is a different
instrument and is not pooled; the two 2014 zips are the same files (noted, not duplicated). 2014 zip hashes:
`d35f07b9…` and `efbc4e22…`.

## Variables (DHS recode names)
- `HV104` sex (1 male, 2 female); `HV105` age in single years.
- `HV121` attended school during the current school year; `HV122` level during current year
  (0 none/preschool, 1 primary, 2 secondary, 3 higher).
- `HV025` residence (1 urban, 2 rural); `HV024` region (12 = Phnom Penh).
- `HV005` sample weight (*1,000,000); `HV021` PSU; `HV022` strata.

## Measurement (fixed before computation)
- **Current attendance (primary):** `HV121 == 1` OR (`HV121 == 2` AND `HV122 > 0`). Reason: the 2000 recode
  uses 1 = currently attending; the 2005–2021 recodes use 2 = attended during the current school year and do not
  use code 1, so `HV122>0` separates current-year attendees from past-only attendees.
- **Upper bound (secondary):** `HV121 in {1,2}` (any attendance during the current year).
- **Out-of-school rate** = 1 − current-attendance rate. Report both variants; primary is used for decisions.
- Age groups: 6–11, 12–14, 15–17 (primary); 6–14 and 15–17 as a check.
- Strata: national; urban/rural; Phnom Penh vs rest.

## Estimator
Weighted percentage with `HV005/1e6`; design-based Taylor-linearized SE with PSU (`HV021`) within strata
(`HV022`), 95% CI = estimate ± 1.96 SE; unweighted n reported. No imputation; missing/unknown attendance
excluded and counted.

## Comparisons / decision rule
Compare the 2021–22 DHS out-of-school estimate for ages 6–11, 12–14, 15–17 with:
- Census 2019 household attendance: 9.4 / 8.4 / 32.4 % out of school (memo table).
- UIS 2024 administrative: 3.7 / 17.6 / 48.9 % (memo table).
If the DHS 2021–22 estimate is materially closer to the census (household) concept than to UIS, record support
for the memo's household-attendance calibration; otherwise flag the conflict. Do not change the shipped model
or app text in this record — the calibration switch needs the operator's sign-off (memo §Decision).

## Outputs
`results/attendance_by_wave.csv`, `results/attendance_2021_22_by_sex_residence.csv`,
`results/catalog.json`, `REPORT.md`. Scripts + hashes committed; raw SAS files not committed.
