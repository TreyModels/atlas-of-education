# Binding-gate experiment (SIMULATION ONLY)

## Per-arm summary
| arm | rows | mean Q5-Q1 tut gap | E8 gap effect (fee .19 vs .00) | E8 gate-fail effect |
|---|---|---|---|---|
| bar_high | 60 | 0.2308 | -0.2076 | -0.0373 |
| share_0.25 | 60 | 0.4419 | -0.0544 | -0.0133 |
| share_0.35 | 60 | 0.4349 | -0.0603 | -0.0182 |
| share_0.45 | 60 | 0.4238 | -0.0615 | -0.0196 |
| share_0.55 | 60 | 0.3969 | -0.0693 | -0.0202 |
| share_0.70 | 60 | 0.3426 | -0.0583 | -0.0112 |

## H2 (primary, pre-registered)
- interaction = E8 effect at S=0.25 minus S=0.7: **+0.0039** (se≈0.0119, 95% CI [-0.01943949435301321, 0.02731402438747379])
- verdict: **UNDERPOWERED**

## H1
- mean tut gap by share: S=0.25: 0.4419, S=0.35: 0.4349, S=0.45: 0.4238, S=0.55: 0.3969, S=0.7: 0.3426
- Spearman rho -1.000; gap(S_lo)-gap(S_hi) +0.0993
- verdict: **SUPPORTED**
