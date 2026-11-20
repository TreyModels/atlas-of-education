# PRE-DECLARATIONS — Cluster A toy experiments (#1–#3)

**ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no historical test; phase closed; do not cite numbers as estimates.**

Written **before the first run** of `code/run_cluster_a.py`. No result from these runs existed when this file was
created; the parameter vectors and thresholds below are fixed and will not be changed after seeing output. Only
mechanical non-degeneracy was checked on paper (expected household counts at baseline / +20% / −20%), not outcome
levels.

Source spec: `extensions_archive/codex_2026-11-20/COUNCIL_TOY_SPECS_015.md`, Cluster A,
experiments #1 (entry-threshold hysteresis), #2 (public expansion, net vs gross), #3 (entry lag and overshoot).
Base toy: `/tmp/codex_unpack/codex-massification-5eec11470690/workspace/model.py` and `experiments.py`
(household side reused; provider side replaced by the fixed-cost threshold rule the spec asks for).

---

## 0. Global protocol

| Item | Declaration |
|---|---|
| Language | Python 3.10, **stdlib only** (no numpy in the model or the run) |
| Seeds | `seed_i = 20261120 + i`, `i = 0 … 199` → **200 seeds per cell** (protocol floor is 100) |
| Pairing | Each seed's latent cohort — budgets, opportunity costs, lottery order — is drawn **once** and reused in every arm and every counterfactual of that seed. Identical latent draws, one-factor shocks. |
| Matched start | Period 1 multiplier = 1.00 for all arms; private sector initialised at the period-1 equilibrium for that same cohort (mature providers, `age ≥ 1`), identically across arms. |
| Units | Applications ≠ public admissions ≠ private admissions ≠ installed seats. Every metric is labelled. |
| Reporting | **All** cells are written to `RESULTS.csv`, including degenerate / censored ones. Censored scalars use the sentinel `-1` and are counted in `FINDINGS.md`. |
| Inference | None. No standard errors, no p-values, no significance language. "PASS/FAIL" below means only "the toy's output does / does not match the pattern predeclared for the toy". |
| Reps | 200 seeds × all cells; deterministic, so a rerun reproduces `RESULTS.csv` bit-for-bit. |

### 0.1 Household side (inherited unchanged from the base toy)

* `N = 100`; budgets: 50 × 1.5 and 50 × 4.0, shuffled; opportunity cost `c_i ~ U[0, 3.5)`; a public lottery order.
* premium `P = 4.0 × multiplier`. Apply iff `P − c_i ≥ 1.0` (public fee). Public seats take the first
  `public_seats` applicants **in lottery order**.
* Private customers: waiting-list households with `budget_i ≥ 2.0` (private tuition) **and** `P − c_i ≥ 2.0`.
* Tuition 2.0, variable cost 1.0 → unit contribution **1.00 per seat**. Break-even seats
  `bk = F_cents / 100` (integer by construction), i.e. entry iff `qty · (tuition − varcost) ≥ F`.

### 0.2 Provider side (the stipulated change)

1. Providers are **lumpy capacity units of `cap` seats**. A provider installs
   `min(cap, unmet customers at its decision date)` and **never partially contracts**: it is either active at its
   installed size or gone (provider exit).
2. **Entry threshold:** an inactive provider is added only if unmet customers
   `≥ bk` (i.e. `qty · 1.00 ≥ F`). At most `max_providers` providers exist.
