import Angkor.Basic

/-!
# Monsoon: the year step of the Angkor climate engine

Source: `public/engines/monsoon.js`.
* Weather translation: lines 48-51 (linear response; `pdsiCap` and the exponential response are not formalized).
* Year step: `run`, lines 37-85 (`for (let year ...)`), with all six switches.
* Parameters: `drawPriors`, lines 124-136. Fixed constants: `fixed`, lines 24-25.

Modelling choices:
* Rationals stand in for floating point. Theorems are about ideal rational arithmetic, not IEEE rounding.
* Randomness is an input. The weather `w` (line 51) is passed in already clamped to [2/5, 23/20].
  The succession cohesion (line 43) is an input in {1, contestCut}. The two logistic values (lines 65, 81)
  are inputs in [0,1]. The year is an input.
* The drought switch acts only through the weather draw (line 46), so the step does not read it.
* Not formalized: `score`, `tests`, `drawPriors` itself, the pre-1250 weather, `pdsiCap`, the exponential response.

Division points (Lean value of `x / 0` is 0; JavaScript gives Infinity or NaN):
* `shortfall`: `harvest / (N + B)` (line 56). With N = B = 0, JavaScript gives NaN, not `1 - harvest/0`.
* `unitNeed`: `pool0 / slack` (line 33). With slack = 0, JavaScript gives Infinity.
* `captives`: `... / (1 - b)` (line 60). With b = 1, JavaScript gives Infinity.
* `revenue`: `... / b` (line 80). With b = 0, JavaScript gives Infinity or NaN.
* `growthRate`: `P0 / harvest` (line 58). Reached only when shortfall <= 0, which forces harvest > 0 when N + B > 0.
* `maintained`: `upkeep / need` (line 76), guarded by `need > 0`.
* `Pn`: floored at 1e-9 (line 79), so the division by it is by a positive number.
-/

namespace Angkor.Monsoon

open Angkor

/-! ## Rational helper lemmas (Lean 4.36 core has no `Rat.div_nonneg` or `Rat.inv_nonneg`) -/

theorem rat_inv_nonneg (b : Rat) (h : 0 < b) : 0 ≤ b⁻¹ := by
  have e : b * b⁻¹ = 1 := Rat.mul_inv_cancel b (by grind)
  apply Decidable.byContradiction
  intro hc
  have hneg : 0 ≤ b * (-b⁻¹) := Rat.mul_nonneg (by grind) (by grind)
  grind

theorem rat_div_nonneg (a b : Rat) (ha : 0 ≤ a) (hb : 0 < b) : 0 ≤ a / b := by
  rw [Rat.div_def]
  exact Rat.mul_nonneg ha (rat_inv_nonneg b hb)

theorem rat_div_zero (a : Rat) : a / 0 = 0 := by
  rw [Rat.div_def, Rat.inv_zero, Rat.mul_zero]

/-- Parameters, named as in `drawPriors` (lines 124-136). `bondedShare` is `b`. -/
structure Params where
  attrition : Rat
  bondedShare : Rat
  bondedWork : Rat
  corvee : Rat
  slack : Rat
  growth : Rat
  famine : Rat
  follow : Rat
  decay : Rat
  buffer : Rat
  channelGain : Rat
  contestCut : Rat
  warLoss : Rat
  warFlight : Rat
  orgyShare : Rat
  templeUpkeep : Rat
  silt : Rat
  court : Rat
  outside0 : Rat
  outside1 : Rat
  theravadaFloor : Rat

/-- The six switches, `MECH` (line 23). `drought` acts only in the weather draw. -/
structure Switches where
  war : Bool
  orgy : Bool
  theravada : Bool
  trade : Bool
  drought : Bool
  hydraulic : Bool

/-- Engine state at the start of a year: N, B, C, E, S, M. -/
structure State where
  N : Rat
  B : Rat
  C : Rat
  E : Rat
  S : Rat
  M : Rat

/-- Per-year inputs. `weather` is line 51 after the clamp; `cohesion` is line 43;
`devotionLogistic` is `logistic(year, theravadaYear, 10)` (line 65); `tradeLogistic` is
`logistic(year, tradeYear, 20)` (line 81). -/
structure Inputs where
  year : Nat
  weather : Rat
  cohesion : Rat
  devotionLogistic : Rat
  tradeLogistic : Rat

/-- Fixed field labour, line 25 (`.26`). -/
def fieldLabour : Rat := 26 / 100

/-- Attack years, line 24. -/
def attackYears : List Nat := [1353, 1370, 1431]

/-- Orgy window, line 25, first and last year. -/
def orgyFirst : Nat := 1181
def orgyLast : Nat := 1218

/-! ## Weather translation (lines 48-51, linear response) -/

/-- Line 48 (neutral forces z = 0) and line 50 (linear). -/
def translated (s pdsi : Rat) (neutral : Bool) : Rat :=
  1 + (if neutral then 0 else pdsi) * s

/-- Line 51: `Math.max(.4, Math.min(1.15, translated))`, which is `clamp` with bounds 2/5 and 23/20. -/
def weatherOf (s pdsi : Rat) (neutral : Bool) : Rat :=
  clamp (translated s pdsi neutral) (2 / 5) (23 / 20)

