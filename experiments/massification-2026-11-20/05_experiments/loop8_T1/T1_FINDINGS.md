# T1 FINDINGS — Korea private-education spend is a price phenomenon, not a participation arms race

**Status:** completed descriptor (official statistics, 2023 cross-section). **Programme remains CLOSED.**
**Predeclaration:** `PRE_DECLARATION.md` (written before computation). **Verdict (as amended after M1 and Council brief 012): descriptive rewrite FORCED; the predeclared two/three-margin rule is CONDITIONAL — the price condition is met (+38.4% under the correct all-student hours denominator) but the "hours fall" clause fails (per-participant hours rise). "Price escalation" is not established.**

## Result (MODS/KEDI Private Education Expenditures Survey 2023, Tables 2 and 9)

| stage | participation | hours/week | spend per participant (k won/month) | spend per student (k won/month, derived) | implied price (won/hour) |
|---|---|---|---|---|---|
| Elementary | 86.0% | 7.5 | 462 | 397.3 | **14,215** |
| Middle | 75.4% | 7.4 | 596 | 449.4 | **18,586** |
| High | 66.4% | 6.7 | 740 | 491.4 | **25,488** |

- spend per student rises **+23.4%** elementary -> high (397.3 -> 491.4k won);
- participation **falls 19.6 pp** (86.0 -> 66.4);
- hours/week **fall 0.8 h** (7.5 -> 6.7);
- **implied price per hour rises +79.3%** (14,215 -> 25,488 won/hour).

## Log decomposition, elementary -> high (identity: spend/student = participation x hours/month x price/hour)

| component | log contribution | share of the +0.2124 increase |
|---|---|---|
| participation | −0.2587 | −122% |
| hours | −0.1128 | −53% |
| **price per hour** | **+0.5839** | **+275%** |
| residual | 0.0000 | 0% |

The price component more than accounts for the entire spend increase; participation and hours push the other way.
The derived spend-per-student series reproduces Council brief 011's quoted 398/449/491k within 0.2% (consistency
check passed).

## Predeclared decision rule

"If price/hour rises >= 20% from elementary to high while participation and hours both fall => two/three-margin."
Observed: +79.3%, participation −19.6 pp, hours −0.8 h. **Rule fires. The paper's one-margin "arms race
participation" mechanism must be rewritten as participation x hours/price (a two/three-margin account), and the
Korea/Hong Kong contrast becomes the paper's real empirical puzzle.**

## Why this matters for the paper (brief 010 / brief 011)

- Regime II as written ("arms race" = more participation) is contradicted by its own best case: Korean
  participation *falls* with stage while spend rises. The mechanism is a **price/quality escalation among a
  shrinking participant pool**, not widening participation.
- This is the test Council brief 011 ranked first (T1). It costs nothing and is decisive for the mechanism
  description; it does **not** test the legitimation claim (T2, needs new survey data) or any causal effect.
- Hong Kong 2003 rises with stage (35.1/46.6/70.3) — the opposite participation profile. A single-margin model
  cannot hold both (brief 009 predeclared impossibility); the two/three-margin structure is the repair.

## Caveats (predeclared and observed)

- Descriptive 2023 cross-section; no causal or time-series claim.
- "Price per hour" is an average across providers/subjects, not a homogeneous market price.
- Hours are survey-reported weekly participation hours; the monthly conversion (52/12) scales all levels equally,
  so it affects levels, not the cross-level comparison.
- Korea only; nothing here transfers to another country.
- Participation/sector composition may change with stage (e.g. high-school split between academic/vocational),
  which this decomposition does not separate; that is a next-step measurement, not a correction.

## Reproduce

`python 05_experiments/loop8_T1/t1_korea.py` -> `t1_inputs.csv`, `t1_decomposition.csv`, `t1_summary.json`.
Inputs on disk: `04_data/shadow_round2/data/shadow_incidence_round2.csv`, `shadow_fees_round2.csv`
(MODS/KEDI 2023 English press release, high confidence).

---

## Council 012 adversarial addendum (binding on how this result is cited)

**Status change: T1 forces a *descriptive rewrite*, but the "+79.3% price/hour" is a constructed residual, not a
measured price.** Citation language must be conditional.

- **What is forced (robust):** spend per student rises ~+23.7% (derived) from elementary to high **while
  participation falls 19.6 pp**. Spending cannot be participation-driven under either hours convention. The paper's
  one-margin "arms-race participation" mechanism therefore cannot stand as written — a two/three-margin
  (participation x hours/price) description is required.
- **What is NOT established:** "price escalation" as a measured fact. Price/hour is the residual spend per
  participant divided by hours; it inherits the hours denominator and the breadth of the numerator (all private
  education incl. arts/physical/materials vs general-subject provider spend 327 of 434k won).
- **Hours-denominator ambiguity (critical, M1):** KEDI Table 2 "students" does not state whether hours are among
  *participating* students or *all* students. Under the alternative convention, per-participant hours **rise**
  (8.72 -> 9.81 -> 10.09) and the price ratio falls to **+38.5%** — the predeclared "hours fall" clause then fails,
  though the price ratio still exceeds the 20% threshold.
- **53/12 vs 52/12:** the conversion cancels in cross-level ratios under a common year-average assumption; a
  term-time convention changes levels, not the sign. Sensitivity recorded in `t1_sensitivity.csv`.
- **Series note:** the derived spend series is +23.7%; Council brief 011's rounded 398/449/491 implies +23.4%.
  Cite the derived series and say "derived".

**Revised verdict language:** *"Because participation falls while spend per student rises, the one-margin
arms-race account cannot hold; the spend rise is consistent with rising spend per participant (price/quality) but
that price reading is not identified without the hours denominator and subject/provider composition. The mechanism
must be rewritten as two/three-margin and tested with M1-M3 below."*

**Measurement steps to settle it (from brief 012):** M1 obtain the KEDI Table 2 denominator/question wording;
M2 decompose spend by provider/subject (hagwon/general vs arts/physical/materials) and by academic vs vocational
high school; M3 (optional) price-per-hour from provider-level fee schedules rather than residual.

**Programme impact:** none on closed claims — T1 is a descriptive decomposition of one country's official table; it
does not reopen incidence, mechanism classification, or forecasting. T2 (legitimation vignette) remains design-only,
not collected.
