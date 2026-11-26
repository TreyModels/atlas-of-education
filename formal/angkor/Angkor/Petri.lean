import Angkor.Basic

/-!
# One year of the Angkor Petri engine

Formalizes one year step of `public/engines/petri.js` (`run`, year loop, source lines 11-53)
exactly as written, the scenario drought schedule (line 12), and the iteration over a list of
weather inputs.

Conventions (see `CONVENTIONS.md`):
* Exact rationals (`Rat`) stand in for JavaScript doubles. Theorems are about ideal arithmetic,
  not IEEE rounding.
* Randomness is an input. The weather draw `u` enters through `weatherOf u = 1 + .04*(u - .5)`
  (source line 12); the step itself takes the weather value `w` directly. The drought flag is an
  input to the step; `droughtYear` gives the scenario schedule (source line 12).
* Division by zero, flagged per division: `labourOf` divides by `max (1/1000) (.65*land) >= 1/1000`;
  `hungerOf` and the source's `people?gap/people:0` are guarded to 0 when `people = 0`;
  `foodMargin` divides by `max (1/1000) people >= 1/1000`; `maintained` is guarded to 1 when
  `maintenanceNeed = 0`, as in the source.
* Knockouts: `Knockout` lists the five values the source tests against; any other string
  behaves as `noKnockout`.
* Scalar constants are exact: `.035` is `35/1000`, `.6` is `6/10`, and so on.
-/

namespace Angkor.Petri

/-- Knockout switch. Source: `p.knockout`, tested at lines 9, 14, 17, 25, 28, 37 (`'coordination'`,
`'water'`, `'transport'`, `'relief'`, `'temple'`). Any other value is `noKnockout`. -/
inductive Knockout where
  | noKnockout
  | coordination
  | water
  | transport
  | relief
  | temple
  deriving DecidableEq, Repr

/-- Scenario parameters that the year step reads. Source: `p` (line 9), fields `extraction`
(line 18), `maintenance` (line 31), `relief` (line 25), `coordination` (line 9), `waterFloor`
(line 37), `knockout`. -/
structure Params where
  extraction : Rat
  maintenance : Rat
  relief : Rat
  coordination : Rat
  waterFloor : Rat
  knockout : Knockout

/-- The parameter ranges assumed by the state-invariant theorems: extraction, maintenance and
relief in `[0,1]`, coordination `>= 0`, waterFloor in `[0,1]`. -/
def ParamsInRange (p : Params) : Prop :=
  0 ≤ p.extraction ∧ p.extraction ≤ 1 ∧
  0 ≤ p.maintenance ∧ p.maintenance ≤ 1 ∧
  0 ≤ p.relief ∧ p.relief ≤ 1 ∧
  0 ≤ p.coordination ∧
  0 ≤ p.waterFloor ∧ p.waterFloor ≤ 1

/-- Year-to-year state. Source: `let rural, core, land, water, temple, store` (line 10). -/
structure State where
  rural : Rat
  core : Rat
  land : Rat
  water : Rat
  temple : Rat
  store : Rat

/-- Starting state. Source: line 10, `rural=.16, core=.015, land=.2, water=.5, temple=0, store=.03`. -/
def initState : State where
  rural := 16/100
  core := 15/1000
  land := 2/10
  water := 1/2
  temple := 0
  store := 3/100

/-- Invariant on states. Positive residents and land in `(0,1]`, water in `[waterFloor, 1]`,
temple and store nonnegative. -/
def StateOK (p : Params) (s : State) : Prop :=
  0 < s.rural ∧ 0 < s.core ∧
  0 < s.land ∧ s.land ≤ 1 ∧
  p.waterFloor ≤ s.water ∧ s.water ≤ 1 ∧
  0 ≤ s.temple ∧ 0 ≤ s.store

/-- Scenario drought schedule. Source: line 12,
`drought = p.scenario==='drought' && ((year>=150&&year<175)||(year>=190&&year<205))`.
The scenario string is reduced to the flag `scenarioDrought`. -/
def droughtYear (scenarioDrought : Bool) (year : Nat) : Bool :=
  scenarioDrought && ((150 ≤ year && year < 175) || (190 ≤ year && year < 205))

/-- Weather from a uniform draw `u`. Source: line 12, `1+.04*(random()-.5)`. The draw is an input;
for `u` in `[0,1)` the weather lies in `[0.98, 1.02)`. -/
def weatherOf (u : Rat) : Rat := 1 + 4/100 * (u - 1/2)

/-- Climate factor. Source: line 13, `climate=weather*(drought?.62:1)`. -/
def climateOf (weather : Rat) (drought : Bool) : Rat :=
  weather * (if drought then 62/100 else 1)

/-- Effective coordination, after the knockout. Source: line 9,
`coord=p.knockout==='coordination'?1:p.coordination`. -/
def coordOf (p : Params) : Rat :=
  if p.knockout = .coordination then 1 else p.coordination

/-- Hydraulic condition. Source: line 14, `hydraulic=p.knockout==='water'?1:.65+.35*water`. -/
def hydraulicOf (p : Params) (water : Rat) : Rat :=
  if p.knockout = .water then 1 else 65/100 + 35/100 * water

/-- Labour factor. Source: line 15, `Math.min(1,rural/Math.max(.001,.65*land))`. -/
def labourOf (rural land : Rat) : Rat :=
  min 1 (rural / max (1/1000) (65/100 * land))

/-- Transport retention. Source: line 17, `p.knockout==='transport'?1:.92`. -/
def transportOf (p : Params) : Rat :=
  if p.knockout = .transport then 1 else 92/100

