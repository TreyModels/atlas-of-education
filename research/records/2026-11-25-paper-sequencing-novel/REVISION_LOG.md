# Revision log — Paper N1 (task-3)

**Branch:** `research/paper-sequencing-novel-2026-11-25` (base `7f73ff1`).
**Record:** `research/records/2026-11-25-paper-sequencing-novel/`.
**Revision date:** 25 November 2026 (session). **Revision commit:** the hash is filled in by the follow-up commit that records it (the main revision of
`PAPER.md` is the preceding commit on this branch).
**Draft after revision:** 6,898 words (was 6,040; this record keeps no word-count target of its own).

## Why

Task-3 of the paper-revision wave: fold the corrected sequencing/E6 fact into the standalone sequencing draft,
retire the 7% labour-demand figure and "demand is ruled out" framing, align the paper with E6 (pre-1990 demand
timing) and E8 (fee-abolition event study with verified dates), soften supply-led/sequencing causal language,
label data tiers, and recompute every quoted number from the committed records.

## Sources read (committed branches, not prose)

| source | branch @ commit | what it supplied |
|---|---|---|
| Handoff §3–5 | `research/handoff-2026-11-24` (`HANDOFF.md`) | retraction list, evidence rules |
| Codex wave ledger | `research/handoff-2026-11-24` (`research/records/2026-11-24-handoff/codex_wave_ledger.md`) | F02/F12 retraction of the 7% figure; verified status |
| E6/E8/N3 | `research/e6e8-sequencing-2026-11-25` @ `2d19da7` | `REPORT.md`, `results/e6_summary.json`, `results/e8_results.json`, `results/n3_recommendation.json` |
| Fee dates | `research/codex-source-verification-2026-11-25` @ `9a0fd69` | `fee_dates.csv` (8 verified, 4 unresolved) |
| Sequencing | `research/subsistence-v2-2026-11-23` @ `ce66cfc` | `results/event_dates.csv`, `results/sequencing.txt/.json` |
| Supply vs demand | `research/supply-demand-2026-11-23` @ `963e5e5` | `results/supply_demand.txt/.json` |
| Historical cases | `research/historical-sequence-2026-11-23` @ `ab658c7` | case dates (all UNVERIFIED literature standard) |

## What changed in `PAPER.md`

1. **Retracted 7% figure removed / replaced.** Removed from the abstract, §1, §4.2 ("Which demand"), §4.4
   (Falsifier 3) and §10; it now appears only where explicitly labelled retracted. Replacement (E6): demand-first
   10.0% (GGDC non-agricultural employment), 15.4% (urbanisation), 24.1% (industry value added), 18.8%
   (agricultural value added) of identifiable countries; all-country bounds 6.7–53.0%; 21–43% weak ties or
   left-censored; N3 54-definition strict range 0.0–30.8% (median 10.45%). Honest framing throughout:
   **"schooling and structural change move together, with schooling typically but not universally first."** The
   Falsifier-3 section now says strict demand-first is a minority ordering but the tie/censoring band means demand
   is not ruled out.
2. **Supply-led / sequencing causal language softened.** Abstract: "Prussia state supply 80–120 years ahead",
   "US state-supplied"; §1: "schooling-first where the state supplied"; §2: "make a general demand-led ordering
   hard to reconcile" instead of "cannot be the general one"; §4.2: "consistent with a supply-side reading … not
   with a causal claim"; historical headings changed from "supply-led" to "state supply"; §6: "makes a general
   demand-led ordering hard to reconcile with the data" and "does not rule demand out"; §7: "the sequence
   co-varies with the supplier", policy lever "associated with" rather than "caused"; §10 conclusion reframed as
   association. The one permitted "consistent with" causal-style statement is the E8 event study (checked
   pre-trends), and the paper says so explicitly.
3. **E8 folded in and aligned.** New §8 design 5 ("The one event study with checked pre-trends"): 8 verified fee
   dates (MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005; CMR/ZMB/RWA/BDI
   unresolved and excluded), Callaway–Sant'Anna post-effects +22 to +29 points at +1..+6, flat pre-trends at
   −2/−3/−4, placebo −0.39, leave-one-out 18.2–26.2, on-impact interval spanning zero, 7 treated countries; it
   identifies an enrolment effect only, not the sequencing. Also referenced in the abstract, §9 limits and the
   data-availability section.
4. **N3 integrated into §4.2** (0.0–30.8% strict range across 54 threshold/smoothing definitions, median 10.45%,
   ordering reported as an interval).
5. **Data tiers labelled.** Abstract data-tier sentence; §3 panel paragraph labels schooling (reconstructed),
   agricultural employment (observed but ILO-modelled) and fertility (observed WDI birth-based TFR); §3.1 repeats
   the TFR construct point; §3 states that the WDI total fertility rate is **not** the project's
   effective-fertility measure (construct difference 0.3042 median / 4.2677 max).
6. **Internal consistency and discrepancy handling.** Abstract, §4.2, §4.4, §8, §9 and §10 now state the same
   E6/E8 numbers. The §9 'internal discrepancy' paragraph was replaced with a fuller statement: the strict
   schooling-before-fertility ordering is 37.5% (24/64, 95% CI 26.6–50.0), 31.25% simultaneous, 31.25%
   fertility-first, 35.8% across all 81 with both dates; the record JSON's 68.75% counts ties as schooling-first
   and is not used. IQR row clarified (forward-case IQR 16.5–29.5; all-64 gap IQR 16–29).
7. **Recomputation artefacts added.** `data/` holds verbatim copies of the source records used by the revision
   (`e6_summary.json`, `e8_results.json`, `n3_recommendation.json`, `fee_dates.csv`,
   `supply_demand_963e5e5.json/.txt`). `scripts/verify_revision_numbers.py` recomputes 28 checks from
   `results/event_dates.csv` and the `data/` copies; `results/revision_verification.json` — **28/28 pass**.

## Verification notes

- A source-record prose line did **not** reproduce during the parallel Paper M revision: the E6 REPORT's
  "18–33% strict schooling-first". Recomputed from `e6_summary.json`, strict schooling-first is 25.0% (GGDC),
  21.5% (urban), 46.3% (industry), 43.8% (agriculture) of identifiable countries. This paper quotes the E6
  demand-first shares and bounds (which reproduce exactly) and does not quote the 18–33% line.
- The E8 record cites fee dates at commit `bfb8c6f`; the verified branch head is `9a0fd69`, and `fee_dates.csv`
  is byte-identical at the two commits, so the paper cites `9a0fd69`.
- **UNVERIFIED numbers:** the only quoted numbers not recomputable in this pass are the four historical
  sequences' literature dates/percentages; they remain labelled **UNVERIFIED literature standard** in §5 and the
  claims map.
- The 7% figure is kept only as an explicitly retracted sentence so that a reader who knows the old draft can see
  what replaced it; no substantive claim rests on it.

## Files changed

- `PAPER.md` — revised draft (6,898 words).
- `claims-to-source.md` — rewritten with retraction row, E6/E8/N3 rows and the recomputation note.
- `REVISION_LOG.md` — this file.
- `data/` — six source-record copies (new).
- `scripts/verify_revision_numbers.py` — new recomputation script.
- `results/revision_verification.json` — new output (28/28 pass).
