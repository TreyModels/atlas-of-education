# Paper M — "Schools before factories": omnibus massification synthesis, 25 Nov 2026

Branch `research/paper-massification-2026-11-25`; record `research/records/2026-11-25-paper-massification/`.
Lead: panel-matrix (task-37). This record consolidates everything the project found about massification into one
synthesis-length paper (target 12,000–18,000 words) with an exhaustive, DOI-verified literature review.

## Deliverables
- **`paper.md`** — full draft, **19,898 words** (about 10.5% above the 12,000–18,000 target because the 24–25 Nov 2026 negative-results and full-system integrations add required results subsections (§7.8–§7.9) and synthesis/limitation entries; flagged for a trim pass), restructured around the finding (Section 2) with explicit Implications (12) and Future research (13), with abstract, introduction,
  four-literature theory section, data and measurement (with a data-tier table), empirical strategy, results sections including the E6 pre-1990 demand-timing re-estimate (7.5) and the E8 fee-abolition event study (7.6), synthesis and
  "What we know now" box, limitations/referee objections, conclusion, and three appendices (evidence labels/data tiers,
  reproduction, data gaps). The 25 Nov revision is logged in `REVISION_LOG.md`. Every number carries sample and uncertainty; the historical dates are labelled
  UNVERIFIED literature standard; the framing is "a late-industrialiser regularity, not a universal law" and the
  causal language is "is better described as", never "causes".
- **`claims-prior-art.md`** — seven claim groups, 3–8 closest works each, DOI + Crossref status, explicit
  "new vs replicated" column; covers human-capital/education demand, world-culture/institutionalism,
  state-building/compulsory schooling, economic-history sequence per country, structural change/agriculture,
  scaling, and credentialism/care.
- **`refs.md`** — APA 7th, 57 entries from this paper's own Crossref run (with MATCH / WEAK / NO-MATCH status)
  plus the section leads' Crossref-verified reference lists in Part B (scaling, drivers/credentials,
  agriculture/history), each with its branch and status markings.
- **`claims-to-source-map.md`** — claim | number | branch @ commit | file | field for every number in the paper, including the E6/E8 rows added in the 25 Nov revision.
- **`data/`** — verbatim copies of the source records used by the revision: `e6_summary.json`, `e8_results.json`, `n3_recommendation.json`, `fee_dates.csv` (from `e6e8 @ 2d19da7` and source verification `9a0fd69`), `supply_demand_963e5e5.json/.txt` and `event_dates_subsistence_v2.csv`.
- **`scripts/verify_revision_numbers.py`** — recomputes every number quoted in the revised passages from `data/`; output `data/revision_verification.json` (41/41 checks pass).
- **`REVISION_LOG.md`** — what changed in the 25 Nov revision, source and commit.
- **`search-strategy.md`** — the recorded search (Crossref API, web queries, project records; what was not
  accessible and why).
- **`contributions/dhs-ecological-gradient-for-paper-F.md`** — the DHS ecological-gradient section draft
  written for Paper F (un-data) at their request, with numbers, sources, prior works and the microdata caveat.
- **`scripts/verify_refs_crossref.py`**, **`data/refs_crossref.json`** — the reference-verification run.

## Section ownership and integration
| section | source record (branch @ commit) | drafted by | integrated/edited by |
|---|---|---|---|
| 1 Introduction; 2 Theory; 3 Data; 4 Strategy; 5 Sequencing; 6 Supply vs demand | subsistence-v2 @ ce66cfc; supply-demand @ 963e5e5 | panel-matrix | panel-matrix |
| 7 Historical cases | historical-sequence @ ab658c7 (definitions @ 74e0fe2) | gpu-dose | panel-matrix |
| 8 Agricultural floor / Boppart / joint model | subsistence @ 41f6429; subsistence-v2 @ ce66cfc | gpu-dose | panel-matrix |
| 9 Scaling, θ/γ, drivers null | scaling @ fd691a6; grouping-multiverse-400 @ 1152cec | cuda-scale; multiverse-400 | panel-matrix |
| 10 Credential inflation, care loop | care-credential @ e626cb8 | multiverse-400 | panel-matrix |
| 11–13 Synthesis, limitations, conclusion | all of the above | panel-matrix | panel-matrix |

