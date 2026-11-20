<!-- Worker W3, 2026-11-20. Scope: 10_massification/extensions/hkg_transfer_2026-11-20/ only.
     PREP ONLY — no HKG model was run, no parameter was fitted, no completion series was imputed.
     Labels used strictly: OBSERVED (read from an on-disk series, cited) / DERIVED (computed on disk from a
     cited series) / RECONSTRUCTED (built from headcounts + a population denominator; BOUND only) /
     POLICY-FACT (dated in POLICY_TIMELINE.csv) / ABSENT (searched, not on disk) / UNABLE (file itself
     declares the object not computable). No causal claim, no direction claim, no portability claim (D77/R13/R22). -->

# HKG INVENTORY — everything on disk about Hong Kong, with locators

**Purpose.** Freeze the HKG record *before* any transfer run, so the run cannot move its own goalposts. This is the evidence side only. The frozen test is in `HKG_TRANSFER_PRE_DECLARATIONS.md`; the run steps are in `HKG_CHECKLIST.md`.

**Authority.** D75 (`08_council/DECISIONS.md:84`), D40 (`:49`), D77 (`:86`), D93 (`:103`), R20/R22. Dispatch: `10_massification/STATUS.md:757` (§3w, W3 row).

**The single most important line in this file is §9.** The frozen PHL model has **no NER object**, and D75's HKG targets are **NER** thresholds. The timing test is therefore blocked at the model interface, not at the data. That is predeclared, not discovered later.

---

## 1. The verified crossing table (the transfer's target object)

Source of record: `10_massification/data/UNIVERSALIZATION_TIMING.csv` (the "C03" layer, 128 rows). Raw series: `data/gmr_observed_6countries_1970_2024.csv` (UIS/GMR, 4,635 rows).

| Level | Threshold | **Measure** | Crossing | Band | Censoring | Status in file | Locator |
|---|---|---|---|---|---|---|---|
| Primary | ≥90 | **NER** | **1974** | 1973–1974 | none | observed, high | `UNIVERSALIZATION_TIMING.csv:48` |
| Primary | ≥95 | **NER** | **1979** | 1978–1979 | none | observed, high | `UNIVERSALIZATION_TIMING.csv:51` |
| Primary | ≥50 | NER | 1971 | — | left | observed, high | `:45` |
| Primary | ≥90 | GER | 2001 | — | **left** (at first obs) | observed, high | `:46` |
| Primary | ≥95 | GER | 2001 | — | **left** | observed, high | `:49` |
| Primary | ≥90/≥95 | **completion** | — | — | — | **unable** | `:42`, `:52` |
| Lower secondary | ≥90 | GER | 1998 | — | **left** | observed, high | `:41` |
| Lower secondary | ≥90 | NER | 2016 | 2015–2016 | none | observed, high — **see §2 artefact note** | `:58` |
| Secondary | ≥90 | GER | 2012 | 2011–2012 | none | observed, high | `:56` |
| Secondary | ≥90 | NER | 2016 | 2015–2016 | none | observed, high | `:58` |
| Upper secondary | ≥90 | GER | 2012 | 2011–2012 | none | observed, high | `:64` |
| Upper secondary | ≥50 | GER | 2001 | — | **left** | observed, high | `:63` |
| Upper secondary | ≥95 | **completion** | — | — | — | **unable** | `:65` |
| Tertiary | ≥15 | GER | 1992 | 1984–1992 | none | observed, high | `:59` |
| Tertiary | ≥50 | GER | 2008 | 2007–2008 | none | observed, high | `:61` |

**The two D75 targets, verified exactly as the Council recorded them.** D75 constraint (iii) states "NER≥90 1974, NER≥95 1979" (`DECISIONS.md:84`). Both reproduce from disk:

