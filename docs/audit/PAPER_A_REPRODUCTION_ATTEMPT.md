# PAPER A — REIMPLEMENTATION PLAN + STATUS (Phase 2)

**STATUS: REIMPLEMENT ON THE REPAIRED ENGINE — NOT A RECOVERY, NOT A CODEX COMPARISON.** Per the operator
clarification: Gemini ran both papers **inside its app** and made other mistakes. **We are not recovering Gemini's
files, and there is no Codex re-run to compare against** (Codex is the independent auditor; it did not like what
Gemini did). We are **reimplementing what Gemini was trying to do — bigger and better — on the repaired engine, using
the server.** The old docx numbers are the **AUTHOR-REPORTED BASELINE** for comparison; the new runs are a **NEW
GENERATION** with pre-registration, hashes, provenance, uncertainty, baselines and sensitivity.

**Adjudicator role note:** `paper-adjudicator` is the independent adjudicator, not the execution owner. This document
specifies the plan, status and acceptance criteria; execution belongs to `atlas-commander` / the engine lanes. It
supersedes the earlier "reproduction attempt" framing.

---

## 0. One-paragraph status

Five computations define Paper A: (a) the E8 fee-abolition event study, (b) the delayed secondary-bulge `t*`, (c) the
gate-architecture/H2 experiment, (d) multi-seed identifiability/Jacobian, (e) the fee-abolition forecast with
held-out horizons. **(a) is DONE and REPLICATES under the author's estimator family — fresh-WDI CS-style group-time ATT gives impact +12.322 (author +12.44) and post mean +25.083 (author +25.26), with 8-cluster wide CI; (b) is DONE (bulge `t*` no detectable jump, −0.956, p .251/.384); (c), (d) are design-ready; (e) is DONE on the fixed engine (`846c9e0`; canonical re-pin `46c080d`, `year_t=T0`, `unfired_events==[]`) and is accepted as a **new-generation conditional simulation** with a declared calibration fallback — the author's 74.88 % anchor is infeasible in the repaired world (max 71.0 % at fee 0).** None of the five depends on recovering the
Gemini code. The new-generation baseline is the repaired 540 (`98baf6b`, sha256 `455649da…`) and the P0 audit
artefacts, which already establish the engine's behaviour and the identifiability limits.

---

## 1. Status at a glance

| # | computation | new-generation design | status | compute class | blocker |
|---|---|---|---|---|---|
| (a) | **E8 fee-abolition event study** | fresh hashed WDI; **CS-style group-time ATT** (not-yet-treated controls), 500 cluster bootstraps + 2,500 Fisher/scheme; full event path | **DONE (REPRODUCED EMPIRICAL ANALYSIS)** — impact **+12.322 pp** (bootstrap mean 12.308, 95% CI [4.48, 22.64]) AND post mean **+25.083 pp** vs author +12.44 / +25.26 — **both replicate**; event path 12.32, 23.66, 25.79, 21.88, 24.94, 28.45, 25.78; Fisher p 0.0044/0.0040. Simple-DiD +2.54 is estimator sensitivity. Artefacts `CS_ESTIMATOR_NEWGEN.md` + `results/audit/newgen/cs_estimator_fresh_wdi_2026-11-25.json` | host, 8.2 s | none; declared deviations (equal weights, no DR covariates, 8 clusters, fresh vintage) |
| (b) | **Delayed secondary-bulge `t*`** | fresh hashed WDI; `t* = abolition + SE.PRM.DURS`; outcome SE.SEC.ENRR; 2,500 perms/scheme | **DONE (fresh WDI)** — ATT at `t*` **−0.956 pp**, post +0.30, Fisher p **0.251/0.384** → **no detectable secondary-bulge jump**; **UNRESOLVED** (no-effect evidence), consistent with the manuscript's honest-null framing | host, 8.7 s | none |
| (c) | **Gate-architecture / H2 (≥5,000 runs)** | repaired engine `98baf6b`; pre-registered gate kinds `bar/bar_high/quota/contest`; S ∈ {.25,.35,.45,.55,.70}; fee ∈ {0,.19}; vac0 ∈ {.02,.08,.25,.50}; **≥5,000 runs** (30–40 matched seeds/cell, expanded grid); H2 = Δcut(S=.25) − Δcut(S=.70); report H1/H2/inverted-U with seed uncertainty and baselines | **DESIGN READY / RUN PENDING** — no new-generation run yet; the paper's 1,640-run version is AUTHOR-REPORTED BASELINE only | server, ~43–60 CPU-h for ≥5,000 runs at `N≈400`/`T≈70`; ~5–8 h wall at ≤10 CPUs | pre-registration + engine config freeze (no SSA config exists in the engine — must be specified in the prereg) |
| (d) | **Multi-seed identifiability / Jacobian (declared perturbations)** | explicit 3-option MNL `masseng-tutoring` model; analytic Jacobian; rank/null-space at **multi-seed declared perturbations** (e.g., 100 population draws); aggregate moments vs micro-moments; report local rank, condition, finite non-identification, and the two-moment remedy; no global "theorem" | **DESIGN READY / MODEL SPEC NEEDED** — the independent ABC harness is the template; Paper A's own model spec must be written down | host, minutes–hours | a documented model specification + declared perturbation grid |
| (e) | **Fee-abolition forecast with held-out horizons** | fixed engine `846c9e0` (canonical re-pin `46c080d`); `year_t=T0`; `assert E.unfired_events==[]`; 40 matched seeds; held-out e=+5,+6; training-only calibration attempted | **DONE — ACCEPTED as REPRODUCED SIMULATION (NEW GENERATION)** — abolition − persistence **+17.19…+25.35 pp**; full-7 **RMSE 2.764 / MAE 2.432** vs persistence **23.759 / 23.260 (−88.4 %)**; held-out e=+5,+6 **RMSE 1.637 / MAE 1.350**. **Fallback:** the author's **74.88 % anchor is infeasible** in the repaired world (max 71.0 % at fee 0; A-38); fee 0.15 + engine pre-abolition level, **no post tuning**. Conditional simulation, not a reproduction of the author's calibration. v1 uncited. | host, 13.8 s | none; provenance `FORECAST_NEWGEN.md` sha256 `d4c0a239…d8f1`; JSON `f0eee995…c04` |

