# MODEL_ZOO_DISCRIMINATORS — pilot-ready D1/D2 designs and model-zoo discriminating moments

Owner lane: `engine-core` (design-only) · 2026-11-25 · branch `research/contest-audit-v2-2026-11-25`
Status: **DESIGN ONLY — NOT PREREGISTERED, NOT RUN.** No engine change, no box job. Companion to
`PAPER_D_EQUATION_AUDIT.md` (divergence tests D1–D9), `PAPER_C_MODEL_GAP.md` (S/L/G extension design),
`MODEL_ZOO_SCOPE.md` (model-zoo protocol draft) and `TUTORING_DATA_INVENTORY.md` (data availability).
Engine pinned at commit `846c9e0` (core.py sha256 `e111397b…8e71`); frozen canonical spec
`docs/audit/canonical_spec.json`; Paper C pilot runner `papers/shadow-education-contest/code/run_paperC_pilot0.py`
(regime anchor definitions). Everything here is **REPRODUCED SIMULATION or DESIGN**; no empirical claim.

---

## 0. TL;DR

* **A single 32-run confirmatory core** covers D1 (D1A/D1B) and D2 (D2A/D2B) at **N=600, T=46, seeds 0–7 matched**,
  reusing all four Paper C Pilot-0 **v3** cell definitions (Pilot-0 v3 is the 4-regime / 128-run design, N=1500,
  exploratory; here the same cells are re-executed at N=600 — **no new cell definitions in the 32-run core**). The only
  new cells are optional: the D1 q0=0.8 third S level (+8 runs) and the mechanism-grade D2 `market_only + firm_ban`
  arm (+8 runs).
* **Ten model-zoo candidates** are mapped to 2–3 observable predictions each, with the exact current outcome keys that
  can test them and a DHS/ILSA evidence verdict. Five **discriminating moment families** separate the models; five
  predictions are marked **UNFALSIFIABLE with current data/engine** (time allocation, Mincer returns in DHS,
  withholding magnitude/provider mix, Kaplan-type firm profits, exact CES substitution sign).
* **Nothing may run until the prereg checklist in §6 is signed off** (cells, seeds, outcomes, predicted signs,
  thresholds, multiplicity, engine/spec hashes, no-op binding assertions, exclusion rules).

---

## 1. Common design conventions (both tests)

| item | value |
|---|---|
| base params | `docs/audit/canonical_spec.json` → `params.HK.primary` (canonical HK gate list **fixed**; L is not varied in this design — L goes to a later Pilot-1) |
| modules | `[PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()]` |
| N / T / measure_from | **N=600, T=46, measure_from=18** (pilot uses N=1500; N=600 is the confirmatory budget) |
| seeds | **0–7, matched** (identical `EventRNG` streams; paired differences per seed) |
| runner pattern | one process per cell, per-seed JSONL checkpoints, atomic final JSON, `assert E.unfired_events == []` (mirror `run_paperC_pilot0.py`) |
| regimes (from the pilot runner code, not its docstring — see §7 gotcha) | `market_only`: `own_ban=.95, pay_ratio=.55, monitoring=.2, withhold_mode='pay_gap'`; `own_open_gap`: `own_ban=0, pay_ratio=.55, monitoring=.2, pay_gap`; `own_open_incentive`: `own_ban=0, pay_ratio=1.2, monitoring=.2, withhold_mode='incentive'`; `own_open_gap_firm_ban`: `own_open_gap + firm_ban=.9` |
| expected withholding under each regime | `h = h_max·max(0,1−pay_ratio)·(1−monitoring)·(1−own_ban)`: market_only **0.0072**, own_open_gap **0.144**, own_open_incentive **0.320**, firm_ban variant **0.144** |
| binding assertions (run invalid otherwise) | non-market cells: `withheld > 1e-3` and `own_share > 0.10`; all cells: `q_pub` monotone in `q0`, `firm_price > 0`, no `event_log` surprises |
| primary-outcome rule | **one pre-registered primary outcome per test**; the rest are a secondary family with Holm correction within family; report all cells, no selective reporting |
| pairing / inference | paired per-seed differences; report mean, per-seed SD, 95% CI (t with 7 df), and the paired sign count; no pooling across N |
| contamination notes to carry in every output | (i) `q0` scales **public and private** school quality (it is school-sector-wide, not public-only); (ii) `own_share`/`tut_firm_by_grade` mix contest-prep pupils with firm tutoring (`tut_any` includes `contest_e>1e-4`); (iii) `firm_price` is an **outcome** and under `firm_ban` its rise is partly *mechanical* (`p_firm·(1+firm_ban)`), so price is not mechanism evidence |

