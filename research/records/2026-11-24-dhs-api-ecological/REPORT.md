# REPORT — schooling → fertility across **all** public DHS survey rounds (ecological, observed data)

**Status:** complete. Pre-registration committed **before any value was pulled** (`88073d0`); Amendment 01 and
the pull/panels committed **before any estimate** (`856c421`); estimates computed on **region-42** (not the Mac)
after Trey's no-Mac-compute instruction. Everything below is **OBSERVED / ECOLOGICAL**: the unit is a
DHS-published **country × survey × education cell**, not a woman. **No causal language is supported.** This
**cannot substitute** for the blocked Individual Recode test.
**Branch:** `research/dhs-api-ecological-2026-11-24` (base `origin/research/handoff-2026-11-24 @ 9242214`).
**Task:** task-16. **Owner:** dhs-scout.

---

## 1. Headline numbers (all OBSERVED, published-cell level)

| # | Result | Number |
|---|---|---|
| 1 | **Prior attempt reproduced exactly.** Completed fertility (women 40–49, mean CEB) on education, country×survey FE, weighted by women, clustered by country — same panel as `research/dhs-micro-2026-11-23 @ 31ded00` | primary **−0.554** (SE 0.058), secondary **−1.608** (0.166), higher **−2.520** (0.230); **1,291 cells, 86 countries** — deltas vs prior record (−0.57/−1.62/−2.54): **0.016 / 0.012 / 0.020** |
| 2 | **Gradient holds across all public rounds, with a minority.** Per-survey secondary+ gradient (2-group), 346 surveys | **98.8% negative**, median **−1.90** children (IQR −2.48 to −1.43), range −4.60 to +0.70; only 4/346 surveys non-negative |
| 3 | **Not a fixed-effects artefact.** Country FE + 5-year-period FE vs saturated country×survey FE vs country trends | M0 **−0.559 / −1.636 / −2.604**; M1 **−0.536 / −1.569 / −2.520**; M5 (+ country trends) **−0.553 / −1.584 / −2.536** (weighted, 4-level panel) |
| 4 | **Window contrast (Q2a): period TFR vs cumulative completed fertility gives the same gradient.** Standardised secondary-vs-none ratio β(TFR)/β(CEB40) | **1.017**, cluster-bootstrap 95% CI **[0.944, 1.102]** (65 common countries, 500 draws); 2-group version **0.960 [0.918, 1.002]** (80 countries) |
| 5 | **Construct contrast (b1): period-vs-cumulative births is null; desired-vs-actual is not.** Stacked, standardised, country×survey FE, clustered by country | A vs B interaction **−0.004 (SE 0.046, p=0.92)**; wanted-TFR vs actual-TFR interaction **−0.089 (0.024, p=0.00025)** — wanted-fertility gradient is *smaller* than the actual gradient |
| 6 | **Construct contrast (b2): the surviving-children measure and period TFR are different series.** 368 surveys, 87 countries, 1985–2025 | corr(surviving₄₀, TFR) **0.822**; corr(CEB₄₀, TFR) **0.899**; median \|TFR − surviving₄₀\| **0.6305**, max **2.681**; median \|TFR − CEB₄₀\| **1.009**, max **3.172**; within-country changes corr(Δsurviving, ΔTFR) **0.321** vs corr(ΔCEB, ΔTFR) **0.509** (65 countries) |
| 7 | **Cohort-proxy interaction: indeterminate.** Education × cohort-proxy (per decade) | secondary **−0.047 (0.245)**, higher **+0.077 (0.261)**, 2-group **+0.151 (0.135, p=0.26)** — direction matches the prior attenuation estimate, CIs include 0 |

**One-sentence reading:** in the published cells, more schooling goes with fewer children in essentially every
DHS round examined, the association is not an artefact of the FE choice or of country trends, and it is the
same whether fertility is measured as a **period TFR** or as **cumulative completed fertility** — but the
births-based measures and the surviving-children measure are **demonstrably different series**, and the
schooling gradient is **weaker in wanted fertility than in realised fertility**. All of this is an ecological
association; the individual-level test remains unrun.

---

## 2. Data and provenance

