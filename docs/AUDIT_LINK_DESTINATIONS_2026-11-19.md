# Link-destination audit — where every click actually goes (PASS 1)

- **Date:** 19 November 2026, ~22:11–22:30 Asia/Shanghai
- **Auditor:** DeepSeek `archive` (fleet teammate), independent, read-only on app code
- **Task:** `task-18` — Trey's bug: clicking a fertility model entry in a hashtag-filtered result started a ZIP download instead of opening the model page. Audit every user-facing link's **actual destination**, not just its HTTP status.
- **Target under test (live):** <https://treymodels.github.io/atlas-of-education/>
- **Deployed commit (live):** **`0b263a1`** — validated from the Pages workflow run "Deploy GitHub Pages", branch `main`, conclusion success, `2026-11-19T14:06:49Z`; live `index.html` serves `assets/index-DZq8iuf3.js` + `assets/index-I_lZIfSh.css`, exactly the asset names emitted by a clean `npm run build` of `0b263a1` in this worktree (local build byte sizes match the live bundle).
- **Repo source read:** `origin/main` @ `0b263a1`
- **Worktree/branch:** `fleet.nosync/wt-compliance`, `audit/link-destinations` (report only; **no app code edited**)
- **Method:** headless Chromium (Playwright, 1280×1000 and 390×844) actually **clicked** every entry/control and recorded the resulting URL, hash, rendered `<h1>`, and any `download` event. Downloads were cancelled after capture so nothing was saved. Machine-readable matrix: [`docs/link-destinations-2026-11-19.json`](link-destinations-2026-11-19.json).

---

## 1. Verdict

**MUST-FIX: 19 catalogue entries whose primary click starts a file download instead of opening a model page** — exactly the list Trey reported (9 fertility models + fertility bundle, 2 shadow bundles, out-of-africa bundle, 4 CCP versions, 2 farmer-field-school models). **No other user-facing dead ends or misdirected links were found.**

| Surface | Clicks tested | Correct page/route | Raw file download | Dead / no-op | Wrong page |
|---|---:|---:|---:|---:|---:|
| Home catalogue entries (65 declared; 66 cards incl. 1 experimental) | 65 (+1) | **46** | **19 (all defects)** | 0 | 0 |
| Find-a-model results (`fertility`, `#fertility`, `#education`, `#water`, `#ccp`) | 5 query states + 3 result clicks | 2 (lab page, filtered route result) | **2 (model rows in `#fertility` results → ZIP)** | 0 | 0 |
| Home tag-cloud / card/topic chips | 5 | 5 (chip opens search with the same tag; results then filter) | 0 | 0 | 0 |
| Journey model-card actions (9 journeys, 41 cards) | 4 "Open workbench" clicks + all hrefs inventoried | 4/4 | 0 primary; **Code/Notes are explicitly labelled downloads/GitHub links (intended secondary)** | 0 | 0 |
| Nav rail / header / footer / mobile drawer | 5 rail + 3 footer + footer workflow button + brand + 5 drawer links | all correct pages / `#workflow` / home | 0 | 0 | 0 |
| About / How models work / Workflow | 3 routes | 3 (no anchor links inside the articles) | 0 | 0 | 0 |
| Workbench controls (`#angkor`, `#china`, `#cambodia`) | back link + 27 controls incl. tag chips, reset, guide | back → home; guide → `#angkor-guide`; tag chips → search overlay with `#tag` (**verified in a second pass**); Save/Export buttons are explicitly labelled | 2 labelled ("Save run JSON", "Export plotted data CSV") — intended | 0 | 0 |
| Research/reference static pages (18 pages) | 155 anchors inspected across 18 pages | internal page links and fragment anchors all resolve (0 unresolved `#fragment`) | all file links carry ZIP/CSV/Download labels | 0 | 0 |
| Classic Full Education Atlas deep links | 6 (`#world=china/city/kenya`, `#tool=indicators/logistic`, `#lab`) | 6/6 render the matching world/tool page | 0 | 0 | 0 |

