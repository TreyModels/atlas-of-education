import Angkor.Basic

/-!
# Angkor Mandala engine: `initialize` and `step`

Source: `public/reference/angkor/model.js` (byte-identical to `src/models/angkor-model.js`,
SHA-256 a4ff2079c56dcef2f4c7e286967595c3fe867608cac8f8232c9524300485fb05). Line numbers refer to it.
Formalized: `initialize` (lines 25-39) and `step` (lines 41-132) with helpers.
Omitted: `simulate`, `mc`, `quantile`, `summarize`, `inverse`, `regress`, `sweep`, the output record
`s.latest` (line 130) and `migration` (line 116), which feed no state variable.
Arithmetic is exact `Rat`; decimal literals are exact. Random draws, `sqrt`, `sin`, `log1p` are inputs.
-/

namespace Angkor.Mandala

open Angkor

/-- `Math.floor` on a rational. -/
def floorR (q : Rat) : Rat := ((q.num / (q.den : Int) : Int) : Rat)

/-- `Math.round` (halves upward): `floor(q + 1/2)`. -/
def roundR (q : Rat) : Rat := floorR (q + 0.5)

/-- Exact sum, left to right. -/
def sumL : List Rat → Rat
  | [] => 0
  | x :: xs => x + sumL xs

/-- Index-aware map: `f i c` with the cell index `i` (the JS loops use the cell index). -/
def mapIdxFrom {α β : Type} (f : Nat → α → β) : Nat → List α → List β
  | _, [] => []
  | i, a :: as => f i a :: mapIdxFrom f (i + 1) as

/-- Parameters read by `initialize` or `step`; defaults at `defaultParams` (line 12). -/
structure Params where
  population : Rat
  riceKm2 : Rat
  yieldT : Rat
  lossPct : Rat
  riceKg : Rat
  importsT : Rat
  localShare : Rat
  estateShare : Rat
  hydraulicDependency : Rat
  maintenanceIntensity : Rat
  climateVolatility : Rat
  growthPct : Rat
  corveeDays : Rat
  bondedBirthPct : Rat
  raidIntensity : Rat
  diplomacy : Rat
  warExpense : Rat
  buildShare : Rat
  monumentSkill : Rat
  tradeIntegration : Rat
  templeAutonomy : Rat
  defenseSpend : Rat
  sackShock : Rat
  lateDrought : Rat
  marketElasticity : Rat
  conquestDamage : Rat
  start : Int
  bonded : Rat

/-- `DEFAULTS` of the source (line 12). -/
def defaultParams : Params where
  population := 250000
  riceKm2 := 1100
  yieldT := 1.6
  lossPct := 16
  riceKg := 200
  importsT := 6000
  localShare := 0.62
  estateShare := 0.25
  hydraulicDependency := 0.45
  maintenanceIntensity := 0.38
  climateVolatility := 0.11
  growthPct := 0.65
  corveeDays := 24
  bondedBirthPct := 1.0
  raidIntensity := 0.45
  diplomacy := 0.48
  warExpense := 0.28
  buildShare := 0.34
  monumentSkill := 0.65
  tradeIntegration := 0.48
  templeAutonomy := 0.52
  defenseSpend := 0.15
  sackShock := 0
  lateDrought := 0.18
  marketElasticity := 0.35
  conquestDamage := 0.4
  start := 850
  bonded := 10000

/-- A grid cell. `loc` is the source field `local` (`local` is a Lean keyword). -/
structure Cell where
  pop : Rat
  fields : Rat
  infra : Rat
  loyalty : Rat
  loc : Rat
  access : Rat
  fertility : Rat

/-- Simulation state (line 137 and the fields `step` writes). `courtPower` and `rivalPower`
are set in line 129; the source leaves them undefined before the first step, here 0. -/
structure State where
  cells : List Cell
  courtLegitimacy : Rat
  shrine : Rat
  bonded : Rat
  monument : Rat
  courtPower : Rat
  rivalPower : Rat
  wars : Nat
  sacks : Nat
  victories : Nat
  defeats : Nat
  shockYears : List Int

/-- Draws for the war branch (lines 92-103); each is one `r()` call. -/
structure WarDraws where
  war : Rat
  loss : Rat
  cas : Rat
  legDrop : Rat
  defect : Rat
  sack : Rat
  capt : Rat
  legGain : Rat

/-- Draws for one year. `wNormal i` is line 48's per-cell normal, `lNormal i` line 123's. -/
structure Draws where
  normShock : Rat
  normImports : Rat
  normRival : Rat
  normGrowth : Rat
  wNormal : Nat → Rat
  lNormal : Nat → Rat
  war : WarDraws

/-! ## Initialization (lines 25-39) -/

/-- Grid index `k = 14*y + x` (lines 27-28). -/
def gridK : List Nat := List.range 140

/-- Access (line 29). `sqrt` is `Math.sqrt`; `r` is the draw for that cell. -/
def accessOf (sqrt : Rat → Rat) (k : Nat) (r : Rat) : Rat :=
  let x : Rat := ((k % 14 : Nat) : Rat)
  let y : Rat := ((k / 14 : Nat) : Rat)
  let xd := (x - 6.3) / 7
  let yd := (y - 5.9) / 5.8
  clamp (1.14 - 0.7 * sqrt (xd * xd + yd * yd) + 0.17 * (r - 0.5)) 0.15 1.35

/-- Fertility (line 31). Upland rows `y < 2`, flood rows `y > 7`. -/
def fertilityOf (k : Nat) (r : Rat) : Rat :=
  clamp (0.72 + 0.4 * r + 0.12 * (if 7 < k / 14 then (1 : Rat) else 0)
      - 0.17 * (if k / 14 < 2 then (1 : Rat) else 0)) 0.48 1.35

/-- Weight (line 32). Draw indices: cell `k` uses `ur (4k)` access, `ur (4k+1)` fertility,
`ur (4k+2)` infra, `ur (4k+3)` local; loyalty uses `ur (560 + k)`. -/
def initWeight (sqrt : Rat → Rat) (ur : Nat → Rat) (k : Nat) : Rat :=
  max 0.04 (accessOf sqrt k (ur (4 * k)) * fertilityOf k (ur (4 * k + 1))
    * (if k / 14 < 2 then (0.55 : Rat) else 1) * (if 7 < k / 14 then (0.7 : Rat) else 1))

