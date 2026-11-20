> **SYNTHETIC EXERCISE — INTAKE STANDARD.** Council acceptance criteria for predeclarations; not evidence.

# INTAKE ACCEPTANCE — E2, E3, M2c predeclarations (Council standard)

**Authority:** Council (protocol §5). **Deadline:** one cycle from assignment. **Rule:** a predeclaration is
**ACCEPTED only when every bullet below is present**; otherwise it is returned with reasons in the same cycle and the
cell does not run. Predeclarations must copy `SUCCESS_CRITERIA.md` §2–§4 and Amendment A1 verbatim, plus the data
and claim labels.

## Common (all three)

- [ ] **Data provenance:** exact series/path, vintage, observed-only flag, imputed/excluded cells named, role
      (fit/check/holdout) per SUCCESS_CRITERIA §2; no target used as a parameter; no imputed cell as observation.
- [ ] **Labels:** observed vs simulated stated; claims capped at the design (no direction claim from panels — R13;
      conditional reproduction labelled PASS-CONDITIONAL).
- [ ] **Rivals:** at least one fair rival/comparator named, with the same population, shock, information, outcome.
- [ ] **Decision rule:** predeclared numeric threshold(s) and what counts as FAIL/PARTIAL/EQUIVALENT.
- [ ] **Failure rule:** the specific stop-rule link (R1–R15) that fires on failure, and the action (no claim /
      descriptive downgrade / redesign).
- [ ] **Deliverables:** `NEW:` post with path, commit/hash, one-line finding, what it changes; `OP:` milestone.
- [ ] **No closed-claim content:** shadow-education claims not re-fit (closed by brief 008).

## E2 — PH K-12 2013 cohort-exposure event study (supply push)

- [ ] **Identifying variation:** K-12 phase-in by cohort (birth year) and/or region rollout; treatment/control
      definition; exposure intensity; pre-period ≥5 cohorts; event window; clustering level.
- [ ] **Estimand:** ATT of exposure on upper-secondary completion and tertiary transition (units, sample, years);
      plus a secondary outcome for falsification (e.g., a level/cohort unaffected by the reform).
- [ ] **Pre-trends test:** event-study pre-coefficients; joint test threshold (e.g., p > 0.10) and no monotone
      pre-trend; pre-2013 placebo cohorts; if pre-trends fail → no causal claim, descriptive only (R10).
- [ ] **Rival explanations tested:** demographic cohort change, SHS capacity/private provision, tertiary intake
      rules, measurement change in completion definitions; each with a predeclared test or a stated limitation.
- [ ] **Thresholds:** predeclared sign and minimum detectable effect; power calculation using observed variance and
      cluster count; if underpowered, declare it now and cap the claim at descriptive.
- [ ] **Fallback:** if `10_massification/data/` is still empty, E2 runs on the observed `04_data` fallback
      (GMR/UIS observed cells) — the fallback must be named in the predeclaration.

## E3 — PH nurse-visa demand-pull replication

- [ ] **Design:** the exact published identification (Abarcar & Theoharides 2024) restated: exposure (visa expansion
      timing), outcomes (nursing licensure per migrant; nursing program enrollment), sample, estimand, unit.
- [ ] **Replication rule:** reproduce the sign and order of magnitude within a predeclared factor (state the factor,
      e.g., ×2) of the published estimate; report the gap whether it lands or not; "unable" if series absent.
- [ ] **Data routes:** PRC licensure series, CHED program enrollment, the published design; missing series marked
      **DATA BLOCKED**, not imputed.
- [ ] **Rivals:** cohort/other-program controls, macro trends, migration policy changes; at least one placebo outcome.
- [ ] **Claim cap:** a replication tests whether the model's pull channel is consistent with a published causal
      design — it does not identify the system's direction (R13); label accordingly.

## M2c — E1-design recovery test (simulated, before E1 is fielded)

- [ ] **DGP:** a simulated two-shock process with **(a) demand-led, (b) supply-led, (c) complementary, (d) outside
      truth (neither / nuisance cohort-fertility)**; parameter grid (effect sizes, noise, N cohorts/regions, timing);
      fixed seeds; ≥ 100 reps per truth (or a power-justified number); all parameters declared.
- [ ] **Estimator:** the **exact E1 estimator** to be fielded (two-shock interaction DiD/event study), with
      specification, clustering, weights; plus a placebo estimator.
- [ ] **Estimands:** recovery rate (correct channel configuration selected); forced-ID rate (outside truth assigned
      to a candidate); complementarity detection rate; sign accuracy; power at the predeclared effect size.
- [ ] **Thresholds (predeclared, no post-hoc change):** recovery ≥ 0.80 (or the lower bound justified in advance);
      forced-ID = 0.00 for the outside truth; false-positive complementarity ≤ 0.10; complementarity effect
      detectable at the predeclared size (state it).
- [ ] **Failure rule:** if recovery < threshold OR forced-ID > 0 → **E1 is not sufficient**; do not field it; report
      the failure and either redesign E1 (new arms/estimator, new predeclaration) or abandon the direction claim
      (programme reduces to conditional reproduction + equivalence). This is an R3/R13 event.
- [ ] **Reporting:** all cells, including failures; no silent dropping; commit/hash in `NEW:`.

## Acceptance log

| item | owner | due | status |
|---|---|---|---|
| E2 predeclaration | exp1 | 1 cycle | pending |
| E3 predeclaration | exp1 | 1 cycle | pending |
| M2b declared partial re-run | exp2 | 1 cycle | pending (ACK required first) |
| M2c predeclaration | exp2 | 1 cycle | **must be accepted before M2c runs** |
| data partial panel | data-hunter | 1 cycle | pending (or DATA BLOCKED) |
| pattern-scout `NEW:` + PAGE caveat | scout | 1 cycle | pending |

**Return-with-reasons** applies in the same cycle: a missing bullet means the cell does not run and the owner is told
which bullet failed. The Council does not accept a predeclaration "in principle".
