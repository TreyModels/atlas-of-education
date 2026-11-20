# COUNCIL REVIEW 016 — brief-015 toy battery (fifteen experiments, five clusters)

**Type:** design/mechanism review only. **Status of the phase:** stays **CLOSED** — closeout commit
`4ba958c`; battery committed `47cad5d`; closeout's recorded authoritative tip `787f1792…`. Honest headline
unchanged: *"conditional LEVEL reproduction + observational equivalence + an unreproduced asymmetry."*
**Status of the material under review:** **ILLUSTRATIVE TOY — stipulated parameters; not calibrated;
not evidence; no historical test; phase closed; do not cite numbers as estimates.** This review does not
re-fit, reopen, promote, or endorse any claim, and no toy number may enter a results table or an evidence
column. Panel composites: LUTZ (measurement), PATRINOS (identification), PAGE (model design),
CARTWRIGHT (falsifiability). Written at the user's request; brief 014 review is `COUNCIL_REVIEW_014.md`,
specification is `COUNCIL_TOY_SPECS_015.md`. Decisions recorded alongside this review:
`08_council/DECISIONS.md` **D79–D87** (D87 = process note on the failed bridge post).

**Source key.** `A`/`B`/`C`/`D`/`E` = `cluster_A…E/FINDINGS.md`; `PA`…`PE` = the matching
`PRE_DECLARATIONS.md`; `MA`…`ME` = the matching `RUN_MANIFEST.json`. Numbers are
cited to these files, not to memory. Verification performed for this review: every one of the 60 entries in
`SHA256SUMS.txt` verifies; `cluster_C` and `cluster_E` were re-run in a clean `/tmp` copy and reproduced
`RESULTS.csv` **byte-identically** (`af889331…`, `f8cb72d1…`; E's `verify_results.py` re-derives 17/17
verdicts); A/B/D were hash-checked but not re-executed. All five `PRE_DECLARATIONS.md` hashes match the
hash recorded in their manifests.

---

## 0. Verdict in one paragraph

