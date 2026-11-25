# TEST REPORT (AFTER) — Gate-1 invariant suite on the repaired engine

**Owner:** `qa-verifier` (task-5, Gate 1d) · **programme:** Atlas contest audit v2 · **date:** 2026-11-25
**Status: GATE-1 AFTER GREEN — 27/27 invariant tests pass on the Phase-B engine, on two independent environments.**
Companion file: `docs/audit/FIRST_FAILURE_REPORT.md` (baseline BEFOREs preserved verbatim; AFTER column filled).

## 1. Tree tested (clean archive, never the dirty shared worktree)

| item | value |
|---|---|
| tree | **`git archive 98baf6b engine tests`** |
| Phase-B commits in tree | `f31e176` gate1a — core.py/rng.py/labour.py/planning.py; `6bc8d61` gate1b — tutoring.py; `23a0173` gate1c — committed `engine/eduengine/contest_math.py` |
| branch state | `git diff 98baf6b..bdded9d -- engine/` **empty** at run time (engine content identical to branch tip during the run) |
| tree file sha256 | `engine/eduengine/core.py 72cbddf7d97db85269081ae1c8ab692153c27b0553d4ce59691beab20bbfcb99` · `engine/eduengine/modules/tutoring.py 7a6fd4c33cc2aefcd47da097b47ac7945744cc1adf9dedbb8ab1ec57d8adc2f8` · `engine/eduengine/contest_math.py 23a01730bf939a9e22befa3ca395094a48c5e870fb10901ceb015cddd793a3c8` |
| contract | `docs/audit/ENGINE_INTERFACE_CONTRACT.md` v1.0 + amendments A1–A7 (A7 read for `contest_candidates`) |
| tests | `tests/test_engine_invariants.py` (27 tests) + `tests/conftest.py`, this lane |

## 2. Commands and environment

**Host (authoritative):**

```
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 QA_WORKERS=4 \
PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python \
  -m pytest tests/test_engine_invariants.py -q --tb=short -rxXf
```

macOS arm64, 8 cores, Python 3.10.2, numpy 2.2.6, scipy 1.15.3, pytest 9.2.0.
**Result: `27 passed, 226 warnings in 72.85s`** → `results/audit/AFTER_pytest_engine_invariants.log`.

**Box (cross-environment replication; declared-stack venv — numpy floor met):**

```
cd /root/work/qa && nice -n 10 env OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
QA_WORKERS=5 PYTHONPATH=/root/work/qa/engine /root/work/venv-declared/bin/python \
  -m pytest tests/test_engine_invariants.py -q --tb=short -rxXf
```

10-CPU cgroup (`cpu.max = 1000000 100000`), Python 3.10.8, **numpy 2.2.6, scipy 1.15.3, pytest 9.2.0**
(`/root/work/venv-declared`); 5 worker processes allocated (test 12 caps its own `ProcessPoolExecutor` at
≤4, so ≤4 concurrent workers + 1 pytest parent). `/root/work/modelrev` and `/root/work/gpu` untouched.
**Result: `27 passed, 226 warnings in 56.73s`** → `results/audit/AFTER_box_pytest.log`
(first box run 60.10 s, identical summary; both with the same tree and venv).

## 3. Summary

| | baseline (`2f8cfd9` engine + snapshot contest_math) | **AFTER (`98baf6b`)** |
|---|---|---|
| pytest | `7 failed, 12 passed, 8 xfailed (strict), 0 errors` (6.41 s) | **`27 passed, 0 failed, 0 xfailed, 0 errors`** (72.85 s host / 56.73 s box) |
| present-and-wrong rows F1–F7 | 7 fail | **7 PASS** |
| contract APIs previously absent | 8 strict xfail | **8 PASS** (markers flipped, no XPASS(strict)) |
| baseline-green regression guards | 12 pass | **12 PASS** (no regression) |
| new failures not in F1–F7 | — | **none** |

## 4. Per-row BEFORE → AFTER

BEFORE numbers are the committed baseline (`docs/audit/FIRST_FAILURE_REPORT.md` §1–§2) and are not rewritten.

