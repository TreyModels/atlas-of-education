# LITERACY × GDP × ECI — with the cohort-replacement correction

**Author:** `pattern-scout` · addendum to task-21 · 2026-11-20. Answers Dr. Menefee's question: *is the literacy–GDP–ECI correlation real, and how much of a literacy rise is just old illiterates dying?*
Everything below is observed data; scripts in `scripts/`, outputs in `data/`.

**New data pulled for this addendum**
- **ECI** — Growth Lab, Harvard Dataverse `doi:10.7910/DVN/XTAQMC` (CC0), file `growth_proj_eci_rankings.csv`, columns `eci_sitc / eci_hs92 / eci_hs12` + the Growth Lab `growth_proj`. Data dictionary archived (`raw/eci_data_dictionary.csv`). **Coverage: all 30 panel countries, 1995–2024.**
- **Literacy** — WDI `SE.ADT.LITR.ZS` (adult 15+), `SE.ADT.1524.LT.ZS` (youth 15–24), gender splits.
- **Population pyramids** — WDI `SP.POP.0014/1564/65UP.TO.ZS`, `SP.POP.TOTL`, CBR/CDR/life expectancy. **Caveat: WDI's 5-year age-band share indicators (e.g. `SP.POP.1519.TO.ZS`) are not served by API v2 — they returned "invalid value". So the pyramid is 3-band (0–14 / 15–64 / 65+), not 5-year, and the 15–24 share is proxied from the birth cohort 15 years earlier (derived, flagged).**

---

## 1. Does literacy correlate with GDP and with ECI?

Two-way FE (country+year), CR1 SE clustered on country, 1995–2024 (`data/eci_literacy_results.csv`):

| # | Test | Coefficient | SE | n | Countries | Reading |
|---|---|---|---|---|---|---|
| **E1** | log GDP pc ~ **ECI** | **0.322** | 0.098 | 895 | 30 | one ECI point ≈ **32% higher GDP pc** within country; p=0.001 |
| **E3** | **ECI** ~ log GDP pc | **0.568** | 0.145 | 895 | 30 | the reverse is just as strong — **joint determination, no direction** |
| **E2** | **ECI** ~ **adult literacy** | 0.001 | 0.005 | 274 | 28 | **no relation** (p=0.83). The literacy *stock* does not track complexity |
| **E5** | **ECI** ~ primary completion, **t−10** | **0.593** | 0.176 | 253 | 23 | the schooling **flow** does track complexity (p=0.001) |
| E6 | ECI ~ upper-secondary attainment | 0.055 | 0.173 | 418 | 30 | no relation |
| E7 | adult literacy ~ log GDP pc | 3.91 | 2.67 | 313 | 28 | income does **not** raise the literacy stock within country (p=0.14) |
| E9 | **youth literacy** ~ primary completion | **29.9** | 5.2 | 222 | 27 | 1pp more completion → **0.30pp more youth literacy** (nearly mechanical) |

**The interesting asymmetry:** within countries, **ECI tracks the school *flow* (recent completion) but not the literacy *stock***. Literacy is near-100% in most of the sample, is measured sparsely (WDI/UIS literacy series are largely survey/census-based **estimates**, often revised), and moves on a 40-year demographic lag — so it is a poor discriminator of current know-how. Completion is the better ECI correlate.

## 2. Does ECI predict growth? (the published claim)

| Test | Specification | Coefficient | SE | Reading |
|---|---|---|---|---|
| E10 | 10y cumulative growth ~ ECI, two-way FE | −0.158 | 0.101 | **no positive premium** |
| E16 | 10y growth ~ ECI + log GDP pc, **year FE only** (the canonical cross-sectional test) | **−0.068** | 0.067 | still no positive premium |
| E17 | + adult literacy added | ECI −0.059; literacy −0.001 | 0.047; 0.002 | literacy adds nothing either |
| E13 | realized 10y growth ~ Growth Lab `growth_proj` | **−0.004** | 0.020 | the Growth Lab's own projection does **not** predict realized growth in this sample |

