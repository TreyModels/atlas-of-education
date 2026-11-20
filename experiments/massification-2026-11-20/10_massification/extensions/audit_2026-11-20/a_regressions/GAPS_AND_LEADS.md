# GAPS AND LEADS — what the regression evidence does not test, and what it could test next

**Companion to** [`REGRESSION_INVENTORY.md`](REGRESSION_INVENTORY.md) and [`REGRESSION_INVENTORY.csv`](REGRESSION_INVENTORY.csv).
Every number below is cited to the artefact it came from (ids as in the inventory). No new estimate was computed for this file.

**Prerequisite, before anything else.** Three numbers that the phase narrative leans on do not reproduce from disk:
the cross-country capacity "null" (FLAG-02), the PHL "+35.2 into the crossing" (FLAG-03), and the single-measure crossing vector
(FLAG-05). Any new direction should be built on re-derived numbers, not on those. This is a 1–2 day bookkeeping task, not a research
programme.

---

## (a) Untested, or only partially tested on disk

| relation | state on disk | evidence | why it stops |
|---|---|---|---|
| **Returns to schooling → enrolment / tutoring** | **UNTESTED** | `model2/runs/scaling_estimates.csv` row 90: "UNABLE: no earnings microdata in any on-disk panel; 8.8% Mincer is calibration-only"; `09_relations/LITERATURE_ELASTICITIES.md` §1 "Country Mincer returns NOT SUPPLIED"; R26 "not identifiable" (4 countries, 3 survey years) | PSA FIES/APIS + LFS are credentialed (403). The model's `+0.9·log1p(ret_S)` is a prior with no estimate behind it (`MODEL_PLUG_MAP.md` A-table, R26). |
| **Signalling / MMI (credential vs skill)** | **UNTESTED** | `10_massification/STATUS.md` §3g D48: signalling/MMI is *design-only*, listed in every results file, never modelled; `LITERATURE_ELASTICITIES.md` records WB Enterprise Surveys 403/000 | Needs the Enterprise Surveys credential/skills module + establishment census; both are HELD asks. No proxy on disk. |
| **Queue / graduate absorption** | **ONLY A PROXY RATIO** | X3 (`cluster_1_absorption/results/X3_queue_depth.csv`) = BA+ attainment ÷ wage-share, **+0.366 (CI 0.198…0.534)**; Council relabelled it derived/mechanical; X1 and X2 are nulls with CIs spanning zero (X1 −0.86, CI −3.91…+2.20; X2 +0.80, CI −0.40…+2.00) | No graduate unemployment, vacancy, or queue-length series exists on disk. The ratio's numerator is a stock and its denominator a wage share, so it is close to mechanical. |
| **Sector-level demand** | **TESTED ONLY ON MODELLED SHARES, ALL NULL** | E5 (`E5_tertiary_structure.csv`): services slope −0.495 (0.217) flips to **+1.82** without log GDP → not robust; Y1 (`Y1_correlations.csv`): agri-share account discarded (−0.105 after income control); X1 services proxy −1.90 (CI −5.92…+2.13); `JOBS_AND_MARKETS_PANEL.csv` SL.* rows are **ILO-modelled**, not measured | The only sector series are ILO modelled estimates; the demand channel has never been tested on a measured sector-employment or vacancy series. |
| **Compulsory-schooling / expansion events, HKG–KOR–KHM** | **DATA BLOCKED** | R27 "not estimated — observed 6-country panel has <13 usable observations per event window"; `EVENT_WINDOWS.md` §4–5: 10 of 20 event rows UNABLE; `SCHOOL_EXPANSION.csv` is **PHL-only** (27 rows) | Observed GER series start ~1998 for these systems; national series (EDB/KEDI/MoEYS) not on disk. Never imputed — correctly. |
| **Teacher supply → learning** | **UNTESTED** | `09_relations/DATA_PATTERNS.md` §6: "no learning outcome on disk for 30 countries"; PISA/TIMSS absent | No learning measure in any panel. The PTR→learning chain is assumed, not tested. |
| **Causal spending → enrolment** | **CORRELATIONAL ONLY** | R01/B02 S01: 0.152 (0.110) levels, 0.014 first differences; B03 Asia split +0.189 (0.090) | No instrument and no rule-based discontinuity in the data; a school-finance reform is named as the way to close it. |
| **Capacity dimensions (fiscal / delivery / enforcement)** | **1 OF 3 MEASURED** | E7: "only delivery capacity has coverage; fiscal/enforcement missing" → DATA LIMITED; `state_capacity.csv` governance weight 0.15 blocked (WGI `GE.EST`), index renormalised to 0.85 coverage | WGI 403; `STATE_CAPACITY.csv` enforcement rows are de jure proxies. |
| **Portability (CHN/HKG)** | **DESIGN-ONLY, NEVER RUN** | Y5: 6/6 inputs present for both countries, 12/12 rows, 0 new asks, DATA-COMPLETE; `STATUS.md` §3q: PARKED-ARMED (D75) | Not a data gap — a decision gap. Requires a new Council decision + predeclaration (R20/R22). |
| **PHL upper-secondary never-crossing** | **OBSERVED, NOT EXPLAINED** | PHL completion_upper_secondary 76.43 (2017) → 75.03 (2024), never ≥90 (C01); capacity rose throughout (A18) | No artefact on disk tests *why* the ceiling did not move. Y1 screened one account (opportunity cost) and discarded it. |

