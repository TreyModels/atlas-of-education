# Which Countries Does the Coefficient Describe? A Grouping Multiverse for Cross-National Panel Claims

**Trey Menefee**
Atlas of Education
Working paper, 23 November 2026

---

## Abstract

Cross-national panel studies routinely summarise a relationship with one pooled coefficient estimated under country and period effects. That number is usually read as a description of "the world", but it is an average over countries that may not share the relationship at all. This paper develops a *grouping multiverse*: the countries are re-partitioned into groups in 50 different ways across eight families of country typology (geography, income, demography, schooling, economy, institutions, k-means profiles, and grouped fixed-effects classes), the full within-country lead-lag matrix is re-estimated inside every group, and each link is compared with the same test performed on random re-partitions of identical group sizes. The random re-partition holds the pooled association fixed, so the resulting null is a test of *heterogeneity and transportability*, not of whether the pooled association exists. In two applications — the drivers of fertility decline and the drivers of schooling expansion — the procedure separates links that travel across country types from links that live only in particular types and from links that are no better than random slicing. Five of 272 links are robust in every kind of grouping; 76 are group-specific; 161 are no better than random. The two fertility links (child mortality and life expectancy leading to fewer births) travel, and no massification driver does. The paper's methodological contribution is a *resolution analysis*: with R random draws the empirical p-value floor is 1/(R+1), and Benjamini–Hochberg at 5% over 272 links needs a first-step p of 0.05/272 = 0.00018, so a lone link would need about 5,440 draws, while a cluster of extreme links at the floor can be certified by the step-up rule (35 links at 400 draws). The rule is arithmetic, not a calibrated test: the 272 tests are dependent because they share draws, the dependence is not uniformly positive, and the effective number of tests is about 157. Under an effective-tests correction 44 links are certified, a dependence-aware permutation null certifies zero in 400 pseudo-runs, and we therefore state the rule as a pre-specified draw budget and certification ceiling conditional on independence or positive dependence, with a sensitivity bound. That is the paper's methodological claim, stated as a design rule with an explicit dependence caveat, not as a new method. We report 74- and 400-draw runs, their disagreement, a split-halves stability test, and a determinism check, and we state plainly what the method cannot do: it tests transportability, not identification.

**Keywords:** multiverse analysis; specification curve; grouped heterogeneity; transportability; cross-national panel data; multiple testing; resolution limits

---

## 1. Introduction

A familiar genre of cross-national claim takes a panel of countries, differences out country and period effects, and reports a single coefficient: more electricity is associated with more schooling; lower child mortality is associated with fewer births; more wage employment is associated with faster schooling expansion. The coefficient is then interpreted as a property of development, and sometimes as a policy lever. The interpretation is vulnerable to a well-known objection, stated most influentially by Brock and Durlauf (2001): a pooled cross-country regression imposes one slope on countries that are not the same object. If the relationship differs by country type, the pooled coefficient is an average that no country actually has, and the usual robustness exercises — adding controls, dropping outliers, averaging over specifications — do not answer the question, because they average over model uncertainty rather than over the heterogeneity of countries. Durlauf, Johnson, and Temple (2005) develop the point into a programme for growth econometrics: the object of interest is not "the" coefficient but the mapping from country characteristics to effects.

This paper takes that objection as its starting point and asks what would have to be true for a cross-national coefficient to be a useful description. The answer we propose is not a better pooled regression. It is a systematic enumeration of the country typologies over which the coefficient is implicitly averaged, combined with a calibration device that says what ordinary sampling and power alone would produce. We call the procedure a **grouping multiverse**.

The design is simple to state. Take the project's within-country lead-lag matrix: 17 country-level measures, each link estimated as the association between a measure at time t and the ten-year change in another measure, with country effects, decade effects, income (logged) and urbanisation controlled, and with or without a straight-line country trend. Estimate all 272 directed links in the whole sample. Then re-partition the 217 countries into groups in 50 different ways — 179 groups in total — spanning geographic regions and continents, income classes, demographic classes (birth rate, child mortality, life expectancy, timing of the fertility transition), schooling classes, economic structure (farm output, farm employment, urbanisation, electricity access), fiscal institutions, k-means clusters on a 1990 profile, and grouped fixed-effects classes in the sense of Bonhomme and Manresa (2015). Re-estimate the whole matrix inside every group. Finally, do the same thing on random re-partitions of the countries that preserve the group sizes and the nesting of cuts. The random re-partitions define what chance alone produces: in a world where a link is the same everywhere, a random slice of the countries will show the link nearly as often as a real slice, merely with less power.

The comparison yields a four-way verdict for each link: *robust everywhere* (the link travels: it is significant in the whole sample in both specifications, in at least half of real groups with trends, in at least a quarter of every family, and it does not flip sign more often than random groups); *group-specific* (some real groupings beat random groupings in the same direction, with a mean z of at least 2 and at least half of the relevant groups significant, at 5% false discovery); *beats random without a clear group* (the link is more common in real than in random groups but is not concentrated in any named family); or *no better than random* (the link is real in the pooled matrix but indistinguishable from random slicing). The verdict rules are explicit and are themselves falsifiable: each verdict is a conjunction of conditions, and failing any condition moves the link down a category.

The paper reports two runs. The first used 74 random re-partitions (the "74-draw" run) and an analysis that approximated the random yardstick with a normal distribution. The second used 400 re-partitions and replaced the approximation with empirical p-values, adding a strict tier alongside the smoothed one. The second run includes the first 74 draws, and the overlap is bit-identical, so differences between runs are differences in the estimated yardstick, not in code or data. The substantive results are stable: the same five links are robust in every kind of grouping, and the massification drivers remain fragile; the group-specific and no-better-than-random counts move by a few links.

The paper makes four contributions.

1. **A multiverse over country groupings rather than over analytic choices.** Existing multiverse and specification-curve methods vary the analyst's decisions — controls, functional form, outlier rules, coding — and report the distribution of results. We vary the *population partition* instead. The question is not "does the result depend on how I analysed it?" but "does the result depend on which countries I am talking about?" This is a transportability question, and we argue that grouping is the natural multiverse dimension for it.

2. **The random-grouping null as an estimable calibration device.** Permutation logic is old, but the relevant permutation here is a re-partition of countries into groups of fixed sizes. That null is computable, reproducible, and — crucially — it does not hold the answer fixed: it holds the *pooled* association fixed while destroying the country-type structure. It therefore measures heterogeneity rather than existence.

3. **A resolution analysis, with an explicit dependence caveat.** We show that the empirical p-value floor of a random-grouping multiverse is 1/(R+1), that Benjamini–Hochberg at 5% over 272 links requires a first-step p of 0.00018, that a lone link therefore needs about 5,440 draws, and that a cluster of links tied at the floor can still be certified because BH is a step-up rule. Because the 272 tests share draws, we also report the effective number of independent tests (about 157), the certified count under an effective-tests correction (44 rather than 35), and a dependence-aware permutation null for the cluster count (zero in 400 pseudo-runs). The contribution is a pre-specified draw budget and certification-ceiling rule conditional on independence or positive dependence — a design rule, not a calibrated test.

4. **Two applications with honest verdicts.** In fertility, two links travel and thirteen are group-specific; in massification, nothing travels and paid employment is a clean null. The pattern is what Durlauf's critique predicts, but the paper's point is that the prediction can be measured rather than merely asserted.

The remainder of the paper is organised as follows. Section 2 reviews the relevant literatures and states the gap. Section 3 describes the estimator, the groupings, the random null, and the verdict rules, including a subsection on what the null does and does not test. Section 4 describes the data. Section 5 reports the results, sorted by application. Section 6 gives the resolution analysis and the three reporting tiers. Section 7 relates the design point by point to prior work. Section 8 discusses what the results mean and where the method could go. Section 9 states the limitations. Section 10 covers reproducibility, Section 11 suggests target venues, and the appendices give definitions, the grouping inventory, and a plain-language summary.

---

## 2. Literature review

### 2.1 Researcher degrees of freedom and the multiverse

The modern discussion begins with the observation that analytic choices are numerous and consequential. Simmons, Nelson, and Simonsohn (2011) showed that ordinary flexibility in data collection and analysis — choosing among dependent variables, covariates, subgroups, and stopping rules — can produce a reported false-positive rate far above the nominal one. Gelman and Loken (2014) generalised the point beyond deliberate fishing: even an honest analyst who chooses a specification after seeing the data is traversing a "garden of forking paths", and the resulting inference is not calibrated. Wicherts and colleagues (2016) turned the idea into a checklist of the degrees of freedom that should be reported.