/-- Core food from the treasury. Source: line 22, `Math.min(coreNeed,treasury)`. -/
def coreFoodOf (core treasury : Rat) : Rat := min core treasury

/-- Temple obligation. Source: line 28, `p.knockout==='temple'?0:temple*.025`. -/
def obligationOf (p : Params) (temple : Rat) : Rat :=
  if p.knockout = .temple then 0 else temple * (25/1000)

/-- Release from store. Source: line 25, `p.knockout==='relief'?0:Math.min(store,householdGap*p.relief)`
(with `store` the value after storage loss). -/
def releaseOf (p : Params) (store1 householdGap : Rat) : Rat :=
  if p.knockout = .relief then 0 else min store1 (householdGap * p.relief)

/-- Water update. Source: line 37,
`if(p.knockout!=='water')water=Math.max(p.waterFloor,Math.min(1,water+.08*(maintained-water)));`. -/
def waterNextOf (p : Params) (water maintained : Rat) : Rat :=
  if p.knockout = .water then water
  else max p.waterFloor (min 1 (water + 8/100 * (maintained - water)))

/-- Hunger ratio. Source: line 38, `people?gap/people:0`. -/
def hungerOf (gap people : Rat) : Rat :=
  if people = 0 then 0 else gap / people

/-- Food margin. Source: line 39, `(harvest-people)/Math.max(.001,people)`. -/
def foodMarginOf (harvest people : Rat) : Rat :=
  (harvest - people) / max (1/1000) people

/-- Growth rate. Source: line 40, `.012*Math.max(-1,Math.min(1,foodMargin))`. -/
def growthOf (foodMargin : Rat) : Rat :=
  12/1000 * clamp foodMargin (-1) 1

/-- Migration attractiveness. Source: line 44, `Math.min(.22,.025+temple*.015)`. -/
def attractivenessOf (temple : Rat) : Rat :=
  min (22/100) (25/1000 + temple * (15/1000))

/-- Migration before clamping. Source: lines 45-47, with `rural`, `core` the post-floor values
(lines 41-42) and `temple` the value after construction (line 35). -/
def migrationRaw (rural1 core1 temple1 hunger : Rat) : Rat :=
  let m := (rural1 + core1) * attractivenessOf temple1 - core1
  let m := m * (if hunger > 2/100 then 15/100 else 35/1000)
  if hunger > 2/100 then m - core1 * (8/100) * min 1 (hunger * 5) else m

/-- Migration after clamping. Source: line 48,
`Math.max(-core*.2,Math.min(rural*.03,migration))`. A positive value moves people from rural to core. -/
def migrationOf (rural1 core1 temple1 hunger : Rat) : Rat :=
  clamp (migrationRaw rural1 core1 temple1 hunger) (-(core1 * (2/10))) (rural1 * (3/100))


/-- Lean-side year: every intermediate of one pass of the source loop body (source lines 12-51),
named after the source variable. `next` fields are the state carried to the next year. -/
structure Year where
  people : Rat
  climate : Rat
  hydraulic : Rat
  labour : Rat
  harvest : Rat
  collected : Rat
  retained : Rat
  delivered : Rat
  transportLoss : Rat
  localFood : Rat
  unusedLocal : Rat
  treasury0 : Rat
  coreFood : Rat
  treasury1 : Rat
  storageLoss : Rat
  store1 : Rat
  householdGap : Rat
  release : Rat
  store2 : Rat
  gap : Rat
  obligation : Rat
  ritual : Rat
  treasury2 : Rat
  maintenanceNeed : Rat
  upkeep : Rat
  treasury3 : Rat
  maintained : Rat
  deposit : Rat
  store3 : Rat
  treasury4 : Rat
  reclamation : Rat
  construction : Rat
  temple : Rat
  land : Rat
  water : Rat
  hunger : Rat
  foodMargin : Rat
  growth : Rat
  rawRural : Rat
  rawCore : Rat
  rural1 : Rat
  core1 : Rat
  migration : Rat
  rural : Rat
  core : Rat
  foodUsed : Rat
  ledger : Rat