---

## (b) Regressions that can become a model-channel test rather than another correlation

Each of these already carries a model-side counterpart, so the marginal work is a **predeclared in-model check**, not a new regression.

1. **A13 `push_pull_tests.csv` → the *asymmetry* as a moment test (orientation-corrected, see FLAG-00).** Correctly read, the file says: **income growth → tertiary GER F=6.52, p<0.001**, but **tertiary GER → income growth F=0.65, p=0.66**; **secondary GER → wage share F=4.11, p=0.001**, while wage share → secondary GER is F=1.88, p=0.094; income → completion **−0.667**; education → growth null in all three. That one-way pattern is a far sharper target than either number alone. Require the model, under each of the three orderings, to reproduce **both the significant direction and the null in the reverse direction** — a model that produces a symmetric lead-lag is falsified, and so is one that produces neither.
2. **A12 `scaling_laws.csv` within/between *gap* → structural target.** Industry share←GDPpc is **0.528 within vs 0.143 between**; agriculture **−0.120 vs −0.990**. The gap is a property of any model with a sector block and is estimated at n=1,017 (`scaling_laws.csv` S7/S8). Make the gap (not the level) the object the model must reproduce — a genuine discriminator between demand-led and supply-led structural change.
3. **A10/A11 E6 → model selection gate.** Score the model's generated curve with the *same* four-form holdout comparison (logistic / Gompertz / linear / exponential, 2011–2024) it was judged by. A model that cannot beat its own linear-trend benchmark (4.35 pp per `MASSIFICATION_CLOSEOUT.md` §2, provenance `model/calib/calibration_table.csv`) fails the shape test regardless of fit — this converts A10/A11 from description into a pass/fail instrument.
4. **A17 `capacity_leadlag.csv` → signed within-country moment.** PHL primary lag +5 r=+0.509 vs KHM lower-sec lag 0 r=−0.719. The *sign flip across countries* is a falsifiable prediction of a capacity-gated arm: a model whose capacity channel is monotone cannot produce both. Use it as a two-cell moment test, not as evidence.
5. **Y2 → a negative moment (anti-overfit constraint).** Max |partial r| after own-lag control is **0.208** across 24 cells; zero-order co-movement 0.49–0.71 is shared trend. Any model that generates a strong schooling↔market lead-lag is over-fitting the visible co-movement. This is the cheapest available specification test in the programme.
6. **X13 Amendment B1 → observed extensive-margin design.** The only channel the toy moved was *whether* a system crosses at all (77% → 100% of seeds), not when (+1.0 y). That is directly testable in the observed record: PHL's 17 regions already contain both crossed and never-crossed systems (`BASELINE_SERIES.csv`, 144 rows; X10–X12 replicate at 17/17).

---

## (c) Where the data can and cannot discriminate

**Can discriminate (these are worth spending on):**