theorem weather_lower (s pdsi : Rat) (neutral : Bool) : 2 / 5 ≤ weatherOf s pdsi neutral :=
  clamp_lower _ _ _

theorem weather_upper (s pdsi : Rat) (neutral : Bool) : weatherOf s pdsi neutral ≤ 23 / 20 :=
  clamp_upper _ _ _ (by grind)

/-- Monotone in pdsi for sensitivity s >= 0 (non-neutral branch). -/
theorem weather_mono (s z₁ z₂ : Rat) (hs : 0 ≤ s) (h : z₁ ≤ z₂) :
    weatherOf s z₁ false ≤ weatherOf s z₂ false := by
  have hp : 0 ≤ (z₂ - z₁) * s := Rat.mul_nonneg (by grind) hs
  unfold weatherOf translated clamp
  grind

/-- Neutral year: the translation is exactly 1. -/
theorem weather_neutral (s pdsi : Rat) : weatherOf s pdsi true = 1 := by
  unfold weatherOf translated clamp
  grind

/-- Sensitivity 0: the translation is exactly 1. -/
theorem weather_sens_zero (pdsi : Rat) (neutral : Bool) : weatherOf 0 pdsi neutral = 1 := by
  unfold weatherOf translated clamp
  grind

/-! ## Hypotheses -/

/-- Parameter ranges used by the invariants. Each field is a bound that drawPriors satisfies
(b = bondedShare lies in (0, .4]; decay, buffer, warLoss, warFlight, orgyShare, theravadaFloor in their ranges). -/
structure ParamsOK (p : Params) : Prop where
  attr_nonneg : 0 ≤ p.attrition
  b_nonneg : 0 ≤ p.bondedShare
  b_lt_one : p.bondedShare < 1
  bw_nonneg : 0 ≤ p.bondedWork
  cor_nonneg : 0 ≤ p.corvee
  slack_pos : 0 < p.slack
  decay_nonneg : 0 ≤ p.decay
  decay_le_one : p.decay ≤ 1
  channel_nonneg : 0 ≤ p.channelGain
  warLoss_nonneg : 0 ≤ p.warLoss
  warLoss_le_half : p.warLoss ≤ 1 / 2
  warFlight_nonneg : 0 ≤ p.warFlight
  warFlight_le_one : p.warFlight ≤ 1
  orgy_nonneg : 0 ≤ p.orgyShare
  orgy_le_one : p.orgyShare ≤ 1
  tu_nonneg : 0 ≤ p.templeUpkeep
  silt_nonneg : 0 ≤ p.silt
  tf_nonneg : 0 ≤ p.theravadaFloor
  tf_le_one : p.theravadaFloor ≤ 1
  court_nonneg : 0 ≤ p.court

/-- Input ranges: cohesion in [0,1] (1 or contestCut in [.2,.6]); logistic values in [0,1] (open (0,1) in the source). -/
structure InputsOK (i : Inputs) : Prop where
  coh_nonneg : 0 ≤ i.cohesion
  coh_le_one : i.cohesion ≤ 1
  dev_nonneg : 0 ≤ i.devotionLogistic
  dev_le_one : i.devotionLogistic ≤ 1
  trade_nonneg : 0 ≤ i.tradeLogistic
  trade_le_one : i.tradeLogistic ≤ 1

/-- State invariant: N, B >= 0; C, E in [0,1]; S, M >= 0. -/
structure StateOK (st : State) : Prop where
  N_nonneg : 0 ≤ st.N
  B_nonneg : 0 ≤ st.B
  C_nonneg : 0 ≤ st.C
  C_le_one : st.C ≤ 1
  E_nonneg : 0 ≤ st.E
  E_le_one : st.E ≤ 1
  S_nonneg : 0 ≤ st.S
  M_nonneg : 0 ≤ st.M

/-! ## One year (lines 37-85) -/

/-- Line 32. Court labour at baseline. -/
def poolZero (p : Params) : Rat := p.bondedWork * p.bondedShare + p.corvee * (1 - p.bondedShare)

/-- Line 33. Upkeep per unit of network at baseline. Divides by `slack`. -/
def unitNeed (p : Params) : Rat := poolZero p / p.slack

/-- Line 52. Buffered weather. -/
def buffered (p : Params) (C w : Rat) : Rat :=
  if w < 1 then w + C * p.buffer * (1 - w) else w

/-- Line 53. Capacity. -/
def capacity (p : Params) (C w : Rat) : Rat :=
  buffered p C w * (1 + p.channelGain * C) / (1 + p.channelGain)

/-- Line 55. Harvest from pre-step N, B, C. -/
def harvest (p : Params) (st : State) (w : Rat) : Rat :=
  capacity p st.C w * min 1 ((st.N + 3 / 4 * st.B) / fieldLabour)

/-- Line 56. Shortfall, with P0 = N + B (line 54). Divides by P0. -/
def shortfall (p : Params) (st : State) (w : Rat) : Rat :=
  max 0 (1 - harvest p st w / (st.N + st.B))

