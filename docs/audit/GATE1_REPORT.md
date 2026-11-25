# GATE 1 REPORT — Atlas contest audit v2 (Commander sign-off pack)

**Owner:** `atlas-commander`. **Date:** 2026-11-25. **Branch:** `research/contest-audit-v2-2026-11-25`.
**Gate-0:** PASS (signed off, `GATE0_VERIFICATION.md`). **Gate-1:** GREEN subject to the items in §9.
**Evidence taxonomy:** every claim below is **REPRODUCED SIMULATION** unless labelled AUTHOR-REPORTED /
UNRESOLVED / VALIDATED SIMULATION. Nothing here is VERIFIED EMPIRICAL.

## 1. What changed (Gate 1)

Contract: `docs/audit/ENGINE_INTERFACE_CONTRACT.md` v1.0 (`37e78fb`) + amendments A1–A7. Phase A audits:
`ENGINE_CORE_AUDIT.md` (`6403089`), `TUTORING_AUDIT.md` (`fa34409`), `FIRST_FAILURE_REPORT.md` baseline (`6844628`).
Phase B: `engine-core` **`f31e176`** (core.py +928/−169, rng.py new 232 L, labour.py, planning.py) and
`engine-tutoring` **`6bc8d61`** (tutoring.py); `contest-math` **`1a6f3d5` + `47f6bd0`** (contest_math.py + validation);
`qa-verifier` **`5df531d`** (AFTER suite). Full file:line change list and review-finding mapping in
`docs/audit/CODE_CHANGES.md` §4.

## 2. The 12 invariant tests — BEFORE vs AFTER

| suite run | tree | result |
|---|---|---|
| BEFORE (qa, 6844628) | clean `2f8cfd9` (unrepaired) + contest_math snapshot | **7 failed / 12 passed / 8 xfailed** (3.31 s) |
| AFTER (qa, 5df531d) host | clean `git archive 98baf6b` | **27 passed, 72.85 s** |
| AFTER (qa) box declared venv | py3.10.8 numpy 2.2.6 | **27 passed, 56.73 s** |
| AFTER (Commander independent) | fresh `/tmp/gate1-after` from `98baf6b` + qa tests | **27 passed, 112.12 s** |

Per-row: F1 universal seat PASS (max e_t 5.968711→0); F2 non-selective gate PASS (ValueError on open+elite_logw;
0 phantom pricing); F3 G9 persistence PASS (0 awards→112 `elite`+112 `elite_prize`; TRACKED track 320/364/196;
SINGLE all −1); F4 expected=PL PASS (max|ΔP|=5.55e-17, ΣP=seats exactly); F5 seat denominator PASS
(applicants-share realized 0.2500 vs 0.513 before); F6 policy-invariant RNG PASS (0 covariate mismatches vs 51
before); F7 gate prize PASS (paid 0.1 as declared vs 0.600000 before). 8 API xfails now pass; 12 baseline greens
still green; **no new failures**.

## 3. Acceptance checks (Commander, clean `git archive 98baf6b`)

| check | command | result |
|---|---|---|
| engine-core checks | `PYTHONPATH=engine:code python docs/audit/ENGINE_CHECKS.py --runner` | **13/13 PASS** |
| tutoring checks | `PYTHONPATH=engine python docs/audit/TUTORING_CHECKS.py` | **17/17 PASS** |
| PL module | `pytest tests/test_contest_math.py -q` | **68 passed** (13.9 s) |

## 4. Repair inventory (review findings)

* **§3.A KR G9 phantom prize (D1)** → explicit `track_consequence` gates + persistent `k['track']` ∈ {−1,0,1};
  all three consequence channels (learning quality multiplier, later-gate weight bonus, earnings premium) fire in
  both `values()` and realisation; `gate_prize_dv` = `V(track=1)−V(track=0)` from the household recursion — the
  expected prize is the actual transition value. KR-SINGLE vs KR-TRACKED are data (`GATE_SPECS`). Unmodified 540
  config (which declares G9 `elite_logw=0.15` and no track flag) now **delivers** that legacy prize rather than
  pricing a phantom — documented residual (§9).
* **§3.B expected vs realised (D2)** → `1−exp(−λx^r)` and the λ re-solve are deleted; expected P =
  `contest_math.pl_win_probs` on the same-year sitting cohort, ΣP=seats hard-checked; realised draw =
  `pl_realize` with event-keyed uniforms. Expected/realised per gate after repair = **1.0000** (KR G9 0.35/0.35,
  KR G12 0.12/0.12, HK G12 0.23/0.23); pre-repair tracer measured **2.41×** (KR G12 0.292/0.121) and **1.96×**
  (HK G12 0.455/0.232).
