# ENGINE INTERFACE CONTRACT — Atlas contest audit v2, Gate 1 (v1.0)

**Owner:** `atlas-commander` (execution owner). **Status: BINDING from 2026-11-25T14:30+08:00.**
**Consumers:** `engine-core` (task-2), `engine-tutoring` (task-3), `contest-math` (task-4), `qa-verifier` (task-5),
`audit-runner` (task-1, read-only consumer of the 540 config).
**Branch:** `research/contest-audit-v2-2026-11-25`. One shared worktree — this contract exists to keep five lanes
writing disjoint files against one API. Amendments only by the Commander, recorded in §14.

Evidence taxonomy for every claim in Lane reports: **VERIFIED EMPIRICAL / REPRODUCED SIMULATION / VALIDATED
SIMULATION / AUTHOR-REPORTED / CONTRADICTED / UNRESOLVED**. Nothing in Gate 1 is VERIFIED EMPIRICAL.

---

## 0. Why this contract exists (defects it freezes the fix for)

Current behaviour, with exact anchors (`engine/eduengine/core.py` = `core`, `.../modules/tutoring.py` = `tut`):

| # | defect | anchor (pre-repair) |
|---|---|---|
| D1 | KR Grade-9 contest has no lasting consequence: `k['elite']` is set **only** when `m_ == nlev-2` (G12); the G9 gate (`kind='contest', share=0.35, fail='track', elite_logw=0.15, set_voc=False`) leaves winners and losers identical, yet `contest_prep` prices the G9 prize from `elite_logw` (phantom prize). | `core` L428–429; gate at `papers/shadow-education-contest/code/run_hk_korea_comparative.py` L115; phantom pricing `tut` L94–101 |
| D2 | Expected probability in the household problem is `P = 1−exp(−λ x^r)` with λ re-solved each year to match aggregate seats; realized admission is Gumbel-max Plackett–Luce over `x_eff`. Different objects. | expected `core` L178 (`values`), `tut` L112; realized `core` L406–426 |
| D3 | Seat denominator: `seats = max(round(share·N), 1)` is a share of the entering cohort, not of applicants; applicants/seats/admission rate are nowhere reported. | `core` L400 (contest), L433 (quota), L464 (`admit`) |
| D4 | Contest expenditure is a single `pc·e_opt` flow, booked to `extra_spend` and to `firm_rev`; there is no resource-cost / tax / household-outlay split and no government receipt ledger. | `tut` L106, L135, L137, L154 |
| D5 | Preparation effort is one flat per-child scalar `k['contest_e']` (no gate index, no depreciation); reset at every gate. | `core` L135, L427; `tut` L104, L136 |
| D6 | RNG is a single sequential `np.random.default_rng(seed)` stream consumed in path order, so exogenous draws are not matched across policy arms; persons have no immutable id. | `core` L93, L124–127, L331–332, L394, L408 |
| D7 | Elite wage premium is a single multiplicative post-labour adjustment with no decomposition into direct elite status vs selection into skilled jobs. | `core` L498–499 |
| D8 | No explicit gate kinds: `kind` anything-else falls through to `quota`; `'bar'` is a string literal in two code paths. | `core` L173/190, L395/397/441 |

Gate 1 fixes D1–D8. **No calibration, policy campaign, or GPU work in wave 1** (Gate discipline, LEAD_GROUND_TRUTH §6).

---

## 1. Gate schema (canonical, normalised at Engine construction)

`gates` remains a list of `dict`, one per level, length **must equal `nlev`** (`len(p['levels'])`).
Canonical kinds: **`open` | `fixed_bar` | `quota` | `contest`**.
`'bar'` is accepted as a **deprecated alias of `fixed_bar`** (the 540 config and all existing world/country configs
use it); normalisation rewrites it to `fixed_bar` and emits one `DeprecationWarning` per Engine.
**Unknown `kind` (including a missing `kind`) raises `ValueError(f"unknown gate kind {kind!r} at level {m}; expected one of ...")`
at Engine construction — it must fail loudly, never fall through to `quota`.**
`p['gates']` and `self.gates` hold the normalised list. Gate lists replaced at runtime through `paths`/`events`
(`core` `apply_calendar` L293–302) are re-normalised immediately after `p.update(ev['set'])`; `self.cut` /
`self.cut_adm` / `self.lam_contest` values are carried over for unchanged indices.

### 1.1 Common fields

| field | type | default | kinds | meaning |
|---|---|---|---|---|
| `kind` | str | **required** | all | `open`/`fixed_bar`/`quota`/`contest`; `'bar'`→`fixed_bar` alias |
| `fail` | str | `'stop'` | fixed_bar, quota, contest | `'track'` = failers continue on the non-elite/vocational track (legacy behaviour); anything else = exit with the credential |
| `academic_only` | bool | `False` | all | vocational-track pupils cannot sit/win |
| `admit` | dict \| None | `None` | fixed_bar, quota, contest | nested admission quota to the **next** level: `{share, cut0=0.0, academic_only=False, kind='quota'|'open'}` |
| `spec` | dict \| None | `None` | all | non-numeric provenance/metadata only: `{id, label, source, citation, note}`. Must never affect numerics; `spec` may not contain any recognised numeric field name |

### 1.2 Kind-specific fields

