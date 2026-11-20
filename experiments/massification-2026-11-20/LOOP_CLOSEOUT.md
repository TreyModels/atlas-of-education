# Loop close-out — 20 November 2026

> **Status: CLOSED.** The research loop has established its own identification limits. This is the final
> adjudication (Council brief 008), superseding the interim reports. Nothing below is a claim about the
> world; it is a claim about this model class and this evidence base.

## 1. What the programme built

A fleet-executed research loop around *Massification and Its Mechanisms* (Menefee & Nordtveit, Oct 2026):
a reproduction audit of the delivered Triad/Massabm models; a literature and model-extraction ledger
(20 core sources, 68-claim register); a sourced six-country data and target layer (WDI/UIS/national,
with a documented-imputation panel); 30+ predeclared experiment cells across six iterations; two
synthetic expert-council cycles per round; an economic-literature and WB-snapshot parameter layer; and
this negative/identification map.

## 2. What it found

- **The mechanism suite reproduces its stored tables** (floor/race 6-arm, graduate supply, gate
  tutoring, actor knockouts, floorworld screen) and the Phase-0 cohort ledger conserves people, money
  and jobs exactly (B1/B2/B3 = 0).
- **Observational equivalence is the headline.** On available national aggregates, the leading accounts
  — surplus/relational-floor versus competitive human capital, and demand-led versus education-led growth
  — are **not distinguishable**: they fit the same six moments equally well (C1 distances 0.012–0.023),
  recovery is 0.50 with forced-identification 0.30–0.50 (U2), and a truth *outside* the candidate set is
  confidently mis-assigned (2/2).
- **Five claim classes are excluded by predeclared tests:**
  1. Gate architecture (where the binding gate sits) — fails all six stage rates (E1: 20–59 pp misses).
  2. Provider technology as *the* missing channel — fails thresholds and reverses sign across defensible
     priors (E2: 3/36 parameterisations; HKG −55.3 pp at prior but 33/36 grid cells pass).
  3. Cross-country shadow-education incidence — not identifiable with public targets (loop-3 S1 3/3
     outside; Korean no-fit benchmark fails by 43–58 pp).
  4. Mechanism classification from national aggregates (C1/U2).
  5. Country completion forecasting — Philippine held-out MAE 14.68 pp versus 5.70 pp naive.
- **The two-way economy is asymmetric.** Freezing schooling still lets complex vacancies rise; schooling
  adds only 3–4% of jobs. Freezing the economy leaves attainment rising ~20–40% less than live (upper
  bound). Economy→education is a model; education→economy is largely a supplied schedule.
- **What survives as positives, narrowly:**
  - A **negative/identification map** (the deliverable);
  - a **measurement programme** (six country cards, 21-row shadow-target register, target sets, parameter
    observability map: 8 of 28 model quantities observable, 10 not);
  - a **Korean provider/fee descriptive block** (fee/GDP-pc 13.5% vs 13.8% observed; fee/income 3.56%
    inside 1.1–5.0%; fees are 1.5–4.2× cost-plus — rents, not teacher time);
  - a **weak income-gradient regularity** (2.14 vs 3.67 observed; inside a ±50% band);
  - a **not-rejected Japanese density channel** with n = 2 (density elasticity 0.226 in band; income and
    gate-stakes channels fail).
- **Eight of nine predeclared stop rules fired.** The rule that ended the central claims was written
  before the results that fired it. That is the programme's methodological success. The one rule that did
  not fire — cohort conservation — passed exactly.

## 3. What it could not do

- Identify its five central claim classes on the available evidence.
- Claim any country-level shadow-education level or completion trajectory.
- Classify mechanisms (surplus vs competitive; demand- vs education-led) from national aggregates.
- Price the shadow sector: provider entry costs, hours, and rents are not observable; the Korean fee
  level is the only anchored price.
- Establish the economy side from macro data: `PARAMETER_MAP.csv` marks formal-job elasticity, wage
  premia, formal/informal transitions, public-sector share and credential requirements **not observable**.

These are limits of the evidence base and the model class, not findings about the world.

## 4. What the next team should do (data-first, ranked)

| # | Acquisition | Reopens | Cost / route |
|---|---|---|---|
| 1 | PSA FIES/APIS/LFS microdata (PH) | national shadow incidence, wage premium, formality transitions | credentialed request, 2–6 weeks (PSA 403) |
| 2 | Cambodia national tutoring module | KHM national incidence (currently case study) | NIS request/advocacy, 2–6 weeks |
| 3 | Establishment censuses + WB Enterprise Surveys credential module | provider entry costs; credential requirements; formal-job elasticity | credentialed, 2–6 weeks |
| 4 | Korea 2011 archive + provider counts/fees | KOR time path; provider mix | public tables, 1 day–2 weeks |
| 5 | Japan fees (MEXT survey, e-Stat ID) + full 47-prefecture table | E3 density identification (n=2→n=47) | API application + tables, 1–3 weeks |
| 6 | HK repeated gradient (EDB/HKEAA, re-weighted survey) | HKG out-of-sample check | institutional re-contact, 2–4 weeks |
| 7 | China post-2021 incidence/provider split (CFPS/CEPS, MOE) | CHN bound → rate | application, 4–8 weeks |
| 8 | LFS two-wave panels | formal/informal transitions; mechanism classification | institutional, months |

**Dissent recorded (BRAY):** for reopening *cross-country incidence*, PH and KHM national surveys should
rank above the Korean archive; KOR ranks higher only on feasibility. Recorded, not adopted.

## 5. What may be published

- **P1 (the headline):** "Observational equivalence and its limits: a predeclared negative map for a
  massification model." Methods/computational social science; the claim is about the model class and
  evidence base.
- **P2:** "Measuring massification and shadow education across six Asian systems: country cards, target
  register, and a parameter observability map."
- **P3 (conditional, descriptive):** "Provider fees, rents and the income gradient of private tutoring: a
  Korean descriptive calibration."
- **P4 (only if the relations layer lands):** a graded cross-country relation panel. `09_relations/`
  contains the WDI panel and scripts; `RELATION_CANDIDATES.csv` / `MODEL_PLUG_MAP.md` were still building
  at close — treat as pending, not as a result.

**Do not publish:** any incidence, forecast, gate-architecture, or provider-as-missing-channel paper.

## 6. Reproduce

Everything is in this package: `05_experiments/` and `05b_experiments/` (cells, predeclarations,
manifests, logs, error logs), `02_lit/`, `04_data/`, `08_council/` (briefs 001–008),
`06_report/RESEARCH_LOOP.md` (the loop and its stop rules), `RUN_MANIFEST.json` (environment, hashes,
commands), and the ZIP at the package root. The Council's files carry a synthetic-exercise disclaimer.

## 7. Final position

> **Within this model class and the available evidence, identification of the five central claim classes
> is not established. This is a statement about the evidence base and the model, not about the world.**