- **PHL regional panel — 17 regions, 2 cohorts, 144 rows** (`BASELINE_SERIES.csv`). National income is common across regions, so a regional contrast can separate provision/capacity from income demand. Replicated three ways already (X10 ρ=−0.444, X11 ρ=−0.622, X12 ratio 1.098), and the same file supports an extensive-margin (crossed vs never-crossed regions) test.
- **Level-specific timing inside one system.** Primary 2017, lower-secondary 2024, upper-secondary never (C01/A01). A single-curve model cannot produce a 7-year floor-to-middle gap and a hard ceiling at 75 %; that asymmetry is a discriminating moment (R23), and the data are observed rather than reconstructed.
- **Within vs between scaling gap at n≈1,000** (A12: secondary GER n=1,042, tertiary 1,037, sector shares 1,017). Precise enough to reject a model whose sector block is a relabelled income term; the tertiary exponent alone is 0.848 (0.172) within vs 0.567 (0.082) between.
- **Two large, well-dated, aligned state pushes.** HKG 2009 **+9.08 pp (t=5.20)** and CHN 1999 **+4.70 pp (t=7.94)** (A14). Only two, but they are the only events in the programme where the sign, size and date agree — usable as out-of-sample mechanism checks for a state-push channel.
- **The free-tuition dip with a known confound.** PHL 2018 tertiary window is negative (−5.39 pp / −28.9 %) and the K-12 cohort delay is a competing, dated explanation. A model with cohort flows but **no** tuition elasticity should reproduce it; that is a sharp, parameter-free falsifier.

**Cannot discriminate (stop trying with these data):**

- **Push vs pull direction from panel moments** — forced-ID 1.00, pure push/pull recoverable 1.00, outside truth forced 1.00 (M2c; `MASSIFICATION_CLOSEOUT.md` §3). Any further panel lead-lag cannot break the equivalence.
- **Cross-country capacity → timing** — n=5, censored outcomes, and the index composition breaks at 2014 and 2018 (A18 coverage 0.35→0.90→0.55). Even the +0.900 (p=0.037) in A16 is one country (JPN at 20.0).
- **JPN / KOR timing** — left-censored before 1971 (A01); only an inequality is admissible until pre-1971 national series are on disk.
- **HKG completion levels** — no UIS completion series; the HKG lower-secondary NER "crossing" 2015–16 is a measure artefact (`EVENT_WINDOWS.md` §5).
- **Secondary→tertiary spacing** — n=3 dated countries (X6 UNABLE), and the HKG gap needs a substitution.
- **Any causal policy effect** — no control group in any single-country event window (A20 hard caveats: naive SE, quality A/B/C, R25).
- **Returns, signalling, queue, learning quality** — no data at all (see (a)).

---

## (d) Five candidate directions this regression evidence would support

1. **Level-disaggregated capacity test** — use PHL's annual, level-specific teacher/PTR series (`STATE_CAPACITY.csv` delivery dimension; `SCHOOL_EXPANSION.csv` 27 PHL rows) to ask whether the primary *floor* and the upper-secondary *ceiling* diverge because teacher supply is level-specific, not because aggregate capacity is low; a within-country, level-disaggregated design the data can actually support.
2. **Cohort-size shock as the one plausibly-causal test** — R07 (fertility→primary completion −0.189, se 0.044; negative in all 10 splits of B03, significant in 8, the exceptions being high-urban p=0.083 and high-GER p=0.400) is the only graded-causal relation in the register; test it as a cohort-shock design using observed births 15 years earlier rather than as another panel correlation.
3. **Free-tuition cohort-delay falsifier** — predeclare that a cohort-flow model with K-12 delay and *zero* tuition elasticity must reproduce the −5.39 pp / −28.9 % PHL 2018 tertiary window; a model needing a tuition parameter to fit it is falsified (`ger_tertiary` 1971–2026, `POLICY_TIMELINE.csv`).
4. **Extensive-margin fragmentation** — take the one channel the toy moved (probability of crossing ever: 77 %→100 %, X13-B1) and test it on the observed record: do PHL regions with more providers/markets have a higher probability of crossing at all, not an earlier crossing date (17 regions, 144 rows).
5. **Within/between gap as the structural target** — replace level-fitting with the requirement that the model reproduce the within-vs-between sector gap (industry 0.528/0.143; agriculture −0.120/−0.990), which distinguishes a demand-led from a supply-led sector block at n=1,017 and cannot be satisfied by a relabelled income term.

**One line on what I would not do next:** another descriptive battery on the same six systems. Battery B's and C's own verdicts (5 NOT SUPPORTED, 1 DATA LIMITED, 1 UNABLE; Y1–Y3 NOT SUPPORTED) are the regression evidence telling the Council that the marginal descriptive return on these six countries is near zero — the binding constraints are the four missing datasets in (a), not the number of specifications.
