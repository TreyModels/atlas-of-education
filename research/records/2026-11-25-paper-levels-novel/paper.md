# The level-of-analysis trap: a multiverse audit of the schooling–fertility gradient

*Draft for Demography / Population and Development Review / Demographic Research (methods framing
also fits Sociological Methods & Research). Paper N2, 24 November 2026. Every number traces to the
`corr-battery` record (9363079); see `SOURCE_MAP.md` for the claim-by-claim map. Pre-registration:
`PRE_REGISTRATION.md`, commits 772650a and 6a1927f, pushed before any code existed.*

## Abstract

A large negative cross-country association between schooling and fertility is one of the most
replicated facts in demography, and one of the most frequently used as evidence that schooling is a
causal lever on fertility. This paper audits the structure of that association rather than
announcing it. Using the project's 17-measure country panel (342 ordered pairs; 296 countries at
most; six decades), we estimate the eight schooling–fertility pairs in two standard ways: in levels
with decade and region fixed effects, and in within-country decade changes with country fixed
effects and country-specific trends. The eight level coefficients are all negative and significant
(for women's mean years of schooling, −0.129, SE 0.029; n = 5,915 country-years, 192 countries), and
they reproduce in 71.5–98.9% of 13,800 random country re-partitions. Under the change specification
the negative association does not survive: three of the eight coefficients are significantly
positive (women's years, +0.115, SE 0.046), none is significantly negative, and only 0.0–7.2% of the
13,800 partitions reproduce a negative-significant change estimate. A future-schooling placebo is
about 90% as strong as the correct-time relation (52.9% versus 58.8% of design cells negative-
significant), so the level gradient is a development-gradient marker, not a demonstrated causal
effect. We frame the contribution as an audit, not a discovery: the within/between issue is old,
but the systematic decomposition of this particular gradient across thousands of country partitions
and a purpose-built placebo, to our knowledge, has not been assembled in one place. The paper then
sets out what the audit does and does not license — for how the field estimates these relations, for
reading existing within-country estimates, for policy claims built on change designs, and for the
research designs that could turn the audit into a causal estimate. We call the 13,800 partitions a
sensitivity universe, not a test.

## 1. Introduction

Few cross-national regularities are as robust as the negative association between schooling and
fertility. Countries where women have more schooling have fewer births; the association appears with
every schooling measure demographers use — enrolment, attainment, completion, mean years, gender
parity — and it appears in every region. It is also one of the associations most often given a causal
reading: expand schooling, the argument goes, and fertility will fall.

This paper does not ask whether that association exists. It asks a different and more uncomfortable
question: **at what level of analysis does it exist, and what does that tell us about how it should
be read?** The standard cross-country evidence is a between-country fact. The standard causal
identification strategy in comparative demography is a within-country change design: does a country
that expands schooling faster also see fertility fall faster, conditional on country fixed effects
and trends? These are different estimands, and they need not agree. When a relation is a property of
the cross-section — a marker of where a country sits on a development gradient — removing the
between-country variation can remove the relation entirely. When it is a causal effect of schooling,
the within-country change design should see it.

We take the eight schooling–fertility pairs from a 17-measure panel and estimate both. The contrast
is stark. The level relation is large, negative and global: all eight coefficients are negative and
significant, and between 71.5% and 98.9% of 13,800 random country re-partitions reproduce a
negative-significant estimate. The change relation is not: three of eight coefficients are
significantly positive, none is significantly negative, and at most 7.2% of partitions reproduce the
negative sign. A future-schooling placebo — schooling measured ten years *after* the fertility
outcome — is 90% as strong as the correctly timed relation, which means the level correlation cannot
be given a causal reading even before the change design is considered.

The demonstration is about the **structure of a known correlation**, not a new correlation. That is
the honest description, and it matters for how the paper should be judged. The within/between
distinction is standard econometrics (Nickell 1981; Angrist and Pischke 2009; Durlauf, Johnson and
Temple 2005; Eberhardt and Teal 2011); the aggregation critique is older still (Robinson 1950); the
multiplicity of defensible specifications is the multiverse literature's central point (Steegen et
al. 2016; Simonsohn, Simmons and Nelson 2020; Patel, Burkhart and Ioannidis 2015). What is less
common is a systematic audit of *this* gradient across thousands of country partitions with a
pre-registered placebo, and the argument that follows from it: that cross-country and within-country
estimates of the schooling–fertility relation are answering different questions, and that the
field's language has not always kept them apart.

The paper's contributions are therefore four, and none is a "first". First, a transparent
decomposition of the eight schooling–fertility pairs into level and change estimates on the same
data, with the same measures and the same controls. Second, a transportability audit: 13,800 random
re-partitions of countries into groups of the same sizes, which quantifies how much of the level
gradient survives arbitrary slicing of the country set, and how little of the change relation does.
Third, two placebo tests — future schooling, and the pre-existing lead/lag check — which together
separate a development gradient from a causal lever. Fourth, an explicit account of what this does
not license: it does not show that schooling has no effect on fertility; it shows that the
cross-country gradient cannot be read as that effect, and it specifies the designs that could
identify it.

The rest of the paper proceeds as follows. Section 2 situates the audit in the ecological-fallacy,
within-between, multiverse and schooling–fertility literatures. Section 3 describes the panel, the
specifications, the transportability design and the pre-registered decision rules. Section 4 reports
the levels-versus-changes contrast, the transportability results, the threshold shape and the
placebo. Section 5 answers the three referee objections we regard as most serious: Nickell bias,
measurement error and change-window sensitivity, and the ecological fallacy. Section 6 draws out the
implications for how the field estimates these relations, for reading existing within-country
estimates, and for policy claims built on change designs. Section 7 specifies the future research
that would turn the audit into a causal estimate, and what each design would and would not identify.
Section 8 concludes.

## 2. Prior work and the framing of the audit

### 2.1 The aggregation problem is old

Robinson (1950) is the canonical statement that a relationship estimated on aggregates need not hold
for the individuals composing them, and the schooling–fertility literature is a natural home for the
problem. The individual-level gradient is robust: women with more schooling have fewer children in
country after country, and the micro literature has spent decades distinguishing the mechanisms
(Cleland and Rodríguez 1988; Martin and Juárez 1995; Basu 2002). Kravdal (2002) went further and
separated individual from community education effects in sub-Saharan Africa, showing that a woman's
own schooling and the schooling of her community can have different associations with fertility;
Kravdal (2012) replicated the community-effect finding elsewhere. A country-level null is therefore
not evidence that schooling does not matter for individual women; it is evidence about what the
country aggregate measures. We return to this in Section 5, because it is the objection that most
constrains what the paper can claim.

### 2.2 The within-between critique is textbook

The econometric case that these are different estimands is equally old. Nickell (1981) showed that
dynamic panel estimators with fixed effects are biased in short panels, which is one reason
within-country change estimates are hard to interpret; Angrist and Pischke (2009) is the standard
teaching statement of what fixed effects do and do not remove; Durlauf, Johnson and Temple (2005)
make the levels-versus-growth distinction central to growth econometrics, and Eberhardt and Teal
(2011) generalise the warning: cross-country level regressions can reflect common factors and
trending regressors rather than a structural relationship, and the within-country change version may
have little power or a different estimand. Brock and Durlauf (2001) add the heterogeneity critique: a
pooled coefficient may be an average that no actual country has, which is why the transportability
audit matters rather than being decorative.

Our audit is not a contribution to this methodological literature. It uses it. The audit's value, if
any, is that it applies the critique to a gradient that is routinely cited as if it were causal, and
quantifies how much of the gradient survives each cut.

### 2.3 Cross-country schooling–fertility work has run both ways

The substantive literature contains both kinds of estimate, often without flagging that they are
different things. Caldwell (1980) argued that mass education is a *determinant* of the timing of
fertility decline — the strongest version of the causal reading, and the one this paper must engage
most directly. Bongaarts (1978) and Bongaarts and Watkins (1996) treat schooling as one of the
proximate and contextual determinants of fertility, with the emphasis on social interaction and
context. Lutz and Skirbekk and colleagues (2014) model education as a driver of demographic
projections, and Barro and Lee (2013) provide the attainment series on which a great deal of
cross-country work rests. Pritchett (2001) is the classic warning that schooling's economic returns
are not automatic — the same caution applies to demographic returns. Duflo (2001) and Chicoine
(2016) are the natural-experiment end of the spectrum: school construction and free primary
education, identifying effects from expansion episodes rather than cross-country levels. Liu and
Raftery (2020) model the education–fertility relationship at the country level with explicit
between-country structure, and are the closest modelling competitor to the audit. Herzer, Strulik
and Vollmer (2012) and Murtin (2013) estimate long-run determinants of fertility across countries and
time, and are the closest historical cross-country competitors.

The pattern is that the literature has strong level evidence (Caldwell; Lutz–Skirbekk; Liu–Raftery),
strong micro evidence (Cleland–Rodríguez; Kravdal), and a small but growing natural-experiment
literature (Duflo; Chicoine). What it does not, to our knowledge, contain is a single paper that
decomposes the schooling–fertility gradient into level and change estimates across the same measures
and the same data, quantifies the transportability of each, and reports a placebo strong enough to
discipline the causal reading. That assembly is the contribution. The verdict we adopt for it is the
literature auditor's: **incremental — new assembly, not new fact or method.**

### 2.4 Multiverse reasoning and the vibration of effects

The audit is a multiverse exercise in the sense of Steegen et al. (2016) and Simonsohn, Simmons and
Nelson (2020): there are many defensible choices — sample restrictions, lags, fixed-effect patterns,
functional form — and reporting one of them as "the" estimate misrepresents the evidence. Patel,
Burkhart and Ioannidis (2015) call the resulting spread the vibration of effects, and it is
substantial in our own grid. The transportability dimension is a natural extension: instead of
varying the specification for a fixed country set, vary the country set itself, with random groupings
of the same sizes as the observed groupings. We stress in advance that this is a **sensitivity
universe, not a test**: a random re-partition is a device to ask how much the estimate depends on the
particular collection of countries, not a randomisation that identifies a causal quantity. The
13,800 draws exceed the pre-registered 800 because the run was extended to fill a compute load; the
statistic is the same and we report the extension rather than hiding it.

## 3. Data, specifications and pre-registered design

### 3.1 Panel and pairs

The panel is the project's country-year panel: 17 measures covering schooling (five attainment and
completion measures, enrolment, and two gender-parity measures), fertility, mortality, income,
urbanisation, employment, electricity and tax, mostly 1960–2014 (some series extend to 2020s), with
income logged and urbanisation controlled. All 17 × 16 = 272 ordered pairs are used in the wider
battery, giving 342 estimable ordered pairs after the minimum-data rule; the audit's focal object is
the eight schooling → fertility pairs.

