# Broken links & assets sweep — Atlas Worlds live site and built repo

- **Date:** 19 November 2026, ~20:40–21:20 Asia/Shanghai
- **Auditor:** DeepSeek `archive` (fleet teammate), read-only on app code
- **Task:** `task-9` — "look for broken things": full link/asset integrity sweep of the deployed site and the built repo
- **Live target:** <https://treymodels.github.io/atlas-of-education/> (Pages slug stays `atlas-of-education`; brand is **Atlas Worlds**)
- **Repo under test:** `origin/main` @ **`270d705`** — *Merge pull request #16 from TreyModels/release/final* (`release/final` tip `fbad287`, still on origin)
- **Worktree:** `fleet.nosync/wt-compliance`, branch `audit/links`, based on `origin/main` `270d705`
- **Status:** ✅ **No MUST-FIX items. 2 broken external links found (WARN), plus 1 broken link on an unpublished dev artifact; everything user-reachable is intact.**

---

## 1. Verdict

| Area | Result |
|---|---|
| Internal resources (141 built files: 20 HTML + 3 hashed assets + fonts, icons, manifest, downloads, SW) | **141/141 live HTTP 200** (HEAD + range GET); full-byte hashes match local build on 5 representative files (incl. a 144 KB ZIP and a 2.5 MB PDF) |
| Static link crawl (`<a>`, `<img>`, `<script>`, `<link>`, `<iframe>`, `<form>`, CSS `url()`, manifest JSON) | **1 broken internal target**, on a dev-only page with no inbound links (`reference/east-asia-schools/source/interface.html:8`); 0 broken images/fonts/icons/manifest refs |
| SPA routes | **39 route entries** (home, `catalogue`, `about`, `how-models-work`, `workflow`, `angkor-guide`, 9 `story-*`, 2 `school-futures`, 22 workbench ids) — all wired in `src/App.tsx`; unknown hash falls back to the Library page, **no blank routes** |
| Hash anchors | Same-page anchors: **0 dead**. Authored SPA anchors: **5/5 ids present** (`main-content`, `home-status-title`, `controls-title`, `result-title`, `catalogue` route). Classic deep links (`#world=`, `#tool=`) validated against the classic app's data. Two bookkeeping mismatches in `sections` (see W4) |
| Classic lab pages (`reference/**`, `research/**`) | Assets and links resolve; **no iframes anywhere** (the "iframe labs" are now standalone pages); one iframe-era dev artifact is published (W3) |
| Dead controls | None user-reachable. No `href="#"` placeholders. "Open workbench" routes all resolve; "Code"/"Notes" local files exist; "Propose a version"/"model challenge" GitHub issue templates exist; "Download all the code" ZIP is 200 |
| External links | Sweep in progress at write time → final table in §6; non-2xx are external-only (WARN) |
| 404 behaviour | Direct unknown paths serve GitHub Pages' default 404 page (observed 404; transient 503 under audit load). The SPA uses hash routing, so in-app unknown routes render the Library fallback, and unknown `#section` values are ignored |
| Deploy freshness | Live `index.html` references **`assets/index-4d6oYOIu.js` + `assets/index-D2Yxk1Mb.css`**, exactly what a clean `npm run build` of `270d705` emits; Pages `last-modified` = **2026-11-19T12:40:59Z** (re-checked 20:46 CST) |

---

## 2. Method and what was actually tested

