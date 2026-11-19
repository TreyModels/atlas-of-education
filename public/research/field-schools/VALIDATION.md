# Validation record — 19 November 2026

Implementation checks pass. Both current models remain developing mechanism explorations; this is not empirical validation.

- Diffusion: 17 targeted unittest checks pass, including a quiet round followed by transmission in both methods, positive reliability changes, replay, eligibility refresh, and graph checks.
- Food price: 18 targeted unittest checks pass, including operating break-even, producing/end-period cohorts, input validation, fiscal feasibility, and replay.
- Original/repaired seed-3 food-price paths match exactly for farmgate and consumer prices, output, demand, imports, deficit, and farmer counts (`07_results/food-price/baseline_regression_check.json`).
- All 38 original-file hashes match the source manifest at their preserved locations.
- Full diffusion grids regenerated in 33.4 seconds (`07_results/diffusion-full`); reduced diagnostic grids are separate (`07_results/diffusion`).
- Food-price annual tables, coefficients and figure regenerated (`07_results/food-price`). The plotted common-intercept regression matches the CSV: rising 0.38548, falling 0.57018. These are descriptive simulated-path slopes, not empirical estimates.
- Five regenerated figures visually inspected. Original figures remain unchanged in `04_figures`.
- Environment: Python 3.11.17, NumPy 2.4.6, Matplotlib 3.11.2. Exact source hashes and run settings are in output metadata.

Commands from the package root:

```sh
python -m unittest discover -s tests -p test_diffusion.py -v
python -m unittest discover -s 03_code/04_food_price/tests -v
python run_diffusion.py --quick
python run_diffusion.py --output-dir 07_results/diffusion-full
python run_foodprice.py --seed 3
```

## What is preserved

- `04_figures/` — eight supplied figures, preserved as supplied.
- `06_archive/original_code/` — original code, preserved.
- `SOURCE_MANIFEST.json` — original file hashes.

## What is not validated

- `01_treadmill_economy` and `02_price_tag` are historical, untouched, and
  superseded. They are not validated.
- The `PW` price index in Model B is undocumented and not verified against any
  source.
- The literature review is unverified beyond limited spotchecks. Existing
  generated expert documents are AI review notes, not peer review. DOI
  resolution is not content verification.
- Descriptive OLS on endogenous model prices is not empirical causal
  validation.

## How to run checks locally

Python 3.11:

    pip install -r requirements.txt
    python run_models.py all --quick

Tests live with each model:

- `tests`
- `03_code/04_food_price/tests`

