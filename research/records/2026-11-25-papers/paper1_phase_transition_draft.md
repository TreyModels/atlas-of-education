# The Exam-Gate Phase Transition

### Fee abolition, formal-job scarcity, and the birth of shadow education in a simulated school system

**Status: draft, 25 Nov 2026. Simulation only — no causal or empirical claims apply to the simulated
results. Empirical quantities are observational associations from DHS/UIS/WDI panels.**

---

## Abstract

Standard education policy treats free primary schooling and meritocratic national exams as twin
virtues. We ask whether, in a system where the formal labour market is small and secondary access is
rationed by a high-stakes exam, abolishing primary fees can push a cohort bulge "up six grades" into a
regressive shadow-education arms race rather than into opportunity. Using a pre-registered agent-based
education system (`eduengine`, 144 parameter combinations), we find **no sharp regime boundary when the
exam gate is non-binding** (max adjacent-cell jump J = 2.88, below the pre-registered threshold of 4),
and a **sharp, interior regime boundary when the gate binds** (J = 11.5, sharpness 18.2, on the formal
vacancy axis at 0.40–0.50 vacancies per cohort entrant; gate-fail share J = 12.58, sharpness 23.5).
The boundary is accompanied by a gate-type contrast of 7.4 pp in the wealth gap in private tutoring
(pre-registered threshold 5 pp) and by 374 "equifinal" cell pairs that reach the same lower-secondary
completion rate with tutoring intensity differing by >20 pp. A pre-registered seat-scarcity sweep
confirms that the tutoring gap widens monotonically as seats shrink (Spearman ρ = −1.00; 0.442 vs
0.343 between seat shares 0.25 and 0.70) but does **not** detect the predicted fee-abolition × scarcity
interaction (interaction +0.0039, 95% CI [−0.019, +0.027]). We report the positive boundary, the null
interaction, and the design's limits with equal weight.

---

## 1. The question

Two literatures have not been forced to collide. The first documents *supply-led massification*: in
many countries schooling expanded decades before industrial demand for educated labour
(E6/E8 evidence packet). The second documents *shadow education*: as exam stakes rise, private
tutoring becomes a positional arms race (Bray; Nordtveit). The policy intuition that links them is
simple and testable: **if you remove the liquidity barrier at the bottom of the system without adding
formal jobs or seats at the top, you do not equalise opportunity — you move the bottleneck upward and
hand it to the private market.**

Stated as a mechanism rather than a narrative, this is a claim about a *phase transition*: for some
range of (job scarcity × liquidity slack × gate tightness), the system should switch from a
liquidity-constrained regime to an exam-gate / tutoring regime. Our contribution is to test for that
transition under pre-registration, and to report where it does and does not appear.

## 2. The model

`eduengine` is an agent-based education system (household affordability → school learning → selection
gates → credential/labour-market outcomes) with modules for public/private schooling, a tutoring
market, a fiscal state, a queue labour market, and SDG-4 aggregation. Two properties matter for honest
reading:

1. **It is a toy world.** Parameters are illustrative; outputs are labelled SIMULATION throughout.
   The MASSENG v5 boundary table is the anchor: no learning state, no score/quota gate, no labour
   market, no rural/urban, no borrowing; tutoring absent; credentials only as exogenous premium drivers.
   `eduengine` goes *beyond* that boundary — which is exactly why its outputs cannot be read as
   estimates of any real system.
2. **The exit accounting was itself once broken**, and the fix matters for every share reported here.
   `core.step` compacts exited children out of the state into `e.exits`, leaving `e.kids['reason']`
   all −1 after `run()`. A driver that read `e.kids` therefore reported a universal 0/0/0 exit
   decomposition; the engine was correct. All results below use the corrected `aggregate_exits()` read,
   where exits + survivors-censored-at-horizon partition the measured population to 1.0
   (branch `fix/edsystem-exit-reason-2026-11-25` @ `4679ddb`; regression test `test_exit_reason.py`).

## 3. Pre-registered design

Two experiments were pre-registered **before** their runs, with fixed statistics and decision rules:

- **Quick grid** (`research/phase-transition-2026-11-25` @ `408aa3e`): X = formal vacancies per cohort
  entrant (10 levels, 0.02–0.50), Y = primary fee as a share of median income (10 levels, 0.00 =
  fee abolition → 0.18), gates ∈ {bar, quota}, 5 seeds. 1,000 runs.
