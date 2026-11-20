<!-- Writer: lit-archivist, 2026-11-20, task-35. Scope: literature only. No model output below.
Verification legend: VERIFIED = primary text read this session (file in 02_lit/raw/ or /tmp archive, hash noted).
STANDARD-CITATION = canonical account, primary text NOT retrieved this session; the mechanism and any
thresholds are as standardly cited in the literature, and must be checked against the original before
publication. NOT-FOUND = searched and did not find; treat as a gap, not as zero. -->
# LABOUR_MARKET_REPORTS — what the ILO/OECD/World Bank evidence actually says (and what is still missing)

**Coordination status.** Data-hunter (`deepseek-data`) has delivered: WDI/UIS/EDUNONCORE panels for six countries (`04_data/data/`), GMR/GEM country-page snapshots (`04_data/gmr_snapshots/`, with `GMR_SNAPSHOTS.md`), and complexity/WDI proxies. It has **not yet delivered** the ILO/OECD jobs-and-skills report corpus. This file therefore separates **what is in hand** from **what is requested**, rather than inventing a synthesis.

---

## 1. In hand and verified

### 1.1 World Bank Enterprise Surveys — the one jobs/skills number we actually have (VERIFIED)
World Bank (2017), *Developing Socioemotional Skills for the Philippines' Labor Market*, DOI 10.1596/978-1-4648-1191-3, **Table 2.1** (`02_lit/raw/wb2017_phl_socioemotional_skills.txt`):

| Share of firms citing **inadequate workforce skills** as a major obstacle | 2009 | 2015 |
|---|---|---|
| All firms | **7.8%** | **10.1%** |
| Manufacturing | 6.7% | 7.3% |
| Services | 8.2% | 11.0% |

**Why it matters.** ~90% of firms do **not** name skills as a major constraint, and the share moved only 2.3pp in six years. This is the single most useful jobs/skills fact for the push-pull question: it is weak evidence for a skills-shortage-driven (demand-pull) account and consistent with a screening/credential account. The same report notes the constraint concentrates among the most dynamic firms — so it is not zero, it is concentrated.

### 1.2 GMR / EFA / GEM country profiles — education-system facts (VERIFIED, via data-hunter)
`04_data/gmr_snapshots/GMR_SNAPSHOTS.md` + `raw/gmr2007/` + `txt/gmr2007/`. Key extraction for the **Philippines** (IBE/2006/EFA/GMR/CP/70, 13 pp., UIS 2002/03–2004/05, i.e. the K-10 era):
- Compulsory education age range: **6–12** (per UIS).
- ISCED 0 gross enrolment ratio **39.9 (2003/04)**; net **31.1 (2002/03)**.
- Children entering primary with previous preschool experience: **59.3 (2003/04)**.
- Age-specific enrolment ratios 2002/03: age 5 = 51.7, age 6 = 97.8.
**Caveat carried from data-hunter and repeated here:** these profiles were *commissioned as background* for the GMR and "have not been edited by the team" — cite as "IBE country profile commissioned for the EFA GMR 2007", not "the GMR says".

### 1.3 Country series on disk (for the sectoral/jobs side)
`04_data/data/`: `wdi_4countries_long.csv`, `uis_sdg4_4countries_long.csv`, `uis_edunoncore_6countries_long.csv`, `gmr_observed_6countries_1970_2024.csv`, `gmr_source_disagreements.csv`, `gmr_annual_1980_2020_imputed.csv`.
**Warning from the data itself:** `gmr_source_disagreements.csv` exists because the GMR and UIS series do not agree. The model must pick one series per indicator and record the choice, and imputed cells must never enter as observations (README binding rule).

---

## 2. Missing — requested from data-hunter (deepseek-data)
Posted to the bridge with precise table/page asks. Priority order:
1. **ILO** — *World Employment and Social Outlook (WESO)* trends series: sectoral employment shares, informal employment, youth unemployment; plus the **ILO informality statistical picture** (women/men in the informal economy) for PHL/KHM. Needed for the formal/informal margin the floor mechanism requires (flagged unusable in `02_lit/ECON_TARGETS.csv`).
2. **ILO** *Global Wage Report* — real wage growth by region; needed as the wage-side series for push-pull lead-lag.
3. **OECD** *Education at a Glance* — tertiary attainment and enrolment ratios for KOR/JPN (benchmarks), plus the **Education at a Glance** transition/returns tables.
4. **World Bank** — *World Development Report* jobs/skills material and the **STEP** skills surveys (if PHL/KHM coverage exists); plus **Enterprise Surveys** raw files for PHL/KHM (the 2023 PHL wave exists and has the constraint variables).
5. **World Bank / ILO** — sectoral productivity (value added per worker by sector) for PHL/KHM/CHN, if published as tables.

---

## 3. What the reports would have to say to change the push-pull verdict
- **ILO informality + youth unemployment**: if educated youth unemployment/informality is high and rising with expansion, that supports supply-push/overeducation (Rival B). If educated workers move into formal jobs roughly as fast as they are produced, that supports demand-led (Rival A).
- **ILO wage series**: if educated wages fall while educated employment rises, that is a supply-shift signature (B); if educated wages and employment rise together, demand-shift (A).
- **OECD attainment vs enrolment**: KOR/JPN are the *completed* universalization cases; their shape parameters are the benchmark for the six-country fits.
- **STEP/Enterprise Surveys**: whether the *requirement schedule* rose independently of job content — this is the credential-inflation measurement that currently does not exist for our countries (`02_lit/ECON_TARGETS.csv`, unusable rows).

---

## 4. Honest statement
I have synthesized **one** verified jobs/skills table (World Bank Enterprise Surveys via the 2017 PHL report) and the education-side report evidence that data-hunter captured. I have **not** read ILO WESO, ILO informality, OECD Education at a Glance, or WDR/jobs reports this session, and I will not paraphrase them from memory. Until data-hunter delivers them, any Council statement about "what the ILO reports say" is unsupported by this lit package.
