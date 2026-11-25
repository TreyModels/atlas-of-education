# CODE CHANGES — Atlas contest audit v2 (Gate 0 + Gate 1)

**Owner:** `atlas-commander`. **Status: Gate 0 complete; Gate 1 Phase A complete; Gate 1 Phase B IN PROGRESS
(this file is updated as each lane commits — Phase-B rows marked PENDING are not yet landed).**
**Branch:** `research/contest-audit-v2-2026-11-25`. **Rule:** one commit per coherent stage; no rewrite of
committed history; every row cites the review finding it closes.

Review findings referenced: `REVIEW_RESPONSE_2026-11-25.md` §3.A (KR G9 phantom prize), §3.B (expected vs realized
probabilities), §3.C (seat denominator), §4 (540-design calibration), §5 (GPU scripts), §7 (reproducibility).
Defects referenced: **D1–D8** as defined in `docs/audit/ENGINE_INTERFACE_CONTRACT.md` §0.

---

## 1. Gate 0 — evidence and environment (no engine behaviour changed)

| # | change | files | rationale | closes |
|---|---|---|---|---|
| G0.1 | Environment manifests captured verbatim (host + box) | `docs/audit/system_host.txt`, `docs/audit/system_box.txt` | pin the two environments that ran Gate 0: macOS 26.6.2 arm64 M1 8c/8 GiB, py 3.10.2, numpy 2.2.6, scipy 1.15.3; box 80 vCPU Xeon Gold 6248, 251 GiB, RTX 3080 Ti idle, py 3.10.8, numpy 1.24.1, scipy 1.13.1 | review §7 |
| G0.2 | Artifact registry: 87 rows, every sha256 re-derived from immutable commit snapshots | `docs/audit/ARTIFACT_REGISTRY.csv` (correction `25fd953`) | provenance for every paper/engine/GPU/result artifact; the one row that had captured a concurrent Phase-B edit was corrected to the Gate-0 snapshot `b2d213b6…`/10,647 B; Commander re-derived 87/87 rows, 0 mismatches | review §7 |
| G0.3 | Archive-branch inventory: 1,123 entries with git blob sha1 + sha256, MANIFEST 13/13 OK | `docs/audit/ARCHIVE_BRANCH_INVENTORY.csv` | proves the all-in-one archive contents without touching the archive branch | review §7 |
| G0.4 | Legacy 540-run reproduction (host, exact runner unmodified) | `results/audit/hk_korea_comparative_with_cf4_repro_mac_2026-11-25.json` (+ `.sha256`, meta, log) | 540/540 exit 0, 119 s; vs committed 540 JSON `c1fa0926…` bit-identical except `metadata.elapsed_seconds`; vs supplied reference 9,174/9,180 seed + 842/846 summary exact, max abs 3.553e-15 / 4.441e-16 | review §7 |
| G0.5 | Box environment-independence re-run (+ 56-vs-8-worker invariance check) | `results/audit/hk_korea_comparative_with_cf4_repro_box8w_2026-11-25.json`, `…box56w…json`, `compare_box*.json`, `per_field_diff_*.{md,csv}` | box numpy 1.24.1/x86: 9,164/9,180 + 831/846 exact, max abs 7.105e-15, all 2 d.p. figures identical; 56w vs 8w bit-identical | review §7 |
| G0.6 | Commander independent reproduction from a clean `git archive HEAD` | `results/audit/commander/` (run JSON, comparator report, README, SHA256SUMS) | independent lane check: output `722c370b…` differs from audit-runner's host run in exactly `elapsed_seconds`; 11 stored numbers differ from reference out of 10,026 (elapsed + 10 last-bit) | review §7 |
| G0.7 | Gate-0 reports | `docs/audit/GATE0_REPORT.md` (audit-runner, immutable record), `docs/audit/GATE0_VERIFICATION.md` (Commander sign-off) | verdict WITHIN TOLERANCE; 420-run / Paper A Exp 1/3/4/5 / GPU outputs carried as AUTHOR-REPORTED / UNRESOLVED | review §1/§7 |
| G0.8 | `/root/work/venv-declared` on the box with the declared stack (py3.10.8 venv, `engine/requirements.txt` + pytest/pandas/pyarrow/psutil); pip freeze captured | `docs/audit/system_box_venv.txt` (to be committed when install completes), box `/root/work/venv-declared` | box numpy 1.24.1 is below the declared `numpy>=1.26` floor; all future box CPU work (Gate 2/3) must use the declared stack | Gate-0 caveat (b) |

