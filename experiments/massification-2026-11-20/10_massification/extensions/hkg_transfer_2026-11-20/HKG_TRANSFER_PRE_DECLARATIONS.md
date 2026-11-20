<!-- Worker W3, 2026-11-20. FROZEN SPECIFICATION. This file is written BEFORE any HKG run and is not edited after
     results are seen. Its sha256 is recorded in RUN_MANIFEST.json and HKG_CHECKLIST.md.
     Scope: 10_massification/extensions/hkg_transfer_2026-11-20/ only.
     NOTHING HERE IS A RESULT AND NOTHING HERE IS A CLAIM ABOUT HONG KONG. -->

# HKG TRANSFER — PRE-DECLARATIONS (FROZEN)

**Written:** 2026-11-20 (Asia/Shanghai). **Status:** frozen, unrun. **No HKG result exists at the time of writing**, and none may be produced until every precondition in §7 is met.

**Governing authority:** D75 (`08_council/DECISIONS.md:84`), D40 (`:49`), D61 (`:70`), D74 (`:79`), D76 (`:85`), D77 (`:86`), D93 (`:103`); R13/R20/R22/R28. Dispatch: `10_massification/STATUS.md:757` (§3w, W3 row). Evidence inventory: `HKG_INVENTORY.md` (this directory).

**Label: DIAGNOSTIC-TRANSFER. This is a diagnostic of a frozen simulator, not evidence about Hong Kong, not a validation, not a portability claim, and not a causal or directional statement of any kind.**

---

## 1. The D75 six constraints, restated verbatim in substance and then operationalised

D75 (`DECISIONS.md:84`) requires a later run to satisfy six constraints. **Two numberings are in circulation and they differ**, so both are given: the **transfer-brief numbering 1–6** (the six constraints as issued to this worker) and **D75's own clause numbering (i)–(vi)**, which combines some of them. Each constraint is bound to a **named, checkable rule in this document**. A run that violates any one of them is void.

| # (brief) | D75 clause | Constraint | How this predeclaration binds it |
|---|---|---|---|
| **1** | (i) | **Fixed PHL behaviour**: the PHL parameterisation is frozen — the HKG run may not re-fit it; only declared country inputs are re-set (R20) | §5a lists every **FIXED** parameter; §5b the **DECLARED HKG INPUTS**. Enforced by the **parameter-freeze audit** (§6, PA-1/PA-2), which **aborts** if any FIXED value moves or any parameter is added. |
| **2** | (ii) | **No re-fit to HKG**; no extra free parameters, no target fitting — any occurrence = FAIL, and the moved parameter named | **SR-3**, **SR-6**, **SR-8**. Any re-fit yields `FAIL-RE-FIT`, with the moved object and its before/after value written into `hkg_parameter_freeze_audit.csv`. No parameter is introduced for HKG. |
| **3** | (iii) part 1 | **HKG timing-only**: test only the **TIMING** of crossings, not levels | **TC-1** and **TC-2** (§2) are the **only** verdict-bearing checks; both are crossing-year tests. No level enters any verdict. |
| **4** | (iii) part 2 | **HKG levels: check-only** | **LC-1** (§3) reports levels under a `LEVELS: CHECK-ONLY — NOT A VERDICT COMPONENT` header and is excluded from the verdict and from all aggregation. |
| **5** | (iii) part 3 | **No completion series for HKG — do not impute one**; the timing test uses **NER/GER crossings only**; targets **NER≥90 1974**, **NER≥95 1979** (verified on disk); threshold-specific, **never spliced** | §4 of `HKG_INVENTORY.md` records that HKG has **no** completion series in the analysis panel; **SR-6** bars imputation/interpolation/import (including the WDI 2001+ series); **SR-8** bars splicing or mixing measures. TC-1/TC-2 use **one** measure (NER) at **one** level. |
| **6** | (v) + (vi) | **Standing scaling-FAIL label applies**; verdict vocabulary is **DIAGNOSTIC-TRANSFER only** — no SUPPORTED / NOT SUPPORTED, no causal or direction claim, no portability claim beyond diagnostic transfer; and the predecl must say **what it would change** | Every table/caption carries the banner **`SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE`** (PA-6). §4 fixes the closed verdict set and the **forbidden strings** (PA-5); **`BLOCKED-*` is a terminal non-verdict state, not a fourth verdict**. §9 carries the no-causality statement. §8 states what each outcome would and would not change. |
| — | **(iv)** | CHN with censoring rules and the 1986-law **−27 y** miss reported as is | **Out of scope for this document.** CHN is slate-A6; this is slate-A7 (HKG). Named only to keep the slates distinct and to prevent a combined CHN+HKG table being assembled by accident. |

