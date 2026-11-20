# Summary for Trey — what actually ran, what we learned, and what to do next

**20 November 2026 · DeepSeek research fleet · for Dr. Trey Menefee**
Programme: *Massification and Its Mechanisms* (Menefee & Nordtveit, October 2026; June single-author draft).

This is the plain-language report. Everything below is either (a) a number I re-ran on your laptop,
(b) a number I pulled from a primary source, or (c) explicitly labelled as a simulation or an
unverified claim. Nothing is invented. Where the results contradict the paper, I say so.

---

## 1. What actually executed (about 35 minutes of compute, 8-core M1, workers ≤ 2)

- **Reproduction audit:** your Triad and Massabm models were run fresh, from your local
  `related/massification_project` source (Atlas `02cade9`), plus the Atlas engines at public main
  `55732f4`. All five headline results I tested reproduce. Details in `03_audit/REPRODUCTION_MATRIX.md`.
- **Twelve new experiment cells** (batch A) with pre-declarations written before the runs, matched
  seeds, and a Phase-0 known-answer accounting gate that passes (people, money and jobs conserve; the
  floor test's lottery slope now matches the stored value at 4 reps).
- **A parallel adversarial batch (B)**: independent replication of the matched-elasticity rival plus
  long-run 10/20/30/40-year trajectories. 72/72 runs OK.
- **Literature:** 20/20 core sources logged; 9 read in full (6 at equation level), the rest labelled
  abstract-only or blocked. 68 manuscript claims registered, 33 verified, 33 unresolved.
- **Data:** WDI (48 indicators × 4 countries), UIS SDG4 (30 indicators), national sources for
  Philippines, Cambodia, Hong Kong, China, with retrieval dates, HTTP status and SHA-256.
- **Two synthetic expert-council sessions** on the results. Their withdrawal list is binding on the
  language below.

## 2. The graduate-supply test: the income version dies, the formal-access version survives (one cell deep)

Your October Prediction 2 says a graduate-supply shock separates the surplus account from a
competitive market on **diploma holders' absolute income**. Two follow-ups tested that and changed the
verdict twice; **the Council has now signed off on exactly one sentence**, which the paper may use:

> *"In this model class, with baseline formal access matched (0.280 vs 0.286), a graduate-supply shock
> under fixed formal vacancies lowers diploma holders' formal-employment probability by 15.1 points
> (±2.2) under credential-rationed hiring, while a level-matched productivity-hiring CES benchmark
> shows no material fall — at most 0.5 points, at σ = 2, the cell where degree income is also matched
> (2.706 vs 2.925); absolute income does not discriminate: there the rival's diploma income rises
> 12.5 points. This is a model-class result, not evidence about any country. At σ = 0.5/1 the formal
> share is matched but income is not (11.4 and 1.5 vs 2.9); the σ = 0.5 income corner of E13b/B1 is
> numerically unstable and is not cited."*

| world (college half price) | Δ diploma formal-job probability | Δ diploma income | level match |
|---|---|---|---|
| surplus (slots + floors + rank) | **−0.1511** (sd 0.022) | −0.0583 (0.018) | target |
| level-matched rival, σ = 0.5 | +0.0085 (0.011) | −0.0270 (0.048) | formal share ✓, income ✗ (11.4 vs 2.9) |
| level-matched rival, σ = 1.0 | +0.0095 (0.008) | +0.0001 (0.002) | formal share ✓, income ✗ (1.5 vs 2.9) |
| level-matched rival, σ = 2.0 | −0.0054 (0.003) | +0.1252 (0.017) | **both ✓** |

**What to withdraw:** the absolute-income discriminator. **What not to say:** that the income
contradiction was a "level artefact" — B1's σ=0.5 fall is real in point estimates (−0.109 / −0.175,
2 sd, plausible baseline 0.234) but that corner is numerically unstable (ratio 0.022–0.055; degree
income 1.0–42.4 across seeds). Its status is **unidentified**, and it is cited for neither theory.
The formal-access claim is **one cell deep** (σ=2 is the only fully matched world); a blind
fully-matched rival is listed below as the first credibility experiment.

