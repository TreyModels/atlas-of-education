# Statistical screen of the full-system multiverse (EXPLORATORY, SIMULATION)

Source: `results_multiverse.json` — 1,440 eduengine runs (144 design cells × 10 seeds, N=400,
T=70, measure from year 35). Toy worlds, illustrative parameters; **no causal or empirical claims**.
Script: `test_full_system.py`. Output: `full_system_tests.json`.

> **Correction notice (25 Nov 2026).** The first version of this record claimed "all Holm p<0.05 and
> sign-consistent across strata" for 49 rows. The line audit found four of those rows were promoted by
> **vacuous stratum checks** (`all([])` is `True`) or by a **rank-deficient design** silently solved with
> `pinv`. This version adds estimability + non-empty-stratum + zero-variance guards, publishes the
> **complete** supported set, and labels the whole exercise **exploratory** (the p-values were never
> pre-registered — see `TEST_PREREGISTRATION_DEVIATION.md`). Supported rows: **45**, not 49; four rows
> moved to a reported `not_estimable` list.

## Method (and what changed)

For each design-axis contrast and outcome: OLS with all main effects + seed fixed effects,
**cluster-robust SEs by design cell** (144 clusters), 95% CI, **Holm correction across the estimable
outcomes within each contrast block**, and a **stratum sign check** (does the sign hold in every level
of every other axis?). An effect is called supported only if **all** of:

1. **estimable** — `e_j` lies in the row space of the outcome-specific design (SVD rank test,
   `RANK_REL_TOL = 1e-8`); otherwise it is reported as `not_estimable`, never as a number;
2. **variable** — the outcome has non-zero variance in the estimation sample;
3. **Holm p < 0.05** within its block;
4. **sign-consistent across a non-empty set of strata** (`bool(strat) and all(...)`).

Guards 1–3 did not exist in the first version: `np.linalg.pinv` returned coefficients/SEs for
directions the data cannot identify, which produced e.g. supply → `formal_share_gdp` "effect 0.135,
SE 0.003, p_holm 0" and a zero-variance `tut_rate` "supported, p=0" row. Both are now `not_estimable`.

**Disclosure — the stratum check is a heuristic, and a stricter one bites.** The stratum step compares
raw cell means with no seed FE and no clustering. A stricter per-cell check (each design cell vs the
same cell with the axis at its reference level, averaged over seeds) finds at least one sign flip in
**17 of the 45** supported rows, but flips whose magnitude is ≥10 % of the pooled effect in only
**6 of 45**; across all 2,200 cell contrasts, 105 flip (4.8 %) and 35 (1.6 %) are large. The full
per-row counts are in the table and in the JSON (`cell_sign_flips`, `cell_sign_flips_10pct`).

## Supported effects — complete list (45 rows, Holm p<0.05, non-empty sign-consistent strata)

**afford: ['credit_constant', 'credit_poverty'] vs cash_only**

| value | outcome | effect [95% CI] | Holm p | strata | cell flips (≥10% of effect) |
|---|---|---|---|---|---|
| credit_constant | completion_primary | +0.1324 [+0.1258, +0.1391] | <1e-16 | n=11 (+0.116..+0.149) | 0/48 (0) |
| credit_constant | completion_lower | +0.0352 [+0.0195, +0.0510] | 4.7e-05 | n=11 (+0.000..+0.070) | 7/48 (0) |
| credit_constant | completion_upper | +0.0380 [+0.0222, +0.0538] | 1.1e-05 | n=11 (+0.001..+0.075) | 2/48 (0) |
| credit_constant | completion_tertiary | +0.0663 [+0.0559, +0.0767] | <1e-16 | n=11 (+0.040..+0.093) | 0/48 (0) |
| credit_constant | formal_share_gdp | +0.0166 [+0.0064, +0.0267] | 0.0041 | n=10 (+0.003..+0.030) | 0/24 (0) |
| credit_constant | parity_wealth_lower | +0.1271 [+0.1132, +0.1409] | <1e-16 | n=11 (+0.074..+0.180) | 0/48 (0) |
| credit_constant | skill_premium | -0.2205 [-0.2537, -0.1874] | <1e-16 | n=10 (-0.285..-0.156) | 0/24 (0) |
| credit_poverty | completion_primary | +0.1131 [+0.1058, +0.1203] | <1e-16 | n=11 (+0.088..+0.138) | 0/48 (0) |
| credit_poverty | completion_lower | +0.0256 [+0.0090, +0.0421] | 0.0074 | n=11 (+0.000..+0.051) | 11/48 (6) |
| credit_poverty | completion_upper | +0.0297 [+0.0140, +0.0454] | 0.00083 | n=11 (+0.001..+0.058) | 4/48 (0) |
| credit_poverty | completion_tertiary | +0.1324 [+0.1206, +0.1442] | <1e-16 | n=11 (+0.100..+0.164) | 0/48 (0) |
| credit_poverty | tut_rate | -0.0204 [-0.0363, -0.0044] | 0.025 | n=9 (-0.027..-0.014) | 2/16 (2) |
| credit_poverty | formal_share_gdp | +0.0381 [+0.0247, +0.0515] | 1.1e-07 | n=10 (+0.001..+0.075) | 5/24 (0) |
| credit_poverty | parity_wealth_lower | +0.0798 [+0.0657, +0.0940] | <1e-16 | n=11 (+0.034..+0.125) | 8/48 (3) |
| credit_poverty | skill_premium | -0.3851 [-0.4179, -0.3524] | <1e-16 | n=10 (-0.443..-0.327) | 0/24 (0) |

