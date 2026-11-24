# SUITE REPORT — Master Equation Inventory experiment suite (task-40) — RE-RECORDED

**Branch:** `research/equation-suite-neon-fixes-2026-11-25` (local; base `a7fcfb9` = old head of
`research/equation-suite-2026-11-25`). **Run:** local Mac (`Treys-MacBook-Air.local`), Python 3.10.2,
NumPy 2.2.6, `nproc 8`.
**Command:** `OMP_NUM_THREADS=1 python scripts/run_all.py --workers 6` · **Wall: 73.18 s** ·
**Execution failures: []** · **Decision-rule failures: 3 (S4, S6, S10)** · **`run_all.py` exit: 1**.
**Window:** 2026-11-24T17:17:29Z → 2026-11-24T17:18:42Z. (Wall time varies with host load: the same suite
also took 224.33 s on an earlier re-record; both are full `--workers 6` runs on the same 8-core Mac.)

> **Why this report was re-recorded.** The previous version of this file (and every number in it) was produced
> at `a7fcfb9` before Neon's verified Part A patch and before the Part B fixes. It is superseded: see
> `NEON_PATCHES_2026-11-25.md` for the full before→after table, the audit-item mapping, and the deviation-log
> rationale. Old values remain in git history at `a7fcfb9`; nothing was overwritten silently.
>
> **Verdict semantics changed.** `run_all.py` no longer treats `returncode == 0` as a pass. A script passes only
> if its own JSON `decision_rule.PASS` is true. The old headline "Failures: [] / smoke PASS, full PASS / all ten
> scripts passed" counted execution only and buried three decision-rule failures.

**Labels:** every script is a standalone demonstration; S7 uses the committed observed/reconstructed panel
descriptively; S8 uses the committed x4 cross-section descriptively; S10 uses Bray literature targets as an
external check. **No causal claims; not MASSENG v5 outputs.** Every script is labelled `SIMULATION` or
`SYNTHETIC`/`OBSERVED` in its own JSON.

## Verdict accounting (corrected)

- **10/10 scripts executed.** Execution failures: none. No run was discarded.
- **3 decision-rule failures: S4, S6, S10.**
  - **S4 (pre-declared FAIL).** The old S5 rule — "quota flips the admission gap" — is applied exactly:
    bar gap **+0.5472**, quota gap **+0.0906** (not < 0), contest **+0.7614** → FAIL.
  - **S6 (post-hoc FAIL).** Migration is a new script from Amendment 02 with **no pre-registered decision
    rule**; the implemented "networks increase the effect" criterion is ad hoc. Network marginal effect
    **0.00892 < 0.01404** without network → FAIL.
  - **S10 (FAIL; also fails a dropped pre-registered rule).** The implemented rule fails on
    `ban_raises_gini_in_all_specs`. Separately, the old S3 tutoring-demand rule required the Tobit to be within
    0.15 of 0.8 in the single-process world; in the truth's units the Tobit is **1.441** — 0.64 away — and
    `tobit_within_0.15_share = 0.0` → that dropped pre-registered sub-rule still fails. The old 7.499-vs-0.8
    comparison was a level-vs-log scale artefact, not a bias estimate.
- **It is NOT "3 pre-declared FAILs".** Only S4's failure is on a clearly pre-registered rule. A reader must not
  take "pre-declared" at face value for S3/S6/S10.
- **Sub-test flags are surfaced.** `run_all.py` now prints each script's `rule_flags`, and S10's
  `decision_rule` carries the three dropped pre-registered S3 sub-rule booleans (outside `PASS`):
  `dropped_prereg_S3_different_two_part_within_0.15 = True`, `dropped_prereg_S3_different_tobit_outside_0.15 = True`,
  `dropped_prereg_S3_single_world_both_within_0.15 = False`. The last one is the dropped rule that **fails**.
- **S3 (eq03) currently PASSES**, but its `rho_recovered_within_0.10` criterion is itself post-hoc; the
  pre-registered "recovered ρ closer than Cobb–Douglas" rule also passes (median ρ̂ 0.6 vs truth 0.5 vs CD 1.0).
- **Smoke vs full.** Smoke (fast, fewer reps) differs from full for eq08 (`clean_lambda_near_truth=False` in
  smoke, `True` in full). Both statuses are recorded in `results/run_all.json`; the full run is the reported one.

## Per-script results (full pass; `status` = own decision rule)

