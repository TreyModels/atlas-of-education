# TOY INVENTORY — Council brief-015 battery (15 experiments, 5 clusters)

**Audit date:** 2026-11-20 · **Auditor:** evidence audit (read-only on the battery)
**Status of the material:** ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no
historical test; phase closed. **No toy was re-run, re-seeded or re-parameterised for this audit.** The only
execution performed was `cluster_E/code/verify_results.py`, which reads `RESULTS.csv` and re-derives verdicts
(17/17 agree); it does not generate results.

**Canonical battery root** (called `TOYS/` throughout):

```
TOYS = 10_massification/extensions/codex_2026-11-20/toys_2026-11-20/
```

Every number below is quoted from a file under `TOYS/` (section cited) or recomputed from
`TOYS/cluster_*/RESULTS.csv` (noted as "recomputed from CSV"). Nothing is from memory.

---

## 0. How each toy is marked

The Council review (`TOYS/COUNCIL_REVIEW_016.md` §1) asks of every result: *would this survive changing the
stipulated rule that produced it?* The five marks used here:

| mark | meaning |
|---|---|
| **informative design constraint** | The transferable content is a constraint on future test/programme design or a genuine negative about a previously asserted inference. Survives its own parameters as a *design* statement (not as evidence). |
| **artefact by construction** | The headline is a restatement of a stipulated rule/identity; changing the rule changes the sign or removes the result. |
| **mechanically forced** | The arithmetic of the toy forces the outcome (identities, definitional nulls, corner solutions); it cannot come out otherwise. |
| **boundary-conditioned** | The verdict sits on a predeclared margin (or is a mixture/knife-edge); a small re-parameterisation flips it. Direction may be informative; magnitude must not travel. |
| **unfirable** | The declared falsifier (or a leg of it) cannot fire under the toy's own construction, so "falsifier not triggered" carries no information. |

A toy can carry more than one property; the mark is the **dominant** one, with the secondary properties in
`artefact_flag`/`note` of the CSV and in the per-toy entries below.

---

## 1. What I inspected (complete list; status)

All files opened and read unless marked "skim" (code: model rules read, row-level data not).

**Root**

- `TOYS/README.md` — read (80 lines). **Its SHA-256 does not match `SHA256SUMS.txt`; see §5.**
- `TOYS/COUNCIL_TOY_SPECS_015.md` — read (164 lines).
- `TOYS/COUNCIL_REVIEW_016.md` — read (358 lines). Not covered by `SHA256SUMS.txt` (written after it).
- `TOYS/COUNCIL_REVIEW_014.md` — read §3 (the C1 provider-entry route that the battery is design space around).
- `TOYS/SHA256SUMS.txt` — read and verified: **59/60 OK, 1 FAILED (`./README.md`)**.
- `TOYS/codex-massification-5eec11470690.zip`, `TOYS/luna-01-15-948a07a2567b.zip` — hash-verified OK (archives not unpacked).

**Cluster A** (`cluster_A/`)

- `PRE_DECLARATIONS.md` (226 lines, incl. AMENDMENT 1) — read.
- `FINDINGS.md` (233) — read.
- `RESULTS.csv` (234,400 data rows) — structured scan (26 arms × 200 seeds × metrics) + targeted recomputation
  of A_high, R, peak vacancy. **No `seed = AGG` rows exist**, contrary to `FINDINGS.md` §6 / `PRE_DECLARATIONS.md` §4.
- `RESULTS_SUMMARY.json`, `verdicts.json` — read (aggregates + mechanical verdicts).
- `RUN_MANIFEST.json` — read (label, parameters, amendments, hashes).
- `code/toy_market.py` (214) — skim: household side, lump vs divisible capacity, break-even `bk = F/contribution`,
  entry iff unmet ≥ bk, exit iff allocated < bk, one-period installation lock.
- `code/run_cluster_a.py` (371) — skim: three experiments, cells, writes CSV/summary.
- `code/verdicts.py` (130) — read: thresholds evaluated mechanically from the summary.
- `code/build_manifest.py` (152) — skim.

**Cluster B** (`cluster_B/`)

- `PRE_DECLARATIONS.md` (178) — read.
- `FINDINGS.md` (249) — read.
- `RESULTS.csv` (84,000 data rows after the label comment + header) — structured scan (20 cells × 500 seeds).
- `code/summary.json` — read in full (cell means, paired contrasts, verdicts, falsifier detail).
- `RUN_MANIFEST.json` — read.
- `code/exp4_visibility.py`, `exp5_queue.py`, `exp6_eligibility.py` — skim (scoring, rank order, two-stage screening).
- `code/toy_common.py`, `verdicts.py`, `run_all.py`, `test_toys.py` — skim (12 structural tests, per FINDINGS §0).
- No `verify_results.py` in this cluster.

**Cluster C** (`cluster_C/`)

- `PRE_DECLARATIONS.md` (244) — read, incl. deviation #1 (F7 applicability condition) and empty post-run edit log.
- `FINDINGS.md` (295) — read.
- `RESULTS.csv` (375 data rows) — read the full verdict/clause rows and cell aggregates; 34 `censored`,
  2 `undefined_no_floor_gain`, 3 `binding`, 16 PASS / 3 FAIL clause rows, 3 falsifiers `not_fired`.
- `RUN_MANIFEST.json` — read.
- `code/cluster_c_model.py` (272) — skim: `completions = admitted` identity, gate `ready + 0.15·aptitude + 0.15·stock ≥ gate_k`.
- `code/run_cluster_c.py` (504) — skim: T7e evaluated literally as two clauses.
- `code/selftest.py` (157) — skim (pairing/one-factor/budget invariants).
- `code/parameters.json`, `predecl_frozen_at_utc.txt` (`2026-11-20T11:03:59Z`), `predecl_refrozen_at_utc.txt`
  (`2026-11-20T11:05:55Z`), `predecl_sha256.txt` (`b0b0bdef…`) — read; hash matches `PRE_DECLARATIONS.md`.
