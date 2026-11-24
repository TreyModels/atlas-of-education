# What the papers should be (assessment of 24 Nov 2026)

Status of every number: see `CLAIMS_LEDGER.md`. Required edits to the seven existing drafts: see `TEXT_FIXES.md`.
Experiments that would change this plan: see `NEXT_EXPERIMENTS.md`.

## Bottom line

The programme has **measurement, sequencing and falsification results**, and **no identified causal mechanism**. The Council
(`research/records/2026-11-25-council-novelty/DECISION.md`) was right: no new correlation, a handful of new assemblies, one
conditional method. Every paper below must be framed as a *quantified audit*, a *dating-and-assembly result*, or a *design
rule*, never as a discovered mechanism. Four papers, one optional note, and a list of things to stop.

## Paper 1 - "Schools before factories" (sequencing)  [lead paper; Council rank 1]
Absorbs the massification draft (M) and the agricultural-development sequencing section (N3).
- **Claim:** in late-industrialising countries the schooling take-off precedes the release of agricultural labour in 31 of the
  34 countries where order can be identified (91%); 30 more cannot be ordered because a date sits on the 1965/1991 window
  boundary; median lead 18 years where both dates are exact (n=18). Bounds across all 64: 48-95%.
- **Supporting:** supply-block vs demand-block ten-year-change horse race (+0.456 vs +0.006, n=78, 51 countries); fee-abolition
  event study as a first-stage check (after E8); historical contrast cases (Prussia/US North supply-led, Britain demand-led).
- **Must drop or restate:** "labour-market demand precedes schooling in only 7% of 58 countries". That figure is largely a
  data-start artefact (wage-employment and agricultural-employment series begin in 1991 for every country; 92% of schooling
  take-offs are dated by 1990). See `results/demand_series_start_check.txt`. Replace with the redesigned test (E6) or delete.
- **Binding conditions (Council):** frame as dating, not causation; keep the schooling-vs-fertility strict ordering (24/64 =
  37.5%) separate from the release-vs-fertility ordering; never use the retracted 68.75%; dedicated paragraph on endogeneity and
  coarse dating.
- **Journal fit:** World Development, Journal of Economic History, or Comparative Education Review.

## Paper 2 - Schooling and fertility: a levels-vs-changes audit  [Council rank 2]
Merges Paper F and Paper N2; folds in the GPU counterfactual as a model-bound section and the supporting nulls as an audit table.
- **Claim:** the schooling-fertility link is a between-country level gradient, not a within-country change lever: negative and
  significant in 71-99% of 13,800 random partitions in levels, 0-7% in ten-year changes; the t+10 future-schooling placebo is
  ~90% as strong (52.9% vs 58.8%).
- **New this session:** the orthogonalised placebo (`results/placebo_orthogonal.txt`). With both S(t) and S(t+10) in the model,
  future schooling keeps a coefficient comparable to or larger than current schooling for lower-secondary, secondary and tertiary, with and
  without country fixed effects; tertiary is dominated by the future value (primary completion is the exception). This is the strongest available evidence for the
  "co-trending, not causal" reading and answers the serial-correlation objection. Limits: exploratory, 22 Nov panel, two
  trending series cannot be fully separated; E11 repeats it with change-on-change at several lags on the 23 Nov battery panel.
- **Supporting audit table (not a separate paper):** farm decline -> fertility null (MDE 0.016 births); care-work absorbed by GDP
  and urbanisation; credential-gap correlation; marriage timing reversing in change-on-change; tipping-point statistics. Label
  them "power-calibrated" only where an MDE exists, and "exploratory" otherwise. Only this paper has a preregistration file.
- **GPU section:** mortality freeze removes 3.2% of the model's collapse; individuation does not beat development-only out of
  sample. Model-bound; state so in title, abstract and conclusion.
- **Never claim a new correlation.** Closest prior art: Liu & Raftery (2020), Nickell (1981), Durlauf et al. (2005).

## Paper 3 - Shape of the fertility transition (short note, conditional on E14)
- **Claim:** in the annual 1960-2023 window, exponential-to-floor and Gompertz forms beat the logistic out of sample; interior
  shape varies little (SD ~0.15) once onset and floor are aligned; timing correlates are schooling timing (+0.16 years per year,
  n=90), starting child mortality (R2 0.29 for onset, 0.53 for midpoint, n=66, post hoc) and not income at onset (n=68, null).
- **Honest limit:** the window is left-censored at 1960, so it cannot distinguish a non-logistic form from a logistic it cannot
  identify. UN projections use a double-logistic (Alkema et al. 2011), which is the real rival; E14-E15 are required before
  submission. If E14 fails or cannot be run, fold this into Paper 2 as a section.
- **Country anchors:** the eight countries that crossed replacement while poor or under-schooled (ARM, CHN, NPL, VNM, GEO, IND,
  ALB, BTN).

## Paper 4 - Which countries does the coefficient describe? (methods note; Council rank 4, conditional)
- **Claim:** varying the *country partition* rather than the controls shows that most cross-national links in the project's matrix
  are group-specific or no better than random (5 of 272 travel; 161 no better than random); plus the 1/(R+1) draw-count rule.
- **New this session (`results/known_truth_sim_summary.md`):** a known-truth simulation shows the verdict taxonomy has low
  power at small R, controls false positives, but labels a link planted in only one third of countries "robust everywhere" 85% of
  the time. The paper must either add a heterogeneity condition or rename the tier "significant everywhere" and always report
  group-specific tags alongside it. This is a real improvement to the paper and a real caveat to its current Section 5.3.
- **Conditions:** E1 (>=1,200 draws), E2 (known-truth with the real estimator), E3 (heterogeneity rule on real data), E4
  (imputed-panel sensitivity). Do not submit before E1 and E2.
- **Journal fit:** Sociological Methods & Research.

## Optional note - "Six Philippine demand models lose to persistence" (registered-null note)
Source: `research/masseng-v6/manuscripts/Philippine_demand_rivals.md` (branch `experiment/masseng-v6-surplus-motor`). Best model
7.458 points error vs 6.600 for repeating the last value; key coefficient at its bound (15/20 recovery replicates). Not
blind validation; the CHED headcount table is unchecked against its PDF. Publish only if the QA gap is closed. It is a negative
result and must not be cited as support for the credential-pipeline manuscripts (`June_credential_pipelines.md`,
`May_structural_account.md`), which are theory papers the data do not support.

## Stop doing
- Electricity as a driver (zero under country trends: +0.05 +/- 0.19 per the 23 Nov dashboard README; 11 of 32 links flip sign
  more than random).
- Paid employment / wage jobs -> tertiary (dies across 1,536 specifications, median 0; clean null in the grouping multiverse).
- Early-marriage timing (reverses in change-on-change, +0.020 -> -0.027; circular shift p = 0.08).
- Tipping-point / scaling statistics (wrong-sign autocorrelation; variance fails 16,000 surrogates).
- Composite "development bundle" stories (PC1 83.7% dissolves to 0.39-0.56 within countries).
- Any reading of MASSENG as support for the surplus-motor theory.
- Child-labour/electricity (-0.417) as independent confirmation: one Bayesian association on sparse survey years, and electricity
  itself is fragile.

## Order of work
1. Text fixes (TEXT_FIXES.md), because one wrong headline sits in three drafts.
2. E1 + E2 + E3 (methods), E6 + E8 (sequencing), E11 (fertility), E14 (shape): these decide whether papers 1-4 are submittable.
3. Everything else is optional.
