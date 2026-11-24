# RUN REPORT — phase-transition sweep: E8 fee abolition × E6 formal-job bottleneck × exam gate

**SIMULATION ONLY — `eduengine` toy worlds; every parameter is illustrative; no country calibration, no
causal or empirical claims, no identification. "E8" / "E6" are labels for the modelled shocks, not
evidence about any country.** Pre-registered before any run: `PREREGISTRATION_PHASE_SWEEP.md`
(commit `408aa3e`). Deviations logged at the end of that file (box execution, exploratory
`bar_binding` arm, decision-metric availability, quote-check A).

Code state: `eduengine` at `4679ddb` (exit-reason driver fix); engine hashes identical to the committed
eDSYSTEM server run (`core 2b7484a9…`, `labour bd3eaae6…`, `schools 9b079280…`, `tutoring 4bc58c3f…`,
`sdg4 5ce05c8b…`, `worlds 2e9ec71a…`). Quick runner sha256 `69b984a3…` (box); exploratory binding
variant `e9a8a9bd…` (local). Branch `research/phase-transition-2026-11-25`.

## REPRODUCTION_STATUS (QA gate; added after the Lead's 40-seed re-run)

- **B — "gates drive 42.4 % of variance in `skill_premium`": REPRODUCED ✓.**
  One-way η²(gates) on `skill_premium` = **42.42 %** (`0.424247`), competitive arm, n = 720 rows of the
  committed raw grid.
- **C — "learning drives 77.8 % of `formal_rate`": REPRODUCED ✓.**
  One-way η²(learning) on `formal_rate` = **77.83 %** (`0.778285`), queue arm, n = 720 rows.
- **A — "poor households exit mostly from liquidity (70.6 %), not exam gates (0.8 %)": PARTIAL, not exact.**
  q1 liquidity = **68.99 % (40-seed mean)** / **69.66 % (seed 0)** vs the quoted **70.6 %**. The 40-seed
  value was verified independently from the pulled fixed-40 decomposition
  (`pulled/engine-fixed-40seeds/decomp_fixed40.json`, combo 0, q1: `liquidity = 0.689866`). The quoted
  **0.8 % q1 gate_fail is folded into `other_terminal`** in the multiverse decomposition (the driver
  buckets reasons 2/3/5/6 together; 40-seed combo-0 q1 `other_terminal` = **1.08 %**), so it is **not
  directly comparable**; a direct reason-code read on the fixed driver gives **1.20 % (seed 0)** and
  **1.14 ± 0.18 % across 5 seeds**. The ordering "mostly liquidity, not exam gates" reproduces; the
  exact decimals do not.
- **Combo-0 exit partition reproduces bit-exactly**: censored 15.3 %, liquidity 35.7 %, choice 16.8 %,
  never 2.8 %, failed 6.2 %, finished 23.1 %, rationed 0.0 % — identical to the committed RUN_REPORT §3.8
  spot-check.
- **8/8 independent re-run cells are bit-exact** (max abs diff 0.0) between this Mac
  (py3.10.2 / np2.2.6) and the committed server run (py3.10.8 / np1.24.1).

## 1. What was run

| arm | grid | seeds | runs | host | wall | file sha256 |
|---|---|---|---|---|---|---|
| `bar` (pre-registered) | X 10 × Y 10 | 5 | 500 | warm AutoDL box, 12 workers, py3.10.8/np1.24.1 | **35.4 s** (first run; JSON later overwritten by a duplicate run, CSV identical) | csv `ce8d0162…` |
| `quota` (pre-registered) | X 10 × Y 10 | 5 | 500 | warm AutoDL box, 12 workers | **42.0 s** | csv `2d4ec3c6…` |
| `bar_binding` (exploratory, post-hoc) | X 10 × Y 10 | 5 | 500 | local Mac, 6 workers, py3.10.2/np2.2.6 | 387 s (load ≫ cores) | csv `dc05c9a3…` |

- **X** = formal vacancies per cohort entrant (`vac0`; 0.02 severe → 0.50 slack). Realised
  `x_vac_per_gate_pass` = annual formal vacancies ÷ children passing the lower-secondary gate: 0.041→0.843
  (`bar`), 0.047→1.178 (`quota`), 0.16→1.58 (`bar_binding`).
