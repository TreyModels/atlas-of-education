# loop5 status — what actually ran (task-23, Council brief 007)

| cell | status | file(s) |
|---|---|---|
| E2 provider technology / fee block (KOR + HKG) | **completed** — thresholds FAIL (details below) | `E2/findings.txt`, `E2/e2_spend_mix.csv`, `E2/e2_price_decomposition.csv`, `E2/e2_sensitivity.csv`, `E2/findings_sensitivity.txt` |
| E3 Japan within-country gradient | **completed** — density channel passes, income & gate-stakes fail | `E3/findings.txt`, `E3/e3_channels.csv` |
| E2/E3 as "rescues" of loop-4 inversions | **NOT SUPPORTED** — diagnostic only | see verdicts |

## E2 — verdict per predeclared threshold

| threshold | result | detail |
|---|---|---|
| T1 KOR spend mix, all five within ±10 pp | **FAIL at the declared quality prior** | hagwon 47.7% vs obs 73.7% (−26.0 pp); 1:1 13.0 vs 11.3 (PASS); small group 17.3 vs 6.7 (FAIL +10.6); internet 13.3 vs 4.9 (PASS); textbook 8.7 vs 3.4 (PASS) |
| T1 robustness over 36 declared quality parameterisations | **3/36 pass (8%)** | best corner (q1:1=0.95, q_sg=0.85, boost=0.15): hagwon 63.8 (−9.9), 1:1 11.3 (exact), sg 12.6 (+5.9), net 7.1 (+2.2), tb 5.2 (+1.8) → all inside ±10 pp |
| T2 HKG mass-lecture S6-7 ≥20 pp above S4-5 | **FAIL at the declared prior; 33/36 in the quality grid pass** | declared-prior run: S4-5 82.3% vs S6-7 27.0% (**−55.3 pp, reversed**); grid runs reach up to +89 pp. The pass/fail flips with quality priors and seed → **not identified** |
| T3 HKG fee/income inside 1.1–5.0% | **PASS** | model average fee 114k won-equiv / 3,200k median income = **3.56%** |

**Robust diagnostic (not a threshold):** observed KOR fees are **1.5–4.2×** the teacher-time-plus-amortised-entry cost
(hagwon 2.2×, 1:1 2.1×, small group 4.2×, internet 1.8×, textbook 1.5×). A cost-plus technology block therefore cannot
price itself: rents/brand/marketing (or hours heterogeneity) carry the fee. The mixed arm separates demand from spend
only weakly (commercial demand 80.2% vs spend 85.3% at the declared prior), so **provider technology is not the missing
channel behind loop-4's provider-ordering inversion, and it does not rescue U1's by-level reversal** (E1's failure
removes the gate-position story; income gradient E4 remains the only loop-5 positive).

## E3 — Japan gradient (grade-6 juku: mean 41.8, Akita 22.1 – Tokyo 57.9)

| channel | Tokyo/Akita auxiliary ratio | required elasticity | predeclared plausibility band | verdict |
|---|---|---|---|---|
| density / competition | 71.5 (density 6,363 vs 89 per km²) | **0.226** | 0.1–0.6 | **PASS** |
| income | 1.6 | 2.05 | 0.1–1.0 | **FAIL** |
| gate stakes | 1.2 | 5.29 | 0.5–2.0 | **FAIL** |

**T5 (density model mean within ±5 pp of 41.8): NOT COMPUTABLE** — only the two endpoints and the mean are on disk;
predicting the unweighted prefecture mean would require inventing 45 prefecture values. Reported as a data gap.
**Limits:** n=2 → no rank correlation / R²; density is *not rejected*, not identified; income collinear with density at
the endpoints; r=−0.16 with achievement is an external note only.

## What did not run
Nothing in E2/E3 is unrun. Both are completed cells. No rescue claim is made, and no threshold is reported as passing
where the declared prior failed — the sensitivity grid is reported alongside, not substituted for, the predeclared test.