/-- Arable (line 33). -/
def initArable (ur : Nat → Rat) (k : Nat) : Rat :=
  clamp (fertilityOf k (ur (4 * k + 1)) * (if 7 < k / 14 then (0.72 : Rat) else 1)
    * (if k / 14 < 2 then (0.5 : Rat) else 1)) 0.12 1.55

/-- Per-cell initialization (lines 25-39). -/
def initCells (p : Params) (sqrt : Rat → Rat) (ur : Nat → Rat) : List Cell :=
  let wsum := sumL (gridK.map (initWeight sqrt ur))
  let asum := sumL (gridK.map (initArable ur))
  gridK.map fun k =>
    { pop := p.population * initWeight sqrt ur k / wsum
      fields := p.riceKm2 * initArable ur k / asum
      infra := clamp (0.32 + 0.45 * accessOf sqrt k (ur (4 * k)) + 0.1 * ur (4 * k + 2)) 0.2 0.9
      loyalty := clamp (0.36 + 0.30 * accessOf sqrt k (ur (4 * k)) + 0.18 * ur (560 + k)) 0.05 0.99
      loc := clamp (p.localShare + 0.18 * (ur (4 * k + 3) - 0.5)) 0.03 0.98
      access := accessOf sqrt k (ur (4 * k))
      fertility := fertilityOf k (ur (4 * k + 1)) }

/-- Initial state (line 137). -/
def initialState (p : Params) (cells : List Cell) : State :=
  { cells := cells, courtLegitimacy := 0.72, shrine := 0.49, bonded := p.bonded, monument := 0,
    courtPower := 0, rivalPower := 0, wars := 0, sacks := 0, victories := 0, defeats := 0,
    shockYears := [] }

/-! ## Year step (lines 41-131) -/

/-- Seasonal ramp (line 44). -/
def seasonal (year : Int) : Rat :=
  if 1300 ≤ year then max 0 ((((year : Int) : Rat) - 1300) / 125) else 0

/-- Regional shock (line 45). -/
def shockOf (p : Params) (year : Int) (normShock : Rat) : Rat :=
  clamp (normShock * p.climateVolatility
    + (if 1300 ≤ year then -(p.lateDrought * seasonal year * 0.42) else 0)) (-0.72) 0.55

/-- Field output of one cell (lines 48-52). `wn` is the cell's weather normal. -/
def tonsCell (p : Params) (shock wn : Rat) (c : Cell) : Rat :=
  let rw := clamp (1 + shock + wn * p.climateVolatility * 0.35) 0.16 1.55
  let he := clamp (1 - p.hydraulicDependency * (1 - c.infra) * 0.42) 0.46 1.12
  let ae := 0.93 + 0.08 * c.loc
  let stress := clamp ((p.corveeDays - 20) / 250) 0 0.16
  c.fields * 100 * p.yieldT * c.fertility * rw * he * ae * (1 - stress * p.estateShare)

/-- Maintenance need of one cell (line 54). -/
def maintNeedCell (p : Params) (c : Cell) : Rat :=
  c.fields * 100 * (0.9 + 4 * p.maintenanceIntensity * p.hydraulicDependency)
    * (1.18 - c.loc * 0.35)

/-- Imports (line 58). -/
def importsOf (p : Params) (normImports : Rat) : Rat :=
  p.importsT * (0.4 + 0.6 * p.tradeIntegration) * clamp (0.85 + 0.1 * normImports) 0.3 1.3

/-- Food ratio (line 61). -/
def foodRatioOf (usable imports demand : Rat) : Rat :=
  clamp ((usable + imports) / max 1 demand) 0 2.2

/-- Field reserve (line 66). -/
def fieldReserveOf (sh : Rat) : Rat := clamp (0.33 + 0.17 * (1 - sh)) 0.30 0.61

/-- Corvee day pool (line 67). `adults` is `prePop * 0.45`. -/
def corveePoolOf (p : Params) (adults bondedC sh : Rat) : Rat :=
  max 0 (adults - bondedC) * p.corveeDays
    * clamp ((1 - fieldReserveOf sh) * (1 + 0.3 * p.localShare)) 0.15 0.85

/-- Bonded day pool (line 68). -/
def bondedPoolOf (bondedC sh : Rat) : Rat :=
  bondedC * 175 * clamp ((1 - fieldReserveOf sh) * 1.3) 0.20 0.85

/-- Maintenance labour (line 70). -/
def maintLaborOf (p : Params) (need laborPool : Rat) : Rat :=
  min need (laborPool * 0.36 + need * p.localShare * 0.17)

/-- Allocatable surplus (line 76). -/
def allocatableOf (surplus : Rat) (p : Params) : Rat :=
  surplus * clamp (0.18 + 0.51 * p.estateShare + 0.17 * p.tradeIntegration) 0.10 0.73

/-- Army budget (line 77). -/
def armyBudgetOf (a : Rat) (p : Params) : Rat := a * p.warExpense

/-- Monument budget (line 78). -/
def monumentBudgetOf (a : Rat) (p : Params) : Rat := a * p.buildShare

/-- Maintain budget (line 79). -/
def maintainBudgetOf (a : Rat) (p : Params) : Rat := a * max 0 (1 - p.buildShare - p.warExpense)

/-- Soldiers (line 80). -/
def soldiersOf (prePop armyBudget : Rat) : Rat :=
  min (prePop * 0.035) (floorR (armyBudget / 0.12))

/-- Build person-days (line 81). -/
def buildDaysOf (laborPool maintLabor monumentBudget : Rat) : Rat :=
  max 0 (min (laborPool - maintLabor) (monumentBudget * 1000 / 0.45))

/-- Contest (line 90). -/
def contestOf (rivalPower corePower : Rat) : Rat :=
  clamp ((rivalPower - corePower) / 30) (-0.6) 0.6

/-- War probability (line 91). -/
def warProbOf (p : Params) (contest : Rat) : Rat :=
  clamp ((0.016 + 0.055 * p.raidIntensity + 0.045 * contest) * (1 - 0.38 * p.diplomacy)) 0.002 0.20

