# FINDINGS — COEVOLUTION v0 (mutual adjustment: towns, providers, gates, cohorts)

**`SIMULATED`.** Every number in this report is produced by a simulator built to a frozen
pre-declaration (`PRE_DECLARATIONS.md`, sha256
`7d25e17631a39f556a17ac62a53de12701d60dca6d09a05e2b080d8d3184799d`). **No observed series was read or
fitted; no country is described; no causal or directional claim is made.** The v0 results are
model-internal and are reported as such. The independent harness that re-derived the numbers below is
in `harness/` and is summarised in `HARNESS_VERIFICATION.md`.

The v0 simulator is built, runs, and its published tables reproduce. Its two headline falsifiers fire:
the three one-change counterfactuals produce the **same** family response, and the spillback experiment
finds **no** spillback. The decisive coexistence test passes, with an important qualification about
what its selective-places criterion actually measures.

---

## 1. What the model is and does, in plain English

A district of **one town** and **eight villages** (2 to 18 km away) is followed for 30 years. Each year
**1,200 children** enter primary school; over 30 modelled years, 24 entry cohorts (years 0–23) plus 11 earlier
"burn-in" cohorts (years −11 to −1) fill the district, so year 0 starts with a school system that has a
history rather than a declared enrolment guess. Report-card items are scored on the 12 cohorts entering
in years 6–17, the window the predeclaration fixes for the decisive test.

Four kinds of decision meet in the model:

1. **Families** decide, year by year, whether another year of school is worth more than the actual
   alternative — the child's work at home or in the market, or staying home. What they weigh is
   declared, not estimated: knowledge, the experience of attending, and the credential (which is
   multiplied by the chance of passing the *next* gate), minus fees, minus the cost of getting there,
   minus the child's wage, plus the value of keeping the next level open.
2. **Providers** decide whether a place exists. A district authority has a budget, observes children
   with no place within reach, and may open a village class, add a town section, or spend on quality
   instead. A private provider enters where fees from families able to attend cover a class. **No seat
   total, capacity path or enrolment target is put into the inputs** — this is the D0 rule, and it
   passes (`D0_CHECK.json`).
3. **Gates** ration the transitions: primary to lower secondary (a place must exist and be accepted),
   lower to upper secondary, upper secondary to a **selective** track (exam score and a fixed number of
   places, with qualified applicants turned away), and upper secondary to **university** (exam, fee and
   a fixed number of places). Post-secondary non-tertiary is a separate track.
4. **Cohorts change the next cohort's circumstances.** Three responses are declared and can be switched
   on separately: more completers create demand for the next level; a secondary class within reach
   raises the value of finishing primary; and accumulating graduates raise the credential an employer
   asks for while lowering the return to a given credential.

**Tutoring** is bought for two declared reasons: *catch-up* for a pupil below the instruction threshold,
and *gate* hours for a pupil near an admission margin. Its concentration around the selective gate is
an **output** inspected after the run, never an input.

The suite is **8 arms × 3 paired seeds = 24 runs in 17.9 s**: the baseline, three one-change
counterfactuals (travel costs halved; ordinary places expanded; selective places × 1.5), three
report-card-B sequence arms (a mandate without funding; fees abolished with travel costs remaining;
graduate supply "doubled"), and the spillback experiment.

---

## 2. Verdict 1 — the four coexistence phenomena: `COEXISTENT`

The declared test asks whether, in one district and one cohort, four things hold **at the same time**:
unused accessible ordinary places, early leaving, oversubscribed selective places, and concentrated
gate tutoring. In the baseline they do.

| criterion | threshold | baseline district × cohort cells passing | cell mean (min–max) |
|---|---|---|---|
| (a) unused accessible ordinary places | ≥ 10 % of offers | **36 / 36** | 0.268 (0.251–0.284) |
| (b) early leaving (entered lower secondary, left before completing) | ≥ 5 % | **36 / 36** | 0.172 (0.126–0.227) |
| (c) qualified applicants per selective place, with turned away > 0 | ≥ 1.20 | **36 / 36** | 6.06 (4.89–7.00) |
| (d) gate hours per applicant ÷ catch-up hours per non-selective pupil | ≥ 2.0 | **36 / 36** | 5.01 (1.71–28.98) |
| (d) gate-tutoring households ÷ selective applicants | ≥ 0.20 | **32 / 36** | 0.224 (0.121–0.287) |

