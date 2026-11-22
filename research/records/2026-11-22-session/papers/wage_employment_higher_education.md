<p align="center"><strong>Wage Employment and Higher Education: A Fragile Association</strong></p>

<p align="center"><em>A Specification-Curve and Falsification Analysis</em></p>

<p align="center">Dr. Trey Menefee</p>

<p align="center">Independent Researcher</p>

**Author Note**

This working paper was completed in November 2026. The author has no conflicts of interest to disclose, and no external funding supported this work. Country-level data are drawn from the World Bank World Development Indicators and the UNESCO Institute for Statistics for 183 countries over 1960–2024. Correspondence concerning this paper should be addressed to Dr. Trey Menefee, Independent Researcher.

<p align="center"><strong>Abstract</strong></p>

Does wage employment drive the expansion of higher education? Across 1,536 defensible specifications of the same cross-national panel—varying the measurement lag, the control set, the fixed effects, the sample restriction, and the outcome transform—the median coefficient is approximately zero, the 5–95% range runs from −0.040 to +1.371, and only 27.9% of specifications return a significant positive estimate. The association is strongest at short lags and on the level scale, and it disappears under a log transform. What this paper reports is therefore a fragile association, not an established effect. Two further exercises bound what can be said about it. A falsification test generates two simulated worlds on the real coverage mask (1,883 country-decades, 157 countries): a chain world returns a median of +2.201, a common-cause world returns +0.000 with a 5–95% range of −0.260 to +0.255, and none of 1,200 common-cause panels reaches the largest observed estimate of +1.425 (*SE* = 0.410). That establishes direction at one specification, not robustness across specifications. The reverse-direction estimate is +0.010 (0.042).

*Keywords:* wage employment, higher education, tertiary enrolment, specification curve, falsification, common cause, cross-national panel, researcher degrees of freedom

<p align="center"><strong>1. Introduction</strong></p>

The claim that wage employment drives the expansion of higher education is one of the more intuitive claims in the political economy of education, and it is one that a cross-national panel appears to support. Countries whose labour markets are organised around payrolls have large tertiary systems. Countries whose labour markets are not, do not. When the share of employment that consists of paid work rises, the tertiary enrolment ratio tends to rise with it. The association is easy to find and easy to report, and it has been reported.

This paper's first contribution is to show that the association, as an estimate, is fragile. The same panel, the same variables, and the same researchers' defensible choices about how to analyse them produce 1,536 specification-dependent answers whose median is approximately zero. The coefficient is positive in 73.7% of specifications but significant and positive in only 27.9%, and its magnitude is governed by two decisions that the literature rarely treats as substantive: how long a lag is allowed between cause and effect, and whether the outcome is measured in levels or in logs. At a ten-year lag the median coefficient is 0.00; at a fifteen-year lag it is +0.02; at five years +0.19; contemporaneously +0.39. On the level scale the median is +0.86; on the log scale it is 0.00. Adding any control beyond the country's own starting enrolment takes the median from +0.12 to +0.01.

The second contribution is to establish what kind of thing the association is, at the specification where it is strongest. Two accounts compete. On the chain account, wage employment expands when production is reorganised around enterprises that hire labour for money, that reorganisation raises the return to credentials and the household income that pays for them, and a decade later the tertiary system absorbs the demand. On the common-cause account, one modernising process—states that deliver services, firms that can hire, households that can plan—raises both the wage share and tertiary enrolment together, and the correlation between them is the correlation of two effects. Schofer and Meyer (2005) supply the institutional version of this second account: higher education spread worldwide because a university system became a standard component of what a modern country is supposed to contain, not because domestic labour markets were hiring. A third possibility reverses the arrow, with educated people taking wage jobs and countries with large tertiary systems therefore reporting more wage employment.

All three accounts fit the same facts, and the obvious remedy fails. Controlling for the common cause requires covariates—income, urbanisation, electrification, mortality—that are themselves consequences of the transformation under study, and that are severely collinear with the variable of interest: electricity access correlates with the wage-employment share at *r* = .80 and urbanisation at .74. The theoretical literature has already established that human capital, fertility, and structural change are jointly determined (Galor & Weil, 1996) and that the release of labour from agriculture is a slow, technology-driven process whose timing has little to do with schooling policy (Boppart et al., 2023). A regression that adds these variables does not identify a mechanism; it allocates one bundle of variation among its proxies.

