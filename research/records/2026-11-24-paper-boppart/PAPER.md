# Cheap inputs, expensive labour: a partial replication and a sequencing test of Boppart, Kiernan, Krusell and Malmberg (2023)

**Manuscript draft for a replication venue (JCRE / IJR / JDE replication section).**
Prepared 24 November 2026. Pre-registration for the underlying estimates was committed before data work in the
two source records (`research/records/2026-11-23-subsistence/`, first commit `d47e5ed`;
`research/records/2026-11-23-subsistence-v2/`, first commit `62730fc`).

## Abstract
Boppart, Kiernan, Krusell and Malmberg (2023) argue that agriculture is labour-intensive in poor countries
because non-agricultural productivity is low, which makes investment and intermediate goods expensive relative
to labour, so farmers substitute the cheap factor (labour) for the expensive ones. We rebuild the objects this
argument needs from public agricultural, price and macro data for up to 182 countries and re-estimate them. The
cross-sectional mechanism replicates in direction and roughly in magnitude: the relative price of inputs and
input intensity are strongly negatively associated (-1.13, SE 0.15, in 2005 and -1.28, SE 0.11, in 2015), the
estimated substitution elasticities exceed one (1.24 and 1.11 in 2005), input intensity rises by roughly 570 to
640 times from the poorest to the richest countries, and input intensification accounts for 55 to 69 per cent of
the agricultural labour-productivity gap, against the paper's "a bit less than two-thirds". But our elasticities
are **lower** than the paper's (1.24 and 1.11 against 1.90 and 1.75) and the land elasticity **cannot be
estimated** without land-quality data, so this is a partial replication, not a confirmation. We then test the
dynamic sequence the mechanism implies — inputs adopted before labour leaves agriculture — and cannot identify
it: in a ten-year country panel the contemporaneous association has the wrong sign (+1.75, SE 0.71), the reverse
association is stronger (-3.32, SE 0.70), and past changes in intensity do not predict the next decade's labour
release. The downstream link from labour release to schooling and fertility is a precise null at that horizon
(fertility change -0.0003, SE 0.0058, n = 503). A joint demography-agriculture model reproduces the shape of the
transition as a demonstration but only two of its five free parameters are identified, so it is evidence about
model structure, not about history. We also document that an earlier test used in this project — a world
commodity-price index interacted with the farm-employment share — measured none of the paper's objects.

## 1. Introduction

Structural transformation is one of the few robust regularities in development economics: as countries grow,
labour leaves agriculture. What is less settled is why the agricultural sector in poor countries uses so much
labour. One family of explanations emphasises the supply of labour, another the technology available to farmers,
and a third the prices they face. Boppart, Kiernan, Krusell and Malmberg (2023) — hereafter BKKM — give the
price explanation a precise form. In a nested CES production function, if non-agricultural productivity is low,
investment goods and intermediate inputs are expensive relative to labour. A farmer facing expensive capital and
expensive fertiliser but cheap labour will farm with many hands and few machines. As non-agricultural
productivity rises, inputs become cheaper relative to labour, farms intensify, and labour is released. The
mechanism is elegant and it organises a large set of facts, but it makes a strong quantitative demand: the
elasticity of substitution between inputs and labour must exceed one for the price-induced intensification to be
large, and inputs must account for a substantial share of the cross-country productivity gap.

This paper does three things. First, it re-estimates the objects that demand requires, from a rebuilt dataset.
Second, it tests the dynamic sequence the mechanism implies, which the original paper does not estimate. Third,
it reports what the data cannot settle, including a correction to an earlier test used in this project that did
not measure the paper's objects at all.

**What was tested before, and why it was not a test of this paper.** An earlier stage of this project examined
the agricultural transition by regressing farm exit, wage-sector job shares and births on a **world commodity
price index interacted with the agricultural employment share**. The rationale was that a commodity-price shock
hits countries differently depending on how much of their labour is in agriculture, so the interaction should
trace the transition. The estimated effects were small and fragile: farm exit fell from +0.024 to +0.012 once
country trends were included, the wage-job association went from -0.014 to -0.0035 and lost significance, and
the births association was indistinguishable from zero. Those numbers are not evidence about BKKM's argument,
because the test contains **none of the paper's objects**. There is no input quantity in it, no relative input
price, no substitution elasticity, no cross-country development decomposition. It measures the exposure of farm
employment to a common world price shock. Whatever that is, it is not the intensive-margin mechanism BKKM
propose, and it could not have detected that mechanism even if the mechanism were true and large. Stating this
plainly matters for how the earlier result is read: the null from the old test carries no information about
BKKM, in either direction.

