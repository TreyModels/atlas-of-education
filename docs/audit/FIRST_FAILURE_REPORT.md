# FIRST FAILURE REPORT — Gate 1d invariant suite (baseline, pre-repair)

**Lane:** `qa-verifier` (task-5) · **programme:** Atlas contest audit v2 · **date:** 2026-11-25
**Branch:** `research/contest-audit-v2-2026-11-25` · **report owner:** Lead deliverable (written by Gate-1d, relayed by `atlas-commander`)

| item | value |
|---|---|
| suite | `tests/test_engine_invariants.py` (27 tests) + `tests/conftest.py` (fixtures) |
| contract | `docs/audit/ENGINE_INTERFACE_CONTRACT.md` v1.0 @ `37e78fb` (binding §1–§14) |
| baseline engine commit | **`2f8cfd9`** (`git archive HEAD engine tests`; engine unrepaired) |
| baseline tree composition | HEAD archive **+ Gate-1c `engine/eduengine/contest_math.py` snapshot** sha256 `81781ce7d6338e26eb6681d18b07d5c3a6c609976cd94c05075d9a7a26729649` (the module is untracked in the shared worktree; snapshot copied so the baseline is reproducible) |
| why a snapshot tree | four lanes share the worktree; at baseline time `engine/eduengine/modules/tutoring.py` already carried an **uncommitted** Phase-B edit, so the raw worktree was *not* the unrepaired baseline. The snapshot is the pristine pre-repair state and was used for every number below. |
| command (exact) | `OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python -m pytest tests/test_engine_invariants.py -q --tb=short -rxXf` |
| host | macOS arm64, Python 3.10.2, numpy 2.2.6, scipy 1.15.3, pytest 9.2.0 (installed into `neon-boot/venv` for this lane) |
| runtime | **6.41 s** (27 tests; test 12 runs 4 workers on the 8-core host, box per-lane cap 4) |
| raw output | `results/audit/BASELINE_pytest_engine_invariants.log` |
| environment manifest | `results/audit/BASELINE_manifest.txt` |
| **AFTER tree** | **`98baf6b`** (engine-core Phase B `f31e176` + engine-tutoring Phase B `6bc8d61` + committed Gate-1c `contest_math.py` `23a0173`; `git diff 98baf6b..bdded9d -- engine/` empty at run time) |
| **AFTER result** | **27 passed, 0 failed, 0 xfailed, 0 errors** — host 72.85 s (`QA_WORKERS=4`) and box 56.73 s (`QA_WORKERS=5`, declared venv py3.10.8/numpy 2.2.6/scipy 1.15.3) |
| AFTER raw outputs | `results/audit/AFTER_pytest_engine_invariants.log`, `results/audit/AFTER_box_pytest.log` |

## Headline

**BASELINE:`7 failed, 12 passed, 8 xfailed (strict), 0 errors`** in 6.41 s.
**AFTER (Phase B, clean `98baf6b` tree): `27 passed, 0 failed, 0 xfailed, 0 errors`** — host 72.85 s, box 56.73 s.
All seven present-and-wrong rows F1–F7 now PASS, all eight previously-absent contract APIs exist (markers flipped
and now run for real), and **no baseline-green regression** occurred (12/12 greens still green; see
`docs/audit/TEST_REPORT_AFTER.md` for the authoritative per-row table).

* **7 present-and-wrong failures** — live defect in the pre-repair tree, each with an
  observed-vs-expected number and a responsible line (D1/D2/D3/D6/D7 of the contract + two
  invariant-level consequences). These are the ones the Gate-1 repairs must turn green.
* **8 strict xfails** — feature absent from the pre-repair tree, written test-first against the
  contract (§1/§1.4/§2/§4/§5/§6). The xfail conditions are capability probes
  (`tests/conftest.py:CAPS`): they flip to `False` automatically when the lanes land, and a stale
  marker then fails loudly as `XPASS(strict)`.
* **12 green** — regression guards that already hold (analytic PL anchor, monotonicity, funds
  constraint, zero-effect invariance, seat cardinality, eligibility, tax identity, cohort
  denominators, parallel determinism).

## 1. Present-and-wrong failures (must go green after Phase B)