The strategy here is therefore twofold, and the order matters. First, the full specification curve is estimated and reported, so that the fragility of the estimate is visible rather than inferred. Second, at the specification where the coefficient is largest, a falsification test is run: two simulated worlds are generated on the real coverage mask of the data—1,883 country-decades in 157 countries—and each is estimated 1,200 times with the estimator applied to the real data.

The results divide cleanly between the two exercises, and the division is the paper's finding. The specification curve says the association is not robust: most defensible analyses return zero, and the sign is the only stable feature. The falsification test says that where the association is largest, it is not an artefact of a symmetric common trend: the common-cause world produces a median of +0.000 with a 5–95% range of −0.260 to +0.255 and never reaches the observed +1.425 (*SE* = 0.410), while the chain world produces a median of +2.201 with a range of +1.543 to +2.885. The reverse-direction estimate is +0.010 (0.042), a precise zero.

The conclusion is not that wage employment matters, and it is not that it does not. It is that the evidence for a lead–lag relationship is real but fragile: directional where it can be tested, and dependent on analytic choices that theory does not settle. A field reporting only the +1.425 would report the top of a distribution whose median is zero; this paper reports the distribution.

<p align="center"><strong>2. The Identification Problem</strong></p>

## **2.1 What the Competing Accounts Require**

The chain account requires a direction and a lag. Wage employment expands when production is reorganised around enterprises that hire labour for money rather than households that deploy their own; that reorganisation raises the return to certified competencies and changes who can afford to acquire them, because a household with a payroll income can forgo a young adult's contribution to the family enterprise in a way a subsistence household cannot. A decade later the tertiary system absorbs the resulting demand. The lag is not incidental: credentials are acquired in anticipation of occupations, and occupational structures change slowly.

The common-cause account requires neither. One process raises the wage share and tertiary enrolment together, for the same reasons, and the correlation between them is the correlation between two effects—as two crops fail in the same drought without one causing the other. The reversal account requires the opposite arrow: educated people take wage jobs. All three accounts imply that the two variables move together, and all three are consistent with the same cross-section and the same time series. What separates them is the mechanism, which is what a cross-national regression is least equipped to see.

## **2.2 Why Controls Cannot Do the Work**

Modernisation is not observable. What is observable are its correlates, and each is both a cause and a consequence of schooling. Conditioning on them does not remove the latent factor; it conditions on endogenous proxies, removes part of the common variation, imports whatever independent effect each proxy carries, and leaves the coefficient of interest determined by relative measurement error. This is the familiar bad-control problem, and it bites harder here than most because the entire covariate set is downstream of the treatment. Collinearity compounds it: electricity, urbanisation, and the wage-employment share are near-interchangeable in this sample (*r* = .80, .74, and .69), so a specification containing all three estimates one bundle and distributes it across three labels. The theoretical objection is stronger still. Galor and Weil (1996) showed that human capital, the gender gap, fertility, and growth are jointly determined, which makes the search for a unidirectional effect between any pair of them ill-posed; Boppart et al. (2023) showed that labour is released into wage employment only after agricultural intensification raises output per worker, a process whose timing is set by technology and land rather than by schooling policy.

## **2.3 The Two Questions This Paper Can Answer**

Two questions are answerable and one is not. The first is descriptive and prior to any mechanism: how much does the estimated relationship depend on defensible analytic choices? That is answered by estimating the full specification curve rather than a preferred specification.

