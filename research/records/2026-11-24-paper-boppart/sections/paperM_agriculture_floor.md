# Paper M (Massification) — Section: the agricultural floor, a partial replication and a sequencing test of the input-price mechanism

**Author: gpu-dose. Sources: `research/records/2026-11-23-subsistence/` (branch `research/subsistence-2026-11-23`,
commit `41f6429`) and `research/records/2026-11-23-subsistence-v2/` (branch `research/subsistence-v2-2026-11-23`,
commit `ce66cfc`). Pre-registrations committed before data work: `d47e5ed` and `62730fc`.**

## 1. The claim this section tests

Boppart, Kiernan, Krusell and Malmberg (2023) explain why agriculture in poor countries uses so much labour. In
their argument, low non-agricultural productivity makes investment goods and intermediate inputs expensive
relative to labour, so farmers substitute the cheap factor for the expensive ones. As non-agricultural
productivity rises, inputs become cheaper, farms intensify, and labour is released. The mechanism is
cross-sectional in the paper's evidence, but it carries a dynamic implication: **input adoption should precede
the labour release**. This section reports a partial replication of the cross-sectional objects and a test of
the dynamic implication, and it explains why the earlier project null on this topic carries no information
about the mechanism.

The antecedent literature is extensive and none of it is ours. Restuccia and Rogerson (2008) and Restuccia, Yang
and Zhu (2008) established that agricultural productivity gaps across countries are large and matter for
aggregate income; Gollin, Parente and Rogerson (2002) framed agriculture's role in development; Caselli and
Coleman (2001) connected structural transformation to regional convergence; Herrendorf, Rogerson and Valentinyi
(2014, 2013) systematised the structural-change facts; Alder, Boppart and Müller (2022) developed a
structural-change theory built to fit the data; Alvarez-Cuadrado, Long and Poschke (2017) studied capital-labour
substitution as a driver of structural change; Gollin, Lagakos and Waugh (2014) documented the agricultural
productivity gap; and Duarte and Restuccia (2010) linked structural transformation to aggregate productivity.
BKKM's specific contribution within this literature is the input-price channel and the elasticities that make it
quantitatively large.

## 2. What was tested before, and why it was not this

An earlier stage of this project regressed farm exit, wage-sector job shares and births on **a world commodity
price index interacted with the agricultural employment share**, on the reasoning that a common price shock hits
countries differently depending on how much labour they have in agriculture. The estimates were small and
fragile: farm exit fell from +0.024 to +0.012 once country trends were included, the wage-job association moved
from -0.014 to -0.0035 and lost significance, and the births association was indistinguishable from zero.

Those numbers are not evidence about BKKM's argument. The test contains **none of the paper's objects**: there is
no input quantity, no relative input price, no substitution elasticity and no cross-country development
decomposition in it. It measures the exposure of farm employment to a common world price shock. It could not
have detected the input-price mechanism even if that mechanism were true and large. This is a statement about
what the test measured, not about anyone's competence, and it belongs in the paper because otherwise a null
about commodity-price exposure may be read later as a null about intensive agriculture.

## 3. Data rebuild

The paper's online appendix contains no data, so everything here is rebuilt. Agricultural quantities (capital,
labour, intermediates, land, output) come from the USDA Economic Research Service input-output accounts for 182
countries from 1961 to 2023. Relative input prices come from the Penn World Table (investment price level,
labour share, GDP per worker). Outcomes and controls — the agricultural employment share, GDP per capita,
urbanisation, fertility, population — come from the World Bank's World Development Indicators, pulled from the
API for this job (207,622 rows). Demography for the joint model comes from the project's long-run transition
panel.

**Deviations from the original, in order of consequence.** (1) **No land-quality adjustment** (the paper uses
GAEZ): the land margin is absorbed into TFP, and **the land elasticity cannot be estimated**, so that row is
reported as missing rather than filled. (2) **No country-specific intermediate prices** (the paper uses BACI):
we use the non-agricultural price level as a proxy, which attenuates the estimated elasticities. (3) **No
household-survey cost shares**: they are assumed and documented. (4) Two benchmark years, 2005 and 2015, rather
than a single cross-section. (5) Samples of 127 (2005) and 128 (2015) countries, against the paper's sample,
which cannot be reproduced. (6) Labour is an index, not hours. (7) The dynamic panel is our construction, not a
re-estimate of a paper claim. The full inventory is in `DATA_AVAILABILITY_AND_DEVIATIONS.md`.