`AFTER` column: filled from the Phase-B tree `98baf6b` (engine-core `f31e176`, engine-tutoring `6bc8d61`,
committed `contest_math.py` `23a0173`); **original baseline numbers are kept verbatim**. **All 7 rows PASS.**

| # | test | invariant / contract | assertion (short) | observed (baseline) | expected | responsible file:line (baseline `2f8cfd9`) | defect | review finding | AFTER |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `test_03_universal_seat_has_no_positional_marginal_return` | §11 #3 universal seat ⇒ no positional marginal return | `max e_t == 0` when every applicant is admitted (share=1.0 of cohort; 434 applicants = 434 awards) | **max e_t = 5.968711** | 0 (tol 1e-12) | `engine/eduengine/core.py:418` (`target_s = min(seats/len(ci), 0.99)`), consumed at `core.py:178` / `tutoring.py:112` | D2 | §3.B expected≠realized | **PASS** — contract path: 40 candidates = 40 seats, `P_i = 1.000000000000` for all, `max e_t = 0` (sitting-cohort contract path; the legacy cohort-share arm is no longer "universal" under amendment A7) |
| F2 | `test_07_nonselective_gate_creates_no_elite_wage_prize` | §11 #7 non-selective gate creates no elite prize | `awards > 0 or e_t == 0` (gate has `fail='drop'`, so it never sets `k['elite']`; `elite_logw=0.60` is still priced into prep) | **awards = 0, max e_t = 5.968711** | awards > 0 (a paid prize exists) **or** e_t = 0 (nothing priced) | priced at `engine/eduengine/modules/tutoring.py:97-99`; award path `core.py:428-429` never fires → premium never paid at `core.py:498-499` | D1/D2 | §3.A phantom prize (generalised: any non-`track` contest) | **PASS** — open gates pay nothing: `ValueError: gate 0: kind='open' may not carry 'elite_logw'`; in the open-gate arm all 56 elite awards come from the contest gate |
| F3 | `test_08b_g9_declared_elite_prize_is_persisted` | §11 #8 G9 track award persists | a Grade-9 contest with `elite_logw=0.15` must leave **some** persistent award on winners (`k['elite']` or `k['elite_prize']`) | **winners' persistent awards = 0**, while **max e_t = 4.731047/yr** was bought for the G9 prize (557 G9 candidates) | ≥ 1 award; expected ≈ 35 % of G9 candidates (share 0.35) | `engine/eduengine/core.py:428` (`and m_ == self.nlev - 2` → G9 index 1 never gets `k['elite']`); pricing at `tutoring.py:97-99` | **D1** | **§3.A confirmed critical** (KR G9 phantom prize) | **PASS** — G9: 560 candidates → 112 `k['elite']` awards and 112 `elite_prize` holders (0 before); GATE_SPECS KR-TRACKED: track −1/0/1 = 320/364/196, KR-SINGLE all −1 |
| F4 | `test_d2_expected_probability_matches_exact_pl_reference` | §11 #4/#5 + §1.3 expected = PL | engine expected probability for a 4:1 / one-seat contest equals exact PL, and ΣP = seats_eff | **belief = [0.193617, 0.052377]** at λ=0.053799; **ΣP = 0.245994** | **[0.8, 0.2]**; ΣP = 1 | `core.py:178` (expected `1−exp(−λx^r)`), λ re-solved at `core.py:416-426`, same form in `tutoring.py:112`; realized gate is Gumbel-max PL at `core.py:406-413` | **D2** | **§3.B confirmed** | **PASS** — `max|P_engine − P_PL| = 5.55e-17`, `ΣP = 5.000000 = seats_eff` (n=40, seats=5) |
| F5 | `test_d3_seat_share_is_of_applicants` | §11 #6 + §1.4 denominators | realised admission rate among **applicants** equals the declared seat share (0.25); cohort-N denominator reported | **realised admit rate = 0.513** (per-year 0.40–0.71); seats/yr = 10; applicants/yr 14–25 (N=40, harsher budget) | 0.25 (±0.05); no applicant/seat/admit-rate series recorded | `core.py:400` (contest `seats = max(round(share*N),1)`), also `core.py:433` (quota) and `core.py:464` (`admit`); reporting absent | **D3** | **§3.C confirmed** | **PASS** — `share_of='applicants'`, share 0.25 ⇒ mean realized admit rate **0.2500**, worst deviation 0.0000 |
| F6 | `test_d6_policy_invariant_rng_across_policy_arms` | §11 #12 / §7 event-keyed RNG | an arm differing only in a **policy parameter** (`fee_public` 0.00 vs 0.15) sees identical exogenous cohort draws `z/a/home` for every person | **51 cohort-covariate groups differ** (17 cohorts; first cohort 5, `z`) | 0 differences | single sequential stream `core.py:93`; cohort draws `core.py:124-127`; conditional path draws `core.py:331-332`, `core.py:394`, `core.py:408`, `core.py:492` | **D6** | new defect frozen by contract §0 (not in REVIEW_RESPONSE) | **PASS** — `fee_public` 0.00 vs 0.15: `pid` sets identical and **0** covariate mismatches (was 51 groups / 17 cohorts) |
| F7 | `test_d7_gate_prize_is_paid_as_declared` | §11 #7 / §8 wage premium | switching the **global** default `elite_logw` 0.0→0.6 must not change the premium paid when the **gate** declares `elite_logw=0.1` | **paid log premium = 0.600000** | 0.1 (tol 1e-9) | `core.py:498-499` (`inc *= exp(p['elite_logw'])` for `k['elite']`; gate prize ignored; no `elite_prize` state) | **D7** | new defect frozen by contract §0 | **PASS** — gate declares `elite_logw=0.1` ⇒ all 90 winners store `k['elite_prize'] = 0.1` exactly (was 0.6 paid) |