- **Source:** `api.dhsprogram.com`, public endpoints, **no key, no login, no gated file** (see
  [`data/source_log.txt`](../2026-11-24-dhs-acquisition/data/source_log.txt) for the probe log of the same API
  on the sibling branch). Raw pages are cached in [`data/raw/`](data/raw) with
  [`data/MANIFEST.sha256`](data/MANIFEST.sha256).
- **Unit:** country × survey round × background category (the DHS-published cell). Everything in this report is
  a property of published aggregates.
- **Indicators used** (exact API ids; the pre-registration fixed the list):

| id | label | construct | education breakdown? | denominators published? |
|---|---|---|---|---|
| `FE_FRTY_W_MNC` | Completed fertility of women 40–49 | cumulative **births** (mean CEB) | yes (4 levels / 2 groups) | **yes** |
| `FE_FRTR_W_TFR` | Total fertility rate 15–49 | **period births** (DHS TFR) | yes | **no** |
| `PR_WTFR_W_WFR` | Total wanted fertility rate | period **desired** births | yes | no |
| `PR_DESL_W_WNM` | Women who want no more children | stated preference | yes | yes |
| `FE_AAFB_W_M25` | Median age at first birth, women 25–29 | tempo | yes | no |
| `FE_FRTR_W_GFR` | General fertility rate | period births (robustness) | yes | no |
| `FE_CEBA_W_MNC` | Mean number of children ever born | cumulative births by age | **no (age only)** | yes |
| `FE_CEBA_W_MND` | Mean number of children died | child deaths by age | **no (age only)** | yes |
| `ED_EDUC_W_SEH` | Women with secondary+ | pipeline density (survey level) | — (age breakdown) | yes |

- **Coverage of the built panels:** completed fertility 4-level **860 cells / 215 surveys / 65 countries**
  (2-group: **692 cells / 346 surveys / 80 countries**); period TFR **1,296 / 324 / 77**; wanted TFR
  **1,244 / 311 / 82**; want-no-more **1,116 / 279 / 79**; survey-level panel **369 surveys / 87 countries,
  1985–2025**. The prior-specification panel is **1,291 cells / 369 surveys / 86 countries** — identical to the
  prior record's sample.
- **Checks run** ([`data/panel_checks.json`](data/panel_checks.json)): one row per survey × education (no
  duplicates — this caught and fixed a hidden second dimension in `PR_DESL_W_WNM`, see
  [`AMENDMENT_01.md`](AMENDMENT_01.md)); `DenominatorUnweighted ≥ 20` where published; weighted mean of the
  education cells vs the published national total (completed fertility: **max abs difference 0.079 children over
  215 surveys**; want-no-more: max 2.74 pp — universe/rounding differences, reported not hidden).

**What is *not* here:** no microdata, no individual records, no synthetic data, no reconstructed series, no
proxy denominator, no imputation. Rate indicators without published denominators enter **unweighted** models
(Amendment 01) — nothing is invented to weight them.

---

## 3. Q1 — does the ecological gradient hold across all public rounds?

Outcome: **mean children ever born to women 40–49** (`FE_FRTY_W_MNC`, cumulative births). Estimator: WLS on
published cells, cell weight = published unweighted women in the cell (weighted columns), cluster-robust SE by
country; per-SD variants reported in `results/model_table.csv`.

### 3.1 Headline model (M1: country×survey FE, 4-level panel, weighted)

| Education | Coefficient (children) | SE | 95% CI | per-SD |
|---|---|---|---|---|
| Primary (vs none) | **−0.536** | 0.060 | [−0.652, −0.419] | −0.353 |
| Secondary (vs none) | **−1.569** | 0.161 | [−1.884, −1.254] | −1.018 |
| Higher (vs none) | **−2.520** | 0.236 | [−2.982, −2.058] | −1.632 |

Monotone in education, all CIs exclude 0, n = 860 cells, 215 surveys, 65 countries.

### 3.2 Specification ladder (weighted, 4-level panel)

