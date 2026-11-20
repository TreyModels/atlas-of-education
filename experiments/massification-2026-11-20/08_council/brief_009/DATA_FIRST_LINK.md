> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# DATA-FIRST LINK — which measured parameter collapses the family space most

Ranked by **collapse power** (how many of the seven assumption families become non-viable or uniquely supported if
the parameter is measured) relative to acquisition cost. Parameter ids refer to `SYNTHETIC_PARAMS.csv`; relation ids
to `09_relations/RELATION_CANDIDATES.csv`.

## 1. Credential requirement share in hiring (P17; employer side) — **rank 1**

**Why it collapses the space.** P17 is the only parameter that determines whether the formal queue is *rationed by
credentials* at all. With a measured P17 high (>0.5 of vacancies), F1 (HC, requirement 0.25) becomes non-viable and
F2/F6/F7 (0.60–0.65) gain support; with P17 low (<0.3), F2/F6 become non-viable and F1/F3 gain support. No other
single parameter separates this many families (F2, F3, F6, F7 are all defined by it). It also anchors the model's
gate module, which currently has **no empirical requirement schedule** (ECON_LIT §3.2: "not found").
**Access route:** World Bank Enterprise Surveys credential/education questions (country microdata, credentialed;
PHL 2023 ES exists; the ES API returned HTTP 000 this session) + establishment censuses (national statistical
offices). **Cost:** 2–6 weeks (credentialed request); no clean existing series.
**What it would reopen:** the credential-rationing vs human-capital distinction; the formal-access conditional's
scope; and the family assignment for PHL/KHM.

## 2. Education→formal-job elasticity (P18) vs the R13 negative-growth evidence — **rank 2**

**Why it collapses.** P18 decides whether F1/F4 (elasticity 0.35–0.50, schooling creates jobs) or F2/F3/F7
(0.05–0.10, jobs are fixed or negative) are coherent with the economy side. R13's panel estimate is **negative**
(tertiary GER t−15: −1.035, se 0.240), which already contradicts the model's `eps_ec > 0` prior; F7 exists to run
that arm. Measuring the formal-job elasticity (or a credible education→growth estimate net of reverse causality)
would eliminate half the families.
**Access route:** two-wave LFS panels + establishment/firm censuses by region and cohort schooling; ILOSTAT
public-sector tables. **Cost:** months (panel access), weeks for establishment censuses.
**What it would reopen:** the two-way feedback claim (currently asymmetric) and the family assignment.

## 3. Returns/premium table by education (P13/P14; R04/R05) — **rank 3**

**Why it collapses.** Returns determine F6 (compressed 5.0% → positional defence) vs F1/F2 (8.8%). The world/EAP
benchmark (8.8/8.7) is literature-grounded, but **country-specific Mincer tables were not extracted** (WPS8402 annex
exists; not read). A country table would fix P13/P14 and either support or retire F6.
**Access route:** extract the WPS8402 annex country tables (cheap), then ILO/ILOSTAT or national LFS microdata for
PHL/KHM/CHN/KOR. **Cost:** days (annex) to weeks (microdata).
**What it would reopen:** the saturation/positional family and the demand-motive interpretation.

## 4. Provider entry costs (P07/P08) and provider counts — **rank 4**

**Why it collapses.** F3 (teacher-sold, entry cost low, teacher capacity high) vs F1/F2/F5/F6 (commercial) hinge on
entry costs and provider counts; E2 showed the fee block cannot price itself (fees 1.5–4.2× teacher-time-plus-entry
cost), so rents/brand/marketing are the missing object. Measuring entry costs and provider counts would decide
whether commercial mass-lecture is a supply technology or a rent-extraction regime.
**Access route:** business registration/establishment censuses, KOR/HKG education-office provider registers; KHM
MoEYS school-level data. **Cost:** 1–4 weeks.
**What it would reopen:** provider technology as a channel (currently "not identified").

## 5. Teacher-tutor capacity and opportunity cost (P09/P10; R10/R24) — **rank 5**

**Why it collapses.** F3 is the only teacher-sold family; its parameters are assumed except for the KHM case-study
anchor (teacher US$44/mo; tutoring US$80–100/mo; 41.5% of urban primary teachers tutor). A teacher-level survey
(fraction tutoring, hours, earnings) would set P09/P10 and test the Rien Kuo mechanism.
**Access route:** KHM MoEYS/teacher survey; Nepal-type household surveys; ILOSTAT teacher pay. **Cost:** 2–6 weeks.
**What it would reopen:** the KHM grade-9 mechanism and the teacher-sold family.

## 6. Capacity-binding flag (P33; typology switch) — **rank 6**

**Why it collapses.** F1/F5/F6 (capacity not binding) vs F2/F3/F4/F7 (binding) is the scout's one-flag typology. The
flag is computable from **observed 1985–2000 means** already on disk (GDP pc, tax/GDP, 1990 secondary GER, urban
share; thresholds US$1,706 / 13.1% / 47.3% / 40.2%) — so it is the **cheapest** calibration step, even though its
collapse power is lower than P17/P18 because it is a switch rather than a continuous parameter.
**Access route:** already available (`09_relations/data/country_typology.csv` + WDI). **Cost:** hours.
**What it would reopen:** the country-type family assignment; it does not reopen any causal claim.

## Answer to the question

**If only one assumed parameter is measured, measure the credential requirement share in hiring (P17).** It separates
the largest number of families (4 of 7), it anchors the model's gate module — which currently has no empirical
requirement schedule — and it is the only *employer-side* parameter in the space. The runner's synthetic frontier
should therefore be read as a **two-dimensional conditional family map**: credential requirement (high/low) ×
capacity-binding (yes/no), with P18 and P13 as the next two axes. Acquisition route: WB Enterprise Surveys
credential module + establishment censuses; 2–6 weeks; no clean existing series in the package.
