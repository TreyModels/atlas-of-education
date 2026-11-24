# Codex wave — verification ledger (run-lead, 2026-11-24)

## Contract (from dashboard + Codex handoff; check on every branch)
1. PRE_REGISTRATION.md committed BEFORE runs/code; order verifiable in git log.
2. Every quoted number -> committed file + field (claims-to-source map).
3. No causal language ("causes", "causal effect", "proves", "drives" as verb) for observational results; "consistent with" only.
4. No "first"; "we are not aware" only with recorded search.
5. Data tiers labelled: observed / reconstructed / imputed (Codex: transition panel is reconstructed; EFR is reconstructed).
6. GPU runs: batch layout PINNED and LOGGED before running; seed+layout repeatable; batch change alters RNG streams.
7. Failed/negative runs preserved, not deleted.
8. No branch rewrites (no force-push/rebase of existing branches); new branches only.
9. No secrets in logs/messages.
10. No scope drift to 1,200-draw/100M-agent scale without a bounded pilot that is stable.

## Codex findings to check each task against (F01-F14)
- F01/F03: effective_fertility = expected SURVIVING children per woman, NOT TFR (births). Never call it TFR. AFG 1950: EFR 3.399 vs TFR 7.248; median |diff| 0.284 over 14,578 country-years.
- F02/F12: the 7% labour-demand figure is RETRACTED as evidence against a demand mechanism (wage/ag series start 1991; original bins 1991->1990; 0.917 of 108 takeoffs <=1990). No paper may repeat it as evidence; re-estimate in common windows if used.
- F04/F14: 91% / 31-forward are selected identifiable-case statistics; bounds 48.4-95.3% all-country; threshold sweep 65.4-70.4% (1.5) vs 95.8-97.0% (0.5); ties are weak inequalities, not reverses.
- F05: Q5 backcast uses donor data in the hidden target years; naive baseline is a 3-point transformed mean, not the 1990 level.
- F06: Q3 form race is a two-logistic sum, not UN model; bounds allow non-monotonicity; end-year selection uses held-out data.
- F07: "robust everywhere" is a significance-share rule, not a p-value; BY zero cannot be inferred from floor counts alone — must compute on all 272 sorted p-values per family.
- F08: minority simulation 85/100 is exploratory, not blind operating characteristics; +-3.6pp MC SE.
- F09: "unrelated" (failure to reject) is not evidence of no relationship; report intervals and common samples.
- F10: Gemini runbook drops rows before shifting; residualization omits current schooling; country FE compatible with no trends.
- F11: "development gradient / causal claim rejected" is too strong; use "associations consistent with common trends, anticipation and a schooling effect".
- F13: row shifts assume complete 5-year grid; 20-year terms standardized on different sample.

## Tasks / owners / branches
- task-43 Q1 mechanisms (gpu-dose) research/q1-mechanisms-2026-11-25
- task-44 Q2 pathways (panel-matrix) research/q2-pathways-2026-11-25
- task-45 Q3 multiverse calibration (multiverse-400) research/q3-multiverse-calibration-2026-11-25
- task-46 E1 multiverse R=1200 (cuda-scale) research/e1-multiverse-1200-2026-11-25
- task-47 E6+E8 sequencing repairs (un-data) research/e6e8-sequencing-2026-11-25
- task-48 E11 fertility audit (methods-paper) research/e11-fertility-audit-2026-11-25
- task-49 source verification (novelty-review) research/codex-source-verification-2026-11-25

## Expected numbers to recompute
- Q2 pair smoke: 105 baseline-complete, 52 disjoint pairs, 1 unpaired, 52 pairs with both 1990-2010 schooling and TFR changes; input sha256 cd30d7ea7beb77b63de092c53f9b143065b94651f1ac95535ac70eebb3280f2d.
- Synthetic: 5/5 tests; structured micro likelihood wins 200/200 effect, 200/200 selection, 0/200 common-trend (constructed demo, not power).
- E1/BH: full sorted p-values per family; the 0/35/44 story must be recomputed, not inherited.
- Fee-abolition dates: 12 dates; conflicts Cameroon 1999/2000, Ghana 1997/2005, Ethiopia 1994/1995, Tanzania 2001/2003, Malawi 1994/1995, Mozambique 2004/2005.