| Model | Primary | Secondary | Higher |
|---|---|---|---|
| **M0** country FE + 5-yr period FE | −0.559 (0.060) | −1.636 (0.191) | −2.604 (0.266) |
| **M1** country×survey FE | −0.536 (0.060) | −1.569 (0.161) | −2.520 (0.236) |
| **M2** M1 + education × pipeline density | −0.528 (0.064) | −1.643 (0.137); interaction +0.184 (0.152), p=0.23 | −2.638 (0.209); interaction +0.232 (0.156), p=0.14 |
| **M5** country FE + year FE + country trends | −0.553 (0.059) | −1.584 (0.167) | −2.536 (0.241) |
| **2-group** M1 (secondary+ vs none/primary), 346 surveys / 80 countries | — | **−1.545** (0.143) | — |

Reading: the gradient is **not produced by the FE choice** (M0 ≈ M1 ≈ M5) and is **not absorbed by
country-specific trends**. The **pipeline-density interaction is positive in direction** (shallower gradient
where more women have secondary+), consistent with the prior record's E3 direction (+0.13 (0.05) per
+10pp), but is **not statistically distinguishable from zero in this panel** (0.18 (0.15) per SD of pipeline,
p=0.23 for secondary). Unweighted estimates are larger in magnitude (secondary −1.87 (0.19)); both are reported.

### 3.3 Replication of the prior attempt (D1)

| | Prior record (`31ded00`) | This run (same implied sample) | Δ |
|---|---|---|---|
| primary | −0.57 | **−0.554** (0.058) | +0.016 |
| secondary | −1.62 | **−1.608** (0.166) | +0.012 |
| higher | −2.54 | **−2.520** (0.230) | +0.020 |
| cells / countries | 1,291 / 86 | **1,291 / 86** | exact |

**D1 verdict: REPRODUCED** (both pre-declared tolerance gates met: ±0.15 secondary, ±0.25 higher).

### 3.4 Heterogeneity (D2)

- **Per survey** (346 surveys with both 2-group cells): **98.8% negative** (4 non-negative), median **−1.90**,
  IQR **[−2.48, −1.43]**, min −4.60, max +0.70. Prior record: 99% negative, median −1.90. **D2 verdict:
  "near-universal"** by the pre-declared ≥ 90% threshold — *and still not "robust everywhere":* the minority is
  named (4 surveys, listed in [`results/heterogeneity_surveys.csv`](results/heterogeneity_surveys.csv)).
- **Per period** (median per-survey gradient): 1985–89 **−2.70** (94.7% negative), 1990–94 −2.20, 1995–99 −2.00,
  2000–04 −1.85, 2005–09 −1.80, 2010–14 −1.90, 2015–19 −1.90, 2020–24 **−1.70**, 2025 (3 surveys) −1.50. The
  gradient is flatter in later periods — **composition of "secondary" is the leading candidate, not a change in
  the individual relationship**; the ecological cells cannot separate them.
- **Per country** (63 countries with ≥2 surveys): **76.2% negative**, 35/63 significant at q=0.05 by
  Benjamini–Hochberg on country-level gradient p-values.

---

## 4. Q2a — does the answer change for completed ages (40–49) vs period fertility (15–49)?

Two **births-based** measures, same education breakdown, same designs:
- **A:** `FE_FRTY_W_MNC` — cumulative, women 40–49 (mean CEB).
- **B:** `FE_FRTR_W_TFR` — period TFR, ages 15–49 (weighted and unweighted not applicable: no published
  denominators, so both A and B are estimated **unweighted** for this comparison — Amendment 01 A1.1).

| Contrast | A (cumulative CEB40, per-SD) | B (period TFR, per-SD) | Ratio β_B/β_A [bootstrap 95% CI] |
|---|---|---|---|
| 4-level, secondary vs none | −1.256 | −1.278 | **1.017 [0.944, 1.102]** (65 countries, 500 draws) |
| 2-group, secondary+ vs none/primary | −1.327 | −1.274 | **0.960 [0.918, 1.002]** (80 countries, 500 draws) |

In raw children the period-TFR gradient is larger (secondary −1.950 vs −1.569; higher −2.871 vs −2.520) because
the period measure varies more across cells; the **pre-registered comparison is the standardised ratio**, which
is what the table reports. **D3 verdict: "same sign, similar magnitude"** (ratio in [0.67, 1.5], CI contains 1).

