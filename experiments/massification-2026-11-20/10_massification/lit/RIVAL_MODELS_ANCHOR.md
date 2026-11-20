<!-- Writer: lit-archivist, 2026-11-20. Deliverable requested by repo-auditor (design pivot): single anchor system,
report layer + rival models on ONE record + discriminating-test table. Write scope: 10_massification/lit/ only.
DESIGN, NOT RESULTS. Labels: OBSERVED / DERIVED / STANDARD-CITATION / NOT-FOUND / BLOCKED / UNREAD.
Companion files (must not drift): ANCHOR_SYSTEM_EVIDENCE.md (system record + state/demand/supply evidence),
RIVAL_MODELS_TO_TEST.md (short summary of the rival slate), UNIVERSALIZATION_TIMELINES_JPN_KOR_HKG.md (kept separate). -->

# RIVAL_MODELS_ANCHOR — report layer, rival models on one record, and the discriminating tests

**Anchor system: PHILIPPINES (provisional; Council to name).** Rationale (stated, not assumed): it is the worked case in both prior manuscripts; it has a dated policy event (RA 10533, 2013) preceded by a 64-year non-event; it is the only system in the data layer with a **full completion series** at all three school levels (1999–2024); and it carries both mechanisms the earlier phase established (informal/formal margin; migration channel). Portability candidates: **CHN** (full completion series, high state capacity) and **HKG** (no completion series — enrolment-only test).

## 1. UNESCO / World Bank report layer — what each document actually supplies

| Document | Table / page | Access status | Number it supplies | Use |
|---|---|---|---|---|
| **IBE country profile commissioned for EFA GMR 2007 — Philippines**, IBE/2006/EFA/GMR/CP/70, 13 pp. (UIS 2002/03–2004/05) | tabulated ISCED tables; age-specific enrolment ratios | **OBSERVED** (text captured by data-hunter; `04_data/gmr_snapshots/`, archived via Wayback) | Compulsory age **6–12**; ISCED 0 GER **39.9** (2003/04), NER **31.1** (2002/03); **59.3%** of primary entrants had preschool experience (2003/04); age 5 = 51.7, age 6 = 97.8 | Pre-reform baseline (K-10 era); continuity of the primary pipeline |
| **World Bank (2017), *Developing Socioemotional Skills for the Philippines' Labor Market***, DOI 10.1596/978-1-4648-1191-3 | **Table 2.1** (and Fig. 2.4) | **VERIFIED** (full text read; `02_lit/raw/wb2017_phl_socioemotional_skills.txt`) | Firms citing *inadequate workforce skills* as a major obstacle: **7.8% (2009) → 10.1% (2015)**; manufacturing 6.7→7.3; services 8.2→11.0 | The demand-pull test: skills shortage is NOT the binding constraint |
| **World Bank (2019), *Philippines Basic Education Public Expenditure Review*** (BEPER) | unknown tables (quintile survival by grade 2007–2017, cited in the October manuscript) | **UNREAD** — located as a citation only; document not retrieved this session | Grade-to-grade survival by income quintile; the "gap opens at lower-secondary and widens" finding | The equity/MMI gradient; **the single most important unread report for this anchor** |
| **UNESCO UIS / SDG4 series** (via data-hunter `UNIVERSALIZATION_SERIES.csv`, UIS provenance) | completion_primary / completion_lower_secondary / completion_upper_secondary; ger_tertiary | **OBSERVED** (series on disk) | Primary completion 83.2 (1999) → **98.3** (2024), ≥90 in **2017**; lower-secondary 58.9 → **92.4**, ≥90 in **2024**; upper-secondary 59.7 → **75.0**, **never ≥90**; tertiary GER 16.3 (1971) → 51.1 (2025) | The system record all rivals must face |
| **OECD *Education at a Glance*** | — | **BLOCKED** (oecd.org HTTP 403, recorded by data-hunter) | attainment/transition benchmarks | Not available; do not cite |
| **ILO WESO / informality** | — | **BLOCKED** (ILOSTAT 403) | informality, youth unemployment | Not available; floor mechanism remains unanchored |
| **PSA FIES/APIS/LFS** | — | **BLOCKED** (403) | returns by education, household spending | The biggest gap; returns cannot be measured for the anchor |

