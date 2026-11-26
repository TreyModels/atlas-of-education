/-!
# Angkor provisioning engine

Formalizes `public/engines/provisioning.js` (30 lines, Klassen, Ortman, Lobo & Evans, Table 5).
The coefficients are normalized associations, not grain tonnes.

Modeling notes:

* Exact rational arithmetic (`Rat`). Constants are exact: `.023` is `23/1000`. Theorems are about
  ideal rational arithmetic, not IEEE floating point.
* The source uses real powers `x ** e`. Core Lean has no reals, and `Rat` is not closed under real
  powers (for example `(1/2 : Rat) ^ (1/2)` is irrational), so no faithful `Rat`-valued power
  function exists. The power function is therefore a parameter `P : PowerLaw`, a structure holding
  `pow : Rat → Rat → Rat` together with only the laws used below. These laws are structure fields,
  not axioms. Every power-dependent theorem is conditional on an arbitrary `P : PowerLaw`.
* Non-vacuity: `PowerLaw.trivial` (every power is 1) satisfies all four laws. It is lawful but not
  faithful. Under it every index is 100, so the monotonicity theorems hold only in their
  non-strict form. Strict monotonicity needs a genuine power law, which `Rat` cannot supply.
* Division: `communityCount` divides by `community`. Lean returns 0 when `community = 0`, while the
  JavaScript returns `Infinity`. The count identity is proved only under `community ≠ 0`.
  The other divisions have literal nonzero denominators (`/ 100`, `/ 10`).
* The period table uses `Nat` (years, population counts, km²), which is exact for integer data.
* `scaling` is a string in JS. Every value other than `'linear'` or `'theory'` falls through to
  `'fitted'`. The `Scaling` enum models the three reachable cases.
* Not formalized: the display curves `sizeCurve` and `distanceCurve` (tabulations of the same
  formulas), `platformElasticity` (unused by `run`), and the `scope` text. The source makes no
  claim about food budget, famine relief, growth dynamics or collapse, and neither does this file.
-/

namespace Angkor.Provisioning

/-- Real-power stand-in. The laws are those the theorems need, for positive bases. -/
structure PowerLaw where
  pow : Rat → Rat → Rat
  /-- `x ** 0 = 1` for `x > 0`. -/
  pow_zero : ∀ x : Rat, 0 < x → pow x 0 = 1
  /-- `1 ** e = 1`. -/
  one_pow : ∀ e : Rat, pow 1 e = 1
  /-- For a nonnegative exponent, `x ** e` is nondecreasing in a positive base. -/
  mono_pos_exp : ∀ x y e : Rat, 0 < x → x ≤ y → 0 ≤ e → pow x e ≤ pow y e
  /-- For a nonpositive exponent, `x ** e` is nonincreasing in a positive base. -/
  anti_neg_exp : ∀ x y e : Rat, 0 < x → x ≤ y → e ≤ 0 → pow y e ≤ pow x e

/-- Every power is 1. Lawful, but not a faithful model of real powers (see module doc). -/
def PowerLaw.trivial : PowerLaw where
  pow _ _ := 1
  pow_zero _ _ := rfl
  one_pow _ := rfl
  mono_pos_exp _ _ _ _ _ _ := Rat.le_refl
  anti_neg_exp _ _ _ _ _ _ := Rat.le_refl

/-- provisioning.js line 4: `coefficients`, exact values. -/
structure Coefficients where
  beta : Rat
  betaSE : Rat
  outputDistance : Rat
  waterDistance : Rat
  areaDistance : Rat
  platformElasticity : Rat

/-- provisioning.js line 4. Exact decimals: `1.227 = 1227/1000`, `-.846 = -846/1000`, and so on. -/
def coefficients : Coefficients where
  beta := 1227 / 1000
  betaSE := 23 / 1000
  outputDistance := -846 / 1000
  waterDistance := -409 / 1000
  areaDistance := 521 / 1000
  platformElasticity := 85 / 1000

/-- provisioning.js line 13: default community size. -/
def defaultCommunity : Rat := 500

/-- provisioning.js line 13: default distance. -/
def defaultDistance : Rat := 10

/-- provisioning.js line 17: fixed population for the regrouping calculation. -/
def population : Rat := 10000

