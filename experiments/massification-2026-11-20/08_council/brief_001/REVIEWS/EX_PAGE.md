> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# REVIEW — PAGE composite (drawing on Page 2018; Miller & Page 2007) — brief_001

**G. GROUNDING.** Literature basis (Page): *The Model Thinker* (2018) and *Diversity and Complexity* (2011) argue that
models are instruments for reasoning, that many models beat one, and that a result is informative when it is
invariant across a model class rather than an artifact of a single formalization. **COUNCIL EXTRAPOLATION:** the
application to this brief is mine; the books do not discuss credential pipelines. Basis: publication-level; full text
not fetched in this environment.

**M. MODEL RENDERING (KIDS).** The claim "intensification requires ranking" lives in a model class:
M1 population = cohort entrants 1995–2012; allocation rule = {rank-order, lottery, fixed cutoff}; wage formation =
{slot-scarce, CES}; household = risk-averse, liquidity-constrained, belief-updating. M2 rule: P(formal job) rises
with credential rank; utility = E[income] − costs, with a cash constraint. M3 parameters: vacancy path, floor level,
risk aversion, wage schedules — all hand-set. M4 observable: slope of Q3–5 college entry on degree income across
demand scales 0/1/2. M5 nesting: the paper's model is one point in this class. M6 falsifier: a rank-ordered
allocation that produces a positive slope. M7 KIDS demand: describe the actual allocation mechanisms (employer
rank-order vs lottery vs cutoffs) before calling the sign a mechanism result.

**A. VERDICTS.** C1 **ESTABLISHED** (implementation): rerun means match stored 4-rep means within 0.013 sd on every
reported cell (`03_audit/logs/floor_test.log` lines 9–14 vs stored `round8…/floor_test/findings.txt` lines 7–10);
slopes differ by ≤0.07 (unranked no-floor +0.221 vs +0.151) — reported. C2 **SIMULATION-ONLY**, and partly imposed
(see B). C3 **SIMULATION-ONLY**; "separation" not established (see C/E). C4 **SIMULATION-ONLY**. C5 **SIMULATION-ONLY**
and largely a restatement of Yoo's fixed-cutoff result (C6). C6 **ESTABLISHED** at literature level: the Yoo card
documents T=αe+ε with effort peaking near the cutoff; the ABM adds no formal object beyond it. C7 **ESTABLISHED**
(counts reconcile: 33 verified / 33 unresolved+partial / 2 constructs in `02_lit/CLAIM_REGISTER.csv`). C8 **UNABLE TO
ASSESS** (cannot verify the Ng & Yip / Gee conflation without the papers). C9 **UNABLE TO ASSESS** (artifact only at a
`/tmp` path, not in `05_experiments/`).

**B. IMPOSED VS DISCOVERED — the core answer.** The rank-vs-lottery contrast changes *two* structural features at
once: (i) who gets the job (rank vs random) and (ii) what investing in the credential buys (positional probability
vs nothing). A lottery arm cannot produce a negative investment slope by construction, because investment has no
rank payoff. So "intensification requires ranking" is near-analytic in this class. What is genuinely *discovered*
within the model is the decomposition: with ranking on, the adaptive-floor arm has a steeper negative slope (−0.068,
line 10) than the fixed-floor arm (−0.037, line 11), i.e. *floor movement*, not the floor level, contributes. That
decomposition is worth reporting and is not in Yoo. The sign itself should not be called a discovery.

**C. ESTIMAND.** The slope is a comparative static across three hand-picked demand levels (0/1/2), not a treatment
effect; "absolute income" is in model units. The C3 rival's formal-employment rate is undefined by construction
(`03_audit/runs/massabm/grad_supply/findings.txt` line 8: 0.000), so "the same outcome in both worlds" is true only
for income. Income baselines differ (1.57 vs 1.07) — the shock is applied to different economies.

**D. TYPE CONFUSION.** The brief is honest ("simulation"), but "separates the account from a competitive market"
(C3) is a claim about theories; no theory was compared, only two model architectures with different margins.

**E. STRONGEST DEFENSIBLE SENTENCE.** "In a model class where formal jobs are allocated by credential rank, a falling
absolute return to the degree can raise investment because rank, not wage level, allocates queue position; under
lottery allocation the same households show the opposite slope. This is a property of the allocation rule, not
evidence about any labour market."

**F. STRONGEST NEGATIVE RESULT.** The floor alone buys little: unranked no-floor completion 0.733 vs 0.771 with a
floor (lines 12–14) — about 4 points — while exclusion is large (formal|dip 0.433 → 0.116). The paper's headline
concept (the relational floor) explains *exclusion and persistence*, not intensification. The brief notices this;
the paper's prose should too.

**G2. STEEL-MAN.** The competitive null deserves a formal-sector margin, endogenous vacancy posting, and CES wages
with the same households; as run, it is a different economy, not a rival theory (PATRINOS makes this case; I
concur).

**H. ALTERNATIVE.** The negative slope may be *insurance/option value* that a credit-constrained human-capital model
also predicts: when formal demand falls, the outside option (informal work) worsens, so schooling is worth more.
The model cannot distinguish "positional" from "option value" because both are coded as income probabilities.

**I. WHAT WOULD CHANGE MY MIND; LIMITS.** A matched-elasticity rival with a formal/informal margin, and a model-class
ensemble (rank, cutoff, lottery × slot-wage, CES). I could not check the allocation-rule code or the promised 4-rep
rerun. That rerun is cheap and should be pre-declared as the reproduction check.
