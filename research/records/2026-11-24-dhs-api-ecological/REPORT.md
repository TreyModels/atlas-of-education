# REPORT — schooling → fertility across **all** public DHS survey rounds (ecological, observed data)

**Status:** complete, **corrected**. Pre-registration committed **before any value was pulled** (`88073d0`);
Amendment 01 and the pull/panels committed **before any estimate** (`856c421`); first estimation on region-42
(`708e34a`); **fixed-effect bug found and corrected on 2026-11-24 23:55** (second box; see §0).
**Branch:** `research/dhs-api-ecological-2026-11-24`. **Task:** task-16 (+ task-36 extension).
**Owner:** dhs-scout.
**Labels:** every number is **OBSERVED (published DHS aggregates) / ECOLOGICAL** — the unit is a
country × survey × education cell, **not a woman**. **No causal language is supported.**
**This cannot substitute for the blocked Individual Recode test.** No simulation or synthetic data is used or
presented anywhere.

---

## 0. Correction notice (read before quoting any number)

The first committed estimate (`708e34a`) dropped the reference level of every categorical fixed effect **without
an intercept**, which constrained the reference group's mean to zero and biased all FE models by ~0.015–0.019
children. Found while independently validating the estimator; fixed by pre-pending an intercept. The **prior
DHS record (`research/dhs-micro-2026-11-23 @ 31ded00`) is unaffected** — it used the correct weighted
within-transform, and the corrected run now reproduces it to **≤0.004**.

**What changed:** full-sample M1 secondary −1.5685 → **−1.5837**; primary −0.5355 → **−0.5541**; higher −2.5201 →
**−2.5382**; Q2a 4-level ratio 1.017 → **1.003**; Q2b1 wanted-vs-actual −0.0893 → **−0.0775**; cohort 2-group
interaction +0.1515 (p=0.26) → **+0.2438 (p=0.016)** — so **D6 moves from "indeterminate" to "attenuation"**.
Per-survey/per-period gradients and the survey-level construct statistics are unaffected (simple differences /
correlations of published aggregates). Full account with old and new values:
[`BUGFIX_FE_PARAMETERISATION.md`](BUGFIX_FE_PARAMETERISATION.md). The biased numbers remain in git history at
`708e34a`; every number below is from the corrected run, independently cross-checked by a second implementation
(`scripts/corrected_reduction.py`, agreement to the last printed digit).

**Computation:** full-sample corrected run on `ssh -p 45973 root@connect.cqa1.seetacloud.com`,
`/root/work/dhs-api/`, **8-worker multiprocessing, 24 s wall**; 11-country extension **13 s** (numpy 1.24.1,
Python 3.10.8). **No project compute on the Mac.** Logs: `results/server_box2/`.
**New in task-36:** the 11 African countries are analysed separately in
[`AFRICA11_EXTENSION.md`](AFRICA11_EXTENSION.md) (coverage tier T1 under Amendment 02).

---

## 1. Headline numbers (all OBSERVED, published-cell level, corrected)

