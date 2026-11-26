# PAPER C v2 / A6 — preregistration (host-only draft; no compute until Lead/Trey approval)

**Status: DRAFT FOR ADJUDICATOR REVIEW. No A6 compute has been launched.** A5 is **VOID** (no A5 data reused:
the preserved 10 rows / 6 cells are a failed-run record only; A5 manifest status VOID). This A6 prereg follows Claude's
redesign Part 2 and the adjudicator's A6 requirements: behavioural estimands not mechanically determined by treatment;
treatment absent from outcome definition/denominator; pre-launch degeneracy screen; manipulation checks separate; full
pre-declared Holm family (no post-screening narrowing); power/MDE-derived seed count; pilot for variance only.

## 1. Design

* **Engine:** pin `846c9e0` (core `e111397b…`); spec `docs/audit/canonical_spec.json` (`e5ddef6b…`); canonical HK base
  gates; treated gate = G6→G9 (`gates[1]`, kind=contest, `share_of='cohort'`, gate-level r fixed by L: 1.2 at L=.25,
  1.6 at L=.45, fail routing from canonical HK gates).
* **Cells (36, same factor space as screening, contrast-complete):** S=q0 ∈ {0.85, 1.0, 1.15} × L ∈ {0.25, 0.45} ×
  supply ∈ {A: own_ban 0/firm_ban 0, B: own_ban .95/firm_ban 0, C: own_ban 0/firm_ban .9} × settings ∈ {P55:
  pay_ratio .55, monitoring .2, pay_gap; P12: pay_ratio 1.2, monitoring .5, pay_gap (no-withholding control)}.
* **N=600, T=46, measure_from=18** (N=600 is the declared confirmatory resolution; screening/pilot variance was measured
  at N=600; N=1500 measured ~809 CPU-s/run and is not used — see §5).
* **Seeds = 8 matched seeds (0–7)** — derived by the power rule in §3 (power-required n≈1 for both tests at
  Bonferroni-adjusted α; a **declared minimum of 8** is required for the seed bootstrap/robustness and is the larger of
  the two rules; no effect-based seed choice).
* **Runner:** to be authored/committed as `run_paperC_A6.py` (new, pinned to the frozen spec; records per-seed rows for
  every declared estimand). Runner sha to be cited in the A6 manifest before launch.

## 2. Estimands and tests (declared family)

**Primary confirmatory family (Holm, m=2, α=.05, two-sided):**
* **T1' (substantive S estimand):** K-12 tutoring **participation rate** (`tut_k12_rate`, pp). Pre-declared direction:
  **S↑ ⇒ participation↓**; contrast = mean over design cells of `rate(S=.85) − rate(S=1.15)` (pp); **minimum effect
  +3.0 pp** (i.e. participation at least 3 pp lower at S=1.15).
* **T4' (substantive L estimand):** **Q5−Q1 K-12 tutoring spend gap** (`q5_q1_spend_gap`, pp). Pre-declared direction:
  **L↑ ⇒ spend gap↑**; contrast = mean over design cells of `gap(L=.45) − gap(L=.25)` (pp); **minimum effect +2.0 pp**.

**Manipulation checks (reported separately, NOT in the confirmatory family, no claims):**
* **M1 own-supply access:** `tut_own_by_grade`/own-share response to own_ban/firm_ban — mechanically tied to the
  treatment input, reported only as a check that the treatment operated.
* **M2 withholding response:** `withheld` under P55 vs P12 — deterministic by construction (`h=.4*(1−pay_ratio)*(1−monitoring)*sell`);
  reported as a check, never as an estimand (the A5 defect).

**Secondary/descriptive (no confirmatory claim):** K-12 spend level, G12 participation, L6/L9 means, fixed-threshold
gap-close (share of Q1 pupils reaching declared fixed proficiency R), rank-based admission rates — reported with CIs but
outside the Holm family and labelled descriptive; learning outcomes may enter a future family only via a new amendment
with pilot-derived variance.

## 3. Power / MDE and seed-count rule

Power/MDE from **screening SDs only** (variance use; no effect-based design choice; screening effects are not reused as
hypotheses):

| test | screening per-seed paired-contrast SD (N=600) | declared minimum effect δ | power formula n=((z_{1−α/2}+z_{1−β})·SD/δ)² | 
|---|---|---|---|
| T1' | **0.0598 pp** | 3.0 pp | n≈0.004 → 1 |
| T4' | **0.0680 pp** | 2.0 pp | n≈0.011 → 1 |

