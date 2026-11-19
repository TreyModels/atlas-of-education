# Model-level coverage audit — all nine families, plus claims wording

**Date:** 19 Nov 2026 · **Auditor:** DeepSeek (auditor teammate) · **Repo:** `TreyModels/atlas-of-education` @ `origin/main` `c3cc71c`
**Branch:** `audit/model-coverage` · **Scope:** read-only analysis; no app, data or engine code changed.
**Trigger:** shared to-do `4a6c0657` (“Model-level coverage audit across all nine families; family badges alone do not complete this requirement”).

---

## 0. Method, and what the existing checks do and do not cover

Read: `src/data/model-catalogue.ts`, all nine `src/data/*-journey.ts`, `src/data/family-stories.ts`, `src/data/site-status.ts`, `src/components/Library.tsx`, `StoryPage.tsx`, `Navigation.tsx`, `Catalogue.tsx`, `App.tsx`, `src/data/about.ts`, `src/data/home-explainer.ts`, `index.html`, `public/research/*`, `experiments/`, and the 22 engine files.

Ground truth run (both **PASS** on `c3cc71c`):

| Script | Result |
| --- | --- |
| `node scripts/check-angkor-journey.mjs` | 9 journeys; Angkor 6 chapters/13 cards/27 links; education 6/8, systems 6/9, extension 6/4, ccp 5/4, fertility 9/9, deephistory 4/1, planning 6/12, shadow 6/3; all links resolve. **Passed.** |
| `node scripts/check-react.cjs` | 22 modules (= 22 live worlds), 1,722 translated entries, four-language render, selector checks. **Passed.** |

**Important limitation of the existing checks:** `check-angkor-journey.mjs` validates journey internals (chapter structure, card labels, link targets, Klassen boundary strings) and checks that every *referenced* card exists. It never compares a journey against `model-catalogue.ts`, so today a family can hold 9 model cards while the catalogue lists 2 and all checks stay green. `check-react.cjs` asserts `worlds.length === 22` and per-world narrative/translation coverage; it too has no catalogue-coverage assertion. That gap is the origin of most defects below.

Current headline counts on `c3cc71c`:

- **Catalogue:** 56 entries, 9 families; sum of `familyCounts` = 56 (`model-catalogue.ts:112-113`).
- **Journeys:** 63 model cards across 9 journeys (13 angkor, 12 planning, 9 systems, 9 fertility, 8 education, 4 ccp, 4 extension, 3 shadow, 1 deephistory).
- **Live worlds:** 22, all browser-executed, and **all 22 are mapped by `internal()`** calls in the catalogue — no live Atlas world is unlisted. This is a genuine strength and should be preserved.
- **Distinct catalogue targets:** 24 Atlas-workbench entries (22 worlds + 2 school-future dashboards), 13 iframe interfaces into the classic Education Atlas, 4 massification experiment tabs (one page), 10 zip-download entries mapping to 9 distinct zips, 3 static write-up/lab pages, 2 narrative journey entries. 24+13+4+10+3+2 = 56.
- **Journey cards vs catalogue entries:** 53 pair up (some only by artefact), 3 catalogue entries have no model card, 10 journey cards have no catalogue entry. Details in §2/§3.

---

## 1. Executive summary — highest-value defects

Severity: **H** = user-visible miscount or false claim; **M** = inconsistent labelling or duplicate interface; **L** = polish.