- **Y** = primary-school fee, share of median income, grades 1–6 only: 0.00 = **E8 abolition slice**,
  0.02…0.18 = pre-abolition fee regimes.
- Fixed: `formal_loop`, N=400, T=70, measure_from=35, private+tutoring on, fiscal loop, `queue_on=True`,
  seeds 0–4. Exits read **only** from `e.exits` via `aggregate_exits()`; censored-at-horizon is its own
  category; every cell's partition asserted to sum to 1.0. Nothing read from `e.kids['reason']`.

## 2. Three outputs (per cell, seed means; sample cells at the E8 slice, fee = 0.00)

Exit partition (measured cohorts, cohort ≥ 35): `liquidity` (reason 1), `gate_fail` (2), censored (−1),
`choice` (0), `never` (4), `no_seat` (5), `not_admitted` (6), `finished` (3). All rows sum to 1.000000.

| arm | vac0 | liq | gate_fail | censored | choice | never | finished | q1 liq | q1 gate_fail | tut_rate | Q5−Q1 tut gap | compl. lower | compl. lower q5−q1 gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bar | 0.02 | .045 | .013 | .289 | .449 | .008 | .195 | .160 | .013 | .272 | .354 | .637 | .929 |
| bar | 0.13 | .130 | .005 | .325 | .257 | .005 | .278 | .197 | .006 | .242 | .356 | .696 | .914 |
| bar | 0.50 | .324 | .001 | .340 | .051 | .004 | .280 | .570 | .002 | .221 | .331 | .771 | .844 |
| quota | 0.02 | .049 | .053 | .279 | .427 | .007 | .185 | .193 | .017 | .379 | .417 | .550 | .860 |
| quota | 0.13 | .148 | .074 | .290 | .286 | .004 | .199 | .264 | .007 | .474 | .517 | .550 | .729 |
| quota | 0.50 | .183 | .083 | .284 | .290 | .003 | .158 | .571 | .008 | .554 | .309 | .550 | .633 |
| bar_binding | 0.13 | .139 | .070 | .30 | .24 | .01 | .24 | .324 | — | .478 | .495 | .289 | .378 |

**E8 fee effect** (fee 0.00 vs 0.18 at vac0 = 0.13; the pre-registered liquidity axis):

| arm | q1 liquidity exit share | Q5−Q1 tutoring gap | lower-secondary completion | lower completion gap | gate_fail share |
|---|---|---|---|---|---|
| bar | **+16.2 pp** (.197 vs .035) | **+4.3 pp** (.356 vs .313) | +5.0 pp (.696 vs .647) | −4.9 pp (.914 vs .962) | +0.2 pp |
| quota | **+21.8 pp** (.264 vs .047) | **+4.1 pp** (.517 vs .476) | +0.1 pp (.550 vs .549) | −10.7 pp (.729 vs .836) | +1.1 pp |

Reading (SIMULATION): E8 in this model *raises* measured liquidity exits among the poorest because children
stay longer and are then hit by higher-level costs — the premise "E8 ⇒ falling liquidity exits" is reversed
in-model. Tutoring becomes slightly more regressive in both pre-registered arms; the wealth completion gap
*narrows*. None of this is a tipping point.

## 3. Boundary statistics and verdict

Pre-registered definitions (in `PREREGISTRATION_PHASE_SWEEP.md` §4): `J_edge = |ΔM| / median(seed SD)`;
`sharpness = J_max / median(J_edge)`; best one-break step vs linear fit (`ΔR²`); gate contrast
`C = median J(bar) / median J(quota)`; SIGNATURE iff `J_max(bar) ≥ 4`, `sharpness ≥ 2`, `C ≥ 2`, and
regressive direction. Exhaustive declared grid scan; all cells published in `PHASE_DIAGRAMS_all.md`.

