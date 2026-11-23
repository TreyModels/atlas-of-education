# Paper N2 — The level-of-analysis trap (standalone paper)

Record for `research/paper-levels-novel-2026-11-25`. Task-39. This is the standalone paper on the
levels-versus-changes / transportability demonstration, one of the two "genuinely new" candidates
identified by the novelty audit.

## Deliverables
- **`paper.md`** — full draft, **6,008 words** (target 6,000–8,000). Sections: abstract; 1 introduction;
  2 prior work and framing; 3 data, specifications and pre-registered design; 4 results (levels,
  changes, transportability, threshold shape, placebo, verdict table, Tables 1–2); 5 referee
  objections (within–between critique, Nickell bias/measurement error/change-window sensitivity,
  ecological fallacy, placebo scope, sensitivity-universe caveat); 6 implications; 7 future research
  (six concrete designs, each with what it would and would not identify); 8 conclusion;
  reproducibility/data-availability note.
- **`claims-prior-art.md`** — the 8–12 closest works per claim, DOI + Crossref status, real
  "new vs replicated" column, the closest competitor named (Liu & Raftery 2020; Kravdal 2002) and why
  this paper differs, search strategy recorded, unverifiable citations marked and not used as
  evidence.
- **`refs.md`** — 29 references, every one DOI-checked (V/S/U/N status).
- **`SOURCE_MAP.md`** — every number in the draft → branch @ commit → file → field.

## Source record
All empirical numbers: `research/corr-battery-2026-11-23` @ **9363079**
(`research/records/2026-11-23-corr-battery/`), pre-registration commits **772650a** and **6a1927f**
pushed before any code. No new estimation was run for this draft (box2 was down; none was needed).

## Novelty framing (auditor's verdict, adopted verbatim)
**INCREMENTAL — new assembly, not a new fact or method.** The within/between move is known (Nickell
1981; Angrist–Pischke; Durlauf et al. 2005; Eberhardt–Teal 2011); the aggregation critique is known
(Robinson 1950); the multiverse machinery is known (Steegen et al. 2016; Simonsohn et al. 2020; Patel
et al. 2015). The auditor found no paper showing the country-level schooling–fertility correlation
vanishing under the within-change specification, quantified across thousands of partitions with a
purpose-built placebo. The paper is framed as an **audit, never a discovery**; there is no "first".

## Referee-memo compliance (from the auditor via the Lead)
- (a) "Just the within–between critique": conceded in §5.1; the audit's object is the application.
- (b) Nickell bias / measurement error / change-window sensitivity: §5.2, with explicit statements of
  what the battery's grid can and cannot resolve, and the change-window limit handed to §7.
- (c) Ecological fallacy: §5.3 scopes all claims to country aggregates and states plainly that the
  DHS individual gradient is cited from the literature, not estimated here; DHS comparison is Future
  Research item 1.
- The 13,800 partitions are called a **sensitivity universe, not a test** (§2.4, §4.3, §5.5), and the
  run's extension beyond the pre-registered 800 is stated.
- Future research covers the six designs the memo expects, including DHS individual panel with
  schooling-reform exposure, subnational DHS-region panel, and natural experiments (school
  construction, compulsory-schooling laws), each with what it would and would not identify.

## Data gaps and limits (also in the paper)
No DHS individual-level estimate in this record; no cohort-fertility or natural-experiment estimate;
the change estimates cannot separate "no effect" from "effect with a longer lag or measurement
error". These are stated as limits, not papered over; they are the future-research agenda.

## Files
`paper.md`, `claims-prior-art.md`, `refs.md`, `SOURCE_MAP.md`, this `README.md`.