/-- One year step. Source: lines 12-51 of `run`. Inputs: the parameters `p`, the state `s` at the
start of the year, the weather value `weather` (line 12), and the drought flag `drought` (line 12). -/
def year (p : Params) (s : State) (weather : Rat) (drought : Bool) : Year :=
  let people := s.rural + s.core
  let climate := climateOf weather drought
  let hydraulic := hydraulicOf p s.water
  let labour := labourOf s.rural s.land
  let harvest := s.land * (3/2) * coordOf p * hydraulic * climate * labour
  let collected := min harvest (p.extraction * harvest)
  let retained := harvest - collected
  let delivered := collected * transportOf p
  let transportLoss := collected - delivered
  let localFood := min s.rural retained
  let unusedLocal := max 0 (retained - localFood)
  let treasury0 := delivered + unusedLocal
  let coreFood := coreFoodOf s.core treasury0
  let treasury1 := treasury0 - coreFood
  let storageLoss := s.store * (4/100)
  let store1 := s.store - storageLoss
  let householdGap := max 0 (s.rural - localFood) + max 0 (s.core - coreFood)
  let release := releaseOf p store1 householdGap
  let store2 := store1 - release
  let gap := householdGap - release
  let obligation := obligationOf p s.temple
  let ritual := min treasury1 obligation
  let treasury2 := treasury1 - ritual
  let maintenanceNeed := s.land * (35/1000)
  let upkeep := min (treasury2 * p.maintenance) maintenanceNeed
  let treasury3 := treasury2 - upkeep
  let maintained := if maintenanceNeed = 0 then 1 else upkeep / maintenanceNeed
  let deposit := min (treasury3 * (35/100)) (max 0 (people - store2))
  let store3 := store2 + deposit
  let treasury4 := treasury3 - deposit
  let reclamation := min (treasury4 * (55/100)) (max 0 (1 - s.land) * (15/100))
  let construction := treasury4 - reclamation
  let temple := s.temple + construction
  let land := min 1 (s.land + reclamation * (6/10))
  let water := waterNextOf p s.water maintained
  let hunger := hungerOf gap people
  let foodMargin := foodMarginOf harvest people
  let growth := growthOf foodMargin
  let rawRural := s.rural * (1 + growth - 8/100 * hunger)
  let rawCore := s.core * (1 + growth - 8/100 * hunger)
  let rural1 := max (1/1000) rawRural
  let core1 := max (1/10000) rawCore
  let migration := migrationOf rural1 core1 temple hunger
  let rural := rural1 - migration
  let core := core1 + migration
  let foodUsed := localFood + coreFood + release
  let ledger := harvest + s.store - (foodUsed + ritual + upkeep + deposit + reclamation
    + construction + transportLoss + storageLoss + (store3 - deposit))
  { people := people, climate := climate, hydraulic := hydraulic, labour := labour,
    harvest := harvest, collected := collected, retained := retained, delivered := delivered,
    transportLoss := transportLoss, localFood := localFood, unusedLocal := unusedLocal,
    treasury0 := treasury0, coreFood := coreFood, treasury1 := treasury1,
    storageLoss := storageLoss, store1 := store1, householdGap := householdGap,
    release := release, store2 := store2, gap := gap, obligation := obligation,
    ritual := ritual, treasury2 := treasury2, maintenanceNeed := maintenanceNeed,
    upkeep := upkeep, treasury3 := treasury3, maintained := maintained, deposit := deposit,
    store3 := store3, treasury4 := treasury4, reclamation := reclamation,
    construction := construction, temple := temple, land := land, water := water,
    hunger := hunger, foodMargin := foodMargin, growth := growth, rawRural := rawRural,
    rawCore := rawCore, rural1 := rural1, core1 := core1, migration := migration,
    rural := rural, core := core, foodUsed := foodUsed, ledger := ledger }

/-- The next state. Source: the end of the loop body, lines 36, 37, 41-42, 48 and the `store`
updates at lines 23, 25, 33. -/
def step (p : Params) (s : State) (weather : Rat) (drought : Bool) : State :=
  let y := year p s weather drought
  { rural := y.rural, core := y.core, land := y.land, water := y.water,
    temple := y.temple, store := y.store3 }

/-- Iterate the year step over a list of `(weather, drought)` inputs, oldest year first. -/
def runYears (p : Params) : State → List (Rat × Bool) → State
  | s, [] => s
  | s, (w, d) :: rest => runYears p (step p s w d) rest

/-- Ledger identity, source line 50. -/
theorem ledger_zero (p : Params) (s : State) (w : Rat) (d : Bool) :
    (year p s w d).ledger = 0 := by
  unfold year
  grind


/-! ## Helper lemmas on the stage functions -/

/-- Nonnegative quotient over a positive denominator. Used for the source divisions at lines
15, 38 and 39 (denominators `>= .001` or guarded). -/
theorem tdiv_nonneg (a b : Rat) (ha : 0 ≤ a) (hb : 0 < b) : 0 ≤ a / b := by
  have hb0 : 0 ≤ b := by grind
  have hne : b ≠ 0 := by grind
  have hi : b * b⁻¹ = 1 := Rat.mul_inv_cancel b hne
  have hinv : 0 ≤ b⁻¹ := by
    by_cases h : 0 ≤ b⁻¹
    · exact h
    · have h1 : b⁻¹ ≤ 0 := by grind
      have h2 := Rat.mul_le_mul_of_nonneg_left h1 hb0
      rw [Rat.mul_zero] at h2
      grind
  rw [Rat.div_def]
  exact Rat.mul_nonneg ha hinv

theorem transportOf_bounds (p : Params) : 0 ≤ transportOf p ∧ transportOf p ≤ 1 := by
  unfold transportOf; split <;> grind

theorem coordOf_nonneg (p : Params) (h : 0 ≤ p.coordination) : 0 ≤ coordOf p := by
  unfold coordOf; split <;> grind

theorem hydraulicOf_nonneg (p : Params) (w : Rat) (h : 0 ≤ w) : 0 ≤ hydraulicOf p w := by
  unfold hydraulicOf; split <;> grind

theorem climateOf_nonneg (w : Rat) (d : Bool) (h : 0 ≤ w) : 0 ≤ climateOf w d := by
  unfold climateOf; split <;> grind

theorem labourOf_nonneg (r l : Rat) (h : 0 ≤ r) : 0 ≤ labourOf r l := by
  unfold labourOf
  have hpos : (0:Rat) < 1/1000 := by grind
  have hd : 0 < max (1/1000) (65/100 * l) := by grind
  have := tdiv_nonneg r (max (1/1000) (65/100 * l)) h hd
  grind

/-- Product of three factors is monotone in the middle one when the outer factors are nonnegative. -/
theorem mul3_mono (X c1 c2 L : Rat) (hX : 0 ≤ X) (hL : 0 ≤ L) (h : c1 ≤ c2) :
    X * c1 * L ≤ X * c2 * L :=
  Rat.mul_le_mul_of_nonneg_right (Rat.mul_le_mul_of_nonneg_left h hX) hL

