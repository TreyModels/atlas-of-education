# MASSENG Philippine v5 rival results

## PHL v5 — retrospective rival test

**Losses first. Status: not calibrated. This was a retrospective, inspected test, not a blind validation.**

The pre-registered winner is **R2**, with three-GER held-out RMSE **7.458**. R0 is **14.230**, persistence **6.600**, and linear trend **11.794**. Lower is better; selection uses the three GERs only, not training cost.

| rival | three-GER RMSE | minus R0 | persistence | trend | training cost | evaluations | at bounds |
|---|---:|---:|---:|---:|---:|---:|---|
| R0 | 14.230 | 0.000 | 6.600 | 11.794 | 171.173 | 77 | nu, eta |
| R1 | 16.925 | 2.695 | 6.600 | 11.794 | 105.258 | 573 | none |
| R2 | 7.458 | -6.771 | 6.600 | 11.794 | 382.875 | 82 | eta_x, nu, b_h |
| R3 | 15.184 | 0.955 | 6.600 | 11.794 | 160.465 | 49 | none |
| R4 | 12.194 | -2.036 | 6.600 | 11.794 | 110.426 | 278 | none |
| R5 | 16.543 | 2.314 | 6.600 | 11.794 | 135.706 | 88 | none |

**Benchmark failure:** R2 does not beat the best naive rule on the three GERs. Its selection among rivals is not forecasting validation.
**Mechanism warning:** R2's fitted `b_h` is -6.000 and hits a bound. It therefore does not estimate a positive human-capital effect; its lower RMSE must not be presented as support for the earnings-return account.
Bound-hitting estimates are reported as computational/red-flag results, not clean structural measurements.

### Held-out losses for the selected rival

| series | n | model | R0 | persistence | trend |
|---|---:|---:|---:|---:|---:|
| edu_share_hh | 1 | 0.343 | 1.107 | — | — |
| enrol_tertiary | 5 | 0.182 | 0.155 | — | — |
| ger_primary | 25 | 5.874 | 7.440 | 4.737 | 10.873 |
| ger_secondary | 24 | 11.130 | 13.049 | 7.793 | 16.762 |
| ger_tertiary | 26 | 3.597 | 19.331 | 6.930 | 5.311 |
| hh_share_total_spending | 6 | 7.363 | 6.659 | — | — |
| ner_primary | 16 | 4.708 | 4.807 | 3.653 | 4.632 |
| ner_secondary | 14 | 8.354 | 5.693 | 5.114 | 8.264 |
| priv_lower_secondary | 1 | 36.406 | 17.908 | — | — |
| priv_primary | 21 | 19.640 | 13.693 | 0.780 | 0.631 |
| priv_secondary | 17 | 19.016 | 7.289 | — | — |
| priv_tertiary | 6 | 37.982 | 17.297 | 23.552 | 23.552 |
| priv_upper_secondary | 1 | 22.046 | 5.929 | — | — |
| trans_lsec_usec | 1 | 5.288 | 6.190 | — | — |

### Separating observations

The protocol pairs tertiary GER in 2013 and 2024 with a college-premium fall from 0.88 to 0.59 log points. The table reports model predictions against the held-out GER observations; it does not infer causation from the timing.

| rival | tertiary GER 2013 | tertiary GER 2024 | Grade 10→11, 2018 |
|---|---:|---:|---:|
| R0 | 56.075 | 79.167 | 99.490 |
| R1 | 64.743 | 76.242 | 100.000 |
| R2 | 34.633 | 44.005 | 88.012 |
| R3 | 56.186 | 80.090 | 99.917 |
| R4 | 57.585 | 68.248 | 94.222 |
| R5 | 61.073 | 80.807 | 99.982 |
| **observed** | **31.870** | **47.413** | **93.300** |

Recession secondary GER predictions (observations, where available, remain in `scores.json`):

| rival | 1984 | 1985 | 1986 | 1998 |
|---|---:|---:|---:|---:|
| R0 | 64.517 | 56.153 | 53.578 | 63.289 |
| R1 | 57.620 | 58.564 | 59.560 | 74.774 |
| R2 | 60.229 | 59.242 | 58.907 | 62.956 |
| R3 | 57.987 | 58.488 | 59.540 | 71.280 |
| R4 | 60.999 | 61.948 | 62.930 | 69.171 |
| R5 | 57.416 | 57.878 | 58.815 | 71.577 |

### Separating-test decisions

| test | observed years | lowest-error rival | RMSE |
|---|---|---|---:|
| tertiary_2013_2024 | 2013, 2024 | R2 | 3.102 |
| recession_secondary | 1998 | R3 | 0.772 |
| grade10_to_grade11_2018 | 2018 | R4 | 0.922 |

### K-12 recovery: CHED tertiary headcount index (2016 = 1)

| year | observed | R0 | R1 | R2 | R3 | R4 | R5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2016 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 2017 | 0.874 | 0.782 | 0.784 | 0.772 | 0.799 | 0.787 | 0.789 |
| 2018 | 0.726 | 0.559 | 0.557 | 0.552 | 0.589 | 0.566 | 0.573 |
| 2019 | 0.783 | 0.593 | 0.569 | 0.562 | 0.630 | 0.571 | 0.604 |
| 2020 | 0.830 | 0.613 | 0.584 | 0.556 | 0.665 | 0.576 | 0.632 |

### FIES household education spending share

| year | observed | R0 | R1 | R2 | R3 | R4 | R5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2012 | 4.100 | 5.207 | 4.973 | 4.443 | 4.850 | 5.027 | 4.949 |

### PIDS NTA household share of total education spending

| year | observed | R0 | R1 | R2 | R3 | R4 | R5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1991 | 47.000 | 51.228 | 48.737 | 51.847 | 50.307 | 50.994 | 50.377 |
| 1994 | 55.000 | 47.371 | 46.110 | 47.600 | 46.749 | 47.659 | 47.032 |
| 1998 | 51.000 | 39.778 | 39.241 | 39.515 | 39.346 | 40.263 | 39.619 |
| 2002 | 55.000 | 47.334 | 47.546 | 46.426 | 46.957 | 47.909 | 47.296 |
| 2007 | 58.000 | 55.901 | 55.343 | 53.342 | 54.796 | 55.473 | 55.152 |
| 2010 | 59.000 | 58.065 | 57.072 | 54.539 | 56.443 | 57.232 | 56.845 |

### Protocol and interpretation limits

- Protocol amendments: none.
- Post-1995 enrolment was not fitted. The explicitly registered FIES and APIS training exceptions were retained.
- Unverified FIES 2023 was excluded. The DepEd transition is reference year 2018 (SY2017–18), not 2017.
- PHL premiums mix methods and interpolate 1995–2013. The relational driver is wage/salary employment (`formal_share`), not a spliced occupation series.
- The occupational-threshold driver is exogenous here; aggregate timing cannot identify whether requirements drove enrolment or enrolment drove requirements.
- These are model comparisons, not proof of the relational account or causal estimates of policy effects.

### Synthetic recovery on the selected rival

Declared Gaussian noise; 20 replicates. A parameter passes only if at least 80% of recoveries fall within ±25% of a nonzero truth.

Optimiser-cap replicates: 0.

| parameter | truth | median | 5th–95th percentile | share within ±25% | bound-hit replicates | status |
|---|---:|---:|---:|---:|---:|---|
| b_h | -6.000 | -6.000 | -6.000 to -4.468 | 0.95 | 15 | **identified** |
| b_p | — | — | — | — | — | not in rival |
| kappa | 1.865 | 1.707 | 0.949 to 2.464 | 0.60 | 0 | **not identified** |

