import Angkor.Basic

/-!
# Obligations engine: one year-step and iteration over an input list

Source: `public/engines/obligations.js`. Line numbers in the doc comments refer to that file.
Constants: lines 4-5. The loop body is lines 13-48. `compare` (lines 52-63) is not formalized.
The upstream rows `(year, harvestShock, tributeReceived)` are an explicit input list. The
Signalling module is not imported.

Arithmetic is exact `Rat`. The theorems are about ideal rational arithmetic, not IEEE
floating point. The JS tolerance `1e-8` is the exact rational `1/100000000`.
There is no division by a variable in the step, so no division-by-zero obligations arise.
The `??=` operators are modelled by `setOnce`.

Bounds and nonnegativity hold under `ParamsOK` (externalShare, rigidity, disruption in
`[0,1]`) and for inputs with `harvestShock >= 0`. The state invariant is `Good`.
-/

namespace Angkor.Obligations

/-- The return rule option, `returnRule` (line 3 default `'closed'`, line 22 test `'open'`). -/
inductive ReturnRule where
  | closed
  | open_
  deriving DecidableEq

/-- Parameters entering one step. Line 3 defaults, line 8 `p`. `supplier` and `seed` only
feed the upstream call (line 9) and are not part of the step. `duration` counts years. -/
structure Params where
  externalShare : Rat
  rigidity : Rat
  disruption : Rat
  duration : Int
  returnRule : ReturnRule

/-- The parameter ranges assumed by the bound theorems. -/
structure ParamsOK (p : Params) : Prop where
  share_nonneg : 0 ≤ p.externalShare
  share_le : p.externalShare ≤ 1
  rigidity_nonneg : 0 ≤ p.rigidity
  rigidity_le : p.rigidity ≤ 1
  disruption_nonneg : 0 ≤ p.disruption
  disruption_le : p.disruption ≤ 1

/-- Constants, source line 4 (`fullReceipts`, `ritualBill`, `courtBill`, `storageCapacity`,
`lossRate`) and line 5 (`startingReserve`, `disruptionStart`, `missedYearsToExit`). -/
def fullReceipts : Rat := 200
def ritualBill : Rat := 40
def courtBill : Rat := 130
def startingReserve : Rat := 70
def storageCapacity : Rat := 100
/-- JS `.10`, exact `1/10`. -/
def lossRate : Rat := 1 / 10
def disruptionStart : Int := 4
def missedYearsToExit : Int := 2
/-- JS `1e-8`, source line 34. Exact `1/100000000`. -/
def tolerance : Rat := 1 / 100000000

/-- State: `reserve`, `arrears`, `missed`, `exitYear`, `returnYear`, `elitePresent`.
Source lines 10-11. -/
structure State where
  reserve : Rat
  arrears : Rat
  missed : Int
  exitYear : Option Int
  returnYear : Option Int
  elitePresent : Bool

/-- One upstream row, source line 14. -/
structure Input where
  year : Int
  harvestShock : Rat
  tributeReceived : Rat

/-- Initial state, source lines 10-11: `reserve = startingReserve`, `arrears = 0`, `missed = 0`,
no exit or return year, elite present. -/
def initial : State where
  reserve := startingReserve
  arrears := 0
  missed := 0
  exitYear := none
  returnYear := none
  elitePresent := true

/-- Source line 17: `year >= disruptionStart && year < disruptionStart + duration`. -/
def interrupted (p : Params) (year : Int) : Bool :=
  decide (disruptionStart ≤ year ∧ year < disruptionStart + p.duration)

/-- Source line 18. Uses the elite status before this year's return check (lines 22-27). -/
def deliveryFraction (p : Params) (s : State) (x : Input) : Rat :=
  if (s.elitePresent || p.returnRule == .open_) && decide (0 < x.tributeReceived) then
    1 - (if interrupted p x.year then p.disruption else 0)
  else 0

/-- Source line 19: `fullReceipts * (1 - externalShare) * harvestShock`. -/
def localReceipts (p : Params) (x : Input) : Rat :=
  fullReceipts * (1 - p.externalShare) * x.harvestShock

/-- Source line 20: `fullReceipts * externalShare * deliveryFraction`. -/
def externalReceipts (p : Params) (s : State) (x : Input) : Rat :=
  fullReceipts * p.externalShare * deliveryFraction p s x

/-- Source line 16: `spoiled = open * lossRate`. -/
def spoiled (s : State) : Rat := s.reserve * lossRate

/-- Source line 21: `open - spoiled + local + external`. -/
def available (p : Params) (s : State) (x : Input) : Rat :=
  s.reserve - spoiled s + localReceipts p x + externalReceipts p s x

/-- Source lines 22-23: `returned` flag. -/
def returned (p : Params) (s : State) (x : Input) : Bool :=
  !s.elitePresent && p.returnRule == .open_ && decide (0 < externalReceipts p s x) &&
    decide (ritualBill + courtBill ≤ available p s x)

/-- Source line 28: `presentAtPayment = elitePresent`, read after the return branch (24-27). -/
def presentAtPayment (p : Params) (s : State) (x : Input) : Bool :=
  s.elitePresent || returned p s x

/-- Source line 29: `Math.min(ritualBill, available)`. -/
def ritualPaid (p : Params) (s : State) (x : Input) : Rat :=
  min ritualBill (available p s x)

/-- Source line 30: `courtBill * (rigidity + (1-rigidity)*deliveryFraction)` if present, else 0. -/
def courtDue (p : Params) (s : State) (x : Input) : Rat :=
  if presentAtPayment p s x = true then
    courtBill * (p.rigidity + (1 - p.rigidity) * deliveryFraction p s x)
  else 0

/-- Source line 31: `Math.min(courtDue, available - ritualPaid)`. -/
def courtPaid (p : Params) (s : State) (x : Input) : Rat :=
  min (courtDue p s x) (available p s x - ritualPaid p s x)