## VERIFIED STATUS (2026-11-24)
- task-43 Q1 mechanisms: VERIFIED @ 9b0cabe. Zero-signal control degenerate (MSE picks flexible 97.5% W1/W2; BIC picks parsimonious 100%); micro-gradient W3 42.5/62.5/62.5% but misattributes W1/W2; GPU gate: repeat 8.9e-16, layout diff 1.9074, pinned nW=12 seed 7; 50k women 2.994 s. Bounded.
- task-44 Q2 pathways: VERIFIED @ f71b789. Smoke exact 105/52/1/52; matching fragility fires (21.2/28.8/61.5/28.8% overlap); random yardstick null (schooling 0.82 vs 0.825, 52.4%; TFR 0.7715 vs 0.77275, 50.3%); farming 1991+ modelled, no backcasting.
- task-45 Q3 calibration: VERIFIED @ 075c8c3. Null FP 4.25% [2.67,6.70]; shared-trend 5.0%; minority 48.25%/87.0%/tag 42.0% [37.3,46.9]; grid 26.5%->55.5%; full BH/BY 35/19/15/53 with BY 0, m_eff 44. MINOR: REPORT ladder 19.2/60.5/95.8 and B_N80 27.5 vs calibration.json 19.0/60.0/95.0 and 26.5 - fix requested.
- task-46 E1 R=1200: VERIFIED @ 7e6f7b5. Wall 5426.9 s, 1200/1200; BH 35/19/15/53 -> 41/20/17/53 -> 41/23/20/53; BY 0 <=800, 32 het at 1200 (first rank 29, floor 32); repro400 exact counts + share diff 5e-7 + vintage t 3.97e-5; halves rank corr 0.9965, BH 34/38,21/23,15/21,53/51; localisation 1/5 robust, 20/32 BY het.
- methods paper: VERIFIED @ d7e8f9f (E1 record merged; R-dependence stated; no single BY-zero claim; contract pass).
- task-47 E6/E8: VERIFIED @ 2d19da7. 7% not re-derived/defended (retracted); E6 demand-first 10.0/15.4/24.1/18.8% with bounds; E8 CS post-effects t0 +12.4 [-2.4,27.2] ... t+6 +25.9 [8.6,43.2], TWFE similar, pre-trends flat, LOO 18.2-26.2; N3 54 defs, 0.0-30.8% median 10.45, q1 6.2/70.6/17.6.
- task-48 E11: VERIFIED @ e926575. EFR vs TFR different constructs (median |diff| 0.3042, AFG 3.399 vs 7.248; opposite lead/lag 0.541 vs 1.555); ladder 4/8 indeterminate, 5/7 does-not-discriminate; 8 Paper F text changes incl. F11 softening.
- task-49 source verification: VERIFIED @ 9a0fd69. 8 fee dates verified (4 unresolved, no guessing), conflict resolutions documented; demand series first years incl. NO pre-1990 wage employment (farm-employment share only); prior art 8/8/8 with DOI statuses; Codex unverified list marked.
- Q3 addendum db7814d: doc-only E1 cross-reference (BH 41/23/20/53 at 1200; BY 32 het, first rank 29) - VERIFIED.
- Paper F final ec899cc: E11 text changes in assembled draft; old overclaim phrases absent; construct note 0.3042 / 0.541 vs 1.555; no 68.75/69% - VERIFIED.
- FINAL HEADS: Q1 9b0cabe; Q2 f71b789; Q3 db7814d; E1 7e6f7b5; E6/E8 2d19da7; E11 e926575; source verification 9a0fd69; methods paper d7e8f9f; Paper F ec899cc.
