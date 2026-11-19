# Polish & zh-Hans gap sweep — Atlas Worlds

**Date:** 19 November 2026, ~20:40–21:00 Asia/Shanghai
**Auditor:** DeepSeek `qa` (read-only; no app edits)
**Task:** `task-7` — "look for broken things and missing Chinese or polishing or anything"
**Base tested:** **`release/final` merged → `main` `270d705`** (PR #16, "Merge pull request #16 from TreyModels/release/final", 20:40:13 +08)
**Live deploy verified:** Pages run `44526033342` **success** (2026-11-19T12:40:16Z, 53 s) — live `index.html` serves `assets/index-4d6oYOIu.js` + `index-D2Yxk1Mb.css`, **byte-identical to a clean local `npm run build` of `270d705`**. Local `npm run build` exit 0 (24.75 s).

> Includes DOI wiring (10.5281/zenodo.24369167), PR #13 grouped nav, PR #15 coverage, workbench wordmark fix.
> **Verdict: NO broken/blank/dead routes, no visual breakage, no console errors. 3 must-fix copy/zh items + 1 verified class of missing-Chinese chrome (likely PR #20 scope).**

---

## 1. Coverage & method

- **19 routes × 2 widths (1280/390) × 2 languages (en, zh-Hans) = 76 page loads** at 1280/390 on the final build (`vite preview` of `270d705`), plus **24 live re-check loads** on the deployed site after the final Pages deploy (home, catalogue, story-angkor, workflow, about, #cambodia).
- Routes: `home`; 9 `story-*` journeys; `catalogue`, `about`, `how-models-work`, `workflow`, `angkor-guide`; workbenches `#cambodia #angkor #monsoon #sector`. (Note: `#petri`/`#fertility` are not world ids in the final build — `#petri` is a research page; the 15 world ids are cambodia, china, teachers, angkor, mandala, credentials, campaign, signalling, obligations, monsoon, cohort, sector, schoolmap, lays, absorption.)
- **zh DOM gap scan** (`?lang=zh-Hans`): visible text-node walk + attribute walk, classified by ancestor (nav/button/label/heading/badge/footer = UI chrome vs `p/li/article/journey-*` = prose). Raw JSON: `zh-scan-local2.json`; live parity confirmed (`zh-scan-live.json` — identical ui/prose counts for every re-checked route).
- **Polish checks:** broken images (`naturalWidth===0`), document/table overflow, clipped text, empty sections, console warnings/errors, per-route title + meta description, OG/social meta, doubled spaces, stray old brand, `undefined`/`NaN`.
- **Live parity:** every re-checked zh route returned **exactly the same ui/prose/broken/overflow/warn counts** locally and on the live site → the deployed bundle is what was audited.

## 2. Broken / blank / visual — none found

| Check | Result |
|---|---|
| HTTP/blank routes | 19/19 routes 200, non-empty app render, both widths, both langs |
| Broken images | **0** |
| Console warnings / errors / page errors | **0** across all 76 loads |
| Horizontal document overflow | **0 px** everywhere |
| Clipped/overlapping text | none real — only `sr-only` (visually hidden by design) and intentional `.table-scroll` horizontal scrollers |
| Empty sections / table overflow / doubled spaces / `undefined` | **0** |
| 404 behaviour | unknown path = Pages 404 (correct); unknown hash route falls back to Library (correct) |
| Visual: home / catalogue / journey (`story-angkor`) / workflow, 1280 + 390 | clean; grouped rail (PR #13) renders correctly; catalogue 390 stacks correctly; no sticky-nav/drawer collisions |
| Rename fixes | workbench wordmark now `ATLAS WORLDS · MODEL LAB` / `ATLAS WORLDS · 模型实验室` ✅; titles, manifest, footer, DOI copy consistent (no stale "when issued" wording) |

**Screenshots:** `qa/shots/polish/{en,zh}-shots-local/{route}-{width}.png` (76), `{en,zh}-shots-live/` (24), plus committed key shots in `docs/audit/polish/screens/`.

## 3. MUST-FIX — verified, not covered by PR #18 (workflow) or PR #20 (chrome/badges/claims)

### M1. Home CTA section heading is untranslated in zh-Hans (mixed-language block)
- **Route/viewport:** `/?lang=zh-Hans`, home, **1280 and 390**.
- **Symptom:** `h2#home-cta-title` renders **"Think a model is missing something? Change it."** in English, while the paragraph and buttons directly under it are Chinese. First untranslated heading on the zh home page.
- **Source:** `src/data/site-status.ts:27` — `title: 'Think a model is missing something? Change it.'` (string rendered untranslated).
- **Fix:** translate that title (`缺少某个模型？来改它。`) and/or wrap in `t()` with a `translations.json` entry.
- **Screenshot:** `docs/audit/polish/screens/zh-home-cta-1280.png` / `zh-home-390.png` (full page), `qa/shots/polish/zh-shots-local/home-1280.png`.

### M2. Workbench playback axis label "Year" not translated (English inside Chinese playback bar)
- **Route/viewport:** `?lang=zh-Hans#angkor`, `#monsoon`, `#sector` (any world whose chart x-axis has no `xTitle`), 1280 + 390.
- **Symptom:** after a run completes, the playback readout shows `Year: 1450` / `Year: …` amid Chinese UI (`年份` expected).
- **Source:** `src/components/Workbench.tsx:63` — `const playbackAxis = view.xTitle ?? (… ? 'Year' : …)`; the literal is **not passed through `t()`**, so it can never be translated. Rendered at `Workbench.tsx` playback readout (`<strong>{t(playbackAxis)}…`).
- **Fix:** `t('Year')` for the fallback + add `"Year": {"zh-Hans":"年份", "fr":"Année", "vi":"Năm"}` to `translations.json`.
- **Screenshot:** `docs/audit/polish/screens/zh-workbench-angkor-390.png`.

### M3. Stale brand still visible in model "Evidence & assumptions" (carried over from task-3 D2, still not fixed in final bundle)
- **Route/viewport:** any model page, e.g. `#cambodia`, then expand **"Evidence & assumptions"**, 1280 + 390 (and in zh-Hans too).
- **Symptom:** panel shows `Atlas of Education 0.11.2 · Cambodia child world · all policy levers` (old brand, 8 model pages).
- **Source:** `src/models/worlds.js:31,112,158,544,588,640,679,719` (`version:` strings, "Atlas of Education 0.11.2 · …"), rendered at `src/components/Workbench.tsx:142`; also exported in run JSON (`Workbench.tsx:98`, `modelVersion`).
- **Fix:** replace with `Atlas Worlds 0.11.2 · …`.
- **Screenshot:** `qa/shots/polish/…` / earlier `qa/shots/live/workbench-cambodia-1280-evidence.png`.

## 4. Verified missing-Chinese UI chrome (hand to PR #20 — do not duplicate)

DOM scan proof (zh-Hans, visible, UI-classified): **8 badge labels + 8 badge tooltips** render English on model cards/journeys:
`In development`, `Implementation checked`, `Empirically evaluated`, `Historical result`, `Mechanism exploration`, `Teaching`, `Description and accounting`, `Published foundation`; tooltips e.g. `"Asks what follows if these rules held. Not a reconstruction of what happened."`
Also in journey pages (English-only journey content, category 2/3): `Open workbench`, `How the maths works`, `How the model works`, `Still unsettled`, `Deeper experiments`, `Download and adapt`, `Chapters` (aria-label).
**These are all chrome/claims → assume PR #20 covers them; if PR #20 is limited in scope, the badge labels + tooltips are must-fix** (they appear on the home page and every card).

## 5. Top 5 nice-to-haves

1. **No OG/Twitter meta at all** (`og:title`, `og:description`, `og:image`, `twitter:card` all absent) — link previews are blank. Add to `index.html`/build.
2. **One static meta description for every route** — catalogue/journey/workbench pages all share the homepage description; generate per-route description from the page title.
3. **DOI is plain text, not a link** on footer/about/workflow (`10.5281/zenodo.24369167`); make it `https://doi.org/10.5281/zenodo.24369167`. (CITATION.cff is correct.)
4. **Journey prose remains fully English under zh-Hans** (9 stories; e.g. story-angkor ≈262 English text nodes/route) — either add a visible one-line disclosure on story pages in zh mode, or translate incrementally. The `/workflow` article is likewise entirely English in zh mode (h1 + 6 h2s + lede) — PR #18 presumably covers this; flagged here for completeness.
5. Small copy/i18n nits: `monsoon` sensitivity note mixes an untranslated word "onset" and uppercase "LIEBERMAN与BUCKLEY" into a Chinese sentence; `Language / 语言 / Ngôn ngữ` sr-only/aria label is untranslated (arguably intentional as a language menu label).

## 6. Artefacts

- Raw scans (JSON): `fleet.nosync/qa/shots/polish/zh-scan-local2.json`, `en-scan-local.json`, `zh-scan-live.json`, `en-scan-live.json`, `ui-diff-local.json`; committed compact extracts in `docs/audit/polish/`.
- Screenshots: `fleet.nosync/qa/shots/polish/{en,zh}-shots-local/` (76), `{en,zh}-shots-live/` (24); committed key shots `docs/audit/polish/screens/`.
- Scripts: `qa/shots/polish/scan.mjs`, `ui-diff.mjs`.
- Reproduce: `PATH=/opt/homebrew/bin:$PATH` (Node 26), `npm run build`, `npx vite preview --port 4180`, then `node qa/shots/polish/scan.mjs http://127.0.0.1:4180/ zh-Hans out.json shots/`.
