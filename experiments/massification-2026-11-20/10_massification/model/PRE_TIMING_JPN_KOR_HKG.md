# PRE-DECLARATION — timing-of-universalization check for near-universal systems (JPN, KOR, HKG)

**Owner:** experiment-runner (`deepseek-exp1`). **Status:** predeclared, **NOT run**. **Origin:** user directive
(logged 2026-11-20): Japan is probably near-universal already; the question is *when* that happened — same for Korea
and Hong Kong; for near-universal systems the outcome is the **timing of universalization, not the level**. Lead asked
the Council to amend the success criteria accordingly (timing within ±N years replaces level tolerance for
JPN/KOR/HKG; levels become check-only) and data/lit/scout to produce crossing-year series. **Coordinate the milestone
definitions with the Council's directive before running.**

## Why this cell is needed
Brief 013's PASS criterion is level-based (MAE ≤5/8 pp) plus universalization midpoint within ±5 years. For systems
already near universal, a level tolerance is uninformative (the series is at/near the ceiling) and a level MAE can
reward a model that is flat at the ceiling without reproducing *when* the system got there. The first-order object for
JPN/KOR/HKG is therefore the **crossing year** of each universalization threshold (and their ordering/spacing), with
levels treated as **censored checks**.

## Milestone definitions (PROVISIONAL — require Council confirmation)
Brief 013 §1 defines universalization as primary completion ≥95%, lower-secondary ≥90%, upper-secondary ≥90% (cohort
completion, not enrollment). This cell uses those thresholds as the default milestone set and asks the Council to
confirm or amend: thresholds, which measure (completion vs GER vs attainment stock), and the tolerance `N` years.
**No crossing year is ever fitted** — they are derived from the model's generated completion paths and compared with
observed crossing years/intervals.

## Data and censoring (declared)
- On disk today: **KOR** has 24 observed completion years (2000–2023, `status==target`); **HKG and JPN have no UIS
  completion rows** in `04_data/TARGETS_FLOW.csv` (brief 013 lists them as CHECK only). Scout's
  `relations/data/universalization_fits.csv` provides fitted logistic/Gompertz curves for GER-type series (e.g. PHL,
  KHM, CHN), **not** completion crossings for JPN/KOR/HKG.
- Therefore the observed crossing years for JPN/KOR/HKG are **DATA BLOCKED pending the crossing-year series** requested
  from data/lit/scout. This cell is predeclared now so it can run the moment those series and the Council amendment
  land; **it will not run before both**.
- **Interval rule (declared before data):** a crossing year is an **interval**, not a point:
  - observed series rises through the threshold → `[last observed year below, first observed year at/above]`;
  - series is already at/above the threshold at first observation → **left-censored**: crossing occurred at or before
    the first observation, interval `(−∞, first observation]`;
  - series never reaches the threshold → **right-censored**: no crossing observed, interval `[last observation, +∞)`;
  - sparse gaps → the interval is the bracket across the gap. Reported as intervals everywhere; a point crossing is
    only reported when the bracket is one year wide. This is the "sparse/censored series make the crossing year an
    interval" note the Lead asked for, stated as a rule rather than a caveat.

## Design (predeclared)
- **Outcome:** crossing years (intervals) for primary/lower-secondary/upper-secondary completion thresholds, for
  JPN, KOR, HKG.
- **Model side:** same fitted cohort-flow model as the calibration cell; generated completion paths produce model
  crossing years. **Model crossing years are never fitted** and never appear in the calibration objective.
- **Checks:** (a) **interval containment** — model crossing year falls inside the observed crossing interval;
  (b) **ordering** — primary crosses before lower-secondary before upper-secondary (within a country);
  (c) **spacing** — the model's year gaps between the three crossings are within `N` years of the observed gaps;
  (d) **country ordering** — the model reproduces the observed ordering of the three countries' crossing years
  (JPN/KOR/HKG) if the observed intervals separate; if the observed intervals overlap, the country ordering is
  reported as **NOT IDENTIFIABLE** (overlapping intervals cannot order the countries);
  (e) **censoring consistency** — where observed is left/right-censored, the model must be consistent with the
  censoring (crossing at/before the first observation, or no crossing), not merely "close".
- **Levels:** reported as **censored checks only** — no level MAE is used for PASS in these three countries.

## PASS / PARTIAL / FAIL (predeclared; `N` pending Council amendment — provisional N = 5 years, flagged)
- **PASS:** all available country-level crossings fall inside their observed intervals AND ordering and spacing hold
  AND censoring consistency holds AND no crossing is generated where the observed series is right-censored.
- **PARTIAL:** crossings inside intervals but ordering or spacing fails by >N years → timing partially reproduced;
  descriptive only.
- **FAIL:** model crossing falls outside an observed interval, or generates a crossing where the observed series never
  crosses (false positive, brief 013 §3 / STOP RULE R6), or reverses ordering where observed intervals separate.
- **NOT IDENTIFIABLE:** observed intervals overlap for a country ordering / spacing comparison — report as such
  rather than picking a winner (consistent with R13 and the Council's EQUIVALENT vocabulary).

## R4 / R5 / R6 / R12 links
- **R4:** crossing years are derived from generated paths; if the model only reproduces them because a crossing year
  or ceiling was supplied, the cell is FAIL (supplied law).
- **R5:** the discriminator is the crossing-year vector (ordering + spacing + interval containment) — a moment not
  used in fitting; level improvements alone do not count.
- **R6:** a generated crossing where the observed series never crosses is a structural failure, not a near miss.
- **R12:** no retro-fit; existing cells (PHL smoke `13c93588…`, PHL+CHN batch, scaling repair if accepted) are not
  re-labelled by this cell.

## Dependencies and sequencing
1. Council amendment to brief 013 (timing replaces level tolerance for JPN/KOR/HKG; `N`; milestone definitions).
2. Crossing-year series from data/lit/scout for JPN/KOR/HKG (or an explicit statement that they are unavailable, in
   which case the cell is DATA BLOCKED and reported as such).
3. Scaling-channel repair decision (this cell runs **after** that, per the Lead's sequencing; it does not depend on
   the repair's outcome for its own validity).

## AMENDMENT (repo-auditor instruction 4; Council Amendment A4 pending) — applied before the next run
- **Role label fixed now:** the crossing years are a **HOLDOUT OUTCOME** — derived from generated completion paths,
  **never** entering the fitting objective, never a parameter, never supplied (R4/R5). This is stated explicitly so
  the label cannot drift once A4 lands.
- **Roles pending A4:** for JPN, KOR and HKG, levels become **CHECK-ONLY** once Council Amendment A4 is posted;
  until then the brief-013 roles stand unchanged and this cell does not run. PHL/CHN/KHM roles are unchanged by A4.
- **Tolerance:** ±N years is **provisional N=5** (brief 013's midpoint tolerance used as the provisional stand-in);
  the cell will not be scored until the Council sets N in A4.
- **Sequencing:** predeclared before the next run, per repo-auditor instruction 4; runs only after (a) A4, (b) the
  crossing-year series, and (c) the scaling-repair decision. Crossing-year series remain DATA BLOCKED for JPN/HKG (no
  UIS completion rows on disk) and are requested from data/lit/scout.
