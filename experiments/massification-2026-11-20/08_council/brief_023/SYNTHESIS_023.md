> **SYNTHETIC EXERCISE — COUNCIL-2 SYNTHESIS (brief 023, cycle 15).** Panelists are AI-constructed composite
> personas; nothing here is a statement by any living person. This is a **research-direction ruling, not evidence**.
> Write scope `08_council/brief_023/` only; append-only. **No bridge post** (D87); **no external message**. **No model
> code was executed** in this session and no data file was written: every number below was re-derived read-only from
> the delivered CSVs and is listed with its path in `VERIFICATION_023.csv`. The log ends at **D131**, so the proposed
> decisions in `PROPOSED_DECISIONS.md` are **D132+**.

# SYNTHESIS 023 — the model-line batch adjudicated, the v1.5 defects ruled, and five anchored experiments

**Batch adjudicated.** `pipe_loo_2026-11-20/` (predecl `97033df0…`), `repro_path_2026-11-20/` (predecl `74f9d0e0…`),
`gate_locus_2026-11-20/` (predecl `a8566fbf…`), `rung_prob_2026-11-20/` (predecl `1cd399dd…`),
`synthetic_2026-11-20/generator_v1_5_bimodal/` (predecl `7178e3d2…`). All five predeclarations were frozen before their
runs; all five re-run byte-identically; **every verdict word stands as predeclared and no cell is returned for
re-execution.** What does not stand is the *scope* of two of them, the *reading* of a third, and the **guard
specification** of the fifth (§3, §5).

**One-line ruling.** The pipeline object survives at its exact boundary and its coefficient is **per-system**
(PHL 0.9491 / KOR 0.9898 / KHM 0.5950 / CHN 0.7222), so the next model line carries **κ per system as a declared
input** — but **no single κ may be applied across systems**, and **CHN's failure is a trend, not noise**, which makes
the *constancy* of κ a question that must be settled **before** κ is used as a forward constraint. v1.5 is admitted
**for representation only**: it can hold untaken cheap places and a contested high gate in the same country-year, and
it cannot hold the level pattern. Its implementation failures are **not tuning problems** — the κ cap breaches a
cell-identity guard that was **arithmetically unsatisfiable**, and the child-wage test was **structurally unfirable** —
so the repair is a **re-specification with declared parameters**, never a re-tune (§5).

---

## Step-back (mandatory, per `BIG_PICTURE_RULE.md`)

1. **First-order goal, one sentence.** A longitudinal model in which *massification/universalization* is produced by
   **schooling, government and markets each standing the others up**, with cohort flows and country/sector variation,
   that reproduces **which** PHL milestones crossed and **when** (floor and middle yes, upper-secondary ceiling no) —
   and then, as a **diagnostic only**, HKG's primary-NER timing; shadow secondary.

2. **KEEP / PARK / KILL (delta vs cycle 14).**
   - **KEEP** — the **transition-ratio object** `upper_t / lower_{t−3}`, now with a **per-system κ** as a **declared
     input** (§2 V9, D128); the **κ-link as a structural constraint** (D121); **v1.2** as a *labelled* instrument
     (**crossing/endpoint placement only** — EXP-7 leg A settled the audit: 9/33, D126); the **A1 write-up**;
     **M1-NER** as the measurement floor of every model-side level claim; the **bimodal class** as a
     **representation** capability (v1.5 check (a)).
   - **KEEP-NEW** — the **declared-parameter repair** of the three v1.5 defects (§5), as a *capability* run and not a
     test of A5; the **per-system κ register** (four declared values + one labelled PHL-derived default for the other
     26 synthetic types).
   - **PARK** — v1.5 as a *level* model (its level pattern collapses by construction of its own declared parameters);
     the **A3 demand line** stays **KILLED** (D130) and is not re-specified; the **W2 shadow module** stays
     design-only; the **exit-cost and induction layers** stay closed (D101/D104); HKG reverts to **`DEFER-HKG`**
     because EXP-10 was not delivered (§2 V14, §3.6).
   - **KILL** — **a single global κ** (the spread across four systems is **0.395**; a single κ = 0.949 overstates
     KHM by **0.354**); **"the ceiling is an upper gate"** (D129 closed it); **"v1.2 reproduces the PHL path"** (D126);
     **scoring a v1.5 successor on the v1.3 signature bands** `[73,77]`/`[55,85]` (a placement target, not a path
     target — D119/EXP-7); **a cell-identity guard on the whole panel** for a binding cross-level link (it cannot
     hold; §5.1); **GER as a pipeline numerator** (D118).

3. **The one thread that most advances the model.** **Make κ an admissible forward input, then let the repaired
   generator be scored on the observed path.** The batch established (i) the ratio predicts its own held-out years in
   **3 of 4** systems, but (ii) fails in the one system undergoing rapid expansion, (iii) its PHL value shifts from
   **0.9596** (pre-2021 pairs) to **0.9491** (all pairs), and (iv) the model's link currently censors an *admission
   cohort* whose survival factor (**0.870**) makes the endpoint **8.31 pp lower** than the number the predeclaration
   expected. Until "is κ constant and forward-usable?" is answered, every downstream level statement inherits a
   coefficient whose stability is untested.

4. **Drift check.** Four red flags, each with its critical-path justification (D11).
   - **R1 — measuring instead of modelling.** Two of the five (KAPPA-FWD; CONV-REG) are measurement/audit objects.
     **Justification:** the object they serve *is* the model's next declared input; κ is about to become a parameter,
     and a parameter whose stationarity is untested is exactly the "fitted curve treated as a law" failure the rule
     names. CONV-REG is the deliberately droppable member and is ranked last.
   - **R2 — single-object concentration.** Three of the five concern the pipeline/level structure.
     **Justification:** the batch produced exactly one forward object. **FLOOR-CLOSE** (capacity) and **CONV-REG**
     (measurement) are the two out-of-object members.
   - **R3 — re-litigating a delivered cell.** KAPPA-FWD re-uses EXP-6's 43 pairs. **Justification:** its estimand is
     **temporal** (κ from past pairs only, applied forward) and **stationarity** (a trend slope), neither of which
     EXP-6 computed; EXP-6's verdict is not re-scored, and the block states that its outcome cannot change EXP-6.
   - **R4 — a repair that is really a rescue.** V16-REPAIR re-declares parameters after seeing v1.5 fail.
     **Justification:** v1.5's verdict stands and is not re-scored; the repair carries **four binding
     obligations** (§5, §6.4) and is labelled a **capability** run, explicitly not an independent test of A5. **If the repair
     cannot be predeclared without choosing a parameter by reference to a level bar, it must not run.**
   **Red-flag count: 4** → written justification above; no paper-test slate this phase (D113b).

5. **If only one thing mattered this week:** **LOWER-DEF** — the lower-secondary series is the named defect
   (**required lower-2021 80.76 vs generator 67.41**, §2 V12) and every level claim in every generator version
   inherits it. **Drop-first of the five: CONV-REG** — it produces a register, not a result; every number it would
   tabulate is partly on disk already (brief-022 V6 / D118), and it changes no model behaviour.

---

## 1. What arrived, and what was verified