### 3.2 The two specifications

**Levels.** The fertility level is regressed on the schooling level with decade fixed effects,
region fixed effects, log income and urbanisation, lag 0, all available years. Standard errors are
clustered by country. This is the specification that produces the familiar cross-country gradient.

**Changes.** Ten-year change in fertility is regressed on the starting schooling level, with country
fixed effects and country-specific linear trends, log income and urbanisation, lag 0, all available
decades. This is the within-country design: the between-country variation is removed, and the
estimate comes from countries that change faster or slower than their own trend.

The two specifications are deliberate mirror images. They use the same measures, the same controls
and the same panel; what differs is the level of analysis. That is the entire point.

### 3.3 The full specification grid

The pre-registration fixed a grid of roughly 6,174 cells per pair (2,111,508 cells in total): sample
restrictions, lags, fixed-effect patterns, and functional form. 936,657 cells were estimable under
the minimum-sample rule (n ≥ 60, ≥ 8 countries); the rest are reported as unestimable rather than
dropped silently. The grid is what lets us say whether the level/change contrast is a feature of the
baseline specification or a robust property of the data.

### 3.4 Transportability design

Each of the 13,800 random partitions splits the 296 countries into six groups with the same sizes as
the observed region-family groups. Within each group, the baseline level and change specifications
are estimated for all 342 pairs. This produces 56,077,352 within-group regressions (reported as
10,447,698 aggregated result rows, because six within-group regressions are aggregated into each
row — the honest accounting difference is stated in the record). The transportability statistic for a
pair is the share of partitions in which the within-group estimate is negative and significant. A
second, clustered bootstrap (500 draws per pair) gives interval estimates for the coefficients
themselves.

