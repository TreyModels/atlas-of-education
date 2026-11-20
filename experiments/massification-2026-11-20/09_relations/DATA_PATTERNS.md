# DATA_PATTERNS — panel, event-window and gradient estimates (09_relations)

**Author:** `pattern-scout` · 2026-11-20 · task-21 · P4-conditional relations layer.

**Data:** observed cells only. Panel = WDI live API pull (30 countries × 1970–2024, 45 indicators), archived in `raw/wdi/` and assembled in `data/panel_wdi_wide.csv`. Shadow numbers are the observed survey values already on disk in `04_data/shadow_round2/`. No imputed cell is used as an observation.

**Panel coverage:** 1650 country-years; 30 countries; 1970–2024. Countries: CHN, HKG, KHM, PHL, KOR, JPN, VNM, THA, IDN, MYS, SGP, MMR, LAO, MNG (Asia) + IND, BGD, PAK, LKA, NPL, TUR, MEX, BRA, EGY, NGA, KEN, ZAF, PER, COL, MAR, UKR.

**Method.** Two-way fixed effects (country + year) by alternating projections, OLS on within-transformed data, CR1 cluster-robust SE clustered on country. `levels-two-way-FE` = y on x with country and year FE; `first-difference` = Δy on Δx, which removes country-specific trends. Every result below is reproducible: `scripts/fetch_wdi_parallel.sh` → `scripts/build_panel.py` → `scripts/analyze_panel.py` → `scripts/analyze_hetero_events.py`.

> **Identification warning, stated once for the whole file.** These are panel associations, not experiments. Country and year FE remove fixed differences and common shocks; they do **not** remove reverse causality, omitted time-varying confounders (reform packages, aid cycles, regime change), or measurement change in UIS/WDI series. Only R07 (fertility→completion) is graded plausibly-causal, and only because the timing ordering is structural. Everything else is correlational.

## 1. Panel estimates (two-way FE)

