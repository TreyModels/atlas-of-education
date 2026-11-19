# The gate

A model moves from the teaching Atlas into `research/` only when its folder answers these six points, in this order. The README of every research folder uses the same headings so the answers are easy to find.

| # | Gate | What the README must show |
|---|---|---|
| 1 | **Fact check** | The pattern to be explained, with a second independent source. If the sources disagree, that comes first. |
| 2 | **Two rivals** | At least two explanations, one plain sentence each. An explanation with no rival is a description. |
| 3 | **The separating observation** | What the rivals predict differently, written down before any code is run. |
| 4 | **Small, or recoverable** | Five or fewer free parameters. A larger model must pass a recovery test: fake data made with known settings, and the fitting procedure finds them again. |
| 5 | **A benchmark** | A naive rule the model has to beat (last year's value, chance, a model with no mechanism). A loss is reported as a loss, in the first sentence of the results. |
| 6 | **Owned** | Every parameter and every step explained in one sentence each, in words the author can defend aloud. |

## House rules

- **No hand-typed numbers.** Each README is written by a `make_readme.py` script from the result files, so the text cannot drift from the results.
- **Engines are not edited for research.** Research code imports the engines in `engine/` and `experiments/` unchanged, or copies them with a note. The site keeps working.
- **Two active research models at most.** New ideas go in `PUZZLE_LOG.md` in the three-line format (fact, rivals, separating observation). They wait there until a slot is free.
- **Frozen forecasts are never refitted before scoring.**

## Status words

- `calibrated`: fitted to sourced data and tested on data it did not see.
- `fitted + free residual`: fits only with an unexplained fitted term.
- `illustrative`: assumed or invented parameters. Fine for teaching, not for claims.
- `not identified`: the available data cannot tell the rival explanations apart. This is a result, and it says which data would.
