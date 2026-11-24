# FOLLOW-UP — E8 Fisher RI **EXPLORATORY POST-HOC** probes A1/A2

**⚠ EXPLORATORY / POST-HOC.** These two probes were defined **after** the confirmatory RI results and are reported
as exploratory robustness checks, not confirmatory tests. They do **not** change the confirmatory record:
`PRE_REGISTRATION.md`, `REPORT.md` and `results/e8_ri_results.json` (classification `robust`) remain exactly as
committed. Every number below is labelled exploratory; no causal language is used ("consistent with" at strongest).

**Branch:** `research/e8-fisher-ri-2026-11-25`. **Record:** `research/records/2026-11-25-e8-fisher-ri/`.
**Probe pre-registration (committed before either run):** `PRE_REGISTRATION_FOLLOWUP.md`, commit **`078dd7f`**.
**Confirmatory base:** `3535e49` (QA-fixed successor of results commit `d1e7b1c`; data/gate `263bef2`; prereg `4e466a3`).
**Date:** 25 November 2026. **Author:** `e8-fisher` (delegated lane; Lead: `lead`).

Machinery re-used unchanged from `scripts/e8_ri.py`: same committed WDI panel (sha256 `365bcd43…`, vintage Last Updated
2026-11-11), same CS estimator logic (universal base `g−1`, not-yet-treated controls, cohort-size-weighted event
aggregation), same statistics (`T0` = ATT at `e=0`; `Tpost` = mean ATT `e=+1..+6`), same p-value/MCSE formulas, same
master seed **20261125** and per-permutation RNG derivation. Observed `T0 = 12.4436239221`, `Tpost = 25.2607463695`
re-checked against the confirmatory JSON to `0.0`. **B = 10,000 per probe, host-only Pool(8), runtime ≈ 9 s.**
Per-probe spot checks (permutations 0/5,000/9,999 recomputed serially) match the stored draws to **0.0**.

**Confirmatory baseline being probed** (from `results/e8_ri_results.json`):

| family | `p2(T0)` | `p2(Tpost)` |
|---|---|---|
| placebo-date (confirmatory) | 9.999e-05 | 9.999e-05 |
| placebo-country (confirmatory) | 5.9994e-04 | 2.9997e-04 |

---

## A1 — placebo-country with the 4 unresolved-date countries excluded from the candidate pool

**Probe.** Candidate pool `P′ = P \ {CMR, ZMB, RWA, BDI}`, so `|P′| = 36` (from 40). Treated dates and draw rule
identical to confirmatory P2 (same RNG streams, family_code = 2). This addresses the *candidate-pool* half of the
contamination risk (REPORT limitation 4). It does **not** remove the four countries from the control group — E8's main
specification treats them as never-treated controls, and changing that would change the sample/estimand; that probe was
not run.

| statistic | `T_obs` | perm mean | perm SD | min | q2.5 | q50 | q97.5 | max | #(\|T\|≥\|obs\|) | B_eff | **p2** | **p+** | MCSE(p2) | MCSE(p+) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `T0` | 12.4436 | −0.7432 | 1.8993 | −9.3819 | −3.8826 | −0.9833 | 3.5488 | 10.5198 | 0 | 9,999 | **1.0e-04** | **1.0e-04** | 1.00e-04 | 1.00e-04 |
| `Tpost` | 25.2607 | −2.8273 | 4.5143 | −28.5398 | −12.1077 | −2.6457 | 5.7800 | 15.4822 | 1 | 10,000 | **1.9998e-04** | **9.999e-05** | 1.41e-04 | 1.00e-04 |

Effective treated n: `n_t0` mean **5.50** (min 0, max 8; 4.1% of permutations use 8 cohorts); `n_post_events` mean
5.999 (min 3, max 6). `B_eff(T0) = 9,999`: one permutation has no estimable `e=0` row (its `T0` is undefined and is
excluded from numerator and denominator, as pre-registered); no imputation.

**Reading (pre-registered): `unaffected`** — `p2(T0) < 0.05` and `p2(Tpost) < 0.05`. Excluding the four
contaminated-control candidates from the placebo-country pool does not move the confirmatory placebo-country result
below the 5% threshold (it is, if anything, slightly smaller: 1.0e-04 / 2.0e-04 vs 5.9994e-04 / 2.9997e-04).

## A2 — local placebo-date window (`g_c ± 3`)

**Probe.** `W_c^local = {g_c−3, g_c+3} ∩ W_c`, with the confirmatory feasible window `W_c` and the true-date ±2
exclusion retained; drawn with the confirmatory P1 draw rule (same RNG streams, family_code = 1). Window sizes:
ETH 2, GHA 2, KEN 2, LSO 2, MOZ 2, MWI 1, TZA 2, UGA 2 (one deterministic date for MWI). All windows non-empty.