**All four hold simultaneously in 32 of 36 baseline cells** — 12/12 for seed 20261121, 10/12 for each
of the other two seeds. The four exceptions fail only the household-share leg of (d) (0.121–0.194). The
declared rule is "at least one district × cohort cell", so the verdict is **`COEXISTENT`**; the
"12/12" shorthand is true only for the primary seed, and the household-share leg is genuinely marginal
(pooled per-year mean 0.203 against a 0.20 threshold).

Over the 30 modelled years the baseline also shows: **25.9 %** of ordinary secondary offers declined;
**17.1 %** of lower-secondary entrants leaving before completion; **5.31** qualified applicants per
selective place and **4,908** qualified applicants turned away per run; gate tutoring at **4.7 ×** the
per-pupil catch-up intensity. The two arms that do **not** show all four fail for intelligible reasons:
`MANDATE-BEFORE-FUNDING` lifts completion so far that early leaving falls to 2.9–3.3 % (criterion b),
and `SPILLBACK` raises primary persistence enough that the gate-tutoring household share falls to
≈ 0.11 (criterion d).

### 2.1 What has two peaks — named, and kept separate

This is a separate claim from the verdict, and the three candidates are reported apart:

- **Years completed is the two-peaked object.** In the baseline, **29.5 %** of pupils complete **0
  years** and **28.5 %** complete **exactly 6 years** — a mass that completes no year at all and a mass
  that completes exactly primary and stops. There are smaller modes at 10 years (9.2 %) and 12 (5.3 %).
- **Tutoring expenditure is not two-peaked.** It is zero-inflated with discrete doses: 95.7 % of pupils
  buy no gate hours; those who do buy 60 (1,172 pupils) or 120 (665) hours. Catch-up: 43.8 % buy
  nothing; doses cluster at 24, 48 and 72 hours.
- **Applications per selective place are not two-peaked.** The ratio rises from 3.23 at t = 0 to about
  6.5 at t = 18 and then plateaus between 5.8 and 6.3; it has one prominent local maximum, not two.

### 2.2 What criterion (c) actually measures — the main qualification

The gate is oversubscribed by construction of the accounting, but **the selective places are largely
not taken**. In the baseline, 371–391 pupils per seed are admitted to the selective track across the 12
scored cohorts, yet the selective level records only **41–71 pupil-years** in 30 years — **4–6 %** of
the 38 places on offer each year — while 330–370 of those admitted pupils complete upper secondary,
most of them outside the selective track. The declared fees explain the direction: the selective track charges 0.60 per year
against 0.35 for ordinary upper secondary, and its declared knowledge/experience/credential values
(1.9 / 2.3 / 3.4) exceed the ordinary track's (1.8 / 2.2 / 3.0) by less than the fee gap at the
household's own gate-pass probability. Admitted pupils therefore mostly take their ordinary
upper-secondary offer instead — they are about half town and half village — and the handful who do
attend the selective level are all recorded in villages.

So the model produces **a queue for an elite place that most qualified households decline**, not
"fierce competition for a few prestigious places". Criterion (c) is satisfied exactly as declared
(qualified per place ≥ 1.20, turned away > 0), and the verdict is not re-tuned — but the criterion is
measuring a **gate queue, not demand for the elite track**. This is recorded as defect D-4 in
`HARNESS_VERIFICATION.md`. It is the single most important thing to fix before treating v0's
coexistence result as a demonstration of the brief's "fierce competition" story.

---

## 3. Verdict 2 — do the three changes help different families? `SAME-RESPONSE`

Mean years completed, by the four declared family types, relative to the baseline (3-seed means):

| arm | town nonpoor | town poor | village nonpoor | village poor | argmax |
|---|---|---|---|---|---|
| TRAVEL-CUT | +0.047 | −0.106 | +0.057 | **+0.110** | village poor |
| ORDINARY-EXPANSION | +0.072 | −0.098 | +0.086 | **+0.183** | village poor |
| SELECTIVE-EXPANSION | +0.021 | +0.005 | −0.021 | **+0.030** | village poor |

The declared pass condition is that the argmax family type differs across at least two arms **and** each
argmax gain is at least 1.5 × another type's gain. The falsifier is a shared argmax **or** a pairwise
correlation of the 4-type gain vectors ≥ 0.95.

- **The argmax is village poor in all three arms** — the first condition fails.
- **Travel-cut and ordinary-expansion correlate at 0.991** — the correlation falsifier fires as well.
- The 1.5 × sub-criterion is reading-dependent; under the implementation's conservative reading
  (positive comparators only) SELECTIVE-EXPANSION also fails at 1.44.

