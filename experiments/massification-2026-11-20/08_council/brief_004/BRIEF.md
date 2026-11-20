> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# RESULTS BRIEF 004 — ITERATION 2 DESIGN REVIEW (pre-results)

- **sent by / date:** lead, 2026-11-20 ~13:05 Asia/Shanghai (transcribed from the task-14 message; no separate
  brief file was supplied).
- **purpose:** review the research-loop design *before* iteration-2 results exist, and fix the anti-re-parameterisation
  requirements, stopping rules, and the one variable to change.
- **informs:** the iteration-2 workstream specification (country cards, target sets, calibration, two-way economy,
  endogenous shadow sector) and the brief-005 review.
- **provisional or final?** provisional by nature (design); the loop's own file is the mutable object.

## 1. Artifacts (read at 13:04–13:07)

| artifact | path | status at intake |
|---|---|---|
| Research loop design | `06_report/RESEARCH_LOOP.md` | **not present at 13:02; present 13:07** (120 lines: loop A–E, shadow-incidence operationalisation, two-way requirement, iteration log, stopping rules) |
| C1 recovery / identification | `05_experiments/runs/C1/findings.txt` (+ c1_confusion.csv, c1_candidate_moments.csv) | completed, pilot-strength (2 noise draws, small grids) |
| C2 floorworld E11 (supplied vs generated) | `05_experiments/runs/C2/findings.txt` (+ c2_decomposition.csv) | completed (instant; prior midpoints; 5 structures) |
| Batch C status | `05_experiments/runs/C_STATUS.md` | C3 PH calibration in progress, **not claimed** |
| Open questions / costed next steps | `OPEN_QUESTIONS.md` | completed |
| Iteration-1 package | `RESULTS_README.md`, `SUMMARY_FOR_TREY.md` | completed |

**Note on iteration-2 artifacts:** none exist yet on disk (`02_lit/COUNTRY_CARDS/`, `04_data/TARGETS_*.csv`,
`05_experiments/loop2/`, `05b_experiments/loop2/` were absent at intake). This review is therefore of the *design*,
not of results.

## 2. Questions (from task-14 / lead message)

1. **(a) Loop design:** is `country cards → target sets → calibration → economy feedback → council review` sound?
2. **(b) Anti-re-parameterisation:** given C1 (surplus vs competitive CES not identifiable on six moments) and C2
   (attainment supplied; jobs not from schooling), what must iteration 2 do to be more than re-parameterisation?
3. **(c) Stopping/falsification criteria and publishability** at each stage.
4. **(d) The single most important variable** to change next.

## 3. Known limitations carried into the review

- C1 is pilot-strength: six aggregate moments, two noise draws per truth, small candidate grids; its own caveat says
  so. The forced-identification result (truth outside the model set assigned to the surplus world 2/2) is the
  load-bearing warning.
- C2 freezes only schooling schedules; "NOT-FROM-SCHOOLING" for formal jobs means the job rise comes from
  investment/industrial-policy schedules and capability feedback, not that it is free-running emergence.
- C3 (PH calibration) is unfinished: no number is reported anywhere; nothing in this brief depends on it.
- C1/C2 are the only iteration-2 inputs that exist; the country cards and target sets do not.

## 4. Budget

- design review, no compute; synthesis ≤900 words.

## 5. Council answer summary

See `SYNTHESIS_004.md`: design sound in architecture, fit-first in sequencing; six anti-re-parameterisation
requirements; four additional stop rules; stage-by-stage publishability; single variable = **provider supply/entry**
(with teacher-tutor capacity).