| # | Sev | Defect | File:line | Minimal suggested fix (patch only, not applied) |
| --- | --- | --- | --- | --- |
| D1 | **H** | **Fertility family is 2 catalogue entries vs 9 journey model cards.** The only “model” entry is the container page `research/fertility.html`; the nine real models (`development-survival`, `matching-dummy`, `credential-cohort`, `mechanism-assortative`, `fecundity-age`, `ivf-policy`, `shock-suite`, `microplastics-test`, `momentum-test`) are Python code in `fertility-research-full.zip` and are invisible to the library, filters, search and family count. | `src/data/model-catalogue.ts:72-75`; cards at `src/data/fertility-journey.ts:459-539` | Add 9 catalogue entries (`family:'fertility'`, `method:'Model variant · Python bundle'`, `format:'Code & data download'`, `href:'research/fertility/fertility-research-full.zip'`) or, minimally, change the lab entry to “Fertility lab (9 models)” and state the 9 variants in `question`. Family count then becomes 11 entries / 9 models. |
| D2 | **H** | **Education count is internally contradictory.** The journey says the family has “three live or fitted models … plus four stored massification experiments” (=7) and that “Download bundles and duplicate interfaces are not separate models” — yet the family has an 8th card, `credential-dhs`, whose only artefact is `credential_floor_dhs.zip`, and `familyCounts.education` is 8. | `src/data/education-journey.ts:48`, `:416`, card `:592-600`; `model-catalogue.ts:80`, `:112` | Either drop the `credential-dhs` card (keep it a research link) and set education count 7, or amend line 48 to “three live or fitted models, four stored massification experiments, and one replication package”. Do not do both. |
| D3 | **H** | **Credential-floor DHS is cross-classified three ways and has no shared id.** Catalogue id `shadow-dhs`, but `family:'education'`, physically defined in the `shadow` array; journey card id is `credential-dhs`; `familyResearch.shadow` still lists the same zip under Shadow. So a lookup by id, the shadow research rail, and the education family count disagree. | `model-catalogue.ts:77-81` (id `:80`), `:187` (shadow research link); `education-journey.ts:592`; shadow journey has no such card | Rename id to `credential-dhs`, move the literal into the `education` array, delete the duplicate from `familyResearch.shadow` (keep it in `familyResearch.education`). |
| D4 | **H** | **`format` cannot express “download” or “write-up”.** `format` is a two-value union (`'Atlas workbench' \\| 'Classic workbench'`, `model-catalogue.ts:11`), so 10 zip-download entries and 3 static report pages all display the badge “Classic workbench” under their title (`Library.tsx:18`), and the “Classic workbenches only” filter (`Library.tsx:221`, predicate `:53`) returns non-workbenches. Six of the zips (politics ×4, extension ×2) do not even say “download” in `method`; the four that do (`fertility-bundle`, `shadow-abm`, `shadow-dhs`, `out-of-africa-bundle`) contradict their own format badge. | `model-catalogue.ts:11,13,79,85,89-92,97-98`; `Library.tsx:18,53,221` | Widen the type to `'Atlas workbench' \\| 'Classic workbench' \\| 'Write-up' \\| 'Code & data download' \\| 'Narrated journey'` and set: 10 zip entries → `Code & data download`; `fertility-collapse`/`shadow-education`/`out-of-africa` → `Write-up`; `fs-treadmill`/`fs-pricetag` → `Narrated journey`. Then filter on `'Classic workbench'` still means what it says. |
| D5 | **H** | **“Every model, searchable” is false.** The library says it twice, but 9 fertility models and the shadow research track are not searchable; the searchable unit is a catalogue entry, not a model. | `Library.tsx:188`, `:210`; heading `:165` already says “catalogue entries”, so the wording is inconsistent within one page | Change both to **“Every catalogue entry, searchable.”** (or “Every listed model and download, searchable”). |
| D6 | **H** | **Two family badges name labels no card in the family carries.** Education badge includes purpose `teaching` but all 8 education cards are `mechanism`. Systems badge includes state `checked` but all 9 systems cards are `developing`. The badge is the only label a home-page visitor sees. | `src/data/site-status.ts:21` (education), `:22` (systems) | Remove `'teaching'` from `:21` and `'checked'` from `:22`. (Or add a genuinely teaching education model / a checked systems model, but no such card exists.) |
| D7 | **H** | **A second, stale catalogue is reachable from the nav and claims entries are “published”.** Nav “Research catalogue” → `Catalogue.tsx`, which renders `src/data/model-catalogue.md` (Nov 8 build queue; 18 rows; statuses Port/Build/Heavy; note “awaiting verification”). Its header promises “published mechanisms”. None of its 18 rows is marked Live, so it contradicts the 56-entry library it sits beside. | `src/components/Navigation.tsx:105`; `src/components/Catalogue.tsx:46`; `src/data/model-catalogue.md:1-30` | Either retire the route or label it: header → **“Browse candidate mechanisms, rival explanations and the proposed build queue.”** and eyebrow → “Research build queue (not the model library)”. |
| D8 | **M** | **Homepage `<meta name="description">` names a non-family and claims blanket interactivity.** “ecology” is not one of the nine families (it is a legacy Angkor chapter title), only 3 of 9 families are named, and 10/56 catalogue entries are downloads that do not run in the browser. | `index.html:6` | `Interactive research models for education, population, history and political economy. Change assumptions, compare outcomes and inspect the evidence; some entries are downloadable code and data.` |
| D9 | **M** | **“Runs locally in your browser” is attached to the whole catalogue count.** On home/catalogue (no active world) the rail reads “56 catalogue entries · 2 languages” immediately above “Runs locally in your browser”, so the blanket browser-execution claim covers 10 Python downloads, 3 static write-ups and 2 narrative entries. | `src/components/Navigation.tsx:120-121` | Render only for a world: `{activeWorld && <small>{t('Runs locally in your browser')}</small>}`, or change the string to **“Interactive entries run in your browser”**. |
| D10 | **M** | **Deephistory is counted 2 but has 1 model.** `out-of-africa-bundle` (a zip) is a catalogue “model” with no journey card; the family count home visitors see is 2. | `model-catalogue.ts:84-86`, `:112`; `deephistory-journey.ts:183` (one card) | Mark the bundle as `Code & data download` and exclude bundles from `familyCounts`/`totalModels` (see D4), or title it “Out of Africa model bundle (download)”. |
| D11 | **M** | **Politics counts four versions as four models, and labels zip downloads “Stored experiment”.** One model in 4 versions (`ccp-v1/v3/v6/v7`), each href a `.zip`, each `format:'Classic workbench'`. `ccp-bus-v1.zip` contains 6 code files and no README/FINDINGS. | `model-catalogue.ts:88-93`; `ccp-journey.ts:24,33,42,51` | Add a version suffix to titles (“CCP bus · Rival mechanisms (v1) · 1 model, 4 versions” on the family heading) and set format to `Code & data download`; add a README to v1 or point the entry at the briefing. |
| D12 | **M** | **Angkor “Guided sequence” / “Further experiment” split disagrees with the journey.** Catalogue puts `maintenance` and `relocation` in *Further experiment*; the journey introduces maintenance in Chapter 3 and relocation in Chapter 5 and lists only `petri, institutions, flight, accounts, mandala` as `deeper`. | `model-catalogue.ts:65-70`; `angkor-journey.ts:134` (ch. 3 models), `:173` (ch. 5), `:205` (`deeper`) | Use `guided = [provisioning, campaign, angkor, signalling, obligations, monsoon, maintenance, relocation]` and `further = [mandala, accounts, institutions, flight, petri]`, or rename the labels to “Chapter models / Deeper experiments”. |
| D13 | **M** | **Duplicate artefacts counted as separate entries in Extension.** `fs-diffusion` and `fs-foodprice` both href the same `field-schools-models.zip`; `fs-treadmill` and `fs-pricetag` both `route:'story-extension'`. All four catalogue titles also differ from the four journey card titles (“Farmer field schools · Diffusion” vs “Finite-horizon adoption on a lattice”, etc.). | `model-catalogue.ts:95-100`; `extension-journey.ts:262,272,282,292` | Keep 4 entries (they are 4 distinct models/cards) but label format correctly (`Code & data download` ×2, `Narrated journey` ×2) and align the four `title` strings with the card titles; state “both current models ship in one bundle” in `question`. |
| D14 | **L** | **Dead narrative layer.** `family-stories.ts` (316 lines, 9 “class stories” with a `StoryPage` component) is not routed: `StoryPage` is imported nowhere, and `familyStories` is used only for `document.title` in `App.tsx:61`. Its `models in this class` rail would also have shown the same under-counts. | `src/components/StoryPage.tsx:35`; `src/data/family-stories.ts:21,315`; `App.tsx:25,61` | Either delete `family-stories.ts` + `StoryPage.tsx`, or wire the story route; do not leave a third narrative surface that nobody can reach. |
| D15 | **L** | **Residual claim/label wording in the About pages.** See §5: `about.ts:28` and `site-status.ts:28` (“Every model can be downloaded, run on your own machine and changed/modified”), `about.ts:20` and `workflow:81` (“Each has a declared purpose”, “labelled as failed” — there is no `failed` state), `about.ts:9` (“current limitations are shared” — not verifiable for `ccp-bus-v1.zip`). | see §5 | Small wording patches in §5. |

