# The level of analysis decides the answer: schooling, fertility, and the standard change specification

**Paper F — fertility synthesis (draft for Population and Development Review / Demographic Research)**

*Working draft, 25 November 2026. Every number traces to a verified project record (branch @ commit, file,
field) in `data/claims_sources.csv`. The paper is a descriptive structural demonstration: it shows what the
field's standard within-country change specification does to a known between-country correlation. It does not
claim a causal effect of schooling on fertility, and no sentence in the abstract, introduction, or conclusion
should be read as such.*

## Abstract

The demography of schooling and fertility contains a contradiction that is usually smoothed over: cross-country
studies find a large negative association between schooling and fertility, while the field's standard
within-country change specification — ten-year changes, country fixed effects, country trends — often finds
nothing. This paper shows that the contradiction is produced by the level of analysis, and measures it. In a
1960–2024 country panel, all eight schooling measures predict lower fertility strongly and precisely in levels
(women's mean years of schooling: −0.129 births per woman per year, SE 0.029, n = 5,915 country-years, 192
countries), and the association survives a pre-registered 336-specification curve (99.7% of period
specifications negative, 91.3% negative-significant, median −0.475). In ten-year changes with country fixed
effects and country trends the same measures are weak or reverse: women's attainment is +0.111 (SE 0.045), and
no measure has a negative-significant change coefficient. Across 13,800 random re-partitions of countries into
six groups, the schooling–fertility level relation is negative and significant in 71–99% of groups; the change
relation in 0–7%. A future-schooling placebo is about 90% as strong as the correct-time relation (52.9% versus
58.8% of cells negative-significant), so the level gradient is a development-gradient association and not an
identified schooling effect. The gradient is steepest below six years of schooling (−0.326, 95% CI [−0.405,
−0.248]), flattens at 6–9 years (−0.092 [−0.175, −0.013]), and reverses above nine (+0.112 [+0.057, +0.171]).
Supporting sections report a survey-level DHS gradient (secondary education −1.62 children, 99% of 346 surveys
negative), falsified dynamic predictions (cohort and pipeline attenuation), a care-work loop absorbed by income
and urbanisation, a strong "no-off-switch" that fails, an absent tipping point, and a transition model whose
mortality counterfactual removes 3.2% of the fertility collapse. The contribution is a quantified audit of a
known correlation: the between-country gradient is real, global, and located at the massification margin, and
the standard change design erases exactly the variation it lives in. It is descriptive, not causal.

## 1. Introduction

### 1.1 The contradiction, stated precisely

Ask whether more schooling means fewer births and the answer depends on the design. In levels — fertility
regressed on schooling across countries, with controls — the association is negative, large, and robust; it is
one of the most reliable regularities in the social sciences (Barro & Lee, 2013; Lutz & KC, 2011; Mincer, 1958;
Psacharopoulos & Patrinos, 2004). In ten-year changes with country fixed effects — the field's standard way of
asking whether a country's schooling expansion was followed by a faster fertility fall — the association is
weak, often indistinguishable from zero, and in several measures significantly positive. Both designs are
reported in the literature as estimates of "the effect of education on fertility". They cannot both be that,
and the usual attributions — measurement, sample, choice of schooling measure — do not explain a sign reversal
on the same measures and the same panel. This paper shows that the reversal is a level-of-analysis effect,
measures its size and its boundary conditions, and draws the consequences for how the field should read its own
literature.

The question the paper is built around is not whether schooling and fertility are negatively correlated; they
are, in levels, almost everywhere. The question is the one a referee should ask before accepting either
literature: **has anyone shown that the field's standard within-country change specification systematically
erases the between-country schooling–fertility gradient, and with what evidence?** The answer, from the review
in Section 2, is that the principle is old and the pattern is documented piecemeal, but a quantified audit of
the pattern for this relation — the full specification space, a random-re-partition transportability test, a
timing placebo, and a threshold location — has not, to our search, been reported. This paper supplies that
audit. It is a structural demonstration about a known correlation, not a new correlation, and the distinction
matters: the claim is about what research designs do to a relation the field already knows, not about a new
empirical regularity.

### 1.2 What the paper shows

Five results, in the order in which the paper builds them.

**In levels, the gradient is large, precise, and robust.** Women's mean years of schooling: −0.129 births per
woman per year of schooling (SE 0.029), on 5,915 country-years and 192 countries. Total attainment: −0.228
(0.042). Secondary enrolment: −0.0213 (0.0037). All eight schooling measures — two attainment series, four
enrolment/completion series, two gender-parity series — are negative and significant. The pre-registered
specification curve reports 336 specifications: 99.7 per cent of the 288 period specifications are negative,
91.3 per cent negative-significant, 0 per cent positive-significant, with a median coefficient of −0.475.

