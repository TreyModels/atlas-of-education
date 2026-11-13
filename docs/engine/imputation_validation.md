# Imputation hold-out validation

The imputation ladder from `engine/impute` (v1.0). Deterministic: gaps deleted with seed 0, every method refit on the damaged panel. Only verified (`v`) cells are deleted and scored.

## 1. GDP per capita, Penn World Table 10.0 (annual)

114 countries, 60 year positions (1960-2019), 5 replicates, seed 0.

Gap length is the number of consecutive missing years. Errors are in log points (a value of 0.05 is about 5%), so the linear rung and the log-linear rung are compared on their natural scale.

MAE (log points) by method and gap length:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 0.034 | 0.037 | 0.055 | 0.052 | 0.080 |
| loglinear | 0.034 | 0.037 | 0.057 | 0.051 | 0.079 |

RMSE by method and gap length:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 0.077 | 0.058 | 0.114 | 0.080 | 0.121 |
| loglinear | 0.064 | 0.059 | 0.118 | 0.081 | 0.121 |

Scored points per cell:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 300 | 300 | 300 | 300 | 300 |
| loglinear | 300 | 300 | 300 | 300 | 300 |

Best method at the longest gap: `loglinear` (MAE 0.079).

## 2. Mean years of schooling, Lee-Lee / Barro-Lee / UNDP (annual 1991-2017)

151 countries, 27 year positions (1991-2017), 5 replicates, seed 0.

Gap length is the number of consecutive missing years. The cohort rung is designed for this variable.

MAE by method and gap length:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 0.048 | 0.053 | 0.064 | 0.109 | 0.179 |
| loglinear | 0.048 | 0.054 | 0.066 | 0.110 | 0.184 |
| scurve | 0.160 | 0.168 | 0.187 | 0.217 | 0.294 |
| cohort | 0.053 | 0.059 | 0.081 | 0.111 | 0.178 |
| kalman | 0.048 | 0.053 | 0.065 | 0.112 | 0.188 |
| amelia | 0.109 | 0.127 | 0.172 | 0.222 | 0.279 |

RMSE by method and gap length:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 0.084 | 0.116 | 0.127 | 0.177 | 0.245 |
| loglinear | 0.085 | 0.112 | 0.128 | 0.176 | 0.248 |
| scurve | 0.242 | 0.262 | 0.287 | 0.314 | 0.366 |
| cohort | 0.089 | 0.120 | 0.167 | 0.174 | 0.256 |
| kalman | 0.084 | 0.115 | 0.126 | 0.177 | 0.257 |
| amelia | 0.164 | 0.180 | 0.232 | 0.308 | 0.361 |

Scored points per cell:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 300 | 300 | 300 | 300 | 300 |
| loglinear | 300 | 300 | 300 | 300 | 300 |
| scurve | 300 | 300 | 300 | 300 | 300 |
| cohort | 300 | 300 | 300 | 300 | 300 |
| kalman | 300 | 300 | 300 | 300 | 300 |
| amelia | 300 | 300 | 300 | 300 | 300 |

Interval coverage (nominal 90%):

| method | nominal | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|---:|
| kalman | 0.90 | 0.940 | 0.960 | 0.950 | 0.890 | 0.870 |
| amelia | 0.90 | 0.957 | 0.967 | 0.963 | 0.940 | 0.917 |

Best method at the longest gap: `cohort` (MAE 0.178).

## 3. Barro-Lee 2010 five-year waves (one wave = 5 years)

146 countries, 13 year positions (1950-2010), 5 replicates, seed 0.

Gap length here is in waves: 1 wave = 5 years, 2 waves = 10 years.

MAE by method and waves:

| method | gap 1 wave | gap 2 wave |
|---|---:|---:|
| linear | 0.128 | 0.174 |
| loglinear | 0.124 | 0.180 |
| cohort | 0.125 | 0.177 |
| kalman | 0.121 | 0.169 |

RMSE by method and waves:

| method | gap 1 wave | gap 2 wave |
|---|---:|---:|
| linear | 0.197 | 0.270 |
| loglinear | 0.190 | 0.278 |
| cohort | 0.193 | 0.278 |
| kalman | 0.191 | 0.267 |

Scored points per cell:

| method | gap 1 wave | gap 2 wave |
|---|---:|---:|
| linear | 300 | 300 |
| loglinear | 300 | 300 |
| cohort | 300 | 300 |
| kalman | 300 | 300 |

Interval coverage (nominal 90%):

| method | nominal | gap 1 wave | gap 2 wave |
|---|---:|---:|---:|
| kalman | 0.90 | 0.933 | 0.910 |

Best method at the longest gap: `kalman` (MAE 0.169).

## 4. Lower-secondary completion, World Bank WDI (annual 1990-2025, bounded %)

125 countries, 36 year positions (1990-2025), 5 replicates, seed 0.

The series the project downloads in B4 (SE.SEC.CMPT.LO.ZS). Bounded percentage in [0, 100], so the S-curve rung is applicable.

MAE by method and gap length:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 2.397 | 3.043 | 2.219 | 3.523 | 4.134 |
| loglinear | 2.408 | 3.014 | 2.267 | 3.466 | 4.097 |
| scurve | 4.549 | 5.131 | 3.946 | 4.498 | 4.808 |
| kalman | 2.430 | 3.065 | 2.229 | 3.427 | 3.992 |