**Verdict `SAME-RESPONSE`, correctly applied.** The three changes do not differentiate families in this
model: cutting travel costs and opening ordinary places move almost the same families by almost the
same amounts, and expanding selective places moves everyone a little. As the design brief anticipated,
**the schools are represented too crudely** — the family response is driven by distance, income and the
existence of a nearby place, and the three levers act on the same margins. The gains are also small
(0.03–0.18 years), and the per-seed argmax is unstable (travel-cut's argmax is village nonpoor, then
town poor, then village poor across the three seeds), so the similarity is not an artifact of averaging
in the other direction.

*Correction to the core summary's wording:* the shared argmax is **village poor** (`village`, `poor = 1`),
not village nonpoor. The gain vectors and the 0.991 correlation are confirmed to 1e-9.

---

## 4. Verdict 3 — the spillback experiment: `NO-SPILLBACK`

The question: when a secondary class opens within reach, does primary persistence rise for **younger**
cohorts in that village, over and above the control villages and the older cohorts?

| seed | treated village | delivered DiD (pp) | pure-village control (pp) | against baseline arm (pp) |
|---|---|---|---|---|
| 20261121 | v5 (10 km) | **+5.14** | +6.40 | +3.93 |
| 20261122 | v5 (10 km) | **+0.66** | +1.02 | +1.77 |
| 20261123 | v8 (18 km) | **−6.39** | −6.88 | −6.15 |
| seeds clearing 5 pp | | 1 / 3 | 1 / 3 | 0 / 3 |

The declared criterion requires **every** paired seed to clear 5 pp. Only the first does; the mean is
−0.20 pp; the third is negative. **Verdict `NO-SPILLBACK`**, and it is robust to how the control group
is defined: the delivered "control villages" turn out to be the whole district (a label/integer
comparison in the derivation never excludes the treated village or the town), which dilutes the
contrast by about 8 % without changing the verdict; the clean village-only control gives +6.40 / +1.02 /
−6.88 pp, and a strict comparison against the baseline arm gives +3.93 / +1.77 / −6.15 pp — **no** seed
clears the bar.

Two caveats on what the experiment identifies, both recorded rather than repaired:

- the SPILLBACK arm switches response (b) on for the **whole district** as well as opening one class, and
  primary persistence in non-treated villages rises from ≈ 0.50–0.52 to ≈ 0.59–0.62. The DiD nets most
  of that out, so it identifies the *incremental* effect of one extra class given response (b) already
  on — not "a class with everything else identical to the baseline", as §9 specifies;
- the treated village is small (62–97 children per cohort), so each seed's DiD rests on a few hundred
  children and the seed-to-seed spread (−6.4 to +5.1 pp) is large relative to the 5 pp criterion.

The honest summary: **in v0, opening one ordinary secondary class in a distant village did not
detectably raise primary persistence among the younger cohorts of that village.**

---

## 5. Report card A — the statistical portrait

From pupil records only, 3-seed means. The harness re-derived every item below from `panel_*.csv` and
`cohorts_*.csv` and reproduced the delivered tables to 5e-10 (`HARNESS_VERIFICATION.md` §2).

| item | baseline |
|---|---|
| cohort completion, primary (ever) | **0.541** |
| cohort completion, lower secondary | **0.213** |
| cohort completion, upper secondary | **0.115** |
| cohort completion, tertiary | **0.004** |
| entered lower secondary | 0.257 |
| early leaving (entered lower secondary, did not complete) | **0.171** |
| mean years completed | **5.09** |
| NER lower secondary, final year | 0.193 |
| NER upper secondary, final year | 0.075 |
| max NER in any cell | 0.730 |
| max GER in any cell | 0.907 |

Rural–urban differences are large at every level:

| item | town | village |
|---|---|---|
| primary completion by 14 | 0.572 | 0.426 |
| lower secondary by 18 | 0.345 | 0.158 |
| upper secondary by 20 | 0.240 | 0.069 |
| tertiary by 26 | 0.013 | 0.001 |
| mean years completed | 6.32 | 4.64 |

Technical notes that matter for reading the portrait:

- **NER cannot exceed 100** and does not in any of the 8,640 cells. **GER is allowed to exceed 100 but
  never does in v0** (max 0.907): the model never approaches universal enrolment, so the repeater
  inflation the GER convention exists to expose is never displayed.
- **No cell is capped**: repeaters and over-age pupils are reported in their own columns (peaks 937 and
  797 pupils in a year-location cell).
- **Tertiary GER uses the declared five-year band 18–22** immediately after the official secondary
  leaving age 17; **post-secondary non-tertiary is a separate level**, not folded into tertiary.
- **"Out-of-school" here means "out of level L and not above it"**, exactly as predeclared. It is not the
  conventional UIS out-of-school rate: 7.8 % of the lower-secondary out-of-school count is children
  still enrolled in primary.
