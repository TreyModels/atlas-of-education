# 04 · Monte Carlo and sensitivity

**Goal.** Run the Atlas's four Monte Carlo questions through one manager — which parameter worlds are plausible, does
a policy work net of simulation noise, which parameters drive an outcome, and does the answer depend on how the
model is built — with seeds and provenance that can be reproduced.

**Use `engine/mc.py` for all of it.** The module docstring states the conventions; do not change them casually,
because stored results depend on them. The tests are `engine/test_mc.py` (15 tests: known answers, determinism,
parallel equals serial, Sobol on the Ishigami function, matched policies).

**You need.** Python with numpy and scipy (for the Sobol and Latin-hypercube designs), the model imported from
`engine/`, and a function you can call cheaply. Run from `engine/` or add it to `sys.path` as the existing scripts
do (`engine/childworld_sobol.py`, `engine/camchild_ridge.py`, `engine/firms/stories.py`).

## Steps

1. **Confirm the manager before using it.**

   ```bash
   cd engine
   python -m unittest test_mc        # Ran 15 tests ... OK (about 2 s)
   ```

2. **Write the prior box.** A prior is a dict `{name: (low, high, 'lin' | 'log')}`; `'log'` means log-uniform.
   The cross-country priors are the model of the form (`engine/childworld.py`):

   ```python
   PRIORS = {'y_med': (0.4, 3.0, 'log'), 'w_child': (0.05, 0.6, 'lin'), ...}
   ```

   Draw from it with `mc.draw_prior(priors, n, master=7, design='random')`. `design='random'` reproduces the old
   `childworld.draw(default_rng(7), n, priors)` bit for bit (there is a test for exactly that); `'sobol'` and
   `'lhs'` are the scrambled low-discrepancy designs for sensitivity work. Do not switch designs for a comparison
   you intend to quote against stored results.

3. **Run a batch.** `sim(theta, seed) -> dict` must be a module-level function: the manager pickles it to worker
   processes. Then:

   ```python
   import childworld as W, mc as MC

   def sim(theta, seed):
       return W.simulate(theta, seed=seed)

   thetas = MC.as_rows(MC.draw_prior(W.PRIORS_V2, 200, master=7))
   outs = MC.monte_carlo(sim, thetas, MC.matched_seeds(200))       # one world per seed
   ```

   `mc.matched_seeds(n, reseed=0)` gives the simulation seed of world *i* as `100000 * reseed + i`. Same worlds and
   same `reseed` reproduce the same noise; a new `reseed` reruns the same parameter worlds with fresh noise, which is
   how seed noise is measured (`childworld_mc.py` does this on 300 worlds). `workers=1` runs in-process, which is
   what the tests use; the result is identical to the parallel path.

4. **Compare policies on matched random numbers.** `mc.paired_effects(sim, policies, seeds, outcome)` runs the
   baseline `{}` and every policy on the same seed per world; the effect is the within-seed difference, and
   `mc.summarize` claims a sign (`'lower'`/`'higher'`) only when the 95% interval over seeds excludes zero,
   otherwise `'none'`. `engine/camchild_ridge.py`'s `seed_check` is the worked example: every curated Cambodia
   policy on seeds 1–4 through `MC.paired_effects`, then the report states which policies are robust and which
   have "no established sign" across variants. Use `result['_raw'][policy]` for your own tables;
   `result['_baseline']` holds the base run values.

5. **Sobol indices, with intervals.** `mc.sobol_indices(f, priors, n=1024, master=0, boot=200)` returns first-order
   `S1` and total-order `ST` (Saltelli 2010 design, Jansen total-order estimator) with 5–95% bootstrap intervals;
   `mc.stiff_directions(idx, 0.05)` returns the parameters whose total-order index is at least 0.05, biggest first.
   Two rules: `n` should be a power of two, and the simulation seed inside `f` must be FIXED, or simulation noise
   is counted as variance that no parameter explains. Cost is `n * (d + 2)` model evaluations.

   The worked example is `engine/childworld_sobol.py`: four outcomes, each with its own module-level
   `f_*` function holding `seed=0`, `n=1024`, ten priors (12,288 worlds per outcome), `boot=100`, output
   `engine/results/childworld_sobol.{json,md}`. Run it with:

   ```bash
   cd engine
   python childworld_sobol.py --n 1024
   ```

   It writes the stored result — do not run it just to read the table; read `engine/results/childworld_sobol.md`.
   The answer it produced on 5 November 2026: the value of state D (neither school nor work) is the stiffest
   parameter for three of the four outcomes; the value of school leads for the share of child labourers still in
   school; the farm share is inert under these priors.

   Three more sweeps were added in the 6 November 2026 run, one per remaining engine, all on the same manager:

   ```bash
   cd engine
   python camchild_sobol.py --n 64 --workers 2        # assumed context constants; -> engine/results/camchild_sobol.{json,md}
   python atlas_sobol.py --n 64 --workers 4           # history_match.SPACE box; -> engine/results/atlas_sobol_cambodia.*
   python -m firms.china_sobol --n 256 --workers 3    # broad behavioural ranges; -> firms/results/china_sobol.{json,md}
   ```

   The camchild/atlas sweeps are expensive (one engine run per evaluation, ~1 s each), so they default to small
   `n` and a few workers; the China model is cheap (~0.06 s per evaluation) and defaults to `n=256`. Sizing rule
   from the runs: engine cost × `n × (d + 2)` evaluations ÷ workers should stay well under an hour.

