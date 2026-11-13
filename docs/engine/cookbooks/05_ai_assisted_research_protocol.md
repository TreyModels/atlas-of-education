# 05 · AI-assisted research protocol

**Goal.** Brief an AI agent so that its output can be checked in minutes by someone who did not watch it work. The
rules are cheap; the alternative — trusting a fluent report — is what this project cannot afford.

**The five rules behind the templates.**

1. **One job per session.** One file, one test, one download. Agents that are given three jobs drift, and then
   nobody can tell which edit came from which instruction.
2. **Exact paths, and a write scope.** Say which files may change and which are read-only. "Improve the tests" is
   not a job; "edit `tests/test_round8.py`, do not touch `run_all.py`" is.
3. **No invented numbers, file names or citations.** Every number the agent states must be either read from a
   named file in the tree or fetched from a URL it can show. If it could not fetch the page, it must say so and
   leave the value flagged (`m` in `engine/firms/data_china.py`, or unverified in its report). Recipe 02 is the
   human version of this rule.
4. **Independent re-derivation.** For anything that matters, require a second route: a second data source that
   agrees, a second implementation (Python twin versus browser), or a clean-copy rerun. The China audit's
   two-transcription rule and the Cambodia Python twin are the worked examples.
5. **A diff review and an acceptance test.** The agent reports what it changed and what it ran; the human reads
   the diff and runs the acceptance command. If the acceptance test is not stated, the job is not defined.

## The session brief (paste and fill in)

```
You are working in the Atlas of Education project folder: <absolute path>.
Read START_HERE.md first, then docs/facts_register.md and docs/cookbooks/README.md.

Job (one only): <one sentence, with the exact outcome>.
Files you may change: <exact paths or "none — read only">.
Files you must not change: index.html, web/data/*, RUN_REPORT.md (generated); <anything else>.
Acceptance command: <exact command, e.g. python run_all.py, or node tests/js_parity.mjs>.
Environment: use the project virtual environment (<path>); Node at <path>.

Rules:
- Do not invent file names, commands, citations or numbers. Every number you report must come from a file you read
  or a page you fetched, and you must give the path or URL.
- If a fetch fails, record the URL, the HTTP status and the date, and mark the value unverified. Do not fill it in.
- Do not edit tests to make them pass, and do not edit generated files.
- Do not start any long refit (python run_all.py --full) unless the job says to.

Report when done, in this order:
1. What changed, file by file (one line each).
2. The acceptance command and its full tail output.
3. Numbers that moved, old -> new, with where each came from.
4. What you could not verify or complete, and why.
5. Anything you noticed that is wrong but outside this job (do not fix it).
```

## Ready-made prompts for the Lane B items

These are the bounded versions of the prompts in `docs/TODO_BY_LANE.md`. Two of the items are now done in the tree
(B6 and B7); their prompts are written so they can be used to verify or restore the work rather than redo it.
Do not run two of these in the same folder at once, and do not combine one with an edit to `run_all.py` by someone
else — see recipe 06 for the parallel-work rules.

### B2 — baseline run (read-only)

```
You are in the Atlas of Education project folder ~/atlas (a Python + Node research project).
Do not edit any file. Do this and report only what you saw:
1. Activate the project virtual environment. Run: pip install -r requirements.txt
2. Run: python run_all.py
3. Open RUN_REPORT.md. List every step whose Result is not "pass", with its last lines.
4. Report the Python version, the Node version (or "no node"), and the command's exit code.
If a command fails, quote the error and stop; do not try fixes.
```

Acceptance: a `RUN_REPORT.md` with every step `pass`, and a reported exit code 0. On 6 November 2026 this was 19
steps, roughly a minute or two of step time.

### B4 — public-data download (World Bank WDI, UNESCO UIS)

The download script now exists; the job is to run it, check the files and record provenance, not to rewrite it.

```
You are in the Atlas of Education project folder ~/atlas.
Job: refresh or verify the public-data download in analysis/public_data/data/.
1. If "requests" is missing, run: pip install requests
2. Run: python analysis/public_data/download_public_data.py
3. Report: the row counts it prints for each WDI indicator and the UIS extract, and the full contents of
   analysis/public_data/data/SOURCES.txt.
4. Check that each CSV in analysis/public_data/data/wdi/ has the header country_iso3,country,year,value and at
   least 1000 data rows; report any file that does not.
5. Run python tests/test_evidence.py and report the result.
Do not modify the download script, any existing OWID CSV, or any file outside analysis/public_data/data/.
Acceptance: data/SOURCES.txt lists every URL with a retrieval date; all eight WDI CSVs parse; the test suite passes.
```

Do not "correct" the data in the script: if an indicator or a URL 404s, record it and stop. The UIS archive is
large (the script keeps a curated SDG-4 national extract and deletes the raw archive); let it run.

### B6 — round-8 results as permanent tests

`tests/test_round8.py` exists (14 tests) and runs in `run_all.py`. The prompt below is the original write job; the
first variant is the one to use now.

