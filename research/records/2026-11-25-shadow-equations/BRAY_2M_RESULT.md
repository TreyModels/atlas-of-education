# Bray reality check — 2,000,000-draw parallel ABC (26 Nov 2026, server)

Protocol unchanged from `bray_reality_check.py`; 64 workers on the 192-core-reported box (the
container is CPU-quota-capped at 15 cores, so the wall time reflects that cap, not 192 cores).

**Result: 95 of 2,000,000 prior draws fit all seven published Bray patterns (0.005%).**
Best fit max-z = **0.432** (all seven inside their tolerance bands):

| pattern | target | best fit |
|---|---|---|
| participation | 0.819 | 0.810 |
| participation, grade 9 | 0.747 | 0.764 |
| participation, grade 12 | 0.898 | 0.900 |
| urban–rural gap | 0.026 | 0.021 |
| own-provider share (among tutored) | 0.577 | 0.563 |
| other-provider share (among tutored) | 0.409 | 0.437 |
| teacher-tutor share | 0.540 | 0.556 |

Accepted parameter ranges (5th–95th pct of the 95 fits) are wide: b0 −1.41…1.40, b_income 0.09…1.97,
b_school_gap 0.21…2.77, grade12_bonus 0.36…1.88, urban_demand 0.06…0.81, teacher_threshold 0.39…0.52,
own_premium 0.17…2.65, other_premium 0.36…2.80, grade9_bonus −0.86…0.79, cost_other 0.19…1.80.

**Reading:** after adding the separate own-teacher and other-provider premiums and a grade-9 shift,
the demand equations *can* reproduce the seven observed Siem Reap patterns — but only in 0.005% of
the declared prior space, and the accepted ranges are wide, so the fit does not identify the
mechanisms. The earlier provider-share denominator bug (shares among all pupils instead of among
tutored pupils) was the main reason the first 200k-draw check found zero fits; after the fix and the
two extra channels, a narrow fitting region exists.

This is a simulation fit to seven aggregate patterns; it is not an empirical validation, not causal,
and it does not distinguish the rival explanations (the repo's earlier recovery test already showed
why). Next: literature verification of the added channels and a proper calibration/recovery test.
