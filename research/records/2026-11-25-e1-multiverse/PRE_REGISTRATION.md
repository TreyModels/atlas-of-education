# PRE-REGISTRATION — E1: grouping multiverse at R = 1200, full BH/BY verdicts

**Task:** task-46. **Branch:** `research/e1-multiverse-1200-2026-11-25`. **Record:**
`research/records/2026-11-25-e1-multiverse/`. **Written before any multiverse run** and committed before the
pilot. **Compute:** box `autodl3` (8-CPU cgroup quota, 60 GB RAM); CPU only — the GPU engine is not used in
this task, so no GPU batch layout exists to pin.

## Question

The methods paper certifies 35 links ("strict tier") at R = 400 under a nominal Benjamini–Hochberg (BH) step-up,
but reports **0** under the dependence-robust Benjamini–Yekutieli (BY) procedure. E1 asks, arithmetically and
with real data: with more random partitions (R), does the BY-certified tier change, and is the strict-tier
story conditional on the dependence assumption? The deliverable is the complete BH and BY verdict pattern for
all 272 links, in four result families, at R = 20 (pilot), 74, 400, 800 and 1200.

## Data, provenance and tier labels

- Panel: `/root/work/data` on box `autodl3` — 68 World Bank WDI series + `meta.json`. **Tier: observed
  (World Bank API pull); no imputation, no reconstruction, no synthetic series.** The estimator's 17 VARS
  (`electricity, wage_emp, lsc, sec, ter, prm_cmp, gdppc_log, urban, tax, agri_va, emp_agri, flfp, life_exp,
  u5mr, gpi_sec, gpi_ter, fertility`) are all present in that directory; none is re-pulled unless missing,
  and anything re-pulled is recorded with URL and hash.
- Provenance evidence committed before the main run: sha256 of each of the 17 series, `meta.json`, and the
  derived arrays where practical (`results/panel_hashes.txt`). The panel is validated against the committed
  400-draw results: the real-grouping pass (deterministic, no random draws) must reproduce the committed
  `edge_table400.csv` columns `pooled_FE_t` and `pooled_TR_t` (544 values) to within 1e-6 absolute; any
  systematic difference stops the run and is reported as a panel-vintage discrepancy, not adjusted away.
- `final400.pkl` from the old box is **lost**. The first 400 draws are therefore reproduced from the same
  code and panel; the reproduction check is the comparison of the real pass above plus the first-400 analysis
  against the committed `edge_table400.csv` and `headline.json` aggregates.

## Estimator (unchanged) and seeds

Estimator is exactly `gm_core.py` from branch `research/grouping-multiverse-400-2026-11-23` @ `1152cec`
(17 variables, 136 unordered pairs × 2 specifications = 272 links, 50 real groupings in 8 families, 10-year
change, own starting level, controls log GDP per head and urbanisation, country and decade fixed effects,
country-clustered SEs, with and without a country trend). Random replicate r uses
`numpy.random.default_rng(1000 + r)`, so r = 1..400 reproduce the committed 400-draw run's draws exactly
(seeds 1001..1400); r = 1..74 reproduce the 74-draw run's draws. No code path is changed: the runner imports
`gm_core` and reproduces `run_multiverse400.job(r)` logic exactly. Working copies are committed in
`scripts/`.

## R ladder and bounded-pilot rule

1. **Pilot (R = 20).** Run r = 0..20 on 8 workers. Check (a) real-pass reproduction against
   `edge_table400.csv` (above); (b) determinism: replicate r = 7 computed twice in fresh processes is
   bit-identical (z, Qp, flip); (c) per-draw wall time → projected wall for R = 1200.
2. **R = 400 comparison.** From the same nested run, analyse the first 400 draws and compare with the
   committed `edge_table400.csv` (per-link `share_TR`, `emp_p_up_TR`, BH counts) and `headline.json`
   (`new_counts`: certified up/dn/flip/het, robust 5, class counts). Pre-specified tolerance: shares and
   empirical p-values must agree to ≤1e-6; BH counts must agree exactly. Any larger difference is reported
   as a panel/code discrepancy and the run stops.
