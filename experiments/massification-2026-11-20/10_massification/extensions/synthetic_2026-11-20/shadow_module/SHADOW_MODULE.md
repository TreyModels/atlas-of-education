# SHADOW MODULE — gate-demand design for the SYNTHETIC generator (v1.3)

**LABEL: SYNTHETIC / DESIGN.** This is a design document. It contains no result. Every number it quotes is either
an on-disk observation (cited) or a declared assumption (labelled). Nothing here is evidence about any country, and
nothing here licenses a causal claim.

**Worker W2 · 2026-11-20 · extends `v1_2/PRE_DECLARATIONS.md` · frozen spec in `PRE_DECLARATIONS.md`.**

---

## 1. Plain English

Shadow education was paused because the programme could not identify cross-country incidence, could not price the
provider sector, and could not separate gate architecture from other explanations (`LOOP_CLOSEOUT.md` §2). The
directive that reopens it is narrow: tutoring demand must **show up around the relevant gating**. So this module
does not build a tutoring industry. It builds a **household decision at a gate**.

The idea in one sentence: a household buys tutoring when the gate in front of it is crowded, the credential behind
the gate is worth something, tutoring measurably improves the chance of getting through, and the fee is affordable
relative to the household's income — and **nothing else**. If the gate is not crowded and the credential is not
worth much, the model produces almost no tutoring, which is exactly the behaviour the user's reading of the
Philippines requires and which the closed phase's own evidence supports: the Hong Kong gradient rises
35.1 → 46.6 → 70.3 per cent as pupils approach the terminal gate
(`09_relations/data/shadow_gradients.csv:2-4`), and Philippine money sits at the college-entrance review centre,
not at the primary tutor (`02_lit/SHADOW_TARGETS.csv:18-19`).

The module therefore has one output that matters — **participation at a gate** — and it is only allowed to be
non-zero for reasons that can be pointed at in the generator's own state.

## 2. Why "at the gate" is a different object from "a shadow sector"

| | a shadow-sector add-on (rejected) | gate demand (this module) |
|---|---|---|
| unit | a tutoring market / provider block | a household at a gate |
| driver | an exogenous participation rate | queue length, credential rank, `P(advance)`, expected return, fee vs income |
| link to the generator | none — parallel sector | sits on Layer 2's queue/matching state |
| what makes it rise | a parameter | a tighter gate, a more valuable credential, a bigger tutoring lift |
| failure mode | reproduces a level by assumption | reproduces a level *or fails its own checks* |

The old failure mode is documented: v1's check A passed "by construction" because its load-bearing object was a
stipulated seat cap (`generator_v1/FINDINGS.md` §4). This module is built so that the analogous object — the
participation level — is **not** a parameter. The level is an output of a decision rule; the rule's coefficients are
declared, and the country inputs are drawn from the record with provenance.

## 3. Mechanism

### 3.1 The decision

A household at gate `g` compares the expected gain from buying tutoring with the fee, in log-odds form:

```
Θ = a_g                                   gate intercept (declared)
  + b_Z · ln R                            (i)  gate pressure: how crowded the gate is
  + b_V · ln(1 + V)                       (ii) expected credential return at this gate
  + b_Δ · ln(1 + Δπ)                      (iv) what tutoring actually buys: a lift in P(pass/advance)
  + b_y · ln(y_q / ȳ)                     (iii) household position in the income distribution
  − b_F · ln(1 + s / (y_q / ȳ))           (iii) fee burden relative to that household's income

p = σ(Θ);   D_g = mean over quintiles of p
```

Full frozen form, parameter values and provenance: `PRE_DECLARATIONS.md` §4, `PARAMETERS.csv`.

### 3.2 Why each term is where it is

- **Gate pressure `R`** is the only term that can make demand rise *without* the household's own return changing.
  It is the positional/arms-race component: when the queue at the gate lengthens, a household that would not have
  bought tutoring now buys it defensively. This is Thurow's job-competition logic (workers queue for jobs; wages
  attach to jobs, not to years of schooling) applied to the *schooling* gate rather than the labour-market gate.
  `R` is built from three mechanical quantities — queue per place, `1/π⁰`, and the credential rank factor — with
  declared weights (0.40, 0.40, 0.20). Nothing about `R` is hand-set per country.
- **Credential value `V`** is the exchange value of the credential at the gate, `φ_c · r_EAP · ΔS_g · H`. `φ_c` is
  the observed probability that a credential is rewarded in wage work (one minus the vulnerable-employment share),
  and `r_EAP` is the programme's on-disk Mincer anchor. `V` is deliberately **positional, not human-capital**: it
  measures what the credential is worth *against the queue*, not what schooling does to productivity. The
  human-capital return lives in v1.2's wage block and is not touched here.
