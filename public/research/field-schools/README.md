# Farmer field schools & food politics — code and results

This public subset contains Python model code, tests, regenerated figures and tables, and documentation. Source PDFs, prompts, manuscripts, AI review notes, and supplied historical figures are excluded. The full private author bundle preserves those materials separately.

# Food-Price and Diffusion Models (repaired research package)

This repository contains two small, developing mechanism models written in
Python. It is a research package, not a validated empirical study. Nothing
here should be read as a calibrated estimate, a causal claim, or a
peer-reviewed result.

## Status

- **Developing mechanism models.** The code is illustrative and exploratory.
- **Implementation checks recorded.** 35 targeted checks pass; full diffusion
  grids and the seed-3 food-price outputs were regenerated. See `VALIDATION.md`.
  These checks do not establish empirical validity.
- **Two historical models are untouched and superseded.** `03_code/01_treadmill_economy`
  and `03_code/02_price_tag` are preserved as-is and are **not** validated.
- **The README you are reading replaces the optimistic handover** archived at
  `06_archive/README_original.md`.

## Models

### Model A — diffusion (`03_code/03_diffusion`)

A finite-horizon, adoption-mediated binary process on a lattice. A practice is
either held or not; a nonadopter becomes eligible to adopt only through
contact with an adopter, and adoption is the only channel by which the
practice spreads. There is **no separate "knowledge" state distinct from
"use"**. A quiet stochastic round is **not** absorption; the process runs to
the horizon or until no eligible nonadopter has an adopted neighbour.

Eligibility uses a risk-weighted expected margin:

    gross           = access * p * (1 - share) * dy
    perceived_cost  = c * (1 + ambiguity) if ambiguity > 0 else c
    expected_margin = risk * gross - perceived_cost

`risk` in [0, 1] is an **assumed probability that the gross yield benefit is
realised before deducting cost**. It is not an estimated risk-aversion
parameter and it is not a claim about Kenya. `risk = 1` is the default
baseline; it reproduces the original full-benefit eligibility rule exactly.

The `lease_share` used for leaseholders is an **illustrative proportional
output share**. It is **not** a calibrated statutory PD 27 rent.

### Model B — food price (`03_code/04_food_price`)

A political price objective with a fixed farm aptitude `apt` and an annually
re-optimised input intensity `k`. Farms may exit irreversibly (a farm that
exits never returns), giving path dependence in the cross-section of active
farms. This is **not** capital accumulation and **not** endogenous or
cumulative TFP.

- The objective is a reduced-form political support function. It is **not** a
  welfare planner.
- `political_counterfactual` (gamma=1, budget_share=0) is the political
  objective under a **zero subsidy allowance**, not an unconstrained optimum
  and not a welfare planner. `planner()` is a deprecated alias for it.
- The reported `breakeven` is an **operating** break-even,
  `sum(c*k*land) / sum(y*land)`, among pre-exit producers at the fixed chosen
  input. It **excludes** the opportunity wage. Exit is a separate
  opportunity-cost decision; `farmers_end` is recorded separately from
  `farmers_producing`.
- `PW` is an **undocumented supplied price index**. Its provenance is not
  recorded and it is not verified against any source. Do not treat it as
  observed data.
- The objective's scaling with `n` is an unresolved assumption (see
  `OBJECTIVE_SCALING_NOTE`).

## Layout

- `03_code/` — two current models and two historical branches.
- `tests/` — diffusion tests; food-price tests are in `03_code/04_food_price/tests`.
- `06_archive/original_code/` — original source for comparison, not current runners.
- `07_results/diffusion-full/` — regenerated full grids, figures and tables.
- `07_results/diffusion/` — reduced diagnostic grids.
- `07_results/food-price/` — annual outputs, regression coefficients and provenance.
- `07_results/checks/` — local test logs.
- `PUBLIC_MANIFEST.json` — SHA256 hashes for this subset.

Historical scripts and archived originals have not been made portable or validated. Run the current root entry points.

## Requirements and running

Python 3.11.

    pip install -r requirements.txt

From the repository root:

    python run_models.py diffusion --quick
    python run_models.py food-price --quick
    python run_models.py all --quick

Individual entry points:

    python run_diffusion.py
    python run_foodprice.py

Tests live with each model:

- `tests`
- `03_code/04_food_price/tests`

## Claims and caveats

- **Biggest correction:** the illustrative 25% proportional output share is
  **not** a calibrated statutory PD 27 rent.
- RA 3844 section 34 uses **net average normal harvest after deductions**, not
  a proportional marginal gross current output. PD 27 concerns ownership and
  amortization. Legal references:
  - https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/23334
  - https://www.lawphil.net/statutes/presdecs/pd1972/pd_27_1972.html
- **No rent-law mechanism is implemented** in this code.
- Do not claim that Kenya's nonadoption proves water or risk is the cause.
- The percolation threshold is a **conditional parameter artifact**; there is
  no universal threshold and no discovery.
- Existing generated expert documents are **AI review notes**, not peer
  review. DOI resolution is not content verification. The literature review
  is unverified beyond limited spotchecks; do not endorse the 130 items.
- Descriptive OLS on endogenous model prices is **not** empirical causal
  validation. The manuscript needs data provenance, an empirical test, and
  model sensitivity analysis.
- No license is asserted for the private originals.

