# STAGE 1 — CONSTRUCT / FEASIBILITY AUDIT (fitted-worlds feasibility pilot, task-24)

**Verdict: STAGE 1 FAILS — "insufficient evidence".** The four-world fitted-worlds question
is **not answerable with the observed series committed to this repository** without inventing
age/unit/scale mappings or a target. Per the pre-registration, the pilot **stops here**: no
frozen split, no synthetic-recovery challenge, no rejection-ABC, no model-free benchmark, and
**no model/fitting compute on region-42 (or anywhere)**.

- Pre-registration: `PRE_REGISTRATION_fitted_worlds_pilot.md`, commit
  **`953a38203e806dd56b4a49e80e5f1ff6e098df49`** (branch
  `research/fitted-worlds-pilot-2026-11-24`, committed **before** this code and before any
  audit/fitting).
- Audit code: `construct_audit.py` (committed after this report); machine-readable results:
  `stage1/stage1_audit.json`.
- Audit method: **inventory and coverage only** — reads committed files on this worktree and
  on other committed branches of this repository via `git show`; no model run, no fitting, no
  imputation, no external data pull, no DHS microdata. No compute was run on the Mac beyond
  this audit's file reading; the server has **not** been used (it remains up and idle).
- Labels: EXPLORATORY. No confirmatory claim. No causal claim. No E1 1.8% comparison.

---

## 1. Observed data actually available in the repository

Only these sources exist (committed). All cover **calendar country-years**, whereas the ABM's
time axis is **synthetic years around a fee-abolition shock**, and the ABM has **no age or
grade variable at all** (one child state per household; `model.py` grep for age/grade = none).

| source | committed location | variables relevant to the ABM | coverage (national, aggregates removed) |
|---|---|---|---|
| D1 WDI/UIS/ILO sweep | `origin/research/massification-panel-2026-11-22` → `sources/wdi_sweep/*.json(.gz)` | `child_work` = ILO/UCW children **7–14 in employment**; `pre_ger` = primary **gross** enrolment ratio; `prm_ner`/`sec_ner` = **net** enrolment; `lsc`/`prm_cmp` = completion; `test_scores` (0–625) / `hci` (0–1); `gdppc`; `repeat_prm` | `child_work`: **100 countries, 281 obs, 1994–2016, median 2 obs/country** (min 1, max 8); `pre_ger`: 207 countries, 1970–2022, median 31 obs; `prm_ner`: 197 countries, 1970–2019; `sec_ner`: 188; `lsc`: 197, 1970–2024; `test_scores`: **172 countries, 2010–2020 only**, 4 obs/country; `gdppc`: 213, 1960–2024 |
| D2 `asia_school_work.json` | `engine/data/asia_school_work.json` | `oos_lower` = adolescents out of school, lower-secondary age (UIS via WDI); `child_labour` = % children **5–17** (ILO/UNICEF estimates as tabulated on Wikipedia) | **21 countries, one mixed-vintage cross-section** (`oos_year` 2015–2022, `cl_year` 2010–2023); 20 with both; 4 composition facts used by their own record as tests only |
| D3 shadow education | `origin/experiment/massification-2026-11-20` → `04_data/shadow_round2/data/` | tutoring **incidence** and fees | **6 countries/sites, 38 + 20 rows**, hand-collected; several are explicitly case studies (e.g. one Cambodian district); years 1996–2023; no harmonised panel |
| D4 E1 multiverse | `origin/research/e1-multiverse-1200-2026-11-25` → record | 17 WDI variables, 179 countries, 1940–2025, 272 derived links | **derived link statistics only** (`edge_table400.csv`, `headline400.json`); the **raw WDI panel is not committed** (it lived at `/root/work/data` on a different host) and no re-pull is allowed |
| D5 Q2 long-run panel | `origin/research/q2-pathways-2026-11-25` → `data/long_run_panel.csv` | child mortality, life expectancy, fertility, **mean years of schooling** (attainment stock), Maddison GDP pc, urban share | 197 countries, 1750–2024; 42,959 rows; schooling is an **attainment stock**, not participation |
| D6 DHS API cache | `origin/research/dhs-api-ecological-2026-11-24` → `data/panel_*.csv` | published DHS **API cells** (no microdata): TFR, GFR, wanted fertility, **median age at first birth by education**, mean CEB by education, women's education | 76–87 countries, 1985–2025; 2-level education split in the committed panels; 369 surveys; **no child-labour, enrolment, tutoring or learning cells** |
| D7 DHS CEB-by-education cells | `origin/research/dhs-acquisition-2026-11-24` → `data/ceb_education_cells.csv` | mean children ever born, women **40–49**, by education (published API cells) | 318 rows, 14 countries, 1988–2025 |
| D8 Philippines HE series | `docs/engine/comparative_cases/philippines_enrolment.json` | higher-education **headcount**, 5 academic years 2015–2020, one country | irrelevant to this ABM (no tertiary layer) |