/-- Chance of loss (line 94). -/
def chanceOf (p : Params) (contest loyFrac : Rat) : Rat :=
  clamp (0.29 + 0.22 * contest + 0.14 * (1 - loyFrac) - 0.15 * p.defenseSpend) 0.06 0.72

/-- Infrastructure update (lines 72-75). -/
def infraUpdate (p : Params) (sh maintSat : Rat) (c : Cell) : Cell :=
  let floodDamage := clamp (-sh * 0.038 * (0.5 + p.hydraulicDependency)) 0 0.075
  { c with infra := clamp (c.infra + (0.006 + 0.015 * p.maintenanceIntensity) * maintSat
      - (0.005 + 0.016 * p.hydraulicDependency * p.maintenanceIntensity)
      - floodDamage + 0.006 * c.loc) 0.03 1 }

/-- War outcome record (lines 88-106). -/
structure WarOut where
  st : State
  casualties : Rat
  defection : Rat
  captives : Rat

/-- War branch (lines 88-106), gated by `year > start + 12` (line 89). -/
def warPhase (p : Params) (year : Int) (prePop loyFrac corePower rivalPower : Rat)
    (d : WarDraws) (s : State) : WarOut :=
  let contest := contestOf rivalPower corePower
  if year > p.start + 12 then
    if d.war < warProbOf p contest then
      let s1 := { s with wars := s.wars + 1 }
      if d.loss < chanceOf p contest loyFrac then
        let casualties := prePop * (0.0006 + 0.002 * d.cas) * (0.6 + 0.7 * p.conquestDamage)
        let leg1 := clamp (s1.courtLegitimacy - (0.055 + 0.075 * d.legDrop)) 0.05 1
        let s2 := { s1 with defeats := s1.defeats + 1, courtLegitimacy := leg1 }
        let defection := 0.02 + 0.04 * d.defect
        if d.sack < 0.25 + 0.35 * p.conquestDamage then
          let s3 := { s2 with sacks := s2.sacks + 1, shockYears := s2.shockYears ++ [year] }
          { st := { s3 with courtLegitimacy := s3.courtLegitimacy * 0.83 },
            casualties := casualties, defection := defection, captives := 0 }
        else
          { st := s2, casualties := casualties, defection := defection, captives := 0 }
      else
        let s3 := { s1 with victories := s1.victories + 1 }
        let leg2 := clamp (s3.courtLegitimacy + 0.012 + 0.017 * d.legGain) 0.05 1
        { st := { s3 with courtLegitimacy := leg2 }, casualties := 0, defection := 0,
          captives := roundR ((300 + 850 * d.capt) * p.raidIntensity) }
    else { st := s, casualties := 0, defection := 0, captives := 0 }
  else { st := s, casualties := 0, defection := 0, captives := 0 }

/-- 1177 infra effect on cells with access above 0.74 (line 111). -/
def infra1177 (damage : Rat) (c : Cell) : Cell :=
  if 0.74 < c.access then { c with infra := clamp (c.infra - 0.12 * damage) 0.03 1 } else c

/-- Shock output record. -/
structure ShockOut where
  st : State
  casualties : Rat
  defection : Rat

/-- 1177 dated shock (lines 107-112). -/
def shockPhase (p : Params) (year : Int) (prePop casualties dfn : Rat) (s : State) : ShockOut :=
  if year = 1177 ∧ 0 < p.sackShock then
    let s1 := { s with courtLegitimacy := clamp (s.courtLegitimacy - 0.27 * p.sackShock) 0.05 1,
                       sacks := s.sacks + 1, shockYears := s.shockYears ++ [year] }
    { st := { s1 with cells := s.cells.map (infra1177 p.sackShock) },
      casualties := casualties + prePop * 0.013 * p.sackShock,
      defection := dfn + 0.09 * p.sackShock }
  else { st := s, casualties := casualties, defection := dfn }

/-- Population factor (line 117). -/
def factorOf (targetGrowth emigrRate casualties prePop : Rat) : Rat :=
  clamp (1 + targetGrowth - emigrRate - casualties / max 1 prePop) 0.87 1.045

/-- Per-cell pop and loyalty update (lines 120-124). -/
def popLoyaltyUpdate (p : Params) (factor leg dfn ln : Rat) (c : Cell) : Cell :=
  let change := clamp ((c.access - 0.62) * p.marketElasticity * 0.001 + (c.loc - 0.5) * 0.001)
    (-0.002) 0.002
  { c with pop := max 1 (c.pop * factor * (1 + change)),
           loyalty := clamp (c.loyalty + 0.012 * (leg - 0.5) + 0.003 * p.diplomacy
             - 0.018 * dfn + ln * 0.009) 0.03 0.98 }

