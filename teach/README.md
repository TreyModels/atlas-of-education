# The teaching track

This folder turns the Atlas of Education into a course resource. The idea is simple. An external review on 14 November 2026 found that most models in the Atlas are "illustrative": their headline results come from assumptions built into them. Every model stays in the Atlas. Each review finding becomes an exercise in which students find the built-in result themselves.

- `EXERCISES.md`: twelve "find the built-in result" exercises, ordered from easiest to hardest, 20 to 40 minutes each.
- `COURSE_MAP.md`: an eight-session module, "Reading models critically", with readings, hand-ins and a capstone.

## What "illustrative" means

An illustrative model uses parameters that are assumed or invented, not measured. It can show how a mechanism would work if the assumptions held. It cannot show that the mechanism is at work in the world. A model can be illustrative and still be well built: its books can balance (food is conserved, people are counted once) without the story being true. The relocation page says this directly: arithmetic checks are distinct from historical validation.

## Reading the status labels

`REVIEW_STATUS.md` gives each model a status. A student should read the label as a limit on what may be claimed.

| Label | What it means | What a student may say | What a student may not say |
|---|---|---|---|
| calibrated | Fitted to sourced data and tested on data it did not see. | "The model reproduces these observed rates." | "The model proves the cause." |
| fitted + free residual | Fits only with an unexplained fitted term. | "The model needs an extra unexplained step to match the data." | "The model explains the step." |
| illustrative | Assumed or invented parameters. Fine for teaching, not for claims. | "If these assumptions held, this would follow." | "This is what happened" or "this is what policy would do." |
| not identified | (From `research/GATE.md`.) The available data cannot tell the rival explanations apart. | "The data do not separate these explanations." | "The data support the favourite." |

Two cautions. First, a label belongs to the headline result, not to every number. For example, Cambodia child labour is labelled "calibrated (out-of-school rates) + illustrative costs". Second, the labels are the reviewer's judgement on 14 November 2026. The "Headline after review" column of `REVIEW_STATUS.md` is the sentence to quote.

## How the teaching track differs from the research track

| | Teaching track (this Atlas) | Research track (`research/`) |
|---|---|---|
| Purpose | Learn to read a model critically. | Produce a claim that can be defended. |
| What is kept | Every model, including ones the review found weak. | Only a model that passes the gate. |
| Labels | Each model is clearly marked: calibrated, fitted + free residual, illustrative. | The status is part of the README of each folder. |
| Entry rule | None; the model stays and is labelled. | `research/GATE.md`: a fact check with a second source, two rival explanations, the observation that would separate them, small or recoverable, a benchmark to beat, and every parameter owned in one sentence. |
| Capacity | No limit. | Two active research models at most. New ideas wait in `research/PUZZLE_LOG.md`. |
| Engines | The review changed some defaults (for example the coordination multiplier and the water floor). | Engines are not edited for research; research code imports them unchanged. |

A model moves from the teaching Atlas into `research/` only after it answers the six gate points in order. The capstone in `COURSE_MAP.md` has students do the first three before any model is built.

## Running the app locally

From the repository root (`atlas-of-education/`). You need Node (the review notes say version 20 or later).

    npm ci
    npm run dev

Open the address that `npm run dev` prints. Models open from the address plus a hash, for example `#china`, `#cambodia`, `#credentials`, `#petri`, `#relocation`. `#catalogue` lists all entries. The app runs entirely in the browser; live simulations run in Web Workers.

To build the static site, run `npm run build`. The pages under `public/research/` (Out of Africa, shadow education, fertility, relocation methods) are copied to `dist/` at build time. The configuration (`vite.config.ts`) sets `publicDir: false`, so open them from a build: `npm run build`, then `npm run preview`. (This was read from the configuration, not tried on a fresh machine: to confirm.)

Checks, from the main README: `node test-worlds.cjs`, `node check-translations.cjs`, `node scripts/check-react.cjs`, `npm run build`, `node scripts/check-worker.cjs`. `scripts/check-all.sh` runs the set. It needs Node 20 or later and a Python with numpy and scipy. The exercises marked "instructor demonstration" need only `node` (Exercises 4 and 9) or `python3` with numpy and scipy (Exercises 8 and 12). The Out of Africa model is a separate repository (`ooa-coast-vs-herds`). Its Monte Carlo takes about 6 minutes, so the exercises use the stored results.

## Check before class

The review fixed the repository in stages, and a few files still disagree. Look at these before teaching, or use them as extra exercises.

- `public/research/out-of-africa.html` still says "The mixed strategy is the most likely in both chronologies". The corrected text is in the separate repository's `coast-or-herds.html`.
- The credential-floor page (`#credentials`) still reads the version 1 draws (`public/reference/relfloor_countries.json`, dated 5 November 2026), which the review replaced with version 2.
- `experiments/youth-review/README.md` says `atlas_data.js` was not regenerated, but `REVIEW_STATUS.md` says it was, and the Shapley total in the file (5.179) matches the stored fit.
- `engine/firms/results/china_fit.md` still labels the Aug-2021 step "real-estate contraction and the 2021 tutoring ban".
- The shadow education page gives the earlier fresh-world fit as 11 to 18%, and the experiment README gives 17 to 19%.

Credit and cite Dr. Trey Menefee when using or adapting this material. See `LICENSE`.