**Naming discipline (D75 last clause).** "Slate A7" / "HKG" = this portability slate. "Amendment A7" = timing-alignment. "A1"/"A2" as used below refer to **`MODEL_ARCHITECTURE.md` Amendments A1 and A2** (education→complexity; demographic/quality/child-labour), **not** to the portability slates. Where ambiguity is possible the full form is written out.

---

## 2. The timing checks — exact crossing, measure, band, window, tolerance

**Two checks only carry the verdict.** Both are primary-level, NER, fixed threshold, fixed target year. They use the same measure at the same level, so no splicing occurs.

### TC-1 — primary NER ≥90, target 1974

| field | frozen value |
|---|---|
| Level | primary |
| **Measure** | **NER** (`ner_primary`, UIS code `NER.1.cp`); **ANER permitted only as a declared equal-series substitution** (identical to NER for HKG 1971–1996 — `HKG_INVENTORY.md` §1) |
| Threshold | **≥ 90.0 %**, fixed |
| **Target crossing** | **1974** |
| Observed band | **[1973, 1974]** — 1973 = 89.60049 (below), 1974 = 91.10855 (above); `data/gmr_observed_6countries_1970_2024.csv:1686–:1687` |
| Observed censoring | **none** |
| **Tolerance** | **± 5 years** → model crossing accepted in **[1969, 1979]** |
| Test statistic | `err_1 = model_crossing_TC1 − 1974` (integer years) |
| Verdict rule | **PASS-component** iff `|err_1| ≤ 5`. Report `err_1` exactly; also report a **strict ±3 y** band as a **secondary disclosure only** (it does **not** change the verdict). |
| Crossing rule (must match the on-disk layer) | model crossing = **first year at/above threshold that is sustained**, using the same rule as `relations/data/UNIVERSALIZATION_TIMING.csv` (**"observed first-sustained crossing (>=5 consecutive years above)"**, `:21`); the raw first-at-above year is **also reported** as a disclosure row |

### TC-2 — primary NER ≥95, target 1979

| field | frozen value |
|---|---|
| Level | primary |
| **Measure** | **NER** (same series, same code) |
| Threshold | **≥ 95.0 %**, fixed |
| **Target crossing** | **1979** |
| Observed band | **[1978, 1979]** — 1978 = 94.6876 (below), 1979 = 95.07646 (above); `data/gmr_observed_6countries_1970_2024.csv:1691–:1692` |
| Observed censoring | **none** |
| **Tolerance** | **± 5 years** → model crossing accepted in **[1974, 1984]** |
| Test statistic | `err_2 = model_crossing_TC2 − 1979` |
| Verdict rule | **PASS-component** iff `|err_2| ≤ 5`; strict ±3 y as secondary disclosure |
| **MANDATORY DISCLOSURE (frozen)** | **1977 = 95.10725 is the first year numerically ≥95** (`:1690`), and **1978 falls back to 94.6876**. 1977 is therefore *not* a sustained crossing and is **not** the target. Every results table must print this disclosure line. `pct_years_above = 45.8` and `later_dips_after_crossing = True` (`relations/data/UNIVERSALIZATION_TIMING.csv:21`) must also be printed: the threshold is **not durably cleared** (below-threshold dips 1995, 1996, 2012–2015; `:1699–:1704`). |

