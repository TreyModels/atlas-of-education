# The shape of the demographic transition: one path, many timings

**Draft for:** *Demography* / *Population and Development Review* / *Population Studies*. **Date:** 25 November
2026. **Data and code:** `research/records/2026-11-25-paper-shape/` (branch `research/paper-shape-2026-11-25`).
**Framing:** a measurement and replication paper about functional form; no causal identification is claimed.

## Abstract

The demographic transition is usually described in words and drawn as an S-curve, but its functional form has
rarely been quantified across the whole set of countries that have transitioned. We fit five competing forms —
logistic, Gompertz, exponential decay to a floor, linear-decline-with-kink, and a flexible spline — to annual
total fertility for 105 countries over 1960–2023, compare them by information criteria and a last-decade
hold-out, extract six shape descriptors (onset, midpoint, speed, duration, floor, curvature), test whether the
shapes cluster, and ask which covariates predict the shape. Three results stand out. First, the canonical
S-curve is not the best description of the estimable window: an exponential decline to a floor fits best for
49% of countries and Gompertz for 29%, while the logistic wins for only 7% and is the worst of the four
parametric forms out of sample (last-decade RMSE 0.48 births per woman, against 0.31 for the exponential).
**With truncated 1960–2023 series we cannot distinguish a genuinely non-logistic form from a logistic that
the window leaves unidentified; the claim is that the exponential-to-floor family describes the available
transition data better, not that the S-curve is refuted.** Second, once each
transition is aligned on its own onset and duration, the *path* is nearly universal (country-to-country
standard deviation of the aligned curve 0.017; the first principal component explains essentially all
remaining variance), so the heterogeneity documented in cross-country fertility studies lives almost entirely
in *timing, pace and level*, not in the functional shape of the decline. Third, two broad transition classes
are nevertheless detectable — an earlier, deeper, more curved class (58 countries; median onset 1965, floor
1.68) and a later, shallower, more linear class (47 countries; median onset 1973, floor 2.36) — and the
partition is better than random (silhouette 0.28; 0 of 500 random partitions as coherent, p < 0.01), though
silhouette levels are modest enough that the honest description is two poles of a continuum rather than
discrete types. The strongest correlate of timing is the timing of mortality decline: a one-year later
ten-year gain in female life expectancy is associated with a 0.24-year later onset (SE 0.04) and a 0.30-year
later midpoint (SE 0.05). Higher urbanisation at onset is associated with earlier transitions; female
secondary completion at onset is associated with longer, more curved declines. Schooling-expansion timing has
no independent association once mortality timing is accounted for. Richer data are needed before any of these
associations can be read causally. The practical implication is that the "model country" approach to
forecasting is defensible for the *shape* of the decline and indefensible for its *timing*.

## 1. Introduction

Few ideas in demography have travelled as far as the demographic transition, and few have been asked to carry
as much. The transition supplies the organising narrative of fertility decline (Notestein 1945; Davis 1963),
the baseline for population projections (Alkema et al. 2011; Raftery et al. 2014), and — increasingly — a
template that policy documents apply to countries still in mid-transition: fertility is said to fall in a
characteristic S-shaped curve from high to replacement, and the task of policy is to move countries along it.
Yet the transition's *functional form* is rarely estimated. The canonical S-curve is usually drawn, not fitted.
When it is fitted, it is fitted as part of a projection model whose parametric family is chosen for
convenience rather than tested against alternatives. And the heterogeneity that the comparative literature
emphasises — early versus late, fast versus slow, deep versus stalled (Cleland & Wilson 1987; Bongaarts 2008;
Bongaarts & Casterline 2013; Reher 2004; Lesthaeghe 2010) — is described in typologies, not measured as
differences in fitted shape parameters.

This paper asks a narrow set of questions with as much measurement discipline as the data allow. Is there one
shape, a few shapes, or country-specific shapes? If shapes differ, along which dimensions do they differ —
timing, pace, depth, or the functional path itself? Do the differences cluster, and is any clustering better
than what random partitions of the same countries produce? And do observable covariates — schooling expansion,
mortality decline, income, urbanisation — predict the shape parameters? The paper is a measurement paper, not
a theory paper. It does not propose a new theory of the transition, and it does not claim causal effects; it
quantifies a functional form that is usually assumed.

The analysis rests on a fresh pull of the World Bank's annual World Development Indicators for 1960–2023, with
105 countries that meet a transparent transition rule. For each country we fit five functional forms, compare
them by AIC/BIC and by a hold-out of the last decade, extract descriptors from the observed series, test
whether the normalised decline paths differ (they barely do), cluster the timing-and-pace descriptors (they
do, weakly, into two poles), and regress the descriptors on covariates.