The second is conditional. At a given specification, could a world in which a single latent factor drives both variables—and no chain connects them—have produced the coefficient observed? This is answerable because such worlds can be constructed, and because the specification controls for the country's own tertiary enrolment at the start of each window along with country and decade fixed effects. That starting level summarises everything that has made the system what it is: history, institutions, income, urban structure, position in the world model of what a country contains. If a latent factor drives the level of tertiary enrolment, the starting level absorbs it, and what remains to be explained is the increment. Under a pure common cause the residual covariation between two increments net of that level carries no systematic sign. Under a chain it does: this decade's increment in wage employment causes the next decade's increment in enrolment, and nothing in the starting level can absorb that, because the causal input had not yet acted when the level was measured. A positive partial coefficient is the signature of lead–lag.

The question that is not answerable here is the counterfactual one—what would happen to a country's tertiary system if its wage-employment share were raised by policy. Nothing in this design identifies that, and Section 7 says so.

## **2.4 Falsification as a Design**

A hypothesis is not supported by consistency with the data; it is supported by inconsistency with its serious rival. The rival here is the common-cause account, which is more parsimonious and which the joint-determination literature says should be preferred until it fails. So the common-cause world is given every advantage: not a straw man in which the two variables are independent, but a world in which a single persistent latent factor drives both, in levels and in increments, estimated on the real coverage mask with the real specification. The chain world is built to the same standard and exists to establish that the estimator can recover a chain when one is present.

What this design establishes is direction at a specification, not robustness across specifications: the test was run where the coefficient is largest, which is the honest place to run it, but a test run at the maximum of a distribution cannot testify about the rest of it.

<p align="center"><strong>3. Method</strong></p>

## **3.1 Data and Coverage**

The sample covers 183 countries over 1960–2024. The World Bank's World Development Indicators supply the wage-employment share—the proportion of total employment accounted for by wage and salaried workers—together with urban population share, access to electricity, GDP per capita, life expectancy, the under-five mortality rate, and female labour force participation. The UNESCO Institute for Statistics supplies the tertiary gross enrolment ratio and the primary, lower-secondary, and upper-secondary completion rates. Variables are observed at decade intervals; each observation is a country-decade, and each records the change in each variable across its window together with the level of tertiary enrolment at the window's start. Coverage differs by variable and period, so the panel is unbalanced, and the falsification exercise runs on a common mask defined by joint availability of the wage-employment share, the tertiary ratio, and the lagged tertiary level: 1,883 country-decade observations across 157 of the 183 countries.

Two measurement features constrain interpretation throughout. The gross enrolment ratio is a flow over a stock—it counts tertiary students, including foreign students studying in the country, against the population of official tertiary age—so it can exceed 100 and moves when definitions change, as they did with successive revisions of the International Standard Classification of Education. The wage-employment share classifies workers by whether they receive a wage or salary, which cuts through the informal sector in ways that vary by survey instrument and statistical convention. Both carry non-classical error correlated with income, statistical capacity, and time.

## **3.2 The Specification Curve**

The curve is built from all combinations of five analytic dimensions: the measurement lag between the wage-employment share and tertiary enrolment (0, 5, 10, or 15 years); all 32 subsets of five controls (electricity, urbanisation, income, life expectancy, and the secondary completion rate); country fixed effects alone versus country and decade fixed effects; three sample restrictions (all countries, excluding oil exporters, and excluding countries with fewer than four usable observations); and the outcome measured in levels versus logs. The country's own starting tertiary enrolment appears in every specification, since it carries the identification argument of Section 2.3 and is not a choice a researcher is free to make.

The full cross of these dimensions yields 1,536 specifications. For each, the coefficient on the wage-employment share, its standard error, and its sign and significance at the 5% level are recorded. The curve is reported in full rather than summarised, with the estimates ordered by magnitude, the inferential statistics displayed beneath them, and the analytic choices producing the extremes labelled.

## **3.3 The Two Simulated Worlds**

In the **chain world**, the wage-employment share and tertiary enrolment are generated as persistent country processes, and increments in the former generate increments in the latter after a lag, with an effect size chosen to be plausible by the standards of the substantive literature rather than large enough to guarantee detection. Measurement noise is imposed at magnitudes consistent with the observed within-country standard deviations—9.43 points for tertiary enrolment and 2.24 points for the wage-employment share—so simulated data are as noisy as real data. In the **common-cause world**, one latent modernisation factor is generated as a persistent country process and both variables load on it in levels and in increments; no chain connects them, and loading, persistence, and noise parameters are set so that the simulated marginal distributions match the observed ones. The common-cause world is thus not one in which the two variables are independent: it is one in which they are strongly associated and the association is entirely spurious.

