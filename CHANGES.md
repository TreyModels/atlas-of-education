# Changes · 19 November 2026 · Atlas Worlds launch, nine journeys, DOIs, design system

## Rename and releases
- Renamed **Atlas of Education** to **Atlas Worlds** (PR #14): brand, page titles, manifest, CITATION, Zenodo metadata, README and licence notice.
- Re-cut release **v2026.11.19** on the renamed main, then released **v2026.11.20** after the design and catalogue integration. First Zenodo DOIs recorded: concept 10.5281/zenodo.24369167, v2026.11.19 = 10.5281/zenodo.24369168, v2026.11.20 = 10.5281/zenodo.24369385.

## Nine narrated journeys and homepage
- All nine families have narrated journeys: Angkor, Shadow education, Political economy, Farmer field schools, Fertility, Deep history, Education planning, Education and work, School systems.
- Expanded homepage explaining the research questions, founder background, AI-assisted implementation, evidence, assumptions, negative findings and contribution process.
- About, How Models Work and My Digital Workflow pages.
- Catalogue and legacy story pages aligned to the journey design (PR #11).

## Design system (Kimi)
- Global shell and responsive article presentation (PR #9).
- Grouped rail and mobile navigation by research family, surfacing About, How Models Work and My Digital Workflow; workflow links added (PR #13).
- English and Simplified Chinese selector; classic workbenches retain their original language.

## Model coverage and honesty fixes
- Fertility family now lists all 11 model variants; catalogue grows from 56 to 65 entries.
- Download bundles and write-ups carry real format labels; blanket download and label claims qualified; precise claims wording (PR #15).
- Model-level coverage, live-site and research-archive audits added under `docs/`.

## DOI wiring
- Concept DOI 10.5281/zenodo.24369167 recorded in CITATION.cff, the site footer, the licence line, the About page, README and `docs/DOI.md`.
- v2026.11.19 notes updated with its version DOI; v2026.11.20 minted as version 2 under the same concept DOI.

## Hashtag search and tag index
- Every catalogue entry now carries curated hashtags (Latin in every language) alongside automatic family and kind tags (PR #23).
- Find-a-model and the Library search accept `#tag` queries: exact, prefix or substring match, several tags ANDed, mixed freely with plain words; ordinary keyword search still works.
- The tag-index update (PR #26) adds a plain-language broad layer: 16 discipline tags and 25 everyday topics (41 broad tags), plus 45 specific and 10 type/status tags. All 65 models are re-tagged with 6–9 tags (average 7.74), every model carries a discipline tag, and no entry is findable only through jargon.
- A grouped tag browser shows Broad topics first with counts, then specific and type/status tags; suggested tags appear in the search modal, and chips on catalogue cards and in the workbench header open a pre-filled search.
- Tags are filters over the existing 65 entries, not new models; totals are unchanged.

## Link destinations: pages first, downloads explicit
- Fixed a click-path bug reported from the live site: 19 catalogue entries (the 9 fertility model variants, the fertility research bundle, both Shadow education bundles, the Out of Africa bundle, the four Political economy/CCP bundles and the two Farmer field schools bundles) pointed their primary link straight at a ZIP, so clicking a model started a download.
- Catalogue entries now open a page (the model's journey or research page) as their primary action; the file moved to an optional `downloadHref` rendered as a separate, explicitly labelled "Download code & data" control. Search results and hashtag-filtered results follow the same rule, so a tag → result → model click always lands on a page.
- Journey model cards label their code link "Download code" and carry the `download` attribute.
- New guard `scripts/check-link-destinations.cjs` (wired into `scripts/check-all.sh` and `npm test`) fails if any catalogue entry's primary link is a file, if a download lacks a page target, or if a download page/file is missing.
- Browser click audit: 66/66 catalogue entries open pages, 19/19 secondary downloads fire only from the labelled control, and `#fertility` search results open `#story-fertility` instead of downloading.

## Workbench model cards
- Every workbench page now opens with a model card before the controls: purpose and development-state badges (from the same labels used on the family journeys), what you are looking at, why the model exists, how far it has been checked, what it does not show, engine version, a link to the family journey, the evidence section and clickable tags.
- The card reuses the journey model cards via `src/data/journey-models.ts`, so the workbench and the family story cannot drift apart. Model version display drops the historical "Atlas of Education" prefix; the raw historical label remains in the evidence panel and exported run JSON.

## Validation
Validation: all nine journey/link checks, link-destination checks, React/translation checks, 52 model tests, production build and 22-model worker parity. Desktop/mobile browser checks completed. These checks establish implementation behavior, not empirical validity of every model.

# Changes · 8 November 2026 · Education-first restructure

## Library and navigation
- The front page is the Atlas of Education: education and employment models first
  (China graduate queue, Cambodia school and work, credential floor), then the
  Planning Lab, then Angkor as one case-study section with its guided sequence and
  all 13 models listed.
- Navigation families: Education & employment · Planning Lab · Angkor case study.
  The model dropdown keeps four groups. Header brand reads "Atlas of Education".
- A credential-floor card was added; the full Education Atlas is linked from the
  Planning Lab section.

## Cambodia: all policy levers
- All 13 CamChild levers are now controls, in three groups: paying for school
  (attendance cash, unconditional cash, ending teacher-sold tutoring, debt relief),
  what school offers (safety, meals, support for children of migrants, harvest
  timetable, bridging classes), and work, credentials and migration (factory
  enforcement, Grade 12 credential floor, Phnom Penh teen wages, Thailand route).
- Results average matched seeds (1, 4 or 8 histories; default 4) with a range band.
  "No programmes" keeps the same seeds and Thailand route, as CamChild.compare does.
  More results: attendance, poorest and richest fifth, rural and Phnom Penh,
  children of migrants, teens working away, cost per child-year avoided.
- The engine file camchild.js is unchanged.

## Planning Lab: five tools brought into the React app
Ported from the full Atlas's tool definitions with the same inputs, defaults and
AtlasLab engine calls (lab_models.js unchanged): reconstructed cohort, sector
simulation, school mapping, learning-adjusted years, graduate absorption.

## Interface fixes
- Whole-number x-axis ticks for annual, grade and count series (no "2027.75").
- Optional axis titles and zero baselines; a fourth line colour.
- Export and inspect chart links are separated.
- Comparison cards at the reference run say "Reference run. Change a control to
  compare." instead of a bare 0.
- Deployment repair: phones retain the introduction and show controls before results.
- Chinese headline line-height fixed.
- Removed the unused Vite starter page, hooks and UI component kit.

## Provenance and tests
- public/evidence.js now declares the new worlds.js hash; src/models re-synced.
- Control audit regenerated: every control in all 22 models changes displayed output.
- Translations added for all new text in Chinese, French and Vietnamese.
- Test counts updated from 17 to 22 models. All checks pass: test-worlds (52),
  check-translations, check-react, check-worker, check-run-lifecycle, check-repairs.

## Build note
dist/ was rebuilt offline with esbuild because packages could not be installed in
the editing environment. The CSS reuses the previously compiled Tailwind output plus
src/education.css. Run `npm ci && npm run build` to rebuild with Vite and the
TypeScript check.

## Deployment validation
Rebuilt with TypeScript and Vite in the deployment workspace. All 52 model tests, 22-model worker parity checks, React translation/render checks, worker lifecycle and repair regression checks passed.

## 2026-11-10 · Fertility collapse lab
- New research page `research/fertility.html` (English and Simplified Chinese; `?lang=zh` opens in Chinese):
  - four-act summary;
  - six-place chart of observed TFR against the held-out development and three-layer models;
  - in-browser cohort mechanism lab (JS port of `unified_suite.cohort`, checked against Python: 2.24/1.28/1.69 vs 2.21/1.25/1.67);
  - tipping/hysteresis lab;
  - claims held vs ruled out;
  - policy levers;
  - downloads.
- New files under `research/fertility/`: `fertility_research.zip` (scripts, data, findings) and `fertility-series.json`.
- Research library: new "Fertility collapse lab" entry.
- Navigation: new "Fertility collapse lab" link under Resources, added in `src/components/Navigation.tsx` and in `ui-translations.json` (zh-Hans, fr, vi).
- `dist/` patched directly (no `npm ci` available offline): the same link and translation were added to `assets/index-CHs6Ab8Q.js` and the static files were copied. A full `npm run build` should be rerun before publishing.
- Not published or deployed.

## 2026-11-10 · Shadow education lab
- New research page `research/shadow-education.html` (English and Simplified Chinese). It covers the Cambodia tutoring ABM:
  - three rival explanations;
  - fit to Bray et al.'s seven patterns, plus fresh-world refit shares;
  - a policy explorer covering the four policies × three explanations, with medians and 5–95% ranges;
  - the DHS 2021–22 credential-floor test;
  - a claims ledger;
  - limits and downloads.
- New files under `research/shadow/`: `tutoring_abm.zip` (model, calibration, results, fresh-world reruns) and `credential_floor_dhs.zip`.
- Research library: new entry.
- Navigation: new "Shadow education lab" link. It is in the source and `ui-translations.json` (zh-Hans, fr, vi) and is patched into the built bundle.
- Not published or deployed. Rerun `npm run build` before publishing.
