# Coupling shadow education into MASSENG v5 R1 (PHL)

**Status: SIMULATION — bounded first-pass coupling prototype. No causal claims. Every tutoring parameter is
declared or transferred from the Cambodian demand-mix check, not estimated for PHL; the only quantity fitted to
PHL data is one intercept fixed to the mean of a small 2010 PHL survey. The engine boundary table in §2 is a result in its own right.**

- Branch: `research/masseng-tutoring-2026-11-25`, additive from `research/codex-masseng-staging-2026-11-24`
  @ `bac3a7c`. Base branch not rewritten.
- Engine: `research/masseng-v6/model/masseng/engine5.py` — **not modified**. New module:
  [tutoring.py](../../masseng-v6/model/masseng/tutoring.py).
- Baseline: committed PHL v5 R1 fit (`outputs/PHL/v5/fit_R1.json`); tutoring OFF is bit-identical to it.
- Record: [PRE_REGISTRATION_COUPLING.md](PRE_REGISTRATION_COUPLING.md), [RUN_REPORT.md](RUN_REPORT.md),
  [results/](results/), [scripts/](scripts/), [ported/](ported/), [logs/](logs/).

This is the massification engine first and a tutoring module second: §1–§2 describe the system and what it can
and cannot carry; tutoring enters only as one switchable module on the household/demand side (§3–§4). The Lead's
scope correction is the organising frame: affordability, state/supply, progression across levels and credential
stocks are foregrounded; shadow education is one corner with the thinnest data.

---

## 1. The system this is attached to (MASSENG v5 R1, PHL)

MASSENG v5 is a deterministic cohort-flow model of the Philippine school system (1940–2024), fitted to PHL
targets. In one paragraph: each birth cohort (WDI births × survival to 5) is split into ten income deciles whose
relative incomes come from the WDI Gini; pupils move through grades 1–12 and four tertiary years in public or
private sectors; each year a fixed share repeats, and the household chooses whether to continue/enter with a
logit in the credential's wage premium (`b_h`), the credential stock of 20–29 year-olds (`b_p`, positional pull),
formal-employment share (`b_r`), decile income (`eta_x`), and an affordability burden
`-kappa·exp(-lam·S_L)·ln(1 + burden)`, where `burden = (c_scale·direct cost + forgone earnings − transfers) / decile income`.
Secondary completers who do not enter tertiary stay in a deferral pool until age 25. Tertiary places are rationed
by a legacy public-capacity rule, and K-12 (Grade 11 from reference year 2017) changes the cycle. Every behaviour
is an expected value; there are **no random draws**, so every run is exactly reproducible.

**State of the system under the committed R1 fit, tutoring OFF** (from [results/tables.md](results/tables.md) §1):

| indicator | 1970 | 1990 | 2010 | 2024 |
|---|---:|---:|---:|---:|
| GER primary | 91.6 | 102.3 | 108.5 | 104.8 |
| GER secondary | 42.3 | 68.8 | 94.1 | 99.1 |
| GER tertiary | 15.2 | 29.1 | 57.9 | 76.2 |
| NER secondary | 38.5 | 61.9 | 68.6 | 89.3 |
| private share, secondary (%) | 4.7 | 8.2 | 17.4 | 33.5 |
| private share, tertiary (%) | 77.8 | 76.5 | 74.7 | 82.3 |
| credential stock, secondary (`S_secondary`) | 0.17 | 0.34 | 0.69 | 0.87 |
| credential stock, tertiary (`S_tertiary`) | 0.10 | 0.21 | 0.40 | 0.49 |
| household education spending (% of household consumption) | 2.07 | 2.79 | 4.73 | 6.52 |

Dropout per cohort entrant over the simulation window is strongly regressive: **0.726 in the poorest decile vs
0.044 in the richest** (all ten deciles in §6.4). The R1 fit is the "full v5" rival, not the best-fitting rival:
its held-out three-GER RMSE is **16.93** against persistence **6.60**, i.e. the committed PHL v5 model *does not
beat a no-change benchmark* on the three GERs (repo `outputs/PHL/v5/report.md`); it is used here because the task
is to couple to the declared PHL R1 baseline, and the coupling must be judged against that known weakness.

