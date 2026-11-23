# The agricultural floor: a partial replication of Boppart et al. and the sequencing of the farm exodus

**Trey Menefee**
Atlas of Education
Working paper, 25 November 2026

**JEL codes:** O11, O13, O14, O15, O33, J21, Q12

---

## Abstract

Why do poor countries keep so much labour in agriculture? Boppart, Kiernan, Krusell, and Malmberg (2023) give the price explanation a precise form: when non-agricultural productivity is low, investment and intermediate goods are expensive relative to labour, so farmers substitute the cheap factor (labour) for the expensive ones, and agricultural labour productivity stays low as an equilibrium outcome. We rebuild the objects this argument needs from public agricultural, price and macro data for up to 182 countries, and we report a **partial replication**: the cross-sectional mechanism replicates in direction and roughly in magnitude. The elasticity of substitution between capital and labour is 1.24 (SE 0.08) in 2005 and 1.40 (SE 0.07) in 2015; between intermediates and labour, 1.11 (0.08) and 1.27 (0.07); at the development extremes these rise to 1.73/1.76 and 1.73/1.64, against the original's preferred 1.90 and 1.75. Capital and intermediates per worker rise by roughly 570- and 637-fold from the poorest to the richest countries (the original reports 300- to 800-fold), and input intensification explains 55-69 per cent of the agricultural labour-productivity gap (the original: "a bit less than two-thirds"). Our elasticities are lower than the original's and the land margin cannot be estimated without land-quality data, so this is a replication in direction and order of magnitude, not a confirmation.

The theory also needs a sequence, and the sequence is where the data stop cooperating. In a ten-year country panel, the level association between input intensity and subsequent labour release has the wrong sign (+1.75, SE 0.71), the reverse association (past agricultural-share change on current intensity) is stronger (-3.32, SE 0.70), and past changes in intensity do not predict the next decade's labour release. The downstream link from labour release to schooling and fertility is a precise null at that horizon (fertility change −0.0003, SE 0.0058, n = 503; a change of 0.016 births would have been detected). The cross-section is consistent with the floor; the country panel cannot order the release.

The sequencing result that matters for agricultural-development policy comes from a separate exercise. In 64 late-industrialising countries with all three event dates identifiable in a common 1965-2010 window, **schooling take-off precedes agricultural labour release in 61 of 64 countries** (median gap 26 years), and labour-market demand — wage premia and paid employment — leads the schooling take-off in only 7 per cent of countries. The pattern is not a discovery of the historical literature, which has documented schooling-before-industry cases since at least Sandberg's (1979) "impoverished sophisticate"; our increment is the systematic country-by-country coding of the sequence and a supply-versus-demand horse race on the coded data. A supply block dominates the horse race (composite standardised coefficient +0.456, SE 0.174, against +0.006, SE 0.203, for demand). The policy reading is that the rural schooling pipeline may be a precondition for the farm exodus, not a consequence of it — which reverses the standard structural-transformation narrative in development economics, while agreeing with the older economic-history literature.

A joint demography-agriculture model is presented as a **demonstration, not an estimate**: five free parameters calibrated jointly, two of five well identified, with counterfactuals showing that freezing mechanisation leaves the agricultural floor in place (39.9 per cent agricultural employment in 2020 against 17.6 per cent in the baseline), freezing the schooling pipeline starves absorption (3.0 years of schooling, TFR 2.94), and freezing the mortality decline removes the population explosion (population index 0.39 against 1.58). We state plainly what the results do **not** support: that mechanisation causes schooling or fertility change. The paper closes with an agricultural-development research agenda — farm-level panels, directly measured tractor adoption, input and land-rental markets, and subnational school construction — and says what each could and could not identify.

---

## 1. Introduction

Structural transformation is one of the few robust regularities in development economics: as countries grow, labour leaves agriculture. What is less settled is *why the agricultural sector in poor countries uses so much labour* — and, once labour is released, *what absorbs it and in what order*. Agricultural-development economists have a stake in both questions. The first determines whether the agricultural "floor" is a technology problem, a price problem, or an institutional one, and therefore whether input subsidies, mechanisation programmes, or land institutions are the right instrument. The second determines whether rural schooling is an input to the farm exodus or a consequence of it, and therefore whether school construction in rural areas should be sequenced before or after agricultural modernisation.

Boppart, Kiernan, Krusell, and Malmberg (2023; hereafter BKKM) give the price explanation a precise form. In a nested CES production function, if non-agricultural productivity is low, investment goods and intermediate inputs are expensive relative to labour. A farmer facing expensive capital and expensive fertiliser but cheap labour farms with many hands and few machines. As non-agricultural productivity rises, inputs become cheaper relative to labour, farms intensify, and labour is released. The mechanism is elegant, it organises a large set of facts, and it makes three quantitative demands: the elasticity of substitution between inputs and labour must exceed one, inputs must account for a substantial share of the cross-country productivity gap, and — for the explanation to be dynamic rather than merely cross-sectional — inputs must be adopted *before* labour leaves agriculture.

This paper does four things.

**First, it replicates the cross-section.** We rebuild the objects BKKM's argument needs from public data: USDA ERS agricultural quantities and output, the Penn World Table price level of investment and labour share, and World Bank development indicators, for up to 182 countries. Our elasticities are 1.24 (capital-labour) and 1.11 (intermediates-labour) in 2005, rising to 1.73 and 1.76 at the development extremes, against BKKM's preferred 1.90 and 1.75. Input intensification explains 55-69 per cent of the agricultural labour-productivity gap, against their "a bit less than two-thirds". This is a partial replication: the direction and order of magnitude hold, the point estimates are lower, and the land elasticity cannot be estimated without land-quality data.