/-- Source line 32: `courtDue - courtPaid`. -/
def unpaid (p : Params) (s : State) (x : Input) : Rat :=
  courtDue p s x - courtPaid p s x

/-- Source line 34 before the exit reset: `unpaid > 1e-8 ? missed + 1 : 0`. -/
def missedAfter (p : Params) (s : State) (x : Input) : Int :=
  if tolerance < unpaid p s x then s.missed + 1 else 0

/-- Source line 35: `elitePresent && missed >= missedYearsToExit`. -/
def exited (p : Params) (s : State) (x : Input) : Bool :=
  presentAtPayment p s x && decide (missedYearsToExit ≤ missedAfter p s x)

/-- Source lines 36-40: the counter is reset to 0 on exit. -/
def missedFinal (p : Params) (s : State) (x : Input) : Int :=
  if exited p s x = true then 0 else missedAfter p s x

/-- JS `??=`: keep the existing value, else set it to `y`. -/
def setOnce (o : Option Int) (y : Int) : Option Int :=
  match o with
  | some z => some z
  | none => some y

/-- Source line 37: `exitYear ??= year` on exit. -/
def exitYearNext (p : Params) (s : State) (x : Input) : Option Int :=
  if exited p s x = true then setOnce s.exitYear x.year else s.exitYear

/-- Source line 26: `returnYear ??= year` on return. -/
def returnYearNext (p : Params) (s : State) (x : Input) : Option Int :=
  if returned p s x = true then setOnce s.returnYear x.year else s.returnYear

/-- Source lines 38 and 25: elite present after return and not exited. -/
def elitePresentNext (p : Params) (s : State) (x : Input) : Bool :=
  presentAtPayment p s x && !exited p s x

/-- Source line 41: `available - ritualPaid - courtPaid`. -/
def unspent (p : Params) (s : State) (x : Input) : Rat :=
  available p s x - ritualPaid p s x - courtPaid p s x

/-- Source line 42: `Math.min(storageCapacity, unspent)`. -/
def reserveNext (p : Params) (s : State) (x : Input) : Rat :=
  min storageCapacity (unspent p s x)

/-- Source line 43: `unspent - reserve`. -/
def overflow (p : Params) (s : State) (x : Input) : Rat :=
  unspent p s x - reserveNext p s x

/-- Source line 47: `available - ritualPaid - courtPaid - overflow - reserve`. -/
def balanceError (p : Params) (s : State) (x : Input) : Rat :=
  available p s x - ritualPaid p s x - courtPaid p s x - overflow p s x - reserveNext p s x

/-- One year-step, source lines 15-47, in source order. -/
def step (p : Params) (s : State) (x : Input) : State where
  reserve := reserveNext p s x
  arrears := s.arrears + unpaid p s x
  missed := missedFinal p s x
  exitYear := exitYearNext p s x
  returnYear := returnYearNext p s x
  elitePresent := elitePresentNext p s x

/-- Iteration over the input list (source lines 13-48, `for (const input of upstream.rows)`). -/
def run (p : Params) : State → List Input → State
  | s, [] => s
  | s, x :: xs => run p (step p s x) xs

/-! ## Balance -/

/-- Target 1: the balance error is exactly zero, for every state, input and parameter. -/
theorem balanceError_eq_zero (p : Params) (s : State) (x : Input) :
    balanceError p s x = 0 := by
  unfold balanceError overflow unspent
  grind

/-! ## Ritual priority -/

/-- Target 3: if any court is paid, the ritual was paid in full. -/
theorem ritual_priority (p : Params) (s : State) (x : Input)
    (h : 0 < courtPaid p s x) : ritualPaid p s x = ritualBill := by
  unfold courtPaid ritualPaid at *
  grind

/-! ## Bounds (per step) -/

/-- Invariant on states: reserve in `[0, storageCapacity]`, arrears and missed nonnegative,
and an absent elite has a zero miss counter. -/
structure Good (s : State) : Prop where
  reserve_nonneg : 0 ≤ s.reserve
  reserve_le : s.reserve ≤ storageCapacity
  arrears_nonneg : 0 ≤ s.arrears
  missed_nonneg : 0 ≤ s.missed
  absent_no_miss : s.elitePresent = false → s.missed = 0

/-- The initial state satisfies `Good`. -/
theorem initial_good : Good initial where
  reserve_nonneg := by unfold initial startingReserve; decide
  reserve_le := by unfold initial startingReserve storageCapacity; decide
  arrears_nonneg := by unfold initial; decide
  missed_nonneg := by unfold initial; decide
  absent_no_miss := by
    intro h
    simp [initial] at h

theorem deliveryFraction_bounds (p : Params) (s : State) (x : Input) (hp : ParamsOK p) :
    0 ≤ deliveryFraction p s x ∧ deliveryFraction p s x ≤ 1 := by
  have h1 := hp.disruption_nonneg
  have h2 := hp.disruption_le
  unfold deliveryFraction
  grind

theorem localReceipts_nonneg (p : Params) (x : Input) (hp : ParamsOK p)
    (hx : 0 ≤ x.harvestShock) : 0 ≤ localReceipts p x := by
  have hs := hp.share_le
  have h1 : (0 : Rat) ≤ 1 - p.externalShare := by grind
  have h2 := Rat.mul_nonneg h1 hx
  unfold localReceipts fullReceipts
  grind

theorem externalReceipts_nonneg (p : Params) (s : State) (x : Input) (hp : ParamsOK p) :
    0 ≤ externalReceipts p s x := by
  have hs := hp.share_nonneg
  have hf := (deliveryFraction_bounds p s x hp).1
  have h1 : (0 : Rat) ≤ fullReceipts * p.externalShare := by
    unfold fullReceipts; grind
  have h2 := Rat.mul_nonneg h1 hf
  unfold externalReceipts
  exact h2

