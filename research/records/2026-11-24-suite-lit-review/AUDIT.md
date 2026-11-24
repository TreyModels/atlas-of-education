# Prior-art and mechanism audit of the GPU micro-simulation suite

**Record:** `research/records/2026-11-24-suite-lit-review/` · branch `research/suite-lit-review-2026-11-24`
**Base commit:** `51f9f02` (handoff head, from `origin/research/handoff-2026-11-24`).
**Auditor:** suite-auditor (task-4, Job A). **Date of audit:** 2026-11-24 (UTC).
**Status:** COMPLETE. Audit only — no suite script was executed. No suite results exist to audit; the payload
under review is `research/records/2026-11-24-gpu-suite/` as committed, which contains a design and four scripts
but no runs and no outputs.

**Method.** Read-only. (i) `git show` on the cited branches; (ii) line-by-line code inspection of all four
scripts; (iii) citation verification against Crossref/OpenAlex metadata records, DOI landing records, publisher
pages, and the primary PDFs of ILO and UN instruments fetched on 2026-11-24; (iv) a World Bank API pull on
2026-11-24 to establish what the exp3/exp4 input series actually contain. Numbers in this record are either
quoted from committed records (with commit), read from a public data API on the audit date (with the query in
the provenance appendix), or are arithmetic on the *published equations* in the suite scripts — arithmetic is
labelled as such. Nothing here is a simulation result.

**What this audit is not.** Not a systematic review; not a reading of the full texts of the cited books/papers
(claims about their content rest on abstracts/records and are marked so); not a judgement about whether the
Atlas's macro-wall finding is real (the E1/Q3 records are cited, not re-verified).

---

## 0. Verdict in one page

The suite is a **possibility demonstration of one builder's reduced-form parameterisation**, not an
implementation of the mechanisms it cites, and three of its own pre-registered inferential objects — the
macro-wall test (H1), the Q1 zero-signal tie-breaker test (H4), and the ABC identifiability gate (exp3) — are
**not implemented by the committed code**. It can honestly establish a methodological template and a
conditional "here is how the logic of the wall could work"; it cannot support any claim about schooling,
child labour, fertility, history, or policy.

| DGP (claimed mechanism) | Faithful mapping to citation? | Load-bearing parameter that is unjustified | Construction-implied observables | If published, would overreach |
|---|---|---|---|---|
| `DGP_POVERTY` (Basu–Van 1998; Baland–Robinson 2000) | **No — reduced form.** Child earnings never enter household income; no credit constraint, no labour market, no borrowing, no fertility choice. A utility penalty on an exogenous income gap replaces the core mechanism. | `w_pov=2.2`; `y_sub=0.90·0.985^t` (−1.5 %/yr, no source); adult shock 8 % iid ×0.55 (no source); gap coefficients 0.45/0.30/0.70 | `hidden_to_sw_ratio`, `enrolled_work_hrs_p90`, `tutor_income_corr`, `mean_learn` are all functions of the same income/ability draws and the same four utility weights | "Poverty-driven child labour reproduced"; "subsistence mechanism tested" |
| `DGP_SCHOOL_PUSH` (Nordtveit 2010a/b) | **Partly — metaphor.** 4-state taxonomy is the model's own; only three states map to standard survey categories. Hidden-cost and hostility magnitudes unsourced. "Hidden work" is not affected by hidden costs or hostility, only by the ban. | `w_push=2.0`; `ψ=0.45`; `h_hidden=0.35`; the 0.45/1.0/0.55 coefficients on ψ | `hidden_to_sw_ratio` directly encodes the state mix; learning is a state indicator | "Nordtveit hidden-cost/hostility mechanism tested"; "bans push youth into hidden work (found)" |
| `DGP_CROWDING_TUTOR` (Bray 2016/2018; Jayachandran 2014; Dang–Rogers 2008) | **No — reduced form.** No teacher agent, no class size, no provider identity, no tutoring price/expenditure; `β_div` is a parameter, not the incentive mechanism Jayachandran formalises. | `w_tutor=2.2`; `div=0.22`; `shadow_cost=0.32`; `q_pub` trajectory rule; 0.5·β tutoring bonus | `tutoring` is binary take-up driven by a threshold; `tutor_income_corr` is a correlation of a binary, not an income gradient | "Shadow-education/crowding mechanism tested"; "tutoring income elasticity measured" |
| `DGP_MIXED` | **None.** A convex-combination parameter vector, not a mechanism. | `w_pov=1.4`, `w_push=1.3`, `w_tutor=1.6`, `div=0.12` — a compromise point, no theory | all of the above | "Mixed-mechanism world" as anything but an interpolation check |

| Arm | Real-world referent | What the code actually changes at t=10 | Confound | Verdict |
|---|---|---|---|---|
| `tuition_only` | Official fee abolition only (hidden costs and hostility remain) | `f_pub 0.45→0`, hidden cost 0.35 and hostility 0.45 unchanged, capacity dilutes (`cap_scale=0.30`) | Fee abolition coincides with a −1.5 %/yr subsistence-threshold drift in **every** world and arm; no no-reform control arm | Defensible as a stylised "fees only" arm; but no counterfactual |
| `protective_capacity` | Does not correspond to a single real policy | `f=0`, `h_hidden 0.35→0`, `ψ 0.45→0.05`, `cap_scale=1.00`. "Capacity" never expands: `q_pub` is capped at its baseline 0.65; `cap_scale=1` only stops dilution | Bundles four interventions; cannot attribute anything to "protective capacity" | Withdraw the label; it is a bundled "school made free, cheap and welcoming" arm |
| `binary_ban` | Compulsory-schooling / child-labour ban without closing the cost gap | `ban=1.8` subtracts 1.8 from the study-and-work utility and adds a +0.85 swing to hidden work vs visible work | The pre-registered "Nordtveit backfire" is hard-coded: utilities move by ±0.40–1.80 against a noise band of ±0.225 | Cannot be a *finding*; at most an assumption, stated as such |

**Three strongest findings** (expanded in §5–§7): (1) the micro "tie-breaker" features are transforms of the DGP
weights, and the Q1 zero-signal control is not implemented and cannot be implemented without a strength-separable
redesign; (2) the pre-registered backfire (H2) is guaranteed by hard-coded utility constants, not emergent;
(3) the empirical arms are not estimable as specified — two pooled moments for four parameters, an unmeasured
"hidden work" state calibrated to measured employment, and a sparse survey outcome for a staggered TWFE.

---

## 1. What the payload is, and what has actually been run

