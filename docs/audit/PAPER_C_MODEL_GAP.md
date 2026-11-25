# PAPER_C_MODEL_GAP — why shadow education emerges and what determines its supply form

Owner lane: `engine-core` (design-only, read-only probes) · 2026-11-25 · branch
`research/contest-audit-v2-2026-11-25`
Inputs: repaired engine tree at commit `79add93` (core.py 1268 L, tutoring.py 551 L, schools.py 170 L),
`docs/audit/canonical_spec.json` (frozen Paper B spec), and the **183-equation inventory**
`docs/audit/refs/education-equation-inventory-20261124.txt` (Bridge attachment `20261124154148-7126f591`,
34,984 B, 404 lines, sha256 `0fd30f77…52df`; committed with a *not-a-verified-bibliography* caveat).
Evidence taxonomy: everything below is **DESIGN / REPRODUCED SIMULATION** (read-only probes on the host); no empirical
claim is made. Every inventory equation is a **candidate** until its primary source is verified.

Purpose: verify precisely what the engine already represents for the Paper-C question (emergence of shadow education
and its supply form), and specify the *minimal* extensions needed for a confirmatory Paper C, without touching the
frozen Paper B spec.

---

## 0. Bottom line

The repaired engine already represents more mechanism than the standard equation inventory:

1. **Demand** is a structural discrete choice between no tutoring, the own teacher, and a firm, priced in cash and
   valued through the marginal value of learning (`mvl`), not a reduced-form participation regression.
2. **Supply** has two suppliers with different technologies (own teacher: buy-back of withheld lessons, price
   controlled; firms: upward-sloping short-run capacity, free entry, bans raise price and cut availability).
3. **Withholding/rent extraction** is explicit: `h = h_max · driver(w_T/w_out) · (1−monitoring) · (1−own_ban)`, and
   the own-teacher market exists only when `1−own_ban > 0`.
4. **Positional competition** (fixed seats, elite/university contest) is explicit and drives contest prep; expected
   and realised admission probabilities are the same Plackett–Luce object after the Gate-1 repair.
5. **Outcome accounting** is rich (participation/spend by quintile, own-vs-firm mix, school quality, withheld,
   teacher pay/PTR, spending, completion/MPL/literacy, elite access).

What is **absent** is exactly what Paper C is about:

* a *positive* school-effort lever (homework/feedback/supervision) — the school can only supply generic quality `q`
  and withhold; there is no effort/preparation input S separate from q;