## 3. The Double Reduction hunch: the direction depends on a parameter the model cannot pin down

This is the one you will care about most, because it tests your Double Reduction hunch:
*if schools give more homework help and teacher feedback, families won't need to buy tutoring.*

The first run (E18) seemed to kill it. With a **universal, free, additive** +0.5 sd score-support
module, paid tutoring spend *rose* 18% (Δ = +723, 2 seed sd ≈ 63), the apex share rose 0.411 → 0.675,
and only a fully enforced ban cut spend (−63%) — by deleting the market, not by substitution.

The Council then judged that test **unfair**: the module had no demand channel, no budget constraint,
no capacity limit, no homework/teacher-time change. Under rank gates, a universal score boost
mechanically crowds takers toward the cut-off. A follow-up (E18b) gave support a real demand channel —
support damps tutoring's marginal value (a linear-damping substitution channel; a literal CES
elasticity-2 aggregator has a positive cross-partial and cannot crowd anything out):

| arm (all vs ban-only C0 = 3,669 paid spend) | paid spend | Δ vs C0 | learning guard (completion) |
|---|---|---|---|
| C1 support halves tutoring's value | 2,377 | **−1,291.5** (2sd 92) | 0.723 vs 0.716 |
| C3 support targeted to Q1–Q2 (40%) | 3,327 | **−341.4** (2sd 149) | 0.718 vs 0.716 |
| C4 support capacity-capped at 25% | 2,427 | **−1,241.2** (2sd 101) | 0.719 vs 0.716 |

**Verdict (Council-amended): C10 is withdrawn as a general claim; "substitution appears" is NOT a
finding.** E18b is a one-parameter linear damping (ts = 1 halves tutoring's value; ts = 2 fully
displaces it). The least constructed arm is C1 (ts = 1, −1,291.5, 2 sd 92.3): *substitution is
possible under a declared channel*. C2/C4 are best cases and are labelled as such.

The honest conclusion: **the direction is unidentified, because the damping parameter is
unestimated.** It hinges on the elasticity of substitution between school support and commercial
tutoring — whether they really produce the same kind of score increment. That is an empirical
question, and the most important parameter to estimate before the model can say anything about China.

> *"In this model, universal additive school support raises paid tutoring spend at high-stakes gates
> (+18%), while support declared to damp tutoring's marginal value lowers it; because the damping is
> unestimated, the effect of China's 2021 Double Reduction on paid tutoring is unidentified, and
> E18/E18b are not tests of that policy."*

## 4. What else the experiments showed

**Supports (but conditionally):**
- **Liquidity is binding.** A hard cash constraint collapses poorest-quintile basic completion from
  0.462 to **0.017** and widens the Q5–Q1 gap from 0.321 to 0.781; expanded credit narrows it to
  0.090; a shock combined with no credit drives Q1 completion to **0.001**. The shock × credit
  interaction is the safe headline — the level collapse is close to the coded constraint.
- **Ranking, not the floor, produces intensification.** At 4 reps the floor's own contribution to
  persistence is at seed noise (|Δ| ≤ 0.002) once ranking is held fixed; ranked arms give slopes
  −0.039 / −0.064 / −0.049, unranked arms +0.151 / +0.036 / +0.630. This is the paper's floor/race
  decomposition, and it is the most defensible mechanism result.
- **Memory length changes investment.** College entry (Q3–Q5) rises 0.212 → 0.511 as memory lengthens,
  and belief speed falls 0.297 → 0.012. Report as model sensitivity, not as a family-behaviour finding.
- **Learning and test performance are separable.** Raising the productive share of tutoring (ω) leaves
  pass rates flat (0.7166 → 0.7167) while later college income rises (+0.092). Pilot-strength (2 reps).
