# NEW-GENERATION PREREGISTRATION — Atlas shadow-education programme (frozen 2026-11-25)

**Authority:** operator/Lead directive 2026-11-25: reproduce what Gemini was attempting, bigger and better, on the
repaired engine, using the server; old docx numbers stay **AUTHOR-REPORTED** baseline; all new runs are a **NEW
GENERATION** (not reproductions, not validations of the originals). Registered **before launch**; deviations must be
logged, not silently absorbed.

## 0. Frozen computational base (no changes without an amendment)

| item | value |
|---|---|
| engine tree | clean `git archive 98baf6b` (gate1a `f31e176` + gate1b `6bc8d61` + gate1c `1a6f3d5`/`23a0173`); file hashes: core `72cbddf7…`, rng `ada4a760…`, contest_math `23a01730…`, tutoring `7a6fd4c3…`, labour `0ccfb3ce…`, planning `13d91bc9…` |
| spec artefact | `docs/audit/canonical_spec.json` (content sha256 `c5f9e2de1c04b4ef467f4e9016c942616f7c7e67f94bc3a08be9bbd7b2f34a05`; file sha256 `35576fed0c132041f8ddbf60d1177f2734a16c3047047169872c6a261fa7b95f`) — **V540-FREEZE**, N=300, T=46, measure_from=18 |
| gates | HK: legacy 540 HK gates; KR primary: `GATE_SPECS['KR-TRACKED']`; KR sensitivity: `GATE_SPECS['KR-SINGLE']` |
| env | box 10-CPU cgroup; `/root/work/venv-declared` py3.10.8, numpy 2.2.6, scipy 1.15.3; `nice -n 10`; OPENBLAS/MKL/OMP=1; ≤10 workers total, ≤4 per lane |
| seeds | matched integer seeds; Paper B primary: **0–99 (100 matched seeds)**; sensitivity: same list |
| code provenance | every output records the engine/spec hashes above + runner sha256 + wall + workers; staged per-arm checkpoints (atomic), no silent partials |

## 1. Paper B — NEW GENERATION (primary + sensitivity)

**Design (new generation):** 18 pre-declared arms (Baseline; CF1a +50 % tax/price; CF1b cap −50 %; CF2a/CF2b
seat-share; CF3a/CF3b wage-compression; CF4a wage+cap; CF4b wage+seats) × {HK, KR} × **100 matched seeds = 1,800
runs** (KR-TRACKED primary), plus **KR-SINGLE sensitivity**: 9 KR arms × 100 seeds = 900 runs (HK unchanged under
the sensitivity; documented, not re-run).

**Outcomes (all pre-declared):** K-12 participation rate; Grade-12 participation; Q5−Q1 participation gap (pp);
Q5/Q1 per-student tutoring spend ratio; mean K-12 household tutoring spend; **elite-track Q5 admission share**;
contest-prep effort; and per-quintile participation/spend (Q1..Q5). **Primary contrast:** CF4a vs Baseline on
(spend, elite-Q5) under the pre-stated Win-Win criterion (spend index < 80 AND elite Q5 below same-jurisdiction
Baseline, both jurisdictions); CF4b, CF1b, CF3b as secondary contrasts. **Multiplicity:** 9 arms × 4 headline
outcomes × 2 jurisdictions — report all, label the pre-stated primary (CF4a) and flag the rest as secondary; no
post-hoc primary switching.
**Uncertainty:** Monte-Carlo/seed uncertainty (sd, 95 % CI across 100 matched seeds) reported **separately** from
calibrated-parameter uncertainty (Gate-2 calibration CIs; none applied here — parameters are frozen, so this stage
has **zero calibrated-parameter uncertainty** and must say so).
**Baselines:** the same frozen engine on Baseline arms; the old 540 pre-repair/legacy-gate numbers kept visible as
AUTHOR-REPORTED comparators only.
**Held-out:** no fitting in this stage; the Paper-A/new-generation cross-checks below are the out-of-sample tests.
**Sensitivity axes:** KR-TRACKED vs KR-SINGLE (gate design); seeded uncertainty; (post-hoc) gate-parameter
magnitudes are reported, not tuned.
**Expected compute:** 2,700 runs × ~31 CPU-s avg ≈ **23 CPU-h ≈ 3–3.5 h at 8–9 box workers** (measured costs:
HK 20.3 CPU-s, KR 41.9 CPU-s; no speed-up assumed).
**Reporting:** CF4 reversal vs the 540 pre-repair result (old failure preserved); all arms; quintile tables; MC vs
parameter uncertainty; provenance hashes. Label: **NEW GENERATION — REPRODUCED SIMULATION (repaired engine, frozen
spec), NOT a reproduction of the 420 docx tables.**

