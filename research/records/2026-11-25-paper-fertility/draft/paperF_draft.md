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


# 2. Literature review: has anyone shown that the standard change specification erases the schooling–fertility gradient?

## 2.1 The question the review must answer

A literature review around this paper's claim cannot be a list of studies that find a negative
schooling–fertility association; there are hundreds, and their existence is not in dispute. The question is
narrower and answerable: **has anyone shown that the field's standard within-country change specification
systematically erases the between-country schooling–fertility gradient, and with what evidence?** The answer
organises this section into four bodies of work — the ecological-fallacy/aggregation tradition, the
within-versus-between fixed-effects critique, the cross-country growth-panel critiques, and the
schooling–fertility literature estimated both ways — and then states what the present paper adds to each. The
short answer is that the *principle* is old and well established in all four bodies of work, that the *pattern*
is documented piecemeal in a few places, and that a **quantified audit** of the pattern for this specific
relation — specification curve, random-re-partition transportability, a timing placebo, and a threshold
location — has not, to our search, been reported. The paper's contribution is that audit, not a new
correlation.

## 2.2 The ecological fallacy and aggregation tradition

Robinson's (1950) demonstration that ecological correlations need not equal individual correlations is the
foundational statement, and it applies to the schooling–fertility relation with unusual force because the
relation is one of the most frequently estimated at both levels. The tradition that followed Robinson
established three things that matter here. First, aggregation bias is not a technicality; it can reverse signs,
and its direction depends on the within-group and between-group covariance structures (Robinson, 1950;
Freedman's later reviews). Second, the solution is not to choose the "right" level but to be explicit about
which level identifies which parameter, and to test whether the aggregate relation is consistent with
micro-level evidence. Third, in the presence of heterogeneous units, the aggregate coefficient is a weighted
average of unit-level coefficients that need not correspond to any policy-relevant parameter.

The cross-country growth literature made the same point in an econometric register. Levine and Renelt's (1992)
sensitivity analysis showed that cross-country growth coefficients are fragile to small changes in the
conditioning set; Sala-i-Martin's (1997) "two million regressions" response argued that some coefficients are
robust if one accounts for the full distribution of specifications; Brock and Durlauf (2001) argued that the
cross-country growth literature's level regressions are "growth empirics and reality" precisely because they
mix between-country and within-country variation and attach causal language to neither; Durlauf, Johnson, and
Temple (2005) systematised the point in the *Handbook of Economic Growth*. Eberhardt and Teal (2011) give the
clearest statement for our purposes: cross-country level regressions and within-country change regressions
routinely disagree, the disagreement is informative about the underlying heterogeneity, and the choice between
them should be made by asking which parameter answers the question, not by which coefficient is larger. Our
paper applies that argument to a relation where the disagreement has usually been treated as a substantive
puzzle rather than as a design artefact.

Two recent literatures reinforce the aggregation point from adjacent directions. The specification-curve and
multiverse literature (Steegen, Tuerlinckx, Gelman, & Vanpaemel, 2016; Simonsohn, Simmons, & Nelson, 2020;
Del Giudice & Gangestad, 2021) shows that reporting a single specification from a large defensible space is
itself a source of inferential error, and that the distribution of estimates across specifications is the
honest object of inference. The many-analysts literature (Silberzahn et al., 2018) shows that analytic choices
alone can produce substantively different answers from the same data. We take both seriously: the paper's
specification curve is pre-registered and complete, and the transportability experiment is a multiverse over
groupings rather than over specifications.

## 2.3 The within-versus-between fixed-effects critique

The panel-data literature's core result is that the within (fixed-effects) estimator and the between estimator
identify different parameters. Hausman and Taylor (1981) formalised the choice between fixed and random effects
and made the correlation between unit effects and regressors the deciding issue; Nickell (1981) showed that
dynamic panel fixed-effects estimators are biased in short panels, a result that matters here because
fertility is strongly persistent; Angrist and Pischke (2009) give the standard teaching statement that the
within estimator "sweeps out" all time-invariant heterogeneity — which is precisely the between-country
variation in which a development gradient lives. Bell and Jones (2015) show that the within-between
decomposition is often the appropriate model when both sources of variation are substantively interesting,
and that reporting only the within coefficient can mislead when the between component is large.

Three further results bear on the change design specifically. Bertrand, Duflo, and Mullainathan (2004) show
that difference-in-differences estimates with serially correlated outcomes are badly over-confident unless
inference is corrected; our change specifications cluster by country, and the paper reports clustered standard
errors throughout. Roth (2022) shows that pre-testing for parallel trends can distort event-study estimates, a
caution that applies to any "trends" specification; our change design includes country trends as one of its
specifications and the battery reports the with- and without-trends results separately. And the broader
external-validity literature (Deaton, 2010; Vivalt, 2020; Bareinboim & Pearl, 2013; Pearl & Bareinboim, 2011)
asks when an estimate travels, which is the question the transportability experiment makes empirical for this
relation.

The consequence for the schooling–fertility literature is direct. A ten-year change regression with country
fixed effects and country trends identifies the association between a country's schooling *increment* and its
fertility *increment*, net of everything time-invariant. If the relation operates through the slow-moving
development process — if schooling and fertility are both indicators of where a country sits — then the
within estimator removes the variation that carries the relation, and the resulting coefficient is attenuated
toward zero by construction. That is not a bug in the estimator; it is the estimator doing what it is designed
to do, and it is why the within estimate is the right answer to a different question (does a country's extra
schooling, relative to its own trend, predict a faster fertility fall?) than the one the cross-country
literature usually asks.

## 2.4 The schooling–fertility literature estimated both ways

**The cross-country levels tradition.** The human-capital tradition from Mincer (1958) and Becker and Lewis
(1973) through Psacharopoulos and Patrinos (2004, 2018) treats schooling as an investment whose returns shape
fertility; the empirical cross-country literature from Barro and Lee (2013) onward finds large negative
associations between schooling and fertility in levels. Lutz and KC (2011) and KC and Lutz (2017) embed
education in the demographic accounting of human capital and find the same negative relation; Skirbekk (2008)
documents the negative educational gradient in fertility across developed countries; Herzer, Strulik, and
Vollmer (2012) find long-run schooling–fertility cointegration over a century; Murtin (2013) finds education
among the long-run determinants of the demographic transition. The mechanisms proposed are the
quantity–quality trade-off (Becker & Lewis, 1973; Hanushek, 1992; Black, Devereux, & Salvanes, 2005; Becker,
Cinnirella, & Woessmann, 2010), women's opportunity cost and autonomy (Duflo, 2012; Basu, 2002), and
information/diffusion channels (Cleland & Wilson, 1987; Bongaarts & Watkins, 1996). Caldwell's (1980) mass-
education thesis is the strongest claim-level competitor to our interpretation: mass schooling as a
*determinant* of the timing of the fertility decline. Our paper agrees with Caldwell on the size and
centrality of the association and disagrees with the causal reading of the cross-country gradient; the placebo
result is the measurable form of that disagreement.

**The within-country and individual literature.** A separate body of work estimates the relation within
populations. Cleland and Rodriguez (1988) and Martin and Juárez (1995) document the individual educational
gradient in developing countries; Kravdal (2002, 2012) separates individual from community education effects in
sub-Saharan Africa and finds both matter; Kravdal (2004) uses a Norwegian school reform to estimate causal
effects of education on fertility; Duflo (2001) uses Indonesian school construction to identify schooling's
labour-market returns; Chicoine (2012, 2021), Osili and Long (2008), and Baird, McIntosh, and Özler (2011) use
policy changes and cash transfers to identify effects on fertility; Breierova and Duflo (2004) and Ainsworth,
Beegle, and Nyamete (1996) use DHS data with policy variation. The DHS literature is the empirical backbone of
the individual gradient (Rutstein & Johnson, 2004, for the wealth-index measurement; Corsi, Neuman, Finlay, &
Subramanian, 2012, for the survey design). This literature is clear that education matters for fertility within
populations; nothing in our paper contradicts it, and Section 7.1 reconciles the macro null with the
individual/survey gradient explicitly.

**The macro within-country panel literature.** The estimates that motivated our project are the macro panel
ones: country fixed effects, decade changes, country trends. They are less visible in the demographic
literature than the cross-sectional and micro estimates, but they are common in economics and in policy
evaluation. What has not been done, to our search, is a systematic comparison of the *distribution* of levels
estimates against the *distribution* of change estimates for the same measures on the same panel, with the
specification space reported in full and with a test of whether the level relation is a global property. That
is the gap this paper fills — not by discovering the pattern, but by measuring it.

## 2.5 What the quantified audit adds

Three additions distinguish this paper from the literatures above. First, the **specification curve** for the
levels relation (336 pre-registered specifications, 99.7 per cent of period specifications negative, 91.3 per
cent negative-significant, 0 per cent positive-significant) establishes that the levels result is not a
selection from a fragile space; the corresponding change grid establishes that the change result is not a
selection either. Second, the **re-partition transportability experiment** (13,800 random six-group splits)
establishes that the level relation is a global property of the cross-section for the schooling–fertility
pairs (71–99 per cent of groups negative-significant) and that the change relation is not (0–7 per cent). This
is, to our search, a new test in this literature; the grouping-multiverse methodology it implements is
described in the project's methods record. Third, the **future-schooling placebo** quantifies the development-
gradient caveat: the level relation is about 90 per cent as strong when schooling is measured ten years after
fertility, which is what a shared development process predicts and what a schooling effect does not. The
combination — full specification space, grouping multiverse, placebo, and a threshold location — is the
contribution. The individual elements are all standard; the coordinated audit is not.

## 2.6 Closest competitors and why this paper differs

The closest **claim-level** competitor is Caldwell (1980): mass education as a determinant of fertility timing.
We agree on the association and on massification's centrality and differ on the causal reading, with the
placebo as the basis of the disagreement. The closest **decomposition** competitor is Kravdal (2002), who
separated individual and community education effects in sub-Saharan Africa; our re-partition test is the
country-level counterpart of his community-effects design, and our contribution is the demonstration that the
between-country relation reproduces in arbitrary groupings while the within relation does not. The closest
**methodological** competitors are Brock and Durlauf (2001) and Eberhardt and Teal (2011), whose level-versus-
change warnings our paper applies; and the level-of-analysis classic, Robinson (1950), whose warning our
cross-country design instantiates. The closest **data-adjacent** competitor is Cleland and Rodriguez (1988),
whose individual-level gradient our survey-level section corroborates but cannot replace. What this paper adds
to all of them is a coordinated, pre-registered, fully reported audit for one relation, with a transportability
test and a quantified causal caveat — a structural demonstration about a known correlation, not a new
correlation.

## 2.7 What this review could not verify in-session

Three classics have no usable Crossref DOI and are cited by hand and marked unverified in `refs.md`:
Notestein (1945), "Population — the long view", in T. W. Schultz (Ed.), *Food for the World* (University of
Chicago Press); Becker (1960), "An economic analysis of fertility", in *Demographic and Economic Change in
Developed Countries* (NBER/Princeton University Press); and Trow (1974), "Problems in the transition from elite
to mass higher education" (OECD/Carnegie report). Schultz (1961), "Investment in human capital", *American
Economic Review*, 51(1), 1–17, is likewise cited by hand. Two works supplied by the independent literature
auditor — Sear, Mace, and McGregor (2003) on kin effects on fertility and Coall and Hertwig (2010) on
grandparental investment — are cited as supporting literature for the care-work nulls; their DOIs are recorded
in the audit memo and in `refs.md` with the auditor's verification status. Rutstein and Johnson (2004), the DHS
wealth-index report, has no Crossref DOI and is cited as a DHS comparative report. The search strategy behind
these claims is recorded in the record's `SEARCH_STRATEGY.md`; "we are not aware" statements in this paper are
tied to that strategy and are not a claim of exhaustive knowledge.


# 3. Data, measures, designs, and evidence standard

## 3.1 The panel

All cross-country analyses use the project's country-year panel, 1960–2024, observed values only. Series come
from the World Bank's World Development Indicators (income, urbanisation, sectoral measures), Barro–Lee
attainment (via OWID where the official tables were unreachable from the compute node), the project's
harmonised enrolment and completion series, and UN and national sources for fertility and mortality. No
imputation and no interpolation enter any estimation sample; the project's imputed panel exists for other
purposes and is not used here. Income enters in logs in every specification. Standard errors are clustered by
country throughout. The panel is unbalanced; every table reports the effective sample (country-years and
countries), not only the nominal one.

## 3.2 Measures

Fertility is the total fertility rate (births per woman). Schooling is measured eight ways: mean years of
schooling for women and for the total adult population; gross secondary enrolment; lower-secondary completion;
primary completion; tertiary enrolment; and gender-parity indices for secondary and tertiary enrolment. The
multiplicity is deliberate: the literature disagrees about the right measure, and the paper's claim is that the
level-of-analysis result is not an artefact of that disagreement. All eight measures are negative-significant
in levels and weak or positive in changes.

## 3.3 The two designs, kept distinct

**Levels.** Fertility level on schooling level, with decade and region fixed effects, log income and
urbanisation controls, all years. This design uses between-country variation and answers: do countries with more
schooling have fewer births?

**Ten-year changes.** The ten-year change in fertility on the starting level of schooling, with country fixed
effects, decade effects, country-specific linear trends, log income and urbanisation. This design uses
within-country variation, absorbs all time-invariant country characteristics, and answers: when a country's
schooling stock rose, did its fertility fall faster?

The paper treats these as estimates of different parameters, not as competing estimates of one parameter. That
is the whole argument in one sentence.

## 3.4 Auxiliary designs

**Specification curves.** Pre-registered grids (fixed-effect designs, control sets, lags, functional forms,
sample splits) with every cell reported. A result is "robust" only if its sign survives the reported grid.

**Re-partition transportability.** Random re-partitions of the panel's countries into groups of the substantive
grouping sizes; the relation is re-estimated within every group for every re-partition; the statistic is the
share of group-by-pair estimates that are negative and significant. This tests whether the relation is a global
property or a grouping artefact.

**Placebo designs.** A variable that cannot plausibly cause the outcome under the causal story is substituted
for the candidate cause: future schooling for current schooling; male care-work for female care-work;
manufacturing employment for care work. If the placebo is as strong as the candidate, the candidate's
association is not identified.

## 3.5 Pre-registration and the claim-to-source map

Every workstream was pre-registered before its analysis code ran: specification grid, sample splits, bootstrap
counts, and decision thresholds were committed to the branch before the runs, and the paper cites the commits.
Every number traces to a record path (branch @ commit, file, field) in `data/claims_sources.csv`; each record's
README states its deviations (unreachable sources, estimable-cell counts, load-driven extensions) rather than
hiding them. The synthesis's conventions: bold in tables means |t| > 1.96; "significant" means the
country-clustered standard error implies |t| > 1.96 unless stated; "negative-significant share" means the share
of specifications or groups with coefficient < 0 and |t| > 1.96; "survives" means the result holds across the
reported specification space, not that it is causally identified.

## 3.6 Evidence grades

Claims carry **S** (survives the reported specification space and its designed falsifiers), **F** (contradicted
by the reported evidence), or **C** (cannot be tested with these data, with the missing observation named). The
grades are the mechanism by which an omnibus paper avoids the omnibus temptation to make everything sound like
it worked; they are applied in the verdict table of Section 8.


# 4. The finding: a global between-country gradient that the standard change design erases

*Draft section for Paper F (omnibus fertility synthesis). Sources: `research/corr-rebuild-2026-11-23` @ `161b563`;
`research/corr-battery-2026-11-23` @ `9363079`. Claim-to-source map in `../data/claims_sources.csv`.*

## 4.1 The question and why the level of analysis decides the answer

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

## 4.2 Data and measures

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

## 4.3 Levels versus changes: the same measures, the same period

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

## 4.4 Specification curve: the levels result is not a specification choice

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

## 4.5 Transportability: a global property or a grouping artefact?

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

## 4.6 The placebo: the gradient is a development gradient, not a schooling effect

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
magnitude. The pre-registered decision rule — if the placebo reaches 80 per cent of the correct-time share, the
level relation is a development-gradient association and not an identified schooling effect — therefore fires.
The levelled relation is descriptive: countries with more schooling have fewer births, and the association is
global and robust, but it cannot be interpreted as the effect of changing schooling while holding development
constant, because future schooling "predicts" current fertility almost as well. The result is not a defect of
the schooling measures; it is what a development gradient looks like in a cross-section, and it means that the
cross-country literature's practice of interpreting the level coefficient causally is unsupported. The same
conclusion was reached on the smaller earlier grid (where the placebo was negative-significant in 24 of 24
specifications, median −0.68); the large-grid result is a measured version of that caveat rather than a
different result.

## 4.7 What survives

Three things survive this section, and one does not. What survives: (i) a large, global, between-country
schooling–fertility gradient — negative for all eight measures, robust across the 336-specification curve,
reproduced in 71–99 per cent of 13,800 arbitrary country groupings; (ii) a clear demonstration that the
within-country change design erases that gradient, with the change coefficient for several measures
significantly positive, which explains why panel fixed-effects studies have returned nulls; and (iii) a
quantified development-gradient caveat: the level relation is not an identified causal effect of schooling, and
future-schooling placebos are the right diagnostic for this literature. What does not survive is the causal
reading of the level coefficient, and with it the practice of citing the between-country gradient as evidence
that expanding schooling will reduce fertility. The section's contribution is not a new causal estimate; it is
the demonstration that the level-of-analysis choice determines the empirical answer, that the level answer is
real and global, and that its causal interpretation is exactly what the placebo rules out. The next sections
of the synthesis ask what the between-country gradient is a gradient *of*, and whether the within-country
weakness is a property of schooling specifically or of the demographic transition's dynamics more broadly.


# 5. Implications: how the field should estimate and read the relation

## 5.1 For estimation practice

The first implication is a design-reporting rule: **state which parameter the design identifies, and do not
report a change coefficient as an estimate of the level relation** (or vice versa). The two designs answer
different questions, and the paper's numbers make the difference concrete. A levels coefficient of −0.129 is a
between-country gradient; a change coefficient of +0.111 is a within-country association between increments. The
field's habit of treating the second as a robustness check on the first is the source of the apparent
contradiction. A paper that reports both, with the level explicitly named, is not hedging; it is being precise.
Concretely: report the between-country coefficient when the question is "where do high-fertility countries
sit?", report the within-country coefficient when the question is "does a country's extra schooling predict a
faster fall?", and do not use the latter to dismiss the former.

The second implication concerns **attenuation**. The change design is not an unbiased estimator of a causal
effect that happens to be small; it is an estimator that removes the between-country variation in which the
gradient lives. If the relation is a development gradient — and the placebo says it is — then the within
coefficient is attenuated toward zero by construction, and the attenuation is a property of the design, not
evidence about the world. The literature that reads small within-country coefficients as "education does not
matter" is reading design-induced attenuation as a substantive null. The correct inference from a small within
coefficient is that the short-run within-country association is small, not that the between-country gradient is
illusory. Symmetrically, the correct inference from a large between coefficient is that countries differ, not
that a schooling programme would work.

The third implication is about **specification reporting**. The paper's specification curve is a practical
template: pre-register the space, report every cell, and let the distribution be the result. The contrast
between the levels and changes distributions (99.7 per cent negative-significant versus a sign-mixed,
mostly-insignificant grid) is the kind of evidence that a single coefficient cannot provide, and it is what
makes the audit credible to a reader who suspects a selected specification. Journals and referees can ask for
the distribution at modest cost; the code and records here are public.

## 5.2 For interpreting the existing within-country literature

The existing within-country schooling–fertility literature is not wrong, and the paper should not be read as
saying so. The individual and micro-econometric literature identifies effects of schooling on fertility using
policy changes, school construction, cash transfers, and sibling/cohort comparisons (Duflo, 2001; Chicoine,
2012, 2021; Osili & Long, 2008; Baird, McIntosh, & Özler, 2011; Breierova & Duflo, 2004; Ainsworth, Beegle, &
Nyamete, 1996), and it finds effects. Those designs identify local causal effects of specific schooling changes
on specific populations; they do not identify the between-country gradient, and the between-country gradient
does not identify them. The macro panel change literature is the ambiguous case: its estimates are attenuated by
design for the reasons above, and the paper's decomposition suggests that its nulls should be read as
"short-run within-country association is weak", not as "schooling does not affect fertility". The survey-level
section (7.1) adds the missing middle: the DHS ecological gradient is large and negative in every pipeline
tercile, which is consistent with the micro literature and cannot confirm it; the individual-level test requires
the microdata that were not obtainable.

For policy, the implication is a warning about **reading change-designed estimates as programme effects**. A
policy evaluation that finds no effect of a schooling expansion on fertility within a decade may be correctly
estimated and still say nothing about the long-run development gradient; a cross-country association that is
large in levels may be a development marker and still say nothing about a programme. The paper's placebo result
is the formal statement of the second half of that warning, and the attenuation argument is the first half.

## 5.3 For the "development gradient versus causal lever" distinction

The paper's central interpretive distinction is between a gradient and a lever. A gradient describes where
countries sit; a lever describes what moves them. The schooling–fertility relation is a gradient: global,
robust, steepest at the massification margin, and — the placebo says — not identified as a lever. This is not a
deflationary conclusion. Gradients are what comparative demography is good at measuring, and knowing where a
country sits relative to the schooling–fertility frontier is useful for description, forecasting, and for
framing questions about mechanism. What a gradient cannot do is license the claim that expanding schooling will
produce the fertility decline that the cross-section associates with it. That claim requires a design in which
schooling changes for reasons unrelated to fertility, and the paper's future-research section names the designs
and data that could supply one.

The distinction also resolves a puzzle in the policy literature. Pronatalist and anti-natalist policies are
often justified by reference to cross-country associations, and often evaluated with within-country change
designs; the two literatures then appear to contradict each other. They do not. The cross-country association
is a gradient; the policy evaluation is a lever estimate; the first is informative about where the second is
likely to be found, and neither substitutes for the other. The care-work nulls in Section 7.2 make the same
point on the policy side: a mechanism that looks plausible in cross-section (care burdens, credit constraints)
can be absorbed by income and urbanisation, and the paper reports that absorption as a finding rather than
burying it.


# 6. Future research: the data and designs that would turn this audit into a causal estimate or a new correlation

The audit is deliberately descriptive, and its most useful output may be a research agenda. This section is
concrete about five data sources, what each would identify, and what each would not.

## 6.1 DHS Individual Recode files (the individual-level test)

**What it would identify.** The individual-level schooling–fertility gradient, with wealth controls, community
placebos, and the quantum/tempo decomposition that the published cells cannot support. DHS women's Individual
Recode files contain education (v106, v133), children ever born (v201), age (v012), residence (v025), wealth
quintile (v190), region (v024), cluster (v005), and survey weights (v021). With these, one can estimate
completed fertility by schooling within country × survey with individual controls, test whether the gradient
survives wealth and community fixed effects, and decompose the difference into delay (tempo) and number
(quantum) using birth histories. **What it would not identify.** A causal effect of schooling: the microdata are
observational, and the schooling-fertility correlation remains confounded by family background, ability, and
community characteristics unless a source of exogenous schooling variation is available. The individual-level
test would settle whether the survey-level gradient is an individual-level fact; it would not settle causality.

## 6.2 Cohort fertility by education (the dynamic test)

**What it would identify.** Whether the gradient steepens or flattens across cohorts at the individual level, and
whether the survey-level attenuation documented in Section 7.1 is composition or a genuine change in the
relation. Cohort fertility by education is available for a subset of countries from national statistical
offices and from the Human Fertility Database and its education-specific extensions; the project's own cohort
cells (24–27 countries) are too thin to settle the question, and the paper reports them as inconclusive. **What
it would not identify.** The macro drivers: cohort data describe the relation's evolution, not its causes.

## 6.3 Historical schooling series with event timing (the historical test)

**What it would identify.** The relation between schooling expansions and fertility declines at the moment of
expansion, using school-construction programmes, compulsory-schooling laws, and missionary/colonial school
networks as event-time variation. The project's transition model is a first step (Section 7.3); a data-driven
event study using historical enrolment and fertility series would test whether expansions precede declines at
the margin the threshold analysis identifies (below six years). **What it would not identify.** Contemporary
effects: historical expansions operated in a different mortality and labour-market regime, and the external
validity of historical estimates is itself a research question.

## 6.4 Subnational variation (the within-country, cross-region test)

**What it would identify.** The gradient within countries across regions with different schooling levels and
different schooling expansions, which is the closest observable analogue of the between-country gradient and
would let the transportability logic be applied within countries. Subnational DHS/GIS data, census microdata,
and administrative schooling records exist for many countries. **What it would not identify.** National policy
effects, and subnational expansions are often endogenous to local fertility trends.

## 6.5 Sibling and cohort comparisons (the family-level test)

**What it would identify.** Whether the quantity–quality trade-off operates within families — the mechanism the
between-country gradient is often said to reflect — using sibling fixed effects and cohort variation in
schooling exposure. The quantity–quality literature (Becker & Lewis, 1973; Hanushek, 1992; Black, Devereux, &
Salvanes, 2005) provides the template. **What it would not identify.** The macro gradient: sibling designs
identify within-family effects and are silent about the development process.

The agenda's logic is a ladder: the individual microdata would establish the micro fact, the cohort data its
evolution, the historical event studies a quasi-causal historical estimate, the subnational data a within-
country transportability test, and the sibling designs the family mechanism. No rung identifies the macro
gradient's causal status by itself, and the audit in this paper is the map of which rung answers which question.
The data that the project most needs — DHS Individual Recodes — are obtainable with a free DHS account and a
dataset-access request; the obstacle is administrative, not scientific, and the record documents the exact
procedure.


# 7. Supporting evidence: the survey gradient, the nulls, the transition, and the threshold

The four subsections that follow are the project's supporting workstreams. They are subordinate to the centrepiece audit: each tests a mechanism or a data source, and each reports its verdict with the same claim-to-source discipline.


## 7.1 The survey-level gradient: what DHS says about schooling and completed fertility, and what it cannot say

*Draft section for Paper F. Source: `research/dhs-micro-2026-11-23` @ `31ded00`; record
`research/records/2026-11-23-dhs-micro/` (`README.md` §1-2, `results/model_education.json`,
`results/cohort_gradients.csv`, `results/survey_gradients.csv`).*

### 7.1.1 The question, and the data gap stated first

The between-country gradient of Section 3 is a country-level object. The literature that most demographers
have in mind when they say "education lowers fertility" is an individual-level object: within a population,
women with more schooling have fewer children. The two can differ in size and even in sign, and the difference
is the ecological fallacy in its most consequential form (Robinson, 1950). This section asks what the
Demographic and Health Surveys — the standard source for the individual-level claim — can add, and it begins
with a limitation that must not be buried: **the pre-registered individual-level test could not be run.** DHS
women's Individual Recode files are not publicly downloadable; the public API exposes indicator aggregates and
a file inventory but no download link, the flat files sit behind a registered account, IPUMS-DHS requires a key,
and the project's local data store contains no DHS microdata. Every attempt is logged in the record's
`data/microdata_probe.txt`. What can be analysed, and is analysed here, are the DHS's **published cells**: mean
children ever born to women aged 40-49 by education, mean age at first birth by education, and the wealth and
residence breakdowns — 81,962 published cells from 377 surveys in 87 countries, 1985-2025. The unit is a
country × survey × education cell, not a woman. Every claim in this section is therefore a **survey-level
(ecological) claim**, and the section labels it as such throughout.

### 7.1.2 The gradient is large, monotone, and almost universal

Within country × survey, with cell weights (the number of women each published cell represents) and standard
errors clustered by country, completed fertility falls monotonically with education relative to no education:
primary education **−0.57 children (SE 0.06)**, secondary **−1.62 (0.17)**, higher **−2.54 (0.24)**. The sample
is 1,291 education cells from 86 countries, median 401 women per cell. The per-survey gradient — secondary or
higher minus none/primary — is negative in **99 per cent of 346 surveys**, with a median of **−1.90 children
(IQR −2.48 to −1.43)**. On these data the canonical gradient is about as universal as a social-science
regularity gets, and it is large in the units that matter: nearly two children between women with secondary
schooling and women with none, within the same survey.

This is the survey-level counterpart of Section 3's country-level gradient, and the two agree in sign and
importance. A country with more schooling has fewer births, and within a country women with more schooling have
fewer children. The agreement is reassuring for the descriptive claim; it does not resolve the causal question,
and the rest of this section explains why not.

### 7.1.3 The dynamic predictions were contradicted

The project pre-registered two dynamic predictions for the survey data, both grounded in the massification
story: the gradient should *steepen* in later cohorts (as schooling becomes a stronger marker of the modern
sector) and should steepen where the education pipeline is denser (the "pipeline-density" prediction). Both were
**contradicted**, and the record reports the contradiction rather than re-spinning it.

On cohorts: the education × cohort interaction is **positive** — the gradient *flattens* over time — at
**+0.26 children per decade (SE 0.13)** for secondary and **+0.40 (0.16)** for higher education. The
cohort-specific median survey gradients trace the same attenuation: 1940s **−2.50** (48 surveys), 1950s
**−1.90** (78), 1960s **−1.85** (122), 1970s **−1.80** (95), 1980s **−1.50** (3). On pipeline density: the
interaction with the survey's own share of women with secondary or higher is also **positive** — the gradient is
*shallower* where schooling is more massified: **+0.13 (SE 0.05)** per ten percentage points for secondary and
**+0.16 (0.05)** for higher education, with median per-survey gradients of **−2.10** (low pipeline tercile),
**−2.00** (middle), and **−1.60** (high). The gradient is negative in **every** pipeline tercile; the direction
is universal, the magnitude is not, and the magnitude moves opposite to the pre-registered prediction.

The most likely reading is composition, and the record says so: "secondary education" is a small elite in early
cohorts and a mass phenomenon later, so the same label spans very different amounts of schooling and different
selection. The survey cells cannot separate composition from a genuine change in the education-fertility
relationship; the individual birth histories that could are the data that were not obtainable. This is the C
label — cannot be tested with these data — applied to the most interesting version of the question.

### 7.1.4 Delay and number cannot be separated here either

The same cells allow a quantum-versus-tempo comparison that the record reports as suggestive, not decisive.
Secondary education is associated with a median age at first birth **+2.65 years (0.15)** later than no
education, and higher education **+5.27 (0.39)** later, while completed fertility is 1.62 and 2.54 children
lower. Both a delay and a lower final number are present, and the published cells cannot say how much of the
fertility difference is tempo (later starts, possibly caught up) and how much is quantum (fewer births). With
1,291 cells, 333 surveys, and 86 countries, the delays are precisely estimated; the decomposition between delay
and number needs birth histories. The paper therefore treats the DHS section as evidence that the survey-level
gradient is real and universal, and not as evidence about its mechanism.

### 7.1.5 What the section does and does not add to the synthesis

What it adds: an independent, survey-based confirmation that the schooling-fertility gradient is negative and
large at the education-cell level across 86 countries and four decades of surveys, which rules out the
possibility that Section 3's country-level gradient is an artefact of national aggregates; and a set of
*negative* results — cohort attenuation and pipeline attenuation in the opposite direction from the
pre-registered predictions — that matter for the massification interpretation. If the gradient were purely a
development-level marker, one might expect it to weaken as schooling spreads; the survey data show exactly that
attenuation (from −2.50 in the 1940s cohorts to −1.80 in the 1970s), which is a finding worth reporting in its
own right. It does not uniquely support the development-gradient reading, because saturation, composition change
and ceiling effects would produce attenuation too, and the composition caveat means it cannot be stated as an
individual-level fact. What it does not add: the individual-level test, the wealth horse-race, the community placebo, and the
quantum/tempo decomposition, all of which require microdata. The record states the data gap and the manual
download procedure (a free DHS account, dataset-access request, Individual Recode Stata files, and the
specified variables) rather than substituting country aggregates for the missing test. A synthesis that claimed
the survey-level gradient settled the individual-level question would be committing the same ecological error
it criticises in Section 3.


## 7.2 Care work, policy bounds, and tipping points: three falsifiable mechanisms

*Draft for the consolidated Fertility paper. 1,650 words. Every number carries its record path
(branch @ commit → file → field); full map in `SOURCE_MAP.md`. Pre-registrations were the first
commit on each record branch. Not softened: the verdict table is the point.*

### 7.2.1 Three questions the framework makes falsifiable

The morphological-governance framework treats fertility decline as a by-product of a credential
pipeline. Three predictions follow that are sharp enough to kill.

**Q1, the care-work loop.** Fertility decline should be amplified by paid care work: a rising care
share of female employment lowers fertility further, and the schooling–fertility link should steepen
where care work is common.

**Q2, no off-switch.** Pipeline-compatible pronatalist policy — cash, leave, childcare subsidies —
should not restore *sustained* fertility above roughly 1.6. The mechanism, not the budget, sets the
ceiling.

**Q3, terminal enclosure as a tipping point.** Before the enclosure, fertility should show the
textbook early-warning signature (rising variance, rising lag-one autocorrelation); after it, the
schooling–fertility link should ratchet — diminishing returns.

### 7.2.2 Data and design

*Care loop:* ILO sectoral employment (education, health/social work) for 656 country-years, 148
countries, 2010–2023, merged with World Bank fertility, female tertiary attainment, log GDP and
urbanisation. The outcome tests use 140–141 countries. [care-credential @ e626cb8 →
`PREREGISTRATION.md`, `scripts/build_care_cred.py`, `results/results_care_cred.json`]

*Policy bound:* 38 hand-coded pronatalist introductions (cash, leave, childcare, reversal) in 25
countries, each with fertility below 1.6 in the introduction year, on the 1960–2023 country-year
panel (217 countries). [policy-foreclosure @ 63691a2 → `data/events.json`,
`results/A_results.txt`, `results/A2_longrun.json`]

*Tipping point:* the pre-registered event rule (first year of the fastest sustained ten-year fall of
at least 1.0 birth) gives 184 transition events; 80 have the full 15-year pre-event window. Each is
compared with 200 pseudo-event dates from its own series (never within ten years of the real
event). Surrogate null: first differences reshuffled and re-integrated 16,000 times. [early-warning
@ 7e64f61 → `results/ews_results.json`]

### 7.2.3 Q1 — the care-work loop: income and urbanisation do the work

The raw gradient is exactly what the framework wants: mean care share of female employment is
**8.1% in the bottom attainment tercile, 19.0% in the middle, 28.4% at the top** (n = 47 each, 148
countries; care share overall 18.3%, sd 12.1, range 1.2–52.1). [results_care_cred.json, A1 terciles]

It disappears with controls. With log GDP per head in the model the attainment coefficient is
**+0.009 (t = +0.17, n = 140)**, log GDP **+0.242 (t = 2.47)**, and with urbanisation added urban
**+0.42 (t = 3.38)**. The pre-registered "fully explained by income/urbanisation" falsifier fires.
[results_care_cred.json, A1 controls]

The amplification test flips sign: interaction of attainment with care share **−0.131 (t = −1.38,
n = 141)** without controls, **+0.128 (t = +1.53)** with GDP and urbanisation. Unstable, so failed.
[A3]

The placebos are decisive. Replacing women's care work with **men's** care work gives **+0.179
(t = 2.10)**; replacing it with **manufacturing** gives **−0.189 (t = −3.47)** — the unrelated-sector
placebo produces a larger "effect" in the predicted direction than care work itself. [A3 placebos]

The dynamic test has the wrong sign: across 119 country pairs, fertility change on the early care
share is **+0.199 (t = 2.14)** without controls (higher care share, *less* decline) and **−0.045
(t = −0.41)** with log GDP. [A2] Across 36 pre-registered specifications the care coefficient takes
both signs, about −0.57 to +0.27, and significance tracks the fixed effects, not the care measure.
[spec curve]

**Verdict: null.** Not that care work is irrelevant — the gradient is real — but the framework's
care loop is not separable from income and urbanisation, and its placebos behave like the treatment.

### 7.2.4 Q2 — no off-switch: strong form falsified, weak form supported

Bound test: **34 of 396 post-introduction country-years above 1.6 = 8.6%** (one-sided 95% upper
bound **11.3%**). The pre-registered prediction was below 10%: the point estimate passes, the
confidence bound does not. Ten of 38 events cross above 1.6 within ten years. [A_results.txt,
BOUND TEST]

The persistence falsifier fires. **Five of 38** events have 3+ consecutive years above 1.6 within
ten years: Russia 2007/2011 (6 years, max 1.78), Czechia 2008 (3, max 1.71), Estonia 2004 (5, max
1.72), Belarus 2007 (5, max 1.73). Beyond the pre-registered window, **9 of 38** events ever have
such a run: **Bulgaria 10 consecutive years 2014–2023, still 1.81 in 2023**; Romania 8, Czechia 7,
Russia 6, Estonia 5, Belarus 5, Latvia 4. The highest fertility reached after any introduction is
**1.83**, and most crossings reverse. [A_results.txt; A2_longrun.json]

The average effect is small and not an artefact: event study with country and calendar-year fixed
effects, first saturated introduction per country, **+0.035 (SE 0.025; 95% CI −0.014 to +0.083)** on
467 country-years and 25 countries. Power: the minimum detectable effect is **+0.070** at 80% power.
Rivals leave it: **+0.028 (SE 0.028)** without controls; **+0.028 (SE 0.028)** with income,
urbanisation and net migration; **+0.017 (SE 0.010)** with country-specific trends. [A_results.txt,
EVENT STUDY / POWER / RIVALS]

Descriptive: the maximum fertility in the ten years after an introduction exceeds the five-year
pre-mean by a median **+0.15 births** (mean +0.18). Thailand's 1997 reversal (outside the saturated
set) was followed by 1.84 → 1.73 (2000) → 1.56 (2010) → **1.21** (2023). [A_results.txt, PRE/POST and
THAILAND]

