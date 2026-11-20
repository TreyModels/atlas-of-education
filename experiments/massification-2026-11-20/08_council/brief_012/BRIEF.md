> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# BRIEF 012 — ADVERSARIAL READ OF THE T1 KOREA DECOMPOSITION

- **sent by / date:** lead-successor, 2026-11-20 ~14:25 Asia/Shanghai (task-32; advisory; **programme stays CLOSED**).
- **object:** `05_experiments/loop8_T1/` — predeclared decomposition of Korea's private-education spend by school
  level (MODS/KEDI 2023). Result reported: implied price/hour 14,215 → 18,586 → 25,488 won/h (+79.3% elementary→high)
  while participation falls 86.0 → 66.4% and hours/week fall 7.5 → 6.7; log decomposition price +0.584,
  participation −0.259, hours −0.113, residual 0. Predeclared rule fired ⇒ two/three-margin.
- **purpose:** adversarial audit of the arithmetic/identity, the inference, the strongest objection, a verdict on
  whether T1 forces the paper's rewrite or only flags it, exact permissible paper language, and 2–3 measurement
  steps. T2 (legitimation vignette) is **design-only, not collected**.

## 1. Inputs read on disk

| Artifact | Content |
|---|---|
| `05_experiments/loop8_T1/PRE_DECLARATION.md` | identity, units, 52/12 conversion assumption, decision rule (two/three-margin if price/hour ≥ +20% while participation and hours both fall/flat), scope caveats |
| `05_experiments/loop8_T1/T1_FINDINGS.md` | table and log decomposition; verdict TWO/THREE-MARGIN |
| `05_experiments/loop8_T1/t1_inputs.csv` | elementary/middle/high: participation, hours/week, spend/participant (462/596/740k), derived spend/student (397.3/449.4/491.4k), hours/month, price (14,215/18,586/25,488) |
| `05_experiments/loop8_T1/t1_decomposition.csv`, `t1_summary.json` | dln_spend 0.2124, participation −0.2587, hours −0.1128, price +0.5839, residual 0; price ratio 1.793; consistency checks 0.17/0.09/0.07% |
| `04_data/shadow_round2/data/shadow_incidence_round2.csv` | KOR participation 86.0/75.4/66.4; hours/week 7.5/7.4/6.7 (Table 2); denominator column says **"students"** for hours, "elementary-school students" for participation |
| `04_data/shadow_round2/data/shadow_fees_round2.csv` | KOR spend per participating student 462/596/740k (Summary text); per student 434k all; provider spend (general subjects): hagwon 241, 1:1 37, group 22, internet 16, textbook 11; income gradient 183 vs 671k |
| `08_council/brief_010/SYNTHESIS_010.md`, `brief_011/SYNTHESIS_011.md` | T1 originated here (T1 = Korea decomposition); paper rewrite requirement |

## 2. Questions (task-32, 1–6)

1. **Arithmetic/identity audit:** is spend/student = participation × hours × price correctly read from KEDI tables?
   Is 52/12 defensible? Same population? Double counting (e.g. spend per participant including non-participants)?
2. **Inference audit:** does +79% mean price escalation, or composition (subject mix, provider type, academic vs
   vocational high school, hagwon vs 1:1), quality, or hours mis-measurement? List alternative decompositions to run
   before the paper uses it.
3. **Strongest objection** to the two/three-margin rewrite, and what evidence would answer it.
4. **Verdict:** does T1 force the rewrite (as the paper's own mechanism claim) or only flag it? Give exact paper
   language.
5. **2–3 measurement steps** (data, cost) to settle composition; T2 marked design-only.
6. **Dissent** recorded.

## 3. Rules

On-disk evidence only; numbers cited to file/row; no fabrication; T1 is descriptive, not causal; programme stays
CLOSED (no stop-rule reopening).