**Scoreboard for the shared checklist item:** coverage at the *family badge* level exists (9 badges, purposes/states), but the model-level requirement is **not met for fertility** (9 models unlisted), **not met for shadow** (2 of 3 cards unlisted / id-mismatched), **not met for deephistory** (bundle counted, 1 model), **over-counted for politics** (4 versions) and **ambiguous for education** (bundle card vs stated rule). Angkor, planning and systems are fully mapped at entry↔card level.

---

## 2. Per-family matrices

### 2.1 Education (catalogue 8 · journey cards 8 · live worlds 3)

| # | Catalogue entry id | Journey card id | Delivery | Labels on card (purpose/state) | Note |
| --- | --- | --- | --- | --- | --- |
| 1 | `china` | `china` | live Atlas world `china` | mechanism / developing | ✓ |
| 2 | `cambodia` | `cambodia` | live world `cambodia` | mechanism / developing | ✓ |
| 3 | `credentials` | `credentials` | live world `credentials` | mechanism / developing | catalogue title shorter than card title |
| 4 | `massification-parents` | same | tab of `research/massification/index.html` | mechanism / checked | 4 entries → 1 page, 4 distinct stored experiments (acceptable, but note the page is not a world) |
| 5 | `massification-actors` | same | tab | mechanism / checked | — |
| 6 | `massification-access` | same | tab | mechanism / checked | — |
| 7 | `massification-persistence` | same | tab | mechanism / checked | — |
| 8 | `shadow-dhs` | `credential-dhs` | **`research/shadow/credential_floor_dhs.zip`** | mechanism / evaluated | **id + family + location mismatch (D3); bundle with a model card (D2)** |

Defects: D2, D3, D5; badge D6.

### 2.2 Systems (catalogue 9 · cards 9 · live React worlds 0, iframe worlds 7)

| # | Entry | Card | Delivery | Card labels |
| --- | --- | --- | --- | --- |
| 1 | `school-futures` | same | `public/reference/east-asia-schools/index.html` via `SchoolFutures` | accounting / developing |
| 2 | `city-networks` | same | `.../city-networks.html` via `SchoolFutures` | accounting / developing |
| 3 | `city-system` | same | `reference/education/index.html#world=city` | teaching / developing |
| 4 | `cambodia-system` | same | `...#world=cambodia` | accounting / developing |
| 5 | `china-system` | same | `...#world=china` | accounting / developing |
| 6 | `philippines-system` | same | `...#world=philippines` | accounting / developing |
| 7 | `kenya-system` | same | `...#world=kenya` | accounting / developing |
| 8 | `riverton-system` | same | `...#world=rising` | teaching / developing |
| 9 | `stillwater-system` | same | `...#world=falling` | teaching / developing |

Fully mapped (9/9). Defect: systems badge claims `checked` but every card is `developing` (D6). Note: entries 3–9 are interfaces **into the classic Education Atlas**, which embeds the same 7 worlds; the catalogue correctly counts the classic world separately from the Atlas-family worlds (`china` vs `china-system`, etc.), so this is not a duplicate.

### 2.3 Planning (catalogue 12 · cards 12 · 6 live worlds + 6 iframe tools)

| # | Entry | Card | Delivery | Purpose/state |
| --- | --- | --- | --- | --- |
| 1 | `cohort` | same | live world `cohort` | teaching / checked |
| 2 | `sector` | same | live world `sector` | teaching / developing |
| 3 | `teachers` | same | live world `teachers` | teaching / developing |
| 4 | `schoolmap` | same | live world `schoolmap` | teaching / developing |
| 5 | `lays` | same | live world `lays` | teaching / developing |
| 6 | `absorption` | same | live world `absorption` | teaching / developing |
| 7 | `indicators` | same | `reference/education/index.html#tool=indicators` | accounting / checked |
| 8 | `population` | same | `...#tool=population` | teaching / developing |
| 9 | `deployment` | same | `...#tool=deployment` | teaching / checked |
| 10 | `equity` | same | `...#tool=equity` | accounting / checked |
| 11 | `grants` | same | `...#tool=grants` | accounting / checked |
| 12 | `logistic` | same | `...#tool=logistic` | teaching / checked |