| # | Result | Number |
|---|---|---|
| 1 | **Prior attempt reproduced exactly.** Completed fertility (women 40–49, mean CEB) on education, country×survey FE, weighted, clustered by country — same panel as `research/dhs-micro-2026-11-23 @ 31ded00` | primary **−0.5700** (SE 0.0580), secondary **−1.6216** (0.1703), higher **−2.5364** (0.2346); **1,291 cells, 86 countries**; deltas vs prior (−0.57/−1.62/−2.54): **0.000 / 0.002 / 0.004** |
| 2 | **Gradient holds across all public rounds, with a minority.** Per-survey secondary+ gradient (2-group), 346 surveys | **98.8% negative**, median **−1.90** children (IQR −2.48 to −1.43), range −4.60 to +0.70; 4/346 non-negative |
| 3 | **Not a fixed-effects artefact.** Country FE + 5-year-period FE vs saturated country×survey FE vs country trends | M0 **−0.557 / −1.593 / −2.550**; M1 **−0.554 / −1.584 / −2.538**; M5 (+ country trends) **−0.553 / −1.584 / −2.536** |
| 4 | **Window contrast (Q2a): period TFR vs cumulative completed fertility gives the same gradient.** Standardised secondary-vs-none ratio β(TFR)/β(CEB40) | **1.0029**, cluster-bootstrap 95% CI **[0.932, 1.077]** (65 countries, 500 draws); 2-group **0.9582 [0.915, 0.998]** (80 countries) |
| 5 | **Construct contrast (b1): period-vs-cumulative births is null; desired-vs-actual is not.** Stacked, standardised, country×survey FE, clustered by country | A vs B interaction **+0.016 (SE 0.041, p=0.70)**; wanted-TFR vs actual-TFR **−0.0775 (0.0217, p=0.0004)** — wanted-fertility gradient is *smaller* than actual by 0.078 SD |
| 6 | **Construct contrast (b2): the surviving-children measure and period TFR are different series.** 368 surveys, 87 countries, 1985–2025 | corr(surviving₄₀, TFR) **0.822**; corr(CEB₄₀, TFR) **0.899**; median \|TFR − surviving₄₀\| **0.6305**, max **2.681**; median \|TFR − CEB₄₀\| **1.009**, max **3.172**; within-country change corr **0.321** vs **0.509** (65 countries) |
| 7 | **Cohort proxy: attenuation in the full sample, steepening in the African-11.** Education × cohort (per decade) | full sample: secondary **+0.240 (0.131, p=0.067)**, higher **+0.367 (0.148, p=0.013)**, 2-group **+0.244 (0.102, p=0.016)**; African-11: secondary **−0.186 (0.076, p=0.014)** — see [`AFRICA11_EXTENSION.md`](AFRICA11_EXTENSION.md) §5 |

**One-sentence reading:** in the published cells, more schooling goes with fewer children in essentially every
DHS round examined; the association is not an artefact of the FE choice or of country trends; it is the same
whether fertility is measured as a **period TFR** or as **cumulative completed fertility**; but the
births-based measures and the surviving-children measure are **demonstrably different series**, the schooling
gradient is **weaker in wanted fertility than in realised fertility**, and the cohort pattern **differs by
region**. All of this is an ecological association; the individual-level test remains unrun.

---

## 2. Data and provenance (unchanged by the correction)

- **Source:** `api.dhsprogram.com`, public endpoints, **no key, no login, no gated file**. Raw pages cached in
  [`data/raw/`](data/raw) with [`data/MANIFEST.sha256`](data/MANIFEST.sha256).
- **Unit:** country × survey round × background category (the DHS-published cell).
- **Indicators:** `FE_FRTY_W_MNC` (completed fertility 40–49; cumulative births; education breakdown; denominators
  published), `FE_FRTR_W_TFR` (period TFR 15–49; education breakdown; **no denominators**), `PR_WTFR_W_WFR`
  (wanted TFR; education; no denominators), `PR_DESL_W_WNM` (want no more; education; denominators),
  `FE_AAFB_W_M25` (median age at first birth; education; no denominators), `FE_FRTR_W_GFR` (GFR; education; **panel pulled but never estimated — no computed value exists**),
  `FE_CEBA_W_MNC` + `FE_CEBA_W_MND` (mean CEB and mean child deaths, **age groups only** → surviving-children
  measure at survey level only), `ED_EDUC_W_SEH` (pipeline density).