**No engine file was edited in Gate 0.** The pristine tree `~/neon-boot/wt4/repro` was never edited; the reproduced
540 output from the prior window stays the Gate-0 baseline artifact.

---

## 2. Gate 1 — binding interface contract (definitional; no engine behaviour yet)

| # | change | commit / file | rationale | closes |
|---|---|---|---|---|
| C.1 | Publish `docs/audit/ENGINE_INTERFACE_CONTRACT.md` v1.0: gate schema (`open|fixed_bar|quota|contest`, `bar` alias, unknown → ValueError), `track_consequence`/`track_prize`/`track_bonus`, persistent state (`k['pid']`, `k['track']` −1/0/1, `k['prep_stock']` (N,nlev), `k['elite']`, `k['elite_prize']`), KR-SINGLE vs KR-TRACKED pre-registered data, tutoring→core accounting identities, prep-stock depreciation convention, `contest_math` API (deterministic `auto`), `rng.py` EventRNG API, labour audit, backward-compatibility rules, and the 12 invariant-test pass definitions | `37e78fb` | fix the shared API **before** four lanes edit engine files; resolve D1–D8/§3.A–C/§4 in one declared place; amendments A1–A6 recorded | review §3.A, §3.B, §3.C, §7; contract D1–D8 |

Contract amendments (all in §14 of the contract): **A1** `rho` = depreciation rate (`prep_stock ← (1−rho)·prep_stock +
e_t`; rho=0 = legacy undepreciated anchor) — resolves the task-3 acceptance-line contradiction raised by
engine-tutoring; **A2** `k['elite_prize']` persistent per-child prize amount; **A3** `contest_price` stays the
**pre-tax** resource price, new `contest_tax_rate`; **A4** `E.values(..., track_state=None)`; **A5** expected
probabilities must be deterministic (no unseeded MC) — contest-math's draft `auto→MC` rejected; **A6** `exact` may
support a documented cap >12 but must raise beyond it.

---

## 3. Gate 1 Phase A — read-only audits (measured evidence; no engine edits)

| lane | artifact | headline measured facts | closes |
|---|---|---|---|
| engine-core | `docs/audit/ENGINE_CORE_AUDIT.md` (`6403089`) + `ENGINE_core_probe.py`, `ENGINE_gate_trace.py`, `ENGINE_synthetic_gate_checks.py` | KR G9 sets **0** elite flags and receives **51.0 %** of contest-prep spend (21,099.6/41,350.4 wage units) while pricing a phantom prize; KR G12 mean expected P **0.292** vs realized **0.121** (HK 0.455 vs 0.232), first cohorts up to 0.97 vs 0.12; seats = share of births, zero-seat quota admits everyone, double admission noise, in-sample cutoff; Baseline vs CF1a exogenous `z` matched in only 9/20 cohorts (first divergence t=9); elite premium global-only and misses queuers | review §3.A–C; D1, D2, D3, D4, D6, D7 |
| engine-tutoring | `docs/audit/TUTORING_AUDIT.md` (`fa34409`) | contest spend is one `pc·e_opt` flow (`tutoring.py:135`), no resource/tax/outlay split, no receipts; flat undepreciated `k['contest_e']` (`core.py:135/427`, `tutoring.py:136`); tax booked as firm revenue would double-count (`tutoring.py:154`); contest prep never enters learning (pure positional) | review §3.A/§3.B; D4, D5 |
| contest-math | `engine/eduengine/contest_math.py` (387 L draft, later committed) + `tests/test_contest_math.py` (47 tests pass) | independent exact subset-DP top-K PL for n≤20, MC estimator with standard errors, deterministic `pl_realize(weights, seats, u)`; exact 4:1→0.8/0.2 verified; large-n deterministic `auto` still pending (A5) | review §3.B; D2 |
| qa-verifier | `docs/audit/FIRST_FAILURE_REPORT.md` (`6844628`) + `tests/test_engine_invariants.py`, `tests/conftest.py` | test-first baseline on the **pristine committed engine**: **7 failed / 12 passed / 8 xfail(strict)**; the 7 present-and-wrong failures give observed-vs-expected + responsible file:line (see §5) | review §3.A–C; D1–D7 |