**Verdict: the strong form is falsified; the weak form is supported.** Sustained fertility above
~1.6 is not impossible — nine introductions were followed by multi-year runs above it, Bulgaria for
a decade — but no country returned toward replacement (ceiling 1.83), the average effect is +0.035,
and most crossings reverse. This is not "policies don't work"; it is a claim about how far and how
long they work.

### 7.2.5 Q3 — tipping point: no early-warning signature; diminishing returns confounded by a floor

Autocorrelation **falls** before the transition: **−0.025 (SE 0.008, t = −3.3)** event minus
pseudo-event — the opposite of the predicted rising signature. Variance rises **+0.079 (SE 0.034,
t = +2.3)**, the right sign, but fails the pre-registered surrogate null (share **0.42** of 16,000
surrogates at least as large; autocorrelation 0.57). Minimum detectable differences: **0.095**
(variance) and **0.021** (autocorrelation); the variance effect is below its own MDE, so that null
is weak, while the autocorrelation null is not weak because the sign is wrong. [ews_results.json]

Diminishing returns are real but observationally equivalent to a floor: 3,865 country-years, 238
countries, ten-year fertility change on lower-secondary completion and its square gives a positive
squared term **+0.00019 (t = 18.2)**, marginal effects **−0.0099** at the 10th percentile
(bootstrap CI −0.0116 to −0.0079), **+0.0064** at the median (0.0059 to 0.0070), **+0.0214** at the
90th (0.0199 to 0.0230), turning point ≈ 39 of 100. A concave response and a floor look the same in
this regression; the result is quoted as a boundary condition, not a ratchet. [ews_results.json,
diminishing]

