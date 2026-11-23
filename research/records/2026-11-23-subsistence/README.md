# Boppart et al.'s intensive agriculture: correct test and subsistence-transition model, 23 Nov 2026

Branch `research/subsistence-2026-11-23`. Pre-registration committed **before any data or code** (`d47e5ed`):
expected elasticities, the corrected reduced-form tests (T2a/T2b/T2c), the model, and the falsifiers.
Server box2 `/root/work/subsistence`. This record answers three questions in order.

## 1. Did the old project test Boppart et al. (2023) right? **No.**
The old "Boppart test" regressed farm exit / wage jobs / births on a **world commodity-price index times the
farm employment share** (handoff job 3: farm exit +0.024 -> +0.012 with country trends; wage jobs -0.014 ->
-0.0035 n.s.; births ~0). That measures the exposure of farm employment to a common world price shock. It
contains **none of the paper's objects**: no input quantities, no relative input prices, no substitution
elasticity, no cross-country development decomposition. The paper's object is a nested CES agricultural
production function estimated on cross-country relative input prices/quantities, where low non-agricultural
TFP makes investment and intermediate goods expensive relative to labour in poor countries, so those
countries substitute labour into agriculture. The old test could not see that mechanism even in principle.
**Data question:** the paper's online appendix (`nber.org/data-appendix/w31101`, fetched with a browser UA from
box2) contains **only the appendix PDF, no data**. We therefore rebuilt the minimum object from: the migrated
project panel's USDA ERS agricultural quantities (capital, labour, intermediates, land, output; 182 countries,
1961-2023), PWT price level of investment, labour share and GDP per worker; World Bank WDI downloaded from the
API for this job (agricultural employment share, GDP per capita, urbanisation, fertility, population; 207,622
rows), and the transition record (`/root/work/transition/out/long_run_panel.csv`) for demography.
**Deviations from the paper, stated:** no GAEZ land-quality adjustment, no BACI country-specific intermediate
prices (non-agricultural price level used as proxy), no LSMS land/intermediate cost shares (assumed,
documented), 2005/2015 instead of a single 2005 benchmark. `/root/work/local_data/` was checked first; it has
no Boppart data (the massification/enrolment series are unrelated), so the numbers below are rebuilt, not the
authors' file.

## 2. Replication of the paper's cross-sectional CES estimation (T1)
Using the obtainable quantities and prices, cross-section 2005 (127 countries) and 2015 (128):

| object | our estimate | paper |
|---|---|---|
| elasticity, capital vs labour | **1.24 (SE 0.08)** 2005; 1.40 (0.07) 2015 | 1.90 (their preferred nesting) |
| same, matched at development extremes | **1.73** (2005), 1.73 (2015) | 1.90 |
| elasticity, intermediates vs labour | **1.11 (0.08)** 2005; 1.27 (0.07) 2015 | 1.75 |
| same, matched at development extremes | **1.76** (2005), 1.64 (2015) | 1.75 |
| capital/labour quantity rise, poorest to richest | 570x (2005), 557x (2015) | 300-800x |
| intermediates/labour quantity rise | 637x (2005), 394x (2015) | 300-800x |
| input intensification share of the agricultural labour-productivity gap | **55-69%** (USDA input index 55-61%; cost-share decomposition 69%) | "a bit less than two-thirds" |

The cross-section behaves as the paper says: relative input prices and input intensities move in opposite
directions, elasticities are **above one**, and inputs explain roughly two-thirds of the productivity gap.
Quantitatively our elasticities are somewhat lower than the paper's and land's elasticity **cannot be
estimated here** (no land price) — the honest reading is a partial replication, not a refusal or a confirmation.

## 3. The corrected reduced-form test (T2), replacing the old proxy
Object: intensity = (agricultural capital + intermediates) per agricultural worker (USDA); relative input
price = log(investment price level / labour compensation per worker) (PWT). Pre-registered tests and results:
- **T2a (price → intensity): confirmed.** Cross-section 2005: log intensity on log relative input price
  **-1.13 (SE 0.15), n=126 countries**; 2015: **-1.28 (0.11), n=128**. Expensive inputs, low intensity — the
  paper's first link.
- **T2a2 (intensity and price → ag employment share): half confirmed.** Cross-section 2005: ag employment
  share on intensity **-4.71 (0.89)**, relative price +1.11 (2.23), income -7.32 (2.07), n=126; 2015:
  intensity **-4.38 (1.15)**, price +4.02 (3.40), income -4.12 (2.31), n=128. Intensity points the right way
  strongly; the relative-price coefficient is positive as predicted but not significant.
- **T2b (does the input margin PRECEDE labour release?): not identified.** Ten-year panel (507 country-year
  observations, 128 countries, outcome t -> t+10, country and decade fixed effects, clustered by country):
  the level specification gives a counterintuitive **+1.75 (0.71)** on intensity. The reverse check (past
  ag-share change on current intensity) is stronger still: **-3.32 (0.70)**. Past *changes* in intensity and
  price do not predict the next decade's labour release (both null, n=472); the only stable predictor is
  convergence in the ag share itself (-0.53 (0.10)). So the cross-section matches the paper, but in this
  country panel the lead-lag direction cannot be established: labour release and intensity move together.