RMSE by method and gap length:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 4.735 | 5.059 | 3.344 | 5.733 | 7.107 |
| loglinear | 4.834 | 5.022 | 3.414 | 5.676 | 6.862 |
| scurve | 7.015 | 7.784 | 5.800 | 6.739 | 7.290 |
| kalman | 4.675 | 5.005 | 3.345 | 5.569 | 6.664 |

Scored points per cell:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 300 | 300 | 300 | 300 | 300 |
| loglinear | 300 | 300 | 300 | 300 | 300 |
| scurve | 300 | 300 | 300 | 300 | 300 |
| kalman | 300 | 300 | 300 | 300 | 300 |

Interval coverage (nominal 90%):

| method | nominal | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|---:|
| kalman | 0.90 | 0.927 | 0.910 | 0.960 | 0.927 | 0.913 |

Best method at the longest gap: `kalman` (MAE 3.992).

## 5. Lower-secondary completion, UNESCO UIS (annual 1996-2024, bounded %)

40 countries, 27 year positions (1996-2024), 5 replicates, seed 0.

UIS register-based completion (CR.2) from the curated B4 extract. Bounded in [0, 100].

MAE by method and gap length:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 0.954 | 0.933 | 0.682 | 0.944 | 0.955 |
| loglinear | 0.954 | 0.937 | 0.683 | 0.972 | 0.979 |
| scurve | 1.267 | 1.280 | 0.952 | 1.547 | 1.213 |
| kalman | 0.943 | 0.915 | 0.690 | 0.924 | 0.943 |

RMSE by method and gap length:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 1.749 | 1.792 | 0.984 | 1.509 | 1.599 |
| loglinear | 1.749 | 1.788 | 0.987 | 1.530 | 1.635 |
| scurve | 2.192 | 2.339 | 1.607 | 2.674 | 2.387 |
| kalman | 1.740 | 1.775 | 0.996 | 1.467 | 1.539 |

Scored points per cell:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 300 | 300 | 300 | 300 | 300 |
| loglinear | 300 | 300 | 300 | 300 | 300 |
| scurve | 300 | 300 | 300 | 300 | 300 |
| kalman | 300 | 300 | 300 | 300 | 300 |

Interval coverage (nominal 90%):

| method | nominal | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|---:|
| kalman | 0.90 | 0.910 | 0.907 | 0.963 | 0.920 | 0.950 |

Best method at the longest gap: `kalman` (MAE 0.943).

## 6. Out-of-school rate, lower-secondary age, UNESCO UIS (annual 2000-2025, bounded %)

206 countries, 26 year positions (2000-2025), 5 replicates, seed 0.

UIS modelled out-of-school rate (ROFST.MOD.2). Bounded in [0, 100]; a rate whose long gaps are the ones that matter most for the child-labour work.

MAE by method and gap length:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 0.275 | 0.334 | 0.733 | 0.545 | 1.685 |
| loglinear | 0.273 | 0.349 | 0.714 | 0.482 | 1.641 |
| scurve | 2.304 | 1.773 | 2.777 | 1.238 | 3.066 |
| kalman | 0.188 | 0.238 | 0.548 | 0.431 | 1.364 |

RMSE by method and gap length:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 0.707 | 0.667 | 1.240 | 0.850 | 2.333 |
| loglinear | 0.704 | 0.722 | 1.236 | 0.769 | 2.218 |
| scurve | 3.814 | 2.898 | 4.279 | 1.865 | 4.242 |
| kalman | 0.642 | 0.563 | 1.236 | 0.704 | 2.086 |

Scored points per cell:

| method | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|
| linear | 300 | 300 | 300 | 300 | 300 |
| loglinear | 300 | 300 | 300 | 300 | 300 |
| scurve | 300 | 300 | 300 | 300 | 300 |
| kalman | 300 | 300 | 300 | 300 | 300 |

Interval coverage (nominal 90%):

| method | nominal | gap 1y | gap 2y | gap 3y | gap 5y | gap 10y |
|---|---:|---:|---:|---:|---:|---:|
| kalman | 0.90 | 0.980 | 0.970 | 0.923 | 0.977 | 0.893 |

Best method at the longest gap: `kalman` (MAE 1.364).

## Reading the tables

- Long gaps should be harder than short ones on average, and the tests check 1- and 2-year gaps against 10-year gaps. Adjacent lengths can cross in a table (3 vs 5 years) because the blocks are randomly placed and some episodes are simply unforecastable; that is sampling noise in the hold-out, not a bug.
- Linear/log-linear rungs are strong on short gaps of smooth series; the S-curve and state-space rungs are for bounded or noisy series, and the state-space rung is the one that supplies honest intervals.
- The multiple-imputation rung borrows the year cross-section from other countries; it can beat univariate interpolation when a country has a long gap while the world moves (the common year factor is observable from the other countries), but it is not guaranteed to win on every series: the tables show where it does and does not.
- Interval coverage is only as honest as the model. The 90% state-space intervals are near nominal on the smooth PWT/attainment series; where they are too wide or too narrow, that is a finding about the model, not something to tune away.

