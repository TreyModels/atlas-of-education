> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# SYNTHESIS 007 — country-evidence-driven experiment slate (iteration 5)

**Headline.** Seven experiments, all changing a structural variable and all anchored in data now on disk. The slate is
led by a **gate-architecture gradient test** (KOR falling vs HKG rising stage profiles), which is the only design that
can explain the loop-4 U1 ordering failure and the HKG shape-pass/level-fail at once. The provider-technology/fee
block is second; Japan's within-country prefecture range is the cleanest identification but a narrower claim. The
`09_relations` layer is **PENDING** (empty at intake): every experiment carries a relation slot PENDING and a
design-intent grade; none is invented.

## 1. What each country profile actually supports

| Country | Evidence quality | Role in iteration 5 | Assumptions that remain |
|---|---|---|---|
| **KOR** | HIGH official (MODS/KEDI 2023): 86.0/75.4/66.4 rates; 434/553k won spend; provider spend 241/37/22/16; income gradient 183 vs 671k | **Calibration/identification anchor** (fees, provider form, stage ordering) | provider cost/wage scaling; no hours object; 2011 "90%" not traceable |
| **HKG** | 2003 peer-reviewed anchor (35.1/46.6/70.3; mass-lecture 72.4% S6-7; fees 1.1–5% income); 1996/2010 LOW | **Check/OOS** (stage gradient, provider ordering, fees) | 2010 85% is the single calibration moment; second-hand/caveated |
| **JPN** | HIGH grade-6 prefecture mean 41.8 (22.1–57.9); MEDIUM 2007 national (26/53) | **Within-country identification** (density/competition) | fee series unresolved (MEXT/e-Stat blocked) |
| **CHN** | MEDIUM 2014 (29.8%, abstract-level); LOW post-2021 (headline inequality) | **Bounded prior / scenario** | no provider split; no post-2021 rate; zhongkao/gaokao typology |
| **KHM** | Case study (one district, six schools, 444 students): G6 60.5 urban/26.4 rural; G9 52/39; Rien Kuo; fees 500–1,000 Riel/session | **Mechanism demonstration** (teacher-sold supply), case scope only | non-national; one district |
| **PHL** | Incidence BLOCKED (PSA 403); one 2010 select sample (46.5 all-basic) | **Data-first / demonstration** | no national rate; cohort/economy targets exist (UIS 2024) |

**Mechanism evidence summary:** gate architecture — KOR (CSAT stage; declining by level), HKG (terminal HKDSE; rising
by stage), CHN (zhongkao/gaokao rank-quota), JPN (high-school entrance gate) are all documented in the cards;
provider form — KOR hagwon spend dominance, HKG commercial mass lectures at senior, KHM teacher-sold, JPN juku; fees —
KOR/HKG/KHM have moments, JPN/CHN/PHL do not; income gradient — KOR bands and HK income share exist.

## 2. The slate (7 experiments)

**E1. Gate-architecture gradient (KOR vs HKG).** *Country/stage:* KOR all levels; HKG S1-3/S4-5/S6-7. *Structural
variable:* where the binding high-stakes gate sits (single terminal gate vs multiple transition gates). *Mechanism:*
households buy tutoring in proportion to the stakes of the *binding* gate; a single terminal exam concentrates demand
at the top of the system (HKG rising 35.1→46.6→70.3), while gates at every transition plus a broader exam footprint
flatten or invert the profile (KOR falling 86.0→75.4→66.4). *Data:* KOR MODS/KEDI 2023 Table 2 (on disk);
HKG Bray & Kwok 2003 Table 1 (on disk); gate dates from country cards. *Arms:* (a) terminal-only gate, (b) gate each
transition, (c) continuous curriculum gate. *Estimand:* six stage take-up rates (two gradients). *Threshold:*
predeclared — all six within ±5 pp, with gate parameters set from policy dates and no take-up fitting; else FAIL.
*Cost:* ~30–45 min. *Type:* identification (plausibly-causal). *Relation slot:* PENDING (09_relations); design-intent
plausibly-causal.

