# Angkor Journey Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A narrated Angkor family page (Klassen et al. 2022 first, Atlas extensions as labelled chapters) inside the React app, plus the Petri correction, a contribution path and a Kimi brief, on a branch that also carries Codex's research integration.

**Architecture:** Typed content in `src/data/angkor-journey.ts` rendered by a new `AngkorJourney` component at the existing `story-angkor` route; one pure helper for the scaling maths; a node check script validates the content. Styling is minimal and semantic; Kimi restyles from `docs/kimi-brief-angkor.md`.

**Tech Stack:** React 19 + TypeScript + Vite (existing), plain CSS, Node check scripts (repo convention, no test framework).

**Spec:** `docs/superpowers/specs/2026-11-19-angkor-journey-design.md`

## Global Constraints

- Branch `angkor-journey` from `origin/feat/research-track`, merged with `origin/integrate/research-rigor-2026-11-19`. PR to `main`; never merge to `main` without Trey.
- No engine equation changes.
- Klassen values verbatim: β = 1.227, SE 0.023, comparators 7/6 and 1; distance slopes −0.846 (output/ha), −0.409 (reservoir/ha), +0.521 (land/person), normalized 100 at 10 km from Bayon; temple-volume elasticity 0.085; Table 4B 93/192/380/511/568/571 communities.
- Boundary sentences kept: proxy not rice tonnage; distance slopes separate associations; 0.085 not a surplus share; β as dynamic harvest multiplier is our hypothesis.
- Purpose ∈ {published foundation, mechanism exploration, teaching, description/accounting}; State ∈ {implementation checked, in development, historical result, empirically evaluated}. Separate fields.
- Sliders only at "watch this" moments (β comparison tonight).
- All user-facing strings go through `t()`.
- Existing checks keep passing: `node test-worlds.cjs`, `node check-translations.cjs`, `node scripts/check-react.cjs`, `npm run build`, `node scripts/check-worker.cjs`.

## Review Focus

- β slider at extremes (N = 10, N = 2000): index finite, monotone in N for β > 1, flat for β = 1 → covered in Task 3.
- Narrow mobile viewport (375 px): chapter index must not cover text; page readable in one column → Task 4 manual check.
- Missing translation key: `t()` falls back to English without throwing → check-translations run in Task 6.
- Links to engines/research files that do not exist in `public/` → Task 2 check script fails on any broken link.
- Old numbers shown beside reviewed code: Petri table must state its defaults → Task 5 asserts page text.

---

### Task 1: Integrate the two branches

**Files:** conflicts in `research/README.md`, `public/evidence.js`, `src/models/evidence.js`, `src/models/source-hashes.json`, `src/data/ui-translations.json`.

- [ ] Create branch `angkor-journey` from `origin/feat/research-track`; `git merge origin/integrate/research-rigor-2026-11-19`.
- [ ] Resolve: `research/README.md` keeps the newer purpose-specific workbench explanation, links research projects and teaching beneath it, no unqualified categorical verdicts. `public/evidence.js`: keep both sides' amendments (credential/forecast from research-track, engine hashes from integrate). `ui-translations.json`: union by key. Then regenerate `src/models/*` with `python3 scripts/sync-react-models.py` and hashes with `scripts/repin-hashes.py` as needed.
- [ ] Run the five global checks. Expected: all pass.
- [ ] Commit "Merge research-rigor integration into research track".

### Task 2: Journey content model and check

**Files:** Create `src/data/angkor-journey.ts`, `scripts/check-angkor-journey.mjs`.

**Interfaces — Produces:**
```ts
export type Purpose = 'published' | 'mechanism' | 'teaching' | 'accounting'
export type DevState = 'checked' | 'developing' | 'historical' | 'evaluated'
export type Claim = 'published' | 'sim' | 'open' | 'method'
export interface Para { claim?: Claim; text: string }
export interface ModelCard { id: string; title: string; purpose: Purpose; state: DevState; note: string; engine?: string; route?: string }
export interface Chapter { id: string; kicker: string; title: string; question: string; evidence: Para[]; rule: Para[]; result: Para[]; limitation: Para[]; maths?: { plain: string; formula?: string; example?: string }; sources: { label: string; href: string }[]; models: string[]; interactive?: 'beta' }
export const journey: { title: string; lede: string; why: Para[]; chapters: Chapter[]; deeper: string[]; models: Record<string, ModelCard>; bottomLine: string }
```
- [ ] Write `check-angkor-journey.mjs` (imports the TS via a tiny esbuild/tsx transform or by reading compiled JSON — use `npx tsx`) asserting: chapter 1 id `klassen` with `interactive: 'beta'`; chapter order `klassen, campaign, growth, signalling, obligations, climate`; every chapter has ≥1 evidence, rule, result, limitation; every `models[]` id exists in `journey.models`; every card has valid purpose and state; every `engine` / source href that is relative resolves to a file under `public/`; the four boundary phrases ("not measured tonnes of rice" or equivalent proxy phrase, "separate associations", "not … surplus share", "our hypothesis") appear in chapter 1.
- [ ] Run → fails (file missing).
- [ ] Write content from `provisioning.html`, `model-stories.json`, `family-stories.ts` (angkor), `experiments/angkor-review/README.md`, Codex math handoff format. Cards for: provisioning, campaign, angkor, signalling, obligations, monsoon, petri, relocation, maintenance, institutions, flight, accounts, mandala.
- [ ] Run → passes. Commit.

