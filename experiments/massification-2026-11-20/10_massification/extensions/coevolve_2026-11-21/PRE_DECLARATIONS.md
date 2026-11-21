# PRE-DECLARATIONS — COEVOLUTION v0 (mutual adjustment; towns, providers, gates, cohorts)

**Status: FROZEN-BEFORE-BUILD.** Written **before any line of the simulator exists**, per the user's directive
(`DESIGN_BRIEF.md`, 2026-11-21). **Label: `SIMULATED`** on every simulator output. **No observed series is fitted,
no known country outcome is targeted, and no causal or direction claim is licensed.** This document predeclares
the v0 rules, parameters, report-card computations, the decisive coexistence test, the counterfactuals and the
falsifiers. It is hashed and the code must refuse to run on a hash mismatch.

**Closed records untouched.** The 2026-11-20 massification phase is CLOSED (D76/D77/D150/D154/D167); the
gate-passed write-up is not edited; the Q-5 correction and the B-1 footnote remain `applied = false` pending the
user's decision. This is a **new modelling phase**, not a reopening.

---

## 0. The three demand objects (kept distinct)

1. **Knowledge** — the child learns to do/understand something (a production/consumption value).
2. **Education** — the child attends the institution and obtains the experience, relationships, standing and future
   options it confers.
3. **A credential** — without the certificate the child cannot apply to the next gate.

The v0 household decision carries **three declared weights** `(w_K, w_E, w_C)`; they can coincide in one purchase.
**Observed demand is the decision, not a measure of values:** identical spending/attendance under different choice
sets implies different values, and **spending alone cannot separate the three objects** (the FFS analogy: a farmer
may value knowledge, learn the practice, and decline it at the prevailing price). No object is inferred from an
observed outcome in v0.

## 1. The v0 system

**Geography.** One **town** (district centre) and **N_v = 8 villages** at declared distances
`d_v ∈ {2, 4, 6, 8, 10, 12, 15, 18}` km from the town, village population weights declared in §13.
**Levels:** primary (6 years), lower secondary (4 years), upper secondary (2 years), post-secondary **non-tertiary**
(1–2 years), tertiary/university (4 years). The elite/selective secondary is one upper-secondary track in the town;
ordinary secondary places exist in the town and, endogenously, in villages (rural classes).
**Time:** annual steps, years `t = 0…29`; cohorts enter primary at age 6; the run follows 24 cohorts.
**Population:** 1,200 children per cohort (town 320, villages 880 by declared village weights).

**Agents and state (per child/year):** age, level, grade, enrolled, repetition count, exam score (ability +
learning + tutoring), household income class (poor/non-poor), village, distance, siblings, child labour value,
tutoring hours (catch-up/gate), completion history, transition outcome.
**Providers/controllers (per year):** district authority budget and seat decisions; private provider entry
decisions; selective gate controller (exam threshold and places); university gate controller (exam + fee);
employer hiring-requirement rule.

## 2. Decision 1 — household next-year choice, with an actual alternative

Each household with a child of school age compares the declared value of **attending next year** with the declared
value of **the actual alternative** (the child works at home/market for the declared child wage, or stays home).
Attendance value, for level `L`:

`V_att = w_K·K_L + w_E·E_L + w_C·P(gate pass ⇒ credential path)·C_L − fees_L − travel(d_v) − θ·child_wage + β·OptionValue(L+1) + ε`

- `K_L` — knowledge gain (declared per-level learning value),
- `E_L` — education/experience value (declared per-level),
- `C_L` — credential/option value (declared per-level, **multiplied by the gate-pass probability** at the next
  transition and the declared credential weight `w_C`),
- `OptionValue(L+1)` — declared continuation value of keeping the next gate open,
- `travel(d_v)` — declared per-km annual travel cost (commute or boarding),
- `θ·child_wage` — declared opportunity cost (θ = declared child-labour share; `child_wage` rural/urban declared),
- `ε` — household taste (declared distribution, seed-driven).

**The alternative is real:** a child who does not attend is on the labour/home branch and may re-enter at declared
cost; stopping forgoes the option value. **Attendance requires the gate to be open** (a place secured), so a
household cannot "demand" a place it cannot obtain.

## 3. Decision 2 — endogenous supply (no seat totals in advance)