12/12 mapped, badges consistent with cards. **Semantic inconsistency:** `model-catalogue.ts:105` says “the toolkit is methods, not models”, yet these 12 entries are included in `totalModels` (56) and in “Every model, searchable”. Also `familyInfo.planning.description` (line 129) calls them “Twelve independent implementations” — the repo shows 6 Atlas worlds + 6 classic-app tools, and the classic app also implements the other 6 methods, so “independent” is **not verified from repo** (D16-L).

### 2.4 Angkor (catalogue 13 · cards 13 · live worlds 13)

All 13 entries are `internal()` → live browser worlds; all 13 cards present. Card labels:

`provisioning` published/checked · `campaign` mechanism/developing · `angkor` mechanism/developing (old engine) · `signalling` mechanism/checked · `obligations` mechanism/checked · `monsoon` mechanism/developing · `petri` mechanism/checked · `relocation` mechanism/checked · `maintenance` accounting/checked · `institutions` teaching/developing · `flight` teaching/developing · `accounts` accounting/checked · `mandala` mechanism/historical.

Fully mapped (13/13). Defects: D12 (guided/further split). Note `mandala` card has no `engine` and no `research` link (`angkor-journey.ts:219`) though the live world exists — acceptable, it is labelled historical/stored runs.

### 2.5 Fertility (catalogue **2** · cards **9** · live worlds 0)

| # | Catalogue entry | Delivery | Journey card (no catalogue entry) |
| --- | --- | --- | --- |
| 1 | `fertility-collapse` (title “Fertility collapse lab”) | static page `research/fertility.html`; 2 script tags and **0 input controls** → a write-up, not a workbench | — |
| 2 | `fertility-bundle` (zip) | `research/fertility/fertility-research-full.zip` (Python) | — |
| — | **missing** | same zip | `development-survival` (459) · `matching-dummy` (468) · `credential-cohort` (477) · `mechanism-assortative` (486) · `fecundity-age` (495) · `ivf-policy` (504) · `shock-suite` (513) · `microplastics-test` (522) · `momentum-test` (531) |

Nine model cards, all mechanism/developing, all with `engine: research/fertility/fertility-research-full.zip`, none with a route. **This is the single largest coverage hole (D1/D5).** Count shown to users: 2.

### 2.6 Shadow (catalogue 2 in family · cards 3 · live worlds 0)

| # | Catalogue entry | Card | Match | Delivery | Card labels |
| --- | --- | --- | --- | --- | --- |
| 1 | `shadow-education` (title “Shadow education lab”) | `shadow-lab` (title “…(stored runs)”, `shadow-journey.ts:388`) | id mismatch | static page `research/shadow-education.html` (report + archived explorer, no input controls found) | mechanism / **historical** |
| 2 | `shadow-abm` (“Tutoring ABM bundle”) | `tutoring-abm` (“Tutoring agent-based model (code and calibration)”, `:396`) | id mismatch | zip `research/shadow/tutoring_abm.zip` | mechanism / **historical** |
| — | **no entry** | `research-folder` (“Shadow education research track”, `:404`) | — | GitHub folder link | mechanism / developing |
| (3) | `shadow-dhs` / `credential-dhs` | card lives in education journey | cross-family | zip | mechanism / evaluated |

Defects: D3, id mismatches, and the catalogue gives **no state label**, so a library browser cannot see that both shadow models are historical (the journey can). The `research-folder` card is a research track, not a model — either add it to the catalogue as a “Research track (not a model)” entry or keep it in the journey only; today it is the only unexplained card.

### 2.7 Deep history (catalogue **2** · cards **1** · live worlds 0)

| # | Entry | Card | Delivery |
| --- | --- | --- | --- |
| 1 | `out-of-africa` | `out-of-africa` (`deephistory-journey.ts:183`) | static write-up `research/out-of-africa.html` (1 slider only) + 800-run Python model in zip |
| 2 | `out-of-africa-bundle` | **none** | `research/out-of-africa/coast-or-herds-model.zip` |

Defect: D10 — bundle counted as a model and as half the family count; 4 chapters, 1 card is correct for a single-model family.

### 2.8 Politics (catalogue 4 · cards 4 · live worlds 0)

| # | Entry | Card (`ccp-journey.ts`) | Delivery | Card labels |
| --- | --- | --- | --- | --- |
| 1 | `ccp-v1` | `:24` | zip `ccp-bus-v1.zip` | mechanism / checked |
| 2 | `ccp-v3` | `:33` | zip | mechanism / developing |
| 3 | `ccp-v6` | `:42` | zip | mechanism / developing |
| 4 | `ccp-v7` | `:51` | zip | mechanism / **evaluated** |

One model, four stored versions — legitimate as versions, but `totalModels` counts them as 4 models (D11). All four are Python zips labelled “Stored experiment … · Classic workbench”; `ccp-bus-v1.zip` has no README/FINDINGS (6 code files), so “limitations are shared” is not verifiable for it.

### 2.9 Extension (catalogue 4 · cards 4 · live worlds 0)