/-- Line 57. -/
def followRate (p : Params) (st : State) : Rat := p.follow * (1 - st.E)

/-- Line 58. The else branch divides by harvest. -/
def growthRate (p : Params) (st : State) (w : Rat) : Rat :=
  if shortfall p st w > 0 then -p.famine * shortfall p st w
  else p.growth * (1 - (st.N + st.B) / harvest p st w)

/-- Line 59. N after growth. -/
def nGrown (p : Params) (st : State) (w : Rat) : Rat :=
  max 0 (st.N * (1 + growthRate p st w - followRate p st))

/-- Line 60. Captives. Divides by 1 - b. -/
def captives (p : Params) (N : Rat) : Rat :=
  p.attrition * p.bondedShare * N / (1 - p.bondedShare)

/-- Line 61. B after attrition, famine, follow and captives (captives use the grown N). -/
def bGrown (p : Params) (st : State) (w : Rat) : Rat :=
  max 0 (st.B * (1 - p.attrition
      - (if shortfall p st w > 0 then p.famine * shortfall p st w else 0)
      - followRate p st) + captives p (nGrown p st w))

def isAttack (i : Inputs) : Bool := attackYears.contains i.year

/-- Lines 46 and 63: war applies in an attack year when the war switch is on. -/
def warOn (on : Switches) (i : Inputs) : Bool := on.war && isAttack i

/-- Line 63: N, B, E after the war hit. -/
def nWar (p : Params) (on : Switches) (i : Inputs) (N : Rat) : Rat :=
  if warOn on i then N * (1 - p.warLoss) else N

def bWar (p : Params) (on : Switches) (i : Inputs) (B : Rat) : Rat :=
  if warOn on i then B * (1 - 2 * p.warLoss) else B

def eWar (p : Params) (on : Switches) (i : Inputs) (E : Rat) : Rat :=
  if warOn on i then E * (1 - p.warFlight) else E

/-- Line 65. Theravada devotion factor. -/
def devotion (p : Params) (on : Switches) (i : Inputs) : Rat :=
  if on.theravada then 1 - (1 - p.theravadaFloor) * i.devotionLogistic else 1

/-- Line 66. Court labour, using the post-war N, B, E. -/
def poolOf (p : Params) (on : Switches) (i : Inputs) (Nw Bw Ew : Rat) : Rat :=
  (p.bondedWork * Bw + p.corvee * Ew * Nw) * devotion p on i * i.cohesion

/-- Line 69. Silting factor. -/
def siltFactor (p : Params) (on : Switches) (i : Inputs) : Rat :=
  if on.hydraulic then 1 + p.silt * ((i.year - 1000 : Nat) : Rat) / 100 else 1

/-- Line 70. Need, with S already updated (line 68) and M the pre-step M. -/
def needOf (p : Params) (on : Switches) (i : Inputs) (S M : Rat) : Rat :=
  unitNeed p * S * siltFactor p on i + (if on.orgy then p.templeUpkeep * M else 0)

/-- Line 71. -/
def inOrgy (on : Switches) (i : Inputs) : Bool :=
  on.orgy && decide (orgyFirst ≤ i.year ∧ i.year ≤ orgyLast)

/-- Lines 72-74. Build. -/
def buildOf (p : Params) (on : Switches) (i : Inputs) (pool need : Rat) : Rat :=
  if inOrgy on i then pool * p.orgyShare else pool - min need pool

/-- Lines 72-74. Upkeep. -/
def upkeepOf (p : Params) (on : Switches) (i : Inputs) (pool need : Rat) : Rat :=
  if inOrgy on i then min need (pool - pool * p.orgyShare) else min need pool

/-- Line 76. -/
def maintainedOf (upkeep need : Rat) : Rat := if need > 0 then upkeep / need else 1

/-- Line 79. -/
def Pn (Nw Bw : Rat) : Rat := max (1 / 1000000000) (Nw + Bw)

/-- Line 80. Divides by Pn (positive) and by b. -/
def revenueOf (p : Params) (H Nw Bw : Rat) : Rat :=
  1 / 2 * min (3 / 2) (H / Pn Nw Bw) + 1 / 2 * (Bw / Pn Nw Bw) / p.bondedShare

/-- Line 81. -/
def outsideOf (p : Params) (on : Switches) (i : Inputs) : Rat :=
  if on.trade then p.outside0 + (p.outside1 - p.outside0) * i.tradeLogistic else p.outside0

/-- One year: lines 46-85 with the drought switch absorbed into `i.weather`.
Order follows the source: growth (57-59), B (60-61), war (63), pool (65-66), S (68),
need (69-70), build (71-75), C (76-77), revenue (79-80), outside (81), E (82-83). -/
def step (p : Params) (on : Switches) (i : Inputs) (st : State) : State :=
  let Nw := nWar p on i (nGrown p st i.weather)
  let Bw := bWar p on i (bGrown p st i.weather)
  let Ew := eWar p on i st.E
  let pl := poolOf p on i Nw Bw Ew
  let S' := max st.S (Nw + Bw)
  let nd := needOf p on i S' st.M
  let gap := revenueOf p (harvest p st i.weather) Nw Bw - outsideOf p on i
  { N := Nw
    B := Bw
    C := st.C * (1 - p.decay) + p.decay * min 1 (maintainedOf (upkeepOf p on i pl nd) nd)
    E := min 1 (max 0 (Ew + p.court * (if gap > 0 then (1 - Ew) * gap else Ew * gap)))
    S := S'
    M := st.M + buildOf p on i pl nd }

