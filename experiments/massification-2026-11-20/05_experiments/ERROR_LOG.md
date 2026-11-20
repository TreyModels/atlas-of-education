# ERROR LOG — every failure, crash, amendment and budget concession

No unrun cell is reported as completed. A failed substantive result still counts when it ran.

## E0 / Phase 0

1. **Known-answer test, first draft, had a design hole (found by the test itself, fixed).**
   The first version of the independent cohort ledger had no tax base for the first 10 years
   (pupils exist before any adult worker does), so household consumption went negative and the
   nonnegativity check failed with 129 violations. That was a *test-design* defect, not a
   conservation defect. Fixed by adding an explicit `START_FUND` endowment that finances the
   fiscal warm-up and is logged, never silently subsidising: draws must not exceed the fund and
   money still conserves exactly. This is the known-answer analogue of massabm starting with
   adult cohorts already in place at t0. Final run: all 9 checks PASS, exit 0.
2. **KAT CSV write failed once** (`FileNotFoundError`) because the output directory had not been
   created. The check itself passed, but the run exited 1. Fixed by creating the directory; the
   recorded Phase 0 log contains the corrected run (exit 0). No check was relaxed.
3. **massabm invariant checks, first pass, two false positives and one real finding.**
   - `reform_year` = -1 is a sentinel for "never reformed", not a negative stock; excluded from
     the nonnegativity check (documented in the checker).
   - `apex_cut` is a score-unit cutoff and can legitimately be negative; excluded.
   - **Real finding:** banning tutoring at every gate does *not* zero tutoring spend
     (4,464 units) because `tut_ban_leak=0.5` by default models an informal substitute market.
     With `tut_ban_leak=0.0` spend is exactly 0. Both behaviours are now reported (V7 and V7b).
     This is why E18 has separate "leak 0.5" and "leak 0.0" arms.

## E8

4. **E8 pilot ran 36/36 at reps=2 in 185 s** (per-run 10.2 s, max 16.9 s at N=6000 under load).
   Amendment: the predeclaration said reps=3. The Council asked for reps=4 to match the stored/
   manuscript design, so E8 was re-run at **reps=4** (72 runs); both runs are kept and the
   reps=4 result is the reported one. Rationale logged: the reps=2 run is retained as a pilot
   because per-run cost on the shared machine was ~10 s, not the ~3.5 s of the smoke run.
5. **E8 findings writer bug (pilot pass):** crashed on `NoneType` formatting *after* both CSVs
   were written. No run was lost; the summary/findings were regenerated from the raw CSV.

## E7

6. **E7 findings pass crashed** on `NoneType.__format__` because the summary row did not include
   per-gate spend keys used by the findings formatter. Both `e7_raw.csv` and the first
   `e7_summary.csv` had already been written; the cell was completed by regenerating the summary
   and findings from the raw CSV with `post_E7.py` (no rerun, no dropped runs). 30/30 runs
   succeeded. The final summary includes spend-by-gate.

## Triad (E14/E15)

7. **Spawn re-import error** (`An attempt has been made to start a new process before the current
   process has finished its bootstrapping phase`) because the runner had top-level code and no
   `if __name__ == '__main__':` guard. Fixed; triad cells then ran to exit 0.
8. **Missing output directory** (`FileNotFoundError: .../E14_necessity/necessity.csv`): triad's
   internal `_csv` does not create directories. Fixed by pre-creating each arm directory.
   The failed attempts are recorded here; the successful runs are the ones reported.

## Labour-market extension (E13b / E10 / E18)

9. **`hc_fair` (the stock competitive world) has no formal/informal margin**, so the original E13
   could not report a formal-employment probability for the competitive arm. Council guidance:
   build a matched rival with the *same* formal vacancy path and a hiring rule based on expected
   productivity. Added as `mode='hc_fair_slots'` in `code/ext_massabm` only; verified that the
   stock modes are untouched.
10. **CES sigma = 1 (rho = 0) divides by zero** in the stock `hc_fair` formula. The new branch has
    an explicit Cobb-Douglas limit guard so sigma ∈ {0.5, 1, 2} all run. Reported.
11. **Extension identity check:** with `support_effect=0` and `tut_hc_equiv=0` the patched copy
    reproduces the unmodified copy bit-for-bit (checksums of `c_cat, c_college, c_basic, c_exit,
    tut, pool_cat, inc_sum, inc_n, enrol` match on seed 0, N=2000). So E8/E13 results are not
    contaminated by the extension and E10/E18 are comparable with them.

## E18

12. **Verdict-logic amendment (disclosed, not silently changed).** The auto-generated findings line
    tested |Δcompletion| < 2 seed sd, but the predeclaration required "completion not LOWER by
    2 sd". Observed Δcompletion = +0.0076 (higher). So the learning guard passes; the failing
    criterion is the spend one. The corrected verdict is written in `runs/E18/README.md` and in
    EXPERIMENTS.md. The raw and summary CSVs are unchanged.

## Budget and scope concessions (not failures)

13. Triad cells E14/E15 ran at **reps=3, N=2000** rather than the model defaults (8, 3000), for
    budget. Seed dispersion is reported; treat as pilot-strength evidence.
14. **E15 and E20 were retained** (they completed cheaply) but E20 is **pilot only** and its
    transfer comparison is model-to-model; **Hong Kong is data blocked** in E19. Nothing about
    Hong Kong is claimed.
15. **Not run at all, recorded as `proposed`, never as completed:** E9 (return compression /
    outside options), E11 (floorworld S1–S5 education–economy mechanisms), E16 (credential
    information/recognition), E4 (childworld four states), and the cross-cutting recovery study.
    No cell, number or verdict exists for them in this package.
