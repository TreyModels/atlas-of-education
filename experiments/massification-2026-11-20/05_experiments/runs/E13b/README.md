# E13b — Matched-elasticity rival for the graduate-supply shock (Council priority)

Command: `PYTHONPATH=<work>/ext/massabm "$PY" exp/run_E13b.py --reps 6 --N 5000 --workers 2 --out <out>`

Both worlds have a formal/informal margin, the same households, the same 1995 tuition shock and the
SAME formal vacancy path. Surplus = credential floors + rank. Rival = CES skill prices with
sigma in {0.5, 1, 2}, hiring by expected productivity, no credential floor.

E13b MATCHED-ELASTICITY RIVAL FOR THE GRADUATE-SUPPLY SHOCK (Council priority)
reps=6 N=5000 wall=282s ok=72/72 failed=0
Same households, same 1995 tuition shock, SAME formal vacancy path. Surplus world hires by
credential floor + rank; rival uses CES skill prices with sigma in {0.5,1,2} and hires by
expected productivity (no credential floor). Both have a formal/informal margin.

  world                                  sigma shock                                d dip inc     d formal|dip   d ratio
  surplus (slots+floors+rank)              0.0 college half price from 1995       -0.0606(0.019)      -0.1542(0.024)   +0.0470
  surplus (slots+floors+rank)              0.0 college 80% off from 1995          -0.0424(0.015)      -0.1683(0.021)   +0.0783
  competitive CES + slots (matched rival)   0.5 college half price from 1995       -0.0591(0.059)      +0.0174(0.025)   +0.2969
  competitive CES + slots (matched rival)   0.5 college 80% off from 1995          -0.0149(0.142)      +0.0079(0.026)   +0.0807
  competitive CES + slots (matched rival)   1.0 college half price from 1995       -0.0338(0.021)      +0.0242(0.017)   -0.1445
  competitive CES + slots (matched rival)   1.0 college 80% off from 1995          -0.0315(0.019)      +0.0101(0.029)   -0.1804
  competitive CES + slots (matched rival)   2.0 college half price from 1995       +0.0420(0.004)      -0.0057(0.003)   +0.0876
  competitive CES + slots (matched rival)   2.0 college 80% off from 1995          +0.0697(0.008)      -0.0146(0.004)   +0.1563

PREDECLARED DECISION RULE (Council): rival contradicts C3 if at ANY sigma the rival reproduces a
fall in diploma holders' absolute income (delta <= 0).
  VIOLATION at sigma=0.5: Δdip income=-0.0591 (±0.0592), Δformal|dip=+0.0174
  VIOLATION at sigma=0.5: Δdip income=-0.0149 (±0.1417), Δformal|dip=+0.0079
  VIOLATION at sigma=1.0: Δdip income=-0.0338 (±0.0206), Δformal|dip=+0.0242
  VIOLATION at sigma=1.0: Δdip income=-0.0315 (±0.0186), Δformal|dip=+0.0101
  -> C3 (the competitive world cannot reproduce diploma-holder losses) is CONTRADICTED.

## Reading the verdict honestly
The predeclared rule fires on point estimates: at sigma=0.5 and sigma=1 the rival's change in
diploma holders' absolute income is <= 0, so C3's sharp version ('only the surplus account can
make diploma holders lose') is contradicted. Precision caveat: at sigma=0.5 the seed dispersion
is large (2*sd 0.12-0.28), so those negative points are not distinguishable from zero; at sigma=1
the negative is about -1.6 seed sd (also under a 2-sd bar); at sigma=2 the rival clearly produces
GAINS (+0.042, +0.070). What discriminates cleanly is the formal-employment probability: it falls
only in the surplus world (-0.154, -0.168) and does not fall at any sigma in the rival
(+0.017, +0.024, -0.006, -0.015). So the defensible claim is about the formal-employment margin,
not about absolute income.

## Correction / authoritative-numbers note (Council brief 002)
The Council's level figures are CONFIRMED against the 6-rep `e13b_summary.csv` (authoritative file):
baseline formal share **0.2858** (surplus) vs **0.4634** (rival, sigma=0.5); rival degree income
**32.319** at sigma=0.5 vs surplus **2.926**; at sigma=1.0 rival degree income 4.002; sigma=2.0 1.987.
Any other figure quoted for E13b should be replaced by the values in `e13b_summary.csv`. The
non-level-matching is real and is what E13c fixes.