/-- Run a list of years. -/
def runSteps (p : Params) (on : Switches) : List Inputs → State → State
  | [], st => st
  | i :: is, st => runSteps p on is (step p on i st)

/-! ## Target 2: one step and any number of steps -/

theorem nGrown_nonneg (p : Params) (st : State) (w : Rat) : 0 ≤ nGrown p st w := by
  unfold nGrown
  grind

theorem bGrown_nonneg (p : Params) (st : State) (w : Rat) : 0 ≤ bGrown p st w := by
  unfold bGrown
  grind

theorem nWar_nonneg (p : Params) (on : Switches) (i : Inputs) (N : Rat) (hp : ParamsOK p)
    (hN : 0 ≤ N) : 0 ≤ nWar p on i N := by
  unfold nWar
  split
  · exact Rat.mul_nonneg hN (by grind [hp.warLoss_le_half])
  · exact hN

theorem bWar_nonneg (p : Params) (on : Switches) (i : Inputs) (B : Rat) (hp : ParamsOK p)
    (hB : 0 ≤ B) : 0 ≤ bWar p on i B := by
  unfold bWar
  split
  · exact Rat.mul_nonneg hB (by grind [hp.warLoss_nonneg, hp.warLoss_le_half])
  · exact hB

theorem eWar_nonneg (p : Params) (on : Switches) (i : Inputs) (E : Rat) (hp : ParamsOK p)
    (hE : 0 ≤ E) : 0 ≤ eWar p on i E := by
  unfold eWar
  split
  · exact Rat.mul_nonneg hE (by grind [hp.warFlight_le_one])
  · exact hE

theorem devotion_bounds (p : Params) (on : Switches) (i : Inputs) (hp : ParamsOK p)
    (hi : InputsOK i) : 0 ≤ devotion p on i ∧ devotion p on i ≤ 1 := by
  unfold devotion
  split
  · have h1 : 0 ≤ (1 - p.theravadaFloor) * i.devotionLogistic :=
      Rat.mul_nonneg (by grind [hp.tf_le_one]) hi.dev_nonneg
    have h2 : 0 ≤ p.theravadaFloor * i.devotionLogistic :=
      Rat.mul_nonneg hp.tf_nonneg hi.dev_nonneg
    grind [hi.dev_le_one]
  · grind

theorem poolOf_nonneg (p : Params) (on : Switches) (i : Inputs) (Nw Bw Ew : Rat) (hp : ParamsOK p)
    (hi : InputsOK i) (hN : 0 ≤ Nw) (hB : 0 ≤ Bw) (hE : 0 ≤ Ew) : 0 ≤ poolOf p on i Nw Bw Ew := by
  have a1 : 0 ≤ p.bondedWork * Bw := Rat.mul_nonneg hp.bw_nonneg hB
  have a2 : 0 ≤ p.corvee * Ew * Nw := Rat.mul_nonneg (Rat.mul_nonneg hp.cor_nonneg hE) hN
  have hd := (devotion_bounds p on i hp hi).1
  have hX : 0 ≤ p.bondedWork * Bw + p.corvee * Ew * Nw := by grind
  unfold poolOf
  exact Rat.mul_nonneg (Rat.mul_nonneg hX hd) hi.coh_nonneg

theorem poolZero_nonneg (p : Params) (hp : ParamsOK p) : 0 ≤ poolZero p := by
  have a1 : 0 ≤ p.bondedWork * p.bondedShare := Rat.mul_nonneg hp.bw_nonneg hp.b_nonneg
  have a2 : 0 ≤ p.corvee * (1 - p.bondedShare) :=
    Rat.mul_nonneg hp.cor_nonneg (by grind [hp.b_lt_one])
  unfold poolZero
  grind

/-- Division by the positive slack. -/
theorem unitNeed_nonneg (p : Params) (hp : ParamsOK p) : 0 ≤ unitNeed p := by
  unfold unitNeed
  exact rat_div_nonneg _ _ (poolZero_nonneg p hp) hp.slack_pos

theorem needOf_nonneg (p : Params) (on : Switches) (i : Inputs) (S M : Rat) (hp : ParamsOK p)
    (hS : 0 ≤ S) (hM : 0 ≤ M) : 0 ≤ needOf p on i S M := by
  have hu : 0 ≤ unitNeed p * S := Rat.mul_nonneg (unitNeed_nonneg p hp) hS
  have hsl : 0 ≤ siltFactor p on i := by
    unfold siltFactor
    split
    · have : 0 ≤ p.silt * ((i.year - 1000 : Nat) : Rat) := Rat.mul_nonneg hp.silt_nonneg (by grind)
      grind
    · grind
  have hus : 0 ≤ unitNeed p * S * siltFactor p on i := Rat.mul_nonneg hu hsl
  have ht : 0 ≤ (if on.orgy then p.templeUpkeep * M else 0) := by
    split
    · exact Rat.mul_nonneg hp.tu_nonneg hM
    · exact Rat.le_refl
  unfold needOf
  grind

