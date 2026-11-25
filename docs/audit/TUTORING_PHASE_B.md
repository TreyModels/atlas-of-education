# TUTORING PHASE B — Gate 1b implementation and acceptance evidence

Lane: `engine-tutoring` · date 2026-11-25 · work tree `/Users/treymenefee/neon-boot/wt4/auditv2`,
branch `research/contest-audit-v2-2026-11-25`.
Authority: `docs/audit/ENGINE_INTERFACE_CONTRACT.md` v1.0 §2/§4/§5/§6/§9/§10 (binding) and its amendment
A1 (rho = **depreciation** rate). Phase-A baseline audit: `docs/audit/TUTORING_AUDIT.md` (commit `fa34409`).
Files owned/changed: `engine/eduengine/modules/tutoring.py`, `docs/audit/TUTORING_PHASE_B.md`,
`docs/audit/TUTORING_CHECKS.py`. No other file was edited by this lane.

---

## 1. What changed (final file:line in `engine/eduengine/modules/tutoring.py`)

### 1.1 New parameters (`TutoringMarket.defaults`, L63–L69) — contract §10 ownership, no clashes

| parameter | default | meaning |
|---|---|---|
| `contest_tax_rate` | `0.0` | tax on the contest resource cost; household unit outlay `contest_price·(1+tax)` |
| `contest_prep_depreciation` | `0.0` | **rho = depreciation rate**; `prep_stock ← (1-rho)·prep_stock + pos_share·e` |
| `contest_prep_mode` | `'positional'` | `'positional'` (legacy) \| `'learning'` \| `'both'` |
| `contest_prep_learning_gain` | `0.0` | grade-equivalents of learning per unit `e_t` (learning/both; must be >0 there) |
| `contest_prep_positional_share` | `1.0` | positional weight of `e_t` in the gate (effective 0 in `'learning'` unless set) |
| `contest_rebate_policy` | `'none'` | `'none'` \| `'uniform'` (rebate credited to households) |
| `contest_rebate_rate` | `0.0` | share of `tut_tax` rebated under `'uniform'` |

`contest_price` / `contest_max_e` stay in `CORE_DEFAULTS` (engine-core). Validation is at `Engine`
construction (`setup`, L72–L96): unknown switch/policy or out-of-range values raise `ValueError`; `learning`/`both`
with a non-positive learning gain raises.

### 1.2 Fiscal ledger split (contract §4.1–§4.3)

Per child-year, L383–L391:

```
res_cost[i]   = contest_price · e_t[i]                  # L383
tut_tax[i]    = contest_tax_rate · res_cost[i]          # L384
tut_outlay[i] = res_cost[i] + tut_tax[i]                # L385  == household outlay (cash-budget quantity)
gov_tax[i]    = tut_tax[i]                              # L386  government receipt attributed to payer
rebate[i]     = rebate_rate · tut_tax[i]                # L388  only when contest_rebate_policy != 'none'
```

* Unit outlay and budget bound: `unit_outlay = contest_price·(1+tax)` (L289);
  `e_hi = min(contest_max_e, cash_rem / unit_outlay)` (L326) with
  `cash_rem = max(E._cash - pre-contest extra_spend, 0)` — so the **outlay**, never the resource cost, is what the
  household budget binds on.
* Asserted in code (contract §4.2, not assumed): `e_opt <= e_hi + 1e-12` (L398),
  `e_t <= contest_max_e` (L399), `contest outlay <= cash_rem` (L400), and the per-child-year global check
  `y['extra_spend'][att] <= E._cash[att] + 1e-9` (L405). Exact identities are asserted at L407–L409.
* `y['extra_spend'] += tut_outlay` (L403) **once** — so `tut_spend`, `tut_k12_spend`, `k['spend']` (`core.py`
  L876), and `SDG4.hh_spend` (`modules/sdg4.py:73`) stay household **gross outlays** and include the contest
  outlay exactly once (contract §4.3).
