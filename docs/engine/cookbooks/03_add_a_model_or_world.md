# 03 · Add a model or world

**Goal.** Take an idea from "we should model this" to a world that runs in the app, is tested in Node and Python,
is wired into `run_all.py`, and is labelled honestly in the facts register.

**Read first.** `engine/mc.py` (recipe 04) if the model needs random draws; `docs/facts_register.md` for what
"built in / emergent / tuned" mean here; `START_HERE.md`'s "What is where" for the current inventory. The two
complete worked examples are the Cambodia child-labour world (`web/camchild.js` + `engine/camchild.py`) and the
cross-country school-and-work model (`engine/childworld.py`). The child-labour intervention simulator
(`web/childlabour.js`, tests only, not yet in the app) is the example of a world that is half-wired.

## Steps

1. **Write the claim and its labels before writing code.** Add the fact rows to `docs/facts_register.md` first:
   every number the model will be scored against is **calibration** (parameters were fitted to it), **test** (it
   played no part in fitting and must have been unseen when the method was fixed), **diagnostic** (context, no
   pass/fail), or **input** (drives the model from outside). Label each mechanism **built in** (follows from how it
   is coded), **emergent** (comes out of interactions the code does not state) or **tuned** (depends on a fitted
   value). A model whose new claim is none of these is a drawing, not a model.

