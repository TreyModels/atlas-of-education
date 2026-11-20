# FINDINGS — EXP-12 FLOOR-CLOSE

**`LABEL: SYNTHETIC`** — every number below is computed from the frozen synthetic generator panel
(`synthetic_panel_v1_2.csv`, sha256 `14729c51…fac5ac`). No observed data series is read, compared or
scored here.

**Experiment:** EXP-12 **FLOOR-CLOSE** — *what closes the model's floor gate: places, cohort, or the
declared `phys_cap = 1.15` crowding allowance?*
**Source:** Council brief 023, `08_council/brief_023/SYNTHESIS_023.md` §6.2 (D136 #2, rank #2);
scope note D133.
**Predeclaration:** `PRE_DECLARATIONS.md`, sha256
**`1db266e2739d09cf54d8ec5dc4f72f2b8e73d6471b4bc7a1ff99de0924e06e44`** (frozen before first
execution; block spliced verbatim).
**Verdict: `ALLOWANCE-CARRIED`** — 40 closing cells, the declared allowance term is ≥ 50 % of the log
change in **40/40** cells (bar: ≥ 50 % of cells; falsifier bar: ≥ 30 cells).

---

## 1. The answer in one paragraph

The model's floor gate does **not** open by adequate places catching up with demand. It opens by
rule: the declared `phys_cap = 1.15` crowding allowance lets 115 pupils occupy 100 adequate places.
In all 40 level×country cells where a gate closes, the gate is on the `1.15·seats` branch at closure,
coverage is below 1.0 (median 0.8355), and the allowance term accounts for a **median 84.2 %** of the
counterfactual log-margin change (range 66.5 %–98.1 %). Evaluated arithmetically with the declared
no-crowding reference (`phys_cap = 1.0`), the gate would be **closed in all 40 cells** at their
closing year. The recorded A10/D62 disposition "capacity buys the floor" therefore has to be
restated as **conditional on a declared crowding convention**: no capacity-mechanism claim may rest
on the floor until a measured places/PTR series exists (HELD), and any downstream repair must report
the floor's dependence on `phys_cap` as a sensitivity. This is an accounting decomposition of a
declared-assumption simulator; it makes **no causal claim** and **no direction claim**.

---

## 2. What was run

The predeclaration (§3) fixes: `p_off = admitted_official / demand_official`; gate **binding** iff
`p_off < 1`; the **closing year `t*`** is the first year with `p_off = 1.0` after ≥ 3 binding years;
the **last binding year** is `t_b = t* − 1`. The decomposition target is

`Δ = ln(min(1.15·seats(t*), 1.05·cohort(t*))/demand(t*)) − ln(min(1.0·seats(t_b), 1.05·cohort(t_b))/demand(t_b))`

attributed over three factors — **places** (`seats`), **demand/cohort** (`demand_official` and its
driver `cohort`), and the **allowance** (`phys_cap`: 1.0 → 1.15) — by an equal-split Shapley value
over the 3! = 6 orderings. The allowance enters as the declared level shift from the no-crowding
reference, not as a within-cell change: `phys_cap` is a constant in the frozen panel, so a pure
year-to-year reading of that term is identically zero (see §6 below and PRE_DECLARATIONS §3.3). One
deterministic script, no RNG, no re-fit, no model re-run, no parameter change. Full definitions and
the verbatim Council block are in `PRE_DECLARATIONS.md`.

---

## 3. The closure census (all 120 cells reported; none dropped)

| status | cells | primary | lower_sec | upper_sec | tertiary |
|---|---|---|---|---|---|
| **closing** (first `p_off = 1` after ≥ 3 binding years) | **40** | 14 | 19 | 7 | 0 |
| `RIGHT_CENSORED_STILL_BINDING` (≥ 3 binding years, still binding in 2025) | 28 | 16 | 11 | 1 | 0 |
| `NEVER_BOUND_3_YEARS` (fewer than 3 binding years; open, mostly from the start) | 52 | 0 | 0 | 22 | 30 |
| total | 120 | 30 | 30 | 30 | 30 |

Three facts belong next to the verdict. (i) **N = 40** clears the predeclared falsifier bar of 30,
so the falsifier did not fire: the verdict is resolved rather than `UNDETERMINED`. (ii) "Floor
universalization" is **not panel-wide**: 40/120 cells close, 28 are still binding in 2025, and 52
never accumulate 3 binding years. Even at primary — the level where the model's level match is
plausible — only **14/30** cells close. (iii) At closure **every** cell is on the `1.15·seats`
branch: the `1.05·cohort` term is the smaller one in **0/40** closing configurations, and no cell
switches branch across the visited configurations, so the "phys_cap is identically zero on the cohort
branch" caveat has **no closing cell** to bite on here (reported separately, per the block, in
`FLOOR_CLOSE_SHAPLEY.csv`, `cohort_branch`/`branch_switch`).

