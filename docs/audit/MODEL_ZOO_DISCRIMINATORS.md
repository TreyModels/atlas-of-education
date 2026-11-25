# MODEL_ZOO_DISCRIMINATORS — engine probes EP-1/EP-2, model-zoo protocol (both modes), and the A/R formalism

Owner lane: `engine-core` (design-only) · 2026-11-25 · branch `research/contest-audit-v2-2026-11-25`
**Revision v2, superseding commit `6e780c2`** after the Codex reply (Lead-relayed, 2026-11-25). Status:
**DESIGN ONLY — NOT PREREGISTERED-FINAL, NOT RUN.** No engine change and no box job in this revision.

Inputs: `PAPER_D_EQUATION_AUDIT.md` (D1–D9), `PAPER_C_MODEL_GAP.md` (S/L/G/time/supply-form extensions),
`MODEL_ZOO_SCOPE.md` (protocol draft), `PAPER_C_CONFIRMATORY_PREREG.md` (draft under review),
`SCIENTIFIC_CLAIM_LEDGER.md` rows MZ-01…MZ-04 / EV-01…EV-03, `TUTORING_DATA_INVENTORY.md`,
`verification/lean/LeanStarter.lean` + `verification/lean/Atlas/{Definitions,Claims}.lean`.
Engine pin `846c9e0` (core `e111397b…8e71`); canonical spec `docs/audit/canonical_spec.json`.

---

## 0. What changed in v2 (Codex corrections, all adopted)

1. **"Kaplan" is likely Bryan Caplan, not a test-prep company.** Row 8 of the zoo is replaced by the
   **Caplan signalling/human-capital-critique model**, tagged **V (unverified citation)**; the primary source is
   *probably* *The Case Against Education* (2018) — must be checked; if "Kaplan" means something else, §5.1 says what
   changes (Kaplan, Inc. = an industry supplier, not a general theory; Kaplan–Meier = an estimator, not a model).
2. **Protocol = both modes**: (A) *competing* models tested against the same evidence with pre-declared discriminating
   moments, and (B) *complementary modules* combined in one mechanism-rich model. Decision vocabulary is
   **holds / fails / indeterminate / not-testable**, never "the model is wrong" (§6–§7).
3. **D1/D2 are reclassified as ENGINE PROBES, not named-theory discriminators.** A demand-regression omission of S
   does **not** imply zero true response — the Lean omission lemmas are *definitional invariance*
   (`Atlas/Claims.lean:129–148`), i.e. the classical equation cannot see the channel, not that the channel is absent.
   And `q0` shifts **public and private** school quality, so it cannot isolate public S. Replaced by:
   * **EP-1** — a matched **public-feedback intervention** with a **no-effect toggle / negative control** (§2);
   * **EP-2** — own-access × firm-constraint interaction with **baseline-matched seeds**, a **fixed `own_share`
     denominator** with explicit contest-prep classification, and **absolute own/firm quantities** (§3);
   * **Seeds 0–7 are EXPOSED/exploratory** (used by Pilot-0 v3) and are excluded from confirmatory inference; the
     confirmatory seed set is the independent block **100–131 (32 matched seeds)**.
4. **A/R formalism adopted** and shared with the Lean starter: **A = achieved learning**, **R = required
   proficiency/cutoff** (fixed threshold *or* endogenous rank), **gap = max(0, R − A)** — definitionally the Lean
   `gap (required achieved : Nat) := Nat.max 0 (required - achieved)` (`LeanStarter.lean:8`), with capacity
   feasibility `Feasible required capacity := required ≤ capacity` (`LeanStarter.lean:25`). All model definitions and
   probe outcomes use A/R/gap; the Paper C/D equations and the machine-checked lemmas share one vocabulary (§1.1).
5. The unfalsifiable/data-blocked list is retained and now states explicitly: **empirical validation requires external
   observations**; engine runs are mechanism plausibility only (§8).

---

## 1. Conventions

### 1.1 The A/R vocabulary (shared with Lean)

