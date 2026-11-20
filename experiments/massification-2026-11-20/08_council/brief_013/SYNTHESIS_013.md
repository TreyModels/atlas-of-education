> **SYNTHETIC EXERCISE — DESIGN REVIEW.** Panelists are AI-constructed composite personas whose positions are
> inferred from the published literature. Nothing here is a statement by, or endorsed by, the named individuals or
> any living person. Design proposals are labelled as design; no fabricated numbers.

# SYNTHESIS 013 — design review: massification-first push-pull programme

## Step-back (mandatory)

1. **First-order goal.** A longitudinal model in which massification/universalization is produced by the
   interaction of schooling, government and markets — each standing the others up — with cohort flows and
   country/sector variation; shadow education is secondary and its closed claims are not re-fit.
2. **Active threads — KEEP / PARK / KILL.** **KEEP:** the gate (SUCCESS_CRITERIA + STOP_RULES); E1 two-shock
   push-pull; E2 PH K-12 cohort exposure; E3 PH nurse-visa demand; E4 sector-demand Bartik (deferred); E6
   scaling-form test (constraint); pattern-scout universalization fits and model2 scaling (provisional intake);
   tasks 34/35 data and lit; country cards/targets. **PARK:** E5 lead-lag panel; E7 staggered reforms; complexity/ECI
   axis; T1 two-margin paper support; T2 legitimation vignette; the shadow flagship paper rewrite. **KILL:** E8
   sectoral-transformation descriptive workstream (cannot change whether the model reproduces massification; no
   discriminating test — appendix at most); shadow-education incidence/mechanism threads (closed by brief 008; cite as
   prior only).
3. **The one thread that most advances the model this cycle:** Phase-1 **E2 + E3** execution (supply and demand
   separately identified), with **E1** as the integration test that follows — without them the model cannot claim the
   schooling↔market interaction that is the first-order goal.
4. **Drift check.** The previous cycle was measurement-heavy (T1 Korea decomposition) and this one opened with a
   definition gate — **one red flag** (measuring vs modelling). Mitigation: the gate is time-boxed to this cycle and
   the next action is experiment execution, not more measurement. No closed claim reopened; no parameter ordered
   without a discriminating test; ECI and paper threads are parked and cannot become the niche.
5. **If only one thing mattered this week:** execute E2 + E3 and predeclare E1; drop E4–E8, ECI and paper tasks
   until Phase-1 reports. Live list: `08_council/BIG_PICTURE.md`.

**Status.** This is the Council's design verdict and the gating document for the new phase. The **binding gate** is
`SUCCESS_CRITERIA.md` (operational definition of "reproducing universalization") plus `STOP_RULES.md` (R1–R12),
both declared before any fit; task-37/38 are cleared on those terms (COUNCIL message posted). Shadow education is
secondary: the prior phase's close-out stands and is not re-fit.

## 1. Design verdict — what must be different so this is not a re-parameterisation

The previous phase failed for an identifiable reason: it fitted first and asked whether the fit identified anything
afterwards. Its own results (C1 equidistant fits and forced-ID; gate-architecture and provider-technology failure;
shadow incidence unidentifiable; 8/9 stop rules fired) are the specification for what not to repeat. The
massification-first programme must adopt six rules **before** fitting:

1. **Identification before calibration.** The first products are exogenous-variation designs (reform timing, cohort
   exposure, sector-demand shift-share), not model fits. The model is fitted only after the reduced-form
   push/pull estimates exist and are predeclared as targets or checks.
2. **New moments, not more moments of the same aggregates.** National time series are already known to be
   insufficient (prior phase). The new information must come from **within-country variation** (cohorts, regions,
   sectors) and from **shocks** (supply and demand), with a predeclared discriminating prediction.
3. **Fit/check/holdout declared before fitting** — PHL/CHN 1980–2010 fit; PHL/CHN 2011–2024 and **all KHM** holdout;
   KOR/HKG/JPN check-only; no series both fit and holdout (SUCCESS_CRITERIA §2).
4. **Scaling relations are constraints/checks, not supplied schedules.** If the model needs the relation as an input
   to reproduce it, it has restated it, not found it (STOP_RULES R4).
5. **Equivalence is a publishable result, not a failure to hide.** If push and pull rivals fit the same moments and
   no new discriminating moment separates them, the outcome is observational equivalence (R3), which is the honest
   product — the prior phase's only defensible output, now applied to massification.
6. **The model must beat naive benchmarks and the false-positive test** (no universalization where none occurred);
   otherwise no country or general claim.

