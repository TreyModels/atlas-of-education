# TUTORING AUDIT — Gate 1b (Phase A, read-only)

Lane: `engine-tutoring` · date 2026-11-25 · work tree `/Users/treymenefee/neon-boot/wt4/auditv2`
(branch `research/contest-audit-v2-2026-11-25` @ `7356c97`).
Sources read in full: `engine/eduengine/modules/tutoring.py` (171 L), `core.py` (580 L),
`planning.py` (113 L), `modules/schools.py`, `modules/sdg4.py`,
`papers/shadow-education-contest/code/run_hk_korea_comparative.py`, `REVIEW_RESPONSE_2026-11-25.md` §3–4.
Line numbers are from this tree at `7356c97`; every claim below was checked against the code.

Scope note: this lane may only edit `engine/eduengine/modules/tutoring.py` and `docs/audit/TUTORING_*.md`.
`core.py` is owned by lane `engine-core`; the Phase-B design below is therefore split into what tutoring.py can do
alone and what needs a contract hook in core.py.

---

## 1. Contest tutoring ledger — current state

### 1.1 Parameters (all in `CORE_DEFAULTS`, `core.py:50-56`)

| param | line | value | role |
|---|---|---|---|
| `elite_logw` | core.py:51 | 0.0 | log-wage premium for winning a `fail='track'` contest gate |
| `contest_r` | core.py:52 | 1.5 | Tullock/Plackett–Luce discrimination exponent `r` |
| `contest_alpha` | core.py:53 | 1.0 | effectiveness of contest effort in `x_eff` |
| **`contest_price`** | **core.py:54** | **0.05** | **single "unit price" of contest tutoring effort** |
| `contest_x0` | core.py:55 | 1.0 | free baseline contest input |
| `contest_max_e` | core.py:56 | 10.0 | annual cap on contest effort `e_t` |

There is **one price only** (`contest_price`). No resource price, no tax rate, no government
receipt, no rebate/transfer concept anywhere in the engine There is no contest-specific tax anywhere (`modules/state.py` `FiscalState` raises general income/consumption
revenue at `state.py:13-39`, but no contest-tutoring line, no receipt series, no rebate).

### 1.2 Effort choice and the spend expression

The contest block is `tutoring.py:72-137`, gated on `contest_gates` (`tutoring.py:75`) being non-empty.

- **Per-year spend accumulator declared**: `contest_spend_now = np.zeros(n)` — `tutoring.py:74`.
  (`contest_e_now = np.zeros(n)` — `tutoring.py:73` — is the per-year effort flow.)
- **Price read once**: `pc = float(p['contest_price'])` — `tutoring.py:77`.
- **Residual cash available**: `cash_rem = np.maximum(E._cash[idx] - y['extra_spend'][idx], 0.0)` —
  `tutoring.py:79`. `y['extra_spend']` here already contains the *budget-tutoring* outlays added at
  `tutoring.py:71`; contest outlays are added afterwards at `tutoring.py:137`, so the two are netted correctly
  in one direction only (see §3.4).
- **Cap and cash both bind the effort upper bound**:
  `e_hi = np.minimum(e_cap, cash_rem[sub] / max(pc, 1e-9))` — `tutoring.py:106`.
  So the regulatory cap (`contest_max_e`) and the household residual-cash budget both bind inside the search.
- **Private marginal cost used in the objective**: `c_y = pc / yy[sub]` — `tutoring.py:108`
  (price / household income; every utility term is income-normalised).
- The optimum `e_opt` is a 25-point grid + 8 golden-section steps (`tutoring.py:109-127`) with an explicit
  `e=0` corner comparison (`tutoring.py:128-133`).
- **The accounting line**:
  - `contest_e_now[idx[sub]] = e_opt` — `tutoring.py:134`
  - **`contest_spend_now[idx[sub]] = pc * e_opt`** — **`tutoring.py:135`**
  - `k['contest_e'] += contest_e_now` — `tutoring.py:136`
  - `y['extra_spend'] += contest_spend_now` — `tutoring.py:137`

