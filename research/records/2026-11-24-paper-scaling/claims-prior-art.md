# Claims → closest prior art (Paper M sections 5–6)

**Author:** cuda-scale. **Verification:** every DOI below was queried against `api.crossref.org` from the
local clone on 24 Nov 2026; raw responses are in `results/doi_verified.json`, `results/doi_verified2.json`,
`results/doi_batch3.json`. "Crossref ✓" = resolved and title/journal matched. Books and arXiv preprints have
no Crossref DOI and are marked accordingly — they are standard citations, not verified DOIs.
**Status column means:** *replicated* = prior result reproduced here; *audit* = existing claim re-examined with
a new test or new data; *new negative* = a claim tested and not supported; *benchmark* = literature value we
could not test. No claim in this section is presented as a discovery, and no "first" is asserted.

## Claim 1 — functional/occupational diversity grows sublinearly (Heaps)

| work | what it shows | update |
|---|---|---|
| Heaps (1975), *Information Retrieval: Computational and Theoretical Aspects* (book; no DOI) | original sublinear distinct-category growth | benchmark: 0.4–0.6 |
| Petersen, Tenenbaum, Havlin & Stanley (2012), Sci Rep 2:313, DOI 10.1038/srep00313 (Crossref ✓) | scaling regularities in word use (Heaps-type) | replicated direction |
| Tria, Loreto, Servedio & Strogatz (2014), Sci Rep 4:5890, DOI 10.1038/srep05890 (Crossref ✓) | generative model of correlated novelties behind category growth | replicated direction |
| Yang et al. (2026), PNAS, DOI 10.1073/pnas.2509729123 (Crossref ✓); arXiv 2208.06487 | function diversity vs size; θ/γ formalism | our observable implication tested |

**Our status: audit + replication.** b = 0.333 (SE 0.011), 151 countries, 11,712 rarefied points: sublinear
replicated; *below* the benchmark (z = −5.9 vs 0.4). New observation is the 1-digit ISCO depth limit, not a new law.

## Claim 2 — a regime change at the universalisation threshold

| work | what it shows | update |
|---|---|---|
| Trow (1973), *Problems in the Transition from Elite to Mass Higher Education* (report; no DOI) | elite/mass/universal thresholds | benchmark |
| Schofer & Meyer (2005), Am Sociol Rev 70(6), DOI 10.1177/000312240507000602 (Crossref ✓) | worldwide higher-education expansion | benchmark |
| Yang et al. (2026), PNAS, DOI 10.1073/pnas.2509729123 (Crossref ✓) | saturating regime at high inhibition | our test target |

**Our status: new negative.** Curvature −0.058 (SE 0.0018) but threshold split not significant
(0.360 / 0.403 / 0.387; Welch p = 0.22). No universalisation break in occupational category richness.

## Claim 3 — education–income "scaling laws"

| work | what it shows | update |
|---|---|---|
| Barro & Lee (2013), J Dev Econ 104, DOI 10.1016/j.jdeveco.2012.10.001 (Crossref ✓) | cross-country education–income association | replicated between countries |
| Psacharopoulos & Patrinos (2018), Education Economics 26(5), DOI 10.1080/09645292.2018.1484426 (Crossref ✓) | stable Mincer returns, ~8.8% | benchmark |
| Bils & Klenow (2000), Am Econ Rev 90(5), DOI 10.1257/aer.90.5.1160 (Crossref ✓) | schooling–growth link | benchmark |
| Hanushek & Woessmann (2012), NBER WP 14633 (working paper; published version not Crossref-checked here) | cognitive skills vs growth | benchmark |

**Our status: audit.** Between-country exponents replicate; within-country ones shrink toward zero
(secondary GER 0.215→0.090; attainment 0.312→0.072; education stock 1.176→0.051). The between/within gap is
the audit finding, not a discovery.

## Claim 4 — urbanisation vs income is an S-curve, not a power law

| work | what it shows | update |
|---|---|---|
| Henderson (2003), J Econ Growth, DOI 10.1023/A:1022860800744 (Crossref ✓) | urbanisation–income relation, large-city bias | benchmark |
| Lee (2003), J Econ Perspect 17(4), DOI 10.1257/089533003772034943 (Crossref ✓) | demographic transition context | benchmark |

**Our status: audit.** Logistic beats power law out of sample (RMSE 0.1523 vs 0.1598; slope 0.572, SE 0.030;
10,986 country-years, 208 countries; midpoint $3,647). Functional-form result; no single exponent.

## Claim 5 — Zipf rank–size for city populations

| work | what it shows | update |
|---|---|---|
| Zipf (1949), *Human Behavior and the Principle of Least Effort* (book; no DOI) | rank–size ≈ 1 | benchmark |
| Malevergne, Pisarenko & Sornotte (2011), Phys Rev E 83:036111, DOI 10.1103/PhysRevE.83.036111 (Crossref ✓) | Pareto vs lognormal test on city sizes | contested benchmark |
| Arcaute et al. (2015), J R Soc Interface 12:20140745, DOI 10.1098/rsif.2014.0745 (Crossref ✓) | boundary definitions change exponents | critique replicated |
| Leitão et al. (2016), R Soc Open Sci 3:150649, DOI 10.1098/rsos.150649 (Crossref ✓) | scaling nonlinearity test | critique replicated |
| Cottineau et al. (2017), PLoS ONE 12(9):e0183919, DOI 10.1371/journal.pone.0183919 (Crossref ✓) | dynamic meta-analysis of city-size distributions | benchmark |

