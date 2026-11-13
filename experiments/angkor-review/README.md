# Angkor model review: before and after

Scope: review items 5.1 to 5.7. Engines are in `public/engines/`. Maintenance-model code is in `model/`. Results are in `results/` and `before/`, `after/`. The originals are in `original/` (HEAD copies, byte-identical to the pre-edit files).

## Defaults changed (new behaviour is the default)

| Item | Where | Old behaviour (reproduce with) | New default |
|---|---|---|---|
| 5.1 coordination multiplier | `public/engines/petri.js`, `public/engines/relocation.js` | `coordination: 5**.227` (1.441) | `coordination: 1` |
| 5.4 water floor | same two files | `waterFloor: 0.1` | `waterFloor: 0` |
| 5.4 canal floor | `model/accounted_v2.py` | `canal_floor=0.3` | `canal_floor=0.0` |
| 5.5 reshuffle channels | `model/accounted_v2.py` | `reshuffle_parts='all'` (all four on, as before) | `'all'`, now selectable: `extraction`, `relief`, `trust`, `grievance` |
| 5.6 elite grain spend | `model/accounted_v2.py` | `elite_spend=0.0` | `elite_spend=0.1`, `elite_use='relief'` |
| 5.2 monsoon | `public/engines/monsoon.js` | unchanged (sweep kept) | unchanged |
| 5.3 calibration | `calibrate_provisioning.py` | standalone; `provisioning.js` unchanged | n/a |

Reproduction check: the new Petri and relocation engines with old parameters match the original engines with zero difference (`results/sweep-engines.md`). The flagged maintenance model with old flags matches the original on 240 runs with zero difference, and matches the stored `experiments/maintenance-repair/runs.csv` to 7e-12 (`results/maintenance-checks.json`). A reshuffle with no channels on equals `maintenance_only` exactly.

## 5.1 and 5.4 (petri and relocation): 256 Petri seeds, 32 relocation seeds

Source: `results/sweep-engines.md`. Values are mean ± SD [p10, p90].

Petri, coordination and water floor:

| Scenario | Coordination | Water floor | Peak population | Final/peak retained | Food gap |
|---|---|---|---|---|---|
| stable | 1 (new default) | 0 (new) | 1.015 ± 0.004 | 0.946 ± 0.004 | 0.698 ± 0.050 |
| stable | 1.200 (midpoint) | 0 (new) | 1.163 ± 0.004 | 0.990 ± 0.003 | 0.217 ± 0.048 |
| stable | 1.441 (old) | 0.1 (old) | 1.383 ± 0.003 | 1.000 ± 0.000 | 0.000 ± 0.000 |
| drought | 1 (new default) | 0 (new) | 0.922 ± 0.001 | 0.665 ± 0.003 | 4.402 ± 0.028 |
| drought | 1.200 (midpoint) | 0 (new) | 1.026 ± 0.001 | 0.884 ± 0.002 | 3.476 ± 0.025 |
| drought | 1.441 (old) | 0.1 (old) | 1.135 ± 0.002 | 1.000 ± 0.000 | 2.132 ± 0.028 |

The water floor alone (coordination 1 fixed) moves drought retention from 0.665 to 0.714 and the food gap from 4.402 to 4.153. Under stable climate it moves retention from 0.946 to 0.991.

Relocation, drought, outside advantage 1.2, moving cost 0.25, portability 0.75, local repair 0.5, 32 seeds:

| Coordination | Water floor | Elite exit | Final elite share | Old-centre rural retained | Old-centre core retained |
|---|---|---|---|---|---|
| 1 (new default) | 0 (new) | 0/32 | 0.749 ± 0.002 | 0.947 ± 0.004 | 0.925 ± 0.004 |
| 1.200 (midpoint) | 0 (new) | 0/32 | 0.740 ± 0.002 | 0.990 ± 0.002 | 0.959 ± 0.003 |
| 1.441 (old) | 0.1 (old) | 32/32 | 0.132 ± 0.003 | 1.000 ± 0.000 | 0.478 ± 0.006 |

Stable climate, same settings: no exits at any coordination value.

Existing scripts, before and after (`run-petri.cjs`, `run-relocation.cjs`, both now take `ENGINE` and `OUT`):
- Petri, 256 seeds, drought, `none`: before peak 1.135, retained 1.000, gap 2.132. After peak 0.922, retained 0.665, gap 4.402. The `coordination` knockout is now identical to `none` because the default multiplier is already 1.
- Relocation grid (`results/relocation-summary.json` in `before/` and `after/`): at outside 1.2, drought, elite-exit runs fall from 142/384 to 62/384. At outside 1.6, drought, they fall from 320/384 to 251/384. Old-centre rural retention at outside 1.2, stable, falls from 0.992 to 0.886.

