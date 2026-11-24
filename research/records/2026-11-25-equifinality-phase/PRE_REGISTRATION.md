# PRE-REGISTRATION — equifinality & phase sweep: 20×20 X/Y grid × {bar, quota} gates × 20 seeds

**SIMULATION ONLY — `eduengine` toy worlds; illustrative parameters; no country calibration, no empirical
validation, no causal claims.** Every output of this workstream carries this label.

Committed **BEFORE any run** of this workstream (no simulation run, not even a smoke test, had been executed
at commit time; only static reads of the engine source and of the base branch's committed outputs). Date
2026-11-25. Branch `research/equifinality-phase-2026-11-25`, worktree `wt3/phase`, base
`origin/research/phase-transition-2026-11-25` @ `2e58d64` (which already contains
`research/records/2026-11-25-phase-transition/{PREREGISTRATION_PHASE_SWEEP.md,phase_sweep_quick.py}`).

This document **extends** the base pre-registration; it does not replace it. Where this document is silent,
the base pre-registration's definitions apply. Additive commits only; nothing is rewritten or force-pushed.

---

## 0. Question

**Equifinality question (primary deliverable).** In the simulated parameter plane, do *distinct* parameter
cells — different formal-vacancy bottlenecks and different primary-fee regimes — arrive at **almost the same
simulated participation** (GER-like measure) while differing **hugely in the distribution of who is excluded
and in shadow-education uptake**? Formally: pairs of cells that are near-identical in simulated participation
but far apart in liquidity-exclusion share or tutoring rate. This is the simulation analogue of "same
enrolment headline, very different schooling regime", and it is a *descriptive property of the toy model's
output surface*, not an empirical claim.

**Secondary question (descriptive only).** How do the same cells differ in `completion_lower` (lower-secondary
completion) — reported as a secondary outcome.

**Explicitly NOT claimed here.** No causal effect of fees, vacancies or examination gates on any real
country; no calibration; no predictive statement. `eduengine` is a toy world (see base pre-registration §0).

---

## 1. Model vehicle and fixed parameters (fixed before running)

`formal_loop` world from the engine's `worlds.py`, with the driver-side `PrimaryFeeSchools` subclass
(adds `fee_primary` on grades 1–6 only, `PublicSchools` otherwise unchanged; as in `phase_sweep_quick.py`),
plus the base module set `[PrimaryFeeSchools, PrivateSchools, TutoringMarket, FiscalState, QueueLabour, SDG4]`
ordered by `ee.ORDER`.

Fixed in **every** cell: `N = 400` children per cohort, `T = 70` years, `measure_from = 35` (cohorts ≥ 35 are
scored), `queue_on = True`, `vac_growth = 0.0`, all other parameters at the `formal_loop` world defaults.

Measured population for every share = **all children ever in the state whose cohort ≥ `measure_from`**
(exited children from `e.exits` *plus* survivors still in the state, read via `aggregate_exits()`; survivors
are the `censored` category). `e.kids['reason']` is never read (it is all −1 after `run()` by design).

Exit partition (must sum to 1.0 per cell within 1e-6, checked and enforced):
`liquidity` (1), `gate_fail` (2), `finished` (3), `never_enrolled` (4), `no_seat` (5), `not_admitted` (6),
`choice` (0), `censored` (−1).

---

## 2. Axes — exact pre-registered levels

**X = formal vacancies per cohort entrant** = the engine's `vac0`. 20 levels, geometric from 0.01 to 0.80,
rounded to 4 significant digits, hard-coded identically in the runner:

```
0.0100, 0.01259, 0.01586, 0.01998, 0.02516, 0.03168, 0.03990, 0.05025, 0.06329, 0.07970,
0.1004, 0.1264,  0.1592,  0.2005,  0.2525,  0.3180,  0.4005,  0.5044,  0.6352,  0.8000
```

(`geomspace(0.01, 0.80, 20)`, ratio 1.2594, then `float(f"{x:.4g}")`; the runner's list must equal this list
exactly.)

**Y = liquidity slack** = household primary-school fee per year as a share of median income = `fee_primary`
on grades 1–6 only (all other fees at `formal_loop` defaults). 20 levels, **exact**:

```
0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09,
0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19
```

`fee_primary = 0.00` is the **fee-abolition (E8) slice**; positive values are pre-abolition regimes.
Secondary forgone earnings, tertiary fee and informal levies remain active in every cell (by design).

**Realised X normalisation** (reported per cell, not used as a grid axis): `x_vac_per_gate_pass` = annual
formal vacancies ÷ children passing the lower-secondary gate (cred ≥ 2) in the measured window, per measured
cohort; and `x_vac_per_lower_complete` (=÷ cred ≥ 1). Reported so the reader can see that the declared X axis
and the realised ratio differ systematically as participation changes.

---

## 3. Gate regimes — and the CONTEST-GATE DECISION (recorded before the run)

Two regimes are run, unchanged from the base pre-registration's `GATES` table:

* **`bar`** — `[bar 3.0, bar 5.5, bar 8.0, bar 11.5]`: a fixed absolute score threshold at each of the four
  transitions (tournament screen with a fixed standard).
* **`quota`** — `[bar 3.0, quota(share=0.55, cut0=7.0), quota(share=0.45, cut0=10.0), bar 11.5]`: at two
  transitions, planned seats = `round(share × N)` and the admission cutoff is endogenous (score-ranked
  seats; the realised cutoff feeds the household belief `self.cut[m]`).

### Decision: **CONTEST GATE = NOT-IMPLEMENTED** (option (b) of the task; not proxied)

The task allowed a third `contest` regime **only** if it could be implemented faithfully, driver-side, as a
subclass of the engine's gate logic using existing score/cred/seats machinery **without editing any engine
file**. That is not possible, for three independently sufficient reasons, with exact evidence:

1. **There is no gate hook to subclass.** The `Module` base class (`engine/eduengine/core.py` lines 60–69)
   exposes only `setup, supply, sector, extras, labour, after, measure, summary`. No module hook touches the
   gate decision. The gate decision is inlined in `Engine.step` (`core.py` ~line 363 onward); no engine gate
   class exists anywhere in the tree.
2. **Only two gate kinds are implemented, and a third kind is silently swallowed.** `core.py` (gate dispatch)
   reads:
   ```
   if gate['kind'] == 'bar':
       ok = score >= gate['bar']
   else:   # quota: seats = share x cohort size ...
       s = np.sort(score[at_gate])[::-1]
       seats = int(round(gate['share'] * p['N']))
   ```
   Any `kind` other than `'bar'` — including `'contest'` — **falls into the quota branch and is silently
   treated as quota**. Passing `kind='contest'` to the engine would therefore be a silent relabelling, which
   the task forbids.
3. **`grep -rn contest` over the engine tree finds exactly one hit, and it is a comment:**
   `engine/eduengine/modules/labour.py:39: # which tiers are ranked contests (the positional race). ...`
   `worlds.py` defines gates with `kind='bar'` and `kind='quota'` only (lines 23–24). There is no
   contest/admission-by-rank rule to reuse.
4. **A "third" regime would also be arithmetically indistinguishable from quota at this design's fixed
   cohort size.** The engine's quota rule is exactly a fixed-seat rank tournament whose seat count is
   `round(share × N)`; with `N = 400` fixed in every cell, absolute-seat `contest` ≡ `quota` by construction.
   A genuinely distinct regime requires decoupling the seat count from cohort size inside `core.step`, i.e.
   editing an engine file — prohibited by the task and by the base pre-registration's code-state pinning.

**Consequence, fixed now:** the sweep runs **`bar` and `quota` only**: 20 X × 20 Y × 2 gates × 20 seeds =
**16,000 runs**, 800 cells. No `contest` label appears in any output. The report will state
`contest gate NOT-IMPLEMENTED` with the evidence above. (If this decision is ever revisited, an amendment must
be committed **before** the affected run.)

---

## 4. Runs, seeds, cost

* Grid: 20 X levels × 20 Y levels × 2 gates = **800 cells**.
* Seeds: **0..19 (20 seeds per cell)**, identical seed set in every cell and gate. Stochastic inputs come only
  from the engine's `np.random.default_rng(seed)`; seeds are the only source of run-to-run variation.
* Total runs: **20 × 20 × 2 × 20 = 16,000** (16,000 seed-level rows).
* Runner: `phase_sweep_full.py` (in this directory), a strict extension of the committed
  `phase_sweep_quick.py`: 20/20 levels, `--gate {bar,quota}`, `--seeds 20`, optional `--pilot`.
* Host: warm AutoDL box (`/root/miniconda3/bin/python`, `--workers 12` of a 15-CPU quota), engine at
  `/root/work/edsystem/engine`, output dir `/root/work/equifinality_phase/` (nothing written outside it on the
  box). Engine code hashes (sha256 of `worlds.py` + every `eduengine/**/*.py`) are written into the run JSON.
* Expected cost (declared): the base quick run did 500 runs in 35.4 s at 12 workers (0.071 s/run effective);
  16,000 runs therefore ≈ 19 min of worker time, budget **20–50 min wall** for box contention. Timing is
  reported, not assumed.
* No GPU; no power/reboot/shutdown command on any machine, ever; no watchers, timers, cron or at-jobs.

---

## 5. Per-run read-out (all seed-level, preserved)

One row per run. Primary definitions (all computed on the measured population as defined in §1):

| column | definition |
|---|---|
| `ger_sim` | **`GER_sim = 1 − never_enrolled_share`** — *declared simulated participation*, NOT an empirical GER. `never_enrolled` = exit reason 4. |
| `liq_share` | share of measured population with exit reason 1 (liquidity) |
| `tut_rate` | engine `out['tut_rate']` = share of pupils receiving tutoring in the measured window |
| `tut_q5_q1_gap` | `tut_by_q[4] − tut_by_q[0]` |
| `completion_lower` | engine lower-secondary completion (secondary outcome) |
| exit shares | `liq_share, gate_fail_share, censored_share, choice_share, never_share, no_seat_share, not_admitted_share, finished_share` (partition to 1.0) |
| q1/q5 | `liq_share_q1, liq_share_q5, gate_fail_share_q1, gate_fail_share_q5, tut_share_q1, tut_share_q5` |
| labour | `formal_rate, queue, grad_unemp, formal_hire_q1, formal_hire_q5` |
| realised X | `x_vac0, x_vac_per_entrant, x_vac_per_lower_complete, x_vac_per_gate_pass` |
| gate diagnostics | `gate_pass_rate_0..3` (`e.pass_rate` at end of run), `cut_0..3` (`e.cut`), `cut_adm_0..3` (`e.cut_adm`) — descriptive; used to show whether a quota gate binds |
| run health | `n_pop_measured, n_cohorts_measured, ok, error` |

`ok=False` rows carry the exception text and are **preserved** in the per-run CSV and counted in the report;
they are excluded from seed means only by explicit `None` propagation (never silently imputed).

Any pair/cell computation using a missing (`None`) primary value is excluded from the equifinality search and
the number of excluded pairs is reported.

---

## 6. Equifinality definition (fixed exactly, before data)

Cell values are **seed-mean values over seeds 0..19**; the seed SD of each primary metric is also recorded.
All differences are in **percentage points (pp)** = 100 × (share difference), i.e. shares are multiplied by
100 first and `Δ` is taken on those pp values.

**Qualifying pair.** An unordered pair of **distinct** cells `(a, b)` is *equifinal* iff **all** of:

1. `|ΔGER_sim| = |GER_sim(a) − GER_sim(b)| < 0.5 pp` (near-identical declared simulated participation), **and**
2. `|Δliq_share| > 25 pp` **OR** `|Δtut_rate| > 20 pp` (very different exclusion composition or shadow-education
   uptake). Absolute values are used because equifinality is direction-agnostic; the **sign** of each `Δ` is
   reported for every qualifying pair.

**Scope of the exhaustive search (declared):**
* **Primary family — within-gate pairs.** Pairs of distinct cells **under the same gate regime**
  (`bar` with `bar`: C(400,2) = 79,800 pairs; `quota` with `quota`: 79,800; **159,600** within-gate pairs).
  A gate change is a discrete regime switch, not a point in the continuous X×Y plane, so cross-gate pairs are
  reported separately rather than pooled into the primary count.
* **Secondary family — cross-gate pairs.** Every `bar` × `quota` pair: 400 × 400 = **160,000** pairs, reported
  separately and labelled.
* These two families together are **every unordered pair of distinct cells = C(800,2) = 319,600** — the search
  is exhaustive over the whole 800-cell design; the split is a declared reporting convention, not a filter.

**Ranking.** Qualifying pairs are ranked by `|Δliq_share| + |Δtut_rate|` (pp, descending); the top 50 are
tabulated with both cells' full coordinates (gate, X index/value, Y index/value) and the three metrics, and
**the complete qualifying set is written to CSV** (not just the top 50).

**Descriptives to report (declared):** qualifying pair counts (total, per gate, per family); number of
distinct cells involved; the maximum number of qualifying partners a single cell has; the seed-mean
`|ΔGER_sim|`, `|Δliq|`, `|Δtut|` distributions among qualifying pairs; and, for the top pairs, the observed
seed-level SDs so the reader can see whether a 0.5 pp GER tolerance is above sampling noise.

**No post-hoc adjustment of the thresholds, the tolerance, the pp units, or the pair scope after seeing data.**

---

## 7. Null / expected-count reference (fixed before data)

Because 159,600 within-gate pairs are examined, a raw pair count is meaningless without a chance reference.
Declared null: **1,000 label-permutation nulls.**

* For permutation `k = 0..999`: within **each gate regime separately**, independently permute the *cell
  labels* of each of the three outcome vectors `GER_sim`, `liq_share`, `tut_rate` across the 400 cells (three
  independent permutations per gate, drawn with `np.random.default_rng(20261125 + k)`). This preserves each
  metric's marginal distribution and each cell's (X,Y) coordinate, and destroys any association among the
  three metrics and between metrics and position — exactly the structure the conjunction in §6 exploits.
* Recompute the §6 count on the permuted data, retaining the same pair family (same-gate pairs on the
  permuted assignment; cross-gate pairs on the permuted assignment) and the same thresholds.
* Report: observed count, null mean, null SD, null 2.5th/50th/97.5th percentiles and max, and the one-sided
  permutation p-value `p = (1 + #{null_k ≥ observed}) / 1001`, separately for the within-gate family
  (primary), the cross-gate family, and each gate's own within-gate count. Also report the ratio
  observed / null-mean.

Pre-declared reading:
* `observed ≤ null 97.5th percentile` ⇒ **"no evidence of equifinality beyond chance"**; quote both numbers.
* `observed > null 97.5th percentile` ⇒ **"excess equifinality"**; quote observed, null mean, ratio and `p`.
* Either way the top-pair table is reported and the result is phrased descriptively (no causal reading).

---

## 8. Secondary outcomes and optional diagnostics (declared now)

1. **`completion_lower`** — seed-mean per cell, per-gate range, and the same pairing exercise run once as a
   *descriptive* secondary: pairs with `|ΔGER_sim| < 0.5 pp` **and** `|Δcompletion_lower| > 20 pp`. No verdict;
   counts and top pairs only.
2. **Phase-boundary diagnostics** — only if cheap: per gate, `J_edge = |ΔM| / σ_med` for axis-adjacent
   (grid-neighbour) cell pairs for `M ∈ {GER_sim, liq_share, tut_rate}`, `J_max`, and
   `sharpness = J_max / median(J_edge)`, plus the bar/quota contrast `C` as in the base pre-registration §4;
   **descriptive only, no phase-transition verdict in this record** (the phase-transition verdict belongs to
   the sibling phase-transition workstream). If the compute is not cheap, these are dropped and said to be
   dropped.
3. **Gate-binding diagnostic** — per cell: `gate_pass_rate_*` and final `cut_*`. Declared because `quota` seats
   are `round(share × N)` with `N = 400` while the taker pool at that gate is smaller; if a quota gate turns
   out non-binding in most cells, that is **reported as a property of the design**, not repaired by
   post-hoc re-tuning.

---

## 9. Validity checks and failure handling (enforced, not optional)

* Exit partition sums to 1.0 within 1e-6 for every run; violation aborts the run and is reported verbatim.
* `GER_sim`, `liq_share`, `tut_rate`, `completion_lower` in [0, 1] (or `None`); `censored_share` reported.
* Every run's `ok`/`error` kept; failures never dropped. Cell seed-means use only `ok` rows and record
  `n_seeds_ok`.
* Engine hash, runner hash and (later) analysis-script hash recorded in the outputs; the analysis is a pure
  function of the committed run CSV + JSON.
* Determinism: same seeds, same order of cells; a re-run must reproduce the seed-mean cells bit-for-bit
  (checked on a 0.5% random subset if a re-run is affordable; otherwise declared untested).
* Data volume: 16,000 seed-level rows are committed as CSV if < 20 MB (expected ≈ 8–12 MB), together with the
  per-cell summary; if larger, gzip and commit that, and say so.

---

## 10. Outputs (names fixed before running)

In this directory: `PRE_REGISTRATION.md`, `phase_sweep_full.py`, `analyze_equifinality.py`, `REPORT.md`,
`data/phase_sweep_full_runs.csv`, `data/phase_sweep_full_summary.csv`, `data/phase_sweep_full_summary.json`,
`data/equifinality_pairs.csv`, `data/equifinality_top50.csv`, `data/equifinality_null.json`,
`data/equifinality_report.json`, `data/analysis_manifest.json` (all code/engine hashes + label).

Every file, every row-level label, every report section carries
`SIMULATION ONLY — eduengine toy worlds; no causal/empirical claims`.

---

## 11. Commit discipline

* This pre-registration is committed **alone**, before any run, and its SHA is reported to the Lead.
* The runner, the run outputs and the analysis are added in later **additive** commits on
  `research/equifinality-phase-2026-11-25`; the branch is pushed with `git push -u origin ...`; never forced,
  never to `main`. No engine file is edited; the engine is pinned by hash in the run metadata.
* Revising the prereg is allowed **only** as a dated amendment committed **before** the run it affects, and it
  is reported to the Lead and listed in the deviation log.

**Deviation log:** (none at commit time)