Both worlds are generated on the real coverage mask, so each replication inherits the actual countries, windows, missing cells, and observation count. The specification of Section 3.2 is estimated on each of 1,200 replications per world, and the reported statistics are the median, the 5th and 95th percentiles, and the number of replications reaching the observed value. The null distribution is thereby defined by the design rather than assumed: not the sampling distribution of the coefficient under a null of zero association, but its distribution under a null of *spurious* association, which has no closed form.

## **3.4 The Driver Battery and the Absorption Exercise**

The battery enters each of ten candidate drivers in the same specification in place of the wage-employment share and standardises the coefficient to points of tertiary growth per standard deviation of the driver. The benchmark is the common-cause noise band of approximately ±1.2 points, obtained by applying the same standardisation to coefficients recovered from the common-cause panels.

The absorption exercise asks what happens to a different edge—the association between tertiary expansion and upper-secondary completion, which any human-capital pipeline account requires—as controls enter. The outcome is the change in upper-secondary completion, the regressor of interest is the change in tertiary enrolment, and the controls are electricity, urbanisation, and the wage-employment share, singly and in combination.

<p align="center"><strong>4. Results</strong></p>

## **4.1 The Specification Curve**

Table 1 summarises the 1,536 specifications and Figure 1 displays them.

**Table 1**

*The Specification Curve: 1,536 Defensible Specifications of the Wage-Employment Coefficient*

| Statistic | Value |
|:-------------------------------------------------|:------------------|
| Median coefficient | ≈ 0.00 |
| 5th percentile | −0.040 |
| 95th percentile | +1.371 |
| Specifications with a positive coefficient | 73.7% |
| Significant and positive at the 5% level | 27.9% |
| Significant and negative at the 5% level | 0.3% |
| Median by measurement lag: 0 years | +0.39 |
| 5 years | +0.19 |
| 10 years | 0.00 |
| 15 years | +0.02 |
| Median by outcome transform: level | +0.86 |
| log | 0.00 |
| Median with the country's starting enrolment only | +0.12 |
| Median with any additional control | +0.01 |

*Note.* All specifications include the country's own starting tertiary enrolment. Dimensions varied are the measurement lag, all 32 subsets of five controls, country versus country and decade fixed effects, three sample restrictions, and level versus log outcome. Coefficients are in points of tertiary growth per point of change in the wage-employment share, or in log points where the outcome is logged.

**Figure 1**

*The Specification Curve: Estimated Wage-Employment Coefficient Across 1,536 Defensible Specifications*

![Figure 1. The specification curve: estimated wage-employment coefficient across 1,536 defensible specifications.](figures/fig17_specification_curve.png)

*Note.* Specifications are ordered by estimated coefficient. The upper panel plots point estimates; the lower panel records the analytic choices associated with each. The horizontal rule marks zero.

The curve's central fact is its median: across the full set of defensible analyses, the typical estimate of the relationship is zero. The 5–95% range runs from −0.040 to +1.371, so the distribution is bounded below by nothing and above by a substantively large positive effect. The coefficient of +1.425 used in the falsification test below sits just above the 95th percentile—a real estimate of a real specification, at the top of the range rather than near its centre.

The sign is the only stable feature. The coefficient is positive in 73.7% of specifications, but positive is not the same as distinguishable from zero: only 27.9% return an estimate that is significant and positive at the 5% level, 0.3% return one that is significant and negative, and the remaining 71.8% cannot be distinguished from no relationship at all. A literature that reported the modal specification would report nothing. That it reports something is a fact about selection among specifications.

The variation is organised by two choices the applied literature treats as conventions rather than commitments. The first is the lag: contemporaneous measurement returns a median of +0.39, five years +0.19, ten years 0.00, fifteen years +0.02. The association is a short-run association that decays to nothing by ten years—the opposite of what the chain account requires, since a chain in which credentials are acquired in anticipation of occupations should be strongest over the interval in which a cohort moves through tertiary study, not at zero.

