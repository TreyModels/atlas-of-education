/-!
# Codex staged-plan model: learning, requirements, accounting, rank, counterexamples

This file implements the Codex guidance recorded in `docs/audit/LEAN_VERIFICATION_SCOPE.md` §3:
pin the model objects and domains, formalise achieved learning `A` and required proficiency `R`
(fixed threshold vs endogenous rank), the gap `max(0, R−A)`, capacity/seat acceptance, source
accounting (no double-booked time), a deterministic rank with an explicit tie rule, and the
conditional invariants / counterexamples that the guidance asks for.

**Scope warning (binding):** these are statements about an *exact integer encoding of selected
mechanisms*, not a verification of the 183 inventory equations, the Python engine, or its
floating-point runtime. See the scope document's Tier-3 limits.
-/
namespace Atlas.Model

/-! ## 1. Achieved learning, required proficiency, and the gap -/

/-- A learning state: `achieved` learning and `required` proficiency. Units: score points. -/
structure Learning where
  achieved : Nat
  required : Nat
deriving Repr, DecidableEq

/-- Requirement regimes: a fixed threshold, or an endogenous rank requirement with `seats`. -/
inductive Requirement where
  | fixed (cutoff : Nat)
  | rank (seats : Nat)
deriving Repr, DecidableEq

/-- Numeric cutoff for a fixed requirement; the `rank` regime has no fixed cutoff and returns `0`
    as a documented sentinel (rank comparisons use `outranks`, below). -/
def Requirement.cutoff : Requirement → Nat
  | .fixed c => c
  | .rank _ => 0

/-- `gap = max(0, R − A)`; on `Nat`, subtraction already truncates at zero. Units: score points. -/
def gap (achieved required : Nat) : Nat := required - achieved

theorem gap_nonneg (achieved required : Nat) : 0 ≤ gap achieved required :=
  Nat.zero_le _

theorem gap_eq_zero_iff_met (achieved required : Nat) :
    gap achieved required = 0 ↔ required ≤ achieved := by
  unfold gap
  exact Nat.sub_eq_zero_iff_le

theorem gap_pos_iff_shortfall (achieved required : Nat) :
    0 < gap achieved required ↔ achieved < required := by
  unfold gap
  exact Nat.sub_pos_iff_lt

/-! ## 2. Capacity, seats, and acceptance -/

/-- Accepted pupils under fixed seat capacity: `min applicants capacity`, so accepted ≤ capacity
    whenever the capacity is the valid one. Units: pupils. -/
def accepted (applicants capacity : Nat) : Nat := min applicants capacity

/-- **Accepted ≤ valid seat capacity** (the conditional invariant). -/
theorem accepted_le_capacity (applicants capacity : Nat) :
    accepted applicants capacity ≤ capacity :=
  Nat.min_le_right _ _

/-- **Zero additional input ⇒ unchanged increment.** Learning increment between two states; going
    from a state to itself adds nothing. Units: score points. -/
def learningIncrement (pre post : Nat) : Nat := post - pre

theorem zero_extra_input_no_increment (base : Nat) :
    learningIncrement base base = 0 := by
  unfold learningIncrement
  exact Nat.sub_self base

/-! ## 3. Source accounting and additivity (no double-booked time/input) -/

/-- School, private-tutoring and home contributions. Units: input units. -/
structure Sources where
  school : Nat
  privateTutoring : Nat
  home : Nat
deriving Repr, DecidableEq

/-- Total input as a sum — the accounting balance identity. -/
def totalInput (s : Sources) : Nat := s.school + s.privateTutoring + s.home

theorem total_input_eq_sum (s : Sources) :
    totalInput s = s.school + s.privateTutoring + s.home := rfl

/-- Additivity of a source-combination operation: distinct source terms sum **only** under this
    explicit assumption. -/
def Additive (combine : Nat → Nat → Nat) : Prop := ∀ a b, combine a b = a + b

theorem additive_combine_eq_sum (combine : Nat → Nat → Nat) (h : Additive combine) (a b : Nat) :
    combine a b = a + b :=
  h a b

/-- **Counterexample:** `max` is not additive, so "distinct source terms sum" is not automatic. -/
theorem max_not_additive : ¬ Additive Nat.max := by
  intro h
  have hne : Nat.max 1 1 ≠ 1 + 1 := by decide
  exact hne (h 1 1)

/-! ## 4. Time budgets (no double-booked time) -/

/-- Elapsed time = preparation + work + review (the Luna starter identity). Units: time units. -/
def timeUsed (preparation work review : Nat) : Nat := preparation + work + review