**Tolerance provenance.** ±5 y is the programme's existing crossing-tolerance convention, not a number invented here: D50/A7 uses "±5 y" for timing alignment (`DECISIONS.md:59`) and D76 re-opener C2 is "fixed-behaviour crossings within ±5 y" (`:85`). It is fixed **before** the run and may not be widened afterwards; widening it is `FAIL-RE-FIT` under SR-3.

**Both TC-1 and TC-2 require a model NER object. The frozen model has none — see §7 SR-1.** That is the predeclared terminal condition, not an oversight.

---

## 3. Levels check-only (constraint iii, second half)

**LC-1 — levels are examined and never scored.**

- At **1974** and **1979**, report the model's primary **NER** level against the observed level (91.10855 and 95.07646; `:1687`, `:1692`), with a **±5 pp** band, plus the mean absolute level error over the two years.
- **LC-1 contributes nothing to the verdict.** It is printed in a table headed `LEVELS: CHECK-ONLY — NOT A VERDICT COMPONENT` and is not aggregated into any score.
- **Rationale, recorded:** at near-universal levels the level is saturated and any rival reproduces it; the discriminating object is the crossing year (`lit/UNIVERSALIZATION_TIMELINES_JPN_KOR_HKG.md:119`). HKG is exactly such a system.
- **D72's ±5 pp tertiary GER line is out of scope here.** D72 (`DECISIONS.md:81`) is a PHL addendum item (C6/C9). HKG tertiary is not a D75 target. If a future Council extends the transfer to tertiary, that is a **new** predeclaration.

### Descriptive-only ordering object (not a check, not a verdict component)

The on-disk ordering for HKG is **primary < tertiary < lower-secondary**, with **primary→lower-secondary spacing 37.0 y** (audit A03, `relations/.../UNIVERSALIZATION_TIMING_PATTERN.csv`, quoted at `audit_2026-11-20/a_regressions/REGRESSION_INVENTORY.csv:4`). This is recorded for completeness only: the lower-secondary crossing is **FLAGGED UNRELIABLE** as a denominator artefact (`UNIVERSALIZATION_TIMELINES_JPN_KOR_HKG.md:99`; `UNIVERSALIZATION_TIMING.md:20`) and **may not be used as a target**. No ordering or spacing check is scored.

---

## 4. Verdict vocabulary — DIAGNOSTIC-TRANSFER only

The verdict is emitted as one token from this **closed** set. **`PASS`, `SUPPORTED`, `NOT SUPPORTED`, `REPRODUCED`, `VALIDATED`, `CONFIRMED`, `PORTABLE` and `HOLDS` are forbidden strings in every HKG output file** (`FAIL` appears **only** as part of `FAIL-RE-FIT`).

| Token | Emitted iff | Meaning, restricted to the model |
|---|---|---|
| **`DIAGNOSTIC-TRANSFER: TRANSFER-HOLDS`** | TC-1 and TC-2 both pass (±5 y) **and** no stop rule fired | Under the frozen PHL parameterisation and declared HKG inputs, the model places the two primary NER crossings within ±5 y of the recorded years. **A statement about the simulator's timing behaviour on a second system. Not a validation, not portability, not evidence about HKG.** |
| **`DIAGNOSTIC-TRANSFER: TRANSFER-FAILS`** | TC-1 or TC-2 misses by > 5 y, **and** no stop rule fired | The frozen parameterisation does not reproduce the HKG crossing timing within tolerance. **A statement about the simulator.** |
| **`DIAGNOSTIC-TRANSFER: FAIL-RE-FIT`** | any FIXED parameter moved, any threshold/target/tolerance changed, any measure spliced, any completion imputed, any free parameter added | The run is **void as a diagnostic**; the moved object and its before/after value must be named. This token **overrides** a favourable TC result. |
| **`BLOCKED-*`** (terminal state, **not a verdict**) | a stop rule in §7 fires before a scored run completes | **No diagnostic was produced.** Must carry the specific stop-rule id (e.g. `BLOCKED-MEASURE(SR-1)`, `BLOCKED-PRECONDITION(SR-2)`, `BLOCKED-INPUT(SR-5)`). **A `BLOCKED` state may never be reported as a transfer finding, and may never be upgraded by relaxing a rule.** |

