# EXPERIMENTS — Loop 8b: ECI-inclusive frontier (wiring correction)

**SYNTHETIC / POSSIBILITY-ONLY — not evidence, not validation; programme stays CLOSED; brief-008 limits
stand.** Correction of loop 8's false ECI absence check: ECI is on disk and is added as graded distributions
using **`eci_hs92`** (country means 2015–2024: KOR 1.754, HKG 1.218, PHL 0.718, KHM −0.281; reference
0.852). ECI conditions E1 terminal-stage gate stakes, E2 terminal-stage credential returns, E3 twoway
completion/tertiary transition, E4 twoway formal-job creation elasticity — distributions and unscoreable
rows are in `PRE_DECLARATIONS_L8B.md`. Same LHS design (256 draws × 5 matched seeds), same targets/bands,
no tuning. Code: `code/synth_wired_eci.py`. **0 failed cells.** Run artefacts in `runs/`.

## Five-target frontier: loop6-before → loop8 (relations) → loop8b (+ECI)

| target | loop 6 inside/256 | loop 8 inside/256 | **loop 8b inside/256** | 8b delta vs 6 | 8b vs 8 |
|---|---|---|---|---|---|
| KOR stage gradient | 0 | 0 | **0** | 0 | 0 — **empty support persists** |
| HKG stage gradient | 0 | 1 | **2** | +2 | +1 — **shrink holds** |
| KOR fee | 28 | 27 | **27** | −1 | 0 |
| KOR income-gradient | 117 | 87 | **82** | −35 | −5 |
| KOR two-margin joint (R23) | 0 | 0 | **0/256** | 0 | 0 — **empty support persists** |

ECI adds a small amount of HKG-gradient support (1→2/256, still predeclared shrink territory) and leaves the
Korean gradient at **0/256**; the KOR two-margin joint pattern remains **0/256** (participation-only 0,
intensity-only 229, neither 27). All five are synthetic possibility fractions under the same bands — not fits.

## Unscoreable ECI rows (direction-only, not scored)
**R44** wage/and-salaried share (not significant) · **R45** cumulative-growth × ECI (growth premium fails;
negative ns) · **R46** youth literacy (jointly produced; auxiliary) · **R47** spending×ECI (not significant) ·
**R48** schooling×ECI (negative — opposite the prior) · **R49** metric choice (methodological) ·
**CX-01…CX-04** direction-only by construction. `eci_sitc` carried as robustness only (never scored); ranks,
`growth_proj`, spliced HS12 never used.

## Verdict
Adding ECI as a country-level graded condition does **not** shrink the Korean stage-gradient empty support
(0/256) and does not produce the joint Korean two-margin pattern (0/256); it slightly increases HKG-gradient
support (1→2/256). The biggest remaining impossibility is unchanged: the **KOR falling stage gradient** (and
the joint Korean pattern), with the demand-level intercept still fixed (A0 = −1.5; no relation supplies a
demand level). **SYNTHETIC/POSSIBILITY ONLY; programme CLOSED; no closed claim reopened.**