**Rule (frozen):** α family = .05, Holm m=2 ⇒ worst-case per-test α/2=.025 (z=2.394); power 1−β=.80 (z=0.842).
Power-required n is 1 for both tests; **declared seed count = max(power-required n, 8) = 8 matched seeds (0–7)**, the
minimum for a stable seed bootstrap and for the degeneracy screen. **Achieved MDE at n=8** = (z_a+z_b)·SD/√8:
**T1' ≈0.065 pp**, **T4' ≈0.074 pp** (far below the substantive minima; the tests are powered ≫0.99 for the declared
effects). The report must state achieved MDE and that seed-level variance is small; statistical significance alone is
not the claim — the **minimum substantively meaningful effect** is the decision threshold.

## 4. Pre-launch degeneracy-screen gate (blocking)

Before any A6 confirmatory run, a **pilot (8 seeds, 36 cells, N=600; the same design)** must pass:
1. **Distinctness/variance:** every declared outcome has ≥2 distinct values and SD>0 across seeds within cells
   (reject SE=0/constant outcomes).
2. **No mechanical determination:** each declared estimand passes an automated input→output mapping check; outcomes
   whose definition/denominator contains a treatment variable are **rejected as estimands** (A5 M1/M2 are the canonical
   failures) and can only be manipulation checks.
3. **Pilot use:** pilot data are used **only** for variance/MDE and degeneracy screening; **no pilot effect sizes are
   used to choose tests, directions, seeds, or stopping**.
4. **A5 data are not reused** (VOID record; preserved ckpts excluded).
If the screen fails, the prereg is amended before launch; no post-hoc test substitution.

## 5. Compute envelope

Measured N=600 cost from screening: ~45.7 CPU-s/run. A6: 36 cells × 8 seeds = **288 runs ≈ 3.7 CPU-h**; at 8 workers
≈0.5 h wall; at 6 workers ≈0.7 h; plus the degeneracy pilot (288 runs same design — if the pilot is the same run reused
for variance screening, budget one run of 3.7 CPU-h total; the confirmatory run requires a separate frozen seed block if
the pilot seeds are used for variance only). Envelope: **≤10 CPU-h including pilot**, ≤2 h wall at 6–8 workers;
1–2 slots reserved for other lanes. (N=1500 is rejected: ~809 CPU-s/run measured.)

## 6. Analysis plan (committed script)

`papers/shadow-education-contest/code/analyze_paperC_A6.py` (sha recorded in the A6 manifest before launch) computes:
* per-seed **paired contrasts** for T1'/T4' (matched seeds across cells), averaged over the design cells;
* **5,000-draw seed bootstrap** 95 % CIs for each contrast (resampling seeds, pairing across cells);
* **Holm** adjustment across the declared family (m=2), two-sided α=.05;
* **achieved MDE** from the pre-declared SDs and n (and empirical SD sanity check);
* **degeneracy-screen report** (distinct values, SD, mechanical-determination flags);
* manipulation checks M1/M2 reported separately, never as claims;
* outputs a JSON with design, hashes, per-test results, decision (holds/fails/indeterminate: effect≥min & Holm p<.05
  & correct direction; otherwise fails/indeterminate per CI).

## 7. Launch gates

1. Adjudicator review of this prereg + analysis script sha; 2. Lead/Trey approval; 3. runner committed and pinned; 4.
degeneracy pilot PASS; 5. box allocation + reserve; 6. manifest frozen with all hashes. **No A6 compute before 1–6.**
No Paper C claim exists until the A6 confirmatory artefact is verified and adjudicated.

## 8. Committed artefacts (hashes for the reviewer)

* This prereg: `docs/audit/PAPER_C_A6_PREREG.md` sha256 **`2c74bf2e6bc2be6363490042316188f2cb031669c75a18922de9d6e6d5d284dc`**
* Machine-readable prereg: `docs/audit/PAPER_C_A6_PREREG.json` (sha recorded at commit; updated with script hash)
* Committed analysis script: `papers/shadow-education-contest/code/analyze_paperC_A6.py` sha256 **`93d762e0f9a7eeb0f7462e2d7768b7446954ca4e06fdefe366960d4da480caef`** at commit **`e6cd2d0`**
  (must be cited in the A6 manifest before launch; no uncommitted analysis code).
