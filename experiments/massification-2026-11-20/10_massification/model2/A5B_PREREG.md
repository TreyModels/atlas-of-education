# PRE-REGISTRATION — A5b rival re-score: crossing ordering/spacing + mechanism-implied ordering (PHL anchor)

**Written before running.** Authority: A5/A6/A7 (D42/D47–D52), R23 (asymmetry is the anchor criterion), R24
(timing alignment), R25 (event evidence descriptive), R13 (no direction claim). Fit **1999–2013**, holdout
**2014–2024**. Levels are NOT the score; ordering/spacing and event breaks are. A single shared universalization
curve/timing is a structural miss (R23) and may at most be PARTIAL. No git writes.

## Observed anchor signature (D47; crossing = first observed year ≥ threshold)
Primary completion ≥90 **2017** (91.92; 98.30 by 2024); lower-secondary completion ≥90 **2024** (92.41);
upper-secondary completion **never ≥90 by 2024** (59.70→75.03); tertiary GER ≥50 **2024–25**. Observed sequence:
primary < lower ≤ tertiary; upper never. **Design-only rivals (listed in every results file, never modelled,
never claimed as tested — D48):** (1) **human capital** — requires PSA returns by education (FIES/APIS/LFS
microdata; blocked, external request needs approval); (2) **signalling/MMI** — requires employer requirement /
credential module (Enterprise Surveys; blocked). These are DATA ASKS, not testable cells.

## Four testable rivals (same PHL record, same events, same fit/holdout windows)
1. **World-society timing (Meyer/Schöfer):** one shared bounded-diffusion timing across levels — logistic with a
   **common r and t0**, level-specific K fitted on 1999–2013 (shared-timing constraint is the rival's signature).
2. **State-building step (Paglayan):** per level, linear model on education spending %GDP, teacher stock and
   pupil–teacher ratio (observed 1995+); predict holdout with observed covariates. No event dummies beyond the
   policy series itself.
3. **Demographic/cohort contrast:** per level, linear model on log cohort (0–14), log population, urbanisation and
   GDP pc; predict holdout with observed covariates.
4. **Formal-model shapes:** per level, independent logistic fit on 1999–2013 (no shared timing) — tests whether the
   bounded-diffusion shape family alone reproduces the asymmetry.

## Scoring (predeclared)
For each rival and milestone, derive predicted crossing year = first predicted year ≥ threshold (else "not
reached" by 2050). Report: ordering pairs (primary<lower, lower<tertiary, upper never), gap errors vs observed
(primary→lower ≈7 y; lower→tertiary ≈0.5 y), upper-secondary false-positive (predicted ≥90 by 2024), and
**mechanism-implied ordering** per rival as predeclared:
- world-society: near-simultaneous crossings across levels (shared timing) — expected **structural miss** (R23) if
  all four crossings fall within 2 y;
- state-building: policy-sequence order (primary before lower before upper), upper may not cross;
- demographic: cohort-compression order (primary earliest, then lower; upper later);
- formal shapes: no shared timing; order determined by independent fits.
**Observational-equivalence (R23/R3):** a rival is *equivalent* if its predicted ordering AND all milestone
crossings are within ±5 y of observed and it has no upper-secondary false positive; otherwise it is distinguished.
**Event-break scoring:** observed vs predicted change 2013→2024 for upper-secondary completion and tertiary GER;
sign and magnitude error (no rival receives event dummies, so this is the anchor-vs-unconditional-rival dimension).
**Timing alignment (R24):** for PHL events (1987, K-12 2013, free SHS 2016, free tertiary 2018) report
event-to-crossing gap on the affected level, post-window flag, predicted sign and quality; a push counts only if
computable, ±5 y OR crossing inside post window, sign matches — otherwise **context, not mechanism** (no causal
claim, R24/R25).

## Decision rule
A5b reports which testable rival (if any) reproduces the observed ordering/spacing and event breaks; if none,
**EQUIVALENT/structural miss for all four** is the honest result (anchor comparison remains deferred to A1).
No direction claim; all cells reported including failures.