So the current identity is exactly `contest_spend_now = pc * e_opt`, i.e. **price × physical effort, with no
resource/tax split**. All of it is booked as household outlay (`tutoring.py:137`) *and* simultaneously as
commercial-tutoring firm revenue (`firm_rev`, `tutoring.py:154`: `... + contest_spend_now[att].sum()`).
Those are the two sides of the same transaction, which is consistent only while 100 % of the price is a
resource cost. **Adding a tax to `contest_spend_now` without separating the two would double-count the tax as
firm revenue** — this is the main Phase-B ledger trap (§5).

### 1.3 Where the spend is recorded / consumed

- `E.note(...)` series set by tutoring each year: `contest_e_mean` — `tutoring.py:161`;
  `firm_rev` (includes `contest_spend_now`) — `tutoring.py:154`; `tut_spend` / `tut_k12_spend`
  (both are `y['extra_spend']`, therefore already include contest outlay) — `tutoring.py:153,157`.
- All yearly `E.note` fields are materialised into `E.R` by `core.py:539-560` (`record`, `E.yr_record`).
- **`contest_spend_now` itself is *not* written to `E.R`** — it exists only inside `extras()`, and leaves the
  module via `firm_rev` and via `y['extra_spend']`. There is no `contest_spend` yearly series.
- Downstream consumers of `y['extra_spend']`:
  - `k['spend'] += att*(y['cost'] + y['extra_spend'])` — `core.py:370` (child lifetime spend)
  - `k['tut_k12'] += k12 * y['extra_spend']` — `tutoring.py:141`
  - `tut_k12_spend_by_q` / `tut_k12_spend` — `tutoring.py:149,157`
  - `SDG4.measure`: `hh_spend = (y['cost'] + y['extra_spend'])[att].sum()` — `modules/sdg4.py:73`
  - the 540 runner's spend index: `k12_spend = mean(R["tut_k12_spend"][m:])` — `run_hk_korea_comparative.py:158`,
    whose cross-arm ratio becomes `total_spend_index` (`:225-244`). **This is the backward-compatibility path**:
    if `y['extra_spend']` keeps receiving the full `household_outlay`, the 540 spend index keeps computing.
- `contest_e_mean` is averaged for reporting at `run_hk_korea_comparative.py:163,183` and in
  `tutoring.summary` at `tutoring.py:171`.

---

## 2. Flat `contest_e` accumulation — no per-gate state, no depreciation

### 2.1 The state and its whole life cycle

- **Allocated once per child**, a single scalar: `contest_e=np.zeros(N)` in the new-cohort dict —
  `core.py:135`.
- **Grown by cohort concatenation**: `self.kids = {k: np.concatenate([self.kids[k], v]) ...}` — `core.py:136-139`.
  (Note for Phase B: `add_cohort` re-keys from the *new-cohort* dict, so a module that injects an extra key into
  `E.kids` loses it at the next cohort add. State must live in the module itself, or be added to `core.py`.)
- **Compacted on exit**: `keep = k['reason'] < 0; self.kids = {kk: v[keep] ...}` — `core.py:510-511`.
- **Accumulated as a lifetime sum since the last contest gate**: `k['contest_e'] += contest_e_now` —
  `tutoring.py:136`.
- **Consumed as "effective contest input" in two places**:
  - expected probability in the household value function:
    `x_eff = max(x0_c * max(Lend,0.1)/max(ends[m],1) + alpha_c * k['contest_e'][sl], 1e-6)` — `core.py:177`
    (inside the `gate['kind']=='contest'` branch `core.py:173-188`; `P = 1 - exp(-lam_contest[m] * x_eff**r)` at
    `core.py:178`)
  - realised gate draw:
    `x_eff = max(x0_c * max(k['L'][ci],0.1)/max(ends[m_],1) + alpha_c * k['contest_e'][ci], 1e-6)` —
    `core.py:406`; Plackett–Luce weights `w_log = r_c*log(x_eff)` — `core.py:407`.
