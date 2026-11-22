# Protocol kiss_phl: enrolment-only, many-model test (Philippines)

**Timing, stated honestly.** The design below was fixed in `scripts/kiss_ensemble.py` before any KISS fit ran: specs, targets, metric, ensemble members and blend weights. This text was written on 2026-11-22 at about 15:05 CST, after two smoke-test fits were scored (K0 seed 0 and K1 seed 1). Nothing in the design was changed after that.

**Status:** retrospective and inspected. Every post-1995 Philippine number has been seen in earlier versions. This is a new experiment and does not replace v5 or v6_phl.

## Why this exists

v6_phl tried to fit enrolment, private shares and household spending together. Six spending rows carried 62% of the loss, and private-share targets pinned the sector parameters on their bounds. The research question is enrolment. This run fits only enrolment and asks two things: whether several simple models beat carrying last year forward, and whether combining them helps.

## Targets

- **Training (≤1995):** primary, secondary and tertiary GER; primary NER.
- **Held-out (post-1995):**
  - *Primary metric:* pooled RMSE over primary NER, secondary NER and tertiary GER. Tertiary has no NER series.
  - *Also reported:* primary and secondary GER.
- **Dropped:** private shares, household spending, rich/poor participation ratios.

## Models (Page: many simple models side by side)

| Name | What it says | Fitted behavioural settings |
|---|---|---|
| K0 | Enrolment follows national income and household cost | `eta`, `kappa` |
| K1 | K0 + positional pull (lagged enrolment saturation, bounded) | `eta`, `kappa`, `b_p` ≥ 0 |
| K2 | K0 + measured returns (wage premium) | `eta`, `kappa`, `b_h` ≥ 0 |
| logistic | Diffusion: one S-curve per series, fitted on training years only (the world-society rival) | 3 per series |
| persistence | Carry the last training value forward | — |
| trend | Linear trend over the training window | — |

- **Level adjustments, fitted for K0–K2:** the five entry and continuation intercepts.
- **Fixed, not fitted:** cost scale = 1 (the declared cash schedule), rich/poor income gradient = 0, private-sector settings at their defaults, all demography and policy dates as in v5.
- **Bounds:** as in v6_phl.
- **Starts:** 10 per spec (seed 0 = default start, seeds 1–9 uniform random within bounds). The best training cost is kept. All start costs are reported.

## Combinations, with weights fixed in advance

- **Page ensemble:** equal-weight mean of K0, K1, K2 and logistic.
- **Silver blend:** 0.5 × persistence + 0.5 × Page ensemble.

## Decision rules

1. Rank every model by the primary metric. Report losses first.
2. A model or combination "beats the naive benchmark" only if it beats **both** persistence and trend on the primary metric.
3. A mechanism is "supported" only if its spec beats K0 **and** logistic on the primary metric, with its dial off its bounds. Beating persistence alone is not enough.
4. **Monte Carlo** (parameter uncertainty only): 300 draws from the Gauss–Newton covariance at the best fit. Report the share of held-out observations inside the 90% band. These bands ignore uncertainty about the model's structure, so they will be too narrow if the model is wrong.
5. **Not done here:** a recovery test. That is next if anything is supported.

## Known limits

- Secondary NER has only 4 points before 1996 (diagnostic rows). It is tested, never trained on. The logistic and benchmark models use those 4 points.
- Not blind: the designer has seen the Philippine series many times.
