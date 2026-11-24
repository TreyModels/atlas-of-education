# PRE-REGISTRATION — phase sweep: fee abolition (E8) × formal-job bottleneck (E6) × exam gate

**Committed BEFORE any run of this workstream.** Date 2026-11-25. Branch
`research/phase-transition-2026-11-25`, base `4679ddb` (exit-reason driver fix), clean worktree at
commit time. **SIMULATION ONLY** on the `eduengine` toy worlds (`engine/eduengine/` + `engine/worlds.py`):
every parameter is illustrative, no country calibration, no empirical validation, **no causal
language**; "E8" / "E6" are labels for the modelled shocks, not evidence about any country.

## 0. Question and model vehicle

Operator/auditor question: *when a country abolishes primary fees (E8) while the formal job market is
still small (E6) and secondary access is rationed by a high-stakes exam gate, does the cohort bulge
inevitably tip liquidity-constrained stagnation into a regressive shadow-education / exam-gate arms
race?* Tested as a **phase transition** in a 2-D parameter plane, not as a narrative.

**Why `eduengine`** (and not the v6 `masseng-gate-jobs` prototype): `eduengine` already contains, in
one system, (i) household affordability with a cash-vs-need liquidity test and exit reason codes,
(ii) public/private/tutoring supply, (iii) bar and quota exam gates, (iv) `QueueLabour` with a formal
vacancy rate and credential floors, and (v) the fixed exit-reason decomposition
(`aggregate_exits`, `fix/edsystem-exit-reason-2026-11-25` @ `4679ddb`). The v6 `labour.py` /
`run_swaps.py` are being fixed concurrently by v6-runner; using them now would confound my results
with an in-flight code state. **Declared deviation:** the v6 prototype is not used here; all code
state is pinned to `4679ddb` and hashed in the run output.

## 1. Axes (both dimensionless)

**X = formal-vacancy bottleneck** = formal vacancies per cohort entrant (the engine's `vac0`, formal
vacancies/year ÷ one cohort of labour-market entrants). Realised normalisation is reported per cell:
`x_vac_per_gate_pass = annual formal vacancies ÷ children who passed the lower-secondary exam gate`
(cred ≥ 2) in the measured window, and `x_vac_per_lower_complete`. Design grid (10 values, severe →
slack, `vac0`): `0.02, 0.03, 0.045, 0.065, 0.09, 0.13, 0.18, 0.25, 0.35, 0.50`.

**Y = liquidity/fee slack (E8 shock)** = household primary-school fee per year, as a share of median
income (`fee_primary` on grades 1–6 only, added by a driver-side subclass; all other fees at the
`formal_loop` world defaults). Grid (10 values, post-abolition → pre-abolition):
`0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18`. `fee_primary = 0.00` is the **E8
abolition slice**; positive values are pre-abolition fee regimes. (Secondary forgone earnings,
tertiary fee and informal levies remain active in every cell — E8 removes the primary cash fee only,
by design of the question.)

**Gate regime (third factor, full sweep only):** the engine's two existing rules —
`bar` (fixed pass threshold at each transition; a tournament screen) and `quota` (planned seats as a
declared share of the cohort; seats scale with the cohort but not with a participation bulge, and the
admission cutoff is endogenous). Fixed at `bar` in the quick 10×10 mode; both in the full sweep.

## 2. Grids and cost (declared before running)

| mode | grid | seeds | runs |
|---|---|---|---|
| quick (for the warm box, `< ~2 min`) | X 10 × Y 10, gate = bar | 5 (0–4) | **500** |
| full local | X 10 × Y 10 × gate 2 | 5 (0–4) | **1,000** |

Fixed: `formal_loop` world, `N=400`, `T=70`, `measure_from=35`, private schools + tutoring market on
(needed for output b), fiscal loop, `queue_on=True` (declared: makes the credential queue explicit so
"queuing" can be observed), all other parameters at world defaults. Seeds are the only stochastic
input; each cell is the mean over seeds and its seed SD is recorded. CPU-local only; no GPU, no power
commands, nothing written outside the run output directory.

## 3. Three outputs, per cell (all seed-level; means and seed SD)

**(a) Exit partition from `e.exits`** via `aggregate_exits()` (survivors still in the state are
`censored` = −1; nothing may be read from `e.kids['reason']`, which is all −1 by design). Categories
partition the measured population (cohort ≥ `measure_from`) to 1.0: `liquidity` (reason 1),
`gate_fail` (2), `choice` (0), `never_enrolled` (4), `no_seat` (5), `not_admitted` (6),
`finished` (3), `censored` (−1). Report population shares, and `liquidity` / `gate_fail` for the
poorest quintile (q1) and the q5−q1 gap.

**(b) Shadow education:** `tut_rate` and `tut_by_q` → `tut_q5_q1_gap` (Q5−Q1 tutoring uptake).

**(c) Secondary-transition inequality:** `completion_lower`, `completion_upper`, the q5−q1 completion
gap at lower secondary, `parity_wealth_lower`, and the q1 gate-fit share. Plus diagnostic: `formal_rate`,
`queue`, `grad_unemp`, `x_vac_per_gate_pass`, `x_vac_per_lower_complete`.

Note: "exam-gate queuing" is measured as gate-fail exits and the credential queue; "regressive" =
the effect is larger for the bottom quintile (gap widens) — no counterfactual causal reading.

## 4. Predicted regime-boundary signature (competing hypotheses, fixed now)

