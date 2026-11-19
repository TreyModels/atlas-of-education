# Research workbench

This collection contains toy models for exploring social mechanisms, descriptive planning tools, and retrospective empirical checks. A contribution can be a counterexample, a clearer mechanism, a better observation equation, or evidence that a proposed explanation fails. A useful theoretical model can remain small.

The revision adds executable designs for eight families. **No production experiment results accompany it.** Historical results remain available as versioned records. Code tests and small execution checks do not validate a model against a social system.

Start with [RUN_LOCAL.md](RUN_LOCAL.md). The [rigor families](rigor/README.md) add mechanism-recovery studies, placebo and rolling-origin forecast tests, spurious-regression benchmarks and an external check against a Cambodian experiment, with verdict thresholds fixed in advance ([rigor/protocols_rigor.json](rigor/protocols_rigor.json)). [rigor/READING_PILOTS_2026-11-16.md](rigor/READING_PILOTS_2026-11-16.md) reads the first local pilot runs. Questions, comparisons, failure criteria and empirical gaps are in [protocols.json](protocols.json). [literature.json](literature.json) connects sources to modelling decisions and records source access. [ISSUES.md](ISSUES.md) distinguishes code repairs from unfinished empirical work.

## What counts as a result

| Purpose | Defensible result | Requirements for stronger use |
|---|---|---|
| Theoretical exploration | These rules generate this pattern; these are the boundary conditions and counterexamples | Map rules and outputs to observed processes before explaining a particular society |
| Illustration or teaching | The example correctly demonstrates its stated proposition | A new evaluation argument before using illustrative outputs as estimates |
| Description and accounting | Defined quantities reconcile and match the reconstruction | Evidence about behavior before drawing causal conclusions |
| Prediction | A declared information set and procedure outperform a matched benchmark on untouched outcomes | New prospective evaluation when an outcome has already influenced model design |
| Policy scenarios | These assumptions imply these conditional consequences | Intervention-response and cost evidence before estimating programme effectiveness |

Edmonds et al. (2019) and Epstein (2008) distinguish modelling purposes. Computational sociology adds a substantive requirement: identify the actors, what they perceive, their institutional constraints and interactions, and the process connecting those interactions to the outcome (Macy & Willer 2002; Hedstrom & Ylikoski 2010). Bruch & Atwell (2015) explain how abstract models generate hypotheses and guide empirical research. One aggregate fit provides limited discrimination among mechanisms.

## Development and evaluation

Connect each substantive change to literature and to an exact rule. Label parameters measured, estimated, calibrated, derived, or assumed. An article motivating a mechanism does not supply every coefficient in its implementation. Cite the equation, table, page or dataset where possible. Record differences in population, period, units and outcome.

Use the shadow ODD with the amendments in [CHANGELOG.md](CHANGELOG.md). Expand other model descriptions where their entities, scheduling, inputs or rules remain unclear. Family experiment protocols do not substitute for full ODD descriptions. Keep a TRACE-style record of rationale, verification, sensitivity and unresolved evidence.

Shared code supports controlled nested comparisons. Its variants' agreement remains conditional on shared rules. Independent implementations can expose coding errors; they do not provide independent observations of society.

The runner crosses selected structural assumptions and nests random realizations within nuisance draws, preserving paired arms and failures. Parameter ranges are judgement choices. It supplies factorial probes and conditional Monte Carlo summaries, without claiming Sobol analysis, empirical sampling intervals or probabilities that social theories are true.

## Results and amendments

The credential counterfactual and tutoring observation equation changed. Old tables and posteriors describe previous experiments. Keep their version labels and write new results to new directories. Updated numerical headlines require completed runs and interpretation review.

Current survey targets and historical evaluation periods have already been inspected. New protocols provide an amendment record. Their timestamp does not make those data unseen. Prospective registration requires a genuinely future outcome and an externally timestamped commitment.

See [CONTRIBUTING.md](../CONTRIBUTING.md) to challenge a claim or propose a repair.
