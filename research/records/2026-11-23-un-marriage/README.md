# UN World Marriage Data and living arrangements: the merge, its coverage, and the honest nulls

Worker `un-data`, branch `research/un-marriage-2026-11-23`, 23 Nov 2026. Scripts in `scripts/`, series + provenance in `data/`, model
outputs in `results/`; raw workbooks (26 MB + 2 MB) stay on the server — see `data/RAW_NOT_COMMITTED.md`.

**Short answer.** The UN data were obtained from the UN's own workbooks for 211 countries and turned into three marriage series
and three living-arrangement series with no interpolation. The honest core: the never-married share by 45-49 shows no significant
association with later fertility change and no stable sign (undetermined, not a clean null); school expansion did **not** predict
later marriage or more never-married women; the school → fertility edge itself is indistinguishable from zero with and without
country trends; living arrangements add nothing measurable (thin data). The one counterintuitive positive coefficient — later female
marriage age "predicting" a smaller future fertility fall — **did not survive the kill test** (it reverses sign when both sides are
changes) and is demoted to a robustness note. Marriage age is on the causal path and is **never a control** in school → fertility.

## Provenance, and which downloads failed

The reported blocker — "un.org returns 403" — is a **user-agent block, not an IP block**: the default `curl` user agent gets 403 from
`www.un.org`, a browser user agent gets 200. Exact call, run on the AutoDL **box1** server on 23 Nov 2026; box1 was retired later that evening (use `ssh autodl2`
now, where the same command in `scripts/download_raw.sh` works unchanged):

```
curl -sS -L -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" \
  -o undesa_pd_2019_wmd_marital_status.xlsx \
  "https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2019_wmd_marital_status.xlsx"
```

Used: **UN World Marriage Data 2019** (POP/DB/Marr/Rev2019), sheets `SMAM` (4,542 rows), `EVER_MARRIED` (55,832),
`MARITAL_STATUS_BY_AGE` (271,607; cross-check only); and the **UN Database on the Households and Living Arrangements of Older Persons
2026**, sheet `HHLA of Older Persons 2026` (9,338 rows; DHS, MICS, IPUMS-I, Demographic Yearbook). UN Data Portal `/api/v1/locations`
gave the M49 → ISO3 map. Citation and hashes in `data/RAW_NOT_COMMITTED.md` (UN material, CC BY 3.0 IGO).

Tried and did not give the needed series: **(a)** default-UA `un.org` — 403 (the reported blocker); **(b)** UN Data Portal API —
reachable but only 86 indicators, currently-married percentages only, no singulate mean age or never-married share; **(c)** Our World
in Data — reachable, but its mean-age-at-marriage chart is **OECD** (30 rich countries, 2001-2021), not the UN series, so cross-check
only; **(d)** World Bank — the mean-age-at-first-marriage WDI indicators are **retired** ("Invalid value"); **(e)** Zenodo refused
connection, archive.org timed out, HDX has no WMD package, DHS API not needed. **Not obtained:** Schulz et al. kinship intensity index
(ethnographic, not a time series) and WVS/EVS family-ties items — not done, not proxied.

## Coverage (`data/availability.csv`)

| series (file) | obs | countries | years | countries with 2+ obs |
|---|---|---|---|---|
| mean age at marriage, women (`smam_f`) | 2,073 | 210 | 1960-2019 | 207 |
| mean age at marriage, men (`smam_m`) | 1,848 | 209 | 1960-2019 | 201 |
| female-minus-male marriage-age gap (`smam_gap`) | 1,845 | 209 | 1960-2019 | 204 |
| never married by 45-49, women (`nevermar_f_4549`) | 2,060 | 211 | 1960-2019 | 207 |
| never married by 45-49, men (`nevermar_m_4549`) | 1,867 | 210 | 1960-2019 | 200 |
| 60+ living with children aged 20+ (`coresid_60plus`) | **705** | 143 | 1960-2025 | **129** |
| 60+ in a multi-generation household (`multigen_60plus`) | **674** | 138 | 1960-2025 | **124** |
| 60+ living alone (`alone_60plus`) | **968** | 174 | 1959-2025 | **159** |

