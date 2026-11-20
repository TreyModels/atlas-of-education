<!-- Writer: lit-archivist, 2026-11-20. Deliverable requested by repo-auditor per user directive A4 (pending):
JPN/KOR/HKG universalization TIMING, not level. Write scope 10_massification/lit/ only.
Labels kept strictly: OBSERVED (read from a table, cited) / DERIVED (computed this session from a series on disk) /
STANDARD-CITATION (canonical date, source not read) / NOT-FOUND (searched, absent) / UNRESOLVED (sources conflict).
No fabricated dates. Companion: 02_lit/COUNTRY_CARDS/{JPN,KOR,HKG}.md and UNIVERSALIZATION_TIMING.md (rival-theory timing predictions). -->

# UNIVERSALIZATION_TIMELINES_JPN_KOR_HKG — dated crossings, policy dates, and what they change

**The question.** For Japan, Korea and Hong Kong universalization is already achieved; the outcome of interest is **when**. A level model cannot discriminate where the level is at ceiling — the timing of each crossing, and the policy dates that bracket it, are the moments a cohort-flow model must reproduce.

## 0. Definitions — read this before quoting any year

A "universalization year" is meaningless without naming the **measure**:

| Measure | What it counts | Why it moves the year | Available for our three systems? |
|---|---|---|---|
| **Enrolment ratio (GER)** | enrolled / official-age population, includes over-age & repeaters; can exceed 100 | earliest crossing; can exceed 100% | **YES** — `04_data/data/gmr_observed_6countries_1970_2024.csv` (UIS/GMR), 1970–2024 |
| **Net enrolment ratio (NER/ANER)** | enrolled *age-appropriate* / age population (ANER adjusts for over-age) | later than GER; ANER > NER | **YES** — same series |
| **Completion rate** | share of a cohort *finishing* the level | latest; the right measure for "universalized" substantively | **PARTIAL — only KOR has it** (2000+). JPN: NOT-FOUND. HKG: NOT-FOUND. |
| **Attainment** | share of population 15+ whose highest level is X | stock measure, lags cohort experience by decades | HKG: 2020–2025 only (`edb_educational_attainment.csv`); JPN/KOR: NOT-FOUND |

**Consequence.** The only *cohort-completion* crossings I can compute from the current data layer are Korean (2000+). For Japan and Hong Kong the honest answer is: **enrolment-based crossings are DERIVED; completion-based crossings are NOT-FOUND and must be sourced (MEXT 100-year statistics; HK Census historical attainment tables; OECD Education at a Glance attainment series).** Any table that reports a single "year universalized" for JPN/HKG without naming the measure is not usable as a target.

---

## 1. JAPAN

### 1a. Attainment / completion crossings
| Level | Completion-based crossing | Status |
|---|---|---|
| Primary | **NOT-FOUND** in current data (no completion series for JPN) | needs MEXT 100-year series / OECD attainment |
| Lower secondary | **NOT-FOUND** | needs MEXT |
| Upper secondary | **NOT-FOUND** | needs MEXT |
| Tertiary | **NOT-FOUND** as completion; enrolment-based only (below) | needs OECD EaG attainment |

### 1b. Enrolment-based crossings (DERIVED from the UIS/GMR series)
| Level | Crossing | Value | Status |
|---|---|---|---|
| Tertiary, mass (Trow 15%) | **before 1971** — first series year 1971 is already 16.9% | GER 16.9% (1971) → implies crossing in the late 1960s | **DERIVED** |
| Tertiary, universal (Trow 50%) | **2013** first year ≥50% (62.8%) — *gaps in series may hide an earlier crossing* | GER 62.8% (2013) | **DERIVED — check for missing years before citing** |
| Primary/lower-sec/upper-sec | no NER/ANER/GER series for these levels for JPN in the panel | — | **NOT-FOUND in data layer** |

