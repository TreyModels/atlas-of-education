# Parameter register: Guangzhou sorting model v5.1 (frozen 2026-11-27)

Sampling: each swept parameter is drawn uniformly over its range by Latin hypercube (v5-v8 sweeps). Fixed parameters use the default.
Evidentiary status: official (rules), literature (published estimates), informant (field record), assumed, unknown.

| Parameter | Definition | Range (swept) | Default | Source | Status | Dependencies |
| --- | --- | --- | --- | --- | --- | --- |
| TAL_WEALTH | Correlation of latent talent with log family wealth | 0-0.3 | 0.1 | Assumption | assumed |  |
| SEG | Residential segregation: correlation of family wealth with zone wealth | fixed | 0.6 | Assumption | assumed |  |
| HOME | Skill at 15 per SD of log wealth from home inputs | 0-0.3 | 0.15 | Assumption | assumed; key driver |  |
| TEACH_SD | SD of teacher effects (junior and senior) | 0.15-0.45 | 0.2 | Dossier: teacher effects 0.17-0.5 SD; 0.4 reproduces 8-11% within-school share | literature range | HS_TEACH_SD set equal |
| TEACH_ZONE | Junior teacher quality per SD of zone wealth | 0-0.25 | 0.1 | Assumption | assumed |  |
| DECAY | Share of pre-gate head start that fades by senior 2 | 0-0.9 | 0.5 | Unmeasured | unknown; most influential | single common stock for home, school, tutoring |
| GROW | Talent-driven learning in senior high | fixed | 0.5 | Assumption | assumed |  |
| SCHOOL_VA | School value added per tier (SD) | 0-0.5 | 0.1 | Dossier RD studies 0-0.2; widened to 0-0.5 | literature range, widened |  |
| TOP_TEACH | Teacher premium in top band (SD) | 0.2-0.4 | 0.3 | Dossier magnet-class RD 0.435 total | literature (one county) | TOP_TEACH + PEER about 0.44 |
| PEER | Peer premium in top band (SD) | 0.05-0.25 | 0.14 | Dossier magnet-class RD 0.435 total | literature (one county) | TOP_TEACH + PEER about 0.44 |
| ZHIBIAO | Share of elite seats allocated to junior schools (hukou only, minimum score) | 0.3-0.6 | 0.5 | Guangzhou 2026 admission rules, about 50% | official | ZB_FLOOR |
| ZB_FLOOR | Minimum score for zhibiao: top share of cohort | 0.2-0.4 | 0.3 | Assumption consistent with 2026 rules | assumed |  |
| NONHUKOU | Share of cohort without local hukou | 0.1-0.4 | 0.2 | Unknown | unknown; drives exclusion |  |
| QUOTA | Cap on non-hukou share of public academic seats (per tier) | 0.08-0.2 | 0.15 | Rules: 8-15% core, 8-18% outer, 8-20% from 2027 | official |  |
| MINBAN_PEN | Junior teaching penalty in minban or purchased places (SD) | 0-0.3 | 0.15 | Assumption; dossier: private VA about 0 | assumed |  |
| NH_WEALTH | Mean log-wealth gap of non-hukou families | -0.6-0 | -0.3 | Assumption | assumed |  |
| NOISE | Exam measurement noise (SD) | 0.25-0.5 | 0.35 | Assumption | assumed |  |
| ACAD | Academic-track share at zhongkao | 0.45-0.65 | 0.65 | Informant about 50%; earlier 60-70% | informant/official |  |
| PRE_SHARE | Share of families buying pre-gate tutoring with no ban (wealth-weighted) | 0.2-0.6 | 0.4 | Informant; CIEFR 36% (2017) | informant + survey |  |
| BAN_RED | Share of pre-gate tutoring removed by the 2021 ban | 0-0.6 | 0.4 | Informant: much continues as private tutors; CIEFR 36.1% to 13.5% | informant + survey |  |
| PRE_EFF | Skill gain for a pre-gate tutoring taker (SD) | 0-0.3 | 0.15 | Literature: mixed, 0 to about 0.15 | literature range |  |
| REBAND_PERF | Weight of senior-1 performance in senior-2 placement | 0-0.5 | 0.3 | Informant: often by subject, but class 16 to class 1 possible | informant | composite rank keeps band size fixed |
| TERM_SHARE | Share of academic pupils tutoring in term when boarding (both tails); x3 without boarding | 0.02-0.15 | 0.1 | Author observation (about none) and informant | informant |  |
| HOL_SHARE | Share of academic pupils tutoring in holidays (both tails, wealth-weighted) | 0.2-0.6 | 0.4 | Informant: summer pre-learning, winter except 3 days | informant |  |
| POST_EFF | Gaokao gain per term or holiday tutoring episode (SD) | 0-0.2 | 0.1 | Literature mixed; meta-analysis near zero | literature range |  |
| FT_SHARE | Share of cohort in full-time institution study (keeps school place) | 0-0.05 | 0.03 | Informant about 5% (denominator unconfirmed) | informant |  |
| FT_EFF | Gaokao effect of full-time study vs staying in school classes (SD) | -0.2-0.3 | 0.0 | Unknown sign | unknown | loses in-school class effects |
| INSURE | Take-up rise with wealth rank minus achievement rank | 0-2 | 1.0 | Behavioural approximation of N3 | assumed |  |
| RHO_DEMAND | Take-up rise with classmates lagged take-up | 0-1 | 0.5 | Behavioural approximation of N3 | assumed |  |
| ART_SHARE | Share of cohort on the art-exam route (wealth-weighted, weaker academically) | 0-0.06 | 0.04 | Informant | informant |  |
| ART_BONUS | Additive advantage of the art route (SD), single-ranking approximation of N4 | 0.3-1.2 | 0.8 | Informant: specialist exam easy | assumed |  |
| HK_SHARE | Share sitting the joint exam as Hong Kong/Macau/Taiwan residents (wealth top 30%) | 0-0.02 | 0.01 | Informant | informant |  |
| HK_BONUS | Additive advantage of the joint-exam route (SD), approximation of N4 | 0.5-1.5 | 1.0 | Informant: much easier entry | assumed |  |

Fixed structural parameters: n=60000, N_JUNIOR=300, JR_CLASSES=6, ELITE=0.1, N_HS=60, HS_CLASS=50, TOP_BAND=0.125, PRIVATE_COST=75000, AFFORD=0.4, MED_INCOME=200000, N_PRIV=12, BOARD=True, FT_COST=140000. ELITE = top-decile proxy; FT_COST 140,000 yuan/yr (informant: small class 60-80k/semester); MED_INCOME 200,000 (dossier); PRIVATE_COST 75,000 (dossier).