- **NER ≥90 → 1974.** `ner_primary` 1973 = **89.60049** (below), 1974 = **91.10855** (above) — `data/gmr_observed_6countries_1970_2024.csv:1686` and `:1687`. Band 1973–1974, censoring none. **CONFIRMED, no ambiguity.**
- **NER ≥95 → 1979.** `ner_primary` 1978 = **94.6876** (below), 1979 = **95.07646** (above) — `:1691` and `:1692`. Band 1978–1979, censoring none. **CONFIRMED as the sustained crossing** — but see §2: it is **not** the first year above 95.

**Measure reconciliation (why NER and not GER/completion).**

- NER and ANER are **numerically identical for HKG 1971–1996** (`ner_primary` `:1684–:1699` vs `aner_primary` `:1203–:1218`, same values to 5 dp); they diverge only from 2012 (`ner_primary:1701` = 94.19961 vs `aner_primary:1220` = 99.27739). **The NER/ANER choice therefore cannot move the 1974 or 1979 crossing**, and any residual measure ambiguity is confined to the post-2012 rows that the D75 test does not use.
- GER is unusable for the D75 targets: HKG `ger_primary` does not begin until **2001** and is already **100.91** at first observation (`:1466`), i.e. left-censored above every threshold. A GER-based crossing is uninformative by construction.
- Completion is unusable: **HKG has no completion series in the analysis panel at all** — see §3.

---

## 2. The one real discrepancy: 1977 vs 1979 (verified, and it does not change the target)

This was flagged as "verify these exact figures" in the dispatch. Verification found a genuine three-way divergence that must be disclosed rather than smoothed:

- `10_massification/lit/UNIVERSALIZATION_TIMELINES_JPN_KOR_HKG.md:98` says primary NER "≥95 in **1977** (95.1%)".
- D75 (`DECISIONS.md:84`) and `UNIVERSALIZATION_TIMING.csv:51` say **1979**.
- The raw series shows **both are factually true of different objects**:
  - **1977 = 95.10725** — the **first year numerically ≥95** (`:1690`).
  - **1978 = 94.6876** — **falls back below** the threshold (`:1691`).
  - **1979 = 95.07646** — re-crosses and then holds 1979–1985 (`:1692–:1698`).
- The method in the relations layer is explicit: **"observed first-sustained crossing (>=5 consecutive years above)"** — `10_massification/relations/data/UNIVERSALIZATION_TIMING.csv:21`. Because 1978 breaks the run, 1977 is **not** a sustained crossing; the first sustained crossing is 1979, band **[1978.0, 1979.0]**, midpoint 1978.5. That same row records **`pct_years_above=45.8`** and **`later_dips_after_crossing`** — i.e. fewer than half the observed years are above 95, because the series dips again in **1995 (93.90)**, **1996 (93.81)**, and **2012–2015 (94.20 / 93.79 / 94.29 / 93.81)** (`:1699–:1704`).
- **Corroboration from an independent measure:** the in-school (100−OOS) series crosses the same ≥95 threshold at band **1979–1980** (`relations/data/UNIVERSALIZATION_TIMING.csv:22`), i.e. one year later, not 1977.

**Resolution adopted (frozen):** the D75 target is **1979**, band [1978, 1979], because D75 and both on-disk derived layers agree and the sustained-crossing rule excludes 1977. **1977 is carried as a mandatory disclosure row** in the predeclaration and in every results table. This is a measure/method difference, not an error in D75, and the lit file's "1977" is the correct first-at-above year — the two are not the same statistic.

**Artefact note (lower secondary).** The lower-secondary NER ≥90 crossing of 2016 (`UNIVERSALIZATION_TIMING.csv:58`) is **flagged unreliable on disk**: 9-year compulsory schooling dates from 1978, so a 2016/2014 crossing is a measure/denominator artefact, not a 38-year delay — `UNIVERSALIZATION_TIMELINES_JPN_KOR_HKG.md:99` ("DERIVED, FLAGGED UNRELIABLE") and `UNIVERSALIZATION_TIMING.md:20` ("Do not read the derived HKG lower-secondary crossing as history"). **This crossing must not be used as a transfer target.**

---

## 3. Completion: ABSENT, and the WDI counter-entry that must not be used to rescue it