/-- One year (lines 41-131). `sinOf year` stands for `Math.sin((year-842)/67)` and `log1p` for
`Math.log1p`; both are inputs. -/
def step (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat) (year : Int) (d : Draws) (s : State) :
    State :=
  let prePop := sumL (s.cells.map (·.pop))
  let sh := shockOf p year d.normShock
  let fieldProduction := sumL (mapIdxFrom (fun i c => max 0 (tonsCell p sh (d.wNormal i) c)) 0 s.cells)
  let maintenanceNeed := sumL (s.cells.map (maintNeedCell p))
  let alignment := sumL (s.cells.map (fun c => c.loyalty * c.pop))
  let usable := fieldProduction * (1 - p.lossPct / 100)
  let imports := importsOf p d.normImports
  let demand := prePop * p.riceKg / 1000
  let grainBalance := usable + imports - demand
  let foodRatio := foodRatioOf usable imports demand
  let surplus := max 0 grainBalance
  let adults := prePop * 0.45
  let bondedC := clamp s.bonded 0 (adults * 0.5)
  let laborPool := corveePoolOf p adults bondedC sh + bondedPoolOf bondedC sh
  let maintLabor := maintLaborOf p maintenanceNeed laborPool
  let maintSat := clamp (maintLabor / max 1 maintenanceNeed) 0 1.4
  let cellsI := s.cells.map (infraUpdate p sh maintSat)
  let allocatable := allocatableOf surplus p
  let monumentBudget := monumentBudgetOf allocatable p
  let soldiers := soldiersOf prePop (armyBudgetOf allocatable p)
  let buildPersonDays := buildDaysOf laborPool maintLabor monumentBudget
  let ornamentalDays := buildPersonDays * p.monumentSkill * (0.38 + 0.4 * s.courtLegitimacy)
  let corePower := (soldiers / 2500) * (0.45 + 0.85 * s.courtLegitimacy)
    + s.courtLegitimacy * 7 + clamp (surplus / 16000) 0 7
  let rivalBase := 9.5 + 5 * sinOf year + 0.014 * (((year : Int) : Rat) - 850) + d.normRival * 1.6
  let rivalPower := max 1 (rivalBase * (0.72 + 0.48 * p.raidIntensity))
  let loyFrac := alignment / max 1 prePop
  let s0 := { s with cells := cellsI, monument := s.monument + ornamentalDays }
  let w := warPhase p year prePop loyFrac corePower rivalPower d.war s0
  let sk := shockPhase p year prePop w.casualties w.defection w.st
  let s2 := sk.st
  let growth := clamp (p.growthPct / 100 + 0.013 * (foodRatio - 1) + d.normGrowth * 0.0017)
    (-0.065) 0.028
  let targetGrowth := clamp growth (-0.06) 0.03
  let emigrRate := clamp ((1 - s2.courtLegitimacy) * 0.0019 + max 0 (1 - foodRatio) * 0.024) 0 0.045
  let factor := factorOf targetGrowth emigrRate sk.casualties prePop
  let cells2 := mapIdxFrom (fun i c => popLoyaltyUpdate p factor s2.courtLegitimacy sk.defection
    (d.lNormal i) c) 0 s2.cells
  let newTotal := sumL (cells2.map (·.pop))
  let bondedNew := clamp ((bondedC + w.captives) * (1 + 0.008 * p.bondedBirthPct - 0.01)
    - bondedC * 0.007 * (1 - s2.courtLegitimacy)) 0 (newTotal * 0.23)
  let cropTax := if 0 < surplus then clamp (allocatable / max 1 surplus) 0 1 else 0
  let legitNew := clamp (s2.courtLegitimacy + 0.005 * clamp (foodRatio - 1) (-1) 1
    + 0.007 * cropTax + 0.002 * log1p (ornamentalDays / 500000)
    - 0.0025 * (1 - loyFrac) - 0.004 * p.warExpense
    - 0.004 * (if surplus = 0 then (1 : Rat) else 0)) 0.035 1
  let shrineNew := clamp (s2.shrine + 0.0025 * p.templeAutonomy + 0.0014 * (ornamentalDays / 500000)
    - 0.002 * max 0 (1 - foodRatio) - 0.0022 * (1 - legitNew)) 0.02 1
  { s2 with cells := cells2, courtLegitimacy := legitNew, shrine := shrineNew, bonded := bondedNew,
            courtPower := corePower, rivalPower := rivalPower }

/-- Run a list of (year, draws) in order. -/
def runSteps (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat) :
    List (Int × Draws) → State → State
  | [], s => s
  | (y, d) :: rest, s => runSteps p sinOf log1p rest (step p sinOf log1p y d s)

/-! ## Lemmas -/

theorem sumL_nonneg : ∀ l : List Rat, (∀ x ∈ l, 0 ≤ x) → 0 ≤ sumL l
  | [], _ => by simp [sumL]
  | x :: xs, h => by
    have hx : 0 ≤ x := h x (by simp)
    have hs := sumL_nonneg xs (fun y hy => h y (by simp [hy]))
    simp only [sumL]
    grind

theorem infraUpdate_ok (p : Params) (sh maintSat : Rat) (c : Cell) :
    0.03 ≤ (infraUpdate p sh maintSat c).infra ∧ (infraUpdate p sh maintSat c).infra ≤ 1 := by
  unfold infraUpdate
  exact ⟨clamp_lower _ _ _, clamp_upper _ _ _ (by grind)⟩

theorem infra1177_ok (damage : Rat) (c : Cell) (h : 0.03 ≤ c.infra ∧ c.infra ≤ 1) :
    0.03 ≤ (infra1177 damage c).infra ∧ (infra1177 damage c).infra ≤ 1 := by
  unfold infra1177
  split
  · exact ⟨clamp_lower _ _ _, clamp_upper _ _ _ (by grind)⟩
  · exact h

theorem popLoyalty_ok (p : Params) (factor leg dfn ln : Rat) (c : Cell)
    (h : 0.03 ≤ c.infra ∧ c.infra ≤ 1) :
    (0.03 ≤ (popLoyaltyUpdate p factor leg dfn ln c).infra
      ∧ (popLoyaltyUpdate p factor leg dfn ln c).infra ≤ 1)
    ∧ (0.03 ≤ (popLoyaltyUpdate p factor leg dfn ln c).loyalty
      ∧ (popLoyaltyUpdate p factor leg dfn ln c).loyalty ≤ 0.98)
    ∧ 1 ≤ (popLoyaltyUpdate p factor leg dfn ln c).pop := by
  unfold popLoyaltyUpdate
  exact ⟨h, ⟨clamp_lower _ _ _, clamp_upper _ _ _ (by grind)⟩, by grind⟩

theorem sumL_pop_nonneg (cs : List Cell) (h : ∀ c ∈ cs, 1 ≤ c.pop) :
    0 ≤ sumL (cs.map (·.pop)) := by
  apply sumL_nonneg
  intro x hx
  obtain ⟨c, hc, rfl⟩ := List.mem_map.mp hx
  have := h c hc
  grind

theorem warPhase_cells (p : Params) (year : Int) (prePop loyFrac corePower rivalPower : Rat)
    (d : WarDraws) (t : State) :
    (warPhase p year prePop loyFrac corePower rivalPower d t).st.cells = t.cells := by
  unfold warPhase
  dsimp only
  repeat' split
  all_goals rfl

theorem shockPhase_cells_ok (p : Params) (year : Int) (prePop cas dfn : Rat) (t : State)
    (h : ∀ c ∈ t.cells, 0.03 ≤ c.infra ∧ c.infra ≤ 1) :
    ∀ c ∈ (shockPhase p year prePop cas dfn t).st.cells, 0.03 ≤ c.infra ∧ c.infra ≤ 1 := by
  intro c hc
  unfold shockPhase at hc
  split at hc
  · dsimp only at hc
    obtain ⟨c0, hc0, rfl⟩ := List.mem_map.mp hc
    exact infra1177_ok _ _ (h c0 hc0)
  · exact h c hc