| # | Entry | Card (`extension-journey.ts`) | Delivery | Card labels |
| --- | --- | --- | --- | --- |
| 1 | `fs-diffusion` | `:262` | `field-schools-models.zip` | mechanism / developing |
| 2 | `fs-foodprice` | `:272` | **same zip** | mechanism / developing |
| 3 | `fs-treadmill` | `:282` | `route: story-extension` (journey page, chapter 5) | mechanism / historical |
| 4 | `fs-pricetag` | `:292` | **same route** | mechanism / historical |

4/4 mapped by id; defects are format labels, duplicate targets and title drift (D13). The zip does contain distinct code directories `03_code/01_treadmill_economy`, `02_price_tag`, `03_diffusion`, so the four entries are four real model artefacts, not one counted four times.

### 2.10 Coverage matrix (one line per family)

| Family | Catalogue entries | Journey cards | Live browser worlds | Zip bundles | Static write-ups | Narrative entries | Unmatched entries | Unmatched cards | Badge/card mismatch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| education | 8 | 8 | 3 | 1 | 0 | 0 | 0 | 0 | purpose `teaching` claimed, absent |
| systems | 9 | 9 | 0 (2 dashboards + 7 iframes) | 0 | 0 | 0 | 0 | 0 | state `checked` claimed, absent |
| planning | 12 | 12 | 6 | 0 | 0 | 0 | 0 | 0 | — |
| angkor | 13 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | — |
| fertility | 2 | 9 | 0 | 1 | 1 | 0 | 1 (lab) | **9** | — |
| shadow | 2 | 3 | 0 | 1 | 1 | 0 | 0 | 1 (research track) | — |
| deephistory | 2 | 1 | 0 | 1 | 1 | 0 | 1 (bundle) | 0 | — |
| politics | 4 | 4 | 0 | 4 (=1 model, 4 versions) | 0 | 0 | 0 | 0 | — |
| extension | 4 | 4 | 0 | 2 (=1 zip) | 0 | 2 (=1 page) | 0 | 0 | — |
| **Total** | **56** | **63** | **22 (+2 dashboards, +13 iframes)** | **9 distinct zips / 10 entries** | **3** | **2** | **3** | **10** | **2** |

---

## 3. Defect list with exact file:line and suggested patches

Numbers match §1; L items collected here.

**D1 — Fertility: 9 models unlisted.** `src/data/model-catalogue.ts:72-75` (array), `src/data/fertility-journey.ts:459-539` (cards). Patch: append 9 entries, e.g.
`{ id: 'fertility-development-survival', family: 'fertility', title: 'Development (survival) model', question: '…', method: 'Model variant · Python bundle', format: 'Code & data download', href: 'research/fertility/fertility-research-full.zip' }` ×9 (titles/ids taken from the journey cards). Update `familyInfo.fertility.description` (`:139`) to “Nine exploratory model variants across six economies…”.

**D2 — Education count contradiction.** `src/data/education-journey.ts:48` vs `:416` vs card `:592`; `src/data/model-catalogue.ts:112`. Patch (preferred, smaller): amend `:48` to “…plus four stored massification experiments and one DHS replication package. Each gets a model card…” and keep `:416` for the catalogue-facing rule. If the DHS is not meant to be a model, delete card `:592-600` and entry `model-catalogue.ts:80` instead.

**D3 — DHS id/family/link mismatch.** `model-catalogue.ts:80` id `shadow-dhs`, family `education`; `model-catalogue.ts:187` shadow research link; `education-journey.ts:592` id `credential-dhs`. Patch: rename to `credential-dhs`; move the object literal from the `shadow` array (`:77-81`) into `education` (`:26-34`); replace the shadow research link at `:187` with an education one (or drop it).

**D4 — format taxonomy.** `model-catalogue.ts:11` (type), `:13` (`external` helper hard-codes `'Classic workbench'`), plus entries `:79, :85, :89-92, :97-98`; render `Library.tsx:18`; filter `Library.tsx:53,221`. Patch as §1 D4. Minimum viable: change `:13` to accept a format parameter and pass per call; add `'Code & data download'` value.

**D5 — “Every model, searchable”.** `Library.tsx:188,210`. Patch wording to “Every catalogue entry, searchable.” (both occurrences).

**D6 — Badge/card mismatch.** `site-status.ts:21` remove `'teaching'`; `site-status.ts:22` remove `'checked'`. Verified by script: education cards purposes = {mechanism}; systems cards states = {developing}.

**D7 — Stale second catalogue.** `Navigation.tsx:105`, `Catalogue.tsx:46`, content `src/data/model-catalogue.md`. Patch: header wording (§1 D7), and retitle the nav button “Research catalogue” → “Research build queue” if the page is kept.

**D8 — meta description.** `index.html:6`. Exact current string: `Interactive research models for education, ecology and political economy. Change assumptions, compare outcomes and inspect the evidence.` Suggested: `Research models for education, population, history and political economy — interactive workbenches plus downloadable code and data. Change assumptions, compare outcomes and inspect the evidence.`

**D9 — browser claim attached to count.** `Navigation.tsx:120-121`. Patch: conditional render (preferred) or “Interactive entries run in your browser”.

**D10 — deephistory over-count.** `model-catalogue.ts:84-86`. Patch: format `Code & data download` + exclude downloads from `familyCounts`/`totalModels` (with D4).

**D11 — politics versions.** `model-catalogue.ts:88-93`, `ccp-journey.ts:24,33,42,51`. Patch: format `Code & data download`; add “(1 model, 4 versions)” to `familyInfo.politics.description` (`:154`) or to each title suffix.

