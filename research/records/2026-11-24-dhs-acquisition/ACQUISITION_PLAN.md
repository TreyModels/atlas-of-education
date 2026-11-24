# ACQUISITION_PLAN — DHS Individual Recode (IR) microdata

**Status:** access path documented and tested up to the login wall; **no gated file requested, downloaded or
bypassed**; no credentials anywhere in this repo, this log or the session.
**Date:** 2026-11-24 (Asia/Shanghai). **Branch:** `research/dhs-acquisition-2026-11-24` (base
`origin/research/handoff-2026-11-24`, head `51f9f02`). **Task:** task-2. **Owner:** dhs-scout.
**Record:** `research/records/2026-11-24-dhs-acquisition/`. **Preregistration:** [`PRE_REGISTRATION.md`](PRE_REGISTRATION.md)
(committed in the same push, before any data arrives).
**Evidence:** [`data/source_log.txt`](data/source_log.txt) (every URL + HTTP code),
[`data/dhs_ir_inventory_targets.csv`](data/dhs_ir_inventory_targets.csv) (the 92 target files),
[`data/ceb_education_cells.csv`](data/ceb_education_cells.csv) (cell-size evidence).

This is an **access-path job, not a scraper**. Every step below is a normal registered-user workflow on
`dhsprogram.com`. Nothing here circumvents the login: the earlier probe on
`research/dhs-micro-2026-11-23 @ 31ded00` had already established that direct flat-file URLs 404 and the
IPUMS API needs a key; we re-verified the wall (public file lists visible, download link = login page only)
and stopped there.

---

## 0. The exact ask, in one paragraph

> **Trey:** register (free, ~10 min) at <https://dhsprogram.com/data/new-user-registration.cfm>, then submit a
> dataset-access request with this project title and description —
> **"The Atlas of Education — schooling and completed fertility in DHS individual recodes"**, description:
> *"Research study of the individual-level association between women's education and children ever born,
> with a comparison between births-based and surviving-children-based fertility measures, using DHS standard
> Individual Recode files for 8 sub-Saharan African countries, 3 Southeast Asian benchmark countries and 3
> comparator countries. Analysis is observational, uses survey weights and clustered standard errors, and
> makes no causal claim."* — asking for **dataset access to 14 countries** (table in §3). After approval
> (DHS says **24–48 h, Monday–Friday, per country**), download the **92 Stata IR ZIP files (~538 MB; 72
> standard-DHS files = ~501 MB)** through Download Datasets → by survey, or the Download Manager. Keep them
> **outside the public repo** (DHS Terms forbid redistribution; the Atlas repo is public). Hand over the
> archive + a `sha256` manifest; the analyser then runs the pre-registered test. **If approval stalls, email
> `archive@dhsprogram.com` — do not substitute model/synthetic datasets.**

---

## 1. Why this is the biggest available upgrade

The closed Codex wave established the **macro regression wall** (`HANDOFF.md` §1; ledger
`research/records/2026-11-24-handoff/codex_wave_ledger.md`): aggregate country panels cannot separate the
competing micro mechanisms, MSE/BIC are degenerate, "robust everywhere" mislabels minority-effect worlds, and
**effective fertility and TFR are different constructs**. The E11 audit
(`origin/research/e11-fertility-audit-2026-11-25 @ e926575`) measured the construct gap: on 2,955 overlapping
country-years / 197 countries, **median |TFR − EFR| = 0.3042**, **max = 4.2677**, mean ratio 1.1749, level
correlation 0.9378; on the matched level ladder (n = 1,417; 109 countries; 1950–2010) the lead/lag ratio is
**0.541** for the surviving-children measure and **1.555** for the births measure. Numbers are quoted from that
committed record; the small sample-specific figures (2,955/0.3042/4.2677/0.541/1.555) match
`results/q1_construct_audit.json` there.

The two attempts so far used proxies: aggregate panels (macro wall) and **published DHS API cells**
(`research/dhs-micro-2026-11-23 @ 31ded00`: 81,962 cells, weighted country×survey FE models — explicitly
*ecological*, and its own report says the individual-level test "could NOT be run"). The IR microdata are the
first data that put **a woman's own schooling and her own children ever born in the same row**, which is the
only level at which the individual test can be run at all. That is the whole case for access.

---

## 2. The real route — registration → approved project → download

All five pages below were fetched on 2026-11-24 (HTTP 200; see `data/source_log.txt`). Quotations are from the
page text as served.

### 2.1 Registration (one-time, free, no institutional subscription)

- Page: <https://dhsprogram.com/data/new-user-registration.cfm> — "Request Access To Datasets".
- Required form fields (Step 1, verbatim from the form): **email address** (this becomes the username),
  **password** (8–15 characters), first name, last name, **institution/organisation name written out in full**
  (the form explicitly says not just the acronym), **institution/organisation type** (Depository Library;
  Govt. Organizations; Individual Researchers; NGO; Other; Private Agencies/Researchers; University Faculty;
  University Student), **country of residence**, **phone number including country code**, and email-alert
  preferences (DHS Newsletter / new survey datasets / survey-specific data alerts — the page recommends the
  survey-specific alerts).
- The same page states: *"Before you can download datasets, you must register as a DHS data user. Dataset
  access is only granted for legitimate research purposes."* and *"re-distribution of any DHS micro-level
  data, either directly or within any tool/dashboard, is not permitted."*
- Expect an **email confirmation step** before the account is active. The static page text does not spell
  the confirmation mechanics out — **UNVERIFIED**; it is the normal behaviour of the form flow.
- The site notes: the form does not work on mobile devices; do not use browser translation; all items in English.

### 2.2 Project request (this is what "approval" means)

From <https://dhsprogram.com/data/Access-Instructions.cfm> (verbatim):

- *"To request dataset access, you must first be a registered user of the website."*
- *"Access to DHS, MIS, AIS and SPA survey datasets (Surveys, HIV, and GPS) is requested and granted by
  country. This means that when approved, full access is granted to all unrestricted survey datasets for that
  country."*
