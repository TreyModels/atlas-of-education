# Missing artifacts — cannot verify the claimed Paper A results without these

The bridge handoff `95831e67` asked for all of the following to be committed. They were **not attached**, so
they are not in this deposit. Nothing here has been reconstructed or approximated.

| # | artifact | status | needed for |
|---|---|---|---|
| 1 | Paper A `.docx` (Google Doc `1NFXSjzRaAXR2nhM6iZVTlhJKcE5puj7PI43ZZkP2cns`) | **NOT RECEIVED** | Paper A text |
| 2 | `engine/eduengine/core.py` **patched file/diff** (Tullock `contest` gate) | **NOT RECEIVED** (spec received only) | Exp 3, 5, Paper B |
| 3 | `engine/eduengine/modules/tutoring.py` **patched file/diff** | **NOT RECEIVED** (spec received only) | Exp 3, 5, Paper B |
| 4 | `run_hk_korea_comparative.py` | RECEIVED — but static check shows it does not fit the committed `Engine` API; see `RUNNER_STATUS.md` | Paper B |
| 5 | `results/exp1_bulge_arrival_summary.json` | bundled inside `results/verified_results_2026_11_25.json` (self-reported) | Paper A Exp 1 |
| 6 | `results/exp3_contest_h1_h2_summary.json` | bundled inside `verified_results_2026_11_25.json` (self-reported) | Paper A Exp 3 |
| 7 | `results/exp4_tutoring_identifiability_summary.json` | bundled inside `verified_results_2026_11_25.json` (self-reported) | Paper A Exp 4 |
| 8 | `results/exp5_e8_shock_summary.json` | bundled inside `verified_results_2026_11_25.json` (self-reported) | Paper A Exp 5 |
| 9 | `results/hk_korea_comparative.json` | bundled inside `verified_results_2026_11_25.json` (self-reported) | Paper B |
| 10 | Exact patched engine commit / pre-registration hashes | **NOT RECEIVED** | reproduction of all simulation claims |

## Why this matters

- The committed `eduengine` in this repository has **only `bar` and `quota`** gate kinds; the dispatch is
  `if kind == 'bar' … else: # quota`, so an unknown kind is silently treated as quota. See
  `research/records/2026-11-25-equifinality-phase/PRE_REGISTRATION.md` (commit `078cc13`). A `contest` gate
  therefore requires the patch above to be committed and hash-pinned before any Exp 3/5/Paper B number can be
  reproduced or cited.
- The committed bulge-arrival record says `t*` is **NOT-ESTIMABLE** in-repo (`L_primary` sourced 0/8). Exp 1
  claims a live-WDI series (7,290 observations); that data and its hashes must be committed to make the claim
  auditable.
- The shadow-equations identifiability work is currently **quarantined** (`research/shadow-equations-review-2026-11-25`
  @ `264c059`); Exp 4 must be reconciled with that record before citation.

## How to deposit

Attach the files to the bridge (the `send_file`/attachment path used for Paper B) or push them to this branch.
Once present, they can be verified by re-running the runner against the committed engine patch and hashing the
results JSONs.