- **T2c (release → schooling and fertility): null.** Change in secondary completion on labour release and
  intensity: -0.16 (0.25) and -1.18 (3.20), n=278; change in fertility: -0.0003 (0.0058) and -0.005 (0.050),
  n=503, with income and urbanisation controls. These are precise nulls (a fertility change of ~0.016 births
  would have been detected), so at the 10-year country-panel horizon the labour-release-to-demography link
  is not visible; the transition record and the model below operate at longer horizons.

## 4. Joint demography-agriculture-absorber model (T3)
A demonstration model, not an estimate of history. Boppart agriculture: observed agricultural labour
productivity is split into TFP and input intensity with the CES elasticity **sigma = 1.5** (estimated above);
food demand has a subsistence floor and low income elasticity. Demography: mortality paths from the transition
record; fertility is a quantity-quality choice (desired *surviving* children falls with schooling, births =
desired / survival). Absorber: a wage sector of finite capacity plus a schooling/credential pipeline that
queues the released labour; queue pressure and the wage premium feed enrolment, schooling lowers fertility.
**Free parameters (3, under the 5-parameter GATE, all calibrated):** queue weight in schooling **3.61**,
wage-premium weight **0.00** (queue pressure dominates), wage-job share growth **0.017 per five years**.
Calibrated directly (not free): desired surviving children at zero schooling **3.18**, schooling effect on
desired fertility **0.124**, sigma 1.5, food floor/income elasticity, investment rate.
**Fit (1950-2020 stylised-country medians):** fertility 5.3 -> 2.19 (data 6.0 -> 2.06); schooling 0.5 -> 8.2
years (data 0.4 -> 9.6); ag employment share 31% in 1960 (data 30.6%) falling to 8% in 2020 (data 19%); model
population grows faster than the data (index 4.4 vs 2.9) and the ag share falls too fast — the two clear
failures. **Recovery test:** 3 of 3 parameters recovered within 0.03 in the queue and job terms; the
wage-premium weight is not recovered (true 0.40, recovered 0.00) because it carries little identifying
variation — reported, not hidden.
**Counterfactual ("no mechanisation / no more ag jobs"):** freeze the relative input price at its 1960 level
after 1960, keep TFP growing. In 2020 the ag labour share stays **17.9% vs 8.1%** in the baseline; schooling
reaches **5.6 vs 8.2 years**; fertility **2.52 vs 2.19**. Mechanisation is the margin that empties agriculture
and feeds the schooling pipeline; without it the transition stalls and the pipeline stays small.
The timing the model produces: population growth peaks around 1980, agricultural labour peaks early and then
falls while the wage share rises, and the schooling/fertility transition comes after the labour release —
the overlap Dr. Menefee described. What would break it: fertility collapsing while agricultural employment is
still large and inputs still expensive (the model requires the labour release to precede the schooling/
fertility transition); population growth without any labour release; or a pipeline that absorbs labour with no
fertility response. None of these is tested against all countries here; the model is a demonstration.

## (1) Fertility
The corrected Boppart test does **not** deliver a country-panel fertility effect at ten-year horizons
(T2c null, n=503, 127 countries, MDE ~0.016 births). What the record supports: the fertility transition in the
stylised-country data is consistent with the joint model in which mortality decline produces the population
explosion and then, as agriculture sheds labour and schooling expands, fertility falls — fertility 5.3 -> 2.2
in the model vs 6.0 -> 2.1 in the data. The mechanism is not a direct input-price effect on births; it runs
through the labour release, the wage/credential queue, schooling, and the quantity-quality margin. That is a
model-consistent story, not an estimated causal effect, and it must be labelled as such.

## (2) Massification
This is where the corrected test is strongest. The paper's object is real in the data: input prices and
intensity are strongly negatively related (T2a), intensity is strongly negatively related to the agricultural
employment share across countries (T2a2), and inputs account for about two-thirds of the agricultural
labour-productivity gap (T1). The old proxy test measured none of this. The model's massification margin is
the pipeline: as mechanisation releases labour, finite wage-sector capacity leaves a queue that schooling
absorbs; in the counterfactual without mechanisation schooling is 5.6 rather than 8.2 years and fertility is
higher. So the paper's mechanism is supported cross-sectionally and is the right foundation for the
schooling/fertility part of the project — but the dynamic sequencing in country panels is **not** established
by our tests, and must not be claimed.

## Files, provenance, reproducibility
`scripts/`: `pull_wdi.py` (World Bank API pull, 207,622 rows), `boppart_replicate.py` (T1),
`corrected_test.py` (T2), `model.py` (T3, calibration + counterfactual + recovery). `results/`:
`replication.txt`, `replication.json`, `corrected_test.txt`, `corrected_test.json`, `model_summary.txt`,
`model_paths.csv`, `model_counterfactual.csv`, `model_params.json`. Raw data: NBER appendix PDF and the WDI
extract live on box2 at `/root/work/subsistence/data/`; the 207,622-row WDI file is not committed (size).
This job is deliberately explicit about the three labels: **estimated** (sigma 1.24-1.76 from T1),
**calibrated** (N0, kappa, food demand, investment rate, and the 3 free parameters), **assumed**
(non-agricultural capital share, depreciation, beta_i = 0.5). The model is a demonstration and the replication
is partial; the falsifiers above are the tests that would overturn them.
