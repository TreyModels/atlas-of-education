# PRE_DECLARATIONS — WT1–WT5 predeclared test battery

**Brief:** `08_council/brief_019/SYNTHESIS_019.md` §C (D98–D101; D89 standing order).
**Worker:** WT (worker id `wt_2026-11-20`).
**Written:** 2026-11-20, before any run of `code/run_wt.py`.

> **This file was written before any run; its sha256 is recorded in `RUN_MANIFEST.json`; no threshold,
> falsifier, qualifying rule or verdict word is changed after results are seen.** If a run later shows a
> threshold to be badly specified, that is reported as a finding about the test — the threshold still governs
> the verdict. The five blocks below are copied **verbatim** from the Council brief (extracted by line range,
> not retyped: `SYNTHESIS_019.md` lines 105–232, plus the slate ranking at lines 234–238).

**Status labels used everywhere in this deliverable**

| label | meaning |
|---|---|
| **OBSERVED** | a value read directly from an on-disk series, no transformation |
| **DERIVED** | arithmetic/statistical construction from OBSERVED series (the test statistics) |
| **HELD** | named data known to be absent from disk. **No number is ever reported for a HELD cell.** |

**Scope discipline.** Descriptive only. No causal claim, no push/pull direction claim, no reopening of C1–C4,
no toy, no external data request, no web. A WT **PASS is a descriptive footprint, not validation of the paper.**

---

## 1. Inputs (all read-only; exact paths)

| id | path | role |
|---|---|---|
| IN1 | `09_relations/data/panel_wdi_long.csv` | long WDI panel, columns `iso3,country,indicator,year,value` |
| IN2 | `10_massification/data/UNIVERSALIZATION_SERIES.csv` | PHL detail series (completion, GER), `status=observed` rows |
| IN3 | `09_relations/data/economic_complexity_panel_30ctys.csv` | `eci_sitc` complementarity proxy |
| IN4 | `09_relations/data/shadow_gradients.csv` | WT5 on-disk gradient tabulation |
| IN5 | `04_data/TARGETS_SHADOW.csv` | WT5 HKG 2010 gate rates; PHL/KHM/CHN/JPN unresolved |

Indicators used: `SE.PRM.CMPT.ZS`, `SE.SEC.CUAT.UP.ZS`, `SE.SEC.CMPT.LO.ZS`, `SE.TER.ENRR`, `SE.ADT.LITR.ZS`
(WT1); `SE.TER.ENRR`, `SL.AGR.EMPL.ZS`, `SE.TER.CUAT.BA.ZS`, `SL.UEM.1524.ZS` (WT2); `SE.SEC.CUAT.UP.ZS`,
`SL.AGR.EMPL.ZS`, `NY.GDP.PCAP.KD` (WT3); PHL `completion_upper_secondary`, `ger_tertiary`,
`completion_primary`, `completion_lower_secondary` (WT4).

**No series is fabricated.** Rows are used only where `status` is `observed` (IN2) or present in IN1/IN3.
Missing years are absent rows and are **never interpolated**.

---

## 2. The five anchoring blocks — VERBATIM from `SYNTHESIS_019.md` §C

<!-- BEGIN VERBATIM COPY: SYNTHESIS_019.md lines 105-232 -->
All five: one deterministic script each, disjoint write scopes, **no direction claim, no toy, no C1–C4 reopening**.
WT1–WT4 are descriptive on-disk tests; WT5 is a design-only HELD ask. The Lead copies these blocks verbatim.

### WT1 — Asymmetric adjustment: adoption fast, exit slow (Prediction 1 + "Hysteresis Is Not Irreversibility")
1. **Paper prediction.** "The cost of abandoning the scaffold is not the inverse of the cost of adopting it"; more
   specifically `C(B→A′) > C(A→B)` (§258–283, Prediction 1). Corollary: in the observed series, *declines* (movement
   toward the predecessor state) should be **fewer and shallower** than *advances* of comparable size.