| field | type | default | kind | meaning |
|---|---|---|---|---|
| `bar` | float | **required** | `fixed_bar` | pass threshold in grade-equivalents (name kept for 540 compat; `'bar'`→`fixed_bar` alias keeps the field) |
| `share` | float | **required** | `quota`, `contest` | seat share; **denominator governed by `share_of`** |
| `share_of` | str | `'cohort'` | `quota`, `contest` | `'cohort'` (legacy: `seats=max(round(share·N),1)`) or `'applicants'` (`seats=max(round(share··),1) where · = candidates`) — finding D3 fix: both are legal, the choice is pre-declared per arm and reported |
| `cut0` | float | `0.0` | `quota` | initial believed cutoff (legacy `g.get('cut0', 0.0)`) |
| `set_voc` | bool | `True` | `contest` | losers with `fail='track'` are sent to the vocational track. Forbidden if `track_consequence=True` |
| `elite_logw` | float \| None | `None` | `contest` | log-wage prize for winning. `None` → inherit `p['elite_logw']`. Forbidden together with `track_consequence=True` (no phantom prizes) |
| `r` | float \| None | `None` | `contest` | contest discrimination exponent; `None` → `p['contest_r']` |
| `alpha` | float \| None | `None` | `contest` | effectiveness of contest effort; `None` → `p['contest_alpha']` |
| `x0` | float \| None | `None` | `contest` | baseline contest input; `None` → `p['contest_x0']` |
| `track_consequence` | bool | `False` | `contest` | **D1.** `True` = this gate places the child on a persistent track; requires `fail='track'`, forbids `elite_logw`/`set_voc`, requires `track_prize` |
| `track_prize` | dict | **required iff `track_consequence`** | `contest` | persistent-consequence rewards, see §3 |
| `track_bonus` | float | `1.0` | `contest` | multiplier on a **track=1** child's contest weight at this (later) gate; implements "G12 admission probability" channel of the G9 consequence |

**Validation (constructor-time, `ValueError` on violation):**
1. `kind` present and ∈ canonical kinds after alias mapping.
2. `fixed_bar` requires numeric `bar`; `quota`/`contest` require numeric `share`; `share`∈(0,1];
   `quota`/`contest` with `share_of='applicants'` is allowed but must be declared in the arm label.
3. `track_consequence` requires `kind='contest'`, `fail='track'`, and exactly the keys
   `{quality_mult, earnings_logw, g12_track_bonus}` in `track_prize` (all floats; at least one non-neutral).
4. `track_consequence` forbids `elite_logw` and `set_voc` (raise: `"a tracking gate may not pay a direct elite_logw;
   use track_prize"`). This makes the G9 phantom prize structurally impossible.
5. At most one gate in the list may have `track_consequence=True`.
6. `open` gates may not carry `share`, `bar`, `elite_logw`, `track_prize`.

### 1.3 Expected / realized probability objects (D2)

For a contest gate `m`, candidates are `att & cred<=m & (~voc if academic_only)`. Define

```
x_eff(i,m) = max( x0 · max(L_i, 0.1)/ends[m] + alpha · prep_stock[i,m] , 1e-6 )
w_i        = x_eff(i,m) ** r
if k['track'][i] == 1 and gate['track_bonus'] != 1.0:  w_i *= gate['track_bonus']
seats      = max(round(share · denominator), 1)          # denominator per share_of
seats_eff  = min(seats, n_candidates)
```

* **Expected** win probability = `pl_win_probs(w, seats_eff, method=p['contest_prob_method'], ...)`
  — **the one and only expected-probability function**. Used by `values()` (household valuation) *and* by tutoring's
  effort choice *and* reported in the annual series. `P_i = 1` for all candidates iff `n_candidates <= seats`.
  Hard invariant: `Σ_i P_i = seats_eff` (abs tol `1e-9`), `0 <= P_i <= 1`.
* **Realized** admission = `pl_realize(w, seats_eff, u)` where `u` is a caller-supplied U(0,1) vector of length
  `n_candidates` drawn from the **event-keyed** stream `(seed, replicate, year, shock_type=f'contest_pl_{m}', pid)`
  (§7). No other RNG may enter the realized draw. `u` is clamped to `[1e-12, 1-1e-12]` inside the module.
* If `n_candidates == 0` the gate is a no-op (record 0 candidates/0 admitted; no draw).
* The old `1-exp(-λ x^r)` / λ-re-solve code path is **removed from `values()` and the gate**, not kept as a fallback.
  `λ` re-solving at `core` L416–426 is deleted. `p['lam_contest']`/`self.lam_contest` may remain as initialised state
  for backward import compatibility but may not feed any probability after repair.
* **Determinism (binding):** `method='auto'` and `method='exact'` must be **pure deterministic functions of
  `(weights, seats)`**. No unseeded RNG, no Monte-Carlo noise, no dependence on `rng`/`n_mc` on the `auto`/`exact`
  paths. `method='auto'` may use the exact subset DP for small `n` and a **documented deterministic algorithm**
  (e.g. exponential-race/Poisson-binomial quadrature) for large `n`; it must expose the method used via a companion
  `pl_win_probs_detail(...) -> (p, info)` (info: method, n, seats, estimated max error, runtime). Seat-sum accuracy on
  `auto`: `|ΣP − seats_eff| ≤ 1e-6` (the engine enforces it explicitly, see below). Accuracy on `auto` for n=300,
  seats=36, log-weight dispersion 0–6: max |P−P_mc| ≤ `0.01` and mean |P−P_mc| ≤ `0.002` (MC reference `n_mc≥400k`,
  SE≤2e-3).
* `method='exact'`: exact to machine precision for `n <= 12`; may support a larger documented cap (contest-math draft:
  20, O(n·2^n)); it must **raise `ValueError` beyond its documented cap** rather than silently approximate.
* `method='mc'` is validation-only (never the engine decision path). It uses a caller-supplied seeded generator and
  returns `(p, se)`. `rng`/`n_mc` are ignored on the `auto`/`exact` paths.
* Performance target (host): `method='auto'`, n=300 candidates, seats=36, one call **≤ 50 ms**; if a gate-year needs
  more, the engine may cache per `(year, m)` weights and recompute only for the children whose own stock is varied
  (see §6 `contest_weights` override); the lane must report measured runtime.
