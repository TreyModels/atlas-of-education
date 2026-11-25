/-! Elementary, purely arithmetic starting points for formal verification.
    All quantities are natural numbers; subtraction is truncated at zero.
    (Luna starter: the leading comment is a module doc comment so the namespace parses.) -/

namespace LeanStarter

/-- The nonnegative gap between a required amount and an achieved amount. -/
def gap (required achieved : Nat) : Nat := Nat.max 0 (required - achieved)

/-- `Nat` subtraction already truncates at zero, so this is the usual positive gap. -/
theorem gap_eq_truncated_sub (required achieved : Nat) :
    gap required achieved = required - achieved := by
  simp [gap]

theorem gap_eq_zero_of_met (required achieved : Nat) (h : required ≤ achieved) :
    gap required achieved = 0 := by
  unfold gap
  exact Nat.sub_eq_zero_of_le h

theorem gap_pos_of_shortfall (required achieved : Nat) (h : achieved < required) :
    0 < gap required achieved := by
  rw [gap_eq_truncated_sub]
  exact Nat.sub_pos_of_lt h

/-- An amount is feasible when it does not exceed available capacity. -/
def Feasible (required capacity : Nat) : Prop := required ≤ capacity

theorem required_within_capacity (required capacity : Nat)
    (h : Feasible required capacity) : required ≤ capacity := h

/-- Remaining capacity after consuming `used` units (for an in-bounds use). -/
def remainingCapacity (capacity used : Nat) : Nat := capacity - used

theorem remaining_capacity_bounded (capacity used : Nat) :
    remainingCapacity capacity used ≤ capacity := by
  simp [remainingCapacity]

theorem used_plus_remaining_eq_capacity (capacity used : Nat) (h : used ≤ capacity) :
    used + remainingCapacity capacity used = capacity := by
  simp [remainingCapacity, Nat.add_sub_of_le h]

/-- Elapsed time as the sum of preparation, work, and review time. -/
def elapsedTime (preparation work review : Nat) : Nat := preparation + work + review

theorem preparation_within_elapsed (preparation work review : Nat) :
    preparation ≤ elapsedTime preparation work review := by
  unfold elapsedTime
  exact Nat.le_trans (Nat.le_add_right preparation work)
    (Nat.le_add_right (preparation + work) review)

theorem work_within_elapsed (preparation work review : Nat) :
    work ≤ elapsedTime preparation work review := by
  unfold elapsedTime
  exact Nat.le_trans (Nat.le_add_left work preparation)
    (Nat.le_add_right (preparation + work) review)

theorem review_within_elapsed (preparation work review : Nat) :
    review ≤ elapsedTime preparation work review := by
  unfold elapsedTime
  exact Nat.le_add_left review (preparation + work)

end LeanStarter