- **Actor ordering holds:** household +3.5, employer +1.7, state +1.2 years of 4.3. Lock-in appears
  only for the employer.
- **State fiscal investment does not pay back at the margin:** net −4.10 under income tax versus a
  frozen state, while attainment deepens. This supports your “capture, not return” conjecture as a
  *model* result only.

**Challenges / limitations:**
- **The default Philippine model misses its own targets.** Basic completion entry 1990–95 is 0.739
  against your 0.55–0.62; basic→college transition is 0.227 against ~0.70; the tertiary GPI is 0.868
  against 1.2–1.3. No four-country claim can be made until the case is calibrated and the misses are
  disclosed.
- **Hong Kong is data-blocked** in this window; nothing about Hong Kong is claimed.
- **Gate clustering is Yoo (2003).** The basic-bar sweep (3% → 76%) is his effort-near-cutoff result.
  Cite him as prior theory; keep only the ban/leak accounting as new (“with a 50% informal substitute,
  banning formal tutoring re-routes spend; 88% persists — enforcement and leaks, not gate design, set
  incidence”).
- **Long-run trajectories do not generate the rise.** In the batch-B long-run model (E12), the
  exogenous path rises as supplied; the endogenous path does **not** reproduce the rise (entry
  0.404 → 0.020; the smoothed post-hoc variant still falls). The degree share and premium are
  generated, but the entry path requires a supplied trend. This matches the floorworld audit: its
  rising-completion path is input-driven, not generated.
- **The allocation-rule knockout is mixed.** Rank-only and rank+cutoff both give negative slopes
  (−0.039, −0.064); “cutoff + random among eligible” gives +0.036 (not beyond 2 sd); pure lottery
  gives +0.151. So intensification is rank/cutoff-dependent, but the pre-declared “any non-rank
  allocation flips the sign” threshold was not met. Report as mixed, not as a clean knockout.
- **Independent replication confirms the rival result.** Batch B re-ran the matched-elasticity rival
  at N=3000, 72/72 runs: at σ = 0.5 the competitive world reproduces diploma-income losses
  (−0.109 and −0.175 across the two shocks) beyond 2 seed sd, with a plausible baseline. At σ = 1.0
  the losses are within noise. The income discriminator fails at high substitutability.
- **Information/recognition (batch B5, first partial test).** A richer domestic reader lowers both
  hiring error (0.045 vs 0.411 for a coarse reader) and certification demand (0.062 vs 0.217); the
  pre-declared "rising certification demand" half-claim is contradicted. The foreign-recognition sign
  is a declared parameter artifact, not an empirical claim.
- **External enrolment benchmark (E21, new UIS panel).** The uncalibrated Philippine model reproduces
  *levels* roughly (primary MAE 3.4 pp; tertiary 5.4 pp) but not the *shape* of the post-1990
  expansion (secondary corr −0.33, tertiary corr −0.40). The Korea-like preset badly under-predicts
  tertiary (41.0 vs 93.7 observed) and must not be quoted as a Korea forecast. Observed cells only;
  imputed UIS cells were not used as truth.
- **The insurance/outside-option story is contradicted (C4).** In the stock model, falling non-degree
  income *lowers* college entry (−0.0875, 2sd 0.041), in the same direction as degree-premium
  compression (−0.0991). Only the human-capital/liquidity factors raise investment (education cost
  down +0.120, borrowing up +0.104). Volatility is insurance-like only at the bottom quintile. The
  paper's "insurance against a bad outside option" reading is not what the model does.
- **The border penalty is about information access, not foreignness (C5).** A well-informed foreign
  reader (true productivity weights, institutional tier visible) has an error gap of +0.014
  (2sd 0.017) versus the domestic detailed reader — inside the pre-declared band — while the lossy
  foreign reader is +0.212 (2sd 0.058). Corruption (κ=0.6) raises error +0.026 and widens the SES hire
  gap +0.096 without moving top-tertile exclusion: access shifts to paying households.