The constructive response was the multiverse analysis of Steegen, Tuerlinckx, Gelman, and Vanpaemel (2016): enumerate the defensible analytic choices, run the analysis under every combination, and report the distribution of results rather than a single one. The specification curve of Simonsohn, Simmons, and Nelson (2020) is the same logic presented as a visual and inferential object: specifications are ordered by effect size, the curve is plotted, and inference is conducted over the curve as a whole. Young and Holsteen (2017) provide a computational framework for multimodel analysis in sociology, and Muñoz and Young (2018) push the enumeration to billions of regressions while insisting on a multiplicity correction. Del Giudice and Gangestad (2021) review the promises and pitfalls of multiverse reasoning, including the risk that the multiverse itself becomes a garden of forking paths if the set of specifications is chosen after the fact. Orben and Przybylski (2019) give a widely cited applied example in the social sciences.

A related diagnostic tradition, the *vibration of effects*, examines how far an association moves as model specification is varied, and has been extended to measurement and sampling uncertainty (Patel, Burford, & Ioannidis, 2015; Klau, Hoffmann, Patel, Ioannidis, & Boulesteix, 2021). The multiverse has also spread into adjacent fields: panel-based models have received a formal treatment of their multiverse structure (Cantone & Tomaselli, 2023), specification curves have been used to identify heterogeneity across outcome definitions (Luo et al., 2024), class schemes have been submitted to a multiverse (Hertel, Barone, & Smallenbroek, 2025), and macroeconomic calibration has been given multiverse robustness tests (Kvarven, Lilletvedt, Strømland, & Johannesson, 2026). Most relevant here are the cross-national applications: Engzell and Mood (2023) run a multiverse over 82,944 definitions of income mobility, "varying how and for whom income is measured"; Herrala (2023) runs 768 multilevel models on 26 European countries, varying exclusion criteria, operationalisation and model formula; and Cakici, Fieberg, Neszveda, Piljak, and Zaremba (2026) examine up to 13,824 implementations of the cross-section of country equity returns. In all of these the dimension is analytic choice, outcome definition, or population definition *within a fixed set of countries*. The dimension here is the country partition itself.

Two features of this literature matter for the present paper. First, the multiverse dimension is almost always *analytic*: controls, functional form, coding, outlier treatment, model family. Second, the inferential target is usually the robustness of a single effect to analyst choices. Neither feature is inevitable. The dimension can instead be the *partition of the sample*, and the target can instead be the *transportability of the effect across populations*. That is the gap this paper occupies.

### 2.2 The heterogeneity critique and the robustness tradition

The cross-country growth literature supplies the sharpest statement of why a single pooled coefficient may not describe anything. Brock and Durlauf (2001) argue that growth empirics rests on implausible homogeneity assumptions: if growth processes differ across countries, then the "true" model is country-specific, the pooled parameter is a mixture, and the standard robustness exercise — varying the control set and reporting the distribution of coefficients, in the tradition of Leamer (1983) and the "two million regressions" of Sala-i-Martin (1997) — answers a question about model uncertainty rather than a question about the population. Durlauf, Johnson, and Temple (2005) develop the implications: theory should specify the sources of heterogeneity, and empirical work should estimate how effects vary with country characteristics.

The distinction is easy to blur and worth stating sharply. The robustness tradition asks: *across defensible specifications, is the sign and significance of the coefficient stable?* The heterogeneity critique asks: *across the countries being pooled, is the effect the same?* These are different questions with different failure modes. A coefficient can be stable across thousands of specifications and still be an average over countries that disagree in sign. Conversely, a coefficient can be fragile to specification while describing a genuinely uniform relationship. The grouping multiverse is designed for the second question. It does not replace the robustness tradition; it fills the dimension that tradition leaves out.

### 2.3 Grouped heterogeneity and grouped fixed effects

Econometrics has developed tools for exactly the kind of structure the critique describes. Bonhomme and Manresa (2015) introduce grouped fixed-effects estimators: units are assigned to a small number of groups, each with its own time profile, and the assignment is estimated rather than assumed. This is attractive when the relevant typology is unobserved, and it has the virtue of making the group structure an object of estimation. The present design uses grouped fixed effects in two ways: as one family of groupings (classes estimated on the birth-rate trajectory and on the income trajectory, with 2 to 6 classes), and as a benchmark against which the substantive families can be compared. The difference is that Bonhomme–Manresa classes are chosen to fit trajectories, whereas the grouping multiverse deliberately includes typologies that are substantively motivated and may cut the data in ways the trajectory fit would not choose. The two are complementary: the estimated groups answer "what does the data say the types are?", and the substantive families answer "do the types that theory names actually behave differently?".

### 2.4 Randomisation, permutation, and negative-control logic

The random-grouping null belongs to a family of calibration devices with a long history. Monte Carlo tests compare an observed statistic with its distribution under random relabelling or random re-sampling (Hope, 1968; Ernst, 2004). The key technical point for this paper is the finite-resolution one: when R random draws are used, the smallest attainable empirical p-value is 1/(R+1), not zero, and reporting zero is a claim of infinite evidence from finite simulation (Phipson & Smyth, 2010; North, Curtis, & Sham, 2002). That floor is the starting point of our resolution analysis.

Negative-control logic supplies the interpretation. Lipsitch, Tchetgen Tchetgen, and Cohen (2010) argue that a negative control — an exposure or outcome that should show no association if the design is sound — can detect confounding and bias that ordinary significance tests cannot. The random-grouping null is a negative control for the *grouping*, not for the exposure: it asks what the multiverse would look like if country type carried no information about the link. Randomisation inference with clustered assignment (Young, 2019) is the closest econometric relative: the assignment mechanism, not the sampling model, generates the reference distribution.

### 2.5 Multiplicity and the resolution of calibration

Testing 272 links at once requires a multiplicity correction. Bonferroni controls the family-wise error rate and is conservative; Benjamini and Hochberg (1995) control the false discovery rate and are the standard in high-dimensional settings. The choice matters enormously here because the floor of an empirical p-value distribution interacts with the correction. Under Bonferroni, a link needs p ≤ 0.05/272 = 0.00018, which no finite random-draw budget can reach for a single link until R is in the thousands. Under Benjamini–Hochberg, the threshold is rank-dependent: the k-th smallest p-value is compared with k × 0.05/272, so a cluster of links tied at the floor can clear the line collectively even though no single link could clear it alone. This is not a technicality; it is the difference between "this method cannot certify anything" and "this method can certify a cluster of extreme findings". Section 6 develops the arithmetic.

### 2.6 Transportability and external validity

The grouping multiverse is a transportability test in the sense of Pearl and Bareinboim (2014) and Bareinboim and Pearl (2016): the question is whether a relationship estimated in one population (here, the pooled sample) holds in target populations defined by country characteristics. The causal-inference literature formalises transportability with selection diagrams and do-calculus; the present paper is deliberately more modest, because it works with associations rather than identified causal effects. The relevant empirical tradition is the generalisation literature in programme evaluation: Hotz, Imbens, and Mortimer (2005) ask whether training effects estimated at one site predict effects at another, and Tipton (2013) develops propensity-score subclassification for generalising experimental results to target populations. Both make the same move we make: define the target populations explicitly, and report whether the effect travels. The difference is that these methods typically have an identified experimental effect to transport, whereas cross-national panel estimates are associational.

### 2.7 Inference with grouped data

Because the estimator is clustered by country, and because the groups being compared are themselves country aggregates, the grouped-data inference literature is directly relevant. Bertrand, Duflo, and Mullainathan (2004) show that ignoring serial correlation in difference-in-differences produces badly underestimated standard errors. Cameron, Gelbach, and Miller (2008) and Cameron and Miller (2015) develop the cluster-robust toolkit and its small-cluster problems, and Abadie, Athey, Imbens, and Wooldridge (2023) give the conditions under which clustering adjustment is warranted. The small-group problem is central to our limitations: with groups of 10 to 30 countries, cluster-robust standard errors are optimistic, so a single-group claim is the weakest kind of claim the design can make. This is why the verdict rules require recurrence across families and nesting cuts, and why the paper does not treat any single-group result as a finding.

### 2.8 What is missing

Two neighbouring literatures deserve to be named because they are the closest analogues we found. The vibration-of-effects framework varies model, measurement, and sampling choices and reports the resulting instability (Patel et al., 2015; Klau et al., 2021); the cross-national multiverse applications vary analytic choices within a fixed set of countries (Engzell & Mood, 2023; Herrala, 2023; Cakici et al., 2026). Our design differs on the dimension that matters for transportability: the population partition itself.

We are not aware of a study that treats the partition of countries into substantive typologies as the multiverse dimension and calibrates it against random partitions of identical size and nesting, with a formal resolution analysis of how many draws a certification would require. The multiverse literature varies analytic choices; the specification-curve literature varies specifications; the grouped-heterogeneity literature estimates latent groups; the transportability literature formalises target populations. The present paper combines the first and the last with a calibration device from the permutation tradition, and adds the resolution arithmetic. We make no claim to have invented any of the components; the claim is about their combination and about the resolution calculus that makes the combination honest about its own limits.

