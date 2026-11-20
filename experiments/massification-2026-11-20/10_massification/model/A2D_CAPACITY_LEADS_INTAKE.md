# A2d — capacity-leads-intake test: DESCRIPTIVE-NEGATIVE report (no new fitting)

**Owner:** experiment-runner (`deepseek-exp1`). **Status:** reported from the completed A1 anchor run; **no refit, no
tuning**. **Authority:** A2 predeclaration, A10/R29 (capacity level-specific), R24/R25, D56–D58/D61. Simulated and
observed labelled; no direction claim (R13).

## Test as predeclared
Capacity (delivery) **leads** intake/enrolment with a declared lag of **2–4 years**, predicted sign **positive**;
placebo = reverse ordering (intake leads capacity) reported as failure; observed capacity = PHL high-school PTR
37 (2000) → 27 (2014) → 24 (2017), teachers hired 2012–16, classroom ratios 2010/2019/2021 (observed cells;
`SCHOOL_EXPANSION.csv`); model capacity index C_t from the declared composite (delivery 0.5 / fiscal 0.3 /
enforcement 0.2) with gate G(C)=C^κ (κ=0.75 declared).

## Result (from the completed anchor run, `anchor_out/run_meta.json`)
- Best cross-correlation between ΔC and enrolment growth over lags 0–6: **r = −0.427 at lag 6**.
- **Negative** at the best lag, and no positive relation at the predeclared lags 2–4 → the predeclared
  capacity-leads-intake relation is **NOT supported**.
- Interpretation limited to description: capacity moved (PTR 37→27→24 across 2000–2017) but the model does not show
  capacity growth *leading* enrolment growth; the observed PTR improvement coincides with the primary ≥90 crossing
  window but this test cannot attribute the crossing to it (A10 already shows capacity is not sufficient for the
  ceiling; the floor precondition is untested here because the model's floor crossings are left-censored).

## Verdict and limits
**DESCRIPTIVE-NEGATIVE:** the capacity-leads-intake hypothesis is not supported by the predeclared test (reported,
not tuned). NULL is a valid result (R25/R12). No direction claim; no behavioural re-fit; the standing scaling FAIL and
the PARTIAL/DESCRIPTIVE phase cap are unchanged. What would unblock a stronger test: annual observed capacity series
(classroom construction by year = DATA ASK; per-student spending/revenue capacity = DATA BLOCKED), and a floor regime
where the model's floor crossings are not left-censored.
