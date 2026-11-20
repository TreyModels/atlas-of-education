# SYNTHETIC TARGETS — education, literacy, ECI and growth

**Scope.** Eight calibration targets for the v1 synthetic generator (`synthetic_2026-11-20/`), restricted to the
education/literacy/ECI/growth question. Companion to [`EXPECTATIONS.csv`](EXPECTATIONS.csv) and
[`PLAIN_ENGLISH.md`](PLAIN_ENGLISH.md). Written 2026-11-20 by the `longitudinal_2026-11-20` lit worker.

**The rule this file exists to enforce:** a number the generator *sets* proves nothing when it comes back out.
Only a number the generator must *produce from structure* can fail, and only a number it can fail is a test.
Every row below is tagged either **ENCODED-ASSUMPTION** (a parameter; never counts as validation, never to be
reported as a finding) or **TEST-TO-PASS** (a check on generated output; may fail, and failure must be printed).

## 0. Provenance vocabulary, and why nothing here is `STANDARD-CITATION`

Checked by grep against the repo-root `LITERATURE_LEDGER.md`: **0 hits** for `Hanushek`, `Woessmann`, `cognitive`,
`ECI`, `Hidalgo`, `Hausmann`, `Schofer`, `Becker`, `Mincer`, `growth`. That ledger catalogues the private-tutoring
literature (Yoo, Kim, Kang, Jayachandran, Bray, …) and carries **no education-and-growth source at all**. Its only
relevant rows are Thurow 1975 and Collins 1979, both marked *"Cited, unverified"*, and Clark & Nielsen 2024,
also not retrieved. The one growth-adjacent magnitude verified at source in this programme is the Mincer return
(Psacharopoulos & Patrinos 2018, FULL-TEXT) via `09_relations/LITERATURE_ELASTICITIES.md` §1.

Consequence: **EXPECTATIONS.csv contains no `STANDARD-CITATION` row** (19 rows: 8 PROGRAMME-PRIOR, 7 UNVERIFIED,
4 BLOCKED). The Hanushek–Woessmann claim is real and canonical, but this programme does not hold it; labelling it
`STANDARD-CITATION` would have implied a source on disk that does not exist. **Data ask:** add the knowledge-capital
line (and Hidalgo–Hausmann) to the ledger before any write-up attributes the horse race to the literature.

## 1. Targets