## 5.4, 5.5, 5.6 (accounted model): 40 seeds (0 to 39), 110 years

Source: `results/maintenance-compact.md`. Retention is state population at the final year divided by its year-54 value. "Share retention<0.5" is the collapse proxy. Values are mean ± SD across seeds.

Canal floor (5.4), elite spend 0, all reshuffle channels on:

| Config | Regime | Climate | State pop. final | Retention | Share retention<0.5 | Canal final |
|---|---|---|---|---|---|---|
| floor 0.3 (old) | reshuffle | drought | 4913 ± 141 | 0.404 ± 0.012 | 1.00 | 0.300 ± 0.000 |
| floor 0.0 (new) | reshuffle | drought | 4913 ± 141 | 0.404 ± 0.012 | 1.00 | 0.286 ± 0.007 |
| floor 0.3 (old) | maintenance_only | drought | 8309 ± 235 | 0.684 ± 0.019 | 0.00 | 0.395 ± 0.009 |
| floor 0.0 (new) | maintenance_only | drought | 8309 ± 235 | 0.684 ± 0.019 | 0.00 | 0.395 ± 0.009 |

The floor binds only in the reshuffle-drought case, and there it changes canal condition, not population or retention. Canal floor does not drive the collapse or decline results.

Reshuffle channels (5.5), each run alone and leave-one-out, drought, elite spend 0, canal floor 0:

| Channels on | Retention | Share retention<0.5 | Cum. shortfall kg |
|---|---|---|---|
| none (= maintenance_only) | 0.684 ± 0.019 | 0.00 | 5468246 ± 158573 |
| extraction only | 0.486 ± 0.015 | 0.82 | 6176455 ± 137428 |
| relief only | 0.680 ± 0.016 | 0.00 | 5385268 ± 133690 |
| trust only | 0.583 ± 0.018 | 0.00 | 5381710 ± 158014 |
| grievance only | 0.632 ± 0.019 | 0.00 | 4840759 ± 173110 |
| all four | 0.404 ± 0.012 | 1.00 | 5886031 ± 124041 |
| all minus extraction | 0.518 ± 0.014 | 0.05 | 4734743 ± 135083 |
| all minus relief | 0.401 ± 0.013 | 1.00 | 6086253 ± 138412 |
| all minus trust | 0.496 ± 0.013 | 0.57 | 5973719 ± 121861 |
| all minus grievance | 0.404 ± 0.012 | 1.00 | 5886031 ± 124041 |

Extraction drives the result. The relief cap has no measurable effect in these runs. Grievance has an effect alone but is redundant once extraction is on. Trust is a moderate contributor.

Elite grain spend (5.6), canal floor 0, all channels on:

| Spend s | Use | Maintenance-only, drought: retention | Reshuffle, drought: retention | Reshuffle, drought: share<0.5 | Reshuffle, drought: elite stock final (kg) |
|---|---|---|---|---|---|
| 0 | relief | 0.684 ± 0.019 | 0.404 ± 0.012 | 1.00 | 3315816 ± 99405 |
| 0.1 | relief | 0.901 ± 0.031 | 0.524 ± 0.015 | 0.03 | 1392768 ± 30412 |
| 0.3 | relief | 0.964 ± 0.034 | 0.552 ± 0.015 | 0.00 | 489479 ± 8238 |
| 0.1 | service | 0.684 ± 0.019 | 0.404 ± 0.012 | 1.00 | 3315816 ± 99405 |
| 0.3 | service | 0.684 ± 0.019 | 0.404 ± 0.012 | 1.00 | 3315816 ± 99405 |

Service spend is inert. Unpaid service is 0 in every checked run, so the court's own grain pays the full service bill and the spent elite grain returns to the elite stock. Relief spend changes outcomes; service spend does not.

Stored-run comparison (before, original model) for reference: reshuffle drought retention 0.404, share<0.5 1.00. The new default (floor 0, spend 0.1 relief) gives 0.524 and 0.03. The collapse headline therefore depends on the elite-spend assumption.

## 5.3 Provisioning calibration

Source: `calibrate_provisioning.py`, `results/calibration-provisioning.md`. Periods are parsed from `public/engines/provisioning.js`. 400,000 draws, seed 20261113.