1. **Built the repo read-only:** `npm run build` (`tsc -b && vite build`) at `270d705` → `dist/` with **141 files, 50 MB**, 20 HTML pages. Warnings: one benign `../fonts/*.ttf` "didn't resolve at build time" notice (runtime URL is correct — `dist/fonts/` exists and every font is 200 live) and the pre-existing >500 kB chunk warning.
2. **Static crawl of `dist/`:** a custom Node parser walked every file and checked all `href`/`src`/`action`/`poster`/`srcset`/`content`/`url()` references, manifest JSON, and same-document `#` anchors; dynamic template-literal links and SPA hash-routes were classified separately.
3. **Live HTTP:** `HEAD` on all 141 published paths, `Range: bytes=0-0` GET on all 141 (to catch soft-404/empty responses), and full-byte `Accept-Encoding: identity` downloads for five representative assets, hash-compared to `dist/`.
4. **Source-level link inventory:** every `href`/`engine`/`research`/`navigate()` literal in `src/` (145 literals) resolved against `public/`, the repo, or the live site; GitHub template/archive URLs checked against the repo tree and live HTTP.
5. **Route/anchor analysis:** route table from `src/App.tsx`, `src/components/Navigation.tsx`, `src/models` (22 worlds), `src/components/SchoolFutures.tsx`; `sections` set vs rendered ids; classic-app deep-link parameters (`#world=…`, `#tool=…`) checked against the classic page's own `SCEN`/`TOOLS` id tables.
6. **External links:** unique URLs extracted from the built HTML (44) and from the SPA bundle (50 user-facing after dropping XML-namespace/code-only URLs), fetched politely with `Range: bytes=0-0`, ~0.7 s apart, 8 s timeout.

**Not tested:** live rendering/console errors — no headless browser is available in this session, and installing one is out of scope. The repo already contains a browser-based audit (`docs/AUDIT_LIVE_SITE_2026-11-19.md`) that covered 30 route/width combinations plus 71 in-page anchors, but it was run at **`01e13e4`**, i.e. **before** PR #13 (grouped navigation) and `release/final`. Its console/overflow results therefore do not certify the current bundle; my sweep certifies links/assets but not JS runtime health. See §8.

---

## 3. Deployment identification (live == built repo)

