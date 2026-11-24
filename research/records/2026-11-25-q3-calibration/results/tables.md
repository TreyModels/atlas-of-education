### Table 1. Known-truth calibration, main regimes (400 independent replicates each, R = 400 draws)

| regime | ROBUST+H | ROBUST-HET | ROBUST-but-GROUP | GROUP | BEATS | NONE | key error rate |
|---|---|---|---|---|---|---|---|
| R0 null | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 0.2% [0.0, 1.4] | 4.0% [2.5, 6.4] | 95.8% [93.3, 97.3] | false-positive **4.2%** [2.7, 6.7] |
| R1 uniform strong (b=0.15) | 95.5% [93.0, 97.1] | 1.0% [0.4, 2.5] | 1.0% [0.4, 2.5] | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 2.5% [1.4, 4.5] | false-negative **2.5%** [1.4, 4.5] |
| R3 minority-only (b=0.40, top third) | 48.2% [43.4, 53.1] | 0.0% [0.0, 1.0] | 38.8% [34.1, 43.6] | 3.2% [1.9, 5.5] | 0.0% [0.0, 1.0] | 9.8% [7.2, 13.1] | planted tag flagged **42.0%** [37.3, 46.9]; false-ROBUST 48.2% [43.4, 53.1] |
| R4 shared country trends (no effect) | 0.2% [0.0, 1.4] | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 1.8% [0.9, 3.6] | 3.0% [1.7, 5.2] | 95.0% [92.4, 96.7] | false-positive **5.0%** [3.3, 7.6] |
| R5 sign-split (+/-0.25) | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 3.2% [1.9, 5.5] | 64.5% [59.7, 69.0] | 32.2% [27.9, 37.0] | descriptive (truth is sign-ambiguous) |

### Table 2. Uniform-effect strength ladder (400 replicates per strength)

| b (per country) | ROBUST+H (strict) [95% CI] | any-robust (ROBUST+H + ROBUST-but-GROUP) [95% CI] | NONE (false negative) [95% CI] |
|---|---|---|---|
| 0.02 | 0.2% [0.0, 1.4] | 0.2% [0.0, 1.4] | 97.2% [95.1, 98.5] |
| 0.04 | 3.8% [2.3, 6.1] | 3.8% [2.3, 6.1] | 93.5% [90.6, 95.5] |
| 0.06 | 19.0% [15.5, 23.1] | 19.2% [15.7, 23.4] | 78.5% [74.2, 82.2] |
| 0.1 | 60.0% [55.1, 64.7] | 60.5% [55.6, 65.2] | 37.2% [32.7, 42.1] |
| 0.15 | 95.0% [92.4, 96.7] | 95.8% [93.3, 97.3] | 3.0% [1.7, 5.2] |
| 0.25 | 97.5% [95.5, 98.6] | 98.5% [96.8, 99.3] | 0.0% [0.0, 1.0] |

Canonical source: `results/calibration.json` -> `strength_ladder[b].ROBUST+H_rate` (strict), `strength_ladder[b].correct_robust_rate` (any-robust), `strength_ladder[b].false_negative_rate`.

### Table 3. Design-size grid (200 replicates per cell): Monte Carlo intervals are in Table 1; here the spread is across sample/mechanism cells

| regime | N | T | R | key rate [95% CI] |
|---|---|---|---|---|
| C | 80 | 50 | 400 | FP 3.0% [1.4, 6.4] |
| C | 150 | 30 | 400 | FP 4.0% [2.0, 7.7] |
| C | 150 | 50 | 400 | FP 2.0% [0.8, 5.0] |
| C | 150 | 60 | 400 | FP 4.5% [2.4, 8.3] |
| C | 220 | 50 | 400 | FP 5.0% [2.7, 9.0] |
| U | 80 | 50 | 400 | any-robust 3.0% [1.4, 6.4] (strict ROBUST+H 3.0%) |
| U | 150 | 30 | 400 | any-robust 10.5% [7.0, 15.5] (strict ROBUST+H 10.5%) |
| U | 150 | 50 | 400 | any-robust 11.0% [7.4, 16.1] (strict ROBUST+H 11.0%) |
| U | 150 | 60 | 400 | any-robust 11.0% [7.4, 16.1] (strict ROBUST+H 11.0%) |
| U | 220 | 50 | 400 | any-robust 28.0% [22.2, 34.6] (strict ROBUST+H 28.0%) |
| B | 80 | 50 | 400 | tag hit 37.5% [31.1, 44.4]; false-ROBUST combined 27.5% (strict ROBUST+H 26.5%) |
| B | 150 | 30 | 400 | tag hit 54.5% [47.6, 61.3]; false-ROBUST combined 38.5% (strict ROBUST+H 38.5%) |
| B | 150 | 50 | 400 | tag hit 38.0% [31.6, 44.9]; false-ROBUST combined 52.0% (strict ROBUST+H 52.0%) |
| B | 150 | 60 | 400 | tag hit 40.0% [33.5, 46.9]; false-ROBUST combined 38.0% (strict ROBUST+H 38.0%) |
| B | 220 | 50 | 400 | tag hit 42.0% [35.4, 48.9]; false-ROBUST combined 55.5% (strict ROBUST+H 55.5%) |

Canonical source: `results/calibration.json` -> `design_grid[cell].ROBUST+H_rate`, `.correct_robust_rate`, `.false_robust_everywhere_rate`, `.planted_tag_flagged_rate`.

### Table 4. Draw-count axis (200 replicates per cell)

| regime | R | key rate [95% CI] |
|---|---|---|
| C | 100 | FP 1.5% [0.5, 4.3] |
| C | 400 | FP 3.0% [1.4, 6.4] |
| U | 100 | any-robust 9.0% [5.8, 13.8] (strict ROBUST+H 9.0%) |
| U | 400 | any-robust 13.0% [9.0, 18.4] (strict ROBUST+H 13.0%) |

### Table 5. Full-vector BH and BY on the four real strict-tier families (272 links each)

| family | BH (m=272) | BY (m=272) | BH at m_eff=157 (approximation) | min p | links at floor |
|---|---|---|---|---|---|
| up | 35 | 0 | 44 | 0.00249 | 30 |
| down | 19 | 0 | 28 | 0.00249 | 19 |
| sign_flip | 15 | 0 | 27 | 0.00249 | 15 |
| heterogeneity | 53 | 0 | 56 | 0.00249 | 39 |

### Adequacy benchmarks (pre-registered)

| benchmark | observed | passed |
|---|---|---|
| null FP <= 5% with upper CI <= 10% | 4.2% [2.7, 6.7] | PASS |
| uniform-strong FN (NONE) <= 5% | 2.5% [1.4, 4.5] | PASS |
| minority planted-tag hit >= 80% | 42.0% [37.3, 46.9] | FAIL |
| minority false-ROBUST <= 10% | 48.2% [43.4, 53.1] | FAIL |
| shared-trend FP <= 5% | 5.0% [3.3, 7.6] | PASS |
