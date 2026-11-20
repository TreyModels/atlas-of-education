# EXPERIMENTS — E6 independent timing comparison (observed estimation; no direction claim)

**Owner pair:** deepseek-exp2 + pattern-scout (brief-013 slate #2; D34–D37, Amendment A4). **Crossing years are
holdout outcomes, never fitted (R4/R5); no direction claim (R13/EQUIVALENT).** Predeclaration: `E6_PREREG.md`
(written before running). Code: `code/e6.py`; outputs `runs/e6_timing_independent.csv`, `runs/e6_findings.txt`,
`runs/e6_meta.json`. Observed cells only; reconstructed timing rows excluded from primary and used as sensitivity.

## Design
For each country × milestone (M1–M4, plus M0 where applicable) with a primary non-reconstructed timing row, the
four single-curve forms (logistic, Gompertz, linear, exponential) were fitted **only on observed years strictly
before the crossing band's lower bound** (crossing = holdout); predicted crossing = first year the fitted curve
reaches the threshold. Tolerances: ±5 y (band midpoint), ±3 y where the band ≤2 y. Left-censored milestones =
boundary constraint only; right-censored = false-positive test (must not predict a crossing before last observation).

## Result (agreement with scout's E6: 0/9 comparable cells within 1 y — method difference flagged below)

| form | scored milestones | PASS | median \|error\| | false crossings |
|---|---|---|---|---|
| logistic | 6 | **2** | 5.5 y | 0 |
| Gompertz | 6 | **1** | 8.0 y | 0 |
| linear | 6 | 0 | 178.5 y | 0 |
| exponential | 6 | 0 | 43.8 y | 0 |

Cell status across all 120 form × milestone rows: LEFT-CENSORED **44**, NO-CROSSING-OK **28**, UNABLE **24**,
FAIL **11**, NO-PRED-CROSSING **7**, PASS **3**, PARTIAL **3**.

**Predeclared rule:** timing reproduced iff ≥2/3 of scored milestones PASS for a bounded form (logistic/Gompertz)
AND zero false crossings. **Result: FAIL — E6 TIMING STRUCTURAL MISS (R19); the cycle closes with PARTIAL +
EQUIVALENT + explicit timing miss (D36).** Only 6 milestones are scored at all: JPN tertiary (logistic PASS +5.0 y,
Gompertz PARTIAL), CHN tertiary (logistic +0.5 y, Gompertz +1.5 y PASS), HKG lower-secondary (no predicted
crossing from the bounded forms; exponential PARTIAL) and HKG tertiary (logistic +10.5 y, Gompertz +11.5 y FAIL),
PHL lower-secondary (logistic PARTIAL +5.5 y), PHL tertiary (logistic +29.5 y FAIL).

## What cannot be identified
- **Near-universal systems are mostly LEFT-CENSORED** (JPN primary/upper-secondary/lower-secondary; KOR all levels;
  HKG upper-secondary mass; PHL upper-secondary mass): the crossing is at/before the observed window, so the timing
  estimand is only a **boundary constraint** ("crossed at or before Y0") — 44/120 cells. There is no point-timing
  information for most near-universal milestones in the observed windows; E6 has little power for exactly the
  systems where timing is the outcome.
- 24 cells are **UNABLE** (fewer than 8 pre-crossing observations), and 7 bounded-form cells produce **no predicted
  crossing** within 300 y.
- **False-positive test passes** for all forms (0 false crossings), so the failure is a timing/magnitude failure,
  not a spurious-crossing failure.

## Scout comparison — flagged, not adjudicated
My E6 agrees with scout's `e6_timing_comparison.csv` in **0/9** comparable cells (within 1 y). The likely cause is
method, not data: this independent version fits **only pre-crossing observations** (strict holdout), while the
scout file's predictions are consistent with fits that include the crossing period. That difference must be
adjudicated by the Council — if the scout fit uses crossing years, its timing errors understate true out-of-sample
error (R4/R5 risk). Our stricter version is the one that can speak to the timing gate.

## Verdict and links
E6 = **FAIL (structural timing miss, R19)** under the predeclared rule; the E6 timing cell cannot certify
"the model generates when universalization happened" for near-universal systems from these observed windows.
R4/R5 (no fitted/supplied timing), R13 (no direction claim), R19 (timing miss), R3 (equivalence) cited. No git
writes (executor commits).