Four findings organise the paper. First, **the S-curve is usually assumed rather than tested, and in the estimable window it is not the best-fitting form**. An exponential decay to a floor and
the Gompertz curve both beat the logistic in most countries; the logistic is the worst of the four parametric
forms in out-of-sample prediction. The transition, as measured annually, is more often a decelerating decline
than a symmetric S. Second, **the path is near-universal once timing is removed**. Aligned on onset and on the
year when 10% of the fall remains, country curves are almost indistinguishable: the cross-country standard
deviation at each point of the aligned path is about 0.017 on a 0–1 scale, and the first principal component
explains essentially all the residual variance. Third, **the heterogeneity is real but is about
timing, pace and level**, and it has two broad poles: an early, deep, curved class and a late, shallow,
near-linear class. The clustering is better than random partitions but weak in absolute separation, so the
right description is a continuum with two poles, not a taxonomy. Fourth, **mortality-decline timing is the
dominant correlate of transition timing**, with urbanisation at onset associated with earlier transitions and
secondary attainment at onset with longer, more curved declines; the timing of schooling expansion has no
independent association once mortality timing is in the model. This last finding is correlational and the
covariate coverage is uneven, so we state it as a description, not an effect.

The paper also serves as the constructive follow-up to an earlier negative result from the same programme: a
"universal collapse curve" relating fertility to female attainment across countries and cohorts was rejected,
with country effects explaining about 72% of the residual variance. That result said *that* a single curve
fails; this paper says *how* it fails. The answer is not that countries follow different functional paths — the
path is remarkably stable — but that they are shifted horizontally (timing) and vertically (floor), and that
the curvature differs modestly. That decomposition is useful for forecasting, for the model-country approach,
and for the theory of terminal enclosure.

The rest of the paper is organised as follows. Section 2 reviews the shape literature. Section 3 describes the
data. Section 4 sets out the methods. Section 5 reports the results. Section 6 connects the results to the
collapse-curve negative. Section 7 draws implications for forecasting, the model-country approach, policy
timing and the terminal-enclosure claim; Section 8 lists concrete future research; Section 9 states
limitations; Section 10 concludes.

## 2. Prior work on the shape of the transition

### 2.1 Classic transition theory and its S-curve

The classic accounts describe the transition as a sequence — high stationary, early expanding, late expanding,
low stationary — driven by mortality decline followed by fertility decline (Notestein 1945; Davis 1963). The
S-curve enters less as an estimated functional form than as a diagram: fertility falls slowly at first, then
rapidly, then slowly again. Coale's reformulation sharpened the conditions under which a transition occurs and
why its timing differs across societies (Coale 1973), and the model-schedule tradition formalised the age
pattern of childbearing rather than its time path (Coale & Trussell 1974). The most influential quantitative
descendant is the United Nations' projection model, whose double-logistic family imposes a particular
S-shaped path with country-specific parameters (Alkema et al. 2011; Raftery et al. 2014). That model is
explicitly a projection device, not a test of functional form; its parametric family is chosen for
smoothness and for the behaviour of long-run forecasts, not because it has been shown to fit historical
transitions better than alternatives.

### 2.2 The critics: heterogeneity, diffusion and the limits of a single shape

The comparative literature has repeatedly emphasised that transitions differ. Cleland and Wilson's
iconoclastic review argued that demand-side accounts miss the diffusion of ideas and that transition timing
and pace reflect social interaction as much as economic change (Cleland & Wilson 1987). Bongaarts documented
that many developing-country transitions stalled or slowed in the 1990s, contradicting a smooth S-curve
(Bongaarts 2008). Bongaarts and Casterline contrasted the fast transitions of East Asia with the slow
transitions of sub-Saharan Africa and argued that the difference is structural, not a matter of being at a
different point on the same curve (Bongaarts & Casterline 2013). Reher proposed a global-process reading in
which timing clusters by region and historical era (Reher 2004), and Lesthaeghe's second-demographic-transition
account adds a later, distinct regime (Lesthaeghe 2010). Dyson's synthesis treats the transition as a set of
regional sequences rather than one curve (Dyson 2010). The mortality channel has its own literature: improved
survival changes the returns to childbearing and can precede or accompany fertility decline (Cleland 2001;
Soares 2000), which is why mortality timing is a natural candidate for explaining transition timing.

### 2.3 Shape work and what is missing

Two strands come closest to the question of functional form. The projection literature imposes a form and
estimates its parameters (Alkema et al. 2011; Raftery et al. 2014; Ševčíková et al. 2016), but does not
compare forms or test the imposed shape against alternatives. The comparative literature describes types —
early/late, fast/slow, stalled — but does not fit a common set of forms to every country and compare their
parameters on a common scale. We found no prior study that (i) fits several parametric forms plus a flexible
alternative to every transition, (ii) compares them out of sample, (iii) extracts shape descriptors on a common
scale and (iv) tests the resulting clustering against random partitions. That is the gap this paper addresses;
it is a gap of measurement and comparison, not a claim of a new theory.

### 2.4 Measuring shape: known pitfalls