## 2. Engine-boundary table — what MASSENG v5 R1 can and cannot carry (KEY RESULT)

| component of the full massification agenda | in MASSENG v5 R1? | where / how | what this coupling does | verdict |
|---|---|---|---|---|
| **Family affordability: school fees, forgone earnings, transfers** | **yes** | `direct` cost schedule × `c_scale`, `forgone` earnings, dated `transfers`, all in `-kappa·ln(1+burden)` over decile income | tutoring outlay added to the same burden behind a switch | wired |
| **Family affordability: borrowing / credit constraint** | **no** | current-income burden only; no asset, credit or debt state | not represented; stated | missing |
| **State/school supply: public–private places, private shares** | partly | two sectors with a nested logit for private choice; public share is an outcome | unchanged; reported by level | wired (as outcome) |
| **State/school supply: funding** | partly | public education spending (% GDP, WDI) enters the household-share indicator only | unchanged | partial |
| **State/school supply: teacher supply / pupil–teacher ratios** | **no as a constraint** | teacher counts are exogenous WDI data; no teacher module, no class size, no PTR ceiling | teacher provision used only as a robustness proxy for school quality | missing as a mechanism |
| **State/school supply: capacity at each level** | partial | legacy tertiary public-capacity rule; optional upper-secondary public seat-share rule; optional annual capacity arrays only in the separate array engine (not the fitted PHL R1 path) | one declared public-SHS seat-share arm (0.529, sourced) | partial, declared |
| **Household demand: progression primary→lower→upper→tertiary** | **yes** | continuation (`pc`) and level-entry (`pe`) logits by decile, private/public nested choice, deferral pool, repetition | declared achievement shift enters `pc` and `pe` | wired |
| **Learning / school quality** | **no learning-production state** ("school quality and learning" is an explicit model omission) | — | school = existing fitted transition margin; tutoring = declared odds increment added to the same index; quality = declared resource proxy | boundary reported, no score equation invented |
| **Selection gates: score bar vs quota** | **no** | entry is probabilistic demand; no score, no income/group quota, no contest | cannot be coupled without an admissions subsystem; not attempted | **not supported** |
| **Selection gates: limited places** | partial | optional tertiary exam pass-rate filter (not configured for PHL); optional public upper-secondary seat share; proportional rationing only | one declared public-SHS seat-share arm | partial, declared |
| **Jobs/credentials: credential → formal employment / pay** | **no labour market** | credentials enter only as *exogenous* wage-premium drivers; no earnings, no formal-job allocation, no credential competition output | credential stocks and completion/dropout flows reported; pay not computed | **not supported** |
| **Rural/urban and migration** | **no** | ten income deciles only; no location; cohort sizes ignore migration | not reportable by rural/urban; listed as missing | **not identifiable** |
| **Macro feedback: education ↔ jobs/formalisation** | **no** | GDP, premia, formal share are exogenous drivers; no feedback from graduates to jobs/wages | unchanged | missing |
| **Shadow education (tutoring demand, providers, spending)** | **no** (explicit omission) | new switchable module `masseng/tutoring.py` | this is the module being tested | added, declared |

Reading: of the four connected pieces in the Codex frame, piece 1 (affordability) is fully wired **except
borrowing**; piece 2 (learning) exists only as a declared odds shift because the engine has no learning state;
piece 3 (gate) exists only as declared public-seat rationing, not bar-vs-quota; piece 4 (credential→pay) is absent.
The honest answer to "couple the full massification system" is therefore: **the engine carries the schooling
accounting and household demand chain; it does not carry learning, labour demand, geography or credit.**

## 3. What was actually wired (the four-piece chain)

### 3.1 Piece 1 — family affordability (wired; borrowing absent)

The engine's existing burden is