theorem available_nonneg (p : Params) (s : State) (x : Input) (hp : ParamsOK p)
    (hs : Good s) (hx : 0 ≤ x.harvestShock) : 0 ≤ available p s x := by
  have hl := localReceipts_nonneg p x hp hx
  have he := externalReceipts_nonneg p s x hp
  have hr := hs.reserve_nonneg
  unfold available spoiled lossRate
  grind

theorem ritualPaid_bounds (p : Params) (s : State) (x : Input) (hp : ParamsOK p)
    (hs : Good s) (hx : 0 ≤ x.harvestShock) :
    0 ≤ ritualPaid p s x ∧ ritualPaid p s x ≤ ritualBill := by
  have ha := available_nonneg p s x hp hs hx
  have hb : (0 : Rat) ≤ ritualBill := by unfold ritualBill; decide
  unfold ritualPaid
  grind

theorem ritualPaid_le_available (p : Params) (s : State) (x : Input) :
    ritualPaid p s x ≤ available p s x := by
  unfold ritualPaid
  grind

theorem courtDue_bounds (p : Params) (s : State) (x : Input) (hp : ParamsOK p) :
    0 ≤ courtDue p s x ∧ courtDue p s x ≤ courtBill := by
  have hf := deliveryFraction_bounds p s x hp
  have hr0 := hp.rigidity_nonneg
  have hr1 := hp.rigidity_le
  have hc : (0 : Rat) ≤ courtBill := by unfold courtBill; decide
  have h1 : (0 : Rat) ≤ (1 - p.rigidity) * deliveryFraction p s x :=
    Rat.mul_nonneg (by grind) hf.1
  have h2 : (0 : Rat) ≤ (1 - p.rigidity) * (1 - deliveryFraction p s x) :=
    Rat.mul_nonneg (by grind) (by grind)
  have h3 : (0 : Rat) ≤ courtBill * (1 - (p.rigidity + (1 - p.rigidity) * deliveryFraction p s x)) :=
    Rat.mul_nonneg hc (by grind)
  have h4 : (0 : Rat) ≤ courtBill * (p.rigidity + (1 - p.rigidity) * deliveryFraction p s x) :=
    Rat.mul_nonneg hc (by grind)
  unfold courtDue
  by_cases h : presentAtPayment p s x = true
  · rw [if_pos h]
    constructor
    · exact h4
    · grind
  · rw [if_neg h]
    constructor
    · exact Rat.le_refl
    · exact hc

theorem courtPaid_bounds (p : Params) (s : State) (x : Input) (hp : ParamsOK p)
    (hs : Good s) (hx : 0 ≤ x.harvestShock) :
    0 ≤ courtPaid p s x ∧ courtPaid p s x ≤ courtDue p s x ∧
      courtPaid p s x ≤ available p s x - ritualPaid p s x := by
  have hcd := courtDue_bounds p s x hp
  have hrp := ritualPaid_le_available p s x
  have hrb := ritualPaid_bounds p s x hp hs hx
  have ha := available_nonneg p s x hp hs hx
  unfold courtPaid
  grind

theorem unpaid_nonneg (p : Params) (s : State) (x : Input) (hp : ParamsOK p)
    (hs : Good s) (hx : 0 ≤ x.harvestShock) : 0 ≤ unpaid p s x := by
  have h := courtPaid_bounds p s x hp hs hx
  unfold unpaid
  grind

theorem unspent_nonneg (p : Params) (s : State) (x : Input) (hp : ParamsOK p)
    (hs : Good s) (hx : 0 ≤ x.harvestShock) : 0 ≤ unspent p s x := by
  have h := courtPaid_bounds p s x hp hs hx
  unfold unspent
  grind

theorem reserveNext_bounds (p : Params) (s : State) (x : Input) (hp : ParamsOK p)
    (hs : Good s) (hx : 0 ≤ x.harvestShock) :
    0 ≤ reserveNext p s x ∧ reserveNext p s x ≤ storageCapacity := by
  have hu := unspent_nonneg p s x hp hs hx
  have hc : (0 : Rat) ≤ storageCapacity := by unfold storageCapacity; decide
  unfold reserveNext
  grind

/-- Target 2, overflow: `overflow >= 0` in every step. -/
theorem overflow_nonneg (p : Params) (s : State) (x : Input) (hp : ParamsOK p)
    (hs : Good s) (hx : 0 ≤ x.harvestShock) : 0 ≤ overflow p s x := by
  have hu := unspent_nonneg p s x hp hs hx
  have hm : reserveNext p s x ≤ unspent p s x := by
    unfold reserveNext; grind
  unfold overflow
  grind

/-- If the elite is absent at payment, the court due is 0, so the unpaid amount is 0 and the
miss counter does not advance. -/
theorem missedAfter_absent (p : Params) (s : State) (x : Input) (hp : ParamsOK p)
    (hs : Good s) (hx : 0 ≤ x.harvestShock) (h : presentAtPayment p s x = false) :
    missedAfter p s x = 0 := by
  have hcd : courtDue p s x = 0 := by
    unfold courtDue; simp [h]
  have hy : 0 ≤ available p s x - ritualPaid p s x := by
    have := ritualPaid_le_available p s x
    have := available_nonneg p s x hp hs hx
    grind
  have hcp : courtPaid p s x = 0 := by
    unfold courtPaid; grind
  have hu : unpaid p s x = 0 := by
    unfold unpaid; grind
  unfold missedAfter
  have hn : ¬ (tolerance < (0 : Rat)) := by
    unfold tolerance; grind
  rw [hu, if_neg hn]

