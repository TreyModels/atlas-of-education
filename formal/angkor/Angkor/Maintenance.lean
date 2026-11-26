import Angkor.Basic

/-!
# One year of the maintenance and flight model (review version)

Source: `experiments/angkor-review/model/accounted_v2.py`.
`Settings` is lines 28-44, `parts_of` lines 47-54, the year loop `run` lines 67-148
(village block 80-134, refuge block 135-148).

Modelling decisions (see CONVENTIONS.md):
* Exact rationals (`Rat`). Theorems are about ideal arithmetic, not IEEE doubles.
* Weather is an input `w : Rat` for each year. The source draws it at line 74 with
  `rng.uniform` times the drought factor; here the draw is replaced by `w`. The drought
  flag still drives the canal shock in years 68 and 72 (line 134).
* Not modelled: `communities`, `years`, `seed` (random draws), and the history rows.
  The village list is an input.
* Run-time assert `sum(shares) <= 1` (line 84). The parameter asserts (lines 58-61) do not
  imply it (`paramAsserts_not_sufficient`). The positive results use `SharesFit`, a
  sufficient parameter condition for it.
* Hypotheses added beyond the source asserts: `0 <= refuge_yield` (the source has no
  assert), and `0 <= w` (nonnegative weather, as the task requires).
* Divisions, each flagged: `paid / bill` is guarded by `bill = 0 -> 1` (line 111);
  `actual / available` by `available = 0 -> 0` (line 132); `farm / (110 * 162)` and
  `farm / (land * 162)` by the constant or the guard `land = 0 -> 0` (lines 87, 138);
  `gap / max 1 need` (line 123) has denominator at least 1; `effective / (25/1000)` is constant.
-/

namespace Angkor.Maintenance

open Angkor

/-- Regime, `s.regime` (line 58). -/
inductive Regime where
  | stable
  | maintenance_only
  | reshuffle
  deriving DecidableEq

/-- Elite grain option, `s.elite_use` (line 61). -/
inductive EliteUse where
  | relief
  | service
  deriving DecidableEq

/-- The four reshuffle channels, `PARTS` (line 25), as four booleans. -/
structure Parts where
  extraction : Bool
  relief : Bool
  trust : Bool
  grievance : Bool

/-- `reshuffle_parts = 'all'` (lines 48-49). -/
def Parts.all : Parts := ⟨true, true, true, true⟩

/-- `reshuffle_parts = 'none'` (lines 50-51). -/
def Parts.none : Parts := ⟨false, false, false, false⟩

/-- The settings read by `run` (source lines 28-44). `years`, `communities` and `seed` are omitted. -/
structure Settings where
  regime : Regime
  drought : Bool
  maintenance_factor : Rat
  military_share : Rat
  monument_share : Rat
  religion_share : Rat
  refuge_yield : Rat
  canal_floor : Rat
  elite_spend : Rat
  elite_use : EliteUse
  parts : Parts

/-- Parameter asserts of source lines 58-61, plus `0 <= refuge_yield` (added, not asserted in source). -/
structure ParamAsserts (s : Settings) : Prop where
  maintenance_factor : 0 ≤ s.maintenance_factor ∧ s.maintenance_factor ≤ 1
  military_share : 0 ≤ s.military_share ∧ s.military_share ≤ 1
  monument_share : 0 ≤ s.monument_share ∧ s.monument_share ≤ 1
  religion_share : 0 ≤ s.religion_share ∧ s.religion_share ≤ 1
  elite_spend : 0 ≤ s.elite_spend ∧ s.elite_spend ≤ 1
  canal_floor : 0 ≤ s.canal_floor ∧ s.canal_floor ≤ 1
  refuge_yield : 0 ≤ s.refuge_yield

/-- Sufficient parameter condition for the run-time assert `sum(shares) <= 1` (line 84).
The maintenance share is `(.025 + .055 * (1 - canal)) * factor <= .08` for canal in [0,1]
and factor in [0,1], so the five shares total at most `military + monument + religion + .015 + .08`. -/
def SharesFit (s : Settings) : Prop :=
  s.military_share + s.monument_share + s.religion_share + 15/1000 + 8/100 ≤ 1

/-- `active = year >= 55 and regime != 'stable'` (line 68). -/
def isActive (s : Settings) (year : Nat) : Bool :=
  decide (55 ≤ year) && decide (s.regime ≠ Regime.stable)

/-- `reshuffle = active and regime == 'reshuffle'` (line 69). -/
def isReshuffle (s : Settings) (year : Nat) : Bool :=
  isActive s year && decide (s.regime = Regime.reshuffle)

/-- `x_ext` (line 70). -/
def xExtraction (s : Settings) (year : Nat) : Bool := isReshuffle s year && s.parts.extraction
/-- `x_rel` (line 71). -/
def xRelief (s : Settings) (year : Nat) : Bool := isReshuffle s year && s.parts.relief
/-- `x_tr` (line 72). -/
def xTrust (s : Settings) (year : Nat) : Bool := isReshuffle s year && s.parts.trust
/-- `x_gr` (line 73). -/
def xGrievance (s : Settings) (year : Nat) : Bool := isReshuffle s year && s.parts.grievance

/-- One village, the dict at line 64. Stocks in kg of grain, `n` persons, `canal` and `trust` in [0,1] by design. -/
structure Village where
  n : Rat
  store : Rat
  temple : Rat
  court : Rat
  elite : Rat
  canal : Rat
  trust : Rat

/-- Grain held in one village (the four stocks, line 76). -/
def Village.grain (v : Village) : Rat := v.store + v.temple + v.court + v.elite

/-- Whole system: villages, refuge population and refuge grain (lines 65 and 75). -/
structure State where
  villages : List Village
  refuge : Rat
  refStore : Rat

/-- Flows accumulated in one year (`births`, `deaths`, `harvest`, ... and the `work` dict, lines 77-78). -/
structure Flows where
  harvest : Rat
  seed : Rat
  spoil : Rat
  consumed : Rat
  shortfall : Rat
  births : Rat
  deaths : Rat
  moving : Rat
  unpaid : Rat
  elite_spent : Rat
  available : Rat
  farm : Rat
  actual : Rat
  idle : Rat

/-- All flows zero. -/
def Flows.zero : Flows := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩

/-- Componentwise sum of flows. -/
def Flows.add (a b : Flows) : Flows :=
  ⟨a.harvest + b.harvest, a.seed + b.seed, a.spoil + b.spoil, a.consumed + b.consumed,
   a.shortfall + b.shortfall, a.births + b.births, a.deaths + b.deaths, a.moving + b.moving,
   a.unpaid + b.unpaid, a.elite_spent + b.elite_spent, a.available + b.available,
   a.farm + b.farm, a.actual + b.actual, a.idle + b.idle⟩

/-- Labour available per village, `n * .45 * 180` (line 81). -/
def availDays (v : Village) : Rat := v.n * (45/100) * 180

/-- Maintenance share, lines 82. Factor applies only when `active`. -/
def maintShare (s : Settings) (year : Nat) (v : Village) : Rat :=
  (25/1000 + 55/1000 * (1 - v.canal)) * (if isActive s year then s.maintenance_factor else 1)