* **§3.C seat denominator (D3)** → `share_of ∈ {cohort, applicants}`; per-gate applicants/seats/ratio/admit-rate/
  expected-P diagnostics series + `contest_summary()`; `planning.gate_accounting()`; zero-seat and non-selective
  defects fixed; double admission noise removed.
* **Randomness (D6)** → `rng.py EventRNG` hash-keyed by (seed, replicate, year, shock_type, pid); all core+labour
  draws migrated; same-seed arms share exogenous covariates (0 mismatches; was 51 groups/17 cohorts).
* **Fiscal ledger (D4/D5)** → per-child `res_cost`/`tut_tax`/`tut_outlay`/`gov_tax`; outlay-based budget with
  in-code assertions; `firm_rev` resource-only; per-gate `prep_stock` with `contest_prep_depreciation` (rho=0 =
  legacy undepreciated anchor), annual cap binding, positional/learning switches, rebate policy.
* **Labour (D7)** → prizes applied multiplicatively last (leavers + queuers), per-child `elite_prize`; audit
  decomposition series (raw = direct + composition).

### 4b. Ledger exercised in a real full-size run (not just assertions) — KR + HK Baseline seed 0, repaired engine

| quantity | KR | HK |
|---|---|---|
| outlay identity rel error (`|outlay−(res+tax)|/outlay`) | **0.0** | **0.0** |
| receipts identity rel error (`|Σgov−Σtax|/Σtax`) | **0.0** | **0.0** |
| max contest effort any child-year vs annual cap 6.0 | **6.0** (cap binds) | **6.0** (cap binds) |
| max(extra_spend − `E._cash`) | **−0.000636** (≤0) | **−0.3183** (≤0) |
| `contest_spend_now` (Σ outlay) mean | 7.7767 | present (tax=0 so resource=outlay) |
| series present | contest_spend_now, resource_cost, tax_paid, gov_tut_receipt, expected_p, admit_rate, seats, applicants, expected_seats, admitted | same |
| expected vs realized per gate | G9 0.35/0.35, G12 0.12/0.12 | G12 0.23/0.23 |

## 5. Fresh 540-run reproduction on the repaired engine (REPRODUCED SIMULATION, not calibration)

**Source: box cross-environment run.** The host authoritative full-540 run failed **twice** in the
ProcessPoolExecutor completion phase (all worker compute done, 0 % CPU, no output, stale pipes; see
`GATE1_POOL_HANG_INCIDENT.md` and `HANG_63896.txt`); both were killed and no partial table was ever used. The box
run completed and is labelled explicitly as the migration source.

| item | value |
|---|---|
| tree | clean `git archive 98baf6b` − engine hashes core `72cbddf7…`, rng `ada4a760…`, contest_math `23a01730…`, labour `0ccfb3ce…`, tutoring `7a6fd4c3…`, planning `13d91bc9…` |
| runner | unmodified legacy 540 runner, only `workers = 6` |
| env / wall / exit | box 10-CPU cgroup, `/root/work/venv-declared` py3.10.8 **numpy 2.2.6**, scipy 1.15.3; `Completed 540 runs in 2960.4s`, 540/540, exit 0 |
| output | `results/audit/commander/hk_korea_540_REPAIRED_box98baf6b_2026-11-25.json`, 435,872 B, sha256 **`455649daf2a1e3367820004c3338deb41236991814887c295b6e7a2bb634ec21`** |
| old run (control) | Gate-0 Commander independent pre-repair 540 output, sha256 `722c370bfc00a339174bf3135f12389dbc53d87a7f607639814ebf43056eaf54` |
| host authoritative | **host run failed twice in pool completion; source = box cross-env declared venv** (no silently partial table) |

**Full migration table: `docs/audit/GATE1_MIGRATION_TABLE.md`** (per-arm HK/KR spend index, elite Q5, Q5−Q1 gap,
Q5/Q1 ratio). Headline baseline (30-seed means):