**No third verdict state exists.** In particular, "inconclusive", "mixed", "partially holds" and "suggestive" are **not available** — a split result (one check passing, one failing) is `TRANSFER-FAILS`, with both errors reported.

---

## 5. Parameter map — what is FIXED, what may be re-set, what is forbidden

Source of the parameter list: `synthetic_2026-11-20/generator_v1/PARAMS.md` (§3, §4; `sha256 9052e85b…`) and, for the v1.2 additions, `v1_2/PRE_DECLARATIONS.md` §4 (`sha256 fde18d40…`). The **v1.2** parameterisation is the one that would be ported (v1 is superseded), but its code does not yet exist — see SR-2.

### 5a. FIXED — behavioural; may not be changed, re-set, re-estimated or added to

| Block | Parameters (all FIXED) | Source |
|---|---|---|
| Economy / regime | `lf_share_of_pop`, `age_share_base`, `age_share_tfr_slope`, `age_share_min/max`, `band_share`, `x_income_coef`, `x_urban_coef`, `x_urban_ref`, `x_min/x_max`, `takeoff_lit`, `takeoff_income`, `div_x`, `div_income`, `lit_learn`, `lit_lag`, all `sec_*` and `sec_floors` | `PARAMS.md:77–96` |
| Job ladder / matching | `rung_a`, `rung_b`, `x_open`, `office_u_coef`, `mfg_u_coef`, `phi_formal`, `sep`, `seek`, `queue_retain`, `queue_max_lf`, `rank_gain` | `PARAMS.md:110–122` |
| Wages / returns | `rung_mult`, `cred_prem`, `psi_pre`, `psi_ind`, `psi_div`, **rank-factor rule incl. rung-1 = exactly 1.0** | `PARAMS.md:131–139` |
| Growth | `gp`, `accel_ind`, `accel_div`, `comp_step`, `lit_ag_growth`, `g_floor`, `g_cap`, `g_noise_sd` | `PARAMS.md:144–152` |
| Schooling supply | `dur`, `ger_cap`, `overage_cap`, `star_c1`, `star_c3`, `adj_speed`, `surv_min`, `seat_lo/seat_hi`, `ter_pool_retain`, `ter_trans_cap`, `meas_completion_factor` | `PARAMS.md:161–173` |
| Cohort-flow identity | `intake`, `graduates`, `completion` algebra exactly as `PARAMS.md:175–186` (completion is a cohort-flow object, not a fitted transform) | `PARAMS.md:175–186` |
| Quality / congestion (v1.2) | congestion `q = cohort/seats`; `Q = exp(−γ·max(0, q−1))`; `γ ≥ 0`; class-size/PTR functions; **capacity response coefficient and lag** — all as declared in the frozen v1.2 `PARAMS` | `v1_2/PRE_DECLARATIONS.md:73–76` |
| Household block (v1.2) | four-state `{school, both, work, neither}` utility form; `y_med`, `w_child`, `farm`, `compat`, `v0`, `decay`, `cost`, `neither`, `girl_care`, `haz`; **rationing rule** (official-age first, then over-age, seeded ties only) | `v1_2/PRE_DECLARATIONS.md:77–81` |
| RNG / determinism | one `PCG64` stream, **seed 20261120**, no wall-clock/OS entropy, floats `%.10g` | `v1_2/PRE_DECLARATIONS.md:123–124`; `PARAMS.md:30` |

