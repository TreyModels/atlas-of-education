# PRE_DECLARATIONS — EXP-12 FLOOR-CLOSE

**`LABEL: SYNTHETIC`** — every panel number in this experiment comes from the frozen synthetic
generator panel. No observed data series is read, compared or scored here.

**Experiment:** EXP-12 **FLOOR-CLOSE** — *what closes the model's floor gate: places, cohort, or the
declared `phys_cap = 1.15` crowding allowance?*
**Source:** Council brief 023, `08_council/brief_023/SYNTHESIS_023.md` §6.2, EXP-12 block (D136 #2,
rank **#2**); scope note D133 (`08_council/DECISIONS.md`).
**Worker:** WORKER FC. **Date frozen:** 2026-11-21.
**Status at freeze:** `PRE-DECL-FROZEN` — this file is hashed (`PRE_DECLARATIONS.sha256`) **before**
`code/run_floor_close.py` is first executed. No result file exists at the moment of the freeze.

This is a **descriptive accounting decomposition of a declared-assumption simulator**. It makes **no
causal claim** and **no direction claim**. It is read-only on the frozen panel: **no re-fit, no new
parameter, no `phys_cap` change in the model, no counterfactual model re-run**. It does not reopen
CEIL-ATTRIB or A3-S and does not touch the demand line.

---

## 1. The EXP-12 block, verbatim

Transcribed from `08_council/brief_023/SYNTHESIS_023.md` lines 436–472 (whole-file sha256
`39e666cffbe3950d43460ba177a36501d53fd0ec8083cd5c9abcbd1c7aeed44c`). The splice is programmatic:
`code/build_predeclarations.py` reads the named source lines and inserts them unchanged, and refuses
to build if the source hash has moved. **Every definition, bar, threshold and falsifier used below is
transcribed from here. None is invented, none is tuned.**

```markdown
<<<VERBATIM_EXP12_BLOCK>>>
```

**Scope note, D133, verbatim** (`08_council/DECISIONS.md`, row D133, whole-file sha256
`15c564cffb1d9994386873b7daf9793407745da5477d437ef3adcb9efba8771c`):

> <<<VERBATIM_D133_SCOPE>>>

---

## 2. Frozen inputs (read-only; declared hashes)

| input | path (programme-root relative) | sha256 | role |
|---|---|---|---|
| frozen panel | `10_massification/extensions/synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv` | `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac` | **primary** — `seats`, `cohort`, `demand_official`, `admitted_official`, `seat_coverage`, `congestion_q`; 30 types × 4 levels × 56 years = 6 720 rows |
| parameter register | `10_massification/extensions/synthetic_2026-11-20/generator_v1_2/PARAMS.md` | `0d619781c4e059f54cf771fb385475f5f939dceced5036e8a21b6e07a2b315e3` | `phys_cap = 1.15` (DECLARED), `overage_cap = 1.05` (CONVENTION), capacity rule §4 |
| generator code | `10_massification/extensions/synthetic_2026-11-20/generator_v1_2/code/sim_v1_2.py` | `61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c` | `sim_v1_2.py:587` `phys = min(P["phys_cap"] * seats[L], P["overage_cap"] * C[L, t])` |
| Council brief | `08_council/brief_023/SYNTHESIS_023.md` | `39e666cffbe3950d43460ba177a36501d53fd0ec8083cd5c9abcbd1c7aeed44c` | definitions, thresholds, falsifier (§1 above) |
| Council decisions | `08_council/DECISIONS.md` | `15c564cffb1d9994386873b7daf9793407745da5477d437ef3adcb9efba8771c` | D133 A10/D62 scope note |

No v1.5 file is read: the EXP-12 block names none. No observed series, no held data, no external
request, no web access.

---

## 3. Operational definitions (frozen before the run)

### 3.1 Cells and the gate

- A **cell** is `(country, level)`: 30 country types × 4 levels = **120 cells**, 1970–2025.
- `p_off(t) = admitted_official(t) / demand_official(t)`, clipped to `[0, 1]`. The gate **binds** at
  `t` iff `p_off(t) < 1 − 1e-12`; it is **open** iff `p_off(t) = 1` (same guard). The `1e-12` guard
  only absorbs the panel's 10-significant-digit CSV rounding; it never decides a substantive case.
- `capacity(t) = min(phys_cap · seats(t), overage_cap · cohort(t))`, with `phys_cap = 1.15`
  (DECLARED) and `overage_cap = 1.05` (CONVENTION), per `PARAMS.md` §4 and `sim_v1_2.py:587`.
- `p_off` is **derived** from `admitted_official / demand_official` exactly as EXP-8 GATE-LOCUS
  derived it (`gate_locus_2026-11-20/code/run_gate_locus.py`, `cell_records`); the panel has no
  `p_off` column.

### 3.2 Closure year

Scanning years in ascending order, the **closing year `t*`** is the **first year with `p_off = 1.0`
after ≥ 3 binding years** (binding years counted strictly before `t*`). The **last binding year
`t_b`** is the last year before `t*` with `p_off < 1`; because `t*` is the first open year,
**`t_b = t* − 1`**, and the script asserts this for every closing cell.

Cells with no such year are **non-closing** and are reported with a reason:

- `RIGHT_CENSORED_STILL_BINDING` — ≥ 3 binding years exist but the gate is still binding in 2025;
- `NEVER_BOUND_3_YEARS` — fewer than 3 binding years in the whole window (these are the cells that
  are open from the start, mostly upper/tertiary; they never had a "floor gate" to close).

Rationale for the ≥ 3 rule: a gate that is open in the first panel years has not *closed*; the block
requires ≥ 3 binding years before closure.

### 3.3 The log margin and the decomposition target

`m(t) = ln( capacity(t) / demand_official(t) )`. Closure means `m(t_b) < 0 ≤ m(t*)`.

The decomposition target is

**Δ = ln( capacity₁.₁₅(t\*) / demand(t\*) ) − ln( capacity₁.₀(t_b) / demand(t_b) )**,

where `capacityᵖ(·)` is the declared capacity rule evaluated with `phys_cap = p`.

**Why the reference shift (declared here, arithmetic only).** `phys_cap` is a constant (`1.15`) in
every row of the frozen panel, so the *observed* within-cell change `ln phys_cap(t*) −
ln phys_cap(t_b)` is identically **zero**. A pure year-to-year reading of term (iii) would therefore
make the allowance leg zero in **every** cell, contradicting the block's requirement that it be
identically zero **only** in cells where `1.05·cohort` is the smaller term. The only reading
consistent with that sentence — and with the block's §6 statement that "the decomposition already
answers the question arithmetically" without a `phys_cap = 1.0` re-run — is that the allowance enters
as the declared **level shift from the no-crowding reference `phys_cap₀ = 1.0` to the declared
`phys_cap = 1.15`**, while the seats and cohort/demand factors move from `t_b` to `t*` as the block
states. Both endpoints are evaluated from frozen columns under the declared rule: this is arithmetic
on the frozen panel, **not** a model run, **not** a new cell, and **not** a change to the model's
`phys_cap` (which remains 1.15). §6.1 below reports the pure observed change as a non-verdict-bearing
sensitivity, where the allowance term is 0 by construction.

### 3.4 The three factors

| | factor | start value (at `t_b`) | end value (at `t*`) | enters |
|---|---|---|---|---|
| **(i) PLACES** | `seats` | `seats(t_b)` | `seats(t*)` | capacity, `p·s` branch |
| **(ii) DEMAND/COHORT** | (`cohort`, `demand_official`) | (`cohort(t_b)`, `demand(t_b)`) | (`cohort(t*)`, `demand(t*)`) | capacity, `1.05·c` branch; denominator `d` |
| **(iii) ALLOWANCE** | `phys_cap` | `1.0` (no-crowding reference) | `1.15` (declared) | capacity, `p·s` branch only |

Factor (ii) carries `demand_official`, the denominator of the object `capacity/demand`; its
demographic driver is `cohort`, and on the cohort branch `cohort` also enters capacity directly
through `1.05·cohort`. The pair therefore moves together as one factor; there is no fourth factor.
This is the block's factor (ii) "`log cohort`" operationalised on the gate object it names.

### 3.5 Value function

`f(p, s, c, d) = ln( min(p·s, 1.05·c) / d )` — the declared capacity rule, evaluated on the binding
branch of the `min`, over the gate's demand denominator.

### 3.6 Equal-split (Shapley) attribution

3 factors → `3! = 6` orderings, each weighted **1/6**. For each ordering the factors are switched
from their start to their end values one at a time, and the change in `f` at each switch is credited
to the factor just switched. The attribution of factor `i` is the average of its marginal
contributions over the six orderings:

`φ_i = (1/6) · Σ_{orderings} [ f(S_k ∪ {i}) − f(S_k) ]`.

**Efficiency is exact**: `Σ_i φ_i = f(end) − f(start) = Δ`. The script asserts this identity to a
relative `1e-9` for every closing cell.

**Share:** `σ_i = φ_i / Δ`. Because the gate is closed at `t_b` and open at `t*`, `Δ > 0` for every
closing cell (asserted); `Δ` may be small, but it is strictly positive by the closure definition.

**Binding-branch reporting rule.** A cell is flagged `COHORT_BRANCH` iff `1.05·cohort(t*) <
1.15·seats(t*)` at the closing configuration; in such a cell the `phys_cap` term is identically zero
by the block's own rule, the cell is **reported separately and cannot carry the allowance leg**
(`σ_allowance := 0`). A cell that visits **both** branches across the six orderings is flagged
`BRANCH_SWITCH`; its Shapley terms remain exact and may be **negative**, because the `min` can make
`f` non-monotone. Negative shares are reported as computed, never clipped.

**Cell label.** A factor "carries" a cell iff `σ_i ≥ 0.5`. At most one factor can exceed 0.5 because
the shares sum to 1; if two are exactly 0.5, the block's listed order
(**ALLOWANCE > CAPACITY > DEMAND**) resolves the tie. A cell with no factor ≥ 0.5 is labelled
`MIXED`.

### 3.7 Panel verdict (bars verbatim from the block)

With `N` closing cells:

- **`ALLOWANCE-CARRIED`** iff `#{σ_allowance ≥ 0.5} / N ≥ 0.5`;
- else **`CAPACITY-CARRIED`** iff `#{σ_places ≥ 0.5} / N ≥ 0.5`;
- else **`DEMAND-CARRIED`** iff `#{σ_demand/cohort ≥ 0.5} / N ≥ 0.5`;
- else **`MIXED`**.

The explicit threshold rule governs. The **plurality label** (the most frequent per-cell label) is
reported as a diagnostic; if it ever differs from the threshold verdict, both are reported and the
**threshold verdict is the verdict**.

### 3.8 Falsifier

`N < 30` → **`UNDETERMINED`**, and the A10/D62 statement is then marked **untested, not confirmed**.
`N` is fixed by the frozen panel alone; no cell may be added, dropped, or redefined after results.

### 3.9 Anchor cell

`SYN00_PHL_LIKE × primary` is reported separately so that V10 can be checked against the panel:
closure year, `seat_coverage` at closure, the `1.15·seats` / `1.05·cohort` / `demand` values, the
binding branch at closure, and its factor shares. V10's recorded values (closure 2019; `seat_coverage`
0.8722) are a consistency check, **not** a new result.

