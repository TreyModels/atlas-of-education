# Negative-results integration — Paper M (24 November 2026, task-37)

**Branch:** new additive branch `research/paper-massification-negatives-2026-11-24` from the verified head
`research/paper-massification-2026-11-25` @ `fb9f419`; no branch rewrite. **Draft after integration:** 18,809 words
(was 17,968; README flags the ~4.5% overage against the 12,000–18,000 target).
| source | branch @ commit | record file(s) |
|---|---|---|
| staging audit (task-26) | `research/masseng-timing-audit-2026-11-24` @ `ff84e75` | `research/records/2026-11-24-masseng-timing-audit/STAGING_AUDIT_AND_MASSENG_INVENTORY.md` (A2, A4, A5, PART D) |
| X1/X3 (task-27) | `research/masseng-staging-x1-2026-11-24` @ `fef7428` | `research/records/2026-11-24-masseng-staging-x1/RUN_REPORT.md`; `results_x1_EXPLORATORY_corrected.json`, `results_x3_EXPLORATORY.json` |
| X2/X4 (task-28) | `research/masseng-staging-x2-2026-11-24` @ `f592bae` | `research/records/2026-11-24-masseng-staging-x2/RUN_REPORT.md`; `results_x2_EXPLORATORY.json`, `results_x4.json` |
| X5 (task-29) | `research/masseng-bayes-audit-2026-11-24` @ `0ecd4be` | `research/records/2026-11-24-masseng-bayes-audit/AUDIT.md` (addendum §1–2) |

## Findings integrated (all labels preserved)

| result | label | headline numbers |
|---|---|---|
| staging audit (task-26) | audit of a **synthetic** staging experiment | arms not exposure-matched: `school_first` vs `jobs_first` differ by +1.8 education-share-years / −1.2 vacancy-years by construction; fiscal loop gives `jobs_first` higher mean education budget (41,818 vs 38,183, +9.5%); completion contrasts ≤0.6pp, 3–4/13 sign-stable; 5–7 distinct schedule orderings across seeds |
| X1 (task-27) | **synthetic toy worlds**, pre-registered; no causal/empirical claim | unmatched formal-share gap −5.4…−4.8pp (sign-stable) collapses under equal exposure totals (18.36 edu-share-years / 9.44 vacancy-years) to −0.13…+0.56pp = 2–12% of unmatched (**88–98% removed**); completion/equity not material; +10-year placebo −6.2…−7.6pp |
| X3 (task-27) | **synthetic**, 800 runs | zero sign reversals across `job_elasticity` 0–1; sequencing contrast NULL on 9–11/13 metrics; only mechanically exposed formal share robust; both-early-vs-neither robust 10–13/13 |
| X4 (task-28) | **observed aggregates, exploratory**; no causal claim | honest 40/21 train/validation split: model MAE 8.81 vs persistence 11.30, pooled trend 9.48; paired MAE −2.49 [−5.76,+0.77], −0.67 [−2.04,+0.66]; ordering coefficient −2.05 [−4.44,+0.87]; all 4 robustness specs FAIL_NO_EVIDENCE |
| X5 (task-29) | **conditional importance weights, NOT posteriors** | main ESS 88.75/4,096 (2.17%), expanded 20.64/4,096 (0.50%); prior-dominated; synthetic recovery confusion diagonal 50% (<60% criterion), error ≤15% in 56.25% (<60%); not usable as posterior-style inference |
| X2 (task-28) | **synthetic** toy worlds | quota gates raise gate-prep tutoring +17.6…+21.1pp (gate-adjacent +23.8…+28.9pp); top-bottom tutoring gap +13.0…+14.5pp; rural-access hypothesis falsified opposite (+7.9pp bar / +9.4pp quota); quota caps completion (lower −11.7…−12.3pp, upper −13.5…−14.5pp) |

## Disposition in `paper.md`

- **Abstract:** one sentence reporting the forward tests as negative results.
- **New §7.8 "What the project's own simulations found: negative results":** staging audit confound, X1, X3, X4,
  X5 and X2 bullets; consequence paragraph.
- **§12.3:** gate-design caution from X2 (credential risk).
- **§14.1:** new synthesis point 7; **§14.2:** new "Forward tests" box bullet.
- **§15:** new objection 13 ("the project's own simulations do not support the staging mechanism").
- **§16:** conclusion sentence.
- **README:** new negative-results integration section; word-count line updated; claims map row 37 added.

**Binding labels.** X1/X2/X3 are simulations on stipulated `eduengine` worlds, not fitted to any country and not
evidence about any real system. X4 is an exploratory aggregate test on observed series with thin constructs (no
child-work/tutoring/learning data). X5 is not a posterior. The staging audit is an audit of a synthetic experiment.
No server compute was performed for this integration; every number above is taken from the committed records named
in the table. No existing branch was rewritten.