**ACCEPT AS ILLUSTRATIVE DESIGN EVIDENCE — evidential weight zero, design weight real.** The battery is
technically competent and unusually honest: paired seeds, predeclared thresholds and falsifiers, all cells
reported including failures, thin margins disclosed, amendments and one post-run code defect disclosed,
deterministic replay. As *design* evidence it yields four usable things: (i) a sharp negative — **a fixed
cost alone does not produce entry/exit hysteresis** (A1, falsifier fired); (ii) the **net-vs-gross**
arithmetic of a public expansion when private providers are lumpy and exit whole (A2); (iii) the
**gate-not-level** account of capacity saturation (C7's own T7c failure); and (iv) the
**complementarity/underpowering** lessons for the rival-discrimination and demand-pull designs
(B4–B6, C8, E14–E15). As *findings* it yields nothing: most "PASS"es are either boundary-conditioned
(A2 at 0.486 vs 0.50; A3 at 8.08 vs 8.0), mechanically forced by a stipulated production function
(C7 T7d, C9 rooms-only, C8 enforcement-without-law, D11 per-child capacity, B5 T5.1/T5.2), or a
consequence of a stipulated premium/ranking rule (B4's `4(1−v)`, B6's zero credential–skill correlation).
**No direction claim, no reopening, and the closed-phase headline is untouched.**

| cluster | experiments | headline | thresholds / verdicts |
|---|---|---|---|
| A supply | #1–#3 | one FAIL, two boundary PASSes | A1 FAIL (falsifier fired); A2 PASS at R=0.486; A3 PASS at 8.08 ≥ 8.0 (A §1–3) |
| B rivals | #4–#6 | no discriminating sign pattern | 5 NOT MET (T4.1, T4.2, T5.4, T6.1, T6.4), 8 PASS, 3 falsifiers not fired (B §0) |
| C capacity | #7–#9 | #8/#9 clean, #7 two FAILs | 15 PASS / 2 FAIL + 3 falsifiers clear (C §0) |
| D timing | #10–#12 | PARTIAL / SUPPORTED / PARTIAL | D10 2 threshold misses + 1 secondary-interval miss; D11 all; D12 2 misses (D §1–3) |
| E demand | #13–#15 | 10 PASS / 4 FAIL | T14-P1c, T14-P4, T15-P1, T15-P3 fail (E §1) |

---

## 1. Per-cluster assessment — mechanism design vs artefact

The question asked of each result: *would this survive changing the stipulated rule that produced it?* A
result that is a restatement of the rule is pedagogy, not mechanism evidence; a result that is a negative
about a **previously asserted inference** is the only kind that transfers, because it constrains future
design even when the parameters are arbitrary.

### Cluster A — provider entry / supply response (touches C1, net≠gross)

| item | genuinely informative (design) | artefact / forced by stipulation | source |
|---|---|---|---|
| **A1 hysteresis** | **The strongest negative in the battery.** The spec's implicit inference "fixed cost ⇒ fast exit / slow entry" is false at this parameterisation: `A_high = 1.034`, `A_low = 1.025`, difference `0.008` vs a required `≥ 0.25`; exit and entry event distributions nearly identical; falsifier fired. A fixed cost buys **discreteness and a level shift**, not asymmetry. Robustness: the discarded divisible-capacity rule also gives `A_high = 1.034` (`A_low = 0.914`), so the null is not a lumpiness artefact. | Near-symmetry is close to symmetry-by-construction: a symmetric threshold, a symmetric ±20% shock, and **contemporaneous** decisions (the predeclaration admits timing asymmetry is zero by construction; only magnitudes could differ). The up-shock also censors applications at the 100-household ceiling (85.66 → 100 vs 62.64 down), so it is not a clean ±20%. | A §1; PA §1; MA `lump.A_*` |
| **A2 net vs gross** | **The most decision-relevant mechanism.** Public expansion 30→50 loses the private provider in 68.5% of seeds: gross +20, private admissions 13.43→3.15, net **+9.73**, retention **R = 0.486** (< 0.50); at 30-seat capacity 42/200 seeds have **net ≤ 0**. The per-seed structure is bimodal (net exactly +5 if the provider exits, +20 if not) — a **mixture, not an elasticity**. | The magnitude is arithmetic: `R = 1 − exit_share × (lost lump / gross)`. The `bk = cap` knife-edge ("break-even only when fully utilised") and all-or-nothing exit *create* the bimodality; with the base toy's `F = $12` retention is **0.665**, i.e. T2a would have failed. A 14-seed swing flips the verdict. Real providers shrink, hold price, or cut quality; this toy only lets them exit whole. | A §2; PA Amendment 1 |
| **A3 entry lag / overshoot** | Usable timing rule: overshoot requires **lag > remaining boom length** (L=4 arrives one period after a 4-period boom); L=2 arrives inside and is absorbed. No lag is best — longer lags buy lower vacancy risk by paying more deficit (admissions 603.52 → 584.60 → 567.06). | Near-tautological at the level claimed: "capacity that arrives after demand recedes is idle". The magnitude (peak vacancy **8.08**, threshold 8.0) is bounded by lump size × number of late orders, and the **installation lock** is what converts late arrival into recorded vacancy — without it the toy shows no overshoot. | A §3 |

**Assessment.** Cluster A is the only cluster whose *negative* is worth carrying forward. A1 says do not
encode hysteresis as a fixed-cost parameter; A3 says the only "asymmetry" the toy can produce from a lag is
**temporal** (deficit in the boom, vacancy after it), not a difference in entry vs exit strength; A2 says
the policy object is **net of private exit**. All
three, however, are statements about the rules as written — none is evidence that Philippine private
providers exit whole, shrink, or respond at all.

### Cluster B — rival discrimination (touches C3)

| item | genuinely informative (design) | artefact / forced by stipulation | source |
|---|---|---|---|
| **B4 visibility × mechanism** | The only stable discriminator is **composition** (rejected-set size, graduate hires), not the direction of the output response: gaps 0.999 / 0.958 / 0.789 (v = 0 / .5 / 1). "Signalling output falls with visibility" is a **metric convention**, not a mechanism-free prediction. | Predicted sign pattern fails because the stipulated premium `4(1−v)` reaches **zero at v=1**: the signalling market **shuts down** (applications 85.85 → 28.45 → 0.00), so measured true skill *rises* for both mechanisms (SG 0.499 → 0.627 → 0.796). T4.2's monotonicity reverses at v=1 for the same reason. **F4's v=0 leg is structurally unfirable** (HC adds +1.0 skill, so the mechanisms differ by construction). | B §1; PB §1 |
| **B5 queue vs HC** | The **decomposition** is the useful part: under responsive jobs the raw output gap is 0.200, of which the allocation-induced component is `~5.6e-17` and the residual is exactly the stipulated +1.0 skill on 20 of 100 people. Rank-vs-skill separation is a **rationing phenomenon**; an observed output gap can be allocation or productivity, separable only by a jobs assumption. | T5.1/T5.2 are near-tautological under the extreme rank rule ("all 80 young outrank all 20 older-diploma holders", ≤40 jobs ⇒ older hires **0.00** vs 7.61 reference). T5.4's "separation disappears" is **arithmetic**: the skill arm literally adds +1.0, so the raw gap cannot vanish. Attenuation 63.8%. | B §2; PB §2 |
| **B6 eligibility repeal vs blind ranking** | Design lesson: **single-lever credential policies can be nulls by construction.** Gate repeal alone is exactly **0.000** when credentialed supply (45) covers offers (35); both levers give 0.350; blind alone 0.000. A one-lever natural experiment is underpowered by design, and a null there is not disconfirmation. | Complementarity is a property of the two-stage screening architecture, and the no-op is arithmetic. The blind-ranking result is forced by the **zero credential–skill correlation** stipulation; with a positive correlation the contrast shrinks. Sensitivity 25/75 gives 0.133, still below the 0.25 "high" bar. | B §3; PB §3 |

**Assessment.** No rival is discriminated here, and the battery says so. B's transferable content is
entirely about **test design**: composition metrics, rationing-conditional allocation, joint levers. That
is a useful constraint on any future C3 attempt; it is not a result about HC, signalling or queues.

### Cluster C — capacity: floor / ceiling, enforcement, buildings (touches A10/R29, C4)

| item | genuinely informative (design) | artefact / forced by stipulation | source |
|---|---|---|---|
| **C7 capacity by level** | **T7c's failure is the most informative result in the cluster**: the Council predicted secondary capacity would convert < 50% of added seats; it converted **70.2%** (11.71 / 16.67 pp), with 15% of added seats idle (util 0.851). The toy therefore corrects the Council's own account: **saturation is a property of the gate / eligible pool, not of the level**. Floor +44.43 pp [44.19, 44.68]; middle +11.71; ceiling +4.58; ceiling max 11.67 pp; floor peak 90.46 pp. | **T7e is a wording defect**, not a mechanism result: its ceiling clause passes (11.67 < 50) and its "no level at 90" clause trips on the **floor** (90.46) — exactly the A10 "capacity buys the floor" reading, not a contradiction of it. T7d (`primary_only` ceiling +0.00) is **mechanically forced** by the unchanged middle (completion = seat used); the ceiling ceiling (11.67) is designed in by the sequential gate chain. | C §1; PC §1, §5 |
| **C8 enforcement × law** | Measurement warning with real force: a paper law moves the **register +9.91 pp** but attendance only **+1.09 pp** and completion +0.51 — register-based compliance would overstate the behavioural effect ~9×. Enforced law: attendance +18.63, completion +20.29; work displacement 18.17× larger at e=1 than e=0. | "Law alone is inert" holds only because the stipulated norm effect is small (`delta_norm = 0.010`); it is a **declared assumption**, and a larger norm term would fire F8. "Enforcement without law = 0.000" is **by construction** of the mapping (`e` multiplies `L`) — a built-in null, explicitly not a finding. Completion > attendance relies on the stipulated inspection-verifies-instruction channel. | C §2; PC §2 |
| **C9 buildings vs teachers** | One transferable measurement caution: **PTR is not usable places** — `teachers_only` has the best declared PTR (3.00) and completes 22.83 pp, below `split` (32.79 / 38.16 pp). Equal budget, composition dominates. | The whole experiment is the stipulated production function `admissions = min(physical, teacher_capacity, 120)`: rooms-only completion is **exactly 0.00 pp** because the function has **no unstaffed-seat channel at all**. T9a/b/c are near-tautologies of that choice; C itself flags the cells as mechanically forced. | C §3; PC §3 |

**Assessment.** C7's *failure* is more informative than C7's *passes*: it produced a genuine
re-specification (gate, not level) that the Council should keep. C8 is the cleanest pedagogy for the
de jure/de facto problem and the most relevant to C4's measurement, but its key sensitivity is an
assumed norm parameter. C9 is the clearest "artefact by construction" in the battery and should never be
quoted as a finding about buildings or teachers.

### Cluster D — timing, cohorts, temporary expansion (touches A6/A7/A10, C2)

| item | genuinely informative (design) | artefact / forced by stipulation | source |
|---|---|---|---|
| **D10 level-first order** | **The spacing negative is genuinely informative:** roll-out order moves crossing years (floor take-off 4 → 10; ceiling 17 → 21) and top-first capacity is wasted (upper-first has the latest ceiling, 21, and the lowest 30-cohort upper output, 1077 vs 1428.5), but **simultaneous expansion does not compress floor→ceiling spacing** — S is 11–13 years in every arm and the paired difference is **0.0** years. Spacing is set by the **credential pipeline**, not by capacity timing. | P10-1 (order preserved in 240/240) is a **design property**: a level cannot complete before the level below because the gate requires the previous credential. The A10 mirror (floor 94%, ceiling 76%, U90 never) is designed in. A **post-run comparator defect** (P10-3 compared to control instead of simultaneous) was corrected and the battery re-run from scratch; verdict unchanged, disclosed in D §4.3. | D §1; PD §2, §6.2 |
| **D11 cohort shock × capacity** | One definitional constraint worth keeping: **a demographic shock is only a shock when capacity fails to scale.** Frozen: up-cohort delays floor take-off by **+4** years and costs 8.7 pp per child; responsive: 0 years and 0.2 pp; DiD +4.0 (240/240). | Near-tautological: under responsive capacity the seat stock **per child is identical by construction**, so "no effect" is arithmetic. D itself says the 240/240 sign consistency is "the arithmetic forces this", and crossing years are degenerate (p10 = p50 = p90). Only 3 seats/cohort, so M1 is censored everywhere; this is a 50%-take-off toy, not a universalization-timing toy. | D §2; PD §6.3 |
| **D12 temporary expansion** | **Price vs belief is the useful distinction:** a fee waiver raises during-lease applications 30–36% and the poor share of upper completions 0.069 → 0.222 but leaves **nothing** after the lease (POST gap 0.0); the information arm leaves **+17.1%** applications in cohorts 5–7, decaying to +0.5% by 16–20. Persistence requires beliefs, not price. | Persistence magnitude is the stipulated adaptive belief (memory 0.70, reference flow 12). P12-2's hire-magnitude/decay FAIL is a **threshold-vs-engine mismatch** (skill-stock memory 0.8 ⇒ ~4–5 cohort time constant, so the declared 3-cohort halving was too fast), not a refutation. "Supply-only cannot raise applications" is a **model limitation** (applications respond only to observed credential flows), and P12-1b "hires flat" is definitional under frozen posts. | D §3; PD §6.1, §6.4 |

**Assessment.** D10's spacing result is a real correction to the Council's sequencing intuition and is
worth keeping as a design constraint (do not expect simultaneity to compress the pipeline). D11 is
near-tautological and should be cited only as a definition. D12's price/belief contrast is useful, but the
decay half-life is an assumption, so no magnitude should travel.

### Cluster E — market pull, sector access, information/roads (touches C1-adjacent, C3)

| item | genuinely informative (design) | artefact / forced by stipulation | source |
|---|---|---|---|
| **E13 migration / remittance** | Clean decomposition and a real measurement lesson: **count migrants once** (78.50 unique vs ≈900 person-cycles, ~11× overstatement). Route raises completion **+15.22 pp** [14.89, 15.54] with local formal posts **exactly 45** in every arm/seed; remittances add **+3.54 pp** [3.36, 3.71] / +8.05 applications. | Origin seats are **deliberately non-binding** (170 seats, peak applications 134), so this is a *demand-channel-only* construction: with binding seats the same push would appear as a queue, not completions (E says so). All four thresholds pass with wide margins — the design bought a clean illustration, not a discriminating one. Local output −1.27 (−1.7%) is a descriptive selection effect. | E §2; PE §#13 |
| **E14 sector shock × access** | **T14-P1c is the most useful negative in the battery:** a sectoral shock **expands total licensed completers by +24.68** (allowance ≤ 10), i.e. there is a **participation margin as well as a switching margin**. Any empirical "sectoral pull" design that cannot separate total participation from field switching will read general expansion. Access gate attenuates to ~0.30 of the open response (apps +106.50 open vs +32.26 closed). | The corner solution is an artefact: `SHOCK = 2.5` **exceeds the entire aptitude range (1.0)**, so switching is 100% and field B empties (apps B = 0.00) — this maximises the participation margin. A smaller shock was not predeclared and not run. T14-P4 vacancies over-predicted (8.35 vs ≥10; no-shock gated vacancies already 10.51). | E §3; PE §#14 |
| **E15 information / roads** | **With fixed seats, application-side interventions show up as queues and spatial reallocation, not completions**: info effect on admissions **−0.00002/hh** while the queue rises **+0.0481/hh**; roads dominate information (+0.2265 vs +0.0481) and reallocate admissions (nearest quartile 0.5875 → 0.4638; farthest 0.2358 → 0.3327). | The interaction (+0.0307 < 0.06 declared) is a **dose effect**: contact probability is stipulated 0.30 without a road vs 0.70 with, and the per-exposed-household effect is roughly equal in both regimes (+0.09 vs +0.11) — so it is not complementarity. T15-P3 fails by **0.002** on the queue margin (threshold artefact, not mechanism); roads cut a stipulated travel-cost term; kin transmission (+0.22) is stipulated. A disclosed **unit fix** (per-village → per-household) flipped T15-P3 from PASS to FAIL. | E §4, §7; PE §#15 |

**Assessment.** E's two negatives (participation margin; queues-not-places) are the cluster's real
content and are genuinely useful for designing demand-pull and access tests. E13 is a clean pedagogy but
constructed to be clean. E15's interaction is explicitly a dose artefact and its queue verdict is a
boundary artefact.

### Cluster-level negative/partial count

Four of the five clusters carry a headline negative or partial — **A** (A1 FAIL, falsifier fired),
**B** (five NOT MET; no sign pattern; no discriminator), **C** (two FAILs, one of which corrects the
Council's own saturation prediction), **E** (four of fourteen thresholds fail) — and **D** is PARTIAL on
#10/#12 and SUPPORTED on #11, with four threshold misses plus a missed secondary interval of its own. The
battery is therefore **more
informative in its failures than in its PASSes**, which is the right way round for design evidence but is
still not evidence about the world.

---

## 2. Decision-relevant takeaways for the programme (eight)

1. **Supply: the object is net, not gross.** Any future capacity-expansion claim or C1 test must measure
   **private exit and net seats**, not gross public seats (A2: gross +20 vs net +9.73; 42/200 seeds net
   ≤ 0 at 30-seat capacity). The magnitude in the toy is a mixture and a knife-edge; the *design
   requirement* is what travels.
2. **A fixed cost alone does not buy asymmetry — do not parameterise hysteresis.** A1's negative plus
   A3's timing condition mean the C1 cell must measure (i) the decision-to-installation **lag**, (ii) the
   **exit trigger**, and (iii) entry and exit responses **separately**; a single "hysteresis" parameter
   is not licensed by anything in this battery.
3. **Capacity buys the floor; saturation is gate-determined, not level-determined.** C7's T7c failure
   re-specifies A10's mechanism: at the ceiling the binding object is the **eligible pool / gate**, not
   seats (conversion 70.2% at secondary with 15% idle; ceiling ≤ 11.67 pp even when every level doubles).
   This is a better *statement* of A10, not evidence for it.
4. **Enforcement and law are complements; register compliance is not classroom compliance.** C8: paper law
   moves the register +9.91 pp and attendance +1.09 pp; enforcement without a statute does exactly
   nothing (by construction). For C4 this means **de facto enforcement must be measured directly**;
   enrolment-on-the-books is not compliance.
5. **Composition beats total spend at equal budget — but this is a stipulated production function.** C9's
   only transferable content is the **measurement caution**: a good PTR is not usable places
   (teachers-only PTR 3.00 but 22.83 pp vs split 32.79–38.16 pp). Do not cite C9 as evidence that
   buildings are useless.
6. **Rival non-separation constrains the C3 design.** Visibility does not produce the predicted
   HC-vs-signalling output sign pattern (B4); queue effects are rationing-conditional and the output
   gap is confounded by the treatment's direct skill increment (B5); single-lever credential policies are
   nulls by construction (B6). A future C3 attempt needs **composition metrics, a joint lever, and a
   rationing measure**; a one-lever null will be uninformative.
7. **Timing: order shifts years, the pipeline sets spacing.** D10 (S = 11–13 years in every arm; paired
   difference 0.0) plus D11 (cohort effects only under frozen capacity) mean a C2-type test must be about
   the **capacity-scaling rule** and the expectation/belief channel (D12: price fades, beliefs persist),
   not about the size of a temporary push.
8. **Demand shocks have a participation margin; access/information effects are queues.** E14's +24.68
   total-completer expansion and E15's flat admissions (+0.0481 queue) mean any demand-pull or access test
   must separate **participation from switching** and **applications from admissions**; otherwise it will
   read general expansion or a queue as a completion effect.

---

## 3. What this is not — no evidence, no reopening

**None of the fifteen experiments is evidence about the world.** Every number is a property of stipulated
rules: there is no observed series, no calibration, no historical test, no equilibrium, no prices, no
quality margin, no dropout, and no external validity beyond the arithmetic of the toy. A toy "PASS" means
only that the stipulated rules mechanically generate the pattern predeclared for the toy; a "FAIL" means
only that they do not. Both are statements about the model.

**None of this reopens C1–C4, and nothing here may be cited in support of any of them.** The phase stays
CLOSED at PARTIAL / DESCRIPTIVE / EQUIVALENT, and the honest headline is unchanged. The only admissible
re-openers remain exactly these four, and each requires **observed** evidence, not a toy:

- **C1** — correct-sign OOS income-scaling exponents **generated with no exponent supplied as a
  parameter** (PASS-CONDITIONAL at best); the route is the observed **provider-entry supply-response
  cell** (entry elasticity first, then the sign flip, or a recorded negative).
- **C2** — fixed-behaviour crossings within **±5 y** on the corrected milestone vector, **including the
  primary-2017 completion crossing** that the A1 test vector omitted.
- **C3** — a **discriminating** push/pull/queue/capacity test, which needs user-approved **PSA / WB
  Enterprise Surveys** data.
- **C4** — **observed annual capacity and enforcement series** (de facto, not de jure).

What would **not** reopen anything: another toy, a re-run with different seeds, a re-parameterised arm
that turns a FAIL into a PASS, or a toy with more clusters. Those are pedagogy, not evidence.

---

## 4. Big-picture step-back

1. **Goal restated:** a longitudinal model in which massification/universalization is produced by the
   interaction of schooling, government and markets — each standing the others up — with cohort flows
   and country/sector variation; shadow secondary; the phase's product is the bounded negative +
   equivalence map.
2. **KEEP:** the **A1 descriptive write-up** under D67/D68 (crossings + spacing, capacity floor-vs-ceiling,
   ceiling residual **UNABLE**, rivals, scaling **FAIL**), the bounded negative result and the
   equivalence/identification map (D58), the gate/rules, and this battery **only as a design appendix**
   (mechanism menu, clearly labelled, never in results tables). The C1 provider-entry cell remains the
   single admissible re-opener, as a design.
3. **PARK:** the twelve mechanism threads as *evidence* (they are illustrative); the C3
   visibility/requirement test (hard data, untested rivals); the C4 de facto enforcement panel; portability
   (PARKED-ARMED, D75); the KHM holdout.
4. **KILL:** citing any toy number as an estimate or a finding; re-running the toys to rescue a FAIL or to
   firm up a thin PASS (A2 0.486, A3 8.08, C7 T7c/T7e, D10 P10-2, E14-P1c, E15-P1/T15-P3); reopening
   C1–C4 on toy grounds; further scaling repair (R27); any "capacity explains the timing" claim (D61/R28).
5. **Critical path:** **A1 write-up (addendum C1–C10) → publish.** The toy battery is off the critical
   path; its only forward use is to constrain the design of the observed provider-entry cell.
6. **Drift check — one red flag stands.** The battery is 15 experiments / ~356k result rows / 30 MB, and
   the drift risk is **mistaking volume for evidence** and letting toy proliferation substitute for the
   observed cell that C1 actually needs. Mitigation: the ILLUSTRATIVE label, the results-table ban, no
   re-runs, and this review's record that the battery is design-only. (Housekeeping, not research: the
   committed copy lives under `…/10_massification/extensions/codex_2026-11-20/toys_2026-11-20/`, while the
   documents reference `extensions_archive/…`; an **untracked duplicate** of the same tree (~30 MB) sits at
   the repo root, identical apart from five top-level files — `COUNCIL_REVIEW_014.md`,
   `COUNCIL_TOY_SPECS_015.md`, `SHA256SUMS.txt` and the two base-model zips. Council did not move or delete
   anything; the Lead may reconcile path labels and the duplicate.)
7. **If only one thing mattered this week:** the **A1 write-up**, not another toy. If one thing had to be
   dropped, it would be the entire battery — the phase loses no evidential content by dropping it, because
   it never had any.

---

## 5. The single most promising mechanism follow-up — and its falsifier

**Follow-up: a two-friction provider-entry cell, measured on observed data (the C1 route), not another
toy.** The battery's one forward-looking message is that supply response is about **frictions**, and the
frictions it names are measurable: an **entry lag** (decision → installed capacity), an **exit trigger**
(the customer count below which a provider withdraws whole capacity), and **net-of-exit seats**. The
predeclared cell is the brief-014 §3.1 observed provider-entry test with three estimands — (i) entry and
exit elasticities to demand **separately**, (ii) the decision-to-installation **lag**, (iii) **net** seats
and admissions after private exit — using public provider-approval / school-count / HEI-programme series
in high- vs low-demand-exposure regions (PHL: BPO/remittance/income growth), with the second stage being
the OOS income-scaling exponents generated **without** an exponent as a parameter.

**Falsifier (predeclared):** if the observed entry and exit responses to a demand shock are
**indistinguishable** — a paired exit/entry ratio inside a declared `1 ± 0.25` band, mirroring A1's
`0.008`-vs-`0.25` structure — **and** net seats retain **≥ 90% of gross** (mirroring A2's `R ≥ 0.90`
falsifier), then the friction/asymmetry story has no bite: record the supply channel as **absent**, write
**C1 as a negative result**, and do not add a third friction or another toy. (If the data are blocked, the
fallback is a single predeclared toy with a sunk-cost band **and** an entry lag, not a new battery; its
falsifier is the same.)

**Why this one:** it is the only follow-up in the battery's design space that could ever change a phase
verdict, it uses the two numbers the toys actually sharpened (net-vs-gross and the lag), and its failure
mode is a recorded negative rather than another iteration.

---

## 6. Limits — stipulated parameters, load-bearing assumptions, disclosures

### 6.1 Stipulated parameters (none estimated, none calibrated)

Representative vectors, all recorded in the manifests: **A** — premium 4.0, 100 households, tuition 2.0,
variable cost 1.0, budgets {1.5, 4.0}, F ∈ {4, 8, 12, 15} with `bk = cap` in the primary arms,
cap ∈ {4, 8, 15, 30}, public seats 30, boom length 4 (MA). **B** — 100 people, 30 public seats, private
capacity 30, fixed cost 12, 40 jobs, HC +1.0 skill, SG premium `4.0·(1−v)`, employer score
`v·skill + (1−v)·credential`, fixed jobs U{35..40}, responsive jobs 100, 35 offers, credential shares
45/55 and 25/75 (MB). **C** — N=120, 30 cohorts, fees (0.20, 0.36, 0.55), base seats (55, 20, 7), gates
(0.30, 0.45, 0.35), cash groups (0.24, 0.62, 1.05), capacity ×2, enforcement e ∈ {0, .5, 1} with
`delta_norm = 0.010`, `enf_coef = 0.35`, budget 480, room 12, post 60, retention π ∈ {0.60, 0.90}
(MC). **D** — N=120, 30 cohorts, fees (0.20, 0.36, 0.55), work multipliers (0.85, 1.35, 1.80), seat0
(18, 0, 0) or (108, 100, 12) for #12, build_limit 12, PV δ=0.97 with 40 seat-years/level, 3 seats/cohort
investment for #11, belief memory 0.70 and reference flow 12 for #12 (MD). **E** — N=200, route premium
2.4, 45 local posts, origin seats 170; shock 2.5, seats 150/field, gate 30%; 60 households/village, seats
(16, 6, 2), contact probability 0.30/0.70, kin +0.22 (ME).

### 6.2 Load-bearing assumptions (the results move when these move)

| assumption | where it carries the result | source |
|---|---|---|
| **All-or-nothing provider exit** | A2's bimodality and R = 0.486; at F=$12 R = 0.665 (T2a would fail). Real providers can shrink/hold price/cut quality. | A §2 |
| **A1's contemporaneous decisions + `bk = cap`** | The near-symmetry and the knife-edge break-even; the disclosed divisible-rule robustness supports the null but not the magnitude. | A §1; PA Amd 1 |
| **B4's premium `4(1−v)` degenerating at v=1** | The signalling cell has 0 applicants; T4.1/T4.2 failure is partly this stipulation; no alternative premium was predeclared or run. | B §1 |
| **B5's credential-inflation queue** ("all young outrank all older-diploma") | Older-group hires 0.00; a weaker queue would null T5.1/T5.2 by symmetry. T5.4's failure is the direct +1.0 skill increment. | B §2 |
| **B6's zero credential–skill correlation** | Blind ranking raises uncredentialed offers; a positive correlation shrinks the contrast. | B §3 |
| **C7's "completion = seat used" + sequential gate chain** | `primary_only` ceiling exactly 0.00; ceiling max 11.67; the floor 90.46. | C §1 |
| **C8's small norm effect (0.010) and `e × L` mapping** | "Paper law inert" and "enforcement without law = 0" (the latter is a built-in null). | C §2 |
| **C9's `min(physical, teacher_capacity)` function** | Rooms-only completion exactly 0.00 pp — no unstaffed-seat channel exists in the specification. | C §3 |
| **D11's per-child capacity definition** | The responsive arm has identical seats per child by construction, so the interaction is arithmetic. | D §2; PD §6.3 |
| **D12's adaptive belief (0.70 memory, reference flow 12)** | The persistence and the decay half-life; the hire-decay FAIL is a memory mismatch (skill stock 0.8). | D §3 |
| **E13's non-binding origin seats** | The completion response is a demand-channel construction; with binding seats it would be a queue. | E §2 |
| **E14's corner shock 2.5 > aptitude range 1.0** | 100% switching, field B empties; maximises the participation margin (the qualitative point survives; the magnitude is the corner). | E §3 |
| **E15's exposure 0.30/0.70 and kin +0.22** | The interaction is a dose effect, not complementarity; kin transmission is stipulated and carries no evidential weight. | E §4 |

### 6.3 Pre-run amendments, disclosed failures, and verdict fragility

- **A — Amendment 1** (before the final 200-seed run, after a 6-seed mechanics smoke): capacity rule set
  to fixed lumps, high-F break-even standardised at `bk = cap`, the pre-amendment `F = $12` retained as a
  reported sensitivity cell. **Thresholds and falsifiers unchanged**; the smoke's `R ≈ 0.82` is disclosed
  and is why `$12` was kept rather than dropped (PA Amd 1).
- **C — Deviation #1** (before the 200-seed run, after a 3-seed smoke): F7 gained an applicability
  condition (only arms whose own floor gain ≥ +2.0 pp) so the ceiling-vs-floor comparison is not a
  degenerate 0-vs-0. No PASS/FAIL threshold changed; predeclaration re-frozen (`b0b0bdef…`); post-run edit
  log empty (PC §5–6).
- **D — §6 pre-run amendment**: #11's capacity rule redefined to absolute vs per-child delivery (and
  employer made per-child invariant) and #12's starting state/information regime redefined (a
  cohorts-2–4 upper-secondary lease is vacuous from the `takeoff.py` start). Thresholds unchanged.
  **Post-run code defect**: P10-3 compared to `control` instead of `simultaneous`; the comparator was
  fixed and the **whole battery re-run from scratch**; P10-3 still meets its band and the #10 verdict is
  unchanged (D §4.3).