---

## 4. Per-closure factor shares (the verdict table)

Shares are `σ = φ/Δ`, equal-split Shapley, 3 factors. A cell carries a factor iff `σ ≥ 0.5`. Negative
shares are possible and reported as computed (two cells have negative places shares, in years when
seats fell between `t_b` and `t*`; twenty-one have negative demand shares, in years when demand rose);
the allowance level shift is large enough that the gate still opens. Coverage is `seats/cohort` at
the closing year.

| level | country | close yr | coverage | σ allowance | σ places | σ demand | cell label |
|---|---|---|---|---|---|---|---|
| primary | SYN00_PHL_LIKE | 2019 | 0.8722 | 0.9285 | 0.0438 | 0.0276 | ALLOWANCE-CARRIED |
| primary | SYN07 | 2006 | 0.8683 | 0.8390 | 0.1490 | 0.0120 | ALLOWANCE-CARRIED |
| primary | SYN08 | 2012 | 0.8616 | 0.9610 | 0.0433 | -0.0044 | ALLOWANCE-CARRIED |
| primary | SYN10_BOOM | 2019 | 0.8722 | 0.9294 | 0.0439 | 0.0268 | ALLOWANCE-CARRIED |
| primary | SYN11_FLAT | 2022 | 0.8665 | 0.9809 | 0.0188 | 0.0003 | ALLOWANCE-CARRIED |
| primary | SYN12_DECLINE | 2009 | 0.8676 | 0.9695 | -0.0323 | 0.0628 | ALLOWANCE-CARRIED |
| primary | SYN16 | 2017 | 0.8472 | 0.9624 | 0.0001 | 0.0375 | ALLOWANCE-CARRIED |
| primary | SYN17 | 2018 | 0.8675 | 0.9697 | -0.0257 | 0.0560 | ALLOWANCE-CARRIED |
| primary | SYN18 | 2010 | 0.8603 | 0.9166 | 0.0637 | 0.0197 | ALLOWANCE-CARRIED |
| primary | SYN19 | 2008 | 0.8647 | 0.8870 | 0.1697 | -0.0568 | ALLOWANCE-CARRIED |
| primary | SYN23 | 2008 | 0.8794 | 0.8441 | 0.1322 | 0.0237 | ALLOWANCE-CARRIED |
| primary | SYN26 | 2019 | 0.8610 | 0.9676 | 0.0392 | -0.0067 | ALLOWANCE-CARRIED |
| primary | SYN27 | 2010 | 0.8640 | 0.9481 | 0.0618 | -0.0099 | ALLOWANCE-CARRIED |
| primary | SYN29 | 2009 | 0.8621 | 0.9216 | 0.1096 | -0.0312 | ALLOWANCE-CARRIED |
| lower_secondary | SYN00_PHL_LIKE | 2023 | 0.8698 | 0.7355 | 0.1889 | 0.0756 | ALLOWANCE-CARRIED |
| lower_secondary | SYN01_TWIN_MFG | 2025 | 0.8355 | 0.7917 | 0.2705 | -0.0622 | ALLOWANCE-CARRIED |
| lower_secondary | SYN02_TWIN_OFFICE | 2025 | 0.8355 | 0.7917 | 0.2705 | -0.0622 | ALLOWANCE-CARRIED |
| lower_secondary | SYN04 | 1975 | 0.4884 | 0.8195 | 0.0000 | 0.1805 | ALLOWANCE-CARRIED |
| lower_secondary | SYN05 | 2023 | 0.8231 | 0.7767 | 0.2659 | -0.0426 | ALLOWANCE-CARRIED |
| lower_secondary | SYN07 | 2019 | 0.8553 | 0.7907 | 0.1972 | 0.0121 | ALLOWANCE-CARRIED |
| lower_secondary | SYN08 | 2022 | 0.7762 | 0.8179 | 0.2189 | -0.0368 | ALLOWANCE-CARRIED |
| lower_secondary | SYN10_BOOM | 2023 | 0.8698 | 0.7212 | 0.1852 | 0.0936 | ALLOWANCE-CARRIED |
| lower_secondary | SYN11_FLAT | 2024 | 0.8508 | 0.7925 | 0.2230 | -0.0154 | ALLOWANCE-CARRIED |
| lower_secondary | SYN12_DECLINE | 2022 | 0.8333 | 0.7808 | 0.1633 | 0.0559 | ALLOWANCE-CARRIED |
| lower_secondary | SYN13 | 2021 | 0.7735 | 0.7838 | 0.2351 | -0.0188 | ALLOWANCE-CARRIED |
| lower_secondary | SYN16 | 2017 | 0.6365 | 0.6646 | 0.0878 | 0.2476 | ALLOWANCE-CARRIED |
| lower_secondary | SYN18 | 2023 | 0.8069 | 0.7928 | 0.1953 | 0.0119 | ALLOWANCE-CARRIED |
| lower_secondary | SYN19 | 2024 | 0.8375 | 0.7838 | 0.2653 | -0.0490 | ALLOWANCE-CARRIED |
| lower_secondary | SYN20 | 2022 | 0.8118 | 0.7787 | 0.2872 | -0.0659 | ALLOWANCE-CARRIED |
| lower_secondary | SYN21 | 2019 | 0.7894 | 0.7926 | 0.2697 | -0.0623 | ALLOWANCE-CARRIED |
| lower_secondary | SYN23 | 2015 | 0.7970 | 0.7550 | 0.1766 | 0.0684 | ALLOWANCE-CARRIED |
| lower_secondary | SYN27 | 2020 | 0.8165 | 0.7913 | 0.2264 | -0.0177 | ALLOWANCE-CARRIED |
| lower_secondary | SYN29 | 2011 | 0.8150 | 0.7946 | 0.2806 | -0.0752 | ALLOWANCE-CARRIED |
| upper_secondary | SYN01_TWIN_MFG | 1979 | 0.4170 | 0.8829 | 0.1343 | -0.0172 | ALLOWANCE-CARRIED |
| upper_secondary | SYN02_TWIN_OFFICE | 1979 | 0.4170 | 0.8829 | 0.1343 | -0.0172 | ALLOWANCE-CARRIED |
| upper_secondary | SYN07 | 1985 | 0.4568 | 0.9251 | 0.2452 | -0.1703 | ALLOWANCE-CARRIED |
| upper_secondary | SYN11_FLAT | 1997 | 0.5528 | 0.8653 | 0.0909 | 0.0438 | ALLOWANCE-CARRIED |
| upper_secondary | SYN12_DECLINE | 2003 | 0.6506 | 0.8449 | 0.0558 | 0.0993 | ALLOWANCE-CARRIED |
| upper_secondary | SYN14 | 1995 | 0.4745 | 0.9167 | 0.1904 | -0.1071 | ALLOWANCE-CARRIED |
| upper_secondary | SYN19 | 1988 | 0.4794 | 0.8991 | 0.1636 | -0.0627 | ALLOWANCE-CARRIED |

