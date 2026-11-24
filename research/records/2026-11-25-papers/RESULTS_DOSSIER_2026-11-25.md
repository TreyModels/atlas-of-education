# RESULTS DOSSIER — 25 Nov 2026

Every quantitative result produced by this programme, with its source. Compiled before the AutoDL
instance was released. **Nothing here is edited by hand; each row is traceable to a branch/commit or a
committed artefact.** Simulations are labelled SIMULATION.

## 0. Status
- **QA**: CLEARED by the adversarial gate (`~/neon-boot/QA_GATE_2026-11-25.md`), 16 branches, no FAIL.
- **Box**: all runs pulled host-side; instance released per operator instruction.
- **Papers drafted**: #1 phase transition, #2 massification, #3 silent-failure methods (draft).

## 1. Phase transition — the central result (SIMULATION)

Dense 20×20 grid, 16,000 runs, 20 seeds, gates {bar, quota} (`/root/work/equifinality_phase`,
run by parallel session `lead-nb`; statistics pre-registered in `research/phase-transition-dense-2026-11-25` @ `40159c7`).

| arm / response | J_max | location vac0 | sharpness | verdict |
|---|---|---|---|---|
| **quota / tutoring Q5−Q1 gap** | **11.50** | **0.4005 → 0.5044** (interior) | **18.17** | **SIGNATURE** |
| **quota / gate-fail share** | **12.58** | **0.4188 → 0.5044** (interior) | **23.48** | **SIGNATURE** |
| quota / liquidity exit share | 11.91 | interior | 11.9 | supporting |
| quota / tutoring rate | 24.71 | interior | 31.3 | supporting |
| bar / tutoring gap | 2.88 | edge | 11.5 | PARTIAL |
| bar / gate-fail | 2.86 | interior | 5.3 | PARTIAL |

- Gate contrast bar vs quota, median |Δ tutoring Q5−Q1 gap| = **0.0741** (pre-registered threshold 0.05).
- **Equifinal pairs: 374 descriptive** (our metric, pooled over gates). Largest: completion differs
  **0.26 pp** while tutoring rate differs **20.9 pp** and liquidity exits **15.5 pp**.
  **NOT evidence of equifinality beyond chance**: an exhaustive permutation test on the same grid
  (within-gate metric, 1,000 permutations) gives **176 observed vs 190.5 expected** (SD 15.7, p97.5 221,
  **p = 0.838**) — `research/equifinality-phase-2026-11-25` @ `ab415f2`. Report the count as description
  only.
- Reading: the arms-race boundary exists **only when the gate binds**, on the formal-vacancy axis at
  ≈0.40–0.50 vacancies per cohort entrant. The `bar` gate is non-binding in-engine (gate-fail ≤1.3%).

Quick grid (10×10×5, pre-registered `408aa3e`) had returned ABSENT: bar J_max 2.58/2.02, C = 0.48.
Record `research/phase-transition-2026-11-25` @ `f1c16f1`, with `REPRODUCTION_STATUS`.

### 1b. Binding-gate sweep (pre-registered `37cbe3d`; 1,800 runs)

| seat share S | mean Q5−Q1 tutoring gap | E8 fee effect on gap (fee .19 vs .00) |
|---|---|---|
| 0.25 | 0.4419 | −0.0544 |
| 0.35 | 0.4349 | −0.0603 |
| 0.45 | 0.4238 | −0.0615 |
| 0.55 | 0.3969 | −0.0693 |
| 0.70 | 0.3426 | −0.0583 |
| high-bar arm (thresholds 14–17) | 0.2308 | −0.2076 |

- **H1 SUPPORTED**: gap rises monotonically as seats shrink, Spearman ρ = **−1.00**, gap difference
  **+9.9 pp** (S=0.25 vs S=0.70).
- **H2 (primary, fee × scarcity interaction) UNDERPOWERED**: **+0.0039**, 95% CI [−0.019, +0.027].
  Fee abolition raises the gap in every arm (negative fee effect), but no detectable differential.
- High-bar arm compresses the gap to 0.231 — the **form** of the binding gate matters.

### 1c. Auditor's three quoted numbers, checked

| claim | result |
|---|---|
| gates η²(skill_premium) = 42.4% | **42.42%** ✓ (n=720, competitive arm) |
| learning η²(formal_rate) = 77.8% | **77.83%** ✓ (n=720, queue arm) |
| q1 liquidity 70.6%, gate-fail 0.8% | **partial**: liquidity **68.99%** (40-seed mean) / 69.66% (seed 0); gate-fail **1.14±0.18%** direct reason-code read (0.8% is folded into `other_terminal`). Ordering reproduces; decimals do not. |

