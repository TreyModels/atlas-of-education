import Angkor.Basic

/-!
# Signalling model (experiment 03)

Source: `src/models/signalling.js`, byte-identical to `public/engines/signalling.js` (88 lines).
Formalized:
* constants: lines 4-12 (defaults and assumptions), line 34 (`1.35` cap);
* one year of the loop body: lines 22-66, as stage definitions in source order (`stepYear`);
* the observer choice: line 53 (`Observer`);
* iteration over a list of draws `(u1, u2)` (`runFrom`), replacing the loop over `year`.

Not formalized: the LCG (lines 16-17) and `compare` (lines 70-85). The draws are explicit inputs
`u1, u2` with `0 ≤ u < 1`, matching the LCG output range `[0, 1)`.

Arithmetic is exact `Rat`, not IEEE doubles: theorems are about the ideal arithmetic.

Elephant counts (`elephants`, `maintained`, `replacements`) are `Int`, because they are counts and
`Rat.floor` returns `Int`. The source has four `Math.floor` calls (lines 37 and 43, two each);
all four are `Rat.floor` here.

Divisions: every divisor is a nonzero constant (`5/2`, `2`, `5`, `40`, `620`, `8`), so no division
by zero occurs in the model.

Parameters (`loss`, `stoneWeight`, `displayShare`, `signalScale`) are arbitrary rationals; each
theorem states the range it needs (`ParamsOK`, `StateOK`, `DrawOK`).
-/

namespace Angkor.Signalling

/-- Which observer's capacity decides the pledge (source line 53). -/
inductive Observer where
  | display
  | truth
  deriving DecidableEq

/-- Per-run parameters (source line 4). -/
structure Params where
  loss : Rat
  stoneWeight : Rat
  displayShare : Rat
  signalScale : Rat

/-- Source defaults (line 4): `loss .55`, `stoneWeight .65`, `displayShare .16`, `signalScale 1`. -/
def defaultParams : Params := ⟨55/100, 65/100, 16/100, 1⟩

/-- Source line 9: `initialElephants: 40`. -/
def initialElephants : Int := 40

/-- Carried state between years (source lines 18-19). -/
structure State where
  reserve : Rat
  stone : Rat
  elephants : Int
  pledged : Bool

/-- Initial state (source lines 18-19): reserve `startingGrain 45`, stone `initialStone 1`,
elephants `initialElephants 40`, pledged `initialPledge true`. -/
def initialState : State := ⟨45, 1, 40, true⟩

/-- Source line 25: `Math.max(0, 1 - (year - 1) / a.recoveryYears)`, recoveryYears 8. -/
def recoveryShare (year : Nat) : Rat := max 0 (1 - ((year : Rat) - 1) / 8)

/-- Source line 25: `1 - p.loss * Math.max(0, 1 - (year - 1) / a.recoveryYears)`. -/
def lossFactor (loss : Rat) (year : Nat) : Rat := 1 - loss * recoveryShare year

/-- Source line 23: `.78 + .44 * draw()`. -/
def harvestOf (u1 : Rat) : Rat := 78/100 + 44/100 * u1

/-- Source line 24: `annualThreatBase + annualThreatSpread * draw()`. -/
def demandOf (u2 : Rat) : Rat := 205 + 110 * u2

/-- Source line 26: `pledged ? a.tribute : 0`, tribute 105. -/
def tributeOf (pledged : Bool) : Rat := if pledged then 105 else 0

/-- Parameter ranges used by the bound theorems. -/
def ParamsOK (p : Params) : Prop :=
  0 ≤ p.loss ∧ p.loss ≤ 1 ∧ 0 ≤ p.displayShare ∧ p.displayShare ≤ 1

/-- State invariant: the bounds claimed for the carried state. -/
def StateOK (s : State) : Prop :=
  0 ≤ s.reserve ∧ s.reserve ≤ 180 ∧ 0 ≤ s.stone ∧ s.stone ≤ 135/100 ∧
  0 ≤ s.elephants ∧ s.elephants ≤ 40

/-- Draw range: `draw()` returns values in `[0, 1)`. -/
def DrawOK (d : Rat × Rat) : Prop := 0 ≤ d.1 ∧ d.1 < 1 ∧ 0 ≤ d.2 ∧ d.2 < 1

/-! ## Stage definitions (source lines 23-65, in source order)

Each stage takes `(p, s, year, d)` and uses the earlier stages, so every stage is an atom to
`grind` until it is unfolded. Reassignments of `available` and `labour` are separate stages
(`a0`..`a3`, `lab1`..`lab3`). -/