- **Reset, flat and gate-agnostic**: `k['contest_e'][at_gate] = 0.0` — **`core.py:427`**, inside the
  `elif gate['kind'] == 'contest':` branch (`core.py:397`). It fires for *every* pupil at *that* gate, and only
  for contest gates; it carries no gate index, no per-gate state.

### 2.2 What is wrong for the audit's purposes

1. **One scalar, not one state per examination gate.** `k['contest_e']` mixes whatever the child accumulated at
   an earlier gate with what it is accumulating for the current one. The reset at `core.py:427` is the only thing
   that accidentally separates them; it is keyed to *being at a gate this year*, not to the gate the effort was
   for. A child who switches gate (e.g. KR G9 → G12; `p['gates']` at `run_hk_korea_comparative.py:113-118`) has no
   separate stock for the later gate.
2. **No depreciation.** `prep_stock_{t+1} = prep_stock_t + e_t` (implicitly, since `+=` at `tutoring.py:136`).
   Effort spent 6 years before the gate counts exactly as much as effort spent in the gate year. The
   Directive §1.3 `rho` decay is absent.
3. **Resets only on contest gates.** A bar/quota gate does not clear `contest_e` (`core.py:395-396`, `:430-436`),
   so stock can leak across non-contest gates.
4. **The household's own marginal-return calculation uses the same sum-to-date**
   (`e_cum = k['contest_e'][idx[sub]]`, `tutoring.py:104`; used as
   `x_g = b_i + alpha_c*(e_cum + grid)` at `tutoring.py:111` and in the golden-section refinements
   `tutoring.py:121-124`). It ignores both decay and the gate's distance; effort's projected date of arrival is
   not modelled.
5. **`contest_e` is never zeroed for a child who exits or who never reaches another contest**, and the reset at
   `core.py:427` is not mirrored anywhere a module can see — important for Phase B, see §6.

Refs for the review finding this audit must reference: `REVIEW_RESPONSE_2026-11-25.md` §3.B
(expected `1-exp(-lam x^r)` vs realised Gumbel-max PL; same `x_eff` construction).

---

## 3. Household cash budget — where tutoring outlays enter (and do not)

The engine has **two separate affordability checks**, and only one of them is a formal budget.

### 3.1 The formal schooling check (`core.py:335-354`)

```python
cash = max(y*exp(shock*shock_sigma) - subsist, 0) + borrow*y + yr['cct']      # core.py:336-337
need = yr['cost'] + need_frac(y)*child_wage(age)                              # core.py:338
broke = go & (need > cash)                                                    # core.py:339
att[idx[go & ~broke]] = True                                                  # core.py:340-341
self._cash = zeros; self._cash[idx] = cash - where(go, need, 0)               # core.py:354
```

`yr['cost']` is the school fee only: public levy + fee (`modules/schools.py:39-60`, `y['cost'] += ...` at
`modules/schools.py:57`) plus private-school price (`modules/schools.py:109-123`, `y['cost'] = where(priv, ...)` at `modules/schools.py:113`).
**Tutoring never enters `need`.** A child can be `broke` (school unaffordable) with zero tutoring; conversely a
child who attends always leaves `_cash >= 0` for the modules.

Also note `_cash` is a **per-child** residual built from **household** income `y`, with no division by the number
of children in the household: every child sees the full household income net of that child's own school cost.
That is the existing aggregation convention; Phase B must not silently change it, but the "budget never violated"
invariant must be stated per child (`outlay_i <= _cash_i`), not per household.

### 3.2 Budget tutoring (own teacher / firm) affordability (`tutoring.py:52-54`)

```python
cash = E._cash[idx]                                        # tutoring.py:52
u_own = where(own_ok & (cash >= p['p_own']), ..., -inf)    # tutoring.py:53
u_firm = where(firm_ok & (cash >= pf), ..., -inf)          # tutoring.py:54
```

