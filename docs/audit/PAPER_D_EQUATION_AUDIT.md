# PAPER_D_EQUATION_AUDIT — what the standard economics-of-education equations can and cannot say about shadow education

Owner lane: `engine-core` (design-only) · 2026-11-25 · branch `research/contest-audit-v2-2026-11-25`
Companion to `PAPER_C_MODEL_GAP.md`. Source being audited: the 183-equation inventory at
`docs/audit/refs/education-equation-inventory-20261124.txt` (Bridge attachment `20261124154148-7126f591`,
34,984 B, 404 lines, sha256 `0fd30f770a75ee55cdf26d3ce332df795f78d29d070bed01af38810bfa4752df`), committed with the
caveat that it is **a candidate map, not a verified bibliography**.

**Paper D thesis (candidate, Commander-recorded):** a mechanism audit of the standard economics-of-education
equations, with shadow education as the test case. The outcome is **incompleteness / context-dependence**, not "the
literature is wrong". The engine is used as the mechanism-rich test bed: for each claimed omission we state a
*divergence test* where the standard equation and the mechanism-rich model predict different signs or magnitudes.

Engine tree: commit `79add93` (core.py 1268 L, tutoring.py 551 L, schools.py 170 L, labour.py 243 L, planning.py 175 L).
Evidence status: **DESIGN + REPRODUCED SIMULATION** (read-only probes on the host; see `PAPER_C_MODEL_GAP.md` §2).

---

## 1. Classification scheme

| class | meaning | how to use it in Paper D |
|---|---|---|
| **(a) accounting identity** | true by construction, no behaviour (e.g. PTR, GER, GPI, expenditure shares, budget identities). Cannot be falsified; only mis-applied (wrong denominator) | never cite as a mechanism; verify denominator + population before use |
| **(b) stylized theory with explicit assumptions** | true *within* stated assumptions; the assumptions are the contribution and the limitation | list the assumptions verbatim; name where they fail for shadow education |
| **(c) empirical specification** | estimates a parameter under identifying assumptions; context-dependent by construction | state the estimator + identifying assumption; Paper B/A designs use these (§9) |
| **(d) incomplete for the mechanism we now model** | the equation omits one of the five mechanisms M1–M5 below; it may still be correct for its own question | state the divergence test (sign/magnitude) and compute it |

Mechanisms that standard equations typically omit (the "M-tags"):

* **M1 — school-supplied effective preparation S**: a positive effort/preparation input from the school (homework,
  feedback, supervision, teaching effort), distinct from generic "school quality", with a cost in teacher time.
* **M2 — positional externalities with fixed seats**: admission is a fixed-seat contest; private effort is partly a
  transfer, and the seat rule (share of cohort vs applicants, multi-seat vs single prize) determines who is crowded out.
* **M3 — teacher-as-supplier withholding / rent extraction**: teachers can withhold lessons they then sell back as
  tutoring (`h = h_max·driver·(1−monitoring)·(1−own_ban)`; engine `schools.py:52-54`), so the own-teacher tutoring
  supply form is created by the school's pay/monitoring regime.
* **M4 — student/teacher time budgets**: total time is fixed; tutoring, homework, school and contest prep compete
  (inventory eq 21 states the identity but no mechanism uses it); teachers have finite marking/feedback time.
* **M5 — supply-form choice**: own teacher vs firm vs state supply have different technologies, prices, entry
  conditions and welfare properties; the standard demand equations treat "tutoring" as one homogeneous good.

---

## 2. Classification tables

### 2.1 §2 — household education decisions (eq 11–25)