Two attacks are fair, and we prefer to name them rather than let a referee spring them. First, the random-partition null is a special case of clustered permutation inference with a fixed pooled association: randomising the labels of a fixed set of countries is, formally, a permutation test. What the design adds is not the permutation idea but the structure — group sizes matched to the real typologies, the nesting of cuts of the same ordering preserved, the typology dimension itself as the object of study, and the transportability reading that follows from holding the pooled association fixed. Second, the resolution analysis applies the known Monte Carlo p-value floor to Benjamini–Hochberg. What is new is the step-up arithmetic: because BH compares the k-th smallest p-value with k × 0.05/M, a cluster of links tied at the floor can be certified even when no single link can, which yields the draws-versus-cluster-size rule (5,440 draws for a lone link, about 182 for a cluster of 30) that we have not seen stated elsewhere. Section 6.6 tests the independence assumption this arithmetic needs and frames the claim as a design rule with an explicit dependence caveat (effective tests about 157; 44 certified under the correction; zero certified in a dependence-aware permutation null). The components are borrowed; the combination and the design rule are the claim.

---

## 3. Method

### 3.1 The underlying estimator

The panel contains 217 countries and 17 country-level measures observed from 1940 to 2025. For each ordered pair of distinct measures (x, y) — 272 directed links — the estimator regresses the ten-year change in y on the level of x ten years earlier, the starting level of y, and controls for log income per head and urbanisation (when neither is the link variable itself), with country fixed effects and decade fixed effects, and with standard errors clustered by country. Each link is estimated twice: once with country fixed effects only ("FE") and once with a country-specific linear trend added ("TR"). The trend specification partials out a straight line per country before the decade demeaning and fit. A country enters the trend specification only if it has at least four usable observations. Income is stored in levels in the source data and is logged here.

The estimator is a within-country lead-lag matrix: it asks whether a country that is higher on x than its own average is subsequently changing on y faster than its own average, net of the common decade and the country's level of income and urbanisation. It is not a causal estimator. It does not instrument, it does not exploit a discontinuity or a reform, and it does not claim to have removed all confounding. Everything that follows inherits this limitation, and Section 9 says so explicitly.

### 3.2 Groupings as typologies

The multiverse dimension is the partition of the 217 countries. Fifty groupings are organised into eight families:

- **Geography:** World Bank region (7 groups), continent (5), World Bank income group (4).
- **Income:** halves through fifths of 1990 log income (2, 3, 4, 5 cuts).
- **Demography:** 1990 birth rate cut 2 to 5 ways, 1990 child mortality cut 2 to 4 ways, 1990 life expectancy cut 3 ways, and two codings of the timing of crossing replacement fertility (3 and 4 bins).
- **Schooling:** 1990 secondary completion cut 2 to 5 ways, 1990 lower-secondary completion cut 2 to 4 ways.
- **Economy:** 1990 farm share of output (2, 3, 4 cuts), 1990 urban share (2, 3, 4 cuts), 1990 agricultural employment share (3 cuts), 1990 electricity access (3 cuts).
- **Institutions:** 1990 tax share cut 2 to 4 ways.
- **k-means:** clusters 2 through 6 on a standardised 1990 profile of six measures (birth rate, log income, urban share, secondary completion, child mortality, life expectancy), ordered by mean birth rate.
- **Grouped fixed effects:** Bonhomme–Manresa-style classes (2 through 6) fitted to the birth-rate trajectory 1960–2020 and, separately, to the log-income trajectory 1990–2020.

Two design choices matter. First, cuts of the same underlying measure are *nested*: the halves, thirds, quarters, and fifths of 1990 income are cuts of one ordering, so the groups at different depths are consistent with one another. The nesting is preserved in the random null, which is why a link that recurs across depths is stronger evidence than a link that appears at one depth only. Second, a group is estimated only if it contains at least 10 countries and at least 150 rows; otherwise the link is not estimated there. This threshold is a compromise between coverage and the small-group inference problem discussed above.

Across the 50 groupings there are 179 groups; a full pass over the real groupings produces 95,214 estimable group-by-specification cells. The design deliberately includes typologies that are *not* the usual clusters — the demography, schooling, economy, and institution families are theory-motivated country types, not regions — because the point is to search for typologies in which a relationship is stable, not merely to reproduce the familiar regional split.

### 3.3 The random-grouping null

For each of the 50 groupings, a random version is generated with the same number of groups and the same group sizes, drawing a random permutation of the covered countries and cutting it at the same sizes. The nesting rule is preserved: groupings that share a key (different cuts of one measure) share one random ordering, so the same country is in the "low" random group at every depth. The real-pass and random-pass estimates are produced by identical code on identical data; the only difference is the partition.

The comparison statistics are family-balanced shares. For each link, the share of groups in which it is significant with the same sign as the whole-sample estimate is computed per grouping family and then averaged across families, so that a family with many groupings (demography has 33) does not dominate one with few (institutions has 9). The same statistic is computed on every random draw, giving an empirical distribution of the share under random partitioning. Two additional statistics are computed: the *sign-flip rate* (the share of groups in which the link is significant in both directions across the multiverse) and the *heterogeneity rate* (the share of groupings whose group-specific estimates are jointly heterogeneous at 5%).

### 3.4 Verdict rules and falsifiers

Each of the 272 links receives one of four verdicts, in this order:

- **Robust everywhere.** The link is significant in the whole sample with both country effects and country trends; it is significant with the whole-sample sign in at least half of real groups in the trends specification; it is significant in at least a quarter of the groups in every family; and its sign-flip rate is not higher than random groups (specifically, at most the larger of 10% and the random mean plus 5 percentage points). This is a *similarity* criterion, not a superiority criterion: a uniform effect appears in random slices too, so the right test of "the same everywhere" is that real and random slices behave alike.
- **Group-specific.** No robust-everywhere verdict, but some tag (a named group, such as "the lowest-birth-rate trajectory class") beats its matched random cells in the same direction, at 5% false discovery across the tag-by-link comparisons, with a mean z of at least 2 (at least 3 for a single group), at least half of the cells in that tag significant, and — for the trends specification — the country-effects version pointing the same way.
- **Beats random without a clear group.** No robust-everywhere or group-specific verdict, but the family-balanced share beats the random distribution at 5% false discovery. These are links that are genuinely more common in real groupings than in random ones, without a named group explaining where.
- **No better than random.** None of the above. The link may be significant in the whole sample, but its behaviour across real groupings is indistinguishable from random slicing.

The falsifiers are built into the rules. A "robust everywhere" claim fails if the link is not significant in both specifications in the whole sample, if fewer than half of real groups are significant, if any family falls below a quarter, or if sign-flipping exceeds the random benchmark. A "group-specific" claim fails if no tag clears the false-discovery threshold, if the mean z is below 2, if fewer than half of the tag's cells are significant, or if the country-effects version disagrees. A "beats random" claim fails if the family-balanced share does not clear the smoothed null at 5%. And every claim is run against a second, independent falsifier — the split-halves test of Section 5.9 — which re-runs the verdicts on two disjoint halves of the random draws and asks whether the verdict survives.

### 3.5 What the null does and does not test

This subsection is the conceptual core of the paper, and it is worth stating as plainly as possible.

The random re-partition **holds the pooled association fixed**. The countries are the same countries, the measures are the same measures, and the estimator is the same estimator. What is destroyed is the *country-type structure*: the random groups have the right sizes but no substantive meaning. The null distribution therefore answers the question: *if the link were the same in every country type, how often would a real-looking grouping show it?* It does not answer the question: *is there a pooled association at all?* The pooled association is the input to the test, not the output. A link with a large pooled coefficient and no cross-type heterogeneity will appear in random groups nearly as often as in real ones — and that is a *pass*, not a failure. A link with a modest pooled coefficient that lives only in one type of country will beat random groupings in that type and fail everywhere else — and that is a finding about heterogeneity.

Two consequences follow. First, the multiverse cannot adjudicate causality. If the pooled association is confounded, every group-specific estimate is confounded too, and the null tests only whether the confounding is homogeneous. This is the honest answer to the deeper form of Durlauf's critique: the method tests transportability, not identification, and it does not rescue a coefficient from the objection that it is not a causal object. Second, the method can *quantify* something the critique only asserts. If the pooled coefficient is an average over country types whose effects disagree in sign, the sign-flip rate measures how much of it is an average of opposing effects; if the effects agree in sign but differ in size, the share statistics measure how much of it is a common effect seen with different power. That is the sense in which the grouping multiverse converts a philosophical objection into a measurable diagnostic.

---

## 4. Data

### 4.1 Panel and measures