The second is the outcome transform: +0.86 in levels, 0.00 in logs. This is the most damaging single result in the paper. A level specification asks whether a country whose wage share grew a point saw its enrolment ratio grow by a fixed number of points; a log specification asks whether the ratio grew proportionally faster. Because enrolment ratios run from single digits to above 100, the level specification weights large systems heavily and the log specification treats a move from 5% to 7% as equivalent to a move from 50% to 70%. The association exists only in the first metric. It is not a relationship between the growth of wage employment and the growth of higher education; it is a relationship between levels that survives differencing on one scale only.

The control set operates in the same direction: with the starting enrolment as the only conditioning variable the median is +0.12, and adding any one of the five controls takes it to +0.01. The starting level absorbs nearly everything, and the remainder is what most specifications' additional controls carry off.

## **4.2 The Falsification Test at the Largest Specification**

The test was run where the coefficient is largest: contemporaneous, level outcome, country and decade fixed effects, and no controls beyond the starting enrolment. The observed estimate there is +1.425 (*SE* = 0.410).

**Table 2**

*Observed Estimate Against Two Simulated Worlds*

| Statistic | Chain world | Common-cause world |
|:-----------------------------------------|:-------------|:-------------|
| Median coefficient | +2.201 | +0.000 |
| 5th percentile | +1.543 | −0.260 |
| 95th percentile | +2.885 | +0.255 |
| Replications | 1,200 | 1,200 |
| Replications reaching the observed value (+1.425) | — | 0 |

*Note.* Each replication is a fresh panel drawn on the real coverage mask (1,883 country-decades, 157 countries). The dash marks a quantity that is not meaningful for a non-null world; the relevant question there is whether the estimator recovers a chain at all, which it does.

**Figure 2**

*Simulated Distributions of the Wage-Employment Coefficient Under a Chain World and a Common-Cause World, With the Observed Value Marked*

![Figure 2. Simulated distributions of the wage-employment coefficient under a chain world and a common-cause world, with the observed value marked.](figures/fig01_chain_vs_common_cause.png)

*Note.* Densities are from 1,200 replications per world on the real coverage mask. The vertical rule marks the observed coefficient of +1.425 (*SE* = 0.410). The two distributions do not overlap.

The common-cause distribution is centred on zero with a 5–95% range of −0.260 to +0.255, which is not wide, because the starting level absorbs the factor's level. None of 1,200 common-cause panels reaches +1.425; with zero hits the 95% upper bound on the probability of such a draw is roughly 0.25%. The chain distribution is centred at +2.201 with a range of +1.543 to +2.885, so the observed value sits 1.9 standard errors below the chain median and just under its fifth percentile—within sampling error of the chain world and nearer its floor than its centre, which is what attenuation in a noisy regressor would produce.

At this specification the association is not an artefact of a symmetric common trend; it is what a chain looks like and not what a common cause looks like. What the result is not is evidence of robustness, since this specification was chosen for its maximum.

## **4.3 Direction**

The reverse-direction estimate is +0.010 (*SE* = 0.042), a precise zero excluding any effect larger than about 0.09. The precision is not an artefact of a weak test: the within-country standard deviation of the wage share is 2.24 points against 9.43 for tertiary enrolment, so the reverse equation returns a standard error an order of magnitude smaller. A latent factor acting on both variables does not privilege a direction, since the covariance of two residuals does not care which is on the left-hand side; under a common cause the design should return two modest coefficients or two zeros. It returns one large coefficient and one zero.

## **4.4 The Cross-Section**

**Figure 3**

*Wage Employment Share and Tertiary Enrolment Across Countries*

![Figure 3. Wage employment share and tertiary enrolment across countries.](figures/fig02_wage_vs_tertiary.png)

*Note.* Each point is a country. The association is strong and positive, and it is uninformative about mechanism: it is equally consistent with wage employment causing higher education, higher education causing wage employment, and a common cause producing both.