| item | source | check | result |
|---|---|---|---|
| EXP-6 predeclaration | `pipe_loo_2026-11-20/PRE_DECLARATIONS.md` | sha256 + sidecar | **`97033df0c5693f50…`**; 13/13 `shasum -c` OK; run1 ≡ run2 on all 4 artifacts |
| EXP-7 predeclaration | `repro_path_2026-11-20/PRE_DECLARATIONS.md` | sha256 | **`74f9d0e0…3db12`**; six artifacts byte-identical across two runs |
| EXP-8 predeclaration | `gate_locus_2026-11-20/PRE_DECLARATIONS.md` | sha256 + verbatim re-check of the quoted block | **`a8566fbfbca5cc5231ef78c35adffbf62264f82bbefe830683616105434c547d`**; 25/25 OK; 8/8 artifacts byte-identical |
| EXP-9 predeclaration | `rung_prob_2026-11-20/PRE_DECLARATIONS.md` | sha256 | **`1cd399dd…`**; 21/21 OK; 0 `cmp` failures across panels + manifests |
| v1.5 predeclaration | `generator_v1_5_bimodal/PRE_DECLARATIONS.md` | sha256 before **and** after | **`7178e3d2ee2e367cd7dbb0619f2031305ff446978a43aab9e1f6caefb07ca97f`**; 84/84 SHA from programme root; 14/14 result files byte-identical across two controller runs |
| v1.5 A00 guard | `results/synthetic_panel_v1_5_A00.csv` | sha256 vs frozen v1.3 panel | **`47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3` — identical**, 6 720 rows; independently reproduced through the frozen base code |
| v1.5 κ audit | `results/kappa_cap_audit.csv` | violations of `upper_t ≤ 0.949·lower_{t−3}` | **20/53 before → 0/53 after** |
| v1.5 κ cell identity | `results/KAPPA_GUARD.json` | A01 vs A00, cell-for-cell | **BREACH** — `upper_diff_only_where_cap_binds = false`; 1 620/1 680 upper rows differ; **180/5 040** non-upper rows cell-identical |
| HKG outcome record | `hkg_transfer_2026-11-20/HKG_H1_OUTCOME.md` | frozen predecl untouched | predecl **`99be01d7…`**; terminal state record only |
| EXP-10 stock-NER design | — | directory search under `10_massification/extensions/` | **ABSENT** — `hkg_stock_ner_2026-11-20/` does not exist; no stock-object predeclaration anywhere on disk |

**No cell is RETURNED for re-execution.** Two are **ACCEPT** (EXP-7, EXP-9), three are **ACCEPT-WITH-CONDITIONS**
(EXP-6, EXP-8, v1.5); every condition is a **record correction or scope narrowing for the Lead**, never a re-run.
**EXP-10 was not delivered**, and the predeclared reversion (SYNTHESIS_022 §5.3) therefore fires (§3.6).

---

## 2. Council-side verification (V9–V15) — what the batch did not say about itself

All re-derived read-only from the delivered files. **These are the load-bearing new facts of cycle 15.**

| # | finding | numbers | source |
|---|---|---|---|
| **V9** | **κ is per-system, and its stability is untested.** The four medians are **PHL 0.9491, KOR 0.9898, KHM 0.5950, CHN 0.7222** — a **0.395** spread; a single κ = 0.949 overstates KHM by **0.354**. Restricting to **pre-2021 pairs only** gives **PHL 0.9596, KOR 0.9887, KHM 0.5950, CHN 0.7222**, i.e. the PHL coefficient moves by **0.0105** when the two 2023–2024 pairs are added. **Post-2020 pairs available as a temporal hold-out: PHL 2, KOR 3, KHM 2, CHN 0 — 7 cells.** Ratio ranges: PHL **0.8892–1.0724**, KOR **0.8308–0.9956**, KHM **0.1389–0.6910**, CHN **0.6448–0.9662**. | 0.9491/0.9898/0.5950/0.7222; 0.9596; spread 0.395; 7 hold-out cells | `pipe_loo_2026-11-20/results/PIPE_LOO_RESULTS.csv` (`kappa_median_ratio`), `PIPE_LOO_PAIRS.csv` (`ratio`, `upper_year`) |
| **V10** | **The model's floor universalization is delivered at 87.2 % of adequate places, by a declared crowding allowance.** Capacity is `min(phys_cap·seats, overage_cap·cohort)` with **`phys_cap = 1.15` (DECLARED)** and `overage_cap = 1.05` (CONVENTION). The anchor's primary gate first admits everyone in **2019**, when `seat_coverage = 0.8722` (seats 2 115 584; cohort 2 425 667; demand 2 415 085; `1.15 × seats` = 2 432 921) — **not at coverage 1.0**. In 2024 the binding term has switched to `1.05 × cohort` (2 372 829 < `1.15 × seats` = 2 426 998) and coverage is **0.9339**. The single-gate stack's `p_off = 1.0000` at primary is therefore a property of the **allowance**, not of places. | coverage at closure **0.8722**; `phys_cap` 1.15; binding switch at 2023 | `generator_v1_2/results/synthetic_panel_v1_2.csv` (`seats`, `cohort`, `demand_official`, `admitted_official`, `seat_coverage`); `generator_v1_2/PARAMS.md` (`phys_cap`, `overage_cap`) |
| **V11** | **The κ-guard breach is narrow in the school block and wide in the economy block.** Anchor type, 2024, A01 vs A00: **primary and lower schooling columns are cell-identical** (`completion_uis`, `enrolment`, `admitted_official`, `demand_official`, `teachers`, `ptr`, `ger` — all equal); the movement is in `ptr_system` **36.6529 → 41.0086**, `gdppc` **8 099.45 → 7 812.68**, `growth` **0.028354 → 0.031291**, `yos_proxy` **6.5082 → 5.9787**, plus upper (completion **0.76639 → 0.55657**; teachers **49 135 → 28 461**; `ptr` **37.25 → 56.02**) and tertiary (admitted **624 719.7 → 614 790.3**; teachers **24 585 → 18 488**; `ptr` **27.64 → 36.22**). | exact cell values as listed | `generator_v1_5_bimodal/results/panel_v1_5_A00_v13cols.csv` vs `panel_v1_5_A01_linked.csv` |
| **V12** | **The link is expressed in the wrong units, and its endpoint arithmetic was missing one term.** The cap bounds an **admission cohort** (`adm_upper ≤ κ·comp_lower_cohort`) while the audited object is a **completion rate**; the two differ by `surv_upper = 0.8700`, which is exactly the **8.31 pp** gap between the predeclared expectation (**63.9695**) and the realised endpoint (**55.6573**). Separately, the **lower** series is the binding defect: to hold upper 2024 at its delivered **76.6391** under κ = 0.949, lower 2021 would need **80.76** — observed **80.896** would support it, the generator's **67.4073** is **13.35 pp short**. The chain is exact and multiplicative: `comp_uis_lower(2021) = 1.10 × adm_off(2018)/cohort(2018) × surv(2021) = 1.10 × 0.783805 × 0.781819 = 0.674073`. | 8.31 pp; 63.9695; 55.6573; 80.76 vs 67.4073; 0.783805 × 0.781819 | `generator_v1_5_bimodal/FINDINGS.md` §5.2–5.3; `synthetic_panel_v1_2.csv` (`completion_uis`, `completion_cohort`, `survival`, `admitted_official`, `cohort`); `generator_v1_2/code/sim_v1_2.py:604-610`, `DVEC = (6,3,3,4)` |
| **V13** | **No declared v1.5 sensitivity cell can reach the level bars.** Across the whole frozen grid the maximum primary 2024 is **61.84** (`q_O = 0.70`), and `h_share + 0.10` gives **56.25**; the bar is **≥ 92**. So the (b) failure is **structural** (quality feeds survival with the untiered exponent, and Tier O is 60–85 % of places), not a knob that was set slightly wrong. | max primary 61.8418; h_share arm 56.2497; bar 92 | `generator_v1_5_bimodal/results/SENSITIVITY.csv` (`S1`,`S5`,`S6` `primary_2024_comp`) |
| **V14** | **The pipeline object cannot be extended on disk, and the HKG arm is unbuilt.** Upper-secondary completion exists for **four systems only** (row counts: KOR 24, KHM 18, PHL 11, CHN 6) and the 30-country WDI panel carries **`SE.SEC.CMPT.LO.ZS` but no upper-secondary completion indicator** — so the 3/4 verdict cannot be strengthened without new data. No stock-NER design exists (EXP-10 absent), so HKG stays `DEFER-HKG`. | 4 systems; 24/18/11/6 rows | `10_massification/data/UNIVERSALIZATION_SERIES.csv` (`indicator`); `09_relations/data/panel_wdi_long.csv` (`indicator`) |
| **V15** | **At observed PHL values the ceiling is consistent with its own κ bound, and upper-90 is arithmetically out of reach under it.** `0.9491 × lower(2021) = 80.896 → 76.778`; observed upper 2024 **75.025** sits **1.75 pp** inside that bound (ratio **0.9274**). Upper **90** requires lower(t−3) **94.827**; the observed lower maximum is **92.414** (2024), so the κ-implied maximum upper for 2027 is **87.710**. **A necessary condition, not a forecast, not a causal claim.** | 76.778 / 1.753 / 0.9274; 94.827; 87.710 | `UNIVERSALIZATION_SERIES.csv` (`completion_lower_secondary`, `completion_upper_secondary`, PHL) |

