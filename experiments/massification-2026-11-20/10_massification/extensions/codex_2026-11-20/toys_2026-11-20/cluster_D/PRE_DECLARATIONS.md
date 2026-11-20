# PRE-DECLARATIONS — Cluster D toys (#10, #11, #12)

**ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no historical test; phase closed; do not cite numbers as estimates.**

Written **before** the run (`RESULTS.csv`, `FINDINGS.md` did not exist at the time of writing). Authority:
`extensions_archive/codex_2026-11-20/COUNCIL_TOY_SPECS_015.md` §Cluster D. This file fixes, in advance, the
model, the arms, the estimands, the thresholds, the decision rules, the falsifiers and the reporting rules.
Nothing below is tuned to data; there are no data. The only inputs are the stipulated rules of the toy.

Prohibitions honoured by this battery: it does **not** reopen the closed massification phase, does **not** test a
historical claim, does **not** calibrate any parameter, does **not** touch phase/closed-anchor files, and is
not written into any results table of the closed phase.
Closeout facts the toys are only *pedagogically adjacent* to (not re-tested here): direction unidentifiable (R13),
income-scaling sign wrong (R27/C1), ceiling residual 14.97 pp UNABLE, capacity floor-not-ceiling (A10/R29),
timing censored.

---

## 0. Protocol (all three experiments)

- Python 3.10, **stdlib only** (`random`, `statistics`, `csv`, `json`, `hashlib`, `pathlib`, `math`).
  No numpy in the model path (numpy is available in the environment but is not used).
- `SEEDS = 240` per cell, `seed ∈ {20261120 + 1, …, 20261120 + 240}` fixed in advance.
- **Paired counterfactuals, identical latent draws.** All arms inside one experiment consume the *same* latent
  cohort draws for a given seed: cohort `(seed, t, slot)` is a pure function of `(seed, t, slot)`, independent
  of arm. Therefore every arm sees byte-identical persons in every cohort-year; only the stipulated rule changed.
- **Matched starting conditions.** Baseline seat stock, readers, formal share, skill stock and the endowment
  construction rule are identical across arms at `t = 0`; the treatment enters only through the declared
  one-factor change.
- **One-factor shocks.** #10 varies only the level-timing schedule (PV-equal); #11 varies only cohort size ×
  the capacity-scaling rule; #12 varies only the lease and/or the expectation regime.
- **All cells reported**, including nulls and failures, with the imposed parameter vector in every output.
- Estimand sign convention: a **gap** is `arm − its paired control`, so positive = arm higher.
- "Never crossed" is encoded as crossing year `31` with `censored = 1` (horizon is 30 cohorts).
- Every output row carries the label string
  `ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence`.

## 1. Shared engine (extension of `takeoff.py`)

Three levels, completed in sequence, one gate per cohort; a cohort passes a gate within one step.
`N = 120` nominal cohort; 3 equal-size resource groups (`i % 3`); 30 cohorts; seats persist; construction has
no delay inside a cohort-year; the state construction budget is rationed to the level with the largest
unmet-application backlog (`build_limit = 12`; `budget = min(12, 3 + int(hires*0.16))`).

