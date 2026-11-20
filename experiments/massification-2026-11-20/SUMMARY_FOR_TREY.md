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

## 2. The graduate-supply test: the income version dies, the formal-access version survives

Your October Prediction 2 says a graduate-supply shock separates the surplus account from a
competitive market on **diploma holders' absolute income**: under surplus, diploma holders lose;
under competition, they gain as they become scarcer.

Two follow-ups tested that, and they changed the verdict twice.

**First (E13b), the income version looked dead.** When the competitive world got the same
formal/informal margin, vacancies and shock, a CES market with high substitutability (σ = 0.5) also
produced diploma-income losses (−0.059, then −0.109 in an independent N=3000 replication). So
absolute income does not separate the accounts.

**Then (E13c), level-matching revived the formal-access version.** The two worlds did not start from
the same place (formal share 0.27 vs 0.46; degree-income scale 2.9 vs 24–32). E13c matched the
baseline formal share (0.2795 vs target 0.286), the vacancy path and the shock, and re-ran:

| world (college half price) | Δ diploma formal-job probability | Δ diploma income |
|---|---|---|
| surplus (slots + floors + rank) | **−0.1511** (sd 0.022) | −0.0583 (0.018) |
| level-matched rival, σ = 0.5 | +0.0085 (0.011) | −0.0270 (0.048) |
| level-matched rival, σ = 1.0 | +0.0095 (0.008) | +0.0001 (0.002) |
| level-matched rival, σ = 2.0 | −0.0054 (0.003) | +0.1252 (0.017) |

The level-matched rival **never shows a material formal-employment fall** (≤ 0.5 pp at σ = 2, versus
−15.1 pp under surplus). Batch B reached the same reading independently: B1's σ=0.5 firing cell is
numerically unstable (baseline ratio 0.022–0.055 and degree income 1.0–42.4 across seeds), and at
σ = 2 the rival clearly gains.

**Verdict:** Prediction 2 **survives as a formal-access claim**, simulation-only:
> when hiring is credential-rationed, a graduate-supply shock with formal vacancies fixed lowers
> diploma holders' formal-employment probability by about 15 points; a level-matched productivity-
> hiring rival shows no material fall (≤ 0.5 pp at σ = 2).

**Withdraw only the absolute-income version.** Caveats that belong in the same sentence: degree income
could be level-matched only at σ = 2; the B1 replication was not blind; the formal share is matched to
0.28, not estimated.

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

**Verdict: C10 is withdrawn.** Substitution appears once support has a demand channel, and completion
does not fall. So E18's “race absorbs the subsidy” was an **artefact of the additive, universal,
no-demand-channel support** — it is not evidence against your hypothesis. Equally, E18b is a
**best-case construction for you**, not evidence for it.

The honest conclusion: **the Double Reduction effect is not identified by the model.** Its sign hinges
on the elasticity of substitution between school support and commercial tutoring — i.e. on whether
they really produce the same kind of score increment. That is an empirical question, and it is the
most important parameter to estimate before the model can say anything about China.
**Do not describe E18/E18b as a measured Double Reduction effect**: no COVID, no policy timing, no
real Chinese data, and the direction is specification-dependent.

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
- **No atlas-engine cells ran** (`floorworld`, `childworld`, `relfloor`, `firms`, `tutoring_abm`).

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

**Withdraw before submission** (Council, updated after E18b): the income discriminator; the bar sweep
as a discovery (Yoo); treating E18 *or* E18b as a Double Reduction effect (the direction is
unidentified); E3/E5 as discoveries; every four-country / HK / transfer claim; and “the floor is an
engine of persistence.” Also withdraw the claim that school support *cannot* crowd out tutoring —
E18b shows it can, when support and tutoring are substitutes.

## 7. What I would do next, in order

1. **Estimate the substitution elasticity between school support and commercial tutoring.** This is now
   the single most decision-relevant parameter in the whole programme: E18 and E18b point in opposite
   directions because of it, and no amount of further simulation will settle it. It needs data (e.g. a
   policy-exposure design with school homework/teacher-feedback intensity and paid-tutoring spend).
2. **Finish E13c (level-matched rival)** and rewrite Prediction 2 around formal-employment probability.
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
