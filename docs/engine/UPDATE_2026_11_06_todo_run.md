# To-do-list run, 6 November 2026 (v0.12)

This is the record of the run that executed `docs/TODO_BY_LANE.md` against the v0.11.2 tree, plus the request to ship
the finished work as one zip with cookbooks. It lists what was done, where the evidence is, and what was deliberately
left undone.

Run environment: macOS (Apple Silicon), Python 3.11.17 in a local virtual environment, Node 26.12.0 for the browser
suites (also checked on Node 18.12.1), live internet access. The work was split across a lead agent and five helpers
with disjoint write scopes (China data; research literature; project documents; imputation code; cookbooks); the
project's own `run_all.py` was run by the lead only.

---

## Lane A: written deliverables

| Item | What was delivered | Where |
|---|---|---|
| **A1** | Verified all 83 remaining from-memory China inputs against fetched pages. 83 confirmed, 0 value corrections, one adjacent error found and fixed (urban 2023-01 5.6 → 5.5). The 2020-01 open question is resolved to 5.3. Births re-derived from NBS yearbook tables and re-flagged `d`. | `docs/china_input_verification.md`; applied in `engine/firms/data_china.py`; guarded by `tests/test_evidence.py` |
| **A2** | Academic CV updated from 2018 to 2026 (massification paper, Atlas, book with Bjørn, SIG Science, Outbreak.Asia, PolyMatter, Menaul teaching; education and appointments from the existing CVs). Exported to Word and PDF. | `deliverables/Trey_Menefee_CV_2026.docx` / `.pdf` (in the delivery zip, built by `tools/build_cv.py`) |
| **A3** | Licence recommendation: MIT for code, CC BY 4.0 for content; per-file table of the terms of all twelve bundled data CSVs (four verified reusable, eight boundary cases); Kimi's interface code flagged as four questions for Trey; a post-approval checklist. | `LICENSES.md`; decision page in `docs/lane_c_briefs.md` C2 |
| **A4** | The facts register (5 Nov) is complete for China, Cambodia, the Atlas engine and the Planning Lab; the China input row is updated with the A1 result. | `docs/facts_register.md` |
| **A5** | 14-row book chapter map with a model/world, a real result, the honest failure and a proposed role for Bjørn per chapter, plus five questions and a sendable covering note. | `docs/book_chapter_map.md`; `docs/lane_c_briefs.md` C3 |
| **A6** | Full methods-paper outline ("Generative comparative education"): Boudon as ancestor, Epstein's standard, the cocoon, the strict protocol, the China failure, Cambodia tests, a falsification table, three target journals and two word-count plans; citations verified. | `docs/methods_paper_outline.md` |
| **A7** | 23-entry annotated prior-work bibliography in six sections with a five-gap synthesis (G1–G5) and refutation conditions; every citation with a verified DOI/URL. | `related/prior_work_annotated.md` |
| **A8** | Seven evidence cards (de Hoop & Rosati; Edmonds & Schady; Filmer & Schady; Beegle, Dehejia & Gatti; Atkin; Kruger; Edmonds & Theoharides) with effect sizes, SEs/CIs, identification, threats and a paper→lever→sign→magnitude calibration table for `web/childlabour.js`. | `docs/evidence_cards_child_labour.md` |
| **A9** | One-page reviewer appendix: what was checked by which test, what was not, how AI-assisted work was cross-checked, and an 11-step repeatable protocol. | `docs/verification_note.md` |
| **A10** | The imputation system: provenance panels, six-rung ladder (linear, log-linear, logit S-curve, cohort back-cast, Kalman smoother with intervals, Amelia-style multiple imputation), hold-out harness, and 35 tests. | `engine/impute/`, `engine/test_impute.py`; report `docs/imputation_validation.md` |

## Lane B: MacBook work