3. **Scale to 800 and 1200 only if** the pilot is stable (reproduction and determinism pass) **and** the
   projected 1200-draw wall fits the session budget. The projection is made from the measured per-draw wall
   time on the 8-core cgroup with a 15% overhead margin. If the projected wall exceeds **10 hours**, stop at
   the largest completed R in {400, 800} and say so explicitly; no unbounded drift, no silent extension.
4. Draws are nested in one run (r = 1..1200) rather than separate 400/800/1200 runs; that is arithmetically
   identical to separate runs with the same seeds and avoids re-computation.

## Checkpoint / resume policy

One checkpoint file per replicate (`out/reps/r0001.npz` … `r1200.npz`; r=0 separate), written as soon as
the replicate finishes, with z (float32, cells × 544), Qp, flip, fits, wall. The runner checks for an
existing checkpoint and skips it, so a crash or box restart loses at most one draw. A progress log records
draw number, wall time and cumulative time. A `.partial` aggregate pickle is written every 50 draws.
Runs are launched under `nohup` (and `tmux` where available) with `OMP/OPENBLAS/MKL/NUMEXPR=1` and 8 workers.

## Analysis specification (fixed before seeing R > 400 results)

- Estimator-derived quantities are computed exactly as in `analyse400.py`: for each link, the real-grouping
  significance share under the trend specification (`Tr_sig`), the family-balanced null distribution over
  random draws (`nullT`), and the same for the four procedures:
  **up** (real share ≥ null; p from exceedances), **down** (real ≤ null), **sign-flip** (real flip rate ≤
  null), **heterogeneity** (real Q-rate ≥ null). Empirical p-values use the conservative
  `(1 + exceedances)/(1 + valid draws)` convention; the liberal `count/R` convention is reported as a
  sensitivity.
- **BH:** Benjamini–Hochberg at α = 0.05 over the sorted 272-link p-vector separately for each of the four
  procedures. Also report the 136-pair parity convention (`q` shared within each specification pair) as in
  the committed analysis.
- **BY:** Benjamini–Yekutieli at α = 0.05 over the same sorted 272-link vector per procedure:
  `q = p · M · H_M`, `H_M = Σ_{i=1..M} 1/i`, `M = 272` (`H_M = 6.185...`); the first-certifying rank is
  reported. (The parity M = 136 sensitivity is also reported.)
- **Verdicts:** a link is "certified up/down/flip/het at R" if its BY q < 0.05 in that procedure. The BY
  tier at each R is reported as the full set of links (and counts), not as a floor count. "Robust
  everywhere" is recomputed with the unchanged rule at R = 1200.
- **BH/BY counts at R = 20, 74, 400, 800, 1200** are reported in `results/verdict_by_R.csv` (per link: p and
  q for each procedure at each R) and `results/summary_by_R.json` (counts, floor, first-certifying rank).
  The pre-specified comparison: does the BY-certified set change with R? Answer yes/no and list links that
  change.
- **Split halves at R = 1200:** two disjoint halves, draws r = 1..600 and r = 601..1200. Within each half,
  recompute empirical p-values against that half's own null and the BH/BY verdicts; report (i) Spearman rank
  correlation of the 272 up-procedure p-values between halves, (ii) exact verdict-agreement counts by
  procedure, (iii) the number of links certified in both halves, one half, or neither.
- **Group-localisation diagnostic:** for the five "robust everywhere" links (and, separately, for all
  BY-certified links at R = 1200), compute leave-one-country-out pooled estimates on the full panel
  (trend specification) using `gm_core`; report the most influential countries, the number of countries
  whose exclusion moves the estimate below |t| = 1.96, and the share of the total signal contributed by the
  top 5 and top 10 countries. Pre-specified reading: a link is "group-concentrated" if excluding its top 5
  countries flips significance or changes |b| by more than 50%.
