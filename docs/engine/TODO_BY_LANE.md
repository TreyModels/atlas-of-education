# Atlas of Education: to-do list by lane

4 November 2026. This sorts the project's `TODO.md` by **where the work should happen** and **how hard it is**.
In each lane, the easiest item comes first.

- **Lane A: Claude (cloud, from the phone).** Writing, reading, web lookups. No heavy compute.
- **Lane B: MacBook.** Anything that runs code, downloads data or refits models. Prompts are written for a local
  model (DeepSeek) or for you at the terminal. The MacBook has open internet, so the World Bank and UNESCO
  downloads that failed in the cloud should work there.
- **Lane C: Trey only.** Decisions, money, people.

Effort: **XS** under 15 min · **S** under 1 hr · **M** an afternoon · **L** several sessions.

---

## Status, 6 November 2026 (the execution run)

The run that this file was written for has happened. Everything in Lane A and Lane B was attempted; Lane C is
prepared but still Trey's to decide. The detail is in `docs/UPDATE_2026_11_06_todo_run.md`; the short version:

| Item | Status | Where |
|---|---|---|
| A1 | **done** — 83/83 remaining `m` values verified, one adjacent correction, no `m` left in the China inputs | `docs/china_input_verification.md`, `engine/firms/data_china.py` |
| A2 | **done** — CV updated 2018→2026 and exported to Word and PDF | `deliverables/Trey_Menefee_CV_2026.docx` / `.pdf` (in the run zip, not the repo) |
| A3 | **done** — MIT recommended for code, CC BY 4.0 content, per-dataset terms table; four questions for Kimi | `LICENSES.md` |
| A4 | **done (5 Nov)** — facts register with calibration/test/diagnostic roles and built-in/emergent/tuned labels | `docs/facts_register.md` (China row updated 6 Nov) |
| A5 | **done** — 14-row book chapter map with real results, honest failures and Bjørn's proposed roles, plus a sendable note | `docs/book_chapter_map.md`, `docs/lane_c_briefs.md` C3 |
| A6 | **done** — full methods-paper outline with verified citations, falsification table, three journals and word-count plans | `docs/methods_paper_outline.md` |
| A7 | **done** — 23-entry annotated bibliography with a five-gap synthesis | `related/prior_work_annotated.md` |
| A8 | **done** — seven evidence cards with verified effect sizes and simulator mappings | `docs/evidence_cards_child_labour.md` |
| A9 | **done** — one-page verification note mapping every claim to a test, and what was not checked | `docs/verification_note.md` |
| A10 | **done** — provenance panels, six-rung ladder, hold-out harness, 35 tests | `engine/impute/`, `engine/test_impute.py` |
| B1 | **partly done** — local git repo + first commit, CI workflow already written; **push blocked on Trey's GitHub credentials** | `docs/GITHUB_SETUP.md` |
| B2 | **done** — baseline all pass (then 20 quick steps; the full refit run has 35 steps, all pass) | `RUN_REPORT.md` |
| B3 | **done** — corrections applied to `data_china.py`, tests re-synced, headline diff recorded after the full refit | `docs/UPDATE_2026_11_06_todo_run.md` §B3 |
| B4 | **done** — eight WDI indicator CSVs and a curated UIS SDG-4 extract, with `SOURCES.txt` | `analysis/public_data/download_public_data.py`, `data/SOURCES.txt` |
| B5 | **done** — T5 credential-flood test with the wage-employment floor | `analysis/public_data/results/public_regressions.md` |
| B6 | **done (5 Nov)** — round-8 conclusions as permanent tests in `run_all.py` | `tests/test_round8.py` |
| B7 | **done** — child-labour simulator's 21 tests in `run_all.py` | `tests/test_childlabour.cjs` |
| B8 | **done** — full refit, new `RUN_REPORT.md` | `RUN_REPORT.md` |
| B9 | **explained, not fixed** — the vacancy failure is documented with the three tests that would settle it; L-effort model fix remains future work | `docs/china_vacancy_failure.md` |
| B10 | **done** — Sobol sweeps for childworld, camchild, China and the Atlas engine; childworld existed, the other three are new | `engine/**/*sobol*.{py,md}` |
| B11 | **done** — hold-out error by method and gap length on PWT, Barro-Lee, WDI and UIS data | `docs/imputation_validation.md` |
| C1–C5 | **prepared** — domain status checked, licence decision page, Bjørn covering note, journal comparison, Cambodian data-request letter; the decisions remain Trey's | `docs/lane_c_briefs.md` |