**Moments that are not used in fitting (declared now):** PHL/CHN 2011–2024 completion; all KHM series; KOR/HKG/JPN
completion/attainment (check-only); universalization crossing years; sector-share series in the holdout window;
every series marked `unresolved` in `04_data/TARGETS_*.csv`; the shadow-phase calibration moments (HK 0.85).

## 2. Push-pull identification

**Fair rivals (must be run, not caricatured):** human capital (schooling→productivity→jobs); world culture/diffusion
(policy scripts and adoption); labour-queue/credentialism (jobs→credentials→schooling); skill-biased demand and
sectoral transformation; migration/remittance demand; state-building/political order (Paglayan); demographic cohort
pressure. Each gets the same population, shock, information and outcome, and the same elasticity/parameter ranges.

**Observational-equivalence traps (predeclared):** common macroeconomic shocks; reverse causality (jobs↔schooling);
selection into schooling and into jobs; measurement (enrollment vs attainment; GER denominator; sector
reclassification; attainment modelled vs survey); staggered-reform TWFE bias (use modern DiD estimators);
composition/cohort effects; migration/remittances; policy endogeneity; ecological inference from national means.

**What identifies what (design):**
- **Push (schooling→jobs/growth):** supply shocks — compulsory-schooling extensions, school-construction
  programmes, K-12 extension (PH 2013), tuition/fee abolition, teacher-supply expansions. Outcomes: completion,
  transition, formal/sector employment, growth. Use cohort exposure and regional rollout; pre-trends and placebo
  outcomes required.
- **Pull (jobs/markets→schooling):** demand shocks — sectoral growth (shift-share/Bartik), FDI/industry openings,
  licensing/registration changes, foreign credential demand (nurse visa expansion), public-sector hiring.
  Outcomes: enrollment, completion, transition, field choice.
- **Minimal convincing design (the one a referee accepts):** a **two-shock design** in one country — a supply shock
  and a demand shock that hit **different** cohorts/regions or the same cohorts from opposite sides — with four
  cells (supply-only, demand-only, both, neither), predeclared signs, pre-trends, placebo outcomes, and an
  interaction term that is **the** estimand. One shock identifies one direction; the two-shock interaction identifies
  complementarity vs substitution and rules out the "everything is common trend" objection. See E1 in the slate.

## 3. Scaling laws — candidate laws vs regularities (with provisional on-disk evidence)

**Provisional intake (files on disk; noted as not yet `NEW:`-ACKed):**
`10_massification/relations/data/universalization_fits.csv` and `universalization_common_shape.csv` (pattern-scout;
post `NEW:` pending). PHL fits: GER secondary Gompertz better shape (K≈92.6, r≈0.044, t0≈1964; full-sample
RMSE≈2.51, r²≈0.96; holdout 2011–24 RMSE≈5.98, MAPE≈5.5%); GER primary logistic K≈104.3, r≈0.087, t0≈1941
(holdout RMSE≈9.79, MAPE≈9.0%); GER tertiary fits are unstable (K_se≈171, t0_se≈147; holdout MAPE≈18%); upper-secondary
logistic K≈77.0, r≈0.110, t0≈1985 (holdout MAPE≈5.5%). Common-shape test: country-specific slopes **rejected** for
secondary (p≈0.0024) and tertiary (p≈0.0); **not rejected** for upper-secondary (p≈0.059) and NER primary (p≈1.0,
low power). Model2 predeclares four independent scaling estimators and a law/regularity/unidentified classification.

**Verdict on laws.** (i) **Accounting identities and mechanical lags are laws** (attainment = f(completion,
mortality, migration); completion lags enrollment by cohort length). They constrain the model exactly and cannot be
fitted. (ii) **Bounded diffusion (logistic/Gompertz) is a candidate form, not a law**: at most it is a
*common-shape-with-country-specific-timing* regularity; the secondary/tertiary common-shape tests reject shared
slopes, and logistic vs Gompertz does not settle — the model must not hard-code either. (iii) **Income-education and
sector-share elasticities are regularities** with Asia heterogeneity (brief 009: R04 income→tertiary 0.848 world/Asia
1.075; R05 income→secondary 0.154; R07 fertility→completion −0.189; R13 education→growth **negative** in the panel).
A "law" requires sign and magnitude stable across estimators × samples (the model2 classification); otherwise it is a
period/region regularity.
**Falsifiers:** out-of-sample failure of the shape; parameter drift across periods/countries; sign reversal of a
regularity; model requiring the relation as an input (R4).
**How they constrain (not supply):** (a) excluded moments for fit and holdout targets; (b) sign/inequality
constraints the model must satisfy (e.g., education→growth must reproduce the panel's negative sign rather than the
model's `eps_ec>0` prior; income→tertiary positive; spending→primary null); (c) out-of-sample targets (fit PHL,
test KHM); (d) benchmarking against the fitted logistic/alternative shapes.