**What this paper adds.** A rebuild of the paper's data objects from public sources; a partial replication of
its cross-sectional estimates with an explicit account of where ours differ and why; a dynamic test of the
sequencing that the mechanism requires and that the original paper does not provide; a precise null on the
labour-release-to-demography link at decadal horizons; and a demonstration model that connects agriculture,
demography and the schooling pipeline. The replication is partial and the sequencing test is negative. We state
both as findings rather than as obstacles.

**Preview of results.**
1. The relative-price-to-intensity link replicates: -1.13 (SE 0.15, n = 126) in 2005 and -1.28 (SE 0.11,
   n = 128) in 2015.
2. The estimated substitution elasticities exceed one but are below the paper's: 1.24 (SE 0.08) for capital
   against labour and 1.11 (SE 0.08) for intermediates against labour in 2005, against the paper's 1.90 and
   1.75; at the development extremes ours reach 1.73 and 1.76. The land elasticity cannot be estimated here.
3. Input intensity and the agricultural employment share are strongly negatively associated (-4.71, SE 0.89,
   n = 126; -4.38, SE 1.15, n = 128), while the relative-price coefficient in that equation is positive as
   predicted but not significant.
4. Input intensification accounts for 55 to 69 per cent of the agricultural labour-productivity gap, consistent
   with the paper's approximate two-thirds.
5. The implied sequencing is **not identified** in a ten-year country panel: the contemporaneous level
   association is positive (+1.75, SE 0.71), the reverse association is stronger (-3.32, SE 0.70), and past
   changes in intensity and price do not predict future labour release.
6. Labour release does not predict schooling or fertility changes at ten-year horizons: the fertility
   coefficient is -0.0003 (SE 0.0058) with n = 503 and a minimum detectable effect of about 0.016 births.
7. A joint model reproduces the stylised transition as a demonstration, but only two of its five free
   parameters are recovered from the data it is fitted to, so its counterfactuals are illustrative.

## 2. The paper under examination

BKKM's argument has three links. **(i)** Non-agricultural productivity determines the price of investment and
intermediate goods relative to labour. **(ii)** Farmers substitute between these inputs and labour according to a
nested CES technology whose elasticities exceed one, so when inputs are expensive they are used sparingly and
labour is used intensively. **(iii)** Because poor countries have low non-agricultural productivity, their
agriculture is labour-intensive, which accounts for a large share of the cross-country gap in agricultural
labour productivity. The accounting follows: agricultural output per worker is a function of total factor
productivity, land per worker and input intensity; if intensity varies enormously across countries, and if it
varies because of relative prices, then much of the measured productivity gap is an input-intensity gap rather
than a technology gap.

Three features of the argument matter for a replication. First, the elasticities are not a side calculation:
the quantitative size of the intensification channel is governed by them, and a value below one would reverse
the sign of the mechanism for the relevant range. Second, the decomposition into TFP, land and inputs requires
a land-quality adjustment, because otherwise land quality is absorbed into the residual and the input share is
misattributed. Third, the argument is essentially **comparative statics across countries**. It implies a
sequence over time — as non-agricultural productivity grows, inputs get cheaper, intensity rises, and labour is
released — but the paper's evidence is a cross-section. The sequence is an implication, not an estimate.

The antecedent literature is large and we do not claim to discover it. Restuccia and Rogerson (2008) and
Restuccia, Yang and Zhu (2008) established that agricultural productivity differences across countries are
large and matter for aggregate income; Gollin, Parente and Rogerson (2002) framed the role of agriculture in
development; Caselli and Coleman (2001) showed how structural transformation and regional convergence interact;
Herrendorf, Rogerson and Valentinyi (2014, 2013) systematised the structural-change facts and the preference
specifications that generate them; Alder, Boppart and Müller (2022) developed a structural-change theory
designed to fit the data; Alvarez-Cuadrado, Long and Poschke (2017) studied capital-labour substitution as a
driver of structural change; Gollin, Lagakos and Waugh (2014) documented the agricultural productivity gap
across countries and within them; and Duarte and Restuccia (2010) connected structural transformation to
aggregate productivity growth. BKKM's contribution within this literature is to put input prices and input
intensity at the centre of the explanation and to estimate the elasticities that make the channel
quantitatively important. Our replication asks whether those elasticities and that decomposition survive an
independent rebuild.