| spec | outcome | driver | lag_years | coef | se | t | p | n | n_cty | period | within_r2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 | ger s | spend gdp | 0 | 0.1524 | 0.1101 | 1.3843 | 0.1663 | 661 | 30 | 1971-2024 | 0.0362 |
| S01 | ger s | spend gdp | 5 | 0.1108 | 0.0649 | 1.7076 | 0.0877 | 511 | 30 | 1976-2024 | 0.0248 |
| S02 | ger p | spend gdp | 0 | 0.0459 | 0.0565 | 0.8126 | 0.4165 | 702 | 30 | 1971-2024 | 0.0085 |
| S02 | ger p | spend gdp | 5 | 0.0215 | 0.0502 | 0.4275 | 0.6690 | 552 | 30 | 1976-2024 | 0.0022 |
| S03 | ger t | spend gdp | 0 | 0.0601 | 0.0549 | 1.0944 | 0.2738 | 624 | 30 | 1971-2024 | 0.0057 |
| S03 | ger t | spend gdp | 5 | -0.0242 | 0.0189 | -1.2841 | 0.1991 | 478 | 29 | 1976-2024 | 0.0018 |
| S04 | cmpt s | spend gdp | 0 | 0.1637 | 0.1222 | 1.3394 | 0.1804 | 435 | 27 | 1971-2024 | 0.0511 |
| S04 | cmpt s | spend gdp | 5 | 0.0174 | 0.0296 | 0.5896 | 0.5554 | 301 | 25 | 1979-2024 | 0.0012 |
| S05 | cmpt p | spend gdp | 0 | 0.0884 | 0.0608 | 1.4545 | 0.1458 | 463 | 27 | 1971-2024 | 0.0225 |
| S05 | cmpt p | spend gdp | 5 | -0.0247 | 0.0320 | -0.7705 | 0.4410 | 330 | 25 | 1977-2024 | 0.0027 |
| S06 | uner p | spend gdp | 0 | -0.3446 | 0.3897 | -0.8842 | 0.3766 | 458 | 30 | 1971-2024 | 0.0040 |
| S06 | uner p | spend gdp | 5 | -0.0097 | 0.4100 | -0.0237 | 0.9811 | 317 | 27 | 1979-2024 | 0.0000 |
| S07 | ptr p | spend gdp | 0 | 0.0059 | 0.0539 | 0.1087 | 0.9134 | 578 | 29 | 1971-2019 | 0.0001 |
| S07 | ptr p | spend gdp | 5 | -0.0347 | 0.0723 | -0.4806 | 0.6308 | 433 | 28 | 1976-2019 | 0.0033 |
| S08 | ger s | gdppc | 0 | 0.0904 | 0.1238 | 0.7304 | 0.4651 | 1042 | 30 | 1970-2024 | 0.0134 |
| S08 | ger s | gdppc | 5 | 0.1542 | 0.0806 | 1.9127 | 0.0558 | 892 | 30 | 1975-2024 | 0.0464 |
| S09 | ger t | gdppc | 0 | 0.8482 | 0.1719 | 4.9347 | 0.0000 | 1037 | 30 | 1970-2024 | 0.2656 |
| S09 | ger t | gdppc | 5 | 0.6272 | 0.1849 | 3.3915 | 0.0007 | 887 | 30 | 1975-2024 | 0.2047 |
| S10 | cmpt s | gdppc | 0 | 0.2468 | 0.1188 | 2.0776 | 0.0377 | 629 | 28 | 1970-2024 | 0.0646 |
| S10 | cmpt s | gdppc | 5 | 0.1337 | 0.0844 | 1.5834 | 0.1133 | 490 | 27 | 1975-2024 | 0.0413 |
| S11 | ger s | urb | 0 | 0.0105 | 0.0044 | 2.3683 | 0.0179 | 1069 | 30 | 1970-2024 | 0.0921 |
| S11 | ger s | urb | 5 | 0.0083 | 0.0049 | 1.7056 | 0.0881 | 919 | 30 | 1975-2024 | 0.0753 |
| S12 | cmpt s | remit | 0 | -0.0068 | 0.0316 | -0.2147 | 0.8300 | 573 | 27 | 1971-2024 | 0.0008 |
| S12 | cmpt s | remit | 5 | 0.0024 | 0.0269 | 0.0896 | 0.9286 | 441 | 25 | 1980-2024 | 0.0002 |
| S13 | cmpt p | tfr | 0 | -0.1893 | 0.0436 | -4.3445 | 0.0000 | 712 | 28 | 1970-2024 | 0.2585 |
| S13 | cmpt p | tfr | 5 | -0.0978 | 0.0253 | -3.8656 | 0.0001 | 572 | 28 | 1976-2024 | 0.2138 |
| S14 | ger s | priv s | 0 | 0.0752 | 0.0205 | 3.6622 | 0.0003 | 431 | 29 | 1998-2024 | 0.0874 |
| S14 | ger s | priv s | 5 | 0.0517 | 0.0501 | 1.0321 | 0.3020 | 292 | 25 | 2003-2024 | 0.0316 |
| S15 | ger t | priv t | 0 | 0.1773 | 0.1068 | 1.6600 | 0.0969 | 379 | 30 | 1998-2019 | 0.0402 |
| S15 | ger t | priv t | 5 | 0.0164 | 0.0717 | 0.2286 | 0.8192 | 234 | 28 | 2003-2019 | 0.0007 |
| S16 | ger p | priv p | 0 | -0.0107 | 0.0116 | -0.9218 | 0.3567 | 834 | 30 | 1970-2024 | 0.0253 |
| S16 | ger p | priv p | 5 | -0.0038 | 0.0084 | -0.4556 | 0.6487 | 684 | 29 | 1975-2024 | 0.0062 |
| S17 | cmpt s | ptr p | 0 | 0.2788 | 0.2413 | 1.1553 | 0.2480 | 442 | 28 | 1970-2019 | 0.0172 |
| S17 | cmpt s | ptr p | 5 | 0.3849 | 0.1089 | 3.5352 | 0.0004 | 309 | 25 | 1978-2019 | 0.1269 |
| S18 | ger p | tch p | 0 | 0.4033 | 0.0798 | 5.0536 | 0.0000 | 1052 | 30 | 1970-2024 | 0.2926 |
| S18 | ger p | tch p | 5 | 0.1833 | 0.0547 | 3.3512 | 0.0008 | 902 | 30 | 1975-2024 | 0.1091 |
| S19 | ger s | tch s | 0 | 0.3831 | 0.0899 | 4.2608 | 0.0000 | 822 | 30 | 1970-2024 | 0.2240 |
| S19 | ger s | tch s | 5 | 0.0591 | 0.0644 | 0.9183 | 0.3585 | 672 | 29 | 1975-2024 | 0.0088 |
| S20 | ger s | voc share | 0 | -0.0151 | 0.0090 | -1.6728 | 0.0944 | 835 | 29 | 1970-2019 | 0.0796 |
| S20 | ger s | voc share | 5 | -0.0043 | 0.0059 | -0.7279 | 0.4667 | 692 | 28 | 1975-2019 | 0.0095 |
| S21 | growth | ger t | 10 | -0.6912 | 0.7731 | -0.8941 | 0.3713 | 735 | 30 | 1981-2024 | 0.0073 |
| S21 | growth | ger t | 15 | -1.0347 | 0.2400 | -4.3117 | 0.0000 | 596 | 27 | 1986-2024 | 0.0193 |
| S22 | growth | ger s | 10 | 0.2166 | 1.2885 | 0.1681 | 0.8665 | 742 | 28 | 1980-2024 | 0.0002 |
| S22 | growth | ger s | 15 | -0.8079 | 0.8787 | -0.9195 | 0.3578 | 609 | 26 | 1985-2024 | 0.0024 |
| S23 | gdppc | urb | 0 | 0.0084 | 0.0082 | 1.0288 | 0.3036 | 1589 | 30 | 1970-2024 | 0.0309 |
| S24 | spend gdp | tax gdp | 0 | 0.4062 | 0.1674 | 2.4256 | 0.0153 | 528 | 26 | 1972-2024 | 0.0251 |
| S25 | ger s | neet | 0 | -0.0009 | 0.0025 | -0.3771 | 0.7061 | 343 | 29 | 1970-2024 | 0.0013 |
| S25 | ger s | neet | 5 | -0.0033 | 0.0041 | -0.8094 | 0.4183 | 212 | 21 | 2001-2024 | 0.0229 |
| S26 | ger s | internet | 0 | 0.0499 | 0.0160 | 3.1210 | 0.0018 | 691 | 30 | 1990-2024 | 0.0910 |
| S26 | ger s | internet | 5 | 0.0130 | 0.0115 | 1.1311 | 0.2580 | 541 | 30 | 1995-2024 | 0.0201 |
| S27 | cmpt s | spend gb | 0 | 0.0112 | 0.0132 | 0.8463 | 0.3974 | 393 | 25 | 1980-2024 | 0.0062 |
| S27 | cmpt s | spend gb | 5 | 0.0072 | 0.0053 | 1.3523 | 0.1763 | 271 | 22 | 1986-2024 | 0.0226 |
| S28 | ger s | xpd prim pc | 0 | -0.0333 | 0.0406 | -0.8202 | 0.4121 | 229 | 27 | 1997-2018 | 0.0068 |
| S28 | ger s | xpd prim pc | 5 | -0.0038 | 0.0580 | -0.0654 | 0.9478 | 118 | 16 | 2003-2018 | 0.0001 |
| S29 | cmpt p | agri | 0 | 0.0616 | 0.2367 | 0.2602 | 0.7947 | 551 | 28 | 1991-2024 | 0.0015 |
| S29 | cmpt p | agri | 5 | 0.0914 | 0.0558 | 1.6393 | 0.1012 | 411 | 27 | 1996-2024 | 0.0095 |
| S30 | ger s | sec durs | 0 | -0.3984 | 0.3499 | -1.1386 | 0.2549 | 1069 | 30 | 1970-2024 | 0.0185 |

