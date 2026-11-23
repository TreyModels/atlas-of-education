# Literature search strategy (Paper M)

Recorded so that "not previously assembled in this form" is auditable and so that the absence of a prior
event-ordering study is a claim about a documented search, not an assumption. No "first" is asserted anywhere in
the paper.

## Tools and dates
- **Crossref REST API** (`api.crossref.org/works`, `query.bibliographic`, title-similarity + year filter):
  used to verify every candidate reference (57 in the paper's own run, 24 Nov 2026; plus the section leads' runs
  on 24–25 Nov 2026, reproduced in `refs.md` Part B). Raw results: `data/refs_crossref.json`; script:
  `scripts/verify_refs_crossref.py`.
- **General web search** (2–3 Nov 2026 style queries, run 24–25 Nov 2026) for the event-ordering prior art, e.g.
  "schooling take-off precedes agricultural employment decline cross-country event ordering"; "supply-led
  massification compulsory schooling before industrialisation sequence"; "sequence of mass education and
  structural transformation did schooling come before farm exit". Results were largely the economic-history and
  world-polity literatures already in the reference list; no study was found that assembles the common
  event-ordering comparison, which is consistent with the paper's carefully-worded "not previously assembled in
  this form as far as we know".
- **Project records**: all prior records of this session were searched for the same question, in particular the
  novelty ledger (`research/novelty-2026-11-23`), which independently audited the session's claims, and the
  historical-sequence, subsistence, supply-demand, scaling, grouping-multiverse and care-credential records.
- **Not used / unavailable**: Scopus, Web of Science, EconLit, Google Scholar API (no access); PubMed and
  publisher pages were not reachable from the environment in this session (documented in the novelty ledger).
  This is a real limitation of the search: a library-subscription search could find more adjacent work, and the
  paper says so.

## Query set used for the core claim
1. schooling / education expansion before agricultural employment decline or structural transformation.
2. mass schooling before industrialisation; compulsory schooling before factory demand.
3. supply-led vs demand-led massification; education as state/institution project.
4. event ordering / sequence of education and structural change; lead-lag education agriculture.
5. Prussia/France/Britain/US sequence histories (economic history literature).
6. scaling laws in education/occupations (Heaps, Zipf, urban scaling).
7. credentialism/signaling and fertility (Spence, Arrow, Collins, Bills, sheepskin).
8. care economy and fertility (female employment composition).

## Prior-art discipline
- 3–8 closest works per claim in `claims-prior-art.md`, each with DOI and Crossref status where a DOI exists.
- Books, reports and some working papers have no Crossref DOI and are marked, not dressed up as verified.
- The paper states what is **replicated** vs what is **new in this assembly** for every claim; the strongest
  "new" items are the common event-ordering comparison, the supply–demand horse race, and the rejection of the
  universal fertility–attainment collapse curve.
- The independent literature auditor (`novelty-review`, task-35) is building its own prior-work list and its
  discrepancies will be added here or answered in the record before submission. This file records our list; it
  does not pre-empt the audit.
