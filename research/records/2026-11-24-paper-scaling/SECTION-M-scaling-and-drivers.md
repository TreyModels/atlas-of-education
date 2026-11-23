# Paper M — Section draft: scaling laws, the θ/γ programme, and the massification-driver null

**Section author:** cuda-scale. **Intended integration:** Paper M (Massification omnibus), sections 5 and 6,
led by panel-matrix (`research/records/2026-11-25-paper-massification/`). **Draft length:** ≈3,400 words.
**Evidence base:** `research/scaling-2026-11-23` @ `fd691a6`, `research/scaling-data-hunt-2026-11-23` @
`9e15b6d`, `research/scaling-laws-catalogue-2026-11-23` @ `cfe372f`, `research/sfi-scan-2026-11-23` @
`fd4cfd2`, and `research/grouping-multiverse-400-2026-11-23` @ `1152cec`. Every number is mapped to its
source file in `SOURCES.md`. This section is a **replication and audit**, not a discovery: it tests
whether canonical scaling laws and the project's own scaling claims survive contact with education and
development data, and it reports what does not.

## 5. Scaling laws and the θ/γ programme

### 5.1 What was tested, and why it is an audit

The canonical scaling literature makes three kinds of claim: that urban socioeconomic output grows
superlinearly with city size (exponent β ≈ 1.15), that material infrastructure grows sublinearly
(β ≈ 0.85), and that rank–size, growth and category-richness regularities (Zipf, Gibrat, Heaps) describe
how city systems and their functional repertoires are distributed (Bettencourt et al. 2007; Bettencourt
2013). The project's theory adds a mechanism-flavoured version: low-inhibition (low-θ) kin networks are
said to diversify functionally as they scale, whereas high-inhibition, high-specialisation (high-θ/high-γ)
systems shift into a saturating regime in which scale buys credential categories but not functions
(the θ/γ formalism of Yang et al. 2026). Our task was not to discover a new law. It was to ask, with
pre-registered tests and honest nulls, **which of these claims are testable with education and
development data, whether they replicate, and what they do and do not describe**. The tests were
pre-registered before the data were touched (`PREREGISTRATION.md`, commits `f8f782f` and `5e0b11a`).

Three design choices follow from the measurement critique literature (Arcaute et al. 2015; Leitão et al.
2016; Cottineau et al. 2017). First, **category counts depend on sampling effort**, so any claim about
functional diversity must be made on rarefaction/accumulation curves, not raw counts. Second,
**functional form must be compared out of sample**, because an S-curve fitted as a power law (or the
reverse) will look like a rejected law. Third, **a between-country cross-section is not a within-country
law of change**: a regularity that holds across countries may say nothing about what happens as any one
country grows, which is the relevant question for a theory of massification.

### 5.2 Occupational diversity: Heaps' law survives the sampling correction, and sits below the benchmark

Raw counts of distinct occupational categories per country are almost pure sampling artefact: regressing
log distinct categories on log workforce size gives a slope of **−0.002**. Countries with more workers do
not record more categories, because the classification has only ten one-digit ISCO-08 groups; what varies
is survey effort. The honest object is the rarefaction curve — the expected number of distinct categories
in a sample of size *n* drawn from a country's employment distribution — and Heaps' law is a statement
about that curve's slope.

On the rarefied curves, the exponent is **b = 0.333 (SE 0.011)** across **151 countries and 11,712 curve
points**, with country-clustered standard errors; the per-country median is 0.374 [IQR 0.319–0.468]. This
is strongly sublinear: proportional growth (b = 1) is rejected at z = −58.8. But it is also **below the
Heaps benchmark of 0.4–0.6** (z = −5.9 against 0.4), and the binding caveat is classification depth: the
public ILOSTAT API now exposes only ISCO-08 one-digit major groups, with the two- and three-digit series
deprecated. A ten-category ceiling truncates the curve and pushes the estimated exponent down. A
bootstrap that uses one curve per country (latest year) gives **0.349, 95% CI 0.331–0.368**; the
all-years estimate and the latest-year estimate agree within their uncertainty, so the number is
robust to resampling, not to depth. **Verdict: sublinear diversity scaling replicates; the literature
value does not.** The comparison is to Heaps (1975) and to the empirical scaling literatures in word
use and novelty (Petersen et al. 2012; Tria et al. 2014), which report exponents in the 0.4–0.6 range
for richer category systems.