- `code/run_stdout.txt` — skim.
- No `verify_results.py`; `selftest.py` only checks invariants.

**Cluster D** (`cluster_D/`)

- `PRE_DECLARATIONS.md` (374, incl. §6 pre-run amendment) — read.
- `FINDINGS.md` (295) — read.
- `RESULTS.csv` (36,922 data rows; 17 distinct threshold ids incl. `SIDE`/`INTERVAL`) — structured scan of all
  threshold rows + cell medians.
- `RUN_MANIFEST.json` — read (seeds 240/cell, parameter vector, `results_sha256_16`).
- `code/toy_engine.py` (303) — skim: gate sequence, `seat0`, readers/formal_share, posts responsive vs frozen 40.
- `code/exp10_level_first.py` (169), `exp11_cohort_shock.py` (117), `exp12_temporary.py` (165) — skim (PV schedules,
  per-child capacity, lease `+12/−12`, belief memory 0.70, reference 12).
- `code/run_all.py` (171) — skim.
- No `verify_results.py`.

**Cluster E** (`cluster_E/`)

- `PRE_DECLARATIONS.md` (182) — read; includes the control-arm-only calibration disclosure.
- `FINDINGS.md` (319) — read, incl. §7 integrity notes (unit fix, definitions).
- `RESULTS.csv` (369 data rows, 17 verdict rows) — read verdict/sensitivity rows; parsed all rows.
- `RUN_MANIFEST.json` — read.
- `code/exp13_migration.py` (290), `exp14_sector.py` (276), `exp15_diffusion.py` (331) — skim (route premium,
  shock 2.5, exposure 0.30/0.70, kin +0.22, travel term).
- `code/common.py`, `run_all.py`, `base_rate_check.py` — skim.
- `code/verify_results.py` (170) — read + executed: **17/17 verdicts agree**.

**Council**

- `08_council/DECISIONS.md` lines 88–96 (D79–D87), plus D92 data ruling — read (rulings, not re-litigated).

**Nothing was empty or unreadable.** No file required a fallback.

---

## 2. Per-toy inventory

### #1 — Entry-threshold hysteresis (Cluster A / `1_entry_hysteresis`)

- **Path:** `TOYS/cluster_A/` (`code/toy_market.py`, `run_cluster_a.py`, `verdicts.py`; `RESULTS.csv` arm prefix `lump_`/`divisible_`).
- **Mechanism/rule:** private providers are fixed lumps of `cap` seats; an inactive provider enters iff unmet
  customers ≥ break-even `bk = F/(tuition − varcost)`; an active provider exits immediately if allocated
  customers < `bk`; one-period installation lock; entry and exit are **contemporaneous** (no lag);
  allocation in entry order (`TOYS/cluster_A/PRE_DECLARATIONS.md` §0.2, §1).
- **Parameters that drive it:** N=100, 30 public seats, 4 providers × 8 seats, tuition 2.0, varcost 1.0
  (unit contribution 1.0), `F_low=$4 (bk 4)`, `F_high=$8 (bk 8 = cap)`, premium path `1.00, ±0.20, ±0.20, 1.00`
  (`PRE_DECLARATIONS.md` §1, Amendment 1 table).
- **Key numbers:** `A_high = 1.0338`, `A_low = 1.0254`, difference `0.008332` vs required `≥ 0.25`; exit seats
  9.80 vs entry seats 9.48; entry event share 0.960, exit 0.940; recovery ratio 1.000; applications 85.66 →
  100.00 (censored) up / 62.64 down; private customers 18.52 → 28.03 / 8.95
  (`FINDINGS.md` §1 table; `verdicts.json` exp1; recomputed from CSV: 9.80/9.48 = 1.0338).
- **Predeclared verdict:** **FAIL**, **falsifier TRIGGERED** (T1a, T1b both fail; band "inside")
  (`FINDINGS.md` §1; `verdicts.json`).
- **Council judgement (informative vs artefact):** "**the strongest negative in the battery**" — a fixed cost
  buys discreteness and a level shift, not asymmetry (`COUNCIL_REVIEW_016.md` §1 Cluster A row, §0(i)). But
  "near-symmetry is close to symmetry-by-construction": symmetric threshold, symmetric ±20% shock,
  contemporaneous decisions, and the up-shock censors applications at the 100-household ceiling
  (`COUNCIL_REVIEW_016.md` §1; `FINDINGS.md` §1 Caveats iii).
- **Mark:** **informative design constraint** (negative). Secondary: partly constructed null; censored up-shock.

### #2 — Public expansion with private exit (net vs gross) (A / `2_public_expansion`)

- **Path:** `TOYS/cluster_A/`.
- **Mechanism/rule:** comparative statics with mature providers; public seats expand 30→50 and 38→39; private
  providers are lumpy and exit **whole** if post-expansion customers < `bk`; demand not shocked
  (`PRE_DECLARATIONS.md` §2).
- **Parameters:** `cap=15, M=2` (private capacity 30) primary; `cap=30, M=1` replication; `F_high=$15 (bk 15 = cap)`,
  `F_low=$4`, `F_mid=$12` retained as the base toy's own value/sensitivity; premium fixed 4.0
  (`PRE_DECLARATIONS.md` §2, Amendment 1).