**E2. Provider technology and fee block (KOR + HKG).** *Country/stage:* KOR all levels; HKG S1-3/S4-5/S6-7.
*Structural variable:* provider production (mass-lecture scale economies vs one-to-one vs teacher-sold) with fixed
cost, capacity and class-size/quality dilution. *Mechanism:* exam-oriented mass lectures are cheap per pupil and
dominant where a terminal exam and dense demand exist; 1:1 is income-elastic; teacher-sold arises where teachers can
sell the curriculum. *Data:* KOR provider spend mix 241/37/22/16 and per-participant fees 462/596/740k (on disk);
HKG mass-lecture 72.4%/33.0%, fee distribution, income share (on disk). *Arms:* mass-lecture-dominant vs 1:1-dominant
vs mixed. *Estimand:* provider spend shares; commercial share by stage; fee/income ratios. *Threshold:* KOR spend
shares within ±10 pp; HKG S6-7 commercial gap ≥20 pp; fee/income inside 1.1–5.0%. *Cost:* ~45–60 min. *Type:*
identification/description. *Relation slot:* PENDING; plausibly-causal.

**E3. Japan within-country density/competition.** *Country/stage:* JPN grade 6, 47 prefectures. *Structural
variable:* local market density and competition (provider entry, urbanisation) rather than fitted take-up.
*Mechanism:* dense urban markets lower tutoring search/transport costs and raise competitive stakes → higher
participation. *Data:* Rappleye & Komatsu 2020 Table 2 (mean 41.8; range 22.1–57.9); prefecture urbanisation from
`ECONOMY_SERIES.csv`/WDI (covered). *Arms:* density channel vs income channel vs both. *Estimand:* prefecture-level
take-up spread and mean. *Threshold:* model range covers 22.1–57.9 with mean within ±5 pp, no prefecture-level
fitting. *Cost:* ~30 min. *Type:* identification (plausibly-causal, within-country). *Relation slot:* PENDING.

**E4. Income gradient of tutoring demand.** *Country/stage:* KOR (income bands) + HKG income share. *Structural
variable:* demand motive — positional (rank) vs consumption/human-capital — with liquidity. *Mechanism:* positional
demand predicts spend rising steeply with income and saturating at the top; consumption predicts flatter gradients.
*Data:* KOR 183k (<3m won) vs 671k (≥8m won) monthly per student (on disk); HKG fees 1.1–5.0% of income (on disk).
*Arms:* positional utility vs human-capital utility (same households). *Estimand:* spend gradient across income bands;
fee/income share. *Threshold:* KOR gradient ~3.67× within ±20%; HKG share in 1.1–5.0%. *Cost:* ~30 min. *Type:*
identification (correlational-to-plausibly-causal). *Relation slot:* PENDING.

**E5. Teacher-tutor channel (KHM, case scope).** *Country/stage:* KHM grade 6 and grade 9. *Structural variable:*
teacher supply of tutoring (teacher time allocation, in-school sale, low fees). *Mechanism:* public teachers sell the
curriculum back to their own students in school buildings; the urban–rural gap follows teacher availability and fee
levels. *Data:* Brehm & Silova case (G6 60.5/26.4; G9 52/39; fees 500–1,000 Riel/session) — case-study scope only.
*Arms:* teacher-sold channel on vs off × fee schedule. *Estimand:* urban–rural gap and provider share. *Threshold:*
gap direction and teacher dominance reproduced at case scope; explicitly not national. *Cost:* ~40 min. *Type:*
mechanism demonstration. *Relation slot:* PENDING; plausibly-causal (case).

**E6. Cohort-ledger long-run collapse diagnosis.** *Country/stage:* PHL, KHM (+HKG/CHN ledger). *Structural
variable:* degree-share/education–economy feedback structure (the new ledger collapses). *Mechanism:* if tertiary
expansion feeds back negatively (credential devaluation without job creation), long-run degree shares can collapse;
if it is a coding artifact, the feedback equation is wrong. *Data:* `05_experiments/loop2/cohort_ledger_annual.csv`,
`findings_ledger.txt`, `balance_checks.csv` (on disk; balances pass exactly). *Arms:* current feedback vs
devaluation vs no-feedback. *Estimand:* 40-year degree/upper-secondary paths. *Threshold:* no collapse (degree share >0;
upper-sec not below start −10 pp) or a documented defect; if collapse persists under all arms, it is a finding about
the feedback, not a bug. *Cost:* ~20–30 min. *Type:* description/validation. *Relation slot:* PENDING.