- **Tutoring's lift `Δπ = δ_g (1 − π⁰)`** is the mechanism the user named: tutoring raises `P(pass/advance)` (or
  the credential rank), and the *room* for it is largest where the gate is tightest. This is why the model's demand
  rises exactly where the horse race is, and it is also why the module cannot separate "pressure" from "returns":
  a tighter gate mechanically raises `R` **and** `Δπ` **and** lowers `π⁰` at the same time (§7, collinearity).
- **Income and fee burden** are what stop the model predicting 100 per cent participation at every hard gate.
  Tutoring is a cash purchase at a fee that is quasi-fixed within a country, so a poorer household faces a higher
  effective fee share. The Korean record gives the relevant shape — tutoring expenditure rises faster than income
  (elasticity 1.33, `09_relations/data/shadow_gradients.csv:8`) — and the Hong Kong record gives the level the fee
  actually takes out of a household (1.1–5.0 % of monthly household income,
  `04_data/shadow_round2/SHADOW_DATA.md` §6).

### 3.3 What the mechanism predicts qualitatively (declared, before any run)

1. Near-zero tutoring **before the first gate** (primary): no queue, no positional good.
2. Within a system, demand rises as the pupil approaches the terminal gate — the HK 2003 gradient.
3. Across systems, **the same rule produces different cohort incidence mainly through who reaches the gate**, not
   through different demand intensities at the gate. This is the module's substantive design claim and it is
   falsifiable by c4.
4. Where the gate is tight but the credential is nearly worthless (a large informal economy), the two channels
   pull against each other and the net is an empirical question the module answers by arithmetic, not by
   assumption.

## 4. State variables

Read-only from v1.2 (Layer 1 and Layer 2). The shadow block adds **no new generator state** except the demand it
computes.

| variable | source in v1.2 | used for |
|---|---|---|
| `intake_L, grads_L, Cann_L, seat_L, surv_L, comp_L, elig_L, ger_L` | Layer 1 cohort flow | `Q`, `π⁰` at g1–g3 |
| `pool_r, vac_r, hires_r, queue_r, rankf_r` | Layer 2 matching | `Q`, `π⁰`, `κ` at g4; `κ` at g1–g3 |
| `w_for_r, w_inf` | Layer 2 wages | `V_{g4}` (formal-rung gap form) |
| `X, Tstate, Y, lit, sec` | Layer 0 | reporting / decomposition only — **not** an input to demand |
| `D, S, π⁰, π¹, Π, R, V, s, p_q` | **written by this module** | outputs + feedback |

`X`, `Tstate`, `Y`, `lit` and `sec` are deliberately **not** arguments of the demand equation. Country income
enters only through `φ_c` (observed), the fee share `s`, and the income distribution — so the module cannot smuggle
a growth effect into tutoring demand.

## 5. The feedback loop

```
        tutoring purchase D_{g,t}
                 │
                 ▼
   Π_{g,t} = (1−D)·π⁰ + D·π¹          (realised advance rate rises)
                 │
                 ▼
   more completers at the next level (one cohort-duration lag)
                 │
                 ▼
   queue Q_{g+1,t+1} ↑  and rank κ ↑     (via v1.2's own queue_carry)
                 │
                 ▼
   gate pressure R_{g+1,t+1} ↑  →  D_{g+1,t+1} ↑  →  …
```

This is the credential-inflation loop, and it is the reason the module is *positional* rather than additive: the
private purchase is individually rational and collectively self-defeating, because it moves the queue rather than
the number of places. The loop is bounded by construction (`|Π − π⁰| ≤ δ_g`), and it is **not** allowed to change
any v1.2 parameter — it only substitutes the realised advance rate. Check c6 enforces that: with the block off,
v1.3 must reproduce v1.2 byte-for-byte.

## 6. What is borrowed, and what is newly declared

### 6.1 Borrowed from the closed phase's theory (structure, not magnitude)

