# Claims → closest prior art (Paper N4, the shape of the demographic transition)

**Author:** cuda-scale. **Search and verification date:** 24–25 November 2026, from the local clone, against
`api.crossref.org` (bibliographic queries) plus web searches for books and reports. Raw Crossref responses are
in `results/../../2026-11-24-paper-scaling/results/doi_*.json` for papers verified earlier in the session; the
shape-specific batch is in `/tmp/doi_shape.json` on the author's machine and its resolved DOIs are listed
below. **Status column:** *replicated* = prior pattern reproduced here; *audit* = prior claim re-tested with
new data or a new comparison; *new measurement* = a quantification the prior literature does not provide in
this form (not a claim of a new theory); *not tested* = prior claim outside what these data can test. **No
"first" is asserted anywhere.**

## Search strategy (recorded as required)

Queries were run as Crossref `query.bibliographic` searches with the full citation as the query string:
"Cleland Wilson Demand theories of the fertility transition", "Reher demographic transition revisited global
process", "Lesthaeghe unfolding story second demographic transition", "Bongaarts fertility transitions
developing countries progress or stagnation", "Bongaarts Casterline sub-Saharan Africa different", "Alkema
probabilistic projections total fertility rate all countries", "Raftery Bayesian population projections United
Nations", "Coale Trussell model fertility schedules", "Davis theory of change and response", "Dyson population
and development demographic transition", "Montgomery Casterline modelling diffusion effects fertility
transition", plus searches for transition-shape clustering and fast/slow transition typologies. The top three
Crossref hits per query were inspected for title/journal/year match; books and reports were checked against
publisher records by web search and are marked as having no Crossref DOI where that is the case. The searches
were aimed at *shape and typology*, not at fertility determinants in general.

## Claim 1 — the transition is (well described by) an S-curve / logistic

| work | what it shows | Crossref status | update |
|---|---|---|---|
| Thompson (1929), *American Journal of Sociology* 34(6):959–975, "Population" | the original three-stage statement | 10.1086/214874 — Crossref ✓ | benchmark |
| Landry (1934), *La révolution démographique* (Sirey) | early French formulation of the transition stages | book; no DOI | benchmark |
| Notestein (1945), "Population — the long view", in *Food for the World* (ed. T. W. Schultz), University of Chicago Press | classic three-stage transition, S-shaped diagram | book chapter; no DOI | benchmark |
| Davis (1963), *Population Index* 29(4):345–366, "The theory of change and response in modern demographic history" | transition as social response, not mechanical curve | 10.2307/2732014 — Crossref ✓ | benchmark |
| Coale (1973), "The demographic transition reconsidered", IUSSP Proceedings | conditions for transition, timing differs | no DOI | benchmark |
| Coale & Trussell (1974), *Population Index* 40(2):185–258, "Model fertility schedules" | formal age schedules, not time path | 10.2307/2733910 — Crossref ✓ | benchmark |
| Alkema, Raftery, Gerland & Clark (2011), *Demography* 48(3):815–839, "Probabilistic projections of the total fertility rate for all countries" | double-logistic S-curve imposed in the UN projection model | 10.1007/s13524-011-0040-5 — Crossref ✓ | **audit target** |
| Raftery, Alkema & Gerland (2014), *Statistical Science* 29(1):1–15, "Bayesian population projections for the United Nations" | same family, Bayesian estimation | 10.1214/13-sts419 — Crossref ✓ | audit target |

**Our status: audit.** The S-curve is not the best-supported form for the estimable annual window: the logistic
wins for 7 of 105 countries and is the worst of four parametric forms out of sample (RMSE 0.48 vs 0.31 for the
exponential). This does not refute the projection literature, whose objective differs, and — because the
1960–2023 series are truncated — it does not refute the S-curve as a description of the underlying process
either: the window cannot distinguish a genuinely non-logistic form from a logistic it leaves unidentified.
The claim is about the estimable window only.

## Claim 2 — transitions differ in type/regime (heterogeneity)

