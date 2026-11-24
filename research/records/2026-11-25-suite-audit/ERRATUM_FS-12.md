# ERRATUM — FS-12 (suite audit, task-47)

**Record:** `research/records/2026-11-25-suite-audit/` · branch `research/edsystem-audit-2026-11-25` @ `fe9c6ee`.
**Raised by:** task-50 retraction-completeness pass, 25 Nov 2026. Additive; no history rewrite.

## FS-12 is retracted

FS-12 (`results/audit.json` line 457; hard-coded at `scripts/audit_claims.py` lines 299-302) records:

> `"pushout": "engine exit-reason bookkeeping overwritten; decomposition 0/0/0 reported as unusable"`

This is **wrong and is retracted.** The engine is correct: `core.step` deliberately compacts exited children into
`e.exits` and then keeps only survivors; the driver read `e.kids['reason']` **after** that compaction, so every
survivor showed reason -1 and the decomposition read 0/0/0. The defect was the **driver**
(`run_edsystem_multiverse.py`), **not the engine**.

Corrected and regression-tested at `fix/edsystem-exit-reason-2026-11-25` @ `4679ddb` (cut from `b7108da`): see its
`RUN_REPORT.md` §3.8 and `test_exit_reason.py`. The liquidity-vs-choice decomposition is recoverable after the
corrected re-run.

**Surviving unqualified wording (left unmodified as audit evidence):**
- `results/audit.json` line 457 — machine record of the flag;
- `scripts/audit_claims.py` lines 299-302 — hard-coded flag text.

These remain as the record of what the audit asserted; this erratum is the qualification. Cite FS-12's finding as
"driver read bug (not engine), corrected at `4679ddb`", never as "engine overwrites the exit reason".
