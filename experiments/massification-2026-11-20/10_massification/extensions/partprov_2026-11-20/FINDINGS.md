# FINDINGS — EXP-16 **PARTPROV** (count-blind provenance diagnostic)

**`LABEL: SYNTHETIC` for every number below.** No observed file was opened, no observed value is compared, no
33-cell count is computed or reported (audit: `results/COUNT_BLIND_AUDIT.json`; guard self-test
`BLOCKED-AS-REQUIRED`, blocked attempts 1, observed file opened **false**). This is a **diagnostic**: it adopts no
value from any arm, re-runs no delivered cell, re-scores no EXP-14 check, and makes **no causal and no direction
claim**. Predeclaration sha256 `d7c81309…` (frozen before any arm of this cell was run); frozen code
`sim_v1_6_repair.py` `9c0e7998…` and `sim_v1_3.py` `70ae8f0e…`, both byte-identical to the files under test.

---

## The answer in one paragraph

**The participation margin is a duplicated parameterisation — exactly so at primary and lower-secondary, and with a
measured residual at upper-secondary that sits in the eligibility pipeline, not in the participation share.**
Substituting the frozen v1.3 block's declared four-state outside-option primitives into the tier choice (P1) restores
the frozen block's own participation share **bit-identically in all 45 level-years** (maximum difference
`0.0` at the panel's written precision) and restores `demand_official/cohort` **exactly** at primary and
lower-secondary (gap `0.000000 pp` in 15/15 years each). At upper-secondary the cohort-normalised object still misses
the frozen block's realised share in 11 of 15 years (4/15 within ±1.0 pp, gap mean `5.992006 pp`, max `10.284467 pp`),
because there the realised demand is multiplied by an eligibility factor that P1 holds fixed by design. The
predeclared rule therefore returns **`MIXED`** for the cell (`DUPLICATED-PRIMITIVES` at primary and lower,
`MIXED` at upper), which **licenses EXP-18** under D144(6) and does **not** close the generator line at
representation-only.

## 1. What was run (three arms, one frozen object, no new number)

All three arms are the frozen v1.6 **A10** configuration (`bimodal=True, kappa_link=False, tier_surv=False`,
`phys_cap=1.15`, seed 20261120, frozen two-pass host resolution) on the **anchor** `SYN00_PHL_LIKE`, 15 anchor years
2010–2024, three levels. Arms differ only in one module-level function lookup on the byte-identical frozen file:

| arm | participation decision | refusal margin | verdict-bearing |
|---|---|---|---|
| **P0** | the tier block's own (hard refusal set, `1.60`/`0.03` cost multiples, no `both` state) | frozen `U_O > max(U_work,U_neither)` | no (comparator) |
| **P1** | **frozen v1.3** `state_shares(...)` called unchanged → `ds13 = Pr[school]+Pr[both]` | frozen, unchanged | **yes** |
| **P2** | same `ds13` mass as P1 | **removed by nesting** (no exit) | no (report-only) |

**Harness identity (guard, not a result).** P0 with the declared demographic input reproduces the frozen
`panel_A10_repaired.csv` PHL rows to a maximum relative error of **4.44e-10** over 315 compared cells
(`S-IDENT`, tolerance `1e-8`). The observed file is never opened: the PHL cohort/population path is reconstructed
from the frozen v1.3 **synthetic** panel (`band_population(primary,t)/band_share[0]`, `population(t)`), so all three
arms sit on the frozen block's own declared demographic path.

## 2. The verdict (predeclared rule, applied unchanged)

| level | P0 `demand_official/cohort` (mean) | frozen block's own (mean) | P1 (mean) | years within ±1.0 pp | years moved ≤0.5 pp | verdict |
|---|---|---|---|---|---|---|
| primary | 0.900000 | 0.995677 | 0.995677 | **15/15** | 0/15 | **`DUPLICATED-PRIMITIVES`** |
| lower_secondary | 0.826667 | 0.954303 | 0.954303 | **15/15** | 0/15 | **`DUPLICATED-PRIMITIVES`** |
| upper_secondary | 0.647287 | 0.694552 | 0.634632 | **4/15** | 1/15 | **`MIXED`** |
| **aggregate** | — | — | — | — | — | **`MIXED`** (unanimity rule) |

