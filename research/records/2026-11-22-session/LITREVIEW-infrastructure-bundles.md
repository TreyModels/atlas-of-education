# Infrastructure bundles and schooling: a literature review

**Commissioned 23 November 2026.** Written to answer one question: has anyone tested
whether a *composite* infrastructure measure predicts schooling better than its
individual components?

**Verification key.** [A] = abstract retrieved and read; findings quoted or paraphrased
from the abstract itself. [R] = bibliographic record verified, no machine-retrievable
abstract — claims restricted accordingly. Every DOI below was returned by OpenAlex.

---

## 1. Has anyone compared the bundle to its parts?

**Almost nobody, and the one extended discussion says not to.**

The closest empirical work is **Calderón, Moral-Benito & Servén (2014, *Journal of
Applied Econometrics*, 10.1002/jae.2373)** [A], who build a synthetic infrastructure
index covering transport, power and telecommunications and embed it in a long-run
production function. Their elasticity of output with respect to that index is
**0.07–0.10**, highly significant. But they never compare the index against its three
components — the index *is* the measure. Notably, they also report that "tests of
parameter homogeneity fail to yield evidence that the long-run parameters differ across
countries," which is the opposite of what a components-first analysis tends to find.

The one extended argument against the whole enterprise is **Ravallion (2011, *World
Bank Research Observer*, 10.1093/wbro/lkr009)** [A], on "mashup indices of development":

> "The parsimony of these indices is often appealing… But the meaning, interpretation,
> and robustness of these indices and their implied country rankings are often unclear."

His conclusion is that "nagging doubts remain about the value-added of mashup indices,
and their policy relevance, relative to the **'dashboard' alternative of monitoring the
components separately**."

That is the theoretical case for what our panel found empirically — and it is a warning,
not a test. Ravallion does not show that dashboards outperform composites; he argues
they might. **Nobody in this literature appears to have run the horse race.**

**Greco, Ishizaka, Tasiou & Torrisi (2018, *Social Indicators Research*,
10.1007/s11205-017-1832-9)** [A] review the composite-index methodology and locate the
criticism precisely where our result lands: "weighting and aggregation… are where the
paramount criticism appears." **Saisana, Saltelli & Tarantola (2005, *JRSS A*,
10.1111/j.1467-985x.2005.00350.x)** [A] supply the diagnostic — uncertainty and
sensitivity analysis on the index itself, applied to the UN technology achievement
index — which is the formal version of asking whether a ranking survives changes in
construction.

**Assessment.** The gap is real. The literature has (a) indices without component
comparison, (b) a normative argument for dashboards, and (c) methods for testing index
robustness. It does not have a head-to-head test of whether the composite beats its
parts for a specific outcome. That is a publishable hole.

---

## 2. Component by component

### 2.1 Electrification

The largest and most consistent body of evidence in the set. **Ekeocha & Garikipati
(2025, *The Energy Journal*, 10.1177/01956574251340007)** [A] meta-analyse **33 studies
and 301 effect sizes** with robust Bayesian model averaging across nine educational
outcomes. Their headline: rural household electrification raises key metrics —
attainment, enrolment, daily study hours — by an average of **15.4 percentage points**;
**+55 minutes** of daily study time for grid connections and **+42 minutes** for solar.
Effects on adult literacy and learning outcomes are weaker, "suggesting that energy
access must be complemented by targeted educational interventions." They detect **no
significant publication bias**.

That +15.4 is almost exactly the +16.05 our panel returns for lower-secondary completion,
which is either reassuring or suspicious, depending on whether the panel is
independently informative. Given that the meta-analysis pools experimental and
quasi-experimental designs and the panel is ecological, the agreement is more likely
coincidence than confirmation.

The causal designs split on magnitude:

| Study | Design | Finding |
|---|---|---|
| **Burlig & Preonas (2024, *JPE*, 10.1086/730204)** [A] | India, RGGVY, 400,000 villages, RD + DID | Access expanded meaningfully, but **"limited economic impacts after 3–5 years."** Full electrification **reduces welfare in small villages** but returns **33% IRR in large villages** |
| **Lipscomb, Mobarak & Barham (2013, *AEJ: Applied*, 10.1257/app.5.2.200)** [A] | Brazil 1960–2000, simulated grid instrument | Large positive development effects, "underestimated when one fails to account for endogenous targeting"; mechanism is **broad-based labour productivity**, not re-sorting |
| **van de Walle, Ravallion, Mendiratta & Koolwal (2015, *WBER*, 10.1093/wber/lhv057)** [A] | Rural India, 17 years | Consumption gains; **village-level externalities** to unconnected households; earnings channel runs through **men's extra work**; **no effect on wage rates** |
| **Khandker, Barnes & Samad (2013, *EDCC*, 10.1086/669262)** [A] | Vietnam, 1,120 households, 41 communes | Commune-level connection benefits **the poor more than the rich, and girls over boys**; household-level connection benefits the rich more, and boys over girls |
| **Barnes, Khandker & Samad (2009, World Bank WP 4859, 10.1596/1813-9450-4859)** [A] | Bangladesh, 20,000 households | Income gains **9–30%**; rich benefit more than poor; benefits plateau with exposure duration |
| **Aguirre (2017, *Lahore Journal of Economics*, 10.35536/lje.2017.v22.i1.a5)** [A] | Peru, IV | Children study an extra **94–137 minutes** at home per day |

The pattern is not that electrification does nothing. It is that **the effect is
conditional on village size and wealth** (Burlig & Preonas), **runs through labour
supply rather than wages** (van de Walle et al.), and **distributes unevenly by gender
and class depending on whether the connection is communal or household** (Khandker et
al.). That heterogeneity is exactly what a cross-national panel cannot see, and it is a
reason to read the panel's +16.05 as a population-average association rather than an
effect any particular village would experience.

Two studies on school-level electrification are recorded but could not be read:
**Adamba (2017, *Educational Research for Policy and Practice*,
10.1007/s10671-017-9215-1)** [R] on Ghanaian pass rates, and **Dasso, Fernández & Ñopo
(2015, SSRN 2586431)** [R] on Peru. The household-versus-school distinction matters and
this literature mostly does not make it.

### 2.2 Water and sanitation

**Sanitation moves enrolment and not learning.** **Adukia (2017, *AEJ: Applied*,
10.1257/app.20150083)** [A] uses India's national school latrine programme: latrine
construction "substantially increases enrollment of pubescent-age girls, though
predominately when providing **sex-specific** latrines," and "**academic test scores did
not increase** following latrine construction." That last clause is the one to keep in
view. Physical infrastructure shifts who attends; it does not by itself shift what is
learned.

The same split appears in water. **Komarulzaman, de Jong & Smits (2019, *Journal of
Water and Health*, 10.2166/wh.2019.044)** [A], 295 Indonesian districts over 20 years:
districts with higher diarrhoea prevalence have lower enrolment (−0.202) and higher
absenteeism (+2.334); districts with more private water access have higher enrolment
(+0.025) and lower absenteeism (−0.027). **Choudhuri & Desai (2021, *World Development*,
10.1016/j.worlddev.2021.105535)** [A] show the mechanism is time, not disease: children
in households that collect water and fuel have lower maths scores, and the burden is
gendered — "in households where the burden of collection is disproportionately borne by
women, child outcomes are significantly lower, particularly for boys."

**Koolwal & van de Walle (2012, *EDCC*, 10.1086/668280)** [A], nine countries: better
water access is **not** associated with more off-farm paid work for women, but it is
associated with **less unpaid work**, and where gender gaps in schooling are large,
"both boys' and girls' enrollments also tend to be better."

The health side is well established and much weaker than commonly assumed at the
household level. **Wolf et al. (2018, *Tropical Medicine & International Health*,
10.1111/tmi.13051)** [A] meta-analyse 135 studies: piped water to premises reduces
diarrhoea risk by 75% and 36% (higher and lower quality respectively), sanitation
interventions by 25%, handwashing with soap by 30%. But **Headey & Palloni (2019,
*Demography*, 10.1007/s13524-019-00760-y)** [A], using a panel of **442 subnational
regions in 59 countries**, find "improved water access is statistically insignificantly
associated with most outcomes, although **water piped into the home** predicts reductions
in child stunting." The distinction between "improved source" and "piped into the home"
recurs throughout this literature and is the difference between a well and a tap.

### 2.3 Roads

The two best studies point in opposite directions on economic outcomes and the same
direction on schooling.

**Asher & Novosad (2020, *AER*, 10.1257/aer.20180268)** [A], India's $40 billion rural
road programme, fuzzy RD on household and firm censuses: "four years after road
construction, the main effect of new feeder roads is to **facilitate the movement of
workers out of agriculture**. However, there are **no major changes in agricultural
outcomes, income, or assets**." That is the cleanest available evidence for the
displacement mechanism, and it is a *null* on the economic gains.

