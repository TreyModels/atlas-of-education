#!/bin/bash
# Fresh data pull (box2 down): World Bank WDI annual 1960-2023 + UN Data Portal indicators list.
set -u
cd "$(dirname "$0")/../data"
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890
INDICATORS="SP.DYN.TFRT.IN SP.DYN.LE00.FE.IN SP.DYN.IMRT.IN SP.URB.TOTL.IN.ZS NY.GDP.PCAP.PP.KD SE.SEC.CUAT.LO.FE.ZS SE.SEC.CUAT.UP.FE.ZS SP.POP.TOTL"
for ind in $INDICATORS; do
  curl -s -m 120 "https://api.worldbank.org/v2/country/all/indicator/${ind}?format=json&per_page=25000&date=1960:2023" -o "wdi_${ind}.json" -w "${ind} http=%{http_code} size=%{size_download}\n"
done
# UN Data Portal: indicators list (search for total fertility / cohort fertility later)
curl -s -m 90 "https://population.un.org/dataportalapi/api/v1/indicators?format=json&pageSize=200&pageNumber=1" -o unp_indicators.json -w "unp_indicators http=%{http_code} size=%{size_download}\n"
