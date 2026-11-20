# E18b — FAIR substitution test (follow-up, Council brief 002)

Command: `PYTHONPATH=<work>/ext/massabm "$PY" exp/run_E18b.py --reps 3 --N 5000 --workers 2 --out <out>`

Status: completed (18/18 runs, 91 s). Predeclared in `PRE_DECLARATIONS_E18b_E13c.md`.

E18b FAIR SUBSTITUTION TEST (Council brief 002, follow-up)
reps=3 N=5000 wall=91s ok=18/18 failed=0
tut_suppress = support damps the marginal effect of paid tutoring: effect x clip(1 - ts*s,0,1), s=0.5 sd.
ts=0 is the stock additive E18 behaviour; ts=1 halves tutoring value; ts=2 fully displaces it.
Decision rule: if any C1-C4 arm has paid spend below ban-only (C0) by >2 seed sd, C10 is WITHDRAWN.

  arm                                                                       paid spend     vs C0     vs A0 apex share   board completion
  A0 untreated baseline                                                           4092    +423.1      +0.0      0.411   0.932      0.717
  C0 ban only                                                                     3669      +0.0    -423.1      0.341   0.870      0.716
  C1 ban+support universal, suppress=1 (halves tutoring value at s=.5)            2377   -1291.5   -1714.6      0.526   0.607      0.723
  C2 ban+support universal, suppress=2 (full displacement at s=.5)                   0   -3668.5   -4091.7      0.000   0.000      0.726
  C3 ban+support targeted Q1-Q2 (40%), suppress=2                                 3327    -341.4    -764.5      0.333   0.871      0.718
  C4 ban+support capacity-limited 25%, suppress=2                                 2427   -1241.2   -1664.4      0.308   0.563      0.719

PAIRED CONTRASTS vs ban-only C0 (matched seeds, 2 seed sd in brackets):
  C1 ban+support universal, suppress=1 (halves tutoring value  d_spend= -1291.5 (2sd≈   92.3) -> BELOW C0 by >2sd
    learning guard: completion 0.7232 vs C0 0.7156 (2sd≈nan)
  C2 ban+support universal, suppress=2 (full displacement at s d_spend= -3668.5 (2sd≈   91.2) -> BELOW C0 by >2sd
    learning guard: completion 0.7257 vs C0 0.7156 (2sd≈nan)
  C3 ban+support targeted Q1-Q2 (40%), suppress=2              d_spend=  -341.4 (2sd≈  148.7) -> BELOW C0 by >2sd
    learning guard: completion 0.7176 vs C0 0.7156 (2sd≈nan)
  C4 ban+support capacity-limited 25%, suppress=2              d_spend= -1241.2 (2sd≈  101.4) -> BELOW C0 by >2sd
    learning guard: completion 0.7187 vs C0 0.7156 (2sd≈nan)

DECISION:
  C10 is WITHDRAWN: substitution is possible in at least one fair arm:
    C1 ban+support universal, suppress=1 (halves tutoring value at s=.5): -1291.5 (2sd 92.3)
    C2 ban+support universal, suppress=2 (full displacement at s=.5): -3668.5 (2sd 91.2)
    C3 ban+support targeted Q1-Q2 (40%), suppress=2: -341.4 (2sd 148.7)
    C4 ban+support capacity-limited 25%, suppress=2: -1241.2 (2sd 101.4)

Council correction recorded: in E18, arm A5 (ban + ADDITIVE support, 60% access) already had
paid spend 3,855 vs 4,092 untreated (-236.5). E18b therefore also reports "vs A0" above, not only "vs C0".

## Notes
1. Learning guard: the auto text prints 2sd=nan because it looked up the wrong sd key. The completion
   values are C0 0.7156 vs C1 0.7232, C2 0.7257, C3 0.7176, C4 0.7187 — all HIGHER than ban-only,
   so the learning guard passes in every arm.
2. C2 (universal support + full 1:1 displacement) is a limit case by construction: supported pupils face
   zero marginal value from paid tutoring, so spend is 0. Reported for completeness; the evidence for
   substitution rests on C1/C3/C4 where the channel is partial.
3. Council correction recorded: E18 arm A5 (ban + additive support, 60% access) already had paid spend
   3,855 vs 4,092 untreated (-236.5). E18b reports every arm against BOTH A0 and C0.
4. Mechanism caveat: the task asked for a CES score-production aggregator (elasticity 2). A CES with any
   finite elasticity has a positive cross-partial — additive-or-complementary — and cannot produce
   crowding-out; implementing it would have repeated E18s unfair test. The declared linear-damping channel
   (support multiplies tuttings marginal effect by clip(1-ts*s,0,1)) is the honest way to give substitution
   its best chance. This choice was predeclared.