So: **the window (period vs cumulative) and the age range (15–49 vs 40–49) do not change the education gradient
in any material way in these cells.** That is a real result: the schooling–fertility association is not an
artefact of looking at completed fertility only.

Robustness: `FE_FRTR_W_GFR` (general fertility rate) gives the same sign and similar standardised magnitude
(see `results/model_table.csv`); median age at first birth (`FE_AAFB_W_M25`) has only 51 surveys with all four
education levels and is reported descriptively, not used in any decision rule.

---

## 5. Q2b — the births vs surviving-children construct contrast

### 5.1 Cell level, births-based (period vs cumulative) — null

Stacked standardised model with country×survey FE and construct × education interaction (1,712 rows, 214
surveys, 65 countries, cluster by country):

| term | coefficient (SD units) | SE | p |
|---|---|---|---|
| secondary × construct (period TFR = 1) | **−0.004** | 0.046 | 0.92 |

**No detectable difference between the period-TFR gradient and the cumulative-CEB gradient.**

### 5.2 Wanted vs actual fertility — the preference gradient is smaller (D4)

Stacked standardised model, wanted TFR (`PR_WTFR_W_WFR`, construct 0) vs actual TFR (`FE_FRTR_W_TFR`,
construct 1), 2,240 rows / 280 surveys / 82 countries:

| term | coefficient (SD units) | SE | p |
|---|---|---|---|
| secondary × construct (actual = 1) | **−0.089** | 0.024 | **0.00025** |

Interpretation: schooling is associated with **lower actual fertility more strongly than with lower wanted
fertility** — about 0.09 SD more. **D4 prediction confirmed** (`|β_wanted| < |β_actual|`): the gradient is not
purely a stated-demand gradient; there is a realisation gap. The separate models give standardised secondary
coefficients of **−1.282** (actual) vs **−1.070** (wanted). Stated "want no more children" (`PR_DESL_W_WNM`)
is reported descriptively; its sign is not part of a decision rule (parity composition makes it ambiguous).

### 5.3 Survey level, births vs surviving children — different series (D5)

`FE_CEBA_W_MNC` and `FE_CEBA_W_MND` are published **only by age group** (no education breakdown). For women
40–49 we combine the 40–44 and 45–49 cells with their published denominators:

`CEB₄₀` = weighted mean of mean CEB; `Deaths₄₀` = weighted mean of mean children died;
**`Surviving₄₀ = CEB₄₀ − Deaths₄₀`** — the individual-level identity `v201 − v206 − v207` aggregated, not a proxy.

368 surveys, 87 countries, 1985–2025:

| statistic | value |
|---|---|
| corr(Surviving₄₀, TFR) | **0.822** (Spearman 0.826) |
| corr(CEB₄₀, TFR) | **0.899** |
| median \|TFR − Surviving₄₀\| | **0.6305** |
| max \|TFR − Surviving₄₀\| | **2.681** |
| median \|TFR − CEB₄₀\| | **1.009** |
| max \|TFR − CEB₄₀\| | **3.172** |
| mean ratio TFR / Surviving₄₀ | **0.942** |
| within-country changes (65 countries): corr(ΔSurviving₄₀, ΔTFR) | **0.321** |
| within-country changes: corr(ΔCEB₄₀, ΔTFR) | **0.509** |
| median Δ gap (ΔSurviving₄₀ − ΔTFR) | **+0.435** |

