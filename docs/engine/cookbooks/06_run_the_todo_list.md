# 06 · Run the to-do list

**Goal.** Work `docs/TODO_BY_LANE.md` (the lane-sorted version of `TODO.md`) without collisions, and package the
finished run so the next person can verify it. This is the operating recipe for a whole session, not one command.

**The three lanes.** This is the project's own division, from `docs/TODO_BY_LANE.md`:

- **Lane A — Claude (cloud, phone).** Writing, reading, web lookups. No heavy compute. This is where input
  verification, CV, licence table, chapter map, method outline and the "how I verified this" note live.
- **Lane B — MacBook.** Anything that runs code, downloads data or refits models. The prompts are written for a
  local model (DeepSeek) or for a person at the terminal.
- **Lane C — Trey only.** Decisions, money, people: domain, licence, GitHub repo, Bjørn session, journal choice,
  Cambodia microdata.

Effort labels are the project's: **XS** under 15 min, **S** under 1 hr, **M** an afternoon, **L** several sessions.

## Before you start

1. Put the folder somewhere stable (the plan uses `~/atlas`) and check the toolchain: Python 3.10+ and Node.
   Recipe 01.
2. **B2 — baseline run.** `pip install -r requirements.txt` then `python run_all.py`. If `RUN_REPORT.md` is not all
   `pass`, stop and repair the tree before doing anything else. A broken baseline makes every later result
   unattributable.
3. Read `docs/facts_register.md` so you know which numbers are calibration and which are tests. Read the current
   `RUN_REPORT.md` headline section so you can spot a number that moves.

## Order of operations

The "easiest high-value path" in `docs/TODO_BY_LANE.md` is still right:

1. **A1 → B3.** Verify the `m` inputs (recipe 02), then apply the corrections in one batch and re-run.
2. **A2** (CV) in parallel: it is Lane A and does not touch the model.
3. **C1, C2, C4** — five minutes each, but they are Trey's; ask early.
4. **B4 → B5.** The WDI/UIS download is now scripted (`analysis/public_data/download_public_data.py`, data already
   in `analysis/public_data/data/` as of 6 November 2026); B5 is the credential-flood regression with the
   wage-employment share.
5. **A5 → C3.** Chapter map, then the Bjørn session.

Two ordering rules bite:

- **B8 (the full refit) only after B3.** `python run_all.py --full` takes 1–2 hours and rewrites the stored results;
  running it before the input corrections means doing it twice.
- **The quick run does not refit.** Editing `engine/firms/data_china.py` changes inputs, but the stored headline
  numbers in `RUN_REPORT.md` move only when a fitting script or `--full` runs. Recipe 02 step 9.

## Moving the run forward (state at 6 November 2026)

This is what the working tree now shows, so a session does not redo it:

- A1: `docs/china_input_verification.md` exists (344 lines), and `engine/firms/data_china.py` carries the applied
  change set (`_URB_CHECKED`, `GRAD_FLAG`/`TERTIARY_FLAG` all `v`, `BIRTHS_FLAG` all `d`). `tests/test_evidence.py`
  guards it.
- B4: `analysis/public_data/data/SOURCES.txt` records eight WDI indicator CSVs and the UIS SDG-4 extract,
  retrieved 6 November 2026 with row counts.
- B6/B7: `tests/test_round8.py` (14 tests) and `tests/test_childlabour.cjs` (21 tests) are in `run_all.py`.
- The imputation module exists in `engine/impute/`; the B11 hold-out report is `python -m engine.impute` from the
  project root (see below).
- The quick run is all pass; the long `--full` rerun (B8) is a separate job. Do not start a second one, and record
  its state (running / finished / not started) in the session note.

Still genuinely blocked or waiting: the GitHub repository push, the licence decision and Kimi's interface terms
(Trey); Bjørn's chapter map/"schools as protection" session and the Nordtveit protection magnitudes (people); the
sector-demand series for China (needs a sourced NBS series — do not enter one from memory); scoring the blind
forecast (waiting on the NBS releases for October 2026 onwards); Cambodia microdata (NIS request).

## Splitting work across agents without collisions

The rule is disjoint write scopes. Everything below is about one shared folder.

1. **One owner per file.** Two sessions editing `run_all.py`, `TODO.md` or `engine/firms/data_china.py` in the same
   hour will produce a hand merge. Write down each agent's files before it starts; a shared task with an advisory
   write scope is enough.
2. **Separate code from docs.** A doc lane writes `docs/**`; a code lane writes `engine/**` and `tests/**`. Cookbooks
   and notes do not need the model to be stable; the model does not need the prose to be finished. This is how
   `docs/china_input_verification.md` (audit only, no code edited) fed a separate code lane.
3. **Generated files are single-writer by nature.** `index.html`, `web/data/atlas_data.js`,
   `web/data/camchild_runs.js` and `RUN_REPORT.md` are outputs of `python run_all.py` / `python build_web.py` /
   `node engine/camchild_record.cjs`. Two concurrent `run_all.py` runs in one tree will overwrite each other; so will
   two `build_web.py` runs. Let one lane own the build, or give each lane its own copy.