* **time budgets** for students or teachers (the inventory's eq 21 is not implemented anywhere);
* **learning decomposition** / an explicit `L` production function (L is an additive cumulative sum with no
  recorded components; no substitution or complementarity between school and tutoring);
* **supply-form equilibrium accounting** (own-teacher strategy, firm profits, state supply, welfare);
* `G = max(0, L − S)` — the shadow-education share of learning — is computable only after decomposition is recorded.

**Canonical Paper B is a private-market regime and cannot answer the emergence question as-is.** In the frozen HK/KR
spec `pay_ratio=1.2 ⇒ driver=0 ⇒ h=0` exactly (probe: `withheld=0.00000` in both), and `own_ban=0.95` offers the
own-teacher option to only 5 % of pupils (realised own share 2.5–2.8 %). The withholding/own-teacher channel is
effectively off; the firm market carries ~97 % of tutored pupils.

---

## 1. What is REPRESENTED / PARTIAL / ABSENT (file:line)

### 1.1 School supply and S

| item | status | anchor |
|---|---|---|
| school budget → teachers: `T = salary_share·B/wT` | REPRESENTED | `schools.py:47` |
| class size → quality: `q = q0·min(1.25,(ptr_target/ptr)^alpha_ptr)` | REPRESENTED | `schools.py:49` |
| `pay_ratio` (teacher pay = pay_ratio·w_outside), `w_outside` | REPRESENTED | `schools.py:43` |
| staffing rule `'budget'` / `'norm'` | REPRESENTED | `schools.py:44-47` |
| public seat capacity + rationing (`ptr_max`, `rationed`) | REPRESENTED | `schools.py:60,62-73` |
| teacher withholding: `h = h_max·driver·(1−monitoring)·(1−own_ban)` | REPRESENTED (negative lever only) | `schools.py:52-54` |
| `withhold_mode='pay_gap'|'incentive'` | REPRESENTED | `schools.py:26,53` |
| buy-back interaction (own tutoring cancels withheld learning loss) | REPRESENTED | `core.py:963-964` (`1−buyback·withheld`), `tutoring.py:252-254` |
| private schools: q = `q0·priv_quality`, price/entry/capacity | REPRESENTED | `schools.py:92,101-107,114,117-165` |
| **positive homework/feedback/supervision effort S** | **ABSENT** | no param; `y['quality']` and `y['withheld']` are the only school inputs (`schools.py:58-59`; learning line `core.py:963-966`) |
| school effort *cost* (teacher time) / workload accounting | **ABSENT** | `teachers` is a headcount (`schools.py:47,60`), no hours; no time params anywhere (grep: no `time_*`, `hours`, `workload`) |
| sector aggregation of public+private quality | PARTIAL | each child gets one sector's q; no CES/aggregate S (inventory eq 120) |

### 1.2 Shadow-education demand and supply form

| item | status | anchor |
|---|---|---|
| three-way choice: none / own teacher / firm, argmax of latent utilities | REPRESENTED | `tutoring.py:232-241` |
| own-teacher availability = `1−own_ban` (ban enforcement) | REPRESENTED | `tutoring.py:73,234` |
| firm availability = `(1−firm_ban)·access` (urban/rural), price `p_firm·(1+firm_ban)` | REPRESENTED | `tutoring.py:96-101,235` |
| firm short-run capacity `K`, free entry `K ← K + firm_entry·(D−K)`, income rationing | REPRESENTED | `tutoring.py:242-250` |
| own-teacher price `p_own` vs firm price `p_firm`; effects `tut_effect_own`/`tut_effect` | REPRESENTED | `tutoring.py:57-58,252` |
| buy-back motive weight `h·q` in own utility, `buyback_firm·h·q` for firms | REPRESENTED | `tutoring.py:232-233` |
| remedial motive via `r0·(1−home)` | REPRESENTED | `tutoring.py:230,232-233` |
| contest-prep motive: effort `e_t` maximising `gate_prize_dv·P − unit cost·e` | REPRESENTED | `tutoring.py:334-380` |
| prep stock per gate with depreciation `rho` | REPRESENTED | `tutoring.py:282-286,389`; core alloc/consume `core.py` prep_stock |
| prep mode `positional|learning|both` + `contest_prep_learning_gain` | REPRESENTED (switch) | `tutoring.py:65-67,200-212,392-393` |
| own-vs-firm **spend** split / own-teacher revenue | **ABSENT** | `extra_spend` aggregate (`tutoring.py:255`); `firm_rev` mixes firm fees + contest resource cost (`tutoring.py:459`); see §1.5 |
| provider cost/profit accounting (`pi_T = P_T Q_T − C(Q_T)`) | **ABSENT** | only `firm_rev` (`tutoring.py:459`); entry rule is not a profit condition |
| market clearing `Q^d = Q^s` | PARTIAL | capacity rationing + entry (`tutoring.py:242-250`), not an equilibrium price that clears demand |
| supply-form *welfare* / who supplies G | **ABSENT** | no welfare/accounting by supplier |
| **time cost of tutoring** (student time) | **ABSENT** | demand is constrained by cash only (`E._cash`, `tutoring.py:236`); no time budget |

### 1.3 Positional competition / gate pressure

| item | status | anchor |
|---|---|---|
| gate kinds open/fixed_bar/quota/contest | REPRESENTED | `core.py` normalise; gate loop `core.py:998-1035` |
| fixed seats by share (`share_of='cohort'|'applicants'`) | REPRESENTED | `core.py:contest_seats`, gate loop `core.py:1002-1012` |
| expected = realised PL top-K admission | REPRESENTED | `core.py:_pl_probs/contest_weights`, `tutoring.py` PL call |
| contest discrimination `contest_r`, baseline input `contest_x0`, effort `contest_alpha` | REPRESENTED | `core.py:452-473` (`x_eff`, `w`) |
| elite prize `elite_logw` / track prize (`quality_mult`, `earnings_logw`, `g12_track_bonus`) | REPRESENTED | `core.py:766` (`gate_prize_dv`), `core.py:1031-1035` |
| exam score = L + `exam_sd`·noise for bar/quota | REPRESENTED | `core.py:996` |
| positional externality (fixed seats ⇒ private effort is a transfer) | PARTIAL/IMPLICIT | zero-sum is inside PL + fixed seats; no welfare/decomposition of effort rents |
| `promote_bar` grade progression pressure | REPRESENTED (off in canonical: 0.0) | `core.py:42,977-978` |
| MPL/literacy thresholds | REPRESENTED (measurement only) | `sdg4.py:48-56`, `measure.py:85` |

### 1.4 Learning production (`L`)

| item | status | anchor |
|---|---|---|
| `dL = q·(1−buyback·withheld)·voc·exp(β_a·a) + tut_gain + home_effect·(home−0.5) + ε` | REPRESENTED (additive) | `core.py:960-968` |
| `L_{t+1} = L_t + dL` (cumulative, no depreciation) | REPRESENTED | `core.py:968` |
| ability `beta_a`, home capital `home_effect/ses_home`, own noise `learn_noise` | REPRESENTED | `core.py:54-55,965-966` |
| track quality multiplier (`quality_mult`) | REPRESENTED | `core.py:962` |
| L6/L9 at gates; `E.ALL['L']` | REPRESENTED (snapshots only) | `core.py:992-993`, `E.ALL` |
| **input decomposition** (`dL_school`, `dL_tutoring`, `dL_home`, `dL_ability`, `dL_noise`) | **ABSENT** | no series; components are summed in one line (`core.py:963-966`) |
| substitution/complementarity between S and tutoring (CES / cross-partial) | **ABSENT** | additive; `tut_gain` is a fixed grade-equivalent (`tutoring.py:252`) |
| dose-response / nonlinearity of tutoring | **ABSENT** | constant `tut_effect` per year |
| teacher/school fixed effects, peers | **ABSENT** | single aggregate q; no peer terms |
| explicit exam-performance vs learning mapping | PARTIAL | contest weight uses L (`core.py:452-473`); bar/quota use L+noise (`core.py:996`); no separate test-prep skill |
| `G = max(0, L − S)` (shadow share of learning) | **ABSENT** | needs S and decomposition |
| literacy/learning outcomes | REPRESENTED | `sdg4.py:25-68` (completion, MPL, learning poverty, parity), `measure.py:85` |

### 1.5 Outcome accounting / ledger

| outcome | status | key |
|---|---|---|
| tutoring participation (all / K-12 / G12) | REPRESENTED | `tut_rate`, `tut_k12_rate`, `tut_g12_rate` (`tutoring.py:456-483`) |
| participation by grade / quintile | REPRESENTED | `tut_by_grade`, `tut_by_q`, `tut_k12_rate_by_q` |
| household tutoring spend (all / K-12 / by q) | REPRESENTED | `tut_spend`, `tut_k12_spend`, `tut_k12_spend_by_q` |
| contest-prep household outlay / resource cost / tax / gov receipt | REPRESENTED | `contest_spend_now`, `contest_resource_cost`, `contest_tax_paid`, `gov_tut_receipt` (`tutoring.py:468-471`) |
| own-vs-firm **mix** | PARTIAL | `own_share`, `tut_own_by_grade`, `tut_firm_by_grade`; **`tut_firm_by_grade` includes contest-prep pupils** (`tutoring.py:433`) |
| own-vs-firm **spend split**, own-teacher revenue, firm profit | **ABSENT** | no series |
| school quality / withheld / PTR / teacher pay / pub spending | REPRESENTED | `q_pub`, `withheld`, `ptr`, `teacher_pay`, `pub_spend`, `pub_budget`, `levy`, `rationed` (`schools.py:77-79`) |
| teacher hours / workload, student time use | **ABSENT** | no series (grep: no time/hours params) |
| elite access | PARTIAL | `elite_share`, `track_share`, `elite_prize_mean`, gaps (`labour.py:183-198`, in `E.R`, not in `summary()`); cohort elite-Q5 share is computed by runners from `E.ALL`, not an engine output |
| spending shares / household vs public | REPRESENTED | `household_share_spending` (`sdg4.py:62`), `hh_spend`, `pub_spend` |
| learning decomposition / S / G | **ABSENT** | — |

---

## 2. Probe evidence on the frozen Paper B spec (read-only, host)

Canonical HK/KR (`docs/audit/canonical_spec.json`, N=300, T=46, seed 0, all five modules; measured host runs):

| quantity | HK | KR |
|---|---|---|
| withheld `h` | **0.00000** | **0.00000** |
| `q_pub` / `ptr` / `teacher_pay` | 1.1014 / 23.8 / 3.000 | 1.0986 / 24.0 / 3.000 |
| K-12 tutoring participation | 0.617 | 0.556 |
| own share of tutored | 0.0247 | 0.0282 |
| household K-12 tutoring spend | 156.5 | 128.3 |
| contest effort `contest_e_mean` | 0.0427 | 0.0144 |
| own-report share (grade mean) | 0.0135 | 0.0137 |
| firm-report share (grade mean; **includes contest prep**) | 0.5339 | 0.4761 |
| firm price | 0.0612 | 0.0613 |
| private-school share | 0.117 | 0.107 |
| elite share / elite-Q5 share (cohort) | 0.175 / 0.247 | 0.091 / 0.237 |
| run time (host, 1 proc) | 9.1 s | 19.1 s |

Regime/lever probes (HK base, T=30, measure_from=10, seed 0; deltas isolate one knob):

| probe | h | q | ptr | K-12 tut | own share | K-12 spend | firm price |
|---|---|---|---|---|---|---|---|
| HK-type (canonical knobs, withholding off) | 0.000 | 1.099 | 24.1 | 0.528 | 0.036 | 145.5 | 0.0703 |
| withholding ON (`own_ban=0, pay_ratio=.55, monitoring=.2`) | **0.144** | 1.250 | 11.0 | 0.776 | 0.528 | 165.0 | 0.0701 |
| withholding ON + firm banned (`firm_ban=.9, access=0`) | 0.144 | 1.250 | 11.0 | 0.627 | 0.978 | 118.1 | **2.0957** |
| `withhold_mode='incentive'`, `own_ban=0`, `monitoring=.2` | **0.320** | 1.120 | 22.3 | 0.811 | 0.553 | 168.6 | 0.0700 |
| `q0=0.8` | 0 | 0.879 | 24.1 | 0.605 | 0.029 | 161.7 | 0.0691 |
| `q0=1.2` | 0 | 1.319 | 24.1 | 0.491 | 0.038 | 135.9 | 0.0703 |
| `budget_per_child=.07` | 0 | 0.933 | 46.4 | 0.569 | 0.032 | 155.1 | 0.0705 |
| `budget_per_child=.21` | 0 | 1.212 | 16.3 | 0.516 | 0.037 | 143.0 | 0.0702 |
| firm market shut (`firm_ban=.9`, withholding off) | 0 | 1.099 | 24.1 | 0.056 | 0.530 | 42.4 | 10.2315 |
| `contest_r=0.8` | 0 | 1.099 | 24.1 | 0.419 | 0.040 | 104.1 | 0.0695 |
| `elite_logw=0.2` | 0 | 1.099 | 24.1 | 0.386 | 0.043 | 93.3 | 0.0691 |

KR contest-prep mode probe (N=300, T=30, seed 0):

| mode | `contest_e` | contest spend | K-12 spend | mean L9 | learning added |
|---|---|---|---|---|---|
| positional (default) | 0.0125 | 7.2 | 117.9 | 11.830 | 0 |
| both, `learning_gain=.02` | 0.0127 | 7.3 | 118.0 | 11.830 | 0.91 |
| learning, `learning_gain=.02` | **0.0000** | **0.0** | 110.5 | 11.827 | 0 |
| learning, `learning_gain=.5` | 0.0823 | 47.3 | 156.7 | 12.302 | 147.9 |
| both, `learning_gain=.2`, `pos_share=.5` | 0.0041 | 2.4 | 113.0 | 11.835 | 2.95 |

Reading: (i) Paper B canonical is a *firm-market* regime (own channel ≈ off, withholding ≡ 0); (ii) switching the
withholding regime on changes the supply mix sharply (own share 0.04→0.53; 0.98 with firms banned; firm price ×30
under a ban); (iii) better school provision **reduces** tutoring demand in this calibration (q0 0.8→1.2 lowers K-12
participation 0.605→0.491 and spend 161.7→135.9) — the substitution channel Paper C needs; (iv) `learning` prep mode
with small `learning_gain` is a silent zero-effort arm (and `both` is effectively positional unless the gain is large).

---

## 3. Minimal extension design

Design rule: additive to the frozen spec; new knobs live in the owning module's `defaults`; no existing series renamed;
defaults reproduce today's numerics. Each extension names the equations it implements (inventory numbering and the
minimal set C in §5 of `PAPER_D_EQUATION_AUDIT.md`).