Marriage observations by decade: 14 (1960s), ~280 (1970s), ~340 (1980s), ~400 (1990s), ~530 (2000s), ~500 (2010s). **Living
arrangements are thin and weak**: ~85% of rows fall in 1990-2020, from household- roster samples (DHS/MICS/IPUMS) with differing
age/household definitions; the co-residence test uses only 402 country-years in 70 countries. Those findings are weak, not
null-of-record. Year = mid-point of the UN survey window; raw years are in each `*_provenance.csv`. About one third of the marriage
rows are the UN's **model-based estimates** (753 of 2,439 source rows), not censuses/surveys; one falsifier drops them.

## (1) Fertility

**Units, exactly.** "Fertility" is the total fertility rate, births per woman (panel range 0.6-8.9). The estimator (reused from
`full_matrix_trends.py`) regresses the **ten-year change** in births per woman on the **level** of the marriage variable at the survey
year, with country fixed effects, decade effects, controls for the starting fertility level, income, urbanisation, and optionally a
straight-line trend per country; errors clustered by country.

**Killed: the positive "later marriage, smaller future decline" coefficient.** The level estimator gives +0.020 births per woman per
year of female marriage age (SE 0.006, n=1,698, 170 countries, with country trends) and it passes within-country permutation (p<0.005),
jackknife (+0.017 to +0.021), dropping UN model-based rows (+0.014) and logging income (+0.020). But it fails the test that matters:
put **changes on both sides** — change in births per woman over a real 8-13-year survey window on the change in marriage age over the
same window — and the coefficient is **−0.027 (SE 0.010, n=1,360, 196 countries, country effects, clustered errors)**: within a
country, when marriage age rose faster, fertility fell faster. The positive level coefficient is therefore a levels-vs-change artefact
(conditioning the ten-year change on the starting fertility level lets a temporary marriage-age deviation "regress back"), not a timing
effect. It is reported here as a robustness note only, not as a finding.

**The raw level pattern, plainly (asked for):** across countries, where marriage age is high, fertility is simply low — pooled
correlation −0.65, decade-fixed-effect slope −0.30 births per woman per year of marriage age (n=2,072). Decade means: 1960s 19.0 years
/ 6.46 births; 1970s 22.0 / 3.96; 1980s 23.6 / 3.31; 1990s 24.4 / 3.30; 2000s 24.9 / 3.00; 2010s 26.2 / 2.63. So the level association
is negative, as expected; the positive sign above only appeared conditional on the starting level and country trends.

**Undetermined: the never-married share and later fertility change.** The level coefficient is −0.0045 births per percentage point
(standard error 0.0027; n=1,684, 170 countries, with country trends) — not significant at conventional levels — but the tests do not
support treating it as exactly zero either: a within-country year shuffle gives p<0.005, while a **circular-shift permutation that
preserves each country's serial correlation gives p=0.08**, and the clustered interval is the primary inference. The sign is not
stable across specifications (without the starting-level control the coefficient is −0.011 ± 0.005; the change-on-change version is
+0.001 ± 0.005, n=1,346, 195 countries). Single consistent statement: **no significant association, not established as zero, sign
not robust — undetermined.**

**Provisional: a narrower female-minus-male marriage-age gap goes with a larger fall.** Level estimator −0.035 ± 0.016 (n=1,453, 156
countries, trends); change-on-change −0.097 ± 0.026 with country effects (n=1,194, 190 countries) — but the level sign flips to +0.018
± 0.019 when the starting-level control is removed, so it is not robust. Provisional.

**Null (weak data): living arrangements add nothing.** Share of 60+ living with adult children: +0.0021 ± 0.0022 births per
percentage point (402 rows, 70 countries, trends); multi-generation households the same. The interval rules out effects above ~0.004
births per point, but on 402 rows/70 countries this is a weak null (circular-shift permutation p=0.29 and year-shuffle p=0.23, both
consistent with no association; without the starting-level control +0.011 ± 0.004 — specification-dependent).

**The rule that matters.** Marriage age is on the causal path from schooling to fertility, so it is never a control in that regression;
nothing here estimates "the effect of schooling holding marriage age fixed". The marriage variables appear only as outcomes or as
associations of their own.

## (2) Massification