Per-slot latent draws (independent of cohort size, so prefix pairing across the #11 size arms is exact):

```
group(i) = i % 3
cash(i)   = (0.24, 0.62, 1.05)[group] + U(0, 0.50)
home(i)   = (0.65, 0.42, 0.25)[group] * U(0.45, 1.55)     # home-work opportunity cost
apt(i)    = U(0, 1)
lottery   = stable shuffle of slots 0..143, then take first n slots
```

Gate for level `k` of cohort `t` (kept from `takeoff.py`): household applies iff

```
cash(i) >= fee[k]  and  payoff[k]*(0.7 + apt(i)) + access[k] + rank[k] >= fee[k] + home(i)*work_mult[k]*work
access[0] = 0.14                                       # administrative demand seeds primary
access[k] = access_raw[k] * readers * formal_share_{t-1} * 5      (k >= 1)
rank[k]   = rank_raw[k]   * readers * formal_share_{t-1} * 4
```

`admitted = applicants[:cap[k]]`; admission is rationed by the installed seat stock in `lottery` order.

Labour market (kept from `takeoff.py`): `skill_stock = 0.8*skill_stock + 0.2*mean(skill)`;
`posts` responsive `= round(n*(0.10 + 0.52*capital*skill_stock))`, frozen `= 40` (the `JOBS = 40` of
`model.py`); credential gating `gated = round(posts*readers)`; credential hires = highest `stage` with
`stage >= 2`; remaining posts filled by aptitude; `formal_share = hires/n`;
`readers = 0.05 + 0.85*share(stage >= 2)`;
`placement_signal = (upper-secondary completers hired) / (upper-secondary completers)`.
Output is computed but is **not** an estimand of this battery (it is carried only for completeness).

### Imposed parameter vector (recorded in `RUN_MANIFEST.json` and every `RESULTS.csv` row group)

| component | value |
|---|---|
| cohort nominal `N` | 120 |
| cohorts (horizon) | 30 |
| max cohort (draw grid) | 144 |
| `fee` (primary, lower-sec, upper-sec) | 0.20, 0.36, 0.55 |
| `work_mult` | 0.85, 1.35, 1.80 |
| `payoff` | 0.65, 0.51, 0.42 |
| `access_raw` | 0.14, 0.90, 0.30 |
| `rank_raw` | 0.05, 0.20, 0.65 |
| `skill_gain` | 0.25, 0.40, 0.60 |
| `seat0` | 18, 0, 0 |
| `build_limit` | 12 |
| `work` / `capital` | 1.0 / 1.0 |
| `fixed_posts` (frozen-capacity employer) | 40 |
| PV discount `delta` (exp #10) | 0.97 |
| PV budget per level (exp #10) | 40 seat-years |
| seeds per cell | 240 |
| seed base | 20261120 |

### Crossing definitions (fixed now, no post-hoc variants reported as primary)

Per **cohort** (not a cumulative stock), level `k` crossing year
`X(k, θ) = min{t : completions_k(t) / cohort_size(t) >= θ}`, else `31` with `censored = 1`.

| milestone | definition |
|---|---|
| `M0` floor take-off | primary completions ≥ **50 %** of cohort |
| `M1` floor universal | primary completions ≥ **90 %** of cohort |
| `M2` middle take-off | lower-secondary completions ≥ **50 %** of cohort |
| `M3` ceiling take-off | upper-secondary completions ≥ **50 %** of cohort |
| `U90` ceiling universal | upper-secondary completions ≥ **90 %** of cohort (expected censored; A10 mirror) |

Derived: spacing `S = X(M3) − X(M0)` (floor→ceiling), level spacing `X(M3) − X(M2)`,
floor/ceiling completion gap at horizon `= mean_{t=26..30} upper_share − mean_{t=26..30} primary_share`,
and `prim_universal_reachable = 1 − censored(M1)`.

---

## 2. Experiment #10 — Level-first roll-out and crossing order

**Question.** Does the *order* in which levels expand change crossing years and the floor/ceiling asymmetry?
**Treatment (one factor):** a PV-equal seat-expansion schedule. Each level receives the same present value,
`40 seat-years` discounted at `δ = 0.97`; injected seats are permanent additions to installed capacity
(unlike #12). Nominal injection in year `t` inside a level's window `[a,b]` is
`(40 / (b−a+1)) · δ^{−t}`, so PV over the window is 40 by construction.

| arm | primary window | lower-sec window | upper-sec window |
|---|---|---|---|
| `control` | — | — | — |
| `primary_first` | cohorts 1–5 | cohorts 6–10 | cohorts 11–15 |
| `lower_first` | cohorts 6–10 | cohorts 1–5 | cohorts 11–15 |
| `upper_first` (spec's "secondary-first" alternative, top-down) | cohorts 11–15 | cohorts 6–10 | cohorts 1–5 |
| `simultaneous` | cohorts 1–15 | cohorts 1–15 | cohorts 1–15 |

**Estimands.** `X(M0..M3)`, `U90`, `S = X(M3) − X(M0)`, level spacing, crossing order per seed,
final completion shares, total upper-secondary completions over 30 cohorts.
**Paired control:** `control` (no injection), same seed, identical latents.

### Pre-declared thresholds (all three must hold for SUPPORTED)

- **P10-1 — order.** In *each* sequential arm (`primary_first`, `lower_first`, `upper_first`), the fraction of
  seeds satisfying the non-decreasing order `X(M0) ≤ X(M2) ≤ X(M3)` is **≥ 0.90**. (Ties allowed;
  censored milestones are ordered by the sentinel 31.)
- **P10-2 — declared spacing vs compression.** Median `S` (floor→ceiling spacing):
  `primary_first` **≥ 2 years**, `simultaneous` **≤ 1 year**, and the paired median of
  `S(primary_first) − S(simultaneous)` **≥ 2 years**.
- **P10-3 — crossing-year band.** `median |X(M3) − X(M3, simultaneous)| ≥ 1.0 year` for at least one
  sequential arm (the declared band; order must move the ceiling crossing by more than one cohort).
- **Interval prediction (secondary, not decisive):** `S(primary_first) ∈ [2, 12]` years, and consecutive
  level-take-off gaps in every sequential arm ≥ 1 year.

**Decision rule.** `SUPPORTED` iff P10-1 ∧ P10-2 ∧ P10-3. `PARTIAL` iff exactly one or two of
{P10-1, P10-2, P10-3} hold. `FALSIFIED` iff P10-1 fails **and** P10-3 fails.

**Falsifier (pre-declared).** Roll-out order has no effect on crossing order: crossing order identical across
all arms and `|X(M3) − X(M3, simultaneous)| < 1` year. If so, order is not a mechanism in this toy and the
"level-first sequencing" story adds nothing to capacity-at-a-level.

**Declared expected failure mode (recorded before the run, not decisive):** because upper-secondary gates
require completed lower-secondary, the `upper_first` arm should show *wasted* early ceiling capacity
(empty seats while no cohort is eligible), i.e. capacity at the top without feeders reproduces the A10
"floor before ceiling" asymmetry. This is a property of the stipulated gate sequence, not evidence.

---

## 3. Experiment #11 — Cohort-size shock × capacity

**Question.** Does a demographic shock change completion timing only when capacity is frozen?
**Treatment (one factor, two dimensions):** permanent cohort-size step `n ∈ {96, 120, 144}` (= ±20 % of the
120 nominal, balanced groups) × capacity rule `frozen` (installed seats fixed in absolute terms, employer
posts fixed at 40) vs `responsive` (installed seats and the construction budget scale with `n/120`;
employer posts scale with `n`). The shock is a permanent step from cohort 1, not a pulse (declared; a pulse
was considered and excluded as a second factor).

| arm | cohort size | capacity |
|---|---|---|
| `neutral_frozen` | 120 | frozen |
| `up_frozen` | 144 | frozen |
| `down_frozen` | 96 | frozen |
| `neutral_responsive` | 120 | responsive |
| `up_responsive` | 144 | responsive |
| `down_responsive` | 96 | responsive |

Prefix pairing makes the smaller cohort draw-identical to the first `n` slots of the larger cohort, so
`up`/`neutral`/`down` are paired person-for-person on the overlapping slots.

**Estimands.** `X(M0..M3)`, `U90`, primary completion per child at horizon (`mean_{t=26..30}`),
lower/upper completion per child, total primary completions.
**Paired control:** `neutral` within the same capacity rule.

### Pre-declared thresholds

- **P11-1 — timing, frozen only.** Median paired `ΔX(M0)` for `up − neutral`: **frozen ≥ +1.0 year**
  (delay) and **responsive |Δ| ≤ 0.5 year**.
- **P11-2 — interaction (difference-in-differences).** Paired DiD
  `= ΔX(M0 | up−neutral, frozen) − ΔX(M0 | up−neutral, responsive)` has median **≥ 0.75 year**.
- **P11-3 — completion per child.** Median `Δ` primary share at horizon, `up − neutral`:
  **frozen ≤ −0.05** and **responsive ≥ −0.02**.
- **Secondary (reported, not decisive):** the symmetric `down` arms; `down` under frozen should *advance*
  crossings (negative `ΔX`), with the same `|Δ|` band.

**Decision rule.** `SUPPORTED` iff P11-2 ∧ P11-1(frozen half) ∧ P11-3. `PARTIAL` iff P11-2 holds but a
completion/timing half fails. `FALSIFIED` iff P11-2 fails (no interaction) — cohort size and capacity rule
then act separably in this toy.

**Falsifier (pre-declared).** No interaction: the demographic effect on crossings/completion per child is the
same under frozen and responsive capacity (DiD < 0.75 year), so the "capacity constraint" leg is not doing
any work in the toy.

---

## 4. Experiment #12 — Temporary expansion with expectations

**Question.** Does a temporary capacity change move applications/hires through expectations **after** it ends?
**Treatment.** 12 leased upper-secondary seats active for cohorts **2–4** only, then removed. Three
expectation/access variants × two employer regimes; each treatment arm has its own paired no-lease control.

| arm | leased seats 2–4 | fee | expectation regime | employer |
|---|---|---|---|---|
| `control_fixed` / `control_responsive` | none | baseline | observed jobs only (`formal_share` signal) | fixed 40 posts / responsive |
| `supply_only_fixed` / `_responsive` | 12 | baseline | observed jobs only | fixed / responsive |
| `fee_waiver_fixed` / `_responsive` | 12 | upper-sec fee 0.0 during cohorts 2–4 | observed jobs only | fixed / responsive |
| `placement_info_fixed` / `_responsive` | 12 | baseline | **placement-information regime**: upper-secondary `access` and `rank` scale with the observed `placement_signal` (`placement_signal/0.50`, the prior is 0.50) in *all* cohorts | fixed / responsive |

The information regime is a persistent rule change; the lease is temporary. This is the stipulated channel by
which a cohort-2–4 supply shock can leave a trace on cohort-5–7 applications after the seats are gone.

**Windows** (cohort numbers, 1-indexed): `PRE = {1}`, `DURING = {2,3,4}`, `POST = {5,6,7}`,
`DECAY = {16..20}`.
**Estimands.** upper-secondary applications per cohort, total applications, formal hires,
upper-secondary completions — each as a paired gap (arm − paired control) in each window, plus relative
gaps (`gap / control mean`).

### Pre-declared thresholds

- **P12-1 — applications up, hires flat (info × fixed jobs).** Median `POST` relative gap in upper-secondary
  applications for `placement_info_fixed` **≥ +5 %**, while median `POST` hires gap **≤ 1.0 person**.
- **P12-2 — temporary hires, responsive employers.** For `supply_only_responsive`: median `DURING` hires gap
  **≥ +2.0 persons** and `POST` hires gap **≤ 50 %** of the `DURING` gap (decay).
- **P12-3 — persistence with decay (the "declared pattern").** At least one treatment arm shows a `POST`
  upper-secondary application gap **≥ +2 %** relative and a `DECAY` gap **≤ 50 %** of its `POST` gap.
- **Secondary:** the `fee_waiver` arms should raise completions and DURING hires mechanically, with a smaller
  expectation trace than `placement_info`; under fixed jobs the hires gap should be ≈ 0 in every window
  (crowding: more graduates, same 40 posts).

**Decision rule.** `SUPPORTED` iff P12-2 ∧ P12-3 (with P12-1 reported as the applications-up/hires-flat
sub-test). `PARTIAL` iff exactly one holds. `FALSIFIED` iff no arm shows a `POST` gap above ±1 % relative
(no expectation/decay effect) — the temporary expansion then leaves no trace.

**Falsifier (pre-declared).** No difference: temporary expansion leaves no post-expansion gap in any
application window (all `|POST|` and `|DECAY|` relative gaps < 1 %), so expectations/decay add nothing.

---

## 5. Reporting and verdict conventions

- `RESULTS.csv` is long-form, one row per (experiment, arm, seed or aggregate, metric), with
  `censored`, `n`, `definition`, and the mandatory label on every row.
  Aggregates: `median`, `mean`, `p10`, `p90`, `share_gt_0`, `share_censored`, plus paired-gap rows.
- Threshold outcomes appear as explicit rows `THRESHOLD:P10-1`, `THRESHOLD:P11-2`, … with
  `metric = met` (1 = met), the observed statistic, and the rule in `definition`.
- `FINDINGS.md` reports **every** cell, including failures and censored milestones, and gives one of
  `SUPPORTED / PARTIAL / FALSIFIED` per experiment, plus the observed value against each threshold.
- `RUN_MANIFEST.json` records: python version, seeds, imposed parameter vector, per-experiment arm tables,
  runtime, SHA-256 of every produced file, and confirms no phase/closed-anchor file was read or written.
- If a code defect is found after the run, the whole battery is re-run from scratch and both manifests are
  retained; thresholds above are **not** edited. (As written: thresholds are frozen at this file's hash.)

— Cluster D pre-declaration, 2026-11-20, before the run.

---

## 6. Pre-run amendment record (written before the battery run; supersedes §1, §3, §4 where noted)

**Scope of the amendment.** Only *design definitions and stipulated rules* changed, not thresholds. Every
numeric threshold, decision rule and falsifier in §2–§4 stands exactly as first written. These changes were
made after 1–5-seed **debug executions** (checking that the code runs and that the stated mechanism is
actually operative in the toy) and **before** the 240-seed run; the debug values were not used to set any
threshold. Reason for each change is recorded so a reader can judge it.

### 6.1 Engine additions (supersedes parts of §1)

- `per_child` capacity mode: the seat stock is seats per 120 children, so delivered capacity is
  `seat_f * n/120`; otherwise the stock is delivered as absolute seats (`seat_f`). Integer truncation applies.
- `investment_fixed`: when set, the state construction rule becomes a fixed number of nominal seats per
  cohort instead of the `takeoff.py` backlog rule (still rationed to the largest backlog).
- Warm start (`warm_stage`): cohort 1 may arrive with a pre-existing stage composition, and the labour
  market may start from inherited stocks (`init_readers`, `init_formal_share`, `init_skill_stock`).
  Identical in every arm of its experiment.
- Adaptive belief (for #12): state `b` in units of the reference credentialed flow
  `placement_reference = 12` per cohort, updated after each cohort's hiring as
  `b ← 0.70·b + 0.30·(grad_hires / 12)`, starting at `b = 1.0`; under the information regime, upper-secondary
  `access` and `rank` are multiplied by `clip(b, 0.5, 2.0)`; without the regime the multiplier is 1.0.
- Labour-market record additions used as estimands: `cred_hires`, `grad_hires` (upper-secondary completers
  among credential hires), `poor_upper` (composition of upper-secondary completions).

### 6.2 #10 — no change

§2 stands as written: endogenous `takeoff.py` construction rule (`build_limit = 12`), PV-equal schedules,
arms `control / primary_first / lower_first / upper_first / simultaneous`, thresholds P10-1…P10-3 unchanged.
One **secondary diagnostic** was added and is reported: P10-3 restricted to seeds where both ceilings were
actually reached (the sentinel 31 can otherwise satisfy the band through censoring).

### 6.3 #11 — capacity rule redefined (supersedes §3 treatment and arm table)

Two defects in the first sketch were found by debug execution, both of which would have made the factor
non-identical in a way that could manufacture an interaction:

1. The `takeoff.py` backlog rule makes investment depend on **absolute** hires. A "frozen" arm therefore
   built *more* seats for smaller cohorts (normalised demand is higher), and a "responsive" arm double-counted
   responsiveness (scaling both the nominal stock and the delivered capacity). Either way the seat path would
   differ across cohort sizes for reasons unrelated to the capacity rule.
2. Bundling the employer-posts rule with the school-capacity rule would confound two channels.

**As run.** The investment rule is held fixed at **3 nominal seats per cohort** (backlog-rationed) in every
arm, and the employer is **responsive** in every arm (posts per child invariant), so that the *only*
difference between arms is whether delivered capacity tracks cohort size:

| arm | cohort size | capacity rule |
|---|---|---|
| `neutral_frozen` | 120 | absolute seats (`cap = seat_f`) |
| `up_frozen` | 144 | absolute seats |
| `down_frozen` | 96 | absolute seats |
| `neutral_responsive` | 120 | per-child (`cap = seat_f·n/120`) |
| `up_responsive` | 144 | per-child |
| `down_responsive` | 96 | per-child |

Consequences to keep in view when reading the results: (i) absolute seats are *identical across sizes* inside
the frozen arms and seats per child are identical inside the responsive arms, which is what makes the
difference-in-differences interpretable; (ii) with only 3 seats/cohort the capacity constraint binds for the
whole horizon, so milestone `M1` (primary 90 %) is often censored — reported as such.

Thresholds P11-1a/b, P11-2, P11-3a/b and the falsifier are **unchanged**.

### 6.4 #12 — starting conditions and information regime redefined (supersedes §4)

Two defects were found by debug execution:

1. From the `takeoff.py` start, upper-secondary capacity and demand are both dormant: the state construction
   budget is captured by the primary backlog for ~27 cohorts, and `readers` (which drives upper-secondary
   access) stays near its floor. A lease of 12 upper-secondary seats in cohorts 2–4 would therefore have been
   **vacuous** (no eligible upper-secondary cohort exists yet), so the experiment could not test anything.
2. A placement-*rate* signal is not transmitted when posts saturate: with responsive employers the placement
   rate is pinned at 1.0 and does not move with the lease, so the information arm would be constant rather
   than a transmitter of the temporary shock.

**As run.** A **mid-transition starting state** (stipulated, identical in all arms) is used:
`seat0 = (108, 100, 12)` — near-universal primary and lower-secondary with an elite upper-secondary tier —
cohort 1 arrives with 12 students already at upper-secondary entry, 88 at primary completion and 20 with no
credential, and inherited labour-market stocks `readers = 0.758`, `formal_share = 0.40`,
`skill_stock = 0.35`. The endogenous construction rule is switched **off** (`investment_fixed = 0`) so that
the temporary lease is the only capacity variation in the window.

The **information regime** is an adaptive belief about upper-secondary opportunity (in units of the reference
flow of 12 credentialed places), as defined in §6.1. The lease raises the observed credentialed flow from 12
to 24 in cohorts 2–4, the belief rises with 0.70 persistence, and it decays after the seats are removed.
This is the stipulated channel by which a temporary expansion can leave a trace on cohort-5–7 applications.

| arm | lease cohorts 2–4 | upper fee | expectation regime | employer |
|---|---|---|---|---|
| `control_{fixed,responsive}` | none | baseline | static (multiplier 1.0) | frozen 40 posts / responsive |
| `supply_only_{fixed,responsive}` | 12 seats | baseline | static | frozen / responsive |
| `fee_waiver_{fixed,responsive}` | 12 seats | 0.0 in cohorts 2–4 | static | frozen / responsive |
| `placement_info_{fixed,responsive}` | 12 seats | baseline | adaptive belief (§6.1) | frozen / responsive |

The lease is added at the start of cohort 2 and removed at the start of cohort 5 (one +12 and one −12
injection), so cohorts 2–4 see 24 upper-secondary seats and cohorts 5+ see 12. Windows are as declared:
`PRE = {1}`, `DURING = {2,3,4}`, `POST = {5,6,7}`, `DECAY = {16..20}`.

Thresholds P12-1a/b, P12-2a/b, P12-3 and the falsifier are **unchanged**. Two definitional facts are
recorded here so they are not read as results: under frozen posts the total hire count is 40 by construction
(posts are always filled), so "hires flat" under frozen jobs is definitional; the informative hire measure
under frozen posts is the composition (`grad_hires`), which is reported.

### 6.5 Freeze

After this amendment the file is hashed again; the hash in `RUN_MANIFEST.json` is the one that was in place
when `RESULTS.csv` was produced.