---

## 4. Gate 1 Phase B — engine repairs (LANDED at `f31e176` [core] + `6bc8d61` [tutoring]; tip `98baf6b`)

Line numbers are in the committed audit-branch files at `98baf6b`. Each row was independently checked by the
Commander on a clean `git archive 98baf6b` tree (see §4b).

| # | repair | file:line (committed) | closes | status |
|---|---|---|---|---|
| P1 | Explicit gate kinds `open|fixed_bar|quota|contest`, normalised at construction, `'bar'`→`fixed_bar` with a `DeprecationWarning`, unknown/missing kind raises `ValueError`, gate lists re-normalised when a calendar event replaces them | `engine/eduengine/core.py:121-143` (validation), `:298-304` (alias warning), `:980` (runtime guard) | D8 | **DONE** |
| P2 | Persistent state allocated in `add_cohort`: immutable `k['pid']=t*N+arange(N)`, `k['track']` int8 −1/0/1, `k['elite']`, `k['elite_prize']`, `k['prep_stock']` (N,nlev); `k['elite']` no longer restricted to `m_==nlev-2`; `GATE_SPECS` KR-SINGLE/KR-TRACKED; `values(..., track_state=None)`; `gate_prize_dv` from the household recursion | `core.py:93-118` (`GATE_SPECS`), `:540-554` (state), `:568-577` (`values`/`_value_recursion`), `:708` (`gate_prize_dv`), `:923-1000` (gate loop / track placement) | D1, D5 (allocation), D6 (pid) | **DONE** |
| P3 | Delete `1−exp(−λx^r)` + λ re-solve; expected P = `pl_win_probs` (imported from `eduengine.contest_math`) on the same-year sitting cohort, `ΣP=seats` hard-checked; realised draw = `pl_realize(w, seats_eff, u)` with event-keyed `u`; no private PL code left | `core.py:25` (import), `:358-531` (`contest_candidates/seats/weights/expected_probs/_gate_expected_P`), `:944-975` (realisation); λ-solve deleted | D2; review §3.B | **DONE** |
| P4 | Seat denominator: `share_of ∈ {cohort, applicants}`; zero-seat quota no longer admits everyone; double admission noise removed; admission rank-based; per-gate diagnostics series + `contest_summary()` merged into `Engine.run()`; `planning.gate_accounting()` reader | `core.py:374-414` (`contest_seats`), `:1069-1129` (diagnostics), `:1105` (`contest_summary`), `:1191-1200` (`run` merge), `planning.py:122` | D3; review §3.C | **DONE** |
| P5 | `engine/eduengine/rng.py` new: `SHOCK_TYPES` registry + `EventRNG` hash-keyed by (seed, replicate, year, shock_type, pid), vectorised, subset/order-independent; legacy methods for unmigrated modules; all core+labour exogenous draws migrated (cohort covariates, continuation, income shock, gate exam, PL, promotion, anchor, street, queue, labour signal/lottery) | `rng.py:36-92` (`SHOCK_TYPES`), `:108-196` (`EventRNG`), `:198-230` (legacy API); call sites `core.py:540-560`, `:891`, `:944-975`, etc.; `labour.py` signal/lottery | D6 | **DONE** (unmigrated `schools.py`/`anchor.py` draws remain legacy — residual risk) |
| P6 | Labour prize audit: prizes applied **last**, multiplicatively, to every applicable income (leavers + queuers via `k['elite_prize']`/`Q['elite_prize']` and track premium); raw/direct/composition decomposition series; wage-compression invariance test | `engine/eduengine/modules/labour.py:77-90` (queue prize state), `:139-148` (prizes last), `:156-162` (queue carry), `:183-197` (audit decomposition), `core.py:924-960` (prize award) | D7; review §3.A/§8 | **DONE** |
| P7 | Tutoring ledger split: `res_cost`, `tut_tax`, `tut_outlay`, `gov_tax` per child-year; outlay-based cash budget with in-code assertions; `firm_rev` uses **resource cost only** (double-count fix); additive series (`contest_spend_now` = Σ outlay for back-compat, `contest_resource_cost`, `contest_tax_paid`, `gov_tut_receipt`, `*_by_q`, `contest_prep_stock_mean`) | `modules/tutoring.py:63-69` (params), `:72-96` (validation), `:261-266` (ledger arrays), `:326-329` (outlay bound), `:397-409` (assertions), `:411-421` (E.yr ledger), `:459` (`firm_rev` resource-only), `:468-481` (series), `:493+` (summary) | D4; review §3.A/§4 | **DONE** |
| P8 | Per-gate `prep_stock` with `contest_prep_depreciation` (rho = depreciation rate; 0 = legacy undepreciated anchor), annual cap binding `e_t`, positional/learning switches, rebate policy | `modules/tutoring.py:63-69` (params), `:276-292` (decay + accumulation), `:326` (cap), `:390-392` (flow-only `k['contest_e']`); core allocation/consume `core.py:553-554`, `:923-1000`; contract §5/A1 | D5; review §4 | **DONE** |
| P9 | `contest_math.py`: deterministic expected probabilities (exact DP n≤20, Poisson-binomial/exponential-race quadrature above, A5), `pl_realize`, `pl_win_probs_detail`; validation + approximation-error study | `engine/eduengine/contest_math.py` (commit `1a6f3d5`), `docs/audit/CONTEST_MATH_VALIDATION.md`, `CONTEST_MATH_APPROX_ERROR.md` (commit `47f6bd0`) | D2; review §3.B | **DONE** |
| P10 | Canonical-spec migration in the runner / 420-vs-540 freeze | `papers/shadow-education-contest/code/…` | review §1, §4 | **NOT IN GATE 1** (canonical spec not frozen; Gate 2/Lead decision) |

