# Opus engine5: fractional annual admissions

This is the integration into **Opus's `engine5.py`**, not the earlier exploratory `CredentialModel` patch. Copy `masseng/engine5.py` and `masseng/array_admissions.py` over the corresponding files in the Opus handoff model; place `tests/test_engine5_array.py` in its `tests/` directory.

## What changed

- `Model5(..., annual_market=True)` enables absolute annual public/private new-entrant capacities, in persons, from `config['v5']['annual_capacity']`. The default remains `False`; the original R0–R5 behaviour and tests are preserved.
- Grade 1, lower-secondary, upper-secondary, and tertiary entrants share a national two-sector market. Fractional mass is rationed proportionally within first-choice sector, followed by one proportional cascade into spare capacity in the other sector. No identifier or cohort ordering affects admission.
- Deferred and new tertiary candidates enter the same market once. Unadmitted new completers join the deferral pool; unadmitted returning candidates remain in it. Existing exam gates and expiry rules remain.
- `result.extra['markets']` reports annual `Q`, `L`, `E`, `R` by level and decile in persons. `L` uses the lower of zero-full-cost and actual subsidised-cost utility, so net-negative transfers do not invert the funnel. Capacity and realised admissions by sector and unmet effective demand are also reported.
- Declared new-entrant capacity is separate from observed enrolment stocks. No supply is inferred from enrolment.

## Verification

From the Opus model directory:

```bash
python -m pytest -q tests/test_engine5_array.py tests/test_engine5.py tests/test_model.py
```

Local result: **29 passed**. Tests cover fractional half-seats, proportional rationing, permutation invariance, cascade conservation, net-negative transfers, deferred-pool conservation, every R0–R5 specification, exact default-indicator equivalence, and PHL/KHM runs.

## Declared sensitivity scenarios

`experiments/run_engine5_array.py` applies the earlier declared capacity-coverage assumptions to reference-age populations. They are **not observed school places, estimated supply elasticities, fitted R0–R5 results, or empirical validation**.

| 2024 diagnostic | Philippines | Cambodia |
|---|---:|---:|
| Tertiary GER, unconstrained | 27.1755% | 8.5776% |
| Tertiary GER, declared capacities | 24.3923% | 7.6437% |
| Unmet effective primary entrants | 0 | 18,541 |
| Unmet effective tertiary entrants | 0 | 0 |

The capped Philippine tertiary stock differs despite zero unmet entrants in 2024 because earlier capacity constraints persist in cohort histories. Full machine-readable outputs are in `results/engine5_array_summary.json`.

No R0–R5 fit was started: the handoff's driver and target gaps remain. Hong Kong cycle structure, joint destinations, gates, tutoring, and its 2012 double cohort remain separate future work.