4. **One long job at a time.** `python run_all.py --full` is CPU-heavy (1–2 hours, several steps say "on 2 cores").
   Do not start it while another lane is fitting or running the quick suite; the timings and the machine both
   suffer.
5. **Serialise the two shared files.** If two lanes must both touch `run_all.py` or `TODO.md`, do it last, one at a
   time. The evidence lane's note says it exactly: "merge by hand: my edits are one inserted line in the default
   steps, one in the `--full` steps, and the two TODO paragraphs named above."
6. **Experiments in copies.** If you are testing a model change that is not committed, copy the folder and run
   there. The deliverable tree's `index.html` and results stay honest.
7. **A blocked job is a report, not a retry.** If a download is WAF-blocked or an approval is needed, record the
   URL, the status and the date (recipe 02 step 10), report it to the owner, and move on. Do not route around a
   denial or invent the value.

## Running the B11 imputation hold-out

The module is `engine/impute/`; the report is stdout by default and takes a couple of seconds:

```bash
python -m engine.impute                                  # all five datasets, 3 replicates, seed 0
python -m engine.impute --datasets pwt --replicates 1    # quick check
python -m engine.impute --out docs/imputation_validation.md
```

It deletes blocks of verified (`v`) cells from the packaged public data (PWT GDP, Lee-Lee/Barro-Lee attainment,
the five-year Barro-Lee waves), refits every rung of the ladder on the damaged panel, and scores MAE/RMSE/bias by
method and gap length. It writes no file unless `--out` is given; the docs file is the Lead's to add. Do not score
against `d` cells: the harness scores only verified cells by design.

## Verify the run

Do these in order when the work is done. The first four are the acceptance gate; the last two are the honesty
check.

1. **Quick suite all pass.** `python run_all.py` → exit code 0, every step `pass`, fresh `RUN_REPORT.md`. If the
   input batch changed, the full refit has also been run (`--full`) and the quick suite re-run afterwards.
2. **Rebuilt artifacts are current.** `python build_web.py`; then check the build did not change the tracked output:
   `git diff --exit-code -- index.html web/data` in a git checkout (this is the CI rule, recipe 01), or compare
   hashes of `index.html` and `web/data/*` before and after a rebuild in a plain zip copy. The build is
   deterministic given the same inputs.
3. **Clean-copy run.** Copy the folder to a temp directory (exclude `.venv`, `__pycache__`, `.DS_Store`), make a
   fresh virtual environment, `pip install -r requirements.txt`, and `python run_all.py` there. This is what CI does
   on a fresh checkout; it proves the package is self-contained and that nothing depended on a stale artifact in
   your working copy.
4. **Open the app.** From the clean copy, open `index.html`; choose a world, move a lever, confirm it renders and
   runs with no console errors. The app must need no server and no account; the only network use is the optional
   Google Fonts stylesheet, and the page falls back to system fonts without it.
5. **Check the record, not just the colour.** `RUN_REPORT.md` all pass means the tests and stored artifacts agree.
   It does not mean the assumptions are true: the report's headline section labels fit statistics versus tests, and
   `docs/facts_register.md` is the standing record. Check that anything new has a role and a label, that no `m`
   flag remains in the China inputs (`python tests/test_evidence.py` enforces this), and that known failures are
   still listed (the "Known failures to keep visible" section of `TODO.md`).
6. **Say what was not verified.** The final session note — and the delivery message — should name the unfinished
   items: the `--full` numbers if the refit has not finished, the blind forecast (waiting on the NBS release), the
   blocked Lane C items. An honest package says so; a silent one gets found out later.

## Package the deliverable

No packaging script is provided in the project root: the deliverable is the project folder, zipped. Include the
whole tree —
`index.html`, `web/`, `engine/`, `tests/`, `analysis/`, `planning/`, `docs/`, `related/`, `worlds/`,
`RUN_REPORT.md`, `START_HERE.md`, `TODO.md`, `requirements.txt`, `build_web.py`, `run_all.py`, `.github/`. Include
`RUN_REPORT.md` even though `.gitignore` lists it: it is evidence, and `START_HERE.md` asks the reader to summarise
it. Do not include `.venv/`, `__pycache__/`, `.DS_Store`, editor backups or the raw UIS archive (the curated extract
in `analysis/public_data/data/uis/` is the useful file; the download script deletes the archive).

A straight zip from the parent directory, with the exclusions above:

```bash
cd ..
zip -r atlas_of_education_<date>.zip atlas \
  -x 'atlas/.venv/*' -x '*__pycache__*' -x '*.DS_Store' -x 'atlas/.git/*'
```

Then **verify the zip itself**, because that is the artifact people will open: unzip it into a clean directory and
repeat "Verify the run" steps 1–4 there. A zip that passes only in the folder it was built from has not been
verified.

The delivery message should state: the zip name; the fact that `RUN_REPORT.md` is all pass and which run it is
(quick or `--full`); the headline results with the fit/test distinction; what is in `docs/cookbooks/`; and the
unfinished or blocked items from check 6.
