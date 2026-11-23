# Pre-registration — supply-led vs demand-led massification, 23 Nov 2026

Committed **before** any data download, script or estimate. Task `task-28`. Branch
`research/supply-demand-2026-11-23` (off `research/subsistence-v2-2026-11-23`); record
`research/records/2026-11-23-supply-demand/`; box2 `/root/work/supply_demand`.

## Starting point from v2 (already pushed, commit ce66cfc)
In the 64 countries where all three events are detectable in the common 1965-2010 window, the schooling
take-off **precedes** agricultural labour release in 61 of 64 (5% the other way; bootstrap 95% 0-11%;
median gap 26 years). So massification is not demand-driven by agriculture shedding labour. The question here:
is it **supply-led** — schools, teachers and laws arriving before the labour-market demand that the human-
capital story requires?

## Supply measures (fixed now)
1. Public education spending, % of GDP (World Bank WDI, pulled from the API for this job).
2. Teacher supply: primary pupil-teacher ratio (WDI; a **fall** is a supply expansion) and teachers per
   1,000 children where available.
3. School capacity near the take-off: primary gross enrolment ratio (WDI) as a capacity proxy.
4. State capacity: the project's observed series in
   `/root/work/local_data/10_massification/data/STATE_CAPACITY.csv` (project file, sources inside it; only
   numeric `observed` rows are used).
5. Compulsory/free-schooling law adoption dates: the project's `POLICY_TIMELINE.csv` (6 systems, sources
   inside it) plus, where a documented literature series exists, its dates cited — coverage is limited and
   will be reported as such rather than extrapolated.

## Demand measures (fixed now)
1. **Wage-premium proxy:** non-agricultural labour productivity relative to agricultural labour productivity
   (from WDI agricultural value added, agricultural employment share, labour force and GDP per worker). A
   rising ratio is the return to leaving the farm / to schooling.
2. Paid (wage) employment share from the project panel (available 1991 onward).
3. Income growth (GDP per worker, long-run Maddison/transition record).
4. Urbanisation share (WDI/project panel).
5. The agricultural labour-release event dates already computed in v2.

## Event-ordering test (pre-registered definitions, common window 1950-2010)
- **Supply onset** = first year after which any of: education spending rises >= 1.0 percentage point within
  10 years; primary pupil-teacher ratio falls >= 10% within 10 years; primary gross enrolment rises >= 10
  percentage points within 10 years.
- **Demand onset** = first year after which any of: non-ag/ag labour-productivity ratio rises >= 20% within
  10 years; paid employment share rises >= 5 percentage points within 10 years; urban share rises >= 5
  percentage points within 10 years.
- Reference: the v2 **schooling take-off** date (mean years of schooling rises >= 1.0 year in 10 years).
- Statistics: share of countries with supply onset <= schooling take-off, and demand onset <= schooling
  take-off; median gaps in years; 1,000-resample bootstrap CIs clustered by country. Cross-tab of the two
  orderings (supply-first / demand-first / both / neither).

## Pre-registered predictions
- **If supply-led:** supply onset precedes the schooling take-off in a clear majority of countries, and before
  the demand onset in most; the horse race puts a larger standardized coefficient on supply.
- **If demand-led:** demand onset precedes the schooling take-off in a majority; the wage-premium proxy leads;
  the horse race puts more weight on demand.
- Given v2, the agricultural-release demand measure is expected to *follow* schooling in the same majority;
  that is the finding being explained, not retested.

## Horse-race panel (pre-registered)
Ten-year changes in mean years of schooling (transition record) on ten-year changes in the supply block and
the demand block, with country fixed effects and period fixed effects, standard errors clustered by country;
standardized coefficients reported both separately and together. Design limits stated in advance: state
capacity, spending and schooling all respond to income and to each other, and there is no instrument here;
this identifies conditional associations and timing, not causal elasticities.

## Falsifiers, stated in advance
1. Supply onset does **not** precede the schooling take-off in a majority (then supply-led fails).
2. Demand onset precedes the schooling take-off in a majority (then the human-capital/demand reading
   survives and supply-led fails).
3. The horse race is indeterminate (neither block carries a stable standardized coefficient).
4. The result depends on one supply measure or one country group (reported with and without each measure).

## Interpretation rule
If supply leads demand and schooling, the "formatting/institutional project" reading survives and the
human-capital-demand story weakens. If demand leads, the opposite. If neither leads, the record says so and
makes no reading. Firmness of the conclusion must match the design: timing + conditional associations, no
causal identification.

## Reporting
Plain words under "(1) Fertility" and "(2) Massification", <120 lines, every number with sample and
uncertainty, data-gap statements where a series is unavailable, <=10-line summary to the dashboard.
