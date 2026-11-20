# ECON_LIT — the economics literature behind the model's quantities
**Compiler:** lit-archivist · 2026-11-20 · task-20 · companion file: `ECON_TARGETS.csv`

**Purpose.** The Council is proposing experiments from country profiles. This file states what the *economics literature* actually supplies for each quantity the two-way model needs, with the number, the unit, the identification, the disagreement, and the model parameter it maps to. Where the literature supplies nothing, it says so.

**Access legend.** `FULL-TEXT` = read this session (file in `raw/`). `ABSTRACT/METADATA` = verified citation only. `NOT FOUND` = I searched and did not find a citable estimate — this is a finding, not an omission.

---

## 1. Returns to schooling

### 1.1 The global benchmark — **FULL-TEXT**
Psacharopoulos & Patrinos, *Returns to Investment in Education: A Decennial Review of the Global Literature*, World Bank Policy Research Working Paper **8402** (2018). Text archived: `raw/psach_patrinos_wps8402.txt`.

| Quantity | Value | Notes |
|---|---|---|
| Global average **private** return to one additional year of schooling | **~9% per year**; annex estimate **8.8%** | The paper's own summary: "about 9 percent a year and very stable over decades" (p. 1). Mincerian, cross-section, 1950–2014, ~139 economies. |
| **Social** returns | **above 10% at secondary and higher** education | p. 1. |
| Private returns by income level | low **9.3**, middle **9.2**, high **8.2**, world avg **8.8** | Annex table. |
| Social returns by income level | low **5.0**, middle **7.0**, high **9.2**, world avg **8.0** | Annex table. |
| East Asia & Pacific | private **8.7**, social **6.9** | Regional table. |
| Trend | small but statistically significant *decline* across the long series (coefficient implies ~0.2pp, **R² = 0.003**), yet returns **rose post-2000** (private 7.8 pre-2000 → 8.6 post-2000) | The two statements coexist in the paper; the time trend explains almost nothing. |

**Disagreements.** The decennial review is the standard benchmark but it is a *compilation of Mincer regressions*, so it inherits every identification problem below. Its "stability" is a statement about the distribution of cross-sectional estimates, not a causal constant.

### 1.2 Country-specific Mincer returns for PHL / KHM / CHN / KOR
**NOT SUPPLIED THIS SESSION.** The WPS8402 annex does contain country-level estimates, but I did not extract them, and I will not fabricate a number. Honest status: **a table of country returns exists in the annex and should be extracted before any country-specific return is hard-coded.** What I can say: the regional East Asia & Pacific private return (8.7%) is the defensible placeholder, and all four of our countries sit near the world average in the sources the manuscripts cite.

### 1.3 Ability bias and the signalling critique
**NOT VERIFIED THIS SESSION.** The manuscripts cite **Clark & Nielsen (2024)**, "The returns to education: A meta-study" (CEPR DP18769), for the claim that average causal returns may be near zero. I could not retrieve it (see `CLAIM_REGISTER.csv` J-06 family and `LITERATURE_LEDGER` §B). This matters because the paper's household mechanism is explicitly built to survive a low causal return — but **the size of ability bias is currently an unverified number in the argument, not a known one.**

### 1.4 Model mapping
- `r_school` annual return: **0.088** (world average, WPS8402) is the defensible default; 0.087 for EAP.
- For a K-12 extension (+2 years), 0.088/year implies ~19% log-wage gain before selection — a **check**, not a target.
- Do **not** calibrate a degree premium separately from secondary without a country Mincer table; the literature does not hand you one in this package.

---

## 2. Does schooling create formal jobs, or redistribute them?

**This is the single most important gap in the literature for this project.**

### 2.1 What the firm-side evidence says — **FULL-TEXT (secondary compilation)**
World Bank, *Developing Socioemotional Skills for the Philippines' Labor Market* (2017), DOI 10.1596/978-1-4648-1191-3. Table 2.1, from World Bank Enterprise Surveys 2009 and 2015:

| Share of firms citing **inadequate workforce skills** as a *major obstacle* | 2009 | 2015 |
|---|---|---|
| All firms | **7.8%** | **10.1%** |
| Manufacturing | 6.7% | 7.3% |
| Services | 8.2% | 11.0% |

