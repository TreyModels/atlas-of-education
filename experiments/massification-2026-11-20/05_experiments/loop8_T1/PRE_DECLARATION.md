# T1 PRE-DECLARATION — Korea spend decomposition (participation x hours x price/hour)

**Written before computation:** 20 Nov 2026, Lead (`lead-successor`). **Status:** authorised follow-on; programme
remains CLOSED (this is a descriptive decomposition of an official statistics table, not a re-fit and not a
country claim).

## Question

Korea's private-education **spend per student** rises from elementary to high school (+23.4%, 398k -> 491k won
per student) while **participation falls** (86.0 -> 75.4 -> 66.4%) and **hours/week fall slightly**
(7.5 -> 7.4 -> 6.7). Is the spend rise a **price per hour** phenomenon rather than a participation/arms-race
phenomenon? This is the test of the paper's one-margin "arms race" mechanism and of the two/three-margin rewrite
proposed in Council brief 011.

## Identity and units

- spend per student (level) = participation(level) x spend per participating student(level)
- spend per participating student = hours per month x price per hour
- hours per month = hours per week x 52/12 (= 4.3333), stated assumption: the survey's "hours per week" is a
  year-average weekly rate; if the survey measures term-time weeks only, the price level changes but the
  **comparison across levels** does not (the same multiplier applies to all three).
- source: MODS/KEDI Private Education Expenditures Survey 2023, English press release, Tables 2 and 9
  (on disk: 04_data/shadow_round2/data/shadow_incidence_round2.csv, shadow_fees_round2.csv).
- Derived spend per student by level = participation x spend-per-participant; the resulting 398/449/491 values
  reproduce the figures quoted in Council brief 011, which is a consistency check.

## Estimands

1. price per hour by level (won/hour, 2023), and its ratio high/elementary.
2. log decomposition of the spend-per-student change elementary->high into participation, hours, and price
   components.
3. the same for middle as a robustness point.

## Predeclared decision rule (binding)

- **Two/three-margin verdict** if price per hour rises **>= 20%** from elementary to high **while** participation
  and hours both fall (or are flat). Then the paper's one-margin "arms race participation" mechanism must be
  rewritten as participation x hours/price, and the Korea/HKG contrast is the paper's real empirical puzzle.
- **One-margin survives** if price per hour is flat (< 10% change); then the spend rise is participation/hours.
- **Indeterminate** if the movements are mixed or the derived spend-per-student values do not reproduce the
  quoted 398/449/491 within 1%.

## Scope and caveats (predeclared)

- Official national statistics, 2023 cross-section; no causal claim, no time-series claim.
- Participation and hours are among the relevant student population; spend per participant is the KEDI series.
- "Price per hour" is an average across provider types and subjects, not a market price for a homogeneous service.
- Korea only; nothing here transfers to another country.

## Reproduction

`05_experiments/loop8_T1/t1_korea.py` reads the two on-disk CSVs and writes `t1_inputs.csv`,
`t1_decomposition.csv`; `T1_FINDINGS.md` records the verdict and the arithmetic.