## 3. Data rebuild and deviations

The paper's online appendix contains no data. Everything below is therefore rebuilt from public sources, and the
paper's published values are used as the comparison point rather than recomputed from their files. The full
inventory, with file paths and every deviation, is in `DATA_AVAILABILITY_AND_DEVIATIONS.md`; here we summarise.

**Quantities.** Agricultural capital, labour, intermediates, land and output come from the USDA Economic
Research Service agricultural input-output accounts, which cover 182 countries from 1961 to 2023. These give the
input ratios at the heart of the argument: capital per worker, intermediates per worker, and land per worker.

**Prices.** Relative input prices are built from the Penn World Table: the price level of investment, the labour
share and GDP per worker. The relative price of inputs is the log of the investment price level minus the log of
labour compensation per worker, following the paper's logic rather than its exact construction.

**Outcomes and controls.** The agricultural employment share, GDP per capita, urbanisation, fertility and
population are from the World Bank's World Development Indicators, pulled from the API for this project
(207,622 rows). Demography for the joint model comes from the project's long-run transition panel.

**Deviations, in order of importance.** (1) **No land-quality adjustment.** The paper uses GAEZ
agro-ecological zones; without them the land margin is absorbed into TFP and **the land elasticity cannot be
estimated**. This is the largest deviation and it is the reason one of the paper's four elasticities is absent
from our table rather than estimated imprecisely. (2) **No country-specific intermediate input prices.** The
paper uses bilateral trade prices from BACI; we use the non-agricultural price level as a proxy. A common
component in prices will attenuate the estimated substitution elasticities, which is the most plausible
explanation for why ours are lower than the paper's. (3) **No household-survey cost shares.** Land and
intermediate cost shares are assumed and documented rather than measured from LSMS data. (4) **Two benchmark
years**, 2005 and 2015, rather than the paper's single cross-section; both are reported so the reader can see
year sensitivity. (5) **Samples differ**: 127 countries in 2005 and 128 in 2015, against the paper's sample,
which we cannot reproduce. (6) **Labour is an index**, not hours. (7) **The dynamic panel is our construction**,
not a re-estimate of a paper claim.

Two consequences follow and we state them at the outset. The replication is **partial by construction**: with
attenuated prices and no land quality, our estimates are biased toward zero relative to the paper's, so a
finding that they are lower is not a refutation. And the **sample is ours**, so differences in point estimates
could reflect sample composition as well as method.

## 4. Design

We estimate six objects. Each was pre-registered in the source records, with the expected sign and the test that
would falsify it, before the data were assembled.

**T1, the elasticities and the decomposition.** For each benchmark year we estimate a nested CES relationship
between inputs and labour across countries, in the form the paper uses: the log input-labour quantity ratio as a
function of the log relative input price, with the estimated coefficient interpreted as the elasticity of
substitution. We report the elasticity at the full sample, at the development extremes (the richest and poorest
deciles, matched in size), and the cross-country change in input intensity from the poorest to the richest
country. We then decompose the agricultural labour-productivity gap: how much is accounted for by input
intensity versus residual TFP and land. The land term is reported as unavailable for the reason given above.

**T2a, the price-to-intensity link.** Cross-section regression of log input intensity on the log relative input
price, for 2005 and 2015.

**T2a2, intensity to the employment share.** Cross-section regression of the agricultural employment share on
input intensity, the relative input price and log income.

**T2b, the sequencing test.** A ten-year country panel: the change in the agricultural employment share from t
to t+10 regressed on intensity at t, with country and decade fixed effects and standard errors clustered by
country. The pre-registered direction for the mechanism is negative: more intensive farms at t should release
more labour by t+10. We also estimate the **reverse** association (past change in the employment share on
current intensity) because a mechanism that cannot beat its own reverse is not identified by this design, and
we test whether past **changes** in intensity and price predict future release.

**T2c, the downstream link.** Changes in secondary schooling completion and in fertility regressed on labour
release and intensity, with income and urbanisation controls, at the same ten-year horizon.

**T3, the joint model.** A demonstration model with three blocks: BKKM-style agricultural production with
substitution elasticity 1.5 (estimated in T1); a demographic block in which desired surviving children fall with
schooling and births equal desired children divided by survival; and an absorbing block in which a wage sector
of finite capacity plus a schooling/credential queue receives the released labour. Five free parameters are
calibrated jointly to 1950-2020 stylised-country medians, and the model is then asked what happens under
counterfactual freezes. A parameter-recovery exercise re-simulates from known values and re-fits.

