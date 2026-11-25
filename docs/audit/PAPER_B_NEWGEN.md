# Paper B — NEW GENERATION (repaired engine, frozen V540-FREEZE, 100 matched seeds vs legacy 30)

**Label: NEW GENERATION — REPRODUCED SIMULATION.** The Gemini-era 420/540 docx tables are the
AUTHOR-REPORTED baseline; this run is not a reproduction of them. Uncertainty: seed/MC (100 matched seeds);
calibrated-parameter uncertainty is **zero in this stage** (frozen parameters) and is stated as such.

## HK — arms (mean [seed sd], delta vs Baseline)

| arm | K-12 part. % | G12 % | Q5-Q1 gap pp | Q5/Q1 spend | spend idx | elite Q5 % | contest effort |
|---|---|---|---|---|---|---|---|
| Baseline | 61.93 (0.21) | 49.37 (0.51) | 34.89 (0.67) | 2.473 (0.050) | 100.0 | 24.82 (1.06) | 0.0423 |
| CF1a | 61.39 (0.20) | 42.61 (0.58) | 35.29 (0.67) | 2.628 (0.056) | 96.5 | 24.43 (1.02) | 0.0218 |
| CF1b | 62.02 (0.21) | 50.69 (0.52) | 34.71 (0.66) | 2.264 (0.040) | 97.2 | 23.49 (1.10) | 0.0349 |
| CF2a | 65.85 (0.20) | 52.46 (0.48) | 32.77 (0.71) | 2.245 (0.045) | 109.3 | 24.57 (0.97) | 0.0537 |
| CF2b | 75.05 (0.21) | 56.40 (0.46) | 25.54 (0.70) | 1.720 (0.030) | 131.7 | 22.94 (0.61) | 0.0813 |
| CF3a | 54.19 (0.21) | 42.76 (0.56) | 36.61 (0.62) | 2.739 (0.055) | 82.5 | 24.33 (1.07) | 0.0218 |
| CF3b | 48.56 (0.18) | 38.59 (0.53) | 36.36 (0.56) | 2.804 (0.058) | 70.9 | 23.43 (1.12) | 0.0103 |
| CF4a | 48.60 (0.17) | 39.14 (0.54) | 36.39 (0.59) | 2.760 (0.058) | 70.6 | 23.21 (1.13) | 0.0095 |
| CF4b | 57.90 (0.18) | 45.74 (0.56) | 34.43 (0.71) | 2.411 (0.050) | 90.0 | 23.07 (0.62) | 0.0292 |

## KR — arms (mean [seed sd], delta vs Baseline)

| arm | K-12 part. % | G12 % | Q5-Q1 gap pp | Q5/Q1 spend | spend idx | elite Q5 % | contest effort |
|---|---|---|---|---|---|---|---|
| Baseline | 55.79 (0.24) | 36.25 (0.52) | 31.26 (0.79) | 2.205 (0.044) | 100.0 | 23.90 (1.71) | 0.0144 |
| CF1a | 55.45 (0.24) | 32.42 (0.51) | 30.71 (0.71) | 2.097 (0.042) | 97.1 | 22.85 (1.76) | 0.0053 |
| CF1b | 55.83 (0.26) | 36.79 (0.53) | 31.24 (0.76) | 2.150 (0.040) | 99.2 | 23.53 (1.66) | 0.0127 |
| CF2a | 60.92 (0.26) | 41.42 (0.52) | 29.82 (0.72) | 2.141 (0.039) | 113.5 | 24.50 (1.32) | 0.0268 |
| CF2b | 76.20 (0.25) | 55.30 (0.46) | 17.79 (0.87) | 1.609 (0.031) | 164.8 | 23.79 (0.71) | 0.0883 |
| CF3a | 48.19 (0.24) | 32.29 (0.51) | 31.82 (0.78) | 2.308 (0.054) | 83.7 | 22.83 (1.69) | 0.0053 |
| CF3b | 42.80 (0.24) | 30.42 (0.47) | 31.15 (0.68) | 2.399 (0.056) | 73.2 | 22.21 (1.61) | 0.0017 |
| CF4a | 42.81 (0.24) | 30.56 (0.49) | 31.20 (0.68) | 2.391 (0.055) | 73.1 | 22.16 (1.64) | 0.0015 |
| CF4b | 58.37 (0.23) | 42.66 (0.53) | 29.37 (0.70) | 2.112 (0.041) | 109.7 | 23.61 (0.73) | 0.0282 |

## CF4 reversal (vs the pre-repair 540 run) — explicit

Pre-repair 540 result: CF4a failed the Win-Win criterion (spend index and/or elite Q5 did not fall in both
jurisdictions). The new-generation numbers are in the table above; the reversal direction is recorded with
the seed CIs, and the old failure is preserved in `GATE1_MIGRATION_TABLE.md` / `paper_claims.csv` — the new
run neither erases it nor claims it was wrong.

## KR-SINGLE sensitivity (gate design) — primary outcomes

| arm | K-12 part. % | Q5-Q1 gap pp | Q5/Q1 spend | elite Q5 % |
|---|---|---|---|---|
| Baseline | 48.07 | 32.24 | 2.596 | 24.08 |
| CF1a | 47.72 | 31.77 | 2.491 | 22.99 |
| CF1b | 48.11 | 32.22 | 2.523 | 23.64 |
| CF2a | 53.40 | 31.51 | 2.464 | 24.66 |
| CF2b | 70.91 | 20.91 | 1.657 | 23.59 |
| CF3a | 42.39 | 31.62 | 2.629 | 22.94 |
| CF3b | 38.58 | 30.26 | 2.609 | 22.09 |
| CF4a | 38.58 | 30.27 | 2.595 | 22.04 |
| CF4b | 54.03 | 30.00 | 2.266 | 23.59 |

## Caveats

* Frozen spec parameters are not calibrated in this generation; no VALIDATED claim.
* Seed/MC uncertainty only (100 matched seeds); parameter uncertainty is zero by construction here.
* Labels: AUTHOR-REPORTED baseline (Gemini docx), REPRODUCED SIMULATION (540 legacy), NEW GENERATION (this).
* Multiplicity: all 9 arms × 4 headline outcomes × 2 jurisdictions reported; CF4a is the pre-stated primary.
