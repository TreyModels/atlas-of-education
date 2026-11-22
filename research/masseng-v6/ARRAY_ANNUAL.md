# Annual array admissions in v5

**Status: illustrative declared-capacity scenario, not observed school supply, calibration, or a validated forecast.**

`masseng/array_admissions.py` implements shared-capacity, fractional, proportional rationing over arbitrary cohort/decile array dimensions. First-choice public and private demand is rationed proportionally. Residual unmet mass may make one second choice in the other sector. No cell ID or input order affects priority.

`masseng/credential.py` adds `annual_market=True` to `CredentialModel`. The default is `False`, preserving the archived run. When enabled, annual declared capacities affect Grade 1, level transitions, tertiary entry, deferred applicants, and subsequent enrollment stocks. The original `engine.py` is untouched.

## Verification

- 18 archived v3/v5 tests pass.
- 26 archived plus array tests pass.
- 24 independent reference-kernel tests pass.
- The array and reference allocators agree across 100 randomized cases; maximum absolute admitted-mass difference is 2.220446049250313e-16.
- Philippines and Cambodia stock-conservation residuals are below 1.6e-16 in the reported runs.

## 2024 scenario diagnostics

| Country | Default tertiary GER | Annual-market tertiary GER | Effective entrants | Admitted entrants | Unmet effective entrants |
|---|---:|---:|---:|---:|---:|
| Philippines | 71.70% | 63.83% | 8,501,064 | 8,501,064 | 0 |
| Cambodia | 17.20% | 16.64% | 991,831 | 970,053 | 21,778 |

Philippine public capacity binds, but spare private capacity absorbs displaced public applicants. Cambodia has positive unmet effective demand. These results demonstrate feedback mechanics only; the seat-coverage inputs are declared assumptions.

Exact outputs are in `results/array_annual_summary.json`. Integration uses the preserved v5 handoff source tree; `engine.py`, country inputs, and fitted parameters remain prerequisites from that archive.
