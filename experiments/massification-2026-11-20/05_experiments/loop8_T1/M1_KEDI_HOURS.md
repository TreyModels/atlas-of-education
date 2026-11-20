# M1 — KEDI Table 2 hours denominator (verified at source)

**Question (Council brief 012, critical).** Are the "weekly participation hours" in KEDI Table 2 measured among
*participating* students or among *all* students? The answer determines whether the predeclared T1 rule's
"hours fall" clause fires.

## Answer — verified from the source on disk

Source: `04_data/shadow_round2/raw/korea_mods_2023_private_edu_survey.txt` line 178, the footnote under
`<Table 2> Private education participation rate and weekly participation hours by school level`:

> **"※ Data on weekly participation hours covers the total students."**

**Therefore the hours series (7.5 / 7.4 / 6.7 h/week) is per ALL students, not per participating student.**
Per-participant hours = hours / participation = **8.72 / 9.81 / 10.09 h/week** (elementary/middle/high):
hours per participant **RISE** with stage, they do not fall.

## Recomputation under the correct convention

| stage | participation | hours/week (all students) | hours/week (participant) | spend per participant (k won/mo) | implied price (won/h, 52/12) |
|---|---|---|---|---|---|
| Elementary | 86.0% | 7.5 | 8.72 | 462 | 12,225 |
| Middle | 75.4% | 7.4 | 9.81 | 596 | 14,006 |
| High | 66.4% | 6.7 | 10.09 | 740 | 16,926 |

Price ratio high/elementary = **1.384 (+38.4%)** under 52/12. Under 48/12 and 9.5/12 the multiplier cancels in the
cross-level ratio (levels shift, ratio unchanged): see `m1_recomputation.csv`.

## Consequence for the predeclared rule

Predeclared rule: "two/three-margin verdict if price/hour rises ≥20% **while participation and hours both fall**."
Under the correct denominator: price +38.4% (≥20% ✓), participation falls ✓, but **hours per participant rise**
(the "hours fall" clause fails). So **the rule does not strictly fire as written** — the verdict is amended:

- **Forced (robust):** the one-margin "arms-race participation" description must be withdrawn — spend per student
  rises (+23.7% derived) while participation falls 19.6 pp. A two/three-margin (participation × hours/price)
  description is required.
- **Not established:** "hours of study fell" (false under the correct denominator) and "price escalation" as a
  measured fact (price is a constructed residual, +38.4% under M1, sensitive to numerator breadth and subject mix).
- **Rule status:** price condition met, hours condition fails ⇒ **conditional/pending M2** for the price reading.

## Citation language now permitted

*"Because participation falls while spend per student rises, a one-margin arms-race account cannot describe the
Korean profile; the rise is consistent with higher spend per participant and higher per-participant hours, not with
widening participation. Whether this reflects price or composition requires the provider×subject decomposition
(M2)."*

**Prohibited until M2:** "price escalation", "families paid 79% more per hour", "hours of study fell", any causal or
cross-country transfer.