```
burden_{L,d,y} = ( c_scale · direct_{L,s} + forgone_L + tutoring_outlay_{L,d,y} − transfers_{d,L} ) / income_d
utility cost  = − kappa · exp(−lam · S_L) · ln(1 + burden)
```

The tutoring module adds `tutoring_outlay_{L,d,y}` (expected outlay per enrolled pupil at level L, in shares of
GDP per capita) to the existing cost term. This is the whole financing channel: there is **no borrowing, saving or
credit** in MASSENG v5, and none was invented. The declared reference fee is **3% of GDP per capita per tutored
pupil-year** with scenario multipliers 0.5 / 1.0 / 2.0; there are **no PHL tutoring-fee data in the repo**, so the
level is a declared exploratory choice, not an estimate.

**Double-counting warning (important).** The fitted `c_scale = 1.10` was calibrated to FIES *total* household
education spending (2003/2006), which already includes whatever shadow-education outlays households reported. If
tutoring outlay is *added* on top of that fitted schedule it is counted twice. The two readings are reported
separately: (a) **learning-only** — `c_scale` is treated as all-in household education cost, the module changes the
system only through the declared achievement shift; (b) **learning + financing** — tutoring outlay is additional
to the fitted schedule. (a) is the headline; (b) is the bounded alternative.

### 3.2 Piece 2 — learning (declared achievement shift only)

MASSENG v5 has no learning production, no test scores and no school-quality state. We did **not** invent a score
equation and did **not** convert the standalone CES learning index into probabilities. Instead:

- **school** = the engine's existing, fitted transition probabilities (`pc` progression, `pe` level entry);
- **purchased tutoring** = a declared shift in the *log-odds* of those same existing transitions, proportional to
  participation:

```
delta_{L,d,y} = ln(odds_multiplier) · participation_{L,d,y}
base_L ← base_L + delta_L            (base_L is the engine's own linear demand index)
```

Consequence, stated plainly: the shift enters **both** the within-level progression probability and the
level-entry probability of the level the pupil is in — those are the engine's existing margins; no new margin is
created. `odds_multiplier = 1.10` is the central value (5% and 20% run as sensitivity; 1.0 = no learning effect).
It is declared, not identified: the repo has no PHL test-score series and no tutoring→progression estimate. Because
the module works with expected mass rather than individuals, averaging over tutored/untutored pupils is a mixture
`(1−p)·σ(x) + p·σ(x+ln m)`; the code uses the first-order approximation `σ(x + p·ln m)`. With `ln m ≤ 0.18` and
`p ≤ 0.9` the approximation error in the index is below ~0.02 logit and is not corrected; it is declared here.

### 3.3 Piece 3 — gates (only the declared public-SHS seat share; no bar/quota)

MASSENG v5 has **no score bar and no income/group quota**. Its only limited-places machinery on the PHL R1 path is
the optional upper-secondary public seat-share rule (a share `f` of upper-secondary entrants faces the
public+private choice; the rest only the private option at private cost). We ran **one declared arm** with
`f = 0.529`, the sourced public share of senior-high enrolment in SY2018-19 (PHL config target: SHS 47.1% private),
labelled **declared supply share, not observed capacity**. The shadow-education literature's score-bar/quota
equations (inventory 81–82) are **not** attached: there is nothing in the engine to attach them to, and building an
admissions subsystem was out of scope. The v6 admissions skeleton on the base branch says itself that it "does not
yet implement v5 behaviour or estimated country parameters", so it is not a substitute.

### 3.4 Piece 4 — credential → jobs/pay (absent; reported as stocks/flows only)

MASSENG v5 has no labour market, no earnings distribution and no formal-job allocation; the wage premium and
formal-share series are *exogenous inputs* to demand. The shadow model's Mincer equation therefore has no engine
state to act on and was not ported. What is reported instead: credential stocks (`S_primary`, `S_secondary`,
`S_tertiary`), GER/NER/private shares by level, dropout rates by decile, and completion flows. Any statement about
pay or job access would be invented.

