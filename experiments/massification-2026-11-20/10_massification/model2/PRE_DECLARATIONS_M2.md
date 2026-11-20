# PRE-DECLARATIONS — Massification model2: independent scaling + rival-model identification

**Scope:** `10_massification/model2/` only. Shadow education is secondary and its closed claims are NOT
re-fit. **Rules binding:** predeclare; label **observed** vs **simulated**; **never use imputed cells as
observations**; fit/holdout split 1980–2010 / 2011–2024 where data permit; no target coded as a parameter.

**Data at predeclaration time:** `10_massification/data/` and `10_massification/relations/` are EMPTY
(workstreams 34/36 not landed). Declared fallback inputs, all observed cells only:
`04_data/ECONOMY_SERIES.csv` (6 countries, 1995–2024: GDP pc PPP/constant, sector shares, urban, wage/
vulnerable shares), `04_data/data/gmr_observed_6countries_1970_2024.csv` (UIS observed GER/completion,
no imputation), `09_relations/data/panel_wdi_eci.csv` (30-country wide WDI panel 1960–2024: GDP pc PPP,
GER by level, completion, agriculture share, urbanisation, education spending, pupil–teacher ratio,
fertility, population growth, private shares). The `gmr_annual_1980_2020_imputed.csv` file is **never**
used. When `10_massification/data|relations` land, the script re-reads them if present (same variable
names) and otherwise uses the fallback — recorded in the manifest.

## (1) Scaling estimation — independent estimator/sample (different from pattern-scout's levels two-way FE)

**Pairs (log-log unless noted):** GER secondary/tertiary/primary vs GDP pc PPP; upper-secondary completion
(logit) vs log GDP pc; lower-secondary completion vs log GDP pc; agriculture employment share (log) vs log
GDP pc; urbanisation (logit) vs log GDP pc; fertility/TFR (log) and population growth vs completion (logit);
services/wage/vulnerable shares (UIS6 sample) vs log GDP pc. **Returns vs schooling:** no earnings microdata
in any on-disk panel → declared **UNABLE** (the 8.8% Mincer figure is `calibration-only`, not an estimate
and not used as an observation).
**Samples:** (S-A) UIS6 observed panel (6 countries, 1980–2024); (S-B) WDI30 panel (30 countries, 1980–2024,
observed cells); (S-C) UIS6 1995–2024 joint with economy series.
**Estimators (independent of pattern-scout's levels two-way FE; that estimator is reported only as
reference):** (E1) **10-year long differences** pooled with period FE, country-clustered SE; (E2) **between**
estimator (country means, HC1 SE, N = countries); (E3) **country-specific time-series OLS** with Newey–West
(lag 3), report median/range of exponents; (E4) first differences pooled with year FE, country-clustered SE.
**Timing:** contemporaneous and 5-year lag.
**Reporting:** exponent, SE, N, clusters, FE structure, sample, timing; sign-and-magnitude stability across
estimators×samples; **classification** = *scaling law* if sign stable and |exponent| within a factor of 2
across all estimator/sample combos with ≥2 significant estimates; *period/region regularity* if sign or
magnitude flips across samples/periods; *unidentified* if no combination is significant. Identification
grade: A (stable, several samples/estimators), B (stable within sample), C (fragile), D (unable).

## (2) Universalization dynamics

- **Logistic fit** y = K / (1 + exp(−r(t−t0))) per country × level (GER primary/secondary/tertiary;
  completion upper-secondary where ≥15 observed points), bounded K, r, t0; **uncertainty** by residual
  bootstrap (B = 300, observed years).
- **Common-parameters test:** per-country fits vs (a) common r with country-specific K,t0; (b) common K,r
  with country-specific t0; compare AIC and F-test (SSE).
- **Lead–lag:** per country, cross-correlation of Δlog GER_secondary (and tertiary) with Δlog(agri share),
  Δlog GDP pc, Δurban at lags −10…+10; report peak lag and sign; **block bootstrap** (B = 200, block 5)
  for the peak-lag CI. **Not identifiable** if peak lag CI covers the whole window or sign flips.

## (3) Rival model comparison (same design as earlier C1/U2)

Country-level time-series (train 1980–2010, test 2011–2024 where ≥8 training and ≥5 test points):
- **Demand-led (pull):** log GER_t = a + b·log GDP_{t−1} + c·log agri_{t−1} + ε.
- **Supply-led (push):** log GER_t = a + b·log GER_{t−1} + trend + u; log GDP_t = d + f·log GER_{t−1} +
  g·log GDP_{t−1} + ε.
- **Complementary:** both equations with the pull term and the push feedback.
Report in-sample and out-of-sample RMSE/R² per country/level; pooled AIC. **Observational-equivalence
region:** for each rival pair, the region of (income, initial GER) or (spending, GER) space where the two
models' predicted education differs by < 2× residual noise sd; report the fraction of observed covariate
space inside it.

## (4) Push–pull identification (the decisive test)

Simulate a panel of 30 countries × 30 years (observed covariate scaffolding, fixed seeds) from four truths:
**D demand-led/pull** (GER responds to lagged income + agriculture; no feedback to GDP), **S supply-led/push**
(exogenous logistic GER path drives GDP growth), **C complementary** (both feedbacks), **OUTSIDE cohort/
fertility truth** (GER driven by lagged TFR only; no income/push channel — outside the candidate set).
Mask the generator; fit the three rivals (D, S, C) by OLS/system likelihood; choose by AIC.
**Recovery** = share of candidate-truth simulations where the correct rival is chosen; **forced-ID** = share
of OUTSIDE-truth simulations classified as any candidate; **equivalence** = share where all three rivals'
AIC are within 2 (report as *not identified* rather than a forced choice).
**Threshold (predeclared):** push–pull is **identifiable** iff recovery ≥ 0.67 AND forced-ID = 0 AND
equivalence < 0.34 for the candidate truths; otherwise report **NOT identifiable** (with the equivalence
regions). No threshold changed after results.

**Failure rule:** failed fits are logged and excluded with counts; no imputation.
