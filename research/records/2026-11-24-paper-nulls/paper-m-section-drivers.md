# Paper M section 1: The massification drivers are not robust — a 400-grouping multiverse

*Draft section for the consolidated Massification paper (lead: panel-matrix). Source: grouping-multiverse-400 @ 1152cec; every number traces there (see `SOURCE_MAP.md`). Plain words; every share with its random-group comparison, sample and multiple-testing rule.*

## What was tested

The framework says massification is driven by the credential pipeline: as schooling expands, the
share of the population pushed through credentials rises, and that is what moves fertility, gender
parity and the rest. A drive-by cross-country regression can look consistent with this. The test
here asks the harder question: **does any of these links hold across the many reasonable ways of
splitting countries into groups?** If a link is a general process, it should show up when countries
are split by region, income, fertility history, schooling history, farm structure, urbanisation or
institutions. If it only shows up in one kind of country, it is a description of that kind of
country, not a driver.

Design: the 17-measure lead-lag matrix (ten-year change, country effects, decade effects,
clustered errors, income and urbanisation controls, with and without a country trend) is re-run
inside **50 real groupings in 8 families (179 groups)**, and compared with **400 random
re-partitions** of the same countries into groups of the same sizes (nesting preserved; the 400
draws are the yardstick). For each of the **272 links** we record the share of real groups in which
it is significant with its whole-sample sign, family-balanced, and compare that with the same share
in random groups. Multiple testing is Benjamini-Hochberg at 5%. The empirical floor is 1/401 =
0.0025: a single link cannot be certified on its own at 400 draws (it would need ~5,440 draws), but
where 30 links pin at the ceiling the step-up rule certifies the cluster.

## Result: a small set of strong links, a large null remainder

With the yardstick estimated from 400 random splits, **46 of 272 links beat random groupings with
trends** (42 of the 43 from the earlier 74-split run survive; 1 dies; 4 are new). **20 links do
worse** than random groupings (an effect that exists in the whole sample but is thinner in any
slice). **32 links show more sign-flipping** than random splits. **Only 5 links are robust in every
kind of grouping**, and of those only two are fertility-side: child mortality → life expectancy
(significant in 62.7% of real groups against 48.5% in random groups, above all 400 draws) and
child mortality → fertility (95.0% versus 93.0% — note this is "the same everywhere", not "beats
random", because a uniform effect shows up in random slices too). The other three are income →
urbanisation (52% versus 49%), farm share of output → income (53% versus 37%) and life expectancy
→ fertility (80.9% versus 93.0%). **No driver of schooling is robust everywhere.**

## The three drivers the framework leans on

**Electricity.** With country effects alone it looks like a strong driver: t = 4.12 for
lower-secondary completion, 4.40 for secondary, 3.85 for primary, 3.57 for gender parity in
secondary, 6.02 for gender parity in higher education. With a country trend it dies: the same
coefficients are 0.53, −0.26, 0.02, −0.77 and −1.94. Across groupings the real shares are 15.6%,
6.0%, 8.0%, 7.4% and 36.0%, against random-group shares of 2.5%, 5.1%, 5.6%, 6.1% and 28.0%. The
links to lower-secondary and higher education survive as group-specific (above all 400 draws); the
secondary link is no better than random; and electricity has the most sign-flipping of any driver
— 11 of its 32 links flip more than random groupings do. Electricity is a weak, group-dependent
driver once country trends are allowed.

**Paid employment.** No wage-employment link to any schooling outcome beats random groupings in
any kind of group. The shares are 8.9% versus 16.7% (lower-secondary), 5.6% versus 2.7%
(secondary), 13.9% versus 11.6% (primary), 5.7% versus 5.3% (gender parity in secondary) and 21.0%
versus 20.5% (higher education); the corresponding corrected p-values for beating the random null
are essentially 1. This is the cleanest null in the run.

**Child mortality and life expectancy.** These are the only robust massification-adjacent links,
and they sit on the fertility side rather than on any schooling outcome: they are the general,
uniform relationships the whole-sample matrix already showed, not evidence of a pipeline mechanism.

## The discipline result: a regularity, not a universal law

A companion scaling test (scaling @ fd691a6) estimated the same relations inside and between
countries. The education–income relations that look strong between countries mostly collapse
inside them: the secondary-enrolment–income exponent is 0.215 (SE 0.035) between countries and
0.090 (SE 0.124) within; upper-secondary attainment is 0.312 (0.052) between and 0.072 (0.167)
within. Only tertiary enrolment, lower-secondary completion, services share and urban share are
stable in both layers. In the fertility–attainment panel the between-country slope is −0.479 while
the ten-year within-country change slope is only −0.056. The appropriate summary is **a
late-industrialiser regularity, not a universal law**: the cross-section shows a strong association
between massification and its correlates, but the same relations are much weaker as within-country
change.

## What this section does not claim

These are associations across country groupings, not causal estimates, and the nulls are
scope-limited: a general process could still be present but diluted by measurement, by the coarse
ten-year window, or by a mechanism that operates within countries over shorter horizons. What the
test does establish is that the drivers the framework nominates — electricity, paid employment and
the broader massification bundle — are not detectable as general processes in the way the
framework requires. The plain attainment channel itself survives, and that is the part of the
massification story the data do support.