Four measurement problems are well known in this literature, and each is handled explicitly here. First,
**period versus cohort fertility**: period TFR is affected by tempo — births brought forward or postponed —
so a period series can show a "shape" that the cohort series does not. The annual data used here are period
data; this is a limitation (Section 9), and cohort fertility by education is the first priority for extension.
Second, **the start and end of the transition are not observed directly**: the peak and the floor are
constructed, not given. We use a moving average and a transparent rule (95% and 10% of the fall) so that the
construction is reproducible, but different thresholds would move onset and t10 by a year or two without
changing the ordering of countries. Third, **annexation and boundary changes** alter the population to which
the TFR refers and can create spurious curvature; this is a general problem for long country series and is
listed as a limitation rather than corrected. Fourth, **the functional form is partly imposed by the fitting
window**: a logistic fitted to a series that starts at the peak and ends at the floor is not the same object
as one fitted to the whole transition including the pre-transition plateau. With truncated 1960–2023 series
we cannot distinguish a genuinely non-logistic form from a logistic that the window leaves unidentified; a
poor fit in this window is evidence about the estimable window, not a refutation of the S-curve. We address
this by fitting from the full available series and by testing the forms out of sample on the last decade,
which is a harder test than in-sample fit.

### 2.5 What this paper does not claim

Three framings are avoided deliberately. First, we do not claim to be first to notice that transitions differ;
that observation is as old as the literature. Second, we do not claim that the fitted shapes are causal
objects; they are descriptions of time paths. Third, we do not treat the clustering as a typology. If the
clusters are weak, as they are, the continuum is the finding. The contribution is the decomposition: path
versus timing versus pace versus level.

## 3. Data

### 3.1 Fertility

The primary series is the World Bank's annual total fertility rate (TFR) for 1960–2023, pulled fresh from the
World Bank API for this paper (indicator `SP.DYN.TFRT.IN`, all countries, annual, 2024 release). The series is
the standard period TFR and is closely related to the UN's World Population Prospects series that underlies
most comparative work; where the two differ, the differences are small relative to the shape features we
extract. We deliberately do not use the project's earlier server-based panel, so the results do not depend on
that environment. Annual data are essential for shape: a five-year series smooths away the onset and the
curvature we are trying to measure. Cohort fertility is not used here because a complete country–cohort
series was not obtained in this pull; this is a stated limitation and a future-research priority.

### 3.2 Transition sample

Of 217 countries in the World Bank country list, 105 meet a transparent transition rule: at least 40 annual
TFR observations; a peak TFR of at least 4.0 births per woman; a fall from peak to the last-five-year mean of
at least 1.5 births; a floor no higher than 3.2; and an estimated duration between 1 and 70 years. Countries
that never had a high-fertility regime, countries whose transition had not begun by 2023, and city-states and
small territories with short or incomplete series are excluded. The rule is stated rather than tuned; it
produces the expected set of transitions and excludes the expected non-transitions.

### 3.3 Covariates

Covariates were pulled from the same World Bank API for 1960–2023: female life expectancy (`SP.DYN.LE00.FE.IN`),
infant mortality (`SP.DYN.IMRT.IN`), urban population share (`SP.URB.TOTL.IN.ZS`), GDP per capita in PPP terms
(`NY.GDP.PCAP.PP.KD`), female primary completion (`SE.PRM.CUAT.FE.ZS`), and female lower- and upper-secondary
completion (`SE.SEC.CUAT.LO.FE.ZS`, `SE.SEC.CUAT.UP.FE.ZS`). Coverage is uneven by construction: urban shares
are nearly complete (105 countries), the mortality-timing variable is available for 101, the schooling-timing
variable for 90 (with left-censoring at the first observation for countries already past the threshold), and
GDP per capita at onset for only 18 because PPP series mostly begin in 1990, after the onset of early
transitions. We report the coverage for every regression and do not impute.

## 4. Methods

### 4.1 Shape descriptors

For each country we take the peak of a five-year centred moving average of the TFR series and the floor as the
mean of the last five observations. The fall is peak minus floor. Three timing points follow: onset is the
first year at or below 95% of the fall, midpoint the first year at or below 50%, and t10 the first year at or
below 10%. Duration is t10 minus the year at 90% of the fall; speed is the maximum five-year average annual
decline; curvature is the maximum speed divided by the average speed of the whole decline (fall divided by
duration), so that a value above one indicates a mid-transition acceleration (an S-shape) and a value near one
a near-linear or decelerating path. These descriptors are computed from the observed series, not from the
fitted models, so that they are comparable across functional forms.

### 4.2 Competing functional forms

Five forms are fitted by least squares to the country's annual series: a four-parameter logistic decline, a
four-parameter Gompertz decline, a four-parameter exponential decline to a floor (with an onset year), a
four-parameter linear decline with a kink and a floor, and a seven-parameter cubic spline as a flexible
benchmark. Each fitted model is summarised by AIC and BIC on the full series, and by out-of-sample root mean
squared error from fitting on 1960–2012 and predicting 2013–2023. The hold-out is the more important
comparison: it asks which form transports best across a decade, which is the relevant question for
forecasting.

### 4.3 Path uniformity and clustering

To separate the *path* of the decline from its timing, each country's series is resampled on a common grid
between its own onset and its own t10, and normalised to run from one at the peak to zero at the floor. If the
paths differ, the normalised curves spread out; if they agree, they lie on top of each other. We report the
cross-country standard deviation of the aligned curves and the variance explained by their first principal
component.