**Adukia, Asher & Novosad (2020, *AEJ: Applied*, 10.1257/app.20180036)** [A], 115,000
roads: "children stay in school longer and perform better on standardized exams," and
the heterogeneity "supports a standard human capital investment model: enrollment
increases most when nearby labor markets offer high returns to education and least when
they imply high opportunity costs of schooling."

Taken together these are the most important pair in the review. Roads move people out
of farming and do not raise incomes — yet they raise schooling, and they do so **where
the returns to schooling are high**. That is a demand story, not an infrastructure
story, and it is the mechanism our panel cannot see.

**Khandker, Bakht & Koolwal (2009, *EDCC*, 10.1086/598765)** [A], Bangladesh: roads
reduce poverty through agricultural production and lower input costs, and raise
**secondary** enrolment more than primary — with gains that accrue disproportionately to
the poor.

### 2.4 School infrastructure

The discouraging literature. **Glewwe, Hanushek, Humpage & Ravina (2011, NBER WP 17554,
10.3386/w17554)** [A] screened over 9,000 studies down to 43 high-quality ones and found
"the estimated impacts on time in school and learning of most school and teacher
characteristics are statistically insignificant"; the exceptions — desks, teacher
subject knowledge, teacher absence — "provide little guidance for future policies."
**Barrett, Treves, Shmis, Ambasz & Ustinova (2018, World Bank, 10.1596/978-1-4648-1378-8)**
[A] synthesise the school-infrastructure evidence around access, safety, design,
pedagogy and sustainability rather than effect sizes.

So: **household and settlement infrastructure has measurable schooling effects; school
buildings mostly do not.** That asymmetry is worth stating explicitly, because "build
schools" is the intuition most policy writing starts from.

---

## 3. Is the bundle real, or is it a portfolio?

The single most useful study for the bundle question is not about infrastructure at
all. **Mitchell, Gelman, Ross, Chen et al. (2018, *Lancet Global Health*,
10.1016/s2214-109x(18)30065-2)** [A] evaluate the Millennium Villages Project — a ten-year,
**multisector** rural package across ten sub-Saharan sites — and find that **30 of 40
outcomes** improved significantly, "some outcomes… roughly one SD better" in agriculture
and health.

That is the best evidence in this literature that **a package delivered as a package
works**. It is also a caution: MVP bundled spending, staffing and political attention
together, so the individual components cannot be separated — which is precisely the
identification problem, and precisely why our panel's finding that the components are
*not* correlated within countries is interesting. In the MVP the bundle was real because
it was *administered* as one. In the cross-national data, infrastructure is administered
by separate ministries and the components come apart.

**Keefer & Knack (2007, *Review of Economics and Statistics*, 10.1162/rest.89.3.566)**
[A] supply the political-economy half of the user's intuition: "public investment is
dramatically higher in countries with low-quality governance and limited political checks
and balances or no competitive elections… these governments use public investment as a
vehicle to increase their rent-seeking." That is the financing package seen from the
supply side. If public investment is a rent vehicle, then measured infrastructure is
partly a measure of rent-seeking capacity, and its correlation with schooling needs no
causal story at all.

**Straub (2008, World Bank WP 4460, 10.1596/1813-9450-4460)** [A] surveys 140
specifications across 64 papers and documents the standing problems: aggregation level,
endogeneity, and the arbitrage between new investment and maintenance. **Foster &
Briceño-Garmendía (2010, AICD)** [A] built the African baseline dataset that makes
country-level infrastructure measurement possible at all.

---

## 4. Where the field disagrees

1. **Magnitude.** Meta-analysis says +15.4 percentage points on educational outcomes
   (Ekeocha & Garikipati); the best RD design says limited economic impact in 3–5 years
   (Burlig & Preonas). These are reconcilable only if the short-run local effect is small
   and the long-run aggregate effect is large — which nobody has demonstrated.
2. **Distribution.** Khandker et al. find commune connection favours the poor and
   household connection favours the rich; Barnes et al. find the rich benefit more.
   Whether electrification is progressive depends on the level at which it is delivered.
3. **Whether infrastructure moves learning at all.** Adukia finds latrines raise
   enrolment and leave test scores flat; Glewwe et al. find most school inputs
   insignificant. Against that, Adukia, Asher & Novosad find roads raise exam
   performance. The difference may be that roads change the *return* to schooling rather
   than the *supply* of it.