**E7. China Double Reduction bound (scenario).** *Country/stage:* CHN all levels. *Structural variable:* enforcement
intensity + school-support substitutability + informal-market leak. *Mechanism:* a ban pushes demand off-campus; school
support substitutes only if it damps tutoring's marginal value. *Data:* 2014 29.8% (medium, Liu & Bray 2020);
post-2021 ">80% did not attend" (LOW, headline only) — used as a bound, never a rate. *Arms:* additive vs substitutive
support × enforcement 0.5/1.0. *Estimand:* post-policy participation bound. *Threshold:* post-ban participation below
20% only under full enforcement + substitution; otherwise report the bound and no policy claim. *Cost:* ~25 min.
*Type:* forecast/scenario. *Relation slot:* PENDING; correlational at best.

## 3. Ranking — identification value × feasibility

| Rank | Experiment | Identification value | Feasibility | Type |
|---|---|---|---|---|
| 1 | E1 gate-architecture gradient | highest — tests the paper's core mechanism; resolves the U1 contradiction | high — data on disk, one structural variable | identification (plausibly-causal) |
| 2 | E2 provider technology/fee | high — explains both loop-4 OOS failures | high — data on disk; 45–60 min | identification/description |
| 3 | E3 JPN within-country | high (cleanest design) but narrower claim | high — data on disk | identification |
| 4 | E4 income gradient | medium-high — identifies demand motive | high | identification |
| 5 | E5 KHM teacher-tutor | medium — mechanism, case scope | high but non-national | demonstration |
| 6 | E6 cohort-collapse diagnosis | low as identification; guards against a catastrophic artifact | high — artifacts on disk | description/validation |
| 7 | E7 China bound | low (weak data) | high compute, low data | scenario |

## 4. Data-first list (profiles imply, data cannot support yet)

1. **PHL national tutoring incidence** — PSA FIES/APIS/LFS microdata (403; credentialed); PIDS; DepEd exit-assessment
   documentation. *New data needed.*
2. **CHN post-2021 rate + provider split** — CFPS/CEPS application; MOE monitoring survey. *New data needed.*
3. **JPN fee series** — MEXT 子供の学習費調査; e-Stat API (application ID). *New data needed.*
4. **KOR 2011 "90%"** — KOSIS/KEDI release (not traceable this round). *New data needed or drop.*
5. **HKG robust 1996/2010 surveys** — authors' caveat stands; a re-weightable survey needed. *New data needed.*
6. **KHM national tutoring module** — CSES/CLFS-style module; otherwise case-study scope only. *New data needed.*
7. **PH cohort/transition and overseas-deployment series** — TARGETS_FLOW proxies only; EMIS/DMW series needed.
8. **Wage premium by education, all countries** — unresolved in TARGETS; would identify the returns channel.
9. **Relation layer (`09_relations`)** — PENDING; once `RELATION_CANDIDATES.csv` lands, every experiment above inherits
   its identification grade and the slate re-ranks.

## 5. The ONE experiment if only one were possible

**E1, the gate-architecture gradient.** It is the only design that uses data already on disk (KOR official 2023 by
level; HKG 2003 by stage) to test the paper's central claim — that demand follows the binding gate — against a
predeclared prediction that simultaneously explains the Korean *fall*, the Hong Kong *rise* and the loop-4 U1
ordering failure. It is one structural variable, ~30–45 minutes, and its failure would be decisive: if a gate
architecture calibrated from policy dates cannot produce both gradients, the programme should drop the gate-position
story rather than re-fit it. It is also the necessary bridge back from the stop-rule event to a *conditional*,
cross-country claim, without re-tuning the failed incidence model.

**Pending layers:** loop-4 U4 verdict; `09_relations` relation layer; WB-econ snapshot and economic-literature pull
(if they land, re-rank E4/E6 and the China scenario). Files: `brief_007/{BRIEF.md, EXPERTS.json, REVIEWS/,
COUNCIL_DELIBERATION_007.md, SYNTHESIS_007.md}`.
