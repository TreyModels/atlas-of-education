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

## 4. Gate 1 Phase B — engine repairs (**PENDING: not yet committed at the time of writing**)

This table is the acceptance map; each row is filled with the committed `file:line` once the lane commits.
No Phase-B entry may be marked DONE without (i) the lane's commit hash, (ii) the pytest/invariant result, and
(iii) the Commander's independent re-run.

| # | repair | expected file(s) | closes | status |
|---|---|---|---|---|
| P1 | Explicit gate kinds `open|fixed_bar|quota|contest` + constructor/calendar normalisation + `ValueError` on unknown; `'bar'`→`fixed_bar` deprecation alias | `engine/eduengine/core.py` | D8; review §3.A | PENDING (engine-core) |
| P2 | Persistent state: `k['pid']`, `k['track']`, `k['elite_prize']`, `k['prep_stock']`; `k['elite']` no longer restricted to `m_==nlev-2`; `GATE_SPECS` KR-SINGLE/KR-TRACKED; `values(..., track_state=)`; `gate_prize_dv` | `engine/eduengine/core.py` | D1, D5 (allocation), D6 (pid) | PENDING (engine-core) |
| P3 | Replace `1−exp(−λx^r)`/λ-solve with `contest_math.pl_win_probs` for expected probabilities in `values()` + `E.contest_expected_probs`; realized gate via `pl_realize` from event-keyed stream | `engine/eduengine/core.py` | D2; review §3.B | PENDING (engine-core) |
| P4 | Seat diagnostics + `share_of='applicants'` option; fix zero-seat admission, non-selective contest, double admission noise | `engine/eduengine/core.py`, `engine/eduengine/planning.py` (`gate_accounting`) | D3; review §3.C | PENDING (engine-core) |
| P5 | `EventRNG` (event-keyed streams) + migrate all core/labour draws; policy-invariant covariates | `engine/eduengine/rng.py` (new, 232 L written), `engine/eduengine/core.py`, `engine/eduengine/modules/labour.py` | D6; review §7/reproducibility | PARTIAL (rng.py written; core/labour migration PENDING) |
| P6 | Labour premium audit: per-child `elite_prize` + track earnings premium applied to all applicable incomes (leavers + queuers), raw/direct/composition decomposition series; wage-compression invariance | `engine/eduengine/modules/labour.py`, `engine/eduengine/core.py` | D7; review §3.A/§8 | PENDING (engine-core) |
| P7 | Tutoring ledger split: `res_cost`/`tut_tax`/`tut_outlay`/`gov_tut_tax`, outlay-based cash budget + assertions; `firm_rev` resource-only (double-count fix); additive series (`contest_spend_now` = outlay, `contest_resource_cost`, `contest_tax_paid`, `gov_tut_receipt`, `*_by_q`, `contest_prep_stock_mean`) | `engine/eduengine/modules/tutoring.py` (522 L written) | D4; review §3.A | PARTIAL (written; needs core §6 API to run) |
| P8 | Per-gate `prep_stock` with `contest_prep_depreciation` (rho), annual cap binding `e_t`, positional/learning switches | `engine/eduengine/modules/tutoring.py` + core allocation/consume | D5; review §4 | PARTIAL (written; needs core §6 API) |
| P9 | Deterministic large-n `pl_win_probs` `auto` path (A5) + approximation-error table vs legacy `1−exp` | `engine/eduengine/contest_math.py`, `docs/audit/CONTEST_MATH_*.md` | D2; review §3.B | PENDING (contest-math) |
| P10 | Contractor: GATE_SPECS updated in the 540 runner / canonical spec decision (canonical spec NOT frozen in Gate 1 — Lead open decision) | `papers/shadow-education-contest/code/…` | review §1, §4 | NOT IN GATE 1 (wave 2) |

**Compatibility obligations checked when Phase B lands** (contract §9): `Engine(modules, **params)` unchanged;
unknown params still `KeyError`; `engine/worlds.py`/`experiments.py`/`countries/*` smoke-run; **540 runner unmodified
must run** against the repaired engine (documented numeric delta, no `KeyError`); series additive-only; default config
legacy-neutral (tax 0, depreciation 0, pure positional, no tracking gates) except the honest D2/D6 changes, which are
quantified here when measured; page-level `firm_rev` correction numerically identical at tax 0.

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
| 2026-11-25 | `…` | Gate 1 Phase B engine repairs — **pending** |