**Compatibility:** all `worlds`/`experiments`/`countries` configs construct and run (checked in `ENGINE_CHECKS.py`
compat item); the unmodified 540 runner's `_run_single` runs on the repaired engine (checked; full fresh 540 run in
§4b); series are additive-only (`firm_rev` resource-cost correction is numerically identical at tax 0); default
params are legacy-neutral (tax 0, rho 0, positional, no tracking gates) except the honest D2/D6 changes, which are
quantified in §4b; `Engine(modules, **params)` unchanged; unknown params still `KeyError`.

### 4b. Independent verification of Phase B (Commander, clean `git archive 98baf6b`)

| check | command | result |
|---|---|---|
| engine-core acceptance checks | `PYTHONPATH="$PWD/engine:$PWD/papers/shadow-education-contest/code" python docs/audit/ENGINE_CHECKS.py --runner` | **13/13 PASS**, exit 0 |
| tutoring acceptance checks | `PYTHONPATH="$PWD/engine" python docs/audit/TUTORING_CHECKS.py` | **17/17 PASS**, exit 0 |
| PL module validation | `pytest tests/test_contest_math.py -q` | **68 passed** (13.9 s) |
| invariant suite (qa, pre-fix of 4 test-side items) | `pytest tests/ -q` | **91 passed, 4 failed** — all 4 test-side (3× `method='exact'` with n>20, correctly raising per A6; 1× stale XPASS-strict CAPS for the now-existing `'open'` kind); qa-verifier fixing its own tests → AFTER column in `TEST_REPORT.md` |
| fixed/committed repair-environment hashes | `git archive 98baf6b` | core.py / rng.py / contest_math.py / labour.py / planning.py / tutoring.py hashes recorded in the Gate-1 report |
| fresh 540 run on the repaired engine | clean archive of `98baf6b`, 6 workers | in progress → results + old-vs-new migration table + expected-vs-realised decomposition in the Gate-1 report |

**Expected-vs-realised decomposition claim under test (Lead ask):** engine-core reports the 540 migration moves KR
Q5−Q1 gap 68.4→30.1 pp, spend ratio 18.1→2.14×, elite Q5 36.7→22.0 %, with the driver being the honest PL
expectation (pre-repair mean expected P ≈ 2.4× realised at KR G12) rather than recalibration. This is
**REPRODUCED SIMULATION on the repaired engine**, not calibration and not VALIDATED; the decomposition and the fresh
hashes are in the Gate-1 report once my run lands.