| statistic | `T_obs` | perm mean | perm SD | min | q2.5 | q50 | q97.5 | max | #(\|T\|≥\|obs\|) | B_eff | **p2** | **p+** | MCSE(p2) | MCSE(p+) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `T0` | 12.4436 | 0.3694 | 1.1382 | −1.9632 | −1.7681 | 0.3545 | 2.4078 | 2.7383 | 0 | 10,000 | **9.999e-05** | **9.999e-05** | 1.00e-04 | 1.00e-04 |
| `Tpost` | 25.2607 | 8.0624 | 3.8553 | 1.1060 | 1.7522 | 7.9294 | 13.0685 | 13.7907 | 0 | 10,000 | **9.999e-05** | **9.999e-05** | 1.00e-04 | 1.00e-04 |

Effective treated n: `n_t0 = 8` and `n_post_events = 6` in every permutation (each local window year guarantees the
base year). Note the local placebo `Tpost` distribution is centred at **+8.06** (SD 3.86), not zero: shifting the
abolition date by ±3 years makes the "abolition year" partly a post-period year (for `g_c−3` the true-date window
`e=+3` post effect enters), so this probe is a *timing-sensitivity* check rather than a pure null. Even against that
upward-shifted local placebo distribution, the observed `Tpost = 25.26` exceeds every one of the 10,000 draws.

**Reading (pre-registered): `unaffected`** — `p2(T0) < 0.05` and `p2(Tpost) < 0.05`; both are at the resolution floor
`1/(B+1) = 9.999e-05` (MCSE 1.0e-4), i.e. no local placebo draw reached either observed statistic.

---

## Overall exploratory conclusion — confirmatory conclusion **UNCHANGED**

| probe | `p2(T0)` | `p2(Tpost)` | reading |
|---|---|---|---|
| A1 placebo-country, pool 36 (excl. CMR/ZMB/RWA/BDI) | 1.0e-04 | 1.9998e-04 | unaffected |
| A2 local placebo-date (`g_c ± 3`) | 9.999e-05 | 9.999e-05 | unaffected |

Both probes are `unaffected`, so per the pre-registered reading rule the confirmatory statement —
*"consistent with a date-specific association; RI passes both placebo schemes"* (classification `robust`) —
**is unchanged**. The confirmatory conclusion is therefore not sensitive to (A1) letting the four unresolved-date
countries act as placebo-treatment carriers, or to (A2) allowing placebo dates far from the true abolition date. The
confirmatory record is left exactly as committed; no confirmatory number or label is edited.

**Exploratory caveats.**
1. These probes are post-hoc robustness checks; their p-values are **not** confirmatory and no multiplicity
   correction is claimed. Both sit at the B = 10,000 resolution floor (`1/(B+1) = 9.999e-05`, MCSE 1.0e-4) where
   applicable — they mean "no placebo draw reached the observed statistic", not a precise tail probability.
2. A1 addresses only the placebo-candidate pool, **not** control-group contamination: CMR/ZMB/RWA/BDI remain
   never-treated controls in the permuted worlds, exactly as in E8's main specification. Removing them from the
   control group would change the sample/estimand and was not done.
3. A2's local placebo distribution is not centred at zero (see above); its role is to test whether the observed
   statistic is extreme relative to *nearby* date assignments, not to provide a pure null.
4. Small treated sample (7–8 countries) and missing-data heterogeneity (A1 `n_t0` mean 5.50) still apply; the RI
   probes complement, and do not replace, the published bootstrap CIs. No causal language: "consistent with".

## Files and reproduction

- `PRE_REGISTRATION_FOLLOWUP.md` (commit `078dd7f`, before any probe run).
- `scripts/e8_ri_followup.py` — imports `scripts/e8_ri.py` machinery; no new estimator.
- `results/e8_ri_followup.json` — both probes' full summaries, distributions, p-values/MCSEs, `B_eff`, n distributions,
  seed/draw rules, determinism spot checks, panel hash, confirmatory baseline.
- `results/e8_ri_followup_perms.csv.gz` — 2 probes × B = 10,000 = **20,000 data rows**, columns
  `probe, perm, T0, Tpost, n_t0, n_post_events` (20,001 lines = header + 20,000 data rows; sha256 `d2c5c5fd…` as
  recorded in the JSON).

```
# host, from this record root (confirmatory outputs already committed)
/Users/treymenefee/neon-boot/venv/bin/python scripts/e8_ri_followup.py    # A1 + A2, B=10,000 each (~9 s)
```