---

## 4. Closed-claim check

1. **Read-only on a frozen panel.** The panel is opened once and never written; hashes are verified
   before any computation.
2. **No re-fit, no new parameter.** No parameter is estimated, tuned or selected. `phys_cap = 1.15`
   and `overage_cap = 1.05` are read from `PARAMS.md`, not inferred.
3. **No counterfactual model re-run.** The `phys_cap = 1.0` reference is evaluated **arithmetically**
   from frozen `seats`/`cohort`/`demand` columns under the declared rule; the simulator is not
   re-executed, so no new model cell is created. The block explicitly requires this (§6).
4. **No causal/direction claim.** The shares are an accounting identity on a declared simulator;
   they are not an estimate of any real schooling system, and they license no statement about
   causality, policy, or the direction of any real-world process.
5. **Does not reopen CEIL-ATTRIB or A3-S; does not touch the demand line.**
6. **A10/D62 restatement** only as far as the block's §2 licenses: `ALLOWANCE-CARRIED` → the
   disposition is restated as conditional on a declared crowding convention, no capacity-mechanism
   claim may rest on the floor until a measured places/PTR series exists (**HELD**), and the repair
   must report the floor's dependence on `phys_cap` as a sensitivity. `CAPACITY-CARRIED` → the A10
   statement survives at the floor. `DEMAND-CARRIED` → the model's floor universalization is
   demographic. `MIXED`/`UNDETERMINED` → no restatement beyond recording the outcome.