## 2. Paper A — NEW GENERATION (the five intended computations, bigger, explicitly NEW where undocumented)

All five are **new experiments** defined here; none claims to reproduce Gemini's undocumented parameters.

**(a) Fee-abolition event-study simulation.** Engine: repaired engine, education-system world with public/private
supply and tutoring; primary fee_public set by an event: 0.19 → 0.00 at t0 for a "treated" cohort set; 40 matched
seeds × 8 synthetic "countries" (parameter draws over income/subsistence/urban share, drawn from a pre-declared
grid, hashed) — **320 runs**; outcomes: primary GER/participation by horizon e=0..+6, quintile gaps. Contrast:
abolition vs persistence. Label: NEW sim; empirical E8 numbers used only as external comparison, AUTHOR-REPORTED.

**(b) Delayed secondary-bulge `t*` with fresh WDI download.** Download (hashed, timestamped) WDI indicators
`SE.PRM.ENRR/SE.PRM.REPT.ZS/SE.SEC.PROG.ZS/SE.SEC.ENRR/SE.SEC.ENRL.TC.ZS` 1990–2020; compute arrival year
t* = abolition + L_primary; Callaway–Sant'Anna-style event study around t* with country/date placebo permutations
(2,000 per scheme, seeds fixed); report estimability per indicator. This is an **empirical re-analysis with fresh
data**, not a simulation; label REPRODUCED EMPIRICAL ANALYSIS if it runs on hashed WDI data.

**(c) Gate-architecture experiment ≥ 5,000 runs.** Repaired engine; gate regimes {bar, bar_high, quota, contest};
seat shares S ∈ {0.25, 0.35, 0.45, 0.55, 0.70}; fee regimes {0.00, 0.19}; vacancy rates vac0 ∈ {0.02, 0.08, 0.25,
0.50}; ≥25 matched seeds per cell; total ≥5,000 runs. Outcomes: Q5−Q1 tutoring gap post- vs pre-abolition (Δcut);
**H2 = Δcut(S=0.25) − Δcut(S=0.70)**; H1: monotone widening as S falls. Design is declared NEW (Gemini's exact
parameterisation undocumented); priors/parameters fixed in the prereg appendix before launch. Compute ≈
5,000 × 35 CPU-s ≈ 48 CPU-h ≈ 6 h at 8 workers.

**(d) Identifiability / Jacobian — multi-seed.** Frozen spec calibration map: θ = (contest_price, contest_alpha,
G9-track prize, y_median) × 4 moments (KR participation, KR gap, KR spend ratio, HK Grade-9 participation);
**multi-seed Jacobians** (≥5 matched seeds per column, central differences, declared step sizes 5 %/3 %/5 %/4 %),
rank/SV/null-space across ≥3 starting points; report condition numbers only as diagnostics, **never as identification
evidence**. This directly addresses the G2-A caveat (one-seed rank 4/4 unstable, max|ΔJ| 26.5).

**(e) Fee-abolition forecast with genuine held-out period.** Fit/condition on pre-abolition period only; forecast
7 horizons; hold out the last ≥3 horizons from any tuning; report RMSE/MAE vs persistence on the held-out horizons
(and full 7-horizon for comparability to the AUTHOR-REPORTED 78.6–80.5 % claim). New design, 40 seeds.

## 3. Evidence labels (mandatory wording)

* Old Gemini docx tables (420 and Paper B) and Paper A Exp1/3/4/5 numbers: **AUTHOR-REPORTED / UNVERIFIED**.
* All runs launched under this preregistration: **NEW GENERATION — REPRODUCED SIMULATION** (repaired engine, frozen
  spec). Not "VALIDATED", not "a reproduction of Gemini".