/-- Sum of the five shares, the terms of line 83 and the assert at line 84. -/
def shareSum (s : Settings) (year : Nat) (v : Village) : Rat :=
  s.military_share + maintShare s year v + s.monument_share + s.religion_share + 15/1000

/-- Coverage, line 87. The denominator `110 * 162` is a nonzero constant. -/
def coverage (farm : Rat) : Rat := min 1 (farm / (110 * 162))

/-- Gross harvest, line 88. -/
def grossHarvest (w canal farm : Rat) : Rat :=
  110 * 2150 * w * (4/10 + 6/10 * canal) * coverage farm

/-- Spoilage on one stock, lines 91-92 (`loss = .06 * stock`). -/
def spoilOf (x : Rat) : Rat := 6/100 * x

/-- Collected tax rate, line 93. -/
def taxRate (s : Settings) (year : Nat) : Rat :=
  if xExtraction s year then 25/100 else 16/100

/-- Service payment, lines 105-111. `paid` is capped by the pool, `fromCourt` by court
grain, and `funded = paid / bill` with the guard `bill = 0 -> 1` (line 111). -/
structure Pay where
  paid : Rat
  fromCourt : Rat
  funded : Rat

/-- Service payment, lines 105-111. -/
def payment (bill court service : Rat) : Pay :=
  let paid := min (court + service) bill
  let fromCourt := min court paid
  ⟨paid, fromCourt, if bill = 0 then 1 else paid / bill⟩

/-- Shortfall deficit, line 123. The denominator `max 1 need` is at least 1. -/
def deficitOf (gap need : Rat) : Rat := gap / max 1 need

/-- Grievance, lines 125-126. -/
def grievanceOf (perceivedTax : Rat) : Rat := max 0 (perceivedTax + 16/100 + 7/100 - 29/100)

/-- Flight fraction, line 127. -/
def fractionOf (deficit grievance trust : Rat) : Rat :=
  min (23/100) ((13/100 * deficit + 32/1000 * grievance + 15/1000 * (1 - trust)) * 92/100)

/-- People moving out, line 128. -/
def movingOf (n died born fraction : Rat) : Rat := max 0 ((n - died + born) * fraction)

/-- Trust after the year, line 131 (clamped to [0,1] as `max(0, min(1, .))`). -/
def trustNew (trust deficit grievance : Rat) (xTr : Bool) : Rat :=
  clamp (trust + (if deficit < 2/100 then 12/1000 else -(9/100 * deficit))
    - 9/1000 * grievance - (if xTr then 15/1000 else 0)) 0 1

