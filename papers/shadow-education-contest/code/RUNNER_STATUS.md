# Runner status — supplied script does not run against the committed engine

**File:** `run_hk_korea_comparative.py` (received 2026-11-25, sha256 `da07107c…4926`, 5,315 bytes).
**Verdict: RECEIVED, NOT RUNNABLE against this repository's engine as committed.** It appears to target a patched
or different `eduengine` API. It was not modified or "fixed" — that would be a new implementation, not a
reproduction of Paper B.

## Static check (what was verified)

- `python -m py_compile` → syntax OK.
- Imports `from eduengine.core import Engine` and `from eduengine.modules.tutoring import TutoringMarket`.

## Compatibility failures against `engine/eduengine/core.py` @ `origin/main` / base `68da16e`

| runner expects | committed engine |
|---|---|
| `Engine(cfg, modules=[TutoringMarket()], seed=seed)` | `def __init__(self, modules, **params)` — the first positional is the **module list**, not a config dict; `modules=` is already passed, so the call is invalid |
| `e.run()` then `e.history[35:]` | no `history` attribute; the engine records into `self.R` via `record()`/`note()` |
| history keys `tut_k12_rate`, `tut_by_grade`, `tut_by_q`, `tut_spend` | `tut_k12_rate`, `tut_by_grade`, `tut_by_q`, `tut_spend` do not occur in `core.py` |
| gate kind `contest` | zero occurrences of `contest` in `core.py` |
| config keys `N, T, fee_public, y_median, y_sigma, urban_share, subsist, borrow, p_own, p_firm, contest_*` | the engine takes these through `worlds.py` params / `Engine(**params)`; the world/params schema is not the runner's flat config |

Some names the runner's logic assumes do exist (`self.closed`, `self.B`, `exam_sd`, `delta`, `kappa`), so the
script is plausible against a *patched* variant — but that variant is not in this repository and was not supplied.

## What is needed to make Paper B / Exp 7 reproducible

1. The **exact patched `engine/eduengine/core.py` and `engine/eduengine/modules/tutoring.py`** at a named commit
   (a diff or the files), not just `contest_gate_spec.md`.
2. Confirmation of the engine API version the runner was written against.
3. A pre-registration and hash record for the 420-run / 1,640-run runs.

Until then, Paper B's numbers remain **author-reported** (the bundled `results/verified_results_2026_11_25.json`
is a self-reported JSON, not a reproducible run from this tree).