---

## 2. Why reimplement rather than recover

The repaired engine (`98baf6b`, Gate-1) fixes the five implementation defects that made the old simulator results
non-comparable: **D1** KR G9 phantom prize → persistent track consequence; **D2** expected admission P = exact
Plackett–Luce (pre-repair expected/realised 2.41× / 1.96× → 1.0000); **D3** applicants-based seat denominator
(0.513 → 0.2500 realised admit rate); **D6** policy-invariant event-keyed RNG (51 → 0 mismatches); **D4/D5** tax/outlay
ledger; **D7** labour prizes last. The 540 generation is reproduced (host 9,174/9,180 seed + 842/846 summary values
exact vs reference; box 9,164/9,180 + 831/846). A paper written on the pre-repair engine is not a baseline we want
to "recover"; it is a **baseline to compare against**. Reimplementation on the repaired engine is both cheaper than
chasing missing files and scientifically stronger.

**The original Gemini artefacts: "not found where searched", then move on.** They were not found in
`~/neon-boot/pulled/gemini-bundles/`, the archive branch `46950ab`, any `research/*` branch, `~/neon-boot/wt2|3|5`,
`~/massification_live`, or the iCloud Downloads bundles. They are noted here for provenance only; they are **not the
blocker**, and we are not waiting for them.

---

## 3. The five computations — new-generation designs

### (a) E8 fee-abolition event study — READY / partly DONE

* **Inputs:** fresh WDI pull (`SE.PRM.ENRR`, secondary `SE.SEC.ENRR`) with vintage + sha256; `fee_dates.csv` (8
  verified abolitions); 40-country SSA donor pool; region map.
* **Design:** Callaway–Sant'Anna group-time ATT, universal base `g−1`, not-yet-treated controls, cohort-size
  weighting, 500 country-cluster bootstrap; **10,000 placebo-date + 10,000 placebo-country** Fisher permutations;
  full event lead vector (do not quote only e = −2/−3); gender split with the pre-registered paired CI; a placebo
  family; secondary outcome.
* **New-generation additions:** pinned WDI vintage + hashes; full lead-vector reporting; pre-registered placebo
  family; secondary outcome; explicit association-only language.
* **Status:** **DONE on fresh hashed WDI — REPLICATES under the author's estimator family.** CS-style group-time
  ATT: impact **+12.322 pp** (bootstrap mean 12.308, 95% CI [4.48, 22.64]); post mean **+25.083 pp** vs author
  +25.26; event path 12.32, 23.66, 25.79, 21.88, 24.94, 28.45, 25.78; pre-trend e=−3 +0.138; Fisher p
  **0.0044 / 0.0040**. Declared deviations: equal weights, no DR covariates, 8 clusters → wide CI, fresh vintage.
  The earlier simple-DiD +2.54 is **estimator sensitivity**. The author-record E8 numbers remain VERIFIED EMPIRICAL
  against the committed record.