- Every number in the report is traced to a committed output file and field.

## What would falsify the substantive story

- If the real-pass panel reproduction fails, the committed 400-draw results cannot be reproduced on the new
  box and the comparison is declared unavailable (not adjusted).
- If the BY-certified tier changes materially between R = 400 and R = 1200, the methods paper's "zero under
  BY at 400" must be re-read as a draw-budget statement and the new count reported.
- If split-halves agreement is low, the strict-tier claim is not stable at R = 1200.

## Reporting, failures and shutdown

`REPORT.md` will list commands, seeds, git commit of the code, input hashes, runtimes, failures, deviations
from this plan and uncertainty. Raw logs and checkpoints stay in `out/` and are committed where small enough
(else their hashes and the regeneration command are). No secrets. The rented instance is shut down when the
job finishes; `REPORT.md` records the shutdown.

## Declared deviations log (append-only, filled during the work)

- **2026-11-24 13:36 UTC — panel-vintage micro-discrepancy (declared before scaling).** The real-grouping
  pass on the new box reproduces the committed `edge_table400.csv` pooled t-statistics with
  **max |Δt| = 3.97e-5**, median **7.54e-7** (258/544 values above 1e-6, none above 1e-4;
  `results/panelcheck.json`). The old box/panel is unavailable (`final400.pkl` lost; box2 closed), so an
  exact panel reproduction is impossible. **Decision: proceed with the new panel as the E1 panel, and report
  the R=400 comparison as a reproduction-with-vintage-difference, not a bit-identical reproduction.** No
  adjustment is applied; the discrepancy is ~4 orders of magnitude below the effect sizes at issue, and the
  R=400 certified counts are compared directly against the committed headline. Full hashes in
  `results/panel_hashes.txt`.
- **2026-11-24 13:36 UTC — pilot (R=20) and runtime projection.** 21 draws in **274.8 s** wall on 8 workers
  (mean per-draw worker wall 97.8 s; **13.08 s/draw effective**). Projected R=1200: ~15,700 s + startup
  ≈ **4.4 h**, inside the 10 h cap, so the run scales to 1200. Determinism: replicate 7 recomputed in a fresh
  process is **bit-identical** in z, Qp and flip. The runner was made importable by moving the deterministic
  grouping construction to module level (job logic unchanged; determinism re-checked after the change).
- **Compute:** CPU only (8-core cgroup); the GPU engine is not used, so no GPU batch layout applies.

- **2026-11-24 07:10 UTC — run complete.** 1,200/1,200 draws + real pass, total wall 5,426.8 s on 8 workers
  (4.52 s/draw effective; per-draw worker wall mean 37.8 s, median 36.4 s). All 1,201 checkpoints valid
  (sha256 manifest in `results/reps_sha256.txt`); no failed draws, no resume events.
- **2026-11-24 — flip-family direction (declared analysis deviation).** The pre-registration wrote the
  sign-flip family as "real flip rate <= null". The committed analysis and the substantive object are
  "real flip rate >= null" (flips *more* than random; `analyse400.py` uses `emp_p(FR, nF, "up")`). Primary
  results use >= and reproduce the committed R=400 count of 15; the <= direction is retained as a sensitivity
  and certifies 0 at every R. This was corrected before the final report; no other analysis direction changed.
- **Final headline (filled at completion):** BH up/down/flip/het = 35/19/15/53 at R=400, 41/20/17/53 at R=800,
  41/23/20/53 at R=1200; BY = 0 for all four families at R<=800 and **32 for heterogeneity at R=1200**
  (first BY rank 29, floor 32), with up/down/flip still 0 at 1200. R=400 BH counts and the 5 robust links
  reproduce the committed headline exactly; `share_TR` differs by <=5e-7; pooled t-stats differ by max 3.97e-5
  (declared panel vintage).