**D5 statement (as pre-declared):** these answer different questions — **surviving family size vs period
births** — and the gap is a **construct difference, not an error and not a correction of either series.** Note
the levels gap here is *not* the E11 macro gap: E11 paired reconstructed surviving children/woman with UN WPP
TFR for 1950–2010 and found median |diff| 0.3042 and max 4.2677; this is a different pairing (DHS published
cells, 1985–2025, `CEB − deaths` for women 40–49 vs the same survey's period TFR). No replication of E11's
numbers is claimed, and the DHS-based number is not a correction of it.

### 5.4 Why no surviving-children-by-education gradient is reported

The API publishes the surviving-children inputs **only by age group**, never crossed with education (metadata
audit in [`data/indicator_availability.json`](data/indicator_availability.json); fixed in the pre-registration
§2.3). We do **not** construct one by matching CEB-by-education to mortality rates. That gradient is exactly
what the **individual microdata** would deliver, and the individual test is blocked on DHS approval
(`research/dhs-acquisition-2026-11-24`).

---

## 6. Cohort-of-women comparison (D6)

Repeated cross-sections, completed-fertility panel; cohort proxy = survey year − 44.5 (5-year bins), country FE,
cohort-proxy FE, education × cohort-proxy (per decade, centred):

| interaction | coefficient (children per decade) | SE | 95% CI |
|---|---|---|---|
| primary × cohort | −0.375 | 0.227 | [−0.820, +0.070] |
| secondary × cohort | −0.047 | 0.245 | [−0.527, +0.434] |
| higher × cohort | +0.077 | 0.261 | [−0.435, +0.589] |
| secondary+ × cohort (2-group) | +0.151 | 0.135 | [−0.113, +0.416] |

**D6 verdict: indeterminate** — all CIs include 0. Directionally the 2-group interaction is **positive** (the
gradient is *less steep* in later cohorts), consistent with the prior record's +0.26 (0.13) attenuation and with
the per-period medians in §3.4. This is a **cohort proxy from survey years, not followed women**; it cannot
separate composition from a change in the individual relationship — the individual test would have to.

---

## 7. Decision-rule scorecard (pre-registered D1–D7)

| Rule | Verdict | Evidence |
|---|---|---|
| **D1** replication of prior magnitudes | **PASS — reproduced** | Δ secondary +0.012, Δ higher +0.020; n/panel exact |
| **D2** coverage/generality | **"near-universal"** (98.8% ≥ 90% threshold) — minority named | 346 surveys; 4 non-negative |
| **D3** window/construct agreement (A vs B) | **"same sign, similar magnitude"** | ratio 1.017 [0.944, 1.102]; 2-group 0.960 [0.918, 1.002] |
| **D4** desired vs realised | **prediction confirmed** (`|β_wanted| < |β_actual|`) | interaction −0.089 (0.024), p=0.00025 |
| **D5** survey-level construct gap | **different series, as expected**; no correction implied | corr 0.822; median gap 0.63; change corr 0.32 vs 0.51 |
| **D6** cohort proxy | **indeterminate** (CIs include 0); direction = attenuation | see §6 |
| **D7** nulls | all nulls reported with intervals above | M2 interaction p=0.23/0.14; cohort CIs |

No decision rule was changed after seeing results. The only pre-estimation change is Amendment 01 (denominators;
hidden second dimension in one indicator), committed before estimation.

---

## 8. Ecological-limits statement (binding)

1. **The unit is a published cell, not a woman.** Every coefficient is an association between group averages —
   consistent with an individual-level association, but not evidence of one.
2. **No causal language.** No instrument, no policy discontinuity, no pre-trends, no within-woman variation.
3. **Aggregation bias is not hypothetical.** Cells differ in education composition and in everything correlated
   with it. The API never crosses education with wealth or residence, so this gradient **cannot** be separated
   from wealth/residence gradients in these data.
4. **Categories change meaning across rounds** (massification): a stable coefficient is not a stable individual
   effect; the per-period medians in §3.4 are consistent with composition.
5. **Published values are already DHS-survey-weighted**; cell weights are denominators, and they re-weight cells,
   not women.
6. **Repeated cross-sections**: one row per country × round; the cohort proxy is derived from survey years.
7. **This cannot substitute for the individual test.** The Individual Recode test
   (`research/dhs-acquisition-2026-11-24/PRE_REGISTRATION.md`) is the only design here that puts a woman's own
   schooling next to her own children ever born. Nothing above replaces it; no simulation or synthetic data was
   used anywhere.
8. **Construct naming:** `FE_FRTY_W_MNC` is a cumulative **births** measure (mean CEB, women 40–49), **not a
   TFR**. `CEB₄₀ − Deaths₄₀` is a **surviving-children** measure, **not a TFR**. Only `FE_FRTR_W_TFR` and
   `PR_WTFR_W_WFR` are rates. Tables name the construct in their headers.

---

## 9. What the individual test must beat (hand-off to the blocked microdata design)

- **The bar for "new information":** the ecological gradient is −1.57 children (secondary vs none, within
  survey) with a near-universal sign. The individual test must show whether **within-cohort, within-woman**
  schooling still carries an association **after wealth, residence and community** — the three things the public
  cells cannot separate (§8.3). If the individual gradient shrinks toward zero once those enter, the ecological
  pattern is composition; if it survives, the "dose" reading gains its first individual-level support.
- **The construct test has a clear target:** the two births-based measures agree (ratio 1.02), the wanted measure
  is weaker (−0.089 SD), and the surviving-children measure cannot be split by education in public data at all.
  The individual test should estimate the **same construct × schooling interaction** with `v201` vs
  `v201 − v206 − v207` — and it should reproduce the wanted-vs-actual gap if preferences are the weaker margin.
- **The cohort question is open:** ecological attenuation is visible but not identified; the individual data with
  birth cohorts can tell composition from change.

---

## 10. Reproduction

- **Compute location:** region-42 (`ssh -p 54585 root@region-42.seetacloud.com`), path `/root/work/dhs-api/`.
  **No estimate was computed on the Mac.** The Mac only ran the API pull (network I/O) and `build_panel.py`
  (seconds), and later only `git` and file copies.
- **Command:** `cd /root/work/dhs-api && DHS_WORKERS=48 /root/miniconda3/bin/python -u scripts/estimate.py`
  (`results/server/estimate.log`, `results/server/stats.log`).
- **Parallelisation:** `multiprocessing.Pool(48)`; each worker sets `OMP/MKL/OPENBLAS/NUMEXPR/VECLIB` thread
  limits to 1 before importing NumPy; the 500-draw country-cluster bootstrap is split as 500 independent
  tasks per contrast and the 63 per-country fits are a second `Pool.map`. Log records `workers: 48`.
- **Wall time:** **13 seconds** (start epoch 1795518781; `WALL_SECONDS=13`). **Load average** sampled during the
  run: **10.5–11.8** (1-min; the box baseline before the run was ≈6–8 from other work, so this job contributed
  roughly 4–6 runnable processes' worth on average, spiking to 48 Python processes during pool dispatch);
  **CPU (system-wide, 96 cores): 5–19% `us`** across samples. The job is small: the 13-second wall time is
  dominated by argument marshalling and the ~40 serial fixed-effects fits, not by the bootstrap.
- **Environment:** Python 3.10.8, **numpy 1.24.1** on the server (no scipy/pandas/statsmodels needed — the script
  is numpy + stdlib only). Local Python had numpy 1.24.3. **Delta check:** the substantive coefficients are
  identical to 4 decimal places between the local NumPy 1.24.3 run and the server NumPy 1.24.1 run. The only
  differences are method/design changes made before this final run and recorded in Amendment 01/this report:
  per-country SEs use HC0 (cluster-robust is degenerate with one country per model) and the bootstrap CIs use
  500 draws instead of the earlier partial run's 300. No numpy-version discrepancy to hide.
- **Determinism:** bootstrap seeds are `20261124 + i` (fixed); the point estimates are closed-form WLS. Re-running
  the script on the same cache reproduces the numbers bit-for-bit up to BLAS arithmetic ordering.

**Files:** `results/results.json` (all coefficients, CIs, samples, diagnostics), `results/model_table.csv`
(flat model table), `results/heterogeneity_surveys.csv`, `results/heterogeneity_countries.csv`,
`results/heterogeneity_bh.json`, `results/survey_construct.csv`, `results/server/{estimate,stats}.log`;
scripts `scripts/pull_dhs_api.py`, `scripts/build_panel.py`, `scripts/estimate.py`; cache under `data/raw/`
with `data/MANIFEST.sha256`; `data/panel_checks.json`; pre-registration `88073d0`, Amendment 01 + pull
`856c421`.

**UNVERIFIED / open items:** DHS API Terms & Conditions text (JS-only page; attribute DHS, no bulk scraping);
the `FE_AAFB_W_M25` education breakdown is sparse (51 surveys with 4 levels) and is descriptive only; the
want-no-more national-vs-cell check differs by up to 2.74 pp in some surveys (universe/rounding — reported, not
corrected); the exact DHS-8 Guide period-TFR window is not re-derived here (we use the API's published TFR as
DHS defines it).
