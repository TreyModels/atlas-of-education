# v6_phl results: Philippine demand experiment (amendment to the v5 results paper)

**Date:** 2026-11-22. **Protocol:** `PROTOCOL_v6_phl.md`, with Amendment A1 (dated, written before any held-out scoring). **Status: not calibrated.** The test is retrospective and inspected, not blind.

This is a new experiment, not a confirmation of v5. The v5 results (`outputs/PHL/v5/`, `PROTOCOL_v5.md`) are unchanged and remain the record of v5.

## 1. Losses first

Error is the held-out root-mean-square error (RMSE) across the three gross enrolment ratios (GER): primary, secondary and tertiary, post-1995. Lower is better.

| Model | Held-out 3-GER RMSE | Behavioural dials on a bound |
|---|---|---|
| **Persistence (carry 1995 forward)** | **6.600** | n/a |
| P2_con: returns + bounded positional pull + cost (registered winner) | 6.854 | `b_h` (=0), `eta_x` (=0) |
| P2_unc | 6.855 | `b_h` (=−6) |
| P1_unc | 7.434 | `b_h` (=−6), `eta_x` (=0) |
| v5 R2 (earlier experiment) | 7.458 | `b_h` (=−6) |
| P1_con | 8.573 | `b_h` (=0), `eta_x` (=0) |
| P3_con: P2 + cost falls with saturation | 9.460 | none (`nu_basic` 7.998, within 0.002 of its bound) |
| Linear trend | 11.794 | n/a |
| P0: income + cost benchmark | 14.226 | `eta` (=6) |
| v5 R0 | 14.230 | — |
| *A1: P0 + returns, b_h ≥ 0* | *14.228* | `eta`, `b_h` (=0) |
| *A1: P0 + returns, unconstrained* | *14.179* | `eta`, `b_h` (=−6) |

**No structural model beats persistence.** By the stopping rule the status stays **not calibrated**. No countries, tutoring or feedback loops are added to rescue it.

By level, the registered winner (P2_con) beats persistence on secondary (RMSE 4.1 against 7.8) and loses on primary (6.6 against 4.7) and tertiary (8.8 against 6.9). The P1 runs fit tertiary best (3.6–4.0). No single specification wins all three levels.

## 2. Sign tests (constrained against unconstrained)

- **Measured returns to schooling: the sign is not identified.** From the default start, every run puts `b_h` on a bound: 0 when constrained, −6 when unconstrained. This holds across P1, P2, the A1 nested pair and v5. Forcing the sign costs +1.14 RMSE in P1 and +0.00 in P2. In the clean A1 comparison, adding returns to the income + cost benchmark does not help (14.23 and 14.18 against 14.23).
  **But one random restart (§5) found a better training fit with large positive returns** (`b_h` = 11.8, near its upper bound of 12): training cost 231.5 against 314.6. That fit forecasts much worse: held-out RMSE 11.1 against 6.85. So the training years cannot settle the sign. The solution that forecasts better is the one where measured returns play no part. The fair statement is "not identified, and positive returns do not help prediction", not "returns are negative".
- **The rich–poor income gradient (`eta_x`) sits at 0 in every run except P0.** As in v3, the cross-sectional gradient comes from costs.
- **National income growth (`eta`) hits its upper bound in P0** and then overshoots out of sample: tertiary GER reaches 79% in 2024, against 47% observed.

## 3. Separating observations

Following A1.5, "every rival" includes persistence and trend wherever they give a prediction.

| Observation | Observed | Lowest error | Notes |
|---|---|---|---|
| Tertiary GER 2013 and 2024 (premium falling) | 31.9, 47.4 | P1_unc (3.09) | beats trend (5.24) and persistence (14.78); but P1_unc's returns dial is at −6 (wrong sign, on bound) |
| Secondary GER 1998 (recession) | 70.5 | P2_con (2.76) | beats persistence (4.34) and trend (8.67) |
| Grade 10→11 transition 2018 | 93.3% | P2_unc (2.71) | `b_h` = −6 on bound |
| CHED tertiary index 2016–20 (provisional source) | — | all within 0.14–0.18 | does not separate |

**No mechanism is called supported.** P2_con wins the recession observation. But the selection rule requires the overall winner to stand against the benchmarks, and it loses to persistence. The other two wins belong to runs whose returns dial sits on its wrong-sign bound.

## 4. Recovery test (P2_con; 20 synthetic replicates, v5 noise design)

| Dial | True value | Median recovered | Within ±25% | Bound hits | Label |
|---|---|---|---|---|---|
| `b_p` (positional pull) | 4.66 | 4.52 | 20/20 | 0 | identified (software diagnostic only) |
| `kappa` (cost sensitivity) | 2.92 | 2.72 | 15/20 | 0 | not identified (75% < 80%) |
| `b_h` (returns) | 0 | 0 | — | 16/20 | **boundary-censored / not cleanly identified** |
| `eta_x` (income gradient) | 0 | 0.02 | — | 10/20 | **boundary-censored / not cleanly identified** |

