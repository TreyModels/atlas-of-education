# DETERMINISM NOTE — v1.4 demand-signal core

**LABEL: SYNTHETIC.** This file records a reproducibility check, not a result.

## Method

Two clean runs of `code/sim_v1_4_demand.py` into **separate output directories**,
same seed, same inputs, no warm start: `results/` and `_determinism/run_b/`.
Then `cmp` on **every** produced file and `shasum -a 256` on both.

- Seed `20261120`; one NumPy PCG64 stream; v1.2 draw order; the shadow block and
  the demand block draw no random numbers.
- Floats written at `%.10g`; no wall-clock, hostname, PID, path or timestamp
  enters any output.
- The OFF (demand-block-off) panel is separately required to be byte-identical to
  `generator_v1_3/results/synthetic_panel_v1_3.csv` (the no-re-fit guard).

## Result

| file | sha256 (run A = run B) |
|---|---|
| `ABLATION_TEST.csv` | `0e719e8ea1009d3df1c4c230de2491d1c3c024145d879b3c3ed52c0db19da2da` |
| `DEMAND_CHECKS.csv` | `53f90250878679717c2c014fa78db9c41791fe5a0b8d5dacbba31c3c9cff1535` |
| `DEMAND_CHECKS_DETAIL.csv` | `547ca39b9a4bd00a796d07a96ac0f1369f86172067599e9055eccf08d35482cc` |
| `DETAIL.csv` | `f158899827489b003a7a603d9546598dd8457845edab516954c4555cf4b1af19` |
| `REPLACEMENT_TEST.csv` | `0633f2ad2cf5f0f5f17aa6ac60e61d3f121eae49a10e91b0e41877811bc47017` |
| `_ablation/synthetic_panel_v1_4_demand_off.csv` | `47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3` |
| `synthetic_panel_v1_4_demand.csv` | `ffecd450514cf8259512647db4e78bcd058639c208a1a2057bbac8b506ddbdaa` |

| guard | sha256 | match |
|---|---|---|
| v1.4 OFF panel vs v1.3 panel | `47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3` vs `47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3` | `TRUE` |

## Command used

```bash
fail=0
for f in results/*.csv results/_ablation/*.csv results/*.json; do
  rel=${f#results/}
  cmp -s "$f" "_determinism/run_b/$rel" || { echo "DIFF $rel"; fail=1; }
done
cmp -s RUN_MANIFEST.json _determinism/run_b/RUN_MANIFEST.json || { echo "DIFF manifest"; fail=1; }
echo "determinism cmp failures: $fail"
```

## Caveat

Byte-identity across repeated runs says the *implementation* is deterministic.
It says nothing about whether the model is right, and it is not evidence about
any country.
