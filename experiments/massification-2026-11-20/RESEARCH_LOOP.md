# The research loop — how this program iterates

This is not a finished product. It is a loop: **country evidence → targets → model → falsification →
Council → next iteration.** Each iteration must leave behind (a) executed cells, (b) the numbers that
failed, and (c) one changed variable that could change the answer.

## 0. Why iteration 2 exists (what iteration 1 forced)

Iteration 1 produced 23 executed cells and one reproduction audit. Three results define the next loop:

1. **No identification between the two central worlds (C1).** On six aggregate moments, a
   surplus/relational-floor world and a competitive-CES world are fitted to the *same* distances
   (0.012–0.023 both), and a truth *outside* the model set is confidently assigned to the surplus world
   (forced identification, 2/2). Yoo's fixed-cutoff world is identifiable (2/2). **New aggregate moments
   or new data are needed — more simulation of the same two worlds will not separate them.**
2. **Attainment is supplied, jobs are not (C2).** Freezing the schooling schedules at 1980 removes
   ~all of the basic-completion and tertiary rise in floorworld (supplied share +1.00 to +1.19), while
   60–90% of the formal-job rise survives with schooling frozen. The model is one-way: the economy
   grows without schooling, and schooling grows without the economy. **Iteration 2 must build the
   two-way interaction, not re-parameterise the one-way one.**
3. **Shadow education is a coded response, not yet an outcome.** Iteration 1 reproduced gate-clustering
   and showed that school support can either intensify or displace paid tutoring depending on an
   unmeasured substitution elasticity. **It has not shown that tutoring appears, in the model, at the
   rates and stages the empirical literature reports.** That is the target of iteration 2.

## 1. The loop

```
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  A. COUNTRY EVIDENCE  (lit + data)                                      │
   │     report cards: shadow-ed incidence by stage/provider, gates, cohort  │
   │     flows, economy context; every number sourced and dated              │
   └───────────────────────────────┬─────────────────────────────────────────┘
                                   ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  B. TARGET SET  (calibration vs check)                                  │
   │     TARGETS_SHADOW.csv, TARGETS_FLOW.csv, ECONOMY_SERIES.csv            │
   │     declare which are targets (fit) and which are checks (not fit)      │
   └───────────────────────────────┬─────────────────────────────────────────┘
                                   ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  C. MODEL  (country configs + two-way economy + endogenous shadow)      │
   │     parameters labelled sourced / estimated / fitted / assumed          │
   └───────────────────────────────┬─────────────────────────────────────────┘
                                   ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  D. FALSIFICATION  (predeclared)                                        │
   │     held-out period; rival models; recovery/identification; the miss     │
   │     that would kill the claim                                           │
   └───────────────────────────────┬─────────────────────────────────────────┘
                                   ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  E. COUNCIL  (synthetic panel, adversarial)                             │
   │     what is imposed, what is discovered; amendments; next experiments   │
   └───────────────────────────────┬─────────────────────────────────────────┘
                                   ▼
                        next iteration (change one variable)
```

## 1a. Amended loop (binding after Council brief 004)

The Council's design review rejected fit-first sequencing: calibration must be preceded by
falsification design, not followed by a review. The following are now binding on iteration 2.

**Before calibration, label every target row `fit` or `check`, with a predicted sign per candidate
world (surplus / competitive / Yoo).** A calibration target may never double as a check.

**Six anti-re-parameterisation requirements**

1. Add moments with *different* predictions across candidate worlds: formal-access response to
   graduate supply; stage/provider shadow take-up; wage-premium dynamics; informality transitions.
   At least two must be real-data and excluded from the fit.
2. Fit 1980–2010, hold out 2011–2024 (and leave one country/stage untouched). Report out-of-sample
   misses, not just in-sample fit.