- **The analysis panel contains completion for CHN, KHM, KOR, PHL — and zero HKG rows.** Verified: `data/gmr_observed_6countries_1970_2024.csv` has indicators `completion_primary`, `completion_lower_secondary`, `completion_upper_secondary` (PHL 33 rows) but **0 HKG rows**.
- `UNIVERSALIZATION_SERIES.csv` HKG: 438 rows, **no completion indicator** (§5).
- The derived layer marks all three HKG completion gates **`unable`**, with the reason given in-file: *"Hong Kong does not report UIS completion (CR.* absent). National source needed"* — `UNIVERSALIZATION_TIMING.csv:42`, `:52`, `:65`.
- **Counter-entry that must be refused.** `DATA_LEDGER.md:45` records WDI `SE.PRM.CMPT.ZS` for HKG **2001–2024 (n=23, 2024=91.7)** and `:56` records `SE.SEC.CMPT.LO.ZS` for HKG **2001–2024 (n=21, 2024=129.5)**. This is **not a usable completion series** for the D75 test on three independent grounds: (a) it is **out of window** — it starts 2001, 27 years after the 1974 target; (b) it is **not ingested** into any analysis panel (absent from `gmr_observed_*` and `UNIVERSALIZATION_SERIES`); (c) the lower-secondary value **129.5 is impossible** (>100), the known UIS/WDI completion-denominator artefact documented at `STATUS.md:639` §3v ("completion can exceed GER because the UIS completion rate uses a 3–5-years-above-grade denominator"). **Using it to substitute for the missing NER object would violate D75 constraint (v) [no imputed completion] and is predeclared as a FAIL-re-fit.**

**Verdict on constraint 5:** HKG has **no** completion series usable for the timing test. The constraint is **factually grounded and correctly enforced**; no imputation is permitted or needed, because the D75 test is NER-based.

---

## 4. Policy timeline — verified from file (not from the lit note)

`10_massification/data/POLICY_TIMELINE.csv` (HKG rows, all `status=policy_fact`):

| Year | Event | Detail | Confidence as recorded | Locator |
|---|---|---|---|---|
| **1971** | 6-year free primary education | free primary schooling policy | `fact (not re-verified this pass)` | `:3` |
| **1978** | 9-year free compulsory education | primary 6 + junior secondary 3 became free and compulsory | `fact (not re-verified this pass)` | `:4` |
| **2008** | 12-year free education rolled out | free senior secondary from **2008/09** academic year | `fact (not re-verified this pass)` | `:5` |
| **2012** | 3-3-4 academic structure reform | secondary reduced to 6 years; 4-year undergraduate degrees; first HKDSE 2012 | `fact` (workspace ledger provenance) | `:6` |

**This resolves the lit file's `UNRESOLVED` 2008/2009/2012 conflict** (`UNIVERSALIZATION_TIMELINES_JPN_KOR_HKG.md:109,113`) in a cleaner way than the lit file knew: the file **separates two distinct reforms** — **2008** = 12-year free education (free senior secondary, SY2008/09) and **2012** = the 3-3-4 *structure* reform + first HKDSE. They are not competing dates for one event.

**Note on the "HKG 2009" label.** D50/D94 and `event_windows.csv` refer to "HKG 2009 +9.08"; that is the **2008 policy with treatment year 2009** (S4–S6 cohorts from SY2008/09) — `relations/data/event_windows.csv:9`, `date_signed=2008.0`, `date_effective=2009`. Cite it as *2008 policy / 2009 treatment*, never as a third reform date.

**Event-window status at the targets (important for the checklist):**

- **1971 free primary → `UNABLE`**: "insufficient observed annual series around the event" (`event_windows.csv:7`); pre-window 1961–1970 has **no data** because HKG series begin 1971.
- **1978 compulsory → `UNABLE`** (`:8`), implied gap to the lower-sec crossing 36.5 y — the artefact in §2.
- **2008/2009 free senior secondary → computed**, shift **+9.08 pp**, se 1.75, t=5.20, n_pre=n_post=7, post mean 71.78 vs pre mean 57.62 (`:9`); the affected crossing is nevertheless `censored_above_at_first_obs`. Descriptive only — no control group, naive SE (audit A14).
- **2012 3-3-4 → `UNABLE`**: needs `completion_upper_secondary`, which HKG does not have (`:10`).