/-- Lines 71-75: allocation bounds for both branches. Build and upkeep are nonnegative,
upkeep is at most need, and build + upkeep is at most pool. -/
theorem alloc_bounds (p : Params) (on : Switches) (i : Inputs) (pl nd : Rat) (hp : ParamsOK p)
    (hpl : 0 ≤ pl) (hnd : 0 ≤ nd) :
    0 ≤ upkeepOf p on i pl nd ∧ upkeepOf p on i pl nd ≤ nd ∧
      0 ≤ buildOf p on i pl nd ∧ buildOf p on i pl nd + upkeepOf p on i pl nd ≤ pl := by
  have h1 : 0 ≤ pl * p.orgyShare := Rat.mul_nonneg hpl hp.orgy_nonneg
  have h2 : 0 ≤ pl * (1 - p.orgyShare) := Rat.mul_nonneg hpl (by grind [hp.orgy_le_one])
  unfold upkeepOf buildOf
  by_cases h : inOrgy on i = true
  · simp only [h, ↓reduceIte]
    grind
  · simp only [h, ↓reduceIte]
    grind

/-- Non-orgy year: build + upkeep = pool exactly. -/
theorem alloc_equality_plain (p : Params) (on : Switches) (i : Inputs) (pl nd : Rat)
    (h : inOrgy on i = false) :
    buildOf p on i pl nd + upkeepOf p on i pl nd = pl := by
  unfold upkeepOf buildOf
  simp only [h, Bool.false_eq_true, ↓reduceIte]
  grind

/-- Orgy year: build + upkeep = pool exactly when need covers the unbuilt pool. -/
theorem alloc_equality_orgy (p : Params) (on : Switches) (i : Inputs) (pl nd : Rat)
    (h : inOrgy on i = true) (hn : pl - pl * p.orgyShare ≤ nd) :
    buildOf p on i pl nd + upkeepOf p on i pl nd = pl := by
  unfold upkeepOf buildOf
  simp only [h, ↓reduceIte]
  grind

/-- Line 76: maintained is nonnegative whenever upkeep is (the else branch gives 1). -/
theorem maintained_nonneg (u n : Rat) (hu : 0 ≤ u) : 0 ≤ maintainedOf u n := by
  unfold maintainedOf
  split
  · exact rat_div_nonneg _ _ hu (by grind)
  · grind

/-- Line 77: C stays in [0,1] when C and decay do and the maintained value is nonnegative. -/
theorem C_next_bounds (C d m : Rat) (hC0 : 0 ≤ C) (hC1 : C ≤ 1) (hd0 : 0 ≤ d) (hd1 : d ≤ 1)
    (hm : 0 ≤ m) : 0 ≤ C * (1 - d) + d * min 1 m ∧ C * (1 - d) + d * min 1 m ≤ 1 := by
  have a : 0 ≤ C * (1 - d) := Rat.mul_nonneg hC0 (by grind)
  have b : 0 ≤ d * min 1 m := Rat.mul_nonneg hd0 (by grind)
  have c : 0 ≤ (1 - d) * (1 - C) := Rat.mul_nonneg (by grind) (by grind)
  have e : 0 ≤ d * (1 - min 1 m) := Rat.mul_nonneg hd0 (by grind)
  constructor <;> grind

/-- Line 83: `Math.min(1, Math.max(0, x))` lies in [0,1]. -/
theorem clamp01_bounds (x : Rat) : 0 ≤ min 1 (max 0 x) ∧ min 1 (max 0 x) ≤ 1 := by
  constructor <;> grind

/-- One step preserves the state invariant. -/
theorem step_StateOK (p : Params) (on : Switches) (i : Inputs) (st : State)
    (hp : ParamsOK p) (hi : InputsOK i) (hs : StateOK st) : StateOK (step p on i st) := by
  have hN1 := nGrown_nonneg p st i.weather
  have hB1 := bGrown_nonneg p st i.weather
  have hNw := nWar_nonneg p on i _ hp hN1
  have hBw := bWar_nonneg p on i _ hp hB1
  have hEw := eWar_nonneg p on i st.E hp hs.E_nonneg
  have hpl := poolOf_nonneg p on i _ _ _ hp hi hNw hBw hEw
  have hS' : 0 ≤ max st.S (nWar p on i (nGrown p st i.weather) + bWar p on i (bGrown p st i.weather)) := by
    grind [hs.S_nonneg]
  have hnd := needOf_nonneg p on i _ st.M hp hS' hs.M_nonneg
  have ha := alloc_bounds p on i _ _ hp hpl hnd
  unfold step
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> dsimp only
  · exact hNw
  · exact hBw
  · exact (C_next_bounds st.C p.decay _ hs.C_nonneg hs.C_le_one hp.decay_nonneg hp.decay_le_one
      (maintained_nonneg _ _ ha.1)).1
  · exact (C_next_bounds st.C p.decay _ hs.C_nonneg hs.C_le_one hp.decay_nonneg hp.decay_le_one
      (maintained_nonneg _ _ ha.1)).2
  · exact (clamp01_bounds _).1
  · exact (clamp01_bounds _).2
  · grind [hs.S_nonneg]
  · grind [hs.M_nonneg, ha.2.2.1]