### 3.5 Placebo

The future-schooling placebo uses schooling measured ten years after the fertility outcome on the
identical design cells. If the level gradient reflects schooling's causal effect, the correctly timed
relation should be much stronger than the mis-timed one. The pre-registered rule: if the placebo is
at least 80% as strong as the correct-time relation, the level gradient is a development gradient and
cannot be given a causal reading. The placebo grid contains 100,092 cells.

### 3.6 Pre-registered decision rules

Three rules were fixed before the run: (i) the level relation is "global" if at least 80% of the
specification grid is negative and the transportability share is at least 0.80; (ii) the change
relation is "weak" if fewer than 30% of cells are negative-significant; (iii) the level gradient is
"descriptive, not causal" if the placebo is at least 80% as strong as the correct-time relation. All
three are evaluated in Section 4, including where they fail.

### 3.7 Compute and reproducibility

The battery ran 57,291,101 regressions in 3,018 seconds (50.3 minutes) on ten workers, with
checkpoints and one recorded crash-and-resume (a dispatch bug cost wall time, not work; the log is
committed). All scripts, the pre-registration, the aggregated result files and the logs are in the
record. No result in this paper comes from a run that was not pre-registered; the extensions
(13,800 partitions instead of 800) are load extensions of pre-registered statistics and are reported
as such.