**Honest summary of the report layer.** Two report-based facts are usable (the 2007 IBE profile baseline and the 2015 Enterprise Survey constraint share), one crucial report is **unread** (BEPER 2019), and the two sources that would nail the demand-pull and floor channels are **blocked**. The Council should treat the report layer as **thin**: it supports the system record and the skills-constraint test, not the returns or informality tests.

## 2. Rival models applied to the same PHL record

For each: mechanism → **exact prediction** (timing / levels / mechanism) → **discriminating observable** → data needed.

### 2.1 World society / neo-institutional (Meyer; Schofer & Meyer 2005)
- **Mechanism.** Global legitimated models of the modern state drive expansion; adoption is partly decoupled from domestic economic need.
- **Exact prediction for PHL.** Expansion should track **international institutional exposure and dates** (EFA 1990, MDG 2 2000, SDG 4 2015) rather than returns; a reform like K-12 should be **packaged in rights/equivalence language** and adopted when the global model demands it. Completion should rise broadly **without** matching employer demand.
- **Discriminating observable.** *(a)* Timing of adoption relative to global declarations — here the record **contradicts a naive version**: SDG 4 (Sept 2015) postdates RA 10533 (Jan/May 2013). *(b)* Cross-country synchrony at different GDP p.c. *(c)* Expansion with a flat skill constraint (observed: 10.1%).
- **Data needed.** Cross-country completion panel (available); a coded justification corpus for 2000–2013 (not available).

### 2.2 Human capital (Becker/Mincer; returns literature)
- **Mechanism.** Investment responds to expected returns; expansion follows the wage premium with a lag.
- **Exact prediction.** Completion should **accelerate where/when returns are high** and **decelerate when they fall**; the 2018 free-tuition reform (RA 10931) should raise tertiary entry by lowering cost.
- **Discriminating observable.** Does the **level-specific** return series lead the level-specific completion series? The record shows upper-secondary completion rising only 15.3pp in 25 years — slow relative to primary/lower-secondary — which is **consistent with returns to the top of the school system being weaker** but does not establish it.
- **Data needed.** PHL returns by education over time (PSA blocked). Without it, this rival cannot be tested, only assumed.

### 2.3 Signalling / queue-credential (Spence; Arrow; Thurow; Collins)
- **Mechanism.** The credential sorts, not trains; schooling is defensive; requirements ratchet.
- **Exact prediction.** Investment **intensifies as a level saturates**; the *requirement* rises while job content is flat; completion should keep rising **even when returns fall**. In PHL terms: upper-secondary at 75% with tertiary GER at 53% and rising is the **ceiling moving up** rather than the base completing — exactly the queue-credential trace.
- **Discriminating observable.** Does the employer **requirement schedule** rise independently of job content? (Enterprise Surveys measure perceived constraints, not requirements — so the standard data cannot answer this.)
- **Data needed.** Employer requirement series / job postings; licensed-profession entry rules (PRC). Neither in hand.

### 2.4 Political economy / state-building (Gellner; Tilly; Paglayan 2024; Ansell & Lindvall 2020)
- **Mechanism.** Schooling expands to build legibility, order and state capacity — often after internal conflict — not in response to returns.
- **Exact prediction.** Expansion should cluster **after capacity/conflict shocks**, and should be **supply-side implemented** (laws → places → teachers). For PHL: RA 10533 should show up as a **step in stage structure and a rise in completion**, and its 64-year delay should be explained by **state capacity**, not by absent recommendations.
- **Discriminating observable.** The 2013 reform is the moment: state-push predicts a step change in the *stage structure* and a rise in completion. **Observed: upper-secondary completion is 75.0 in 2024 and never crossed 90; lower-secondary crossed 90 only in 2024.** So the state push moved the floor and the lower levels but did **not** universalize the top — this partially **falsifies a naive state-push**, and the residual must be explained by capacity, cost, or demand.
- **Data needed.** Place-expansion and teacher-hiring series 2010–2024 (ASKed from data-hunter); a state-capacity index.