- **Key numbers:** gross +20.0, private admissions 13.43 → 3.15, net **+9.73**, **R = 0.486**, exit share 0.685;
  per-seed bimodal: +5 in 137/200 seeds (exit), +20 in 63/200; `F=$12` gives R = 0.665; cap30/F_high gives
  R = 0.314 with **42/200 seeds net ≤ 0**; 38→39 gives R = 0.550 (F_high)
  (`FINDINGS.md` §2 table; `verdicts.json` exp2; recomputed from CSV: 9.725/20.0 = 0.48625).
- **Predeclared verdict:** **PASS, on a thin margin** (T2a 0.486 < 0.50; T2b 0.708; T2c 0.685); falsifier not
  triggered (`FINDINGS.md` §2).
- **Council judgement:** "**the most decision-relevant mechanism**"; "the magnitude is arithmetic
  `R = 1 − exit_share × (lost lump/gross)`", a mixture not an elasticity; the design requirement (measure net,
  not gross) travels, the number does not (`COUNCIL_REVIEW_016.md` §1, §2.1).
- **Mark:** **boundary-conditioned** (14-seed swing; F=$12 → 0.665). Transferable: net-of-exit accounting design.

### #3 — Provider entry lag and overshoot (A / `3_entry_lag`)

- **Path:** `TOYS/cluster_A/`.
- **Mechanism/rule:** entry lag `L ∈ {0,2,4}` periods between order and first active period; temporary (4-period)
  vs permanent boom; exit immediate; new provider locked in for its first active period; entrants observe
  capacity already under construction (`PRE_DECLARATIONS.md` §3).
- **Parameters:** 30 public seats, 10 providers × 4 seats, `F=$4 (bk 4 = cap)`, 12 periods, boom t=2…5, 200 seeds
  (`PRE_DECLARATIONS.md` §3, Amendment 1).
- **Key numbers:** peak vacancy L=4 temporary **8.08** (rule ≥ 8.0, margin 0.08), 0.00 at L=0/L=2 and in every
  permanent cell; peak backlog 10.89; cumulative backlog 53.22; admissions over 12 periods 603.52 / 584.60 /
  567.06 (L=0/2/4); steady state t=7 vs t=6; idle capacity in 100% of L=4 temporary seeds, 0% elsewhere
  (`FINDINGS.md` §3; `verdicts.json` exp3; recomputed from CSV).
- **Predeclared verdict:** **PASS, on a thin margin** (T3a 8.08 ≥ 8.0; T3b; T3c 0.00 < 4.0); falsifier not
  triggered (`FINDINGS.md` §3).
- **Council judgement:** usable timing rule — "overshoot requires **lag > remaining boom length**"; the level is
  near-tautological ("capacity that arrives after demand recedes is idle"), and the **installation lock** is what
  records the vacancy (`COUNCIL_REVIEW_016.md` §1 Cluster A A3 row; `FINDINGS.md` §3 Caveats).
- **Mark:** **boundary-conditioned** (0.08 seats). Transferable: the lag-vs-boom-length condition.

### #4 — Visibility × mechanism (HC vs signalling) (B / `exp4_visibility_mechanism`)

- **Path:** `TOYS/cluster_B/` (`code/exp4_visibility.py`).
- **Mechanism/rule:** one-cohort admissions market; HC graduates gain +1.0 true skill, gross premium 4.0 at every
  visibility `v`; signalling graduates gain no skill, premium `4.0·(1−v)`; employer score
  `v·true_skill + (1−v)·credential`; top 40 hired (`PRE_DECLARATIONS.md` §1).
- **Parameters:** 100 people, 30 public seats, private capacity 30, fixed cost 12, 40 jobs, 500 seeds
  (`PRE_DECLARATIONS.md` §4).
- **Key numbers:** HC true output 1.498 → 1.585 → 1.585; signalling true output **0.499 → 0.627 → 0.796**
  (rises, not falls); signalling applications **85.85 → 28.45 → 0.00**; signalling rejected count 45.86 → 1.03 → 0;
  composition gaps 44.82 (v=.5) / 45.85 (v=1); output-true gaps 0.999 / 0.958 / 0.789
  (`FINDINGS.md` §1; `code/summary.json` exp4).
- **Predeclared verdict:** T4.1 **NOT MET**, T4.2 **NOT MET**, T4.3 PASS; F4 "not triggered", **but its v=0 leg is
  structurally unfirable** (`FINDINGS.md` §1, §5).
- **Council judgement:** the only stable discriminator is **composition**, not the direction of the output
  response; the predicted sign pattern fails because the stipulated premium reaches zero at v=1 (degenerate cell);
  F4's v=0 leg can never fire because HC adds +1.0 skill by definition (`COUNCIL_REVIEW_016.md` §1 Cluster B;
  `FINDINGS.md` §1).
- **Mark:** **unfirable** (F4 v=0; and v=1 degenerate by the `4(1−v)` stipulation). Secondary: it does license a
  design lesson (composition metrics).

### #5 — Queue vs human capital under fixed jobs (B / `exp5_queue_vs_human_capital`)

- **Path:** `TOYS/cluster_B/` (`code/exp5_queue.py`).
- **Mechanism/rule:** fixed older-diploma group (20), fixed treated young set (20); `skill_upgrade` adds +1.0 true
  skill; `rank_upgrade` grants queue priority only, with the **extreme credential-inflation order** "treated →
  other young by skill → older-diploma holders"; jobs fixed `U{35..40}` or responsive 100
  (`PRE_DECLARATIONS.md` §2).
- **Parameters:** 100 people, older group indices 0–19, treated 20–39, J0 ~ U{35..40}, responsive J=100, 500 seeds
  (`PRE_DECLARATIONS.md` §2, §4).
- **Key numbers:** older-group hires: rank **0.00**, reference 7.61, skill 4.38; output among hires: rank 0.6608,
  reference 0.8080, skill 1.2126; responsive output gap **0.200** (allocation component `~5.6e-17`, i.e. the
  residual is exactly the stipulated +1.0 skill on 20/100); attenuation 63.8%; rank−reference output −0.147;
  skill−reference +0.405 (`FINDINGS.md` §2; `code/summary.json` exp5).