Panel counts: allowance ≥ 0.5 in **40/40** cells (100 %); places ≥ 0.5 in 0/40; demand ≥ 0.5 in 0/40;
`MIXED` 0/40. Allowance share quartiles: **0.7908 / 0.8415 / 0.9242** (min 0.6646, max 0.9809).
Shapley efficiency holds exactly (maximum absolute residual **2.78e-17**); the binding-branch
additive identity holds in all 40 cells (maximum residual **2.08e-16**), with `φ_allowance =
ln(1.15) = 0.139762` in every cell.

**Coverage at closure is below 1.0 in every closing cell** (range 0.4170–0.8794, median 0.8355).
Evaluated arithmetically at the declared no-crowding reference, `min(1.0·seats, 1.05·cohort) < demand`
in **40/40** cells: the gate would be closed at its own closing year in every cell. The allowance is
necessary for every observed closure; it is not merely one contributor among three.

---

## 5. Anchor cell vs V10 (reported separately, as the block requires)

`SYN00_PHL_LIKE × primary`, last binding year **2018** (49 binding years before closure), close year
**2019**:

| quantity | value |
|---|---|
| `seat_coverage` at closure | **0.872165715** (V10: 0.8722 — **PASS**) |
| `seats` / `cohort` / `demand` at closure | 2 115 583.672 / 2 425 667.090 / 2 415 085.140 |
| `1.15·seats` at closure | 2 432 921.223 (V10: 2 432 921 — **PASS**) |
| `1.05·cohort` at closure | 2 546 950.444 (larger term — places branch) |
| margin `ln(capacity/demand)` at 2018 → 2019 | −0.003397 → +0.007358 |
| `Δ` (decomposition target) | 0.150517 |
| **σ allowance / places / demand** | **0.9285 / 0.0438 / 0.0276** → `ALLOWANCE-CARRIED` |
| `φ allowance` / `φ places` / `φ demand` | 0.139762 / 0.006595 / 0.004160 |