### 2.5 Demographic / cohort
- **Mechanism.** Cohort size changes the per-child cost/benefit of schooling; shrinking cohorts raise per-child investment and accelerate per-child completion.
- **Exact prediction.** For PHL — a still-growing cohort — the prediction is the **opposite** of JPN/KOR: expansion should be **slower** per child and driven by places, not by per-child investment. Cohort size (0–14) is available in `UNIVERSALIZATION_SERIES.csv`.
- **Discriminating observable.** Does completion rise when the cohort shrinks? PHL's cohort has not yet shrunk, so this rival makes a **timing prediction the anchor can test by contrast**: the same model run on KOR/JPN should show the demographic channel where PHL does not.
- **Data needed.** Cohort series (available); per-child spending (blocked).

### 2.6 Formal education-expansion models (from the model cards, all equation-verified)
- **GXL 2017** (SD pipeline; cascading + provider reinforcement): predicts **overshoot** of degree supply after shocks and a **U-shaped** provider-feedback effect. In PHL terms, the tertiary GER swing (16.3→51.1) is the trace; the model predicts the *mechanism* (provider capacity response) rather than a date.
- **Yoo 2003** (fixed cutoff vs quota): predicts effort depends on where the gate line sits; falsifier = cutoff at extremes reduces aggregate effort.
- **Kang 2026** (estimated tournament): predicts 77%/89% of tutoring expenditure is competition-driven — a *post-universalization* mechanism, useful for the portability stage (HKG/KOR), not the anchor's massification.
- **He 2024** (`S_cut = S̄ + kσ_S`): the gate line as a mean-plus-kσ rule.
- **Ostrovsky & Schwarz 2010** (compression; balanced disclosure): predicts unraveling iff disclosure exceeds the balanced amount — relevant to credential *reading*, not expansion timing.
- **Exact prediction for PHL.** These models predict **mechanisms and shapes**, not calendar dates; the discriminating observable is whether the fitted provider/gate parameters reproduce the *level ordering with gaps* (primary 2017 → lower-sec 2024 → upper-sec not yet).

## 3. Discriminating-test table (rival × prediction × moment × data availability) — DESIGN, NOT RESULTS

| Rival | Prediction (direction) | Test moment | Observable | Data availability |
|---|---|---|---|---|
| World society | Adoption tracks global dates, not returns; expansion decoupled from demand | 1990 EFA / 2000 MDG 2 / 2013 RA 10533 / 2015 SDG 4 | Adoption timing vs declaration dates; flat skill constraint | **Available** for dates + constraint; justification corpus missing |
| Human capital | Completion accelerates with returns; slows when returns fall | level-specific return series vs completion series | Lead-lag of returns → completion by level | **BLOCKED** (PSA) |
| Signalling/queue | Requirement ratchets at saturation; completion rises despite falling returns | upper-secondary at 75% with tertiary GER 53% | Requirement schedule vs job content | **NOT FOUND** (no requirement data) |
| State-building | Reform produces step in stage structure + completion | 2013 RA 10533 | Completion by level pre/post; places/teachers | **Partially available** — completion yes, places/teachers ASKed |
| Demographic | Expansion slower per child while cohort grows | PHL cohort 0–14 series | Cohort size vs per-child completion | **Available** (cohort series); per-child spend blocked |
| Formal expansion (GXL/Yoo/Kang/He) | Mechanism shapes: overshoot, gate-position effects, competition shares | tertiary GER swing; gate parameters | Fitted shapes vs level ordering with gaps | **Available** for GER; gate data partial |
| MMI (Raftery-Hout) | Inequality falls only after saturation | lower-secondary saturation (2024) | Class-specific crossing years | **BLOCKED** — needs household surveys |

## 4. Design notes the runner must honour
1. **Measure must be named** for every crossing claim (completion vs GER vs NER differ by up to a decade).
2. **Fit 1999–2013, holdout 2014–2024.** Fitting through the reform makes the policy test circular.
3. **Score rivals on ordering and gaps**, not levels: the anchor's discriminating pattern is *primary crossed, lower-secondary just crossed, upper-secondary has not*.
4. **±5 years** tolerance for crossing-year claims (Council A4).
5. **Rival models that need blocked data (human capital, signalling, MMI) are design-only for now** — state that in any results file rather than silently dropping them.

## 5. What this changes
The rival slate can be run **now** on four of six accounts (world society timing, state-building step, demographic contrast, formal-model shapes) using data already on disk. Two accounts — human capital and signalling/MMI — **cannot** be tested on the anchor without PSA household/returns data and employer requirement data. That split should drive the Council's next data ask, not the modelling order.
