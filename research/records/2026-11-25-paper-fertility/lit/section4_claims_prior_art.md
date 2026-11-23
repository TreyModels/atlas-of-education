# Paper F section draft — the DHS ecological schooling–fertility gradient

**Prepared for un-data (Paper F integration) by panel-matrix, 25 November 2026.**
**Source record: `research/dhs-micro-2026-11-23` @ `31ded00`** (pre-registration first commit `283e34c`).
All numbers below are from `research/records/2026-11-23-dhs-micro/results/model_summary.txt` and the JSON files
in the same `results/` folder; field names are given so the Paper F claims-to-source map can be built.

## (1) The question
Do women with more schooling have fewer children when the comparison is made **within** a country and survey —
the canonical relationship the demographic literature rests on — and does the size of that gradient behave the
way the theory says (a cohort/generational phenomenon; steeper where the schooling pipeline is denser; not
merely an income gradient; quantum rather than only tempo)? The previous project tested only country-year
matrices, where the relationship is a between-country development gradient; this section asks whether the
individual-level relationship is visible in the best published DHS data that could be obtained in this session.

## (2) Data and sample
The paper's public API was used to obtain every published DHS cell that reports completed fertility, age at
first birth and attainment by education, wealth, residence and age: **81,962 cells across 377 surveys, 87
countries, 1985–2025**. The unit of observation is a **published cell** (country × survey × education, or
wealth/residence), not a woman. The main model sample is **1,291 education cells from 369 surveys and 86
countries, median 401 women per cell**. Models are weighted by the published number of women per cell, include
**country × survey fixed effects**, and cluster standard errors by country. The outcome is mean children ever
born to women aged **40–49** (completed fertility; the age range is set by DHS, so timing truncation of younger
women is not an issue). The schooling variable is the published education level (no education, primary,
secondary, higher), with no education as the reference.

## (3) Every number, with uncertainty, sample and recording path

**The gradient (completed fertility, women 40–49; country × survey fixed effects).**
Primary **−0.570 children (SE 0.058)**; secondary **−1.622 (SE 0.170)**; higher **−2.536 (SE 0.235)**; n=1,291
cells, 369 surveys, 86 countries. Source: `results/model_summary.txt`, section A; fields `edu_primary`,
`edu_secondary`, `edu_higher` in `results/model_education.json`.

**Per-survey robustness.** The secondary+ minus none/primary gradient is **negative in 99% of 346 surveys**;
median **−1.900** (interquartile range −2.475 to −1.425); 346 surveys, 80 countries. Source:
`results/model_summary.txt`, section B; `results/survey_gradients.csv` (column `gradient`).

**Cohort attenuation — the theory's cohort prediction is contradicted.** The gradient does **not** steepen in
later cohorts: the interaction is **+0.262 (SE 0.127)** children per decade for secondary and **+0.396 (SE
0.161)** for higher, i.e. the gradient becomes *less* negative over time. Early-cohort (birth ≤1964) vs
late-cohort secondary gradient: **−1.959 (SE 0.181)** vs **−1.499 (SE 0.164)**; higher: **−2.989 (SE 0.203)** vs
**−2.347 (SE 0.242)**. Cohort-specific median survey gradients: 1940s **−2.50** (48 surveys), 1950s **−1.90**
(78), 1960s **−1.85** (122), 1970s **−1.80** (95), 1980s **−1.50** (3). Source: `results/model_summary.txt`,
section C; `results/cohort_gradients.csv` (columns `cohort`, `median_gradient`, `n_surveys`).

**Pipeline attenuation — the theory's pipeline prediction is contradicted.** The gradient is **shallower**
where the schooling pipeline is denser: interaction **+0.130 (SE 0.050)** children per +10 percentage points of
women with secondary+ for secondary education and **+0.162 (SE 0.053)** for higher. Per-survey gradients by
pipeline tercile: low **−2.10** (108 surveys), middle **−2.00** (108), high **−1.60** (108); pipeline = share of
women 15–49 with secondary+, built from the survey's own age breakdown weighted by women (348 surveys; range
2–100%, median 34%). Source: `results/model_summary.txt`, section D and F3.

**Tempo (median age at first birth, women 25–29; same fixed effects).** Secondary **+2.648 years (SE 0.149)**;
higher **+5.272 (SE 0.389)**; primary +0.535 (SE 0.095); 996 cells, 333 surveys, 86 countries. Source:
`results/model_summary.txt`, section F; `results/model_age_first_birth.json`.

**Wealth gradient (for comparison, not a horse race).** Highest vs lowest wealth quintile **−1.993 children
(SE 0.159)**; middle vs lowest **−0.875 (SE 0.083)**; 1,585 cells, 317 surveys, 77 countries. The DHS API does
not cross education with wealth, so "education survives wealth" **cannot be tested with published cells**;
source: `results/model_summary.txt`, section E; `results/model_wealth.json`.

**Data-quality checks.** Mean children ever born by age rises **0.18, 1.05, 2.26, 3.45, 4.54, 5.32, 5.77**
across the seven five-year age groups 15–19 to 45–49 — the extract behaves as a real fertility series. Source:
`results/model_summary.txt`, section G.