| Item | Result | Evidence |
|---|---|---|
| **B1** | Local git repository initialised and first commit made. **Push is blocked**: no GitHub credential on the machine. | `docs/GITHUB_SETUP.md` (two-minute steps for Trey) |
| **B2** | Baseline: all quick steps pass (20/20, including the new child-labour and imputation steps). | `RUN_REPORT.md` (full run) |
| **B3** | A1 corrections applied to `data_china.py`; `tests/test_evidence.py` re-synced (13 tests, including "no `m` flag remains"); the data-level diff is summarised below. No headline number moved in the quick run (the stored results are unchanged until the refit); the full refit then re-estimated the China results with the corrected 2023-01 input. | this file, §B3; `engine/firms/data_china.py`; `tests/test_evidence.py` |
| **B4** | Eight World Bank WDI indicator CSVs (tidy, ISO3, 1990–2025, aggregates dropped) and a curated 117,047-row UNESCO UIS SDG-4 national extract, from the live World Bank API and UIS bulk archive, with `SOURCES.txt`. | `analysis/public_data/download_public_data.py`, `analysis/public_data/data/wdi/`, `data/uis/uis_sdg4_national.csv`, `data/SOURCES.txt` |
| **B5** | T5 credential-flood test with the wage-employment share as the formal-economy floor, with country and year effects. Interaction −0.028 (se 0.019, t −1.5); marginal effect of a year of schooling on the graduate-minus-basic gap +2.1 pts at the 10th percentile of the wage share vs +0.7 at the 90th. The floor story is not rejected, but this panel cannot separate it from a flat gradient. | `analysis/public_data/results/public_regressions.md` |
| **B6** | Round-8 conclusions are permanent tests in `run_all.py` (14 tests, stored full-size results plus a reduced re-run). | `tests/test_round8.py` |
| **B7** | 21 child-labour simulator tests wired into `run_all.py`: conservation, luxury axiom, transfer income effect, ban displacement into unenforced work, money conservation. | `tests/test_childlabour.cjs`; `run_all.py` |
| **B8** | Full refit (`python run_all.py --full`) run on the corrected inputs: **all 35 steps pass** (20 quick + 15 long), finished 10:53 on 6 November 2026, new report and stored results. | `RUN_REPORT.md`, `engine/**/results/` |
| **B9** | Vacancy failure **explained in writing**, as the item's done criterion allows: why free entry cannot produce a postings collapse, the aggregate-demand path contradicted by the adult market, and three designed tests (postings coverage, time-varying matching efficiency, NEET margin) with the data each needs. The model fix remains future L work. | `docs/china_vacancy_failure.md` |
| **B10** | Sobol sensitivity for all four engines through `engine/mc.py`: childworld (existing), camchild (assumed context constants), China youth market (broad behavioural ranges) and the Atlas engine (the pre-registered `history_match.SPACE` box). Stiff directions reported per outcome. | `engine/camchild_sobol.py`, `engine/firms/china_sobol.py`, `engine/atlas_sobol.py`; `engine/**/results/*sobol*.md` |
| **B11** | Hold-out error by method and gap length on PWT, Barro-Lee, World Bank WDI and UNESCO UIS data; linear/log-linear strongest on short gaps of smooth series, cohort back-cast competitive at five-year gaps, state-space intervals near nominal, multiple imputation best where the common year factor is informative. | `docs/imputation_validation.md`, `engine/impute/report.py` |

### §B3: what the A1 corrections changed

- **Values:** 83 confirmed; **one correction inside already-verified data**: NBS overall urban unemployment, 2023-01,
  5.6 → 5.5 (Wang Pingping commentary, 2023-04-19). No other value moved.