Clustering uses the six descriptors (onset, midpoint, duration, speed, floor, curvature), standardised.
K-means is fitted for k = 2 to 6 and the number of clusters is chosen by silhouette. To test whether the
clustering is more than an artefact of partitioning, the same countries are randomly partitioned into clusters
of the same sizes 500 times and the silhouette of the real partition is compared with the null distribution;
the reported p-value is the share of random partitions at least as coherent as the real one. This is the same
random-partition discipline used elsewhere in the programme for grouped regressions. A weak silhouette is
reported as a continuum, not hidden behind a cluster count.

### 4.4 Determinants

Shape descriptors are regressed on covariates with robust (HC1) standard errors. The timing covariates are
defined as leads: the schooling-expansion lead is the onset year minus the year female primary completion
reached 50% (left-censored at first observation), and the mortality-decline lead is the onset year minus the
year female life expectancy gained ten years over its first observed value. Level covariates are measured at
onset: urban share, female upper-secondary completion, and log GDP per capita where available. Each descriptor
is regressed on each covariate separately with the available cases, and a multivariate model is attempted on
complete cases; where complete cases are too few, the multivariate model is reported as not estimable rather
than dropped silently. All coefficients are correlations, not causal effects.

## 5. Results

### 5.1 Which functional form wins?

Table 1 reports the model-selection counts and the out-of-sample errors. The S-curve picture is not the best
description of the available annual data.

**Identification caveat, stated first because it bounds every claim in this subsection.** The annual series
begin near the 1960s peak and end in a partial decline, so the lower asymptote and the early phase of the
curve are only partly observed. A logistic fitted to such a window can be *unidentified* rather than wrong:
the data cannot always separate a genuinely non-logistic decline from a logistic whose parameters the window
does not pin down. We therefore read the model comparison as a statement about the **estimable window** — the
exponential-to-floor family describes the available transition data and transports better out of sample —
not as a refutation of the S-curve as a description of the underlying process. The same caveat applies to the
Gompertz and linear-kink results. The exponential decline to a floor is the best-supported form for **51 of 105
countries (49%)**, the Gompertz for **30 (29%)**, the linear-decline-with-kink for **15 (14%)**, the logistic
for **7 (7%)** and the flexible spline for **2 (2%)**. The same ordering appears out of sample: fitting on
1960–2012 and predicting 2013–2023, the average root-mean-squared error is **0.31 births per woman for the
exponential**, **0.36 for the Gompertz**, **0.39 for the linear kink** and **0.48 for the logistic**. The
logistic is not a marginally worse approximation; it is the worst of the four parametric forms on the
criterion that matters for forecasting, and it wins in only seven countries.

Two features of the data explain this. First, the onset of the decline is often abrupt relative to an S-curve:
the logistic's slow first phase is not visible in annual series that begin from a high plateau and start falling
within a few years. Second, the floor is reached gradually and the series then wobbles, so a form that
decelerates smoothly toward a floor (exponential or Gompertz) tracks the last two decades better than a
symmetric S. The Gompertz, which is asymmetric in the other direction (slow early, faster late), does better
than the logistic but less well than the exponential. The linear kink wins where the decline is genuinely
straight, which is more common than the S-curve tradition would suggest.

This is a descriptive result, not an argument against using logistic models in projection. A projection model
optimises different objectives, and a parametric S-curve may still be a useful smoothing device. Nor is it a
refutation of the S-curve as a description of some underlying process: the window cannot tell "not logistic"
from "logistic left unidentified". What the annual series do not support is the stronger claim that the
historical transition *is* an S-shaped curve in a way that an exponential or kinked-linear decline is not.

**Table 1. Functional-form comparison (105 countries, annual TFR 1960–2023).**

| Form | Best by BIC (countries) | Share | Mean hold-out RMSE (births/woman) |
|---|---|---|---|
| Exponential to floor | 51 | 49% | 0.31 |
| Gompertz | 30 | 29% | 0.36 |
| Linear decline with kink and floor | 15 | 14% | 0.39 |
| Logistic (S-curve) | 7 | 7% | 0.48 |
| Cubic spline (flexible benchmark) | 2 | 2% | — |

*Notes:* best form by BIC on the full series; hold-out fits 1960–2012 and predicts 2013–2023; the spline is a
flexible benchmark and is not included in the hold-out comparison. Source:
`results/shape_results.json` → `functional_forms`.

### 5.2 The distribution of shapes

Table 2 gives the distribution of the six descriptors across the 105 transitions. The median transition begins
in **1967** (interquartile range 1964–1970), reaches its midpoint in **1982** (1976–1990), takes **35 years**
from the 90% to the 10% point (28–41), falls at a maximum of **0.19 births per woman per year** (0.157–0.232),
ends at a floor of **1.95** (1.56–2.45), and has a curvature of **1.38** (1.17–1.83) — that is, the fastest
part of the decline is about 1.4 times the average pace. The tenth-to-ninetieth percentile ranges are wide:
onset spans 1963–1977, duration 20–47 years, speed 0.14–0.31 births per woman per year, and the floor
1.37–2.79. These are not small differences around a common curve; they are the dimensions along which
transitions actually differ.

