# RUN REPORT — fitted-worlds feasibility pilot (task-24)

**OUTCOME: STAGE 1 FAILS → "INSUFFICIENT EVIDENCE". The pilot stopped at Stage 1 under its
own pre-registered stop rule. No frozen split, no synthetic-recovery challenge, no
rejection-ABC, no model-free benchmark, and no model/fitting compute were run — on region-42
or anywhere. The server was not used.**

EXPLORATORY throughout. No confirmatory claim, no causal claim, no E1 1.8% comparison, no
theory ranking. This report contains no invented target and no proxy result.

---

## 1. Provenance

| item | value |
|---|---|
| branch | `research/fitted-worlds-pilot-2026-11-24` (additive from corrected branch head `7f0221bd`) |
| pre-registration | `PRE_REGISTRATION_fitted_worlds_pilot.md`, commit **`953a382`**, committed before code |
| prereg sha256 | `e9e05b1892ed4b1062fa20002836fd1a6cb908e43bf6ba3c8c7df50f45efdb58` |
| audit code | `construct_audit.py`, sha256 `efef81d5fdec7713191ff073c0a5088d0a6d63a60c7d6ee952d96d6caa1d56e5` |
| audit results | `stage1/stage1_audit.json`, sha256 `a15643f60b4cb7f6d6da4ef216736234a2937794c2e664e8cde2073b0ea96581` (28 KB) |
| audit report | `STAGE1_CONSTRUCT_AUDIT.md`, sha256 `01fd11099459d497c98e40c7a2c22684d07d26c81264a230f374eea98d26f3ed` |
| server | region-42 reachable and idle at check (2026-11-24T12:45Z; 96 cores, 0 jobs of ours). **Not used** — Stage 1 failed before any compute. |
| code edits | none to `a12d357`; separate doc correction `26d9b27` applied to `PRE_REGISTRATION_MAPPING.md` on the results branch (Codex request 12:32Z; documentation only) |

## 2. What was done

1. Pre-registration written and committed first (commit `953a382`): five-stage gate after
   Codex `1028340e`, with explicit per-stage stop rules and a Stage-1 pass rule requiring
   ≥2 measurement-compatible model outputs, a joint moment that constrains the four worlds'
   distinguishing parameters, and a frozen split of ≥20 training / ≥10 independent validation
   countries.
2. Stage 1 construct/feasibility audit executed as a **read-only inventory** of committed repo
   data (this worktree and other committed branches via `git show`): WDI/UIS/ILO sweep,
   `asia_school_work.json`, shadow-education data, E1 derived outputs, Q2 long-run panel, DHS
   API cached cells, DHS CEB-by-education cells, Philippines HE series.
3. Every one of the 11 model observables was mapped to observed candidate series with age,
   unit, definition, period and coverage; joint overlap across the constructs needed to
   distinguish the worlds was computed; the pre-registered pass rule was applied.

No model was run, no data were imputed or pulled, no DHS microdata was acquired, and no
fitting/ABC/synthetic-recovery/timing compute was executed.

## 3. Stage-1 findings (numbers)

- **Mapping: 0 compatible, 4 partial, 7 unmatched** (of 11 model observables).
  - *Partial*: `ger` (participation share vs gross/net enrolment, no age in model),
    `cl` (ILO/UCW children 7–14 employment vs household states, no age in model),
    `learn` (test-score scale vs model grade-equivalents — no scale anchor),
    Phase B `B3` (DHS median age at first birth vs model mean, different age/education cuts).
  - *Unmatched*: `sw`, `wo` (study-and-work / work-only shares are not in the committed data),
    `hw` (hidden work is unobservable), `tut` (only 6-country hand-collected case-study
    incidence), `inc` (GDP pc vs arbitrary-unit household income), Phase B `B1` (needs
    birth-interval microdata that this pilot may not acquire), Phase B `B2` (PPR is not
    published; mean CEB is a different quantity).