## 4. The tutoring sub-module (port, not import)

Provenance: copied from `research/records/2026-11-25-shadow-equations/` on branch
`research/shadow-equations-2026-11-25` @ `fdc8da0` into [ported/](ported/) (copies, no cross-branch imports); the
engine-side re-implementation is
[tutoring.py](../../masseng-v6/model/masseng/tutoring.py).

**Ported unchanged (household demand block).** Four-option multinomial logit over none / own-teacher /
other-teacher / commercial (inventory 23, 57–63; budget 70; spending 64–69):

```
u_none = 0
u_k    = b0 + level_tilt[L] + b_income·log(decile income)
         + b_quality·(1 − q_L) − price_k·fee + provider_offset_k
P      = softmax(u_none, u_own, u_other, u_commercial)
participation = 1 − P_none;  provider shares = P_k / participation
outlay per pupil = fee_ref·fee·Σ_k price_k·P_k           (share of GDP per capita per year)
ban on own-teacher tutoring: u_own = −∞ (option removed, not re-priced)
```

**Dropped because the engine cannot carry them (declared, not silently ignored):** individual ability; the
household's own school-quality draw; own-teacher quality; urban/rural (no location dimension in v5).

**Mapped to engine objects:** `log(decile income) = log(GDPpc_y · decile_multiplier_d)` (the constant
`log GDPpc_1990` is absorbed into `b0`); `level_tilt` reuses the standalone's grade-9 and grade-12 intercept bonuses
for lower- and upper-secondary (tertiary uses the grade-12 tilt); `q_L` is a declared level-specific school-quality
**proxy**; the exogenous fee is in the standalone's fee units with the reference fee converting to money.

**Declared parameters** (central arm; the shape parameters are the closest-to-Bray draw from the demand-mix check
in §7.2; the intercept `b0` is re-calibrated for PHL — see below):

| parameter | value | provenance |
|---|---:|---|
| `b_income` | 0.9825 | best Bray draw (Cambodian schools) |
| `b_quality` | 1.8721 | best Bray draw (`b_school_gap`) |
| `own_premium` | 1.8244 | best Bray draw |
| `other_premium` / `cost_other` | 2.5665 / 1.5319 | best Bray draw |
| `cost_commercial` / prices | 1.0 / 1.0, 0.8, 1.5 | `shadow_model.py` defaults |
| `level_tilt` | primary 0; lower-sec −0.3059; upper-sec/tert +1.2203 | best Bray draw's grade-9 / grade-12 bonuses |
| `fee_ref` | 0.03 × GDPpc | **declared** exploratory (no PHL fee data) |
| fee grid | 0.5 / 1.0 / 2.0 × reference | **declared** |
| `odds_multiplier` | 1.10 (1.0/1.05/1.20 sensitivity) | **declared** (no PHL tutoring→progression estimate) |
| `b0` (calibrated) | −2.6999 | solved so mean of primary and lower-secondary participation in **2010** = **0.436** |

**School-quality proxy** (the engine has no quality state): headline `q_L = clip(public spending per pupil
(% GDPpc) / 30, 0, 1)` from WDI `SE.XPD.PRIM/SECO/TERT.PC.ZS` (observed 1997–2009, flat outside); robustness
`q_L = clip((teachers / official-age population − 0.02) / 0.03, 0, 1)` from `SE.PRM.TCHR`/`SE.SEC.TCHR`
(1971–2024). These are **resource proxies**, not learning outcomes; upper secondary reuses the secondary series,
tertiary falls back to secondary in the teacher variant.

**Demand properties** (consistent with the ported equations): participation falls with the fee (61.8% at fee 0.5,
52.3% at fee 1.0, 33.8% at fee 2.0 in 2010); the own-teacher ban removes the option (participation 52.3% → 32.8%,
own share → 0, other share among tutored 93.9%); the provider mix is **invariant to income, level and fee** because
the shared terms cancel in the MNL — that is a property of the ported equations, and it is why the Bray mix is used
only as a mix check, never as a test of PHL income gradients.