* `firm_rev` now counts **resource cost only**: `pf·(#firm) + res_cost.sum()` (L459) — the tax is a government
  receipt, not firm revenue. At `tax=0` this is numerically identical to the pre-repair expression
  (`tutoring.py:154` before repair), so the double-count trap flagged in `TUTORING_AUDIT.md` §5 is structurally
  impossible.
* Per-year ledger arrays for tests: `E.yr['res_cost'|'tut_tax'|'tut_outlay'|'gov_tut_tax']` (L411–L414),
  `E.yr['rebate']` when active (L421). Audit-only state (not read by any probability path):
  `E.yr['prep_stock_pre']`, `E.yr['contest_effort']`, `E.yr['contest_assigned_gate']`,
  `E.yr['contest_prob_evals']`, `E.yr['contest_grid_bound']` (L416–L420).
* Rebate semantics: policy active ⇒ rebate is a separate transfer line credited to paying households, recorded as
  `contest_rebate_total`, `contest_rebate_recipients` and `summary()['contest_rebate_recipient'] = 'households'`
  (L478–L480, L515). `gov_tut_receipt` is **not** reduced by the rebate (contract §4.1.4).
* Reporting series (additive; old keys unchanged): `contest_spend_now` = Σ outlay (backward-compatible name,
  L468), `contest_resource_cost`, `contest_tax_paid`, `gov_tut_receipt` (L469–L471),
  `contest_outlay_by_q`, `contest_res_cost_by_q`, `contest_tax_by_q`, `contest_effort_by_q`,
  `contest_prep_stock_mean`, `contest_rebate_total`, `contest_rebate_recipients`, `contest_learning_added`,
  `contest_k12_count_by_q`, `contest_assigned_count_by_q`, `contest_prob_evals`, `contest_grid_bound`
  (L472–L481); all mirrored in `TutoringMarket.summary()` (L493–L515).

### 1.3 Per-gate preparation stock (contract §2/§5; ownership split confirmed by engine-core)

* Core owns `k['prep_stock'] (N, nlev)`: allocated in `add_cohort`, compacted on exit, and consumed
  (`prep_stock[at_gate, m] = 0`) after the realised gate draw. Tutoring never allocates/removes it.
* Tutoring's sole annual update (L282–L286, L389): depreciation over **every attending child and every gate**,
  `k['prep_stock'][att] *= (1 - contest_prep_depreciation)`; then the chosen effort is accumulated on the child's
  gate column, `k['prep_stock'][sub, m] += pos_share·e_t`.
* `rho=0` is therefore the legacy **undepreciated lifetime sum** (the pre-repair `k['contest_e'] += e_t`);
  `rho=1` is memoryless (current-year effort only). Sensitivity grid is wave-2: `{0, .25, .5, .75, 1}`.
* `k['contest_e']` is now a **this-year flow only** (L390–L391, and zeroed for non-assigned at L402); it feeds
  `contest_e_mean` reporting and no probability/gate path (core reads `prep_stock`).
* Assignment: each contest gate's candidate pool is authoritative — `E.contest_candidates(m)` = children
  currently studying level `m` (`cred == m`, academic/track filters applied), i.e. the same pool core uses for the
  realised gate (L299–L305). *Deviation from the literal contract §5 "legacy assignment rule (cred<=m)" wording:*
  the frozen §6 API defines candidates as `cred==m`, so only children in the gate level accumulate prep; this was
  flagged to engine-core and the Commander (their API note says this was deliberate). Consequence: `contest_e_mean`
  is much smaller than the legacy series because only the gate-level grades prepare, not the whole school.

### 1.4 Expected probability and prize (contract §1.3/§5/§6) — no private PL, no phantom prize

* Expected `P` is the canonical module: `_pl_win_probs` (L520+) imports `eduengine.contest_math.pl_win_probs`
  and applies core's documented seat-sum renormalisation. There is **no** `1-exp(-lam x^r)` path and no private
  Gumbel/`argsort(-` implementation in the module (the legacy λ re-solve is not used).