- **Observed coverage highlights:** child employment (ILO/UCW via WDI) **100 countries,
  281 observations, 1994–2016, median 2 obs/country**; primary GER 207 countries 1970–2022;
  net enrolment 197/188 countries 1970–2019; harmonized test scores **172 countries but only
  2010–2020**; learning index 172 countries 2010–2020; Q2 long-run panel 197 countries
  1750–2024; DHS API cached panels 76–87 countries 1985–2025 (fertility/women's education
  only); DHS CEB-by-education cells 14 countries; shadow-education data 6 countries/sites
  (38 + 20 rows, case studies); E1 record holds **derived** link statistics only — the raw
  WDI panel is not committed.
- **Joint overlap (the decisive point):** the most favourable cross-construct overlap is
  `child_work × pre_ger`: **90 countries, 240 country-years within ±2 years** (also
  `× prm_ner` 93/240, `× lsc` 88/236, `× test_scores` 35/55). But this is **total child
  employment + an age-mismatched enrolment series on a sparse irregular panel** — it does not
  observe the study-and-work / work-only / hidden-work decomposition that the four worlds
  differ in. No documented measurement-compatible change moment exists on disjoint countries
  for a frozen 20-training / 10-validation split.
- **Sensitivity:** relaxing "compatible" to accept the two best *partial* constructs still
  fails the pre-registered joint-constraint condition and the split-size condition; passing
  would require inventing an age rule and a panel construction, which the pre-registration
  forbids. Stage 1 therefore fails on (a), (b) and (c) simultaneously.

## 4. Per-stage status

| stage | status | note |
|---|---|---|
| 1 construct/feasibility audit | **FAIL — insufficient evidence** | 0 compatible outputs; only cross-output overlap misses the distinguishing decomposition; no frozen split feasible |
| 2 frozen split | **NOT LAUNCHED** | stop rule at Stage 1 |
| 3 synthetic-recovery challenge | **NOT LAUNCHED** | stop rule |
| 4 bounded equal-budget rejection-ABC | **NOT LAUNCHED** | stop rule |
| 5 model-free benchmark | **NOT LAUNCHED** | stop rule |
| §6 kernel-through-moment timing pilot | **NOT RUN** | only needed before a draw/cores commitment; none was made |

## 5. Cost

- Server wall: **0 s** (region-42 not used; 0 jobs).
- Audit compute: read-only file reading, negligible (seconds); no model/fitting compute on the
  Mac.
- No draws, cores, storage or paid server time were committed. No existing output was
  overwritten.

## 6. What would be needed to make the fitted-worlds question answerable

1. An **age/grade-structured** model output (or a declared, testable age-aggregation rule) so
   UCW 7–14 child-labour states and primary/secondary enrolment can be matched.
2. **UCW study-and-work and work-only shares** as a harmonised country-year panel — the
   decomposition that separates the four worlds; the committed cache has only total child
   employment.
3. A **learning-scale anchor** (explicit, out-of-sample-validated model→test-score mapping).
4. A **harmonised cross-country tutoring/shadow-education panel** (current data are case
   studies).
5. **DHS birth-interval microdata** for B1 (not permitted in this pilot).
6. Consistent vintages/periods across constructs so a frozen, non-overlapping split is
   possible.

Until these exist, "fitted worlds separate/converge" would be a statement about an invented
target, not about observed education systems. Reporting this stop is the pre-registered
Stage-1 outcome.

## 7. Caveats and limitations of this audit

- Observed data are limited to what is committed in the repository; the E1 raw WDI panel is
  not committed (derived link statistics only) and no re-pull was allowed, so E1's panel could
  not be used as a target.
- Data vintages differ across sources (ILO/UCW modelled estimates 1994–2016; WDI enrolment
  1970–2022; harmonized test scores 2010–2020; DHS surveys 1985–2025). The audit reports
  them; it does not harmonise them.
- "Partial" constructs are not thereby ruled out forever: they require a declared, testable
  approximation and an amendment reviewed before use — none was made here.
- No confirmatory claim; no causal claim; no E1 1.8% comparison; no theory ranking.

## 8. Shutdown advice

- region-42 was up and idle at the last check and **nothing of this pilot ran on it**; there is
  no server-only artefact and no job to preserve. The branch and this record are pushed to
  GitHub; the audit inputs are committed on other branches of the same repository.
- **Trey can stop (关机, not 释放) region-42 whenever he wishes.** If a later stage of this
  pilot is ever authorized, the box would need to be powered back on; the Stage-1 blocker is
  data/construct availability, not compute.
