# PRE-REGISTRATION — E11 change-on-change placebo ladder + Q2 construct reconciliation

Record `research/records/2026-11-25-e11-fertility-audit/`, branch `research/e11-fertility-audit-2026-11-25`,
based on `origin/research/assessment-and-next-experiments-2026-11-24`. Author `methods-paper`, 25 Nov 2026.

**This file is committed before any script is written or run.** It fixes the questions, data, specifications,
decision rules, interpretation limits and output files. Deviations are recorded in `REPORT.md`; failure to
complete a step is reported, not hidden. No credentials, no branch rewrites, no causal language.

---

## 0. Why this job exists

Codex's independent review (`research/records/2026-11-24-codex-review/REVIEW.md`, findings F01/F03/F11) found:

- **F01/F03 — a construct error.** The transition record's `effective_fertility` is *children per woman expected
  to survive to childbearing age* (a surviving-children measure), while `tfr_observed_1950plus` is the total
  fertility rate — *births per woman* (UN WPP 2024, 1950+). They are different constructs, not the same series
  with an unexplained discrepancy. Codex: AFG 1950 effective fertility 3.399066 vs TFR 7.248; median |difference|
  0.283536 over 14,578 overlapping post-1950 country-years, maximum 4.489685.
- **F11 — an overclaim.** Paper F's draft calls the schooling–fertility relation a "development gradient" and
  says the "causal claim [is] rejected", which the lead/lag test cannot support: common development trends,
  anticipation/quantity-quality, and a schooling effect all predict the same lead-term pattern.

Sonnet's Step 3 / E11 asks for a change-on-change placebo ladder on the 23 Nov battery panel. This record does
that, reconciles the two fertility constructs, and lists the exact Paper F text changes.

---

## 1. Data (fixed)

All data are public and already on the box or restored there; no imputation, no interpolation.

| Source | File | Role | Data tier |
|---|---|---|---|
| Transition record `research/transition-2026-11-23` | `research/records/2026-11-23-transition/data/long_run_panel.csv` | long-run panel, 1750-2024, 5-year grid; columns `effective_fertility`, `tfr_observed_1950plus`, `tfr_implied_derived`, `mean_years_schooling`, child mortality, life expectancy | **reconstructed pre-1950** (OWID/Gapminder); post-1950 TFR observed (UN WPP 2024) |
| Project panel | `/root/work/data/*.json` (68 WDI/macro series; 1960-2024; no imputation) | 6 project schooling indicators + `fertility` (births per woman) + income + urbanisation | observed |
| OWID grapher exports (corr-rebuild URLs) | `mean-years-of-schooling.csv` (total), `average-years-of-schooling-males-vs-females.csv` (female) | add 2 schooling indicators to reach 8 | observed/reconstructed (OWID/Barro-Lee-Lee) |

- **8 schooling indicators (S):** mean years total (OWID), mean years female (OWID), secondary enrolment
  (`sec`), lower-secondary completion (`lsc`), primary completion (`prm_cmp`), tertiary enrolment (`ter`),
  gender parity secondary (`gpi_sec`), gender parity tertiary (`gpi_ter`).
- **Fertility outcome for E11 (F):** project panel `fertility` — births per woman (TFR-type). This is *not* the
  transition record's effective-fertility series; the construct is stated in every table.
- **Controls:** log income per head and urbanisation (project panel), both standard.
- **Grid:** 5-year years, 1960-2014 (so t+10 and t+20 terms exist), country-year panel.
- If the OWID download fails on the box, fall back to the transition panel's `mean_years_schooling` for total
  mean years and run 7 indicators; record the failure and do not silently substitute.

## 2. Construct audit (Q1) — fixed method

**Definitions, quoted from the committed sources** (transition.py header and OWID metadata):
- `effective_fertility` = "children per woman expected to survive to childbearing age" (OWID / Malani & Jacob,
  1751-2023; reconstructed before 1950).
- `tfr_observed_1950plus` = total fertility rate = "the average number of children a woman would have if she
  experienced the year's age-specific birth rates throughout her childbearing years"; unit "live births per
  woman" (UN WPP 2024; 1950-2023).
- `tfr_implied_derived` = effective fertility / survival approximation, survival ≈ 1 − 1.10 × child
  mortality/100; derived, never used for a claim.

**Q1 specifications (all on matched samples — same countries, years, rows for both outcomes):**
1. **Descriptive:** overlap count, median |difference|, maximum |difference|, correlation in levels and in
   ten-year changes, ratio of means; AFG 1950 spot check; coverage by period.
2. **Level ladder, both outcomes, identical sample:** F(t) on S(t−10), S(t), S(t+10), each schooling lag
   standardised within the estimation sample; country FE + year FE; country-clustered SEs; controls income and
   urbanisation; sample 1950-2010 5-year grid restricted to rows where *both* EFR and observed TFR exist.
   (This is the Q2 design, re-run for both outcomes on the same rows.)
