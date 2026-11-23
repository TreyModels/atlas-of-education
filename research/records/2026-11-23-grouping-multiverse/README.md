# Grouping multiverse, 23 Nov 2026

**Idea:** split the countries into groups in many different ways, rerun the whole within-country lead-lag matrix inside every group, and see which links hold across groupings, and which only hold in particular kinds of country. Random splits with the same group sizes are the yardstick for "what chance alone gives you".

Everything was run on the rented server (`/root/work/groups/`); scripts and results are copied here. Raw replicate file (42 MB, `final75.pkl`) is not committed; it sits in the session scratchpad and can be regenerated with the scripts.

## What was run
- **Estimator:** the corrected matrix from the recompute branch (17 measures, change over the next ten years, country effects, decade effects, clustered errors, controls for income and urbanisation; with and without a straight-line trend per country). Income is logged here (the stored file holds levels). The whole-sample run reproduces the earlier matrix almost exactly: 127 links significant with country effects (same), 43 with trends (earlier 42), 26 in both (earlier 24); the small gap comes from partialling out the country trend once per country instead of with dummy columns.
- **50 groupings in 8 families, 179 groups:** geography (World Bank region, continent, World Bank income group); income (halves to fifths of 1990 income); demography (1990 birth rate cut 2 to 5 ways, 1990 child mortality, 1990 life expectancy, timing of crossing replacement fertility, two cuts); schooling (1990 secondary and lower-secondary completion); economy (farm share of output, urban share, farm share of jobs, electricity access); institutions (tax share); k-means on a 1990 profile for 2 to 6 clusters; grouped fixed effects (Bonhomme-Manresa style) on the birth-rate trajectory and on the income trajectory, 2 to 6 classes each.
- **Rule for every group:** at least 10 countries and 150 rows, otherwise the link is not estimated there.
- **Random yardstick:** 74 random re-partitions of the same countries into groups of the same sizes (different cuts of one measure share one random ordering, so the nesting is kept). Planned 400; stopped at 75 because the shared server was slow. Because 74 is few, p-values use a normal approximation to the random distribution, and all multiple-testing correction is Benjamini-Hochberg at 5 percent across the 272 links (and across all group-by-link tests for the "where it holds" claims).
- **Total regressions run: 7,185,790** (about 96 thousand per full pass over the real groups, 74 random passes, plus the whole-sample reference).

## How to read the verdicts
For each link we count the share of groups where it is significant with the same sign as in the whole sample (family-balanced: each family counts once), separately with country effects and with country trends, and compare with the same share in random groups.
- A link that is **really the same everywhere** looks the same in real and random groups, because a random slice of a uniform effect shows the uniform effect (just with less power). So "robust everywhere" requires: significant in the whole sample in both versions, significant in at least half the groups with trends, at least a quarter in every family, and no more sign flipping than random groups.
- A link that is **group-specific** has real groups beating random groups at some kind of group, with the same sign, mean z of at least 2, and half the groups significant, correct at 5 percent false discovery.
- **No better than random**: neither of the above, and not beating the random groups.
- Caution: in small groups (10 to 30 countries) clustered errors are optimistic, so single-group claims (one region, one income class) are the weakest ones. Claims that recur across several nested cuts are stronger.

## Headline numbers
- 43 of 272 links beat the random groupings with trends (43 with country effects only, 27 in both), and 21 do worse than random groups (an effect that lives in the whole sample but is thinner in any slice).
- 36 links show more sign flipping across groups than random groups do.
- Of the 24 links that survived country trends in the earlier matrix, only **5** are robust in every kind of grouping (income to urbanisation, farm share to income, child mortality to life expectancy, and the two fertility links below); 5 are group-specific; **14 are no better than random** (a real pooled effect that does not show up consistently in slices).

## (1) Fertility
**Robust everywhere:** child mortality leading to the birth rate (significant in 95 percent of groups with trends), and life expectancy leading to the birth rate (81 percent). Both are also in the earlier list. These are the only two fertility links that hold in nearly every kind of country.

**Hold only in specific kinds of country:**
- The birth rate leading to later income (negative) is concentrated in the lowest-birth-rate trajectory class (countries whose birth rate fell earliest and furthest), not in the rest; in the earlier matrix this link looked general.
- Birth rate leading to secondary completion is concentrated in the high-birth-rate clusters.
- More urbanisation leading to fewer births holds in the low-birth-rate groups (the late stage), not early on.
- Birth rate leading to farm share of output and farm share of jobs: nothing in the whole sample with trends, but strong in the low-birth-rate, high-electricity, high-income groups (that is where falling births go with a shrinking farm sector). Birth rate leading to life expectancy: only among early crossers and low-birth-rate countries.
- Primary completion leading to births changes sign: negative in the early and low-birth-rate groups, positive in the highest-income trajectory class.
- Higher-education leading to births, and farm share of output leading to births, beat the random groups but are not tied to any one kind of group.

**No better than random (13 links), including several earlier survivors:** birth rate leading to lower-secondary completion and to electricity and to primary completion. These are real in the whole sample but are weak and patchy in groups.

## (2) Massification (drivers of schooling expansion)
**Nothing is robust everywhere** among the drivers the project is chasing.
- **Electricity:** large and positive with country effects in the whole sample (t about 4 to 6 for lower-secondary, secondary, primary, gender parity), but with country trends it is zero in the whole sample and in almost every group (significant in 6 to 16 percent of groups, versus 3 to 6 percent for random groups). Where it holds it is specific: lower-secondary completion in the low-birth-rate trajectory class. Electricity also has the most sign-flipping of any driver: its links to schooling and to income, urbanisation and child mortality flip sign across income and trajectory groupings (for the high-income classes the sign reverses), so electricity is a weak, group-dependent driver once country trends are allowed.
- **Paid jobs (wage employment):** no link to any schooling outcome beats random groups, in the whole sample or in any kind of group. This is the clearest null.
- **Farm change:** farm share of output leading to higher education beats random groups (concentrated in the low-birth-rate and low-child-mortality groups); farm share leading to lower-secondary completion holds in Latin America (single region, weakest evidence). Farm share of jobs is no better than random for schooling.
- **Urbanisation and income leading to secondary completion** (both earlier survivors): significant in the whole sample with trends but no better than random groups, i.e. patchy in slices.
- **Group-specific, and also earlier survivors:** primary completion leading to gender parity in secondary (holds in the high-birth-rate groups and classes); child mortality leading to gender parity in higher education (early crossers).
- Child mortality leading to higher education has the opposite sign with trends than with country effects and holds in cities-heavy, low-farm, high-income groups.

## Things that disagree with the earlier matrix
- Only 5 of its 24 trend survivors hold in every kind of grouping; the rest are weaker in slices than the whole-sample count implies.
- Links with no whole-sample effect with trends can be strong in the right group (births to farm share and farm jobs; farm share to higher education), so the whole-sample matrix hides group-specific structure.
- Electricity and schooling: the earlier note says it is "real with country effects, not separable from a country trend"; this run adds that the country-effects result is itself group-dependent.

## Files
`scripts/gm_core.py` (panel, groupings, fast estimator), `scripts/run_multiverse.py` (real and random passes), `scripts/analyse.py` (verdicts); `results/summary.txt` (full text, sorted by topic), `results/edge_table.csv` (all 272 links: whole-sample estimates, shares vs random, corrected p-values, groups where it holds, verdict), `results/cells_real.csv.gz` (every group-by-link estimate), `results/groupings.csv`, `results/base_survivors.txt`, `results/run.log`.