7. The A10/D62 claim is a **model-side** statement about the synthetic generator; nothing here
   validates or invalidates any observed-data capacity mechanism.

---

## 5. Determinism

No RNG, no clock, no environment-dependent ordering. Cells are sorted by the declared level order
(`primary`, `lower_secondary`, `upper_secondary`, `tertiary`) then `country_id` then `year`;
orderings are enumerated from a fixed tuple; floats are written `%.12f`; files are LF-only. The run
is executed **twice**, into `results/` and `results/determinism_run2/`; the three CSVs and the panel
JSON must be **byte-identical**. Any difference is a `DETERMINISM-FAIL`.

---

## 6. Non-verdict-bearing sensitivities (declared now; reported separately, never scored)

### 6.1 S1 — pure observed change

`Δ_obs = m(t*) − m(t_b)` with `phys_cap = 1.15` at both endpoints. Under this reading the allowance
term is **identically zero** (the allowance is a constant), and all of `Δ_obs` is attributed to
places and demand. Reported to make the reference-shift choice in §3.3 transparent and to show what
the observed year-to-year movement attributes. **Never verdict-bearing.**

### 6.2 S2 — capacity only, demand held at `t_b`

`Δ_cap = ln( capacity₁.₁₅(t*) / capacity₁.₀(t_b) )` with `demand` fixed at `d_b`, attributed with the
same three-factor Shapley rule. Non-verdict-bearing.

