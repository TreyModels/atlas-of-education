# TARGETS_README — iteration-2 target sets

Owner: `data-hunter` (task-11). Written 2026-11-20. All files in `04_data/`. **Every value in these files is an observed value from a retrievable source. Nothing here is imputed, interpolated or modelled by this project.** Where a target does not exist, the row is present with `status=unresolved` and an empty value — the gap is part of the deliverable.

## Files

| File | Rows | Content |
|---|---|---|
| `TARGETS_SHADOW.csv` | 13 | Tutoring participation by country × stage × provider. Rate, year, denominator, source, confidence, `imputed=FALSE`, `status`. |
| `TARGETS_FLOW.csv` | 747 | Cohort-flow and credential targets: completion (primary/lower/upper), out-of-school, gross-intake proxies, Cambodian formality and degree share, HK attainment stock. Plus explicit unresolved rows for transition, repetition, dropout, wage premium, formal share. |
| `ECONOMY_SERIES.csv` | 4,031 | Annual 1995–2024 economy series: GDP p.c. (3 variants), urbanisation, remittances, sector and status employment, unemployment/youth/NEET/LFPR, population. Plus explicit unresolved rows for overseas deployment. |

## Status vocabulary — read this before using anything

- **`target`** — an observed point estimate that a model may be calibrated to or scored against. Definition, denominator, year and vintage are in the row.
- **`check`** — observed, but *not* a target. Either a different concept that is often mistaken for the target (gross-intake ratio as a "transition" proxy; parent-level rather than student-level tutoring), or a value whose denominator does not match the model's object. Use for plausibility, not calibration.
- **`unresolved`** — no verified observation was retrieved. Value is blank on purpose. The `notes` column names the blocker and what would fix it. **Do not fill these with model output and call them targets.**

## Country × domain matrix

| Domain | PHL | KHM | HKG | CHN | KOR | JPN |
|---|---|---|---|---|---|---|
| Tutoring participation (student) | unresolved | unresolved | **7 targets** (1996, 2010 by stage) | unresolved | unresolved | unresolved |
| Tutoring (parent-level) | — | — | 1 check | — | — | — |
| Primary completion | target (to 2024) | target (to 2023) | **none in UIS** | target (to 2020) | target (2012 only) | **none in UIS** |
| Lower-sec completion | target (to 2024) | target (to 2021) | none in UIS | target (to 2020) | target (to 2023) | none in UIS |
| Upper-sec completion | target (to 2024) | target (to 2023) | none in UIS | target (to 2020) | target (to 2023) | none in UIS |
| Out-of-school rate (primary age) | target (to 2025) | target (to 2025) | target (to 2025) | target (**1997 — stale**) | target (to 2024) | target (to 2024) |
| Transition to tertiary | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved |
| Repetition / dropout | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved |
| Formal/informal employment | unresolved | **target 2019** (11.7% formal / 88.3% informal) | unresolved | unresolved | unresolved | unresolved |
| Degree-holding employed share | unresolved | **target 2019** (6.6%) | 27.6% degree stock (2025) | unresolved | unresolved | unresolved |
| Tertiary attainment stock | — | — | **target 36.4%** (post-secondary, 2025) | — | — | — |
| Wage premium by education | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved |
| GDP p.c. (PPP) | 2024 | 2024 | 2024 | 2024 | 2024 | 2024 |
| Sector employment | 2024 | 2024 | 2024 | 2024 | 2024 | 2024 |
| Status employment (wage/vulnerable) | 2024 | 2024 | 2024 | 2024 | 2024 | 2024 |
| Urbanisation / remittances | 2024 | 2024 | 2024 | 2024 | 2024 | 2024 |
| Overseas deployment | **unresolved** | unresolved | unresolved | unresolved | unresolved | unresolved |

## What a model can be calibrated to (the `target` rows)

**Cohort flows (UIS SDG4 release 2026-11, observed years only).** Completion is the share of the population 3–5 years above graduation age that has completed the level — a cohort *attainment* measure, not an enrolment rate.

| Country | Primary completion | Lower-sec completion | Upper-sec completion |
|---|---|---|---|
| Philippines | 98.3 (2024) | 92.4 (2024) | 75.0 (2024) |
| Cambodia | 84.6 (2023) | 56.0 (2021) | 27.9 (2023) |
| China | 99.2 (2020) | 95.7 (2020) | 87.5 (2020) |
| Rep. of Korea | 100.0 (2012) | 100.0 (2023) | 99.5 (2023) |
| Hong Kong, Japan | — | — | — (not reported to UIS) |

**Out-of-school (primary age, latest observed):** PHL 12.8% (2025), KHM 11.9% (2025), HKG 1.3% (2025), KOR 0.1% (2024), JPN 0.1% (2024), CHN 6.7% (**1997 — do not use as a contemporary target**).

**Cambodia 2019 (CLFS, one-off survey — record as such):** formal employment 11.7% of employed persons; informal 88.3%; university-degree holders 6.6% of employed persons (urban 13.8%, rural 2.9%); upper-secondary attainment 15.7%.

**Hong Kong stock (EDB, 2025):** 36.4% of population 15+ has post-secondary attainment (degree course 27.6% alone).

