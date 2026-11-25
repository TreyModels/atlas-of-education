# TEST REPORT — Gate 1 invariant status (before → after)

**Owner:** `atlas-commander` (master rollup; lane evidence attributed). **Status: BASELINE RECORDED — AFTER COLUMN
PENDING Phase-B engine commits.** Feed files: `docs/audit/FIRST_FAILURE_REPORT.md` (qa-verifier),
`docs/audit/CONTEST_MATH_VALIDATION.md` + `CONTEST_MATH_APPROX_ERROR.md` (contest-math),
`results/audit/BASELINE_pytest_engine_invariants.log`, `results/audit/BASELINE_manifest.txt`.
**Rule:** no "tests pass" claim without the command and its output; baseline failures are preserved verbatim.

---

## 1. Suites and their role

| suite | file | tests | role | baseline result |
|---|---|---|---|---|
| Engine invariants (contract §11) | `tests/test_engine_invariants.py` + `tests/conftest.py` (qa-verifier) | 27 | the 12 required invariant tests + Directive accounting tests; written **test-first** against `ENGINE_INTERFACE_CONTRACT.md` v1.0 | **7 failed, 12 passed, 8 xfailed (strict), 0 errors** (3.31 s; refreshed on 5f72ef0: 6.41 s) |
| PL reference validation | `tests/test_contest_math.py` (contest-math) | 68 | validates `engine/eduengine/contest_math.py` (exact DP n≤20, deterministic quadrature n>20, MC validation, `pl_realize`) | **68 passed** (13.9 s) at `47f6bd0` |
| Independent 540 migration check | Commander, in progress | 540 runs | post-repair the 540 config must still run (documented numeric delta); no `KeyError`/`TypeError` | baseline established by Gate 0: REPRODUCED SIMULATION, 9,174/9,180 seed values exact |

Environment for every run (host): macOS 26.6.2 arm64, 8 cores; `/Users/treymenefee/neon-boot/venv/bin/python`
3.10.2; numpy 2.2.6, scipy 1.15.3; always `OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1
PYTHONPATH="$PWD/engine"`. Box (if used): 10-CPU cgroup, py 3.10.8 / numpy 1.24.1; box compute frozen during the
legacy run, then ≤8 workers total / ≤4 per lane. **Test 12 was already satisfied on the host** at the corrected cap
(8 tasks, `ProcessPoolExecutor(fork)`, chunksize 1 and 4, full task-order permutation: serial = repeat = chunksize1 =
chunksize4 = shuffled, bit-identical; `QA_WORKERS=4`; commit `5f72ef0`), so no box oversubscription is needed for it.

Baseline provenance: qa-verifier used a **clean `git archive 2f8cfd9` engine** (the shared worktree was not the
unrepaired baseline — engine lanes had uncommitted edits) plus a snapshot of the then-untracked `contest_math.py`
(sha256 `81781ce7…`). Raw log and manifest committed under `results/audit/`.

## 2. BEFORE — the seven present-and-wrong failures (preserved verbatim)

| # | test | observed (baseline) | expected | responsible file:line (pre-repair) |
|---|---|---|---|---|
| F1 | 03 universal seat | max `e_t` = 5.968711 (434/434 admitted) | 0 | `core.py:418` |
| F2 | 07 non-selective gate | awards 0, max `e_t` = 5.968711 | awards>0 or `e_t`=0 | pricing `modules/tutoring.py:97-99`; award path `core.py:428-429` |
| F3 | 08b G9 award persistence | 557 G9 candidates → 0 awards, 4.731047 `e_t`/yr bought | ≥1 persistent award | `core.py:428` (`m_ == nlev-2`) |
| F4 | d2 expected = exact PL | belief `[0.193617, 0.052377]`, ΣP = 0.245994 | `[0.8, 0.2]`, ΣP = 1 | `core.py:178`, `core.py:416-426`; `tutoring.py:112` |
| F5 | d3 seat denominator | declared 0.25, realized admit rate 0.513 (10 seats, 14–25 applicants) | admitted ≤ seats; denominators reported | `core.py:400` (+433/464) |
| F6 | d6 policy-invariant RNG | `fee_public` 0.00 vs 0.15 ⇒ 17/51 cohort-covariate groups differ (first cohort 5) | 0 | `core.py:93/124-127/331/332/408` |
| F7 | d7 gate prize | gate declares `elite_logw`=0.1, paid premium = 0.600000 | 0.1 | `core.py:498-499` |

**API-absent strict xfails (8):** 05b (`contest_weights`/`contest_expected_probs`), 06c (§1.4 series),
08a (`GATE_SPECS`+`k['track']`), 10 (tax/res_cost/tut_tax/gov_tut_tax), 11b (gate kind `open`), ac4/ac5 (§1.4
reporting/reconciliation), ac6 (`k['prep_stock']`; measured lifetime stock 65.971 vs annual cap 6.0).
**Green at baseline (12):** 01, 02, 04, 05a, 06a, 06b, 09, 11a, 12, ac1 (tax revenue 22/22),
ac2 (per-quintile register-exact), ac3 (cohort denominators 3·N).

## 3. Independent Commander checks already run

| check | result |
|---|---|
| `pytest tests/test_contest_math.py -q` on the committed module (`1a6f3d5`) | **68 passed** (13.9 s) — matches lane report |
| `pytest tests/test_engine_invariants.py -q` on the **pristine committed** engine (my own run, pre-`5f72ef0` tests) | 19 failed/1 passed/7 xfailed — superseded by qa's authoritative clean-tree baseline (7F/12P/8xfail); my run was against a **dirty** worktree (expected-fixture RuntimeErrors), recorded only to show the harness worked |
| invariant suite against the **legacy** `research/model-revision-2026-11-25` engine | 7 failed / 10 passed / 10 xfailed — the same F1–F7 rows; legacy fixes close none of them (`docs/audit/harvest/HARVEST.md` §3) |
| Gate-0 540 reproduction (pristine) | 9,174/9,180 seed + 842/846 summary exact vs reference; max abs 3.553e-15 / 4.441e-16 (`GATE0_VERIFICATION.md`) |

## 4. AFTER — pending Phase-B commits

To be filled when `engine-core` (core.py/rng.py/labour.py/planning.py) and `engine-tutoring` (tutoring.py) commit:

1. re-run the full invariant suite (27 tests) on a clean `git archive <commits>` + committed `contest_math.py`,
   same command, record pytest summary and per-test status;
2. per-row AFTER table (F1–F7 + xfail flips + any new failures outside the baseline rows — the most important
   signal, since a repair that breaks a green guard is a regression);
3. explicit statement of which commits were in the tree (all three lanes if available, partial otherwise);
4. my own independent rerun (not the lane's) of the same command, plus the 540 migration check (config must run;
   numeric delta documented in `CODE_CHANGES.md` §4);
5. **Gate-1 verdict** only if: all 12 invariant tests green, no baseline-green regression, tax/outlay identities
   exact, `ΣP = seats` exact, RNG arm-matching test green, 540 config runs, and the 68-test contest_math suite green.

**No AFTER numbers exist yet; any claim of Gate-1 green before this column is filled is premature.**