### 5b. DECLARED HKG INPUTS — may be re-set for HKG, and must be written down before the run

These are the eleven objects D40/D75(i) permit to change. Each is an **input**, never a fitted object. "Source" is the on-disk file; where coverage is short, the **declared** extension is flagged as such.

| # | Declared HKG input | On-disk source & coverage | Status for the run |
|---|---|---|---|
| D1 | Initial cohorts / population path | `UNIVERSALIZATION_SERIES.csv` HKG `cohort_population_0_14`, `population_total` — **1995–2024 only** (`HKG_INVENTORY.md` §6) | **DECLARED PATH REQUIRED for 1971–1994** (no observed data) — SR-5 |
| D2 | Observed economy series | `JOBS_AND_MARKETS_PANEL.csv` HKG — **1995–2024**; `economic_complexity_panel.csv` — **1995–2024** | **DECLARED PATH REQUIRED for 1971–1994** — SR-5 |
| D3 | Policy dates / pushes | `POLICY_TIMELINE.csv:3–6` — **1971 / 1978 / 2008 / 2012** | present; dates fixed, no re-dating after output |
| D4 | Capacity trajectory | `STATE_CAPACITY.csv` HKG PTR 1996–2018, teachers 1996–2024, spending 1996–2024; **long PTR 1971–2025** in `gmr_observed_*` (`:1878+`) | present (PTR from 1971); fiscal/enforcement partial — D74 split kept |
| D5 | Level-gate mapping | `UNIVERSALIZATION_TIMING.csv` HKG rows (`:41–:65`) | present; **thresholds 90/95 and targets 1974/1979 are NOT re-set** |
| D6 | Measurement definitions | `DATA_NOTES_MASSIFICATION.md` + in-file `unit`/`definition`/`source_detail` | present — **hash drift noted** (`HKG_INVENTORY.md` §11.2); NER/ANER equivalence declared |
| D7 | Initial conditions | `y0` (1970 GDPpc), `pop0`, `TFR0`, `urban0`, `literacy0`, initial GER by level (p, l, u, t) | **DECLARED** — no observed 1970 values for most; each must be tabulated with its source or marked DECLARED |
| D8 | Sector offsets / office–mfg bias | country characterisation, analogous to the PHL/TWIN rows `PARAMS.md:206–207` | **DECLARED** — must be tabulated, never fitted to the crossings |
| D9 | Delivery pace | analogous to `PARAMS.md:209` | **DECLARED** — must be tabulated, never fitted |
| D10 | State-push / law markers used as timing markers | `POLICY_TIMELINE.csv` (D3); A7 alignment rules apply | present; **alignment is not a mechanism claim** (A7/R24) |
| D11 | NER↔ANER substitution | `HKG_INVENTORY.md` §1 (identical 1971–1996) | **permitted, declared**; must be printed in the run meta |

**D7–D9 are the leak risk.** They are declared country characterisations and they *can* be tuned until the crossings land. **This predeclaration does not solve that by good faith — it solves it by auditing:** every D7–D9 value must be tabulated with a value and a rationale **before** the run, hashed into the manifest, and the parameter-freeze audit must show **zero** post-hoc change. If any D7–D9 value is adjusted after a crossing is observed, the verdict is **`FAIL-RE-FIT`** and the moved value is named (SR-3).

### 5c. NOT ALLOWED — any occurrence makes the run void

