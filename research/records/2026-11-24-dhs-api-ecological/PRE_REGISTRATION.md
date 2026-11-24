# PRE-REGISTRATION — ecological schooling→fertility panel from the DHS public API (all countries, all rounds)

**Commit this file before pulling any indicator values and before estimating anything.** It was written on
2026-11-24 after a **metadata-only availability audit** (category/label fields only, `Value` never requested);
that audit is cached as [`data/indicator_availability.json`](data/indicator_availability.json) and
[`data/indicator_catalogue.json`](data/indicator_catalogue.json). No cell value was read before this commit,
no model was estimated, and the indicator list below is fixed here.
**Branch:** `research/dhs-api-ecological-2026-11-24` (base `origin/research/handoff-2026-11-24 @ 9242214`).
**Task:** task-16. **Owner:** dhs-scout. **Record:** `research/records/2026-11-24-dhs-api-ecological/`.
**Supersedes nothing:** the earlier ecological attempt (`research/dhs-micro-2026-11-23 @ 31ded00`, 81,962 cells,
377 surveys, 87 countries, weighted country×survey FE) is **extended**, not duplicated — see §1.
**Data tier for every number produced under this document: OBSERVED (published DHS aggregates) / ECOLOGICAL.**
No reconstructed or imputed values, no synthetic data, no gated microdata.

---

## 1. What is already known, and what this adds

From the committed prior record (`research/dhs-micro-2026-11-23 @ 31ded00`), quoted not recomputed here:
81,962 published cells, 377 surveys, 87 countries, 1985–2025; within country×survey, completed fertility
(women 40–49) falls with schooling — primary **−0.57 (SE 0.06)**, secondary **−1.62 (0.17)**, higher
**−2.54 (0.24)** children relative to no education (n = 1,291 cells, 86 countries); the per-survey
secondary+ gradient is negative in **99% of 346 surveys**, median **−1.90**; cohort interaction **+0.26
(0.13)** (attenuation, contradicting the pre-registered steepening); pipeline-density interaction **+0.13
(0.05)** (shallower where massified). Those are the numbers this document must reproduce before it extends.

**This job adds, pre-declared now:**

- **A period-births measure by education** (`FE_FRTR_W_TFR`, TFR 15–49) — the API does expose it by education,
  which the prior attempt did not use. This makes the construct contrast about *period births* possible.
- **A desired-fertility measure by education** (`PR_WTFR_W_WFR`, wanted TFR) and a stated-preference measure
  (`PR_DESL_W_WNM`, % wanting no more children) — new.
- **A surviving-children construct**, but only at the **survey level** (see §2.3 — the API does *not* publish it
  by education, and we will not fake a proxy).
- **A country-FE + period-FE specification** alongside the saturated country×survey FE, and a
  **cohort-proxy** specification.

---

## 2. Data (fixed now)

### 2.1 Source and scope

- **Source:** `api.dhsprogram.com`, public endpoints, **no key, no login** (verified 2026-11-24; see
  `ACQUISITION_PLAN.md` on branch `research/dhs-acquisition-2026-11-24` for the probe log).
- **Scope:** **all countries and all survey rounds the API publishes** for each indicator with an
  `Education` (4 categories) or `Education (2 groups)` breakdown. No country restriction, no year restriction.
  This is deliberate: the task asks whether the association holds "across all publicly available DHS
  surveys/rounds", and restricting the universe would be a selection decision that must not be made after
  seeing results.
- **Unit of observation:** the DHS-published **cell** = country × survey round × education category. This is
  an **ecological** unit: it is an average over women, not a woman.
- **Cached data:** every raw JSON page pulled is stored under `data/raw/` (one file per indicator, plus
  surveys/countries metadata). The analysis reads only from the cache; the cache's sha256s are in
  `data/MANIFEST.sha256`.

### 2.2 Cell-level indicators (education breakdown available — audited)