---

## 5. FIRST-FAILURE table (baseline, pristine committed engine — qa-verifier `6844628`)

Source: `docs/audit/FIRST_FAILURE_REPORT.md`; log `results/audit/BASELINE_pytest_engine_invariants.log`.
Command: `cd <clean archive of 2f8cfd9> && OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1
PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python -m pytest tests/test_engine_invariants.py -q
--tb=short -rxXf` → **7 failed, 12 passed, 8 xfailed (strict), 0 errors, 3.31 s.**

| test (contract §11) | observed | expected | responsible file:line | defect |
|---|---|---|---|---|
| 03 universal seat | max `e_t` = 5.968711, 434/434 applicants admitted | max `e_t` = 0 | `core.py:418` (`target_s = min(…, 0.99)`) | D2 |
| 07 non-selective gate | 0 elite awards yet max `e_t` = 5.968711 | no positional return ⇒ `e_t` = 0 | priced `modules/tutoring.py:97-99`, never set `core.py:428-429` | D1 |
| 08b G9 award (KR) | 557 G9 candidates, 0 awards, 4.731047 `e_t`/yr bought | ≥1 persistent award; effort only where priced | `core.py:428` (`m_ == nlev-2`) | D1 / review §3.A |
| d2 expected≠realized | belief `[0.193617, 0.052377]`, ΣP = 0.245994 | exact PL `[0.8, 0.2]`, ΣP = 1 | `core.py:178`, `core.py:416-426`; `modules/tutoring.py:112` | D2 / review §3.B |
| d3 seat denominator | declared share 0.25, realized admit rate 0.513 (10 seats, 14–25 applicants) | admitted ≤ seats; applicants/seats/rate reported | `core.py:400` (also 433/464) | D3 / review §3.C |
| d6 policy-invariant RNG | `fee_public` 0.00 vs 0.15 ⇒ 17/51 cohort-covariate groups differ (first cohort 5) | all cohort covariates identical for same pid | `core.py:93`, `124-127`, `331`, `332`, `408` | D6 |
| d7 gate prize | gate declares `elite_logw=0.1`; paid premium 0.600000 | paid = declared 0.1 | `core.py:498-499` | D7 |

**API-absent xfail(strict) — expected until Phase B lands (8):** 05b (`contest_weights`/`contest_expected_probs`),
06c (§1.4 series), 08a (`GATE_SPECS`+`k['track']`), 10 (`contest_tax_rate`/`res_cost`/`tut_tax`/`gov_tut_tax`),
11b (gate kind `open`), ac4/ac5 (§1.4 reporting/reconciliation), ac6 (`k['prep_stock']`; measured lifetime stock
65.971 vs annual cap 6.0).
**Green at baseline (12):** 01, 02, 04, 05a, 06a, 06b, 09, 11a, 12 (serial=parallel chunksize 1/4/shuffled),
ac1 tax revenue 22/22, ac2 per-quintile register-exact, ac3 cohort denominators (3·N).

The AFTER column (same tests re-run after Phase B) is appended in `docs/audit/TEST_REPORT.md`; the baseline
failures above are preserved verbatim as the historical record.

---

## 6. Change log (append-only)