Gap = |P1 − frozen block|; move = |P1 − P0|; both in pp. P0's own gap is `9.567735 / 12.763614 / 5.709341 pp`
(mean), so **every level starts 5.7–12.8 pp below the frozen block's own share**. P1's move is
`9.567735 / 12.763614 / 1.265465 pp` (mean), max `9.576937 / 15.656053 / 2.342124 pp`. Precedence was tested in the
declared order (`DUPLICATED-PRIMITIVES` first); no level satisfied both labels (`both_applicable = 0` everywhere).

**Anchor cells (the two the Council will quote).** Primary 2024: P0 `0.900000`, frozen `0.9956438553`, P1
`0.995643` → gap `0.000000 pp`. Upper 2010: P0 `0.489845`, frozen `0.552736`, P1 `0.480640` → gap `7.209612 pp`.

## 3. Why upper-secondary is `MIXED` — and why it is not a menu effect

In this class `demand_official/cohort = ds × elig`, with `ds` the participation share and
`elig = min(1, eligibility_pool/cohort)` the pipeline factor. Measured on the second object:

- **`ds` (participation share): P1 equals the frozen block in every one of the 45 level-years — maximum
  |Δ`ds`| = `0.0` at written precision** (secondary-target column, `results/PARTPROV_DETAIL.csv`).
- **`elig`: P1 carries P0's pipeline** (0.5973 in 2010, 0.9219 in 2020, 1.0000 from 2022 at upper), because P1 keeps
  the tier block's admission and refusal margins fixed; the frozen block's own pipeline is higher (implied 0.6870 in
  2010). The entire upper-level residual is `ds × |Δelig|`: at 2010, `0.804590 × (0.6870 − 0.5973) ≈ 7.2 pp` — the
  measured `7.209612 pp`.

So the upper label is `MIXED` **because the realised, cohort-normalised demand is jointly gated by the eligibility
pool**, not because any menu object enters the participation share. The cell measures *where the residual sits*: in the
pipeline factor, not in the participation decision. No menu object (`q_O`, `T06/T07`, `T12/T13`) is moved by P1, and
the frozen block's participation primitive does not read any of them.

## 4. P2 — nesting and the unfilled object (reported, never adopted)

`unfilled = V_O/K_O`; "zero" = `V_O ≤ 1e-12`.

| arm | primary: years with `V_O = 0` (of 15) | lower: years with `V_O = 0` | upper: years with `V_O = 0` | upper `unfilled` min–max |
|---|---|---|---|---|
| P0 (as built) | 3 | 12 | 0 | 0.5174 – 0.7127 |
| P1 (primitives) | 12 | 13 | 0 | 0.4325 – 0.6635 |
| **P2 (nested)** | **15** | **15** | 0 | 0.1328 – 0.4559 |

**Nesting destroys the unfilled object at primary and lower-secondary (15/15 years at zero) and does not destroy it
at upper-secondary.** That is a **representation** statement, not a level one, and P2 supplies no number to any
successor. The same table carries a warning the Council did not ask for but needs before EXP-18: **P1 — the licensed
declaration-consistency route — also collapses the unfilled margin at primary (12/15 years at zero) and lower
(13/15)**, because a larger school-going mass fills the Tier-O places that were previously left empty. Under P1 the
`unfilled ≥ 0.10` condition holds in 0/15 years at primary and 0/15 at lower (P0: 5/15 and 2/15). The representation
capability and the participation margin are therefore in tension on this class, and that tension is **measured, not
adjudicated**, here.

## 5. What this licenses — EXP-18

