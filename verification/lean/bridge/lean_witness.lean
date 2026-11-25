/-
Executable Lean witness for the differential-test bridge. Prints one JSON object per line
with exact integer values computed by the proved definitions. The Python side
(bridge/differential_test.py) compares these against fixture expectations.

Units are the exact integer encodings documented in Atlas/Definitions.lean.
-/
import Atlas

open Atlas

def jLine (k : String) (v : Int) : IO Unit :=
  IO.println s!"\{\"key\": \"{k}\", \"value\": {v}}"

def main : IO Unit := do
  -- Budget ledger: total 100, spend 60 => unallocated 40, identity holds.
  jLine "budget.total" 100
  jLine "budget.spend" 60
  jLine "budget.unallocated" (Int.ofNat (unallocated 100 60))
  -- Prep-stock recursion: retention 2, initial 3, inflows [1,2,3] => closed form.
  let inflows : List Int := [1, 2, 3]
  jLine "prep.rec" (prepRec 2 3 inflows)
  jLine "prep.closed" (3 * 2 ^ inflows.length + inflowGeomSum 2 inflows)
  -- Seat count: share 23/100 over cohort 300 => round(69) = 69, max 1 = 69.
  jLine "seats.share23.n300" (Int.ofNat (seatCount 23 100 300 (by decide)))
  -- Seat count: share 1/1000 over cohort 10 => round(0.01)=0 -> max 1 = 1.
  jLine "seats.minimum" (Int.ofNat (seatCount 1 1000 10 (by decide)))
  -- PL top-1 numerators for weights (2,3): sum = 5 = denominator.
  jLine "pl.top1.numer.sum" (Int.ofNat (top1Numerator ⟨2, 3⟩ .a + top1Numerator ⟨2, 3⟩ .b))
  jLine "pl.top1.denom" (Int.ofNat (plDenom ⟨2, 3⟩))
  -- Luna starter parity values.
  jLine "luna.gap.shortfall" (Int.ofNat (LeanStarter.gap 5 3))
  jLine "luna.gap.met" (Int.ofNat (LeanStarter.gap 3 5))
  jLine "luna.remainingCapacity" (Int.ofNat (LeanStarter.remainingCapacity 10 4))
  -- Codex-model parity values.
  jLine "model.gap.shortfall" (Int.ofNat (Atlas.Model.gap 3 5))
  jLine "model.gap.met" (Int.ofNat (Atlas.Model.gap 5 3))
  jLine "model.accepted" (Int.ofNat (Atlas.Model.accepted 10 4))
  jLine "model.increment.zero" (Int.ofNat (Atlas.Model.learningIncrement 7 7))
  jLine "model.totalInput" (Int.ofNat (Atlas.Model.totalInput ⟨2, 3, 4⟩))
  jLine "model.timeUsed" (Int.ofNat (Atlas.Model.timeUsed 1 2 3))
  jLine "model.complementarity" (Int.ofNat (Atlas.Model.complementaryLearning 3 2))
  jLine "model.feedback" (Int.ofNat (Atlas.Model.acceptedWithFeedback 2 1))
  jLine "model.rank.tie" (if Atlas.Model.outranksBool 5 5 0 1 then 1 else 0)
  jLine "model.rank.tie.shifted" (if Atlas.Model.outranksBool (5 + 7) (5 + 7) 0 1 then 1 else 0)