### (b) Delayed secondary-bulge `t*` — DATA-BLOCKED

* **Inputs:** fresh, hashed WDI/UIS series for `SE.PRM.DURS`, `SE.PRM.REPT.ZS`, `SE.SEC.PROG.ZS`, `SE.SEC.ENRR`,
  `SE.SEC.ENRL.TC.ZS` (1990–2020); a **documented** `L_primary` source (ISCED/UNESCO mapping); `fee_dates`.
* **Design:** `t* = t_ab + L_primary` by country; CS event studies centred on `t*`; 2,500 permutations/scheme;
  pre-registered capacity strata; report estimable cells and NOT-ESTIMABLE cells honestly; no imputation.
* **Status:** **DONE on fresh hashed WDI.** `t*` per country from `SE.PRM.DURS`; ATT at `t*` **−0.956 pp**, post mean
  **+0.30 pp**, Fisher p **0.251** dates / **0.384** countries → **no detectable secondary-bulge jump** (UNRESOLVED,
  no-effect evidence). Consistent with the manuscript's honest-null framing; no causal claim.

### (c) Gate-architecture / H2 — DESIGN READY / RUN PENDING

* **Engine:** repaired `98baf6b` (`core.py 72cbddf7…`, `contest_math.py 23a01730…`, `tutoring.py 7a6fd4c3…`); frozen
  config documented in the pre-registration (no SSA `countries/` config exists; specify the household/liquidity/
  labour/gate dict).
* **Design:** gate kinds `bar`, `bar_high`, `quota`, `contest`; S ∈ {.25,.35,.45,.55,.70}; fee ∈ {0,.19}; vac0 ∈
  {.02,.08,.25,.50}; **≥5,000 runs** (expand seeds to 30–40 and/or add gate/fee cells); H1 = Δ(S=.25 − .70); H2 =
  Δcut(S=.25) − Δcut(S=.70); report the inverted-U with 95% seed CIs; include a quota-benchmark arm and a
  no-contest control; report effort, spend, elite share and admission diagnostics.
* **Cost model:** HK 20.3 CPU-s/run, KR 41.9 CPU-s/run (measured); the 1,640-run Paper A grid at `N=400/T=70` ≈
  14–30 CPU-h; **≥5,000 runs ≈ 43–60 CPU-h** ≈ 5–8 h wall at ≤10 CPUs. Must be pre-registered and budgeted.
* **Status:** design ready; no new-generation run yet. This is the largest single item and the one that most
  directly replaces the paper's most-cited claim.

### (d) Multi-seed identifiability / Jacobian — DESIGN READY / MODEL SPEC NEEDED

* **Model:** the 3-option MNL (`none / own-teacher / other-provider`) with the documented covariates (income,
  school-quality gap, grade bonuses, urban demand, teacher threshold); the exact 10-parameter vector and the 7
  Bray aggregate targets must be written down (the manuscript has prose only).
* **Design:** compute the analytic Jacobian of the moment map; rank and null space at **multiple seed points and
  declared perturbations** (e.g., 100 population draws, covariate perturbations, target perturbations); report
  finite non-identification (distinct θ on the moment manifold), condition numbers as diagnostics only (never as
  identification evidence); add the two micro-moments and report **local** rank only; no "theorem".
* **Independent anchor:** the audit's ABC harness (`docs/audit/code/abc_identification_audit.py`) is the template;
  re-executed by the adjudicator with output sha256 `66bb2648…15808` (rank 4/5, 2-dim null, analytic
  δ = −0.7537718023763802, local 5/5 after two moments). It is **not** Paper A's model, but it sets the standard.
* **Status:** design ready; a documented model spec + perturbation grid is the only missing input; compute is
  minutes–hours on host.

### (e) Fee-abolition forecast with held-out horizons — DESIGN READY / RUN PENDING

* **Design:** specify the SSA engine config in the pre-registration; calibrate `fee_public` to pre-abolition GER
  **on training horizons only**; hold out e = +5/+6 (and a country holdout if feasible); ≥40 paired seeds; report
  RMSE/MAE vs persistence on the **held-out** horizons; sensitivity to `max_entry_age`, repetition, and the gate
  regime; no post-abolition fitting in the calibration.