The θ/γ theory predicts that the exponent should differ between low- and high-inhibition systems. We
cannot test that, because **θ and γ are not measured variables**: they are model primitives, not country
observables. We can say what happens when the closest observable institutional proxies are used —
income group and region — and we report that as a proxy result, not as a test of θ/γ. The rarefied
exponent does **not** vary significantly across income groups (means 0.343–0.355; Kruskal H = 1.22,
p = 0.75) or regions (0.281–0.400; H = 6.48, p = 0.26); the high-vs-low income difference is 0.010
(95% CI −0.043 to 0.062), and negative curvature is present in every group. The data give no support
for a two-regime story, but they also give no test of it. That distinction between "unsupported" and
"not estimable" is essential: θ/γ must be **fitted from category data with depth**, not inferred from
income or region labels.

### 5.3 No regime break at the universalisation threshold

The theory's second quantitative move is a threshold: past universalisation of schooling, additional
scale should yield diminishing functional novelty — a saturating regime. On the rarefied accumulation
curves, adding a squared log-size term does show **negative curvature, c = −0.058 (SE 0.0018; t ≈ −33)**.
That is consistent with saturation. But saturation in this dataset is partly the ten-category ceiling
speaking. The sharper test is a slope break at the universalisation threshold. Splitting countries by
female secondary attainment gives exponents of **0.360** (27 countries, below 50%), **0.403** (24
countries, 50–80%) and **0.387** (85 countries, above 80%): **no significant difference** (Welch
t = −1.25, p = 0.22). **Verdict: curvature yes, threshold break no.** A pre-registered regime-change
claim at universalisation fails. The closest prior benchmark is Trow's (1973) elite–mass–universal
threshold account of higher education and the world-society expansion literature (Schofer & Meyer
2005), both of which motivate a break; neither implies that occupational *category richness* must
break there.

### 5.4 Within versus between: most education–income "scaling laws" are cross-sectional regularities

This is the most useful result in the section for the massification argument, and it is a negative one.
Using the project's prior 30-country panel (15 relations, each estimated within countries and between
countries in log–log form), most education–income relations that look like scaling laws between
countries **weaken or vanish inside them**. Secondary enrolment vs income: between **0.215 (SE 0.035)**,
within **0.090 (SE 0.124)** — indistinguishable from zero. Upper-secondary attainment: between 0.312
(0.052), within 0.072 (0.167). Education stock vs output: between 1.176 (0.258), within 0.051 (0.108).
Cohort size vs enrolment: between −0.612 (0.127), within −0.006 (0.219). A handful survive both layers —
tertiary enrolment (0.567 between, 0.848 within), lower-secondary completion (0.169/0.247), services
employment share (0.294/0.275), urban share vs enrolment (0.012/0.011, semi-log) — and these are the
only ones we call **law-like candidates under a within-and-between criterion**. The local project's
five-estimator stability test classifies three relations as "scaling law (stable across estimators)"
(secondary GER, tertiary GER and lower-secondary completion vs GDP per capita), 14 as period/region
regularities and one as unidentified. The two classifications agree on the general picture: stability
across estimators is necessary but not sufficient; an exponent that lives only in the cross-section is
a **between-country regularity, not a law of change**. The same lesson appears in our own collapse
analysis below, and it is a direct caution for any theory that wants to read cross-country
massification gradients as a law of growth.

### 5.5 Urbanisation and income: an S-curve, not a power law

Urbanisation is the standard development companion of mass schooling, and the catalogue flagged that the
urbanisation–income relation is usually described as an S-curve. We fitted a logistic, a log-linear form
and a power law to 10,986 country-year observations across 208 countries. The logistic is **not
rejected and fits best out of sample** (RMSE in urban-share units: 0.1523 logistic, 0.1532 log-linear,
0.1598 power law), with slope **0.572 (SE 0.030)** and a midpoint at about **$3,647** per head. But the
margin over a straight line is small, and the correct verdict is a **regularity, not a scaling law**:
functional form matters, yet no single power-law exponent describes the urban transition. The literature
benchmark here is qualitative (the S-curve account of urbanisation; Henderson 2003 on the urbanisation–
growth relation), not an exponent, and we label it that way.

