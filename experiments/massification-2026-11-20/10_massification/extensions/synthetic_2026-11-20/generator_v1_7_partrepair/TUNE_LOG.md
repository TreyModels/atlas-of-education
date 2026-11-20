# TUNE_LOG — EXP-18 **PART-REPAIR** (v1.7)

**Nothing was tuned.** This log records every probe, every freeze event, every amendment and
every launch attempt, in order, so that the count-blind and no-fit claims are checkable rather
than asserted. `LABEL: SYNTHETIC` for every number mentioned here; the observed series is
mentioned only to say that it was **not** read by any probe.

## 1. What was read, and when

| when | what | observed file? | count computed? |
|---|---|---|---|
| before freeze | the frozen v1.6 code, `PARAMS.md`, `PRE_DECLARATIONS.md` and **`results/`** (including `observed_path.csv`, which prints the 33 observed values and A10's deviations); the frozen v1.3 code/panel/PARAMS; EXP-16's predecl/arms/results; EXP-17's predecl/results; the Council brief and D142–D149 | **no** — `UNIVERSALIZATION_SERIES.csv` was **not** opened | **no** |
| before freeze | `code/selftest_v17.py` (probe 1, §2) | no | no |
| before freeze | `code/sim_v1_7_partrepair.py --harness-test` (probe 2, §3) | no | no |
| scored run | phase A (demographic input, 2 indicators) then phase C (33 cells, after every arm) | yes, exactly twice | yes, once, at phase C |

**Disclosure.** Reading the frozen v1.6 results meant that this worker saw the observed values
and A10's deviations before freezing. That is declared, not hidden. It changed **no**
parameter, threshold, arm or verdict word: the repair is fully specified by the licence (EXP-16
P1 substituted unchanged), the arms are named by the licence, and the one interpretive choice
(§5) was fixed **by the licence**, not by any number. **No probe of this cell computed the
repaired class's 33-cell count before the freeze** — the falsifier for `FAIL-RE-FIT` /
`VOID (CONTAMINATED-BY-DESIGN)` did not fire.

## 2. Probe 1 — `code/selftest_v17.py` (declared; synthetic only)

Purpose: prove the harness and the repair before freezing, without touching the observed file.
Input: a demographic path **reconstructed from the frozen v1.3 panel** (no observed read).
Output: `_scratch/SELFTEST.json`.

Result (final run, before freeze):

- `harness_identity`: 67 200 cells compared, **0 differing** above 1e-6 relative, max relative
  error **1.27e-9** — the copied frozen code path reproduces the frozen v1.3 panel.
- `repair_in_force`: **45/45** cells — A17's `demand_share` equals the frozen block's own.
- `tier_objects`: finite; at 2018 `unfilled = (0.0, 0.0, 0.564282)`, `queue_ratio =
  (6.923, 4.102, 1.533)` — the floor/middle unfilled margin is closed and the upper one is not.
- `phase_guard_selftest`: **BLOCKED-AS-REQUIRED**.
- It printed **no** observed deviation, **no** cell count and **no** level statement. **(This is
  the probe the predeclaration §8.1 declares.)**

## 3. Probe 2 — `--harness-test` (declared; synthetic only; pre-freeze only)

Purpose: exercise the whole pipeline end to end (arms, panels, scoring, crossings,
representation, guards, writers) before freezing. Input: the reconstructed v1.3 demographic path
plus a **constant 90.0 scoring fixture** in 11 arbitrary years per level — **not** the PHL
series. Output archived under
`_scratch/harness_test_DUMMY_FIXTURE_NOT_A_RESULT/` with a README saying its "count" is
meaningless. The mode **refuses to run** once `FREEZE_RECORD.json` exists.

What it established: all guards hold on their declared column sets (`G2` 0/18 480 after the
scope fix, `G3` 0/53 760, `G4` 0 hits, `G9` 45/45, no-fit 0), the phase guard blocks, and every
writer runs. What it also **found** (and this is why the probe existed): the frozen
`inject_upper` hook sets the upper official admission **after** the over-age top-up has been
computed, so `admitted_overage, enrolment, ger, teachers, ptr` are **not replay-determined**.
The predeclaration's G2 column set was therefore **narrowed, before the freeze**, from 16
columns to the **11 replay-determined** ones, with the other 5 **reported** (counts + mechanism)
rather than asserted. No threshold, arm, parameter or verdict object changed.

## 4. The one interpretive choice (fixed before the run)

The two-tier declaration allocates **adequate places** (`K_H + K_O = seats`) and therefore does
not carry the untiered arm's `phys_cap = 1.15` crowding allowance. The licence moves the
**participation decision only**, so the tier capacity was **kept as built**, and its arithmetic
is reported as a **decomposition** (`results/capacity_decomposition.csv`), not as an arm. **No
alternative capacity value was run and no alternative count exists.** The choice was made from
the licence before any run; it is stated in the predeclaration §4.1.

## 5. Freeze events and amendments (all before the scored run)

1. **Predeclaration written** and hashed; the sha256 embedded in the driver
   (`EXPECTED_PREDECL_SHA`), which refuses to run on a mismatch.
2. **Amendment A (licence evidence).** `partprov_2026-11-20/results/PARTPROV_RESULTS.csv` was
   **rewritten by another process** on disk at 01:31 (sha256 `a8469ac0…` → `24fbd6…`) between
   this cell's reading and its freeze. The predeclaration now **enforces** the **unchanged**
   `PARTPROV_DETAIL.csv` hash plus EXP-16's predeclaration hash, **records** both RESULTS
   hashes, and relies on D149 for the verdict word. **The verdict rows are unchanged** (P1
   15/15, 15/15, 4/15; aggregate `MIXED`). No threshold, arm, parameter or verdict word changed.
3. **Amendment B (guard scope).** G2's column set narrowed from 16 to 11 replay-determined
   columns, with the 5 non-replay columns reported (§3). No threshold, arm, parameter or
   verdict word changed.
4. **Freeze record written three times** (`code/build_v17.py`), each time **before** any scored
   run, and each time invalidated only by a **non-model** fix: the band-scan constructor's own
   literal, the build's lint token list, and the driver's path constants (`MASS`/`PROG`).
   **No edit after the freeze of the scored run.** After the successful run only documentation
   (`FINDINGS.md`, this file) and `SHA256SUMS.txt` were written.

## 6. Launch attempts

| attempt | outcome |
|---|---|
| 1 (harness mode, before freeze) | refused: `declared block != code constants` — EXP-16's rewritten RESULTS hash. Fixed by amendment A. |
| 2 (harness mode) | refused: `AST-OWN-CODE-CLEAN` — the rule did not yet accept the derived `OBSERVED_PATH` name. Fixed in the lint only. |
| 3 (harness mode) | refused: `AST-OWN-CODE-CLEAN` — `path` matched the writers too. Fixed in the lint only. |
| 4 (harness mode) | crashed on a `%`-format arity bug in `no_fit_rows`. Fixed (documentation string only). |
| 5 (harness mode) | **HARNESS-OK**. |
| 6 (scored, first) | `FileNotFoundError` on the **wrong `DATA` path** (`MASS` mis-set to `extensions/`). The open failed **before any byte of the observed file was read**; no arm ran, no count was computed. Fixed the path constants, re-froze (event 4), and ran again. |
| 7 (scored) | **complete**: `PATH-FAILED`, determinism 18/18. **No code change after this run.** |

## 7. No-tuning statement (checkable)

- No parameter value was edited at any point: `git`-less audit = the frozen copies are
  byte-identical (`9c0e7998…`, `70ae8f0e…`) and `PARAMS.md` lists 110 = 110 parameters, 0 new.
- The declared grids were **not** searched: `phys_cap` stays 1.15 and no grid was run; `q_O`
  was **not** moved (D144(5)); no λ was installed.
- No threshold, band, year set, level set, arm or verdict word changed after the freeze of the
  scored run.
- The 26-object no-fit audit returns **0** and the prohibited-band scan returns **0**.
- The scored arm used the **pre-declared** value of every object; the only report-only tables
  (capacity decomposition, upper structural sensitivity) are arithmetic on A17's own panel and
  change nothing.