- **E — disclosed unit fix**: T15-P3's queue was first compared per-village against a per-household
  margin and recorded PASS; corrected to the declared per-household rule, verdict became **FAIL**
  (2.888 → 0.0481). No parameter/seed/threshold changed; E14 definition strings clarified for
  readability (E §7).
- **B — no amendment, but one design defect**: F4's v=0 leg is **structurally unfirable** because the HC
  arm adds +1.0 skill by construction (B §1, §5).
- **Verdict fragility (read every PASS with this table):** A2 `0.486` vs `< 0.50` (a 14-seed swing
  flips it; `F=$12` gives 0.665); A3 `8.08` vs `≥ 8.0` (0.08 seats); C7's T7c is a direction-correct
  magnitude miss and T7e is a wording defect; D10's P10-3 `lower_first` is exactly `1.0` at its band;
  E15's interaction `0.0307` clears its falsifier floor `0.03` by 0.0007 and T15-P3 misses its queue
  margin by 0.002. **These are boundary artefacts; do not read them as effects.**
- **Inference conventions differ by cluster** (A/B: no SEs or p-values; C/E: 95% normal-approximation
  CIs on paired differences; D: medians/p10/p90). Disclosed in each predeclaration; no cluster uses
  significance language to make a claim about the world.
- **Path/label anomaly:** the committed artefacts are under
  `…/10_massification/extensions/codex_2026-11-20/toys_2026-11-20/`, but the documents and several
  manifests record `extensions_archive/…` (a repo-root **untracked duplicate** of the same tree exists,
  ~30 MB, identical apart from the five top-level review/spec/SHA/zip files noted in §4). This is a
  provenance-label issue, not a data-integrity issue — all 60 hashes verify — but a reader following the
  in-document path will land in the wrong tree.