**District authority (per year, per level):** budget `B_t` (declared per-capita rule, not a seat path). It observes
declared **unserved eligible children within reach** (village children with no place within declared accessible
distance) and can:
(a) **open a rural class** in a village if unserved eligible children there ≥ declared class size `K_class` and
budget ≥ cost/section; (b) **add a section** at the town school under the same rule; (c) **spend elsewhere**
(declared quality/instruction improvement, no seats). Budget not spent on seats is spent on quality at declared
effect. **Seat counts are outputs of these decisions; no exogenous seat total, capacity path or GER target enters
the run** (this is the binding D0 rule; see §8.1 verification).
**Private provider (per year):** enters a village/level if expected fee revenue from households able to attend
(distance/fee/income) ≥ declared fixed + variable cost per class; exits if revenue < declared variable cost for
`K_exit` consecutive years. Private places are a **decision**, not an input.
**Rural community failure:** a village may have many willing children yet fail both tests (district budget
insufficient, private fees not sustainable) — this is an **outcome** the run reports, never an input.

## 4. Decision 3 — named gates with controllers

Four transitions, each with a named controller and a declared rule:
1. **Primary completion → any lower-secondary place:** place secured if a secondary place is allocated
   (residence catchment: nearest provider within declared reach, or a village class) and the household accepts.
2. **Lower-secondary completion → any upper-secondary place:** same allocation rule; ordinary upper-secondary
   places exist in the town and (endogenously) villages.
3. **Upper-secondary → selective/elite secondary track:** admission by **exam score ≥ declared threshold** and
   **selective places** (fixed declared K_sel, an institutional constraint, not a modelled decision); qualified
   applicants above places are **turned away** (oversubscription).
4. **Upper-secondary/selective completion → university:** **exam score ≥ declared threshold AND fee paid**; places
   are declared (K_uni) and rationed by rank. **Post-secondary non-tertiary** is a separate declared track with its
   own fee and completion convention.
**Residence, examination and fees are each declared controllers;** a gate can combine them (declared per gate).
**No gate is supplied with the run's own next-year NER.**

## 5. Tutoring — catch-up and gate, concentration as an output

Two declared tutoring motives, priced and access-constrained:
- **Catch-up:** a pupil whose declared score falls below the declared passing/instruction-following threshold may
  buy catch-up hours at price `p_c` and distance-constrained access; it raises learning and reduces repetition/failure.
- **Gate:** a pupil whose declared admission margin to the selective gate (or university gate) is within a declared
  band may buy gate hours at `p_g`; it raises exam score toward the threshold.
Tutoring hours are chosen by the household under its budget constraint and declared weights; **provider availability**
(distance/price) constrains them. **The concentration of tutoring around gates is an OUTPUT inspected after the
run** (gate hours per selective applicant / catch-up hours per non-selective pupil, by family type), never an input
or a fitted target.

## 6. Decision 4 — cohort feedback (three declared responses, introduced separately)

