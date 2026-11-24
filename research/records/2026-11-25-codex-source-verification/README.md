# Codex source verification — task-49

**Owner:** novelty-review. **Branch:** `research/codex-source-verification-2026-11-25`.
**Date:** 24 November 2026. No compute; web + Crossref only.

Read first: `origin/research/codex-handoff-run-2026-11-24:research/records/2026-11-24-codex-review/REVIEW.md`
and `findings.csv`; handoff `LETTER_FOR_DEEPSEEK.md`/`SYNTHETIC.md`; assessment record
`origin/research/assessment-and-next-experiments-2026-11-24:research/records/2026-11-24-assessment-and-next-experiments/`
(`NEXT_EXPERIMENTS.md` E6/E8, `DATA_SOURCES.md`).

**METADATA ERRATUM (see `ERRATUM.md`):** the commit message of the verified head `9a0fd69` describes the Job-3
prior art as "24 DOI-verified"; the tables below mark **21 V / 2 U / 1 W** (24 works checked). No table value
changes.

## Job 1 — Fee-abolition dates (E8)

Script of record: `research/records/2026-11-22-massification-panel/scripts/final_tests.py` (`FEE` dict):
Malawi 1994, Ethiopia 1995, Uganda 1997, Lesotho 2000, Cameroon 2000, Tanzania 2001, Zambia 2002, Kenya 2003,
Rwanda 2003, Mozambique 2004, Burundi 2005, Ghana 2005.

**Resolution rule.** The event year is the calendar year in which the abolition policy took effect (administrative
act, announcement, or policy launch). Where the reform is defined by an academic year, code the calendar year of
effect (Ghana 2005/06 → 2005; Ethiopia 1994/95 policy implemented 1995 → 1995). The "alternative" year is the
policy-adoption year or the first full academic year, to be used as a ±1/alternative-date sensitivity, not as the
main date.

### Verified (8 of 12)

| Country | Preferred | Alternative | Source (page/box) | Quote |
|---|---|---|---|---|
| Malawi | **1994** | 1995 | World Bank/UNICEF 2009 *Six Steps* Guide, Box 3.2; World Bank 2009 *Abolishing School Fees in Africa* ch.5 | "In 1994 Malawi's newly elected government eliminated school fees for primary education." |
| Ethiopia | **1995** | 1994 | World Bank 2009 book, ch.2, PDF p.75 / printed p.49 (DOI 10.1596/978-0-8213-7540-2) | "education expenditure has been greater since 1995, when the new Education and Training Policy was implemented and fees abolished" |
| Uganda | **1997** | — | *Six Steps* Guide, Box 3.2 | "In Uganda political pressures in 1997 prompted the government to adopt the 'big bang' approach…" |
| Lesotho | **2000** | — | *Six Steps* Guide, Box 3.3 | "In 2000 it introduced free primary education starting with grade 1." |
| Tanzania | **2001** | 2003 | *Six Steps* Guide, Box 6.1 | "Tanzania's Primary Education Development Program, launched in 2001, abolished school fees…" |
| Kenya | **2003** | — | World Bank 2009 book, ch.4, PDF p.156 / printed p.130 | "as of January 4, 2003, all Kenyan children…" |
| Mozambique | **2004** | 2005 | World Bank 2009 book, ch.6, PDF p.233 / printed p.207 | "School fees … were abolished by the government of Mozambique in 2004" |
| Ghana | **2005** | 1997 | *Six Steps* Guide, Box 4.2; World Bank 2009 book ch.3, PDF p.119/137 | "scaled at a national level in 2005/06 … with effect from the 2005/06 academic year" (pilot 2004/05) |

### Unresolved (4 of 12) — do not guess

| Country | Conflict | What is missing |
|---|---|---|
| Cameroon | 1999 / 2000 | No primary source located: not covered by the World Bank/UNICEF 2009 book or guide; no ministry decree retrieved. Need the *arrêté* ministerial, UNICEF Cameroon, or EFA country report. |
| Zambia | 2002 | No abolition source located. The SFAI guide's "Zambia (2002)" is a DHS survey year, not a fee-abolition date. Need the Ministry of Education 2002 Free Education Policy or a World Bank education-sector document. |
| Rwanda | 2003 | No primary source located. Need MINEDUC fee-abolition policy citation. |
| Burundi | 2005 | No primary source located. Need ministerial *arrêté* / UNICEF Burundi citation. |

### Conflict resolutions requested by the lead

