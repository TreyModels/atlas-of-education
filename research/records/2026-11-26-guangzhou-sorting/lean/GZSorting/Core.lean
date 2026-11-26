/-!
# GZSorting.Core: tutoring hours, skill at 15, gates, senior-2 re-banding, pre-gate ban knockout

Sources:
* `/home/claude/sig/gz_talent.py`: skill at 15 (lines 25-26), academic gate (line 28), top band
  (lines 31-36), skill at 16 (line 39), senior-2 re-banding (line 41).
* `/home/claude/sig/gz_system.py`: pre-gate tutoring and ban (lines 67-73), post-gate window
  (line 103), tutoring hours (line 106), zeroing below one hour (line 110).

Fidelity and scope:
* Values are `Rat`. Theorems are about exact rational arithmetic, not IEEE floating point.
* Non-rational operations enter as arguments. `sq` stands for `np.sqrt` in gz_system.py line 73.
  Quantile cutoffs (`np.quantile`, gz_talent.py lines 28, 35, 41) enter as `Rat` arguments. Nothing
  here shows that a quantile gives the stated share of pupils. Random draws (`rng.normal`,
  `rng.random`) are absorbed into arguments such as `base`, `talent` and `obs`. No distributional
  claim is made.
* Python `zk >= line` becomes `line <= score`. Gates are `Prop`s. The band indicator used in
  `skill16` is a `Rat` equal to 1 or 0, standing for Python's boolean times `CLASS_EFF`.
* `np.minimum` is `ratMin`, defined as `if a <= b then a else b`.
* No division occurs in this file.
* The source's `skill16` contains a `POST_TUT * logw` term (gz_talent.py line 39). It is kept
  throughout. The "gap equals (1 - decay)*(head1 - head2)" statement is proved separately with
  `postTut` set to 0 (`skill16_gap_no_postTut`).
-/

namespace GZSorting

/-- Minimum of two rationals, `if a <= b then a else b`. Stands for `np.minimum` in
gz_system.py line 106. -/
def ratMin (a b : Rat) : Rat := if a ≤ b then a else b

/-- Tutoring hours `T = min(min(want, window), afford)`, from gz_system.py line 106
(`np.minimum.reduce([want_post, window, afford_post])`). `window` is the output of the
window line 103: `WEEKEND_HRS` for boarders and `EVENING_HRS` for day pupils. -/
def tutorHours (window want afford : Rat) : Rat := ratMin (ratMin want window) afford

/-- Zeroing below one hour, from gz_system.py line 110 (`T[T < 1] = 0.0`). -/
def zeroBelow1 (T : Rat) : Rat := if T < 1 then 0 else T

/-- Head start before grade 15, from gz_talent.py line 25:
`ZONE_TEACH*zone + HOME*logw + PRE_TUT*logw`. The `PRE_TUT` term is kept, as in the source. -/
def headStart (zoneTeach home preTutCoef zone logw : Rat) : Rat :=
  zoneTeach * zone + home * logw + preTutCoef * logw

/-- Skill at 15, from gz_talent.py line 26: `talent + head`. -/
def skill15 (talent zoneTeach home preTutCoef zone logw : Rat) : Rat :=
  talent + headStart zoneTeach home preTutCoef zone logw

/-- Academic-track gate, from gz_talent.py line 28: `zk >= np.quantile(zk, 1 - ACAD)`. The
quantile is passed in as `line`. -/
def academic (score line : Rat) : Prop := line ≤ score

/-- Top-band gate inside a school tier, from gz_talent.py lines 31-35:
`score >= np.quantile(score, 1 - TOP_BAND)` within the tier. The within-tier quantile is passed
in as `cutoff`. -/
def topBand (score cutoff : Rat) : Prop := cutoff ≤ score