## Project brief headings (mandatory record sort)

The project brief asks every record to be sortable under **(1) Fertility** and **(2) Massification**. The paper
keeps its journal structure; this map gives the sort:
- **(1) Fertility**: Section 2 (headline: schooling precedes the fertility decline in 37.5% under a strict ordering, 95% interval 26.6-50.0%, with 31.3% simultaneous; the source JSON's 68.75% counted ties as schooling-first and is not used); Section 6
  (sequencing result and the schooling-before-fertility ordering); Section 11 (credential/care fertility
  mechanisms); plus the DHS ecological-gradient contribution in `contributions/` for Paper F.
- **(2) Massification**: Sections 1-8 and 10-16 (everything about schooling expansion, the supply/demand
  decomposition, the historical cases, the agricultural floor, scaling and drivers, implications and future
  research).

## Verification status
- **Numbers**: every number quoted in the revised passages was **recomputed** from a committed copy of the source record (`data/`) by `scripts/verify_revision_numbers.py`, 41/41 checks passing (`data/revision_verification.json`); the remaining unchanged numbers are fields in verified branches at named commits (see `claims-to-source-map.md`). No new estimation was done for the paper; only the Crossref verification run and the recomputation of already-committed numbers.
- **Historical dates**: **all UNVERIFIED literature standard**; the negative facts verified in-session are that
  the project's own long-run panel cannot adjudicate them (schooling starts 1870, urban share 1950) and that no
  national enrolment series was obtainable from public APIs.
- **References**: 57 entries in this paper's own Crossref run (50 MATCH, 2 WEAK, 3 NO_MATCH, 2 NO_RESULT; the
  non-matching entries are books/reports/working papers and are flagged as such). Section leads' verified lists
  are reproduced with their own status marks; unverified books/reports are marked, never dressed up as verified.
- **Literature independence**: `novelty-review` (task-35) is building an independent prior-work list; its
  discrepancies will be addressed in this record or the claims tables before submission.
- **No "first"**: the paper claims a new assembly, not precedence, and records the search that supports that
  wording.

## The synthesis verdict
Massification in late-industrialising countries is better described as schooling and structural change moving
together, with schooling typically but not universally first: the schooling take-off precedes the release of
agricultural labour in 61 of 64 countries (median 26 years, reverse 5%, 0–11%). On pre-1990 structural-change
series, demand-first is 10.0% (GGDC non-agricultural employment), 15.4% (urbanisation), 24.1% (industry value
added) and 18.8% (agricultural value added) of identifiable countries, with all-country bounds of 6.7–53.0%
and 21–43% weak ties/left-censored: demand is neither eliminated nor cleanly ordered. The retracted "7%"
labour-demand figure came from a 1991-start series and is not used. The raw demand-first event ordering (73%)
is a data-availability artefact; in the fair sample supply (76%) and demand (79%) turn together, and the horse
race puts the conditional association on supply (+0.456, SE 0.174 vs +0.006, SE 0.203; n=78, 51 countries).
The fee-abolition event study is **consistent with** a supply-side effect on primary enrolment (+22 to +29
points after event year +1, flat pre-trends, sparse coverage, on-impact interval spanning zero). The
agricultural floor is real in the cross-section but does not deliver the dynamic sequence; scaling regularities
are regularities, not laws; credential and care mechanisms are null in the data they can be tested on. The
historical cases show why the regularity is conditional: Prussia shows state supply 80–120 years ahead,
Britain demand-led by 40–90 years. **Late-industrialiser regularity, not a universal law.**