**supply: ['fiscal_loop'] vs fixed_budget**

| value | outcome | effect [95% CI] | Holm p | strata | cell flips (≥10% of effect) |
|---|---|---|---|---|---|
| fiscal_loop | q_pub | +0.1319 [+0.1145, +0.1493] | <1e-16 | n=12 (+0.029..+0.234) | 0/72 (0) |

**learning: ['plus_private', 'plus_private_tutoring'] vs public_only**

| value | outcome | effect [95% CI] | Holm p | strata | cell flips (≥10% of effect) |
|---|---|---|---|---|---|
| plus_private | completion_primary | +0.0163 [+0.0093, +0.0233] | 3.8e-05 | n=11 (+0.013..+0.020) | 0/48 (0) |
| plus_private | formal_share_gdp | +0.0193 [+0.0077, +0.0309] | 0.0066 | n=10 (+0.002..+0.037) | 3/24 (1) |
| plus_private | skill_premium | -0.0486 [-0.0800, -0.0171] | 0.012 | n=10 (-0.072..-0.026) | 0/24 (0) |
| plus_private | q_pub | +0.0383 [+0.0163, +0.0604] | 0.0046 | n=11 (+0.032..+0.045) | 0/48 (0) |
| plus_private_tutoring | completion_primary | +0.0346 [+0.0276, +0.0416] | <1e-16 | n=11 (+0.025..+0.045) | 0/48 (0) |
| plus_private_tutoring | completion_tertiary | +0.0327 [+0.0208, +0.0445] | 3.1e-07 | n=11 (+0.007..+0.058) | 2/48 (0) |
| plus_private_tutoring | formal_share_gdp | +0.0473 [+0.0356, +0.0591] | 2.1e-14 | n=10 (+0.036..+0.059) | 0/24 (0) |
| plus_private_tutoring | skill_premium | -0.0891 [-0.1210, -0.0572] | 2.6e-07 | n=10 (-0.136..-0.042) | 0/24 (0) |
| plus_private_tutoring | q_pub | +0.0396 [+0.0175, +0.0617] | 0.0013 | n=11 (+0.027..+0.053) | 0/48 (0) |

**gates: ['quota'] vs bar**

| value | outcome | effect [95% CI] | Holm p | strata | cell flips (≥10% of effect) |
|---|---|---|---|---|---|
| quota | completion_lower | -0.1703 [-0.1839, -0.1567] | <1e-16 | n=12 (-0.220..-0.120) | 0/72 (0) |
| quota | completion_upper | -0.1595 [-0.1724, -0.1466] | <1e-16 | n=12 (-0.203..-0.116) | 0/72 (0) |
| quota | completion_tertiary | -0.0990 [-0.1082, -0.0898] | <1e-16 | n=12 (-0.128..-0.060) | 0/72 (0) |
| quota | tut_rate | +0.2261 [+0.2134, +0.2388] | <1e-16 | n=10 (+0.202..+0.250) | 0/24 (0) |
| quota | parity_wealth_lower | -0.0144 [-0.0251, -0.0037] | 0.022 | n=12 (-0.025..-0.004) | 14/72 (14) |
| quota | skill_premium | +0.3240 [+0.2988, +0.3491] | <1e-16 | n=11 (+0.251..+0.379) | 0/36 (0) |
| quota | q_pub | +0.0238 [+0.0064, +0.0412] | 0.022 | n=12 (+0.011..+0.037) | 0/72 (0) |

**jobs: ['competitive'] vs queue_floors**

| value | outcome | effect [95% CI] | Holm p | strata | cell flips (≥10% of effect) |
|---|---|---|---|---|---|
| competitive | completion_primary | +0.0539 [+0.0485, +0.0594] | <1e-16 | n=12 (+0.026..+0.076) | 1/72 (0) |
| competitive | completion_lower | +0.0386 [+0.0250, +0.0521] | 9.9e-08 | n=12 (+0.000..+0.077) | 14/72 (0) |
| competitive | formal_share_gdp | +0.3340 [+0.3243, +0.3438] | <1e-16 | n=11 (+0.301..+0.374) | 0/36 (0) |
| competitive | parity_wealth_lower | +0.0639 [+0.0532, +0.0746] | <1e-16 | n=12 (+0.015..+0.106) | 2/72 (0) |
| competitive | q_pub | +0.1045 [+0.0871, +0.1220] | <1e-16 | n=12 (+0.002..+0.207) | 19/72 (9) |

