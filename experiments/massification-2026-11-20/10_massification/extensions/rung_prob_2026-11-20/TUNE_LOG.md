# TUNE_LOG — EXP-9 RUNG-PROB

**LABEL: SYNTHETIC.** This log records every code change made between the freeze of
`PRE_DECLARATIONS.md` (sha256 `1cd399dd…`) and the scored run. **No parameter, band edge,
tolerance, ablation bar, arm definition, substitution rule, fallback rule, seed, scored object or
frozen code line was changed after any result was seen.** No re-tune was attempted.

## C1 — path constant (coding error, fixed before the scored run)

- **Symptom:** the first invocation refused at `load_rung4_lookup()` with `FileNotFoundError` for
  `10_massification/extensions/generator_v1_2/...` — the constant `SYNTH` had been written as
  `ROOT.parent`, which is `extensions/`, not `extensions/synthetic_2026-11-20/`.
- **Fix:** `SYNTH = ROOT.parent / "synthetic_2026-11-20"`. One line; no value, threshold, arm or
  substitution changed. The run had not produced any result file at the point of failure.
- **Hash before/after of `code/run_rung_prob.py`:** not carried (the file was still being
  authored when the path failed; the first executable hash is the one in `RUN_MANIFEST.json`).

## C2 — report completeness (no numerical effect)

- Added `BASELINE_GUARD.json` to the manifest's file-hash table and the full set of anchor-2024
  components (`R_gate`, `access`, `w_dest`, `w_inf`, `ER`, `ER_hh`, `ER_mig`, `ER_net`, `ER_P`) to
  `RUNG_PROB_RESULTS.csv`. Reporting only; no value, threshold or arm changes.

## C3 — explicit seed argument (no numerical effect)

- `mod.run_all(...)` now receives `seed=SEED` explicitly in all three calls. The frozen default was
  already `SEED = 20261120`; the values are unchanged (both sealed runs reproduce the same numbers
  and the same panel hashes). Clarity only.

## Dry-run validation (before the scored run)

The harness was exercised once into `_scratch/` to confirm that the byte-identical frozen copy
reproduces the frozen panels. The dry run returned OFF `76.63908112`, arm A `95.04548615` (both
panel hashes matched the frozen files) and arm B `42.12562430`. The scored run reproduced these
numbers exactly; the dry-run directory is deleted before the package is sealed.

## Arm-B definedness rule (fixed before the scored run)

`rung4_demand == 0` in 100 of 1 680 country-years (all pre-2006; none in `SYN00_PHL_LIKE`). The
rule — leave `pi0(g2)` in place where the rung-4 probability does not exist — was fixed from the
data structure before the scored run and is recorded in `PRE_DECLARATIONS.md` §4.2. It is inert for
the scored anchor. The arm-B self-check asserts zero anchor fallbacks and 100/1 680 total.

## Not done (deliberately)

- No `ER_scale`, destination set, migration value, `H`, `B_Z_D`, band, tolerance or seed was
  changed.
- No third arm, no clipping of the rung-4 ratio, no fitted demand parameter (R4/R27).
- No frozen file was edited; the v1.4 code copy hash remains `6e4a6761…`.