## 4. Operational definition of "reproducing universalization"

Registered in `SUCCESS_CRITERIA.md` (binding). In one line: *the model generates the observed
massification/universalization crossing, with midpoint within ±5 years and final level within ±5 pp, on a held-out
country (KHM) and period (2011–2024), beating persistence and linear-trend benchmarks, with no false universalization
where none was observed, and with exact cohort conservation.* Series/roles/tolerances in §2–§3 of that file; the
PASS/PARTIAL/FAIL/EQUIVALENT vocabulary in §4. **Task-37/38 fit only after ACKing it.**

## 5. Ranked experiment slate (summary; full fields in `EXPERIMENT_SLATE.csv`)

| Rank | ID | Design | Identification value | Feasibility |
|---|---|---|---|---|
| 1 | **E1** | PH two-shock push-pull: K-12 2013 supply × health-worker visa demand, 4 cells, interaction estimand | Highest — only design that separates both directions | Medium (3–4 wks data) |
| 2 | **E2** | PH K-12 cohort-exposure event study (supply push) | High — clean cohort variation, pre-trends testable | High (1–2 wks) |
| 3 | **E3** | PH nurse visa-expansion replication (demand pull) | High — published causal design; tests pull channel | High (1 wk) |
| 4 | **E4** | Sector-demand Bartik exposure → schooling (PH/KHM) | High — within-country demand variation | Medium (3–4 wks; PHL data access risk) |
| 5 | **E6** | Scaling-form test: logistic vs Gompertz vs linear vs exponential, out of sample | Medium — constrains the model's shape claim | High (1 wk) |
| 6 | **E5** | 6-country lead-lag panel (block-bootstrap peak lags) | Medium — description unless sign/CI predeclared | High (2–3 wks) |
| 7 | **E7** | Cross-country staggered schooling-reform event study | High but conditional on reform data quality | Low (4–6 wks) |
| 8 | **E8** | Sectoral transformation and attainment (Kuznets/Clark–Fisher) | Low — descriptive link | High (2 wks) |

**Single most important test: E1.** It is the only design that identifies push and pull *against each other* in the
same setting and can rule out the common-shock and equivalence objections; every other item either measures one
direction (E2, E3, E4) or constrains the model's shape (E6). If E1 cannot be fielded, run E2+E3 as a pair and
predeclare the joint interpretation (supply and demand separately identified, complementarity not identified).

## 6. Stop/falsification rules and publishable results

Rules R1–R12 in `STOP_RULES.md` (out-of-sample, conservation, equivalence, supplied law, no-new-moment, false
universalization, measurement break, sector heterogeneity, iteration budget, pre-trends, rival exclusion, no
retro-fits). **Publishable positive:** identified push or pull effect with clean pre-trends and placebos; a
universalization timing result tested out of country; a scaling regularity validated out of sample; a two-shock
interaction showing complementarity. **Publishable negative:** observational equivalence of push/pull on available
moments; a null demand→schooling response; model failure against naive benchmarks; failure of the bounded-diffusion
form; measurement limits with the design that would close them. Both are results; neither may be renamed the other.

## 7. Intake / ACK status (protocol §2–§4)

- `NEW:` received at intake: none for `10_massification/` yet; pattern-scout's universalization fits and model2's
  predeclaration are on disk and cited provisionally above. **Requirement:** pattern-scout and exp2 must post `NEW:`
  with path + key number + hash + what it changes; runners and Council ACK. Until then, those numbers are treated as
  provisional and are not used as targets.
- Decision log: `08_council/DECISIONS.md` (D6 gate, D7 intake, D8 slate). Next intake cycle in ~10–15 min; I will
  ACK new batches and may re-rank the slate.

## 8. Dissent recorded

- **PATRINOS:** E1 is correct as the flagship but data assembly (visa/PRC/CHED linkage) may slip; he would run E2+E3
  first and E1 as the joint test, and warns the interaction may be underpowered at national scale.
- **LUTZ:** completion (cohort attainment) should be the primary series, not GER; GER denominators are the recurring
  trap; KHM holdout is right but its completion series has definitional breaks — verify before using as holdout.
- **CARTWRIGHT:** the universalization thresholds (95/90/90) are design choices, not natural constants; report them as
  declared conventions and test sensitivity (90/85/85) before any claim.
- **PAGE:** the logistic-vs-Gompertz ambiguity means "shape" is not identified by fit alone; the model should be
  constrained to produce bounded diffusion without fixing the functional form, and the common-shape test must use
  modern methods (the on-disk test uses F-tests; check assumptions).