/-- Release is at most the household gap (relief in `[0,1]`) and at most the store. Source line 25. -/
theorem releaseOf_bounds (p : Params) (s1 hg : Rat) (h1 : 0 ≤ s1) (hg0 : 0 ≤ hg)
    (hr0 : 0 ≤ p.relief) (hr1 : p.relief ≤ 1) :
    0 ≤ releaseOf p s1 hg ∧ releaseOf p s1 hg ≤ s1 ∧ releaseOf p s1 hg ≤ hg := by
  have h2 : hg * p.relief ≤ hg * 1 := Rat.mul_le_mul_of_nonneg_left hr1 hg0
  rw [Rat.mul_one] at h2
  have h3 := Rat.mul_nonneg hg0 hr0
  unfold releaseOf
  by_cases hk : p.knockout = .relief
  · simp only [hk, ite_true]
    grind
  · simp only [hk, ite_false]
    grind

/-- Water update bounds. Source line 37. -/
theorem waterNextOf_bounds (p : Params) (w m : Rat) (hwf : p.waterFloor ≤ w) (hw1 : w ≤ 1) :
    p.waterFloor ≤ waterNextOf p w m ∧ waterNextOf p w m ≤ 1 := by
  constructor <;> (unfold waterNextOf; split <;> grind)

/-- Migration conserves rural plus core (source lines 45-48), taken separately from the births and
deaths in lines 41-42. -/
theorem migration_conserves (r c t h : Rat) :
    (r - migrationOf r c t h) + (c + migrationOf r c t h) = r + c := by
  grind

/-- Upper clamp of migration: at most `.03` of rural residents leave in a year. -/
theorem migration_le (r c t h : Rat) (hr : 0 ≤ r) (hc : 0 ≤ c) :
    migrationOf r c t h ≤ r * (3/100) := by
  unfold migrationOf
  exact clamp_upper _ _ _ (by grind)

/-- Lower clamp of migration: at most `.2` of core residents leave in a year. -/
theorem migration_ge (r c t h : Rat) :
    -(c * (2/10)) ≤ migrationOf r c t h := by
  unfold migrationOf
  exact clamp_lower _ _ _

/-- After migration, rural residents stay positive when they were positive and core is nonnegative. -/
theorem migration_rural_pos (r c t h : Rat) (hr : 0 < r) (hc : 0 ≤ c) :
    0 < r - migrationOf r c t h := by
  have hr0 : 0 ≤ r := by grind
  have := migration_le r c t h hr0 hc
  grind

/-- After migration, core residents stay positive when they were positive. -/
theorem migration_core_pos (r c t h : Rat) (hc : 0 < c) :
    0 < c + migrationOf r c t h := by
  have := migration_ge r c t h
  have hc0 : 0 ≤ c := by grind
  grind

/-! ## Demographic floors -/

/-- The rural floor (source line 41): after it, rural is at least `.001`, whatever the input. -/
theorem rural1_floor (p : Params) (s : State) (w : Rat) (d : Bool) :
    1/1000 ≤ (year p s w d).rural1 := by
  show 1/1000 ≤ max (1/1000) _
  grind

/-- The core floor (source line 42): after it, core is at least `.0001`, whatever the input. -/
theorem core1_floor (p : Params) (s : State) (w : Rat) (d : Bool) :
    1/10000 ≤ (year p s w d).core1 := by
  show 1/10000 ≤ max (1/10000) _
  grind

/-! ## Step invariant -/