### 3.1 Positive school-effort lever S (homework / feedback / supervision)

Today's effective school input is `S_it = q_it·(1−h_it)·voc·exp(β_a a_i)` (the first term of `core.py:963-965`):
quality is passive, effort is only *negative* (withholding). Minimal positive lever:

* **Params** (PublicSchools.defaults): `school_prep=0.0` (grade-equivalents/yr supplied when unconstrained),
  `school_prep_exam=0.0` (share of S that also raises exam score, not just learning),
  `homework_time=0.10` (student time units per unit S per year),
  `marking_time=0.05` (teacher time units per pupil per unit S),
  `teacher_time=1.0`, `class_time=0.55` (teacher-time budget, §3.2),
  `school_prep_max=1.0` (cap), `school_prep_quad=0` (0 = public only, 1 = state can scale with budget).
* **Supply**: in `PublicSchools.supply` compute `S = min(school_prep_max, school_prep·g(ptr, budget, monitoring))`
  where `g` includes the teacher-time constraint (below); store `y['school_prep']` (array) and `y['school_prep_cost']`.
  Private schools get `priv_school_prep = priv_quality·school_prep` (or a separate `priv_prep`).
* **Learning**: add `+ p['school_prep_gain']·y['school_prep']·exp(β_a a)` to `dL` in `core.py:965` (default
  `school_prep_gain=1` so `school_prep` is already in grade-equivalents). To model substitution/complementarity with
  tutoring (inventory eq 30/31/41) add a switch `production='additive'|'ces'` and
  `dL_tut_eff = y['tut_gain']·(1 − subst·S_norm) + comp·S_norm·y['tut_gain']` (default subst=comp=0 = legacy).
