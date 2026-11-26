import Angkor.Basic

/-!
# Relocation: two-region year step

Formalizes `public/engines/relocation.js` (81 lines): `economy` (lines 9-38), the
year-loop body with the four mobility modes (lines 42-68), and iteration over a list
of weather inputs (`runYears`). The `run` summaries (lines 69-78: exit year, retained
shares, peaks, output rows) are not formalized.

Modelling choices (CONVENTIONS.md):
* Exact rationals (`Rat`) stand in for floating point. Theorems are about ideal
  arithmetic, not IEEE rounding.
* Randomness is an input. Each year's `noise` (line 43, from `rng`) and `dry` flag
  (line 43, drought schedule) are arguments. Only `0 ≤ noise` is assumed (JS draws
  give noise in [0.98, 1.02)). The drought schedule is not formalized.
* Division: Lean gives x / 0 = 0, JavaScript gives Infinity or NaN. The divisors are
  `.65*land` (line 11), `land*.035` (line 13), `people` (lines 23, 30, 35 via
  `urbanNeed/people`), `eliteTotal` (a constant .01), and `max(.0001, urbanNeed)`
  (never zero). The theorems take `0 < land` and `0 < rural` as hypotheses, which give
  `0 < people`.
* JS mutates `s` in place. Here each reassignment is a successive `let` or a field of
  the returned structure. Order of updates is kept.
* `eliteTotal` is the constant `.01` (line 40), not the live sum of elites.
* Not modelled: the output fields `demographicChange` (line 31) and `maintained`
  (line 36), and the `run` summaries (lines 69-78). `coverage` (line 35) is folded into
  `returnIndex`.
* Growth (line 30) is not conserved: the two-region total changes each year by
  `demographicChange`. Only movement (lines 49-65) conserves rural+core+elite.
-/

namespace Angkor.Relocation

open Angkor

/-- Mobility setting, lines 53 and 58: `'open'`, `'elite-only'`, `'workers-only'`.
Any other string (line 5 default is `'open'`) is `other`, which allows neither. -/
inductive Mobility where
  | open_
  | eliteOnly
  | workersOnly
  | other
  deriving DecidableEq

/-- Parameters, line 5 (`defaults`) and the `options` override. `waterFloor` is the
lower bound on water (line 29), `coordination` the harvest multiplier (line 11). -/
structure Params where
  outside : Rat
  portability : Rat
  movingCost : Rat
  localRepair : Rat
  coordination : Rat
  waterFloor : Rat
  mobility : Mobility

/-- Regional state, line 8 (`initial`). `rural`, `core`, `elite` are population,
`land` is a fraction in (0,1], `water` a condition index, `temple` and `store` stocks. -/
structure Region where
  rural : Rat
  core : Rat
  land : Rat
  elite : Rat
  water : Rat
  temple : Rat
  store : Rat

/-- The two regions, `old` and `south` (line 40). -/
structure World where
  old : Region
  south : Region

/-- One year's randomness input: `noise` is `1+.04*(random()-.5)` (line 43) and
`dry` is the drought flag (line 43). -/
structure Year where
  noise : Rat
  dry : Bool

/-- Constant `eliteTotal = .01`, line 40. Not the live sum of elites. -/
def eliteTotal : Rat := 1/100

/-- Weather factor for `old`, line 45: `noise*(dry?.62:1)`. -/
def weatherOld (y : Year) : Rat := y.noise * (if y.dry then 62/100 else 1)

/-- Weather factor for `south`, line 46: `noise*(dry?.85:1)`. -/
def weatherSouth (y : Year) : Rat := y.noise * (if y.dry then 85/100 else 1)

/-- Outputs of `economy`. `region` is the updated state (the JS mutates `s`). `ledger`
is line 33. `returnIndex` is line 37. -/
structure Econ where
  region : Region
  harvest : Rat
  gap : Rat
  hunger : Rat
  ledger : Rat
  returnIndex : Rat