| symbol | definition (engine units) | engine object / key | Lean object |
|---|---|---|---|
| **A** | achieved learning: cumulative grade-equivalents at a decision point | `k['L']`, `E.ALL['L']`, `L6`, `L9` (and `L12` after the wave-2 gate-snapshot extension) | `Nat`-encoded learning in the exact prototype; units documented in `Atlas/Definitions.lean` |
| **R** | required proficiency/cutoff: **(a) fixed threshold** (`fixed_bar` gate `bar`; MPL `mpl_primary`/`mpl_lower`) or **(b) endogenous rank** (contest/quota seat rank: the k-th competitor score; admission probability via Plackett–Luce) | gate `bar`, `contest_seats` rank, `cut`/`cut_adm`, `sdg4.py:48–56` MPL thresholds | fixed-threshold predicate vs rank predicate; `Gate`/`seatCount` in `Atlas/Definitions.lean` |
| **gap** | `max(0, R − A)` | computed per child from A and the gate's R; expected vs realised gap reported separately | `gap R A` (`LeanStarter.lean:8`); `gap_eq_zero_of_met`, `gap_pos_of_shortfall` |
| **capacity** | seats, student time, teacher hours | seats (`contest_seats`), `E._cash` (cash capacity), student/teacher time after the wave-2 extension | `Feasible required capacity` (`LeanStarter.lean:25`), `remainingCapacity` (`:31`) |

Rules: (i) never compare an A across units without stating the grade-equivalent scale; (ii) fixed-R and rank-R tests
are separate outcomes (fixed-R gap-closing is a human-capital prediction; rank-R order preservation is a positional/
signalling prediction); (iii) the Lean prototype is exact integer/rational — engine floats are reported separately as
REPRODUCED SIMULATION, not as proofs (claim status is recorded in `docs/audit/LEMMA_LEDGER.md`).

### 1.2 Run conventions

| item | value |
|---|---|
| engine pin | commit `846c9e0`, core sha256 `e111397bd8a50f94e82bb77715f236ee3d5c0bf863a23d84afdf1c6c71fa8e71`, frozen spec sha (re-pinned `e5ddef6b…`), runner sha — all in every manifest |
| base params | `docs/audit/canonical_spec.json` → `params.HK.primary` (canonical HK gates fixed; L not varied in probes) |
| modules | `[PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()]` |
| N / T / measure_from | N=600 screening, N=1500 confirmatory (per draft prereg); T=46, measure_from=18 |
| **seeds** | **0–7 = EXPOSED / exploratory only** (Pilot-0 v3, N=1500); **confirmatory = 100–131 (32 matched seeds)**, identical seed sets across cells of a contrast, paired per-seed differences; no seed may appear in both blocks |
| regimes | **v3 code values** (authoritative; the runner docstring is stale — see §10): `market_only` = own_ban .95, pay_ratio .55, monitoring .2, pay_gap (h≈.0072); `own_open_gap` = own_ban 0, pay_ratio .55 (h=.144); `own_open_incentive` = own_ban 0, pay_ratio 1.2, monitoring .2, incentive (h=.32); `own_open_gap_firm_ban` = own_open_gap + firm_ban .9 |
| assertions | `E.unfired_events == []`; manipulation checks per probe; binding/no-op assertions (h, own access, S moved); any failure ⇒ cell reported invalid, not silently dropped |
| inference | paired per-seed differences, seed-MC sd and 95 % CI; MDE declared pre-run; estimate below MDE ⇒ **indeterminate**, not "no effect"; Holm within a declared family |
| determinism | same seed ⇒ bit-identical engine run; event-keyed RNG (contract §7) makes arms share exogenous draws |

### 1.3 Outcome keys (current + required additions)

**Current** (all in `E.R`, most in module `summary()`; exact names unchanged): `tut_rate`, `tut_k12_rate`,
`tut_g12_rate`, `tut_by_grade`, `tut_by_q`, `tut_k12_rate_by_q`, `tut_k12_spend`, `tut_k12_spend_by_q`,
`tut_own_by_grade`, `tut_firm_by_grade`, `own_share`, `firm_price`, `firm_rev`, `contest_spend_now`,
`contest_resource_cost`, `contest_tax_paid`, `gov_tut_receipt`, `q_pub`, `withheld`, `ptr`, `teacher_pay`,
`pub_spend`, `pub_budget`, `rationed`, `priv_share`, `elite_share`, `track_share`, `elite_prize_mean`,
`track_prize_mean`, `completion_*`, `mpl_primary`, `mpl_lower`, `parity_*`, `learning_poverty`, `mean_years`,
`L6`/`L9` (per child, `E.ALL`), `elite`/`q`/`track` (`E.ALL`), `inc_by_cred`, `formal_by_cred`, `floor_skilled`.