| # | test | BEFORE (observed) | AFTER | AFTER evidence |
|---|---|---|---|---|
| F1 | `test_03_universal_seat_has_no_positional_marginal_return` | max `e_t` = 5.968711 (434/434 admitted) | **PASS** | contract path `share_of='applicants', share=1.0`: 40 candidates = 40 seats, `P_i = 1.000000000000`, `max e_t = 0` |
| F2 | `test_07_nonselective_gate_creates_no_elite_wage_prize` | awards 0, max `e_t` = 5.968711 | **PASS** | `open` gate with `elite_logw` → `ValueError: gate 0: kind='open' may not carry 'elite_logw'`; open-gate arm: all 56 elite awards come from the contest gate |
| F3 | `test_08b_g9_declared_elite_prize_is_persisted` | 557 G9 candidates → 0 awards, 4.731047 `e_t`/yr bought | **PASS** | 560 G9 candidates → **112** `k['elite']` awards and **112** `elite_prize` holders; `GATE_SPECS` KR-TRACKED track −1/0/1 = 320/364/196, sticky, KR-SINGLE all −1 |
| F4 | `test_d2_expected_probability_matches_exact_pl_reference` | belief `[0.193617, 0.052377]`, ΣP = 0.245994 | **PASS** | `max|P_engine − P_PL| = 5.55e-17`; `ΣP = 5.000000 = seats_eff` (n=40 candidates, 5 seats) |
| F5 | `test_d3_seat_share_is_of_applicants` | declared 0.25, realized admit rate 0.513 | **PASS** | `share_of='applicants'`: mean realized admit rate **0.2500**, worst deviation **0.0000**; applicants/seats/ratio/admit-rate series present |
| F6 | `test_d6_policy_invariant_rng_across_policy_arms` | 51 cohort-covariate groups differ (17 cohorts, first cohort 5) | **PASS** | `fee_public` 0.00 vs 0.15: `pid` sets identical, **0** covariate mismatches (event-keyed RNG) |
| F7 | `test_d7_gate_prize_is_paid_as_declared` | gate declares 0.1 but paid premium = 0.600000 | **PASS** | all 90 winners store `k['elite_prize'] = 0.1` exactly; paid premium = declared prize |
| X1 | `test_05b_engine_expected_probability_monotone_in_own_stock` | API absent (xfail) | **PASS** | `contest_weights(..., stock_override=...)` / `contest_expected_probs`; own-weight and exact-P monotone in own prep stock |
| X2 | `test_06c_reported_expected_seats_sum_to_seats_eff` | API absent | **PASS** | `Σ expected P = seats_eff` (≤1e-6), admitted ≤ candidates, admitted ≤ seats_eff, every contest gate year |
| X3 | `test_08a_g9_track_persists_kr_tracked_vs_single` | API absent | **PASS** | `GATE_SPECS` + `k['track']`; KR-TRACKED places winners/losers and is sticky; KR-SINGLE `track == -1` everywhere; earnings/quality channels fire |
| X4 | `test_10_gross_outlay_reconciles_to_resource_cost_plus_tax` | API absent (D4) | **PASS** | `tut_outlay == res_cost + tut_tax` and `Σgov_tut_tax == Σtut_tax` per year **and** per child-year (22/22 years), `contest_tax_rate=0.25` |
| X5 | `test_11b_zero_effort_contests_match_forced_open_gate` | API absent (D8) | **PASS** | gate kind `open` normalises; zero-prize contest reproduces the forced-open-gate enrolment path bit-identically |
| X6 | `test_ac4_contest_denominators_are_reported` | API absent (D3) | **PASS** | candidates/seats/applicant-seat-ratio/admit-rate/expected-P series finite on all contest gate years |
| X7 | `test_ac5_expected_vs_realized_reconciliation_over_seeds` | API absent (D2) | **PASS** | 30-seed `|admit_rate − mean P|` gap within 4 seed-SE |
| X8 | `test_ac6_prep_stock_follows_depreciation_recurrence` | API absent (D5); lifetime stock 65.971 vs annual cap 6.0 | **PASS** | `k['prep_stock']` shape (880, 4); `(1−rho)·stock + e_t` recurrence and gate consumption hold at rho=0.0/0.25/1.0 |
| G1–G12 | the 12 baseline greens | PASS | **PASS** | unchanged (01, 02, 04, 05a, 06a, 06b, 09, 11a, 12, ac1, ac2, ac3) — see §5 |

## 5. The 12 binding invariants (§11) — final status

