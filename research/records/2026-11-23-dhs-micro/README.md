# DHS women's schooling and children ever born, 23 Nov 2026

Branch `research/dhs-micro-2026-11-23`. Pre-registration committed **before any data or code** (`283e34c`,
`PRE_REGISTRATION.md`: E1 canonical gradient, E2 cohort steepening, E3 pipeline-density steepening, E4 wealth
survival, E5 quantum-vs-tempo, E6 urban/rural + community placebo, plus the falsifiers). Server box2,
`/root/work/dhs`. This record reports what was obtained, what was not, and only the claims each supports.

## The individual-level test could NOT be run — data gap stated first
The pre-registered design was individual-level DHS microdata. **DHS women's Individual Recode files are not
publicly downloadable:** the public API exposes indicator aggregates and a file *inventory* but no download
link, and the flat files sit behind a registered DHS account. Every attempt is logged in
`data/microdata_probe.txt`; in short: indicator API 200; dataset-metadata API 200 (15,518 file records, of
which **2,005 are Individual Recode files for 85 countries**, e.g. `AFIR71DT.ZIP`); direct flat-file URLs
(`/data/dataset/AFIR66FL.ZIP`, `/data/AFIR66FL.ZIP`) 404; the dataset landing page 200 but login-gated;
IPUMS-DHS API 403 (key required); Zenodo search 403; Harvard Dataverse has no DHS recodes; `/root/work/local_data`
(checked: 04_data, 09_relations, 10_massification) contains **no DHS microdata**. So the canonical
individual-level test is **not done here** and no country-aggregate number below is offered as a substitute
for it. Manual download needs: a free DHS account and dataset-access request, then the Individual Recode Stata
files (education level, years of schooling, children ever born, age, residence, wealth quintile, region,
weights, cluster — DHS codes v106/v133/v201/v012/v025/v190/v024/v005/v021).

## What was obtainable, and what it is (and is not)
DHS public API indicator extracts: **81,962 published cells, 377 surveys, 87 countries, 1985–2025** — mean
children ever born to women aged 40–49 by education, median age at first birth by education, wealth and
residence breakdowns, and children ever born by age. Unit = country x survey x education **cell**, not a
woman. Models are weighted (weight = number of women in the cell) with country x survey fixed effects and
standard errors clustered by country; 1,291 education cells, 369 surveys, 86 countries, median 401 women per
cell. These are **ecological** associations; they cannot carry individual-level causal claims.
Local data: `/root/work/local_data/10_massification/data/UNIVERSALIZATION_SERIES.csv` and
`UNIVERSALIZATION_TIMING.csv` were checked (pipeline/enrolment series by country-year, no DHS records);
they were not needed because the DHS survey itself publishes women's attainment, which is the pipeline
measure used below. Everything else was downloaded from `api.dhsprogram.com` (DHS Program public API).

## (1) Fertility
**E1 (canonical gradient): confirmed, and it is large.** Within country x survey, completed fertility falls
monotonically with schooling: primary **-0.57 children (SE 0.06)**, secondary **-1.62 (0.17)**, higher
**-2.54 (0.24)** relative to no education (n=1,291 cells, 86 countries). The per-survey gradient (secondary+
minus none/primary) is negative in **99% of 346 surveys**, median **-1.90 (IQR -2.48 to -1.43)**. The
pre-registered falsifier — no gradient within country/survey — fails to appear.
**E2 (cohort steepening): contradicted in these data.** The gradient is *less* steep in later cohorts:
the secondary interaction is **+0.26 (0.13) children per decade** and higher **+0.40 (0.16)**. Cohort-specific
median survey gradients: 1940s **-2.50** (48 surveys), 1950s **-1.90** (78), 1960s **-1.85** (122),
1970s **-1.80** (95), 1980s **-1.50** (3). The most likely reading is composition: "secondary education" is a
small elite in early cohorts and mass schooling later, so the same label spans very different attainment.
Cell data cannot separate this from a genuine change in the effect — the individual microdata would.
**E5 (quantum vs tempo): both are present and cannot be separated here.** Same model: secondary education
moves median age at first birth **+2.65 years (0.15)** and higher **+5.27 (0.39)**, while completed fertility
falls 1.62 and 2.54 children. That is a large delay *and* a lower final number; distinguishing tempo from
quantum needs individual birth histories. 996 cells, 333 surveys, 86 countries.
**E4 (not just wealth): not testable with published cells.** The API does not cross education with wealth.
The wealth gradient on the same outcome is large — highest vs lowest quintile **-1.99 children (0.16)**
(1,585 cells, 317 surveys, 77 countries), comparable in size to the secondary-education gradient. Whether
education survives a wealth control is exactly what the individual data would settle; it is not claimed here.