/-- Skill at 16, from gz_talent.py line 39:
`tal + (1 - DECAY)*head + GROW*tal + school + band1*CLASS_EFF + POST_TUT*logw`.
`school` is `tier * SCHOOL_EFF` (line 38). `band` is the entry top-band indicator, 1 or 0. -/
def skill16 (tal headStart decay grow school band classEff postTut logw : Rat) : Rat :=
  tal + (1 - decay) * headStart + grow * tal + school + band * classEff + postTut * logw

/-- Senior-2 band, from gz_talent.py line 41: `bands(obs16, acad) if REBAND else band1`. The
top-band test among academic pupils is `cutoff <= obs`. `reband` is the REBAND flag. -/
def band2 (reband : Bool) (cutoff obs : Rat) (band1 : Bool) : Bool :=
  if reband then decide (cutoff ≤ obs) else band1

/-- Pre-gate tutoring hours after the ban, from gz_system.py lines 70-72:
`pre = min(...)`, then `pre * (LEGAL + (1 - LEGAL)*(1 - ENFORCE))` if the ban is on. `pre0`
is the unbanned value from line 70. -/
def preTutHours (ban : Bool) (legal enforce pre0 : Rat) : Rat :=
  if ban then pre0 * (legal + (1 - legal) * (1 - enforce)) else pre0

/-- Zhongkao score, from gz_system.py line 73:
`zk = base + EARLY_EFF * sqrt(pre) + noise`. `base` stands for
`apt - MINBAN_PEN*(~hukou) + ZONE_G*zone + noise`. `sq` stands for `np.sqrt`. -/
def zhongkaoScore (sq : Rat → Rat) (base earlyEff pre : Rat) : Rat :=
  base + earlyEff * sq pre

/-! ### Helper lemmas for `ratMin` and `zeroBelow1` -/

theorem ratMin_le_left (a b : Rat) : ratMin a b ≤ a := by
  unfold ratMin
  split <;> grind

theorem ratMin_le_right (a b : Rat) : ratMin a b ≤ b := by
  unfold ratMin
  split <;> grind

theorem ratMin_nonneg (a b : Rat) (ha : 0 ≤ a) (hb : 0 ≤ b) : 0 ≤ ratMin a b := by
  unfold ratMin
  split <;> grind

/-- `ratMin` is non-decreasing in its first argument. -/
theorem ratMin_mono_arg1 (x1 x2 b : Rat) (h : x1 ≤ x2) : ratMin x1 b ≤ ratMin x2 b := by
  unfold ratMin
  split <;> split <;> grind

/-- `ratMin` is non-decreasing in its second argument. -/
theorem ratMin_mono_arg2 (a w1 w2 : Rat) (h : w1 ≤ w2) : ratMin a w1 ≤ ratMin a w2 := by
  unfold ratMin
  split <;> split <;> grind

/-- `zeroBelow1` is non-decreasing. -/
theorem zeroBelow1_mono (x y : Rat) (h : x ≤ y) : zeroBelow1 x ≤ zeroBelow1 y := by
  unfold zeroBelow1
  split <;> split <;> grind

/-! ### 1. Tutoring hours -/

/-- Hours never exceed the window: `T <= window`. -/
theorem tutor_le_window (window want afford : Rat) : tutorHours window want afford ≤ window := by
  have h1 := ratMin_le_left (ratMin want window) afford
  have h2 := ratMin_le_right want window
  unfold tutorHours
  grind

/-- Zero window, zero hours. If the window is 0 and the wanted and affordable hours are
non-negative, tutoring is 0 hours. -/
theorem tutor_zero_window (want afford : Rat) (hw : 0 ≤ want) (ha : 0 ≤ afford) :
    tutorHours 0 want afford = 0 := by
  have hle := tutor_le_window 0 want afford
  have hnn : 0 ≤ tutorHours 0 want afford := by
    unfold tutorHours
    exact ratMin_nonneg (ratMin want 0) afford (ratMin_nonneg want 0 hw (by grind)) ha
  grind

