# The model, described from the code

`masseng` is a cohort-flow model of a national school system. It is written for comparative work. The engine
holds no country facts: every country-specific number lives in `countries/<ISO3>/`. Moving the model to a new
country means writing a new folder, not new code.

## What is simulated

**Population.**
- Each birth cohort is sized from World Bank data: births = crude birth rate × population, multiplied by
  survival to age five (1 − under-five mortality).
- Before 1960 the population is back-extrapolated at a declared growth rate.
- Later mortality and migration are ignored.
- Each cohort is split into ten equal income deciles. The income of each decile relative to the national mean
  comes from a lognormal distribution with the WDI Gini for that year.

**Schooling states.**
- For each cohort, decile, grade and sector (public or private), the model tracks the share of the cohort
  enrolled in a given year.
- Years are reference years: the year in which the school year ends, the UIS convention used by WDI.
- Grades:
  - primary: 6;
  - lower secondary: 3 or 4, by country;
  - upper secondary: the rest of six secondary grades, from the year the country introduces it;
  - tertiary: 4.
- Flows are expected values. There are no random draws, so every run is exactly reproducible.

**Each year, for every enrolled pupil:**
1. A fixed share repeats the grade (declared, by level). The rest pass.
2. The household decides whether the child continues. The probability is a logit in:
   - a level intercept, with a separate intercept for the decision to enter a new level;
   - `eta × ln(household income ÷ 1990 national mean income)`: demand rises with income. Under the "trend"
     rival this term is a smooth time trend with the same 1971–95 slope; under "none" only cross-sectional
     income differences remain.
   - `− kappa × ln(1 + cost ÷ household income)`: the cost of a school year, including fees, uniforms,
     transport and the child's forgone earnings, as a burden on that household. (v1 used `cost ÷ income`.
     See PROTOCOL.md, amendment A2.)
3. At entry to a level the household also chooses public or private. This is a nested logit: private carries
   its own intercept and an income slope, and the continuation decision uses the inclusive value of both
   options.
4. **Tertiary public places are rationed.**
   - Each year the public first-year places equal a capacity share × the population at tertiary entry age.
   - If more families want a public place than exist, every applicant has the same chance of an offer.
   - Applicants without an offer can still enrol privately, at private cost.
   - How the capacity grows is a named hypothesis:
     - `fiscal`: with income per head;
     - `trend`: at a fitted rate;
     - `responsive`: by a share of last year's unmet demand;
     - `unconstrained`: no rationing.
5. Where a country has an exam between secondary and tertiary (Cambodia's Grade 12 Bac II), only the observed
   share who pass face the tertiary decision.

**Entry to Grade 1.**
- Children plan to start at 6 or 7; the share starting at 6 is a declared, dated path.
- A declared share starts one year late.
- Optionally, children who have never entered can enter up to a declared age at a declared yearly rate.
- Optionally, after a conflict, children up to 14 catch up at a declared rate. This is used for Cambodia after
  1979.

**Policies** are dated changes to the cost of a level and sector, for example the abolition of public
secondary tuition in the Philippines in 1988. Some are decile-targeted transfers, such as conditional cash
transfers for the poorest three deciles.

## What is measured, and how

Every indicator is computed the way the source computes it.
- **GER:** everyone enrolled in a level, divided by the population in the official age band for that level
  in that year.
- **NER:** only enrolled children of official age, over the same band.
- The official entrance age and durations are read from WDI for each year (`SE.PRM.AGES`, `SE.PRM.DURS`,
  `SE.SEC.DURS`). The tertiary band is the five years after the end of secondary, as in UIS.
- So when the Philippines changed its official entrance age (7 to 6, 1998), or when K-12 lengthened secondary
  (4 to 5 to 6 years, 2017–18), the model's denominators change exactly as the published ones did. Breaks in
  the published series are reproduced, not smoothed away.
- Private shares are private enrolment over all enrolment in the level.

## What is checked automatically (`tests/test_model.py`)

- Stock-flow conservation, for every cohort and decile. Everyone who enters Grade 1 ends up enrolled, a
  dropout, a completer of some level, or censored at the maximum age.
- Determinism.
- Upper secondary appears only from the reform year.
- K-12 produces a tertiary entry gap in the two transition years, and nothing changes before the reform.
- The fitting function refuses test rows.
- Training and test rows are split by year.
- Indicator age bands match WDI definitions.
- Switching policies off changes nothing before the first policy year.

## Parameters

Eleven parameters are fitted on training years only:
- `eta`: demand–income;
- `kappa`: cost burden;
- five level and entry intercepts;
- `mu_basic`, `mu_ter`, `nu`: private choice;
- `k_ter`: public tertiary capacity.

The S2 and S3 supply rivals add one rate each. Every other number is declared, with a source or a reason, in
`docs/assumptions.md`. Because more than five parameters are fitted, a recovery test is required:
`scripts/recovery_test.py`.

## What the model leaves out

- school quality and learning;
- teachers and budgets, except through the tertiary capacity rule;
- geography and distance;
- migration;
- shadow education (private supplementary tutoring);
- informal fees beyond the declared cost levels;
- gender;
- any change in the labour-market return to a credential except through household income.

Each omission is a place where the model could be wrong for reasons it cannot see. The report says which
failures probably come from which omission.