**Table 2. Shape descriptors across 105 transitions (observed-series quantities).**

| Descriptor | Median | IQR | P10 | P90 |
|---|---|---|---|---|
| Onset year (5% of fall) | 1967 | 1964–1970 | 1963 | 1977 |
| Midpoint year (50% of fall) | 1982 | 1976–1990 | 1973 | 1995 |
| Duration, years (90% to 10%) | 35.0 | 28.0–41.0 | 20.4 | 47.0 |
| Speed, max annual decline | 0.190 | 0.157–0.232 | 0.138 | 0.309 |
| Floor TFR (last 5-year mean) | 1.95 | 1.56–2.45 | 1.37 | 2.79 |
| Curvature (max speed / average speed) | 1.38 | 1.17–1.83 | 1.06 | 2.40 |

*Source:* `results/shape_results.json` → `shape_descriptors`; per-country values in
`results/country_descriptors.csv`. Figure 3 plots the distributions.

### 5.3 One path, many timings

Figure 1 shows fitted shapes for representative countries, two per best-fitting form. Figure 4 shows the
aligned curves. Once each transition is resampled between its own onset and the year when 10% of the fall
remains, and normalised to run from one to zero, the curves hardly differ. The cross-country standard
deviation of the aligned curve is **0.017 at every point of the path**, and the mean absolute deviation from
the mean curve is **0.011** on a 0–1 scale. The first principal component of the aligned curves explains
essentially **all** of their variance (the second component is numerically zero), which means that the
variation that remains after alignment is a single, small, common deviation rather than several distinct path
types.

This is the paper's central decomposition. The literature correctly documents enormous heterogeneity, but that
heterogeneity is **horizontal and vertical**, not in the shape of the path: transitions start at different
times, fall at different speeds and depths, and end at different floors, but once those are aligned they follow
the same path. The qualification is important: alignment is partly constructed by definition — any two
monotone declines will look similar when both are normalised between their own endpoints. The informative
part is the *size* of the residual: 0.017 on a 0–1 scale is small relative to the interval between, say, a
linear and an S-shaped path (which would differ by an order of magnitude more at the midpoint). The result is
therefore a statement about magnitude, not a tautology.

This finding also explains the earlier collapse-curve rejection. If a single curve were imposed on the raw
data, country differences in vertical level and horizontal timing would generate exactly the residual
structure that the earlier analysis found: country intercepts and slopes differing while the pooled shape
fit well (R² 0.78 pooled, but 71.6% of the residual variance attributable to country identity). The present
analysis shows where that structure comes from.

### 5.4 Two poles, not a taxonomy

Clustering the six standardised descriptors gives a best solution of **k = 2** by silhouette (**0.275**; k = 3:
0.239; k = 4: 0.260; k = 5: 0.219; k = 6: 0.233). The real partition is more coherent than random partitions of
the same countries into clusters of the same sizes: **0 of 500** random partitions reach the real silhouette
(p < 0.01 by the 1/(500+1) rule). Table 3 gives the cluster profiles. The first class (**58 countries**)
transitions earlier (median onset 1965, midpoint 1977), more deeply (floor 1.68), more slowly in duration
terms (37 years) but with a higher peak speed (0.22 births per woman per year) and more curvature (1.89); it
includes most of Latin America, the Caribbean, and the early transition countries of Asia and Europe. The
second class (**47 countries**) transitions later (onset 1973, midpoint 1991), more shallowly (floor 2.36),
with a shorter duration (30 years) but a lower peak speed (0.19) and less curvature (1.26); it includes most of
sub-Saharan Africa, the later Middle East and South Asia, and several late-transition countries elsewhere.

**Table 3. Transition classes (k = 2, silhouette 0.275; random-partition p < 0.01).**

| Descriptor | Class 1 (early–deep–curved, n=58) | Class 2 (late–shallow–linear, n=47) |
|---|---|---|
| Onset (median) | 1964.7 | 1972.8 |
| Midpoint | 1977.4 | 1990.7 |
| Duration, years | 37.2 | 30.3 |
| Speed, max annual decline | 0.220 | 0.194 |
| Floor | 1.68 | 2.36 |
| Curvature | 1.89 | 1.26 |

*Source:* `results/shape_results.json` → `clustering.cluster_profiles`; cluster assignments in
`results/country_descriptors.csv`; Figure 2 plots the descriptor space.

The honest description is not "two types of transition". A silhouette of 0.28 is weak in absolute terms; it
says the partition is better than chance, not that countries fall into two separated groups. The continuum
reading is the correct one: transitions shade from an early–deep–curved pole to a late–shallow–linear pole, and
the clustering at k = 2 picks the ends of that continuum. Reporting k = 2 with a p-value but without the
silhouette caveat would overstate the typology.

### 5.5 What predicts the shape?

Table 4 reports the available-case regressions of each descriptor on each covariate. Three patterns are
robust across specifications.