* **Cost:** ~1–3 CPU-h at `N≈400`/`T≈70`.
* **Status:** **DONE on the fixed engine — ACCEPTED as a new-generation conditional simulation (REPRODUCED SIMULATION).**
  The v1 runner/calendar-year bug is fixed (`846c9e0`, canonical re-pin `46c080d`); this run uses `year_t=T0` and
  asserts `E.unfired_events == []` per arm. Results: abolition − persistence **+17.19, +20.97, +23.37, +25.03,
  +26.14, +26.18, +25.35 pp** (e=0..6); full-7 **RMSE 2.764 / MAE 2.432** vs persistence **23.759 / 23.260**
  (**−88.4 %**); held-out e=+5,+6 **RMSE 1.637 / MAE 1.350**. **Calibration caveat (binding):** training-only
  bisection was attempted and **failed** — the author's **74.88 % anchor is infeasible** in the repaired world
  (max 71.0 % at fee 0; at fee 0.15 pre-attendance 59.44 %, residual 15.44 pp) — so the documented fallback is
  manuscript fee 0.15 + engine pre-abolition level, **no post-abolition tuning**; held-out horizons reported
  separately. This is a **conditional simulation forecast**, not a reproduction of the author's calibration. v1
  numbers remain uncited. The paper's RMSE 5.13/4.68 vs 23.93 and impact +11.60/+13.48 are AUTHOR-REPORTED baseline.

---

## 4. New-generation evidence standard (apply to every item)

1. **Pre-registration** committed before the run: design, gates, seeds, grid, selection rule, pass/fail, what will
   be reported even if it fails.
2. **Hashes:** engine commit + every engine file sha256, config hash, seed list hash, output sha256.
3. **Provenance:** box/host, environment (py/numpy/scipy), workers, wall time, exit code; loud failure, no silent
   partials.
4. **Uncertainty:** seed (Monte Carlo) uncertainty reported separately from calibrated-parameter uncertainty.
5. **Baselines:** at least one no-policy baseline and one persistence/naive baseline; report the pre-repair
   generation when relevant.
6. **Sensitivity:** the assumptions that drive results (S grid, fee, vac0, N/T, gate spec) reported in a grid;
   declared perturbation grid for (d).
7. **Labels:** every table carries `NEW GENERATION (repaired engine, uncalibrated)` or `AUTHOR-REPORTED BASELINE`;
   never mix.

---

## 5. What already exists as new-generation evidence

| item | status | artifact |
|---|---|---|
| Repaired-engine 540 (legacy gate list) | REPRODUCED SIMULATION, uncalibrated | `results/audit/commander/hk_korea_540_REPAIRED_box98baf6b_2026-11-25.json` sha256 `455649da…`; `GATE1_MIGRATION_TABLE.md` |
| CF4 reversal | REPRODUCED SIMULATION | CF4a Win-Win both (HK 70.58/23.44; KR 72.48/21.47); CF1b fails (97.21/99.25); CF4b fails; CF3b passes |
| D2 calibration-artefact decomposition | REPRODUCED SIMULATION | expected/realised 2.41×/1.96× → 1.0000; KR gap 68.36 → 29.71; ratio 18.01 → 2.11; participation 57.44 → 58.38 |
| ABC identification audit | VALIDATED/RE-EXECUTED | rank 4/5, 2-dim null, 44 θ, analytic δ; local 5/5 after two moments |
| DGP corrected design | VALIDATED SIMULATION | rank 5/5 in 500/500; legacy 3/5 |
| Bootstrap size/power + invalid permutation | VALIDATED SIMULATION | pooled size 0.996–1.000; FE 0.052–0.062; within-invariance 6.66e-16 |
| E8 empirical block (author record) | VERIFIED EMPIRICAL | committed records `bd782be`/`fb8b67e`/`b4eb680` |
| **E8 fresh-WDI new generation (simple DiD)** | **REPRODUCED EMPIRICAL ANALYSIS** | impact +12.322 vs +12.44; simple-DiD post +2.54 (estimator sensitivity); `E8_BULGE_NEWGEN.md` sha256 `97734cdc…`; JSON `5c2439…`; WDI manifest `d7296e1f…` |
| **E8 fresh-WDI new generation (CS-style)** | **REPRODUCED EMPIRICAL ANALYSIS** | impact +12.322 (bootstrap mean 12.308, CI [4.48, 22.64]); **post +25.083 vs +25.26 (replicates)**; Fisher p 0.0044/0.0040; `CS_ESTIMATOR_NEWGEN.md` sha256 `04faf9dc…b196`; JSON `4ac9551d…1905` |
| **Bulge `t*` fresh-WDI** | **UNRESOLVED** (no-effect evidence) | ATT −0.956, post +0.30, p .251/.384 |
| Paper B 540 regenerated tables | REPRODUCED SIMULATION, uncalibrated | `PAPER_B_TABLE_REGENERATION.md`; csv sha256 `da40a2ee…` |
| Engine mid-run calendar-event fix | VALIDATED SIMULATION (numerics unchanged) | `846c9e0`; `ENGINE_MIDRUN_EVENTS.md`; `_validate_events`/`E.unfired_events`/`year_t`; new core sha `e111397b…`; 118-series identical; 27 qa tests; ENGINE_CHECKS 14/14; canonical re-pin `46c080d` |
| **Forecast (e) new generation** | **REPRODUCED SIMULATION (NEW GENERATION)** | abolition − persistence +17.19…+25.35 pp; full-7 RMSE 2.764 vs persistence 23.759 (−88.4 %); held-out e=+5,+6 RMSE 1.637; declared calibration fallback (74.88 % anchor infeasible, A-38); `FORECAST_NEWGEN.md` sha256 `d4c0a239…d8f1`; JSON `f0eee995…c04` |

