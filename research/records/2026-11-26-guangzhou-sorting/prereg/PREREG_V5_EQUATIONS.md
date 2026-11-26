# Pre-registration v5: do the inventory equations hold in the Guangzhou system?

Written 2026-11-26 23:55 CST before running. Model `gz_v5.py` (v4 + insurance demand with peer escalation, art-exam
route, Hong Kong-status route); tests `eq_tests_v5.py`; 300 LHS draws, seed 20261130, n = 40,000. Unknowns swept:
tutoring effect POST_EFF 0-0.2 SD, take-up TERM_SHARE 0.02-0.15 / HOL_SHARE 0.2-0.6, INSURE 0-2, RHO_DEMAND 0-1,
ART_SHARE 0-6%, ART_BONUS 0.3-1.2 SD, HK_SHARE 0-2%, HK_BONUS 0.5-1.5 SD, plus all v4 ranges. ILLUSTRATIVE.

## Verdict rules (per equation, share of draws)
An equation **HOLDS** if its estimate is within the tolerance of the model truth in >= 80% of draws; **BIASED** if the
sign is right but the tolerance is missed in > 20% of draws; **MISLEADS** if the sign or the mechanism is wrong in > 20%.
- E74 tutoring-achievement (naive, and with prior score + SES): truth = POST_EFF x tutoring episodes for takers; tolerance +/- 0.05 SD.
- E76 SES x tutoring interaction: truth 0; MISLEADS if |t| > 2 in > 20% of draws.
- E58 participation logit on income: HOLDS if adding score and score-squared raises pseudo-R2 by < 0.01 in >= 80% (i.e. income alone is enough); otherwise the U-shape (both tails) is missed.
- E79 peer effect in tutoring demand: truth RHO_DEMAND; MISLEADS if the estimate is > 0.1 in > 20% of draws with RHO_DEMAND < 0.1 (spurious peer effect from class sorting), and report its rank correlation with the truth.
- E35, E159, E36, E152, E32, E34 as in v3 (school FE vs true VA within 0.1 SD; variance share vs VA share within 2x; peer coefficient vs PEER/(PEER+TOP_TEACH); RD vs true school VA within 0.1 SD; VA coefficient within 0.05; teacher-effect correlation >= 0.7).
- Descriptive: wealth gap at equal talent with vs without the art and Hong Kong routes; share of elite seats taken through those routes.
