# Massification research results — 20 November 2026

This is an **experimental results folder** for the DeepSeek research execution of the
*Massification and Its Mechanisms* handoff (Menefee & Nordtveit, October 2026).

It is deliberately isolated from the Atlas site: the site builds from `src/` and `public/`
only (see `package.json`, `vite.config.ts`, `.gitignore`), and nothing here is imported by
the site. It does not modify `main` or the Atlas page.

## Read first
- `SUMMARY_FOR_TREY.md` — plain-language findings, including what is withdrawn and what failed.
- `RESULTS_README.md` — how to read the package, what actually executed, honesty rules.
- `OPEN_QUESTIONS.md` — ranked next experiments and blocked data.
- `PROVENANCE.md` — sources, hashes, environment, site-safety check.

## Status
- 12 completed experiment cells + a Phase-0 accounting gate, 1 pilot, 0 substantive failures.
- A second adversarial batch and Council-recommended follow-ups (E18b / E13c) are included where
  available at commit time.
- All experiment outputs are **simulated model output**, not observations. Country data in `data/`
  is observed, with retrieval dates and sources.
- The synthetic expert-council files are AI composites grounded in published work; they are not
  statements by the named scholars.

Source of the models: `work/atlas/related/massification_project` (parent Atlas checkout `02cade9`);
Atlas public main at `55732f4728a13adb3aec5173d8bc7f3a4ac7f926`.