## 2. First differences (country-trend-free check)

| spec | coef | se | t | p | n | n_cty | period | within_r2 |
|---|---|---|---|---|---|---|---|---|
| S01-FD | 0.0144 | 0.0756 | 0.1904 | 0.8490 | 631 | 30 | 1972-2024 | 0.0006 |
| S02-FD | -0.0177 | 0.0184 | -0.9595 | 0.3373 | 672 | 30 | 1972-2024 | 0.0011 |
| S04-FD | 0.0787 | 0.1175 | 0.6698 | 0.5030 | 408 | 27 | 1972-2024 | 0.0071 |
| S08-FD | 0.3687 | 0.1499 | 2.4594 | 0.0139 | 1012 | 30 | 1971-2024 | 0.0988 |
| S11-FD | -0.0126 | 0.0138 | -0.9076 | 0.3641 | 1039 | 30 | 1971-2024 | 0.0203 |
| S17-FD | -1.2429 | 0.3183 | -3.9049 | 0.0001 | 414 | 28 | 1972-2019 | 0.1913 |
| S18-FD | 0.3224 | 0.0728 | 4.4303 | 0.0000 | 1022 | 30 | 1971-2024 | 0.1540 |
| S24-FD | -0.2016 | 0.2879 | -0.7003 | 0.4837 | 502 | 24 | 1973-2024 | 0.0020 |
| S26-FD | 0.0101 | 0.0099 | 1.0231 | 0.3063 | 661 | 30 | 1991-2024 | 0.0116 |