**Compute (measured, host, 1 process):** canonical HK N=300/T=46 = 9.1 s; scaling to N=600 ≈ 2.1–2.5× (candidate
count and seats double; PL quadrature grows with n) ⇒ **≈20–23 s/run**. The 32-run core ≈ **11–12 CPU-min** (≈6 min at
2 workers, ≈12 min at 1 worker); add 20 % margin → ~14 CPU-min. Mechanism-grade D2 (+16 runs) → ~18 CPU-min. Host-only
screening is cheap; a box allocation is optional, not required.

---

## 2. D1 — school supply S and tutoring demand (omitted-S divergence)

**Question.** Does the standard demand equation (inventory eq 58/65, no S) mispredict when school-supplied preparation
changes? **Mechanism-rich prediction:** S enters the tutoring demand through the marginal value of learning and through
substitution, so participation/spend fall as S rises and the income gradient attenuates; a school-blind demand equation
predicts no effect.

| cell | regime | overrides | runs | reuse status |
|---|---|---|---|---|
| D1A | `market_only` | `q0=1.0, p_firm=0.08` | 8 (seeds 0–7) | **cell definition reused from Pilot-0** (pilot N=1500; this is an N=600 re-execution) |
| D1B | `market_only` | `q0=1.2, p_firm=0.08` | 8 | **reused cell definition** |
| D1C *(optional)* | `market_only` | `q0=0.8, p_firm=0.08` | +8 | **NEW cell** (adds a third S level; only if the prereg wants a monotone response with a below-baseline point) |

**Primary outcome:** paired Δ K-12 tutoring participation (`tut_k12_rate`, D1B − D1A).
**Secondary (Holm):** Δ `tut_k12_spend`; Δ `tut_k12_rate_by_q` (income gradient); Δ `tut_k12_spend_by_q`; `own_share`;
`firm_price`; `q_pub` (manipulation check); `L6`, `L9`, `mpl_lower`, `completion_upper` (learning side); `contest_e_mean`.

**Predicted X (standard demand, no S):** `Δ participation ≈ 0`, `Δ spend ≈ 0` after S change; income gradient unchanged.
**Predicted Y (mechanism):** `Δ participation < 0`, `Δ spend < 0`; the fall is larger at the extensive margin for the
cash-constrained quintiles than for Q5 (gradient attenuation) because high-S substitutes for compensating tutoring.
Probe prior (N=300/T=30, not the design): overall participation .528→.491 (−3.7 pp), spend 145.5→135.9 (−6.6 %).

**Decision rule (pre-registered before running):**
* Y supported iff paired mean Δparticipation ≤ **−2.0 pp** and Δspend ≤ **−3 %**, each with 95 % CI excluding 0;
* X rejected iff also the CI excludes 0 (i.e. the "no effect" prediction is outside the interval);
* **indeterminate** if |Δparticipation| < 1.0 pp (underpowered: extend seeds to 16 rather than reinterpret);
* gradient attenuation is a secondary test: report Δ by quintile and the Q1–Q5 difference with CI; only claim it if the
  pre-registered ordering holds in ≥7/8 paired seeds.
**Manipulation check:** `q_pub` must rise with `q0` in the expected direction (`q = q0·min(1.25,(ptr_target/ptr)^.25)`,
`schools.py:49`); if q_pub is flat the cell is void. **Contamination caveat:** q0 also raises private quality → the claim
is about school-sector supply, not public-only S (isolating public S needs the wave-2 `school_prep` lever).

Runs: **16** (24 with D1C) ≈ 6 (9) CPU-min.

---

## 3. D2 — tutoring cap/ban: reduced-form vs withholding displacement

**Question.** Inventory eq 86 (reduced-form cap/ban) predicts lower tutoring spending and participation with no supplier
shift. The mechanism-rich model predicts **displacement**: a firm ban raises the firm price, collapses firm supply, and
shifts demand to the own teacher **iff sell-back/withholding is available** (`sell = 1−own_ban > 0`, `h>0`). The
discriminating part is not the total spend fall (both models predict some) but **supplier substitution and the
interaction with the withholding channel**.

### 3.1 Minimal D2 (fits the 32-run core)