**Interpretation that matters for the model:** in the Philippines, **~90% of firms do not name skills as a major obstacle**, and the share rose only 2.3pp over six years. So the "employers are starved for educated workers" premise is **weak evidence** — which cuts *for* the paper's account (employers screen credentials for cheapness, not because skills are scarce) and *against* a pure human-capital/skill-shortage story. The same report finds inadequate skills matters most among the *most dynamic* firms, so the constraint is not zero — it is concentrated.

### 2.2 Elasticity of formal employment to educated labour supply
**NOT FOUND.** No credible estimate for PHL/KHM of how formal-sector employment responds to an increase in educated labour supply. This is exactly the parameter the Triad's "responsive jobs" sweep varies (0–1.5) and the paper's Prediction 2 depends on. **The literature cannot supply it; the model must report it as unidentified.**

### 2.3 Overeducation / establishment dynamics / macro productivity
**NOT VERIFIED.** The overeducation literature (e.g. ILO/IMF mismatch series) and firm-dynamics evidence were not retrieved this session. GXL 2017 (see `MODEL_CARDS.md` §5) supplies a *theoretical* cascading mechanism, not an estimate.

### 2.4 Model mapping
- The Enterprise Survey figure is best used as a **check**: if the model generates a world where most firms report skills as the binding constraint, it contradicts the observed Philippine firm distribution.
- Formal-job elasticity ∈ [0, 1.5] must be labelled **calibration-only, no external anchor**.

---

## 3. Credential requirements in hiring

### 3.1 Verified
- Enterprise Surveys 2009/2015 (above): only ~10% of Philippine firms call inadequate skills a major obstacle — evidence *against* a tight skill-shortage-driven credentialism story and *consistent with* cheap-screening credentialism.
- GXL 2017's motivating facts (FULL-TEXT): in 1970 <1% of US taxi drivers and 2% of firefighters had college degrees; **now >15% in both** — a measurable "degree inflation" fact in an advanced economy (quoted from Vedder et al. 2013 in GXL).

### 3.2 NOT SUPPLIED
- **World Bank Enterprise Surveys: the share of *jobs* that formally require a degree** (as distinct from the share of workers holding one) — not extracted. The PH 2023 Enterprise Survey exists and has the constraint variables; nobody in the package has queried it.
- **STEP / employer skill-need surveys** — the Cambodia 2024 Employer Skill-Need Survey was on the data plan and is another agent's task; **not retrieved here**.
- **Licensed professions**: PRC (Philippines) board pass rates and the number of licensed professions were **NOT FOUND** this session.
- **Degree inflation over time outside the US** — no PHL/KHM/CHN series found.

### 3.3 Model mapping
The model's gate module needs a **requirement schedule** (share of vacancies requiring credential level c) and a **holding schedule** (share of applicants holding c). The literature supplies **neither for our countries**. The Enterprise Survey constraint share is a *proxy for the tightness of screening*, not for the requirement schedule. Flag as calibration-only.

---

## 4. Informality: transitions, earnings gaps, definitions

### 4.1 Verified
- **Cambodia:** teacher monthly salary **US$44** at the time of the Benveniste fieldwork; a teacher can earn **US$80–100/month** with tutoring (Brehm & Silova WP39, FULL-TEXT). Education spending **2.3% of GDP**; ~**21%** of enrolled students drop out of upper secondary (UNESCO 2010, second-hand).
- **Cambodia shadow fees:** hourly **300–1,000 Riel (US$0.08–0.25)**; one-on-one tutoring up to **US$100/month** (Brehm & Silova WP39, FULL-TEXT).

### 4.2 NOT SUPPLIED
- **PHL informality rate** (share of employment informal) and **KHM informality rate** — **NOT FOUND this session**. The PSA LFS and Cambodia CLFS 2019 are the right sources; the CLFS 2019 report URL was on the handoff list and is the data track's job.
- **Formal↔informal transition rates** — no estimates found. This is the parameter the floor mechanism most needs.
- **Informal/formal earnings gap for PHL and KHM** — no retrieved estimate.
- **Definitional warning from the standards file, confirmed here:** the sources use at least four different informality definitions (enterprise-based, job-based, social-protection-based, ILO 15th ICLS). The model must pick one and say which.

