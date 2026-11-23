# E1: does fertility respond to the LEVEL of child mortality or to its VOLATILITY?

Worker `un-data`, branch `research/level-volatility-2026-11-23`, 23 Nov 2026. Box2 only (`ssh autodl2`),
working directory `/root/work/level_vol`. Design pre-registered in
`research/records/2026-11-23-mechanisms/EXPERIMENTS.md` (E1). Scripts + outputs in `scripts/`, `data/`, `results/`.

**Short answer.** Fertility responds to the **slow level** of child mortality, not to its short-run volatility.
The level effect is +0.0067 births per woman per point of child mortality with country trends (standard error
0.0015; 7,531 country-years, 193 countries) and is unchanged when volatility is added. The volatility coefficient is
−0.0022 (0.0038) — indistinguishable from zero, and the design would have detected a volatility effect as large as
the level effect (MDE 0.0108). This favours replacement / quantity-quality stories over a pure insurance-against-risk
story at country level — but **common cause is not excluded**, and a country-level null does not rule out household
insurance.

## What was run (and how it deviates from the pre-registered design)

For every country and year t: fit a straight line to under-five mortality over the trailing ten years (t−9…t, past
data only, no look-ahead), take the fitted value at t as the **level** and the standard deviation of the residuals as
**volatility**. Then run the project's within-country lead-lag estimator: ten-year change in births per woman on the
starting value of the mortality measure, with country effects, decade effects, income logged, urbanisation controlled,
country-clustered errors, with and without a straight-line country trend. Level, volatility and both enter as separate
specifications; 7,531-7,533 country-years, 193-194 countries, 6 decades.

Deviations from `EXPERIMENTS.md` E1, all recorded: (i) start years are **annual** (the matrix convention), not a
5-year grid; (ii) the trailing window is 10 years (E1 allowed 5-10); (iii) two secondary specifications were added —
the most recent transitory shock, and relative volatility (SD/mean); (iv) the country placebo was run two ways because
the first way is invalid (see below); (v) only the observed panel (`/root/work/data`) was used — no imputed or gap-filled
rows — which also satisfies the "observed cells only" check.

## (1) Fertility

Outcome: ten-year change in births per woman. Numbers are coefficient (standard error); * means |t|>1.96.

| specification | country effects | with country trends |
|---|---|---|
| level only | +0.0072 (0.0007)* | +0.0067 (0.0015)* |
| volatility only | +0.0020 (0.0023) | +0.0020 (0.0020) |
| level and volatility | level +0.0073 (0.0007)*; vol −0.0027 (0.0035) | level +0.0070 (0.0017)*; vol −0.0022 (0.0038) |
| recent shock only | −0.0012 (0.0010) | −0.0002 (0.0008) |
| relative volatility only | −0.0119 (0.0262) | +0.0132 (0.0297) |

**The level effect is the finding and it replicates the matrix**: the matrix's raw child-mortality link is
+0.0060 ± 0.0011 (8,567 country-years, 193 countries); here, using a smoothed trailing-average level, it is
+0.0067 ± 0.0015. Volatility adds nothing: its coefficient is small, and its sign even flips between specifications.

**Power / minimum detectable effect** (2.802 × standard error, 80% power at 95%): level 0.0046 in the joint model;
volatility 0.0108 in the joint model and 0.0056 in the volatility-only model; recent shock 0.0023. So a volatility
effect as large as the level effect (0.007) would have been detected; an effect half that size would not. Level and
volatility are only mildly collinear (correlation 0.29), so the joint model can separate them.

**Tests designed to kill the level result.**
1. *Circular-shift permutation within country* (200 draws; the only permutation used — no year-shuffle): level
   |b| = 0.0070 against a shuffled null 95th percentile of 0.0008, **p<0.005**. Volatility: p=0.29.
2. *Country placebo for volatility, whole-series swap* (200 draws): each country receives another country's complete
   volatility path, preserving within-country structure and clustering. The volatility |b| = 0.0022 sits inside that
   null (95th percentile 0.0031, **p=0.12**) — consistent with no effect. A first, naive placebo that scrambles
   volatility *values* across countries gave p<0.005, but it is **invalid** here: scrambling values breaks the
   within-country clustering that the clustered standard error is built on, so its null is far too tight (95th
   percentile 0.0006 against a clustered standard error of 0.0038). It is reported only as a methodological lesson.
3. *Observed rows only*: the observed panel was used throughout (no gap-filled rows).
4. The recent-shock coefficient is null, so sudden jumps in mortality do not predict later fertility changes in this
   design — only the persistent level does.

**What a level-only result favours, plainly.** Replacement (parents replace lost children), quantity-quality/human
capital (fewer survivors needed; higher return per survivor), and a level-based life-history response all predict a
level effect with no volatility effect. Insurance/uncertainty predicts the opposite pattern (a volatility effect), so
it is **disfavoured as the country-level driver**. Two honest limits: (a) a **common third factor** (development,
public health, state capacity) also predicts exactly this level-only pattern, so this experiment cannot separate
replacement from common cause — that needs exogenous mortality shocks (E4) or health-technology instruments (E7);
(b) a country-level null on volatility does **not** rule out household insurance: this is an aggregate proxy,
volatility measured from modelled national mortality, and the MDE (0.011) means a modest insurance channel would be
missed.

**What would change our mind.** A volatility coefficient above about 0.011 births per unit of volatility (significant
in the joint model) would resurrect the insurance/uncertainty channel; conversely, a level coefficient that
collapses when state capacity is controlled would favour common cause over replacement.

## (2) Massification

This does not change the schooling story. The survival-fertility association is a **level** phenomenon in child
mortality, which leaves the existing results intact: schooling → fertility is null with country trends, and the
survival links remain the dominant country-level predictors of births. What E1 does is narrow the mechanism from
"survival risk" to "survival level" — it is silent on whether schooling is a co-traveller of that level or a channel
through which it operates (the quantity-quality interaction, E5, is the test for that and is underpowered in the
current panel).

## Files, and what this cannot say

`scripts/level_vol.py` (decomposition, specifications, circular-shift permutation, MDEs), `scripts/placebo_fix.py`
(naive value-scramble placebo, reported as invalid), `scripts/placebo_swap.py` (cluster-preserving whole-series
placebo), `data/level_vol.json`, `data/placebo_variance_matched.json`, `data/placebo_swap.json`, `results/logs/`.
Decomposition is a country-level proxy built from modelled national mortality, not observed household risk; no causal
claim beyond the within-country design; common cause and replacement remain inseparable at this level. No imputed data
used; no box1 use.