**D12 — angkor grouping.** `model-catalogue.ts:65-70` vs `angkor-journey.ts:134,173,205`. Patch: `guided = ['provisioning','campaign','angkor','signalling','obligations','monsoon','maintenance','relocation']`, `further = ['mandala','accounts','institutions','flight','petri']`.

**D13 — extension artefacts/titles.** `model-catalogue.ts:95-100`; `extension-journey.ts:262,272,282,292`. Patch: align four titles; format `Code & data download` ×2 / `Narrated journey` ×2; note shared bundle in `question`.

**D14 — dead narrative layer.** `App.tsx:25,61` (only use = title); `StoryPage.tsx:35` (export, never imported); `family-stories.ts` whole file. Patch: delete both, or route. Not urgent for launch, but it is 400+ lines of unreachable copy that can drift.

**D15 — About claims.** `about.ts:20` “Each has a declared purpose.” → “Every narrated model has a declared purpose; download-only entries carry their purpose in the bundle README.”; `about.ts:28` “Every model can be downloaded, run on your own machine and changed.” → “Every model’s code can be downloaded and run on your own machine.”; `workflow` §“The scientific process underneath” `about.ts:81` “labelled as failed” → “labelled as a historical or limited result” (no `failed` value exists in `stateLabel`, `angkor-journey.ts:30-35`); `about.ts:9` “The code, available data, assumptions and current limitations are shared.” → add “in the bundles’ README or FINDINGS files” or, if not true for `ccp-bus-v1.zip`, leave as “as available”.

**D16-L — planning semantics.** `model-catalogue.ts:105` comment (“toolkit is methods, not models”) vs 12 entries in `totalModels`; `:129` “Twelve independent implementations” — not verified from repo. Suggested: “Twelve planning tools (six Atlas worlds, six classic implements) in the IIEP/UIS tradition.”

**D17-L — other wording/consistency nits found, low value:**
- `model-catalogue.ts:4` family order vs `familyGroups` (`:106-110`) order differ; menu groups are a different taxonomy from the library sections. Not wrong, but two orderings.
- `site-status.ts:6` `family: ModelFamily | 'politics'` — `'politics'` is already in `ModelFamily`; simplify to `ModelFamily`.
- `model-catalogue.ts:73` fertility lab `method` “Exploratory lab · six economies” while journey calls it a page of 9 models; align wording.
- `angkor-journey.ts:219` `mandala` card has no `engine`/`research` key (other 12 do). Add `research: 'reference/mandala/model_card.json'` if that file is the record.
- Extension catalogue links `research/field-schools/README.md` and `VALIDATION.md` from `familyResearch` (`:201-204`); both exist — good, leave.

---

## 4. What I verified as sound (avoid over-correcting)

- **22/22 live worlds are catalogued.** `internal()` lookups resolve for all 22 `AtlasWorldsLab.worlds` on `c3cc71c`; no unmapped live model. (`models/worlds.js` 18 + `institution-worlds.js` 4.)
- **All catalogue href/route targets exist** under `public/` (script checked every entry: 0 missing files); all journey `engine`, `research` and `sources` links resolve, including `research/shadow-education` in the GitHub repo (verified via `gh api`).
- **All 63 journey cards carry a valid `purpose` and `state`** and are referenced by a chapter or `deeper` list (no orphan cards).
- **“2 languages”** in `Navigation.tsx:120` is **correct**, not a bug: `Language` has 4 values but the selector exposes English + 简体中文 only, and `check-react.cjs` explicitly keeps English + Chinese mandatory (vi/fr best-effort). Do not “fix” this.
- **`check-react.cjs`'s “four languages”** is a render-robustness test, not an advertising claim.
- **`home-explainer.ts:84`** (“Interactive workbenches run in your browser, while downloadable Python models run on your own machine, and the two are different things”) is the right qualification and the model for other copy; the defect is that the catalogue `format` badge contradicts it (D4).
- **`about.ts:9`** (“Draft papers are being added; public availability does not imply peer review”) is a good existing qualifier — keep.
- **Massification 4 entries → 1 page** and **4 angkor lab worlds → 1 engine** are deliberate multi-experiment interfaces, not duplicate counting; do not “fix”.
- `classicLabs` (“…rather than inflating the count”, `Library.tsx:242`) is defensible: the three standalone labs are outside `catalogue`/`totalModels`, even though two of them (Original Angkor Atlas, Angkor Mandala Lab) expose models also reachable as catalogue worlds (`angkor`, `mandala`).

---

## 5. Claims audit — exact quotes and minimal suggested wording

Scope: `about.ts` (about / howModelsWork / workflow), `home-explainer.ts`, homepage copy (`Library.tsx`, `Navigation.tsx`, `site-status.ts`, `index.html`).

### 5.1 Blanket “published” claims

