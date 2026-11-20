# EQUATION REGISTER — the massification literature, extracted into executable form

**Deliverable 1 of the synthetic-data task.** Companion to `EQUATION_REGISTER.csv` (43 rows, 12 columns,
all cells populated, no duplicate ids).

**Purpose.** A synthetic-data generator is only as honest as the equations it is built from. This register lists,
once, every equation or relationship in the programme's massification / push-pull literature layer that a simulator
could conceivably be built on, and says for each one: what it claims in plain English, what the functional form is,
which numbers actually exist on disk and where, whether the programme's own code implements it, and — the column that
matters most — **what status it has**. It is a register, not a model. Nothing here was fitted, estimated or re-run
for this file.

**Not claimed.** No new equation is proposed. No coefficient is inferred where the source is silent. Where a number
appears, it is copied from a named file; where no number exists, the cell says so.

---

## 1. How to read a row

| column | what goes in it |
|---|---|
| `equation_id` | family prefix + number (`WS`, `HC`, `LQ`, `SB`, `DEM`, `PP`, `SC`, `SEC`) |
| `model_family` | one of the eight families the task names |
| `plain_english_claim` | the mechanism in one sentence, no jargon |
| `functional_form` | LaTeX-ish or code-like; or `narrative-only` / `NOT FOUND` plus the form that *would* be needed |
| `variables_units` | every symbol with its unit |
| `parameters` | symbol, meaning, and the value **if** the literature or the programme supplies one, with its file |
| `data_needed` | the series a user would have to obtain to estimate or calibrate it |
| `predicts` | which observed quantity it is a claim about |
| `programme_implementation` | `file` + line numbers if implemented; `none` if not |
| `status` | see §2 |
| `citation` | author–year (or "programme design" where the programme invented it) |
| `source_file` | path in this repo + section/line locator |

## 2. Status vocabulary (five tokens, defined before use)