- **H1 (operator's arms-race hypothesis):** under `bar`, as Y falls (E8 abolition) and X tightens,
  liquidity exits fall and there is a **sharp boundary** past which `tut_q5_q1_gap` and the q5−q1
  gate/transition inequality jump upward (positional competition replaces exclusion); under `quota`
  (cohort-scaled seats) the boundary is absent or much weaker.
- **H2 (engine-mechanism null):** tutoring demand tracks the marginal value of learning; with `bar`
  thresholds fixed, a participation bulge devalues credentials through beliefs and tutoring *falls*;
  no boundary under `bar`. A ratchet can only appear under `quota`, whose cutoff rises with takers.
- **H0:** no phase transition anywhere; gradients are smooth in both X and Y under both gate rules.

**Boundary statistics (defined before seeing data).** For each metric M and each gate regime:
1. `J_edge = |M_cell_a − M_cell_b| / σ_med` over all axis-adjacent cell pairs, where σ_med = median
   across cells of the seed-level SD of M; `J_max`, the edge attaining it, and
   `sharpness = J_max / median(J_edge)`.
2. Along every fixed-Y row (and fixed-X column), compare linear vs best one-break step fit in X:
   `ΔR² = R²_step − R²_linear`; report max `ΔR²` and the break location.
3. Gate contrast: `C = mean J_edge(bar) / mean J_edge(quota)` at the same metric.

**Decision rule for a phase transition (fixed).** SIGNATURE PRESENT iff for `tut_q5_q1_gap` **or**
the q1 gate/transition inequality: (i) `J_max(bar) ≥ 4`, (ii) `sharpness(bar) ≥ 2`, (iii) `C ≥ 2`,
and (iv) the direction is the regressive one (inequality higher on the tight-X / low-fee side of the
break). **PARTIAL** if any one clause fails; **ABSENT** if `J_max < 4` everywhere or `C < 2`.
The verdict quotes the numbers; a missing tipping point is reported as a result. This is an exhaustive
declared scan (no post-hoc selection of cells), and the whole grid is published, not just the maximum.

## 5. Auditor's quoted numbers — reproduction checks (declared before running, do not accept on trust)

- **A.** "Poor households exit mostly from liquidity (70.6%), not exam gates (0.8%)." Reproduce the
  **driver-fixed baseline cell** (multiverse combo 0: `cash_only`, `fixed_budget`, `public_only`,
  `bar`, `queue_floors`, `low_penalty`, seed 0, N=400, T=70) with `aggregate_exits` and report the q1
  `liquidity` and `gate_fail` shares. My value is the reproduction test; any difference (counts shift
  with in-process RNG order) is reported as-is.
- **B.** "Gates drive 42.4% of variance in `skill_premium`." Recompute one-way η² of the `gates` axis
  on `skill_premium` from the committed multiverse raw grid (`results_multiverse.json`, competitive
  arm; unaffected by the exit-reason bug), and verify code reproducibility by re-running 4 cells
  (2 combos × 2 seeds) at `4679ddb` and comparing `skill_premium`.
- **C.** "Learning drives 77.8% of `formal_rate`." Same: one-way η² of the `learning` axis on
  `formal_rate` from the committed grid (queue arm), plus a 4-cell reproducibility re-run.
- η² is defined as between-variant SS / total SS on seed-level run values (as in the committed
  RUN_REPORT §3.1). If a quoted value does not reproduce within the seed/rounding noise, say so with
  the value obtained; retractions stay retractions.

## 6. Honesty rules

SIMULATION label on every output; no causal or empirical claims; missing mechanisms declared (migration,
rural–urban sorting, remittances, country calibration, teacher labour supply outside the pay/monitoring
channel, informal/formal composition beyond queue vs competitive — all absent). Negative/failed
results preserved. Additive commits only on this branch; no push/force/reset. No power/shutdown/reboot
command on any machine, ever. Deviation log below, filled before any affected run.

**Deviation log:** (none at commit time)

---

### Deviation log (appended AFTER the pre-registration commit; every item is a declared deviation, none changes the pre-registered decision rule)

1. **Primary grid executed on the warm AutoDL box, not CPU-local.** Per the Lead's shutdown-checklist instruction
   (quick mode first), the 200-cell × 5-seed grid for both gates was run on `autodl-container-a8f742b5ee-292349c5`
   with the quick-mode runner copied by server-runner (script sha256 `69b984a3…`, engine root
   `/root/work/edsystem/engine`, 12 workers): bar 35.4 s / 500 runs, quota 42.0 s / 500 runs. The engine
   hashes on that box equal the committed eDSYSTEM server run (record `code_sha256`), i.e. the same
   `eduengine` code as this worktree. A local full-runner duplicate (1,000 runs) was launched 01:00–01:03
   and **killed** when the box grid made it redundant and the Mac reached load 53; no local full-run rows
   are reported. The pre-registered design is unchanged (same X/Y levels, 5 seeds, `formal_loop`, N=400,
   T=70, measure_from=35, queue_on=True).
2. **`bar_binding` exploratory arm, declared post-hoc.** After the pre-registered bar arm was seen to be
   **non-binding** (gate_fail ≤ 1.3 % of the measured population), an extra arm with binding bar thresholds
   (3.0 / 13.5 / 17.5 / 11.5) was calibrated on one probe run (gate_fail ≈ 9 %) and run on the same 10×10×5
   grid. It is reported **separately as an exploratory diagnostic** and is **not** part of the pre-registered
   decision rule (which remains bar vs quota).
3. **Decision-metric availability.** The box quick runner does not expose `gate_pass_q_gap` or
   `formal_hire_q_gap`; the pre-registered decision therefore uses the metrics it does expose —
   `tut_q5_q1_gap`, `completion_lower_q_gap`, `q1_gate_fail_share` — exactly as the rule allows
   ("tut gap OR the q1 gate/transition inequality").
4. **Quote check A** is run on the committed multiverse baseline combo 0 with the fixed exit read and a
   5-seed spread; "exam gates" = reason 2 (`gate_fail`).