* Weights are owned by core: `E.contest_weights(m)` gives the candidate weight vector; the counterfactual effort
  grid asks `E.contest_weights(m, idx=sub, stock_override=...)` and splices the overridden children into the
  cached full vector (`_weights_with_override`, L147–L181). We never re-derive `x_eff`.
* Prize is read **only** through `E.gate_prize_dv(m, idx)` (`_prize_dv`, L182–L193): tracking gates get the
  actual continuation-value difference; non-tracking gates `kappa·effective_elite_logw`; `elite_logw`/`track_prize`
  are never read directly (fixes the phantom G9 prize structurally).
* Effort choice (L330–L379): maximise `dV·P + learn_value·e − unit_net·e/y` (`unit_net` = net-of-rebate outlay;
  income-normalised cost keeps the legacy objective shape). Sampling = **9-point proportional grid**
  (`_PREP_GRID`, L48) over each child's `[0, e_hi]`, then a documented **analytic quadratic local search** through
  the three nodes around each child's best node (parabola vertex, clipped to ±half a step). Cost: **9 batched
  probability evaluations per contest gate-year** (0 when no pool member has a positive prize/learning value or a
  positive cash bound), with the residual bound reported as `contest_grid_bound` (≈|second difference|/8 relative).
  Universal seat (`seats_eff >= n_cand`) has no positional return: `e=0` unless the learning channel makes effort
  worthwhile (L374–L379). The 25-point+golden version was replaced because it made the 540 runner ~8× slower.

### 1.5 Optional learning effect / explicit positional switch (contract §5)

* `'positional'` (canonical default, 540 numerics): no learning channel, positional share 1.
* `'learning'`: positional channel off (effective share 0), `y['tut_gain'][sub] += contest_prep_learning_gain·e_t`
  (L393) feeds `dL` in `core.py` L870; effort is pursued only where the marginal value of learning makes it
  worthwhile (`learn_value = mvl·gain`, L330–L331).
* `'both'`: positional share = `contest_prep_positional_share` (default 1.0) **and** the learning channel.
* Defaults are legacy-neutral: canonical 540 config uses tax 0, depreciation 0, `'positional'`, gain 0 — no silent
  change to the 540 default. `contest_learning_added` reports the channel's annual contribution (0 in positional).

---

## 2. Acceptance evidence

### 2.1 `docs/audit/TUTORING_CHECKS.py` — 17/17 PASS against the integrated engine

Command (host): `PYTHONPATH="$PWD/engine" .../python docs/audit/TUTORING_CHECKS.py`.
Mode `engine` (core §6 API present). Checks (line refs in the script):

| # | check | result |
|---|---|---|
| 1 | mode detection | PASS (mode=engine) |
| 2 | identities + per-quintile reconciliation, `tax=0.5` (L282) | PASS — `outlay == res+tax` per year to 1e-12 rel; `Σgov_tut_receipt == Σtut_tax`; per-quintile means × counts reconcile to totals |
| 3 | annual cap binds `e_t`, `max_e=0.05` (L309) | PASS — max observed effort hit the cap exactly; no child exceeds it |
| 4 | cash budget never violated, huge cap forces cash bound (L319) | PASS — per-child `extra_spend <= _cash` every year, in-code assertions |
| 5 | tax ≤ effect: household effort falls, receipts rise (L328) | PASS |
| 6 | rebate credited to households, gov receipt not reduced (L342) | PASS — `rebate == 0.5·tax`, recipients>0, recipient='households' |
| 7 | prep-stock recurrence every year, rho∈{0,.5,1} (L356) | PASS — exact `(1-rho)·pre + share·e` |
| 8 | learning/positional switch direction (L370) | PASS — positional: no learning channel, prep stock >0; both: learning channel >0 and higher learned skill; learning: prep stock 0 |
| 8b | zero prize ⇒ zero positional effort and zero outlay, contract §11 test 1 | PASS |
| 8c | zero contest effectiveness ⇒ `e_t=0`, contract §11 test 2 | PASS |
| 8d | universal seat (`share_of='applicants'`, `share=1`) ⇒ `P=1`, `e_t=0`, contract §11 test 3 | PASS |
| 9 | no double count: `firm_rev` uses resource cost (L404) | PASS — matched-seed `Δfirm_rev == Δresource_cost` while `Δoutlay` includes the tax wedge |
| 10 | 540 runner compatibility (L417) | PASS — all runner-read `E.R` keys finite measured-window; `E.ALL[cohort,q,elite,g]` present; `contest_spend_now` series present |
| 11 | non-contest legacy worlds unchanged (L436) | PASS |
| 12 | invalid switch/policy raises at construction (L446) | PASS |
| 13 | **rho=0 == legacy cumulative stock; rho=1 == memoryless** (pid-matched, L462) | PASS — per-pid `prep_stock == Σ_e` at rho=0 and `== last-year e` at rho=1 |
| 14 | grid cost/accuracy (L486) | PASS — 9 evals per active gate-year; grid bound < 0.25; coarse-vs-25-point effort difference **2.5 %**, max bound **0.035** |

