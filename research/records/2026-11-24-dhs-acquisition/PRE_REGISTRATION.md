# PRE_REGISTRATION — individual-level schooling and children ever born (DHS IR), with the EFR/TFR construct split

**Commit this file before any DHS microdata arrive, before any analysis script is written, and before any
estimate is computed.** It is committed in the same push as
[`ACQUISITION_PLAN.md`](ACQUISITION_PLAN.md); at the time of writing **no DHS microdata file has been
downloaded, opened or seen** by this workstream (the access route is documented in the plan, up to the login
wall).
**Date:** 2026-11-24. **Branch:** `research/dhs-acquisition-2026-11-24` (base
`origin/research/handoff-2026-11-24 @ 51f9f02`). **Task:** task-2. **Owner:** dhs-scout.

**Standing rules that bind this document:** no causal language; simulation/synthetic/model data are **not**
an acceptable substitute for the real test and must never be presented as one; effective fertility
(surviving children) is **never** called "TFR"; recompute before quoting; no secrets; never rewrite an
existing branch. Data tier for everything here: **observed** (once it arrives) — never reconstructed or
imputed.

**Status if the data do not arrive:** the test stays **unrun** and the record says so. It does not get
replaced by API cells, a simulation, or a synthetic file.

---

## 1. Why this test, and what it is not

The macro regression wall says aggregate panels cannot separate competing micro mechanisms (handoff §1;
`codex_wave_ledger.md`). The prior DHS attempt ran the canonical gradient on **published cells** and stated
plainly that the individual-level test "could NOT be run" and that its results are **ecological**
(`research/dhs-micro-2026-11-23 @ 31ded00`). This preregistration covers the **woman-level** test on DHS
Individual Recode (IR) files.

E11 (`origin/research/e11-fertility-audit-2026-11-25 @ e926575`) established that the project's two fertility
series are **different constructs**: `effective_fertility` = surviving children per woman (reconstructed) vs
`tfr_observed_1950plus` = births per woman (UN WPP). Measured gap over 2,955 overlapping country-years/197
countries: **median |TFR − EFR| = 0.3042**, **max = 4.2677**, mean ratio 1.1749, level correlation 0.9378;
matched level ladder (n = 1,417; 109 countries; 1950–2010): lead/lag **0.541** (surviving children) vs
**1.555** (births). Those are aggregated series. **This test asks the same question one level down:** at the
individual woman level, within birth cohort and survey round, does the schooling coefficient change sign or
change materially when fertility is measured as **births ever** vs **children surviving**?