| File | sha256 (2026-11-24) | Claims | What the code does |
|---|---|---|---|
| `scripts/exp1_unified_gpu_abm.py` | `33cd60c6…0e7da8` | unified 4-DGP/3-arm ABM, Philox RNG, Q1 zero-signal control | 213-line CuPy single-kernel multinomial-choice simulator; emits 11 summary fields per (dgp,arm,seed,year) |
| `scripts/exp2_macro_wall_and_tiebreaker.py` | `847607ed…5ff3d` | macro-wall check + micro tie-breaker classification | pre/post means per cell; 2-feature vs 4-feature logistic classifier; **no FE regression, no zero-signal branch, no overlap statistic** |
| `scripts/exp3_rejection_abc_realdata.py` | `646de67f…d6e341` | rejection-ABC fit to public WDI/UCW targets, 0.80 identifiability gate | 4-parameter, 2-moment synthetic ABC over one kernel step; fixed unlogged nuisance parameters |
| `scripts/exp4_fee_abolition_child_labor.py` | `5809aced…84ee3a` | TWFE check of fee abolition on ILO/UCW child-labour series | staggered TWFE on sparse survey outcome; **crashes on its first network call** (see §7.4) |
| `METHODOLOGY.md` | `2df6b4fd…461cb6d` | four-step pipeline | aspirational; several steps are not implemented |
| `PRE_REGISTRATION.md` | `5899c95a…ef60b08` | H1–H4, reporting rules | H1 and H4 have no executable implementation; H2 is pre-determined by the code |
| `run_all.sh` | `84a5ae02…96ae03` | end-to-end | requires CuPy (so cannot run on the CPU/Apple path); `sha256sum` is not a macOS default; no interpreter/version/hash logging |

No results directory, no logs, no `REPORT.md`, no seeds file are committed. This is consistent with the
handoff's statement that the Apple-Silicon port is the branch that will run it. **Every claim in this audit about
behaviour is therefore a claim about the code, not about output.**

The four scripts are internally inconsistent about the story the suite is supposed to test:

1. `METHODOLOGY.md` §3 promises "standard 10-year country + decade FE regressions on the synthetic macro panel";
   `exp2` runs no regression at all and there is no country dimension in `exp1` (one `base_y` population per
   seed; "country" and "country-arm" are the same object). There is nothing to put a country FE on.
2. `PRE_REGISTRATION.md` H1 promises "cross-DGP macro slope overlap > 75 %"; no overlap statistic is computed
   anywhere.
3. `PRE_REGISTRATION.md` H4 promises a `strength = 0` chance-accuracy control; the string `strength` does not
   occur in any executable line, and `exp2` filters to the three single-mechanism DGPs and never touches
   `DGP_ZERO_SIGNAL`.
4. `METHODOLOGY.md` §3 and H4 list `tutor_income_elast` and "learning-per-grade slope" as tie-breakers;
   `exp1` emits neither (it emits `tutor_income_corr`, and `mean_learn` with no grade or cohort dimension).
5. `METHODOLOGY.md` §4 lists seven ABC targets including `cl_work_only`, `cl_study_work`, `cl_agri`, `prm_cmp`,
   `sec_enr`; `exp3` defines four indicators and uses exactly **two** (`prm_enr`, `cl_total`).

A reader should treat `METHODOLOGY.md` and `PRE_REGISTRATION.md` as a design sketch, not as a description of the
code.

---

## 2. The model, reconstructed

All four states are chosen by a single multinomial comparison of utilities; `U(0)` school-only, `U(1)`
study-and-work, `U(2)` visible work only, `U(3)` hidden work (`exp1_unified_gpu_abm.py:72-82`):

```
U0 =  w_t·q_eff·a − (f + h)            − w_p·ψ − w_v·gap + ε0
U1 =  w_t·0.72·q_eff·a − (f + h) + 0.55·w_c − 0.45·w_p·ψ − 0.30·w_v·gap − ban + ε1
U2 =  w_c + 0.45·w_v·gap − 0.30·ban + ε2
U3 =  0.85·w_c + 0.70·w_v·gap + [ban>0 ? +0.40 : −0.45]                (no ε term)
```

where `gap = max(0, y_sub − y_hh)`, `y_hh = base_y · adult_shock`, `y_sub = 0.90·0.985^t`,
`q_eff = max(0.10, q_pub·(1−β_div))`, `q_pub` is initialised at 0.65 and updated as
`clip(0.65 − (1−cap_scale)·max(0, GER−0.55)·0.45, 0.30, 0.80)`, and `ε ∈ [−0.225, +0.225]`.

Tutoring is a binary take-up: if the child is in state 0 or 1 and `y_hh − (f+h) > 0.32`, take tutoring when
`w_t·(1−q_eff)·a + 0.5·β_div − 0.32 > 0.05`. Learning is
`learn = (state 0 ? q_eff : state 1 ? 0.70·q_eff : 0.05)·a + 0.28·tutor`. Work hours are deterministic
functions of `gap` plus one uniform draw: state 1 → `10 + 12·min(1, gap+0.2u)`, state 2 → `28+10u`,
state 3 → `36+12u`.

**What this arithmetic implies (computed by inspection, no run):**

- `w_v = 2.2` multiplies `gap` terms with coefficients of 0.30–1.0, giving utility differences of order 0.5–1.0
  across the income distribution — several times the ±0.225 noise band. `w_t = 2.2` times `q_eff·a` is of order 1.0–1.4, against a
  cost of 0.8. The state is therefore an almost deterministic threshold function of the exogenous income and
  ability draws. The simulated "micro distributions" carry almost no behavioural stochastic structure beyond the
  exogenous `base_y` and `ability` distributions; there are only three independent choice shocks per household
  per year (`ε0..ε2`, each ±0.225) plus the adult shock, and they are small relative to the weight terms.
- The ban term is not a behavioural response but a hard re-ordering. With `w_c = 0.55`, the hidden-work minus
  visible-work difference under a ban is `−0.15·w_c + 0.25·w_v·gap + 0.70`, i.e. **+0.62 at zero gap** — beyond
  the total ε range. The study-and-work utility is simultaneously hit by −1.8. A ban therefore forces the state
  mix toward hidden work by construction. Whatever the model "finds" about backfire, it was written into the two
  constants `+0.40` and `−0.30` and the −1.8 penalty.
- `y_sub` drifts down 1.5 %/yr in **every** world and **every** arm, −30 % over 25 years. That solo drift drives a
  secular decline in work in all cells; `d_cl_total`, the macro quantity exp2 uses, mixes it with the policy shock.
- Pre-shock, all three arms are identical (`f=0.45, h=0.35, ψ=0.45, ban=0, cap_scale` irrelevant). Post-shock,
  **every** arm sets `f_post = 0`: there is no no-reform control arm anywhere in the design.
- The "school push" mechanism is a linear penalty on schooling utilities; it does not model school quality,
  teacher behaviour, distance, or exam failures. The "crowding" mechanism is a `q_pub` feedback rule plus a
  tutoring take-up threshold; there is no teacher, classroom, peer, or provider.

---

## 3. DGP-by-DGP audit

### 3.1 `DGP_POVERTY` — Basu–Van (1998), Baland–Robinson (2000)