### 5.6 The negative result: there is no universal fertility–attainment collapse curve

The theory's most ambitious scaling claim is that fertility, as a function of female attainment, falls on
**one common curve across countries and cohorts** — "same niche, same function". We built the cohort
panel directly: for each country and birth cohort (1950–1996), female secondary completion (adjusted by
the gender-parity index) at age 20 against total fertility at age 28. This gives **4,394 country–cohort
points across 158 countries**.

The best common curve is exponential: fertility = 1.13 (SE 0.26) + 5.97 (SE 0.23) × exp(−0.0197
(SE 0.0025) × attainment), pooled R² = 0.78. If one stopped there, one would report a successful data
collapse. One should not. **Country identity explains 71.6% of the remaining residual variance**;
country intercepts raise R² to 0.914 and country-specific slopes to 0.955; the slope-heterogeneity
F-test is **46.4 on 313 and 3,717 degrees of freedom**. The residual standard deviation is **0.847
births per woman, 11.2% of the fertility range**, and after a country-level multiplicative rescaling it
is still 0.434 (R² = 0.942). The residuals are structured, not noise: low-income countries sit **+0.40**
births above the common curve while high-income countries sit −0.11; the 1950s cohorts sit **+0.29** and
the 1970s cohorts −0.17. In other words, the common shape is real but it is not *binding*: countries and
cohorts shift it systematically.

The levels-versus-changes decomposition makes the point in the form most relevant to massification. The
between-country slope of log fertility on log attainment is **−0.479**; the within-country levels slope
is **−0.299 (SE 0.026, t = −11.7)**; but the slope for **ten-year changes within countries is only
−0.056** across 2,064 changes in 201 countries. The relation exists in levels and in cross-sections, and
it is roughly a sixth as strong when countries actually move. **Verdict: the "universal collapse curve"
is rejected as a universal law** — a common functional shape with country-specific levels and slopes is
all the data support. This is the paper's main negative result and should keep its own subsection.
The closest prior work is the comparative demographic-transition literature, which has long documented
country-specific timing even under shared direction (Lee 2003; Brewster & Rindfuss 2000; Soares 2000);
our contribution is the explicit collapse test with a specified common curve and reported residual
structure, not a new theory of fertility decline.

### 5.7 Rank–size: consistent with Zipf, but a weak test

With a city-population list finally assembled (GeoNames, 34,248 populated places; 22,465 cities in
**55 countries** with at least 50 cities), the per-country rank–size exponent has **median 0.859**
(bootstrap 95% CI 0.746–0.978; IQR 0.647–1.237; mean 1.142, SD 1.147). Only 27% of countries fall inside
0.8–1.2, and a Wilcoxon test against ζ = 1 does **not reject** (p = 0.23). **Verdict: consistent with
Zipf's ≈1, but not a strong confirmation.** The caveats are severe: GeoNames is crowdsourced and lists
localities/city-proper populations rather than UN urban agglomerations; only larger countries have 50+
towns above 15,000 people, so the sample is selected; and a pooled country-fixed-effects estimate
(0.386, cluster bootstrap CI 0.293–0.677) is dominated by large countries with many small towns and is
reported only as a secondary statistic. This sits inside the contested rank–size literature rather than
resolving it (Zipf 1949; Malevergne et al. 2011; Cottineau et al. 2017).

### 5.8 Gravity: a partial replication

The one classic law that our data allow cleanly is the gravity relation for bilateral migrant stocks.
Using the UN DESA 2024 bilateral migrant stock matrix and CEPII weighted distances, we estimate PPML
with origin and destination fixed effects on **8,020 country pairs** (195 origins × 187 destinations),
clustering by destination. The **distance elasticity is −0.970 (SE 0.076)**, against a literature range
of roughly −1 to −2 (Beine et al. 2016). Without fixed effects (which absorb the size terms) the
distance coefficient is −0.622 (0.149), with origin size +0.456 (0.057), destination size +0.533 (0.114),
contiguity +0.677 and common language +0.603; OLS log–log with fixed effects gives distance **−1.306
(0.053)**. **Verdict: partial replication** — the distance decay is negative and of the right order,
at the edge of the literature band under PPML and inside it under OLS, while the size elasticities
(≈0.5) fall short of the canonical ≈1. Data integrity was checked before fitting: the pair matrix sums
to **282 million** against the published world total of **281 million**, the gap arising from
region-level/unknown origins, and spot checks against UN destination totals are reported rather than
hidden. This is a correlational cross-section (2024 only; time-invariant distances), not a causal
estimate.