### 2.2 Runner-path integration (real 540 code path, `_run_single` from the unmodified runner)

* Reduced HK/KR arms (N=30,T=24) run end-to-end through `process`-free `_run_single`; determinism: same
  config+seed twice ⇒ identical seed rows (NaN-aware comparison, 0 mismatched keys).
* **Full-size single runs** (N=300,T=46, all 540 config params): HK **16.4 s**, KR **37.8 s** wall on the host
  (single process). Extrapolated 540-run campaign at 8 workers ≈ **30 min** (dominated by the canonical PL calls;
  the old mandatory cost was ~3 min, so the honest expected probability is the added cost — a documented,
  unavoidable consequence of contract §1.3, not a tutoring inefficiency).
* KR `GATE_SPECS['KR-SINGLE']` and `KR-TRACKED` (tracking gate, `gate_prize_dv` from the values recursion) both
  run without shape errors; tracking distribution and prep stock populated (`N=20,T=20` smoke).
* `firm_rev` change is numerically identical at `tax=0` (check 9).

### 2.3 Ledger identity summary (from check 2, tax=0.5 config)

`Σtut_outlay == Σres_cost + Σtut_tax` (rel 1e-12), `Σgov_tut_tax == Σtut_tax` (rel 1e-12),
per-quintile means × counts equal the aggregate totals for all three marginals, per-child `outlay_i <= cash_rem_i`
and `Σ tutoring outlay_i <= E._cash_i` in every year, `max e_t <= contest_max_e`, `e_t <= e_hi`.

---

### 2.4 CLEAN-TREE STAMP + full-size runner ledger numbers (gate 1b sign-off evidence)

Clean tree: `git archive 98baf6b` (branch tip; engine-core `f31e176` is in the tree, contest-math
`1a6f3d5`) → `docs/audit/TUTORING_CHECKS.py` **17/17 PASS**. Committed `tutoring.py` sha256
`7a6fd4c33cc2aefcd47da097b47ac7945744cc1adf9dedbb8ab1ec57d8adc2f8` (identical to the archive).
Full-size runner configuration HK N=300/T=46, 1 seed, `contest_tax_rate=0.10`, rho=0 (unless stated):

