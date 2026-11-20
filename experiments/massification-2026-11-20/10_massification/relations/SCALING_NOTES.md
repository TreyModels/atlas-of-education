# SCALING_NOTES — method, caveats, and what the model must reproduce

**Author:** `pattern-scout` · task-36 · 2026-11-20 · write scope `10_massification/relations/`.
**Status: PROVISIONAL** — these are inputs to the Council's gate, not supplied model parameters. Per the phase rules
(and Council brief 013), scaling relations here are **checks or constraints on the model**, never targets and never
parameters. Nothing in this directory may be fitted to.

**Sources.** (a) My 30-country WDI panel `09_relations/data/panel_wdi_wide.csv` (45+ indicators, 1960–2024, rebuilt
from raw archived API payloads; observed cells only). (b) `04_data/data/gmr_observed_6countries_1970_2024.csv`
(observed-only; the imputed companion file is never read as observations). (c) data-hunter's task-34 MVP
`10_massification/data/UNIVERSALIZATION_SERIES.csv` (sha256 `85bc8693…`, 2,458 rows) and
`JOBS_AND_MARKETS_PANEL.csv` (sha256 `aaaab274…`, 5,622 rows), ACKed and adopted; every table row states its source.
(d) `04_data/complexity/ECONOMIC_COMPLEXITY.csv` (Growth Lab ECI, CC0) for the parked complexity axis.

---

## 1. Universalization curves

**Fit.** Logistic `y = K / (1 + exp(-r (t - t0)))` and Gompertz `y = K exp(-exp(-r (t - t0)))`, bounded NLS with
multi-start (48 starts). Ceiling bound: `K ≥ max(observed)` and `K ≤ 130` for GER, `≤ 100.5` for completion. Declared
before fitting: **fit 1980–2010, holdout 2011–2024**. 194 series fitted, 634 parameter rows.
`data/universalization_fits.csv`.

**Shape parameters for the six countries (identified fits, full sample, logistic):**

| Country | Indicator | ceiling K (se) | slope r (se) | midpoint t0 (se) | R² | net rise |
|---|---|---|---|---|---|---|
| PHL | secondary GER | 92.3 (2.4) | 0.0525 (0.0051) | 1971.9 (0.9) | 0.96 | +41.0pp |
| KOR | secondary NER | 98.2 (0.6) | 0.1414 (0.0063) | 1974.7 (0.2) | 0.99 | +62.7pp |
| HKG | secondary NER | 96.1 (8.2) | 0.0576 (0.0146) | 1976.6 (3.0) | 0.91 | +62.3pp |
| KHM | lower-secondary GER | 71.3 (2.7) | 0.2162 (0.0296) | 2002.1 (0.5) | 0.95 | +47.0pp |
| KHM | primary completion | 84.6 (2.6) | 0.1583 (0.0214) | 2001.5 (0.6) | 0.96 | +50.3pp |
| CHN | upper-secondary GER | 90.4 (6.8) | 0.1595 (0.0308) | 2002.3 (1.2) | 0.92 | +49.3pp |
| CHN | tertiary GER | 125.6 (9.4) | 0.1267 (0.0053) | 2020.1 (1.2) | 0.995 | +76.7pp |
| JPN | tertiary GER | 108.3 (28.9) | 0.0371 (0.0076) | 2010.0 (15.2) | 0.96 | +48.4pp |

**What the model must reproduce** (per SUCCESS_CRITERIA): midpoint year within ±5y, final level within ±5pp,
in-sample MAE ≤5pp, holdout MAE ≤8pp and better than last-value and linear-trend benchmarks, shape correlation ≥0.6
in-sample / ≥0.5 out-of-sample, and no false universalization where the observed series did not universalize.
The fits above give the **observed midpoint** to check against, not a schedule to supply.

**Common shape?** The restricted model (shared slope `r`, country-specific ceiling and midpoint) is **rejected** on the
asymptotic F test for secondary GER (F=4.21, p=0.003), tertiary GER (F=60.9, p<0.001), upper-secondary GER (F=3.58,
p=0.018) and primary NER (F=2.77, p=0.045). **But the auditor's caveat applies and is adopted:** these are F tests on
nonlinear fits with few countries, so "rejection" is provisional. Therefore:
- `data/universalization_common_shape_bootstrap.csv` gives a residual-bootstrap p for each indicator (reps=40, trimmed
  for runtime). Read the bootstrap p, not only the asymptotic p, before any "no common shape" claim.
- `data/e6_shape_comparison.csv` (E6) compares **logistic vs Gompertz vs linear vs exponential** on the declared
  holdout per series, so the shape claim is a model-comparison claim, not a single-model F claim.
- The honest reading: *similar shapes, country-specific timing and slopes*; slope varies ~5× across the six
  (KHM r≈0.22 vs HKG r≈0.06), so a single common slope is not supported but a common *family* is.