This is **not** a causal design. There is no instrument, no policy discontinuity, no pre-trend test available
in repeated cross-sections of individuals. All language is associational ("is associated with", "the
coefficient is", "consistent with"). No result here can establish that schooling causes lower fertility.

---

## 2. Data (to arrive; see ACQUISITION_PLAN.md)

- **Source:** DHS Program Individual Recode (IR) files, Stata format (`…IR…DT.ZIP`), obtained by Trey through
  the registered-user, country-approved download route in `ACQUISITION_PLAN.md` §2–§3. No alternative source,
  no scrape, no borrowed account, no synthetic substitute.
- **Countries:** 8 verified E8 sub-Saharan countries (**MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA**), 3
  Southeast Asian benchmarks (**KHM, PHL, VNM**), 3 comparators (**BEN, NAM, SWZ**).
- **Rounds:** **standard-DHS** IR rounds only in the main analysis — 72 files, ~501 MB — exactly the
  `survey_type == DHS` rows of
  [`data/dhs_ir_inventory_targets.csv`](data/dhs_ir_inventory_targets.csv). **MIS and AIS** rounds (20 files)
  enter only as a clearly-labelled robustness tier *and only if* the needed variables (`v133`, `v206`, `v207`)
  are verified present on opening the file (§7 of the plan).
- **Unit:** one woman 15–49 at interview. Variables and derivations: `ACQUISITION_PLAN.md` §4.
  Outcome and exposure are recorded (`v201`–`v207`, `v106`/`v133`/`v149`), not reconstructed.
- **Design-based weights and clustering:** `pw = v005/1e6`; PSU = `v021`; strata = `v022`.
- **Vintages:** each file's exact `FileName`, sha256, release code `v000`, and download date are recorded in
  `ACCESS_LOG.md` before analysis. A re-release with the same name is a vintage change, recorded, not
  "corrected".
- **What is explicitly excluded:** the DHS public API cell aggregates (used only for the §7 cross-check), DHS
  model datasets (synthetic), any imputed or reconstructed microdata, any harmonised third-party extract
  (IPUMS-DHS) unless it is derived from the same approved DHS files **and** the mapping is logged — main
  results must come from the DHS IR files themselves.

---

## 3. Samples (fixed now)

| Sample | Definition | Role |
|---|---|---|
| **Main (S-A)** | Women aged **40–49** at interview, `v201` non-missing, `v106` non-missing, in a standard-DHS round | Completed-fertility sample; the headline estimates |
| S-B | Women aged **35–49** | Robustness (some truncation at 35–39) |
| S-C | Women aged **25–49** | Robustness only; explicitly right-censored, never the headline |
| S-D | S-A restricted to rounds with **≥ 2 standard-DHS rounds in that country** | Cohort-vs-round separation test |
| S-E | S-A excluding **Vietnam** (ever-married universe) | Comparability check |

Cohorts: 5-year **birth-year** bins from `v011` (CMC date of birth): `cohort5 = 5·floor(floor(v011/12)/5)`.
A cohort enters the model if it appears in **≥ 2 survey rounds** (otherwise cohort and round effects are not
separately identified).

Cell floor: a cohort × education cell with **< 50 women** is not estimated separately; it is (a) pooled to a
10-year cohort, or (b) merged into "secondary or higher", or (c) dropped from that round's contribution —
in that order. The choice is logged per cell, never made per result.

---

## 4. Specification (fixed now)

### 4.1 Headline model (M1)

For woman *i* in birth cohort *c* (5-year), survey round *r*:

```
Y_irc = β · Edu_i + δ_c + γ_r + φ_{r,region} + θ · urban_i + ε_irc
```

- `δ_c`: 5-year birth-cohort fixed effects.
- `γ_r`: survey-round fixed effects.
- `φ_{r,region}`: region × round fixed effects (`v024` changes meaning across rounds; see plan §8.5).
- `urban_i`: `v025`.
- **No age control in M1.** Age, cohort and round are linked by the accounting identity `age ≈ round_year −
  birth_year`; with cohort FE and round FE, a linear age term is not separately identified from the cohort
  effects. This is stated up front rather than "discovered" in the output. (A model with age instead of cohort
  FE is reported as a descriptive alternative, labelled as such.)
- **Weights:** `v005/1e6`, renormalised so each survey round has equal total weight in the pooled model
  (population-proportional reweighting is reported as an alternative; both are reported, never mixed).
- **SEs:** clustered on `v021` (PSU) with `v022` strata (design-based, `svyset` with a subpopulation option —
  rows are never dropped before `svyset`). Country-clustered SEs reported as a sensitivity.
- **Exposure:** `Edu_i` = `v106` dummies (reference: no education), so β is a vector: primary, secondary,
  higher. **Headline coefficient = secondary vs no education.** The "dose" version uses `v133` single years
  (linear, plus a restricted cubic spline with 3 knots) and is reported alongside; `v149` (6 categories) is a
  robustness encoding.
- Monotonicity is checked: β(none) ≥ β(primary) ≥ β(secondary) ≥ β(higher) in the expected order.

### 4.2 Pre-declared model ladder (all reported; M1 is the headline)

| Model | Adds | Purpose |
|---|---|---|
| M0 | cohort FE + round FE | raw within-cohort association |
| **M1** | + region×round FE + urban | **headline** |
| M2 | + wealth quintile FE (`v190`) | robustness; wealth is a **mediator/descendant** of schooling, so M2 is *not* the preferred specification |
| M3 | + `Edu × cohort5` (or `Edu × linear cohort`) | does the gradient steepen or attenuate across cohorts? |
| M4 | `Edu × round` | heterogeneity across survey rounds (reported as share of rounds negative, not as a p-value hunt) |

### 4.3 Outcomes (the construct split)

- **O1 — births ever:** `v201` ("total number of children ever born"). A cumulative, quantum-type measure.
- **O2 — children surviving:** `v201 − v206 − v207`. The individual-level analogue of the project's
  `effective_fertility` (surviving children). **Never called TFR, never described as a rate.**
- **O3 — survey-level period TFR:** computed from each IR's birth history (`REC21`) by the DHS procedure in the
  Guide to DHS Statistics; used **only** as a survey-level comparison and validation series. It is not an
  individual outcome and is not regressed on individual schooling.

**Construct test (pre-declared).** Stack O1 and O2 for the same women (two rows per woman), fit
```
Y_ij = β1·Edu_i + β2·(construct_j) + β3·(Edu_i × construct_j) + δ_c + γ_r + φ_{r,region} + θ·urban_i + ε_ij
```
with cluster-robust SEs **on the woman** (the two rows are the same person). Standardise both outcomes
(per-SD) before interacting so the comparison is scale-free. The construct question is answered by the sign and
confidence interval of the **standardised** β3 term and by the ratio `β_surviving / β_births`, exactly analogous
to E11's lead/lag comparison.

### 4.4 What is NOT in the model

No lagged/lead outcome terms (impossible at the individual level), no country-year aggregates, no
post-treatment controls beyond M2, no sample-dependent control sets, no stepwise selection, no specification
search. The model list is closed at M0–M4.

---

## 5. Pre-registered hypotheses and decision rule

**H1 (the "dose" association, headline).** Within 5-year birth cohort and survey round, women with more
schooling have **fewer children ever born**; the secondary-vs-none coefficient is negative.
- **Confirmed** if, in M1 on S-A with O1: β(secondary) < 0 with a 95% CI excluding 0, **and** the pooled
  ordering is monotone (none > primary > secondary > higher), **and** the per-round gradient (same contrast,
  each standard-DHS round estimated separately) is negative in **≥ 70% of rounds**. The share is reported; the
  result is **not** described as "robust everywhere" (Q3: that label mislabels 87% of minority-effect worlds).
- **Killed** if β(secondary) ≥ 0 in M1, or the 95% CI excludes zero on the positive side.
- **Wealth-mediated (reported as its own finding, not as a pass/fail):** if the negative coefficient disappears
  (CI includes 0) once `v190` enters in M2, that is reported as "the association is carried by wealth", with the
  effect size, and H1 is **not** counted as confirmed.
- **Inconclusive otherwise.** Intervals are reported, not just stars.

**H2 (the construct split).** The choice between O1 (births) and O2 (surviving children) changes the
schooling–fertility association.
- **"Sign change"** if the standardised β(secondary) has opposite signs for O1 and O2, with the interaction β3
  CI excluding 0.
- **"Material magnitude difference"** if the signs agree but |β_O2/β_O1| lies outside **[0.75, 1.33]** or the
  interaction CI excludes 0.
- **"No material construct difference"** otherwise.
- **Prior expectation, stated honestly:** E11 found the two *aggregate* series to move differently (lead/lag
  0.541 vs 1.555, median gap 0.3042), so a material difference at the individual level is plausible but **not
  assumed** — the individual-level gap is about birth *survival*, which is much smaller in magnitude than the
  aggregate EFR/TFR gap (which also embeds reconstruction). Either result is informative; neither outcome is a
  "correction" of the other.

**H3 (cohort trend).** The schooling gradient changes across birth cohorts. Two-sided test, no directional
claim: the prior ecological evidence found **attenuation**, not steepening (secondary interaction **+0.26
(0.13)** children per decade, `research/dhs-micro-2026-11-23 @ 31ded00`), and that record flagged composition
as the likely reason. The individual data can separate composition (category meaning changes) from a change in
the within-category association. Pre-registered falsifier for "the gradient is steepening with mass schooling":
an `Edu × cohort` interaction that is **not** positive and distinguishable from zero on the individual data.
A null is reported as a null.

**Heterogeneity reporting rule.** For every heterogeneity family (rounds, countries, urban/rural, cohorts),
report the **share** of units with the pre-declared sign, the median magnitude, and the BH-adjusted
significance count within that family. No single-round or single-country result is reported as the finding.
Minority effects are described as minority effects.

**Multiplicity.** One headline test (H1: secondary vs none, O1, M1). H2 and H3 are secondary and reported with
their own CIs; their families get BH adjustment. No p-value screens.

**Stopping rule.** The sample is **all** standard-DHS rounds of the 14 countries that pass the verification
checklist, fixed in advance. No optional stopping, no dropping rounds for results, no adding countries after
seeing estimates. A round that fails structural verification is excluded **before** any estimation and the
exclusion is logged.

**Deviations.** Any change to this document after data arrival is an **amendment appended below** with date,
reason and the affected estimate; the original text is never edited. If the deviation is substantive, the
result is labelled exploratory.

---

## 6. Falsifiers (stated before the data)

The claim "more schooling, fewer births, as an individual-level dose" fails if any of the following holds:
1. β(secondary) is not negative in M1, or its CI is uninformative.
2. The ordering is non-monotone (higher > secondary > primary) in the pooled estimate.
3. The negative association disappears under the wealth control (M2) — then the finding is about wealth, not
   schooling.
4. The per-round gradient is negative in fewer than 70% of rounds (a minority-effect reality must be reported
   as such, not averaged away).
5. The construct split shows that the negative association exists only for one construct in a way that the
   other construct contradicts — reported as a construct finding, and **no claim** is made about "fertility"
   in general.
6. The whole association is an artefact of the completed-fertility sample choice: it disappears or flips in
   S-B/S-C, or is confined to one country or one round.

A null, a reversal or an uninformative interval is reported with the same prominence as a confirmation.

---

## 7. Honest limits (binding on every downstream use)

1. **Observational.** Within-cohort, within-round associations conditional on observed controls. No causal
   language, ever, without an event study with checked pre-trends — and this design cannot supply one.
2. **Age–period–cohort identity.** With cohort FE + round FE, age is not separately identified. Effects that
   the literature attributes to age at interview are absorbed. This is a limitation, not a fix.
3. **Right-censoring.** Completed fertility is only observed for older women; the 40–49 sample is survivors who
   are still in the sample, married or not, alive at interview. Younger cohorts are truncated and are
   robustness-only.
4. **Selection and attrition.** DHS samples women in sampled households; women who died or emigrated are absent;
   in high-mortality/high-migration countries this is not ignorable.
5. **Recall and imputation.** Birth dates and children-ever-born counts are self-reported; DHS imputes some
   dates. Counts for very high parities may be heaped.
6. **Education's meaning changes.** `v133` uses country-specific years-to-complete (`x`,`y`); "secondary" spans
   an expanding share of the population across rounds (`research/dhs-micro-2026-11-23 @ 31ded00` found the
   category meaning shifting). Cohort FE do not fix a change in the *meaning* of the exposure.
7. **Construct difference, not measurement error.** Births ≠ surviving children. The surviving-children measure
   is the individual analogue of `effective_fertility`; it is not a period TFR and not a rate. Neither measure
   "corrects" the other (E11 §1).
8. **Period TFR is a survey-level quantity.** Any TFR number comes from the birth-history procedure at the
   survey level; an individual's CEB is not a TFR. Tables must name the construct
   ("births per woman (cumulative, individual)" vs "surviving children per woman (cumulative, individual)").
9. **Comparability.** Vietnam 1997/2002 IR files have an **ever-married women** universe (from the public DHS
   survey metadata); Eswatini has one round; Ethiopia's first round is 2000 and Lesotho's 2004. Cross-country
   pooling is therefore explicitly unequal and is reported with and without the thin cells.
10. **Aggregate ≠ individual.** Reproducing the DHS API's country × survey × education cells from the microdata
    is a **sanity check**, not the test. The individual test is the woman-level model, and only that.
11. **No substitution.** Synthetic/model data are not a substitute; API cells are not a substitute; a
    simulation of a "schooling effect" is not evidence. If the files do not arrive, this test is not run.

---

## 8. Pre-declared predictions (recorded now so later claims can be scored)

| # | Prediction | Confidence | If contradicted |
|---|---|---|---|
| P1 | β(secondary) < 0 for births (O1) in M1, pooled across the standard-DHS rounds | high (prior ecological evidence is large and near-universal in sign) | report the reversal prominently; check coding/weights first, then report |
| P2 | The gradient is monotone in education categories | high | report the non-monotonicity; it is a substantive result about category meaning |
| P3 | A negative association survives the wealth control (M2), attenuated but negative | medium | report wealth-mediation as the finding |
| P4 | The EFR/TFR construct split changes the **magnitude** at the individual level less than it does at the aggregate level; a full **sign** flip is unlikely | medium | a sign flip would be a major construct finding and would be reported as such |
| P5 | The cohort interaction is positive (attenuation), not negative (steepening) | medium — prior ecological evidence points up, but composition is not separable there | report steepening; state that the individual test overrides the ecological one |
| P6 | Minorities exist: not every round/country shows a negative gradient | high (Q3 lesson) | report the share honestly either way |

These predictions are **not** the decision rule; the rule is §5. They exist so the record can say, later,
whether the preregistered expectations were right — including where they were wrong.

---

## 9. Outputs and reporting contract

- Every estimate: coefficient, design-based clustered SE, 95% CI, n (women), number of rounds, number of
  countries, weighted and unweighted versions.
- `REPORT.md` must reproduce the headline numbers from committed code and committed outputs; every number
  carries a file + field locator.
- Every table names the construct explicitly (§7.8).
- Negative, null and failed runs are preserved and reported (handoff rule 8).
- No microdata, and no cell small enough to identify a woman or community, is committed to the public repo.
- Any result described as "consistent with" must name the alternative explanations it is also consistent with.

---

## 10. Sign-off

Written by **dhs-scout** for **task-2**, 2026-11-24, **before any DHS microdata were obtained**. If the access
route in `ACQUISITION_PLAN.md` succeeds, the analysis proceeds under this document unchanged; deviations are
appended with dates and reasons. If it fails, this document stays as the record of the test that remains
unrun.