- Console errors on the SPA: **0**.
- One pre-existing JS error on a **dev-only page with no inbound links** (`reference/east-asia-schools/source/interface.html`, `SyntaxError: Unexpected token ';'`) — WARN, see §5.
- The 19 defective entries are data-authored in `src/data/model-catalogue.ts` (no click handler: the card's primary element is `<a href="…zip">`). The same records feed the home catalogue, the Library search, Find-a-model results and hashtag-filtered results, so the bug appears on every one of those surfaces.

---

## 2. MUST-FIX: the 19 model entries whose primary click is a raw file download

All are `format: 'Code & data download'` and authored in `src/data/model-catalogue.ts` with a direct `href` to a file. Observed: click fires a `download` event; the user stays on the home page and never sees a page that names/describes the model. **Expected:** primary click opens the page that names and describes the entry (journey section/card or the relevant lab page), with the ZIP exposed as a **secondary, explicitly labelled** download (the fix branch `fix/link-destinations` is remapping these).

| # | id | Title (card) | source | currently downloads | expected destination (page naming it) |
|---|---|---|---|---|---|
| 1 | `development-survival` | Development (survival) model | `model-catalogue.ts:80` | `research/fertility/fertility-research-full.zip` (5,102,926 B) | `#story-fertility` — card `development-survival` |
| 2 | `matching-dummy` | Development + matching + post-2015 period dummy | `:81` | same fertility ZIP | `#story-fertility` — card `matching-dummy` |
| 3 | `credential-cohort` | Credential cohort model | `:82` | same fertility ZIP | `#story-fertility` — card `credential-cohort` |
| 4 | `mechanism-assortative` | Assortative matching mechanism lab | `:83` | same fertility ZIP | `#story-fertility` — card `mechanism-assortative` |
| 5 | `fecundity-age` | Fecundity-age model | `:84` | same fertility ZIP | `#story-fertility` — card `fecundity-age` |
| 6 | `ivf-policy` | IVF and policy suite | `:85` | same fertility ZIP | `#story-fertility` — card `ivf-policy` |
| 7 | `shock-suite` | Post-2015 shock suite | `:86` | same fertility ZIP | `#story-fertility` — card `shock-suite` |
| 8 | `microplastics-test` | Microplastics test | `:87` | same fertility ZIP | `#story-fertility` — card `microplastics-test` |
| 9 | `momentum-test` | Tipping / momentum lab | `:88` | same fertility ZIP | `#story-fertility` — card `momentum-test` |
| 10 | `fertility-bundle` | Fertility research bundle | `:89` | same fertility ZIP | `research/fertility.html` (lab page), secondary ZIP |
| 11 | `shadow-abm` | Tutoring ABM bundle | `:94` | `research/shadow/tutoring_abm.zip` | `#story-shadow` — matching card |
| 12 | `shadow-dhs` | Credential-floor DHS test | `:95` | `research/shadow/credential_floor_dhs.zip` | `#story-shadow` — matching card |
| 13 | `out-of-africa-bundle` | Out of Africa model bundle | `:100` | `research/out-of-africa/coast-or-herds-model.zip` | `#story-deephistory` (or `research/out-of-africa.html`), secondary ZIP |
| 14 | `ccp-v1` | CCP bus · Rival mechanisms | `:104` | `research/ccp-bus/ccp-bus-v1.zip` | `#story-politics` — card `ccp-v1` |
| 15 | `ccp-v3` | CCP bus · Economy and factions | `:105` | `research/ccp-bus/ccp-bus-v3.zip` | `#story-politics` — card `ccp-v3` |
| 16 | `ccp-v6` | CCP bus · Tilly mechanisms | `:106` | `research/ccp-bus/ccp-bus-v6.zip` | `#story-politics` — card `ccp-v6` |
| 17 | `ccp-v7` | CCP bus · Identification comparison | `:107` | `research/ccp-bus/ccp-bus-v7.zip` | `#story-politics` — card `ccp-v7` |
| 18 | `fs-diffusion` | Farmer field schools · Diffusion | `:111` | `research/field-schools/field-schools-models.zip` | `#story-extension` — card `fs-diffusion` |
| 19 | `fs-foodprice` | Farmer field schools · Food-price politics | `:112` | `research/field-schools/field-schools-models.zip` | `#story-extension` — card `fs-foodprice` |

All 19 download events were captured **(19/19 confirmed)**. Titles above are the exact rendered card titles. The eight distinct target files are all existing, byte-faithful downloads (see `docs/AUDIT_BROKEN_LINKS_2026-11-19.md`), so no link is 404 — the defect is purely destination/semantics.

### Reproduction of Trey's report

1. Home → "Find a model" → type `#fertility` (or click a `#fertility`-style chip on a model card).
2. The results list shows `Fertility collapse lab` (opens `research/fertility.html`) followed by 10 model rows.
3. Clicking row 2 (`Development (survival) model`) or row 3 (`Development + matching + post-2015 period dummy`) fires a download of `fertility-research-full.zip` and leaves the user on the home page. **Confirmed.** Rows 2–10 in that filtered list are among the 19 defects.

---

## 3. Correct destinations verified (no action)

- **Home catalogue, 46/65 entries already behave**: 27 are route `<button>`s that open workbenches/school-futures/journey pages naming the model (e.g. `China · Graduate jobs → #china`, `Angkor · Temple communities → #provisioning`, `Farmer field schools · Treadmill economy → #story-extension`), and 19 are in-site page links: 7 research lab/write-up pages (`research/massification/index.html#parents…`, `research/fertility.html`, `research/shadow-education.html`, `research/out-of-africa.html`) and 12 classic-atlas deep links (`reference/education/index.html#world=…` / `#tool=…`). Every one landed on a page whose `<h1>` names the destination or the model; **0 raw-file downloads, 0 dead clicks, 0 wrong pages**.
- **Experimental interface** `Scenario Theatre` (1 extra card, not counted in the 65) → `#sector` workbench, correct.
- **Hashtag behaviour:** home tag-cloud chip `#education` sets the Library search to `#education` (33 results → correct subset); a model-card tag chip opens the search overlay already filtered by that tag (e.g. `#economics`); workbench tag chips open the overlay with the tag (`#archaeology` verified). Tag→search→result→page flow is correct **except** when the chosen result is one of the 19 file-primary rows (then it downloads) — this is the same defect, not a tags defect.
- **Journeys:** 9 journey routes render 41 model cards; **0 unresolved `#fragment` anchors**; "Open workbench" buttons land correctly (e.g. angkor → `#provisioning`, education → `#china`, systems → `#school-futures`, planning → `#sector`). `Code`/`Notes`/`Propose a version` are explicit secondary actions: Code downloads the model ZIP or opens the engine `.js`, Notes opens README/RESULTS (or GitHub at the pinned import commit `2e19f07`), Propose opens the GitHub issue template — all labelled, all 200, and none is a card's primary action. **No change needed here**, but the fix must not make these the primary action.
- **Nav/header/footer/drawer:** 5 rail resources (`research/index.html`, `research/fertility.html`, `research/shadow-education.html`, `research/out-of-africa.html`, `reference/education/index.html`) all open the expected pages; footer `Reuse terms` (`LICENSE.txt`), Zenodo concept DOI (external, intended), `Full Education Atlas`; footer "My digital workflow" button → `#workflow`; brand → home; mobile drawer exposes the same 5 links. All correct.
- **Workbench:** back link → home (`#`); guide link → `#angkor-guide`; reset/recompute/replay/pin controls work without navigation; "Save run JSON" and "Export plotted data CSV" are explicitly labelled downloads (intended). No misrouted control found.
- **Static research/reference pages:** 18 pages, 155 anchors, **0 unresolved in-page fragments**, every local page link resolves, and every file link is labelled with ZIP/CSV/Download/Read wording (e.g. "Tutoring model · ZIP ↓", "720-run repair comparison · CSV"). The classic Full Education Atlas accepts `#world=` / `#tool=` / `#lab` deep links and renders the matching world/tool (6/6 verified).
- **Search coverage note:** `#ccp` returns 0 results because `ccp` is not one of the curated tags (the entries carry family/kind tags such as `#politics`/`#code-data`). Not a defect; recorded so the fix doesn't mistake it for a broken search.

---

## 4. Machine-readable matrix

`docs/link-destinations-2026-11-19.json` contains, for every surface above: the click target metadata (title/href/route/source), the observed result (landed URL/hash/`<h1>`/download filename), and pass/fail classification. It is regenerated by the same Playwright click harness used for PASS 2; PASS 2 will diff against this file.

---

## 5. WARN / observations (not blocking, not part of the 19)

| ID | Note |
|---|---|
| W1 | `public/reference/east-asia-schools/source/interface.html` throws `SyntaxError: Unexpected token ';'` in its inline script on load. It is a **dev artifact with no inbound links** on the live site (direct URL only); a separate polish PR (#21) repairs its dead `city-networks.html` href. Not a user-visible regression; fix or drop the `source/` directory in a later pass. |
| W2 | The catalogue's 19 entries display `Code & data download` as their format label, so the download is at least announced in the meta line — but the **primary action still downloads**, which is the reported bug. The fix should keep a clearly labelled secondary download control (e.g. "Download bundle · ZIP ↓"). |
| W3 | Journey `Code` actions download ZIPs (CCP/field-schools) or open `.js`; `Notes` open README/RESULTS on GitHub at the pinned `2e19f07` import commit. These are secondary and labelled; no change requested, but they should remain secondary after remapping. |
| W4 | Home tag click `#education` shows 33 cards while Find-a-model `#education` reports 32 results — the delta is the `Scenario Theatre` experimental interface, which is excluded from the 65-entry catalogue count by design. Benign. |
| W5 | Two external research links known from the broken-links audit are being fixed on `fix/polish-links` (UN WPP downloads page, MHLW FY2021 PDF). They are external 404s, unrelated to the 19 destination defects. |

---

## 6. PASS 2 plan (after `fix/link-destinations` deploys)

Re-run the same harness against the new live SHA and assert:

1. **Zero model-entry clicks that download:** all 19 ids from §2 open a page (route/hash or in-site HTML) whose `<h1>`/page text names/describes the entry — no `download` event on the primary card/row click.
2. **Every remapped entry lands on a page that names it:** expected page per §2 table; verify `<h1>`/card title match.
3. **Every download entry exposes a secondary labelled download:** on the destination page (or card) there is a control whose text contains "Download"/"ZIP"/"CSV" that fires the expected file download.
4. **Tag→search→result→page:** `#fertility`, `#politics`, `#water`, `#education` chips → search overlay filtered by the same tag → first model result opens a page (not a file).
5. **No new dead links:** all previously-correct 46 entries, nav/footer/journey/static/classic destinations still land where they did in PASS 1 (diff JSON).

Report will be a message (no new report file): new SHA, Pages run, PASS/FAIL per criterion, residual defects.

---

## 7. Bottom line

- **19 must-fix entries** (the exact list in §2; source lines `src/data/model-catalogue.ts:80-112`). All are model entries whose card/row is a raw ZIP anchor; 19/19 reproduced. Everything else Trey asked about — 46 catalogue entries, all hashtag chips, all Find-a-model surfaces, 41 journey cards, nav/footer/header/drawer, workbench controls, 18 static research/reference pages, and 6/6 classic deep links — goes to the correct page or a clearly labelled download.
- No app code was edited in this pass. Report + JSON are on `audit/link-destinations`.
