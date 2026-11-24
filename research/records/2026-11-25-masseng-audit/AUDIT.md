# MASSENG v5 massification claim-layer audit (task-38)

**Record:** `research/records/2026-11-25-masseng-audit/` · branch `research/masseng-audit-2026-11-25`
(base `origin/research/handoff-2026-11-24` @ `e8ba60c`). **Auditor:** suite-auditor. **Date:** 2026-11-25.
**Scope (as corrected):** engine/data reality only — what MASSENG v5 actually estimates, the mechanism boundary,
the Philippine fit/reproduction and training/holdout reuse, and which repo/marketing claims must be downgraded or
withdrawn. **No literature verification** (stopped by instruction; not started here) and no new lit review.
**No server compute.** Read-only: no MASSENG, dashboard or paper file was edited. Verification script and
machine-readable results: `scripts/audit_claims.py`, `results/claims_audit.json` (49 checks, 39 flags).

**Audited objects:** MASSENG v6/v5 branch `origin/experiment/masseng-v6-surplus-motor` @ **`9571eb4`**
(`research/masseng-v6/model/`: `engine5.py`, `calibrate5.py`, `countries/PHL`, `outputs/PHL/v5`, docs, QA);
the earlier independent audits `research/masseng-timing-audit-2026-11-24` and
`research/masseng-bayes-audit-2026-11-24` (read for the staging/Bayesian numbers, not recomputed); dashboard
`origin/research/dashboard-2026-11-23` @ `84ff00f`. The boundary facts below were verified in the engine code and
docs, and are consistent with the masseng-coupler boundary table supplied by the Lead.

---

## 0. Bottom line

1. **MASSENG v5 is a deterministic cohort-accounting model with a one-equation demand utility** — not a general
   massification engine. It tracks children from births through primary/secondary/upper-secondary/tertiary by
   income decile and public/private sector, with repetition, deferral, declared cost policies, transfers and a
   tertiary-capacity rule. Everything behavioural is the four-term demand utility plus fit/declared nuisance
   parameters.
2. **R1 is not "the demand engine"; it is the worst of the six rival specifications.** On the registered metric
   (pooled three-GER held-out RMSE) R1 = **16.925**, against R2 7.458, R4 12.194, R0 14.230, R3 15.184, R5 16.543;
   persistence 6.600 and a linear trend 11.794. R1 loses to the v3 benchmark by 2.695 pp and to persistence by
   10.324 pp. The selected rival is R2, whose `b_h` is **−6.000 at its lower bound** and whose own report says it
   loses to persistence.
3. **The boundary is the finding.** v5 has **no learning-production state, no quality/score/achievement variable,
   no score bar or quota gate, no labour-market/earnings/employer module, no rural/urban dimension and no
   migration, and no borrowing/credit constraint**. Credentials enter only as exogenous wage-premium drivers and a
   formal-employment-share proxy. Shadow education is not in v5; the coupled tutoring module is an external,
   declared layer. Claims in the repo that depend on the missing mechanisms cannot be supported by v5, however
   carefully the simulation labels are written.
4. **The PHL fit is a retrospective, inspected comparison, not a validation.** The record's own reproduction QA is
   strong (13/13 files byte-identical, pinned environment, hashes committed), but the test period (1996–2024) was
   inspected in earlier versions and is used for model selection; 9/121 training rows are post-1995 (APIS 2019
   participation gradient inside the test window; FIES 2003/2006); two of the four premium drivers are
   contemporaneous with the outcomes. "Post-1995 enrolment was not fitted" is true but is not the whole story.
5. **23 claims must be downgraded or withdrawn** (§5): 15 withdraw, 8 downgrade. The repo's best documents
   (v5 report, Philippine paper, `ATLAS_WORLDS_QA.md`, `docs/model.md`) already contain most of the correct
   caveats; the overclaims live in the **label layer** ("the demand engine"), the **theory manuscripts'**
   attributed mechanisms, and any downstream use of R1 or the Bayesian screen as an identified object.

---

## 1. What MASSENG v5 actually is

### 1.1 The engine

`masseng/engine5.py` is a deterministic cohort-flow model. The demand side is one utility comparison per level,
decile, sector and year:

```
U_Ldy = alpha_L + b_h·premium_L(y) + b_p·S_L(y-1) + b_r·R(y) + eta_x·ln(decile income/mean)
        - kappa·exp(-lam·Z_L)·ln(1 + burden_Lsdy)          [+ eta·ln(GDPpc/GDPpc_1990) in R0 only]
Z_L = S_L(y-1) in R1/R3/R4, R(y) in R5
```

with cohort accounting (births → Grade 1 → 6/4/2/4 grades), income deciles, public/private providers,
repetition (`rep_prim`, `rep_sec`), late entry, tertiary deferral (`h_def`, max age 25), cycle structure (K-12 from
2017), and supply/finance **inputs**: public tertiary capacity (rationed), optional upper-secondary public capacity,
dated fee/subsidy/voucher cost changes, and CCT transfers (4Ps) as cost reductions. There is no likelihood: the
fits are bounded weighted least squares over declared targets.

Six specifications are estimated: R0 (v3 income benchmark), R1 (all four demand terms), R2 (b_h only), R3 (no
lam), R4 (no b_p), R5 (lam on R instead of S). R1 fits **15 parameters** (11 nuisance + b_h, b_p, b_r, lam).

### 1.2 The mechanism boundary (verified in code and docs)

| Domain | MASSENG v5 reality | Evidence |
|---|---|---|
| Learning / quality / achievement | **Absent.** No learning state, no score, no achievement, no school-quality variable. | `engine5.py` keyword counts: learning 0, quality 0, score 0, achievement 0; `docs/model.md` §"What the model leaves out" lists "school quality and learning" first. |
| Gates | **No score bar, no quota/reserved seats.** An optional *exogenous* tertiary exam pass-rate schedule exists (not configured for PHL); public tertiary capacity is rationed. | `engine5.py` `tertiary_entry_exam` block; PHL `config.json` has no such block; no quota code. |
| Labour market / earnings / employer | **Absent.** No wages, earnings, employment, employer screening or queues. Credentials appear only as exogenous wage-premium drivers and `formal_share`. | keyword counts: earnings 3 (all "forgone earnings"), wage 1, premium 6; `docs/model.md` lists labour-market return changes as omitted. |
| Rural / urban / migration | **Absent.** No region, rural, urban or migration state. | keyword counts 0; `docs/model.md` lists geography/distance and migration as omitted. |
| Borrowing / credit | **Absent.** Affordability is a cost-burden term; no borrowing, credit, savings or uncertainty state. | keyword counts 0; utility has only the burden term. |
| Shadow education / tutoring | **Absent from v5.** A tutoring coupling layer is being built separately by masseng-coupler; it is a declared external shift (no learning production), not an estimate. | keyword counts 0; coupler design note (not committed on this branch at audit time). |
| State capacity / tax / budgets / teacher supply | **Absent.** Capacity and cost policies are declared inputs; no tax, budget, construction or teacher-market response. | `docs/model.md`: teachers and budgets only through the tertiary capacity rule; no fiscal state in `engine5.py`. |
| Household demand across levels | **Present but conditional.** Four-level demand by decile with income, cost burden, premium/positional/relational terms; no borrowing, intra-household, fertility, child labour or gender. | §1.1 utility; `docs/model.md` omission list. |
| Supply / finance inputs | **Partial.** Public tertiary capacity, optional upper-secondary capacity, fee/subsidy/voucher cost changes, 4Ps cost reductions, household-spending outputs; no endogenous supply response. | `countries/PHL/config.json` `tertiary_public_capacity`, `policy_events`, `transfers`. |

The repo's own `docs/model.md` already lists the missing mechanisms — the audit did not have to infer them. The
claim layer's problem is that it frequently writes as if the model contains them.

### 1.3 What the docs correctly say

- `model/README.md` and the v5 report: **"Status: not calibrated. This was a retrospective, inspected test, not a
  blind validation."** R2 wins among rivals but loses to persistence; the selected `b_h` is at a bound.
- `manuscripts/Philippine_demand_rivals.md`: three stronger claims "are not licensed" (earnings returns cause
  participation; positional competition drives massification; occupational thresholds form a relational floor);
  "not calibrated".
- `ATLAS_WORLDS_QA.md`: release **NOT READY** (CHED source still open); recovery `kappa` not identified; `b_h`
  boundary recovery only; China credential-floor check is a **FAIL** and "must not be cited as support".