/-- Closing the window cannot raise tutoring: `T` is non-decreasing in `window`, before zeroing. -/
theorem tutor_mono_window (w1 w2 want afford : Rat) (h : w1 ≤ w2) :
    tutorHours w1 want afford ≤ tutorHours w2 want afford := by
  unfold tutorHours
  exact ratMin_mono_arg1 (ratMin want w1) (ratMin want w2) afford (ratMin_mono_arg2 want w1 w2 h)

/-- Closing the window cannot raise tutoring after the one-hour zeroing rule. -/
theorem tutor_zeroed_mono_window (w1 w2 want afford : Rat) (h : w1 ≤ w2) :
    zeroBelow1 (tutorHours w1 want afford) ≤ zeroBelow1 (tutorHours w2 want afford) :=
  zeroBelow1_mono _ _ (tutor_mono_window w1 w2 want afford h)

/-- After zeroing, tutoring is still at most the window, provided the window is non-negative. -/
theorem tutor_zeroed_le_window (window want afford : Rat) (hw : 0 ≤ window) :
    zeroBelow1 (tutorHours window want afford) ≤ window := by
  have h := tutor_le_window window want afford
  unfold zeroBelow1
  split <;> grind

/-- One-hour rule: if the window is shorter than one hour, the zeroed tutoring hours are 0. -/
theorem tutor_zero_below_one (window want afford : Rat) (hw : window < 1) :
    zeroBelow1 (tutorHours window want afford) = 0 := by
  have h := tutor_le_window window want afford
  unfold zeroBelow1
  split
  · rfl
  · grind

/-! ### 2. Skill at 15 and wealth -/

/-- With zone teacher, home and pre-gate tutoring effects all 0, two pupils of equal talent have
equal skill at 15. Wealth and zone cannot enter. -/
theorem skill15_no_wealth (talent z1 z2 w1 w2 : Rat) :
    skill15 talent 0 0 0 z1 w1 = skill15 talent 0 0 0 z2 w2 := by
  unfold skill15 headStart
  grind

/-- For two pupils of equal talent, the skill gap is `zoneTeach*(zone1-zone2)` plus
`(home+preTut)*(logw1-logw2)`. Zone and wealth are the only sources of the gap. -/
theorem skill15_gap (talent zoneTeach home preTutCoef z1 z2 w1 w2 : Rat) :
    skill15 talent zoneTeach home preTutCoef z1 w1 - skill15 talent zoneTeach home preTutCoef z2 w2
      = zoneTeach * (z1 - z2) + (home + preTutCoef) * (w1 - w2) := by
  unfold skill15 headStart
  grind

/-! ### 3. Gate monotonicity -/

/-- A higher zhongkao score never loses the academic-track seat. -/
theorem academic_gate_mono (s1 s2 line : Rat) (h : s1 ≤ s2) (ha : academic s1 line) :
    academic s2 line := by
  unfold academic at *
  grind

/-- A higher score never loses the top-band seat. -/
theorem topBand_gate_mono (s1 s2 cutoff : Rat) (h : s1 ≤ s2) (ha : topBand s1 cutoff) :
    topBand s2 cutoff := by
  unfold topBand at *
  grind

/-! ### 4. Head-start fade at senior 2 -/

/-- The senior-2 gap `(1-decay)*(head1-head2)` lies between 0 and `head1-head2` when
`0 <= decay <= 1` and `head1 >= head2`. The fade removes part of the head start, never adds to it. -/
theorem fade_gap_bounds (decay h1 h2 : Rat) (hd0 : 0 ≤ decay) (hd1 : decay ≤ 1) (hh : h2 ≤ h1) :
    0 ≤ (1 - decay) * (h1 - h2) ∧ (1 - decay) * (h1 - h2) ≤ h1 - h2 := by
  have hx : 0 ≤ h1 - h2 := by grind
  have hA : 0 ≤ (1 - decay) * (h1 - h2) := Rat.mul_nonneg (by grind) hx
  have hB : 0 ≤ decay * (h1 - h2) := Rat.mul_nonneg hd0 hx
  exact ⟨hA, by grind⟩

