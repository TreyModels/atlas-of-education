# WEB_BASELINE_NOTES — A8 public-source baseline search (first batch)

`data-hunter`, 2026-11-20. Public sources only; no credentialed requests; no imputation as observation. Access status and effective citation for everything added to `BASELINE_SERIES.csv`, `SCHOOL_EXPANSION.csv` and `POLICY_TIMELINE.csv`.

## Sources obtained

| Source | URL | HTTP | Used for |
|---|---|---|---|
| PIDS (2025), *Making Philippine Education Reforms and Interventions More Transformative* (7.46 MB PDF, 329 pp) | `https://pidswebs.pids.gov.ph/CDN/document/pidsbk2025-Education.pdf` | 200 | regional attainment/inequality table (ch.3 Table 1, p.86); high-school PTR 37→27→24 (ch.4 pp.97–98); DepEd teacher hiring 2012–16 (~200k kindergarten/elementary, ~40k SHS); HEI/free-tuition discussion (ch.9); 4Ps/feeding programme material (ch.10) |
| WTO case study, *Services Export Promotion: The Case of Philippine IT-BPM* (28 pp) | `https://www.wto.org/english/tratop_e/ts4d_e/case_studies_e/philippines.pdf` | 200 | services exports context (services exports USD 52bn in 2024 vs merchandise 55bn); explicitly notes **"no systematic public data on IT-BPM program graduates and employment outcomes"**; TWSP 2011 IT-BPM allocation PHP 500m, 70% employment rate among beneficiaries |
| PRC exam results pages | `https://prc.gov.ph/articles/exam-results` | 200 | nurse licensure pages exist but are per-examination; **no annual aggregate licensure series extracted** |
| IBPAP | `https://www.ibpap.org/` | 200 | industry site reachable; FTE/revenue figures are JS chart widgets, **not extractable as tables** |
| World Bank Enterprise Surveys PHL 2015 country profile | `enterprisesurveys.org` PDF (archived in `04_data/econ_round2/raw/`) | 200 | firm constraints; **no education-credential table**; 2023 wave not obtained |

## Sources blocked (recorded; not worked around)

`psa.gov.ph` **403** (all paths); `deped.gov.ph` **403**; `officialgazette.gov.ph` **403**; `ched.gov.ph` **403**; `legacy.senate.gov.ph` **403**; `neda.gov.ph` **DNS/000**; `dbm.gov.ph` **DNS/000**; Enterprise Surveys API **000**; ILOSTAT **403** (earlier); OECD **403** (earlier).

## What these numbers can and cannot support

- **Can support:** PHL high-school PTR trend (37 in 2000–2011 → 27 in 2014 → 24 in 2017) as the "state push — teachers" mechanism evidence; the 2012–16 hiring scale (~200k + ~40k) as an order-of-magnitude supply shock (marked `check`, not precise); regional attainment/inequality levels for the two cohorts as portability benchmarks; dated policy events (K-12 2013, free SHS 2016, RA 10931 2017/2018, 4Ps 2008).
- **Cannot support (yet):** a PHL **school/classroom count series** (DepEd 403) — so "places" is currently only evidenced through teachers/PTR, not construction; **pre-1999 completion/attainment series** (no accessible table found; UIS archive pages not probed); **IT-BPM employment counts** (industry figures are behind JS charts or not public); **nurse licensure/deployment counts** (PRC per-exam pages; POEA/DMW blocked); **regional sector employment for Bartik** (PSA blocked).

## Policy dates added (with confidence)

K-12 RA 10533 (signed 2013; first SHS cohort SY2016-17; first K-12 graduates 2018) — `fact` (workspace papers). Free SHS tuition SY2016-17 — `fact (not re-verified this pass)` because the Official Gazette returned 403. RA 10931 free tertiary (signed 2017-08-03, IRR March 2018, effective AY 2018-19) — same caveat; PIDS 2025 ch.9 discusses it. 4Ps launched 2008, institutionalised RA 11310 (2019) — same caveat. **US nurse visa expansion 2005–06 — `UNVERIFIED`**: the event is in the handoff as a demand-pull lead but I could not verify instrument or dates from a public source; do not treat as dated evidence until someone gets the primary source.

## Next steps (if A8 continues)

1. Probe `uis.unesco.org` archived pages and `unesdoc` via Wayback for PHL completion tables before 1999 (UIS used to publish country tables in EFA GMR annexes; the 2002–2009 reports' statistical annexes are the realistic source).
2. PSA: a one-page public "statistical tables" mirror may exist under rssoXX.psa.gov.ph subdomains (some RSSO pages returned 200 earlier in a different context) — try regional RSSO subdomains for LFS tables.
3. DepEd: try Wayback captures of `deped.gov.ph/datasets/` and the EBEIS pages for school/teacher counts.
4. PRC: scrape per-examination NLE results pages if an aggregate series is needed (tens of pages; defer).
5. CHN provinces: needs a Chinese-language NBS provincial yearbook source; not attempted.