6. **Approximate Bayesian computation.** `mc.abc_accept(outputs, targets, tol)` returns a boolean mask of worlds
   within `tol[key]` of `targets[key]` on every key. `engine/childworld_mc.py` is the full worked example: 20,000
   worlds, each country matched on out-of-school (lower secondary) and child labour with tolerances
   `max(2.5, 0.2 * target)` and `max(1.5, 0.2 * target)`; accepted worlds give posterior medians and the predicted
   composition of the out-of-school, which is then compared with survey data that were NOT used in the matching.
   Keep the world count and tolerances in the report; an "accepted" count below 5 is not a posterior.

7. **Compare structures.** `mc.compare_structures(models, thetas, seeds, keys)` runs rival models on the SAME
   parameter draws and seeds, and for each output key reports per-structure means, every pairwise mean difference
   with its interval, the share of worlds where the first is higher, the rank correlation (do the structures agree
   about which worlds are high?), and `between_share` — the share of output variance that sits between structures
   rather than between worlds. Near zero means the conclusion does not depend on the structure. Models are
   `{name: sim(theta, seed) -> dict}` and every `sim` must be module-level for the same pickling reason.

8. **Record provenance.** Every stored Monte Carlo result carries `mc.provenance(...)` — manager version, numpy
   and scipy versions, plus the design, master seed and reseed where they apply. Copy the pattern in
   `childworld_mc.py` and `childworld_sobol.py`:
   `provenance=MC.provenance(design='random', master=7, reseed=0)`. A result without seed, design and version cannot
   be reproduced.

9. **Know where the other Monte Carlos are.**
   - China story tournament: `engine/firms/stories.py` uses `MC.rng` and `MC.run_batch`; it proposes draws around
     each fit and keeps only those inside the 90% joint confidence region (Bates & Watts SSR test), reported in
     `firms/results/stories.md`. `python -m firms.stories --draws 400` from `engine/` is the `--full` run (about
     15 minutes on 2 cores).
   - China strict tournament: `firms/stories_strict.py` uses the same manager (`MC.rng`, `MC.run_batch`) and is a
     `--full` step (`python -m firms.stories_strict --starts 6`, about 10 minutes on 2 cores).
   - The strict forecast scripts (`firms/forecast_strict.py`, `firms/forecast_2024.py`, `firms/seasonal_2024.py`)
     do not go through `mc.py`: they fit with seeded numpy multi-starts (`np.random.default_rng`), so they are
     reproducible but are not managed here.
   - Cambodia: the app's 30-seed bands are produced by the JavaScript recorder `engine/camchild_record.cjs`, which
     follows the same matched-seed rule with seeds 1..30 (`mc.APP_SEEDS`); that file cannot import Python, so the
     convention is duplicated deliberately. The ridge `seed_check` is Python and goes through `mc.py`.

## Checks

- `python -m unittest test_mc` passes.
- A sign is claimed only with an interval excluding zero; quote the interval, not just the mean.
- Sobol `S1` is not larger than `ST` beyond bootstrap noise, and the evaluation count in the metadata equals
  `n * (d + 2)`.
- Changing `reseed` on the same parameter worlds changes the seed-noise estimate but not the parameter draw; changing
  `master` changes the draw.
- Stored results include provenance, and a rerun with the same arguments reproduces them exactly (the stored
  `childworld_mc_v1/v2` and `camchild_ridge` results have been reproduced this way).

## Common failures

- **A lambda or a function defined inside `main()` passed to `monte_carlo`/`sobol_indices`.** The worker processes
  cannot pickle it: define the function at module level, as `childworld_mc.py`, `childworld_sobol.py` and
  `stories.py` all do.
- **A varying simulation seed inside the function.** Then the noise enters the Sobol variance and the indices stop
  meaning "share of variance explained by parameters". Fix the seed inside `f` and measure seed noise separately by
  rerunning the same worlds with a new `reseed`.
- **Too few seeds, then a confident sentence.** With a handful of seeds the interval includes zero and the manager
  correctly says `'none'`; do not report the mean as an effect anyway. The Cambodia ridge's seed check runs four
  seeds on two of its five calibration variants and reports ranges, not stars.
- **Sobol with a non-power-of-two `n`, or a design changed between runs.** `n` should be a power of two; the stored
  results were produced with `design='sobol'`, `master=0`, `boot=100` — changing them makes the old table stale.
- **Treating ABC acceptance as a point estimate.** Report the accepted count, the tolerances and the priors; the
  posterior is conditional on all three.
- **Forgetting that the JavaScript side cannot import `mc.py`.** Any JS Monte Carlo must follow the same conventions
  by hand (`engine/camchild_record.cjs`); check the seed rule in both places if you change it.
- **Changing a convention in `mc.py` to make one experiment convenient.** The docstring says why not: stored results
  depend on `matched_seeds`, the design order and the childworld draw order.
