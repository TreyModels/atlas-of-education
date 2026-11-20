# Determinism note — EXP-9 RUNG-PROB

Two clean runs, separate output directories (`results/` and `results/determinism_run2/`).
Every result file and the manifest `cmp` byte-identical; **0 failures**.

| file | sha256 (run 1 = run 2) | cmp |
|---|---|---|
| `RUNG_PROB_RESULTS.csv` | `95b598dbf998ed1a061ad9295d13970e89d45b55073b2365e102ca185fd73a7d` | OK |
| `RUNG_PROB_ARMS.csv` | `7743bbfaa8d100791cd26e85cce0a8f772d90d005012b6df98f24013eb616aa7` | OK |
| `BASELINE_GUARD.json` | `21c94d637a0f063ab03b9848e5599825b375a9bef9ffda03965fde3780108672` | OK |
| `panels/synthetic_panel_v1_4_demand_off.csv` | `47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3` | OK |
| `panels/synthetic_panel_v1_4_demand_on_armA.csv` | `ffecd450514cf8259512647db4e78bcd058639c208a1a2057bbac8b506ddbdaa` | OK |
| `panels/synthetic_panel_v1_4_demand_on_armB.csv` | `6b9befffc159d536c470267e55ab6fba2d27ebb8e281342877fa06ce125c10f7` | OK |
| `RUN_MANIFEST.json` | `58eed2131ede1b3b0c9fafb7ec2dc7d693b9c88a323597d663aab416d2b75e12` | OK |

Command equivalent:
```
for f in results/*.csv results/*.json results/panels/*.csv; do
  rel=${f#results/}; cmp -s "$f" "results/determinism_run2/$rel" || echo DIFF $rel
done
cmp -s RUN_MANIFEST.json results/determinism_run2/RUN_MANIFEST.json || echo DIFF manifest
```

No wall-clock, absolute path, PID or hostname appears in any result file. Floats use `%.10g`.