* Engine post-processing: `E.contest_expected_probs` rescales `P ← P · seats_eff / ΣP` when `ΣP` deviates from
  `seats_eff` by ≤`1e-3` (documented correction, makes the seat-sum invariant exact), and **raises** if the deviation
  is larger (signals a broken probability module).

### 1.4 Gate diagnostics (D3 fix — reporting, additive series)

Every year, for every contest gate `m`, core records through `E.note`, as **list-of-nlev** series (non-contest
indices are `NaN`):

| series key | definition |
|---|---|
| `contest_candidates` | `n_candidates` |
| `contest_seats` | `seats` (pre-cap; for `share_of='applicants'`, computed on candidates) |
| `contest_expected_seats` | `Σ_i P_i` |
| `contest_admitted` | `Σ_i realized` |
| `contest_applicant_seat_ratio` | `n_candidates / max(seats,1)` |
| `contest_admit_rate` | `admitted / max(n_candidates,1)` |
| `contest_expected_p_mean` | `mean_i P_i` over candidates |
| `contest_expected_p_by_q` | list of 5 means of `P_i` over qualifying candidates by `k['q']` |
| `contest_realized_by_q` | list of 5 admission rates over candidates by `k['q']` |
| `contest_prep_stock_mean_by_q` | list of 5 means of `prep_stock[i,m]` over candidates by `k['q']` |

`Engine.run()` merges `self.contest_summary()` into the returned dict (additive keys only):
`contest_seats_by_gate`, `contest_candidates_by_gate`, `contest_applicant_seat_ratio_by_gate`,
`contest_admit_rate_by_gate`, `contest_expected_seats_by_gate`, `contest_expected_vs_realized_gap`
(= mean over years/gates of `|admit_rate − expected_p_mean|`, diagnostic only, not a fit statistic).

---

## 2. Persistent state additions (D1/D5/D6)

`core.add_cohort` allocates the following keys with the rest of the child dict (`core` L128–135, new dict).
All are sliced automatically by the existing exit compaction (`core` L510–511); **core owns allocation and removal**,
modules never add or remove keys.