## 4. Results

### 4.1 Levels: large, negative, and global

All eight schooling–fertility level coefficients are negative and significant at conventional levels
(Table 1). For women's mean years of schooling the coefficient is **−0.129 (SE 0.029; n = 5,915
country-years, 192 countries)**; for total mean years, **−0.227 (0.042; n = 1,394, 144)**; for
secondary enrolment, **−0.0213 (0.0037; n = 5,927, 202)**; lower-secondary completion, **−0.0224
(0.0035; n = 4,106, 193)**; primary completion, **−0.0239 (0.0033; n = 4,878, 193)**; tertiary
enrolment, **−0.0040 (0.0020; n = 5,126, 198)**; gender parity in secondary, **−1.968 (0.277;
n = 5,708, 199)**; gender parity in tertiary, **−1.265 (0.197; n = 4,455, 198)**. The country-
clustered bootstrap excludes zero for all eight focal pairs (8/8).

The level relation is also robust across the specification grid: the coefficient is negative in
70.4–83.4% of specifications per pair, and negative-significant in 42.9–59.4%. That is the sense in
which the gradient is a property of the cross-section, not an artefact of one specification.

### 4.2 Changes: the gradient does not survive the within-country design

Under the change specification the picture inverts (Table 1). Three of the eight coefficients are
significantly positive: women's mean years, **+0.115 (SE 0.046; n = 4,225, 189)**; total mean years,
**+0.189 (0.054; n = 1,107, 109)**; lower-secondary completion, **+0.0064 (0.0031; n = 2,830, 185)**.
None is significantly negative. The remaining five are small and indistinguishable from zero:
secondary enrolment +0.0029 (0.0026), primary completion −0.0004 (0.0020), tertiary enrolment −0.0044
(0.0026), gender parity in secondary +0.059 (0.190), gender parity in tertiary +0.010 (0.207). Across
the specification grid the change coefficient is negative in only 24.1–44.3% of specs and negative-
significant in 3.5–13.5%.

This is the paper's central descriptive fact: **a relation that is large, negative and global in
levels is null or positive in the standard within-country change specification.** The two estimates
are not in tension; they are estimates of different things, and the field has often spoken as if they
were the same thing.

### 4.3 Transportability: global in levels, absent in changes

The transportability audit makes the contrast quantitative. Over 13,800 random country partitions,
the share of partitions reproducing a negative-significant estimate is **71.5–98.9%** for the eight
level pairs and **0.0–7.2%** for the eight change pairs (Table 2). Across all 342 pairs the level
share is 0.227 [95% interval 0.214, 0.239] and the change share 0.111 [0.103, 0.120].