### 5.9 θ and γ are not estimable with these data

The theory's θ/γ formalism is its most direct quantitative prediction: functional diversity should grow
sublinearly with system size, with an inhibition parameter θ and a specialisation parameter γ governing
the regime (Yang et al. 2026; Holehouse et al. 2025). **We cannot estimate θ or γ.** They are not
observed country variables; they are latent model parameters. Estimating them requires (i) category
counts at two- or three-digit depth, which ILOSTAT no longer serves publicly, and (ii) credential counts
to observe the claimed divergence between category proliferation and functional novelty, which are not
held. We tested the *observable implication* — sublinear rarefied diversity — and it holds (b = 0.333);
we could not test the regime parameterisation. The honest statement is **not estimable**, not
"unsupported": the theory's central parameter is outside the current measurement envelope.

### 5.10 The data walls, stated plainly

Three canonical tests remain **untested because the data do not exist in our environment**, and we did
not proxy them. (i) **Bettencourt urban output and infrastructure scaling**: requires city-level GDP,
wages, patents or infrastructure stock. Every known source failed: UN WUP city files returned 404; the
UN Data Portal API exposes city data only as size-class aggregates; the US BEA regional archives failed
with HTTP 000. City populations but not city output is the binding gap, exactly as the prior feasibility
audit predicted. (ii) **Credential inflation**: requires counts of distinct credential categories and
detailed occupations over time. BLS SOC/OES returned HTTP 403 (Access Denied) and the Credential Engine
registry returned a 403 Cloudflare challenge; no credential series is held. (iii) **Gibrat's law**:
requires two city-population waves for the same city definitions; GeoNames is one vintage and no WUP
panel was reachable. Each failure is recorded with its exact URL, status and byte count in the data
record (`results/pull_log.json`). The literature exponents (Bettencourt et al. 2007; Bettencourt 2013;
Ortman et al. 2014, 2015) remain benchmarks we could not test on education/development data, and we say
so rather than substituting a country panel for a city panel.

### 5.11 What scaling laws do and do not describe

Three conclusions follow, and they are the point of the audit. First, **a scaling regularity is not a
causal identification**: none of the exponents above identifies a mechanism, a policy lever, or a
parameter that can be transplanted into a schooling model. Second, **not every scaling candidate is even
a regularity**: of the classics, only the gravity relation partially replicates on our data, Zipf is
consistent-but-weak, Heaps is sublinear-but-below-benchmark, and the urban-output laws are untested.
Third, and most consequential for the massification paper, **between-country scaling is a different
object from within-country change**: education–income exponents shrink when countries are compared to
themselves, and the fertility–attainment relation is roughly six times weaker in ten-year changes than
between countries. A theory that treats cross-country gradients as a law of massification inherits that
gap. The honest summary is a replication-and-audit verdict: the canonical laws are useful as
**benchmarks and diagnostic frames**, not as established quantitative laws of education and development.

## 6. Massification drivers: a 272-link multiverse that returns a small set of nulls

### 6.1 Design

The massification-driver question was posed as a lead–lag matrix: 17 measures, change over the following
ten years, country and decade effects, clustered errors, controls for income and urbanisation, with and
without a country trend. That produces **272 links**. Because any split of countries into groups is
somewhat arbitrary, each link is re-estimated inside **50 real groupings** (8 families, 179 groups) and
inside **400 random re-partitions** of the same countries with the same group sizes — the yardstick for
what chance alone produces (38.4 million regressions; `research/grouping-multiverse-400` @ `1152cec`).
A link "beats random" only if its real-group evidence exceeds the random-group distribution. The run is
deterministic (three replicates and the real pass are bit-identical), reproduces the earlier 74-draw
classification exactly, and is stable to half-splits (p rank correlation 0.994; full-400 verdicts agree
with a half in 267–269 of 272 links).