| # | Indicator | API label | Construct | Role |
|---|---|---|---|---|
| **A** | `FE_FRTY_W_MNC` | Completed fertility of women age 40–49 | **Cumulative births** (mean children ever born, cohort-type) | Primary outcome: replication + extension |
| **B** | `FE_FRTR_W_TFR` | Total fertility rate 15–49 | **Period births** (DHS TFR) | Construct/window contrast (births, period) |
| **C** | `PR_WTFR_W_WFR` | Total wanted fertility rate | **Period desired births** | Desired-fertility contrast |
| **D** | `PR_DESL_W_WNM` | Women who want no more children | **Stated fertility preference** | Desired-fertility robustness |
| **E** | `FE_AAFB_W_M25` | Median age at first birth, women 25–29 | **Tempo** | Mechanism descriptor (delay) |
| **F** | `FE_FRTR_W_GFR` | General fertility rate | Period births, different denominator | Robustness for B |

**Audited availability (metadata only, 2026-11-24):** A, B, C, D, E, F each return
`Education` = {No education, Primary, Secondary, Higher} and `Education (2 groups)` =
{No education or primary, Secondary or higher}. Their record counts are 9,283 / 9,403 / 8,168 / 61,976 /
7,844 / 9,403 respectively (all background characteristics combined, including Region). The Region category is
here a *breakdown*, not a control, and is not used at cell level (regions are nested in country and their
definitions change across rounds).

### 2.3 Survey-level indicators (no education breakdown — that is the finding, not a gap to paper over)

| # | Indicator | API label | Construct |
|---|---|---|---|
| **G** | `FE_CEBA_W_MNC` | Mean number of children ever born | Cumulative births by age group (15–19 … 55–59) |
| **H** | `FE_CEBA_W_MND` | Mean number of children died | **Cumulative child deaths** by age group |

**Surviving-children measure:** mean surviving children = **mean CEB − mean children died** (indicators G − H).
This is not a proxy: at the individual level `v201 − v206 − v207` *is* the definition of surviving children
(DHS Recode Manual; `ACQUISITION_PLAN.md` §4), so at aggregate level the difference of the two published means
is the mean of the surviving-children variable, for the same population and survey. It is a subtraction of two
observed quantities of the same women, not an imputation.
**But it can only be computed for the population the API publishes it for — the age groups — not by education.**
Therefore:
- The **births-vs-surviving construct contrast** (question b) is estimated at the **survey level** (§4.3), for
  women 40–49 (combining the 40–44 and 45–49 age cells, weighted by their published denominators).
- The **education-gradient** contrast is estimated between the two **births-based** measures A (cumulative) and
  B (period) — both available by education — and **no surviving-children-by-education gradient is constructed**.
  If an analyser later wants it, it requires the individual microdata, i.e. exactly the blocked test.

### 2.4 Modifier variables (survey level, for heterogeneity only)

- `ED_EDUC_W_SEH` (women with secondary or higher) by 5-year age groups → **pipeline density** = the
  age-weighted share of women 15–49 with secondary+ in that round (weights = published denominators).
- Calendar year, survey type (DHS/MIS/AIS), country, region, and `NumberOfWomen` from the surveys endpoint.

### 2.5 What is excluded and why

- **No within-country×survey×education wealth or residence cross-tabs:** the API publishes education,
  residence and wealth as *separate* breakdowns, never crossed. An education gradient conditional on wealth is
  exactly the individual-level horse race the public cells cannot run — it is named as a limit, not approximated.
- **No derived or matched series** (no matching CEB to mortality rates, no interpolation, no reconstruction).
- **No MIS/AIS exclusion by default:** the API mixes survey types. The main specification pools whatever exists
  and a pre-declared robustness split by `SurveyType == "DHS"` is reported.
- **No model/synthetic datasets.**

---

## 3. Panel construction (fixed now)

- Education categories: **No education (ref), Primary, Secondary, Higher** (`Education` breakdown), plus the
  2-group breakdown {No education or primary (ref), Secondary or higher} as the **coverage-maximising** panel.
- A cell enters the **4-level panel** only if all four categories are present for that survey and have
  `Value` non-missing, `DenominatorUnweighted ≥ 20`, and the education labels are exactly those four.
