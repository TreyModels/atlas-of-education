# AMENDMENT 02 — access coverage and what may be analysed under partial approval

**Committed before any DHS microdata arrives** (none has arrived; no individual-level data has been seen by this
workstream). Appends to [`PRE_REGISTRATION.md`](PRE_REGISTRATION.md); does not edit it. Motivation: the DHS
request form allows **one region per project request**, so the pre-registered 14-country panel is being acquired
as **two requests** (11 African + 9 Asian, the latter containing KHM/PHL/VNM plus 6 out-of-scope Asian
countries). See [`application/CONFIRMATION_2026-11-24.md`](application/CONFIRMATION_2026-11-24.md) and
[`application/NEXT_ACTION_2026-11-24.md`](application/NEXT_ACTION_2026-11-24.md).
**Status when written:** Asian request pending (snapshot 2026-11-24 18:32); African request not yet submitted.

## A2.1 What the pre-registered main test requires

The main test (PRE_REGISTRATION §3, samples S-A…S-E; §4 models M0–M4; §5 D1–D3) requires:
- the **11 African countries** (MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA, BEN, NAM, SWZ) — the 8 E8 countries plus
  3 comparators;
- the **3 Asian benchmarks** (KHM, PHL, VNM).

Both are needed for the pre-registered pooled panel. Neither alone is the pre-registered sample.

## A2.2 Pre-declared coverage tiers (fixed now)

| Tier | Coverage | What may be run | Label |
|---|---|---|---|
| **T0** | Both requests approved; 14 countries' **standard-DHS IR** files verified | The full pre-registered analysis: S-A…S-E, M0–M4, construct split, cohort test, heterogeneity | **PRIMARY — pre-registered** |
| **T1** | Only the **11 African** countries approved | The same S-A…S-E and M0–M4 **restricted to the 11 African countries**; the 3 Asian benchmarks are reported as **missing coverage**, not as a failure. This is a **pre-declared coverage-restricted analysis**, not the main test; every table must say "11-country coverage" | **coverage-restricted primary** |
| **T2** | Only the **3 Asian** countries approved (KHM/PHL/VNM) | **Exploratory only.** The Asian panel is 3 countries / 5–7 rounds each; the pre-registered main test cannot be run. Any estimate is labelled **EXPLORATORY, out of pre-registered coverage**, and is not counted toward D1–D3. | **exploratory** |
| **T3** | One country or a handful approved | Descriptive verification and data-quality work only. No hypothesis tests reported as findings. | **descriptive** |
| **T4** | Nothing approved / refused | No DHS microdata analysis. The public-API ecological record (`research/dhs-api-ecological-2026-11-24`) stands as the only evidence, and the individual test remains **unrun**. | — |

Rules for T1–T3, fixed before data:
1. **No silent redefinition of the sample.** The analysis run and the coverage tier are reported in the same
   sentence as every headline number.
2. **No adding countries after seeing results.** The set is exactly the approved subset of the pre-registered 14;
   the six extra Asian countries in the pending request (India, Indonesia, Myanmar, Nepal, Sri Lanka, Thailand)
   are **outside the pre-registration** and may be used only as a clearly-labelled descriptive robustness
   appendix under a separate pre-registration, never as part of D1–D3.
3. **Construct split unchanged.** O1 = `v201` (births), O2 = `v201 − v206 − v207` (surviving children), O3 =
   survey-period TFR from **Births Recode (BR)** files (see A2.4). O2 is never called TFR.
4. **Tier T2 cannot confirm or kill D1–D3.** A 3-country Asian panel does not test "does the association hold
   across the pre-registered panel"; it can only be reported as exploratory.

## A2.3 GPS and HIV scope

- **GPS is not used** by the pre-registered test (the design uses `v024` region FE, not coordinates). The GPS
  tickets on 6 of 9 Asian countries add Terms-of-Use scope and are not needed; they do not change the analysis.
- **HIV datasets are not requested** and are not needed.
- If the account later offers to amend the pending request, dropping the GPS tickets is acceptable but not
  necessary; no analysis depends on them.

## A2.4 Correction to the pre-registration's O3 operationalisation (before any data)

PRE_REGISTRATION §4.3 defines O3 (survey-level period TFR) as "computed from each IR's birth history
(`REC21`)". The **Stata IR recode is one record per woman**; the birth history is a separate record type in the
hierarchical/ASCII distribution and is distributed cleanly as the **Births Recode (BR, `??BR??DT.ZIP`)**.
Therefore O3, if computed, will be computed **from the BR files** — which the same country-level approval covers
(the approval is by country for unrestricted survey datasets). The pipeline therefore expects, per country-round:
**IR (required)** and **BR (optional, only for O3)**. If BR files are not obtained, O3 is reported as
**not computed**; the survey's **published** TFR (DHS API / final report) is quoted only as an external check and
is labelled as a published aggregate, not as our computed O3. This is an operational correction, not a change to
any hypothesis or decision rule.

## A2.5 Verification gate (unchanged, now enforceable by code)

No analysis runs until `scripts/ir_pipeline.py --check-only` passes on the downloaded files and writes
`verification.json` (file sha256s, variable presence, `v201 == Σ v202..v207`, weights normalisation, CMC/age
consistency, cluster counts vs published sample points, fieldwork-window check). Any structural failure stops the
analysis and is reported — the file is re-downloaded, not patched.

## A2.6 Access log

Every approval/refusal and every download is recorded in `application/STATUS_LOG.md` with a timestamp. No
credentials, no account email, and no page captures with personal data enter the repository.