**Our status: replication (weak).** Median ζ = 0.859 (CI 0.746–0.978; 55 countries, 22,465 cities); consistent
with 1 (p = 0.23), not a confirmation; crowdsourced localities, not UN agglomerations.

## Claim 6 — gravity for migration

| work | what it shows | update |
|---|---|---|
| Beine, Bertoli & Fernández-Huertas Moraga (2016), World Economy 39(4), DOI 10.1111/twec.12265 (Crossref ✓) | gravity practice for migration | benchmark: distance ≈ −1 to −2 |
| Abel & Cohen (2019), Sci Data 6:96, DOI 10.1038/s41597-019-0089-3 (Crossref ✓) | bilateral migration flow estimates | data benchmark |
| Rozenfeld et al. (2008), PNAS 105(48), DOI 10.1073/pnas.0807435105 (Crossref ✓) | city growth scaling (Gibrat context) | benchmark (not tested) |

**Our status: replication (partial).** PPML FE distance −0.970 (SE 0.076), 8,020 pairs; OLS FE −1.306 (0.053);
size elasticities ≈0.5 vs benchmark ≈1. Correlational.

## Claim 7 — Bettencourt urban output/infrastructure scaling

| work | what it shows | update |
|---|---|---|
| Bettencourt, Lobo, Helbing, Kühnert & West (2007), PNAS 104(17), DOI 10.1073/pnas.0610172104 (Crossref ✓) | β ≈ 1.15 socioeconomic, ≈0.85 infrastructure | **benchmark only — untested** |
| Bettencourt (2013), Science 340:1438, DOI 10.1126/science.1235823 (Crossref ✓) | network derivation | benchmark only |
| Bettencourt & West (2010), Nature 467:912, DOI 10.1038/467912a (Crossref ✓) | synthesis | benchmark only |
| Bettencourt & Lobo (2016), J R Soc Interface 13:20160005, DOI 10.1098/rsif.2016.0005 (Crossref ✓) | exponents vary across Europe | critique |
| Ortman, Cabaniss, Sturm & Bettencourt (2014), PLoS ONE 9(2):e87902, DOI 10.1371/journal.pone.0087902 (Crossref ✓) | settlement scaling in ancient society | benchmark only |
| Ortman et al. (2015), Sci Adv 1:e1400066, DOI 10.1126/sciadv.1400066 (Crossref ✓) | increasing returns in ancient settlements | benchmark only |

**Our status: not testable.** No city-level output/wages/patents/infrastructure; all known sources blocked
(WUP 404, UN Data Portal no city rows, BEA HTTP 000). Stated as a data wall, not proxied.

## Claim 8 — universal fertility–attainment collapse curve

| work | what it shows | update |
|---|---|---|
| Lee (2003), J Econ Perspect 17(4), DOI 10.1257/089533003772034943 (Crossref ✓) | transition with country-specific timing | prior expectation of heterogeneity |
| Brewster & Rindfuss (2000), Annu Rev Sociol 26, DOI 10.1146/annurev.soc.26.1.271 (Crossref ✓) | fertility–employment relation is context-dependent | prior expectation |
| Soares (2000), J Dev Econ 63(1), DOI 10.1016/s0304-3878(00)00073-0 (Crossref ✓) | mortality decline and human capital | prior expectation |

**Our status: new negative.** No universal collapse: 4,394 country–cohort points, 158 countries; common
exponential R² = 0.78 but country effects explain 71.6% of the residual, slope F = 46.4, residual SD 11.2% of
range; ten-year change slope −0.056 vs between-country −0.479. A common shape with country-specific levels.

## Claim 9 — θ/γ formalism

| work | what it shows | update |
|---|---|---|
| Yang et al. (2026), PNAS, DOI 10.1073/pnas.2509729123 (Crossref ✓) | θ/γ function-diversity model | target |
| Holehouse et al. (2025), arXiv:2509.14468 (arXiv; no DOI) | generative category-growth model | target |
| Tria et al. (2014), Sci Rep 4:5890, DOI 10.1038/srep05890 (Crossref ✓) | novelty-driven category growth | related |

**Our status: not estimable.** θ and γ are latent model parameters; 2–3 digit ISCO unavailable, credential
counts unavailable. Sublinear diversity (0.333) is consistent with the model but does not identify θ/γ.

## Claim 10 — massification drivers (Paper M section 6)

| work | what it shows | update |
|---|---|---|
| Dinkelman (2011), Am Econ Rev 101(7), DOI 10.1257/aer.101.7.3078 (Crossref ✓) | rural electrification effects are context-dependent | consistent with our electricity result |
| Brewster & Rindfuss (2000), DOI 10.1146/annurev.soc.26.1.271 (Crossref ✓) | fertility–employment context dependence | consistent |
| Lee (2003), DOI 10.1257/089533003772034943 (Crossref ✓) | mortality/transition links | consistent (robust fertility links) |
| Boppart, Krusell, Mitman & Violante (2014), Econometrica 82(6), DOI 10.3982/ecta11354 (Crossref ✓) | structural change / relative prices | benchmark (other sections) |
| Spence (1973), Q J Econ 87(3), DOI 10.2307/1882010 (Crossref ✓) | signalling | benchmark (credential section) |
| Collins (2019), *The Credential Society* (book; DOI 10.7312/coll19234, Crossref ✓) | credentialism | benchmark (credential section) |

**Our status: audit / new nulls.** 272 links × 400 random groupings: nothing robust everywhere; electricity
dies under country trends; paid employment is a clean null; child mortality and life expectancy are the only
robust fertility links. The multiverse design, not a new coefficient, is the contribution.