### 4.3 Model mapping
The "floor" needs an informal-sector wage and an informal→formal transition hazard. Neither is in hand. Until they are, any PHL/KHM floor result is **conditional on invented parameters** and must be reported as such.

---

## 5. Migration and remittances

### 5.1 The place premium — **FULL-TEXT**
Clemens, Montenegro & Pritchett, *The Place Premium: Wage Differences for Identical Workers across the US Border*, World Bank Policy Research Working Paper **4671** (2008). Text archived: `raw/clemens_montenegro_pritchett_wps4671.txt`.

| Quantity | Value |
|---|---|
| **Philippines**: wage ratio for observably identical workers in the US vs at home (`R_o`) | **3.99** (main table); alternative specifications **3.80 / 4.36 / 3.71** |
| Median across 42 countries (Bolivia) | **3.98** → the Philippines is *at the median* |
| Range across countries | **1.37–1.43** (Dominican Republic) to **8.4** |
| Method | Mincer-style wage regressions on >2 million formal-sector wage-earners in 43 countries, PPP-adjusted; then corrected using the New Immigrant Survey for unobserved skill selection (`R_e`) |

**Model mapping:** this is the best-anchored quantity in the whole file. A PHL→US move multiplies the wage of an observably identical worker by **~4**. Use **4.0 (range 3.7–4.4)** as the migration wage-gain parameter — and note it is a *gross* place premium, before recognition/licensure barriers.

### 5.2 Nurse emigration and origin-country human capital — **FULL-TEXT (slides)**
Abarcar & Theoharides, *Medical Worker Migration and Origin-Country Human Capital: Evidence from U.S. Visa Policy*, NBER Summer Institute slides, 27 July 2021 (`raw/abarcar_theoharides_slides.pdf`); published in *Review of Economics and Statistics* (2024).
- **"9 nurses for every new migrant"** — the headline structural ratio, now **VERIFIED** at source (slide text; this upgrades `CLAIM_REGISTER` O-38 from unresolved to verified-as-reported).
- Average treatment effect of the US visa expansion on licensed nurses: **3.9 nurses per 100,000 population = 126%** of the pre-period mean of 3.1 per 100,000.
- Supply response runs through **nursing programme entry and pass rates**, not just applications: implied pass rate **38.4%**; pass-rate increase **0.17pp/yr (80%)**.
- Non-nursing disciplines **decline** in enrollment during the expansion — a crowding/relative-price effect the model should be able to reproduce.

**Model mapping:** the "motor in miniature" is real and quantified: a foreign demand shock raised origin-country *licensure* roughly ninefold per migrant, financed largely by households. The project's own Massabm produces **0.25** — a failure the paper already admits. This is the sharpest validation target in the file.

### 5.3 Remittances → schooling
**NOT VERIFIED THIS SESSION.** The Clemens/Yang remittance-and-schooling studies were not retrieved. The manuscripts' remittance figures ($38.3bn, 8.3% of GDP for 2024) remain unresolved (`CLAIM_REGISTER` O-28).

### 5.4 Recognition barriers
**NOT QUANTIFIED.** No estimate of the wage cost of non-recognition, of the probability of recognition by destination, or of the effect of cycle length on recognition was found. The October paper itself concedes the EU/AQRF record is mixed (note `fp`, note `aqrf`). This is a **hard gap**: the migration channel's *barrier* side is currently asserted, not measured.

---

## 6. Provider/supply economics of the shadow sector

### 6.1 Verified prices
| Market | Price | Source |
|---|---|---|
| Korea (official) | **434,000 won/month** per student; **553,000 won** per participating student; national total **27.1tn won** (2023) | MODS/KEDI survey 2023, press release 2024-03-14 (FULL-TEXT) |
| Cambodia | **300–1,000 Riel/hour (US$0.08–0.25)**; one-on-one up to **US$100/month** | Brehm & Silova WP39 (FULL-TEXT) |
| Nepal (teacher tutoring) | median **300 NPR/month** (govt schools), **400** (private); mean 359/566; SD 391/646. Private-school annual fees 7,960 NPR; GDP p.c. 20,800 NPR; 76 NPR/US$ | Jayachandran 2014, Appendix Table 2 (FULL-TEXT) |
| Implied Nepal | median tutoring ≈ **US$3.9/month** ≈ **4.5% of annual GDP p.c. per month**, i.e. ~23% of a month's GDP p.c. | derived arithmetic from the above |

