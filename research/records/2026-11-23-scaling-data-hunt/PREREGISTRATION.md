# Pre-registration — retry blocked scaling data pulls (task-27)

Committed BEFORE any download result or fit. Branch `research/scaling-data-hunt-2026-11-23`,
record `research/records/2026-11-23-scaling-data-hunt/`. Compute on box2, 1–2 cores.

## Purpose

Four canonical scaling tests were blocked in task-19 only because their data could not be obtained:
Zipf/rank-size and Gibrat (city populations), Bettencourt urban scaling (city output), credential
inflation (credential vs occupation counts), gravity (bilateral migration + distance). This task
retries the pulls against alternative sources and runs the tests **only if usable data arrive**. If
a pull fails, the exact error is recorded and the test is declared unavailable — **no proxies**.

## Privacy/credentials

No credentials, keys or private registries are used. Only public downloads.

## Integrity checks applied to every download (before any use)

1. HTTP status and final URL recorded; redirect chain followed and logged.
2. File size compared with the provider's stated/expected size where known.
3. Archive integrity test (`unzip -t` / `python zipfile.testzip`) where the file is a zip.
4. Row/column counts and header names recorded; a minimum-row threshold declared per source below.
5. Plausible-range checks (populations > 0 and < 100 million per city; shares in [0,1]; counts
   non-negative integers; bilateral stock ≤ origin and destination populations).
6. A source is "usable" only if all checks pass; otherwise it is recorded as failed with the exact
   error, and the test is declared unavailable. No substitution of a different variable.

## Tests pre-registered for each data type (run only if the pull succeeds)

| test | data needed | specification | literature benchmark |
|---|---|---|---|
| Zipf / rank–size | city populations, one year, ≥50 cities per country | OLS log10(rank) = a − ζ log10(pop), per country; pooled with country fixed effects; cluster/bootstrap SE by country | ζ ≈ 1 |
| Gibrat | city populations, two waves ≥10 years apart, same city definitions | OLS of log population growth on log initial population; slope ≈ 0; SE clustered by country | slope ≈ 0 (independence) |
| Bettencourt urban output | city/metro output (GDP, wages, patents, income) + population | OLS log(output) = a + β log(pop) | socioeconomic β ≈ 1.15; infrastructure β ≈ 0.85 |
| Credential inflation | counts of distinct credential categories and detailed occupations over ≥5 years | growth rates of each; credential:occupation ratio; superlinearity test | ratio rises, not proportional |
| Gravity | bilateral migrant stock + bilateral distance + origin/destination size | PPML: stock = exp(a + b1 log(pop_o) + b2 log(pop_d) + b3 log(distance) + FE) | distance elasticity ≈ −1 to −2; size ≈ 1 |

Every estimated exponent will be reported with SE and n, beside its literature value. A replication
or a failure to replicate is reported plainly; identification is correlational, not causal.

## Attempt order (fixed in advance)

1. **City populations:** GeoNames `cities15000.zip` (resume, retries, browser UA) → `cities5000.zip`
   → `cities1000.zip` → `wget` resume of `cities15000.zip` → UN Data Portal API (search indicators
   for city/urban-agglomeration population, then pull the data) → UNdata city files → Eurostat
   cities API (`urb_lpop`) → US Census places → BEA metro areas → Atlas of Urban Expansion.
2. **Credential/occupation:** BLS SOC 2018 definitions (`soc_2018_definitions.xlsx`) and BLS OES
   national (`oesm23nat.zip`, plus earlier years for growth) → Credential Engine public registry
   endpoints (`credreg.net`, Credential Finder) → document gap if closed.
3. **Gravity:** UN DESA international migrant stock page (find xlsx link) → CEPII `dist_cepii.zip`
   and `geo_cepii` → run PPML if both usable.

A source is abandoned after two documented failures (or one hard failure: file corrupt after a
complete download) and the next source is tried. Sixty-minute budget; pulls are time-boxed so the
report is written even if the last source is still failing.