| # | equation | class | assumptions / where it fails | engine mapping | M-tag |
|---|---|---|---|---|---|
| 11 | `U=U(C,H,L)` | (b) | separable/representative utility; no intra-household conflict, no peer/positional terms | implicit value recursion `core.py:626,635`; `delta`, `kappa`, logit noise `tau` (`core.py:926`) | M2 |
| 12 | `C+p_sS+p_tT+X=Y` | (a) identity **as a constraint**, (d) as a mechanism | static; no borrowing limit dynamics, no time; treats schooling and tutoring as perfect cash substitutes | cash/need `core.py:933-935`; `borrow`, `subsist`, `shock_sigma` | M4 |
| 13 | `max_S Σ E(w_t|S)/(1+r)^t − C(S)` | (b) | expected-wage objective, rational expectations, no credit constraints, no peer effects | `values()` backward induction + beliefs `B` (`core.py:626-635,1200-1226`) | M2, M5 |
| 14 | `MB(S*)=MC(S*)` | (b) | interior optimum; with discrete school sectors/credit constraints the choice is a corner | discrete continue decision ('go' logit `core.py:926`; liquidity `core.py:937-944`) | — |
| 15–18 | NPV / IRR / PV / full cost | (b)/(c) | require an income path and a discount rate; the engine has `delta`/`kappa` but does not output r or IRR | `delta=0.93`, `kappa=12`; `inc_by_cred` (`labour.py` summary) | — |
| 19 | Becker–Lewis `C+p_n n+p_q nq ≤ Y` | (b) | fertility-quality trade-off; not modelled (cohort size fixed) | — | — |
| 20 | `H_{t+1}=(1−δ)H_t+I_t` | (b) | linear depreciation; **incomplete for M1/M4** (I is not decomposed into S/T/time) | `k['L'] += dL` `core.py:960-968` (δ=0, additive) | M1, M4 |
| **21** | `T_s+T_t+T_w+T_l = T̄` | **(a) identity** + **(d) mechanism absent** | an identity is not a behavioural model: no time cost of tutoring, no homework/teacher time, no leisure choice | **ABSENT** (no time params anywhere) | **M4** |
| 22 | `P(S_i=1|X)=logit` | (c) | reduced-form; mixing true state dependence and unobserved heterogeneity; no price/time channel unless included | structural continue logit `core.py:926` (mechanism, not estimated) | M4 |
| 23 | multinomial `P_ij=e^{V_ij}/Σe^{V_ik}` | (c)/(b) | IIA; no capacity constraints in standard form | school choice `schools.py:117-134`; 3-way tutoring choice `tutoring.py:232-241` (capacity+rationing added) | M5 |
| 24 | `B_i ≤ B̄_i` | (b) | borrowing constraint; engine has a linear `borrow` share, no collateral/credit rationing | `borrow` `core.py:933`; `need_mode/need_max` | — |
| 25 | `(∂U/∂S)/(∂U/∂C)=p_s` | (b) | interior optimum, no discrete supplier, no time | tutoring argmax `tutoring.py:239-241`; school choice `schools.py:131-134` | M4, M5 |

### 2.2 §3 — education production / skill formation (eq 26–41)

| # | equation | class | assumptions / where it fails | engine mapping | M-tag |
|---|---|---|---|---|---|
| 26 | `A_i=f(S_i,F_i,P_i,θ_i)` | (b) general form | "S" is generic school input; no distinction between quality, effort, time, or supplier | `dL` `core.py:963-966`: school `q·(1−h)·voc·exp(β_a a)`, tutoring, home, noise | M1, M3 |
| 27 | `A_it=f(S_i^t,F_i^t,θ_i)` | (b) cumulative inputs | no time allocation, no diminishing returns specified | cumulative `L` (`core.py:968`) | M1, M4 |
| 28 | `A=BS^αF^βT^γ` | (b) Cobb–Douglas | constant elasticities, log-linear, no fixed-seat competition, no time; substitution between S and T is imposed by α,β | **ABSENT** (engine additive-linear, `production='additive'`) | M1 |
| 29 | `MP_T=∂A/∂T` | (b) | marginal productivity; engine's value of learning is its *price*, not its production derivative | `mvl` `core.py:854`; fixed `tut_effect` `tutoring.py:252` | M1 |
| 30 | `A=B[ωS^ρ+(1−ω)T^ρ]^{1/ρ}` | (b) CES | requires ρ and ω; the sign of substitution is the whole question and is not identified without variation in S | **ABSENT** (additive only) | M1 |
| 31 | `∂²A/∂S∂T>0` | (b) assumption | complementarity is assumed, not derived; opposite sign (substitutes) plausible when S is test-aligned | **ABSENT** — engine tutoring gain is independent of S (`tutoring.py:252`) | M1 |
| 32 | `ΔA_it=βX_it+ε` | (c) value-added regression | requires no dynamic selection; teacher/school inputs not randomised | not estimated; engine generates such data | — |
| 33 | `A_it=ρA_i,t−1+X'β+ε` | (c) | ρ captures persistence; engine has ρ=1 with δ=0 by construction | `k['L'] += dL` (`core.py:968`) | — |
| 34, 35 | teacher / school FE models | (c) | FE absorbs time-invariant quality; engine has one aggregate q, no teacher/school IDs | aggregate only (`schools.py:49,58-59`) | — |
| 36 | peer achievement `A_i=…+γĀ_{-i}` | (c) | reflection problem; engine has no peers | **ABSENT** | — |
| 37 | `A_i=α+β_1ClassSize_i+…` | (c) | class size endogenous to school choice; engine links ptr→q mechanically | `q(ptr)` `schools.py:49`; private `priv_ptr` `schools.py:92` | M1 |
| 38 | `H_{t+1}=f_t(H_t,I_t)` | (b) dynamic technology | general; needs functional form/estimates | additive `L` recursion | M1 |
| 39 | `∂H_{t+1}/∂H_t>0` | (b) self-productivity | holds by construction in engine (L cumulative) | `core.py:968` | — |
| 40 | `∂²H/∂H∂I>0` | (b) dynamic complementarity | not implied by additive engine | **ABSENT** | M1 |
| 41 | `A_i=α+β_1S_i+β_2T_i+β_3S_iT_i+…` | (c) empirical interaction | sign is an estimate; causal requires identification; engine demand side has `h·q` buy-back interaction (`tutoring.py:232-233`) but **achievement side has none** | **PARTIAL** — demand interaction only | M1, M3 |