| File:line | Exact quote | Problem | Suggested minimal wording |
| --- | --- | --- | --- |
| `src/components/Catalogue.tsx:46` | `Browse published mechanisms, rival explanations and the proposed build queue.` | The page renders the Nov 8 markdown build queue whose own note says “awaiting verification”; none of its 18 rows is marked Live, so “published” is a blanket claim over unbuilt/proposed entries. | `Browse candidate mechanisms, rival explanations and the proposed build queue.` |
| `src/data/about.ts:20` | `Each has a declared purpose.` | True for the 63 journey cards; not true for the 56 catalogue entries — `CatalogueItem` (`model-catalogue.ts:5-15`) has no `purpose`/`state` field, and 10 cards/models (9 fertility + shadow research track) have no catalogue entry at all. | `Every narrated model has a declared purpose; download-only entries state theirs in the bundle README.` |
| `src/data/about.ts:81` (workflow) | `Models that fail a test stay on the site, labelled as failed.` | There is no `failed` value in `stateLabel` (`angkor-journey.ts:30-35`: checked/developing/historical/evaluated). Nothing is labelled “failed”. | `Models that fail a test stay on the site, labelled as a historical or limited result.` |
| `src/data/site-status.ts:11` | `Some models implement findings from peer-reviewed studies. Some explore what would follow if a mechanism held.` | **Sound** — non-blanket, matches the `published` purpose used by exactly one card (`provisioning`). Keep. | — |
| `src/data/home-explainer.ts:74` | `Some models implement results from peer-reviewed studies. Others explore what would follow if a mechanism held, or exist to teach an idea. These are marked differently.` | **Sound.** Keep. | — |

### 5.2 Blanket “browser-executed” / “downloadable” claims

| File:line | Exact quote | Problem | Suggested minimal wording |
| --- | --- | --- | --- |
| `src/components/Navigation.tsx:120-121` | `{n} catalogue entries · 2 languages` / `Runs locally in your browser` | On home and catalogue routes there is no active world, yet the browser claim sits under the 56-entry count. 10/56 entries are Python zip downloads, 3 are static write-ups, 2 are narrative entries that do not “run in your browser”. | Wrap in `{activeWorld && …}`, or change to `Interactive entries run in your browser`. |
| `src/components/Library.tsx:210` and `:188` | `Every model, searchable.` | Not every model is in the catalogue (9 fertility models, 1 shadow research track); and “model” conflates bundles/write-ups with models. | `Every catalogue entry, searchable.` |
| `index.html:6` | `Interactive research models for education, ecology and political economy.` | “Interactive” is blanket over a catalogue that includes 10 downloads; “ecology” is not a family (legacy Angkor chapter title, still in `translations.json`/`cards.json`); only 3 of 9 families named. | `Research models for education, population, history and political economy — interactive workbenches plus downloadable code and data.` |
| `src/data/about.ts:28` + `src/data/site-status.ts:28` | `Every model can be downloaded, run on your own machine and changed.` / `…modified.` | Repeated verbatim in two surfaces. Downloads are Python zips (runnable), but 2 entries are historical narrative cards and 10 entries are bundles, not models; “every model” is doing more work than the inventory supports. | `Every model’s code can be downloaded and run on your own machine.` (Both locations.) |
| `src/data/home-explainer.ts:84` | `Interactive workbenches run in your browser, while downloadable Python models run on your own machine, and the two are different things.` | **Sound in itself**; it is contradicted by the catalogue’s `format` badge (all downloads say “Classic workbench”). Fix D4, do not weaken this sentence. | — |
| `src/components/Library.tsx:194` | `Most interactive models run in your browser; downloadable Python models run on your own machine.` | **Sound** (“Most”, explicitly two categories). Keep; model for other copy. | — |

### 5.3 Badge wording vs card evidence (family badges)

| File:line | Exact quote (badge arrays) | Evidence | Suggested patch |
| --- | --- | --- | --- |
| `src/data/site-status.ts:21` | education `purposes: ['mechanism', 'teaching']` | All 8 education cards: `mechanism`. Zero `teaching`. | `purposes: ['mechanism']` |
| `src/data/site-status.ts:22` | systems `states: ['checked', 'developing']` | All 9 systems cards: `developing`. Zero `checked`. | `states: ['developing']` |

All other seven family badges match the union of their cards exactly (verified by script: angkor, planning, fertility, shadow, deephistory, politics e.g. politics `checked/developing/evaluated` ✓, extension `developing/historical` ✓).

---

## 6. Not verified from repo (do not assert in public copy)

1. Whether the 9 fertility Python models reproduce their stated findings — code is in a zip; no test harness in repo.
2. Whether `ccp-v1/v3/v6/v7` are genuinely distinct model versions (different file sizes and contents; semantics not inspected).
3. Whether the 6 Atlas planning worlds and 6 classic-app planning tools are “independent implementations” (`model-catalogue.ts:129`) — no shared spec/test comparison found.
4. Whether every bundle’s “current limitations” are documented: `ccp-bus-v1.zip` has no README/FINDINGS; `credential_floor_dhs.zip` has `FINDINGS.md` but no README.
5. DOI/Zenodo issuance claims (`about.ts:28`, `site-status.ts:35`, `:30`) — no DOI file for the current release found beyond `docs/DOI.md`; “will be displayed when issued” is fine.
6. External GitHub links (issue templates, `CITATION.cff`, `LICENSE.txt`) were not fetched; only in-repo relative targets were verified.

---

## 7. Reproduction commands (read-only)

```bash
export PATH=/opt/homebrew/bin:$PATH
cd fleet.nosync/wt-audit
node scripts/check-angkor-journey.mjs        # PASS
node scripts/check-react.cjs                 # PASS

# Journey card inventory (Node 26 strips TS types natively)
node --input-type=module -e "
const files=['angkor','education','systems','planning','fertility','shadow','deephistory','ccp','extension'];
for (const f of files){const m=await import('./src/data/'+f+'-journey.ts');
 const j=m[Object.keys(m).find(k=>k.endsWith('Journey')||k==='journey')];
 console.log(f, j.family, Object.keys(j.models).length, Object.values(j.models).map(c=>c.purpose+'/'+c.state).join(','));}
"

# Live world inventory (22)
node --input-type=module -e "
const order=['atlas_data','youth','camchild','lab_models','angkor-model','campaign','signalling','obligations','monsoon','relocation','petri','provisioning','evidence','worlds','institution-data','institution-worlds'];
for (const f of order) await import('./src/models/'+f+'.js');
console.log(globalThis.AtlasWorldsLab.worlds.map(w=>w.id).join(' '));"
```