/-- `economy(s, weather, localRepair, eliteShare, coord, waterFloor)`, source lines 9-38.
Each JS assignment to `s.*` becomes a `let` with the same name where possible. The
`s.store` on line 26 is the value after line 22, which `store2` names. -/
def economy (s : Region) (weather localRepair eliteShare coord waterFloor : Rat) : Econ :=
  let before := s.store
  let people := s.rural + s.core + s.elite
  -- line 11
  let harvest := s.land * (3/2) * coord * (13/20 + 7/20 * s.water) * weather
    * min 1 (s.rural / (13/20 * s.land))
  -- line 13
  let maintenanceNeed := s.land * (7/200)
  -- line 14
  let tax := harvest * (1/5) * (3/10 + 7/10 * eliteShare)
  let retained := harvest - tax
  -- lines 15-16
  let farmFood := min s.rural retained
  let farmGap := s.rural - farmFood
  let farmSurplus := retained - farmFood
  -- lines 17-18
  let localUpkeep := min farmSurplus (localRepair * maintenanceNeed)
  let householdOther := farmSurplus - localUpkeep
  -- line 19
  let transportLoss := tax * (2/25)
  let budget0 := tax - transportLoss
  -- line 20
  let urbanNeed := s.core + s.elite
  let urbanFood := min urbanNeed budget0
  let budget1 := budget0 - urbanFood
  -- line 21
  let storageLoss := s.store * (1/25)
  let store1 := s.store - storageLoss
  -- line 22
  let rawGap := farmGap + urbanNeed - urbanFood
  let release := min store1 rawGap
  let store2 := store1 - release
  -- line 23
  let gap := rawGap - release
  let hunger := gap / people
  -- line 24
  let ritual := min budget1 (s.temple * (1/40))
  let budget2 := budget1 - ritual
  -- line 25
  let courtUpkeep := min (budget2 * (9/20)) (max 0 (maintenanceNeed - localUpkeep))
  let budget3 := budget2 - courtUpkeep
  -- line 26
  let deposit := min (budget3 * (7/20)) (max 0 (people - store2))
  let store3 := store2 + deposit
  let budget4 := budget3 - deposit
  -- line 27
  let reclamation := min (budget4 * (11/20)) ((1 - s.land) * (3/20))
  let budget5 := budget4 - reclamation
  -- line 28
  let construction := budget5
  let temple := s.temple + construction
  let land := min 1 (s.land + reclamation * (3/5))
  -- line 29
  let upkeep := localUpkeep + courtUpkeep
  let water := clamp (s.water + (2/25) * (upkeep / maintenanceNeed - s.water)) waterFloor 1
  -- line 30
  let growth := (3/250) * clamp ((harvest - people) / people) (-1) 1 - (2/25) * hunger
  -- lines 31
  let rural := s.rural * (1 + growth)
  let core := s.core * (1 + growth)
  -- line 32
  let foodUsed := farmFood + urbanFood + release
  -- line 33
  let ledger := harvest + before
    - (foodUsed + householdOther + transportLoss + ritual + upkeep + reclamation
       + construction + storageLoss + store3)
  -- line 35
  let coverage := clamp ((urbanFood + release * (urbanNeed / people))
    / max (1/10000) urbanNeed) 0 1
  -- lines 36-37
  { region := { rural := rural, core := core, land := land, elite := s.elite,
                water := water, temple := temple, store := store3 }
    harvest := harvest
    gap := gap
    hunger := hunger
    ledger := ledger
    returnIndex := 13/20 * coverage + 7/20 * water - 2 * hunger }

/-- Elite flow, lines 53-55 for an elite-allowing mobility. Line 55 overwrites line 54,
so the second test takes precedence when both hold (possible only if movingCost < 0). -/
def eliteFlow (p : Params) (adv oldElite southElite : Rat) : Rat :=
  if adv < -p.movingCost then -southElite * min (2/25) (3/25 * (-adv - p.movingCost))
  else if adv > p.movingCost then oldElite * min (2/25) (3/25 * (adv - p.movingCost))
  else 0

/-- Elite movement, line 53 gate (`open` or `elite-only`), lines 54-55 flow. -/
def eliteMove (p : Params) (adv oldElite southElite : Rat) : Rat :=
  if p.mobility = Mobility.open_ ∨ p.mobility = Mobility.eliteOnly then
    eliteFlow p adv oldElite southElite
  else 0

/-- Advantage, lines 48-50. `a` is the post-economy `old` region, so `a.region.water`
is the updated water used on line 49, as in the JS. -/
def advantage (p : Params) (a b : Econ) : Rat :=
  (p.outside * b.returnIndex - (1 - p.portability) * (1/2) * a.region.water) - a.returnIndex

/-- Worker flow, lines 62-63. The two tests use constant `.15`, so they are exclusive. -/
def workerFlow (wa oldCore southCore : Rat) : Rat :=
  if wa > 3/20 then oldCore * min (1/40) (1/25 * (wa - 3/20))
  else if wa < -(3/20) then -southCore * min (1/40) (1/25 * (-wa - 3/20))
  else 0

/-- Worker movement, line 58 gate (`open` or `workers-only`), lines 60-63. `southElite`
is the value after the elite move (line 60 reads `south.elite` after line 56). -/
def workerMove (p : Params) (a b : Econ) (southElite oldCore southCore : Rat) : Rat :=
  if p.mobility = Mobility.open_ ∨ p.mobility = Mobility.workersOnly then
    workerFlow ((b.returnIndex - a.returnIndex) + (southElite / eliteTotal - 1/5) * (3/10))
      oldCore southCore
  else 0