3. **Exit rule:** an active provider whose allocated customers `< bk` exits immediately (capacity withdrawn).
4. **Installation lock:** a provider cannot exit in its first active period (one-period irreversibility).
5. **Pipeline awareness:** entrants observe capacity already under construction, so at most one cohort of orders is
   placed per shortage. (Over-entry therefore requires the entry lag itself to outlast the demand boom — this is what
   #3 tests.)
6. Allocation: active providers fill in entry order, each up to its installed capacity.

### 0.3 Declared deviations from the Council spec (each is a stipulation, not a finding)

* **#1 uses a market of 4 providers × 8 seats** instead of the base toy's single 30-seat provider, so that *entry*
  and *exit* events are both observable in the same market. F is rescaled so that break-even sits inside one
  provider's capacity (`F ≤ cap × contribution`); the base toy's `F = $12.00` against a 30-seat provider is not
  expressible in a 4 × 8 market.
* **#1 adds period 4** (shock ends) to trace the path and to test whether the level recovers; the spec's "demand
  shock ±20% over two periods" is implemented as periods 2–3 shocked, period 4 back to baseline.
* **#2 adds a `cap = 30, M = 1` replication** because the spec says "private fixed cost **and capacity** varied".
  The four primary cells are `cap = 15, M = 2`; the replication is secondary.
* **#3 fixes the temporary boom at 4 periods** (t = 2…5) because the spec leaves "temporary" undefined. Permanent =
  t ≥ 2 forever. The duration choice is a stipulation and is reported as such (with L ∈ {0,2,4}, a 4-period boom is
  the boundary at which L = 4 necessarily lands after the boom).

---

## 1. Experiment #1 — Entry-threshold hysteresis

**Question.** Does a fixed-cost entry threshold with exit-when-unmet generate an asymmetric supply response
(exit faster/stronger than entry) after a ±20% demand shock?

**Parameter vector (imposed).**
`N=100, public_seats=30, public_fee=1.0, tuition=2.0, varcost=1.0, cap=8, max_providers=4, M·cap=32`.
Arms: `F_low = $4.00 → bk=4` and `F_high = $8.00 → bk=8 (= cap)`.
Demand path (premium multiplier), periods t = 1…4:
`shock_up   = [1.00, 1.20, 1.20, 1.00]`, `shock_down = [1.00, 0.80, 0.80, 1.00]`.
4 cells = {F_low, F_high} × {up, down}, 200 seeds, all four cells on the same 200 latent cohorts.

**Estimand.** Net private **installed seats** and private **admissions** path over t = 1…4, public admissions,
applications, provider counts, exit/entry events. Asymmetry at impact (t1 → t2):
`exit_seats_down = max(0, seats_t1 − seats_t2)` in the down cell and
`entry_seats_up = max(0, seats_t2 − seats_t1)` in the up cell, each on the same cohorts;
`A_F = mean(exit_seats_down) / mean(entry_seats_up)` (undefined → reported as censored if the denominator is 0).

**Predeclared threshold.** The fixed-cost hysteresis story PASSES only if **both** hold:
* (T1a) `A_high ≥ 1.25` — high-F exit is at least 25% stronger than high-F entry;
* (T1b) `A_high − A_low ≥ 0.25` — the asymmetry is specific to the high fixed cost (low-F stays near symmetric).

**Predeclared falsifier.** `A_high ≤ 1.00` **or** (`A_high < 1.25` and `A_high − A_low < 0.25`): no asymmetry —
the fixed-cost story adds nothing to a plain capacity story. Band `1.00 < A_high < 1.25` = weak/ambiguous, reported
as such.

**Secondary, predeclared (descriptive, no threshold).** (i) share of seeds with a private exit under down-shock;
(ii) share with a private entry under up-shock; (iii) recovery ratio `seats_t4 / seats_t1` — level hysteresis would
show `< 1`; (iv) the customer-count changes `−Δ̄` vs `+Δ̄`, to show whether any seat asymmetry is inherited from
demand asymmetry or from the threshold itself.

---

## 2. Experiment #2 — Public expansion with private exit (net vs gross)

**Question.** How much of a public seat expansion survives private provider exit?

**Parameter vector (imposed).**
`N=100, public_fee=1.0, tuition=2.0, varcost=1.0`.
Primary: `cap=15, max_providers=2` (private capacity 30). Secondary replication: `cap=30, max_providers=1`.
Arms: `F_low = $4.00 (bk=4)` / `F_high = $12.00 (bk=12)` × expansion `{30→50, 38→39}`.
Comparative statics: pre-state and post-state are each the **static equilibrium with mature providers** at the same
premium (`P = 4.0`) and the same latent cohort. 8 cells (4 primary + 4 secondary), 200 seeds, paired
pre/post within seed, and all cells on the same cohorts.

**Estimand.** `gross_gain = public_admissions_post − public_admissions_pre`;
`net_gain = total_admissions_post − total_admissions_pre`;
`retention R = mean(net_gain) / mean(gross_gain)`; private exit count `providers_pre − providers_post`; private
seats and admissions lost; applications (constant by construction — demand is not shocked).

**Predeclared threshold.** PASSES only if all three hold:
* (T2a) `R(F_high, 30→50) < 0.50` — less than half the gross public gain survives;
* (T2b) `R(F_low, 30→50) ≥ 0.50` — the offset is specific to the high fixed cost;
* (T2c) `share of seeds with a private exit in F_high × 30→50 ≥ 0.50`.

**Predeclared falsifier.** `R(F_high, 30→50) ≥ 0.90` → net ≈ gross, no offsetting exit; the fixed-cost exit
channel contributes nothing. Band `0.50 ≤ R < 0.90` = partial offset (fail of the declared <50% threshold, reported
as such).

**Secondary, predeclared (descriptive, no threshold).** `38→39` is a near-threshold probe: for `F_high` the exit
trigger rate and `R` are reported **without** a directional threshold (a one-seat expansion can tip a provider whose
break-even sits at the pre-expansion customer count, and the toy cannot tell us whether that is common in the world);
for `F_low` we predeclare only `exit trigger rate ≤ 0.05` (bk = 4 is far below the customer pool). `cap=30`
replication is reported against T2a/T2b as a robustness check, not as an independent test.

---

## 3. Experiment #3 — Provider entry lag and overshoot

**Question.** Does a lag between the entry decision and installed capacity produce enrolment deficits during a boom
and idle capacity (overshoot) after it?

**Parameter vector (imposed).**
`N=100, public_seats=30, public_fee=1.0, tuition=2.0, varcost=1.0, cap=12, max_providers=4, F=$4.00 (bk=4)`,
`T = 12` periods. `L ∈ {0, 2, 4}` = periods between an order and the provider's first active period
(`L = 0` = capacity available in the same period as the decision).
Shock: `temporary = [1.00, 1.20, 1.20, 1.20, 1.20, 1.00, … 1.00]` (boom t = 2…5);
`permanent = [1.00, 1.20 × 11]` (boom from t = 2 onward).
6 cells = L × {temporary, permanent}, 200 seeds, all six cells on the same cohorts.

**Estimand.** Per period: installed private seats, private admissions, `vacancy = seats − admissions`,
`backlog = customers − admissions`, providers. Scalars:
`peak_vacancy = max_t max(0, seats_t − customers_t)`; `peak_backlog = max_t max(0, customers_t − seats_t)`;
`cumulative_vacancy = Σ_t (seats_t − admissions_t)` (seat-periods);
`time_to_steady_state` = first `t ≥ 2` such that `seats_s == equilibrium_seats(customers_s)` for all `s ≥ t`
(−1 if never within T; counted as censored);
paired gaps vs the same seed's `L = 0` cell: `peak_admission_shortfall = max_t (served_L0 − served_L)` and
`peak_admission_excess = max_t (served_L − served_L0)`.

**Predeclared threshold.** PASSES only if all three hold:
* (T3a) `mean peak_vacancy(L=4, temporary) ≥ 8.0 seats` (at least 8 idle installed seats at peak);
* (T3b) `mean peak_vacancy(L=4, temporary) ≥ mean peak_vacancy(L=0, temporary) + 4.0 seats`;
* (T3c) `mean peak_vacancy(L=4, permanent) < 4.0 seats` — overshoot requires the *temporary* shock.

**Predeclared falsifier.** `mean peak_vacancy(L=4, temporary) ≤ mean peak_vacancy(L=0, temporary) + 2.0` → the lag
has no overshoot effect; no dynamic supply story.

**Secondary, predeclared (descriptive).** monotonicity `peak_vacancy` and `cumulative_vacancy` across L ∈ {0,2,4}
for the temporary shock; peak backlog during the boom (the opposite error); censored `time_to_steady_state` counts.

---

## 4. Analysis plan and file hashes

`code/run_cluster_a.py` writes `RESULTS.csv` (long format: `experiment,arm,seed,metric,value`) with one block per
seed plus aggregate rows (`seed = AGG`) for every mean / ratio / share named above, and `RESULTS_SUMMARY.json`
(the exact numbers quoted in `FINDINGS.md`). `RUN_MANIFEST.json` records seeds, reps, Python version, the full
imposed parameter vectors, and SHA-256 of every artefact. Thresholds and falsifiers are evaluated mechanically in
`code/verdicts.py` from those numbers.

Nothing outside `extensions_archive/toys_2026-11-20/cluster_A/` is written; no phase/closed-anchor file is touched;
no git action is taken.

---

## AMENDMENT 1 — written before the final 200-seed run (disclosed, supersedes §1–§3 vectors)

**When.** After a 6-seed mechanics smoke test (`--smoke`, stdout only, no file written) and a demand-count check, and
**before** the final 200-seed run whose output is delivered. No delivered result existed at the time of this amendment.

**Why (two mechanical defects, no result was used to set a threshold).**

1. **Provider capacity rule.** The first engine draft let a provider install `min(cap, unmet customers)` at entry
   ("build to demand"). That is *not* the base toy's provider: `model.py` fixes `PRIVATE_CAPACITY = 30` and the
   provider serves `min(30, customers)`, i.e. capacity is a fixed lump whose *utilisation* varies. The primary rule is
   therefore **fixed capacity lumps** (`mode = "lump"`). Because the capacity rule is exactly the assumption that can
   generate or destroy the #1 asymmetry, the discarded "build to demand" rule is kept as a **declared robustness cell**
   for #1 (`mode = "divisible"`, 4 extra cells) rather than being hidden.
2. **Break-even scale.** With fixed lumps, `F` must not exceed one provider's contribution, and the high-F arm is
   standardised at **`bk = cap`** — "a provider breaks even only when fully utilised". This is one rule applied in all
   three experiments: `$8.00 / 8 seats` (#1), `$15.00 / 15 seats` (#2), `$4.00 / 4 seats` (#3). `#2` additionally
   retains **`F = $12.00` (the base toy's own value)** as a reported sensitivity cell, because the demand check showed
   `bk = 12` sits exactly on the mean post-expansion customer pool (12.2 households) — i.e. it is a knife-edge, not a
   clean test. Reporting it means the pre-amendment parameterisation is visible, not discarded.
3. **#3 granularity.** `cap = 12, M = 4` could not express a two-unit over-build inside the boom shortage; `cap = 4,
   M = 10, F = $4.00 (bk = cap)` can. Chosen so that break-even = one capacity unit, as above.

**Final parameter vectors (these are the imposed vectors; they are dumped into `RUN_MANIFEST.json`).**

| | #1 | #2 | #3 |
|---|---|---|---|
| `public_seats` | 30 | 30→50 and 38→39 | 30 |
| `cap` / `max_providers` | 8 / 4 | 15 / 2 (primary), 30 / 1 (secondary) | 4 / 10 |
| `F` (cents) | 400 (bk 4), 800 (bk 8 = cap) | 400 (bk 4), **1200 (bk 12, sensitivity)**, 1500 (bk 15 = cap) | 400 (bk 4 = cap) |
| demand | t=1…4: 1.00, ±0.20, ±0.20, 1.00 | P = 4.0 both states | temp 1.00, 1.20×4, 1.00×7; perm 1.00, 1.20×11 |
| entry lag | 0 (contemporaneous) | n/a (comparative statics) | L ∈ {0, 2, 4} |
| cells | 4 primary + 4 robustness | 4 primary + 8 secondary | 6 |

**Thresholds and falsifiers are unchanged** from §1–§3. T1a `A_high ≥ 1.25`; T1b `A_high − A_low ≥ 0.25`;
T2a `R(F_high, 30→50) < 0.50`; T2b `R(F_low, 30→50) ≥ 0.50`; T2c exit share ≥ 0.50;
T3a `mean peak vacancy (L=4, temporary) ≥ 8.0`; T3b `≥ L0 + 4.0`; T3c `L=4 permanent < 4.0`.

**Disclosure of what the smoke test already showed (so the reader can see it was not used to move a bar).**
The 6-seed smoke produced `R(F_high=$12.00, 30→50) ≈ 0.82` (a partial offset) — that number is *why* `$12.00` is kept
and reported as a sensitivity cell instead of being dropped. The smoke also produced `A_high ≈ 1.0` /
`A_low ≈ 1.5` under the discarded "build-to-demand" rule, which is why that rule is reported as a robustness cell.
Neither smoke number is a delivered result; both are reproduced by the full run and quoted in `FINDINGS.md` only as
sensitivity comparisons.
