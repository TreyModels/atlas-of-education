# Retried data pulls: two laws unlocked, three still blocked

**Task 27**, branch `research/scaling-data-hunt-2026-11-23`, 23 Nov 2026. **Pre-registration**
committed before any download (`5e0b11a`, `PREREGISTRATION.md`). Compute on box2, 1–2 cores, no
credentials, no proxies substituted for missing variables. A data source counts as usable only if
the pre-registered integrity checks pass; failures are recorded with the exact error and the test is
declared unavailable — nothing is proxied.

## Data-availability verdict

| source | URL tried | result | usable? |
|---|---|---|---|
| GeoNames city populations | `download.geonames.org/export/dump/cities15000.zip`, resumed `curl -C - --retry 5 -A browser` after 3 truncated pulls | HTTP 200, 3,369,122 bytes, `unzip -t` OK, 34,248 rows, sha256 `acdd89…` | **YES** |
| UN WUP city files | `population.un.org/wup/Download/Files/WUP2018-F22-Cities_Over_300K_Annual.xlsx` + alternates | HTTP 404 on all known paths | NO |
| UN Data Portal API | `population.un.org/dataportalapi/api/v1/indicators` | HTTP 200, 86 indicators, but city data only as "cities by size class" aggregates — no city-level list or panel | NO for these tests |
| BLS SOC 2018 definitions | `bls.gov/soc/2018/soc_2018_definitions.xlsx` | HTTP 403 Access Denied (419-byte error page) | NO |
| BLS OES | `download.bls.gov/pub/time.series/oe/` | HTTP 403 Access Denied | NO |
| Credential Engine registry | `credreg.net/registry/` | HTTP 403 Cloudflare challenge ("Just a moment…") | NO |
| BEA metro GDP / income | `apps.bea.gov/regional/zip/CAGDP1.zip`, `CAINC1.zip` | HTTP 000 connection failure | NO |
| CEPII distances | `cepii.fr/distance/dist_cepii.zip` | HTTP 200, 2,102,114 bytes, zip OK, `dist_cepii.xls` 8.1 MB (iso_o, iso_d, distw, contig, comlang_off) | **YES** |
| UN DESA bilateral migrant stock 2024 | `un.org/…/undesa_pd_2024_ims_stock_by_sex_destination_and_origin.xlsx` | HTTP 200, 6,005,287 bytes; Table 1 parsed, 9,035 country pairs | **YES** (with coverage caveat) |
| World Bank population 2024 | `api.worldbank.org` `SP.POP.TOTL` | HTTP 200, 266 rows | **YES** |

**Integrity evidence:** the bilateral stock pair matrix sums to **282 million**, against the published
world total of **281 million** (0.3% gap), so the extraction is coherent. Spot checks against UN
destination totals are lower (USA 48.3 vs 52.4 million, Germany 12.3 vs 16.1, Saudi Arabia 13.3 vs
13.7, Russia 7.3 vs 12.0, UK 8.0 vs 10.4) because the pair matrix puts some stock under region-level
or unknown origins; that gap is reported, not hidden. No pair exceeds the destination population.
Downloads that succeeded were checked by archive test, row/column counts and checksums (`pull_log.json`).

## (1) Fertility

**No fertility test was unlocked by this task.** The pulled data are city populations, bilateral
migration and distances; none of them measures fertility or female attainment. The fertility scaling
result therefore remains the task-19 finding: a common fertility–attainment shape does **not** collapse
across countries and cohorts (4,394 country–cohort points; country effects explain 72% of the residual;
slope-heterogeneity F = 46.4). Nothing here revises it.

## (2) Massification

**Zipf/rank–size: not rejected, with caveats.** From GeoNames (34,248 places; 22,465 cities in
**55 countries** with ≥50 cities; city-proper populations, not UN agglomerations), the per-country
rank–size exponent has median **ζ = 0.859**, bootstrap 95% CI **0.746–0.978**, IQR 0.647–1.237,
mean 1.142 (sd 1.147). Only 27% of countries lie inside 0.8–1.2. The Wilcoxon test against ζ = 1 does
not reject (p = 0.23), so **the data are consistent with Zipf's ~1**, but this is a weak test: GeoNames
is crowdsourced, lists localities rather than agglomerations, and only larger countries have 50+
towns above 15,000 people. A pooled country-fixed-effects estimate is much lower (ζ = 0.386,
cluster bootstrap CI 0.293–0.677) because it is dominated by large countries with many small towns;
it is reported but is not the primary statistic.

**Gibrat's law: not testable.** It needs two population waves for the same cities; GeoNames is one
vintage and the UN Data Portal offers no city-level panel. **Documented gap, not proxied.**

**Bettencourt urban scaling: not testable.** Both BEA regional archives failed (HTTP 000) and no city
GDP, wage, patent or infrastructure series is on the machine. The literature exponents (0.77–1.34)
were collated in the previous record; we cannot estimate them here.

**Credential inflation: not testable.** Both required sources are blocked (BLS 403 Access Denied;
Credential Engine 403 Cloudflare challenge). The 2,000:1 credential:occupation claim remains untested.

**Gravity: partial replication.** UN bilateral migrant stock 2024 × CEPII weighted distance,
**8,020 country pairs**, 195 origins × 187 destinations, 2024; PPML preferred because the stock matrix
is sparse, cluster SEs by destination. With origin and destination fixed effects (the standard
specification, which absorbs the size terms — see correction below), the **distance elasticity is
−0.970 (SE 0.076)**, against a literature range of about −1 to −2. Without fixed effects, distance is
−0.622 (SE 0.149), origin size +0.456 (SE 0.057), destination size +0.533 (SE 0.114), contiguity
+0.677, common language +0.603. OLS log-log fixed effects gives distance **−1.306 (SE 0.053)**
(no-FE: −1.130, SE 0.121; sizes +0.547 and +0.643). **Verdict: the distance decay is negative and of
the right order; the PPML estimate sits just at the edge of the literature band and the OLS estimate
inside it, but the size elasticities (~0.5) are below the standard ~1. A partial, correlational
replication — not a causal estimate.** Caveats: 2024 cross-section only, CEPII distances are
time-invariant, and some stock sits under unknown/region origins.

**Pre-registered specification correction (documented):** the pre-registration asked for PPML with
origin and destination fixed effects *and* size terms; those fixed effects absorb the size variables,
so both specifications are reported (FE: distance only; no-FE: distance and sizes). The pre-registration
otherwise held. A scaling regularity is not a causal identification.

## Files

`PREREGISTRATION.md`; `scripts/zipf.py` (rank–size), `scripts/gravity2.py` (clean gravity rebuild);
`results/zipf.json`, `results/zipf_countries.csv`, `results/gravity.json`, `results/pull_log.json`
(every URL, HTTP status, byte count, checksum, integrity verdict). Raw downloads stay on box2 under
`/root/work/datahunt/raw/` (largest 6 MB, checksums in `pull_log.json`).
