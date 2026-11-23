# The level of analysis decides the answer: a synthesis of schooling, fertility, and the development gradient

**Paper F — omnibus fertility synthesis (draft for Population and Development Review / Demographic Research)**

*Working draft, 25 November 2026. Every number in this paper traces to a verified project record (branch @ commit,
file, field); the claim-to-source map is in the record's `data/claims_sources.csv`. The paper is a descriptive
synthesis: it reports what the project found, under which designs, and with which caveats. It does not claim
causal identification of the effect of schooling on fertility, and no sentence in the abstract, introduction, or
conclusion should be read as such.*

## Abstract

The demography of schooling and fertility contains a contradiction that is usually smoothed over: cross-country
studies find a large negative association between schooling and fertility, while panel studies with country fixed
effects often find none. This paper synthesises a coordinated programme of work that treats the contradiction as
the object of study rather than as a nuisance. We report five sets of results. First, in levels, all eight
schooling measures available in a 1960–2024 country panel predict lower fertility strongly and precisely (women's
mean years of schooling: −0.129 births per woman per year, SE 0.029, n = 5,915 country-years, 192 countries), and
the association survives a 336-specification curve (99.7% of 288 period specifications negative, 91.3% negative
and significant). Second, in ten-year changes with country fixed effects and country trends the association
vanishes or reverses: the change coefficients are small, and for several measures significantly positive (no
measure has a negative-significant change coefficient). Third, across 13,800 random re-partitions of countries
into six groups, the schooling–fertility level relation is negative and significant in 71–99% of groups, against
0–7% for the change relation: the level relation is a global between-country property, the change relation is
not. Fourth, a future-schooling placebo is about 90% as strong as the correct-time relation (52.9% versus 58.8%
of cells negative and significant), so the level gradient is a development-gradient association, not an
identified schooling effect. Fifth, the gradient is steepest in the first six years of schooling (−0.326, 95% CI
[−0.405, −0.248]) and flattens, then reverses sign, above nine years. The synthesis also reports the project's
nulls — an ecological survey-level gradient that is real but attenuates across cohorts, a care-work loop that is
absorbed by income and urbanisation, a strong "no-off-switch" claim that is falsified while a weak form survives,
and a transition model whose mortality counterfactual removes only 3.2% of the fertility fall — with the same
discipline: all specifications reported, placebos decisive, descriptive language throughout. The verdict is that
the schooling–fertility relation is a robust, global, between-country gradient marking where countries sit in the
development process, that the within-country design erases exactly the variation that gradient lives in, and that
neither design identifies a causal effect of schooling on fertility. For policy, the synthesis cautions against
reading the cross-country gradient as a lever: mass schooling marks the fertility transition's development
margin, it is not a demonstrated instrument for accelerating it.

## 1. Introduction

### 1.1 A contradiction that is usually smoothed over

Ask a demographer whether more schooling means fewer births and the answer will depend, in a predictable way, on
which literature the demographer reads. The cross-country literature — the Barro–Lee tradition in economics, the
Lutz–KC tradition in demography, the human-capital tradition from Mincer and Becker onward — reports large
negative associations between schooling and fertility, associations that are robust to income, urbanisation, and
a long list of controls (Barro & Lee, 2013; Lutz & KC, 2011; Mincer, 1958; Psacharopoulos & Patrinos, 2004). The
panel literature — country fixed effects, decade changes, sometimes country-specific trends — reports something
much smaller, often indistinguishable from zero, and occasionally the wrong sign. The two literatures rarely
confront each other directly. When they do, the disagreement is usually attributed to measurement, to sample,
or to the choice of schooling measure, and the discussion moves on. That attribution is, in our reading of the
evidence, wrong. The disagreement is about the level of analysis, and it is large enough to decide the sign of
the answer.

