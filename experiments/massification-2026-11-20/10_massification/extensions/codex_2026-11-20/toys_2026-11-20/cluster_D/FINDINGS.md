# FINDINGS — Cluster D toys (#10, #11, #12)

**ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no historical test; phase closed; do not cite numbers as estimates.**

These are three seeded toy simulations built from the archived `takeoff.py` / `model.py` engine, to the
Council specification in `extensions_archive/codex_2026-11-20/COUNCIL_TOY_SPECS_015.md` §Cluster D. They test
**properties of stipulated rules**, not the world. Nothing here reopens the closed massification phase,
nothing here is a re-analysis of any data, and no phase/closed-anchor file was read or written. The
predeclared thresholds, estimands, falsifiers and decision rules are in `PRE_DECLARATIONS.md` (including the
§6 pre-run amendment record); `RESULTS.csv` holds every cell, every paired gap and every per-seed audit value.

Run: 240 fixed seeds per cell (`seed = 20261120 + 1 … + 240`), paired counterfactuals with identical latent
draws per `(seed, cohort, slot)`, matched starting conditions, one-factor treatments, Python 3.10 stdlib only.
Full parameter vector in `RUN_MANIFEST.json`; reproduction command at the end.

**Verdicts.** #10 roll-out order — **PARTIAL** (order moves crossing years and preserves floor→ceiling order,
but simultaneous expansion does **not** compress the floor→ceiling spacing). #11 cohort shock × capacity —
**SUPPORTED** (large, exact interaction). #12 temporary expansion — **PARTIAL** (expectation trace confirmed;
the hire gain is below the predeclared bar and decays too slowly).

---

## 1. Experiment #10 — level-first roll-out and crossing order

**Treatment (one factor):** PV-equal seat expansion, 40 discount-0.97 seat-years per level, injected into one
level at a time or into all three at once. Everything else (latent draws, gate rules, endogenous
backlog-rationed construction) identical. `control` = no injection.

### 1.1 Every cell (median of 240 paired seeds; crossing year 31 = never within 30 cohorts)

| arm | `X_M0` primary 50 % | `X_M1` primary 90 % | `X_M2` lower-sec 50 % | `X_M3` upper-sec 50 % | `U90` upper 90 % | spacing `S = X_M3 − X_M0` | primary share at horizon | lower-sec share | upper-sec share | upper-sec completions, 30 cohorts |
|---|---|---|---|---|---|---|---|---|---|---|
| `control` | 10 | 31 | 27 | 31 | 31 | 21 | 0.85 | 0.56 | 0.04 | 22 |
| `primary_first` | **4** | **16** | 12 | **17** | 31 | 13 | 0.94 | 0.87 | 0.76 | **1428.5** |
| `lower_first` | 7 | 10 | 13 | 18 | 31 | 11 | 0.94 | 0.87 | 0.76 | 1340 |
| `upper_first` | 10 | 13 | 15 | 21 | 31 | 11 | 0.94 | 0.87 | 0.76 | 1077 |
| `simultaneous` | 6 | 13 | 14 | 19 | 31 | 13 | 0.94 | 0.87 | 0.76 | 1278 |