**Calibration and its honesty.** Exactly one parameter (`b0`) is fixed to the mean of the only two PHL tutoring
data points in the repo (Grade 6 40.7%, Grade 10 46.5% in 2010; small purposive sample, 1,235 pupils, 23 schools,
not nationally representative). The two grades are then read as a check (§7.3), not reused for validation.

**Switch.** `switches={'tutoring': False}` is the default and returns `super()` unchanged in every override; the
new file adds no code path to `engine5.py`. The identity test is §6.1.

## 5. Experiment design

53 deterministic runs on the AutoDL server, 60 workers, 10.4 s of grid wall time, 0 errors
(the pristine baseline is additionally run in-process; full command in [RUN_REPORT.md](RUN_REPORT.md)):

- **OFF** (tutoring off) and **OFF + declared gate**;
- **main ON grid**: fee 0.5/1.0/2.0 × own-teacher ban off/on × outlay-in-burden off/on × 3 parameter-uncertainty
  draws = 36 runs;
- **learning sensitivity**: odds multiplier 1.0 (=no learning), 1.05, 1.20 at central fee/no ban/financing on,
  3 draws each;
- **quality-proxy robustness**: teacher-provision proxy, central settings, 3 draws;
- **declared gate arm**: public-SHS seat share 0.529, central settings, 3 draws.

**Seeds** are parameter-uncertainty draws (MASSENG v5 has no random draws): the unestimated shape parameters are
multiplied by `U(0.8, 1.2)`, and the calibrated `b0` is re-solved for each draw so the declared 2010 participation
anchor is held. Seed 0 is the unperturbed anchor. This is stated because "3 seeds" would otherwise be misread as
sampling uncertainty.

## 6. Results

### 6.1 Acceptance A1 — switch-off identity: PASS (bit-for-bit)

`TutoringModel5(switches={'tutoring': False})` vs the untouched `Model5`, same fit, same code:

- full run, 1940–2024, 85 years: **318 comparisons, all byte-identical** (2.06 s baseline + 1.41 s off);
- short run, 2000–2024, 25 years: **138 comparisons, all byte-identical**;
- the only difference in `Result.extra` is the added diagnostics key `tutoring` (not a numerical object).

Evidence: [results/switch_off_identity.json](results/switch_off_identity.json). The coupled grid also contains an
OFF arm that reproduces the pristine baseline exactly (`summary.json:switch_off_arm_equals_pristine = true`).

### 6.2 Coupling effects by level (deltas from the untouched baseline, mean over 3 draws)

| arm | Δ GER secondary 2010 | Δ GER tertiary 2010 | Δ S_secondary 2010 | Δ GER secondary 2024 | Δ GER tertiary 2024 | Δ S_secondary 2024 |
|---|---:|---:|---:|---:|---:|---:|
| **learning-only** (headline) | **+0.99** | **+2.32** | **+0.0219** | **+0.22** | **+0.87** | **+0.0096** |
| learning + financing | −4.78 | −9.01 | −0.0938 | −0.82 | −3.67 | −0.0473 |
| financing only (no learning) | −6.42 | −11.54 | −0.1196 | −1.32 | −5.13 | −0.0663 |
| learning-only, fee low (1.5% GDPpc) | +1.28 | +2.97 | +0.0285 | +0.28 | +1.09 | +0.0123 |
| learning-only, fee high (6% GDPpc) | +0.51 | +1.25 | +0.0114 | +0.12 | +0.48 | +0.0051 |
| learning-only, own-teacher ban | +0.45 | +1.10 | +0.0099 | +0.10 | +0.42 | +0.0045 |
| learning ×1.05 / ×1.20 (financing on) | −5.56 / −3.41 | −10.25 / −6.68 | −0.106 / −0.071 | — | — | — |
| teacher-provision quality proxy (financing on) | −6.23 | −11.03 | −0.1181 | −1.08 | −4.54 | −0.0615 |
| declared SHS gate (financing on) | −4.78 | −9.01 | −0.0938 | −2.48 | −8.72 | −0.0874 |
| declared SHS gate alone (tutoring off) | 0.00 | 0.00 | 0.0000 | −1.42 | −5.28 | −0.0384 |

