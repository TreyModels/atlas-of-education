#!/bin/bash
# Exact downloads for the UN marriage / living-arrangement data, run on the
# AutoDL server in /root/work/undata on 2026-11-23.
#
# KEY FINDING: www.un.org and population.un.org return HTTP 403 to the default
# curl user-agent but HTTP 200 to a normal browser user-agent.  Without -A the
# raw-file links below fail; with it they download.  (population.un.org's
# /dataportalapi API answers 200 either way; www.un.org does not.)
set -euo pipefail
cd /root/work/undata
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
mkdir -p raw logs

# 1. UN World Marriage Data 2019 (POP/DB/Marr/Rev2019), all four indicators.
curl -sS -L -A "$UA" -o raw/undesa_pd_2019_wmd_marital_status.xlsx \
  "https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2019_wmd_marital_status.xlsx"

# 2. UN Database on the Households and Living Arrangements of Older Persons 2026.
curl -sS -L -A "$UA" -o raw/undesa_pd_2026_living-arrangements-older-persons.xlsx \
  "https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2026_living-arrangements-older-persons.xlsx"

# 3. Companion household size/composition file (2026), used only for context.
curl -sS -L -A "$UA" -o raw/undesa_pd_2026_hh-size-composition.xlsx \
  "https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2026_hh-size-composition.xlsx"

# 4. UN Data Portal location table: numeric M49 code -> ISO3 (300 locations).
for p in 1 2; do
  curl -sS -L -A "$UA" -o raw/un_locations_$p.json \
    "https://population.un.org/dataportalapi/api/v1/locations?pageNumber=$p&pageSize=200"
done

# 5. OWID grapher CSV exports (used only as cross-checks / fallbacks; the UN
#    World Marriage Data xlsx above is the primary source).
curl -sS -L -A "$UA" -o raw/owid_women-married-by-age-18.csv \
  "https://ourworldindata.org/grapher/women-married-by-age-18.csv?v=1&csvType=full&useColumnShortNames=true"
curl -sS -L -A "$UA" -o raw/owid_share-of-women-married-or-in-a-union.csv \
  "https://ourworldindata.org/grapher/share-of-women-married-or-in-a-union.csv?v=1&csvType=full&useColumnShortNames=true"

sha256sum raw/*.xlsx raw/*.json raw/*.csv > raw/SHA256SUMS.txt 2>/dev/null || true
ls -la raw/