**What the citations actually claim.** Basu & Van's subsistence model has child labour as an *income* response:
when adult income falls below subsistence, the household sends the child to work, and the child's earnings enter
household income; this can create multiple equilibria (a "luxury axiom" and a "substitution axiom" generate a
child-labour equilibrium that is privately rational and socially inefficient). Baland & Robinson's extension
adds the fertility–child-labour–credit interaction: child labour and fertility are complements under capital-market
imperfections, and the labour-market externality can make child labour inefficient. *Both* mechanisms require
child earnings to enter the household budget and require the labour-market/credit environment to be a constraint.

**What the code implements.** Household income `y_hh` is exogenous (`base_y × adult_shock`); the child's work
never adds to it. There is no borrowing, no credit constraint, no adult/child wage interaction, no fertility
choice, and no household composition. The "poverty mechanism" is a utility penalty on the *distance* between
exogenous household income and an exogenous subsistence line (`w_v·gap`), plus a small preference term for
visible work. The label `DGP_POVERTY` therefore names a **survival-preference parameter**, not the Basu–Van
subsistence economy.

**Load-bearing parameters that are unjustified.**

| Parameter | Value | Why it matters | Source status |
|---|---|---|---|
| `w_pov` | 2.2 | Sets the entire income gradient of state choice; three to five times the noise band | No citation for the value or functional form |
| `y_sub` level and drift | 0.90 · 0.985^t | Introduces a common −30 %/25-yr trend in the survival gap; contributes to every `d_cl_total` | The −1.5 %/yr drift has no source in the payload |
| Adult shock | 8 % p.a. iid, ×0.55 | Modelled as "HIV/poverty vulnerability" | The cited HIV/AIDS channel (Nordtveit 2010a) is persistent/state-dependent; an iid annual draw is a different object; the 8 %/0.55 values are unsourced |
| Gap coefficients | 0.45 / 0.30 / 0.70 in U0/U1/U3 | Determine which states the poor choose | Unsourced |
| Child wage / work value | 0.55 constant | Standing in for a labour market | No market clearing, no wage response |

**Observables that are construction-implied, not discovered.** `hidden_to_sw_ratio = hidden/(study_and_work)`
is a direct nonlinear transform of the state mix that the four weights determine. `enrolled_work_hrs_p90` is the
90th percentile of a deterministic function of `gap` plus one uniform draw. `tutor_income_corr` is a correlation
between log income and a binary take-up whose only income dependence is the affordability threshold
`y_hh − cost > 0.32`. `mean_learn` is a state indicator times `q_eff·ability`. All four are functions of the same
income/ability draws and the same weight vector. A classifier given them is re-identifying the parameter vector,
not measuring an independent mechanism.

**Verdict.** Not a test of Basu–Van or Baland–Robinson. It is a one-dimensional poverty-preference world. Useful
only as a *stylised vertex* for a methodological demonstration, and even then its income gradient is imposed, not
derived.

### 3.2 `DGP_SCHOOL_PUSH` — Nordtveit (2010a, 2010b)

**Citation check and what can be attributed.** The suite's reference resolves most plausibly to two 2010 works:
Nordtveit (2010a) *Comparative Education Review* 54(2): 223–242, "Schools as agencies of protection in Namibia
and Swaziland: Can they prevent dropout and child labor in the context of HIV/AIDS and poverty?" (DOI
10.1086/651261, verified) and Nordtveit (2010b) *Discourse* 31(5): 699–712, "Discourses of education, protection,
and child labor: case studies of Benin, Namibia and Swaziland" (DOI 10.1080/01596306.2010.516954, verified). The
suite does not give titles, so the a/b pairing is an inference. The 2010b abstract (read) supports three claims
the suite uses: the education-to-work transition is a *smooth continuum* rather than an age-determined binary;
international discourse promotes free compulsory education "without recognizing the direct and indirect costs of
education"; and local survival logic can make child work normal. The 2010a abstract was not retrievable from the
metadata record I used, so any claim that the specific four named states appear there is **UNVERIFIED**. The
four-state taxonomy `school_only / study_and_work / visible_work_only / hidden_work` is the model's own
construction; its first three states map onto the standard survey distinction between children in employment who
are "work only" and those "studying and working" (see §7.2 for the WDI/UCW indicator definitions), but "hidden
work" is a latent conceptual category, not a survey category.

**What the code implements.** A scalar hostility/stigma penalty `ψ` on the two schooling states (0.45 baseline;
0.05 in the `protective_capacity` arm), a hidden direct cost `h_hidden` added to `f_pub` (0.35 baseline),
and a four-state choice. There is no measurement of hidden costs, no school-quality or distance term, no exam
system, no teacher hostility, no household decision-maker, and no distinction between stigma and direct cost:
they enter only as additive constants on schooling utilities.

**Load-bearing parameters that are unjustified.** `w_push = 2.0` (three to five times the noise); `ψ = 0.45`
(a 0.45 utility penalty on schooling, one quarter of the entire ε range); `h_hidden = 0.35` (43 % of the
pre-shock total school cost of 0.80); the coefficients 0.45/1.0 on ψ and 0.55/0.30 on `w_c`/`w_v` in U1. None
of these has a source in the payload; the "hidden costs" literature documents that costs exist and are
substantial, not that they are 43 % of a normalised cost index.

**The state that carries the Nordtveit story is not connected to the Nordtveit variables.** U3 (hidden work)
depends on `ban`, `w_c`, and `w_v·gap` only. It does **not** depend on `h_hidden`, `ψ`, `f_pub`, `q_pub`,
tutoring, or learning. Therefore the suite cannot test the sentence "hidden costs / hostility push children into
hidden work": its own hidden-work state is invariant to hidden costs and hostility. The only channel into hidden
work is the ban penalty. This is the single clearest mismatch between the citation narrative and the code.

**Verdict.** The 4-state *rhetoric* is Nordtveit-adjacent; the *behaviour* is a schooling-penalty parameter.
The 2010a/2010b attribution of a "4-state continuum" is at best PARTLY VERIFIED; the mapping from hidden work to
anything measured is unaddressed.

### 3.3 `DGP_CROWDING_TUTOR` — Bray (2016, 2018), Jayachandran (2014), Dang–Rogers (2008)

**What the citations claim.** Bray et al. (2016, 2018) document fee-charging supplementary tutoring provided by
teachers in Cambodian public schools, the "internal dynamics of privatised public education", and the hidden
curriculum of relationships and values. Jayachandran (2014) formalises and tests the incentive for teachers to
under-teach in class in order to sell after-school tutoring. Dang & Rogers (2008) review the growth of private
tutoring and its implications for human-capital inequality, including household expenditure patterns.

