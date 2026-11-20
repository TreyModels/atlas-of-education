# COUNCIL-2 INTAKE — first cycle after rotation (2026-11-20 14:31 +08)

**Party:** `deepseek-council2` (fresh-context subagent, rotated from expert-council per `06_report/CONTEXT_ROTATION_PLAN.md`).
**Authority:** inherited from files, not from the previous window. **Scope:** `08_council/` only; no fits, no experiments,
no external actions. **Label:** AI-composite design/decision output, not evidence; every number is cited to a file on disk.

## 1. ACKs (intake closed)

- **A5b final scoring** (`model2/runs/a5b_final_scoring.txt`): **equivalence set to the observed record EMPTY**; all four
  testable rivals fail the observed ordering/spacing; pairwise equivalence only empty-sense {demographic_cohort,
  state_building}; design-only rivals listed, not tested. Phase **EQUIVALENT + PARTIAL**; no direction claim.
- **A3 / D55** (`model2/A3_D55_STATUS.md`): **E4 DATA BLOCKED** (no national-share proxy); **E3 DATA BLOCKED** (nurse-visa
  2005–06 unverified in POLICY_TIMELINE → not an R24 marker; A3b simulated only); **A3a FAIL** (tertiary GER β = −0.213,
  se 0.070, n=27 vs required +0.10…+1.50; secondary lead-placebo |t|=3.33) — reported as failure, national descriptive only.
- **Capacity reconciliation** (STATUS §3p): `data/STATE_CAPACITY.csv` canonical for the **three dimensions** (fiscal 611 /
  delivery 509 / enforcement 679); scout composite canonical only as **DERIVED** (1,182 country-years × 30, 1971–2024);
  **tax/GDP from scout WDI GC.TAX** with provenance, never spliced; **WGI GE.EST blocked in both** → renormalised **0.85**;
  **de jure ≠ de facto binding** (compulsory years vs 110,954 missing classrooms vs unmeasured inspection = three separate
  inputs, no collapse); **BEPER 2019 DATA BLOCKED**, no citations.
- **Series correction (binding):** “PTR 37→27→24” is the **PIDS high-school** ratio, **not** WDI primary PTR
  (~32–35 → ~29–30); never splice.
- **Anchor A1 report** (exp1 NEW 439e28eb; `model/anchor_out/`) — ACKed as delivered; reviewed in §2.

## 2. Anchor A1 review verdict — **PARTIAL / DESCRIPTIVE + EQUIVALENT** (no PASS, no direction claim)

Observed, re-derived from `data/UNIVERSALIZATION_SERIES.csv` (PHL, observed rows): **M0 left-censored** (lower-sec 58.86 at
1999 → bound ≤1999); **M1 left-censored** (primary NER 96.79 at first observed **1976**, GER≥100 **1977** → bound ≤1976/77;
the report text's ≤1999 is looser than the on-disk Y0); **M2 ≥90 in 2024** (92.41; band 2023 88.44 → 2024, narrow ±3 y =
2021–2027); **M3 never ≥90** (75.03); **M4 tertiary GER ≥50 first in 2025** (51.07; 2024 = 47.41; band 2024–25).

Model (12 arms, `anchor_table.csv`): **M0/M1 = 1960/1966** almost everywhere → bounds satisfied, **no timing credit**
(uninformative). **M2: no crossing in 9/12 arms**; inside the narrow band only education_led/capacity_gated (2025), late
demand_led/capacity_only (2028, outside ±3 / inside ±5), far out complementary/none (2038). **M3:** R6 **in-window** test
**passes** (no arm ≥90 by 2024) but **2/12 arms cross after the window** (education_led gated 2027; demand_led capacity_only
2031) → **ceiling-channel overshoot** under A10/R29, disclosed, not tuned. **M4: all 12 arms cross at 1960** → miss ≈65 y;
the crossing sits at the simulation start, so the implied simulated tertiary GER is ≥50 across 1960–2024 vs observed 16.34
(1971) / 47.41 (2024) — and **no tertiary-GER level check is reported** (GER is check-only, never fitted). ⇒ **The A6
asymmetry is NOT reproduced: 0/3 informative outcomes reproduced-and-credited.** Consistent with A5b (rival field empty).