**This is a failure to replicate, and must be stated as such.** The Growth Lab's ECI-growth premium is estimated on all countries 1962–2010; our panel is 30 Asia+comparator countries 1995–2024. Either the relation does not survive the sample/period, or our FE/annualisation is wrong. **Do not put ECI into the model as a growth driver on the basis of the literature claim alone** — the data here do not support it.

## 3. The cohort-replacement correction — "a lot of literacy gains are just old illiterates dying"

**The identity.** Adult literacy is a *stock* of cohorts:
`Lit_15+ = Σ_a (share of 15+ in age band a) × (literacy of that band)`. A rise can come from (i) young literate cohorts **entering**, (ii) old illiterate cohorts **dying**, (iii) adults actually **learning** (adult education), and (iv) survey/measurement revision.

We built the flow version (`scripts/analyze_literacy_eci.py`):
- **Entrant flow** = (births 15 years earlier ÷ population 15+) × (youth literacy − adult literacy). *Observed variables; the entrant share is derived from the birth cohort, flagged.*
- **Exit flow** = (deaths ÷ population 15+) × (adult literacy − literacy of the dying cohort). The dying cohort's literacy is **not observed**, so it is bounded: lower bound assumes the dying are as literate as the stock, upper bound assumes the earliest observed youth literacy. Both bounds reported.
- **Residual** = actual change − entrant − exit ⇒ within-cohort learning (or loss/revision).

### The headline number

| Quantity | Value |
|---|---|
| **Median replacement share of observed adult-literacy gains** | **0.62 – 0.66** (lo–hi bounds), **24 countries** with a positive change |
| Unweighted mean 5-year literacy change | **+1.73pp** |
| Of which cohort replacement (hi bound) | **+1.07pp** |
| Of which within-cohort/adult learning (residual) | **≈ +0.66pp** |
| Regression: Δliteracy ~ entrant-flow contribution | **1.655** (se 0.526, p=0.002), n=241 country-periods, 25 countries |
| … plus the youth−adult gap | entrant flow **1.635** (0.467); gap **0.318** (0.122) |

**So: roughly two-thirds of the typical measured rise in adult literacy is demographic turnover, not new learning.** Using Δliteracy as a measure of schooling effectiveness overstates the within-cohort effect by roughly 2–3×.

### Per-country (mean of 5-year periods; `data/literacy_cohort_decomposition.csv`)

| Country | Δliteracy (pp) | Replacement share (lo–hi) | Reading |
|---|---|---|---|
| IND | +1.56 | **0.81 – 1.02** | replacement fully explains it; little adult learning |
| BGD | +1.84 | 0.40 – 0.54 | mixed |
| PHL | +0.54 | 0.50 – 0.66 | two-thirds turnover |
| TUR | +1.62 | 0.51 – 0.57 | mixed |
| MEX | +0.23 | 0.75 – 0.81 | mostly turnover |
| SGP | +0.16 | 0.20 – 0.22 | universal literacy; almost nothing to replace |
| **CHN** | +12.3 (one usable period) | 0.43 – 0.59 | sparse WDI series — **gap** |
| **KHM** | +0.51 | **1.82 – 1.98** | replacement predicts *more* than observed ⇒ within-cohort loss or series revision |
| **THA** | −0.19 | negative (series falls) | revision in the census series, not a real fall |
| LAO / LKA / VNM | small | >1.2 | same anomaly |

The >1 cases are **not** evidence of mass literacy loss — they are the measurement revision problem, and they are the honest reason not to treat the residual as a clean estimate of adult learning.

### Population pyramids (`data/population_pyramids.csv`, 3-band, observed)

