# Revision log — Paper M (task-3)

**Branch:** `research/paper-massification-2026-11-25` (base `76d929a`).
**Record:** `research/records/2026-11-25-paper-massification/`.
**Revision date:** 25 November 2026 (session). **Revision commit:** see the last commit touching `paper.md` on this
branch (the hash is recorded in the hand-off message; this file was committed with the revision).
**Draft after revision:** 17,968 words (was 17,433; target 12,000–18,000).

## Why

Task-3 of the paper-revision wave: integrate E6 (pre-1990 demand timing), E8 (fee-abolition event study with
verified dates) and N3 (threshold/smoothing), retire the 7% labour-demand figure and all "demand is ruled out"
framing, soften supply-led/sequencing causal language, label data tiers, and recompute every quoted number from the
committed records.

## Sources read (all read from committed branches, not from prose)

| source | branch @ commit | what it supplied |
|---|---|---|
| Handoff §3–5 | `research/handoff-2026-11-24` (`HANDOFF.md`) | verified heads, retraction list, evidence rules |
| Codex wave ledger | `research/handoff-2026-11-24` (`research/records/2026-11-24-handoff/codex_wave_ledger.md`) | F02/F12 retraction, contract, verified status |
| E6/E8/N3 | `research/e6e8-sequencing-2026-11-25` @ `2d19da7` | `REPORT.md`, `results/e6_summary.json`, `results/e8_results.json`, `results/n3_recommendation.json` |
| Fee dates | `research/codex-source-verification-2026-11-25` @ `9a0fd69` | `fee_dates.csv` (8 verified, 4 unresolved) |
| Sequencing | `research/subsistence-v2-2026-11-23` @ `ce66cfc` (+ correction note @ `8caaeac`) | `results/event_dates.csv`, `results/sequencing.txt/.json` |
| Supply vs demand | `research/supply-demand-2026-11-23` @ `963e5e5` | `results/supply_demand.json/.txt` |
| Historical cases | `research/historical-sequence-2026-11-23` @ `ab658c7` | case dates and verdicts (all UNVERIFIED) |
| Agricultural floor | `research/subsistence-2026-11-23` @ `41f6429`, `research/subsistence-v2-2026-11-23` @ `ce66cfc` | elasticities, dynamic nulls, joint model |
| Scaling / driver nulls | `research/scaling-2026-11-23` @ `fd691a6`; `research/grouping-multiverse-400-2026-11-23` @ `1152cec` | exponents, collapse curve, multiverse |
| Credential / care | `research/care-credential-2026-11-23` @ `e626cb8` | credential gap and care-loop results |

## What changed in `paper.md`

1. **Retracted 7% figure removed / replaced.** Removed from the abstract, §1 ("finding in one paragraph"), §2,
   §7.5 (old §6.5 "Labour-market demand specifically does not lead"), §14 synthesis and box, §15 objection 11 and
   §16 conclusion. The figure now appears only where explicitly labelled retracted. Replacement (E6): demand-first
   10.0% (GGDC non-agricultural employment), 15.4% (urbanisation), 24.1% (industry value added), 18.8%
   (agricultural value added) of identifiable countries; all-country bounds 6.7–53.0%; 21–43% weak ties or
   left-censored; N3 54-definition range 0.0–30.8% (median 10.45%). Honest framing throughout: **"schooling and
   structural change move together, with schooling typically but not universally first."** All "demand is ruled
   out / the demand account is hard to maintain" phrasing removed or rewritten as "neither eliminated nor cleanly
   ordered".
2. **Supply-led / sequencing causal language softened.** Title changed from "supply-led massification … why it is a
   regularity rather than a law" to "schooling, structural change and the sequencing of massification in
   late-industrialising countries". Thesis rewritten as an association ("mass schooling and structural change moved
   together"), demand-led/state-supply accounts described as *descriptions* that differ by case, not causes.
   Historical case labels changed from "supply-led" to "state supply/supply-side"; §9.4 and §10 headings changed
   from "what drives massification" to "what the evidence says …"; §12.1 heading changed to "supply-side versus
   demand-led accounts"; "the supplier determines the sequence" → "the sequence co-varies with the supplier"; policy
   phrasing changed from "the lever that moved massification" to "the lever associated with historical
   massification". The one permitted "consistent with" causal-style statement is the E8 event study (checked
   pre-trends), and the paper says so explicitly.
