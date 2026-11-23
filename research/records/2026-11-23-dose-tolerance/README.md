# Does a stricter fit pin the dose strengths down? A tolerance ladder (23 November 2026)

## The question
The previous record (`research/records/2026-11-23-dose-gpu/`) found the individuation strengths "stable
across independent runs but nearly as wide as the priors" and called that an identification limit. That
verdict is only meaningful if it survives tightening the fit tolerance: if the intervals narrow toward the
data as the tolerance tightens, "direction not strength" was a tolerance choice; if they stay prior-wide,
the data genuinely cannot pin the strengths.

## Method
Same engine and fitter as the previous record: equal-weight rejection ABC on the **exact published CPU
model**, no importance weights (importance weights were shown to collapse to one particle and are not used
here). One thing changes: the tolerance.

The tolerance comes from the **prior-predictive distance distribution** — the distances from drawing
parameter vectors from the prior and simulating with no fitting at all. That distribution was measured with
2,500 pure prior draws over the eight fit countries (`results/prior_pred_A.json`, seed 11, 30 draws/s):

| percentile of the prior-predictive distance | distance | used as |
|---|---|---|
| 5th | 16.59 | eps 16.59 (tightest) |
| 10th | 18.33 | eps 18.33 |
| 20th | 21.68 | eps 21.5, the previous record's baseline |

eps 18.33 therefore accepts the closest 10% of prior draws, eps 16.59 the closest 5%. Each run draws
independently from the prior and keeps every draw below the tolerance with equal weight, so the effective
sample size equals the number of accepted draws by construction. Scenario A, eight fit countries, the three
country-effects profiled out by taking the best per country, the same four target groups and the same
standardisation as before. Physical parameter values are the lower prior bound plus the unit-cube draw times
the prior width.

## (1) Fertility

### The ladder
| tolerance | prior draws | accepted | acceptance | accepted distance, median [min, max] |
|---|---|---|---|---|
| eps 21.5 (closest 20%) | 5,000 | 1,044 | 20.9% | 18.40 [10.96, 21.50] |
| eps 18.33 (closest 10%) | 10,000 | 1,012 | 10.1% | 16.44 [10.22, 18.32] |
| eps 16.59 (closest 5%) | 12,000 | 660 | 5.5% | 15.25 [10.25, 16.59] |

Effective sample size equals accepted draws in every row (equal weights). Median and 90% interval, with the
fitted spread as a fraction of the prior spread in brackets:

| strength (prior range) | eps 21.5 | eps 18.33 | eps 16.59 |
|---|---|---|---|
| kin-support loss per full dose (0-5) | 2.80 [0.34, 4.74] (0.96) | 2.82 [0.42, 4.85] (0.98) | 2.82 [0.39, 4.76] (0.96) |
| downward money flow (0-5) | 2.62 [0.30, 4.77] (1.00) | 2.63 [0.30, 4.73] (1.00) | 2.74 [0.23, 4.76] (1.01) |
| cohort deepening (0-3) | 1.58 [0.15, 2.85] (0.98) | 1.58 [0.24, 2.81] (0.94) | 1.31 [0.21, 2.62] (0.87) |
| career delay per unit independence (0-8) | 5.32 [1.10, 7.71] (0.88) | 6.05 [2.64, 7.80] (0.71) | 6.35 [1.77, 7.85] (0.76) |
| marriage-market pickiness (0-5) | 2.41 [0.25, 4.70] (0.98) | 2.47 [0.28, 4.74] (0.97) | 2.61 [0.29, 4.78] (1.00) |

Interval width as a fraction of the prior width (the sharpest way to see whether the data are biting):

| strength | eps 21.5 (20%) | eps 18.33 (10%) | eps 16.59 (5%) |
|---|---|---|---|
| kin-support loss | 0.88 | 0.89 | 0.87 |
| downward money flow | 0.89 | 0.89 | 0.91 |
| cohort deepening | 0.90 | 0.86 | 0.80 |
| career delay | 0.83 | 0.64 | 0.76 |
| marriage-market pickiness | 0.89 | 0.89 | 0.90 |