### Minimal repro snippets (baseline)

```python
# F1 — universal seat still buys positional effort
from conftest import tracked_run, legacy_gates_g12
E, years = tracked_run(gates=legacy_gates_g12(contest=dict(share=1.0)))
cand = sum(y["candidates"][2] for y in years); assert cand == sum(y["elite_new"] for y in years)
max(abs(v) for v in E.R["contest_e_mean"])        # 5.968711...  expected 0  -> core.py:418

# F2 — priced but never paid (non-track contest gate)
from conftest import build_engine
E = build_engine(gates=legacy_gates_g12(contest=dict(fail="drop")), elite_logw=0.60); E.run()
E.ALL["elite"].sum(), max(abs(v) for v in E.R["contest_e_mean"])   # (0, 5.968711...) -> tutoring.py:97-99

# F3 — G9 award is a phantom (KR-TRACKED semantics missing)
E, years = tracked_run(gates=legacy_gates_g9())
rows = list(years[-1]["rows"].values())
sum(r["elite"] for r in rows)                     # 0  expected > 0   -> core.py:428

# F4 — expected object is not PL
E = build_engine(N=24, T=18, measure_from=6, gates=legacy_gates_g12()); E.run()
lam, r = E.lam_contest[2], E.p["contest_r"]; x = np.array([4**(1/r), 1.0])
1 - np.exp(-lam * x**r)                           # [0.1936, 0.0524]  expected [0.8, 0.2] -> core.py:178

# F5 — seat denominator is the cohort, not the applicants
E, years = tracked_run(gates=legacy_gates_g12(contest=dict(share=0.25)), N=40,
                       subsist=1.1, borrow=0.0, y_median=1.1, y_sigma=0.7)
gy = [y for y in years if y["candidates"][2] > 0]
sum(y["elite_new"] / y["candidates"][2] for y in gy) / len(gy)     # 0.513  expected 0.25 -> core.py:400

# F6 — policy parameter shifts exogenous draws
a = build_engine(gates=legacy_gates_g12(), fee_public=0.00); a.run()
b = build_engine(gates=legacy_gates_g12(), fee_public=0.15); b.run()
# compare sorted a.ALL["z"] vs b.ALL["z"] per cohort: 17 cohorts differ -> core.py:93/124-127/331/408

# F7 — global default overrides the declared gate prize
lo = build_engine(gates=legacy_gates_g12(contest=dict(elite_logw=0.1)), elite_logw=0.0, contest_alpha=0.0, T=20); lo.run()
hi = build_engine(gates=legacy_gates_g12(contest=dict(elite_logw=0.1)), elite_logw=0.6, contest_alpha=0.0, T=20); hi.run()
# mean log income of elite leavers in the first elite-exit year: hi - lo = 0.600000  expected 0.1 -> core.py:498-499
```

## 2. API-absent xfails (written test-first; no defect number until the API exists)