Capacity vs law (D61/A9 §3): demand_led law 2.03/4.42 vs gated 1.85/4.51 — **identical crossings** (tie); complementary
2.17/4.57 vs 1.97/4.01 — identical (M0 1963 vs 1960 is a left-censored bound only) (tie); education_led 2.16/5.19 vs
2.05/5.26 — gated gains M2 2025 **but generates M3 2027**, a ceiling universalization the record does not show (not
creditable, R29). **capacity_only worse** (fit 2.47–3.29, hold 4.55–6.12). ⇒ **capacity-gated does not beat law-only on the
A6 crossings → capacity-timing hypothesis NOT supported → EQUIVALENT** (R28/D61). **A2d:** best ΔC ↔ enrolment-growth
r = **−0.427 at lag 6** — negative, and outside the predeclared 2–4 lag window (max-|r| selection) → **DESCRIPTIVE-NEGATIVE,
exploratory**; no positive support. **Scaling criterion: FAIL standing**, reproduced in every arm, not re-fit, not tuned.

## 3. Report-completeness conditions before the write-up (no verdict change)

C1 naive benchmarks (persistence, linear trend) for anchor fit 1999–2013 / holdout 2014–2024 are **absent** (§5/R18);
C2 **κ/weight sensitivity** table absent (A9 §2); C3 the A10/R29 floor-ceiling addendum is **post-run** → declare it, assert
no tuning, predeclare the residual decomposition next time (D63/R12); C4 **gate-form documentation mismatch** — findings
text says `sigmoid((C−0.5)/0.15)`, executed `model/anchor.py` uses **G(C)=C^0.75** (A9/D60 form) — correct the text; C5 the
enforcement sub-index is a **de jure** compulsory-duration mapping (6/10/13 y ÷ 13, weight 0.2), not observed → label de
jure proxy (§3p); C6 report the **M4/tertiary-GER level check** (check-only ±5 pp); C7 correct M1's censoring year to
1976/77. All are write-up items, not re-runs (R27/R12).

## 4. Next-cycle priorities

1. **A1 descriptive write-up (KEEP, critical path):** crossings + spacing, capacity floor-vs-ceiling, ceiling residual
   14.97 pp reported **UNABLE**, rivals, scaling FAIL — with C1–C7 closed; Council reviews the text before it leaves.
2. **A2d note (KEEP):** fold `model/A2D_CAPACITY_LEADS_INTAKE.md` into the A1 capacity section with the exploratory-lag
   caveat.
3. **A6/A7 portability (PARK, design-only):** fixed-behaviour / declared-inputs checklist may be drafted; **no run or claim**
   before the A1 report is final (R20/R22). KHM holdout-country check after the write-up (cannot change the A1 verdict).
4. **Data asks (HELD — nothing sent; user approval required):** PSA microdata; WB Enterprise Surveys credential module;
   real per-pupil spending; enforcement (inspection/sanctions); schools/classrooms/procurement; GC.* tax/revenue
   verification; BEPER 2019 public retrieval; HKG/CHN/JPN/KOR historical timing series.
5. **No new fitting (NO):** no scaling repair (R27); no arm re-specification to chase M2/M4.

## 5. PARK / KILL / KEEP

**KILL:** further scaling repair (R27); direction/complementarity claims from panel moments (R13); a capacity-mechanism
claim from this record (EQUIVALENT); reopening shadow education; post-hoc arm re-specification. **PARK:** A6 CHN + A7 HKG
portability; KHM check; E4; E3; E1; E5/E7; ECI; T1/T2; shadow paper. **KEEP:** A1 write-up; the A5 rival field as reported;
gate + rules; **the bounded negative result + equivalence/identification map** as the phase's publishable objects (D58).

## 6. Open questions (non-blocking)

Q1 Internal memo or report-layer section for the A1 descriptive report? (Nothing external without approval.) Q2 KHM
holdout-country check: run as a check-only cell after the write-up, or defer? (Council: after the write-up.) Q3 If data asks
are approved, Council priority = **real per-pupil spending + enforcement** (capacity from proxy to measured), then PSA
microdata for the design-only rivals.

## 7. Step-back (mandatory, 5 lines)

1. **Goal:** massification/universalization produced by schooling–government–market interaction, each standing the others up,
   with cohort flows and country/sector variation; shadow secondary. 2. **Threads:** labels in §5. 3. **This cycle's one
   thread:** the **A1 write-up** — the failure converted into the product. 4. **Drift check:** after A1 the temptation is
   another run (chase M2/M4) or a capacity story — both barred (R27/R29/D61); one red flag (two cycles of
   validation/reporting rather than model improvement), mitigated by **closing the phase with the negative result**; no
   closed claim reopened. 5. **If only one thing mattered:** the A1 write-up, not another run.

## 8. Decisions and bridge

`DECISIONS.md` **D66–D70** appended (intake ACK; A1 verdict; write-up conditions C1–C7; priorities + PARK/KILL; authority
persistence). `COUNCIL_STATE.md` rotation line appended; `BIG_PICTURE.md` cycle-8 step-back appended. Bridge: online
**abe34ae0**; intake + verdict **d9d52980**; count correction **43d0b699**.