- *"Dataset requests must include contact information, a research project title, and a description of the
  analysis you propose to perform with the data."*
- *"The DHS Program will normally review all data requests within 24 – 48 hours (Monday - Friday), and provide
  notification if access has been granted or additional project information is needed, before access can be
  granted."*
- *"If for some reason you requested a DHS datasets, but need to modify your request or give additional
  information to gain dataset approval, you can find the instructions in the video below."*
- **Restricted datasets:** *"A few datasets are restricted and are noted on the request form… Permission to
  access restricted datasets must be submitted after registration… the datasets made available by secure FTP."*
- **GPS/HIV/other biomarkers:** separate electronic Terms-of-Use acknowledgment inside the account.
- **Access is per country, not per file.** Fourteen countries ⇒ up to fourteen country-level grants (one
  request, or one per country if the form requires it). The 72 standard-DHS IR files are "unrestricted survey
  datasets"; the 20 MIS/AIS files should fall under the same country grant, but that is **UNVERIFIED** until
  the account shows them.

Contact for access problems (from the login page): **`archive@dhsprogram.com`**. Publications go to
**`references@dhsprogram.com`** (§2.4). API questions: `api@dhsprogram.com`.

### 2.3 Download

- Entry points: **Data → Download Datasets** → *by survey* (page lists every file for a survey with size and
  format; the Individual Recode block holds the IR files), or the **Download Manager** for many
  surveys/countries at once (recommended for 92 files).
- Distribution format: **all datasets are ZIP archives**. For the Stata format (`…DT.ZIP`) the archive contains
  `.DTA` (the system file), plus `.DCT` (Stata dictionary), `.DO` (Stata syntax), `.MAP` (layout/codebook),
  `.FRQ` / `.FRW` (unweighted / weighted frequency distributions), and — **IR and MR only** — a `.DOC` with
  country information (source: <https://dhsprogram.com/data/File-Types-and-Names.cfm>).
- Men's / couples' / birth / household / children's recodes are separate ZIPs; **we need only IR** (and,
  optionally, BR if a birth-history-only re-computation is wanted — the IR already contains the history).
