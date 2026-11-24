# PRE-REGISTRATION — E8 Fisher RI **EXPLORATORY POST-HOC** follow-up probes (A1, A2)

**⚠ LABEL: EXPLORATORY / POST-HOC.** This file is written *after* the confirmatory RI results
(`results/e8_ri_results.json`, `REPORT.md`, classification `robust`) and is **not** a confirmatory
pre-registration. It fixes the two follow-up probes requested by the operator (via Lead) **before** either probe is
run, so the probes are not tuned to their outcomes. Nothing in the confirmatory record is changed: `PRE_REGISTRATION.md`
and `REPORT.md` stay as committed; this record only adds exploratory outputs.

**Branch:** `research/e8-fisher-ri-2026-11-25`. **Record:** `research/records/2026-11-25-e8-fisher-ri/`.
**Base (confirmatory):** `3535e49` (QA-fixed successor of results commit `d1e7b1c`; data/gate `263bef2`; prereg `4e466a3`).
**Date:** 25 November 2026. **Author:** `e8-fisher` (delegated lane; Lead: `lead`).
**Status: committed BEFORE either follow-up probe is run.** Host-only; Pool ≤ 8; no box, no shutdown/timer/watcher.

**Language rule:** association only; "consistent with" at strongest; no causal language. Every output is labelled
EXPLORATORY POST-HOC.

---

## 1. Why these two probes

The confirmatory RI (B = 10,000 per family, seed 20261125) gave two-sided `p2(T0) = 9.999e-05` (placebo-date),
`5.9994e-04` (placebo-country), `p2(Tpost) = 9.999e-05` / `2.9997e-04`, classification `robust`. The operator asked
which design choices could plausibly change that reading. Two were identified in `REPORT.md` §9 limitations:

- **A1 — control-pool contamination (limitation 4):** the 4 unresolved-date countries (CMR, ZMB, RWA, BDI) are
  never-treated controls in the E8 main specification and therefore 4 of the 40 placebo-country candidates. If any of
  them actually abolished fees in-window, both the control pool and the P2 candidate pool are contaminated.
- **A2 — far placebo dates (limitation 3):** the confirmatory placebo-date family draws dates anywhere in
  1990–2010 (minus true ±2), so many placebo cohorts are far from the true abolition date. A **local** placebo-date
  window (±3 years) asks whether the confirmatory result survives when placebo cohorts must sit next to the true date.

These are robustness probes of the confirmatory **inference**, not new estimands and not confirmatory tests.

## 2. Unchanged machinery (reuse, no re-estimation)

- Data: the committed `data/e8_primary_ger_panel.csv` (sha256 `365bcd43…`) + `data/wdi_region_map.csv`; WDI vintage
  Last Updated 2026-11-11. No re-download, no panel change.
- Estimator and statistics: exactly `scripts/e8_ri.py` (`event_stats`, imported as a module): CS ATT with universal
  base `g−1`, not-yet-treated controls (≥3), event time −5..+6, cohort-size-weighted event aggregation; `T0` = ATT at
  `e=0` (primary statistic); `Tpost` = unweighted mean of event ATTs `e=+1..+6`. Observed `T0`/`Tpost` are re-checked
  against the committed confirmatory JSON to 1e-12 before any probe runs; a mismatch is a stop.
- p-values and MCSE: same formulas as the confirmatory record —
  `p2 = (1 + #{|T_perm| ≥ |T_obs|})/(B_eff + 1)`, `p+ = (1 + #{T_perm ≥ T_obs})/(B_eff + 1)`,
  `MCSE(p) = sqrt(p(1−p)/(B_eff+1))`; undefined permutations excluded with `B_eff` reported.
- Seeds and draw rules: **identical** to the confirmatory families, so the probes re-use the same per-permutation RNG
  streams and change only the probe's window/pool:
  `numpy.random.default_rng([20261125, family_code, i])`, `i = 0..9999`, family_code **2** for A1, **1** for A2.
- B = 10,000 permutations per probe. Fork Pool(8) on the host; results invariant to scheduling.

## 3. A1 — placebo-country with the 4 unresolved-date countries excluded

- Sample and treated dates unchanged (8 verified dates; treated-in-Y = 8).
- Candidate pool **P′ = P \ {CMR, ZMB, RWA, BDI}** where `P` is the confirmatory 40-country never-treated
  SSA pool (SSA ∩ panel minus the 8 verified-treated). Expected `|P′| = 36` (asserted at run time).