**What the code implements.** A public-quality term `q_pub` that is diluted as enrolment rises when
`cap_scale < 1`; a teacher-effort-diversion parameter `β_div` that lowers `q_eff` for everyone and slightly raises
the tutoring incentive; a household tutoring take-up threshold; and a learning bonus `+0.28` for tutored children.
There is no teacher agent, no provider identity (own teacher vs other teacher vs commercial), no tutoring price
or expenditure, no class size, no peer effects, and no school-resource constraint linking `cap_scale` to spending.

**Why this is not the cited mechanism.** Jayachandran's mechanism is an *incentive* created by a specific
institutional setting: teachers can sell tutoring to their own pupils and have control over what is taught in
class. In the code, `β_div` is an exogenous scalar applied to all agents; no teacher chooses it, and no teacher
receives tutoring revenue. Bray's central empirical phenomenon is *who provides* the tutoring (most pupils buying
from their own teacher); the model cannot represent provider identity at all, so it cannot engage the phenomenon.
The repo already contains a prior ABM of exactly this Cambodian setting whose own README reports that its
"favour" (own-teacher) variant is algebraically the same model as "thin" demand — the largest output difference
between the two was 6.7e-16 — yet a classifier distinguished them 62 % of the time because the two calibrations
settled in different parameter ranges (`research/shadow-education/README.md`, this branch). That is the same
inferential failure mode the GPU suite's exp2 is set up to repeat (§6.2).

**Observables.** `tutoring` is a binary take-up rate, not expenditure or hours. `tutor_income_corr` is a
correlation with a binary take-up driven by an income *threshold*, not the expenditure gradient Dang–Rogers and
Bray & Kwok study (for the gradient precedent, see Bray & Kwok 2003 and Tansel & Bircan 2006, both verified and
listed in §8). There is no tutoring quantity, price, or expenditure variable, so "income elasticity of tutoring"
(H4/METHODOLOGY) is not measured; the emitted field is named `tutor_income_corr`.

**Verdict.** A reduced-form crowding/tutoring demand system, not the Bray/Jayachandran/Dang–Rogers mechanisms.
It cannot speak to provider identity, expenditure inequality, or teacher incentives.

### 3.4 `DGP_MIXED`

A weighted combination of the three vertex parameter vectors (`w_pov=1.4, w_push=1.3, w_tutor=1.6, div=0.12`),
chosen by hand. No cited theory implies these weights. Any result about "the mixed world" is a statement about
convex combinations in this model, not about a real mixed-mechanism economy. It should be labelled an
interpolation check, not a mechanism.

---

## 4. Arm-by-arm audit

Baseline (t < 10) is identical for all arms: `f_pub = 0.45`, `h_hidden = 0.35`, `ψ = 0.45`, `ban = 0`.
At t ≥ 10 every arm sets `f_pub = 0` — **including the nominal "treatment" arms and every other arm; there is no
untreated arm.** The arms are therefore four-way variations on top of a common fee-abolition shock.

| | `tuition_only` | `protective_capacity` | `binary_ban` |
|---|---|---|---|
| fee | 0 | 0 | 0 |
| hidden cost | 0.35 (unchanged) | 0 | 0.35 (unchanged) |
| hostility ψ | 0.45 (unchanged) | 0.05 | 0.45 (unchanged) |
| ban | 0 | 0 | 1.8 |
| capacity | 0.30 (dilutes) | 1.00 (no dilution; no expansion) | 0.30 (dilutes) |
| faithful to a real policy? | Yes: official-fee abolition only | No single policy | Yes in spirit: a ban with no cost relief |
| confounded by | common fee shock, `y_sub` drift | fee + hidden cost + hostility + capacity in one arm | hard-coded utility ordering |
| identified against? | nothing (no control) | nothing (no control) | nothing (no control) |

Two further points. (i) `protective_capacity` is not "capacity": `q_pub` is capped at its baseline 0.65, and
`cap_scale = 1` only removes the dilution term. The arm's effect on child work and tutoring comes chiefly from
`h_hidden → 0` and `ψ → 0.05`, i.e. from making school cheap and welcoming, not from capacity. (ii) The ban arm
applies a −1.8 penalty only to state 1 (study-and-work) and changes U3 by +0.85 relative to U2; it does not
compel school attendance, does not raise the cost of visible work, and has no enforcement intensity. Its
"backfire" is therefore an assumption, not a simulation result. This matters for the Atlas because the real-world
evidence on bans is contested in a way the model cannot represent: Bharadwaj, Lakdawala & Li (2020, JEEA;
DOI 10.1093/jeea/jvz059, verified) find perverse effects of India's child-labour ban operating through wages and
subsistence — a channel the model has deliberately removed by making income exogenous.

---

## 5. Observables: construction-implied rather than discovered

`exp1` emits 11 fields per household-year (`exp1_unified_gpu_abm.py:177-185`). Their status:

| Field | Definition | Structural dependence | Literature measures it? | Verdict |
|---|---|---|---|---|
| `ger` | mean(state ≤ 1) — share of households with the child enrolled | direct function of the four weights | WDI `SE.PRM.ENRR` is a **gross enrolment ratio** (children, can exceed 100 %), not a household share ≤ 1 | construct mismatch (also makes the pooled exp3 target 101.54 % unreachable exactly) |
| `study_work` | mean(state = 1) | state mix | WDI `SL.TLF.0714.SW.ZS` is a share **of children in employment**, not of all children | denominator mismatch |
| `work_only` | mean(state = 2) | state mix | WDI `SL.TLF.0714.WK.ZS` is a share **of children in employment** | denominator mismatch |
| `hidden_work` | mean(state = 3) | state mix + ban | Not a survey category; the concept is precisely the work surveys under-count | cannot be calibrated to a measured series (§7) |
| `cl_total` | `study_work + work_only + hidden_work` = mean(state ≥ 1) | state mix | WDI `SL.TLF.0714.ZS` is "children in employment", explicitly *not* child labour | mislabelled as child labour in the payload |
| `tutoring` | binary take-up, threshold rule | `w_t`, `β`, `q_pub`, income threshold | Surveys measure participation and expenditure; the model has no expenditure | usable as take-up only |
| `enrolled_work_hrs_p90` | 90th pct of a deterministic hours function among state ≤ 1 | `gap`, one uniform draw | Hours are measured (ILO 2008 resolution; ILO 2017 report) | a transform of the income and state mix |
| `hidden_to_sw_ratio` | `hidden / max(study_work, 1e-4)` | direct transform of the state mix | No such ratio in the literature | construction-implied; unstable (divides by ~0 in the crowding world) |
| `tutor_income_corr` | corr(log y_hh, tutoring) among enrolled | threshold take-up | The literature estimates expenditure/hours gradients (Bray & Kwok 2003; Tansel & Bircan 2006) | not the gradient the literature measures; no expenditure variable |
| `mean_learn` | state-indicator × `q_eff·ability` + 0.28·tutor | state mix + ability | Learning is measured by grade-based assessments (ASER/Uwezo; MICS6 FLS; Kaffenberger & Pritchett 2020) | no grade, no cohort, no learning profile |
| `q_pub` | policy-feedback scalar | arm + enrolment | — | not an observable; a policy state variable |

