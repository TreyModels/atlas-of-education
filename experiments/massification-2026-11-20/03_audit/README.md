# 03_audit — code inventory and reproduction audit

Owner: `repo-auditor` (task-2). Scope: this directory only. Audited 2026-11-20.
Sources under `01_sources/` were read, not modified (`PYTHONDONTWRITEBYTECODE=1`; massabm/triad write
only to `--out`; Atlas engines were copied before running).

## Deliverables

| File | What it is |
|---|---|
| `MODEL_INVENTORY.md` | One row per engine (16 rows) + stored-result lineage + missing code paths |
| `REPRODUCTION_MATRIX.md` | 7 headline results: reported vs fresh, delta, design/reps gaps, verdicts |
| `STOCKTAKE.json` | Machine-readable version: sources/hashes, engines, results, provenance, run list |
| `COPY_PROVENANCE.md` | Source identities, what was copied, the exact diffs, environment |
| `RUN_LOG.md` | Every command, exit code, wall time, output path; failures stated |
| `scripts/` | Audit drivers + worker-capped Atlas engine copies (never the source) |
| `runs/` | Fresh outputs: `massabm/`, `triad/`, `floorworld/`, `childworld/`, `relfloor/` |
| `logs/` | Raw stdout/stderr for every execution |

## Headline verdicts (detail and caveats in `REPRODUCTION_MATRIX.md`)

Reproduced with fresh runs:
1. Six-arm floor/race table — all 30 level cells within 0.014; 1 of 6 slopes off by 0.07.
2. Graduate-supply shock (surplus vs competitive) — all 20 shock changes within 0.0063.
3. Gate tutoring shares (93/30/5/35%; bar sweep 3→76%) — every share within 0.01.
4. K-12 reform distribution, as-built variant — aggregate −0.131 vs −0.132; Q1 −0.254 vs −0.258.
5. Floorworld engine + 8-test MC screen — pass rates match the stored 6,000-draw report.

Reproduced at small reps: triad actors' contributions (ordering and size hold; the "4% without
credential screening" cell is fragile — 0.0004 fresh).

Partially reproduced: H2 slope −0.068 fresh vs −0.09 reported (the standalone ablation was not run).

Not run (cost stated in the matrix): 30-rep sets, `audit`/`ablation`, massabm rounds 2–4,
full childworld/relfloor screens, firms/Tilly fits, shadow-abm SMC.

## Biggest provenance gap

The public checkout stores `public/research/massification/parent-runs.csv` (peer-pressure experiment)
with **no generating code anywhere in the delivered material**, and `actor-runs.csv` is an **8-seed
mean** while the paper reports **30-replication medians** (values close, same design, not the same run).
The local `01_sources/massification_project` copy is what makes the paper's own `massabm`/`triad` results
runnable at all; the public `atlas-main` tree does not contain that source (its own `research/ISSUES.md`
says so).

## Reproduction status of sources

- `massification_project`: **no VCS metadata** — provenance is a local snapshot only; the handoff's
  prior docking prefix `02cade9d` cannot be verified here.
- `atlas-main-55732f4`: git worktree, HEAD `55732f4728a13adb3aec5173d8bc7f3a4ac7f926`, clean before and
  after the audit.
