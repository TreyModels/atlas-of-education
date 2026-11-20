> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# COUNCIL DELIBERATION 003 — FINAL adjudication

**Panel (AI composites, literature-based):** PATRINOS (education economics; steel-man), BRAY (shadow education,
mandatory), PAGE (model reasoning), CARTWRIGHT (philosophy of social science).
**Input:** `brief_003/BRIEF.md` (sha256 `88a2cf57…13e3`); artifacts read directly: `SUMMARY_FOR_TREY.md`,
`05_experiments/{runs/E13c, runs/E18b, runs/E21, EXPERIMENTS.md, SUMMARY_TABLE.csv}`,
`05b_experiments/{EXPERIMENTS_B.md, runs/B1, runs/B2_B3, runs/B4, runs/B5}`. Closing cycle; no further summons.

## Agreed

1. **F1 is signable only as one clean cell deep.** At σ=2 the rival's degree income is matched (2.706 vs 2.925) and
   its formal-probability response is −0.0054 (±0.0027) against surplus −0.1511 (±0.0217); at σ=0.5/1 the formal
   share is matched (0.279–0.280 vs 0.286) but income is not (11.388 and 1.457 vs 2.925). The sentence must say
   "no material fall (≤0.5 pp at σ=2, the fully matched cell)", never "does not fall at σ≤2".
2. **F2's "level artefact" framing is withdrawn.** B1's σ=0.5 income fall is real in point estimates (−0.109,
   −0.175; 2 sd; plausible baseline 0.234) but that corner is numerically unstable (baseline ratio 0.022–0.055;
   degree income 1.0–42.4 across seeds). The correct status is **unidentified at high substitutability**, and the
   corner must not be cited for either theory.
3. **C10's withdrawal stands; F3's positive phrasing does not.** E18b is a one-parameter linear damping
   (`ts` = 1 halves, 2 fully displaces at s=0.5 sd); ts=2 zeroes paid spend by construction. Cite C1 (ts=1;
   −1,291.5, 2sd 92.3) as the least constructed arm; label C2 (spend 0) and C4 (capacity 25%, ts=2) as best cases.
   The finding is "the sign is unidentified", not "substitution appears".
4. **F4 sentence** (BRAY): "In this model, a universal additive school-support module raises paid tutoring spend at
   high-stakes gates (+18%), while a module declared to damp tutoring's marginal value lowers it; the sign hinges on
   an unestimated substitution elasticity, so the effect of China's 2021 Double Reduction on paid tutoring is not
   identified here and is not a tested policy effect."
5. **F5 is still the strongest plank, restated:** floor level ≤ seed noise; floor *movement* and rank ordering carry
   intensification; the allocation knockout is mixed — only lottery-vs-rank is identified (cutoff+random +0.036, n.s.).
6. **F6 forces withdrawal of trajectory/projection claims.** B4: EXO 0.22→0.55 supplied; ENDO 0.404→0.020 with
   sd 0.384; smoothed 0.218→0.108. The generated path is unstable, not merely flat.
7. **F7:** PH levels roughly right (MAE 3.4/12.6/5.4 pp; bias +7.6 secondary) and shape not reproduced
   (−0.33/−0.40); uncalibrated; Korea preset never quoted (41.0 vs 93.7, corr 0.156). Defensible sentence: an
   uncalibrated accounting description, not a fitted reconstruction.
8. **F8:** keep the detailed-reader error advantage (0.045 vs 0.411; 10/10 signs); withdraw "certification demand
   rises with detail" (0.062 vs 0.217, contradicted); foreign-recognition sign is a declared parameter artifact.

## Disagreements preserved

**D1. PATRINOS vs the draft's F2 wording.** PATRINOS: B1 makes "artefact" untenable; the report should say
"unidentified". The draft's §2 says "level-matching revived the formal-access version" — true — but §1/F2's
"income contradiction was a level artefact" over-reads. CARTWRIGHT concurs and adds: do not use "artefact" as
exculpation; the corner is a numerical instability. *Resolution:* F2 amended to "unidentified corner".

**D2. PATRINOS vs BRAY — what is the strongest plank?** PATRINOS: the formal-access gap is the only
discriminating claim with an empirical test (Prediction 2 rewritten). BRAY: the floor/race decomposition is the
paper's real contribution, and China claims must not be in the headline. PAGE: both are model-class; rank neither
above the other. *Resolution:* two planks, ordered: (1) floor/race decomposition, (2) formal-access conditional;
tutoring/China appears only as an unidentified-parameter result.

**D3. The fairness of the formal-access margin.** PATRINOS (steel-man): the rival hires by productivity, so the
margin is partly definitional; it survives only as "rationed vs productivity hiring". CARTWRIGHT: that is a
capacity claim, conditional. BRAY: irrelevant to the credential/tutoring literature. *Resolution:* all agree it is a
model-class implication, never evidence that markets ration.

**D4. Sign-off mechanics.** The report must amend three summary sentences (σ≤2; "substitution appears";
"ranking, not the floor" without the mixed-knockout caveat), fix §7's stale "Finish E13c", and add the trajectory
withdrawal explicitly. CARTWRIGHT drafted the final claim and withdrawal list; all concur.

## Model contest (final)

| Composite's rendered model | Δ diploma formal probability after shock | Δ diploma income | Status |
|---|---|---|---|
| Surplus (slot-rationed, rank) | −15.1 pp (±2.2) | −5.8 pp (±1.8) | E13c, clean cell at σ=2 |
| Competitive CES, level-matched (steel-man) | −0.5 pp at σ=2; +0.9/+1.0 pp at σ=0.5/1 | +12.5 pp at σ=2 | survives on income only where levels unmatched; formal gap fails |
| Allocation knockout | lottery +0.151 vs rank −0.039/−0.064; cutoff+random +0.036 n.s. | — | mixed, not a clean knockout |
| Long-run generated path | — | ENDO entry 0.404→0.020 (sd 0.384) | requires supplied trend |

**Sign-off:** conditional, with the amendments above. Files: brief_003/{BRIEF,EXPERTS,REVIEWS,COUNCIL_DELIBERATION_003,SYNTHESIS_003}.
