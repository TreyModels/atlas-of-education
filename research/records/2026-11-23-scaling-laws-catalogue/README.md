# Scaling laws catalogue and testability audit — urbanisation and development

Worker `novelty-review`, branch `research/scaling-laws-catalogue-2026-11-23`, 23 November 2026. Task-20.
For Dr. Menefee's request: list the standard urbanisation/development scaling laws and test for them in our data.
This is a catalogue and a feasibility audit, not a test result. `[verified URL]` = a search result pointed at the
work itself; `[unverified]` = standard citation not URL-confirmed today. Exponents are the literature's typical
values, not ours.

## The action table

| Law / candidate | Literature exponent (range) | Data needed | Feasible here? | How to test |
|---|---|---|---|---|
| **Urban superlinear scaling** — city output, wages, patents, crime (`Bettencourt et al. 2007 PNAS` [verified URL: pnas.org/doi/10.1073/pnas.0610172104]; `Bettencourt 2013 Science` [verified URL: science.org/doi/10.1126/science.1235823]) | total output β ≈ **1.15** (1.01–1.27); per-capita ≈ size^0.15 | city populations **plus city-level output/wages/patents** | **NO** — binding gap: no city-level output data | Cross-sectional log-log regression of city output on city population, with country fixed effects; not possible with what we have |
| **Urban sublinear infrastructure** — roads, cables, utilities (`Bettencourt 2007` [verified]; built-mass study [verified URL: nature.com/articles/s44284-026-00532-x]) | infrastructure β ≈ **0.85** (0.78–0.92) | city populations **plus infrastructure stock by city** | **NO** — no city infrastructure stock | Same log-log design on infrastructure per city; needs new data |
| **Zipf / rank-size** for city populations (`Zipf 1949` [unverified]; deviations contested, e.g. Turkey concavity [verified URL: m2.mtmt.hu record]; "Beyond the power law" [verified URL: ScienceDirect S0198971506001025]) | Pareto α ≈ **1** (0.8–1.2 typical; rejects often) | city populations by country | **YES** — UN World Urbanization Prospects city file [verified URL: population.un.org/wup/downloads?tab=Cities] | Per country, regress log(rank) on log(population) for cities above a size floor; report α by country and region; test concavity |
| **Gibrat's law** — growth independent of size (`Gibrat 1931` [unverified]; city applications e.g. [verified URL: ScienceDirect S016517651400278X]) | growth ~ size^≈0 (weak negative in practice) | city populations at **two or more dates** | **PARTIAL** — WUP has historical agglomerations but boundary changes | Regress log growth on log initial size for cities present in both years; report the size-growth slope and boundary caveats |
| **Kleiber / biological allometry** (`West, Brown & Enquist 1997 Science` [unverified]; reviews [verified URL: besjournals 2008]) | metabolic rate ~ mass^**0.75** | biological/individual metabolism | **NO** (not a social law) | Only as a conceptual analogy; do not test on social data |
| **Heaps' law** — distinct categories grow sublinearly with sample (`Heaps 1978` [unverified]; deviations [verified URL: nature.com/articles/srep01082]) | distinct categories ~ sample^**0.4–0.6** | occupation/industry categories per country with sample sizes (ILOSTAT; ILO ISCO) | **PARTIAL** — ILOSTAT occupation data downloadable | Per country-year: number of distinct 2- or 3-digit occupations vs employment (or survey sample); slope of log categories on log sample |
| **Lotka / Price laws** — productivity concentration (`Lotka 1926` [unverified]; `Price 1963` [verified URL: ScienceDirect 0306457388900490]) | Lotka: inverse-square; Price: half the output from √N authors | author/patent/publication microdata | **NO** — we hold no bibliometric or patent microdata | Needs a publication/patent database; not a country-panel test |
| **Firm / organisation scaling** — sales vs employees ≈1; overhead ≈0.85 (`company scaling` [verified URL: research.chalmers.se]; `multidimensional firm scaling` [verified URL: aoyama.ac.jp PDF]) | sales ~ employees^**≈1**; overhead ~ employees^**≈0.85** | firm-level balance-sheet data | **NO** — no firm microdata | Firm-size scaling regressions; requires Orbis/Compustat-type data |
| **Diversity & specialisation scaling** (`Yang, Holehouse, Youn, Arroyo, Redner & West 2026 PNAS`, "Scaling laws for function diversity and specialization…" [verified URL: LSE researchonline pnas.2509729123.pdf; scixplorer 2026PNAS..12309729Y]) | function diversity superlinear; specialisation parameter γ with common mean | counts of distinct functions/occupations by city or country | **PARTIAL** — occupation categories (ILOSTAT) can stand in for "functions" at country level | Compute diversity of occupations vs population size; compare the fitted γ with the paper's cross-system range; label the proxy |
| **Urbanisation vs income — S-curve, not power law** (`Renaud/Pernia scattergrams` [verified URL: ageconsearch record]; three-model analysis [verified URL: wanfang]) | logistic/S-curve; no single exponent | urbanisation rate and income per head by country-year | **YES** — we have both in the panel | Fit logistic (and compare with log-linear and power) of urban share on log income, country and decade effects; test which functional form wins out of sample |
| **Agglomeration / wage premium** | wages ~ city size^**≈0.05–0.10** | city wages | **NO** — no city wage data | Same as urban scaling; blocked by the same city-output gap |
| **Gravity law for migration** (`Reilly 1931` [unverified]; modern tests e.g. radiation-model comparison [verified URL: arxiv.org/html/1803.09067v1]) | flows ~ M1·M2 / distance^**β**, β ≈ **1–2** | bilateral migration **stocks or flows**, distance/contiguity | **PARTIAL** — UN bilateral migrant stock matrix is available; flows are not | Poisson/PPML regression of migrant stock on origin and destination size and distance; report β and compare stocks vs any flow data |
| **Wagner's law** — public spending share rises with income (`Wagner 1883` [unverified]) | income elasticity > 1; no power-law exponent | government spending share and income | **YES** — the matrix has tax share and income | Country panel: spending share on log income, country and decade effects; already close to an existing matrix link |
| **Mincer schooling → earnings** (`Mincer 1974` [unverified]; support [verified URL: econ.yale.edu PDF]) | log earnings = a + b·years of schooling; **log-linear, not a power law** | individual earnings and schooling | **PARTIAL** — country-level schooling and income, no individual earnings | Test log-linearity of schooling-income at country level as a weak proxy; a real test needs survey microdata (DHS/ILO) |
| **Fertility vs income / urbanisation — nonlinear** | no stable exponent; negative and flattening | fertility, income, urbanisation by country-year | **YES** — in the panel | Nonlinear (quadratic/spline) fertility on log income and urban share, country and decade effects; test whether the scaling-style power form beats a flexible nonlinear form |
| **Occupation diversity vs population** (Heaps-like candidate) | distinct occupations ~ population^**<1** | occupation categories and employment/population | **PARTIAL** — ILOSTAT | Same design as Heaps; test at country level, then at city level only if occupation-by-city data exist |
| **School-size economies** — teacher-student ratio vs school size | per-student cost U-shaped; ratio falls then flattens | school-level enrolment and staffing | **NO** — no school-level data | Needs school censuses/administrative microdata |
| **Per-student cost vs district size — U-shaped** (`Iowa economies-of-size case` [verified URL: eric.ed.gov ED228704]) | cost falls then rises past an administrative threshold | district-level spending and enrolment | **NO** — no district finance data | Needs district finance panels |

