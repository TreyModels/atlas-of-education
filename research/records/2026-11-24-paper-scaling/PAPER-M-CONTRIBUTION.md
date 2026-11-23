# Paper M contribution — sections "Scaling laws + θ/γ" and "Massification drivers null"

**Author:** cuda-scale. **For:** Paper M (task-37, lead panel-matrix). **Length:** ≈1,250 words (scaling
≈920; drivers ≈330). **Fuller standalone draft:** `SECTION-M-scaling-and-drivers.md` (≈3,400 words).
**Traceability:** every number carries its branch @ commit and file field, and is listed in `SOURCES.md`.
**Framing:** replication and audit, not discovery; no causal identification is claimed anywhere.

## Scaling laws and the θ/γ programme

We tested the canonical scaling laws and the project's θ/γ extension against education and development
data, with pre-registered tests (`research/scaling-2026-11-23` @ `fd691a6`; `research/scaling-data-hunt-
2026-11-23` @ `9e15b6d`; catalogue `cfe372f`; scan `fd4cfd2`). Four things were measurable, and one was
not.

**Occupational diversity (Heaps).** Raw category counts are a sampling artefact: regressing the number
of distinct occupational categories on workforce size gives a slope of −0.002 (branch `scaling` @
`fd691a6`, `results/scaling_results.json` → `sections.heaps.raw_count_vs_workforce_exponent`). The honest
object is the rarefaction curve — expected distinct categories at a common sample size. On those curves,
the Heaps exponent is **0.333 (SE 0.011, 151 countries, 11,712 points; per-country median 0.374 [IQR
0.319–0.468])**, strongly sublinear (proportional growth rejected, z = −58.8) but **below the 0.4–0.6
literature band** (z = −5.9 against 0.4) (`sections.heaps`). A one-curve-per-country bootstrap gives
0.349 (95% CI 0.331–0.368; `results/heaps_groups.json` → `overall`), so the estimate is resampling-robust
but depth-limited: the public ILOSTAT API now serves only one-digit ISCO categories (ten groups), and that
ceiling pushes the exponent down. Sublinear diversity replicates; the literature value does not.

**No regime break at universalisation.** The accumulation curve has negative curvature, c = −0.058 (SE
0.0018) (`results/regime_break.json` → `curvature`), consistent with saturation. But splitting countries
by female secondary attainment yields exponents of 0.360 (27 countries, <50%), 0.403 (24, 50–80%) and
0.387 (85, >80%): **no significant difference** (Welch t = −1.25, p = 0.22; `threshold_split`). The
pre-registered threshold-break claim fails: curvature yes, break no.

**Education–income exponents are cross-sectional, not laws of change.** In the prior 30-country panel,
most education–income relations that look like scaling laws between countries weaken or vanish inside
them: secondary enrolment vs income 0.215 (SE 0.035) between vs 0.090 (0.124) within; upper-secondary
attainment 0.312 (0.052) vs 0.072 (0.167); education stock vs output 1.176 (0.258) vs 0.051 (0.108);
cohort size vs enrolment −0.612 (0.127) vs −0.006 (0.219) (`results/consolidated_verdicts.csv`; source
table in `data/scaling_laws.csv`, copied from the local massification project). Only tertiary enrolment
(0.567/0.848), lower-secondary completion (0.169/0.247), services share (0.294/0.275) and urban share vs
enrolment (0.012/0.011, semi-log) survive both layers; the project's five-estimator rule independently
calls three relations stable (secondary GER, tertiary GER, lower-secondary completion vs GDP per capita),
14 regularities and one unidentified (`data/scaling_classification.csv`). Cross-country gradients are
not a law of growth.

**Urbanisation vs income is an S-curve, not a power law.** A logistic beats a power law and a straight
line out of sample (RMSE in urban-share units 0.1523 / 0.1598 / 0.1532; slope 0.572, SE 0.030; 10,986
country-years, 208 countries; midpoint about $3,647; `sections.urban_income`). A functional-form
regularity, not a scaling law with an exponent.