**Second, it tests the sequence, and reports a failure.** BKKM is a cross-sectional paper; the dynamic sequence is an implication, not an estimate. In a ten-year country panel with country and decade fixed effects, the level association between input intensity and subsequent labour release has the wrong sign (+1.75, SE 0.71), the reverse check is stronger (-3.32, SE 0.70), and past changes do not predict the next decade. The downstream link from labour release to schooling and fertility is a precise null (fertility change −0.0003, SE 0.0058; minimum detectable effect about 0.016 births). The honest conclusion is that the country panel cannot order the release: intensity and labour release move together, and the cross-section is consistent with the floor without identifying the path.

**Third, it reports the sequencing surprise.** In 64 late-industrialising countries with event dates for all three transitions in a common 1965-2010 window, schooling take-off precedes agricultural labour release in 61 of 64 countries (median gap 26 years), and labour-market demand leads the schooling take-off in only 7 per cent of countries. This is where we must be careful with the claim. The direction — schooling before factories — is not new; Sandberg (1979) described Sweden's "impoverished sophisticate", and the world-polity school has argued for decades that mass schooling spread by institutional imitation rather than industrial demand (Boli, Ramirez, & Meyer, 1985; Meyer, Ramirez, & Soysal, 1992; Ramirez & Boli, 1987). Our increment is **systematic measurement**: we code the sequence for 64 countries with pre-registered event rules, report a date table, and run a supply-versus-demand horse race on the coded data, in which a supply block dominates (composite +0.456, SE 0.174) and labour-market demand is null (+0.006, SE 0.203). The finding contradicts the standard structural-transformation narrative in *development economics* — farm productivity growth releases labour, and the non-farm economy then demands skills — while agreeing with the older economic-history literature. For agricultural-development policy, that is the useful part: the rural schooling pipeline may be a precondition for, not a consequence of, the farm exodus.

**Fourth, it presents the joint model as a demonstration.** A demography-agriculture-absorber model with five free parameters, calibrated jointly on stylised-country medians, reproduces the shape of the transition and produces counterfactuals: freezing mechanisation leaves 39.9 per cent of labour in agriculture and cuts schooling to 0.2 years; freezing the schooling pipeline leaves released labour unabsorbed and fertility at 2.94; freezing the mortality decline removes the population explosion (population index 0.39). Two of the five parameters are well identified, so the model is evidence about structure, not about history. We label it accordingly.

The rest of the paper is organised as follows. Section 2 describes the floor and the replication. Section 3 tests the sequence in the country panel. Section 4 reports the sequencing exercise and the supply-demand horse race. Section 5 presents the joint model as a demonstration. Section 6 is the literature review, organised for the agricultural-development audience. Section 7 draws out the policy implications, and Section 8 lays out the research agenda that would turn the cross-sectional mechanism into a causal statement. Section 9 states the limitations and what the paper does not claim; Section 10 covers reproducibility and data availability.

---

## 2. The agricultural floor: theory and replication

### 2.1 The mechanism in one paragraph

BKKM's argument is a relative-price argument with a substitution elasticity attached. In a nested CES production function, the farmer combines capital, intermediate inputs, land, and labour. If non-agricultural productivity is low, the relative price of investment goods and intermediates is high; the farmer substitutes away from them toward labour. Poor countries therefore farm with low input intensity and low labour productivity, and the low productivity is an equilibrium outcome of the price environment rather than a failure of the farmer. As non-agricultural productivity rises, inputs cheapen, intensity rises, and labour is released. The mechanism requires three empirical supports: substitution elasticities above one, input intensity that varies strongly with relative input prices across countries, and input intensification that accounts for a substantial share of the labour-productivity gap.

### 2.2 Data and deviations from the original

The original's online appendix (NBER data appendix w31101) contains only an appendix PDF, with no data. We therefore rebuilt the minimum object from public sources: the project panel's USDA ERS agricultural quantities (capital, labour, intermediates, land, output; 182 countries, 1961-2023), the Penn World Table price level of investment, labour share and GDP per worker, a fresh World Bank WDI pull for agricultural employment share, GDP per capita, urbanisation, fertility and population (207,622 rows), and the transition record for demography.

Our deviations from the original are stated up front because they bound what the replication can mean. **No GAEZ land-quality adjustment.** **No BACI country-specific intermediate prices**: the non-agricultural price level is used as a proxy. **No LSMS land and intermediate cost shares**: these are assumed and documented. **Benchmark years 2005 and 2015** instead of a single 2005 cross-section. **The land elasticity cannot be estimated** because no land price is available. These are not cosmetic deviations; they are why the result is a partial replication rather than a confirmation.

### 2.3 What replicates

Table 1 reports the cross-sectional estimates against the original's values.

**Table 1. Replication of BKKM's cross-sectional objects (subsistence@41f6429, results/replication.txt and replication.json).**