**Required additive series for the probes (design; no numerics change):** `own_count`, `firm_count`,
`contest_only_count`; `own_spend`, `firm_spend`, `contest_only_spend`; `own_share_financial`
(= `own_count/(own_count+firm_count)`, financial tutoring only, contest-only pupils excluded);
`contest_prep_class` (0 none / 1 own / 2 firm / 3 contest-only / 4 own+contest / 5 firm+contest);
per-quintile versions of `own_count`/`firm_count`/`own_spend`/`firm_spend`; A/R series: `A_mean`, `gap_mean`,
`gap_by_q`, and pass/admit counts at fixed-R and at rank-R gates. These are reporting-only additions in
`tutoring.py` (reporting block) and `core.py`/`sdg4.py` (A/R snapshots); they must not change any probability path.

---

## 2. EP-1 — matched public-feedback intervention (ENGINE PROBE, not a theory discriminator)

**Purpose.** Test whether the *engine's* school-supply channel produces the substitution/learning response that a
public-only effective-preparation lever should generate, with a matched no-effect control so that a null result is
unambiguous. This is a probe of mechanism implementability — it does **not** test or rank any named theory. (The
classical demand equation cannot see S by construction; the Lean omission lemma is definitional invariance,
`Atlas/Claims.lean:129–132`.)

**Design status:** **NOT RUNNABLE TODAY** — the engine has no positive public-school effort/preparation lever
(`PAPER_C_MODEL_GAP.md` §3.1; `q0` is a both-sector quality bundle, so it is *not* a valid substitute; Codex confirmed).
The design is ready for the wave-2 `school_feedback` extension.

| arm | lever | requirement | role |
|---|---|---|---|
| **C0** | none | baseline cell | control |
| **P** | `school_feedback = x` with `feedback_intensity = 0` (declared inert toggle), or a matched dummy that consumes the same teacher marking time | **must be bit-identical to C0** on every declared outcome; pre-run assertion | **no-effect negative control** (validates the comparison) |
| **T** | `school_feedback = x` with `feedback_intensity = 1`, **public basic schools only**, costed in teacher marking time | manipulation check: S > 0 and teacher marking hours increase | treatment |
| **B** | `q0` raised to give the same average school-quality increase (both sectors) | declared bundle contrast, not treatment | shows why `q0` cannot isolate public S (contamination demonstration) |

* Matched aspects: same seeds (100–131), same cohorts, same teacher-time budget consumed in P and T (so any time-cost
  channel is matched and cannot explain a T−P difference), same computational path; P and T differ only in
  `feedback_intensity`.
* **Primary outcome:** Δ K–12 tutoring participation, T − C0, with the P − C0 contrast as the negative control.
* **Secondary (Holm):** Δ `tut_k12_spend`; Δ absolute `own_count`/`firm_count` and spends (not just shares);
  Δ `A` (`L6`,`L9`), Δ fixed-R gap-close rate and rank-R admission probability; Δ `gap_by_q`; teacher marking hours and
  any binding time/capacity indicator.
* **Validating conditions:** P ≡ C0 bit-identical; S moved in T; no `unfired_events`; placebo and treatment consume the
  same declared teacher-time budget.
* **Decision rule:** probe is *informative* if validating conditions hold. Then:
  **mechanism present** iff Δ participation ≤ −MDE_participation **and** Δ spend ≤ −MDE_spend with CI excluding 0;
  **mechanism absent in this geometry** iff |Δ| < MDE with a CI that excludes the mechanism's minimum effect;
  **indeterminate** otherwise (extend seeds within 100–131, never reuse 0–7). A "mechanism absent" result is an engine
  limitation to report, **not** evidence about the world or about a theory.
* **A/R reading:** the fixed-R prediction is `gap`-closing (A↑ ⇒ gap↓) **and** tutoring participation↓ (school
  substitutes for bought preparation); the rank-R prediction is admission-probability↑ with rivals' A fixed. Report
  both fixed-R and rank-R outcomes; do not pool them.
