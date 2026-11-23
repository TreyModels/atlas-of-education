## 13. Future research: what would settle it

The paper's central vulnerability is that its dates are ours — literature-standard dates and our own event
definitions — and its central claim is an ordering claim. Future work should attack both, in the order of what
would most change the conclusion.

### 13.1 The ordering itself: recoding and re-detection

Before any new data, the ordering claim needs a robustness pass that this session could not complete (the raw
series were on a server that went down, so alternative-threshold recoding was not possible). Concretely: re-detect
the three events under alternative definitions — statute versus measured enrolment for schooling; 1 versus 2
years of schooling per decade; 3 versus 5 points of agricultural-employment decline; different windows and
smoothing rules — and report how many of the 61 forward cases flip under each. A second coder should code a
sample of countries blind to the first coder's dates, with a pre-registered agreement threshold, and a
date-by-date source table with page references should be published for every country in the headline table. What
this would settle: whether the 61/64 count is a property of the events or of our definitions. What it would not
settle: causality.

### 13.2 Historical enrolment series: measuring the classic cases properly

The four historical cases are the paper's weakest evidence because their dates are literature-standard. Four
series would turn them into measurements:

- **Prussian enrolment 1800-1870** from Flora, Kraus and Pfenning (1983) and Lindert (2004), checked against the
  Prussian statistical yearbooks where possible. What it identifies: the date at which enrolment take-off precedes
  industrialisation and the farm exodus — the 80-120 year lead — on a measured series rather than a statute date.
- **French primary enrolment 1830-1900** from Diebolt's series and the ministry's *Statistique de l'enseignement
  primaire*. What it identifies: the gap between the 1833 statute and the attainment take-off, which is the
  France case's whole point, and which literature dates only bound.
- **UK school attendance 1850-1900** from the Newcastle Commission (1861) and the Board of Education annual
  reports. What it identifies: attendance before and after 1870, i.e. whether the Act ratified demand or created
  supply.
- **US high-school enrolment 1890-1940** from US Historical Statistics, series H-598 onward. What it identifies:
  the timing of the high-school movement relative to the national farm exodus, which the paper currently states
  from literature dates only.

What these series would not do: identify causal effects. They would date the events better, and they would allow
the lead/lag to be quantified with the uncertainty of each series rather than as point dates. Definitional
changes in the series (who counts as enrolled, attendance versus registration) are themselves a research problem,
not a nuisance.

### 13.3 Compulsory-schooling-law dates as treatment

The strongest design the project can see is to use the staggered adoption of compulsory-schooling laws as a
natural experiment. The data exist in Flora and Alber (1981), Flora, Kraus and Pfenning (1983) and the subsequent
literature; the design is an event study or difference-in-differences around law adoption, with pre-trends and
heterogeneity by enforcement. What it identifies: the effect of a **law**, not of schooling per se, on enrolment,
attainment, fertility and labour supply — a policy-relevant parameter, and a test of whether state action moved
the pipeline. Threats: laws are endogenous to demand and to state capacity, enforcement varied enormously (the
Prussian case is a warning), adoption is bundled with other reforms, and anticipation can shift effects earlier.
A credible design would need enforcement variation (e.g. district-level enforcement intensity) and would have to
be pre-registered.

### 13.4 Subnational school-construction variation

The most promising design for the mechanism is subnational: district-level school openings or school-construction
programmes, matched to census attainment, fertility and employment. What it identifies: local effects of school
supply on attainment and on the labour market, with better control of national policy and income; spillovers and
migration are the main threats, and they are measurable. Data needs: school registers or construction records,
census microdata, and boundary maps. The project does not have these data, but the design is the natural next
step for a country-level research programme, and it is the design that could turn "supply-led" from a description
into an estimate.

### 13.5 Cohort-linked microdata for the generational claim

The theory's generational wording — a cohort that entered school as the farm exodus accelerated had fewer
children — needs cohort-linked microdata: DHS or IPUMS samples with attainment, fertility and employment for the
same women. What it identifies: the individual-level relationship, the wealth horse race, and the quantum-tempo
decomposition that the project's cell-level (ecological) DHS gradient could not test. The data gap is documented
in the record (the public DHS API exposes aggregates only; individual recodes sit behind registration).

### 13.6 What the current evidence cannot claim

Stated plainly, so that no reader mistakes the paper for more than it is:

- The historical **dates are literature-standard, not verified** in this pass; every one is labelled UNVERIFIED,
  and a referee should spot-check two.
- The **event definitions are ours** (1 year of schooling per decade; 3 points of agricultural decline; 10-year
  windows), chosen in advance but not given by nature; alternative thresholds have not been run.
- There is **no causal identification**: the horse race is a decomposition, the event ordering is timing, and the
  policy implications are about sequencing logic, not effect sizes.
- The data are **period series, not cohorts**; the generational claim is not tested here.
- The 64-country sample is **selected on data availability**, and the historical cases are a **dated argument,
  not a sample**.
- The literature search could not use subscription databases (no Scopus/Web of Science/EconLit), so "as far as
  our recorded search can find" is a real qualification, not boilerplate.