| key | dtype/shape | init | semantics |
|---|---|---|---|
| `k['pid']` | int64 `(N,)` | `t*N + np.arange(N)` at cohort creation | **immutable** person id. Never renumbered, never mutated by any module. Used only for event-keyed RNG and cross-arm matching. `N` must be the same across arms to match persons across arms; record `pid` mapping in metadata. |
| `k['track']` | int8 `(N,)` | `-1` | track placement: `-1` = not yet placed, `0` = non-elite/vocational track, `1` = elite track. Set only by a `track_consequence` gate (winners→1, losers→0). Sticky: never re-set by a later gate; at most one tracking gate exists per list. |
| `k['elite']` | bool `(N,)` | `False` | won a **non-tracking** contest gate with effective `elite_logw>0`. May be set at **any** level (fixes D1's `m_==nlev-2` restriction; for the canonical KR/HK specs it is still only the G12 gate that pays `elite_logw`). |
| `k['elite_prize']` | float64 `(N,)` | `0.0` | effective log-wage prize won: `max(existing, effective_elite_logw)` at win time (`None`→`p['elite_logw']`). Labour applies `inc *= exp(k['elite_prize'])`. This replaces the global-only application at `core` L498–499 and preserves legacy values (`elite_prize == p['elite_logw']` exactly, gate omitted). |
| `k['prep_stock']` | float64 `(N, nlev)` | `0.0` | per-gate preparation stock; column `m` is stock accumulated toward the gate at the end of level `m`. See §5. |

Anything else a lane believes it needs must be a **derived per-year value** in `E.yr` (no new persistent child keys).

---

## 3. Named gate specs: KR-SINGLE vs KR-TRACKED (D1)

Wave 1 must make both configs available **as data** (no fitting/calibration in wave 1). Engine-core adds a module-level
dict to `engine/eduengine/core.py`:

```python
GATE_SPECS = {
    'KR-SINGLE':  [ ...4 gates... ],
    'KR-TRACKED': [ ...4 gates... ],
}
```
Runners copy/deepcopy one entry into `gates=`. The two specs differ only at level index 1 (Grade 9):

| | KR-SINGLE | KR-TRACKED |
|---|---|---|
| G9 (index 1, ends at grade 9) | `dict(kind='open', spec=dict(id='KR-G9-open', label='regular grade-9 transition'))` — no selection, no prize | `dict(kind='contest', share=0.35, fail='track', track_consequence=True, track_prize=dict(quality_mult=1.10, earnings_logw=0.15, g12_track_bonus=1.25), spec=dict(id='KR-G9-track', label='selective grade-9 placement'))` |
| G12 (index 2, ends at grade 12) | `dict(kind='contest', share=0.12, fail='track', spec=dict(id='KR-G12'))` | same, plus `track_bonus=1.25` |
| levels 0/3 | unchanged from the 540 config: `dict(kind='fixed_bar', bar=2.0)` / `dict(kind='fixed_bar', bar=10.0)` | same |

**Pre-registration statement (must appear verbatim in the lane report and CODE_CHANGES.md):** the three
`track_prize` magnitudes are **pre-registered structural placeholders, not estimates**. `earnings_logw=0.15` reuses
the old phantom G9 `elite_logw` value so the repair converts an unpriced prize into a delivered one; `quality_mult`
and `g12_track_bonus` are pre-registered placeholders whose sensitivity is a wave-2 task (grid recorded but not run in
wave 1). No empirical claim attaches to them. Global `elite_logw` stays 0.60 (KR) / 0.50 (HK) for the G12 prize.

**Semantics that must hold identically in `values()` and in the realized path:**
1. `track=1` children have effective learning quality multiplied by `quality_mult` in later years (learning line,
   `core` L363) — **realized**; and the value function must project the same multiplier for later years.
2. At a later contest gate with `track_bonus != 1.0`, a `track=1` candidate's weight `w` is multiplied by
   `track_bonus` — **realized**; value function must use the same weight.
3. `track=1` leavers earn `exp(earnings_logw)` more (`inc *= exp(track_prize['earnings_logw'])`), applied in the
   labour step *before* the elite prize multiplier; the value function's income beliefs must include it (prior/observed
   wage for the child's credential must be track-conditional in `values()`).
4. **Expected prize = actual transition continuation value (binding):** tutoring must obtain the prize for gate `m`
   from `E.gate_prize_dv(m, idx)` (§6), which core computes *from the same `values()` recursion* as
   `V(track=1 continuation) − V(track=0 continuation)` (for tracking gates) or `kappa · effective_elite_logw`
   (for non-tracking elite gates). Tutoring may not read `elite_logw`/`track_prize` directly for pricing.
5. `track_prize=None`/absent on a non-tracking gate means no track effect. KR-SINGLE's open G9 has no place to store
   track state; `k['track']` stays `-1` for all its children, and the G12 gate and labour must behave exactly as the
   no-track baseline (no `track`-dependent modifiers fire when `track == -1`).

---

## 4. Tutoring → core accounting contract (D4)

### 4.1 Units and identities

`contest_price` (`CORE_DEFAULTS`, `core` L54) is the **pre-tax resource price** of one unit of contest-prep effort
(wage units per unit `e`). New tutoring default `contest_tax_rate` = `0.0`; the household's unit outlay is
`contest_price · (1 + contest_tax_rate)`.

Per year `t`, per child `i` (arrays length `N`, all `.sum()`-reconcilable):

| `E.yr` array | definition | invariant |
|---|---|---|
| `res_cost[i]` | `contest_price · e_t[i]` — physical tutoring resource cost (teacher time, materials) | `>= 0` |
| `tut_tax[i]` | `contest_tax_rate · res_cost[i]` — tax paid by household | `>= 0` |
| `tut_outlay[i]` | `res_cost[i] + tut_tax[i]` — **household outlay**, the amount that enters the cash budget and `extra_spend` | `tut_outlay == res_cost + tut_tax` (exact identity) |
| `gov_tut_tax[i]` | `tut_tax[i]` attributed to the paying household (so per-quintile receipt is possible) | `Σ gov_tut_tax == Σ tut_tax` |

Financial identities that must hold exactly (tolerance `1e-12` relative):
1. `tut_outlay == res_cost + tut_tax`
2. `Σ gov_tut_tax == Σ tut_tax` (government receipts)
3. `extra_spend == legacy tutoring outlays + tut_outlay` (i.e. contest outlay is booked **once**)
4. no rebate unless `contest_rebate_policy != 'none'`; if a rebate is active it is credited explicitly to households
   and recorded in `E.yr['rebate']` with total `Σ rebate` and recipient count (`gov_tut_tax` is NOT reduced; the
   rebate is a separate transfer line). Default `contest_rebate_policy='none'`.

### 4.2 Cash budget rule (binding)

Annual cap and cash both bind the **outlay**, not the resource cost:

```
cash_rem  = max(E._cash[idx] - pre_contest_extra_spend[idx], 0)
e_cap     = contest_max_e
e_hi      = min(e_cap, cash_rem / (contest_price * (1 + contest_tax_rate)))
assert 0 <= e_opt <= e_hi + 1e-12          # must be asserted in code, not assumed
```

`E._cash` is core's residual liquidity after the schooling decision (`core` L354); tutoring must not raise it.
`pre_contest_extra_spend` is the own-teacher + firm spending already booked this year (`tut` L71). Contest
preparation may not push a household's total yearly tutoring outlay above `E._cash`; a per-child assertion is
required. The annual cap binds `e_t` every year (not the stock).

### 4.3 Reporting keys (backward compatible; additive only)

`contest_spend_now` (new annual series, **household outlay** of contest prep, i.e. `Σ tut_outlay`) — this is the
backward-compatible quantity the 540-era naming implies. Additional series (additive, same names in `E.R` and in
`TutoringMarket.summary()`):

| series | definition |
|---|---|
| `contest_resource_cost` | `Σ res_cost` |
| `contest_tax_paid` | `Σ tut_tax` |
| `gov_tut_receipt` | `Σ gov_tut_tax` |
| `contest_outlay_by_q` | 5 means of `tut_outlay` over K-12 pupils by `k['q']` |
| `contest_res_cost_by_q` | 5 means of `res_cost` by quintile |
| `contest_tax_by_q` | 5 means of `tut_tax` by quintile |
| `contest_effort_by_q` | 5 means of `e_t` over assigned pupils by quintile |
| `contest_prep_stock_mean` | mean `prep_stock[:,m]` over candidates for each contest gate (list) |

**`firm_rev` semantics change (required, D4 double-count fix):** commercial-tutoring revenue must count
`contest_resource_cost`, **not** `contest_spend_now`/outlay; the tax is a government receipt, not firm revenue.
With `contest_tax_rate == 0` this is numerically identical to the legacy `tut` L154 expression. Tutoring lane updates
`tut` L154; no other consumer of `firm_rev` changes (`modules/labour.py` L105–108 reads it for tutor jobs).

Existing series **must keep their names and meaning**: `tut_k12_spend`, `tut_k12_rate`, `tut_g12_rate`,
`tut_k12_rate_by_q`, `tut_k12_spend_by_q`, `tut_spend`, `tut_rate`, `tut_by_grade`, `tut_by_q`, `contest_e_mean`,
`firm_rev`, `own_share`. `tut_k12_spend*`, `tut_spend`, `hs_spend` remain **household outlays** (gross), so they
include `tut_outlay` exactly once. `contest_e_mean` remains the mean **current-year** effort `e_t` over K-12 pupils.

---

## 5. Preparation stock and effort-cap semantics (D5; resolves the rho contradiction)

**Binding convention (amendment to task-3 wording, recorded in §14):** `prep_depreciation` (called `rho` in the
brief) is a **DEPRECIATION RATE**; higher `rho` = more memory loss:

```
prep_stock[i, m] ← (1 - rho) * prep_stock[i, m]            # every year, for every attending child, every gate m
prep_stock[i, m_gate] += e_t[i]                             # + this year's effort toward the child's assigned gate
```

with `m_gate` = the nearest upcoming contest gate for that child (the legacy assignment rule, `tut` L86–89).
Gate-time effective input uses the **stock at the gate year**, i.e. this year's effort included:

```
x_eff(i,m) = max( x0 · max(L_i,0.1)/ends[m] + alpha · prep_stock[i,m], 1e-6 )
```
and after the gate draw core sets `prep_stock[at_gate, m] = 0` for **all** children sitting gate `m` (consumed),
keeping other columns untouched.

**Why this is the legacy anchor:** the pre-repair code accumulates `k['contest_e'] += e_t` every year and resets only
at the gate (`core` L135/L427, `tut` L136) — an **undepreciated lifetime sum**, which under the recurrence above is
`rho = 0`. Task-3's acceptance line "rho=0 reproduces old behaviour" is correct **only** with the depreciation
convention (it is inconsistent with the literal recurrence `stock_{t+1}=rho·stock+e`; the acceptance line wins).
So:
* `contest_prep_depreciation` default **`0.0`** = legacy semantics, frozen for backward compatibility.
* Sensitivity grid (declared now, run in wave 2): `{0.0, 0.25, 0.5, 0.75, 1.0}`; `1.0` = memoryless (current-year
  effort only).
* `prep_stock` is per-gate, so effort spent toward G9 is consumed at G9 and never helps G12. This reproduces the
  legacy reset semantics for the canonical two-contest-gate specs.
* `k['contest_e']` is retained **only** as the `(N,)` current-year effort flow `e_t` for reporting/legacy
  (`contest_e_mean`); it is assigned (not accumulated) each year and is not read by any probability or gate path.

**Optional learning effect (switch, default off):** if `contest_prep_learning_gain > 0`, contest prep also adds
`contest_prep_learning_gain · e_t` grade-equivalents to `dL` (learning line), i.e. exam-prep is treated as skills
rather than pure position. `contest_prep_mode ∈ {'positional','learning','both'}`, default `'positional'`; with
`'learning'`/`'both'` the positional weight in the gate is scaled by `contest_prep_positional_share` (default 1.0 for
`'both'`, 0.0 for `'learning'`). Default configuration = pure positional, legacy numerics unchanged.

**Tutoring objective (unchanged shape):** choose `e_t ∈ [0, e_hi]` to maximize
`E.gate_prize_dv(m, ·) · P(x_eff(e)) − contest_price·(1+tax)·e` where `P` is the **§1.3 expected probability**
(the same function as `values()`), sampled on an explicit grid + local refinement. The lane must report the number of
probability evaluations per gate-year and the max grid/refinement error; if the accurate `P` makes the 25-point grid
too slow, reduce the grid to **≥ 9 points plus a documented local search** and record the bounding error — never
silently substitute the old `1-exp` formula.

---

## 6. Core API surface that other lanes may rely on (frozen names)

`engine-core` implements these on `Engine` (all are read-only for tutoring/QA):

| method | returns | contract |
|---|---|---|
| `E.gates` | list[dict] | normalised gates (§1) |
| `E.gate_kind(m)` | str | canonical kind |
| `E.contest_gates` | list[(m, gate)] | gates with `kind='contest'` |
| `E.contest_candidates(m)` | bool mask `(N,)` | **amendment A7 (2026-11-25): the same-year *sitting cohort*** — pre-promotion `cred==m & g==ends[m]-1` (fallback `cred==m` if that is empty), `academic_only` respected, and (if `track_consequence`) `track==-1`; NOT the literal `cred<=m` pool, which spans year groups and would re-introduce D2. Used by `values()`, tutoring and the realised gate, so expected and realised probabilities are the same object. |
| `E.contest_seats(m)` | int | `max(round(share·denominator),1)` per `share_of`, candidates not yet capped |
| `E.contest_weights(m, idx=None)` | `(pids, w)` | `w` per §1.3 using current `prep_stock`; `idx` restricts the returned order; weight definition is owned by core, tutoring must not re-derive it. Optional keyword `stock_override` (array-like aligned with `idx`) replaces those children's stock for a counterfactual probability call — this is how tutoring evaluates `P(x_eff(e))` without a cross-call cache; the override never mutates state. |
| `E.contest_expected_probs(m, idx=None)` | `(idx_or_pids, P)` | `pl_win_probs` on `E.contest_weights(m)` over the full candidate set, subset-selected; `ΣP = min(seats, n_cand)` |
| `E.gate_prize_dv(m, idx=None)` | `(idx_or_pids, dV)` | utility value of passing gate `m`, from `values()`; for tracking gates = `V(track=1)−V(track=0)`; for elite gates = `kappa·elite_logw`. **This is the only prize tutoring may price.** |
| `E.values(t, L=None, idx=None, track_state=None)` | `(V_stop, V_cont)` | extended signature; `track_state` (scalar/array) overrides `k['track']` for counterfactual evaluation; default `None` |
| `E.contest_summary()` | dict | §1.4 summary keys |
| `E.rng` | `EventRNG` | §7; keeps numpy-Generator-compatible methods for non-migrated callers |

`pl_win_probs`/`pl_realize` live in `engine/eduengine/contest_math.py`; `core.py` **imports** them. No re-implementation
of PL anywhere else (a grep for `gumbel`/`argsort(-` in core/tutoring after repair must show no private PL code).

**Residual risk recorded for the Gate-1 report (expected-P for *future* gates).** For a child valued at a gate it
has not reached yet, `_gate_expected_P` evaluates PL once on the current same-year sitting cohort and maps the
child's projected weight through that pool's probability curve (monotone interpolation), because the future
cohort's weight distribution is unknown. This is a documented approximation: it is exact for pool members, and
for future-gate valuations it is the official-pool-map approximation. It is reported, not hidden (engine-core
`ENGINE_CORE_AUDIT.md` §B12).

---

## 7. `engine/eduengine/rng.py` — event-keyed streams (D6)

**Goal:** exogenous characteristics/shocks matched across policy arms for the same person; same config+seed
deterministic; vectorizable over pid arrays; subset- and order-independent.

```python
# API (binding)
class EventRNG:
    def __init__(self, seed: int, replicate: int = 0): ...
    # key = (seed, replicate, year, shock_type, pid); value is a pure function of the key
    def uniform(self, year, shock_type, pid)        -> np.ndarray   # shape == np.shape(pid)
    def normal(self, year, shock_type, pid)         -> np.ndarray   # N(0,1), Box–Muller from two keyed uniforms
    def logistic(self, year, shock_type, pid)       -> np.ndarray
    def gumbel(self, year, shock_type, pid)         -> np.ndarray   # standard Gumbel (for pl_realize u only if needed)
    def permutation_like(self, year, shock_type, pid) -> np.ndarray # per-pid U; caller argsorts; replaces r.permutation
    # --- legacy compatibility only (non-migrated callers in wave 1) ---
    def random(self, size=None) -> np.ndarray        # internal default_rng stream (legacy, path-dependent)
    def standard_normal(self, size=None) -> np.ndarray
    def logistic(self, size=None) -> np.ndarray      # NOTE: legacy size-based call is `legacy_logistic`
    def permutation(self, n) -> np.ndarray
    def choice(self, a, size=None, replace=True) -> np.ndarray
```

To avoid the `logistic` name clash the contract fixes **two explicit names**: event API `E.rng.logistic(year, shock, pid)`
and legacy API `E.rng.legacy_logistic(size)`; all event methods are positional as above. Implementation is
hash-based (splitmix64 over a 128-bit mix of `seed, replicate, year, shock_type_id, pid, tap`) so a pid's draw does not
depend on which other pids are requested or their order; `shock_type` is mapped to a stable int via a module-level
`SHOCK_TYPES: dict[str,int]` registry (new shock types appended, never renumbered).

**Rules**
1. `k['pid']` immutable; engine-core migrates **all core.py and labour.py** exogenous draws to event streams:
   `cohort_z, cohort_urban, cohort_home, cohort_ability` (year = cohort year), `continuation`, `income_shock`,
   `gate_exam_{m}`, `promote`, `contest_pl_{m}`, `anchor`, `street`, `queue_accept`, `labour_signal`,
   `labour_lottery` (per-pid U replaces `r.permutation`).
2. `Engine.rng` remains an `EventRNG` instance (same attribute name) so unmigrated modules (`schools.py`,
   `tutoring.py`, `anchor.py`) keep working through the legacy methods; their draws are **known residual
   path-dependence in wave 1**, recorded in CODE_CHANGES.md and in the Gate-1 report. Tutoring lane MAY migrate its
   own three draws (`tut_own_ok`, `tut_firm_ok`, `tut_taste`) to event streams at its discretion (its file, its scope).
3. `replicate = p['seed']`. Runner must pass distinct seeds across replicates; EventRNG must not combine with the
   legacy stream (no shared state).
4. Test: two Engines with the same params/seed produce identical `k['pid']`, identical cohort covariates, identical
   gate exam noise; an arm differing only in a policy parameter sees identical cohort covariates for every pid.

---

## 8. Labour premium audit (D7)

`modules/labour.py` (engine-core scope) applies prizes without changing wage structure:
1. After the labour module returns `inc`, apply `inc *= exp(k['elite_prize'])` **and** `inc *= exp(track_prize['earnings_logw'])`
   for `track==1` leavers whose tracking gate exists. Both are multiplicative and applied last.
2. **Wage-compression invariance:** varying only `elite_logw`/`track_prize['earnings_logw']` must leave every other wage
   relationship unchanged — `w_skilled`, `w_routine`, `w_informal`, `theta_L`, `theta_L_inf`, `floor0`, and the
   conditional income distribution by credential must be bit-identical at `elite_logw=0` vs the same run with the
   premium applied. Test: `elite_logw=0` ⇒ mean log income by credential identical to a run with `elite_prize≡0`.
3. Required audit series (`E.note`): `elite_share` (share of leavers with `k['elite']`), `elite_prize_mean`,
   `track_share`, `track_prize_mean`, `elite_inc_gap_raw` (mean income elite − non-elite), and a decomposition series
   `elite_inc_gap_direct` (= raw gap minus the gap implied by the multiplier, i.e. `mean((exp(prize)−1)·inc_base)`),
   `elite_inc_gap_composition` (residual = selection/skilled-job route). Report all three per arm; do not claim a
   "direct elite effect" from the raw gap.

---

## 9. Backward-compatibility rules (binding)

1. **Constructor unchanged:** `Engine(modules, **params)`; unknown params still raise `KeyError` at construction;
   `eduengine.build()` still filters module params. New knobs must be declared in `CORE_DEFAULTS` (engine-core) or
   `TutoringMarket.defaults` (engine-tutoring) — see §10 for ownership, no duplicate names.
2. **Legacy configs run:** `engine/worlds.py`, `engine/experiments.py`, `engine/checks.py` and `engine/countries/*`
   must construct and run after repair (existing gates use `kind='bar'|'quota'`; alias covers them). A smoke test
   (`python -c` building each world + one year) is part of acceptance.
3. **540 runner unmodified must run** against the repaired engine: it reads only
   `E.R[tut_k12_spend, tut_g12_rate, tut_k12_rate, tut_k12_rate_by_q, tut_k12_spend_by_q, contest_e_mean]` and
   `E.ALL[elite,q,cohort,g]` — all retained. It must not raise. Numerics are allowed to change (canonical spec is
   **not frozen**: DASHBOARD open decision 1), but the change must be **documented** with a small migration table
   (e.g. 1 arm × 3 seeds old-vs-new, listing which repair causes what), and the pristine-tree 540 output stays the
   Gate-0 reproduced artifact.
4. **Series keys are additive-only.** No existing `E.R` key, `summary()` key, or runner-read seed-row key may be
   renamed, removed, or given a new meaning (except the explicitly documented `firm_rev` resource-cost correction from
   §4.3, numerically identical at `tax=0`).
5. **Default configuration = legacy numerics where a feature is off:** `contest_tax_rate=0`, `contest_prep_mode='positional'`,
   `contest_prep_depreciation=0`, no tracking gates, no `elite_logw` change ⇒ probabilities may change only because of
   D2's honest expected probability (PL) and D6's RNG keying; both differences must be quantified in CODE_CHANGES.md.
6. **No new required arguments** on public functions/classes; no changes to `modules` dict keys or `Module` hook
   signatures. `Module.setup/supply/sector/extras/labour/after/measure/summary` signatures unchanged.

---

## 10. File ownership / write scopes (no lane may cross)

| lane | exclusive write scope | may read |
|---|---|---|
| audit-runner | `docs/audit/{GATE0_REPORT.md,system_*.txt,ARTIFACT_REGISTRY.csv,ARCHIVE_BRANCH_INVENTORY.csv}`, `results/audit/**`, throwaway in `wt4/repro` | everything; never edits `wt4/repro` engine |
| engine-core | `engine/eduengine/core.py`, `engine/eduengine/rng.py` (new), `engine/eduengine/planning.py`, `engine/eduengine/modules/labour.py`, `docs/audit/ENGINE_*.md` | `tutoring.py` (read), `contest_math.py` (import) |
| engine-tutoring | `engine/eduengine/modules/tutoring.py`, `docs/audit/TUTORING_*.md`, `docs/audit/TUTORING_CHECKS.py` | `core.py`, `contest_math.py` |
| contest-math | `engine/eduengine/contest_math.py` (new), `tests/test_contest_math.py`, `docs/audit/CONTEST_MATH_*.md` | `core.py` |
| qa-verifier | `tests/**` except `tests/test_contest_math.py`, `docs/audit/FIRST_FAILURE_REPORT.md`, `docs/audit/TEST_REPORT*.md`, `results/audit/**` | everything, read-only on `engine/` |
| commander | `docs/audit/{ENGINE_INTERFACE_CONTRACT,DASHBOARD,CODE_CHANGES,TEST_REPORT,GATE0_VERIFICATION}.md` | everything |

**Parameter ownership dictionary (no duplicate names):**
* `CORE_DEFAULTS` (engine-core) keeps/owns `contest_r, contest_alpha, contest_price, contest_x0, contest_max_e,
  elite_logw` and adds only `contest_prob_method='auto'`, `contest_prob_mc=20000`, `contest_prob_seed_offset=0`.
   `elite_logw` remains the global default G12 prize.
* `TutoringMarket.defaults` (engine-tutoring) adds only `contest_tax_rate=0.0`, `contest_prep_depreciation=0.0`,
  `contest_prep_mode='positional'`, `contest_prep_learning_gain=0.0`, `contest_prep_positional_share=1.0`,
  `contest_rebate_policy='none'`, `contest_rebate_rate=0.0`.
* Gate `track_prize` numbers are data (`GATE_SPECS`), not params.

---

## 11. Acceptance: the 12 invariant tests map onto this contract (qa-verifier)

Tests are written **test-first against the pre-repair tree**, then re-run after repairs. Definitions are contractual so
a failure is unambiguous:

| # | test | pass definition after repair |
|---|---|---|
| 1 | zero elite prize ⇒ zero positional effort | with every contest gate `elite_logw=0`/`track_prize` neutral and `contest_price>0`, `Σ e_t = 0` (tol 1e-12) for all years |
| 2 | zero effectiveness ⇒ effort cannot raise admission | `contest_alpha=0` ⇒ `e_t=0` and admission independent of effort (same seed, two effort levels ⇒ identical admissions) |
| 3 | universal seat ⇒ no positional marginal return | `share_of='applicants'`, `share=1.0` (or seats≥candidates) ⇒ `P_i=1`, `e_t=0` |
| 4 | seats=1, weights 4:1 ⇒ 0.8/0.2 exact | `pl_win_probs([4,1],1,method='exact') == [0.8,0.2]` (1e-12) |
| 5 | monotonicity in own effective input | `pl_win_probs` is non-decreasing in own weight (grid), and engine admission probability is non-decreasing in `e_t` holding others fixed |
| 6 | no over-allocation / no ineligible admission | `contest_admitted <= contest_seats_eff`; admitted ⊆ candidates (`academic_only` respected); `Σ expected = seats_eff` |
| 7 | non-selective gate creates no elite prize | `open`/non-tracking gate ⇒ `k['elite']` never set, `elite_prize==0`, no premium in `inc`; declared `elite_logw` cannot exist on non-track gates that pay nothing |
| 8 | G9 track persists | KR-TRACKED: winners `track=1`, losers `track=0` after G9, state unchanged at exit; quality/G12/earnings channels fire; KR-SINGLE: `track==-1` everywhere, identical to no-track baseline |
| 9 | annual expenditure respects available funds | for every child-year: `schooling need + own/firm spend + tut_outlay <= E._cash + 1e-9` and contest outlay ≤ `e_hi·price·(1+tax)` |
| 10 | gross outlay == resource + tax | per child-year and per year aggregate identity (tol 1e-12); `Σgov_tut_tax == Σtut_tax` |
| 11 | zero effort reproduces no-contest behaviour | `contest_price=0` and prizes zero (or cap 0) ⇒ admissions equal an otherwise identical engine with the gate kind forced `open` under the same seed/event streams |
| 12 | parallel/deterministic stability | same config+seed run twice and under `ProcessPoolExecutor.map(chunksize=1..4)` with shuffled task order ⇒ bit-identical seed rows |

Plus the additional tests from the Directive: tax revenue identity, per-quintile accounting reconciliation, cohort
denominators (seats/applicants/admit rate non-NaN for contest arms), expected-vs-realized reconciliation
(`|admit_rate − mean P|` within 4 seed-SE over 30 seeds for a runnable small config).

---

## 12. Minimal test fixture contract (so tests are fast and deterministic)

`tests/conftest.py` (qa-verifier scope) provides:
* `build_engine(**overrides)` → `Engine` with modules `[PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()]`,
  `N<=120, T<=24, measure_from<=10`, small seeds, `warnings` not filtered;
* `small_contest_engine(gate_extra=None, **params)` → one primary fixed_bar gate at level 0, a single contest gate at
  level 1 (the last paid gate at `nlev-2`) and open elsewhere, so prize/gate tests are isolated from G12-style logic;
* helper to read a yearly series as `np.array` and to build a 2-seed run.
Tests may import `eduengine.contest_math` only through the module API; they may not depend on private core attributes
beyond `E.gates`, `E.R`, `E.kids`, `E.ALL`, `E.yr` and the methods in §6.

---

## 13. Sequencing (Commander-enforced)

1. Commander publishes this contract + messages lanes. **engine-core and engine-tutoring: proceed.**
2. contest-math lands `contest_math.py` (needed by both engine lanes' imports) — **highest priority**; engine-core may
   code against the frozen API meanwhile.
3. engine-tutoring Phase B (accounting + prep stock + switches) after contract, using §6 API; if core methods not yet
   present, implement against this contract and integrate immediately when core lands.
4. engine-core Phase B (gate kinds, state, PL in values/realization, track consequences, prize dv, event RNG).
5. qa-verifier re-runs tests after each lane reports; FIRST_FAILURE_REPORT updated before/after.
6. Commander re-runs 540 comparison independently (temp copy of pristine tree), runs pytest, writes
   CODE_CHANGES/TEST_REPORT/GATE0_VERIFICATION, commits, reports Gate 0+1 to Lead. **Wave 2 waits for Lead sign-off.**

---

## 14. Amendment log (Commander only)

| # | date | change | reason |
|---|---|---|---|
| A1 | 2026-11-25 | `rho` fixed as **depreciation rate** with `prep_stock ← (1−rho)·prep_stock + e`, `rho=0` = legacy undepreciated anchor; default 0.0 | task-3 acceptance line "rho=0 reproduces old behaviour" is only consistent with the depreciation convention; the literal recurrence in the brief contradicts its own acceptance test. engine-tutoring raised this; resolution recorded. |
| A2 | 2026-11-25 | `k['elite_prize']` added as persistent state (beyond the brief's four keys) | gate-level `elite_logw` already exists in the 540 config; labour must apply the *won* prize, and CF3 wage-compression scales gate prizes, so the prize amount must be stored per child. Supersedes the global-only application at `core` L498–499. |
| A3 | 2026-11-25 | `contest_price` kept as **pre-tax resource price**; new `contest_tax_rate` default 0 | avoids a second price parameter and makes tax=0 numerically legacy. Legacy CF1a "tax" arm is a price increase and must be relabelled when the new spec is frozen (wave 2). |
| A4 | 2026-11-25 | `E.values(..., track_state=None)` extension | needed for `gate_prize_dv` to price the actual track continuation value; backward compatible (default `None` = `k['track']`). |
| A5 | 2026-11-25 | `pl_win_probs(method='auto'/'exact')` must be **deterministic**; `auto` above `n=12` uses a documented deterministic algorithm, not unseeded MC. Added `pl_win_probs_detail`, seat-sum renormalisation + hard failure, accuracy/perf targets. | contest-math's draft had `auto → pl_win_probs_mc(rng=None)` (fresh unseeded generator) for `n>12`, which would make household expected probabilities non-reproducible. MC is retained only as `method='mc'` validation. |
| A6 | 2026-11-25 | `method='exact'` may support a documented cap larger than 12 (draft: `EXACT_MAX_N=20`) and must raise beyond it. | the draft's exact subset DP is genuinely exact to n=20; capping at 12 would be artificial. The binding requirement is "exact for n≤12, raise rather than approximate". |
| A7 | 2026-11-25 | `contest_candidates(m)` fixed as the **same-year sitting cohort** `cred==m & g==ends[m]-1` (fallback `cred==m`), superseding the literal `cred<=m` wording in §1.3/§6 | with the literal `cred<=m` pool the expected-probability object spans several year groups and is no longer the pool the Gumbel-max draw actually ranks — i.e. it would re-introduce the D2 mismatch the repair exists to remove. engine-core implemented this; Commander accepts and records it. Resolved by making the pool identical in `values()`, tutoring and the gate. |