**Shadow education (HK only):** senior secondary 85%, middle secondary 82%, lower secondary 72% (2010 survey); primary 45%, lower 26%, middle 34%, senior 40% (1996 HKFYG). All are one-off, non-probability surveys and the reporting authors say they are *not statistically robust* — calibrate softly or use as bounds, not point targets.

**Economy (WDI, annual 1995–2024):** GDP p.c. PPP 2024 — HKG 75,342; KOR 61,051; JPN 54,156; CHN 27,140; PHL 11,814; KHM 7,982. Wage-and-salaried share 2024 — HKG 92.2, JPN 90.8, KOR 77.1, PHL 63.5, CHN 61.9, KHM 44.2. Vulnerable employment 2024 — KHM 52.6, PHL 33.9, CHN 33.8, KOR 17.9, JPN 7.6, HKG 5.8. Remittances 2024 — PHL 8.7% of GDP, KHM 6.1%, all others ≤0.4%.

## What is a check, not a target

1. **Gross intake ratios (AIR.1, AIR.2).** New entrants in a grade ÷ population of official entry age. They are *throughput proxies*, not transition rates, and can exceed 100%. Do not calibrate a transition parameter to them.
2. **HK parent-level tutoring (58%).** Parent share who paid for tutoring (press-reported HKU study) is not student participation.
3. **Wage-and-salaried share.** A status-of-employment measure. It is **not** formality: a salaried worker can be informal, and a self-employed worker can be registered. Do not treat it as "formal share".
4. **Out-of-school rate.** Complements of enrolment, not dropouts; the household-survey and administrative versions differ (`ROFST.*.CP` vs `ROFST.H.*` in the source data).

## What is unusable (and why)

| Missing target | Blocker | What would fix it |
|---|---|---|
| Tutoring participation, all countries except HK | no probability survey retrieved; CFPS/CEPS (CHN), KEDI survey (KOR), APIS/FIES (PHL) inaccessible or not machine-readable here | obtain KEDI Private Education Expenditure Survey tables (Korea, annual by school level), CFPS/CEPS extracts, a PH household survey with tutoring items |
| Transition to tertiary, repetition, dropout | not in UIS SDG4 bulk; UIS core education dataset is API-key only | UIS API subscription, or national EMIS series |
| Formal employment share, all but Cambodia | ILOSTAT returned HTTP 403; no WDI informality series | ILOSTAT bulk/API, or national LFS tabulations |
| Wage premium by education | no earnings microdata retrieved | LFS/FIES microdata, ILOSTAT earnings |
| Overseas deployment (PH OFW/nurses) | PSA blocked (403); DMW not machine-readable in this pass | DMW/POEA deployment tables, or PSA Survey on Overseas Filipinos |
| HKG/JPN completion | these systems do not report UIS completion rates | HKEAA/EDB (HK), MEXT (Japan) cohort data |

## Five traps the model is most likely to hit

1. **Completion ≠ enrolment.** Philippines upper-secondary completion is 75.0% (2024) while its gross *secondary* enrolment ratio is ~85–92%. Calibrating a completion flow to an enrolment ratio will overstate throughput. And WDI's `SE.SEC.CMPT.LO.ZS` is a **gross intake ratio** (PHL 97.4 in 2022), not the UIS completion rate (84.2) — the two live in the same WDI file.
2. **Hong Kong tutorials are not a flat 85%.** 85% is *senior secondary* in a 2010 survey; the same survey gives 72% lower secondary, and 1996 gives 40% senior / 26% lower. A single-HK-parameter model will mis-state the stage gradient that drives when demand starts.
3. **Cambodia's 6.6% is a share of *employed persons*, not of jobs, and 88.3% is informality, not "non-graduates".** The same survey has 1.2% unemployment including 1.2% for graduates — a labour market where the degree is scarce is not a labour market where the degree is required.
4. **"Wage employment" is not "formal employment".** Korea's wage-and-salaried share is 77.1% and Cambodia's 44.2%, but that tells you about contracts, not registration or benefits. Korea's vulnerable-employment share (17.9%) and Cambodia's (52.6%) are the better status-gradient variables; neither is informality.
5. **Three of the six can't be calibrated on completion or on pre-2013 Japan/Korea enrolment.** HKG and JPN have no UIS completion series at all; Japan's level enrolment ratios exist in the current vintage only for 2013–2023, Korea's only from 2000. Any cross-country calibration that silently drops or fills these will fit the four well-measured systems and then generalise wrongly.

## Reproduction and provenance

- `TARGETS_FLOW.csv` rows labelled UIS are lifted **observed-only** from `data/gmr_observed_6countries_1970_2024.csv` (which carries the source layer per value); `CR.MOD.*` modelled series are excluded by construction.
- `ECONOMY_SERIES.csv` is built from live WDI API pulls in `raw/worldbank_economy/` (23 indicator files + per-indicator metadata files used for the `definition` column), accessed 2026-11-20.
- `TARGETS_SHADOW.csv` is built from the archived IIAS article in `gmr_snapshots`/`raw/hongkong/bray_iias_hk.pdf` (Kwo & Bray 2011, p.20); the quoted caveat is on that page.
- Longer provenance, including blockers, is in `DATA_LEDGER.md`, `retrieval_log.md` and `SOURCES.json`.
