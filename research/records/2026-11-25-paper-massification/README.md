# Paper M — "Schools before factories": omnibus massification synthesis, 25 Nov 2026

Branch `research/paper-massification-2026-11-25`; record `research/records/2026-11-25-paper-massification/`.
Lead: panel-matrix (task-37). This record consolidates everything the project found about massification into one
synthesis-length paper (target 12,000–18,000 words) with an exhaustive, DOI-verified literature review.

## Deliverables
- **`paper.md`** — full draft, **17,433 words** (within the 12,000–18,000 target), restructured around the finding (Section 2) with explicit Implications (12) and Future research (13), with abstract, introduction,
  four-literature theory section, data and measurement, empirical strategy, six results sections, synthesis and
  "What we know now" box, limitations/referee objections, conclusion, and three appendices (evidence labels,
  reproduction, data gaps). Every number carries sample and uncertainty; the historical dates are labelled
  UNVERIFIED literature standard; the framing is "a late-industrialiser regularity, not a universal law" and the
  causal language is "is better described as", never "causes".
- **`claims-prior-art.md`** — seven claim groups, 3–8 closest works each, DOI + Crossref status, explicit
  "new vs replicated" column; covers human-capital/education demand, world-culture/institutionalism,
  state-building/compulsory schooling, economic-history sequence per country, structural change/agriculture,
  scaling, and credentialism/care.
- **`refs.md`** — APA 7th, 57 entries from this paper's own Crossref run (with MATCH / WEAK / NO-MATCH status)
  plus the section leads' Crossref-verified reference lists in Part B (scaling, drivers/credentials,
  agriculture/history), each with its branch and status markings.
- **`claims-to-source-map.md`** — claim | number | branch @ commit | file | field for every number in the paper.
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
- **Numbers**: every number in the paper is a field in a verified branch at a named commit (see
  `claims-to-source-map.md`). No new estimation was done for the paper; only the Crossref verification run.
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
Massification in late-industrialising countries is better described as state/institution-led: the schooling
take-off precedes the release of agricultural labour in 61 of 64 countries (median 26 years, reverse 5%,
0–11%); labour-market demand (wage premium, paid employment) precedes it in only 7% of countries; the raw
demand-first event ordering (73%) is a data-availability artefact, and in the fair sample supply (76%) and
demand (79%) turn together while the horse race puts the association on supply (+0.456, SE 0.174 vs +0.006,
SE 0.203; n=78, 51 countries). The agricultural floor is real in the cross-section but does not deliver the
dynamic sequence; scaling regularities are regularities, not laws; credential and care mechanisms are null in
the data they can be tested on. The historical cases show why the regularity is conditional: Prussia supply-led
by 80–120 years, Britain demand-led by 40–90 years. **Late-industrialiser regularity, not a universal law.**

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
