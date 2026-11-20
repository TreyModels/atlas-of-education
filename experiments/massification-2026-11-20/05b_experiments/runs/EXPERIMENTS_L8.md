# EXPERIMENTS — Loop 8: relations→model wiring, synthetic frontier re-run

**SYNTHETIC / POSSIBILITY-ONLY.** Authorised follow-on (task B); **the programme stays CLOSED** — this does
not reopen any closed claim, does not re-fit closed targets, is not evidence, and brief-008 identification
limits stand. Predeclaration: `PRE_DECLARATIONS_L8.md` (written before running; one-line status relayed to
ops centre when written). Same LHS design as loop 6: **256 draws × 5 matched seeds**, same target bands and
tolerances, no tuning. Code: `loop8/code/synth_wired.py`. **0 failed cells.**

## Wiring (declared distributions; graded relations, never point fits)

| relation | wired parameter | declared distribution |
|---|---|---|
| R01 spending→secondary | twoway completion logit (spend ratio, lag 5) | b01 ~ LHS[0.010, 0.189]; spend_ratio LHS[0.8,1.6] |
| R04 income→tertiary | twoway college-entry (income ratio) | b04 ~ LHS[0.281, 1.075]; income LHS[0.5,3.0] |
| R07 fertility→primary completion | twoway completion (births ratio) | b07 ~ LHS[0.10, 0.30]; births_ratio LHS[0.6,1.3] |
| R13 education→growth (`eps_ec`) | twoway regime eps_ec | eps_ec ~ LHS[−1.035, 0.6]; explicit arm {−1.035, 0, 0.3, 0.6} |
| R21 gate proximity→tutoring | shadow-demand stakes concentration | b21 ~ LHS[0.4, 1.0] |
| R22 income elasticity of spend | shadow-demand income coefficient (0.55·b22) | b22 ~ LHS[0.6, 1.3] |
| R23 two-margin (extensive×intensive) | stage intensity multiplier | b23 ~ LHS[0.10, 0.60] |
| R24 urban→tutoring | urban income-multiplier ratio (r24/2.0) | r24 ~ LHS[2.29, 2.62] |
| R29 price elasticity | shadow-demand price coefficient (1.1·scale) | B_FEE_scale ~ LHS[0.5, 2.0] |
| R41–R49 ECI/complexity | — | **PENDING** (`04_data/complexity/` absent; no imputation; CX-type rows unscoreable) |

Unwired relation rows stay declared priors. The demand-level intercept remains the fixed structural constant
**A0 = −1.5** for every draw (no relation supplies it) — recorded in advance as the known blocker.

## Per-target frontier: loop 6 before vs loop 8 after (inside/256)

| target | loop 6 | loop 8 | delta | shrink? |
|---|---|---|---|---|
| KOR stage gradient (86.0/75.4/66.4 ±5pp) | 0 | **0** | 0 | no — **empty support persists** |
| HKG stage gradient (35.1/46.6/70.3 ±5pp) | 0 | **1** | +1 | **YES (predeclared shrink)** |
| KOR per-participant/per-student fee | 28 | 27 | −1 | no |
| HKG fee/income 1.1–5.0% | 134 | 137 | +3 | no |
| KOR income-gradient ratio 3.67 ±50% | 117 | 87 | −30 | no |
| KOR commercial provider share 55.5 ±10pp | 42 | 44 | +2 | no |
| PHL completion 75.0 ±5pp (cohort-flow) | 36 | **0** | −36 | no |
| KHM completion 27.9 ±5pp (cohort-flow) | 73 | **142** | +69 | no |

**Decision rule (predeclared):** a "frontier shrink" = a target that was **0/256 in loop 6** becomes **≥1/256
in loop 8** under the same bands and no fitting. Result: **shrink occurred for the HKG stage gradient
(0→1/256)**; **KOR stage gradient remains 0/256**, so **empty support persists for the Korean gradient**.
Other targets moved both ways (KHM completion support more than doubled; PHL completion support collapsed
to 0; KOR income-gradient support fell by 30). These are synthetic possibility fractions, not fits.

## R13 / eps_ec arm (run against the negative panel estimate, not assumed)

Synthetic eps_ec ∈ {−1.035, 0, 0.3, 0.6} (5 seeds each; PH-like and KHM-like):

| eps_ec | PH-like completion | PH degree share | PH complex jobs | KHM completion | KHM degree share | KHM complex jobs |
|---|---|---|---|---|---|---|
| −1.035 | 61.07 | 12.29 | 122.3 | 33.15 | 7.62 | 71.7 |
| 0.000 | 61.13 | 12.47 | 125.1 | 33.20 | 7.84 | 74.8 |
| 0.300 | 61.14 | 12.53 | 126.0 | 33.21 | 7.91 | 75.8 |
| 0.600 | 61.16 | 12.58 | 126.9 | 33.23 | 7.97 | 76.7 |

The negative panel estimate (R13) is wired in the eps_ec distribution (range includes −1.035) and its arm is
run explicitly; the module's complex/formal jobs remain mildly increasing in eps_ec, i.e. the model class
still contains the positive education→growth channel the panel rejects, but the effect on the synthetic
outcomes is small (~2–3% of complex jobs across the whole arm). No synthetic target needed eps_ec>0.

## KOR two-margin arm (R23)

Under the wired intensity margin: **joint pattern 0/256**; participation-only 0; intensity-only 229; neither
27. The participation gradient itself remains unreachable (consistent with KOR gradient 0/256), so the
**joint Korean pattern (falling participation + rising spend) has empty support even with both margins
present** — the predeclared "if only one margin available, record empty support" is satisfied in the stronger
form: both margins are present and joint support is still empty.

## Biggest remaining impossibility

The **KOR falling stage gradient** — and a fortiori the joint two-margin Korean pattern (0/256) — remain
unproducible inside the declared assumption space, and with the demand-level intercept fixed (no relation
supplies a demand level) the wiring cannot reach the observed levels. **SYNTHETIC/POSSIBILITY ONLY — not
evidence, not validation; no closed claim reopened; brief-008 limits stand.**