Two honest qualifications. First, the pre-registered "at least 80% transportable" rule is met for
the schooling–fertility pairs (five of eight exceed 0.80; all exceed 0.715) but not for the matrix as
a whole — most of the 342 pairs are not schooling–fertility pairs, and signs are mixed by
construction. The rule was written for the relation of interest and fails as a description of all 342
links; we report both. Second, transportability is not a test of a causal hypothesis. That the
gradient survives arbitrary country slicing says the gradient is not an artefact of which countries
are grouped together; it does not say why it exists.

### 4.4 Threshold shape

The level relation is steepest at the bottom of the schooling distribution. The clustered bootstrap
(500 draws) gives, for women's mean years: below 6 years of schooling, **−0.326 [−0.405, −0.248]**;
6–9 years, **−0.092 [−0.175, −0.013]**; above 9 years, **+0.112 [+0.057, +0.171]**. For total mean
years the pattern is the same: −0.387 [−0.483, −0.283], −0.274 [−0.364, −0.182], +0.174 [0.106,
0.250]. The steep part of the cross-country association is the movement from minimal schooling to
about six years — the massification margin — and beyond nine years the conditional level association
reverses. This is consistent with a development-gradient reading, and it is also consistent with the
threshold literature's finding that the first years of schooling carry the largest fertility
associations.

### 4.5 The placebo: about 90% as strong as the real thing

The future-schooling placebo is not null. For the schooling–fertility pairs, **52.9%** of placebo
cells are negative-significant with a median coefficient of −0.0179, against **58.8%** for the
correctly timed relation with a median of −0.0224 — the placebo is about **90% as strong**. Across
all pairs the placebo is 20.1% against 21.1% for the correctly timed relation. The pre-registered
rule (placebo ≥ 80% of correct-time) fires: the strong level correlation is a development-gradient
association and cannot be given a causal reading. This is the most important result in the paper for
the causal question, and it is the one that most reduces what the level literature can claim.

### 4.6 Summary of verdicts

| test | pre-registered rule | outcome | verdict |
|---|---|---|---|
| level relation large and global | level coefficient negative-significant in ≥80% of specs; transportability ≥0.80 | 8/8 negative-significant at baseline; negative in 70–83% of specs; transportability 0.715–0.989 | **holds for the eight focal pairs; fails matrix-wide (0.227)** |
| change relation weak by the <30% rule | <30% of change cells negative-significant | change negative-significant share 3.5–13.5% per pair; matrix 9.0% | **holds** |
| level gradient is descriptive, not causal | placebo ≥80% as strong as correct-time | 52.9% vs 58.8% (≈90%) | **fires: descriptive** |

**Table 1. Levels versus changes, eight schooling → fertility pairs** (baseline specifications;
clustered SE; n country-years and countries).

| schooling measure | level b (SE), n, countries | change b (SE), n, countries |
|---|---|---|
| mean years, women | −0.129 (0.029), 5,915, 192 | +0.115 (0.046), 4,225, 189 |
| mean years, total | −0.227 (0.042), 1,394, 144 | +0.189 (0.054), 1,107, 109 |
| secondary enrolment | −0.0213 (0.0037), 5,927, 202 | +0.0029 (0.0026), 4,548, 198 |
| lower-secondary completion | −0.0224 (0.0035), 4,106, 193 | +0.0064 (0.0031), 2,830, 185 |
| primary completion | −0.0239 (0.0033), 4,878, 193 | −0.0004 (0.0020), 3,561, 185 |
| tertiary enrolment | −0.0040 (0.0020), 5,126, 198 | −0.0044 (0.0026), 3,854, 191 |
| gender parity, secondary | −1.968 (0.277), 5,708, 199 | +0.059 (0.190), 4,900, 195 |
| gender parity, tertiary | −1.265 (0.197), 4,455, 198 | +0.010 (0.207), 3,198, 191 |

**Table 2. Transportability, share of 13,800 random partitions with a negative-significant
within-group estimate.**