Reading. The **learning-only** channel is small and positive (the declared odds increment is ≤0.10 logit), and it
reduces dropout in every decile (§6.4). The **financing** channel is large and negative — the fitted R1 demand is
very cost-elastic (`kappa = 39.0`), so adding ~1–1.3% of GDPpc per pupil in tutoring outlay per pupil-year moves
progression and entry materially. Whether that is a real effect or an artefact of adding a cost the fitted scale
already contains is **not identified**; that is why the two readings are separated rather than combined into one
headline. The fee lever works through participation (participation 61.8% at low fee, 33.8% at high fee); the
own-teacher ban halves the learning effect because it cuts participation roughly in half. The multiverse shows the
learning multiplier moving the combined arm monotonically from −6.42 (no learning) to −3.41 (×1.20), and the
quality proxy moving it by ~1.5 pp — both declared choices, neither identified.

### 6.3 Where tutoring piles up, who buys it, and who is pushed out

Tutoring demand in the coupled model (central arm; [results/tables.md](results/tables.md) §6):

- **participation by decile, 2010**: 27.0, 38.1, 45.0, 50.5, 55.5, 60.2, 65.0, 70.0, 75.7, 85.5 % (poorest → richest);
  the rich–poor gap is **56.0 pp in 2010**, narrowing to **39.9 pp in 2024** as participation saturates.
- **participation by level, 2010**: primary 46.9%, lower-secondary 40.3%, tertiary 70.1% (upper secondary does not
  exist in PHL before 2017); **2024**: primary 60.3%, lower-secondary 53.4%, **upper-secondary 82.2%**, tertiary
  81.0% — tutoring piles up at the upper-secondary/tertiary gate, which is where the engine's progression margin is.
- **provider mix among tutored pupils**: own teacher **62.9%**, other **34.9%**, commercial **2.3%** (invariant to
  income/level/fee in the ported MNL; with the own-teacher ban: own 0%, other 93.9%, commercial 6.1%).
- **spending**: expected tutoring outlay ≈ 0.45% of GDP in 2010 rising to 0.62% in 2024 in the central arm
  (gold fee 1.0); it is reported separately and *not* added to the FIES-matched household education share in the
  headline arm.

Dropout per entrant change by decile (2010; negative = kept in school):

- **learning-only**: −0.009, −0.014, −0.015, −0.014, −0.014, −0.014, −0.013, −0.011, −0.008, −0.003 —
  proportionally and absolutely largest for the poorest deciles, smallest for the richest (richest already had
  almost no dropout). The declaration is mechanical (participation rises with income, the shift helps everyone), so
  this is *not* evidence that tutoring equalises.
- **learning + financing**: +0.026 to +0.055 in every decile (largest in the middle), because the outlay drag
  dominates the achievement shift; the poor are pushed out most in absolute terms.

The rural/urban dimension cannot be reported: MASSENG v5 has no location state. Stated, not approximated.

### 6.4 Seed spread (declared ±20% parameter-uncertainty draws)

At 2010, across draws 0–2: learning-only Δ GER secondary 0.985, 0.971, 1.000 (sd 0.015); Δ GER tertiary 2.315,
2.313, 2.345 (sd 0.018); participation 0.523–0.525. Learning + financing: Δ GER secondary −4.698, −4.686, −4.953
(sd 0.151); Δ GER tertiary −8.854, −8.972, −9.216 (sd 0.185). The parameter-uncertainty band is small relative to
the variation across *declared structural choices* (fee, ban, financing, learning multiplier, quality proxy) —
i.e. the honest uncertainty here is model uncertainty, not seed noise. Full table in
[results/tables.md](results/tables.md) §3.

## 7. Reality check

