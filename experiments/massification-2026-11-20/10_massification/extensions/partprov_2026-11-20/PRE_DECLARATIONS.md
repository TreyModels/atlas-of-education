# PRE_DECLARATIONS — EXP-16 **PARTPROV** (count-blind provenance diagnostic)

**`LABEL: SYNTHETIC` for every generator object and every arm output. `LABEL: OBSERVED` is used nowhere in this
cell: no observed file is read, no observed value is compared, and no 33-cell count is computed or reported.**
This is a **diagnostic**, not a scored test: it adopts **no** value from any arm, re-runs **no** delivered cell as a
verdict, re-scores **no** EXP-14 check, re-freezes nothing, re-opens no C1–C4 claim, makes **no causal and no
direction claim**, and does not test A5. It is a new cell (Council brief 024 §5.1, D145 #1) with a new
predeclaration. Its question is **provenance**, not size.

Frozen before the run: this file, `code/run_partprov.py`, `code/arms.py`, and the byte-identical copies
`code/frozen/sim_v1_6_repair.py` (sha256 `9c0e7998…`) and `code/frozen/sim_v1_3.py` (sha256 `70ae8f0e…`). The driver
embeds the sha256 of **this** file and **refuses to run** on any mismatch; it also parses the machine-readable block
in §9 and refuses if any declared constant differs from the code's own constants. **No threshold, band, year set,
level set, arm definition or verdict word below is chosen by reference to any result — no arm of this cell had been
run when this file was hashed.** Disclosed state of knowledge at freeze: the frozen v1.6 **P0** arm already exists on
disk (`panel_A10_repaired.csv`, D144) and the frozen v1.3 block's panel already exists on disk; both were readable
before freeze and their values are **not** new information. **No P1 or P2 output existed anywhere on disk at freeze
time.** The declared 15 anchor years and the per-level rule are copied from the Council block, not selected.

---

## 1. The EXP-16 block, **verbatim** (SYNTHESIS_024.md §5.1, lines 413–459; sha256 of the source file
`6c6aea45…`). The four operative thresholds (15 years; ±1.0 pp in ≥15/15; ≤0.5 pp; VOID on any observed read) are
taken from this block and are **not** restated with any other value anywhere in this file.

