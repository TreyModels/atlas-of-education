# EXP-17 JOINT-COVER — FINDINGS

**One line.** In the declared law's own terms, **yes**: **one** coverage path — the panel's own, moved by a single
number — satisfies both lower channels at the required value. There is exactly **one** such uplift,
**`λ* = 1.114650`**, applied at **both** the entry year (2018) and the completion year (2021); it takes the declared
chain from **0.674073** to the required **0.8076**. Verdict: **`SINGLE-LEVER-IDENTIFIED`**. The falsifier passes at
**1.03e-12** (tolerance 1e-9). **No λ is adopted**, and "satisfies the equation" is not "is achievable" — see §5 of
the predeclaration and §8 below.

**Labels.** The panel and everything computed from it = `SYNTHETIC`. The requirement `0.8076` = `DERIVED`
(`76.6391/0.949` — the model's own internal-consistency object, **not** an observed or policy target). The observed
PHL reference `80.8960494995` = `OBSERVED`, printed once, used nowhere in the verdict. **No causal claim and no
direction claim is made anywhere below.** Nothing here says that building places raises completion, in the model's
world or in any other.

---

## 1. The answer, with its numbers

The declared lower-secondary chain is `m · gate(2018) · survival(2021)`. At the frozen panel's own coverage path it
delivers **0.6740731179**, which is **13.3526882 pp** short of the required **0.8076** — D142's gap, with the
chain itself reconstructed to **1.03e-12**. Both channels are functions of the *same* object, `coverage = seats/cohort`: the gate rises with
coverage, congestion falls with it, and survival rises with coverage. So the question was whether **one** uplift on
that one object can satisfy both channels at once, or whether the requirement needs two independent moves.

It needs one:

| quantity | value | label |
|---|---|---|
| **`λ*`** | **1.11465019198434** | `DERIVED` — required state, **not adopted** |
| implied coverage, entry year **2018** | **0.7597121046** (+7.8142 pp over the panel's 0.6815700) | `DERIVED` |
| implied coverage, completion year **2021** | **0.8735231987** (+8.9848 pp over the panel's 0.7836747) | `DERIVED` |
| implied gate **`a`** | **0.8736689202** | `DERIVED` |
| implied survival **`s`** | **0.8403432939** | `DERIVED` |
| product `m·a·s` | **0.8076** (residual 7e-15) | `DERIVED` |
| implied `phys_cap · coverage` at entry | **0.873669** (= `a`, the `phys_cap` branch binds) | `DERIVED` |
| implied seats, 2018 / 2021 | **1 850 382 / 2 075 666** (+190 326 / +213 498; +11.465 %) | `DERIVED`, `SYNTHETIC` basis |
| law's maximum over `[0.5, 2.0]` | **1.051050** (= `m·1.05·0.91`, reached for `λ ≥ 1.339618`) | `DERIVED` |
| gap closed by the one lever | **13.3527 pp** (−0.18073 in logs) | `DERIVED` |
| observed reference (context) | 0.808960494995 → `λ` 1.1158023; **non-verdict-bearing** | `OBSERVED` |

The implied seat counts are **model-internal** objects (the panel's own `seats` column scaled by λ\*). They are not
a classroom count, not a budget, and not an estimate of anything in the Philippines.

---

## 2. What the two numbers say about the two channels

This is the substantive result, and it is arithmetic about the **declared law**, not an empirical claim.

- **At the realised coverage**, survival would have to be **0.936689** to close the gap on its own — above the
  law's ceiling **`surv_max` = 0.91** (D140/EXP-13: `UNREACHABLE-UNDER-DECLARED-LAW`, 2.3011 pp short). The gate
  alone would need **0.939069** (EXP-13's `a*`; reproduced here to 5e-11 as a by-product).
- **At the required coverage**, survival needs only **0.840343** — comfortably **below** the 0.91 ceiling — and the
  gate needs only **0.873669**, below the 0.939069 it needed when survival was held fixed. Neither channel is asked
  for an impossible value once they move together.

So D140's law statement "survival cannot close" is **not absolute**: it holds *at the realised coverage* and stops
holding once the coverage object moves — which is exactly the condition D140 C-3 attached to it ("must be re-tested
if the coverage object changes"). EXP-17 is that re-test, and it returns the opposite answer at the required
coverage. **This is a statement about the declared law.** It is not evidence that raising coverage anywhere would
raise survival, and it is not a claim that the coverage is achievable.

---

## 3. The checks that could have overturned the verdict

| check | result | what it rules out |
|---|---|---|
| **Falsifier** (block clause 5): `λ = 1` reproduces the panel's 2021 `completion_uis` to 1e-9 | **PASS**, abs error **1.0258e-12** (chain 0.6740731179 vs panel 0.6740731179); survival diagnostic error **4.15e-11** | that the accounting executed is not the declared one — wrong lag, wrong `phys_cap`, wrong survival law |
| **Two independent root-finders** (bisection on the grid bracket; Newton on the analytic derivative) | **1.11465019198434** vs **1.11465019198435**; **\|Δ\| = 5.77e-15** (tolerance 1e-9) | a root that the solver cannot pin |
| **Monotonicity audit** (grid, N = 6001, step 2.5e-4) | **0** decreasing intervals | a second, undiscovered root or a non-monotone law |
| **Root count** | **1** sign change, **0** exact zeros, **0** plateau intervals | `MULTIPLE` |
| **Law maximum** | grid max **1.05105** = analytic `m·1.05·0.91` = **1.05105** | "no root" being confused with "root outside range" (block's requirement) |
| **Bracket ends** | `F(0.5) = 0.167063`, `F(2.0) = 1.051050` | the target sitting outside the bracket in either direction |
| **Capacity-regime scope check** | `λ* = 1.114650 < λ_demand = 1.218125` | the implied gate being an artefact of an equation that ignores demand: at the root the capacity term still binds (implied 0.873669 < the panel's own 2018 demand share 0.954773) |
| **Clip inactivity** | survival clip `[0.02, 0.995]` never binds on the bracket (`s` ranges 0.3875 → 0.9100) | a clipped value being read as the law |
| **Resolution pretest** (D147 rule ii) | `dG/dλ = 0.783805 > 0`, `dS/dλ > 0`, finite difference over ±0.01 = **2.36e-02** | the leg being `UNFIRABLE-BY-DESIGN` |

The structure of the answer is not a surprise and is disclosed as such: `PRE_DECLARATIONS.md` §7 records, **before
the run**, that `F` is non-decreasing in λ, strictly increasing below `λ_cap = 1.339618`, and flat at `1.05105`
above it — so the law admits at most one isolated root. The information this cell adds is **the number** `λ*`, the
implied `(a, s)` pair, the implied coverage and seats at both years, and the falsifier — not the label.

---

## 4. What this means for V16's lower declaration (D140 / EXP-13)

The block's own consequence clause applies without amendment: the lower defect becomes a **coverage requirement
with one number**; **the successor declares a coverage path, not two channels**; and D140's split-language is
**superseded by "one object, two channels, one required state"** — with the six-decimal shares **still reported**
and **still unidentified as separate levers** (the weight interval `[0.466649, 0.525137]` is untouched, and
**"survival loses 50.7 %" remains barred**).

Three consequences the successor should carry, each with its label attached:

1. **The lower declaration has a parameter-shaped object after all — but it is a *required state*, not a
   parameter.** `λ* = 1.114650` with the `DERIVED` target `0.8076` attached is what a successor may cite as
   `REQUIRED-STATE (EXP-17)`. It may **not** be written into a `PARAMS` block, rounded into a declared value, or
   described as calibrated, estimated, achieved or achievable (§8 of the predeclaration; any such use is a
   `FAIL-RE-FIT`-class defect).
2. **"Fix survival only" stays barred, and is now barred for a better reason.** It was barred because `s* = 0.9367`
   exceeds the law's ceiling. It is *still* barred — the lever is coverage, and survival follows it. What changes is
   that survival is no longer the channel that cannot move: at the required coverage it sits at **0.8403**, inside
   the declared law.
3. **The requirement is a two-year object, not a 2021 number.** The same uplift must hold at the entry year
   (2018: coverage 0.6816 → 0.7597) **and** the completion year (2021: 0.7837 → 0.8735). A successor that moves only
   the completion-year coverage does not satisfy this solution; the block's equation moves both, by construction.

---

## 5. What this means for EXP-19's proxy bound

EXP-19 was written to ask whether the **required coverage** can be bounded by anything observed on disk, comparing
a classroom→places interval (class-size norms {40, 45, 50}, none adopted) against "EXP-17's required coverage — the
`λ`-implied `seats/cohort` at both years". Those two numbers now exist:

- **entry year 2018: `seats/cohort` = 0.759712**
- **completion year 2021: `seats/cohort` = 0.873523**

Three things follow, and they are all scope statements rather than results:

1. **EXP-19 must test the interval against *both* years, and report them separately.** They differ by 11.4 pp; a
   single "required coverage" number would misstate one of them. The 2021 value is the binding one for the required
   product; the 2018 value is what the gate sees.
2. **The observed-reference variant does not move the target materially.** Solving against the observed
   `0.808960494995` gives `λ = 1.115802`, i.e. required coverage **0.760497 / 0.874426** — **+0.079 pp / +0.090 pp**
   above the derived-requirement values. That is the entire consequence of the +0.136 pp provenance delta (D142
   C-4). EXP-19's interval test is therefore not sensitive to *which* of the two references it is handed at that
   margin — but it **must still state which it used**, and it must not adopt the reference as the requirement.
3. **The implied seats are `SYNTHETIC`-basis.** `λ*` implies +190 326 places at 2018 and +213 498 at 2021 *relative
   to the panel's own seats path*. EXP-19 converts classrooms to places in the observed world; those two objects are
   not the same thing and may not be equated. EXP-19's own falsifier (conflicting on-disk counts → `PROXY-SILENT`)
   is unaffected by this cell.

---

## 6. Scope: where `λ*` does **not** carry (D143 (viii) / D147 scope-inheritance)

- **It does not carry to the A10 repaired arm's lower cell.** The equation was solved on the frozen **v1.2** panel,
  where the 2018 gate is **capacity-limited**: `admitted_official/cohort = 0.783805 = 1.15 · coverage(2018)`, and the
  panel's own demand share is `0.954773`. In the **A10** (two-tier) arm the same cell's gate is
  **participation-limited** — `0.681570` with `demand_official/cohort = 0.900000` and the unfilled-Tier-O margin
  taking a further 10 pp (D144) — so a seats uplift there would **not** move the gate at all until the participation
  margin is repaired. **`λ*` is therefore a coverage requirement conditional on the gate being capacity-limited**;
  it is not A10's requirement, and citing it as such would be a scope error of exactly the class D143 (viii) names.
  (*No A10-equivalent `λ` was computed here: the block's equation does not describe that arm, and computing one
  would be a new cell with a new predeclaration.*)
- **It does not carry to other levels, countries or years.** Only the 2021/2018 lower cell is verdict-bearing. The
  by-year context run (§7) shows the requirement moving, which is exactly why it must not be transplanted.
- **It says nothing about the observed series.** The single `OBSERVED` number appears in §1 and §5 as a reference
  and enters no verdict path.

---

## 7. Path context (declared, **non-verdict-bearing**)

The same solve at the neighbouring years, each with its own bracket and its own entry year (D142/D143's "report the
whole path" requirement):

| completion year | 2017 | 2019 | 2020 | **2021** | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|
| required `λ` | 1.313635 | 1.217934 | 1.166538 | **1.114650** | 1.063991 | 1.013340 | 0.962597 |
| implied `a` | 0.883729 | 0.877891 | 0.876134 | **0.873669** | 0.870912 | 0.868739 | 0.867517 |
| implied `s` | 0.830777 | 0.836302 | 0.837979 | **0.840343** | 0.843003 | 0.845111 | 0.846302 |

The required uplift falls monotonically and crosses 1.0 between 2023 and 2024 — the same crossing D140 reports from
the gap path (+1.72 pp at 2023, −5.11 pp at 2024). That is a **consistency observation**, not a re-score of EXP-13,
and it does not license a later-year reading: **the scored year is 2021** and the successor scores 2021.

---

## 8. What this cell does not say

- **No adoption.** `λ*` is a required state. No constant was re-chosen, no grid cell adopted, no parameter tuned;
  `m = 1.10`, `phys_cap = 1.15`, `surv_max = 0.91`, `gamma = 0.55` are the frozen values, unchanged.
- **No causal or direction claim.** Not "coverage raises completion"; not "the fix is to build places"; nothing
  about the Philippines; nothing about policy.
- **Not a repair, not a target, not a forecast.** `0.8076` is the model's own internal-consistency requirement, and
  `λ*` is its arithmetic consequence.
- **No re-scoring.** EXP-13's shares, label and reachability verdicts stand untouched; EXP-14 is not re-scored; no
  generator was run; no observed-path count is computed (`count_blind = TRUE` in the results).
- **D63 stays `UNABLE as to cause`**; the phase verdict and the scaling `FAIL` are untouched.
- **Synthetic ≠ observed.** Every number in the verdict path is `SYNTHETIC` or `DERIVED` from `SYNTHETIC` values.

---

## 9. Reproduction

```
python3 code/run_joint_cover.py --outdir results
python3 code/run_joint_cover.py --outdir results/determinism_run2
```

No RNG, no clock, no network, no generator import; all inputs read-only; the script **refuses to run** if
`PRE_DECLARATIONS.md`'s sha256 is not `3394e3f4f085d73e62fa5b07e11270dcc53357516935f2f6975129d3c15ee271` (the value
embedded in it and in the manifest). Two runs are **byte-identical**: `JOINT_COVER_RESULTS.csv`
`9d5afc9a…`, `JOINT_COVER_DETAIL.csv` `0e46899c…`, `INPUT_HASHES.json` `85430a1f…` in both `results/` and
`results/determinism_run2/`.

**Files:** `PRE_DECLARATIONS.md` (frozen, hashed before the run) · `code/run_joint_cover.py` ·
`results/JOINT_COVER_RESULTS.csv` (86 rows: falsifier, roots, implied state, checks, verdict, reference, context) ·
`results/JOINT_COVER_DETAIL.csv` (6 001-point grid, brackets, 33-step bisection trace, Newton trace, critical λ) ·
`results/INPUT_HASHES.json` · `results/determinism_run2/` · `RUN_MANIFEST.json` · `SHA256SUMS.txt`.