2. **First-order link (channel):** **schooling + cohort flows** — the phase's central unreproduced object is the
   anchor asymmetry; this asks whether "asymmetric cost of exit" has *any* observable footprint in the one dataset we
   own, before the paper is given model status.
3. **Discriminating action.** *positive* (falls systematically fewer and shallower than rises within-series) → the
   paper's return-path asymmetry has a descriptive footprint; the exit-cost account survives to WT2–WT4 and a declared
   model layer is *considered*. *negative* (symmetric rise/fall dynamics) → the paper adds nothing at this granularity
   and is parked as a rival with no empirical footprint.
4. **Why not a niche.** It is the cheapest possible operationalization of the paper's single defining claim; a reader
   of the first-order question ("does massification reverse symmetrically?") cares directly.
5. **Data on disk.** `09_relations/data/panel_wdi_long.csv` (columns `iso3,country,indicator,year,value`; indicators
   `SE.PRM.CMPT.ZS` n=712/28, `SE.SEC.CUAT.UP.ZS` n=459/30, `SE.SEC.CMPT.LO.ZS`, `SE.TER.ENRR` n=1074/30,
   `SE.ADT.LITR.ZS`); `10_massification/data/UNIVERSALIZATION_SERIES.csv` (PHL completion CR.1/CR.2/CR.3 + GER.5T8,
   incl. the 2016→18 tertiary dip −10.2 pp and the 2018→21 primary GER fall 99.4→88.8). No DATA ASK.
6. **Threshold + falsifier (fixed).** Per qualifying series (n≥15 observed years), define a **rise-run** = ≥2
   consecutive years of positive Δ with cumulative Δ ≥ **+3 pp**; a **fall-run** = ≥2 consecutive negative Δ with
   cumulative Δ ≤ **−3 pp**. Support (descriptive) iff, aggregated across all qualifying series: (a) `#fall-runs ≤
   0.5 × #rise-runs` **and** (b) `median|fall depth| ≤ 0.5 × median|rise depth|`. **Falsifier** = either ratio > 0.5 →
   record "symmetric adjustment; no return-path-asymmetry footprint at this granularity".
7. **Closed-claim check.** No C1–C4 reopening; descriptive episode-count asymmetry only; no push/pull or causal claim
   (R13-safe). **Caveat recorded:** the panel is an expansion era, so "falls are rare" is partly exogenous — WT1 is
   *partially diagnostic*, reported with that caveat.
8. **Cost / rank:** **small.** **Rank #1.**

### WT2 — Credential decoupling: adoption continues after the destination saturates (credential application + Prediction 1)
1. **Paper prediction.** "The resulting equilibrium can persist even if the credential becomes only weakly related to
   job-specific competence" (§321–331); Prediction 1 (adoption alters reverse costs). Corollary: credential *adoption*
   (enrolment/completion) should **not reverse** as the credential's *destination* (formal-sector rungs) saturates.
2. **First-order link (channel):** **markets + schooling** — this is the user's "marginal graduate when the office rung
   fills" question (external review §9: genuinely open), restated as an on-disk decoupling test.
3. **Discriminating action.** *positive* (credentials grow while the formal destination is flat/slower, and enrolment
   does not reverse) → the persistence signature of a credential scaffold is present; the queue story gains a
   descriptive on-disk footing. *negative* (enrolment tracks the destination — stalls/reverses when the rung fills) →
   the credential-queue reading has no on-disk footprint and the ceiling must be explained by something else.
4. **Why not a niche.** It is the paper's signature credential-hysteresis claim, and it is exactly the absorption/
   composition margin the user made first-order (A3).
5. **Data on disk.** `09_relations/data/panel_wdi_long.csv` (`SE.TER.ENRR` tertiary GER; `SE.TER.CUAT.BA.ZS` tertiary
   attainment n=230/27; `SL.AGR.EMPL.ZS` → formal-non-agric share `=100−SL.AGR.EMPL.ZS`, 30 cty; `SL.UEM.1524.ZS` youth
   unemployment). **HELD (named, never fabricated):** the credential **wage premium** time series — PSA microdata
   (FIES/LFS) and WB Enterprise Surveys; the external facts (39% overeducated, flat graduate wages) are **cited, not
   measured** (D49).