| id | target | value / range | provenance | how the generator encodes it | status |
|---|---|---|---|---|---|
| **T1** | Mincer wage premium per year of schooling | **8.8%/yr** (world, 1950–2014 compilations); EAP 8.7%; social EAP 6.9%. Use a 7–10% band | **Literature**, verified at source: Psacharopoulos & Patrinos 2018, WB PRWP 8402, via `09_relations/LITERATURE_ELASTICITIES.md` §1 (`FULL-TEXT`) | **Parameter** in the Layer-2 wage equation: `wage = rung wage × (1 + premium × completed level) × rank factor` | **ENCODED-ASSUMPTION** — no earnings microdata on disk, so there is no test (MIN-01, testable = no). A generator that "recovers" 8.8% has recovered its own parameter |
| **T2** | Takeoff regime switch: literacy pays ~0 pre-industrial, positive while industrialising, not binding once diversified | threshold **not recorded anywhere** — declared, never estimated | **Programme prior** (Dr. Menefee's verbal specification, recorded as design) `MODEL_ARCHITECTURE.md` Layer 0 / check D | **Parameter**: `T_c ∈ {pre-industrial, industrialising, diversified}` plus a literacy cut that permits the upgrade | **ENCODED-ASSUMPTION** — any "literacy causes growth" sentence the generator emits from this switch is circular. It is admissible only as a *conditional* prediction, tested by T3/T5 |
| **T3** | The 2015 horse race, in synthetic cross-section and country FE | literacy coefficient **> 0, CI excluding 0**; `MYS_proxy` **not significant, or standardized \|coef\| < 0.5 × literacy's** | **Programme prior** — frozen `PRE_DECLARATIONS.md` H1 (line 60). No effect size recorded in any ledger | **Check only.** Literacy must never enter the growth equation directly; it enters through informal/agri productivity and the takeoff switch, and the horse race must *emerge* | **TEST-TO-PASS** — falsifier: `MYS_proxy` positive and significant while literacy is not; or both null |
| **T4** | ECI → 10-year growth in the 30-country 1995–2024 panel | observed **−0.142 (se 0.105, n=893)**; pass band **[−0.35, +0.05]** (i.e. not significantly positive) | **On-disk estimate**, `DATA_PATTERNS.md` §9 test C7. The literature (Hidalgo–Hausmann) says *positive*; that claim is **not on disk** | **Check.** Rung demand grows with `X`, so a positive micro channel exists — but the aggregate ECI-growth premium must **not** come out positive | **TEST-TO-PASS**, with a **declared conflict**: encode the literature sign as a parameter and you fail this check; pass this check and you have not validated the literature. Do not do both and call either one validation |
| **T5** | Education → growth is null to negative | growth ~ tertiary GER(t−15) **−1.035 (se 0.240)**; ~ secondary GER(t−10) **+0.217 (se 1.289, ns)**; education→growth **F = 0.943 / 0.648 / 1.516** (all ns) | **On-disk estimate**: `DATA_PATTERNS.md` §1 S21/S22 and `STYLIZED_FACTS.csv` PP-03 | **Check** on generated panel, same specs. The Layer-3 composition term (moving a worker informal→formal adds a finite step; extra graduates add queue) is the mechanism that must produce it | **TEST-TO-PASS** — a generator whose education channel raises growth fails, and that failure is the informative output |
| **T6** | Complexity interaction with schooling, sign | completion × ECI **−0.039 (se 0.015, p=0.007)**; tertiary × ECI **−0.077 (se 0.020, p<0.001)** | **On-disk estimate**, `DATA_PATTERNS.md` §9 X5/X6. The frozen H3 expects the **opposite** (high-tercile slope ≥ 1.5× low) | **Check.** A generator that builds "more rungs at higher complexity" will likely produce the *positive* interaction and fail this; print the failure | **TEST-TO-PASS** — this is the sharpest available discriminator between the user's gating hypothesis (ABS-01) and the sample. Do not tune the rung structure until the sign flips |
| **T7** | Adult literacy is a demographic stock, not a flow | **62–66%** of observed adult-literacy gains is cohort replacement | **On-disk estimate**, `DATA_PATTERNS.md` §8 addendum (programme decomposition) | **Structure**: age-specific literacy by cohort + mortality + cohort entry. The replacement share must **emerge** | **TEST-TO-PASS** *if* literacy is built from cohorts. If literacy is instead a fitted smooth path, it becomes **ENCODED-ASSUMPTION** and validates nothing — the distinction must be stated in the generator's own output |
| **T8** | ECI tracks the schooling **flow**, not the literacy **stock** | completion(t−10) → ECI **0.593**; contemporaneous **0.197 (se 0.069)**; youth literacy **4.493 (se 1.531, p=0.003)**; adult stock association recorded as absent | **On-disk estimate**, `DATA_PATTERNS.md` §8 addendum and §9 C3/C10 | **Structure**: complexity as a slow product-space stock fed by completions. The near-null on the adult stock and the positive youth-literacy association must both emerge from the vintages | **TEST-TO-PASS** — note the tension: C10 says *youth* literacy co-moves with ECI while §8 says the *adult stock* does not. Both are on disk; the generator must reproduce the vintage gap, not pick one |

## 2. Assumptions that must never be reported as validation

1. The 8.8% Mincer premium (T1) — calibration-only, no test exists on disk.
2. The takeoff threshold and the `{pre-industrial, industrialising, diversified}` switch (T2) — this is where the
   "literacy bonus" the user remembers is *put into* the model.
3. Any country-specific return (PHL/KHM/CHN/KOR) — `LITERATURE_ELASTICITIES.md` §5: *"Must not be used at all
   without new data"*.
4. The rung-demand elasticity to complexity, if it is set so that T6 passes. Tuning a parameter until a check
   passes converts the check into an assumption; the tuning must be reported.

## 3. What would count as success, and what would not

**Would count:** all of T3–T8 evaluated once on frozen parameters, printed with passes *and* failures side by side,
with the two failures in §1 (T4/T6 conflict with the literature and with the user's hypothesis) left visible.

**Would not count:** a run in which the generator reproduces its own parameters; a horse race produced by putting
literacy in the growth equation; an ECI-to-growth premium produced by a fitted ECI coefficient; any claim that the
synthetic world "confirms" absorptive capacity when T6's sign is imposed rather than generated; and any causal or
direction reading of T3–T5 (barred by ID-01 / R13 — forced-ID 1.00, equivalence 0.07).

**One line.** Six of these eight targets can fail. The two that cannot (T1, T2) are the two the programme most
wants to believe, which is exactly why they are labelled as assumptions rather than results.
