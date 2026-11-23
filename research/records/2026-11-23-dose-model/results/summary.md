## Recovery (synthetic data from known parameters)

| data from | fitted as | best distance | parameter: truth [5%, 50%, 95% of fit] |
|---|---|---|---|
| A | A | 3.38 | th_k: 2.20 [2.23, 2.28, 2.33]; th_f: 2.50 [2.21, 2.34, 2.48]; kappa: 1.00 [1.81, 1.82, 1.83]; gam: 3.00 [0.93, 0.93, 0.93]; lam_s: 2.00 [3.77, 3.77, 3.77] |
| A | B | 4.83 | th_k: 2.20 [1.70, 3.95, 4.00]; th_f: 2.50 [0.37, 0.46, 0.46]; gam: 3.00 [3.98, 3.99, 5.35]; lam_s: 2.00 [3.92, 4.23, 4.23] |
| B | A | 4.97 | th_k: 2.20 [1.58, 4.10, 4.13]; th_f: 2.50 [1.27, 1.27, 2.20]; kappa: 0.00 [0.62, 0.85, 1.03]; gam: 3.00 [0.46, 0.47, 1.35]; lam_s: 2.00 [1.88, 1.88, 2.81] |
| B | B | 2.83 | th_k: 2.20 [0.98, 3.67, 4.01]; th_f: 2.50 [3.45, 4.12, 4.89]; gam: 3.00 [0.29, 0.96, 4.04]; lam_s: 2.00 [0.28, 2.01, 2.16] |

## Real-data posterior (final population)

Scenario A: best in-sample distance 9.62, median 12.75

- th_k: median 3.43  90% [0.02, 4.99]  posterior/prior sd 1.28
- th_f: median 1.62  90% [0.03, 4.92]  posterior/prior sd 1.20
- kappa: median 0.31  90% [0.01, 1.98]  posterior/prior sd 0.77
- gam: median 7.25  90% [5.27, 7.99]  posterior/prior sd 0.39
- lam_s: median 2.59  90% [0.03, 4.90]  posterior/prior sd 1.23

Scenario B: best in-sample distance 12.75, median 14.73

- th_k: median 2.70  90% [0.16, 4.90]  posterior/prior sd 1.13
- th_f: median 0.89  90% [0.05, 3.63]  posterior/prior sd 0.80
- kappa: median 2.34  90% [0.11, 2.98]  posterior/prior sd 1.15
- gam: median 7.37  90% [5.78, 7.89]  posterior/prior sd 0.29
- lam_s: median 2.94  90% [0.91, 4.46]  posterior/prior sd 0.73

## Held-out
mean D A 16.8 vs B 19.9; diff -3.1 (95% [-9.4, 3.1]); A better in 4/6; ensemble TFR RMSE {'A': 1.1751065878639342, 'B': 1.7039286095060586}

| country | D_A | D_B |
|---|---|---|
| KOR | 8.5 | 2.7 |
| MYS | 9.4 | 10.1 |
| KEN | 50.6 | 60.4 |
| BRA | 8.2 | 15.3 |
| TUR | 15.8 | 7.7 |
| MEX | 8.2 | 23.1 |

Decomposition A (fit countries), births per woman lost, 1940 -> 1980 cohort: none/some primary: quantum -0.24, tempo 0.04; primary: quantum 0.11, tempo -0.08; lower secondary: quantum 0.22, tempo -0.05; upper secondary: quantum 0.18, tempo -0.02; tertiary: quantum 0.23, tempo -0.06; national: quantum 1.42, tempo -0.24

Decomposition A (holdout countries), births per woman lost, 1940 -> 1980 cohort: none/some primary: quantum 0.00, tempo -0.04; primary: quantum 0.03, tempo -0.03; lower secondary: quantum 0.33, tempo -0.07; upper secondary: quantum 0.10, tempo 0.01; tertiary: quantum 0.03, tempo 0.03; national: quantum 1.60, tempo -0.25

Decomposition B (fit countries), births per woman lost, 1940 -> 1980 cohort: none/some primary: quantum 0.77, tempo -0.22; primary: quantum 0.51, tempo -0.19; lower secondary: quantum 0.45, tempo -0.12; upper secondary: quantum 0.35, tempo -0.10; tertiary: quantum 0.36, tempo -0.07; national: quantum 1.36, tempo -0.16

Decomposition B (holdout countries), births per woman lost, 1940 -> 1980 cohort: none/some primary: quantum -0.03, tempo -0.00; primary: quantum 0.06, tempo 0.05; lower secondary: quantum 0.18, tempo 0.10; upper secondary: quantum -0.02, tempo 0.14; tertiary: quantum 0.10, tempo 0.18; national: quantum 0.86, tempo 0.09