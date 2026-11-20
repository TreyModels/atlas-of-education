# EXP-13 LOWER-DEF — FINDINGS

**Which of rationing / survival / convention loses the 13.35 pp in the lower-secondary series?**
**Answer: rationing and survival, almost exactly equally — the convention loses none of it. Verdict `JOINT`.**

Council brief 023 §6.3 (D136 #3, rank #3). Predeclaration: `PRE_DECLARATIONS.md`,
sha256 `0ab3a90e3220ef967e64e45f453d2aa7646583146c892fd34165528408f561bd` (hashed before the run).
Arithmetic: `code/run_lower_def.py`, sha256 `0eab319eb23545962b6a7dfc9b7427c4e7a5fa00c5b8998c7325a4197e55aed6`.
Everything below is `SYNTHETIC` panel arithmetic plus one `DERIVED` required value, except the single `OBSERVED`
reference number, which is labelled. **No causal claim, no direction claim, no forecast.**

---

## 1. The one-paragraph answer

The lower-secondary series delivers **0.674073** at 2021 against a requirement of **0.8076** — a gap of
**13.3527 pp**. The chain is exact and multiplicative: `1.10 × 0.783805472329 × 0.7818186593 = 0.674073117881`,
against the panel's stored `completion_uis = 0.6740731179`, difference **1.91 × 10⁻¹¹**. The identity holds in
**53 of 53** scored cells (1973–2025, max error 2.06 × 10⁻¹⁰, tolerance 10⁻⁹), so the falsifier does not fire and the
experiment is **not** `UNDETERMINED`. Under the declared equal-split (Shapley) attribution the gap splits
**rationing 49.30 % / survival 50.70 % / convention 0.00 %** — a 1.40 pp difference, inside the block's 10 pp
`JOINT` window. **`JOINT`.** The two state channels are equally deep (0.7838 vs 0.7818, a **0.20 pp** difference),
and the measurement convention is not a loss at all: `m = 1.10` is a **10 % uplift**. Remove it and the model would
be **19.48 pp** short, not 13.35 — the convention is covering 6.13 pp of the deficit, not causing it.

---

## 2. The chain, checked

| element | value | label | source |
|---|---|---|---|
| `m` (`meas_completion_factor`) | 1.10 | `CONVENTION` | `sim_v1_2.py:133` |
| admission rate at entry, `admitted_official(2018)/cohort(2018)` | 0.783805472329 | `SYNTHETIC` | panel |
| `survival(2021)` | 0.7818186593 | `SYNTHETIC` | panel |
| **chain product** | **0.674073117881** | `SYNTHETIC` | this experiment |
| panel `completion_uis(2021)` | 0.6740731179 | `SYNTHETIC` | panel |
| absolute difference | **1.91 × 10⁻¹¹** | — | tolerance 10⁻⁹ → **pass** |
| required 2021 lower | 0.8076 (80.76) | `DERIVED` | `76.6391 / 0.949 = 80.7577` → 80.76 (V12/D133) |
| **gap** | **13.3527 pp** (`ln` gap 0.180728) | `DERIVED` | `100 × (0.8076 − 0.674073)` |

The block's 6-decimal rendering reproduces to `1.10 × 0.783805 × 0.781819 = 0.674073005` (difference
1.12 × 10⁻⁷, print rounding, tolerance 5 × 10⁻⁷ as declared in §2 of the predeclaration). It is a display check,
not the identity test.

**The identity is not a coincidence of one year.** For every year with a lagged entry cohort (1973–2025) the
reconstruction equals the stored value: 53 cells, 0 failures. The chain is the accounting executed.

---

## 3. Full decomposition table

Declared attribution D1 (predeclaration §5): the convention is held at its declared value (`m* = m`, because a
constant applied to every cell cannot be moved by a lower-series repair and choosing it against a level bar is
`FAIL-RE-FIT` under D134); the residual required log product is split equally between the two state factors,
`a* = s* = exp(½ ln(0.8076/1.10)) = 0.856844`; contributions `c_i = ln(x_i*/x_i)`; shares `c_i / G_log`.