**Pre-registration/observable mismatch.** H4 promises `tutor_income_elast` and `METHODOLOGY.md` promises
"learning-per-grade slope"; the code contains neither string and no grade dimension exists. The pre-registration
was therefore written against an output schema that the model does not produce, which is a pre-registration
defect independent of any run.

**"Non-transform" test.** A useful operational criterion for the next stage (and the basis of Job B's
admissibility rule): an observable should not be predictable, within the calibrated parameter set, from the
three DGP weights plus the macro moments with R² near 1. All four H4 features fail that test by construction.

---

## 6. The three inferential objects that are not implemented

### 6.1 The macro wall (H1)

The Atlas's wall is an *observational-equivalence* claim about real panels: E1 finds 5/272 links travel across
all groupings (`origin/research/e1-multiverse-1200-2026-11-25` @ `7e6f7b5`); Q3 shows "robust everywhere"
mislabels 87 % of minority-effect worlds (`origin/research/q3-multiverse-calibration-2026-11-25` @ `db7814d`);
Q1 shows MSE (97 %) and BIC (100 %) fail a zero-signal control (`origin/research/q1-mechanisms-2026-11-25` @
`9b0cabe`). The suite would test the *synthetic analogue*: do different micro mechanisms generate the same macro
moments?

`exp2` does not do that. It computes a pre/post mean vector per (dgp, arm, seed) and asks whether a logistic
regression can name the DGP from `d_ger` and `d_cl_total`. Three problems:

1. **No equivalence test.** Different DGP weight vectors produce different macro moments by construction; a
   classifier failing to separate them (or succeeding) says nothing about whether one mechanism *could* produce
   the other's moments. The correct design is moment matching / indirect inference: for each candidate mechanism,
   search its nuisance parameters to match a common macro vector, then ask whether the matched sets are
   distinguishable at the micro level. No such search exists in the payload.
2. **No country, no panel, no FE.** There is one synthetic population per seed-arm, so "country+decade FE
   regressions" cannot be run. The macro object in exp2 is a single time series' pre/post difference. The
   suite's synthetic "macro panel" is a metaphor.
3. **No overlap statistic.** H1's ">75 % cross-DGP macro slope overlap" is undefined in the code.

A conditional "wall" demonstration is still possible: *if* one calibrates each world to the same macro moments
and *then* shows that micro observables separate them, that is a meaningful (model-conditional) statement. It is
not what exp1/exp2 do.

### 6.2 The Q1 zero-signal control (H4)

Q1's control works because its three worlds share an effect-content parameter (strength) that can be set to zero
while keeping the mechanism labels: at strength 0 the worlds become distributionally equivalent, so a valid
discriminator must be at chance (~33 %), and both MSE and BIC failed that test. The suite's design has no such
separation: the mechanism label **is** the parameter vector (`DGP_POVERTY` = a particular `w_pov/w_push/w_tutor`
tuple). There is no `strength` argument, and `DGP_ZERO_SIGNAL` is a separate, degenerate world (all weights zero)
that `exp1` can generate but `exp2` never uses. Running exp2 as written cannot produce a zero-signal accuracy;
running it on `DGP_ZERO_SIGNAL` would classify a fourth label, not test the three at zero content.

Consequences:

- H4's ">80 % out-of-seed accuracy, dropping to ~33 % at strength = 0" is **not executable**. It needs a
  redesign in which each world is `θ0 + s·Δ_w` with a common baseline `θ0` at `s = 0`.
- Even with such a redesign, exp2's out-of-seed CV is only across seeds of the same parameter vectors. That tests
  Monte-Carlo variability, not identification; a flexible classifier will separate vertices at near-100 % because
  the vertices are far apart by construction. This is precisely the trap documented in the repo's own shadow-
  education recovery study (62 % on an algebraically identical pair). The honest test needs held-out **parameter
  regions** and **mixture** worlds, not just held-out seeds.
- Because the H4 features are transforms of the same state mix, the classifier's success is guaranteed by the
  builder's choice of separated vertices. That is a tautology, not evidence about the world.

### 6.3 The exp3 identifiability gate

`exp3` draws four parameters from uniform priors (`w_pov`, `w_push`, `w_tutor` ∈ [0,3]; `div ∈ [0,0.35]`), runs
**one** kernel step with fixed `f=0.20, h=0.30, ψ=0.40, ban=0, q_pub=0.60, w_child=0.55, y_sub=0.85,
shadow_cost=0.32`, and accepts the top 10 % by Euclidean distance in **two** moments (`ger`, `cl_total`). Four
parameters, two moments: the acceptance region is a two-dimensional sheet in a four-dimensional prior, so the
marginal credible widths are generically wide and the 0.80 gate is expected to declare most or all parameters
UNIDENTIFIED. That is the correct outcome, but it should be pre-registered as the expectation, not presented as
a calibration.

Further defects: (i) the fixed nuisance parameters are arbitrary, not country/year-specific, and are not reported
as fixed; the "posterior" is conditional on them. (ii) The distance is computed from a single kernel step, so the
model's time dynamics (the whole point of `T=25`, fee shock at t=10) are unused. (iii) Candidate draws use
different RNG streams (`year = d`, `seed1 = d+1`), so the distance includes Monte-Carlo noise; no common random
numbers. (iv) There is no prior predictive check, no posterior predictive check, and the 0.80 "prior-width" rule
is not a posterior credible interval. (v) `tgt_enr = mean(SE.PRM.ENRR)/100 = 1.0154` exceeds the model's
maximum of 1.0, so the model can never match on that moment — a leaked construct mismatch inside the distance.

### 6.4 The exp4 TWFE check

`exp4` runs `val ~ post + C(iso3) + C(year)` with country-clustered SEs for staggered fee-abolition dates. This is
the specification that the modern staggered-DiD literature shows is biased under heterogeneous effects
(Goodman-Bacon 2021, DOI 10.1016/j.jeconom.2021.03.014; Callaway & Sant'Anna 2021,
DOI 10.1016/j.jeconom.2020.12.001; Sun & Abraham 2021, DOI 10.1016/j.jeconom.2020.09.006 — all verified). The
E8 record on `origin/research/e6e8-sequencing-2026-11-25` already used Callaway–Sant'Anna with event-time leads
and a bootstrap; exp4 regresses from that standard, with no event study and no pre-trend check. It also sets
`post = 1` for *every* year ≥ date in treated countries while using all other SSA countries (including
later/contaminated reformers) as controls, and names the coefficient `att` — causal language that HANDOFF rule 5
forbids absent checked pre-trends. And it cannot run: its first call uses
`https://api.worldbank.org/v2/country/region/SSF?format=json&per_page=100`, which on 2026-11-24 returns
`[{"message":[{"id":"120","key":"Invalid value",…}]}]`; the code then indexes `[1]` and raises `IndexError`
before any regression. The correct endpoint is `/v2/region/SSF/country`.

