# Pre-registration — Boppart et al. intensive agriculture: correct test + subsistence model

Committed **before** any data download, script or estimate. Date: 23 Nov 2026. Task `task-22`.
Branch `research/subsistence-2026-11-23`; record `research/records/2026-11-23-subsistence/`; box2 `/root/work/subsistence`.

## What the old project test actually was (statement of the error, written before re-analysis)
The earlier "Boppart test" used a **world commodity price index multiplied by the farm employment share** as the
regressor for farm exit and births. That measures short-run exposure of farm employment to world prices. It is
**not** the paper's object: Boppart et al. study a cross-country nested CES agricultural production function in
which *relative input prices* (investment/intermediate goods vs labour) differ across countries and generate
input intensification. The old test could not estimate substitution elasticities, could not do the development
decomposition, and its price instrument is common across countries (so it identifies a world shock, not the
cross-country relative-price mechanism). Pre-registered expectation: the old proxy test is not a test of the
paper; the corrected test below should behave differently.

## Data plan, in order
1. The paper's online appendix at `nber.org/data-appendix/w31101` (redirects to `data.nber.org`). Fetch with a
   browser user-agent. If it contains data, replicate their estimation directly. If it contains only the
   appendix PDF (as NBER working papers usually do), record that and rebuild.
2. Rebuild the minimum series from World Bank WDI API (reachable from box2) and the Penn World Table: ag
   employment share, ag value added, arable land, fertiliser and tractor intensity, gross capital formation,
   population/labour force, investment price level, labour share, real GDP per worker. World Bank commodity
   prices for the intermediate-price deflator. FAO/GAEZ/BACI/LSMS quantities are not obtainable here; every
   departure from the paper's data is to be documented, not hidden.
3. Use local `/root/work/local_data/` (checked before any web pull) where it helps for the schooling side.

## T1 — replication of the paper's cross-sectional CES estimation (pre-registered)
- Estimate substitution elasticities from the 2005 (and, if possible, 2015) cross-section: regress
  log(input/labour quantity ratio) on log(relative input price); report the slope as the elasticity estimate
  (paper's own procedure matches ratios at the development extremes; both are reported).
- Pre-registered expectation from the paper: elasticity between labour and capital **above one** (paper:
  σ1 = 1.90), between the labour-capital nest and intermediates **above one** (paper: σ3 = 1.75); land
  complementarity is what their preferred nesting estimates (σ2 = 0.66) — this is the paper's own number and
  will be compared to ours rather than re-stated from the brief.
- Input-intensification decomposition of the agricultural labour-productivity gap between the poorest and
  richest countries (their claim: "a bit less than two thirds" from inputs).
- **Falsifiers:** estimated elasticities below one, or input intensification explaining less than 40% of the
  gap, would contradict a successful replication (data deviations will be listed if this happens).

## T2 — the correct reduced-form test (pre-registered)
Construct the paper's object directly: agricultural input intensity relative to labour (capital and
intermediates per agricultural worker, and the tractor/fertiliser intensity of land), and the **relative price
of inputs to labour** (investment-good price ÷ wage; intermediate-price index ÷ wage).
- T2a: intensity rises where inputs are cheap relative to labour (negative price elasticity, cross-section and
  within-country).
- T2b: lagged intensity and lagged relative input price predict the subsequent ten-year decline in the
  agricultural employment share, with country and decade fixed effects, clustered by country — i.e. the input
  margin *precedes* labour release.
- T2c: the released-labour margin predicts subsequent schooling expansion and fertility decline (secondary
  completion up, births down) after controlling income and urbanisation, in a separate, pre-specified step.
- **Falsifiers:** wrong sign on T2a; no lead of intensity/price over labour share (T2b); or schooling/fertility
  effects vanish once income and urbanisation are controlled (T2c). Any of these is reported as a failed
  prediction, not re-spun.

## T3 — smallest defensible subsistence-transition model (pre-registered)
Two sectors: agriculture (CES in labour, capital, intermediates, and quality-adjusted land) and
non-agriculture (Cobb-Douglas); non-homothetic (Stone-Geary/subsistence-floor) demand for food; labour is
mobile across sectors and wages equalise. The model is driven by falling non-agricultural input prices /
rising non-agricultural TFP; agricultural labour is released and non-agricultural wage employment expands.
Then a demographic block: released labour raises the return to schooling and lowers fertility through a
quantity-quality margin.
- Parameter discipline: **at most 5 free parameters**, everything else calibrated to the cross-section or
  assumed; if more are needed, run a synthetic recovery test (simulate from known parameters, re-estimate,
  report whether they recover) before using the model for any claim.
- **Falsifiers:** if a mechanisation-driven simulation cannot generate the observed labour-share decline and
  intensification share; if the implied schooling/fertility response has the wrong sign or is quantitatively
  negligible; or if the model needs implausible parameters, the model fails and the record will say so.

## Reporting commitment
Plain words, mandatory headings "(1) Fertility" and "(2) Massification", every number with sample and
uncertainty, all calibrated vs estimated vs assumed parameters labelled, and the answer to "did we test this
paper right?" stated plainly (pre-registered expectation: no, and here is the correction).