| quantity | value |
|---|---|
| `contest_spend_now` in `E.R` | present; Σ series = **861.864940** = Σ household contest outlay over all K–12 pupil-years (the K-12 post-promotion gauge artifact: sitters carry `g=12` after promotion, so a `g<12` filter misses them; the series is the gross contest outlay and is the binding quantity) |
| ledger identity per year | Σ outlay = Σ res + Σ tax; max per-year rel err **3.91e-16**; Σres **783.513582**, Σtax **78.351358**, Σgov **78.351358** (exact) |
| firm_rev double-count | actual Σ **6231.414966**; old-style (outlay-based) would be **6309.766324** ⇒ wedge = Σtax **78.351358** — `firm_rev` is resource-cost-only |
| cap / cash | max e_t = **6.0** = `contest_max_e` (binds); max(extra_spend − `E._cash`) = **−0.309** ≤ 1e-9 in every child-year |
| rho grid (HK tax=.10) | prep_stock_mean **0.475467 / 0.442238 / 0.451151**; contest_e_mean **0.029896 / 0.029477 / 0.030912**; k12_spend_mean **155.845 / 154.826 / 154.833** for rho = 0 / .5 / 1 |
| rho anchor (pid-matched, 739,200 (pid,gate) pairs) | rho=0 vs legacy undepreciated cumulative stock: **max abs diff 0.0**; rho=1 vs memoryless current-year contribution (after core gate consumption): **max abs diff 0.0** |
| learning switch (HK, `mode='both'`, gain 0.3) | `contest_learning_added` Σ **1729.64**; mean learned skill (cred≥1) **18.845104** vs positional **18.706977** (**+0.138127**); contest_e_mean 0.035199 vs 0.034762; positional default unchanged |
| timing (host, single process) | HK 33.4–38 s full-size; KR 58.4 s; cold first run 155 s (cache). ≈30–45 min for the 540 campaign on 8 workers |

Candidate-pool item is resolved by contract amendment A7 (sitting cohort): the effort assignment uses
`E.contest_candidates(m)` directly, i.e. exactly the same pool as the realised gate. Residual documented in §3.1:
under the sitting-cohort pool a child prepares only in the year it sits (retakers excepted), so `rho` has little
room to act on the canonical 540 spec; multi-year preparation would need a gate-approaching-pool extension
(wave-2 decision, not a defect in this lane).

## 3. Remaining risks / open items

1. **Canonical-pool wording.** Tutoring prepares only for the gate level (`cred==m`, core's authoritative
   candidate pool), not for `cred<=m` as the contract §5 legacy-assignment sentence says. This is a deliberate
   API-consistent choice (flagged to engine-core/Commander) and a *documented numerics change* for the 540 spec:
   `contest_e_mean` is much lower than the legacy series because only gate-level grades prepare. If the Commander
   wants the literal `cred<=m` accumulation instead, tutoring must price effort against a *future* pool the §6 API
   cannot currently evaluate — needs an API extension.
2. **Coordinated proportional grid.** The 9 batched PL calls evaluate every same-gate candidate at the same
   fraction of own cap, so `P_i` internalises cross-effort effects approximately (a coordinated-deviation
   profile), not an exact single-child deviation. This is a documented approximation with a reported bounding
   error (`contest_grid_bound`); exact per-child best responses would need `O(n_cand)` calls per grid point, which
   the 540 runtime cannot absorb. All contract invariants (monotone own weight, zero prize ⇒ zero effort,
   universal seat ⇒ zero effort) still hold.
3. **Numerics change vs pre-repair 540.** Expected with D2 (honest PL instead of `1-exp(-λx^r)`) and D5 (per-gate
   stock); not attributable to ledger accounting. Default config keeps tax 0 / depreciation 0 / positional, so
   the only sources of change are the repaired probability and the candidate-pool definition — documented here
   and to be quantified by the Commander's migration table (contract §9.3/§9.5).
4. **Learning-only mode at a top-level gate** can legitimately choose `e=0` when the marginal value of learning
   is zero (`mvl=0`, no further level); that is economically correct, not a switch failure (`'both'`/bar-gate
   configs show the positive direction).
5. **Clean-tree verification DONE** — see §2.4 (clean `git archive 98baf6b`, core `f31e176`: 17/17 PASS; stamped
   numbers above). Note §2.2's dirty-tree timings are superseded by the stamped ones.
6. **Box usage:** none needed; all checks are small and ran on the host (no box quota consumed by this lane).