## **4.5 The Driver Battery**

**Table 3**

*Standardised Coefficients for Ten Candidate Drivers of Tertiary Expansion*

| Driver | Standardised coefficient | *SE* | Position relative to the common-cause band (±1.2) |
|:---------------------------|-----:|-----:|:----------------------------|
| Lower-secondary completion | +4.01 | 0.86 | Outside, above |
| Upper-secondary completion | +3.79 | 0.84 | Outside, above |
| Urbanisation (cities) | +3.21 | 1.01 | Outside, above |
| Paid employment (wage share) | +3.20 | 0.92 | Outside, above |
| Life expectancy | +2.69 | 0.63 | Outside, above |
| Primary completion | +2.04 | 0.42 | Outside, above |
| Child mortality (under five) | −2.09 | 0.61 | Outside, below |
| Income (log GDP per capita) | +0.97 | 0.81 | Inside |
| Electricity access | +0.19 | 0.45 | Inside |
| Female labour force participation | −0.14 | 0.77 | Inside |

*Note.* Coefficients are in points of growth in the tertiary gross enrolment ratio per standard deviation of the driver, estimated with country and decade fixed effects and the country's own starting tertiary enrolment ratio. The band is the range within which standardised coefficients recovered from the common-cause panels fall—roughly ±1.2, varying between about ±1.1 and ±1.5 across drivers.

**Figure 4**

*Standardised Coefficients for Ten Candidate Drivers Against the Common-Cause Noise Band*

![Figure 4. Standardised coefficients for ten candidate drivers against the common-cause noise band.](figures/fig03_driver_battery.png)

*Note.* Points are standardised coefficients; horizontal bars are one standard error. The shaded region is the common-cause noise band of roughly ±1.2.

The battery divides cleanly, and not along the line a modernisation account predicts. Income per capita, the workhorse control of this literature, returns +0.97 (*SE* = 0.81); electricity access +0.19 (0.45); female labour force participation −0.14 (0.77). All three sit inside the band, so once the country's own starting enrolment and the fixed effects are in the specification, none of them says anything about which decade grew faster. What survives is a different list—secondary completion, urbanisation, the wage share, life expectancy, primary completion, and child mortality, all outside the band (Table 3). The survival variables are not obviously part of a labour-market story, which is a caution against reading the battery as a ranking of mechanisms; what it shows is which variables behave like chain variables and which like markers of a trend. Like the falsification test, it was estimated at one specification, and the fragility documented in Section 4.1 applies to its entries as much as to the coefficient it interprets. Its contribution is comparative, not inferential.

<p align="center"><strong>5. Robustness</strong></p>

## **5.1 Influence and Absorption**

The specification curve tests one kind of fragility and the jackknife tests another. Across 203 leave-one-country-out estimates the coefficient runs from +0.83 when Turkey is dropped to +1.22 when North Macedonia is dropped, and is positive in 100% of them: the largest specification is not an artefact of any single country. That is a genuine robustness result and a narrow one. It says no influential case drives the estimate, not that the estimate survives analytic choices.

**Table 4**

*Absorption of the Tertiary-to-Secondary Edge as Controls Enter*

| Control set | Coefficient on tertiary expansion |
|:-----------------------------------------|------:|
| No controls | +0.106 |
| + electricity | +0.102 |
| + cities | +0.035 (n.s.) |
| + paid employment | +0.049 |
| + electricity, cities | +0.079 |
| + cities, paid employment | +0.017 |
| + electricity, cities, paid employment | +0.066 |

*Note.* Outcome is the change in the upper-secondary completion rate; the regressor of interest is the change in tertiary enrolment, with country and decade fixed effects throughout. n.s. = not statistically significant. The full-controls row does not fall monotonically because electricity, cities, and paid employment correlate at .69 to .80.

**Figure 5**

*Absorption of the Tertiary-to-Secondary Edge as Controls Enter*

![Figure 5. Absorption of the tertiary-to-secondary edge as controls enter.](figures/fig04_absorption.png)