## Revision of 25 November 2026 (E6/E8 integration)
Applied after the Codex wave retracted the 7% labour-demand figure and verified the E6/E8 record (`e6e8 @ 2d19da7`) and the fee dates (`task-49 @ 9a0fd69`). Changes: replaced the 7% figure and all "demand is ruled out" framing with E6's pre-1990 numbers and the "schooling and structural change move together" framing (with bounds and ties/censoring flagged); softened supply-led/sequencing causal language to association/consistency language; added the E8 fee-abolition section (7.6) and the N3 threshold-smoothing caveat (7.5); added a data-tier table and labelled every series; corrected subsection numbering; rechecked abstract/results/limitations against each other; recomputed the quoted numbers. Details, sources and commit: `REVISION_LOG.md`.

## Full-system multiverse integration (25 November 2026, task-45)

Adds §7.9 "What the full-system multiverse adds: gates, affordability, jobs and rural structure" (pre-registered
1,440-run toy `eduengine` multiverse, 144 equation-choice combinations × 10 seeds, with independent cluster-robust
OLS/seed-FE/Holm/stratum tests), plus an abstract sentence, synthesis point 8, a "What we know now" bullet,
limitation objection 14, a conclusion sentence and the §12.3 cross-reference. Core numbers: gates dominate
lower/upper completion and the wealth completion gaps (bar .720/.609 vs quota .550/.449; quota−bar −17.0/−16.0pp;
bar screens q1 hardest, .174 vs .966); affordability dominates primary/tertiary completion and the poverty margin
(cash-only .797/.296 vs credit up to .929/.428; q1 lower .091→.195); jobs regime dominates formal share (.293 queue
vs .627 competitive); rural structure dominates wealth parity (.245 vs .100); supply/funding moves public quality
(0.99 vs 1.12) but is not identifiable from attainment; tutoring is gate-driven (.273→.499) and second-order.
**All of it is a toy, uncalibrated simulation, not evidence**; engine boundaries are stated in §7.9. Sources:
`research/masseng-edsystem-2026-11-25` @ `b7108da` (pre-registration `3679f2d`) and
`research/edsystem-tests-2026-11-25` @ `aadbbb4`; details in `EDSYSTEM_INTEGRATION.md`.

## Negative-results integration (24 November 2026, task-37)
Adds §7.8 "What the project's own simulations found: negative results" (staging audit exposure/fiscal confound; X1 exposure matching removes 88–98% of the apparent order effect; X3 no elasticity reversal or rescue; X4 aggregate FAIL_NO_EVIDENCE; X5 Bayesian screens not posteriors; X2 gate/tutoring inequality), plus abstract/conclusion sentences, synthesis point 7, the "What we know now" bullet and limitation 13, and the §12.3 gate-design caution. All X results are labelled **simulations** or **exploratory aggregates**, not evidence. Sources: `research/masseng-staging-x1-2026-11-24` @ `fef7428`, `research/masseng-staging-x2-2026-11-24` @ `f592bae`, `research/masseng-bayes-audit-2026-11-24` @ `0ecd4be`, `research/masseng-timing-audit-2026-11-24` @ `ff84e75`; details in `X_RESULTS_INTEGRATION.md`.

## Known gaps (stated, not proxied)
1. Cohort-linked microdata (the theory's generational claim) not obtainable; event data are period data.
2. Full cross-country compulsory-schooling-law compilation not done; only the project's six-system timeline and
   four historical cases.
3. Historical enrolment series named but not digitised (Flora/Lindert; Newcastle Commission; Diebolt; US
   Historical Statistics H-598+).
4. City-size distributions and functional-category depth limited (WUP/GeoNames failed; 1-digit ISCO), so
   theta/gamma is not estimable.
5. Credential registries and care-sector detail limited to ILO SDMX; no causal identification for the horse race.

## Submission targets
Review/synthesis venue (*Review of Educational Research*, *Annual Review of Sociology*, *Sociology of Education*)
or development economics (*World Development*, *Journal of Development Economics*); the paper explains in
Section 12 why it is not an *Explorations in Economic History* archival paper (historical section is a synthesis
of literature dates, not new archival measurement).