---

## 7. Data-tier and construct audit of the exp3/exp4 inputs

### 7.1 What the indicators are (World Bank API metadata, pulled 2026-11-24)

| Code | WDI name | Source note (quoted) |
|---|---|---|
| `SL.TLF.0714.ZS` | Children in employment, total (% of children ages 7–14) | "children involved in economic activity for at least one hour in the reference week of the survey"; source organisation: **Understanding Children's Work (UCW), ILO, UNICEF, World Bank** |
| `SL.TLF.0714.WK.ZS` | Children in employment, work only (% **of children in employment**, ages 7–14) | "Work only refers to children involved in economic activity and not attending school" |
| `SL.TLF.0714.SW.ZS` | Children in employment, study and work (% **of children in employment**, ages 7–14) | "Study and work refer to children attending school in combination with economic activity" |
| `SE.PRM.ENRR` | School enrolment, primary (% gross) | gross ratio: total enrolment / official-age population, can exceed 100 % |

Three construct errors follow. **(a)** The suite calls `SL.TLF.0714.ZS` "child labour"; WDI's name is "children in
employment", a broader concept that includes permissible light work, and ILO/UCW's child-labour concept is a
further subset. **(b)** `WK.ZS` and `SW.ZS` are shares of *children in employment*; the model's `work_only` and
`study_work` are shares of *all children*. (Checked against the data: for ETH, 52.26 + 47.74 = 100.00; for UGA,
7.18 + 92.82 = 100.00; the two indicators are complements among employed children.) Mapping model shares of all
children onto them would be wrong; exp3 avoids that only by not using them at all. **(c)** Gross enrolment is a
ratio over 100; the model's `ger` is a share ≤ 1. The pooled exp3 target is 101.54 %, unreachable.

### 7.2 Coverage (World Bank API, 1990–2023, pulled 2026-11-24)

`SL.TLF.0714.ZS` in sub-Saharan Africa: **105 non-missing country-year observations across 40 of 48 countries**
for the whole 1990–2023 window. The E8 treated countries are exactly the sparse ones:

| E8 country (fee date) | Non-missing years of `SL.TLF.0714.ZS` 1990–2023 |
|---|---|
| MWI (1994) | 5: 2004, 2006, 2011, 2014, 2015 |
| ETH (1995) | 2: 2005, 2011 |
| UGA (1997) | 2: 2006, 2012 |
| LSO (2000) | 2: 2000, 2002 |
| TZA (2001) | 4: 2001, 2006, 2011, 2014 |
| KEN (2003) | 3: 1999, 2000, 2009 |
| MOZ (2004) | 2: 1996, 2008 |
| GHA (2005) | 3: 2003, 2006, 2012 |

The 14 exp3 comparison countries have 1–5 observations each (`NAM` has one, 1999). Pooling 1990–2023 per country
and then across countries gives `prm_enr ≈ 101.54 %`, `cl_total ≈ 27.05 %` — a two-number summary of a very
sparse, very heterogeneous panel (country means range roughly 11–49 % for `cl_total`). Whatever ABC does with
those two numbers, it is not calibrating a dynamic model to a panel, and the date structure that exp4 needs does
not exist in the series. **Data tier:** observed, harmonised household-survey observations (UCW), not annual
administrative or modelled series; sparse and irregular in time. The suite nowhere labels this tier.

### 7.3 "Hidden work" cannot be calibrated to a measured series

`hidden_work` is by construction the part of child work that surveys do not capture (Nordtveit's latent
category; ILO/UCW measurement practice counts economic activity, and MICS-style questionnaires collect household
chores in a separate module — module existence PARTLY VERIFIED in §8). `exp3`
and `exp4` calibrate/estimate on `SL.TLF.0714.ZS`, which measures *reported* economic activity. The latent state
is therefore being fitted to a series from which it is definitionally absent; the fitted `hidden_work` share has
no measurement counterpart. Any "calibration" of `w_push`/ban effects through that channel is uninterpretable.

### 7.4 Consequences for the empirical claims

- `exp3` cannot identify four parameters from two moments, cannot use the model's dynamics, and is conditional on
  arbitrary fixed nuisance parameters. It should be reported as a synthetic exercise, never as calibration to data.
- `exp4` cannot be run as committed and, even fixed, has 105 observations at most, 2–5 per treated country, no
  pre-trends, and the known staggered-TWFE bias. It cannot support a fee-abolition claim; the E8 record's own
  Callaway–Sant'Anna estimate on the *observed* GER series is the stronger object, and even that record says only
  "consistent with".

---

## 8. Citation verification

Status key: **VERIFIED** = bibliographic record confirmed (DOI resolves / publisher or Crossref/OpenAlex record
matches). **PARTLY VERIFIED** = exists, but a detail or the attributed content is not confirmed. **UNVERIFIED** =
could not confirm. **MIS-CITED** = the suite's use does not match the source's claim. Verified 2026-11-24 via
Crossref/OpenAlex metadata, DOI landing records, publisher pages, and the primary PDFs named below. I did not
read full texts; content claims rest on abstracts/records.