Paired gaps vs `control` (median; share of seeds in parentheses): `primary_first` `X_M0 −6` (240/240),
`X_M3 −14` (240/240, control's ceiling is censored), `S −8` (240/240), upper-secondary completions
`+1407` (240/240). `upper_first` `X_M0 0` (the primary level receives nothing until cohort 11, so its floor
crossing is identical to control in 240/240 seeds) and `X_M3 −10`.

### 1.2 Thresholds

| id | rule | observed | met |
|---|---|---|---|
| P10-1 | order `X_M0 ≤ X_M2 ≤ X_M3` in ≥ 90 % of seeds in each sequential arm | 1.000 in all three | **yes** |
| P10-2a | `S(primary_first) ≥ 2` yr | 13 | yes |
| P10-2b | `S(simultaneous) ≤ 1` yr (compression) | **13** | **no** |
| P10-2c | paired `S(primary_first) − S(simultaneous) ≥ 2` yr | **0.0** | **no** |
| P10-3 | `median abs(X_M3(arm) − X_M3(simultaneous)) ≥ 1` yr for some sequential arm | 2.0 (primary_first), 1.0 (lower_first), 2.0 (upper_first) | **yes** |
| INTERVAL (secondary) | `S(primary_first) ∈ [2, 12]` yr | **13** | **miss** |

**Verdict: PARTIAL.** P10-1 and P10-3 hold; P10-2 fails outright.

### 1.3 Reading

1. **Order is preserved, always.** Every arm crosses the floor take-off before the middle and the middle
   before the ceiling take-off, in 240/240 seeds, including `upper_first`. This is a structural consequence:
   a level's completions cannot precede the level below it because each gate requires the previous credential.
   P10-1 therefore confirms a *design property of the toy*, not a finding about schooling systems.
2. **Order moves crossing years.** Floor take-off `X_M0` runs 4 (primary-first) to 10 (upper-first);
   ceiling take-off `X_M3` runs 17 to 21. `primary_first` reaches 90 % primary completion by cohort 16;
   `upper_first` not until 13 and `simultaneous` also 13, while `control` never does. The declared one-year
   band (P10-3) is exceeded by 2 years even on the uncensored-only diagnostic
   (`median_abs_gap_X_M3_uncensored_*` = 2.0 / 1.0 / 2.0).
3. **Simultaneity does not compress floor→ceiling spacing — the pipeline does.** `S` is 11–13 years under
   *every* arm, and the paired `S(primary_first) − S(simultaneous)` difference is 0.0 years. The predeclared
   "simultaneous compresses them" clause is falsified. In this toy the floor→ceiling spacing is set by the
   credential gate sequence (each level needs the previous completion), not by the timing of capacity
   injection; simultaneous expansion just shifts the whole sequence earlier.
4. **Top capacity without feeders is wasted.** `upper_first` gives the top level the first five cohorts of
   PV-equal seats and yet has the *latest* ceiling take-off (21) and the *lowest* cumulative upper-secondary
   output (1077, i.e. 25 % below `primary_first` at identical present value). Seats at a level with no eligible
   cohort do nothing.
5. **A10 mirror (descriptive, not a test).** With equal PV to all three levels, the floor reaches 94 %
   completion while the ceiling reaches 76 %, and the 90 % ceiling is never reached in any arm or any seed
   (`censored_U90 = 1.00`). Capacity alone does not universalize the top level — the same asymmetry as A10,
   reproduced as a property of these stipulated gates. It is **not** evidence about A10.

### 1.4 Predeclared falsifier

"Roll-out order has no effect on crossing order" — not observed: order is always floor-first, but crossing
*years* and cumulative output do move with the schedule. The falsifier is not met. The *spacing* clause of the
threshold, however, is met in the opposite direction: order does not compress spacing at all.

---

## 2. Experiment #11 — cohort-size shock × capacity rule

**Treatment (one factor, two levels each):** permanent cohort size `n ∈ {96, 120, 144}` (±20 %) × capacity
rule `frozen` (absolute seats, `cap = seat_f`) vs `responsive` (per-child seats, `cap = seat_f·n/120`).
Investment is a fixed 3 nominal seats/cohort in every arm and the employer is per-child invariant in every
arm, so the capacity rule is the only difference (see `PRE_DECLARATIONS.md` §6.3).

### 2.1 Every cell (median of 240 seeds)

| arm | `X_M0` (p10/50/p90) | `X_M1` | primary completion per child at horizon | lower-sec share | primary seats at horizon | primary applications at horizon |
|---|---|---|---|---|---|---|
| `neutral_frozen` | 15 / 15 / 15 | 31 | 0.772 | 0.053 | 92.6 | 107.6 |
| `up_frozen` | 19 / 19 / 19 | 31 | **0.688** | 0.000 | 99.0 | 129.0 |
| `down_frozen` | 11 / 11 / 11 | 31 | 0.819 | 0.212 | 78.6 | 86.4 |
| `neutral_responsive` | 15 / 15 / 15 | 31 | 0.772 | 0.053 | 92.6 | 107.6 |
| `up_responsive` | 15 / 15 / 15 | 31 | 0.771 | 0.049 | 111.0 | 129.1 |
| `down_responsive` | 15 / 15 / 15 | 31 | 0.771 | 0.047 | 74.0 | 86.0 |

Paired gaps vs the neutral arm of the same capacity rule (median; share of seeds in parentheses):
`up_frozen` `X_M0 +4` (240/240), completion per child `−0.087` (0/240 positive); `down_frozen` `−4` (240/240),
`+0.047` (240/240); `up_responsive` `X_M0 0` (0/240), `−0.002`; `down_responsive` `0`, `−0.002`.

### 2.2 Thresholds

| id | rule | observed | met |
|---|---|---|---|
| P11-1a | `up − neutral` on `X_M0` ≥ +1 yr under frozen | **+4.0** | **yes** |
| P11-1b | `abs` of the same gap ≤ 0.5 yr under responsive | **0.0** | **yes** |
| P11-2 | paired DiD ≥ 0.75 yr | **+4.0** (240/240 positive) | **yes** |
| P11-3a | `up − neutral` primary share ≤ −0.05 under frozen | **−0.0868** | **yes** |
| P11-3b | same gap ≥ −0.02 under responsive | **−0.0021** | **yes** |
| SIDE | `down_frozen` advances crossings (≤ 0) | −4.0 | yes |

**Verdict: SUPPORTED.** The interaction is the entire phenomenon: a 20 % larger cohort delays floor take-off
by four cohorts and costs 8.7 pp of completion per child when capacity is absolute, and changes nothing
(0 cohorts, 0.2 pp) when capacity tracks cohort size.

### 2.3 Reading, caveats and what it does not show

1. The shock is **not** a shock by itself. Under per-child capacity the median crossing year is *identical*
   (15) at 96, 120 and 144 students, because the seat stock per child is identical by construction. All of the
   effect in the frozen arms is the denominator moving against a fixed stock.
2. `M1` (90 % primary) is **censored in every cell** (3 seats/cohort never reaches 90 % within 30 cohorts), so
   this toy says nothing about universalization timing — only about the 50 % take-off and the final level of
   completion.
3. Crossing years are near-degenerate across seeds (p10 = p50 = p90 in every cell) because the capacity path
   is deterministic; the 240/240 sign consistency is a structural implication of the rules, not a statistical
   regularity. Read the "240/240" as "the arithmetic forces this", not as a p-value.
4. The fixed 3-seat investment is rationed to the largest backlog, so the *down* arm shifts some investment to
   lower-secondary once primary demand is satisfied (`lower-sec share 0.212` vs 0.053). That is a second,
   unintended channel present only in the small-cohort arm; it does not affect the up-shock thresholds, which
   is where the verdict rests. (The pre-run amendment §6.3(i) overstated this: total seats built are identical
   across sizes, but the *level* allocation is not.)
5. The employer is per-child invariant in both arms, so this is a statement about **school capacity only**;
   job capacity is deliberately not the varying factor here.

---

## 3. Experiment #12 — temporary expansion with expectations

**Treatment.** 12 leased upper-secondary seats in cohorts 2–4 only (upper-secondary places 12 → 24 → 12),
crossed with an information regime and with employer responsiveness. Starting state is a stipulated
mid-transition system (108/100/12 places per 120 children) with the construction rule off, so the lease is the
only capacity variation. Paired controls share every latent draw and every starting condition (verified:
`PRE` window values are identical in all eight arms — 86.0 upper-secondary applications, 12 completions,
40/35 hires).

### 3.1 Every cell (median of 240 seeds)

Upper-secondary applications per cohort:

| arm | PRE (cohort 1) | DURING (2–4) | POST (5–7) | DECAY (16–20) |
|---|---|---|---|---|
| `control_frozen` | 86.0 | 75.0 | 73.7 | 73.6 |
| `supply_only_frozen` | 86.0 | 75.0 | 73.7 | 73.6 |
| `fee_waiver_frozen` | 86.0 | **97.7** | 73.7 | 73.6 |
| `placement_info_frozen` | 86.0 | 83.0 | **86.3** | 74.0 |
| `control_responsive` | 86.0 | 71.7 | 78.0 | 83.6 |
| `supply_only_responsive` | 86.0 | 72.7 | 79.7 | 83.6 |
| `fee_waiver_responsive` | 86.0 | **97.3** | 79.7 | 83.6 |
| `placement_info_responsive` | 86.0 | 80.7 | **87.3** | 83.8 |

Upper-secondary completions, formal hires and composition:

| arm | completions DURING / POST | total hires DURING / POST / DECAY | graduate hires DURING / POST | poor share of upper completions DURING / POST |
|---|---|---|---|---|
| `control_frozen` | 12 / 12 | 40 / 40 / 40 | 12 / 12 | 0.069 / 0.056 |
| `supply_only_frozen` | **24 / 12** | 40 / 40 / 40 | **24 / 12** | 0.083 / 0.056 |
| `fee_waiver_frozen` | **24 / 12** | 40 / 40 / 40 | **24 / 12** | **0.222** / 0.056 |
| `placement_info_frozen` | **24 / 12** | 40 / 40 / 40 | **24 / 12** | 0.097 / 0.111 |
| `control_responsive` | 12 / 12 | 40 / 45 / 50 | 12 / 12 | 0.056 / 0.083 |
| `supply_only_responsive` | **24 / 12** | **41.7 / 46 / 50** | **24 / 12** | 0.069 / 0.083 |
| `fee_waiver_responsive` | **24 / 12** | 41.7 / 46 / 50 | **24 / 12** | **0.222** / 0.083 |
| `placement_info_responsive` | **24 / 12** | 41.7 / 46 / 50 | **24 / 12** | 0.097 / 0.139 |

Paired median gaps (arm − own control) for the two arms that carry the expectation question:

| gap | `placement_info_frozen` | `placement_info_responsive` | `supply_only_responsive` |
|---|---|---|---|
| DURING upper-secondary applications | +8.0 (+10.6 %) | +9.0 (+12.4 %) | +1.0 (+1.4 %) |
| POST upper-secondary applications | **+12.7 (+17.1 %)** | **+9.3 (+11.9 %)** | +1.3 (+1.8 %) |
| DECAY upper-secondary applications | +0.4 (+0.5 %) | +0.2 (+0.2 %) | 0.0 (0.0 %) |
| DURING total hires | 0.0 | **+1.67** | **+1.67** |
| POST total hires | 0.0 | **+1.0** | **+1.0** |
| DECAY total hires | 0.0 | 0.0 | 0.0 |
| DURING poor share of upper completions | +0.028 | +0.041 | +0.006 |
| fee waiver: DURING applications | — | — | +22.7 / +25.3 (frozen / responsive, +30 %/+36 %) |

### 3.2 Thresholds

| id | rule | observed | met |
|---|---|---|---|
| P12-1a | info × frozen: POST upper-secondary applications ≥ +5 % | **+17.1 %** | **yes** |
| P12-1b | info × frozen: `abs(POST hires gap) ≤ 1.0` | **0.0** | yes (definitional, see below) |
| P12-2a | `supply_only_responsive`: DURING hires gap ≥ +2.0 persons | **+1.67** | **no** |
| P12-2b | POST hires gap ≤ 50 % of the DURING gap | **+1.0 = 60 %** | **no** |
| P12-3 | some arm: POST applications ≥ +2 % and DECAY ≤ 50 % of POST | info-frozen 17.1 % → 0.5 %; info-responsive 11.9 % → 0.2 % | **yes** |

**Verdict: PARTIAL.** The expectation mechanism (P12-1, P12-3) works; the hire-magnitude/decay rule (P12-2)
fails on both its parts.

### 3.3 Reading, including the misses

1. **A temporary expansion leaves a trace, but only through beliefs.** `supply_only` doubles upper-secondary
   completions during the lease (12 → 24) and they snap back to 12 the moment the seats are removed, with
   applications unchanged in every window (0.0 gap). The information arm is what carries the shock forward:
   +17.1 % upper-secondary applications in cohorts 5–7 — i.e. one to three cohorts *after* the seats are gone
   — decaying to +0.5 % by cohorts 16–20. P12-3 is met with a wide margin.
2. **The decay rate is a stipulated parameter.** The 0.70 belief memory is imposed; the toy shows that an
   adaptive expectation with memory is *sufficient* to produce a persistent-then-decaying application gap. It
   is not evidence that any such gap exists, and the half-life (≈2 cohorts) is an assumption, not a result.
3. **The hire gain misses both predeclared parts.** Under responsive employers the lease raises hires by
   +1.67 persons during the lease (4.2 %) — below the predeclared ≥ 2.0 bar — and the gap is still +1.0
   (≈60 % of the during-lease gap) in cohorts 5–7, so the "≤ 50 % by POST" decay rule also fails. The reason
   is structural: the hire response runs through `skill_stock`, which has a 0.8-per-cohort memory, so the trace
   decays with a time constant of ~4–5 cohorts and only reaches 0 by cohorts 16–20. The predeclared 3-cohort
   halving was too fast for this engine. Reported as a miss; not re-specified after the fact.
4. **"Hires flat under fixed jobs" is definitional, not a result.** With frozen posts the employer fills all 40
   posts in every cohort, so the total-hire gap is exactly 0 by construction (P12-1b is trivially true). The
   informative measure under frozen posts is composition: graduate hires do double during the lease
   (12 → 24) while total hires do not move — graduates displace non-graduates in the same 40 posts.
5. **A price instrument is not an expectation instrument.** The fee waiver raises during-lease applications by
   30–36 % and the poor share of upper-secondary completions from 0.069 to 0.222, and leaves *nothing* after
   the lease (POST gap 0.0). In this toy, access composition responds to price; persistence requires beliefs.
6. **Applications never respond to seats directly.** By stipulation, applications in this engine respond only
   to observed credential flows (`readers`, `formal_share`, belief). "Supply-only" therefore cannot raise
   applications at all — a limitation of the toy that bounds what it can say about the real
   applications/expansion nexus, and the reason the information arm is doing all the work.

---

## 4. Cross-cutting statements

### 4.1 What these toys can and cannot do

- **Can:** show that a stipulated mechanism *could* produce a pattern; separate timing from spacing; show that
  a demographic shock is only a shock when capacity fails to scale; show that a temporary expansion can leave
  an expectation trace while leaving no hire trace.
- **Cannot:** test any historical claim, calibrate any parameter, or speak to R13, R27/C1, A10/R29 or the
  14.97 pp ceiling residual. The A10-shaped outcomes above (floor before ceiling; ceiling never universalized)
  are properties of the stipulated gate rules and were designed in, not discovered.
- **Must not be cited** as estimates. No number here is a measurement of anything.

### 4.2 Where the results depend on stipulations (not on data)

| result | depends on |
|---|---|
| crossing order always floor-first | one-gate-per-cohort sequencing in the engine |
| spacing `S` ≈ 11–13 years, not compressed by simultaneity | the same sequencing plus the 3-level structure |
| cohort shock × capacity interaction | absolute vs per-child delivery of the seat stock; fixed 3 seats/cohort |
| temporary-expansion persistence | adaptive belief memory 0.70 and reference flow 12/cohort |
| hire trace size (+1.7 persons) | responsive posts `= n·(0.10 + 0.52·skill_stock)`, skill memory 0.8 |
| fee waiver effect on composition | the `cash ≥ fee` gate and the 3-group endowment |

### 4.3 Reporting integrity

- **All cells are reported**, including the three threshold failures (P10-2b, P10-2c, P12-2a/b) and the
  missed interval prediction, plus censored milestones (`M1` and `U90` in most cells).
- **Post-run code defect, corrected and re-run.** In the first full run, P10-3 compared each sequential arm
  with the no-injection `control` instead of with `simultaneous`, as declared; the census of P10-3 therefore
  read 14 years (a censoring artefact) instead of 2. The comparator was fixed and the **entire battery was
  re-run from scratch**; `RESULTS.csv` and `RUN_MANIFEST.json` are from the re-run. Thresholds were not
  touched. The corrected P10-3 (2.0 / 1.0 / 2.0 years) still meets the ≥ 1-year band, so the #10 verdict is
  unchanged (PARTIAL, on P10-2).
- **Pre-run design amendment** (§6 of `PRE_DECLARATIONS.md`) is recorded in full, with reasons: the #11
  capacity rule and the #12 starting state / information regime were redefined after 1–5-seed debug executions
  showed the first sketches to be either non-identical across arms or vacuous (an upper-secondary lease in
  cohorts 2–4 does nothing if no upper-secondary cohort can exist yet). No numeric threshold was changed.
- No git commit, no iCloud writes, no phase/closed-anchor file touched. All writes are under
  `extensions_archive/toys_2026-11-20/cluster_D/`.

---

## 5. Reproduce

```
cd extensions_archive/toys_2026-11-20/cluster_D/code
python3 run_all.py 240      # ~40 s, stdlib only; rewrites ../RESULTS.csv and ../RUN_MANIFEST.json
```

Files: `PRE_DECLARATIONS.md`, `RESULTS.csv` (36 922 rows: cell aggregates, paired gaps, per-seed audit,
threshold outcomes), `RUN_MANIFEST.json` (parameter vector, seeds, verdicts, SHA-256 of every file),
`code/toy_engine.py`, `code/exp10_level_first.py`, `code/exp11_cohort_shock.py`,
`code/exp12_temporary.py`, `code/run_all.py`.

— Cluster D, 2026-11-20. ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no historical test; phase closed; do not cite numbers as estimates.