## 2. eduengine driver correction

- Root cause: `core.step` compacts exited children into `e.exits` and leaves `e.kids['reason']` all −1;
  the driver read `e.kids` → universal liquidity/choice/never = 0/0/0, started_share = 1.0.
- Corrected decomposition, combo 0 (cash_only/fixed_budget/public_only/bar/queue/low_penalty):
  started-liquidity **43.9%**, started-choice **17.3%**; q1 liquidity **68.5%**, choice 10.1%,
  never 14.7%, censored 5.6%; q5 liquidity 0.3%.
- Combo 143 (credit_poverty/fiscal_loop/plus_private_tutoring/quota/competitive/high_penalty):
  started-liquidity **23.4%**, choice **25.6%**; q1 50.1/30.1/0.1/8.6.
- Runs: 1,440-run grid **301 s**; bonus 40-seed 5,760-run grid **214 s**; a concurrent duplicate run
  reproduced rows **byte-identically** (determinism check).
- Branch `fix/edsystem-exit-reason-2026-11-25` @ `4679ddb`; test `test_exit_reason.py` ALL PASS.

## 3. DHS corrected education–fertility gradient (observational)

Authoritative record `research/dhs-corrected-2026-11-25` @ `22de735`; patched re-run
**PASS_BYTE_IDENTICAL** (13/13 outputs, 27/27 anchors, selftest 51 rows, M4 `SurveyType=="DHS"` passed,
76 non-DHS cells excluded; IR individual-level **NOT FEASIBLE**, 0/72 microdata, nothing fabricated).

- Africa-11 2-group ratio **1.0698 [0.9987, 1.1403]** — now includes 1.0 (was [1.011, 1.135]).
- Full-sample 2-group ratio **0.9582 [0.9056, 1.0144]**; 4-level **1.0029 [0.9208, 1.0954]**.
- Q2b1 C_vs_B **−0.1962 (SE 0.0495)** (was −0.0775) → D4 re-read; A_vs_B **+0.0711**;
  higher×cohort **+0.1804 (p=0.030)**.
- **Attribution**: the −0.0775 → −0.1962 move is the **interaction-set change**, not the bootstrap
  multiplicity fix (which moves CIs only). Neon's bootstrap-only diff reproduces ≈ −0.0775.
- Full-sample M1 weighted (860 cells/215 surveys/65 countries): primary **−0.5541** (SE .0588),
  secondary **−1.5837** (.1667), higher **−2.5382** (.2419). Africa-11: −0.7070, −2.1627, −3.1977.
- Uncomputed reference `FE_FRTR_W_GFR` marked never estimated (0 rows) at every site.

## 4. Equation suite (simulated demonstrations; quarantined until patched)

Branch `research/equation-suite-neon-fixes-2026-11-25` @ `575d4cd`. Full `run_all.py` 73.18 s,
10/10 executed, 0 execution failures, **3 RULE_FAIL (eq04/S4 pre-declared, eq06/S6 post-hoc,
eq10/S10 dropped pre-registered rule)**, 11/11 JSON strict-parse, **0 NaN/Infinity** (was 15).

- eq09: TWFE now equals the within transform to **5.4e-15** (base 0.1753 vs 0.2290); 2SLS SE from
  actual-D residuals **0.046350** (base 0.080571 = fitted-D).
- eq07: Gini/Theil on positive level income, decomposition identity holds, 0 NaN.
- eq10: log1p Tobit recovers **1.441 single / 1.370 different** vs truth 0.8 (0.64/0.57 away),
  `tobit_within_0.15_share = 0.0` → dropped S3 rule **FAILS**; `ban_raises_gini` now FALSE
  (ΔGini −0.064…−0.041). S10 sub-flags surfaced in `rule_flags`.
- Framing corrected: only **S4** is a pre-declared FAIL; S6 post-hoc; S10 dropped rule.
- Deviations logged: eq03 2-D (ρ,ω) grid vs prereg 1-D (control run preserved); eq04 q-shadow.

## 5. E6/E8 massification evidence (observational)

Draft packet `research/bulge-arrival-2026-11-25` @ `1b91a71`; Paper #2 draft `papers/paper2_massification_draft.md`.

- E6 (1900–2012, reconstructed mean-years-of-schooling take-off vs structural-change proxies):
  demand-first **10.0–24.1%**, schooling-first **21.5–46.3%** (strict orderings **58.3–71.4%**),
  bounds 6.7–53.0%, weak-tie/left-censored **21–43%**; N3 strict demand-first **0.0–30.8%** across 54
  dating definitions (median 10.45). Auditor's "76–90% / 20–40 years" does **not** reproduce.
