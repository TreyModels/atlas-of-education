# 3. Data, measures, designs, and evidence standard

## 3.1 The panel

All cross-country analyses use the project's country-year panel, 1960–2024, observed values only. Series come
from the World Bank's World Development Indicators (income, urbanisation, sectoral measures), Barro–Lee
attainment (via OWID where the official tables were unreachable from the compute node), the project's
harmonised enrolment and completion series, and UN and national sources for fertility and mortality. No
imputation and no interpolation enter any estimation sample; the project's imputed panel exists for other
purposes and is not used here. Income enters in logs in every specification. Standard errors are clustered by
country throughout. The panel is unbalanced; every table reports the effective sample (country-years and
countries), not only the nominal one.

## 3.2 Measures

Fertility is the total fertility rate (births per woman). Schooling is measured eight ways: mean years of
schooling for women and for the total adult population; gross secondary enrolment; lower-secondary completion;
primary completion; tertiary enrolment; and gender-parity indices for secondary and tertiary enrolment. The
multiplicity is deliberate: the literature disagrees about the right measure, and the paper's claim is that the
level-of-analysis result is not an artefact of that disagreement. All eight measures are negative-significant
in levels and weak or positive in changes.

## 3.3 The two designs, kept distinct

**Levels.** Fertility level on schooling level, with decade and region fixed effects, log income and
urbanisation controls, all years. This design uses between-country variation and answers: do countries with more
schooling have fewer births?

**Ten-year changes.** The ten-year change in fertility on the starting level of schooling, with country fixed
effects, decade effects, country-specific linear trends, log income and urbanisation. This design uses
within-country variation, absorbs all time-invariant country characteristics, and answers: when a country's
schooling stock rose, did its fertility fall faster?

The paper treats these as estimates of different parameters, not as competing estimates of one parameter. That
is the whole argument in one sentence.

## 3.4 Auxiliary designs

**Specification curves.** Pre-registered grids (fixed-effect designs, control sets, lags, functional forms,
sample splits) with every cell reported. A result is "robust" only if its sign survives the reported grid.

**Re-partition transportability.** Random re-partitions of the panel's countries into groups of the substantive
grouping sizes; the relation is re-estimated within every group for every re-partition; the statistic is the
share of group-by-pair estimates that are negative and significant. This tests whether the relation is a global
property or a grouping artefact.

**Placebo designs.** A variable that cannot plausibly cause the outcome under the causal story is substituted
for the candidate cause: future schooling for current schooling; male care-work for female care-work;
manufacturing employment for care work. If the placebo is as strong as the candidate, the candidate's
association is not identified.

## 3.5 Pre-registration and the claim-to-source map

Every workstream was pre-registered before its analysis code ran: specification grid, sample splits, bootstrap
counts, and decision thresholds were committed to the branch before the runs, and the paper cites the commits.
The rules used in this paper are compiled, with their provenance commits, in `PREREGISTRATION.md` on this record
(a dated compilation, not a new pre-registration).
Every number traces to a record path (branch @ commit, file, field) in `data/claims_sources.csv`; each record's
README states its deviations (unreachable sources, estimable-cell counts, load-driven extensions) rather than
hiding them. The synthesis's conventions: bold in tables means |t| > 1.96; "significant" means the
country-clustered standard error implies |t| > 1.96 unless stated; "negative-significant share" means the share
of specifications or groups with coefficient < 0 and |t| > 1.96; "survives" means the result holds across the
reported specification space, not that it is causally identified.

## 3.6 Evidence grades

Claims carry **S** (survives the reported specification space and its designed falsifiers), **F** (contradicted
by the reported evidence), or **C** (cannot be tested with these data, with the missing observation named). The
grades are the mechanism by which an omnibus paper avoids the omnibus temptation to make everything sound like
it worked; they are applied in the verdict table of Section 8.
