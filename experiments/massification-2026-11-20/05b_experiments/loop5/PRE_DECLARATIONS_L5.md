# PRE-DECLARATIONS — Loop 5: E1 gate-architecture gradient, E1b KOR no-fit benchmark, E4 income gradient

Written BEFORE any loop-5 run. Scope `05b_experiments/loop5/`. Workers ≤ 2 (numpy-only),
`PYTHONDONTWRITEBYTECODE=1`, matched seeds, 0 failed cells reported, no unrun cell claimed. All numbers
are stylized model output; only observed data cells are compared; no imputed cell used.
**Relation slots are PENDING** — `09_relations/` exists but its slot tables are not part of this batch;
no relation-slot claim is made.

Sources read first: `08_council/brief_007/SYNTHESIS_007.md`, `05b_experiments/loop4/U4_VERDICT.md`,
`02_lit/COUNTRY_CARDS/{KOR,HKG}.md`. Gate dates from the cards: **KOR** — CSAT (Suneung) for university
admission, endogenous admission cutoffs, high-school equalisation (card §2; CSAT operation from **1994**
is an ASSUMED date, not independently verified in the card). **HKG** — HKDSE first cohort **2012**
(single terminal norm-referenced exam, replaced HKCEE+HKALE), JUPAS centralised admission, SSPA at
primary→secondary transition (card §2; card itself says dates not independently verified → ASSUMED).

## E1 — gate-architecture gradient

**Question.** Can a model in which households buy tutoring in proportion to the stakes of the *binding
gate* reproduce BOTH observed stage gradients: Korean official 2023 **86.0 / 75.4 / 66.4** (falling) and
Hong Kong Bray & Kwok 2003 **35.1 / 46.6 / 70.3** (rising) — with gate parameters set from policy dates
and **no take-up fitting**?

**Structural variable and arms (declared orderings, fixed before running).** The binding-gate stakes
vector by stage is the only experimental variable:
- (a) **terminal-only**: stakes rise sharply at the final stage `[0.30, 0.50, 1.50]`;
- (b) **gate each transition**: early binding gates `[1.20, 0.90, 0.60]`;
- (c) **continuous curriculum**: flat `[0.80, 0.80, 0.80]`.
**Policy-dated assignment (declared):** KOR = (b) gate-each-transition (CSAT terminal + high-school
equalisation + continuous school-record/admissions competition; KOR card §2) — this is the arm predicted
to invert the gradient; HKG = (a) terminal-only (single HKDSE from 2012; in 1998/99 HKCEE+HKCALE are both
terminal summer exams; HKG card §2) — predicted to concentrate demand at the top. All three arms are run
for both countries for transparency; the pass criterion uses the policy-dated assignment.
**Structural parameters frozen** from the loop-4 uncalibrated KOR/HK configs (income, public-school
substitute, provider costs, capacity, teacher capacity, enrolment shares). **No demand-intercept
calibration and no take-up fitting** — the only difference across arms is the gate-stakes vector.
**Estimand.** Six stage take-up rates: KOR (elementary, middle, high) and HKG (S1-3, S4-5, S6-7).
**Threshold (predeclared).** PASS iff **all six** rates are within **±5 pp** of the observed values under
the policy-dated assignment; otherwise **FAIL** and the gate-position story is dropped, not re-fitted.
**Prediction before running.** Shape may come out right but levels are unlikely to be within ±5 pp with
frozen structural parameters → expected FAIL or partial (shape-only).

## E1b — KOR no-fit benchmark (single-country rescue)

**Design.** Frozen structural parameters from the uncalibrated baseline (no take-up fitting). Fit **only
fee parameters** to the Korean fee moments: three stage fee multipliers (elementary/middle/high) are
fitted to the official by-level annual spend/GDP-pc ratios **11.5% / 14.9% / 18.4%** (462/596/740k won
× 12 / (36,238.6 US$ × 1,330 KRW/USD)). The overall moments (10.8% per student; 13.8% per participant,
434/553k won) are then **checks**, not fitted. KOR gate architecture fixed from the policy date: (b)
gate-each-transition (KOR card §2).
**Estimand and threshold (predeclared).** One-country incidence claim restored for Korea iff **all three
reported stages 86.0 / 75.4 / 66.4 are within ±5 pp** AND the direction checks hold: (i) provider
direction — model commercial provider share ≥ 50% (observed hagwon = 241/434 = 55.5% of expenditure);
(ii) hours direction — model participation falls with stage while fitted spend rises with stage (observed
7.5/7.4/6.7 h and 462/596/740k). Hours level (7.3 h/wk) remains **UNABLE** (no hours object) and is not
used as a pass condition. Otherwise the stop-rule stands permanently. Passing does NOT rescue
cross-country incidence; KHM/PH transfer remains out-of-sample and is expected to fail (reported as such).
**Prediction before running.** Fitting three fee multipliers to three spend ratios reproduces the fee
gradient by construction; whether participation levels land within ±5 pp is the open question. Expect
partial: direction checks likely pass, level threshold uncertain.

## E4 — income gradient (only if E1/E1b finish in time)

**Question.** Does the model reproduce the Korean spend gradient across income bands
**183k won (<3m won) < … < 671k (≥8m won)** (ratio 3.67)?
**Design.** KOR config (frozen structural params); five declared household income bands with income
multipliers `[0.50, 0.75, 1.00, 1.40, 2.00]` relative to the mean (declared from the band midpoints,
not fitted). Model spend per student = price × participation by band; estimand = spend(top) /
spend(bottom) and monotonicity.
**Threshold (predeclared).** PASS iff the model spend gradient is monotone increasing with income AND
the top/bottom spend ratio lies inside **3.67 × [0.5, 1.5] = [1.84, 5.51]** (±50% relative band);
otherwise FAIL. HKG income share 1.1–5.0% noted as a check only if a dated HK config is available
(not fitted).
**Prediction before running.** Income enters demand only through log-income and price/income, so the
gradient is likely too flat (ratio near 1.3–1.8) → expected FAIL.

## Failure / reporting rules

Any failed cell is logged and excluded with counts. Cells not executed are marked `not run`. Every UNABLE
is named (hours level; KHM/PH transfer). No threshold is changed after seeing results.
