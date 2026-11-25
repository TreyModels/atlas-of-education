# Paper A — general mechanism (Sub-Saharan Africa)

**Status: RECEIVED as a draft (2026-11-25).** The canonical all-in-one bundle contains the Paper A manuscript:
`When_Fee_Abolition_Meets_Rationed_Gates_APA.docx`, 369,246 bytes, sha256
`39092abb071f0f50552bfd920f16503c8280ecf585a7703b333657d099820c91`. It is a **draft manuscript deposited as
received** — its simulation/identifiability numbers are **not independently reproduced here** (the code and
result JSONs for Exp 1/3/4/5 have not been supplied and were not run), so nothing below is citable as verified.
Label everything from it **author-reported draft**.

Manuscript title (as received): *When Fee Abolition Meets Rationed Gates: Shadow Education, Strategic
Contests, and Micro-Identifiability in Massifying Education Systems*, Trey Menefee, Atlas of Education
Research Program. (The bridge handoff had previously supplied only a Google Doc ID
`1NFXSjzRaAXR2nhM6iZVTlhJKcE5puj7PI43ZZkP2cns`; the `.docx` is now on disk.)

## What was spot-checked (not a verification)

- The manuscript's empirical E8 figures are **consistent with the committed E8 record**
  (`research/e6e8-sequencing-2026-11-25` @ `bd782be`): abolition-year GER jump **+12.44 pp** (committed
  12.4436), mean post-abolition **+25.26 pp** (committed 25.2607), and event range **+22.12 to +28.56 pp**
  over e = +1…+6 (committed min 22.1208 at +3, max 28.5608 at +5). The earlier draft's conflicting event
  column flagged in `../RECONCILIATION.md` is **not** what this manuscript contains.
- Its simulation and identifiability claims (Exp 1 live-WDI `t*`, Exp 3 Tullock `H2 = +0.1086`, Exp 4
  Jacobian rank 5/7 → 7/7, Exp 5 74.88 % calibration and predicted `+11.60`/`+13.48`) remain
  **author-reported** — no committed code/results reproduce them, and the `t*` record in-repo is
  **NOT-ESTIMABLE** (`L_primary` sourced 0/8), so Exp 1's live-WDI series must be committed before citation.

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

**These remain partly unverified and conflict in part with committed records.** See `../RECONCILIATION.md`
before citing anything.

## Still needed to verify Paper A

1. The runner(s) and the five result JSONs named in the handoff (Exp 1/3/4/5) — the manuscript alone is not
   a reproduction artifact.
2. A pre-registration/hash record for the 1,640-run and 7,290-observation runs.
3. The live-WDI series and its hashes for Exp 1.

The engine patch and the Paper B 540-run CF4 reproduction are now on this branch; see
`../code/REPRODUCTION_CF4_2026-11-25.md`. Paper A's own simulations were **not** run here.