*Note.* Bars are the coefficient on tertiary expansion in a regression for upper-secondary completion growth, by control set. The edge survives the infrastructure control almost unchanged and is absorbed by the labour-market controls.

Electricity barely moves the edge (+0.106 to +0.102); urbanisation absorbs two-thirds of it (+0.035, no longer distinguishable from zero); paid employment absorbs about half (+0.049); the two together reduce it to +0.017, while all three return +0.066—collinearity doing what Section 2.2 said it would. The reading is narrow: the pipeline is not mechanical, the absorption is done by the urban-wage bundle rather than by infrastructure, and the contributions of cities and paid employment cannot be separated.

<p align="center"><strong>6. Discussion</strong></p>

Two findings have to be held together, and most of the difficulty in this literature comes from reporting one without the other.

The first is fragility. The median of 1,536 defensible specifications is zero, only 27.9% are significant and positive, and the two choices that govern the magnitude—lag and outcome transform—are exactly the choices that applied work tends to settle by convention. The lag result is the more substantive: an association strongest contemporaneously and gone by ten years is not the association the human-capital account predicts, since that account requires the delay in which a cohort is trained. The transform result is the more damaging: the relationship exists between levels and vanishes between proportional changes, so it is partly a statement about the scale on which enrolment ratios are measured. Any claim that wage employment drives the growth of higher education has to survive the log specification, and it does not.

The second is direction. At the specification where the association is largest, it is not what a common cause produces. The simulated common-cause world, built with a persistent latent factor loading on both variables and estimated on the real coverage mask, returns a median of zero with a ceiling of +0.255, and never reaches +1.425 in 1,200 attempts; the chain world returns a median of +2.201. The reverse-direction estimate is a precise zero, which a symmetric latent process would not produce. The driver battery points the same way: income, electricity, and female participation behave like markers of the trend, while the schooling pipeline, urbanisation, and the wage share do not.

Put together, these say that the fragile signal is not noise: it is a directional relationship of modest and unstable magnitude, visible where measurement is contemporaneous and on the level scale, and not attributable to a symmetric common trend. That is weaker than the literature usually claims and stronger than the curve alone would license.

The battery's treatment of income deserves emphasis, because it is where the fragility and the direction results intersect. Income per capita is the best available proxy for the latent factor, and it fails the battery: entered on its own terms it returns +0.97, inside the noise band, because the country's own starting enrolment already encodes how rich it is. Richer countries do have larger tertiary systems; income simply does not tell us which decade grew faster. The same holds for electricity. This is consistent with Schofer and Meyer's (2005) observation that expansion is not reducible to domestic economic demand, with one qualification: diffusion may explain why nearly every country expanded, but not why one expanded faster than another in a given decade.

The same identification problem runs through the adjacent literature on demographic change, where diffusion and social interaction were advanced against demand theories of the fertility transition (Bongaarts & Watkins, 1996; Cleland & Wilson, 1987) and where a global process has regional timing that no single covariate explains (Reher, 2004). In each case the dispute concerns whether a correlation is a chain or a common cause, and its resolution has required designs that distinguish the two rather than specifications that add controls.

One battery result cuts against expectation. Female labour force participation returns −0.14, inside the band and marginally negative, which is not evidence that female employment is irrelevant to education but evidence that the aggregate participation rate is a poor index of the gendered structure of wage work. The cross-national literature on female schooling has long found its measurable returns running through fertility and child survival rather than participation alone (Subbarao & Raney, 1995), and the survival variables are among the battery's strongest entries.

<p align="center"><strong>7. Limitations</strong></p>

The design cannot separate the wage-employment share from urbanisation. The two correlate at .74, perform almost identically in the battery (+3.20 and +3.21), and act as a bundle in the absorption exercise. The honest description is that higher education tracks the growth of an urban wage-labour economy, and nothing here establishes that the wage share rather than the urban share is operative.

The design cannot exclude a chain through an unmeasured correlate of the wage share. Falsifying the common-cause account falsifies one rival, not all rivals: a chain in which formal hiring is driven by foreign investment, commodity rents, or public payroll expansion would produce the same signature. Nor is the null distribution a theorem: the band is narrow because of how the latent factor was specified, and a differently specified process could in principle generate residual covariation the starting level does not remove.

