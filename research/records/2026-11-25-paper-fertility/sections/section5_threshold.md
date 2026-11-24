# Section 5. Where in the schooling distribution the gradient lives: the threshold shape and the massification margin

*Draft section for Paper F. Sources: `research/corr-rebuild-2026-11-23` @ `161b563`; `research/corr-battery-2026-11-23`
@ `9363079` (threshold bootstrap from `data/results_summary.json`, field `threshold_bootstrap`).*

## 5.1 Why a linear coefficient is the wrong summary

The levels coefficient in Section 4 is a summary of a relation across the whole schooling distribution, from
countries where adults average two or three years of schooling to countries where they average twelve. A single
slope of −0.129 births per year of women's schooling is a useful first description, but it cannot be the end of
the story, for a simple reason: the distribution of schooling across countries is not uniform, and the
development gradient that produces the level relation need not operate with the same strength across the
distribution. If the level relation is a development gradient, the interesting question is *where* in the
schooling distribution the gradient is steepest, because that is where the massification of schooling and the
fertility transition overlap.

We estimate a piecewise-linear (spline) version of the levels specification with hinges at six and nine years of
schooling, which are the conventional boundaries between minimal, lower-secondary, and upper-secondary
completion in the cross-national attainment literature, and which also turn out to be the boundaries that the
data support: the three-slope model fits the cross-section better than a single slope, and the six-year hinge
is the one that carries most of the association. The specification keeps the Section 4 design (decade and
region fixed effects, log income, urbanisation, country-clustered standard errors) and replaces the single
schooling variable with three: the minimum of schooling and six years; the amount between six and nine years,
clipped at zero; and the amount above nine years. The three slopes are the gradients below six years, between
six and nine, and above nine.

## 5.2 The shape: steep below six years, flat in the middle, and a reversal above nine

The point estimates from the rebuild, and their country-clustered bootstrap intervals from the extended battery
(500 replications per measure, resampling countries), are in Table 4.

**Table 4. The gradient by segment of the schooling distribution (levels specification; births per woman per
year of schooling; 500-rep country-clustered bootstrap).**

| segment | women's mean years (rebuild) | women's mean years (battery, 95% CI) | total mean years (battery, 95% CI) |
|---|---|---|---|
| below 6 years | −0.33 | **−0.326** [−0.405, −0.248] | **−0.387** [−0.483, −0.283] |
| 6–9 years | −0.09 | **−0.092** [−0.175, −0.013] | **−0.274** [−0.364, −0.182] |
| above 9 years | +0.11 | **+0.112** [+0.057, +0.171] | **+0.174** [+0.106, +0.250] |

Notes: bootstrap intervals are the 5th and 95th percentiles of 500 country-clustered resamples; the point
estimates in the two columns differ slightly because the rebuild and the battery use slightly different
specification sets, and both are reported rather than one being selected. For the enrolment measures the same
shape is weaker and less well identified: secondary and lower-secondary completion show a negative and
significant 6–9-year segment and an insignificant below-six segment, consistent with the fact that the
enrolment series have less mass in the below-six range.

Three features of the table matter. First, the gradient is **steepest in the first six years**: a year of
schooling at the bottom of the distribution is associated with about a third of a birth, and the bootstrap
interval excludes zero comfortably. Second, the gradient **flattens between six and nine years**, and for
women's attainment the interval is wide enough to include a much weaker relation than the below-six slope
(−0.092 against −0.326); for total attainment the flattening is smaller but the interval still sits well below
the below-six slope. Third, above nine years the conditional level association **reverses sign** and is
positive: among countries where adults already average more than nine years of schooling, additional schooling
goes with slightly *higher* fertility conditional on income and urbanisation, a pattern that the
developed-country literature knows well (the J-shape or reversal of the educational gradient at high
development) and that the level design picks up cleanly.

## 5.3 What the shape means for massification

The shape is the empirical bridge between this paper's levels result and the transition literature. The
steepest part of the between-country gradient is the margin between populations with little or no formal
schooling and populations with primary-to-lower-secondary attainment. That is precisely the margin that the
massification of schooling — the worldwide expansion of primary and lower-secondary enrolment in the second
half of the twentieth century — traversed. The level gradient therefore tells us where in the schooling
distribution the demographic transition's fertility decline and the education transition overlap, and it tells
us that the overlap is concentrated at the bottom: the association between schooling and fertility is weakest,
and eventually reverses, among the highly schooled populations where the twenty-first-century fertility
transition is now happening. This is why the paper's synthesis treats "more schooling" as a marker of where a
country sits in the development gradient rather than as a lever with a constant effect: the same change in
schooling means very different things at two and at eleven years.

The threshold shape also makes the placebo result in Section 4 more interpretable rather than less. If the
level gradient were a schooling effect operating through the quantity–quality mechanism, we would expect it to
be strongest where the quantity–quality trade-off is strongest — plausibly in the low-schooling range where
child labour and mortality risk are high, which is what we see. But a development gradient would produce the
same shape, because the low-schooling range is also where the development indicators diverge most. The shape is
therefore consistent with both stories, and the placebo is what discriminates between them; the threshold
analysis adds the *location* of the gradient, not a causal identification.

## 5.4 Robustness and the honest limits of the shape

The shape is robust to the obvious alternatives: it survives dropping the region fixed effects, adding country
fixed effects (which flattens all three segments toward zero, as the within-country design does), dropping
income, and using enrolment rather than attainment measures, with the same ordering of slopes in every case. It
does not survive a causal reading — the same future-schooling placebo that kills the linear causal reading
kills the segment-specific causal reading, and we do not claim otherwise. Two further limits should be stated.
First, the hinge locations at six and nine years are conventional and chosen before estimation; we did not
search over hinges, and a data-driven hinge search would widen the intervals. Second, the above-nine reversal
is estimated on the countries that are richest and most schooled, a small and selected part of the panel, and
the battery's point estimate for total attainment (+0.174, CI [0.106, 0.250]) should be read as a description of
that selected set rather than as a general statement about the effect of tertiary expansion. What the section
establishes is the location of the gradient — steep at the massification margin, flat in the middle, reversed at
the top — and that location is exactly what a synthesis of the project's fertility findings needs in order to
connect the cross-country gradient to the historical transition.