**Consequence:** the only *computed* HKG event window is 2008/2009, and it is **not** at either D75 target crossing. The 1971 law-to-1974-crossing association (the "3 years" often quoted, e.g. `lit/STATE_CAPACITY.md:68`) is **not computable as an event window on disk** — it is a descriptive juxtaposition of a policy date and a crossing, not a measured shift.

---

## 5. Capacity / PTR availability — longer than the capacity layer admits, and the "moment of universalization" framing does not survive it

| Object | Coverage | Locator | Label |
|---|---|---|---|
| **PTR primary (long series)** | **1971–2025 (52 obs)** | `data/gmr_observed_6countries_1970_2024.csv:1878–1929` | OBSERVED |
| **PTR secondary (long series)** | **1971–2025 (44 obs)** | `:1930–…` | OBSERVED |
| PTR primary in capacity layer | **1996–2018 (22 obs)** | `10_massification/data/STATE_CAPACITY.csv` | OBSERVED (subset) |
| PTR secondary in capacity layer | 1996–2018 (19 obs) | same | OBSERVED (subset) |
| Teachers primary / secondary | 1996–2024 (28 / 27) | same | OBSERVED |
| Education spending %GDP (WDI) | 1996–2024 (25) | same | OBSERVED |
| Education spending %GDP (UIS cross-check) | 1971–2025 (42) | same | OBSERVED |
| Per-student spending (const PPP$) primary/secondary | 2001–2025 / 2002–2025 | same | OBSERVED |
| Policy-event rows 1971/1978/2008/2012 | single years | same (`dimension=enforcement_capacity`) | POLICY-FACT |
| **School expansion (classrooms, schools)** | **ABSENT — 0 HKG rows** | `10_massification/data/SCHOOL_EXPANSION.csv` is **PHL-only (27 rows)** | ABSENT |

**Verified cross-source consistency:** PTR primary 1996 = **23.72998046875** and 2018 = **13.34788036346436** agree to 5 dp between `gmr_observed:1901/:1922` and `STATE_CAPACITY.csv`. The capacity layer is a **subset** of the long series, not a different measurement.

**Discrepancy to report (descriptive, no capacity claim).** `lit/STATE_CAPACITY.md:61–68` presents HKG as having "high delivery capacity **at the moment of universalization**" with PTRs "13–24", but its own table is anchored on **1996–2018** — and 1996 is **22 years after** the 1974 crossing. The PTR that is actually on disk **at** the crossing is **31.89 (1974)** and **30.21 (1979)** (`gmr_observed:1881`, `:1886`); secondary is **24.20 (1974)** and **30.11 (1979)** (`:1933`, `:1938`). Those values are **not** dramatically below PHL's contemporaneous 33.7/36.2 (`lit/STATE_CAPACITY.md:56–57`). **The "13–24" range describes post-1996 HKG, not HKG at universalization.** No inference is drawn here — capacity claims are barred (D61/R28/D74) — but the transfer must not import the "high capacity at the moment" reading as if it were measured at 1974.

**Coverage verdict for the transfer:** capacity is **available at the crossing window** via the long PTR series (1971+), but **fiscal/enforcement capacity is not** (spending %GDP usable from 1971 only in the UIS cross-check; enforcement is unmeasured — `lit/STATE_CAPACITY.md:30`, `:85`). Per D74, `K_fiscal`/`K_delivery`/`K_enforcement` stay separate and **no collapsed index may carry a claim**.

---

## 6. Economy and ECI series — present, but **all start ~year 1995**, i.e. after the targets