/-- Movement phase, lines 49-65, applied to the two post-economy regions. -/
def movePhase (p : Params) (a b : Econ) : World :=
  let adv := advantage p a b
  let eMove := eliteMove p adv a.region.elite b.region.elite
  let southElite := b.region.elite + eMove
  let wMove := workerMove p a b southElite a.region.core b.region.core
  { old := { a.region with elite := a.region.elite - eMove, core := a.region.core - wMove }
    south := { b.region with elite := southElite, core := b.region.core + wMove } }

/-- One year, lines 43-65: economy for both regions (lines 45-46), then movement. -/
def step (p : Params) (y : Year) (w : World) : World :=
  movePhase p
    (economy w.old (weatherOld y) p.localRepair (w.old.elite / eliteTotal) p.coordination p.waterFloor)
    (economy w.south (weatherSouth y) p.localRepair (w.south.elite / eliteTotal) p.coordination p.waterFloor)

/-- Iterate `step` over a list of year inputs, in order. -/
def runYears (p : Params) : World → List Year → World
  | w, [] => w
  | w, y :: ys => runYears p (step p y w) ys

/-- Rural + core + elite for one region. -/
def regionMass (r : Region) : Rat := r.rural + r.core + r.elite

/-- Two-region total rural + core + elite. -/
def worldMass (w : World) : Rat := regionMass w.old + regionMass w.south

/-- Invariant assumed of a region: positive rural (so people > 0 and the divisions are
defined), nonnegative core and elite, land in (0,1], water in [waterFloor,1], nonnegative
temple and store. -/
def RegionOK (p : Params) (r : Region) : Prop :=
  0 < r.rural ∧ 0 ≤ r.core ∧ 0 ≤ r.elite ∧ 0 < r.land ∧ r.land ≤ 1 ∧
    p.waterFloor ≤ r.water ∧ r.water ≤ 1 ∧ 0 ≤ r.temple ∧ 0 ≤ r.store

/-- Parameter range needed for the bounds: coordination nonnegative, waterFloor in [0,1]. -/
def ParamsOK (p : Params) : Prop :=
  0 ≤ p.coordination ∧ 0 ≤ p.waterFloor ∧ p.waterFloor ≤ 1

/-- World invariant: both regions OK and the two elite stocks sum to `eliteTotal`
(initial values .008 + .002 = .01, lines 40 and 8). -/
def WorldOK (p : Params) (w : World) : Prop :=
  RegionOK p w.old ∧ RegionOK p w.south ∧ w.old.elite + w.south.elite = eliteTotal

/-! ## Target 1: the ledger -/

/-- The economy ledger is exactly zero. No hypotheses are needed. -/
theorem economy_ledger_zero (s : Region) (weather localRepair eliteShare coord waterFloor : Rat) :
    (economy s weather localRepair eliteShare coord waterFloor).ledger = 0 := by
  unfold economy
  grind

/-! ## Generic helper lemmas (each is about abstract rationals) -/

theorem div_le_one_gen {x y : Rat} (hy : 0 < y) (h : x ≤ y) : x / y ≤ 1 := by
  rw [Rat.div_def]
  have hi : 0 ≤ y⁻¹ := Rat.le_of_lt (Rat.inv_pos.mpr hy)
  have hne : y ≠ 0 := by grind
  have hm : y * y⁻¹ = 1 := Rat.mul_inv_cancel y hne
  have hp : 0 ≤ (y - x) * y⁻¹ := Rat.mul_nonneg (by grind) hi
  grind

theorem harvest_nonneg_gen (land coord water weather rural : Rat) (hl : 0 < land)
    (hc : 0 ≤ coord) (hw : 0 ≤ water) (hx : 0 ≤ weather) (hr : 0 ≤ rural) :
    0 ≤ land * (3/2) * coord * (13/20 + 7/20 * water) * weather
      * min 1 (rural / (13/20 * land)) := by
  have hd : 0 < 13/20 * land := by grind
  have hq : 0 ≤ rural / (13/20 * land) := by
    rw [Rat.div_def]
    exact Rat.mul_nonneg hr (Rat.le_of_lt (Rat.inv_pos.mpr hd))
  have hm : 0 ≤ min 1 (rural / (13/20 * land)) := by grind
  have hb : 0 ≤ 13/20 + 7/20 * water := by grind
  have hL : 0 ≤ land * (3/2) := by grind
  exact Rat.mul_nonneg (Rat.mul_nonneg (Rat.mul_nonneg (Rat.mul_nonneg hL hc) hb) hx) hm