/-- Invariant on states, preserved by one year. Source: lines 10-51 read as a state transition. -/
theorem step_ok (p : Params) (s : State) (w : Rat) (d : Bool)
    (hp : ParamsInRange p) (hs : StateOK p s) (hw : 0 ≤ w) :
    StateOK p (step p s w d) := by
  unfold ParamsInRange at hp
  unfold StateOK at hs
  obtain ⟨he0, he1, hm0, hm1, hr0, hr1, hco, hf0, hf1⟩ := hp
  obtain ⟨hR, hC, hLa, hLa1, hWf, hW1, hT, hS⟩ := hs
  show StateOK p (State.mk (year p s w d).rural (year p s w d).core (year p s w d).land
    (year p s w d).water (year p s w d).temple (year p s w d).store3)
  unfold StateOK
  dsimp only
  obtain ⟨y, hy⟩ : ∃ y, year p s w d = y := ⟨_, rfl⟩
  rw [hy]
  have hR0 : 0 ≤ s.rural := by grind
  have hC0 : 0 ≤ s.core := by grind
  have hL0 : 0 ≤ s.land := by grind
  have hW0 : 0 ≤ s.water := by grind
  have hS0 : 0 ≤ s.store := by grind
  have hT0 : 0 ≤ s.temple := hT
  -- the year's equations (definitional)
  have eq_cl : y.climate = climateOf w d := by subst hy; rfl
  have eq_hy : y.hydraulic = hydraulicOf p s.water := by subst hy; rfl
  have eq_lab : y.labour = labourOf s.rural s.land := by subst hy; rfl
  have eq_H : y.harvest = s.land * (3/2) * coordOf p * y.hydraulic * y.climate * y.labour := by subst hy; rfl
  have eq_C : y.collected = min y.harvest (p.extraction * y.harvest) := by subst hy; rfl
  have eq_ret : y.retained = y.harvest - y.collected := by subst hy; rfl
  have eq_del : y.delivered = y.collected * transportOf p := by subst hy; rfl
  have eq_LF : y.localFood = min s.rural y.retained := by subst hy; rfl
  have eq_UL : y.unusedLocal = max 0 (y.retained - y.localFood) := by subst hy; rfl
  have eq_T0 : y.treasury0 = y.delivered + y.unusedLocal := by subst hy; rfl
  have eq_CF : y.coreFood = coreFoodOf s.core y.treasury0 := by subst hy; rfl
  have eq_T1 : y.treasury1 = y.treasury0 - y.coreFood := by subst hy; rfl
  have eq_SL : y.storageLoss = s.store * (4/100) := by subst hy; rfl
  have eq_S1 : y.store1 = s.store - y.storageLoss := by subst hy; rfl
  have eq_HG : y.householdGap = max 0 (s.rural - y.localFood) + max 0 (s.core - y.coreFood) := by subst hy; rfl
  have eq_Rel : y.release = releaseOf p y.store1 y.householdGap := by subst hy; rfl
  have eq_S2 : y.store2 = y.store1 - y.release := by subst hy; rfl
  have eq_gap : y.gap = y.householdGap - y.release := by subst hy; rfl
  have eq_Ob : y.obligation = obligationOf p s.temple := by subst hy; rfl
  have eq_Rit : y.ritual = min y.treasury1 y.obligation := by subst hy; rfl
  have eq_T2 : y.treasury2 = y.treasury1 - y.ritual := by subst hy; rfl
  have eq_MN : y.maintenanceNeed = s.land * (35/1000) := by subst hy; rfl
  have eq_Up : y.upkeep = min (y.treasury2 * p.maintenance) y.maintenanceNeed := by subst hy; rfl
  have eq_T3 : y.treasury3 = y.treasury2 - y.upkeep := by subst hy; rfl
  have eq_Dep : y.deposit = min (y.treasury3 * (35/100)) (max 0 (s.rural + s.core - y.store2)) := by subst hy; rfl
  have eq_S3 : y.store3 = y.store2 + y.deposit := by subst hy; rfl
  have eq_T4 : y.treasury4 = y.treasury3 - y.deposit := by subst hy; rfl
  have eq_Rec : y.reclamation = min (y.treasury4 * (55/100)) (max 0 (1 - s.land) * (15/100)) := by subst hy; rfl
  have eq_Cons : y.construction = y.treasury4 - y.reclamation := by subst hy; rfl
  have eq_Temple : y.temple = s.temple + y.construction := by subst hy; rfl
  have eq_Land : y.land = min 1 (s.land + y.reclamation * (6/10)) := by subst hy; rfl
  have eq_Water : y.water = waterNextOf p s.water y.maintained := by subst hy; rfl
  have eq_Mig : y.migration = migrationOf y.rural1 y.core1 y.temple y.hunger := by subst hy; rfl
  have eq_R1 : y.rural1 = max (1/1000) y.rawRural := by subst hy; rfl
  have eq_C1 : y.core1 = max (1/10000) y.rawCore := by subst hy; rfl
  have eq_R : y.rural = y.rural1 - y.migration := by subst hy; rfl
  have eq_Co : y.core = y.core1 + y.migration := by subst hy; rfl
  -- nonnegativity chain
  have f_cl : 0 ≤ y.climate := by rw [eq_cl]; exact climateOf_nonneg w d hw
  have f_hy : 0 ≤ y.hydraulic := by rw [eq_hy]; exact hydraulicOf_nonneg p s.water hW0
  have f_lab : 0 ≤ y.labour := by rw [eq_lab]; exact labourOf_nonneg s.rural s.land hR0
  have hL32 : 0 ≤ s.land * (3/2) := Rat.mul_nonneg hL0 (by grind)
  have f_H : 0 ≤ y.harvest := by
    rw [eq_H]
    exact Rat.mul_nonneg (Rat.mul_nonneg (Rat.mul_nonneg (Rat.mul_nonneg hL32
      (coordOf_nonneg p hco)) f_hy) f_cl) f_lab
  have hEH := Rat.mul_nonneg he0 f_H
  have f_C : 0 ≤ y.collected := by rw [eq_C]; grind
  have f_CH : y.collected ≤ y.harvest := by rw [eq_C]; grind
  have f_ret : 0 ≤ y.retained := by rw [eq_ret]; grind
  have f_del : 0 ≤ y.delivered := by
    rw [eq_del]; exact Rat.mul_nonneg f_C (transportOf_bounds p).1
  have f_delC : y.delivered ≤ y.collected := by
    rw [eq_del]
    have := Rat.mul_le_mul_of_nonneg_left (transportOf_bounds p).2 f_C
    rw [Rat.mul_one] at this
    exact this
  have f_LF : 0 ≤ y.localFood := by rw [eq_LF]; grind
  have f_LFr : y.localFood ≤ y.retained := by rw [eq_LF]; grind
  have f_UL : 0 ≤ y.unusedLocal := by rw [eq_UL]; grind
  have f_T0 : 0 ≤ y.treasury0 := by rw [eq_T0]; grind
  have f_CF : 0 ≤ y.coreFood ∧ y.coreFood ≤ y.treasury0 := by
    rw [eq_CF]; unfold coreFoodOf; constructor <;> grind
  have f_T1 : 0 ≤ y.treasury1 := by rw [eq_T1]; grind
  have f_S1 : 0 ≤ y.store1 := by rw [eq_S1, eq_SL]; grind
  have f_HG : 0 ≤ y.householdGap := by rw [eq_HG]; grind
  have f_Rel := releaseOf_bounds p y.store1 y.householdGap f_S1 f_HG hr0 hr1
  have f_S2 : 0 ≤ y.store2 := by rw [eq_S2]; grind
  have f_Ob : 0 ≤ y.obligation := by rw [eq_Ob]; unfold obligationOf; split <;> grind
  have f_Rit : 0 ≤ y.ritual ∧ y.ritual ≤ y.treasury1 := by rw [eq_Rit]; constructor <;> grind
  have f_T2 : 0 ≤ y.treasury2 := by rw [eq_T2]; grind
  have f_MN : 0 ≤ y.maintenanceNeed := by rw [eq_MN]; grind
  have f_Up : 0 ≤ y.upkeep ∧ y.upkeep ≤ y.treasury2 := by
    have hTm := Rat.mul_nonneg f_T2 hm0
    have hTm2 := Rat.mul_le_mul_of_nonneg_left hm1 f_T2
    rw [Rat.mul_one] at hTm2
    rw [eq_Up]; constructor <;> grind
  have f_T3 : 0 ≤ y.treasury3 := by rw [eq_T3]; grind
  have f_Dep : 0 ≤ y.deposit ∧ y.deposit ≤ y.treasury3 := by
    rw [eq_Dep]; constructor <;> grind
  have f_S3 : 0 ≤ y.store3 := by rw [eq_S3]; grind
  have f_T4 : 0 ≤ y.treasury4 := by rw [eq_T4]; grind
  have f_Rec : 0 ≤ y.reclamation ∧ y.reclamation ≤ y.treasury4 := by
    rw [eq_Rec]; constructor <;> grind
  have f_Cons : 0 ≤ y.construction := by rw [eq_Cons]; grind
  have f_Temple : 0 ≤ y.temple := by rw [eq_Temple]; grind
  have f_Land : 0 < y.land ∧ y.land ≤ 1 := by rw [eq_Land]; constructor <;> grind
  have f_Water : p.waterFloor ≤ y.water ∧ y.water ≤ 1 := by
    rw [eq_Water]; exact waterNextOf_bounds p s.water y.maintained hWf hW1
  have f_R1 : 1/1000 ≤ y.rural1 := by rw [← hy]; exact rural1_floor p s w d
  have f_C1 : 1/10000 ≤ y.core1 := by rw [← hy]; exact core1_floor p s w d
  have f_Mig1 : y.migration ≤ y.rural1 * (3/100) := by
    rw [eq_Mig]; exact migration_le _ _ _ _ (by grind) (by grind)
  have f_Mig2 : -(y.core1 * (2/10)) ≤ y.migration := by
    rw [eq_Mig]; exact migration_ge _ _ _ _
  have f_Rpos : 0 < y.rural := by
    rw [eq_R, eq_Mig]; exact migration_rural_pos _ _ _ _ (by grind) (by grind)
  have f_Cpos : 0 < y.core := by
    rw [eq_Co, eq_Mig]; exact migration_core_pos _ _ _ _ (by grind)
  exact ⟨f_Rpos, f_Cpos, f_Land.1, f_Land.2, f_Water.1, f_Water.2, f_Temple, f_S3⟩