3. **New §7.6 "Supply-side event evidence: fee abolition and primary enrolment" (E8).** Verified dates (MWI 1994,
   ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005; CMR/ZMB/RWA/BDI unresolved and excluded
   from main); CS event study with pre-trends at −2/−3/−4 flat, post-effects +22 to +29 points at +1..+6, TWFE
   similar, placebo −0.39, LOO 18.2–26.2, on-impact interval spanning zero, secondary-GER proxy with no clear
   detected effect; explicit ties/censoring and sparse-coverage caveats. Also referenced in abstract, §14 box,
   §15 objections 11–12 and Appendix A.
4. **N3 integrated into §7.5** (threshold/smoothing range 0.0–30.8%, median 10.45%; ordering reported as an
   interval, not a point estimate).
5. **Data tiers labelled.** New §4.1 data-tier table (observed / reconstructed / imputed / literature-standard,
   with the ILO-modelled agricultural share and the verified/unresolved fee dates called out); Appendix A gains a
   data-tier column; §4.2 states that the WDI total fertility rate used for the event dates is a birth-based TFR and
   is *not* the project's effective-fertility measure (construct difference 0.3042 median / 4.2677 max stated).
   "TFR" is used only for the birth-based WDI series and the joint model's birth-based TFR.
6. **Internal consistency.** Abstract, §2, §6.1, §7.5–7.7, §14 synthesis/box, §15 limitations and §16 conclusion
   now state the same E6/E8 numbers. Subsection numbering fixed (was off by one throughout: `### 2.x` under §3,
   `### 3.x` under §4, etc.; now `### 3.x` … `### 14.x`). Cross-references updated (`Section 7.5`, `Section 7.6`,
   `Sections 6–7`). README word count updated to 17,968; the draft is within the 12,000–18,000 target.
7. **Recomputation artefacts added.** `data/` now holds verbatim copies of the source records used by the revision
   (`e6_summary.json`, `e8_results.json`, `n3_recommendation.json`, `fee_dates.csv`,
   `supply_demand_963e5e5.json/.txt`, `event_dates_subsistence_v2.csv`). `scripts/verify_revision_numbers.py`
   recomputes 41 checks from these files; `data/revision_verification.json` — **41/41 pass**.

## Verification notes and discrepancies

- One source-record prose line did **not** reproduce: the E6 REPORT's "18–33% strict schooling-first". Recomputed
  from `e6_summary.json`, strict schooling-first is 25.0% (GGDC), 21.5% (urban), 46.3% (industry) and 43.8%
  (agriculture) of identifiable countries (21.5–46.3%). The paper uses the recomputed range and does not quote the
  REPORT line; recorded in `discrepancy.md` §H for the source-record owner.
- The E8 record cites fee dates at commit `bfb8c6f`; the verified branch head is `9a0fd69`. `fee_dates.csv` is
  byte-identical at the two commits, so the paper cites `9a0fd69`.
- **UNVERIFIED numbers:** the only quoted numbers that cannot be recomputed in this pass are the four historical
  sequences' literature dates/percentages; they remain labelled **UNVERIFIED literature standard** in the text and
  Appendix A. Numbers in §§9–11 were re-checked against their committed source records; where a record gives a
  value only in prose/table (no machine-readable field) it is marked "verified in record" rather than
  "recomputed".
- The 68.75%/69% fertility-ordering figure remains flagged and unused (strict ordering 37.5% = 24/64,
  CI 26.6–50.0; 31.25% simultaneous; 31.25% fertility-first; all-81 35.8%).

## Files changed

- `paper.md` — revised draft (17,968 words).
- `claims-to-source-map.md` — claim 6 marked retracted; rows 32–36 added (E6, E8, data tiers, 7% retirement,
  recomputation).
- `README.md` — word count, deliverables, verification status, synthesis verdict, revision note.
- `discrepancy.md` — §H added (E6/E8 integration, 7% retirement, recomputation, E6 prose discrepancy).
- `REVISION_LOG.md` — this file.
- `data/` — six source-record copies (new).
- `scripts/verify_revision_numbers.py` — new recomputation script.
- `data/revision_verification.json` — new output (41/41 pass).