Each replicate starts at the true values, which makes this a generous test. That matters given §5: from random starts, the same model reaches very different optima. `b_p` recovering is a software result only. It is not evidence for positional demand: lagged enrolment saturation trends upward, and the protocol has no rival that separates it from momentum or diffusion.

## 5. Optimiser restarts (A1.3)

The registered P2_con fit (training cost 314.6) came from one start. Four random-start refits reached training costs of 3475.7, 3703.7, 335.5 and **231.5**. Seed 4 hit the 250-evaluation cap, so it had not converged.

Seed 4's parameters tell a different story: returns `b_h` = 11.8 (near its upper bound), positional pull `b_p` = 5.9, cost sensitivity `kappa` = 21.4. **Its held-out 3-GER RMSE is 11.1**, worse than the registered fit (6.85) and worse than persistence (6.60). Tertiary GER is 54% in 2013 against 31.9% observed.

Consequences:
1. The registered P2_con fit is **not the training optimum**. The fit surface has several modes.
2. The pre-registered rule selects on held-out error, so restarts do not change the registered result, and the better training optimum would score worse anyway.
3. No conclusion here relies on a single-start sign. That applies especially to the returns dial (§2).
4. Before any next experiment, use at least 10 starts and a higher evaluation cap as standard.

File: `multistart/P2_con_seed04_scores.json`.

## 6. Diagnosis: why the private shares fail (post-inspection, not eligible for selection)

The private-share repair failed. In the winner, primary private share has an RMSE of 18.7 against persistence's 0.8, and it misses even in training (16–19% fitted against 6–8% observed). Both private slopes (`nu_basic`, `nu_ter`) sit at their upper bound of 8.

A loss breakdown shows the cause. **Six household-spending rows (FIES 2003 and 2006) account for 62% of the training loss.** The two bottom-30% rows alone account for 47%: the model gives poor households about 3% of their budget spent on schooling, while FIES reports 1.3%.

Diagnostic A2 (`diag_A2_no_spending_rows.json`) refits P2_con without those rows:

- primary private share fits (held-out RMSE 1.8);
- `nu_basic` moves off its bound (0.27);
- training loss falls from 314.6 to 11.4;
- but the cost multiplier `c_scale` rises to 6.6, so modelled household spending becomes 16–24% of consumption, against 1–5% observed;
- held-out 3-GER RMSE is 7.54, still worse than persistence.

**Interpretation.** One parameter does two jobs: the same cost scale sets both what deters enrolment and what households are recorded as spending. Enrolment and sector choices behave as if schooling costs about six times the declared cash schedule. Measured cash spending says it doesn't. Either deterrence includes costs that are not cash outlays, which bears on Bray's full-cost argument, or the cost schedule or burden function is wrong. This experiment cannot tell which.

## 7. Illustrative declared-capacity diagnostic

`illustrative_capacity_diagnostic.json` is **illustrative only**. Its seat numbers are declared fractions of cohort size, not observed school supply. One oddity to check before using it: private seats fill exactly to capacity at every level while public seats have vacancies. That pattern may come from the allocator's priority order rather than from behaviour.

## 8. Measurements needed for a stronger test

1. **A cost input that separates cash from non-cash costs.** For example, FIES spending by enrolment status and level, plus a separate measured indirect-cost or distance series. Then pre-register a spec where deterrence and recorded spending have separate scales.
2. **Decile-level FIES education spending for more years.** This would replace two bottom-30% points carrying half the loss.
3. **Historical public and private seat counts** (DepEd BEIS classrooms, CHED institutional capacity), so capacity can be tested rather than declared.
4. **A rival that separates positional pull from momentum.** For example, a diffusion S-curve driven by measured exposure, or lagged enrolment from other countries.
5. **A comparable wage-premium series across 1995–2013** (the current series mixes methods and is interpolated), before returns are tested again.

## Files

- Fits: `fit_P0.json`, `fit_P1_con.json`, `fit_P1_unc.json`, `fit_P2_con.json`, `fit_P2_unc.json`, `fit_P3_con.json`, plus the A1 fits `fit_P0h_con.json` and `fit_P0h_unc.json`. Each holds bounds hit, optimiser status and its message.
- Scores: `scores.json` (registered), `scores_amendA1.json`.
- Recovery: `recovery_P2_con.json`, `recovery_reps/`.
- Restarts: `multistart/`.
- Diagnostics: `diag_A2_no_spending_rows.json`, `illustrative_capacity_diagnostic.json`.
- Figures: `figures/fig1_fit_and_test.png`, `figures/fig2_rivals_and_private_repair.png`.
- Hashes and environment: `reproducibility_hashes.json`.
- P3_con, the A1 runs, scoring, recovery and A2 were run in a Linux workspace (Python 3.13, numpy 2.5.3, scipy 1.18.1). P0–P2 were run earlier on the Mac.
