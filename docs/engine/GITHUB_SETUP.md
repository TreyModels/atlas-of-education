# Putting the repository on GitHub (to-do item B1)

Status, 6 November 2026: **local repository done; remote push needs Trey's credentials.** This machine has no GitHub
CLI and no stored credential, so the private repository cannot be created or pushed from the run that executed the
to-do list. Everything else for B1 is in place.

## What is already in the tree

- `.gitignore` — excludes `__pycache__/`, `*.pyc`, `.venv/`, `.DS_Store`, `node_modules/`, `RUN_REPORT.md`.
- `.github/workflows/ci.yml` — on every push and pull request: Python 3.12 + Node 22, `pip install -r requirements.txt`,
  `python run_all.py`, then `git diff --exit-code -- index.html web/data` so a stale build fails CI.
- A local git repository initialised on 6 November 2026 with a first commit of the full tree.

## What Trey needs to do (about two minutes)

1. Create the private repository (empty, no README):
   - github.com → New repository → name e.g. `atlas-of-education` → **Private** → Create.
2. From the project folder (`~/atlas` once copied there), connect and push:

   ```bash
   git remote add origin git@github.com:<your-account>/atlas-of-education.git
   git branch -M main
   git push -u origin main
   ```

   If HTTPS is easier: `git remote add origin https://github.com/<your-account>/atlas-of-education.git`
   and push; the credential helper will ask for a personal access token (not the account password).
3. Watch the first Actions run. It is the first real CI run; the local run of `run_all.py` passes (see
   `RUN_REPORT.md`), but the pinned Python 3.12 / Node 22 combination has not been tested on the runner before.
4. If the runner fails on a missing package: `pip install -r requirements.txt` is the only install step; the known
   extra dependency for the download script is `requests`, which is now in `requirements.txt`.

## Notes

- `RUN_REPORT.md` is deliberately gitignored: it records local runs (including the 1–2 hour `--full` refit) and
  should not churn on every push. The stored results under `engine/**/results/` and `web/data/` are the committed
  record.
- The long steps in `run_all.py --full` are not run in CI (30-minute timeout); only the quick suite is. The stored
  results from a local `--full` are committed alongside the code.
- Do not make the repository public before the licence decisions in `LICENSES.md` are settled: eight of the twelve
  bundled public-data CSVs are boundary cases, and the licence draft recommends a data split before any public push.