**What V9–V15 do to the batch.** They overturn no predeclared verdict. They change what the batch may be *said* to
have shown: κ is a **system input with untested stability**, the floor's universalization is **allowance-carried**, the
κ guard failed **for a reason the guard made inevitable**, and the ceiling question now has **an observed-side
arithmetic** that no model produced.

---

## 3. Adjudication

**One-line ruling: all five verdicts stand as predeclared; two are accepted clean or narrowly conditioned, three are
narrowed to what they actually tested, and one guard is ruled mis-specified rather than failed.**

### 3.1 EXP-6 PIPE-LOO — **ACCEPT-WITH-CONDITIONS**

Verdict confirmed: **`PREDICTIVE (3/4)`**, reproduced exactly — PHL n=8, median |LOO error| **1.50 pp**, **7/8
(87.50 %)** within ±5 pp; KOR n=19, **0.48**, **17/19 (89.47 %)**; KHM n=11, **2.17**, **10/11 (90.91 %)**; CHN n=5,
**14.48**, **0/5**. 43 pairs (8/19/11/5), **16** upper years dropped by rule, pooled 1.01 pp / 79.07 % (descriptive).
HKG and JPN **non-entrants** with zero completion pairs, nothing imputed. Determinism 13/13.

**Named defects.**
- **(a) The verdict is at its exact boundary.** 3/4 with 3 required — **one country flipping flips it**. No
  downstream text may say "the transition ratio is predictive" without the count, the pair numbers and this sentence.
- **(b) KOR's pass is close to an arithmetic identity at saturation** (lower series pinned 99.90–100.00; 17/19 upper
  values in 97.3–99.5), and **KHM's median is carried by one collapse-year outlier** (ratio **0.1389** at t = 2000, on
  the 1996 lower value at a realised lag of 4 y). The informative systems are **PHL and KHM positively, CHN negatively**.
- **(c) CHN's failure is a trend, not noise**: the ratio runs **0.6448 → 0.9662** while lower completion is flat
  (82.6–95.7); residuals are **+14.5, +8.4, +7.7, −15.6, −22.4 pp**. A constant-κ predictor is the wrong *shape* there.
- **(d) PHL's pass rests on 2003–2017**, and **upper 2022 — the largest single-year move in the series (76.43 →
  68.28) — is dropped by the pairing rule** (no lower observation within ±1 y of 2019). Part of the recent turbulence
  lies outside the test by construction.
- **(e) Record correction (D113a class).** "A single κ misstates KHM by ~0.40" is imprecise: the **median difference
  is 0.354** (0.9491 − 0.5950) and **0.395** is the **spread across the four systems**. Both numbers should be quoted
  for their own purpose.

**Conditions:** κ is recorded as **four per-system declared inputs**; no cross-system κ; every downstream use carries
the pair count; CHN's κ = 0.7222 is recorded as **a within-sample median for a non-stationary series** and **may not be
used as a forward constraint**.

### 3.2 EXP-7 REPRO-PATH — **ACCEPT (audit clean; both legs bind)**

Verdict confirmed: **leg A `ENDPOINT-ONLY`** (9/33 = 27.27 % within ±5 pp against the **≥17/33** bar; ±10 pp 13/33;
medians −4.30 / −29.44 / −27.59; by level 6/11, **0/11**, 3/11; worst upper 1999 **−36.62**, lower 2000 **−33.37**;
1999–2017 **2/22** cells with median **−28.21**, 2021–2024 **7/11** with median **+0.04**); **leg B `b2`** (20/53 → 0/53;
largest excess **+18.31 pp** in 2022; 12 anchor years with ratio > 1.10, max **1.2661**; upper 2024 76.6391 →
**63.9695**, Δ **−12.6695**; ratio 2024 **1.136955**; κ sensitivity 0.960 → 64.71, class unchanged). Baseline guard
**PASS** on all four legs (G1–G4).

**No execution defect.** Two scope rulings the Lead must carry:
- **(a)** The **33-comparison construction is PHL-only**; it cannot be quoted as a statement about any other system,
  and it must travel with its cell counts wherever D119 is cited.
- **(b)** The **"63.97" reading is an admission-cohort bound, not a completion endpoint** (§2 V12): the realised
  completion endpoint under the same link is **55.66** once survival (**0.870**) is applied. Any predeclaration that
  quotes 63.97 as "the upper level the link implies" repeats v1.5's §9 omission.

### 3.3 EXP-8 GATE-LOCUS — **ACCEPT-WITH-CONDITIONS**

Verdict confirmed: primary **79.11 % / 87.38 %** `GATE BINDS` (bars 0.95/0.99; n = 1 680 per level), lower-secondary
**91.31 % / 93.33 %** `GATE BINDS`, upper **4.70 % / 6.55 %** `UNRATIONED`, tertiary **0.00 % / 0.00 %** `UNRATIONED`
(an **accounting identity**: `admitted ≡ demand` in 1 680/1 680). Anchor type: upper `p_off = 1.0000` and
`rationed_official = 0` in **56/56** years; primary rations 49 years (none after 2018), lower 53 (none after 2022);
rung-4 absorption **0.0678 / 0.1095 / 0.1661 / 0.1854** (2010+ median **0.1510**; panel median **0.5066**). Falsifier
**NOT TRIPPED** (0/1 680 upper, 0/1 680 tertiary below 0.50; nearest approach **0.7879**). **The "ceiling as an upper
gate" line is CLOSED.**

**Named defects.**
- **(a) The falsifier is measure-dependent, disclosed by the worker and now load-bearing for the Council.** On the
  gate panel's own `pi0`, the PHL-like tertiary `g3` is below 0.50 in **8/56** years (14.3 %) but the **KHM-like** `g3`
  is below 0.50 in **53/56** (94.6 %) — which **would trip it**. The verdict is therefore a statement about **the flow
  panel's admission accounting**, not about every probability in the module. Any citation must say so.
- **(b) The tertiary row is an identity, not a measurement**, and may never be cited as "tertiary is unrationed".
- **(c) Two on-disk constructs disagree below and above the upper gate** (gate-panel `g1` mean 0.979 vs flow-panel
  lower rationing 91.3 %; gate-panel `g3` for PHL-like 0.431–0.712 vs flow-panel tertiary `p_off ≡ 1.0`): the
  disagreement is a **construct difference (denominator: candidates vs official-age demand)** and must be named
  wherever both are used. **No number here mixes them.**

**Condition:** the anchor's "no binding school gate at any level by 2024" is recorded as a statement about
`v1.2`'s flow panel and `v1.3`'s gate panel **jointly**, with the `g3` divergence disclosed.

### 3.4 EXP-9 RUNG-PROB — **ACCEPT (clean)**

Verdict confirmed: **`NOT DEMAND-DERIVABLE`**. Arm A (`P = pi0(g2) ≈ 0.999`) → upper 2024 **95.04548615**, **+16.0455**
above 79, ablation **+18.4064** (NON-DECORATIVE); arm B (`P = rung4_emp/rung4_demand`, anchor median 0.151) →
**42.12562430**, **−28.8744** below 71, ablation **−34.5135**. Both outside **[71,79]** → falsifier fires → **A3 line
KILLED, not parked**; taste parameter **irreducible without a fit**. Guards **PASS** (G1 `47d4b082…` = v1.3;
G2 `ffecd450…` = frozen v1.4). The bracketing is clean: `v_2 = 0.78608` sits between arm B's `v_D = 0.2981` and arm
A's `v_D = 1.9394`.

**No execution defect.** Three carry-forward rulings:
- **(a) The kill is a statement about the generator, not about demand.** It may not be summarised as evidence that
  demand is weak; the banned phrasing (D124) stands.
- **(b) Arm B substituted an absorption ratio for a probability** — the worker had *already* disclosed this (EXP-8 §7
  Condition 2), so the undershoot was partly arithmetic. That is a property of the test as designed, and the verdict is
  correct **about the two probabilities the model has**.