### Task 3: Scaling helper

**Files:** Create `src/lib/scaling.ts`; extend the check script.

**Produces:** `perPersonIndex(n: number, beta: number): number` = 100 × (n/100)^(β−1).

- [ ] Assertions: `perPersonIndex(100, 1.227) === 100`; `perPersonIndex(500, 1) === 100`; `perPersonIndex(500, 1.227)` ≈ 144.1 (±0.1); strictly increasing in n for β = 1.227 over n ∈ {10, 100, 2000}; finite at n = 10 and 2000.
- [ ] Implement; run; commit.

### Task 4: AngkorJourney component and route

**Files:** Create `src/components/AngkorJourney.tsx`, `src/components/BetaExplorer.tsx`, `src/journey.css`; modify `src/App.tsx` (render `AngkorJourney` when `storyFamily === 'angkor'`, else `StoryPage`).

**Consumes:** `journey`, `perPersonIndex`.

- [ ] `BetaExplorer`: one range input (community size 20–1000, step 10), shows per-person index for β = 1, 7/6, 1.227 and the 95% band (1.227 ± 0.045) as numbers plus a small SVG line chart over n ∈ [20,1000]; caption carries the proxy boundary sentence.
- [ ] `AngkorJourney`: hero (title, lede, why), sticky chapter nav (anchor links, `aria-current` via IntersectionObserver, disabled under `prefers-reduced-motion` smooth scroll), chapters with sections Evidence / Rule we wrote / What the experiment shows / Limits / How the maths works (`<details>`), sources, model cards (purpose + state badges, "Open workbench" via `navigate(route)`, "Code" link to engine, "Propose a version" → GitHub issue `template=propose-a-version.yml`), deeper-experiments grid, bottom line.
- [ ] Class names stable and semantic (`journey-*`) for Kimi.
- [ ] `npm run build` passes; open `#story-angkor` in the browser at 1280 px and 375 px; screenshot both.
- [ ] Commit.

### Task 5: Petri correction

**Files:** `experiments/angkor-review/results/petri-results.csv` (regenerate), `public/research/petri-results.csv`, `public/research/provisioning.html`.

- [ ] Run `node run-petri.cjs` (reviewed defaults). Expected drought/none retained ≈ 0.665, gap ≈ 4.402.
- [ ] Copy CSV to `public/research/`; replace the Petri table and interpretation in `provisioning.html`: state defaults (coordination 1, water floor 0), note the coordination knockout now equals "none", keep the old values only as a labelled pre-review row set (coordination 5^0.227, water floor 0.1).
- [ ] Check: `grep -c "66.5%" public/research/provisioning.html` ≥ 1 and the phrase "pre-review" present. Commit.

### Task 6: Contribution path, Kimi brief, verification

**Files:** Create `.github/ISSUE_TEMPLATE/propose-a-version.yml`, `docs/kimi-brief-angkor.md`.

- [ ] Issue form fields: fork URL, base commit, model id, what changed and why, how to reproduce, evidence; label `proposed-version`. Keep Codex's `model-challenge.yml`.
- [ ] Kimi brief: page anatomy, component list with class names, content constraints (claim types must stay distinguishable, boundary sentences cannot be cut, slider only in chapter 1), accessibility requirements, files Kimi may edit (`src/journey.css`, presentational JSX) vs must not (`angkor-journey.ts` numbers, engines).
- [ ] Run all five global checks + `node scripts/check-angkor-journey.mjs`. All pass.
- [ ] Push branch, open PR "Angkor journey: Klassen-first narrative, Petri correction, research integration". Do not merge.