- **Predeclared verdict:** T5.1/T5.2/T5.3 **PASS**, T5.4 **NOT MET**; D5.5/D5.6 PASS; falsifier not triggered
  (`FINDINGS.md` §0, §2).
- **Council judgement:** "the **decomposition** is the useful part … rank-vs-skill separation is a **rationing
  phenomenon**"; T5.1/T5.2 are "near-tautological under the extreme rank rule", T5.4's failure is arithmetic
  (`COUNCIL_REVIEW_016.md` §1 Cluster B).
- **Mark:** **mechanically forced** (older hires 0.00; T5.4 arithmetic). Transferable: rationing-conditional
  decomposition.

### #6 — Eligibility repeal vs blind ranking (B / `exp6_eligibility_vs_blind_ranking`)

- **Path:** `TOYS/cluster_B/` (`code/exp6_eligibility.py`).
- **Mechanism/rule:** two-stage screening: gate (retained = credentialed only; repealed = all) × ranking
  (visible = credentialed first; blind = skill only); 35 offers; credentials **independent of true skill**
  (`PRE_DECLARATIONS.md` §3).
- **Parameters:** 100 applicants, 35 offers, credential shares 45/55 main and 25/75 sensitivity, zero
  credential–skill correlation, 500 seeds (`PRE_DECLARATIONS.md` §3, §4).
- **Key numbers:** uncredentialed offer rate: visible/repealed **0.000**, visible/retained 0.000, blind/retained
  0.000, blind/repealed **0.350**; sensitivity 25/75 visible/repealed 0.133; gate-retained c25 leaves 10 vacancies
  (`FINDINGS.md` §3; `code/summary.json` exp6).
- **Predeclared verdict:** T6.1 **NOT MET**, T6.2 **PASS**, T6.3 **PASS**, T6.4 **NOT MET**; F6 not triggered
  (`FINDINGS.md` §0, §3).
- **Council judgement:** gate and visibility are **complements**; "a one-lever natural experiment can be a null by
  construction" — the no-op is arithmetic (45 credentialed ≥ 35 offers); blind result forced by zero
  credential–skill correlation (`COUNCIL_REVIEW_016.md` §1 Cluster B, §2.6).
- **Mark:** **mechanically forced**. Transferable: joint-lever design + "single-lever null".

### #7 — Capacity by level (floor/ceiling split) (C / `7_capacity_by_level`)

- **Path:** `TOYS/cluster_C/` (`code/cluster_c_model.py`).
- **Mechanism/rule:** 30 cohorts of 120; three sequential levels; admission requires `cash ≥ fee_k` and
  `ready + 0.15·aptitude + 0.15·stock_k ≥ gate_k`; **completions = admitted** (no dropout); capacity doubled at one
  level / all levels with a 4-cohort ramp (`PRE_DECLARATIONS.md` §1).
- **Parameters:** fees (0.20, 0.36, 0.55), base seats (55, 20, 7), gates (0.30, 0.45, 0.35), cash groups
  (0.24, 0.62, 1.05), 200 seeds (`PRE_DECLARATIONS.md` §1).
- **Key numbers:** floor +44.43 pp [44.19, 44.68]; middle (secondary) +11.71 [11.29, 12.12]; ceiling +4.58
  [4.38, 4.77]; secondary **conversion 70.2%** (14.05 of 16.67 pp added seats; 15% of added seats idle,
  utilization 0.851); ceiling maximum 11.67 pp even with all levels doubled; floor peak **90.46 pp**;
  `primary_only` ceiling +0.00 (`FINDINGS.md` §1; `RESULTS.csv`; recomputed: (34.05−20)/20 = 70.2%).
- **Predeclared verdict:** T7a PASS, T7b PASS, **T7c FAIL** (70.2% > 50% cap), T7d PASS, **T7e FAIL** (clause i
  PASS 11.67 < 50; clause ii FAIL 90.46 ≥ 90 — a **wording defect**), T7f PASS; F7 not fired
  (`FINDINGS.md` §1.3–1.4).
- **Council judgement:** "**T7c's failure is the most informative result in the cluster**" — the Council's own
  prediction (< 50% conversion) was wrong; **saturation is a property of the gate/eligible pool, not of the
  level**; T7d mechanically forced; T7e a wording defect, not a contradiction
  (`COUNCIL_REVIEW_016.md` §1 Cluster C, §2.3).
- **Mark:** **informative design constraint** (the re-specification). Secondary: T7d forced; T7e defect.

### #8 — Enforcement × compulsory law (C / `8_enforcement_x_law`)

- **Path:** `TOYS/cluster_C/`.
- **Mechanism/rule:** one cohort of 120; de jure law `L` × declared enforcement `e ∈ {0,.5,1}`; the statute carries
  a small stipulated norm effect (`delta_norm = 0.010`) and a larger register-only effect (`reg_norm = 0.10`);
  `e` multiplies attendance pressure and verified learning; work displaced by attendance
  (`PRE_DECLARATIONS.md` §2).
- **Parameters:** `delta_norm=0.010`, `delta_enf=0.35`, `reg_norm=0.10`, `reg_enf=0.30`, thresholds
  0.55/0.60/0.70, work retention 0.60, 200 seeds (`PRE_DECLARATIONS.md` §2).
- **Key numbers:** no-law: registration 29.94, attendance 44.64, completion 18.90 pp. Paper law (L=1,e=0):
  registration **+9.91 pp**, attendance **+1.09 pp**, completion +0.51 pp. Enforced (e=1): attendance **+18.63**
  [+18.09, +19.17], completion **+20.29** [+19.77, +20.81]; e=0.5 attendance +9.71. Work reduction 18.17× larger
  at e=1 than e=0. Enforcement without law = **0.000** in all eight metrics (`FINDINGS.md` §2).