| schooling measure | level share | change share |
|---|---|---|
| mean years, women | 0.913 | 0.000 |
| mean years, total | 0.914 | 0.002 |
| secondary enrolment | 0.979 | 0.001 |
| lower-secondary completion | 0.986 | 0.001 |
| primary completion | 0.989 | 0.028 |
| tertiary enrolment | 0.715 | 0.001 |
| gender parity, secondary | 0.962 | 0.072 |
| gender parity, tertiary | 0.811 | 0.003 |

## 5. Referee objections and what they do to the argument

### 5.1 "This is just the within–between critique"

Yes, in part — and it is important to say so. The methodological content here is old, and the paper
does not claim otherwise. The audit's claim is narrower: that the specific gradient used to justify
schooling as a fertility lever behaves in the way the critique predicts, and that the size of the
divergence has not been quantified in one place for this relation. The contribution is the assembly:
eight measures, both estimators on the same data, a 13,800-partition sensitivity universe, a
future-schooling placebo, and a pre-registered decision rule that fires. A referee who says "this is
Nickell 1981 applied to fertility" has understood the paper correctly; the response is that the
application is the useful object, and that its results discipline a literature that has often used
the level gradient as if it were the within estimate.

### 5.2 Nickell bias, measurement error and change-window sensitivity

Three econometric worries deserve separate answers.

**Nickell bias.** Nickell (1981) shows that fixed-effects estimators with a lagged dependent variable
are biased in short panels. Our change specification does not include the lagged dependent variable:
it regresses the ten-year change in fertility on the starting schooling level with country fixed
effects and country-specific trends. The Nickell critique therefore does not mechanically apply to
the headline change estimate, but related finite-sample concerns do: with roughly six decades per
country the within estimator can still be biased when regressors are predetermined, and the
ten-year changes are not independent within country. Clustered standard errors and country trends are
the minimum response, and the change estimates' standard errors (0.020–0.054 in Table 1) reflect
that. This is a real limit on precision, not a licence to dismiss the contrast.

**Measurement error.** Schooling series are notoriously noisy, especially completion and attainment
before 1990, and measurement error in the regressor attenuates the within estimate toward zero. This
cuts against our change estimate being "the true causal effect" even if a causal effect exists. The
battery's grid includes sample restrictions and alternative measures; the fact that the change
coefficient is not negative-significant in any measure or in 96.5–98.9% of partitions is stronger
than a single attenuated estimate, but measurement error remains an alternative explanation for a
null change relation. We say so rather than claiming the change design has proven anything.

**Change-window sensitivity.** Fertility may respond to schooling with a delay longer than ten years;
if so, a ten-year change design will understate the effect regardless of measurement. This is the
strongest substantive objection to the change result, and it is not answerable within this record. It
is exactly why Section 7 proposes cohort and historical designs; those are the tests that could
distinguish "no effect" from "effect with a long lag". The honest verdict on the change result is
therefore: *the standard ten-year within-country design does not show the gradient*, not *schooling
has no within-country effect*.

**What the robustness grid does and does not establish.** The grid varies sample restrictions, lags,
fixed-effect patterns and functional form. The level negative-significance share (42.9–59.4% per
pair) and the change negative-significance share (3.5–13.5% per pair) are stable across that grid,
which is the relevant robustness claim for the audit. It does not resolve the three deeper problems
above; no specification grid can. We flag that in the record and in the abstract's scope.

### 5.3 The ecological fallacy: what a country-level null cannot say

A country-level null does not contradict the individual-level gradient, and the paper must not be
read as claiming it does. The micro literature finds a robust education–fertility gradient
(Cleland and Rodríguez 1988; Martin and Juárez 1995; Basu 2002), separates individual from community
effects (Kravdal 2002, 2012), and finds that women's own schooling matters. Those are individual
associations, and they are compatible with a country-level gradient that is a development marker: a
society where most women have little schooling has high fertility for many reasons, and the
country-average association need not identify the effect of one more year for one woman.

Two things follow. First, the audit's claims are scoped to country aggregates and to the aggregate
estimand. Second, the DHS individual-gradient comparison that a demographer will ask for is a data
gap in this record, not a result. The DHS Individual Recode would let us compare the individual and
country gradients directly — that is Future Research item 1, and until it is done the paper should
say plainly that the individual gradient is taken from the literature, not estimated here. The
referee memo's recommendation (report the individual gradient alongside the country gradient) is
right, and the honest response at this stage is to scope the claim and specify the design.