| metric | arm | J_max | sharpness | best step ΔR² (break) |
|---|---|---|---|---|
| **Q5−Q1 tutoring gap** | **bar** | **2.58** | 3.45 | +0.09 (vac0 0.25) |
| | **quota** | **13.69** | **8.72** | **+0.39 (vac0 0.50)** |
| | bar_binding (exploratory) | 4.03 | 3.51 | +0.34 (vac0 0.13) |
| lower completion q5−q1 gap | bar | 3.59 | 5.29 | +0.02 |
| | quota | 3.54 | 3.10 | +0.01 |
| q1 gate-fail share | bar | 2.32 | 16.2 | — |
| | quota | 2.50 | 10.0 | — |
| formal_rate (capacity, not positional) | bar | 114.9 | 35.9 | +0.30 |
| | quota | 87.0 | 36.5 | +0.25 |

**Pre-registered verdict: SIGNATURE ABSENT under the `bar` rule.** `tut_q5_q1_gap` fails three of four
clauses (`J_max` 2.58 < 4, `C` 0.48 < 2, direction false; sharpness 3.45 passes). Lower-completion and q1
gate-fail inequalities fail `J_max` and `C` as well. Gate contrast is **reversed**: `C = 0.48`, i.e. the
sharp boundary is in the *quota* arm, not the bar arm.

**Where the boundary actually is:** under `quota` the Q5−Q1 tutoring gap traces an **inverted U** in X —
.417 at the most severe bottleneck (x_vac_per_gate_pass .047), **peak .517 at moderate tightness
(x ≈ .31)**, then a **sharp collapse to .309 at x ≈ 1.18** (`J_max` 13.7, 8.7× median; step break
vac0 0.35→0.50, R² .27→.66). The boundary is the point where **formal vacancies reach the gate-passing
cohort** (x ≈ 0.8–1.2): credential scarcity, and with it the shadow-education race, collapses. The
`bar` arm's corresponding surface is flat (.295–.359 across the whole plane).

**Why `bar` failed — the pre-registered bar arm is non-binding:** almost nobody fails the configured bar
thresholds (gate_fail **0.07–1.3 %** of the measured population; quota 3.6–8.4 %), so it is not a
tournament at all. The exploratory `bar_binding` arm (thresholds calibrated so gate-fail ≈ 9 %, one probe
run) *does* generate the race: Q5−Q1 gap .362–.525, `J_max` 4.03, step `ΔR²` .339 with break at
vac0 0.13. Post-hoc reading (declared exploratory, **not** in the decision rule): the arms race requires a
**binding** rationing gate; whether the rule is called "bar" or "quota" matters less than whether it
binds. `quota`'s endogenous cutoff produces the sharpest positional boundary.

### 3b. Reconciliation with the Lead's fee-axis / equifinality analysis (and the 20-seed bar check)

The Lead's `phase_boundary.py` (branch `research/box-runs-2026-11-25`,
`research/records/2026-11-25-box-runs/boundary-equifinality/`) reports **sharpness 0.01–0.29** and
concludes "no sharp regime boundary at this resolution". **The number is not the pre-registered
statistic:** it divides the raw fee-axis jump by the **median level of the response** (`|Δ| / median|M|`),
scans the **fee axis only**, and never divides by seed noise. The pre-registered statistic (§4) is
`J = |Δ| / median(seed SD)` over **both** axes and `sharpness = J_max / median(J_edge)`. Recomputing
both on the same CSVs (`reconcile_lead.py` → `results/lead_reconciliation.json`):

| source | `tut_q5_q1_gap`: pre-reg `J_max` | pre-reg sharpness | Lead-style (level-norm, fee axis) |
|---|---|---|---|
| bar, my 5 seeds | **2.58** (Y axis) | **3.45** | 0.040 |
| bar, Lead's 20 seeds (dense) | **2.02** (Y axis) | **2.66** | 0.031 |
| quota, 5 seeds | **13.69** (**X** axis, vac0 .35→.50) | **8.72** | 0.098 |

Consequences for the verdict:
- **The bar verdict (ABSENT) is confirmed by both seed counts** — my 5-seed and the Lead's 20-seed grid
  agree (J_max 2.58 vs 2.02, same Y axis); the failing clauses are `J_max < 4` and gate contrast
  `C = 0.48 < 2`, **not** sharpness (the pre-registered sharpness clause actually passes, 2.66–3.45 ≥ 2).
  The Lead's conclusion is right; the reason given (sharpness far below 2) is a normalisation error.