---

# §9 SECOND PASS (verification + additions; decisions D71–D78)

**Process note (append-only):** two Council-2 processes ran concurrently against the same handoff. §1–§8 above are
kept unchanged as the first pass; this section **verifies** them against the files and **adds** what they missed. On
any conflict, **this section and D71–D78 bind**. Verified hashes this pass: `findings.txt` `927b7e900cbb4c88`,
`anchor_table.csv` `2a6d4e8ea76f49d7`, `A2D_CAPACITY_LEADS_INTAKE.md` `a139f6ff03f6f144`,
`PRE_PORTABILITY_A6_A7.md` `533730072d12e16d`. Cycle stamp 2026-11-20 14:33 (+08).

## 9.1 Verification of §2 numbers (re-derived from `data/UNIVERSALIZATION_SERIES.csv`, `status=observed`, iso3=PHL)

| item | §2 claim | verified on disk | note |
|---|---|---|---|
| M1 boundary | left-censored ≤1976/77 | **NER≥95 first observed 1976 (96.79)**; **GER≥100 first 1977 (100.59)** | report's "≤1999" is looser than the data; use **≤1977** (GER convention the model uses) |
| M2 | 2024 (92.41), band 2023 88.44 → ±3 | **2024 = 92.41; 2023 = 88.44** | band gap 1 y ⇒ narrow ±3 → **2021–2027** ✓ |
| M3 | never ≥90 | **2024 = 75.03**, peak **76.43 in 2017** | ✓ (also: the series falls to 68.28 by 2022 — the "never" is robust) |
| M4 | first ≥50 in 2025 (51.07); 2024 = 47.41 | **2024 = 47.41; 2025 = 51.07; 2026 = 52.99** | band **2024–25** ✓ |
| M0 | left-censored (58.86 in 1999) | **lower-sec completion 58.86 (1999)** | ✓ |

§2's verdict (PARTIAL/DESCRIPTIVE + EQUIVALENT), its crossing counts, and C1–C7 all **stand** after verification.

## 9.2 New findings (F1–F6) — none changes the verdict; all change how it must be written

- **F1 (material): the A6 signature's first milestone is missing from the tested vector.** Amdt-A6/D47 define the
  asymmetry with **primary completion ≥90 = 2017** (83.16 in 1999 → 85.56 by 2004 → 87.45 in 2013 → **91.92 in
  2017**). The official M-vector's M1 is **primary NER≥95/GER≥100** — left-censored by construction — so the one
  cleanly observed, informative *primary* crossing was **never tested**. The report's line "M2/M4 are the informative
  crossings" silently drops it. The corrected informative vector is: **{primary completion ≥90 2017 — NOT TESTED;
  M2 lower-sec 2024 — 0/12 clean, 1/12 R29-flagged; M3 never — 12/12 in-window pass, 2/12 post-window overshoot; M4
  2024–25 — not discriminable (F2)}**. The addendum must report the primary-2017 crossing from the existing
  simulated completion series; if it lands within ±5 y the report must say so (a crossing hit does not lift PARTIAL —
  the cap is the scaling FAIL — but suppressing it would be a reporting failure).
- **F2 (material): M4 is not "a timing miss of 64 y" — it is not discriminable in this run.** `anchor.py:102-107`
  returns the first year at/above threshold, so **M4 = 1960 in all 12 arms, including the no-push arm**, means the
  simulated tertiary GER is **already ≥50 at the first simulated year**, against **16.34 observed in 1971**. Two
  readings (initialisation artefact vs gross tertiary level error) cannot be separated without the simulated level
  path. Until then M4 is **untested**, not "wrong by 64 years" — the stronger, correct statement is that the
  simulated tertiary level sits **≥33 pp above the earliest observed level (16.34 in 1971), eleven years earlier**,
  **or** the crossing is an artefact.
- **F3: capacity is back-filled constant before the first observed year.** `anchor.py:34-43` `interp_flat` holds the
  first observed value (C = **0.2337** flat 1960–1986 in `run_meta.json`). So the 1960/1966 crossings rest on an
  **assumed** capacity path (R28: measured, not assumed) — undisclosed in the report; must be labelled.
- **F4: `law × G(C)` double-counts the law.** The enforcement component is `compulsory_years/13` with steps at
  **1987** and **2013** (`anchor.py:57-59`) — a **de jure** input inside the "capacity" gate, **collinear with the
  policy marker**. Any capacity claim would need this removed or declared first. No re-run ordered (R27).