/-- provisioning.js line 13 default `'fitted'`, and the branches on line 16. Any other source
string falls through to `'fitted'`. -/
inductive Scaling where
  | fitted
  | linear
  | theory
  deriving DecidableEq

/-- provisioning.js line 16: `beta` by scaling option. -/
def betaOf : Scaling → Rat
  | .fitted => coefficients.beta
  | .linear => 1
  | .theory => 7 / 6

/-- provisioning.js line 18: `scale n = 100 * (n/100) ** (beta - 1)`. Meaningful for `0 < n`. -/
def scaleIndex (P : PowerLaw) (beta n : Rat) : Rat :=
  100 * P.pow (n / 100) (beta - 1)

/-- provisioning.js line 22: `perPersonIndex = scale(community)`. -/
def perPersonIndex (P : PowerLaw) (s : Scaling) (community : Rat) : Rat :=
  scaleIndex P (betaOf s) community

/-- provisioning.js line 22: `totalIndex = scale(controls.community)`. The source does not use
the population argument, so it is taken and ignored here. -/
def totalIndex (P : PowerLaw) (s : Scaling) (_pop community : Rat) : Rat :=
  scaleIndex P (betaOf s) community

/-- provisioning.js line 21: `population / community`. Division by zero gives 0 in Lean. -/
def communityCount (community : Rat) : Rat := population / community

/-- provisioning.js lines 23-25: `100 * (d/10) ** k`. -/
def distanceIndex (P : PowerLaw) (d e : Rat) : Rat := 100 * P.pow (d / 10) e

/-- provisioning.js line 23: output index at distance `d`. -/
def distanceOutput (P : PowerLaw) (d : Rat) : Rat :=
  distanceIndex P d coefficients.outputDistance

/-- provisioning.js line 24: water index at distance `d`. -/
def distanceWater (P : PowerLaw) (d : Rat) : Rat :=
  distanceIndex P d coefficients.waterDistance

/-- provisioning.js line 25: area index at distance `d`. -/
def distanceArea (P : PowerLaw) (d : Rat) : Rat :=
  distanceIndex P d coefficients.areaDistance

/-- provisioning.js lines 5-12: one row of the period table. Years, counts and km² are `Nat`.
Field names: `begin` becomes `startYear`, `end` becomes `endYear`, and `population` becomes
`people` to avoid clashing with the `population` constant. -/
structure Period where
  startYear : Nat
  endYear : Nat
  communities : Nat
  people : Nat
  areaKm2 : Nat
  deriving Repr, DecidableEq

/-- provisioning.js lines 5-12, row for row. -/
def periods : List Period :=
  [ ⟨770, 906, 93, 24894, 1327⟩
  , ⟨907, 961, 192, 55062, 1321⟩
  , ⟨962, 1001, 380, 136912, 1279⟩
  , ⟨1002, 1113, 511, 184275, 1244⟩
  , ⟨1114, 1180, 568, 209357, 1323⟩
  , ⟨1181, 1308, 571, 213521, 1323⟩ ]

/-- Adjacent pairs of the period table. -/
def periodPairs : List (Period × Period) := periods.zip periods.tail

/-! ## Scale index -/

/-- Target 1 helper: the scale index is 100 at `beta = 1` for every positive `n`. -/
theorem linear_scale_const (P : PowerLaw) {n : Rat} (hn : 0 < n) :
    scaleIndex P 1 n = 100 := by
  unfold scaleIndex
  rw [show (1 : Rat) - 1 = 0 by grind, P.pow_zero _ (by grind)]
  grind

/-- Target 1: with linear scaling, the per-person index is 100 for every positive community
size, so it does not depend on community size. -/
theorem linear_perPerson_const (P : PowerLaw) {c : Rat} (hc : 0 < c) :
    perPersonIndex P .linear c = 100 :=
  linear_scale_const P hc

/-- Target 1: with linear scaling, the total index is 100 for every positive community size
and every population, so it does not depend on community size. -/
theorem linear_total_const (P : PowerLaw) (p : Rat) {c : Rat} (hc : 0 < c) :
    totalIndex P .linear p c = 100 :=
  linear_scale_const P hc