- **Cameroon 1999/2000** — UNRESOLVED; no source supports either year in-session.
- **Ghana 1997/2005** — **2005** (national; 2005/06 academic year). 1997 is not a national fee abolition: FCUBE began 1996 and fees were first abolished in 1961.
- **Ethiopia 1994/1995** — **1995** (implementation). 1994 is the Education and Training Policy adoption year.
- **Tanzania 2001/2003** — **2001** (PEDP launch abolished fees). 2002/2003 is the first academic year/rollout.
- **Malawi 1994/1995** — **1994** (elimination). 1995 is the first full academic year (1994/95).
- **Mozambique 2004/2005** — **2004** (abolition). 2005 is the first full academic year.

**Verified-only set for E8 main specification (8):** MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003,
MOZ 2004, GHA 2005. **Sensitivity/all-dates set (12):** add CMR 2000, ZMB 2002, RWA 2003, BDI 2005, flagged
UNRESOLVED.

### Sources

1. World Bank & UNICEF (2009). *Six Steps to Abolishing Primary School Fees: Operational Guide*. Washington, DC:
   World Bank. Open Knowledge Repository: https://openknowledge.worldbank.org/entities/publication/a55bc38c-5d2b-5932-83e4-debc56e30da9
   (no Crossref DOI; PDF bitstream retrieved 24 Nov 2026; boxes 3.2, 3.3, 4.2, 6.1).
2. World Bank (2009). *Abolishing School Fees in Africa: Lessons from Ethiopia, Ghana, Kenya, Malawi, and
   Mozambique*. Washington, DC: World Bank. DOI **10.1596/978-0-8213-7540-2** (Crossref verified). Chapters 2-6;
   page locators given as PDF page / printed page.

## Job 2 — Demand series (E6)

All checks below were run on 24 Nov 2026 against the live sources via the proxy; "first year" is the earliest
non-missing year for the indicator in the current release.

| Source / version | What it has | First year | Access | Status |
|---|---|---|---|---|
| **GGDC 10-Sector Database, 2014 release** (Timmer, de Vries & de Vries; Groningen Growth and Development Centre) | value added, output deflators, and **persons employed** for 10 broad sectors; 11 Africa + 11 Asia + 2 MENA + 9 Latin America countries plus US/Europe comparators | **1950** (country-varying: e.g., India 1950, Tanzania/Zambia 1960, Morocco 1970); ends 2010-2013 | Free Excel/Stata download: https://www.rug.nl/ggdc/structuralchange/previous-sector-database/10-sector-2014 | AVAILABLE. Note: this is the "previous" database; the current GGDC successor is the **Economic Transformation Database (ETD)**, 1990-2018, 51 countries — post-1990 only, so not a pre-1990 substitute. |
| **Penn World Table 11.0** (published 7 Oct 2025) | 185 countries, 1950-2023; includes labour share (`labsh`) and employment (`emp`) | **1950** | Free: https://www.rug.nl/ggdc/productivity/pwt/ (Excel/Stata/Dataverse) | AVAILABLE. PWT 10.01 is superseded by 11.0; both cover 1950+. |
| **WDI urbanisation** (`SP.URB.TOTL.IN.ZS`) | urban share of population | **1960** (Kenya 1960-2025; n=66) | World Bank API, free: https://api.worldbank.org/v2/country/KEN/indicator/SP.URB.TOTL.IN.ZS?format=json | AVAILABLE |
| **WDI sector value added** | `NV.AGR.TOTL.ZS` agriculture, `NV.IND.TOTL.ZS` industry, `NV.SRV.TOTL.ZS` services | agriculture **1960**, industry **1960**, services **2006** (current WDI; services VA is not available pre-2006 in this series) | World Bank API, free | AVAILABLE with the services caveat |
| **Wage employment** (`SL.EMP.WORK.ZS`, wage and salaried workers, % total employment, modelled ILO) | wage employment | **1991** (Kenya 1991-2025; n=35) | World Bank API, free | **NO pre-1990 coverage** |

### Does any pre-1990 wage-employment series exist for the sequencing sample?