## 2. Mapping of every model observable (pre-registration §1)

Status key: **compatible** = same target population / unit / definition / period (or a
genuinely age-unspecified aggregate with an exact declared transformation); **partial** =
same broad construct but an age/unit/definition/period mismatch requiring a declared
approximation; **unmatched** = no observed series in the repo or conceptually different.

| # | model output | observed candidate (age, unit, period) | status | why |
|---|---|---|---|---|
| 1 | `ger` — household school-participation share (states 0,1), no age/grade | D1 `pre_ger` (pupils / official-age population, % gross, can exceed 100), `prm_ner`/`sec_ner` (age-specific net enrolment), `lsc` (completion), D5 mean years schooling | **partial** | participation **share of households** vs **gross ratio of pupils**; net enrolment is age-specific while the model has no age; completion/attainment are stocks, not participation; calendar vs synthetic period |
| 2 | `cl` — observed child employment (states 1+2), no age | D1 `child_work` (children **7–14 in employment**, 100 countries, 1994–2016, median 2 obs/country); D2 `child_labour` (**5–17**, 20-country mixed-year cross-section) | **partial** | employment definition broadly matches; **age bands differ and the model has none**; child- vs household-weighted; ILO modelled/administrative estimates; sparse irregular panel, not a change panel |
| 3 | `sw` — study-and-work share | none: UCW publishes such shares, but the committed cache holds **only total employment** | **unmatched** | observed decomposition absent locally |
| 4 | `wo` — work-only share | none, same reason | **unmatched** | observed decomposition absent locally |
| 5 | `hw` — hidden work (state 3) | none | **unmatched** | unobservable by construction; surveys do not publish this state |
| 6 | `tut` — tutoring share | D3 shadow-education incidence (6 countries/sites, 38 rows, case studies, mixed definitions) | **unmatched** | no harmonised country-year panel; using it would invent a national tutoring target |
| 7 | `learn` — mean learning in model grade-equivalents | D1 `test_scores` (0–625, 2010–2020), `hci` (0–1) | **partial** | **unit/scale cannot be mapped** to model grade-equivalents without an invented anchor; observed period only 2010–2020 |
| 8 | `inc` — household mean income in arbitrary model units | D1 `gdppc` (dollars per capita), D5 Maddison GDP pc | **unmatched** | country vs household, dollars vs arbitrary units; only a scale-free shape comparison, which would require inventing a normalisation |
| 9 | Phase B `B1` — post-death birth-spacing contrast | none | **unmatched** | requires birth-interval microdata; DHS API publishes no such cell and microdata acquisition is forbidden |
| 10 | Phase B `B2` — parity-progression gradient by education | D6/D7 mean CEB by education (women 40–49) | **unmatched** | PPR is a different quantity from mean CEB; age band/education categories differ; survey vintages |
| 11 | Phase B `B3` — age-at-first-birth gradient | D6 `FE_AAFB_W_M25` (median age at first birth by education) | **partial** | years vs years, but **median vs mean**, women 25+ vs model women 15–40, mismatched education categories |

