# L1→M6 extension — held-out and within/between checks (v0.1, 2026-11-25)

**Owner:** `deepseek-dhs`. **Status:** exploratory; host-only; no box; no restricted microdata involved
(inputs are the executed L1 estimate table + public DHS-API panels). **Code:**
`integration/within_between.py`; **outputs:** `within_between_results.csv` (88 series),
`heldout_results.csv` (572 tests), `extension_manifest.json`.

## Question

The milestone-2 prototype attached public DHS-API country-year context indicators to executed survey-wave
domain means (same-year and 5-year lag). This extension asks two deliberately modest questions:

1. **Within vs between:** for each (experiment × indicator × education stratum) series, does the context
   association operate **between countries** or **within countries over waves**?
2. **Held-out value:** does a context model predict **unseen countries** (leave-one-country-out) or an
   **unseen last wave** better than a simple training-mean baseline?

## Method (fully documented, no causal apparatus)

* Observations: L1 cell = weighted domain mean (estimate, design-based SE) matched to the same-year public
  DHS-API indicator value; one row per (experiment, country, wave, group).
* Weights: inverse-variance `1/SE²` (L1 SEs are design-based; weights are descriptive).
* **Pooled** model `y = a + b·x`; **within/between** model
  `y = a + b_within·(x − country_mean_x) + b_between·country_mean_x` (weighted least squares, naive WLS SEs).
* **Held-out checks:** leave-one-country-out and last-wave holdout; baseline = training weighted mean;
  metric = RMSE on held-out cells. All 88 series, 572 tests.
* Effective N for cross-country statements = **4 countries**; cells are not independent; no inference beyond
  description is claimed.

## Results (honest, mixed)

* **88 series** analysed (E1–E8 × six indicators × two education strata, where matched).
* **Between/within divergence is common and material.** Example: E1 vs `FE_FRTY_W_MNC` (edu stratum 3):
  pooled b = +0.391, **within b = −0.412, between b = +1.479** — the cross-country association is positive
  while the within-country-over-waves association is negative, the classic signature that a country-level
  covariate cannot be read as a household- or wave-level relationship (ecological-fallacy warning, not a finding
  about schooling).
* **Held-out prediction does not support the context model.**
  * Leave-one-country-out: median RMSE model **0.180** vs baseline **0.169**; model better in only **43.3 %** of
    tests.
  * Last-wave holdout: median RMSE model **0.179** vs baseline **0.199**; model better in **53.7 %** of tests —
    essentially a coin flip.
* Conclusion for the programme: **public country-year context adds little reliable out-of-sample predictive
  value for these survey means**, and where it "works" it is between-country variation with only four countries.
  This is a genuine negative result; it should not be presented as evidence about mechanisms.

## Guardrails encoded

`context_not_exposure = True`, `causal_claim = False`, `exploratory = True` on every row; no interpolation;
no pooling of repeated cross-sections into a panel; country-level covariates are never treated as household
measurements; effective N = 4 countries; no causal or policy interpretation.

## Files and reproduction

```bash
~/neon-boot/venv/bin/python experiments/dhs_v1/integration/within_between.py
# inputs pinned by sha256 in extension_manifest.json (prototype_l1_m6_final.csv, itself built from
# runs/2026-11-25_final/estimates_final.csv — the executed, QA-signed engine output)
```

These results are separate from, and do not modify, the milestone-2 estimates or the eight descriptive
experiments. No restricted data left the Mac; box unused.
