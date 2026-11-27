# Revision 1.2 release checks

The paper and technical manuscript describe an exploratory mechanism simulation, not empirical Guangzhou effects. All outputs were regenerated after the cumulative-premium correction, wealth-graded restriction and exclusive-route changes.

Experiments: 1,024 independent parameter settings × 40,000 pupils; 128 settings × 8 cohorts; 150-setting mechanism ablations; 256 settings at each of three fixed enforcement gradients. The sweep includes 32 independent uniform inputs. Deterministic seeds and SHA256SUMS support reproduction. Independent cross-machine reproduction of this revision remains open.

The principal CSV has unique draw IDs, finite numeric values and exact capacity/band assertions. A deterministic draw was replayed. verify_model.py checks exact cumulative premium scaling, exclusive routes, zero-ban equivalence and neutral-world wealth independence over 20 cohorts. The neutral-world geometric-mean ratios are T 1.0003, S 1.0044, S* 1.0021.

The complete Spearman and partial rank correlation table is bundled. Rank correlations assume approximate monotonicity and describe the specified ranges; they do not identify causal effects or variance shares. TEACH_SD also sets HS_TEACH_SD.

Lean 4.36.0 checks Admission.lean. FORMAL_AUDIT.md states the abstraction boundary. The proofs do not verify the Python program, parameter values or empirical validity.

The combined before/after contrast changes restrictions and senior-2 reassignment together. The separate no-ban scenario holds reassignment on. Neither is an estimate of Double Reduction’s actual causal effect. Families do not re-optimize spending, prices do not adjust, and empirical calibration/validation remain open.

S and T compare local-hukou wealth groups in ten bands of the top cohort-wide score or ability quintile. S* uses score and ability cutoffs within the top score quintile and requires five pupils in each wealth group per retained cell.

The university proxy targets 10% with an inclusive cutoff; exact capacity was checked for these sampled runs, not proved universally. Alternative routes are bonuses in one ranking rather than real separate admission systems. N_PRIV counts schools.

Section 5 is an exploratory estimand diagnostic. Binary tutoring combines doses; generator coefficients are not automatically regression targets. No stronger estimator-validity claim is made.

Source metadata are recorded in references.json and SOURCE_NOTES.json. The unresolved Zhang (2016) author-year attribution is omitted. No confidential transcript or personal educational pathway is released. Informal field context is not a representative survey.

Status: suitable for advisor feedback as a scoped exploratory working paper. Independent empirical validation and external statistical peer review remain open.