**Rank–size and gravity: weak and partial replications.** From a rescued city list (GeoNames; 22,465
cities in 55 countries with at least 50 cities), the median rank–size exponent is **0.859 (bootstrap 95%
CI 0.746–0.978)**; Wilcoxon against 1 does not reject (p = 0.23), but only 27% of countries lie in
0.8–1.2 and the source lists localities, not UN agglomerations (branch `scaling-data-hunt` @ `9e15b6d`,
`results/zipf.json`). For migration, PPML with origin and destination fixed effects on 8,020 country
pairs gives a **distance elasticity of −0.970 (SE 0.076)**; OLS gives −1.306 (0.053); size elasticities
are ≈0.5, not the benchmark ≈1 (`results/gravity.json`). The pair matrix sums to 282 million against the
published 281 million, so the data are coherent; the result is a partial, correlational replication.

**The negative result: no universal fertility–attainment collapse.** The theory's strongest scaling
claim — fertility on one common curve of female attainment across countries and cohorts — is **rejected**.
Using 4,394 country–cohort points (158 countries, cohorts 1950–1996), the best common exponential fits
with R² = 0.78, but country identity explains **71.6% of the residual variance**, country-specific slopes
raise R² to 0.955, slope heterogeneity is F = 46.4 (313, 3,717 df), and the residual SD is 0.847 births per
woman (11.2% of the range; 0.434 after a country-level rescale). Residuals are structured — low-income
countries +0.40, high-income −0.11; 1950s cohorts +0.29, 1970s −0.17. Between countries the
fertility–attainment slope is −0.479; within countries at levels −0.299 (SE 0.026); for ten-year changes
only **−0.056** (2,064 changes, 201 countries) (`sections.collapse`; `consolidated_verdicts.json` →
`levels_vs_changes`). A common shape with country-specific levels, not a universal law.

**θ/γ are not estimable.** They are latent model parameters, not observed country variables. Our
observable implication (sublinear diversity) holds, but estimating θ and γ needs two- to three-digit
category depth, which is unavailable, plus credential counts, which are not held. Using income group and
region as explicitly labelled proxies, the exponent does not vary (income means 0.343–0.355, Kruskal
p = 0.75; region 0.281–0.400, p = 0.26; `results/heaps_groups.json`). That is not a test of θ/γ; the
honest verdict is **not estimable**.

**Data walls.** Bettencourt's urban output and infrastructure exponents (β ≈ 1.15 / 0.85) remain untested
because there is no city-level output, wage, patent or infrastructure data: UN WUP files returned 404, the
UN Data Portal API exposes city data only as size-class aggregates, and BEA regional archives failed with
HTTP 000. Credential inflation is untested because BLS SOC/OES returned HTTP 403 and the Credential Engine
registry returned a 403 Cloudflare challenge. Gibrat needs two city-population waves and is untested
(`results/pull_log.json`, branch `scaling-data-hunt` @ `9e15b6d`). These are stated as gaps, not proxied.
The literature values are benchmarks; the paper must not describe them as tested here.

**What scaling laws can and cannot prove.** They can benchmark whether a relation has a stable functional
form and whether our data are consistent with a claimed exponent. They cannot identify a mechanism, a
cause or a policy lever; they cannot be transplanted from cities to schooling; and a between-country
exponent cannot be read as a law of within-country change. The audit verdict is that the canonical laws
are useful diagnostic benchmarks, not established quantitative laws of education and development.

## Massification drivers: a small set of nulls

The massification-driver matrix has **272 links** (17 measures, ten-year changes, country and decade
effects, clustered errors, with and without country trends), each re-estimated inside 50 real groupings
and **400 random re-partitions** of the same countries — the chance yardstick (`research/
grouping-multiverse-400-2026-11-23` @ `1152cec`, record README and `results/headline.json`). The run is
deterministic (three replicates and the real pass bit-identical), reproduces the earlier 74-draw
classification exactly, and is stable to half-splits (p rank correlation 0.994).

**No driver is robust everywhere.** Of 272 links, 5 are robust in every kind of grouping, 76 are
group-specific, 30 beat random without a clear group, and **161 are no better than random**. With the
better-estimated null, 46 links beat random (42 of the old 43 survive, 1 dies, 4 are new), 20 are worse,
and 32 show more sign-flipping than chance. The large null remainder is not a power artefact: none of the
previously null links is above the 400-draw ceiling.