**Inference and reporting.** Standard errors are heteroskedasticity-robust for cross-sections and clustered by
country for panels. Samples are always named. Every null is reported with its minimum detectable effect. The
pre-registered falsifiers were: for T2a, a non-negative price coefficient; for T2a2, intensity with a positive
sign; for T2b, a negative contemporaneous and a weaker reverse association; for T2c, a detectable negative
fertility effect. The first two did not fire; the last two did.

## 5. Results

### 5.1 The cross-section replicates in direction, not in magnitude

The relative-price mechanism is present. Regressing log input intensity on the log relative input price gives
**-1.13 (SE 0.15) with n = 126 countries in 2005** and **-1.28 (SE 0.11) with n = 128 in 2015**: where inputs are
expensive relative to labour, farms use less of them. This is the paper's first link and it replicates in both
benchmark years.

The elasticities are above one but below the paper's published values:

| object | our 2005 | our 2015 | paper |
|---|---|---|---|
| capital-labour elasticity | 1.24 (SE 0.08) | 1.40 (SE 0.07) | 1.90 |
| intermediates-labour elasticity | 1.11 (SE 0.08) | 1.27 (SE 0.07) | 1.75 |
| same, matched at the development extremes | 1.73 | 1.73 | 1.90 |
| intermediates at the extremes | 1.76 | 1.64 | 1.75 |
| capital-labour quantity ratio, poorest to richest | 570x | 557x | 300-800x |
| intermediates-labour quantity ratio, poorest to richest | 637x | 394x | 300-800x |
| land elasticity | not estimable | not estimable | in the paper's nesting |

Four of these rows need comment. First, the elasticities are **lower** than the paper's, and the most likely
reason is our price proxy: if the measured relative price contains a common component, the classical
attenuation result applies and the estimated elasticity is biased toward one. The development-extreme estimates
(1.73, 1.76) are much closer to the paper's, which is what attenuation of this kind would produce: at the
extremes, the cross-country variation in relative prices is largest relative to the noise. Second, the quantity
ratios replicate in magnitude: a rise of 570 to 637 times in capital or intermediates per worker between the
poorest and richest countries is inside the paper's reported 300-800 fold range. Third, the **land elasticity
is not estimated at all**, because without land-quality data the land share is absorbed into the residual. An
honest replication reports this row as missing rather than filling it with a number that cannot be interpreted.
Fourth, the estimates are **not a confirmation of the paper's point values**: they are consistent with the
direction and with elasticities above one, and they are lower. A reader who wants the paper's elasticities
confirmed will not find that here.

### 5.2 Inputs account for a bit less than two-thirds of the productivity gap

Decomposing the cross-country gap in agricultural labour productivity between the poorest and richest deciles,
input intensification accounts for **55 to 69 per cent** of the gap depending on the decomposition used (the
USDA input index gives 55 to 61 per cent; the cost-share decomposition gives 69 per cent). The paper's
characterisation is "a bit less than two-thirds", and our range brackets that statement. The remaining 31 to 45
per cent is residual TFP and land, with the land component unidentifiable in our data. This is the most
reassuring of the replication results, because the decomposition is a matter of accounting rather than of
estimated elasticities: if the quantity data are right, the shares follow.

### 5.3 Intensity and the agricultural employment share

Across countries, input intensity is strongly negatively associated with the agricultural employment share:
**-4.71 (SE 0.89) with n = 126 in 2005** and **-4.38 (SE 1.15) with n = 128 in 2015**, controlling for income. The
relative-price coefficient in the same equation is positive as the mechanism predicts (+1.11, SE 2.23 in 2005;
+4.02, SE 3.40 in 2015) but not distinguishable from zero. So the cross-sectional picture is: expensive inputs
go with low intensity (strong), low intensity goes with more agricultural employment (strong), but the
price-to-employment link conditional on intensity is not precisely estimated in a sample of 126 to 128
countries. This is a partial replication of the second link, and the imprecision is a sample-size fact rather
than an objection.

### 5.4 The sequencing is not identified, and the reverse is stronger

