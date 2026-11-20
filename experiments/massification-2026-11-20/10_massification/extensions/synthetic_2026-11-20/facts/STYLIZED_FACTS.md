# STYLIZED FACTS REGISTER — massification programme, synthetic-data build

**Built:** 2026-11-20 · **Worker:** stylized-facts register (synthetic-data build) · **Base:** `experiments/massification-2026-11-20`
**Write scope:** `10_massification/extensions/synthetic_2026-11-20/facts/` only. No other file was modified.
**Companions:** [`STYLIZED_FACTS.csv`](STYLIZED_FACTS.csv) (machine-readable, one row per fact), [`build_facts_csv.py`](build_facts_csv.py)
(the deterministic builder — rerunning rewrites a byte-identical CSV), [`MUST_REPRODUCE.md`](MUST_REPRODUCE.md),
[`PLAIN_ENGLISH.md`](PLAIN_ENGLISH.md).

**Purpose.** A synthetic-data generator may only reproduce regularities the programme has actually established, and must
not launder the ones it has not. This register is the honest, provenance-labelled list: what is a fact, what is a fact
*about the data* rather than about the world, what is disputed, and what is a model output that happens to have been
quoted as a fact.

**What this worker did.** Read the closeout, `STATUS.md` §3t–§3u, the three new audits (`a_regressions`,
`b_models`, `c_toys`), `SYNTHESIS_017`, `SYNTHESIS_018`, the four data files the task names, the relation data tables
(`scaling_laws`, `capacity_crosscountry`, `capacity_alignment`, `state_capacity`, `push_pull_tests`), the two model
scaling artefacts (`scaling_check`, `repair_scaling`), the smoke file, the recovery/equivalence files, and all three
lab batteries' `RESULTS.csv`. **Re-checked from disk (no regression run):** all PHL milestone series in two independent
files, the 17-region equalization statistics including both Spearman coefficients and the quartile ratio, the
capacity-alignment recomputation, the PHL capacity/PTR/spending row values, the scaling-law coefficients against the
model2 targets, and the generated-exponent signs. Descriptive panel computations (Y2 partial correlations, Y1 rank
partials) were **read from `RESULTS.csv`, not re-run** — they are regressions, and the brief forbids running them.

---

## 0. Evidence labels and counts

| label | meaning | n |
|---|---|---|
| **VERIFIED-FROM-DISK** | this worker re-read or recomputed the value(s) from the cited file; the file is observed/derived data, not a model run | **35** |
| **REPORT-ONLY-UNRELIABLE** | the value is quoted in narrative but is absent from disk, or contradicted by the file it claims to come from | **3** |
| **DISPUTED** | two on-disk objects disagree, or one object is internally contradictory; no single target exists | **5** |
| **MODEL-OUTPUT-NOT-FACT** | produced by a model or identification run; a property of the instrument, not of the world | **4** |
| **SIMULATED** | stipulated toy; design constraint only, evidential weight zero (D79/D88) | **6** |
| **total** | | **53** |

Confidence: **51 high / 2 medium / 0 low**. The two medium rows are INC-03 (the CHN/KHM attribution is the battery's
report, not re-derived here) and TOY-06 (a corner-solution toy, so only its direction travels).

Read the counts honestly: **35 of 53 rows are facts we can check from disk, and only 19 of those 35 are about the world
in a way a theory could have gotten wrong** (PHL-01…06, REG-01…05, SCA-01…05, INC-01…03). The rest of the verified rows
are negative results, capacity facts, and data-limitation facts — which are just as binding on a generator but are
statements about what the evidence can and cannot show.

---

## 1. The anchor fact — the PHL milestone signature

**This is the one fact the whole programme stands on, and it verifies twice from two independent files.**