/-- Iterating the step preserves the invariant over any finite list of weather inputs. -/
theorem runYears_ok (p : Params) (hp : ParamsInRange p) (draws : List (Rat × Bool)) :
    ∀ s : State, StateOK p s → (∀ x ∈ draws, 0 ≤ x.1) → StateOK p (runYears p s draws) := by
  induction draws with
  | nil => intro s hs _; exact hs
  | cons x rest ih =>
    intro s hs hw
    obtain ⟨w, d⟩ := x
    exact ih (step p s w d) (step_ok p s w d hp hs (hw (w, d) (by simp)))
      (fun y hy => hw y (by simp [hy]))

/-- The population stays positive through any number of years. -/
theorem runYears_pop_pos (p : Params) (hp : ParamsInRange p) (s : State) (draws : List (Rat × Bool))
    (hs : StateOK p s) (hw : ∀ x ∈ draws, 0 ≤ x.1) :
    0 < (runYears p s draws).rural + (runYears p s draws).core := by
  have := runYears_ok p hp draws s hs hw
  unfold StateOK at this
  grind

/-- The initial state satisfies the invariant when the water floor is at most `1/2`. -/
theorem initState_ok (p : Params) (hf : p.waterFloor ≤ 1/2) : StateOK p initState := by
  unfold StateOK initState
  dsimp only
  grind


/-! ## Hunger, growth and the demographic floors -/

