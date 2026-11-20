<!-- Writer: lit-archivist, 2026-11-20, task-35. Scope: literature only. No model output below.
Verification legend: VERIFIED = primary text read this session (file in 02_lit/raw/ or /tmp archive, hash noted).
STANDARD-CITATION = canonical account, primary text NOT retrieved this session; the mechanism and any
thresholds are as standardly cited in the literature, and must be checked against the original before
publication. NOT-FOUND = searched and did not find; treat as a gap, not as zero. -->
# SCALING_LAWS — what is a law, what is a regularity, and what must be estimated

**Distinction used throughout:** a **scaling law** is a power-law relation `Y = Y₀ N^β` with a stable exponent β across samples and an interpretation; a **regularity** is a stable empirical pattern without a claimed law; a **threshold** is a descriptive cut-point. Only the first is a law.

---

## 1. Urban scaling — the only genuine scaling law in this file (VERIFIED)
Bettencourt, Lobo, Helbing, Kühnert & West (2007), *PNAS* 104(17):7301–7306, "Growth, innovation, scaling, and the pace of life in cities". Retrieved and mined this session (PMC1852329; `raw/bettencourt2007_pnas_urban_scaling.txt`).

**Functional form.** `Y(t) = Y₀ · N(t)^β` — city indicator `Y` against population `N`, estimated in log–log OLS with reported confidence intervals and adjusted R².

**Verified exponents from Table 1 (β [95% CI], adj-R², n, sample year):**

| Indicator | β | 95% CI | adj-R² | n | Sample |
|---|---|---|---|---|---|
| New patents | **1.27** | [1.25, 1.29] | 0.72 | 331 | US 2001 |
| Inventors | **1.25** | [1.22, 1.27] | 0.76 | 331 | US 2001 |
| Private R&D employment | **1.34** | [1.29, 1.39] | 0.92 | 266 | US 2002 |
| "Supercreative" employment | **1.15** | [1.11, 1.18] | 0.89 | 287 | US 2003 |
| R&D establishments | **1.19** | [1.14, 1.22] | 0.77 | 287 | US 1997 |
| R&D employment | **1.26** | [1.18, 1.43] | 0.93 | 295 | China 2002 |
| Total wages | **1.12** | [1.09, 1.13] | 0.96 | 361 | US 2002 |
| Household water consumption | **1.01** | [0.89, 1.11] | 0.96 | 295 | China 2002 |
| Gasoline stations | **0.77** | [0.74, 0.81] | 0.93 | 318 | US 2001 |
| Gasoline sales | **0.79** | [0.73, 0.80] | 0.94 | 318 | US 2001 |
| Length of electrical cables | **0.87** | [0.82, 0.92] | 0.75 | 380 | Germany 2002 |
| Road surface | **0.83** | [0.74, 0.92] | 0.87 | 29 | Germany 2002 |

**The three-category taxonomy (verified verbatim from the paper).** Exponents cluster into three groups: **(i) β ≈ 1** for individual human needs (jobs, housing, household water); **(ii) β ≈ 0.8 < 1 (sublinear)** for material quantities displaying economies of scale (infrastructure: cables, road surface, gasoline stations); **(iii) β > 1 (superlinear)** for socioeconomic output (patents, wages, R&D employment, "supercreative" employment).

**Status.** This is the strongest *candidate law* available: stable exponents, tight CIs, large samples, and an interpretation (mixing/matching in dense networks). **But note the limits before transplanting it into education:** the samples are city cross-sections in three countries; the estimates are OLS on log-log with no causal identification; and **there is no education indicator in Table 1**. The exponents are a *benchmark for what a scaling law looks like*, not a parameter for a schooling model.

## 2. Returns to schooling — a regularity, not a scaling law
Global average private return **8.8%/yr** (headline ~9%), EAP **8.7%**, social >10% at secondary+ (Psacharopoulos & Patrinos 2018, WPS8402, VERIFIED). "Very stable over decades."
**Status: regularity.** It is a characteristic value of a Mincer coefficient, not a power law in any variable. Using 8.8% as a *parameter* is legitimate (`02_lit/ECON_TARGETS.csv`, usable_as = calibration-only); calling it a scaling law is not.

## 3. Enrolment vs income — must be estimated, currently unestimated
**Status: NOT FOUND as a published elasticity for our countries.** The relation `enrolment ratio = f(GDP p.c.)` is one of the programme's core scaling candidates (README question 3), but no retrieved source supplies a defensible elasticity. Data to estimate it exist on disk (`04_data/data/wdi_4countries_long.csv`, `gmr_observed_6countries_1970_2024.csv`, `uis_sdg4_*`).
**Recommendation.** Treat the income elasticity of enrolment as an **output of `relations/`/`model2/`**, not an input here. Predeclare: specification (logit of ANER on log GDP p.c., country FE, period split), fit window 1980–2010, holdout 2011–2024.

## 4. Education–output elasticities — no canonical estimate
**Status: NOT FOUND.** "Education–output elasticity" is not a standard, uniquely defined quantity: growth-accounting estimates depend entirely on the assumed human-capital share and on how schooling is converted to skill units, and cross-country growth regressions are plagued by endogeneity. **Do not put a number in the model and call it literature.** If the Council wants one, it must be an explicitly assumed calibration with a sensitivity range.

## 5. Sectoral productivity scaling — not an established literature
**Status: NOT FOUND.** There is no canonical "sector productivity scaling law". The nearest empirical object is the urban scaling of wages (β ≈ 1.12 in Table 1 above), which is a *city-size* relation, not a sectoral one. Sector shares vs income (structural transformation) are a *development regularit
y* (Kuznets/Petty), not a scaling law with a stable exponent for our countries.

## 6. Education-specific regularities worth testing (candidates, not laws)
| Regularity | Statement | Status | Test |
|---|---|---|---|
| Trow thresholds | 15% / 50% of cohort mark regime changes in tertiary | STANDARD-CITATION | Discontinuity tests at thresholds in ANER/tertiary series |
| Logistic universalization | enrolment follows a logistic/Gompertz with country-specific midpoint and ceiling | candidate | Fit logistic vs Gompertz vs linear on 1980–2010, holdout 2011–2024 |
| MMI saturation timing | inequality falls only after saturation | STANDARD-CITATION | Transition odds by origin around saturation |
| Cohort-size effect | smaller cohorts ⇒ higher per-child investment | NOT VERIFIED | Cohort size vs per-child spending/participation |

## 7. Verdict table — law vs regularity
| Relation | β / estimate | Units | Sample | Identification | Verdict |
|---|---|---|---|---|---|
| City indicator ~ population | 0.77–1.34 (see table) | exponent | 29–380 cities, US/DE/CN | OLS log-log, cross-section | **candidate law** (not for education) |
| Returns to schooling | 8.8%/yr | % per year | ~139 economies, 1950–2014 | Mincer compilation | regularity |
| Enrolment ~ income | unknown | elasticity | — | — | **must estimate** |
| Education–output | unknown | elasticity | — | — | **no canonical quantity** |
| Sector shares ~ income | unknown | — | — | — | development regularity |
| Universalization shape | unknown | logistic params | 6 countries on disk | — | **must estimate** |

**Bottom line for the Council.** Exactly **one** genuine scaling law is available (urban, with verified exponents and CIs) and it is *about cities, not schooling*. Everything education-specific in this file is either a regularity (returns), a threshold (Trow), or something the programme must estimate itself (enrolment–income, universalization shape). The programme should not describe its own fitted exponents as "scaling laws" until they are shown to be stable across samples and periods — that is the difference between `relations/` producing a *finding* and producing a re-description of its fitting window.