- **The Lead's scan misses the one candidate boundary** because it scans the fee axis only: the largest
  quota jump is on the **vacancy axis** (vac0 0.35 → 0.50, `x_vac_per_gate_pass` .83 → 1.18, Δ gap
  −.123). Under 5-seed σ this is `J = 13.7`, pre-reg sharpness 8.7, step ΔR² .392. **This is
  PROVISIONAL, not a verdict**: 5 seeds only, a single grid step, and a non-uniform X grid with a 43 %
  vacancy jump in that cell. It is logged as a candidate for the 20×20 lane, not claimed as a transition.
- The Lead's "gate contrast" (raw median |Δ| = .092) and the pre-registered `C = median J(bar)/median
  J(quota) = 0.48` are different statistics but agree in direction: the positional response is larger
  under quota.

**Equifinality (Lead's auditor thresholds: |Δ lower-secondary completion| < 0.5 pp and
|Δ tutoring uptake| > 20 pp or |Δ liquidity| > 25 pp).** My 5-seed CSVs reproduce the Lead's count
exactly: **0 pairs in bar, 20 pairs in quota** (within-gate). Top pairs (all quota):

| cell A (vac0, fee) | cell B (vac0, fee) | Δ completion (pp) | Δ tut_rate (pp) | Δ liq (pp) | Δ(tut Q5−Q1 gap) (pp) |
|---|---|---|---|---|---|
| (.02, .18) | (.50, .18) | 0.06 | **+21.5** | 11.0 | 8.8 |
| (.02, .18) | (.50, .16) | 0.14 | **+21.6** | 11.3 | 8.8 |
| (.02, .18) | (.50, .14) | 0.13 | **+21.0** | 11.6 | 8.0 |
| (.02, .18) | (.50, .12) | 0.14 | **+20.3** | 12.4 | 8.9 |
| (.02, .18) | (.50, .10) | 0.14 | **+20.5** | 12.5 | 6.9 |

**Construct caveat on the pairs:** under `quota`, lower-secondary completion is pinned by the seat share
(`share × N` = .55 of the population cohort), so it is near-constant *by rule* (completion_a .5486 vs
completion_b .5501–.5501). The same-completion condition is therefore partly an accounting identity of
the quota policy, not an emergent equifinality; the informative part is that tutoring uptake differs by
20–22 pp and liquidity exits by 11–13 pp **at the same completion level** — i.e. the participation bulge
is absorbed by competition, not by attainment. (The Lead's message calls this "Δtut gap"; in the code it
is `tut_rate`, the uptake rate. The Q5−Q1 gap difference for these pairs is 7–9 pp.)

**Dense-grid decision (superseded by the live run, see §3c).** The 10×10 quick grid is too coarse to test
the candidate boundary: the jump sits across a single step whose `vac0` changes by 43 %, and the X levels
are not uniform. A 20×20 × 20-seed grid is the right instrument. **I did not start a second grid.**
Coordination posted to the shared board (`domus_board_post`, to `deepseek`) with the things the 20×20
lane should preserve: (i) the bar arm is non-binding (gate_fail ≤ 1.3 %), so report it and add a
binding-bar variant; (ii) quota completion is pinned by the seat share, so equifinality there is partly
accounting; (iii) densify X near `x_vac_per_gate_pass` 0.5–1.6 and around the inverted-U peak (x ≈ 0.3),
and normalise J by seed SD.

### 3c. Dense 20×20 resolution test — Lead's live run (this record does NOT claim its verdict)

The Lead has pre-registered and launched the dense resolution test:
`research/phase-transition-dense-2026-11-25` @ **`8b0cc88`** (committed before launch) — 20×20
(X `vac0` geometric 0.02→0.50, 20 levels; Y `fee_primary` 0.00→0.19 step 0.01) × gates `bar`/`quota`
× 20 seeds = 16,000 runs. The **bar arm (8,000 runs) is running on the box under the Lead's claim**; the
**quota arm** is taken by `deepseek` after the Lead's release. This is a **resolution test, not a re-test
after seeing a positive**.

- **What it tests:** the quick-grid quota candidate on the vacancy axis — `vac0` .35→.50
  (`x_vac_per_gate_pass` .83→1.18), Δ gap −.123, **J = 13.69**, pre-registered sharpness **8.72**,
  step **ΔR² .392**, **PROVISIONAL on 5 seeds and one coarse grid step**. The dense grid resolves that
  interval into ~4 geometric steps (.30→.36→.42→.50), so it can confirm or dissolve the jump.
- **This record keeps the quick-grid verdict intact** — ABSENT (pre-registered bar signature) /
  PARTIAL (equifinality) / PROVISIONAL (quota vacancy-axis candidate) — and **does not claim any dense
  verdict**. When the Lead posts the dense statistics, they are to be reconciled here as a separate
  section, with the quota candidate preserved as provisional whatever the dense result.
- **Flagged analysis-definition risk (raised to the Lead):** the dense pre-registration's statistics
  section describes the *Lead's* fee-axis, level-normalised sharpness (`|Δ| / median level`,
  threshold ≥ 2), whereas `408aa3e` defines `J = |Δ| / median(seed SD)` over **both** axes with
  `sharpness = J_max / median(J_edge)`. Under the level-normalised fee-axis definition the ≥ 2 threshold
  is effectively unreachable (0.01–0.29 observed on both quick grids), and the candidate boundary is on
  the **X** axis that definition does not scan. The dense results must therefore be analysed with the
  `408aa3e` statistic (applied symmetrically to quick and dense); any post-hoc analysis change must be
  declared as a deviation before the dense numbers are read.

## 4. Auditor's three quoted numbers — checked against the code actually run

Method: `check_quotes.py` (committed) re-runs the committed multiverse baseline with the fixed exit read
and recomputes one-way η² from the committed raw grid (`results_multiverse.json`), plus 8 independent
re-run cells. 8/8 re-run cells are **bit-identical** to the committed values (max abs diff 0.0), so the
η² checks are not sensitive to the later driver fix.

| quote | my value | verdict |
|---|---|---|
| "poor households exit mostly from liquidity (70.6 %), not exam gates (0.8 %)" | baseline combo 0 (cash_only/fixed_budget/public_only/bar/queue/low_penalty), seed 0: q1 **liquidity 69.66 %**, q1 **gate_fail 1.20 %**; 40-seed q1 liquidity **68.99 %** (verified from `decomp_fixed40.json`); across seeds 0–4: **69.58 ± 0.76 %** and **1.14 ± 0.18 %** | **PARTIAL — see `REPRODUCTION_STATUS` above.** The ordering reproduces; 70.6 % vs 68.99 % (40-seed mean) / 69.66 % (seed 0). The quoted 0.8 % q1 gate_fail sits inside `other_terminal` (1.08 % at 40 seeds) in the multiverse decomposition, so it is not directly comparable. The record's own overall combo-0 partition reproduces **exactly**: censored 15.3 %, liquidity 35.7 %, choice 16.8 %, never 2.8 %, failed 6.2 %, finished 23.1 %, rationed 0.0 % |
| "gates drive 42.4 % of variance in `skill_premium`" | one-way η²(gates) on `skill_premium`, competitive arm, n=720: **0.42425** | **reproduces** (42.4 %) |
| "learning drives 77.8 % of `formal_rate`" | one-way η²(learning) on `formal_rate`, queue arm, n=720: **0.77829** | **reproduces** (77.8 %) |

Full η² tables (all axes) are in `results/quote_checks.json`; for `skill_premium` the ranked movers are
gates .424, affordability .403, rural .103, learning .021, supply .001, jobs < .001; for `formal_rate`,
learning .778, gates .031, rural .028, supply .001, affordability < .001, jobs < .001.

## 5. Answer to the question, stated as a simulation result (no causal reading)

- **Verdict: the pre-registered bar-gate signature is ABSENT; a quota-arm candidate boundary is
  PARTIAL/PROVISIONAL; the equifinality result is a positive descriptive finding.** In this model,
  abolishing the primary fee does not tip a liquidity-constrained system into a sharp bar-gate
  shadow-education race. The pre-registered bar rule produces **no boundary** (J_max 2.02–2.58 < 4,
  gate contrast 0.48 < 2, direction wrong; 5- and 20-seed grids agree). The only sharp jump under the
  pre-registered statistic sits in the **rationed quota** arm, on the **vacancy axis**
  (vac0 .35→.50, x_vac_per_gate_pass .83→1.18, Δ gap −.123, J 13.7), and is **provisional** (5 seeds,
  one grid step, coarse non-uniform X; the 20×20 lane tests it).
- **A boundary does exist, but it is an arms-race *collapse* at the slack end** (quota arm): when formal
  vacancies approach/exceed the gate-passing cohort (x_vac_per_gate_pass ≳ 0.8–1.2), the wealth-stratified
  tutoring gap falls sharply (.517 → .309; J = 13.7). Shadow-education pressure is **maximal at moderate
  bottleneck tightness**, not at the most severe: extreme stagnation suppresses the race by excluding
  children before the gate (choice exits 45 % at vac0 = 0.02 vs 5 % at 0.50).
- **E8 moves inequality in the predicted direction only weakly and smoothly** (+4 pp tutoring gap),
  raises poorer-household liquidity exits by +16–22 pp (duration/level-cost mechanism), and *narrows* the
  wealth completion gap. No inevitability, no tipping in the fee channel.
- **Top construct caveat:** the operator's "seats scale with the cohort" regime is **not implemented** by
  this engine. `quota` seats are a declared share of the *population cohort*, not of *takers*, so an E8
  participation bulge tightens the cutoff — that is why the quota arm shows the race. A gate whose seats
  expand with the participating cohort was not testable here and is the first missing mechanism.

## 6. Top risks / what is not identifiable

1. Toy model, illustrative parameters, no calibration; every level is a modelling assumption.
2. The pre-registered `bar` arm is non-binding, so it tests "open screen + affordability", not a
   high-stakes tournament; the binding-bar arm is post-hoc and single-bar calibration.
3. `quota` ≠ the operator's "seats scale with cohort" (see §5); no rule where seats expand with takers.
4. X is `vac0` (vacancies per entrant); the requested vacancies/gate-eligible ratio is reported as a
   realised per-cell normalisation, not imposed.
5. Missing mechanisms (declared, not invented): migration, rural–urban sorting, remittances, country
   calibration, general-equilibrium wage feedback, teacher labour supply outside pay/monitoring,
   informal/formal composition beyond queue vs competitive. Quintiles are income proxies; the engine's
   exit codes are mechanism labels, not observed data. Horizon truncation (T=70) puts many young cohorts
   in `censored`; 5 seeds only.

## 7. Files and reproduction

```
research/records/2026-11-25-phase-transition/
  PREREGISTRATION_PHASE_SWEEP.md      # commit 408aa3e, before any run (+ deviation log)
  phase_sweep_quick.py                # box runner (sha256 69b984a3…); bar_binding variant e9a8a9bd…
  run_phase_sweep.py                  # local full runner (superseded; see deviation log)
  analyze_phase_sweep.py              # boundary statistics + phase diagrams
  check_quotes.py                     # the three quote reproduction checks
  results/box_quick/                  # box bar + quota CSVs/JSONs, binding CSVs, MANIFEST.sha256
  results/boundary_stats_all.json     # J / sharpeness / step fits / decision clauses, 3 arms
  results/PHASE_DIAGRAMS_all.md       # ASCII phase maps + E8 and fee slices, 3 arms
  results/quote_checks.json           # A (seed spread), B, C, 8/8 bit-exact re-runs
  results/lead_reconciliation.json    # pre-registered J vs Lead's level-normalised fee-axis number; equifinal pairs
  reconcile_lead.py                   # reproduces the Lead's 0-bar / 20-quota equifinal count and reconciles sharpness
```
Reproduce box arms: `/root/miniconda3/bin/python phase_sweep_quick.py --engine-root <engine> --out <dir>
--workers 12 [--gate quota|bar_binding]`. Analyse: `python analyze_phase_sweep.py --source box --box-dir
results/box_quick --out-tag all`. Quote checks: `python check_quotes.py <engine_root>`.