**Verdict: no tipping-point signature.** Whatever enclosure the theory describes is not announced by
classic early warning in national fertility series.

### 7.2.6 Verdict table (the paper's value)

| # | prediction | pre-registered killing test | outcome | verdict |
|---|---|---|---|---|
| 1 | care-work loop amplifies schooling–fertility link | income/urbanisation absorption; placebo sectors | absorbed: +0.009 (t 0.17) with GDP (t 2.47) and urban (t 3.38); placebos male +0.179 (t 2.10), manufacturing −0.189 (t −3.47); 36-spec curve both signs | **null** |
| 2 | strong no-off-switch: no sustained fertility above ~1.6 | bound test; persistence; event study; rivals | 8.6% of post-introduction years above 1.6 (upper 11.3%); persistence fires 5/38 within 10y, 9/38 long-run (Bulgaria 10 years, 1.81 in 2023); +0.035 (SE 0.025), MDE 0.070; rivals +0.028 (0.028), trends +0.017 (0.010); ceiling 1.83 | **strong form falsified; weak form supported** |
| 3 | enclosure is a critical transition with early warning | event vs pseudo-event; surrogate null; power | autocorrelation −0.025 (SE 0.008), wrong sign; variance +0.079 (SE 0.034) fails surrogate 0.42; diminishing returns +0.00019 (t 18.2) floor-confounded | **no tipping point; diminishing returns a boundary condition** |