/-- One step: state invariant, S >= N + B after the update, S and M nondecreasing. -/
theorem step_inv (p : Params) (on : Switches) (i : Inputs) (st : State)
    (hp : ParamsOK p) (hi : InputsOK i) (hs : StateOK st) :
    StateOK (step p on i st) ∧ st.S ≤ (step p on i st).S ∧ st.M ≤ (step p on i st).M ∧
      (step p on i st).N + (step p on i st).B ≤ (step p on i st).S := by
  have hN1 := nGrown_nonneg p st i.weather
  have hB1 := bGrown_nonneg p st i.weather
  have hNw := nWar_nonneg p on i _ hp hN1
  have hBw := bWar_nonneg p on i _ hp hB1
  have hEw := eWar_nonneg p on i st.E hp hs.E_nonneg
  have hpl := poolOf_nonneg p on i _ _ _ hp hi hNw hBw hEw
  have hS' : 0 ≤ max st.S (nWar p on i (nGrown p st i.weather) + bWar p on i (bGrown p st i.weather)) := by
    grind [hs.S_nonneg]
  have hnd := needOf_nonneg p on i _ st.M hp hS' hs.M_nonneg
  have ha := alloc_bounds p on i _ _ hp hpl hnd
  refine ⟨step_StateOK p on i st hp hi hs, ?_, ?_, ?_⟩
  · unfold step
    dsimp only
    grind
  · unfold step
    dsimp only
    grind [ha.2.2.1]
  · unfold step
    dsimp only
    grind

theorem runSteps_inv (p : Params) (on : Switches) (hp : ParamsOK p) :
    ∀ (is : List Inputs) (st : State), (∀ i ∈ is, InputsOK i) → StateOK st →
      StateOK (runSteps p on is st)
  | [], _, _, hs => hs
  | i :: is, st, hi, hs =>
    runSteps_inv p on hp is (step p on i st) (fun j hj => hi j (by simp [hj]))
      (step_StateOK p on i st hp (hi i (by simp)) hs)

/-- S never decreases over any number of years. -/
theorem runSteps_S_ge (p : Params) (on : Switches) (hp : ParamsOK p) :
    ∀ (is : List Inputs) (st : State), (∀ i ∈ is, InputsOK i) → StateOK st →
      st.S ≤ (runSteps p on is st).S
  | [], st, _, _ => Rat.le_refl
  | i :: is, st, hi, hs =>
    Rat.le_trans (step_inv p on i st hp (hi i (by simp)) hs).2.1
      (runSteps_S_ge p on hp is (step p on i st) (fun j hj => hi j (by simp [hj]))
        (step_inv p on i st hp (hi i (by simp)) hs).1)

/-- M never decreases over any number of years. -/
theorem runSteps_M_ge (p : Params) (on : Switches) (hp : ParamsOK p) :
    ∀ (is : List Inputs) (st : State), (∀ i ∈ is, InputsOK i) → StateOK st →
      st.M ≤ (runSteps p on is st).M
  | [], st, _, _ => Rat.le_refl
  | i :: is, st, hi, hs =>
    Rat.le_trans (step_inv p on i st hp (hi i (by simp)) hs).2.2.1
      (runSteps_M_ge p on hp is (step p on i st) (fun j hj => hi j (by simp [hj]))
        (step_inv p on i st hp (hi i (by simp)) hs).1)

/-! ## Target 3: division points -/

/-- With N = B = 0 the Lean shortfall is 1. JavaScript computes 0/0 = NaN here. -/
theorem shortfall_empty_pool (p : Params) (st : State) (w : Rat) (h0 : st.N = 0) (h1 : st.B = 0) :
    shortfall p st w = 1 := by
  simp [shortfall, h0, h1] <;> grind

/-- If shortfall <= 0 and P0 > 0, then harvest > 0, so `P0 / harvest` on line 58 is safe. -/
theorem harvest_pos_of_no_shortfall (p : Params) (st : State) (w : Rat)
    (hP : 0 < st.N + st.B) (hs : shortfall p st w ≤ 0) : 0 < harvest p st w := by
  unfold shortfall at hs
  have h1 : 1 - harvest p st w / (st.N + st.B) ≤ 0 := by grind
  have key : harvest p st w / (st.N + st.B) * (st.N + st.B) = harvest p st w :=
    Rat.div_mul_cancel (by grind)
  have q : 0 ≤ (harvest p st w / (st.N + st.B) - 1) * (st.N + st.B) :=
    Rat.mul_nonneg (by grind) (by grind)
  grind