- **Predeclared verdict:** T8a–T8d **PASS**; F8 not fired (`FINDINGS.md` §2.2).
- **Council judgement:** "a measurement warning with real force": a paper law moves the register +9.91 pp but
  attendance +1.09 pp, so **register-based compliance overstates the behavioural effect ~9×** — C4 must measure
  de facto enforcement. But "law alone is inert" depends on the stipulated `delta_norm=0.010`, and
  "enforcement without law = 0.000" is a **built-in null by construction** (`COUNCIL_REVIEW_016.md` §1 Cluster C,
  §2.4; `FINDINGS.md` §2.3).
- **Mark:** **informative design constraint** (measurement: register ≠ classroom). Secondary: the e×L null and the
  9× ratio are stipulated magnitudes.

### #9 — Buildings vs teachers at equal budget (C / `9_buildings_vs_teachers`)

- **Path:** `TOYS/cluster_C/`.
- **Mechanism/rule:** fixed budget `B=480` (`rooms·12 + posts·60 = 480`) in every purchase arm; matched stock 30
  places / 2 posts; `admissions = min(physical_places, teacher_capacity, 120)`; retention `π ∈ {0.60, 0.90}`;
  completions depend on teacher load (`PRE_DECLARATIONS.md` §3).
- **Parameters:** room cost 12, post cost 60, teacher capacity 12, q_base 0.92, q_floor 0.55, 200 seeds
  (`PRE_DECLARATIONS.md` §3).
- **Key numbers:** `rooms_only`: physical **70 (+40)**, staffed **+0.00**, completion **+0.00 pp** (both π);
  `teachers_only`: PTR **3.00** (best) but completion 22.83 pp; `split`: staffed +29, completion 32.79 / 38.16 pp;
  retention gain +5.37 (split) vs +0.00 (teachers_only) (`FINDINGS.md` §3).
- **Predeclared verdict:** T9a–T9d PASS (7 clause rows), F9 not fired (`FINDINGS.md` §3.2).
- **Council judgement:** "**the clearest 'artefact by construction' in the battery**" — rooms-only completion is
  exactly 0.00 because the production function has **no unstaffed-seat channel at all**; the only transferable
  content is the measurement caution "**PTR is not usable places**"; "do not cite C9 as evidence that buildings
  are useless" (`COUNCIL_REVIEW_016.md` §1 Cluster C, §2.5).
- **Mark:** **artefact by construction**.

### #10 — Level-first roll-out and crossing order (D / `10_level_first`)

- **Path:** `TOYS/cluster_D/` (`code/exp10_level_first.py`, `toy_engine.py`).
- **Mechanism/rule:** PV-equal seat expansion (40 discount-0.97 seat-years per level) injected into one level at a
  time or all at once; endogenous backlog-rationed construction; one-gate-per-cohort sequencing
  (`PRE_DECLARATIONS.md` §2).
- **Parameters:** N=120, 30 cohorts, δ=0.97, 40 seat-years/level, `seat0=(18,0,0)`, 240 seeds
  (`PRE_DECLARATIONS.md` §1, §2).