```
Verify variant:
You are in the Atlas of Education project folder ~/atlas.
Job: check that tests/test_round8.py still guards the round-8 conclusions; change nothing unless a test is wrong.
1. Read related/massification_project/results/round8_mechanisms_and_ledger_fix/floor_test/findings.txt and
   .../grad_supply/findings.txt.
2. Read tests/test_round8.py and list, for each findings.txt claim, the test that asserts it and whether it is
   checked on the stored full-size results, the reduced rerun, or both.
3. Run: python tests/test_round8.py   (about 30-60 seconds)
4. Run: python run_all.py and report that the round-8 step passes.
Report the claim-to-test mapping and the exact commands' output tails. Do not change any test to make it pass.
Acceptance: every surviving conclusion has a named test and both commands pass.

Write variant (if the test file is missing):
... same preamble ...
1. Read .../floor_test/findings.txt and .../grad_supply/findings.txt, and the stored CSVs next to them.
2. Write tests/test_round8.py with two unittest tests that re-run those experiments at a small size
   (related/massification_project/code/massabm; do not change that code) and assert the direction of each
   finding stated in findings.txt, not exact numbers.
3. Add it to run_all.py the same way the other Python tests are added (one step).
4. Run python tests/test_round8.py then python run_all.py; report both.
Acceptance: the tests fail if a conclusion is reversed, and pass on the current tree.
```

### B7 — child-labour simulator tests

`web/childlabour.js` and `tests/test_childlabour.cjs` exist (21 tests) and the test is in `run_all.py`. The job now
is to verify the required mechanisms are actually tested, not merely asserted in the report.

```
You are in the Atlas of Education project folder ~/atlas.
Job: verify, and if necessary extend, tests/test_childlabour.cjs against web/childlabour.js; do not weaken it.
Required checks, each with its name in the test output:
1. identities: every child in exactly one state each year; population fixed; deterministic for a seed.
2. luxury axiom: child labour falls when household income rises, rises when it falls.
3. transfers: an unconditional transfer lowers child labour, a larger one lowers it more, attendance rises.
4. a partial ban: no enforcement changes nothing; more inspected jobs lower child labour more; some work is
   displaced into unenforced forms.
5. money conservation: spending = amount x eligible children x years for the one exact lever.
Run: node tests/test_childlabour.cjs
Then: python run_all.py and confirm the child-labour step passes.
Report which of the five checks exist, which are missing, and the exact test output. If you add a check, change
only tests/test_childlabour.cjs and web/childlabour.js if the lever needs exposing; report both.
Acceptance: 21+ tests pass and run_all.py's child-labour step passes.
```

## Reviewing the result

- **Read the diff, not the report.** `git diff` if the folder is a repository; otherwise ask for a file–by–file
  description and open the changed files. An agent's summary is a claim, not evidence.
- **Run the acceptance command yourself.** A reported pass that you did not see is not a pass. For evidence jobs,
  open at least one cited URL and re-read the sentence that contains the number.
- **Compare the headline numbers.** `RUN_REPORT.md`'s "Headline results (stored)" should change only when a fit was
  re-run, and then only in ways the job explains. Recipe 02 step 9 covers the before/after record.
- **Check the labels.** New numbers need a role in `docs/facts_register.md`; new mechanisms need
  built-in/emergent/tuned; a value that was `m` must not quietly become `v` without a URL.
- **Look for the failure it did not mention.** Unverified values, skipped tests, a tolerance widened, a test
  deleted, `index.html` edited by hand. The report's "what I could not verify" section is the most informative
  part; if it is empty, be suspicious.
- **Write the A9 note.** The project owes reviewers a one-page "how I verified the AI-assisted work": what was
  checked, by which test, and what was not. `docs/CHANGES_evidence_lane_2026_11_05.md` is a good model of the
  shape — files changed, checks run, values verified with sources, unresolved discrepancies.

## Common failures in AI-assisted sessions

- **"Done" without a run.** The agent read the code and concluded it would work. Demand the command and its output.
- **Editing generated files.** `index.html`, `web/data/atlas_data.js`, `web/data/camchild_runs.js` and
  `RUN_REPORT.md` are outputs; only the build regenerates them. See recipes 01 and 03.
- **Fixing the test instead of the code.** Weaker assertions make the suite green and the project wrong. The
  acceptance command must be one that can fail.
- **Invented sources.** A plausible-looking URL that 404s, or a quote that is not on the page. This is the exact
  reason the China audit records HTTP statuses and quotes; make it the house rule.
- **Silent number changes.** A fitted result drifting by a decimal without explanation destroys the audit trail.
  Compare the stored results before and after.
- **Colliding agents.** Two sessions editing `run_all.py` or `TODO.md` in the same hour produce a hand merge. Give
  each agent a disjoint write scope (recipe 06); one inserted line is cheap, a merge conflict is not.
- **Long jobs started without saying so.** `python run_all.py --full` is 1–2 hours and rewrites stored results;
  only start it deliberately, and tell the next person.