| Object | Coverage | Locator | Label |
|---|---|---|---|
| GDP pc (current / constant / PPP) | 1995–2024 (30) | `10_massification/data/JOBS_AND_MARKETS_PANEL.csv` | OBSERVED |
| Sector employment shares (SL.AGR/IND/SRV/EMP.WORK) | 1995–2024 (30) | same | OBSERVED |
| Unemployment (total / youth 15–24 / NEET) | 1995–2024 / 2009–2024 | same | OBSERVED |
| Remittances (US$ and %GDP) | 1998–2024 (27) | same | OBSERVED |
| Education spending %GDP | 1996–2024 (25) | same | OBSERVED |
| **ECI (SITC, HS92)** | **1995–2024 (30**, coverage 30/30 y**)** | `09_relations/data/economic_complexity_panel.csv` | OBSERVED |
| ECI (HS12) | 2012–2024 only | same; audit B17 (`REGRESSION_INVENTORY.csv:39`) | OBSERVED |
| Adult/youth literacy | **ABSENT for HKG** (`HKG none`) | `DATA_LEDGER.md:44` | ABSENT |

**Consequence for the run (predeclared):** the economy layer cannot be driven by observed HKG data in **1971–1994** — there is none. Any pre-1995 economic path used to initialise or drive a 1971–1979 simulation is a **DECLARED input**, must be written down before the run, and **may never be fitted**. If it is not declared, the run is **BLOCKED** (see predecl. SR-5). This is a real constraint that the Y5 "6/6 DATA-COMPLETE" verdict does **not** capture — see §10.

---

## 7. Shadow-education 85% figure — found, sourced, and caveated

- **Value:** **~85%** of **senior-secondary** students receiving shadow education, **c.2011**, interval **80–90**.
- **Locators:** `02_lit/COUNTRY_CARDS/HKG.md:15` (table row) and `:9` (headline); `02_lit/SHADOW_TARGETS.csv:9` (structured row).
- **Provenance as recorded:** Bray & Lykins, *Shadow Education* (ADB 2012), **p. X (introduction)**, "quoted verbatim by J. Dierkes, Jukupedia, 19 May 2012" — labelled **`SECOND-HAND QUOTATION`**, confidence **medium**, and flagged `Provenance verified` but **denominator = "senior secondary" specifically, not all secondary** (`SHADOW_TARGETS.csv:9`).
- **Caveats that travel with it:** not a first-hand reading of the book's table; the 2014 *Economics of Education Review* disaggregation is paywalled/unread (`HKG.md:16,19`); the **denominator is the single biggest unknown** — treat as an **upper-bound, upper-secondary-only** target, **not** a system-wide rate (`HKG.md:38–39`); **no structure target** (no income-quintile or provider split) is available (`:39`).
- **Claim-register status:** `02_lit/CLAIM_REGISTER.csv:3` (J-02) marks the June-draft sentence **`unresolved`** with note "October drops the figure entirely"; it is **not** an established claim in this programme.

**Transfer status: NOT a D75 transfer input.** D75's six inputs are cohorts, economy, policy dates, capacity, gate mapping, measurement definitions (`Y5` checklist I1–I6). **The 85% shadow figure is not among them** and is **not scored** by this transfer. It is inventoried here because the dispatch asked where it is, and because the v1.3 shadow block (W2) will need it as a *prior*, not a test.

---

## 8. Labour-market anchors — series present, narrative absent

- **Narrative anchors: ABSENT.** `10_massification/lit/LABOUR_MARKET_REPORTS.md` contains **zero** occurrences of "HKG" or "Hong Kong" (verified by grep; file scope is the ILO/OECD corpus generally, header at `:1–6`). There is **no HKG labour-market narrative** on disk.
- **Series: PRESENT but 1995+.** Employment/unemployment/sector/remittance/participation series as in §6, all `JOBS_AND_MARKETS_PANEL.csv` (1995–2024).
- **No wage/earnings by education for HKG** — the programme's largest push-pull gap, stated at `relations/SCALING_NOTES.md` (audit A19: "'no wages/earnings by education' is the largest push-pull gap").
- **Gates (qualitative only):** HKDSE (first cohort 2012), JUPAS, SSPA — `02_lit/COUNTRY_CARDS/HKG.md:22–24`; pass rates / Level-4+ shares **NOT FOUND** (`:25`); senior-secondary participation / tertiary entrance / dropout **NOT FOUND** (`:28`). The "near-lossless positional resolution" phrase is **interpretive, not a measured property** (`:29`).