* **Exam performance**: `score` (`core.py:996`) becomes `L + exam_sd·noise + school_prep_exam·S` for bar/quota gates;
  for contest gates optionally add `contest_school_prep` to `x_eff` (`core.py:452-473`). Default 0 = legacy.
* **Demand channel**: `mvl` (`core.py:854`) already capitalises higher L; plus the tutoring utilities should see S
  (school and tutoring are substitutes if `subst>0`): `u_own/u_firm` (`tutoring.py:232-233`) gain `−subst·S` on the
  tutoring marginal product. The buy-back term already couples h and tutoring (`h·q`).
* **Ledger/outcome rows** (`E.note`): `school_prep_mean`, `school_prep_by_q`, `school_prep_cost_teacher_hours`,
  `dL_school_mean`, `dL_tut_mean`, `dL_home_mean`, `dL_noise_mean` (see §3.3).
* **Identities** (assert in code): `school_prep >= 0`; `school_prep_cost_teacher_hours <= teachers·teacher_time`;
  `sum(school_prep over pupils)` reconciles with `teacher_hours_marking`.

### 3.2 Time budgets (students and teachers)

Absent today: `cash` (`core.py:933-935`) is the only household constraint; tutoring/contest effort are cash-bound
only; teachers are a headcount (`schools.py:47,60`) with no hours.

