import Atlas.Definitions

/-!
# Kind-2 identities (proved in Lean 4 core)

Every theorem below states units and domain in its docstring. These are the identities the
Python engine relies on; the engine itself is *not* verified — it is differential-tested
against exactly these Lean statements on fixtures (see `LEAN_VERIFICATION_SCOPE.md` §4).
-/


namespace Atlas

/-! ## 1. Budget / teacher-salary ledger identity -/

/-- Unallocated budget remainder. Units: resource units (`Nat`). -/
def unallocated (budget spend : Nat) : Nat := budget - spend

/-- **Budget ledger identity.** Allocated spend plus the unallocated remainder equals the
    total budget. Units: resource units (`Nat`). Domain: `spend ≤ total` (the hypothesis is
    explicit — no partial subtraction). -/
theorem budget_ledger_identity (budget spend : Nat) (h : spend ≤ budget) :
    spend + unallocated budget spend = budget := by
  unfold unallocated
  exact Nat.add_sub_of_le h

/-- Tax revenue at an integer rate `rateNum/rateDen` (floor-truncated integer accounting).
    Units: resource units. Domain: `rateDen > 0`. -/
def taxRevenue (base rateNum rateDen : Nat) (_hden : rateDen > 0) : Nat :=
  base * rateNum / rateDen

/-- Tax ledger identity: revenue cannot exceed the base when the rate is at most 1.
    Units: resource units. Domain: `rateDen > 0`, `rateNum ≤ rateDen`. -/
theorem tax_revenue_le_base (base rateNum rateDen : Nat) (_hden : rateDen > 0)
    (hrate : rateNum ≤ rateDen) :
    taxRevenue base rateNum rateDen _hden ≤ base := by
  unfold taxRevenue
  have h1 : base * rateNum ≤ base * rateDen := Nat.mul_le_mul_left base hrate
  have h2 : base * rateNum / rateDen ≤ base * rateDen / rateDen :=
    Nat.div_le_div_right h1
  rw [Nat.mul_div_left base _hden] at h2
  exact h2

/-- **Seat-share denominator identity.** `seats = max 1 (round(share·N))` is always at least
    one seat, for any share numerator and any cohort size, given a positive share denominator.
    Units: seats (`Nat`). Domain: `shareDen > 0`. -/
theorem seat_count_positive (shareNum shareDen cohortSize : Nat) (_hden : shareDen > 0) :
    0 < seatCount shareNum shareDen cohortSize _hden := by
  unfold seatCount
  exact Nat.lt_of_lt_of_le Nat.zero_lt_one (Nat.le_max_left _ _)

/-! ## 2. Prep-stock recursion `prep_t = (1-ρ) prep_{t-1} + e_t` -/

/-- One prep-stock step. Units: stock units (`Int`). `retention` is the integer retention
    multiplier (in the physical model `(1-ρ)` as a rational; integer encoding here keeps the
    algebra exact and is extended to `Rat`/`ℝ` in Tier 1b). `inflow` is the period's
    additions in stock units. -/
def prepStep (retention inflow stock : Int) : Int :=
  retention * stock + inflow

/-- Prep-stock recursion over chronological inflows. Units: stock units (`Int`). -/
def prepRec (retention initial : Int) : List Int → Int
  | [] => initial
  | inflow :: rest => prepRec retention (prepStep retention inflow initial) rest

/-- Weighted geometric sum of inflows: `Σ_i inflow_i · retention^(n−1−i)`. -/
def inflowGeomSum (retention : Int) : List Int → Int
  | [] => 0
  | inflow :: rest => inflow * retention ^ rest.length + inflowGeomSum retention rest

/-- **Prep-stock closed-form identity.**
    `prep_n = retention^n · prep_0 + Σ_{i<n} inflow_i · retention^(n−1−i)`.
    Units: stock units (`Int`). Domain: any integer retention (incl. 0 and negative),
    any finite inflow list. -/
theorem prep_recursion_closed_form (retention initial : Int) (inflows : List Int) :
    prepRec retention initial inflows
      = initial * retention ^ inflows.length + inflowGeomSum retention inflows := by
  induction inflows generalizing initial with
  | nil => simp [prepRec, inflowGeomSum]
  | cons inflow rest ih =>
      show prepRec retention (prepStep retention inflow initial) rest
        = initial * retention ^ (rest.length + 1)
          + (inflow * retention ^ rest.length + inflowGeomSum retention rest)
      rw [ih (prepStep retention inflow initial)]
      unfold prepStep
      rw [Int.pow_succ', Int.add_mul]
      ac_rfl

end Atlas
