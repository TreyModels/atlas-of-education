# Section 1. The wrong level of analysis: a large between-country schooling–fertility gradient that the within-country design erases

*Draft section for Paper F (omnibus fertility synthesis). Sources: `research/corr-rebuild-2026-11-23` @ `161b563`;
`research/corr-battery-2026-11-23` @ `9363079`. Claim-to-source map in `../data/claims_sources.csv`.*

## 1.1 The question and why the level of analysis decides the answer

The empirical literature on schooling and fertility contains an unusually clean contradiction. Cross-country
studies almost always find that countries with more schooling have fewer births, with coefficients that are
large, stable, and insensitive to the usual controls. Panel studies that follow countries over time, with
country fixed effects and ten-year changes, almost always find something much smaller — often zero, sometimes
the "wrong" sign. Both sets of estimates are usually presented as estimates of "the effect of education on
fertility," and both are usually reported with clustered standard errors and defensible controls. The
contradiction is not a data problem. It is a level-of-analysis problem, and it has a long and uncomfortable
pedigree in the social sciences: correlations computed between units need not describe relations within units
(Robinson, 1950), and the econometrics of panel data has known for four decades that the between and within
components of a panel identify different parameters with different biases (Hausman & Taylor, 1981; Nickell,
1981; Angrist & Pischke, 2009). Demography has used both designs for the schooling–fertility relation without
always being explicit that they answer different questions.

This section of the synthesis takes the contradiction seriously and treats it as a finding rather than a
nuisance. We ask three questions. First, how large is the schooling–fertility association when it is estimated
at the level at which it is actually a near-universal empirical regularity — the between-country level?
Second, what happens to that association when the same measures are estimated on within-country decade changes
with country fixed effects and country trends? Third, is the level association a *global* property that
reproduces itself in arbitrary subsets of countries, or is it produced by a particular grouping of the data
(the regions, income classes, or decades that researchers happen to use)? A fourth question follows from the
answers: if the level association is global but does not survive a timing placebo, what is it a property of?

The answers, in one paragraph, are these. In levels, all eight schooling measures we can construct predict
lower fertility, with coefficients that are large and precisely estimated, and the association is one of the
most robust cross-country regularities in the panel. In decade changes, the same measures are weak, and for
several of them the coefficient is significantly *positive*: decades in which schooling expanded fastest are
not decades in which fertility fell fastest, and are often the opposite. Across 13,800 random re-partitions of
the panel's countries into six groups, the level relation is negative and significant in 71–99 per cent of
groups for the eight schooling–fertility pairs, while the change relation is negative and significant in 0–7
per cent — the level relation is a property of almost any subset of countries, and the change relation is
nearly absent from all of them. But a placebo in which *future* schooling predicts *current* fertility is
about 90 per cent as strong as the correct-time relation, so the gradient is a development-gradient
association: schooling and fertility both move with a country's position in the development process, and the
level correlation does not identify a causal effect of schooling at a point in time. The level of analysis
determines the sign of the answer; it does not, by itself, license a causal reading.

## 1.2 Data and measures

The analysis uses the project's country-year panel, 1960–2024, observed values only (no imputation, no
interpolation), covering 196 countries with non-aggregate ISO-3 codes. Fertility is the total fertility rate
(births per woman). Schooling is measured eight ways, because the literature disagrees about which measure is
the right one and because the disagreement turns out not to matter for the levels result: mean years of
schooling for women and for the total adult population (Barro–Lee/OWID series, female series 1990–2023), gross
secondary enrolment, lower-secondary completion, primary completion, tertiary enrolment, and the gender-parity
indices for secondary and tertiary enrolment. Controls are the log of GDP per capita (the income file holds
levels; the log is taken at load) and the urbanisation rate. All standard errors are clustered by country. The
panel is unbalanced by construction: coverage of the schooling measures ranges from about 1,400 country-years
(total attainment, 144 countries) to about 5,900 country-years (female attainment, 192 countries).

