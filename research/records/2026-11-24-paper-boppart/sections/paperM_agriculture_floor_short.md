# Paper M — Agricultural floor: Boppart/Kiernan/Krusell/Malmberg replication and sequencing test (short draft, ~950 words)

**Provenance: `research/subsistence-2026-11-23` @ `41f6429` (pre-registered at `d47e5ed`) and
`research/subsistence-v2-2026-11-23` @ `ce66cfc` (pre-registered at `62730fc`). Field paths in brackets refer to
the results files in those records.**

Boppart, Kiernan, Krusell and Malmberg (2023) — BKKM — explain why poor-country agriculture uses so much
labour: low non-agricultural productivity makes investment and intermediate goods expensive relative to labour,
so farmers substitute the cheap factor in; as non-agricultural productivity rises inputs get cheaper, farms
intensify, and labour is released. Their evidence is cross-sectional, but the argument implies a sequence:
**inputs before labour release**. We re-estimated the cross-sectional objects on rebuilt data and tested the
sequence.

**The earlier test was not this paper's object.** An earlier stage of this project regressed farm exit, wage jobs
and births on a world commodity-price index interacted with the agricultural employment share; farm exit fell
from +0.024 to +0.012 with country trends, wage jobs from -0.014 to -0.0035 and lost significance, births were
indistinguishable from zero (record `README.md`, section 1). That test contains none of BKKM's objects: no input
quantities, no relative input prices, no substitution elasticity, no development decomposition. It measures the
exposure of farm employment to a common world price shock and could not have detected the input-price mechanism
even in principle. Its null carries no information about BKKM in either direction.

**Rebuild.** The paper's appendix contains no data, so everything is rebuilt: USDA ERS agricultural quantities
(182 countries, 1961-2023), Penn World Table relative input prices, World Bank WDI outcomes and controls
(207,622 rows), and the project's long-run transition panel for demography. Seven deviations are documented in
`DATA_AVAILABILITY_AND_DEVIATIONS.md`; the two that matter are no land-quality adjustment (so **the land
elasticity is not estimable**) and no country-specific intermediate prices (the non-agricultural price level is
a proxy, which attenuates the elasticities).

**Cross-section: direction replicated, magnitude not.** Log input intensity on the log relative input price:
**-1.13 (SE 0.15), n = 126** in 2005 and **-1.28 (SE 0.11), n = 128** in 2015
[`results/corrected_test.json`]. The elasticities are above one but below the paper's: capital-labour **1.24 (SE
0.08)** in 2005 and **1.40 (SE 0.07)** in 2015, intermediates-labour **1.11 (SE 0.08)** and **1.27 (SE 0.07)**,
against the paper's 1.90 and 1.75; at the development extremes ours reach **1.73** and **1.76**
[`results/replication.json`, fields `sigma_k_l_2005`, `sigma_m_l_2005`, `sigma_k_l_2015`, `sigma_m_l_2015`].
Input quantities rise **570x** (capital) and **637x** (intermediates) from poorest to richest in 2005, inside
the paper's 300-800x range. Input intensification accounts for **55.0 to 69.4 per cent** of the agricultural
labour-productivity gap [fields `usda_input_share_2005` = 0.550 and `input_share_2005_paper-` = 0.694], against
the paper's "a bit less than two-thirds". Intensity and the agricultural employment share are strongly
negatively related, **-4.71 (SE 0.89), n = 126** and **-4.38 (SE 1.15), n = 128**; the relative-price coefficient
in that equation is positive as predicted but insignificant.

This is a **partial replication, not a confirmation**. The attenuation explanation (proxy prices) is consistent
with the extremes sitting close to the paper's values while the full sample sits below; but without the authors'
data we cannot distinguish "the paper is slightly high" from "our proxy is slightly noisy", and we say so.

**Sequencing: not identified.** A ten-year country panel with country and decade fixed effects (503
country-year observations, 128 countries, clustered) gives the wrong-signed level association: change in the
agricultural employment share on intensity at t is **+1.75 (SE 0.71)**, so more intensive farms at t release
*less* labour over the next decade [`corrected_test.json`, T2b `log_intensity`]. The reverse association is
stronger: past agricultural-share change on current intensity is **-3.32 (SE 0.70), n = 383**
[`corrected_test.txt`, "reverse check"]. Past **changes** in intensity and price do not predict future release
(both nulls, n = 472); the only stable predictor of the change in the agricultural share is its own level
(**-0.53, SE 0.10**), i.e. convergence. Both variables converge and each predicts the other, so this design
cannot order them in time. The cross-section is real; the sequence is not established.

**Downstream: a precise null.** Ten-year change in secondary completion on labour release and intensity:
**-0.16 (SE 0.25)** and **-1.18 (SE 3.20), n = 278**; ten-year fertility change: **-0.0003 (SE 0.0058)** and
**-0.005 (SE 0.050), n = 503**, with income and urbanisation controls [T2c]. The minimum detectable fertility
effect is about **0.016 births**, so the null has power at this horizon.

**Joint demography-agriculture model: demonstration.** BKKM-style production with substitution elasticity 1.5,
a quantity-quality demographic block, and a wage sector plus schooling queue absorbing released labour; **five
free parameters**, all calibrated to 1950-2020 stylised-country medians [`model_v2_summary.txt`]. Repair status:
the agricultural share reaches **17.6 per cent against 19.4 in the data** (inside the 5-point pre-registered
tolerance), TFR **2.35 vs 2.06**, schooling **7.5 vs 9.6 years**, while the population index is **1.58 vs 2.92**
— the population repair failed in the other direction (too slow). Counterfactuals in 2020: freezing
mechanisation leaves the agricultural share at **39.9 per cent**, schooling at **0.2 years** and TFR at **3.29**;
freezing the schooling pipeline leaves schooling at **3.0 years** and TFR at **2.94**; freezing the mortality
decline takes the population index to **0.39** and TFR to **3.96**. The mortality decline is the model's first
mover, mechanisation empties the floor, and the pipeline converts released labour into schooling. But the
parameter-recovery test identifies only **two of the five free parameters** (agricultural TFP growth and the food
elasticity recovered; the job-creation rate approximately; the queue weight and mortality shift have errors of
**2.50** and **2.54**), so the counterfactuals illustrate structure and are **not historical estimates**.

**Prior art (DOIs Crossref-verified unless marked).** BKKM (2023) 10.3386/w31101 (verified, working paper;
SSRN version 10.2139/ssrn.4413838 verified); Gollin, Lagakos & Waugh (2014) 10.1093/qje/qjt056 (verified);
Duarte & Restuccia (2010) 10.1162/qjec.2010.125.1.129 (verified); Alvarez-Cuadrado, Long & Poschke (2017)
10.3982/te2106 (verified); Alder, Boppart & Müller (2022) 10.1257/mac.20190303 (verified); Restuccia, Yang & Zhu
(2008) 10.1016/j.jmoneco.2007.11.006 (verified); Caselli & Coleman (2001) 10.1086/321015 (verified);
Herrendorf, Rogerson & Valentinyi (2013) 10.1257/aer.103.7.2752 (verified); Restuccia & Rogerson (2008) chapter
(**not** returned by Crossref in-session; related verified chapter Rogerson 2019,
10.1093/oxfordhb/9780198793847.013.2). The replicated objects are BKKM's; the sequencing and downstream tests are
new to this project; no claim of precedence is made, and no causal claim is made from the cross-section.