| token | meaning | n |
|---|---|---|
| **`equation-in-literature`** | The source actually states this equation, and this register reproduces its form. Either the primary text was read in this programme (labelled VERIFIED/FULL upstream) or it is a canonical form the literature layer is willing to state. | 10 |
| **`narrative-only`** | The literature states the *mechanism* but no functional form, or the primary text was not retrieved. The cell says what form would be needed; **inventing one and calling it the literature's would be a fabrication.** | 13 |
| **`programme-invented`** | The form exists only because programme code declared it. Not in any cited source. Legitimate as a *declared assumption*; never presentable as literature. | 15 |
| **`programme-estimated`** | No literature form or value existed for our countries, so the programme fitted a generic regression and the register carries its own estimate as the only number available. Must be labelled programme-side, not literature. | 5 |
| **`unreadable`** | Used once in the wider audit (GXL's Vensim appendix). Not needed here: GXL is recorded as `narrative-only` because its *structure* is verified even though the equations are not readable. | 0 |

**The rule this register enforces.** A generator may calibrate `programme-estimated` values to *this* dataset, may
adopt `programme-invented` forms only as declared assumptions with an explicit sensitivity range, and may **never**
present either as "the literature says". `narrative-only` rows cannot be simulated at all until someone chooses a
form — and that choice is a modelling decision that has to be written down and defended, not discovered.

## 3. Coverage

| # | family | rows | in literature | narrative-only | programme-invented | programme-estimated | implemented in code |
|---|---|---|---|---|---|---|---|
| 1 | world-society / neo-institutional | 2 | 0 | **2** | 0 | 0 | no |
| 2 | human capital / demand-led | 4 | 2 | 2 | 0 | 0 | no (returns absent from code) |
| 3 | labour queue / credential | 9 | 4 | 5 | 0 | 0 | no |
| 4 | state-building / capacity-gated supply | 3 | 0 | 1 | 2 | 0 | yes (anchor) |
| 5 | demographic / cohort flow | 4 | 0 | 1 | 2 | 1 | yes (core) |
| 6 | formal push-pull (programme's own) | 10 | 2 | 0 | 8 | 0 | yes (core) |
| 7 | scaling laws | 6 | 3 | 0 | 0 | 3 | yes (estimators) |
| 8 | sectoral / structural | 5 | 0 | 1 | 3 | 1 | yes (core) |
| | **total** | **43** | **10** | **13** | **15** | **5** | |

**Headline.** Of 43 relationships, **10 are equations the literature actually states**, **13 are narrative only**, and
**20 exist only because this programme wrote them down** (15 invented, 5 estimated). The generator's honest ceiling is
therefore the 10 literature equations plus whatever the programme is willing to declare — not 43 equations of
"literature".

---

## 4. The register, by family

Forms are abbreviated here; the full strings (with every unit and clip bound) are in the CSV.

### 4.1 World-society / neo-institutional (WS-01, WS-02) — *2 rows, both narrative-only*

| ID | claim | form | status | key number | code |
|---|---|---|---|---|---|
| WS-01 | expansion driven by global legitimation, partly decoupled from domestic demand | `E_it = a_i + d_t + b1 ln GDPpc + b2 democr + b3 science + b4 WS_ties + e` — **specification and coefficients not retrieved** | narrative-only | none | none |
| WS-02 | states adopt the *form* (law, ministry, target) long before outcomes | two-equation adoption/outcome system; no form given | narrative-only | none | none |

This is the family that would most cheaply explain the programme's motivating anomaly (expansion while returns fall),
and it is the one with **zero usable functional form**. Its only testable trace on disk is a *timing* claim
(adoption clusters after global declarations, not after return shocks), and even that is confounded — SDG 4 (Sept 2015)
postdates RA 10533 (2013).

### 4.2 Human capital / demand-led (HC-01…04) — *2 literature, 2 narrative*

| ID | claim | form | status | key number | code |
|---|---|---|---|---|---|
| HC-01 | one more year of school raises earnings by ~8.8% | `ln Y = α + rS + β1X + β2X² + ε` (Mincer) | **equation-in-literature** | r = **0.088** world, **0.087** EAP, social **0.069** EAP | **none** — no earnings channel exists in `pushpull.py` |
| HC-02 | invest until marginal return = marginal cost incl. foregone wages | optimality condition only | narrative-only | — | none (no fee/cost term; 2016/2018 reforms are 0/1 markers) |
| HC-03 | expansion follows returns with a lag; slows when returns fall | needs `ΔEnrol/Enrol = c + a·Δr_{t−k}` | narrative-only | elasticity **NOT FOUND** | none |
| HC-04 | identical worker earns 3.99× more in the US than in PHL | place premium = Mincer-adjusted PPP wage ratio | **equation-in-literature** | **3.99** (3.71–4.36) | none (E3 predeclared, not run) |

**The most consequential gap in the whole register:** the human-capital story is the one the programme is *about*, and
its central object — a returns→enrolment response — has **no estimable form in the retrieved literature and no data on
disk**. The 8.8% return is a *price*, not a behavioural elasticity. A generator that hard-codes "enrolment responds to
8.8%" is inventing the mechanism (HC-03), not implementing HC-01.

### 4.3 Labour queue / credential / signalling (LQ-01…09) — *4 literature, 5 narrative*

| ID | claim | form | status | key number | code |
|---|---|---|---|---|---|
| LQ-01 | workers queue by training cost; schooling buys position | queue with job-set wage; no closed form | narrative-only | — | none |
| LQ-02 | schooling signals pre-existing ability | separating equilibrium, single-crossing cost condition | narrative-only | — | none |
| LQ-03 | admission line = mean + kσ; effort clusters near it | `S_cut = S̄ + k·σ_S`; `u_i = log(2+S_i−S_cut) − C_i` | **equation-in-literature** | **k ≈ 1.645** (5th pct) | none |
| LQ-04 | tutoring is rent seeking; effort peaks near the bar | `T = αe+ε`; `max_e X·F(αe−t*) − βc(e)`; FOC `X f(αe−t*)α = βc'(e)` | **equation-in-literature** | signs only (no values) | none |
| LQ-05 | two-family game: `W > 2C` ⇒ prisoner's dilemma | `EW = PW + (1−P)·0 − C` | **equation-in-literature** | threshold `W > 2C` | none |
| LQ-06 | MMI: inequality falls only after saturation | transition-probability matrix + odds ratios | narrative-only | — | none |
| LQ-07 | RRA: families defend relative position | expected-utility comparison, RRA coefficient | narrative-only | RRA value not read | none |
| LQ-08 | credential inflation ratchets the requirement | needs `req_t = req_{t−1} + g(supply_t − demand_t)` | narrative-only | g **NOT FOUND** | none |
| LQ-09 | degree supply overshoots; graduates cascade down | 3 workforce stocks × 3 job tiers, top-down matching, TPA share r | narrative-only (structure verified, equations in unreadable Vensim appendix) | r: hypothetical by the authors' own statement | none |

Four genuine equations exist here (LQ-03/04/05 and, structurally, LQ-09), and **every one of them is about
gate-and-contest mechanics, not about expansion**. They are the best-specified equations in the package and the
least useful for a *massification* generator: they predict effort and distribution, not enrolment levels.
Note also that LQ-04 and LQ-05 are pure theory with **no calibration at all** — the sources say so themselves.

### 4.4 State-building / capacity-gated supply (SB-01…03) — *2 invented, 1 narrative*

| ID | claim | form | status | key number | code |
|---|---|---|---|---|---|
| SB-01 | a law moves enrolment only as far as capacity allows | `effective_push = law_t · G(C_t)`, `G(C)=C^κ` | programme-invented | **κ = 0.75** (declared range 0.5–1.0); PUSH **0.05**; CEIL **0.25** | `anchor.py` L64–90; `pushpull.py` L104–113 |
| SB-02 | capacity = weighted mix of delivery, fiscal, enforcement | `C = Σ w_j x_j`; `x_del=clip((40−PTR)/20)`, `x_fis=clip((%GDP−2)/3)`, `x_enf=years/13` | programme-invented | weights **0.5/0.3/0.2**; PHL C(1960)=**0.2337**, C(2017)=**0.7964**, C(2024)=**0.7925** | `anchor.py` L46–61; `run_meta.json` |
| SB-03 | compulsory law necessary, not sufficient; enforcement binds | needs `attendance = law_t · e_t` with measured `e_t` | narrative-only | **no enforcement series exists anywhere in the package** | de jure proxy only (`anchor.py` L58) |

The literature here (Paglayan, Gellner, Tilly, Angrist–Krueger) supplies **mechanism and falsifiers, never a
functional form**. The gate `C^κ` and the index weights are Council decisions (A9/A10) — defensible, but they are the
programme's assumptions. **κ sensitivity over {0.5, 0.75, 1.0} is declared and was never run** (audit D-07), so the one
new mechanism has no robustness check behind it.

### 4.5 Demographic / cohort flow (DEM-01…04) — *2 invented, 1 estimated, 1 narrative*

| ID | claim | form | status | key number | code |
|---|---|---|---|---|---|
| DEM-01 | births from women 15–49 × TFR; cohort becomes intake at 6 | `births_t = 0.5·Σ_{15..49} pop · TFR/35` | programme-invented | TFR paths: PHL 4.32→2.08, KHM 5.64→2.70, HKG 1.27→0.88, CHN 2.51→1.24 (S); KOR/JPN **A** | `pushpull.py` L71–74; `configs.py` L14–21 |
| DEM-02 | one-year ageing with fixed band survival | `pop_{a,t} = pop_{a−1,t−1}·s_a` | programme-invented | s = **0.995/0.994/0.96** (declared, no life table) | `pushpull.py` L36–39, 75–77 |
| DEM-03 | bigger cohorts depress completion | semi-log completion on ln TFR | programme-estimated | **−0.1893** (0.0436) within / **−0.1222** (0.0267) between, n=712 | none consumes it |
| DEM-04 | crossings always ordered primary→lower→upper→tertiary, gaps widening | crossing-year vector + gaps | narrative-only | PHL: **2017 / 2024 / never (75.03) / 2024–25 band** | scored at `anchor.py` L147–150 |

DEM-01/02 are declared accounting approximations and are fine as such — but they are the *engine* of a cohort-flow
model, and their constants (1/35, female share 0.5, three-band survival) are not sourced. DEM-03's coefficient is the
programme's own and the literature layer grades the underlying hypothesis **NOT VERIFIED**; the CSV also records an
ambiguity: `scaling_laws.csv` labels the relation "semi-log" without saying whether the outcome is a level or a logit,
so the coefficient cannot be re-used without re-reading the script.

### 4.6 Formal push-pull — the programme's own model (PP-01…10) — *2 literature, 8 invented*

| ID | form | status | what it does | code |
|---|---|---|---|---|
| PP-01 | `intake_t = clip(intake_{t−1}[1 + 0.1 e_d(job_{t−lag}/job_t − 1)], 0.2, 1)` | programme-invented | demand-led channel | L83–84 |
| PP-02 | `p_k = clip(a_k + g_k ln gdp + u_k urb + m_k ln gdp [+0.02 e_d ln job], lo, hi)` | programme-invented | progression (14 free params) | L95–103 |
| PP-03 | `job_t = exp(0.012(t−1960))(1 + e_s(educ−0.15))` | programme-invented | jobs index | L79 |
| PP-04 | `g_t = g0 + 0.5 e_s max(0, educ−0.15) + shock`; `gdp_t = gdp_{t−1}(1+g_t)` | programme-invented | education-led feedback | L80–81 |
| PP-05 | `ent=pop_6·intake; prim=ent·cyc_p; low=prim·p_p·cyc_l; …` | programme-invented **(mis-specified)** | enrolment stocks | L114–120 |
| PP-06 | `GER_l = 100·stock_l/Σ pop_band` | **equation-in-literature** (UIS definition) | GER | L140–143 |
| PP-07 | `completion = 100·p_pri; 100·p_pri·p_low; 100·p_pri·p_low·p_up` | programme-invented **(contradicts its own comment)** | the FIT series | L134–139 |
| PP-08 | `educ_t = 0.97 educ_{t−1} + 0.03 min(1,(up+ter)/prim)` | programme-invented | educated share | L130 |
| PP-09 | `intake ×= (gdp_{t−lag_in})^{eta_in}` | programme-invented | scaling repair margin | L85–90 |
| PP-10 | panel Granger test `y_t ~ Σb y_{t−j} + Σc x_{t−j} + FE` | **equation-in-literature** (test form) | the push-pull discriminator | `m2.py`; `push_pull_tests.csv` |

PP-10's estimates (on disk, all labelled EQUIVALENT / no direction claim) are the closest thing the programme has to
push-pull *moments*: wage-share growth → secondary GER **F=4.11, p=0.001, sum +0.050**; tertiary GER → GDP growth
**F=6.52, p<0.001, sum +0.205**; completion → GDP growth **sum −0.667 (0.270)**; and GDP growth → GER **null**.

**Three code-level facts a generator must not ignore** (all inspection, not new estimates):
1. **PP-07 makes completion a product of fitted probabilities.** The cohort flow never enters it, despite the code
   comment and `PREDECLARATION_AMENDMENT_013.md` §G (audit D-01). "Cohort-flow model" describes only the GER branch.
2. **PP-05 double-multiplies cycle lengths**, so committed GER runs 332.8–3514.4% (audit D-02). GER-based milestones
   are therefore artefacts — M4 = 1960 in all 12 arms including the no-push arm.
3. **PP-09 is not the equation the predeclaration states.** `PRE_SCALING_REPAIR.md` §2 declares
   `intake_t = intake_base·(Y_{t−lag}/Y_ref)^{eta_in}` — a *level* relation to a reference income. The code compounds
   the previous year's intake by `gdp^eta_in` each year (`pushpull.py` L90), which is a cumulative growth factor that
   saturates at the clip `[0,1]`. The two are not the same model; the repair's failure to generate positive scaling is
   consistent with intake being pinned at its ceiling.

### 4.7 Scaling laws (SC-01…06) — *3 literature, 3 estimated*

| ID | form | status | key numbers (with path) |
|---|---|---|---|
| SC-01 | `Y = Y0·GDPpc^β`, within and between FE | programme-estimated (power-law form imported from urban scaling) | sec GER **0.0904** (0.1238) within / **0.2154** (0.0349) between, n=1042; tert GER **0.8482** (0.1719) / **0.5666** (0.0817), n=1037; lower-sec comp **0.2468** (0.1188) / **0.1690** (0.0343), n=629 |
| SC-02 | the three adopted **targets** (between estimator) | programme-estimated | **+0.28584** (0.04516); **+0.77609** (0.08642); **+1.17400** (0.15722) — `model2/runs/scaling_estimates.csv` |
| SC-03 | within-vs-between **gap** as the object | programme-estimated | industry **0.528 vs 0.143**; agriculture **−0.120 vs −0.990**; services 0.275 vs 0.294 |
| SC-04 | `y = K/(1+exp(−r(t−t0)))` | **equation-in-literature** (candidate form only) | PHL sec GER K=**92.3**(2.4), r=**0.0525**, t0=**1971.9**; KHM primary K=84.6, r=0.1583, t0=2001.5; CHN tertiary K=125.6, r=0.1267, t0=2020.1 |
| SC-05 | `y = K exp(−exp(−r(t−t0)))` (Gompertz) | **equation-in-literature** (candidate) | E6 holdout: logistic 2/6 PASS, Gompertz 1/6, linear 0/6, exponential 0/6 |
| SC-06 | `Y = Y0·N^β` (urban) | **equation-in-literature** (VERIFIED, the only real scaling law) | patents **1.27** [1.25,1.29]; wages **1.12**; gasoline stations **0.77**; cables 0.87 |

Two cautions the register records in full:
- **A1 and A3 are mutually inconsistent** (audit D-13): the target secondary exponent **0.286** lies *outside* the
  containment range **[0.0904, 0.2154]**. A simulator that generated exactly 0.286 would *fail* containment. Do not
  copy both into a generator's success test.
- The A1 targets are model2's own *between* estimate (`scaling_estimates.csv`), so the "independent estimator" claim
  covers the model, not the target (audit D-14).
- SC-04/05 are **candidate** forms, not laws: `SCALING_LAWS.md` §6 lists logistic universalization as a candidate and
  says the shape "must be estimated"; and only **68 of 194** fitted series are identified.

### 4.8 Sectoral / structural (SEC-01…05) — *3 invented, 1 estimated, 1 narrative*

| ID | form | status | key number | code |
|---|---|---|---|---|
| SEC-01 | `agri = clip(0.75·exp(−0.35 ln gdp) + 0.02, 0.01, 0.95)` | programme-invented | 0.75 / 0.35 / 0.02 (declared) | L123 |
| SEC-02 | `serv_nonag = clip(0.45 + 0.08 ln gdp + 0.15 educ, 0.2, 0.9)` | programme-invented | 0.45 / 0.08 / 0.15 | L125–127 |
| SEC-03 | `formal = clip(0.25 + 0.55 educ + 0.05 ln gdp, 0.02, 0.95)` | programme-invented | 0.25 / 0.55 / 0.05 | L128 |
| SEC-04 | `ln(share) = a + γ ln GDPpc` | programme-estimated | agri −0.1201/−0.9901; industry 0.5283/0.1426; services 0.2745/0.2938 | `scaling_laws.csv` S7–S9 |
| SEC-05 | ECI ↔ schooling | narrative-only | ECI~completion(t−10) 0.593 (0.176); ECI~literacy 0.001 ns; ECI→growth replication **fails** (−0.158, −0.068) | none (parked) |

`SCALING_LAWS.md` §5 is explicit: **there is no canonical sectoral scaling law**, and sector shares vs income are a
*development regularity*, not a law with a stable exponent for our countries. The three code equations are therefore
declared reduced forms whose constants were chosen, not estimated — the audit's phrase for this block is "a relabelled
income term", and SEC-01's `0.35` and SEC-03's `0.55` have no source at all.

---

## 5. Every numeric value used above, and where it lives

| value | meaning | source path |
|---|---|---|
| 0.088 / 0.087 / 0.069 | Mincer private return world / EAP; social return EAP | `02_lit/ECON_TARGETS.csv`; `10_massification/lit/SCALING_LAWS.md` §2 |
| 3.99 (3.71–4.36) | PHL→US place premium | `02_lit/ECON_TARGETS.csv` row 4; `10_massification/lit/PUSH_PULL.md` |
| 9 : 1 ; 126% ; 38.4% | licensed nurses per migrant; rise per 100k; pass rate | `10_massification/lit/PUSH_PULL_TARGETS.csv`; `model/PRE_EXP_E3_PH_NURSES.md` |
| 10.1% (7.8% in 2009) | firms citing skills as a major obstacle | `10_massification/lit/LABOUR_MARKET_REPORTS.md` §1.1 |
| 0.0904 / 0.2154 ; 0.8482 / 0.5666 ; 0.2468 / 0.1690 | within/between exponents: secondary GER, tertiary GER, lower-sec completion | `10_massification/relations/data/scaling_laws.csv` S1–S4 |
| −0.1201 / −0.9901 ; 0.5283 / 0.1426 ; 0.2745 / 0.2938 | sector shares vs income (agri / industry / services) | same file, S7–S9 |
| −0.1893 / −0.1222 | primary completion ← TFR (within / between) | same file, S12 |
| 0.28584 / 0.77609 / 1.17400 | the three A1 target exponents (+se) | `10_massification/model2/runs/scaling_estimates.csv` |
| 92.3 / 0.0525 / 1971.9 | PHL secondary GER logistic K / r / t0 | `10_massification/relations/SCALING_NOTES.md` §1 |
| κ = 0.75 ; 0.5/0.3/0.2 ; 0.05 ; 0.25 | gate exponent, index weights, push scale, ceiling share | `10_massification/model/anchor.py` L64, L54–59, L73, L82 |
| C(1960)=0.2337 … C(2024)=0.7925 | PHL capacity index series | `10_massification/model/anchor_out/run_meta.json` |
| 0.995/0.994/0.96 ; 6/4/2/4 | survival bands; PHL cycle lengths | `10_massification/model/configs.py` L41, L33 |
| 4.35 / 8.60 | linear-trend and persistence benchmarks (pp) | `10_massification/model/calib/calibration_table.csv` |
| −1.893 / −0.379 / −0.743 ; −1.229 / −0.137 / −0.353 | generated OOS exponents, unrepaired (secondary / tertiary) | `10_massification/model/calib/scaling_check.csv` (via `STATUS.md` §3k; **no generator script found** — audit D-11) |
| −2.734 / −2.527 / −1.034 ; −0.319 / −1.317 / −0.391 | generated OOS exponents, repair cell | `10_massification/model/calib/repair_scaling.csv` |
| 1.27 / 1.12 / 0.77 | urban scaling exponents (patents / wages / gasoline stations) | `10_massification/lit/SCALING_LAWS.md` §1 (Bettencourt 2007 Table 1) |

## 6. Divergences found while extracting (recorded, not repaired)

These are observations from reading code against the documents that govern it. None was created for this file; all are
checkable at the cited line.

| # | divergence | evidence |
|---|---|---|
| 1 | Declared parameter ranges **disagree between two files**: `e_d` hi = 0.8 (`configs.py` CHANNEL_PRIORS) vs 0.6 (`calibrate.py` BOUNDS); `lag_d` hi = 5 vs 3; `g0` hi = 0.05 vs 0.045; `lag_s` hi = 8 vs 6 | `model/configs.py` L44–50 vs `model/calibrate.py` BOUNDS |
| 2 | Progression is declared **logistic** but coded as a **clipped linear** function of log income | `PRE_SCALING_REPAIR.md` §2 item 2 vs `pushpull.py` L95–103 |
| 3 | The gate is declared a **sigmoid** (`C0=0.5, s=0.15`) then amended to a **power** `C^κ`; the committed findings file still prints "sigmoid" because `anchor.py` L182 hard-codes that sentence (audit D-17) | `PRE_ANCHOR_CAPACITY.md` §2 vs `anchor.py` L64, L182 |
| 4 | Completion is documented as cohort-flow-generated but is a product of fitted probabilities (audit D-01) | `pushpull.py` L132–139 |
| 5 | The intake "income margin" is a level equation in the predeclaration but a compounding update in code (§4.6) | `PRE_SCALING_REPAIR.md` §2 item 1 vs `pushpull.py` L88–90 |
| 6 | The K-12 cycle-length switch is **declared but not implemented**: `CYCLE['PHL']` is one constant dict with no year dimension (audit D-21) | `configs.py` L32–39; `pushpull.py` L53, L116–119 |
| 7 | The A1 target 0.286 is **outside** the A3 containment range [0.0904, 0.2154] — an unwinnable criterion (audit D-13) | `repair.py` L21–24 |
| 8 | `scaling_check.csv`, the source of the programme's central negative number, has **no generator script** in the tree (audit D-11) | `model/calib/scaling_check.csv`; grep finds no writer |
| 9 | Enforcement sits inside `G(C)` *and* is a step function of the same law dates, so `law × G(C)` counts compulsory-length changes twice (audit D-09) | `anchor.py` L58 vs L77–79 |

## 7. What is deliberately absent

- **No Yang (2026) equation.** The card is abstract-only and the CES form in the architecture notes is explicitly
  the author's conjecture, not the source's. Registering it would have been fabrication.
- **No education–output elasticity.** `SCALING_LAWS.md` §4: it is "not a standard, uniquely defined quantity" — there
  is no canonical number to put in a parameter cell.
- **No returns→enrolment coefficient, no requirement-schedule effect, no informality elasticity, no price elasticity of
  tutoring.** All four are `NOT FOUND`/`unusable` in `02_lit/ECON_TARGETS.csv`, and all four are load-bearing for one
  family or another.
- **No fitted θ from the anchor's 12 arms.** None was persisted (audit D-03), so no arm can be reproduced or re-scored.

---

## 8. Sources actually opened for this register

**Literature layer (`10_massification/lit/`)** — read in full: `MASSIFICATION_THEORY.md`, `PUSH_PULL.md`,
`RIVAL_MODELS_ANCHOR.md`, `RIVAL_MODELS_TO_TEST.md`, `SCALING_LAWS.md`, `STATE_CAPACITY.md`,
`LABOUR_MARKET_REPORTS.md`, `PHASE_WRITEUP_SHELL.md`, `UNIVERSALIZATION_TIMELINES_JPN_KOR_HKG.md`.
Also opened: `PUSH_PULL_TARGETS.csv`.

**Predeclarations (`10_massification/model/`, `model2/`)** — read in full: `PREDECLARATION.md`, `PRE_ANCHOR_A1.md`,
`PRE_PIVOT_ANCHOR.md`, `PRE_SCALING_REPAIR.md`, `PRE_EXP_E2_PH_K12.md`, `PRE_EXP_E3_PH_NURSES.md`,
`model2/PRE_DECLARATIONS_M2.md`. Read for the gate form and weights that the code implements: `PRE_ANCHOR_CAPACITY.md`
(not on the required list, opened because `anchor.py` cites it and A9/A10 amend it).

**Estimates and data** — `relations/data/scaling_laws.csv`, `relations/SCALING_NOTES.md`,
`model2/runs/scaling_estimates.csv` (to verify that the A1 targets 0.286/0.776/1.174 are its *between* rows),
`model/anchor_out/run_meta.json` (capacity series). Inspected, not registered: `relations/data/push_pull_tests.csv`
via `SCALING_NOTES.md` §3.

**Council** — `08_council/brief_018/SYNTHESIS_018.md` (direction menu and selected portfolio M/V, §B–§C, and the Z1–Z4
blocks), `08_council/brief_013/SUCCESS_CRITERIA.md` (all of it: §1–§7 and Amendments A1–A10).

**Audit** — `extensions/audit_2026-11-20/b_models/MODEL_INVENTORY.md` (implemented vs claimed; the defect register
D-01…D-21), `extensions/audit_2026-11-20/a_regressions/GAPS_AND_LEADS.md` (what is untested, and the six candidate
moments).

**Code read line-by-line** — `model/pushpull.py` (203 lines), `model/anchor.py` (199), `model/configs.py` (60),
`model/calibrate.py` (KEYS/BOUNDS and loaders), `model/repair.py` (A1/A3 dicts, NEW_KEYS/BOUNDS).

**Opened only to trace an equation the required files cite** — `02_lit/MODEL_CARDS.md` (Yoo §1, Kim §2, Kang §3,
Jayachandran §4, GXL §5, Ostrovsky–Schwarz §6, Yang §7, He §8), `02_lit/ECON_TARGETS.csv`,
`09_relations/LITERATURE_ELASTICITIES.md`, `09_relations/LITERACY_ECI_DEMOGRAPHY.md` (ECI §1–2),
`10_massification/README.md` (binding rules).

**Not opened** (and therefore not cited): `02_lit/ECON_LIT.md`, `02_lit/CLAIM_REGISTER.csv`, the raw `02_lit/raw/`
sources, `model/model*/PRE_ANCHOR_A2.md`, `PRE_PORTABILITY_A6_A7.md`, `PRE_TIMING_JPN_KOR_HKG.md`,
`relations/CAPACITY_LAYER.md`, `relations/EVENT_WINDOWS.md`, and the many `runs/*.csv` behind the audit's numbers
(those are quoted from the audit, not re-read).
