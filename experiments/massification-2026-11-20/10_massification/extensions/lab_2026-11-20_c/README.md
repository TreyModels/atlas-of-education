# Lab battery 2026-11-20_c — five Council-anchored experiments (Y1–Y5)

**Status: DESCRIPTIVE / DESIGN-ONLY — no causal or direction claims; not evidence of policy effects.**
The Synthetic Council (Council-2) adjudicated battery B (`lab_2026-11-20_b`) at brief 017 and — under the new
standing order D89 — issued **five anchored experiments**, each carrying the mandatory 7-field anchoring block
(`08_council/brief_017/SYNTHESIS_017.md` §D). The Lead predeclared them **before running**
(`PRE_DECLARATIONS.md`, sha256 `8b431b672bbc9679dc192e907c1db3b95e22bacad2abd6b377c68e864dc336e1`) and executed
them with DeepSeek Flash workers. The massification phase remains **CLOSED** at
PARTIAL/DESCRIPTIVE/EQUIVALENT (D76); none of Y1–Y5 reopens C1–C4.

| # | experiment | channel | verdict vocabulary | Council rank |
|---|---|---|---|---|
| Y1 | ceiling-residual candidate-account screen (opportunity-cost vs demand-returns) | markets + cohort flows | SUPPORTED / NOT SUPPORTED / UNABLE | #1 |
| Y2 | cross-channel lead-lag constraint (schooling ↔ markets) | schooling ↔ markets | SUPPORTED / NOT SUPPORTED / UNABLE | #4 |
| Y3 | capacity floor-not-ceiling observed check (6 systems) | government | SUPPORTED / NOT SUPPORTED / UNABLE | #3 |
| Y4 | world-society rival false-positive check (null model) | rival comparison (A5b) | DISTINGUISHED / NOT DISTINGUISHED / UNABLE | #2 |
| Y5 | portability design data-completeness audit (CHN/HKG) | cohort flows / scaling | DATA-COMPLETE / BLOCKED-ON-DATA / UNABLE | #5 (drop-first) |

**Artefacts:** `PRE_DECLARATIONS.md` (frozen thresholds), `RESULTS.csv` (one row per experiment),
`FINDINGS.md` (consolidated), `RUN_MANIFEST.json` (hashes, determinism re-runs), `SHA256SUMS.txt`,
and per-experiment dirs `Y1_…/ Y2_…/ Y3_…/ Y4_…/ Y5_…/` (each with `code/run.py`, `results/*.csv`,
`CLUSTER_RESULTS.csv`, `FINDINGS.md`, `RUN_MANIFEST.json`).

**Run:** `"/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python" <Y_dir>/code/run.py`
for each of the five dirs, then `build_battery_c.py` (Lead consolidation + determinism check).

**Data:** on-disk only (`10_massification/data/`, `09_relations/data/`); no external request, nothing sent.
Blocked/HELD data (PSA microdata, WB Enterprise Surveys, annual capacity/enforcement, per-pupil spending,
subnational sector employment) are **not** used and remain awaiting user approval.