4. **Whether composite indices are useful.** Calderón et al. use one and find a clean
   elasticity; Ravallion argues the enterprise is uninterpretable and recommends
   dashboards.

---

## 5. What is missing

1. **No head-to-head test of composite versus components** for any schooling outcome.
   This is the gap the review was commissioned to find, and it is open.
2. **No test of whether infrastructure components co-move within countries.** The
   cross-country literature treats "infrastructure access" as one thing because it
   correlates across countries; nobody reports the within-country correlation matrix.
3. **Household versus school versus settlement infrastructure are rarely separated** in
   the same study, although the effects differ sharply.
4. **The financing package is almost never measured.** Keefer & Knack treat public
   investment as a rent proxy; nobody tests whether aid, credit, fiscal capacity and
   macro stability predict *access* once the level of income is controlled.
5. **Roads are the weakest-measured and most-important component.** Asher & Novosad and
   Adukia et al. use programme rollouts in one country. No cross-national road series of
   usable quality exists, which is why the road question is answered by case study or not
   at all.

---

## 6. What this means for constructing a bundle index

Five practical rules, drawn from the methodological literature above:

1. **Weight, don't average.** Greco et al. locate the criticism in weighting and
   aggregation; an unweighted mean of z-scores is the least defensible choice available
   and is the one most often used.
2. **Report the components.** Ravallion's dashboard recommendation is not modesty — it
   is the claim that a reader should be able to see which component is doing the work.
3. **Test the index's sensitivity.** Saisana et al. provide the machinery: perturb
   weights, aggregation rule and component definitions, and see whether conclusions
   survive.
4. **Check co-movement before assuming a factor.** A composite assumes the components
   measure one thing. That is a testable assumption — within-country correlations — and
   it should be reported, not assumed.
5. **Compare against the best single component, not against nothing.** The relevant null
   for a composite is not "no predictor"; it is "the strongest component alone." A
   composite that cannot beat its best part should not be used.

**What would count as evidence that the bundle works?** A composite that (a) is
internally coherent within countries, (b) predicts the outcome better than its best
component out of sample, and (c) survives weight and aggregation perturbation. Absent
all three, a dashboard is the honest presentation.

---

## References

Adukia, A. (2017). Sanitation and education. *American Economic Journal: Applied
Economics, 9*(2), 23–59. https://doi.org/10.1257/app.20150083

Adukia, A., Asher, S., & Novosad, P. (2020). Educational investment responses to
economic opportunity: Evidence from Indian road construction. *American Economic
Journal: Applied Economics, 12*(1), 348–376. https://doi.org/10.1257/app.20180036

Aguirre, J. C. (2017). The impact of rural electrification on education: A case study
from Peru. *The Lahore Journal of Economics, 22*(1). https://doi.org/10.35536/lje.2017.v22.i1.a5

Asher, S., & Novosad, P. (2020). Rural roads and local economic development. *American
Economic Review, 110*(3), 797–823. https://doi.org/10.1257/aer.20180268

Augsburg, B., & Rodríguez Lesmes, P. A. (2018). Sanitation and child health in India.
*World Development, 107*, 22–39. https://doi.org/10.1016/j.worlddev.2018.02.005

Barnes, D. F. O., Khandker, S. R., & Samad, H. A. (2009). *Welfare impacts of rural
electrification: A case study from Bangladesh* (Policy Research Working Paper 4859).
World Bank. https://doi.org/10.1596/1813-9450-4859

Barrett, P., Treves, A., Shmis, T., Ambasz, D., & Ustinova, M. (2018). *The impact of
school infrastructure on learning: A synthesis of the evidence*. World Bank.
https://doi.org/10.1596/978-1-4648-1378-8

Barro, R. J., & Lee, J.-W. (2013). A new data set of educational attainment in the
world, 1950–2010. *Journal of Development Economics, 104*, 184–198.
https://doi.org/10.1016/j.jdeveco.2012.10.001

Burlig, F., & Preonas, L. (2024). Out of the darkness and into the light? Development
effects of rural electrification. *Journal of Political Economy, 132*(9).
https://doi.org/10.1086/730204

Calderón, C., Moral-Benito, E., & Servén, L. (2014). Is infrastructure capital
productive? A dynamic heterogeneous approach. *Journal of Applied Econometrics, 30*(2),
177–198. https://doi.org/10.1002/jae.2373

