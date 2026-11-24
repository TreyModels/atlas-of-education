# One-page report — equation test bench (cached-data attempt)

**Outcome: no family reaches SUPPORTED or REJECTED.** The honest results of this bounded attempt are
**UNTESTABLE** (data absent: F1–F8, shared-code ablation, multiverse swap) and **NOT IDENTIFIED** (F9/F10 —
the lagged design returned n=0 on the cached panel; Q1 zero-signal control could not complete because of a
singular-matrix failure in the fold fit). No effect size or benchmark comparison is claimed.

- F9/F10 attempted on `long_run_panel.csv` (Q2 `9a4f586`, sha256 `cd30d7ea…`) with lagged predictors, controls,
  LCO + time splits, persistence/trend/null benchmarks, cluster SE and a 12-variant spec curve; the estimator
  produced **n=0** (degenerate join), so verdict = **NOT IDENTIFIED**, not REJECTED.
- Q1 permutation control **failed to run** (`numpy.linalg.LinAlgError: Singular matrix`, `test_bench2.py:41`);
  no pass/fail can be stated until `pinv`/rank guards and the join are fixed.
- F2/F6 in particular: **UNTESTABLE** — no PTR/teacher/private/finance panel and no lagged growth panel with
  controls in the cached inputs; `x4_panel.csv` is a wide cross-section, not a time panel.
- E8 fee-abolition and PHL K–12 benchmark gates: **UNTESTABLE** — those panels are not in the cached inputs,
  and no live pulls were used.
- Shared-code ablation and multiverse structural swap: **UNTESTABLE in this branch** (no equation model code).
- No causal claims; no invented targets; no SUPPORTED/REJECTED verdicts were asserted.

**Required next:** fix the F9 join + `pinv` guards and rerun (script hash `b8d099ad…`); add the E8/PHL panels from
the repo records if the benchmark gate is wanted; wire the equation model code before (d)/(e) can be tested.