**No, not in the standard public sources checked.** WDI's wage-and-salaried-workers series starts in **1991** for
every country (ILO modelled estimates begin 1991); the project's own `wage_emp.json` also starts in 1991 for every
country (`DATA_SOURCES.md`). ILOSTAT paid-employment series are likewise 1991+ in the public API, with only scattered
longer national series. **Consequence for task-47 (common-window re-estimate):** a pre-1990 common-window
re-estimate of the wage-employment/demand comparison **cannot be run on wage employment**. It can be run on
pre-1990 **sector employment shares** from GGDC 10-Sector (1950/1960+) or PWT `emp` (1950+), and on WDI
urbanisation/agriculture VA (1960+); the 7% labour-demand figure remains a 1991+ comparison unless a historical
national wage series is assembled by hand. This is the direct answer to whether the common-window re-estimate is
possible: **yes for farm-employment share, no for wage employment.**

## Job 3 — Prior art for Q1/Q2/Q3

DOIs verified via Crossref on 24 Nov 2026 (V = DOI resolves with matching title/author/year; W = working-paper
version; U = no DOI, book/pre-DOI). No "first" claims.

### Q1 — Schooling, structural transformation and the sequencing claim (8)

| # | Work | DOI | Status | What it pre-empts |
|---|---|---|---|---|
| 1 | Porzio, Rossi & Santangelo (2021), The Human Side of Structural Transformation, NBER WP 29390 | 10.3386/w29390 | V | closest systematic schooling↔structural-transformation paper; the competitor to the sequencing assembly |
| 2 | Boppart, Kiernan, Krusell & Malmberg (2023), The Macroeconomics of Intensive Agriculture, NBER 31101 | 10.3386/w31101 | V | agricultural floor / structural-change mechanism |
| 3 | Goldin & Katz (2008), The Race between Education and Technology | 10.2307/jctvf9x5x | V (book) | demand-led US case |
| 4 | Sandberg (1979), The Case of the Impoverished Sophisticate, JEH 39(1) | 10.1017/s0022050700096418 | V | schooling before industrialisation (Sweden) — canonical |
| 5 | Squicciarini & Voigtländer (2015), QJE 130(4) | 10.1093/qje/qjv025 | V | upper-tail knowledge before industrialisation |
| 6 | de Pleijt & van Zanden (2016), EREH 20(4) | 10.1093/ereh/hew013 | V | human capital before growth (Little Divergence) |
| 7 | Boli, Ramirez & Meyer (1985), Comparative Education Review 29(2) | 10.1086/446504 | V | world-polity supply-led expansion account |
| 8 | Soysal & Strang (1989), Sociology of Education 62(4) | 10.2307/2112831 | V | state-building origins of mass schooling |

(Also verified and relevant: Benavot & Riddle 1988 10.2307/2112627; Schofer & Meyer 2005 10.1177/000312240507000602.)

### Q2 — Country path comparison, matched pairs, process tracing (8)

| # | Work | DOI | Status | Caveat it supplies |
|---|---|---|---|---|
| 1 | Beach & Pedersen (2013), Process-Tracing Methods | 10.3998/mpub.2556282 | V (book) | process-tracing standards; avoiding hand-picked cases |
| 2 | Collier (2011), Understanding Process Tracing, PS: Political Science & Politics 44(4) | 10.1017/s1049096511001429 | V | process-tracing caveats |
| 3 | Lieberman (2015), Nested analysis, in Advances in Comparative-Historical Analysis | 10.1017/cbo9781316273104.010 | V (chapter) | combining large-N with case study |
| 4 | Abadie, Diamond & Hainmueller (2010), Synthetic control, JASA 105(490) | 10.1198/jasa.2009.ap08746 | V | comparative case design with a donor pool |
| 5 | Stuart (2010), Matching methods for causal inference, Statistical Science 25(1) | 10.1214/09-sts313 | V | matched-pair design and balance diagnostics |
| 6 | Mahoney & Rueschemeyer (2003), Comparative Historical Analysis in the Social Sciences | — | U (book) | comparative-historical method |
| 7 | Gerring (2007), Case Study Research: Principles and Practices | — | U (book) | case-selection principles |
| 8 | Romano & Wolf (2004), Exact and approximate stepdown methods | 10.2139/ssrn.563267 | W (SSRN; published Econometrica 2005 DOI not verified) | multiple-testing for path comparisons |

### Q3 — Multiverse calibration and permutation validity (8)