**rural: ['high_penalty'] vs low_penalty**

| value | outcome | effect [95% CI] | Holm p | strata | cell flips (≥10% of effect) |
|---|---|---|---|---|---|
| high_penalty | completion_primary | -0.0323 [-0.0377, -0.0268] | <1e-16 | n=12 (-0.050..-0.019) | 0/72 (0) |
| high_penalty | completion_lower | -0.0501 [-0.0636, -0.0365] | 1.8e-12 | n=12 (-0.100..-0.000) | 4/72 (0) |
| high_penalty | completion_upper | -0.0442 [-0.0571, -0.0313] | 6e-11 | n=12 (-0.087..-0.001) | 6/72 (0) |
| high_penalty | completion_tertiary | -0.0529 [-0.0621, -0.0437] | <1e-16 | n=12 (-0.082..-0.024) | 0/72 (0) |
| high_penalty | tut_rate | -0.0684 [-0.0811, -0.0557] | <1e-16 | n=10 (-0.092..-0.044) | 0/24 (0) |
| high_penalty | formal_share_gdp | -0.0212 [-0.0310, -0.0114] | 4.2e-05 | n=11 (-0.033..-0.009) | 1/36 (0) |
| high_penalty | parity_wealth_lower | -0.1458 [-0.1565, -0.1351] | <1e-16 | n=12 (-0.190..-0.083) | 0/72 (0) |
| high_penalty | skill_premium | +0.1597 [+0.1345, +0.1848] | <1e-16 | n=11 (+0.103..+0.220) | 0/36 (0) |


## Not estimable (reported, never "supported")

| contrast | value | outcome | reason |
|---|---|---|---|
| supply: fiscal_loop vs fixed_budget | fiscal_loop | formal_share_gdp | design rank 17 < 18 — outcome exists only in the fiscal arms |
| learning: plus_private / plus_private_tutoring vs public_only | plus_private | tut_rate | design rank 16 < 18 — tutoring switched off by construction |
| learning: plus_private / plus_private_tutoring vs public_only | plus_private_tutoring | tut_rate | likewise (zero-variance row in the first version) |
| jobs: competitive vs queue_floors | competitive | skill_premium | design rank 17 < 18 — premium exists only in competitive arms |

All four were "supported" in the first version; every one is a design artefact, not evidence.

## What this means (unchanged qualitatively, now without the four artefacts)

In this toy full system, the structural axes — **credit access, gate design, jobs/credential regime,
rural penalty** — dominate attainment and distribution. Tutoring is a real but second-order channel
(+3.5 pp primary completion, −0.09 skill premium) and reacts strongly to gates (+22.6 pp under quota).
The "shadow education" story is a small corner of a system whose main levers are affordability, gate
design, jobs and rural disadvantage.

Caveats that bound the claims: these are **exploratory** significance statements about a **simulated
design**, not the world; the Holm family is per contrast block, not joint; p-values are not
pre-registered; and 17/45 supported rows contain at least one cell-level sign flip.

## Limits

Toy eduengine, illustrative parameters; no migration, rural–urban sorting, remittances, country
calibration; p-values describe regularities of the simulated design, not the world. No causal claims.
Not pre-registered (see `TEST_PREREGISTRATION_DEVIATION.md`).

## Provenance / reproduction

`full_system_tests.json` now carries `provenance`: script sha256, source (`results_multiverse.json`)
sha256, numpy/python versions, git commit, full-design rank (18 < 18 columns → full rank with all rows;
the rank losses above are outcome-specific). Regenerate with `python3 test_full_system.py` from this
directory (numpy only). Reproduction hash of the source used here: `004173aa…` (matches the run record).

---

## Reconciliation addendum — 25 Nov 2026 (counts for citation)

- **Supported: 45 of 72 tested contrast-outcome rows (45/72).** The denominator is the 72 rows in
  `full_system_tests.json` (`contrasts`): 6 contrast blocks x their outcome rows = 72 estimable-and-variable
  candidates; 4 are reported in `not_estimable`, and the remaining 23 are not supported.
- **Strict 5-axis sign-consistent count: 28 of 72 (28/72).** This is the task-47 audit's stricter requirement that
  the sign hold across every level of all five *other* design axes, not merely the non-empty-stratum heuristic used
  by the `supported` flag. Quoted from the task-47 audit; it is not machine-readable in `full_system_tests.json`
  and was not recomputed in this addendum.
- The first version's **49/72** is superseded and must not be quoted (four empty-stratum rows and one zero-variance
  row were false positives; see the correction notice above). Cite **45/72 supported, 28/72 strict**, with the
  exploratory label.