| cell | regime | overrides | runs | reuse status |
|---|---|---|---|---|
| D2A | `own_open_gap` | `q0=1.0, p_firm=0.08` | 8 | **cell definition reused from Pilot-0** |
| D2B | `own_open_gap_firm_ban` | `q0=1.0, p_firm=0.08` (i.e. D2A + `firm_ban=0.9`) | 8 | **reused cell definition from Pilot-0 v3** (regime R4; N=600 re-execution) |

**Primary outcome:** paired Δ `own_share` (D2B − D2A).
**Secondary (Holm):** Δ `tut_k12_spend`; Δ `tut_k12_rate`; Δ `firm_price`; Δ `firm_rev`; Δ `tut_k12_rate_by_q`;
`contest_e_mean`; `withheld` (manipulation check); `L9`/`completion_upper` (learning side).

**Predicted X (reduced-form ban):** total spend falls roughly in proportion to the firm share; `own_share ≈ unchanged`;
relative price unchanged; participation falls uniformly.
**Predicted Y (displacement):** `own_share` jumps (probe: 0.53→0.98), firm-side spend collapses while own-teacher spending
rises (total spend falls less than the firm component), firm price rises, and participation falls **less** where the own
channel is open. Probe prior (N=300/T=30): own_share .528→.978, K-12 participation .776→.627, spend 165.0→118.1,
firm price 0.070→2.096.

**Decision rule:** Y supported iff paired Δ`own_share` ≥ **+0.20** with CI excluding 0, and the firm-revenue collapse
accounts for more than the total-spend fall (i.e. displacement absorbs part of it); X rejected iff both hold. The
**firm-price prediction is NOT used as evidence** (mechanical in `p_firm·(1+firm_ban)`, `tutoring.py:96-101`). If
Δ`own_share` < 0.05 → X not rejected (indeterminate mechanism in this regime).

### 3.2 Mechanism-grade D2 (recommended if 16 extra runs are affordable)

2×2 design isolating the withholding channel: **own channel** (`own_ban` 0.95 vs 0) × **firm ban** (0 vs 0.9), all at
`q0=1.0, p_firm=0.08`, 8 seeds = **32 runs**:

| cell | regime | purpose | reuse |
|---|---|---|---|
| D2A′ | `market_only` (own ≈ closed, h≈.007) | control: no own displacement channel | reused cell definition (Pilot-0 R1) |
| D2B′ | `market_only + firm_ban=.9` | ban without displacement | **NEW cell** (only regime/combination not already in Pilot-0 v3) |
| D2A | `own_open_gap` (own open, h=.144) | displacement channel active | reused (Pilot-0 v3 R2) |
| D2B | `own_open_gap + firm_ban=.9` | ban with displacement | reused (Pilot-0 v3 R4) |

**Key mechanism prediction (the discriminator vs a reduced-form cap):** the ban's participation loss is **larger when
the own-teacher channel is closed** (`own_ban=.95`), because there is no substitute supplier — i.e. the
`own-banned × ban` interaction on `tut_k12_rate` is negative. A reduced-form ban model predicts the same drop in both
arms (no supplier substitution). Pre-register the interaction sign and test it with the paired 2×2 contrast.
Runs: **32** ≈ 11–12 CPU-min (8 of them on a new cell, 24 re-executing pilot v3 cells at N=600).

---

## 4. The 32-run confirmatory core (D1 + D2 minimal)

| # | cell | regime | q0 | p_firm | seeds | purpose | new? |
|---|---|---|---|---|---|---|---|
| 1 | D1A | market_only | 1.0 | 0.08 | 0–7 | D1 baseline | reused cell |
| 2 | D1B | market_only | 1.2 | 0.08 | 0–7 | D1 S↑ | reused cell |
| 3 | D2A | own_open_gap | 1.0 | 0.08 | 0–7 | D2 no ban | reused cell |
| 4 | D2B | own_open_gap_firm_ban | 1.0 | 0.08 | 0–7 | D2 ban | reused cell (Pilot-0 v3 R4) |

= **32 runs, N=600/T=46, seeds 0–7 matched**, ≈11–12 CPU-min (≈6 min at 2 workers). This is a *confirmatory-ready*
design: **all four cells are Pilot-0 v3 design points re-executed at N=600**, so no new design space is introduced and no
exploratory cherry-picking is possible. Optional add-ons: D1C q0=0.8 (+8 runs, one new cell) and §3.2 mechanism-grade D2
2×2 (+32 runs, of which 24 re-execute pilot cells and 8 are the new `market_only + firm_ban` arm) — total 72 runs if all
extensions are used (≈26 CPU-min).

---

## 5. Model-zoo discriminating moments