---

## 9. THE BLOCKER — the frozen PHL model has no NER object

This is the decisive interface fact and it is why the run is not runnable today.

- D75 constraint (iii) requires the HKG timing test on **NER** crossings: NER≥90 1974, NER≥95 1979 (`DECISIONS.md:84`). Also restated in the Y5 checklist: *"HKG timing-only and levels check-only (NER≥90 1974, NER≥95 1979, threshold-specific, never spliced)"* — `lab_2026-11-20_c/Y5_portability_audit/results/transfer_checklist.csv:11`.
- The PHL model that would be ported **emits no NER**. Its output contract is:
  `ger`, `completion`, `survival`, `enrolment`, `intake`, `graduates`, `out_of_school`, … — `synthetic_2026-11-20/generator_v1/results/synthetic_panel_v1.csv` header (48 columns, **no `ner`**).
- `generator_v1/PARAMS.md:59` states it directly: *"PHL primary NER 96.79 (1976) — **not used** (v1 has no NER object)"*; and `:252`: *"**No NER object**, no PTR/spending series inside the model (they are rationale, not inputs)."*
- Confirmed by code inspection: `generator_v1/code/sim_v1.py` contains **no** NER computation (grep for `ner` returns no match).

**Therefore:** the D75 target object (an NER crossing) **cannot be produced by the model whose behaviour is frozen**. The model can emit `ger` and `completion` crossings — but both are unusable for HKG:
- **GER**: HKG `ger_primary` is **left-censored above all thresholds at its first observation (2001)** — no informative crossing exists.
- **completion**: HKG has **no series at all** (§3), and imputing one is barred by constraint (v).

**This is a data/interface block, not a modelling result.** The honest outcomes are: (a) Council authorises a **predeclared NER object** as an interface amendment to v1.2/v1.3 *before* the HKG run (then the test is runnable); or (b) the transfer is recorded **BLOCKED-MEASURE** and not run. Substituting a measure to make it runnable is **FAIL-re-fit** and is predeclared as such (SR-1). No rescue is permitted.

---

## 10. What is MISSING — for the transfer and for the record

| # | Missing object | Why it matters | Status |
|---|---|---|---|
| M1 | **NER object in the PHL model** | D75's targets are NER; the model emits none (§9) | **BLOCKING** |
| M2 | HKG **completion** series (pre-2001) | Would allow a completion-based cross-check; barred as a substitute | ABSENT (declared `unable`, `UNIVERSALIZATION_TIMING.csv:42,52,65`) |
| M3 | HKG **economy series before 1995** | The 1971–1979 simulation has no observed driver | ABSENT — must be a **declared** path (SR-5) |
| M4 | HKG **school expansion** (classrooms/schools) | Capacity-expansion input I4 is only partly present | ABSENT — `SCHOOL_EXPANSION.csv` is PHL-only (27 rows) |
| M5 | HKG **fiscal/enforcement capacity before 1996** | Only UIS %GDP from 1971; enforcement unmeasured | PARTIAL (D74: no collapsed index) |
| M6 | HKG **labour-market narrative / earnings by education** | Push-pull inputs; largest gap (audit A19) | ABSENT |
| M7 | HKG **literacy series** | `HKG none` in ledger | ABSENT (`DATA_LEDGER.md:44`) |
| M8 | HKG **lower-secondary crossing** usable as history | The 2016/2014 crossing is a denominator artefact | FLAGGED UNRELIABLE — do not target |
| M9 | Pre-1970 HKG series | 1971 event window is `UNABLE` for want of a pre-period | ABSENT (lit:96) |
| M10 | A **Council decision** authorising the run | D75 requires "a new Council decision + predecl" | **NOT YET GRANTED** |