theorem tax_gen (H e : Rat) (hH : 0 ≤ H) (he0 : 0 ≤ e) (he1 : e ≤ 1) :
    0 ≤ H * (1/5) * (3/10 + 7/10 * e) ∧ H * (1/5) * (3/10 + 7/10 * e) ≤ H := by
  have ha : 0 ≤ H * (1/5) := by grind
  have hb : 0 ≤ 3/10 + 7/10 * e := by grind
  constructor
  · exact Rat.mul_nonneg ha hb
  · have hp : 0 ≤ H * (1/5) * (1 - (3/10 + 7/10 * e)) := Rat.mul_nonneg ha (by grind)
    grind

theorem gap_generic (R U retained budget S : Rat) (hR : 0 ≤ retained) (hR0 : 0 ≤ R)
    (hU : 0 ≤ U) (hB : 0 ≤ budget) (hS : 0 ≤ S) :
    (R - min R retained) + U - min U budget - min S ((R - min R retained) + U - min U budget)
      ≤ R + U := by
  have h1 : 0 ≤ min R retained := by grind
  have h2 : 0 ≤ min U budget := by grind
  have h3 : 0 ≤ min S ((R - min R retained) + U - min U budget) := by grind
  grind

theorem min_nonneg_gen {a b : Rat} (ha : 0 ≤ a) (hb : 0 ≤ b) : 0 ≤ min a b := by
  first
    | grind
    | exact Rat.le_min ha hb
    | (rw [Rat.min_def]; split <;> grind)

theorem min_le_left_gen (a b : Rat) : min a b ≤ a := by
  first
    | grind
    | exact Rat.min_le_left a b
    | (rw [Rat.min_def]; split <;> grind)

theorem budget0_gen (T : Rat) (hT : 0 ≤ T) : 0 ≤ T - T * (2/25) := by
  grind

theorem storeLoss_gen (T : Rat) (hT : 0 ≤ T) : 0 ≤ T - T * (1/25) := by
  grind

theorem min_le_right_gen (a b : Rat) : min a b ≤ b := by
  first
    | grind
    | exact Rat.min_le_right a b
    | (rw [Rat.min_def]; split <;> grind)

theorem add_nonneg_gen (x y : Rat) (hx : 0 ≤ x) (hy : 0 ≤ y) : 0 ≤ x + y := by
  grind

/-- Budget step: subtracting `min (b*k) c` with `0 ≤ k ≤ 1` keeps the budget nonnegative. -/
theorem bud_gen (b k c : Rat) (hb : 0 ≤ b) (hk0 : 0 ≤ k) (hk1 : k ≤ 1) :
    0 ≤ b - min (b * k) c := by
  have h1 : min (b * k) c ≤ b * k := min_le_left_gen _ _
  have h2 : b * k ≤ b := by
    have := Rat.mul_nonneg hb (show (0 : Rat) ≤ 1 - k by grind)
    grind
  grind

/-- Budget step: subtracting `min b c` keeps the budget nonnegative. -/
theorem bud_min1 (b c : Rat) (hb : 0 ≤ b) : 0 ≤ b - min b c := by
  have := min_le_left_gen b c
  grind

/-- Budget step: subtracting `min a b` keeps the budget nonnegative. -/
theorem bud_min2 (a b : Rat) (hb : 0 ≤ b) : 0 ≤ b - min a b := by
  have := min_le_right_gen a b
  grind

theorem grow_pos (Y hun : Rat) (h : hun ≤ 1) :
    0 < 1 + ((3/250) * clamp Y (-1) 1 - (2/25) * hun) := by
  have := clamp_lower Y (-1) 1
  grind

theorem mul_bounds_gen (x m : Rat) (hx : 0 ≤ x) (hm0 : 0 ≤ m) (hm1 : m ≤ 1) :
    0 ≤ x * m ∧ x * m ≤ x := by
  refine ⟨Rat.mul_nonneg hx hm0, ?_⟩
  have := Rat.mul_nonneg hx (show (0 : Rat) ≤ 1 - m by grind)
  grind

theorem eliteTotal_pos : 0 < eliteTotal := by
  unfold eliteTotal
  grind

theorem share_gen (x y : Rat) (hx : 0 ≤ x) (hy : 0 ≤ y) (h : x + y = eliteTotal) :
    0 ≤ x / eliteTotal ∧ x / eliteTotal ≤ 1 := by
  have hpos := eliteTotal_pos
  refine ⟨?_, div_le_one_gen hpos (by grind)⟩
  rw [Rat.div_def]
  exact Rat.mul_nonneg hx (Rat.le_of_lt (Rat.inv_pos.mpr hpos))

