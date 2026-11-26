/-! Shared definitions for the Angkor formalizations. Core Lean only, exact rationals. -/
namespace Angkor

/-- `Math.max(a, Math.min(b, x))`, matching the JavaScript engines. -/
def clamp (x a b : Rat) : Rat := max a (min b x)

theorem clamp_lower (x a b : Rat) : a ≤ clamp x a b := by
  unfold clamp; grind

theorem clamp_upper (x a b : Rat) (h : a ≤ b) : clamp x a b ≤ b := by
  unfold clamp; grind

end Angkor