* **Student time** (PublicSchools + TutoringMarket shared): total `1.0` per year, params (PublicSchools.defaults, read
  by tutoring through `E.p`): `student_time=1.0`, `time_school=0.55`, `homework_time=0.10` (per unit S),
  `time_tut_unit=0.15` (time per firm/own tutoring year), `time_prep_unit=0.05` (time per unit contest effort).
  Constraint in `TutoringMarket.extras`: `time_left = student_time − time_school − homework_time·S`;
  `e_hi = min(e_cap, cash_rem/unit_outlay, time_left/time_prep_unit)`;
  own/firm `cash` affordability (`tutoring.py:236-238`) becomes `min(cash, time_left/time_tut_unit)`; store
  `E.yr['student_time_used']`, `E.yr['time_binding']`.
* **Teacher time**: `teacher_time=1.0`, `class_time=0.55` per pupil-year, `marking_time` per unit S. In
  `PublicSchools.supply`: `teacher_hours = T·teacher_time`; `used = pupils·(class_time + marking_time·S)`;
  if `used > teacher_hours`, solve `S` down until `used = teacher_hours` (or raise class size / withheld), record
  `teacher_hours`, `teacher_hours_marking`, `class_size_binding`. Ledger identity:
  `pub_spend = T·wT + (1−salary_share)·B` (already `schools.py:76`) and `teacher_hours_used <= T·teacher_time`.
* **Household budget with time**: inventory eq 12/70/21 combined; the household problem already uses
  `cash/need` (`core.py:933-935`, `values` recursion `core.py:626/635`); time enters only through the caps above, so
  no change to `values()` is needed in wave 1 (documented partial equilibrium).
* **Outcome rows**: `student_hours_school/homework/tutoring/prep`, `teacher_hours_supply/used/marking`,
  `time_binding_share`, `teacher_time_binding`, by quintile.

### 3.3 Explicit `L` and learning decomposition

Current `L` is an additive cumulative sum with no recorded components (`core.py:960-968`). Minimal explicit form
(Paper C/D minimal equation set, C1–C3):

```
L_it = L_i,t-1 + S_it + T_it + F_it + ε_it                                  (C1, additive baseline)
S_it = q_it·(1−h_it)·v_it·exp(β_a a_i) + σ·hw_it                           (C2, school-supplied prep; hw = positive eff.)
T_it = θ_own·own_it + θ_firm·firm_it + θ_prep·e_it                         (C3, shadow-education prep)
G_it = max(0, L_it − Σ_{τ≤t} S_iτ)                                          (C4, shadow-education share of learning)
```
* **Implementation**: split the `dL` line (`core.py:963-966`) into named arrays
  `dL_school, dL_tut, dL_home, dL_noise` (and `dL_ability = dL_school·(exp(β_a a)−1)` if a separate ability term is
  wanted); record annual cohort means and per-quintile means via `E.note`; keep `k['L'] += dL` unchanged so numerics
  are identical in the default configuration.
* **Optional CES/nested production** (inventory eq 30): `dL = [ω·S^ρ + (1−ω)·T^ρ]^{1/ρ} + F + ε` behind
  `production='ces'` with `ces_rho` (ρ=1 reproduces additive only if ω admits linear weights; document the mapping),
  `ces_omega`. Record Shapley/marginal contributions rather than additive components under CES.
* **Explicit L outputs**: `L` at each gate (L6/L9 exist, `core.py:992-993`; add `L12` at the G12 gate), plus
  `L_mean_by_q`, `L_gain_school/tutoring/home`, `mpl_*` already from `sdg4.py:48-56`.
* **Gate mapping** (explicit test-prep vs learning): bar/quota `score = L + exam_sd·noise + school_prep_exam·S`
  (`core.py:996`); contest `x_eff = x0·L/ends + α·prep_stock` (`core.py:452-473`) optionally plus
  `school_prep_contest`. This makes "learning" L and "positional prep" separate objects, which is required to define
  G without circularity.