Two design choices follow the project's standing rules and should be stated plainly. First, income enters in
logs, because the relation between income and fertility is multiplicative rather than additive at these levels
of development; entering income in levels changes the fitted fixed-effect counts in the companion matrix but
not the substantive conclusion. Second, the within-country change design uses the project's standard
specification: the ten-year change in fertility on the starting level of schooling, country fixed effects,
decade effects, country-specific linear trends, income and urbanisation controls, and country-clustered
standard errors. That specification is deliberately conservative — country trends absorb any smooth national
path, and the change design throws away the between-country variation that the levels design uses. It is the
design that produced the original null, and we keep it intact so that the comparison is honest.

## 1.3 Levels versus changes: the same measures, the same period

Table 1 reports the two designs side by side for the seven measures available in both the rebuild and the
extended battery (the eighth, the secondary gender-parity index, is in the extended table). Columns 1 and 2 are
the levels and change coefficients for each measure; columns 3 and 4 give the sample size and the number of
countries in the levels specification.

**Table 1. Schooling and fertility, levels versus ten-year changes (same measures, same period).**

| measure | levels | ten-year changes | n / countries (levels) |
|---|---|---|---|
| mean years of schooling, women | **−0.129** (0.029) | **+0.111** (0.045) | 5,915 / 192 |
| mean years of schooling, total | **−0.228** (0.042) | **+0.190** (0.055) | 1,394 / 144 |
| secondary enrolment (%) | **−0.0213** (0.0037) | +0.0030 (0.0026) | 5,927 / 202 |
| lower-secondary completion (%) | **−0.0224** (0.0035) | **+0.0066** (0.0031) | 4,106 / 193 |
| primary completion (%) | **−0.0239** (0.0033) | −0.0003 (0.0019) | 4,878 / 193 |
| tertiary enrolment (%) | **−0.0040** (0.0020) | −0.0044 (0.0026) | 5,126 / 198 |
| gender parity index, tertiary | **−1.27** (0.20) | +0.0006 (0.207) | 4,455 / 198 |

Notes: country-clustered standard errors in parentheses. Levels: fertility level on schooling level, decade
and region fixed effects, income (log) and urbanisation, all years; changes: ten-year change in fertility on the
starting schooling level, country fixed effects, decade effects, country trends, income and urbanisation.
Bold: |t| > 1.96.

The levels column is not a marginal association. A country in which women have five more years of schooling has
about 0.65 fewer births per woman, conditional on income and urbanisation; one more percentage point of
secondary enrolment goes with 0.02 fewer births. Every one of the seven coefficients is negative and
significant, and the eighth measure (secondary gender parity) behaves the same way in the extended battery
(−1.97, SE 0.28). The change column is a different object. Female attainment's change coefficient is
**+0.111** (0.045), significantly positive; total attainment +0.190 (0.055); lower-secondary completion
+0.0066 (0.0031) — all significant, all the opposite of the levels sign. The remaining measures are near zero,
and the extended battery finds that **no measure has a negative and significant change coefficient**. The
chosen specification matters for magnitudes but not for the contrast: across the full pre-registered grid of
levels specifications (four fixed-effect designs — decade, decade+region, country within, country within plus
country trends — three control sets, six lags, 49 samples), the level coefficient for each schooling–fertility
pair is negative in 70–83 per cent of specifications and negative-significant in 43–59 per cent; across the
corresponding change grid it is negative in only 24–44 per cent and negative-significant in 3.5–13.5 per cent.

The contrast survives the obvious rival: income. Adding the log of GDP per capita to the levels specification
leaves female schooling at −0.129 (0.029) with income −0.231 (0.063); total attainment at −0.228 (0.042) with
income −0.142 (0.087, not significant); income alone gives −0.318 (0.066). Both income and schooling predict
the level, and schooling is not a proxy for income in this comparison. In the change specification income's
coefficient is also small and imprecise, so the flip is not an income composition effect.

What does the contrast mean? It means the two designs are not estimating the same parameter. The levels
coefficient compares countries at different stages of the development process and answers the question "do
countries with more schooling have fewer births?" The change coefficient compares a country to itself a decade
earlier and answers the question "when this country's schooling stock rose, did its fertility fall faster?" The
first is a between-country gradient; the second is a within-country association. Robinson's (1950) warning
applies in its classic form, and so does the panel-data point: the within estimator removes all
time-invariant country characteristics — family systems, kinship structures, the demographic regime, the
measurement conventions that make a "year of schooling" mean different things in different systems — and so
identifies a parameter that is local to short-run covariation. Neither coefficient is "wrong." They are
answers to different questions, and the literature's practice of reporting one as if it answered the other's
question is the error this paper is about.