**In changes, the same measures are weak or reversed.** Ten-year changes with country fixed effects, decade
effects, and country-specific trends give women's attainment +0.111 (0.045), significantly positive; total
attainment +0.190 (0.055); lower-secondary completion +0.0066 (0.0031). Across the change specification grid,
no measure has a negative-significant coefficient; three of eight are positive-significant; the change
coefficient is negative in only 24–44 per cent of specifications, against 70–83 per cent for levels.

**The level relation is a global property; the change relation is not.** Across 13,800 random six-group
re-partitions of the panel's countries, the schooling–fertility level relation is negative and significant in
**71–99 per cent** of groups, while the change relation is in **0–7 per cent**. The matrix-wide comparison
reported alongside it (22.7 per cent for levels against 11.1 per cent for changes over all 342 ordered pairs)
is the honest version of the same test: the global-property claim is about the schooling–fertility relation, not
about every pair in the data.

**The gradient is a development gradient, not an identified schooling effect.** The future-schooling placebo,
in which schooling measured ten years after fertility predicts current fertility on the identical design
cells, is 52.9 per cent negative-significant against 58.8 per cent for the correct-time relation — about 90 per
cent as strong, and about 80 per cent as large in median magnitude. The pre-registered decision rule therefore
fires: the level relation is descriptive. Countries with more schooling have fewer births, and the association
cannot be read as the effect of changing schooling while holding development constant.

**The gradient is concentrated at the massification margin.** Piecewise-linear estimates put the slope at
−0.326 (95% CI [−0.405, −0.248]) below six years of schooling, −0.092 [−0.175, −0.013] between six and nine,
and +0.112 [+0.057, +0.171] above nine. The steepest part of the between-country gradient is the margin the
massification of schooling traversed; the twenty-first-century fertility transition, among highly schooled
populations, sits where the association is weakest and may reverse.

### 1.3 Why this is a contribution and not a complaint

The paper's contribution is the **audit**, and it has four components that the literature has not combined for
this relation. First, the specification curve: the levels result is not a selected specification, and the change
result is not either; both distributions are reported in full. Second, the re-partition transportability test:
rather than asserting that the level relation is a general property, the paper re-partitions the panel 13,800
times and reports the distribution. Third, the placebo: the development-gradient caveat is measured, not
asserted, so the descriptive claim survives while the causal one is rejected with evidence. Fourth, the
threshold location: the gradient is placed in the schooling distribution, which is what connects the
cross-section to the historical transition. The paper then uses the same discipline on the project's other
fertility workstreams — a survey-level gradient, care-work and no-off-switch nulls, a transition model, a
tipping-point test — so that the synthesis is a verdict table rather than a victory lap.

### 1.4 What the paper does not claim

It does not claim to identify the causal effect of schooling on fertility; the placebo is designed to show that
the level design cannot, and the language is descriptive throughout. It does not claim that education is
irrelevant within populations; the individual and survey literature is clear that it is not (Cleland &
Rodriguez, 1988; Kravdal, 2002; Chicoine, 2012; Osili & Long, 2008), and Section 7.1 reconciles the macro null
with the individual gradient explicitly. It does not claim that the change design is wrong; it is the right
design for a different question, and the paper says which. It does not claim novelty for the observation that
levels and changes disagree — Robinson (1950), Nickell (1981), Brock and Durlauf (2001), and Eberhardt and Teal
(2011) establish that, and the paper cites it as established. It does not claim that mass schooling causes
fertility to fall; Caldwell's (1980) thesis is the closest competitor, and the placebo is why this paper reads
the gradient as a development marker rather than a determinant. And it does not claim that the project's other
workstreams settle the fertility transition; they narrow the space of live hypotheses, which is what the
evidence supports.

### 1.5 Roadmap

Section 2 reviews the four literatures that bear on the audit question and states what the audit adds. Section 3
describes the panel, the measures, the designs, and the evidence grading. Section 4 presents the finding: levels
versus changes, the specification curve, the transportability experiment, and the placebo. Section 5 draws the
implications for how the field estimates and reads schooling–fertility relations. Section 6 sets out the data
and designs that would turn the audit into a causal estimate or a new correlation. Section 7 presents the
supporting workstreams: the survey-level DHS gradient and its reconciliation with the macro result, the
care-work and no-off-switch nulls, the transition model, and the threshold shape. Section 8 discusses
limitations and concludes.