- **Coverage:** completed fertility 4-level **860 cells / 215 surveys / 65 countries** (2-group **692 / 346 /
  80**); period TFR **1,296 / 324 / 77**; wanted TFR **1,244 / 311 / 82**; want-no-more **1,116 / 279 / 79**;
  survey-level panel **369 surveys / 87 countries, 1985–2025**. Prior-spec replication panel **1,291 / 369 / 86**
  (identical to the prior record's sample).
- **Checks:** [`data/panel_checks.json`](data/panel_checks.json); one row per survey × education (this caught the
  hidden second dimension in `PR_DESL_W_WNM`, Amendment 01 A1.2); `DenominatorUnweighted ≥ 20` where published;
  weighted mean of education cells vs published national total (completed fertility: max abs difference **0.079
  children** over 215 surveys; want-no-more: max 2.74 pp — universe/rounding, reported not hidden).
- **What is not here:** no microdata, no individual records, no synthetic data, no reconstructed series, no proxy
  denominator, no imputation. Rate indicators without published denominators enter **unweighted** models
  (Amendment 01).

---

## 3. Q1 — does the ecological gradient hold across all public rounds?

Outcome: mean children ever born to women 40–49 (`FE_FRTY_W_MNC`, cumulative births). WLS on published cells,
cell weight = published unweighted women; cluster-robust SE by country; corrected estimator.

### 3.1 Headline model (M1: country×survey FE, 4-level panel, weighted)

| Education | Coefficient (children) | SE | 95% CI | per-SD |
|---|---|---|---|---|
| Primary (vs none) | **−0.554** | 0.059 | [−0.669, −0.439] | −0.357 |
| Secondary (vs none) | **−1.584** | 0.167 | [−1.911, −1.257] | −1.021 |
| Higher (vs none) | **−2.538** | 0.242 | [−3.012, −2.064] | −1.636 |

Monotone in education, all CIs exclude 0, n = 860 cells, 215 surveys, 65 countries.

### 3.2 Specification ladder (weighted, 4-level panel)

| Model | Primary | Secondary | Higher |
|---|---|---|---|
| **M0** country FE + 5-yr period FE | −0.557 (0.059) | −1.593 (0.170) | −2.550 (0.243) |
| **M1** country×survey FE | −0.554 (0.059) | −1.584 (0.167) | −2.538 (0.242) |
| **M2** M1 + education × pipeline density | −0.554 (0.059) | −1.675 (0.135); interaction **+0.242 (0.132), p=0.068** | −2.675 (0.207); interaction **+0.297 (0.134), p=0.027** |
| **M5** country FE + year FE + country trends | −0.553 (0.059) | −1.584 (0.167) | −2.536 (0.241) |
| **2-group** M1 (secondary+ vs none/primary), 346 surveys / 80 countries | — | **−1.551** (0.145) | — |

The gradient is **not produced by the FE choice** (M0 ≈ M1 ≈ M5) and is **not absorbed by country-specific
trends**. The **pipeline-density interaction is positive** (shallower gradient where more women have secondary+),
now significant for higher education (+0.297 (0.134), p=0.027) and marginal for secondary (+0.242 (0.132),
p=0.068) — the same direction as the prior record's E3 (+0.13 (0.05) per +10 pp). Unweighted estimates are larger
in magnitude (secondary −1.87 (0.19)); both reported in `results/model_table.csv`.

### 3.3 Replication of the prior attempt (D1)

| | Prior record (`31ded00`) | This run (same panel) | Δ |
|---|---|---|---|
| primary | −0.57 | **−0.5700** (0.0580) | 0.000 |
| secondary | −1.62 | **−1.6216** (0.1703) | 0.002 |
| higher | −2.54 | **−2.5364** (0.2346) | 0.004 |
| cells / countries | 1,291 / 86 | **1,291 / 86** | exact |

**D1 verdict: REPRODUCED — now exactly** (both pre-declared tolerance gates met; deltas ≈ 0).

### 3.4 Heterogeneity (D2)

- **Per survey** (346 surveys with both 2-group cells): **98.8% negative** (4 non-negative, listed in
  [`results/heterogeneity_surveys.csv`](results/heterogeneity_surveys.csv)), median **−1.90**, IQR **[−2.48,
  −1.43]**, min −4.60, **max +0.70**. **D2 verdict: "near-universal"** by the pre-declared ≥ 90% threshold — *not*
  "robust everywhere": the 4 non-negative surveys are named.
- **Per period** (median per-survey gradient): 1985–89 **−2.70** (94.7% negative), 1990–94 −2.20, 1995–99 −2.00,
  2000–04 −1.85, 2005–09 −1.80, 2010–14 −1.90, 2015–19 −1.90, 2020–24 **−1.70**, 2025 (3 surveys) −1.50.
- **Per country** (63 countries with ≥2 surveys): **62/63 negative** (the exception is **Tajikistan +0.04, p=0.90**), **61/63**
  significant at q=0.05 (Benjamini–Hochberg). All rows are in
  [`results/heterogeneity_countries.csv`](results/heterogeneity_countries.csv).

---

## 4. Q2a — completed ages (40–49) vs period fertility (15–49)

Both births-based; standardised within outcome; unweighted for both (rate indicators publish no denominators;
Amendment 01 A1.1).

| Contrast | A (cumulative CEB40, per-SD) | B (period TFR, per-SD) | Ratio β_B/β_A [bootstrap 95% CI] |
|---|---|---|---|
| 4-level, secondary vs none | −1.2915 | −1.2983 | **1.0029 [0.932, 1.077]** (65 countries, 500 draws) |
| 2-group, secondary+ vs none/primary | −1.3364 | −1.2806 | **0.9582 [0.915, 0.998]** (80 countries, 500 draws) |

Raw children: period TFR secondary **−2.022** (0.119) and higher **−2.944** (0.146); cumulative CEB40 secondary
**−1.584** (0.167) and higher **−2.538** (0.242). The raw difference is scale (period measures vary more across
cells); the pre-registered comparison is the standardised ratio.

**D3 verdict:** 4-level contrast **"same sign, similar magnitude"** (ratio 1.003, CI contains 1). The 2-group
contrast is "same sign" and 4% smaller in standardised units; by the letter of the pre-declared rule its CI
excluding 1 makes it **"materially different magnitude"**, and that is reported as such. Overall: **the window
and age range do not change the sign, and change the standardised magnitude by at most ~4%.**

**Not computed.** `FE_FRTR_W_GFR` (general fertility rate) was pre-registered as indicator **F** (a planned
robustness check for B) and its panel was pulled (see `data/panel_edu*_FE_FRTR_W_GFR.csv`), but
`scripts/estimate.py` never estimated it and **no GFR row exists in any committed result**
(`results/model_table.csv`, `results/results.json`, `results/africa11/results.json` — 0 matches). No GFR number
is reported or claimed here.
`FE_AAFB_W_M25` (median age at first birth) has only 51 surveys with all four education levels and is descriptive
only.

---

## 5. Q2b — the births vs surviving-children construct contrast

### 5.1 Cell level, births-based (period vs cumulative) — null

Stacked standardised model, country×survey FE, construct × education interaction, cluster by country:

| term | coefficient (SD units) | SE | p |
|---|---|---|---|
| secondary × construct (period TFR = 1) | **+0.016** | 0.041 | 0.70 |

**No detectable difference between the period-TFR gradient and the cumulative-CEB gradient.**

### 5.2 Wanted vs actual fertility — the preference gradient is smaller (D4)

Stacked standardised model, wanted TFR (construct 0) vs actual TFR (construct 1):

| term | coefficient (SD units) | SE | p |
|---|---|---|---|
| secondary × construct (actual = 1) | **−0.0775** | 0.0217 | **0.0004** |

Separate standardised models: actual TFR secondary **−1.298** (0.076) vs wanted TFR **−1.085** (0.089) — a gap of
~0.21 SD. **D4 prediction confirmed** (`|β_wanted| < |β_actual|`): the gradient is not purely a stated-demand
gradient. Stated "want no more children" (`PR_DESL_W_WNM`) is descriptive only (parity composition makes its sign
ambiguous); it is in no decision rule.

### 5.3 Survey level, births vs surviving children — different series (D5)

`FE_CEBA_W_MNC` − `FE_CEBA_W_MND` for women 40–49 (weighted combination of the 40–44 and 45–49 age cells with
published denominators): **mean surviving children**. This is the individual identity `v201 − v206 − v207`
aggregated, not a proxy. 368 surveys, 87 countries, 1985–2025:

| statistic | value |
|---|---|
| corr(Surviving₄₀, TFR) | **0.822** (Spearman 0.826) |
| corr(CEB₄₀, TFR) | **0.899** |
| median \|TFR − Surviving₄₀\| | **0.6305** |
| max \|TFR − Surviving₄₀\| | **2.681** |
| median \|TFR − CEB₄₀\| | **1.009** |
| max \|TFR − CEB₄₀\| | **3.172** |
| mean ratio TFR / Surviving₄₀ | **0.942** |
| within-country changes (65): corr(ΔSurviving₄₀, ΔTFR) | **0.321** |
| within-country changes: corr(ΔCEB₄₀, ΔTFR) | **0.509** |
| median Δ gap (ΔSurviving₄₀ − ΔTFR) | **+0.435** |

**D5 statement (as pre-declared):** different constructs — **surviving family size vs period births**; the gap is
not an error and neither series corrects the other. These are *not* E11's numbers: E11 paired reconstructed
surviving children/woman with UN WPP TFR for 1950–2010 (median |diff| 0.3042, max 4.2677); this is a different
pairing (DHS published cells, 1985–2025, `CEB − deaths` for women 40–49 vs the same survey's period TFR). No
replication of E11 is claimed and the DHS-based number is not a correction of it.

### 5.4 Why no surviving-children-by-education gradient is reported

The API publishes the surviving-children inputs **only by age group**, never crossed with education (metadata audit
in [`data/indicator_availability.json`](data/indicator_availability.json); fixed in the pre-registration §2.3). We
do **not** construct one by matching CEB-by-education to mortality rates. That gradient is exactly what the
individual microdata would deliver — and that test is blocked on DHS approval
(`../2026-11-24-dhs-acquisition/application/NEXT_ACTION_2026-11-24.md`).

---

## 6. Cohort-of-women comparison (D6)

Repeated cross-sections, completed-fertility panel; cohort proxy = survey year − 44.5 (5-year bins); country FE,
cohort-bin FE, education × cohort-proxy (per decade, centred):

| interaction | coefficient (children per decade) | SE | 95% CI |
|---|---|---|---|
| primary × cohort | −0.019 | 0.076 | [−0.169, +0.130] |
| secondary × cohort | **+0.240** | 0.131 | [−0.017, +0.497] |
| higher × cohort | **+0.367** | 0.148 | [+0.077, +0.657] |
| secondary+ × cohort (2-group) | **+0.244** | 0.102 | [+0.045, +0.443] |

**D6 verdict: attenuation** in the full sample (the 2-group interaction's CI excludes 0; the direction matches the
prior record's +0.26 (0.13)). This is a **cohort proxy from survey years, not followed women**: it cannot separate
composition from a change in the individual relationship. **Regional divergence:** restricted to the 11 African
countries the same specification gives **steepening** for primary (−0.278 (0.112), p=0.013) and secondary
(−0.186 (0.076), p=0.014) — see [`AFRICA11_EXTENSION.md`](AFRICA11_EXTENSION.md) §5. The two must not be averaged
away; the individual data are needed.

---

## 7. Decision-rule scorecard (pre-registered D1–D7)

| Rule | Verdict | Evidence |
|---|---|---|
| **D1** replication of prior magnitudes | **PASS — exact** | deltas 0.000 / 0.002 / 0.004; panel exact |
| **D2** coverage/generality | **"near-universal"** (98.8% ≥ 90% threshold); minority named | 346 surveys; 4 non-negative |
| **D3** window/construct agreement (A vs B) | 4-level: **"same sign, similar magnitude"** (1.003 [0.932, 1.077]); 2-group: same sign, **materially different magnitude** by rule (0.958 [0.915, 0.998]) | §4 |
| **D4** desired vs realised | **prediction confirmed** (`\|β_wanted\| < \|β_actual\|`) | −0.0775 (0.0217), p=0.0004 |
| **D5** survey-level construct gap | **different series, as expected**; no correction implied | §5.3 |
| **D6** cohort proxy | **attenuation** (full sample); **steepening** in the African-11 | §6, Africa-11 §5 |
| **D7** nulls | all nulls reported with intervals | Q2b1 A-vs-B p=0.70; pipeline secondary p=0.068 |

No decision rule was changed after seeing results. The two changes since the first run are a **correctness fix**
(§0) and the **T1 coverage-restricted extension** (task-36), both documented in committed files before the
affected numbers were final.

---

## 8. Ecological-limits statement (binding)

1. **The unit is a published cell, not a woman.** Every coefficient is an association between group averages.
2. **No causal language.** No instrument, no policy discontinuity, no pre-trends, no within-woman variation.
3. **Aggregation bias is not hypothetical.** The API never crosses education with wealth or residence, so this
   gradient cannot be separated from wealth/residence gradients in these data.
4. **Categories change meaning across rounds** (massification): a stable coefficient is not a stable individual
   effect.
5. **Published values are already DHS-survey-weighted**; cell weights re-weight cells, not women.
6. **Repeated cross-sections**: one row per country × round; the cohort proxy is derived from survey years.
7. **This cannot substitute for the individual test.** The Individual Recode test
   (`../2026-11-24-dhs-acquisition/PRE_REGISTRATION.md`, execution-ready at
   `../2026-11-24-dhs-acquisition/EXECUTION_READY.md`) is the only design here that puts a woman's own schooling
   next to her own children ever born. No simulation or synthetic data is used anywhere.
8. **Construct naming:** `FE_FRTY_W_MNC` is a cumulative **births** measure, **not a TFR**. `CEB₄₀ − Deaths₄₀` is a
   **surviving-children** measure, **not a TFR**. Only `FE_FRTR_W_TFR` and `PR_WTFR_W_WFR` are rates.

---

## 9. What the individual test must beat

- **Bar for "new information":** the ecological gradient is −1.58 children (secondary vs none, within survey) with
  a near-universal sign. The individual test must show whether **within-cohort, within-woman** schooling still
  carries an association **after wealth, residence and community** — the three things the public cells cannot
  separate. If the individual gradient shrinks toward zero once those enter, the ecological pattern is composition;
  if it survives, the "dose" reading gains its first individual-level support.
- **Construct target:** the two births-based measures agree (ratio 1.003), wanted is weaker (−0.078 SD), and the
  surviving-children measure cannot be split by education in public data. The individual test should estimate the
  same construct × schooling interaction with `v201` vs `v201 − v206 − v207`.
- **Cohort question:** ecological attenuation (full sample) vs steepening (African-11) is unresolved by these data;
  birth cohorts in the microdata can separate composition from change.

---

## 10. Reproduction

- **Compute:** box `ssh -p 45973 root@connect.cqa1.seetacloud.com`, path `/root/work/dhs-api/`; command
  `DHS_WORKERS=8 /root/miniconda3/bin/python -u scripts/estimate.py --outdir results`; **24 s wall, 8 workers**,
  per-worker thread limits = 1. 11-country job: same script with
  `--countries MWI,ETH,UGA,LSO,TZA,KEN,MOZ,GHA,BEN,NAM,SWZ --outdir results/africa11`, **13 s**. Box load average
  ≈ 19–25 (shared; the job used ≤ 8 of the 15-CPU container quota). **No project compute on the Mac.**
- **Environment:** Python 3.10.8, **numpy 1.24.1**; script is numpy + stdlib only. Local NumPy is 1.24.3; the
  substantive coefficients are identical to 4 dp (no numpy-version delta).
- **Determinism:** closed-form WLS; bootstrap seeds `20261124+i`; independent cross-check
  (`scripts/corrected_reduction.py`) reproduces the point estimates exactly and validates the estimator against the
  prior record (max |Δ| 0.0036).
- **Files:** `results/results.json` (corrected full sample), `results/model_table.csv`,
  `results/heterogeneity_*.{csv,json}`, `results/survey_construct.csv`, `results/africa11/*` (task-36 extension),
  `results/corrected/corrected_results.json` (cross-check), `results/server_box2/` (logs); biased-run logs kept as
  `results/server_superseded_biased/`.
- **Scripts:** `scripts/pull_dhs_api.py`, `scripts/build_panel.py`, `scripts/estimate.py` (corrected),
  `scripts/corrected_reduction.py` (independent cross-check).
- **Commits:** pre-registration `88073d0`; Amendment 01 + pull/panels `856c421`; first (biased) results `708e34a`;
  correction + task-36 outputs in the commit that carries this file.

**UNVERIFIED / open:** DHS API Terms & Conditions text (JS-only page; attribute DHS, no bulk scraping); the
`FE_AAFB_W_M25` education breakdown is sparse (51 surveys) and descriptive only; want-no-more national-vs-cell
check differs by up to 2.74 pp in some surveys (reported, not corrected); O3 period TFR is not computed from IR
(needs BR files; see `../2026-11-24-dhs-acquisition/AMENDMENT_02_ACCESS_COVERAGE.md` A2.4); the exact DHS-8 Guide
window for a computed TFR was not re-derived (we use the API's published TFR as DHS defines it).