> ### 5.1 EXP-16 — **PARTPROV**: is the participation margin a *duplicated parameterisation* or a *structural consequence of the declared tier menu*? (rank **#1**)
>
> 1. **First-order link (schooling supply + government capacity at the floor; the model-level question).** What sets the
>    model's **floor level** now that EXP-14's C3 established the floor is **take-up-limited, not capacity-limited**?
>    The answer is the **participation margin**: `demand_share` 0.900000 and `admission` 0.800000 against the frozen
>    block's 0.995644, with survival identical (V17, V18). The question is **provenance**, not size: is that loss
>    produced by a **second, undeclared outside-option parameterisation** inside the tier block (a
>    declaration-consistency defect, repairable **without a new value**) or by the **declared tier menu itself**
>    (`q_O = 0.55`, the declared cost/quality of Tier O; structural, **not** repairable without a fit)?
> 2. **What changes if positive vs negative.** **`DUPLICATED-PRIMITIVES`** → the successor is licensed as a
>    **declaration-consistency** act (one behavioural object declared once, no new parameter), and the observed-path
>    question is worth one more cell (EXP-18). **`STRUCTURAL-MENU`** → **no repair is admissible** without moving a
>    declared value against the path, the generator line **closes at representation-only**, and the programme's model
>    line becomes (b)+(c) immediately. **`MIXED`** → only the consistency part may move; the structural part must be
>    **declared and reported as a sensitivity**, with the level statement conditional on it. **Either way the answer is
>    actionable before EXP-18's predeclaration is frozen** — which is the whole point of ranking it #1.
> 3. **Why it is not a niche.** It is the only remaining question between the programme and either a level model or an
>    honest close. Every other candidate has been eliminated by measurement: survival (identical in both arms), `q_O`
>    (inert at 0.55; 3/33 even at 1.00), κ (diagnostic only, D138), `phys_cap` (never binds at the anchor). A reader of
>    the first-order question is entitled to know whether the model's level is set by a **declared behaviour** or by a
>    **duplicated parameter**.
> 4. **Data on disk (no DATA ASK).** `generator_v1_6_repair/code/sim_v1_6_repair.py` — the tier-choice/utility block and
>    the outside-option evaluation (the `max(U_work, U_neither)` refusal set disclosed in v1.5's post-run note);
>    `generator_v1_6_repair/PARAMS.md` — `T01 h_share` = (0.15, 0.28, 0.40, 0.50), `T05 q_O` = **0.55**, `q_H_mult =
>    q_O_mult = 1.00` (survival), `v_O = 0.55 v_H`; the frozen v1.3 parameter set and its **declared four-state
>    outside-option primitives** (cited **by name**, values unread by the Council); `results/panel_A10_repaired.csv` and
>    `results/panel_A00_v13cols.csv` — columns `demand_official`, `admitted_official`, `cohort`, `survival`,
>    `measurement_factor`; `results/representation_cells.csv` — `unfilled`, `queue_ratio`; `results/reconciliation_v15.csv`
>    (the 1-cell `demand_official` difference between A11V15 and frozen v1.5).
> 5. **Threshold + falsifier (fixed before the run).** Three **diagnostic** arms on the frozen v1.6 code, **no value
>    adopted, no arm scored on the path**: **P0** = as built; **P1** = the tier choice evaluated with the frozen v1.3
>    block's **declared outside-option primitives substituted unchanged** (no new number); **P2** = the tier choice
>    restricted to the **frozen block's school-going mass** (a diagnostic of what nesting would do to the unfilled
>    object, not a repair). Verdict, per level, over the **15** anchor years 2010–2024: **`DUPLICATED-PRIMITIVES` iff
>    P1 moves `demand_official/cohort` to within `±1.0 pp` of the frozen block's own demand share in `≥ 15/15` years**;
>    **`STRUCTURAL-MENU` iff P1 moves it by `≤ 0.5 pp`**; `MIXED` otherwise. **P2 is reported, never adopted:** the
>    Council needs to know whether nesting **destroyed** the unfilled object (if `unfilled → 0`, nesting is not an
>    admissible repair and only primitives-unification is), and that is a **representation** statement, not a level one.
>    **COUNT-BLIND GUARD (binding):** no arm may read `UNIVERSALIZATION_SERIES.csv`, compute a deviation, or emit an
>    observed-path count; the driver must refuse to run if the observed file is opened, and the build must carry an
>    AST/static check for it. **Falsifier:** any arm that reads the observed series, or any report that contains a
>    33-cell count → verdict **VOID (`CONTAMINATED-BY-DESIGN`)**, and EXP-18 loses its licence.
> 6. **Closed-claim check.** Does **not** re-run A10 as a verdict, does **not** re-score EXP-14's S1, does **not**
>    re-freeze any EXP-14 check; adopts **no** value from any arm; no C1–C4 reopening; no direction claim; the arms are
>    `SYNTHETIC` diagnostics and none is a test of A5.
> 7. **Cost / rank.** **Small–medium** (one diagnostic build on the frozen v1.6 base, three arms, **no observed data**).
>    **Rank #1** — cheapest decisive cell in the slate; it decides whether the generator line continues.

---

## 2. What this cell decides, in one sentence

**Which of two objects sets the participation margin:** the tier block's own second parameterisation of
school-versus-outside (a **duplicated primitive**, repairable as a declaration-consistency act with **no new value**),
or the **declared tier menu** (`T05 q_O = 0.55`, `T06/T07` relative costs, `T13` risk, `T12` gate — **structural**,
not repairable without fitting a declared value against the path)? The cell returns a **label per level** and one
aggregate label. It returns **no** level statement, **no** repair, and **no** observed comparison.

## 3. The three arms, by full switch tuple (D147(iii))

The object under test is the **frozen v1.6 code**, copied byte-for-byte into `code/frozen/sim_v1_6_repair.py`
(sha256 `9c0e799850fd30bb0b46bb7841e8f301715745a5c73452e7644055122325de56`, identical to
`generator_v1_6_repair/code/sim_v1_6_repair.py`). The frozen v1.3 block is copied byte-for-byte into
`code/frozen/sim_v1_3.py` (sha256 `70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877` = the v1.6
`EXPECTED_BASE_SHA`). **Neither copy is edited.** Arms are produced by replacing exactly one module-level function
lookup in the imported frozen module (`tier_cells`), never by editing the frozen file.