3. Carry a truth *outside* the candidate set each round; report the forced-identification rate.
   (C1's baseline: outside truth forced into the surplus world 2/2.)
4. Replace at least one behavioural schedule rather than recalibrating it, and show the generated
   path is stable (B4's endogenous collapse is the warning).
5. Symmetric two-way test: freeze schooling — does the job path rise? Freeze wages/jobs — does
   attainment rise? If neither moves, the two-way claim is a schedule, not a model.
6. Shadow take-up and provider mix are **checks, never fitted shares**. Fitted objects are household
   demand, provider entry cost, and teacher-tutor capacity. If matching a literature rate requires
   setting the tutoring rule to that rate, the result is a restatement and must be labelled.

**The structural variable for iteration 2 is provider supply/entry, including teacher-tutor
capacity** — the change that creates a new checkable moment, endogenises the economy→education leg,
and addresses the paper's nursing failure (0.25 versus ~9 licensed per migrant).

## 2. What "shadow education appears where the literature says" means operationally

It is **not** "the model has a tutoring rule". It is:

- For each country × stage, the model's **take-up rate** must fall inside the literature's reported
  range (or we report the miss), **without** the target being directly coded as a parameter.
- The **provider mix** (commercial firms, teacher-tutoring, informal) must respond to demand and
  capacity, not be fixed shares.
- The **gate position** of tutoring must match the observed stage (e.g. upper-secondary/tertiary
  entrance vs basic completion).
- **Spending** and **hours** should scale with income and gate stakes in the direction the surveys show.
- The shadow sector must be able to **expand as an industry** (provider entry) at the same time as it is
  a **household response** — both "creating opportunities" and "being the opportunity".

The first target table will be `02_lit/SHADOW_TARGETS.csv`; the first fit table
`05_experiments/loop2/CALIBRATION_TABLE.csv`.

## 3. The two-way economy requirement

The economy side must be a *model*, not a schedule:

- **Education → economy**: human capital raises productivity, formal-job creation and complex-job
  share, with a stated elasticity and delay; the model must report the formal-job path with schooling
  frozen vs endogenous, so the generated share is visible.
- **Economy → education**: wages, formal opportunities, informality risk and returns shape household
  schooling and tutoring choices; include the case where schooling does **not** create jobs.
- **Both**: the same household decision is simultaneously an investment in opportunity and a purchase
  of position — the model must be able to show both, and the identification study must say which is
  doing the work in each country.

## 4. Iteration log

| iteration | what ran | what changed | what it forced |
|---|---|---|---|
| 1 (20 Nov, AM) | 23 cells: floor/race, grad supply, liquidity, memory, gates, actor knockouts, state, China support, information, trajectories, child states, recovery, floorworld, PH benchmark | established the mechanism suite; reproduction audit | C1 no identification; C2 one-way economy; shadow incidence untested |
| 2 (20 Nov, PM) | 6 country cards + 21-row shadow target table; WDI/UIS target sets; two-way economy module with provider entry/teacher-tutor capacity (150 trajectories, 0 failures); calibration loop + cohort ledger (in progress); Council design review (004) and results review (005) | changed variable: **provider supply/entry + endogenous two-way economy** | **Two-way test: the job side is still ~a supplied schedule** (freezing schooling still lets complex vacancies rise; schooling adds only 3–4% of jobs). **Economy→education is the dominant direction** (+6.7–11.8pp live vs +2.2–2.8pp frozen), with a 20–40% residual shadow-supply channel. **Shadow pattern not identified by one moment**: fitting HK 0.85 forces PH/KHM to 0.88–0.89 with no target to check. Teacher-tutors dominate supply (76–97%); endogenous entry raises take-up 46–66pp. Positional response is a null in this specification. |
| 3 | (to be designed from iteration 2's misses) | one variable at a time | |

## 5. Stopping and falsification criteria (declared before iteration 2 results)

The program stops claiming a mechanism when any of these is true:

1. **Shadow incidence fails**: after calibration, the model's take-up by stage is outside the
   literature range in ≥2 of the 4 main countries, and no plausible parameter change fixes it.
2. **Two-way feedback is imposed**: the generated formal-job share is unchanged when schooling is
   frozen (then the economy leg is a schedule, not a model).
3. **Identification fails**: adding the new moments still cannot separate the surplus world from a
   competitive world, and no natural experiment is proposed.
4. **Cohort flows do not balance** or require impossible transition rates to hit targets.
5. **The target was coded as a parameter**: if matching the literature rate requires setting the
   tutoring rule to that rate directly, the result is a restatement, not a finding.

Additional stop rules (Council brief 004):

6. **Out-of-sample miss**: if held-out 2011–2024 misses exceed a declared threshold, no country claim.
7. **Sign instability of an unmeasured parameter** ⇒ withdraw the claim (the substitution elasticity
   is the live case; E18/E18b already show the sign flipping by specification).
8. **Institutional-parameter audit**: if a country result depends on hand-set floors, readers or
   regulation parameters rather than behaviour, it is description, not mechanism.
9. **Iteration budget**: two iterations without an identification gain ⇒ stop claiming the mechanism
   and publish the equivalence/negative map (which is itself the contribution).

A stage is **publishable** when it has: executed cells, a predeclared comparison, a disclosed miss, and
one result that a referee could try to replicate.

## 6. Status (updated by the Lead as the loop runs)

- Iteration 1 package: `massification-2026-11-20/`; GitHub branch `experiment/massification-2026-11-20`.
- Iteration 2 workstreams: `02_lit/COUNTRY_CARDS/`, `04_data/TARGETS_*.csv`,
  `05_experiments/loop2/`, `05b_experiments/loop2/`, `08_council/brief_004`, `brief_005`.
- Current open questions and costed next steps: `OPEN_QUESTIONS.md`.
