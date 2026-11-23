# Plan for jobs 4 and 7 (not run: need data not on the server and several hours of modelling)

## Job 7 first (it feeds job 4)
Inputs to fetch: UN World Marriage Data (WMD 2019+ xlsx: singulate mean age at marriage, % never married at 45-49, by sex, census/survey year);
UN World Population Prospects living arrangements of 60+ (co-residence with children); Schulz et al. 2019 kinship intensity index; WVS/EVS family-ties items.
Steps: (1) download on the server (internet works), keep raw files under data/raw; (2) map country names to ISO3 via meta.json;
(3) keep survey years, interpolate to the 5-year grid only for plotting, never for estimation; (4) merge into the panel as separate files
(`smam_f`, `nevermar_f_4549`, `coresid_60plus`, `kin_index`) with an availability table (countries x years) before any regression;
(5) test: do marriage-timing proxies add anything to schooling -> fertility once country trends are in (reuse full_matrix_trends.py edge()).
Deliverable: coverage table + 4 new edges with/without trends. Estimated 1-2 hours.

## Job 4: individual-level marriage/fertility model (rebuild matching_model.py)
Fix REVIEW's list: women 15-49 by single age and schooling including zero (Barro-Lee attainment by age group, 5-year steps);
two-sided marriage market with depletion (men's schooling distribution, age gap, matching by schooling, unmatched women remain single);
kin-support channel as an ESTIMATED parameter (not hand-set), with a prior centred on no effect; cohort deepening as a parameter;
fit jointly on 8-10 countries (births by age, never-married 45-49, SMAM from job 7) by approximate Bayesian computation or SMM;
validate on held-out countries and on the last cohort. Falsifiers: (a) world with kin parameter = 0 must be recoverable;
(b) permuting schooling across women must remove the fit gain. Success criterion decided in advance: held-out births within 15% in >=70% of countries.
Estimated 1-2 days; do not start before job 7 data exist.
