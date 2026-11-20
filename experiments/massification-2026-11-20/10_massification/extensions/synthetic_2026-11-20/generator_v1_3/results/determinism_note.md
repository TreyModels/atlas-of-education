# DETERMINISM NOTE — v1.3 shadow module

**LABEL: SYNTHETIC.** This file records a reproducibility check, not a result.

## Method

Two clean runs of `code/sim_v1_3.py` into **separate output directories**, same seed, same inputs,
no warm start:

```
run A:  python code/sim_v1_3.py --out results                            --manifest RUN_MANIFEST.json
run B:  python code/sim_v1_3.py --out _determinism/run_b                 --manifest _determinism/run_b/RUN_MANIFEST.json
```

Then `cmp` on **every** produced file, plus `shasum -a 256` on both.

- Seed: `20261120`; one NumPy `PCG64` stream (`np.random.default_rng`); v1.2 draw order; the shadow
  block draws no random numbers at all.
- Floats written at `%.10g`; no wall-clock, hostname, PID or path enters any output; no timestamp.
- `run B` was executed after `run A` completed, in the same interpreter version
  (Python 3.11.17, NumPy 2.4.6).

## Result

**9 of 9 result files are byte-identical, and so is `RUN_MANIFEST.json`.** `cmp` reported no
difference for any file.

| file | sha256 (run A = run B) |
|---|---|
| `synthetic_panel_v1_3.csv` | `47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3` |
| `shadow_gates_v1_3.csv` | `df3cab007ce5fbe9a48d58b0701d04e6d762591848ca1517a634c8f897edb351` |
| `shadow_checks_v1_3.csv` | `e6a83de509362fbeb1e1e987e9b2b30dd1ff1e13905d56db0938cab911bd68f1` |
| `shadow_checks_detail_v1_3.csv` | `b194e3579b9d7cffcc4e6d8e59bcb843f98363f62ecbb6638ccbe3c1784f30e5` |
| `shadow_decomposition_v1_3.csv` | `db8b7643d2b35f91954c0951af9a22a8500a1f089c4fd79823c60300af2851a9` |
| `shadow_sensitivity_v1_3.csv` | `49c2d6a9e753513aaa0d0b33367883c1e7d8796a23858ce8fad20db37d70f366` |
| `shadow_country_inputs_audit.csv` | `8620316d3427183c3d22110616ee8f712218d35b42c05ae0d6f07264c2c61f86` |
| `shadow_diagnostics_v1_3.json` | `9dadee96fbdf5f636b195b63bced2d5eeb451f99c822c16a01147a0f54353548` |
| `_ablation/synthetic_panel_v1_3_shadow_off.csv` | `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac` |
| `RUN_MANIFEST.json` | `7e1f14526886d16230d867d8cfc81f90429ffb12b17bc881845b3dc766bde09c` |

The ablation artifact's sha256 is **also** the sha256 of the frozen
`generator_v1_2/results/synthetic_panel_v1_2.csv` (`14729c51…`), which is check **c6**.

## Command used

```bash
fail=0
for f in results/*.csv results/*.json results/_ablation/*.csv; do
  rel=${f#results/}
  cmp -s "$f" "_determinism/run_b/$rel" || { echo "DIFF $rel"; fail=1; }
done
cmp -s RUN_MANIFEST.json _determinism/run_b/RUN_MANIFEST.json || { echo "DIFF manifest"; fail=1; }
echo "determinism cmp failures: $fail"     # -> 0
```

## Caveat

Byte-identity across repeated runs says the *implementation* is deterministic. It says nothing
about whether the model is right, and it is not evidence about any country.