| fact | value | check |
|---|---|---|
| **PHL-01** primary completion | 83.16 (1999) → 87.45 (2013) → **91.918 (2017)** → 95.40 (2021) → 98.305 (2024) | first year ≥90 is 2017 (2013 = 87.45) |
| **PHL-02** lower-secondary completion | 58.86 (1999) → 71.27 (2013) → 81.255 (2017) → 88.442 (2023) → **92.414 (2024)** | first year ≥90 is 2024 |
| **PHL-03** upper-secondary completion | 76.433 (2017, series max) → 75.025 (2024) | **never ≥90**; 14.975 pp short |
| **PHL-04** tertiary GER | **16.336 (1971)** → 38.345 (2016) → 28.117 (2018) → 47.414 (2024) → **51.072 (2025)** → 52.990 (2026) | 25 pp rise 2018–2026 after a 10 pp dip |
| **PHL-05** primary GER | 99.54 (1971) → 106.47 (1990) → 99.37 (2017) → 88.83 (2021) → 94.03 (2024); primary NER 96.79 (1976) | participation was ≥95 for 46 years *before* the "universal primary" date |

Sources: `10_massification/data/UNIVERSALIZATION_SERIES.csv` (all rows `status=observed`) and
`data/gmr_observed_6countries_1970_2024.csv` (indicators `CR.1`, `CR.2`, `CR.3`, `GER.5T8`, `NER.1.cp`) — the two files
agree to the last decimal. The A6/D77 signature in `MASSIFICATION_CLOSEOUT.md` §2 and `SYNTHESIS_018` §A.1 is therefore
**confirmed from source, not merely quoted**.

**PHL-06 is the structural content of the anchor, and it is not just "three numbers".** The floor (primary) and the
middle (lower secondary) both cross 90 within seven years of each other; the ceiling (upper secondary) does not move at
all, in either direction, over 25 years of observation. A generator that reproduces 91.92 / 92.41 / 75.03 as three
independent levels has *not* reproduced the fact. The fact is the **asymmetry**: the same system, the same government,
the same period, and a ceiling that does not respond to whatever lifted the two levels below it.

**PHL-05 is the fact that keeps the anchor honest.** "Primary universalisation in 2017" is a statement about *cohort
completion*. On the participation measure (GER) the Philippines was above the 95 line from 1971 to 2017 and fell below it
only after K-12 changed the cohort structure. Any narrative that reads a 1987 participation law against a 2017 completion
crossing is comparing two different objects (audit FLAG-05). The observed signature survives; the story attached to it
does not.

---

## 2. PHL regional equalization — the cleanest result in the programme, with one hard limitation

All five numbers below were **recomputed by this worker** from `10_massification/data/BASELINE_SERIES.csv` (17 regions ×
2 cohorts × 2 sex rows per indicator, sex rows averaged as the battery declares) and match the battery
(`lab_2026-11-20_b/RESULTS.csv` X10–X12) and the Council's independent re-derivation (`SYNTHESIS_017` §B, all MATCH).

| fact | value | what it means |
|---|---|---|
| **REG-01** | ΔMYS > 0 in **17/17** regions; +0.505 y (NCR) to +2.095 y (CAR) | every region gained schooling |
| **REG-02** | ΔGini ≤ −0.02 in **17/17**; −0.030 (NCR) to −0.095 (ARMM) | education inequality fell everywhere |
| **REG-03** | **ρ(ΔMYS, MYS₀) = −0.443627** | the laggards caught up |
| **REG-04** | **ρ(ΔGini, Gini₀) = −0.621524** | the most unequal regions equalized fastest |
| **REG-05** | Q1/Q4 median ΔMYS ratio = **1.098** (1.340 vs 1.220; cut-offs 9.16/9.39/9.82) | a *mild* pro-poor gradient, not a strong one |

**REG-06 is the binding limitation and a generator must inherit it.** `BASELINE_SERIES.csv` contains exactly four
region-level indicators (`education_gini`, `mean_years_of_schooling`, PTR, teachers hired) — **there is no regional
tertiary enrolment series anywhere on disk.** So REG-01…05 are facts about *attainment and inequality across cohorts*,
not about regional post-secondary participation. X10–X12 disclose this in their own `note` columns; `SYNTHESIS_017` §B
cluster-4 calls them "attainment/inequality proxies". A synthetic world may *generate* regional tertiary participation;
it must label it GENERATED and must not calibrate it to anything, because nothing observed exists to calibrate to.