The panel is the project's country-level panel, assembled from standard international series: national-accounts and development indicators for income, urbanisation, electricity, farm output and farm employment; education-attainment series following the Barro–Lee approach (Barro & Lee, 2013) for primary, lower-secondary, secondary, and tertiary completion and for gender parity; UN and World Bank mortality and life-expectancy series; and ILO labour-market series for wage employment and female labour-force participation. The per-series provenance is carried in the panel metadata; a reader re-running the analysis should confirm each series against its source before publication, because the panel is a working compilation rather than a published dataset.

The 17 measures are listed in Table 1. Income is stored in levels and logged before use. All measures enter as levels in the regressors and as ten-year changes on the left-hand side, so the estimand is the association between a country's relative position on x and its subsequent change in y.

**Table 1. The 17 measures.**

| Measure | Role in the matrix | Notes |
|---|---|---|
| Electricity access | x and y | share of population with access |
| Wage employment | x and y | share of employment that is paid |
| Lower-secondary completion | x and y | attainment share |
| Secondary completion | x and y | attainment share |
| Tertiary completion | x and y | attainment share |
| Primary completion | x and y | attainment share |
| GDP per head (log) | x, y, control | source stores levels; logged here |
| Urban share | x, y, control | share of population urban |
| Tax share | x and y | share of output |
| Farm share of output | x and y | agriculture, value added |
| Farm share of employment | x and y | agricultural employment |
| Female labour-force participation | x and y | share of women in labour force |
| Life expectancy | x and y | years |
| Under-5 mortality | x and y | deaths per 1,000 births |
| Gender parity, secondary | x and y | ratio of girls to boys |
| Gender parity, tertiary | x and y | ratio of girls to boys |
| Fertility | x and y | births per woman |

All 17 × 16 = 272 ordered pairs are estimated, each in two specifications, giving 544 edge specifications.

### 4.2 Coverage and gaps

The panel's metadata covers 296 territories and aggregates; the analysis keeps the 217 that have a non-aggregate three-letter ISO code and a region. Observations run from 1940 to 2025, so a country can contribute at most 66 ten-year change observations; in practice coverage is uneven, and the trend specification requires at least four usable observations per country. The design does not impute for the main results: a link is estimated on whatever complete rows a group provides, subject to the 150-row and 10-country thresholds. The project's imputed panel (twenty imputations plus a mean panel) exists, but the multiverse was run on the observed panel so that the results are not conditional on a particular imputation model. This choice costs coverage and should be revisited in a replication; it is flagged in the limitations.

### 4.3 Grouping variables

The grouping variables are measured at or near 1990 so that they are predetermined relative to most of the changes being studied: 1990 log income, 1990 birth rate, 1990 child mortality, 1990 life expectancy, 1990 secondary and lower-secondary completion, 1990 farm output and farm employment shares, 1990 urban share, 1990 electricity access, and 1990 tax share. The one deliberately non-predetermined grouping is the timing of crossing replacement fertility, which is a feature of the whole trajectory rather than a 1990 snapshot; it is included because the timing of the transition is a substantively important typology and because it is a *classification of countries*, not a variable on the causal path of any single link. The k-means and grouped-fixed-effects families use the trajectory information by construction. Table 2 summarises the inventory.

**Table 2. The grouping inventory.**

| Family | Groupings | Groups | Basis |
|---|---|---|---|
| Geography | 3 | 16 | World Bank region, continent, World Bank income group |
| Income | 4 | 14 | 1990 log income, 2–5 cuts |
| Demography | 9 | 33 | 1990 birth rate (2–5), child mortality (2–4), life expectancy (3), transition timing (3–4 bins) |
| Schooling | 6 | 23 | 1990 secondary (2–5), lower-secondary (2–4) |
| Economy | 10 | 24 | farm output (2–4), urban share (2–4), farm employment (3), electricity (3) |
| Institutions | 3 | 9 | 1990 tax share, 2–4 cuts |
| k-means | 5 | 20 | 2–6 clusters on a 1990 six-measure profile |
| Grouped fixed effects | 10 | 40 | 2–6 classes on birth-rate and on log-income trajectories |
| **Total** | **50** | **179** | |

---

## 5. Results

### 5.1 The whole-sample reference