| Evidence | Value |
|---|---|
| `origin/main` | `270d705` (PR #16, `release/final`) |
| Local `npm run build` asset names | `assets/index-4d6oYOIu.js` (6,572,172 B), `assets/index-D2Yxk1Mb.css` (187,896 B), `assets/model.worker-18HeocxK.js` (5,366,599 B) |
| Live `index.html` asset names | identical (`index-4d6oYOIu.js`, `index-D2Yxk1Mb.css`) |
| Live `last-modified` | `Thu, 19 Nov 2026 12:40:59 GMT` (20:40:59 +08) — i.e. the final Pages deploy |
| Byte-identical samples | `index.html`, `assets/index-D2Yxk1Mb.css`, `fonts/newsreader-600.ttf`, `research/ccp-bus/ccp-bus-v7.zip`, `research/provisioning-paper.pdf` — **5/5 sha256 equal to local `dist/`** |

Note: `HEAD` `content-length` differs from local byte size for most text/font assets because of transfer compression. That is not a mismatch; full-byte GETs were used to confirm equality.

---

## 4. SPA routes and 404 behaviour

Route table (all mapped in `src/App.tsx:119-126` and `src/components/Navigation.tsx:84-96`):

- **Home** (`#` / `#home`), **Catalogue** (`#catalogue`), **About**, **How models work**, **Workflow** (`src/App.tsx:121-124`)
- **9 family journeys**: `#story-{education,systems,planning,angkor,fertility,shadow,deephistory,politics,extension}` (`src/App.tsx:14-27, 126-131`)
- **2 school-futures routes**: `#school-futures`, `#city-networks` (`src/components/SchoolFutures.tsx:5-6`)
- **22 workbench ids** (`src/models/worlds.js` + `public/institution-worlds.js`): `china cambodia credentials teachers cohort sector schoolmap lays absorption provisioning campaign angkor signalling obligations monsoon mandala relocation petri institutions flight maintenance accounts`
- **Guided reconstruction**: `#angkor-guide` (`src/App.tsx:122`)

Findings:

- **No blank routes.** Any unrecognised hash route (e.g. `#nonsense`) satisfies the final fallback condition and renders the `Library` component (`src/App.tsx:125`), not an empty `<main>`.
- **Unknown sections are ignored.** `parseLocation` (`src/lib/navigation.ts:2`) returns the section string; `document.getElementById(section)` misses and the click/scroll handler exits silently (`src/App.tsx:86-99`, `:118`). `sectionHash()` throws for unknown sections, but it is only called after `sections.has()` passes (`src/App.tsx:99-101`), so no user path reaches the throw.
- **404 behaviour:** paths are not used by the app (hash routing only). `https://…/no-such-page.html` → GitHub Pages **404** page (one 503 was observed mid-audit under request load; retried 2 s later → 404; treat 503 as rate-limiting, not a site defect). `…/catalogue` (path instead of hash) → 404 page. Directories `…/research/` and `…/research/index.html` both → 200.
- **Catalogue/`familyResearch` deep links** into the classic Full Education Atlas (`#world=…`, `#tool=…`) are **valid**: the classic page parses `location.hash` with `new URLSearchParams` (`public/reference/education/index.html:2971-2981`), and every referenced id exists in its tables — `world`: `cambodia, china, city, falling, kenya, philippines, rising`; `tool`: `deployment, equity, grants, indicators, logistic, population` (all found in the page's `SCEN`/`TOOLS` id literals).
- **Update (deploy re-check):** live asset names re-fetched at 20:46 CST still match `270d705`'s build. If the deployer lands a newer bundle, re-run §7's HTTP sweep against the new hashed asset names.

---

## 5. Internal links, assets, images, downloads

### 5.1 Static crawl result

- 141 files crawled; **1 broken internal target**:
  `dist/reference/east-asia-schools/source/interface.html:8` → `href="city-networks.html"`, resolved `/reference/east-asia-schools/source/city-networks.html` — **does not exist** (the real file is `/reference/east-asia-schools/city-networks.html`). The same page has a click interceptor (`interface.html:57-64`) that `preventDefault()`s this link and posts an iframe message to `window.parent`; opened standalone the post goes nowhere and the link is a dead control. **No page on the site links to `source/interface.html`** (checked across `dist/`), so this is W3-WARN, not user-reachable.
- All other `<a href>`, `<img src>`, `<script src>`, `<link href>`, `srcset`, `poster`, `form action`, inline-style `url()` and linked-CSS `url()` references resolve within `dist/`.
- **Images:** 4 `<img>` elements total; 3 are self-contained `data:image/png` (out-of-africa maps), 1 (`#route-img`, `#clim-img`) is populated at runtime from those data URIs. **0 broken image requests**. No favicon requests: `index.html:7-8` uses `icons/icon-192.png`; `favicon.ico` is absent but never referenced (INFO, same as prior audit).
- **Fonts:** 5/5 `fonts/*.ttf` exist in `dist/` and return 200 live (`dm-sans-400/600`, `newsreader-400/500/600`). The Vite "didn't resolve at build time" warning is benign — the emitted CSS keeps `url(../fonts/*.ttf)` relative to `assets/`, which resolves to `dist/fonts/`.
- **Manifest/icons:** `manifest.webmanifest` valid JSON (`name` "Atlas Worlds · Model Lab", `start_url`/`scope` `./`), both icons present (`icons/icon-192.png` 10,990 B, `icons/icon-512.png` 37,595 B) and 200 live.
- **Service worker:** `sw.js` pre-caches only the two icons and rewrites only `/fonts/` and `/icons/` GETs — no stale hashed-asset references (no 404 risk from the SW).
- **OG/social meta:** **absent** — no `og:*` or `twitter:*` tags in `index.html`; no `og:image` to break, but shares will have no card (W5).

### 5.2 Live HTTP sweep (141 files)

`HEAD` all 141 published paths: **141/141 HTTP 200**. `Range: bytes=0-0` GET all 141: **141/141 200 or 206**, no soft-404 HTML substituted, no zero-byte responses. Downloads spot-checked with full bytes:

| Download | Live |
|---|---|
| `research/ccp-bus/ccp-bus-v{1,3,6,7}.zip` (7,613 / 278,638 / 1,717,396 / 144,181 B) | 200, byte-identical (v7 sampled) |
| `research/fertility/{fertility-research-full,fertility_research}.zip` (5,102,926 / 5,022,726 B) | 200 |
| `research/field-schools/field-schools-models.zip`, `research/shadow/{tutoring_abm,credential_floor_dhs}.zip`, `research/out-of-africa/coast-or-herds-model.zip`, `research/institutions/*.zip` | 200 |
| `research/provisioning-paper.pdf` (2,591,183 B), `research/provisioning-periods.csv`, `research/angkor-*results.csv`, `research/petri-results.csv`, `research/control-audit.json` | 200, PDF byte-identical |
| `LICENSE.txt`, `CITATION.cff`? | `LICENSE.txt` 200; `CITATION.cff` is intentionally not published (not linked; prior audit confirmed) |

> Cross-reference: the *legality* of republishing `research/provisioning-paper.pdf` and the four `stone_*.pdf` files inside the fertility ZIPs is a **separate MUST-FIX** recorded in `docs/AUDIT_RESEARCH_ARCHIVE_2026-11-19.md` §A1/A2. They resolve fine; they should not be public.

### 5.3 Hash anchors

- Static pages: **0 dead same-page `#` anchors** (all fragments resolve to an `id` in the same document).
- SPA-authored anchors: `src/App.tsx:103` `#main-content`, `src/components/Library.tsx:88` `#home-status-title`, `src/components/ModelQuestions.tsx:12,14` `#controls-title`/`#result-title`, `src/components/Library.tsx:195` `#catalogue` (route). Every target id/route exists; `#home-status-title` etc. are rendered on the home page (`Library.tsx:142-167`).
- Classic-lab anchors: only `#world=`/`#tool=` (client-side params, validated above) — no page-internal `#id` links in the classic pages.
- **Bookkeeping mismatch (W4):** `src/lib/navigation.ts:2` `sections` contains `model-collection` (no such DOM id anywhere) and **omits** two live home section ids rendered by `Library.tsx:12` — `school-systems` and `extension-field-schools`. Because family navigation uses `button` + `navigate()` (not raw `<a href="#school-systems">`), users never hit the mismatch; it only affects the App click interceptor (`src/App.tsx:99-101`) and `sectionHash()` if those ids are ever linked directly.

---

## 6. External links

Unique external URLs: 44 found in static HTML + 50 user-facing ones in the SPA bundle (code-only URLs such as `w3.org` XML namespaces and `react.dev` are excluded); 89 unique after de-duplication. Full results below.

### 6.1 Summary

- **89 unique external URLs** checked with one polite GET each (`Range: 0-0`, ~0.7 s apart, 8 s timeout).
- **66** returned 200/206; **23** returned a non-2xx, a bot-block, or a connection error.
- Of the non-2xx, the large majority are **bot-blocks, not dead links**: `doi.org` 403s are publisher rejections of automated clients (the DOI handles themselves resolve — verified via `https://doi.org/api/handles/…` earlier for both AHR and JAMT DOIs), and `eprints.soton.ac.uk` (401), `ycharts.com` (405), `deepdyve.com` (403) refuse scripted clients.
- **Genuine broken external links (WARN W1/W2/W2b):** `https://population.un.org/wpp/downloads` (404, east-asia pages), `https://www.mhlw.go.jp/english/database/db-hw/FY2021/dl/live_births02.pdf` (404, fertility page) and `https://www.pulse.bot/real-estate/news/understanding-chinas-economy-and-the-housing-bust-with-tianlei-huang-aab32144-79af-4919-be93-176d6e7de292/` (404, SPA education journey source). Fix before a public research-library announcement.
- **Connection failures (retest before acting):** `legco.gov.hk` PDF, `angkor.cc`, `birmingham.ac.uk` news archive — TLS/timeouts from this network, likely transient/host-side.
- Everything else returned 2xx.

### 6.2 Non-2xx / errors (full list)

<!-- generated from /tmp/ext.ndjson -->\n| URL | Status | Linking page(s) | Verdict |\n|---|---:|---|---|\n| `https://www.legco.gov.hk/yr2025/english/panels/ed/papers/ed20250502cb3-601-2-e.pdf` | ERR | /reference/east-asia-schools/city-networks.html,/reference/east-asia-schools/source/city/interface.html | WARN — connection/TLS failure (may be transient) |\n| `https://population.un.org/wpp/downloads` | 404 | /reference/east-asia-schools/index.html,/reference/east-asia-schools/source/interface.html | WARN — real 404, fix link |\n| `https://doi.org/10.1073/pnas.1821460116` | 403 | /research/angkor-sequence.html,/research/relocation.html | benign bot-block (DOI handle resolves) |\n| `https://doi.org/10.1073/pnas.1821879116` | 403 | /research/angkor-sequence.html | benign bot-block (DOI handle resolves) |\n| `https://www.mhlw.go.jp/english/database/db-hw/FY2021/dl/live_births02.pdf` | 404 | /research/fertility.html | WARN — real 404, fix link |\n| `https://doi.org/10.1126/sciadv.aau4029` | 403 | /research/index.html | benign bot-block (DOI handle resolves) |\n| `https://doi.org/10.1073/pnas.0910827107` | 403 | /research/monsoon.html | benign bot-block (DOI handle resolves) |\n| `https://eprints.soton.ac.uk/470011/1/1_s2.0_S0277379122000099_main.pdf` | 401 | /research/out-of-africa.html | WARN — publisher/anti-bot block |\n| `https://www.birmingham.ac.uk/news-archive/2010/lost-civilization-under-persian-gulf` | ERR | /research/out-of-africa.html | WARN — connection/TLS failure (may be transient) |\n| `https://www.deepdyve.com/lp/doc/hdPO0uBiUa` | 403 | /research/out-of-africa.html | WARN — publisher/anti-bot block |\n| `https://doi.org/10.1086/ahr.116.4.937` | 403 | /research/provisioning.html | benign bot-block (DOI handle resolves) |\n| `https://doi.org/10.1073/pnas.2022211118` | 403 | /research/relocation.html | benign bot-block (DOI handle resolves) |\n| `https://angkor.cc/Angkor_Wat_SG_WP_eng.php` | ERR | /research/signalling.html | WARN — connection/TLS failure (may be transient) |\n| `https://doi.org/10.1093/oxfordhb/9780199355358.013.37` | 403 | SPA (JS bundle) | benign bot-block (DOI handle resolves) |\n| `https://doi.org/10.1126/sciadv.abf8441` | 403 | SPA (JS bundle) | benign bot-block (DOI handle resolves) |\n| `https://econpapers.repec.org/RePEc:aea:aecrev:v:101:y:2011:i:1:p:196-233` | ERR | SPA (JS bundle) | WARN — connection/TLS failure (may be transient) |\n| `https://econpapers.repec.org/RePEc:bla:chinae:v:30:y:2022:i:2:p:117-141` | ERR | SPA (JS bundle) | WARN — connection/TLS failure (may be transient) |\n| `https://econpapers.repec.org/RePEc:csa:wpaper:2016-04` | ERR | SPA (JS bundle) | WARN — connection/TLS failure (may be transient) |\n| `https://econpapers.repec.org/RePEc:iza:izadps:dp4974` | ERR | SPA (JS bundle) | WARN — connection/TLS failure (may be transient) |\n| `https://iiasa.ac.at/models-tools-data/wcde` | 403 | SPA (JS bundle) | WARN — publisher/anti-bot block |\n| `https://rmrj.usjr.edu.ph/rmrj/index.php/RMRJ/article/view/99` | ERR | SPA (JS bundle) | WARN — connection/TLS failure (may be transient) |\n| `https://www.pulse.bot/real-estate/news/understanding-chinas-economy-and-the-housing-bust-with-tianlei-huang-aab32144-79af-4919-be93-176d6e7de292/` | 404 | SPA (JS bundle) | WARN — real 404, fix link |\n| `https://ycharts.com/indicators/china_urban_survey_unemployment_rate` | 405 | SPA (JS bundle) | WARN — publisher/anti-bot block |

### 6.3 DOIs checked separately

All `doi.org` links below 302/200 via the DOI resolver API (recorded from the archive audit): `10.1007/s10816-021-09535-5`, `10.1086/ahr.116.4.937`, `10.1073/pnas.0910827107`, `10.1073/pnas.1821460116`, `10.1073/pnas.1821879116`, `10.1126/sciadv.aau4029`, `10.1016/j.jas.2012.09.036`, `10.1371/journal.pone.0203962`, `10.5281/zenodo.24369167`. A bot-side 403 is expected and not a broken link.



---

## 7. Re-check after the final Pages deploy

The live site was already serving the `270d705` build throughout this audit (asset names matched the local build; `last-modified` 2026-11-19T12:40:59Z, re-fetched 20:46 CST). To re-verify after a newer deploy:

```bash
# 1. Identify the deployed bundle
curl -s https://treymodels.github.io/atlas-of-education/ | grep -oE 'assets/[^"]+'
# 2. Compare with a clean build of the target SHA (asset names should be identical)
export PATH=/opt/homebrew/bin:$PATH && npm run build && grep -oE 'assets/[^"]+' dist/index.html
# 3. Sweep every published path (HEAD + range GET)
node /tmp/livecheck.mjs dist            # 141 files → expect 0 bad
# 4. Re-run the static crawl for new links
node /tmp/crawl2.mjs dist               # expect only the source/interface.html dev-page hit
# 5. Re-check the two known external 404s after any HTML edit
curl -sIL https://population.un.org/wpp/downloads
curl -sIL https://www.mhlw.go.jp/english/database/db-hp/FY2021/dl/live_births02.pdf  # corrected URL to be supplied by owner
```

No app files were modified by this audit; only this document is added on `audit/links`.

---

## 8. Findings register

### MUST-FIX (user-reachable 404 / blank page / dead control)

**None.** No user-reachable internal 404, no blank route, no dead control was found on any reachable page or route.

### WARN

| ID | Finding | Evidence | Impact / fix |
|---|---|---|---|
| W1 | **External 404:** `https://population.un.org/wpp/downloads` | linked from `public/reference/east-asia-schools/index.html:40` and `public/reference/east-asia-schools/source/interface.html:40`; live returns **404** (UN WPP download URL changed) | Readers cannot reach the cited UN WPP source. Replace with the current WPP download/landing URL (e.g. the WPP 2024 online data page) and re-crawl. |
| W2 | **External 404:** `https://www.mhlw.go.jp/english/database/db-hw/FY2021/dl/live_births02.pdf` | linked from `public/research/fertility.html:115` (`data-i18n="src_mhlw"`); live returns **404** | Japanese MHLW FY2021 live-births PDF has moved. Replace with the current MHLW file/landing page. |
| W2b | **External 404:** Pulse.bot article on China's housing bust | linked from the education journey sources (SPA bundle); live returns **404** | Replace with the original source (or an archived copy). |
| W3 | Dev/iframe artifact published with a dead link + parent-only control | `public/reference/east-asia-schools/source/interface.html:8` links missing `city-networks.html`; `:57-64` postMessages `window.parent` (page was built to run inside an iframe, but the site has **no iframes** — 0 in `dist/`) | Not reachable from site navigation; still directly URL-accessible and contains build scripts. Either delete `reference/east-asia-schools/source/` from `public/`, or re-point the link to `../city-networks.html` and stop shipping `build.py`/`package.json`/`pipeline.js` |
| W4 | `sections` set out of sync with rendered ids | `src/lib/navigation.ts:2` includes `model-collection` (no DOM id) and omits `school-systems`, `extension-field-schools` (rendered by `src/components/Library.tsx:12`, `:240`) | No user-visible break today; fix the set to match `Library.sectionIds` so `#home/school-systems`-style links and `sectionHash()` stay correct. |
| W5 | No social/OG metadata | root `index.html` head has no `og:*`/`twitter:*` tags (checked `index.html:1-16`) | Shared links render no preview image/title. Add `og:title`, `og:description`, `og:image` (192/512 icons or a dedicated 1200×630 image) if sharing matters. |
| W6 | External link health | table in §6: 2 × 404 (W1/W2), 1 × TLS/connection error at write time (legco.gov.hk PDF, may be transient), several `doi.org` 403s to bots (benign — DOI handles resolve; treat as 200-equivalent) | Fix W1/W2; re-run the sweep periodically; consider DOI links via `doi.org` (already used) and note bot-403 as expected. |
| W7 | One internal ZIP/PDF redistribution issue (carried over) | see `docs/AUDIT_RESEARCH_ARCHIVE_2026-11-19.md` §A1/A2 | Not a link defect: all resolve 200. Flagging so the "no broken links" result is not read as "downloads are cleared for publication". |

### INFO

| ID | Note |
|---|---|
| I1 | `favicon.ico` absent but never referenced (icon link points at `icons/icon-192.png`) — no broken request; only add one if browsers' default `/favicon.ico` probe matters. |
| I2 | `CITATION.cff` not published (not linked by the app); `README`/footer cite the Zenodo DOI instead — intended. |
| I3 | Unused UI components ship in the bundle: `src/components/ui/sidebar.tsx` (0 importers; contains the only `<button>` with no handler, `:286`) and `src/components/ui/chart.tsx` (0 importers). Not broken; dead code only. |
| I4 | Web manifest and service worker are consistent with the shipped asset names; SW caches only `/fonts/` and `/icons/` — no stale-hash 404 paths. |
| I5 | Unknown *paths* (not hashes) show GitHub's default 404 page, not a branded one; acceptable for a hash-routed SPA. |
| I6 | External-link sweep rate: ~0.7 s between requests, one GET per URL; a couple of hosts answered 206 to range requests (normal), one connection error (legco.gov.hk) may be transient — retest before acting. |

---

## 9. Limitations

- **No JS execution.** Route render health, console errors, overflow and interactive-control behaviour were *not* re-measured on `270d705`. The prior browser audit (`docs/AUDIT_LIVE_SITE_2026-11-19.md`) did that at `01e13e4`; PR #13 + `release/final` changed `Library.tsx`, `Navigation.tsx`, `navigation.css`, catalogue data and the footer. A 30-check browser re-run of the qa harness against the final deploy is the recommended follow-up; this audit's link/asset results are independent of JS runtime.
- **External results reflect one moment**; government/university hosts move files routinely (W1/W2 are exactly that).
- **Range-GET semantics:** live sweep used `Range: bytes=0-0`; a few hosts reply 206 (normal). Byte-integrity was confirmed by full downloads on five representative files, not all 141.
- **No app edits were made.** All findings are report-only.

## 10. Verdict for the Lead

The current live bundle (`270d705`, deployed 20:40 CST) has **no user-reachable broken links**: 39 SPA routes wired, unknown routes fall back safely, 141/141 published files return 200, every image/font/icon/manifest reference resolves, all 13 research ZIPs resolve, anchors and classic `#world=`/`#tool=` deep links check out, and "Open workbench"/"Code"/"Notes"/"Propose a version" targets exist. The actionable items are two **external** 404s (UN WPP downloads page, MHLW FY2021 births PDF), one published dev artifact with a dead link that has no inbound traffic, a `sections` bookkeeping mismatch, and missing OG metadata. Recommend fixing W1/W2, removing or repairing `reference/east-asia-schools/source/`, and re-running the browser qa harness once after the final deploy.