- **Children's four states: shock → out-of-school is supported (C6, first childworld cell).** Baseline
  shares school 0.289 / both 0.174 / work 0.116 / neither 0.421; higher shock risk raises out-of-school
  (+0.0087, 2sd 0.0016; +0.0131 at higher risk) against a fixed-share baseline response of 0. The high
  baseline "neither" share is flagged for validation, not treated as an estimate.
- **No atlas-engine cells ran** (`floorworld`, `childworld`, `relfloor`, `firms`, `tutoring_abm`).

## 4b. Iteration 1's hinge: the model can't yet identify its own rivals, and the economy is one-way

Two cell results are the reason this is now a research loop rather than a finished report:

- **C1 (recovery/identification): the two central worlds are not distinguishable.** On six aggregate
  moments, a surplus/relational-floor world and a competitive-CES world fit the same data equally well
  (distances 0.012–0.023 both), a competitive truth is never recovered (0/2), and a truth *outside* the
  model set is confidently assigned to the surplus world (forced identification). Yoo's fixed-cutoff
  world is identifiable. More simulation of the same two worlds will not separate them — new moments or
  natural experiments are required.
- **C2 (floorworld): attainment is supplied; jobs are not from schooling.** Freezing the schooling
  schedules at 1980 removes essentially all of the basic-completion and tertiary rise, while 60–90% of
  the formal-job rise survives with schooling frozen. The model is one-way: the economy grows without
  schooling, and schooling grows without the economy.

Iteration 2 built the two-way interaction and an endogenous shadow sector; iteration 3 showed that the
structural shadow model **cannot reproduce the literature's stage-matched rates in any assessable
country**, so the incidence claim is withdrawn and the attempt is reported as a failed calibration — a
finding about the data and the model class, not a parameter to tune. The loop, its stopping rules, and
its success criteria are in [`06_report/RESEARCH_LOOP.md`](06_report/RESEARCH_LOOP.md).

## 4c. Stop-rule event: the model does not (yet) put shadow education where the literature does

Iteration 3 tested the loop's central ambition directly — does tutoring appear, in the model, at the
rates and stages the literature reports, without the rate being coded as a parameter? **No.**

- **Stage-matched check: FAIL in 3/3 assessable countries.** PHL all-basic 23.5% vs 46.5% literature;
  KHM grade-9 21.3% vs 68.4%, primary 12.8% vs 41.3%; HKG lower-secondary 30.6% vs 72%, middle 40.2%
  vs 82% (HKG senior-secondary 85% is excluded because it is the one calibration). Korea, Japan and
  HKG-1996 could not be assessed (no country variant / no dated model).
- **No defensible parameter combination reproduces the Philippine rate.** A joint structural search over
  gate stakes, public-school substitutes, income distribution, provider cost, teacher capacity and
  credential returns gives best RMSE 11.7pp for PHL; KHM partial (8.3pp); HKG fits its two checks but
  with 8 parameters for 2 targets (weak identification, not validation).
- **Price/entry economics: unable to assess.** The only verified fee moments are Korean; there is no
  Korean model variant, and no observed PH/HK/KHM fee moment.