**Summary: 0 compatible, 4 partial, 7 unmatched (of 11 model observables).**

## 3. Joint coverage — the decisive point

The four literature worlds differ mainly in the school/work/tutoring utility weights
(`w_pov, w_push, w_tutor, div`) and the fixed parameters (`h_hidden, psi, q_pub0`). Their
observable signature is therefore the **joint decomposition** of school and work states over
time — not any single aggregate. The audit's overlap computation (±2 years, national series):

| overlapping pair | countries | country-year pairs |
|---|---|---|
| `child_work` × `pre_ger` | **90** | **240** |
| `child_work` × `prm_ner` | 93 | 240 |
| `child_work` × `sec_ner` | 78 | 181 |
| `child_work` × `lsc` | 88 | 236 |
| `child_work` × `test_scores` | 35 | 55 |
| `child_work` × `gdppc` | 100 | 281 |

Even taking the most favourable reading, the joint moment is only **total child employment +
an age-mismatched enrolment series**, on a **sparse irregular panel** (child employment:
median 2 observations per country; mixed vintages 1994–2016). It **does not observe**
study-and-work vs work-only vs hidden work — exactly the decomposition the worlds differ in.
There is no documented, measurement-compatible change moment on disjoint countries that could
serve as a frozen training panel and independent validation set.

**Sensitivity (why relaxing the rule does not rescue the pilot):** if "compatible" were
relaxed to accept the two best *partial* constructs (`cl` total employment + net enrolment),
the pilot would still fail the pre-registered joint-constraint condition: the state
decomposition that separates the worlds is unobserved, and a frozen 20-training / 10-validation
country split of documented change moments cannot be built from a median-2-observation,
mixed-vintage series without inventing an age rule and a panel construction. The
pre-registration forbids inventing those.

## 4. Stage-1 decision (pre-registered rule applied)

The pre-registered pass rule required (a) ≥2 **compatible** outputs, (b) those outputs jointly
constraining the four worlds' distinguishing parameters, and (c) a frozen split with ≥20
training and ≥10 independent validation countries. The audit found **0 compatible**
(a fails); the only cross-output overlap is missing the distinguishing decomposition (b
fails); and no compatible joint moment supports the split (c fails).

**Therefore: STOP — insufficient evidence.** As declared in the pre-registration (§1, §8):
no fitting run, no frozen split, no synthetic-recovery challenge, no rejection-ABC, no
model-free benchmark, and **no server draw or cores commitment**. The box was not used.

## 5. What would be needed to make the question answerable

1. An **age/grade-structured** model output (or a declared, testable age-aggregation rule) so
   that UCW 7–14 child-labour states and primary/secondary enrolment can be matched.
2. The **UCW study-and-work and work-only shares** (not just total child employment) as a
   harmonised country-year panel — the decomposition that separates the four worlds.
3. A **learning-scale anchor** (explicit, out-of-sample-validated model→test-score mapping).
4. A **harmonised cross-country tutoring/shadow-education panel** (current data are case
   studies).
5. **DHS birth-interval microdata** for B1 (not permitted in this pilot).
6. Consistent vintages/periods across constructs so a frozen, non-overlapping train/validation
   split is possible.

Until then, any "fitted-worlds separation" result would be a statement about an invented
target, not about observed education systems. Reporting this is the correct Stage-1 outcome.

## Deviations log (Stage 1)

- None from the pre-registration. The audit script was run on the Mac as a **read-only
  inventory** (file reading); no model/fitting compute ran anywhere, so the pre-registration's
  "all model compute on region-42" rule was not engaged. The box was verified up and idle but
  not used.
- The pre-registration's §6 timing pilot is not run because Stage 1 failed (declared stop
  rule); no draw/cores commitment was made.