- **(c) The rung-4 absorption used to kill the line is a model object, not a measurement.** No file may say the
  model's queue was "measured at 0.151"; it is `rung4_emp/rung4_demand` from the frozen panel. A measured
  credential-queue series is a **HELD DATA ASK** (unchanged).

### 3.5 v1.5 BIMODAL-GATE — **ACCEPT-WITH-CONDITIONS; model class admitted for REPRESENTATION ONLY**

Verdict confirmed exactly as delivered: **`a = MIXED; b = FAIL; c = MIXED; d = FAIL; e = MIXED; ALL = FAIL`**;
`BASELINE-GUARD-PASS`, `KAPPA-GUARD-FAIL`, `FROZEN-FILE-GUARD-PASS`, `DETERMINISM-PASS`; **R1 ratchet audit 0 hits**;
T-AUD-1…5 **PASS**; frozen inputs **20/20**; determinism **14/14**.

**What is accepted as achieved (the user's structural requirement).** For `SYN00_PHL_LIKE` in **all 15** scored years
2010–2024, upper-secondary **Tier O unfilled share 0.648–0.932** coexists with **Tier H queue ratio 1.29–1.93** and
credentialed-job absorption **p₄ ≈ 0.250**; (a-i) 18/30 cells, (a-ii) 30/30, (a-iii) 15/15 years, `p₄ ≤ 0.50` 15/15;
and the single-gate arm's `same_level` is **0** against **15** in the tiered and linked arms. **The class can represent
the phenomenon the single-gate stack could not** — and that is a capability fact, not evidence about the Philippines.

**What is not accepted.** The level pattern **collapses, not stalls**: Tier O survival **0.508 / 0.476 / 0.479 / 0.501**
against `surv_H = 0.995`, at a Tier O share of 60–85 % of places → primary 2024 **51.62568565** (never ≥ 90), upper
**33.68346818**, lower 2024 ≈ **51.6**, tertiary **44.1**. **(b) FAIL is a structural consequence of the declared
`q_O_mult = 0.55` fed through the untiered survival exponent**; §2 V13 shows **no declared sensitivity cell** reaches
the bars (max primary **61.84**). **(c) MIXED** on a **1.16 pp** miss (open-tier R→2R gap **+2.16 pp** vs **≤ +1.0**;
placement ratio min 33.2, `D_O` max 0.0077, high-gate gap **+31.13 pp** all pass) — recorded as a **minor numerical
miss, no rescue, no re-score**. **(d) FAIL** on the child-wage leg (**+1.080546093 pp** vs **≤ −2.0**), with the
no-free-taste audit (**0 hits**), `w_work_free = 0`, **slack ≥ 0 in 53/53**, and the quality ablation
(**+11.22406483 pp**) all passing; **cap non-binding 0/53**. **(e) MIXED** on `KAPPA-GUARD-FAIL`.

**Four record corrections (no re-run, no re-score).**
- **(a) The a-iv leg is a pre-run labelling error, recorded, never re-scored.** The frozen text reasoned *"in arm A01
  (`bimodal OFF`) this count must be 0 because the upper school gate is unrationed"* — true of the **frozen single-gate
  panel (A00)**, false of **A01**, which is `bimodal OFF` **but κ ON**, where the cap itself rations the upper entry.
  The correct contrast is **A00 (0) vs A11 (15)**. The leg's **FAIL stands as scored**; the *reason* it failed is that
  the predeclaration named the wrong arm. The same confusion is in D131's parenthetical and should be corrected there.
- **(b) D131's description of the breach understates it.** The movement is not "secondary columns": per V11 the
  **primary and lower schooling columns are cell-identical**, while the **economy columns** (`ptr_system`, `gdppc`,
  `growth`, `yos_proxy`), **upper**, and **tertiary admission** all move. The guard failed on **system-level columns**,
  which makes the design fix tractable (§5.1).
- **(c) The (d-ii) "cap non-binding ≥ 5/53" leg was unsatisfiable by construction**, and its expectation was derived
  from the wrong register: the 20/53 figure it was calibrated against is a **completion-level** audit, while the cap
  operates on an **admission cohort** (V12). The two registers are mutually exclusive — the count reading gives
  **0/53 binding** and **20/53 completion violations**; the rate reading gives **0/53 violations** and **53/53
  binding**. **No reading satisfies both (e-ii)(3) and (d-ii)**; the leg is a **predeclaration defect**, not a worker
  error.
- **(d) The disclosed process error is accepted.** `TUNE_LOG.md` B1: the pre-run `SHA256SUMS.txt` was overwritten by
  smoke runs before it could be snapshotted, so `results/FROZEN_BEFORE_SHA256SUMS.txt` is a reconstruction (30/33
  still match; the exceptions are the two files the run updates and the externally edited `DECISIONS.md`), with the
  original's sha256 **`89638b39…`** recorded in `RUN_MANIFEST.json`/`guard_report.json`. **No value impact:** the A00
  guard was verified two independent ways. Also recorded, not repaired: `DECISIONS.md` moved
  **`6fdcf8ee…` → `59696b81…` at 00:05** (Lead's edit, outside E3's declared scope and outside this worker's).

### 3.6 Hong Kong — **`DEFER-HKG` (the predeclared reversion fired)**

EXP-10 STOCK-NER-D was **rank #5 / DROP-FIRST** last cycle and was **not delivered**: no `hkg_stock_ner_2026-11-20/`,
no stock-object predeclaration, no construct test. SYNTHESIS_022 §5.3 declared *"if the design is not delivered by the
next Council cycle, the path reverts to DEFER-HKG with the object blocker recorded"* — **that condition has now
occurred, and the Council executes it.** Recorded state: `BLOCKED-MEASURE(SR-1)` **terminal** for the cohort-flow NER
object; **no HKG result exists**; D111 void for that object; observed reference only (first-sustained HKG `ner_primary`
≥ 90 **1974**, ≥ 95 **1979**; overlap with `ger_primary` 7 years, 2012–2018). **The Council does not re-issue the design
as one of this cycle's five** — re-issuing a dropped deliverable would reward non-delivery and consume a slot that the
level defect needs. A future HKG attempt requires a **new Council decision**; the object blocker and the **HELD**
single-age HKG population 1971–1996 are named, never fabricated.

---

## 4. Dispositions — confirm or correct

| recorded disposition | Council-2 | correction / condition |
|---|---|---|
| **A3 demand line KILLED** (D130) | **CONFIRM** | Kill is **model-side**: the unrationed single-gate stack has no dimensionally neutral slot for demand. No re-specification this phase; banned phrasing stands; the rung-4 object is a model ratio, not a measurement. |
| **"Ceiling as an upper gate" CLOSED** (D129) | **CONFIRM** | Binds at the floor (79.11 % / 91.31 %), unrationed at upper (4.70 %) and tertiary (0.00 %, identity); falsifier not tripped; **the falsifier is measure-dependent** and the `g3` divergence must travel with it. |
| **Pipeline object = transition ratio** (D118/D121) | **CONFIRM AS LOCATION; CORRECT THE COEFFICIENT** | The object is `upper_t / lower_{t−3}`; its coefficient is **per-system, never global** (0.9491 / 0.9898 / 0.5950 / 0.7222; spread **0.395**). **CHN's κ may not be used forward** (trend). |
| **v1.2 `PASS-CONDITIONAL`** (D110/D119) | **CONFIRM AS SCORED; LABEL NOW FINAL** | EXP-7 leg A settled the audit: **9/33 = ENDPOINT-ONLY**. The label is **"crossing/endpoint placement"** permanently; the `m = 1.10` convention is unchanged and is a **convention**, not a conversion. |
| **v1.5 BIMODAL-GATE** (D131) | **CONFIRM VERDICT; ADMIT THE CLASS FOR REPRESENTATION ONLY; CORRECT FOUR RECORDS** | Level pattern **not** reproduced and **not** reachable inside the declared grid; the class is admitted for the **representation capability** it demonstrated and for nothing else. Corrections at §3.5(a)–(d). |
| **HKG `BLOCKED-MEASURE(SR-1)`** (D114) | **CONFIRM TERMINAL; PATH NOW `DEFER-HKG`** | EXP-10 not delivered → SYNTHESIS_022 §5.3 reversion executed. No portability/capacity/timing/phase claim is licensed by anything on disk. |
| **D63 ceiling residual `UNABLE` as to cause** | **CONFIRM, WITH ONE ADDITION** | Stays `UNABLE`. New **observed-side arithmetic** (V15) is recorded as a **necessary condition**: under κ = 0.9491, upper 90 requires lower(t−3) ≥ **94.827**; observed max **92.414** → κ-implied upper max **87.710** for 2027. **Not a forecast, not a cause.** |
| **A10/D62 "capacity buys the floor"** | **CORRECT (scope)** | In this implementation the floor is delivered at `seat_coverage` **0.8722** by the declared **`phys_cap = 1.15`** crowding allowance (V10). The claim must be restated as conditional on that **declared convention**; **FLOOR-CLOSE** (§6.2) is the panel-wide test. |

---

## 5. Rulings on the v1.5 implementation defects

### 5.1 The κ cell-identity breach — **the guard was mis-specified; the implementation reveals the right object**

**Finding (accepted):** `KAPPA-GUARD-FAIL`. A01 differs from A00 on `upper_diff_only_where_cap_binds = false`
(1 620/1 680 upper rows differ, most in years where the cap does not bind) and on non-upper cell identity
(180/5 040 identical).

**Ruling.** **The breach is not an implementation error to be patched; sub-guard (e-ii)(1) demanded something
arithmetically impossible.** Once the cap binds at upper entry, the model's own accounting routes the capped graduate
flow into the tertiary eligibility pool, the rung-matching candidate pool and formal employment, which drives the
growth equation — so **every** system-level column must move. A guard that requires the whole non-upper panel to be
cell-identical therefore **cannot hold for any binding link**, and its failure carries **no information about the
link's validity**. Three design obligations for the repair predeclaration, all binding:

- **(i) Bound the right object.** The constraint must be stated in **completion units** with the survival allowance
  explicit — `adm_upper(t) ≤ κ · comp_lower(t−3) / surv_upper(t)`, or equivalently a declared endpoint object
  `κ · lower · surv` — so that the audited completion ratio and the enforced object are the **same object** and the
  "≈ κ·lower" reading is not off by `1/surv` (V12: **8.31 pp**). **The predecl must say which object it bounds and
  which number it expects**; the v1.5 §9 omission may not recur.
- **(ii) Declare a legitimate projection order.** The propagation cannot be removed, only **ordered and audited**: the
  cap is applied at the upper entry; graduates then feed the tertiary eligibility pool, the matching pool and growth;
  capacity and gates for **t+1** read the economy. The repair must ship a **propagation ledger** — every column that
  moves, its mechanism, and its sign relative to the cap — and must show **one-way** propagation (no within-year
  feedback from the capped economy back into the *same-year* school admission of any level). **If a within-year feedback
  exists, the cap is not a projection and the repair must say so.**
- **(iii) Restate the guard as a counterfactual identity, not a panel identity.** The test is: feed **A01's upper
  admission vector** into the **A00 accounting** and reproduce A01 cell-for-cell. That is the identity that actually
  certifies "the link changed nothing except through the declared channel". Alongside it, keep two cheap exact checks
  that V11 shows *do* hold: **primary and lower schooling columns cell-identical** (`completion_uis`, `enrolment`,
  `admitted_official`, `demand_official`, `teachers`, `ptr`, `ger`), and **tertiary admission moving only through the
  eligibility pool** (non-increasing when the cap binds). **A whole-panel identity guard must not be re-frozen.**

**Also ruled:** the **cap's register (rate vs count) must be declared in one unit** before the run. v1.5's two guards
required two different registers (§3.5(c)), which made one of them unsatisfiable by construction. This is the defect
that produced the "defect".

### 5.2 The child-wage sign — **the test was structurally unfirable; re-specify the object, not the bar**

**Finding (accepted):** `w_child +10 %` moves upper 2024 by **+1.080546093 pp** against a required **≤ −2.0**.

**Ruling.** Under a **binding** κ cap the **total** upper entry is fixed in all 53 cells, so the shock can only move
the **H/O composition**, and because `surv_H = 0.995` ≫ `surv_O ≈ 0.48`, a composition shift toward H mechanically
**raises** admission-weighted completion. The observed sign is therefore **predicted by the model's own accounting
before any behaviour is involved** — the leg is **structurally incapable of returning the declared sign**, exactly the
class of defect the toy battery disclosed for its unfirable `v = 0` leg (D85). **It is not evidence that the outside
option is inert, and it is not evidence that it is active.**

**Design obligation.** The shock must be re-specified on **an object it can move**:
- **(i)** test it where the constraint is slack — **arm A10 (bimodal ON, κ OFF)** — with a declared sign on the
  **upper completion** object, and
- **(ii)** in the capped arm, test it on the **pre-cap** object (`demand_official` / `A_H` / the queue), with a declared
  sign **derived from the declared utility block before the run**, and
- **(iii)** report the capped-arm completion response as a **composition effect**, non-verdict-bearing.
**A completion-level sign test under a binding cap must not be re-frozen.** The worker's `q_O` sensitivity (V13) shows
the outside option *does* move the unfilled share, which is the right margin for this channel.

### 5.3 The Tier O quality collapse — **re-declare the mapping; do not search the grid**

**Finding (accepted):** `q_O_mult = 0.55` → `surv_O = 0.508 / 0.476 / 0.479 / 0.501`, and with a Tier O share of
60–85 % of places the level collapses (primary **51.63**, upper **33.68**). V13: **no declared grid cell reaches the
bars** (max primary **61.84** at `q_O = 0.70`).

**Ruling.** The defect is **modelling**, not calibration: the declared quality discount is fed through the **same
survival exponent as the untiered system** (`surv = surv_max · Q^θ`, `θ = 1.0` for the first three levels), so a
**free multiplier on tier quality sets the system's level**, with nothing observing it. That is the wrong margin for
the user's own definition — A5 places Tier O's low quality in the **return** ("low quality and **low return**;
take-up is an equilibrium"), i.e. in the **utility/take-up** comparison that produces **unfilled places**, not in the
conditional survival of pupils who enrol. Obligations:
- **(i)** the repair must **locate the quality discount at the return/take-up margin**, which is the object the
  representation check is about;
- **(ii)** if a survival penalty is retained, it must be **declared separately**, with its **own value, its own
  justification written before the run, and its own sensitivity**, and every level statement is then reported as
  **conditional on that declared penalty** — not as a property of the class;
- **(iii)** **no parameter may be chosen by reference to `primary 2024 ≥ 92` or `upper ∈ [55,85]`**, and the repair must
  state the rule that fixes the parameters **before** the run. A grid search that lands on a passing cell is
  `FAIL-RE-FIT`;
- **(iv)** since V13 shows the current grid cannot reach the bars, the **(b) family of level bars must be retired for
  the successor** and replaced by the **observed-cell count bar** (EXP-7's own **≥17/33 within ±5 pp**, derived from the
  observed panel, not from v1.3) plus the declared **±5 y** crossing tolerance (D34/A6). Scoring a v1.5 successor on
  `[73,77]`/`[55,85]` would encode the very placement error EXP-7 measured.

### 5.4 The mislabelled a-iv leg — **record, never re-score**

**Finding (accepted):** the frozen predeclaration expected `same_level = 0` in **A01**, reasoning from the
**unrationed** upper gate. A01 is `bimodal OFF` **but κ ON**, and the cap rations the upper entry, so the count is
**15**; A00 has **0**; A11 has **15**.

**Ruling.** This is a **pre-run labelling error of the predeclaration's own object** and it is **recorded, not
re-scored**: the leg's `FAIL` stands in the frozen verdict string, the representation claim is supported by the
**correct** contrast (**A00 = 0 vs A11 = 15**), and no document may present the (a) check as a clean PASS or the a-iv
leg as a substantive failure. The error class — **naming an arm by one switch when two switches are orthogonal** — is
logged as a predeclaration-authoring rule for every future arm-based check: **every leg must name the arm by its full
switch tuple.**

### 5.5 What the Council does *not* rule

No re-run, no re-fit, no re-tuning, no arm re-specification of v1.5 (R27/R12). v1.5's verdict string is permanent.
**The repaired generator is a new cell with a new predeclaration** and cannot be described as "v1.5 passing", nor as
an independent test of A5 (§6.4).

---

## 6. The five anchored experiments (D89 standing order)

**Slate (information-gain order):** **KAPPA-FWD #1** · **FLOOR-CLOSE #2** · **LOWER-DEF #3** · **V16-REPAIR #4** ·
**CONV-REG #5 / DROP-FIRST**. All are on-disk only; none re-runs a WT/DT cell, EXP-1/2/3, EXP-6/7/8/9 or an A3-S check
in order to re-score it; none is a toy; none reopens C1–C4; none makes a direction or causal claim; **no paper-test
slate** (D113b); HELD data named, never fabricated. Every number below was re-derived from disk in this session
(D113a) and is cited with its path in `VERIFICATION_023.csv`.

### 6.1 EXP-11 — **KAPPA-FWD**: is the per-system transition ratio a *forward-usable* declared input? (rank **#1**)

1. **First-order link (schooling + cohort flows).** Whether the one-stage transition ratio — the object the batch
   renamed "the ceiling" and the coefficient the next model line is about to carry as a **declared input** — is
   constant enough to be applied **forward** in a system, or only describable **within** the window it was computed on.
2. **What changes if positive vs negative.** **Positive** (`κ-STABLE` and the bound holds out of sample) → κ enters the
   model as a **declared constant per system**, the pipeline link is a forward constraint, and the ceiling question
   stays "what sets κ?". **Negative** (a trend in PHL/KOR/KHM, or bound violations in the 7 hold-out cells) → κ enters
   only as a **within-window description**; the link must be declared a **trajectory input** (a declared path, never
   extrapolated) or dropped as a forward constraint, and every downstream statement about 2025+ inherits that limit.
   Either way the answer is **actionable in the predeclaration before V16-REPAIR is frozen**.
3. **Why it is not a niche.** κ is about to become a parameter. A parameter whose stationarity is untested is the
   "fitted curve treated as a law" failure the step-back rule names — and the batch already contains the failure mode:
   **CHN's ratio runs 0.6448 → 0.9662 while its lower series is flat**. A reader of the first-order question is entitled
   to know whether "the ceiling is a pipeline ratio" means a **system property** or a **window**.
4. **Data on disk (no DATA ASK).** `pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv` — columns `iso3`, `upper_year`,
   `lower_year_used`, `year_offset_used`, `ratio`, `loo_kappa`; **43 pairs** (PHL 8, KOR 19, KHM 11, CHN 5); declared
   pre-2021 medians **PHL 0.9596 / KOR 0.9887 / KHM 0.5950 / CHN 0.7222**; **post-2020 hold-out cells: PHL 2, KOR 3,
   KHM 2, CHN 0 (7 total)**. Declared limitation: **HKG and JPN cannot enter** (zero completion pairs, V14).
5. **Threshold + falsifier (fixed before the run).** *Leg (a) stationarity:* per system, `κ-STABLE` iff
   **|OLS slope of `ratio` on `upper_year`| ≤ 0.005 per year** **and** the **first-half vs second-half LOO median
   differ by ≤ 2.0 pp**; else `κ-TRENDING`. *Leg (b) temporal hold-out:* for each system with a pre-2021 κ, predict the
   post-2020 cells as `upper_t ≤ κ_pre · lower_{t−3}`; `BOUND-HOLDS` iff **≥ 6 of the 7** hold-out cells are within the
   bound; `BOUND-BREAKS` iff **≥ 2** violations. **Verdict: `FORWARD-USABLE` iff (a) all three of PHL/KOR/KHM are
   `κ-STABLE` and (b) `BOUND-HOLDS`; `WINDOW-ONLY` otherwise.** **Falsifier:** a PHL slope > 0.005/yr or ≥ 2 hold-out
   violations → `WINDOW-ONLY`, and **no downstream predeclaration may treat κ as a forward constraint**.
   Report all 43 ratios and all 7 hold-out cells; no threshold may move after results.
6. **Closed-claim check.** Does **not** re-score EXP-6 (different estimand: out-of-sample *in time* and a trend slope,
   not LOO in-sample); EXP-6's `PREDICTIVE (3/4)` stands regardless of this outcome. No re-fit (κ values are observed
   medians), no C1–C4 reopening, no direction claim. A `WINDOW-ONLY` verdict is not a falsification of the pipeline
   reclassification — it bounds its **use**.
7. **Cost / rank.** **Small** (one deterministic script, read-only, no RNG). **Rank #1.**

### 6.2 EXP-12 — **FLOOR-CLOSE**: what closes the model's floor gate — places, cohort, or a declared crowding allowance? (rank **#2**)

1. **First-order link (government capacity / schooling supply).** Whether the model's **floor universalization** — the
   one level where its level match is plausible (primary median **−4.30 pp**, D126) — is delivered by **capacity**,
   by **cohort decline**, or by the declared **`phys_cap = 1.15` crowding allowance** that lets 115 pupils occupy 100
   adequate places.
2. **What changes if positive vs negative.** **`ALLOWANCE-CARRIED`** → **A10/D62's "capacity buys the floor" must be
   restated** as conditional on a declared crowding convention, no capacity-mechanism claim may rest on the floor until
   a measured places/PTR series exists (**HELD**), and the repair must report the floor's dependence on `phys_cap` as
   a sensitivity. **`CAPACITY-CARRIED`** → the A10 statement survives at the floor and the capacity channel has a
   measured footprint in the model. **`DEMAND-CARRIED`** → the model's floor universalization is **demographic**, which
   changes what the model may claim about schooling supply altogether.
3. **Why it is not a niche.** It decides whether the programme's **government-capacity channel** has any footprint it
   can defend, and it tests a claim already recorded as a disposition (D62/A10). A reader of "schooling, government and
   markets each stand the others up" is entitled to know whether the model's floor is bought by capacity or by a
   convention.
4. **Data on disk (no DATA ASK).** `generator_v1_2/results/synthetic_panel_v1_2.csv` — `seats`, `cohort`,
   `demand_official`, `admitted_official`, `seat_coverage`, `congestion_q`; panel indexed by level, year and
   country (30 types × 4 levels × 56 years); `generator_v1_2/PARAMS.md` — **`phys_cap = 1.15` (DECLARED)**, **`overage_cap = 1.05`
   (CONVENTION)**; capacity rule `min(phys_cap·seats, overage_cap·cohort)`. Motivating cell (Council re-derivation,
   **V10**, not a result): the anchor's primary gate closes in **2019** at `seat_coverage = 0.8722`, and the binding
   term switches from `1.15·seats` to `1.05·cohort` in **2023**.
5. **Threshold + falsifier (fixed before the run).** For every level×country cell in which a gate closes (first year
   with `p_off = 1.0` after ≥ 3 binding years), decompose the change in `log(capacity/demand)` from the last binding
   year to the closing year into **three** declared terms — (i) `log seats`, (ii) `log cohort`, (iii) `log phys_cap` —
   under a declared **equal-split (Shapley) attribution over 3 factors** — computed **on the binding branch of the
   `min`**, so the `phys_cap` term is identically zero in cells where `1.05 · cohort` is the smaller term (those cells
   are reported separately and cannot carry the allowance leg). Panel verdict = the **majority label** over cells: `ALLOWANCE-CARRIED` iff (iii) ≥ **50 %** of the log change in **≥ 50 %** of cells; `CAPACITY-CARRIED` if
   (i) ≥ 50 % in ≥ 50 %; `DEMAND-CARRIED` if (ii) ≥ 50 % in ≥ 50 %; `MIXED` otherwise. **Falsifier:** fewer than
   **30** closing cells → `UNDETERMINED`, and the A10 statement is then marked **untested**, not confirmed. Report the
   anchor cell separately so that V10 can be checked against the panel.
6. **Closed-claim check.** Read-only on a frozen panel; **no re-fit, no new parameter, no `phys_cap` change** — the
   experiment must **not** re-run the model with `phys_cap = 1.0`: a counterfactual re-run would be a new cell with its
   own predeclaration, and the decomposition already answers the question arithmetically. No direction claim; does not
   reopen CEIL-ATTRIB or A3-S; does not touch the demand line.
7. **Cost / rank.** **Small.** **Rank #2** — it can **retract a recorded disposition** (A10/D62 scope), which is the
   highest-value class of result the Council can obtain on disk right now.

### 6.3 EXP-13 — **LOWER-DEF**: where does the lower-secondary series lose its 13.35 pp? (rank **#3**)

1. **First-order link (cohort flows + schooling supply, with measurement).** Whether the **named defect** of the whole
   generator line — the lower-secondary series, **required 80.76 vs realised 67.4073** (V12) — is a **rationing**,
   a **survival/quality**, or a **convention** problem, since the repair's target depends on which.
2. **What changes if positive vs negative.** **`RATIONING-CARRIED`** → the repair must act on the **lower gate**
   (`admitted_official/cohort`, 0.783805 in 2018), which is a **capacity** object. **`SURVIVAL-CARRIED`** → it must act
   on the **quality/congestion → survival** law (`0.781819` in 2021), which is a **tier-quality** object and connects
   directly to §5.3. **`CONVENTION-CARRIED`** → the `m = 1.10` constant or the duration vector is doing it, which is a
   **measurement** problem. **`JOINT`** → no single lever is admissible and the repair must move both, with a declared
   joint target. In every case the repair's parameter provenance is fixed **before** V16-REPAIR runs.
3. **Why it is not a niche.** It is the one number that every level claim in v1.2/v1.3/v1.4/v1.5 inherits: EXP-7's
   class **b2** says the **lower** series is the binding defect, and v1.5 widened the gap (**A11 lower 2021 = 43.73**,
   **37.03 pp** short). Without this decomposition the repair would be guessing which block to change — which is how
   target-fitting starts.
4. **Data on disk (no DATA ASK).** `synthetic_panel_v1_2.csv` — `completion_uis`, `completion_cohort`, `survival`,
   `admitted_official`, `cohort`, `measurement_factor` (lower_secondary, SYN00_PHL_LIKE, 2017–2021);
   `generator_v1_2/code/sim_v1_2.py:604-610` and `DVEC = (6,3,3,4)` (lower duration **3**); observed reference
   `UNIVERSALIZATION_SERIES.csv` (`completion_lower_secondary`, PHL 2021 = **80.896**). Verified chain:
   `1.10 × 0.783805 × 0.781819 = 0.674073` = the delivered `completion_uis` **exactly**.
5. **Threshold + falsifier (fixed before the run).** Declared log decomposition
   `ln comp = ln m + ln(adm_rate at t−3) + ln surv`; attribute the gap `ln(0.8076) − ln(0.674073)` (i.e. to the
   **required 80.76**, re-derived as `76.6391/0.949`) across the three factors under a declared **equal-split
   (Shapley) attribution**. **`X-CARRIED` iff factor X ≥ 50 % of the gap; `JOINT` iff the two largest factors are within
   **10 percentage points** of each other; `UNDETERMINED` if the chain identity fails in any scored year (tolerance
   1e-9).** **Falsifier:** if the chain does not reproduce `completion_uis` exactly, the accounting is not the one
   executed and the experiment reports `UNDETERMINED` — it does **not** re-derive its own model. Secondary
   (non-verdict-bearing): the same decomposition on **all 30 country types**, and the width of the gap at 2017, 2022,
   2024, so the Lead can see whether the shortfall is local to 2021.
6. **Closed-claim check.** Pure arithmetic on frozen output plus one frozen code line; **no re-fit, no new parameter, no
   re-run, no re-scoring of EXP-7**. Does not reopen class **b2** or the endpoint object; makes no claim about observed
   Philippine cause.
7. **Cost / rank.** **Small.** **Rank #3** — it is cheap, it gates the repair's parameter choice, and it is the
   "one thing that mattered" of the step-back.

### 6.4 EXP-14 — **V16-REPAIR**: the repaired generator, on declared parameters, scored on the observed path (rank **#4**)

1. **First-order link (schooling + cohort flows + markets, at the level).** Whether the two-tier class can hold the
   **coexistence** *and* a **level pattern**, once the κ link is bounded at the right object, Tier O quality acts on
   **take-up** rather than on survival, and the outside option is tested on a margin it can move.
2. **What changes if positive vs negative.** **Positive** (representation holds **and** the path bar is met) → the class
   becomes a **candidate level model** for PHL and the next question is what sets κ and the tier share. **Negative**
   (representation holds, path fails) → the class is recorded as a **representation-only** capability and the ceiling
   remains **UNATTRIBUTED** (a stronger, cleaner negative than v1.5's). **Falsifier fires** → no successor is built this
   phase and the level question is closed at `UNABLE`.
3. **Why it is not a niche.** It is the only path by which the user's structural requirement (D124) can become a model
   that also reproduces the record, and the batch's own decomposition shows the pattern failure is attributable to the
   **tier block**, not to the pipeline link (arm A01 alone: primary **100.0**, lower **85.87**, upper **55.66**).
4. **Data on disk (no DATA ASK).** Frozen `generator_v1_5_bimodal/code/sim_v1_5_bimodal.py`; frozen v1.3/v1.5 panels;
   `UNIVERSALIZATION_SERIES.csv` for the **33 observed cells**; `PARAMETERS.csv` for the declared prov (all parameters
   labelled DECLARED / DERIVED / CONVENTION, **none FITTED**). **HELD** (named, unused): DepEd/CHED seats-vs-enrolment,
   private/public shares, SHS voucher take-up, capacity utilisation.
5. **Threshold + falsifier (fixed before the run).** **Primary bar: EXP-7's own, unchanged — ≥ 17/33 observed cells
   within ±5 pp**, plus crossing years within **±5 y** (D34/A6). Reported, **not** verdict-bearing: upper 2024, the
   `[55,85]` stall band, and the ratio audit. **Four binding design obligations** (§5): **(i)** κ bounded in completion
   units with the survival allowance explicit and **per-system** for the four declared systems (single **0.949
   labelled PHL-derived default** for the other 26 — never described as a per-system value); **(ii)** the guard restated
   as a **counterfactual identity** + propagation ledger + one-way order; **(iii)** Tier O quality at the **return/
   take-up** margin, any survival penalty separately declared; **(iv)** the child-wage shock tested in **A10** with a
   sign derived before the run. **Falsifier: `FAIL-RE-FIT` if (a) any parameter is chosen by reference to the 17/33
   bar or the `[55,85]` band, (b) the A00 arm is not byte-identical to `47d4b082…`, or (c) a within-year feedback from
   the capped economy into same-year admission is found and not declared.**
6. **Closed-claim check.** A **new cell** with a new predeclaration; **v1.5's verdict stands and is not re-scored**
   (no a–e check is re-frozen); **not** an independent test of A5 (its parameters are post-observation) — the
   predeclaration must say so in its first paragraph; **not** a scaling-repair iteration (R27 untouched); **not** a
   re-tune of A3-D (KILLED); no C1–C4 reopening; no direction claim; D63 stays `UNABLE`.
7. **Cost / rank.** **Medium–large** (build + run + audit). **Rank #4** — the largest single information gain but the
   only member whose design depends on two others (KAPPA-FWD's verdict on forward-usability; LOWER-DEF's target), so it
   is ranked below them and must not be predeclared before both return.

### 6.5 EXP-15 — **CONV-REG**: which object carries which statement (completion / GER / `m`)? (rank **#5 / DROP-FIRST**)

1. **First-order link (measurement for every level claim).** Whether the three objects the programme uses
   interchangeably in prose — `completion_uis`, `completion_cohort` and `ger` — may in fact stand for one another, per
   system and level, and what the `m = 1.10` convention actually converts.
2. **What changes if positive vs negative.** **Positive** (`INTERCHANGEABLE` within the declared band) → level
   statements may use either object and the register is short. **Negative** → a **binding register** is issued: which
   object carries which statement, per system×level, and every future predeclaration and results table must cite it;
   GER-derived level statements are **barred** where `NOT INTERCHANGEABLE`. Either way the error class that produced
   three known defects (**WT5's cross-year ratio**, **v1.2 FINDINGS §1.2's `1.136`**, **GER as a pipeline numerator**)
   gets a declared rule instead of a repeated review note.
3. **Why it is not a niche.** Every claim the programme has made about a level is a claim on one of these three
   objects, and D118 established that the ratio has **exactly one** admissible numerator. A model whose next run will
   be scored on **observed cells** must know which observed object it is scored against.
4. **Data on disk (no DATA ASK).** `UNIVERSALIZATION_SERIES.csv` (`completion_primary`,
   `completion_lower_secondary`, `completion_upper_secondary`, `ger_primary`, `ger_lower_secondary`,
   `ger_upper_secondary`, `status = observed`) for PHL/KOR/KHM/CHN; `synthetic_panel_v1_2.csv` (`completion_uis`,
   `completion_cohort`, `measurement_factor`, `ger`); `data/gmr_observed_6countries_1970_2024.csv` (`ger_*`).
5. **Threshold + falsifier (fixed before the run).** Per system×level: `INTERCHANGEABLE` iff
   **`completion/GER ∈ [0.85, 1.15]` in ≥ 80 % of its cells AND `max − min ≤ 0.30`**; else `NOT INTERCHANGEABLE`. For
   the model panel: the m convention holds iff **`completion_uis / completion_cohort = 1.10 ± 1e-9` in every cell**.
   **Falsifier:** a single model cell where `completion_uis/completion_cohort ≠ 1.10` → the m convention is **not**
   applied uniformly and **no statement of the form "m converts X to Y" may be made**; a system×level with
   `completion/GER` outside the band in **> 20 %** of cells → GER barred from that level's statements.
6. **Closed-claim check.** Read-only, arithmetic, **no re-fit**; does **not** re-derive V6 (V6 established that GER is
   not a pipeline numerator for the *ratio*; this establishes interchangeability **per level and system** for *level*
   statements). No C1–C4 reopening, no direction claim.
7. **Cost / rank.** **Small.** **Rank #5 / DROP-FIRST** — it produces a register, not a result; most of its inputs are
   already on disk; and nothing in the model's behaviour changes because of it. It is kept at all only because the
   repair will be scored on observed cells and must know which object it is scored against.

### 6.6 Slate table, drop-first, sequencing

| rank | token | channel (D89-i) | data | cost | one-line discriminative question |
|---:|---|---|---|---|---|
| **#1** | **EXP-11 KAPPA-FWD** | schooling / cohort flows | 43 pairs + 7 hold-out cells, on disk | small | Is κ a forward constraint or a within-window description? |
| **#2** | **EXP-12 FLOOR-CLOSE** | government capacity | frozen v1.2 panel + `PARAMS.md` | small | Is the floor bought by capacity, by demography, or by a 15 % crowding allowance? |
| **#3** | **EXP-13 LOWER-DEF** | cohort flows + measurement | frozen panel + one code line + observed | small | Which of rationing / survival / convention loses the 13.35 pp? |
| **#4** | **EXP-14 V16-REPAIR** | schooling + markets, at the level | frozen code + observed 33 cells | medium–large | Can the class hold the coexistence **and** the path on declared parameters? |
| **#5** | **EXP-15 CONV-REG** | measurement | observed + model panels | small | Which object may carry which level statement? |

**Drop-first: CONV-REG.** It changes no model behaviour, most of its inputs are already tabulated, and its one
decision-relevant output (which object the repair is scored on) can be carried by a single register line inside the
V16 predeclaration if the Council must cut a slot. **Dependency order (binding): KAPPA-FWD ∥ FLOOR-CLOSE ∥ LOWER-DEF
first; V16-REPAIR only after KAPPA-FWD and LOWER-DEF return; CONV-REG last or dropped.** Nothing downstream may be
predeclared before its inputs land: **κ's forward-usability and the lower-series target are the two predeclaration
inputs of the repair**, and V16-REPAIR's frozen predeclaration must cite their hashes.

---

## 7. Labels, limits, data

- **Labels.** Every generator number here is `SYNTHETIC`; every observed comparison is `OBSERVED`; every behavioural
  assumption is `DECLARED`; V9–V15 are **Council-side re-derivations**, not new evidence and not a re-score. **No
  direction or causal claim is made anywhere in this brief.** D63 remains `UNABLE as to cause`; V15 is a **necessary
  condition**, not a forecast. The phase verdict (D76/D77: PARTIAL/DESCRIPTIVE/EQUIVALENT, scaling FAIL standing) is
  untouched and no on-disk test can move it.
- **Limits.** (i) κ is estimated on **43 pairs across 4 systems**, with **HKG and JPN non-entrant** and **CHN
  non-stationary**; the temporal hold-out is **7 cells**, so a single flip moves the verdict. (ii) V10 is **one cell**
  (anchor primary); FLOOR-CLOSE is the panel-wide test. (iii) V11 is the **anchor type, one year**; the propagation
  ledger must be panel-wide. (iv) V15 uses κ = 0.9491 (all PHL pairs); at κ = 0.9596 (pre-2018) the implied upper
  maximum is 88.680 instead of 87.710. (v) The v1.5 level numbers are readable only as **2022–2024 placement**
  statements (D119).
- **HELD (named, never fabricated, no external request).** **Upper-secondary completion for additional systems** (the
  only way to strengthen EXP-6's 3/4 — V14); HKG single-age population 1971–1996; HKG senior-secondary queue/places;
  PSA microdata; WB Enterprise Surveys; real per-pupil spending; annual capacity/enforcement; a measured
  credential-queue (rung-4) series; DepEd/CHED seats-vs-enrolment, private/public shares, SHS voucher take-up, capacity
  utilisation; PHL/KHM/CHN/JPN shadow participation; measured remittance→schooling coefficient. **Nothing was sent;
  user approval required.**
- **Process.** No bridge post attempted (D87); no external message; **no model code executed**; no data file written;
  no write outside `08_council/brief_023/`; `DECISIONS.md`, `BIG_PICTURE.md`, `COUNCIL_STATE.md` untouched (the Lead
  merges).

---

## 8. For the Lead's merge (BIG_PICTURE / COUNCIL_STATE delta)

- **BIG_PICTURE — KEEP/PARK/KILL:** keep the **transition-ratio object with a per-system κ**; add **"single global κ"**
  to KILL; add **"scoring a v1.5 successor on `[73,77]`/`[55,85]`"** to KILL; move HKG to **`DEFER-HKG`**; move
  **V16-REPAIR** to KEEP-NEW as a **capability** run; keep A10 but **mark it conditional on `phys_cap = 1.15`** pending
  FLOOR-CLOSE.
- **Header line to add above the model line:** `PIPELINE: per-system κ (PHL 0.9491 / KOR 0.9898 / KHM 0.5950 / CHN
  0.7222; spread 0.395) — forward-usability UNTESTED (EXP-11) — CHN non-stationary, not used forward.`
- **COUNCIL_STATE:** cycle-15 note = five results adjudicated (two ACCEPT, three ACCEPT-WITH-CONDITIONS), the **κ guard
  ruled mis-specified**, four v1.5 records corrected, **EXP-10 not delivered → `DEFER-HKG`**, five experiments with
  **KAPPA-FWD #1** and **CONV-REG drop-first**; next actions = predeclare KAPPA-FWD, FLOOR-CLOSE, LOWER-DEF in
  parallel, then V16-REPAIR.
- **No claim in this brief may be copied into the A1 write-up** except the V15 necessary-condition arithmetic (with its
  κ value and its "not a forecast" label) and the D119/EXP-7 label sentence.

---

## 9. Files written this cycle

| file | contents |
|---|---|
| `08_council/brief_023/SYNTHESIS_023.md` | this document — step-back, V9–V15 verification, five adjudications, dispositions, the v1.5 defect rulings, the five anchoring blocks |
| `08_council/brief_023/PROPOSED_DECISIONS.md` | six decisions in house format, `D?` = D132+ |
| `08_council/brief_023/VERIFICATION_023.csv` | every number in §1–§6 with its path and re-derivation, machine-readable for the Lead |

**Nothing else was written. No file was edited outside `08_council/brief_023/`. No model code was executed and no data
file was written.**

---

*Council-2 (synthetic composite panel), cycle 15 — 2026-11-21 00:20 +08:00. Research direction, not evidence. The
composite personas are AI-constructed; no living scholar is quoted, paraphrased or represented.*
