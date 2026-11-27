import Std

namespace Guangzhou

/-- Each row records admission before and after bonuses for the same pupil. -/
def count (f : α → Bool) (xs : List α) := (xs.filter f).length

theorem seat_balance (xs : List (Bool × Bool)) :
    count Prod.fst xs + count (fun p => !p.1 && p.2) xs =
    count Prod.snd xs + count (fun p => p.1 && !p.2) xs := by
  induction xs with
  | nil => rfl
  | cons p xs ih =>
    obtain ⟨a,b⟩ := p
    cases a <;> cases b <;> simp [count] at * <;> omega

theorem displacement (xs : List (Bool × Bool))
    (capacity : count Prod.fst xs = count Prod.snd xs) :
    count (fun p => !p.1 && p.2) xs = count (fun p => p.1 && !p.2) xs := by
  have h := seat_balance xs
  omega

/-- For the focal pupil, count rivals strictly above its unchanged score.
    Covers cutoff-with-ties: a pupil qualifies iff fewer than k strictly outrank it. -/
def above (s : Int) (rivals : List Int) := count (fun x => decide (s < x)) rivals

theorem rival_bonus (s x b : Int) (others : List Int) (k : Nat) (hb : 0 ≤ b)
    (after : above s ((x+b)::others) < k) : above s (x::others) < k := by
  by_cases h : s < x
  · have h' : s < x+b := by omega
    simpa [above, count, List.filter_cons, h, h'] using
      (show above s ((x+b)::others) < k from after)
  · by_cases h' : s < x+b <;> simp [above, count, h, h'] at * <;> omega

theorem strict_displacement_witness : above 8 [7] < 1 ∧ ¬ above 8 [7+2] < 1 := by decide

/-- Sorting only permutes distinct pupil IDs. Cardinality is independent of the ranking rule. -/
theorem band_size (ranked roster : List Nat) (order : ranked.Perm roster)
    (ids : roster.Nodup) (k : Nat) :
    (ranked.take k).length = min k roster.length ∧ (ranked.take k).Nodup := by
  constructor
  · simp [List.length_take, order.length_eq]
  · exact (order.nodup_iff.mpr ids).sublist (List.take_sublist ..)

/-- Two equally scoring applicants each qualify under a one-seat inclusive cutoff. -/
theorem cutoff_tie : above 8 [8] < 1 ∧ count (fun x : Int => decide (8 ≤ x)) [8,8] > 1 := by decide

end Guangzhou
#print axioms Guangzhou.displacement
#print axioms Guangzhou.rival_bonus
#print axioms Guangzhou.strict_displacement_witness
#print axioms Guangzhou.band_size
#print axioms Guangzhou.cutoff_tie

namespace Guangzhou
/-- All eight pupils have identical latent talent. High score wins.
    Booleans in each group are the observed high-score indicators. -/
def richScores := [true, true, true, false]
def poorScores := [true, false, false, false]

def winRate (scores : List Bool) : Rat :=
  (count id scores : Rat) / (scores.length : Rat)

def scoreStandardized (scores : List Bool) : Rat :=
  (winRate (scores.filter id) + winRate (scores.filter (!·))) / 2

theorem conditioning_witness :
    scoreStandardized richScores / scoreStandardized poorScores = 1 ∧
    winRate richScores / winRate poorScores = 3 := by decide +kernel
end Guangzhou
#print axioms Guangzhou.conditioning_witness