- A dataset page is public and lists the files, but the only access link is
  `https://dhsprogram.com/data/dataset_admin/login_main.cfm` ("If you are a registered user, please login here
  to gain access to these files"). Confirmed on
  <https://dhsprogram.com/data/dataset/Malawi_Standard-DHS_2015.cfm> (2026-11-24).

### 2.4 Terms of Use — the de facto data-use agreement

There is **no separate countersigned DUA** for unrestricted survey files; the agreement is the account-level
acceptance of the Terms of Use (<https://dhsprogram.com/data/Terms-of-Use.cfm>) plus the country-level project
approval. The binding conditions, verbatim/paraphrased:

1. Use the data **only for the registered research/study**; a new purpose requires a new project request
   ("Create a New Project" in the account).
2. **Do not share the datasets** with other researchers without DHS's written consent.
3. Keep the files in a **secure location** not accessible to unauthorised users.
4. Treat all data as **confidential**; make no effort to identify any individual, household or enumeration area.
5. Publish **no results in which communities or individuals can be identified**.
6. No marketing or commercial use.
7. **No re-distribution of micro-level data, "either directly or within any tool/dashboard".**
8. Submit copies of resulting reports/publications to **references@dhsprogram.com**.
9. Country-specific extra conditions that bite here:
   - **Cambodia:** send **ten (10) copies** of any publication to National Institute of Statistics/MOH,
     386 Monivong Bd., Phnom Penh.
   - **Vietnam 2005:** submit any paper/report to **NIHE & GSO for approval *prior to publication*** (and send
     10 copies to each). This is a pre-publication approval requirement — a reason to use Vietnam 1997/2002 for
     the main analysis and treat 2005 as optional.

**Operational consequence for the Atlas (important).** The Atlas repository is public and the project ships a
public dashboard. Conditions 3, 5 and 7 mean: (a) microdata live **outside** the repo in a private, access-
controlled directory; (b) only code, hashes and **aggregate** outputs (cells with adequate cell sizes) are
committed; (c) no Atlas tool, dashboard or web page may serve DHS micro-level records, not even a single row.

### 2.5 Programme status — route is open, but in stabilised mode (read this before planning a deadline)

This matters because the funding environment changed after the Codex wave:

- **Feb 2025:** USAID support to the DHS Program ended. Per third-party reporting, **new online applications
  for DHS data were closed** and existing users could not add countries.
- **Jul 2025:** ICF received a **3-year Gates Foundation grant** ("Emergency Support to Stabilize the DHS
  Program") covering the website, the data archive, free access to tools/data, and completion of selected
  surveys.
- **Aug–Sep 2025:** DHS **reopened new registrations**; ~"we are now open for new registrations"; at least ten
  countries' new samples were expected to be released.

Sources (external, cited as sources — not instructions):
[IPUMS blog, 2025-09-03](https://blog.popdata.org/dhs-data-again-available-to-new-users/),
[DC Sociological Society, 2025-08-16](https://www.dcsociologicalsociety.org/news/13532577),
[DHS funding FAQ](https://dhsprogram.com/Who-We-Are/News-about-the-DHS-Program.cfm) (confirms the funding
facts; the "open for new registrations" sentence is a DHS announcement reported by the two links above, not
printed on the FAQ page we could fetch — **UNVERIFIED at primary source**).

**Our own check (2026-11-24):** the registration form is live, the access-instructions page still states the
24–48 h review, and **no closure notice appears** on the registration, login, access-instructions or FAQ pages
(`data/source_log.txt` §1). The IPUMS-DHS registration page still carries a **stale 2025-02-07 note** saying
DHS "is not currently reviewing new user applications" — that note is **superseded** by the Aug/Sep 2025
reopening and by the fact that the DHS form is open now. Verdict: **route confirmed to exist and to be open as
of the most recent verifiable statements; the current (Nov 2026) *processing* status and turnaround are
UNVERIFIED** — treat 24–48 h as DHS's stated norm, not a guarantee, and plan for a 1–2 week approval window.

---

## 3. File naming, and exactly which files to request

### 3.1 Naming convention (from DHS's own "File Types & Names" page)

`CCDDVV[FF]DS.ZIP` where

| Part | Meaning |
|---|---|
| `CC` | 2-letter country code (`MW` Malawi, `ET` Ethiopia, `UG` Uganda, `LS` Lesotho, `TZ` Tanzania, `KE` Kenya, `MZ` Mozambique, `GH` Ghana, `KH` Cambodia, `PH` Philippines, `VN` Vietnam, `BJ` Benin, `NM` Namibia, `SZ` Eswatini) |
| `DD` | 2-letter file type — **`IR` = Individual Recode** (women's file); also BR/KR/HR/PR/CR/MR/AR/GC/GE |
| `VV` | version code: survey sequence within the DHS phase + **release version** digit (phase digit 0–9 = first survey of that phase; letters A–H = second, I–Q = third, R–Z = fourth; the trailing character distinguishes release versions: `0`=release 0, `1`=release 1, …). Example: `MWIR7A` = Malawi IR, DHS-VII second survey, release version 1 |
| `[FF]` | format: **`DT` = Stata**, `FL` = flat ASCII, `SV` = SPSS, `SD` = SAS; **blank** = hierarchical ASCII |
| `DS` | data-structure code, SPA surveys only |

**Do not decode the year from `VV`.** It is a phase/sequence/release code, not a date, and two countries in the
same round can carry different codes (`MWIR7A` vs `KEIR8C`). Always take the exact `FileName` from
[`data/dhs_ir_inventory_targets.csv`](data/dhs_ir_inventory_targets.csv).

**Correction to the example in the task brief:** `MWIR7XDT` is **not a real file**. There is **no file
containing "7X" anywhere in the 15,518-record public inventory** (checked 2026-11-24), and the Malawi
2015-16 standard-DHS Individual Recode in Stata is **`MWIR7ADT.ZIP`** (19.1 MB hierarchical ASCII; 14.9 MB
Stata per the dataset page). Use `MWIR7ADT.ZIP`.

### 3.2 The 14 countries — Standard DHS first, MIS/AIS second

All 92 IR Stata files below are confirmed present in the public DHS file inventory (API pull 2026-11-24;
`FileType = Individual Recode`, `FileFormat = Stata`). "std/total" = standard-DHS rounds / all IR rounds
including MIS and AIS. MB = Stata ZIP bytes.

| ISO3 | Country | Standard-DHS IR (Stata) files: year → file | MIS/AIS extras | std/total | MB |
|---|---|---|---|---|---|
| MWI | Malawi | 1992: `MWIR22DT.ZIP`; 2000: `MWIR41DT.ZIP`; 2004: `MWIR4EDT.ZIP`; 2010: `MWIR61DT.ZIP`; 2015: `MWIR7ADT.ZIP`; 2024: `MWIR81DT.zip` | 2012: `MWIR6ADT.ZIP`; 2014: `MWIR72DT.ZIP`; 2017: `MWIR7IDT.ZIP` | 6/9 | 64.7 |
| ETH | Ethiopia | 2000: `ETIR41DT.ZIP`; 2005: `ETIR51dt.zip`; 2011: `ETIR61DT.ZIP`; 2016: `ETIR71DT.ZIP`; 2019: `ETIR81DT.ZIP`; 2024: `ETIR8ADT.zip` | — | 6/6 | 53.0 |
| UGA | Uganda | 1988: `UGIR01DT.ZIP`; 1995: `UGIR33DT.ZIP`; 2000: `UGIR41DT.ZIP`; 2006: `UGIR52DT.ZIP`; 2011: `UGIR61DT.ZIP`; 2016: `UGIR7BDT.ZIP` | 2009: `UGIR5ADT.ZIP`; 2011: `UGIR6ADT.ZIP`; 2014: `UGIR72DT.ZIP`; 2018: `UGIR7IDT.ZIP`; 2024: `UGIR91DT.zip` | 6/11 | 45.2 |
| LSO | Lesotho | 2004: `LSIR41DT.ZIP`; 2009: `LSIR61DT.ZIP`; 2014: `LSIR71DT.ZIP`; 2023: `LSIR81DT.ZIP` | — | 4/4 | 17.8 |
| TZA | Tanzania | 1992: `TZIR21DT.ZIP`; 1996: `TZIR3ADT.ZIP`; 1999: `TZIR41DT.ZIP`; 2004: `TZIR4IDT.ZIP`; 2010: `TZIR63DT.ZIP`; 2015: `TZIR7BDT.ZIP`; 2022: `TZIR82DT.ZIP` | 2003: `TZIR4Adt.zip`; 2007: `TZIR51DT.ZIP`; 2012: `TZIR6ADT.ZIP`; 2017: `TZIR7IDT.ZIP` | 7/11 | 56.0 |
| KEN | Kenya | 1989: `KEIR03DT.ZIP`; 1993: `KEIR33DT.ZIP`; 1998: `KEIR3ADT.ZIP`; 2003: `KEIR42DT.ZIP`; 2008: `KEIR52DT.ZIP`; 2014: `KEIR72DT.ZIP`; 2022: `KEIR8CDT.ZIP`; 2025: `KEIR91DT.zip` | 2015: `KEIR7ADT.ZIP`; 2020: `KEIR81DT.ZIP` | 8/10 | 67.2 |
| MOZ | Mozambique | 1997: `MZIR31DT.ZIP`; 2003: `MZIR41DT.ZIP`; 2011: `MZIR62DT.ZIP`; 2022: `MZIR82DT.zip` | 2009: `MZIR51DT.ZIP`; 2015: `MZIR71DT.ZIP`; 2018: `MZIR7ADT.ZIP` | 4/7 | 34.2 |
| GHA | Ghana | 1988: `GHIR02DT.ZIP`; 1993: `GHIR31DT.ZIP`; 1998: `GHIR41DT.ZIP`; 2003: `GHIR4BDT.ZIP`; 2008: `GHIR5ADT.ZIP`; 2014: `GHIR72DT.ZIP`; 2022: `GHIR8CDT.ZIP` | 2016: `GHIR7BDT.ZIP`; 2019: `GHIR82DT.ZIP` | 7/9 | 29.4 |
| KHM | Cambodia | 2000: `KHIR42dt.zip`; 2005: `KHIR51dt.zip`; 2010: `KHIR61DT.ZIP`; 2014: `KHIR73DT.ZIP`; 2021: `KHIR82DT.ZIP` | — | 5/5 | 47.7 |
| PHL | Philippines | 1993: `PHIR31DT.ZIP`; 1998: `PHIR3BDT.ZIP`; 2003: `PHIR41DT.ZIP`; 2008: `PHIR52DT.ZIP`; 2013: `PHIR61DT.ZIP`; 2017: `PHIR71DT.ZIP`; 2022: `PHIR82DT.ZIP` | — | 7/7 | 59.0 |
| VNM | Vietnam | 1997: `VNIR31DT.ZIP`; 2002: `VNIR41DT.ZIP` | 2005: `VNIR52DT.ZIP` | 2/3 | 5.5 |
| BEN | Benin | 1996: `BJIR31DT.ZIP`; 2001: `BJIR41DT.ZIP`; 2006: `BJIR51DT.ZIP`; 2012: `BJIR61DT.ZIP`; 2017: `BJIR71DT.ZIP` | — | 5/5 | 37.2 |
| NAM | Namibia | 1992: `NMIR21DT.ZIP`; 2000: `NMIR41DT.ZIP`; 2006: `NMIR51dt.zip`; 2013: `NMIR61DT.ZIP` | — | 4/4 | 17.7 |
| SWZ | Eswatini | 2006: `SZIR51dt.zip` | — | 1/1 | 3.4 |

**Total: 92 files, 538.0 MB; 72 standard-DHS files, 501.1 MB.** Per-file survey metadata (fieldwork window,
unweighted women, sample points, women's universe) is in the CSV.

Tiering for the download (so a partial approval still unblocks work):

- **Tier 1 (minimum viable):** all **standard-DHS** IR files for **MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA**
  (48 files) + **KHM, PHL** (12 files) + **BEN, NAM** (9 files) = **69 files, 493.6 MB**. This supports the
  cohort FE design (≥ 4 rounds per country except SWZ and VNM).
- **Tier 2:** **SWZ 2006** (1 file — only DHS round Eswatini has; it cannot support cohort-vs-round separation
  on its own, so it enters only as a descriptive comparator) and **VNM 1997 + 2002** (2 files; both are
  *ever-married women* universes, see §8).
- **Tier 3 (optional, robustness only):** the 20 **MIS/AIS** IR files. Published DHS API cells show
  education × CEB aggregates for several of them (e.g. MWI 2012/2014/2017, TZA 2007/2012/2015/2017, GHA
  2016/2019, KEN 2015/2020, UGA 2009/2014/2018, MOZ 2015/2018), which *implies* `v201` and the education
  variables are in those IR files — but **whether `v133` (single years) and the full `v206/v207` set are present
  is UNVERIFIED** until a file is opened. Keep them out of the main specification.

Country-round gaps to state up front (they constrain the design, not the access): **Ethiopia's first DHS is
2000** and **Lesotho's first is 2004**, so neither has a pre-1995 / pre-2000 round; **Eswatini has one round**;
**Vietnam stops at 2002 (+2005 AIS)**. The E8 fee-abolition event years (MWI 1994, ETH 1995, UGA 1997, LSO
2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005 — the 8 VERIFIED dates in
`research/records/2026-11-25-e6e8-sequencing/data/fee_dates.csv`) bracket these rounds well for MWI/UGA/TZA/
KEN/MOZ/GHA, but **ETH and LSO are post-treatment only** on DHS data.

---

## 4. Variables — exact names, labels, and derivations

Definitions are quoted from the **DHS Recode Manual** (DHS-7 edition,
<https://dhsprogram.com/pubs/pdf/DHSG4/Recode7_DHS_10Sep2018_DHSG4.pdf>, fetched 200; DHS-6 edition
<https://dhsprogram.com/pubs/pdf/DHSG4/Recode6_DHS_22March2013_DHSG4.pdf> used for the cross-checks below).
The same core variable names appear in the DHS-8 files.

### 4.1 The variables we actually need

| Variable | DHS label (Recode Manual) | Use in the test |
|---|---|---|
| `v005` | **Sample weight**, 8 digits with **6 implied decimals** — divide by 1,000,000 before weighting; normalised so weighted N = unweighted N on the full file | Survey weights |
| `v008` | **Century month code (CMC) of date of interview** | Survey round timing; age/cohort arithmetic |
| `v011` | **CMC of date of birth of the respondent** (imputed where needed) | **Birth cohort**; age check against `v012` |
| `v012` | Current age in completed years, computed from `v011` and `v008` | Age control; completed-fertility sample (40–49) |
| `v021` | **Primary sampling unit** (usually = cluster) | Clustered SEs / `svyset` PSU |
| `v022` | **Sample strata for sampling errors** | Strata for design-based SEs |
| `v023` | Stratification used in the sample design | Alternative/additional stratum control |
| `v024` | **De facto region of residence** (copy of `v101`) | Region FE |
| `v025` | **De facto type of place of residence** (urban/rural; copy of `v102`) | Urban/rural control and split |
| `v106` | **Highest education level attended** — 0 no education, 1 primary, 2 secondary, 3 higher | **Main schooling regressor** (4 categories) |
| `v107` | Highest year of education at that level | Input to `v133`; country-specific |
| `v133` | **Education in single years**, constructed as `v106=0→0`, `1→v107`, `2→v107+x`, `3→v107+y` (x, y country-specific) | **Dose** measure (linear/spline), and the "years of schooling" gradient |
| `v149` | Educational achievement recode: none / incomplete primary / complete primary / incomplete secondary / complete secondary / higher | Alternate schooling specification (robustness) |
| `v190` | Wealth index (quintile) | Control / mediator (see §4.3) |
| `v201` | **Total number of children ever born** — explicitly *"the sum of variables V202 to V207"* | **Births-based outcome (CEB)** |
| `v202` | Total number of sons living at home | component |
| `v203` | Total number of daughters living at home | component |
| `v204` | Total number of sons living away from home | component |
| `v205` | Total number of daughters living away from home | component |
| `v206` | **Total number of sons who have died** | **surviving-children outcome** |
| `v207` | **Total number of daughters who have died** | **surviving-children outcome** |
| `v224` | Number of entries in the birth history (≤ 20; `v201` can exceed it) | Birth-history work; never use as CEB |
| `v212` | Age of respondent at first birth | Tempo descriptor (secondary) |

Identification columns for merging/audit: `v001` (cluster), `v002` (household), `v003` (respondent line),
`v000` (country/phase/rec version), `v007`/`v006` (year/month of interview).

### 4.2 Derived constructs (the part that must not be fudged)

```text
w          = v005 / 1_000_000                      # survey weight
birth_year = floor(v011 / 12)                      # CMC -> calendar year
cohort5    = 5 * floor(birth_year / 5)             # 5-year birth cohort
age        = floor((v008 - v011) / 12)             # should equal v012 (+-1); assert it
births     = v201                                   # BIRTHS-based, cumulative/quantum-type
surviving  = v201 - v206 - v207                     # SURVIVING-CHILDREN measure (the EFR analog)
```

- `surviving` is **not** a period rate and **must never be called "TFR"**. It is the individual-level analogue
  of the project's `effective_fertility` (surviving children per woman) defined in E11 §1.1. `births = v201`
  is the individual-level analogue of the births measure (CEB, not a period TFR either).
- **Period TFR is a different object and is computed at the survey level, not per woman**: from the birth
  history (`REC21` inside the IR file) using the DHS procedure in the
  [Guide to DHS Statistics](https://dhsprogram.com/data/Guide-to-DHS-Statistics/index.htm) — age-specific
  fertility rates over the reference period before the survey, summed × 5. Its exact reference window and
  denominator must be copied from the current Guide chapter when the code is written (**UNVERIFIED here**:
  the Guide is served as a JS app and the fertility chapter could not be fetched as static text on 2026-11-24).
  It is used only as a survey-level comparison/validation series, **never** as an individual outcome.
- Education encodings differ by phase and country (`x`, `y` in `v133` are country-specific). Log the
  country-specific education codes from the `.DOC`/`.FRQ` in each ZIP; never assume the same mapping across
  rounds (§8).
- Missing/`don't know` codes for education are 8/9 after recoding; `v201`–`v207` should be non-missing for
  eligible women — assert, don't impute silently.

### 4.3 The EFR/TFR construct split as an *individual-level* question

E11 established, at the macro level, that the births measure and the surviving-children measure behave
differently (lead/lag **1.555 vs 0.541**; median |diff| **0.3042**; max **4.2677**). The IR data let us ask the
individual-level version of the same question: **does the within-cohort schooling coefficient change sign, or
change materially in size, when the outcome is births vs surviving children?** That is pre-registered in
[`PRE_REGISTRATION.md`](PRE_REGISTRATION.md) §5 as a construct × schooling interaction on the stacked outcomes,
with the woman as the clustering unit. Neither outcome "corrects" the other; a sign flip would be a **construct
finding**, a magnitude difference a **materiality finding**, and equality a **no-difference finding**. All three
are reportable; none is causal.

Wealth (`v190`) is treated as a **mediator/descendant of schooling**, not a confounder: it enters as a
robustness column, never as the headline specification (§8, and the preregistration's M3).

---

## 5. What is obtainable **without** login — and what is not

### 5.1 Public, no account, no key (all verified 2026-11-24)

| Resource | URL | What you get | Limits |
|---|---|---|---|
| **DHS Program API** | <https://api.dhsprogram.com> | 4,655 indicators; 377 surveys; **15,518 dataset/file records** (names, sizes, formats, survey type, fieldwork dates, unweighted women, sample points, women's universe); **indicator data** with `DenominatorWeighted` *and* `DenominatorUnweighted`, CIs | **Aggregates and metadata only** — no microdata, and the dataset endpoint returns *metadata*, not a download link. **No API key was required** in our tests (indicators/surveys/datasets/data all HTTP 200). The API Terms & Conditions page is a JS app (`/#/terms.cfm`) and could not be read mechanically → **UNVERIFIED**; attribute the DHS Program and check the terms in a browser before bulk pulling |
| **STATcompiler** | <https://www.statcompiler.com/en/> | Published indicator tables by country/survey/background characteristic | Aggregates; no individual records |
| **Dataset landing pages** | `https://dhsprogram.com/data/dataset/<Country>_<SurveyType>_<Year>.cfm` | Full **file list** with sizes/formats, survey description | Download link = login page only |
| **Published reports** | DHS final reports / Key Indicators Reports / STATcompiler tables (public PDFs) | Published TFR **as DHS defines it**, sample designs, universes, field dates | Publication-level, not woman-level |
| **Recode Manual / Guide / questionnaires** | <https://dhsprogram.com/pubs/pdf/DHSG4/Recode7_DHS_10Sep2018_DHSG4.pdf>, <https://dhsprogram.com/data/Guide-to-DHS-Statistics/index.htm> | Variable definitions, coding, file structures | Documentation only |
| **Model datasets** | <https://dhsprogram.com/data/Model-Datasets.cfm>, `Download-Model-Datasets.cfm` | Synthetic practice files on the DHS-6 questionnaire (`zzir62*` etc.), **no registration** | **Synthetic. Not country data. Not an acceptable substitute for the real test** (project rule; also §7) |
| **IPUMS-DHS** | <https://www.idhsdata.org/idhs/register.shtml> | Harmonised DHS extracts | Registration **is managed by The DHS Program** — same approval wall; existing DHS approval carries over. Useful only *after* the DHS account exists, for harmonised education coding |

What the API already buys us (this is not nothing): the earlier branch pulled **81,962 published cells**
(`research/dhs-micro-2026-11-23 @ 31ded00` — 377 surveys, 87 countries) and ran the canonical gradient as an
**ecological** association: primary −0.57 (SE 0.06), secondary −1.62 (0.17), higher −2.54 (0.24) children
relative to no education, n = 1,291 cells, 86 countries; the per-survey gradient negative in 99% of 346 surveys.
Those numbers are **quoted from that committed record, not recomputed here**; they motivate the test and cannot
substitute for it.

For the present record we recomputed independently from the API, in this session:
15,518 dataset records / 2,005 IR records / 2,000 unique IR filenames / 85 countries; 92 target-country IR
Stata files (538.0 MB); and 318 published education cells for women 40–49 with denominators (§7).

### 5.2 Requires the DUA / approved account

- All **microdata**: IR (women), BR (births), KR (children), HR (household), PR (members), CR, MR, AR — I.e.
  every individual-level record. The Atlas test needs **IR only**.
- **GPS / geospatial** and **HIV / other biomarker** datasets: additional Terms-of-Use acknowledgment and
  (for restricted files) secure-FTP delivery.
- Any *new* purpose beyond the registered project description: a new request.

### 5.3 Do not do

- Do not scrape the gated files, guess download URLs, use a colleague's account, or publish file contents.
  The prior probe already showed that guessed flat-file URLs return **404** and the IPUMS extract API returns
  **403** without a key (`data/source_log.txt` §3, quoting `research/dhs-micro-2026-11-23 @ 31ded00`).
- Do not put credentials in the repo, logs, chat or issue trackers. Register with Trey's own account; the
  analyser never needs the password.

---

## 6. Concrete steps for Trey, with turnaround

| # | Step | Time | Notes |
|---|---|---|---|
| 1 | Register at <https://dhsprogram.com/data/new-user-registration.cfm> | ~10 min | Use full institution name; use a desktop browser; confirm the email link |
| 2 | Log in → create the project request: title + description exactly as in §0; select **the 14 countries** | ~5 min | If the form allows only one country per request, submit 14 — the approval is per country anyway |
| 3 | Wait for approval notifications | **24–48 h per DHS's stated norm (Mon–Fri)**; plan 1–2 weeks | If >3 working days with no reply, email `archive@dhsprogram.com` quoting the project title; if the request needs more detail, the account shows how to amend it |
| 4 | Download **Tier 1 = 69 standard-DHS IR Stata ZIPs (493.6 MB)**, then Tier 2 (SWZ 2006, VNM 1997/2002), then optionally Tier 3 MIS/AIS | ~30–60 min on a normal connection | Use **Download Manager** for many surveys; verify each ZIP is a valid archive and matches the expected byte size in the CSV |
| 5 | Store outside the repo, in a directory only you/analyst can read (e.g. an encrypted disk image or a private server path `~/dhs_microdata/`); **never** `git add` it | ~10 min | DHS Terms 3, 7 |
| 6 | Produce a `sha256` manifest (`shasum -a 256 *.ZIP > MANIFEST.sha256`) and note the download date; hand it to the analyser with the directory path | ~5 min | The manifest and the manifest *alone* may be committed — no data |
| 7 | Record the account-level facts the record needs: approval date, countries approved, any country refused, DHS release version strings (`v000`) | ~5 min | Goes in a short `ACCESS_LOG.md` in the record dir (no credentials) |

**Turnaround summary:** registered account same day; **country approvals 1–2 weeks realistically** (DHS says
24–48 h after the request is reviewed, and it is per country); download under an hour; verification checklist
(§7) ~half a day; the pre-registered analysis itself is a day of compute-light work once the files are present.
**No step in this chain requires the analyser to hold a password.**

---

## 7. Verification checklist on arrival — before any analysis

Run this on every file; log results into a `VERIFICATION.md` in the record dir. Expected values for each file
are in [`data/dhs_ir_inventory_targets.csv`](data/dhs_ir_inventory_targets.csv).

**Archive integrity**

1. ZIP opens; members include `.DTA`, `.DCT`, `.DO`, `.MAP`, `.FRQ`, `.FRW`, and (IR files) `.DOC`.
2. ZIP byte size matches the CSV's `bytes_stata` (the API's FileSize) within rounding; record `sha256`.
3. `FileName` is **exactly** the one in the CSV (watch case: `…DT.ZIP` vs `…dt.zip`; and release digits
   `7A` vs `72` vs `7I` — these are different files).

**Structural checks in the `.DTA`**

4. Number of rows equals the survey's unweighted number of women (`NumberOfWomen` in the CSV) for
   standard-DHS files. Small mismatches need an explanation (e.g. the IR file can include a few women outside
   the 15–49 interview universe in early phases) — **do not silently accept**.
5. `v001`+`v002`+`v003` is unique (no duplicate respondents).
6. `v021` distinct values ≈ `NumberOfSamplePoints` (the CSV column `sample_points`); report both.
7. `v012` range = 15–49 (or the universe in `universe_of_women` — **Vietnam 1997/2002 are ever-married women**
   and the file/universe must match the CSV's `Ever Married Women`); `v025` has no missing values.
8. `v008` (interview CMC) falls inside the fieldwork window in the CSV (`fieldwork_start`/`fieldwork_end`)
   ± a month; `floor(v011/12)` is plausible for the reported ages; `|v012 − age_from_CMCs| ≤ 1`.
9. `v005` sums: weighted N ≈ unweighted N (to ~1%); no zeros/negatives; weight range plausible
   (normalised weights ≈ 1e6 × design effect).
10. `v201 == v202+v203+v204+v205+v206+v207` for every row (the Recode Manual states this identity);
    `v206+v207 ≤ v201`; no negative `surviving = v201 − v206 − v207`.
11. `v106` ∈ {0,1,2,3} (plus documented missing codes); `v133` ∈ 0–25 (with 99 = missing); `v149` ∈ 0–5.
12. `v190` ∈ 1–5; region `v024` non-missing and its count plausible for the country.

**Substantive checks (catch a wrong file or a broken merge)**

13. Mean `v201` by 5-year age group rises monotonically to ages 40–49 and plateaus near the country's
    completed fertility in that round (published TFR for the survey is in the final report; the *level* of CEB
    at 45–49 is a cumulative measure, not the period TFR — compare orders of magnitude only).
14. Mean `v201` falls monotonically across `v106` categories (0 → 1 → 2 → 3) in every survey; if not, stop and
    investigate coding before running the model.
15. Share with any child death (`v206+v207 > 0`) is plausible for the country/period (typically ~10–25% in
    these SSA rounds; Vietnam lower); dead-children counts ≤ 10.
16. Cross-check one cell against the public API: e.g. Malawi 2015-16 **mean CEB for women 40–49 by education**
    should reproduce the published cell value in `data/ceb_education_cells.csv` (same survey, education,
    women 40–49) within rounding of the published precision. Do this for **at least two countries/two rounds**
    before trusting the weights.
17. Log the release string `v000` and the `.DOC`/`.FRQ` metadata; confirm the education categories actually
    present match what the manual implies, and record the country-specific `x`,`y` used for `v133`.

**Provenance**

18. Write down, per file: URL path, download timestamp, sha256, DHS release code, and the exact `FileName`.
    These go in `ACCESS_LOG.md`/`VERIFICATION.md`. If a file is re-released by DHS under the same name, the
    sha256 will differ — that is a version event, not an error, and must be recorded, not "fixed".

Any failure at items 4–12 is a **stop** condition: do not run the pre-registered model on a file that fails
structural checks; report the file and the failure.

---

## 8. Risks — what can go wrong, with numbers where we have them

### 8.1 Cohort cell sizes (the binding constraint)

Using the public API's published education cells for women 40–49 (which already pool two 5-year cohorts),
across **318 cells in 89 survey-rounds** of the 14 countries:

- median cell size **367** women; range **25–2,841**;
- the **"higher education"** cell has median **75** women, **min 25** (56 rounds have a higher-ed cell at all;
  **38** of those cells are below 100 women);
- **55 of 89** survey-rounds have at least one education cell below 100 women.

Splitting to a single 5-year birth cohort roughly **halves** these counts, so expect a median of ~180 and
higher-education cells of ~35 women per cohort. Consequences: (i) the higher-education category is unusable as
a cohort-level estimate in many rounds — pool it with secondary for cohort cells, or report only the pooled
secondary+ contrast; (ii) pre-declare a **minimum cell floor of 50 women** and wider cohorts (10-year) where the
floor fails; (iii) a null or unstable higher-ed coefficient in small cohorts is a **precision** result, not
evidence about behaviour. Source: [`data/ceb_education_cells.csv`](data/ceb_education_cells.csv) (API
`FE_FRTY_W_MNC`, `breakdown=background`).

### 8.2 Weights and design

`v005` is normalised **within survey** (weighted N = unweighted N on the file), so pooling rounds does not by
itself weight countries by population. Options: (a) renormalise weights so each survey-round has total weight
proportional to its population of women 15–49 (external denominators) or equal weight per round (state which);
(b) always report the unweighted result next to the weighted one. Standard errors must be **design-based**:
`svyset v021 [pw=v005/1e6], strata(v022)` with the subpopulation option for the 40–49 subset (never drop rows
before `svyset`). Some early rounds have large design effects; naive SEs will be too small.

### 8.3 Urban/rural and geography

`v025` is the de facto residence; urban shares differ enormously across these 14 countries and change over
time, and some rounds oversample urban areas. Region (`v024`) boundaries change between rounds, so region FE are
**within-round** controls only — do not interpret a region coefficient across rounds. The urban/rural contrast
is itself a pre-declared heterogeneity split, not a nuisance to be washed out.

### 8.4 Survey-year sparsity and design identifiability

Rounds are irregularly spaced (e.g. Malawi 1992, 2000, 2004, 2010, 2015, 2024; Kenya 1989 … 2025). With
**cohort FE + round FE**, only cohorts observed in more than one round identify the model; young cohorts appear
in only one or two rounds. Consequences: the identifying variation is "older cohorts in later rounds", which is
exactly where survivorship/recall problems are worst; and countries with **1 round (Eswatini)** or **2 rounds
(Vietnam)** cannot contribute to a cohort-vs-round separation at all — they are descriptive comparators only.
Ethiopia (first round 2000) and Lesotho (first round 2004) cannot be used as pre/post fee-abolition evidence,
whatever their E8 status.

### 8.5 Comparability across rounds

The manual is explicit that `v133` is built with **country-specific** years-to-complete-primary (`x`) and
years-to-complete-secondary (`y`), and `v106`'s "secondary" spans very different attainment as systems massify
(the earlier branch's own cell analysis found the *gradient* attenuating in later cohorts and interpreted it as
composition — `research/dhs-micro-2026-11-23 @ 31ded00`). Questionnaire content, contraceptive availability,
marriage timing and child-mortality regimes all shift. Therefore: (i) never pool raw education categories
across countries without documenting the country code; (ii) include **round × cohort** FE where possible, so
the comparison is within round and within cohort; (iii) report the per-round gradient next to the pooled one —
a pooled coefficient that hides sign flips across rounds is exactly the "robust everywhere" error that Q3
documented (mislabelling 87% of minority-effect worlds).

### 8.6 What cross-sectional IR can and cannot say

- One row per woman, measured **once**, at interview. `v201` is cumulative at her age — completed only for the
  40–49 group; for younger women it is **truncated** (right-censored), so they cannot enter the main model.
- **Survivorship/selection:** women who died, migrated or were absent are not in the sample; the sample is
  women in sampled households. In high-mortality, high-migration settings this is not ignorable.
- **Recall and imputation:** birth dates are imputed where incomplete; the manual flags imputed dates.
- **No identification:** this design identifies a **within-cohort, within-round association** conditional on
  observed controls. It cannot separate schooling from family background, ability, marriage-market or
  community effects; no instrument, no policy discontinuity, no pre-trends are available in these data alone
  (the fee-abolition event study E8 is a separate, aggregate design with its own limits). No causal language.
- **Construct limits:** the births measure and the surviving-children measure answer different questions (E11).
  Neither is a period TFR; the period TFR is a survey-level rate computed from the birth history. Any statement
  that treats one as a correction of the other is wrong, and the plan says so.
- **Aggregation trap:** the same IR data can also produce the country×survey×education cells the API publishes;
  reproducing those cells is a *sanity check*, not the individual test. The individual test is only the
  woman-level model in the preregistration.

### 8.7 Compliance / operational risks

- **No redistribution, no dashboards** (Terms 7): the Atlas is public; the data must sit outside the repo and
  never be embedded in any Atlas page, API or downloadable artifact.
- **Publication obligations:** send outputs to `references@dhsprogram.com`; Cambodia (10 copies) and Vietnam
  2005 (pre-publication approval by NIHE & GSO) need handling — prefer Vietnam 1997/2002 and flag Cambodia in
  any Cambodia-based output.
- **Approval risk:** country approvals are discretionary; a refusal for one country removes it from the design
  and must be reported, not worked around. If approvals stall, email `archive@dhsprogram.com`; escalate to a
  co-investigator with an institutional account only with Trey's decision.
- **Funding risk:** the programme runs on interim/Gates funding (2025–2028); archive services could be
  interrupted. Mitigation: download the full Tier 1+2 set in one pass while access is open, keep the sha256
  manifest.
- **Versioning risk:** same-named re-releases. Mitigation: record sha256 and `v000`; state the exact vintage
  in every table.

---

## 9. Limits of this plan (stated so nobody over-reads it)

- **This record did not see a single DHS microdata file.** Everything about variables comes from the Recode
  Manual and the public metadata; every expectation in §7 is an expectation, not an observation.
- Numeric claims have mixed provenance, and are labelled accordingly: the **macro construct** figures are
  quoted from E11's committed record; the **API inventory / cell-size** figures were **recomputed here on
  2026-11-24**; anything else is marked UNVERIFIED at the point of use or in `data/source_log.txt`.
- Synthetic/model datasets are **not** a fallback for the real test. If the data do not arrive, the record says
  so and the individual test stays unrun (as it did on `research/dhs-micro-2026-11-23`).
- Access is a normal registered-user workflow with a discretionary country-level review. It is not guaranteed,
  not automatable, and must not be worked around.

---

## 10. Sources (all fetched 2026-11-24 unless noted; HTTP codes in `data/source_log.txt`)

**DHS Program (primary)**
- Registration: <https://dhsprogram.com/data/new-user-registration.cfm>
- Access instructions / approval flow: <https://dhsprogram.com/data/Access-Instructions.cfm>
- Terms of Use: <https://dhsprogram.com/data/Terms-of-Use.cfm>
- Dataset login / contact: <https://dhsprogram.com/data/dataset_admin/login_main.cfm>
- File types and names: <https://dhsprogram.com/data/File-Types-and-Names.cfm>
- Available datasets: <https://dhsprogram.com/data/available-datasets.cfm>
- Model datasets: <https://dhsprogram.com/data/Model-Datasets.cfm> and
  <https://dhsprogram.com/data/Download-Model-Datasets.cfm>
- Data variables & definitions: <https://dhsprogram.com/data/Data-Variables-and-Definitions.cfm>
- Guide to DHS Statistics: <https://dhsprogram.com/data/Guide-to-DHS-Statistics/index.htm>
- DHS Recode Manual, DHS-7: <https://dhsprogram.com/pubs/pdf/DHSG4/Recode7_DHS_10Sep2018_DHSG4.pdf>
- DHS Recode Manual, DHS-6: <https://dhsprogram.com/pubs/pdf/DHSG4/Recode6_DHS_22March2013_DHSG4.pdf>
- Funding FAQ: <https://dhsprogram.com/Who-We-Are/News-about-the-DHS-Program.cfm>
- Public API: <https://api.dhsprogram.com> (endpoints and behaviour in `data/source_log.txt` §2)
- STATcompiler: <https://www.statcompiler.com/en/>

**Programme status (third-party)**
- IPUMS blog, 2025-09-03, "DHS Data Again Available to New Users":
  <https://blog.popdata.org/dhs-data-again-available-to-new-users/>
- DC Sociological Society, 2025-08-16, "DHS is processing new registrations":
  <https://www.dcsociologicalsociety.org/news/13532577>
- IPUMS-DHS registration (managed by The DHS Program, stale 2025-02-07 note):
  <https://www.idhsdata.org/idhs/register.shtml>

**Project records cited**
- `HANDOFF.md`; `research/records/2026-11-24-handoff/codex_wave_ledger.md` (this branch, base `51f9f02`).
- E11 audit: `research/records/2026-11-25-e11-fertility-audit/REPORT.md` and
  `results/q1_construct_audit.json` on `origin/research/e11-fertility-audit-2026-11-25 @ e926575`.
- Earlier DHS attempt: `research/records/2026-11-23-dhs-micro/` on
  `origin/research/dhs-micro-2026-11-23 @ 31ded00`.
- E8 verified fee dates: `research/records/2026-11-25-e6e8-sequencing/data/fee_dates.csv` on
  `origin/research/e6e8-sequencing-2026-11-25 @ 2d19da7`.