/-- The household gap after release is nonnegative (release is at most the gap). Source line 26. -/
theorem gap_nonneg (p : Params) (s : State) (w : Rat) (d : Bool)
    (hp : ParamsInRange p) (hs : StateOK p s) (hw : 0 ≤ w) : 0 ≤ (year p s w d).gap := by
  unfold ParamsInRange at hp
  unfold StateOK at hs
  obtain ⟨he0, he1, hm0, hm1, hr0, hr1, hco, hf0, hf1⟩ := hp
  obtain ⟨hR, hC, hLa, hLa1, hWf, hW1, hT, hS⟩ := hs
  have hS0 : 0 ≤ s.store := by grind
  have e1 : (year p s w d).store1 = s.store - s.store * (4/100) := rfl
  have hs1 : 0 ≤ (year p s w d).store1 := by rw [e1]; grind
  have hLF : 0 ≤ (year p s w d).localFood := by
    have e : (year p s w d).localFood = min s.rural (year p s w d).retained := rfl
    have hH : 0 ≤ (year p s w d).retained := by
      have e2 : (year p s w d).retained = (year p s w d).harvest - (year p s w d).collected := rfl
      have hC' : 0 ≤ (year p s w d).collected := by
        have eC : (year p s w d).collected = min (year p s w d).harvest (p.extraction * (year p s w d).harvest) := rfl
        have hH0 : 0 ≤ (year p s w d).harvest := by
          have eH : (year p s w d).harvest = s.land * (3/2) * coordOf p * hydraulicOf p s.water * climateOf w d * labourOf s.rural s.land := rfl
          rw [eH]
          have hL32 : 0 ≤ s.land * (3/2) := Rat.mul_nonneg (by grind) (by grind)
          have b1 := Rat.mul_nonneg hL32 (coordOf_nonneg p hco)
          have b2 := Rat.mul_nonneg b1 (hydraulicOf_nonneg p s.water (by grind))
          have b3 := Rat.mul_nonneg b2 (climateOf_nonneg w d hw)
          exact Rat.mul_nonneg b3 (labourOf_nonneg s.rural s.land (by grind))
        rw [eC]
        have := Rat.mul_nonneg he0 hH0
        grind
      have hCH : (year p s w d).collected ≤ (year p s w d).harvest := by
        have eC : (year p s w d).collected = min (year p s w d).harvest (p.extraction * (year p s w d).harvest) := rfl
        rw [eC]; grind
      grind
    grind
  have hHG : 0 ≤ (year p s w d).householdGap := by
    have e : (year p s w d).householdGap = max 0 (s.rural - (year p s w d).localFood) + max 0 (s.core - (year p s w d).coreFood) := rfl
    rw [e]; grind
  have hr := releaseOf_bounds p (year p s w d).store1 (year p s w d).householdGap hs1 hHG hr0 hr1
  have eg : (year p s w d).gap = (year p s w d).householdGap - releaseOf p (year p s w d).store1 (year p s w d).householdGap := rfl
  rw [eg]
  grind

/-- Hunger is nonnegative. Source line 38. -/
theorem hunger_nonneg (p : Params) (s : State) (w : Rat) (d : Bool)
    (hp : ParamsInRange p) (hs : StateOK p s) (hw : 0 ≤ w) : 0 ≤ (year p s w d).hunger := by
  have hg := gap_nonneg p s w d hp hs hw
  have hs' := hs
  unfold StateOK at hs'
  obtain ⟨hR, hC, -, -, -, -, -, -⟩ := hs'
  have e : (year p s w d).hunger = hungerOf (year p s w d).gap (s.rural + s.core) := rfl
  rw [e]
  unfold hungerOf
  by_cases h0 : s.rural + s.core = 0
  · simp only [h0, ite_true]; grind
  · simp only [h0, ite_false]
    exact tdiv_nonneg _ _ hg (by grind)

/-- The raw rural value before the floor is at most `1.012` times the rural value. Source lines
40-41: growth is at most `.012` and hunger is nonnegative. -/
theorem rawRural_le (p : Params) (s : State) (w : Rat) (d : Bool)
    (hp : ParamsInRange p) (hs : StateOK p s) (hw : 0 ≤ w) :
    (year p s w d).rawRural ≤ s.rural * (1012/1000) := by
  have hh := hunger_nonneg p s w d hp hs hw
  have hs' := hs
  unfold StateOK at hs'
  obtain ⟨hR, -, -, -, -, -, -, -⟩ := hs'
  have hg : (year p s w d).growth ≤ 12/1000 := by
    have e : (year p s w d).growth = 12/1000 * clamp (year p s w d).foodMargin (-1) 1 := rfl
    have h1 := clamp_upper (year p s w d).foodMargin (-1) 1 (by grind)
    have h2 := Rat.mul_le_mul_of_nonneg_left h1 (by grind : (0:Rat) ≤ 12/1000)
    rw [Rat.mul_one] at h2
    rw [e]; exact h2
  have e : (year p s w d).rawRural = s.rural * (1 + (year p s w d).growth - 8/100 * (year p s w d).hunger) := rfl
  rw [e]
  exact Rat.mul_le_mul_of_nonneg_left (by grind) (by grind)

/-! ## A concrete step where the rural floor creates people -/

/-- Example parameters, inside the stated ranges. -/
def pEx : Params :=
  { extraction := 1/5, maintenance := 9/20, relief := 1, coordination := 1, waterFloor := 0,
    knockout := .noKnockout }

/-- Example state with rural `1/10000`, below the rural floor, in a valid (not necessarily
reachable) configuration. -/
def sEx : State :=
  { rural := 1/10000, core := 1/100, land := 1/5, water := 1/2, temple := 0, store := 3/100 }

theorem exEx_ok : ParamsInRange pEx ∧ StateOK pEx sEx := by
  constructor
  · dsimp only [ParamsInRange, pEx]; grind
  · dsimp only [StateOK, pEx, sEx]; grind

/-- The demographic floors create people in one step: for this valid state the raw rural and core
values sum to less than the floored values. The rural floor binds (raw rural is below `.001`), so
the floored population exceeds the unfloored one. -/
theorem floor_creates_people :
    (year pEx sEx 1 false).rawRural + (year pEx sEx 1 false).rawCore <
      (year pEx sEx 1 false).rural1 + (year pEx sEx 1 false).core1 := by
  have hr := rawRural_le pEx sEx 1 false exEx_ok.1 exEx_ok.2 (by grind)
  have hR : sEx.rural = 1/10000 := rfl
  have h1 := rural1_floor pEx sEx 1 false
  have h2 : (year pEx sEx 1 false).rawCore ≤ (year pEx sEx 1 false).core1 := by
    have e : (year pEx sEx 1 false).core1 = max (1/10000) (year pEx sEx 1 false).rawCore := rfl
    rw [e]; grind
  rw [hR] at hr
  grind