| jur | K-12 spend | participation % | elite Q5 % | Q5−Q1 gap pp | Q5/Q1 ratio | contest effort |
|---|---|---|---|---|---|---|
| HK old→new | 1343.4 → 156.5 (−88.3 %) | 59.1 → 61.9 | 46.36 → 25.01 | 70.63 → 34.76 | 39.81 → 2.47 | 2.192 → 0.042 |
| KR old→new | 1068.1 → 135.0 (−87.4 %) | 57.4 → 58.4 | 36.12 → 22.13 | 68.36 → **29.71** (target 32.1) | 18.01 → **2.11** (target 3.4) | 1.711 → 0.016 |

**Expected-vs-realised decomposition (the driver):** participation is essentially unchanged; contest-prep effort
collapses 98–99 %. Pre-repair the household's expected admission probability was ~2.4× (KR G12: 0.292 vs 0.121) and
~2.0× (HK G12: 0.455 vs 0.232) the realised PL probability; after the D2 repair per-gate expected/realised =
**1.0000** (KR G9 0.35/0.35, KR G12 0.12/0.12, HK G12 0.23/0.23). Contest prep was ~92–94 % of pre-repair K-12
household spending in this config, so the honest re-pricing collapses the spend index. **Conclusion: a large part of
the "540 design lost the Korean calibration" finding is a contest-probability-consistency artefact, not a
parameterisation problem** — REPRODUCED SIMULATION on the repaired engine, uncalibrated, not VALIDATED. Remaining
deviations (gap 29.7 vs 32.1 pp; ratio 2.11 vs 3.4×) still require Gate-2 calibration after the spec is frozen.

**CF4 pre-stated Win-Win verdict flips with the repair** (spend < 80 AND elite Q5 below baseline, both jurisdictions):

| arm | old (pre-repair) | new (repaired, uncalibrated) |
|---|---|---|
| CF1b (cap −50 %) | **TRUE** (only arm) | FALSE (spend 97.21 HK / 99.25 KR) |
| CF3b (ΔV −50 %) | FALSE | TRUE |
| **CF4a (ΔV −50 % + cap)** | FALSE (HK elite 48.64 > 46.36) | **TRUE** (HK 70.58/23.44 < 25.01; KR 72.48/21.47 < 22.13) |
| CF4b | FALSE | FALSE (spend 89.98/105.54) |

The old CF4 failure remains reported; the flip is reported as conditional simulation under the uncalibrated 540
config — not a policy result.

## 6. Gate-0 recap (unchanged)

Host reproduction 9,174/9,180 seed + 842/846 summary values exact vs reference (max abs 3.553e-15 / 4.441e-16);
box 9,164/9,180 + 831/846 (7.105e-15); 56-vs-8-worker bit-identical; registry 87/87 independently re-derived;
`GATE0_REPORT.md` immutable, `GATE0_VERIFICATION.md` signed PASS. 420-run / Paper A Exp1/3/4/5 / GPU outputs remain
AUTHOR-REPORTED / UNRESOLVED.

## 7. P0 GPU-audit track (parallel annex; does not gate Gate 1) — all routed tasks complete

* **task-6 ABC identification** (`5fcee05`, `8281dd9`, `79bc919`): five advertised moments **rank 4/5** at
  1000/1000 prior-box points (structural m_part ≡ ⅔m_g9+⅓m_g12; left-null certificate ≤3.4e-16); 6 active params ⇒
  **2-dim null space**; **44 distinct θ** inside the prior box reproduce the same moments; analytic Jacobian vs FD
  4.3e-6; analytic δ = −0.7537718023763802 (own share 0.68 exact, covariate-free); archived 7/6-param deltas
  69.51 %/66.11 % are inside the 6 pp tolerance (masked an exactly solvable parameter); reduced 5-param/3-moment
  rank 3 ⇒ exactly **two further independent moments required**; Paper A micro-moments give local rank 5/5
  (6/6 unsubstituted) — **LOCAL ONLY**, its Jacobian must be independently computed and must not cite archived ABC
  outputs; the 0.14 urban–rural gap implies a 30.7 pp within-grade G9 gap given the empty G12×urban cell.
* **task-9 general-r Tullock** (`66abc13`, `0f56621`): FOC derived/validated; seats=1 single-prize Tullock == exact PL
  to 1.1e-16; new analytic symmetric anchor x* = rV(n−1)/(n²c) for every r (FOC residual ≤5.6e-17); archived
  r=1-with-r-multiplier formula's fixed point is accidentally right but its **individual response** is wrong by up
  to 0.87 (r=1.5) / 2.68 (r=2.5) effort units under heterogeneity (utility loss up to 0.162/child); for r>1 a corner
  e=0 can be the global best response in 5/24 anchors; archived (r,p) enter only as r/p (1-D, rank 2) — corrected
  exact-PL model separates them. **The archived "100 % Seat-Expansion Paradox" is an S-grid truncation artefact**
  (S stopped at 0.50): corrected surface is an **inverted-U ending at 0**; archived paradox **CONTRADICTED**.