### 3.4 Supply-form equilibrium and the three regimes

The engine is a *partial*-equilibrium simulation with household demand + mechanical supplier rules. The minimal
supply-form extension (inventory eq 83/84/85) is accounting, not new optimisation:

* own teacher: supply rule = availability `1−own_ban`, price `p_own`, capacity unlimited but tied to withholding
  (only own pupils); record own-teacher revenue `p_own·own`, rent from withholding `(p_own−cost)·own`.
* firm: entry/capacity already (`tutoring.py:242-250`) — add `firm_cost`, `firm_markup`, profit
  `pi = firm_rev − cost·Q`, utilisation `D/K`, unmet demand by quintile.
* state: S supplied by public schools; record public unit cost and the effective S subsidy.
* welfare/policy block (optional Paper C outcome): social welfare `SW = Σ ω_i U_i − λ·C_public` (inventory eq 183)
  with `ω_i` from `k['q']`, λ as a parameter; requires utilities comparable across types (document the
  cardinalisation).

Three supply regimes as data bundles (all existing knobs except S/time extensions; canonical Paper B is R2 with
withholding off):

| | R1 own-teacher withholding (Cambodia-type) | R2 private market (HK-type, Paper B) | R3 state supply (China-type) |
|---|---|---|---|
| `own_ban` | 0.0 | 0.95 | 0.90 |
| `monitoring` | 0.2 | 0.9 | 0.6 |
| `pay_ratio` | path 0.40→0.85 | 1.2 | 1.0 |
| `h_max` | 0.4 | 0.4 | 0.4 |
| `firm_ban` | 0.0 | 0.0 | 0.88 (post-2021) |
| `firm_entry` / `p_firm` | 0.3 / 0.06 | 0.3 / 0.06 | 0.3 / 0.06 |
| `urban_share` / `rural_firm_access` | 0.2 / 0.4 | 1.0 / 0.4 | 0.5 / 0.4 |
| S (`q0`, budget, positive lever) | low (q0 0.85) | mid (q0 1.0) | high (q0 1.1 + budget path + school_prep) |
| gates | bar/retake (Bac II) | contest G12 (DSE) | quota + gaokao bar (high stakes) |
| predicted supply form | own-teacher buy-back dominant, firm small | firm dominant, own ≈ 0 | state S dominant, firm sharply restricted, own residual |
| anchor | Cambodia pack (`countries/cambodia.py`) | `canonical_spec` HK | China pack (`countries/china.py`) |

Add a PH-type variant as R2b: low-cost private schools + modest tutoring (`priv_quality=1.05`, `p_firm` low,
`own_ban` low, `fee_public` low, urban share 0.45) — this is the HK-vs-PH contrast (§5).

---

## 4. Proposed experiment grid (Paper C confirmatory design)

Factors (orthogonal, so S, L and private supply vary *separately*; regimes enter as anchors):

* **S (school-supplied prep)**: `q0 ∈ {0.80, 1.00, 1.20}` (probe range is clean; q0 scales q 1:1 and also scales
  private quality — document that S is school-sector-wide). If the §3.1 extension lands, add a second S axis
  `school_prep ∈ {0, 0.05, 0.10}` with time budget.
* **L (gate pressure)**: 3 levels per regime — HK: contest `share ∈ {0.12, 0.23, 0.35}`; KR: G9 contest
  `share ∈ {0.25, 0.35, 0.50}` (or fixed_bar `bar`); keep `contest_r`/`elite_logw` at their regime anchors so the
  axis is one-dimensional. `exam_sd` is *not* an L lever for contest gates (it does not enter PL weights).
* **Private supply**: 4 levels — `own_open_gap` (`own_ban=0, pay_ratio=.55, monitoring=.2`; h>0, own market open),
  `mixed` (`own_ban=.5, firm_ban=0, firm_entry=.3`), `firm_market` (`own_ban=.95, firm_ban=0`), `state_restricted`
  (`own_ban=.9, firm_ban=.9`).
* **Regimes**: anchors R1/R2/R3 (+R2b PH) held at their data-bundle values.

Design: full 3 (S) × 3 (L) × 4 (supply) = **36 cells** × 8 matched seeds = **288 runs** (matches the Pilot-0 size),
plus 4 regime anchors × 8 = 32 runs for the regime comparison = **320 runs**. Suggested N/T: **N=600, T=46** for the
screening stage; **N=1500, T=46** for the confirmatory stage on the subset of cells that show effects.
(If the §3.1/§3.2 extensions land, add a 3-level `school_prep`/time-budget axis on the R2 anchor only: +2 axes ×
9 cells × 8 seeds = 144 runs.)

