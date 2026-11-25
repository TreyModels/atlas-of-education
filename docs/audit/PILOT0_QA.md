# PAPER C — PILOT-0 QA

**Owner:** qa-verifier · **date:** 2026-11-25 · **mode:** host-only, no box jobs, no microdata off-Mac
**Artefact under audit:** `/root/work/paperC/results` (Paper C Pilot-0 v3, runner
`papers/shadow-education-contest/code/run_paperC_pilot0.py`, engine pin `846c9e0`)
**Status: ARTEFACT UNAVAILABLE → checks BLOCKED.** The box was powered off on 2026-11-24 17:44Z
(`~/neon-boot/box_lease.jsonl`, final `powered_off` entry) and no local copy of `/root/work/paperC/results`
exists on this Mac. A read-only copy was requested from `atlas-commander`; when it lands, run:

```
python3 docs/audit/pilot0_qa.py --results <copy>/results --engine-repo ~/neon-boot/repos/atlas
```

The validator (`docs/audit/pilot0_qa.py`) implements every check below mechanically and prints
PASS/FAIL/BLOCKED per item; this file records the **static code audit** that can be done without the run.

## 1. What the runner commits to (code-authoritative: `run_paperC_pilot0.py`)

| item | contract (code line) | status |
|---|---|---|
| design | 4 regimes × q0 {1.0, 1.2} × p_firm {0.03, 0.08} × seeds 0–7 = **128 runs**, N=1500, base `params.HK.primary` (lines 39–41, 44–49, 168) | recorded in code; **needs artefact** |
| regimes | `market_only` {own_ban .95, pay_ratio .55, monitoring .2, pay_gap}; `own_open_gap` {0, .55, .2, pay_gap}; `own_open_incentive` {0, 1.2, .2, incentive}; `own_open_gap_firm_ban` {0, .55, .2, pay_gap, firm_ban .9} (lines 35–40) | static PASS — matches declared design |
| no-op guard | non-market cells require mean(`withheld`) > 1e-3 **and** mean(`own_share`) > 0.1 across the cell; otherwise `RuntimeError` aborts the pilot (lines ~103–109) | static PASS (guard exists); **needs artefact** for observed values |
| per-run engine sanity | `run_seed` raises if `Engine.unfired_events` non-empty (line 61) | static PASS |
| manifest | `paperC_pilot0_results.json` → `label`, `manifest{status=EXPLORATORY, generation, engine_commit='846c9e0', engine_core_sha256, spec_sha256, runner_sha256, base, regimes, q0_proxy, p_firm, seeds, n_seeds, cells, runs, workers, wall_seconds, notes}`, `summary` (lines 126–155) | static PASS (keys defined); **needs artefact** |
| summary keys | 16 cell keys `"<regime>|q0=|p_firm="`, 23 metrics each with `mean, sd, ci95_lo, ci95_hi, n` (lines 126–142) | static PASS (keys defined); **needs artefact** |
| label | `EXPLORATORY / HYPOTHESIS-GENERATING`, no confirmatory claim, L varied in Pilot-1 (line 33) | static PASS |

## 2. Engine-pin verification (independent, host-side)

| check | result |
|---|---|
| commit `846c9e0` exists in `~/neon-boot/repos/atlas` | **PASS** — `846c9e0a47cd75f211a8b12ace641fbb77731398`, "[gate1a] Mid-run calendar events: … numerics unchanged" |
| `core.py` sha256 at pinned commit | **PASS** — `e111397bd8a50f94e82bb77715f236ee3d5c0bf863a23d84afdf1c6c71fa8e71` (matches the pinned-engine record in `GATE2_PREREGISTRATION.md` A2 and `MODEL_ZOO_DISCRIMINATORS.md`) |
| `docs/audit/canonical_spec.json` file sha256 at pinned commit | `35576fed0c132041f8ddbf60d1177f2734a16c3047047169872c6a261fa7b95f` — note the docs cite a *spec content* sha (`e5ddef6b…`), which is a different quantity; the pilot manifest records the file sha at run time, so compare like-for-like |

## 3. Static-review defects / risks (file:line)

| id | severity | finding |
|---|---|---|
| P1 | medium | **Pin is a label, not an enforced invariant.** `LABEL` and `manifest.engine_commit` hard-code `'846c9e0'` (runner lines 33, 143); the runner never checks `git rev-parse`/`core.py` sha at run time. A stale or dirty engine tree would still be labelled `846c9e0`. QA must verify `engine_core_sha256` in the payload against the pin (the validator does). |
| P2 | low | **No-op guard double-counts rows on resume.** `all_rows = rows_this + [json.loads(l) for l in open(ck)]` (line ~104) counts each newly appended row twice; harmless for the pass/fail decision but the reported guard mean is not the plain cell mean on restart. Guard is a cell-level mean, not per-seed. |
| P3 | low | Guard wording conflates the two conditions (`NO-OP regime … withheld=… own_share=…`), so a failure message does not say which threshold failed; the validator reports both values per cell. |
| P4 | low | Pilot-0 summary CIs are normal-approximation 95% intervals on 8 seeds (line 131), no multiplicity handling. Acceptable for EXPLORATORY but must not be read as confirmatory. |
| P5 | informational | `own_share`/`tut_firm_by_grade` mix contest-prep with firm tutoring (documented contamination note, runner line 25); results are recorded as-is and must carry that caveat. |

## 4. Completion checklist (runs automatically once the copy lands)

| check | expected | status |
|---|---|---|
| A1 payload present (`paperC_pilot0_results.json`) | exists | **BLOCKED — artefact unavailable** |
| A2 engine pin / core sha | `846c9e0`, `e111397b…` verified against git | blocked on A1 (static pin verified §2) |
| A3 design | 16 cells, 128 runs, q0/p_firm/seeds as declared | blocked on A1 |
| A4 recorded regime parameters | match declared design exactly | blocked on A1 (static PASS) |
| A5 seed completeness | 16 `ckpt_*.jsonl`, seeds 0–7 unique per cell, row params match cell | blocked on A1 |
| A6 summary keys | all 16 cell keys, all 23 metrics, `n=8` | blocked on A1 |
| A7 no-op guard fired | 12/12 non-market cells: withheld > 1e-3 AND own_share > 0.1 | blocked on A1 |
| A8 label | EXPLORATORY, no confirmatory/causal claim | blocked on A1 (static PASS) |

**Verdict:** Pilot-0 **cannot be QA-signed off until the run payload is copied from the box** (or the
instance is restarted and the pull is done through the Commander). Static code audit finds the declared
design and no-op guard present and the engine pin genuine, with the P1–P5 risks above; none of the
result-level claims (withheld/own_share values, 128/128 completeness) can be verified without the run
artefacts. No numbers are asserted here from memory; nothing is fabricated.