/-- The step preserves the state invariant `Good`. -/
theorem step_good (p : Params) (s : State) (x : Input) (hp : ParamsOK p) (hs : Good s)
    (hx : 0 ≤ x.harvestShock) : Good (step p s x) where
  reserve_nonneg := (reserveNext_bounds p s x hp hs hx).1
  reserve_le := (reserveNext_bounds p s x hp hs hx).2
  arrears_nonneg := by
    show 0 ≤ s.arrears + unpaid p s x
    have := unpaid_nonneg p s x hp hs hx
    have := hs.arrears_nonneg
    grind
  missed_nonneg := by
    show 0 ≤ missedFinal p s x
    unfold missedFinal missedAfter
    have := hs.missed_nonneg
    split <;> grind
  absent_no_miss := by
    intro h
    show missedFinal p s x = 0
    have h' : (presentAtPayment p s x && !exited p s x) = false := h
    unfold missedFinal
    by_cases hpres : presentAtPayment p s x = true
    · rw [hpres, Bool.true_and] at h'
      have he : exited p s x = true := by simpa using h'
      simp [he]
    · have hpres' : presentAtPayment p s x = false := by simpa using hpres
      have he : exited p s x = false := by
        unfold exited; simp [hpres']
      simp [he, missedAfter_absent p s x hp hs hx hpres']

/-- Iterating over any list keeps the invariant, provided all harvest shocks are nonnegative. -/
theorem run_good (p : Params) (hp : ParamsOK p) :
    ∀ (xs : List Input) (s : State), Good s → (∀ x ∈ xs, 0 ≤ x.harvestShock) → Good (run p s xs)
  | [], s, hs, _ => hs
  | x :: xs, s, hs, hx =>
      run_good p hp xs (step p s x) (step_good p s x hp hs (hx x (by simp)))
        (fun y hy => hx y (by simp [hy]))

/-- Arrears never decrease, over any number of steps. -/
theorem run_arrears_mono (p : Params) (hp : ParamsOK p) :
    ∀ (xs : List Input) (s : State), Good s → (∀ x ∈ xs, 0 ≤ x.harvestShock) →
      s.arrears ≤ (run p s xs).arrears
  | [], s, _, _ => Rat.le_refl
  | x :: xs, s, hs, hx => by
      have hu := unpaid_nonneg p s x hp hs (hx x (by simp))
      have ih := run_arrears_mono p hp xs (step p s x) (step_good p s x hp hs (hx x (by simp)))
        (fun y hy => hx y (by simp [hy]))
      show s.arrears ≤ (run p (step p s x) xs).arrears
      have hsa : s.arrears ≤ (step p s x).arrears := by
        show s.arrears ≤ s.arrears + unpaid p s x
        grind
      exact Rat.le_trans hsa ih

/-! ## Exit and return -/

/-- Exit needs the miss counter to reach `missedYearsToExit`; each exit year is preceded by a
shortfall. A single shortfall year in a state with `missed = 0` is not enough. -/
theorem missed_pos_imp_shortfall (p : Params) (s : State) (x : Input)
    (h : 0 < missedFinal p s x) : tolerance < unpaid p s x := by
  unfold missedFinal missedAfter at h
  split at h <;> grind

/-- Target 4: an exit at year `x1` after year `x0` requires shortfalls (above the tolerance) in both
years. -/
theorem exit_needs_two_consecutive_shortfalls (p : Params) (s : State) (x0 x1 : Input)
    (h : exited p (step p s x0) x1 = true) :
    tolerance < unpaid p s x0 ∧ tolerance < unpaid p (step p s x0) x1 := by
  have hm : 2 ≤ missedAfter p (step p s x0) x1 := by
    unfold exited at h
    simp only [Bool.and_eq_true, decide_eq_true_eq] at h
    exact h.2
  have hsh1 : tolerance < unpaid p (step p s x0) x1 := by
    unfold missedAfter at hm
    split at hm <;> grind
  have hpos : 0 < missedFinal p s x0 := by
    unfold missedAfter at hm
    have hstate : (step p s x0).missed = missedFinal p s x0 := rfl
    split at hm
    · grind
    · grind
  exact ⟨missed_pos_imp_shortfall p s x0 hpos, hsh1⟩

/-- Target 4: no exit in the first year of a run from the initial state. -/
theorem no_exit_first_step (p : Params) (x : Input) :
    exited p initial x = false := by
  have h : missedAfter p initial x ≤ 1 := by
    have hm0 : initial.missed = 0 := rfl
    unfold missedAfter
    split <;> omega
  have hn : ¬ (missedYearsToExit ≤ missedAfter p initial x) := by
    unfold missedYearsToExit; omega
  unfold exited
  simp [hn]

/-- Target 4: `exitYear` is set once and never changes. -/
theorem exitYear_stable (p : Params) (s : State) (x : Input) (y : Int)
    (h : s.exitYear = some y) : (step p s x).exitYear = some y := by
  show exitYearNext p s x = some y
  unfold exitYearNext setOnce
  split <;> simp [h]

theorem run_exitYear_stable (p : Params) :
    ∀ (xs : List Input) (s : State) (y : Int), s.exitYear = some y →
      (run p s xs).exitYear = some y
  | [], s, y, h => h
  | x :: xs, s, y, h =>
      run_exitYear_stable p xs (step p s x) y (exitYear_stable p s x y h)

/-- Under `returnRule = closed`, the return branch never fires. -/
theorem returned_closed (p : Params) (s : State) (x : Input) (hc : p.returnRule = .closed) :
    returned p s x = false := by
  unfold returned
  simp [hc]

/-- Target 4: under `closed`, an elite who is gone never returns. -/
theorem closed_absent_stays (p : Params) (s : State) (x : Input) (hc : p.returnRule = .closed)
    (h : s.elitePresent = false) : (step p s x).elitePresent = false := by
  have hr := returned_closed p s x hc
  show (presentAtPayment p s x && !exited p s x) = false
  simp [presentAtPayment, hr, h]

theorem run_closed_absent_stays (p : Params) (hc : p.returnRule = .closed) :
    ∀ (xs : List Input) (s : State), s.elitePresent = false → (run p s xs).elitePresent = false
  | [], s, h => h
  | x :: xs, s, h =>
      run_closed_absent_stays p hc xs (step p s x) (closed_absent_stays p s x hc h)

/-- Under `closed`, the return year is never set. -/
theorem closed_returnYear_fixed (p : Params) (s : State) (x : Input) (hc : p.returnRule = .closed) :
    (step p s x).returnYear = s.returnYear := by
  show returnYearNext p s x = s.returnYear
  unfold returnYearNext
  simp [returned_closed p s x hc]

/-- Target 4: a return only happens with enough cash for the ritual and court bills. -/
theorem returned_budget (p : Params) (s : State) (x : Input)
    (h : returned p s x = true) : ritualBill + courtBill ≤ available p s x := by
  unfold returned at h
  grind

/-- Target 5: exit and return cannot occur in the same year. The hypothesis is the invariant
that an absent elite has a zero miss counter, which holds in every reachable state. -/
theorem exit_and_return_same_year_impossible (p : Params) (s : State) (x : Input)
    (hmiss : s.elitePresent = false → s.missed = 0) :
    ¬ (returned p s x = true ∧ exited p s x = true) := by
  rintro ⟨hr, he⟩
  have hab : s.elitePresent = false := by
    unfold returned at hr
    grind
  have hm := hmiss hab
  unfold exited presentAtPayment missedAfter at he
  unfold missedYearsToExit at he
  grind

/-- The invariant holds along any run, so the same-year impossibility holds at every year of
any run from the initial state. -/
theorem same_year_impossible_reachable (p : Params) (hp : ParamsOK p) (xs : List Input)
    (hx : ∀ x ∈ xs, 0 ≤ x.harvestShock) (x : Input) :
    ¬ (returned p (run p initial xs) x = true ∧ exited p (run p initial xs) x = true) :=
  exit_and_return_same_year_impossible p (run p initial xs) x
    (run_good p hp xs initial initial_good hx).absent_no_miss

/-! ## The 1e-8 tolerance -/

/-- A shortfall at most the tolerance resets the counter and is not counted as missed. -/
theorem tolerance_resets_counter (p : Params) (s : State) (x : Input)
    (h : unpaid p s x ≤ tolerance) : missedAfter p s x = 0 := by
  unfold missedAfter
  grind

/-- Witness parameters: externalShare 0, rigidity 0, disruption 0, closed rule. Each is on the
lower bound of its UI range (externalShare 0 to 0.9, rigidity 0 to 1, disruption 0 to 1,
`public/worlds.js` lines 413-415), so 0 is an in-range value. -/
def witnessParams : Params where
  externalShare := 0
  rigidity := 0
  disruption := 0
  duration := 3
  returnRule := .closed

/-- Hand-chosen witness state: elite present, one prior missed year, empty reserve. It is NOT
shown reachable from `initial` under the engine's harvest range; the tolerance theorems use it
only as a state to test the one-step rule. (The reachable in-range exit is
`disruption_zero_exit_in_range`, which reaches reserve 0 and missed 1 in year 4.) -/
def witnessState : State where
  reserve := 0
  arrears := 0
  missed := 1
  exitYear := none
  returnYear := none
  elitePresent := true

/-- Witness input with available cash `200 * h`. -/
def witnessInput (h : Rat) : Input where
  year := 1
  harvestShock := h
  tributeReceived := 1

/-- In the witness, a present elite with positive tribute pays a full delivery fraction of 1
(`disruption = 0`, so the interruption does not matter). -/
theorem witness_df (s : State) (y : Int) (h T : Rat) (hT : 0 < T) (hP : s.elitePresent = true) :
    deliveryFraction witnessParams s ⟨y, h, T⟩ = 1 := by
  unfold deliveryFraction
  rw [if_pos (by simp [hP, hT])]
  have hd0 : witnessParams.disruption = 0 := rfl
  grind

/-- Unpaid court dues in the witness state as a function of the harvest shock `h`, when the
available cash `200 * h` lies between the ritual and the full court bill. -/
theorem witness_unpaid (h : Rat) (h1 : 40 ≤ 200 * h) (h2 : 200 * h ≤ 170) :
    unpaid witnessParams witnessState (witnessInput h) = 170 - 200 * h := by
  have hdf : deliveryFraction witnessParams witnessState (witnessInput h) = 1 :=
    witness_df witnessState 1 h 1 (by grind) rfl
  have hpres : presentAtPayment witnessParams witnessState (witnessInput h) = true := by
    simp [presentAtPayment, witnessState]
  have hav : available witnessParams witnessState (witnessInput h) = 200 * h := by
    simp [available, spoiled, localReceipts, externalReceipts, witnessParams, witnessState,
      witnessInput, fullReceipts, lossRate] <;> grind
  have hcd : courtDue witnessParams witnessState (witnessInput h) = 130 := by
    unfold courtDue
    rw [if_pos hpres, hdf]
    simp [witnessParams, courtBill] <;> grind
  have hrp : ritualPaid witnessParams witnessState (witnessInput h) = 40 := by
    unfold ritualPaid
    rw [hav]
    unfold ritualBill
    grind
  have hcp : courtPaid witnessParams witnessState (witnessInput h) = 200 * h - 40 := by
    unfold courtPaid
    rw [hcd, hrp, hav]
    grind
  unfold unpaid
  rw [hcd, hcp]
  grind

/-- Target 5 (tolerance): with available `170 - 1e-8`, the court shortfall is exactly `1e-8`.
It is not counted (`1e-8` is not `> 1e-8`), so the counter resets and no exit occurs. The
arrears still rise by exactly `1e-8`. -/
theorem tolerance_hides_shortfall :
    unpaid witnessParams witnessState (witnessInput ((170 - 1 / 100000000) / 200)) =
        1 / 100000000 ∧
      missedAfter witnessParams witnessState (witnessInput ((170 - 1 / 100000000) / 200)) = 0 ∧
      exited witnessParams witnessState (witnessInput ((170 - 1 / 100000000) / 200)) = false ∧
      (step witnessParams witnessState (witnessInput ((170 - 1 / 100000000) / 200))).arrears =
        1 / 100000000 := by
  have hu : unpaid witnessParams witnessState (witnessInput ((170 - 1 / 100000000) / 200)) =
      1 / 100000000 := by
    rw [witness_unpaid ((170 - 1 / 100000000) / 200) (by grind) (by grind)]
    grind
  have hm : missedAfter witnessParams witnessState (witnessInput ((170 - 1 / 100000000) / 200)) =
      0 := by
    unfold missedAfter
    have hn : ¬ (tolerance < unpaid witnessParams witnessState
        (witnessInput ((170 - 1 / 100000000) / 200))) := by
      rw [hu]
      unfold tolerance
      grind
    rw [if_neg hn]
  have hex : exited witnessParams witnessState (witnessInput ((170 - 1 / 100000000) / 200)) =
      false := by
    unfold exited
    rw [hm]
    simp [presentAtPayment, witnessState, missedYearsToExit]
  refine ⟨hu, hm, hex, ?_⟩
  show witnessState.arrears +
      unpaid witnessParams witnessState (witnessInput ((170 - 1 / 100000000) / 200)) = _
  rw [hu]
  show (0 : Rat) + 1 / 100000000 = 1 / 100000000
  grind

/-- Contrast: a shortfall of `2e-8` is counted, so the same state exits. -/
theorem shortfall_above_tolerance_exits :
    exited witnessParams witnessState (witnessInput ((170 - 2 / 100000000) / 200)) = true := by
  have hu : unpaid witnessParams witnessState (witnessInput ((170 - 2 / 100000000) / 200)) =
      2 / 100000000 := by
    rw [witness_unpaid ((170 - 2 / 100000000) / 200) (by grind) (by grind)]
    grind
  have hlt : tolerance < unpaid witnessParams witnessState
      (witnessInput ((170 - 2 / 100000000) / 200)) := by
    rw [hu]
    unfold tolerance
    grind
  have hm : missedAfter witnessParams witnessState (witnessInput ((170 - 2 / 100000000) / 200)) =
      2 := by
    unfold missedAfter
    rw [if_pos hlt]
    simp [witnessState]
  unfold exited
  rw [hm]
  simp [presentAtPayment, witnessState, missedYearsToExit]

/-! ## Disruption zero -/

/-- Target 6: with `disruption = 0`, the year (and hence whether it is interrupted) does not
change reserve, arrears, missed counter or elite presence. -/
theorem disruption_zero_year_irrelevant (p : Params) (hd : p.disruption = 0) (s : State)
    (h T : Rat) (y y' : Int) :
    (step p s ⟨y, h, T⟩).reserve = (step p s ⟨y', h, T⟩).reserve ∧
      (step p s ⟨y, h, T⟩).arrears = (step p s ⟨y', h, T⟩).arrears ∧
      (step p s ⟨y, h, T⟩).missed = (step p s ⟨y', h, T⟩).missed ∧
      (step p s ⟨y, h, T⟩).elitePresent = (step p s ⟨y', h, T⟩).elitePresent := by
  have hfy : ∀ z : Int, deliveryFraction p s ⟨z, h, T⟩ =
      (if (s.elitePresent || p.returnRule == .open_) && decide (0 < T) then 1 else 0) := by
    intro z
    unfold deliveryFraction
    grind
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
    simp only [step, reserveNext, unspent, available, spoiled, localReceipts, externalReceipts,
      ritualPaid, courtDue, courtPaid, unpaid, presentAtPayment, returned, missedAfter,
      missedFinal, exited, elitePresentNext, hfy]

/-! ## Exit witness inside the engine's harvest range

The engine draws `harvestShock = .78 + .44 * draw()` (`src/models/signalling.js` line 23), so
every harvest shock lies in `[0.78, 1.22)`. The witness below uses the lowest in-range value
`39/50 = 0.78` in every year, starting from `initial` (not hand-chosen). Its parameters
are `witnessParams` (externalShare 0, rigidity 0, disruption 0). These sit on the lower
bounds of the UI ranges (`public/worlds.js` line 413-415 and `public/research/control-audit.json`:
externalShare 0 to 0.9, rigidity 0 to 1, disruption 0 to 1). The witness needs tribute `> 0`.
The trajectory is 70 -> 49 -> 30.1 -> 13.09 -> 0 in reserve, with shortfalls in years 4 and 5,
so the elite exits in year 5. -/

/-- Court-level facts for a present elite with full delivery at harvest `39/50`. -/
theorem W_facts (s : State) (y : Int) (T : Rat) (hT : 0 < T) (hP : s.elitePresent = true) :
    presentAtPayment witnessParams s ⟨y, 39 / 50, T⟩ = true ∧
      courtDue witnessParams s ⟨y, 39 / 50, T⟩ = 130 ∧
      available witnessParams s ⟨y, 39 / 50, T⟩ = s.reserve * (9 / 10) + 156 := by
  have hd := witness_df s y (39 / 50) T hT hP
  have hpa : presentAtPayment witnessParams s ⟨y, 39 / 50, T⟩ = true := by
    simp [presentAtPayment, hP]
  refine ⟨hpa, ?_, ?_⟩
  · unfold courtDue
    rw [if_pos hpa, hd]
    simp [witnessParams, courtBill] <;> grind
  · unfold available spoiled localReceipts externalReceipts
    rw [hd]
    simp [witnessParams, fullReceipts, lossRate] <;> grind

/-- Unpaid court bill once the court bill is 130 (ritual paid first). -/
theorem W_unpaid_eq (s : State) (x : Input) (hcd : courtDue witnessParams s x = 130) :
    unpaid witnessParams s x =
      130 - min 130 (available witnessParams s x - min ritualBill (available witnessParams s x)) := by
  unfold unpaid courtPaid ritualPaid
  rw [hcd]

/-- Unspent cash once the court bill is 130. -/
theorem W_unspent_eq (s : State) (x : Input) (hcd : courtDue witnessParams s x = 130) :
    unspent witnessParams s x =
      available witnessParams s x - min ritualBill (available witnessParams s x) -
        min 130 (available witnessParams s x - min ritualBill (available witnessParams s x)) := by
  unfold unspent courtPaid ritualPaid
  rw [hcd]

/-- Witness year 1 (reserve 70, no shortfall). -/
theorem wY1 (s : State) (y : Int) (T : Rat) (hT : 0 < T) (hP : s.elitePresent = true)
    (hx : s.exitYear = none) (hr : s.reserve = 70) (hm : s.missed = 0) :
    (step witnessParams s ⟨y, 39 / 50, T⟩).reserve = 49 ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).missed = 0 ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).elitePresent = true ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).exitYear = none := by
  obtain ⟨hpa, hcd, hav⟩ := W_facts s y T hT hP
  rw [hr] at hav
  have hu : unpaid witnessParams s ⟨y, 39 / 50, T⟩ = 0 := by
    rw [W_unpaid_eq s _ hcd, hav]
    unfold ritualBill
    grind
  have hun : unspent witnessParams s ⟨y, 39 / 50, T⟩ = 49 := by
    rw [W_unspent_eq s _ hcd, hav]
    unfold ritualBill
    grind
  have hlt : ¬ tolerance < unpaid witnessParams s ⟨y, 39 / 50, T⟩ := by
    rw [hu]
    unfold tolerance
    grind
  have hma : missedAfter witnessParams s ⟨y, 39 / 50, T⟩ = 0 := by
    unfold missedAfter
    rw [if_neg hlt]
  have hex : exited witnessParams s ⟨y, 39 / 50, T⟩ = false := by
    unfold exited
    rw [hma, hpa]
    simp [missedYearsToExit]
  refine ⟨?_, ?_, ?_, ?_⟩
  · show reserveNext witnessParams s ⟨y, 39 / 50, T⟩ = 49
    unfold reserveNext
    rw [hun]
    unfold storageCapacity
    grind
  · show missedFinal witnessParams s ⟨y, 39 / 50, T⟩ = 0
    unfold missedFinal
    rw [hex]
    simp [hma]
  · show elitePresentNext witnessParams s ⟨y, 39 / 50, T⟩ = true
    unfold elitePresentNext
    rw [hpa, hex]
    rfl
  · show exitYearNext witnessParams s ⟨y, 39 / 50, T⟩ = none
    unfold exitYearNext
    rw [hex]
    simp [hx]

/-- Witness year 2 (reserve 49, no shortfall). -/
theorem wY2 (s : State) (y : Int) (T : Rat) (hT : 0 < T) (hP : s.elitePresent = true)
    (hx : s.exitYear = none) (hr : s.reserve = 49) (hm : s.missed = 0) :
    (step witnessParams s ⟨y, 39 / 50, T⟩).reserve = 301 / 10 ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).missed = 0 ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).elitePresent = true ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).exitYear = none := by
  obtain ⟨hpa, hcd, hav⟩ := W_facts s y T hT hP
  rw [hr] at hav
  have hu : unpaid witnessParams s ⟨y, 39 / 50, T⟩ = 0 := by
    rw [W_unpaid_eq s _ hcd, hav]
    unfold ritualBill
    grind
  have hun : unspent witnessParams s ⟨y, 39 / 50, T⟩ = 301 / 10 := by
    rw [W_unspent_eq s _ hcd, hav]
    unfold ritualBill
    grind
  have hlt : ¬ tolerance < unpaid witnessParams s ⟨y, 39 / 50, T⟩ := by
    rw [hu]
    unfold tolerance
    grind
  have hma : missedAfter witnessParams s ⟨y, 39 / 50, T⟩ = 0 := by
    unfold missedAfter
    rw [if_neg hlt]
  have hex : exited witnessParams s ⟨y, 39 / 50, T⟩ = false := by
    unfold exited
    rw [hma, hpa]
    simp [missedYearsToExit]
  refine ⟨?_, ?_, ?_, ?_⟩
  · show reserveNext witnessParams s ⟨y, 39 / 50, T⟩ = 301 / 10
    unfold reserveNext
    rw [hun]
    unfold storageCapacity
    grind
  · show missedFinal witnessParams s ⟨y, 39 / 50, T⟩ = 0
    unfold missedFinal
    rw [hex]
    simp [hma]
  · show elitePresentNext witnessParams s ⟨y, 39 / 50, T⟩ = true
    unfold elitePresentNext
    rw [hpa, hex]
    rfl
  · show exitYearNext witnessParams s ⟨y, 39 / 50, T⟩ = none
    unfold exitYearNext
    rw [hex]
    simp [hx]

/-- Witness year 3 (reserve 30.1, no shortfall). -/
theorem wY3 (s : State) (y : Int) (T : Rat) (hT : 0 < T) (hP : s.elitePresent = true)
    (hx : s.exitYear = none) (hr : s.reserve = 301 / 10) (hm : s.missed = 0) :
    (step witnessParams s ⟨y, 39 / 50, T⟩).reserve = 1309 / 100 ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).missed = 0 ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).elitePresent = true ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).exitYear = none := by
  obtain ⟨hpa, hcd, hav⟩ := W_facts s y T hT hP
  rw [hr] at hav
  have hu : unpaid witnessParams s ⟨y, 39 / 50, T⟩ = 0 := by
    rw [W_unpaid_eq s _ hcd, hav]
    unfold ritualBill
    grind
  have hun : unspent witnessParams s ⟨y, 39 / 50, T⟩ = 1309 / 100 := by
    rw [W_unspent_eq s _ hcd, hav]
    unfold ritualBill
    grind
  have hlt : ¬ tolerance < unpaid witnessParams s ⟨y, 39 / 50, T⟩ := by
    rw [hu]
    unfold tolerance
    grind
  have hma : missedAfter witnessParams s ⟨y, 39 / 50, T⟩ = 0 := by
    unfold missedAfter
    rw [if_neg hlt]
  have hex : exited witnessParams s ⟨y, 39 / 50, T⟩ = false := by
    unfold exited
    rw [hma, hpa]
    simp [missedYearsToExit]
  refine ⟨?_, ?_, ?_, ?_⟩
  · show reserveNext witnessParams s ⟨y, 39 / 50, T⟩ = 1309 / 100
    unfold reserveNext
    rw [hun]
    unfold storageCapacity
    grind
  · show missedFinal witnessParams s ⟨y, 39 / 50, T⟩ = 0
    unfold missedFinal
    rw [hex]
    simp [hma]
  · show elitePresentNext witnessParams s ⟨y, 39 / 50, T⟩ = true
    unfold elitePresentNext
    rw [hpa, hex]
    rfl
  · show exitYearNext witnessParams s ⟨y, 39 / 50, T⟩ = none
    unfold exitYearNext
    rw [hex]
    simp [hx]

