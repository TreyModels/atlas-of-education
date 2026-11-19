# Live-site & build audit — Atlas Worlds (post-rename)

**Date:** 19 November 2026, ~20:12–20:40 Asia/Shanghai
**Auditor:** DeepSeek `qa` (fleet teammate), read-only on app code
**Task:** `task-3` — prove the renamed live site works end to end, catch rename regressions
**Live URL:** <https://treymodels.github.io/atlas-of-education/> (repo/Pages slug intentionally stays `atlas-of-education`; brand is **Atlas Worlds**)
**Worktree:** `fleet.nosync/wt-qa` (branch `audit/live-site`, based on final `origin/main`)
**Status:** ✅ **PASS with 1 major brand defect and 1 minor; no blockers**

---

## 1. Verdict

| Area | Result |
|---|---|
| Live routes, 15 × {1280, 390} | **30/30 PASS** — status 200, root rendered, 0 console errors, 0 page errors, 0 px horizontal overflow |
| zh-Hans spot check, 4 × {1280, 390} | **8/8 PASS** — no `undefined`/`NaN`/`[object Object]`, Latin brand preserved |
| Local `npm run build` | **PASS** (exit 0) at both deployed SHAs |
| Relative/static link checks | **64/64 HTTP 200**; 229 unique hrefs inventoried; **71/71 in-page hash anchors resolve** |
| Title + manifest + icons + SW | **PASS** — `Atlas Worlds · Model Lab`, manifest `name`/`short_name` = Atlas Worlds |
| Visible stale old brand | **FAIL on model/workbench pages** — see **D1** (major) |
| Visual review (editorial/Kimi system) | No layout breakage found at 1280 or 390 |

**No blockers.** One major rename defect is prominent but confined to the runnable model pages, which are not among the 15 audited routes; the rest of the rename is clean.

---

## 2. Deployment under test (main was redeployed mid-run)

`main` moved while this audit was running, so the suite was executed twice.

| Phase | main SHA | Pages deploy run | Live assets (`index.html`) |
|---|---|---|---|
| Initial run | `c3cc71c` — Merge PR #14 *rename/atlas-worlds* (2026-11-19 20:01 +08) | `44519968455` success, 12:01:06Z | `assets/index-D7zxQZ-1.js`, `index-CKdqqN6r.css` |
| **Final (authoritative)** | **`01e13e4`** — Merge PR #11 *design/catalogue-stories* (deployer) | **`44522336935` success, 2026-11-19T12:16:21Z (20:16:21 +08)** | **`assets/index-CXOMC1LQ.js`, `index-BT6qzP8y.css`** |

**Proof the live deployment is `01e13e4`:** a clean `npm run build` of `origin/main` at `01e13e4` emits byte-identical asset names — `index-CXOMC1LQ.js` and `index-BT6qzP8y.css` — exactly the files referenced by the live `index.html`. The same comparison at `c3cc71c` matched the pre-redeploy live assets (`index-D7zxQZ-1.js`). PR #11 only adds `src/navigation.css` (`git diff --stat c3cc71c..01e13e4` = 1 file, +828), so it is a styling-only change; the final suite re-ran anyway.

- Final report timestamp: `2026-11-19T12:27:57.807Z` (`qa-report.json`).
- Post-audit live `index.html` still serves the `01e13e4` assets; `origin/main` = `01e13e4`.

---

## 3. Route matrix (final deployment `01e13e4`)

All 15 routes at both widths. `ov` = horizontal overflow (px), `err` = pageerrors/console-errors, `t` = rendered root text length. Every document title ends with the new brand.

