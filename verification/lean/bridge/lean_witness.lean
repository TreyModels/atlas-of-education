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
