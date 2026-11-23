# Raw data sources (not committed; on box2 at /root/work/transition/raw)

All series are Our World in Data grapher exports downloaded on 23 Nov 2026 with a browser user-agent
(the same trick that unblocked www.un.org; see `scripts/download_raw.sh`). Raw CSVs total about 7 MB and
live on box2; the tidy derived panel committed here is `data/long_run_panel.csv`.

| series | chart citation (from the download's embedded metadata) |
|---|---|
| `average-years-of-schooling` | UNDP, Human Development Report (2025) |
| `birth-rate-total` | Human Mortality Database (2025) |
| `child-mortality` | Gapminder (2015); UN Inter-agency Group for Child Mortality Estimation (2025) |
| `child-mortality-complete-gapminder` | Gapminder (2015); UN Inter-agency Group for Child Mortality Estimation (2025) |
| `child-mortality-igme` | United Nations Inter-agency Group for Child Mortality Estimation (2025) |
| `children-per-woman` | UN, World Population Prospects (2024) |
| `children-per-woman-un` | UN, World Population Prospects (2024) |
| `fertility-rate-with-projections` | UN, World Population Prospects (2024) |
| `gdp-per-capita-maddison-project-database` | Bolt and van Zanden – Maddison Project Database 2023 |
| `infant-mortality` | United Nations Inter-agency Group for Child Mortality Estimation (2025) |
| `life-expectancy` | Riley (2005); Zijdeman et al. (2015); HMD (2025); UN WPP (2024) |
| `literacy` | UNESCO Institute for Statistics (2026) |
| `mean-years-of-schooling` | Barro and Lee (2015); Lee and Lee (2016) |
| `share-of-population-urban` | United Nations Department of Economic and Social Affairs, Population Division (2025) |

Download endpoint (per series):

```
https://ourworldindata.org/grapher/<series>.csv?v=1&csvType=full&useColumnShortNames=true
https://ourworldindata.org/grapher/<series>.metadata.json
```

The metadata JSONs (small) are committed under `data/owid_metadata/` so the chart citations and units are
reproducible without the raw CSVs. Larger raw files are not committed; re-download with `scripts/download_raw.sh`.

Unit notes: child mortality is under-5 deaths per 100 live births (OWID convention); life expectancy in years;
effective fertility in children per woman expected to survive to childbearing age; total fertility in births per
woman; mean years of schooling in years; income in 2011 international-$ (Maddison 2023); urban share in per cent.