**Electricity: strong first pass, contingent after trends.** Electricity is zero in the whole sample once
country trends are allowed, and 11 of its 32 links show more sign-flipping than random groupings — the
most of any driver — while a cluster of schooling links beats random only in specific classes. It is a
weak, group-dependent driver, not a universal lever.

**Paid employment: the cleanest null.** No wage-employment link to a schooling outcome beats random
groupings in any kind of group. Because the test is not a pooled coefficient but "no group-based
evidence above chance across 400 partitions", this is a result: paid-employment expansion alone does not
reliably lead schooling expansion in these data.

**The two robust fertility links.** Child mortality → birth rate is significant in 95% of real groups
(random-group median 93%) and life expectancy → birth rate in 81% (random median 93%). These are claims
of a *uniform* effect, so the correct comparison is similarity to the random distribution; both are
statistically indistinguishable from it, survive the halves test, and do not change class. Most other
fertility links are group-specific or no better than random.

**What the nulls mean.** The resolution is part of the result: with 400 draws the empirical p floor is
1/401, a lone link would need about 5,440 draws, and certification of the 30-link ceiling cluster yields
35 up and 19 down links (Benjamini–Hochberg step-up; the exact counts are provisional under positive
dependence, and named groups are descriptions, not certified claims). For the massification argument the
matrix supports a synthesis in which massification is institution- and state-led in late-industrialisers
and demand-led only where industrialisation came first — not a universal law driven by any single variable.

## References for this contribution

DOI-verified (Crossref ✓, checked 24 Nov 2026 against `api.crossref.org`; raw responses in
`results/doi_verified*.json`): Bettencourt et al. 2007 PNAS 10.1073/pnas.0610172104; Bettencourt 2013
Science 10.1126/science.1235823; Bettencourt & West 2010 Nature 10.1038/467912a; Bettencourt & Lobo 2016
J R Soc Interface 10.1098/rsif.2016.0005; Ortman et al. 2014 PLoS ONE 10.1371/journal.pone.0087902;
Ortman et al. 2015 Sci Adv 10.1126/sciadv.1400066; Arcaute et al. 2015 J R Soc Interface
10.1098/rsif.2014.0745; Leitão et al. 2016 R Soc Open Sci 10.1098/rsos.150649; Cottineau et al. 2017
PLoS ONE 10.1371/journal.pone.0183919; Malevergne et al. 2011 Phys Rev E 10.1103/PhysRevE.83.036111;
Petersen et al. 2012 Sci Rep 10.1038/srep00313; Tria et al. 2014 Sci Rep 10.1038/srep05890; Yang et al.
2026 PNAS 10.1073/pnas.2509729123; Beine et al. 2016 World Economy 10.1111/twec.12265; Abel & Cohen 2019
Sci Data 10.1038/s41597-019-0089-3; Rozenfeld et al. 2008 PNAS 10.1073/pnas.0807435105; Barro & Lee 2013
J Dev Econ 10.1016/j.jdeveco.2012.10.001; Psacharopoulos & Patrinos 2018 Education Economics
10.1080/09645292.2018.1484426; Bils & Klenow 2000 AER 10.1257/aer.90.5.1160; Henderson 2003 J Econ Growth
10.1023/A:1022860800744; Lee 2003 J Econ Perspect 10.1257/089533003772034943; Brewster & Rindfuss 2000
Annu Rev Sociol 10.1146/annurev.soc.26.1.271; Soares 2000 J Dev Econ 10.1016/s0304-3878(00)00073-0;
Dinkelman 2011 AER 10.1257/aer.101.7.3078; Boppart et al. 2014 Econometrica 10.3982/ecta11354; Spence
1973 QJE 10.2307/1882010; Schofer & Meyer 2005 Am Sociol Rev 10.1177/000312240507000602.

No Crossref DOI (standard citations, not DOI-verified): Zipf 1949 (book); Gibrat 1931 (book); Heaps 1975
(book); Trow 1973 (report); Holehouse et al. 2025 (arXiv:2509.14468); Hanushek & Woessmann 2012 (NBER
WP 14633; published version not independently checked in this pass). Full list: `refs.md`; claim-by-claim
prior art with "new vs replicated": `claims-prior-art.md`.
