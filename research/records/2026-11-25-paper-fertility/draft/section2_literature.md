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