Also added by this run: six cookbooks (`docs/cookbooks/`), the to-do-run report (`docs/UPDATE_2026_11_06_todo_run.md`)
and the final deliverable zip (kept outside the repository, described in that report).

---

## Lane A: Claude, from the phone

| # | Task | Effort | Done when |
|---|---|---|---|
| A1 | **Verify the 'm' (from-memory) China inputs by web search.** These are the 2025 youth rates for Jan, Mar, Apr, May, Jul, Aug, Sep and Oct; graduate counts for 2008–20 and 2022; urban unemployment before Aug 2022; births; tertiary entrants; and property growth 2018–21. Output: a table of value, source URL and corrected flag, ready to paste into `engine/firms/data_china.py` on the MacBook. | S | Every row is 'v' with a URL, or marked "drop" |
| A2 | **Update your academic CV** (2018 → 2026) as a doc: the massification paper, the Atlas, the book with Bjørn, PolyMatter, Outbreak.Asia, SIG Science, and teaching at Menaul. | S | A doc you can export to Word or PDF |
| A3 | **Licence table:** MIT or Apache-2.0 for code, CC BY 4.0 for content, plus the terms for each bundled dataset (Penn World Table, Barro-Lee, ILOSTAT, UN). Flag Kimi's interface code as a question for you. | S | A `LICENSES.md` draft |
| A4 | **Split calibration facts from test facts.** For each mechanism, label each fact as built in, emergent or tuned. This only needs reading the docs, not running anything. | S | A table for `docs/` |
| A5 | **Book chapter map with Bjørn:** each chapter tied to a world, a test and a result. | M | A one-page doc to share with Bjørn |
| A6 | **Outline of the methods paper "Generative comparative education":** Boudon (1974), Epstein's standard, the cocoon (stock-flow consistency, docking, pattern-oriented modelling, history matching), and the China forecast as an honest failure. | M | A full outline with sections and claims |
| A7 | **Prior-work search** beyond the two searches already done: Grimm 2004; Fanti, Pereira & Virgillito 2023; MAMS; International Futures; agent-based stock-flow-consistent macro. | M | An annotated bibliography added to `related/` |
| A8 | **Evidence cards for the child-labour simulator:** effect sizes from de Hoop & Rosati 2014, Edmonds & Schady 2012, Filmer & Schady 2008, Beegle, Dehejia & Gatti 2006, Atkin 2016, Kruger 2007, and Edmonds & Theoharides 2020. | M | One card per paper: setting, intervention, effect, standard error |
| A10 | **Imputation system: spec and code.** Write `engine/impute/`: provenance flags; a ladder of methods (linear or log interpolation → logit S-curve for rates → cohort back-casting for attainment → state-space smoother with intervals → Amelia-style multiple imputation across countries); and a hold-out test that scores error by gap length. The code is written here; it runs on the MacBook (B11). | M | Module and tests ready to drop in |
| A9 | **A "how I verified the AI-assisted work" note** for reviewers: what was checked, by which test, and what wasn't. | S | One page for the paper's appendix |

**Recommended first step: A1.** It's pure lookup, it's the biggest credibility gap, and it feeds B3.

---

## Lane B: MacBook (DeepSeek or terminal)

Before you start, put the folder somewhere stable, e.g. `~/atlas`, and check that Python 3.11+ and Node are installed.

| # | Task | Effort | Done when |
|---|---|---|---|
| B1 | **Git + a private GitHub repository.** | XS | First commit pushed |
| B2 | **Baseline run:** `pip install -r requirements.txt && python run_all.py` | XS | `RUN_REPORT.md` is all pass |
| B3 | **Paste in the A1 corrections**, re-run, and record which headline numbers moved. | S | A diff of the headline results |
| B4 | **Download World Bank (WDI) and UNESCO (UIS) data** into `analysis/public_data/data/`. | S | CSVs saved, plus a note of where each came from |
| B5 | **Re-run the credential-flood regression** with the wage-employment share as the formal-economy floor. | S | Result in `public_regressions.md` |
| B6 | **Make the round-8 results permanent tests** (floor test, graduate-supply test). | S | Both are in `run_all.py` and pass |
| B7 | **Child-labour simulator tests:** people are conserved, the luxury axiom holds, transfers have an income effect, a ban displaces work into unenforced sectors. | M | The tests run in `run_all.py` |
| B8 | **Full refit** with `python run_all.py --full` (1–2 hours, so leave it running). Only after B3. | M | A new `RUN_REPORT.md` |
| B9 | **China vacancy fix:** add a participation/NEET margin and graduate-sector demand. | L | The vacancy check passes, or a written reason why not |
| B11 | **Run the imputation hold-out test** on the WDI/UIS/Barro-Lee data from B4: delete known points, impute them, and report error by method and gap length. | S | Error table in `docs/imputation_validation.md` |
| B10 | **Sobol sensitivity analysis** for each engine. | L | The few parameter directions that matter, per outcome |

