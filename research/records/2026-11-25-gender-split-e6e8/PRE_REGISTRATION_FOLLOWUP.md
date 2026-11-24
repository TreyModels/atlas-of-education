# PRE-REGISTRATION — EXPLORATORY POST-HOC follow-up to the gender split (task-7)

**Status: written and committed BEFORE any follow-up computation.** This file appends to task-3; it does **not**
edit the confirmatory `PRE_REGISTRATION.md` (commit `875ffd8`) or `REPORT.md` (commit `5b42bfd`), and it changes no
confirmatory number.

**Branch:** `research/gender-split-e6e8-2026-11-25` (confirmatory head `5b42bfd`). **Record:**
`research/records/2026-11-25-gender-split-e6e8/`. **Date:** 25 November 2026. **Author:** `gender-split`
(delegated worker; Lead `lead`), task-7. **Host-only** (host venv; no AutoDL box, no GPU, no power/watcher action).

**Labels (binding).** Everything in this follow-up is **EXPLORATORY / POST-HOC**. It uses only data and outputs
already committed in this record; it generates no new data and makes no new inferential claim that can replace the
confirmatory one. The confirmatory headline stands unless the pre-registered decision rule below fires, and even
then the result is reported as exploratory, in addition to (never instead of) the confirmatory result. Language is
association-only; no causal wording.

**Motivating question (operator).** The confirmatory primary statistic
`D = mean_{e=+1..+6}(ATT_F − ATT_M) = −3.94395 pp`, 95% paired-bootstrap CI **[−8.72, +0.29]** (includes 0 →
"no detected sex difference"), while the event-level differences at **+1** (−3.99 [−7.09, −0.53]) and **+2**
(−4.67 [−8.61, −0.87]) have CIs that exclude 0. Is the aggregate null a **weighting artefact** of the equal-weight
mean over six post events?

---

## B1 — inverse-variance weighted mean of the six post-event differences (RECOMPUTATION, not estimation)

Input: committed `results/e8_event_difference_verified8.csv`, post events `e ∈ {1,…,6}`.

For each `e`:
- `d_e = att_diff_F_minus_M` (committed point estimate);
- `se_e = (diff_ci_hi − diff_ci_lo) / (2 × 1.96)`, i.e. the reported 95% percentile paired-bootstrap CI half-width
  divided by 1.96. **This treats the percentile interval as a symmetric normal interval — a stated approximation;
  the underlying bootstrap distribution is skewed, so the weights are approximate.**
- `w_e = 1 / se_e²`; report both raw `w_e` and normalised weights `w_e / Σw`.

Statistic: `D_IV = Σ_e w_e d_e / Σ_e w_e`; `SE_IV = 1 / sqrt(Σ_e w_e)`;
95% CI = `D_IV ± 1.96 · SE_IV`.

Comparators, all reported:
1. the pre-registered equal-weight `D = −3.9439509825652124` with its committed paired percentile CI
   [−8.717832601194601, +0.29456768330537014];
2. an equal-weight mean with the *same* normal-approximation SEs for comparability:
   `D_eq = mean(d_e)`, `SE_eq = sqrt( (1/36) Σ_e se_e² )` (independent-events approximation), 95% CI
   `D_eq ± 1.96·SE_eq`.

**Pre-registered reading rule for B1.** If the `D_IV` 95% CI **excludes** 0, the equal-weight aggregate null is
partly a **weighting artefact** — this is reported as an EXPLORATORY finding and does **not** overwrite the
confirmatory "no detected sex difference" headline (it is added beside it, with its post-hoc status stated). If the
`D_IV` 95% CI **includes** 0, the confirmatory conclusion is unchanged and the event-level +1/+2 pattern remains a
descriptive, multiplicity-untested observation. Either way report sign, CI, and the full weight profile — no
selective reporting.

## B2 — leave-one-event-out equal-weight D (RECOMPUTATION)

For each dropped post event `e* ∈ {1,…,6}`: `D_(−e*) = mean_{e ∈ {1..6}, e ≠ e*} d_e`.
Report all six values, their range, and leverage `D_(−e*) − D_full` where `D_full = −3.9439509825652124`.
**Most influential event** = the drop with the largest |leverage| (ties: report both, flagged). Interpretation is
descriptive leverage only; no significance test is invented for it.

## B3 — drop-MOZ paired CS D (EXPLORATORY RE-ESTIMATION; optional, only if cheap on host)

Rationale: MOZ 2004 contributes no e=0 row (missing 2003 base) and 6 instead of 7 treated cohorts at several
horizons; the drop tests whether the D estimate leans on that one country's treatment timing.
Design: exactly the confirmatory design (`att_cs` from `bd782be`, SSA 1990–2015, verified-8 dates, universal base
`g−1`, not-yet-treated controls, event −5..+6, cohort-weighted aggregation), with **MOZ removed from the whole
sample** (not only from the treated dict — so it cannot re-enter as a never-treated control), **7 treated
countries**, 500 paired country-cluster bootstrap replicates with the same seeds `20261125+i`, percentile 95% CIs,
and the same primary statistic `D = mean_{e=+1..+6}(ATT_F − ATT_M)`. Report `D_dropMOZ`, its CI, replicates used.
This is a **new estimation** (different sample), reported as exploratory robustness; it cannot replace the
confirmatory estimate. If the run is not reliable on the host, report **"not run — reason"** instead of a number.

## Outputs, discipline, and what will not change

- New files only: `results/gender_split_followup.json`, `FOLLOWUP.md`, `scripts/gender_split_followup.py`, and this
  pre-registration. The confirmatory `REPORT.md` and `PRE_REGISTRATION.md` are **not edited**.
- Additive commit(s); push; never force; never `main`.
- All three probes and every null are reported. No new series, no imputation, no proxies.
- The confirmatory conclusion ("no detected sex difference; female and male post-abolition primary-GER
  trajectories are similar, female point estimate lower by 3.94 pp but the CI includes zero") stands unless B1's
  pre-registered rule fires, and even then the revision is flagged exploratory and remains alongside, not
  instead of, the confirmatory result.