/-- Witness year 4 (reserve 13.09): the court bill is short by 2.219, the first miss,
and the reserve is emptied. -/
theorem wY4 (s : State) (y : Int) (T : Rat) (hT : 0 < T) (hP : s.elitePresent = true)
    (hx : s.exitYear = none) (hr : s.reserve = 1309 / 100) (hm : s.missed = 0) :
    (step witnessParams s ⟨y, 39 / 50, T⟩).reserve = 0 ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).missed = 1 ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).elitePresent = true ∧
      (step witnessParams s ⟨y, 39 / 50, T⟩).exitYear = none := by
  obtain ⟨hpa, hcd, hav⟩ := W_facts s y T hT hP
  rw [hr] at hav
  have hu : unpaid witnessParams s ⟨y, 39 / 50, T⟩ = 2219 / 1000 := by
    rw [W_unpaid_eq s _ hcd, hav]
    unfold ritualBill
    grind
  have hun : unspent witnessParams s ⟨y, 39 / 50, T⟩ = 0 := by
    rw [W_unspent_eq s _ hcd, hav]
    unfold ritualBill
    grind
  have hlt : tolerance < unpaid witnessParams s ⟨y, 39 / 50, T⟩ := by
    rw [hu]
    unfold tolerance
    grind
  have hma : missedAfter witnessParams s ⟨y, 39 / 50, T⟩ = 1 := by
    unfold missedAfter
    rw [if_pos hlt]
    simp [hm]
  have hex : exited witnessParams s ⟨y, 39 / 50, T⟩ = false := by
    unfold exited
    rw [hma, hpa]
    simp [missedYearsToExit]
  refine ⟨?_, ?_, ?_, ?_⟩
  · show reserveNext witnessParams s ⟨y, 39 / 50, T⟩ = 0
    unfold reserveNext
    rw [hun]
    unfold storageCapacity
    grind
  · show missedFinal witnessParams s ⟨y, 39 / 50, T⟩ = 1
    unfold missedFinal
    rw [hex]
    simp [hma]
  · show elitePresentNext witnessParams s ⟨y, 39 / 50, T⟩ = true
    unfold elitePresentNext
    rw [hpa, hex]
    rfl
  · show exitYearNext witnessParams s ⟨y, 39 / 50, T⟩ = none
    unfold exitYearNext
    rw [hex]
    simp [hx]