This paper synthesises a coordinated programme of work that took the contradiction seriously. The programme asked
four questions in sequence. How large is the schooling–fertility association when it is estimated at the level at
which it is a near-universal empirical regularity — the between-country level? What happens to the association
when the same measures are estimated on within-country changes? Is the level association a global property of
countries, or an artefact of the particular groupings (regions, income classes, decades) that researchers happen
to use? And if the level association is global but does not survive a timing placebo, what is it a property of?
The answers, developed in the sections that follow, are: large and precise; it disappears or reverses; it is a
global property for the schooling–fertility relation; and it is a property of the development gradient, not of
schooling as an intervention.

The tension is not new. Robinson's (1950) warning that correlations between units need not describe relations
within units is the canonical statement, and the panel-data literature has known for four decades that the
between and within components of a panel identify different parameters with different biases (Hausman & Taylor,
1981; Nickell, 1981; Angrist & Pischke, 2009; Bell & Jones, 2015). Cross-country growth econometrics has fought
the same battle over levels versus changes and over the fragility of cross-country coefficients (Brock &
Durlauf, 2001; Durlauf, Johnson, & Temple, 2005; Levine & Renelt, 1992; Sala-i-Martin, 1997). What is new here is
not the methodological principle; it is the systematic application of the principle to the schooling–fertility
relation, with the full specification space reported, with a re-partition transportability test, and with a
placebo that can discriminate between the two interpretations of the cross-country gradient.

### 1.2 What this paper synthesises

The paper brings together five workstreams that were run as separate pre-registered investigations and are
reported here in a common voice and a common evidence standard:

1. **The level-of-analysis workstream.** A pre-registered specification curve (336 specifications) and a
   levels-versus-changes comparison for the schooling–fertility relation in the project's 1960–2024 panel, plus a
   re-partition transportability experiment (13,800 random six-group re-partitions) and a future-schooling
   placebo, extended to a 342-pair, 57.3-million-regression battery. This is the paper's core.
2. **The survey-level ecological gradient.** A harmonised analysis of 346 DHS surveys across cohorts, asking
   whether the fertility gradient by education is a survey-level (ecological) phenomenon, whether it attenuates
   across cohorts, and whether it survives the pipeline of survey design. The honest limitation is that
   individual microdata were not available for the harmonised sample, so the section's claims are ecological
   claims, and are labelled as such throughout.
3. **The care-work loop and the no-off-switch question.** Tests of whether the care-work burden, credit
   constraints, and policy foreclosure generate a self-reinforcing low-fertility loop, whether a strong
   "no-off-switch" claim (that once fertility falls below a threshold it cannot recover) holds, and whether
   fertility transitions exhibit a tipping point.
4. **The transition engine and the individuation model.** A calibrated counterfactual that shuts off the
   mortality decline, a model of individuation (the "dose" model) in which schooling and marriage-market position
   govern fertility, an out-of-sample comparison against a development-only rival, and a tolerance ladder that
   shows whether the model's wide parameter intervals are an identification limit or a statistical artefact.
5. **The threshold shape.** A piecewise-linear analysis of where in the schooling distribution the between-country
   gradient is steepest, and what that location implies for the massification of schooling.

The synthesis is deliberately structured as a hierarchy of evidence. Sections report, in order of decreasing
identification strength: what the data show descriptively at the level of countries (Sections 3 and 5); what the
survey-level and individual literatures add (Section 6); what the mechanism tests and model comparisons can and
cannot establish (Section 7); and what the nulls imply (Section 8). Each section carries a verdict label — S for
*what survives*, F for *what fails*, C for *what cannot be tested with these data* — and the labels are the
paper's contribution as much as the numbers are.

### 1.3 Contributions

The paper makes five contributions, stated here in the plainest terms the evidence allows.