---

## 3. Income scaling — two targets on disk, and the gate picked the one its own range rejects

### 3.1 The five scaling regularities that verify (SCA-01…05)

All from `10_massification/relations/data/scaling_laws.csv` (two-way FE "within" / year-FE "between", CR1 clustered,
30 countries, n≈1,000):

| law | within | between | note |
|---|---|---|---|
| secondary GER ~ GDPpc | **0.0904** (0.1238, ns) | **0.2154** (0.0349) | **between > within** |
| tertiary GER ~ GDPpc | **0.8482** (0.1719) | **0.5666** (0.0817) | **within > between** |
| lower-sec completion ~ GDPpc | **0.2468** (0.1188) | **0.1690** (0.0343) | marginal within |
| agricultural share ~ GDPpc | −0.1201 (0.0834, ns) | **−0.9901** (0.2162) | large negative gap |
| industrial share ~ GDPpc | **+0.5283** (0.1508) | +0.1426 (0.0555) | opposite-sign gap |
| fertility → primary completion (semi-log) | **−0.1893** (0.0436) | −0.1222 (0.0267) | the one graded-causal relation |

**The within-vs-between gap does not have one sign.** Secondary and agriculture have |between| > |within|; tertiary and
industry have |within| > |between|. A generator that imposes a single "within-country is steeper" (or flatter) rule will
fail on half the laws. SCA-04 is the notice that the **gap** — not the level — is the discriminating object
(`GAPS_AND_LEADS` (b) item 2, item 5; n=1,017).

### 3.2 The target chain is disputed (SCA-06, DISPUTED)

Two mutually inconsistent "targets" are on disk for the same panel and the same pair of laws:

- `10_massification/model2/runs/scaling_estimates.csv` — between estimator: secondary **+0.285844** (0.045163, n=30),
  tertiary **+0.776087** (0.086416, n=30). These are the A1 gate's targets.
- `10_massification/relations/data/scaling_laws.csv` — year-FE: secondary **0.2154**, tertiary **0.5666**. This pair
  defines the A3 containment range.
- `10_massification/model/calib/repair_scaling.csv` writes the contradiction in one row:
  `secondary, generated=-2.73, A3_lo=0.0904, A3_hi=0.2154, contained=False, **A1_value=0.286**`.

So a model that generated *exactly* A1's secondary target would fail A3 containment (audit **D-13**). The A1 target is
also one of the two estimators that define the comparison (**D-14**), so it is not the independent check it is described
as. **A generator must pick one pair and declare it.** The one thing that is *not* disputed is the sign: see SCA-07.

### 3.3 The bounded negative that survives the dispute (SCA-07, MODEL-OUTPUT-NOT-FACT)

`10_massification/model/calib/scaling_check.csv` and `repair_scaling.csv` both show the old cohort-flow class generating
**wrong-signed** out-of-sample income exponents: secondary −1.893 / −0.379 / −0.743 and tertiary −1.229 / −0.137 /
−0.353 (unrepaired), secondary −2.734 / −2.527 / −1.034 and tertiary −0.319 / −1.317 / −0.391 (repair cell). Signs
correct 1/3, contained 0/3. The sign failure is robust to which target is used because **every** generated value is
negative against a required positive. Caveat: the unrepaired file has **no generator script in the tree** (audit D-11),
so those numbers are quoted, not reproduced; the repair file does have a pipeline (D-12: its completion-law comparison is
a logit-vs-log-log unit mismatch, so only the secondary/tertiary rows are interpretable).

---

## 4. The six-system income gradient — a fact about the data, not a law