Every arm runs with the identical engine tuple
`bimodal=True, kappa_link=False, tier_surv=False, tier_cfg=None, inject_upper=None, w_child_mult=1.0, phys_cap=1.15,
shadow=True, hosts=<frozen two-pass host rule>, seed=20261120` — i.e. the **A10** configuration of the frozen v1.6
run (the bimodal class, κ OFF per D138/R6, no retained tier survival penalty per R4c). The two-pass host resolution
(`run_arm_full`: shadow-BLIND pass, then `resolve_hosts`, then the run) is the frozen procedure, unchanged.

| arm | `tier_cells` | `tier_allocate` | participation decision | refusal margin (`acc`) | verdict-bearing |
|---|---|---|---|---|---|
| **P0** | frozen `tier_cells` | frozen `tier_allocate` | tier block's own (hard refusal set, `1.60`/`0.03` cost multiples, no `both` state) | `U_O > max(U_work, U_neither)` (frozen) | as built — the comparator |
| **P1** | `arms.tier_cells_p1` | frozen `tier_allocate` via `arms.alloc_compose` (pass-through: rewrites **only** `mW, mB, mN`, a reporting object) | **frozen v1.3 four-state logit**, called as `sim_v1_3.state_shares(cp, level, y_shock)` — the frozen function itself, no re-implementation, no new value | `U_O > max(U_work, U_neither)` (frozen, unchanged) | **YES** |
| **P2** | `arms.tier_cells_p2` | frozen `tier_allocate` via `arms.alloc_compose` (identical pass-through) | frozen v1.3 mass (same call as P1) | **none** — nesting: the mass is school-going by construction, so no cell can exit to the outside option | NO (report-only) |

**Capability lint (D147(iii)), enforced by the build.** P1 and P2 both require (i) `bimodal=True` (the tier block
must exist), (ii) the frozen `tier_allocate` symbol to be the *frozen* one, (iii) `sim_v1_3.state_shares` to be
callable and to return a 4-vector summing to 1±1e-12, and (iv) L < 3 (levels with a household participation
decision). If any of these fails, the build **aborts** (`REFUSED: CAPABILITY-LINT`) instead of producing a partial
table. P0 with `bimodal=False` (the single gate) would be a different arm and is **not** used here.

### 3.1 P0 — as built

Frozen `tier_cells` and frozen `tier_allocate`, unmodified. `demand_official = A_H + A_O_first` (the D-2
unduplicated applicant object of v1.6). This arm exists to (a) prove the harness runs the frozen code path and
(b) supply the **movement** baseline for the `STRUCTURAL-MENU` threshold.

### 3.2 P1 — the frozen v1.3 block's declared outside-option primitives, substituted unchanged

**What is substituted (the whole of it).** In the frozen v1.3 block, who is school-going is decided by the
**declared four-state block** `state_shares(cp, level, y_shock)` — the multinomial logit over
`{school, both, work, neither}` with its declared primitives `NEED = 0.85`, `UTIL_SCALE = 0.30`,
`GIRL_SHARE = 0.50`, `TASTE = 0.0`, `ABILITY = 0.0`, `OUT_YEARS = 0.0`, `AGE_W = (0.25, 0.70, 1.00)`, the
declared `cost_base = (0.05, 0.14, 0.22)` and the declared `cp` fields `y_med, w_child, farm, cost, v0, decay,
compat, neither, girl_care`. Its school-going share is `ds13 = Pr[school] + Pr[both]`, and its out-of-school split
is `(Pr[work], Pr[neither])`.

P1 **calls that frozen function** (`sim_v1_3.state_shares`, sha256 of the defining file recorded above) and uses its
two outputs, `ds13` and `(Pr_work, Pr_neither)`, as the participation primitives of the tier block. **Nothing is
re-implemented and no number is introduced.** The substituted object is exactly the object the tier block duplicates.