| # | Script | System part | Execution | Decision rule | Failing / key sub-rule | Full wall (s) | Script sha256 | Output sha256 |
|---|---|---|---|---|---|---|---|---|
| S1 | `eq01_family_demand.py` | household demand/affordability | PASS | **PASS** | — | 2.79 | `acf642629c1d` | `d682987ff95a` |
| S2 | `eq02_supply_finance.py` | state/school supply + finance | PASS | **PASS** | — | 11.55 | `1709a7f8b4dc` | `39b1ce8e54a6` |
| S3 | `eq03_learning_quality.py` | learning/quality | PASS | **PASS** | (post-hoc ρ criterion now passes) | 36.46 | `f5492b4cf693` | `56418f7d46cf` |
| S4 | `eq04_transitions_gates.py` | gates + attainment/completion | PASS | **FAIL** | `quota_flips_gap_negative` (pre-declared) | 2.05 | `bd32ea9c5fe0` | `86ae086ba9da` |
| S5 | `eq05_returns_credentials.py` | jobs/credentials | PASS | **PASS** | — | 1.70 | `42fd596d1dee` | `1eb60a7a2381` |
| S6 | `eq06_migration_rural_urban.py` | rural-urban/migration | PASS | **FAIL** | `network_spec_effect_larger_than_no_network` (ad hoc) | 14.70 | `a7907b58987e` | `388962b364f4` |
| S7 | `eq07_inequality_dashboard.py` | inequality/dashboard | PASS | **PASS** | — | 10.28 | `df0b97195211` | `2da6b9d0e17f` |
| S8 | `eq08_growth.py` | structural change + macro | PASS | **PASS** | — | 0.47 | `b0fe636a2ad5` | `8416f732ef76` |
| S9 | `eq09_identification.py` | test bench | PASS | **PASS** | — | 13.21 | `deec9435d748` | `688741b82ac1` |
| S10 | `eq10_tutoring_shadow.py` | exams-shadow (single tutoring module) | PASS | **FAIL** | `ban_raises_gini_in_all_specs`; dropped S3 Tobit rule | 61.24 | `5103ff04b0c2` | `00e70d435933` |

Smoke statuses in the same run: S1–S3, S5, S7, S9 PASS; S4, S6, S8, S10 RULE_FAIL (eq08 smoke is the only
smoke/full disagreement).

## Plain-English results and multiverse ranges

### S1 eq01_family_demand — household demand/affordability
- **Data tier:** SYNTHETIC
- **Plain result:** Family income raises schooling demand in every budget specification (income elasticity range
  0.16–1.51), forgone earnings reduce it, and at zero schooling effect on births the raw schooling–births
  association is absorbed once income is controlled. This is a demonstration of budget arithmetic, not an
  estimate of any country's demand.
- **Decision rule:** PASS=True `{affordability_positive_across_specs: True, forgone_earnings_reduces_schooling: True, zero_signal_association_absorbed_by_income: True}`
- **Observed vs assumed:** observed: no usable public household demand micro panel (DHS IR gated; no fees/forgone
  panel) | assumed: all budget/credit parameters | gap: task-41 top gap 1

### S2 eq02_supply_finance — state/school supply + finance
- **Data tier:** SYNTHETIC
- **Plain result:** A universal per-student subsidy is pro-rich in this model (concentration index 0.406 vs
  −0.479 for means-testing) because enrolment rises with income; the investment arithmetic gives a positive NPV
  at 5% and an IRR of 25.0%. These are arithmetic consequences of the stated assumptions, not policy estimates.
- **Multiverse range:** [−0.4791, 0.4061]; spec_robust=False
- **Decision rule:** PASS=True `{universal_more_pro_rich_than_means_tested: True, npv_positive_at_5pct: True, irr_above_5pct: True}`
- **Observed vs assumed:** observed: UIS/EdStats PTR, private share, EMIS, WDI GDP available (not fitted) |
  assumed: coverage, unit costs, allocation rules | gap: no unified school-finance panel

### S3 eq03_learning_quality — learning/quality
- **Data tier:** SYNTHETIC
- **Plain result:** In the CES world the ability-controlled interaction is positive (0.002) and the CES fit beats
  Cobb-Douglas on RMSE (0.291 vs 0.558); in the linear null world the controlled interaction is near zero (0.004).
  This is a demonstration about estimators, not evidence about any school system.
- **Fits:** CES world median ρ̂ = 0.60 (truth 0.5; share within 0.10 = 1.00); linear world median ρ̂ = 1.00
  (truth 1.0; share within 0.10 = 0.69). CES objective is the normalised CES on the A-scale with a 2-D (ρ, ω)
  grid — see the deviations log.
- **Decision rule:** PASS=True (one criterion, `rho_recovered_within_0.10_in_half_reps`, is post-hoc)
- **Observed vs assumed:** observed: PISA/TIMSS/PIRLS/SACMEQ anchors available (not fitted) | assumed: production
  technology and parameters | gap: task-41 top gap 2

