> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# SYNTHESIS 001 — reproduction + literature audit (for `lead`)

**Headline.** The reproduction is clean and should be trusted as an implementation check, not a theoretical one. Of
the nine claims, six are simulation or literature findings that follow from coded rules or documented prior work;
the one theory-separating test (C3) is not yet a fair beat because the rival has no formal sector; and the one
defensible novelty — the floor/race decomposition, with floor *movement* as the contribution inside a ranked queue —
is small, conditional, and must replace "intensification requires ranking" as the headline. Yoo (2003) does contain
the gate-clustering result; say so.

## Verdict table

| ID | Claim | Verdict | Imposed by equations? | Reason / what would change it |
|---|---|---|---|---|
| C1 | 6-arm table reproduces | **ESTABLISHED** | no (implementation) | means match stored within 0.013 sd; slopes ≤0.07 apart; rerun at 4 reps |
| C2 | floor alone ≠ intensification; ranking gives it | **SIMULATION-ONLY**, sign near-analytic | **yes, sign**; decomposition discovered | rank vs lottery changes allocation and signal together; ensemble needed |
| C3 | grad-supply shock separates from competitive market | **NOT ESTABLISHED** as separation; CONDITIONALLY SUPPORTED only for income sign | **yes** (fixed slots/vacancies; rival has no formal sector, formal rate 0.000) | matched-elasticity cell with formal margin in rival |
| C4 | actor knockouts 3.45/1.49/1.19 of 4.29 | **SIMULATION-ONLY** | partly (target removed by construction; 1.49→0.04 weak-skill) | report regime dependence; do not claim necessity |
| C5 | tutoring clusters where bar sits among takers | **SIMULATION-ONLY** | **yes** (coded payoff discontinuity; exogenous bar sweep) | Yoo 2003; endogenous-bar arm would be new |
| C6 | Yoo already derives effort-near-cutoff | **ESTABLISHED** (literature) | — | cite it; restate Prediction 3 as prior work |
| C7 | 33/68 claims unresolved; October drops external numbers | **ESTABLISHED** (audit) | — | counts reconcile; publish the register |
| C8 | Ng & Yip likely Gee conflation | **UNABLE TO ASSESS** | — | library check before submission; do not assert |
| C9 | cohort accounting conserves | **UNABLE TO ASSESS** | — | artifact only at `/tmp`; copy into `05_experiments/` |

**Fatal vs fixable.** Fatal as currently written: C3's "separates the accounts" (F4, rigged rival on the formal-rate
outcome) — repairable only by running the matched cell, then relabelling. Fixable: C2/C5 novelty claims (F8-lite,
overclaim), C4 conditionality, C1 rep count, C8 citation, C9 artifact location. C6/C7 are not defects — they are
findings to report.

## Answers to the Lead's four questions

**Q1 — what is imposed.** C2's sign, C3's displacement, C5's gate ranking are consequences of coded rules (rank
allocation; fixed slots/vacancies; a payoff discontinuity with an exogenous bar). What is discovered: the
*decomposition* — with ranking on, the adaptive floor's slope (−0.068) is steeper than the fixed floor's (−0.037);
floor movement, not floor level, adds intensification, a small but real result absent from Yoo. C4's employer
contribution is definitional at the target (credential hiring set to zero) and regime-dependent (1.49 → 0.04).

**Q2 — strongest defensible novel claim given Yoo.** Not the gate result, not "intensification requires ranking."
The defensible package is: (a) the floor is an *eligibility* object distinct from rank, explaining exclusion where
no ranked contest exists; (b) inside a ranked queue the floor's distinct contribution is its *movement*; (c) floors
are many, institution-specific, dated, with grandfathering — the Philippine case's real comparative contribution.
That is a conceptual + simulation paper (comparative education / sociology of education), not an empirical labour
paper. The state-capture proposition is not model-supported and must stay a research proposition.

**Q3 — ranked shortlist for ~30 min compute** (all costs include dev time; the grad_supply run itself took 54 s):

1. **Matched-elasticity rival (highest value; most likely to change Trey's mind).** Arms: surplus vs competitive CES
   *with a formal/informal margin in both*, σ ∈ {0.5, 1, 2}, same tuition shock and vacancy path; 6 paired reps.
   Estimand: Δ diploma holders' absolute income **and** Δ formal-employment probability. Pre-declared threshold: if
   the rival reproduces a fall in formal probability (or Δincome ≤ 0) at any σ, C3's separation is **CONTRADICTED**;
   if not, C3 becomes **CONDITIONALLY SUPPORTED**. Cost ~10–15 min (mostly coding the rival's formal sector).
2. **Yoo nesting + equation knockout (protects novelty).** Arms: (a) fixed-cutoff payoff only, no suppliers, no
   endogenous floor; (b) full C5 model. Estimand: retention of the basic-bar sweep (0.03 → 0.77). Threshold: if (a)
   reproduces ≥ half the sweep, C5 is a restatement; report it as such. Cost ~5 min compute + a one-page analytic
   derivation (free, and the more convincing artefact).
3. **Allocation-rule knockout / recovery (tests imposed-vs-discovered).** Arms: rank-order vs employer-specific
   cutoffs vs random-among-eligible, utility spec held fixed. Estimand: sign of the investment-return slope.
   Threshold: a sign flip in the ranked arm at fixed utility → intensification is allocation-rule-specific. Cost
   ~5 min. *Cheap fourth if compute remains:* the 4-rep floor-test rerun (~7 min, 2 workers) to close the brief's own
   admitted gap — low mind-changing value, but it removes a reviewer objection.

**Q4 — citation visibility.** Make C6–C8 **visible**, not quiet. C6 and C7 are verified findings and belong in the
paper's "Prior work and what is new" subsection (cite Yoo 2003 and Kim 2007; restate Prediction 3 as prior work, not
discovery). C8 is unresolved: label it a citation check pending, do not assert the conflation. Give Bjørn the audit
trail (claim register, model cards) rather than a silent fix; a referee who finds Yoo will discredit far more than
the correction costs. C7's unresolved claims should be footnoted as such in the report.

**Most publishable:** the floor/race decomposition plus the many-floors, dated-reader Philippine institutional
analysis (comparative education / sociology of education). **Most falsifiable:** Prediction 2's graduate-supply shock
with formal demand roughly fixed — the one claim that can be killed by matched-elasticity evidence.

**One thing first:** run experiment 1 (matched-elasticity rival). It is the only result that can change the paper's
theoretical claim rather than its presentation. **What the Council needs to review it:** the run log, the rival's
formal-sector and vacancy rules, paired seeds, and the pre-declared threshold above.

**UNABLE TO ASSESS:** C8 (sources unavailable), C9 (artifact in transit). **Panel:** the Lead's functional
roles are staffed by AI composites drawing on Page (2018); Collins (1979/2019); Psacharopoulos & Patrinos (2018);
Bray & Lykins (2012); Cartwright (1999, 2012), with the shadow-education composite under the mandatory rule.
