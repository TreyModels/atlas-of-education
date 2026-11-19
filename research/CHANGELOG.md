# Research amendment, 16 November 2026

Purpose: preserve small, inspectable models while making their propositions and limits testable. No production numerical claims are added.

## Code and experiment changes

- Credential screening v3 separates the same-year premium intervention effect from scenario growth and preserves incomplete chunk remainders. Independent seed identities prevent overlapping chunks. KS output carries a narrower interpretation.
- Tutoring matches provider reports to pupil-level events, exposes source-school subsets and subject representation, and permits alternative teacher initial conditions. Nonconverged states cannot pass calibration. The final SMC evidence estimator uses raw mixture densities with zero terms outside prior support; proposal budgets and calibration-completion metadata are explicit.
- Cambodia experiments can use indexed household-event randomness and a national-income grouping proxy. Legacy options remain the shipped defaults. No new empirical programme coefficient is claimed.
- Teacher pipeline scenarios can continue the 2030 hiring floor or taper it, and can carry a declared share of unmatched candidates into subsequent applicant pools. Defaults retain the previous arithmetic.
- Monsoon scenarios can change the assumed response shape, cap extrapolated PDSI, and override the stochastic seed. Stored summaries are withheld for variants outside their original design.
- The common runner plans and records trials across eight families, hashes code/inputs and preserves failure status. It includes reviewed institutional factorials and a companion-repository dispersal adapter. Full production runs are delegated to the local execution instructions.

## Amendment to the shadow ODD

**Purpose and patterns:** the provider targets count pupils naming providers among tutored pupils in three source schools. They do not count purchases per subject. These outcomes can overlap for a pupil; the remaining percentage is not an exclusive commercial category. Source-school mappings need further evidence.

**Entities and scales:** four subjects remain the default; six-subject variants use declared illustrative offsets. This changes pupil-subject representation and teacher count. Variant runs record the chosen offsets.

**Initialization and scheduling:** `all_sell`, `none_sell` and seeded `random` teacher states can be compared with the same generated pupil/teacher attributes. A solver reaching its sweep budget remains an unfinished sequence; it does not supply an equilibrium fit.

**Observation:** source provider probabilities use any purchase from the provider across subjects divided by any tutoring participation, over the declared school subset. Purchase shares remain available for different questions. Coverage remains curriculum coverage, with no calibrated mapping to learning or welfare.

## Numerical outputs

Prior results and downloadable bundles are historical. Corrected equations require new runs before numbers, fits or evidence values can be updated. The common runner reports synthetic variability and design-conditional Monte Carlo error; empirical sampling uncertainty and outside-data validation require additional work.

# Rigor amendment, 16 November 2026 (second pass)

- Six runner families in `research/rigor/`: `credential_recovery`, `shadow_recovery`, `youth_placebo`, `youth_rolling`, `fertility_placebo`, `camchild_validation`. Thresholds and verdict words are declared in `rigor/protocols_rigor.json` before any run; `rigor/analyze.py` applies them.
- `engine/relfloor_gate.py`: an eligibility-gate structure (M_GATE) that gives the relational account an institutional rule and observable implications. With the gate off it reproduces `relfloor_countries.sim` exactly (tested).
- `engine/firms/model.py`: new parameter `dr_date` (default `(2021, 8)`, output unchanged; tested) so the residual step can be moved for placebo tests.
- `rigor/stats.py`: Diebold–Mariano with HLN correction, MASE, leave-one-out ABC model recovery, paired summaries; known-answer tests in `tests/test_rigor.py`.
- `analyze.py` also tests the `schools` backtests against their flat benchmark and marks series with fewer than 10 forecasts as anecdotal.
- No engine default and no shipped number changed.
