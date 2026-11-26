# GZSorting: Lean 4 formalization of the Guangzhou sorting model core logic

Lean 4.36.0, core only (no Mathlib). Not compiled by the author: this code was written without a
Lean toolchain. Expect possible small syntax or tactic errors on first build.

Sources:
* `/home/claude/sig/gz_talent.py` (lines 25-26, 28, 31-41)
* `/home/claude/sig/gz_system.py` (lines 67-73, 103, 106, 110)

## Build

    cd /home/claude/gzlean && lake build

Axiom check (after a successful build):

    cd /home/claude/gzlean && lake env lean axioms_check.lean

Expected output: each theorem depends only on `propext`, `Classical.choice`, `Quot.sound`, or a
subset of these. No `sorry`, `axiom`, `native_decide` or `unsafe` is used.

## What is proved (file `GZSorting/Core.lean`)

1. Tutoring hours `T = min(min(want, window), afford)` (gz_system.py line 106):
   - `tutor_zero_window`: window 0, want and afford non-negative, so T = 0.
   - `tutor_mono_window`, `tutor_zeroed_mono_window`: T (before and after zeroing) is non-decreasing
     in the window.
   - `tutor_le_window`: T <= window. `tutor_zeroed_le_window` gives the same bound after zeroing,
     for window >= 0.
   - `tutor_zero_below_one`: window < 1 gives zeroed hours 0.
2. Skill at 15 (gz_talent.py line 26): `skill15_no_wealth` (zone and home and preTut all 0, equal
   talent, equal skill); `skill15_gap` (exact gap formula for equal talent).
3. Gates: `academic_gate_mono` and `topBand_gate_mono` (a higher score keeps the seat).
4. Head-start fade: `fade_gap_bounds` (gap in [0, head1-head2]); `fade_full` (gap 0 at decay 1);
   `skill16_gap` (general gap, with the POST_TUT term); `skill16_gap_no_postTut` (gap equals
   (1-decay)*(head1-head2) with postTut = 0).
5. Re-banding (gz_talent.py line 41): `reband_formula`, `reband_ignores_entry`,
   `reband_top_if_clears`, `reband_off_keeps_entry`.
6. Pre-gate ban knockout: `early_zero_ban_irrelevant` (EARLY_EFF = 0 makes the score independent of
   the ban); `preTutHours_ban_changes` (non-vacuity: the ban does change the hours).

Each theorem has a doc comment with its plain-English meaning for the model.

## What is NOT proved, and deviations from the brief

- Deviation (item 4): the brief defines `head = zoneTeach*zone + home*logw`. The source
  (gz_talent.py line 25) also includes `PRE_TUT*logw`. The file follows the source (`headStart`).
  With PRE_TUT = 0 the two definitions agree.
- Deviation (item 4): the source's skill16 (line 39) includes `POST_TUT*logw`, so the gap between
  equal-talent pupils is `(1-decay)*(head1-head2) + postTut*(logw1-logw2)`. The brief's claim
  holds only when postTut = 0. That is proved as `skill16_gap_no_postTut`. The general form is
  `skill16_gap`.
- Item 6 uses `EARLY_EFF` and `sqrt(pre)` from gz_system.py (line 73). gz_talent.py has no
  pre-gate hours term; its PRE_TUT enters skill at 15 linearly in logw, not through hours.
- Not modelled: the quantile cutoffs (gz_talent.py lines 28, 35, 41) and all random draws. They
  enter as arguments. No theorem says that a quantile gives the stated share of pupils.
- Not modelled: the non-academic-track zero (`np.where(academic, ..., 0)`), the boarding lottery
  (`buys`, gz_system.py lines 107-109), the zero-want clip, and the `WEEKEND_HRS`/`EVENING_HRS`
  window selection (line 103). Only the functions of their values are formalized.
- Not proved: the sqrt function itself (it is an argument `sq`), and any property of the Python
  simulation outputs (EO ratios, concentration indices). Those are numerical results, not logic.
- No theorem about IEEE floating point. Rationals stand for floats.

## Least confident proofs (most likely to need edits)

- `ratMin_mono_arg1`, `ratMin_mono_arg2`, `zeroBelow1_mono`: rely on `split <;> split <;> grind`.
- `tutor_zero_window`, `fade_gap_bounds`: rely on `grind` with `Rat.mul_nonneg` and `(by grind)`
  side goals.
- `preTutHours_ban_changes`: uses `decide +kernel` on Rat literals (as hflow does for `1/2`).
- `skill15_gap`, `skill16_gap`, `skill16_gap_no_postTut`: rely on `grind` for ring identities
  over Rat.