| §11 | test | status |
|---|---|---|
| #1 zero elite prize ⇒ zero positional effort | `test_01` | PASS |
| #2 zero effectiveness ⇒ effort cannot raise admission | `test_02` | PASS |
| #3 universal seat ⇒ no positional marginal return | `test_03` | PASS (contract path) |
| #4 seats=1, weights 4:1 ⇒ exact [0.8, 0.2] | `test_04` | PASS (`method='exact'`, atol 1e-12) |
| #5 monotone in own effective input | `test_05a`, `test_05b` | PASS |
| #6 no over-allocation / no ineligible admission | `test_06a`, `test_06b`, `test_06c` | PASS |
| #7 non-selective gate creates no elite prize | `test_07` | PASS |
| #8 G9 track persists | `test_08a`, `test_08b` | PASS |
| #9 annual expenditure respects available funds | `test_09` | PASS (0 child-year violations, 22 years) |
| #10 gross outlay == resource + tax | `test_10` | PASS |
| #11 zero effort reproduces no-contest behaviour | `test_11a`, `test_11b` | PASS |
| #12 parallel/order stability | `test_12` | PASS (host and box) |
| + Directive: tax revenue identity | `test_ac1` | PASS (revenue recomputed from labour stock, 22/22 years) |
| + Directive: per-quintile accounting | `test_ac2` | PASS (register-exact, weighted identities) |
| + Directive: cohort denominators | `test_ac3`, `test_ac4` | PASS (`3·N` completion denominator; contest reporting finite) |
| + Directive: expected-vs-realized reconciliation | `test_d2`, `test_ac5` | PASS |

## 6. Parallel/determinism arm (test 12) — environments and workers

8 independent tasks (seeds 0–3 × contest shares 0.15/0.40); serial run, same-config+seed repeat,
`ProcessPoolExecutor` (fork) with **chunksize 1 and 4**, and a full task-order permutation
(`[5,2,7,0,3,1,6,4]`); all seed rows bit-identical. Worker caps enforced at the corrected, Lead-verified
allocation: host `QA_WORKERS=4` (8 cores), box `QA_WORKERS=5` with the pool capped at 4 and the pytest parent
(10-CPU cgroup, `nice -n 10`, single-thread BLAS). No oversubscription occurred; the earlier 12-worker
plan was withdrawn before any >4-worker run was made.

## 7. Test-side fixes between the first and final AFTER run (no assertion weakened)

1. `test_05a`, `test_05b`, `test_d2`: `pl_win_probs(..., method='exact')` on n=24–40 vectors correctly raises
   above `EXACT_MAX_N = 20` (contract A6). Engine-vs-reference comparisons now use `method='auto'` — the
   contract's single deterministic expected-probability function (exact subset DP for n≤20, validated
   deterministic quadrature above; Gate-1c 68-test validation). The analytic anchor remains `method='exact'`
   at n=2 with atol 1e-12.
2. `test_11b`: the stale `CAPS` gate-kind probe was fixed — it had run a T=8 world, which raised an unrelated
   `KeyError('formal_by_cred')` in `labour.summary()` (too-short world, no exits), and wrongly concluded the
   `open` gate kind was absent. The probe now uses T=18 and checks
   `E.gate_kind(m) == ['fixed_bar', 'contest', 'open']`.

## 8. New failures not covered by the baseline rows

**None.** After the two test-side fixes above, no test fails on the Phase-B tree; no baseline-green guard
regressed.

**Residual risk (documented in contract A7, not a test failure).** For children *not yet in the same-year
sitting cohort*, expected P for a future gate uses the official pool-map approximation (`ENGINE_CORE_AUDIT.md`
§B12). Consequence in the old F1 scenario (`share=1.0` of the cohort, amendment A7 makes this non-universal):
`max e_t` falls 5.968711 → **0.343441** (down 94.2 %) but is not exactly zero, while the binding universal-seat
scenario (`share_of='applicants', share=1.0`) is exact (`P_i = 1`, `e_t = 0`). Wave-2 sensitivity should report
this approximation rather than treat cohort-share `share=1.0` as a universal-admission arm.

## 9. Artifacts

| artifact | path |
|---|---|
| baseline raw log | `results/audit/BASELINE_pytest_engine_invariants.log` |
| baseline manifest | `results/audit/BASELINE_manifest.txt` |
| AFTER raw log (host) | `results/audit/AFTER_pytest_engine_invariants.log` |
| AFTER raw log (box) | `results/audit/AFTER_box_pytest.log` |
| AFTER manifest | `results/audit/AFTER_manifest.txt` |
| BEFORE/AFTER narrative | `docs/audit/FIRST_FAILURE_REPORT.md` |
