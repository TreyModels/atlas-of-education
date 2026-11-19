# Brief for Kimi: visual design of the Angkor journey page

**Branch:** `angkor-journey` in `TreyModels/atlas-of-education`. **Route:** `#story-angkor` (run `npm ci && npm run dev`).
**Your files:** `src/journey.css`, and presentational markup in `src/components/AngkorJourney.tsx` and `src/components/BetaExplorer.tsx`.
**Not yours (content and correctness):** `src/data/angkor-journey.ts`, `src/lib/scaling.ts`, anything in `public/engines/`. Do not change wording or numbers; if copy needs to change for layout, ask Claude.

## What the page is

A story, read top to bottom, about how Angkor's food economy worked and what our models built on it can and cannot show. It starts from a peer-reviewed study (Klassen et al. 2022) and then walks through Atlas extensions, one per chapter. It is the template for the other six model families, so design reusable pieces, not one-offs. Audience tonight: an applied-AI centre director; later: researchers, teachers, students.

Tone: an atlas or a good long-form science feature, not a dashboard. Calm, typographic, generous whitespace. The existing site uses a warm paper palette, serif headings and the CSS variables `--ink --paper --line --muted --green --ochre --surface --serif --sans`; stay within that family.

## Anatomy (class names are stable; keep them)

1. **Hero** `.journey-hero`: kicker, `h1`, `.journey-lede`, then "why" paragraphs.
2. **Chapter index** `.journey-nav`: sticky left column on desktop, horizontal strip on mobile. Each link has `.journey-nav-kicker` and `.journey-nav-title`; the chapter in view gets `aria-current="true"`.
3. **Chapter** `.journey-chapter` (`id="ch-…"`): kicker, `h2`, `.journey-question`, then four `.journey-block`s in fixed order: *What the evidence says / The rule we wrote / What the experiment shows / Limits*. Then optional `details.journey-maths` ("How the maths works"), `.journey-sources`, `.journey-cards`.
4. **Paragraph** `.journey-para` with a claim class and a small `.journey-claim` label: `claim-published` (from the study), `claim-sim` (Atlas simulation), `claim-open` (unsettled), `claim-method` (how it works). **These four must stay visually distinguishable at a glance, including in greyscale and for colour-blind readers** (colour plus another cue: rule style, icon, or label weight).
5. **Model card** `.journey-card`: title, two badges (`.badge.purpose-*`, `.badge.state-*`), note, actions (Open workbench, Code, Notes, Propose a version). Purpose and state are *different axes* (why it exists vs how far it is checked); don't merge them into one colour scale, and don't make "In development" look like an error.
6. **Watch-this moment** `.beta-explorer` (chapter 1 only): one slider, a small line chart (`.beta-klassen` published fit, `.beta-theory` 7/6, `.beta-flat` constant, `.beta-band` 95% range, `.beta-marker`), a readout table, a note. It should feel like a pause in the story, not a control panel. No other sliders.
7. **Deeper experiments** `.journey-deeper`, **bottom line** `.journey-bottomline`, **download** `.journey-download`.

## Must keep

- The boundary sentences in chapter 1 (proxy not rice tonnage, separate associations, not a surplus share, our hypothesis) visible without clicking.
- Keyboard access, visible focus, `prefers-reduced-motion` respected (no scroll-jacking, no parallax, no auto-play).
- Readable at 375 px; body text ≥ 16 px; line length ≤ ~75 characters.
- No new dependencies without asking. No images of real people.

## Check before handing back

`node scripts/check-angkor-journey.mjs && npm run build && node scripts/check-react.cjs`. Screenshots at 1280 and 390 px.
