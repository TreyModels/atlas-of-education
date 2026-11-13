# When children leave school: dropout and child labour across Asia

Research note and Monte Carlo results, 5 November 2026. Data: `engine/data/asia_school_work.json`. Model: `engine/childworld.py`. Experiments: `engine/childworld_mc.py` → `engine/results/childworld_mc_v1.md`, `_v2.md`; age-aligned survey tests: `engine/childworld_agealigned.py` → `engine/results/childworld_agealigned.md`.

## The question

Aggregate statistics treat "dropout" and "child labour" as one problem. They are not. Children aged 6–17 are in one of four states:

| State | Meaning |
|---|---|
| A, school | in school, not working |
| B, both | in school and working (time, fatigue, learning costs) |
| C, work | out of school, working |
| D, neither | out of school and not in market work: domestic care, marriage, disability, displacement, inaccessible school, disengagement |

Globally, 31% of children aged 5–14 in child labour are out of school, against 8% of other children (ILO–UNICEF 2024 estimates). In Asia-Pacific, 42% of child labourers are out of school, rising to 71% at ages 15–17. Of Asia-Pacific child labour, 46% is in agriculture (ILO, Asia-Pacific brief, Jan 2026).

## The country pattern

Lower-secondary out-of-school (UIS via WDI, register-based) against child labour (ILO/UNICEF, % of 5–17). Thresholds: 10% and 5%.

| Pattern | Countries (OOS / CL, %) | What the evidence says is going on |
|---|---|---|
| **High dropout + high child labour** | Laos 30.5 / 21.9; Ethiopia 47.1 / 18.7; Cambodia 14.7 / 10.4; Myanmar 21.0 / 8.1; Bangladesh 33.1 / 7.0; Pakistan 30.0 / 6.8 | Poverty and opportunity cost, plus local labour demand (farms, garments, migration). Bangladesh: 68% of rural boys aged 14–17 who dropped out were working; child marriage pulls girls out (51% of women in their mid-20s married before 18). |
| **High dropout, little child labour** | Indonesia 16.3 / 1.7; India 15.1 / 1.0; Bhutan 12.0 / 1.7; Philippines 10.5 / 1.2; Malaysia 12.1 / n.a. | Exit into state D. India (PLFS 2018/19): 4.8% of 6–17s were neither in school nor working, against 1.8% working only; girls do 134 minutes a day of unpaid domestic work, against 79 for boys. Philippines (PSA 2022): reasons for not attending were finished schooling 21%, employment 20%, lack of interest 13%, marriage 11%, cost 10%. |
| **Child labour, little dropout** | Kyrgyzstan 0.5 / 18.0; Uzbekistan 1.2 / 17.8; Nepal 2.6 / 19.2 | Work around school. Kyrgyzstan: 34% of 5–14s work, 94.7% attend, and 38.4% of 7–14s combine both (cotton, tobacco, herding). |
| **Low on both** | Sri Lanka 0.1 / 0.8; Japan; Korea 4.9 / 0 | Universal secondary; little child-labour demand. |

