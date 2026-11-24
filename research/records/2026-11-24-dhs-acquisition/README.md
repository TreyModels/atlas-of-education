# DHS Individual Recode acquisition — record (2026-11-24)

**Task:** task-2. **Branch:** `research/dhs-acquisition-2026-11-24` (base `origin/research/handoff-2026-11-24 @ 51f9f02`).
**Verdict in one line:** the real access route is **documented and confirmed to exist** (DHS says open again
since Aug–Sep 2025); the files are **login-gated by design**, so this record contains **no microdata**, only the
plan, the preregistration, and public metadata. The individual test is **not run** and must not be faked.

## Files

| File | What it is |
|---|---|
| [`ACQUISITION_PLAN.md`](ACQUISITION_PLAN.md) | The deliverable: exact registration → project request → download route, Terms of Use, file naming (`CCDDVV[FF]DS.ZIP`) with the 92 exact IR files for 14 countries, variable table and derivations, the EFR/TFR construct split, what is free vs gated, the step-by-step ask with turnaround, a verification checklist, and risks with real numbers |
| [`PRE_REGISTRATION.md`](PRE_REGISTRATION.md) | Pre-registered individual-level test, written **before any data arrives**: question, samples, M0–M4 specifications (cohort FE + round FE, design weights, PSU-clustered SEs, pre-declared controls), construct×schooling test, decision rule, falsifiers, honest limits, predictions |
| [`data/dhs_ir_inventory_targets.csv`](data/dhs_ir_inventory_targets.csv) | 92 target IR Stata files (14 countries): exact `FileName`, survey id/type, fieldwork window, unweighted women, sample points, women's universe, bytes |
| [`data/ceb_education_cells.csv`](data/ceb_education_cells.csv) | 318 published education cells (women 40–49, mean CEB) with unweighted denominators — the evidence for the cell-size risk |
| [`data/source_log.txt`](data/source_log.txt) | Every public page/API endpoint touched, HTTP code, and what it establishes (proof the wall was tested, not breached) |
| [`data/README.md`](data/README.md) | Provenance of the two CSVs, exact API queries, and the "no microdata here" rule |

## The exact ask for Trey (short form)

Register free at <https://dhsprogram.com/data/new-user-registration.cfm>; submit a dataset-access request with
the project title/description in `ACQUISITION_PLAN.md` §0 for **14 countries**; after approval (**24–48 h per
country per DHS's stated norm; plan 1–2 weeks**), download the **92 Stata IR ZIPs (~538 MB; Tier 1 = 69
standard-DHS files, 493.6 MB)**; keep them **outside the public repo**; hand over the archive plus a `sha256`
manifest. If approvals stall: `archive@dhsprogram.com`. **Do not substitute model/synthetic data.**

## What was established here (and what was not)

**Established / recomputed 2026-11-24 from the public DHS API and public DHS pages**
- Public API (no key in our tests): **4,655 indicators, 377 surveys, 15,518 dataset/file records**, of which
  **2,005 are Individual Recode records / 2,000 unique IR filenames across 85 countries**.
- The 14 target countries have **92 IR Stata files (538.0 MB)**; **72 standard-DHS files (501.1 MB)**.
- Dataset pages show full file lists to anonymous users; the only access link is the login page. Direct
  flat-file URLs 404 (prior probe, quoted). No scraping, no credentials.
- Published education cells for women 40–49 across those countries: **318 cells in 89 survey-rounds**; median
  cell **367** women, min **25**; **"higher education" cells median 75** women; **55 of 89** rounds have at
  least one cell under 100. (≈ halve for a single 5-year cohort — the binding precision constraint.)
- Programme status: USAID support ended Feb 2025, registrations were closed, **Gates-funded stabilisation from
  Jul 2025**, and **registrations reopened Aug–Sep 2025**. The DHS pages we could fetch carry **no closure
  notice** today. Current (Nov 2026) processing status remains **UNVERIFIED** — the 24–48 h figure is DHS's
  stated norm, not a guarantee. The IPUMS-DHS page still shows a **stale 2025-02-07** "not currently reviewing
  new applications" note; it is superseded.
- Terms of Use that bind us: **no re-distribution, including within any tool/dashboard**; secure storage;
  publications to `references@dhsprogram.com`; **Cambodia** 10 copies to NIS/MOH; **Vietnam 2005** requires
  pre-publication approval by NIHE & GSO. The Atlas repo is public, so **microdata never enters it**.

**Not established (and must not be claimed)**
- No DHS microdata was downloaded, opened or seen. No estimate of the individual-level association exists yet.
- The variable map comes from the DHS Recode Manuals (fetched), not from a file. Whether `v133`/`v206`/`v207`
  exist in the 20 MIS/AIS files is **UNVERIFIED** until one is opened; they are Tier 3 only.
- The period-TFR computation's exact reference window/denominator must be copied from the DHS-8 Guide when the
  code is written (**UNVERIFIED**: the Guide is a JS app and its fertility chapter could not be fetched as text).
- The API's Terms & Conditions could not be read mechanically (**UNVERIFIED**); attribute DHS and check in a
  browser before bulk pulling.

**Quoted, not recomputed** (labelled at point of use): E11's construct numbers (median |diff| 0.3042, max
4.2677, lead/lag 0.541 vs 1.555; branch `e926575`); the prior API-cell ecological estimates and the
"individual-level test could not be run" verdict (branch `research/dhs-micro-2026-11-23 @ 31ded00`).

## Next moves (in order)

1. Trey does §0 of the plan (registration → 14-country request → download Tier 1, then Tier 2).
2. Independent verifier runs `ACQUISITION_PLAN.md` §7 against each file and writes `VERIFICATION.md`; any
   structural failure stops the analysis.
3. Implement `PRE_REGISTRATION.md` exactly: M0–M4, O1/O2 (+ survey-level O3), construct×schooling test,
   decision rule. No specification search; deviations appended.
4. Report the share of rounds with the pre-declared sign, not "robust everywhere".