The anchor's allowance share (92.9 %) is slightly above the panel median (84.2 %). V10's motivating
numbers reproduce exactly; V10 is a consistency check here, not a new result.

---

## 6. The year-of-closure nuance (declared sensitivity S1 — never verdict-bearing)

The verdict above rests on the declared counterfactual reading of the allowance term (§3.3 of the
predeclaration). The observed **year-to-year** movement is a different object: between `t_b` and `t*`
the allowance is constant, so a pure observed-change decomposition gives the allowance exactly **0**
and attributes the movement to places or demand. That sensitivity (S1) is reported in
`FLOOR_CLOSE_SENSITIVITY.csv`: **34/40 CAPACITY, 6/40 DEMAND, 0/40 ALLOWANCE**, with observed log
movements of 0.0027–0.0705.

Both statements are true and should travel together:

- **Why the gate is *open* at sub-unity coverage (median 84 %)** — the standing `phys_cap = 1.15`
  allowance. This is the predeclared verdict object, and it is what makes A10/D62 conditional.
- **What moved in the closing year** — seats growth (34 cells) or demand/cohort decline (6 cells).
  The allowance contributes none of that movement; it is a constant of the rule.

S2 (demand held at `t_b`, capacity-only) gives ALLOWANCE in 40/40 cells and is also non-verdict-
bearing. Neither sensitivity can change the verdict; they exist to make the reading transparent.

---

## 7. What this means for the recorded "capacity buys the floor" disposition

The block's §2 consequence fires: **`ALLOWANCE-CARRIED`**.

1. **A10/D62 must be restated as conditional on a declared crowding convention.** The accurate
   statement is: *in this implementation, the floor gate opens at sub-unity coverage under the
   declared capacity rule, which lets `1.15·seats` count as capacity; it does not open by adequate
   places reaching the cohort.* The recorded disposition "capacity buys the floor" survives only in
   that conditional form.
2. **No capacity-mechanism claim may rest on the floor until a measured places/PTR series exists
   (HELD).** The experiment supplies no evidence about real schooling supply; it shows what the
   declared rule does.
3. **The repair (V16) must report the floor's dependence on `phys_cap` as a sensitivity.** The floor
   result is not robust to the crowding convention: at `phys_cap = 1.0` every closing gate in this
   panel would be closed at its observed closing year (arithmetic only; no re-run was performed, per
   the block).