- **Before/after the refit.** The quick run before the correction and the full refit after it were compared on the
  `## Headline results` section of `RUN_REPORT.md`. Every number that moved (old → new):

  | Headline | Before (pre-correction report) | After (6 Nov refit) |
  |---|---:|---:|
  | Whole-record fit, two-type model (fit statistic) | 1.14 pts | 1.27 pts |
  | Modelled rise, whole record | +5.0 pts | +5.2 pts |
  | 2018–22 fit: forecast error vs naive | 5.50 vs 1.71 | 5.54 vs 1.61 |
  | 2018–22 fit: modelled rise | −0.1 | +0.1 |
  | Shapley: supply / composition / demand / sector / screening | +1.93 / −0.22 / −0.15 / +3.45 / 0.00 | +1.47 / −0.10 / −0.04 / +3.84 / 0.00 |
  | Tilly: official rate / slack / waiting / insiders | +4.8 / +7.7 / 1.32m / 75% | +5.1 / +9.5 / 2.00m / 76% |
  | Tilly: graduate unemployment, insiders vs outsiders | 18.4% / 21.1% | 19.0% / 22.6% |
  | Strict Dec 2022 forecast vs naive | 5.54 vs 1.61 | 5.54 vs 1.61 (unchanged) |
  | Tilly strict, unemployment only / with wages | 5.84 / 5.57 | 5.84 / 5.49 |
  | Dec 2024 cutoff, same-definition model vs naive | 1.36 vs 0.89 (bias −0.09) | 1.71 vs 0.89 (bias −1.47) |
  | Seasonal: spread11 vs naive | 0.62 vs 0.89 | 0.77 vs 0.89 |
  | Tournament winner, strict protocol, vs naive | 5.51 vs 0.89 (bias +5.26) | 1.09 vs 0.89 (bias −0.41) |
  | Tournament winner, postings H1 2025 | −9% | −89% |
  | Graduate vacancies, H1 2025, model vs observed −22% | +6% | +2% |

  The large moves in the tournament row are not a correction effect: they are two different points in a flat,
  unprofiled optimum valley (the pre-refit note already warned that "the stored result is one honest strict fit, not
  the best the structure could do"). The result is still a loss to the naive benchmark (1.09 > 0.89). Several
  documents quoting the old numbers were updated to the new ones (see the working-tree diff), and `docs/facts_register.md`
  now records the new fit statistics.
- **Flags:** `GRAD_FLAG` and `TERTIARY_FLAG` are now all `v`; `BIRTHS` carries a new `BIRTHS_FLAG` of `d` (derived);
  the whole `_URB_M` series is in `_URB_CHECKED` with an import-time assert; no `m` flag remains anywhere in the China
  inputs.
- **Tests:** `tests/test_evidence.py` now asserts the resolved 2020-01 value, the corrected 2023-01 value, the all-`v`
  flags, the `d` births and the absence of `m`; 13 tests pass.

## Lane C: prepared, not decided

`docs/lane_c_briefs.md` contains: C1 the domain facts (educationatlas.com registered and parked since 2005; .org taken
since 2026-10-21 by a live Ukrainian education atlas; .net/.io/.study/.academy appear available) and a recommendation;
C2 the licence decision page; C3 the covering note to Bjørn and the session agenda; C4 a CER/IJED/Comparative
Education comparison and a recommendation; C5 the Cambodian data-request letter for CSES, LFS and the child-labour
survey, with the public DHS 2021–22 fallback. These are decisions for Trey.

## Cookbooks (requested in the follow-up message)

Six recipe guides under `docs/cookbooks/`, indexed by `docs/cookbooks/README.md`: run and rebuild; verify an input (using
the A1 audit as the worked example); add a model or world; Monte Carlo and sensitivity; AI-assisted research protocol
(with ready-made prompts); run the to-do list (the workflow used here, safely split across agents, and how the final
zip is verified). The commands in them were executed on this machine where safe; the ones that would write generated
artifacts or need network were documented from the code instead, and that is stated in each recipe.

## Verification

- `python run_all.py` — all 20 quick steps pass, including the new child-labour simulator (21 checks) and imputation
  (35 tests) steps.
- `python run_all.py --full` — **all 35 steps pass** (20 quick + 15 long refit steps); finished 10:53 on 6 November
  2026. Its report is the shipped `RUN_REPORT.md`, and the stored results beside the engines are those the run
  produced. The headline numbers before and after the refit are tabulated in §B3 above.
- `node Angkor_Atlas_Research_Edition_v1/test_model.js` — pass (seeded reproducibility, spatial geography, finite
  outputs, paired MC, sweep, regression).
- `node Atlas_of_Education_Research_Edition_v1/test_model.js` — pass, 292 checks.
- `python -m engine.impute --out docs/imputation_validation.md` — deterministic; regenerating reproduces the report.
- `python -m unittest engine.test_impute` — 35 tests pass in ~1.5 s.
- `node tests/test_childlabour.cjs` — 21 checks pass.
- Browser/Python parity, Planning Lab, Cambodia parity, round-8 and the planning kernel all pass inside `run_all.py`.

## What is not done, and why

1. **GitHub push (B1).** No GitHub credential on the machine; the repository is committed locally and the workflow is
   written. Steps to finish: `docs/GITHUB_SETUP.md`.
2. **Vacancy model fix (B9).** The done criterion allows a written explanation, which is delivered; the structural fix
   needs a second vacancy observable and a new posting rule, and the to-do list itself schedules L work for after the
   paper.
3. **Lane C decisions.** None can be made by an agent (money, people, licences).
4. **The three research items that remain blocked on data people:** Cambodia microdata (C5), the MICS/DHS survey inputs
   (needs attached tables), and Bjørn's protection magnitudes.
5. **Pre-existing project items outside the by-lane list** (the research programme in `TODO.md` §R, the narrative engine,
   the country board, the Planning Lab's missing models) are unchanged; only the items the run was asked to finish were
   touched. `TODO.md` marks what this run closed.

## Files added by this run (summary)

New code: `engine/impute/` (10 modules), `engine/test_impute.py`, `engine/camchild_sobol.py`, `engine/atlas_sobol.py`,
`engine/firms/china_sobol.py`, `tests/test_childlabour.cjs`, `analysis/public_data/download_public_data.py`.
New documents: `LICENSES.md`, `docs/china_input_verification.md`, `docs/imputation_validation.md`,
`docs/book_chapter_map.md`, `docs/methods_paper_outline.md`, `docs/verification_note.md`,
`docs/evidence_cards_child_labour.md`, `docs/china_vacancy_failure.md`, `docs/lane_c_briefs.md`,
`related/prior_work_annotated.md`, `docs/GITHUB_SETUP.md`, `docs/cookbooks/` (7 files), this file.
Updated: `engine/firms/data_china.py`, `tests/test_evidence.py`, `analysis/public_data/public_regressions.py`,
`analysis/public_data/README.md`, `requirements.txt`, `run_all.py`, `START_HERE.md`, `README.md`, `TODO.md`,
`docs/TODO_BY_LANE.md`, `docs/facts_register.md`, and the stored results rewritten by the full refit.