Counting `model-catalogue.ts` directly is awkward because `./src/models` imports `source-hashes.json` without an import attribute; the catalogue was imported by stubbing its two value imports (`worlds`, `schoolFutures`) outside the worktree, no files changed.

---

## 8. Suggested dispatch order for the Lead

1. D4 + D1 + D5 together (one catalogue change set) — fixes the largest user-visible count/coverage problem.
2. D2 + D3 (education/DHS consistency) — one small data edit, plus translation keys for any changed visible strings.
3. D6 + D9 + D8 (badges/claims) — copy-only, cheap, high credibility impact.
4. D7 (stale catalogue route) — decide product question: keep as “build queue” or retire; copy fix at minimum.
5. D10/D11/D12/D13 — labelling/count semantics, safe after D4 lands.
6. D14/D15/D16/D17 — cleanup batch.

Any change to `model-catalogue.ts` titles/questions/methods must be mirrored into `src/data/translations.json` or `check-react.cjs` will fail on missing translation entries; the accepted plan should run both check scripts plus the catalogue import before merge.

---

## 9. Post-fix status — `fix/model-coverage` (19 Nov 2026, for Lead dispatch)

Applied on branch `fix/model-coverage` (off main `01e13e4`), one commit per fix, PR opened against main and **not merged**.

| Fix | Status | What changed |
| --- | --- | --- |
| D4 format taxonomy | **done (data only)** | `CatalogueItem.format` widened with `'Write-up' \| 'Code & data download' \| 'Narrated journey'`. 10 zip entries → `Code & data download`, 3 report pages → `Write-up`, 2 historical cards → `Narrated journey`. No Library.tsx edit: `ModelLink` already renders `t(item.format)`, so badges change automatically and the existing “Classic workbenches only” filter now excludes non-workbenches. zh-Hans added for the 3 new values. |
| D1 fertility coverage | **done** | 9 fertility entries added using the journey card ids/titles (`development-survival` … `momentum-test`), short questions from each card note, one shared method string, href to `fertility-research-full.zip`. Fertility 2 → 11 entries (9 models + lab write-up + bundle); `totalModels` 56 → 65; family count and search wired automatically. 19 zh-Hans strings added. |
| D5 searchability claim | **partial** | The substantive gap is closed (every fertility model is now searchable). The literal promise `Every model, searchable.` remains in Library.tsx, which this pass must not edit — exact TODO below. |
| D8 blanket claims | **done** | `index.html` meta description (no more “ecology”, no blanket “Interactive”, names 4 areas + notes downloads); `about.ts` and `site-status.ts` “Every model can be downloaded, run…” → “Every model’s code can be downloaded and run…”; `about.ts` workflow “labelled as failed” → “labelled as a historical or limited result”. |

**Superseded counts in §0/§1/§2:** after D1 the catalogue is **65 entries** (fertility 11), not 56/2. The per-family matrices in §2 remain the `c3cc71c` audit record; only fertility's entry count changed.

### TODO for the Library pass (Kimi PR #13 overlap; do not edit these files on `fix/model-coverage`)

1. **`src/components/Library.tsx:188` and `:210`** — change `Every model, searchable.` → `Every catalogue entry, searchable.` After D1 the only journey card still without a catalogue entry is the shadow `research-folder` research track (not a model), so “every model” is now nearly true; “every catalogue entry” is exactly true.
2. **`src/components/Library.tsx:53` + `:221`** — predicate `item.format === 'Classic workbench'` is now finally correct (only the 13 iframe entries + 4 massification tabs pass; downloads, write-ups, narrated cards no longer leak in). If the label is retouched, prefer `Classic workbenches only` → `Classic iframe workbenches`; no semantic fix is needed in code.
3. **`src/components/Library.tsx:18`** — no change required for correctness. Optional polish: show a different arrow/icon for `format === 'Code & data download'` so a download is distinguishable from a write-up at a glance (today both use `ArrowUpRight`).
4. **`src/components/Navigation.tsx:120-121`** — D9: render `Runs locally in your browser` only when `activeWorld`, or change the string to `Interactive entries run in your browser`. Deferred because Navigation.tsx is in the avoided write set.
5. **Dictionary consolidation (optional)** — the 19 new fertility strings + 3 format strings were appended to `src/data/translations.json` (allowed file) because `src/data/ui-translations.json` (where the other catalogue strings live) is in Kimi's write set. When the two dictionaries are consolidated, move them to the same place; `i18n.ts` merges both today, so nothing is broken meanwhile.
6. **Still deferred from the audit:** D2 (education count contradiction), D3 (credential-floor triple-classification), D6 (`site-status.ts:21` education badge claims `teaching`; `:22` systems badge claims `checked`), D7 (stale markdown catalogue reachable from nav), D9 (above), D12–D14. D4's data change also makes D10/D11 label fixes cheap; they were left out of scope deliberately.

### Verification for this fix set

`npm run build`, `node scripts/check-react.cjs`, `node check-translations.cjs`, `node test-worlds.cjs`, `node scripts/check-angkor-journey.mjs` — results recorded in the PR description; all must pass before push.