* GPU/ABC/P0 findings: QUARANTINED unless revalidated; measured numbers (rank 4/5, pooled size ≈1.0 vs FE 0.05–0.06,
  permutation within-invariance 6.66e-16) are cited from our own executed audits.
* Any unexpected result is preserved and reported; no silent re-runs to "fix" signs.

## 4. Preregistration amendments log

| # | date | change | reason |
|---|---|---|---|
| — | 2026-11-25 | initial registration before launch | operator directive |
| A1 | 2026-11-25 | adjudication fold-in (claim labels, budgets, review gate) committed before launch | adjudication `32718ba` |
| A2 | 2026-11-25 | engine re-pin `98baf6b` -> `846c9e0` (mid-run calendar-event fix; core `e111397b…`; numerics unchanged): Paper B and g2a runs remain on `98baf6b` and are labelled so; gate grid and forecast rerun use `846c9e0` | engine-core `846c9e0`; 27-suite PASS; max|Δ|=0.0 |

## 5. Addendum A1 — adjudication fold-in and budget (before launch, 2026-11-25)

**Authority:** adjudication `32718ba` (`AUDIT_VERDICT.md`, `PAPER_A_VERIFICATION.md`, `PAPER_B_ADJUDICATION.md`,
`paper_claims.csv`). Legacy manuscript numbers are the **AUTHOR-REPORTED BASELINE**; the repaired runs are the
**NEW GENERATION**; nothing below implies reproduction of Gemini.

**Paper A baseline labels:** 4 **VERIFIED EMPIRICAL** (E8 block only: +12.44 impact, +25.26 post, RI p 9.999e-05 /
5.999e-04, gender −3.94 [−8.72, +0.29]); 20 AUTHOR-REPORTED; 8 **CONTRADICTED even as baseline** (flat pre-trends,
gender-IV, theorem 7/7, condition-number identification, out-of-sample validation, legacy DGP/ABC). The E8 empirical
block may be used as an external comparator only, with its cited provenance; the contradicted items may not be cited.

**Paper B baseline labels:** 8 REPRODUCED (540-generation only); 18 AUTHOR-REPORTED (420 tables); 14 CONTRADICTED —
every policy headline reverses/dissolves under the repaired/540 work (tax backfires→spend falls; wage compression
regressive→falls; CF1b→fails spend; CF4a→Win-Win both; CF4b fails; CF3b passes). Old 420/540 tables remain visible
as baseline only.

**Reimplementation budget (used for scheduling):** (a) E8 fresh-vintage event study — READY, ~1–2 CPU-h; (b) bulge t*
— **DATA-BLOCKED** (needs fresh hashed WDI/UIS + L_primary; not launched); (c) gate architecture ≥5,000 runs —
**43–60 CPU-h** (≈5.5–7.5 h at 8 workers); (d) multi-seed Jacobian — ~2–6 CPU-h; (e) forecast with held-out —
1–3 CPU-h. Combined A-side ≈47–71 CPU-h; scheduled after/alongside Paper B (26 CPU-h for 2,700 runs).

**Prereg review gate (binding, from AUDIT_VERDICT §4C):** reject any design that (i) keeps the rank-4/6
advertised-moment structure without a rank audit, (ii) leaves the empty G12×urban cell / omits school IDs (the
"smarter Paper A" must use a crossed grade×urban population with school random effects), (iii) uses the pooled
selftest instead of FE + WCR/whole-trajectory bootstrap, or (iv) uses country-block permutation (within-invariant
under FE). The Gate-2 design uses crossed synthetic populations with school IDs (per P0-03), FE + wild-cluster /
whole-trajectory bootstrap (per P0-04/05), and multi-seed Jacobians — these are recorded as *satisfied by design*.

**Publishability (recorded):** neither manuscript is submittable; Paper A → E8 empirical short + measurement
conjecture after (c)–(e); Paper B → methods/negative paper after Gate-2/3. No citation of 420 tables, H2 numbers,
theorem, simulator RMSE, t* null, or GPU/ABC outputs.

**Label rule for anything launched before this addendum:** EXPLORATORY; re-reported under the preregistered label
once the addendum is committed. This addendum commits before the Paper B launch.