**Mortality timing is the strongest correlate of transition timing.** A one-year later ten-year gain in female
life expectancy is associated with a **0.24-year later onset (SE 0.036, n = 101)** and a **0.30-year later
midpoint (SE 0.046, n = 101)**; later mortality decline also predicts a shorter duration (−0.17 years per year,
SE 0.068) and less curvature (−0.014, SE 0.004). The near one-for-one relation is consistent with mortality
decline being part of the same process rather than an external cause: it is a description of co-movement at the
level of countries. Because both variables are timing measures on the same scale, the coefficient is easy to
read: a country whose mortality decline arrived a decade later in relative terms typically began its
fertility transition about 2.4 years later.

**Urbanisation at onset is associated with earlier, faster transitions.** A one-percentage-point higher urban
share at onset is associated with a **0.05-year earlier onset (SE 0.025, n = 105)** and a **0.15-year earlier
midpoint (SE 0.036)**; the onset coefficient is significant at conventional levels and the midpoint coefficient
is strongly significant. The magnitudes are modest but the sign is consistent with an urban transition
occurring earlier in more urban societies.

**Schooling is about level, not timing.** The timing of schooling expansion (the year female primary completion
reached 50%) has no independent association with onset (**0.049 years later per year of lead, SE 0.041,
n = 90**) or midpoint (−0.063, SE 0.085). What does predict shape is the *level* of female secondary completion
at onset: a ten-point higher level is associated with a **2.5-year earlier onset (coefficient −0.246, SE
0.097, n = 30)**, a **5.8-year longer duration** (coefficient +0.583 years per percentage point, SE 0.20),
and **more curvature** (+0.024 per point, SE 0.009) — i.e. higher-attainment countries have longer, more
S-shaped declines. The schooling-level sample is only 30 countries, so this is a hypothesis, not an
established pattern.

**Income could not be tested well.** GDP per capita at onset is available for only 18 transitions, because PPP
series mostly start in 1990 and many onsets are in the 1960s and 1970s. We report the coverage rather than
impute a backcast series.

**Table 4. Correlates of shape descriptors (available-case OLS, robust SE; n in parentheses).**

| Descriptor | Mortality-decline lead (years) | Schooling-expansion lead (years) | Urban share at onset (pp) | Female upper-sec. at onset (pp) |
|---|---|---|---|---|
| Onset year | **0.240 (0.036)**, n=101 | 0.049 (0.041), n=90 | **−0.052 (0.025)**, n=105 | **−0.246 (0.097)**, n=30 |
| Midpoint year | **0.301 (0.046)**, n=101 | −0.063 (0.085), n=90 | **−0.146 (0.036)**, n=105 | **−0.291 (0.116)**, n=30 |
| Duration (years) | **−0.168 (0.068)**, n=101 | −0.072 (0.101), n=90 | −0.042 (0.045), n=105 | **0.583 (0.200)**, n=30 |
| Curvature | **−0.014 (0.004)**, n=101 | −0.004 (0.006), n=90 | 0.000 (0.003), n=105 | **0.024 (0.009)**, n=30 |
| Floor | **0.005 (0.004)**, n=101 | −0.000 (0.006), n=90 | −0.004 (0.003), n=105 | −0.024 (0.017), n=30 |

*Notes:* each cell is a separate regression with an intercept; coefficients in descriptor units per covariate
unit; robust (HC1) standard errors; bold marks the associations discussed in the text. The multivariate
complete-case model is not estimable because GDP coverage reduces it to one observation; the multivariate
model without GDP has n = 25 and is reported in `results/shape_results.json`. Source:
`results/shape_results.json` → `determinants`.

The multivariate model without income (n = 25) leaves the mortality coefficients essentially unchanged
(mortality lead 0.236 on onset, SE 0.041) and the urban coefficient smaller, while the schooling-level
coefficients lose precision. We therefore report the univariate patterns and flag the multivariate model as
underpowered rather than treating it as the headline.

### 5.6 Robustness and descriptor structure

Three checks support the main patterns. First, **the form ranking is the same in-sample and out of sample**:
the exponential is both the most frequent BIC winner (51 countries) and the best form on the last-decade
hold-out (RMSE 0.31), while the logistic is both rare (7 countries) and worst (0.48). A ranking that only
held in-sample would be suspect; this one does not. Second, **the descriptor space is coherent**: the
correlations among the six descriptors have the expected signs. Onset and midpoint correlate at 0.68;
duration correlates negatively with speed (−0.47) and negatively with curvature (0.51 — longer transitions
are more curved); and the floor correlates positively with onset (0.46) and midpoint (0.51), so later
transitions end higher. These correlations are what the two-pole structure summarises. Third, **k = 3 splits
the same continuum rather than overturning it** (silhouette 0.239): the three-class solution separates a very
early, very deep, strongly curved group (35 countries; onset 1964, floor 1.49, curvature 2.17), a very late,
shallow, fast group (23 countries; onset 1978, floor 2.45, curvature 1.21), and a large middle group (47
countries) between them. The k = 2 solution is the more parsimonious summary of the same ordering; we report
k = 3 here so that a reader can see that the choice of k is a summary decision, not an artefact that
manufactures the two-pole reading.