Compute estimate (from host measurements: HK N=300/T=46 = 9.1 s, KR = 19.1 s; contest-cell cost scales with
candidate count and seats; N=600 ≈ 2×, N=1500 ≈ 5×, T=30 ≈ 0.65×; add 20 % margin for contest cells):
* screening 320 runs at N=600/T=46, avg ≈ 25 s ⇒ **≈2.2 CPU-h** (≈1.1 h wall at 2 CPUs, ≈20 min at 8);
* confirmatory 36 cells × 16 seeds = 576 runs at N=1500/T=46, avg ≈ 75 s ⇒ **≈12 CPU-h** (≈6 h at 2 CPUs,
  ≈1.5 h at 8); reduce to N=1000 (≈50 s) if time-boxed.
* Paper D divergence tests reuse the same cells; the 8 targeted tests need ≈ **350–500 extra runs** at N=600/T=30
  (≈2–3 CPU-h).

Outcome rows to pre-register (all already emitted unless marked new): K-12/G12 tutoring participation and spend
(`tut_k12_rate`, `tut_g12_rate`, `tut_k12_spend`), participation/spend by quintile (`tut_k12_rate_by_q`,
`tut_k12_spend_by_q`), own-vs-firm mix (`own_share`; new: own/firm spend split), school `q_pub`/`withheld`/`ptr`/
`teacher_pay`, contest `contest_e_mean`/`contest_admit_rate`/`contest_expected_p_mean`, elite/track access
(`elite_share`, `track_share`, `E.ALL['elite']` by q), learning (`mpl_lower`, `completion_*`, `E.ALL['L6','L9']`;
new: L decomposition, S, G), new time rows if the extension lands.

---

## 5. Data needs: HK vs PH (and what stays theory-only)

Programme rule (LEAD_GROUND_TRUTH §6): every benchmark carries citation + survey year + population + denominator. The
inventory is a candidate map, **not** a verified bibliography — the same caution applies to data sources: every source
below must be verified (title, year, table, denominator) before it enters a prereg.

### 5.1 HK (the high-firm-market, high-stakes case)

Needed to calibrate/validate R2 and the emergence margin:
* tutoring participation and **monthly expenditure per child, by household income quintile** (participation split by
  grade band: primary / junior / senior; hours/week; subjects). Programme benchmark currently cited: HK Grade 9
  **53.8 %**, Grade 12 **71.8 %** (2011/12 survey) — **citation/denominator to verify** (likely HK Census & Statistics
  Department thematic household survey; do not cite until checked).
* **own-teacher vs commercial provider** split and price paid — may not be separable in the HK survey; if absent, the
  supply-form parameter (`own_ban`, `p_own/p_firm`) is theory-only for HK and only the total supply margin is usable.
* school provision: PTR, teacher pay, public spending per pupil (existing education statistics); public exam
  admission rates (DSE/university seats) for seat scarcity; PISA 2018/2022 HK learning scores for the L anchor.
* household income distribution (for quintiles) and the fee regime (`fee_public=0` in canonical).

### 5.2 PH (the low-cost-private, weaker-regulatory contrast)

* **No national tutoring survey is assumed.** Candidate sources to verify: PSA Family Income and Expenditure Survey
  (education expenditure, usually no tutoring line), Annual Poverty Indicators Survey, SEA-PLM (Philippines
  participation and any private-tutoring/after-school item — verify), PISA 2018 Philippines (verify after-school
  lesson items), DepEd school statistics (PTR, teacher pay), private-school fee schedules.
* Critical missing for the PH contrast: tutoring **participation/expenditure by income** and **supply form**
  (own teacher vs low-cost private vs commercial); teacher pay relative to outside wage (for h); seat scarcity
  (senior-high/college admission). Without the first two, PH can only support the *state/low-cost-private* regime
  qualitatively, not a calibrated comparison.

### 5.3 Theory-only until data arrive

Withholding magnitude `h` / buyback share, teacher effort response (inventory eq 175–177), firm entry and
price elasticity (eq 83–84), time budgets (eq 21 + teacher time), S production elasticity and S×T substitution
(eq 30–31), positional-externality size and welfare ranking (eq 81–83, 183), and the welfare weights for eq 183.
These are declared as structural placeholders with sensitivity grids (the Paper C prereg must state that they are
not estimates).

---

## 6. Inventory mapping (§2/§3/§5 → engine) — summary

Full classification (identity / stylized theory / empirical spec / incomplete-for-mechanism), assumptions and
divergence tests are in **`PAPER_D_EQUATION_AUDIT.md`**. The Paper-C-relevant core:

| inventory eq (section) | engine implementation / param (file:line) | status for Paper C |
|---|---|---|
| 12, 19, 24, 70 (budget/borrowing) | `cash/need` `core.py:933-935`; `borrow` | PARTIAL (cash only, no time; no collateral) |
| 13–18 (NPV/IRR) | implicit value recursion `core.py:626/635`; `delta`, `kappa` | PARTIAL (no r/IRR output; `prior_logw` beliefs) |
| 20 (`H_{t+1}=(1−δ)H_t+I_t`) | `k['L'] += dL` `core.py:960-968` | REPRESENTED with δ=0; components not recorded |
| **21 (time allocation)** | — | **ABSENT** (the key missing constraint) |
| 22 (participation logit) | continue decision `core.py:926`; tutoring argmax `tutoring.py:239-241` | REPRESENTED (structural discrete choice) |
| 23, 25 (choice/optimal private) | school choice `schools.py:117-134`; tutoring choice `tutoring.py:232-241` | PARTIAL (2 sectors, 3 supplier options) |
| 26, 27 (production `A=f(S,F,θ)`) | `dL` `core.py:963-966` | PARTIAL (additive, no decomposition) |
| 28 (Cobb-Douglas), 30 (CES), 31 (complementarity) | none | **ABSENT** (`production='additive'` only) |
| 29 (`MP_T`) | `mvl` `core.py:854`; constant `tut_effect` `tutoring.py:252` | PARTIAL (value of learning ≠ marginal productivity of tutoring) |
| 32, 33 (value-added/lagged) | `dL`, `L_t+1` | PARTIAL (additive increments, no dynamics beyond cumulative) |
| 37 (class size) | `q(ptr)` `schools.py:49` | REPRESENTED (public) / ABSENT for private q |
| 38–40 (skill formation, complementarity) | none explicit | PARTIAL (self-productivity implicit; dynamic complementarity absent) |
| 41, 72, 80 (S×T interaction) | demand side: `h·q` buy-back `tutoring.py:232-233`; achievement side: none | PARTIAL — **the key Paper C gap** |
| 57–63 (participation/spending models) | structural demand `tutoring.py:232-241` | engine mechanism represented; equations are estimation specs (measurement) |
| 64–69 (shares, Engel, elasticities) | outputs `tut_k12_spend_by_q`, `tut_k12_rate_by_q` | measurement: computable from runs, not parameters |
| 71–76 (tutoring in production/dose/SES) | fixed effect `tut_effect`; SES through cash/income | PARTIAL (no dose-response) |
| 81 (contest success `P_i=e_i^κ/Σe_j^κ`) | PL top-K with seats + expected P (`core.py` PL API) | ALTERNATIVE REPRESENTED (multi-seat PL, not single-prize power form) |
| 82 (household contest choice) | contest effort `tutoring.py:334-380` | REPRESENTED |
| 83, 84, 85 (market equilibrium/profit/tax) | firm entry/capacity `tutoring.py:242-250`; `firm_rev`; `contest_tax_rate` | PARTIAL (no profit/clearing; tax only on contest prep) |
| 86 (reduced-form policy) | — | estimation only (Paper B/A designs) |
| 175–177 (teacher effort/incentive) | `h` mechanical rule `schools.py:52-54` | PARTIAL — S/effort lever candidate |
| 178–179 (school choice/capacity) | `schools.py:117-134`; firm capacity | REPRESENTED |
| 183 (social welfare) | — | ABSENT — Paper C welfare block candidate |

**Attribution risk (binding):** the inventory is an AI-generated candidate map with placeholder citations
("UIS+2", "OECD+3", "doi.org+4", "hanushek.stanford.edu+2", "World Bank+2"). Do **not** cite equation numbers as if
they came from a verified source; before integration each equation's origin (Hanushek; Todd & Wolpin; Cunha & Heckman;
Becker; Mincer; Dang & Rogers; Bray; Tansel & Bircan; Biswal; Jayachandran; Kim & Lee; and the measurement sources UIS,
World Bank, OECD) must be checked against the primary text. Committed at
`docs/audit/refs/education-equation-inventory-20261124.txt` (sha256 `0fd30f77…52df`) with
`docs/audit/refs/README.md` recording the caveat.

---

## 7. Implementation plan and residual risks

1. **Wave 1 (this design):** pilot uses existing switches only (q0 for S, gate share/bar for L,
   own_ban/firm_ban/pay_ratio/monitoring/withhold_mode for supply). No engine change, no box job.
2. **Wave 2 (extension, if Paper C proceeds):** implement §3.1–§3.4 in this order — learning decomposition (no
   numerics change), positive S lever + time budgets (new defaults off = legacy), supply-form accounting, then
   explicit L/CES switch. Each requires `ENGINE_CHECKS.py` additions and a new engine hash + canonical re-pin.
3. **Residual risks:** (i) q0 scales both sectors, so S is not public-only until the S extension lands; (ii) the
   canonical spec cannot identify withholding/own-teacher mechanisms (h≡0, own≈2.5 %) — the Paper C prereg must
   switch regimes, not just vary q0; (iii) `tut_firm_by_grade` conflates firm tutoring with contest prep — use
   `own_share` or add the spend split; (iv) `contest_prep_mode='learning'` is inert at small `learning_gain`;
   (v) no provider profit/clearing or time budgets, so supply-form welfare statements are theory-only in wave 1;
   (vi) all benchmarks data sources are unverified until checked (inventory is not a bibliography).