2. **Choose the smallest surface that can be tested.** Preferred: a Python module `engine/<name>.py` with a pure,
   deterministic `simulate(...)` that returns a dict of aggregates, plus tests. If it must also be in the browser,
   a mirror `web/<name>.js` is needed. Examples of the Python shape:
   `engine/childworld.py` — `simulate(th, N=2000, years=8, keep=3, seed=0)`; `engine/camchild.py` — a line-by-line
   twin of `web/camchild.js` ("The browser file is the source of truth for the interface; this file must reproduce
   it draw for draw"). Declare which file is the source of truth in the module docstring, and say what every
   constant is (assumption, calibration, or fitted).

3. **Write the identity tests first.** Every person, unit of money and state must be conserved, and the model must
   be deterministic for a fixed seed. Follow `engine/test_childworld.py` (states sum to 1; same seed, same output;
   richer households send more children to school) and `tests/test_camchild.cjs` ("children conserved in every
   region and year", "deterministic for a fixed seed", "regions add up to the national population"). Run them
   from the right directory: `python -m unittest test_childworld` from `engine/`, or
   `node tests/test_camchild.cjs` from the project root.

   Keep the project's distinction between tier-1 **identity** tests (true by construction — conservation, balance,
   docking with a predecessor) and tier-2 **limiting-case/theorem** tests (a parameter setting where the answer is
   known, as in `tests/test_lab.cjs`'s "perfect flow: CoE 1", `engine/test_mc.py`'s Ishigami indices, and
   `engine/firms/test_tilly.py`). A model whose theorem test cannot be written in closed form is not yet understood.

4. **Test mechanisms by direction, averaged over seeds.** A one-seed direction is a coin toss when the model is
   noisy. `tests/test_camchild.cjs` averages over `SEEDS = [7, 11, 13]`; `tests/test_childlabour.cjs` does the same,
   and its header states what each test is for (luxury axiom, income effect of transfers, ban displacement, money
   conservation). Write the expected direction in the failure message so a future reader knows what broke.

5. **If you mirror it in the browser, build the parity test in the same change.** Two patterns exist:
   - **Draw-for-draw parity, Python twin.** `tests/camchild_parity.py` runs the JS through `node`, dumps every
     yearly aggregate, the child-wage index, spending and every household choice, and compares with
     `engine/camchild.py`: choices identical, numbers to 1e-12. Ten scenarios, around 20 seconds.
   - **Reference-run parity, browser model.** `engine/firms/export_web.py` runs the Python model on three
     reference parameter sets and stores the series in `web/data/atlas_data.js` under `refruns`;
     `tests/js_parity.mjs` runs `web/youth.js` and requires every series within `1e-6` (export values are rounded
     to 1e-10) and the balance within `1e-9`. The rule in `START_HERE.md`: change the model in
     `engine/firms/categorical.py`, mirror it in `web/youth.js`, and `js_parity` fails until they agree — that is
     the point.

   Browser modules are IIFEs that export themselves both ways (see the ends of `web/camchild.js`,
   `web/childlabour.js`): `root.CamChild = api` for the page, `module.exports = api` for the tests.

6. **Wire it into the app only if it belongs in the app.**
   - Add the script file name to the tuple in `build_web.py` — that tuple *is* the app's script list; `index.html`
     is generated. Order matters: data, engines, curated scenarios, pre-run data, UI, then `app.js` last. For
     example, the Cambodia world is `camchild.js`, `camchild_scenarios.js`, `data/camchild_runs.js`,
     `camchild_ui.js` before `app.js`.
   - Add the view in `web/app.js` (see `renderCamChild()` and the `case` that mounts `CamChildUI.mount($('#cc-root'))`)
     or in a separate `<name>_ui.js` added to the tuple before `app.js`.
   - Curated scenarios go in their own file like `web/camchild_scenarios.js` (id, name, policy dict, note).
   - Expensive Monte Carlo bands can be pre-run by a recorder like `engine/camchild_record.cjs`, which
     writes `web/data/camchild_runs.js` (about 90 seconds for 30 seeds) and is then inlined.
   - `web/childlabour.js` shows the incomplete state to avoid: it has 21 passing tests and a `run_all.py` step, but
     it is not in `build_web.py` and not in `web/app.js`, so it is not in the app yet. That is a deliberate state,
     but say so in `START_HERE.md` rather than letting people assume it is shipped.

7. **Add the tests to `run_all.py`.** `run_all.py` is the acceptance gate, and the run report lists every step.
   Follow the existing shape: `step('What is checked', [cmd...])`. Python steps run with `cwd=ENG` by default;
   root-level Python tests pass the full path and `cwd=ROOT`; Node steps live inside the
   `if shutil.which('node'):` block. Put slow refits and large Monte Carlos under `--full`; the default run must
   stay about a minute. If you add a Node test, add it here or CI will not run it.

8. **Export and rebuild.**
   - If the browser page needs fitted parameters or Python reference runs, extend
     `engine/firms/export_web.py` and run `cd engine && python -m firms.export_web` (writes
     `web/data/atlas_data.js`). `run_all.py` does this too.
   - Rebuild: `python build_web.py` (prints `wrote index.html <N> KB`), or just `python run_all.py`.
   - Open `index.html` and walk the new world. Search the built file for the module name to confirm it was inlined.

9. **Label it where people will look.** `docs/facts_register.md` gets the rows from step 1;
   `START_HERE.md`'s "What is where" and "What the numbers can and cannot claim" get a line; `TODO.md` gets the
   remaining work (unverified constants, blocked behaviour, the test that comes next). If an assumption is doing
   real work — e.g. the Cambodia "unexplained boost" of 5.66 in the rural lower-secondary value — say so in the
   module docstring and the register, not only in a commit message.

## Checks

- `python run_all.py` is all pass, and the run report shows your new step.
- The parity test passes (draw-for-draw or within `1e-6`).
- The new test fails when you deliberately reverse a mechanism direction — a test that cannot fail is not a test.
- `index.html` contains the new world; open it and use it as a person would.
- The register lists every number the model is scored against, with a role and a label; nothing scored is new,
  unrecorded and hidden inside a fit.

## Common failures

- **Editing `index.html` directly.** The next build overwrites it. CI also fails when a fresh build changes
  `index.html` or `web/data/` (recipe 01).
- **Forgetting `build_web.py`.** `node tests/<name>.cjs` passes because it requires the file directly, but the app
  has no script; the world simply never appears.
- **Stale `web/data/atlas_data.js`.** Parity compares against it; run `python -m firms.export_web` from `engine/`
  first. Also, `export_web.py` needs `engine/firms/results/china_fit.json`, `tilly_fit.json` and `tilly.json`.
- **Python/JS drift that "looks like" rounding.** The exported values are rounded to 1e-10 and the tolerance is
  1e-6; a difference above that is a logic difference, not rounding. Change both files in the same commit.
- **A noisy one-seed test.** Average the direction over at least three seeds, as `tests/test_camchild.cjs` and
  `tests/test_childlabour.cjs` do; otherwise the suite becomes flaky and people start re-running it.
- **Unseeded randomness.** Any RNG must take an explicit seed; stored results and the parity tests depend on it.
- **Testing a calibration fact as if it were evidence.** The register's rule: a fact moves from test to calibration
  only with a dated entry, and never the other way. A model that matches its own fitting target proves nothing.
- **Putting a 15-minute run in the default suite.** It belongs under `--full`; the quick run is the thing people
  will actually run before committing.
- **Hand-editing recorded data.** Generated recorder output (`web/data/camchild_runs.js`) is a build artifact:
  regenerate it with the recorder, do not edit it.
