# Runner status — supplied runner reproduced against the exact patched engine

**Current status (2026-11-25 14:00 CST): RECEIVED, TESTED, RAN — 540/540 runs, output numerically
identical to the supplied reference to the last floating-point bit.** The exact patched
`engine/eduengine/core.py` + `engine/eduengine/modules/tutoring.py` and the matching runner were received
in the bundle (sha256 `e9cc02c2…` / `da5cd1ee…`), applied on this branch, and the runner was executed
unmodified. See `REPRODUCTION_CF4_2026-11-25.md` for the full record and
`results/hk_korea_comparative_with_cf4.json` for the reproduced output.

**File:** `run_hk_korea_comparative.py`, sha256 `dd0b1d8d1a17e4639e45c1ae085d4efe5be613fde509c62f7a8345170786bcec`
(293 lines). This is the bundle's tested runner and **replaces** the earlier received runner
`da07107c…4926` (5,315 bytes), which was written against a different `Engine` API.

## Verified against the bundle (2026-11-25)

- `run_hk_korea_comparative.py`, `engine/eduengine/core.py`, `engine/eduengine/modules/tutoring.py` and
  `contest_gate.patch` are byte-identical to the bundle files.
- `git diff -- engine/eduengine/core.py engine/eduengine/modules/tutoring.py` is byte-identical to
  `contest_gate.patch`; the patch reverse-applies to the worktree (`worktree = HEAD + patch`).
- `HEAD:engine/eduengine/{core.py,modules/tutoring.py}` equal the same files at `68da16e`, and applying
  the patch to `68da16e` reproduces the bundle engine files exactly.

## Invocation (the runner was not edited)

The runner sets `ENGINE_DIR = os.path.join(ROOT, "engine")` with `ROOT` = the script's directory
(`papers/shadow-education-contest/code`), so that path does not exist; the engine is at the repository
root. The correct import path is supplied by `PYTHONPATH`:

```
cd /Users/treymenefee/neon-boot/wt3/shadow
PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python \
    papers/shadow-education-contest/code/run_hk_korea_comparative.py
```

Result: `Running 540 simulations (18 arms x 30 seeds) on 8 workers... Completed 540 runs in 178.7s`
(exit 0), writing `code/hk_korea_comparative_with_cf4.json` (committed copy: `results/hk_korea_comparative_with_cf4.json`) (sha256 `c1fa0926…2e99`).

## Environment actually used

macOS 26.6.2 arm64, 8 logical cores; Python 3.10.2; **NumPy 2.2.6**
(`engine/requirements.txt` requires `numpy>=1.26`; `research/requirements.txt` `numpy>=1.26,<3`). The
reference output records no Python/NumPy version, so the reference environment cannot be pinned from the
bundle; despite that the run matched the reference up to last-bit floating-point rounding. Details in
`REPRODUCTION_CF4_2026-11-25.md` §2–3.

## Outcome (CF4a/CF4b)

Under the pre-stated Win-Win criterion (spend index < 80 **and** elite Q5 share below baseline, in **both**
jurisdictions), **CF4a fails (Hong Kong elite share +2.28 pp above baseline) and CF4b fails (spend
90.88 HK / 88.04 KR ≥ 80)**. The only arm meeting the criterion is the single effort-cap arm **CF1b**.
Numbers and tables in `REPRODUCTION_CF4_2026-11-25.md` §4. SIMULATION; not empirical.

---

## Earlier static check (2026-11-25 13:32 CST) — superseded

The following analysis was correct for the *committed* engine before the exact patch arrived, and is kept
as the historical record of why the first attempt could not run.

**Verdict then: RECEIVED, NOT RUNNABLE against this repository's engine as committed.** The earlier runner
appeared to target a patched or different `eduengine` API. It was not modified or "fixed" — that would be a
new implementation, not a reproduction of Paper B.

### Static check (what was verified)

- `python -m py_compile` → syntax OK.
- Imports `from eduengine.core import Engine` and `from eduengine.modules.tutoring import TutoringMarket`.

### Compatibility failures of the earlier runner (`da07107c…4926`) against `engine/eduengine/core.py` @ `origin/main` / base `68da16e`

| runner expects | committed engine (pre-patch) |
|---|---|
| `Engine(cfg, modules=[TutoringMarket()], seed=seed)` | `def __init__(self, modules, **params)` — the first positional is the **module list**, not a config dict; `modules=` is already passed, so the call is invalid |
| `e.run()` then `e.history[35:]` | no `history` attribute; the engine records into `self.R` via `record()`/`note()` |
| history keys `tut_k12_rate`, `tut_by_grade`, `tut_by_q`, `tut_spend` | `tut_k12_rate`, `tut_by_grade`, `tut_by_q`, `tut_spend` do not occur in `core.py` |
| gate kind `contest` | zero occurrences of `contest` in `core.py` |
| config keys `N, T, fee_public, y_median, y_sigma, urban_share, subsist, borrow, p_own, p_firm, contest_*` | the engine takes these through `worlds.py` params / `Engine(**params)`; the world/params schema is not the runner's flat config |

### What was needed (now supplied)

1. The **exact patched `engine/eduengine/core.py` and `engine/eduengine/modules/tutoring.py`** — supplied
   in the bundle and applied on this branch (exact files, not a spec).
2. Confirmation of the engine API version the runner was written against — supplied by the same bundle
   (the tested runner targets the patched API).
3. A hash record for the run — the bundle reference output is committed alongside the reproduced JSON
   (`reference/`), with sha256s recorded in `REPRODUCTION_CF4_2026-11-25.md`.