### S4 eq04_transitions_gates — gates + attainment/completion
- **Data tier:** SYNTHETIC
- **Plain result:** A score bar admits rich pupils at a higher rate (gap 0.547); a reserved quota narrows the gap
  (0.091) but does NOT flip its sign, so the pre-declared "quota flips the gap" rule FAILS; a contest in which
  richer pupils invest more effort widens it further (0.761). The quota changes who is admitted, not how much
  anyone learns — this is a rationing demonstration, not an evaluation of any admissions policy.
- **Multiverse range:** [−0.0912, 0.7614]; spec_robust=False. Quota-share gaps now computed (they were NaN):
  0.4 → +0.2593, 0.5 → +0.0906, 0.6 → −0.0912; the sign of the quota gap depends on the quota share.
- **Decision rule:** FAIL (pre-declared) `{baseline_gap_positive: True, quota_flips_gap_negative: False, contest_widens_gap: True}`
- **MASSENG boundary:** progression/capacity exist in MASSENG v5; the exam score bar and reserved-quota gates do
  NOT — standalone synthetic demonstration only (the old `mechanism_in_masseng_v5: true` was wrong).
- **Observed vs assumed:** observed: EdStats completion/transition proxies available (not fitted) | assumed: gate
  thresholds, quota rules | gap: task-41 top gap 3

### S5 eq05_returns_credentials — jobs/credentials
- **Data tier:** SYNTHETIC
- **Plain result:** Under the stipulated ability-bias DGP the naive regression overstates the return (mean bias
  0.033) while 2SLS is much closer (mean bias −0.000); with no ability bias both recover the 9% return. This is a
  demonstration of the estimator, not an estimate of any real return.
- **Multiverse range:** [0.0897, 0.1226]; spec_robust=True
- **Decision rule:** PASS=True `{bias_world_naive_biased: True, bias_world_iv_bias_smaller: True, null_world_naive_close: True, null_world_iv_close: True}`
- **Observed vs assumed:** observed: ILOSTAT/STEP wage premia available (not fitted) | assumed: returns,
  credential premiums | gap: task-41 top gap 5

### S6 eq06_migration_rural_urban — rural-urban/migration
- **Data tier:** SYNTHETIC
- **Plain result:** Education raises the migration probability in every specification (marginal effect range
  0.0089–0.0140) and migrants are more educated than stayers; networks slightly REDUCE the estimated marginal
  effect (0.0089 with vs 0.0140 without), so the ad hoc "networks increase the effect" criterion FAILS. MASSENG
  v5 does not model rural-urban migration, so this is a synthetic demonstration of the equation, not a model
  output.
- **Multiverse range:** [0.00892, 0.01404]; spec_robust=True
- **Decision rule:** FAIL (post-hoc; no pre-registered rule for this new script)
- **Observed vs assumed:** observed: WDI urbanisation, UN migrant stock, remittances available (not fitted) |
  assumed: flows, costs, networks | gap: task-41 top gap 4

### S7 eq07_inequality_dashboard — inequality/dashboard
- **Data tier:** SYNTHETIC + OBSERVED/RECONSTRUCTED descriptive dashboard check
- **Plain result:** In the null world the intergenerational elasticity is indistinguishable from zero (90% CI
  −0.00 to 0.00); in the persistent world it is 0.45 and the Theil decomposition puts 0.10 of inequality between
  parent-education groups. The elasticity, the Gini and the transition matrix are different summaries of the same
  synthetic process, not interchangeable evidence.
- **Inequality domain:** Gini/Theil/within–between are computed on exp(child log income) = level income (strictly
  positive); IGE, rank–rank and Oaxaca (log points) stay on log income. Gini persistent 0.6006; Theil within
  0.6141 / between 0.0951; the previous Theil-within was NaN and the Gini was computed on negative log values.
- **Multiverse range:** [0.4503, 0.5167]; spec_robust=True
- **Decision rule:** PASS=True `{null_elasticity_ci_includes_0: True, persistent_elasticity_positive: True, theil_between_positive: True}`
- **Observed vs assumed:** observed: WID/SWIID, Barro-Lee, Learning Poverty; committed long_run_panel used
  descriptively (schooling coefficient for effective fertility −0.372, SE 0.0631; TFR −0.3316, SE 0.0644) |
  assumed: mobility process, dashboard thresholds | gap: descriptive use only