### How to read the two tables

- **The spending→enrolment channel is weak in levels and absent at primary.** S01 secondary GER elasticity 0.111
  (se 0.065) at a 5-year lag; S02 primary GER 0.021 (se 0.050); the first-difference versions are ~0
  (S01-FD 0.014, se 0.076). This is the honest bottom line: at 30-country FE, public spending does not buy
  measurable enrolment except in the Asia / low-enrolment splits below.
- **Income→tertiary is the strongest relation in the panel**: S09 0.848 (se 0.172). Income→secondary is weaker
  and lagged (S08 0.154, p=0.056; FD 0.369, p=0.014) — effects appear with a 5-year lag, consistent with the
  schooling pipeline.
- **Fertility→primary completion is the most robust relation in the file**: S13 −0.189 (se 0.044) at L0 and
  −0.098 (se 0.025) at L5, holding in every split. Cohort size suppresses completion.
- **The pupil-teacher ratio result has a sign conflict and is reported as not identifiable.** Levels say +0.385
  (higher PTR ↔ higher completion, i.e. an enrolment boom raises PTR first), first differences say −1.243
  (se 0.318): tightening teacher supply per pupil hurts completion. Both are in `data/panel_results.csv`; do
  not use either as a parameter.
- **Education→growth rejects the model's positive `eps_ec`.** S21: log GDP growth on tertiary GER 15 years
  earlier = −1.035 (se 0.240). This is not a causal estimate, but it is a direct failure of the "more
  tertiary → faster growth" prior that the two-way module assumes (eps_ec > 0 in 8 of its 10 regimes).
- **Teacher stocks co-move mechanically with enrolment** (S18 0.403, se 0.080; FD 0.322). Treated as a capacity
  constraint, not a behavioural parameter.

## 3. Heterogeneity — where a relation holds and where it fails

**spending→secondary GER** (`log_ger_s` ~ `log_spend_gdp`)

| group_type | group | coef | se | t | p | n | n_cty |
|---|---|---|---|---|---|---|---|
| region | Asia | 0.1894 | 0.0896 | 2.1141 | 0.0345 | 324 | 19 |
| region | non-Asia | 0.0099 | 0.1058 | 0.0937 | 0.9253 | 187 | 11 |
| income_grp | low-income-1990 | 0.1246 | 0.0919 | 1.3560 | 0.1751 | 249 | 15 |
| income_grp | high-income-1990 | 0.1459 | 0.1010 | 1.4440 | 0.1487 | 262 | 15 |
| bursary_grp | low-tax-capacity | 0.0454 | 0.0520 | 0.8737 | 0.3823 | 284 | 20 |
| bursary_grp | high-tax-capacity | 0.1059 | 0.0792 | 1.3371 | 0.1812 | 227 | 10 |
| urb_grp | low-urban | 0.1545 | 0.0966 | 1.6001 | 0.1096 | 285 | 15 |
| urb_grp | high-urban | 0.0392 | 0.1007 | 0.3887 | 0.6975 | 226 | 15 |
| base_ger | GER-low-1990 | 0.1320 | 0.0720 | 1.8326 | 0.0669 | 276 | 17 |
| base_ger | GER-high-1990 | 0.0768 | 0.0445 | 1.7275 | 0.0841 | 235 | 13 |

**income→tertiary GER** (`log_ger_t` ~ `log_gdppc`)

| group_type | group | coef | se | t | p | n | n_cty |
|---|---|---|---|---|---|---|---|
| region | Asia | 1.0746 | 0.2191 | 4.9046 | 0.0000 | 688 | 19 |
| region | non-Asia | 0.2807 | 0.4748 | 0.5911 | 0.5544 | 349 | 11 |
| income_grp | low-income-1990 | 0.8461 | 0.2571 | 3.2914 | 0.0010 | 576 | 15 |
| income_grp | high-income-1990 | 0.6972 | 0.1557 | 4.4788 | 0.0000 | 461 | 15 |
| bursary_grp | low-tax-capacity | 0.6813 | 0.2242 | 3.0392 | 0.0024 | 650 | 20 |
| bursary_grp | high-tax-capacity | 1.0280 | 0.2875 | 3.5756 | 0.0003 | 387 | 10 |
| urb_grp | low-urban | 0.8564 | 0.2600 | 3.2938 | 0.0010 | 581 | 15 |
| urb_grp | high-urban | 0.7139 | 0.2758 | 2.5885 | 0.0096 | 456 | 15 |
| base_ger | GER-low-1990 | 0.6801 | 0.2521 | 2.6972 | 0.0070 | 557 | 17 |
| base_ger | GER-high-1990 | 0.9616 | 0.2522 | 3.8123 | 0.0001 | 480 | 13 |