/-- With full fade (`decay = 1`), the head-start gap at senior 2 is 0. -/
theorem fade_full (decay h1 h2 : Rat) (hd : decay = 1) :
    (1 - decay) * (h1 - h2) = 0 := by
  rw [hd]
  grind

/-- For two pupils with equal talent, in the same tier and the same entry band, the skill-16 gap is
`(1-decay)*(head1-head2) + postTut*(logw1-logw2)`. -/
theorem skill16_gap (tal decay grow school band classEff postTut h1 h2 w1 w2 : Rat) :
    skill16 tal h1 decay grow school band classEff postTut w1 -
      skill16 tal h2 decay grow school band classEff postTut w2
      = (1 - decay) * (h1 - h2) + postTut * (w1 - w2) := by
  unfold skill16
  grind

/-- Same setting as `skill16_gap` with no post-gate tutoring (`postTut = 0`, the 2026 setting in
gz_talent.py line 75). The skill-16 gap is then exactly `(1-decay)*(head1-head2)`. -/
theorem skill16_gap_no_postTut (tal decay grow school band classEff h1 h2 w1 w2 : Rat) :
    skill16 tal h1 decay grow school band classEff 0 w1 -
      skill16 tal h2 decay grow school band classEff 0 w2
      = (1 - decay) * (h1 - h2) := by
  have h := skill16_gap tal decay grow school band classEff 0 h1 h2 w1 w2
  grind

/-! ### 5. Re-banding at senior 2 -/

/-- With re-banding on, the senior-2 band is exactly the test `cutoff <= obs`. -/
theorem reband_formula (cutoff obs : Rat) (band1 : Bool) :
    band2 true cutoff obs band1 = decide (cutoff ≤ obs) := by
  simp [band2]

/-- With re-banding on, the senior-2 band does not depend on the entry band. -/
theorem reband_ignores_entry (cutoff obs : Rat) (b b' : Bool) :
    band2 true cutoff obs b = band2 true cutoff obs b' := by
  simp [band2]

/-- With re-banding on, a senior-2 score at or above the cutoff puts the pupil in the top band,
whatever the entry band was. -/
theorem reband_top_if_clears (cutoff obs : Rat) (band1 : Bool) (h : cutoff ≤ obs) :
    band2 true cutoff obs band1 = true := by
  simp [band2, h]

/-- With re-banding off, the senior-2 band equals the entry band. -/
theorem reband_off_keeps_entry (cutoff obs : Rat) (band1 : Bool) :
    band2 false cutoff obs band1 = band1 := by
  simp [band2]

/-! ### 6. Pre-gate ban knockout -/

/-- If the pre-gate tutoring coefficient `EARLY_EFF` is 0, the zhongkao score is the same whether
the pre-gate ban is on or off. The ban changes the hours but not the score. -/
theorem early_zero_ban_irrelevant (sq : Rat → Rat) (base legal enforce pre0 earlyEff : Rat)
    (h : earlyEff = 0) :
    zhongkaoScore sq base earlyEff (preTutHours true legal enforce pre0) =
      zhongkaoScore sq base earlyEff (preTutHours false legal enforce pre0) := by
  subst h
  unfold zhongkaoScore
  grind

/-- Non-vacuity instance: with `LEGAL = 0` and `ENFORCE = 4/5`, the ban cuts 10 pre-gate hours to 2.
With the ban off, the hours stay at 10. So the ban does change the hours in `early_zero_ban_irrelevant`. -/
theorem preTutHours_ban_changes :
    preTutHours true 0 (4 / 5) 10 = 2 ∧ preTutHours false 0 (4 / 5) 10 = 10 := by
  decide +kernel

end GZSorting