First, it **demonstrates rather than asserts the level-of-analysis problem** for schooling and fertility. The
levels result is reported across a pre-registered specification curve with every cell visible, and the changes
result is reported on the same measures and the same panel; the contrast is not a comparison of two literatures
with different samples, it is a comparison of two designs on one dataset. The levels coefficient for women's
attainment is −0.129 (SE 0.029) on 5,915 country-years and 192 countries; the ten-year change coefficient for
the same measure is +0.111 (SE 0.045), significantly positive.

Second, it performs a **transportability test of the between-country property**. Rather than asking whether the
relation appears in the usual regional groupings, the programme re-partitions the panel's countries into 13,800
random six-group splits and asks how often the relation reproduces itself. For the schooling–fertility pairs,
the level relation is negative and significant in 71–99% of arbitrary groups; the change relation in 0–7%. This
is the strongest evidence available in the project that the level relation is not a grouping artefact. The same
test also reports the sobering matrix-wide result (22.7% against 11.1% across all 342 ordered pairs), because a
synthesis that reported only the favourable version of the re-partition test would be doing exactly what the
paper criticises.

Third, it **quantifies the development-gradient caveat** instead of asserting it. The future-schooling placebo is
a natural diagnostic: if schooling *at time t+10* predicts fertility *at time t* almost as well as schooling at
time t, then the level correlation is not identifying the effect of schooling at a point in time. In the large
grid the placebo reaches 90% of the correct-time magnitude for the schooling–fertility pairs; the pre-registered
decision rule therefore fires, and the paper records the level gradient as descriptive throughout. This is a
convenience for critics and a cost for advocates: the gradient is real and global, and it still cannot be read
causally.

Fourth, it **brings the nulls into the same frame**. The project's other fertility workstreams — the DHS
ecological gradient, the care loop, the no-off-switch claim, the tipping-point test, the mortality
counterfactual, the tolerance ladder — produced a mixture of survivors, failures, and untestable claims. The
synthesis reports them with the same claim-to-source discipline as the headline result. An omnibus fertility
paper that reported only the striking levels result would be a misleading document; the nulls are what make the
surviving claims credible.

Fifth, it **locates the gradient in the schooling distribution**. The threshold analysis shows that the
association is concentrated at the bottom of the distribution: −0.326 (95% CI [−0.405, −0.248]) below six years,
−0.092 [−0.175, −0.013] between six and nine years, and +0.112 [+0.057, +0.171] above nine years. That location is
the empirical bridge to the historical transition: the steepest part of the between-country gradient is the
margin the massification of schooling traversed.

### 1.4 What the paper does not claim

It is as important to state what this paper does not establish. It does not claim to identify the causal effect
of schooling on fertility; the placebo analysis is designed to show that the level design cannot do so, and the
paper's language is descriptive throughout. It does not claim that schooling is irrelevant to fertility; the
individual-level literature is clear that parental education predicts lower fertility within populations
(Cleland & Rodriguez, 1988; Kravdal, 2002; Chicoine, 2012; Osili & Long, 2008), and nothing here contradicts it
— the claim is about what a between-country level regression identifies. It does not claim that the within-country
change design is "wrong"; it is the right design for a different question, and the paper explains which question.
It does not claim novelty for the observation that levels and changes disagree; the methodological point is old
(Robinson, 1950; Nickell, 1981), and the paper cites it as old. What is new is the systematic demonstration for
this relation, the re-partition test, the quantified placebo, and the synthesis of the programme's other
findings into one verdict table. And it does not claim that any of the project's other workstreams settle the
fertility transition; they narrow the space of live hypotheses, which is what the evidence supports.

## 2. Data and evidence standard

### 2.1 The panel

All cross-country analyses use the project's country-year panel, 1960–2024, observed values only. The panel is
built from standard public series: the World Bank's World Development Indicators for income, urbanisation, and
the sectoral measures; Barro–Lee attainment (via the OWID series where the official tables were unreachable from
the compute node) for mean years of schooling; the project's harmonised enrolment and completion series for the
remaining measures; and UN and national sources for fertility and mortality. No imputation and no interpolation
are used in any estimation sample; the project's imputed panel exists for other purposes and is not used in the
paper's cross-country results. Income enters all specifications in logs. Standard errors are clustered by country
throughout. The panel is unbalanced, and every table reports the effective sample (country-years and countries)
rather than only the nominal one.