A fourth check is conceptual rather than numerical. The path-uniformity result uses alignment on onset and
t10, which is a strong normalisation; the honest question is whether the residual variation is small enough
to matter. The cross-country standard deviation of 0.017 is small relative to the difference between
alternative paths: a linear decline and an S-shaped decline differ by roughly 0.15 at the midpoint on the
same normalised scale. The residual after alignment is an order of magnitude smaller than a genuine
path difference, which is why we describe the path as near-universal rather than as sharing a family
resemblance. The alignment does, however, absorb information about the *approach* to the endpoints — a
transition that creeps at onset and plunges later is aligned away from one that plunges immediately — so the
claim is best stated as: heterogeneity in the interior shape of the decline is small, not that timing and
pace are unimportant. They are the main story.

## 6. Relation to the "no universal collapse curve" result

An earlier analysis in this programme tested the claim that fertility, as a function of female attainment,
falls on one common curve across countries and cohorts. Using 4,394 country–cohort points (158 countries,
cohorts born 1950–1996), it found that a common exponential fit had R² = 0.78 but that country identity
explained 71.6% of the residual variance, country-specific slopes raised R² to 0.955, and the slope
heterogeneity F-statistic was 46.4 on 313 and 3,717 degrees of freedom; the residual standard deviation was
0.847 births per woman, 11.2% of the fertility range, and remained 0.434 after a country-level rescaling. That
paper said the universal collapse curve is rejected.

The present paper is the constructive follow-up. It explains *why* the collapse fails, and the answer is
unexpectedly benign for the idea of a common transition: countries do not follow different functional paths.
Once aligned, they follow an almost identical one. The collapse fails because countries are **shifted** — in
timing (onset spans two decades or more) and in level (floors range from 1.37 to 2.79) — and because curvature
varies modestly (1.06 to 2.40). A single curve imposed on raw data therefore fits shape but not placement, and
placement dominates the residual. The correct object is a family with a common path and country-specific
shift parameters; that is exactly what the fitted exponential and Gompertz models provide.

This reconciliation matters for how the earlier negative is read. "No universal curve" does not mean "no
common shape"; it means "no common placement". The two claims are compatible, and separating them is the
contribution of this paper.

## 7. Implications

### 7.1 For forecasting

Three implications follow. First, the commonly imposed S-curve is not the best-supported functional form for
historical annual data in this estimable window; an exponential or Gompertz family, or a flexible spline, transports better. Projection
models that impose an S-curve should test the imposed form against these alternatives rather than treating it
as given. Second, because the path is near-universal once timing is fixed, the key forecasting problem is not
the shape of the decline but the **timing and the floor**. Forecast uncertainty should be concentrated on
onset/midpoint timing and on the post-transition level rather than on curvature. Third, the two transition
poles provide a natural donor pool for model-country forecasts: late, shallow transitions resemble each other
more than they resemble the early deep transitions, and borrowing the *shape* from the right pole while
estimating timing from the country's own covariates is a defensible strategy.

### 7.2 For the "model country" approach

The model-country approach uses one country's history as a template for another's future. The results draw a
sharp line: **the shape is transportable, the timing is not**. Aligned curves differ by about 0.017 on a 0–1
scale, so borrowing the path is defensible. Onset and midpoint differ by decades, so borrowing the timing
without re-estimating it would be indefensible. Any model-country exercise should therefore separate the two
operations: take the normalised path from a donor (or from a pooled estimate), and estimate the timing
parameters from the receiving country's own covariates, accepting that the mortality-timing and urbanisation
associations above are only correlational.

### 7.3 For policy timing

If mortality timing and urbanisation are the covariates most strongly associated with transition timing, then
the window in which fertility policy can plausibly bite is set by processes that are not themselves fertility
policy. The correlational pattern suggests that interventions are most likely to matter around the mortality
decline and urban transition, not decades before or after. This is a hypothesis about timing, not an
identified effect; it is offered because policy documents routinely assume a generic S-curve in which the
intervention point is chosen by position in the curve, and the evidence here suggests that position in the
curve is itself mostly a function of mortality and urbanisation timing.

### 7.4 For the theory of terminal enclosure

The programme's theory of terminal enclosure expects high-inhibition systems to approach a terminal state in
which additional scale yields little further functional change. The transition-shape results speak to the
demographic side of that claim in one specific way: the **floor** — the terminal fertility level — varies
substantially (1.37 to 2.79) and is not bound to a single value. If enclosure implies a common terminal state,
the cross-country record does not support a common terminal *level*, only a common terminal *shape*. The
theory's terminal-enclosure prediction should therefore be stated in terms of shape and trajectory, not in
terms of a universal end-point.

### 7.5 What would change our mind

The claims in this paper are falsifiable and we state the tests. The path-uniformity claim would fail if
cohort or subnational data showed materially different aligned paths — for example, a markedly slower start
followed by a steeper interior than the 0.017 spread found here. The functional-form claim would fail if a
properly specified logistic with a flexible floor tracked the annual data as well as the exponential family
in a rolling-origin forecasting evaluation. The two-pole reading would fail if clustering with additional
shape descriptors (for example, the skew of the decline or the duration of the final deceleration) produced
clusters with substantially higher silhouette and a different substantive split. The covariate associations
would fail if within-country or historical data reversed them, or if mortality timing turned out to be
mechanically tied to the TFR series through the tempo effect. None of these tests is run here; they define
the next paper, not a weakness of this one.