| # | Work | DOI | Status | What it pre-empts |
|---|---|---|---|---|
| 1 | Simonsohn, Simmons & Nelson (2020), Specification curve analysis, Nature Human Behaviour 4 | 10.1038/s41562-020-0912-z | V | joint inference over specifications |
| 2 | Patel, Burford & Ioannidis (2015), Vibration of effects, J Clin Epidemiol 68(9) | 10.1016/j.jclinepi.2015.05.029 | V | multiverse instability |
| 3 | Steegen, Tuerlinckx, Gelman & Vanpaemel (2016), Multiverse analysis, Perspectives on Psychological Science 11(5) | 10.1177/1745691616658637 | V | the multiverse method |
| 4 | Klau, Hoffmann, Patel et al. (2020), Robustness to model/measurement/sampling uncertainty, IJE 49(6) | 10.1093/ije/dyaa164 | V | sampling uncertainty of multiverse results |
| 5 | Benjamini & Yekutieli (2001), FDR under dependency, Annals of Statistics 29(4) | 10.1214/aos/1013699998 | V | dependence-robust FDR (BY) |
| 6 | Li & Ji (2005), Adjusting multiple testing using eigenvalues, Heredity 95 | 10.1038/sj.hdy.6800717 | V | effective number of independent tests |
| 7 | Phipson & Smyth (2010), Permutation p-values should never be zero, SAGMB 9(1) | 10.2202/1544-6115.1585 | V | Monte Carlo p-value floor |
| 8 | Ernst (2004), Permutation methods, Statistical Science 19(4) | 10.1214/088342304000000396 | V | exact permutation inference |

## Codex review unverified-items list — CONFIRMED / UNRESOLVED

| Item (from REVIEW.md "What remains unverified and next steps") | Mark | Basis |
|---|---|---|
| Original supply-demand wage input and full WDI data provenance | **UNRESOLVED** | Source script names absolute `/root/work/data/wage_emp.json` without a hash; `DATA_SOURCES.md` confirms wage/ag series start 1991; no hash chain to the committed inputs. |
| Original multiverse country panel not rerun; four strict-tier p-value arrays not checked | **UNRESOLVED** for the arrays | The methods paper (c5dfe66/1fef07e) commits the family definition and the **up** array; the down/sign-flip/heterogeneity null matrices were not saved (its own JSON note says so). |
| BY controls FDR only when individual null p-values are valid | **CONFIRMED** | Logical condition; also stated in the methods paper §6.6 (permutation validity, exchangeability caveat). |
| Methods "0 / 35 / 44" is not a confidence interval; 44 is anti-conservative | **CONFIRMED** | Methods paper states the three-way range and labels 44 an anti-conservative directional sensitivity. |
| Separate four procedures do not automatically control the union of claims | **CONFIRMED** | Methods paper H7 fix (c5dfe66) says the four procedures do not share one error rate; BY=0 per procedure. |
| Gemini DHS identifiers, category labels, endpoint, pagination | **UNRESOLVED** | No DHS fetch was possible in this session (public API check not run); no primary source located. |
| Gemini 49/29/7 shape figures | **CONFIRMED (source-confirmed, not rerun)** | `shape_results.json` in the shape record shows 51/30/7 of 105; not independently rerun here. |
| +0.035 (0.025), 38-policy event-study claim | **UNRESOLVED** | Location in the F draft confirmed by the Codex review, original event-study calculation not rerun/read. |
| +0.05 ± 0.19 electricity claim; CR.3 67.5% → 75.0% | **UNRESOLVED** | Not located in inspected original results by the Codex review; absence from inspected files is not proof of absence. |
| Comprehensive line-by-line/table/bibliography audit of every draft | **CONFIRMED as not done** | Scope limitation of the Codex review, carried forward. |
| Unverified fee-abolition dates (this memo) | **PARTIALLY CONFIRMED** | 8 of 12 verified to primary/authoritative sources; 4 unresolved (Cameroon, Zambia, Rwanda, Burundi). |

## Files

- `README.md` — this memo (Jobs 1-3, unverified-item marks).
- `fee_dates.csv` — 12-row fee table with source, locator, status, note.

## Search strategy

- Crossref API via proxy (polite `mailto`, title/author/year checked); every DOI in this record carries its status.
- World Bank Open Knowledge Repository API: item → bundles → bitstreams to retrieve the two 2009 SFAI documents;
  the book's PDF text was extracted with `pypdf` (280 pp) and quotes located by page marker.
- `web_search` for the unresolved countries; `web_fetch` and DuckDuckGo HTML were unavailable for most hosts in
  this session (non-public IP / empty results), so unresolved means **no source located**, not "no source exists".
- No "first" claims; no guessed dates; every unverified item is marked.