Choudhuri, P., & Desai, S. (2021). Lack of access to clean fuel and piped water and
children's educational outcomes in rural India. *World Development, 145*, 105535.
https://doi.org/10.1016/j.worlddev.2021.105535

Ekeocha, D. O., & Garikipati, S. (2025). Does rural household electrification improve
education in the Global South? Evidence from a robust Bayesian meta-analysis. *The
Energy Journal*. https://doi.org/10.1177/01956574251340007

Foster, V., & Briceño-Garmendía, C. (Eds.). (2010). *Africa's infrastructure: A time for
transformation*. World Bank. https://doi.org/10.1596/978-0-8213-8041-3

Glewwe, P., Hanushek, E. A., Humpage, S. D., & Ravina, R. (2011). *School resources and
educational outcomes in developing countries: A review of the literature from 1990 to
2010* (NBER Working Paper 17554). https://doi.org/10.3386/w17554

Greco, S., Ishizaka, A., Tasiou, M., & Torrisi, G. (2018). On the methodological
framework of composite indices: A review of the issues of weighting, aggregation, and
robustness. *Social Indicators Research, 141*, 61–94.
https://doi.org/10.1007/s11205-017-1832-9

Headey, D., & Palloni, G. (2019). Water, sanitation, and child health: Evidence from
subnational panel data in 59 countries. *Demography, 56*, 729–754.
https://doi.org/10.1007/s13524-019-00760-y

Keefer, P., & Knack, S. (2007). Boondoggles, rent-seeking, and political checks and
balances: Public investment under unaccountable governments. *Review of Economics and
Statistics, 89*(3), 566–572. https://doi.org/10.1162/rest.89.3.566

Khandker, S. R., Bakht, Z., & Koolwal, G. B. (2009). The poverty impact of rural roads:
Evidence from Bangladesh. *Economic Development and Cultural Change, 57*(4), 685–722.
https://doi.org/10.1086/598765

Khandker, S. R., Barnes, D. F., & Samad, H. A. (2013). Welfare impacts of rural
electrification: A panel data analysis from Vietnam. *Economic Development and Cultural
Change, 61*(3), 659–692. https://doi.org/10.1086/669262

Komarulzaman, A., de Jong, E., & Smits, J. (2019). Effects of water and health on
primary school enrolment and absenteeism in Indonesia. *Journal of Water and Health,
17*(2), 271–283. https://doi.org/10.2166/wh.2019.044

Koolwal, G., & van de Walle, D. (2013). Access to water, women's work, and child
outcomes. *Economic Development and Cultural Change, 61*(2), 369–405.
https://doi.org/10.1086/668280

Lipscomb, M., Mobarak, A. M., & Barham, T. (2013). Development effects of
electrification: Evidence from the topographic placement of hydropower plants in Brazil.
*American Economic Journal: Applied Economics, 5*(2), 200–231.
https://doi.org/10.1257/app.5.2.200

Mitchell, S., Gelman, A., Ross, R., Chen, J., Bari, S., et al. (2018). The Millennium
Villages Project: A retrospective, observational, endline evaluation. *The Lancet Global
Health, 6*(5), e500–e513. https://doi.org/10.1016/s2214-109x(18)30065-2

Ravallion, M. (2011). Mashup indices of development. *The World Bank Research Observer,
27*(1), 1–32. https://doi.org/10.1093/wbro/lkr009

Saisana, M., Saltelli, A., & Tarantola, S. (2005). Uncertainty and sensitivity analysis
techniques as tools for the quality assessment of composite indicators. *Journal of the
Royal Statistical Society: Series A, 168*(2), 307–323.
https://doi.org/10.1111/j.1467-985x.2005.00350.x

Straub, S. (2008). *Infrastructure and growth in developing countries: Recent advances
and research challenges* (Policy Research Working Paper 4460). World Bank.
https://doi.org/10.1596/1813-9450-4460

van de Walle, D., Ravallion, M., Mendiratta, V., & Koolwal, G. (2017). Long-term gains
from electrification in rural India. *The World Bank Economic Review, 31*(2), 331–356.
https://doi.org/10.1093/wber/lhv057

Wolf, J., Hunter, P. R., Freeman, M. C., Cumming, O., Clasen, T., et al. (2018). Impact
of drinking water, sanitation and handwashing with soap on childhood diarrhoeal disease:
Updated meta-analysis and meta-regression. *Tropical Medicine & International Health,
23*(5), 508–525. https://doi.org/10.1111/tmi.13051