## (4) What is new here vs replicated
**Replicated:** the negative schooling–fertility association itself is one of the most replicated findings in
demography (see prior works below); the completed-fertility age pattern; the general finding that higher
education is associated with substantially fewer births.
**New in this assembly:** (i) the gradient is estimated on the **published DHS cells** in a common
country×survey fixed-effects framework — a cell-level (ecological) version rather than the individual-level
estimates of the micro literature; (ii) the **cohort and pipeline attenuation** results are reported as a
**contradiction** of the theory's steepening predictions rather than as a confirmation; (iii) the
**individual-microdata gap is documented** rather than papered over (next section). No claim of precedence is
made; the individual-level association is not new.

## (5) Closest prior works (DOI and Crossref status checked 25 Nov 2026)
- Ainsworth, Beegle & Nyamete (1996), *World Bank Economic Review* 10(1):85–122. DOI 10.1093/wber/10.1.85 —
  **Crossref ✓ MATCH**. Fourteen sub-Saharan African countries; women's schooling and fertility/contraception.
  Our ecological gradient is consistent with it; the contribution here is the 87-country DHS cell assembly.
- Breierova & Duflo (2004), NBER Working Paper 10513. DOI 10.3386/w10513 — **Crossref ✓ MATCH**. Education and
  fertility/child mortality, fathers vs mothers; the individual-level question our cell data cannot answer.
- Duflo (2012), *Journal of Economic Literature* 50(4):1051–1079. DOI 10.1257/jel.50.4.1051 —
  **Crossref ✓ MATCH**. Women's empowerment and development; frames why fertility is a core outcome.
- Psacharopoulos & Patrinos (2018), *Education Economics* 26(5). DOI 10.1596/30154 (World Bank working-paper
  version) — **Crossref ✓ MATCH**. Returns to schooling; the demand-side mechanism that the gradient is often
  read through.
- Baird, McIntosh & Özler (2011), *Quarterly Journal of Economics* 126(4):1709–1753. DOI 10.1093/qje/qjr032 —
  **Crossref ✓ MATCH**. Cash vs conditionality and fertility; experimental evidence that schooling/transfer
  design can move fertility, not the gradient itself.
- Chicoine (2021), *World Bank Economic Review*, free primary education and fertility in Ethiopia.
  DOI 10.1596/1813-9450-9105 (World Bank working-paper version) — **Crossref ✓ MATCH**. A supply-side schooling
  expansion with fertility effects; complements the gradient evidence.
- Barro & Lee (2013), *Journal of Development Economics* 104:184–198. DOI 10.3386/w15902 (NBER working-paper
  version) — **Crossref WEAK** (year/journal of the published version not confirmed in-session). Attainment
  data; not a fertility study, included for the attainment measure.
- Rutstein & Johnson (2004), *The DHS Wealth Index*, DHS Comparative Reports No. 6 — **no Crossref DOI**
  (report). Source of the wealth-quintile measure used in the comparison above.
- Osili & Long (2008), "Does female schooling reduce fertility? Evidence from Nigeria", *Journal of Development
  Economics* 87(1):57–75 — **not returned by Crossref in-session** (bibliographic details unverified); included
  only as a standard individual-level reference, not as a verified DOI.

## (6) The honest caveat — this is an ecological gradient, not the individual-level test
**DHS individual-level microdata were not obtainable in this session.** The public API exposes indicator
aggregates and a file inventory but no download link; the flat files sit behind a registered DHS account. The
documented attempts are in `research/records/2026-11-23-dhs-micro/data/microdata_probe.txt`: indicator API 200;
dataset-metadata API 200 (15,518 file records, of which **2,005 are Individual Recode files for 85 countries**,
e.g. `AFIR71DT.ZIP`); direct flat-file URLs 404; dataset landing page login-gated; IPUMS-DHS API 403; Zenodo 403;
Harvard Dataverse has no DHS recodes; `/root/work/local_data` contains no DHS microdata. The manual route is
specified (free DHS account, dataset access request, Individual Recode Stata files; variables for education
level, years of schooling, children ever born, age, residence, wealth, region, weights and cluster).
**Therefore the numbers above are a survey-level ecological gradient, not the individual-level relationship.**
They cannot control for woman-level covariates, cannot separate composition from effect, and the cohort and
pipeline attenuation results are especially vulnerable to the changing composition of the education categories
over time (secondary education is an elite category in early cohorts and mass education later). The individual
test, the wealth horse race, the quantum-vs-tempo decomposition and the community placebo remain **undone** for
lack of microdata. Paper F should present this section as the best available **ecological** evidence and state
the gap plainly; it must not be cited as individual-level evidence.

**One flag:** the task text provided to this section matches our record (primary −0.57, secondary −1.62, higher
−2.54; 99% of 346 surveys negative; cohort attenuation 1940s −2.50 to 1970s −1.80; pipeline attenuation
contradicted). No discrepancies to report.