## 6. Amendment A3 — Paper A (c) gate-architecture: adjudicator conditions applied (pre-launch)

**Authority:** adjudicator conditional approval `456ecac` / Lead instruction 2026-11-25. This amendment is committed
**before** any fee-contrast run.

**Design (final):** repaired engine **pin `846c9e0`**; declared NEW world N=300, T=20, T0=12, measure_from=4,
start_year=0; gate under test = G6→G9 transition; **4 architectures** {bar, bar_high, quota, contest} × **S**
{0.25,0.35,0.45,0.55,0.70} × **fee** {0.19 kept, 0.00 abolished at T0 via `year_t`} × **vac0** {0.02,0.08,0.25,0.50}
× **32 matched seeds** = **5,120 runs (primary, `fail='track'`)**; plus a declared **`fail='stop'` sensitivity block**
(contest only, S∈{0.25,0.70}, all vac0, both fees, 32 seeds = **512 runs**) for a total of **5,632 runs**.

**(1) Fail routing declared:** primary `fail='track'` (matches canonical KR G9-track vertical-tier design; failing the
gate places the child on the non-elite track rather than removing them), so the Q5−Q1 tutoring gap is not confounded
with dropout/selection. The `fail='stop'` block is a declared sensitivity factor (dropout routing), reported separately.

**(2) POST window:** e = **+1…+6** (years 13–18), matching the paper's 7-horizon post window; no truncation.

**(3) Primary estimand / uncertainty (pre-declared):**
* **Primary H2** = `Delta_cut(contest, S=.25) − Delta_cut(contest, S=.70)` at **vac0=.08, fail='track'**, where
  `Delta_cut = gap_delta(fee=0) − gap_delta(fee=0.19)` with **paired seeds** (same seed index for both fee cells), and
  `gap_delta = post(e=+1..+6) − pre(T0−4..T0−1)` Q5−Q1 K-12 tutoring-participation gap (pp).
* **Uncertainty = paired-seed bootstrap 95 % CI** (5,000 resamples of the 32 matched seeds, pairing fee cells by seed);
  the **MDE proxy = bootstrap 95 % CI half-width** of the primary H2 (reported); seed sd/CI also reported.
* **Secondary:** quota H2 (same construction), the per-vac0 Delta_cut curve for contest, and **H1** =
  `gap_delta(fee=0, S=.25) − gap_delta(fee=0, S=.70)` plus a **Spearman monotonicity statistic** of fee=0 `gap_delta`
  across S (pre-stated: widening as seats shrink).
* **Exploratory only:** bar / bar_high "H2" (their S is a bar-threshold mapping, not a realized seat share) — reported
  with **realized admission rates** per cell, never as the paper's H2.
* **Multiplicity:** exactly one pre-stated primary (contest H2 at vac0=.08); everything else is secondary/exploratory;
  no post-hoc primary switching.
* **Null-reporting rule:** the pre-repair +0.1086 is the **AUTHOR-REPORTED baseline**, not a target; a null or negative
  repaired-engine H2 is a result to report, not a failure.
* **Achievable MDE:** with 32 matched seeds the primary H2 CI half-width is the reported MDE proxy; if the estimated H2
  is small relative to it, the result is **inconclusive**, not evidence of no effect.

**Provenance recorded in the output:** archs/shares/fees/vacs, N, T0, T, measure_from, start_year, engine_commit,
`engine_core_sha256`, spec sha256, runner sha256, event_key `year_t`, per-run `event_log`, quintile×urban cell counts,
gate applicants/seats/admit rates, per-run `E.unfired_events == []` assertion, realized r/alpha in `gate_spec`.

**Four Codex criticisms — explicit positions for (c):** (i) **no identification claim** is made from (c); the 4θ map
limitation and the 6-parameter ABC rank-4/6 criticism are recorded elsewhere and are **not** addressed by this
experiment; (ii) grade×urban **cell counts are reported as a design check**, not used as an estimation population
(no empty synthetic cell enters any estimator); (iii) uncertainty is **seed Monte-Carlo only** — no pooled/FE selftest
claim is made; (iv) **no permutation inference / country blocking** is used (this is a within-engine simulation).
