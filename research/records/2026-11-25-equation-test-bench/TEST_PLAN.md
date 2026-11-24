# TEST PLAN — statistical equation test bench (pre-registered, before any run)

**Task-43.** Branch `research/equation-test-bench-2026-11-25` (from handoff `e8ba60c`). Data map:
`research/full-system-data-2026-11-25` @ `34fd7c9`. **No causal claims; no invented targets.** SIMULATION /
OBSERVED labels as marked; every family gets a verdict **SUPPORTED / NOT IDENTIFIED / REJECTED / UNTESTABLE**.

## Global rules (binding)
1. **Estimand + identification stated before estimation**; no post-hoc switching.
2. **Splits:** leave-country-out (LCO) and time-block (earlier → later) for every Tier-A test; no row-level random CV.
3. **Benchmarks:** persistence (last observed value) and linear-trend forecasts per series, plus a NULL (no-effect / zero-coefficient) placebo; model must beat both out-of-sample.
4. **Uncertainty:** cluster-robust by country (or DHS cluster where applicable); 95 % CIs.
5. **Multiverse/specification curve:** 12 pre-declared defensible variants per family (winsorisation, FE structure, control set, windows, weighting, level/difference, log form); a result is "supported" only if ≥ 80 % of variants keep the same sign and the OOS advantage holds in ≥ 80 %.
6. **Negative controls:** where possible, permute country labels or use a lagged placebo target; a real relationship must not appear in the placebo.
7. **Tier B:** synthetic recovery/coverage/power with known parameters; report bias, coverage of 95 % CI, confusion; failure → NOT IDENTIFIED.
8. **Tier C:** no data/construct → UNTESTABLE with the explicit reason; no fake tests.
9. Failures/nulls preserved; seeds, hashes, logs recorded; server run ≤8 workers, do not shut down.

## Families (10) — pre-declared design

| # | family | estimand (observational) | identification | testable restrictions | data | benchmark | tier |
|---|---|---|---|---|---|---|---|
| 1 | household demand/affordability | enrolment/attendance association with household resources | cross-country ecological only; no micro public | sign/magnitude of income gradient; no fee instrument | WDI/EdStats + DHS API aggregates | persistence/trend/null | **A (ecological) + C** (micro affordability UNTESTABLE) |
| 2 | school/state supply & finance | enrolment association with teachers/PTR/spending | within-country change + LCO | PTR and teacher-share signs; no capacity data | UIS/EdStats (PTR, teachers, private share, spending) | persistence/trend | A |
| 3 | education production/learning | learning outcome association with inputs | cross-section assessment anchors only | assessment-year input associations; scales not equated | PISA/TIMSS/SACMEQ anchors + HCI/LP | null + persistence | A (anchors) + C (grade-level annual profile) |
| 4 | stage transitions/gates | transition/completion association with schooling & supply | ecological; no exam rules | completion/transition signs; no gate rule data | EdStats CMPT/TRAN + UIS | persistence/trend | A (proxy) + C (exam gates) |
| 5 | returns/credentials/jobs | wage/employment association with education | cross-country ILOSTAT; no panel | wage-premium sign by level; credential requirements absent | ILOSTAT wages by education + repo credential-floor | null + trend | A (premia) + C (credential requirement) |
| 6 | structural change & growth | schooling vs demand-first ordering; growth association | cross-country; E6 timing | demand-first shares reproduce E6; growth assoc sign | GGDC/PWT + E6 record `bd782be` | trend/persistence | A |
| 7 | inequality/mobility | schooling inequality association with attainment dispersion | cross-country; imputed cells | Gini/attainment dispersion sign | WID/SWIID (labelled reconstructed) + Barro-Lee | null/trend | A (reconstructed tier) |
| 8 | tutoring/shadow (one row only) | shadow-education prevalence assoc with crowding/quality | cross-country/selected surveys | tutoring assoc sign with PTR/quality | repo shadow-education record + DHS/STEP where present | null/persistence | A (selected) + C (causal) |
| 9 | fertility/health associations | schooling↔CEB/health at individual/ecological level | DHS API ecological; IR gated | gradient sign, cohort/round FE; EFR vs TFR construct split | DHS API aggregates + E11 record `e926575` | persistence/null | A (ecological) + C (individual, gated) |
| 10 | measurement/attainment (LAYS) | attainment/learning measure association with enrolment | cross-country; composite | LAYS vs completion sign; measurement-error model | WB HCI/LP + Barro-Lee + UIS | null/trend | A (measurement) + B (error-model recovery) |

## Decision rule (fixed)
- **SUPPORTED** iff (i) OOS beats persistence AND trend AND null benchmark on the pre-declared test years, (ii) cluster-robust 95 % CI excludes the null-effect value in the pre-declared direction, and (iii) ≥80 % of the 12-variant specification curve agrees in sign with the OOS advantage.
- **NOT IDENTIFIED** iff the estimand cannot be separated from benchmark/confounders under Tier A, or Tier B recovery fails (bias/coverage poor) where a synthetic test is the only route.
- **REJECTED** iff OOS fails to beat benchmarks or the sign is opposite to the claim in ≥80 % of variants.
- **UNTESTABLE (C)** where data/construct are absent (no invented proxies).

## Run protocol
Server `ssh -p 45973` (key only; **do not shut down**), `/root/work/testbench/`, ≤8 workers, BLAS=1, logs +
hashes preserved. Mac orchestration only.

## Deviations log
- (to be filled)