/-- Target 2: the scale index is 100 at `n = 100` for every `beta`. -/
theorem scale_at_100 (P : PowerLaw) (beta : Rat) :
    scaleIndex P beta 100 = 100 := by
  unfold scaleIndex
  rw [show (100 : Rat) / 100 = 1 by grind, P.one_pow]
  grind

/-- Target 2: the three distance indices equal 100 at distance 10, for every power law. -/
theorem distances_at_10 (P : PowerLaw) :
    distanceOutput P 10 = 100 ∧ distanceWater P 10 = 100 ∧ distanceArea P 10 = 100 := by
  unfold distanceOutput distanceWater distanceArea distanceIndex
  rw [show (10 : Rat) / 10 = 1 by grind, P.one_pow, P.one_pow, P.one_pow]
  grind

/-- Helper for target 3: with a nonnegative exponent `beta - 1`, the scale index is nondecreasing
in community size. -/
theorem scale_mono_of_one_le (P : PowerLaw) {beta n m : Rat} (hbeta : 1 ≤ beta)
    (hn : 0 < n) (hnm : n ≤ m) :
    scaleIndex P beta n ≤ scaleIndex P beta m := by
  unfold scaleIndex
  have h1 : 0 < n / 100 := by grind
  have h2 : n / 100 ≤ m / 100 := by grind
  have h3 := P.mono_pos_exp (n / 100) (m / 100) (beta - 1) h1 h2 (by grind)
  grind

/-- Target 3: fitted scaling (`beta = 1.227`) makes the scale index monotone in community size. -/
theorem fitted_scale_mono (P : PowerLaw) {n m : Rat} (hn : 0 < n) (hnm : n ≤ m) :
    scaleIndex P (betaOf .fitted) n ≤ scaleIndex P (betaOf .fitted) m :=
  scale_mono_of_one_le P (by unfold betaOf coefficients; grind) hn hnm

/-- Target 3: theory scaling (`beta = 7/6`) makes the scale index monotone in community size. -/
theorem theory_scale_mono (P : PowerLaw) {n m : Rat} (hn : 0 < n) (hnm : n ≤ m) :
    scaleIndex P (betaOf .theory) n ≤ scaleIndex P (betaOf .theory) m :=
  scale_mono_of_one_le P (by unfold betaOf; grind) hn hnm

/-! ## Distance indices -/

/-- Helper for target 3: a nonpositive distance exponent makes the index nonincreasing in
distance (positive distances). -/
theorem distanceIndex_anti (P : PowerLaw) {d₁ d₂ e : Rat} (hd : 0 < d₁) (h12 : d₁ ≤ d₂)
    (he : e ≤ 0) :
    distanceIndex P d₂ e ≤ distanceIndex P d₁ e := by
  unfold distanceIndex
  have h1 : 0 < d₁ / 10 := by grind
  have h2 : d₁ / 10 ≤ d₂ / 10 := by grind
  have h3 := P.anti_neg_exp (d₁ / 10) (d₂ / 10) e h1 h2 he
  grind

/-- Helper for target 3: a nonnegative distance exponent makes the index nondecreasing in
distance (positive distances). -/
theorem distanceIndex_mono (P : PowerLaw) {d₁ d₂ e : Rat} (hd : 0 < d₁) (h12 : d₁ ≤ d₂)
    (he : 0 ≤ e) :
    distanceIndex P d₁ e ≤ distanceIndex P d₂ e := by
  unfold distanceIndex
  have h1 : 0 < d₁ / 10 := by grind
  have h2 : d₁ / 10 ≤ d₂ / 10 := by grind
  have h3 := P.mono_pos_exp (d₁ / 10) (d₂ / 10) e h1 h2 he
  grind

/-- Target 3: the output index decreases with distance. The exponent `-.846` is negative. -/
theorem output_decreasing (P : PowerLaw) {d₁ d₂ : Rat} (hd : 0 < d₁) (h12 : d₁ ≤ d₂) :
    distanceOutput P d₂ ≤ distanceOutput P d₁ :=
  distanceIndex_anti P hd h12 (by unfold coefficients; grind)

/-- Target 3: the water index decreases with distance. The exponent `-.409` is negative. -/
theorem water_decreasing (P : PowerLaw) {d₁ d₂ : Rat} (hd : 0 < d₁) (h12 : d₁ ≤ d₂) :
    distanceWater P d₂ ≤ distanceWater P d₁ :=
  distanceIndex_anti P hd h12 (by unfold coefficients; grind)