- **Key numbers:** crossing years (M0 primary 50% / M1 primary 90% / M2 lower-sec 50% / M3 upper-sec 50%):
  control 10/31/27/31; primary_first **4/16/12/17**; lower_first 7/10/13/18; upper_first 10/13/15/**21**;
  simultaneous 6/13/14/19. Spacing `S` = 21/13/11/11/13. Paired `S(primary_first) − S(simultaneous)` =
  **0.0** (P10-2c fail; rule ≥ 2). P10-1 order holds 1.000 in all sequential arms. Upper-secondary completions
  22 / 1428.5 / 1340 / **1077** / 1278 (upper_first lowest). `S(primary_first)=13` misses the declared
  [2, 12] interval (`FINDINGS.md` §1.1–1.2; `RESULTS.csv`).
- **Predeclared verdict:** **PARTIAL** — P10-1 and P10-3 met; P10-2b and P10-2c fail; secondary INTERVAL miss
  (`FINDINGS.md` §1.2).
- **Council judgement:** the spacing negative is genuinely informative: order moves crossing years but
  **simultaneity does not compress floor→ceiling spacing — the credential pipeline does** (S = 11–13 in every
  arm; paired difference 0.0). P10-1 is a design property (a level cannot complete before the level below);
  the A10 mirror is designed in (`COUNCIL_REVIEW_016.md` §1 Cluster D, §2.7).
- **Mark:** **informative design constraint** (spacing). Secondary: P10-1 unfirable as a finding.

### #11 — Cohort-size shock × capacity (D / `11_cohort_shock`)

- **Path:** `TOYS/cluster_D/`.
- **Mechanism/rule:** permanent cohort size `n ∈ {96, 120, 144}` × capacity rule frozen (absolute seats) vs
  responsive (seats per child, `cap = seat_f·n/120`); fixed 3 seats/cohort investment, employer per-child invariant
  (`PRE_DECLARATIONS.md` §3, §6.3).
- **Parameters:** 3 seats/cohort, `seat0=(18,0,0)`, employers responsive in every arm, 240 seeds
  (`PRE_DECLARATIONS.md` §6.3).
- **Key numbers:** `X_M0` neutral 15, up_frozen **19**, down_frozen **11**, responsive all **15**; completion per
  child 0.772 / 0.688 / 0.819; paired DiD **+4.0 years** (240/240); P11-3a −0.0868, P11-3b −0.0021; M1 (primary
  90%) censored in **every** cell (`FINDINGS.md` §2.1–2.2).
- **Predeclared verdict:** **SUPPORTED** (P11-1a/b, P11-2, P11-3a/b all met; SIDE met) (`FINDINGS.md` §2.2).
- **Council judgement:** "near-tautological: under responsive capacity the seat stock **per child is identical by
  construction**, so 'no effect' is arithmetic"; D itself says the 240/240 sign consistency is "the arithmetic
  forces this"; cite only as a definition — **a demographic shock is only a shock when capacity fails to scale**
  (`COUNCIL_REVIEW_016.md` §1 Cluster D; `FINDINGS.md` §2.3.3).
- **Mark:** **mechanically forced**.

### #12 — Temporary expansion with expectations (D / `12_temporary`)

- **Path:** `TOYS/cluster_D/` (`code/exp12_temporary.py`).
- **Mechanism/rule:** 12 leased upper-secondary seats in cohorts 2–4 only; arms supply-only / fee waiver /
  placement information × employer frozen/responsive; mid-transition start `seat0=(108,100,12)`, construction off;
  information regime = adaptive belief `b ← 0.70·b + 0.30·(grad_hires/12)`, access/rank multiplied by `clip(b,0.5,2)`
  (`PRE_DECLARATIONS.md` §4, §6.1, §6.4).
- **Parameters:** lease +12 cohorts 2–4 (i.e. t=1…3 0-based), belief memory 0.70, reference flow 12, 240 seeds
  (`PRE_DECLARATIONS.md` §6.1, §6.4; `code/exp12_temporary.py` constants).
- **Key numbers:** PRE identical in all arms (86.0 upper-secondary applications, 12 completions, 40/35 hires).
  Info+frozen: POST applications **+17.1%**, DECAY +0.5%; info+responsive POST +11.9%, DECAY +0.2%. Fee waiver:
  DURING +30%/+36%, poor share of upper completions 0.069 → **0.222**, POST **0.0**. Supply-only+responsive:
  DURING hires **+1.67** (< 2.0 rule), POST +1.0 (60% of DURING, rule ≤ 50%) (`FINDINGS.md` §3.1–3.2).
- **Predeclared verdict:** **PARTIAL** — P12-1a/1b/3 met; P12-2a and P12-2b fail (`FINDINGS.md` §3.2).
- **Council judgement:** "**price vs belief** is the useful distinction" (price fades, beliefs persist); the
  persistence magnitude is the stipulated belief memory and the hire-decay FAIL is a **threshold-vs-engine
  mismatch** (skill-stock memory 0.8 ⇒ 4–5 cohort time constant vs declared 3-cohort halving); "supply-only cannot
  raise applications" is a model limitation; P12-1b is definitional (`COUNCIL_REVIEW_016.md` §1 Cluster D, §2.7;
  `FINDINGS.md` §3.3).
- **Mark:** **boundary-conditioned** (threshold-vs-engine mismatch; stipulated half-life).

### #13 — Migration and remittance route (E / `E13_migration_remittance`)

- **Path:** `TOYS/cluster_E/` (`code/exp13_migration.py`).
- **Mechanism/rule:** 200 origin households × 20 cycles; external credentialed route open/closed × remittances
  on/off; local formal posts **fixed at 45**; origin seats **deliberately non-binding** (170; peak applications 134);
  migration counted once (`PRE_DECLARATIONS.md` #13).
- **Parameters:** route premium 2.4, local jobs 45, seats 170, remittance amount 0.8 / kin 0.35 / reference 40,
  diaspora 20, 200 seeds (`PRE_DECLARATIONS.md` #13).
- **Key numbers:** completion 40.24% → 55.45%, route effect **+15.22 pp** [14.89, 15.54]; remittances **+3.54 pp**
  [3.36, 3.71] and **+8.05 applications/cycle**; local posts **45 in all 4 cells, all 200 seeds**; local output
  73.35 → 72.08 (−1.7%); unique migrants **78.50** vs ≈900 person-cycles (~11× overstatement); sensitivity
  half-premium +11.36 pp (`FINDINGS.md` §2).
- **Predeclared verdict:** T13-P1a/P1b/P2/P3 **PASS**; F13 not triggered (`FINDINGS.md` §1, §2).
- **Council judgement:** clean decomposition and a real measurement lesson (**count migrants once**), but the
  construction is deliberately clean: origin seats non-binding, so it is a **demand-channel-only** result — with
  binding seats the same push would appear as a queue, not completions (E says so)
  (`COUNCIL_REVIEW_016.md` §1 Cluster E; `FINDINGS.md` §2.1).
- **Mark:** **artefact by construction** (clean by design). Transferable: count-once measurement note.

### #14 — Sector-demand shock × field access (E / `E14_sector_shock_field_access`)

- **Path:** `TOYS/cluster_E/` (`code/exp14_sector.py`).
- **Mechanism/rule:** 200 leavers, two fields; one-factor shock (+2.5 return) to one field; field access open vs
  closed (top-30% gate); seats per field non-binding (150); value-threshold application rule
  (`PRE_DECLARATIONS.md` #14).
- **Parameters:** `SHOCK=2.5` (vs aptitude range 1.0), seats 150/field, gate 30%, posts 30 / 55, 200 seeds
  (`PRE_DECLARATIONS.md` #14).
- **Key numbers:** open: Δapps A **+106.50** [105.50, 107.49], Δcompleters A **+90.07**, **Δtotal completers +24.68**
  [23.93, 25.43] (rule ≤ 10); closed: +32.26 / +27.16 (ratios **0.303 / 0.302**); field-B apps **0.00** under a
  field-A shock; placebo +106.73 / −74.11; vacancies closed **8.35** vs open 0.00 (rule ≥ 10 / ≤ 3), no-shock
  closed vacancies already 10.51 (`FINDINGS.md` §3).
- **Predeclared verdict:** T14-P1a/P1b PASS; **T14-P1c FAIL**; T14-P2a/b PASS; T14-P3 PASS; **T14-P4 FAIL**;
  F14 not triggered (`FINDINGS.md` §1, §3).
- **Council judgement:** "**T14-P1c is the most useful negative in the battery**" — a sectoral shock has a
  **participation margin as well as a switching margin**; but the corner solution (`SHOCK=2.5` > aptitude range
  1.0 ⇒ 100% switching, field B empties) maximises that margin; T14-P4 over-predicts vacancies
  (`COUNCIL_REVIEW_016.md` §1 Cluster E, §2.8).
- **Mark:** **informative design constraint** (the participation negative). Secondary: corner solution.

### #15 — Neighbour information and roads (E / `E15_neighbour_information_roads`)

- **Path:** `TOYS/cluster_E/` (`code/exp15_diffusion.py`).
- **Mechanism/rule:** two villages × 60 households; info × road × teacher (8 cells, 2 tie types); information
  exposure probability `0.30 + 0.40·road`; kin transmission **+0.22 stipulated**; seats bind at every level
  (16/6/2, +1 with teacher); admissions capped by seats (`PRE_DECLARATIONS.md` #15).
- **Parameters:** 120 households, seats (16,6,2), fees (0.19,0.34,0.52), travel reduction 0.55 (sensitivity 0.30),
  exposure 0.30/0.70, kin +0.22, 200 seeds (`PRE_DECLARATIONS.md` #15).
- **Key numbers:** info effect road=1 **+0.0634/hh** [0.0600, 0.0669]; road=0 **+0.0328** [0.0301, 0.0354]; DiD
  **+0.0307** [0.0266, 0.0347] (rules ≥0.06, ≥0.10, ≤0.06); road main **+0.2265**; teacher main **+6.67 pp**; info
  main **+0.0481**; info effect on admissions **−0.00002**; queue **+0.0481** (rule ≥ 0.05; fails by **0.002**);
  nearest-quartile admissions 0.5875 → 0.4638, farthest 0.2358 → 0.3327; tied 0.7855 vs untied 0.7065
  (`FINDINGS.md` §4; `code/verify_results.py` run: same values).
- **Predeclared verdict:** **T15-P1 FAIL**, T15-P2 PASS, **T15-P3 FAIL**; F15 not triggered, marginal (0.0307 vs
  0.03 floor) (`FINDINGS.md` §1, §4).
- **Council judgement:** the interaction is a **dose effect** (contact probability 0.30 vs 0.70; per-exposed
  effect roughly equal, +0.09 vs +0.11), **not complementarity**; T15-P3 fails by 0.002 — a **threshold artefact**,
  not a mechanism failure; the real content is "with fixed seats, application-side interventions show up as
  **queues and spatial reallocation**, not completions" (`COUNCIL_REVIEW_016.md` §1 Cluster E, §2.8).
- **Mark:** **boundary-conditioned** (T15-P3 by 0.002; interaction by dose). Transferable: queues-not-places.

---

## 3. Summary table

| # | toy | cluster | verdict | mark | Council's core reading |
|---|---|---|---|---|---|
| 1 | entry hysteresis | A | FAIL (falsifier fired) | informative design constraint | fixed cost ≠ asymmetry — strongest negative |
| 2 | net vs gross | A | PASS 0.486 (thin) | boundary-conditioned | measure net of private exit |
| 3 | entry lag / overshoot | A | PASS 8.08 (thin) | boundary-conditioned | overshoot needs lag > boom |
| 4 | visibility × mechanism | B | 2 NOT MET, 1 PASS | unfirable | composition, not output direction; F4 v=0 unfirable |
| 5 | queue vs HC | B | 3 PASS, 1 NOT MET | mechanically forced | rationing-conditional decomposition |
| 6 | eligibility vs blind | B | 2 PASS, 2 NOT MET | mechanically forced | gate × visibility are complements; joint lever |
| 7 | capacity by level | C | 4 PASS, 2 FAIL | informative design constraint | gate, not level, sets saturation (T7c) |
| 8 | enforcement × law | C | 4 PASS | informative design constraint | register ≠ classroom (~9×); de facto e needed |
| 9 | buildings vs teachers | C | 4 PASS (7 clauses) | artefact by construction | only PTR-is-not-places travels |
| 10 | level-first roll-out | D | PARTIAL | informative design constraint | order moves years; pipeline sets spacing |
| 11 | cohort shock × capacity | D | SUPPORTED | mechanically forced | shock only if capacity fails to scale |
| 12 | temporary expansion | D | PARTIAL | boundary-conditioned | price fades, beliefs persist (magnitude stipulated) |
| 13 | migration / remittance | E | 4 PASS | artefact by construction | clean by design (non-binding seats); count migrants once |
| 14 | sector shock × access | E | 5 PASS, 2 FAIL | informative design constraint | participation margin as well as switching |
| 15 | info / roads | E | 1 PASS, 3 FAIL | boundary-conditioned | queues not places; interaction is a dose effect |

**Counts (dominant mark):** informative design constraint **5** (#1, #7, #8, #10, #14); boundary-conditioned
**4** (#2, #3, #12, #15); mechanically forced **3** (#5, #6, #11); artefact by construction **2** (#9, #13);
unfirable **1** (#4). Toy-level predeclared verdicts: 1 outright FAIL (#1); 6 with at least one NOT MET/FAIL
(#4, #5, #6, #7, #14, #15); 2 PARTIAL (#10, #12); 1 SUPPORTED (#11); 5 all-PASS (#2, #3, #8, #9, #13).

If "informative" is read narrowly (would survive its own stipulations as a negative or a *design* statement),
the count is **5 of 15**; if boundary-conditioned results are counted as informative design input (as the Council
does for A2 — "the most decision-relevant mechanism"), the count is **7 of 15**. Separately, **8 of 15** carry a
*structural* non-citability (built-in null, unfirable falsifier, arithmetic identity, degenerate cell) rather
than a mere boundary: #4, #5, #6, #9, #11, #13 outright, plus #7 (its T7d cell is forced) and #8 (its `e×L` cell
is a built-in null). The four boundary-conditioned toys (#2, #3, #12, #15) may be cited only as directions, never
as effects (LUTZ's caution, `COUNCIL_REVIEW_016.md` §7).

---

## 4. Cross-cutting anatomy of the artefacts (what makes a toy "forced")

1. **Identities:** C7 `completions = admitted` (no dropout) → `primary_only` ceiling exactly 0.00 pp; C9
   `admissions = min(physical, teacher_capacity, 120)` → rooms-only 0.00 pp; C8 `e × L` mapping → enforcement
   without law 0.000; D12 frozen posts always filled → "hires flat" exactly 0; D11 per-child capacity → responsive
   arm identical by construction.
2. **Knife-edges and mixtures:** A2 `bk = cap` and all-or-nothing exit → bimodal net (+5 / +20), R = 0.486;
   A3 8.08 vs 8.0; E15 0.0481 vs 0.05; E14's `SHOCK=2.5` corner.
3. **Stipulated premia:** B4 `4(1−v)` ⇒ degenerate v=1 cell; B5 extreme rank order ⇒ older hires 0.00; B6 zero
   credential–skill correlation ⇒ blind-ranking contrast.
4. **Unfirable falsifiers:** B4/F4 v=0 leg; C8's built-in null (Cartwright's caution: never report as
   "falsifier not triggered"); D10 P10-1 (order is a design property).
5. **Threshold-vs-engine mismatches:** D12 P12-2 (3-cohort halving vs 0.8 skill memory); C7 T7e (wording);
   E15 T15-P3 (per-village → per-household unit fix flipped PASS→FAIL; disclosed).

---

## 5. Integrity and mislabel log (also see `GAPS_AND_LEADS.md` §f)

1. **`README.md` fails its own hash.** `shasum -a 256 -c SHA256SUMS.txt` → 59 OK, **1 FAILED: `./README.md`**
   (expected `0fe6b6fb…`, actual `71a49cb6…`). Timestamps: `SHA256SUMS.txt` 19:14:42, `COUNCIL_REVIEW_016.md`
   19:19:46, `README.md` **19:20:10**. The README's mtime post-dates the review by 24 s, which is consistent with
   the review's "every one of the 60 entries verifies" (`COUNCIL_REVIEW_016.md` §0/§6.3; D79) being accurate when
   written and the README being edited immediately afterwards (its last section, "Canonical location", lines
   73–80, is the natural candidate — it is the only README content that reads as post-review housekeeping, though
   the file cannot prove which edit moved the hash). **Not fabrication — a stale checksum.** The review itself
   (`COUNCIL_REVIEW_016.md`) is not in `SHA256SUMS.txt` at all. Fix: regenerate the hash file and add the review.
2. **A's `RESULTS.csv` has no `seed = AGG` rows.** `cluster_A/PRE_DECLARATIONS.md` §4 and `cluster_A/FINDINGS.md`
   §6 state that aggregates are written as `seed = AGG`; the delivered CSV has 200 distinct numeric seeds and no
   `AGG` row. The aggregates exist in `RESULTS_SUMMARY.json`/`verdicts.json`. Documentation overstatement, not a
   data loss (all 200 seeds × 26 arms × metrics present: 234,400 rows).
3. **"Several include a `verify_results.py`"** (`README.md` line 63) — only `cluster_E` has one. B has
   `test_toys.py`, C has `selftest.py`; A and D have no independent verdict re-derivation.
4. **D10 prose inconsistency:** `cluster_D/FINDINGS.md` §1.3 point 2 says "`primary_first` reaches 90 % primary
   completion by cohort 16; `upper_first` not until 13 and `simultaneous` also 13". The table (§1.1) gives
   `upper_first` = 13 and `simultaneous` = 13, i.e. **earlier** than 16; "not until 13" is directionally wrong
   (the substantive point — `upper_first` wastes early top capacity — is supported by the 1077 vs 1428.5 output).
   Numbers are right; the sentence is not.
5. **Path-label anomaly (known, D84):** all five `PRE_DECLARATIONS.md` and `RUN_MANIFEST.json` files, and most
   `FINDINGS.md`, reference `extensions_archive/…`; the canonical artefacts are under
   `TOYS/`. The untracked ~30 MB duplicate recorded in D84 was **not present** under
   `experiments/massification-2026-11-20/` or `massification_live/` at audit time — only the label problem remains.
6. **Predeclaration re-freeze (C):** `predecl_frozen_at_utc.txt` 11:03:59Z → `predecl_refrozen_at_utc.txt`
   11:05:55Z, hash still `b0b0bdef…`; deviation #1 changed only F7's applicability condition (thresholds
   unchanged), post-run edit log empty. Disclosed and consistent.
7. **E unit fix (disclosed):** T15-P3 compared per-village totals against a per-household margin (PASS) and was
   corrected to per-household (**FAIL**, 2.888 → 0.0481). A PASS→FAIL correction is the conservative direction;
   no parameter/seed/threshold changed (`cluster_E/FINDINGS.md` §7.1).
8. **No empty or missing artefacts.** All 60 hash entries exist; 59 verify; the two zips verify.

*The label binds every file in this inventory: ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not
evidence; no historical test; phase closed; do not cite numbers as estimates.*