## 4. The cross-section replicates in direction, not in magnitude

The first link replicates in both benchmark years: log input intensity on the log relative input price gives
**-1.13 (SE 0.15), n = 126** for 2005 and **-1.28 (SE 0.11), n = 128** for 2015. Expensive inputs, low
intensity.

The elasticities are above one but below the paper's published values:

| object | our 2005 | our 2015 | paper |
|---|---|---|---|
| capital-labour elasticity | 1.24 (SE 0.08) | 1.40 (SE 0.07) | 1.90 |
| intermediates-labour elasticity | 1.11 (SE 0.08) | 1.27 (SE 0.07) | 1.75 |
| capital-labour at the development extremes | 1.73 | 1.73 | 1.90 |
| intermediates-labour at the extremes | 1.76 | 1.64 | 1.75 |
| capital-labour quantity rise, poorest to richest | 570x | 557x | 300-800x |
| intermediates-labour quantity rise, poorest to richest | 637x | 394x | 300-800x |
| land elasticity | not estimable | not estimable | in the paper's nesting |

Two readings are possible and a replication must not choose the self-serving one. The attenuation explanation —
our price proxy carries a common component, so the elasticity is biased toward one — is consistent with the
pattern that the development-extreme estimates (1.73, 1.76) are much closer to the paper's than the full-sample
ones. The alternative, that the paper's estimates are somewhat high, cannot be excluded without the authors'
data. We therefore report a **partial replication**: the sign and the above-one property replicate, the point
values do not, and the land margin is untestable.

The accounting result is the most reassuring. Decomposing the cross-country gap in agricultural labour
productivity between the poorest and richest deciles, input intensification accounts for **55 to 69 per cent**
of the gap (USDA input index: 55 to 61 per cent; cost-share decomposition: 69 per cent), bracketing the paper's
"a bit less than two-thirds". Input intensity is also strongly negatively associated with the agricultural
employment share, **-4.71 (SE 0.89), n = 126** and **-4.38 (SE 1.15), n = 128**, though the relative-price
coefficient in that equation is positive as predicted but insignificant (+1.11, SE 2.23; +4.02, SE 3.40).

## 5. The dynamic implication is not identified

The mechanism requires inputs before release. A ten-year country panel with country and decade fixed effects
(507 country-year observations, 128 countries, clustered by country) gives the opposite level association:
**+1.75 (SE 0.71)** on intensity, so more intensive farms at t are followed by a *smaller* fall in the
agricultural employment share. The reverse association is stronger: **-3.32 (SE 0.70)**. Restricting to past
**changes** in intensity and price, neither predicts the next decade's release (both nulls, n = 472), and the
only stable predictor of the change in the agricultural employment share is its own level (-0.53, SE 0.10).

The interpretation is convergence with simultaneity: both variables move toward their cross-sectional
relationship and each predicts the other. The cross-section is real; this design cannot order the two variables
in time. That is a negative for the mechanism as a theory of transitions and it is not a contradiction of BKKM,
whose evidence is cross-sectional. It does explain why the historical case studies in the companion section
matter: only independent dating of adoption and release can order them.

The downstream link is a precise null at the same horizon. The ten-year change in secondary completion on
release and intensity gives **-0.16 (SE 0.25)** and **-1.18 (SE 3.20), n = 278**; the ten-year change in
fertility gives **-0.0003 (SE 0.0058)** and **-0.005 (SE 0.050), n = 503**, with income and urbanisation
controls. The minimum detectable effect on fertility is about **0.016 births**, so the null has power. At
decadal horizons, labour leaving agriculture does not visibly move schooling or births.

## 6. The joint demography-agriculture model: demonstration, not estimate

The v2 model joins three blocks: BKKM-style production with substitution elasticity 1.5; a demographic block in
which desired surviving children fall with schooling and births equal desired children divided by survival; and
an absorbing block in which a wage sector of finite capacity plus a schooling queue receives the released
labour. Five free parameters are calibrated to 1950-2020 stylised-country medians, and counterfactual freezes
are run.