This is the part of the argument that the original paper leaves as an implication, and it is where our results
turn negative. The mechanism requires that input adoption precede labour release: as inputs get cheaper,
intensity rises, and the labour that is no longer needed leaves. A ten-year panel with country and decade fixed
effects gives the opposite level association: **+1.75 (SE 0.71)** on intensity, meaning that more intensive
agriculture at t is followed by a *smaller* fall (or a rise) in the agricultural employment share over the next
decade. The reverse association — the past change in the employment share predicting current intensity — is
stronger: **-3.32 (SE 0.70)**.

The natural interpretation is convergence and simultaneity. Both variables are moving toward their
cross-sectional relationship, and a country that is releasing labour rapidly also tends to be one where
intensity is rising; each predicts the other. When we restrict attention to past **changes** in intensity and in
price, neither predicts the next decade's labour release (both nulls, n = 472), and the only stable predictor of
the change in the agricultural employment share is its own level (-0.53, SE 0.10), which is convergence. In other
words: the cross-sectional relationship is real, and this design cannot order the two variables in time.

That is a meaningful negative for the mechanism as a statement about transitions. It does not contradict BKKM,
whose evidence is cross-sectional; it says that the country panel available here cannot supply the dynamic
evidence that would turn the cross-section into a causal account. It also explains why historical case studies
matter: only a design that dates input adoption and labour release independently can order them, which is a
different paper.

### 5.5 Labour release does not move schooling or fertility at decadal horizons

The downstream link is a precise null. Regressing the ten-year change in secondary schooling completion on
labour release and intensity gives **-0.16 (SE 0.25)** and **-1.18 (SE 3.20)** with n = 278. Regressing the
ten-year change in fertility gives **-0.0003 (SE 0.0058)** and **-0.005 (SE 0.050)** with n = 503, controlling
for income and urbanisation. The minimum detectable effect on the fertility coefficient is about **0.016
births**, so this is not an underpowered study: an effect of the size that a labour-release story would need
would have been seen. At ten-year country-panel horizons, labour leaving agriculture does not visibly move
schooling or births.

This null sits awkwardly with the project's other records, which find schooling and fertility transitions at
longer horizons and in historical cases. The reconciliation we offer is horizon: the demographic transition is a
process of generations, and a decade is too short to see it in a country panel. The null is therefore a
statement about what a decadal panel can detect, and the model in the next section operates at the longer
horizon at the cost of being a demonstration rather than an estimate.

### 5.6 The joint model: a demonstration, and only two of five parameters are identified

The v1 model, with three free parameters, reproduces the stylised transition and delivers a counterfactual that
is interesting in its own right: freezing mechanisation after 1960 leaves the agricultural employment share at
**17.9 per cent in 2020 against 8.1 per cent** in the baseline, schooling at **5.6 against 8.2 years**, and
fertility at **2.52 against 2.19 births**. Mechanisation is the margin that empties agriculture and, through the
queue, feeds the schooling pipeline.

The v2 model repairs two failures of v1 — the agricultural share was falling too fast and population was
growing too fast — by adding an explicit wage sector with its own job-creation rate and a schooling queue, and
by calibrating agricultural TFP growth and the food-demand elasticity. It brings the agricultural share to
**17.6 per cent against 19.4 in the data** (inside the pre-registered 5-point tolerance) but overshoots the
population repair: the population index is **1.58 against 2.92**, now too slow rather than too fast, because the
fitted mortality-timing shift delays the mortality decline. TFR fits at 2.35 against 2.06 and schooling at 7.53
against 9.57 years.

The counterfactuals are the part that would matter if the model were estimated:

| freeze | agricultural share | schooling | TFR | population index |
|---|---|---|---|---|
| none (baseline) | 17.6% | 7.5 yrs | 2.35 | 1.58 |
| mechanisation after 1960 | 39.9% | 0.2 yrs | 3.29 | 2.19 |
| the schooling pipeline after 1960 | 18.0% | 3.0 yrs | 2.94 | 1.90 |
| the mortality decline (at its 1800 level) | 18.4% | 7.2 yrs | 3.96 | 0.39 |

Read as structure, the model says three things: mechanisation empties the floor and starves the pipeline
without it schooling collapses to 0.2 years; the pipeline is what converts released labour into schooling and
lower fertility; and the mortality decline is the model's first mover, since freezing it removes the population
explosion altogether. Read as evidence, it says much less, because the parameter-recovery test identifies only
**two of the five free parameters** (agricultural TFP growth and the food elasticity are recovered exactly, the
job-creation rate approximately, while the queue weight and the mortality shift have recovery errors of 2.50 and
2.54). The queue and demography channels are weakly identified, and no structural claim should rest on their
point values.