| date | commit | stage |
|---|---|---|
| 2026-11-25 | `fa34409` | Gate 1b Phase A: tutoring accounting audit |
| 2026-11-25 | `6403089` | Gate 1a Phase A: engine core/PL/seat/RNG/labour audit |
| 2026-11-25 | `37e78fb` | Gate 1: interface contract v1.0 + box allocation |
| 2026-11-25 | `9536870` | Gate 0: evidence + GATE0_REPORT |
| 2026-11-25 | `48d1670`, `2f8cfd9` | Gate 0: Commander independent run + GATE0_VERIFICATION |
| 2026-11-25 | `25fd953` | Gate 0: registry correction to immutable snapshot |
| 2026-11-25 | `6844628` | Gate 1d: test-first invariant suite + FIRST_FAILURE_REPORT |
| 2026-11-25 | `5ac7a2b` | Gate 0: box 10-CPU cgroup correction recorded in GATE0_REPORT |
| 2026-11-25 | `1a6f3d5` | Gate 1c: deterministic `contest_math` (`pl_win_probs` auto/exact, `pl_win_probs_detail`, `pl_realize`; 62 tests) — engine-core unblocked |
| 2026-11-25 | `…` | Gate 0 addendum: legacy-work harvest (`docs/audit/harvest/`, 25 files, AUTHOR-REPORTED/PRE-REPAIR; invariant suite rejects legacy fixes 7F/10P/10xfail; calibration failure preserved) |
| 2026-11-25 | `6bc8d61` | Gate 1b Phase B landed: tutoring ledger split + per-gate prep stock + switches (17/17 checks) |
| 2026-11-25 | `f31e176` | Gate 1a Phase B landed: gate kinds, KR track consequence, PL expected/realized probabilities, event-keyed RNG, labour prize audit (13/13 checks) |
| 2026-11-25 | `98baf6b` | external GPU-bundle audit recorded + docs corrected; GPU conclusions quarantined (Lead) |
| 2026-11-25 | `28a7d20` | contract amendment A7 (`contest_candidates` = sitting cohort) + dashboard Phase-B verification delta |
| 2026-11-25 | `79bc919`, `5fcee05`, `8281dd9` | P0 task-6 ABC identification audit (rank 4/5, 2-dim null space, analytic δ, reduced-system rank 3) |
| 2026-11-25 | `66abc13`, `0f56621` | P0 task-9 general-r Tullock validation (100 % paradox CONTRADICTED as S-grid truncation; analytic symmetric anchor) |
| 2026-11-25 | `c114a61`, `307b59c` | P0 task-11 corrected GPU harness + experiment manifest + scientific claim ledger (GPU conclusions quarantined) |
| 2026-11-25 | `01cb4d3`, `9e04236`, `47b342a`, `ffed664` | P0 task-7 DGP validation (rank 5/5 in 500/500) + task-8 bootstrap size/power factorial |
| 2026-11-25 | `d1acdf3`, `1b34d36` | P0 task-12 perf: KEEP-MEMO-ONLY shipped, outputs bit-identical, 1.113× (2–5× unproven) |
| 2026-11-25 | `8148998` | **Gate-1 close**: repaired-engine 540 migration table (`GATE1_MIGRATION_TABLE.md`), CF4 flip, honest-P decomposition, Gate-1 report pack, pool-hang incident + stack, P0 annex to claim ledger |


## Re-pin 2026-11-25 (gate1a mid-run calendar events, engine-core `846c9e0`)

* New engine pin: clean `git archive 846c9e0`; `engine/eduengine/core.py` sha256 `e111397bd8a50f94e82bb77715f236ee3d5c0bf863a23d84afdf1c6c71fa8e71`
  (was `72cbddf7…` @ `98baf6b`); `contest_math.py` sha256 `cd7b5ba6cb55d250dfce9479cfd6b3d8dfcd7cf4120208ecd26c4116a0ab38bb` (task-12 version).
* `docs/audit/canonical_spec.json` re-pinned: engine_commit `846c9e0`, engine_file_sha256 refreshed, content sha256
  `280b5d953cb17b9f2d5c08e354b16d58cb66882b77f66464ab87cfc6c9a12932`, file sha256
  `e5ddef6b4ecd04a0e96f480b43a97f0567bed7654ec032c1779c9e20f6beb755`.
* Why: `Engine.apply_calendar` silently accepted events whose `year` never coincides with `start_year + t`; a runner that
  passed a simulation index as `year` got a silent no-op (root cause of the forecast-(e) zero-effect artefact). Fix adds
  `_validate_events` warnings, `E.unfired_events`, `year_t=<t>` event key, cached-param/path-shadow audits, and
  regression tests.
* Evidence: `ENGINE_CHECKS.py` 14/14 PASS; `tests/test_engine_invariants.py` **27 passed** on the pinned tree; numeric
  comparison old vs new (HK baseline, all 46 `tut_k12_rate` values) **max|Δ| = 0.0**; engine-core's 118-series
  signature identical. All pre-re-pin new-generation runs (Paper B, g2a) remain valid and must be labelled with the
  `98baf6b`/`72cbddf7…` pin in their manifests.