/-! ## Economy: region invariants -/

/-- Gap is at most total population: the gap is at most `rawGap`, which is at most
`farmGap + urbanNeed`, which is at most `rural + core + elite`. -/
theorem economy_gap_le (s : Region) (w l e c f : Rat) (hr : 0 < s.rural) (hc : 0 ≤ s.core)
    (he : 0 ≤ s.elite) (hl : 0 < s.land) (hw : 0 ≤ w) (hcoord : 0 ≤ c) (hwf : 0 ≤ f)
    (hwater : f ≤ s.water) (hs : 0 ≤ s.store) (he0 : 0 ≤ e) (he1 : e ≤ 1) :
    (economy s w l e c f).gap ≤ s.rural + s.core + s.elite := by
  have hw0 : 0 ≤ s.water := Rat.le_trans hwf hwater
  have hH := harvest_nonneg_gen s.land c s.water w s.rural hl hcoord hw0 hw (Rat.le_of_lt hr)
  have hT := tax_gen _ e hH he0 he1
  have hT1 := hT.1
  have hT2 := hT.2
  dsimp only [economy]
  refine Rat.le_trans (gap_generic _ _ _ _ _ ?_ ?_ ?_ ?_ ?_) ?_
  all_goals grind

/-- Hunger is at most one (its numerator is at most the population). -/
theorem economy_hunger_le (s : Region) (w l e c f : Rat) (hr : 0 < s.rural) (hc : 0 ≤ s.core)
    (he : 0 ≤ s.elite) (hl : 0 < s.land) (hw : 0 ≤ w) (hcoord : 0 ≤ c) (hwf : 0 ≤ f)
    (hwater : f ≤ s.water) (hs : 0 ≤ s.store) (he0 : 0 ≤ e) (he1 : e ≤ 1) :
    (economy s w l e c f).hunger ≤ 1 := by
  have hgap := economy_gap_le s w l e c f hr hc he hl hw hcoord hwf hwater hs he0 he1
  have hpos : 0 < s.rural + s.core + s.elite := by grind
  dsimp only [economy] at hgap ⊢
  exact div_le_one_gen hpos hgap

/-- One economy call keeps a region OK. Uses `0 ≤ weather` and `0 ≤ eliteShare ≤ 1`. -/
theorem economy_region_ok (p : Params) (s : Region) (w e : Rat) (hp : ParamsOK p)
    (hR : RegionOK p s) (hw : 0 ≤ w) (he0 : 0 ≤ e) (he1 : e ≤ 1) :
    RegionOK p (economy s w p.localRepair e p.coordination p.waterFloor).region := by
  unfold RegionOK at hR
  obtain ⟨hr, hc, he, hl, hl1, hwf, hw1, ht, hs⟩ := hR
  obtain ⟨hco, hf0, hf1⟩ := hp
  have hw0 : 0 ≤ s.water := Rat.le_trans hf0 hwf
  have hH := harvest_nonneg_gen s.land p.coordination s.water w s.rural hl hco hw0 hw
    (Rat.le_of_lt hr)
  have hT := tax_gen _ e hH he0 he1
  have hT1 := hT.1
  have hT2 := hT.2
  have hhun := economy_hunger_le s w p.localRepair e p.coordination p.waterFloor hr hc he hl hw
    hco hf0 hwf hs he0 he1
  dsimp only [economy] at hhun
  unfold RegionOK
  dsimp only [economy]
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact Rat.mul_pos hr (grow_pos _ _ hhun)
  · exact Rat.mul_nonneg hc (Rat.le_of_lt (grow_pos _ _ hhun))
  · exact he
  · grind
  · grind
  · exact clamp_lower _ _ _
  · exact clamp_upper _ _ _ hf1
  · -- temple + construction, construction = budget5 peeled step by step
    apply add_nonneg_gen _ _ ht
    refine bud_gen _ _ _ ?_ (by grind) (by grind)
    refine bud_gen _ _ _ ?_ (by grind) (by grind)
    refine bud_gen _ _ _ ?_ (by grind) (by grind)
    refine bud_min1 _ _ ?_
    refine bud_min2 _ _ ?_
    exact budget0_gen _ hT1
  · -- store3 = (store1 - release) + deposit
    apply add_nonneg_gen
    · refine bud_min1 _ _ ?_
      exact storeLoss_gen _ hs
    · refine min_nonneg_gen ?_ ?_
      · refine Rat.mul_nonneg ?_ (by grind)
        refine bud_gen _ _ _ ?_ (by grind) (by grind)
        refine bud_min1 _ _ ?_
        refine bud_min2 _ _ ?_
        exact budget0_gen _ hT1
      · first
          | exact Rat.le_max_left _ _
          | grind

