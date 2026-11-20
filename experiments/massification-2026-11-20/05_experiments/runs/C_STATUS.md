# Batch C status (task-8) — what ran, what did not

| cell | status | evidence |
|---|---|---|
| C1 recovery/identification | **completed** | `runs/C1/` (findings.txt, c1_confusion.csv, c1_candidate_moments.csv, c1_truth_moments.csv, run_meta.json), 61 s |
| C2 floorworld S1–S5 (E11) | **completed** | `runs/C2/` (findings.txt, c2_floorworld.csv, c2_decomposition.csv), instant |
| C3 PH calibration | **in progress — NOT completed, not claimed** | predeclared in PRE_DECLARATIONS_C.md; runner `code/exp/run_C3.py` written and launched twice; see below |

## C3: why it did not complete inside the timebox
1. First launch crashed on a spawn-pickling error (local closure passed to ProcessPoolExecutor).
2. Second launch exposed a year-mapping bug: model years are indices into 1920–2035 while observed years
   are 1980–2020; the intersection was computed on values not years, so every distance was 0.
3. Both were fixed in `code/exp/run_C3.py`, and a third launch was started, but the lead's stop order
   arrived before it produced `findings.txt`. No C3 number is reported anywhere and no C3 row is in
   SUMMARY_TABLE.csv. This is honest in-progress, not a failed substantive result.

## Next run (exact)
`PYTHONPATH=code/massabm MASSRUN_EXP=code/exp "$PY" code/exp/run_C3.py --draws 96 --best 6 --N 2000 --Nfine 4000 --out runs/C3`
Expected ~3-4 min on 2 workers: 96 LHS draws at N=2000, best 6 re-evaluated at N=4000, residuals vs the
OBSERVED-only PHL GER series (imputed cells never used). Params: cost_col, cost_shs, bar_college,
bar_basic, apex_mult, hc_school. The cell is a calibration, not a validation.
