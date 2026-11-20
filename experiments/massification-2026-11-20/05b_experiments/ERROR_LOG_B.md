# ERROR LOG — Batch B (`experiment-runner-2`)

Failures, amendments, implementation defects, interpretation issues and environment problems.
Nothing was dropped silently; no reported number comes from a run listed here as defective.

## Run-level failures

- **B1:** 72 runs requested, **72 ok, 0 failed**, wall 97 s (N=3000, workers=2).
- **B2/B3:** 72 runs requested, **72 ok, 0 failed**, wall 294 s (N=6000, workers=2). No massabm
  non-convergence flags exist in this model; the per-run 300 s SIGALRM did not fire.
- **B4:** 60 trajectories (3 modes × 2 turnover × 2 birth settings × 5 seeds), **0 invariant
  failures**, wall ≈ 7 s.
- **B5:** 800 static screening cells (5 reader arms × 16 factor combinations × 10 seeds),
  **800/800 ok, 0 failed**, wall ≈ 2 s.

## Interpretation issues and amendments (recorded, dated after the runs)

1. **Spec drift on the E13b baseline (before running).** The task brief said the E13b first pass was
   `reps=1, N=2000`. On arrival the stored cell had already been upgraded by runner 1 to
   `reps=6, N=5000` (wall 282 s). I did not rerun at reps=1. I treated the stored reps=6/N=5000 cell
   as the comparator and ran an **independent replication at N=3000** plus a precision/plausibility
   rule the stored pass had not applied. This is a deviation from the literal brief and is stated in
   `PRE_DECLARATIONS_B.md` and `EXPERIMENTS_B.md`.
2. **B1 plausibility gate was written on an arm mean (predeclared, but a weak formulation).** The
   predeclared condition (3) — "baseline diploma/degree ratio ≥ 0.20" — was evaluated on the mean over
   seeds. At sigma=0.5 the mean (0.234) passed while **5 of 6 seeded worlds** had per-seed baselines
   between 0.022 and 0.055. The literal rule therefore fired at sigma=0.5, but the cell is numerically
   unstable (degree income 1.01–42.39 across seeds). Fix: a **post-hoc** diagnostic
   (`code/b1_robust.py`, `runs/B1/b1_robustness.csv`) re-applies the gate per replication and is
   appended to `runs/B1/findings.txt` under an explicit "POST-HOC, not the declared test" heading.
   It can only downgrade, never upgrade, the declared verdict. Outcome: the contradiction does **not**
   survive as a fair-rival result. The literal program output (`survives=[0.5]`) is retained in the
   findings file for audit; the robust reading is reported in `EXPERIMENTS_B.md`.
3. **B4 post-hoc arm (amendment 1, added after the primary B4 run).** The primary ENDO arm showed
   cobweb instability (entry collapsing to the 0.02 floor, seed sd up to 0.38 at year 20). To check
   that the "requires supplied trend" verdict was not an artefact of an instantaneous switch, a
   post-hoc `ENDO_SMOOTH` arm (partial adjustment 0.5/yr) was added. It is **not predeclared**,
   is labelled POST-HOC in `PRE_DECLARATIONS_B.md` and in the findings/CSV, and the primary verdict is
   still taken from the predeclared EXO-vs-ENDO rule. Result: ENDO_SMOOTH also does not rise
   (0.218 → 0.108), so the verdict is robust to the smoothing check.
4. **B4 implementation defect found in code review BEFORE the model ran.** The first draft computed
   the workforce degree share with `sum(len(c[1])...)` / tuple indexing on the annual cohort lists,
   which would have counted tuple length (3) rather than cohort size. Fixed (cohort stock and head-count
   denominators) before the first execution; no reported B4 number comes from the defective version.
5. **B4 arm-specific burn-in caveat.** Each arm's 40-year burn-in uses its own decision rule, so EXO
   and ENDO start from different initial states (visible in ENDO turnover=20 premium ≈ 0.60 vs ≈ 0.90
   in turnover=40). The comparison is of trajectory **direction**, not levels; flagged in
   `EXPERIMENTS_B.md`. Common-burn-in is listed as the next design improvement.
6. **B2/B3 model copy.** B2/B3 deliberately ran the **unmodified** stock massabm
   (`code/stock/massabm`, copied from `01_sources`), not runner 1's patched extension, so the floor/race
   design is not contaminated by the extension. The extension defaults are 0.0, but using the stock
   copy removes the question.