| factor | realised | required (D1) | log contribution | share of the 13.35 pp | share, alternate rule D2 | single lever that alone closes the gap | reachable under the declared rules? |
|---|---|---|---|---|---|---|---|
| **convention** `m` | 1.100000 | 1.100000 | **0.000000** | **0.00 %** | 16.29 % | `m* = 1.317899` | **`ARITH-ONLY`, declared-excluded** — fitting `m` to a level bar is `FAIL-RE-FIT` (D134); the convention question is EXP-15's |
| **rationing** `adm/cohort` | 0.783805 | 0.856844 | **0.089095** | **49.30 %** | 41.64 % | `a* = 0.939069` → entry coverage `0.816582` | **yes** — `REACHABLE-BY-CAPACITY` (realised entry coverage 0.681570) |
| **survival** | 0.781819 | 0.856844 | **0.091633** | **50.70 %** | 42.07 % | `s* = 0.936689` | **no** — `UNREACHABLE-UNDER-DECLARED-LAW`: `surv_max = 0.91 < 0.936689`; the channel's ceiling is **0.784589**, i.e. **2.3011 pp short** of 80.76 |

`c_convention + c_rationing + c_survival = 0.180728 = G_log` (sum residual 5.7 × 10⁻¹⁴). Verdict:
top 50.702 %, second 49.298 %, delta **1.4043 pp** ≤ 10 pp → **`JOINT`**. Under the block's literal test order
(`X-CARRIED` if ≥ 50 %) the label would read **`SURVIVAL-CARRIED`** at 50.70 %; both labels are reported
(`LOWER_DEF_RESULTS.csv`, `verdict_label` and `verdict_label_literal_order`) because the block states no precedence
(predeclaration §6.2). **The two labels lead to the same action, for the reason in the survival row: the survival
channel physically cannot close the gap under the declared law, so "survival-carried" cannot be read as
"fix survival only".**

The `D2` column weights each factor by `|ln x|`, so it treats the `m > 1` uplift as a positive term and is **not** a
share of the gap in the same sense; it is reported only so the Council can see that the ordering
(survival ≈ rationing ≫ convention) does not depend on D1's required-state split.

### 3.1 The mechanism, in the declared rules (arithmetic, not causation)

Both loss terms are functions of **one** declared object — adequate-place coverage `seats/cohort`:

- **the gate**: `admission = min(phys_cap·seats, overage_cap·cohort)/cohort`. At the 2018 entry cohort the first term
  binds (`gate_binding_term = phys_cap*seats`, gate identity error **2.05 × 10⁻¹¹**), so
  `admission = 1.15 × 0.681570 = 0.783805` **exactly**;
- **the survival law**: `surv = 0.91 × exp(−0.55 · max(0, C/seats − 1))`. In 2021 `C/seats = 1.276040`, so
  `Q = 0.859141` and `surv = 0.781819`.

The chain therefore reads `0.8076 vs 1.10 × 1.15·cover(2018) × 0.91·Q(cover(2021))`. The 13.35 pp is lost through
the declared capacity path, entering **twice**. This is an identity of the declared rules, not a claim that places
cause completion.

---

## 4. What is identified and what is not (this matters for how the verdict is read)

**Identified, no allocation rule needed:**

1. The convention is **not** the loss: `m = 1.10 > 1`. Dropping it gives `0.612794` and a **19.48 pp** gap — it would
   widen the gap by **6.13 pp**. There is no reading of the chain in which the convention removes 13.35 pp.
2. The two state channels are **equally deep to 0.20 pp** (0.783805 vs 0.781819). Neither dominates.
3. **Asymmetric feasibility** (the decision-relevant object): the gate can close the gap alone (needs entry coverage
   0.8166 vs 0.6816 realised); the survival channel **cannot**, because `surv_max = 0.91` caps it at 78.46 pp,
   2.30 pp below the requirement, however the quality index is re-declared within its own rule.
