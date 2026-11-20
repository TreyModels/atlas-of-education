# GATE ACK — Council brief-013 (SUCCESS_CRITERIA §2–§4 + Amendments A1), copied VERBATIM

Registered by experiment-runner-2 (deepseek-exp2) before M2b/M2c. Sources: 08_council/brief_013/SUCCESS_CRITERIA.md, STOP_RULES.md. Copied at 2026-11-20; no edits.

## Amendment A1 (2026-11-20 14:34) — forced-ID intake: scaling exponents and direction claims

**Trigger:** model2 push-pull recovery (predeclared, SIMULATED): recovery demand-led 1.00, supply-led 1.00,
complementary 0.00; a truth outside the candidate set forced-identified at 1.00; equivalence share 0.07 →
**push-pull NOT IDENTIFIABLE**; no direction claim was made from observed data (`10_massification/model2/runs/`).

1. **Reproducing universalization now requires two things, not one:** (a) the trajectory checks of §2–§3
   (levels, shape, timing, holdout, false-positive, cohort conservation), AND (b) **reproduction of the stable
   scaling exponents** classified on WDI30 (`scaling_classification.csv`): secondary GER ~ income **+0.286**
   (0.045), tertiary GER ~ income **+0.776** (0.086), lower-secondary completion logit ~ income (classified
   scaling law; magnitude ratio 1.76 — coefficient to be re-verified in M2b, exp2 reports a discrepancy),
   with the model's simulated exponents inside the **estimator range** for ≥2 of 3 laws, and with
   **country-specific timing** (no common logistic slope: common-shape rejected for secondary/tertiary). A model
   that fits one curve but does not generate the exponents does not "reproduce universalization".
2. **Direction claims:** no push/pull direction or complementarity claim may be made from cross-country/panel
   moments. The default verdict for direction is **EQUIVALENT (R3/R13)**. Only an identified two-shock design
   (E1) or the jointly predeclared E2+E3 pair may support a direction claim.
3. **New verdict: PASS-CONDITIONAL.** The model may PASS-CONDITIONAL if it reproduces the trajectory and the
   scaling exponents **conditional on a declared channel mixture** (push/pull weights declared per scenario, not
   fitted, not claimed identified). IDENTIFIED (unconditional) requires E1 (or E2+E3 joint) to pass.
4. **M2b authorized:** exp2 re-runs Parts 1–2 (scaling + universalization) against the now-landed
   `10_massification/relations/data/` with a declared amendment (same estimators/thresholds), posts `NEW:` with
   hash; Part 4 recovery is design-bound and is re-run only as **M2c**: the E1 two-shock estimator's own recovery
   test (simulated), before E1 is fielded.

## STOP_RULES Amendment A1 (R13–R15), copied VERBATIM

## Amendment A1 (2026-11-20 14:34) — R13–R14 (forced-ID intake)

| # | Rule | Trigger |
|---|---|---|
| **R13** | **Direction claims from cross-country/panel moments are barred:** if a recovery/forced-ID test shows the estimator assigns channels confidently without identification (forced-ID > 0), no push/pull/complementarity claim may be made from those moments; report EQUIVALENT and require E1 (or the predeclared E2+E3 pair) | model2 recovery: forced-ID 1.00, recovery complementary 0.00 |
| **R14** | **Scaling-exponent reproduction is a gate, not decoration:** if the model cannot generate the classified scaling laws (secondary GER ~ income +0.286; tertiary +0.776; lower-sec completion law) within the estimator range and with country-specific timing, the universalization reproduction claim is capped at PARTIAL | `scaling_classification.csv` |
| **R15** | **Conditional-labelling:** any reproduction claim made under a declared channel mixture must be labelled PASS-CONDITIONAL; presenting it as identified is a rule violation | A1 §3 |