/-- Witness year 5 (empty reserve, second consecutive shortfall): the elite exits. -/
theorem wY5 (s : State) (y : Int) (T : Rat) (hT : 0 < T) (hP : s.elitePresent = true)
    (hx : s.exitYear = none) (hr : s.reserve = 0) (hm : s.missed = 1) :
    (step witnessParams s ⟨y, 39 / 50, T⟩).exitYear = some y := by
  obtain ⟨hpa, hcd, hav⟩ := W_facts s y T hT hP
  rw [hr] at hav
  have hu : unpaid witnessParams s ⟨y, 39 / 50, T⟩ = 14 := by
    rw [W_unpaid_eq s _ hcd, hav]
    unfold ritualBill
    grind
  have hlt : tolerance < unpaid witnessParams s ⟨y, 39 / 50, T⟩ := by
    rw [hu]
    unfold tolerance
    grind
  have hma : missedAfter witnessParams s ⟨y, 39 / 50, T⟩ = 2 := by
    unfold missedAfter
    rw [if_pos hlt]
    simp [hm]
  have hex : exited witnessParams s ⟨y, 39 / 50, T⟩ = true := by
    unfold exited
    rw [hma, hpa]
    simp [missedYearsToExit]
  show exitYearNext witnessParams s ⟨y, 39 / 50, T⟩ = some y
  unfold exitYearNext
  rw [hex]
  simp [hx, setOnce]

/-- Exit witness inside the engine's harvest range: five years at harvest `39/50` from the
initial state, with `witnessParams`, exit in year 5. Needs tribute `> 0`. -/
theorem disruption_zero_exit_in_range (T : Rat) (hT : 0 < T) :
    (run witnessParams initial
      [⟨1, 39 / 50, T⟩, ⟨2, 39 / 50, T⟩, ⟨3, 39 / 50, T⟩, ⟨4, 39 / 50, T⟩, ⟨5, 39 / 50, T⟩]).exitYear
      = some 5 := by
  obtain ⟨a1, b1, c1, d1⟩ := wY1 initial 1 T hT rfl rfl rfl rfl
  obtain ⟨a2, b2, c2, d2⟩ := wY2 _ 2 T hT c1 d1 a1 b1
  obtain ⟨a3, b3, c3, d3⟩ := wY3 _ 3 T hT c2 d2 a2 b2
  obtain ⟨a4, b4, c4, d4⟩ := wY4 _ 4 T hT c3 d3 a3 b3
  exact wY5 _ 5 T hT c4 d4 a4 b4

end Angkor.Obligations