- A cell enters the **2-group panel** on the same rule with its two labels.
- Weight: `DenominatorUnweighted` (women in the cell). Unweighted estimates reported alongside.
- Education is treated as **ordered categories**, not as a continuous dose in the main model (the API does not
  publish mean years *within* education categories); a linear-category version is reported as a sensitivity.
- Duplicates: `SurveyId` × education must be unique; exact duplicate records dropped and counted.
- Checks before estimation: (i) the published national value of each indicator matches the cell values when
  re-aggregated with denominators (tolerance 1%); (ii) education levels are exhaustive/ordered; (iii) no survey
  appears twice under two ids.

---

## 4. Specifications (fixed now — closed list, no searching)

Let *c* index cells, *j* country, *s* survey round, *e* education, *t* calendar year.

**Estimator:** weighted least squares, weight = unweighted women in cell; standard errors **clustered by
country** (the level at which the schooling system and the fertility regime vary); sensitivity: clustered by
survey, and unweighted. All coefficients reported per-SD of the outcome (across the estimation sample) and in
raw units.

### 4.1 Replication and extension (question 1)

| Model | Specification | Role |
|---|---|---|
| **M0** | Y = β_e Edu + **country FE** + **5-year period FE** | country FE + round FE (pre-declared headline for Q1) |
| **M1** | Y = β_e Edu + **country×survey FE** | saturated within-round estimate (the prior spec; replication anchor) |
| **M2** | M1 + `Edu × pipeline density` | does the gradient depend on how massified the system is (prior E3)? |
| **M3** | M1 but **2-group** education panel | coverage-maximised replication |
| **M4** | M1 restricted to `SurveyType == "DHS"` | survey-type robustness |
| **M5** | Y = β·Edu + **country FE** + **year FE** + country-specific linear trends | trend-robustness (the E11 lesson that country trends absorb much variation) |

Outcome for Q1: **A** (`FE_FRTY_W_MNC`). "Round" in M0 is the 5-year period of the survey year (1990–94 etc.),
not the survey id, so that country FE and round FE are both identified.

### 4.2 Age/period window (question 2a)

Pre-declared contrast: **completed fertility by education (A, cumulative, ages 40–49)** vs **period TFR by
education (B, ages 15–49)**. Both are births-based, so this isolates the **window** (cumulative vs period) and
the **age range** (40–49 vs 15–49), not the births-vs-surviving construct.
- Run the M1 and M0 specifications for B (and F as robustness) on their own education panels.
- Standardise both outcomes (per-SD within their own estimation samples) before comparing magnitudes.
- Report the **ratio** of the standardised secondary-vs-none coefficient `β_B / β_A` and its bootstrap CI
  (cluster bootstrap by country, 500 draws, fixed seed).

### 4.3 Construct contrast (question 2b)

**(b1) Cell level, births-based only.** Stack the A-cells and B-cells for the same country×survey×education,
standardise each outcome within indicator, and estimate:
```
Y_z = β1·Edu + β2·(indicator = B) + β3·(Edu × indicator B) + country×survey FE
```
cluster-robust by country. Report β3 and the A/B ratio of standardised gradients.
- **Desired-fertility limb:** same stacked design for **C** (wanted TFR) vs **B** (TFR), and for **D** vs a
  stated-preference baseline. This asks whether the schooling gradient is a *realisation* gradient (larger for
  actual births) or also a *preference* gradient (similar for wanted births).

**(b2) Survey level, births vs surviving children.** For each survey with G and H age-group cells, compute for
women 40–49:
`CEB40 = weighted mean of G(40-44), G(45-49)` and `Deaths40 = weighted mean of H(40-44), H(45-49)` with the
published unweighted denominators as weights; `Surviving40 = CEB40 − Deaths40`. Then:
- correlate `Surviving40` with `CEB40` and with the survey's **TFR** (B's "Total" national value), across
  surveys and within countries (levels and first-differences);
- report the distribution of `TFR − CEB40`, `TFR − Surviving40`, and `Surviving40 / TFR`;
- **no regression of Surviving40 on education is possible** (no education breakdown) and none is attempted.