/-- A budget is respected when total time does not exceed it. -/
def respectsBudget (preparation work review budget : Nat) : Prop :=
  timeUsed preparation work review ≤ budget

/-- **Conditional invariant:** if the budget is respected, every component fits within it. -/
theorem budget_implies_component (preparation work review budget : Nat)
    (h : respectsBudget preparation work review budget) : preparation ≤ budget := by
  unfold respectsBudget timeUsed at h
  exact Nat.le_trans
    (Nat.le_trans (Nat.le_add_right preparation work)
      (Nat.le_add_right (preparation + work) review)) h

/-- No double-booking: the accounting identity for time, as a proved equality. -/
theorem time_accounting_identity (preparation work review : Nat) :
    timeUsed preparation work review = preparation + work + review := rfl

/-! ## 5. Deterministic rank with an explicit tie rule -/

/-- Deterministic outranking: strictly higher score, or an exact tie broken by a stable id
    (`myTie < otherTie`). This makes the tie rule explicit (no silent tie assumption).
    Scores are `Nat` points (the common shift below is nonnegative; negative shifts are outside
    the pinned domain and are flagged in the scope document). -/
def outranks (myScore otherScore : Nat) (myTie otherTie : Nat) : Prop :=
  myScore > otherScore ∨ (myScore = otherScore ∧ myTie < otherTie)

/-- Decidable (Bool) rendering of `outranks`, used by the differential-test witness. -/
def outranksBool (myScore otherScore myTie otherTie : Nat) : Bool :=
  decide (myScore > otherScore ∨ (myScore = otherScore ∧ myTie < otherTie))

/-- The Bool rendering computes the same relation as `outranks`. -/
theorem outranksBool_eq_true_iff (myScore otherScore myTie otherTie : Nat) :
    outranksBool myScore otherScore myTie otherTie = true ↔
      outranks myScore otherScore myTie otherTie := by
  unfold outranksBool outranks
  simp

/-- **Rank invariance to common score shifts** for the deterministic rank with the tie rule:
    adding the same constant `c` to all scores leaves the outranking relation unchanged
    (including ties). -/
theorem rank_invariant_under_common_shift (myScore otherScore myTie otherTie c : Nat) :
    outranks (myScore + c) (otherScore + c) myTie otherTie ↔
      outranks myScore otherScore myTie otherTie := by
  unfold outranks
  simp only [Nat.add_lt_add_iff_right, Nat.add_right_cancel_iff]

/-- **Counterexample (fixed-seat relative rank):** with a fixed capacity of one seat, raising
    demand from 1 to 2 does not raise the accepted count — so "more applicants ⇒ more accepted"
    is not a theorem; it needs the fixed-capacity hypothesis and is still only non-strict. -/
theorem fixed_seat_relative_rank_counterexample :
    ∃ applicants, ¬ (accepted applicants 1 < accepted (applicants + 1) 1) := by
  exact ⟨1, by decide⟩

/-- Monotonicity that **does** hold: under a constant capacity, `min` is monotone in demand
    (non-strict). This is the assumption-restricted counterpart of the counterexample. -/
theorem accepted_monotone_fixed_capacity (applicants₁ applicants₂ capacity : Nat)
    (h : applicants₁ ≤ applicants₂) :
    accepted applicants₁ capacity ≤ accepted applicants₂ capacity := by
  unfold accepted
  rw [Nat.le_min]
  exact ⟨Nat.le_trans (Nat.min_le_left _ _) h, Nat.min_le_right _ _⟩

/-! ## 6. Complementarity and feedback-capacity counterexamples -/

/-- Complementarity: learning is `min` of two inputs (one input alone does not help). -/
def complementaryLearning (x y : Nat) : Nat := min x y

/-- **Counterexample (complementarity):** increasing one input alone need not increase learning. -/
theorem complementarity_counterexample :
    ∃ x y, complementaryLearning (x + 1) y ≤ complementaryLearning x y := by
  exact ⟨1, 1, by decide⟩

/-- Feedback capacity: capacity reacts to demand (`seats − 1` once demand exceeds seats). -/
def acceptedWithFeedback (applicants seats : Nat) : Nat :=
  if applicants > seats then min applicants (seats - 1) else min applicants seats

/-- **Counterexample (feedback capacity):** accepted can *fall* when demand rises, because the
    capacity responds; "accepted is monotone in demand" needs capacity exogeneity. -/
theorem feedback_capacity_counterexample :
    ∃ applicants seats,
      acceptedWithFeedback (applicants + 1) seats < acceptedWithFeedback applicants seats := by
  exact ⟨1, 1, by decide⟩

end Atlas.Model
