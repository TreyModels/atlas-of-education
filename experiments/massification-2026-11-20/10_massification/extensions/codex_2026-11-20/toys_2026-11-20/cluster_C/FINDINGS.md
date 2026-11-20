# FINDINGS — Cluster C toys (#7 capacity by level, #8 enforcement × law, #9 buildings vs teachers)

**ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no historical test; phase closed; do not cite numbers as estimates.**

These three simulations were built to the Council specification (`COUNCIL_TOY_SPECS_015.md`, Cluster C, experiments
#7–#9) and to the pre-declarations frozen in `PRE_DECLARATIONS.md` (`sha256 b0b0bde…`) **before** the run. Nothing
below is evidence about the Philippines, about massification, or about any historical episode. Every number is a
property of the stipulated rules in `code/cluster_c_model.py`. The massification phase remains CLOSED (closeout
`787f1792…`); this run does not reopen it, and no phase file, closed-anchor file or results table was read for values
or written.

---

## 0. What was run

| Item | Value |
|---|---|
| Seeds per cell | **200** (`20261120 … 20261319`), pre-declared; every cell |
| Pairing | identical latent draws across arms within a seed (checked by `code/selftest.py`) |
| Starting conditions | identical per experiment (same base seats; same 30 rooms / 2 posts; same no-law baseline) |
| Shocks | exactly one imposed parameter per arm |
| Language | Python 3.10.2, standard library only (`numpy` installed but not imported) |
| Runtime | 8.0 s for all three experiments; two independent runs produced **byte-identical** `RESULTS.csv` (`sha256 af88933…`) |
| Output rows | 375 result rows in `RESULTS.csv`, all cells including null, censored and failed cells |

Verdict summary: **20 verdicts — 15 PASS, 2 FAIL, 3 falsifiers clear** (not fired). `RESULTS.csv` also carries a
per-clause status tally (16 PASS / 3 FAIL) because the failed T7e is split into its two declared clauses. The two
experiments with a clean sweep (#8, #9) pass every pre-declared threshold; **#7 fails two of its six thresholds**, and
both failures are reported in full in §1.4. That asymmetry between experiments is itself worth noting: the thresholds that failed are the ones I made
*auxiliary and quantitative* (a conversion-rate cap, an any-level universalization clause), not the ones that restate
the A10-style claim.

---

## 1. Experiment 7 — capacity by level (floor / ceiling split)

**Design (stipulated).** 30 cohorts of 120 children; three sequential levels. Admission at level *k* requires
`cash ≥ fee_k` and `ready_ik + 0.15·aptitude_i + 0.15·stock_k ≥ gate_k`; a used seat is a completion. Capacity is
doubled at the shocked level(s), phased over cohorts 1–4, permanent after. Floor = primary completion; ceiling =
tertiary completion. Every level's seats are exactly binding in control (utilization 1.000), so the binding
precondition in the pre-declaration is satisfied.

### 1.1 Cohort-30 completions (seed means, 200 seeds)

| Arm | primary | secondary | tertiary | floor pp | middle pp | ceiling pp | floor−ceiling pp | util P / S / T |
|---|---|---|---|---|---|---|---|---|
| `control` | 55.00 | 20.00 | 7.00 | 45.83 | 16.67 | 5.83 | 40.00 | 1.000 / 1.000 / 1.000 |
| `primary_only` | 108.32 | 20.00 | 7.00 | 90.27 | 16.67 | 5.83 | 84.43 | 0.985 / 1.000 / 1.000 |
| `secondary_only` | 55.00 | 34.05 | 7.00 | 45.83 | 28.38 | 5.83 | 40.00 | 1.000 / **0.851** / 1.000 |
| `tertiary_only` | 55.00 | 20.00 | 12.49 | 45.83 | 16.67 | 10.41 | 35.43 | 1.000 / 1.000 / **0.892** |
| `all_levels` | 108.32 | 40.00 | 14.00 | 90.27 | 33.33 | 11.67 | 78.60 | 0.985 / 1.000 / 1.000 |

Paired gains vs `control` (pp, 95 % CI over 200 paired seeds):

| Arm | floor | middle | ceiling | ceiling gain / floor gain |
|---|---|---|---|---|
| `primary_only` | **+44.43** [+44.19, +44.68] | 0.00 | **0.00** [0.00, 0.00] | 0.000 |
| `secondary_only` | 0.00 | **+11.71** [+11.29, +12.12] | 0.00 | undefined (no floor gain) |
| `tertiary_only` | 0.00 | 0.00 | **+4.58** [+4.38, +4.77] | undefined (no floor gain) |
| `all_levels` | +44.43 | +16.67 | +5.83 | 0.131 |

### 1.2 Crossing behaviour (cohort of first crossing; `>30` = censored, never reached)

| Arm | floor 0.25 | floor 0.50 | floor 0.90 | middle 0.25 | middle 0.50 | ceiling 0.25 | ceiling 0.50 / 0.90 |
|---|---|---|---|---|---|---|---|
| `control` | 1 | >30 | >30 | >30 | >30 | >30 | >30 |
| `primary_only` | 1 | **2** | 9.82 | >30 | >30 | >30 | >30 |
| `secondary_only` | 1 | >30 | >30 | **3.27** | >30 | >30 | >30 |
| `tertiary_only` | 1 | >30 | >30 | >30 | >30 | >30 | >30 |
| `all_levels` | 1 | **2** | 9.82 | **3.00** | >30 | >30 | >30 |

`9.82` is the seed mean of an integer crossing year: the floor sits just above the 0.90 bar at its peak (90.46 pp), so
some seeds cross at cohort 9 and some at 10. The ceiling never crosses even the 0.25 bar in any arm, at any cohort —
that is the A10/R29 timing censoring reappearing in the toy's own terms.

### 1.3 Verdicts (as pre-declared, evaluated mechanically)

| ID | Verdict | Observed |
|---|---|---|
| T7a floor moves ≥ +10 pp, CI > 0 | **PASS** | +44.43 pp [+44.19, +44.68]; primary utilization 1.000 |
| T7b tertiary-only moves ceiling ≥ +2 pp | **PASS** | +4.58 pp [+4.38, +4.77]; tertiary utilization 1.000 |
| T7c secondary-only: middle ≥ +3 pp **and** < 50 % seat conversion | **FAIL** | middle +11.71 pp ✓ but conversion 11.71 / 16.67 = **70.2 %**, above the 8.33 pp cap |
| T7d primary-only: ceiling ≤ +2 pp and ≤ 0.25 × floor | **PASS** | ceiling +0.00 pp = 0.000 × floor (mechanically forced, see §1.5) |
| T7e no ceiling ≥ 50 pp **and** no level ≥ 90 pp | **FAIL** | clause (i) ceiling max 11.67 pp ✓; clause (ii) any-level max **90.46 pp** ✗ (the *floor*) |
| T7f floor crosses 0.50, ceiling censored everywhere | **PASS** | floor crossing observed in 1.00 of seeds; ceiling 0.50 crossing observed in 0.00 |
| F7 (fires ⇒ contradicts A10) | **not fired** | floor-moving arms: `primary_only`; of these, ceiling ≥ floor: none; ceiling universalization: false |

### 1.4 The two failures, stated plainly

- **T7c failed on the conversion cap, not on the direction.** Adding 20 secondary seats converted 14.05 of them into
  completions (70.2 %), so secondary capacity did **not** saturate: 15 % of the added seats stood idle
  (utilization 0.851) but the rest found qualified applicants. My pre-declared expectation that the middle level
  would convert < 50 % of added seats was **wrong**. The lesson the toy actually teaches is the opposite of the one I
  wrote down: saturation is not a property of a *level*, it is a property of the *gate* (fee plus readiness plus the
  size of the eligible pool). Where the gate leaves a large qualified pool, seats convert; where the pool is thin
  (the ceiling), seats sit idle even after doubling.
- **T7e failed on a wording defect in my own pre-declaration.** Clause (i) — the ceiling clause, the one the
  experiment is about — passes comfortably (max ceiling share 11.67 pp over every arm and cohort). Clause (ii), which
  I wrote as "no arm reaches the 0.90 universalization bar at any level", fails because capacity *does* nearly
  universalize the **floor** (90.46 pp peak) — which is exactly the A10/R29 "capacity moves the floor" reading, not
  a contradiction of it. I did not edit the threshold after seeing the result; both clauses are reported separately
  in `RESULTS.csv` (`T7e_i_ceiling_below_50pp` = PASS, `T7e_ii_no_level_at_90pp` = FAIL) and the combined verdict is
  the literal FAIL. Read as intended (ceiling clause only), the A10-style claim survives; read literally, my own
  sentence was too broad.

### 1.5 Cell that is mechanically forced (flagged, not counted as support)

`primary_only`'s ceiling gain is **exactly 0.00 pp** in all 200 seeds. This is forced by the seat chain: primary
seats rise but secondary seats are unchanged, secondary completions are pinned at 20, so the tertiary eligible pool
is identical to control and tertiary completions are pinned at 7. The cell is informative about *where the binding
constraint sits* — it is a chain, and a shock at the bottom does not pass through an unchanged middle — but it is not
a discovery, and it is excluded from any "support" language.

### 1.6 What #7 illustrates (and what it cannot)

- **Illustrates:** a capacity shock at one level moves that level's completions and can move the floor towards
  universality (45.83 → 90.27 pp) while the ceiling does not move at all (+0.00 pp) and no arm at any budget reaches
  a ceiling above 11.67 pp. Doubling **every** level still leaves the ceiling at 11.67 pp (14 children of 120),
  because the ceiling is gated by eligibility (secondary completers × readiness × fee), not by seats alone. The
  floor−ceiling gap *widens* under a floor-only shock (40.00 → 84.43 pp).
- **Cannot:** say anything about whether real capacity programmes move real ceilings; the gate parameters are
  stipulated; there is no price, no labour market, no quality margin, no dropout, and the "completion = seat used"
  identity is a modelling convenience, not a fact about schooling.

---

## 2. Experiment 8 — enforcement × compulsory law

**Design (stipulated).** One cohort of 120 households; de jure law `L ∈ {0,1}` × declared enforcement
`e ∈ {0, 0.5, 1}` (inspection-and-sanction intensity, declared not measured). The statute carries a small stipulated
norm effect (`0.010`) so that "paper law ≈ no law" is a testable margin rather than an algebraic identity, and a
larger register-only effect (`0.10`). Enforcement multiplies both attendance pressure and verified-learning quality.

### 2.1 Cells (seed means, 200 seeds; gains paired vs no-law in brackets)

| Cell | registration pp | attendance pp | completion pp | household work (units) |
|---|---|---|---|---|
| `no_law` (0,0) | 29.94 | 44.64 | 18.90 | 0.366 |
| `law_e0` (1,0) | 39.85 (+9.91) | 45.73 (**+1.09** [+0.95, +1.23]) | 19.41 (**+0.51** [+0.42, +0.60]) | 0.363 (−0.0031) |
| `law_e05` (1,0.5) | 47.49 (+17.55) | 54.35 (+9.71) | 28.21 (+9.31) | 0.337 (−0.029) |
| `law_e1` (1,1) | 55.04 (+25.10) | 63.27 (**+18.63** [+18.09, +19.17]) | 39.18 (**+20.29** [+19.77, +20.81]) | 0.309 (−0.0565) |
| `no_law_e05` (0,0.5) | 29.94 (0.00) | 44.64 (0.00) | 18.90 (0.00) | 0.366 (0.00) |
| `no_law_e1` (0,1) | 29.94 (0.00) | 44.64 (0.00) | 18.90 (0.00) | 0.366 (0.00) |

### 2.2 Verdicts

| ID | Verdict | Observed |
|---|---|---|
| T8a paper law inert in the classroom (|att| ≤ 2 pp, comp ≤ +1 pp) | **PASS** | attendance +1.09 pp, completion +0.51 pp |
| T8b enforced law binds (att ≥ +10, comp ≥ +6) | **PASS** | attendance +18.63 pp, completion +20.29 pp |
| T8c enforcement gates (monotone, ≥ 4×, gap ≥ +8 pp) | **PASS** | 1.09 → 9.71 → 18.63 pp; ratio 17.06×; gap +17.54 pp |
| T8d work falls only where attendance rises (≥ 3×) | **PASS** | work reduction 18.17× larger at e=1 than at e=0 |
| F8 (fires ⇒ law binds without enforcement) | **not fired** | law-alone attendance gain 1.09 pp, far inside the 2 pp equivalence band |

### 2.3 What #8 illustrates

- **The de jure / de facto split is the whole result.** A statute with no enforcement moves the **register** by
  +9.91 pp and the **classroom** by +1.09 pp — register-based compliance measures would overstate the effect about
  nine-fold. Attendance and completion then rise monotonically with declared enforcement, and enforcement without a
  statute does exactly nothing (0.000 pp in all eight metrics, by construction of the mapping — a built-in null, not
  a finding).
- **Completion responds more than attendance** (+20.29 pp vs +18.63 pp): enforcement also raises completion *given*
  attendance, because inspection verifies instruction, not just presence. An attendance-only monitoring story would
  slightly understate the completion response. This is a stipulated channel, labelled as such.
- **Household work falls only with enforcement** (0.366 → 0.309 units), i.e. the toy's "cost" of the law is paid by
  households, and only where the law actually binds.
- **Cannot:** say what the real enforcement elasticity is (e is declared, not measured); audit data for de jure law
  on the books exists, but this toy supplies no estimate of compliance with it.

---

## 3. Experiment 9 — buildings vs teachers at equal budget

**Design (stipulated).** Fixed budget `B = 480` units in every purchase arm (`rooms·12 + posts·60 = 480`; invariant
asserted in code and in `selftest.py`). Matched stock: 30 physical places, 2 teacher posts. Retention
`π ∈ {0.60, 0.90}` scales effective teachers; staffed places = min(physical, effective-teacher capacity, 120);
completions = admitted children whose pass draw clears a quality threshold that depends on teacher load.

### 3.1 Cells (seed means, 200 seeds)

| Cell | physical places | staffed places (admissions) | completions | completion pp | PTR declared | PTR effective |
|---|---|---|---|---|---|---|
| `baseline`, π=0.60 | 30 | 14 | 12.74 | 10.62 | 7.00 | 11.67 |
| `baseline`, π=0.90 | 30 | 21 | 19.12 | 15.93 | 10.50 | 11.67 |
| `rooms_only`, π=0.60 | **70** | 14 | 12.74 | 10.62 | 7.00 | 11.67 |
| `rooms_only`, π=0.90 | **70** | 21 | 19.12 | 15.93 | 10.50 | 11.67 |
| `teachers_only`, π=0.60 | 30 | 30 | 27.40 | 22.83 | **3.00** | **5.00** |
| `teachers_only`, π=0.90 | 30 | 30 | 27.40 | 22.83 | **3.00** | **3.33** |
| `split`, π=0.60 | 50 | 43 | 39.35 | 32.79 | 7.17 | 11.94 |
| `split`, π=0.90 | 50 | 50 | 45.79 | **38.16** | 8.33 | 9.26 |

### 3.2 Verdicts

| ID | Verdict | Observed |
|---|---|---|
| T9a rooms without staff (physical ≥ +30, staffed ≤ +2, comp ≤ +1 pp) | **PASS** (both π) | physical +40; staffed +0.00; completion +0.00 pp |
| T9b split dominates rooms (staffed ≥ +20, comp ≥ +5 pp) | **PASS** (both π) | staffed +29.00; completion +22.18 / +22.23 pp |
| T9c composition matters (split − teachers ≥ 3 pp; teachers' gain ≤ 70 % of split's) | **PASS** (both π) | +9.96 pp (share 0.55) / +15.33 pp (share 0.31) |
| T9d retention binds only where teachers bind | **PASS** | retention gain: split +5.37, baseline +5.32, rooms_only +5.32, teachers_only **+0.00** pp |
| F9 (fires ⇒ rooms alone raise completion) | **not fired** | rooms_only completion gain 0.00 pp ≤ 1 pp |
| D9 diagnostic: teachers_only has the best PTR but not the best completion | **holds** | lowest PTR (declared 3.00, effective 5.00/3.33) yet 22.83 pp vs split's 32.79/38.16 pp |

### 3.3 What #9 illustrates

- **Equal money, unequal places.** 480 units of rooms buys +40 physical places and **zero** usable ones; the same
  money in salaries buys +16 staffed places (π=0.60) or +9 (π=0.90); half-and-half buys +29 at *both* retention
  levels. The split dominates both pure strategies at the same budget — composition, not just spend.
- **Retention is not a free-floating quality parameter:** it raises completions exactly in the arms where teachers
  are the binding constraint (baseline, rooms_only, split: +5.3 to +5.4 pp) and does nothing in `teachers_only`
  (+0.00 pp), where 30 physical places bind. A toy-level restatement of "complementarity determines which margin
  matters".
- **PTR is a misleading indicator.** `teachers_only` has the best pupil–teacher ratio in the table (3.00 declared,
  3.33 effective at high retention) and completes 22.83 pp, below `split` at 32.79–38.16 pp. A good PTR can describe
  idle teachers behind unusable rooms.
- **Mechanically forced cell (flagged):** `rooms_only`'s completion gain is exactly 0.00 pp because the stipulated
  production function has no unstaffed-seat channel at all. It is the clearest illustration of the complementarity
  the experiment is about, but it is an artefact of the specification, not a result — see §4.
- **Cannot:** price a real classroom or a real teacher post (the spec's DATA ASK stands: the toy cannot settle real
  construction cost); say whether real buildings programmes are staffed or not.

---

## 4. Failures, anomalies and cells that are forced

Complete list; nothing suppressed or re-rolled.

1. **T7c FAIL** — secondary capacity converted 70.2 % of added seats, above the pre-declared 50 % cap. Direction as
   predicted, magnitude of saturation not.
2. **T7e FAIL (literal wording)** — clause (ii) trips at the *floor* (90.46 pp ≥ 90), not at the ceiling (11.67 pp).
   Clause (i) passes. Pre-declaration wording defect; threshold not edited.
3. **34 censored crossing cells** in `RESULTS.csv` (`status=censored`) — all ceiling crossings at every bar, all
   middle crossings above 0.25, and control's floor 0.50/0.90 crossings. Reported as `>30`, never as a number.
4. **2 `undefined_no_floor_gain` cells** — the ceiling/floor gain ratio where the arm does not move the floor
   (division by zero); recorded as 0 with an explicit status, not silently dropped.
5. **Mechanically forced cells** flagged in §1.5 and §3.3 (`primary_only` ceiling 0.00 pp; `rooms_only` staffed and
   completion 0.00 pp; enforcement-without-law 0.000 pp; T9d's baseline/rooms_only retention gains).
6. **Pre-declaration deviation #1** (F7 applicability condition, before the run) is logged in
   `PRE_DECLARATIONS.md` §5 with the 3-seed smoke test that motivated it. No PASS/FAIL threshold was changed.

---

## 5. Cross-cutting reading — three mechanisms the toys can *illustrate*

**All three are properties of the stipulated rules.** They are candidate hypotheses for real-data tests, not
findings.

1. **Capacity migrates the bottleneck upward; it does not remove it.** In #7 a floor-only shock moved the floor
   44.43 pp and the ceiling 0.00 pp; a ceiling-only shock moved the ceiling 4.58 pp and nothing else; even doubling
   every level left the ceiling at 11.67 pp. The constraint that survives capacity is the *gate* (eligibility,
   affordability, progression), which is why a capacity-only programme can look like "floor universalization" while
   the top of the distribution is unchanged. This is the shape of A10/R29, reproduced from stipulated rules — which
   is exactly why it cannot count as evidence for it.
2. **De jure compliance is a register fact; de facto compliance is a classroom fact.** In #8 the statute with no
   enforcement moved registration +9.91 pp and attendance +1.09 pp. Any evaluation that measures the law by
   enrolment-on-the-books would report ~9× the behavioural effect that the toy actually produces. (PHL de jure vs de
   facto problem; C4-adjacent.)
3. **At equal budget, composition dominates the total.** In #9 rooms-only produced +40 physical places and zero
   usable ones; the split produced +29 usable places and +22 pp completion, and beat salaries-only by 10–15 pp.
   Where teachers are the binding constraint, retention matters; where rooms bind, it does not. Physically visible
   outputs (buildings, PTR) are the least reliable indicators of usable places.

---

## 6. Honest limits

- All parameters are stipulated; none is calibrated to any data. Changing the gates, fees or costs would change the
  pp magnitudes (not necessarily the directions, which are designed in).
- One cohort (#8, #9) or 30 cohorts (#7) with no equilibrium, no prices, no labour market, no quality choice, no
  dropout, no heterogeneity beyond the stated draws.
- "Completion" means "a seat that was used" in #7 and "attendance plus a pass draw" in #8/#9. This is a modelling
  convenience, not a claim about learning.
- Enforcement intensity `e` is declared, not measured; the toy cannot tell anyone what a real inspection regime is
  worth.
- A PASS here means the stipulated rules reproduce a pre-declared pattern. That is a statement about the model. A
  FAIL means they do not. Neither is a statement about the world, and neither reopens the closed phase.

**What would actually count as evidence** remains the single cell named in brief 014 §3.1: the observed provider-entry
supply-response test (entry elasticity first, sign flip second, or a recorded negative). These toys are design space
around that cell, not a substitute for it.

---

## 7. Reproducibility

```
cd extensions_archive/toys_2026-11-20/cluster_C/code
python3 selftest.py          # invariants: determinism, pairing, one-factor, budgets, stdlib-only
python3 run_cluster_c.py     # 200 seeds/cell -> ../RESULTS.csv + parameters.json + stdout verdicts
```

Two independent full runs produced byte-identical `RESULTS.csv`. File hashes (sha256, first 16 shown here; full
values in `RUN_MANIFEST.json`): `PRE_DECLARATIONS.md b0b0bdefa91d05ca`, `RESULTS.csv af889331b6668f5b`,
`cluster_c_model.py 2d81e767ab112318`, `run_cluster_c.py 6469897007831d4e`, `selftest.py d5e1aa14455af267`.

— Cluster C findings, 2026-11-20. ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.