### 6.2 The result: no driver is robust everywhere

**Nothing is robust everywhere among the massification drivers.** Of 272 links, 5 are robust in every
kind of grouping, 76 are group-specific, 30 beat random without a clear group, and **161 are no better
than random**. With a better-estimated null, 46 links beat random with trends (42 of the old 43 survive,
1 dies, 4 are new), 20 are worse than random, and 32 show more sign-flipping. The honest reading is
"a small set of strong links, a large null remainder" — and the large remainder is not a power artefact:
none of the links previously classified as no-better-than-random is above the 400-draw ceiling.

### 6.3 Electricity: a strong first-pass signal that becomes contingent and sign-unstable

Electricity is the clearest example of why the multiverse matters. In the pooled matrix it looks strong.
Once country trends are allowed it is **zero in the whole sample**, and its grouped evidence is patchy:
11 of its 32 links show more sign-flipping than random groupings — the most of any driver — while a
cluster of its schooling links beats random only in specific classes. **Verdict: electricity is a weak,
group-dependent driver whose apparent effect is not stable once countries are allowed their own trends.**
The prior-art benchmark is the rural-electrification literature, where effects on employment and
household behaviour are real but context-dependent (Dinkelman 2011); our result is consistent with that
reading, not with a universal electrification lever.

### 6.4 Paid employment: the cleanest null

**No wage-employment link to a schooling outcome beats random groupings in any kind of group.** This is
the clearest null in the run. It is a strong statement because the test is not "no significant pooled
coefficient" — it is "no group-based evidence above chance across 400 random partitions". A null that
survives this design is a result: paid-employment expansion, on its own, does not reliably lead
schooling expansion in these data.

### 6.5 The two robust fertility links, and what "robust" can mean

On the fertility side, exactly two links are robust everywhere: **child mortality → birth rate**
(significant in 95% of real groups, versus a random-group median of 93%) and **life expectancy → birth
rate** (81% versus 93%). Note the correct comparison: these are claims of a *uniform* effect, so a
uniform effect also shows up in random slices, and the right test is similarity to the random
distribution. Their random-comparison shares are statistically indistinguishable from the random median
at 400 draws — which is the point. Both survive the split-halves test and neither changes class.
Everything else on the fertility side is group-specific or no better than random; 13 fertility links hold
only in particular kinds of country, and several of those rest on one region or one class and should not
be carried as general claims.

### 6.6 What 400 draws can and cannot certify

The resolution arithmetic is part of the result. With 400 random groupings the smallest achievable
empirical p-value is 1/401 ≈ 0.0025; a lone link cannot clear a 5% false-discovery threshold over 272
links, which would need about **5,440 draws**. Certification is nonetheless possible because links pile
up at the ceiling and Benjamini–Hochberg is a step-up rule: with 30 links at the floor, the cluster
clears, and the strict tier certifies **35 up and 19 down** links. The descriptive ceiling statement is
"30 links above all 400 random draws" (0.68 expected by chance). The main-tier normal-fit test certifies
46 links; a t-fit certifies 42. These are the bounds a reader should carry: **the exact counts are
provisional under the positive-dependence assumption of BH, and the named groups are descriptions of
where a link is concentrated, not certified claims.**

### 6.7 What a null means here

The value of the run is the discipline it imposes: a driver claim must survive a random-grouping
yardstick, a better-estimated null, sign stability across classes, and split-half stability. Electricity
and paid employment do not; the two mortality links do; the rest are contingent. For the massification
argument this supports the synthesis that massification is **institution- and state-led in
late-industrialisers and demand-led only where industrialisation came first**, not a universal law
driven by any single variable — with the caveat that the driver matrix is correlational and the
group-specific labels are the weakest evidence in it.

**Data notes for integration.** All scaling numbers and their source files are listed in `SOURCES.md`;
the scaling records carry their own pre-registrations (`f8f782f`, `5e0b11a`) and data-wall logs
(`results/pull_log.json`); the multiverse record carries its determinism, reproduction and half-split
falsifiers. Literature for each claim, with Crossref verification status, is in `claims-prior-art.md`;
the bibliography is `refs.md`.
