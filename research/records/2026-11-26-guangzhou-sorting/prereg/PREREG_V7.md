# Pre-registration v7: second-review analyses (2026-11-27 00:30 CST, before running)
Model gz_v5.py (v5.1, band-size fix), script run_factorial.py, 150 LHS draws over the v5 ranges, seed 20261202, n = 30,000.
1. 2^4 factorial over BAN (pre-gate ban reach), BOARD (boarding), REBAND (senior-2 re-banding), SUBST (holiday tutoring,
   full-time institutions, art and Hong Kong routes). Shapley decomposition of the change from all-off to all-on in T, S,
   unconditional ratio U and household tutoring spend (cumulative per pupil over junior 1-3 and senior 1-2).
2. S*: richer/poorer elite-university ratio holding both zhongkao score (5 bands) and talent (5 bands) fixed, standardised
   to the pooled cell mix. Pre-stated reading: if S < 1 but S* is about 1, the favourable same-score result for poorer
   pupils is a composition (collider) effect; if S* < 1 too, it reflects treatment after admission.
3. Interventions at the current setting: HOME = 0, TEACH_ZONE = 0, PRE_EFF = 0, all three, and no art/HK routes.
No pass/fail thresholds: these are decompositions to replace the additive reading of ratio differences.