Each marker is `@pytest.mark.xfail(<capability absent>, strict=True, reason="missing API: …")`.
The capability probe is `tests/conftest.py::CAPS`; the marker flips off automatically when the
lane lands. A stale marker (feature present **and** test passing) fails as `XPASS(strict)`.

| # | test | missing API (exact) | contract | responsible defect | baseline state | AFTER (Phase B) |
|---|---|---|---|---|---|---|
| X1 | `test_05b_engine_expected_probability_monotone_in_own_stock` | `Engine.contest_weights/contest_expected_probs` (§6) | §6, §11 #5 | D2 | absent (no PL API in core) | **PASS** — `contest_weights`/`contest_expected_probs` exist; #5b passes with `stock_override` |
| X2 | `test_06c_reported_expected_seats_sum_to_seats_eff` | `contest_candidates`, `contest_seats`, `contest_admitted`, `contest_expected_seats` series (§1.4) | §1.4, §11 #6 | D3 | absent | **PASS** — all §1.4 series present; `ΣP = seats_eff` (1e-6) and admitted ≤ candidates |
| X3 | `test_08a_g9_track_persists_kr_tracked_vs_single` | `core.GATE_SPECS` (KR-SINGLE/KR-TRACKED) + `k['track']` (§2/§3) | §2, §3, §11 #8 | **D1** | absent | **PASS** — `GATE_SPECS` + `k['track']`; KR-TRACKED places 196 on track=1 / 364 on track=0, sticky; KR-SINGLE −1 everywhere |
| X4 | `test_10_gross_outlay_reconciles_to_resource_cost_plus_tax` | `TutoringMarket.defaults['contest_tax_rate']`, `E.yr res_cost/tut_tax/tut_outlay/gov_tut_tax`, `E.R contest_resource_cost/contest_tax_paid/gov_tut_receipt` (§4.1/§4.3) | §4, §11 #10 | **D4** | absent (`tutoring.py:106,135,137,154` book one gross flow; no tax/resource split, `firm_rev` counts gross) | **PASS** — `res_cost/tut_tax/tut_outlay/gov_tut_tax`; identity exact every year (22/22 rows), `Σgov_tut_tax = Σtut_tax` |
| X5 | `test_11b_zero_effort_contests_match_forced_open_gate` | gate kind `'open'` normalisation + `Engine.gate_kind` (§1) | §1, §11 #11 | **D8** | absent (`kind` not `'bar'`/`'contest'` falls through to quota, `core.py:173/190`) | **PASS** — gate kind `open` normalises; zero-prize contest reproduces the forced-open enrolment path |
| X6 | `test_ac4_contest_denominators_are_reported` | `contest_applicant_seat_ratio`, `contest_admit_rate`, `contest_expected_p_mean` (§1.4) | §1.4 | D3 | absent | **PASS** — candidates/seats/ratio/admit-rate/expected-P series all finite on contest arms |
| X7 | `test_ac5_expected_vs_realized_reconciliation_over_seeds` | `contest_admit_rate` / `contest_expected_p_mean` over 30 seeds (§1.4) | §1.4, §3.B | D2 | absent | **PASS** — 30-seed expected-vs-realized gap within 4 seed-SE |
| X8 | `test_ac6_prep_stock_follows_depreciation_recurrence` | `k['prep_stock'][:, m]` + `contest_prep_depreciation` (§2/§5) | §2, §5 | **D5** | absent: one flat scalar `k['contest_e']` = undepreciated lifetime sum; measured max lifetime stock **65.971** vs annual cap `contest_max_e=6.0` (N=40, T=22) — structurally the D5 defect, not itself a contract violation because the contract freezes `rho = 0` as the legacy anchor (§5/A1) | **PASS** — `k['prep_stock']` shape (880,4); recurrence and gate consumption hold at rho=0 and rho=0.25 |

## 3. Green on the baseline (regression guards)