**private share→secondary GER** (`log_ger_s` ~ `log_priv_s`)

| group_type | group | coef | se | t | p | n | n_cty |
|---|---|---|---|---|---|---|---|
| region | Asia | 0.0864 | 0.0164 | 5.2834 | 0.0000 | 248 | 18 |
| region | non-Asia | 0.0026 | 0.1113 | 0.0235 | 0.9812 | 183 | 11 |
| income_grp | low-income-1990 | 0.0809 | 0.0181 | 4.4667 | 0.0000 | 158 | 14 |
| income_grp | high-income-1990 | 0.0140 | 0.0844 | 0.1655 | 0.8685 | 273 | 15 |
| bursary_grp | low-tax-capacity | 0.1016 | 0.0183 | 5.5641 | 0.0000 | 269 | 19 |
| bursary_grp | high-tax-capacity | -0.0651 | 0.0811 | -0.8030 | 0.4220 | 162 | 10 |
| urb_grp | low-urban | 0.0952 | 0.0141 | 6.7593 | 0.0000 | 166 | 14 |
| urb_grp | high-urban | 0.0532 | 0.0428 | 1.2445 | 0.2133 | 265 | 15 |
| base_ger | GER-low-1990 | 0.0840 | 0.0213 | 3.9357 | 0.0001 | 191 | 16 |
| base_ger | GER-high-1990 | 0.0255 | 0.0488 | 0.5225 | 0.6013 | 240 | 13 |

**tax/GDP→education spend** (`log_spend_gdp` ~ `log_tax_gdp`)

| group_type | group | coef | se | t | p | n | n_cty |
|---|---|---|---|---|---|---|---|
| region | Asia | 0.5410 | 0.1255 | 4.3115 | 0.0000 | 322 | 16 |
| region | non-Asia | -0.3205 | 0.3698 | -0.8666 | 0.3862 | 206 | 10 |
| income_grp | low-income-1990 | 0.5491 | 0.1943 | 2.8257 | 0.0047 | 187 | 12 |
| income_grp | high-income-1990 | 0.3438 | 0.1950 | 1.7634 | 0.0778 | 341 | 14 |
| bursary_grp | low-tax-capacity | 0.0830 | 0.2103 | 0.3945 | 0.6932 | 265 | 16 |
| bursary_grp | high-tax-capacity | 0.6144 | 0.1825 | 3.3670 | 0.0008 | 263 | 10 |
| urb_grp | low-urban | 0.5817 | 0.1655 | 3.5152 | 0.0004 | 218 | 12 |
| urb_grp | high-urban | 0.1688 | 0.2868 | 0.5886 | 0.5561 | 310 | 14 |
| base_ger | GER-low-1990 | 0.4313 | 0.0913 | 4.7268 | 0.0000 | 232 | 13 |
| base_ger | GER-high-1990 | 0.4808 | 0.3576 | 1.3444 | 0.1788 | 296 | 13 |

**teachers→primary GER** (`log_ger_p` ~ `log_tch_p`)

| group_type | group | coef | se | t | p | n | n_cty |
|---|---|---|---|---|---|---|---|
| region | Asia | 0.4170 | 0.1098 | 3.7982 | 0.0001 | 700 | 19 |
| region | non-Asia | 0.4128 | 0.1126 | 3.6663 | 0.0002 | 352 | 11 |
| income_grp | low-income-1990 | 0.5284 | 0.0557 | 9.4911 | 0.0000 | 605 | 15 |
| income_grp | high-income-1990 | 0.1916 | 0.1565 | 1.2239 | 0.2210 | 447 | 15 |
| bursary_grp | low-tax-capacity | 0.5104 | 0.0635 | 8.0357 | 0.0000 | 680 | 20 |
| bursary_grp | high-tax-capacity | 0.2437 | 0.1555 | 1.5673 | 0.1171 | 372 | 10 |
| urb_grp | low-urban | 0.4799 | 0.0745 | 6.4447 | 0.0000 | 599 | 15 |
| urb_grp | high-urban | 0.2376 | 0.1717 | 1.3840 | 0.1664 | 453 | 15 |
| base_ger | GER-low-1990 | 0.4867 | 0.0756 | 6.4345 | 0.0000 | 571 | 17 |
| base_ger | GER-high-1990 | 0.1411 | 0.0976 | 1.4454 | 0.1483 | 481 | 13 |