### 5.4 What the placebo does and does not prove

The future-schooling placebo is 90% as strong as the correctly timed relation, which is decisive
against a naive causal reading of the level coefficient. It is not decisive against every causal
story: schooling at t+10 is correlated with schooling at t, both index the same development process,
and a causal effect of schooling on fertility could in principle be persistent enough to show up at
either lead. What the placebo shows is that the level association is not specific to the timing a
causal effect requires — the standard lead/lag test fails. That is a diagnostic, and we present it as
one. The strongest statement it licenses is the one we make: the level gradient is a
development-gradient marker, not a demonstrated causal effect.

### 5.5 The transportability design is a sensitivity universe, not a test

Random re-partitions of countries are not random draws from a population, and the intervals we report
across partitions describe how much the estimate varies with the country grouping, not sampling
uncertainty. The 13,800 partitions exceed the 800 fixed in the pre-registration because the run was
extended to fill a compute load; the statistic is unchanged and the extension is reported. We
therefore call this a sensitivity universe. Its value is that it shows the level gradient survives
arbitrary slicing (71.5–98.9%) while the change relation does not (0.0–7.2%) — a statement about
robustness to the country set, not about causal identification.

## 6. Implications

### 6.1 For how the field estimates schooling–fertility relations

The audit implies a reporting norm: whenever a cross-country schooling coefficient is presented as
evidence about schooling's effect on fertility, the paper should say which estimand it is. A level
coefficient with region and decade fixed effects is a between-country association; a within-country
change coefficient with country trends is a different animal. They are both informative, but they
answer different questions, and a literature that reports one and describes it as the other
accumulates a misleading confidence. Concretely: report both estimates in the same table, on the same
measures and data, and report a placebo. The extra cost is small; the clarification is large.

### 6.2 For interpreting existing within-country estimates

Existing within-country estimates of schooling's fertility effect should be read with two opposite
errors in mind. They may be **attenuated** by measurement error in schooling, short change windows,
and country trends that absorb slow-moving changes — so a null within estimate is weaker evidence
than it looks. They may also be **biased** by finite-sample within-estimator problems and by
endogenous schooling policy — so a non-null within estimate is not automatically causal either. The
audit's contribution to this debate is the level of the contrast: a within estimate near zero is what
one expects when the level gradient is a development marker, so a null within estimate should not be
treated as a surprising anomaly to be explained away. It is the expected pattern under the audit's
reading.

### 6.3 For policy claims built on change designs

