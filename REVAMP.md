# Revamp: 14 November 2026

This branch reorganises the project into a teaching track and a research track without moving or changing the existing engines or the site. Start with `research/README.md` and `teach/README.md`.

## What was added

- `research/GATE.md`: the six points a model must meet before it counts as research, and the house rules (generated READMEs, engines not edited, two active models at most).
- `research/PUZZLE_LOG.md`: where new ideas wait, in a three-line format.
- `research/shadow-education/`: an exact check that the "favour" explanation is the "thin" explanation relabelled, a recovery test on 24,000 simulated datasets, and a ranking of unmeasured outputs.
- `research/credential-floor/`: a fourth rival structure (Breen and Goldthorpe's relative risk aversion), a recovery test, and a ranking of what would separate the four.
- `research/china-forecast-ledger/`: five small forecasters, a rolling-origin evaluation against the naive rule, a frozen ledger for October 2026 to March 2027, and a scoring script.
- `research/marriage-gap/`: a worked example of the gate on the IFS marriage-wishes chart, with a source check.
- `research/methods-paper/`: outline v2, a reference list with a verification status for each entry, and a novelty assessment.
- `teach/`: twelve "find the built-in result" exercises, an eight-session course map, and a guide to the status labels.

## What was changed in existing files

- `engine/firms/seasonal_2024.py`: the prose under "What this establishes" is now computed from the results, and a `--render-only` flag regenerates the write-up without refitting.
- `engine/firms/results/seasonal_2024.md`: regenerated. It now says that the variant chosen on training fit does not beat the naive benchmark. `seasonal_2024.json` is byte-identical.

Nothing under `public/`, `src/`, `docs/` or `dist/` was touched, and no pinned hash changes.

## What the new results change in the plan

1. **The shadow-education paper cannot be written from the current model.** Inside it the three explanations are one. The paper needs a redesigned model in which each explanation has its own observable consequence, and pupil-level data. Ask Mark Bray's team about the Siem Reap survey before more modelling.
2. **The methods paper moves to first place.** It now has three worked identification results (shadow education, credential floor, forecast ledger) and a verified reading of the analytical-sociology literature. See `research/methods-paper/OUTLINE_v2.md`.
3. **The massification paper gets a sharper test.** Wealth gradients cannot separate the theories; the response of completion to a change in the graduate premium can.

## Stale pages: fixed when the revamp was merged (15 November 2026)

- **Out of Africa page:** already replaced by ooa-coast-vs-herds PR #2 and #3.
- **Credential-floor world:** now reads the v2.1 graded-liquidity results (`relfloor_countries_v2_smoothliq.json`) through `scripts/build-relfloor-evidence.py`. It shows the 2021 poorest-40% share and the relational-weight posterior. The 2035 projections are dropped.
- **`engine/firms/results/china_fit.md`:** the August 2021 step is labelled "unexplained", matching `calibrate_china.py`.
- **`docs/engine/relational_floor_test.md` and `relational_floor_countries.md`:** each now opens with a superseded notice.
- **Shadow-education page and story:** the fresh-world fit was already corrected. Both now also say that favour is thin relabelled.

## Only the author can do these

- Register for CFPS and CGSS, and apply for the Cambodia DHS 2021–22 microdata.
- Write to Mark Bray's team about pupil-level data from the Siem Reap study.
- Find a quantitative coauthor for the microdata paper.
- Append each new NBS youth figure to the ledger and run the scoring script.
- State whether the 70–73 ka humid window in the Out of Africa model was chosen before or after seeing the Nefud date.

## Checks run

- `research/china-forecast-ledger/test_ledger.py`, `research/credential-floor/test_structures.py`, `research/marriage-gap/test_model.py`: all pass.
- `engine/firms/results/seasonal_2024.json` compared byte for byte with the committed version: identical.
- Not run: the Node checks in `scripts/check-all.sh` (no `node_modules` in the build environment) and the long engine fits.
