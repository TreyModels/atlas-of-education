# Angkor journey: design (19 Nov 2026)

## Intent

Make the Angkor family page the first complete *narrated* model family, and the template for the others. A reader follows one route: why model this → what the published study found → how we turned evidence into rules → what the experiments show → what is still weak → get the code. First viewer: James Hutson (Lindenwood Applied AI Innovation Center), 23:00 Asia/Shanghai, 19 Nov.

Guiding stance: KIDS (Edmonds & Moss, "From KISS to KIDS") — descriptive complexity where the evidence justifies it, every model with a declared purpose and scope. Honesty about development state is a feature, not a disclaimer.

## Goals

1. **Klassen et al. (2022) front and centre.** Chapter 1 is the peer-reviewed foundation: Y = Y₀N^β, β = 1.227 (SE 0.023) vs 7/6 and 1; distance-to-Bayon slopes; temple-volume elasticity 0.085; Table 4B buildup 93 → 571 communities. Interactive β comparison is the centrepiece. Boundary kept visible (wording from `provisioning.html`): the output index is an archaeological proxy, not rice tonnage; distance slopes are separate associations; 0.085 is not a surplus share; using β as a dynamic harvest multiplier is *our* hypothesis.
2. **Extensions as labelled chapters**, in this order: campaign logistics → growth & the integrated Angkor world → authority/signalling → obligations & court exit → climate (monsoon). Further experiments (Petri, relocation, maintenance, institutions, flight, accounts, mandala) appear as a "deeper experiments" grid. Each chapter: question · evidence · rule we wrote · experiment & result · limitation · "how the maths works" (plain words, symbols, one small worked example where cheap).
3. **Two separate labels on every model card**: *purpose* (published foundation / mechanism exploration / teaching / description-accounting) and *state* (implementation checked / in development / historical result / empirically evaluated). No "publication ready" from passing tests.
4. **Fix the stale Petri result.** Regenerate the provisioning-page Petri table under reviewed defaults (coordination 1, water floor 0; drought: 66.5% retained, gap 4.402) or show the old table explicitly labelled as a historical run, and rewrite the interpretation (the coordination knockout no longer demonstrates the old effect).
5. **Code and contribution**: each card links to its engine file and the repo; "Propose a version" opens a GitHub issue template asking for fork URL, base commit, what changed, how to reproduce, evidence.
6. **Story first; sliders only at "watch this" moments.** The page is read, not operated. Interaction appears only where changing one variable teaches something: tonight the β comparison in chapter 1, and at most one more (Petri coordination/water-floor before/after). Other models are reached through links to their existing workbenches, not embedded controls.
7. **Division of labour: Kimi owns all visual/UI design.** Claude delivers the content model, narrative copy, data, a functional and accessible page with minimal semantic styling (stable class names), and a Kimi brief (structure, components, content constraints, what must not change). Kimi restyles. Structural needs Kimi may design: sticky chapter index, narrative + figure layout, expandable source notes, claim-type distinction (published / simulated / open).

## Non-goals (tonight)

- Login (Apple/Google) or direct uploads. GitHub links only.
- Restructuring the other six families (they keep `StoryPage`; Angkor becomes the template).
- New experiments or re-estimation from archaeological records.
- Visual polish by Claude. Kimi does it from the brief.
- Full Chinese/Vietnamese translation of new copy (English first; strings go through `t()` so they can be translated later).

## Anti-goals

- Presenting Atlas extensions as if they came from the paper.
- Showing pre-review numbers next to reviewed code without a version label.
- Categorical language ("ruled out", "proves") beyond what an experiment's design supports.

## Constraints

- Build on `feat/research-track` merged with Codex's `integrate/research-rigor-2026-11-19` (five known conflicts; resolve `public/evidence.js` first, regenerate React copies and hashes with repo scripts, merge translations by key).
- Existing checks must still pass: `test-worlds.cjs`, `check-translations.cjs`, `scripts/check-react.cjs`, `npm run build`, `scripts/check-worker.cjs`.
- No engine equation changes. Merging to `main` deploys via GitHub Pages — only with Trey's go-ahead. Work goes up as a PR.

## Approaches considered

1. **Rebuild the Angkor family page inside the React app** — chosen (Trey via Codex). Reuses navigation, i18n, workbench links; becomes the template.
2. Standalone static page under `public/research/angkor/` — faster, but outside app navigation and not reusable.
3. Kimi designs first — best polish, too slow for 23:00; becomes round two.

## Decided how

- New component `AngkorJourney` served at the existing `story-angkor` route (other families unchanged). Content lives in `src/data/angkor-journey.ts`, typed so other families can adopt the same shape.
- β chart: client-side, plotting per-person index 100 × (N/100)^(β−1) for β ∈ {1, 7/6, 1.227 ± 1.96·SE}, community-size slider.
- Numbers on the page come from repo result files (paper tables, `experiments/angkor-review/results`, family-stories figures already reviewed), each with a source note.

## Left to the builder

Visual treatment (Kimi); which chapters get a worked example tonight (Klassen and campaign at minimum); copy edits for length.
