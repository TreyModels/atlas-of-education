# Codex source verification — task-49

**Owner:** novelty-review. **Branch:** `research/codex-source-verification-2026-11-25`.
**Date:** 24 November 2026. No compute; web + Crossref only.

Read first: `origin/research/codex-handoff-run-2026-11-24:research/records/2026-11-24-codex-review/REVIEW.md`
and `findings.csv`; handoff `LETTER_FOR_DEEPSEEK.md`/`SYNTHETIC.md`; assessment record
`origin/research/assessment-and-next-experiments-2026-11-24:research/records/2026-11-24-assessment-and-next-experiments/`
(`NEXT_EXPERIMENTS.md` E6/E8, `DATA_SOURCES.md`).

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

*(to be completed in this record — GGDC 10-Sector, PWT labour share/employment, WDI urbanisation/sector VA, and
whether any pre-1990 wage-employment series exists)*

## Job 3 — Prior art for Q1/Q2/Q3

*(to be completed in this record — 5-8 works per question with DOI + Crossref status)*

## Codex review unverified-items list

*(to be completed in this record — CONFIRMED/UNRESOLVED per item)*

## Search strategy

- Crossref API via proxy (polite `mailto`, title/author/year checked); every DOI in this record carries its status.
- World Bank Open Knowledge Repository API: item → bundles → bitstreams to retrieve the two 2009 SFAI documents;
  the book's PDF text was extracted with `pypdf` (280 pp) and quotes located by page marker.
- `web_search` for the unresolved countries; `web_fetch` and DuckDuckGo HTML were unavailable for most hosts in
  this session (non-public IP / empty results), so unresolved means **no source located**, not "no source exists".
- No "first" claims; no guessed dates; every unverified item is marked.