### 2.2 Measures

Fertility is the total fertility rate, births per woman. Schooling is measured eight ways: mean years of schooling
for women and for the total adult population; gross secondary enrolment; lower-secondary completion; primary
completion; tertiary enrolment; and the gender-parity indices for secondary and tertiary enrolment. The
multiplicity is deliberate. The literature disagrees about which measure is the right one, and the paper's claim
is that the level-of-analysis result is not an artefact of that disagreement: the levels result is negative and
significant for all eight measures, and the changes result is weak for all eight. Additional variables —
mortality, marriage, labour-force participation, sectoral composition, policy indicators — enter the mechanism
and null-result sections, where their provenance and construction are documented in the relevant section.

### 2.3 Designs

Five designs recur across the paper, and the evidence standard depends on keeping them distinct.

**Levels.** Fertility level on schooling level, with decade and region fixed effects, log income and
urbanisation controls, all years. This design uses between-country variation; it answers "do countries with more
schooling have fewer births?"

**Ten-year changes.** The change in fertility over ten years on the starting level of schooling, with country
fixed effects, decade effects, country-specific linear trends, log income and urbanisation. This design uses
within-country variation and absorbs all time-invariant country characteristics; it answers "when a country's
schooling stock rose, did its fertility fall faster?"

**Specification curves.** Pre-registered grids of specifications (fixed-effect designs, control sets, lags,
functional forms, sample splits), with every cell reported, not a selected subset. The paper's convention is that
a result is "robust" only if the sign survives the whole reported grid.

**Re-partition transportability.** Random re-partitions of the panel's countries into groups of the same sizes
as the substantive groupings, with the relation re-estimated within each group for every re-partition. The
statistic is the share of group-by-pair estimates that are negative and significant. This tests whether the
relation is a global property or a grouping artefact.

**Placebo designs.** A variable that cannot plausibly cause the outcome under the causal story is substituted for
the candidate cause (future schooling for current schooling; male care-work for female care-work; manufacturing
for care work). If the placebo is as strong as the candidate, the candidate's association is not identified.

### 2.4 Pre-registration, recording, and reporting discipline

Every workstream was pre-registered before its analysis code ran: the specification grid, the sample splits, the
bootstrap counts, and the decision thresholds were committed to the branch before the runs, and the paper cites
those commits. Every number reported here traces to a record path (branch @ commit, file, field) in the
`claims_sources.csv`; the record's README files state the deviations that occurred (unreachable sources,
estimable-cell counts, load-driven extensions) rather than hiding them. The synthesis's own conventions are
stated here so a reader can check them: bold in tables means |t| > 1.96; "significant" means the country-clustered
standard error implies |t| > 1.96 unless otherwise stated; "negative-significant share" means the share of
specifications (or groups) with coefficient < 0 and |t| > 1.96; and "survives" means the result holds across the
reported specification space, not that it is causally identified.

### 2.5 Evidence grades

Each section's claims carry one of three labels. **S (survives)** means the claim holds across the reported
specification space and survives its designed falsifiers. **F (fails)** means the claim is contradicted by the
reported evidence, and the paper says so plainly. **C (cannot be tested)** means the data cannot discriminate, and
the paper says which observation would have been needed. The labels are not decoration: they are the mechanism by
which an omnibus paper avoids the omnibus temptation to make everything sound like it worked.

## 3. The level of analysis: a global between-country gradient that within-country changes erase

*The full section, with tables, is Section 1 of this document (the section files are numbered by workstream and
this introduction is numbered separately; the paper's own numbering will be unified in the final formatting
pass).*