(a) **Completers create demand for the next level:** the number of primary completers changes the eligible pool and
the district's declared opening rule for secondary places (already in §3).
(b) **A nearby class changes primary persistence:** a household's declared continuation value of primary includes
the **presence of a secondary place within reach** (`OptionValue` increases if a secondary place exists within the
declared reach for the child's village), so a secondary opening can raise primary persistence of **younger cohorts**.
(c) **Graduates induce employer response:** the declared hiring-requirement rule
`req_t = req_0 + λ_req·(graduate_share_t − g0)` raises the credential required for a given job as graduates
accumulate; declared returns to a given credential fall with graduate supply (`return_t = return_0·(1 − λ_ret·(share_t − g0))`).
**Baseline starts with the economy steady** (all three responses OFF); each response is then introduced separately
(and jointly) in declared counterfactual arms, so the run can say **when** it changes the path.

## 7. Report card A — the statistical portrait (computed from pupil records)

For each year `t` and level `L`, from pupil-level records only (no external denominators):
- **NER_L(t)** = children of the **official age band** for L enrolled at L ÷ children of that age band in the
  population (≤ 100 **by construction**; asserted at run time).
- **GER_L(t)** = **all** children enrolled at L (including repeaters/over-age) ÷ official-age population for L.
  **May exceed 100**; repeaters and over-age are reported separately, never capped.
- **Out-of-school(t)** = children of the level's age band not enrolled at that level **and not enrolled at a higher
  level**; children at a higher level are reported separately (inside the conventional NER numerator's blind spot).
- **Tertiary GER** uses the **standard five-year age group immediately after the official secondary leaving age**
  (declared ages); repeaters/over-age reported.
- **Cohort completion** (share of a cohort completing each level by a declared age), **transition rates**
  (level-to-level, by gate), **rural–urban** differences for every above.
- **Post-secondary non-tertiary** reported separately from tertiary.
- **UIS metadata** (country series, age bands, level mappings) is **HELD** — flagged as a verification item; **no
  cross-country comparison is made in v0**.

## 8. The decisive test — coexisting withdrawal and competition (v0 baseline)

### 8.1 D0 verification (no seat totals in the inputs)
Before any outcome is read, the harness must verify that **no seat/capacity path is an input**: seats in year `t`
are produced only by the district/private decisions of §3; the run fails `D0-INPUT-SEATS` if any exogenous seat
series is read or if seats are computed from the same year's enrolment/cohort target (i.e., next-year NER used as
input). **This check is release-blocking.**

### 8.2 The four coexistence phenomena
In **one district (the town+its villages) and one cohort window** (declared: the 12 cohorts entering primary in
years 6–17), the baseline must show all four simultaneously in at least one district×cohort cell:
1. **Unused accessible ordinary places** — ordinary secondary places within declared reach that eligible children do
   not take: `unused_accessible_places_t ≥ 10%` of ordinary places offered that year in the district.
2. **Early leaving** — share of the cohort that entered secondary and left before completing it: `≥ 5%`.
3. **Oversubscribed selective places** — qualified applicants per selective place `≥ 1.20`, with turned-away
   qualified applicants `> 0`.
4. **Concentrated tutoring near the gate** — gate-tutoring hours per selective applicant `≥ 2×` catch-up hours per
   non-selective pupil, **and** gate-tutoring households `≥ 20%` of selective applicants.
**What has two peaks must be named** in the result: the report distinguishes **tutoring expenditure**, **applications
per selective place**, and **years completed** — these are different claims and are reported separately (the run may
show one, two or all three; the declaration is that they are not conflated).
**Falsifier (typed):** if **no** district×cohort cell satisfies all four, v0's mechanism set is **INSUFFICIENT**
(`COEXISTENCE-MISSING`) and is reported as a failure; **no rescuing by tuning** (see §12).

### 8.3 The three one-change counterfactuals
Relative to the baseline, three runs change **exactly one declared object** each, all else (seeds, parameters,
decisions) identical:
1. **TRAVEL-CUT:** declared travel cost per km `× 0.5` (all villages).
2. **ORDINARY-EXPANSION:** the district authority's declared class-opening rule is relaxed by one declared step
   (e.g., `K_class` −25%, declared) — it may open **more ordinary places**; **no selective places** change.
3. **SELECTIVE-EXPANSION:** declared selective places `K_sel × 1.5` (institutional constraint), **no ordinary
   places** added by this arm.
**The response test:** for each run, compute completion/attendance gains by **family type**
(rural/urban × poor/non-poor, 4 types) relative to the baseline. The three changes **must help different families
for intelligible reasons**: the run passes `DIFFERENT-FAMILIES` iff (i) the **argmax family type differs across at
least two of the three runs**, and (ii) in each run the argmax type's gain is **≥ 1.5×** the gain of at least one
other type. **Falsifier:** if all three runs have the same argmax type **or** the pairwise correlation of their
4-type gain vectors is **≥ 0.95**, the schools are **represented too crudely** (`SAME-RESPONSE`); reported as a
failure, not re-tuned.

### 8.4 Mandate/fee/graduate-supply arms (report card B comparisons)
Three further declared arms, each one change and reported as **sequence/distribution** comparisons, not pass/fail:
- **MANDATE-BEFORE-FUNDING:** required years raised by one step at year 8 **without** additional district budget.
- **FEES-ABOLISHED-TRAVEL-REMAINS:** all declared fees set to 0 at year 8; travel costs unchanged.
- **DEGREES-OUTRUN-JOBS:** graduate supply growth doubled from year 8; employer requirement and returns rules as §6(c).
Expected direction is **not** predeclared as a verdict; the report states what the sequence does in the model.

## 9. First paper-sized question — the spillback experiment

**Question:** when does **opening the next level change demand for the level below**? Declared experiment:
**SPILLBACK:** at year 8 a secondary provider (ordinary class) opens within the declared reach of **one treated
village** (randomly chosen by the declared seed, with paired control villages); everything else identical to the
baseline. Measure **primary persistence** (share of primary entrants completing primary) for **younger cohorts**
aged 3 years or less at the opening vs older cohorts, treated vs control villages. **Declared criterion:** a
spillback is **present** iff the treated-village younger-cohort primary persistence gain is **≥ 5 pp** relative to
control-cohort-adjusted baseline; **falsifier:** gain < 5 pp or negative → **no spillback detected in v0** (reported,
not tuned). This is a **model-mechanism result**, not evidence about any country.

## 10. Runs, seeds, determinism

- **Runs:** baseline; 3 one-change counterfactuals (§8.3); 3 report-card-B arms (§8.4); spillback (§9) — **8 runs**.
- **Seeds:** base seed **20261121**; each run uses the same paired seed set `{20261121, 20261122, 20261123}`
  (3 replications); results are reported as means with ranges; **no seed chosen after results**.
- **Determinism:** one numpy `PCG64` stream per run; floats written at `%.10g`; no wall-clock, hostname or PID in
  outputs; two clean runs of the same seed must be **byte-identical**.
- **Runtime:** the full 8-run × 3-seed suite must complete in **< 2 minutes** on the local machine.
- **Labels:** every output `SIMULATED`; `DERIVED` for report-card arithmetic; `DECLARED` for parameters;
  `HELD` for UIS metadata. **No OBSERVED label in v0** (no observed series is used).

## 11. Declared parameter table (provisional; frozen before build)

All values are **design values** (no fitting to a known outcome). The frozen table lives in
`PARAMETERS.csv`; the predeclaration hash covers this document and the parameter file is hashed in the manifest.
Key values: `N_v=8`; distances above; cohorts `1,200` (town 320); years `30` (cohorts entering 6–17 scored);
primary 6 / lower 4 / upper 2 / post-sec non-tert 1–2 / tertiary 4 years; `K_class=40`; `K_sel` declared (selective
places per cohort, e.g. 12% of the town cohort); `K_uni` declared (e.g. 35% of selective completers); declared fee
levels by level and village/town; travel cost per km per year; child wage rural/urban; `θ=0.5`; weights
`(w_K, w_E, w_C)=(0.25, 0.35, 0.40)` (declared, not fitted); gate thresholds: selective exam ≥ 60/100, university
exam ≥ 65/100; tutoring prices `p_c,p_g`; catch-up trigger (score < 45); gate band (margin ≤ 8 points); access
distance limits. **Every value is listed in `PARAMETERS.csv` with a provenance tag (`DECLARED`).**

## 12. Falsifiers and failure reporting (typed, no rescue)

| id | test | failure string | action |
|---|---|---|---|
| D0-INPUT-SEATS | §8.1 verification | `D0-INPUT-SEATS` | **release-blocking**; do not read outcomes |
| COEXISTENCE | §8.2 four phenomena in one cell | `COEXISTENCE-MISSING` | report failure; **no tuning** |
| DIFFERENT-FAMILIES | §8.3 argmax/correlation rule | `SAME-RESPONSE` | report failure; **no tuning** |
| SPILLBACK | §9 ≥ 5 pp | `NO-SPILLBACK` | report failure; no tuning |
| ENDOGENEITY | seats produced only by decisions | `ENDOGENEITY-FAIL` | report failure |
| DETERMINISM | two runs byte-identical | `NON-DETERMINISTIC` | report failure |
| NER-CEILING | NER ≤ 100 by construction | `NER-CEILING-FAIL` | report failure |
**No threshold, parameter or seed may be changed after any result is seen; a failure is reported as a failure.**

## 13. What v0 does NOT claim

- Not evidence about the Philippines, Cambodia, China, Hong Kong or any country (v0 has **no observed input**).
- Not a validation of the 2026-10-24 massabm/triad models, nor of the closed 2026-11-20 phase; v0 **reuses declared
  household logic and measurement conventions only**, without copying claims.
- No causal or direction claim from the simulator; the coexistence/counterfactual results are **model-internal**
  (`SIMULATED`) and are reported as such.
- Cross-country institutional documentation and UIS metadata verification are **HELD**; v0 does not do them.

## 14. Acceptance criteria for the v0 deliverable

1. `code/` contains one deterministic simulator; `D0-INPUT-SEATS` passes; full suite < 2 min.
2. `results/` contains pupil-level records, report card A tables, coexistence metrics, the 3+3 counterfactual
   comparisons, and the spillback table; all labelled `SIMULATED`.
3. `FINDINGS.md` reports the coexistence verdict, the different-families verdict, the spillback verdict, the
   report-card-B sequences, and **every failure honestly**.
4. `RUN_MANIFEST.json` + `SHA256SUMS.txt`; two runs byte-identical; predeclaration hash enforced by the code.

**FROZEN. Hash recorded in `PRE_DECLARATIONS.sha256`; the simulator must refuse to run if this file changes.**
