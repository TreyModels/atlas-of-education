# Fertility trend check

Tests whether the page's levels relation between fertility (period TFR) and trending covariates survives first differences and an Engle-Granger cointegration test.

Run: `python3 check.py` (statsmodels backend, writes `results.json`). `python3 check.py --no-statsmodels` runs the numpy/scipy/pandas fallback (writes `results_fallback.json`).

Inputs: TFR from `public/research/fertility/fertility-series.json`; life expectancy and GDP per capita from `fertility-research-full.zip` (`life_asia.json`, `asia_panel_data.json`). The page series matches the panel TFR exactly. Sample 1961–2024, n = 64 per place. Covariates are World Bank series via FRED.

## Before (levels) and after (first differences)

Slopes: TFR on the covariate. Levels are the page's trend-on-trend form. Differences use HAC (Newey-West, 2 lags) p-values. EG p is the statsmodels Engle-Granger cointegration p-value (MacKinnon, N=2, constant).

| Place | Covariate | Levels slope | Levels R² | Diff slope | Diff HAC p | EG p |
|---|---|---|---|---|---|---|
| PHL | life expectancy | −0.380 | 0.89 | +0.019 | 0.0001 | 0.079 |
| THA | life expectancy | −0.206 | 0.94 | −0.079 | 0.069 | 0.084 |
| KOR | life expectancy | −0.155 | 0.87 | −0.015 | 0.009 | 0.709 |
| JPN | life expectancy | −0.058 | 0.83 | +0.016 | 0.72 | 0.353 |
| HKG | life expectancy | −0.211 | 0.82 | −0.021 | 0.46 | 0.806 |
| CHN | life expectancy | −0.177 | 0.78 | +0.205 | <0.001 | 0.330 |
| PHL | log GDP per capita | −4.206 | 0.85 | +0.023 | 0.89 | 0.734 |
| THA | log GDP per capita | −2.165 | 0.90 | −0.481 | 0.046 | 0.651 |
| KOR | log GDP per capita | −1.215 | 0.90 | −0.436 | 0.32 | 0.320 |
| JPN | log GDP per capita | −0.583 | 0.77 | +0.240 | 0.58 | 0.890 |
| HKG | log GDP per capita | −1.614 | 0.86 | +0.238 | 0.41 | 0.398 |
| CHN | log GDP per capita | −1.017 | 0.65 | −2.231 | 0.34 | 0.257 |

Pooled over six places (no place effects, HAC p):

| Covariate | Levels, pooled | Levels, within place | Differences, pooled |
|---|---|---|---|
| life expectancy | −0.170 (R² 0.77) | −0.181 (R² 0.78) | +0.109 (p 0.096, R² 0.16) |
| log GDP per capita | −0.893 (R² 0.59) | −1.333 (R² 0.69) | −0.507 (p 0.22, R² 0.01) |

## Sensitivity: sample from 1964

The 1961–63 Chinese series swings from 3.86 to 6.09 to 7.51, which drives CHN's differenced fit. Dropping 1961–63 (sample 1964–2024):

| Place | LE levels | LE diff | LE diff HAC p | LE EG p | GDP EG p |
|---|---|---|---|---|---|
| PHL | −0.367 | +0.018 | 0.0001 | 0.127 | 0.68 |
| THA | −0.202 | −0.081 | 0.065 | 0.075 | 0.503 |
| KOR | −0.146 | −0.018 | 0.0004 | 0.791 | 0.128 |
| JPN | −0.063 | +0.007 | 0.90 | 0.043 | <0.001 |
| HKG | −0.191 | −0.025 | 0.42 | 0.164 | 0.073 |
| CHN | −0.197 | −0.334 | 0.007 | 0.516 | 0.356 |

In CHN the differenced LE slope changes sign between the two samples (+0.205 in 1961–2024, −0.334 in 1964–2024).

## Unit roots (prerequisite for Engle-Granger)

ADF with AIC lag choice, 64 observations. Results are mixed. TFR is I(1) by ADF in PHL and JPN only, and trend-stationary in THA, KOR, HKG and CHN at 5%. Life expectancy is stationary in levels in THA, KOR, JPN, HKG and CHN. Low power at n = 64 makes these calls weak. Engle-Granger is a standard test for I(1) series, so its results are less clean for places where the series are I(0).

## Leave-one-place-out spread (the page's stored development series)

Recomputed from `fertility-series.json`. The fits are the page's stored series, not refitted here.

- Development model, mean absolute error 1961–2024: 0.30 (JPN) to 1.14 (PHL); mean 0.61; SD 0.29.
- Development model, 1985–2024: 0.24 (HKG) to 0.81 (PHL); mean 0.40. This is the "0.40" on the page.
- Development + matching + post-2015 dummy, 1985–2024: 0.13 (HKG) to 0.94 (PHL); mean 0.39.
- 2024 held-out predictions of the development model range from 1.06 (JPN) to 2.22 (PHL). KOR is 1.22 and HKG 1.32. The page's "floor of about 1.3–1.5" is not what these predictions show for JPN and KOR.

Six held-out errors give a wide and unstable spread. It is not a confidence interval.

## Reading

- The levels relation is strong in every place (R² 0.65–0.94 for life expectancy and GDP).
- It does not survive first differences. Four of twelve differenced slopes are significant at 5%: PHL life expectancy (+0.019, p 0.0001, wrong sign, R² 0.06), THA GDP (−0.48, p 0.046, R² 0.04), KOR life expectancy (−0.015, p 0.009, R² 0.01) and CHN life expectancy (+0.205, p <0.001, R² 0.42, driven by the 1961–63 swing). The signs disagree across places, and the explained variance is small except in CHN.
- Engle-Granger finds no cointegration at 5% in any place over 1961–2024 (lowest p 0.079, PHL). Over 1964–2024, only JPN passes (life expectancy p 0.043; GDP p <0.001), while its differenced slope is near zero (p 0.90 and 0.80).
- Conclusion: the headline claim that development explains the fall, with a floor of 1.3–1.5, does not stand as a time-series result. The levels fit is real across places. It is not shown to be a stable year-to-year relation.

## Caveats

- Period TFR, not cohort fertility. Timing effects (tempo) move period TFR without changing completed family size.
- n = 64 per place. Unit-root and cointegration tests have low power, and EG p-values are asymptotic.
- Two covariates only. Infant mortality (in the panel) and education are not used.
- Pooled standard errors ignore cross-place dependence and are too small.
- statsmodels and numpy-fallback EG statistics differ, because the fallback uses one fixed lag and statsmodels uses AIC. Both agree that no place passes at 5% over 1961–2024. Levels and difference slopes are identical in both.
