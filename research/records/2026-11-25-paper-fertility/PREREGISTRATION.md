# PREREGISTRATION.md — pre-registered rules compiled for Paper F (dated 25 November 2026)

This file exists because "pre-registered" is load-bearing in the paper (the 336-specification curve, the 80%
transportability rule, the future-schooling placebo rule). The paper is a synthesis of workstreams that each
pre-registered its own design **before their analysis code ran**; this file compiles the rules verbatim from
those pre-registrations so the paper branch carries the artefact a methods referee will look for. It is a
compilation with provenance, not a new pre-registration: it adds no analyses and was written after the results
exist, which is why each rule cites the earlier commit that fixed it before estimation.

## 1. Specification curve (Paper F §4.4; 336 specifications)

Source: `research/corr-rebuild-2026-11-23`, `PRE_REGISTRATION.md`, commit **c077672** — committed and pushed
before any analysis code (`c077672` is the first commit on that branch; results are the second commit). The
pre-registered grid: 4 lags × 3 control sets × 2 fixed-effect sets × 4 functional forms × 3 measures = 288
period-TFR specifications, plus 48 cohort cells = 336 total; **every cell reported**; decision rule P5:
"≥80% negative and ≥50% negative-significant" for the period specs.

## 2. Transportability (Paper F §4.5; random re-partitions)

Source: `research/corr-battery-2026-11-23`, `PRE_REGISTRATION.md`, commits **772650a** and **6a1927f** (both
before the battery code existed). Rule: random re-partitions of countries into 6 groups with the real-grouping
size structure; statistic = share of group × pair estimates negative and significant; pre-registered decision
threshold: the level relation is a global property if the random-repartition share is **≥ 0.80** and the change
share **≤ 0.10**; patchy if the real-group share differs from the random share by more than 2 random SDs.
Pre-registered minimum 800 partitions; the run extended to 13,800 in waves for the mandated load target, same
statistic, reported as an extension in the paper and the record.

## 3. Future-schooling placebo (Paper F §4.6)

Source: `research/corr-battery-2026-11-23`, `PRE_REGISTRATION.md` commit **6a1927f**. Rule: x measured at
t+10 predicting y at t, on the identical design cells as the correct-time relation; pre-registered decision
rule: if the future-schooling placebo's negative-significant share is **≥ 80%** of the correct-time share in the
identical cells, the level relation is declared a development-gradient association and not an identified
schooling effect; if the placebo share is below half the correct-time share, the level relation is more credible
as a timing-specific association.

## 4. Threshold shape (Paper F §7.4)

Source: same `corr-battery` pre-registration (threshold bootstrap: 500 country-clustered replications for the
spline with hinges at 6 and 9 years, four schooling measures). Hinge locations were fixed before estimation at
the conventional minimal/lower-secondary/upper-secondary boundaries; the paper grades the *shape* S and the
*hinge locations* C, because a data-driven hinge search would widen the intervals.

## 5. Synthesis sections that are not pre-registered

The DHS ecological gradient, the care/no-off-switch/tipping tests, and the transition engine are pre-registered
in their own records (`research/dhs-micro-2026-11-23` PRE_REGISTRATION.md; `research/care-credential-2026-11-23`
@ 7356e76, `policy-foreclosure-2026-11-23` @ 7ad44d5, `early-warning-2026-11-23` @ e12249b;
`research/transition-gpu-2026-11-23` pre-registration), not here. Nothing in this file pre-registers a new
analysis; it records which prior commit fixed which rule.
