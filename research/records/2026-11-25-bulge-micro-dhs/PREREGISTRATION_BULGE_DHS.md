# PRE-REGISTRATION — Bulge Arrival, **DHS micro leg** (wealth gap in secondary attainment by `t*` cohort)

**Branch:** `research/bulge-micro-dhs-2026-11-25` (additive; no push). **Record:** this directory.
**Date:** 25 November 2026. **Author:** `dhs-runner` (delegated lane; Lead: `lead`).
**Status: written BEFORE any estimation. No estimation was run. The registered data gate FAILS (§7), so the
main specification is empty by rule, not by hindsight.** This is a pre-registration, not a results note.

Language rule: **association only.** Permitted: "is associated with", "the estimate for cohort c is". Forbidden:
"effect of abolition", "caused", "drives", "led to". Nulls and failures are reported, never dropped.

---

## 1. Question (micro leg of the Paper-#2 bulge test)

The macro test (Paper-#2 packet: `~/neon-boot/paper2/PREREGISTRATION_BULGE_ARRIVAL.md`) asks whether the
primary-school bulge reaches the **primary→secondary gate** at `t* = t_abolition + L_primary`. The DHS
individual-recode (IR) micro leg asks the distributional version:

> **Does the wealth gap (Q5 − Q1) in women's secondary attainment widen for cohorts exposed to the post-abolition
> bulge (`t*`-exposed), even though the primary wealth gap had narrowed 6–8 years earlier?**

This is a descriptive, associational question about repeated cross-sections of individual women. It cannot
identify a causal effect of fee abolition, does not use a treatment/control contrast, and is not a policy
evaluation.

## 2. Sourcing rule (binding, inherited from the Paper-#2 preregistration)

Every input must be traceable to a **real repo file at a named branch + commit**, else it is `UNSOURCED`, the
country is excluded and the value is **not** estimated, inferred, rounded or borrowed:

- `t_abolition`: `research/records/2026-11-25-e6e8-sequencing/data/fee_dates.csv` @
  `research/e6e8-sequencing-2026-11-25` @ `2d19da7` (blob `85d09f86…`), `preferred_year`, `status=VERIFIED`.
  **8/8 E8 countries sourced** (MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005).
- `L_primary` (length of the primary cycle, years): **must come from a repo file**. A repo-wide search finds
  **no** education-structure / ISCED-duration file (`L_primary` / `primary_length` / primary-duration). Therefore
  `L_primary` is **UNSOURCED 0/8**, `t*` is **UNSOURCED 0/8**, and **no cohort is assigned exposure**.
- No "standard 6–8 years" fill-in; auditor candidate lengths (UGA 7, MWI 8, TZA 7, KEN 8, GHA 6) are recorded as
  unadopted candidates only (Paper-#2 §4).

## 3. Registered estimand (executed only if the §7 gate passes)

Unit: woman *i* in birth cohort *c* (5-year bins from `v011`), DHS round *r*, country *k*.

- **Outcome (secondary attainment):** `S_ic = 1{v106 >= 2}` (attained secondary or higher). `v106 < 2` = 0.
  **Definitional limit, fixed now:** the DHS IR contains **no school-entry date/age**; this is *attained*
  secondary, not entry timing. Wording in any report must say "attained secondary", never "entered secondary".
- **Primary-attainment comparator (the "6–8 years earlier" claim):** `P_ic = 1{v106 >= 1}` (attained primary or
  higher), estimated on the same cohorts as a descriptive check; it is not a causal "narrowing".
- **Exposure:** cohort *c* is `t*`-exposed if its members would have been at the primary→secondary transition in
  the school year beginning at `t*`; operational rule registered as: birth-year interval
  `[t* − 15, t* − 11]` for the primary-completion cohort (women aged 11–15 at `t*`; DHS `v011` gives the birth
  year exactly). Where `t*` is unsourced, no exposure is assigned.
- **Wealth:** `v190` quintiles (1–5); `v190` missing/not-finite → drop the row from wealth models (listwise; logged).
  Q5−Q1 gap = coefficient difference between `wealth_5` and `wealth_1` in the same model.
- **Model:** linear probability (WLS) or logit (reported both, LPM primary), with birth-cohort FE, DHS-round FE,
  region×round FE (the record's patched `ir_pipeline` convention), `v005` survey weights (per-survey normalised),
  PSU-clustered SEs (`v021`), controls: urban (`v025`) + a 5-year-cohort trend; education is the outcome, not a
  control. No wealth-as-control (wealth is the stratifier).
- **Sample:** women aged 40–49 (completed-fertility frame reused for consistency), standard-DHS rounds only
  (`SurveyType=="DHS"`, 72-file rule), E8 countries, rounds with ≥2 waves per country; `v190` and `v106` non-missing.
- **Contrast of interest:** cohort × wealth-quintile interaction `γ_c` (change in Q5−Q1 gap for `t*`-exposed vs
  adjacent cohorts), reported with CI; the parallel primary-attainment contrast is reported alongside.
- **Pre-trends:** cohort-specific Q5−Q1 gaps for the 5 cohorts before `t*`; a flat pre-trend is required before any
  "widening" reading.
- **Placebo:** `t*` shifted **6 years earlier** (and 4 years later as a second shift); the Q5−Q1 contrast for the
  pseudo-exposed cohort must be ≈0 for a result to be read.
- **Decision rule (registered):** report "consistent with a widening Q5−Q1 gap at the `t*` cohort" **only if**
  (i) pre-trends are flat (no monotone trend in the pre-period gaps), (ii) the earlier-shifted placebo is ≈0,
  and (iii) the `γ_c` 95% CI excludes 0. Otherwise report the estimate as inconclusive/null — never dropped.
- **Multiplicity:** one primary contrast (secondary attainment, Q5−Q1); the primary-attainment contrast and the two
  placebos are labelled secondary and not used to rescue a null.

## 4. Registered data gate (run BEFORE estimation) — outcome: **FAIL**

| gate item | requirement | found | verdict |
|---|---|---|---|
| `t_abolition` | sourced per country | 8/8 sourced (`fee_dates.csv` @ `2d19da7`) | PASS |
| `L_primary` | repo file stating primary-cycle length | **none in repo** | **FAIL** |
| `t*` | = t_abolition + L_primary | **UNSOURCED 0/8** | **FAIL** |
| DHS IR microdata | 48 standard-DHS E8 IR files obtained and manifest-verified (target CSV: 48 DHS + 13 MIS + 6 AIS = 67 rows) | **0/48 held** (no `.dta`/`.zip` on box or repo; Africa-11 request not yet submitted) | **FAIL** |
| secondary-entry variable | direct entry timing in IR | **absent by instrument design** (attainment `v106` only) | **FAIL (definitional, logged)** |

**Registered consequence.** Because the gate fails, the main specification, the pre-trends and the placebos are
**NOT-ESTIMABLE**; **no estimation was run**, no cohort was assigned, and no number was invented. This is the
pre-registered outcome, not a post-hoc excuse: the gate rule was fixed before any data was in hand.

## 5. What would make it estimable (exact acquisitions)

1. Commit a hashed `L_primary` source file per E8 country/year (e.g. UNESCO UIS ISCED duration of primary, or
   World Bank EdStats education-structure table) with source URL + locator → then `t*` is computable 8/8.
2. Submit the DHS **Africa-11** request (contains the 8 E8 countries) and download the **48** standard-DHS IR files
   (67 target rows total: 48 DHS + 13 MIS + 6 AIS);
   verify against `dhs_ir_inventory_targets.csv` (see `DATA_AVAILABILITY.md` §1 in the Paper-#2 micro record).
3. Accept the definitional limit (attained secondary, not entry) or find an alternative instrument with entry
   timing; this is not fixable inside the DHS IR.
4. Re-run this registration unchanged; no re-specification after seeing outcomes.

## 6. Boundaries

No DHS microdata was read (none exists in holdings); no simulation is cited; no synthetic rows are used here.
All language is associational. This record does not touch the IR pre-registration (`2026-11-24-dhs-acquisition`)
or the DHS-API ecological record; it is a separate, gated micro leg.
