> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# REVIEW — PAGE composite (model reasoning / scaling) — brief_013

**Scaling verdict.** The on-disk fits (pattern-scout, provisional) show the right lesson: PHL GER-secondary prefers
Gompertz over logistic, primary prefers logistic, tertiary fits are unstable (K_se ≈ 171, t0_se ≈ 147), and the
common-shape test rejects shared slopes for secondary/tertiary while not rejecting for upper-secondary/NER (low
power). Therefore: **bounded diffusion is a candidate form, not a law; the functional form is not identified by fit
alone.** The model must be constrained to produce *a* bounded diffusion path with country-specific timing and must not
take shape parameters from the fitted curves as inputs. Use the scaling relations as (a) excluded holdout moments,
(b) sign/inequality constraints (R13 education→growth negative; R04 positive; R02 null), (c) out-of-sample country
targets. Falsifier: if the model needs the fitted shape to reproduce the shape, it has restated it (R4).

**Dissent:** the common-shape test on disk uses F-tests on nonlinear fits; check assumptions and use information
criteria/bootstraps before calling "no common shape" a finding. Also, 8 experiments overreach the fleet; the slate
should be sequenced, not parallelised.