- Checked **option-by-option before the choice**, against `_cash`; not against a running spend total.
- The chosen option's outlay is booked at `tutoring.py:71`:
  `y['extra_spend'] += where(own, p_own, 0) + where(firm, pf, 0)`.
- Firm capacity rations demand ex post (`tutoring.py:58-66`) but does **not** re-check cash for the re-routed
  children (they are re-routed to 0, so no spend), and the price `pf` is fixed before the choice
  (`tutoring.py:42`).
- That outlay is *not* deducted from `E._cash` globally; each module reads the same `_cash`. Global accounting of
  module outlays happens only through `y['extra_spend']` (`core.py:370`, `modules/sdg4.py:73`).

### 3.3 Contest tutoring affordability (`tutoring.py:79-108`)

- Residual after budget tutoring: `cash_rem = max(E._cash[idx] - y['extra_spend'][idx], 0)` —
  `tutoring.py:79` (correct ordering: budget tutoring added at `:71`, contest at `:137`).
- Binding cap: `e_hi = min(e_cap, cash_rem / max(pc, 1e-9))` — `tutoring.py:106`.
- Objective cost: `c_y = pc / yy[sub]` — `tutoring.py:108`.
- Hence **per child, the current code already enforces `contest_spend_now_i <= _cash_i - budget_tutoring_i`**,
  and hence `y['extra_spend']_i <= _cash_i`. That invariant is not asserted or reported anywhere; Phase B must
  keep it and add a check (§6).

### 3.4 Gaps in the budget accounting (to fix or to declare)

1. **No cross-module budget**: each module independently assumes it may spend `_cash`. Today only tutoring spends
   `_cash` in `extras`, so the invariant holds by ordering. Any Phase-B change must preserve the
   `_cash`-then-`extra_spend` ordering, or the budget can be violated.
2. **No tax wedge** anywhere: the household pays `pc*e_opt`; there is no distinction between the price the firm
   receives and the tax the household pays. The budget check therefore already checks exactly the same quantity
   that will become `resource_cost` today, but will be **wrong** once a tax is added (§5).
3. **No government/receipt ledger**: `E.R` has no tax revenue series, no per-quintile resource/tax split.
   §1.3's identity `gov receipts == sum(taxes)` currently has no representation, hence no test can bind it.
4. **`firm_rev` uses the outlay** (`tutoring.py:154`), so a tax added to outlay would be paid to firms too — a
   double count of the same unit of money, see §5.
5. **Rebates/transfers do not exist**. Nothing in the engine can credit a household for a contest subsidy, and no
   recipient is recorded.

---

## 4. How `tut_gain` and `extra_spend` reach `core.py`

### 4.1 `tut_gain` (learning channel)

- Created per year: `tut_gain=np.zeros(n)` — `core.py:310`.
- Written by tutoring: `y['tut_gain'] += where(own, tut_effect_own, 0) + where(firm, tut_effect, 0)` —
  `tutoring.py:68`. **This is budget tutoring only.**
- Consumed by the core learning equation:
  `dL = eff*exp(beta_a*a) + y['tut_gain'] + home_effect*(home-0.5) + learn_noise*rand` — `core.py:364`,
  applied only to attending children: `dL = where(att, max(dL,0), 0)` — `core.py:366`.
- **Contest prep effort `e_opt` never enters `dL` anywhere.** `grep contest` in the learning path is empty. So the
  current model is *pure positional coaching*: contest effort buys only a higher `x_eff` in the gate, with no
  skill accumulation. That is the spec the Phase-B learning switch must make optional, and it is why the 540
  default must keep `contest_learning = 0`.

### 4.2 `extra_spend` (money channel)

- Created per year: `extra_spend=np.zeros(n)` — `core.py:311`; **reset to zero every year**, so it is a flow, not
  a stock (unlike `contest_e`).