/-- Land never decreases in one economy call. -/
theorem economy_land_nondecreasing (s : Region) (w l e c f : Rat) (hl : 0 < s.land)
    (hl1 : s.land ≤ 1) (hr : 0 < s.rural) (hc : 0 ≤ s.core) (he : 0 ≤ s.elite) (hw : 0 ≤ w)
    (hcoord : 0 ≤ c) (hwf : 0 ≤ f) (hwater : f ≤ s.water) (hs : 0 ≤ s.store)
    (he0 : 0 ≤ e) (he1 : e ≤ 1) (ht : 0 ≤ s.temple) :
    s.land ≤ (economy s w l e c f).region.land := by
  have hw0 : 0 ≤ s.water := Rat.le_trans hwf hwater
  have hH := harvest_nonneg_gen s.land c s.water w s.rural hl hcoord hw0 hw (Rat.le_of_lt hr)
  have hT := tax_gen _ e hH he0 he1
  have hT1 := hT.1
  have hT2 := hT.2
  dsimp only [economy]
  grind

/-! ## Movement -/

theorem eliteFlow_bounds (p : Params) (adv oldE sE : Rat) (h0 : 0 ≤ oldE) (h1 : 0 ≤ sE) :
    -sE ≤ eliteFlow p adv oldE sE ∧ eliteFlow p adv oldE sE ≤ oldE := by
  unfold eliteFlow
  by_cases hA : adv < -p.movingCost
  · rw [if_pos hA]
    have hm0 : 0 ≤ min (2/25) (3/25 * (-adv - p.movingCost)) := by grind
    have hm1 : min (2/25) (3/25 * (-adv - p.movingCost)) ≤ 1 := by grind
    have := mul_bounds_gen sE _ h1 hm0 hm1
    grind
  · rw [if_neg hA]
    by_cases hB : adv > p.movingCost
    · rw [if_pos hB]
      have hm0 : 0 ≤ min (2/25) (3/25 * (adv - p.movingCost)) := by grind
      have hm1 : min (2/25) (3/25 * (adv - p.movingCost)) ≤ 1 := by grind
      have := mul_bounds_gen oldE _ h0 hm0 hm1
      grind
    · rw [if_neg hB]
      grind

/-- Elite flow never takes more than the origin stock, nor more than the source's stock. -/
theorem eliteMove_bounds (p : Params) (adv oldE sE : Rat) (h0 : 0 ≤ oldE) (h1 : 0 ≤ sE) :
    -sE ≤ eliteMove p adv oldE sE ∧ eliteMove p adv oldE sE ≤ oldE := by
  unfold eliteMove
  by_cases hg : p.mobility = Mobility.open_ ∨ p.mobility = Mobility.eliteOnly
  · rw [if_pos hg]
    exact eliteFlow_bounds p adv oldE sE h0 h1
  · rw [if_neg hg]
    grind

theorem workerFlow_bounds (oc sc wa : Rat) (h0 : 0 ≤ oc) (h1 : 0 ≤ sc) :
    -sc ≤ workerFlow wa oc sc ∧ workerFlow wa oc sc ≤ oc := by
  unfold workerFlow
  by_cases hA : wa > 3/20
  · rw [if_pos hA]
    have hm0 : 0 ≤ min (1/40) (1/25 * (wa - 3/20)) :=
      min_nonneg_gen (by grind) (by grind)
    have hm1 : min (1/40) (1/25 * (wa - 3/20)) ≤ 1 :=
      Rat.le_trans (min_le_left_gen _ _) (by grind)
    have := mul_bounds_gen oc _ h0 hm0 hm1
    grind
  · rw [if_neg hA]
    by_cases hB : wa < -(3/20)
    · rw [if_pos hB]
      have hm0 : 0 ≤ min (1/40) (1/25 * (-wa - 3/20)) :=
        min_nonneg_gen (by grind) (by grind)
      have hm1 : min (1/40) (1/25 * (-wa - 3/20)) ≤ 1 :=
        Rat.le_trans (min_le_left_gen _ _) (by grind)
      have := mul_bounds_gen sc _ h1 hm0 hm1
      grind
    · rw [if_neg hB]
      exact ⟨by grind, h0⟩

theorem workerMove_bounds (p : Params) (a b : Econ) (sE oc sc : Rat) (h0 : 0 ≤ oc)
    (h1 : 0 ≤ sc) :
    -sc ≤ workerMove p a b sE oc sc ∧ workerMove p a b sE oc sc ≤ oc := by
  unfold workerMove
  by_cases hg : p.mobility = Mobility.open_ ∨ p.mobility = Mobility.workersOnly
  · rw [if_pos hg]
    exact workerFlow_bounds _ _ _ h0 h1
  · rw [if_neg hg]
    grind