### Prompts to paste into DeepSeek

Small local models work best with one job at a time, exact file paths and a check to finish on. Give it one prompt per session.

**B2: Baseline run**
```
You are in the folder ~/atlas (a Python + Node research project).
1. Run: pip install -r requirements.txt
2. Run: python run_all.py
3. Open RUN_REPORT.md. List any step whose Result is not "pass", with its last lines.
Do not edit any file. Report only what you saw.
```

**B3: Apply the verified data**
```
In ~/atlas, the file engine/firms/data_china.py has data values with a flag 'v' (verified) or 'm' (from memory).
Below is a table of corrections: year, month (or series), new value, new flag, source URL.
[PASTE TABLE FROM CLAUDE HERE]
For each row, change only that value and flag. Add the URL to the SOURCES dict under a clear key.
Do not change anything else. Then run: python run_all.py
Then compare the "Headline results" section of RUN_REPORT.md with this old version:
[PASTE OLD HEADLINE RESULTS]
List every number that changed, old -> new.
```

**B4: Public data download**
```
In ~/atlas, create the folder analysis/public_data/data/wdi/ if it doesn't exist.
Using Python requests and the World Bank API (https://api.worldbank.org/v2/country/all/indicator/CODE?format=json&per_page=20000&date=1990:2025),
download these indicators to one CSV each (columns: country_iso3, year, value):
SL.EMP.WORK.ZS (wage and salaried workers, % of employment)
SL.UEM.1524.ZS (youth unemployment)
SE.TER.ENRR (tertiary gross enrolment)
SE.SEC.CMPT.LO.ZS (lower secondary completion)
SE.XPD.TOTL.GD.ZS (education spending, % GDP)
SL.AGR.EMPL.ZS, SL.IND.EMPL.ZS, SL.SRV.EMPL.ZS (employment by sector)
Write a file SOURCES.txt listing each URL and the download date.
Print the row count of each CSV. Do not modify any other file.
```

**B6: Make the round-8 results permanent tests**
```
In ~/atlas, read related/massification_project/results/round8_mechanisms_and_ledger_fix/RUN_NOTES.md
and the two findings.txt files under floor_test/ and grad_supply/.
Write tests/test_round8.py with two unittest tests that re-run those two experiments at a small size
(use the existing code in related/massification_project/code/massabm; do not change it) and assert
the direction of each finding stated in findings.txt (not exact numbers).
Add the new test to run_all.py the same way the other Python tests are added.
Run python run_all.py and report the result.
```

When DeepSeek finishes, paste its report (or the new `RUN_REPORT.md`) back here and I'll check it.

---

## Lane C: Trey only

| # | Task | Effort |
|---|---|---|
| C1 | Check and buy educationatlas.com (or .org) | XS |
| C2 | Decide on the licence, and ask Kimi's side about the interface code | XS |
| C3 | Send the chapter map (A5) to Bjørn and set up the "schools as protection" session | S |
| C4 | Decide the paper's target journal (CER, IJED, Comparative Education) | XS |
| C5 | Cambodia microdata access: CSES, LFS 2019, the 2012 child-labour survey. These usually need a request to the National Institute of Statistics. | M |

---

## Easiest high-value path

1. **A1** (here) → **B2 + B3** (MacBook): the data becomes defensible.
2. **A2** (here): the CV.
3. **C1, C2, C4** (you, five minutes each).
4. **B4 → B5** (MacBook): the waiting regressions run.
5. **A5 → C3**: the book moves.

Everything in L effort (B9, B10, the China planner game, the spatial board) waits until the paper is submitted.