/-! ## Knockouts and monotonicity -/

/-- Coordination knockout: the step does not depend on the coordination parameter. -/
theorem coord_knockout_indep (p : Params) (c : Rat) (hk : p.knockout = .coordination)
    (s : State) (w : Rat) (d : Bool) :
    step { p with coordination := c } s w d = step p s w d := by
  have h : coordOf { p with coordination := c } = coordOf p := by
    have h1 : coordOf p = 1 := by unfold coordOf; simp only [hk, ite_true]
    have h2 : coordOf { p with coordination := c } = 1 := by unfold coordOf; simp only [hk, ite_true]
    rw [h1, h2]
  unfold step year
  rw [h]
  all_goals rfl

/-- Water knockout: the next water value equals the current one. -/
theorem water_knockout_freezes (p : Params) (hk : p.knockout = .water)
    (s : State) (w : Rat) (d : Bool) :
    (step p s w d).water = s.water := by
  have e : (year p s w d).water = waterNextOf p s.water (year p s w d).maintained := rfl
  have h : (year p s w d).water = s.water := by
    rw [e]; unfold waterNextOf; simp [hk]
  exact h

/-- Harvest is monotone in the weather draw (the climate factor is `weather` times a nonnegative
constant). -/
theorem harvest_mono_weather (p : Params) (s : State) (d : Bool) (w₁ w₂ : Rat)
    (hp : ParamsInRange p) (hs : StateOK p s) (h : w₁ ≤ w₂) :
    (year p s w₁ d).harvest ≤ (year p s w₂ d).harvest := by
  unfold ParamsInRange at hp
  unfold StateOK at hs
  obtain ⟨he0, he1, hm0, hm1, hr0, hr1, hco, hf0, hf1⟩ := hp
  obtain ⟨hR, hC, hLa, hLa1, hWf, hW1, hT, hS⟩ := hs
  have hX : 0 ≤ s.land * (3/2) * coordOf p * hydraulicOf p s.water :=
    Rat.mul_nonneg (Rat.mul_nonneg (Rat.mul_nonneg (by grind) (by grind))
      (coordOf_nonneg p hco)) (hydraulicOf_nonneg p s.water (by grind))
  have hL : 0 ≤ labourOf s.rural s.land := labourOf_nonneg s.rural s.land (by grind)
  have hc : climateOf w₁ d ≤ climateOf w₂ d := by
    unfold climateOf; split <;> grind
  have e1 : (year p s w₁ d).harvest = s.land * (3/2) * coordOf p * hydraulicOf p s.water * climateOf w₁ d * labourOf s.rural s.land := rfl
  have e2 : (year p s w₂ d).harvest = s.land * (3/2) * coordOf p * hydraulicOf p s.water * climateOf w₂ d * labourOf s.rural s.land := rfl
  rw [e1, e2]
  exact mul3_mono _ _ _ _ hX hL hc

/-- A drought year (factor `.62`) has no larger harvest than the same weather without drought. -/
theorem drought_lowers_harvest (p : Params) (s : State) (w : Rat)
    (hp : ParamsInRange p) (hs : StateOK p s) (hw : 0 ≤ w) :
    (year p s w true).harvest ≤ (year p s w false).harvest := by
  unfold ParamsInRange at hp
  unfold StateOK at hs
  obtain ⟨he0, he1, hm0, hm1, hr0, hr1, hco, hf0, hf1⟩ := hp
  obtain ⟨hR, hC, hLa, hLa1, hWf, hW1, hT, hS⟩ := hs
  have hX : 0 ≤ s.land * (3/2) * coordOf p * hydraulicOf p s.water :=
    Rat.mul_nonneg (Rat.mul_nonneg (Rat.mul_nonneg (by grind) (by grind))
      (coordOf_nonneg p hco)) (hydraulicOf_nonneg p s.water (by grind))
  have hL : 0 ≤ labourOf s.rural s.land := labourOf_nonneg s.rural s.land (by grind)
  have hc : climateOf w true ≤ climateOf w false := by
    show w * (62/100) ≤ w * 1
    grind
  have e1 : (year p s w true).harvest = s.land * (3/2) * coordOf p * hydraulicOf p s.water * climateOf w true * labourOf s.rural s.land := rfl
  have e2 : (year p s w false).harvest = s.land * (3/2) * coordOf p * hydraulicOf p s.water * climateOf w false * labourOf s.rural s.land := rfl
  rw [e1, e2]
  exact mul3_mono _ _ _ _ hX hL hc

/-- One step leaves rural at least `.97` of the rural floor, whatever the inputs. -/
theorem rural_after_step (p : Params) (s : State) (w : Rat) (d : Bool) :
    97/100 * (1/1000) ≤ (year p s w d).rural := by
  have h1 := rural1_floor p s w d
  have h2 := core1_floor p s w d
  have hm := migration_le (year p s w d).rural1 (year p s w d).core1 (year p s w d).temple
    (year p s w d).hunger (by grind) (by grind)
  have e : (year p s w d).rural = (year p s w d).rural1 - (year p s w d).migration := rfl
  have e2 : (year p s w d).migration = migrationOf (year p s w d).rural1 (year p s w d).core1
    (year p s w d).temple (year p s w d).hunger := rfl
  rw [e]
  grind

end Angkor.Petri