1. Re-fitting, re-estimating or hand-tuning any **5a** parameter.
2. Changing the **thresholds** (90/95), the **targets** (1974/1979), the **bands**, or the **±5 y tolerance** after output is seen (SR-3).
3. **Splicing** measures across a series, or mixing NER and GER within a check (SR-8). "Never spliced" is D75's own word.
4. **Imputing, interpolating or reconstructing an HKG completion series** — including the WDI `SE.PRM.CMPT.ZS` / `SE.SEC.CMPT.LO.ZS` series recorded at `DATA_LEDGER.md:45,56`, which is out of window, un-ingested, and impossible-valued (129.5) — SR-6.
5. **Adding a free parameter** for HKG, or any per-country override / per-level anchor interpolation. v1.2 removed anchor interpolation by design (`v1_2/PRE_DECLARATIONS.md:88`); HKG may not reintroduce it.
6. Using the **2016/2014 lower-secondary crossing** as a target (artefact; §3).
7. **Adding an NER object to the model as an in-run rescue.** The NER object is *required* for the test (§7 SR-1) and its absence *is* the predeclared blocker; it may only arrive as a **Council-authorised, predeclared interface amendment made before the HKG run**, never as a mid-run patch to obtain a crossing.
8. Substituting `ger` or `completion` for the NER target, in whole or in part.

---

## 6. Audits the run must emit (parameter-freeze enforcement)

| id | Audit | Rule |
|---|---|---|
| **PA-1** | Parameter-freeze audit | Emit one row per **5a** parameter with `frozen_value`, `run_value`, `delta`. **Abort if any `delta ≠ 0`.** Emit one row per **5b** input with `value`, `source_or_DECLARED`, `hash`. |
| **PA-2** | No-extra-parameter audit | Emit the full set of free parameters in the run and diff it against the frozen set. **Abort on any addition.** |
| **PA-3** | No-anchor-interpolation audit | Static check that no per-level/per-country anchor array or override exists for HKG (`v1_2/PRE_DECLARATIONS.md:88–92`). |
| **PA-4** | Measure-integrity audit | Print, for every check, the measure name and series id actually used; abort if a check's measure differs from §2/§3. |
| **PA-5** | Forbidden-string audit | Grep all outputs for the forbidden verdict strings (§4). Abort on any hit. |
| **PA-6** | Banner audit | Confirm the `SCALING: FAIL …` banner is present in **every** table header and figure caption (constraint v). |

---

## 7. Stop rules — BLOCKED is a terminal state, never a rescue

These fire **before** or **during** the run. A fired stop rule ends the attempt with a `BLOCKED-*` token and **no** transfer verdict. **No stop rule may be relaxed, and no substitute may be found to keep the run alive.** This is the discipline D75(ii) exists to protect.