---

## 7. Bottom line (plain language)

The toys do what toys can do: they show **why** certain intuitions are or are not mechanical. They show
that a public expansion can be partly eaten by private exit (A2), that a fixed cost by itself does not
make supply react asymmetrically (A1), that capacity moves the floor while the gate holds the ceiling
(C7), that a law without enforcement is a register entry (C8), that composition matters at equal budget
(C9, mostly by construction), that visibility and one-lever credential policies do not separate rivals
(B4–B6), that order shifts crossing years but not the pipeline's spacing (D10), and that demand and
information shocks show up as participation and queues before they show up as completions (E14–E15).
**None of that is evidence about the Philippines, about massification, or about any historical episode.**
The phase's product remains the bounded negative result and the equivalence/identification map; the one
follow-up worth doing is the **observed provider-entry cell**, and its falsifier is a symmetric entry/exit
response with net ≈ gross. If that response is not there, the honest answer is the closeout's negative
result, and the toys are a well-labelled appendix — not a reason to reopen anything.

**Dissent / cautions.** PATRINOS — A2's "net" is an accounting identity once whole-provider exit is
stipulated; the observed cell must measure exit, not assume it. PAGE — the battery's real value is the
mechanism menu and the design constraints, not any number; C7's T7c is the one result that changed how
the Council should *state* A10. CARTWRIGHT — the falsifiers that could not fire (B4/F4, C8's built-in
null, D10's P10-1) must never be reported as "falsifier not triggered" in any external summary. LUTZ —
the thin margins (A2, A3, E15) are boundary artefacts and should not be quoted as effects even inside the
fleet.

— Council-2, brief 015 follow-on (design review only; phase CLOSED; nothing pushed; no external messages).