### 1c. Policy / institutional dates
| Date | Event | Citation / access |
|---|---|---|
| **1872** | *Gakusei* (Education Order) — national school system | STANDARD-CITATION (Hara & Saito; JICA study snippet only) |
| **1900** | Elementary School Order — tuition abolished, compulsory-attendance rules clarified; attendance rising through the 1890s | **OBSERVED** (MEXT, *Japan's Modern Educational System*, "The Abolition of Tuition and the Clarification of Rules for Compulsory Attendance") |
| **1907** | Compulsory primary extended to **six years** | STANDARD-CITATION (not read at source) |
| **1947** | Fundamental Law of Education + **6-3-3-4** system: compulsory lower secondary created | STANDARD-CITATION |
| **post-1947** | Upper-secondary expansion during the high-growth era; "exam hell" complex | STANDARD-CITATION |

**Conflict to resolve:** whether Japan's primary system should be dated **1900** (tuition/attendance order) or **1907** (six-year compulsion). Both are defensible; they answer different questions (legal compulsion vs effective universal attendance). Marked **UNRESOLVED** — do not pick silently; report both.

---

## 2. KOREA

### 2a. Attainment / completion crossings — **the only completion series in the data layer**
| Level | Crossing | Value | Status |
|---|---|---|---|
| Lower secondary, completion ≥90% | **2003** (first series year; already 99.9%) | completion_lower_secondary 99.9% (2003) → 100.0% (2023) | **DERIVED** — the crossing predates the series, so 2003 is a *lower bound on lateness*, not the crossing year |
| Upper secondary, completion ≥90% | **2000** (first series year; 97.3%) | 97.3% (2000) → 99.5% (2023) | **DERIVED** — same caveat |
| Primary, completion | only one observation (2012, 100.0%) | — | **DERIVED (single point — cannot date a crossing)** |

### 2b. Enrolment-based crossings (DERIVED)
| Level | Crossing | Value | Status |
|---|---|---|---|
| Primary, NER ≥90/≥95 | **before 1971** (95.9% in first series year) | NER 95.9% (1971) | **DERIVED** |
| Lower secondary, ANER ≥90 | **1991** (91.2%); ≥95 in **1996** (96.7%); ANER 36.2% in 1971 | — | **DERIVED** |
| Upper secondary, GER ≥90 | **1994** (91.6%, first series year) | GER 91.6% (1994) → 100.3% (2018) | **DERIVED** |
| Tertiary, universal (≥50%) | **before 2000** — first series year 2000 is already 74.7% | GER 74.7% (2000) | **DERIVED — do not report a crossing year; it predates the series** |

### 2c. Policy / institutional dates
| Date | Event | Citation / access |
|---|---|---|
| **1949** | Education Law: 6-year primary | STANDARD-CITATION |
| **1953-54** | Compulsory primary education; **Six-Year Compulsory Education Plan launched 1954**; primary enrolment **96.4% by 1959** | STANDARD-CITATION (World Bank document; Korean-language source gives the same 1954/96.4% pair — **second-hand, needs MOE/KEDI original**) |
| **1969** | Middle-school equalisation / entrance-exam abolition — drives lower-secondary expansion | STANDARD-CITATION |
| **1974** | High-school equalisation policy | STANDARD-CITATION |
| **1985-2004** | Middle-school compulsory education phased in (islands/rural first, national completion 2004) | STANDARD-CITATION |
| **1994+** | CSAT-centred admissions; tertiary massification | STANDARD-CITATION |

**Conflict to resolve:** compulsory primary is dated **1953** in some sources (Education Law implementation) and **1954** in others (plan launch). The 96.4%-by-1959 figure is consistent with either. Marked **UNRESOLVED**.

---

## 3. HONG KONG

### 3a. Attainment / completion crossings
| Level | Completion-based crossing | Status |
|---|---|---|
| Primary / lower-sec / upper-sec completion | **NOT-FOUND** — the panel has no HKG completion series | needs HK Census historical attainment tables |
| Attainment (stock), 2025 | Primary-and-below **16.1%**; secondary **47.6%**; degree **27.6%** of population 15+ | **OBSERVED** (`edb_educational_attainment.csv`, EDB/C&SD GHS 2025) — a *stock* snapshot, **not** a crossing year |

### 3b. Enrolment-based crossings (DERIVED)
| Level | Crossing | Value | Status |
|---|---|---|---|
| Primary, NER ≥90 | **1974** (91.1%); ≥95 in **1977** (95.1%); 88.5% in 1971 | — | **DERIVED** |
| Lower secondary, ANER ≥90 | **2014** (93.7%) — **artefact warning**: 9-year compulsory schooling dates from **1978**, so this late crossing is a measure/denominator artefact, not history. NER lower-sec: 76.7% (2001) → 92.3% (2018) | — | **DERIVED, FLAGGED UNRELIABLE** |
| Upper secondary, GER | 68.7% (2001) → **100.2% (2014)** → 106.1% (2019) | — | **DERIVED** |
| Tertiary, mass (Trow 15%) | **1992** (19.6%; 7.3% in 1971) | — | **DERIVED** |
| Tertiary, universal (Trow 50%) | **2008** (55.8%) | — | **DERIVED** |

### 3c. Policy / institutional dates
| Date | Event | Citation / access |
|---|---|---|
| **1971** | Free primary education (six years) | STANDARD-CITATION |
| **1978** | **Nine-year free compulsory education** (primary + junior secondary) — EDB 1978 white paper on secondary/tertiary development exists, not read | STANDARD-CITATION (white paper located, unread) |
| **2008/2009** | **New senior secondary academic structure (3-3-4)**: 3-year junior + 3-year senior secondary replacing 7-year secondary | **UNRESOLVED — 2008 is the policy/announcement year, 2009 the implementation year; both appear in sources** |
| **2012** | First **HKDSE** cohort (replaces HKCEE + HKALE); first 4-year university intake | STANDARD-CITATION |
| **1989-95** | University-place expansion (standard claim: age-cohort participation ~8% → ~18%) | STANDARD-CITATION — figure not verified |

**Conflict to resolve:** the 3-3-4 reform is dated **2008** (policy) or **2009** (implementation) in different sources; the examination transition is **2012**. Three defensible "dates" for one reform — the model must pick one and say which. **UNRESOLVED.**

---

## 4. What it changes for the model

1. **Level models cannot discriminate at ceiling.** For JPN/KOR/HKG the level is saturated; any rival mechanism can fit the level. **The model must be scored on crossing years and their ordering**, not on final levels.
2. **The crossing years are measure-dependent to a degree that exceeds most modelling tolerances.** GER-based and NER-based crossings differ by up to a decade (HKG lower secondary; KOR upper secondary). A success criterion stated as "crossing year ± X years" must state the measure, or it is untestable.
3. **The ordering of crossings is the robust object.** All three systems order primary → lower-secondary → upper-secondary → tertiary, with widening gaps. A model that gets the *order* and the *gaps* right but the levels off is more credible than one that nails final levels.
4. **Policy dates bracket the crossings and are better identified than the crossings themselves** (JPN 1900/1907; KOR 1954/1969/1974; HKG 1971/1978/2008-12). A cohort-flow model can be tested against a *reform date* even where the attainment series is missing.
5. **For JPN and HKG the completion-based crossings are NOT in the data layer.** Any calibration target advertised as "Japan universalized primary in year Y (completion)" is currently unsupported by this package. Record it as a required data pull, not a target.

## 5. Data needed (posted to bridge as ASK to deepseek-data)
1. **JPN**: MEXT 100-year education statistics — primary/lower-sec/upper-sec **completion** by cohort, 1900-1990; OECD EaG attainment 25-64 by level.
2. **KOR**: KEDI/KOSIS historical completion by level **pre-2000** (the current series starts 2000/2003).
3. **HKG**: Census & Statistics Department historical attainment tables (1971-2021 by census round) + EDB enrolment by level 1950-1990.
4. **All three**: a conflict file for the unresolved dates above (JPN 1900/1907; KOR 1953/1954; HKG 2008/2009/2012) so the Council can adjudicate once.

## 6. Cross-links
- `10_massification/lit/UNIVERSALIZATION_TIMING.md` — what each rival theory (Trow, world society, MMI, human capital, push-pull, state-building, fertility) predicts about the *crossing year*, with falsifiers. This file is the evidence side; that file is the prediction side.
- `02_lit/COUNTRY_CARDS/JPN.md`, `KOR.md`, `HKG.md` — gates, cohort flows, economy context.
- `02_lit/SHADOW_TARGETS.csv` — the participation targets for the same three systems (secondary phase is closed; cited only as prior).
- `04_data/data/gmr_observed_6countries_1970_2024.csv` — the series all DERIVED crossings come from; `gmr_source_disagreements.csv` — why measures disagree.
