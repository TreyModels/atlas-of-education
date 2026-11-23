# Supply-led vs demand-led massification: why schooling precedes farm exit, 23 Nov 2026

Branch `research/supply-demand-2026-11-23`. Pre-registration was the **first commit** (`f7b38f3`), before any
data download, code or estimate. Box2 `/root/work/supply_demand`. This tests the question left by subsistence
v2: the schooling take-off precedes agricultural labour release in 61 of 64 countries (median gap 26 years), so
massification is not demand-driven by agriculture shedding labour. Is it **supply-led**?

## Data
- **Event data reused from v2** (`/root/work/subsistence_v2/out/event_dates.csv`): 108 countries with a
  schooling take-off date, 97 with a demand onset, 89 with both a supply and a demand onset.
- **Supply:** public education spending (%GDP), primary pupil-teacher ratio, primary gross enrolment (World
  Bank WDI, pulled from the API for this job, 1960-2024); plus the project's 6-country state-capacity file
  (`STATE_CAPACITY.csv`: spending, teachers, compulsory-education years in law) and compiled
  compulsory/free-schooling law dates (`POLICY_TIMELINE.csv`, sources inside the file).
- **Demand:** non-agricultural relative to agricultural labour productivity (a wage-premium proxy built from
  WDI agricultural value added, employment shares, labour force and GDP), paid-employment share (project
  panel), urbanisation, income growth, and the v2 agricultural release dates.
- **Data gaps stated, not proxied:** a full cross-country compulsory-schooling-law compilation from the
  literature was not possible in this window (documented law-date datasets exist, e.g. for OECD countries;
  not compiled here), and the state-capacity file covers only six East Asian systems. The education-spending /
  pupil-teacher / enrolment series start in the median country only in **1975**.

## (2) Massification
**Raw event ordering** (pre-registered rules, common window 1950-2010): supply onset precedes the schooling
take-off in **28%** of countries (bootstrapped 95% CI 19-37%; median gap +10 years, i.e. supply turns later);
demand onset precedes it in **73%** (64-82%; median gap -5 years). At face value this looks demand-led — but
two measurement facts undercut that reading:
1. **Censoring and data start.** 61 of 108 schooling take-offs sit exactly on the 1965 window boundary, while
   the supply series start in the median country in 1975. Countries whose schooling turned early cannot show a
   supply date before it. In a **fair sample** of 33 countries (schooling after 1965 and supply data present
   before the take-off), supply precedes schooling in **76%** and demand in **79%**, with supply before demand
   in only 39% — the two sides turn at essentially the same time.
2. **Which demand?** When demand is measured only by labour-market variables (wage premium and paid
   employment), it precedes schooling in just **7%** of countries. The raw "demand-first" result is carried by
   broad development indicators (income, urbanisation), not by the returns to schooling or wage jobs.

**The horse race is the sharper test** (ten-year changes in mean years of schooling, country and period fixed
effects, clustered by country; supply and demand measures standardized and entered together): the **supply
block dominates** — composite standardized coefficient **+0.456 (SE 0.174)** for supply versus **+0.006
(SE 0.203)** for demand; individually, gross enrolment **+0.307 (0.146)** and education spending **+0.125
(0.058)** are significant, while every demand measure is null (wage premium -0.209 (0.114), paid employment
+0.051 (0.117), urbanisation -0.049 (0.096), income +0.140 (0.136)); n=78 country-period observations, 51
countries (limited by supply-data coverage). With demand alone, no demand measure is significant (n=300, 103
countries). The six-country state-capacity/law dates are mixed relative to the (censored) schooling dates and
are reported as a caveat, not as evidence.

**Reading, and how firmly:** the supply-side (schooling-system/institutional, "formatting") reading survives.
School places, teachers and spending move at least as early as the labour-market demand indicators and carry
the conditional association with schooling expansion, while wage premia and paid jobs do **not** lead the
schooling take-off. The human-capital-demand reading is therefore not supported by the timing of its own
variables. This is **timing plus conditional association, not causal identification**: education policy,
state capacity and income are jointly determined, the supply series are short, and there is no instrument
here. The honest statement is "supply-led is the better description of these data", not "supply caused
massification".

**Pre-registered falsifiers and what happened:** (1) supply does not precede schooling — *fired in the raw
test (28%) but not in the fair sample (76%), so it is a measurement artefact, reported*; (2) demand leads —
*true only for broad development indicators, false for labour-market demand (7%)*; (3) horse race
indeterminate — *not fired; supply dominates*.

## (1) Fertility
This job does not estimate a fertility effect, so no new fertility claim is made ("not applicable here" as a
direct test). The relevant link from v2 is that the schooling take-off also precedes the fertility decline in
69% of countries (bootstrap 58-80%). Read together with the supply-side result: mass schooling expands before
the labour-market demand and before the fertility fall, which is the ordering a formatting/institutional
reading predicts and the opposite of schooling expanding because fertility fell or because farms released
labour. That is a sequencing statement, not a fertility effect, and fertility estimates remain
demonstration-level from v2.

## Files and provenance
`scripts/`: `pull_wdi_education.py` (World Bank API supply indicators; raw file on box2 at
`/root/work/supply_demand/data/wdi_education_long.csv`, 2.4 MB, not committed), `supply_demand.py` (events,
ordering, robustness, horse race, six-country note). `results/`: `supply_demand.txt`, `supply_demand.json`,
`event_ordering.csv` (one row per country: schooling, release, supply, demand, gaps), and the intermediate
five-year panel (kept on box2; not committed). Reused data: v2 event dates, task-22 WDI extract, transition
record, project panel; `STATE_CAPACITY.csv` and `POLICY_TIMELINE.csv` from the project's local massification
folder. Runtime: API pull ~2 minutes (network); analysis a few seconds on one core — the box was running the
task-21 battery, so the job stayed light.
