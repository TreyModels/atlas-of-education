# RUN LOG — every command executed by the audit, with exit code

All runs executed 2026-11-20 between 12:16 and 12:23 CST on an 8-core macOS box under
shared load (other agents running). `PY` = `/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python`.
`PYTHONDONTWRITEBYTECODE=1` in every run. `nice -n 10`; per-run `perl -e 'alarm N; exec @ARGV'`.
Source trees were not written to (massabm/triad take `--out`; atlas engines were copied — see
`COPY_PROVENANCE.md`).

| # | Command | Exit | Wall | Output | Notes |
|---|---|---|---|---|---|
| 1 | `cd 01_sources/massification_project/code/massabm && $PY run.py smoke --out 03_audit/runs/massabm/smoke` | 0 | 4.0 s | `runs/massabm/smoke/` (no file expected; prints calibration table) | baseline calibration table printed; targets shown as in README |
| 2 | `.../massabm && $PY run.py grad_supply --reps 2 --N 6000 --workers 2 --out 03_audit/runs/massabm` | 0 | 54 s | `runs/massabm/grad_supply/{findings.txt,grad_supply.csv}` | 36 runs; no failed model runs reported |
| 3 | `.../massabm && $PY run.py floor_test --reps 2 --N 6000 --workers 2 --out 03_audit/runs/massabm` | 0 | 204 s | `runs/massabm/floor_test/{findings.txt,floor_test.csv}` | 36 runs; slow under load |
| 4 | `.../massabm && $PY run.py gates --reps 2 --N 6000 --workers 2 --out 03_audit/runs/massabm` | 0 | 143 s | `runs/massabm/gates/{findings.txt,gates.png}` | 20 runs |
| 5 | `.../massabm && $PY run.py reform_distribution --reps 2 --N 6000 --workers 2 --out 03_audit/runs/massabm` | 0 | 57 s | `runs/massabm/reform_distribution/{findings.txt,reform_distribution.png}` | 8 paired runs |
| 6 | `cd 01_sources/massification_project/code/triad && $PY run_triad.py all --quick --workers 2 --out 03_audit/runs/triad` | 0 | ~71 s | `runs/triad/<9 experiments>/` | 9 experiments; per-experiment times: emergence 3 s, necessity 11 s, lockin 6 s, conditions 7 s, dose 7 s, fair_signal 9 s, learning 9 s, state_motive 9 s, macro_state 17 s |
| 7 | `.../triad && $PY run_triad.py necessity --reps 2 --N 3000 --workers 2 --out 03_audit/runs/triad` | 0 | 32 s | `runs/triad/necessity/` | 32 runs; overwrote the 1-rep quick output for this experiment |
| 8 | `cd 03_audit/scripts/atlas_engine && $PY ../run_floorworld_baseline.py` | 0 | 0.5 s | `runs/floorworld/{baseline_paths.csv,baseline_tests.json}` | 5 structures × 4 countries, deterministic first `rng(23)` draw |
| 9 | `cd 03_audit/scripts/atlas_engine && $PY floorworld_mc.py --draws 400` (attempt 1) | **1** | ~75 s | none — **failed at final `json.dump`** | `FileNotFoundError`: `scripts/atlas_engine/results/` did not exist (copy missing the repo's committed `engine/results/` dir). All five structures computed and printed. |
| 10 | `mkdir -p results && $PY floorworld_mc.py --draws 400` (retry) | 0 | ~80 s | `scripts/atlas_engine/results/floorworld_mc.{json,md}` | fresh table used in matrix §5 |
| 11 | `cd 03_audit/scripts/atlas_engine && $PY ../run_childworld_audit.py 100` | 0 | ~40 s | `runs/childworld/{childworld_mc_v1.json,childworld_mc_v1.md}` | 100-world smoke (documented default 6,000); most countries have too few accepted worlds at n=100 — not interpretable, execution-only check |
| 12 | `cd 03_audit/scripts/atlas_engine && $PY ../run_relfloor_audit.py 120` | 0 | ~60 s | `runs/relfloor/{relfloor_smoke.json,relfloor_countries_nd120.json}` | single deterministic household path (completion 0.428/0.638/0.833 for 1998/2016/2035) + 120-draw country screen; acceptance thin (0–10 draws/cell) — execution check, not inference |
| 13 | `.../massabm && $PY -B -c "timing probe: run_model on each floor_test mode at N=6000"` | 0 | 55 s | stdout only | per-run cost probe: 9.2–13.3 s/run under load; explains floor_test wall time |

## Run status summary

- **Executed cleanly:** massabm smoke, floor_test, grad_supply, gates, reform_distribution; triad all
  (quick) and necessity (reps 2); floorworld baseline + MC; childworld smoke; relfloor smoke.
- **Failed once and then fixed:** floorworld_mc attempt 1 (missing output directory, not a model failure).
- **Heavy runs deliberately not started / not scaled** (Lead instruction to keep machine load down):
  full 6,000-world childworld MC, 24,000-draw relfloor screen, firms/Tilly fits, shadow-abm SMC,
  massabm all/round2–round4, triad 30-rep sets, calibrate/sensitivity.
- **Model-run failures / non-convergence:** none reported by `run_many` in any executed experiment
  (`massabm` prints failed runs; `triad` filters them; both stayed empty).
- **No exit code other than the one floorworld_mc attempt-1 failure.**

## Log files

`logs/floor_test.log`, `logs/grad_supply.log`, `logs/gates.log`, `logs/reform_distribution.log`,
`logs/triad_all_quick.log`, `logs/triad_necessity_reps2.log`, `logs/floorworld_baseline.log`,
`logs/floorworld_mc.log`, `logs/childworld.log`, `logs/relfloor.log`, `logs/smoke.log`
(the smoke calibration table is in `logs/smoke.log`; command #1 above).

## Reproduction environment

Python 3.11.17, numpy 2.4.6, scipy 1.17.1, pandas 3.1.1, matplotlib 3.11.2, macOS, 8 cores.
Stored historical runs used Python 3.10.2 / numpy 2.2.6 / scipy 1.15.3 / matplotlib 3.10.9 (round-2
notes). No dependency lock file exists in `massification_project`.
