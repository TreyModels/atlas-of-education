import Atlas.Definitions

/-!
# Finite Plackett–Luce prototype (Lean 4 core, two-candidate case)

Semantics. With candidate weights `w0,w1`, the top-1 Plackett–Luce selection probabilities
are `w0/(w0+w1)` and `w1/(w0+w1)`. We encode the numerators over the common denominator
`D = w0+w1`; the statement `Σ_i P_i = min(1, 2) = 1` therefore becomes
`numerator_a + numerator_b = D`. For top-K with `K ≥ 2 = |candidates|`, both candidates are
selected with probability 1, so `Σ_i P_i = min(K,2) = 2` becomes the indicator sum `= 2`.

The general-`n` version (`Σ_seats P_i = min(seats, |candidates|)` for arbitrary finite
candidate sets, monotonicity/symmetry, subset-DP ↔ closed form) is Tier 2 in
`docs/audit/LEAN_VERIFICATION_SCOPE.md`; this file is the compiling Tier-2 seed.
-/


namespace Atlas

/-- Common denominator of the two-candidate PL probabilities. Units: weight units. -/
def plDenom (w : PLWeights) : Nat := w.w0 + w.w1

/-- Integer-scaled top-1 selection numerator for a candidate (units: weight units). -/
def top1Numerator (w : PLWeights) : Cand → Nat
  | .a => w.w0
  | .b => w.w1

/-- **Finite PL identity (top-1, n = 2):** `Σ_i P_i = min(1, 2) = 1` in integer-scaled
    encoding: the numerators sum to the common denominator. Units: weight units. Domain:
    any Nat weights (the positive-total hypothesis only matters for the rational reading,
    not for this identity). -/
theorem pl_top1_sum_eq_denom (w : PLWeights) :
    top1Numerator w .a + top1Numerator w .b = plDenom w := rfl

/-- Same identity written against `min(seats, candidates)`: with `seats = 1` the sum of
    selection numerators is `min 1 2 = 1` times the denominator. -/
theorem pl_top1_sum_eq_min (w : PLWeights) :
    top1Numerator w .a + top1Numerator w .b = plDenom w * min 1 2 := by
  rw [pl_top1_sum_eq_denom]
  simp [plDenom]

/-- Selected-indicator for top-K selection (1 if the candidate is admitted). For `K ≥ n`
    every candidate is admitted, so the indicator is 1. -/
def topKSelectedIndicator (k : Nat) : Cand → Nat
  | _ => if 1 ≤ k then 1 else 0

/-- **Finite PL identity (top-K, n = 2, K ≥ 2):** `Σ_i P_i = min(K, 2) = 2`. Units:
    probability mass units (indicator sum). Domain: `2 ≤ K`. -/
theorem pl_topK_selected_sum (k : Nat) (hk : 2 ≤ k) :
    topKSelectedIndicator k .a + topKSelectedIndicator k .b = min k 2 := by
  have hk1 : 1 ≤ k := Nat.le_trans (by decide : 1 ≤ 2) hk
  simp [topKSelectedIndicator, hk1, Nat.min_eq_right hk]

/-! ### Computational checks (exact small-case evaluation; Tier-2 "small n" evidence) -/

/-- Concrete top-1 evaluation for weights `(2,3)`: `2/(2+3) + 3/(2+3) = 1`. -/
example : top1Numerator ⟨2, 3⟩ .a + top1Numerator ⟨2, 3⟩ .b = plDenom ⟨2, 3⟩ := by
  decide

/-- Concrete top-2 evaluation for weights `(2,3)`: both admitted, sum of indicators = 2. -/
example : topKSelectedIndicator 2 .a + topKSelectedIndicator 2 .b = 2 := by
  decide

end Atlas