## 6. Comparison with the original

**Where we agree.** The economic content of BKKM's argument survives an independent rebuild on different data.
Relative input prices and input intensity are strongly negatively related; elasticities are above one; input
intensity rises by hundreds of times between the poorest and richest countries; inputs account for a bit less
than two-thirds of the agricultural labour-productivity gap; and intensity and the agricultural employment share
are strongly negatively related across countries. Three of the paper's four elasticities are replicated in sign
and in being above one, and the decomposition — the accounting result — replicates in magnitude within a few
points. This is the pattern a replication should expect to find if the underlying data construction is sound.

**Where we differ, and why.** Our capital-labour and intermediates-labour elasticities are **lower** than the
published ones: 1.24 and 1.11 against 1.90 and 1.75 in the preferred year, rising to 1.73 and 1.76 at the
development extremes. We do not read this as a refutation. Two features of our rebuild push in that direction:
the relative price is a proxy (the non-agricultural price level rather than BACI country-specific prices), which
attenuates an errors-in-variables estimate; and the sample is ours, not the paper's. The fact that the
development-extreme estimates are close to the paper's is consistent with attenuation: the signal-to-noise ratio
in relative prices is highest at the extremes. A replication cannot distinguish "the paper is slightly high" from
"our proxy is slightly noisy" without the original data, and we say so rather than adjudicating in our own
favour.

**What we could not reproduce at all.** The land elasticity. This is not an imprecision but an absence: without
land-quality adjustment the land margin is absorbed into TFP, and the resulting number would be uninterpretable.
We report the row as not estimable. Anyone comparing our table to the paper's should treat the land row as
missing data, not as a zero or a disagreement.

**The status of the sequencing result.** BKKM's paper is cross-sectional, so our failure to identify the
sequence is not a failure to replicate a claim of theirs. It is a failure to extend their mechanism to the
dynamic question that the mechanism naturally raises. That distinction is worth keeping explicit: the paper
claims that relative prices shape input intensity across countries, and that claim replicates; it does not claim
that input adoption demonstrably precedes labour release in country panels, and we cannot show that it does.

**The old test.** The earlier proxy test in this project — commodity prices interacted with the farm-employment
share — measured the exposure of farm employment to a common world price shock. It contained no input
quantities, no relative input prices, no substitution elasticity and no cross-country decomposition. Its small
and fragile estimates carry no information about BKKM's mechanism, and the correct response to that test is to
replace it, which is what the estimates in this paper do. This is a statement about what the test measured, not
about the people who ran it, and it belongs in the record because otherwise a later reader may treat a null
about commodity-price exposure as a null about intensive agriculture.

## 7. What cannot be tested with rebuildable data

Three things, in increasing order of importance.

**The paper's exact sample and weights.** Without the authors' data we cannot reproduce their sample, so
differences in point estimates confound method with composition. A replication package from the authors would
resolve this in an afternoon, and we recommend the venue request one.

**Land quality and the land margin.** GAEZ or equivalent land-quality data is obtainable but was not assembled
here. It matters because the decomposition attributes the non-input remainder to TFP and land; without land
quality, part of what looks like TFP is land quality. This is the most consequential gap in our rebuild and the
first thing a follow-up should close.

**The dynamic sequence, with any design available to us.** The country panel cannot order input adoption and
labour release because both are converging and each predicts the other. Ordering them requires dated, independent
measures of adoption and release — firm or household panels with input use, or historical case studies with
independent dates, which is a different research design rather than a better regression.

Two further gaps are worth recording. Household-survey cost shares (LSMS) would let the cost-share
decomposition be measured rather than assumed. And the downstream link from labour release to schooling and
fertility is not testable at decadal horizons with country data: the demographic transition is a
multi-generational process, and a ten-year panel cannot see it. The project's other records address that link
with longer historical series and with models, and both of those routes carry their own identification
problems.

## 8. Relation to the literature

