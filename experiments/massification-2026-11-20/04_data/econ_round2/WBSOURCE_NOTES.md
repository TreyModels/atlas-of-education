# WBSOURCE_NOTES — what was pulled, what is missing, and the definition traps

Task-19, `data-hunter`, 2026-11-20. Companion to `econ_round2/data/econ_panel_round2.csv` (7,704 rows, 62 indicators, six countries, annual 1995–2024) and the six `WB_SNAPSHOT_<ISO3>.md` files.

## Pulled — World Bank WDI (live API, accessed 2026-11-20)

Raw JSON: `raw/worldbank_economy/`, `raw/worldbank_econ2/`, `raw/worldbank_fin/`. Every record carries the WDI `sourceNote` as its `definition` field in the panel.

| Group | Indicators |
|---|---|
| Income and growth | `NY.GDP.PCAP.PP.CD` (PPP current int'l $), `NY.GDP.PCAP.CD` (current US$), `NY.GDP.PCAP.KD` (constant 2015 US$), `NY.GDP.MKTP.KD.ZG`, `NY.GDP.PCAP.KD.ZG`, `NY.GDP.MKTP.CD` (total GDP, current US$), `FP.CPI.TOTL.ZG` (CPI inflation), `NE.TRD.GNFS.ZS` (trade openness) |
| Labour force | `SL.TLF.TOTL.IN`, `SL.TLF.ACTI.ZS`, `SL.TLF.ACTI.1524.ZS`, `SL.EMP.TOTL.SP.ZS`, `SL.EMP.TOTL.SP.FE.ZS` |
| Sector employment | `SL.AGR.EMPL.ZS`, `SL.IND.EMPL.ZS`, `SL.SRV.EMPL.ZS` |
| Status in employment | `SL.EMP.WORK.ZS` (wage and salaried), `SL.EMP.SELF.ZS`, `SL.EMP.MPYR.ZS` (employers), `SL.EMP.VULN.ZS` (vulnerable) |
| Unemployment / NEET | `SL.UEM.TOTL.ZS`, `SL.UEM.1524.ZS`, `SL.UEM.1524.FE.ZS`, `SL.UEM.1524.MA.ZS`, `SL.UEM.NEET.ZS` |
| Population / ageing | `SP.POP.TOTL`, `SP.POP.0014.TO.ZS`, `SP.POP.1564.TO.ZS`, `SP.POP.65UP.TO.ZS`, `SP.POP.DPND` |
| Urbanisation | `SP.URB.TOTL.IN.ZS` |
| Remittances | `BX.TRF.PWKR.CD.DT`, `BX.TRF.PWKR.DT.GD.ZS` |
| Education spending | `SE.XPD.TOTL.GD.ZS` (% of GDP), `SE.XPD.TOTL.GB.ZS` (% of total govt expenditure) |
| Teachers / ratios | `SE.PRE.TCHR`, `SE.PRM.TCHR`, `SE.SEC.TCHR`, `SE.PRE.ENRL.TC.ZS`, `SE.PRM.ENRL.TC.ZS`, `SE.SEC.ENRL.TC.ZS`, `SE.PRM.TCAQ.ZS`, `SE.SEC.TCAQ.ZS`, `SE.TER.TCHR` |

**Derived (flagged, not reported):** `DERIVED_GOVT_EDU_SPEND_USD` = `SE.XPD.TOTL.GD.ZS`/100 × `NY.GDP.MKTP.CD`. WDI reports education spending only as a share; the US$ total is arithmetic. It is labelled DERIVED in `indicator_name` and `definition` and must not be cited as an official US$ series.

## Pulled — UNESCO UIS SDG4 (release 2026-11, extracted 2026-10-22)

| Group | Indicators |
|---|---|
| Education spending | `XGDP.FSGOV` (% GDP), `XGOVEXP.IMF` (% of total government expenditure, UIS calculation from IMF data) |
| Per-student funding | `XUNIT.PPPCONST.{02,1,2,2T3,3,5T8}.FSGOV.FFNTR` — **constant PPP$ per student** (govt funding); `XUNIT.GDPCAP.{1,2T3,3,5T8}.FSGOV.FFNTR` — per student as % of GDP per capita |
| Teacher pay | `XASTRP.GDPCAP.{1,2,3}.TXP15/TXPS.PCONTR` — statutory teacher remuneration as % of GDP per capita, at 15 years' experience (`TXP15`) and starting salary (`TXPS`) |

## Access attempts — World Bank Enterprise Surveys, STEP, EdStats, others

| Source | Result |
|---|---|
| **Enterprise Surveys** site `enterprisesurveys.org/en/data` | HTTP 200 |
| ES country profile PDF, Philippines 2015 | **HTTP 200, 595,019 bytes**, archived at `econ_round2/raw/enterprisesurvey_PHL_2015.pdf`. Contains firm characteristics, workforce composition (female share, formal training, temporary work), business-environment constraints, performance — **no education/credential-requirement table** |
| ES country profile, Cambodia 2016 (`Cambodia-2016.pdf` naming guess) | **HTTP 404** — the naming pattern is country-year specific and not discoverable without the ES data portal |
| ES data API `api.enterprisesurveys.org/api/v1/...` | **HTTP 000** (host did not resolve) — cannot query credential/hiring indicators programmatically |
| **STEP** (Skills Toward Employment and Productivity) | `microdata.worldbank.org` catalog pages HTTP 200; STEP studies exist (e.g. Bolivia, Colombia, Ghana, Kenya, Lao PDR, Sri Lanka, Vietnam, Yunnan) but **microdata are credentialed**; the programme page is 404. No STEP survey covers the six target countries in the free files. |
| **EdStats** | The World Bank data catalog page for the retired Education Statistics dataset is HTTP 200, but **EdStats is discontinued**; its returns-to-schooling and education-expenditure-by-level series are not served by an API any more |
| **ILOSTAT** | `ilostat.ilo.org` HTTP 403; no informal-employment or public-sector tables pulled |
| **PSA (Philippines)** | HTTP 403 on every path; no FIES/APIS/LFS microdata or summary tables |
| **DHS** | credentialed; Cambodia DHS exists but no tutoring module and no download in this pass |
| **World Bank microdata catalog** | HTTP 200; FIES/APIS/LFS/STEP studies credential-gated, not requested |

## Definition traps — read before using the panel

1. **Status ≠ formality.** `SL.EMP.WORK.ZS` (wage and salaried) is status in employment, not formal employment. A salaried worker can be informal; the only actual informality number in the project is Cambodia's 88.3% (CLFS 2019, ILO definition). Vulnerable employment = own-account + contributing family workers, again not "informal".
2. **% of GDP ≠ % of government budget.** `SE.XPD.TOTL.GD.ZS` and `SE.XPD.TOTL.GB.ZS` are different denominators and move differently; `XGOVEXP.IMF` is a UIS calculation from IMF data and may differ from the national budget share.
3. **"Initial government funding per student" ≠ total spending per student.** UIS `XUNIT.*` excludes household and other private spending; in Cambodia private tutoring is a large part of real unit cost, so these series understate the household-financed pipeline.
4. **PPP ≠ current US$ ≠ constant US$.** `NY.GDP.PCAP.PP.CD` is current international dollars (rebased, not a time series of real growth); `NY.GDP.PCAP.CD` is current US$ (moves with exchange rates); `NY.GDP.PCAP.KD` is the only one suitable for real growth. Growth series (`*.KD.ZG`) are annual percent changes.
5. **ILO modelled vs national survey.** Every `SL.*` series in WDI is an ILO **modelled** estimate for these countries, not a national LFS tabulation; Cambodia's CLFS 2019 gives 1.2% unemployment where WDI's modelled series differs. Use national surveys where you have them.
6. **Trained teachers ≠ qualified teachers.** `SE.PRM.TCAQ.ZS` is the share with the minimum required training; UIS `TRTP.*` is the share meeting the national minimum qualification standard — different criteria.
7. **Pupil-teacher ratio is headcount-based.** Part-time teachers and double-shift schools distort it; Cambodia's two-shift schooling (81% of primary, 41% of lower secondary in 2005) makes ratio comparisons with Japan especially misleading.
8. **Attainment stock ≠ flow.** WDI `SE.*.CUAT.*` are **modelled** (Barro-Lee/Wittgenstein) stock shares of the 25+ population — not survey tabulations, and not "share of jobs".
9. **Remittances ≠ migration.** `BX.TRF.PWKR.*` is a balance-of-payments flow; it is not deployment. The Philippine OFW deployment series (POEA/DMW) is not retrieved.
10. **Urbanisation is nationally defined.** HKG is 100% urban by construction; KHM's 40.9% and PHL's 55.5% use national definitions that change over time.
11. **Age cohorts are UN estimates, not censuses**, and are revised with each WPP round.
12. **Vintage mixing.** WDI access is live (2026-11-20), UIS is release 2026-11; the same underlying series can differ between them (e.g. education spending %GDP for PHL: WDI 3.93 for 2024, UIS 3.45 for 2025). Do not average across the two.

## What the six snapshots contain, and which are complete

Each `WB_SNAPSHOT_<ISO3>.md` lists every available series with its code, latest value and year, plus an explicit "not available" list. Series present: PHL 49, KHM 49, HKG 53, CHN 47, KOR 47, JPN 47 (of ~53 listed in the template). The differences are mostly missing teacher counts/trained-teacher shares (HKG/JPN) and missing status/sector employment in some years.

**Most complete:** HKG (53). **Least complete:** JPN and CHN (47), missing parts of the teacher-pay and per-student funding suites. All six have GDP, labour force, sector and status employment, urbanisation, age structure, education spending (%GDP and %budget), pupil-teacher ratios, remittances and inflation.

## Where the parameter map comes from

`PARAMETER_MAP.csv` has 28 rows: **8 observable**, **3 observable-partial**, **3 proxy-only**, **1 observed-but-uneven**, **3 sparse/limited**, and **10 marked not observable** with the reason. The not-observable set is the honest core of the Council's "data on hand vs new data needed" line: formal-job creation elasticity, wage premium/returns to schooling, formal-informal transitions, public-sector employment share, credential requirements in hiring, LFPR by education, transition/repetition/dropout, formal wage premium, migration by occupation, contributing-family workers.