### 7.1 PHL held-out fit consistency (retrospective/inspected — **not validation**)

Compare each coupled arm to the same committed PHL held-out rows the repo scorecard uses
([results/tables.md](results/tables.md) §4):

| arm | three-GER RMSE | Δ vs R1 baseline | GER secondary | GER tertiary | edu_share_hh |
|---|---:|---:|---:|---:|---:|
| R1 baseline, tutoring OFF | 16.925 | 0 | 12.843 | 25.009 | 0.873 |
| learning-only | 17.871 | **+0.947 (worse)** | 13.513 | 26.532 | 1.616 |
| learning + financing | 13.361 | **−3.563 (better)** | 10.518 | 19.088 | 1.060 |
| declared SHS gate, tutoring off | 16.274 | −0.651 | 12.411 | 23.941 | 0.873 |
| declared SHS gate + financing | 12.639 | −4.285 | 10.016 | 17.880 | 1.060 |

**Interpretation — this is a fit-consistency check, not support for any mechanism.** The learning-only arm makes
the held-out fit *worse* because it raises attainment while R1 already **over-predicts** tertiary GER massively
(R1 predicts 64.7 and 76.2 for 2013 and 2024 against observed 31.9 and 47.4 — repo report). The financing arm looks
"better" only because suppressing enrolment moves the model toward that observed tertiary shortfall; it is an
in-sample inspection artefact, exactly the kind of result the repo's own protocol warns about, and the household
spending target gets *worse* (Δ +0.19 to +0.74 on the FIES series). The underlying R1 model does not beat
persistence (16.93 vs 6.60), so neither arm can be read as improving the PHL account. **Pass/fail: the coupling
does not fail its own identity or break the model; it does not pass any validation test, and none is claimed.**

### 7.2 Bray six-school patterns — demand-mix check only (not PHL validation)

The ported demand block, run on six Siem Reap schools (three lower-secondary with Grade 9, three high schools with
Grades 9 and 12; 70 pupils per class), against the seven published Bray et al. (2016, 2018) patterns, with the
repo's own tolerances and 50,000 prior draws:

| pattern | target | tolerance | best draw | \|z\| |
|---|---:|---:|---:|---:|
| participation | 0.819 | ±0.03 | 0.806 | 0.42 |
| participation, Grade 9 | 0.747 | ±0.04 | 0.752 | 0.13 |
| participation, Grade 12 | 0.898 | ±0.04 | 0.914 | 0.41 |
| urban–rural gap | 0.026 | ±0.04 | 0.005 | 0.53 |
| own-provider share | 0.577 | ±0.07 | 0.561 | 0.23 |
| other-provider share | 0.409 | ±0.07 | 0.439 | 0.43 |
| teacher-tutor share | 0.540 | ±0.20 | 0.444 | 0.48 |

**Result: 1 of 50,000 prior draws fits all seven patterns within tolerance** (best max \|z\| = 0.531; the
committed standalone 8k-draw best was 1.14 with no full fit). The ported demand form *can* reproduce the Siem Reap
mix, but only in a very thin corner of the prior — a demand-mix consistency statement about Cambodian schools,
**not** evidence about PHL and **not** validation of the coupling. The anchor used for the coupled runs is that
best draw; using it makes this check non-independent, which is why it is labelled a mix check.

### 7.3 PHL tutoring participation — external survey check (not reused for calibration)

The model is calibrated to the *mean* of the two PHL points, so the check is the two grades separately:

| | PHL 2010 survey (De Castro & de Guzman) | coupled model 2010, central arm | difference |
|---|---:|---:|---:|
| Grade 6 (engine: primary) | 40.7% | 46.9% | +6.2 pp |
| Grade 10 (engine: lower-secondary) | 46.5% | 40.3% | −6.2 pp |
| mean | 43.6% | 43.6% (calibrated) | 0 |

