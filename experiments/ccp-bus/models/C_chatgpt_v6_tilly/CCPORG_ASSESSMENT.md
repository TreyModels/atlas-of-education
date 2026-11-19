# ccporg.org: evidence assessment and integration rules

Reviewed 18 November 2026, while the V6 experiments were running. Sources: [personnel index](https://ccporg.org/list), [methods](https://ccporg.org/method), [network page](https://ccporg.org/en/hall/net). The site is an independent source index, rather than an official complete risk register. No bulk export or API has been verified here. None of its records has been fitted to the executed model.

## Available material

The index reports 741 personnel events through 17 November 2026, with 444 people on the appointment side and 187 on the disciplinary side. Event counts and person counts use different units. Its methods describe department/director-general rank and above, requiring an identified person and at least two career segments for inclusion. Appointment, pre-appointment notice, investigation, disciplinary action and judicial referral are separate event categories.

Career links include co-service, succession and transfer-following, alongside educational/geographic ties and rumors. The site assigns evidence grades and clusters weighted links with Louvain. Rumors contribute to clustering; a B-grade link is therefore not by itself a verified co-service relation. Promotion-side and disciplinary-side networks are constructed separately. Reported coverage differs across ranks and cohorts, with some provincial estimates based on only three sampled provinces.

## What it can contribute

Use source-linked career segments to build observed office histories. Dated overlap can supply candidate exposure to people who later experience a disciplinary event. Preserve announcement type and publication date. An investigation, sanction, judicial referral and proven conduct need different variables. Selection during a leader's tenure does not independently establish that leader's personal selection.

The graphic's groups are exploratory descriptions. Build a common person-position-year population before comparing outcomes. Fix the same observed-edge rules and risk window for everyone. Include incumbents without a recorded 2026 event; missing records remain unknown. A site built around personnel news cannot supply an unbiased national denominator.

The methods page also describes one-sided binomial comparisons at p < 0.1 for neighborhood statistics. My methodological assessment is that overlapping neighborhoods, shared campaign exposure and many comparisons prevent those labels from serving as independent confirmatory tests. Use a declared risk population and uncertainty treatment appropriate to dependent observations. The current event index chiefly concerns 2026; historical career segments do not by themselves supply complete earlier disciplinary follow-up.

## Primary analysis rules

- Keep only source-backed co-service links with usable service intervals and source publication dates preceding the analysis cutoff. Exclude rumor links from the primary graph; other relationship types remain separately labeled.
- Distinguish evidence grades from the actual basis of a link. A/B alone is insufficient because the site's categories can include rumors.
- Freeze the evidence available before an outcome. A biography published following investigation can enrich an earlier career retrospectively and create detection bias if used as though it were available beforehand.
- Keep imputed end dates flagged. Use explicit-date links in the strict graph and alternative interval assumptions in robustness checks.
- Define entry, position change, retirement and censoring from source-backed dates. Absence of a news item is not evidence that an incumbent remained in office or stayed clean.
- Preserve separately documented personal-selection evidence. Shared service, later promotion and network membership do not establish that Xi personally selected someone.
- Treat uneven coverage as a measurement problem. The small-sample coverage percentages do not provide validated sampling weights.

## Implication for this model

The strongest immediate use is an observed-career layer and a traceable event ledger. It can help specify targets for role turnover, career overlap and appointment-to-investigation intervals. The model's latent obligations and misconduct still need independent operational evidence. A node's proximity to an investigated official can become an exposure variable after the source rules above; it does not establish guilt.

Terra reviewed these integration principles during the model's peer review. Its principal cautions concern selected high ranks, left-truncated careers, event-conditioned graph construction and unobserved links. The supplied `empirical_adapter.py` applies conservative evidence filters to compatible CSV exports and keeps rejection reasons. It does not claim to have downloaded the site's underlying database.