* **task-12 performance** (`d1acdf3`, `1b34d36`): shipped **KEEP-MEMO-ONLY** (result LRU + grid memo), outputs
  **bit-identical to pre-task-12 (max |diff| = 0.000e+00 over 130 fixtures; 68/68 tests)**, end-to-end 1.113×
  (controller measured 1.196× on a superseded build); **2–5× is UNPROVEN** — 405 elemental float32 DP calls are
  93.6 % of runtime and the ≤1e-12 acceptance blocks arithmetic re-association. Levers quantified: tutoring prep
  grid 9→5 ⇒ ~1.7×, 9→4 ⇒ ~2.0×; compiled kernel 5–10× (violates pure-NumPy). Gate-2/3 budget must assume the
  current engine cost (~20.3 CPU-s/HK run, ~41.9 CPU-s/KR run, 540-class ≈ 4.7 CPU-h), not a hoped-for speedup.
* **task-11 GPU execution integrity** (`c114a61`, `307b59c`): corrected harness 18/18 assertions host+box (failing
  job aborts rc=7, no manifest/partial output); `CORRECTED_GPU_EXPERIMENT_MANIFEST.json` (10 experiments, 7/7
  integrity defects); `SCIENTIFIC_CLAIM_LEDGER.md` 36 claims + **P0 annex updated with task-6/9/12 findings**
  (ABC calibration claims, 100 % paradox, Tullock structural map now CONTRADICTED/unvalidated with exact artifacts).
  GPU conclusions remain QUARANTINED; no GPU campaign.
* **task-7/8 DGP + bootstrap** (`01cb4d3`, `9e04236`, `47b342a`, `ffed664`): corrected crossed design → Jacobian
  rank **5/5 in 500/500 populations** (legacy 3/5, min SV exactly 0), recovery RMSE 0.04–0.13 vs legacy 0.58–0.64,
  182,212 accepted + 106,902 posterior-predictive draws retained; bootstrap factorial: FE size 0.052–0.062 vs
  pooled size 0.996–1.000 under a zero-effect null (pooled selftest cannot separate OVB from minority-effect
  leakage), permutation within-invariance 6.66e-16, replacement WCR size 0.025–0.042 and cluster bootstrap
  0.033–0.050 / coverage 0.95–0.97.

## 7bis. Lead sign-off — GATE 1 CLOSED

