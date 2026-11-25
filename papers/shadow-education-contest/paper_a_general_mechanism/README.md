# Paper A — general mechanism (Sub-Saharan Africa)

**Status: NOT RECEIVED.** The bridge handoff supplied only a Google Doc ID, not the file:

> Paper A APA `.docx` — Google Doc ID `1NFXSjzRaAXR2nhM6iZVTlhJKcE5puj7PI43ZZkP2cns`

That document was not downloadable from this environment (no Google auth) and no `.docx` was attached to the
bridge message. The handoff described the manuscript as "Fee abolition meets rationed gates: shadow education,
strategic contests, and micro-identifiability", with the claimed results summarised in
`../RECONCILIATION.md`.

## Claimed headline results (author-reported; NOT verified here)

Recorded only so the gap is explicit. None of these has committed code/data in `TreyModels/atlas-of-education`:

- **Exp 1** — live-WDI `t*` bulge-arrival test, 7,290 observations, 2,500 Fisher permutations: reported as an
  honest null for `SE.PRM.REPT.ZS` (`T0 = +1.061`, `p_date = 0.1407`, `p_country = 0.2791`) and sparse/non-
  estimable for progression and pupil–teacher series.
- **Exp 3** — Tullock `contest` gate, 1,640 matched runs: H2 fee × scarcity interaction `+0.1086`
  (`p = 1.9e-11`) vs quota `−0.0145`; inverted-U in `vac0`; H1 `+0.3430` (Spearman −1.00).
- **Exp 4** — identifiability: Bray's 7 aggregate moments rank 5/7 (condition 1.09e13); adding income and
  within-grade quality micro-moments restores rank 7/7 (condition 43.81).
- **Exp 5** — out-of-sample E8 shock: 7-horizon RMSE `5.13`/`4.68` pp vs persistence `23.93` pp; calibrated to
  74.88% pre-abolition GER; predicted on-impact `+11.60`/`+13.48` pp vs empirical `+12.44`.

**These conflict in part with committed records.** See `../RECONCILIATION.md` before citing anything.

## Needed to deposit Paper A

1. The Paper A `.docx` (attach to the bridge, or provide a downloadable URL).
2. The engine patches (the exact `core.py` / `modules/tutoring.py` diff).
3. The runner(s) and the five result JSONs named in the handoff.
4. A pre-registration/hash record for the 1,640-run and 7,290-observation runs.