### S8 eq08_growth — structural change + macro/development
- **Data tier:** SYNTHETIC (+ descriptive OBSERVED cross-section if input present)
- **Plain result:** In the clean world the convergence coefficient is recovered and the human-capital term is
  zero; with an omitted TFP term correlated with human capital the human-capital coefficient is inflated
  (0.5192 vs 0.0008), so a positive growth coefficient is not evidence of a causal human-capital effect.
- **Multiverse range:** [0.00085, 0.51924]; spec_robust=True
- **Decision rule:** PASS=True `{clean_lambda_near_truth: True, confound_inflates_beta_H: True, nelson_phelps_interaction_positive: True}`
  (smoke FAILS `clean_lambda_near_truth`; see verdict accounting)
- **Observed vs assumed:** observed: WDI GDP, GGDC/PWT, Barro-Lee; committed x4_panel used descriptively with
  honest split | assumed: Solow/NP parameters, structural-change mapping | gap: descriptive use only

### S9 eq09_identification — test bench
- **Data tier:** SYNTHETIC
- **Plain result:** Each design recovers its target in its own known-truth world and is near zero in the no-effect
  control; the naive estimators are biased in the stated violation worlds (IV 1.49 vs OLS 1.76 against a true
  1.5; TWFE bias −1.15 vs the group-time estimator −0.02). This is a demonstration of the designs, not an
  estimate of any real programme.
- **Fix note:** TWFE dummies were transposed (unit/time swapped for the row-major layout) and the 2SLS SE used
  fitted-D residuals; both fixed. TWFE mean 0.785 → 0.138, bias −0.499 → −1.146 (the old transposed dummies were
  accidentally attenuating TWFE bias); IV SE mean 0.082 → 0.045.
- **Decision rule:** PASS=True `{null_twfe_near_zero: True, null_iv_near_zero: True, null_rd_near_zero: True, null_sc_near_zero: True, iv_closer_than_ols: True}`
- **Observed vs assumed:** observed: none needed (known-truth synthetic designs) | assumed: all DGP parameters |
  gap: n/a

### S10 eq10_tutoring_shadow — exams-shadow (single tutoring module)
- **Data tier:** SYNTHETIC + LITERATURE_TARGETS (Bray; descriptive check only)
- **Plain result:** Tutoring behaves as one exams-shadow module for demand: on the log1p scale (same units as the
  0.8 truth) the two-part model is closer than the Tobit (0.73 vs 1.37); the log1p Tobit does NOT recover the
  truth, so the dropped pre-registered single-process rule fails (Tobit within-0.15 share 0.00). On inequality the
  own-teacher ban does NOT raise the learning Gini once the Gini is computed on a strictly positive level domain:
  in this reduced production model there is no substitution margin, so removing tutoring lowers the Gini in every
  CES/retention specification (Δ range −0.064..−0.041). The illustrative model is far from Bray's targets
  (max |z| = 10.6), so nothing here is a fit to a real shadow-education system.
- **Tobit scale:** same **units** as the 0.8 truth (log1p); the estimate recovers **1.441 single / 1.370
  different** vs truth 0.8, i.e. **0.64/0.57 away**, and `tobit_within_0.15_share = 0.0` — the dropped
  pre-registered single-process rule **FAILS**. The level-scale fit (8.612 / 8.781) is reported separately and
  never compared to 0.8.
- **Gini domain:** exp(achievement index); the raw additive index is non-positive in ~37% of draws, where the Gini
  is undefined (old committed Ginis were 0.71–1.07, outside [0,1]).
- **Decision rule:** FAIL `{two_part_closer_than_tobit: True, ban_raises_gini_in_all_specs: False, model_not_claimed_to_fit_bray: True}`.
  The dropped pre-registered S3 sub-rules are carried alongside (not in PASS) and surface via `run_all.py`
  `rule_flags`: `dropped_prereg_S3_different_two_part_within_0.15=True`,
  `dropped_prereg_S3_different_tobit_outside_0.15=True`, `dropped_prereg_S3_single_world_both_within_0.15=False`.
- **Observed vs assumed:** observed: no harmonised tutoring panel; Bray targets are literature targets | assumed:
  demand and production parameters | gap: no tutoring data

## Deviations log (dated 2026-11-25, this run)

The pre-registration says any later change must be logged here. Committed-before-run rules were not deleted;
each deviation below is stated with its effect on the verdict.