## (2) Massification
**E3 (steeper where the pipeline is denser): contradicted in these data.** The education gradient is
*shallower* where female schooling is more massified: interaction **+0.13 (0.05)** children per +10 percentage
points of women with secondary+ for secondary education and **+0.16 (0.05)** for higher. Per-survey gradients by
pipeline tercile: low **-2.10** (108 surveys), middle **-2.00** (108), high **-1.60** (108). The same
composition caveat applies (mass education is less selected, so the label's margin shrinks). The gradient is
negative in **every** pipeline tercile — the direction is universal, the size is not.
The pipeline measure is the survey's own share of women aged 15–49 with secondary or higher, built from the
age breakdown weighted by women per age group (348 surveys; range 2–100%, median 34%).
This is a within-country association across education systems; it does **not** confirm or overturn the
between-country development gradient that task-15 found (those are different margins).

## Tests designed to kill these results
- **Falsifier 1 (no gradient / positive):** run — 99% of survey gradients are negative; not triggered.
- **Falsifier 2 (gradient vanishes once wealth is controlled):** cannot be run on published cells (no
  education x wealth cross-tab). Reported as a data gap, not as a pass.
- **Falsifier 3 (no cohort or pipeline variation):** run — variation exists, but in the opposite direction to
  the pre-registered expectation (attenuation, not steepening). Reported as a contradiction, not re-spun.
- **Placebo (community/other-people's schooling; E6 urban vs rural):** not testable from univariate published
  breakdowns — needs microdata linking a woman to her community and to her own schooling. Not claimed.
- **Sanity check:** mean children ever born by age rises 0.18 (15–19), 1.05, 2.26, 3.45, 4.54, 5.32,
  5.77 (45–49) — the extract behaves as a real fertility series; using women 40–49 avoids the timing
  truncation that affects younger women.
- **Selection caveats:** DHS covers women 15–49 and its samples are weighted, clustered and country-specific;
  completed fertility at 40–49 reflects survivorship, marriage and recall; the education categories change
  meaning across cohorts and systems; all estimates here are cell-level.

## Honest verdict
At the level actually observed — countries, surveys and education groups — the canonical negative
schooling–fertility gradient is **large, monotone and almost universal** in DHS data. But the two dynamic
predictions the project wanted (gradient steepens in later cohorts; steepens where the pipeline is denser)
are **contradicted** in the published cells, and the crucial individual-level test, the wealth horse-race and
the quantum/tempo decomposition **remain undone** because DHS microdata are not obtainable without an account.

## Files, provenance, throughput
`scripts/pull_dhs.py` (API pull, 81,962 rows; raw 10 MB extract stays on box2 at
`/root/work/dhs/data/dhs_extract.csv`), `analyse_dhs.py`, `probe_microdata.py`, `probe_datasets.py`;
`results/model_summary.txt`, `model_education.json`, `model_wealth.json`, `model_age_first_birth.json`,
`extract_completed_fertility_education.csv`, `extract_age_first_birth_education.csv`,
`survey_gradients.csv`, `cohort_gradients.csv`; `data/microdata_probe.txt`, `dhs_individual_files.csv`,
`pull_log.txt`. Throughput: API pull ~6 min wall, network-bound (box CPU idle in that phase, as expected);
all seven weighted fixed-effects models plus per-survey gradients in **10 s wall / ~9 CPU-seconds on one
core** — this job is light, the 3-core allowance was not needed.