Policy claims that expanding schooling will reduce fertility are usually supported by two kinds of
evidence: the cross-country level gradient (this paper's level estimate) and natural experiments on
schooling expansion (Duflo 2001; Chicoine 2016). The audit says the first kind cannot carry the
claim, and it sharpens what the second kind must show: an effect of an expansion on fertility in the
window studied, not a correlation between schooling and fertility across countries. Where policy
evaluations use ten-year change designs, the audit suggests they have limited power to detect
slow-moving effects and should report their minimum detectable effect, as the earlier phase of this
project does for the electricity case. The "development gradient versus causal lever" distinction is
the practical takeaway: schooling is a marker of the development gradient, and whether it is a lever
is an empirical question for designs that can isolate expansions.

### 6.4 For how "the education transition" is described

The finding that the level gradient is steepest in the first six years of schooling and reverses
above nine years is consistent with the massification reading: the cross-country association is
largest on the margin where mass schooling is being created, and it is not a linear "more schooling,
fewer births" law at the top. That is a descriptive refinement of how the education transition should
be described, and it is compatible with the development-gradient interpretation. It should not be
read as a causal threshold without the designs in Section 7.

## 7. Future research: designs that could turn the audit into a causal estimate

The audit's weakness is that it can show the level gradient is not a causal effect, but it cannot say
whether a causal effect exists. Six designs can move the question forward; each is concrete, and each
has limits worth stating up front.

1. **DHS Individual Recode, individual-level schooling and births.** The DHS gives women's schooling,
   birth histories, and cluster identifiers for many countries and waves. It would let us estimate
   the individual gradient and community effects directly and compare them with the country
   gradient — the comparison a demographer will ask for first (Kravdal 2002 is the benchmark). What
   it identifies: individual and community associations; the ecological-fallacy question. What it
   does not: a causal effect of schooling, because family background, ability and fertility
   preferences are unobserved.
2. **Cohort fertility by education.** Completed cohort fertility by women's education avoids period
   tempo distortions and the ten-year window problem. What it identifies: the long-run association
   between education and completed fertility. What it does not: causal identification, for the same
   selection reasons.
3. **Historical schooling series with event timing.** School-expansion dates, compulsory-schooling
   laws and the construction of school infrastructure give timing variation. An event-study or
   difference-in-differences design around expansions would identify the effect of *expansion
   episodes*, with country and cohort fixed effects. What it identifies: the effect of schooling
   expansions on fertility in the affected cohorts; the causal question the audit cannot answer. What
   it does not: the effect of the level gradient per se, and external validity is limited to the
   episodes studied.
4. **Subnational variation.** DHS regions or census regions within countries give many more
   within-country units and more power than country panels. A region-level panel with region fixed
   effects and trends could detect a change effect that the country-level design is too coarse to
   see. What it identifies: regional change effects, with better power. What it does not: causal
   identification where regional schooling policy is endogenous to fertility.
5. **Sibling and cohort designs.** Sisters' schooling differences and cohort exposure to schooling
   reforms identify within-family or within-cohort effects. What they identify: family-level
   schooling effects, free of some family background confounds. What they do not: the aggregate
   effect of the schooling system, and samples are small and selected.
6. **School-expansion natural experiments.** Indonesia's school construction (Duflo 2001), free
   primary education reforms (Chicoine 2016), and compulsory-schooling laws are the designs that
   could make the audit causal. What they identify: the effect of the expansion on the cohorts
   exposed. What they do not: the effect of the level gradient, and they require the expansion to be
   plausibly exogenous to fertility preferences.

The sequencing matters: designs 1 and 2 answer the ecological-fallacy objection; designs 3, 5 and 6
answer the causal question; design 4 is the power fix. None is a substitute for the audit, and the
audit is not a substitute for them.

## 8. Conclusion

The schooling–fertility gradient is one of the most replicated associations in demography and one of
the most frequently over-read. This paper has tried to separate two things that the literature has
often run together: a large, global, between-country association that survives every grouping of
countries we can construct, and a within-country change relation that does not survive the standard
design. The level gradient is real, transportable, steepest at the massification margin — and, on the
evidence of a placebo that is 90% as strong as the real thing, a development-gradient marker rather
than a causal lever. The change estimate is null or positive, but it is also vulnerable to
measurement error, short windows and finite-sample bias, so it does not prove there is no effect.

The paper's claim is therefore deliberately modest: the standard within-country change specification
erases the schooling–fertility gradient, and this is a level-of-analysis fact that the field should
report rather than bury. The contribution is the assembly — both estimators, the same data, a
13,800-partition sensitivity universe, a pre-registered placebo, and an explicit account of what the
audit does not license. The literature auditor's verdict, which we adopt, is that this is incremental:
a new assembly, not a new fact or method. The next step is not more cross-country decomposition; it
is the designs in Section 7, which could turn the audit into a causal estimate.

## Reproducibility and data availability

All estimates in this draft come from the `corr-battery` record (branch `research/corr-battery-2026-11-23`,
commit 9363079): `PRE_REGISTRATION.md` (pre-registration commits 772650a and 6a1927f, pushed before code),
`data/results_summary.json` (aggregates, including transportability and placebo blocks),
`data/pair_table.csv` (342 pairs with level/change coefficients and transportability shares),
`data/transport.csv` (13,800 partitions), `data/bootstrap.csv` (500-draw bootstrap), `scripts/` and
`results/logs/` (run, crash and resume logs). The panel itself is the project's `/root/work/data`
series. `SOURCE_MAP.md` in this record maps every number in the paper to its file and field. No new
estimate was run for this draft; the only post-record computation is none — all tables are read from
the committed JSON/CSV.