3. **Change-direction test, both outcomes, identical sample:** dF(t,t+10) on dS(t−10,t), dS(t,t+10),
   dS(t+10,t+20), all standardised in-sample, country FE, country-clustered SEs; and the reverse
   dS(t,t+10) on dF(t−10,t), dF(t,t+10), dF(t+10,t+20). Report both fertility outcomes.

**Decision rule (pre-registered):** report both outcomes side by side; never pool them; never call effective
fertility "TFR" or vice versa. If the lead/lag patterns differ, the conclusion is that the two outcomes answer
different questions (surviving children versus births) and neither is a correction of the other. The
`tfr_implied_derived` series is not tested.

## 3. E11 change-on-change placebo ladder (Q2) — fixed design

For each of the 8 schooling indicators, on the E11 panel, country-clustered SEs throughout, controls log income
and urbanisation, estimation samples listwise-complete within indicator (n and countries reported):

**A. Levels ladder (outcome F(t)):**
- A0 `F(t) ~ S(t)` — current.
- A1 `F(t) ~ S(t+10)` — **future-schooling placebo**.
- A2 `F(t) ~ S(t) + S(t+10)` — both; the lead/lag comparison.
- A3 `F(t) ~ S(t−10)` — lagged (past).
- A4 `F(t) ~ dS(t+10, t+20)` — **frozen/future-change placebo** (future change in schooling).
FE: country + decade. With and without a country-specific linear trend.

**B. Change ladder (outcome dF(t,t+10)):**
- B0 `dF(t,t+10) ~ dS(t−10,t)` — past change (lag term).
- B1 `dF(t,t+10) ~ dS(t,t+10)` — concurrent change.
- B2 `dF(t,t+10) ~ dS(t+10,t+20)` — **future-schooling placebo** (lead term).
- B3 all three together.
FE: country. With and without country trends.

**C. Reverse change ladder (outcome dS(t,t+10)) — the future-fertility placebo:**
- C0 `dS(t,t+10) ~ dF(t−10,t)`; C1 `~ dF(t,t+10)`; C2 `~ dF(t+10,t+20)`; C3 all three.
FE: country. With and without country trends.

Reported per indicator: coefficient, SE, 95% CI, n, countries, and the **lead/lag ratio** (future term ÷ lag
term) for A2 and B3. A compact table gives every indicator × every ladder step.

**Pre-registered decision rule (from Sonnet NEXT_EXPERIMENTS E11, adopted unchanged):**
- If the lead term (`S(t+10)` or `dS(t+10,t+20)`) is **at least 80% of the lag term in more than half of the
  indicators**, the paper says the link **"does not discriminate between a common development gradient,
  anticipation/quantity-quality, and a schooling effect"** (not "co-trending", not "causal").
- If the lag term is **at least twice the lead term in more than half of the indicators**, say **"temporal
  asymmetry present; the causal reading is still untested"**.
- Otherwise: **"the ladder is indeterminate"**.
The reverse ladder (C) is reported alongside; it is the sign of the quantity-quality/anticipation channel, not a
test that can confirm it.

**Interpretation limit, fixed before results:** a future-schooling term that is as strong as the current term is
*consistent with* (i) a common development gradient, (ii) anticipation/quantity-quality (parents' fertility and
expectations at t affect children's schooling within a decade), and (iii) a schooling effect that operates with
a long lag. The design cannot distinguish these. It also cannot "reject" a schooling effect. No causal language
in any output.

## 4. Required Paper F text changes (Q3) — fixed list

Codex F11. The draft (`research/records/2026-11-25-paper-fertility/draft/paperF_draft.md`, branch
`fix/fertility-text-2026-11-24`) currently says the relationship is a "development gradient" and that the causal
claim is "rejected". Required replacements (exact wording to be listed in `REPORT.md` with draft line numbers):

1. Replace "development gradient" as a *finding* with: "the association is consistent with a common development
   gradient, with anticipation/quantity-quality, and with a schooling effect".
2. Replace "causal claim rejected" with: "the lead/lag design cannot distinguish these mechanisms and does not
   reject a schooling effect".
3. Any sentence that calls effective fertility "total fertility" or "TFR" must name the construct: "effective
   fertility (surviving children per woman)".
4. Any claim that one fertility series "corrects" or "explains the discrepancy" in the other is removed; the two
   answer different questions.
5. The ladder table (this record) must be cited where the draft says the placebo "works" or "fails".

## 5. Outputs and provenance

`scripts/q1_construct_audit.py`, `scripts/e11_ladder.py`; `results/q1_construct_audit.txt/.json`,
`results/e11_ladder.txt/.json`, `results/e11_ladder.csv`; `REPORT.md`; this file.
Every number in the report is traced to a committed file and field in `REPORT.md`; the run records the git commit
of this branch, input file hashes, seeds (none used), runtime, and the failed steps (if any). Raw data are on the
box; small results and scripts are committed. The long-run panel is reconstructed data and is labelled as such.
Run on `ssh autodl3` (8 cores), repo `/root/work/repo`, data `/root/work/data`; scripts are CPU-only and run in
minutes.