### 6.3 S3 — binding-branch additive identity

In cells whose every visited configuration is on the places branch,
`φ_allowance = ln(1.15)`, `φ_places = ln(s*/s_b)`, `φ_demand = −ln(d*/d_b)` **exactly**. The script
asserts this against the Shapley values in those cells. Non-verdict-bearing check of the arithmetic.

### 6.4 S4 — closure-definition sensitivity

Recompute the closing-cell count with (a) the open bar `p_off ≥ 1 − 1e-9` and (b) **≥ 3 consecutive**
binding years. By §3.2 these must coincide (`t_b = t* − 1` and the run length ending at `t_b` is
≥ 3 whenever the cumulative count is ≥ 3); the check documents the coincidence rather than choosing
between definitions. Counts only; non-verdict-bearing.

---

## 7. No-threshold-change rule

Every definition, bar, threshold, verdict word and falsifier above is frozen by this file's sha256
before the first execution of `code/run_floor_close.py`. **No threshold may move after results.** A
post-freeze change to a definition, a bar, a cell rule or a factor boundary is `FAIL-RE-FIT` and
voids the run — including any change made to produce a preferred verdict. The script refuses to run
if this file's hash does not match the frozen constant in `code/run_floor_close.py`, or if the panel
hash does not match `14729c51…fac5ac`.