| # | Citation as used by the suite | DOI / locator | Status | Note |
|---|---|---|---|---|
| 1 | Basu & Van (1998), *AER* 88(3): 412–427 | no DOI found in the Crossref/OpenAlex searches run here; RePEc/IDEAS record | **VERIFIED** (bibliographic); DOI **not confirmed** | Semantic use as the subsistence/child-labour mechanism: **MIS-CITED** — the model has no child earnings in household income and no child-labour market |
| 2 | Baland & Robinson (2000), *JPE* 108(4): 663–679 | 10.1086/316097 | **VERIFIED** | Fertility–child-labour–credit mechanism absent from the code: **MIS-CITED** |
| 3 | Nordtveit (2010a), *Comparative Education Review* 54(2): 223–242 | 10.1086/651261 | **VERIFIED** | Title includes "…and Poverty?"; abstract not retrieved, so the 4-state attribution is **UNVERIFIED** |
| 4 | Nordtveit (2010b), *Discourse* 31(5): 699–712 | 10.1080/01596306.2010.516954 | **VERIFIED** | Abstract supports smooth education–work transition and "direct and indirect costs of education"; does not name four states |
| 5 | Nordtveit (2016), *Schools as Protection?* Springer | 10.1007/978-3-319-25651-1 | **VERIFIED**; ISBN **UNVERIFIED** | Book record matches; ISBN not independently checked here |
| 6 | Bray, Kobakhidze, Liu & Zhang (2016), *IJED* 49: 291–299 | 10.1016/j.ijedudev.2016.04.003 | **VERIFIED** | Source of the Cambodian fee-charging teacher-tutoring evidence |
| 7 | Bray, Kobakhidze, Zhang & Liu (2018), *J. Curriculum Studies* 50(4): 435–455 | 10.1080/00220272.2018.1461932 | **VERIFIED** | |
| 8 | Jayachandran (2014), *J. Development Economics* 108: 190–205 | 10.1016/j.jdeveco.2014.02.008 | **VERIFIED** | DOI differs from a common guess (2013.12.005); the verified DOI is the one above. Used for teacher-diversion: apt citation, **but the model has no teacher incentive** |
| 9 | Dang & Rogers (2008), *World Bank Research Observer* 23(2): 161–200 | 10.1093/wbro/lkn004 | **VERIFIED** | |
| 10 | Pritchett (2013), *The Rebirth of Education: Schooling Ain't Learning* (CGD) | no DOI; OpenAlex bibliographic record | **PARTLY VERIFIED** | Title/author/year confirmed; ISBN and page count **UNVERIFIED**. The suite's "flat cohort learning profile α(g)" is **not implemented** (no grade/cohort) |
| 11 | Pritchett & Beatty (2012), *The Negative Consequences of Overambitious Curricula* | SSRN 10.2139/ssrn.2102726 (2012 version) | **PARTLY VERIFIED** | SSRN record confirmed; CGD working-paper number **UNVERIFIED** |
| 12 | Bray & Kwok (2003), *Economics of Education Review* 22(6): 611–620 | 10.1016/S0272-7757(03)00032-3 | **VERIFIED** | Note correct DOI prefix `S0272-7757(03)00032-3` |
| 13 | Tansel & Bircan (2006), *Economics of Education Review* 25(3): 303–313 | 10.1016/j.econedurev.2005.02.003 | **VERIFIED** | Online 2005, volume 2006; cite 2006 |
| 14 | Kaffenberger & Pritchett (2020), *IJED* 79: 102272 | 10.1016/j.ijedudev.2020.102272 | **VERIFIED** | Learning-profile precedent |
| 15 | ILO (2008), Resolution II concerning statistics of child labour, 18th ICLS | `wcms_112458.pdf`; landing page `/resource/resolution-concerning-statistics-child-labour` | **VERIFIED** | "…use a cut-off point of 14 hours during the reference week, below which work can be considered permissible light work" (quoted from the PDF) |
| 16 | ILO (2017), *Global Estimates of Child Labour: Results and Trends, 2012–2016* | `wcms_575499.pdf`; landing page | **VERIFIED** | Contains hours brackets "27–42" and "43 or more" and a section "Child labour and education" |
| 17 | World Bank WDI indicators `SL.TLF.0714.*`, `SE.PRM.ENRR` | World Bank API metadata, 2026-11-24 | **VERIFIED** | Names and source notes quoted in §7.1 |
| 18 | UCW (Understanding Children's Work) | WDI source organisation field | **PARTLY VERIFIED** | Existence confirmed as the source organisation; `ucw-project.org` unreachable from this sandbox (connection failure), so the programme page is **UNVERIFIED** |
| 19 | DHS-8 Model Woman's Questionnaire | dhsprogram.com PDF `DHS8_Womans_QRE_EN_14Feb2023_DHSQ8.pdf` | **VERIFIED** | Items quoted in §7/Job B: "Have you ever attended school?"; "What is the highest level…"; "What is the highest [GRADE/FORM/YEAR] you completed…" |
| 20 | UNICEF MICS6 Foundational Learning Skills | UNICEF/UNStats side-event, 4 Mar 2020 (`Children-Left-Behind-in-Learning.pdf`) | **PARTLY VERIFIED** | Module existence and purpose confirmed; MICS tools page returned HTTP 403 and exact item wording is **UNVERIFIED** |
| 21 | UN (2004/2005), *Guide to Producing Statistics on Time Use: Measuring Paid and Unpaid Work* | ST/ESA/STAT/SER.F/93, Sales No. E.04.XVII.7, ISBN 92-1-161471-6 | **VERIFIED** (series/sales/ISBN from the PDF); title string **PARTLY VERIFIED** (title page is image-only) | Imprint year: PDF says © 2004; the conventional citation is 2005 — say "2004/2005" until confirmed |
| 22 | World Bank (2018), *World Development Report 2018: Learning to Realize Education's Promise* | worldbank.org/en/publication/wdr2018 | **VERIFIED** | |
| 23 | ASER Centre / Uwezo learning assessments | asercentre.org (HTTP 200); twaweza.org (HTTP 200) | **VERIFIED** domains; specific report **UNVERIFIED** | Uwezo's own site unreachable |
| 24 | Goodman-Bacon (2021) | 10.1016/j.jeconom.2021.03.014 | **VERIFIED** | *J. Econometrics* 225(2): 254–277 |
| 25 | Callaway & Sant'Anna (2021) | 10.1016/j.jeconom.2020.12.001 | **VERIFIED** | *J. Econometrics* 225(2): 200–230 |
| 26 | Sun & Abraham (2021) | 10.1016/j.jeconom.2020.09.006 | **VERIFIED** | *J. Econometrics* 225(2): 175–199 |
| 27 | Bharadwaj, Lakdawala & Li (2020) | 10.1093/jeea/jvz059 | **VERIFIED** | *JEEA* 18(3): 1158–1195 |

**Reference list used in this audit but not in the suite.** Bray & Kwok (2003), Tansel & Bircan (2006),
Kaffenberger & Pritchett (2020), ILO (2008, 2017), DHS-8, MICS6 FLS, UN time-use guide, WDR 2018, ASER/Uwezo,
Goodman-Bacon/Callaway–Sant'Anna/Sun–Abraham, Bharadwaj et al. These are the sources Job B uses for measurement
precedent; they are cited here so that the two records share one verification log.

---

## 9. Claims that must be withdrawn before publication

If any suite output is ever written up, these statements must not appear in the form below. The safer
formulation is given so the record can be repaired rather than abandoned.

1. **"The macro wall is demonstrated / four DGPs collapse to identical macro slopes."** → Withdraw. No
   equivalence test, no moment matching, no macro panel, no country dimension. Safer: "In a stylised model with
   builder-chosen parameter vectors, macro summaries are not mechanically informative about which weight vector
   generated them; testing the real wall requires the moment-matching design in §6.1."
2. **"Binary bans backfire (Nordtveit)."** → Withdraw as a result. The backfire is the arithmetic of
   `−1.8` to U1 and `+0.40`/`−0.30` to U3/U2 against ±0.225 noise. Safer: "We implemented a ban as a utility
   penalty; by construction it reallocates the state mix toward hidden work. This is an assumption of the
   parameterisation, not a finding about bans."
3. **"Protective capacity reduces child labour while fee abolition alone does not."** → Withdraw. The arm bundles
   fee abolition, hidden-cost removal, de-stigmatisation and capacity-no-dilution; there is no no-reform control.
   Safer: "A bundled school-cost-and-hostility reduction changes the state mix relative to a fees-only arm; the
   bundle cannot be decomposed."
4. **"A micro tie-breaker passes the Q1 zero-signal control."** → Withdraw. The control is not implemented and is
   not implementable in the current parameterisation. Safer: "The current design cannot run the Q1 control; a
   strength-separable redesign is required (see Job B preregistration)."
5. **"Rejection-ABC calibrates the model to public data / identifies the mechanism weights."** → Withdraw. Four
   parameters, two moments, arbitrary fixed nuisance parameters, one kernel step, sparse survey targets. Safer:
   "A synthetic exercise illustrates why this ABC design cannot identify the weights."
6. **"Fee abolition reduces child employment."** → Withdraw. Script fails; staggered TWFE with sparse outcome and
   no pre-trends; even the stronger E8 CS design reports "consistent with" for GER only.
7. **"Learning-per-grade slope / flat Pritchett profile tested."** → Withdraw. No grade, cohort, or learning
   profile exists in the model.
8. **"The 3/4-DGP structure maps to Basu–Van, Baland–Robinson, Nordtveit, Bray, Jayachandran, Dang–Rogers,
   Pritchett."** → Withdraw as a mapping claim. Safer: "The model's parameters are *inspired by* these
   literatures; it implements reduced-form utility weights and does not reproduce the cited mechanisms."
9. **"Hidden work is measured."** → Withdraw. It is a latent category surveys under-count; it must be labelled
   unobserved and its fitted values reported as model-imputed.
10. **"The mixed DGP is a mixed-mechanism world."** → Withdraw. It is a convex combination chosen by hand.

---

## 10. What the suite can honestly establish

1. **A methodological template**: a transparent, reproducible way to translate cited mechanisms into explicit
   reduced-form utility rules, with pinned batch size and a fixed Philox stream. That is a modest methods
   contribution, and it is real.
2. **A conditional possibility result**: for a *stated* parameterisation, distinct weight vectors can produce
   similar macro summaries and different micro summaries. Stated as a logic-of-the-wall demonstration (and only
   after a moment-matching design exists), this is publishable as a simulation note. It is not evidence about any
   real economy.
3. **A negative methodological result**: the suite's own pre-registered tests (H1, H4) cannot be implemented as
   written because the mechanism label is the parameter vector and there is no strength parameter. That is worth
   reporting, alongside the repo's prior shadow-education finding that classifier recovery of explanations can be
   an artefact of parameter ranges.
4. **A design checklist** for v2 (§11). Nothing about schooling, fertility, history, or policy.

---

## 11. Required changes before any output is reported as evidence

**P0 — blocking.**

1. **Strength-separable parameterisation.** Each world `θ_w(s) = θ0 + s·Δ_w` with a common baseline `θ0`; at
   `s = 0` the worlds must be distributionally identical. Only then can the Q1 zero-signal control be run.
2. **No-reform control arm** and an unbundled arm design (fee / hidden cost / hostility / capacity as separate
   factors, ideally 2×2×2×2). Without a control, no arm effect is identified.
3. **Moment-matching / indirect-inference macro test.** For each world, search nuisance parameters to match a
   common macro moment vector; report which parameter sets are macro-equivalent; only then run micro tests.
4. **Replace hard-coded ban constants** with an explicit enforcement/penalty model, or state unambiguously that
   the ban effect is a built-in assumption.
5. **Fix exp4**: correct the region endpoint; use Callaway–Sant'Anna (or an event study with leads) and check
   pre-trends; snapshot and hash the data; label the data tier; use only observed survey years; drop causal
   language.
6. **Fix exp3**: log all fixed nuisance parameters; report the parameter/moment dimension mismatch and expect
   UNIDENTIFIED; add prior/posterior predictive checks; use common random numbers; stop calling it a calibration
   to data.
7. **Add the observables the pre-registration promises** (grade attainment and learning by grade; tutoring
   expenditure/hours) or delete those hypotheses.

**P1 — needed for a credible tie-breaker stage.** Survey measurement layer (sampling, item non-response, hours
heaping, reference-period differences, hidden-work under-reporting); out-of-seed **and** out-of-parameter-region
**and** mixture-world validation; algebraic-equivalence placebo pairs (must be at chance); Holm correction; report
all nulls and failures.

**P2 — provenance/portability.** Hash and log the kernel source, CuPy version, grid layout, interpreter, data
vintages; replace `sha256sum` with a portable hash; make the CPU path work or fail with a clear message.

---

## 12. Provenance

**Post-audit note (24 Nov 2026, added before this record was finalised).** The handoff branch advanced after
this audit began: `origin/research/handoff-2026-11-24` now records that the Apple-Silicon port completed at
`fd933d9` and that a *PORT-PRODUCTION* run (exp1 7,500 rows, exp2, exp3) was executed on that branch and
labelled "not research results" (`HANDOFF.md` §6–7). That run is **not** in the payload audited here, and this
auditor did not open its results; nothing in this record is based on it. Before any output from it is used as
evidence, the v2 fixes in §11 still apply — a production run of the current code inherits every defect above,
including the missing zero-signal control and the construction-implied features.

- Base commit: `51f9f02` (`origin/research/handoff-2026-11-24`).
- Referenced records: Q1 `origin/research/q1-mechanisms-2026-11-25` @ `9b0cabe` (REPORT read); E1
  `origin/research/e1-multiverse-1200-2026-11-25` @ `7e6f7b5` (REPORT head read); Q3
  `origin/research/q3-multiverse-calibration-2026-11-25` @ `db7814d` (REPORT head read); E6/E8
  `origin/research/e6e8-sequencing-2026-11-25` @ `2d19da7` (fee dates and estimator read).
- Suite file hashes: table in §1.
- Public data pull: World Bank API v2, indicators `SL.TLF.0714.ZS`, `SL.TLF.0714.WK.ZS`,
  `SL.TLF.0714.SW.ZS`, `SE.PRM.ENRR`, dates `1990:2023`, region `SSF` country list via
  `/v2/region/SSF/country`, executed 2026-11-24 (UTC). Counts in §7.2 are from that pull.
- Citation checks: Crossref `api.crossref.org/works/<DOI>` and OpenAlex `api.openalex.org/works/<DOI|search=…>`,
  2026-11-24; ILO Resolution II PDF `wcms_112458.pdf`; ILO 2017 PDF `wcms_575499.pdf`; UN time-use guide PDF
  `Seriesf_93e.pdf`; DHS-8 woman's questionnaire PDF; UNICEF/UNStats FLS side-event PDF.
- **Not run:** `exp1`, `exp2`, `exp3`, `exp4`, `run_all.sh`. No simulation output was inspected because none is
  committed.
- What this audit could **not** do: retrieve the 2010a CER abstract (paywall/metadata only); open
  `ucw-project.org` (connection failure); open the MICS tools page (HTTP 403); extract the UN guide's title page
  as text (image-only). These are marked UNVERIFIED in §8 rather than guessed.
