#!/bin/bash
# Exact data downloads for task 15, run on box2 in /root/work/corr_rebuild on 2026-11-23.
# Our World in Data grapher exports, downloaded with a browser user-agent.
set -euo pipefail
cd /root/work/corr_rebuild
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
mkdir -p raw
for s in mean-years-of-schooling average-years-of-schooling-males-vs-females \
         gender-ratios-for-mean-years-of-schooling cohort-fertility-rate children-per-woman-un; do
  curl -sS -L -A "$UA" -o "raw/$s.csv" \
    "https://ourworldindata.org/grapher/$s.csv?v=1&csvType=full&useColumnShortNames=true"
done
# Project panel (already on box2): /root/work/data
#   fertility, prm_cmp, sec, lsc, ter, gpi_sec, gpi_ter, gdppc_log (levels -> log), urban, meta.json