6. **Threshold + falsifier (fixed).** Per country with ≥15 y of both series: `D_cred` = % growth of tertiary GER
   1995→2024; `D_dest` = change (pp) in formal-non-agric employment share over the same window. **Decoupled** iff
   `D_cred > 0` and `D_dest < D_cred`. Support iff decoupled in **≥50% of qualifying countries** **and** in **≥2/3** of
   the decoupled countries there is **no** ≥5 pp tertiary-GER reversal sustained ≥3 y within the window. **Falsifier**
   = decoupled in <50%, or reversal in >1/3 of decoupled countries.
7. **Closed-claim check.** Descriptive; no direction/causal claim (the reverse-order issue is not estimated here); the
   wage-premium version is **C3/HELD** and is **not** reopened by this on-disk decoupling test.
8. **Cost / rank:** **medium.** **Rank #2.**

### WT3 — Complementarity → persistence (Prediction 4)
1. **Paper prediction.** "Scaffolds surrounded by dense complementary investment should display greater persistence
   following deterioration of their original adoption advantage" (§492–494).
2. **First-order link (channel):** **markets (sector structure) + schooling** — the comparative claim that persistence
   scales with the *depth* of the credential's complementary economy, the paper's most general testable prediction.
3. **Discriminating action.** *positive* (income-partial persistence rises with complementarity) → Prediction 4 has a
   descriptive footing and a declared complementarity→persistence layer is *considered* for the generator. *negative*
   (no partial association, or it is absorbed by income — the Y1 lesson) → Prediction 4 has no on-disk footprint;
   complementarity is parked.
4. **Why not a niche.** It is the only one of the paper's five predictions that is genuinely *comparative* and can be
   approached with our 30-country panel.
5. **Data on disk.** `09_relations/data/panel_wdi_long.csv` (`SE.SEC.CUAT.UP.ZS` upper-sec attainment, n=459/30;
   `SL.AGR.EMPL.ZS`; `NY.GDP.PCAP.KD` income); `09_relations/data/economic_complexity_panel_30ctys.csv` (`eci_sitc`
   complementarity proxy). No DATA ASK.
6. **Threshold + falsifier (fixed).** Persistence proxy = upper-sec attainment **saturation ceiling** (max 1995–2024)
   and **reversal count** (≥3 pp negative Δ years after detrending). Complementarity proxy = median `eci_sitc` and
   formal-non-agric share. Metric = **income-partial Spearman ρ**. Support iff `|ρ(persistence, complementarity |
   log income)| ≥ +0.40` **and** the sign is retained after income control. **Falsifier** = |income-partial ρ| < 0.40
   or sign flips on income control.
7. **Closed-claim check.** No C1–C4 reopening; cross-sectional descriptive association, no direction claim (R13);
   **n=30, power low** — reported as descriptive, never as a law.
8. **Cost / rank:** **medium.** **Rank #4.**

### WT4 — The PHL ceiling as a scaffold that cannot be exited (credential application + Discussion)
1. **Paper prediction.** "A credentialed labor market cannot instantly revert to reputation-based hiring while
   preserving every organization designed around standardized qualifications" (§544); Prediction 1. Corollary: the PHL
   upper-secondary ceiling should show **zero exit episodes** — it should not revert toward its predecessor level —
   even through dated shocks.
2. **First-order link (channel):** **government (policy) + schooling** — formalizes, predeclared, the anchor's central
   unreproduced fact (ceiling never ≥90) as "what exit would look like and why we never see it."
3. **Discriminating action.** *positive* (zero exit episodes through the K-12/free-tuition/cohort shocks, while the
   same shocks moved other levels) → the "cannot be exited" reading is *consistent* with the record and the paper's
   account survives as the leading (still-undemonstrated) candidate for the D63 ceiling residual. *negative* (an exit
   episode occurs) → the "cannot be exited" claim is false on this record.
