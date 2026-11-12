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