- Upper secondary is tabulated as **two levels** (`upper_secondary` and `upper_selective`) with no
  combined row; the selective share of the level is 1.3 % on average.
- Early-year tertiary and post-secondary ratios (624 cells) are computed on **truncated age bands**
  because the population frame starts at entry year −11; `ner_primary_final_year` in `RUNS.json` is
  `NaN` for the same reason.

---

## 6. Report card B — the three sequences

These are **sequence and distribution comparisons, not pass/fail tests**; the predeclaration fixed no
expected direction. 3-seed means.

| metric | baseline | MANDATE-BEFORE-FUNDING | FEES-ABOLISHED | DEGREES-OUTRUN-JOBS |
|---|---|---|---|---|
| completion primary | 0.541 | **0.618** | 0.563 | 0.544 |
| completion lower secondary | 0.213 | **0.505** | 0.252 | 0.222 |
| completion upper secondary | 0.115 | **0.387** | 0.165 | 0.124 |
| completion tertiary | 0.004 | 0.004 | 0.007 | 0.005 |
| mean years completed | 5.09 | **6.92** | 5.46 | 5.15 |
| early leaving | 0.171 | **0.031** | 0.087 | 0.149 |
| unused accessible ordinary places | 0.259 | 0.165 | 0.197 | 0.248 |
| qualified applicants per selective place | 5.31 | **12.87** | 5.45 | 5.45 |
| gate-tutoring household share | 0.203 | 0.131 | 0.199 | 0.198 |
| NER lower secondary, final year | 0.193 | **0.413** | 0.223 | 0.196 |

**MANDATE-BEFORE-FUNDING** (required years raised from 6 to 9 at year 8, no extra budget) is the
strongest sequence in the model: lower-secondary completion more than doubles, early leaving collapses
to 3.1 %, and the selective queue lengthens to 12.9 qualified applicants per place. The mechanism is
compulsion, not capacity — attendance is forced where the household would otherwise decline, subject
only to the declared cash constraint — so the sequence shows what a mandate does when the places happen
to exist, and the model reports that the selective gate then absorbs the pressure.

**FEES-ABOLISHED-TRAVEL-REMAINS** (all fees to zero at year 8, travel unchanged) moves the system much
less: upper-secondary completion +0.050, tertiary completion +0.003, mean years +0.37, early leaving
down 8.4 pp. It is the clearest illustration of the model's geography: removing the fee does not remove
the distance, so the villages that were excluded by travel stay excluded.

**DEGREES-OUTRUN-JOBS does not test a glut.** The declared anchor `g0 = 0.20` sits **above** the
model's own graduate share (0.111–0.115 of the 18–22 band), so the declared rule
`req = 3 + 0.8(share − g0)` **lowers** the employer requirement (to 2.865–2.879) and **raises** the
return (to 1.068–1.076) as graduates accumulate — the opposite of a glut. Doubling the deviation pushes
the requirement further down still. The requirement move is also **inert**, because credentials are
integer levels and the access step is unchanged anywhere in (2, 3]; the arm's only live channel is a
≈ 7 % uniform credential premium, and the observed attainment changes (upper secondary +0.9 pp,
tertiary +0.1 pp, mean years +0.06) are consistent with that premium. The arm is therefore recorded as
design defect **`ARM-NOT-TESTING-GLUT`**, **not** as a result about degrees and jobs. A future
predeclared v0.1 would have to (i) take the anchor from the model's own baseline steady state, or
declare it as an external institutional constant with a sensitivity range, (ii) declare an explicit
graduate-supply instrument (a tertiary-place path or cohort-size shock) rather than rescaling the
argument of the employer rule, (iii) predeclare the expected sign of the requirement and return paths
and fail the arm loudly if the run moves them the other way, (iv) run a pre-outcome manipulation check
that the arm moves the declared object, and (v) keep the response switch separate from the supply shock
so the arm stays a one-change counterfactual. **None of that is decided here** — it is a requirement for
a future frozen predeclaration.

---

## 7. Every failure and oddity, honestly

**Failures (declared falsifiers, reported as failures, not rescued):**

1. **`SAME-RESPONSE`** — the three one-change counterfactuals share the same argmax family type
   (village poor) and the travel/ordinary gain vectors correlate at 0.991 ≥ 0.95. The schools are
   represented too crudely; no threshold, parameter or seed was changed in response.
2. **`NO-SPILLBACK`** — only 1 of 3 paired seeds clears 5 pp; mean −0.20 pp; one seed is negative. The
   result is robust to the control-group construction and stronger against the baseline arm (0/3).