4. The shortfall is **not local to 2021** — it is a path phenomenon that closes: 2017 **+30.48 pp**, 2019 +23.01,
   2021 **+13.35**, 2022 +7.84, 2023 +1.72, 2024 **−5.11**, 2025 −11.89 (negative = the model is above the
   requirement). The model's own lower series **crosses 80.76 between 2023 and 2024**.

**Not identified (declared, not repaired after the fact):** the *split* of the required product between rationing
and survival. One equation, three unknowns: any pair `(a*, s*)` with `a*·s* = 0.8076/1.10` reproduces the
requirement. D1 fixes it at ½/½, which is a **declared normalisation, not an estimate**. Consequences, reported
in the results file:

- the label is `JOINT` for split weight `w_a ∈ [0.466649, 0.525137]` and `X-CARRIED` outside it
  (`joint_split_weight_interval`); at `w_a = 0.25` shares are 92.04 / 7.96, at 0.75 they are 6.55 / 93.45;
- the share **difference** is `|ln s − ln a| / G_log`, so it scales with the gap: at the 13.35 pp cell it is
  1.40 pp; at a small gap the same rule returns `X-CARRIED`, and at very small gaps a factor's share can exceed
  100 % or turn negative (flagged per year in `LOWER_DEF_DETAIL.csv`, `share_rule_note`; no attribution is
  reported where the gap is negative).

**So: the point shares are conditional on the declared split; the near-even split and the feasibility asymmetry
are not.** The verdict `JOINT` is the frozen rule's output at the declared normalisation; it is not presented as an
estimate of a population quantity.

---

## 5. What the V16-REPAIR predeclaration must fix first (the lower series)

1. **Declare the target's provenance in one sentence and never swap it.** `80.76` is `76.6391/0.949` — an
   *internal-consistency* requirement derived from the model's own delivered upper 2024, not an external standard.
   The `OBSERVED` PHL 2021 value is **80.896**, which sits **0.136 pp above** the requirement. If V16 scores against
   the observed number, it must say so, with the observed cell cited; the two must not be used interchangeably.
2. **Declare both lower-series channels together, because they are one object.** The gate is
   `1.15 × cover(entry)` and the survival law is `0.91 × exp(−0.55(1/cover − 1))`. A predeclaration that moves one
   and not the other reproduces the same defect through the other channel. If V16 intends a single-channel repair,
   the only arithmetically available channel is the **gate** (entry coverage 0.6816 → ≥ 0.8166), and that must be
   declared before the run.
3. **Freeze `m = 1.10` and put the convention out of scope.** `m = 1.317899` would "close" the gap by construction.
   That is target-fitting, it is `FAIL-RE-FIT` under D134, and the convention object belongs to EXP-15 CONV-REG.
   The lower-series repair must be scored with `m` untouched.
4. **Declare the scoring years and the path, not a single year.** The model's own lower series crosses 80.76 between
   2023 (+1.72 pp) and 2024 (−5.11 pp). A repair scored only at 2024 or 2025 **passes without changing anything**;
   the requirement is stated for **2021**, so 2021 must be in the scored set and the full path reported.
5. **Declare the survival ceiling explicitly.** Any repair that proposes to reach 80.76 by re-declaring
   `surv_max` (or the quality mapping) must show arithmetic that reaches it: `surv_max = 0.91` caps that channel at
   78.46 pp, 2.30 pp short. A proposal that does not clear 80.76 through its declared channel is not a repair of
   this defect.
6. **Declare the clip boundary.** `completion_uis` is clipped to `[0, 1]`. In `primary`, `m × completion_cohort`
   exceeds 1.0 in 2024–2025, so the stored value is `1.0` and the identity **cannot** reproduce it (error 0.0121) —
   that is a declared clip, not an accounting failure. No clipped cell may be used as an exact identity check.
   `lower_secondary` never clips (max `m × completion_cohort` = 0.9265), which is why the verdict cell is clean.