/-- Line 25: local grain for the year. -/
def lgOf (p : Params) (year : Nat) (d : Rat × Rat) : Rat :=
  320 * harvestOf d.1 * lossFactor p.loss year

/-- Lines 27-29: `available` after spoilage and inflows. -/
def a0Of (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  s.reserve - s.reserve * (12/100) + lgOf p year d + tributeOf s.pledged

/-- Line 31: `build = min(available * displayShare, openingLabour)`, openingLabour 420. -/
def buildOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  min (a0Of p s year d * p.displayShare) 420

/-- Line 32: `available -= build`. -/
def a1Of (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  a0Of p s year d - buildOf p s year d

/-- Line 33: `labour = openingLabour - build`. -/
def lab1Of (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  420 - buildOf p s year d

/-- Line 34: `stone = min(1.35, stone * (1 - stoneLoss) + build / buildingScale)`. -/
def stoneOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  min (135/100) (s.stone * (1 - 15/1000) + buildOf p s year d / 620)

/-- Line 36: `elephantBudget = available * elephantBudgetShare`. -/
def ebOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  a1Of p s year d * (28/100)

/-- Line 37, first integer floor:
`maintained = min(elephants, floor(budget / upkeep), floor(labour / elephantLabour))`. -/
def mOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Int :=
  min (min s.elephants (Rat.floor (ebOf p s year d / (5/2)))) (Rat.floor (lab1Of p s year d / 2))

/-- Line 38: `upkeep = maintained * elephantUpkeep`. -/
def upkOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  (mOf p s year d : Rat) * (5/2)

/-- Line 39: `upkeepLabour = maintained * elephantLabour`. -/
def ulOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  (mOf p s year d : Rat) * 2

/-- Line 40: `available -= upkeep`. -/
def a2Of (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  a1Of p s year d - upkOf p s year d

/-- Line 41: `labour -= upkeepLabour`. -/
def lab2Of (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  lab1Of p s year d - ulOf p s year d

/-- Line 42-43, second integer floor:
`replacements = min(annualReplacements, initialElephants - maintained,
floor((elephantBudget - upkeep) / replacementCost), floor(labour / elephantLabour))`.
Here `annualReplacements = 5` and `replacementCost = 5`. -/
def rOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Int :=
  min (min (min 5 (initialElephants - mOf p s year d))
      (Rat.floor ((ebOf p s year d - upkOf p s year d) / 5)))
    (Rat.floor (lab2Of p s year d / 2))

/-- Line 44: `replacementSpend = replacements * replacementCost`. -/
def rsOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  (rOf p s year d : Rat) * 5

/-- Line 45: `replacementLabour = replacements * elephantLabour`. -/
def rlOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  (rOf p s year d : Rat) * 2

/-- Line 46: `available -= replacementSpend`. -/
def a3Of (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  a2Of p s year d - rsOf p s year d

/-- Line 47: `labour -= replacementLabour`. -/
def lab3Of (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  lab2Of p s year d - rlOf p s year d

/-- Line 50: `trueCapacity = min(available, labour)`. -/
def tcOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  min (a3Of p s year d) (lab3Of p s year d)

/-- Line 51 bracket: `stoneWeight * stone + (1 - stoneWeight) * maintained / initialElephants`. -/
def bracketOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  p.stoneWeight * stoneOf p s year d +
    (1 - p.stoneWeight) * ((mOf p s year d : Rat) / (initialElephants : Rat))

/-- Lines 51-52: `displayedCapacity = capacityScale * signalScale * bracket`, capacityScale 300. -/
def dispOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  300 * p.signalScale * bracketOf p s year d

/-- Line 53: `perceivedCapacity`, chosen by the observer. -/
def percOf (obs : Observer) (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  if obs = Observer.truth then tcOf p s year d else dispOf p s year d

/-- Line 56: `defenceSpend = min(trueCapacity, demand)`. -/
def spendOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  min (tcOf p s year d) (demandOf d.2)

/-- Line 57: `unspent = available - defenceSpend`. -/
def unOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  a3Of p s year d - spendOf p s year d

/-- Line 58: `reserve = min(storageCapacity, unspent)`, storageCapacity 180. -/
def resOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  min 180 (unOf p s year d)

/-- Line 59: `storageOverflow = unspent - reserve`. -/
def ovOf (p : Params) (s : State) (year : Nat) (d : Rat × Rat) : Rat :=
  unOf p s year d - resOf p s year d

/-- Everything the year produces (the `rows.push` of source lines 60-65). -/
structure Row where
  demand : Rat
  harvestShock : Rat
  openingReserve : Rat
  localGrain : Rat
  tributeReceived : Rat
  spoiled : Rat
  build : Rat
  stone : Rat
  maintained : Int
  upkeep : Rat
  upkeepLabour : Rat
  replacements : Int
  replacementSpend : Rat
  replacementLabour : Rat
  elephants : Int
  openingLabour : Rat
  labourLeft : Rat
  trueCapacity : Rat
  displayedCapacity : Rat
  perceivedCapacity : Rat
  pledged : Bool
  defended : Bool
  defenceSpend : Rat
  storageOverflow : Rat
  reserve : Rat
  grainBalanceError : Rat

/-- One year, source lines 23-65. `pledged` is `perceivedCapacity >= demand` (line 54) and
`defended` is `trueCapacity >= demand` (line 55). `grainBalanceError` is line 64-65. -/
def stepYear (p : Params) (obs : Observer) (year : Nat) (s : State) (d : Rat × Rat) : Row :=
  { demand := demandOf d.2
    harvestShock := harvestOf d.1
    openingReserve := s.reserve
    localGrain := lgOf p year d
    tributeReceived := tributeOf s.pledged
    spoiled := s.reserve * (12/100)
    build := buildOf p s year d
    stone := stoneOf p s year d
    maintained := mOf p s year d
    upkeep := upkOf p s year d
    upkeepLabour := ulOf p s year d
    replacements := rOf p s year d
    replacementSpend := rsOf p s year d
    replacementLabour := rlOf p s year d
    elephants := mOf p s year d + rOf p s year d
    openingLabour := 420
    labourLeft := lab3Of p s year d
    trueCapacity := tcOf p s year d
    displayedCapacity := dispOf p s year d
    perceivedCapacity := percOf obs p s year d
    pledged := decide (demandOf d.2 ≤ percOf obs p s year d)
    defended := decide (demandOf d.2 ≤ tcOf p s year d)
    defenceSpend := spendOf p s year d
    storageOverflow := ovOf p s year d
    reserve := resOf p s year d
    grainBalanceError :=
      s.reserve + lgOf p year d + tributeOf s.pledged - s.reserve * (12/100) - buildOf p s year d
        - upkOf p s year d - rsOf p s year d - spendOf p s year d - ovOf p s year d
        - resOf p s year d }

/-- Next carried state after one year. -/
def nextState (p : Params) (obs : Observer) (year : Nat) (s : State) (d : Rat × Rat) : State :=
  ⟨resOf p s year d, stoneOf p s year d, mOf p s year d + rOf p s year d,
    decide (demandOf d.2 ≤ percOf obs p s year d)⟩

/-- Iterate the year step over a list of draws, the first draw being year `y`. -/
def runFrom (p : Params) (obs : Observer) : Nat → State → List (Rat × Rat) → State
  | _, s, [] => s
  | y, s, d :: ds => runFrom p obs (y + 1) (nextState p obs y s d) ds

/-! ## Floor facts -/

/-- A nonnegative argument has a nonnegative floor. -/
theorem floor_nonneg' (x : Rat) (h : 0 ≤ x) : 0 ≤ Rat.floor x := by
  refine Decidable.byContradiction fun hc => ?_
  have hc' : Rat.floor x ≤ -1 := by omega
  have h5 : ((Rat.floor x : Int) : Rat) ≤ ((-1 : Int) : Rat) := by exact_mod_cast hc'
  have := Rat.lt_floor_add_one x
  grind

/-! ## Target 1: grain balance -/

/-- Target 1: the grain ledger balances exactly in every year, for every state, draw,
parameter set and observer. No hypotheses are needed. -/
theorem grainBalanceError_eq_zero (p : Params) (obs : Observer) (year : Nat) (s : State)
    (d : Rat × Rat) : (stepYear p obs year s d).grainBalanceError = 0 := by
  unfold stepYear ovOf resOf unOf spendOf a3Of a2Of a1Of a0Of
  dsimp only
  grind

/-! ## Target 2 and 3: bounds and replacement sign checks -/

theorem lossFactor_bounds (loss : Rat) (year : Nat) (hy : 1 ≤ year) (h0 : 0 ≤ loss) (h1 : loss ≤ 1) :
    0 ≤ lossFactor loss year ∧ lossFactor loss year ≤ 1 := by
  have hy' : (1 : Rat) ≤ (year : Rat) := by exact_mod_cast hy
  have hm0 : 0 ≤ recoveryShare year := by unfold recoveryShare; grind
  have hm1 : recoveryShare year ≤ 1 := by unfold recoveryShare; grind
  have hp := Rat.mul_nonneg h0 hm0
  have hq := Rat.mul_nonneg (show (0 : Rat) ≤ 1 - loss by grind) hm0
  unfold lossFactor
  constructor <;> grind

theorem lg_nonneg (p : Params) (year : Nat) (d : Rat × Rat) (hy : 1 ≤ year) (hp : ParamsOK p)
    (hd : DrawOK d) : 0 ≤ lgOf p year d := by
  obtain ⟨hl0, hl1, -, -⟩ := id hp
  obtain ⟨hu0, -, -, -⟩ := id hd
  have hs : 0 ≤ harvestOf d.1 := by unfold harvestOf; grind
  have hL := (lossFactor_bounds p.loss year hy hl0 hl1).1
  unfold lgOf
  exact Rat.mul_nonneg (by grind) hL

theorem a0_nonneg (p : Params) (s : State) (year : Nat) (d : Rat × Rat) (hy : 1 ≤ year)
    (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) : 0 ≤ a0Of p s year d := by
  obtain ⟨h1, -, -, -, -, -⟩ := id hs
  have hlg := lg_nonneg p year d hy hp hd
  have htr : 0 ≤ tributeOf s.pledged := by unfold tributeOf; split <;> grind
  unfold a0Of
  grind

theorem build_bounds (p : Params) (s : State) (year : Nat) (d : Rat × Rat) (hy : 1 ≤ year)
    (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) :
    0 ≤ buildOf p s year d ∧ buildOf p s year d ≤ a0Of p s year d := by
  have ha0 := a0_nonneg p s year d hy hp hd hs
  obtain ⟨-, -, hpd0, hpd1⟩ := id hp
  have h1 : 0 ≤ a0Of p s year d * p.displayShare := Rat.mul_nonneg ha0 hpd0
  have h2 : 0 ≤ (1 - p.displayShare) * a0Of p s year d := Rat.mul_nonneg (by grind) ha0
  unfold buildOf
  constructor <;> grind

theorem a1_nonneg (p : Params) (s : State) (year : Nat) (d : Rat × Rat) (hy : 1 ≤ year)
    (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) : 0 ≤ a1Of p s year d := by
  have hb := build_bounds p s year d hy hp hd hs
  unfold a1Of
  grind

theorem lab1_nonneg (p : Params) (s : State) (year : Nat) (d : Rat × Rat) :
    0 ≤ lab1Of p s year d := by
  unfold lab1Of buildOf
  grind

theorem eb_nonneg (p : Params) (s : State) (year : Nat) (d : Rat × Rat) (hy : 1 ≤ year)
    (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) : 0 ≤ ebOf p s year d := by
  have ha1 := a1_nonneg p s year d hy hp hd hs
  unfold ebOf
  grind

theorem stone_bounds (p : Params) (s : State) (year : Nat) (d : Rat × Rat) (hy : 1 ≤ year)
    (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) :
    0 ≤ stoneOf p s year d ∧ stoneOf p s year d ≤ 135/100 := by
  have hb := build_bounds p s year d hy hp hd hs
  obtain ⟨-, -, hst0, -, -, -⟩ := id hs
  unfold stoneOf
  constructor <;> grind

/-- Targets 2 and 3 for the first integer floor: `maintained` is between `0` and `elephants`,
its upkeep fits inside the budget, and its labour fits inside the labour left. -/
theorem maintained_facts (p : Params) (s : State) (year : Nat) (d : Rat × Rat) (hy : 1 ≤ year)
    (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) :
    0 ≤ mOf p s year d ∧ mOf p s year d ≤ s.elephants ∧
      upkOf p s year d ≤ ebOf p s year d ∧ ulOf p s year d ≤ lab1Of p s year d := by
  have hEb := eb_nonneg p s year d hy hp hd hs
  have hL := lab1_nonneg p s year d
  obtain ⟨-, -, -, -, hel0, -⟩ := id hs
  have f1 := floor_nonneg' (ebOf p s year d / (5/2)) (by grind)
  have f2 := floor_nonneg' (lab1Of p s year d / 2) (by grind)
  have g1 := Rat.floor_le (ebOf p s year d / (5/2))
  have g2 := Rat.floor_le (lab1Of p s year d / 2)
  have hA : mOf p s year d ≤ Rat.floor (ebOf p s year d / (5/2)) := by unfold mOf; grind
  have hB : mOf p s year d ≤ Rat.floor (lab1Of p s year d / 2) := by unfold mOf; grind
  have hC : 0 ≤ mOf p s year d := by unfold mOf; grind
  have hD : mOf p s year d ≤ s.elephants := by unfold mOf; grind
  have hA' : (mOf p s year d : Rat) ≤ (Rat.floor (ebOf p s year d / (5/2)) : Rat) := by
    exact_mod_cast hA
  have hB' : (mOf p s year d : Rat) ≤ (Rat.floor (lab1Of p s year d / 2) : Rat) := by
    exact_mod_cast hB
  refine ⟨hC, hD, ?_, ?_⟩
  · unfold upkOf; grind
  · unfold ulOf; grind

/-- Targets 2 and 3 for the second integer floor, the replacements. The four terms of the
`min` are nonnegative: `5`, `initialElephants - maintained`, `(budget - upkeep) / 5` and
`labour / 2`. -/
theorem replacement_facts (p : Params) (s : State) (year : Nat) (d : Rat × Rat) (hy : 1 ≤ year)
    (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) :
    0 ≤ rOf p s year d ∧ mOf p s year d + rOf p s year d ≤ 40 ∧
      0 ≤ ebOf p s year d - upkOf p s year d ∧ 2 * (rOf p s year d : Rat) ≤ lab2Of p s year d ∧
      0 ≤ lab2Of p s year d := by
  obtain ⟨hC1, hC2, hC3, hC4⟩ := maintained_facts p s year d hy hp hd hs
  obtain ⟨-, -, -, -, -, hel1⟩ := id hs
  have hEb := eb_nonneg p s year d hy hp hd hs
  have hL := lab1_nonneg p s year d
  have hLab2 : 0 ≤ lab2Of p s year d := by unfold lab2Of; grind
  have hBud : 0 ≤ ebOf p s year d - upkOf p s year d := by grind
  have f3 := floor_nonneg' ((ebOf p s year d - upkOf p s year d) / 5) (by grind)
  have f4 := floor_nonneg' (lab2Of p s year d / 2) (by grind)
  have g3 := Rat.floor_le (lab2Of p s year d / 2)
  have hA : rOf p s year d ≤ Rat.floor (lab2Of p s year d / 2) := by unfold rOf; grind
  have hA' : (rOf p s year d : Rat) ≤ (Rat.floor (lab2Of p s year d / 2) : Rat) := by
    exact_mod_cast hA
  have hR0 : 0 ≤ rOf p s year d := by unfold rOf initialElephants; grind
  have hR40 : mOf p s year d + rOf p s year d ≤ 40 := by unfold rOf initialElephants; grind
  refine ⟨hR0, hR40, hBud, ?_, hLab2⟩
  grind

/-! ## Step-level statements -/

/-- Reserve stays in `[0, storageCapacity]` for every state, draw and parameter set. -/
theorem reserve_bounds (p : Params) (obs : Observer) (year : Nat) (s : State) (d : Rat × Rat) :
    0 ≤ (stepYear p obs year s d).reserve ∧ (stepYear p obs year s d).reserve ≤ 180 := by
  show 0 ≤ resOf p s year d ∧ resOf p s year d ≤ 180
  unfold resOf unOf spendOf tcOf
  constructor <;> grind

/-- Stone stays in `[0, 1.35]` (source line 34). -/
theorem stone_step_bounds (p : Params) (obs : Observer) (year : Nat) (s : State) (d : Rat × Rat)
    (hy : 1 ≤ year) (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) :
    0 ≤ (stepYear p obs year s d).stone ∧ (stepYear p obs year s d).stone ≤ 135/100 :=
  stone_bounds p s year d hy hp hd hs

/-- Target 2 and 3: the maintained elephants lie in `[0, elephants]`. -/
theorem maintained_step_bounds (p : Params) (obs : Observer) (year : Nat) (s : State) (d : Rat × Rat)
    (hy : 1 ≤ year) (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) :
    0 ≤ (stepYear p obs year s d).maintained ∧ (stepYear p obs year s d).maintained ≤ s.elephants :=
  ⟨(maintained_facts p s year d hy hp hd hs).1, (maintained_facts p s year d hy hp hd hs).2.1⟩

/-- Target 2: the elephant count stays in `[0, initialElephants]`. -/
theorem elephants_step_bounds (p : Params) (obs : Observer) (year : Nat) (s : State) (d : Rat × Rat)
    (hy : 1 ≤ year) (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) :
    0 ≤ (stepYear p obs year s d).elephants ∧ (stepYear p obs year s d).elephants ≤ 40 := by
  have hm := maintained_facts p s year d hy hp hd hs
  have hr := replacement_facts p s year d hy hp hd hs
  show 0 ≤ mOf p s year d + rOf p s year d ∧ mOf p s year d + rOf p s year d ≤ 40
  exact ⟨by grind, hr.2.1⟩

/-- Target 2: labour is never negative (source lines 33, 41, 47). -/
theorem labour_step_nonneg (p : Params) (obs : Observer) (year : Nat) (s : State) (d : Rat × Rat)
    (hy : 1 ≤ year) (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) :
    0 ≤ (stepYear p obs year s d).labourLeft := by
  have hr := replacement_facts p s year d hy hp hd hs
  show 0 ≤ lab3Of p s year d
  unfold lab3Of rlOf
  grind

/-- Target 2: the opening labour is exactly covered by build, upkeep labour, replacement labour and
what is left. -/
theorem labour_ledger (p : Params) (obs : Observer) (year : Nat) (s : State) (d : Rat × Rat) :
    (stepYear p obs year s d).openingLabour =
      (stepYear p obs year s d).build + (stepYear p obs year s d).upkeepLabour +
        (stepYear p obs year s d).replacementLabour + (stepYear p obs year s d).labourLeft := by
  show (420 : Rat) = buildOf p s year d + ulOf p s year d + rlOf p s year d + lab3Of p s year d
  unfold lab3Of lab2Of lab1Of rlOf ulOf
  grind

/-- Target 3, first sign check: `initialElephants - maintained >= 0`. -/
theorem sign_initial_minus_maintained (p : Params) (s : State) (year : Nat) (d : Rat × Rat)
    (hy : 1 ≤ year) (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) :
    0 ≤ initialElephants - mOf p s year d := by
  have hm := maintained_facts p s year d hy hp hd hs
  obtain ⟨-, -, -, -, -, hel1⟩ := id hs
  unfold initialElephants
  grind

/-- Target 3, second sign check: `elephantBudget - upkeep >= 0`. Proved from the floor bound alone,
with no hypotheses on the state. -/
theorem sign_budget_minus_upkeep (p : Params) (s : State) (year : Nat) (d : Rat × Rat) :
    upkOf p s year d ≤ ebOf p s year d := by
  have hA : mOf p s year d ≤ Rat.floor (ebOf p s year d / (5/2)) := by unfold mOf; grind
  have hA' : (mOf p s year d : Rat) ≤ (Rat.floor (ebOf p s year d / (5/2)) : Rat) := by
    exact_mod_cast hA
  have g1 := Rat.floor_le (ebOf p s year d / (5/2))
  unfold upkOf
  grind

/-- Target 3, the replacement terms are all nonnegative. -/
theorem sign_replacement_terms (p : Params) (s : State) (year : Nat) (d : Rat × Rat)
    (hy : 1 ≤ year) (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) :
    0 ≤ (5 : Int) ∧ 0 ≤ initialElephants - mOf p s year d ∧
      0 ≤ ebOf p s year d - upkOf p s year d ∧ 0 ≤ lab2Of p s year d :=
  ⟨by decide, sign_initial_minus_maintained p s year d hy hp hd hs,
    by have := sign_budget_minus_upkeep p s year d; grind,
    (replacement_facts p s year d hy hp hd hs).2.2.2.2⟩

/-! ## Target 4: observers -/

/-- Under the truth observer the pledge equals the defence, every year. -/
theorem truth_pledged_eq_defended (p : Params) (year : Nat) (s : State) (d : Rat × Rat) :
    (stepYear p Observer.truth year s d).pledged = (stepYear p Observer.truth year s d).defended := by
  show decide (demandOf d.2 ≤ percOf Observer.truth p s year d) =
    decide (demandOf d.2 ≤ tcOf p s year d)
  unfold percOf
  simp

/-- Under the truth observer there is no false reassurance. -/
theorem truth_no_false_reassurance (p : Params) (year : Nat) (s : State) (d : Rat × Rat) :
    ¬ ((stepYear p Observer.truth year s d).pledged = true ∧
      (stepYear p Observer.truth year s d).defended = false) := by
  intro h
  have e := truth_pledged_eq_defended p year s d
  rw [e] at h
  rw [h.1] at h
  exact Bool.noConfusion h.2

/-- Under the truth observer there is no lost credibility. -/
theorem truth_no_lost_credibility (p : Params) (year : Nat) (s : State) (d : Rat × Rat) :
    ¬ ((stepYear p Observer.truth year s d).pledged = false ∧
      (stepYear p Observer.truth year s d).defended = true) := by
  intro h
  have e := truth_pledged_eq_defended p year s d
  rw [e] at h
  rw [h.1] at h
  exact Bool.noConfusion h.2

/-! ## Target 5: displayed capacity and defence -/

/-- Displayed capacity is monotone in `signalScale` when `0 ≤ stoneWeight ≤ 1` (the bracket is then
nonnegative, since the stone and maintained elephants are nonnegative). -/
theorem displayed_mono_signalScale (p : Params) (s : State) (year : Nat) (d : Rat × Rat)
    (hy : 1 ≤ year) (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s)
    (hw0 : 0 ≤ p.stoneWeight) (hw1 : p.stoneWeight ≤ 1) (x y : Rat) (hxy : x ≤ y) :
    300 * x * bracketOf p s year d ≤ 300 * y * bracketOf p s year d := by
  have hst := stone_bounds p s year d hy hp hd hs
  have hm := maintained_facts p s year d hy hp hd hs
  have hmR : (0 : Rat) ≤ (mOf p s year d : Rat) := by exact_mod_cast hm.1
  have hB : 0 ≤ bracketOf p s year d := by
    unfold bracketOf
    have h1 := Rat.mul_nonneg hw0 hst.1
    have h2 := Rat.mul_nonneg (show (0 : Rat) ≤ 1 - p.stoneWeight by grind)
      (show (0 : Rat) ≤ (mOf p s year d : Rat) / (initialElephants : Rat) by
        unfold initialElephants; grind)
    grind
  have h3 := Rat.mul_nonneg (show (0 : Rat) ≤ y - x by grind)
    (show (0 : Rat) ≤ 300 * bracketOf p s year d by grind)
  grind

/-- With `stoneWeight = 1` the elephant term vanishes: the displayed capacity is
`capacityScale * signalScale * stone`. -/
theorem displayed_stoneWeight_one (p : Params) (s : State) (year : Nat) (d : Rat × Rat) :
    dispOf { p with stoneWeight := 1 } s year d = 300 * p.signalScale * stoneOf p s year d := by
  show 300 * p.signalScale * ((1 : Rat) * stoneOf p s year d +
    (1 - 1) * ((mOf p s year d : Rat) / (initialElephants : Rat))) = 300 * p.signalScale * stoneOf p s year d
  grind

/-- With `stoneWeight = 1` the displayed capacity does not depend on the elephant count. -/
theorem displayed_stoneWeight_one_no_elephants (p : Params) (s : State) (year : Nat) (d : Rat × Rat)
    (e e' : Int) :
    dispOf { p with stoneWeight := 1 } { s with elephants := e } year d =
      dispOf { p with stoneWeight := 1 } { s with elephants := e' } year d := by
  show 300 * p.signalScale * ((1 : Rat) * stoneOf p s year d +
    (1 - 1) * ((mOf p { s with elephants := e } year d : Rat) / (initialElephants : Rat))) =
      300 * p.signalScale * ((1 : Rat) * stoneOf p s year d +
    (1 - 1) * ((mOf p { s with elephants := e' } year d : Rat) / (initialElephants : Rat)))
  grind

/-- `defended` depends on the parameters only through `trueCapacity` and `demand`: parameters that
agree on `loss` and `displayShare` give the same trueCapacity and the same defended flag, whatever
`signalScale`, `stoneWeight` and the observer. -/
theorem defended_depends_only_via_tc (p1 p2 : Params) (o1 o2 : Observer) (year : Nat) (s : State)
    (d : Rat × Rat) (hl : p1.loss = p2.loss) (hdp : p1.displayShare = p2.displayShare) :
    (stepYear p1 o1 year s d).trueCapacity = (stepYear p2 o2 year s d).trueCapacity ∧
      (stepYear p1 o1 year s d).defended = (stepYear p2 o2 year s d).defended := by
  obtain ⟨l1, w1, b1, x1⟩ := p1
  obtain ⟨l2, w2, b2, x2⟩ := p2
  simp only at hl hdp
  subst hl
  subst hdp
  exact ⟨rfl, rfl⟩

/-! ## Iteration over draws -/

theorem nextState_ok (p : Params) (obs : Observer) (year : Nat) (s : State) (d : Rat × Rat)
    (hy : 1 ≤ year) (hp : ParamsOK p) (hd : DrawOK d) (hs : StateOK s) :
    StateOK (nextState p obs year s d) := by
  have h1 := reserve_bounds p obs year s d
  have h2 := stone_step_bounds p obs year s d hy hp hd hs
  have h3 := elephants_step_bounds p obs year s d hy hp hd hs
  unfold StateOK
  show 0 ≤ resOf p s year d ∧ resOf p s year d ≤ 180 ∧
    0 ≤ stoneOf p s year d ∧ stoneOf p s year d ≤ 135/100 ∧
    0 ≤ mOf p s year d + rOf p s year d ∧ mOf p s year d + rOf p s year d ≤ 40
  exact ⟨h1.1, h1.2, h2.1, h2.2, h3.1, h3.2⟩

/-- The state invariant holds after any number of years, for any list of draws in `[0,1)`. -/
theorem runFrom_stateOK (p : Params) (obs : Observer) (hp : ParamsOK p) :
    ∀ (ds : List (Rat × Rat)) (y : Nat) (s : State), 1 ≤ y → StateOK s →
      (∀ d ∈ ds, DrawOK d) → StateOK (runFrom p obs y s ds)
  | [], _, s, _, hs, _ => hs
  | d :: ds, y, s, hy, hs, hall =>
    runFrom_stateOK p obs hp ds (y + 1) (nextState p obs y s d) (by omega)
      (nextState_ok p obs y s d hy hp (hall d (List.mem_cons_self)) hs)
      (fun d' hd' => hall d' (List.mem_cons_of_mem _ hd'))

theorem initialState_ok : StateOK initialState := by
  unfold StateOK initialState
  grind


/-! ## Target 4: display witnesses (one step each) -/

/-- Witness, false reassurance under the display observer. Reachable: the state is the initial
state and year 1 is the first step. Draws `u1 = 0` (harvest .78) and `u2 = 0` (demand 205).
Displayed capacity is 41540601/155000 (about 268.0) against demand 205, so the pledge is made;
true capacity is 97383/625 (about 155.8), below demand, so the defence fails. -/
theorem witness_false_reassurance :
    (stepYear defaultParams Observer.display 1 initialState (0, 0)).pledged = true ∧
    (stepYear defaultParams Observer.display 1 initialState (0, 0)).defended = false := by
  with_unfolding_all decide

/-- Witness, lost credibility under the display observer. NOT reachable from the initial state in
one step: year 1 always starts from `initialState` (elephants 40), and this witness starts from
elephants 12, reserve 180 and stone 1.35. Draws `u1 = 3/4`, `u2 = 17/20`, demand 298.5. Displayed
capacity is 294.75 < 298.5, so no pledge; true capacity is about 300.52 >= 298.5, so the defence
holds. -/
theorem witness_lost_credibility :
    (stepYear defaultParams Observer.display 1 ⟨180, 135/100, 12, true⟩ (3/4, 17/20)).pledged = false ∧
    (stepYear defaultParams Observer.display 1 ⟨180, 135/100, 12, true⟩ (3/4, 17/20)).defended = true := by
  with_unfolding_all decide

/-- Multi-year run from the initial state, for any list of draws in `[0,1)` and both observers. -/
theorem run_from_initial_ok (p : Params) (obs : Observer) (hp : ParamsOK p) (ds : List (Rat × Rat))
    (hd : ∀ d ∈ ds, DrawOK d) : StateOK (runFrom p obs 1 initialState ds) :=
  runFrom_stateOK p obs hp ds 1 initialState (Nat.le_refl 1) initialState_ok hd


/-- Exact values behind `witness_false_reassurance`. -/
theorem witness_false_reassurance_values :
    (stepYear defaultParams Observer.display 1 initialState (0, 0)).displayedCapacity = 41540601/155000 ∧
    (stepYear defaultParams Observer.display 1 initialState (0, 0)).trueCapacity = 97383/625 ∧
    (stepYear defaultParams Observer.display 1 initialState (0, 0)).demand = 205 := by
  with_unfolding_all decide

/-- Exact values behind `witness_lost_credibility`. -/
theorem witness_lost_credibility_values :
    (stepYear defaultParams Observer.display 1 ⟨180, 135/100, 12, true⟩ (3/4, 17/20)).displayedCapacity = 1179/4 ∧
    (stepYear defaultParams Observer.display 1 ⟨180, 135/100, 12, true⟩ (3/4, 17/20)).demand = 597/2 ∧
    (stepYear defaultParams Observer.display 1 ⟨180, 135/100, 12, true⟩ (3/4, 17/20)).trueCapacity
      ≥ 597/2 := by
  with_unfolding_all decide

end Angkor.Signalling
