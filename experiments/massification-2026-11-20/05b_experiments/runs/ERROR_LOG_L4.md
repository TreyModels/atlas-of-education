# ERROR LOG — Loop 4 (`05b_experiments/loop4/`)

## Run-level
- Final run: 4 cells (U1, U1b, U2, U3) executed; **0 failed runs**. U1/U1b/U2 are numpy-only; U3 uses the
  loop-2 module with the horizon constant patched to 60 years (t=0 <-> 1965) — a declared extension.

## Interpretation issues / caveats
1. **U1 calibration vs checks.** U1 calibrates exactly one demand intercept (all-levels participation
   78.5%); fee ratios and by-level participation are then checks. The fee pass is therefore a check
   against a target on which the intercept was NOT fit; the by-level ordering failure is a genuine
   structural failure (stakes rise with stage in the model; official participation falls with stage).
2. **U1 hours = UNABLE.** The module has no hours object; no hours number is claimed or fitted.
3. **U1b provider-mix rule reversed.** The declared rule (teacher-tutor capacity to highest-stakes stage
   first) implies commercial share is LOWER at S6-7 (model 22.3% vs S4-5 100%), the opposite of the
   observed 72.4% vs 33.0%. The rule was declared before running and is reported as a failed prediction,
   not silently re-specified. U1b verdict is FAIL under the predeclared four-condition rule (the shape
   alone would be "shape-only"; provider-ordering failure blocks even that).
4. **U1b fee 5.19% vs band 1.1-5.0%** — 0.19 pp over the upper bound; does not affect the FAIL verdict
   (levels already fail), but noted as near-marginal.
5. **U2 estimator used the plain 0.25 threshold** as predeclared; the optional 2-seed-sd significance
   variant was not applied (would be a separate specification). The negative recovery/forced-ID result is
   reported under the predeclared rule; the no-placebo forced-ID (1.00) is reported as a design warning.
6. **U3 KHM "PASS" is mechanical**: in-sample RMSE 14.8 pp, s0 multiplier at the grid edge (0.40), held-out
   MAE 1.84 pp because the modelled path is nearly flat and happens to match a flat observed stretch. It
   meets the predeclared threshold but is explicitly NOT treated as a validated country claim.
7. **New-anchor discipline:** Korea official 2023 only (Korea 2011 "90%" excluded, not traceable); Hong
   Kong Bray & Kwok 2003 six-school quota sample (medium-high, not territory-wide); Japan/UNABLE; China
   and Cambodia used only as bounds; PH blocked. HK 0.85 remains a calibration, never incidence evidence.
8. **U4 has no new compute**; it is a verdict over the loop-3 and loop-4 results, and it names every
   unrun/UNABLE item.