- Written by tutoring: budget tutoring `tutoring.py:71`; contest outlay `tutoring.py:137`.
- Consumed:
  - `k['spend'] += where(att, y['cost'] + y['extra_spend'], 0)` — `core.py:370` (lifetime household spend)
  - `k['tut_k12'] += where(k12, y['extra_spend'], 0)` — `tutoring.py:141`
  - `SDG4.measure` `hh_spend` — `modules/sdg4.py:73`
  - 540 runner `tut_k12_spend` / `tut_k12_spend_by_q` — `tutoring.py:149,157` → `run_hk_korea_comparative.py:158`
    → `total_spend_index` (`:225`).
- **`y['cost']` and `y['extra_spend']` are disjoint by construction** (schooling vs tutoring), so there is no
  double count between school cost and tutoring outlay in `k['spend']`, `hh_spend`, or the SDG4 household share.

---

## 5. Double-counting map (current and after the Phase-B change)

| flow | current code | Phase-B risk |
|---|---|---|
| household outlay | `pc*e_opt` → `y['extra_spend']` (`tutoring.py:135,137`) | must become `resource_cost + tax_paid`; budget check must use it |
| firm revenue | `contest_spend_now[att].sum()` added to `firm_rev` (`tutoring.py:154`) | **must become `resource_cost` only**, else tax is booked as firm revenue *and* as government receipt → double count |
| school cost | `y['cost']`, `core.py:338,370`, `schools.py:57,113` | disjoint from tutoring; no change needed |
| household spend total | `y['cost'] + y['extra_spend']` (`core.py:370`, `sdg4.py:73`) | keeps working if outlay includes tax; report tax separately |
| 540 spend index | `tut_k12_spend` ← `y['extra_spend']` (`tutoring.py:157`) | keeps working if `extra_spend` receives `household_outlay` — this is the compatible path |
| per-quintile spend | `tut_k12_spend_by_q` ← `extra_spend` (`tutoring.py:149`) | must add separate per-quintile `resource_cost` and `tax_paid` |
| contest_e stock | single scalar (`core.py:135,427`) | new per-gate stock; must keep writing a compatible effective stock into `k['contest_e']` because `core.py:177,406` read it directly |
| tax receipts | **absent** | new `E.note` series: gross receipts, rebates, resource cost, tax paid, per quintile |

Two further non-double-counting observations that Phase B must not break:
- `k['tut_k12']` (`tutoring.py:141`) and `tut_k12_spend` (`:157`) are the same quantity through different
  aggregations — both include contest outlay; keep both.
- `contest_e_mean` (`tutoring.py:161`) currently averages `contest_e_now` (annual flow) over K-12, not the stock;
  a stock report must be a new field, not a redefinition of `contest_e_mean` (the 540 comparator reads
  `contest_e_mean`: `compare_cf4_reference.py:26`).

---

## 6. Phase-B contract requirements that cannot be met inside `tutoring.py` alone