### Verdict: an identification limit, not a tolerance artefact
Quadrupling the strictness (accepting the closest 20% of prior draws down to the closest 5%) leaves four of
the five strengths essentially where they were, on the width measure 0.88 -> 0.89 -> 0.87, 0.89 -> 0.89 ->
0.91 and 0.89 -> 0.89 -> 0.90 of the prior width; on the spread measure 0.96 -> 0.98 -> 0.96 of the prior spread,
1.00 -> 1.00 -> 1.01 and 0.98 -> 0.97 -> 1.00. The intervals at
the tightest tolerance still cover 87% of the prior range for kin-support loss. **For these four, the wide
intervals are what the data can deliver, not an artefact of a loose fit**, and the earlier "direction not
strength" sentence stands.
Two strengths do move, but modestly and not monotonically enough to change the reading: cohort deepening
narrows from 0.98 to 0.87 of the prior spread (median 1.58 -> 1.31) and career delay narrows from 0.88 to
0.71-0.76 (median 5.32 -> 6.35 of a 0-8 prior). Even for these, the 90% intervals still span more than half
the prior range.
Test designed to kill the claim: the ladder itself. If the intervals had been a tolerance artefact they would
have narrowed monotonically as acceptance fell from 20.9% to 5.5%; they did not, for four of five.

### The caveat that matters more than the ladder
Even at the tightest tolerance the accepted draws have median distance 15.25 against a best of 10.25, so the
fit is still poor in absolute terms and the tolerance is coarse by any standard. A tighter tolerance does not
just shrink the accepted set, it changes *what kind* of parameter vector survives: selection is on overall
distance across all targets, so a stringent cut favours vectors that are mediocre everywhere over vectors
that are excellent on one target and poor on another. The 660-draw tight sample is therefore a valid
equal-weight ABC sample at a stated tolerance, but it is not evidence that the model fits.

### Scenario B
Not interpretable, and reported as such rather than quoted. The one tight-tolerance run attempted used
scenario A's 5th-percentile distance as the tolerance for B; because development-only fits the data worse,
that admitted only 0.8% of prior draws (32 accepted at 4,000 draws drawn), so I stopped it deliberately
rather than let it produce a ~120-draw selected set: that is too few draws to support intervals, and a
narrow-but-biased posterior would have been the likely outcome.
A B ladder needs B's own prior-predictive distribution (B's 20th percentile is 22.9 against A's 21.5); that
was not measured inside the time budget. No B interval from a tight tolerance is quoted anywhere.

## (2) Massification
Nothing here changes the massification reading. The dose strengths that carry the massification story
(how much schooling shifts kin support, money flows and the marriage market) are the four that do **not**
narrow, so a stricter fit does not rescue them: at the closest 5% of prior draws the kin-support effect is
still anywhere from 0.39 to 4.76 on a 0-5 scale, which is "keeps between 78% of kin support at a full dose
and essentially none". The one dose-side strength that does narrow, cohort deepening, moves in the direction
of a weaker effect (1.58 -> 1.31), not a stronger one. The earlier conclusion therefore stands and is now
better supported: the direction of the schooling channel is identified, its magnitude is not, and that is a
property of the data rather than of the fitting choice.

## Limits
Two rungs, not many: the ladder is 20% -> 10% -> 5% of the prior-predictive distribution, so a finer ladder
between 5% and 1% was not run (it would need roughly 60,000 prior draws for a 600-draw sample at 1%, about an
hour at the achieved 20-34 draws/s). Scenario B's ladder was not completed (above). The accepted-distance
median at the tightest rung is still 15.25, so even the tightest posterior is an ABC summary of a badly
fitting model. And all of it is scenario A on the eight fit countries; the held-out countries were not
re-fitted.

## Files
`scripts/reject_abc.py` (the fitter, unchanged from the previous record apart from progress logging and
saving the drawn-distance distribution), `scripts/ladder_report.py` (builds the tables), `results/`:
`prior_pred_A.json` (the prior-predictive measurement), `lad_A_eps10.json`, `lad_A_eps05.json`, the
baseline `rej_fitA.json` carried over from the previous record for comparison, `ladder.json` (every number
in the tables as data), and the run logs.