| element | source | status of the source | what is taken |
|---|---|---|---|
| Workers/households compete for **places**, not for wages; education orders the queue | Thurow (1975), *Generating Inequality* | **UNVERIFIED** in this programme (monograph not fetched; `rows_B_absorption_credential.csv` B21) | the queue-as-ordering idea behind `R` |
| Credentials ratchet upward as supply grows; schooling allocates access to status groups | Collins (1979), *The Credential Society* | **UNVERIFIED** (B18) | the feedback loop of §5 |
| Schooling can signal/filter rather than create ability; private return can exceed social | Spence (1973); Arrow (1973) | Spence **VERIFIED-ABSTRACT** (B20); Arrow **UNVERIFIED** (B19) | why a *positional* value `V` is the right object, not a productivity effect |
| Returns to **surplus** schooling are far below returns to **required** schooling — about 45 % | Leuven & Oosterbeek (2011), *Handbook*, ch. 3 | **VERIFIED-FULLTEXT** (B22) | the reason the module discounts `V` by the *queue*, not by years |
| Overeducation is measurement-dependent; cross-country incidence shares are not comparable | McGuinness (2006) | **VERIFIED-ABSTRACT** (B23) | the reason c4 is an *ordering on a declared statistic*, never a cross-country incidence claim |

And from the programme's own full-text **model cards** (`02_lit/MODEL_CARDS.md`) — these are stronger evidence
status than the B17–B25 theory rows and they line up with the gate design:

| element | source | card | what is taken |
|---|---|---|---|
| Tutoring as **rent seeking** with a discontinuous payoff at the gate's line: effort concentrates where `f(αe − t*)` is largest, i.e. **where the gate's cutoff sits among its takers** | Yoo (2003), KDI School, FULL (37 pp.) | `MODEL_CARDS.md:15`, quote at `:43` | the *shape* of the demand equation: a threshold in the payoff, not a smooth add-on — the formal basis for `Δπ` being largest where `π⁰` is lowest |
| Tournament admissions: **77 %** of secondary tutoring expenditure and **89 %** in the final year is attributable to the competition channel, holding direct human-capital returns fixed | Kang (2026), FULL (69 pp.) | `MODEL_CARDS.md:70`, numbers at `:76` | that the *positional* share at the gate can be very large — an order-of-magnitude warrant for `b_Z` dominating `b_V` |
| **Teacher-sold** tutoring: a ban on teacher tutoring raises instructional quantity when school and tutoring are substitutes; offering tutoring makes teachers 5.3 pp less likely to teach the full period | Jayachandran (2014), *J. Dev. Econ.* 108:190–205, FULL | `MODEL_CARDS.md:87`, result at `:101` | the *boundary* of this module: teacher-sold supply is a different mechanism (deliberate withholding), which is why the Cambodian case is out of scope (§7) |

**Do not cite Freeman, Collins, Arrow or Thurow for magnitudes** — the programme's own caution list says so
(`EXTERNAL_LITERATURE_MEMO.md` §6, caution 4). They are cited here for *structure only*. The verifiable magnitude
anchors are the Mincer compilation (Psacharopoulos & Patrinos 2018), the PHL mismatch/premium evidence (PIDS 2025;
World Bank 2026) and Leuven & Oosterbeek (2011).

### 6.2 Borrowed from the programme's own shadow record

| element | where | how it is used |
|---|---|---|
| Gate-proximity gradient, HKG 2003: 35.1 / 46.6 / 70.3 (+35.2 pp S1-3 → S6-7) | `09_relations/data/shadow_gradients.csv:2-5`; `RELATION_CANDIDATES.csv` R21 | the empirical shape `R` must be able to produce; R21's own calibration test (**R×2 ⇒ ≥ +10 pp**, declared) is the basis of c1 |
| Income elasticity of tutoring expenditure ≈ 1.33 | `shadow_gradients.csv:8`; R22 | sign and rough scale of the income term |
| Participation falls with level while spend rises (KOR 86.0 → 66.4; 398 → 491k won) | `shadow_gradients.csv:9-12`; R23 | the warning that a one-margin model is incomplete — this module models the **extensive** margin only (see §7) |
| Returns → tutoring demand: **not identifiable**; in-model coefficient must stay a prior | `RELATION_CANDIDATES.csv` R26 | why `b_V` is a declared prior and c2 is a *comparative static*, not an estimate |
| Price elasticity: not identified; prior −1.1 | `RELATION_CANDIDATES.csv` R29 | why this module uses a fee *burden*, and why it declares no price elasticity |
| Credential gate response: ~9 licensed nurses per migrant | `RELATION_CANDIDATES.csv` R28; Abarcar & Theoharides (2024) | the template for what `g4` is (a credential-conversion gate), **not** a magnitude |
| HKG ~85 % senior-secondary | `04_data/TARGETS_SHADOW.csv:4`; `02_lit/SHADOW_TARGETS.csv:9` | the c4a **band** anchor, with its low/medium confidence caveat |
| PHL 46.5 % all-basic, 23.8 % elementary, 28.1 % review-centre | `02_lit/SHADOW_TARGETS.csv:17-19` | the *gate-clustering* reading (`D*` vs gate-conditional), never a point target |
| KHM 68.4 % grade-9 (two schools), 41.3 % primary | `02_lit/SHADOW_TARGETS.csv:10-11`; `COUNTRY_CARDS/KHM.md:15-16` | the **out-of-scope contrast** that c3 must be honest about |
| **Gate-indexed take-up** in the closed phase's own simulation: 93 % licensure board, 35 % college completion, 30 % elite admission, 5 % basic diploma | `02_lit/CLAIM_REGISTER.csv:41` (O-22, "verified (model output)", `simulated`) | the *precedent*: the closed phase already expressed tutoring take-up **by gate**, not as one aggregate rate. This module keeps that structure and gives it a mechanism |
| **Gate-stakes experiment**: raising the basic-diploma bar alone moves tutoring at that gate from **3 % to 76 %** of takers | `02_lit/CLAIM_REGISTER.csv:42` (O-23, model output, `simulated`) | direct precedent for c1/c2: a change in the gate, not in income, moves demand. Labelled **model output, not evidence** — it licenses the *design*, not a magnitude |