| fact | value | label |
|---|---|---|
| **INC-01** | within slope of upper-secondary GER on log GDP = **+56.066** (se 19.558, CI 17.73–94.40, n=93, **5 clusters**); between slope +159.857 (n=5) | VERIFIED |
| **INC-02** | the same gradient on 30 countries = **+14.7397** (se 8.3156, **CI −1.5588…+31.0382**, n=14) | VERIFIED |
| **INC-03** | the gradient shrinks ~74% and loses significance out of sample | VERIFIED, confidence medium |

`lab_2026-11-20/results/E1_income_gradient.csv` and `E10_replication.csv`. The programme's own replication cell (E10)
falsifies E1: +56.07 is a six-country, five-cluster description, and +14.74 with a CI spanning zero is what happens when
you ask 30 countries. The battery's own attribution ("driven by CHN and KHM") is quoted from its FINDINGS and the audit
(FLAG-08) and was **not re-derived here** — hence medium confidence on INC-03 only.

**What a generator must do with this:** target the *shape* (a steep income-elasticity segment in a pair of fast-growing
systems, ~+14 overall with a wide CI), not the number +56. And never label +56 a scaling law: the programme spent a whole
repair cell failing to generate it, and the failure is the more informative object.

---

## 5. Timing and censoring — dates are intervals, and the vector is measure-dependent

**TIM-01 / TIM-02 — censoring is the estimand, not a nuisance.** From `10_massification/relations/data/UNIVERSALIZATION_TIMING.csv`:
JPN primary ≥95 is `censored_above_at_first_obs` at 1971 (its reconstructed NER interval 1975–76 is flagged
`reconstructed=True`); KOR primary NER ≥95 censored at 1971, KOR lower-secondary completion ≥90 censored at 2003, KOR
upper-secondary completion ≥90 censored at 2000 while its NER crosses at 2009.5 (a measure disagreement *inside one
level*); HKG primary NER ≥90 at 1974 (band 1973–74) and ≥95 at 1979 (band 1978–79); HKG upper-secondary NER ≥90 never.

**TIM-03 — the PHL vector on the completion measure:** primary 2017–2021 (band midpoint 2019), lower-secondary
2023–2024 (2023.5), tertiary GER 2024–2025 (2024.5), upper-secondary not crossed. Note these are **bands**: "2017" is
the band start, and the capacity claim in CAP-02 silently used the 2019 midpoint.

**TIM-04 / TIM-05 — two files, two vectors, and no corrected one (DISPUTED).** Two identically-named files disagree
because they use different measures *and* different crossing definitions —

| milestone | `relations/data/…` (A01, 63 rows, completion/NER, first-sustained) | `data/…` (C03, 128 rows, GER/NER, first-above) |
|---|---|---|
| PHL primary ≥95 | 2017–2021 (completion) | 1971 (GER, left-censored) / 1976 (NER) |
| PHL lower-secondary ≥90 | 2023–2024 (completion) | 2014 (GER, band 2009–2014) |
| CHN lower-secondary ≥90 | 2014–2016 (completion) | 2006 (GER) |
| PHL tertiary ≥50 | 2024–2025 | 2025 (agree) |

Both are internally valid; nothing on disk disambiguates them at the point of use (audit **FLAG-05**). `SYNTHESIS_018`
Z2 ordered a corrected single-measure vector as the C2 prerequisite; **it has not landed**, so no single agreed vector
exists (TIM-05). A generator must pick one measure per milestone and declare it — the predeclared mapping is M1 NER/GER,
M2/M3 completion, M4 GER.

---

## 6. Three numbers that are NOT facts

This is the part of the register that matters most for a synthetic build, because these three are the ones most likely
to be copied forward.

### 6.1 "Capacity does not predict crossing timing (Spearman +0.15/+0.10/+0.41/+0.30, all ns, n=5)" — **CAP-01, REPORT-ONLY-UNRELIABLE**

**Those four numbers appear in no file on disk.** `10_massification/relations/data/capacity_crosscountry.csv` holds:

| level | n | rho | p |
|---|---|---|---|
| primary universal | 5 | **+0.872** | 0.054 |
| lower-secondary universal | 5 | **+0.900** | **0.037** |
| upper-secondary mass | 5 | +0.103 | 0.870 |
| tertiary mass | 5 | +0.800 | 0.104 |

The file's own `reading` column says *"higher capacity associates with LATER crossing"* — the **opposite** of the
narrative. And neither reading is usable: the association is a **one-country artefact**, because Japan enters at
`capacity_within` **20.0** against 46.5–61.1 for the other four (its within-normalisation is distorted by a 0.30 coverage
collapse). The audit recomputed all four values from `state_capacity.csv` + the timing file and got identical numbers, so
the *file* is internally consistent and the *narrative* is not. **Verdict: unsupported either way; the honest target is
"not identifiable at n=5".** `SYNTHESIS_018` withdrew the narrative and ordered re-derivation (Z2, not run).

### 6.2 PHL "+35.2 points into the primary crossing" — **CAP-02, REPORT-ONLY-UNRELIABLE**

`10_massification/relations/data/capacity_alignment.csv` does contain the row: PHL primary,
`crossing_year_used=2019`, `capacity_5y_before=49.5`, `capacity_at_crossing=84.7`, `capacity_change_pre=+35.2`.
**But it does not reproduce from the index it claims to summarise.** Recomputed by this worker from
`state_capacity.csv` (`capacity_within`):

- 5-year pre-window mean (2014–18) **57.214** → 2019 value **83.36** = **+26.15** (not +35.2)
- at the A4/A01 crossing year 2017: pre-window mean (2012–16) **42.946** → 2017 value **57.38** = **+14.43**
- `capacity_within` in **2017 (57.38) is below its 2005 value (58.89)** — so "capacity rose into the crossing" is true
  only if the crossing is dated 2019–21 rather than 2017
- `weight_coverage` falls 1.00 (2005) → 0.90 (2017) → 0.60 (2019–23): the 2019 index is differently composed

The auditor's recomputation (+26.1 at 2019, +14.4 at 2017, +3.7/+14.1 on the panel-comparable index) is confirmed
independently here. **Verdict: the +35.2 does not reproduce on any reading; the claim weakens substantially and is
crossing-year dependent.** Audit **FLAG-03**.

### 6.3 "The" crossing vector — **TIM-04 / TIM-05, DISPUTED**

There is no single-measure crossing vector on disk (two competing files, §5). Any generator that takes "the" vector as
its target is taking a 50/50 guess about measure and definition. Audit **FLAG-05**; re-derivation ordered (Z2), not run.

**What does survive in the capacity layer** is descriptive and checkable (CAP-03): PHL primary PTR **35.074 (2005) →
29.084 (2017)**, education spending **2.328 → 3.964 %GDP**, and upper-secondary completion **76.433 → 75.025** across the
same years — a genuine counterexample to a *pure* capacity driver (capacity improved; the ceiling did not move). And at
n=6 the floor-vs-ceiling separation cannot be tested at all (CAP-04: floor ρ +0.50 with n=5, ceiling ρ +0.60 with n=6,
leave-one-out 0.0–0.8 / 0.3–0.9, both conditions hold only when JPN is dropped).

---

## 7. Push–pull: the labels are reversed, and no direction claim follows

**PP-06 (DISPUTED) — audit FLAG-00, the most serious labelling defect in the regression layer.**
`10_massification/relations/data/push_pull_tests.csv` estimates `y_t ~ own lags + driver lags`, so the coefficient block
runs **driver → dependent**. The `hypothesis` text on **every one of the 13 rows** says the opposite. `SCALING_NOTES.md`
§3, `MASSIFICATION_CLOSEOUT.md` §2/§3 and (consequently) the phase narrative quote the labels. Corrected by reading the
`dependent`/`driver` columns directly:

| corrected reading | F | p | sum |
|---|---|---|---|
| **GDP-pc growth → tertiary GER** (row P5) | **6.522** | **<0.001** | **+0.2051** |
| **GDP-pc growth → secondary completion** (P6) | 3.514 | 0.0035 | **−0.6674** |
| **wage-share growth → secondary GER** (P9) | 4.108 | 0.0010 | +0.0504 |
| secondary GER → wage share (P10) | 1.881 | 0.094 | +0.1059 |
| secondary GER → GDP growth (P1) | 0.943 | 0.452 | −0.0752 |
| tertiary GER → GDP growth (P2) | 0.648 | 0.663 | −0.0004 |
| secondary completion → GDP growth (P3) | 1.516 | 0.181 | −0.0349 |

So the file actually says: **income growth → tertiary enrolment, strongly and positively (F=6.52)**; **income growth →
completion, negatively (−0.67)**; **wage share → secondary enrolment (F=4.11) while the reverse is marginal**; and
**education → growth is null in all three tests**. That one-way pattern — significant one way, null the other — is a far
sharper generator target than either number alone (`GAPS_AND_LEADS` (b) item 1: a model producing a symmetric lead-lag
is falsified, and so is one producing neither).

**PP-05 (MODEL-OUTPUT-NOT-FACT) — no direction claim follows, and this is a fact about the identification machinery.**
The recovery test recovers pure-demand and pure-supply worlds (1.00 each) but never the complementary world, and an
outside truth is forced (forced-ID 1.00, equivalence 0.07 — quoted from `MODEL_INVENTORY` §3.7;
`model2/runs/recovery.csv` re-read here confirms the pattern: truths D and S recovered 5/5, truth C never, truth OUT
misclassified in 3/5). **R13 bars any push/pull/complementarity claim from these moments.** A generator may *embed* a
direction as a stipulation; it may not claim the data license it, and it should reproduce the one-way significance
pattern above rather than a symmetric one.

---

## 8. Negative results that are facts about the data

These are as binding as the positive facts: a generator that produces a strong version of any of them is falsified.

| fact | number | label |
|---|---|---|
| **NEG-01** no detectable schooling↔market lead-lag | max \|partial r\| = **0.208** (lag 1, n=700, 30 cty); **0/24** cells reach 0.25; zero-order 0.49–0.71 is shared trend | VERIFIED (read from `RESULTS.csv`, not re-run) |
| **NEG-02** absorption proxies do not replicate | X1 −0.858 (CI −3.915…2.198, 6 cty) vs X2 +0.797 (CI −0.402…1.996, 30 cty) — **opposite signs**, both CIs include 0 | VERIFIED |
| **NEG-03** the surviving absorption cell is mechanical | X3 QUEUE on TER +0.366 (0.198…0.534) = (lagged BA+ stock) ÷ (wage share) | REPORT-ONLY-UNRELIABLE (relabelled derived/mechanical, `SYNTHESIS_017` condition 2) |
| **NEG-04** system size null | X7 SIZE −1.739 (CI −5.377…1.900); X8 one usable duration pair 0.667 (HKG *slower*) | VERIFIED |
| **NEG-05** crossings are structurally heterogeneous | E2 max 0.60 inside the GDP IQR (<4/6 rule); X4 3/5,3/5,3/5 and 2/6,2/6,2/6; X5 DATA LIMITED; X6 UNABLE (n=3) | VERIFIED |
| **NEG-06** the world-society null manufactures false crossings | 4 false upper-secondary crossings (of which CHN, PHL are evidence-backed); null year **2011.5 from one dated crossing**; 7 false cells across four levels | VERIFIED |
| **NEG-07** the ceiling residual is unexplained | 90 − 75.025 = **14.975 pp**; Y1 opportunity-cost account **discarded** (ρ_partial −0.105 agri / +0.246 youth-unemp vs a −0.40 bar, n=30) | VERIFIED |
| **NEG-08** "no common shape" is not established | A06 F 4.210/60.941 (reject) vs A07 p 1.000/0.125 (not) vs A08 F_all 0.236/0.303 (not robust) | DISPUTED |