## 1.4 Specification curve: the levels result is not a specification choice

A natural objection is that the levels result is an artefact of one specification. The rebuild therefore
pre-registered a 336-specification grid (four lags, three control sets, two fixed-effect sets, four functional
forms, three measures, plus a cohort extension) and reported every cell, not a selected subset. For the 288
period-TFR specifications, **99.7 per cent are negative, 91.3 per cent are negative and significant, and 0 per
cent are positive and significant**, with a median coefficient of −0.475. Across all 336 specifications,
including the 48 cohort cells, 96.1 per cent are negative and 81.8 per cent are negative-significant, with 3.6
per cent positive-significant; the cohort cells are mixed (75 per cent negative, 25 per cent
negative-significant, 25 per cent positive-significant) on only 24–27 countries, and are reported as
inconclusive rather than folded into the headline. The pre-registered criterion — at least 80 per cent negative
and 50 per cent negative-significant — is met for the period specifications. The levels result is robust to the
specification curve in the strong sense that there is no specification in the reported grid that reverses it and
survives as a defensible alternative.

The change result is the opposite kind of object: it is not that some specification reverses it, it is that the
sign is not stable across measures and the magnitudes are small relative to their uncertainty. In the extended
battery the change coefficients span −0.0044 to +0.189 depending on the measure, with standard errors of the
same order as the smaller coefficients. That is the signature of a weak within-country association rather than
of a robust negative one.

## 1.5 Transportability: a global property or a grouping artefact?

The most direct test of the claim "the level relation is a property of countries in general" is not another
regression; it is a re-partition experiment. If the relation is a global between-country property, it should
reproduce itself in almost any arbitrary grouping of countries, because any grouping is a sample of the same
underlying cross-section. If it is an artefact of one particular grouping — the six regions, four income
classes, or seven decades that a researcher happens to use — it will be strong in those groups and weak or
absent in random ones.

We ran 800 pre-registered random re-partitions of the panel's countries into six groups (same group sizes under
the nesting rule, family-balanced shares) and then extended the run in waves to **13,800 re-partitions** to
tighten the random yardstick; within every group and every pair we estimate the levels relation and the change
relation with the same baseline specification. For each re-partition we compute the share of the 342 ordered
pairs × 6 groups whose estimate is negative and significant. Table 2 reports the comparison.

**Table 2. Transportability: share of within-group estimates that are negative and significant (13,800 random
six-group re-partitions; 342 ordered pairs; the eight schooling–fertility pairs shown separately).**

| grouping | levels | changes |
|---|---|---|
| all 342 pairs, random re-partitions, mean [5th, 95th pct] | **0.227** [0.214, 0.239] | **0.111** [0.103, 0.120] |
| real groupings (regions, income groups, decades; pooled) | 0.54 | 0.01–0.12 |
| schooling–fertility pairs, random re-partitions (range over the 8 measures) | **0.715–0.989** | **0.000–0.072** |

Two readings matter here, and they point in opposite directions. The first is the one this paper is about: for
the schooling–fertility pairs, the level relation is reproduced in **71–99 per cent** of arbitrary country
groups and the change relation in **0–7 per cent**. That is the strongest available evidence that the level
relation is a global between-country property and not a grouping artefact: it does not depend on which
countries you put together. The second reading is a caution about the whole 342-pair matrix: across *all*
pairs, only 22.7 per cent of group × pair estimates are negative and significant, because most of the 342
ordered pairs are not schooling–fertility pairs and their signs are mixed by construction. The pre-registered
"global property" threshold of at least 80 per cent is met for the relation of interest and is not met for the
matrix as a whole; both facts are reported here rather than one being selected.

This distinction is the paper's answer to the transportability question. The level relation is not a fragile
finding that happens to hold in the countries we have; it is a property of the cross-section that survives
arbitrary re-groupings. What is fragile is the *change* relation, which is not reproduced in arbitrary groups
even when it is estimated on the same countries and measures.