| test | invariant | evidence |
|---|---|---|
| `test_01_zero_elite_prize_yields_zero_positional_effort` | §11 #1 | max e_t = 0 with prize 0; control arm e_t > 0 (non-vacuous) |
| `test_02_zero_effectiveness_effort_cannot_raise_admission` | §11 #2 | `contest_alpha=0` ⇒ e_t = 0 at prices 0.02 and 1.60; identical admissions/enrolment |
| `test_04_exact_pl_two_applicants_one_seat` | §11 #4 | `pl_win_probs([4,1],1,'exact') = [0.8,0.2]` at 1e-12 (Gate-1c module) |
| `test_05a_pl_probability_non_decreasing_in_own_weight` | §11 #5 | reference PL monotone over weight grid for seats 1–3 |
| `test_06a_no_contest_allocates_more_placements_than_seats` | §11 #6 | every gate year: placements ≤ seat cap (10/yr) |
| `test_06b_no_ineligible_applicant_is_admitted` | §11 #6 | 0 of N vocational pupils admitted by an `academic_only` contest; all awards on children with cred ≥ 3 |
| `test_09_annual_expenditure_within_available_funds` | §11 #9 | 0 child-year violations of `extra_spend ≤ E._cash` (22 years) |
| `test_11a_zero_effort_contest_parameters_are_inert` | §11 #11 | `contest_max_e=0` ⇒ arms differing in `alpha`/`price` bit-identical on recorded series |
| `test_12_parallel_and_task_order_stability` | §11 #12 | serial = same-seed repeat = `ProcessPoolExecutor` chunksize 1 and 4 (fork, `QA_WORKERS=4`, 8 tasks, full task-order shuffle) = bit-identical seed rows |
| `test_ac1_tax_revenue_identity` | Directive: tax totals | revenue = `tax_formal·formal + tax_cons·(formal+informal)` every year (22/22), rebuilt independently from the labour earnings stock; `tax_gdp` and `edu_budget = max(edu_share·revenue+aid, floor)` hold; 0 discrepancies |
| `test_ac2_per_quintile_accounting_reconciles` | Directive: per-quintile | every year/quintile: recorded spend mean = register mean (1e-12); Σ_q n_q·mean_q = total; quintile-weighted rate = aggregate rate; quintile population shares = 0.2 ± 1 child |
| `test_ac3_cohort_denominators` | Directive: cohort denominators | `enrolled[t] = Σ att_by_grade[t]` all years; census cells ≤ N and unique per cohort; `completion_cohort` denominator = 3·N (each intended age exactly once); `gross_intake_last` = entrants/N |

## 4. Mapping to the external review (`papers/shadow-education-contest/REVIEW_RESPONSE_2026-11-25.md`)

1. **§3.A “Korea Grade-9 contest has no lasting prize (critical)” — CONFIRMED by measurement.**
   F3: 557 Grade-9 candidates, **0** persistent awards, while households bought **4.73 e_t/pupil-year**
   priced on the declared `elite_logw=0.15`. Anchor `core.py:428` (`m_ == nlev-2`). Also F2 shows the
   same phantom mechanism for any non-`track` contest gate.
2. **§3.B “Expected vs realized probabilities differ” — CONFIRMED.**
   F4: for a 4:1/one-seat contest the household expected object gives `[0.194, 0.052]` (ΣP = 0.246)
   where exact PL is `[0.8, 0.2]` (ΣP = 1). F1 is its behavioural consequence: because λ is solved to
   a **0.99** cap (`core.py:418`), universal admission still leaves a positive effort gradient.
3. **§3.C “Seat-share denominator” — CONFIRMED.** F5: declared share 0.25, realised admission rate
   among applicants **0.513**; seats are a share of the entering cohort (`core.py:400`) and no
   applicant/seat/ratio/admit-rate series exists (X2, X6).
4. **§4 calibration / §1 two-generation results** — no invariant failure is claimed here; the
   suite only checks mechanism identities. Gate-2 owns calibration.
5. **Contract §0 defects not in the review** — F6 (D6 path-dependent RNG), F7 (D7 global-only wage
   premium) and X4 (D4 no resource/tax split) were frozen by the binding contract; they fail/are
   absent exactly as the contract predicts.

## 5. AFTER run (Phase B) — how it was produced + result

1. **Tree:** clean `git archive 98baf6b engine tests` (never the dirty shared worktree) + this lane's
   committed tests. Phase-B commits in the tree: `f31e176` (core/rng/labour/planning, gate1a),
   `6bc8d61` (tutoring, gate1b), `23a0173` (Gate-1c `contest_math.py`); `git diff 98baf6b..bdded9d -- engine/`
   was empty at run time. Tree file hashes: `core.py 72cbddf7…`, `contest_math.py 23a0173…`,
   `tutoring.py 7a6fd4c3…`.
