# A1 — China input verification for `engine/firms/data_china.py`

**Atlas of Education v0.9 · audit completed 4 November 2026**  
**Scope:** every value currently flagged `'m'`; adjacent errors discovered in already-`'v'` values are listed separately.  
**Status:** audit only. `data_china.py` has **not** been edited. Apply these changes in B3 and rerun the model; do not silently alter headline results.

## Decision summary

- **107 memory-flagged entries reviewed.**
- **106 can become `'v'`** with the source mapping below.
- **1 should drop:** 2026 tertiary entrants = 10.8m, a scenario assumption rather than an observation.
- **2 memory-flagged values need correction:** 1994 births, 20.9m → **21.1m**; 2021 tertiary entrants, 10.01m → **9.56m** under the series' dominant exclusion of five-year vocational transfers.
- **3 additional already-`'v'` urban-unemployment values need correction:** 2022-10, 2025-01, and 2025-04.
- `GRADUATES` must be relabelled **expected graduating-class scale used in employment planning**, not realised regular-HEI graduates.
- The birth figures below are **derived from NBS population and birth-rate tables**, not directly tabulated birth counts. Preserve that distinction in `SOURCES`.

## 1. Youth unemployment, new definition — eight `'m'` entries

Urban workers aged 16–24, **excluding students**; percent. All eight values are retained and become `'v'`.

Primary monthly database: [NBS National Data, employment indicators](https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0E01&sj=202510).