**fertility→primary completion** (`log_cmpt_p` ~ `tfr`)

| group_type | group | coef | se | t | p | n | n_cty |
|---|---|---|---|---|---|---|---|
| region | Asia | -0.1724 | 0.0515 | -3.3474 | 0.0008 | 437 | 18 |
| region | non-Asia | -0.2218 | 0.0601 | -3.6898 | 0.0002 | 275 | 10 |
| income_grp | low-income-1990 | -0.1669 | 0.0444 | -3.7618 | 0.0002 | 350 | 15 |
| income_grp | high-income-1990 | -0.2247 | 0.0602 | -3.7310 | 0.0002 | 362 | 13 |
| bursary_grp | low-tax-capacity | -0.2117 | 0.0492 | -4.3055 | 0.0000 | 385 | 18 |
| bursary_grp | high-tax-capacity | -0.2331 | 0.0557 | -4.1856 | 0.0000 | 327 | 10 |
| urb_grp | low-urban | -0.2132 | 0.0393 | -5.4192 | 0.0000 | 341 | 15 |
| urb_grp | high-urban | -0.1569 | 0.0903 | -1.7365 | 0.0825 | 371 | 13 |
| base_ger | GER-low-1990 | -0.1714 | 0.0560 | -3.0622 | 0.0022 | 308 | 15 |
| base_ger | GER-high-1990 | -0.0560 | 0.0666 | -0.8408 | 0.4004 | 404 | 13 |

**Thresholds used for the splits** (`data/country_typology.csv`, 1985–2000 country means):
GDP per capita median US$1,706 (2015 constant); tax/GDP median 13.1%; 1990 secondary GER median 47.3%;
urban share median 40.2%. Asia = 19 countries (CHN, HKG, KHM, PHL, KOR, JPN, VNM, THA, IDN, MYS, SGP, MMR,
LAO, MNG, IND, BGD, PAK, LKA, NPL); non-Asia = 11 (TUR, MEX, BRA, EGY, NGA, KEN, ZAF, PER, COL, MAR, UKR).

**The three strongest conditionings** (these are the "only in certain types of countries" findings):
1. **Spending→secondary enrolment is an Asia/low-enrolment relation.** Asia +0.189** (se 0.090) vs non-Asia
   +0.010 (se 0.106); low-1990-GER +0.132* vs high-GER +0.077*.
2. **Private provision expands enrolment only where the state is weak.** Asia +0.086*** vs non-Asia +0.003;
   low-income-1990 +0.081*** vs high-income +0.014; low-tax-capacity +0.102*** vs high-tax-capacity −0.065.
3. **Fiscal space (tax/GDP) translates into education spending only in Asia and in low-urban settings**
   (+0.541*** and +0.582***), and not in non-Asia (−0.320 ns) — a state-capacity condition, not an income one.

## 4. Event windows (interrupted time series: linear pre-trend + post level shift)

### WDI panel outcomes

| iso3 | event_year | outcome | jump_log | se | t | pct_jump | n | pre_rms |
|---|---|---|---|---|---|---|---|---|
| PHL | 2016 | log_ger_s | -0.0081 | 0.0070 | -1.1621 | -0.8055 | 14 | 0.0039 |
| PHL | 2018 | log_ger_t | -0.0878 | 0.0200 | -4.3828 | -8.4028 | 17 | 0.0164 |
| CHN | 1986 | log_ger_s | 0.0914 | 0.0482 | 1.8983 | 9.5750 | 18 | 0.0392 |
| IDN | 1994 | log_ger_s | -0.0124 | 0.0202 | -0.6120 | -1.2279 | 17 | 0.0252 |
| THA | 1999 | log_ger_s | -0.1022 | 0.0270 | -3.7832 | -9.7148 | 15 | 0.0144 |
| MYS | 1996 | log_ger_s | 0.0223 | 0.0102 | 2.1894 | 2.2551 | 18 | 0.0065 |

### Observed GMR 6-country outcomes (`04_data/data/gmr_observed_6countries_1970_2024.csv`)