### 6.3 Newly declared (no on-disk anchor — this is where the design work is)

1. The gate-demand equation and its functional form (§3.1).
2. The gate-pressure index `R` and its weights (0.40, 0.40, 0.20).
3. The positional definition of `V` and the horizon `H = 20`.
4. The tutoring-lift function `Δπ = δ_g(1−π⁰)` and the values of `δ_g`.
5. The income distribution (lognormal, per-country dispersion `σ_c`) — **no Gini series exists on disk**.
6. The cohort-incidence statistic `D*` and its exposure weights `ν_{c,g}`.
7. The country types `SYN_*_LIKE` and their fee shares where no fee series exists (PHL).

## 7. Grounding: what is observed, derived, declared — and the conflicts

Labels used throughout: `OBSERVED` (on-disk observation, cited) · `DERIVED` (arithmetic from observed values, shown)
· `DECLARED` (assumption of the synthetic world) · `BORROWED-FROM-SHADOW-RECORD` · `SYNTHETIC` (simulator output).

**Grounded:**
- `φ_c = 1 − vulnerable-employment share, 2019` — HKG 0.940, PHL 0.677, KHM 0.464, from
  `04_data/ECONOMY_SERIES.csv` (WDI/ILO modelled estimates). This is a *proxy* for "probability a credential is
  rewarded in wage work"; the programme's `PARAMETER_MAP.csv` correctly warns that status of employment is **not**
  formality, so `φ` is labelled **OBSERVED SERIES, DECLARED INTERPRETATION**.
- `r_EAP = 0.087` — East Asia & Pacific private Mincer return, `02_lit/ECON_TARGETS.csv:3`, compilation of
  cross-sections, **calibration-only**, explicitly not causal.
- Cohort exposure `ν` — anchored on observed UIS SDG4 out-of-school rates at the upper-secondary age (2020):
  HKG 5.4 %, PHL 24.7 %, KHM 57.0 %, from `10_massification/data/UNIVERSALIZATION_SERIES.csv`. The split of
  in-school youth across gates is **DECLARED**, constrained to sum to `1 − oos`.
- Fees — HKG 1.1–5.0 % of monthly household income (`SHADOW_DATA.md` §6) → declared midpoint 3.05 %; KHM
  500–1,000 Riel/session → declared 16 sessions/month and converted to an income share (≈2.1 %) — **DERIVED with a
  declared session count**; PHL **no fee series exists on disk** → 4.0 % **DECLARED**.

**Conflicts and holes I could not ground (flagged, not papered over):**

1. **"KHM low" is not in the on-disk KHM record.** The record says the opposite at the gate: 68.4 % of Grade-9
   students in a two-school case study attend tutoring, "the highest credible lower-secondary rate in the set"
   (`SHADOW_TARGETS.csv:10`; `COUNTRY_CARDS/KHM.md:15`). `TARGETS_SHADOW.csv:11` records the *national* rate as
   **unresolved**. The module therefore makes KHM low **on the cohort-incidence statistic** (because only ~43 % of
   the cohort is in school at the gate age, observed), and can perfectly well predict a **higher gate-conditional**
   rate for KHM than for PHL. This is declared ex ante in `PRE_DECLARATIONS.md` §8 (c4, declared risk) and is a
   design feature, not a rescue: the on-disk KHM case-study number is **out of scope** and is classed `NOT-SCORED`.
2. **"HKG ~85 %" is weak and stage-specific.** Two on-disk rows disagree on year (2010 vs c.2011) and both are
   second-hand; the 2010 survey's own reporters say it "should not be considered statistically robust", and the
   2014 paper that would fix the denominator was paywalled. The figure is a **senior-secondary** rate, not a
   system rate. Hence a ±10 pp band (c4a), not a point target.
