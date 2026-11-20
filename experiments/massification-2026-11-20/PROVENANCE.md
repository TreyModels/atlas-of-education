# Provenance, environment, and delivery policy

Prepared by the Lead (`lead`), DeepSeek research fleet, 20 November 2026, Asia/Shanghai.
This file records where every artifact came from. It is filled further as agents report.

## 1. Handoff package

- Source ZIP: `/Users/treymenefee/Downloads/DeepSeek_Massification_Research_Package.zip`
  (99,932 bytes; mtime 2026-11-20 12:05 local).
- Extracted copy: `00_handoff/` (11 files incl. `MANIFEST.sha256`).
- Contents: `README.md`; `instructions/01_directive.md` .. `05_literature_data.md`;
  `papers/01_june_bjorn.txt` (June single-author draft) and
  `papers/02_october_massification.md` (October co-authored draft, 377 lines);
  `context/06_conversation.md`; `templates/07_report_templates.md`.
- `00_handoff/MANIFEST.sha256` is the package's own integrity list; verify with
  `cd 00_handoff && shasum -a 256 -c MANIFEST.sha256`.

## 2. Atlas repository

- GitHub remote: `https://github.com/TreyModels/atlas-of-education`
  (also called Atlas Worlds; formerly Atlas of Education).
- `gh auth status`: logged in as `TreyModels`, scopes `gist, read:org, repo, workflow`.
- Audited public main: `origin/main` = `55732f4728a13adb3aec5173d8bc7f3a4ac7f926`
  (matches the commit named in `00_handoff/README.md`).
- Clean read-only checkout used for this program:
  `01_sources/atlas-main-55732f4/` — a linked git worktree at that commit, detached HEAD,
  created with `git -C fleet.nosync/atlas worktree add --detach … 55732f4`.
  `git status --porcelain` empty at checkout; 1,108 tracked files. Never edited.
- The user's live working tree (`fleet.nosync/atlas`, branch `fix/doi-brand`,
  HEAD `01e13e4`) has uncommitted user changes (`CITATION.cff`,
  `src/components/Workbench.tsx`, `src/data/translations.json`,
  `src/data/ui-translations.json`, untracked `fleet-out/`). **These were not touched.**

### Site-safety check for the experimental push
`package.json` build script is `tsc -b && vite build`; `vite.config.ts` builds from
`src/` and copies only `public/` (`publicDir: false`, custom `verify-public-assets`
plugin reading `resolve(__dirname, 'public')`). `.gitignore` excludes `node_modules/`,
`dist/`, `research/runs/`, `__pycache__/`.
→ Adding a directory under `experiments/` and pushing it on a **non-main** branch cannot
change the Atlas page. Policy adopted: results go to
`experiments/massification-2026-11-20/` on branch `experiment/massification-2026-11-20`,
never to `main`, `src/`, or `public/`.

## 3. Massification models (the paper's code)

- Local source: `work/atlas/related/massification_project` (DeepSeek workspace),
  a checkout of Atlas at git HEAD `02cade9` ("Atlas of Education v0.12: 6 Nov 2026 to-do run").
  This is the source the prior November audit recorded as *absent* from the public checkout;
  it exists locally. Copied read-only to `01_sources/massification_project/`.
- SHA-256 of copied files (all four confirmed in `01_sources/`):
  - `code/massabm/massabm/model.py` = `2b6484e7a98866f8362a216b118cf8abbfefc7236b9278d2ec0ac47d6eafeb40`
  - `code/massabm/run.py` = `f2e23a62bd78919c229bf24530a25a34b8562aa9d161cc5d240663e396565ddd`
  - `code/triad/triad/model.py` = `7b22d93cab66f8c4af08f3131800f8dc5489f5f9041cd66dc5b327053314ccea`
  - `paper/Massification_and_Its_Mechanisms.md` = `1138d453a79243f573b57f971369a61f598aecc6f4882f7ff052fd1ea90228cf`
  These hashes match the file list recorded by the 16 Nov docking run for `massabm`
  (`run.py`, `model.py`), i.e. the same source generation.
- Stored historical outputs: `01_sources/massification_project/results/round1…round8`.
  These are the numbers the October manuscript reports (Lead spot-check below).

## 4. Compute environment actually used

| Item | Value |
|---|---|
| OS / hardware | macOS (Darwin), Apple silicon arm64, 8 cores, 8 GB RAM |
| Python | 3.11.17 (`/opt/homebrew/bin/python3.11`) |
| venv (local disk) | `/Users/treymenefee/Library/Application Support/dsh-massification/venv` |
| numpy / scipy / pandas / matplotlib | 2.4.6 / 1.17.1 / 3.1.1 / 3.11.2 |
| CWD / delivery root | `…/Downloads/DeepSeek/massification_2026-11-20` |

Note: the iCloud copy of the 16 Nov venv was evicted and slow to import, so a fresh local
venv was built at the path above. `PYTHONDONTWRITEBYTECODE=1` is used for all runs against
`01_sources/` to avoid writing bytecode into read-only sources.

Lead smoke test (independent of `repo-auditor`), 2026-11-20:
`cd 01_sources/massification_project/code/massabm && python run.py smoke`
→ `ok in 3.5s; reform year 2013`, calibration table produced (e.g. basic completion
entry 1990-95 = 0.743 vs target 0.55-0.62; tutoring rate at board exam 2010 = 0.921;
tutoring rate at basic gate = 0.069; degree share entry 1990-95 = 0.196).

## 5. Lead spot-check: stored findings vs October manuscript

| Manuscript claim (Oct) | Stored `results/` value | Match |
|---|---|---|
| 6-arm diplomas 0.731/0.771/0.771/0.772/0.770/0.772 | round8 `floor_test` 0.731/0.771/0.771/0.772/0.770/0.772 | yes |
| Slopes +0.15/+0.04/+0.63/−0.04/−0.06/−0.05 | round8 `floor_test` +0.151/+0.036/+0.630/−0.044/−0.064/−0.048 | yes (rounding) |
| Grad shock Δ dip income −0.06 / −0.04; formal|dip −0.16 / −0.17 | round8 `grad_supply` −0.061/−0.042; −0.156/−0.169 | yes |
| Actor cost 3.5 / 1.5 / 1.2 of 4.3 years | round2b `necessity` 3.45 / 1.49 / 1.19 of 4.29 | yes |
| Tutoring share 93/30/5/35% | round1 `gates` 0.93/0.30/0.05/0.35 | yes |
| Basic bar 3%→76% | round1 `gates` −2.0: 0.03 … +0.0: 0.76 | yes |
| Nurse 0.25 per migrant vs ~9 | round4 `nurse_check` 0.25 | yes |

Conclusion so far: the October manuscript's reported numbers are in the stored run outputs;
whether they *execute today* is what `repo-auditor` tests. Do not call stored output a rerun.

## 6. GitHub delivery (per user instruction)

User authorised: push experimental results into an experimental folder on GitHub, provided it
does not touch the main Atlas page in any way. Therefore:
- branch: `experiment/massification-2026-11-20` (never `main`);
- path: `experiments/massification-2026-11-20/`;
- no edits under `src/`, `public/`, `index.html`, `package.json`, `vite.config.ts`;
- push only after the Lead has verified the package and the site-safety diff.