| Route | 1280 | 390 | Document title |
|---|---|---|---|
| home | PASS ov=0 t=27712 err=0/0 | PASS ov=0 t=27303 err=0/0 | Atlas Worlds · Model Lab |
| story-angkor | PASS ov=0 t=16880 err=0/0 | PASS ov=0 t=16478 err=0/0 | How food, labour, authority and climate interact · Atlas Worlds |
| story-shadow | PASS ov=0 t=18540 err=0/0 | PASS ov=0 t=18135 err=0/0 | Why do pupils pay their own teachers? · Atlas Worlds |
| story-politics | PASS ov=0 t=13506 err=0/0 | PASS ov=0 t=13093 err=0/0 | Can enforcement change corruption when obligations outlast a campaign? · Atlas Worlds |
| story-extension | PASS ov=0 t=9838 err=0/0 | PASS ov=0 t=9429 err=0/0 | Farmer field schools & food politics · Atlas Worlds |
| story-fertility | PASS ov=0 t=16210 err=0/0 | PASS ov=0 t=15805 err=0/0 | Why fertility fell, and what can still move it · Atlas Worlds |
| story-deephistory | PASS ov=0 t=8159 err=0/0 | PASS ov=0 t=7751 err=0/0 | Coast or herds? How people got from Africa to Australia · Atlas Worlds |
| story-education | PASS ov=0 t=27302 err=0/0 | PASS ov=0 t=26890 err=0/0 | Who stays in school, and what the diploma is worth · Atlas Worlds |
| story-systems | PASS ov=0 t=22176 err=0/0 | PASS ov=0 t=21766 err=0/0 | What happens when a cohort moves through the system · Atlas Worlds |
| story-planning | PASS ov=0 t=10440 err=0/0 | PASS ov=0 t=10025 err=0/0 | The planner's arithmetic, showing its work · Atlas Worlds |
| catalogue | PASS ov=0 t=12995 err=0/0 | PASS ov=0 t=12581 err=0/0 | Atlas of Models · Atlas Worlds |
| about | PASS ov=0 t=4231 err=0/0 | PASS ov=0 t=3822 err=0/0 | Atlas Worlds · Model Lab |
| how-models-work | PASS ov=0 t=4783 err=0/0 | PASS ov=0 t=4374 err=0/0 | Atlas Worlds · Model Lab |
| workflow | PASS ov=0 t=5235 err=0/0 | PASS ov=0 t=4826 err=0/0 | Atlas Worlds · Model Lab |
| angkor-guide | PASS ov=0 t=3310 err=0/0 | PASS ov=0 t=2908 err=0/0 | ANGKOR · A GUIDED RECONSTRUCTION · Atlas Worlds |

Note: `catalogue`'s `<h1>` is **"Atlas of Models"** with the page title `Atlas of Models · Atlas Worlds`. That is the model-atlas catalogue title, **not** the retired brand — intentional.

---

## 4. Build sanity

`npm run build` (`tsc -b && vite build`) — **exit 0**, no type errors:

| SHA | Build time | JS | CSS | Warnings |
|---|---|---|---|---|
| `c3cc71c` | 17.53 s | `index-D7zxQZ-1.js` 6,564.19 kB (gz 1,758.71) | `index-CKdqqN6r.css` 169.26 kB | chunks > 500 kB; `../fonts/*.ttf` "didn't resolve at build time" |
| `01e13e4` | 14.14 s | `index-CXOMC1LQ.js` 6,564.19 kB | `index-BT6qzP8y.css` 183.57 kB | same two warnings |

- The font warnings are **benign**: the emitted CSS keeps `url(../fonts/dm-sans-400.ttf)` etc., and all five fonts return **200** on live (`fonts/dm-sans-400.ttf` sha256 matches local `dist/fonts/`). Do not "fix" by inlining unless intended.
- Large-chunk warning is pre-existing (worker + app bundle), not a rename regression.
- `node_modules` is the shared symlink `../atlas/node_modules`; no install was run.

---

## 5. Link, anchor & static-asset checks (final deployment)

- **64/64** relative links found in the shipped app return **HTTP 200** (followed redirects).
- **71/71** in-page `#` anchors resolve to an existing element (0 dead anchors across all 15 routes).
- 229 unique `href`s inventoried site-wide (incl. external); static assets checked:
  - `research/index.html`, `research/fertility.html`, `research/shadow-education.html`, `research/out-of-africa.html` — 200
  - `research/ccp-bus/ccp-bus-v{1,3,6,7}.zip` — 200 (4.9–6.7 MB)
  - `research/fertility/fertility_research.zip`, `research/fertility/fertility-research-full.zip`, `research/shadow/tutoring_abm.zip`, `research/shadow/credential_floor_dhs.zip`, `research/out-of-africa/coast-or-herds-model.zip`, `research/field-schools/field-schools-models.zip` — 200
  - `research/{provisioning,monsoon,relocation,signalling,angkor-sequence}.html`, `research/provisioning-paper.pdf`, `research/provisioning-periods.csv`, `research/angkor-paired-results.csv` — 200
  - `reference/education/index.html` + all `#world=`/`#tool=` deep links, `reference/angkor/index.html`, `reference/mandala/index.html`, `reference/monte-carlo/index.html`, `reference/east-asia-schools/*` — 200
  - `LICENSE.txt`, `manifest.webmanifest`, `icons/icon-192.png`, `sw.js`, `engines/*.js` — 200
- `CITATION.cff` and `favicon.ico` are **not published** (404) but are **not linked** anywhere in the shipped app — not a defect.
- `manifest.webmanifest`: `{"name":"Atlas Worlds · Model Lab","short_name":"Atlas Worlds", ...}` — correct.
- `<title>` = `Atlas Worlds · Model Lab`; `<meta name="theme-color">` `#ece4d9`; icons present.

---

## 6. Rename / brand audit