| Month | Old | Corrected | New flag | Direct corroboration |
|---|---:|---:|:---:|---|
| 2025-01 | 16.1 | 16.1 | `v` | [Caixin, 21 Mar 2025](https://economy.caixin.com/2025-03-21/102300574.html): February 16.9, 0.8 pp above January |
| 2025-03 | 16.5 | 16.5 | `v` | [NBS monthly database](https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0E01&sj=202503); [Caixin year-on-year check](https://economy.caixin.com/2026-04-21/102436199.html) |
| 2025-04 | 15.8 | 15.8 | `v` | [Contemporaneous NBS-release report](https://www.mycaijing.com/flash/detail/624354) |
| 2025-05 | 14.9 | 14.9 | `v` | [Caixin, 19 Jun 2025](https://economy.caixin.com/2025-06-19/102332256.html) |
| 2025-07 | 17.8 | 17.8 | `v` | [NBS-release report with July and August](https://www.sina.cn/news/detail/5212148407731095.html) |
| 2025-08 | 18.9 | 18.9 | `v` | [NBS-release report with July and August](https://www.sina.cn/news/detail/5212148407731095.html) |
| 2025-09 | 17.7 | 17.7 | `v` | [Global Times, citing NBS](https://www.globaltimes.cn/page/202511/1348496.shtml) |
| 2025-10 | 17.3 | 17.3 | `v` | [Global Times, citing NBS](https://www.globaltimes.cn/page/202511/1348496.shtml) |

## 2. Overall urban surveyed unemployment — 55 `'m'` entries

Percent; January–December in order. Every value is retained and becomes `'v'`. One NBS monthly series covers all rows, avoiding 55 fragile article citations.

| Months | Old → corrected monthly values | New flag | Source |
|---|---|:---:|---|
| 2018-01…12 | 5.0, 5.0, 5.1, 4.9, 4.8, 4.8, 5.1, 5.0, 4.9, 4.9, 4.8, 4.9 → unchanged | `v` | [NBS National Data](https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0E01&sj=201812) |
| 2019-01…12 | 5.1, 5.3, 5.2, 5.0, 5.0, 5.1, 5.3, 5.2, 5.2, 5.1, 5.1, 5.2 → unchanged | `v` | [NBS National Data](https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0E01&sj=201912) |
| 2020-01…12 | 5.3, 6.2, 5.9, 6.0, 5.9, 5.7, 5.7, 5.6, 5.4, 5.3, 5.2, 5.2 → unchanged | `v` | [NBS National Data](https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0E01&sj=202012) |
| 2021-01…12 | 5.4, 5.5, 5.3, 5.1, 5.0, 5.0, 5.1, 5.1, 4.9, 4.9, 5.0, 5.1 → unchanged | `v` | [NBS National Data](https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0E01&sj=202112) |
| 2022-01…07 | 5.3, 5.5, 5.8, 6.1, 5.9, 5.5, 5.4 → unchanged | `v` | [NBS National Data](https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0E01&sj=202207) |

### Adjacent corrections in entries already labelled `'v'`

These are outside the strict `'m'` count but must enter the same B3 correction set.

| Month | Current | NBS value | Action | Source |
|---|---:|---:|---|---|
| 2022-10 | 5.6 | **5.5** | Correct; retain `v` | [NBS National Data](https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0E01&sj=202210) |
| 2025-01 | 5.2 | **5.3** | Correct; retain `v` | [NBS National Data](https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0E01&sj=202501) |
| 2025-04 | 5.1 | **5.2** | Correct; retain `v` | [NBS National Data](https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0E01&sj=202504) |

## 3. Expected graduating-class scale — 14 `'m'` entries

Millions. All values are retained and become `'v'`.

**Definition correction required:** this is the scale announced for graduate-employment planning, often before graduation. It is **not** the realised count of regular-HEI graduates in education statistical communiqués. For example, the employment series uses 5.59m for 2008, while the education communiqué reports 5.1195m realised regular-HEI graduates. Do not replace this series with realised graduates.

| Class year | Old | Corrected | New flag | Source |
|---|---:|---:|:---:|---|
| 2008 | 5.59 | 5.59 | `v` | [Sinoss compilation of government/MoE releases, table 2](https://www.sinoss.net/uploadfile/2015/0531/20150531092204192.pdf) |
| 2009 | 6.11 | 6.11 | `v` | [Same source](https://www.sinoss.net/uploadfile/2015/0531/20150531092204192.pdf) |
| 2010 | 6.31 | 6.31 | `v` | [MoE-hosted historical summary](https://www.moe.gov.cn/jyb_xwfb/s5147/201503/t20150312_186243.html) |
| 2011 | 6.60 | 6.60 | `v` | [Same source](https://www.moe.gov.cn/jyb_xwfb/s5147/201503/t20150312_186243.html) |
| 2012 | 6.80 | 6.80 | `v` | [Same source](https://www.moe.gov.cn/jyb_xwfb/s5147/201503/t20150312_186243.html) |
| 2013 | 6.99 | 6.99 | `v` | [MoE](https://www.moe.gov.cn/jyb_xwfb/s5147/201307/t20130726_154636.html) |
| 2014 | 7.27 | 7.27 | `v` | [MoE](http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/moe_1485/201312/t20131206_160544.html) |
| 2015 | 7.49 | 7.49 | `v` | [MoE](https://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/moe_1485/201412/t20141204_180306.html) |
| 2016 | 7.65 | 7.65 | `v` | [MoE](http://www.moe.gov.cn/jyb_xwfb/s5148/201606/t20160615_267636.html) |
| 2017 | 7.95 | 7.95 | `v` | [MoE](https://www.moe.gov.cn/jyb_xwfb/s5147/201612/t20161201_290552.html) |
| 2018 | 8.20 | 8.20 | `v` | [MoE](http://www.moe.gov.cn/jyb_xwfb/moe_2082/zl_2018n/2018_zl37/201805/t20180515_336007.html) |
| 2019 | 8.34 | 8.34 | `v` | [MoE](http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/moe_1485/201811/t20181128_361821.html) |
| 2020 | 8.74 | 8.74 | `v` | [MoE](https://www.moe.gov.cn/srcsite/A15/s3265/202003/t20200306_428194.html) |
| 2022 | 10.76 | 10.76 | `v` | [MoE](http://www.moe.gov.cn/fbh/live/2021/53931/mtbd/202112/t20211229_591299.html) |

## 4. Births reconstructed from NBS tables — 12 `'m'` entries

Millions. Formula:

`births_million = birth_rate_per_thousand × mean(year_end_population, previous_year_end_population) / 1000 / 100`

The NBS tables use 万人 for population and ‰ for birth rate. Sources for every row: [NBS year-end population](https://www.stats.gov.cn/sj/ndsj/2011/html/D0301C.HTM), [NBS birth rates](https://www.stats.gov.cn/sj/ndsj/2011/html/D0302C.HTM), and [NBS indicator definition](https://www.stats.gov.cn/sj/ndsj/2021/html/zb02.htm).

| Birth year | Old | NBS reconstruction | Corrected model value | New flag |
|---|---:|---:|---:|:---:|
| 1988 | 24.6 | 24.6435 | 24.6 | `v` |
| 1990 | 23.9 | 23.9070 | 23.9 | `v` |
| 1992 | 21.2 | 21.2491 | 21.2 | `v` |
| 1994 | 20.9 | **21.0955** | **21.1** | `v` |
| 1996 | 20.7 | 20.6740 | 20.7 | `v` |
| 1998 | 19.4 | 19.4239 | 19.4 | `v` |
| 2000 | 17.7 | 17.7149 | 17.7 | `v` |
| 2002 | 16.5 | 16.4659 | 16.5 | `v` |
| 2004 | 15.9 | 15.9288 | 15.9 | `v` |
| 2006 | 15.8 | 15.8502 | 15.8 | `v` |
| 2008 | 16.1 | 16.0813 | 16.1 | `v` |
| 2010 | 15.9 | 15.9187 | 15.9 | `v` |

**Provenance wording:** call these `NBS-derived births` and record the formula. Do not describe them as directly published annual birth counts.

## 5. New tertiary entrants — 14 `'m'` entries

Millions; regular undergraduate + vocational undergraduate + higher-vocational college entrants. Unless noted, five-year vocational transfers are **excluded**, matching the dominant series convention. Values rounded to two decimals.

| Year | Old | Corrected | New flag | Source / calculation |
|---|---:|---:|:---:|---|
| 2006 | 5.46 | 5.46 | `v` | [MoE 2006 communiqué](http://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/tnull_23240.html): 546.05万 |
| 2008 | 6.08 | 6.08 | `v` | [2008 communiqué report](https://www.chinanews.com.cn/edu/edu-zcdt/news/2009/07-18/1780677.shtml): 607.66万 |
| 2010 | 6.62 | 6.62 | `v` | [MoE 2010 communiqué](http://www.moe.gov.cn/srcsite/A03/s180/moe_633/201203/t20120321_132634.html): 661.76万 |
| 2012 | 6.89 | 6.89 | `v` | [MoE 2012 communiqué](http://www.moe.gov.cn/srcsite/A03/s180/moe_633/201308/t20130816_155798.html): 688.83万 |
| 2014 | 7.21 | 7.21 | `v` | [MoE 2014 communiqué](http://www.moe.gov.cn/srcsite/A03/s180/moe_633/201508/t20150811_199589.html): 721.40万 |
| 2016 | 7.49 | 7.49 | `v` | [MoE 2016 communiqué](http://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/201707/t20170710_309042.html): 748.61万 |
| 2018 | 7.91 | 7.91 | `v` | [MoE 2018 communiqué](http://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/201907/t20190724_392041.html): 790.99万 |
| 2019 | 9.15 | 9.15 | `v` | [MoE 2019 communiqué](http://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/202005/t20200520_456751.html): 914.90万 |
| 2020 | 9.67 | 9.67 | `v` | [MoE 2020 communiqué](https://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/202108/t20210827_555004.html): 967.45万 |
| 2021 | 10.01 | **9.56** | `v` | [MoE 2021 communiqué](http://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/202209/t20220914_660850.html): (444.60 + 4.14 + 552.58 − 45.20) / 100 = 9.5612m; removes included five-year transfers |
| 2022 | 10.14 | 10.14 | `v` | [MoE 2022 release](http://www.moe.gov.cn/fbh/live/2023/55167/): 1014.54万, transfers separately excluded |
| 2023 | 10.42 | 10.42 | `v` | [MoE 2023 communiqué](http://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/202410/t20241024_1159002.html): (478.16 + 8.99 + 555.07) / 100 = 10.4222m |
| 2024 | 10.68 | 10.68 | `v` | [MoE 2024 communiqué](https://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/202506/t20250611_1193760.html): (489.97 + 10.96 + 567.94) / 100 = 10.6887m |
| 2026 | 10.80 | — | **drop** | No observed MoE source; forward assumption. Remove from observations. `_interp` then holds the 2024 value flat beyond 2024. If desired, put 10.8 in a separately named scenario dictionary. |

**Alternative defensible convention:** include five-year vocational transfers in every year. That requires rebuilding the entire series, not retaining the current mixed treatment. Do not mix conventions within one calibrated input.

## 6. Real-estate development investment growth — four `'m'` entries

Annual growth, percent. All retained and become `'v'`.

| Year | Old | Corrected | New flag | NBS source |
|---|---:|---:|:---:|---|
| 2018 | 9.5 | 9.5 | `v` | [NBS 2018 release](https://www.stats.gov.cn/sj/zxfb/202302/t20230203_1900208.html) |
| 2019 | 9.9 | 9.9 | `v` | [NBS 2019 release](https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/202001/t20200117_1767745.html) |
| 2020 | 7.0 | 7.0 | `v` | [NBS 2020 release](https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/202101/t20210118_1812461.html) |
| 2021 | 4.4 | 4.4 | `v` | [NBS 2021 release](https://www.stats.gov.cn/sj/zxfb/202302/t20230203_1901340.html) |

## 7. Paste-ready B3 change list

```python
# Value corrections
BIRTHS[1994] = 21.1
TERTIARY_ENTRANTS[2021] = 9.56
_URB_V[2022][9] = 5.5
_URB_V[2025][0] = 5.3
_URB_V[2025][3] = 5.2

# Observation removal
TERTIARY_ENTRANTS.pop(2026)

# After adding per-entry provenance/source mappings:
# Change all eight 2025 youth 'm' flags to 'v'.
# Move the pre-Aug-2022 _URB_M observations into verified data.
# Change all GRAD_FLAG entries to 'v'.
# Change PROPERTY_FLAG[2018:2021] to 'v'.
# Births and entrants need explicit per-entry flags rather than a blanket comment.
```

### Required documentation edits when applying B3

1. Replace `regular HEIs, bachelor + junior college` with `expected graduating-class scale used in employment planning`.
2. Add `NBS-derived births` and the reconstruction formula to `SOURCES`.
3. State the five-year-vocational-transfer convention for tertiary entrants.
4. Preserve the existing caveat that tertiary entrants are not necessarily drawn from the same 18-year-old birth cohort.
5. Record before/after headline outputs in B3; provenance repair does not license silently changing calibrated conclusions.