### 6.2 Provider structure and entry
- **Cambodia**: dominant provider is the **own teacher**; 41.5% of urban primary teachers name tutoring as their out-of-school work; tutoring earnings ≈ **two-thirds of monthly base salary** (Benveniste et al. 2008 via Brehm & Silova, SECOND-HAND).
- **Korea**: Kang 2026 estimates **77%** of secondary tutoring expenditure (89% in the final year) is competition-driven; <half of self-study time. Structural counterfactual, not observed.
- **Commercial chains / franchising**: no quantitative entry or concentration data retrieved.

### 6.3 Regulation effects
- **China Double Reduction (July 2021)**: the policy content is documented, but **no credible quantitative evaluation of its effect on total household investment was retrievable** (IAFOR paper 403; CCNU survey paywalled). The manuscript's "rerouted, not disappeared" claim is **unverified**.
- **Korea**: annual official measurement exists back to 2007, so a pre/post design is possible — but no retrieved study identifies a regulation effect.
- **Cambodia**: no tutoring regulation to evaluate.

### 6.4 Price elasticity of demand for tutoring
**NOT FOUND.** This is the parameter a shadow-sector supply module most needs and the literature does not supply it. Jayachandran's model *assumes* demand is weakly decreasing in price and derives `p*(m)`; no elasticity is estimated. Brehm & Silova report fees and attendance but not a price response. Korea's survey reports expenditure, not a demand system.

### 6.5 Model mapping
- Fee levels can be **calibrated** (they are observed); **elasticities cannot** — they must be swept, with results reported as conditional.
- The teacher-tutoring share (Cambodia ~41.5% of urban primary teachers) is a *supply* parameter with a real anchor.

---

## 7. What is NOT identified — the honest gaps

Ranked by how much they constrain the experiment slate:

1. **Elasticity of formal employment to educated labour supply.** No estimate for any of our countries. Prediction 2's discriminating test rests on it. → *Identified in no source retrieved.*
2. **Price elasticity of demand for tutoring.** No estimate anywhere in the retrieved literature. → *The shadow-sector module cannot be estimated from secondary data; it can only be swept.*
3. **The causal effect of credential requirements on hiring** (as opposed to the effect of skills). Enterprise Surveys give perceptions of constraints, not requirement schedules. → *Not identified.*
4. **Formal↔informal transition hazards and the informal earnings gap** for PHL/KHM. → *Not retrieved; likely available from PSA LFS/CLFS panels but not as a published estimate.*
5. **Ability bias in the returns to schooling** — the Clark & Nielsen critique could not be read; the size of the bias is unknown in this package. → *Not verified.*
6. **The cost of non-recognition** — no estimate of what a credential's non-recognition costs a worker, by destination. → *Not found.*
7. **The Double Reduction causal effect** on household investment. → *Blocked sources; unverified.*
8. **Employer requirement vs worker holding** (the credential gap). → *Not extracted for any country.*

**What this means for the Council.** Six of the model's household/positional parameters have real anchors (returns, place premium, fees, nurse multiplier, participation rates, teacher-tutoring share). **Almost none of the economy-side parameters do** (formal-job elasticity, informality transitions, requirement schedules, tutoring elasticity). Experiments that vary the economy side are therefore *explorations of assumption space*, not tests against evidence — and should be labelled that way in the writeup.

---

## Provenance
Files archived under `02_lit/raw/` with sha256 in `SOURCES.json`: `psach_patrinos_wps8402.txt`, `clemens_montenegro_pritchett_wps4671.txt`, `abarcar_theoharides_slides.pdf`, `phl_skills.txt` (World Bank 2017 PHL skills report). Also used (already archived): `brehm_silova2014_wp39_cambodia.pdf`, `jayachandran2014_incentives_to_teach_badly.pdf`, `kang2026_parental_investment_rat_race.pdf`, `decastro_deguzman2010_kjep_philippines.pdf`.