## 8. Future research

Four concrete extensions follow directly. First, **cohort fertility by education**: the period TFR used here is
a period measure, and the transition's shape may look different in cohort data, especially where tempo effects
are large; WPP cohort fertility by education is the natural next pull. Second, **subnational shapes**: the
country is a coarse unit, and transitions within large countries (China, India, Brazil, Nigeria) may have
different shapes from the national average; subnational series would let the path-uniformity claim be tested
within countries as well as between them. Third, **historical series for the earliest transitions**: our data
begin in 1960, so the earliest transitions (Britain, France, Sweden, the United States) are left-censored;
historical series from the Human Mortality Database and national statistical yearbooks would test whether the
near-universal path holds for the first transitions or whether the path itself changed over history. Fourth,
**a forecasting horse race**: compare the fitted functional forms against the UN double-logistic and against
simple random-walk benchmarks on a rolling-origin evaluation; the hold-out comparison here is a first step,
not a forecasting evaluation.

## 9. Limitations

The results are descriptive and correlational. Five limitations matter. (i) **Period TFR**: annual period TFR
is affected by tempo and by birth timing; cohort fertility would be the cleaner object for some purposes.
(ii) **Left-censoring**: 1960 start and left-censored schooling timing mean that early transitions and early
schooling expansions are under-observed. (iii) **Coverage**: income at onset is available for only 18
countries and female secondary attainment for 30; the schooling-level results are therefore hypotheses.
(iv) **Clustering**: the two-class solution is better than random but weak in absolute separation; the
continuum reading is the honest one. (v) **No causal identification**: the mortality-timing and urbanisation
coefficients are associations among variables driven by the same historical processes, and reverse causation
is plausible. The paper's claims are about functional form and measurement, not about causes.

## 10. Conclusion

The demographic transition has a shape, and the shape is not quite the one usually drawn. Across 105
countries, annual total fertility in the estimable window is better described as an exponential or Gompertz
decline to a floor than as a logistic S-curve; the logistic is the worst of the four parametric forms out of
sample and wins in only seven countries, though the truncation of the series means this is evidence about the
window rather than a refutation of the S-curve. Once transitions are aligned on their own onset and duration, their paths are almost identical: the
heterogeneity that the comparative literature documents is in timing, pace and floor, not in the path. That
heterogeneity has two poles — early, deep, curved transitions and late, shallow, near-linear ones — which are
better than random partitions but weak enough to describe a continuum. Mortality-decline timing is the
strongest correlate of transition timing; urbanisation at onset is associated with earlier transitions; the
level of female secondary attainment at onset is associated with longer, more curved declines, while the
timing of schooling expansion is not independently associated once mortality timing is accounted for. These
are descriptions, not causes. For forecasting and for the model-country approach, the practical lesson is
simple: borrow the shape, estimate the timing. For the earlier "no universal curve" negative, the lesson is
that a single curve fails not because paths differ but because placements do.

## Data and code availability

Data were pulled fresh from the World Bank API on 25 November 2026 (indicator codes in Section 3); raw pulls,
the analysis script, per-country descriptors, result JSON and four figures are in
`research/records/2026-11-25-paper-shape/`. The analysis is reproducible with `scripts/pull.sh` and
`scripts/analysis.py`; the random seed is 20261125. No data were obtained from the project's server, which was
unavailable. Code and data are released with the paper's repository.

### Figures

**Figure 1.** Fitted shapes for representative transitions, two countries per best-fitting functional form
(observed annual TFR points; best-BIC fit line). The S-curve appears rarely and mostly in the countries where
the logistic is the best of the fitted forms, not as the typical case.

**Figure 2.** Transition classes in the standardised descriptor space (first two principal components, 43% and
26% of variance). Blue: early–deep–curved class (n = 58); orange: late–shallow–linear class (n = 47). The two
poles are visible but overlap, which is why the paper describes a continuum with two ends.

**Figure 3.** Distributions of onset year, duration, maximum annual decline and floor TFR across the 105
transitions (dashed line = median). The spans are wide in every dimension, which is the quantitative content
of "heterogeneity".

**Figure 4.** Left: aligned decline paths (mean ± one standard deviation across countries) — the near-universal
path. Right: mean aligned path by transition class, showing that the classes differ mainly in level and pace,
with little difference in the aligned path itself.

## References

See `refs.md` for the full reference list with Crossref verification status. Key works cited above:
Notestein (1945), Davis (1963), Coale (1973), Coale & Trussell (1974), Cleland & Wilson (1987), Cleland
(2001), Bongaarts (2008), Bongaarts & Casterline (2013), Reher (2004), Lesthaeghe (2010), Dyson (2010),
Alkema et al. (2011), Raftery et al. (2014), Psacharopoulos & Patrinos (2018), Barro & Lee (2013), Soares
(2000), Lee (2003), Henderson (2003), and the programme's earlier scaling and collapse records (cited in
Section 6).
