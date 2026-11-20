> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# COUNCIL DELIBERATION 012 — adversarial read of T1

**Panel (AI composites):** BRAY (shadow education, mandatory), PATRINOS (measurement/econometrics; steel-man),
PAGE (decomposition/arithmetic), CARTWRIGHT (claim discipline).
**Input:** `05_experiments/loop8_T1/{PRE_DECLARATION.md, T1_FINDINGS.md, t1_inputs.csv, t1_decomposition.csv,
t1_summary.json, t1_korea.py}`; `04_data/shadow_round2/data/{shadow_incidence_round2.csv, shadow_fees_round2.csv}`;
briefs 010/011. Programme remains CLOSED; T1 advisory.

## Agreed (with severity)

1. **Arithmetic is sound (no error).** participation × per-participant spend = 397.3/449.4/491.4k, reproducing the
   reported 398/449/491k within 0.17/0.09/0.07%; the log identity is exact (residual 0 by construction). No
   double-counting of non-participants: numerator is per-participant spend; the per-student series is its
   participation-weighted product. **PAGE: the decomposition is definitional, not informative about mechanism.**
2. **The "price" term is a constructed residual, not a measured price (major).** q = all-private-education spend per
   participant ÷ survey participation hours. It absorbs provider mix (hagwon/1:1/group), subject mix (general vs
   arts/physical; math/English), purpose mix (makeup/advance/next-level), academic vs vocational high school,
   materials/textbooks, quality/class size, and participant selection. +79.3% is an **upper bound** on any true
   price change; it cannot be called price escalation.
3. **Hours denominator is ambiguous in the source (critical).** `shadow_incidence_round2.csv` reports KEDI Table 2
   hours with denominator "students", while participation rows name school-level students. If hours are per *all*
   students, per-participant hours are 8.72/9.81/10.09 (rising), and the decomposition becomes: Δln spend/participant
   0.4715 − Δln hours/participant 0.1457 = price log-change 0.326 (ratio 1.385, +38.5%). The predeclared rule's
   conjunction ("price ≥ +20% while participation and hours both fall") then **fails on the hours clause**; the
   verdict should be *indeterminate pending verification*, not "fired".
4. **Internal inconsistency (minor).** `T1_FINDINGS.md` says +23.4% (reported series 398→491); `t1_summary.json`
   computes +23.7% (derived 397.3→491.4). Pick one series and label it.
5. **52/12 is defensible only as an assumption.** It cancels across levels if Table 2 hours are year-average; if
   term-time, seasonal composition by level can bias the cross-level price path. Report sensitivity (52/12, 48/12,
   9.5/12).
6. **What T1 does force:** the paper's one-margin "more participation drives spend" mechanism description is
   contradicted by its own best case — participation falls 19.6 pp while spend rises. That sentence must be
   rewritten. **What T1 does not force:** a "price race" interpretation; that requires provider/subject/selection
   decomposition. T2 (legitimation) is untouched and design-only.

## Disagreements preserved

**D1. PATRINOS (dissent) vs PAGE/CARTWRIGHT — did the rule fire?** PATRINOS: the predeclared rule cannot be said to
have fired until the hours denominator is verified; under the alternative convention the "hours fall" conjunct fails,
so the correct verdict today is *indeterminate/conditional*. PAGE: regardless of the hours convention, the spend rise
is not participation, so the one-margin participation mechanism is withdrawn either way. CARTWRIGHT: split the verdict
— descriptive mechanism rewrite **forced**; price interpretation **not established**. *Resolution:* adopt the split
verdict; record PATRINOS's formal dissent, and require M1 before "rule fired" is printed.

**D2. BRAY vs PATRINOS — which composition check is decisive?** BRAY: provider × level (KEDI Tables 9–11) is
decisive for the basket story. PATRINOS: selection (income-band × level) is equally decisive because participation
falls 19.6 pp and the leavers may be lower spenders. *Resolution:* run both (M2, M3); predeclare that if
within-provider and within-income-band spend/hour rises less than half the aggregate, composition/selection explains
most of the +79%.

**D3. CARTWRIGHT vs all — the word "hours fell".** CARTWRIGHT: the paper may not write "hours of study fell" until the
denominator is verified; report both conventions in a footnote. BRAY/PAGE concur; PATRINOS adds that the rule's
conjunction depends on it.
