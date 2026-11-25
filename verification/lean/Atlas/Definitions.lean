/-!
# Atlas model definitions (Lean 4 core; host-only verification prototype)

Units and domains are documented for every `def`. There are no partial functions:
where a numeric precondition is needed (a positive denominator, a share in `[0,1]`)
it is a named predicate or an explicit argument of the function, never a silent
assumption. This file is also the `def` tier of `docs/audit/LEMMA_LEDGER.md`.
-/
namespace Atlas

/-- A pupil cohort. Units: pupils. Domain: any `Nat` (use `Cohort.positive` where needed). -/
structure Cohort where
  size : Nat
deriving Repr, DecidableEq

/-- Gate kinds used by the engine's vertical routing ladder. -/
inductive GateKind where
  | bar
  | quota
  | contest
deriving Repr, DecidableEq

/-- A gate. `seats` is elite seats (pupils); `shareNum/shareDen` is the seat share as a
    rational with `shareDen > 0`; meaningful shares satisfy `shareNum ≤ shareDen`
    (predicate `Gate.valid`). No proof fields, so the structure is `Repr`-able. -/
structure Gate where
  kind : GateKind
  seats : Nat
  shareNum : Nat
  shareDen : Nat
deriving Repr, DecidableEq

/-- Well-formedness of a gate: positive share denominator and share in `[0,1]`. -/
def Gate.valid (g : Gate) : Prop :=
  g.shareDen > 0 ∧ g.shareNum ≤ g.shareDen

/-- Seat count from a share: `max 1 (round (share · N))`, round half up, integer numerator
    and denominator. Units: seats (`Nat`). Domain: `shareDen > 0`, any cohort size.
    The `max 1` is the engine's `seats = max(round(share·N), 1)` convention (the seat-share
    denominator convention flagged in the contest audit). -/
def seatCount (shareNum shareDen cohortSize : Nat) (_hden : shareDen > 0) : Nat :=
  let numer := shareNum * cohortSize
  let q := numer / shareDen
  let r := numer % shareDen
  let rounded := if 2 * r >= shareDen then q + 1 else q
  max 1 rounded

/-- Accounting budget. Units: resource units. -/
structure Budget where
  total : Nat
  spend : Nat
deriving Repr, DecidableEq

/-- Tax ledger. Units: resource units; `rateNum/rateDen` is the tax rate (domain:
    `rateDen > 0`). -/
structure TaxLedger where
  base : Nat
  rateNum : Nat
  rateDen : Nat
deriving Repr, DecidableEq

/-- Prep-stock state. Units: stock units (`Int`, prototype integer encoding; the physical
    model uses a rational retention factor — see `prepStep`). -/
structure PrepStock where
  stock : Int
deriving Repr, DecidableEq

/-- Plackett–Luce candidate set with two candidates (the finite prototype case; the general
    `n` case is Tier 2 in the scope document). -/
inductive Cand where
  | a
  | b
deriving Repr, DecidableEq

/-- Candidate weights, integer-scaled (units: weight units; positive total weight is stated
    as a hypothesis where used). -/
structure PLWeights where
  w0 : Nat
  w1 : Nat
deriving Repr, DecidableEq

/-- Paper D "inventory equation" state. The five channels that Paper D claims are omitted
    are tracked explicitly as fields: M1 `schoolSupply`, M2 `positionalSeats`,
    M3 `withholding`, M4 `timeBudget`, M5 `supplyForm`. Units: integer model units
    (prototype exact encoding); domain: any state. -/
structure EqState where
  income : Int
  price : Int
  fee : Int
  schoolSupply : Int
  positionalSeats : Int
  withholding : Int
  timeBudget : Int
  supplyForm : Int
deriving Repr, DecidableEq

/-- The classical/inventory demand equation, as the inventory states it: demand depends on
    income, price and fees only. Units: integer demand units. -/
def classicalDemand (q : EqState) : Int :=
  q.income - q.price - q.fee

end Atlas