/-- Line 33: with slack = 0 the Lean value is 0; JavaScript gives Infinity when pool0 > 0. -/
theorem unitNeed_zero_slack (p : Params) (h : p.slack = 0) : unitNeed p = 0 := by
  simp [unitNeed, h, rat_div_zero]

/-- Line 60: with b = 1 the Lean value is 0; JavaScript gives Infinity when N > 0. -/
theorem captives_b_one (p : Params) (N : Rat) (h : p.bondedShare = 1) : captives p N = 0 := by
  simp [captives, h, Rat.sub_self, rat_div_zero]

/-- Line 80: with b = 0 the second term of revenue vanishes in Lean; JavaScript gives Infinity or NaN. -/
theorem revenue_b_zero (p : Params) (H Nw Bw : Rat) (h : p.bondedShare = 0) :
    revenueOf p H Nw Bw = 1 / 2 * min (3 / 2) (H / Pn Nw Bw) := by
  simp [revenueOf, h, rat_div_zero, Rat.add_zero]

/-! ## Target 4: switches -/

/-- Orgy off: `need` does not depend on M. -/
theorem needOf_indep_M (p : Params) (on : Switches) (i : Inputs) (S M₁ M₂ : Rat)
    (h : on.orgy = false) : needOf p on i S M₁ = needOf p on i S M₂ := by
  simp [needOf, h]

/-- Orgy off: the whole step, except M itself, does not depend on M; build is also unchanged. -/
theorem step_indep_M (p : Params) (on : Switches) (i : Inputs) (st : State) (m₁ m₂ : Rat)
    (h : on.orgy = false) :
    (step p on i { st with M := m₁ }).N = (step p on i { st with M := m₂ }).N ∧
    (step p on i { st with M := m₁ }).B = (step p on i { st with M := m₂ }).B ∧
    (step p on i { st with M := m₁ }).C = (step p on i { st with M := m₂ }).C ∧
    (step p on i { st with M := m₁ }).E = (step p on i { st with M := m₂ }).E ∧
    (step p on i { st with M := m₁ }).S = (step p on i { st with M := m₂ }).S ∧
    (step p on i { st with M := m₁ }).M - m₁ = (step p on i { st with M := m₂ }).M - m₂ := by
  simp [step, needOf, buildOf, upkeepOf, inOrgy, h, nGrown, bGrown, harvest, capacity, buffered,
    shortfall, growthRate, followRate, captives, nWar, bWar, eWar, warOn, poolOf, devotion,
    siltFactor, outsideOf, revenueOf, Pn, maintainedOf] <;> grind

/-- All switches off: the year step does not depend on warLoss, warFlight, orgyShare,
templeUpkeep, silt, theravadaFloor or outside1. -/
def allOff : Switches :=
  ⟨false, false, false, false, false, false⟩

theorem step_allOff_indep (p : Params) (i : Inputs) (st : State)
    (a b c d e f g : Rat) :
    step { p with warLoss := a, warFlight := b, orgyShare := c, templeUpkeep := d, silt := e, theravadaFloor := f, outside1 := g } allOff i st
      = step p allOff i st := by
  simp [step, allOff, nWar, bWar, eWar, warOn, poolOf, devotion, needOf, siltFactor,
    buildOf, upkeepOf, inOrgy, outsideOf, nGrown, bGrown, harvest, capacity, buffered,
    shortfall, growthRate, followRate, captives, unitNeed, poolZero, revenueOf, Pn, fieldLabour,
    maintainedOf]

/-- All switches off: the year step does not depend on the attack year, the logistic inputs,
or the year itself. -/
theorem step_allOff_indep_inputs (p : Params) (i : Inputs) (st : State) (y : Nat) (x z : Rat) :
    step p allOff { i with year := y, devotionLogistic := x, tradeLogistic := z } st
      = step p allOff i st := by
  simp [step, allOff, nWar, bWar, eWar, warOn, poolOf, devotion, needOf, siltFactor,
    buildOf, upkeepOf, inOrgy, outsideOf, isAttack]

/-! ## Target 5: monotone effects -/

/-- Capacity is nondecreasing in w below 1 when C * buffer <= 1 (lines 52-53). -/
theorem capacity_mono (p : Params) (C w₁ w₂ : Rat) (hp : ParamsOK p) (hC : 0 ≤ C)
    (hcb : C * p.buffer ≤ 1) (h : w₁ ≤ w₂) (h2 : w₂ < 1) :
    capacity p C w₁ ≤ capacity p C w₂ := by
  have hw1 : w₁ < 1 := by grind
  have hd : 0 ≤ (w₂ - w₁) * (1 - C * p.buffer) := Rat.mul_nonneg (by grind) (by grind)
  have hK : 0 ≤ 1 + p.channelGain * C := by
    have := Rat.mul_nonneg hp.channel_nonneg hC
    grind
  have hG : 0 ≤ (1 + p.channelGain)⁻¹ := rat_inv_nonneg _ (by grind [hp.channel_nonneg])
  have hf : 0 ≤ (w₂ - w₁) * (1 - C * p.buffer) * ((1 + p.channelGain * C) * (1 + p.channelGain)⁻¹) :=
    Rat.mul_nonneg hd (Rat.mul_nonneg hK hG)
  unfold capacity buffered
  rw [if_pos hw1, if_pos h2, Rat.div_def, Rat.div_def]
  grind