2. **Command (identical to the baseline):**
   `OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 QA_WORKERS=4 PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python -m pytest tests/test_engine_invariants.py -q --tb=short -rxXf`
3. **Result — host:** `27 passed, 226 warnings in 72.85s` (0 failed / 0 xfailed / 0 errors).
   **Result — box** (`/root/work/qa`, declared-stack venv py3.10.8 / numpy 2.2.6 / scipy 1.15.3 / pytest 9.2.0,
   `QA_WORKERS=5`, nice -n 10, 10-CPU cgroup): `27 passed, 226 warnings in 56.73s`.
   Raw logs: `results/audit/AFTER_pytest_engine_invariants.log`, `results/audit/AFTER_box_pytest.log`.
4. **No baseline-green regression:** all 12 tests green at baseline are green in the AFTER run (27/27), so no
   repair broke a guard. No new failure outside F1–F7 occurred once the four test-side issues below were fixed.
5. Authoritative per-row table: `docs/audit/TEST_REPORT_AFTER.md`.

### 5.1 Test-side fixes made between the first and final AFTER run (qa-verifier scope only)

The first Phase-B run (`f31e176` tree) had 4 failures, **all test-side, none engine-side**:

| issue | fix |
|---|---|
| `test_05a`, `test_05b`, `test_d2` called `pl_win_probs(..., method='exact')` on engine candidate vectors of n=24–40 | contract amendment A6 / `contest_math.EXACT_MAX_N = 20`: `method='exact'` correctly **raises** above n=20. The engine-representation comparisons now use `method='auto'` (deterministic: exact subset DP for n≤20, validated deterministic quadrature above — the one contract expected-probability function; see `docs/audit/CONTEST_MATH_APPROX_ERROR.md` / 68-test validation). The analytic anchor `[4,1], seats=1` still uses `method='exact'` at n=2 (tolerance 1e-12). No assertion was weakened. |
| `test_11b` was `XPASS(strict)`: the `CAPS` gate-kind probe was stale | the probe had run `small_contest_engine(T=8)`, which raised an unrelated `KeyError('formal_by_cred')` in `labour.summary()` on very short worlds, so it concluded "gate kinds absent". The probe now builds a T=18 world and asserts `E.gate_kind(m) == ['fixed_bar','contest','open']`; on the repaired tree the marker flips off and the test runs for real (and passes). |

### 5.2 Residual risk observed (documented, not a contract failure)

The legacy cohort-denominator arm `share=1.0` (the *baseline* F1 scenario) is **no longer "universal"** under
contract amendment A7: candidates are the same-year sitting cohort, so this arm has 40 sitting candidates = 40
seats at every gate year, but children **not yet in the sitting cohort** are priced with the documented
future-gate pool-map approximation (`ENGINE_CORE_AUDIT.md` §B12; contract §6 amendment A7 note). In that arm
`max e_t` falls from **5.968711** (baseline) to **0.343441** (one year-group, year 10), and prep stock is
consumed at the gate. The binding invariant #3 scenario — `share_of='applicants'`, `share=1.0` — is exact:
40/40 candidates, `P_i = 1.000000000000`, `max e_t = 0`. Recorded so the approximation is not silently read as
an exact zero; not a test failure and not covered by F1 any more.

## 6. Notes / caveats

* The baseline suite has **0 errors**: every failure is an assertion with a number, so a red test
  cannot be dismissed as an environment problem.
* `test_04`/`test_05a` exercise the Gate-1c reference module only (as the contract requires,
  §11 #4: `pl_win_probs([4,1],1,method='exact')`); the engine-side consistency is F4.
* The baseline tree contains the Gate-1c module whose sha256 is recorded above; when the lane
  commits it, the baseline row for `test_04` remains valid (reference math is a pure function).
* Harness: `tests/conftest.py` provides the §12 fixture contract (`build_engine`,
  `small_contest_engine`, `annual_series`, `two_seed`) plus additive helpers
  (`audited_engine`, `tracked_run`) used only by the accounting/denominator tests. All tests import
  only public engine API (`Engine`, module classes, `E.R/E.kids/E.ALL/E.yr` + §6 methods) and
  `eduengine.contest_math`; `engine/` was never edited by this lane.
