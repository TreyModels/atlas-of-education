# Copy provenance and run environment

Auditor: `repo-auditor`. Audit root: `03_audit/`. Nothing under `01_sources/` was modified.

## Sources inspected (read-only)

| Source | Identity available | Status |
|---|---|---|
| `01_sources/massification_project/` | **No VCS metadata** (no `.git`, no `.gitignore`, no exported commit id). `run.py`/model mtimes in the delivered snapshot are 2026-11-20 12:10 (copy time); the paper is "revised October 2026"; results notes are dated Oct 24–25 2026. The handoff's prior docking note (`02cade9d`) is **not verifiable from this copy** — nothing in the tree carries that prefix. | Local snapshot only; provenance = "unstamped local copy, Oct 25–Nov 5 2026 content". |
| `01_sources/atlas-main-55732f4/` | Git worktree, `.git` → `fleet.nosync/atlas/.git/worktrees/atlas-main-55732f4`. `git rev-parse HEAD` = **55732f4728a13adb3aec5173d8bc7f3a4ac7f926**; worktree clean at audit start. | Verified public-main worktree. |

Key SHA-256 of the audited files are in `STOCKTAKE.json` (`source_hashes`). The stored-result hashes for the reported headline tables are also recorded there.

## The model code was executed from the source directories, not copied

`run.py` and `run_triad.py` take `--out`, and every experiment writes only under `--out`.
So massabm/triad were run **in place** with `--out 03_audit/runs/...`; no file under
`01_sources/` is written (`PYTHONDONTWRITEBYTECODE=1` prevents `__pycache__`).

The Atlas engines do **not** accept an output directory (`floorworld_mc.OUT` and
`childworld_mc.OUT` are hard-coded to `<engine>/results`; `relfloor_countries.__main__`
writes beside itself). They were therefore **copied** into `03_audit/scripts/atlas_engine/`
and run there, so their `results/` land inside the audit scope.

## Deviations of the audit copies from source (both are compute caps only)

| Copy | Diff from `01_sources/atlas-main-55732f4/engine/` |
|---|---|
| `scripts/atlas_engine/floorworld_mc.py` | line 81 `with ProcessPoolExecutor() as ex:` → `with ProcessPoolExecutor(max_workers=2) as ex:` |
| `scripts/atlas_engine/relfloor_countries.py` | line 252 `with Pool(os.cpu_count()) as p:` → `with Pool(2) as p:` |

These change only worker count, not arithmetic or seeds. All other copied engine files are
byte-identical to source (hashes in `STOCKTAKE.json`).

## Environment

Local fast-disk venv (not the evicted iCloud `.venv`):
`/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python`
Python 3.11.17, numpy 2.4.6, scipy 1.17.1, pandas 3.1.1, matplotlib 3.11.2, macOS, 8 cores.

Historical stored runs were made on **different versions** (round-2 notes: Python 3.10.2,
numpy 2.2.6, scipy 1.15.3, matplotlib 3.10.9, 7 workers). Any residual mismatch is therefore a
version/replication difference, not necessarily a design difference. No pinned environment file
(`requirements.txt` is unpinned: `numpy>=1.24`, `scipy>=1.10`, `matplotlib>=3.7`) exists in
`massification_project`.

## Compute discipline

`nice -n 10`, per-run `perl -e 'alarm N; exec @ARGV'` timeouts, workers ≤ 2 per run,
small `--reps`. Every command, exit code and wall time is listed in `RUN_LOG.md`.