/-! ## Target 1: bounds after one step -/

/-- Legitimacy after a step is in [0.035, 1]. -/
theorem step_legit_bounds (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat) (year : Int)
    (d : Draws) (s : State) :
    0.035 ≤ (step p sinOf log1p year d s).courtLegitimacy
      ∧ (step p sinOf log1p year d s).courtLegitimacy ≤ 1 := by
  obtain ⟨X, hX⟩ : ∃ X, (step p sinOf log1p year d s).courtLegitimacy = clamp X 0.035 1 := ⟨_, rfl⟩
  rw [hX]
  exact ⟨clamp_lower _ _ _, clamp_upper _ _ _ (by grind)⟩

/-- Shrine after a step is in [0.02, 1]. -/
theorem step_shrine_bounds (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat) (year : Int)
    (d : Draws) (s : State) :
    0.02 ≤ (step p sinOf log1p year d s).shrine ∧ (step p sinOf log1p year d s).shrine ≤ 1 := by
  obtain ⟨X, hX⟩ : ∃ X, (step p sinOf log1p year d s).shrine = clamp X 0.02 1 := ⟨_, rfl⟩
  rw [hX]
  exact ⟨clamp_lower _ _ _, clamp_upper _ _ _ (by grind)⟩

theorem mapIdxFrom_mem {α β : Type} (f : Nat → α → β) :
    ∀ (l : List α) (n : Nat) (x : β), x ∈ mapIdxFrom f n l → ∃ i a, a ∈ l ∧ x = f i a
  | [], _, _, hx => by simp [mapIdxFrom] at hx
  | a :: as, n, x, hx => by
    simp only [mapIdxFrom, List.mem_cons] at hx
    rcases hx with rfl | hx
    · exact ⟨n, a, by simp, rfl⟩
    · obtain ⟨i, b, hb, rfl⟩ := mapIdxFrom_mem f as (n + 1) x hx
      exact ⟨i, b, by simp [hb], rfl⟩

/-- Cells after a step: infra in [0.03, 1], loyalty in [0.03, 0.98], pop at least 1. -/
theorem step_cellsOK (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat) (year : Int)
    (d : Draws) (s : State) :
    ∀ c ∈ (step p sinOf log1p year d s).cells,
      (0.03 ≤ c.infra ∧ c.infra ≤ 1) ∧ (0.03 ≤ c.loyalty ∧ c.loyalty ≤ 0.98) ∧ 1 ≤ c.pop := by
  intro c hc
  unfold step at hc
  dsimp only at hc
  obtain ⟨i, c0, hc0, rfl⟩ := mapIdxFrom_mem _ _ _ _ hc
  have h0 : 0.03 ≤ c0.infra ∧ c0.infra ≤ 1 := by
    refine shockPhase_cells_ok _ _ _ _ _ _ ?_ c0 hc0
    intro x hx
    rw [warPhase_cells] at hx
    dsimp only at hx
    obtain ⟨c1, _, rfl⟩ := List.mem_map.mp hx
    exact infraUpdate_ok _ _ _ _
  exact popLoyalty_ok _ _ _ _ _ _ h0

/-- Target 1 as one predicate on a state. -/
def InBounds (s : State) : Prop :=
  (0.035 ≤ s.courtLegitimacy ∧ s.courtLegitimacy ≤ 1) ∧ (0.02 ≤ s.shrine ∧ s.shrine ≤ 1)
  ∧ (∀ c ∈ s.cells, (0.03 ≤ c.infra ∧ c.infra ≤ 1) ∧ (0.03 ≤ c.loyalty ∧ c.loyalty ≤ 0.98) ∧ 1 ≤ c.pop)
  ∧ (0 ≤ s.bonded ∧ s.bonded ≤ sumL (s.cells.map (·.pop)) * 0.23)

/-- Bonded after a step is in [0, 0.23 * new population total]. -/
theorem step_bonded_bounds (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat) (year : Int)
    (d : Draws) (s : State) :
    0 ≤ (step p sinOf log1p year d s).bonded
      ∧ (step p sinOf log1p year d s).bonded
        ≤ sumL ((step p sinOf log1p year d s).cells.map (·.pop)) * 0.23 := by
  obtain ⟨X, hX⟩ : ∃ X, (step p sinOf log1p year d s).bonded
      = clamp X 0 (sumL ((step p sinOf log1p year d s).cells.map (·.pop)) * 0.23) := ⟨_, rfl⟩
  have hn := sumL_pop_nonneg _ (fun c hc => (step_cellsOK p sinOf log1p year d s c hc).2.2)
  rw [hX]
  exact ⟨clamp_lower _ _ _, clamp_upper _ _ _ (by grind)⟩

/-- Target 1 after one step, from any starting state. -/
theorem step_inBounds (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat) (year : Int)
    (d : Draws) (s : State) : InBounds (step p sinOf log1p year d s) :=
  ⟨step_legit_bounds p sinOf log1p year d s, step_shrine_bounds p sinOf log1p year d s,
    step_cellsOK p sinOf log1p year d s, step_bonded_bounds p sinOf log1p year d s⟩

/-- Target 1 over any nonempty run, from any starting state. -/
theorem runSteps_inBounds (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat) :
    ∀ (xs : List (Int × Draws)) (s : State), xs ≠ [] → InBounds (runSteps p sinOf log1p xs s)
  | [], _, h => absurd rfl h
  | (y, d) :: rest, s, _ => by
    cases rest with
    | nil => exact step_inBounds p sinOf log1p y d s
    | cons r rs => exact runSteps_inBounds p sinOf log1p (r :: rs) _ (by simp)

/-! ## Counters (target 2) -/