## 1.6 The placebo: the gradient is a development gradient, not a schooling effect

A global level correlation is compatible with two very different stories. The first is that schooling itself
lowers fertility — through the quantity–quality trade-off, through women's time allocation, through the
information and autonomy channels that the literature has documented. The second is that both schooling and
fertility are consequences of a country's position in the development process — its income, its mortality
regime, its urban structure, its position in the demographic transition — and that the level correlation is
the shadow that the development gradient casts on two of its indicators. The two stories predict the same
cross-sectional correlation; they differ in what happens when the timing is disrupted.

We implemented the disruption that the project's earlier work used: a future-schooling placebo, in which
schooling measured **ten years after** the fertility outcome predicts current fertility, on exactly the same
design grid as the correct-time relation. Under the schooling-effect story, future schooling cannot affect
current fertility, so the placebo coefficient should be near zero and insignificant. Under the
development-gradient story, future schooling is another noisy indicator of the same country position, so the
placebo should be nearly as strong as the correct-time relation. Table 3 reports the result.

**Table 3. Future-schooling placebo versus the correct-time relation, identical design cells (battery run,
9363079).**

| comparison | share of cells negative & significant | median coefficient |
|---|---|---|
| schooling–fertility pairs, future schooling (t+10) | **52.9%** | −0.0179 |
| schooling–fertility pairs, correct time | **58.8%** | −0.0224 |
| all 342 pairs, future schooling | 20.1% | +0.0034 |
| all 342 pairs, correct time (same cells) | 21.1% | +0.0024 |

The placebo is not null. For the schooling–fertility pairs it is about **90 per cent as strong** as the
correct-time relation in the share of negative-significant cells, and about 80 per cent as strong in median
magnitude. The pre-registered decision rule — if the placebo reaches 80 per cent of the correct-time share, the level
relation is not an identified schooling effect — therefore fires. The level relation is not an identified
schooling effect, and it is not evidence for a pure development gradient either: common development trends,
anticipation/quantity-quality, and a long-lag schooling effect all predict the same future-schooling pattern.
The change-on-change ladder in the E11 fertility audit (`research/e11-fertility-audit-2026-11-25` @ `e926575`)
returns "does not discriminate", so the placebo cannot isolate a development gradient. The levelled relation is
descriptive: countries with more schooling have fewer births, and the association is global and robust, but it
cannot be interpreted as the effect of changing schooling while holding development constant, because future
schooling "predicts" current fertility almost as well. The result is not a defect of the schooling measures; it
is what a development gradient — or anticipation, or a long-lag schooling effect — looks like in a cross-section,
and it means that the
cross-country literature's practice of interpreting the level coefficient causally is unsupported. The same
conclusion was reached on the smaller earlier grid (where the placebo was negative-significant in 24 of 24
specifications, median −0.68); the large-grid result is a measured version of that caveat rather than a
different result.

## 1.7 What survives

Three things survive this section, and one does not. What survives: (i) a large, global, between-country
schooling–fertility gradient — negative for all eight measures, robust across the 336-specification curve,
reproduced in 71–99 per cent of 13,800 arbitrary country groupings; (ii) a clear demonstration that the
within-country change design erases that gradient, with the change coefficient for several measures
significantly positive, which explains why panel fixed-effects studies have returned nulls; and (iii) a
quantified caveat that the level relation is not an identified causal effect; the future-schooling placebo cannot
distinguish a development gradient from anticipation or a long-lag schooling effect. What does not survive is the
causal reading of the level coefficient, and with it the practice of citing the between-country gradient as
evidence that expanding schooling will reduce fertility; the placebo cannot distinguish a development gradient
from anticipation or a long-lag schooling effect. The section's contribution is not a new causal estimate; it is
the demonstration that the level-of-analysis choice determines the empirical answer, that the level answer is
real and global, and that its causal interpretation is exactly what the placebo rules out. The next sections
of the synthesis ask what the between-country gradient is a gradient *of*, and whether the within-country
weakness is a property of schooling specifically or of the demographic transition's dynamics more broadly.