* Compute (once the extension lands): C0/P/T/B = 4 arms × 32 seeds × N=600 ≈ 128 runs ≈ **45–50 CPU-min** host
  (measured HK N=300/T=46 = 9.1 s ⇒ N=600 ≈20–23 s/run); a 16-seed screening subset (100–115) halves it.

---

## 3. EP-2 — own access × firm constraint, with fixed denominators and absolute quantities (ENGINE PROBE)

**Purpose.** Establish how the engine's two shadow-education suppliers reallocate when one is constrained, under
baseline-matched seeds — an **engine probe**, not a test of any named model. It supplies the mechanism evidence a later
model-zoo test would need, with the measurement defects of the earlier D2 fixed.

**Status:** switches exist, but the probe is **NOT CONFIRMATORY-RUNNABLE** until the §1.3 additive series land
(fixed `own_share` denominator + contest-prep classification + absolute counts/spends). The existing `own_share`
denominator is `own/(any tutored)` where `tut_any` includes contest-prep pupils (`tutoring.py:429`), so it is
contaminated; and only shares are available.

### 3.1 Design (2×2, baseline-matched)

| cell | `own_ban` | `firm_ban` | role |
|---|---|---|---|
| E00 | 0.95 (own channel ~closed) | 0.0 | own-closed, firm-open (baseline) |
| E01 | 0.95 | 0.9 | own-closed, firm-constrained |
| E10 | 0.0 (own open) | 0.0 | own-open, firm-open |
| E11 | 0.0 | 0.9 | own-open, firm-constrained |

Fixed: `q0=1.0`, `p_firm=0.08`, canonical HK base, N=600 (screening) / N=1500 (confirmatory), **seeds 100–131
matched across all four cells**; pay_ratio/monitoring from the v3 code values (`.55`/`.2`) so withholding is active
when own_ban=0 (h=.144) and near-off when own_ban=.95 (h≈.0072).

* **Primary outcome:** `own_share_financial` (own vs firm among financial tutoring, contest-only pupils excluded),
  E11 − E10 with E01 − E00 as the contamination-matched control (both have the firm constraint; only own access
  differs).
* **Secondary (Holm):** Δ absolute `own_count`, `firm_count`, `own_spend`, `firm_spend`, `contest_only_count`,
  `contest_only_spend`; Δ K–12 participation and spend; Δ A/R outcomes (`gap_by_q`, rank-R admission probability);
  `firm_rev`. **`firm_price` is reported but NOT used as mechanism evidence** (`firm_ban` mechanically raises the
  price base, `tutoring.py:96–101`).
* **Interaction prediction (engine-mechanism):** the firm constraint's effect on *participation* is larger (more
  negative) when the own channel is closed (E01−E00) than when open (E11−E10), because displacement absorbs demand in
  E11. Pre-register the difference-in-differences sign: `ΔΔ participation = (E01−E00) − (E11−E10) < 0`.
* **Decision rule:** displacement present iff `Δ own_share_financial(E11−E10) ≥ +MDE_share` and the DiD interaction is
  negative with CI excluding 0; absent iff both < MDE with CIs excluding the mechanism minima; indeterminate otherwise.
  Binding assertions: E10/E11 `withheld > 1e-3`; E00/E01 `withheld < 5e-3`; the classification reconciles
  `own_count + firm_count + contest_only_count == tutored_count` exactly.
* **A/R reading:** access to the own channel should reduce the fixed-R `gap` for cash-constrained households (they can
  buy back withheld S); rank-R incidence should shift toward higher quintiles if firm rationing is income-based.
* Compute: 4 cells × 32 seeds × N=600 ≈ 128 runs ≈ **45–50 CPU-min**; 16-seed screening (100–115) ≈ 22–25 CPU-min.

---

## 4. Runnability matrix and required engine additions

