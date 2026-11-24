# BULGE ARRIVAL — DHS micro leg, status report (no estimation run)

**Branch:** `research/bulge-micro-dhs-2026-11-25` (additive; no push). **Record:** this directory.
**Date:** 25 November 2026. **Author:** `dhs-runner`. **Pre-registration:**
[`PREREGISTRATION_BULGE_DHS.md`](PREREGISTRATION_BULGE_DHS.md) (written before estimation).
**Data inventory:** [`DATA_AVAILABILITY.md`](DATA_AVAILABILITY.md).
**No estimation was run. No server/GPU was used for this record. No power/shutdown command was issued. No series
or duration was invented.**

---

## A. Verdicts

| leg | verdict | decisive blocker |
|---|---|---|
| `t*` = `t_abolition` + `L_primary` | **NOT-ESTIMABLE (0/8)** | `L_primary` has **no in-repo source**; `t_abolition` is sourced 8/8 |
| DHS IR micro: Q5−Q1 gap in secondary attainment by `t*` cohort | **NOT-ESTIMABLE** | **DHS IR: 0/48 held** (target set 48 DHS + 13 MIS + 6 AIS = 67 rows; Africa-11 request not submitted) **and** `t*` unsourced; IR also has no secondary-**entry** variable (attainment only) |
| DHS IR micro: primary-attainment comparator ("6–8 y earlier") | **NOT-ESTIMABLE** | same: no IR microdata held |
| LSMS-ISA tutoring / extra-classes / exam-prep spend (MWI, ETH, UGA, TZA) | **NOT-ESTIMABLE / item existence UNVERIFIED** | 0 LSMS-ISA files or questionnaires in holdings; no proxy permitted |
| Pre-trends / placebo (`t*` shifted earlier) / decision rule | **cannot be computed** | properties of an estimate; no estimate exists. Reporting them as "flat"/"≈0" would be fabrication |

This matches, and extends to the micro level, the macro verdict in the Paper-#2 packet
(`~/neon-boot/paper2/BULGE_ARRIVAL_STATUS.md`, C43–C44): `t*` 0/8 and the outcome series absent.

## B. Evidence (all traceable)

- `t_abolition` 8/8 VERIFIED: `research/records/2026-11-25-e6e8-sequencing/data/fee_dates.csv` @
  `research/e6e8-sequencing-2026-11-25` @ `2d19da7` (blob `85d09f86…`): MWI 1994, ETH 1995, UGA 1997, LSO 2000,
  TZA 2001, KEN 2003, MOZ 2004, GHA 2005.
- `L_primary` 0/8: no education-structure / primary-duration file in the repo (independently re-checked in the
  checked-out trees for `L_primary`, `primary_length`, ISCED/primary-duration files). No duration was borrowed
  from the auditor or assumed.
- DHS IR holdings 0: repo `git ls-files` → 0 `.dta` (DHS Terms forbid committing microdata); box scan
  (`/root/work`, `/root`) → no `.dta`/`.zip` > 1 MB; `/root/work/dhs_ir` does not exist. Only **target inventory**
  metadata exists: `research/records/2026-11-24-dhs-acquisition/data/dhs_ir_inventory_targets.csv`
  (48 standard-DHS E8 waves + 13 MIS + 6 AIS = 67 target rows; see [`data/dhs_ir_target_waves_e8.csv`](data/dhs_ir_target_waves_e8.csv)).
- DHS access status: Asia request "received and pending"; **Africa-11 request (contains all 8 E8) not yet
  submitted** — `research/records/2026-11-24-dhs-acquisition/application/STATUS_LOG.md`.
- Secondary-entry variable: DHS IR has no school-entry date/age; only attained level (`v106`, `v107`, `v133`,
  `v149`). The registered outcome is therefore **attained secondary**, explicitly not entry timing.
- LSMS-ISA holdings 0: no LSMS mentions in any record; no questionnaires/data on the box. Item existence
  (tutoring/extra-classes/exam-prep out-of-pocket) is **UNVERIFIED** and must be read from each wave's
  questionnaire after download (World Bank Microdata Library; Trey holds the registered account).

## C. What the "micro" question would have tested (registered, not run)

Registered estimand: cohort × wealth-quintile interaction `γ_c` — the change in the Q5−Q1 gap in **attained
secondary** for the `t*`-completion cohort, with an attained-primary comparator on the same cohorts, pre-trends on
the prior five cohorts, a `t*`-shifted-6-years placebo, and a one-sided (CI-excluding-0) decision rule. Full
specification, sample restrictions, controls and multiplicity rule are fixed in
[`PREREGISTRATION_BULGE_DHS.md`](PREREGISTRATION_BULGE_DHS.md) §3; none of it was executed because the §4 gate
failed first.

## D. What was NOT done (explicit)

- No estimation, no cohort assignment, no `t*` value, no wealth-gap number, no LSMS spending number.
- No proxy for `L_primary` (no 6/7/8-year fill-in), no proxy for tutoring spend (other school costs were not
  substituted), no synthetic or interpolated series.
- No conclusion of any kind about fee abolition, wealth gaps, or the bulge — there is nothing to conclude from
  without data.
- No power/shutdown command; no push; working tree additive only.

## E. Re-entry (exact next actions)

1. Commit a hashed `L_primary` source per E8 country/year (UIS ISCED primary duration or WB EdStats
   education-structure table, with URL + locator) → `t*` becomes computable.
2. Submit the DHS **Africa-11** request (the 8 E8 countries), download and manifest-verify the **48** standard-DHS
   IR files (67 target rows: 48 DHS + 13 MIS + 6 AIS; `data/dhs_ir_target_waves_e8.csv`), store outside the repo.
3. LSMS-ISA: download the four countries' candidate waves + questionnaires, inspect the education module for
   out-of-pocket tutoring/extra-classes/exam-prep items, commit hashed excerpts + exact variable names; if an item
   is absent in a wave, record it as missing (do not proxy).
4. Re-run this pre-registration unchanged.

## F. Risk / honest limits

1. The **hardest** blocker is the missing `L_primary` file (one acquisition, not a compute job) — after it, `t*` is
   immediate but the DHS IR files still need the country-approved access request.
2. Even with IR data, the instrument cannot measure secondary **entry** timing; the registered outcome is
   attainment, and any "entry" language would overstate what DHS observes.
3. The LSMS-ISA tutoring item may simply not exist in some waves; that is a finding, not a defect to fix by proxy.
