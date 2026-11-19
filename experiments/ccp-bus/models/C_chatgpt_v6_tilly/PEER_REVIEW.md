# Peer review: V6 Tilly model

Reviewer: gpt-6.1-terra. Review covers `model.py`, `tilly.py`, `observation.py`, `SPEC.md` and `checks.py` before the experiment batch. This is an implementation and design review, not empirical validation.

## Findings and responses

- Cohort membership follows immutable person IDs. First-act risk sets exclude people with a prior act, and the model records assistance, obligations owed, creditors exposed and illicit receipts separately. Person-case resolutions remain attached to the filed identity after departure.
- Public delivery and diversion exhaust the allocation; illicit payments redistribute the diverted amount. The obligation ledger records creation, lawful and illicit discharge, and departure write-offs. The supplied checks passed on the reviewed code, including identity mapping, accounting, settlement participation, case lag and a clean-outcome limit.
- Head appointees can request assistance from contacts. Protection is tied to the providing identity and cleared on provider exit. Promotion support requires payment to the live appointing boss. Hidden exchange protection no longer directly enters the center's target score.
- Equal-resource and zero-attraction controls address separate rank pathways; the no-replacement arm permits a shock comparison. The reset draws fresh supplier identities and clears inherited supplier tie strengths.
- A pre-batch policy error made `no_replacement` and `zero_attraction` also disable payment-based promotion. The code now removes that extra change, and `checks.py` compares each control policy to the campaign policy. The runner exports person-level cohort records and the 828-job manifest matches the current behavioral source hashes. Updated checks should pass before batch execution.

## Interpretation and remaining assumptions

Resource weights and the coefficients on obligations, requests and resource control are imposed. A positive relationship between dependency and misconduct under those settings follows partly from the decision rule. Paired ablations and parameter settings with zero or negative request pressure test its dependence on those assumptions; they do not establish a historical causal effect.

The model's local rewiring uses a candidate's latent current misconduct, consistent only with an explicit assumption of local knowledge. The center sees reports, performance and visible network signals; observed cases can include false filings. A true or false case describes the act associated with the filing, not a person's complete moral history. A clean appointment means no modeled prior misconduct for the synthetic outsider.

Access and obligation creation are simplified: one outstanding creditor per debtor, and assistance to a debtor with a different creditor need not create another debt. Organizational resets, legal discharge, supplier selection and the effect of reporting on emulation are model choices. Report the full cohort denominator, first-act risk sets, competing exits, uncertainty across seeds and parameter settings, and event histories when exported. The annual model output is not a fitted estimate of actual prevalence.

## Execution and analysis follow-up

The first batch stopped when a NumPy integer in the cohort risk count failed JSON serialization after a departure. Only no-replacement jobs had been saved. The count now converts to a Python integer, and `checks.py` exercises a complete cohort run, JSON export and stale-hash rejection. The restarted `results_completed` batch uses a new source hash; the earlier `results` batch is not evidence for the restarted runs.

Review of `analyze.py` found that 10-, 20- and 30-step cohort fractions retain the initial appointment denominator. For first misconduct, retirement and employment removal compete with the event because a departed person has no further modeled acts. Interpret these as event fractions under the modeled exit process, not risks under a hypothetical intervention that prevents exit. Delayed cases can resolve after retirement. True-case and false-case exits refer to the modeled act at filing; the latter does not imply an entirely clean career. Point-and-seed pairing and separate conditional seed MCSEs support within-model comparisons.

For any future use of ccporg.org as an observed-career source, define the pooled person-position-year population and event-specific inclusion, entry, exit and censoring rules before comparison. Publicly indexed career and network information has uneven coverage and cannot establish misconduct or the absence of a tie. Exclude rumor-based relationships from the primary analysis; retain source and confidence fields and investigate rumor inclusion separately. Current and previous-status graphs require an explicit temporal crosswalk. Sparse coverage assessments from selected provinces do not identify national inclusion probabilities.

## Raw-run audit during execution

A read-only audit at 560 saved runs examined 523 cohort jobs and 33,472 person records. Appointment and event times, exposure through retirement or removal, mutually exclusive exits, and the recorded case truth associated with each removal passed consistency checks. Independently computed first-act fractions at 10, 20 and 30 steps matched `analyze.outcomes` and the corresponding annual cumulative counts in every cohort run checked. All 540 Latin-hypercube jobs were present, covering all 15 scenarios at each of 36 parameter-point and seed pairs. No claim of full batch completion follows from this partial audit.

The model description explicitly records both positive initial and target closure and the logistic misconduct baseline. Accordingly, apparent reconstruction or eventual onset alone cannot establish a dependency mechanism; the relevant internal evidence lies in paired contrasts and sensitivity to the stipulated parameters.

The 120 reference jobs later completed, eight seeds per regime. In these synthetic runs, the sustained campaign produced a 10-step first-act fraction of 83.0% and a 30-step fraction of 87.5%; strong oversight produced 81.1% and 86.9%, respectively. True-case removal reached 6.4% under the campaign and 22.5% under strong oversight. Higher removal can shorten the period in which misconduct can be observed, so compare these fractions with exposure and competing exits. Across all officials in the last five periods, misconduct averaged 32.48% under the campaign and 28.14% with strong oversight. The default no-replacement arm averaged 32.50% in the same population outcome. These are descriptive reference estimates, not evidence that enforcement has a particular real-world effect.

## Completed batch and final numerical review

All 828 raw run files are present. The completed report states 37,260 annual rows. Independently recomputing all 15 reference rows from the raw files reproduced the displayed values after rounding. Across the eight reference campaign runs, the independently tallied cohort comprises 512 people and 8,718 person-years; 448 had an act, 33 left on true cases and one on a false case. At their first act, 189 received illicit payments in the same step; 310 had first owed an obligation by that step. These agree with the report.

The paired-effects table displays tiny emulation effects as zero to four decimals while counting signs from unrounded numbers. Those signs do not indicate a practically material direction. Counts above and below zero need not sum to 12, since exact-zero effects appear in neither count. The values reflect synthetic model assumptions and the listed exit process, with no empirical fit to real officials.