1. **eq03 estimator is a 2-D (ρ, ω) grid, not the pre-registered 1-D grid over ρ** (Amendment 02 S3). Rationale:
   the old 1-D estimator regressed A^ρ on (1, S^ρ, T^ρ) and returned ρ̂ = 0.2 in both worlds. With the corrected
   normalised-CES objective, a 1-D grid **does** pass (median ρ̂ = 0.60, share within 0.10 = 1.00) but **only**
   if ω is pinned at the DGP value ω = 0.6; with ω ∈ {0.4, 0.5, 0.7} the 1-D criterion fails (share 0.00). The
   2-D grid makes the PASS independent of an oracle ω. The PASS flip is caused by the objective fix, not by the
   extra grid dimension. `rho_recovered_within_0.10` is itself an added (post-hoc) criterion.
2. **eq05 2SLS now has an intercept and n−k σ²** (Neon Part A). The old slope was read off the intercept-free
   column stack; the 2SLS estimate moves 0.0836 → 0.0897 and its bias −0.0064 → −0.0003. Rule PASS unchanged.
3. **eq04 `q`-shadowing bug**: the quota_share gap loop reused the name `q`, so those gaps were NaN and three of
   the five multiverse specs silently vanished from the recorded range. Fixed; range [−0.0912, 0.7614]; the
   sign of the quota gap depends on the quota share (spec_robust=False). Pre-declared S4 FAIL unchanged
   (default 0.5-share quota gap +0.0906).
4. **eq04 MASSENG boundary flag** True → False (Amendment 03 says exam bar/quota are outside MASSENG v5); the note
   now splits progression/capacity (in v5) from bar/quota (not in v5).
5. **eq06 has no pre-registered decision rule** (new script, Amendment 02 lists only multiverse choices). The
   implemented "network effect larger than no-network" criterion is ad hoc; it fails (0.00892 < 0.01404) and the
   plain summary now says so.
6. **eq07 inequality domain** changed from log income (negative values → NaN Theil, out-of-domain Gini) to level
   income exp(log income); this changes Gini 0.24 → 0.60 and Theil between 0.0128 → 0.0951 in the persistent
   world. eq07's top-level data tier corrected to include the observed dashboard check.
7. **eq09 identification fixes** (TWFE dummy transpose; 2SLS SE from actual-D residuals). TWFE bias −0.499 →
   −1.146; IV SE 0.082 → 0.045. The demonstration's conclusion (TWFE biased, CS-style close) holds more
   strongly.
8. **eq10 Tobit scale and Gini domain** (see S10 above). Consequence: `ban_raises_gini_in_all_specs` flips
   True → False and S10 PASS → FAIL. The old ΔGini 0.0247..0.3721 was computed on a variable with ~37%
   non-positive draws.
9. **`run_all.py` verdict semantics** changed from process exit code to the script's own `decision_rule.PASS`
   (plus sub-test flags). Under the old semantics this same run would have printed "Failures: []".
10. **eq04/eq06 plain summaries corrected** where they asserted the opposite of their own numbers (S4 quota
    "flips" a +0.0906 gap; S6 "networks increase" when 0.00892 < 0.01402).
11. **`write_result` refuses non-finite JSON.** The old eq04 had 12 literal `NaN`s and eq07 had 3; the
    re-recorded results have zero non-finite values and 11/11 JSON files strict-parse.
13. **S10's dropped pre-registered S3 sub-rules are now reported in `decision_rule`** (prefixed
    `dropped_prereg_S3_...`) and therefore appear in `run_all.py`'s `rule_flags`. They are *not* part of
    S10's `PASS`: the implemented-rule flags are computed first. This makes the dropped-rule failure
    traceable instead of prose-only.
12. **Not changed here:** the DHS `ir_pipeline` CONSTRUCT clustering change (woman → PSU) belongs to the DHS
    branch and does not appear in this record.

## What ran / what failed

- 10/10 scripts executed (smoke then full); execution failures `[]`; no run discarded.
- 3 decision-rule failures: **S4 (pre-declared), S6 (post-hoc), S10 (implemented rule + dropped pre-registered
  S3 sub-rule)**. Smoke additionally flags S8 (full passes) and mirrors S4/S6/S10.
- Real-data use: **S8** uses the committed `x4_panel.csv` (OBSERVED aggregates) with an honest ISO3-sorted
  train/validation split and persistence/training-mean benchmarks; **S7** uses the committed `long_run_panel.csv`
  (OBSERVED/RECONSTRUCTED) as a descriptive country+year FE check; **S10** uses Bray six-school targets
  (LITERATURE_TARGETS) as an external reality check only.
- All other scripts are SYNTHETIC demonstrations with stipulated DGPs (see `data_map` per script and
  `PRE_REGISTRATION.md`).
- Records: `results/run_all.json`, `results/run_all_manifest.csv`, per-script `.json`/`.csv`. The old server
  `run_console.log` is not part of this re-recorded run; the re-recorded command and wall time are in
  `run_all.json`.
