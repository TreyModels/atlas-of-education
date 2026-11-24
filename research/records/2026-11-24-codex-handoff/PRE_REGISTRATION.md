# Pre-registration — replication of the Codex handoff benchmark

Written before running anything. Branch: research/codex-handoff-run-2026-11-24 (off origin/main).

## Question
Can the reader reproduce the Codex handoff benchmark exactly as supplied, on a clean Linux environment, and do the supplied synthetic and pairing scripts yield the stated metadata? This is a replication/verification job, not a new analysis.

## Inputs
- `research/records/2026-11-24-next-tests/data/long_run_panel.csv`, sha256 `cd30d7ea7beb77b63de092c53f9b143065b94651f1ac95535ac70eebb3280f2d` (verified on receipt).
- Codex scripts at the committed paths under `research/records/2026-11-24-codex-handoff/scripts/`.

## Environment to record
python -V, numpy/pandas versions, platform, `OPENBLAS_NUM_THREADS=1`, seeds, input sha256, stdout/stderr, wall time.

## Specifications and decision rules
1. `test_checks.py`: report pass/fail count; expected 5/5 pass.
2. `competing_worlds.py --seed 71201 --reps 200 --n-per-cell 400`: expected summary — structured micro likelihood wins 200/200 effect world, 200/200 selection world, 0/200 common-trend world. Record any deviation as a replication failure.
3. `country_pairs.py --panel ... --baseline 1980 --start 1990 --end 2010`: expected metadata — 105 baseline-complete countries, 52 disjoint pairs, 1 unpaired, 52 pairs with both 1990–2010 schooling and TFR changes. Record any deviation.
4. `fdr_check.py`: do NOT apply to the "robust everywhere" rule as if it were a p-value. Only run on a real, complete p-value family if one is supplied; otherwise record as not applicable.
5. No new inference, no causal language, no performance claims. All outputs labelled exploratory replication.

## Interpretation rule
Pass = the supplied scripts run and reproduce the stated expected values within the stated tolerances. A mismatch is reported plainly, not explained away.