3. **PHL and KHM evidence is not commensurable with HKG.** PHL's 46.5 % is *all basic education* (diluted by
   primary); KHM has no national rate at all; HKG's 85 % is *senior secondary*. The programme's own register
   forbids comparing these directly (`SHADOW_DATA.md` §8, rule 2; McGuinness 2006). The ordering is therefore a
   comparison of a **declared common statistic** (`D*`), not of the observed figures.
4. **No Gini / income-share series is on disk.** `04_data/ECONOMY_SERIES.csv` carries vulnerable/wage employment
   and GDP pc, not inequality. The income dispersion `σ_c` is **DECLARED** and enters the sensitivity set.
5. **No country-specific Mincer table.** `02_lit/ECON_LIT.md` §1.2 says the WPS8402 annex contains one but it was
   not extracted, and warns "do not hard-code a country return". The module uses the EAP regional placeholder and
   differentiates countries through `φ_c`, not through `r`.
6. **PHL fee series does not exist on disk** (`SHADOW_DATA.md` §3). The 4.0 % share is DECLARED and is in the
   sensitivity set.
7. **Tutoring effectiveness `δ_g` has no on-disk anchor at all.** No estimate of the effect of tutoring on
   transition probability exists in this package (the closed phase never estimated one; `RELATION_CANDIDATES`
   has no such row). `δ_g` is therefore the module's most exposed declared parameter and is varied one-at-a-time
   in the pre-declared sensitivity.

## 8. What this cannot claim

- **No causal claim.** No causal effect of tutoring on attainment, earnings or welfare; no causal effect of
  returns on demand. Everything is a declared-assumption simulation.
- **No incidence claim.** It cannot claim any country's shadow-education level or trajectory — the programme's
  exclusion 3 stands. c4 is a synthetic reproduction/ordering check, not a validation.
- **No separability of "pressure" from "returns".** In the feedback loop a tighter gate raises `R`, raises `Δπ`
  and lowers `π⁰` simultaneously; the three are collinear by construction. The module reports a **joint**
  contribution and a decomposition that is arithmetic, not identified. R26 already recorded that
  returns→demand is not estimable at this data coverage; nothing here changes that.
- **No provider, fee, hours or rent claim.** Exclusion 6 stands. Fees are declared cost shares; there is no
  provider block, no entry cost, no rent. The Korean fee/rent descriptive block is untouched.
- **Nothing about primary-stage tutoring.** `c3` is a *structural consistency* check (no gate ⇒ no positional
  demand), not an empirical prediction. Observed primary-stage tutoring — PHL 23.8 %, KHM 41.3 % — is real in the
  record and is **not** explained here: the Cambodian case is teacher-sold (`rien kuo`), a
  supply/withholding mechanism this module deliberately does not model.
- **No welfare statement.** "Self-defeating" in §5 is a statement about the model's queue arithmetic, not a
  welfare finding. The module cannot say whether the tutoring is good or bad for anyone.
- **No policy claim, no forecast, no country model.** The three country types are declared parameterisations
  named for the cases they are *informed by*; they are not Hong Kong, the Philippines or Cambodia.

## 9. How it plugs into the generator

See `DRY_RUN_PLAN.md` for the step-by-step plan: the insertion points inside `simulate_country`, the exact state
contract, the data it needs (all on disk), the expected runtime, and what the first dry run will emit. In short:
one function `shadow_block(...)` called after the schooling and matching updates in `simulate_country`, returning
`D, S, Π, π⁰, π¹, R, V, s, p_q`; one substitution (`Π` for `π⁰` in next period's advance rate); and an ablation
flag that must reproduce v1.2 byte-for-byte.

## 10. Files in this module

| file | what it is |
|---|---|
| `PRE_DECLARATIONS.md` | the frozen spec (sha256 in `RUN_MANIFEST.json`) — read this first |
| `SHADOW_MODULE.md` | this design document |
| `PARAMETERS.csv` | every parameter, its value/range, provenance label, file:line, and where it enters |
| `DRY_RUN_PLAN.md` | v1.3 implementation plan and first-dry-run expectations |
| `toy_design_check.py` | the SYNTHETIC/TOY design check (pre-declared §12; **not** a v1.3 run) |
| `toy/TOY_DESIGN_CHECK.md`, `toy/toy_results.csv` | toy output, labelled SYNTHETIC/TOY |
| `RUN_MANIFEST.json` | hashes of this module and of every on-disk input cited; seed |