This replication sits at the intersection of two literatures. On the substance, it belongs with the structural
transformation literature that treats agriculture's factor proportions as the object (Restuccia & Rogerson,
2008; Restuccia, Yang & Zhu, 2008; Gollin, Parente & Rogerson, 2002; Caselli & Coleman, 2001; Herrendorf,
Rogerson & Valentinyi, 2014, 2013; Gollin, Lagakos & Waugh, 2014; Duarte & Restuccia, 2010; Alder, Boppart &
Müller, 2022; Alvarez-Cuadrado, Long & Poschke, 2017). BKKM's specific contribution within that literature is the
input-price channel and the estimated elasticities that make it quantitatively large; our contribution is to
test whether those estimates survive a rebuild, and to show that the dynamic implication does not follow from
the cross-section.

On method, it belongs with the replication literature in economics and the wider credibility movement
(Christensen & Miguel, 2018; Nosek et al., 2015; Nosek, Spies & Motyl, 2012; Open Science Collaboration, 2015;
Camerer et al., 2016; Mueller-Langer et al., 2019). That literature has established a set of conventions which
this paper follows: pre-registration of the tests before the data are assembled; reporting of every deviation
from the original; separation of what is replicated from what is corrected and what is new; data-availability
statements that name what could not be obtained; and full reporting of nulls with their minimum detectable
effects. The convention that matters most here is the last one: the sequencing null and the downstream null are
results, and a replication venue is the right place for them, because a null with power is information that
never appears in a published positive result.

Replication venues — the *Journal of Comments and Replications in Economics*, the *International Journal for
Re-Research*, and replication sections of field journals — exist precisely for this kind of paper: a serious
re-estimation with honest partial agreement, an explicit gap list, and a negative extension. We have written
this manuscript to their conventions (APA 7; separate data-availability appendix; claims-prior-art table) and we
have avoided any claim of precedence, since the antecedents are extensive and the object-level claim belongs to
BKKM.

## 9. Limitations

Our estimates are a **partial replication**: the elasticities are lower than the paper's, the land elasticity is
missing, the sample is rebuilt and smaller, and prices are proxied. The cross-sectional associations are
correlations across countries, not causal effects, and the paper's own design shares that limitation. The
dynamic panel is our construction and its negative result is a statement about what a ten-year country panel can
identify, not evidence that inputs never precede labour release anywhere. The joint model is a demonstration with
two of five parameters identified; its counterfactuals are useful for thinking about structure and should not be
quoted as historical estimates. The downstream null has a minimum detectable effect of about 0.016 births at ten
years, which is precise for that horizon but says nothing about longer horizons. And the whole exercise is
constrained by the absence of the authors' data, which is the single change that would most improve it.

## 10. Conclusion

Boppart, Kiernan, Krusell and Malmberg's central empirical claim survives an independent rebuild in direction
and roughly in magnitude: input prices shape input intensity, intensity shapes the agricultural employment share,
elasticities exceed one, and inputs account for a bit less than two-thirds of the agricultural
labour-productivity gap. The replication is partial — our elasticities are lower, land is untestable, and the
sample is ours. The mechanism's dynamic implication is not identified in the country panel available to us, and
the implied downstream link to schooling and fertility is a precise null at decadal horizons. We also document
that an earlier test used in this project measured none of the paper's objects, which is why the project's
previous null about intensive agriculture should not be read as evidence about the mechanism. The paper's
argument, on this evidence, is best described as **well supported cross-sectionally and untested dynamically**,
and closing that gap needs data we do not have: land quality, the authors' sample, and dated independent
measures of input adoption and labour release.

## Appendix: files and provenance
- Pre-registrations: `research/records/2026-11-23-subsistence/PRE_REGISTRATION.md` (commit `d47e5ed`);
  `research/records/2026-11-23-subsistence-v2/` pre-registration (commit `62730fc`).
- Estimates: `research/records/2026-11-23-subsistence/results/` (`replication.json`, `corrected_test.json`,
  `model_summary.txt`, `model_paths.csv`, `model_counterfactual.csv`, `model_params.json`).
- Model and sequencing: `research/records/2026-11-23-subsistence-v2/results/` (`model_v2_summary.txt`,
  `model_v2_paths.csv`, `model_v2_counterfactual.csv`, `model_v2_params.json`, `sequencing.txt`,
  `sequencing.json`, `event_dates.csv`).
- Scripts: `pull_wdi.py`, `boppart_replicate.py`, `corrected_test.py`, `model.py` (v1); `pull_us_history.py`,
  `sequencing.py`, `model_v2.py` (v2).
- Data availability and every deviation: `DATA_AVAILABILITY_AND_DEVIATIONS.md`.
- Claim-by-claim prior art with Crossref status: `claims-prior-art.md`. References: `refs.md`.