| Surface | Expected | Finding |
|---|---|---|
| `<title>` / manifest / og | Atlas Worlds | ✅ correct on all 15 routes + model pages |
| Rail/header brand (desktop + mobile) | Atlas Worlds / Model Lab | ✅ correct |
| Global footer | Atlas Worlds · 2026 | ✅ correct on all routes |
| Homepage footer licence/DOI | no false DOI claim | ✅ "Versioned releases support citation; **DOI details appear when available**" |
| About licence/DOI | no false DOI claim | ✅ "Releases are versioned for citation; **a DOI will be displayed when issued**" |
| Workflow licence/DOI | no false DOI claim | ✅ "…**Zenodo DOI details are displayed when issued**" |
| Reuse terms (footer → `LICENSE.txt`) | Atlas Worlds, formerly Atlas of Education | ✅ `LICENSE.txt:1` says "Atlas Worlds (formerly Atlas of Education)" |
| README / CITATION.cff | Atlas Worlds | ✅ `README.md:1`, `CITATION.cff:3` new title; README notes former name |
| **Model/workbench eyebrow** | Atlas Worlds | ❌ **D1 — old brand, visible** |
| **Model version strings (evidence panel)** | Atlas Worlds | ❌ **D2 — old brand, visible on expand** |
| zh-Hans title + chrome | Latin "Atlas Worlds" preserved | ✅ (titles and rail brand intact) |

No visible `undefined`, `NaN` or `[object Object]` was found on any audited route in either language.

### Intentionally retained old names (not bugs)

Per the task brief, the classic Full Education Atlas and historical archives legitimately keep the old name:

- `public/LICENSE.txt` — "formerly Atlas of Education" (deliberate provenance note).
- `README.md`, `CITATION.cff` — former-name note.
- Footer link **"Full Education Atlas"** → `reference/education/index.html` (classic workbench site, `src/components/Navigation.tsx:110`; label is the classic product's own name).
- `public/reference/education/index.html` (6 hits), `public/reference/angkor/research/BUILD_HISTORY.md`, `public/research/massification/index.html` (archived research page), `docs/**` internal docs.
- Repo/Pages slug `TreyModels/atlas-of-education` and GitHub links to `.../atlas-of-education/blob/...` — deliberately unchanged.

---

## 7. Defects (prioritised)

### D1 — MAJOR: stale brand eyebrow on every model/workbench page
**Where:** `src/components/Workbench.tsx:109`
**String:** `THE ATLAS OF EDUCATION · MODEL LAB`
**Also:** translation key `THE ATLAS OF EDUCATION · MODEL LAB` in `src/data/translations.json:2` (zh-Hans renders it as **"教育地图集 · 模型实验室"**, fr/vi likewise translate the old brand), so the UI is *actively translating a retired brand*.

```tsx
// src/components/Workbench.tsx:109 (world-header)
<p className="eyebrow">{guide ? t(guide[1]) : t('THE ATLAS OF EDUCATION · MODEL LAB')}</p>
```

**Impact:** the red eyebrow sits directly above the `<h1>` on **all 56 runnable model pages** (every `world.id` route, e.g. `#cambodia`, `#china`, `#teachers`, `#angkor`, `#credentials`, `#sector`, `#lays`, `#absorption`, `#schoolmap`, `#cohort`), at both 1280 and 390 px. It is the first brand string a visitor sees when they actually run a model. zh-Hans users see a translated old brand ("教育地图集"), inconsistent with the Latin "Atlas Worlds" brand used in titles and the rail.
**Repro:** open <https://treymodels.github.io/atlas-of-education/#cambodia> → eyebrow reads "THE ATLAS OF EDUCATION · MODEL LAB" (screenshot: `qa/shots/live/workbench-cambodia-1280.png`, `-390.png`, `-zh-1280.png`).
**Likely fix:** rename the key to `THE ATLAS WORLDS · MODEL LAB` (or reuse `Atlas Worlds`/`Model Lab`), update `Workbench.tsx:109`, the `translations.json:2` key and its zh/fr/vi values (zh should keep the Latin brand, e.g. "ATLAS WORLDS · 模型实验室").

### D2 — MINOR: stale "Atlas of Education 0.11.2" model version strings
**Where:** `src/models/worlds.js:31, 112, 158, 544, 588, 640, 679, 719`
**Rendered at:** `src/components/Workbench.tsx:142` (`<p>{world.version}</p>` inside the "EVIDENCE & ASSUMPTIONS" details panel).

**Impact:** expanding "Evidence & assumptions" (`details.evidence-section`, `#method`) on any affected model shows e.g. `Atlas of Education 0.11.2 · Cambodia child world · all policy levers`. Hidden by default; visible on interaction. 8 of 16 worlds carry the old string; the others have no/other version text.
**Repro:** open `#cambodia` → expand "Evidence & assumptions" → screenshot `qa/shots/live/workbench-cambodia-1280-evidence.png`.
**Fix:** update the 8 strings to "Atlas Worlds 0.11.2 · …" (and bump the version if appropriate).
**Note:** this also flows into the exported run JSON (`Workbench.tsx:98`, `modelVersion`) — data files, not just UI text.

### D3 — MINOR: dead translation residue
`src/data/ui-translations.json:1357` still holds `"THE ATLAS OF EDUCATION · COMPLETE MODEL LIBRARY"` with no remaining consumer in `src/**/*.ts(x)` (the classic site uses `public/languages.js`). Harmless today, but it invites the old brand back. Remove or rename alongside D1.

*No blockers were found; all 15 routes, both widths, both languages, the build, and every published link work.*

---

## 8. Visual review (editorial/Kimi design system)

Reviewed screenshots at 1280 and 390, plus full-page and section crops. No layout breakage, no clipped text, no overlap, no horizontal scrollbars.

- **Header/rail brand:** "Atlas Worlds / Model Lab" with the orange rosette mark — correct desktop rail, mobile top bar, and mobile drawer. Sticky rail behaves at 1280.
- **Homepage:** strong editorial hero ("Social science you can run."), three-column story-card grid with status badges (PUBLISHED FOUNDATION / MECHANISM EXPLORATION / TEACHING / DESCRIPTION AND ACCOUNTING / IMPLEMENTATION CHECKED / IN DEVELOPMENT / HISTORICAL RESULT / EMPIRICALLY EVALUATED) and "Read what the models found →" affordances; "9 collections, 56 catalogue entries." section intact. No stale card titles.
- **Catalogue (PR #11 redesign, final SHA):** "RESEARCH CATALOGUE / Atlas of Models" with search field and topic chips; renders cleanly at 1280 and stacks correctly at 390. PR #11 caused no regression.
- **Journey page (`story-angkor`, `story-shadow`, `angkor-guide`):** chapter rail + dropcap/editorial type, badges and "Open step →" rows all correct; angkor-guide guided-reconstruction layout clean.
- **Workflow / About:** long-form article layout, pull quotes and rules correct; footer licence + "How to cite" CTA correct.
- **Mobile 390:** bottom tab bar (Home / Models / Planning / Menu), single-column cards, no overflow on any route; hamburger and language selector visible.
- **zh-Hans:** Chinese UI chrome renders with correct type; Latin brand stays "Atlas Worlds". Long-form story prose remains English under zh-Hans (story-angkor), with UI/chapter chrome partly translated — this is a pre-existing content-translation gap, **not** a rename regression and not in scope of the rename.

---

## 9. Artefacts

All under `fleet.nosync/qa/shots/live/` (not committed to the repo):

- `qa-report.json` — final 30-check report (`generatedAt 2026-11-19T12:27:57Z`)
- `home|story-*|catalogue|about|how-models-work|workflow|angkor-guide-{1280,390}.png` — 30 viewport shots (final SHA)
- `zh/` — 8 zh-Hans shots + `zh/qa-report.json`
- `sections/` — homepage card/collection/footer crops; `full/` — full-page captures
- `workbench-cambodia-{1280,390,zh-1280}.png`, `workbench-cambodia-{1280,390}-evidence.png` — D1/D2 evidence
- `scan-en.json` / `scan-zh.json` — per-route visible text, footers, header/footer anchors, old-brand/undefined counts
- `links.json` — per-route anchors, hash-target resolution, 64 fetched link statuses
- `_scan.mjs`, `_links.mjs`, `_full.mjs`, `_sections.mjs`, `_models.mjs`, `_brand2.mjs` — audit scripts

Reproduce:

```bash
export PATH=/opt/homebrew/bin:$PATH          # Node 26 (default node v16 breaks Vite 7)
node fleet.nosync/qa/qa.mjs https://treymodels.github.io/atlas-of-education/ \
  --routes home,story-angkor,story-shadow,story-politics,story-extension,story-fertility,story-deephistory,story-education,story-systems,story-planning,catalogue,about,how-models-work,workflow,angkor-guide \
  --widths 1280,390 --shots fleet.nosync/qa/shots/live
```

---

## 10. Recommendation

Rename is **good to go public** as-is; the remaining work is a small follow-up patch (no redeploy urgency, but should ship before any post-launch announcement that points at model pages):

1. **D1** — fix `Workbench.tsx:109` + `translations.json:2` key/values (keep Latin "Atlas Worlds" in zh) — highest visual impact.
2. **D2** — replace the 8 `Atlas of Education 0.11.2` strings in `src/models/worlds.js` (they also leak into exported run JSON).
3. **D3** — drop `ui-translations.json:1357` dead key.
4. Optional: consider code-splitting the 6.5 MB app chunk / 5.4 MB worker (pre-existing warning) — performance, not a rename issue.