### 2.3 §5 — shadow education & private tutoring (eq 57–86)

| # | equation | class | assumptions / where it fails | engine mapping | M-tag |
|---|---|---|---|---|---|
| 57 | `D_i=1(T_i>0)` | (a) definition | — | `tut_any` `tutoring.py:429` | — |
| 58, 59 | logit/probit participation | (c) | reduced-form; no price/time/supplier structure unless included; endogeneity of tutoring and achievement | structural choice `tutoring.py:232-241` (mechanism, not estimation) | M4, M5 |
| 60 | `ln T_i=α+X'β+ε` (intensity) | (c) | selection on participants; engine produces spend distribution | `tut_k12_spend_by_q` series | — |
| 61–63 | hurdle / Tobit / double-hurdle | (c) | latent-variable assumptions; distinguishes participation vs amount | engine is a structural discrete+continuous choice (cash cap), not these estimators | — |
| 64 | `s_i^T=E_i^T/Y_i` | (a) identity | denominator choice matters (income vs total expenditure) | spend/income computable from `k['y']`, `tut_k12_spend` | — |
| 65, 66 | Engel curve / income elasticity | (c) | estimated on positive expenditure; engine can generate it; **omits S** so estimates confound school supply with income | computable; pilot q0 axis provides S variation | M1 |
| 67, 68 | own/cross-price elasticities | (c) | requires price variation; engine has `p_own`, `p_firm`, `firm_ban`, `own_ban` variation | `tutoring.py:57-60,96-101` | M5 |
| 69 | tutoring share of education spending | (a) identity | — | computable (`tut_spend`, `hh_spend`) | — |
| 70 | `C+P_TT+P_SS≤Y` | (a) constraint / (b) | joint constraint; engine has cash constraint but **no time constraint and no endogenous schooling price for public** | `core.py:933-935`; `fee_public` `schools.py:57` | M4 |
| 71, 72 | tutoring in production (+interaction) | (b)/(c) | same as eq 26/41; engine demand reflects it, achievement side incomplete | `core.py:963-966`; `tutoring.py:252` | M1 |
| 73 | `∂A/∂T>0` | (b) | assumed positive; could be zero/negative if time crowds out schoolwork or if tutoring is positional | engine imposes positive `tut_effect`; no time crowding | M1, M4 |
| 74, 75 | baseline/dose-response regressions | (c) | linearity/dose form assumed; engine imposes constant effect | fixed `tut_effect` (`tutoring.py:252`) | M1 |
| 76 | tutoring×SES heterogeneity | (c) | engine has SES through income/cash and `home`, not an explicit heterogeneous effect | PARTIAL (`tutoring.py:230-238`) | M4, M5 |
| 77, 78 | IV first/second stage | (c) | exclusion restriction; **not a mechanism** | estimation only (Paper B/A) | — |
| 79 | peer tutoring demand `T_i=…+ρT̄_{-i}` | (c) | engine has no peers | **ABSENT** | — |
| 80 | tutoring×school-quality `β_3 T_i Q_{s(i)}` | (c) | the key Paper C estimate; **engine achievement side has no interaction** (demand has buy-back `h·q`) | PARTIAL | M1, M3 |
| 81 | `P_i(admission)=e_i^κ/Σe_j^κ` | (b) Tullock contest | single prize, no seats, no heterogeneity in outside options; **engine uses multi-seat PL top-K** (`core.py` PL API) with fixed seats — a different contest object | contest gates `core.py:998-1035`; PL expected/realised | M2 |
| 82 | `max_{T_i}[V_iP_i−P_TT_i]` | (b) | fixed prize V, no time, no school prep, no own-teacher alternative | contest effort `tutoring.py:334-380` (prize = `gate_prize_dv`, P = PL) | M2, M4, M5 |
| 83 | `Q_T^d(P_T,Y,…)=Q_T^s(P_T,W,…)` | (b) market equilibrium | needs supply conduct; engine uses capacity+entry, not price clearing | capacity/entry `tutoring.py:242-250`; price `96-101` | M5 |
| 84 | `π_T=P_TQ_T−C(Q_T)` | (b) provider profit | not in engine (only `firm_rev`) | **ABSENT** (only revenue, `tutoring.py:459`) | M5 |
| 85 | `P_T^{consumer}=P_T(1+τ)` | (a) definition | tax only applied to contest prep in engine (`contest_tax_rate`), not to firm tutoring | `tutoring.py:63,288-291` | — |
| 86 | reduced-form policy regression | (c) | identification-dependent; cannot speak to supply form | estimation only | — |