- E8 (8 page-located fee abolition dates; 4 unresolved excluded): Callaway–Sant'Anna post
  **+22.12 to +28.56 pp**; on-impact **+12.44** (CI includes 0); pre-trends flat at −2/−3/−4,
  imprecise at −5; placebo **−0.39**; LOO **18.17–26.16**.
- E8 Fisher randomization inference (committed record `research/e8-fisher-ri-2026-11-25` @ `fb8b67e`):
  T_obs **12.4436**, B=10,000; placebo-date p = **9.999e-05**, placebo-country p = **5.999e-04**
  (Tpost 2.9997e-04). *A separate uncommitted run reported 0.0131/0.0004 — not cited; commit it first.*
- **t\*** (abolition + primary length) = **NOT-ESTIMABLE**: `L_primary` sourced 0/8 in-repo, no proxy
  used. Bulge-arrival event study and falsifier therefore NOT-ESTIMABLE, not null.
- E1 context: BY **0/0/0/32** at R=1200 (procedure-dependent; panel inputs not committed;
  regenerable in principle from `sweep.py`+WB API, not bit-reproducible — vintage).

## 6. v6 gate/jobs fixes (SIMULATION)

Branch `research/masseng-gate-jobs-neon-2026-11-25` @ `9d79df1` (7 commits). Fixed:
fractional-mass vacancy clearing (**25 vacancies / two 50-mass cells → formal_share 0.25**; base 1.0 =
4× over-hiring), p_hire ∈ [0,1], quota double-count (channels 1170 → 700 = rejected; 575 + 125),
dashboard fractional share, run_swaps T1b point-biserial + T5 four distinct arms + strict JSON.
Tests: fixed **8/8, 4/4, 3/3, 7/7**; base **1/8, 2/4, 2/3, 3/7**; independent verifier 6/6.
Open (disclosed): `_record()` spend double-count; MNL vs Bray price/option; Tullock invariance
unadjudicable; v6 not wired to `core/runner.py`.

## 7. Test-bench and audit corrections

- Test bench `fix/equation-test-bench-2026-11-25` @ `2c575d9`: F9 lag fixed (n=1,495 / 135 countries /
  5 folds; model RMSE 0.2381 vs persistence 0.2855 vs mean-null 0.2311 → **REJECTED**); `inv` singular
  crash fixed; Q1 permutation 0.15.
- eDSYSTEM tests `fix/edsystem-tests-pinv-2026-11-25` @ `3e35ff0`: supported rows **49 → 45** (4
  `not_estimable`), **45/72** supported, audit strict 5-axis **28/72**; per-cell disclosure 17/45 have
  ≥1 sign flip.
- Quarantine (do not cite): `research/equation-test-bench-2026-11-25` @ `02d930c` (key-name bug F2/F6,
  OOS controls, wins no-op, contemporaneous ΔX→ΔY leakage); `research/shadow-equations-review-2026-11-25`
  @ `264c059` (negative-value Gini, `_income_elasticity==0`, re-ranking, collinearities).
- Engine-blame retraction complete: `RUN_REPORT §3.8`, audit FS-12 erratum `3afac25`,
  `d87b89f`, `6935026`; no unqualified "engine overwrites exit reason" remains.

## 8. Meta — five silent failure classes caught (for Paper #3)

| class | receipt |
|---|---|
| cluster-bootstrap multiplicity dropping duplicate draws → CIs only | DHS `estimate.py` |
| transposed TWFE dummy matrix | eq09 (base 0.1753 vs within 0.2290) |
| `pinv` masking rank deficiency → false "supported" | tests: 49→45 rows |
| `e.kids['reason']` read after exits compacted → universal 0/0/0 | eduengine driver |
| `returncode == 0` treated as PASS while `decision_rule.PASS = False` | `run_all.py` |

All five were invisible to CI, unit tests, and plausibility review; each fix ships with a test that
fails on base.

## 9. Provenance artifacts

- Box evidence + lockfile: `research/box-runs-2026-11-25` @ `0fd9928` /
  `research/records/2026-11-25-box-runs/` (1,440 grid, 5,760 grid, 500+500 sweeps, 2,000 dense sweep,
  DHS patched verify, `pips_freeze`, input SHA-256, env summary).
- Handoff: `research/handoff-2026-11-24` @ `4df8f5d`; QA gate `~/neon-boot/QA_GATE_2026-11-25.md`.
- Power rules: `~/neon-boot/POWER_RULES_2026-11-25.md`; lease log `~/neon-boot/box_lease.jsonl`.