4. **Why not a niche.** The 15.0-pp ceiling residual is the single object the phase could not explain; this is its
   first predeclared operationalization.
5. **Data on disk.** `10_massification/data/UNIVERSALIZATION_SERIES.csv` (PHL CR.3 upper-sec completion; GER.5T8
   tertiary GER); `10_massification/data/POLICY_TIMELINE.csv` (K-12 2013/2016; free tertiary 2018); `STATE_CAPACITY.csv`
   + R11/CAP-03 (capacity improves 2005–2017 while ceiling flat). No DATA ASK.
6. **Threshold + falsifier (fixed).** Define an **exit episode** = upper-secondary completion falling **≥5 pp below
   its 2017 peak (76.43)** for **≥3 consecutive years** without recovering to within 2 pp of the peak by 2024; or
   tertiary GER falling **≥5 pp below its 2016 level (38.35)** for ≥3 y without recovery. Support iff **zero** exit
   episodes in upper-sec completion 1999–2024 **and** the tertiary 2018 dip (−10.2 pp) recovers to **≥50 by 2025**
   (already observed). **Falsifier** = an exit episode occurs.
7. **Closed-claim check.** No C1–C4 reopening (the *discriminating* queue test remains C3/HELD); this is descriptive
   confirmation of the known non-response, predeclared, no direction claim.
8. **Cost / rank:** **small.** **Rank #3.**

### WT5 — Shadow education as adoption of a positional scaffold at gates (Forward Path + credential application) — DESIGN-ONLY
1. **Paper prediction.** "Adoption can diffuse even among actors who would prefer a world in which no competitor
   adopted the scaffold" (§93–101); credential scaffolds are adopted at the gate. Corollary: shadow demand
   **concentrates at the credential gate**, not at primary — tutoring is a positional scaffold adopted at the queue.
2. **First-order link (channel):** **shadow at the gates (user directive) + markets** — the user's explicit "shadow as
   a demand signal at the gates"; the paper supplies the vocabulary (positional scaffold).
3. **Discriminating action.** *positive* (observed gate gradient: senior-secondary shadow ≥1.5× primary) → consistent
   with shadow-as-positional-scaffold; the v1.3 shadow module (W2) is framed as the real test. *negative* (no gradient)
   → shadow is not gate-concentrated in the data we hold.
4. **Why not a niche.** It is the user's revived shadow direction — but as an *on-disk paper test* it is the weakest:
   it re-tabulates already-known gate concentration (Bray & Kwok 2003) under the paper's vocabulary.
5. **Data on disk.** `04_data/TARGETS_SHADOW.csv` (HKG 2010 primary 45 / lower 72 / middle 82 / senior 85);
   `09_relations/data/shadow_gradients.csv` (HKG 2003 S1-3 35.1 → S6-7 70.3, gate gradient **+35.2 pp**; KOR 2023
   elementary 86 vs high 66.4 participation but **+23% per-student spend** at the high gate). PHL/KHM/CHN participation
   **unresolved on disk** → HELD.
6. **Threshold + falsifier (fixed).** Support iff the observed **gate gradient ≥ 1.5×** (senior-secondary shadow rate
   ≥ 1.5× primary rate) in every system where both are observed (HKG: 85/45 = 1.89; 70.3/35.1 = 2.00), **and** where
   level participation *declines* (KOR), per-student spend **rises** at the gate (+23% already on disk). **Falsifier**
   = no gate gradient (shadow flat or declining toward the gate).
7. **Closed-claim check.** Does **not** reopen the closed shadow incidence/mechanism claim (brief 008/D76); tests only
   the paper's positional-scaffold reading; n tiny and near-circular (re-tabulates known facts) — the *real* shadow test
   is the v1.3 model check d5, not this WT.
8. **Cost / rank:** **small.** **Rank #5 → DROP-FIRST.**
<!-- END VERBATIM COPY -->

Verbatim set ranking (same section):