| item | status | blocker |
|---|---|---|
| EP-1 | design-ready | wave-2 positive public-school S lever (`school_feedback`, teacher marking time) + matched placebo semantics; no engine change in this revision |
| EP-2 | design-ready | §1.3 additive reporting series + contest-prep classification; switches already exist; no probability change |
| Model-zoo *competing* tests (Mode A) | needs EP-1/EP-2 + external data | see §6–§8; many moments data-blocked |
| Model-zoo *complementary modules* (Mode B) | design-ready as a module stack; estimation needs external data | model fitting is not runnable in-engine as "evidence" |

**No run may start** until (i) the Paper C prereg draft is amended per its own 8 blocking items + Codex protocol/
Kaplan confirmation, (ii) this probe design is signed off, (iii) seeds 100–131 + engine/spec/runner hashes are frozen,
(iv) Commander allocates host/box capacity.

---

## 5. Model zoo (revised)

### 5.1 Row 8 — "Kaplan": Bryan Caplan, **V (unverified)**

* Most likely **Bryan Caplan**, *The Case Against Education* (2018) and related work: education largely **signals**
  rather than produces skills; **sheepskin/credential discontinuities**; **low returns to marginal schooling**;
  large private returns with small social skill returns; education as a partly consumption/credential good.
  **Primary source citation is UNVERIFIED** (tag **V**); per the programme's attribution rule the citation must be
  checked before any use. The Codex reply says *probable*, so the row is provisional.
* Testable predictions (engine/probe-level, with A/R): (i) **credential discontinuity**: income/formal-hiring jumps at
  completion (credential boundaries) while A is continuous — compare `inc_by_cred`/`formal_by_cred` steps against the
  smooth ∇A gradient; (ii) **signalling share** rises with cohort education/credential abundance (premia shrink as
  credentials expand) — needs a massification scenario; (iii) **low marginal schooling returns** near completion —
  sheepskin effect larger than the last-year learning effect on earnings/hiring.
* What it discriminates against: Becker/Hanushek (skills drive outcomes), Mincer (smooth log-linear schooling return).
  Complementary to Spence (both signalling; different welfare/consumption claims); the engine cannot separate their
  welfare implications without a welfare block.
* **If "Kaplan" is not Bryan Caplan:** (a) *Kaplan, Inc.* (test-prep company) is an **industry supplier case**, not a
  general model → becomes a supply-form module datum (firm entry/price/market conduct), not a zoo theory row;
  (b) *Kaplan–Meier* is an estimator → §9 methods, not a model row. Record the ambiguity and do not attribute
  signalling claims to a different Kaplan.

### 5.2 Zoo table (10 rows; 2–3 observable predictions each; V = citation unverified)

Evidence verdicts use the programme's verified limitations (`SCIENTIFIC_CLAIM_LEDGER.md` EV-01…EV-03): PISA 2018/2022
has participation/hours by ESCS for HK/PH/CN but **no expenditure and no own-vs-firm item**; **SEA-PLM 2019 has no
tutoring item** (refuted route); **SEA-PLM 2024 framework item PA18A–D** is the candidate supply-form route (text
verified, dataset/linkage V); CEPS China expenditure; **DHS E1–E8 cannot test the zoo** (no tutoring/learning/gate/seat/
time/earnings/expenditure) and is auxiliary descriptive evidence at most.