**Consequence (the loop's own stop rule): the program stops claiming shadow-education incidence.** The
claim that the model reproduces where shadow education appears is withdrawn. What survives is the
method, the negative/identification map, and a provider/fee economics question that needs a Korean
variant and more data. The next round is identification-focused (recovery with outside-set truths,
holdout) and data-first (close the shadow-incidence data gap), not another incidence fit.

## 4d. Iteration 5: the gate-position story is dropped; one small income-gradient result survives

The Council's top-ranked test was whether **where the binding gate sits** explains the cross-country
gradients — Korea falling (86.0 / 75.4 / 66.4) and Hong Kong rising (35.1 / 46.6 / 70.3). It was run
with frozen structural parameters and **no take-up fitting**, gate dates taken from the country cards.

- **E1: FAIL.** Policy-dated assignment (Korea = gate at every transition; Hong Kong = terminal-only)
  gives six rates 20–59 pp too low: Korea 27.3 / 25.0 / 24.4; Hong Kong 14.4 / 19.7 / 46.7. The
  *shapes* are right (Korea falls, Hong Kong rises) but the levels are not, so **the gate-position
  story is dropped, not re-fitted.** This is the programme's decisive negative on its central mechanism.
- **E1b: the Korea no-fit rescue also fails.** Fitting only three fee multipliers to official Korean fee
  moments leaves participation at 27.8 / 24.6 / 23.3 vs 86.0 / 75.4 / 66.4. **The stop-rule stands
  permanently: no incidence claim, not even for Korea.**
- **E4: a small positive.** The income gradient is monotone and inside the predeclared band, but the
  model's top/bottom spend ratio is **2.14 vs the observed 3.67** — the demand channel exists and is
  about 40% too shallow. Hours remain `UNABLE` (no hours object).

- **E2: provider technology is not the missing channel.** At the declared quality prior the Korean
  spend mix fails (hagwon 47.7% vs 73.7% observed; only 3/36 parameterisations pass). The Hong Kong
  mass-lecture ordering reverses (−55.3 pp) but passes in 33/36 grid runs — the sign flips with priors
  and seed, so it is **not identified**. The fee/income check passes (3.56%), and a robust diagnostic
  is that observed Korean fees are **1.5–4.2× cost-plus**: a cost-plus provider block cannot price
  itself. So the candidate that would have explained loop-4's provider inversion does not.
- **E3: Japan density is not rejected but not identified.** The density elasticity needed to span
  Tokyo/Akita is 0.226 (inside the 0.1–0.6 band), but income (2.05) and gate-stakes (5.29) are far
  outside theirs, and with n = 2 endpoints the mean test is not computable. Density is collinear with
  income at the endpoints.

What this leaves is a clean negative map plus one conditional demand result. The remaining work is
data-first: better shadow-incidence and fee/breadth data for PH/KHM/CN, repeated within-country stage
gradients, provider entry/capacity data, and the empirical-relations layer (`09_relations/`) that plugs
estimated relationships into the model as parameters with identification grades.

## 5. Numbers, corrected (this is the “pull the numbers” part)

| claim | verdict | what the source actually says |
|---|---|---|
| Philippines upper-secondary completion 67.5% (2013) | **verified exactly** | UIS CR.3, DHS 2013: 67.47% |
| Philippines 67.0% (2022) | **stale** | current UIS: 68.28% (2022), 71.93% (2023), **75.03% (2024, LFS)** — the correction strengthens your post-reform argument |
| “more than half lost before secondary completion” | **contradicted** | max implied loss ≈ 41.1% (1999); 32.5% in 2013. Date the “four in ten” figure to c.1999–2004 or restate |
| Cambodia “6% / 6.6%” | **resolved** | CLFS 2019 Table 5.3: 6.6% of **employed persons 15+** have a university degree (urban 13.8%, rural 2.9%). Not a share of jobs; the “Phnom Penh 6%” recollection is unsupported |
| Cambodia informality | verified | 88.3% of 7,883,106 employed (CLFS 2019 Table 6.2) |
| Hong Kong 85% senior-secondary tutoring | **weak attribution** | traced to Kwo & Bray (2011) reporting a 2010 survey the authors themselves call “not statistically robust”; usable 1996→2010 trend is 40% → 85% |
| HKDSE “norm-referenced, fine-grained” | **wrong description** | HKEAA standards-referenced, 5 levels + 5*/5** — coarse, not fine-grained |
| Ng & Yip (2020) | **citation suspect** | printed subtitle is verbatim Gee (2012) IPS WP-20; no Ng & Yip article found. Do not silently substitute Gee |
| Breen–Goldthorpe | **not cited in either draft** | 0 hits |
| Stange 14%, PIDS 32/19/16.2pp, Abarcar–Theoharides ~9 | **unverified** | October silently drops June's external numbers; the model claims got stronger while the empirical backing got thinner |

## 6. What the paper can and cannot claim now (Council verdict)

**Lead with one conditional sentence:**
> “In this model class, a graduate-supply shock with formal vacancies fixed lowers diploma holders'
> formal-employment probability substantially under credential-rationed hiring; the absolute-income
> version fails against a matched competitive benchmark, whose formal-employment response does not fall
> at σ ≤ 2.”

**Second plank:** the floor/race decomposition — floor as eligibility, race as intensification, floor
*movement* as the additional effect — plus the many-dated-readers framing for the Philippines.

**Withdraw before submission** (Council brief 003, signed): the absolute-income discriminator; the
bar sweep as a discovery (Yoo 2003); E18 *or* E18b as Double Reduction evidence; the phrase
"substitution appears" (the direction is unidentified); E3/E5 as discoveries; "the floor is an engine
of persistence"; **all massification trajectories/projections** (the generated path collapses — they
are conditional accounting, not forecasts); every four-country / Hong Kong / transfer claim; "rising
certification demand with reader detail"; and the σ = 0.5 income corner in either direction.

