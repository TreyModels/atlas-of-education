# Angkor charter-fiscal model — experiment series, 22 Nov 2026

A computational exploration of why a low-density agrarian polity (Angkor, 9th–15th c.)
would rise, peak and relocate. This is a **screening exercise**, not a validated model of
Angkor. Every number here describes the behaviour of a simulator under stated assumptions.

## What is in this directory

```
scripts/
  v6_engine.js        fiscal model with switchable mechanisms (charter, ratchet, climate, raid, transport)
  v7_engine.js        space-explicit version: concentric rings, haul decay, garrison cost, endogenous reach
  v8_engine.js        v7 + maintenance-funded productivity + alternative endowment/tax targets
  v6_worker.js        sharded experiment worker (factorial / Morris / grid)
  v7_worker.js        same, for the ring model
  v8_experiments.js   the ten designed experiments (E1–E10)
  v*_driver.js        core fan-out
  v*_analyze.js       reducers
  v8_report.js        ten-experiment aggregation
  v5_ratchet.js       minimal single-mechanism test (endowment ratchet alone)
  charter*.js         earlier iterations, kept because their failures are informative
research/
  litreview.md        8,267-word literature review (charter states, low-density urbanism, rice yields)
results/
  analysis_v7.json    factorial + Morris + grid for the ring model
  analysis_v8.json    the ten experiments
```

## The model in one paragraph

Four stocks — population, cultivated land, endowment share (land permanently alienated to
temple estates), and charter (portable legitimacy) — plus a water network whose upkeep must be
funded. Revenue is a tax on the *non-alienated* share of production, discounted by haul cost
from each ring to the capital, net of a garrison cost that rises with distance. Obligations are
elite stipends, network upkeep and defence. When revenue covers obligations, legitimacy grows;
when it does not, legitimacy erodes; when legitimacy falls below a threshold the capital moves,
taking a smaller catchment and a fresh endowment base. **The fall is therefore a relocation, not
a collapse** — which is the behaviour Lieberman's charter-state argument predicts.

## What the experiments found

**Charter is necessary.** In every cell of a 2^5 factorial without it, the rise-peak-relocation
pattern never occurs (P = 0). Main effect +0.62. It is the memory term: without a relocatable
legitimacy stock, a fiscal crisis is terminal.

**Two sufficient mechanisms, but one axis.** The endowment ratchet alone produces peak ~913,
lag ~150, decline 0.71. Elite overproduction alone (with transport discount off) produces peak
~1297, lag ~200, decline 0.65. A 6×5 surface shows they are **not rivals**: raising elite growth
pulls the peak earlier at every ratchet level. There is one axis from "slow squeeze" (peak 1600,
no fall) to "fast squeeze" (peak 838).

**Raiding is harmful, not neutral.** Main effect −0.254. Capture adds population without adding
taxable land, which destroys the shape.

**Yield is nearly irrelevant to the dynamics.** Morris score 0.013 against `endowRate` at 7.0.
The yield band changes the absolute population, not the timing of the peak or the relocation.

**The model's peak comes too early.** Placing the peak at the historical ~1150 requires an
endowment rate of ~0.00025/yr — roughly 9% of land alienated over 350 years, well below what the
inscription corpus implies. This is the strongest falsification in the series and the main open
question: crown revenue was more resilient than a simple land-endowment ratchet allows.

**Charter erosion rate sets the lag, not the peak.** Varying it from 0.001 to 0.02 moves the
relocation lag from 154 years to 17 while the peak stays at 913. That is a clean separation of
*why it peaked* from *how long it held on*.

## Known defects (do not build on these without fixing them)

1. **Cultivation tracks demand instantaneously**, so a harvest shock cancels out before it can
   matter. Climate experiments therefore return a null by construction, not by finding. This
   invalidates any climate conclusion drawn from this engine, including the "drought is
   irrelevant" claim in the v7 Morris run.
2. **E1 and E2 are degenerate**: the alternative endowment targets and tax bases do not separate.
3. **No space in v6**, and the v7 ring areas are stipulated rather than measured.
4. **No monument stock, no households, no trade.** The model cannot speak to the things the
   archaeological record mostly consists of.

## Reproduction

Node 12 compatible, no dependencies.

```bash
node scripts/v8_experiments.js 0 2136 results/v8_all.csv
node scripts/v8_report.js
```

The experiment suite runs in seconds on 90 cores; each individual run is a few hundred
microseconds.

## Status

Exploratory. Not peer reviewed, not calibrated, not a claim about the past. The literature
review at `research/litreview.md` carries a "sources I could not verify" section that should be
read before any citation from it is used.