4. **Places are not irrelevant** — the allowance operates through adequate places: every closure is
   on the `1.15·seats` branch, so places are necessary but not *sufficient* at observed coverage.
   This is an accounting statement about the declared rule, not a finding about real capacity.

The other two verdict classes did not occur: `CAPACITY-CARRIED` (places ≥ 50 % in ≥ 50 % of cells)
and `DEMAND-CARRIED` (demand/cohort ≥ 50 % in ≥ 50 %) are both 0/40, and `MIXED` is 0/40.

---

## 8. Honest limits

- **Synthetic, not observed.** The panel is 30 *generator types* × 4 levels × 56 years, produced by a
  declared-assumption simulator. "Countries" are `SYN00…SYN29` generator types, not real systems.
  Nothing here estimates a real capacity mechanism, a real crowding norm, or a real cohort effect.
- **One anchor type.** The separate anchor check is `SYN00_PHL_LIKE` (primary); no cross-type or
  cross-country inference is made or licensed.
- **Declared capacity rule.** The decomposition is of `min(phys_cap·seats, overage_cap·cohort)` with
  `phys_cap = 1.15` (DECLARED) and `overage_cap = 1.05` (CONVENTION). A different declared rule would
  be a different experiment.
- **The reference-shift reading is a declared choice.** `phys_cap` is constant, so a pure observed-
  change decomposition gives the allowance zero by construction (S1). The verdict uses the level
  shift from the declared no-crowding reference; this is stated in the predeclaration before results
  and the alternative is reported alongside. The verdict is an accounting convention on that
  reading, not an estimate.
- **Coverage.** 40 of 120 cells close; 28 are right-censored (still binding in 2025) and 52 never
  accumulate 3 binding years. The verdict describes the cells that close, not the whole panel. Only
  14/30 primary cells close, so even the floor claim is a partial-panel statement.
- **`phys_cap` is never estimated.** 1.15 is a declared modelling convention; the experiment does
  not test whether 1.15 is empirically right.
- **No causal or direction claim.** The shares are an accounting identity on a declared simulator.
  They do not establish that crowding, places or cohorts cause anything in the world, and they do not
  license a policy direction.
- **No re-fit, no threshold change, no model re-run.** `phys_cap` was not changed in the model; the
  `1.0` reference is arithmetic on frozen columns. The predeclaration hash is pinned in the script.

---

## 9. Determinism and integrity

- Two runs, `results/` and `results/determinism_run2/`; **5/5 output files byte-identical**
  (`FLOOR_CLOSE_RESULTS.csv`, `FLOOR_CLOSE_SHAPLEY.csv`, `FLOOR_CLOSE_DETAIL.csv`,
  `FLOOR_CLOSE_SENSITIVITY.csv`, `FLOOR_CLOSE_PANEL.json`).
- No RNG, no clock, no environment-dependent ordering. Rows sorted by declared level order, then
  `country_id`; orderings from a fixed tuple; floats `%.12f`; LF newlines.
- Predeclaration sha256 `1db266e2…e06e44`, verified by the script before any computation. Panel
  sha256 `14729c51…fac5ac`, verified likewise. Reproduction:
  `python code/run_floor_close.py` and `python code/run_floor_close.py results/determinism_run2`.
- Closure-definition sensitivity (S4): the closing count is **40** under all three definitions —
  primary (`p_off < 1 − 1e-12`), the looser open bar (`1 − 1e-9`), and the ≥ 3 *consecutive* binding-
  years variant. The definition does not decide the verdict.

---

## 10. What would have changed the verdict (block §2, recorded before the run)

`CAPACITY-CARRIED` (places ≥ 50 % in ≥ 50 % of cells) would have preserved A10 at the floor and given
the capacity channel a measured footprint in the model. `DEMAND-CARRIED` would have made the model's
floor universalization demographic. `UNDETERMINED` (fewer than 30 closing cells) would have marked
A10 **untested, not confirmed**. None of these obtained: the allowance term is ≥ 50 % of the log
change in every closing cell.
