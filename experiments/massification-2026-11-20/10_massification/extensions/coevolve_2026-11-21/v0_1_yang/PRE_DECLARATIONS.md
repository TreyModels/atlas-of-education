# v0.1-YANG PRE-DECLARATIONS — wiring the Yang gate margin into coevolution (BEFORE ANY RUN)

**Label: `SIMULATED` / `ILLUSTRATIVE`.** New extension; **coevolve v0 and its frozen predeclaration are untouched.**
This document is to be hashed before any run (it is: see `PRE_DECLARATIONS.sha256`).

## 1. The requested wiring (as specified by the Lead, 2026-11-21)

City-size block: town size N ∈ {50k, 200k, 500k, 1m, 2m}; household/cohort structure FIXED; N enters **only**
through Yang occupational variety and the resulting gated share (this isolates the gate margin, not demography).
Yang mapping `D(N)=128·ln N + c`, anchored `D(1e6)=500`; `g(N)=clip((D−D(50k))/(D(2m)−D(50k)),0,1)`; gate-mapping
variants linear / proportional / convex (scale U[100,400]) equal probability. Gate wiring: g(N) sets the **share of
the upper-secondary and tertiary gate places that carry a credential requirement** (gate incidence rises with city
size), existing gates/controllers otherwise unchanged. Designs `none` (g=0), `yang` (g(N) fixed), `yang_endog` (gate
incidence rises when applicants/gated place > 3, falls when < 1, bounded). MC: 150 draws × paired seeds {0,1} ×
sizes {200k,500k,1m} × designs {none,yang,yang_endog} = 2,700 runs; CRN; bar completion gap ≥0.5 pp at ≥3 sizes =
ACTIVE; report leaving gap and coexistence metrics; boundary check against the Yang-toy inert draws; two runs
byte-identical; pre-shock PASS; runtime target < 45 min with a declared reduction if projected over.

## 2. FEASIBILITY TEST — declared in advance (the stop clause)

The Lead explicitly permits a clean **"not wireable as specified"** outcome. This predeclaration therefore fixes the
**feasibility criterion before any run**:

> **The primary wiring is implementable within the model's existing gate objects iff there exist gate applicants
> who do not already hold the credential that the gated place would require.** If the number of such applicants is
> **exactly zero** across the audited runs, the share g cannot change any admission decision: the wiring is
> **`INERT-BY-CONSTRUCTION`**, and the requested primary MC would be meaningless (it would report 0 by design, not
> by result). In that case we **STOP**, record the design mismatch with file:line evidence, and do not force a
> variant that changes the model's gate objects.

The audit (run once, before any MC) instruments the frozen v0 model (read-only import; no modification) and counts,
for every gate and every year and seed: applicants, and applicants whose `cred` is below the gate's prerequisite
credential (`upper-secondary` requires completed lower secondary, `cred≥2`; the university/post-secondary gate
requires completed upper secondary, `cred≥3`; allocation candidates are checked level by level). The audit writes
`results/CREDENTIAL_GATE_AUDIT.json`; it runs 2 seeds of the baseline arm.

## 3. If (and only if) the feasibility test passes

Then, and only then, the declared MC is run exactly as in §1 (the ranges in the Lead's brief; MC predeclaration
detail would be appended here and re-hashed **before** the MC run). **No parameter, design or bar may be changed
after any result.**

## 4. Declared alternative wiring (future work; NOT run here)

The Lead's declared alternative — `g(N)` multiplies the credential value `C_value` (a return-side wiring rather than
a gate-incidence wiring) — is recorded as **future work**. It is **not** run in this extension and must not be
presented as the requested primary wiring.

## 5. What this extension does NOT claim

No observed data; no country claims; no causal or direction claims; no re-tuning; coevolve v0 frozen predeclaration
and all closed records untouched. Labels: `SIMULATED` (model output), `DERIVED` (audit arithmetic),
`ILLUSTRATIVE` (toy).