/-- Movement keeps both regions OK, given both inputs are OK. -/
theorem movePhase_ok (p : Params) (a b : Econ) (hA : RegionOK p a.region)
    (hB : RegionOK p b.region) :
    RegionOK p (movePhase p a b).old ∧ RegionOK p (movePhase p a b).south := by
  unfold RegionOK at hA hB
  obtain ⟨ar, ac, ae, al, al1, aw, aw1, at', as'⟩ := hA
  obtain ⟨br, bc, be, bl, bl1, bw, bw1, bt, bs⟩ := hB
  have hE := eliteMove_bounds p (advantage p a b) a.region.elite b.region.elite ae be
  have hW := workerMove_bounds p a b
    (b.region.elite + eliteMove p (advantage p a b) a.region.elite b.region.elite)
    a.region.core b.region.core ac bc
  unfold movePhase
  dsimp only
  unfold RegionOK
  constructor
  · refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> grind
  · refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> grind

theorem movePhase_mass (p : Params) (a b : Econ) :
    worldMass (movePhase p a b) = regionMass a.region + regionMass b.region := by
  unfold movePhase worldMass regionMass
  dsimp only
  grind

theorem movePhase_elite_sum (p : Params) (a b : Econ) :
    (movePhase p a b).old.elite + (movePhase p a b).south.elite
      = a.region.elite + b.region.elite := by
  unfold movePhase
  dsimp only
  grind

/-! ## One year and the list iteration -/

theorem weather_old_nonneg (y : Year) (hn : 0 ≤ y.noise) : 0 ≤ weatherOld y := by
  unfold weatherOld
  cases y.dry <;> simp <;> grind

theorem weather_south_nonneg (y : Year) (hn : 0 ≤ y.noise) : 0 ≤ weatherSouth y := by
  unfold weatherSouth
  cases y.dry <;> simp <;> grind

theorem step_elite_sum (p : Params) (y : Year) (w : World) :
    (step p y w).old.elite + (step p y w).south.elite = w.old.elite + w.south.elite := by
  unfold step
  rw [movePhase_elite_sum]
  rfl

/-- The two elite stocks keep their total (= `eliteTotal`) through a year. -/
theorem step_ok (p : Params) (y : Year) (w : World) (hp : ParamsOK p) (hw : WorldOK p w)
    (hn : 0 ≤ y.noise) : WorldOK p (step p y w) := by
  obtain ⟨hO, hS, hsum⟩ := hw
  have hO' := hO
  have hS' := hS
  unfold RegionOK at hO' hS'
  obtain ⟨hr1, hc1, he1, -, -, -, -, -, -⟩ := hO'
  obtain ⟨hr2, hc2, he2, -, -, -, -, -, -⟩ := hS'
  obtain ⟨hsh0, hsh1⟩ := share_gen w.old.elite w.south.elite he1 he2 hsum
  obtain ⟨hsh0', hsh1'⟩ := share_gen w.south.elite w.old.elite he2 he1
    (by grind)
  have hEo := economy_region_ok p w.old (weatherOld y) (w.old.elite / eliteTotal) hp hO
    (weather_old_nonneg y hn) hsh0 hsh1
  have hEs := economy_region_ok p w.south (weatherSouth y) (w.south.elite / eliteTotal) hp hS
    (weather_south_nonneg y hn) hsh0' hsh1'
  obtain ⟨hMo, hMs⟩ := movePhase_ok p _ _ hEo hEs
  refine ⟨hMo, hMs, ?_⟩
  unfold step
  rw [movePhase_elite_sum]
  exact hsum

theorem runYears_ok (p : Params) (hp : ParamsOK p) :
    ∀ (ys : List Year) (w : World), WorldOK p w → (∀ y ∈ ys, 0 ≤ y.noise) →
      WorldOK p (runYears p w ys)
  | [], _, hw, _ => hw
  | y :: ys, w, hw, hn =>
    runYears_ok p hp ys (step p y w) (step_ok p y w hp hw (hn y (by simp)))
      (fun z hz => hn z (by simp [hz]))

theorem runYears_elite_sum (p : Params) :
    ∀ (ys : List Year) (w : World),
      (runYears p w ys).old.elite + (runYears p w ys).south.elite
        = w.old.elite + w.south.elite
  | [], _ => rfl
  | y :: ys, w => by
    rw [show runYears p w (y :: ys) = runYears p (step p y w) ys from rfl,
      runYears_elite_sum p ys (step p y w), step_elite_sum]