/-- Canal condition after the year, lines 132-134. `effective = actual irrigation / available`
is guarded by `available = 0 -> 0` (line 132). The floor is `canal_floor`, cap 1. -/
def canalNew (s : Settings) (year : Nat) (canal actIrr avail n' : Rat) : Rat :=
  let effective := if avail = 0 then 0 else actIrr / avail
  let repair := effective / (25/1000) * (18/1000) * min 1 (n' / 400)
  clamp (canal - 18/1000 + repair
    - (if s.drought && (year == 68 || year == 72) then 6/100 else 0)) s.canal_floor 1

/-- One village for one year, lines 80-134. Returns the new village and its flows. -/
def stepVillage (s : Settings) (year : Nat) (w : Rat) (v : Village) : Village × Flows :=
  -- labour and shares (lines 81-86)
  let avail := availDays v
  let maint := maintShare s year v
  let reqMil := avail * s.military_share
  let reqIrr := avail * maint
  let reqMon := avail * s.monument_share
  let reqRel := avail * s.religion_share
  let reqAdm := avail * (15/1000)
  let reqTotal := reqMil + reqIrr + reqMon + reqRel + reqAdm
  let farm := avail * (1 - shareSum s year v)
  -- harvest (lines 87-89)
  let gross := grossHarvest w v.canal farm
  let seed := min gross (110 * 65)
  let net := gross - seed
  -- spoilage (lines 91-92), then distribution of net harvest (lines 93-95)
  let spoil := spoilOf v.store + spoilOf v.temple + spoilOf v.court + spoilOf v.elite
  let store1 := v.store - spoilOf v.store
  let temple1 := v.temple - spoilOf v.temple
  let court1 := v.court - spoilOf v.court
  let elite1 := v.elite - spoilOf v.elite
  let tax := taxRate s year
  let court2 := court1 + net * tax
  let temple2 := temple1 + net * (16/100)
  let elite2 := elite1 + net * (7/100)
  let store2 := store1 + net * (1 - tax - 16/100 - 7/100)
  -- elite grain spend (lines 97-103)
  let spent := elite2 * s.elite_spend
  let elite3 := elite2 - spent
  let serviceGrain := if s.elite_use = EliteUse.relief then 0 else spent
  let store3 := if s.elite_use = EliteUse.relief then store2 + spent else store2
  -- service payment (lines 105-113)
  let bill := reqTotal / 365 * 280
  let pay := payment bill court2 serviceGrain
  let court4 := court2 - pay.fromCourt
  let elite4 := elite3 + (serviceGrain - (pay.paid - pay.fromCourt))
  let store4 := store3 + pay.paid
  let unpaid := bill - pay.paid
  -- actual and idle labour (lines 114-119)
  let actMil := reqMil * pay.funded
  let actIrr := reqIrr * pay.funded
  let actMon := reqMon * pay.funded
  let actRel := reqRel * pay.funded
  let actAdm := reqAdm * pay.funded
  let actTotal := actMil + actIrr + actMon + actRel + actAdm
  let idle := reqTotal - actTotal
  -- eating from store, then temple relief (lines 120-122)
  let need := v.n * 280
  let eatStore := min need store4
  let store5 := store4 - eatStore
  let relief := min (need - eatStore) (temple2 * (if xRelief s year then 3/10 else 95/100))
  let temple3 := temple2 - relief
  let eaten := eatStore + relief
  -- shortfall, demography and flight (lines 123-129)
  let gap := need - eaten
  let deficit := deficitOf gap need
  let died := v.n * (13/1000 + 19/100 * deficit)
  let born := v.n * (21/1000) * (1 - deficit)
  let perceived := if xGrievance s year then 25/100 else tax
  let grievance := grievanceOf perceived
  let fraction := fractionOf deficit grievance v.trust
  let moving := movingOf v.n died born fraction
  let n' := v.n + born - died - moving
  -- trust and canal (lines 131-134)
  let trust' := trustNew v.trust deficit grievance (xTrust s year)
  let canal' := canalNew s year v.canal actIrr avail n'
  ({ n := n', store := store5, temple := temple3, court := court4, elite := elite4,
     canal := canal', trust := trust' },
   { harvest := gross, seed := seed, spoil := spoil, consumed := eaten, shortfall := gap,
     births := born, deaths := died, moving := moving, unpaid := unpaid, elite_spent := spent,
     available := avail, farm := farm, actual := actTotal, idle := idle })

/-- Refuge block, lines 135-148. `pop` is the refuge population after this year's moves
(`refuge` at line 135, including `moving` from every village). Returns the new population,
the new refuge grain and the flows. -/
def stepRefuge (s : Settings) (w pop store : Rat) : Rat × Rat × Flows :=
  let land := min 3575 (pop * 110 / 400)
  let avail := pop * (45/100) * 180
  let farm := min avail (land * 162)
  -- coverage guard `if land else 0` (line 138)
  let cov := if land = 0 then 0 else min 1 (farm / (land * 162))
  let gross := land * s.refuge_yield * w * (91/100) * cov
  let seed := min gross (land * 65)
  let loss := spoilOf store
  let store1 := store - loss + gross - seed
  let need := pop * 280
  let eaten := min need store1
  let store2 := store1 - eaten
  let gap := need - eaten
  let deficit := deficitOf gap need
  let died := pop * (13/1000 + 19/100 * deficit)
  let born := pop * (21/1000) * (1 - deficit)
  (pop + born - died, store2,
   { harvest := gross, seed := seed, spoil := loss, consumed := eaten, shortfall := gap,
     births := born, deaths := died, moving := 0, unpaid := 0, elite_spent := 0,
     available := avail, farm := farm, actual := 0, idle := avail - farm })

/-- The village loop of `run` (line 79-134), folded over the list in order. -/
def stepList (s : Settings) (year : Nat) (w : Rat) : List Village → List Village × Flows
  | [] => ([], Flows.zero)
  | v :: vs =>
    let a := stepVillage s year w v
    let b := stepList s year w vs
    (a.1 :: b.1, a.2.add b.2)

/-- One year for the whole system (lines 67-148). -/
def stepYear (s : Settings) (year : Nat) (w : Rat) (st : State) : State × Flows :=
  let vs := stepList s year w st.villages
  let r := stepRefuge s w (st.refuge + vs.2.moving) st.refStore
  ({ villages := vs.1, refuge := r.1, refStore := r.2.1 }, vs.2.add r.2.2)

/-- Years in order, with the weather of each year. -/
def runYears (s : Settings) : List (Nat × Rat) → State → State
  | [], st => st
  | (y, w) :: rest, st => runYears s rest (stepYear s y w st).1

/-- Sum of grain over a list of villages. -/
def grainSum : List Village → Rat
  | [] => 0
  | v :: vs => v.grain + grainSum vs

/-- Sum of population over a list of villages. -/
def popSum : List Village → Rat
  | [] => 0
  | v :: vs => v.n + popSum vs

/-- Sum of labour-related identity terms is checked by the theorems below. -/
def State.grain (st : State) : Rat := grainSum st.villages + st.refStore

/-- Total population in the system, including the refuge. -/
def State.pop (st : State) : Rat := popSum st.villages + st.refuge

/-! ## Target 1 and 2: ledgers, population and labour (exact identities, no hypotheses) -/

theorem stepList_cons (s : Settings) (year : Nat) (w : Rat) (v : Village) (vs : List Village) :
    stepList s year w (v :: vs)
      = ((stepVillage s year w v).1 :: (stepList s year w vs).1,
         (stepVillage s year w v).2.add (stepList s year w vs).2) := rfl

/-- Grain ledger for one village, both `elite_use` modes (the mode only changes which
branch the `if` takes, and the identity holds in each). Source lines 91-122. -/
theorem village_grain_ledger (s : Settings) (year : Nat) (w : Rat) (v : Village) :
    (stepVillage s year w v).1.grain
      = v.grain + (stepVillage s year w v).2.harvest - (stepVillage s year w v).2.seed
        - (stepVillage s year w v).2.spoil - (stepVillage s year w v).2.consumed := by
  simp only [stepVillage, Village.grain]
  grind

/-- Grain ledger for the refuge block, lines 141-144. -/
theorem refuge_grain_ledger (s : Settings) (w pop store : Rat) :
    (stepRefuge s w pop store).2.1
      = store + (stepRefuge s w pop store).2.2.harvest - (stepRefuge s w pop store).2.2.seed
        - (stepRefuge s w pop store).2.2.spoil - (stepRefuge s w pop store).2.2.consumed := by
  simp only [stepRefuge]
  grind

/-- Grain ledger for a list of villages, by induction on the list. -/
theorem list_grain_ledger (s : Settings) (year : Nat) (w : Rat) :
    ∀ vs : List Village,
      grainSum (stepList s year w vs).1
        = grainSum vs + (stepList s year w vs).2.harvest - (stepList s year w vs).2.seed
          - (stepList s year w vs).2.spoil - (stepList s year w vs).2.consumed
  | [] => by simp [stepList, grainSum, Flows.zero] <;> grind
  | v :: vs => by
    have ih := list_grain_ledger s year w vs
    have hv := village_grain_ledger s year w v
    rw [stepList_cons]
    simp only [grainSum, Flows.add]
    grind

/-- Grain ledger for the whole year, villages plus refuge (lines 67-148). -/
theorem year_grain_ledger (s : Settings) (year : Nat) (w : Rat) (st : State) :
    (stepYear s year w st).1.grain
      = st.grain + (stepYear s year w st).2.harvest - (stepYear s year w st).2.seed
        - (stepYear s year w st).2.spoil - (stepYear s year w st).2.consumed := by
  have h1 := list_grain_ledger s year w st.villages
  have h2 := refuge_grain_ledger s w (st.refuge + (stepList s year w st.villages).2.moving) st.refStore
  simp only [State.grain, stepYear, Flows.add]
  grind

/-- Village population: `n_new + moving = n + born - died` (lines 124-129). -/
theorem village_population (s : Settings) (year : Nat) (w : Rat) (v : Village) :
    (stepVillage s year w v).1.n + (stepVillage s year w v).2.moving
      = v.n + (stepVillage s year w v).2.births - (stepVillage s year w v).2.deaths := by
  simp only [stepVillage]
  grind

theorem list_population (s : Settings) (year : Nat) (w : Rat) :
    ∀ vs : List Village,
      popSum (stepList s year w vs).1
        = popSum vs + (stepList s year w vs).2.births - (stepList s year w vs).2.deaths
          - (stepList s year w vs).2.moving
  | [] => by simp [stepList, popSum, Flows.zero] <;> grind
  | v :: vs => by
    have ih := list_population s year w vs
    have hv := village_population s year w v
    rw [stepList_cons]
    simp only [popSum, Flows.add]
    grind

/-- Refuge population: the refuge gets `moving` and then its own births and deaths. -/
theorem refuge_population (s : Settings) (w pop store : Rat) :
    (stepRefuge s w pop store).1 = pop + (stepRefuge s w pop store).2.2.births
      - (stepRefuge s w pop store).2.2.deaths := by
  simp only [stepRefuge]

/-- System population: `total_new = total + births - deaths` (line 150-153). -/
theorem year_population (s : Settings) (year : Nat) (w : Rat) (st : State) :
    (stepYear s year w st).1.pop
      = st.pop + (stepYear s year w st).2.births - (stepYear s year w st).2.deaths := by
  have h1 := list_population s year w st.villages
  have h2 := refuge_population s w (st.refuge + (stepList s year w st.villages).2.moving) st.refStore
  simp only [State.pop, stepYear, Flows.add]
  grind

/-- Labour in one village: available = farm + actual + idle (lines 81-119). -/
theorem village_labour (s : Settings) (year : Nat) (w : Rat) (v : Village) :
    (stepVillage s year w v).2.available
      = (stepVillage s year w v).2.farm + (stepVillage s year w v).2.actual
        + (stepVillage s year w v).2.idle := by
  simp only [stepVillage, shareSum, availDays]
  grind

theorem list_labour (s : Settings) (year : Nat) (w : Rat) :
    ∀ vs : List Village,
      (stepList s year w vs).2.available
        = (stepList s year w vs).2.farm + (stepList s year w vs).2.actual
          + (stepList s year w vs).2.idle
  | [] => by simp [stepList, Flows.zero] <;> grind
  | v :: vs => by
    have ih := list_labour s year w vs
    have hv := village_labour s year w v
    rw [stepList_cons]
    simp only [Flows.add]
    grind

/-- Refuge labour: available = farm + 0 + (available - farm). -/
theorem refuge_labour (s : Settings) (w pop store : Rat) :
    (stepRefuge s w pop store).2.2.available
      = (stepRefuge s w pop store).2.2.farm + (stepRefuge s w pop store).2.2.actual
        + (stepRefuge s w pop store).2.2.idle := by
  simp only [stepRefuge]
  grind

/-- Labour for the whole year. -/
theorem year_labour (s : Settings) (year : Nat) (w : Rat) (st : State) :
    (stepYear s year w st).2.available
      = (stepYear s year w st).2.farm + (stepYear s year w st).2.actual
        + (stepYear s year w st).2.idle := by
  have h1 := list_labour s year w st.villages
  have h2 := refuge_labour s w (st.refuge + (stepList s year w st.villages).2.moving) st.refStore
  simp only [stepYear, Flows.add]
  grind

/-! ## Target 4: service payment (lines 105-111) -/

/-- The paid amount never exceeds the bill or the pool. -/
theorem payment_paid_le (bill court service : Rat) :
    (payment bill court service).paid ≤ bill ∧
      (payment bill court service).paid ≤ court + service := by
  simp only [payment]
  grind

/-- `from_court <= court`. -/
theorem payment_fromCourt_le (bill court service : Rat) :
    (payment bill court service).fromCourt ≤ court := by
  simp only [payment]
  grind

/-- Unused elite grain returned, `service - (paid - from_court)`, is nonnegative when
the service grain is nonnegative (source line 110). -/
theorem payment_returned_nonneg (bill court service : Rat) (hs : 0 ≤ service) :
    0 ≤ service - ((payment bill court service).paid - (payment bill court service).fromCourt) := by
  simp only [payment]
  grind

/-- `funded` lies in [0,1] when the bill, court and service grain are nonnegative.
The case `bill = 0` gives `funded = 1` (line 111). -/
theorem div_unit_bounds (p b : Rat) (hp : 0 ≤ p) (hpb : p ≤ b) (hb : 0 < b) :
    0 ≤ p / b ∧ p / b ≤ 1 := by
  have hi0 := Rat.inv_pos.mpr hb
  have hi : 0 ≤ b⁻¹ := by grind
  have hbb : b * b⁻¹ = 1 := Rat.mul_inv_cancel b (by grind)
  rw [Rat.div_def]
  constructor
  · exact Rat.mul_nonneg hp hi
  · have h := Rat.mul_le_mul_of_nonneg_right hpb hi
    rw [hbb] at h
    exact h

theorem payment_funded_bounds (bill court service : Rat) (hb : 0 ≤ bill) (hc : 0 ≤ court)
    (hs : 0 ≤ service) :
    0 ≤ (payment bill court service).funded ∧ (payment bill court service).funded ≤ 1 := by
  simp only [payment]
  split
  · grind
  · have hbpos : 0 < bill := by grind
    have hp : 0 ≤ min (court + service) bill := by grind
    have hpb : min (court + service) bill ≤ bill := by grind
    exact div_unit_bounds _ _ hp hpb hbpos

theorem payment_funded_zero_bill (court service : Rat) :
    (payment 0 court service).funded = 1 := by
  simp [payment]

/-! ## Target 3 and 5: bounds and invariance -/

/-- The state invariant of target 3 for one village: nonnegative population and stocks,
canal in [canal_floor, 1], trust in [0, 1]. -/
def VillageOK (s : Settings) (v : Village) : Prop :=
  0 ≤ v.n ∧ 0 ≤ v.store ∧ 0 ≤ v.temple ∧ 0 ≤ v.court ∧ 0 ≤ v.elite ∧
    s.canal_floor ≤ v.canal ∧ v.canal ≤ 1 ∧ 0 ≤ v.trust ∧ v.trust ≤ 1

/-- The invariant for the whole system. -/
def StateOK (s : Settings) (st : State) : Prop :=
  (∀ v ∈ st.villages, VillageOK s v) ∧ 0 ≤ st.refuge ∧ 0 ≤ st.refStore

/-- Division of a nonnegative value by a positive one. -/
theorem div_nonneg_of_pos (a b : Rat) (ha : 0 ≤ a) (hb : 0 < b) : 0 ≤ a / b := by
  have hi0 := Rat.inv_pos.mpr hb
  have hi : 0 ≤ b⁻¹ := by grind
  rw [Rat.div_def]
  exact Rat.mul_nonneg ha hi

/-- Maintenance share, line 82: between 0 and `.08` for canal in [0,1] and factor in [0,1]. -/
theorem maint_bounds (s : Settings) (year : Nat) (v : Village) (hp : ParamAsserts s)
    (hc0 : 0 ≤ v.canal) (hc1 : v.canal ≤ 1) :
    0 ≤ maintShare s year v ∧ maintShare s year v ≤ 8/100 := by
  unfold maintShare
  have hmf0 := hp.maintenance_factor.1
  have hmf1 := hp.maintenance_factor.2
  have hb0 : 0 ≤ 25/1000 + 55/1000 * (1 - v.canal) := by grind
  have hb1 : 25/1000 + 55/1000 * (1 - v.canal) ≤ 8/100 := by grind
  split
  · have p1 := Rat.mul_nonneg hb0 hmf0
    have p2 := Rat.mul_nonneg hb0 (show (0:Rat) ≤ 1 - s.maintenance_factor by grind)
    exact ⟨p1, by grind⟩
  · exact ⟨by grind, by grind⟩

/-- Sufficient parameter condition implies the run-time assert `sum(shares) <= 1` (line 84). -/
theorem shareSum_le_one (s : Settings) (year : Nat) (v : Village) (hf : SharesFit s)
    (hm : maintShare s year v ≤ 8/100) : shareSum s year v ≤ 1 := by
  unfold shareSum
  unfold SharesFit at hf
  grind

theorem coverage_bounds (f : Rat) (hf : 0 ≤ f) : 0 ≤ coverage f ∧ coverage f ≤ 1 := by
  unfold coverage
  have hd := div_nonneg_of_pos f (110 * 162) hf (by grind)
  constructor
  · grind
  · grind

theorem deficit_bounds (gap need : Rat) (h0 : 0 ≤ gap) (h1 : gap ≤ need) :
    0 ≤ deficitOf gap need ∧ deficitOf gap need ≤ 1 := by
  unfold deficitOf
  have hM : 0 < max 1 need := by grind
  have hgM : gap ≤ max 1 need := by grind
  exact div_unit_bounds gap (max 1 need) h0 hgM hM

theorem fraction_bounds (d g t : Rat) (hd : 0 ≤ d) (hg : 0 ≤ g) (ht : t ≤ 1) :
    0 ≤ fractionOf d g t ∧ fractionOf d g t ≤ 23/100 := by
  unfold fractionOf
  have hX : 0 ≤ (13/100 * d + 32/1000 * g + 15/1000 * (1 - t)) * 92/100 := by grind
  constructor
  · grind
  · grind

theorem grievance_nonneg (p : Rat) : 0 ≤ grievanceOf p := by
  unfold grievanceOf
  grind

/-- `n - died + born` is nonnegative (the moved-people bound needs it). -/
theorem balance_nonneg (n d : Rat) (hn : 0 ≤ n) (_hd0 : 0 ≤ d) (hd1 : d ≤ 1) :
    0 ≤ n - n * (13/1000 + 19/100 * d) + n * (21/1000) * (1 - d) := by
  have h := Rat.mul_nonneg hn (show (0:Rat) ≤ 1 - 211/1000 * d by grind)
  grind

theorem moving_bounds (n died born f : Rat) (hA : 0 ≤ n - died + born) (_hf0 : 0 ≤ f)
    (hf1 : f ≤ 1) :
    0 ≤ movingOf n died born f ∧ movingOf n died born f ≤ n + born - died := by
  unfold movingOf
  have h := Rat.mul_nonneg hA (show (0:Rat) ≤ 1 - f by grind)
  constructor
  · grind
  · grind

theorem trust_bounds (trust deficit grievance : Rat) (xTr : Bool) :
    0 ≤ trustNew trust deficit grievance xTr ∧ trustNew trust deficit grievance xTr ≤ 1 := by
  unfold trustNew
  exact ⟨clamp_lower _ _ _, clamp_upper _ _ _ (by grind)⟩

theorem canal_bounds (s : Settings) (year : Nat) (canal actIrr avail n' : Rat)
    (hfl : s.canal_floor ≤ 1) :
    s.canal_floor ≤ canalNew s year canal actIrr avail n'
      ∧ canalNew s year canal actIrr avail n' ≤ 1 := by
  unfold canalNew
  exact ⟨clamp_lower _ _ _, clamp_upper _ _ _ hfl⟩

/-- `0 <= X * c` and `X * c <= X` for `0 <= X` and `0 <= c <= 1`. -/
theorem mulc_bounds (X c : Rat) (hX : 0 ≤ X) (hc0 : 0 ≤ c) (hc1 : c ≤ 1) :
    0 ≤ X * c ∧ X * c ≤ X := by
  have h := Rat.mul_nonneg hX (show (0:Rat) ≤ 1 - c by grind)
  constructor
  · exact Rat.mul_nonneg hX hc0
  · grind

/-- Spoilage `loss = .06 * x` never exceeds `x` (lines 91-92). -/
theorem spoil_bounds (x : Rat) (hx : 0 ≤ x) : 0 ≤ spoilOf x ∧ spoilOf x ≤ x := by
  unfold spoilOf
  constructor <;> grind

/-- Eating from store then temple relief (lines 120-122): the shortfall `need - eaten` lies in
[0, need] whenever the store and temple are nonnegative and the cap is in [0,1]. -/
theorem eaten_bounds (need s4 tp cap : Rat) (hn : 0 ≤ need) (hs : 0 ≤ s4) (ht : 0 ≤ tp)
    (hc0 : 0 ≤ cap) (_hc1 : cap ≤ 1) :
    0 ≤ need - (min need s4 + min (need - min need s4) (tp * cap))
      ∧ need - (min need s4 + min (need - min need s4) (tp * cap)) ≤ need := by
  have h1 : 0 ≤ tp * cap := Rat.mul_nonneg ht hc0
  grind

/-- Paid service grain is nonnegative when the bill, court and service grain are. -/
theorem payment_paid_nonneg (bill court service : Rat) (hb : 0 ≤ bill) (hc : 0 ≤ court)
    (hs : 0 ≤ service) : 0 ≤ (payment bill court service).paid := by
  simp only [payment]
  grind

/-- `fromCourt` is nonnegative when the bill, court and service grain are nonnegative. -/
theorem payment_fromCourt_nonneg (bill court service : Rat) (hb : 0 ≤ bill) (hc : 0 ≤ court)
    (hs : 0 ≤ service) : 0 ≤ (payment bill court service).fromCourt := by
  simp only [payment]
  grind

/-- One village keeps the invariant, and its flight is nonnegative (targets 3 and 5).
The proof names each intermediate value of `stepVillage` in the order of the definition, then
bounds the named values one at a time. -/
theorem stepVillage_ok (s : Settings) (year : Nat) (w : Rat) (v : Village)
    (hp : ParamAsserts s) (hf : SharesFit s) (hw : 0 ≤ w) (hv : VillageOK s v) :
    VillageOK s (stepVillage s year w v).1 ∧ 0 ≤ (stepVillage s year w v).2.moving := by
  obtain ⟨hn, hst, htm, hct, hel, hcf, hc1, ht0, ht1⟩ := hv
  have hfl0 := hp.canal_floor.1
  have hfl1 := hp.canal_floor.2
  have hc0 : 0 ≤ v.canal := by grind
  have hm := maint_bounds s year v hp hc0 hc1
  have hsh := shareSum_le_one s year v hf hm.2
  have hav0 : 0 ≤ availDays v := by unfold availDays; grind
  have hfarm0 : 0 ≤ availDays v * (1 - shareSum s year v) :=
    Rat.mul_nonneg hav0 (by grind)
  have hcov := coverage_bounds (availDays v * (1 - shareSum s year v)) hfarm0
  have hgross0 : 0 ≤ grossHarvest w v.canal (availDays v * (1 - shareSum s year v)) := by
    unfold grossHarvest
    have hX : 0 ≤ 4/10 + 6/10 * v.canal := by grind
    exact Rat.mul_nonneg (Rat.mul_nonneg (Rat.mul_nonneg (by grind) hw) hX) hcov.1
  have htax0 : 0 ≤ taxRate s year ∧ taxRate s year ≤ 25/100 := by
    unfold taxRate
    split <;> grind
  have hcap0 : 0 ≤ (if xRelief s year then (3/10 : Rat) else 95/100)
      ∧ (if xRelief s year then (3/10 : Rat) else 95/100) ≤ 1 := by
    split <;> grind
  have hmil := hp.military_share
  have hmon := hp.monument_share
  have hrel := hp.religion_share
  have hes := hp.elite_spend
  simp only [stepVillage, VillageOK]
  generalize h_avail : availDays v = avail
  generalize h_maint : maintShare s year v = maint
  generalize h_reqMil : avail * s.military_share = reqMil
  generalize h_reqIrr : avail * maint = reqIrr
  generalize h_reqMon : avail * s.monument_share = reqMon
  generalize h_reqRel : avail * s.religion_share = reqRel
  generalize h_reqAdm : avail * (15/1000) = reqAdm
  generalize h_reqTotal : reqMil + reqIrr + reqMon + reqRel + reqAdm = reqTotal
  generalize h_farm : avail * (1 - shareSum s year v) = farm
  generalize h_gross : grossHarvest w v.canal farm = gross
  generalize h_seed : min gross (110 * 65) = seed
  generalize h_net : gross - seed = net
  generalize h_tax : taxRate s year = tax
  generalize h_cap : (if xRelief s year then (3/10 : Rat) else 95/100) = cap
  generalize h_spent : (v.elite - spoilOf v.elite + net * (7/100)) * s.elite_spend = spent
  generalize h_sg : (if s.elite_use = EliteUse.relief then 0 else spent) = sg
  generalize h_bill : reqTotal / 365 * 280 = bill
  generalize h_court2 : v.court - spoilOf v.court + net * tax = court2
  generalize h_pay : payment bill court2 sg = pay
  generalize h_store3 : (if s.elite_use = EliteUse.relief
      then v.store - spoilOf v.store + net * (1 - tax - 16/100 - 7/100) + spent
      else v.store - spoilOf v.store + net * (1 - tax - 16/100 - 7/100)) = store3
  generalize h_store4 : store3 + pay.paid = store4
  generalize h_temple2 : v.temple - spoilOf v.temple + net * (16/100) = temple2
  generalize h_need : v.n * 280 = need
  generalize h_eatStore : min need store4 = eatStore
  generalize h_relief : min (need - eatStore) (temple2 * cap) = relief
  generalize h_gap : need - (eatStore + relief) = gap
  generalize h_deficit : deficitOf gap need = deficit
  generalize h_died : v.n * (13/1000 + 19/100 * deficit) = died
  generalize h_born : v.n * (21/1000) * (1 - deficit) = born
  generalize h_grievance : grievanceOf (if xGrievance s year then 25/100 else tax) = grievance
  generalize h_fraction : fractionOf deficit grievance v.trust = fraction
  generalize h_moving : movingOf v.n died born fraction = moving
  -- equations for the earlier values, rewritten into the named form
  have hav : 0 ≤ avail := by rw [← h_avail]; exact hav0
  have hmaint : 0 ≤ maint ∧ maint ≤ 8/100 := by rw [← h_maint]; exact hm
  have htax : 0 ≤ tax ∧ tax ≤ 25/100 := by rw [← h_tax]; exact htax0
  have hcap : 0 ≤ cap ∧ cap ≤ 1 := by rw [← h_cap]; exact hcap0
  have hreqMil : 0 ≤ reqMil := by rw [← h_reqMil]; exact Rat.mul_nonneg hav hmil.1
  have hreqIrr : 0 ≤ reqIrr := by rw [← h_reqIrr]; exact Rat.mul_nonneg hav hmaint.1
  have hreqMon : 0 ≤ reqMon := by rw [← h_reqMon]; exact Rat.mul_nonneg hav hmon.1
  have hreqRel : 0 ≤ reqRel := by rw [← h_reqRel]; exact Rat.mul_nonneg hav hrel.1
  have hreqAdm : 0 ≤ reqAdm := by rw [← h_reqAdm]; exact Rat.mul_nonneg hav (by grind)
  have hreqTotal : 0 ≤ reqTotal := by rw [← h_reqTotal]; grind
  have hfarm : 0 ≤ farm := by rw [← h_farm, ← h_avail]; exact hfarm0
  have hgross : 0 ≤ gross := by rw [← h_gross, ← h_farm, ← h_avail]; exact hgross0
  have hseed : 0 ≤ seed ∧ seed ≤ gross := by rw [← h_seed]; grind
  have hnet0 : 0 ≤ net := by rw [← h_net]; grind
  have helite : 0 ≤ v.elite - spoilOf v.elite + net * (7/100) := by
    have := spoil_bounds v.elite hel
    grind
  have hspent : 0 ≤ spent ∧ spent ≤ v.elite - spoilOf v.elite + net * (7/100) := by
    rw [← h_spent]
    exact mulc_bounds _ _ helite hes.1 hes.2
  have hsg : 0 ≤ sg := by
    rw [← h_sg]
    split <;> grind
  have hcourt2 : 0 ≤ court2 := by
    rw [← h_court2]
    have := spoil_bounds v.court hct
    have := Rat.mul_nonneg hnet0 htax.1
    grind
  have htemple2 : 0 ≤ temple2 := by
    rw [← h_temple2]
    have := spoil_bounds v.temple htm
    grind
  have hstore3 : 0 ≤ store3 := by
    rw [← h_store3]
    have := spoil_bounds v.store hst
    have := Rat.mul_nonneg hnet0 (show (0:Rat) ≤ 1 - tax - 16/100 - 7/100 by grind)
    split <;> grind
  have hbill : 0 ≤ bill := by rw [← h_bill]; grind
  have hpaid0 : 0 ≤ pay.paid := by
    rw [← h_pay]; exact payment_paid_nonneg _ _ _ hbill hcourt2 hsg
  have hpaidle : pay.paid ≤ bill := by rw [← h_pay]; exact (payment_paid_le _ _ _).1
  have hfc0 : 0 ≤ pay.fromCourt := by
    rw [← h_pay]; exact payment_fromCourt_nonneg _ _ _ hbill hcourt2 hsg
  have hfcle : pay.fromCourt ≤ court2 := by rw [← h_pay]; exact payment_fromCourt_le _ _ _
  have hret : 0 ≤ sg - (pay.paid - pay.fromCourt) := by
    rw [← h_pay]; exact payment_returned_nonneg _ _ _ hsg
  have hstore4 : 0 ≤ store4 := by rw [← h_store4]; grind
  have hneed : 0 ≤ need := by rw [← h_need]; grind
  have heat := eaten_bounds need store4 temple2 cap hneed hstore4 htemple2 hcap.1 hcap.2
  rw [h_eatStore, h_relief, h_gap] at heat
  have hdef := deficit_bounds gap need heat.1 heat.2
  rw [h_deficit] at hdef
  have hA : 0 ≤ v.n - died + born := by
    rw [← h_died, ← h_born]; exact balance_nonneg v.n deficit hn hdef.1 hdef.2
  have hgr : 0 ≤ grievance := by rw [← h_grievance]; exact grievance_nonneg _
  have hfr := fraction_bounds deficit grievance v.trust hdef.1 hgr ht1
  rw [h_fraction] at hfr
  have hmv := moving_bounds v.n died born fraction hA hfr.1 (by grind)
  rw [h_moving] at hmv
  have hea : eatStore ≤ store4 := by rw [← h_eatStore]; grind
  have hrelmul := mulc_bounds temple2 cap htemple2 hcap.1 hcap.2
  have hrel_le : relief ≤ temple2 * cap := by rw [← h_relief]; grind
  have hrelle : relief ≤ temple2 := by grind
  refine ⟨⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩, ?_⟩
  · grind
  · grind
  · grind
  · grind
  · grind
  · exact (canal_bounds s year v.canal _ _ _ hfl1).1
  · exact (canal_bounds s year v.canal _ _ _ hfl1).2
  · exact (trust_bounds v.trust deficit grievance (xTrust s year)).1
  · exact (trust_bounds v.trust deficit grievance (xTrust s year)).2
  · exact hmv.1

/-- Refuge coverage in [0,1] (line 138; `if land` guard). -/
theorem refuge_cov_bounds (land farm : Rat) (hl : 0 ≤ land) (hf : 0 ≤ farm) :
    0 ≤ (if land = 0 then 0 else min 1 (farm / (land * 162)))
      ∧ (if land = 0 then 0 else min 1 (farm / (land * 162))) ≤ 1 := by
  split
  · grind
  · have hpos : 0 < land * 162 := by grind
    have hd := div_nonneg_of_pos farm (land * 162) hf hpos
    constructor <;> grind

/-- Refuge block keeps the population and the refuge store nonnegative (lines 135-148). -/
theorem refuge_ok (s : Settings) (w pop store : Rat) (hp : ParamAsserts s) (hw : 0 ≤ w)
    (hpop : 0 ≤ pop) (hst : 0 ≤ store) :
    0 ≤ (stepRefuge s w pop store).1 ∧ 0 ≤ (stepRefuge s w pop store).2.1 := by
  have hy := hp.refuge_yield
  simp only [stepRefuge]
  generalize h_land : min 3575 (pop * 110 / 400) = land
  generalize h_avail : pop * (45/100) * 180 = avail
  generalize h_farm : min avail (land * 162) = farm
  generalize h_cov : (if land = 0 then 0 else min 1 (farm / (land * 162))) = cov
  generalize h_gross : land * s.refuge_yield * w * (91/100) * cov = gross
  generalize h_seed : min gross (land * 65) = seed
  generalize h_loss : spoilOf store = loss
  generalize h_store1 : store - loss + gross - seed = store1
  generalize h_need : pop * 280 = need
  generalize h_eaten : min need store1 = eaten
  generalize h_gap : need - eaten = gap
  generalize h_deficit : deficitOf gap need = deficit
  generalize h_died : pop * (13/1000 + 19/100 * deficit) = died
  generalize h_born : pop * (21/1000) * (1 - deficit) = born
  have hland : 0 ≤ land := by rw [← h_land]; grind
  have havail : 0 ≤ avail := by rw [← h_avail]; grind
  have hfarm0 : 0 ≤ farm := by rw [← h_farm]; grind
  have hcov := refuge_cov_bounds land farm hland hfarm0
  rw [h_cov] at hcov
  have hgross : 0 ≤ gross := by
    rw [← h_gross]
    exact Rat.mul_nonneg (Rat.mul_nonneg (Rat.mul_nonneg (Rat.mul_nonneg hland hy) hw)
      (by grind)) hcov.1
  have hseed : 0 ≤ seed ∧ seed ≤ gross := by rw [← h_seed]; grind
  have hloss := spoil_bounds store hst
  rw [h_loss] at hloss
  have hstore1 : 0 ≤ store1 := by rw [← h_store1]; grind
  have hneed : 0 ≤ need := by rw [← h_need]; grind
  have heat : 0 ≤ eaten ∧ eaten ≤ need := by
    rw [← h_eaten]
    constructor
    · grind
    · grind
  have hgap : 0 ≤ gap ∧ gap ≤ need := by rw [← h_gap]; grind
  have hdef := deficit_bounds gap need hgap.1 hgap.2
  rw [h_deficit] at hdef
  have hA : 0 ≤ pop + born - died := by
    rw [← h_died, ← h_born]
    have := balance_nonneg pop deficit hpop hdef.1 hdef.2
    grind
  have hstore2 : 0 ≤ store1 - eaten := by grind
  exact ⟨hA, hstore2⟩

/-- A list of villages keeps the invariant and yields nonnegative moving flow. -/
theorem list_ok (s : Settings) (year : Nat) (w : Rat) (hp : ParamAsserts s) (hf : SharesFit s)
    (hw : 0 ≤ w) : ∀ vs : List Village, (∀ v ∈ vs, VillageOK s v) →
      (∀ v ∈ (stepList s year w vs).1, VillageOK s v) ∧ 0 ≤ (stepList s year w vs).2.moving
  | [] => fun _ => by
    refine ⟨fun u hu => by simp [stepList] at hu, ?_⟩
    simp [stepList, Flows.zero]
  | v :: vs => fun h => by
    have hv := stepVillage_ok s year w v hp hf hw (h v (by simp))
    have ih := list_ok s year w hp hf hw vs (fun u hu => h u (by simp [hu]))
    rw [stepList_cons]
    simp only [Flows.add]
    constructor
    · intro u hu
      simp only [List.mem_cons] at hu
      rcases hu with rfl | hu
      · exact hv.1
      · exact ih.1 u hu
    · have := hv.2
      have := ih.2
      grind

/-- One year keeps the whole-system invariant (targets 3). -/
theorem stepYear_ok (s : Settings) (year : Nat) (w : Rat) (hp : ParamAsserts s)
    (hf : SharesFit s) (hw : 0 ≤ w) (st : State) (hs : StateOK s st) :
    StateOK s (stepYear s year w st).1 := by
  obtain ⟨hv, hR, hS⟩ := hs
  have hl := list_ok s year w hp hf hw st.villages hv
  have hpop : 0 ≤ st.refuge + (stepList s year w st.villages).2.moving := by
    have := hl.2
    grind
  have hr := refuge_ok s w _ st.refStore hp hw hpop hS
  simp only [stepYear, StateOK]
  exact ⟨hl.1, hr.1, hr.2⟩

/-- Any number of years, with nonnegative weather, keeps the invariant (target 3). -/
theorem runYears_ok (s : Settings) (hp : ParamAsserts s) (hf : SharesFit s) :
    ∀ (sched : List (Nat × Rat)) (st : State), (∀ p ∈ sched, 0 ≤ p.2) → StateOK s st →
      StateOK s (runYears s sched st)
  | [], st, _, h => by simpa [runYears] using h
  | (y, w) :: rest, st, hw, h => by
    have h1 := stepYear_ok s y w hp hf (hw (y, w) (by simp)) st h
    simp only [runYears]
    exact runYears_ok s hp hf rest _ (fun p hq => hw p (by simp [hq])) h1

/-! ## Target 5: regime and parts facts -/

/-- The tax rate is `.16` whenever the extraction channel is off (line 93). -/
theorem taxRate_of_no_extraction (s : Settings) (y : Nat) (h : xExtraction s y = false) :
    taxRate s y = 16/100 := by
  unfold taxRate
  simp [h]

/-- The shares do not read `parts`. -/
theorem shareSum_parts (s : Settings) (p : Parts) (y : Nat) (v : Village) :
    shareSum { s with parts := p } y v = shareSum s y v := rfl

theorem maintShare_parts (s : Settings) (p : Parts) (y : Nat) (v : Village) :
    maintShare { s with parts := p } y v = maintShare s y v := rfl

/-- With `parts = none`, the regime `reshuffle` and `maintenance_only` give the same shares. -/
theorem shareSum_reshuffle_eq (s : Settings) (p : Parts) (y : Nat) (v : Village) :
    shareSum { s with regime := Regime.reshuffle, parts := p } y v
      = shareSum { s with regime := Regime.maintenance_only, parts := p } y v := by
  simp [shareSum, maintShare, isActive]

/-- `canalNew` reads only `drought` and `canal_floor`, not `parts` or `regime`. -/
theorem canalNew_parts (s : Settings) (p : Parts) (y : Nat) (c a v n : Rat) :
    canalNew { s with parts := p } y c a v n = canalNew s y c a v n := rfl

theorem canalNew_regime (s : Settings) (r : Regime) (p : Parts) (y : Nat) (c a v n : Rat) :
    canalNew { s with regime := r, parts := p } y c a v n = canalNew s y c a v n := rfl

theorem maintShare_reshuffle_eq (s : Settings) (p : Parts) (y : Nat) (v : Village) :
    maintShare { s with regime := Regime.reshuffle, parts := p } y v
      = maintShare { s with regime := Regime.maintenance_only, parts := p } y v := by
  simp [maintShare, isActive]

/-- With regime `stable`, the reshuffle parts do not change a village's year. -/
theorem village_stable_parts (s : Settings) (p q : Parts) (year : Nat) (w : Rat) (v : Village)
    (hs : s.regime = Regime.stable) :
    stepVillage { s with parts := p } year w v = stepVillage { s with parts := q } year w v := by
  have hxp : xExtraction { s with parts := p } year = false := by
    simp [xExtraction, isReshuffle, isActive, hs]
  have hxq : xExtraction { s with parts := q } year = false := by
    simp [xExtraction, isReshuffle, isActive, hs]
  simp only [stepVillage]
  rw [taxRate_of_no_extraction _ _ hxp, taxRate_of_no_extraction _ _ hxq]
  simp only [shareSum_parts, maintShare_parts, canalNew_parts]
  simp [xRelief, xTrust, xGrievance, isReshuffle, isActive, hs]

/-- With `reshuffle_parts = 'none'`, the reshuffle regime and the maintenance-only regime give
the same village year. -/
theorem village_none_reshuffle (s : Settings) (year : Nat) (w : Rat) (v : Village) :
    stepVillage { s with regime := Regime.reshuffle, parts := Parts.none } year w v
      = stepVillage { s with regime := Regime.maintenance_only, parts := Parts.none } year w v := by
  have hx1 : xExtraction { s with regime := Regime.reshuffle, parts := Parts.none } year = false := by
    simp [xExtraction, Parts.none]
  have hx2 : xExtraction { s with regime := Regime.maintenance_only, parts := Parts.none } year
      = false := by
    simp [xExtraction, Parts.none]
  simp only [stepVillage]
  rw [taxRate_of_no_extraction _ _ hx1, taxRate_of_no_extraction _ _ hx2]
  simp only [shareSum_reshuffle_eq, maintShare_reshuffle_eq, canalNew_regime]
  simp [xRelief, xTrust, xGrievance, isReshuffle, isActive, Parts.none]

/-! ## Counterexample and non-vacuity -/

/-- A configuration that meets every parameter assert of lines 58-61 (and `refuge_yield >= 0`),
with military, monument and religion shares at 1. -/
def badSettings : Settings :=
  { regime := Regime.stable, drought := false, maintenance_factor := 1/2,
    military_share := 1, monument_share := 1, religion_share := 1, refuge_yield := 2150,
    canal_floor := 0, elite_spend := 1/10, elite_use := EliteUse.relief, parts := Parts.none }

theorem paramAsserts_badSettings : ParamAsserts badSettings := by
  simp only [badSettings]
  refine ⟨⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ?_⟩ <;> grind

/-- The parameter asserts alone do not imply the run-time assert `sum(shares) <= 1` (line 84). -/
theorem paramAsserts_not_sufficient :
    ∃ s : Settings, ParamAsserts s ∧
      ∃ v : Village, 1 < shareSum s 0 v :=
  ⟨badSettings, paramAsserts_badSettings,
    { n := 400, store := 12000, temple := 15000, court := 0, elite := 0, canal := 85/100,
      trust := 75/100 },
    by simp [shareSum, maintShare, isActive, badSettings] <;> grind⟩

/-- Without the shares assert, the harvest can go negative (so the assert is needed for target 3). -/
theorem harvest_negative_without_fit :
    ∃ v : Village, (stepVillage badSettings 0 1 v).2.harvest < 0 :=
  ⟨{ n := 400, store := 12000, temple := 15000, court := 0, elite := 0, canal := 85/100,
      trust := 75/100 },
    by simp [stepVillage, grossHarvest, coverage, shareSum, maintShare, availDays, isActive,
      badSettings] <;> grind⟩

/-- A concrete settings record meeting every hypothesis of the invariance theorem. -/
def exSettings : Settings :=
  { regime := Regime.reshuffle, drought := true, maintenance_factor := 35/100,
    military_share := 8/100, monument_share := 4/100, religion_share := 4/100,
    refuge_yield := 2150, canal_floor := 0, elite_spend := 1/10, elite_use := EliteUse.relief,
    parts := Parts.all }

theorem exSettings_param : ParamAsserts exSettings := by
  simp only [exSettings]
  refine ⟨⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ?_⟩ <;> grind

theorem exSettings_fit : SharesFit exSettings := by
  simp only [SharesFit, exSettings]
  grind

/-- Initial state of the source (lines 64, 75): 24 villages, empty refuge. -/
def initState : State :=
  { villages := List.replicate 24
      { n := 400, store := 12000, temple := 15000, court := 0, elite := 0, canal := 85/100,
        trust := 75/100 },
    refuge := 0, refStore := 0 }

theorem initState_ok : StateOK exSettings initState := by
  refine ⟨?_, by simp [initState] <;> grind, by simp [initState] <;> grind⟩
  intro v hv
  simp only [initState] at hv
  have hv' := List.eq_of_mem_replicate hv
  subst hv'
  simp only [VillageOK, exSettings]
  grind

/-- Any run with nonnegative weather keeps the invariant, from the initial state (target 3). -/
theorem example_run (sched : List (Nat × Rat)) (hw : ∀ p ∈ sched, 0 ≤ p.2) :
    StateOK exSettings (runYears exSettings sched initState) :=
  runYears_ok exSettings exSettings_param exSettings_fit sched initState hw initState_ok

end Angkor.Maintenance