- **Aggregate `MIXED` → EXP-18 may be predeclared** (D144(6), D145 #3). `STRUCTURAL-MENU` was not returned, so the
  generator line does **not** close at representation-only and EXP-18 is **not VOID by its own rule**.
- **The declaration-consistency part is licensed as a declaration, not a fit:** one behavioural object
  (school-versus-outside) declared once, **no new parameter** (P1 added zero numbers; every value is a frozen v1.6
  constant or a frozen v1.3 declared primitive, cited by name).
- **The part that must be declared and reported as a sensitivity (the `MIXED` residue):** the eligibility-pool
  coupling at upper-secondary, i.e. the fact that the realised demand share is `ds × elig` and `elig` is itself
  downstream of the Tier-O refusal margin. EXP-18's level statement must be conditional on that coupling; it may not
  move it.
- **The closing rule is unchanged:** if EXP-18 misses its predeclared bar, the generator line closes at
  representation-only and there is no successor this phase.
- **The representation warning in §4 is a design input, not a licence:** EXP-18's carried-forward
  `unfilled ≥ 0.10` condition should be re-read against the P1 column before its predeclaration is frozen.

## 6. What this does **not** license

1. **No observed statement.** Nothing here says anything about any observed series; the observed file was never
   opened and no observed value appears in any output.
2. **No causal or direction claim.** The labels name *which object* produced the share in a synthetic class. They do
   not say why any observed path took the values it did.
3. **No level statement and no adoption.** No arm's value is adopted into any generator, parameter table, panel or
   successor; P2 in particular is never adopted. A10's `PATH-FAILED` verdict stands permanently and is not re-scored.
4. **No re-fit and no threshold move.** Thresholds (`±1.0 pp`, `≤0.5 pp`, 15/15, the 2010–2024 set, the three
   levels, the verdict words) were frozen in `PRE_DECLARATIONS.md` (`d7c81309…`) before any arm ran, and no
   parameter was chosen by reference to any result.

## 7. Guards, audit, determinism

- **Count-blind guard (three layers).** (i) AST scan of all four executed sources: the cell's own two files contain
  the forbidden basename **only** as the guard constant `OBSERVED`, with **one** `open` site (the self-test) —
  `own_code_rule = PASS`, 0 violations; the two frozen files each contain exactly **one** forbidden literal, inside
  `load_observed_phl_paths`, which is **shadowed before any arm runs** and never called. (ii) Runtime open-audit over
  the whole scored path: **observed file opened = false, bytes read 0, blocked attempts 1** (the self-test), and the
  complete list of opened files is in the audit (14 entries, all synthetic panels / code / outputs). (iii) Guard
  self-test: the attempted open was **BLOCKED-AS-REQUIRED** before the OS call.
- **No-count.** No observed deviation and no 33-cell object is computed; `count_computed: false`,
  `n_33cell_counts_emitted: 0`, `n_observed_files_referenced_in_code: 0`.
- **Reachability lint.** Only two frozen-module calls are reachable from this cell's code: `verify_predecl` and
  `run_arm_full` (+ `state_shares` from the v1.3 block). No scoring function is reachable.
- **Determinism.** Two complete runs, **byte-identical 3/3** (`PARTPROV_RESULTS.csv`, `PARTPROV_DETAIL.csv`,
  `COUNT_BLIND_AUDIT.json`); no RNG in this cell beyond the frozen engine's unchanged seed/draw order.

## 8. Limitations (stated, not hidden)

1. **The P1 equality is a closed-form identity, not an independent replication.** The frozen participation primitive
   is a deterministic function of the (unchanged, static) household parameterisation and the shared income-shock
   draw, so substituting it reproduces the frozen share exactly by construction. What the cell establishes is
   **which object sets the share** (the duplicated primitive, not the menu), **not** that an independently
   re-specified block would land on the same number.
2. **The upper residual is a held-fixed pipeline, not a menu contribution.** P1 deliberately keeps the tier block's
   refusal margin (removing it is P2). The residual therefore measures the coupling, and the coupling's size is
   conditional on the unfixed Tier-O margin.
3. **Three levels, one anchor system, 15 years.** Tertiary is excluded and declared so (it has no participation
   decision; the tier block only splits its composition).
4. **P2's zero unfilled is partly a capacity statement:** at primary/lower the O-candidate mass exceeds `K_O`, so
   nesting fills O places rather than revealing demand; that is why P2 is report-only.

## 9. Files

`PRE_DECLARATIONS.md` (`sha256 d7c81309…`) · `code/run_partprov.py`, `code/arms.py`,
`code/frozen/sim_v1_6_repair.py`, `code/frozen/sim_v1_3.py` · `results/PARTPROV_RESULTS.csv` (per arm × level + the
aggregate row) · `results/PARTPROV_DETAIL.csv` (per arm × level × year, 45 cells per arm) ·
`results/COUNT_BLIND_AUDIT.json` · `results/determinism_run2/` · `RUN_MANIFEST.json` · `SHA256SUMS.txt`.

**Closed-claim check (D145 §5.1.6):** does not re-run A10 as a verdict; does not re-score EXP-14's S1 or any C-check;
re-freezes nothing; adopts no value from any arm; no C1–C4 reopening; no direction claim; no observed read; both the
arms and this report are `SYNTHETIC` diagnostics and none is a test of A5.