theorem warPhase_counters (p : Params) (year : Int) (prePop loyFrac corePower rivalPower : Rat)
    (wd : WarDraws) (t : State) :
    t.wars ≤ (warPhase p year prePop loyFrac corePower rivalPower wd t).st.wars
      ∧ t.sacks ≤ (warPhase p year prePop loyFrac corePower rivalPower wd t).st.sacks
      ∧ t.victories ≤ (warPhase p year prePop loyFrac corePower rivalPower wd t).st.victories
      ∧ t.defeats ≤ (warPhase p year prePop loyFrac corePower rivalPower wd t).st.defeats
      ∧ (t.wars = t.victories + t.defeats →
          (warPhase p year prePop loyFrac corePower rivalPower wd t).st.wars
            = (warPhase p year prePop loyFrac corePower rivalPower wd t).st.victories
              + (warPhase p year prePop loyFrac corePower rivalPower wd t).st.defeats) := by
  unfold warPhase
  dsimp only
  repeat' split
  all_goals (dsimp only; refine ⟨by omega, by omega, by omega, by omega, fun h => by omega⟩)

theorem shockPhase_wars_eq (p : Params) (year : Int) (prePop cas dfn : Rat) (t : State) :
    (shockPhase p year prePop cas dfn t).st.wars = t.wars := by
  unfold shockPhase
  split <;> rfl

theorem shockPhase_victories_eq (p : Params) (year : Int) (prePop cas dfn : Rat) (t : State) :
    (shockPhase p year prePop cas dfn t).st.victories = t.victories := by
  unfold shockPhase
  split <;> rfl

theorem shockPhase_defeats_eq (p : Params) (year : Int) (prePop cas dfn : Rat) (t : State) :
    (shockPhase p year prePop cas dfn t).st.defeats = t.defeats := by
  unfold shockPhase
  split <;> rfl

theorem shockPhase_sacks_ge (p : Params) (year : Int) (prePop cas dfn : Rat) (t : State) :
    t.sacks ≤ (shockPhase p year prePop cas dfn t).st.sacks := by
  unfold shockPhase
  split
  · show t.sacks ≤ t.sacks + 1
    omega
  · exact Nat.le_refl _

/-- One step never decreases a counter, and keeps wars = victories + defeats. -/
theorem step_counters (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat) (year : Int)
    (d : Draws) (s : State) (hinv : s.wars = s.victories + s.defeats) :
    s.wars ≤ (step p sinOf log1p year d s).wars
      ∧ s.sacks ≤ (step p sinOf log1p year d s).sacks
      ∧ s.victories ≤ (step p sinOf log1p year d s).victories
      ∧ s.defeats ≤ (step p sinOf log1p year d s).defeats
      ∧ (step p sinOf log1p year d s).wars
        = (step p sinOf log1p year d s).victories + (step p sinOf log1p year d s).defeats := by
  unfold step
  dsimp only
  rw [shockPhase_wars_eq, shockPhase_victories_eq, shockPhase_defeats_eq]
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · refine Nat.le_trans ?_ (warPhase_counters _ _ _ _ _ _ _ _).1
    exact Nat.le_refl _
  · refine Nat.le_trans ?_ (shockPhase_sacks_ge _ _ _ _ _ _)
    refine Nat.le_trans ?_ (warPhase_counters _ _ _ _ _ _ _ _).2.1
    exact Nat.le_refl _
  · refine Nat.le_trans ?_ (warPhase_counters _ _ _ _ _ _ _ _).2.2.1
    exact Nat.le_refl _
  · refine Nat.le_trans ?_ (warPhase_counters _ _ _ _ _ _ _ _).2.2.2.1
    exact Nat.le_refl _
  · exact (warPhase_counters _ _ _ _ _ _ _ _).2.2.2.2 hinv

theorem runSteps_counters (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat) :
    ∀ (xs : List (Int × Draws)) (s : State), s.wars = s.victories + s.defeats →
      s.wars ≤ (runSteps p sinOf log1p xs s).wars
        ∧ s.sacks ≤ (runSteps p sinOf log1p xs s).sacks
        ∧ s.victories ≤ (runSteps p sinOf log1p xs s).victories
        ∧ s.defeats ≤ (runSteps p sinOf log1p xs s).defeats
        ∧ (runSteps p sinOf log1p xs s).wars
          = (runSteps p sinOf log1p xs s).victories + (runSteps p sinOf log1p xs s).defeats
  | [], s, h => ⟨Nat.le_refl _, Nat.le_refl _, Nat.le_refl _, Nat.le_refl _, h⟩
  | (y, d) :: rest, s, h => by
    have h1 := step_counters p sinOf log1p y d s h
    have ih := runSteps_counters p sinOf log1p rest (step p sinOf log1p y d s) h1.2.2.2.2
    show _ ∧ _ ∧ _ ∧ _ ∧ _
    obtain ⟨a1, a2, a3, a4, _⟩ := h1
    obtain ⟨b1, b2, b3, b4, b5⟩ := ih
    exact ⟨Nat.le_trans a1 b1, Nat.le_trans a2 b2, Nat.le_trans a3 b3, Nat.le_trans a4 b4, b5⟩

/-! ## Monument (target 2) -/

theorem shockPhase_monument (p : Params) (year : Int) (prePop cas dfn : Rat) (t : State) :
    (shockPhase p year prePop cas dfn t).st.monument = t.monument := by
  unfold shockPhase
  split <;> rfl

theorem warPhase_monument (p : Params) (year : Int) (prePop loyFrac corePower rivalPower : Rat)
    (wd : WarDraws) (t : State) :
    (warPhase p year prePop loyFrac corePower rivalPower wd t).st.monument = t.monument := by
  unfold warPhase
  dsimp only
  repeat' split
  all_goals rfl

theorem le_add_nonneg' (a b : Rat) (h : 0 ≤ b) : a ≤ a + b := by grind

theorem ornamental_nonneg (p : Params) (s : State) (L m M : Rat) (hskill : 0 ≤ p.monumentSkill)
    (hleg : 0 ≤ s.courtLegitimacy) :
    0 ≤ buildDaysOf L m M * p.monumentSkill * (0.38 + 0.4 * s.courtLegitimacy) := by
  refine Rat.mul_nonneg (Rat.mul_nonneg ?_ hskill) ?_
  · unfold buildDaysOf
    grind
  · grind