| work | what it shows | Crossref status | update |
|---|---|---|---|
| Cleland & Wilson (1987), *Population Studies* 41(1):5–30, "Demand theories of the fertility transition: an iconoclastic view" | demand accounts incomplete; diffusion matters | 10.1080/0032472031000142516 — Crossref ✓ | replicated direction |
| Chesnais (1992), *The Demographic Transition: Stages, Patterns and Economic Implications* (Oxford University Press) | canonical stage typology incl. fast/slow transitions | 10.1093/oso/9780198286592.001.0001 — Crossref ✓ (book) | benchmark |
| Coale & Watkins (eds.) (1986), *The Decline of Fertility in Europe* (Princeton University Press) | classic regional pattern/shape-typology precedent | 10.1515/9781400886692 — Crossref ✓ (reissue) | benchmark |
| Reher (2004), *Population, Space and Place* 10(1):9–24, "The demographic transition revisited as a global process" | transitions cluster by region/era | 10.1002/psp.313 — Crossref ✓ | replicated |
| Bongaarts (2008), *Studies in Family Planning* 39(4):303–310, "Fertility transitions in developing countries: progress or stagnation?" | many transitions stalled | 10.1111/j.1728-4465.2008.00157.x — Crossref ✓ | replicated (floors vary) |
| Bongaarts & Casterline (2013), *Population and Development Review* 39(2):299–312, "Fertility transition: is sub-Saharan Africa different?" | slow vs fast transitions are structurally different | 10.1111/j.1728-4457.2013.00557.x — Crossref ✓ | replicated (two poles) |
| Lesthaeghe (2010), *Population and Development Review* 36(2):211–251, "The unfolding story of the second demographic transition" | a later distinct regime | 10.1111/j.1728-4457.2010.00328.x — Crossref ✓ | not tested (post-transition) |
| Dyson (2010), *Population and Development: The Demographic Transition* (Zed Books) | transitions as regional sequences | 10.5040/9781350221819 — Crossref ✓ (book) | benchmark |

**Our status: replicated + new measurement.** The heterogeneity is real, but it decomposes into timing, pace
and floor; the aligned path is nearly universal (SD 0.017). Two poles are detected (silhouette 0.275; random
partition p < 0.01), and described honestly as a continuum.

## Claim 3 — the transition is a universal/global process

| work | what it shows | Crossref status | update |
|---|---|---|---|
| Notestein (1945) | transition as universal sequence | book; no DOI | benchmark |
| Davis (1963) | change-and-response reformulation | 10.2307/2732014 — Crossref ✓ | benchmark |
| Reher (2004) | global process with regional timing | 10.1002/psp.313 — Crossref ✓ | partially replicated |
| Dyson (2010) | regional sequences of a global process | 10.5040/9781350221819 — Crossref ✓ | partial |
| Bongaarts & Casterline (2013) | limits of universality (slow transitions) | 10.1111/j.1728-4457.2013.00557.x — Crossref ✓ | replicated in the negative direction |

**Our status: audit.** Universality holds for the *path* once timing is aligned; it fails for *placement*
(onset spans two decades, floors 1.37–2.79). The correct object is a common path with country-specific shift
parameters.

## Claim 4 — diffusion/social interaction shapes transition timing and pace

| work | what it shows | Crossref status | update |
|---|---|---|---|
| Cleland & Wilson (1987) | diffusion of ideas, not only demand | 10.1080/0032472031000142516 — Crossref ✓ | context |
| Bongaarts & Watkins (1996), *Population and Development Review* 22(4):639–682, "Social interactions and contemporary fertility transitions" | social-interaction/diffusion model of transition timing and pace; the rival to mortality/demand explanations when timing is the outcome | 10.2307/2137804 — Crossref ✓ | not directly tested; mortality-timing association is consistent with it but is not a test |
| Montgomery & Casterline (1993), *Population Studies* 47(3):457–479, "The diffusion of fertility control" / "Modelling diffusion effects in fertility transition" | formal diffusion models of transition | 10.1080/0032472031000146786 — Crossref ✓ | not directly tested |
| Reher (2004) | regional timing clusters consistent with diffusion | 10.1002/psp.313 — Crossref ✓ | context |

**Our status: not tested.** The mortality-timing and urbanisation associations are reduced-form correlations
consistent with diffusion (and with many other mechanisms); they are not a test of diffusion.

## Claim 5 — mortality decline precedes/enables fertility decline