- `docs/model.md` §"What the model leaves out": school quality/learning, teachers/budgets, geography, migration,
  shadow education, informal fees, gender, labour-market returns.

These are the honest parts of the claim layer. §5 targets the places that still overstate.

---

## 2. What MASSENG v5 R1 actually estimates

### 2.1 Performance (recomputed from `scores.json` obs/pred; pooled over all 75 held-out GER rows)

| rival | pooled three-GER RMSE (pp) | rank | minus R0 | training cost | fitted params | at bounds (record) |
|---|---:|---:|---:|---:|---:|---|
| R2 | 7.458 | 1 | −6.771 | 382.875 | 12 | eta_x, nu, b_h |
| R4 | 12.194 | 2 | −2.036 | 110.426 | 14 | none* |
| R0 | 14.230 | 3 | 0.000 | 171.173 | 12 | nu, eta |
| R3 | 15.184 | 4 | +0.955 | 160.465 | 14 | none |
| R5 | 16.543 | 5 | +2.314 | 135.706 | 15 | none |
| **R1** | **16.925** | **6** | **+2.695** | 105.258 | **15** | none |

Naive benchmarks: persistence **6.600**, linear trend **11.794**. R1 is worse than both by 10.324 and 5.131 pp and
worse than every other rival. (\* R4's `kappa = 39.995` against the upper bound 40 is **not flagged** by the
record's rule; see §2.4.)

At the paper's separating observation, R1 predicts tertiary GER **64.7 in 2013 and 76.2 in 2024** against observed
**31.9 and 47.4** — an overprediction of 32.9 and 28.8 pp. R2 predicts 34.6 / 44.0. The full engine is not close on
the series that carries the paper's headline contrast.

### 2.2 The coefficients are not stable or identified

The four "mechanism" coefficients move wildly across the six specifications:

| spec | b_h | b_p | b_r | lam |
|---|---:|---:|---:|---:|
| R1 | **+1.431** | 5.010 | 3.063 | 3.095 |
| R2 | **−6.000** (bound) | 0 (restricted) | 0 | 0 |
| R3 | **−5.722** | 6.923 | 8.136 | 0 (restricted) |
| R4 | **+2.489** | 0 (restricted) | 9.193 | 4.261 |
| R5 | **−3.681** | 8.040 | 7.256 | 2.285 |

`b_h` is positive in R1 and R4, negative at/near a bound in R2/R3/R5. R1's positive `b_h` cannot be read as a
human-capital return; it is one sign among several, and the selected model's sign is the opposite. No fit stores
standard errors, confidence intervals, a likelihood, or an identification test. The only recovery test is on the
**selected rival R2**, not R1: `b_h` "passes" only as boundary recovery (15/20 replicates hit the bound) and
`kappa` fails (60% within ±25%, required 80%). `b_p` is "not in rival". R1 is never recovered.

### 2.3 The training signal for the demand coefficients is thin

- Training: 121 rows; test: 164. Only **9/121 training rows are post-1995** (7.4%): the APIS 2019
  richest/poorest participation gradients (3 rows) and FIES education-spending shares for 2003 and 2006 (6 rows).
- `premium_tertiary` and `premium_secondary` have **three observed anchors inside the training window**
  (1988, 1990, 1995). Between 1995 and 2013 the premium is linearly interpolated; 2013 and 2024 are observed
  values used as drivers for the test years.
- `formal_share` (the b_r driver) exists only from **1991**, giving five training years of variation (1991–1995);
  before that it is flat-extrapolated.
- Therefore b_h and b_r are informed by roughly 3–5 years of driver variation, not by the full 25-year window; the
  test-period premium values are **contemporaneous** with the outcomes, so the "premium falls while participation
  rises" contrast is not a pre-period prediction.
- The 2019 APIS participation gradient is a **test-window outcome used in training**, and the Bayesian screen later
  fixes all non-demand parameters at an R1 fit that used these rows (the screen's own baseline note calls this
  "data reuse").

### 2.4 Two bookkeeping defects in the claim layer

1. **Bound detection is scale-dependent.** `calibrate5.py` flags a parameter as "at bounds" when
   `abs(value - bound) < 1e-3`. On a 0–40 parameter that is far too tight: R4's `kappa = 39.995` is effectively at
   the upper bound but is reported as "none". R1's `kappa = 39.045` is 97.6% of the way to the bound. The table's
   "at bounds: none" must not be read as "all parameters interior".
2. **"Reproduction" is the record's own QA, not an independent re-run.** The fresh-copy comparison is genuine
   (13/13 files byte-identical, hashes committed, pinned Python 3.12.16 / numpy 2.4.4 / scipy 1.18.1 / BLAS 1
   thread), and the committed output hashes match it. But R1 and R4 are **two-stage optimizer continuations**
   (`continued_from` cost/nfev only; total nfev 573 and 278); the stage-1 parameter vector is not committed, so a
   third party must re-run the recorded two commands, and the result is reproducible only under the pinned
   optimizer. No independent refit was performed here (no scipy in the local runtime; no server compute by
   instruction).

### 2.5 What R1 does and does not estimate

**Does:** one conditional weighted-least-squares parameter vector (15 numbers) that minimises squared error
against 121 declared training targets, given the model structure, the driver interpolation, the target weights and
the optimizer bounds; and the model-conditional predictions that follow from it (which are 30 pp off on tertiary
GER).

**Does not:** identify human-capital, positional, relational or saturation effects; estimate causal or policy
effects; recover structural parameters; rank mechanisms; validate the model for forecasting or policy simulation;
or support any claim about the world. The paper and report already say most of this in their limitations. The
label "the demand engine" and the use of R1 as a Bayesian baseline are what remain to be corrected.

---

## 3. PHL fit: reproduction and training/holdout reuse

### 3.1 Reproduction

| item | result |
|---|---|
| Record's fresh-copy QA | **13/13 files byte-identical**, `all_byte_identical = true` (`outputs/qa/fresh_copy_comparison.json`) |
| Committed outputs vs QA hashes | all six fits + `scores.json` match the fresh-copy and final-output manifests |
| Environment pinned | Python 3.12.16, numpy 2.4.4, scipy 1.18.1, matplotlib 3.10.9, pytest 9.2.0, BLAS threads 1 |
| R1 / R4 | two-stage continuations; stage-1 parameters not committed; total nfev 573 / 278 |
| Independent re-run here | **not performed** (no scipy locally; no server compute) |

The reproduction claim is therefore **"reproduces the record's own fresh-copy QA under the pinned two-stage
procedure"**, not "anyone can reproduce a one-command fit from the bundle". That distinction belongs in the claim
layer.

### 3.2 Training/holdout reuse

- **Test is retrospective and inspected** (PROTOCOL_v5 status statement); the test years were seen in v1–v4.
- **Test is used for model selection**: the registered decision rule picks the rival with the lowest mean test
  RMSE on the three GERs. That makes 7.458 a selection statistic, not a validation statistic; persistence 6.600
  beats it. The record says this.
- **Post-1995 training rows**: 9/121 as above. "Post-1995 enrolment was not fitted" is true (GER/NER/private
  enrolment rows are 1971–1995 only), but the fit still uses post-1995 *outcomes*: APIS 2019 participation
  gradients (inside the test window) and FIES 2003/2006 spending shares.
- **Drivers use test-period information**: the 2013 and 2024 premium values are in the test period; `formal_share`
  varies annually through the test period. The model is a conditional historical decomposition, not a forecast.
- **Bayesian baseline reuse**: the screen fixes 11 parameters at an R1 fit estimated using the broader data and
  varies only b_h, b_p, b_r, lam; its own `baseline_note` calls this "empirically informed conditioning [that]
  involves data reuse". The screen's holdout is the same retrospective test.

**Verdict:** reproduction is substantiated as record-internal QA; the test is not a blind holdout, and the claim
layer must stop calling it one.

---

## 4. Claim inventory by mechanism domain

For each domain: what v5 has, what the claim layer says, and the action. (Source quotes are paraphrased from the
committed documents; exact strings are in `results/claims_audit.json` `CL-*`.)

| Domain | v5 has | Claims that assume more | Action |
|---|---|---|---|
| State / school supply and finance | Declared capacity, cost policies, transfers; no tax, budget, construction or teacher response | "supply-led is the better description"; "state-building/surplus drives schooling"; capacity-policy scenarios as causal levers | **Withdraw** as MASSENG results; panel claim only (already softened to "move together") |
| Household demand, all levels | Four-level conditional demand utility by decile; no borrowing/credit/intra-household | "the demand engine"; "household demand identified"; "the premium drives participation" | **Withdraw** "engine/identified"; downgrade to conditional accounting |
| Learning / quality | None | Theory manuscripts' developmental/neurocognitive and learning-quality claims; tutoring-learning effects | **Withdraw** as model-supported; literature/theory only (no lit verification here) |
| Gates | Optional exogenous tertiary exam pass-rate; capacity rationing; no score bar/quota | "high-stakes gates", "quota/bar effects", "gate-prep competition" | **Withdraw**; v6 Phase-1 is accounting only; X2 is a toy ABM, not v5 |
| Jobs / credentials | Exogenous wage-premium drivers and formal-share proxy only | "credential queues", "employer screening", "surplus motor", "returns drive demand" | **Withdraw** as model evidence; the paper already says the three strong claims are not licensed |
| Rural / urban / migration | None | Rural access, urbanisation, OFW/AQRF/migration arguments | **Withdraw** as model claims; documented omissions |
| Borrowing / credit | None (cost burden only) | "credit constraints", "liquidity" interpretations of demand | **Withdraw** |
| Shadow education | Not in v5; external declared coupling | Tutoring effects/inequality claims as MASSENG results | **Withdraw** as MASSENG evidence; stand-alone shadow work is illustrative |
| Dashboard / public page | No MASSENG result claimed; dashboard links to staging/Bayes/shadow records and marks the coupling in flight | Any use of X1–X5/shadow as MASSENG v5; earlier "supply-led" line (already retracted) | **Downgrade/relabel**; keep panel vs ABM vs v5 separate |

---

## 5. Claims to downgrade or withdraw

**Withdraw (do not publish in the current form).**

| # | Claim | Where it appears | Why |
|---|---|---|---|
| C1 | "MASSENG v5 R1 is the demand engine" | `PROTOCOL_v5.md` title/§4; `HANDOFF_v5.md`; `engine5.py` docstring | R1 is a rival, not selected; worst of six on the registered metric |
| C3 | "positive b_h supports a human-capital demand channel" | result table/paper discussion | b_h flips sign across specs; selected R2's b_h is −6 at its bound |
| C4 | "saturation-dependent cost sensitivity (lambda > 0) is supported" | protocol decision rule | R1 loses to R3 on both required criteria (RMSE and 1998 recession) |
| C5 | "the full positional-relational engine is the preferred demand account" | implied by the "demand engine" label | R1 is worst of six; paper says it does not win |
| C10 | "learning/quality is modelled" | theory manuscripts and model prose | no learning/quality/score variable exists |
| C11 | "score bars / quotas / high-stakes gates are modelled" | theory manuscripts; v6 notes | no score bar/quota; only optional exogenous pass-rate; PHL has none |
| C12 | "teacher supply / teacher effort is modelled" | theory manuscripts | teachers only via the capacity rule; no teacher market/effort |
| C13 | "labour market / earnings / employer screening / credential queues are modelled" | June manuscript; "relational floor" prose | no labour market or earnings; credentials only exogenous premiums and a formal-share proxy |
| C14 | "rural/urban differences and migration are modelled" | theory manuscripts; HKG/AQRF material | no region, urban/rural or migration state |
| C15 | "borrowing/credit constraints are modelled" | demand discussion | affordability is a cost burden; no borrowing/credit |
| C16 | "shadow education effects are estimated by MASSENG" | coupling notes | v5 has no tutoring state; coupling is a declared external shift |
| C17 | "state supply/finance drive massification (supply-led established)" | theory manuscripts; dashboard line | v5 takes capacity/cost policies as inputs; no state response; panel claim only |
| C18 | "MASSENG v5 validates the surplus/credential-pipeline theory" | May/June manuscripts | the theory's mechanisms are outside the engine |
| C19 | "MASSENG is calibrated / validated / usable for forecasting or policy simulation" | release prose | report/paper say not calibrated; no blind holdout; no policy effects |
| C23 | "the Bayesian screen yields a posterior / identifies mechanisms" | Bayesian record/prose (cited) | ESS 2.17%, prior/σ-dominated, X5 confusion 50% (<60% criterion), baseline data reuse; the screen's own status is "not a calibrated posterior" |

**Downgrade (keep with a narrower, accurate statement).**

| # | Claim | Replacement |
|---|---|---|
| C2 | "R1 estimates human-capital/positional/relational/saturation coefficients" | "R1 yields conditional weighted-least-squares point values for four coefficients; they have no SEs/CIs, no R1 recovery, and are unstable across specifications" |
| C6 | "test RMSE on 1996–2024 validates the model" | "test RMSE is a selection statistic on a retrospective, previously inspected period; the selected rival loses to persistence" |
| C7 | "post-1995 enrolment was not fitted, so the test is clean" | "post-1995 enrolment was not fitted; 9/121 training rows are post-1995 non-enrolment outcomes (APIS 2019 gradient; FIES 2003/2006)" |
| C8 | "the 1971–1995 training window identifies the demand coefficients" | "the premium has 3 observed anchors (1988/1990/1995); formal_share has 5 years (1991–95); b_h/b_r are weakly informed" |
| C9 | "drivers are exogenous and predetermined" | "2013/2024 premium values are contemporaneous with the outcomes; formal_share varies through the test period" |
| C20 | "dashboard/public massification claims are MASSENG results" | "dashboard = E1/E6 panel claims; public page = ABM mechanism tests; neither is MASSENG v5" |
| C21 | "the PHL fit reproduces from the committed bundle" | "reproduces the record's fresh-copy QA (13/13 byte-identical) under a pinned two-stage continuation; no independent refit" |
| C22 | "'at bounds: none' for R4" | "no parameter within 1e-3 of a bound; R4 kappa 39.995/40 and R1 kappa 39.045/40 are effectively near-bound and the rule misses them" |

**What can be said honestly (positive):** v5 is a transparent, reproducible cohort-accounting model with a
conditional four-level demand utility; it can produce accounting-consistent counterfactuals under declared
capacity, cost and transfer inputs; its QA honestly reports the failure of its own benchmark and the
non-identification of `kappa`; and the PHL comparison is a useful negative result about demand-side explanations
at this measurement quality. It cannot adjudicate the mechanisms the claim layer attributes to it.

---

## 6. Verification and limits

- **Recomputed here** (script): all rival pooled RMSEs from `scores.json`; R1 rank/benchmarks; R1 tertiary
  predictions; coefficient instability; training/test composition; driver anchors; fit hashes vs QA; output
  hashes; boundary keyword counts; QA spotchecks/credential-floor/completion checks; dashboard MASSENG mentions;
  claim inventory.
- **Read, not recomputed**: Bayesian screen ESS/prior/σ/X5 numbers (from the committed Bayes-audit record); test
  suite counts (not run; no scipy locally); staging/X1–X5 and shadow numbers (out of scope; cited as dashboard
  context only).
- **Not done:** literature verification (stopped by instruction); independent refit of any v5 rival; server
  compute; any edit to MASSENG/dashboard/paper files.
- **Reproduce:** `git fetch origin 'refs/heads/*:refs/remotes/origin/*'` then
  `python3 research/records/2026-11-25-masseng-audit/scripts/audit_claims.py` (needs numpy; writes
  `results/claims_audit.json`).
- **Limit:** this is a claim-layer audit of the domains the Lead named, not a line-by-line audit of every
  sentence in the two long theory manuscripts; those manuscripts' claims are treated at the domain level and
  marked out of engine scope.

## 7. What the repo should change (short list)

1. Remove "the demand engine" as a label for R1; call it "the unrestricted demand rival (not selected)".
2. Add the boundary table of §1.2 to `model/README.md`, the paper and the public-facing material, before any
   mechanism sentence.
3. Attach to R1: number of fitted parameters, absence of SEs/recovery, the b_h sign instability, and the driver
   anchors. Do not report R1's coefficients as "estimates" without that.
4. Fix the at-bounds rule to a relative tolerance; re-report R4/R1 near-bound parameters.
5. Replace "held-out RMSE" with "test-set selection RMSE" and state the persistence comparison in the same
   sentence.
6. Add the 9/121 post-1995 training rows and the 2013/2024 driver timing to the reproduction section.
7. Mark the Bayesian screen as a diagnostic (already its own status), and stop using "posterior" anywhere in
   summaries.
8. Keep dashboard (E1/E6 panel), public page (ABM mechanism tests) and MASSENG v5 in separate labelled lanes.
