# Publishable papers: ranked audit (23 Nov 2026)

Basis: handoff pack (STATUS, REVIEW, results, papers), the two massification branches, the research track (marriage-gap, credential-floor,
china-forecast-ledger, methods-paper) and today's runs. "Solid" = survived a test built to break it. I read the research-track READMEs and
NOVELTY.md only; I did not audit their numbers. Literature novelty is judged from the pack's own lit review and from memory, not a fresh search; check before submitting.

## 1. "Wage employment and higher education: a fragile association" (paper 01)  -- most ready
- Claim: the cross-country link between wage jobs and university enrolment looks strong in one specification (+1.43) but is positive and significant in only 27.9% of 1,536 defensible specifications; median about zero.
- Evidence (solid, as a fragility finding): spec_curve_1536.txt; leave-one-country-out stays positive in 203 of 203 drops; a common-cause simulation cannot reach the headline (0 of 1,200) but only at the favourable specification.
- Novel: a specification-curve audit (Simonsohn, Simmons and Nelson 2020 method) applied to cross-national education-labour regularities, with a simulation of the rival "one latent development factor" world. Negative/robustness papers in this field are rare.
- Missing: rerun the curve with country trends (today's matrix suggests most FE edges die); drop the "+1.43 leads" language; add power simulation like job 2 so the null is interpretable; clean replication package (hard-coded /root paths).
- Target: International Journal of Educational Development, or Comparative Education Review (research note).

## 2. A development-panel audit: most cross-country "causal" edges vanish under country trends, and the trend test can see real effects
- Claim: of 126 edges that pass country fixed effects among 17 development variables, 25 survive country-specific trends; a simulated true electricity effect of 20 points is caught 91% of the time with trends (false positives 2-4%), so the loss is mostly confounding by shared trends, not blindness.
- Evidence (solid for the method, today's runs): full_matrix_trends_out.txt; bpower_out.txt (500 panels, null and S-curve worlds). Weak spot: real-data electricity -> lower-secondary trend estimate is 0.052 +/- 0.19 (95%), so it is "not separable", not "zero".
- Novel: power-checked trend test on a full variable matrix; most "what drives schooling" cross-country regressions only report fixed effects. Close relatives: Bayesian model averaging growth papers (Sala-i-Martin; Moral-Benito), Nickell-type panel critiques, Boppart et al. 2023 (their latent-development logic is used as the null world).
- Missing: power curve matched to real sample sizes (simulate at n=1,343); lead/lag and quadratic-trend variants; multiplicity control across 272 pairs; show which of the 25 survivors are mechanical (e.g. mortality -> fertility).
- Target: Journal of Development Studies, or Demography/Population Studies as a methods note; Journal of Applied Econometrics if the power section is deepened.

## 3. Schooling and the fertility fall: association is not chance, but the schooling channel adds little out of sample
- Claim: schooling is strongly tied to fertility within countries, yet adding a schooling term to a markets-only cohort model improves prediction of the last two cohorts in just 15% of countries (worsens 16%), with large gains only in a few high-fertility countries.
- Evidence: luck test (0 of 20,000 shifted worlds reach 11.97%; REVIEW says the time-shift null is easy, so treat as moderate); today's cohort_huge_out.txt (power ok: alpha 0.15 detected in 90% of worlds, false alarms 2%). Not solid on causation: model is hand-structured, schooling interpolated with look-ahead.
- Novel: out-of-sample comparison with a built-in power check; a null/mixed result against the individuation story (Caldwell wealth flows; Henrich) is publishable if framed as a test of that mechanism.
- Missing: the rebuilt individual model (job 4) and marriage data (job 7); estimated rather than hand-set parameters (GAMMA, THETA, PSI, ETA are fixed); drop the 12% variance-share figure; proper loss metric instead of ratio-of-errors.
- Target: Demographic Research or Population and Development Review.

## 4. Credential floor: can the data distinguish four theories of the credential? (research track, not audited)
- Claim: Cambodian wealth-quintile completion profiles fit human-capital, positional, relational and relative-risk-aversion versions equally; the paper asks what data would separate them.
- Evidence: structured recovery and nesting checks in research/credential-floor/results (read README only). Tier unknown until results are checked; an identifiability result is only as good as its recovery test.
- Novel: adds Breen-Goldthorpe relative risk aversion as a rival and frames the problem as identification, not fit; fits the "model uncertainty" literature in education.
- Missing: independent audit of the numbers; second country; a concrete proposed natural experiment.
- Target: Comparative Education Review, or Sociology of Education.

## 5. Methods paper: executable models with a testing protocol for comparative education
- Claim: educational models should be published with recovery tests, nesting checks and frozen forecasts.
- Evidence: the repo's own worked cases (marriage-gap, forecast ledger where an 11-parameter model lost to a seasonal naive rule). The repo's NOVELTY.md already concedes that analytical sociology (Hedstrom; Manzo) has argued the core idea; contribution is translation plus protocol.
- Missing: forecast ledger needs months of out-of-sample data; fact-check sources for China youth unemployment (only partly verified); systematic literature search.
- Target: Sociological Methods and Research, or Comparative Education Review.

## 6. Input prices move farm exit, not births -- HOLD / negative note only
- Today's rebuild with income controlled: the wage-jobs effect disappears (-0.014 -> -0.002), farm exit halves and with trends is +0.007 +/- 0.005; births zero everywhere. The original +0.445 could not be reproduced (script lost). Also: CES elasticity 0.43 [0.31, 0.56] is reproducible (independent-seed recovery now unbiased) but not structural.
- Only publishable as a short negative result ("fertility does not respond to world fertiliser prices"), e.g. Food Policy or Agricultural Economics note, after the construction is rebuilt and checked against the Boppart et al. input measures.

Do not submit: paper 02 (floor and apex) as written. It rests on +16.05 from a single specification; with trends the electricity effect is +0.05 +/- 0.19.

Ranking rationale: 1 and 2 rest on tests that already ran and can be written now; 3 needs the model rebuild; 4 and 5 need external audit; 6 is mostly dead.