### 2.4 Sections used for claims (§1, §7, §8, §9, §10)

| # | equation | class | note / engine mapping |
|---|---|---|---|
| 1–10 | GER, NER, AR, CR, TR, DR, PTR, EPS, GPI, z-score | (a) identities + definitions | engine emits the underlying counts: `att_by_grade`, `new_by_grade`, `census`, `ptr`, `pub_spend`, `private_share`; denominators must be stated (see D3 audit) |
| 106–109 | ES/GDP, ES/G, unit cost, real spending | (a) identities | `pub_spend`, `pub_budget`, `gdp` (`state.py` FiscalState note) |
| 110–115 | input budget, ICER, SNPV, BCR, NB, fiscal NPV | (b)/(c) cost-benefit | engine can produce costs/benefits but no discounting block (`delta` is utility discount, not fiscal r) |
| 116, 117 | benefit incidence, concentration index | (a)/(c) | SDG4 parity (`sdg4.py:39-56`) gives partial incidence; concentration index not computed |
| 118, 119 | voucher/effective tuition, net subsidy | (a) definitions | `voucher` (`schools.py:92`), `levy`, `fee_public` |
| 120 | CES aggregation public/private inputs `H=[ωG^ρ+(1−ω)P^ρ]^{1/ρ}` | (b) | **ABSENT** — engine assigns one sector's q per child |
| 121 | funding formula | (b)/(policy) | `budget_per_child`, `FiscalState` (`state.py`) |
| 122 | `MSB=MSC` social optimum | (b) | no welfare block; Paper C §3.4 candidate (eq 183) |
| 123–131 | Gini/Theil/variance/gaps/tutoring-gap Gini | (a)/(c) | computable from `E.ALL`; tutoring-gap series already `tut_k12_rate_by_q`; Gini/concentration not implemented |
| 132–137 | intergenerational elasticities, Oaxaca, SES×T, QTE | (c) | estimation only; engine data could support them |
| 138–143 | OLS/FE/DiD/event study/ATT/DDD | (c) | Paper B uses FE/event-study style specifications; **not mechanisms**; note staggered-DiD pitfalls (142/143) |
| 145–154 | ATE/ATT/ITT/LATE/IV/RD/RCT | (c) | identification designs; Paper A/B claim support only |
| 155–167 | propensity, matching, quantile, multilevel, cluster, ordered logit, Poisson, NB, synthetic control, control function, mediation | (c) | estimators; note cluster-robust eq 160 used by Paper B/A claims (see bootstrap audit) |
| 168–174 | LAYS, learning poverty, skill gap, migration, health, fertility | (a)/(c) | SDG4 `learning_poverty`, `mean_years` (`sdg4.py:56-57`) |
| **175–177** | teacher exit/incentive/`bA'(e)=C'(e)` | (b) | **PARTIAL** — engine has mechanical withholding `h` (`schools.py:52-54`), no teacher utility/effort optimisation; candidate S/M3 extension |
| 178, 179 | school choice utility, capacity `Σ_i x_is ≤ Capacity_s` | (b) | `schools.py:117-165` (choice + rationing); firm capacity `tutoring.py:242-250` |
| 181 | intergenerational transmission | (b)/(c) | **ABSENT** |
| 183 | `SW=Σω_iU_i−λC_public` | (b) welfare | **ABSENT** — Paper C welfare block candidate |

---

## 3. Incomplete-for-mechanism: omissions and contradictions (kept separate)

**Omissions (class d) — the inventory is not "wrong", it lacks the mechanism:**