| # | model (status) | observable predictions (2–3) | discriminates against | engine/outcome keys | A/R reading | data verdict |
|---|---|---|---|---|---|---|
| 1 | **Becker human capital** | (i) higher returns/capacity ⇒ more investment; (ii) A rises with school/tutoring inputs and gaps close at fixed R; (iii) borrowing constraints bite | Spence/Caplan (flat A), Hirsch (rank-only), Bray (demand-only) | `completion_*`, `mpl_*`, `L6/L9`, `gap_*`, `inc_by_cred` | A↑ closes fixed-R gap | PROXY (DHS completion by wealth; no earnings) |
| 2 | **Mincer returns** | (i) log earnings linear in schooling; (ii) smooth returns (no sheepskin jumps); (iii) stable returns across supply regimes | Caplan/Spence (discontinuities), Becker (investment dynamics) | `inc_by_cred`, `formal_rate`, `theta_L`, `cred_step` | smooth A/credential gradient | **UNFALSIFIABLE now** (no DHS earnings; engine-simulated returns are not empirical) |
| 3 | **Spence signalling/screening** | (i) credential premium with flat A; (ii) effort rises with gate stakes without learning gain; (iii) credential floors persist | Becker/Hanushek, Hirsch (demand mechanism) | `inc_by_cred`, `formal_by_cred`, `floor_skilled`, `contest_e_mean`, `L9` | rank-R preserved, fixed-R gap unchanged | PROXY (PISA skills + education; DHS lacks skills) |
| 4 | **Hanushek production function** | (i) school inputs raise A; (ii) diminishing returns; (iii) class size/teacher quality matter | Hirsch/Caplan (A flat), time-allocation (capacity) | `q_pub`, `ptr`, `teacher_pay`, `mpl_*`, `L6/L9` | A↑ ⇒ fixed-R gap↓ | PROXY (PISA/SEA-PLM school questionnaire; DHS no school inputs) |
| 5 | **Hirsch positional competition** | (i) prep rises with fixed-seat intensity while A flat; (ii) spending tracks relative rank not q; (iii) seat expansion lowers effort | Becker/Hanushek (absolute skill), Bray (positional vs demand) | `contest_e_mean`, `tut_k12_rate`, `elite_share`, Q5−Q1 gap | rank-R not fixed-R | PROXY (needs gate/seat + spend; PISA/CEPS) |
| 6 | **Bray shadow-education demand** | (i) participation rises with exam stakes; (ii) falls with household capacity; (iii) responds to S | Hirsch (mechanism), human-capital supply models | `tut_k12_rate`, `tut_g12_rate`, `tut_k12_rate_by_q` | demand side of A/gap | FALSIFIABLE-PARTIAL if PISA/CEPS items verified (participation/hours only) |
| 7 | **Biswal / Jayachandran withholding** | (i) h>0 when pay gap + sellable; (ii) own-teacher share rises with h; (iii) banning sell-back lowers h and own supply | Bray, Caplan/Spence, Becker | `withheld`, `own_share_financial`, absolute `own_count`, `teacher_pay` | S lower ⇒ A lower unless bought back | **theory-only magnitudes** (no own-provider/teacher-pay data; engine mechanism only) |
| 8 | **Caplan signalling critique (Kaplan = Bryan Caplan, V unverified)** | (i) sheepskin/credential discontinuities with continuous A; (ii) signalling share changes with credential massification; (iii) low marginal-schooling returns | Becker/Hanushek/Mincer (skills/smooth returns), Spence (welfare/consumption claims) | `inc_by_cred`, `formal_by_cred`, Vc credential steps, `gap` vs credential | rank-R/credential jumps vs fixed-R A | PROXY/V: citation unverified; engine can simulate sheepskin, external data needed for validation |
| 9 | **China state provision / DL model** | (i) state S crowds out private tutoring; (ii) for-profit ban shifts supply to own/residual; (iii) state expansion lowers household shadow share | Bray/industry-supply models, withholding | q0/budget → `tut_k12_rate`, `own_share_financial`, `firm_rev`, `household_share_spending` | public S raises A; fixed-R gap↓, private demand↓ | PROXY (CEPS China + 2021 DL timing; DHS no tutoring) |
| 10 | **Household time allocation** | (i) time, not cash, binds tutoring; (ii) contest prep crowds out study time; (iii) time binds more in higher grades | all cash-only demand models | **none** (no time variables today); needs wave-2 time budget | capacity-feasibility, not gap alone | **NOT-TESTABLE now** (no time-use data; engine lacks time budget) |

---

## 6. Zoo protocol: both competing and complementary

### 6.1 Mode A — competing models on the same evidence

* Every model declares **2–3 observable predictions with a sign/magnitude** on named A/R outcomes before any run.
* A **discriminating moment** is usable only if two models predict *different signs/magnitudes* for the *same*
  parameter change (see §7); otherwise the moment is descriptive, not discriminating.
* Same evidence = the EP-1/EP-2 cells + external data (ILSA/CEPS); results reported for **all** models × moments
  (family-wise), no selective reporting.
* Decision: a model **holds** if its pre-declared predictions are confirmed within CI/MDE; **fails** the specific
  pre-declared falsification test if the opposite sign is established; **indeterminate** if underpowered or mixed;
  **not-testable** if the lever/data is absent. A fail is a *prediction* failing, not "the model is wrong".