| iso3 | event_year | indicator | jump_log | se | t | pct_jump | n | y_pre | y_post | pre_rms |
|---|---|---|---|---|---|---|---|---|---|---|
| PHL | 2016 | ger_secondary | -0.0244 | 0.0326 | -0.7496 | -2.4147 | 15 | 79.27 | 85.61 | 0.0125 |
| PHL | 2018 | ger_tertiary | -0.3407 | 0.0766 | -4.4492 | -28.87 | 19 | 31.16 | 38.73 | 0.0740 |
| PHL | 2013 | ger_secondary | -0.0158 | 0.0337 | -0.4692 | -1.5683 | 15 | 77.98 | 83.19 | 0.0140 |
| JPN | 1980 | ger_tertiary | -0.0980 | 0.1134 | -0.8638 | -9.3311 | 18 | 24.15 | 30.05 | 0.1119 |
| CHN | 1986 | ger_secondary | 0.2774 | 0.1853 | 1.4966 | 31.97 | 19 | 40.35 | 39.95 | 0.1727 |

**What happened to each event we could test.**

| Event | Tested? | Result | Reading |
|---|---|---|---|
| PHL K-12 (RA 10533, 2016) | yes, GMR observed | secondary GER jump −2.4% (se 3.3), ns | **no total-GER level shift**; the documented "surge" is a composition/denominator effect of adding G11–12 to upper secondary, not a level move. This is a null the model must reproduce (R18). |
| PHL free SUC tuition (RA 10931, 2018) | yes, GMR observed | tertiary GER jump −28.9% (se 7.7), t=−4.45 | enrolment **fell** through the event, confounded by the K-12 cohort delay. Do not read it as a tuition effect (R19). |
| CHN Compulsory Education Law (1986) | yes, GMR observed | +32% (se 18.5), t=1.50 | right sign, pre-trend noise 17%, only 19 obs → weak (R20). |
| THA Education Act 1999 | yes, WDI | −9.7% (se 2.7), t=−3.78 | a *decline* at the event; series break / no detectable jump. Not usable. |
| MYS 1996 K-12 expansion | yes, WDI | +2.3% (se 1.0), t=2.19 | small positive, consistent with a slow expansion. |
| IDN 9-year compulsory (1994) | yes, WDI | −1.2% (se 2.0), ns | no jump. |
| HKG 1971 / 1978 compulsory schooling, KOR 1974 equalisation, KHM 1996/2001 | **blocked** | not estimated | the observed-only GMR panel has <13 usable secondary-GER observations per event window (series start ~1998). Never imputed. Needs EDB (HK) / KEDI (KOR) national series before running. |

## 5. Shadow-education gradients (observed survey values only)

| country | year | dimension | level | value_pct | source |
|---|---|---|---|---|---|
| HKG | 2003 | stage | S1-3 | 35.10 | Bray & Kwok (2003) EER 22:611-620, Table 1 p.616 |
| HKG | 2003 | stage | S4-5 | 46.60 | Bray & Kwok (2003) EER 22:611-620, Table 1 p.616 |
| HKG | 2003 | stage | S6-7 | 70.30 | Bray & Kwok (2003) EER 22:611-620, Table 1 p.616 |
| HKG | 2003 | gate-gradient | S6-7 minus S1-3 | 35.20 | Bray & Kwok (2003) Table 1 |
| KOR | 2023 | income-band | <3m won | 183.00 | MODS/KEDI 2023 English release, income table |
| KOR | 2023 | income-band | >=8m won | 671.00 | MODS/KEDI 2023 English release, income table |
| KOR | 2023 | income-elasticity | >=8m vs <3m | 1.3247 | derived from MODS/KEDI 2023 income bands |
| KOR | 2023 | level-participation | elementary | 86.00 | MODS/KEDI 2023 Table 2 |
| KOR | 2023 | level-participation | high | 66.40 | MODS/KEDI 2023 Table 2 |
| KOR | 2023 | level-spend | elementary | 398.00 | MODS/KEDI 2023 Table 2 |
| KOR | 2023 | level-spend | high | 491.00 | MODS/KEDI 2023 Table 2 |
| JPN | 2018 | urbanisation | Tokyo (max) | 57.90 | Rappleye & Komatsu (2020) EPAA 28(67), Table 2 |
| JPN | 2018 | urbanisation | Akita (min) | 22.10 | Rappleye & Komatsu (2020) EPAA 28(67), Table 2 |
| KHM | 2012 | urbanisation | urban grade 6 | 60.50 | Brehm & Silova (2013 WP39; 2014 JERO 6(1)) |
| KHM | 2012 | urbanisation | rural grade 6 | 26.40 | Brehm & Silova (2013/2014) |
| CHN | 2014 | policy | pre-Double-Reduction | 29.80 | Liu & Bray (2020) Educational Studies 46(2):170-187 (ERIC abstract) |
| CHN | 2022 | policy | post-Double-Reduction (<20%) | 20.00 | China Education Daily 2022-03-03 headline (LOW confidence) |

