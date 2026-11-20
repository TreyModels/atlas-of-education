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
| `DEMAND_CHECKS.csv` | `e4d7c43c29c04b013868da68c52a8e1f3eacb113b7cdf2a927954047ea21aa83` |
| `DEMAND_CHECKS_DETAIL.csv` | `4e320e97e8d94a5eb21ceeb95ec29b4a541f3771bc3407b07ad3757f802ae474` |
| `DETAIL.csv` | `f158899827489b003a7a603d9546598dd8457845edab516954c4555cf4b1af19` |
| `REPLACEMENT_TEST.csv` | `b1b5ac89f8840046ed15ae216ceffcdf33ee778ad2261b5f14f6449f56441feb` |
| `SENSITIVITY.csv` | `289efe4d1fbcfa573cf7e8a0b0224665de2fc7da36067ef40fd43021e840a466` |
| `_ablation/placebo_v2_unchanged_panel.csv` | `af8a088f74f98c4d3dcdfe080485f6e96b37903caa8abefda2a4a2cd0ab9aa57` |
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