| mechanism | equations that presume it / omit it | engine evidence that the omission matters |
|---|---|---|
| **M1 school-supplied preparation S** | 20, 26–31, 37–41, 65–66, 71–76, 80 | probe: q0 0.8→1.2 lowers K-12 tutoring 0.605→0.491 and spend 161.7→135.9 (substitution); achievement side has no S×T term (`tutoring.py:252`) |
| **M2 positional seats** | 11, 13, 75, 81–83 | gate share/contest drive prep (probe `contest_r=.8` → K-12 tutoring 0.528→0.419; `elite_logw=.2` → 0.386); single-prize Tullock is a different contest from multi-seat PL |
| **M3 teacher withholding/rent** | 12, 26, 41, 58–59, 71–80 | probe: switching it on (`pay_ratio=.55, monitoring=.2, own_ban=0`) raises h 0→0.144, own share 0.04→0.53, tutoring 0.53→0.78; banning firms leaves own share 0.98 but spend falls 165→118 and firm price ×30 |
| **M4 time budgets** | 12, 20–25, 29, 70, 73, 82 | **absent in engine** (no time params); the inventory's eq 21 is an identity, not a behavioural constraint. Divergence: "more tutoring time raises A" can fail if it crowds out homework/school time |
| **M5 supply form** | 23, 25, 68, 70, 82–85 | engine has three suppliers (own/firm/state) with different price, entry, ban and rent rules; the standard equations treat tutoring as one good. Probe: firm ban changes own share from 0.53 to 0.98, price 0.07→2.10 |

**Contradictions already recorded in the programme (these are claims/implementations, not inventory equations):**

* The **"G9 phantom prize"** (KR G9 paid a prize with no persistent consequence) was **CONTRADICTED** by code audit and
  repaired (D1; `ENGINE_CORE_AUDIT.md` §A).
* **Expected ≠ realised admission probabilities** (1−exp vs PL) was **CONTRADICTED** and repaired (D2).
* The **"100 % seat-expansion paradox"** from the GPU bundle is **CONTRADICTED** (solver truncation; corrected
  inverted-U) — see `EXTERNAL_AUDIT_GPU_2026-11-25.md` / `AUDIT_VERDICT.md`. Not a claim of the inventory.
* Paper B's **combined-policy "win-win" pairing** is **CONTRADICTED** on the frozen 540 record and **flips** on the
  repaired engine under some arms (CF4a); it is a policy claim, not an inventory equation.

**Do not overclaim:** no inventory equation is declared false here. Identities cannot be false (they can be
mis-applied); theory equations are true within assumptions; empirical specifications are context-dependent by
construction. Only the programme-level claims above carry CONTRADICTED status.

---

## 4. Divergence tests (Paper D + Paper C discriminating moments)

For each: standard-equation prediction **X** vs mechanism-rich prediction **Y**, the engine cell to run, the outcome
that discriminates, and minimal compute. "Reuse" = same cell as the Paper C grid. All at matched seeds; report
per-seed CIs; N=600/T=30 for screening unless stated.

| id | omission | standard equation predicts X | mechanism-rich model predicts Y | cells | outcome | compute |
|---|---|---|---|---|---|---|
| **D1** | M1 (S) | tutoring participation/spend independent of school supply after income controls (eq 58/65) | participation **falls** with S (substitution); income elasticity biased if S omitted | q0 ∈ {0.8,1.0,1.2} × 3 income groups (reuse Paper C S axis) | `tut_k12_rate_by_q`, `tut_k12_spend_by_q` | 3 cells × 8 seeds ≈ 24 runs |
| **D2** | M3/M5 | a tutoring **cap/ban** lowers total tutoring spending/participation (eq 86) | cap displaces demand to own-teacher withholding and raises firm price; total spend may fall while own share rises, and the poor lose access | firm_ban {0,.9} × own_ban {0,.95} (+h on/off) | `tut_k12_spend`, `own_share`, `tut_k12_rate_by_q`, `firm_price` | 4 cells × 8 = 32 runs |
| **D3** | M1/M4 | "more homework/feedback raises learning" monotonically (eq 26/28) | with a time budget, S crowds out homework/tutoring time; effect on L can be smaller or zero, and tutoring falls | school_prep {0,.05,.1} × time budget {off,on} (needs wave-2 extension) | `L6/L9`, `student_hours`, `tut_k12_rate` | 6 cells × 8 = 48 runs |
| **D4** | M2 | single-lever policy compression improves both spend and access (additive pairing) | interaction: cap + shadow-price ⇒ single lever may fail, combination may win — Paper B found the pairing claim fails | reuse Paper C cells; add cap arm (contest_max_e×0.5) | spend index, elite-Q5 share, q5−q1 gap | reuse + 12 runs |
| **D5** | M2 | more seats ⇒ monotonically lower effort / higher access (Tullock eq 81) | multi-seat PL with heterogeneous demand can give an **inverted-U** in effort/admission and non-monotone elite incidence | gate share {.12,.23,.35,.50} per regime | `contest_e_mean`, `contest_admit_rate`, elite by q | 4 cells × 8 = 32 runs |
| **D6** | M3 | banning own-teacher tutoring reduces shadow spending (eq 86) | a ban also removes the withholding-sale channel (sell=1−own_ban), so h falls and the welfare effect is ambiguous; firm price rises | own_ban {0,.5,.95} at pay_ratio .55, monitoring .2 | `h`, `own_share`, `tut_k12_spend`, `firm_price` | 3 cells × 8 = 24 runs |
| **D7** | M5 | market clears, one price, no excess demand (eq 83/84) | capacity rationing + entry lag ⇒ price dispersion, unmet demand concentrated by income, provider rents | firm_ban {0,.9} × firm_entry {.1,.3} | utilisation `D/K`, `firm_price`, unmet demand by q | 4 cells × 8 = 32 runs |
| **D8** | M2/M3 | positional contest dissipates rents symmetrically (eq 81) | track/elite prize incidence differs by income because S, h and tutoring access differ; welfare effects not symmetric | 2 gate designs × 3 supply regimes | elite share by q, gap, `elite_inc_gap_*` | 6 cells × 8 = 48 runs |
| **D9** | M5 | supply form is a fixed household choice parameter (eq 58/59) | supply form is **jointly determined** by pay/monitoring policy (own), firm entry/price (firm) and S (state); policy changes supplier mix | reuse D2/D6 cells + R1/R2/R3 regime anchors | `own_share`, `firm_rev`, `h`, `q_pub` | 30 runs (anchors) |