## Testability audit — what we can actually do

**Feasible now, with data in hand (country panel):** urbanisation-versus-income functional form (logistic vs
log-linear vs power); Wagner's law (spending share vs income); fertility vs income/urbanisation nonlinearity;
country-level log-linearity of schooling and income as a weak Mincer proxy.

**Feasible after a short data pull (all free):** Zipf/rank-size and Gibrat's law from the UN World Urbanization
Prospects city file; Heaps' law and occupation-diversity scaling from ILOSTAT occupation categories; gravity for
migration from the UN bilateral migrant-stock matrix plus CEPII distance.

**Not feasible without new data:** urban superlinear/sublinear scaling (β ≈ 1.15 / 0.85), the agglomeration wage
premium, firm scaling, Lotka/Price, school-size economies and district-cost U-shapes. **The binding constraint is
city-level output** — we have city populations but not city GDP, wages, patents or infrastructure. Everything in
the first column of the table above that needs "size^β" for a socioeconomic quantity is blocked on that single
gap. A secondary binding constraint is microdata at the firm/school/individual level.

## Measurement traps to state before any test

- **Boundaries:** city versus metropolitan area versus agglomeration changes the population denominator and can
  manufacture or destroy a scaling exponent; WUP agglomerations are redefined over time.
- **Total versus per-capita:** β and β−1 are easily confused; per-capita output scales superlinearly only if
  β > 1.
- **Category counts versus sampling effort:** Heaps' and diversity measures depend on sample size and
  classification depth (2-digit vs 4-digit occupations); always report the classification and the sample.
- **Functional form:** an S-curve fitted to a power law (or the reverse) will look like a rejected law; compare
  functional forms out of sample rather than reporting one fit.
- **Endogeneity:** city size and output are jointly determined; cross-sectional scaling exponents are
  associations, not causal elasticities.
- **Country panels are not cities:** the country-level versions of these laws (urbanisation vs income, Wagner)
  are different objects from the city-level scaling laws; do not blend them in one claim.

## (1) Fertility

The scaling laws add one testable item to the fertility question: whether fertility's relationship with income
and urbanisation is better described by a power law or by a flexible nonlinear/S-curve form. Our panel can answer
that now. City-level scaling does not touch fertility without city-level fertility and output data, so the
existing country-level survival results remain the core.

## (2) Massification

The massification-relevant tests are the urbanisation-income functional form (S-curve vs power law), Wagner's
law, and — with a short data pull — rank-size, Gibrat, Heaps and gravity. What we cannot do without city output
data is the classic urban-scaling claim that schooling or output grows superlinearly with city size (β ≈ 1.15);
that is the binding gap and should be stated as such if Dr. Menefee wants urban scaling in the paper.

## Files and provenance

One table, one audit, one trap list. No new computation. Citations marked [verified URL] were confirmed through
web search on 23 Nov 2026; [unverified] ones are standard and should be checked against the publisher before a
paper. Data sources named are free to download; the UN WUP city file and ILOSTAT are the two quickest wins.