1. **Per-child persistent state.** `contest_e` is a core-owned array. A per-gate stock of shape `(N, nlev)` (or the
   contract's equivalent) must survive (a) cohort append `core.py:122-139`, (b) exit compaction `core.py:510-511`,
   and (c) the gate reset `core.py:427`. A module cannot inject a key into `E.kids` (`add_cohort` re-keys from the
   new-cohort dict), so one of the following is required from the contract / `engine-core`:
   - **(preferred)** `core.py` allocates the per-gate stock in `add_cohort` and compacts it with the other arrays,
     with configurable `rho` and cap; or
   - an `E.register_state(name, shape, dtype)` hook that `core.py` maintains through append/compaction; or
   - explicit permission for tutoring.py to keep module-side state and mirror the compaction itself.
   *Fallback that needs no core change:* tutoring.py maintains its own `(nlev, n_alive)` state arrays, extends them
   on cohort append, compacts them in the `after()` hook using `keep = E.kids['reason'] < 0` (exactly the mask
   `core.py:510` will take, since `after` runs at `core.py:502-503` before compaction), and detects core's gate
   reset by observing `k['contest_e'] == 0` at the start of the next `extras`. This is implementable but subtle;
   I will use it only if the contract does not provide a hook.
2. **Backward-compatible effective input.** `core.py:177` and `core.py:406` read `k['contest_e']` directly. To make
   the realised gate depend on *remaining stock* without editing core.py, tutoring.py must keep writing the
   updated stock into `k['contest_e']` for the child's next contest gate each year. `core.py:427` then clears it at
   the gate, which is the desired reset. Please confirm this is the intended compat shim (it keeps the
   expected-probability input and the realised input on the same scalar, as today).
3. **`rho` convention (blocking).** Task acceptance says *"rho=0 must recover the old flat behaviour"*, but the old
   behaviour is an **undepreciated lifetime sum** (`tutoring.py:136`, reset only at `core.py:427`), which under the
   stated recurrence `prep_stock_{t+1} = rho*prep_stock_t + e_t` is **`rho=1`**, not `rho=0`
   (`rho=0` gives current-year-only effort). Please confirm which is canonical:
   - **(a)** `prep_stock_{t+1} = rho*prep_stock_t + e_t`, and the "old behaviour" anchor is `rho=1`; or
   - **(b)** `rho` is a *depreciation rate*, `prep_stock_{t+1} = (1-rho)*prep_stock_t + e_t`, so `rho=0` is the old
     behaviour and the sensitivity grid runs over depreciation.
   I recommend (b) for matching the acceptance line; I will name the parameter so both readings are documented in
   `TUTORING_PHASE_B.md`. **This one blocks the acceptance test, so I need an answer before Phase B sign-off.**
4. **Parameter ownership.** Directive names are `p["contest_price_base"]` and `p["contest_tax_rate"]`. `core.py` is
   not my write scope. `Engine` rejects unknown params (`core.py:86-89`), so the new knobs must be declared as
   defaults somewhere. Proposal: tutoring module `defaults` own the whole contest-tutoring block
   (`contest_price_base`, `contest_tax_rate`, `prep_rho`, `contest_learning`, `contest_rebate`, and an effort cap
   alias), with `contest_price`/`contest_max_e` kept as deprecated aliases for the 540 config. Needs contract
   agreement to avoid a clash with `engine-core`'s `CORE_DEFAULTS` edit.
5. **Canonical 540 default must not move**: `contest_tax_rate` default `0.0`, `contest_learning` default `0.0`
   (pure positional), prep stock `rho=1` if reading (a) / `rho=0` if reading (b) — and any non-zero setting must be
   opt-in via the runner config, not a silent default change.

## 7. Phase-B acceptance checks I will implement (docs/ side only; `tests/` belongs to qa-verifier)

A standalone script `docs/audit/TUTORING_CHECKS.py` will assert, on small deterministic configs:
1. `household_outlay == resource_cost + tax_paid` per child and in aggregate (exact float identity, `atol=0`).
2. `government_receipts == sum(tax_paid)` and, if a rebate is active, `net_receipts == sum(tax_paid - rebate)` and
   `sum(rebate) == sum(rebate_credit_to_households)` (recipient recorded).
3. Per-quintile `resource_cost`, `tax_paid`, `outlay` sum exactly to the aggregate totals.
4. `e_t <= contest_max_e` for every child; report the binding rate (cap binds on a non-trivial share).
5. `y['extra_spend']_i <= _cash_i` for every attending child (budget never violated), including tax.
6. `rho`-anchor reproduces the unrepaired `contest_spend_now`/`contest_e_mean` path bit-for-bit on the 540 HK/KR
   config (or within 1e-12), and the 540 runner still produces `k12_spend` (`tut_k12_spend` in `E.R`).
7. Positional vs learning switch: with `contest_learning>0`, mean `dL` rises and contest effort per unit of dV
   falls (documented direction), everything else fixed.
