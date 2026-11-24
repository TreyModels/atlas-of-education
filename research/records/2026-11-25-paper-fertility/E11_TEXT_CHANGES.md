# E11 text changes applied to Paper F (audit `research/e11-fertility-audit-2026-11-25` @ `e926575`)

Applied 25 Nov 2026 to branch `research/paper-fertility-2026-11-25`. The audit's eight exact changes were applied
to the **build sources**, the draft was rebuilt with `build_paper.py`, and the assembled artefact was grepped.
Numbers were not changed; the 68.75%/69% ordering figure does not appear in Paper F and was not reintroduced.

| # | audit change | source fragment(s) edited | before → after (exact) |
|---|---|---|---|
| 1 | §1.2 heading (draft L86) | `draft/frame_intro_new.md` | "The gradient is a development gradient, not an identified schooling effect." → "The association is consistent with a common development gradient, with anticipation/quantity-quality, and with a schooling effect." |
| 2 | §1.2 paragraph (L88–91) | `draft/frame_intro_new.md` | "The pre-registered decision rule therefore fires: … cannot be read as the effect of changing schooling while holding development constant." → "The pre-registered decision rule fires: the level relation cannot be read as the effect of changing schooling. But the placebo does not identify a development gradient either. Future schooling at t+10 can move with parents' fertility plans at t (anticipation/quantity-quality), and a schooling effect with a long lag predicts the same pattern. The association is consistent with all three; this design cannot distinguish them or reject a schooling effect." |
| 3 | §1.3 (L106) | `draft/frame_intro_new.md` | "…so the descriptive claim survives while the causal one is rejected with evidence." → "…so the descriptive claim survives while no mechanism — common development trends, anticipation/quantity-quality, or a schooling effect — is identified or rejected." |
| 4 | §4.6 placebo conclusion (L590–596) | `sections/section1_levels_changes.md` | "…a development-gradient association and not an identified schooling effect — therefore fires. The levelled relation is descriptive…" → "…the level relation is not an identified schooling effect — therefore fires. The level relation is not an identified schooling effect, and it is not evidence for a pure development gradient either: common development trends, anticipation/quantity-quality, and a long-lag schooling effect all predict the same future-schooling pattern." |
| 5 | §4.6 (L601–604) | `sections/section1_levels_changes.md` | "it is what a development gradient looks like in a cross-section" → "it is what a development gradient — or anticipation, or a long-lag schooling effect — looks like in a cross-section" |
| 6 | §4.7 (L640) | `sections/section1_levels_changes.md` | "a quantified development-gradient caveat: the level relation is not an identified causal effect of schooling" → "a quantified caveat that the level relation is not an identified causal effect; the future-schooling placebo cannot distinguish a development gradient from anticipation or a long-lag schooling effect" |
| 7 | construct rule | `sections/section3_methods.md`, `sections/section4_transition.md` | Added: "effective fertility (surviving children per woman) and total fertility (births per woman) are different constructs; they are not interchangeable and neither corrects the other"; matched-sample numbers stated (median absolute difference 0.3042, maximum 4.2677; lead/lag 0.541 versus 1.555); "TFR" never used for effective fertility |
| 8 | cite E11 record where the placebo is discussed | `draft/frame_intro_new.md`, `sections/section1_levels_changes.md` | Added "(E11 fertility audit, `research/e11-fertility-audit-2026-11-25` @ `e926575`; change-on-change ladder returns 'does not discriminate')" |

## Consistency changes made alongside (same softening; no numbers touched)

- Abstract: "development-gradient association and not an identified schooling effect" → "consistent with a
  development gradient — or with anticipation or a long-lag schooling effect — but is not an identified schooling
  effect."
- Verdict table row 5: claim softened and graded **S (descriptive; mechanism not identified)**, with the E11
  "does not discriminate" note.
- §8.2: "signature of a shared development process rather than an identified effect of schooling" → "consistent
  with a shared development process, with anticipation/quantity-quality, or with a long-lag schooling effect; the
  design cannot distinguish them or reject a schooling effect."
- §8.4 conclusion: "what survives is a development gradient … what fails is the causal reading" → "what survives
  is a non-causal, global, between-country gradient … what is not identified is its mechanism — a development
  gradient, anticipation and a long-lag schooling effect remain observationally equivalent in this design."

## Grep of the assembled draft (post-rebuild)

Old phrases (all 0 hits): "The gradient is a development gradient, not an identified schooling effect";
"cannot be read as the effect of changing schooling while holding development constant"; "signature of a shared
development process"; "quantified development-gradient caveat"; "what fails is the causal reading of it"; "so the
level gradient is a development-gradient association".

New phrases present: audit heading (1); "this design cannot distinguish them or reject a schooling effect" (2,
including the abstract-adjacent §1.2 and §8.2 renderings); "it is not evidence for a pure development gradient
either" (1); "E11 fertility audit" (3); "0.3042" (1); "0.541 versus 1.555" (1); "does not discriminate" (3);
"observationally equivalent in this design" (1); "S (descriptive; mechanism not identified)" (1).