Caveats:
- Rows mix years (Nepal's child labour figure is from 2014).
- The out-of-school series is register-based, which can be twice the survey figure (Cambodia: `docs/cambodia_observation_equation.md`).
- Child-labour definitions differ across national surveys.

## What the Monte Carlo shows

20,000 simulated worlds, each with 2,000 children over eight years. Ten structural parameters are drawn from wide priors: income, child wage, family farm or business, how well work fits around school, value of school and its decline by level, school cost, the value of state D, girls' care and marriage pull, and the hazardous share. Seed noise is small next to the differences between patterns: about 1 point on out-of-school rates and 0.6 points on child labour.

**What separates the patterns.** AUC measures how well each parameter tells one pattern from the rest: 0.5 means no separation, 1.0 perfect.
- **Dropout + child labour** is a poverty pattern. Income is low (AUC 0.23, i.e. low income separates it strongly).
- **Dropout without child labour** is driven by the value of state D (AUC 0.89), at higher incomes (0.70). Children leave school not because work pulls them but because school is not worth staying for, compared with care, marriage or disengagement. In these worlds 99% of out-of-school children are in state D.
- **Child labour without dropout** needs schooling that stays valuable (value decline by level, AUC 0.73) and work that fits around it (0.68). In these worlds 94% of child labourers are still in school.

**What each country's two numbers imply** (worlds within tolerance; medians):

| Country | Out-of-school in D | Child labourers in school | Work fits school | Value of D |
|---|---:|---:|---:|---:|
| Bangladesh, Pakistan | 85% | 67–69% | 0.29–0.30 | 1.2–1.3 |
| Indonesia, India, Philippines | 95–97% | 65–78% | 0.10–0.18 | 1.6–2.2 |
| Laos, Cambodia, Mongolia | 28–36% | 46–55% | 0.21–0.45 | about 0 |
| Kyrgyzstan, Uzbekistan, Nepal | 6–14% | 97–98% | 0.79–0.80 | about 0 |

## Tests against survey compositions (not used in the matching)

### First round (5 Nov 2026, matched on register data, tested on a survey of different age bands)

| Country | Observed | Predicted | Result |
|---|---|---|---|
| Kyrgyzstan | 38.4% of 7–14s combine work and school | 42% [36–49] | pass (both prior sets) |
| India | 73% of out-of-school 6–17s are in state D | 96–97% [92–99] | fail (both prior sets) |
| Bangladesh | 68% of out-of-school rural boys 14–17 working | 42–54% [8–90] | passes but uninformative |

These two country tests mixed sources and age bands, so the verdicts above are superseded for India and Kyrgyzstan by the age-aligned round. The first-round India "explanation" (register vs survey out-of-school) is kept as history: it was a reasonable guess, but it was never tested on matching data from one survey.

### Age-aligned round (5 Nov 2026, third pass): `engine/childworld_agealigned.py` → `engine/results/childworld_agealigned.md`

Matching targets and test targets now come from one survey on the same age bands (100,000 worlds from the v1 priors; v2 changes only the hazardous share, which none of these quantities use).

**India, PLFS 2018/19** (UNICEF Innocenti 2024, Table 7, p. 34; economic activity only, chores excluded):

| Age | School only | School and work | Work only | Neither | Out of school |
|---|---:|---:|---:|---:|---:|
| 6–17 | 93.0 | 0.4 | 1.8 | 4.8 | 6.6 |
| 7–14 | 96.4 | 0.2 | 0.5 | 2.9 | 3.4 |
| 15–17 | 82.4 | 0.9 | 5.7 | 10.9 | 16.6 |

1. *Match on out-of-school at 7–14 (3.4%) and 15–17 (16.6%).* 808 worlds kept. The model **fails** on school-and-work: it predicts 31% of 6–17s combining school and work [8–68] against 0.4% observed. The out-of-school composition is not constrained (neither-share 8% [0–70] against 73%; it passes at 15–17 only because the range is 72 points wide). Out-of-school alone does not identify India: most worlds with India's low dropout have a lot of overlap, because work that fits around school is common in the priors.
2. *Add school-and-work (0.4%) as a third target.* Only 26% of prior worlds are that low, and at the tolerances used in specification 1 just 1 of 100,000 worlds reaches all three targets. At 2× tolerance 24 worlds do; at 3× 110. At 3× the neither-share of the out-of-school is 70% [7–94] against 73% observed, and the same at 7–14 and 15–17. That is a **weak pass**: the range spans 87 points, so it would pass almost any composition.
3. *What must be true* in those 110 worlds: low child wage (0.16), work that fits poorly around school (0.06 on a 0–1 scale, 90% range 0.01–0.23), high value of school, income above the middle. In other words India's pattern needs the model's "work around school" channel almost shut, and then the composition follows from the shut channel rather than from anything that was tested.

*Reading.* The earlier "India fails because of register vs survey data" story is **not** the whole story. With survey inputs on matching age bands, the model's specific failure is that it generates too much school-and-work for a country with low dropout, so India sits in a corner of the parameter space (0.1% of draws) the model reaches only with the overlap channel closed. A rival structure should be tried where work and school compete for a fixed time budget (the hours margin, TODO §10), which would make low overlap the default rather than a corner.

**Kyrgyzstan, MICS6 2018** (UNICEF snapshots; out-of-school by level: primary 1.0%, lower secondary 1.4%, upper secondary 11.4%): 228 worlds kept. Predicted school-and-work among 7–14s is 38% [9–71]. The DOL's 38.4% sits at the median, but the range is so wide the data do not discriminate: **the first-round "pass" (42% [36–49]) came from matching on the 18.0% child-labour figure, which MICS6 does not contain, and should not be cited.** Predicted child labour on the model's economic definition is 16% [3.5–34] against 26.7% for MICS (5–17), which also counts 28+ hours of household chores and hazardous conditions, so 26.7 is an upper bound for the model's quantity and no point test is possible.

**Unresolved (kept in `engine/data/asia_school_work.json`, `age_aligned.unresolved`):**
- The 38.4% "combining work and school, age 7–14" (US DOL, citing ILO analysis of MICS6) has no definition on the page that gives it. Its denominator and work concept are unconfirmed.
- The Kyrgyz MICS tables PR3.x (child labour by age and by attendance) were not retrievable. The snapshot shows the split only in unlabelled bars (about 27% of attenders, 22% of non-attenders), which was not used.
- The Kyrgyz school-level age bands follow the national system (grades 1–4, 5–9, 10–11), not the model's 6–11, 12–14, 15–17.
- MICS child labour is 26.7% (5–17); the 18.0% used in the first round came from a secondary page and is not in MICS6.
- PLFS: whether "school and work" is measured on principal status only (which would undercount student workers) is unchecked. The report itself warns activity status is inconsistent across surveys (the 2011/12 EUS gives 10.7% out of school and 0.6% school-and-work). PLFS 2023–24 has only a secondary-source count of 14–18-year-olds not attending (20.07 million).
- The India PLFS microdata (variable `b4q11_per_rv`, "Status of Current Attendance in Educational Institution", 265,925 person records in 2018/19) could not be tabulated from the cloud sandbox; it would settle the principal-status question.

## What to model next

1. **Survey-based inputs for every country** (MICS, DHS, LFS, PLFS) on one age definition. Done for India (Innocenti Table 7) and partly for Kyrgyzstan (out-of-school by level only); the UIS register figures stay as labelled diagnostics. Next: the Kyrgyz MICS6 PR3 tables, the PLFS principal-status check, then Bangladesh.
   - **Rival structure to try next:** a fixed time budget shared by school and work (the hours margin), so low overlap is the default. The age-aligned India test says the present structure reaches India only with the work-around-school channel almost shut.
2. **Split state D** into domestic care, marriage, disability or access, and idleness, as the memo proposes. The surveys give the reasons (Philippines, India), so the split can be tested.
3. **Education ↔ labour market:** let the value of school respond to graduates' outcomes, closing the loop with the China and Cambodia labour-market models (household–schooling loop and education–employment loop).
4. **Case studies:** Thailand (stateless children: institutional exclusion), Vietnam (ethnic-minority upper secondary), Nepal (migration and grade-10 exit) and Myanmar (conflict). Each is a different route into state D.

## Sources

- ILO, *Child labour in Asia and the Pacific* technical brief (Jan 2026): https://www.ilo.org/sites/default/files/2026-01/Child%20Labour%20Brief%20-%20Asia-Pacific.pdf
- Child labour rates by country (ILO/UNICEF estimates as tabulated): https://en.wikipedia.org/wiki/List_of_countries_by_child_labour_rate
- Adolescents out of school, % of lower-secondary age (UIS via WDI): https://www.indexmundi.com/facts/indicators/SE.SEC.UNER.LO.ZS/rankings/asia
- UNICEF Innocenti, *Child Labour and Schooling in India: A reappraisal* (July 2024; Table 7 and overall activity-status table): https://www.unicef.org/innocenti/media/9356/file/UNICEF-Innocenti-Child-labour-schooling-India-Report-2024.pdf
- UNICEF Kyrgyzstan, MICS6 2018 statistical snapshots: https://www.unicef.org/kyrgyzstan/media/6066/file/MICSStatisticalSnapshots.pdf
- US DOL ILAB, Kyrgyz Republic 2020 findings (Table 1, source ILO analysis of MICS6): https://www.dol.gov/sites/dolgov/files/ILAB/child_labor_reports/tda2020/Kyrgyz-Republic.pdf
- UNICEF Innocenti, *Leveraging Education to End Child Labour: Lessons from India and Bangladesh* (2024): https://www.unicef.org/innocenti/media/9371/file/UNICEF-Innocenti-Leveraging-Education_Child-Labour-2024-report.pdf
- US DOL ILAB, Kyrgyz Republic findings (2024): https://www.dol.gov/sites/dolgov/files/ILAB/child_labor_reports/tda2024/Kyrgyz-Republic.pdf
- PSA 2022 APIS via Philstar: https://philstar.com/headlines/2023/09/26/2299033/186-percent-ages-5-24-not-attending-school-last-year-psa
- Pakistan out-of-school (PES 2021–22; Census 2023): https://stateofchildren.com/education-in-pakistan/out-of-school-children-in-pakistan