**What is NOT substituted (the menu).** The tier block's declared menu is held fixed: `T01 h_share`, `T05 q_O = 0.55`,
`T06 cost_H_mult = 1.60`, `T07 cost_O_mult = 0.03`, `T12 a_gate = 0.40`, `T13 risk_pen = 0.20`, `T14 H_h = 20.0`,
`S01–S08` cell weights/ranks, and the frozen `tier_allocate` ranking and capacity split. In particular the
**O-versus-outside refusal margin** `acc: U_O > max(U_work, U_neither)` is **kept exactly as built**, because that
margin is where the menu's declared quality discount acts (R4a: `q_O` enters `U_O` and nowhere else) — removing it
would be a *second* change and is exactly what P2 is for.

**Operative rule (deterministic, no RNG).** For each level `L < 3` and year `t`, with frozen `cp, level, y_shock`:
1. `Pr = sim_v1_3.state_shares(cp, L, y_shock)`; `ds13 = Pr[0] + Pr[1]`; `(pw, pn) = (Pr[2], Pr[3])`.
2. Per cell `k` (5 income × 3 ability), the school-going mass weight is `w_school[k] = w[k] * ds13`
   (`w[k]` = the declared `S01` joint weights, sum 1). The block has no income/ability dimension, so the mass is
   **uniform across cells by construction** — this is the block's own structure, not a smoothing choice.
3. The tier block's own payoff comparison splits that mass: `first = H` iff `U_H[k] > U_O[k]`, else `O`
   (tie → `O`, the frozen convention `elif uh > u0: H else O`; the frozen `U_H, U_O` formulas and the tier block's
   own `cost_H, cost_O, hterm, risk, v_H, v_O = q_O·v_H` are used unchanged).
4. The frozen `tier_allocate` is called with `w = w_school`, `first ∈ {H, O}`, `U_O`, `u_out` unchanged, and the
   frozen `K_H, K_O`; its result is used unchanged **except** the out-of-school composition `(mW, mB, mN)`, which is
   overwritten with `(pw, pn, 0)` scaled to the mass — a reporting object only (declared, no effect on demand,
   admission or capacity).
5. `demand_official = A_H + A_O_first` as in P0 (`A_O_first` = first-choice-O mass).