| Object | Our estimate | BKKM (2023) |
|---|---|---|
| Elasticity, capital vs labour, 2005 | 1.24 (SE 0.08), n = 127 | 1.90 (preferred nesting) |
| Elasticity, capital vs labour, 2015 | 1.40 (SE 0.07), n = 128 | — |
| Same, matched at development extremes, 2005 / 2015 | 1.73 / 1.73 | 1.90 |
| Elasticity, intermediates vs labour, 2005 | 1.11 (SE 0.08), n = 127 | 1.75 |
| Elasticity, intermediates vs labour, 2015 | 1.27 (SE 0.07), n = 128 | — |
| Same, matched at development extremes, 2005 / 2015 | 1.76 / 1.64 | 1.75 |
| Capital/labour quantity rise, poorest to richest | 570× (2005); 557× (2015) | 300-800× |
| Intermediates/labour quantity rise | 637× (2005); 394× (2015) | 300-800× |
| Input intensification share of the labour-productivity gap | 55-69% (USDA input index 55-61%; cost-share decomposition 69%) | "a bit less than two-thirds" |

The cross-section behaves as the paper says: relative input prices and input intensities move in opposite directions, elasticities are above one, and inputs explain roughly two-thirds of the productivity gap. The agricultural labour-productivity gap itself is large — 4.78 log points, a ratio of about 119 to 1 between the richest and poorest deciles in 2005 (4.80 and 122 to 1 in 2015) — and the decomposition with paper-style shares gives 3.32 log points, or 69 per cent, of that gap (higher input shares give 86 per cent; the USDA's own input index gives 55-61 per cent).

Our reading is deliberately narrow: **direction and order of magnitude replicate, point estimates do not.** The elasticities are somewhat lower than the original's and the land margin is untestable here. A referee should treat this as a partial replication with rebuilt data, not as an independent confirmation of BKKM's preferred parameter values.

### 2.4 The reduced-form objects the mechanism needs

Two cross-sectional relationships carry the mechanism, and both replicate. First, the relative input price and input intensity are strongly negatively associated: the log intensity on the log relative input price gives **−1.13 (SE 0.15) in 2005 (n = 126)** and **−1.28 (SE 0.11) in 2015 (n = 128)**. Expensive inputs, low intensity — the first link.

Second, intensity is strongly negatively associated with the agricultural employment share, controlling income. In 2005 the agricultural employment share on intensity gives **−4.71 (SE 0.89)** with a relative-price coefficient of +1.11 (2.23) and income −7.32 (2.07), n = 126; in 2015, **−4.38 (SE 1.15)**, relative price +4.02 (3.40), income −4.12 (2.31), n = 128. The intensity coefficient is robust; the relative-price coefficient has the predicted positive sign but is not significant. This is a half-confirmation of the second link: countries with more intensive agriculture keep less labour on the farm, but the price channel is not separately identified in this cross-section.

**Table 2. Corrected reduced-form tests (subsistence@41f6429, results/corrected_test.txt).**

| Test | Estimate (SE) | n | Reading |
|---|---|---|---|
| T2a: log intensity on log relative input price, 2005 | −1.13 (0.15) | 126 | confirmed |
| T2a: same, 2015 | −1.28 (0.11) | 128 | confirmed |
| T2a2: ag employment share on intensity, 2005 | −4.71 (0.89) | 126 | half confirmed |
| T2a2: same, 2015 | −4.38 (1.15) | 128 | half confirmed |
| T2a2: relative price coefficient, 2005 / 2015 | +1.11 (2.23) / +4.02 (3.40) | 126 / 128 | predicted sign, n.s. |

A note on the project's own history. An earlier test in this project regressed farm exit, wage jobs and births on a world commodity-price index interacted with the farm employment share. It measured the exposure of farm employment to a common world price shock; it contained none of BKKM's objects — no input quantities, no relative input prices, no substitution elasticity, no development decomposition — and it could not have detected the intensive-margin mechanism even if the mechanism were true and large. The corrected tests above replace it. The old null is not evidence about BKKM in either direction.

---

## 3. The release the theory needs: why the country panel cannot order it

The cross-section is consistent with the floor. But the floor explanation is also a story about time: inputs are adopted, then labour is released. If the correlation is simultaneous or the causation runs the other way — labour release creates the demand for labour-saving inputs — the cross-section cannot tell us which.

We pre-registered three tests (T2b, T2b(a)-(c), T2c) and report them in the order they were run. The panel is a ten-year lead-lag set-up: outcome at t+10 on intensity and relative input price at t, with country and decade fixed effects, clustered by country. The sample is 507 country-year observations covering 128 countries, years 1995-2010 every fifth year.

**The level association fails the sign test.** Change in the agricultural employment share from t to t+10 on intensity(t) and relative price(t) gives **+1.75 (SE 0.71)** on intensity and +0.82 (0.32) on price. Both are significant, and both have the *wrong* sign for the theory: higher intensity and higher input prices are associated with *less* labour release over the next decade, not more. This is the counterintuitive result that motivates the rest of the section.

**The reverse association is stronger.** Regressing past agricultural-share change (t−10 to t) on current intensity and price gives **−3.32 (SE 0.70)** on intensity and −1.09 (0.37) on price, n = 383. If the reverse check is at least as strong as the forward check, the lead-lag ordering is not identified; here it is stronger. Labour release and input intensity move together, and the panel cannot say which comes first.

**Past changes do not predict the next decade.** Change in intensity from t to t+10 on the relative input price at t gives −0.0022 (0.0636), n = 503; on the change in the relative price over the same decade, +0.0122 (0.0348), n = 376. Change in the agricultural share from t to t+10 on *past* changes in intensity and price, controlling for the current share, gives −0.044 (0.378) and +0.355 (0.386), n = 472; the only stable predictor is convergence in the agricultural share itself (−0.530, SE 0.101). A long difference (1995-2015) gives the same picture: initial intensity −0.757 (0.871), initial relative price +0.181 (0.897), initial agricultural share −0.193 (0.052), initial income +0.305 (0.748), n = 124. All null except convergence.

**The downstream link is a precise null.** Change in secondary completion from t to t+10 on labour release and intensity gives −0.162 (0.245) and −1.184 (3.198), n = 278. Change in fertility gives **−0.0003 (0.0058)** and −0.0047 (0.0500), n = 503, with income and urbanisation controls. The minimum detectable effect is about **0.016 births** — the estimate is an order of magnitude smaller than the MDE, so the null is not a power failure. At ten-year country-panel horizons, labour release does not visibly move schooling or fertility.

The conclusion is structural, not a matter of one regression: **the cross-section supports the floor, and the country panel cannot order the release.** The mechanism may be right; the dynamic sequence the mechanism implies is not identified in these data. That is the paper's main negative result, and it is reported as such.

---

## 4. The sequencing surprise: schools before farms

### 4.1 The event coding

The follow-up exercise asks a different question: when the two transitions happen, which comes first? We pre-registered event rules and a common window (1965-2010). Release onset is the first year after which the agricultural employment share falls by at least 3 points in ten years. Schooling take-off is the first year after which mean years of schooling rises by at least 1.0 year in ten years. Fertility onset is the first year after which TFR falls by at least 1.0 birth in ten years. Of 180 countries with data, **64 have all three events detected**.

### 4.2 The result

**Table 3. Country event sequencing (subsistence-v2@ce66cfc; the fertility ordering is recomputed strictly from `results/event_dates.csv`, canonical recomputation at `research/paper-massification-2026-11-25` @ `95dc135`).**

| Ordering | Share of 64 countries | Bootstrap 95% CI |
|---|---|---|
| Schooling before agricultural labour release | **61/64 = 95%** | — |
| Release before schooling | 5% (3/64) | [0, 11]% |
| Schooling before fertility (strict: take-off strictly earlier) | **37.5% (24/64)** | [26.6, 50.0]% |
| Schooling and fertility take off in the same year | 31.3% (20/64) | — |
| Fertility before schooling | 31.3% (20/64) | — |
| Release before fertility | 6.25% (4/64; no ties) | — |

Median gap release → schooling: **−26 years** (bootstrap 95% CI −26 to −22): schooling take-off comes a generation *before* the large farm-labour release. The individual country dates are in `event_dates.csv`; the list spans Albania, Bangladesh, Belize, Brazil, Chile, China, Côte d'Ivoire, Colombia, Costa Rica, Cuba, the Dominican Republic, Algeria, Ecuador, Egypt, Spain, Fiji, Ghana, Guatemala, Guyana, Honduras, and 41 more.

**A correction on the fertility ordering.** An earlier version of the source record reported "schooling before fertility" as 69%. That field (`pct_schooling_before_fertility` = 68.75 in `sequencing.json`) counts the 20 simultaneous take-offs as schooling-first and must not be cited as the ordering (the record is annotated at `subsistence-v2` @ `8caaeac`). The strict recomputation gives 24/64 = 37.5% (bootstrap 95% CI 26.6-50.0%), 20 simultaneous (31.3%), 20 fertility-first (31.3%), median gap 0 years (IQR −5 to +8); across all 81 countries with both dates it is 29/81 = 35.8% (25.9-45.7%). For release versus fertility, 4/64 = 6.25% have release first with no ties, so in 60/64 = 93.75% the fertility decline precedes the farm-labour release. The schooling-fertility ordering is therefore much weaker than the schooling-release ordering: the robust sequence in these data is schooling before release and fertility before release, not a clean schooling → fertility → release order.

### 4.3 What is new here, and what is not

The direction is **not new**. Sandberg (1979) documented Sweden's early mass literacy as the "impoverished sophisticate"; the world-polity school has argued since the 1980s that mass schooling spread through institutional imitation and state formation rather than industrial demand (Boli, Ramirez, & Meyer, 1985; Meyer, Ramirez, & Soysal, 1992; Ramirez & Boli, 1987; Benavot & Riddle, 1988); and the human-capital-before-industry literature has made the same case with historical evidence from Prussia, England and the Low Countries (Becker & Woessmann, 2009; Squicciarini & Voigtländer, 2015; de Pleijt & van Zanden, 2016; Galor & Moav, 2006). What is new is the **systematic, pre-registered coding of the sequence for 64 countries**, with a date table and a robustness discussion, and a **supply-versus-demand horse race** on the coded data. The paper does not claim to have discovered that schooling can precede industry. It claims to have measured how often, by how much, and against which demand-side alternative, in a sample that spans the late-industrialising world.

### 4.4 Is it supply or demand?

The supply-side follow-up asks whether the schooling take-off is better described as supply-led (school places, teachers, spending) or demand-led (wage premia, paid jobs, urbanisation, income). Three results matter.

**Raw event ordering is uninformative because of data start dates.** Supply onset precedes the schooling take-off in 28 per cent of countries (bootstrap [19, 37] per cent) and demand onset in 73 per cent ([64, 82] per cent), but 61 of 108 schooling take-offs sit exactly on the 1965 window boundary, while the supply series start in the median country only in 1975. In a fair-comparison sample of 33 countries (schooling after 1965 and supply data present before the take-off), supply precedes schooling in 76 per cent and demand in 79 per cent, with supply before demand in 39 per cent — the two sides turn at essentially the same time.

**Labour-market demand does not lead.** When demand is measured only by labour-market variables — the wage premium (non-agricultural relative to agricultural labour productivity) and the paid-employment share — it precedes the schooling take-off in just **7 per cent of 58 countries**. The raw "demand-first" result is carried by broad development indicators (income, urbanisation), not by returns to schooling or wage jobs. That distinction is the one an agricultural-development audience should care about: it is not that development doesn't move first; it is that *the labour-market demand channel does not*.

**The horse race is the sharper test.** Ten-year changes in mean years of schooling on standardised supply and demand blocks, with country and period fixed effects, clustered by country (n = 78 country-period observations, 51 countries):

**Table 4. Supply-versus-demand horse race (supply-demand@963e5e5, results/supply_demand.txt and supply_demand.json).**

| Block | Coefficient (SE) | Reading |
|---|---|---|
| Supply composite | **+0.456 (0.174)** | dominant |
| Demand composite | +0.006 (0.203) | null |
| Education spending | +0.125 (0.058) | significant |
| Gross enrolment | +0.307 (0.146) | significant |
| Pupil-teacher ratio | +0.098 (0.102) | null |
| Wage premium | −0.209 (0.114) | null |
| Paid employment | +0.051 (0.117) | null |
| Urbanisation | −0.049 (0.096) | null |
| Income | +0.140 (0.136) | null |

The supply block dominates. But the honest reading is a decomposition, not a causal test: education policy, state capacity and income are jointly determined, the supply series are short, and there is no instrument here. The claim is "supply-led is the better description of these data", not "supply caused massification".

### 4.5 The US benchmark, and what it can and cannot say

A US laboratory check gives the theory's ordering for the twentieth century: farm-employment decline in 1910, schooling take-off in 1955, fertility decline in 1957. But the US farm-share series is not available long-run — the OWID share-of-employment series starts in 1991, four other OWID slugs and FRED returned 404 or timed out, so documented Historical Statistics/USDA benchmark dates are used as external reference points, not API data. The OWID fertility series begins in 1933, so the US cannot adjudicate the nineteenth-century transition. The UK check could not be done: no long-run farm-employment series was obtainable, so no UK ordering is claimed. The cross-country result and the US result point in opposite directions, and the paper reports both.

---

## 5. The joint model: a demonstration, not an estimate

### 5.1 Structure

The model joins three blocks. **Agriculture:** BKKM's CES production function, with observed agricultural labour productivity split into TFP and input intensity using the estimated substitution elasticity (σ = 1.5). **Demography:** mortality paths from the transition record; fertility is a quantity-quality choice, with desired *surviving* children falling with schooling and births equal to desired children divided by survival. **Absorber:** a wage sector of finite capacity plus a schooling/credential pipeline that queues the released labour; queue pressure and the wage premium feed enrolment, and schooling lowers fertility.

### 5.2 Calibration and fit

The v2 model has **five free parameters**, calibrated jointly on 1950-2020 stylised-country medians: queue weight in schooling 4.87, wage-job creation rate 0.021 per five years, agricultural TFP growth 0.045 per five years, food income elasticity 0.409, and a mortality timing shift of +28.8 years. N0 (3.18) and kappa (0.124) are calibrated from endpoints, not free; σ = 1.5 is estimated in the replication.

**Table 5. Model fit and counterfactuals (subsistence-v2@ce66cfc, results/model_v2_summary.txt and model_v2_counterfactual.csv).**

| Year | Agricultural employment share, model / data | TFR, model / data | Schooling years, model / data | Population index, model / data |
|---|---|---|---|---|
| 1960 | 39.3% / 30.6% | 4.40 / 6.01 | 2.99 / 3.12 | 1.00 / 1.00 |
| 2000 | 24.9% / 30.3% | 2.72 / 2.71 | 5.77 / 7.92 | 1.33 / 2.24 |
| 2020 | **17.6% / 19.4%** | 2.35 / 2.06 | 7.53 / 9.57 | **1.58 / 2.92** |

The agricultural-share repair succeeded (1.8 points from the data, inside the pre-registered five-point tolerance); the population repair failed in the other direction (1.34 below the data, outside the 0.5 tolerance). The v1 model had failed the other way (8.1 per cent agricultural employment against 19.4; population index 4.4 against 2.9); v2 fixes the first and overcorrects the second.

**Parameter recovery:** re-simulating from known parameters and re-fitting all five series recovers agricultural TFP growth and the food elasticity, approximately recovers the job-creation rate, and **fails to recover the queue weight and the mortality shift** (recovery errors 2.50 and 2.54). **Two of five parameters are well identified.** No structural claim should rest on the point values of the other three.

### 5.3 Counterfactuals

The counterfactuals are the model's most policy-relevant output and its most fragile, because they inherit the identification problem.

**Table 6. Counterfactuals, 2020 (baseline = v2).**

| Scenario | Agricultural share | Schooling (years) | TFR | Population index |
|---|---|---|---|---|
| Baseline | 17.6% | 7.5 | 2.35 | 1.58 |
| Freeze mechanisation after 1960 | **39.9%** | **0.2** | 3.29 | 2.19 |
| Freeze schooling pipeline after 1960 | 18.0% | **3.0** | **2.94** | 1.90 |
| Freeze mortality decline (1800 level) | 18.4% | 7.2 | **3.96** | **0.39** |

Reading: freezing mechanisation keeps the floor in agriculture and starves the schooling pipeline; freezing the pipeline leaves released labour unabsorbed and fertility higher; freezing the mortality decline removes the population explosion altogether, which makes the mortality decline the model's implicit first mover. The model therefore produces the *opposite* sequencing to the country event dates: mortality first, then mechanisation, then schooling, then fertility. That contradiction is itself a result: the model's structure can generate the transition, but the historical sequencing it requires is not the sequencing the country data show. The model is a demonstration of a mechanism, not a reconstruction of history.

---

## 6. Literature

This section is written for the agricultural-development audience and deliberately states what is replicated, what is corrected, and what is genuinely new. A claim-by-claim map with Crossref status is in the accompanying `claims-prior-art.md`.

### 6.1 BKKM and the price explanation of agricultural intensity

BKKM (2023) is the paper under replication. Its antecedents include Restuccia, Yang, and Zhu (2008), who show that agricultural productivity differences account for a large share of cross-country income differences; Caselli and Coleman (2001), who analyse the US structural transformation and regional convergence through a multi-sector lens; Gollin, Parente, and Rogerson (2002), who place agriculture at the centre of development; Herrendorf, Rogerson, and Valentinyi (2013, 2014), who formalise the preferences-and-technology decomposition of structural change; Alder, Boppart, and Müller (2022), who build a theory of structural change that can fit the data; Alvarez-Cuadrado, Long, and Poschke (2017), who emphasise capital-labour substitution; and Duarte and Restuccia (2010), who quantify the role of structural transformation in aggregate productivity. The labour-productivity gap itself is documented by Gollin, Lagakos, and Waugh (2014), and its farm-size dimension by Adamopoulos and Restuccia (2014). Our replication sits directly on this literature: we re-estimate the objects BKKM need from rebuilt public data and find them in the same direction and roughly the same magnitude, with lower elasticities and no land margin.

### 6.2 Structural transformation: Lewis, Kuznets, Timmer, McMillan-Rodrik

The broad literature on structural transformation frames the floor. Lewis (1954) is the origin of the dual-economy view: a low-productivity agricultural sector supplies labour to a modern sector at a subsistence wage. Kuznets (1957, 1973) documented the sectoral reallocation regularities; Timmer's work (e.g., 2009) emphasises the agricultural transition and the role of food demand; McMillan and Rodrik (2011) show that the growth contribution of structural change varies with whether labour moves to high- or low-productivity activities; Rodrik (2016) documents premature deindustrialisation. The paper's sequencing result speaks directly to this literature: the standard narrative has agricultural productivity growth releasing labour, and the non-farm sector then demanding skills. Our country event dates say the schooling expansion often comes first; the supply-demand horse race says the labour-market demand channel does not lead. This is consistent with the world-polity and human-capital-before-industry literatures, and it is a problem for the strong version of the Lewis-Kuznets sequence in late-industrialising countries.

### 6.3 Mechanisation, technology adoption, and input subsidies

The agricultural-development literature on mechanisation and technology adoption is the policy-relevant neighbour. Binswanger (1986) gives the comparative-historical account of mechanisation; Pingali (2007) reviews adoption patterns and economic impacts in developing countries; Foster and Rosenzweig (1995, 2010) study learning, human capital and technical change in agriculture and the decline of agricultural employment; Gollin (2010) reviews agricultural productivity and growth; Ricker-Gilbert, Jayne, and Chirwa (2011) provide the canonical evidence on fertiliser subsidies and crowding out in Malawi. Our contribution to this literature is not a new adoption result: it is that the price mechanism BKKM propose is visible in the cross-section (input prices and intensity), that the dynamic adoption-release sequence is not identified in country panels, and that the sequencing of the *schooling* response to mechanisation is not what the standard story assumes. The policy implication — that mechanisation and input subsidies may need to be sequenced with rural schooling investment rather than assumed to generate it — is a hypothesis for farm-level work, not a finding of this paper.

### 6.4 Rural schooling: the world-polity and human-capital literatures

The rural schooling literature is where the sequencing claim must be situated. The world-polity school (Boli, Ramirez, & Meyer, 1985; Meyer, Ramirez, & Soysal, 1992; Ramirez & Boli, 1987; Benavot & Riddle, 1988) argues that mass schooling spread through institutional imitation and state formation, not industrial demand. Lindert (2004) documents the political economy of public schooling. The human-capital-before-industry literature provides the historical case evidence: Goldin and Katz (1998) on US secondary schooling, Becker and Woessmann (2009) on Prussia, Squicciarini and Voigtländer (2015) on the Enlightenment, de Pleijt and van Zanden (2016) on the Little Divergence, and Galor and Moav (2006) on the theory of the demise of the class structure. Sandberg (1979) is the canonical Swedish case. Our 64-country coding and horse race are an attempt to systematise this literature's direction of causality for the late-industrialising world; the paper does not claim to have discovered it.

### 6.5 Replication standards

The paper follows the replication turn in economics: pre-registration before data work (both source records commit the pre-registration first), a data-availability and deviations statement, a pre-registered falsifier list, and an explicit separation of estimated, calibrated and assumed objects. Christensen and Miguel (2018) state the transparency standard; Mueller-Langer, Fecher, Harhoff, and Wagner (2019) document how replication is practised in economics; the Open Science Collaboration (2015) and Nosek et al. (2015) supply the broader credibility norms. The replication here is partial by construction: the original data are not public, the land margin is untestable, and the elasticities are lower. We report that as the result rather than as a caveat.

### 6.6 The closest competitors

For the **replication**, the closest competitor is BKKM (2023) itself: no other paper, as far as this search found, rebuilds their cross-sectional objects from public data. For the **sequencing claim**, the closest competitors are the human-capital-before-industry papers — Squicciarini and Voigtländer (2015) and de Pleijt and van Zanden (2016) — which establish the direction on historical cases, and the world-polity school, which establishes it institutionally. Our increment is the systematic 64-country coding and the supply-demand horse race, not the direction. For the **dynamic failure**, the closest work is the structural-change literature that estimates the sequence rather than the cross-section (Alder et al., 2022; Alvarez-Cuadrado et al., 2017); those papers impose or estimate the sequencing through theory, and our contribution is the negative result that a country panel cannot identify it.

---

## 7. Implications for agricultural development

### 7.1 Mechanisation and input subsidies

The replication supports the price logic: input intensity is strongly negatively associated with relative input prices across countries, and intensity is strongly negatively associated with agricultural employment. If the floor is a price phenomenon, then policies that reduce the effective price of capital and intermediates — mechanisation programmes, fertiliser subsidies, credit for equipment — should raise intensity and release labour. Two caveats from this paper. First, the release is not identified in the time series: the panel cannot show intensity leading labour release, and the reverse association is stronger. Second, the cross-section is an equilibrium relationship; a subsidy that changes prices at the margin may move a country along the relationship without changing its position, and the paper cannot say how far.

### 7.2 Rural schooling investment

If mass schooling tends to precede the large farm-labour release, then rural schooling investment is not what the released labour "demands" after the fact; it may be a precondition for absorption, or at least a co-moving investment that is not generated by agricultural modernisation on any short time scale. The supply-demand horse race supports the supply reading: school places, teachers and spending move at least as early as labour-market demand and carry the conditional association, while wage premia and paid jobs do not lead. The policy implication is sequencing: school construction, teacher supply and compulsory-schooling enforcement may need to lead mechanisation programmes, not follow them. This is a hypothesis generated by the timing evidence, not a causal claim; Section 8 names the designs that could test it.

### 7.3 Sequencing of structural transformation

The standard narrative — agricultural productivity releases labour, the non-farm sector demands skills, schooling responds — is not what the country event dates show for late-industrialising countries. Both the schooling expansion and the fertility decline often precede the large farm-labour release. For policy, this changes the order of operations: if the non-farm sector is slow to absorb, and the schooling pipeline expands first, the result can be a queue of educated labour rather than a shortage of skills. The model's counterfactuals illustrate the mechanism (freezing the pipeline leaves released labour unabsorbed; freezing mechanisation starves the pipeline), though the model is a demonstration and its parameter values are only partly identified.

### 7.4 What the results do not support

The paper does **not** support the claim that mechanisation causes schooling or fertility change. It does not support the claim that labour release causes fertility decline at decadal horizons (the null is precise). It does not support using the joint model's counterfactuals as policy forecasts, because two of five parameters are not identified and the population path is mis-fitted. It does not support reading the 61/64 sequencing result as causal: the event dates are country-level, the thresholds are coding choices, the schooling series starts in 1870 and the window is 1965-2010, and the direction of the ordering is known from the historical literature. What it supports is narrower and still useful: the cross-sectional price mechanism replicates; the dynamic release sequence is not identified in country panels; and the sequencing of schooling relative to the farm exodus is systematically the opposite of the standard development narrative in late-industrialising countries.

---

## 8. Future research: what would turn the mechanism into a causal statement

The paper's central limitation is that the cross-section is consistent with the price mechanism and the panel cannot identify the sequence. Four research programmes would change that, in ascending order of cost.

**Farm-level panel data (LSMS-ISA and agricultural censuses).** The LSMS-ISA surveys (Tanzania, Uganda, Malawi, Nigeria, Ethiopia, and others) follow farm households and record plot-level inputs, labour, and output. They could measure the adoption-release sequence at the household level, where it happens, and distinguish the farmer's own labour allocation from the community's. What it cannot identify: price variation is common to a district, so household panels alone cannot separate the price channel from correlated shocks; and coverage is limited to a subset of countries.

**Directly measured tractor and mechanisation adoption.** The literature's standard instrument is adoption timing. A cross-country panel of tractor and combine adoption — from FAO machinery statistics, agricultural censuses, or national sources — could date mechanisation and test whether it precedes labour release, which is the forward test the country panel here fails. What it cannot identify: adoption is endogenous to wages and output prices, so the design needs an instrument (e.g., import-price shocks to machinery, or a mechanisation programme's eligibility rule).