### 4.4 Cohort-of-women comparison (if identifiable)

The 40–49 completed-fertility cells in a round with survey year *t* refer, on average, to a birth cohort near
*t − 44.5*. Using only the completed-fertility panel (A) and keeping the cross-section design, estimate
`Edu × cohort-proxy` in a model with country FE and cohort-proxy FE, where `cohort-proxy = year − 44.5` in
5-year bins. This is a **repeated-cross-section cohort proxy**, not a true panel of women; it is labelled as
such. Two-sided test; the prior ecological estimate (+0.26 per decade, attenuation) is the comparison point,
not an anchor.

### 4.5 Heterogeneity

- Per-survey 2-group gradient (secondary+ minus none/primary) distribution: median, IQR, share negative.
- Per-country pooled gradient; per-period gradient.
- BH adjustment within each heterogeneity family (surveys, countries, periods); report the count and the
  excluded share. **No "robust everywhere" claim** (Q3 finding: that label mislabels 87% of minority worlds).

---

## 5. Decision rules (fixed now)

**D1 — Replication.** The completed-fertility gradient is confirmed in these data if, in **M1** on the 4-level
panel with outcome A, β(secondary) < 0 **and** β(higher) < 0 with 95% CIs excluding 0, **and** the ordering is
monotone (Primary ≥ Secondary ≥ Higher), **and** the prior record's headline magnitudes are reproduced within
±0.15 children for secondary and ±0.25 for higher. If they are not reproduced, the prior numbers are flagged as
**not reproduced** and the new estimate is the reported one.

**D2 — Coverage/generality.** Report the share of surveys with a negative 2-group gradient. Pre-declared
thresholds: **"near-universal"** ≥ 90%; **"common but with a measurable minority"** 70–90%; **"not general"**
< 70%. The share is the finding; the label is fixed by these thresholds, not chosen after seeing the data.

**D3 — Window/construct agreement (Q2a, Q2b1).** For each contrast, pre-declared verdicts:
- **"same sign, similar magnitude"**: same sign and the standardised ratio in **[0.67, 1.5]** with a CI
  containing 1;
- **"same sign, materially different magnitude"**: same sign and the ratio outside that band or its CI
  excluding 1;
- **"sign disagreement"**: opposite signs with both CIs excluding 0.
The ratio is reported either way; the verdict names the finding, it does not rank the measures.

**D4 — Desired vs realised.** Pre-declared prediction: the standardised schooling gradient for **wanted** TFR is
smaller in magnitude than for **actual** TFR (`|β_C| < |β_B|`). If instead `|β_C| ≥ |β_B|`, this is reported as
**"the schooling gradient is at least as strong in preferences as in outcomes"** — a substantive result about
whether the pattern is about realised births or about stated demand.

**D5 — Construct gap at survey level (Q2b2).** Report the level correlation and median absolute difference
between `Surviving40` and TFR, and between `CEB40` and TFR, plus within-country change correlations. Pre-declared
statement: **these two measures answer different questions (surviving family size vs period births)**; a
difference is expected and is **not** a data error and **not** a correction of either series. We do **not**
attempt to reproduce E11's exact 0.3042 / 4.2677 / 0.541 / 1.555 numbers from a different data source; we report
the analogous DHS-based gap and say explicitly that it is a different pairing.

**D6 — Cohort proxy.** Two-sided. If the `Edu × cohort-proxy` interaction is positive and its CI excludes 0,
report **attenuation** (consistent with the prior ecological estimate and with composition); if negative and
excluding 0, report **steepening**, which would contradict the prior record; otherwise **indeterminate**.

**D7 — Nulls.** Any pre-declared coefficient whose 95% CI includes 0 is reported as a null with its interval,
not as a failure to find support. Intervals always accompany signs.

**Stopping rule.** The sample is every qualifying cell the API publishes at pull time — fixed by the rules in
§2–§3, not by results. No dropping of countries/rounds for results. If a pull fails or an indicator is absent,
it is reported and the affected analysis is dropped (never proxied).