**Reconciliation with the Y5 "DATA-COMPLETE" verdict (must be stated, not hidden).** `lab_2026-11-20_c/FINDINGS.md:20` reports **6/6 D75 inputs present-on-disk for both countries, 0 NEW-ASK → DATA-COMPLETE**, reaffirmed at `STATUS.md:567` §3u. That verdict is about **presence of the six inputs, not their coverage in the test window or their compatibility with the frozen model**. Specifically it does not capture: (i) the **no-NER-object** interface block (M1); (ii) economy/capacity series that begin **~20 years after** the targets (M3/M5); (iii) `SCHOOL_EXPANSION.csv` being PHL-only, which Y5 itself notes at `FINDINGS.md:46` ("not a D75 input for the transfer"). **The transfer is therefore data-complete in Y5's declared sense and simultaneously not runnable — the gap is the model interface, not the data.** Both statements are true and both are recorded here.

---

## 11. Source-integrity notes found while inventorying

1. **Stale path (known defect, confirmed).** The lit and audit layers cite `04_data/data/gmr_observed_6countries_1970_2024.csv` — e.g. `UNIVERSALIZATION_TIMELINES_JPN_KOR_HKG.md:135`, `UNIVERSALIZATION_TIMING.md:20`. **That path does not exist**; the file is at `data/gmr_observed_6countries_1970_2024.csv`. This is audit **C01's "PATH DRIFT"** finding (`audit_2026-11-20/a_regressions/REGRESSION_INVENTORY.csv:50`), a known housekeeping item (D94 FLAG-01). **No analysis is affected; the series verifies.** This inventory cites the real path.
2. **Hash drift in the capacity/definition inputs.** `10_massification/data/SHA256SUMS.txt` **fails on one entry**: `DATA_NOTES_MASSIFICATION.md` recorded `e2cfcdb2…`, actual **`5e51c5d0a6d620125f0f8ef902ed8942cf3bed96af762cd213f71b7613a8c244`**. Explained by `STATUS.md:639` §3v — a measurement-definition note was added to that file at 22:12 **after** the sums were generated, and the sums were not regenerated. **Housekeeping defect, not corruption**; the other 10 entries verify `OK`. The transfer records the **actual** hash and flags the drift; it does **not** treat the manifest as authoritative for that file.
3. **Cross-hashes match the audit register**, confirming the inputs this inventory relies on: `relations/data/UNIVERSALIZATION_TIMING.csv` = `6223b75a…` = audit **A01**; `data/gmr_observed_6countries_1970_2024.csv` = `794a67c1…` = audit **C01**; `10_massification/data/UNIVERSALIZATION_TIMING.csv` = `6e067ffd…` = audit **C03**; `relations/data/event_windows.csv` = `7bac26b3…` = audit **A14**. All four match the audit's recorded hashes exactly.
4. **Two timing layers share a filename** (audit C03's flag): `10_massification/relations/data/UNIVERSALIZATION_TIMING.csv` (**63 rows**, first-**sustained**) vs `10_massification/data/UNIVERSALIZATION_TIMING.csv` (**128 rows**, 80 observed/42 reconstructed/6 unable). **They disagree for HKG on method, not on the target years.** This inventory cites the 128-row layer for the crossing table and the 63-row layer for the sustained-crossing method/`pct_years_above`. **A future reader must not conflate them** — precisely the confusion C03 warns about.

---

## 12. One-line summary for the Council

**The HKG record is complete enough to specify the D75 test and not complete enough to run it: both NER targets verify exactly on disk (1974 at 91.11, 1979 at 95.08 with band 1978–1979, 1977 disclosed as the first-at-above year), HKG has no completion series (constraint 5 correct), the economy and capacity series begin ~20 years after the targets, and — decisively — the frozen PHL model emits no NER object at all, so the timing test cannot be computed on fixed behaviour without a predeclared interface amendment.**