### 6.2 Mode B — complementary modules in one mechanism-rich model

The competing models are also **modules** that can coexist and are jointly needed by Paper C:

| module | source model(s) | what it adds to the engine (design mapping) |
|---|---|---|
| production of A | Becker + Hanushek | A accumulation from S, tutoring, family, ability (C1–C2 in `PAPER_D_EQUATION_AUDIT.md` §5) |
| positional/rank R | Hirsch | fixed-seat contests, rank-R admission, contest prep (C9) |
| credential/signalling value | Spence + Caplan | credential steps in beliefs/values, sheepskin, signalling share (Vc steps, `B`) |
| supplier/withholding | Biswal/Jayachandran | teacher rent extraction, own-teacher supply (C8) |
| market supply | Bray + industry/state | firm entry/price/profit + state provision (C6–C7) |
| time/capacity | household time allocation | Feasible constraints (C5a/C5b) |

Protocol: inspect/fit **nested module stacks** on the same evidence; a module is retained if it improves the
pre-declared fit/moment match without violating the others' falsifiers; do not declare a single "winning" model. This
is the "complementary modules" half of the Codex protocol, and the formal basis of Paper C's mechanism-rich model.

---

## 7. Discriminating moment families (A/R terms) and decision rules

| family | moment / manipulation | separates | A/R formulation | engine/probe |
|---|---|---|---|---|
| **M-A fixed-R gap-closing** | school input S↑ | Becker/Hanushek vs Caplan/Spence (flat A) / time-capacity | A↑ ⇒ `gap(R_fixed, A)`↓ and pass rate↑ | EP-1 (needs S lever) |
| **M-B rank-R competition** | gate share/contest intensity↑ | Hirsch/Spence/Caplan (rank/credential) vs Becker (absolute skill) | rank-R probability changes with rivals' A, not own A alone; effort↑, A flat | EP-2 + existing contest cells |
| **M-C supplier access** | own_ban × firm_ban | Biswal/state/market-supply vs single-good demand models | own/firm absolute quantities and `gap_by_q` reallocation | EP-2 |
| **M-D credential discontinuity** | credential boundary vs A continuity | Caplan/Spence vs Becker/Mincer | income/hiring jump at credential completion while `gap`/A continuous | engine sheepskin simulation; external earnings data needed |
| **M-E time/capacity** | student/teacher time binding | time-allocation vs all cash-only models | `Feasible` constraints bind; crowding-out | not-testable now |
| **M-F state vs market** | q0/budget/firm_ban | China state provision vs Bray/industry supply | S↑ ⇒ A↑, fixed-R gap↓, private demand↓ | EP-1 + EP-2; CEPS proxy |

**Holds / fails / indeterminate / not-testable (binding wording):** identical thresholds and MDE discipline for every
model; an unrejectable prediction is recorded as **not-testable**, never as evidence for the model. Underpowered
outcomes are **indeterminate**; only a pre-declared falsification test with the opposite established sign is **fails**.

---

## 8. Data status, unfalsifiable list, and the empirical-validation rule

* **Empirical validation requires external observations.** Engine runs are REPRODUCED SIMULATION (mechanism
  plausibility); the Lean statements are arithmetic/definitional (identity, omission-invariance, exact finite PL), never
  empirical. No model may "win" on engine or Lean evidence alone; DHS/ILSA/CEPS comparisons are a separate evidence
  layer and must be cited with source, survey year, population and denominator.
* **Falsifiable-partial routes:** PISA 2018/2022 participation/hours by ESCS (HK/PH/CN; no expenditure, no
  own-vs-firm); SEA-PLM 2024 PA18A–D supply-form item (**candidate** — framework text verified, dataset/linkage V;
  SEA-PLM 2019 has *no* tutoring item, earlier route refuted); CEPS China expenditure; KOSTAT Korea provider-type.
* **UNFALSIFIABLE / NOT-TESTABLE now (retained):** (i) **time allocation** (no engine time budget, no time-use data);
  (ii) **Mincer returns** (no earnings in DHS; engine simulation is not evidence); (iii) **withholding magnitudes /
  own-vs-firm provider mix** (no own-provider/teacher-pay data; engine mechanism only); (iv) **firm profits/entry**
  (no firm-market data; engine price/entry rules are mechanical constructs); (v) **CES substitution sign / dynamic
  complementarity** (engine production is additive today; needs `production='ces'` extension); (vi) **welfare ranking**
  of supply regimes (no welfare block, no empirical welfare weights). These are pre-registerable tests, not results;
  later documents must not imply they were tested.

