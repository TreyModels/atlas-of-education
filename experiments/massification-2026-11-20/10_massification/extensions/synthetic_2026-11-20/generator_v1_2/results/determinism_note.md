# Determinism note — SYNTHETIC generator v1.2

**`LABEL: SYNTHETIC.`** This note records the evidence that the v1.2 results are byte-reproducible. It is
not evidence about any country.

## Method

Two clean runs of the **same frozen code** and the **same frozen parameters** into separate output
directories, followed by `cmp` on all three results CSVs and on the manifest. No wall-clock, hostname,
elapsed time, process id or OS entropy is written into any output file; the only time value is printed to
stdout.

- RNG: `numpy.random.default_rng(20261120)` (PCG64), one stream, fixed draw order.
- Floats: written at `%.10g`; column order fixed.
- Run 1 output: `results/` (the canonical artifacts), manifest `RUN_MANIFEST.json`.
- Run 2 output: `/tmp/v12_rerun_b/`, manifest `/tmp/v12_manifest_b.json`.

## Commands

```bash
python code/sim_v1_2.py
python code/sim_v1_2.py --out /tmp/v12_rerun_b --manifest /tmp/v12_manifest_b.json

for f in synthetic_panel_v1_2.csv reproduction_checks_v1_2.csv \
         reproduction_checks_detail_v1_2.csv; do
  cmp results/$f /tmp/v12_rerun_b/$f && echo "IDENTICAL $f"
done
cmp RUN_MANIFEST.json /tmp/v12_manifest_b.json && echo "IDENTICAL RUN_MANIFEST.json"
```

## Result

```
IDENTICAL synthetic_panel_v1_2.csv
IDENTICAL reproduction_checks_v1_2.csv
IDENTICAL reproduction_checks_detail_v1_2.csv
IDENTICAL RUN_MANIFEST.json
```

## sha256 (run 1 = run 2)

| file | sha256 |
|---|---|
| `results/synthetic_panel_v1_2.csv` | `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac` |
| `results/reproduction_checks_v1_2.csv` | `72a17fb6dcf59db671bbbcdb04111560d1d1aee59791009111dc3861b3f0fba8` |
| `results/reproduction_checks_detail_v1_2.csv` | `0597bafb8f8b90ad03a0164e9c2137cdaaff2186f1d7d0c5e5476462b285706b` |
| `RUN_MANIFEST.json` | `36c40ff95470893a6d6fda21d9afe341ec0f374073a7af56cdf9c55c9b75b876` |

Frozen inputs recorded in the manifest:

| object | sha256 |
|---|---|
| `v1_2/PRE_DECLARATIONS.md` | `fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16` |
| `code/sim_v1_2.py` | `61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c` |
| `PARAMS.md` | `0d619781c4e059f54cf771fb385475f5f939dceced5036e8a21b6e07a2b315e3` |
| `TUNE_LOG.md` | `acc5d929dd1547709010b4a87f719477303d6021441b0cf03478fb9256ec37b0` |

Input data hashes are in `RUN_MANIFEST.json → hashes.input_data_sha256`; results hashes are in
`RUN_MANIFEST.json → hashes.results_sha256`.

## Re-freeze note

Two labelling/contract fixes were made after the first scored run and disclosed in `TUNE_LOG.md` (D5:
tertiary adult rows no longer carry a placeholder child "neither" share; D6: the manifest now records the
results sha256 values). No model parameter changed and every check value is identical; the code was
re-frozen and **both runs repeated** — the hashes above are from the final pair.

## Environment and runtime

- Python 3.11.17 (the programme venv), NumPy 2.4.6.
- ≈0.6 s per run (wall clock; not written to outputs).
- Row count: 30 countries × 56 years × 4 levels = **6 720** panel rows + header.

## Note on `PARAMS.md`

`PARAMS.md` is the human-readable mirror of the module-level parameter block. The **authoritative**
values are the `params` object in `RUN_MANIFEST.json`, emitted by the frozen code. The manifest records
the sha256 of `PARAMS.md` so a reader can detect any post-freeze edit.