Two of these need their caveat attached in the generator's documentation:

- **NEG-01** is the single most useful specification test in the programme (`GAPS_AND_LEADS` (b) item 5): the *visible*
  schooling–market co-movement (zero-order 0.49–0.71) is shared trend; only the partial structure is null. A generator
  must produce the co-movement **and** the null, not one of them.
- **NEG-06** is thin: the whole upper-secondary conclusion rests on **one** dated crossing (HKG 2011.5), and the two
  numbers originally cited for it (CHN **79.39**, PHL **66.05**) are upper-secondary **GER** finals, not the completion
  series the ≥90 threshold is defined on — on completion they are **87.52** (2020) and **75.03** (2024). The conclusion
  survives; the cited series was wrong (audit **FLAG-11**).

---

## 9. Toy design constraints — SIMULATED, never evidence

Six constraints are worth carrying into a generator's *design*, and none of their magnitudes are. All are
`SIMULATED` (stipulated parameters, not calibrated, no historical test; D79/D88/D92).

| fact | stipulated number | the design constraint that travels |
|---|---|---|
| **TOY-01** net of private exit | gross +20 → net +9.73, **R = 0.486** (F=$12 → 0.665) | supply is **net**, not gross; model provider exits |
| **TOY-02** fixed cost ≠ hysteresis | A_high 1.0338 vs A_low 1.0254, diff **0.0083** vs a 0.25 bar; falsifier fired | do **not** parameterise hysteresis; need separate entry/exit elasticities + a lag |
| **TOY-03** gate-determined saturation | floor **+44.43 pp**, ceiling **+4.58 pp**, ceiling max +11.67, secondary conversion **70.2%** (>50% cap → T7c FAIL) | saturation is set by the **eligible pool/gate**, not by seats at that level |
| **TOY-04** register ≠ classroom | paper law: register **+9.91 pp** vs attendance **+1.09 pp** (≈**9.1×**); enforced e=1: attendance +18.63 | two compliance states and a de facto enforcement parameter; never use enrolment-on-the-books as the outcome |
| **TOY-05** pipeline spacing | S = **11–13 y** in every non-control arm; paired S(primary_first) − S(simultaneous) = **0.0**; control 21 | spacing comes from the credential pipeline, not from the size of the push |
| **TOY-06** participation margin | total completers **+24.68** vs field-specific **+90.07** (ratio 0.30) | a demand shock carries a participation margin as well as a switching margin |

**What a generator must not do with these:** cite 0.486, 9.1×, 70.2% or 11–13 y as observed facts. `SYNTHESIS_017`
condition 1 and `SYNTHESIS_018` §A ("battery-B numbers banned from evidence columns") forbid it; `TOY_INVENTORY` §3 notes
8 of 15 toys carry a *structural* non-citability (built-in null, unfirable falsifier, arithmetic identity, degenerate
cell). The design constraint is the durable output; the number is not.

---

## 10. Model outputs that must not be inherited (MOD-01, MOD-02)

Two rows exist so a generator does not copy a defect:

- **MOD-01 — GER was 3–35× too large.** `10_massification/model/smoke/structure_smoke.csv`, 1,458 rows: `ger_lower`
  332.8–1477.0%, `ger_upper` 837.3–3514.4%, `ger_tertiary` 583.4–3247.9%, **1458/1458 rows >100% at each level**
  (`ger_primary` 64.3–206.6%, 98/1458 >100). Cause: cycle lengths multiplied into the progression chain (D-02), with an
  accounting check that reported zero failures anyway (D-16). The generator's inverse requirement is
  **GER ∈ [0, ~105] at every level and year with no per-country scale factor** — exactly the Z1 validity gate.
- **MOD-02 — the milestone table is not reproducible.** M4 (tertiary ≥50) "crossed in **1960**" in all 12 arms *including
  the no-push arm* — an initialisation artefact of MOD-01, not a finding. M2 (lower-secondary ≥90, observed 2024): **0/12
  clean hits**; M3: in-window 12/12 but 2/12 post-window overshoots (2027, 2031). No fitted θ was ever persisted (D-03),
  so the table cannot be re-scored without a re-fit barred by R27/R12. `SYNTHESIS_018` lists it as KILL / non-citable.