**Out-of-school supplement** (`data/universalization_fits_supplement.csv`): fitting the in-school rate (100 − OOS)
works only where the series still varies; KHM lower-secondary is a genuine curve (K=86.6, r=0.486, t0=2004.7, R²=0.91),
whereas KOR/JPN/HKG primary are already universal at the start (R²<0, midpoint at the bound) → **not identified**, and
reported as such rather than forced.

**Reproducibility check:** re-fitting `ger_secondary` from data-hunter's `UNIVERSALIZATION_SERIES.csv` reproduces my
GMR-based parameters exactly (same underlying observations; `data/universalization_refit_verification.csv`, identical
for PHL/KHM/CHN/HKG/KOR). This is a provenance check, not an independent replication.

## 2. Scaling laws

**Method.** Log-log (and semi-log where the driver is already a share) OLS with two FE structures:
**within** = country+year FE, CR1 clustered on country (the within-country exponent), and
**between** = year FE only (the cross-country exponent, the classic scaling-law object).
15 relations, `data/scaling_laws.csv`. All graded **correlational**; "scaling law candidate" means stable across
within/between, not causal.

**Candidate laws (within / between exponents):**

| Relation | within | between | reading |
|---|---|---|---|
| Secondary GER ← GDP pc | 0.090 (0.124) ns | **0.215 (0.035)** | between-country scaling; within-country the income effect is weak (the R04 income→tertiary finding is the strong one) |
| Tertiary GER ← GDP pc | **0.848 (0.172)** | **0.567 (0.082)** | the strongest education-income scaling in the panel |
| Tertiary share of enrolment ← GDP pc | **0.692 (0.149)** | **0.280 (0.051)** | same ordering, weaker between |
| Lower-secondary completion ← GDP pc | **0.247 (0.119)** | **0.169 (0.034)** | stable both ways |
| Upper-secondary attainment ← GDP pc | 0.072 (0.167) ns | **0.312 (0.052)** | a between-country law only; the within-country stock moves on a 30–40y lag (cf. LITERACY_ECI_DEMOGRAPHY.md) |
| Agriculture share ← GDP pc | −0.120 (0.083) ns | **−0.990 (0.216)** | between ≈ unit elasticity (Engel); within countries the transition is slower |
| Industry share ← GDP pc | **0.528 (0.151)** | **0.143 (0.056)** | within > between: structural change within a country outpaces the cross-section |
| Services share ← GDP pc | **0.275 (0.083)** | **0.294 (0.039)** | stable both ways |
| GDP pc ← upper-secondary attainment | 0.051 (0.109) ns | **1.176 (0.258)** | education-stock↔output is a between-country relation; not identified as causal |
| Secondary GER ← fertility | −0.006 (0.219) ns | **−0.612 (0.127)** | between-country only |
| Primary completion ← fertility | **−0.189 (0.044)** | **−0.122 (0.027)** | stable both ways — the cohort-size law |
| Secondary GER ← urban share (pp) | **0.0105 (0.0044)** | **0.0119 (0.0023)** | stable, small |
| Wage-and-salaried share ← GDP pc | **0.206 (0.075)** | **0.339 (0.047)** | formalisation scales with income both ways |