- Draw rule identical to confirmatory P2: draw `size = 8` countries without replacement from `P′` sorted ascending
  ISO3 via `rng.choice(len(P′), 8, replace=False)`; sort the drawn countries ascending ISO3; assign the 8 actual
  dates (ascending-ISO3 date vector ETH 1995, GHA 2005, KEN 2003, LSO 2000, MOZ 2004, MWI 1994, TZA 2001, UGA 1997)
  via `rng.permutation(8)`. The original 8 countries are never-treated controls in each permuted world.
- Report: `p2(T0)`, `p+(T0)`, `p2(Tpost)`, `p+(Tpost)`, MCSEs, `B_eff`, `n_t0` and `n_post_events` distributions,
  permutation distribution mean/SD/quantiles, and number of draws ≥ observed.

## 4. A2 — local placebo-date window

- Treated countries unchanged (8 verified countries; only dates re-drawn).
- **Local window** for country `c` with true date `g_c`:
  `W_c^local = {g_c − 3, g_c + 3} ∩ W_c`, where `W_c` is the confirmatory feasible window
  (`{y ∈ 1990..2010 : outcome non-missing in y−1 and y} \ {g_c−2 … g_c+2}`). The true-date ±2 exclusion is thereby
  retained; each element of `W_c^local` is at distance 3 from the true date.
- Expected sizes, derived deterministically from the committed confirmatory
  `results/e8_ri_results.json -> sample.placebo_date_windows` (verified at run time): ETH 2, GHA 2, KEN 2, LSO 2,
  MOZ 2, MWI 1, TZA 2, UGA 2. If a window is empty the country is not re-dated (reported; expected none).
- Draw rule identical to confirmatory P1: countries in ascending ISO3 order, each consuming one
  `rng.integers(0, len(W_c^local))` draw.
- Report the same fields as A1.

## 5. Pre-registered reading rules (fixed before the probes run)

Baseline confirmatory values (from the committed `results/e8_ri_results.json`): placebo-country `p2(T0) = 5.9994e-04`,
`p2(Tpost) = 2.9997e-04`; placebo-date `p2(T0) = 9.999e-05`, `p2(Tpost) = 9.999e-05`.

- **A1 reading:** `unaffected` if `p2(T0) < 0.05` **and** `p2(Tpost) < 0.05` under P′; `partially sensitive` if
  `p2(T0) < 0.05` but `p2(Tpost) ≥ 0.05`; `sensitive` if `p2(T0) ≥ 0.05` (the confirmatory placebo-country result
  then depends on the contaminated-control pool).
- **A2 reading:** `unaffected` / `partially sensitive` / `sensitive` by the same rule applied to the local-window
  placebo-date family.
- **Overall:** the confirmatory conclusion ("consistent with a date-specific association; RI passes both placebo
  schemes") is reported as **unchanged** only if both A1 and A2 are `unaffected`; otherwise `FOLLOWUP.md` states which
  probe moved and how, while the confirmatory record is left exactly as committed. Exact p-values, MCSEs and counts
  are always reported; no multiplicity correction (exploratory); no post-hoc window or pool tweaking beyond A1/A2.

## 6. Outputs

- `scripts/e8_ri_followup.py` (imports `e8_ri.py` machinery; no new estimator).
- `results/e8_ri_followup.json` — both probes' summaries, distributions, p-values, MCSEs, B_eff, n distributions,
  determinism spot checks, seeds/draw rules, panel hash, confirmatory baseline.
- `results/e8_ri_followup_perms.csv.gz` — 2 probes × B = 10,000 rows (`probe, perm, T0, Tpost, n_t0, n_post_events`).
- `FOLLOWUP.md` — short exploratory report with the reading-rule outcome; explicit statement that the confirmatory
  record is unchanged unless a probe is not `unaffected`.

## 7. Stop rules

If the confirmatory gate JSON is missing/false, the committed panel sha256 does not match the confirmatory JSON, or
the re-computed observed `T0`/`Tpost` differ from the confirmatory JSON by more than 1e-12, the probes stop and the
failure is reported. No other stopping condition. No shutdown/reboot/power or watcher/timer action is taken.