**Deviations.** Any change after this commit is an amendment appended to `REPORT.md` with date and reason; the
affected numbers are labelled exploratory. This file is never edited.

---

## 6. Ecological-limits statement (binding on every downstream use, written in advance)

1. **The unit is a published cell, not a woman.** Every coefficient is an association between *group averages*.
   It cannot establish that an individual woman with more schooling has fewer children; it is consistent with
   that, and with composition, selection, and district-level development gradients.
2. **No causal language.** No instrument, no policy discontinuity, no pre-trends, no within-woman variation.
   "Schooling is associated with lower completed fertility in the published cells" is the strongest sentence
   this design supports.
3. **Aggregation bias is not hypothetical here.** The cells differ in their education composition *and* in
   everything correlated with education (residence, wealth, region, cohort). The API never crosses education
   with wealth or residence, so the education gradient cannot be separated from those gradients in these data.
4. **Education categories change meaning across rounds** (massification: "secondary" is an elite label early,
   a mass label late). A stable coefficient across rounds does not mean a stable individual effect.
5. **The API's published cells are already DHS-weighted** (the values are survey-weighted estimates); the cell
   weights used here are *unweighted denominators* and only re-weight cells, not women.
6. **Cross-sectional, repeated rounds**: one observation per country×round; no panel of women; the cohort proxy
   is derived from survey years, not followed women.
7. **This cannot substitute for the individual-level test.** The Individual Recode test (blocked on DHS
   approval; `research/dhs-acquisition-2026-11-24`) is the only design in this programme that puts a woman's own
   schooling next to her own children ever born. Nothing here replaces it, and no simulation or synthetic data
   is used anywhere.
8. **Construct naming.** `FE_FRTY_W_MNC` is a **cumulative births** measure (mean children ever born for women
   40–49), **not a TFR**. `FE_CEBA_W_MNC − FE_CEBA_W_MND` is a **surviving-children** measure, **not a TFR**.
   Only `FE_FRTR_W_TFR` / `PR_WTFR_W_WFR` are rates. Every table names the construct in its header.

---

## 7. Expected results (recorded now so the record can score itself)

| # | Prediction | Confidence | If wrong |
|---|---|---|---|
| P1 | β(secondary) < 0 and β(higher) < 0 for completed fertility, monotone in education | high | report reversal, check merge/units first, then report |
| P2 | The 2-group gradient is negative in ≥ 90% of surveys (prior found 99%) | high | report the lower share; it is the finding |
| P3 | Period TFR by education shows the same sign and a similar standardised magnitude as completed fertility (ratio in [0.67, 1.5]) | medium | a material gap is a window finding worth reporting |
| P4 | Wanted TFR gradient is negative but **smaller** than actual TFR | medium | report the opposite as a preferences finding |
| P5 | Surviving-children and period-TFR levels differ materially at survey level (construct gap), and their rank correlation is high | medium-high | report exactly what is found |
| P6 | The cohort-proxy interaction is positive (attenuation), as in the prior record | medium | report steepening if found; the individual test would then be needed to separate composition |

---

## 8. Deliverables

- `data/raw/*.json` (cached API pages), `data/MANIFEST.sha256`, `data/indicator_availability.json`,
  `data/indicator_catalogue.json`.
- `scripts/pull_dhs_api.py` (pull + cache), `scripts/build_panel.py` (checks + panel), `scripts/estimate.py`
  (M0–M5, contrasts, heterogeneity; prints a machine-readable `results/results.json`).
- `results/` CSVs + `REPORT.md` (headline numbers, D1–D7 verdicts, heterogeneity shares, limits, and the
  explicit statement that this is OBSERVED/ECOLOGICAL and cannot substitute for the individual test).
- Every number in `REPORT.md` carries its file + field locator; unverified or non-reproduced items are marked.

---

## 9. Sign-off

Written by **dhs-scout** for **task-16**, 2026-11-24, **before any indicator value was pulled and before any
estimate was computed**. The only prior DHS knowledge used is the committed prior record and the metadata
catalogue. If the analysis contradicts this document, the document wins and the contradiction is reported.