**Pass (level), fail (direction).** The mean matches by construction (one parameter); the model gets Grade 6
within 6 pp but reverses the Grade 10 > Grade 6 ordering that the survey reports, because the transferred level
tilt (from Bray's Grade 9 < Grade 12 pattern) puts lower-secondary participation *below* primary. The survey is a
small purposive 2010 sample, not nationally representative. This is reported as a mismatch, not fixed.

### 7.4 What passes, fails, and is not identifiable

**Passes**
- Switch-off identity: bit-for-bit on full and short runs (A1).
- Demand monotonicity in the fee and the own-teacher ban (A2).
- Demand-mix: all seven Bray patterns fit by 1/50,000 prior draws (max \|z\| 0.53) — Cambodian demand-mix only.
- The engine accepts the module without breaking accounting, determinism or any existing indicator definition.

**Fails / does not support**
- PHL held-out fit: learning-only worsens it; financing "improves" it only by suppressing a known over-prediction;
  household-spending fit worsens. Neither is evidence.
- PHL Grade 6/10 participation direction: model reverses the survey's grade ordering.
- Bar-vs-quota gate: cannot be run at all.
- Jobs/pay, rural/urban, borrowing, migration: cannot be run at all.

**Not identifiable with these data/engine**
- the tutoring **fee level and total spending** (no PHL data; the fee grid is declared; with a calibrated intercept
  the overall fee level is absorbed);
- **provider mix in PHL** (no PHL provider data; only Bray's Cambodian shares, transferred);
- the **learning odds multiplier** (no test-score→progression mapping);
- **school quality** (resource proxy only; 1997–2009 for per-pupil spending; no PHL learning-outcome series);
- **rural/urban** anything (no location dimension);
- **who is pushed out at a score gate** (no gate);
- **pay/job outcomes** (no labour market).

## 8. Missing mechanisms (explicit list, no invention)

1. Borrowing / credit constraint (current-income burden only).
2. School-quality and learning-production state (declared proxy + declared odds shift only).
3. Teacher supply, class size, pupil–teacher ratio as a constraint (teacher counts exogenous; used only as a
   quality-proxy robustness).
4. Score-bar admissions, income/group quotas, contest-success selection.
5. Observed public/private capacity at each level (only a declared public-SHS seat share and the legacy tertiary
   capacity rule).
6. Labour market: formal employment, earnings, credential competition, returns as an outcome.
7. Rural/urban location, distance, and internal/rural–urban migration (cohort sizes ignore migration entirely).
8. Macro feedback from education to jobs/formalisation/wages (all exogenous drivers).
9. Tutoring-supplier behaviour: teacher withholding / buy-back, market clearing, supplier entry, tutoring quality
   (fee is exogenous, supply is not modelled).
10. Tutoring spending measurement in PHL (FIES composition does not isolate it; no fee data).

## 9. Reproduction

All numbers are generated by committed scripts from the committed raw results; see
[RUN_REPORT.md](RUN_REPORT.md) for exact commands, environment, wall times and sha256 hashes.
The engine file was not modified (`git diff bac3a7c -- …/engine5.py …/data.py` is empty), so the baseline is the
committed one; the tutoring module is a new file and the switch-off test proves the identity.

## 10. Bottom line

The coupling is buildable and the engine accepts it without changing behaviour when switched off. The tutoring
module runs on the real PHL massification model and produces internally coherent, monotone demand (income gradient,
fee response, ban response, gate pile-up). But the shape of the *system* answer is honest and modest: the engine
carries affordability (minus borrowing) and the progression/credential accounting; it does not carry learning,
selection gates, labour demand, geography or credit. The declared learning channel adds about **+1 pp secondary
GER / +2.3 pp tertiary GER in 2010** with small seed spreads and reduces dropout most in the poorest deciles; if
tutoring outlay is treated as additional to the fitted household cost schedule, the financing drag dominates and
the net is negative. Neither arm validates the PHL account; the Bray patterns are a Cambodian demand-mix check only;
the PHL fit already fails its own persistence benchmark. Everything structural — fee level, provider mix, learning
effect, quality proxy — is declared or transferred, not identified.