Total divergence-test compute: ≈ **300–420 runs** at N=600/T=30 (≈2–3 CPU-h) with heavy reuse of the Paper C screening
cells; no Paper D compute until the Paper C confirmatory run and an approved prereg (Commander rule).

---

## 5. Minimal new equation set for the Paper C prereg

Notation: i child, t year, S school-supplied effective preparation, T shadow-education preparation, F family input,
L cumulative learning, G shadow share of learning, h withholding, e contest effort, s supplier ∈ {none, own, firm}.

```
(C1) L_{i,t}   = L_{i,t-1} + S_{i,t} + T_{i,t} + F_i + ε_{i,t}                       cumulative learning (eq 20, 33)
(C2) S_{i,t}   = q_{s(i),t}·(1 − h_{s(i),t})·v_{i,t}·exp(β_a a_i) + σ·hw_{s(i),t}   school-supplied prep (eq 26–28)
(C3) T_{i,t}   = θ_own·1[s=own] + θ_firm·1[s=firm] + θ_prep·e_{i,t}                shadow-education prep (eq 29, 71–75)
(C4) G_{i,t}   = max(0, L_{i,t} − Σ_{τ≤t} S_{i,τ})                                 shadow share of learning (new)
(C5a) t_school + t_homework(S) + t_tut(s) + t_prep(e) + t_work + t_leisure = T̄     student time (eq 21 — identity
                                                                                    turned into a constraint)
(C5b) N_pupils·(c_class + c_mark·S) ≤ T_teachers·T̄_teacher                          teacher time (new)
(C6) s_i = argmax_{s∈{none,own,firm}} [ ψ_s(S_i, L_i, p_s, time_left_i) + ξ_{i,s} ] supplier choice (eq 23, 25, 82)
(C7) K_{t+1} = K_t + κ·(D_t − K_t);  P_T = p_firm(1+τ)·max(1, D_t/K_t)^{1/ε};
     π_t = P_T·Q_t − C(Q_t)                                                        firm market (eq 83–85)
(C8) h_t = h_max·max(0, 1 − w_T/w_out)·(1 − monitoring)·(1 − own_ban)              withholding/rent (eq 175–177)
(C9) P_i(admit) = PL_topK( w_i = [x0·L_i/ends + α·prep_i]^r·bonus ; seats )        contest (eq 81 variant: multi-seat)
(C10) SW = Σ_i ω_i U_i − λ·C_public                                                 welfare block (eq 183, optional)
```

