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

## Research projects and teaching materials

Projects aimed at a specific paper also pass the six points in [`GATE.md`](GATE.md). New ideas start in [`PUZZLE_LOG.md`](PUZZLE_LOG.md). Everything else in the repository is the teaching Atlas (see [`../teach/`](../teach/README.md)).

Each folder's README is generated from its result files and is the current source. The summaries below were written on 14 November 2026 and describe the designs tested then; they are not general impossibility results. The credential and tutoring code has since changed (see *Results and amendments* above), so their summaries describe previous experiments.

| Folder | Question | Status on 14 Nov 2026, under the tested design | Feeds |
|---|---|---|---|
| [`shadow-education/`](shadow-education/README.md) | Can the three explanations of own-teacher tutoring be told apart? | The current aggregate targets poorly distinguish the variants. "Favour" and "thin" are equivalent under a stated reparameterisation where the commercial-cost floor does not bind; "diversion" mostly behaves like "thin". A redesign with distinguishing signatures is needed. Historical: the tutoring observation equation has since been corrected. | Methods paper (as a case); a later shadow-education paper, after pupil-level data |
| [`credential-floor/`](credential-floor/README.md) | Can wealth profiles of completion separate four theories of the credential (human capital, positional, relational, Breen–Goldthorpe)? | Poor recovery on wealth profiles in a ten-dataset-per-structure design with these priors and tolerances. The response of completion to a change in the graduate premium is a proposed discriminator within these implementations. Historical: the premium counterfactual is now same-year (2035). | Massification paper with Nordtveit |
| [`china-forecast-ledger/`](china-forecast-ledger/README.md) | Do small models forecast China's youth unemployment better than "same month last year"? | No model beat the naive rule by a margin distinguishable from noise in retrospective tests. Forecasts for Oct 2026 to Mar 2027 are recorded for scoring; their freeze provenance rests on dated commits. | Methods paper; a public running scoreboard |
| [`marriage-gap/`](marriage-gap/README.md) | Is the gap in marriage wishes among unmarried Chinese men and women a preference gap or a selection effect? | The published chart cannot separate them; the headline rests on an opt-in online sample. Age-specific data would help. | Worked example of the gate; candidate microdata paper |
| [`methods-paper/`](methods-paper/OUTLINE_v2.md) | Revised outline, verified references, novelty assessment | Outline v2; novelty claims still need a fuller literature search. | The methods paper |

### Adding a month to the forecast ledger

Append the new NBS figure to `china-forecast-ledger/data/observed.csv` and run `python3 score.py` in that folder. Nothing is refitted.
