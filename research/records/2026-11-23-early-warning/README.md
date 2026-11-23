# Is the terminal enclosure a tipping point? Early-warning signals and diminishing returns (23 November 2026)

## What this tested, and the short answer
If "terminal enclosure" is a critical transition, the standard early-warning toolkit should see it coming:
rising variance and rising autocorrelation in the years before the transition, relative to periods that did not
end in one. **It does not.** Across 80 countries with a dated fertility transition, autocorrelation **falls**
before the event (the opposite of the prediction), variance rises slightly, and **neither signal survives the
surrogate null**. The diminishing-returns side is more positive: the marginal fertility effect of schooling
completion **does** weaken as the pipeline deepens, and it turns positive at the very top — but part of that is
the arithmetic floor, so it is not clean evidence for a ratchet.

The pre-registration is `PREREGISTRATION.md`, committed (`e12249b`) before any computation. All definitions,
placebos and decision rules below were fixed in it.

## (1) Fertility

### The event set, and the sample limitation that comes with it
Using the pre-registered rule (the first year of the fastest sustained ten-year fall, minimum 1.0 births),
**184 countries** have a transition event. Only **80** also have the 15-year pre-event window inside their
observed annual series, because the World Bank fertility series mostly starts in 1960 and for 105 countries the
transition begins at the first observation. That restriction is a real limitation and it biases the sample
towards later transitioners; it is a data-availability fact, not a modelling choice.

### Early-warning signals: event minus pseudo-event
For each event country, the same measures were computed at 200 pseudo-event dates drawn from its own series
(never within ten years of the real event), and the comparison is paired within country (n = 80):

| signal (trend across the pre-event window) | event minus pseudo-event | s.e. | t | predicted sign | verdict |
|---|---|---|---|---|---|
| lag-1 autocorrelation | **-0.025** | 0.008 | -3.3 | **rising** | **wrong sign** |
| variance | **+0.079** | 0.034 | +2.3 | rising | right sign, **fails the surrogate null** |
| skewness | -0.097 | 0.043 | -2.3 | (descriptive) | more negative before the event |
| autocorrelation level | +0.025 | 0.013 | +2.0 | rising | small, not robust |

**Surrogate null** (pre-registered): the pre-event window's first differences were reshuffled and
re-integrated 16,000 times. The share of surrogates with a trend at least as large as the observed one is
**0.57 for autocorrelation and 0.42 for variance** — so neither the autocorrelation decline nor the variance
rise is distinguishable from what the same series produces by chance. Per the pre-registered decision rule
the early-warning signal is **absent**.

**Placebo transitions were not usable**: only **1** country in the panel never had a ten-year fall of even
0.3 births, because fertility fell almost everywhere in the period covered. That placebo is reported as
unavailable rather than contrived.

**Power, stated honestly:** with the observed dispersion, the minimum detectable difference at 80% power is
**0.095 for the variance trend and 0.021 for the autocorrelation trend**. The variance effect found (0.079)
is *below* its own MDE, so this design could not reliably detect an effect of the size it estimates. The null
on variance is therefore weak evidence of absence; the null on autocorrelation is not weak, because the point
estimate has the wrong sign.

**Secondary event (schooling universalisation) is a data gap.** The universalisation timing file covers
**6 countries** (many thresholds censored or "unable"), far below the 25-country gate fixed in the
pre-registration, so that test is reported as unavailable rather than approximated.

### Diminishing returns to schooling: the one positive result
3,865 country-year observations, 238 countries, ten-year change in fertility on lower-secondary completion,
completion squared, and region fixed effects:

- the quadratic term is **positive: +0.00019 per squared point (t = 18.2)**, i.e. the response is convex, the
  decline gets weaker as completion rises;
- the marginal effect of one more point of completion is **-0.0099 births** at the 10th percentile of
  completion, **+0.0064** at the median, **+0.0214** at the 90th percentile, with bootstrap 95% intervals
  excluding zero at all three (-0.0116 to -0.0079; +0.0059 to +0.0070; +0.0199 to +0.0230);
- the turning point sits at **completion ≈ 39 of 100**, inside the observed range.

So the pre-registered pattern (decline weakening with depth, turning over at the top) is present and
precisely estimated. **But the honest reading is contaminated by arithmetic:** once fertility is near its
floor it cannot fall further, and post-transition fertility rebounds slightly. A concave response and a floor
look the same in this regression. The result is consistent with diminishing returns; it does not identify a
ratchet, and I do not claim it does.

## (2) Massification
The massification reading of this is narrow but useful. The *pipeline* stage does not show a visible
approaching-transition signature in the fertility series: whatever enclosure the theory describes, it is not
announced by the classic rising-variance/rising-autocorrelation pattern in the ten to twenty years before the
fall. What the schooling data do show is saturation: each further point of lower-secondary completion buys
less fertility decline, and beyond roughly 39 points of completion the marginal relationship turns positive.
That is consistent with the theory's "saturation" language and with earlier records' finding that the
massification channel slows as it deepens — but it is equally consistent with a mechanical floor, so it should
be quoted as a boundary condition on the schooling-fertility relation, not as a tipping point.

## Limits
Annual series that start in 1960 for most countries, so the pre-event window exists for 80 of 184 events and
the sample tilts late. The within-country pseudo-event null is the only placebo that could be built; the
no-transition country placebo failed for lack of countries. Early-warning methods are contested and require a
slowly changing driver plus noise; a national fertility series with a policy-driven break is not an ideal
substrate, and a null here is weak evidence about any single country. The diminishing-returns result is a
level-versus-change regression in which the floor is not separately identified; no causal claim is made.
Trend breaks from the WDI splice are not corrected.

## Data availability
| series | source | coverage | verdict |
|---|---|---|---|
| annual total fertility | `/root/work/data/fertility.json` | 16,933 country-years, 238 countries, mostly 1960-2024 | used, 80 usable events |
| lower-secondary completion | `/root/work/data/lsc.json` | merged to 3,865 country-year pairs, 238 countries | used |
| regional classification | `/root/work/data/meta.json` | 238 countries | used for fixed effects |
| schooling universalisation timing | `local_data/10_massification/data/UNIVERSALIZATION_TIMING.csv` | 6 countries, many censored | **data gap**, not used |
| child mortality, urbanisation | `/root/work/data` | available | not needed for the pre-registered tests |
| historical long-run panel | `/root/work/transition/out/long_run_panel.csv` | 1800+, reconstructed | not needed; its coverage cannot support 15-year windows at the transition for most countries |

## Files
`PREREGISTRATION.md` (first commit), `scripts/ews.py` (the whole analysis), `scripts/diag.py` (sample
diagnostic), `results/ews_results.json` (every number above).