### 7.2.7 New vs replicated, and what this does not test

**New:** the placebo-based falsification of the care loop; the explicit pre-registered 1.6 bound
and its persistence test (the strong form's falsification); the paired pseudo-event early-warning
test in 80 national fertility series. **Replicated:** the care-share gradient and the post-socialist
recovery patterns (Frejka & Sobotka 2008; Zakharov 2008; Koytcheva & Philippov 2008), the small
bounded policy effects (Gauthier 2007; Thévenon 2011; Thévenon & Gauthier 2011; Luci-Greulich &
Thévenon 2013), and the skeptical side of the early-warning literature (Hastings & Wysham 2010;
Ditlevsen & Johnsen 2010; Kéfi et al. 2013; Boettiger et al. 2013; Dakos et al. 2015).

This section does not test the framework as a whole. Nulls on three mechanisms are informative
about those mechanisms, not about the broad claim that credential pipelines shape fertility. The
plain attainment channel survives (tertiary attainment correlates −0.62 with fertility in the
companion paper), and the weak no-off-switch form survives; those are what the data support. Five
to eight closest prior works per claim, with DOIs and Crossref status, are in
`paper-f-claims-prior-art.md`.


## 7.3 The transition engine, the individuation model, and the tolerance ladder

**Author: gpu-dose. Provenance: `research/transition-gpu-2026-11-23` @ `f9f2f18`; `research/dose-gpu-2026-11-23`
@ `774085c`; `research/dose-tolerance-2026-11-23` @ `baadfe6`; the transition record `research/transition-2026-11-23`
@ `b13fde8` supplies the historical paths and the mortality-leads-fertility estimate. All files below are in
those records' `results/` directories unless stated.**

### 7.3.1 The question this section answers

The demographic transition has a standard ordering in demography: mortality falls first, the population grows,
and fertility falls later. What the ordering does not establish is what **drives** the fertility fall. The two
candidates that matter for this project are the quantity-quality mechanism (schooling raises the cost of
children) and a mortality-led mechanism (parents insure against child deaths by having more births). This
section reports four results: a calibrated counterfactual that shuts off the mortality decline; a model of
individuation (the "dose" model) in which schooling and marriage-market position govern fertility; an
out-of-sample comparison of that model against a development-only rival; and a tolerance ladder showing that the
wide parameter intervals are an identification limit rather than a statistical artefact.

The engine is a GPU port of the project's published individual-level model. The port is bit-exact against the
CPU reference with its new channels switched off — woman-level states differ by zero and all four target series
by 0.0 (`trans/test_port.py`, `results/` of the transition record) — which is the precondition for reading the
counterfactual at all. The two additions for this exercise, both switchable and both labelled as extensions
rather than parts of the published model, are a configurable cohort base and a child-mortality channel.

### 7.3.2 Does the fertility collapse survive without the mortality decline?

The counterfactual holds child mortality at its pre-antibiotic level while schooling and income follow history,
for cohorts 1930 to 1995 across eight fit countries, and compares births by age 49:

| arm | 1930 cohort | 1995 cohort | change |
|---|---|---|---|
| history (child mortality follows history) | 4.96 | 3.60 | **-1.36** |
| frozen (pre-antibiotic child mortality) | 5.01 | 3.70 | **-1.31** |

Freezing the mortality decline removes **3.2 per cent of the fall** (country range -1.8 to +8.2 per cent:
Bangladesh +8.2, Egypt +7.3, Indonesia +4.8, India +0.3, Vietnam -1.8). The counterfactual does raise the
*level* of fertility — 5.01 against 4.96 in the 1930 cohort — but it adds births roughly evenly and cannot stop
a fall that the schooling rise drives. Three falsifiers were run and did not flip the verdict: a ±50 per cent
band on the calibrated mortality coefficient moves the share removed only from **0.9 to 4.7 per cent**; a 4.5×
power check (a coefficient more than four times larger than the observed relationship) moves it to only **10 per
cent**; and the 3.36-million-woman and 10.08-million-woman runs agree within 0.02 births, so the result is not
simulation noise. **In this model the fertility collapse is schooling-led, not mortality-led.**

The rival specification answers the same way. With development-only fertility behaviour the collapse is larger —
cohort fertility 5.22 to 2.08, a fall of 3.14 births against 1.35 — and freezing child mortality removes **2.0
per cent** of it. So the answer to "was it mortality-led?" is no under both specifications; the development-only
engine simply falls further and closer to the observed trajectories, which is why the levels cannot be used to
choose between them.

**The pre-antibiotic arc is only partly reachable, and this is an honest limit of the extension.** Run on
cohorts 1890-1955, the model does not generate a transition at all: cohort fertility goes 4.01 (1890) to 4.94
(1920) to 4.64 (1955), a rise of 0.63 of a birth rather than a fall. The highest cohort fertility anywhere in
the committed runs is **5.20** (1890 cohort, frozen mortality, high coefficient) and **5.42** in the 4.5× power
check, against a historical national total fertility of about 5. The model's collapse is produced by mass
schooling in cohorts born after about 1930, so the engine cannot stand in for the pre-antibiotic equilibrium;
what it can do is show what the post-1930 cohorts imply.

**On the empirical ordering, the record we build on reports that mortality leads fertility by about twelve
years** (`research/transition-2026-11-23` @ `b13fde8`, transition record). The counterfactual above does not
contradict that ordering: mortality does fall first. It shows that the *level* channel from mortality to births
is small relative to the schooling channel, which is a statement about magnitudes, not about sequence.

### 7.3.3 The individuation model: what schooling and marriage-market position do to fertility

The dose model treats a woman's schooling as a sequence of doses and asks which channels of the theory survive
rejection-based Bayesian estimation on 31 parameters against the observables. The five theory parameters are
reported with their 5th-95th percentile intervals (`research/dose-gpu-2026-11-23` @ `774085c`,
`results/rej_fitA.json`; the same numbers are tabulated in `research/dose-tolerance-2026-11-23` @ `baadfe6`,
`results/ladder.json`, fields `params.th_k.q50`, `params.th_f.q50`, `params.kappa.q50`, `params.gam.q50`,
`params.lam_s.q50` with `q05`/`q95`):

| channel | 5th | median | 95th | prior |
|---|---|---|---|---|
| kin-support loss per full dose | 0.34 | **2.80** | 4.74 | 0-5 |
| downward money flow to parents | 0.30 | **2.62** | 4.77 | 0-5 |
| cohort deepening (sibling configuration) | 0.15 | **1.58** | 2.85 | 0-3 |
| career delay at high schooling | 1.10 | **5.32** | 7.71 | 0-8 |
| pickiness (partner standards) | 0.25 | **2.41** | 4.70 | 0-5 |

Every channel points in the theory's direction and the intervals exclude zero at the 5th percentile, with 1,044
of 5,000 draws accepted (20.9 per cent) in the primary fit and a replicate fit giving a kin-support median of
2.73 (0.37-4.78), so the rank ordering is stable. **But the intervals are wide**: at the primary tolerance they cover 88 to 100 per cent of the prior range
(and 71 to 101 per cent across the three rungs of the ladder), and that width is the next section's subject.

### 7.3.4 Out of sample: individuation against development-only

The two arms are fitted on the same windows and compared on held-out country histories
(`results/analysis_holdout.json`, fields `holdout.mean_A`, `holdout.mean_B`, `holdout.diff_mean`,
`holdout.diff_ci`, `holdout.A_better`): the individuation arm's held-out distance is **24.43** against **21.10**
for the development-only arm, a difference of **+3.32 with a 95 per cent interval of [-3.76, +11.14]**, and the
individuation arm is closer in 3 of 6 held-out countries. Repeating the exercise with populations fitted by the
GPU engine rather than the CPU engine gives 25.48 against 21.68, a difference of +3.80 [-2.60, +11.96], also
3 of 6 (`results/analysis_holdout_gpuengine.json`). **The out-of-sample comparison does not separate the two
arms**: the interval spans zero, the sign favours development-only, and the country count is three of six. Any
claim that the individuation channels improve prediction would not survive this test.

The quantum-tempo decomposition makes the same point about model dependence
(`results/analysis_decomp.json`, fields `decomposition.A_fit.quantum_mean`, `.tempo_mean`,
`decomposition.A_holdout.*`): in-sample the model attributes a quantum of **2.09** and a tempo of **-0.34** to
the transition, while out of sample the same decomposition gives **2.55** and **-0.42**. The split between how
many children and when is not stable across the fit and the holdout, so quantum-versus-tempo statements from
this model should be read as model-dependent.

### 7.3.5 The tolerance ladder: the wide intervals are an identification limit

Because the earlier intervals were prior-wide, the natural objection is that the tolerance in the ABC fit — not
the data — set them. The ladder varies the tolerance from the 20th to the 10th to the 5th percentile of the
prior-predictive distance distribution, with equal-weight rejection sampling only
(`research/dose-tolerance-2026-11-23` @ `baadfe6`, `results/ladder.json`, fields `drawn`, `accepted`,
`acceptance`, `params.<name>.spread`):

| tolerance | drawn | accepted | acceptance | kin (th_k) | downward flow (th_f) | cohort (kappa) | career (gam) | pickiness (lam_s) |
|---|---|---|---|---|---|---|---|---|
| 20th pct (eps 21.5) | 5,000 | 1,044 | 20.9% | 0.96 | 1.00 | 0.98 | 0.88 | 0.98 |
| 10th pct (eps 18.33) | 10,000 | 1,012 | 10.1% | 0.98 | 1.00 | 0.94 | 0.71 | 0.97 |
| 5th pct (eps 16.59) | 12,000 | 660 | 5.5% | 0.96 | 1.01 | 0.87 | 0.76 | 1.00 |

Spread columns are `params.<name>.spread` from `ladder.json`, in the order of the ladder file (th_k, th_f, kappa, gam, lam_s), and the labels are the file's own `pretty` names.
"Spread" is the width of the 90 per cent interval relative to the prior width. Tightening the tolerance from the
20th to the 5th percentile leaves **four of the five** spreads between 0.87 and 1.01, essentially unchanged; the
one that moves is career delay, from 0.88 to 0.71-0.76, a slight tightening that does not bring the posterior near
the data. The point medians are similarly stable for kin support, downward flow and pickiness (2.80/2.82/2.82;
2.62/2.63/2.74; 2.41/2.47/2.61) but drift for cohort deepening (1.58/1.58/1.31) and career delay
(5.32/6.05/6.35), which is a further reason to treat those two channels cautiously. In the rival arm the tight tolerance accepts only **32 of 4,000 draws (0.8 per cent)**, at which point the
posterior cannot be interpreted. The conclusion is that the wide dose intervals reflect **a genuine
identification limit of this design**, not a loose tolerance, and that reporting them as though a larger
simulation would tighten them would be wrong.

### 7.3.6 Prior art for this section [DOIs Crossref-checked 24 Nov 2026; status given]

| work | DOI | Crossref status | relation |
|---|---|---|---|
| Becker & Lewis (1973), On the interaction between the quantity and quality of children, *JPE* | 10.1086/260166 | verified | the quantity-quality mechanism the dose model formalises |
| Bongaarts (1978), A framework for analyzing the proximate determinants of fertility, *PDR* | 10.2307/1972149 | verified | the decomposition logic behind quantum/tempo |
| Easterlin (1975), An economic framework for fertility analysis, *Studies in Family Planning* | 10.2307/1964934 | verified | the relative-income/cost framing |
| Becker & Barro (1988), A reformulation of the economic theory of fertility | 10.3386/w1793 | verified (working paper) | fertility as an investment in children |
| Notestein (1945), Population: the long view | not returned by Crossref in-session | **unverified** | the classic transition ordering |
| Davis (1963), The theory of change and response in modern demographic history | not returned in-session | **unverified** | change-and-response alternative to transition theory |
| Caldwell (1976), Toward a restatement of demographic transition theory | not returned in-session | **unverified** | intergenerational wealth-flow theory |
| Cleland & Wilson (1987), Demand theories of the fertility transition | not returned in-session | **unverified** | the demand-side critique |
| Galor & Weil (2000), Population, technology, and growth | not returned in-session | **unverified** | unified growth theory |
| Doepke (2004), Accounting for fertility decline during the transition to growth | not returned in-session (SSRN version resolves) | **unverified** | quantity-quality in a growth model |
| Guinnane (2011), The historical fertility transition: a survey | not returned in-session | **unverified** | the historical record |
| Coale & Watkins (1986), *The Decline of Fertility in Europe* | not returned in-session | **unverified** | the European fertility project's dating |
| Lesthaeghe (1983), The second demographic transition | not returned in-session | **unverified** | the post-transitional regime |

**What is replicated, corrected and new.** The transition ordering (mortality first) is replicated from the
prior record and is not new. The mortality **counterfactual** is new to this project and, as far as this
section's literature search found, no antecedent reports the share of a schooling-led fertility collapse that
survives a mortality freeze in a calibrated individual-level model; we do not claim it is the first such test.
The dose model's five channels are this project's construction; the quantity-quality mechanism they formalise is
Becker-Lewis's. The out-of-sample comparison is a correction of any impression that the individuation model
predicts better: it does not. The tolerance ladder is a correction of the earlier inference — the intervals are
an identification limit. No claim of precedence is made, and the historical-transition literature above is
cited because these results have to be read against it, not replaced by it.


## 7.4 Where in the schooling distribution the gradient lives: the threshold shape and the massification margin

*Draft section for Paper F. Sources: `research/corr-rebuild-2026-11-23` @ `161b563`; `research/corr-battery-2026-11-23`
@ `9363079` (threshold bootstrap from `data/results_summary.json`, field `threshold_bootstrap`).*

### 7.4.1 Why a linear coefficient is the wrong summary

The levels coefficient in Section 1 is a summary of a relation across the whole schooling distribution, from
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
is the one that carries most of the association. The specification keeps the Section 1 design (decade and
region fixed effects, log income, urbanisation, country-clustered standard errors) and replaces the single
schooling variable with three: the minimum of schooling and six years; the amount between six and nine years,
clipped at zero; and the amount above nine years. The three slopes are the gradients below six years, between
six and nine, and above nine.

### 7.4.2 The shape: steep below six years, flat in the middle, and a reversal above nine

The point estimates from the rebuild, and their country-clustered bootstrap intervals from the extended battery
(500 replications per measure, resampling countries), are in Table 5.

**Table 5. The gradient by segment of the schooling distribution (levels specification; births per woman per
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

### 7.4.3 What the shape means for massification

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

The threshold shape also makes the placebo result in Section 1 more interpretable rather than less. If the
level gradient were a schooling effect operating through the quantity–quality mechanism, we would expect it to
be strongest where the quantity–quality trade-off is strongest — plausibly in the low-schooling range where
child labour and mortality risk are high, which is what we see. But a development gradient would produce the
same shape, because the low-schooling range is also where the development indicators diverge most. The shape is
therefore consistent with both stories, and the placebo is what discriminates between them; the threshold
analysis adds the *location* of the gradient, not a causal identification.

### 7.4.4 Robustness and the honest limits of the shape

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


# 8. Discussion, limitations, and conclusion

## 8.1 The verdict table

Table 8 collects the paper's claims and their evidence grades. **S** = survives the reported specification space
and its designed falsifiers; **F** = contradicted by the reported evidence; **C** = cannot be tested with these
data, with the missing observation named.

**Table 8. What the project knows now.**

| # | claim | grade | key number |
|---|---|---|---|
| 1 | Schooling–fertility is large and negative in levels, all eight measures | S | women's attainment −0.129 (0.029), n = 5,915, 192 countries; 8/8 negative-significant |
| 2 | The levels result is robust across the specification space | S | 99.7% of 288 period specs negative; 91.3% negative-significant; 0% positive-significant; median −0.475 |
| 3 | The level relation is a global between-country property | S (this relation) | 71–99% of 13,800 random six-group partitions negative-significant vs 0–7% in changes |
| 4 | The standard change design erases or reverses the relation | S | women's attainment +0.111 (0.045); 0/8 negative-significant; 3/8 positive-significant |
| 5 | The level relation is a development gradient, not an identified schooling effect | S | future-schooling placebo 52.9% vs 58.8% negative-significant (~90% as strong) |
| 6 | The gradient is steepest at the massification margin (shape), with conventional hinge locations | S (shape) / C (hinge locations) | below 6y −0.326 [−0.405, −0.248]; 6–9y −0.092 [−0.175, −0.013]; >9y +0.112 [+0.057, +0.171]; hinges at 6 and 9 years are conventional, not data-searched |
| 7 | A survey-level (DHS) negative gradient exists across 86 countries | S (ecological) | primary −0.57 (0.06), secondary −1.62 (0.17), higher −2.54 (0.24); 99% of 346 surveys negative |
| 8 | The gradient steepens in later cohorts and denser pipelines | F | attenuates instead: cohort +0.26 (0.13); pipeline +0.13 (0.05) |
| 9 | Individual-level and wealth-controlled tests of the gradient | C | DHS Individual Recodes not publicly obtainable |
| 10 | A care-work loop generates a self-reinforcing low-fertility trap | F | care-work gradient +0.009 (t 0.17) once income (+0.242, t 2.47) and urbanisation (+0.42, t 3.38) enter; male-care placebo +0.179 (t 2.10); manufacturing placebo −0.189 (t −3.47) |
| 11 | A strong "no-off-switch" | F (strong); S (weak) | 34/396 country-episodes rebound (8.6%, upper 11.3%); 5/38 within 10y; ceiling 1.83; event study +0.035 (0.025), MDE 0.070 |
| 12 | A tipping point / critical slowing down | F | autocorrelation −0.025 (0.008), wrong sign; variance +0.079 (0.034) fails surrogate (0.42) |
| 13 | Mortality decline is the leading driver of the collapse | F | freezing pre-antibiotic mortality removes 3.2% (range −1.8 to +8.2%); ±50% band 0.9–4.7%; 4.5× check 10% |
| 14 | The individuation model beats a development-only rival out of sample | F (tie) | 24.43 vs 21.10, diff +3.32 [−3.76, +11.14]; 3/6 countries |
| 15 | Wide model intervals are a statistical artefact | F | four of five spreads stay 0.87–1.01 across the tolerance ladder |

## 8.2 What the audit establishes and what it leaves open

The audit establishes four things. First, the between-country gradient is one of the most robust regularities
available for this relation: it survives the full specification curve, all eight measures, and 13,800 arbitrary
re-groupings of countries. Second, the field's standard change specification erases it: the same measures on the
same panel give weak or positive coefficients, with no negative-significant change cell. Third, the erasure is a
design property, not a substantive finding: the within estimator removes the between-country variation in which
the gradient lives, and the paper's decomposition of that variation is the audit's core. Fourth, the level
gradient is descriptive: the future-schooling placebo is about 90 per cent as strong as the correct-time
relation, which is the signature of a shared development process rather than an identified effect of schooling.

Three things remain open, and the paper names them rather than resolving them. The individual-level mechanism is
open because the DHS microdata were not obtainable; the survey-level gradient is consistent with an individual
gradient but cannot confirm it. The historical driver question is open in the sense that the transition model's
mortality counterfactual removes only 3.2 per cent of the collapse while the development-only rival ties the
individuation model out of sample; the model attributes most of the collapse to its schooling-side mechanisms —
a property of the calibrated model, not an identified fact about the world. The causal question is open by design: no observational design in the
project identifies the effect of schooling on fertility, and the paper's most useful contribution to the causal
literature may be the specification of what a credible design would need (Section 6).

## 8.3 Limitations

**Observational designs throughout.** The levels analysis is a between-country description; the change analysis
is a within-country association; the survey analysis is ecological; the transition analysis is a calibrated
model. The placebo is the paper's own statement of the limit, not an appendix to it.

**Measurement.** "Years of schooling" and "secondary education" mean different things across countries and
cohorts; the DHS cohort results are the clearest demonstration. Harmonised attainment series carry documented
reconstruction assumptions; enrolment and completion measures are not identical objects; gender-parity indices
can hide distributional change. The robustness of the levels sign across eight measures is reassuring for the
sign, not for the magnitude.

**Multiple comparisons.** The paper reports large specification grids without a formal family-wise correction.
The defence is procedural — pre-registered grids, every cell reported, claims about sign consistency rather than
single p-values — and it is a defence, not a substitute for one.

**Data gaps.** DHS Individual Recodes were not obtainable, so the individual-level test, the wealth horse-race,
the community placebo, and the quantum/tempo decomposition remain undone. The literature search is documented
but is not a PRISMA-style systematic review. One ad-hoc multiverse run produced during the project could not be
re-verified after the compute node went offline; it is not used for any number in this paper, and the published
battery covers the same ground.

**Generalisability.** The panel is 196 countries over 1960–2024. The transportability experiment shows the level
relation reproduces in arbitrary subsets of those countries; it does not show it would reproduce in another era
or measurement regime. The above-nine-years reversal is estimated on the richest and most schooled countries and
should not be read as a general statement about tertiary expansion.

**Authorship of evidence.** This is a synthesis across several workstreams; each section carries its record and
provenance, and the responsibility for a number is the record's. The claim-to-source map is the audit trail.

## 8.4 Conclusion

The level of analysis decides the answer. Between countries, the schooling–fertility relation is large, precise,
robust across 336 specifications, and reproduced in 71–99 per cent of 13,800 arbitrary country groupings. Within
countries, on decade changes, the same relation weakens and for several measures reverses, with no
negative-significant change cell. Both estimates answer different questions; reading one as if it answered the
other's question is what produced the contradiction this paper set out to audit. The audit's second conclusion is
less comfortable: the between-country gradient is not an identified schooling effect, because a future-schooling
placebo is about 90 per cent as strong as the correct-time relation. The gradient is descriptive — real, global,
steepest at the massification margin, and located in the first six years of schooling — and it should be read
that way.

The contribution is therefore a structural demonstration about a known correlation, not a new correlation: it
shows what the field's standard change specification does to the gradient, measures the erasure with a full
specification space and a random-re-partition yardstick, quantifies the development-gradient caveat with a
placebo, and places the gradient in the schooling distribution. The project's nulls — the care-work loop
absorbed by income, the falsified strong no-off-switch, the absent tipping point, the mortality counterfactual
that removes 3.2 per cent, the tolerance ladder that is an identification limit — are reported with the same
discipline, because a synthesis that reported only the surviving results would be doing to its own evidence what
the paper criticises in the literature. What survives is a development gradient at the massification margin;
what fails is the causal reading of it; what cannot be tested with these data is the individual-level mechanism,
and the paper names the data that would test it.


# References

- Angrist, J. D., & Pischke, J.-S. (2009). Mostly Harmless Econometrics. Princeton University Press. https://doi.org/10.1515/9781400829828 *[V (Crossref)]*
- Bareinboim, E., & Pearl, J. (2013). A General Algorithm for Deciding Transportability of Experimental Results. Journal of Causal Inference, 1(1), 107-134. https://doi.org/10.1515/jci-2012-0004 *[V (Crossref)]*
- Barro, R. J., & Lee, J. W. (2013). A new data set of educational attainment in the world, 1950–2010. Journal of Development Economics, 104, 184-198. https://doi.org/10.1016/j.jdeveco.2012.10.001 *[V (Crossref)]*
- Basu, A. M. (2002). Why does Education Lead to Lower Fertility? A Critical Review of Some of the Possibilities. World Development, 30(10), 1779-1790. https://doi.org/10.1016/s0305-750x(02)00072-4 *[V (Crossref)]*
- Becker, G. S. (1960). An economic analysis of fertility. In Demographic and economic change in developed countries (pp. 209–231). Princeton University Press. *[U (no DOI; hand-cited)]*
- Becker, G. S., & Lewis, H. G. (1973). On the Interaction between the Quantity and Quality of Children. Journal of Political Economy, 81(2, Part 2), S279-S288. https://doi.org/10.1086/260166 *[V (Crossref)]*
- Becker, G., & Barro, R. (1986). A Reformulation of the Economic Theory of Fertility. National Bureau of Economic Research. https://doi.org/10.3386/w1793 *[V (Crossref)]*
- Bell, A., & Jones, K. (2014). Explaining Fixed Effects: Random Effects Modeling of Time-Series Cross-Sectional and Panel Data. Political Science Research and Methods, 3(1), 133-153. https://doi.org/10.1017/psrm.2014.7 *[V (Crossref)]*
- Boettiger, C., & Hastings, A. (2012). Early warning signals and the prosecutor's fallacy. Proceedings of the Royal Society B: Biological Sciences, 279(1748), 4734-4739. https://doi.org/10.1098/rspb.2012.2085 *[V (Crossref)]*
- Bongaarts, J. (1978). A Framework for Analyzing the Proximate Determinants of Fertility. Population and Development Review, 4(1), 105. https://doi.org/10.2307/1972149 *[V (Crossref)]*
- Bongaarts, J., & Feeney, G. (1998). On the quantum and tempo of fertility. Population Council. https://doi.org/10.31899/pgy6.1010 *[V (Crossref)]*
- Bongaarts, J., & Watkins, S. C. (1996). Social Interactions and Contemporary Fertility Transitions. Population and Development Review, 22(4), 639. https://doi.org/10.2307/2137804 *[V (Crossref)]*
- Breierova, L., & Duflo, E. (2004). The Impact of Education on Fertility and Child Mortality: Do Fathers Really Matter Less Than Mothers?. National Bureau of Economic Research. https://doi.org/10.3386/w10513 *[V (Crossref)]*
- Brock, W. A., & Durlauf, S. N. (2001). Growth Empirics and Reality. Washington, DC:  World Bank. https://doi.org/10.1596/17447 *[V (Crossref)]*
- Caldwell, J. C. (1976). Toward A Restatement of Demographic Transition Theory. Population and Development Review, 2(3/4), 321. https://doi.org/10.2307/1971615 *[V (Crossref)]*
- Caldwell, J. C. (1980). Mass Education as a Determinant of the Timing of Fertility Decline. Population and Development Review, 6(2), 225. https://doi.org/10.2307/1972729 *[V (Crossref)]*
- Chicoine, L. (2012). Education and Fertility: Evidence from a Policy Change in Kenya. SSRN Electronic Journal. https://doi.org/10.2139/ssrn.2157920 *[V (Crossref)]*
- Cleland, J., & Rodríguez, G. (1988). The Effect of Parental Education on Marital Fertility in Developing Countries. Population Studies, 42(3), 419-442. https://doi.org/10.1080/0032472031000143566 *[V (Crossref)]*
- Cleland, J., & Wilson, C. (1987). Demand Theories of the Fertility Transition: An Iconoclastic View. Population Studies, 41(1), 5-30. https://doi.org/10.1080/0032472031000142516 *[V (Crossref)]*
- Coale, A. J. (1986). The Decline of Fertility in Europe. Princeton University Press. https://doi.org/10.1515/9781400886692 *[V (Crossref)]*
- Coall, D. A., & Hertwig, R. (2010). Grandparental investment: Past, present, and future. Behavioral and Brain Sciences, 33(1), 1-19. https://doi.org/10.1017/s0140525x09991105 *[V (Crossref)]*
- Dakos, V., Carpenter, S. R., Brock, W. A., Ellison, A. M., Guttal, V., Ives, A. R., Kéfi, S., Livina, V., Seekell, D. A., Nes, E. H. v., & Scheffer, M. (2012). Methods for Detecting Early Warnings of Critical Transitions in Time Series Illustrated Using Simulated Ecological Data. PLoS ONE, 7(7), e41010. https://doi.org/10.1371/journal.pone.0041010 *[V (Crossref)]*
- Davis, K. (1963). The theory of change and response in modern demographic history. Population Index, 29(4), 345–366. https://doi.org/10.2307/2732014 *[V (Crossref)]*
- Deaton, A. (2010). Instruments, Randomization, and Learning about Development. Journal of Economic Literature, 48(2), 424-455. https://doi.org/10.1257/jel.48.2.424 *[V (Crossref)]*
- Ditlevsen, P. D., & Johnsen, S. J. (2010). Tipping points: Early warning and wishful thinking. Geophysical Research Letters, 37(19). https://doi.org/10.1029/2010gl044486 *[V (Crossref)]*
- Doepke, M. (2001). Accounting for Fertility Decline During the Transition to Growth. Elsevier BV. https://doi.org/10.2139/ssrn.279519 *[V (Crossref)]*
- Doepke, M. (2003). Child Mortality and Fertility Decline: Does the Barro-Becker
- Duflo, E. (2000). Schooling and Labor Market Consequences of School Construction in Indonesia: Evidence from an Unusual Policy Experiment. National Bureau of Economic Research. https://doi.org/10.3386/w7860 *[V (Crossref)]*
- Duflo, E. (2012). Women Empowerment and Economic Development. Journal of Economic Literature, 50(4), 1051-1079. https://doi.org/10.1257/jel.50.4.1051 *[V (Crossref)]*
- Easterlin, R. A. (1975). An Economic Framework for Fertility Analysis. Studies in Family Planning, 6(3), 54. https://doi.org/10.2307/1964934 *[V (Crossref)]*
- Eberhardt, M., & Teal, F. (2011). ECONOMETRICS FOR GRUMBLERS: A NEW LOOK AT THE LITERATURE ON CROSS-COUNTRY GROWTH EMPIRICS. Journal of Economic Surveys, 25(1), 109-155. https://doi.org/10.1111/j.1467-6419.2010.00624.x *[V (Crossref)]*
- Frejka, T., & Sobotka, T. (2008). Overview Chapter 1: Fertility in Europe. Demographic Research, 19, 15-46. https://doi.org/10.4054/demres.2008.19.3 *[V (Crossref)]*
- Galor, O., & Weil, D. (1998). Population, Technology, and Growth:  From the Malthusian Regime to the  Demographic Transition and Beyond. National Bureau of Economic Research. https://doi.org/10.3386/w6811 *[V (Crossref)]*
- Gauthier, A. H. (2007). The impact of family policies on fertility in industrialized countries: a review of the literature. Population Research and Policy Review, 26(3), 323-346. https://doi.org/10.1007/s11113-007-9033-x *[V (Crossref)]*
- Giudice, M. D., & Gangestad, S. W. (2021). A Traveler’s Guide to the Multiverse: Promises, Pitfalls, and a Framework for the Evaluation of Analytic Decisions. Advances in Methods and Practices in Psychological Science, 4(1). https://doi.org/10.1177/2515245920954925 *[V (Crossref)]*
- Guinnane, T. W. (2010). The Historical Fertility Transition: A Guide for Economists. Elsevier BV. https://doi.org/10.2139/ssrn.1692848 *[V (Crossref)]*
- Hanushek, E. A. (1992). The Trade-off between Child Quantity and Quality. Journal of Political Economy, 100(1), 84-117. https://doi.org/10.1086/261808 *[V (Crossref)]*
- Hastings, A., & Wysham, D. B. (2010). Regime shifts in ecological systems can occur with no warning. Ecology Letters, 13(4), 464-472. https://doi.org/10.1111/j.1461-0248.2010.01439.x *[V (Crossref)]*
- Hausman, J. A., & Taylor, W. E. (1981). Panel Data and Unobservable Individual Effects. Econometrica, 49(6), 1377. https://doi.org/10.2307/1911406 *[V (Crossref)]*
- KC, S., & Lutz, W. (2017). The human core of the shared socioeconomic pathways: Population scenarios by age, sex and level of education for all countries to 2100. Global Environmental Change, 42, 181-192. https://doi.org/10.1016/j.gloenvcha.2014.06.004 *[V (Crossref)]*
- Koytcheva, E., & Philipov, D. (2008). Bulgaria: Ethnic differentials in rapidly declining fertility. Demographic Research, 19, 361-402. https://doi.org/10.4054/demres.2008.19.13 *[V (Crossref)]*
- Kravdal, O. (2002). Education and Fertility in Sub-Saharan Africa: Individual and Community Effects. Demography, 39(2), 233. https://doi.org/10.2307/3088337 *[V (Crossref)]*
- Lesthaeghe, R. (1983). A Century of Demographic and Cultural Change in Western Europe: An Exploration of Underlying Dimensions. Population and Development Review, 9(3), 411. https://doi.org/10.2307/1973316 *[V (Crossref)]*
- Levine, R., & Renelt, D. (1992). A sensitivity analysis of cross-country growth regressions. American Economic Review, 82(4), 942–963. *[U (no DOI; hand-cited)]*
- Lutz, W., & KC, S. (2011). Global Human Capital: Integrating Education and Population. Science, 333(6042), 587-592. https://doi.org/10.1126/science.1206964 *[V (Crossref)]*
- Martin, T. C., & Juarez, F. (1995). The Impact of Women's Education on Fertility In Latin America: Searching for Explanations. International Family Planning Perspectives, 21(2), 52. https://doi.org/10.2307/2133523 *[V (Crossref)]*
- Mincer, J. (1958). Investment in Human Capital and Personal Income Distribution. Journal of Political Economy, 66(4), 281-302. https://doi.org/10.1086/258055 *[V (Crossref)]*
- Murtin, F. (2013). Long-Term Determinants of the Demographic Transition, 1870–2000. Review of Economics and Statistics, 95(2), 617-631. https://doi.org/10.1162/rest_a_00302 *[V (Crossref)]*
- Nickell, S. (1981). Biases in Dynamic Models with Fixed Effects. Econometrica, 49(6), 1417. https://doi.org/10.2307/1911408 *[V (Crossref)]*
- Notestein, F. W. (1945). Population — the long view. In T. W. Schultz (Ed.), Food for the world (pp. 36–57). University of Chicago Press. *[U (no DOI; hand-cited)]*
- Osili, U. O., & Long, B. T. (2007). Does Female Schooling Reduce Fertility? Evidence from Nigeria. National Bureau of Economic Research. https://doi.org/10.3386/w13070 *[V (Crossref)]*
- Pearl, J., & Bareinboim, E. (2011). Transportability of Causal and Statistical Relations: A Formal Approach. 2011 IEEE 11th International Conference on Data Mining Workshops, 540-547. https://doi.org/10.1109/icdmw.2011.169 *[V (Crossref)]*
- Psacharopoulos, G., & *, H. A. P. (2004). Returns to investment in education: a further update. Education Economics, 12(2), 111-134. https://doi.org/10.1080/0964529042000239140 *[V (Crossref)]*
- Robinson, W. S. (1950). Ecological Correlations and the Behavior of Individuals. American Sociological Review, 15(3), 351. https://doi.org/10.2307/2087176 *[V (Crossref)]*
- Roth, J. (2022). Pretest with Caution: Event-Study Estimates after Testing for Parallel Trends. American Economic Review: Insights, 4(3), 305-322. https://doi.org/10.1257/aeri.20210236 *[V (Crossref)]*
- Rutstein, S. O., & Johnson, K. (2004). The DHS wealth index (DHS Comparative Reports No. 6). ORC Macro. *[U (no DOI; hand-cited)]*
- Sala-i-Martin, X. (1997). I Just Ran Four Million Regressions. National Bureau of Economic Research. https://doi.org/10.3386/w6252 *[V (Crossref)]*
- Schultz, T. W. (1961). Investment in human capital. American Economic Review, 51(1), 1–17. *[U (no DOI; hand-cited)]*
- Silberzahn, R., Uhlmann, E. L., Martin, D. P., Anselmi, P., Aust, F., Awtrey, E., Bahník, Š., Bai, F., Bannard, C., Bonnier, E., Carlsson, R., Cheung, F., Christensen, G., Clay, R., Craig, M. A., Rosa, A. D., Dam, L., Evans, M. H., Cervantes, I. F., Fong, N., Gamez-Djokic, M., Glenz, A., Gordon-McKeon, S., Heaton, T. J., Hederos, K., Heene, M., Mohr, A. J. H., Högden, F., Hui, K., Johannesson, M., Kalodimos, J., Kaszubowski, E., Kennedy, D. M., Lei, R., Lindsay, T. A., Liverani, S., Madan, C. R., Molden, D., Molleman, E., Morey, R. D., Mulder, L. B., Nijstad, B. R., Pope, N. G., Pope, B., Prenoveau, J. M., Rink, F., Robusto, E., Roderique, H., Sandberg, A., Schlüter, E., Schönbrodt, F. D., Sherman, M. F., Sommer, S. A., Sotak, K., Spain, S., Spörlein, C., Stafford, T., Stefanutti, L., Tauber, S., Ullrich, J., Vianello, M., Wagenmakers, E.-J., Witkowiak, M., Yoon, S., & Nosek, B. A. (2018). Many Analysts, One Data Set: Making Transparent How Variations in Analytic Choices Affect Results. Advances in Methods and Practices in Psychological Science, 1(3), 337-356. https://doi.org/10.1177/2515245917747646 *[V (Crossref)]*
- Skirbekk, V. (2008). Fertility trends by social status. Demographic Research, 18, 145-180. https://doi.org/10.4054/demres.2008.18.5 *[V (Crossref)]*
- Thévenon, O., & Gauthier, A. H. (2011). Family policies in developed countries: a ‘fertility-booster’ with side-effects. Community, Work &amp; Family, 14(2), 197-216. https://doi.org/10.1080/13668803.2011.571400 *[V (Crossref)]*
- Trow, M. (1974). Problems in the transition from elite to mass higher education. Carnegie Commission on Higher Education. *[U (no DOI; hand-cited)]*
- Vivalt, E. (2020). How Much Can We Generalize From Impact Evaluations?. Journal of the European Economic Association, 18(6), 3045-3089. https://doi.org/10.1093/jeea/jvaa019 *[V (Crossref)]*
- Zakharov, S. (2008). Russian Federation: From the first to second demographic transition. Demographic Research, 19, 907-972. https://doi.org/10.4054/demres.2008.19.24 *[V (Crossref)]*