**Null: more secondary schooling did not predict later marriage.** With country trends, a one-point higher secondary enrolment share
goes with **0.036 years lower** subsequent change in women's mean marriage age over an 8-13-year window (SE 0.022; 95% interval −0.080
to +0.008; 435 country-window rows, 63 countries). Wrong sign, interval includes zero; without trends +0.0001 ± 0.009 (599 rows, 156
countries); lower-secondary completion −0.050 ± 0.027. Falsifier: within-country permutation of the marriage series across survey years
— p=0.22, i.e. shuffled years produce estimates at least this large a fifth of the time, so the point estimate is not distinguishable
from noise. Reading: no detectable positive link — not evidence that schooling shortens marriage.

**Null: more schooling did not predict more never-married women.** With trends −0.057 points of never-married share per point of
secondary enrolment ± 0.042 (428 rows, 63 countries); without trends +0.041 ± 0.025. Sign flips between specifications; permutation
p=0.53. Undetermined.

**Null: the school → fertility edge itself is indistinguishable from zero.** −0.0015 births per point of secondary enrolment ± 0.0016
with country trends (4,535 rows, 191 countries); −0.0022 ± 0.0018 without. This reproduces `results/full_matrix_trends_out.txt` from
the handoff run exactly (replication checked to seven decimal places). Adding marriage timing cannot rescue an edge that is already
null, and putting it on the right-hand side would violate the causal-path rule. So "do marriage-timing proxies add anything to
schooling → fertility?" — **no, and they cannot legitimately be used to answer it.**

Split-sample check (a split, not a control): school → fertility is −0.0037 ± 0.0026 in countries with a below-median never-married
share (2,554 rows) and +0.0002 ± 0.0021 above it (1,946 rows) — no effect hidden in one marriage regime. Sample-selection check: on the
rows where marriage data exist the school → fertility edge is −0.0018 ± 0.0020 (780 rows, 104 countries), the same null as on the whole
panel — so the marriage merge does not change the schooling conclusion either way.

## Falsifiers, per headline

**Permutation tests and their limitation.** The simple within-country permutation reshuffles the sparse series' values across survey
years at random. That destroys each country's serial correlation, so the null distribution is too narrow and the test **rejects too
easily** (anti-conservative) — the p<0.005 values in `results/results_falsifiers.json` must be read that way. We therefore also ran a
**circular-shift permutation** within country (`scripts/block_perm.py`, `results/results_block_perm.json`): the country's values keep
their order and spacing and only their alignment to calendar years rotates, which preserves serial correlation. Under that scheme:
never-married p=0.08 (the year-shuffle p<0.005 was an artefact of the broken autocorrelation), female marriage age p<0.005, gap
p=0.03, co-residence p=0.29 (consistent with its year-shuffle p=0.23 and with the null). Other falsifiers: drop-one-country
jackknife; dropping the UN's model-based estimate rows; income logged vs in levels (the handoff estimator used levels); the
**change-on-change test** that killed the positive level coefficient; removing the starting-fertility-level control (shows which
results are specification-dependent); and a cross-check of the never-married construction — 100 minus the ever-married share matches
the workbook's direct "Never married" tabulation on 459 country-years (median absolute difference 0.0 points, 90th percentile 0.2,
one 20.6-point outlier; `data/crosscheck_nevermar_f.csv`).

## What this does not support

No causal claim about marriage age and fertility. The male marriage-age series is built but untested. Living arrangements are
cross-sectional survey snapshots and thin. Kinship intensity and WVS/EVS items are not obtained and not proxied. The gap edge and the never-married results are not stable across specifications. The positive level coefficient is not a
finding.

## Files

`scripts/`: `download_raw.sh`, `extract_un.py` (workbook → series, availability, provenance), `edge_marriage.py` (estimator reuse),
`falsify.py`, `block_perm.py`, `robust_extra.py`, `nolevel_check.py`, `change_test.py`. `data/`: series JSONs, `*_provenance.csv`, `availability.csv`,
`source_composition.csv`, `crosscheck_nevermar_f.csv`; one-page plain-words summary `TOP5_PLAIN.md`. `results/`: `results_edges.json`, `results_falsifiers.json`,
`results_robust_extra.json`, `results_nolevel.json`, `results_change_test.json`, `results_block_perm.json`, run logs.