---

## 11. What a generator should take from this register

1. **One anchor, reproduced as an asymmetry, not as three numbers** (PHL-06): floor crosses, middle crosses seven years
   later, ceiling does not move; ~15 pp residual left explicitly unexplained.
2. **Participation and completion are different objects** (PHL-05): reproduce both, and never let one stand in for the
   other.
3. **Within- and between-country income elasticities differ, with no common sign for the gap** (SCA-01…04), and the
   sector gap is the discriminating object.
4. **A steep six-system gradient must collapse at 30 countries** (INC-01…03).
5. **Crossings are intervals, censored, and measure-dependent** (TIM-01…05).
6. **One-way lead-lag: income → tertiary strong, education → growth null** (PP-01…04), with no direction claim (PP-05).
7. **The visible co-movement, the null partials, the null size effect, the null absorption replication, and the
   heterogeneous crossings** (NEG-01…05) are all part of the target.
8. **Regional equalization across 17 regions with a mild pro-poor gradient** (REG-01…05), with the tertiary-participation
   limitation declared (REG-06).
9. **Six design constraints, zero magnitudes** from the toys (§9).
10. **Do not inherit the 3–35× GER scale, the 1960 milestone artefact, or any of the three non-facts (§6).**

See [`MUST_REPRODUCE.md`](MUST_REPRODUCE.md) for the ranked short list with exact numeric checks, and
[`PLAIN_ENGLISH.md`](PLAIN_ENGLISH.md) for the one-page non-statistician version.

---

## 12. Measurement note added 2026-11-20 — completion can exceed GER because the denominators differ

**Why this is in the register.** A synthetic generator that builds completion from a cohort-flow identity cannot
produce completion above the entering gross enrolment ratio. The observed Philippine series does produce it, at every
level in 2024. That is not a data error; it is a **measurement-definition fact** that every completion/GER comparison
in the programme must respect.

**Verified from disk** (`10_massification/data/UNIVERSALIZATION_SERIES.csv`, `data/gmr_observed_6countries_1970_2024.csv`; 2024, PHL):

| level | completion rate | gross enrolment ratio | ratio |
|---|---|---|---|
| primary | **98.30** | **94.03** | 1.045 |
| lower secondary | **92.41** | 85.29 *(secondary GER, combined lower+upper)* | 1.08 |
| upper secondary | **75.03** | — *(upper-secondary GER not in the on-disk extract)* | — |

**The coherent explanation:** the UIS completion rate is measured on children **3–5 years above the official grade
age**, whereas GER is enrolment in the age band for that level. They are different denominators, so completion can
exceed GER. The alternative — that the cohort-flow identity is wrong — would imply the observed series are
inconsistent; nothing on disk supports that.

**Consequences for the programme.**
1. **"Universalisation" is measure-dependent.** GER-based and completion-based crossing dates are not interchangeable:
   a GER-based reading can put primary universalisation decades earlier than a completion-based one. `MUST_REPRODUCE.md`
   R2 already flags this ambiguity; the numbers above quantify it.
2. A synthetic cohort-flow model must either (a) declare the completion denominator and accept that it reports later
   crossing dates than the observed completion series, or (b) add an explicit declared measurement-factor for the
   age-above-grade convention — never silently "fit" completion up to the observed level (that is target encoding).
3. Any completion/GER ratio comparison elsewhere in the programme must state which series/denominator it uses.
4. This also explains part of the old model's over-scale GER artefact (GER 64–207 %, `100_massification` audit D-02):
   GER and completion were being treated as the same object.

**Evidence label:** VERIFIED-FROM-DISK for the 2024 PHL numbers above; the denominator mechanism is the UIS
definition, reported as the coherent explanation (not separately re-derived here).
