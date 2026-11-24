# Review of Gemini's "Next-Tests Runbook" (Claude, 24 Nov 2026)

`Next_Tests_Runbook.md` is Gemini's file, stored unchanged. This note says what in it is usable, what is wrong, and where each test was
run or replaced. Nothing in the runbook was executed as written.

## Test 1 - orthogonalised t+10 placebo (fertility audit)
- Usable: specifications 1-3 are sensible. Replaced/extended by `scripts/q2_adult_stock_placebo.py`.
- Problems: (a) the paths and column names (`/root/work/data/panel_observed.parquet`, `yr_sch_fem`, `lsec_comp`, ...) are not in the repo and were not
  checked; (b) `shift(-10)` shifts rows, so it is only correct if the panel is annual; on 5-year grids it jumps 50 years (I hit this exact bug
  in my own first draft); (c) overlapping 10-year changes at every year are serially correlated; cluster by country is the minimum;
  (d) enrolment and completion rates at t+10 describe children born within a decade of t, so parents' fertility and expectations can affect them
  (see PAPER_PLAN Paper 2); the design needs an adult attainment stock (done in Q2); (e) "without country trends" is labelled but the code uses country fixed effects, not trends.

## Test 2 - pre-1960 complete transitions (shape paper)
- Problems: (a) the script prints BIC winners only; the stated training/hold-out split and the `linear_kink` model are not implemented; (b) `exp_floor`
  is called "3-param" but has 4; (c) BIC penalty k=4 for all, no double-logistic (the UN projection model, the real rival); (d) the 1800-2023 window includes
  the baby boom and the post-1970 sub-replacement period, which no monotone form can fit; the window must end at the first sustained rebound; (e) pre-1950 OWID/Gapminder TFR is a
  modelled reconstruction (Sweden 1891 looks low against HFD-type estimates - verify), so ranking on it is weak evidence.
- Replaced by `scripts/q3_form_race.py`, run on the 9-10 countries with pre-1900 data in the repo's long-run panel; the OWID download for the US, Japan, Germany, UK, Canada, Australia was not possible here (pass it as the optional second argument).

## Test 3 - 1,200-draw multiverse + known-truth simulation
- Arithmetic is right in substance: per-rank BY threshold is j x 0.05/(272 x 6.185) = j x 2.97e-5; the floor 1/1201 = 8.33e-4 clears rank j >= 29.
  But "alpha_BY = 0.05/6.185 = 0.00808" is the family-level BY level, not the per-rank threshold.
- "Reuse r = 1..400 from final400.pkl and compute 401..1200" is not supported by `run_multiverse400.py` (no start option; it recomputes r = 0..R). Run R=1200 from scratch and compare the first 400 to final400.pkl (that is the determinism check).
- `/root/work/data`, `/root/work/groups/out/final400.pkl` and `ssh autodl2` were not verified. If they exist, E0 (panel availability) is resolved.
- The three synthetic DGPs omit the cases that matter most: shared country trends (the electricity case) and an effect planted in a minority of countries labelled robust. Use regimes A-S in `q4_methods_params.json` and add Gemini's three as extras.

## Test 4 - DHS STATcompiler API
- Plausible and useful; not run (no network here). Verify the indicator IDs against `https://api.dhsprogram.com/rest/dhs/indicators` before use (the mean-children-ever-born ID, `FE_CEBA_W_CHB`, was not checked).
  The category names ("Education", "Wealth quintile", "Residence") and pagination also need checking. The script saves raw rows only; no gradient or attenuation analysis is written yet.

## Test 5 - censoring-aware threshold sweep
- Good design. Implemented and run: `scripts/q1_threshold_sweep.py`. It reproduces the paper's default exactly (64 of 64 countries with identical dates, 31/3/30, median lead 18, n=18) and then sweeps the grid.
- Result: the "91%" is sensitive to the schooling-take-off threshold (see README).
- The fee-abolition primary-source audit was not possible here.