/-! ## Target 3 and 4 summaries -/

/-- Elite shares stay in [0,1] in both regions, given the world invariant. -/
theorem elite_shares_in_unit (p : Params) (w : World) (hw : WorldOK p w) :
    0 ≤ w.old.elite / eliteTotal ∧ w.old.elite / eliteTotal ≤ 1 ∧
      0 ≤ w.south.elite / eliteTotal ∧ w.south.elite / eliteTotal ≤ 1 := by
  obtain ⟨hO, hS, hsum⟩ := hw
  unfold RegionOK at hO hS
  obtain ⟨-, -, he1, -, -, -, -, -, -⟩ := hO
  obtain ⟨-, -, he2, -, -, -, -, -, -⟩ := hS
  obtain ⟨a1, a2⟩ := share_gen w.old.elite w.south.elite he1 he2 hsum
  obtain ⟨b1, b2⟩ := share_gen w.south.elite w.old.elite he2 he1 (by grind)
  exact ⟨a1, a2, b1, b2⟩

/-- Concrete parameter set: the source defaults (line 5) with waterFloor 0. -/
def defaultParams : Params :=
  { outside := 6/5, portability := 3/4, movingCost := 1/4, localRepair := 1/2,
    coordination := 1, waterFloor := 0, mobility := Mobility.open_ }

/-- Initial world: lines 8 and 40 (`initial(.16,.015,.2,.008)` and
`initial(.05,.005,.08,.002)`). Reachable at year 0. -/
def initWorld : World :=
  { old := { rural := 16/100, core := 15/1000, land := 2/10, elite := 8/1000,
             water := 6/10, temple := 0, store := 3/100 },
    south := { rural := 5/100, core := 5/1000, land := 8/100, elite := 2/1000,
               water := 6/10, temple := 0, store := 3/100 } }

/-- The source defaults and the initial world satisfy the invariant (non-vacuity). -/
theorem initWorld_ok : WorldOK defaultParams initWorld := by
  unfold WorldOK RegionOK defaultParams initWorld eliteTotal
  refine ⟨⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩, ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩, ?_⟩ <;>
    grind

/-! ## Target 5: when movement is zero -/

/-- No elite moves when |advantage| <= movingCost, written as -mc <= adv <= mc. -/
theorem eliteMove_zero_of_within_cost (p : Params) (adv oldE sE : Rat)
    (hlo : -p.movingCost ≤ adv) (hhi : adv ≤ p.movingCost) :
    eliteMove p adv oldE sE = 0 := by
  have hA : ¬ (adv < -p.movingCost) := by grind
  have hB : ¬ (adv > p.movingCost) := by grind
  unfold eliteMove eliteFlow
  rw [if_neg hA, if_neg hB]
  split <;> rfl

theorem eliteMove_zero_of_workers_only (p : Params) (adv oldE sE : Rat)
    (h : p.mobility = Mobility.workersOnly) : eliteMove p adv oldE sE = 0 := by
  simp [eliteMove, h]

theorem eliteMove_zero_of_other (p : Params) (adv oldE sE : Rat)
    (h : p.mobility = Mobility.other) : eliteMove p adv oldE sE = 0 := by
  simp [eliteMove, h]

theorem workerMove_zero_of_elite_only (p : Params) (a b : Econ) (sE oc sc : Rat)
    (h : p.mobility = Mobility.eliteOnly) : workerMove p a b sE oc sc = 0 := by
  simp [workerMove, h]

/-- With movingCost >= 0, the two elite tests cannot both hold. -/
theorem elite_branches_exclusive (p : Params) (adv : Rat) (h : 0 ≤ p.movingCost) :
    ¬ (adv < -p.movingCost ∧ p.movingCost < adv) := by
  grind

/-- With movingCost < 0 both tests can hold at once. In that case the second
(line 55) overwrites the first, so elite flows from south to old even though
the south has the advantage. Parameter is outside the UI range [0, 0.6]. -/
theorem negative_movingCost_wrong_direction :
    ∃ (p : Params) (adv oldE sE : Rat), p.movingCost < 0 ∧ p.mobility = Mobility.open_ ∧
      0 < adv ∧ 0 ≤ oldE ∧ 0 < sE ∧ eliteMove p adv oldE sE < 0 :=
  ⟨{ outside := 6/5, portability := 3/4, movingCost := -1/4, localRepair := 1/2,
     coordination := 1, waterFloor := 0, mobility := Mobility.open_ },
   1/10, 8/1000, 2/1000, by grind, by rfl, by grind, by grind, by grind, by
     unfold eliteMove eliteFlow; grind⟩

end Angkor.Relocation
