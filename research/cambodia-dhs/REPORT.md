# Cambodia DHS — school attendance / out-of-school, first results (25 Nov 2026)

Pre-registered in `PRE_REGISTRATION.md`; script `ingest_cambodia_dhs.py`; derived tables in `results/`.
Raw DHS microdata are **not** committed (DHS terms); only aggregates + file hashes are.

## 1. Extraction is validated against DHS Table 2.12 (2021–22)

DHS 2021–22 final report (FR377), Table 2.12 “School attendance ratios”:

| measure (2021–22) | DHS report | our PR extraction |
|---|---|---|
| Primary NAR (age 6–11, attending primary) | **72.8** (M 72.0, F 73.5) | 6–11 any-current-year attendance **74.7** (M 73.2, F 76.1) |
| Primary GAR | 92.5 | — |
| Secondary NAR (age 12–18, attending secondary) | **42.0** (M 39.2, F 44.9) | 12–14 any 72.0; 15–17 any 51.1 (not directly comparable) |
| Primary NAR urban / rural | 75.5 / 71.3 | 6–11 any urban 79.7 / rural 73.5 |

The upper-bound measure (`HV121 ∈ {1,2}`, “attended during the current school year”) reproduces the
report’s NAR closely; the strict measure (`HV121==2 & HV122>0`) undercounts because `HV122=0` includes
preschool/early-childhood attendance and some current attendees. **Use the upper-bound variant as primary.**

Coding note: the 2000 recode uses `HV121==1` = currently attending; the 2005–2021 recodes use
`HV121==2` = attended during the current school year and do **not** use code 1. This is documented in the
script and is why both variants are reported.

## 2. Attendance by wave (%, upper-bound variant; strict variant in brackets)

| wave | 6–11 | 12–14 | 15–17 |
|---|---|---|---|
| 2000 | 66.6 [66.6] | 77.8 | 42.0 |
| 2005 | 76.7 [74.5] | 89.1 | 60.4 |
| 2010 | 90.4 [88.0] | 86.1 | 53.8 |
| 2014 | **90.4** [86.6] | 83.5 | 46.8 |
| 2021–22 | **74.7** [69.2] | 72.0 | 51.1 |

The 2014 DHS (90.4% at 6–11, i.e. ≈9.6% out of school) matches the **census 2019 household attendance**
(9.4% out of school at 6–11). The 2021–22 DHS is **16 points lower** at 6–11.

## 3. 2021–22 out-of-school vs the two candidate targets

| age group | DHS 2021–22 (100 − attendance) | census 2019 | UIS 2024 |
|---|---:|---:|---:|
| 6–11 | **25.3** | 9.4 | 3.7 |
| 12–14 | **28.0** | 8.4 | 17.6 |
| 15–17 | **48.9** | 32.4 | 48.9 |

The 2021–22 DHS is **not** a correction of the household concept — it is far above the census and UIS at
primary/lower-secondary. The 15–17 figure equal to UIS is coincidental.

## 4. Sex and residence (2021–22, upper-bound variant, %)

| age | Female | Male | Urban | Rural | Phnom Penh (female) | Other (female) |
|---|---:|---:|---:|---:|---:|---:|
| 6–11 | 76.1 | 73.2 | 79.7 | 73.5 | 82.8 | 69.3 |
| 12–14 | 72.3 | 71.8 | ~78.9 | ~69.6 | 87.3 | 69.9 |
| 15–17 | 55.0 | 47.5 | ~55.0 | ~49.9 | 65.0 | 52.4 |

Girls have higher attendance at primary and upper-secondary; urban and Phnom Penh are higher.
These match the report’s direction (primary NAR girls 73.5 vs boys 72.0; secondary 44.9 vs 39.2).

## 5. Interpretation — the decision memo needs a revision

The observation-equation memo (`docs/engine/cambodia_observation_equation.md`) said: use the 2019 census
now, and the DHS 2021–22 attendance tables when they are in hand. The data are now in hand and the answer
is **not** the one the clause anticipated:

- **DHS 2021–22 is a COVID-period observation.** Fieldwork ran Aug 2021–Feb 2022, through school closures
  and disrupted attendance. Its primary NAR is 72.8% (report) vs the census 2019 household figure of 90.6%
  attendance, and its 6–11 attendance is 16 points below the 2014 DHS. It should **not** be used as the
  calibration target for the pre-COVID household concept, and it should **not** be mixed with UIS or census.
- **The census 2019 household target stands** (9.4 / 8.4 / 32.4% out of school at 6–11 / 12–14 / 15–17).
  The 2014 DHS (90.4% at 6–11) is independent corroboration of the household concept at primary age.
- **Report DHS 2021–22 as a COVID-period sensitivity**, not a target: 25.3 / 28.0 / 48.9% out of school.
- The household-vs-UIS conflict remains (census 9.4/8.4/32.4 vs UIS 3.7/17.6/48.9). The DHS 2014 result
  supports the household side at 6–11/12–14; the 15–17 gap also reflects 2014-vs-2019 change and the
  any-level vs level-specific NAR definition.

**Recommended next step (needs operator sign-off):** keep the memo’s census-2019 calibration set for the
household concept; add a “COVID-period DHS 2021–22” sensitivity to the app/diagnostics; do not switch the
app text to UIS. No shipped model or app text was changed in this record.

## 6. Caveats

- NAR is level-specific (primary among 6–11, secondary among 12–18); our attendance is any-level, so the
  validation is approximate.
- 1998 National Health Survey excluded (different instrument; no PR recode). The two 2014 zips are the same
  data (different hashes: `d35f07b9…`, `efbc4e22…`).
- Weights `HV005/1e6`; Taylor-linearized SE with PSU (`HV021`) within strata (`HV022`); unweighted n in
  the CSVs.
- 2021–22 fieldwork during COVID school closures; the “current school year” question is affected.
