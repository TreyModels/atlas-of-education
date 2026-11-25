# Gate-architecture grid (Paper A(c)) — X-27 provenance note

**Status: 5,632/5,632 runs complete; aggregation fixed; clean JSON committed.** Engine pin `846c9e0`
(`core.py` `e111397b…8e71`), spec file `e5ddef6b…`, runner code in repo commit `5012ce3` (module-top
`import numpy as np` + `--aggregate-only`); the box copy used for the clean run was a literal `import numpy as np`
insert of the same logic (box runner sha `cbdea3cd…`, recorded in the JSON metadata). **No simulation was re-run.**

## Artefact lineage

| stage | sha256 | note |
|---|---|---|
| first aggregation attempt | — | crashed: `NameError: np` in `h2()` (runner copy lacked module-top numpy) — 5,632 rows already on disk |
| provisional artefact (Lead, `builtins.np` injection, unmodified logic) | `685db398a9e6052446312e6dacfc2b06f09aa809d60b2f2b145e8e6cf2453f40` | 5,632 runs, 176 cells, wall 7.6 s |
| **clean re-run (committed artefact)** | **`bce3da363afbdcfd16052d2c661107dc8c88d082d640625ef1b0b334d8f72638`** | same numbers; sha differs only because `metadata.runner_sha256` changed (`cbdea3cd…`) |
| committed copy | `results/audit/newgen/gate_architecture_results.json` | byte-identical to the clean box JSON |

## Results (Amendment A3)

* **Primary H2** (contest, vac0=.08, `fail='track'`): **+5.0551 pp**, paired-seed bootstrap 95 % CI **[2.4820, 7.9614]**,
  **MDE (CI half-width) 2.7397** → primary met. Δ_cut(S=.25) +5.6170 [3.551, 7.884]; Δ_cut(S=.70) +0.5619.
* Secondary: quota H2 **+0.9915** [0.5675, 1.4893]; stop-sensitivity (contest, fail=stop) **+5.4715** [2.2078, 8.4476];
  per-vac0 Δ_cut curve **+3.105 / +5.055 / +1.145 / +0.325**.
* H1: **+7.9350** [6.9585, 8.9127], Spearman across S **−1.00** (gap widens as seats shrink).
* bar / bar_high exploratory: −0.255 / +0.204 (null), reported with realized-admission caveat below.
* Labels: NEW GENERATION — REPRODUCED SIMULATION; the pre-repair +0.1086 is the AUTHOR-REPORTED baseline, not a target.

## X-29 — realized-admission diagnostics unmet

The pre-registered realized-admission series (`contest_candidates/seats/admitted/applicant_seat_ratio/admit_rate`) are
**NaN in the raw checkpoints**, so they cannot be recovered by re-aggregation. Primary/secondary results are unaffected.
A **diagnostic-only rerun** (same cells, engine series extraction fixed to per-level `nanmean`; labelled
DIAGNOSTIC-ONLY) is scoped at 1,280 contest-cell runs ≈ 35 min at 8 workers and will run **after Pilot-0 finishes**.
No diagnostic numbers are claimed until it lands.

## X-29 diagnostic rerun design (scoped, diagnostic-only)

`design_diag` extraction fixed to **per-level `nanmean`** (`contest_*` series are NaN at non-contest levels; a plain
mean returned NaN). Diagnostic cells = contest architecture only (the only cells with contest-admission series):
S∈{.25,.35,.45,.55,.70} × fee∈{0.19,0.00} × vac0∈{.02,.08,.25,.50} × 32 seeds = **1,280 runs** (bar/bar_high have no
contest gate, so contest-admission series do not apply there; reported as not-applicable rather than NaN). Output:
`results_diag/gate_architecture_diagnostic.json`, labelled **DIAGNOSTIC-ONLY** (no mixing with the X-27 primary/secondary).
Runs after Pilot-0 completes.