- **Dense grid** (`research/phase-transition-dense-2026-11-25` @ `8b0cc88`, statistic amendment
  `40159c7`): 20×20 levels, 20 seeds, both gates. 16,000 runs. The statistic was declared before any
  dense number was read: `J(pair) = |Δ response| / median(seed SD of the two cells)` along both axes;
  `sharpness = J_max / median(J_edge)`; **SIGNATURE** requires an interior `J_max ≥ 4`, sharpness ≥ 2,
  and a gate contrast `C > 0.05`.
- **Binding-gate experiment** (`research/binding-gate-2026-11-25` @ `37cbe3d`): quota seat share
  S ∈ {0.25, 0.35, 0.45, 0.55, 0.70} × 10 vacancy levels × 6 fee levels × 5 seeds (1,500 runs) plus a
  high-bar arm (score thresholds 14–17); primary test pre-declared as the **fee-abolition × scarcity
  interaction**.

## 4. Results

### 4.1 No boundary when the gate does not bind

Under the pre-registered `bar` gate the exam is **non-binding by construction in this engine** (q1
gate-fail share ≤ 1.3% at every vacancy level). The dense grid therefore cannot show a gate-driven
transition there, and it does not: the sharpest tutoring-gap jump is **J = 2.88** (edge, sharpness
11.5), below the pre-registered `J_max ≥ 4`. The quick grid agreed (J_max 2.02–2.58). **Verdict:
ABSENT/PARTIAL for the bar signature.** This is a statement about the model's gate, not about real
exam systems — the pre-registered bar arm is not a tournament.

### 4.2 A sharp, interior boundary when the gate binds

With the quota shoulder making seats scarce, the dense grid produces the pre-registered signature on
the **vacancy (bottleneck) axis**:

| response (quota arm, dense 20×20, 20 seeds) | J_max | location (vac0) | sharpness | verdict |
|---|---|---|---|---|
| tutoring Q5−Q1 gap | **11.50** | 0.4005 → 0.5044 (interior) | **18.17** | **SIGNATURE** |
| gate-fail share | **12.58** | 0.4188 → 0.5044 (interior) | **23.48** | **SIGNATURE** |
| liquidity exit share | 11.91 | interior | 11.9 | (supporting) |
| tutoring rate | 24.71 | interior | 31.3 | (supporting) |

The gate does not bind at low vacancy levels (liquidity exit shares are large, gate-fail small); as
formal vacancies per entrant approach ≈0.40–0.50, gate failure rises and the wealth gap in tutoring
jumps. The same grid's bar arm stays PARTIAL. **The transition is conditional on the gate binding, and
that is the mechanism claim, not a universal one.**

### 4.3 The gate contrast

Holding the (vacancy, fee) cell fixed, switching from the bar to the quota gate changes the median
wealth gap in tutoring by **C = 0.074** (7.4 pp), above the pre-registered 0.05 threshold — consistent
with the boundary being a *gate* phenomenon rather than a generic scarcity effect.

### 4.4 Equifinality: same attainment, different competition

374 cell pairs reach the same lower-secondary completion rate (within 0.5 pp) while differing by >20 pp
in tutoring intensity (auditor thresholds, fixed in advance). The largest example: (vac0 ≈ 0.010,
fee 0.19) vs (vac0 ≈ 0.50, fee 0.00) — completion differs by **0.26 pp**, but tutoring rate differs by
**20.9 pp** and liquidity exits by **15.5 pp**. Caveat: quota completion is partly pinned by seat share,
so "same attainment" is in part an accounting identity; the informative statement is *the bulge is
absorbed by competition rather than attainment*, not that attainment is invariant.

### 4.5 Seat scarcity widens the gap; the fee interaction is not detected

In the pre-registered binding-gate sweep, mean Q5−Q1 tutoring gap falls monotonically as seats become
abundant: **0.442 (S=0.25), 0.435, 0.424, 0.397, 0.343 (S=0.70)** — Spearman ρ = −1.00, difference
+9.9 pp (H1 **SUPPORTED**).

