# BUGFIX — fixed-effect parameterisation in the ecological estimator (supersedes `708e34a` numbers)

**Found:** 2026-11-24 ~23:40, while validating a closed-form reduction against the committed region-42 results
(task-36). **Fixed:** `scripts/estimate.py` (intercept pre-pended; indices shifted), verified on the new box.
**Nothing here touches DHS microdata** — all numbers are OBSERVED / ECOLOGICAL published cells.

## 1. What was wrong

`scripts/estimate.py` (committed at `856c421`, run at `708e34a`) built every fixed-effect design by **dropping the
first level of each categorical FE as the reference but including no intercept**. That silently constrains the
reference group's mean to zero instead of estimating it. The correct parameterisation is either all FE dummies
(no reference dropped) or dropped-reference dummies **plus an intercept**. The prior DHS record
(`research/dhs-micro-2026-11-23 @ 31ded00`) used the correct weighted within-transform, so **the prior record's
numbers are correct**; it was my region-42 run that was biased.

**Magnitude:** small but systematic — about **+0.015 to +0.019 children** away from zero for the education
coefficients (the biased run was slightly closer to zero). Bootstrap ratios and the cohort interaction moved a
little more; the constructed ranking/verdicts mostly did not flip (see §4).

## 2. How it was caught

While reproducing the 11-country subset for task-36, a closed-form re-implementation of the estimator was
validated against the prior record. It matched the prior record exactly (−0.570 / −1.622 / −2.536 vs
−0.57 / −1.62 / −2.54, SE 0.058 / 0.170 / 0.235) **and disagreed with my own committed `results.json`
(−0.5545 / −1.6083 / −2.5203)** — the discrepancy was exactly the missing intercept.

## 3. Fix and verification

- `scripts/estimate.py`: `fit()` now pre-pends an intercept; all coefficient indices shifted by one
  (`run_spec`, `stacked`, `_country_task`).
- Independent cross-check implementation (`scripts/corrected_reduction.py`, weighted within-transform /
  alternating projections, no shared code with `estimate.py`) reproduces both the corrected `estimate.py`
  outputs **and** the prior record:
  - validation on the prior-spec panel: −0.5700 / −1.6216 / −2.5364 vs prior −0.57 / −1.62 / −2.54 →
    **max |Δ| = 0.0036 → PASSED**;
  - full sample: ratio 2-group 0.958225 and 4-level 1.002927, A-vs-B interaction 0.0158, C-vs-B −0.07747 —
    **identical to the corrected `estimate.py` run**;
  - 11-country subset: ratio 4-level 1.177998, A-vs-B −0.07948, Q1 M1 −0.7070 / −2.1627 / −3.1977 —
    **identical** (independent bootstrap streams give CI endpoints differing in the third decimal, points equal).
- **D1 after the fix is exact:** the corrected full-sample replication gives −0.5700 / −1.6216 / −2.5364 against
  the prior record's −0.57 / −1.62 / −2.54 (deltas ≤ 0.0036), where the biased run gave deltas of 0.012–0.020.

## 4. What changed in the reported numbers (full sample, all 87 countries)

| quantity | biased (commit `708e34a`) | corrected | change |
|---|---|---|---|
| M1 weighted, primary | −0.5355 | **−0.5541** | −0.0186 |
| M1 weighted, secondary | −1.5685 | **−1.5837** | −0.0152 |
| M1 weighted, higher | −2.5201 | **−2.5382** | −0.0181 |
| M0 weighted (country+period FE), secondary | −1.6357 | **−1.5934** | +0.0423 |
| 2-group M1 weighted | −1.5449 | **−1.5514** | −0.0065 |
| Q2a ratio, 4-level | 1.0170 [0.944, 1.102] | **1.0029 [0.932, 1.077]** | still "same sign, similar magnitude" |
| Q2a ratio, 2-group | 0.9602 [0.918, 1.002] | **0.9582 [0.915, 0.998]** | unchanged verdict (4 % lower) |
| Q2b1 A-vs-B interaction | −0.0044 (p=0.92) | **+0.0158 (p=0.70)** | still null |
| Q2b1 C-vs-B interaction | −0.0893 (p=0.00025) | **−0.0775 (p=0.0004)** | D4 still confirmed |
| cohort 2-group × decade | +0.1515 (p=0.26) | **+0.2438 (p=0.016)** | **D6 changes: indeterminate → attenuation** |
| per-survey share negative | 98.84 % | 98.84 % | unaffected (simple differences) |
| Q2b2 survey-level construct | unchanged | unchanged | unaffected (correlations of published aggregates) |

**Verdict changes:** D1 becomes exact rather than approximate; **D6 (cohort) moves from "indeterminate" to
"attenuation"** in the full sample (2-group interaction +0.244, p=0.016; higher +0.367, p=0.013), while the
11-country African subset shows *steepening* for secondary (−0.186, p=0.014 — see `AFRICA11_EXTENSION.md`). D2,
D3, D4, D5 keep their verdicts. The 2-group window contrast's CI now just excludes 1 (0.915–0.998), so under the
letter of the pre-declared D3 rule that contrast is "same sign, materially different magnitude" (by 4 %); the
4-level contrast remains "similar magnitude". Both are reported.

## 5. Files superseded / regenerated

- `results/results.json`, `results/model_table.csv`, `results/heterogeneity_countries.csv`,
  `results/heterogeneity_bh.json`, `results/heterogeneity_surveys.csv`, `results/survey_construct.csv` —
  **regenerated** by the corrected run on the new box (`results/server_box2/` logs).
- The biased run's logs are kept, renamed `results/server_superseded_biased/`, for the record.
- The old numbers remain in git history at `708e34a`; this file and the regenerated outputs supersede them.
- `REPORT.md` headline tables updated; a pointer to this file is in its §0.

## 6. Compute / provenance

- New box: `ssh -p 45973 root@connect.cqa1.seetacloud.com` (`/root/work/dhs-api/`), **8 workers**
  (`multiprocessing`), `OMP/MKL/OPENBLAS/NUMEXPR=1`, Python 3.10.8, numpy 1.24.1.
- Wall times: full-sample corrected run **24 s** (with the 11-country job chained before it), 11-country subset
  **13 s**; load average on the shared box ≈ 19–25 during the runs (other agents active; the job used ≤ 8 of the
  15-CPU container quota).
- No compute was run on the Mac for these estimates (only `rsync`/`git` and file inspection). The one earlier
  local attempt was killed per instruction and never resumed.

## 7. Rule changes (none to the science)

The pre-registration, decision rules D1–D7, indicators, samples and labels are unchanged. This is a
**correctness fix to the estimator**, not a change of hypothesis, sample or decision threshold. Its only
verdict-level consequence is the D6 change in §4, which is reported as a correction, not as a new result.
