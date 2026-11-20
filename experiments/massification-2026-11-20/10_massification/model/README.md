# 10_massification/model — push-pull cohort-flow massification model

**Owner:** experiment-runner (`deepseek-exp1`). **Status: scaffold + predeclaration; calibration GATED on Council
brief 013.** Nothing in this directory is a fitted result.

## Files
| file | purpose |
|---|---|
| `PREDECLARATION.md` | full declared design: structure, channels, rivals, calibration/holdout, scaling checks, push-pull decomposition, discriminating test, recovery design, gate conditions |
| `pushpull.py` | the model. `--structure-smoke` = accounting-only run with declared priors; any calibration mode prints `GATED` and exits |
| `configs.py` | six country configs (PHL/KHM/HKG/CHN/KOR/JPN), every value labelled S/E/A/F |
| `smoke/structure_smoke.csv` | structure smoke output, 6 countries × 3 rivals × 1960–2040 (simulated; NOT a result) |
| `smoke/accounting_checks.csv` | B1–B4 accounting-check results (0 failures at the declared priors) |

## Model in one paragraph (for replication by the other runner)
Single-year cohorts 0–84 with a declared TFR path; intake at age 6; annual progression through
primary/lower/upper/tertiary with country cycle lengths; sectoral employment shares (agri/industry/services,
formal/informal) as declared reduced forms in log GDP per capita and the educated-labour share; two lagged
channels with elasticities — education→jobs (`e_s`, lag `lag_s`) and jobs→schooling (`e_d`, lag `lag_d`); three
rivals are the same code with the channels switched. No observed target is coded as a parameter; the config
holds parameter *ranges* only. Enrolment stocks are generated from cohort flow, not supplied.

## How to run (only the smoke is permitted until the gate lands)
```
cd 10_massification/model
"$PY" pushpull.py --structure-smoke     # writes smoke/*, prints accounting failures, exits 0
"$PY" pushpull.py --calibrate           # prints GATED and exits 2 (no fitting)
```

## Replication request (to experiment-runner-2)
Reproduce `smoke/structure_smoke.csv` from `configs.py` at the declared priors and confirm the accounting checks
(B1 population/births, B2 non-negative generated enrolment rates, B3 sector shares sum to 1 and rates in [0,1],
B4 no target coded as a parameter). If your independent version disagrees on the generated enrolment ranges, post
`ACK:` with the disagreement before either of us fits anything.

## Status note (2026-11-20, repo-auditor instruction 4)
The PHL smoke fit and the PHL+CHN+KHM batch (`calib/`) are **pre-anchor diagnostics**, not the anchor-system result:
they were run before the user/Council pivot to a one-anchor design. Their labels are unchanged (R12): PHL PARTIAL at
best (loses the linear-trend benchmark), CHN in-sample FAIL on a thin n=4 window, KHM held-out FAIL by 28–32 pp,
rivals EQUIVALENT, no direction claim. They are retained as diagnostics; the anchor-system model (switchable
state-push/demand-pull/supply-push mechanisms) is predeclared in `PRE_PIVOT_ANCHOR.md` and will be built only after
the Council names the anchor and the single-system success criteria.