The primary hypothesis H2 — that the *fee-abolition effect* on the gap is larger when seats are scarce
— is **NOT detected**: interaction = **+0.0039**, approximate SE 0.012, 95% CI [−0.019, +0.027]
(verdict UNDERPOWERED). A high-bar arm (score thresholds 14–17, i.e. a binding *bar* rather than a seat quota) sits apart:
mean tutoring gap **0.231** and a much larger negative fee effect (−0.208 vs −0.054…−0.069 under the
quota arms), i.e. a binding bar compresses tutoring far below the quota regimes — the *form* of the
binding gate matters, not just its tightness. The fee effect itself is negative at every seat share (gap at fee 0.19 vs 0.00:
−0.054 to −0.069), i.e. within the simulation, abolishing fees *raises* the wealth gap in tutoring —
but we cannot distinguish an interaction from noise with 5 seeds. We report H2 as a null, not as
support.

### 4.6 The auditor's three quoted numbers, checked

| claim | result |
|---|---|
| gates drive 42.4% of variance in `skill_premium` | **42.42%** ✓ (one-way η², competitive arm, n=720) |
| learning drives 77.8% of `formal_rate` | **77.83%** ✓ (one-way η², queue arm, n=720) |
| poor households exit mostly from liquidity (70.6%), not gates (0.8%) | **partial**: q1 liquidity 68.99% (40-seed mean) / 69.66% (seed 0); q1 gate-fail 1.14±0.18% by direct reason-code read, but the 0.8% figure is folded into `other_terminal` in the multiverse decomposition. Ordering reproduces; exact decimals do not. |

## 5. What this does and does not show

**Shows (in the simulation):** a genuine, pre-registered regime boundary exists only when the exam gate
binds; it sits on the bottleneck axis; identical attainment can hide very different competition
intensity; scarcity of seats monotonically widens the tutoring gap.

**Does not show:** that any real country crossed this boundary; that fee abolition *causes* an arms
race (the pre-registered interaction is a null here); that the bar gate's non-binding regime resembles
real high-stakes exams; or any causal effect of E8 reforms. The empirical E8 event-study quantities
(CS post +22.12 to +28.56 pp; on-impact +12.44, CI includes 0) and the "bulge arrival" test (t* not
estimable — primary-school duration sourced 0/8 in-repo) are reported separately as observational
associations and a data gate.

## 6. Replication

All runs, pre-registrations, and outputs are committed:
`research/box-runs-2026-11-25` @ `0fd9928` (1,440-run fixed-driver multiverse, 5,760-run 40-seed grid,
500+500 bar/quota sweeps, 2,000-run dense quick sweep, patched-DHS byte-identical re-run, replication
lockfile); quick-grid record `research/phase-transition-2026-11-25` @ `f1c16f1`; dense pre-registration
`research/phase-transition-dense-2026-11-25` @ `40159c7`; binding-gate pre-registration
`research/binding-gate-2026-11-25` @ `37cbe3d`; fixed driver
`fix/edsystem-exit-reason-2026-11-25` @ `4679ddb`. The dense grid itself was run by a parallel session
(`lead-nb`) into `/root/work/equifinality_phase`; statistics are ours, computed with the pre-registered
metric.

## 7. Limitations

1. **Toy worlds.** No claim transfers to a real system without re-estimation.
2. **The `bar` gate is non-binding** in-engine; the "twin virtues" setup is only instantiated by the
   quota shoulder, and the engine's quota is not the same as "seats scale with the cohort".
3. **Seeds.** The dense grid has 20 seeds/cell; the binding sweep has 5 — H2 is underpowered by design
   and reported as such.
4. **Deterministic components.** Completion can be pinned by seat share, so equifinality counts include
   accounting identity, not only behaviour.
5. **The simulator was itself audited and repaired** during this work (exit-reason read, gate quota
   double-count, fractional-mass vacancy clearing); earlier numbers from this engine should not be
   quoted.

## References

Bray, M. — shadow education (book/compendium) **[cite]**. Nordtveit, B. — schooling, child labour and
liquidity **[cite]**. Pritchett, L. — schooling vs learning, supply-led expansion **[cite]**.
Callaway & Sant'Anna — difference-in-differences with multiple time periods **[cite]**.
*(Citations are placeholders; no bibliographic claim is made in this draft.)*