7. **B2/B3 shared-run declaration.** B3 is a predeclared subset analysis of B2's 72 runs, not a second
   independent replication. Declared in `PRE_DECLARATIONS_B.md`; no extra runs were spent.
8. **B4 ENDO at year 20 has seed sd 0.384** on the entry rate (some seeds at the 0.98 ceiling, others
   at the 0.02 floor). Reported, not smoothed away; flagged as a genuine instability of the declared
   mechanism and the reason no stable ENDO trajectory is claimed.

## Environment / machine

- 8-core / 8 GB shared laptop. `load average` reached ~25 during B2/B3 (runner 1's `run_E18b.py` was
  running several workers in parallel). B2/B3 wall was 294 s vs the stored E8's 332 s, so contention
  did not block the cell, but wall-clock numbers are not comparable across the suite.
- Python 3.11.17, numpy 2.4.6, scipy 1.17.1 (matplotlib not imported by any Batch-B driver).
  `PYTHONDONTWRITEBYTECODE=1`, `nice -n 10`, workers ≤ 2, per-run SIGALRM 300 s.
- Sandbox: Batch B wrote only inside `05b_experiments/`. `01_sources/` was read-only; runner 1's
  `05_experiments/` was read only (its extension copied into `code/ext_massabm/`).

## B5 outcome issues (recorded after the B5 run; NOT defects)

- **Predeclared B5 calling-card claim partly contradicted.** The predeclaration said the detailed
  domestic reader would have lower hiring error than the coarse reader *but higher* certification
  demand. The run gives lower error (−0.365, 2sd 0.076, 10/10) **and lower** certification demand
  (−0.155, 2sd 0.030, 10/10). Reported as a contradicted half-claim in `EXPERIMENTS_B.md`; the
  predeclaration was not edited to remove it.
- **B5 foreign-recognition sign is counterintuitive and parameter-dependent.** Lowering recognition
  ρ from 1.0 to 0.3 *improves* coverage and error in the declared model because the foreign reader at
  ρ=1 over-weights a credential whose true productivity return (0.5 per tier) is below its signalling
  weight. This is a property of the declared weights, not evidence about real migrant recognition;
  flagged prominently in `EXPERIMENTS_B.md`.
- B5 was predeclared as **Amendment 5** (before running). The earlier "B5 not run" text in
  `PRE_DECLARATIONS_B.md` Amendment 4 is marked superseded.

## Cells not run

- E16's corruption channel and the menu's explicit **well-informed foreign reader control** were not
  run; only the ρ variation on a single foreign reader was run.
- No parameter-uncertainty sweep (Sobol/LHS), no external data fitting, no causal claim.

---

# BATCH C2 (task-9) — failures and amendments

- **Run-level:** C4 32/32 runs ok (wall 48 s); C5 1,440 static screening cells, 0 failures; C6 55/55
  trajectories, 0 failures. No per-run timeouts fired.
- **C5 first pass used a sequential RNG stream across cells** (inherited from B5), confounding paired arm
  contrasts with stream position. Rerun with per-cell matched streams before any result was recorded;
  first-pass output overwritten and never reported. B5 itself retains the sequential-stream limitation
  (recorded as a caveat in its record; results are averaged over 10 seeds with large effect sizes).
- **C4 literal rule vs targeted reading:** the predeclared three-way rule's `not specific` branch fired
  (cost_down, borrow_up rise) while the paper's insurance specificity claim is contradicted
  (outside_down −0.0875, 2sd 0.0413). Both are reported; interpretation appended to findings, no re-run.
  Caveat: the outside-down arm changes two wage-base entries at once (routine + informal), as declared.
- **C6 engine copy is patched** (declared): `shock_p`/`shock_size` parameters and a `mean_out_years`
  output only; defaults reproduce the original draw exactly (verified by inspection of the RNG
  consumption: `r.random(N)` is always drawn, so changing `shock_p` does not shift the stream).
  The mid-prior baseline's high "neither" share (0.421) is an engine property, flagged for validation.
- **C5 corrupt reader at κ=0 exactly equals the detailed reader** (0.851/0.045) after the matched-stream
  fix, verifying the corruption add-on does not perturb the base screen.
- **Timebox:** C4–C6 ran inside ~25 minutes; workers ≤ 2 throughout; `PYTHONDONTWRITEBYTECODE=1`.