---

## 9. Pre-registration checklist (revised)

1. **Engine pin** (commit `846c9e0`, core `e111397b…8e71`), spec sha (`e5ddef6b…`), runner sha; every manifest records
   all three; `unfired_events==[]` per run.
2. **Seeds:** exploratory 0–7 (EXPOSED, Pilot-0 v3, excluded from confirmatory inference); confirmatory 100–131
   (32 matched) frozen before any run; seed lists in the manifest; no overlap.
3. **Cells:** EP-1 arms (C0/P/T/B) and EP-2 2×2 (E00/E01/E10/E11) with exact overrides and N=600 (screening) /
   N=1500 (confirmatory); any additional cell declared before the run (no post-hoc cells).
4. **One primary outcome per probe** (EP-1: participation T−C0; EP-2: `own_share_financial` E11−E10); ordered
   secondary family with Holm; all outcomes reported.
5. **Predicted signs + MDE** for every primary and key secondary (EP-1: Δparticipation ≤ −MDE and Δspend ≤ −MDE;
   EP-2: Δown_share ≥ +MDE and negative DiD interaction).
6. **Validating conditions:** EP-1 placebo P bit-identical to C0; S moved in T; matched teacher-time budget;
   EP-2 `withheld` assertions and exact classification reconciliation (`own+firm+contest_only = tutored`).
7. **Measurement definitions locked:** `own_share_financial` denominator (financial tutoring only), contest-prep
   classification, absolute counts/spends, A/R outcomes (fixed-R gap vs rank-R probability reported separately).
8. **Contamination declarations:** `q0` = public+private bundle (never used as clean S; EP-1 B-arm demonstrates it);
   `firm_price` mechanical; `tut_firm_by_grade` mixing; own-teacher availability tied to `own_ban`.
9. **Protocol both modes:** Mode A competing predictions (all models × moments, family-wise) and Mode B complementary
   module stack; decisions holds/fails/indeterminate/not-testable only.
10. **Evidence layering:** engine simulation vs Lean proofs vs external data kept separate; "empirical validation
    requires external observations" stated in the prereg.
11. **Kaplan resolution:** Caplan row stays **V** until the primary citation is verified; if it is a different Kaplan,
    the row is reclassified per §5.1 before any use.
12. **Compute envelope + process gate:** EP-1 ≈45–50 CPU-min host once the S lever lands; EP-2 ≈45–50 CPU-min once
    the series land (16-seed screening halves both); no run before the Paper C prereg amendments + Codex protocol/
    Kaplan confirmation + Commander allocation; negative results preserved.

---

## 10. Gotchas / open items

* **Pilot-0 runner inconsistency:** `run_paperC_pilot0.py` module docstring says "96 runs / 3 supply regimes /
  pay_ratio=0.8", but committed v3 code has **4 REGIMES (→128 runs)** and `pay_ratio=0.55`, `monitoring=0.2`
  (matches commit `fbc1991`); the prereg must quote code + commit. Seeds 0–7 are therefore **exposed** in any case.
* **`q0` is not an S lever** (public+private bundle); only EP-1's public-only `school_feedback` can test S cleanly.
  The Paper C prereg draft's T1 (q0 0.85→1.15) is a *quality-bundle* test and must be relabelled (its own amendment 6);
  EP-1 supersedes it once the extension lands.
* **Existing `own_share` is contaminated** (`tut_any` includes contest prep, `tutoring.py:429`); EP-2 is confirmatory
  only after the fixed denominator + classification + absolute series land.
* **Rank-R vs fixed-R outcomes must not be pooled**; A/R vocabulary is binding for Paper C/D and the Lean lemmas.
* **Kaplan ambiguity (V):** do not attribute signalling claims to a non-Caplan Kaplan; keep the tag until verified.
* **Unfalsifiable items must stay flagged**; use "not-testable", not "no effect".