Estimated on all 217 countries, 127 of the 272 links are significant at 5% with country effects, 43 with country trends, and 26 in both specifications with the same sign. (The project's earlier full-matrix run reported 127, 42, and 24; the small differences come from partialling out the country trend once per country rather than with dummy columns.) These 43 country-trend links are the "pooled claims" that the multiverse interrogates. The earlier matrix's list of 24 links that survived both specifications is the project's `base_survivors.txt`, and it is the reference list against which the multiverse verdicts are compared.

### 5.2 Overview of verdicts

Table 3 gives the verdict counts in the 74-draw and 400-draw runs.

**Table 3. Verdict counts, 74-draw and 400-draw runs (272 links).**

| Verdict | 74 draws | 400 draws |
|---|---|---|
| Robust everywhere | 5 | 5 |
| Group-specific | 81 | 76 |
| Beats random, no clear group | 27 | 30 |
| No better than random | 159 | 161 |

The headline counts are close but not identical. The 74-draw run used a normal approximation to only 74 draws; the 400-draw run uses the empirical distribution. Under the smoothed (normal-fit) tier, 46 links beat random groupings with trends at 400 draws, against 43 at 74 draws: 42 of the old 43 survive, one dies (farm employment to gender parity in tertiary education), and four are new (wage employment to child mortality, secondary completion to wage employment, female labour participation to secondary completion, and birth rate to life expectancy). Twenty links do worse than random groupings (was 21), 32 show excess sign-flipping (was 36), and the same five links are robust everywhere.

The more important change is inferential rather than substantive. At 400 draws the strict empirical tier certifies 35 links going up, 19 going down, 15 sign-flip links, and 53 heterogeneity links. This is possible not because a lone link can be certified — it cannot — but because 30 links sit exactly on the 400-draw floor and the Benjamini–Hochberg step-up rule rejects the cluster. Section 6 explains the arithmetic. The practical reading is that the substantive conclusions are stable and that the certification language has to be attached to the cluster, not to individual links.

### 5.3 The five links that travel

Five links pass the robust-everywhere rule at both 74 and 400 draws. Table 4 reports their whole-sample statistics and their multiverse behaviour.

**Table 4. The five robust-everywhere links (74-draw and 400-draw runs).**

| Link | Whole-sample t (FE / TR) | Share of real groups significant (TR) | Random median share (TR) | Family minimum (TR) | Class |
|---|---|---|---|---|---|
| Under-5 mortality → fertility | +13.6 / +5.4 | 0.95 | 0.93 | 0.85 | robust |
| Life expectancy → fertility | −7.4 / −6.1 | 0.81 | 0.93 | 0.58 | robust |
| Under-5 mortality → life expectancy | −4.1 / −3.0 | 0.63 | 0.49 | 0.44 | robust |
| Farm output → log income | −3.1 / −2.6 | 0.53 | 0.37 | 0.51 | robust |
| Log income → urbanisation | +2.0 / +4.0 | 0.52 | 0.49 | 0.25 | robust |

Source: `results/edge_table.csv` (74-draw run), columns `pooled_FE_t`, `pooled_TR_t`, `share_TR`, `null_TR`, `fam_min_TR`; `results/edge_table400.csv` for the replication. The fertility figures at 400 draws are 95% versus a random median of 93% for child mortality, and 81% versus 93% for life expectancy; the binomial 95% half-width of a share near these values is about 2.5 to 4.9 percentage points with 400 draws, so the real and random shares are statistically indistinguishable. That is the intended reading of "robust everywhere": a uniform effect is seen by random slices too.

The five are exactly the links the substantive literature would expect to be structural rather than policy-contingent: the mortality–fertility and life-expectancy–fertility relationships are features of the demographic transition; child mortality and life expectancy move together; farm output falls as income rises; and income and urbanisation rise together. None of them is a claim about a policy lever, and none is presented as causal.

### 5.4 Group-specific links

Seventy-six links are group-specific at 400 draws (81 at 74 draws), meaning that a named country type explains where the link is concentrated. Five of the project's 24 earlier survivors fall here, and the group-specific labels are the least certain verdicts in the paper: they combine a smoothed-null test across roughly 16,600 tag-by-link comparisons with thresholds on the share of groups significant, and at 400 draws a single tag claim cannot be certified strictly under the same floor arithmetic that applies to links. The labels are therefore best read as *descriptions of where a link is concentrated*, not as certified claims. Single-region and single-class results are the weakest evidence in the run.

Two examples illustrate the type. Birth rate leading to later income (negative) is concentrated in the lowest-birth-rate trajectory class — the countries whose birth rate fell earliest and furthest — although in the earlier pooled matrix it looked general. Primary completion leading to gender parity in secondary is concentrated in the high-birth-rate groups and the high-birth-rate trajectory classes. Both are the kind of result that a pooled coefficient hides: the pooled number is an average over types, and the multiverse says which type carries it.

### 5.5 Links that are no better than random

One hundred and sixty-one links (159 at 74 draws) are no better than random. This is the largest category and the most important one for the paper's argument. It includes several of the project's earlier survivors: birth rate to lower-secondary completion, birth rate to electricity, birth rate to primary completion, urbanisation to secondary completion, and income to secondary completion. These are real in the pooled matrix but patchy across slices — their significance is not a property that survives a change of country typology. None of the old no-better-than-random links is above the 400-draw ceiling, so the large null remainder is not a power artefact: at this resolution those links really are indistinguishable from random groupings.

The honest summary of the whole table is "a small set of strong links and a large null remainder". That is not a disappointing result; it is the measurement of the phenomenon Durlauf described. The contribution is that the size of the robust set, the identity of the group-specific links, and the size of the null remainder are now quantities rather than assertions.

### 5.6 (1) Fertility

The fertility application asks which of the 32 links involving the birth rate survive the multiverse. The results divide cleanly.

**Robust everywhere (2).** Child mortality leading to the birth rate, and life expectancy leading to the birth rate, are significant in 95% and 81% of real groups with trends, against random medians of 93% and 93%; both pass the family-minimum condition (0.85 and 0.58) and neither flips sign more than random groups. These are the only two fertility links that hold in nearly every kind of country.

**Group-specific (13).** The clearest cases: birth rate leading to later income (negative) is concentrated in the lowest-birth-rate trajectory class; birth rate leading to secondary completion is concentrated in the high-birth-rate clusters; more urbanisation leading to fewer births holds in the low-birth-rate groups (the late stage of the transition) rather than early; and birth rate leading to farm output and to farm jobs is strong in the low-birth-rate, high-electricity, high-income groups — that is, where falling births coincide with a shrinking farm sector. Birth rate leading to life expectancy holds only among early crossers and low-birth-rate countries. Primary completion leading to births changes sign across types: negative in the early and low-birth-rate groups, positive in the highest-income trajectory class. Higher education leading to births and farm output leading to births beat random groupings without a named group.

**Beats random without a clear group (3).** Higher education to births, secondary completion to births, and farm output to births are more common in real than random groupings but are not concentrated in a named type.

**No better than random (14).** Birth rate to lower-secondary completion, to secondary completion (which moved down from group-specific in the 74-draw normal approximation), to electricity, to primary completion, to female labour participation, to tax share, and to urbanisation; wage employment to births; income to births; farm employment to births; female labour participation to births; primary-school gender parity to births; birth rate to child mortality; and birth rate to wage employment. These are real in the pooled matrix but weak and patchy across slices.

**Falsifiers.** The two robust fertility links survive the split-halves test and the t-fit version of the yardstick. The new and changed fertility verdicts — particularly the move of secondary completion to births from group-specific to beats-random-no-clear-group — are the most fragile claims in this application, because they depend on the normal fit of the yardstick; the 400-draw empirical tier does not certify them individually.

### 5.7 (2) Massification

The massification application asks which drivers of schooling expansion hold across country types. The answer is that nothing is robust everywhere. Of the 90 links with a schooling outcome on the left-hand side, none passes the robust-everywhere rule at either draw count.

**No robust driver.** The candidate drivers are electricity, wage employment, farm change, urbanisation, and income. Each fails in a different way.

**Electricity.** With country effects alone, electricity is large and positive for lower-secondary, secondary, primary, and gender-parity outcomes (t of about 3.6 to 6.0). With country trends, it is zero in the whole sample and in most groups: significant in 6% to 36% of groups depending on the outcome, against 3% to 28% in random groups. Where it holds, it is specific — lower-secondary completion in the lowest-birth-rate trajectory class — and it has the most sign-flipping of any driver: 11 of its 32 links show more sign-flipping than random groupings, with the sign reversing in high-income and high-trajectory classes for the income, urbanisation, tax, and child-mortality links. Electricity is therefore a weak, group-dependent driver once country trends are allowed, and the earlier note's verdict ("real with country effects, not separable from a country trend") is sharpened rather than overturned.

**Paid employment.** No wage-employment link to a schooling outcome beats random groupings in any kind of group. The shares are essentially identical to the random benchmark (for example, wage employment to lower-secondary completion: 9% of real groups versus 16% random; to secondary completion: 6% versus 3%; to tertiary completion: 21% versus 21%). This is the clearest null in the run, and it is a null that survives a power check: the random benchmark is estimated from 400 draws, and the real groups are not above it.

**Farm change.** Farm output leading to higher education is group-specific (it beats random in the 74-draw normal approximation but is classified as concentrated in the low-birth-rate and low-child-mortality groups at 400 draws); farm output leading to lower-secondary completion holds weakly; farm output to primary completion beats random groupings. Farm employment to gender parity in tertiary education loses its beats-random status at 400 draws. Urbanisation and income leading to secondary completion — both earlier survivors — are still no better than random: significant in the whole sample with trends but patchy in slices.

### 5.8 Sign flipping

Sign flipping is the multiverse's direct measure of "the pooled coefficient is an average of effects that disagree". Thirty-six links show more sign-flipping than random groupings at 74 draws (32 at 400 draws). The phenomenon is overwhelmingly concentrated in electricity: electricity to income, to urbanisation, to tax share, to child mortality, to life expectancy, and to several schooling outcomes flips sign across income and trajectory groupings, with the high-income classes reversing. The largest excess is electricity to log income, where 60% of GFE classes and 75% of income groups flip sign, against about 1% in random groups. In substantive terms: in poor countries electrification accompanies growth, in rich countries the association can run the other way, and the pooled coefficient is an average of those two regimes. This is the clearest single illustration of why the pooled number is not a description of "the world".

### 5.9 Split-halves stability

The split-halves test is the paper's main internal falsifier. The 400 draws are split into two disjoint halves of 200, the null distribution is re-estimated in each half, and the verdicts are recomputed. At 200 draws the floor is 1/201 = 0.0050. The results: the two halves' p-values rank-correlate at 0.994; their random-share means correlate at 0.9998 with a maximum difference of 0.76 percentage points; the smoothed-null significant set is 42 links in both halves (43 in one, 49 in the other, 8 disagreements, overlap 84%); the full-400 significance agrees with a half in 267 and 269 of 272 links; and the ceiling counts agree in 30 links (8 disagreements). The verdicts are stable at the link level. At 74 draws the same test had shown the yardstick was *not* stable — the 74-draw random-share means differ from the 400-draw means by up to 0.89 percentage points, and its p-values depended on the normal approximation — which is why the 400-draw run was necessary. The halves result is the empirical warrant for saying that 400 draws is enough for the descriptive and smoothed tiers, even though it is not enough to certify a lone link.

---

## 6. The resolution analysis

### 6.1 The empirical p-value floor

Suppose a link's real-grouping share is compared with R random re-partitions. The strongest statement the data can support is that the real grouping beat every random draw. The honest empirical p-value for that event is 1/(R+1), not zero: a p-value of zero would claim infinite evidence from a finite simulation (Phipson & Smyth, 2010; North, Curtis, & Sham, 2002; Hope, 1968). At 74 draws the floor is 1/75 = 0.0133; at 400 draws it is 1/401 = 0.00249; at 5,440 draws it would be about 0.00018. The floor is a property of the compute budget, not of the data.

### 6.2 What Benjamini–Hochberg requires

At a 5% false discovery rate over M = 272 links, the k-th smallest p-value is compared with k × 0.05/272. For k = 1 the threshold is 0.05/272 = 0.00018. A lone link therefore needs an empirical p at or below 0.00018, which requires R + 1 ≥ 272/0.05 = 5,440, i.e. about 5,440 draws. If one corrects within each specification separately (136 links per specification), the requirement is 2,720 draws. These are the numbers that make the 400-draw run's limits explicit: 400 draws is 13.6 times too coarse for a lone link (0.00249 against 0.00018).

### 6.3 Why 400 draws nevertheless certifies a cluster

Benjamini–Hochberg is a step-up rule, not a Bonferroni rule. When many links pile up exactly on the floor, the k-th smallest p-value at rank k is compared with k × 0.05/272, and for modest k the line rises above the floor. With j links at the floor, certification requires R + 1 ≥ 272/(0.05·j). The arithmetic: 1 link needs 5,440 draws; 5 need 1,088; 10 need 544; 14 need 389; 20 need 272; 30 need 182; 35 need 156. At 400 draws, 30 links sit at the floor, the largest passing rank is 35 (p at that rank = 0.00499, threshold 0.00643), and the strict tier certifies 35 up links, 19 down links, 15 sign-flip links, and 53 heterogeneity links. A separate implementation (statsmodels `multipletests`, `fdr_bh`) returns the same counts. The general lesson is that **the practical bar to certification is not one number**: a lone finding needs thousands of draws, a cluster of extreme findings needs hundreds.

Two caveats are part of the result, not a footnote. First, the 400 draws are shared by all links, so the p-values are dependent; empirically the dependence is neither absent nor uniformly positive, so BH's PRDS assumption is not established and the arithmetic of this section is a design rule rather than a calibrated test. Section 6.6 quantifies this (mean absolute correlation 0.041; effective tests about 157), recomputes the certified count under an effective-tests correction (44 rather than 35), and reports a dependence-aware permutation null for the cluster count (zero in 400 pseudo-runs). Second, the links in the floor cluster are the extreme links; a certified cluster is not a certified set of individually transportable claims. The tier language in Section 6.5 is designed to keep that distinction visible.

### 6.4 Uncertainty of the yardstick itself

A share estimated from 400 draws has binomial standard error √(0.25/400) = 2.5 percentage points near 50%, so a 95% interval of about ±4.9 points, and about ±2.9 points near 90%; the median binomial standard error across links is 1.4 points. For the hard ceiling, zero of 400 above the real value implies a true chance below about 3/400 = 0.75% at 95%. These intervals are the uncertainty in the *yardstick*, not in the substantive estimate; they are reported so that a reader does not treat a one-draw difference as a finding. The split-halves test in Section 5.9 shows the practical consequence: the verdicts are stable, the borderline p-values are not.

### 6.5 The three reporting tiers

The paper reports three tiers, and every claim in Section 5 is labelled with the tier that supports it.

**Table 5. The three tiers (trends specification, 272 links).**

| Tier | Test | What it can say | Result at 400 draws |
|---|---|---|---|
| 1. Strict | empirical p from the 400 draws, BH 5% | a lone link is unresolvable; a floor cluster is certifiable | 35 up certified (30 at the floor), 19 down, 15 sign-flips, 53 heterogeneity |
| 2. Main | normal fit to the 400-draw yardstick, BH 5% | re-tests the old claims with a better-estimated yardstick | 46 up (old 43: 42 survive, 1 dies, 4 new), 20 worse, 32 flips, 5 robust |
| 3. Descriptive | real above all 400 draws | the strongest descriptive statement at this budget | 30 up, 19 down, 15 flips (expected by chance 0.68; Poisson p ≈ 2 × 10⁻³⁸) |

The tiers are not interchangeable. A strict-tier claim is a claim about the cluster; a main-tier claim is a claim conditional on a parametric fit to the yardstick; a descriptive claim is a ranking. The paper's substantive conclusions — five robust links, nothing robust in massification, paid employment as a clean null — are main-tier and descriptive claims. The strict tier adds that the extreme cluster is real but does not license individual certification.

### 6.6 Dependence, effective tests, and what the rule is

The arithmetic in Sections 6.2-6.3 carries an assumption that must be stated rather than buried: the Benjamini–Hochberg guarantee used here requires the 272 tests to be independent or to satisfy positive regression dependence (PRDS; Benjamini & Yekutieli, 2001). The 272 null-share series are **not independent** — they are computed from the same 400 random partitions, so every link's yardstick is correlated with the others'. Using the committed matrix of family-balanced random shares (`null_shares_TR.csv.gz`, 400 draws × 272 links), the mean absolute off-diagonal correlation between link-specific null-share series is **0.041**, with 51% of pairs positive and 49% negative and a maximum absolute correlation of **0.44** (`results/dependence_analysis.json`). Dependence is therefore present and is **not uniformly positive**, so the PRDS condition is not established empirically. This is a real objection: the step-up certification of Section 6.3 is a design arithmetic, not a calibrated test.

Three things follow. First, the effective number of independent tests is smaller than 272. The Li–Ji (2005) eigenvalue formula applied to the correlation matrix gives **M_eff ≈ 157** (162 principal components are needed for 90% of the variance), about 58% of the nominal count. Second, certification can be recomputed under the effective count. At M_eff = 157 the strict tier certifies **44** links rather than 35; a sensitivity grid over the assumed number of tests gives 35 at M = 272, 44 at M = 157, 46 at M = 150, 52 at M = 100 and 60 at M = 50. The floor-cluster certification is robust in every case — it never falls below the baseline — but the count moves by up to 25 links, so the honest statement is a bound, not a point. Third, the draw budget scales with the effective count: a lone link needs about **3,140** draws at M_eff = 157 rather than 5,440 at M = 272, and a cluster of 30 needs about **105** rather than 182. We report the nominal numbers in Sections 6.2-6.3 and the effective-tests sensitivity here; neither is "the true" number, because the dependence structure is itself estimated.

The joint count can also be tested without assuming independence at all. Treat each of the 400 random draws as pseudo-real — a draw in which, by construction, there is no real grouping — compare it with the other 399 draws, and apply the same BH step-up. In all 400 pseudo-runs the number of certified links is **zero** (permutation null: mean 0, maximum 0; `results/dependence_analysis.json`). The observed 35 certified links therefore sits far above a dependence-aware null for the count; by the rule of three, zero events in 400 pseudo-runs bound the chance of such a cluster at about **0.75%** at 95%. This does not rescue the individual p-values — they remain uncalibrated — but it does show that the cluster is not an artefact of the shared-draw dependence.

What the paper claims, then, is narrower than "a new method" and should be read that way: **a pre-specified draw budget and a certification-ceiling rule, conditional on independence or positive dependence, with an effective-tests sensitivity bound and a dependence-aware permutation null for the count.** The closest prior work is the inference machinery for specification curves (Simonsohn, Simmons, & Nelson, 2020), the vibration-of-effects framework (Patel, Burford, & Ioannidis, 2015) and its extension to sampling uncertainty (Klau, Hoffmann, Patel, Ioannidis, & Boulesteix, 2021). All three treat the joint distribution of many specifications or samples; none of them derives the Monte Carlo-floor/cluster interaction used here. The same caveat applies, more strongly, to larger partition batteries built the same way — the project's 13,800-partition, 342-link correlation battery shares draws across partitions in exactly this way — and any such battery needs its own dependence check before its certification counts are read as calibrated.

### 6.7 What would change our minds, and how to run this at full resolution

Four things would change the paper's conclusions. First, a replication on a larger draw budget (about 5,440 under the nominal count, about 3,140 under the effective-tests count) would convert the main-tier claims into strict individual certifications; the paper predicts that the five robust links will certify and that most of the group-specific labels will not, because the tag-level tests have the same floor problem. Second, a different estimator — one with an identified causal effect, such as a schooling reform or a mortality shock — could be run through the same multiverse; if the effect is heterogeneous in the same way, the transportability verdicts should replicate, and if they do not, the pooled association was doing the work. Third, a replication on the project's imputed panel would test whether the coverage choices drive the null remainder. Fourth, a pre-registered set of groupings (rather than the 50 chosen here) would test whether the multiverse itself is a garden of forking paths; the 50 were chosen before the results were seen and are documented in the repository, which is the practical safeguard, but a pre-registration would be stronger.

The compute arithmetic for full resolution is straightforward. One draw is a full pass over 179 groups and 544 specifications, about 95,000 regressions. The 400-draw run took 3,711 seconds (62 minutes) on 16 worker processes under an 8-core container quota, about 9.2 seconds per draw, for 38,420,908 regressions in total. A 5,440-draw replication at the same rate is about 14 hours on the same allocation (about 8 hours at the effective-tests budget of roughly 3,140 draws). That is feasible on a single machine over a weekend, and it is the honest number to quote to a reader who wants individual certification. It also motivates the GPU route discussed below.

### 6.8 A known-truth simulation, and the case for GPU acceleration

The resolution analysis says how many draws are needed; it does not say what the verdicts would be if the truth were known. A *known-truth simulation* closes that gap, and it is the natural next step for this project. Simulate a panel from a data-generating process with three regimes: a link that is uniform across all countries, a link planted only in one type of country, and no link at all. Run the identical grouping multiverse on the simulated panel and check whether the verdict taxonomy recovers the planted truth, at 74, 400, and 5,440 draws. That yields the type-I error and power of each verdict — the missing piece of a pure resolution calculus, which is about the yardstick rather than about the verdicts.

The project's simulation work makes this unusually cheap to do. The executable models on the simulation branch can generate synthetic country panels with known heterogeneity, and the grouping multiverse can be applied to their output as a recovery test: if a model implies that a driver should matter only in one type of country, the multiverse should say so. Two cautions apply. A simulation can only validate recovery under the simulated data-generating process, so it inherits that process's assumptions; and calibration on one's own model risks circularity, because a model and its validation can share code and assumptions. The safeguard is to freeze the simulation design before looking at the multiverse results, and to report the recovery rates as a property of the design rather than as evidence for the substantive claims.

The compute argument for GPU acceleration is direct. The estimator's expensive part is a large number of small regressions on a common panel; the country-level terms are removed once per link and the per-group fits are small matrix operations. That structure is friendly to a batched GPU implementation, and a CUDA kernel for the grouped fits would turn the 5,440-draw requirement from a 14-hour job into a minutes-to-hours job, making full-resolution certification routine. The project is developing such a kernel on a parallel branch; the present paper does not depend on it, and the numbers here were produced on CPU. The point for this paper is that the resolution limit is a compute limit, and compute limits are the kind of limit that can be engineered down.

---

## 7. Relation to prior work

The paper borrows heavily and claims narrowly. Table 6 states the relation point by point.

**Table 6. Relation to prior work.**

| Prior work | What it does | What this paper borrows | What this paper adds |
|---|---|---|---|
| Steegen et al. (2016), multiverse analysis | enumerates analytic choices and reports the distribution of results | the multiverse logic and the norm of reporting the whole distribution | the multiverse dimension is the *partition of countries*, not the analyst's choices |
| Simonsohn et al. (2020), specification curve | orders specifications and conducts inference over the curve | the visual and inferential object; the insistence on joint inference | a curve over country typologies, calibrated against random typologies |
| Simmons et al. (2011); Gelman & Loken (2014); Wicherts et al. (2016) | researcher degrees of freedom and the garden of forking paths | the diagnosis and the reporting norms | a design that makes the relevant degrees of freedom (groupings) explicit and enumerable |
| Young & Holsteen (2017); Muñoz & Young (2018) | computational multimodel analysis and multiplicity correction | the computational framework and the multiplicity discipline | the null is a random *partition*, not a random *specification* |
| Leamer (1983); Sala-i-Martin (1997) | robustness to model uncertainty | the sceptical tradition | the question is heterogeneity across countries, not uncertainty across models |
| Brock & Durlauf (2001); Durlauf et al. (2005) | the heterogeneity critique of cross-country growth empirics | the framing and the objection | the heterogeneity is measured: shares, sign-flip rates, and group-specific verdicts |
| Bonhomme & Manresa (2015) | grouped fixed effects: estimate the groups | grouped FE as one family of groupings and as a benchmark | substantive typologies are added to estimated ones, and all are calibrated against random partitions |
| Hope (1968); Ernst (2004); Phipson & Smyth (2010) | Monte Carlo and permutation tests; finite-resolution p-values | the p floor of 1/(R+1) | the floor is combined with BH to derive the draws needed for certification |
| Benjamini & Hochberg (1995) | false discovery rate control | the correction | the step-up interaction with a floor cluster is made explicit |
| Lipsitch et al. (2010) | negative controls | the interpretation of the random-grouping null | the negative control is a random partition of the population |
| Pearl & Bareinboim (2014); Bareinboim & Pearl (2016) | transportability | the target-population framing | transportability is tested with associations and calibrated against random partitions |
| Hotz et al. (2005); Tipton (2013) | generalisation of experimental effects across sites | the empirical generalisation question | no identified effect; the method is a diagnostic, not a transport formula |
| Bertrand et al. (2004); Cameron et al. (2008); Cameron & Miller (2015); Abadie et al. (2023) | cluster-robust inference and small-cluster problems | the clustering discipline and the small-group warning | the warning is built into the verdict rules (recurrence across families, no single-group claims) |

**What we do not claim.** We do not claim to have invented multiverse analysis, specification curves, grouped fixed effects, permutation tests, false-discovery control, transportability, or the heterogeneity critique. We do not claim causal identification. We do not claim that the 50 groupings exhaust the space of country typologies. We do not claim that the random-grouping null is assumption-free: it inherits the estimator's assumptions, including the functional form, the control set, and the clustering. And we do not claim that "no better than random" means "no effect"; it means "no effect detectable at this resolution under this estimator". The claim of novelty is narrow: we are not aware of a multiverse over country partitions calibrated against random partitions of identical size, with a formal resolution analysis of how many draws certification requires. That analysis is a design rule conditional on independence or positive dependence; Section 6.6 reports the effective-tests sensitivity and the dependence-aware null, and the paper does not present the rule as a calibrated test.

---

## 8. Discussion

### 8.1 Answering Durlauf with a measurement

Durlauf's objection is that the pooled coefficient may be an average no country has. The grouping multiverse turns that objection into three measurable quantities. The *share of real groups* in which a link holds tells us how widespread the association is. The *sign-flip rate* tells us how much of the pooled coefficient is an average of effects that disagree in direction. The *group-specific labels* tell us which types carry the association when it does not travel. The fertility and massification results are exactly the pattern the critique predicts: a small set of demographic links travel, and the policy-adjacent massification drivers do not. The paper's contribution is not that the critique is wrong; it is that the critique's central claim — the coefficient is a mixture — can be estimated rather than merely asserted. That is also the answer to the sceptical question "does this kind of cross-country work work at all?" The honest answer is: sometimes, and the multiverse says when.

### 8.2 Typologies, not regions

The design deliberately includes theory-motivated country types — fertility-transition timing, schooling stocks, farm structure, fiscal capacity — alongside the familiar geographic and income cuts. The results justify the choice: many of the group-specific findings are not regional. Birth rate to income is concentrated in the low-birth-rate trajectory class, not in a continent; primary completion to gender parity is concentrated in high-birth-rate groups; electricity's sign reversal follows income and trajectory classes. A method that only cut by region would miss these. The practical implication for comparative research is that "region" is a convenient but weak typology, and that substantive typologies should be part of the multiverse by default.

### 8.3 A method for researchers without proprietary microdata

The grouping multiverse is designed for a particular research situation: the analyst has the standard cross-country macro panels — the ones that are generally available — but not proprietary in-country survey or administrative microdata. In that situation, the choice is not between a credible research design and a pooled regression; it is between a pooled regression presented as a description of the world and a pooled regression presented with an honest account of how much of it survives a change of country typology. The multiverse requires no new data, no experimental variation, and no privileged access; it requires the panel, the groupings, and compute. That is its niche, and the two applications show what it buys: a defensible claim that the demographic links travel, and a defensible null on the policy-adjacent drivers.

### 8.4 What the results mean substantively

For fertility, the two robust links are the demographic-transition relationships, and their robustness is reassuring rather than surprising: they are the links least likely to be confounded by policy or institutions. The thirteen group-specific fertility links are the interesting ones, because they locate the transition's mechanisms in types: the late-stage urbanisation effect, the low-birth-rate farm-sector effect, and the sign reversal in primary completion. For massification, the results are a warning. Electricity, the most policy-salient driver in the project's original matrix, is strong only with country effects and vanishes with country trends, and its associations flip sign across income and trajectory classes. Paid employment is a clean null. Farm change is group-specific and concentrated. If a comparative-education claim about massification is to be made, the multiverse says it must be a claim about types, not about the world.

### 8.5 What the method cannot do

The method cannot establish causality, cannot rule out confounding, cannot fix measurement error in crude country-level indicators, and cannot make a small group of countries into a large sample. It cannot certify a lone link at 400 draws, and it cannot tell a transportable association from a confounded one that happens to be homogeneous. These are not implementation gaps; they are the boundaries of a diagnostic that takes the pooled association as its input. The paper's tier language exists to keep those boundaries visible.

---

## 9. Limitations

1. **Clustered errors are optimistic in small groups.** Groups of 10 to 30 countries make cluster-robust standard errors unreliable, so single-group claims are the weakest evidence in the design. The verdict rules partially mitigate this by requiring recurrence across families and nesting cuts, but they do not eliminate it.
2. **No causal identification.** The estimator is a within-country lead-lag association. Nothing here identifies a causal effect, and the multiverse cannot adjudicate confounding. The transportability verdicts are verdicts about associations.
3. **Crude country-level measures.** Attainment shares, electricity access, and farm shares are coarse indicators with known measurement problems; ten-year changes are sensitive to revisions. Differences across groupings may reflect measurement heterogeneity as well as substantive heterogeneity.
4. **The random null inherits the estimator's assumptions.** The null is computed with the same estimator, controls, functional form, and clustering as the real pass. If the estimator is misspecified, the null is misspecified in the same way, and the comparison may be too generous or too conservative in ways the design cannot detect.
5. **The resolution limit.** At 400 draws a lone link cannot be certified and a tag-level claim cannot be certified at all; the strict tier's 35 certifications are cluster-level, not individual. The 5,440-draw requirement is a real constraint, not a rhetorical one.
6. **The resolution rule is not a calibrated test.** The 272 tests share draws and are neither independent nor uniformly positively dependent (mean absolute correlation 0.041; effective tests about 157). The BH step-up arithmetic is therefore a design rule conditional on independence or positive dependence; the effective-tests correction (44 certified rather than 35) and the dependence-aware permutation null (zero in 400 pseudo-runs) bound the uncertainty but do not remove it.
7. **The compute constraint.** The 400-draw run took 62 minutes on 16 workers under an 8-core quota; the full-resolution run is about 14 hours. A replication on different hardware will have different timing, and a much larger draw budget may need the GPU implementation.
8. **The groupings are chosen, not exhaustive.** Fifty groupings in eight families are a large but selected set. The multiverse can itself become a garden of forking paths if the groupings are chosen after seeing results; the repository documents that these 50 were specified before the run, but a pre-registration would be stronger.
9. **Single-country and single-region claims are the weakest.** A group-specific verdict that rests on one region or one class should be treated as a hypothesis, not a finding.
10. **The observed panel is unbalanced.** No imputation was used for the main results, so coverage varies by measure and period, and links estimated on different subsets are not strictly comparable.

---

## 10. Reproducibility

Everything reported here is reproducible from the repository. The 74-draw run is in `research/records/2026-11-23-grouping-multiverse/` and the 400-draw run in `research/records/2026-11-23-grouping-multiverse-400/`; each contains its scripts, results, and a README with the exact commands.

- **Scripts.** `gm_core.py` (panel, groupings, estimator), `run_multiverse.py` (real and random passes), `analyse.py` (verdicts, 74-draw), and the corresponding `run_multiverse400.py`, `analyse400.py`, and `determinism_check.py` for the 400-draw run.
- **Seeds.** Random partitions use seeds 1000 + r for r = 1..400, so the 400-draw run contains the 74-draw run bit-for-bit. The grouping construction uses fixed seeds for k-means (1) and grouped fixed effects (2).
- **Commands.** The 400-draw run was launched as `python run_multiverse400.py 400 16 out/final400.pkl`, followed by `python analyse400.py out/final400.pkl results/`. The determinism check is `python determinism_check.py`.
- **Runtime.** 3,711 seconds (62 minutes) for 400 draws on 16 workers under an 8-core container quota, 38,420,908 regressions, mean 146.5 seconds of worker time per draw, 9.2 seconds of wall time per draw. The 74-draw run took longer per draw because it shared the server; its total was 7,185,790 regressions.
- **Determinism.** Replicates 7, 250, and 400, and the real-grouping pass, were recomputed from scratch in a fresh process: all outputs bit-identical (max difference 0, zero flip mismatches). The 74 overlapping draws reproduce the 74-draw run exactly (max difference 0 in the statistics and heterogeneity tests), so every difference between the runs is a better-estimated yardstick, not code drift.
- **What a reader needs.** The panel (22 series plus metadata, on the project server), the scripts above, a Python environment with numpy, scipy, and statsmodels, and about 62 minutes on 16 workers for the 400-draw run. The raw 214 MB replicate file is not committed; it regenerates in about 62 minutes.
- **Numbers.** Every number in this paper is traceable to a named file: `results/edge_table.csv` and `results/summary.txt` for the 74-draw run; `results/edge_table400.csv`, `results/summary400.txt`, `results/headline.json`, `results/halves.csv`, `results/determinism.txt`, and `results/run400.log` for the 400-draw run. The README in each record directory maps the claims to the files.

---

## 11. Target venues and what each would require

- **Sociological Methods & Research.** The best fit for the methods contribution: the multiverse framing, the calibration device, and the resolution analysis are squarely in the journal's scope, and the journal has published the adjacent work (Young & Holsteen, 2017; Hedström & Manzo, 2015). Would require: a fuller treatment of the estimator's statistical properties, a simulation study of the verdict rules' size and power, and a shorter empirical section.
- **Journal of Development Studies.** The Durlauf framing and the two applications fit the development audience. Would require: a stronger substantive literature review, a defence of the country-level measures against the measurement literature, and a policy-facing conclusion.
- **Comparative Education Review (methods note).** The massification application is the hook. Would require: a shorter paper (methods note format), more attention to the comparative-education literature on cross-national comparability, and a clearer statement of what the null on paid employment means for the field's claims.
- **Demography.** The fertility application is the hook. Would require: a proper review of the fertility-decline literature, demographic measurement expertise, and a sharper distinction between the mortality–fertility link and the policy-relevant drivers.
- **Political Analysis or Sociological Methodology.** If the paper is reframed as a general method for transportability testing, these venues would want the formal treatment of the null, the simulation-based size and power results, and the GPU implementation as a reproducibility asset.

---

## Appendix A. Definitions

- **Link.** An ordered pair of measures (x → y), estimated as the association between x at time t and the ten-year change in y.
- **Specification.** One of two estimator versions: with country fixed effects only (FE), or with a country-specific linear trend added (TR). Each link has two specifications; 272 links give 544 specifications.
- **Grouping.** A partition of the countries into named groups based on one typology (for example, 1990 income halves).
- **Family.** A set of groupings that share a typology (for example, income cuts at 2, 3, 4, and 5).
- **Nested cuts.** Groupings that are cuts of the same ordering at different depths, so that a country's group at one depth is consistent with its group at another.
- **Random re-partition.** A random partition with the same group sizes as a real grouping, preserving the nested-cuts rule.
- **Family-balanced share.** The average, across families, of the share of a family's groups in which a link is significant with the whole-sample sign. Each family counts once.
- **Sign-flip rate.** The share of groups in which a link is significant in both directions across the multiverse.
- **Heterogeneity rate.** The share of groupings in which the group-specific estimates are jointly heterogeneous at 5%.
- **Verdict.** One of four labels: robust everywhere, group-specific, beats random without a clear group, no better than random.
- **Floor.** The smallest attainable empirical p-value from R random draws, 1/(R+1).
- **Ceiling.** The set of links whose real-grouping statistic exceeds every random draw.
- **Tier.** The inferential standard used for a claim: strict (empirical p, BH), main (normal fit to the yardstick, BH), or descriptive (above the ceiling).

---

## Appendix B. The grouping inventory

| Family | Groupings (names) | Groups |
|---|---|---|
| Geography | World Bank region; continent; World Bank income group | 7 + 5 + 4 |
| Income | 1990 log income ×2, ×3, ×4, ×5 | 2 + 3 + 4 + 5 |
| Demography | 1990 birth rate ×2–×5; 1990 child mortality ×2–×4; 1990 life expectancy ×3; replacement-crossing ×3 and ×4 | 2+3+4+5 + 2+3+4 + 3 + 3+4 |
| Schooling | 1990 secondary ×2–×5; 1990 lower-secondary ×2–×4 | 2+3+4+5 + 2+3+4 |
| Economy | 1990 farm output ×2–×4; urban share ×2–×4; farm employment ×3; electricity ×3 | 2+3+4 + 2+3+4 + 3 + 3 |
| Institutions | 1990 tax share ×2–×4 | 2+3+4 |
| k-means | 2 to 6 clusters on a six-measure 1990 profile | 20 |
| Grouped fixed effects | 2–6 classes on the birth-rate trajectory; 2–6 classes on the log-income trajectory | 20 + 20 |
| **Total** | **50 groupings** | **179 groups** |

---

## Appendix C. Plain-language abstract and five-point summary

### Plain-language abstract

We take a common kind of research claim — that one thing drives another across countries, measured with a single number from a panel of countries — and stress-test it by cutting the countries into groups in many different ways: by region, by income, by birth rate, by schooling, by farm economy, by tax capacity, by data-driven clusters, and by statistical groupings that follow countries' own trajectories. We rerun the whole analysis inside every group and compare the results with what happens when we cut the countries up at random. Random cuts are the yardstick for what chance alone would produce. Two things follow. First, a claim that is the same everywhere looks the same in random cuts as in real cuts, so the method can tell "this travels" from "this only happens in certain kinds of country". Second, the number of random cuts limits how strong a statement we can make: with 400 random cuts we can vouch for a cluster of very strong findings but not for any one finding on its own, and a single finding would need about 5,440 random cuts to be certified. In the two applications, the demographic links between child mortality and fertility, and between life expectancy and fertility, travel across almost every kind of country; the policy-adjacent drivers of schooling expansion do not. Paid employment shows no link to schooling that beats random cuts — the clearest null in the study.

### Five-point plain-language summary

1. **The problem.** A single number from a cross-country panel is an average over countries that may not share the relationship at all, so the number can describe a world that no country actually lives in.
2. **The test.** Cut the countries into groups 50 different ways — geography, income, birth rate, schooling, farm economy, taxes, data-driven clusters, and trajectory-based classes — rerun the whole analysis in each group, and compare with the same exercise on random cuts of the same sizes.
3. **What the test can say.** It can separate claims that travel across country types from claims that only hold in certain types, and from claims that are no better than random slicing. It cannot say whether the underlying relationship is causal.
4. **What it found.** Two demographic links travel: lower child mortality and longer life expectancy both go with fewer births. None of the schooling-expansion drivers travel, and paid employment shows no link to schooling that beats random cutting.
5. **The limit.** The number of random cuts is a hard ceiling on how strong the evidence can be: 400 cuts can vouch for a cluster of very strong findings but not for a single one, and a lone finding would need about 5,440 cuts (or about 3,140 if the overlapping information in the 272 links is taken into account). The cluster result is a design rule with a stated dependence caveat, not a calibrated test.
