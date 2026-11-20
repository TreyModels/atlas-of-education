# A5b REPORT — PHL anchor rival re-score: crossing ordering/spacing + mechanism-implied ordering

**Fit 1999–2013, holdout 2014–2024** (declared in `A5B_PREREG.md`, written before running). No direction or causal
claim (R13/R24/R25); event evidence descriptive; no git writes. Code `code/a5b.py`; outputs `runs/a5b_*.csv`,
`runs/a5b_findings.txt`, `runs/a5b_meta.json`.

## Observed anchor signature (D47; from `UNIVERSALIZATION_SERIES.csv`, observed only)
- Primary completion ≥90: **2017** (91.92; 98.30 by 2024).
- Lower-secondary completion ≥90: **2024** (92.41).
- Upper-secondary completion: **never ≥90 by 2024** (59.70 → 75.03; peak 76.43 in 2017).
- Tertiary GER ≥50: **2025** (47.41 in 2024; ≥50 in 2025 — inside D47's 2024–25 range).
- Observed sequence: **primary < lower-secondary < tertiary**; upper never. This asymmetry is the anchor criterion
  (A6/R23); a single shared universalization curve/timing can at most be PARTIAL.

## Four testable rivals (same record/events; design-only rivals listed at the end)
| rival | predicted primary | lower | upper | tertiary | order correct | upper FP | EQUIVALENT (R3) | shared curve (R23) |
|---|---|---|---|---|---|---|---|---|
| world-society timing (shared r,t0) | 2014 | none | none | none | no | no | no | **yes — structural miss** |
| state-building step (spend, teachers) | none | none | none (NaN covariate) | none | no | no | no | no |
| demographic/cohort contrast | none | none | none | none | no | no | no | no |
| formal-model shapes (per-level logistic) | 2023 | none to 2050 | none to 2050 | none to 2050 | no | no | no | no |

*None of the four testable rivals reproduces the observed ordering/spacing; none is observationally equivalent
under ±5 y and no-false-positive (R3).* World-society is a **shared-timing structural miss** (only primary moves;
the asymmetry cannot arise). Formal shapes fitted pre-2013 have ceilings below the later thresholds, so they cannot
generate the 2024 lower/2025 tertiary crossings — a pre-2013-record failure, not a fit artefact. State-building and
demographic rivals produce no crossings in the holdout; the demographic upper-secondary extrapolation is implausible
(−122 pp), i.e. the rival fails rather than explains.

## Mechanism-implied orderings (predeclared) and what is observationally equivalent
- **World-society:** near-simultaneous across levels (shared timing). Predicted: primary only → **structural miss**
  of the observed primary/lower/tertiary spacing (R23); not equivalent.
- **State-building:** policy-sequence order (primary before lower before upper). Predicted: no crossings in holdout;
  does not generate the 2024 lower/2025 tertiary sequence; not equivalent.
- **Demographic/cohort:** cohort-compression order (primary earliest, then lower, upper later). Predicted: none;
  extrapolation unstable; not equivalent.
- **Formal-model shapes:** data-determined order; predicted primary 2023 with no later crossings; not equivalent.
**Observational equivalence set = empty:** given the observed sequence and ±5 y tolerance, none of the four
testable rivals' implied orderings is consistent with the record. (This is a statement about these rivals fitted to
this record, not a direction claim.)

## Event breaks (2013→2024 observed vs predicted change; pp; no rival receives event dummies)
| rival | upper-secondary obs/pred/err | tertiary GER obs/pred/err |
|---|---|---|
| world-society | +7.6 / +3.6 / −4.0 | +15.5 / −0.6 / −16.1 |
| state-building | +7.6 / NaN (missing covariate) | +15.5 / −12.9 / −28.5 |
| demographic/cohort | +7.6 / −122.1 / −129.7 | +15.5 / +11.1 / −4.5 |
| formal shapes | +7.6 / +6.4 / −1.2 | +15.5 / −0.8 / −16.4 |
No rival reproduces the post-2013 break; formal shapes comes closest for upper-secondary (−1.2) but misses tertiary
by −16.4. The anchor model (A1) must beat these on event breaks, not just levels.

## Timing alignment (R24) — PHL events (descriptive; no causal claim)
| event | affected level | observed crossing | event→crossing gap | verdict |
|---|---|---|---|---|
| PHL 1987 compulsory-primary lineage | primary | 2017 | −30 y | **context, not mechanism** |
| PHL K-12 2013 (RA 10533) | upper-secondary | never by 2024 | — | **context, not mechanism** (no crossing to align) |
| PHL free SHS 2016 | upper-secondary | never by 2024 | — | context, not mechanism |
| PHL free tertiary 2018 | tertiary GER | 2025 | −7 y (outside ±5; crossing in later window) | **context, not mechanism** (confounded with free SHS/K-12) |
Consistent with D50/D51: PHL's discrete state-push dates do not align with its universalization crossings; the
state-push mechanism is **not established** by these data and may not be assumed (A7/R24).

## Design-only rivals (D48; listed in every results file, NOT modelled and NOT claimed as tested)
- **Human capital** (Becker/Mincer): requires PSA returns by education (FIES/APIS/LFS microdata) — **DATA BLOCKED**;
  external request needs user approval.
- **Signalling/MMI** (Thurow/Collins; employer requirements): requires an Enterprise Surveys credential/skills
  module — **DATA BLOCKED**; external request needs user approval.
These are data asks, not testable cells this cycle; no citation of unread material (D49).

## Verdict
All four testable rivals **fail/are not equivalent (R3)** on the PHL anchor record; the observed asymmetry is not
reproduced by any of them, and the two blocked rivals cannot be tested. The anchor-vs-rival comparison remains
**deferred to A1**: the anchor model must beat this (weak) rival field on crossing ordering/spacing and event breaks,
or the honest A5 result is EQUIVALENT. No direction/causal claim; no git writes (executor commits).

---

## FINAL SCORING under the repair-failure ruling (D56–D58/R27, branch 3k)
Phase stands at **conditional reproduction + observational equivalence**; universalization capped **PARTIAL**;
anchor A1 descriptive-only. A5b's final scoring (added after the ruling; no re-fit, no threshold change):

- **Pairwise observational equivalence among the four testable rivals:** {state_building, demographic_cohort} are
  equivalent to each other only in the empty sense (both predict no crossing in the holdout); {formal_shapes} and
  {world_society} are each distinguished from all others (single early primary crossing, 2023 vs 2014).
  File: `runs/a5b_pairwise_equivalence.csv`.
- **Equivalence to the observed record** (primary 2017, lower 2024, tertiary 2025, upper never by 2024; ±5 y):
  **the equivalence set is EMPTY** — no testable rival is equivalent to the observed ordering/spacing.
  File: `runs/a5b_equivalence_to_observed.csv`.
- **No rival, including the anchor model class, reproduces the observed milestone ordering**; under D56–D58 the
  honest phase result is **EQUIVALENT + PARTIAL universalization**, with the observed asymmetry (primary 2017 <
  lower 2024 < tertiary 2025; upper never ≥90) left unreproduced by this rival field.
- **Design-only rivals remain listed in every results file** (human capital — PSA returns by education; signalling/
  MMI — Enterprise Surveys credential module; both DATA BLOCKED, not modelled, not claimed as tested, D48/D49).
- **No direction/causal claim; event evidence descriptive (R24/R25); never supplied as schedules (R4/R14).**
  Final scoring file: `runs/a5b_final_scoring.txt`; meta `runs/a5b_final_meta.json`.
