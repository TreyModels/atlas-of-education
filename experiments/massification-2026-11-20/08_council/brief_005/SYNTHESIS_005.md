> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# SYNTHESIS 005 — iteration-2 partial results (for `lead`)

**Sign-off: conditional and narrow — the module may be published as a method + negative map, not as validation of
incidence, two-way feedback, or identification.** The partial set is enough to answer most of the questions, and
three of the answers are negative. The runner-1 layer (country configs, `CALIBRATION_TABLE.csv`, cohort ledger) and
both predeclared tests (recovery/forced-ID, 2011–2024 holdout) are absent and are marked `UNABLE TO ASSESS`.

## Restatement test (the key one) — FAILED at the one cell that is tested

| Shadow row (use_as_model_target=YES) | value | in model target dict? | checked? | verdict |
|---|---|---|---|---|
| KOR all levels | 78.5 | no | no | unused (KOR not simulated) |
| KOR elementary | 90 | no | no | unused |
| JPN primary G6 | 41.8 | no | no | unused (JPN not simulated) |
| **HKG senior secondary** | **85** | **yes — the fitted moment** | **fit, by construction** | **RESTATED** |
| KHM Grade 9 | 68.4 | no | no | unused; stage-matched model 0.887 ≈ miss +20 pp |
| KHM primary | 41.3 | no | no | unused (model 0.887 senior; no primary reporting) |
| KHM primary urban | 60.5 | no | no | unused |
| KHM primary rural | 26.4 | no | no | unused |
| PHL all basic | 46.5 | no | no | unused; model 0.899 college-gate ≈ +43 pp |
| PHL elementary | 23.8 | no | no | unused |
| PHL upper-secondary review centre | 28.1 | no | no | unused; model 0.899 ≈ +62 pp |

The register has **11** YES rows (not 6); the model wires in **one**, as the calibration target. So: one literature
shadow rate is coded as a parameter (through the fitted intercept), and the other ten are not even checked. The
model's PH/KHM take-up (88–89%) is a stage-level over-universalisation produced by that one intercept; the
uncalibrated HK rate (0.581, −26.9 pp) shows the fit is doing the work. **Do not say "shadow education appears where
the literature says"; the target exercise is a one-moment calibration with an unreported check table.**

## Answers

**(1) Shadow incidence by stage/provider/country — NOT ESTABLISHED.** One fitted cell; ten unused; stage-matched
PH/KHM levels contradicted; KOR/JPN not simulated. The one genuine positive is structural: provider entry with
teacher-tutor dominance (76/86/97%) emerges without fixed shares and is qualitatively consistent with the comparative
record — report as generated possibility, not validation. Positional response is null in this module (state as null,
not disconfirmation).

**(2) Cohort flows — UNABLE TO ASSESS.** The longitudinal cohort ledger is pending. The module's own targets are
mostly unresolved/proxy in `TARGETS_FLOW.csv`; where observed, it misses (PH completion −8.9 pp; KHM +9.9 pp; KHM
formal share +14.0 pp; KHM university proxy +17.5 pp). Nothing about conservation can be said yet.

**(3) Two-way feedback — IMPOSED ON THE JOB SIDE, GENUINE ON THE EDUCATION SIDE.** Freezing schooling leaves complex
vacancies rising strongly (PH 71.0→130.9; HK 172.8→235.8; KHM 32.3→80.0); endogenous schooling adds +4.5/+6.5/+3.1
jobs (≈3–4%). Freezing the economy leaves attainment rising +0.028/+0.022/+0.024 (vs +0.067/+0.118/+0.077 live) — a
shadow-supply residual of ≈20–40%, an upper bound per the first-order counterfactual. The module is therefore
asymmetric: economy→education is a model; education→economy is approximately a schedule. Direction: HK demand-led
(Ec_dir +0.098, 2sd 0.014); PH/KHM neither (effects ≈0). One country is a demonstration, not a pattern.

## Amendments (minimum, before any iteration-2 result is cited)

1. Replace "two-way feedback" with "asymmetric feedback: education→economy is schedule-like (3–4%); economy→education
   is genuine, with a 20–40% shadow-supply residual (upper bound)".
2. Report a stage-matched check table for all 11 shadow targets with confidence flags; label HK 0.85 a calibration and
   exclude it from incidence claims; disclose the PH/KHM over-universalisation as a miss.
3. Mark cohort flows, calibration table, holdout (L2-5) and recovery/forced-ID (L2-4) `UNABLE TO ASSESS`/pending.
4. Fix intake discrepancies: 11 YES (not 6); entry effect 54–67 pp (not 46–66); price/entry overshoot (prices at
   floor, providers 5–90×) must be in the main text, not only the error log.
5. Hedge "HK demand-led" as a within-module classifier outcome and name the pending holdout/recovery.
6. Keep the positional null as a null; do not use it against the paper's positional claim.

## Next 3 experiments (arms / estimand / threshold / cost)

1. **Stage-matched shadow check table (all 11 rows; +KOR/JPN or mark unassessed).** Arms: baseline vs
   country-specific demand-intercepts; estimand: take-up by stage × provider vs predeclared range; threshold: ≥2 of 4
   countries outside the predeclared range ⇒ stop claiming shadow incidence; cost ~10–15 min (KOR/JPN configs +
   stage-level reporting).
2. **Holdout + recovery (L2-5, L2-4).** Arms: fit intercept/parameters to 1980–2010 PH/KHM observed completion;
   hold out 2011–2024; recovery with 4 truths including one outside the candidate set. Estimand: held-out MAE by
   country and recovery share / forced-ID rate; threshold: recovery share ≥0.67 with forced-ID = 0 (or reported);
   cost ~20–30 min.
3. **Price/entry calibration.** Arms: entry-cost/capacity grid vs fixed supply; estimand: price level, provider count,
   teacher share vs observed price/fee moments (KHM teacher fees, PH review-centre fees — data thin, likely
   `UNABLE TO ASSESS`); threshold: price inside observed range, or mark unassessed and report entry effects only
   qualitatively; cost ~15 min + data.

**Most publishable:** the asymmetric-feedback negative plus the restatement audit (methods + negative map).
**Most falsifiable:** the stage-matched shadow checks — they can kill the shadow-incidence claim outright.
**Bridge:** partial-results verdict posted to `all` (party `deepseek-research`).