| id | Stop rule | Fires when | Token |
|---|---|---|---|
| **SR-1** | **NER interface** | The run's model does not emit an **NER object** (or emits one whose age-appropriate definition is undeclared), so TC-1/TC-2 **cannot be computed**. **This is the current state:** `generator_v1` has no NER object (`PARAMS.md:59,252`; no `ner` column in `results/synthetic_panel_v1.csv`; no NER in `code/sim_v1.py`). | **`BLOCKED-MEASURE(SR-1)`** — *not rescued* by GER, by completion, by a derived NER proxy, or by a mid-run model patch. |
| **SR-2** | **PHL precondition (W1's job)** | **v1.2 has not passed its own PHL checks** — `v1_2/PRE_DECLARATIONS.md` §5 **(a)–(e)**, `:86–:115`. Porting a model that fails its anchor is exactly what D75's rationale forbids ("porting a model that misses PHL's own informative crossings would re-measure a known miss"). **Currently unmet: `v1_2/` contains `PRE_DECLARATIONS.md` only — no `code/sim_v1_2.py`, no `PARAMS.md`, no results** (`ls 10_massification/extensions/synthetic_2026-11-20/v1_2/`). | **`BLOCKED-PRECONDITION(SR-2)`** |
| **SR-3** | **Re-fit** | Any 5a parameter moved; any threshold/target/tolerance changed after output; any D7–D9 declared value adjusted post hoc to move a crossing | **`FAIL-RE-FIT`** (name the object and before/after) |
| **SR-4** | **Observational insufficiency** | Fewer than the declared minimum observed NER years are available in the window for a check, or the observed band cannot be established | **`BLOCKED-INPUT(SR-4)`** |
| **SR-5** | **Undeclared pre-1995 input** | A 1971–1994 cohort or economy path is **not** written down as DECLARED before the run (D1/D2), or is fitted | **`BLOCKED-INPUT(SR-5)`** (or `FAIL-RE-FIT` if fitted) |
| **SR-6** | **Completion imputation** | Any HKG completion series is imputed, interpolated, reconstructed or imported (incl. the WDI 2001+ series) | **`FAIL-RE-FIT`** |
| **SR-7** | **Determinism** | Two clean runs are **not** byte-identical | **run invalid; no verdict** |
| **SR-8** | **Splicing / measure drift** | Measures spliced, or NER/GER mixed within a check, or a check run on a measure other than §2/§3 | **`FAIL-RE-FIT`** |
| **SR-9** | **No Council decision** | A new Council decision authorising the HKG run is absent (D75: "requires a new Council decision + predecl"; slate remains **PARKED-ARMED**, `STATUS.md:441`; `COUNCIL_STATE.md:88`) | **`BLOCKED-AUTHORITY(SR-9)`** — the run may not start at all |

**The run may start only when SR-1, SR-2 and SR-9 are all clear.** SR-1 and SR-2 are **not currently clear**; SR-9 is **not currently granted**. **The correct current status is `BLOCKED`, and this document says so in advance so that no future worker mistakes the block for a failure or a finding.**

---

## 8. What each outcome would change (D75 constraint vi)

**Baseline that cannot be changed by anything in this transfer.** The PHL anchor cell is **CLOSED** at **PARTIAL / DESCRIPTIVE / EQUIVALENT** (D76, `DECISIONS.md:85`), with a standing **scaling FAIL** (A12/B02) and a recorded timing profile: M2 lower-secondary 2024 (narrow band), M3 upper-secondary **never** ≥90 (peak 76.43 in 2017), M4 tertiary **not discriminable** (initialisation artefact, not a 64-y miss — D72). Re-openers are **only** C1–C4 (D76). **This transfer is not a re-opener and cannot become one.**

| Outcome | What it would change | What it would **not** change |
|---|---|---|
| **TRANSFER-HOLDS** | Would show the frozen parameterisation can place HKG's two primary NER crossings within ±5 y given declared inputs — i.e. the model's crossing-timing behaviour is **not purely PHL-idiosyncratic**. Its only actionable consequence: it would justify (not compel) a **Cycle-11 proposal** to re-fit the anchor against a cross-system timing criterion. | **Not** a portability claim (R22), **not** a validation, **not** evidence about Hong Kong, **not** an upgrade of the anchor, **not** a change to the phase verdict or headline (D77), **not** a route to "capacity explains timing" (D61/R28). |
| **TRANSFER-FAILS** | Would show the frozen parameterisation's timing error recurs on a **second, high-capacity system**, strengthening the existing reading that the anchor's timing misses are a property of the **model class** rather than of Philippine data. Also note-only. | Same as above; **no** claim about HKG's history, **no** rival adjudication, **no** verdict change. |
| **FAIL-RE-FIT** | Records that the diagnostic was **void** and names the moved object — a **process finding about the run**, reportable as such. | **No** transfer information of any kind. |
| **BLOCKED-* ** | Records that **no diagnostic was produced** and which precondition failed. Actionable only as a to-do list for a future Council. | **No** transfer information; must never be cited as a result. |

**In one line: no outcome of this transfer can change the closed phase verdict, and none may be reported as if it could.**

---

## 9. No-causality / no-direction statement (binding on every output)

Every output file carries this statement verbatim:

> **No causal claim. No direction or push–pull claim (R13/D77). No portability claim (R22). No policy claim. This transfer tests only whether a frozen simulator's crossing TIMING falls within a pre-declared tolerance on one system; it cannot identify a cause, a direction, or a mechanism, and a favourable result is not evidence that any mechanism operated in Hong Kong.** The model is a **declared-assumption simulator** (`PARAMS.md:3–6`); its parameters are invented or declared, not estimated, and its output is not an estimate of anything.

Additional binding restrictions:

- **No level claim** from LC-1 (check-only).
- **No capacity claim** — capacity is a declared input here, not a tested channel (D61/D74/R28); `K_fiscal`/`K_delivery`/`K_enforcement` stay separate and no collapsed index may appear.
- **No "HKG universalized because…" sentence**, in any file, at any confidence.
- **No comparison to PHL as a mechanism** — the PHL record appears only as the frozen parameterisation's origin and as the closed-verdict baseline.
- Every reported number is labelled **model output** (not observed) or **observed** with `file:line`; the two may never be printed in the same column.

---

## 10. Expected-output table (declared before the run)

| file | contents | must contain |
|---|---|---|
| `results/hkg_transfer_checks.csv` | one row per check: `TC-1`, `TC-2`, `LC-1` | `measure`, `series_id`, `threshold`, `target_year`, `observed_band`, `model_crossing`, `err_years`, `tolerance`, `component_result`, `verdict_component(Y/N)` |
| `results/hkg_crossings_model.csv` | model crossing year per level × threshold × measure, with the **same** first-sustained + first-at-above rule as the on-disk layer | both crossing rules, and `pct_years_above` for comparability with `relations/.../UNIVERSALIZATION_TIMING.csv:21` |
| `results/hkg_levels_checkonly.csv` | primary NER level at 1974 and 1979 vs observed | header `LEVELS: CHECK-ONLY — NOT A VERDICT COMPONENT` |
| `results/hkg_parameter_freeze_audit.csv` | PA-1…PA-4 rows | `delta` column, all zero for 5a |
| `results/hkg_declared_inputs.csv` | every D1–D11 value with `source_or_DECLARED` and hash | the pre-1995 declared paths, explicitly |
| `results/hkg_run_meta.json` | seed, python version, input hashes, v1.2 precondition status, run timestamps, byte counts | `seed=20261120`, `precondition_v1_2_checks = PASS` |
| `results/DISCLOSURE_1977.txt` or the disclosure row in the checks table | the mandatory 1977/1978/dips disclosure (§2 TC-2) | verbatim disclosure line |
| `RUN_MANIFEST.json` | post-run hashes of code, params, inputs, results; check summary; verdict token | the verdict token and `BLOCKED`/stop-rule id if applicable |
| `FINDINGS.md` | written **after** the run only; includes FAILs and BLOCKEDs | the no-causality statement and the banner |

**Every** one of the above carries the header banner:
`SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE`

---

## 11. Determinism requirement

- One `PCG64` stream, **seed 20261120**; no wall-clock, no OS entropy, no dict-ordering dependence; floats at `%.10g` (`v1_2/PRE_DECLARATIONS.md:123–124`).
- **Two clean runs must be byte-identical**, both to each other and to the delivered files.
- The verification is a stored diff, not an assertion: `sha256sum` over every result file from run 1 and run 2, recorded in `RUN_MANIFEST.json`. Any difference ⇒ **SR-7**, run invalid, no verdict.

---

## 12. Freeze statement

This file was written **before** any HKG run and **before** any HKG result existed. It is **not edited after results are seen**. Its sha256 is recorded in `RUN_MANIFEST.json` and `HKG_CHECKLIST.md`; the run script must **refuse to run** if the on-disk hash of this file and of every 5a/5b input does not match the manifest (§6 PA-1/PA-2).

**If a rule here turns out to be wrong, the correct action is a new predeclaration under a new Council decision — never an edit to this file.**

**Current disposition: `BLOCKED-MEASURE(SR-1)` + `BLOCKED-PRECONDITION(SR-2)` + `BLOCKED-AUTHORITY(SR-9)`. No run. No result. No claim.**
