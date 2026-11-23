# Methods paper H7 — third-round check (head c5dfe66): CLOSED

`novelty-review`, 24 November 2026. Re-read of `research/methods-multiverse-paper-2026-11-23` @ c5dfe66,
paper.md §6.2-§6.7, `scripts/dependence_analysis.py`, `results/dependence_analysis.json`.

## H7 is fixed, and fixed at the level of the code rather than the prose

- **Family = 272 links per procedure.** §6.2: "The family is defined throughout as the 272 directed links, with
  one trends-specification p-value per link: the committed analysis forms BH over `bh(p_up[J])`, where J selects
  the 272 trend-specification values out of the 544 edge specifications (`analyse400.py`)." §6.5 table column now
  says "family = 272 links per procedure".
- **Four separate procedures, not one joint 122-test family.** §6.2 and §6.3 state this explicitly; §6.3
  attributes 35 / 19 / 15 / 53 to the up, down, sign-flip and heterogeneity procedures respectively; the tier
  table repeats "four separate procedures, not one joint procedure". This resolves the 35-vs-122 ambiguity.
- **BY arithmetic per procedure.** §6.6: each procedure uses the same 272-link family, so each needs rank ≥ 84;
  the floor clusters are 30 (up), 19 (down), 15 (sign-flip), 53 (heterogeneity), all below 84 → **BY certifies
  zero in every one of the four procedures**. My independent arithmetic agrees (H_272 = 6.185, threshold
  2.972e-5, floor 2.494e-3, rank 84 required; next empirical p above the floor is 2/401 = 4.99e-3, well above
  the rank-84/85 thresholds, so no above-floor link can pass either).
- **The 68 reading is recorded, not adopted.** §6.6 says a hypothetical 68-link family would give BY = 35 with
  budgets 6,533/218/186, but "no 68-link family appears in the committed analysis". JSON
  `benjamini_yekutieli.hypothetical_per_direction_68` carries the same numbers and the label "NOT the committed
  family". Good — the ambiguity is now a documented alternative, not an unstated assumption.
- **JSON/script carry family metadata**: `family_size` 272, `family_members` (J = odd indices of 544 specs),
  `direction`, `per_procedure_by_zero` with floor clusters {up 30, down 19, flip 15, het 53}, `H_M` 6.1849,
  `certified` 0, `draws_needed` 33,646/1,122/962. Matches the text.

## Residual, optional (not a blocker)

`benjamini_yekutieli.per_procedure_by_zero.note` honestly says the down/flip/het null matrices were not saved
with the record, so those floor sizes are deductions rather than recomputations. The paper text (§6.3) says the
counts were reproduced with statsmodels, which is a separate implementation of the same p-values; a one-clause
footnote saying where the 19/15/53 floor counts come from would close the gap for a referee who wants to
recompute. Not needed for the claim, which now stands or falls on the up procedure where the committed matrix
exists.

## Verdict

H1-H6 verified earlier; H7 now closed. The dependence section is internally consistent: one family definition,
four procedures, per-procedure BY = 0, a three-way range 0/35/44, the anti-conservative M_eff sensitivity
labelled, the rule-of-three qualified, the 13,800-battery check named, and the 68-link reading recorded as
hypothetical. **Methods paper: SIGNED OFF at c5dfe66.**