**Design and implementation defects (recorded; none repaired in this phase):**

3. **`ARM-NOT-TESTING-GLUT`** — the degrees arm lowers the requirement and raises the return instead of
   testing a glut; its "doubling" acts on the employer rule's argument, not on graduate supply
   (§6 above).
4. **Selective track almost empty** — 371–391 admissions but only 41–71 pupil-years at the selective
   level, 4–6 % of the places on offer, with most admitted pupils completing upper secondary elsewhere.
   Criterion (c) measures a gate queue, not demand for the elite track (§2.2).
5. **Spillback control group** — a string/integer comparison makes the delivered "control villages" the
   whole district including the treated village and the town; the contrast is diluted by ≈ 8 %. The
   verdict is unchanged.
6. **Spillback arm is two changes** — it also switches response (b) on district-wide, so it is not
   "everything else identical to the baseline".
7. **Report-card A level split** — upper secondary is reported as two levels with no combined row.
8. **Out-of-school definition** — "out of level L" rather than "out of school" (7.8 % of the
   lower-secondary count is children in primary).
9. **GER > 100 never exercised** (max 0.907).
10. **Truncated age bands** in 624 early-year cells; `NaN` headline metrics in `RUNS.json`.
11. **Two different "selective applicant" denominators** between criteria (c) and (d).
12. **`RUNS.json` contains 24 `NaN` literals**, not strict JSON.

**Verification limits:** the full pupil-year table was not delivered (only the declared 1-in-32
sample), so per-cell NER/GER are verified statistically, not exactly; determinism is accepted from
`DETERMINISM.json` rather than re-run; the simulator was not executed by the harness. All three are
stated in `HARNESS_VERIFICATION.md` §7.

---

## 8. What v0 cannot claim

- **Not evidence about any country.** There is no observed input of any kind; the Philippines, Cambodia,
  China, Hong Kong and every other case are outside what these runs can say.
- **No fit and no validation.** No series was fitted, no known outcome targeted, no external parameter
  calibrated. `PARAMETERS.csv` is design values, `DECLARED`.
- **No causal or directional claim.** Every result is `SIMULATED` and model-internal. The
  counterfactuals are one-change comparisons inside one model, not estimates of what a policy would do.
- **No cross-country comparison and no UIS claim.** UIS metadata (country series, age bands, level
  mappings) is **HELD**: it was not verified, so no cross-country comparison is made. The report card
  uses the model's own declared bands only.
- **Not a reopening of the closed phase.** The 2026-11-20 massification records are untouched
  (`PHASE_WRITEUP.md`, `DATA_NOTES_MASSIFICATION.md`; git shows no modified tracked file), the Q-5
  correction and the B-1 footnote were not edited by this phase, and v0 validates neither the closed
  phase nor the earlier massabm/triad models.
- **The coexistence result is narrower than it looks.** It says the four declared metrics can hold
  together in one district-cohort cell in this model. It does **not** say the model generates a
  contested elite sector: criterion (c) is met by a queue whose places are mostly declined (§2.2), and
  years-completed is where the genuine two-peaked distribution lies.
- **`SAME-RESPONSE` and `NO-SPILLBACK` are findings about the model, not about schooling.** They say
  these decision rules, at these declared values, do not differentiate families across the three levers
  and do not produce a detectable spillback. They license no claim about real school systems.

---

## 9. Where the numbers live

| what | file |
|---|---|
| predeclared contract (frozen) | `PRE_DECLARATIONS.md` |
| declared parameters | `PARAMETERS.csv` |
| simulator (unchanged) | `code/coevolve_v0.py` |
| D0 / determinism / run record | `results/D0_CHECK.json`, `results/DETERMINISM.json`, `results/RUNS.json` |
| pupil records | `results/panel_*.csv` |
| pupil-year sample (1-in-32) | `results/pupilyear_*.csv` |
| report card A | `results/aggregates_*.csv`, `results/cohorts_*.csv`, `results/families_*.csv` |
| coexistence metrics | `results/coexistence_*.csv` |
| gates | `results/transitions_all_arms.csv` |
| spillback | `results/spillback_SPILLBACK.csv` |
| object values | `results/objects_all_arms.csv` |
| independent verification | `HARNESS_VERIFICATION.md`, `harness/out/` |
| numbers cited here, regenerable | `harness/out/REPORT_NUMBERS.md`, `harness/out/verification_results.json` |

*Predeclaration hash verified unchanged:
`7d25e17631a39f556a17ac62a53de12701d60dca6d09a05e2b080d8d3184799d`.*