| Country-year | 0–14 share | 65+ share | Adult literacy | Youth−adult gap |
|---|---|---|---|---|
| PHL 1980 | 44.3 | 2.6 | 83.3 | 8.5 |
| PHL 2020 | 30.7 | 4.7 | 98.5 | 0.8 |
| KHM 2010 | 33.3 | 3.9 | — (no adult series) | — |
| CHN 1982 | 34.3 | 4.6 | 65.5 | — |
| CHN 2020 | 18.0 | 12.6 | 96.7 | 3.0 |
| IND 1981 | 39.7 | 4.0 | 40.8 | — |
| IND 2024 | 24.6 | 7.1 | 78.2 | 19.2 |

The youthful pyramid (PHL 0–14 share 44→31) is exactly the mechanism that inflates a literacy rate with zero learning; China's ageing (65+ 4.6→12.6) is the mechanism that *slows* the measured rate even as schooling expands.

## 4. What this means for the model

1. **Do not model literacy as a function of current spending or income.** R31/R34: within country, income does not move the literacy stock. Literacy is a **lagged, age-structured convolution of past completion and survival**.
2. **Add a cohort-replacement term to any attainment/literacy block.** `massabm` already has cohorts (`N`, births, the `t-16`/`t-20` pipeline); the addition is a literacy/attainment *stock* that weights past completion by cohort size and survival, not a contemporaneous production function.
3. **Report attainment/literacy by cohort, not as an aggregate rate.** R39: the aggregate rate is a population-weighted artifact of the pyramid.
4. **ECI: use the flow (completion), not the stock (literacy), if a complexity block is added** — and carry the growth-replication failure (R35/R36) as an explicit caveat.

## 5. Caveats, stated plainly

- **WDI literacy is not raw census data.** It is a UIS-compiled series built from census/survey items, interpolated and revised (the THA series actually *falls* between rounds; KHM/LAO/LKA/VNM imply impossible within-cohort losses). Treat every literacy level as **medium confidence** and every literacy *change* as noisier than the panel SEs suggest.
- **The 15+ stock is not observed at 5-year age bands** (WDI API v2 does not serve `SP.POP.1519/2024`), so the 15–24 share is proxied from the birth cohort 15 years earlier. This biases the entrant flow toward countries with good birth registration.
- **No adult literacy series at all for KOR, JPN, HKG** — the developed benchmark countries. The literacy analysis is therefore a developing-country analysis.
- **The exit component is bounded, not estimated.** The reported 0.62–0.66 replacement share is conditional on that bound.
- **ECI is export-based** and mechanically reflects trade composition; the ECI↔GDP relation cannot be given a direction from this data (E1 vs E3).
- **China's literacy series is too sparse in WDI for the decomposition** (one usable period). A census-based CHN series (1982/1990/2000/2010/2020) would close it.

## 6. Files added by this addendum

| File | Content |
|---|---|
| `data/panel_wdi_eci.csv` | 30-country panel with ECI merged (1995–2024) |
| `data/eci_literacy_results.csv` | E1–E15: ECI × GDP × literacy × growth tests |
| `data/eci_growth_crosssection.csv` | E16–E17: canonical year-FE ECI growth test |
| `data/literacy_cohort_decomposition.csv` | 241 country-periods: entrant/exit/residual decomposition |
| `data/literacy_decomposition_regressions.csv` | D1–D2 regressions on the decomposition |
| `data/population_pyramids.csv` | 3-band pyramids + literacy, 10 countries × 7 decades |
| `data/literacy_country_examples.csv` | first/last observed literacy, pop, pyramid shift |
| `scripts/analyze_literacy_eci.py` | end-to-end reproduction |
| `raw/eci_growth_proj_rankings.csv`, `raw/eci_data_dictionary.csv` | ECI source (Growth Lab, CC0) |

**Register rows added: R31–R40** (literacy×GDP, ECI×GDP, ECI×flow vs stock, ECI→growth null, growth-proj null, cohort replacement, youth-literacy production, pyramid measurement caveat, within-cohort residual).