---

## 6. Secondary analyses (declared non-verdict-bearing)

**Shortfall localisation** (`LOWER_DEF_DETAIL.csv`, same required 0.8076 throughout): +30.48 pp (2017), +27.05
(2018), +23.01 (2019), +18.45 (2020), +13.35 (2021), +7.84 (2022), +1.72 (2023), −5.11 (2024), −11.89 (2025).
The shortfall is **local to the pre-2024 path**, not to the type: the model's own trajectory crosses the requirement
in 2023–24. Only 2024 and 2025 are at or above it.

**All 30 country types, 2021** (`LOWER_DEF_TYPES.csv`, common declared yardstick 0.8076 — a *benchmark*, not a
requirement derived for those types): **27 of 30** are short, **3** are at or above (`NO-SHORTFALL`), and the chain
identity holds in **30 of 30** (0 failures). Among the 27, the frozen rule returns **16 `JOINT`** and
**11 `SURVIVAL-CARRIED`**. The label distribution moves with the size of each type's gap because the D1 share
difference is `|ln s − ln a| / G`; it is context, not a verdict, and no type is re-scored.

---

## 7. Honest limits

1. **Decomposition depends on the declared chain.** The result is a statement about
   `m × admission(t−3) × survival` — the chain the generator executes. If the repair changes the chain (for example
   by carrying survival into the entry year or by using admission including over-age intake), the decomposition is
   the wrong accounting and must be re-predeclared. It does not "fail"; it stops applying.
2. **The required state is not identified** (§4). The ½/½ split is declared. A Council that prefers a different
   split gets different shares — 92/8 or 7/93 at the extremes — and the same two substantive facts: the convention
   is not the loss, and the survival channel cannot close the gap.
3. **Synthetic.** The panel is `SYNTHETIC`; the 30 types share one declared supply rule parameterised by two traits
   (`cap0_c`, `dshift_c`). Nothing here is an observed Philippine measurement except the single labelled 80.896.
   There is **no observed admission-rate or survival series for PHL on disk**, so this decomposition cannot be
   replicated on observed data. That data is **HELD, not fabricated** (DepEd/CHED seats-vs-enrolment, capacity
   utilisation, a measured transition/queue series).
4. **One verdict cell.** The verdict is the 2021 cell, the year the requirement is stated for. The path and the
   30-type results are context and cannot move it.
5. **`0.8076` is derived from the model's own output** (`76.6391/0.949`), so the "gap" is an internal-consistency
   gap. It is not evidence about the Philippines, not a policy target, and not a forecast. V15's necessary condition
   stands untouched.
6. **No causal or direction claim.** Nothing here says that expanding lower-secondary places, or improving quality,
   would raise completion; the arithmetic locates channels in a declared rule. D63 remains `UNABLE as to cause`; the
   phase verdict (PARTIAL/DESCRIPTIVE/EQUIVALENT, scaling `FAIL`) is untouched; EXP-7's `ENDPOINT-ONLY 9/33` and
   v1.5's verdict are not re-scored.

---

## 8. Reproducibility

```
python code/run_lower_def.py --outdir results
python code/run_lower_def.py --outdir results/determinism_run2
```

No RNG, no clock, no network, no environment-dependent ordering. Two independent executions produce
**byte-identical** outputs — `LOWER_DEF_RESULTS.csv` `10d44743…`, `LOWER_DEF_DETAIL.csv` `277c613c…`,
`LOWER_DEF_TYPES.csv` `dff97b9f…`, `INPUT_HASHES.json` `a8231e52…` (run 2 stored in
`results/determinism_run2/`, compared in `RUN_MANIFEST.json`). Inputs were read-only; nothing outside
`10_massification/extensions/lower_def_2026-11-20/` was written.