/-- Target 3: the area index increases with distance. The exponent `.521` is positive. -/
theorem area_increasing (P : PowerLaw) {d₁ d₂ : Rat} (hd : 0 < d₁) (h12 : d₁ ≤ d₂) :
    distanceArea P d₁ ≤ distanceArea P d₂ :=
  distanceIndex_mono P hd h12 (by unfold coefficients; grind)

/-! ## Total and per-person index -/

/-- Target 4: in the source, `totalIndex` is identical to `perPersonIndex`. -/
theorem total_eq_perPerson (P : PowerLaw) (s : Scaling) (p c : Rat) :
    totalIndex P s p c = perPersonIndex P s c :=
  rfl

/-- Target 4, meaning at fixed population: `totalIndex` does not depend on population at all.
Two populations give the same value, so the "total" index is a per-community index. -/
theorem total_independent_of_population (P : PowerLaw) (s : Scaling) (p q c : Rat) :
    totalIndex P s p c = totalIndex P s q c :=
  rfl

/-! ## Community count -/

/-- Target 5: `community * communityCount = population` whenever `community ≠ 0`. -/
theorem community_mul_count (c : Rat) (hc : c ≠ 0) :
    c * communityCount c = population := by
  unfold communityCount
  grind

/-! ## Period table -/

/-- Target 6: each period starts no later than it ends. -/
theorem periods_ordered : ∀ p ∈ periods, p.startYear ≤ p.endYear := by
  decide

/-- Target 6: each period begins the year after the previous one ends (contiguous). -/
theorem periods_contiguous : ∀ pq ∈ periodPairs, pq.2.startYear = pq.1.endYear + 1 := by
  decide

/-- Target 6: periods do not overlap (each ends before the next starts). -/
theorem periods_nonoverlap : ∀ pq ∈ periodPairs, pq.1.endYear < pq.2.startYear := by
  decide

/-- Target 6: the community count strictly increases over the periods. -/
theorem communities_increasing : ∀ pq ∈ periodPairs, pq.1.communities < pq.2.communities := by
  decide

/-- Target 6: the population strictly increases over the periods. -/
theorem people_increasing : ∀ pq ∈ periodPairs, pq.1.people < pq.2.people := by
  decide

/-- Target 6: area is not nondecreasing over the periods (1327 to 1321 drops). -/
theorem area_not_nondecreasing : ¬ ∀ pq ∈ periodPairs, pq.1.areaKm2 ≤ pq.2.areaKm2 := by
  decide

/-- Target 6: area is not nonincreasing over the periods (1244 to 1323 rises). -/
theorem area_not_nonincreasing : ¬ ∀ pq ∈ periodPairs, pq.2.areaKm2 ≤ pq.1.areaKm2 := by
  decide

/-! ## Beta standard error -/

/-- Target 7, positive half: with `k = 9`, `1.227 - 9 * .023 = 1.020 > 1`. -/
theorem coefficients_beta : coefficients.beta = 1227 / 1000 := rfl

theorem coefficients_betaSE : coefficients.betaSE = 23 / 1000 := rfl

theorem betaSE_nine_holds : 1 < coefficients.beta - (9 : Rat) * coefficients.betaSE := by
  rw [coefficients_beta, coefficients_betaSE]
  grind

/-- Target 7, both directions: `1 < 1.227 - k * .023` holds exactly for `k ≤ 9`, so 9 is the
largest natural number for which it holds. Since `10 * .023 = .230 > .227`, the value at `k = 10`
is `.997`. -/
theorem betaSE_iff_le_nine (k : Nat) :
    1 < coefficients.beta - (k : Rat) * coefficients.betaSE ↔ k ≤ 9 := by
  rw [coefficients_beta, coefficients_betaSE]
  constructor
  · intro h
    cases Nat.lt_or_ge k 10 with
    | inl hk => omega
    | inr hk =>
      exfalso
      have h10 : (10 : Rat) ≤ (k : Rat) := by exact_mod_cast hk
      grind
  · intro hk
    have hk' : (k : Rat) ≤ 9 := by exact_mod_cast hk
    grind

end Angkor.Provisioning