/-- Monument never decreases in one step when `monumentSkill >= 0` and legitimacy is nonnegative. -/
theorem step_monument_ge (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat) (year : Int)
    (d : Draws) (s : State) (hskill : 0 ≤ p.monumentSkill) (hleg : 0 ≤ s.courtLegitimacy) :
    s.monument ≤ (step p sinOf log1p year d s).monument := by
  unfold step
  dsimp only
  rw [shockPhase_monument, warPhase_monument]
  exact le_add_nonneg' _ _ (ornamental_nonneg p s _ _ _ hskill hleg)

theorem runSteps_monument (p : Params) (sinOf : Int → Rat) (log1p : Rat → Rat)
    (hskill : 0 ≤ p.monumentSkill) :
    ∀ (xs : List (Int × Draws)) (s : State), 0 ≤ s.courtLegitimacy →
      s.monument ≤ (runSteps p sinOf log1p xs s).monument
  | [], s, _ => by
    simp only [runSteps]
    exact Rat.le_refl
  | (y, d) :: rest, s, h => by
    have h1 := step_monument_ge p sinOf log1p y d s hskill h
    have h2 := step_legit_bounds p sinOf log1p y d s
    have ih := runSteps_monument p sinOf log1p hskill rest (step p sinOf log1p y d s) (by grind)
    show s.monument ≤ (runSteps p sinOf log1p rest (step p sinOf log1p y d s)).monument
    grind

/-! ## Budget (target 3) -/

theorem budget_identity (a : Rat) (p : Params) :
    armyBudgetOf a p + monumentBudgetOf a p + maintainBudgetOf a p
      = a * max 1 (p.buildShare + p.warExpense) := by
  unfold armyBudgetOf monumentBudgetOf maintainBudgetOf
  have k : p.buildShare + p.warExpense + max 0 (1 - p.buildShare - p.warExpense)
      = max 1 (p.buildShare + p.warExpense) := by grind
  have k2 : a * (p.buildShare + p.warExpense + max 0 (1 - p.buildShare - p.warExpense))
      = a * max 1 (p.buildShare + p.warExpense) := by rw [k]
  grind

/-- The three budgets sum to `allocatable` exactly when buildShare + warExpense <= 1 (for allocatable > 0). -/
theorem budget_sum_eq_iff (a : Rat) (p : Params) (ha : 0 < a) :
    armyBudgetOf a p + monumentBudgetOf a p + maintainBudgetOf a p = a
      ↔ p.buildShare + p.warExpense ≤ 1 := by
  rw [budget_identity]
  constructor
  · intro h
    by_cases hc : p.buildShare + p.warExpense ≤ 1
    · exact hc
    · exfalso
      have hx : max 1 (p.buildShare + p.warExpense) = p.buildShare + p.warExpense := by grind
      rw [hx] at h
      have hne : a ≠ 0 := by grind
      have h2 : a * (p.buildShare + p.warExpense - 1) = 0 := by grind
      grind
  · intro h
    have hx : max 1 (p.buildShare + p.warExpense) = 1 := by grind
    rw [hx]
    grind