**Input prices and land-rental markets.** The relative input price is the mechanism's key variable, and it is measured here with a proxy (the non-agricultural price level). Direct measures — fertiliser prices, machinery prices, land-rental rates from household surveys or land-market data — would test the first link without the proxy. What it cannot identify: prices are equilibrium objects; the design needs exogenous price variation, such as a subsidy reform or a border-price shock.

**Subnational variation in school construction.** The sequencing claim could be tested with subnational data on school construction, teacher hiring, and rural schooling expansion, matched to local agricultural employment and mechanisation. If school construction leads local farm-labour release, the supply-led reading gains a within-country test; if it follows, the demand reading does. What it cannot identify: school placement is endogenous to local demand and politics; the design needs a placement rule or a policy discontinuity.

**The design that would do most.** A pre-registered, multi-country farm-panel study with exogenous machinery-price variation and subnational school-construction timing would identify both the adoption-release sequence and the schooling response. No such study exists at the scale of the 64-country event coding here; the agenda above is the path from the cross-section to that design.

---

## 9. Limitations and what we do not claim

1. **The replication is partial.** The original data are not public; we rebuilt the objects from USDA, PWT and WDI. Elasticities are lower than the original's (1.24/1.11 against 1.90/1.75), the land margin is untestable, and the intermediate price is proxied. Direction and order of magnitude replicate; the preferred parameter values are not confirmed.
2. **The dynamic sequence is not identified.** The level association has the wrong sign, the reverse association is stronger, and past changes do not predict the next decade. The paper reports this as a negative result, not a confirmation.
3. **The downstream null is a null with power.** The fertility estimate is −0.0003 (SE 0.0058) against an MDE of about 0.016 births: at decadal horizon the labour-release-to-fertility link is not visible. Longer horizons and the historical record are what the model uses; they are not estimated here.
4. **The sequencing result is a coding result.** The 61/64 depends on the event thresholds, the window, and the schooling series' coverage. The paper states the rules and the contradictions (the US ordering runs the other way); a referee will want a date-by-date source table and a robustness exercise with alternative thresholds.
5. **The direction is not new.** Sandberg (1979) and the world-polity school documented schooling before industry. Our claim is systematic measurement, not discovery.
6. **The model is a demonstration.** Two of five parameters are well identified, the population path is mis-fitted (1.58 against 2.92), and the counterfactuals are structural illustrations, not forecasts.
7. **No causal identification anywhere in the paper.** No instrument, no experiment, no policy discontinuity. The paper's causal language is confined to what the designs in Section 8 would require.