## 7. What I would do next, in order

1. **Estimate the substitution elasticity between school support and commercial tutoring.** This is now
   the single most decision-relevant parameter in the whole programme: E18 and E18b point in opposite
   directions because of it, and no amount of further simulation will settle it. It needs data (e.g. a
   policy-exposure design with school homework/teacher-feedback intensity and paid-tutoring spend).
2. **Propagate E13c**: rewrite Prediction 2 around formal-employment probability, and replace the
   σ=0.5 income corner with the σ=2 fully-matched cell everywhere.
3. **Calibrate the Philippine case** to its own targets and publish the residual misses before any
   country statement.
4. **Build the China Double Reduction test properly** — dated policy evidence, separate
   restriction/homework/teacher-feedback/provider-substitution channels, no-effect baseline. This is a
   paper in its own right and the current model cannot identify it.
5. **Run the recovery study** (simulate from each rival, mask the generator, fit all rivals) — this is
   the cheapest way to show what the model can and cannot identify, and it is what a referee will ask for.
6. **Add the private-provider fourth leg** for the nursing failure (0.25 licensed per migrant versus
   the ~9 causal estimate). October already names this as its own failure.
7. **Fix the citations and the dropped numbers** before Bjørn sees the next draft. A referee who finds
   Yoo or Ng & Yip costs far more than an honest correction now.

## 8. The honest bottom line

The code you built is real, runs, and reproduces its own headline tables. The mechanisms are
internally coherent, and the floor/race decomposition is a genuine contribution. This run also found
two things that force revisions: **the graduate-supply income discriminator fails against a fairly
matched rival** (only the formal-access version survives), and **the Double Reduction/school-support
direction is unidentified** — it can intensify the race when support is additive and universal, and it
can crowd out paid tutoring when support substitutes for it. That is more useful than a clean result:
it tells you exactly what the paper may claim, which parameter decides the China question, and which
experiment (a level-matched rival, a measured substitution elasticity, and real China policy data)
would actually move the field.

Nothing in this package is causal evidence about the Philippines, Cambodia, Hong Kong or China. It is
a reproducible map of what your model can and cannot say — which is what you asked for.

---
*The synthetic Council of Experts is an AI construct: panelists are composite personas grounded in
published literature. Nothing in the council files is a statement by, or endorsed by, the named
scholars. Charter and disclaimers: `08_council/CHARTER.md`.*
