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

## sha256

| file | sha256 (run 1 = run 2) |
|---|---|
| `results/synthetic_panel_v1_2.csv` | `7669486ccac56a36065da1dce3443090f31149afdba48c8479196429c2427093` |
| `results/reproduction_checks_v1_2.csv` | `72a17fb6dcf59db671bbbcdb04111560d1d1aee59791009111dc3861b3f0fba8` |
| `results/reproduction_checks_detail_v1_2.csv` | `0597bafb8f8b90ad03a0164e9c2137cdaaff2186f1d7d0c5e5476462b285706b` |
| `RUN_MANIFEST.json` | `9a2d9c77b14595bdc5e08bd286b1ea865e2091c25ab0ffae49ce8ed544c21afa` |

Frozen inputs recorded in the manifest:

| object | sha256 |
|---|---|
| `v1_2/PRE_DECLARATIONS.md` | `fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16` |
| `code/sim_v1_2.py` | `7aded3e2b099e870a99f1714201536403a5e611ade32380bcbd12e73ee1fa2e5` |
| `PARAMS.md` | `b6f6e84f046d1dcab9d64c95a0209b78cacd0c5aa0ee38a42cfe6e1ce013119a` |
| `TUNE_LOG.md` | `20f5727d20f4feb8629f191b297a0e07971a1a080dbce3223afd9e115f313665` |

Input data hashes are in `RUN_MANIFEST.json → hashes.input_data_sha256`.

## Environment and runtime

- Python 3.11.17 (the programme venv), NumPy 2.4.6.
- ≈0.6 s per run (wall clock; not written to outputs).
- Row count: 30 countries × 56 years × 4 levels = **6 720** panel rows + header.

## Note on `PARAMS.md`

`PARAMS.md` is the human-readable mirror of the module-level parameter block. The **authoritative**
values are the `params` object in `RUN_MANIFEST.json`, emitted by the frozen code. The manifest records
the sha256 of `PARAMS.md` so a reader can detect any post-freeze edit.
