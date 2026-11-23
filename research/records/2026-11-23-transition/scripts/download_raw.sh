#!/bin/bash
# Exact long-run downloads, run on box2 in /root/work/transition on 2026-11-23.
# Our World in Data grapher CSV exports. The browser user-agent is required for
# some hosts; it is the same trick that unblocked the UN downloads earlier.
set -euo pipefail
cd /root/work/transition
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
mkdir -p raw
SLUGS="child-mortality child-mortality-complete-gapminder child-mortality-igme life-expectancy
children-per-woman children-per-woman-un fertility-rate-with-projections crude-birth-rate
effective-fertility-rate-children-per-woman-who-are-expected-to-survive-until-childbearing-age
mean-years-of-schooling average-years-of-schooling literacy share-of-population-urban
gdp-per-capita-maddison-project-database infant-mortality"
for s in $SLUGS; do
  curl -sS -L -A "$UA" -o "raw/$s.csv" \
    "https://ourworldindata.org/grapher/$s.csv?v=1&csvType=full&useColumnShortNames=true"
  curl -sS -L -A "$UA" -o "raw/$s.metadata.json" \
    "https://ourworldindata.org/grapher/$s.metadata.json"
done
sha256sum raw/*.csv raw/*.json > raw/SHA256SUMS.txt