/-- In-range overspend: buildShare 0.6 and warExpense 0.5 (both inside the page sliders' 0-0.8 range)
give budgets totalling 1.1 times allocatable. -/
theorem overspend_witness : ∃ (a : Rat) (p : Params), 0 < a
    ∧ 1 < p.buildShare + p.warExpense
    ∧ a < armyBudgetOf a p + monumentBudgetOf a p + maintainBudgetOf a p := by
  refine ⟨1, { defaultParams with buildShare := 0.6, warExpense := 0.5 }, by grind, ?_, ?_⟩
  · show (1 : Rat) < 0.6 + 0.5
    grind
  · rw [budget_identity]
    show (1 : Rat) < 1 * max 1 (0.6 + 0.5)
    grind

/-! ## Soldiers, food ratio and factor (target 5) -/

theorem floorR_nonneg (q : Rat) (h : 0 ≤ q) : 0 ≤ floorR q := by
  unfold floorR
  have h1 : 0 ≤ q.num := Rat.num_nonneg.mpr h
  have h3 : 0 ≤ q.num / (q.den : Int) := Int.ediv_nonneg h1 (by omega)
  exact_mod_cast h3

theorem le_div_of_mul_le' (a b c : Rat) (hb : 0 < b) (h : c * b ≤ a) : c ≤ a / b := by
  have hi : 0 < b⁻¹ := Rat.inv_pos.mpr hb
  have hi0 : (0 : Rat) ≤ b⁻¹ := by grind
  have hne : b ≠ 0 := by grind
  have h1 : b * b⁻¹ = 1 := Rat.mul_inv_cancel b hne
  have h2 := Rat.mul_le_mul_of_nonneg_right h hi0
  rw [Rat.div_def]
  grind

theorem soldiers_nonneg (prePop A : Rat) (hp : 0 ≤ prePop) (hA : 0 ≤ A) :
    0 ≤ soldiersOf prePop A := by
  unfold soldiersOf
  have h1 : 0 ≤ A / 0.12 := le_div_of_mul_le' A 0.12 0 (by grind) (by grind)
  have h2 := floorR_nonneg (A / 0.12) h1
  grind

theorem soldiers_le (prePop A : Rat) : soldiersOf prePop A ≤ prePop * 0.035 := by
  unfold soldiersOf
  grind

theorem foodRatio_bounds (u i d : Rat) : 0 ≤ foodRatioOf u i d ∧ foodRatioOf u i d ≤ 2.2 := by
  unfold foodRatioOf
  exact ⟨clamp_lower _ _ _, clamp_upper _ _ _ (by grind)⟩

theorem factor_bounds (tg em cas prePop : Rat) :
    0.87 ≤ factorOf tg em cas prePop ∧ factorOf tg em cas prePop ≤ 1.045 := by
  unfold factorOf
  exact ⟨clamp_lower _ _ _, clamp_upper _ _ _ (by grind)⟩

/-! ## Labour (target 4) -/

theorem labour_build_plus_maint_le (L m M : Rat) (h : m ≤ L) : buildDaysOf L m M + m ≤ L := by
  unfold buildDaysOf
  grind

/-- With localShare = 1, need = 10 and laborPool = 1 (all inside the sliders' ranges), maintLabor = 2.06 > 1. -/
theorem maintLabor_exceeds_witness : ∃ (p : Params) (need L : Rat), 0 ≤ L ∧ L < maintLaborOf p need L :=
  ⟨{ defaultParams with localShare := 1 }, 10, 1, by grind, by
    unfold maintLaborOf
    show (1 : Rat) < min 10 (1 * 0.36 + 10 * 1 * 0.17)
    grind⟩

/-- Labour overspend: build days plus maintenance labour exceed laborPool = 1 (build days are 0). -/
theorem labour_overspend_witness : ∃ (p : Params) (need L M : Rat), 0 ≤ L ∧ 0 ≤ M
    ∧ L < buildDaysOf L (maintLaborOf p need L) M + maintLaborOf p need L :=
  ⟨{ defaultParams with localShare := 1 }, 10, 1, 0, by grind, by grind, by
    unfold buildDaysOf maintLaborOf
    show (1 : Rat) < max 0 (min (1 - min 10 (1 * 0.36 + 10 * 1 * 0.17)) (0 * 1000 / 0.45))
      + min 10 (1 * 0.36 + 10 * 1 * 0.17)
    grind⟩

/-! ## Factor and casualties (target 5-6) -/

theorem div_le_of_le_mul' (a b c : Rat) (hb : 0 < b) (h : a ≤ c * b) : a / b ≤ c := by
  have hi : 0 < b⁻¹ := Rat.inv_pos.mpr hb
  have hi0 : (0 : Rat) ≤ b⁻¹ := by grind
  have hne : b ≠ 0 := by grind
  have h1 : b * b⁻¹ = 1 := Rat.mul_inv_cancel b hne
  have h2 := Rat.mul_le_mul_of_nonneg_right h hi0
  rw [Rat.div_def]
  grind

/-- If casualties are at least 0.17 * prePop (and prePop >= 1, tg <= 0.03, em >= 0), the
factor clamp at 0.87 is active: the excess casualties are absorbed. -/
theorem factor_absorbs (tg em cas prePop : Rat) (htg : tg ≤ 0.03) (hem : 0 ≤ em)
    (hpre : 1 ≤ prePop) (hcas : 0.17 * prePop ≤ cas) : factorOf tg em cas prePop = 0.87 := by
  have hm : max 1 prePop = prePop := by grind
  have hpos : (0 : Rat) < max 1 prePop := by grind
  have hd : 0.17 ≤ cas / max 1 prePop :=
    le_div_of_mul_le' cas (max 1 prePop) 0.17 hpos (by rw [hm]; exact hcas)
  have hx : 1 + tg - em - cas / max 1 prePop ≤ 0.87 := by grind
  unfold factorOf clamp
  grind

/-- Casualties from a defeat plus the 1177 shock are at most 0.0164 * prePop for all draws and
parameters in [0, 1]. -/
theorem casualties_bound (prePop cas cd sd : Rat) (hp : 0 ≤ prePop) (h1 : 0 ≤ cas) (h2 : cas ≤ 1)
    (h3 : 0 ≤ cd) (h4 : cd ≤ 1) (h5 : 0 ≤ sd) (h6 : sd ≤ 1) :
    prePop * (0.0006 + 0.002 * cas) * (0.6 + 0.7 * cd) + prePop * 0.013 * sd ≤ 0.0164 * prePop := by
  have hu : 0.0006 + 0.002 * cas ≤ 0.0026 := by grind
  have hv : 0.6 + 0.7 * cd ≤ 1.3 := by grind
  have hv0 : 0 ≤ 0.6 + 0.7 * cd := by grind
  have e1 : (0.0006 + 0.002 * cas) * (0.6 + 0.7 * cd) ≤ 0.0026 * 1.3 := by
    have a1 := Rat.mul_le_mul_of_nonneg_right hu hv0
    have a2 := Rat.mul_le_mul_of_nonneg_left hv (by grind : (0 : Rat) ≤ 0.0026)
    grind
  have e2 : prePop * ((0.0006 + 0.002 * cas) * (0.6 + 0.7 * cd)) ≤ prePop * (0.0026 * 1.3) :=
    Rat.mul_le_mul_of_nonneg_left e1 hp
  have e3 : prePop * sd ≤ prePop * 1 := Rat.mul_le_mul_of_nonneg_left h6 hp
  grind

/-- Within the stated ranges, the factor is never clamped: the unclamped value is used. -/
theorem factor_unclamped (tg em c prePop : Rat) (htg1 : -0.06 ≤ tg) (htg2 : tg ≤ 0.03)
    (hem1 : 0 ≤ em) (hem2 : em ≤ 0.045) (hc0 : 0 ≤ c) (hc : c ≤ 0.0164 * max 1 prePop) :
    factorOf tg em c prePop = 1 + tg - em - c / max 1 prePop := by
  have hpos : (0 : Rat) < max 1 prePop := by grind
  have hd : c / max 1 prePop ≤ 0.0164 := div_le_of_le_mul' c (max 1 prePop) 0.0164 hpos hc
  have hx1 : 0.87 ≤ 1 + tg - em - c / max 1 prePop := by grind
  have hdn : 0 ≤ c / max 1 prePop := le_div_of_mul_le' c (max 1 prePop) 0 hpos (by grind)
  have hx2 : 1 + tg - em - c / max 1 prePop ≤ 1.045 := by grind
  unfold factorOf clamp
  grind

/-- A cell whose pop is below 1/factor gains people from the floor: pop 0.5 at factor 0.87 becomes
pop 1, so the floor creates 0.565 people. Such a cell is far below the reference state. -/
theorem pop_floor_witness : ∃ (c : Cell) (f : Rat),
    c.pop * f < (popLoyaltyUpdate defaultParams f 0 0 0 c).pop :=
  ⟨{ pop := 0.5, fields := 0, infra := 0.5, loyalty := 0.5, loc := 0.5, access := 0.62,
     fertility := 1 }, 0.87, by
    unfold popLoyaltyUpdate
    show (0.5 : Rat) * 0.87 < max 1 (0.5 * 0.87
      * (1 + clamp ((0.62 - 0.62) * defaultParams.marketElasticity * 0.001 + (0.5 - 0.5) * 0.001)
        (-0.002) 0.002))
    unfold clamp
    grind⟩

end Angkor.Mandala