/-- A war hit does not raise N (warLoss in [0, 1/2]): `nWar` is at most its input. -/
theorem nWar_le (p : Params) (on : Switches) (i : Inputs) (N : Rat) (hp : ParamsOK p)
    (hN : 0 ≤ N) : nWar p on i N ≤ N := by
  unfold nWar
  split
  · have := Rat.mul_nonneg hN hp.warLoss_nonneg
    grind
  · exact Rat.le_refl

/-- A war year does not raise B (warLoss in [0, 1/2]). -/
theorem bWar_le (p : Params) (on : Switches) (i : Inputs) (B : Rat) (hp : ParamsOK p)
    (hB : 0 ≤ B) : bWar p on i B ≤ B := by
  unfold bWar
  split
  · have := Rat.mul_nonneg hB (by grind [hp.warLoss_nonneg] : (0 : Rat) ≤ 2 * p.warLoss)
    grind
  · exact Rat.le_refl

/-- Compared with the same year with the war switch off, the war year's N is no larger. -/
theorem war_does_not_raise_N (p : Params) (on : Switches) (i : Inputs) (st : State)
    (hp : ParamsOK p) :
    (step p on i st).N ≤ (step p { on with war := false } i st).N := by
  have h := nWar_le p on i (nGrown p st i.weather) hp (nGrown_nonneg p st i.weather)
  have hoff : nWar p { on with war := false } i (nGrown p st i.weather)
      = nGrown p st i.weather := by
    unfold nWar warOn
    simp
  show nWar p on i (nGrown p st i.weather) ≤ nWar p { on with war := false } i (nGrown p st i.weather)
  rw [hoff]
  exact h

/-- Compared with the same year with the war switch off, the war year's B is no larger. -/
theorem war_does_not_raise_B (p : Params) (on : Switches) (i : Inputs) (st : State)
    (hp : ParamsOK p) :
    (step p on i st).B ≤ (step p { on with war := false } i st).B := by
  have h := bWar_le p on i (bGrown p st i.weather) hp (bGrown_nonneg p st i.weather)
  have hoff : bWar p { on with war := false } i (bGrown p st i.weather)
      = bGrown p st i.weather := by
    unfold bWar warOn
    simp
  show bWar p on i (bGrown p st i.weather) ≤ bWar p { on with war := false } i (bGrown p st i.weather)
  rw [hoff]
  exact h

/-! ## Counterexample: a war year can raise E (all parameters inside the drawPriors ranges) -/

/-- Witness parameters. Each value lies in its drawPriors range: attrition .04 in [.02,.06];
bondedShare .08 (consistent with a draw u = .0032 in [.0028,.0038] and attrition .04);
bondedWork .5, corvee .05, slack 1.5, growth .02, famine .5, follow .01, decay .05, buffer .5,
channelGain .2, contestCut .4, warLoss .1, warFlight .5, orgyShare .7, templeUpkeep .01,
theravadaFloor .4, silt .1, court .1, outside0 .6, outside1 1.2. -/
def witnessParams : Params :=
  { attrition := 4 / 100, bondedShare := 8 / 100, bondedWork := 1 / 2, corvee := 1 / 20,
    slack := 3 / 2, growth := 1 / 50, famine := 1 / 2, follow := 1 / 100, decay := 1 / 20,
    buffer := 1 / 2, channelGain := 1 / 5, contestCut := 2 / 5, warLoss := 1 / 10,
    warFlight := 1 / 2, orgyShare := 7 / 10, templeUpkeep := 1 / 100, silt := 1 / 10,
    court := 1 / 10, outside0 := 3 / 5, outside1 := 6 / 5, theravadaFloor := 2 / 5 }

/-- Witness year: attack year 1353, weather 1, full cohesion, logistic inputs 1/2. -/
def witnessInputs : Inputs :=
  { year := 1353, weather := 1, cohesion := 1, devotionLogistic := 1 / 2, tradeLogistic := 1 / 2 }

/-- Witness state: N = 1, B = 7/100, C = 1, E = 0, S = N + B, M = 0. -/
def witnessState : State :=
  { N := 1, B := 7 / 100, C := 1, E := 0, S := 107 / 100, M := 0 }

/-- With war and trade on, E after the attack year exceeds E without the war hit.
Stated against the no-war counterfactual. This is a claim that a war year can raise E,
so the "war does not raise E" target is false in range. -/
def witnessOn : Switches := ⟨true, false, false, true, false, false⟩

def witnessOff : Switches := ⟨false, false, false, true, false, false⟩

-- NOT PROVED IN LEAN: the claim that the war-year E exceeds the no-war E at this witness
-- (exact-fraction check outside Lean: 2102072/1408296075 with war, 0 without). `decide` cannot
-- reduce the Rat order instances (stuck at Int.decLt), so no theorem is stated here.

end Angkor.Monsoon
