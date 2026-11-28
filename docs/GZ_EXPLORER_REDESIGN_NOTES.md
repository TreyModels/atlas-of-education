# Guangzhou Explorer — redesign notes (28 Nov 2026)

Audience: **absolute beginners and expert readers (e.g. Mark Bray)**. Must work on **mobile first** (iPhone 15 Pro Max = minimum; new iPhone 17 Pro-class orange phone too) and desktop. Sky is the limit on tech (Canvas/WebGL, React, JS).

## Audit findings (page at `public/guangzhou-explorer/`)
- Hero opens with "65.8% vs 81.8%" and ratios 0.91 / 1.17 / 1.37 and never says what they are. Too many unstated assumptions.
- ~230 words total, one chart, no hero visual. Nothing hits you on arrival.
- Undefined terms: entrance score, joint score & ability, setting, top 10% ability, academic track, seeds.
- **The double reduction (双减) policy is not explained at all.** Needs a plain-language section: what it is, what it banned/limited, why it matters to the model, what the enforcement-sensitivity runs test. Beginner paragraph + expert box (policy details, sources, model parameters).
- Screenshot via file:// showed empty findings grid and chart. Probably data fetch blocked on file://, **verify on the live site** (could be a real first-screen bug).
- Stage 1 done: author name changed to "Dr. Trey Menefee" (committed to this branch, not yet on `main`/live).

## Plan
1. **Check `data.json` first**: per-pupil outcomes or aggregates only? If aggregates only, the sorter replays a sample drawn to match saved rates and must say so ("replay of saved run #…"). Never invent outcomes.
2. **Plain-language "What is this?"** block under the title (question, simulated pupils, what the model does, what numbers mean), 3-4 short paragraphs. Expert "details" toggle beside it.
3. **Hero = sorting machine.** ~4,000 dots (one per pupil) fall through the real stages (tutoring, school type, entrance score) into baskets (selective university / other university / vocational / out). Colour by family income (warm = richer 40%, cool = poorer 40%, grey = middle). Live share counters per basket. Caption: "each dot stands for one of ~41 million simulated pupils" (40,000 pupils x 1,024 settings, plus tutoring runs).
4. **Three-sorts toggle.** Re-sort the same pupils by entrance score / score + ability / starting ability; dots animate and the rich-poor gap widens 0.91 -> 1.17 -> 1.37. This explains why the ratios differ.
5. **Double-reduction scenario toggle** on the sorter: policy off vs on, and enforcement level. Show what changes.
6. Later: ability-vs-outcome swarm with "turn tutoring on" slider; Sankey pathway ribbons (income -> track -> destination); 1,024-setting heatmap that loads a run into the sorter; scrollytelling captions; mini animated bar pairs on finding cards; glossary tooltips; "what this model can't tell you" note.
7. Reuse school-pathway diagrams already in `research/` (paper).

## Constraints
- Mobile layout first: single column, thumb-sized controls, no hover-only info, canvas sized to viewport, ~60 fps on a phone (cap dot count adaptively), pause/replay button, honour `prefers-reduced-motion` (static end state).
- Bilingual: every new string goes in `i18n.js` (EN + zh-Hans). Chinese reader gets same explanations.
- Keep "precomputed saved runs only" honesty label visible.
- Accessibility: text alternatives for the animation (live-region summary of basket shares).
- Deploy only runs from `main` (`.github/workflows/pages.yml`); this branch is `claude/busy-mayer-mdo5c4`.

## Atlas Bridge
No access to Bridge from the coding session. Paste this file's "Plan" section into the Bridge log.