**Computed elasticities/gradients (and what they are not):**
- **Gate gradient, HK 2003** (Bray & Kwok, EER 22:611-620, Table 1 p.616, one survey of 6 schools n=630):
  35.1% (S1–3) → 46.6% (S4–5) → 70.3% (S6–7), a **+35.2pp** rise at the senior gate. This is the cleanest
  within-country evidence that tutoring demand is **positional/gate-driven**, and it is exactly the
  `R_gate` channel in `twoway.py`.
- **Income elasticity of tutoring expenditure, Korea 2023** (MODS/KEDI official survey): 183 → 671 thousand
  won/month across the <3m vs ≥8m won income bands; income gap 2.67×, spend gap 3.67× → **elasticity ≈ 1.33**.
  Tutoring spending is a luxury good even in a rich country.
- **Two-margin fact, Korea 2023**: participation *falls* from 86.0% (elementary) to 66.4% (high) while
  expenditure per student *rises* 398 → 491 thousand won (+23%). A single-margin demand block cannot produce
  both; the model needs an extensive and an intensive margin.
- **Urban gradient**: Japan 57.9% (Tokyo) vs 22.1% (Akita) = 2.62× (Rappleye & Komatsu 2020, Table 2);
  Cambodia grade-6 60.5% urban vs 26.4% rural = 2.29× but from a **6-school case study**, not national.
- **The one relation the model most needs and the data cannot give: returns→tutoring.** Four countries, three
  usable shadow survey years, no common instrument → not identifiable (R26). Keep it as a prior.

## 6. What could not be estimated, and why (blocked, not omitted)

| Relation | Why blocked | What would close it |
|---|---|---|
| spending→enrolment, causal | no instrument; only FE association available | a school-finance reform with a rule-based discontinuity |
| PTR/class size→completion | sign conflict between levels and FD (R11) | a class-size rule (e.g. maximum-size law) event study |
| returns→tutoring | <5 country-year cells, no common instrument | household survey with earnings + tutoring module (PHL FIES/APIS microdata is credentialed) |
| remittances→schooling | small volatile series, migration selection | PHL province-level panel with remittance shocks |
| compulsory-schooling events (HKG/KOR/KHM) | observed GER series start ~1998 | EDB / KEDI / MoEYS national series |
| price elasticity of tutoring demand | no credible estimate located | KEDI price variation / a fee deregulation episode |
| teachers→learning (not just enrolment) | no learning outcome on disk for 30 countries | PISA/TIMSS linkage (not in this panel) |

## 7. Files
| File | Content |
|---|---|
| `data/panel_wdi_wide.csv` | 30-country × 1970–2024 wide panel, observed cells only |
| `data/panel_results.csv` | 66 specifications (levels FE + first differences) |
| `data/panel_heterogeneity.csv` | 110 split-sample regressions across 5 typologies |
| `data/event_windows.csv`, `data/event_windows_gmr.csv` | interrupted-time-series event estimates |
| `data/shadow_gradients.csv` | observed shadow-education gradients |
| `data/country_typology.csv` | country baseline groups (1985–2000 means) |
| `raw/wdi/*.json` | raw API payloads, one file per indicator × country chunk |


## 8. Addendum A1 — literacy, ECI and population pyramids

A separate analysis file, **`LITERACY_ECI_DEMOGRAPHY.md`**, extends this layer with the ECI (Growth Lab / Harvard Dataverse, CC0) and literacy/pyramid data: tests E1–E17 (ECI × GDP × literacy × growth), the cohort-replacement decomposition D1–D2, and the population pyramids. Headline: **62–66% of observed adult-literacy gains is cohort replacement, not learning**; ECI tracks the schooling *flow* (completion t−10, 0.593) but not the literacy *stock*; and the published ECI growth premium does not replicate in this 30-country 1995–2024 panel (−0.068, se 0.067). Register rows R31–R40.