`ds13` is the frozen block's own participation share evaluated at **P1's own state** (P1's own `Y, X, w_child,
y_med, cost, pools`), which is not identical to the frozen panel's state — that difference is the substance of the
test, not a nuisance: the substitution returns the block's **primitive**, and the cell measures whether the
primitive, run inside the repaired class, lands on the block's own share.

### 3.3 P2 — the tier choice restricted to the frozen block's school-going mass (report-only, never adopted)

Same engine tuple and same `ds13` call as P1. The difference is the **use** of the mass: P2 applies the tier block's
own participation **structure** to the nested mass, i.e. the tier block's 15-cell payoff comparison (`U_H` against
`U_O`, frozen formulas, frozen `outside_utilities16` still evaluated for the reporting object) is evaluated over the
mass `w_school = w·ds13` with **`first ∈ {H, O}` only and no exit** — because the mass is, by nesting, already
school-going, there is no outside option to refuse to. The frozen `tier_allocate` then produces `admitted_H, T_O,
V_O` on that nested mass.

P2 therefore answers exactly one question, in the Council's own words: **does nesting destroy the unfilled object?**
It reports, per level and year, `V_O/K_O`, `T_O/K_O`, `admission/cohort`, and the level-level counts
`years_with_unfilled_zero` and `years_with_unfilled_ge_0.10`. **P2 carries no verdict and is never adopted**: it is
a **representation** statement about the unfilled object, not a level statement, and it supplies no number to any
successor. P2's demand object is reported for completeness only and does **not** enter any threshold.

**How the exit is removed (declared implementation detail, no behavioural value).** P2 keeps the frozen
`tier_allocate` call and the frozen `tier_cells` formulas; the *outside option* is removed by construction by
setting the cell's `u_out` to the sentinel `arms.OUTSIDE_REMOVED = -1.0e300`, so the frozen refusal test
`U_O > u_out` is vacuously true and every refused Tier H applicant is offered a Tier O place while capacity
remains. `u_out` is not a behavioural parameter of the tier block (it is the outside option this arm deletes); no
declared value is moved and `OUTSIDE_REMOVED` is a sentinel, not a number that can be fitted. Both P1 and P2 use the
identical mass and the identical H/O payoff comparison, so the **only** difference between them is this removal —
which is exactly what isolates the unfilled-object question.

## 4. The comparison target, the anchor, and the 15 years

- **Anchor system:** `SYN00_PHL_LIKE` (index 0), the frozen v1.6 anchor. **Levels:** `primary`,
  `lower_secondary`, `upper_secondary` — the three levels the four-state household block governs. **`tertiary` is
  excluded and declared so:** its demand is an adult pipeline object (`t3_a/b/c`), not a participation decision, and
  the tier block only splits its composition.
- **Years:** **2010–2024 inclusive = 15 anchor years** (the Council block's own set; not selected here).
- **Primary target (verdict-bearing):** `demand_official / cohort` in each arm's own panel, compared with the
  **frozen v1.3 block's own `demand_official / cohort`** at the same level and same year
  (`generator_v1_3/results/synthetic_panel_v1_3.csv`, sha256 `47d4b082…`, columns `demand_official`, `cohort`).
  This is the frozen block's **realised** demand share — the same construction as the arm object — and is the
  reading that matches the block's quoted `0.9956438553`. The target is a **SYNTHETIC** object.
- **Secondary target (declared, NON-verdict-bearing):** the frozen block's own `demand_share` column (its
  pre-eligibility participation share `ds`). Reported per cell **only** to show whether the eligibility pool path
  confounds the primary target; it cannot change the label. If primary and secondary disagree, the primary stands
  and the disagreement is reported in `FINDINGS.md` (it is a robustness statement, never a threshold move).
- **No third target, no band, no exclusion rule.** A gap of exactly `1.0 pp` is **within** (`≤`); a movement of
  exactly `0.5 pp` is **≤ 0.5** (moves `≤`0.5). Both are inclusive, declared here.

## 5. Label definitions, precedence, and aggregation (D147(i) precedence rule)

Per level, over the 15 anchor years, with `g_t = |P1_dc(t) − V13_dc(t)|` in pp and `m_t = |P1_dc(t) − P0_dc(t)|`
in pp:

1. **`DUPLICATED-PRIMITIVES`** iff `g_t ≤ 1.0` for **all 15** years (`years_within_1pp = 15/15`).
2. **`STRUCTURAL-MENU`** iff `m_t ≤ 0.5` for **all 15** years (`years_moved_le_0.5pp = 15/15`).
3. **`MIXED`** otherwise.

**Precedence (declared, printed order, D147(i)).** The labels are tested **1 → 2 → 3**; **where both 1 and 2 could
apply, `DUPLICATED-PRIMITIVES` wins** (it is the narrower, licence-granting label the cell exists to detect), and the
coincidence is reported in the level row (`both_applicable = 1`). A level can satisfy both only if the P0-to-frozen
gap is ≤1.5 pp everywhere; that coincidence is recorded, not resolved by preference.

**Aggregate cell label (declared).** `DUPLICATED-PRIMITIVES` iff **all three** levels return it;
`STRUCTURAL-MENU` iff **all three** levels return it; otherwise **`MIXED`**. This aggregation introduces no new
threshold and no level weighting. The aggregate label is the one quoted to the Council and the one that governs
EXP-18's licence (per D144(6): `DUPLICATED-PRIMITIVES` or `MIXED` → EXP-18 may be predeclared; `STRUCTURAL-MENU` →
EXP-18 is VOID and the generator line closes at representation-only).

**Verdict vocabulary — exactly four words, nothing else:** `DUPLICATED-PRIMITIVES`, `STRUCTURAL-MENU`, `MIXED`,
`VOID (CONTAMINATED-BY-DESIGN)`.

## 6. COUNT-BLIND GUARD — enforcement, not intention

Binding (Council block §5.1.5, D147(iv)): **no arm may read `UNIVERSALIZATION_SERIES.csv`, compute a deviation, or
emit an observed-path count.** Enforcement is three-layered and every layer writes evidence to
`results/COUNT_BLIND_AUDIT.json`:

1. **Static AST scan (before any run).** Every `.py` file that the driver imports or executes — `code/run_partprov.py`,
   `code/arms.py`, `code/frozen/sim_v1_6_repair.py`, `code/frozen/sim_v1_3.py` — is parsed with `ast`. The scan
   reports, per file: every string literal containing `UNIVERSALIZATION`; every `open`/`read_csv`/`loadtxt`/`genfromtxt`
   call and its first argument; every reference to the module-level `DATA` path constant; and whether a
   `33`-cell/scored-count construct appears. **The two frozen files are expected to contain exactly one forbidden
   literal each** (the frozen `load_observed_phl_paths`), which is precisely the object the guard exists for: the
   scan records the hit, and layers 2–3 prove the function is never reached. The driver **refuses to run** if the
   scan finds the literal in `code/arms.py` or `code/run_partprov.py` (the cell's own code must be clean), or if any
   file it imports at run time is outside the declared import set.
2. **Runtime open-audit (whole scored path).** `builtins.open` (and `io.open`) are wrapped for the duration of the
   run: every `open` is resolved to an absolute path and appended to the audit log; if any path's **basename** is
   `UNIVERSALIZATION_SERIES.csv` (case-insensitive, any directory), or if it resolves inside
   `10_massification/data/` under that name, the wrapper **raises `ObservedFileAccess` before the OS call is made**
   — nothing is read — the driver aborts with exit code **42** and writes
   `verdict = VOID (CONTAMINATED-BY-DESIGN)`, `refusal = "OBSERVED-FILE-OPEN-ATTEMPT"`. Every arm's panel work is
   inside this wrapper, including the frozen module's own I/O.
3. **Guard self-test (positive control, run in the same process).** Before the arms, the driver attempts
   `open(<resolved observed path>, "rb")` **through the wrapper**: the attempt must be **blocked**, must be recorded
   as `blocked_attempts: 1`, and must leave `observed_file_opened: false`. If the attempt **succeeds**, the guard is
   dead, the run aborts `VOID (CONTAMINATED-BY-DESIGN)` with `refusal = "GUARD-SELFTEST-FAILED"`. The self-test
   therefore proves the guard fires; a passing self-test cannot contaminate anything because the open is intercepted
   before the OS call.

**No-count rule.** The driver computes **no** observed deviation and **no** cell count: it never loads the observed
series, never forms a 33-cell object, and its outputs contain no observed column and no observed-value comparison.
The audit records `observed_file_opened: false`, `observed_file_read_bytes: 0`, `count_computed: false`,
`observed_values_in_outputs: 0`. **Falsifier (from the block, unchanged):** any observed read or any reported
33-cell count → `VOID (CONTAMINATED-BY-DESIGN)`, and EXP-18 loses its licence.

**One disclosed structural fact (declared before the run).** The frozen v1.6 module contains
`load_observed_phl_paths()`, which would open the observed file to obtain the PHL cohort/population path. That
function is **shadowed before any arm runs** by a declared, hashed stub (`arms.declared_demographic_path`) that
reconstructs the demographic input **without any observed read**: `S_path[t] = band_population(primary,t) /
band_share[0]` and `Pop_path[t] = population[t]`, both taken from the **frozen v1.3 synthetic panel** (sha256
`47d4b082…`), i.e. from the frozen block's own declared demographic path. The reconstruction is validated as a
**synthetic identity**: P0 with this input must reproduce the frozen `panel_A10_repaired.csv` PHL rows to a relative
error ≤ `1e-8` on the compared columns (`S-IDENT` guard). If `S-IDENT` fails, the cell aborts
`REFUSED: DEMOGRAPHIC-INPUT-IDENTITY` — no results are written. This keeps the observed file closed for the entire
cell **and** keeps the comparison honest: all three arms sit on the same demographic path, which is the frozen
block's own.

## 7. What the cell does **not** do (closed-claim note)

1. **No observed read, no observed comparison, no count.** Any of the three voids the cell (§6).
2. **No causal and no direction claim.** A label says *which object* produced the share, not *why* the observed
   path took the values it did, and not what would happen to any observed series.
3. **No adoption.** No arm's value is adopted into any generator, parameter table, panel, successor specification or
   level statement. P2 in particular is never adopted (declared).
4. **No re-run / re-score of a delivered cell.** A10 is not re-run "as a verdict", EXP-14's checks C1–C5 are not
   re-scored, `representation_cells.csv` is not recomputed, and EXP-14's `PATH-FAILED` verdict string stands
   permanently. P0 is a **harness comparator**, and its identity with the frozen A10 panel is a *guard*, not a result.
5. **No re-fit, no threshold move, no band.** No parameter, threshold, year, level, arm or verdict word may be
   changed after this file is hashed. The values `1.60/0.03/0.55/0.40/0.20/20.0` are the frozen declarations and are
   not touched; the declared grids of v1.6 are not searched; nothing here is `FITTED`.
6. **No new behavioural parameter.** Count of behavioural parameters is non-increasing: P1 and P2 add **zero**
   numbers; every value is either a frozen v1.6 constant or a frozen v1.3 declared primitive, cited by name.
7. **No C1–C4 reopening; not a test of A5; A3 line stays KILLED; κ stays diagnostic only (D138); `phys_cap` stays
   1.15 (not re-chosen); D63 stays `UNABLE as to cause`.**
8. **`SYNTHETIC` everywhere.** Every number this cell emits is a model output on a synthetic panel; the only
   observed object named anywhere in this file is named in order to be **excluded**.

## 8. Deliverables and determinism

`results/PARTPROV_RESULTS.csv` (per arm × level, plus the aggregate row), `results/PARTPROV_DETAIL.csv` (per arm ×
level × year, 45 cells per arm), `results/CB_AUDIT.json` → `results/COUNT_BLIND_AUDIT.json`,
`results/determinism_run2/` (the complete second run), `FINDINGS.md`, `RUN_MANIFEST.json`, `SHA256SUMS.txt`.
**Determinism:** no RNG anywhere in this cell (the frozen seed `20261120` is used only by the frozen engine, whose
draw count and order are unchanged); floats written `%.10g`; two complete runs must be **byte-identical** on every
result file. If they are not, the cell is `UNDETERMINED` and no verdict is issued.

## 9. Machine-readable declaration block (parsed by the driver; any mismatch refuses to run)

```json
{
  "cell": "EXP-16-PARTPROV",
  "label": "SYNTHETIC",
  "anchor": "SYN00_PHL_LIKE",
  "levels": ["primary", "lower_secondary", "upper_secondary"],
  "year_start": 2010,
  "year_end": 2024,
  "n_anchor_years": 15,
  "tol_dup_pp": 1.0,
  "min_years_within_1pp": 15,
  "tol_struct_pp": 0.5,
  "min_years_moved_le_0.5pp": 15,
  "target": "v13_panel_demand_official_over_cohort",
  "secondary_target": "v13_panel_demand_share",
  "precedence": ["DUPLICATED-PRIMITIVES", "STRUCTURAL-MENU", "MIXED"],
  "aggregate_rule": "unanimous_else_MIXED",
  "verdict_vocabulary": ["DUPLICATED-PRIMITIVES", "STRUCTURAL-MENU", "MIXED", "VOID (CONTAMINATED-BY-DESIGN)"],
  "forbidden_basename": "UNIVERSALIZATION_SERIES.csv",
  "void_exit_code": 42,
  "seed": 20261120,
  "engine_arm": {"bimodal": true, "kappa_link": false, "tier_surv": false, "tier_cfg": null,
                 "inject_upper": null, "w_child_mult": 1.0, "phys_cap": 1.15},
  "frozen_sim_v16_sha256": "9c0e799850fd30bb0b46bb7841e8f301715745a5c73452e7644055122325de56",
  "frozen_sim_v13_sha256": "70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877",
  "frozen_v13_panel_sha256": "47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3",
  "frozen_a10_panel_sha256": "349cf637f1415b7809c17696dea4e842434f846b6be607c8d24047f9f0d1a8c4",
  "frozen_v16_predecl_sha256": "6a554dc033828835431f65be2e5e218833fcdb56220baad8fbe53c3324e78991",
  "s_ident_tol_rel": 1e-08,
  "arms": ["P0", "P1", "P2"],
  "verdict_bearing_arms": ["P1"],
  "report_only_arms": ["P0", "P2"]
}
```