| freeze | agricultural share | schooling | TFR | population index |
|---|---|---|---|---|
| none (baseline) | 17.6% (data 19.4%) | 7.5 yrs (data 9.6) | 2.35 (data 2.06) | 1.58 (data 2.92) |
| mechanisation after 1960 | 39.9% | 0.2 yrs | 3.29 | 2.19 |
| the schooling pipeline after 1960 | 18.0% | 3.0 yrs | 2.94 | 1.90 |
| the mortality decline (1800 level) | 18.4% | 7.2 yrs | 3.96 | 0.39 |

Read as structure, three things follow: mechanisation is the margin that empties the floor (without it schooling
collapses to 0.2 years); the pipeline is what converts released labour into schooling and lower fertility; and
the mortality decline is the model's first mover, since freezing it removes the population explosion entirely.
The agricultural share is repaired to 17.6 against 19.4 per cent, inside the pre-registered tolerance; the
population repair overshoots (1.58 against 2.92, now too slow). Read as evidence, the model says much less: the
parameter-recovery test identifies only **two of the five free parameters** (agricultural TFP growth and the food
elasticity are recovered exactly, the job-creation rate approximately; the queue weight and the mortality shift
have recovery errors of 2.50 and 2.54). **The counterfactuals are illustrations of model structure and are not
historical estimates.**

## 7. Prior art for this section [DOIs Crossref-verified unless marked]

| claim in this section | status | closest prior work | DOI | relation |
|---|---|---|---|---|
| Expensive inputs in poor countries; labour substituted in | replicated (cross-section) | Boppart, Kiernan, Krusell & Malmberg (2023) | 10.3386/w31101 | we re-estimate the object on rebuilt data; point values lower |
| Substitution elasticities above one | replicated in sign, not in magnitude | BKKM; Alvarez-Cuadrado, Long & Poschke (2017); Alder, Boppart & Müller (2022) | 10.3982/te2106; 10.1257/mac.20190303 | ours are lower; land untestable |
| Inputs explain about two-thirds of the productivity gap | replicated in magnitude | BKKM; Gollin, Lagakos & Waugh (2014); Duarte & Restuccia (2010) | 10.1093/qje/qjt056; 10.1162/qjec.2010.125.1.129 | ours 55-69 per cent |
| Intensity and the employment share | replicated | BKKM; Herrendorf, Rogerson & Valentinyi (2013) | 10.1257/aer.103.7.2752 | rebuilt cross-section |
| Input adoption precedes labour release | **new test; not identified** | BKKM is cross-sectional; Alder et al. and Alvarez-Cuadrado et al. supply the dynamic theory | as above | negative result |
| Release feeds schooling and fertility at ten years | **new test; precise null** | no antecedent at this horizon | — | null with power |
| The old proxy test did not measure the object | **correction** (internal to this project) | none: it is the project's own earlier test | — | factual restatement |
| Joint demography-agriculture model | **new demonstration** | Alder, Boppart & Müller (2022); BKKM; Herrendorf et al. (2014) | as above | 2 of 5 parameters identified |
| Restuccia & Rogerson (2008), Agriculture and structural transformation | antecedent | chapter not returned by Crossref in-session; related verified chapter Rogerson (2019) | 10.1093/oxfordhb/9780198793847.013.2 | framing, not an estimate |
| Herrendorf, Rogerson & Valentinyi (2014) | antecedent | working-paper version verified | 10.3386/w18996 | structural-change facts |
| Caselli & Coleman (2001) | antecedent | verified | 10.1086/321015 | structural transformation and convergence |
| Gollin, Parente & Rogerson (2002) | antecedent | verified | 10.1257/000282802320189177 | agriculture in development |
| Restuccia, Yang & Zhu (2008) | antecedent | verified | 10.1016/j.jmoneco.2007.11.006 | agricultural productivity gaps |

**No claim of precedence is made anywhere.** The object-level claim belongs to BKKM; the dynamic test is new to
this project but the historical and theoretical literature on the sequencing of mechanisation and labour release
is large, and we cite the closest works rather than asserting novelty. What this section offers is a partial
replication with an explicit gap list, a negative dynamic test, and the removal of a proxy test that was being
read as if it were evidence about this mechanism.
