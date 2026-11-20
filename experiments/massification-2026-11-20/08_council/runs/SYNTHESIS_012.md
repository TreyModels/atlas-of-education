> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# SYNTHESIS 012 — adversarial read of T1 (advisory; programme CLOSED)

**Verdict in one sentence.** T1's arithmetic is sound and it **forces a descriptive rewrite** of the paper's
one-margin "arms-race participation" mechanism (spending cannot be participation-driven when participation falls),
but its headline "+79.3% price/hour" is a **constructed residual, not a measured price**, and the predeclared rule's
"hours fall" clause depends on an unverified Table 2 denominator — so the price-escalation reading is
**not established**, and "rule fired" should be reported as conditional on M1.

## 1. Arithmetic/identity audit

| Check | Result | Severity |
|---|---|---|
| participation × per-participant spend = reported per-student spend (398/449/491) | 397.3/449.4/491.4 — within 0.17/0.09/0.07% | ✓ pass |
| log identity (Δln L = Δln p + Δln h + Δln q; residual 0) | exact by construction; sum 0.2124 | ✓ pass (but definitional, not evidence) |
| per-participant spend = per-student/participation | exact to rounding (KEDI reports the tied series) | ✓ pass (circular but consistent) |
| **hours denominator** (Table 2 "students" vs participating students) | **ambiguous**; under all-students convention per-participant hours rise 8.72→10.09 and price ratio becomes 1.385 (+38.5%), the "hours fall" clause fails | **critical — M1 required** |
| 52/12 conversion | fine if Table 2 hours are year-average; term-time assumption biases cross-level path; multiplier cancels only under the stated assumption | medium — report sensitivity (52/12, 48/12, 9.5/12) |
| numerator breadth | all private education (general + arts/physical + materials) vs provider split general-subjects only (241+37+22+16+11 = 327 of 434k) | major for interpreting q |
| internal consistency | T1_FINDINGS +23.4% vs t1_summary +23.7% (derived) — pick and label one series | minor |
| double counting of non-participants | none: numerator per participant; per-student = participation-weighted | ✓ pass |

## 2. Inference audit — the residual contains the composition

q ("price") = spend per participating student ÷ survey hours. It absorbs: **provider mix** (hagwon vs 1:1 vs group),
**subject mix** (general vs arts/physical; math/English vs others), **purpose mix** (makeup/advance/next-level prep),
**school type** (academic vs vocational high school), **materials/textbooks**, **quality/class size**, and
**participant selection** (participation falls 19.6 pp; if leavers are lower spenders, per-participant spend rises
mechanically). KEDI tables on disk give provider spend only for all levels combined, so the decomposition cannot
separate price from basket. **+79.3% is an upper bound on true price change.**

**Alternative decompositions to run before any use (A1–A9):** A1 hours-denominator verification + month-multiplier
sensitivity; A2 provider mix × within-provider spend/hour by level (decisive); A3 general vs arts/physical/materials
split by level; A4 purpose mix by level; A5 academic vs vocational high school; A6 participation and spend by income
band by level (selection, decisive); A7 quality proxies (1:1/group/hagwon shares); A8 subject mix if reported;
A9 report reported and derived per-student series side by side.

## 3. Strongest objection and the evidence that answers it

**Objection.** The +79% is composition and selection: high-school tutoring is a different basket (academic exam prep,
hagwon/1:1, materials) bought by a selected minority of students; the "price" term is the union of those shifts, so
T1 measures basket upgrade, not escalation. **Evidence that would answer it:** (i) KEDI provider × level tables —
does within-provider spend/hour rise similarly? (ii) income-band × level participation and spend — do within-band
spend/hour profiles rise, or is the aggregate rise driven by who remains? (iii) the hours definition and seasonal
split. If within-basket spend/hour is flat while the aggregate rises, composition/selection dominates and the
"two-margin price story" must be described as a basket/intensity shift, not escalation.

## 4. Verdict and exact permissible language

**Two-level verdict:**
- **Forced:** the paper must withdraw the one-margin "arms-race participation" description. This follows from
  participation falling while spending rises, regardless of the hours convention.
- **Not established:** price escalation. The +79.3% is a constructed residual; the predeclared rule's "hours fall"
  clause is conditional on M1. Do not print "rule fired" without M1.

**Permissible language:**
> "In Korea (2023), spending per student rises 23.4% between elementary and high school even as participation falls
> from 86.0% to 66.4%. Because per-student spending is the product of participation and spending per participant, the
> increase cannot be a participation effect; in an exact log decomposition it is located entirely in spending per
> participating student-hour (+79.3% under the survey's reported weekly hours). That quantity is a composite of
> price, provider and subject mix, materials and quality, and the available tables do not separate them. The
> one-margin 'arms-race participation' mechanism is therefore withdrawn; the Korean case is described as an
> intensive-margin pattern whose price-versus-composition interpretation requires provider- and subject-level data."

**Prohibited:** "price escalation", "families paid 79% more per hour", "the arms race is a price race", "hours of
study fell" (until M1), and any causal or cross-country transfer. Add a footnote reporting both hours conventions
and the 23.4/23.7 percentage difference between reported and derived series.

## 5. Measurement steps (2–3) — and T2

| # | Step | Data | Settles | Cost |
|---|---|---|---|---|
| **M1** | Verify KEDI Table 2 hours definition (per participant vs per all students; term vs year) and the month convention; recompute both conventions | KEDI 2023 press release PDF table notes (on-disk URL) + methodology section | the "hours fall" clause and the rule's status (price +79.3% per-participant-hours vs +38.5% per-all-students; 52/12 vs 48/12 vs 9.5/12) | **~1 day** |
| **M2** | Provider × level and subject/purpose decomposition; within-provider spend/hour | KEDI Tables 9–11 by school level if published; otherwise table/microdata request to KEDI/KOSIS | is the rise within-basket (price/quality) or between-basket (composition)? | **1–2 days** if tables; **2–4 weeks** microdata request |
| **M3** | Selection test: participation and spend by income band × level; within-band spend/hour | KEDI income-band tables (press release/microdata) | is the +79% driven by who remains (falling participation) rather than by what they pay? | **1–2 days** tables; **2–4 weeks** microdata |

**Predeclared rule for M2/M3:** if within-provider and within-income-band spend/hour rises by **less than half** the
aggregate (+79.3%), composition/selection explains most of the movement; the paper then describes a basket/intensity
shift and drops escalation language.

**T2 — design only, not collected.** Legitimation vignette: arms = described family's tutoring investment
(high/low) × outcome (admitted/not); estimand = perceived fairness/meritocracy rating; threshold = investment arm
≥ +0.2 SD; N ≈ 600–1,000; cost low (one survey round, 2–4 weeks); no data exist — no claim may cite it.

## 6. Dissent recorded

- **PATRINOS (formal):** the predeclared rule cannot be said to have fired until M1 verifies the hours denominator;
  under the alternative convention the hours clause fails and the correct current verdict is *indeterminate /
  conditional*. Adopted as the caveat in §4; the descriptive mechanism withdrawal stands regardless.
- **BRAY:** provider × level (M2) is the decisive composition check; selection (M3) second. No dissent on the
  rewrite, but "price" must not appear.
- **PAGE:** the decomposition is an identity; treat it as organization, not inference; no causal language.
- **CARTWRIGHT:** split verdict adopted; language in §4 is the boundary; hours statement must carry its conditional.

**Cross-links:** brief 010 (Regime II mechanism), brief 011 (T1 as the first test; T2 as the distinctive test);
programme remains CLOSED — T1 does not reopen any stop rule, and neither does this advisory read.
