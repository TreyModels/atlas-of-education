# Deviation / amendment note — full-system statistical screen (25 Nov 2026)

The multiverse pre-registration (`research/records/2026-11-25-masseng-edsystem/PRE_REGISTRATION_masseng_edsystem.md`,
analysis-plan item 5) fixed the summarisation rule as:

> "Seed-level uncertainty: mean and 90 % interval across 10 seeds for every reported cell; **no p-values**;
> no causal language."

`test_full_system.py` (this branch) adds OLS coefficients, cluster-robust SEs, 95 % CIs, Holm
correction and a **"supported" decision rule**. That is a change to the pre-declared analysis, so this
file logs it as a deviation rather than letting it pass as pre-registered.

## What was added, when, and why

| addition | when | why | status |
|---|---|---|---|
| OLS all main effects + seed FE, cluster-robust SE by design cell | first version (before the audit) | asked "are the multiverse contrasts regularities of the simulated design?" | **exploratory** |
| 95 % CI, normal p, Holm within contrast block, `supported = p<0.05 ∧ sign-consistent` | first version | decision rule for the table | **exploratory, not pre-registered** |
| estimability guard (SVD rank + row-space test), zero-variance guard, non-empty-stratum guard | 25 Nov, after Neon's line audit | four false-positive rows came from `pinv` on rank-deficient designs and `all([])` on empty strata | guard, does not create new claims |
| per-cell sign disclosure (`cell_sign_flips`, `cell_sign_flips_10pct`) | 25 Nov | the stratum check is a raw-mean heuristic; disclose how strict a per-cell check is | disclosure |

## Consequences for reading the record

- Everything in `MULTIVERSE_TESTS.md` / `full_system_tests.json` is **exploratory**: a screen of a
  simulation design, not a pre-registered test, and not an empirical claim.
- The Holm family is the estimable outcomes within one contrast block (8 blocks), **not** jointly
  controlled across the table; this is stated in the JSON `notes`.
- The p-values are not evidence about the world. "Supported" here means "the simulated design
  reproduces this sign with a small cluster-robust SE and a sign-consistent stratum check".
- If this screen is to be kept as a formal test, the honest route is a **new pre-registration for the
  test layer** (family definition, one primary contrast per axis, multiplicity policy, minimum cell
  size), run before looking at any further outcome. Until then, downgrade the wording.

## Not changed by this note

The underlying multiverse results (`results_multiverse.json`) and the multiverse pre-registration are
untouched; the four bogus "supported" rows are now reported as `not_estimable`, and the supported set
is published in full (45 rows) with the report/JSON reconciled.