---

## 10. Reproducibility and data availability

The paper is built from three records, all pushed to the repository:

- `research/records/2026-11-23-subsistence/` at `41f6429`: the replication (T1), the corrected reduced-form tests (T2), and the v1 model.
- `research/records/2026-11-23-subsistence-v2/` at `ce66cfc`: the calibration repair (C1-C3), the country event sequencing (C4), the US laboratory (C5), and the v2 model.
- `research/records/2026-11-23-supply-demand/` at `963e5e5`: the supply-versus-demand event ordering and horse race.

Each record contains a pre-registration committed before data work, scripts, results, and a README with provenance and deviations. A `claims-to-source.md` in this paper's record maps every number in the paper to its branch, commit hash, file and field. The raw WDI pull (207,622 rows), the OWID/FRED pulls, and the intermediate panels live on the project server and are not committed; they are regenerated by the scripts. Data are public: USDA ERS international agricultural productivity, the Penn World Table, World Bank WDI, and OWID/FRED. Runtime is light: the sequencing and model scripts run in seconds to minutes on one core; only the data pulls need network access. The earlier proxy test replaced by T2 is documented in the project's handoff record.

---

## Appendix A. Definitions and data

- **Input intensity**: (agricultural capital + intermediates) per agricultural worker, from USDA ERS quantities.
- **Relative input price**: log(investment price level / labour compensation per worker), from PWT.
- **Agricultural employment share**: share of employment in agriculture, WDI/ILO.
- **Schooling**: mean years of schooling, ages 15-64.
- **Release onset**: first year after which the agricultural employment share falls ≥3 points in ten years (1965-2010 window).
- **Schooling take-off**: first year after which mean years of schooling rises ≥1.0 year in ten years.
- **Fertility onset**: first year after which TFR falls ≥1.0 birth in ten years.
- **Supply block**: education spending (% GDP), primary pupil-teacher ratio, primary gross enrolment.
- **Demand block**: wage premium (non-agricultural relative to agricultural labour productivity), paid-employment share, urbanisation, income growth.
- **Estimated / calibrated / assumed**: estimated = from the data with a standard error (the substitution elasticities); calibrated = chosen to fit moments (the five model parameters, N0, kappa); assumed = imposed and documented (non-agricultural capital share, depreciation, β_i = 0.5).

## Appendix B. Suggested figures

1. **Relative input price and input intensity, 2005 and 2015** (scatter, log-log), with the fitted slopes −1.13 and −1.28.
2. **Input intensity and the agricultural employment share**, controlling income, 2005 and 2015.
3. **Event sequencing**: a country-sorted timeline with schooling take-off, release onset and fertility onset dates, ordered by the schooling-release gap (the 61/64 pattern visible at a glance).
4. **Supply versus demand horse race**: coefficient plot for the supply and demand blocks, with confidence intervals.
5. **Model paths and counterfactuals**: agricultural employment share under baseline, freeze-mechanisation, freeze-pipeline, freeze-mortality, 1950-2020, with data medians overlaid.
6. **The replication table as a forest plot**: our elasticities against BKKM's preferred values, with confidence intervals.