Structural result: the one-logistic population path (5 free parameters, P0 included) accepts zero draws at population ±10% with area ±5%, and at ±10%/±10%, and at ±20%/±10%. The Klassen table implies growth that rises from 0.0083 (838 to 934) to 0.0192 (934 to 981) and then falls to 0.0002 (1147 to 1244) per year, which one logistic cannot produce.

| Tolerance (pop, area) | Accepted | Acceptance rate |
|---|---|---|
| ±10%, ±5% | 0 | 0.000% |
| ±10%, ±10% | 0 | 0.000% |
| ±20%, ±10% | 0 | 0.000% |
| ±25%, ±15% | 86 | 0.021% |
| ±30%, ±20% | 1309 | 0.327% |

Posterior at ±30%/±20% (accepted draws): r median 0.0135 (5th to 95th pct 0.0110 to 0.0162); K median 2.31e5 (1.63e5 to 2.93e5); Amax median 1304 (1213 to 1391). Area is non-monotone in the table (1244 at period 4, 1323 before and after), which a population-driven area rule cannot match within 5%.

## 5.2 Monsoon (no engine change)

`results/monsoon-check.json` recomputes the stored summary from the engine (2000 draws per sensitivity). Declines match the stored counts exactly: 0 / 217 / 1260 / 1657 at 0 / 0.04 / 0.07 / 0.10. Deep collapse never occurs in any draw. Moat loss occurs in 128 draws even at sensitivity 0, so it is not caused by PDSI alone. The unsourced coefficient decides the onset-decline result.

## 5.7 Findings that restate rules

Proposed rewording is in `TEXT_CHANGES.json` (entries for `experiments/learning-round2/RESULTS.md` and `experiments/frontier-allocation/RESULTS.md`). These are the only places found. Site text in `src/data` does not present these as findings.

## Which headline claims survive

- Relocation elite exit ("the court chooses another centre"): does not survive as a default. It needs the 5^0.227 multiplier. At 1, 0/32 drought seeds exit at outside 1.2. It still occurs at outside 1.6 without the multiplier (251/384 drought runs).
- Petri rise and decline: the default now shows decline under stable climate (retention 0.946), not a rise. Drought decline is stronger (0.665).
- Coordination knockout as a causal test: meaningless at default.
- Canal floor: does not drive the collapse result.
- Reshuffle collapse: driven by extraction. Relief cap inert. Survives only with the spend assumption at 0; at 0.1 or 0.3 spend the collapse share falls.
- Monsoon result: decided by the unsourced sensitivity. No decline at 0.
- Provisioning: the simple path does not match the period table within ±20%.

## Test status (node 26 at /opt/homebrew/bin/node; node 16 cannot run `node:test`)

- `node check-translations.cjs`: passes.
- `node test-worlds.cjs`: 47 of 52 pass. Five fail:
  1. `china` hash. Caused by `public/engines/youth.js`, which changed on disk at 23:31, after the session began and not by this review. Not touched here.
  2. `petri` hash pin in `public/evidence.js` (intended engine change). Pin not regenerated; `evidence.js` is outside the editable set.
  3. `relocation` hash pin in `public/evidence.js` (intended engine change). Same reason.
  4. `Petri ledger balances and matched drought coordination knockout changes recovery`. Asserts default drought retention above 0.99 and a knockout effect. Both are the old causal behaviour.
  5. `moving hurdle changes elite exit under the same outside opportunity`. Asserts exit at low moving cost under the default multiplier. Requires the old multiplier.

Items 4 and 5 cannot pass without either changing `tests/` or reverting the 5.1 default. Items 2 and 3 need `public/evidence.js` regenerated (`prepare-evidence.py`). Item 1 needs whoever changed `youth.js` to decide.

## Files

- `sweep-engines.cjs` (5.1, 5.4 petri and relocation sweep and reproduction check)
- `model/accounted_v2.py` and `run_review_maintenance.py` (5.4, 5.5, 5.6)
- `calibrate_provisioning.py` (5.3)
- `check-monsoon.cjs` (5.2)
- `TEXT_CHANGES.json` (5.1 to 5.7 proposed wording, 16 entries; each `old` verified to occur in its file)
- `results/`: all tables and logs; `before/` and `after/`: run-petri and run-relocation outputs
- `original/`: HEAD copies of the six engines and the maintenance-repair folder

Translation work: any changed English key needs zh-Hans, fr and vi entries in `src/data/translations.json`. Not done here, since site text is out of scope.