- **F5: A5b's "empty" set has a narrower reading than §3 of the report.** world-society's predicted primary crossing
  (**2014**) is **within ±5 y of the A6 primary-2017 signature**. The equivalence set is empty because of
  **ordering/spacing and the upper-secondary non-crossing**, not because every rival misses every milestone. The
  sharpened headline (D77): the asymmetry is **unreproduced by every model on disk, including the anchor model**.
- **F6: A2d is a model-internal test.** §2 calls it "exploratory"; it is stronger and more precise as: **computed on
  simulated series**, best |r| selected over lags 0–6 (a max-|r| search, outside the predeclared 2–4 window), with
  only **three observed PHL capacity points** (2000/2014/2017) so an observed-data lag test is not computable. It is
  a diagnostic of the implementation, **not an empirical null about the Philippines** (D73).

## 9.3 Additions to the write-up conditions (C8–C10; amend D68, no re-run)

- **C8:** report the **A6 primary-completion-≥90 (2017)** crossing (F1), or state UNABLE with the reason it cannot be
  extracted from the existing outputs.
- **C9:** report the **simulated vs observed level path** at 1960/1971/1999/2013/2024 for tertiary (and each level),
  and classify M4 as **untested/artefact vs level error** (F2); include the tertiary GER check-only ±5 pp line (C6).
- **C10:** disclose the **constant back-fill** of capacity before the first observed year (F3) and the **de jure
  enforcement component inside G(C)** (F4); correct the `findings.txt` gate-form line (C4) in the same edit.

## 9.4 Portability — ruling (supersedes the soft "design-only" phrase where it differs)

**PARKED-ARMED. No run, no verdict this cycle.** R22 bars a portability *claim* (the anchor passed none of the
discriminating criteria). Design notes are accepted as intake only. A later run needs a new Council decision +
predecl and six constraints: (i) fixed PHL behaviour/parameters, only declared country inputs re-set (R20); (ii) no
re-fit, no extra free parameters, no target fitting — **any occurrence = FAIL** and the moved parameter named;
(iii) HKG **timing-only, levels check-only** (NER≥90 **1974**, NER≥95 **1979**, threshold-specific, never spliced);
(iv) CHN with censoring rules and the 1986-law **−27 y** miss reported as is; (v) the standing scaling **FAIL** printed
in every table; (vi) verdict vocabulary **DIAGNOSTIC-TRANSFER** (transfer-holds / transfer-fails / FAIL-re-fit),
**never PASS**, and the predecl must state **what it would change** given the anchor's own misses. **Naming:** slate
**A6 = CHN**, **A7 = HKG**; Amendment **A6 = asymmetry**, **A7 = timing alignment** — write "slate-A6/A7" or
"Amdt-A6/A7".

## 9.5 Phase headline (label rule)

**"Conditional *level* reproduction + observational equivalence + an unreproduced asymmetry."** "Conditional
reproduction" without **"level"** overstates (no informative crossing is cleanly reproduced); "reproduces
universalization" is barred (R14/R17); "capacity explains the timing" is barred (D61/R28); "portability holds" is
barred (R22); direction words are barred (R13). **Re-openers (only these):** **C1** a predeclared structural class
generates the A1/A3 exponent **signs OOS** with containment ≥2/3 and no exponent as a parameter (→
PASS-CONDITIONAL at best, never IDENTIFIED); **C2** fixed-behaviour crossings reproduce within ±5 y (±3 narrow) for
primary-completion-2017 / lower-sec-2024 / tertiary-2024–25 with no upper-sec ≥90 by 2024; **C3** a discriminating
test separates push/pull/queue/capacity (needs PSA returns and/or ES module — user approval); **C4** annual
classrooms, real per-pupil spending, or enforcement arrive **observed**, making capacity measured.

## 9.6 PHL cell closed

The PHL anchor cell is **CLOSED at PARTIAL/DESCRIPTIVE/EQUIVALENT** (D76). Remaining PHL-side work = the addendum
(C1–C10) and the write-up. **No** new fit, repair, arm re-specification, rival re-score, capacity re-index or level
re-fit without a new Council decision (R27). Data asks stay **HELD**; nothing sent.

## 9.7 Step-back addendum (labels only; the five lines in §7 stand)

Thread change: portability slate-A6/A7 moves from **PARK (design-only)** to **PARK (armed, diagnostic-only)**;
capacity re-measurement is **not** a KEEP (it was implicit) — **PARK** until observed annual series arrive (C4); the
A1 addendum absorbs C8–C10 and remains the **one thread**; drop-if-one-thing is unchanged (the A1 accounting + the
write-up). Drift flags still **two**; mitigation unchanged (close, don't add cells).