**Five exponents worth the model's attention** (check/constraint only):
1. **Tertiary GER ← GDP pc, 0.85 within / 0.57 between** — the largest and most robust education-income exponent.
2. **Tertiary share ← GDP pc, 0.69 within** — the structural-composition version of (1).
3. **Lower-secondary completion ← GDP pc, 0.25 within / 0.17 between** — stable; the completion margin the gate fits.
4. **Primary completion ← fertility, −0.19 within / −0.12 between** — the cohort-size law that survives every split.
5. **Agriculture share ← GDP pc, −0.99 between** — the structural-transformation constraint on sector flows.
(6th, for the sector link: industry share ← GDP pc 0.53 within > 0.14 between — the within/between gap itself is a
finding the model must respect: a country's own transition is faster than the cross-section suggests.)

## 3. Push-pull lead-lag

**Method.** 13 panel Granger-style tests: `y_t ~ own lags(1–5) + driver lags(1–5)`, two-way FE, CR1 clustered on
country; Wald test on the driver-lag block; annual changes; N=295–787, 27–30 countries. `data/push_pull_tests.csv`.

**Headline set (all labelled EQUIVALENT / descriptive per STOP RULE R13 — no direction claims):**
- Lagged GDP-pc growth → secondary/tertiary GER growth: **null** (p=0.45, 0.66, 0.18) — the aggregate income-pull
  reading is not supported in annual data.
- Lagged wage-and-salaried-share growth → secondary-GER growth: joint **F=4.11, p=0.001**, sum +0.050 (se 0.038) —
  the formal-jobs association is the one that survives; it is **a predictive moment, not identification**.
- Lagged tertiary-GER growth → GDP-pc growth: joint F=6.52, p<0.001, sum +0.205 (se 0.210) — jointly significant,
  individual sum not; consistent with either ordering.
- Lagged completion growth → GDP-pc growth: joint F=3.51, p=0.004, sum **−0.667 (se 0.270)** — replicates the
  register's R13 negative education→growth sign; **this is a constraint, not a push-pull verdict**.
- Spending → enrolment weak (p=0.14); enrolment → spending null (p=0.83); enrolment → formal jobs p=0.094.

**What cannot discriminate.** Panel moments of this kind are **observationally compatible with demand-led, supply-led
and complementary data-generating processes**. deepseek-exp2's forced-ID gate (msg 761cb5cd) reports NOT IDENTIFIABLE
(forced-ID 1.00); the Council's R13 bars direction claims from panel moments. Consequence adopted: every row carries
`claim_label = EQUIVALENT / descriptive`, `direction_claim = none`, and a `cannot_discriminate` note. The lead-lag set
**ranks which channel to test**, it does not select one. Direction requires the E2 (PH K-12 cohort exposure) and E3
(PH nurse-visa) designs, with E1 as the integration test.

## 4. Caveats (hard)

- **Logistic identification.** Midpoint and ceiling are jointly identified only when the series starts well below the
  ceiling and has a completed take-off. Where the series is already near-ceiling at the first observation (KOR/JPN/HKG
  primary, KOR secondary NER), the midpoint is pinned at the bound and `fit_status=not_identified`; 68 of 194 series
  are identified. **Never quote an unidentified midpoint.** `ident_flags` says why.
- **Ceiling priors.** GER is capped at 130 and completion at 100.5; a ceiling at the bound (`ceiling_at_bound`) means
  the data still rise and K is not estimated — read those rows as "rising, no ceiling identified".
- **Gross vs net.** GER can exceed 100 (over-age/repetition) and is **not** a cohort participation measure; NER and
  completion are. Mixing them is a definition trap. Universalization verdicts must use completion/NER (as
  SUCCESS_CRITERIA does), not GER.
- **Cohort vs stock.** Attainment and literacy are stocks of past cohorts; they move on 30–40 year lags and their
  measured rises are largely cohort replacement (62–66% median; `09_relations/LITERACY_ECI_DEMOGRAPHY.md`). A model
  that equates Δattainment with current schooling effectiveness is wrong by a factor of ~2–3.
- **PPP.** Scaling elasticities are sensitive to the income measure. The panel uses constant-2015 USD GDP pc for the
  within/between tests (PPP pc is available and gives similar signs); do not mix the two across rows.
- **Non-nested F tests are provisional** on short nonlinear series — the bootstrap and the E6 model comparison exist
  precisely because the asymptotic p on a 4–6 country nonlinear fit is not a reliable rejection.
- **Annual Granger tests are not causal**, and with 5 lags and FE they can absorb slow common trends into the country
  effects; first differences are used to reduce this but do not eliminate it.
- **Blocked data** (from data-hunter's notes, adopted): ILOSTAT 403, OECD 403, PSA 403, Enterprise Surveys 000,
  WDI productivity codes 000 → **no wages/earnings by education**, which is the single largest gap for a push-pull
  test. Sector shares are ILO-modelled, not measured.

## 5. What the model must reproduce (constraint list, not parameters)

1. The **midpoint years** in §1 for the six countries, within ±5y, on held-out PHL/CHN 2011–2024 and held-out KHM.
2. **No false universalization**: countries whose observed series did not cross must not cross in the model.
3. **Slope heterogeneity** (~5× range) rather than one common slope — the common-shape F is rejected provisionally and
   the E6 comparison says which functional form survives out-of-sample.
4. The **sign constraints** already registered: income→tertiary positive (R04), spending→primary null (R02),
   education→growth negative in the panel (R13), fertility→completion negative (R07).
5. **Sector shares**: agriculture ← GDP pc between-elasticity ≈ −1.0; within-country transition faster for industry
   (0.53) than the cross-section (0.14) — the model's sector block must be able to produce that gap.
6. **Push-pull**: the model must be run under demand-led, supply-led and complementary orderings and must be able to
   match the observed lead-lag moments **under more than one** — the equivalence is the finding, and the E1/E2/E3
   designs are what break it (or fail to).

## 6. Files

| File | Content |
|---|---|
| `data/universalization_fits.csv` | 634 fits: logistic+Gompertz, full sample + 1980–2010 fit / 2011–2024 holdout, identification flags, 194 series |
| `data/universalization_common_shape.csv` | common-slope F tests (asymptotic) |
| `data/universalization_common_shape_bootstrap.csv` | residual-bootstrap p (provisional, reps=40) |
| `data/e6_shape_comparison.csv` | E6 logistic vs Gompertz vs linear vs exponential, holdout comparison |
| `data/universalization_fits_supplement.csv` | in-school rate (100 − OOS) curves |
| `data/universalization_refit_verification.csv` | provenance check against data-hunter's series |
| `data/scaling_laws.csv` | 15 relations × within/between exponents, SEs, FE structure, grade |
| `data/push_pull_tests.csv` | 13 panel lead-lag tests, EQUIVALENT-labelled |
| `scripts/` | `fit_universalization.py`, `e6_shape_bootstrap.py`, `scaling_laws.py`, `push_pull.py`, `oos_curves_and_verify.py`, `refit_from_datahunter.py` |