Each model gets 2–3 **observable** predictions, the discriminating counterpart(s), the current engine outcome keys that
can test them, and a data verdict. "Engine" = simulated test bed; "DHS/ILSA" = empirical test with current data routes
(`TUTORING_DATA_INVENTORY.md`); **PROXY** = only indirect measures; **UNFALSIFIABLE** = no current data/mechanism.

| # | model | observable predictions (2–3) | discriminates against | engine outcome keys | DHS/ILSA verdict |
|---|---|---|---|---|---|
| 1 | **Becker human capital** | (i) higher returns/income → more schooling investment; (ii) tutoring raises **learning** (`L6/L9`, `mpl_*`) and later completion, not only credentials; (iii) borrowing constraints bite (completion gap by income) | Spence (no learning effect), Hirsch (no absolute-skill claim), pure demand models | `completion_*`, `mpl_primary/lower`, `L6/L9`, `completion_*_q`, `inc_by_cred` | **PROXY** (DHS completion by wealth; no earnings, weak identification) |
| 2 | **Mincer returns** | (i) log earnings linear in schooling; (ii) returns stable across contexts/supply regimes; (iii) experience–earnings profile (not modelled) | Becker (dynamic investment), Spence (credential jumps) | `inc_by_cred`, `formal_rate`, `theta_L`, `cred_step` (simulated returns); no experience variable | **UNFALSIFIABLE in DHS** (no earnings); engine can simulate but that is not evidence |
| 3 | **Spence signalling / screening** | (i) credential premium with **flat L** (`formal_by_cred`, `inc_by_cred` vs same-L comparison); (ii) gate/elite pressure raises effort (`contest_e_mean`, `elite_share`) without learning gain; (iii) credential floors persist (`floor_skilled`, `queue`) | Becker/Hanushek (skills drive outcomes), Hirsch (relative rank drives demand, not employer screen) | `inc_by_cred`, `formal_by_cred`, `floor_skilled`, `queue`, `elite_share`, `contest_e_mean`, `L9` | **PROXY** (DHS education levels but no skills; PISA skills + education partially identify) |
| 4 | **Hanushek production function** | (i) school inputs (q0, budget, PTR, teacher pay) raise learning; (ii) diminishing returns; (iii) class size/teacher quality matter | Hirsch/Bray (learning flat while spend rises), Spence | `q_pub`, `ptr`, `teacher_pay`, `mpl_*`, `L6/L9`, `completion_*` | **PROXY** (PISA/SEA-PLM school questionnaire; DHS has no school inputs) |
| 5 | **Hirsch positional competition** | (i) tutoring/prep rises with fixed-seat contest intensity (`contest_e_mean`, `tut_k12_rate` vs gate share) while learning is flat; (ii) spending tracks relative rank (`elite_q5_share`, Q5–Q1 gap) not q; (iii) seat expansion lowers effort (inverted-U) | Becker/Hanushek (absolute skill), Bray (exam motive alone doesn't distinguish positional vs human-capital demand) | `contest_e_mean`, `tut_k12_rate`, `tut_k12_spend`, `elite_share`, `elite_q5_share_pct`, Q5–Q1 gap | **PROXY** (needs seat/admission + tutoring spend: PISA/CEPS + exam-seat data; DHS no) |
| 6 | **Bray shadow-education demand** | (i) participation rises with exam stakes (`tut_k12_rate`, `tut_g12_rate` vs gate share); (ii) falls with household capacity (income gradient `tut_k12_rate_by_q`); (iii) responds to school supply S (`q0` cells D1) | Hirsch (Bray is demand-side, not positional mechanism), human-capital supply models | `tut_k12_rate`, `tut_g12_rate`, `tut_k12_rate_by_q`, `tut_k12_spend_by_q` | **PROXY/FALSIFIABLE IF VERIFIED**: PISA 2022 HK/PH tutoring items; SEA-PLM PH/KH; CEPS China (per inventory, items must be verified) |
| 7 | **Biswal / Jayachandran withholding** | (i) `h>0` when pay gap and lessons sellable (`withheld`, `own_share`); (ii) own-teacher tutored share rises with h and falls with monitoring/own_ban (`own_share` vs regime); (iii) banning own tutoring lowers h (supply side) and own supply (`withheld`, `own_share`) | Bray (demand-only), Kaplan (firm supply), Becker (no teacher rent) | `withheld`, `own_share`, `tut_own_by_grade`, `q_pub`, `teacher_pay` | **UNFALSIFIABLE magnitudes** (teacher pay + own-provider data absent; see inventory §2/§3); engine-only mechanism |
| 8 | **Kaplan-type test-prep supply** | (i) for-profit prep scales with exam stakes and ability to pay (`firm_rev`, `firm_price`, firm share vs income/`elite_logw`); (ii) entry expands capacity when demand high (`firm_openings`, `D/K`); (iii) bans raise price sharply (`firm_price`) — *mechanical in engine, not evidence* | Bray (household demand), state-provision (crowd-out), withholding (supply by teachers) | `firm_rev`, `firm_price`, `tutor_openings`, `contest_spend_now`, `tut_firm_by_grade` | **UNFALSIFIABLE firm-market data** (no entry/price/profit data; CEPS expenditure only); theory-only until verified |
| 9 | **China state provision / DL model** | (i) state supply S crowds out private tutoring (`tut_k12_rate`, firm/own share vs q0/budget); (ii) for-profit ban shifts supply to own/residual and raises price (`own_share`, `firm_price`); (iii) state capacity expansion lowers household shadow share (`household_share_spending`) | market models (Bray/Kaplan), withholding (state as supplier) | `q0`/`budget_per_child` → `tut_k12_rate`, `own_share`, `firm_rev`, `household_share_spending`, `priv_share` | **PROXY** (CEPS China + 2021 DL timing; DHS no tutoring) |
| 10 | **Household time allocation** | (i) time (not cash) is the binding constraint on tutoring; (ii) contest prep crowds out other study time; (iii) time binds more in higher grades | all cash-only demand models | **none** — no student/teacher time variables exist (`PAPER_C_MODEL_GAP.md` §1.4); `time_*` params not implemented | **UNFALSIFIABLE NOW** (no time-use data; engine lacks time budget; wave-2 extension + time-use survey needed) |

### 5.1 Discriminating moment families (which moments separate which pairs)

| family | moment / manipulation | separates | engine test | data status |
|---|---|---|---|---|
| **M-A gate pressure** | gate share / `elite_logw` ↑ → spend & prep ↑, learning flat | Hirsch/Spence vs Becker/Hanushek; Bray demand amplifies it | `contest_e_mean`, `tut_k12_rate`, `tut_k12_spend`, `L9` | proxy (gate + tutoring spend data needed) |
| **M-B school supply S** | q0/budget ↑ → tutoring ↓ (substitution) and learning ↑ | Hanushek/Becker vs demand-only models; China state provision | D1 cells, `q_pub`, `tut_k12_rate`, `L6/L9` | proxy (PISA school inputs + ILSA learning) |
| **M-C supplier availability** | own_ban × firm_ban → own↔firm substitution, price, participation | Biswal/Kaplan/state-provision vs reduced-form cap; D2 | `own_share`, `firm_rev`, `firm_price`, `tut_k12_rate` | withholding magnitudes theory-only |
| **M-D credential vs skill** | same L, different credential → pay/hiring; same credential, different L | Spence vs Becker/Mincer | `inc_by_cred`, `formal_by_cred`, `floor_skilled`, `L9` | proxy (PISA skills + DHS education) |
| **M-E time** | time-use vs participation; crowding-out of study time | time-allocation vs all cash models | **absent** (needs wave-2) | **data-blocked** |
| **M-F state vs market** | q0/budget/firm_ban → private tutoring share and household spending share | China state provision vs Bray/Kaplan market models | `priv_share`, `household_share_spending`, `firm_rev`, `own_share` | proxy (CEPS + DL) |

**Cross-model decision rule (per `MODEL_ZOO_SCOPE.md` §2):** *holds / fails / indeterminate-by-context*, with the
context (L, S, supply form) named. No model may "win" on engine simulation alone; engine = mechanism plausibility,
DHS/ILSA = empirical pattern, published estimates = baseline. Multiplicity: report the full model × moment family, no
selective reporting.

---

## 6. What must be pre-registered before any run

1. **Engine pin**: commit + `core.py` sha256 (currently `846c9e0` / `e111397b…8e71`), frozen spec sha256, runner sha256.
2. **Cells and seeds**: the exact four (or more) cells in §4 with `seed` list 0–7; declare which are pilot-cell
   re-executions and which are new (D2B); no cell dropped after seeing results.
3. **Primary outcome per test** (D1: `tut_k12_rate` paired Δ; D2: `own_share` paired Δ) and the ordered secondary
   family with Holm correction.
4. **Predicted sign and minimum effect size** for X and Y (D1: Δparticipation ≤ −2.0 pp, Δspend ≤ −3 %; D2:
   Δown_share ≥ +0.20; mechanism-grade: negative `own-banned × ban` interaction on participation).
5. **Decision rule and "indeterminate" zone** (powered/underpowered thresholds; if underpowered extend seeds to 16
   rather than reinterpret).
6. **Binding / no-op assertions** (h, own_share, q_pub monotone; `unfired_events == []`; regime classification).
7. **Contamination declarations**: q0 scales both sectors; `own_share` mixes contest prep; firm price is mechanical.
8. **Data layering**: engine cells are REPRODUCED SIMULATION; DHS/ILSA comparisons are separate evidence statuses; no
   promotion of a model based on engine alone.
9. **Negative-result preservation**: failed predictions are reported in full (Paper B precedent).
10. **Compute envelope**: ≤ ~14 CPU-min host for the 32-run core; no box job without Commander allocation; results
    committed under `results/paperC_confirmatory/` with manifest + sha256.
11. **No post-hoc cells**: any new cell (e.g. q0=0.8, mechanism-grade D2) is declared before the run, not after.
12. **Zoo tests reuse these cells**; any model-zoo claim that needs S/time levers awaits the wave-2 extension and is
    marked theory-only until then.

---

## 7. Gotchas carried from the pilot (must be fixed in the prereg)

* **Runner docstring vs code mismatch (two inconsistencies, both must be fixed by taking the code as authoritative)**:
  the `run_paperC_pilot0.py` module docstring says "96 runs / 3 supply regimes" and `pay_ratio=0.8`, while the code
  (lines 28–34) has **4 `REGIMES`** (→ 4×2×2×8 = **128 runs**, matching commit `fbc1991`'s "v3 … 128 runs") and uses
  **`pay_ratio=0.55`, `monitoring=0.2`**. The prereg must quote regime parameters from code + the v3 commit message,
  not the header; the expected h values in §1 are computed from the code.
* **Pilot-0 v3 = 128 runs, not 96**: the earlier 96-run figure was v2 (3 regimes); v3 added the `own_open_gap_firm_ban`
  regime. D2B therefore reuses a v3 cell; the only genuinely new D2 cell is `market_only + firm_ban` in §3.2.
* **Pilot-0 N=1500** (exploratory, v3 128 runs) vs this design N=600: cell *definitions* are reused, but results are new
  executions — do not mix pilot numbers into confirmatory tables.
* **`q0` scaling**: `q = q0·min(1.25, (ptr_target/ptr)^alpha_ptr)` (`schools.py:49`) — the cap is on the ratio term, not
  on q0; q0 scales public **and** private quality 1:1.
* **Withholding needs `own_ban<1`**: `sell = 1−own_ban`; `market_only` (own_ban .95) has h≈.007, so D2's no-displacement
  control is valid; `own_open_gap` (own_ban 0) has h=.144.
* **`firm_price` is an output**, and `firm_ban` mechanically raises the price base (`p_firm·(1+firm_ban)`) — price is not
  mechanism evidence; use `own_share`/`firm_rev` decomposition.
* **Contest-prep contamination**: `own_share` and `tut_firm_by_grade` include contest-prep pupils; D1/D2 primary
  outcomes are participation/spend and own_share, with the contamination declared.
* **Learning-side outcomes** (`L6/L9`, `mpl_*`, `completion_*`) are secondary here; a learning claim needs the wave-2
  S/time decomposition (`PAPER_C_MODEL_GAP.md` §3).

---

## 8. What stays unfalsifiable / data-blocked at this stage

* **Household time allocation** (M-E): no student/teacher time variables in the engine and no time-use data in DHS/ILSA;
  wave-2 extension + time-use survey required.
* **Mincer returns**: DHS has no earnings; engine-simulated returns are not empirical evidence.
* **Withholding magnitudes and own-vs-firm provider mix** (Biswal/Jayachandran): teacher pay + own-provider data absent in
  HK/PH; theory-only (engine mechanism can be tested, magnitudes cannot).
* **Kaplan-type firm profits/entry** (commercial supply): no firm-market data; `firm_price`/entry rules are mechanical
  constructs.
* **CES substitution sign / dynamic complementarity** (eq 30/31/40): the engine's production is additive today; the sign
  cannot be tested until the `production='ces'` extension lands.
* **DHS-based tutoring moments**: DHS has no tutoring module — all shadow-education moments are ILSA/CEPS/theory-only,
  not DHS-testable (state this in every model-zoo row).