<!-- BEGIN VERBATIM COPY: SYNTHESIS_019.md lines 234-238 -->
**Slate ranking (info gain):** WT1 > WT2 > WT4 > WT3 > WT5. **Drop-first: WT5** — near-circular re-tabulation of a
known gate gradient; its outcome cannot change the model, and the shadow work that *can* change the model is the
v1.3/W2 module, not this re-read. WT1 is the sharpest on-disk operationalization of the paper's core claim; WT2/WT4
target the PHL ceiling/queue (the phase's open object); WT3 is the comparative prediction but income-confounded and
n=30.
<!-- END VERBATIM COPY -->

**Dispatch note (no threshold content).** §C assigns each test its own write scope
(`experiments/wt1_asymmetry/` … `wt5_shadow_gate/`). The Lead's dispatch for this run consolidates all five
into the single worker directory `10_massification/extensions/wt_2026-11-20/` (D100: "Lead copies blocks
verbatim, predeclare, dispatch in parallel"). The consolidation changes **only** where files are written —
not any estimand, threshold, falsifier or verdict word.

**Deviation register.** No deviation from the blocks' numbers. One *addition* per the Lead's dispatch: WT5 is
run **design-only / on-disk descriptive and is NOT SCORED** (the block itself calls it near-circular and
drop-first; the Lead's instruction fixes it as unscored). This lowers WT5's status; it does not raise it.

---

## 3. Frozen operational readings (mechanics only — **no threshold is changed**)

The blocks fix estimands and numbers but not every mechanical detail (what "consecutive" means on a gappy
annual panel, how a maximal run is delimited, which of several proxies is primary). Those details are **frozen
here, before the run**, so the script cannot choose them after seeing results. Each is the most literal reading
of the block; none alters a stated number.

**M1 — qualification (WT1, literal from block: "n≥15 observed years").** A *series* is one `(iso3, indicator)`
pair from IN1 with **≥15 observed year–value pairs** (any years 1970–2024). IN2 PHL series qualify under the
same rule and are added only if not duplicates (M2).

**M2 — duplicate exclusion.** IN2 repeats PHL series that also exist in IN1 (e.g. `ger_tertiary` ≡
`SE.TER.ENRR`, verified identical to <1e-8 on shared years). A candidate series is dropped from the WT1
aggregate if ≥90% of its years are shared with an IN1 series and max |difference| ≤ 1e-6 on those years
(the IN1 series is kept). Dropped duplicates are reported, not silently merged, so PHL episodes are not
double-counted.

**M3 — Δ and "consecutive years".** Δ is computed between **consecutive observed years**; a missing year is
one Δ step, not an interpolation. A Δ of exactly 0 is neither rise nor fall and breaks a run. A block of ≥2
consecutive same-sign Δ is a *maximal run* iff it is not extendable in either direction by the same sign.

**M4 — run thresholds (verbatim numbers).** A maximal run is a **rise-run** if its cumulative Δ (sum of its
Δs = last value − value before the run) **≥ +3.0 pp**; a **fall-run** if cumulative Δ **≤ −3.0 pp**. Shorter
or smaller blocks are counted as "sub-threshold" and excluded from the counts (reported in DETAIL).

**M5 — WT1 aggregation and verdict.** Pooled across qualifying series: ratio_count = #fall-runs / #rise-runs;
ratio_depth = median|fall-run cumulative Δ| / median|rise-run cumulative Δ| (medians over run depths of the
respective type). **SUPPORTED** iff ratio_count ≤ 0.50 **and** ratio_depth ≤ 0.50. **NOT SUPPORTED** if either
ratio > 0.50 (block's falsifier: "symmetric adjustment; no return-path-asymmetry footprint at this
granularity"). **DATA LIMITED** if the number of qualifying series is 0 or #rise-runs = 0 (ratio unformable).
**Degenerate case:** if #fall-runs = 0, ratio_count = 0 and ratio_depth is set to 0 (no decline at all is
maximal asymmetry, not missing data); the degeneracy is recorded in the components.

**M6 — WT2 window and endpoints.** Window **1995→2024**, both endpoint years must be **observed** in both
series, and each series must have **≥15 observed years**. D_cred = 100·(v_2024/v_1995 − 1) (percent growth of
tertiary GER). D_dest = (100 − SL.AGR.EMPL.ZS_2024) − (100 − SL.AGR.EMPL.ZS_1995) (percentage-point change in
formal-non-agricultural employment share). **Decoupled** iff D_cred > 0 **and** D_dest < D_cred (verbatim
condition). Countries lacking either endpoint are excluded and counted (never proxied by another year).

**M7 — WT2 unit caveat (recorded, not repaired).** The literal criterion compares a *percent growth*
(D_cred) with a *percentage-point change* (D_dest). It is implemented exactly as written. A **diagnostic**
column (D_cred also expressed in pp: v_2024 − v_1995) is reported in DETAIL for the reader, and the caveat
that this makes "decoupled" easy to satisfy is carried into `FINDINGS.md`. The verdict is NOT taken from the
diagnostic.

**M8 — WT2 reversal (verbatim "≥5 pp tertiary-GER reversal sustained ≥3 y within the window").** On
SE.TER.ENRR within 1995–2024: a reversal exists iff there is a year *p* and a later year *t* with
v_t ≤ v_p − 5.0, where v_p is the maximum over p ≤ t, and at least **3 consecutive observed years** from *t*
stay ≤ v_p − 5.0 before any year exceeding v_p − 5.0 (recovery ends the episode). Support iff decoupled in
**≥50%** of qualifying countries **and** reversal in **≤1/3** of the decoupled countries. Falsifier as written:
decoupled <50%, or reversal in >1/3 of decoupled countries.

**M9 — WT3 minimum window (**declared**, mirroring the n≥15 family; no number changes).** A country qualifies
if `SE.SEC.CUAT.UP.ZS` has **≥15 observed years within 1995–2024**. Fewer than 5 qualifying countries →
DATA LIMITED.

**M10 — WT3 persistence proxies (as the block names them).** **P1 saturation ceiling** = max
`SE.SEC.CUAT.UP.ZS` 1995–2024. **P2 reversal count** = number of Δ steps ≤ **−3.0 pp** in the series
**detrended** by OLS on observed years (residual = value − fitted linear trend), Δ between consecutive observed
years. (Raw, non-detrended ≥3 pp falls are reported in DETAIL as a sensitivity only.)

**M11 — WT3 complementarity proxies (as the block names them).** **C1** = median `eci_sitc` 1995–2024.
**C2** = median formal-non-agricultural share `100 − SL.AGR.EMPL.ZS` 1995–2024.

**M12 — WT3 income control (declared).** income = ln(`NY.GDP.PCAP.KD`, year 2015); 2015 is present for all
30 countries. **Income-partial Spearman:** ρ_xy·z = (r_xy − r_xz·r_yz)/√((1−r_xz²)(1−r_yz²)) with all r
Spearman rank correlations. **Primary combination is predeclared as P1×C1** (the block's own "saturation
ceiling" × `eci_sitc`); the other three combinations are reported in DETAIL as robustness and do **not** move
the verdict. **SUPPORTED** iff ρ_partial ≥ **+0.40** and the sign is retained (ρ_partial > 0 and same sign as
raw ρ_xy). **NOT SUPPORTED** iff ρ_partial < 0.40 or the sign flips (block's falsifier). n≈14 → descriptive
only, never a law.

**M13 — WT4 exit-episode mechanics (verbatim numbers).** Upper-secondary anchor = **76.432953 (2017, on
disk)**; peak − 5 = **71.432953**; recovery band = peak − 2 = **74.432953**. **Exit episode (upper-sec)** =
≥**3 consecutive observed years** with completion < 71.432953 **and** no value ≥ 74.432953 by 2024.
Tertiary anchor = **38.344741 (2016)**; below = < **33.344741**; **exit episode (tertiary)** = ≥3 consecutive
observed years below 33.344741 **without** recovery to ≥50 by 2025. "Consecutive years" = consecutive
**observed** years (primary reading, M3), because interpolating the gaps would fabricate observations. The
alternative calendar-span reading is reported as a sensitivity in DETAIL; both are computed and shown.
**SUPPORTED** iff **zero** exit episodes in upper-secondary completion 1999–2024 **and** the tertiary 2018 dip
recovers to **≥50 by 2025** (observed 51.071883). **Falsifier:** an exit episode occurs.

**M14 — WT5 is design-only / NOT SCORED (per Lead dispatch).** No support/falsifier verdict is returned. The
block's tabulation is reproduced as a **tabulation only**: HKG 2010 senior/primary = 85/45, HKG 2003
S6-7/S1-3 = 70.3/35.1, KOR 2023 participation elementary 86 → high 66.4 with per-student spend 398 → 491
(+23.4%). PHL/KHM/CHN/JPN participation is **HELD**. Near-circularity caveat: this re-tabulates a gradient
already held (Bray & Kwok 2003); it cannot change the model. The real shadow test is the v1.3/W2 module (d5).

**M15 — determinism.** No bootstrap, no Monte Carlo, no RNG → **seed = null**. All group orders, sorts and
float formatting are fixed (`%.6f` for reported statistics); no dependence on dict/hash order. The battery is
run twice into separate output directories and the two `RESULTS.csv` / `DETAIL.csv` pairs are required to be
**byte-identical** (sha256 equality); evidence in `RUN_MANIFEST.json`.

**M16 — reporting precision.** Statistics to 6 decimals; components to 6 decimals; counts as integers.
`n` = number of independent units entering the statistic (series for WT1, countries for WT2–WT3);
`n_countries` as stated per test.

---

## 4. Verdict vocabulary (closed list)

`SUPPORTED` · `NOT SUPPORTED` · `DATA LIMITED` · `DESIGN-ONLY` · `HELD`.

`DATA LIMITED` is used only where the frozen rules cannot form the statistic (no qualifying series, no
qualifying countries, undefined denominator). It is **never** used as a euphemism for a null result: a formed
statistic that misses its threshold is `NOT SUPPORTED`. `HELD` rows carry no numbers.

---

## 5. HELD register (named, never fabricated)

| id | held object | why held | consequence |
|---|---|---|---|
| **HELD-1** | credential **wage premium** time series (PSA FIES/LFS microdata; WB Enterprise Surveys) | not on disk; the "39% overeducated / flat graduate wages" facts are external, cited not measured (D49) | WT2's wage-premium version is **not run**; WT2 is an enrolment-vs-destination decoupling test only. The C3 claim is **not** reopened. |
| **HELD-2** | PHL / KHM / CHN / JPN shadow **participation rates** | `TARGETS_SHADOW.csv` rows are `unresolved` with empty values | WT5 reports no number for these systems; they stay unresolved. |
| **HELD-3** | PHL/KHM participation beyond the on-disk gradient; de facto enforcement; individual competence data; withdrawal episodes | not on disk | outside WT1–WT5 scope; no estimate attempted |

---

## 6. What this battery cannot claim (stated before results)

1. A WT PASS is a **descriptive footprint**, never validation of the hysteresis paper, and never evidence that
   the paper's mechanism operates.
2. WT1 is **partially diagnostic at best**: the 30-country panel is an expansion era, so few/shallow falls is
   partly exogenous — the block records this caveat and so do we.
3. WT2/WT4 are **descriptive confirmations of a known non-response** under new vocabulary (low new
   information); WT4's discriminating (queue) version remains C3/HELD.
4. WT3 is **income-confounded by construction** and n≈14 → descriptive association only, no law, no direction.
5. WT5 is **near-circular** and **NOT SCORED**.
6. No causal claim, no push/pull direction claim, no C1–C4 reopening, no model change. The D101 conditional
   (a declared complementarity→persistence term only if WT1 **and** WT3 are both non-null) is a Council gate,
   not something this battery can satisfy on its own — and a WT3 pass here would still be income-partial
   descriptive only.