| work | what it shows | Crossref status | update |
|---|---|---|---|
| Cleland (2001), "The effects of improved survival on fertility: a reassessment", *Population and Development Review* 27 (supplement) | survival improvement as a fertility-decline driver | no DOI verified in this pass (standard citation) | context |
| Soares (2000), *Journal of Development Economics* 62(1):1–23, "Mortality decline, human capital investment, and economic growth" | mortality decline raises human-capital investment | 10.1016/s0304-3878(00)00073-0 — Crossref ✓ | context |
| Lee (2003), *Journal of Economic Perspectives* 17(4):167–190, "The demographic transition: three centuries of fundamental change" | mortality-first transition narrative | 10.1257/089533003772034943 — Crossref ✓ | benchmark |
| Davis (1963) | mortality decline as the trigger of response | 10.2307/2732014 — Crossref ✓ | benchmark |

**Our status: replicated as a correlation.** Mortality-decline timing is the strongest correlate of onset
(0.24 years later per year of lead, SE 0.036, n = 101) and midpoint (0.30, SE 0.046). Not causal.

## Claim 6 — schooling/education drives the transition

| work | what it shows | Crossref status | update |
|---|---|---|---|
| Barro & Lee (2013), *Journal of Development Economics* 104:184–198, "A new data set of educational attainment" | education–income–fertility cross-country associations | 10.1016/j.jdeveco.2012.10.001 — Crossref ✓ | benchmark |
| Psacharopoulos & Patrinos (2018), *Education Economics* 26(5):445–458, "Returns to investment in education" | stable returns; education as human capital | 10.1080/09645292.2018.1484426 — Crossref ✓ | benchmark (returns, not transitions) |
| Cleland & Wilson (1987) | demand-side schooling accounts incomplete | 10.1080/0032472031000142516 — Crossref ✓ | context |
| Dyson (2010) | education in the transition narrative | 10.5040/9781350221819 — Crossref ✓ | context |

**Our status: weak level association, timing null.** Female secondary attainment at onset (n = 30) is associated
with earlier onset and longer, more curved declines; the timing of schooling expansion has no independent
association once mortality timing is in the model (0.049, SE 0.041, n = 90). Stated as a hypothesis given
coverage.

## Claim 7 — fast and slow transitions are distinct types

| work | what it shows | Crossref status | update |
|---|---|---|---|
| Bongaarts (2008) | stalled/slow transitions contradict an S-curve | 10.1111/j.1728-4465.2008.00157.x — Crossref ✓ | replicated |
| Bongaarts & Casterline (2013) | sub-Saharan African slow transitions as a distinct regime | 10.1111/j.1728-4457.2013.00557.x — Crossref ✓ | replicated |
| Chesnais (1992) | canonical fast/slow and stage typology | 10.1093/oso/9780198286592.001.0001 — Crossref ✓ | benchmark |
| Reher (2004) | regional/era typology | 10.1002/psp.313 — Crossref ✓ | replicated |

**Our status: two poles, reported as a continuum.** The late–shallow–linear class (47 countries) matches the
"slow/late" type; the early–deep–curved class (58 countries) matches the classic fast transition. The
silhouette (0.275) does not support a strong typology.

## Claim 8 — has anyone clustered transition shapes?

We did not locate a prior study that (i) fits several parametric forms plus a flexible benchmark to every
country's annual series, (ii) compares them out of sample, (iii) extracts shape descriptors on a common scale
and (iv) tests a clustering against random partitions. The closest bodies of work are the projection models
(Alkema et al. 2011; Raftery et al. 2014), which impose a form; the typological accounts (Reher 2004;
Bongaarts & Casterline 2013; Dyson 2010), which describe types; and the model-schedule tradition (Coale &
Trussell 1974), which formalises the age pattern rather than the time path. **Absence of a located prior study
is not proof that none exists**; the search strategy above is documented so a reader can extend it. We do not
claim to be first, and the paper is framed as a measurement/audit contribution.

## Framing statement for integration

This is a replication and measurement paper. Its contribution is a decomposition (path vs timing vs pace vs
floor), a formal comparison of functional forms on annual data, and a random-partition test of shape
clustering. None of these is a new theory of the transition, and none of the covariate associations is a causal
effect.