Measurement is a first-order problem. The wage-employment share classifies informal wage work inconsistently across surveys and decades; the gross enrolment ratio moves with age structure, cross-border student mobility, and successive revisions of the International Standard Classification of Education. Attenuation is the likeliest reason the largest estimate falls below the chain median, but it cannot be distinguished here from a real effect smaller than the simulated one, or from a specification selected for its maximum.

Coverage is not random: the 157 countries on the mask are those with usable series, so the panel over-represents states with the administrative capacity to report. The ten-year grid is coarse, a chain over five or twenty years mismatching the interval. And the estimates are ecological: they describe countries, not people, and the individual-level relation between schooling, wage employment, and enrolment need not resemble the aggregate one (Kravdal, 2002).

<p align="center"><strong>8. Conclusion</strong></p>

The association between wage employment and the expansion of higher education is real and fragile. Across 1,536 defensible specifications of the same cross-national panel the median coefficient is approximately zero, the 5–95% range runs from −0.040 to +1.371, and only 27.9% of specifications return a significant positive estimate. The association is strongest at short lags, on the level scale, and with no controls beyond the country's own starting enrolment; it disappears at a ten-year lag and under a log transform. Where it is largest, +1.425 (*SE* = 0.410), it is not an artefact of a symmetric common trend: a simulated common-cause world returns a median of +0.000 with a ceiling of +0.255 and never reaches the observed value, a chain world returns a median of +2.201, and the reverse-direction estimate is +0.010 (0.042). Leave-one-country-out estimates are positive in all 203 jackknifes.

The honest summary is that direction can be established at a specification and stability cannot be established at all. A field reporting +1.425 as the finding would report the top of a distribution whose median is zero; a field reporting the median would discard the one result that survives a falsification test. Both belong in the abstract, and the specification curve belongs in the paper rather than an appendix.

<p align="center"><strong>References</strong></p>

<p style="margin-left: 2em; text-indent: -2em;">Bongaarts, J., & Watkins, S. C. (1996). Social interactions and contemporary fertility transitions. <em>Population and Development Review, 22</em>(4), 639–682. https://doi.org/10.2307/2137804</p>

<p style="margin-left: 2em; text-indent: -2em;">Boppart, T., Kiernan, P., Krusell, P., & Malmberg, H. (2023). <em>The macroeconomics of intensive agriculture</em> (NBER Working Paper No. 31101). National Bureau of Economic Research.</p>

<p style="margin-left: 2em; text-indent: -2em;">Cleland, J., & Wilson, C. (1987). Demand theories of the fertility transition: An iconoclastic view. <em>Population Studies, 41</em>(1), 5–30. https://doi.org/10.1080/0032472031000142516</p>

<p style="margin-left: 2em; text-indent: -2em;">Galor, O., & Weil, D. N. (1996). The gender gap, fertility, and growth. <em>American Economic Review, 86</em>(3), 374–387.</p>

<p style="margin-left: 2em; text-indent: -2em;">Kravdal, Ø. (2002). Education and fertility in sub-Saharan Africa: Individual and community effects. <em>Demography, 39</em>(2), 233–250. https://doi.org/10.1353/dem.2002.0017</p>

<p style="margin-left: 2em; text-indent: -2em;">Reher, D. S. (2004). The demographic transition revisited as a global process. <em>Population, Space and Place, 10</em>(1), 19–41. https://doi.org/10.1002/psp.313</p>

<p style="margin-left: 2em; text-indent: -2em;">Schofer, E., & Meyer, J. W. (2005). The worldwide expansion of higher education in the twentieth century. <em>American Sociological Review, 70</em>(6), 898–920. https://doi.org/10.1177/000312240507000602</p>

<p style="margin-left: 2em; text-indent: -2em;">Subbarao, K., & Raney, L. (1995). Social gains from female education: A cross-national study. <em>Economic Development and Cultural Change, 44</em>(1), 105–128. https://doi.org/10.1086/452202</p>