**GATE 1: GREEN / CLOSED, signed by `lead` 2026-11-25; Gate-1 pack tree `8148998`.**
Accepted in full: Gate-0 PASS (within tolerance; 87/87 registry independently re-derived; box independence; NumPy
caveat operationalised via `/root/work/venv-declared`); Gate-1 repairs; BEFORE `7F/12P/8xf` → AFTER **27/27**
(host 72.85 s, box 56.73 s, Commander independent 112.12 s); `ENGINE_CHECKS` 13/13; `TUTORING_CHECKS` 17/17;
`contest_math` 68/68; real-run ledger identities 0.0 relative error; fresh-540 migration accepted as
REPRODUCED SIMULATION with the exact source label ("box cross-env, declared venv, clean `98baf6b`, 6 workers,
49.3 min, sha256 `455649da…`") and both host failures disclosed; CF4 flip accepted as **conditional simulation**
with the old failure preserved; P0 annex accepted; residual risks accepted; A7 declared. Compute-controller
stand-down acknowledged (`dc3141c`; box idle; ledger sha `bac993cc…`).

**Gate 2 = GO, CONDITIONAL.** Do not launch the campaign until: (a) operator decides the canonical spec; (b) runner
hardening (`task-13`, audit-runner) reports; (c) the A7 residual is declared in the Gate-2 plan. Preparation (no
runs) is in `docs/audit/GATE2_PLAN.md` and `docs/audit/GATE2_BENCHMARK_REGISTRY.csv`.

## 8. Compute record

10-CPU cgroup (`cpu.max=1000000 100000`); 56/80-worker rule void. Declared-stack venv `/root/work/venv-declared`
(numpy 2.2.6) in use; `docs/audit/system_box_venv.txt`. Controller allocations: qa ≤3-5, contest ≤3, audit 0-1,
commander 0-1, total ≤10; legacy `/root/work/modelrev` tenant retired 15:05:19 after repeated relaunches (outputs
harvested as AUTHOR-REPORTED/PRE-REPAIR in `docs/audit/harvest/`).

## 9. Residual risks / not established

1. **A7 pool-map approximation**: future-gate expected P uses the current sitting cohort's probability curve
   (interpolated); cohort-share `share=1.0` is no longer literally universal (max e_t 5.97→0.343), use
   `share_of='applicants'` for universal arms. 2. **Unmigrated modules** (`schools.py`, `anchor.py`) still use the
   legacy sequential RNG → residual path dependence. 3. **Quota CDF unchanged** (fixed_bar/quota expected P still
   normal-CDF at lagged cutoff; not PL) — contract scoped. 4. **Legacy G9 premium now delivered in the unmodified
   540 run** (540 config declares it; not the canonical repaired spec). 5. **Canonical spec not frozen** (420 vs
   540; Lead decision) — Gate-1 numbers are conditional on the 540 config. 6. **Runtime**: repaired 540 ≈20–30 min
   at 8 host workers (PL evaluations); wave-2 calibration must budget for it / optimise. 7. **420 generation, Paper A
   Exp1/3/4/5, GPU outputs** remain AUTHOR-REPORTED/UNRESOLVED. 8. No calibration/policy claim is made; the
   540-migration improvement is REPRODUCED SIMULATION, not VALIDATED and not a recalibration. 9. **Engine runtime /
   Gate-2 budget**: repaired engine ≈20.3 CPU-s/HK run, ≈41.9 CPU-s/KR run (540-class ≈ 4.7 CPU-h); 93.6 % of runtime
   is the PL quadrature; task-12 memo-only gives 1.113× (bit-identical) and 2–5× is UNPROVEN. 10. **ProcessPool
   completion-phase hang**: observed twice on the host (all worker compute done, 0 % CPU, workers gone/reparented,
   stale pipes, blocked in pymain/thread lock, no output), killed both times; not reproduced in 10 bounded trials of
   the orchestration path; **loud, not corrupting** (no partial table used); hardening required in wave 2 =
   incremental checkpointing, process-group kill semantics (macOS spawn workers reparent to PID 1), memory-aware
   worker caps on the 8 GiB host, collection-phase watchdog. Host run failed twice → migration source is labelled box
   cross-env. 11. **Gate-1 numbers are from `98baf6b` (pre-task-12)**; task-12's shipped module is bit-identical, so a
   future Gate-1 rerun is numerics-unchanged and ~1.11× faster.

## 10. Go / No-Go for Gate 2

**Gate-1 verdict: GREEN — GO for Gate 2, conditional on the Lead sign-off and the preconditions below.**
Evidence: 27/27 invariants AFTER (host+box+Commander), all 7 before-failures closed with no baseline-green
regression; ENGINE_CHECKS 13/13; TUTORING_CHECKS 17/17; contest_math 68/68; ledger identities exact in a real
KR+HK full-size run; fresh 540 on the repaired engine completed (box cross-env, labelled) with old→new migration
and CF4 flip recorded; contract + amendments A1–A7; complete file:line change log; P0 annex delivered.

**Preconditions before any Gate-2 calibration run:**
1. Lead freezes the canonical spec (420 vs 540) — Gate-1 migration is on the unmodified 540 config, not a spec.
2. Use the declared-stack box venv (`/root/work/venv-declared`, numpy 2.2.6) and the controller's ≤10-worker split;
   budget from the measured cost (~4.7 CPU-h per 540-class job), not from an unproven speedup.
3. Implement wave-2 runner hardening first: incremental checkpointing/atomic assembly, process-group kill semantics,
   collection-phase watchdog; the completion-phase hang is unresolved and has already cost two full runs.
4. Keep the following OUT of Gate 2 until separately validated: GPU/ABC conclusions (QUARANTINED), the 420-run
   generation (AUTHOR-REPORTED), Paper A Exp1/3/4/5 (UNRESOLVED), and any claim that the CF4 flip is a policy result
   (it is conditional simulation under an uncalibrated config).
5. Resolve/declare the A7 cohort-share residual (use `share_of='applicants'` for universal-admission arms).

**No calibration, policy campaign, or GPU work has been run in Gate 1.**