**Adjudicator re-executions (host):** the ABC identification audit was re-run and its output is **bit-identical**
to the committed host JSON (`/tmp/abc_identification.json` sha256 `66bb2648…15808`; rank 4/5, 2-dim null, analytic
δ −0.7537718023763802, local 5/5). The bootstrap size/power factorial was re-run to exit 0 and its summary matches
the committed result to last-bit float (FE size median **0.05925**, pooled size under confounding **1.0**,
permutation within-invariance **6.661338147750939e-16**, `permutation_invariant=true`, `benchmark_matches=true`;
only date/runtime/last-bit differ). The corrected-DGP harness was still running under host load at finalisation; its
committed result (rank 5/5 vs legacy 3/5) stands and is labelled as the audit's.

---

## 6. Execution queue (proposed; owner = `atlas-commander` / engine lanes)

| order | item | prepare | run | acceptance |
|---|---|---|---|---|
| 1 | (c) gate architecture ≥5,000 runs | freeze config + pre-register (1 h) | server, 43–60 CPU-h | H1/H2 + inverted-U with seed CIs; all cells reported; hashes |
| 2 | (d) multi-seed Jacobian | write model spec + perturbation grid (1 h) | host, minutes–hours | rank/null space across seeds/perturbations; local-only statement; two-moment remedy |
| 3 | (e) forecast held-out | **DONE** (fixed engine; declared fallback) | — | held-out RMSE 1.637 vs persistence; 74.88 % infeasibility recorded (A-38) |
| 4 | (b) bulge `t*` | **DONE** — fresh WDI; no detectable jump | — | artefact hashed; report as no-effect evidence |
| 5 | (a) E8 fresh-vintage re-run | **DONE (both estimators)** — impact and amplification replicate under CS-style; simple DiD is sensitivity | — | artefacts hashed; report CS-style as primary, simple DiD as sensitivity |

---

## 7. Relationship to the legacy docx numbers — TWO columns only

The old docx numbers are the **AUTHOR-REPORTED BASELINE**. They are not deleted and not silently replaced. Every
new-generation table will show **two columns**: **Gemini docx (AUTHOR-REPORTED baseline)** vs **new generation
(ours, repaired engine, preregistered, hashed)**, with a **difference** and a **reason** for each row. There is **no
Codex column**. Template:
`docs/audit/PAPER_A_BASELINE_VS_NEWGEN_TEMPLATE.md`. The verified E8 empirical values are the one case where the
baseline is already independently confirmed; the new-generation run hardens provenance rather than changing the
numbers.

---

## 8. What the repaired engine contradicts in the legacy generation

The reimplementation is not neutral: the repaired engine already shows that several legacy claims do not survive.
For Paper B this is explicit — the **CF4 reversal** (CF4a Win-Win both; CF1b no longer passes), the D2 calibration
artefact (KR gap 68.36 → 29.71 without re-estimation), and the reversal of the tax/wage-compression signs. For Paper
A, the repaired engine's **exact PL expected probability** and **persistent G9 consequence** mean that a contest-gate
H2 result must be re-derived, not assumed; the old 1,640-run number is a baseline, not a result. Any new-generation
table must state this.

---

## 9. What not to do

* Do **not** cite the legacy Exp 1/3/4/5 numbers as results; label them AUTHOR-REPORTED BASELINE.
* Do **not** claim the original artefacts do not exist; say they were not found where searched and are no longer
  the blocker.
* Do **not** reconstruct from memory; every new-generation run needs a written spec and a pre-registration.
* Do **not** present the repaired 540 (`455649da…`, legacy gate list) as the frozen `canonical_spec.json` V540 run;
  that is a separate, not-yet-executed run.