Assumptions to state in the prereg (and deviations from the inventory's own assumptions): (i) C1 is additive in the
baseline and a CES/nested variant (eq 30) is a declared switch, not the default; (ii) C2's `hw` is the *positive*
school-effort lever and is the Paper C treatment object; (iii) C5 makes eq 21 a constraint; the inventory's identity
alone cannot generate the divergence tests; (iv) C6 is a random-utility discrete choice with capacity rationing (eq 23
+ 179), not a multinomial logit *estimate*; (v) C7–C8 are partial-equilibrium supplier rules, not a full market
equilibrium; (vi) C9 replaces the single-prize power-form contest with the multi-seat Plackett–Luce object the
repaired engine realises (contract §1.3), so the mapping must be stated explicitly with `seats`, `share_of`, `r`.

---

## 6. Attribution, data and execution notes

1. **Attribution risk (binding):** the inventory is an AI-generated candidate map with placeholder citations
   ("UIS+2", "OECD+3", "doi.org+4", "hanushek.stanford.edu+2", "World Bank+2"). Before any equation is cited in a
   prereg or manuscript, verify the primary source: Hanushek (education production), Todd & Wolpin (cumulative
   production), Cunha & Heckman (skill formation), Becker (human capital), Mincer (returns), Dang & Rogers (shadow
   education), Bray (shadow education), Tansel & Bircan (demand), Biswal (withholding/buy-back), Jayachandran
   (teacher absence), Kim & Lee (Korean tutoring/CSAT), plus measurement sources (UIS, World Bank, OECD).
   Do not cite an equation number as if the inventory were a bibliography.
2. **What the engine can test without new data:** behavioural divergences D1–D9 (simulation) and the consequence of
   supply-form policy parameters. What it cannot test without data: the *magnitudes* of h, buyback share, S
   elasticity, time budgets, firm entry/price elasticities, welfare weights, and which regime is empirically relevant
   for HK vs PH (see `PAPER_C_MODEL_GAP.md` §5).
3. **Execution:** all Paper D tests reuse Paper C pilot/screening cells where possible; no Paper D compute until the
   Paper C confirmatory run and an approved prereg; host-only, ≤2 workers for screening (box only with Commander
   allocation). Report per-seed CIs and preserve negative results.
4. **Deliverable status:** this is a design/audit document, not a claim that the standard equations are wrong. Paper D
   results (labels CONTRADICTED / OMITTED / CONTEXT-DEPENDENT) are future work.

---

## 7. Residual risks

* Equation-numbering refers to the committed inventory text, not to the original sources; numbers may differ in
  published versions — cite sources, not inventory numbers, in the paper.
* Engine mappings are to the current tree `79add93`; the Paper C wave-2 extension (S, time, decomposition,
  supply-form accounting) will add mapping rows and requires a new engine hash and canonical re-pin.
* Divergence tests D3/D7 need the wave-2 extensions before they are runnable; D1/D2/D4/D5/D6/D8/D9 are runnable on
  the current engine with existing switches.
* The `both`/`learning` contest-prep modes and `q0` scaling are easy to misread as separate supply/S levers (see the
  probe gotchas in `PAPER_C_MODEL_GAP.md` §2); the prereg must state the exact switch semantics.

<!-- REFS_DOIS_CROSSREF -->
## Reference register (DOI/ISBN) — cross-reference

Every external source cited in this document is listed below with the identifier that exists (DOI, else ISBN/publisher) and the verification status recorded in the programme register. **Register:** [`docs/audit/REFS_DOIS.md`](REFS_DOIS.md). Add a register row before citing a new source; do **not** cite the 183-equation inventory’s placeholder tokens (`UIS+2`, `doi.org+4`, …).

- `biswal_1999` — Biswal, B. P. (1999). Private tutoring and public corruption: A cost-effective education system for developing countries. The Developing Economies 37(2):222–240. **Identifier:** DOI 10.1111/j.1746-1049.1999.tb00232.x. **Status:** PAYWALLED — NOT RETRIEVED (content described in Dang & Rogers 2008).
- `cunha_heckman_2007` — Cunha, F. & Heckman, J. (2007). The Technology of Skill Formation. American Economic Review 97(2):31–47. **Identifier:** DOI 10.1257/aer.97.2.31. **Status:** VERIFIED BIBLIOGRAPHIC.
- `dang_rogers_2008` — Dang, H.-A. & Rogers, F. H. (2008). The Growing Phenomenon of Private Tutoring: Does It Deepen Human Capital, Widen Inequalities, or Waste Resources? The World Bank Research Observer 23(2):161–200. **Identifier:** DOI 10.1093/wbro/lkn004. **Status:** VERIFIED PRIMARY TEXT.
- `filmer_2020_lays` — Filmer, D., Rogers, H., Angrist, N., & Sabarwal, S. (2020). Learning-adjusted years of schooling (LAYS): Defining a new macro measure of education. Economics of Education Review 77:101971. **Identifier:** DOI 10.1016/j.econedurev.2020.101971. **Status:** VERIFIED BIBLIOGRAPHIC.
- `hanushek_1986` — Hanushek, E. A. (1986). The Economics of Schooling: Production and Efficiency in Public Schools. Journal of Economic Literature 24(3):1141–1177. **Identifier:** No DOI. JSTOR stable URL: https://www.jstor.org/stable/2725865. **Status:** BIBLIOGRAPHIC — AMBIGUOUS AS CITED (docs say only “Hanushek” without year/title; this is the standard candidate work).
- `jayachandran_2014` — Jayachandran, S. (2014). Incentives to teach badly: After-school tutoring in developing countries. Journal of Development Economics 108:190–205. **Identifier:** DOI 10.1016/j.jdeveco.2014.02.008. **Status:** VERIFIED PRIMARY TEXT.
- `kim_lee_2010` — Kim, S. & Lee, J.-H. (2010). Private Tutoring and Demand for Education in South Korea. Economic Development and Cultural Change 58(2):259–296. **Identifier:** DOI 10.1086/648186. **Status:** ABSTRACT-ONLY (full text paywalled).
- `tansel_bircan_2006` — Tansel, A. & Bircan, F. (2006). Demand for education in Turkey: A tobit analysis of private tutoring expenditures. Economics of Education Review 25(3):303–313. **Identifier:** DOI 10.1016/j.econedurev.2005.02.003. **Status:** VERIFIED PRIMARY TEXT (working-paper version; published version bibliographically verified).
- `todd_wolpin_2003` — Todd, P. E. & Wolpin, K. I. (2003). On the Specification and Estimation of the Production Function for Cognitive Achievement. The Economic Journal 113(485):F3–F33. **Identifier:** DOI 10.1111/1468-0297.00097. **Status:** VERIFIED BIBLIOGRAPHIC.
- `becker_human_capital` — Becker, G. S. (1964; 3rd ed. 1993). Human Capital: A Theoretical and Empirical Analysis, with Special Reference to Education. New York: Columbia University Press / NBER; 3rd ed. Chicago: University of Chicago Press. **Identifier:** No DOI. 3rd ed. 1993, University of Chicago Press, ISBN 978-0-226-04119-3 (ISBN via OpenLibrary edition record); 1st ed. 1964 Columbia UP/NBER. **Status:** BOOK — BIBLIOGRAPHIC (not read).
- `mincer_1974` — Mincer, J. (1974). Schooling, Experience, and Earnings. New York: NBER / Columbia University Press. **Identifier:** No DOI. NBER/Columbia University Press, 1974; ISBN 0-87014-265-8 / 978-0-87014-265-9 (OpenLibrary edition record). **Status:** BOOK — BIBLIOGRAPHIC (not read).
- `tullock_1980` — Tullock, G. (1980). Efficient Rent-Seeking. In J. M. Buchanan, R. D. Tollison & G. Tullock (eds.), Toward a Theory of the Rent-Seeking Society, pp. 97–112. College Station: Texas A&M University Press. **Identifier:** No DOI for the 1980 original. Book: Texas A&M University Press, 1980, ISBN 0-89096-090-9 / 978-0-89096-090-5 (OpenLibrary record); 2001 reprint chapter DOI 10.1007/978-1-4757-5055-3_2. **Status:** BIBLIOGRAPHIC (1980 original not read; reprint record verified).
- `oecd` — OECD — Organisation for Economic Co-operation and Development (PISA programme; see PISA entries for specific DOIs). **Identifier:** Covered by PISA DOIs above; general OECD data: https://data.oecd.org/. **Status:** INSTITUTIONAL DATA SOURCE — no standalone DOI (inventory placeholder “OECD+3” excluded).
- `uis` — UNESCO Institute for Statistics (UIS). Education statistics (UIS Data Centre / SDG 4 indicators). **Identifier:** No DOI. Provider: https://uis.unesco.org/. **Status:** INSTITUTIONAL DATA SOURCE — no DOI (inventory placeholders “UIS+2” excluded).
- `world_bank` — World Bank. World Development Indicators / Education Statistics (EdStats) and country documents. **Identifier:** No DOI. Provider: https://data.worldbank.org/ ; https://databank.worldbank.org/. **Status:** INSTITUTIONAL DATA SOURCE — no DOI (inventory placeholders “World Bank+2” excluded).
- `bray_1999` — Bray, M. (1999). The Shadow Education System: Private Tutoring and its Implications for Planners. Fundamentals of Educational Planning No. 61. Paris: UNESCO IIEP. **Identifier:** No DOI. Publisher: UNESCO IIEP, Paris (ISBN not independently verified in this pass). **Status:** VERIFIED BIBLIOGRAPHIC (peer-reviewed review record).
