# Cambodia out-of-school: which number the model should match

Decision memo, TODO §10 P1 "Settle the Cambodia out-of-school observation equation", 5 November 2026.

## The disagreement

| Source | Year | Ages 6–11 | Ages 12–14 | Ages 15–17 | How it counts |
|---|---|---:|---:|---:|---|
| UNESCO UIS (current calibration target) | 2024 | 3.7% | **17.6%** | 48.9% | Children of each level's official age **not enrolled in any level**. Enrolment comes from administrative school records, divided by UN population estimates. |
| Census, NIS | 2019 | 9.4% | **8.4%** | 32.4% | 100 − share of each age group **attending** school (household-reported). |
| CSES 2012 (All in School country study) | 2012 | 13.2% | **11.4%** | n/a | Household survey, not attending, by age |

UIS definition: under the 2019 methodology, children "are now considered out of school if they are not enrolled in pre-primary, primary, secondary or post-secondary education" (UNESCO fact sheet, 2019).

The two household sources agree with each other and fall over time (11.4% in 2012 → 8.4% in 2019 at ages 12–14). UIS is about twice the survey figure at lower-secondary age, and much higher at upper secondary. It is lower at primary age, where the census counts 6-year-olds who have not yet started school.

## What the model measures

In `camchild.js` (and `engine/camchild.py`), a child is out of school when the household chooses **work** or **neither** for that year. The level is set by **age** (≤11 primary, 12–14 lower secondary, 15–17 upper secondary). That is an attendance concept by age group, which is what a household survey or census measures. It is not an enrolment-register count over a projected population.

Admin-over-population rates are known to be sensitive to the population denominator. If UN projections overstate a cohort, the out-of-school rate is overstated. Admin rates also miss children enrolled but not attending, and the reverse. Both effects can produce a factor-of-two gap of this kind. This memo does not settle which one applies in Cambodia.

## Decision (recommended; needs Trey's sign-off because the app text names UNESCO)

1. **Calibrate to household attendance by age**, the model's own concept. Use the 2019 census now, and the CSES 2019/20 or DHS 2021–22 attendance tables when they are in hand (DHS Table 2.12 "School attendance ratios"; not reachable from this sandbox).
2. **Keep UIS as a diagnostic** in the app, labelled "administrative enrolment ÷ UN population estimate". Do not use it as a target.
3. **Urban/rural split:** use the CSES 2012 ratios (primary 1.9×, lower secondary 3.8×) until a newer survey gives Phnom Penh directly.

Ready-made constants under this decision (solved by `engine/camchild_ridge.py`, variant `census2019`; national out of school 9.3 / 9.2 / 34.9%):

| Region | vPrim | vLow | vUp |
|---|---:|---:|---:|
| Phnom Penh | 2.197 | 4.830 | 1.290 |
| Countryside | 2.859 | 7.213 | 3.257 |

These replace (shipped, UIS-tuned): Phnom Penh 3.391 / 2.162 / 0.886; countryside 3.506 / 5.657 / 2.199.

Applying the switch means editing `REGIONS` in `web/camchild.js` and `engine/camchild.py` together; the parity test enforces this. It also means updating the calibration check in `tests/test_camchild.cjs` to the census targets, rerunning `engine/camchild_record.cjs` for the 30-seed bands, and changing the "What is calibrated" text in the app.

## What it does not fix

Child labour stays at about 14% under either target set (`camchild_ridge.md`), against 10.7% in the 2012 child labour survey. The gap is on the work side. The next item is that retune, with the 2012 survey put on the model's child-labour definition: work for under-15s, hazardous or over 48 hours for 15–17s, and school-and-work under 12.

## Sources

- UNESCO UIS, "New methodology shows 258 million children, adolescents and youth are out of school" fact sheet (2019): https://www.allinschool.org/media/2856/file/UNESCO-Fact-Sheet-New-Methodology-2019.pdf
- NIS, General Population Census 2019 leaflet (attendance by age): https://nis.gov.kh/wp-content/uploads/2025/09/Final-Leaflet-Census-Report-2019-Eng.pdf
- All in School, Cambodia Country Study 2016 (CSES 2012 tables 2-3, 2-4, 2-6): https://www.allinschool.org/media/3456/file/Country-Study-Cambodia-2016.pdf
- DHS 2021–22 final report (Table 2.12, not read here): https://www.dhsprogram.com/pubs/pdf/FR377/FR377.pdf
