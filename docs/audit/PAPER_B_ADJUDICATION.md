# PAPER B — ADJUDICATION

**Manuscript:** *Why Tutoring Taxes Backfire and Expanding Elite Seats Fuels the Arms Race: A Comparative
Structural Study of Shadow Education in Hong Kong and South Korea* (Trey Menefee, Atlas of Education Research
Program). File `papers/shadow-education-contest/paper_b_hk_korea/Shadow_Education_Arms_Race_HK_Korea_APA.docx`,
642,328 B, sha256 `fe63be84fe873ef57f1dde5ae0d588077d957b75d127b7a656a7fc884d8b9602`.
**Adjudicator:** `paper-adjudicator` (independent; did not write the engine repairs, the audit, or the manuscript).
**Date:** 2026-11-25. **Branch:** `research/contest-audit-v2-2026-11-25`. **Mode:** read-only synthesis; no experiments run.
**Taxonomy (verbatim, one status per claim):** `VERIFIED EMPIRICAL` · `REPRODUCED SIMULATION` ·
`VALIDATED SIMULATION` · `AUTHOR-REPORTED` · `CONTRADICTED` · `UNRESOLVED`.

## 0. Bottom line

**Every substantive counterfactual conclusion in Paper B is an artefact of either a different result generation or
a repaired engine defect. None of the headline policy claims survives.**

* The manuscript's tables are the **420-run generation** (`N=400`, `T=70`, 14 arms). That generation has **no
  runnable runner** — the docx tables match the author self-reported JSON
  (`code/results/verified_results_2026_11_25.json`, sha256 `b14e2816…b1de`) exactly, but that JSON is not a run
  and cannot be reproduced against the committed engine. → **AUTHOR-REPORTED**.
* The only reproduced generation is the **540-run** (`N=300`, `T=46`, 18 arms). On the pre-repair engine its
  calibration fails badly (KR Q5−Q1 gap 68.36 pp vs target 32.1; spend ratio 18.01× vs 3.4×; KR K–12 participation
  57.4 % vs 76.5 %). **Most of that "failure" is the expected-vs-realised probability defect (D2), not a
  parameterisation failure**: after the repair and with **no re-estimation**, the KR gap moves to 29.71 pp and the
  ratio to 2.11×. But participation and grade-12 participation are still far off (KR K–12 58.4 %; HK G12 49.3 %;
  KR G12 36.0 % vs a 71.8 % target). → the paper's calibration table is **not reproduced (AUTHOR-REPORTED / UNVERIFIED)**, and the review's
  framing of the 540 as a lost calibration is **partly wrong**.
* **The policy findings reverse under repair.** The +50 % tax raises spend and Q5 capture pre-repair; after repair
  it **lowers** both (HK spend 96.49, elite 24.67 vs 25.01; KR 96.88, 21.57 vs 22.13). Wage compression raises Q5
  capture pre-repair; after repair it **lowers** it (HK 23.64; KR 21.48). Effort caps broaden participation
  pre-repair; after repair participation is **flat**. The "only CF1b wins" result becomes "CF1b fails spend and
  CF4a/CF3b pass". The combined-policy claim is therefore **spec-dependent**, not established.
* **The 2024 Korean medical-seat episode is not "reproduced."** A simulation cannot reproduce a historical event;
  the empirical episode itself has unresolved provenance (2,000 proposed vs ~1,500 finalised; 2024 spend KRW 29.2 tn
  vs ~27.5 tn in 2025) and rests on an unreviewed arXiv preprint and news sources.

**Publishability verdict:** the manuscript is **not publishable** as a calibrated structural comparative study in
any form similar to the current draft. Its only defensible future form is a **methods/negative paper** about
specification dependence and expected-probability consistency — and that requires Gate-2 calibration and Gate-3
policy re-runs that have not happened. The current text must not be submitted.

## 1. The three generations, and why the table generation matters

| | 420 generation (manuscript Tables 2–4) | 540 generation, pre-repair (reproduced) | 540 generation, repaired engine (Gate-1 migration) |
|---|---|---|---|
| design | 14 arms × 30 seeds; `N=400`, `T=70`; y_median 3.0; alpha 1.2/1.25; price .12/.11; `max_e` 4.0/4.5; `elite_logw` .85/1.15; bar gates 0/0/0 | 18 arms × 30 seeds; `N=300`, `T=46`; alpha .25; price .16; `max_e` 6.0; `elite_logw` .50/.60; gates 2/4/10 | same 540 config, repaired engine `98baf6b` |
| runner | **none runnable** (old `Engine(cfg, modules=…)`/`e.history` API) | `run_hk_korea_comparative.py` (committed, reproduced) | same runner on repaired engine |
| artifact | `verified_results_2026_11_25.json` (self-reported) | `code/results/hk_korea_comparative_with_cf4.json` (sha256 `c1fa0926…2e99`) | `results/audit/commander/hk_korea_540_REPAIRED_box98baf6b_2026-11-25.json` (sha256 `455649da…`) |
| evidence status | **AUTHOR-REPORTED** | **REPRODUCED SIMULATION** | **REPRODUCED SIMULATION** (uncalibrated, not validated) |
| HK baseline elite Q5 | 30.0 % | 46.36 % | 25.01 % |
| KR baseline elite Q5 | 24.6 % | 36.12 % | 22.13 % |
| KR K–12 participation | 76.5 % | 57.44 % | 58.38 % |
| HK G12 participation | 71.6 % | 72.37 % | 49.30 % |
| KR G12 participation | 71.8 % | 73.69 % | 36.00 % |
| KR Q5−Q1 gap | 34.1 pp | 68.36 pp | 29.71 pp |
| KR Q5/Q1 ratio | 3.19× | 18.01× | 2.11× |

**Hard rule for this adjudication:** the manuscript's numbers are the 420 generation and are citable only as
AUTHOR-REPORTED. The 540 numbers are reproduced simulation but are a **different design**; they cannot be used to
"confirm" the manuscript's magnitudes. The repaired-engine numbers are the most current evidence but are
**uncalibrated** and therefore cannot be used as policy estimates either. No table in the manuscript can be
presented as reproduced.

**What the 420 record actually is.** I re-extracted the docx tables and compared them cell-by-cell with
`verified_results_2026_11_25.json -> paperB_hk_korea_comparative`. All seven rows of Table 3 and all seven rows of
Table 4 match exactly (e.g. HK baseline `40.0/53.8/71.6`, `+52.8 pp/11.83×`, `100.0`, `30.0`; KR CF3b
`68.3/85.2/57.4`, `+37.6 pp/4.62×`, `54.9`, `27.5`). The tables are therefore a verbatim rendering of an
unreproduced, author-supplied JSON.

### 1b. The repaired 540 is a NEW GENERATION — provenance and what changed

Per the operator decision, the repaired-engine run is a **new generation**, not a correction of the 420 numbers.
It carries its own engine and parameter provenance, and it must be cited with that provenance:

* **engine commit `98baf6b`** (Gate-1 tree: `f31e176` + `6bc8d61` + `1a6f3d5`/`23a0173`); `core.py`
  `72cbddf7…`, `rng.py` `ada4a760…`, `contest_math.py` `23a01730…`, `tutoring.py` `7a6fd4c3…`, `labour.py`
  `0ccfb3ce…`, `planning.py` `13d91bc9…` (full list in `AUDIT_VERDICT.md` §5A / `canonical_spec.json`);
* **design** `N=300`, `T=46`, `measure_from=18`, 18 arms × 30 matched seeds = 540; HK single G12 gate `share=0.23`;
  KR stacked G9 `share=0.35` + G12 `share=0.12`;
* **the actual run** (`455649da…`) used the **legacy 540 gate list** — the frozen `canonical_spec.json`
  (V540-FREEZE, `GATE_SPECS` KR-TRACKED / KR-SINGLE, hardened runner `932515ca…`) is a **new, not-yet-executed**
  frozen spec; do not label the regenerated tables "canonical-spec";
* **what changed**: D1 KR G9 phantom prize → persistent track consequence; D2 expected P = exact Plackett–Luce
  (2.41×/1.96× → 1.0000); D3 applicants-based seat denominator (0.513 → 0.2500 realised admit rate); D6
  policy-invariant RNG (51 → 0 mismatches); D4/D5 tax/outlay/receipt ledger; D7 labour prizes last;
* **explicit CF4 reversal**: pre-repair CF4a **fails HK equity** (48.64 % > 46.36 %) and CF1b is the only pass;
  repaired CF4a is **Win-Win in both** (HK 70.58/23.44; KR 72.48/21.47), **CF1b no longer passes** (spend 97.21/99.25),
  CF4b still fails, CF3b passes. The old failure stays reported as the prior result.

## 2. Claim-by-claim adjudication

### 2.1 Calibration and empirical targets

| ID | Claim (manuscript location) | Supporting / refuting artifact | Status | Required change |
|---|---|---|---|---|
| B-01 | Design: "14 arms, 420 runs, 30 matched stochastic seeds", `N=400`, `T=70` (abstract, Method, Table 3/4 notes, Conclusion) | The 420-era runner/engine generation was **not found in the locations searched** (bundles, archive `46950ab`, all `research/*` branches, worktrees); the old runner targets an older `Engine(cfg, modules=…)` API and is not runnable (`MISSING_ARTIFACTS.md`; `RECONCILIATION.md`; `LEAD_GROUND_TRUTH.md` §5.1). Tables match the self-reported JSON exactly (see §1). **This is not a claim that the 420 artefacts do not exist** (operator decision); it is the basis for the **AUTHOR-REPORTED BASELINE** label. | **AUTHOR-REPORTED** | Label the design and every table "AUTHOR-REPORTED / UNVERIFIED 420 generation; not reproduced". If the 420 runner turns up, deposit it; otherwise re-specify on the canonical engine. |
| B-02 | Table 1 structural parameters: single Grade-12 gate HK `S=0.23`; stacked KR `S₁₂=0.12`; `fail="track"`; `own_teacher=False`; higher ΔV in Korea (Method, Table 1) | No source artifact found for the parameter values. These are **assumptions**, not measurements. The 540 runner uses `N=300`/`T=46` and different parameters (`GATE_SPECS` in the repaired engine; `GATE2_PLAN.md` §1b). | **AUTHOR-REPORTED** | Label as pre-registered structural assumptions; cite an empirical basis for `S`/`S₁₂` or mark as calibration choices. |
| B-03 | HK Grade-9 participation **53.8 % exact match** (Table 2; Results ¶1) | 420 self-reported JSON (`HK_G9: target 53.8, sim 53.8`) only. 540 run does not report Grade 9. | **AUTHOR-REPORTED** | Cannot be verified. If retained, mark `AUTHOR-REPORTED`; on the repaired engine there is no Grade-9 calibration check at all. |
| B-04 | HK Grade-12 participation **71.6 % vs 71.8 %**; ramp +17.8 vs +18.0 pp (Table 2; Results ¶1) | 420 self-reported JSON. The 540 repaired run gives HK G12 **49.30 %** (baseline), far from 71.8 %. | **AUTHOR-REPORTED** | Delete the claim from the calibration table or mark author-reported; the only current engine run contradicts the target badly. |
| B-05 | KR overall K–12 participation **76.5 %**, "inside the published 2023–2025 corridor 75.7 %–78.5 %" (Table 2; Results ¶1; abstract) | `docs/audit/GATE2_BENCHMARK_REGISTRY.csv`: KR 2024 = **80.0 %** (`KR_part_2024`); KR 2025 = **75.7 %** (`KR_part_2025`, held out); the 76.5 % band is a **DERIVED target, DIAGNOSTIC ONLY — never in fit**. Repaired 540 run: KR K–12 **58.38 %**. | **AUTHOR-REPORTED** (and mislabelled) | Correct to the registry: 2024 = 80.0 %, 2025 = 75.7 % (held-out, never pooled); remove 76.5 % from the calibration fit (registry rule); the current engine does not reproduce any value in the band. |
| B-06 | KR Q5−Q1 gap **34.1 pp vs published +32.1 pp** (84.9 % vs 52.8 %) (Table 2; abstract) | 420 self-reported JSON. Registry `KR_gap_q5_q1_participation` = **32.1 pp is a DERIVED TARGET** from a legacy pre-registered sweep — *"original empirical source/citation NOT located"* — explicitly **not an observation**; tolerance 3.0 pp; household-income brackets vs simulated ability quintiles is undeclared. Repaired 540: 29.71 pp (2.4 pp below target). | **AUTHOR-REPORTED** (target mislabelled as published) | Relabel the target "derived calibration target (source unlocated)"; declare the income-bracket→simulated-quintile mapping; do not call 34.1 a match to a published number. |
| B-07 | KR Q5/Q1 spend ratio **3.19× vs published 3.4×** (662k vs 192k KRW/month) (Table 2; abstract) | 420 self-reported JSON. Registry `KR_spend_ratio_q5_q1` = **3.4× is a DERIVED TARGET** (source unlocated); target is **per-student**, and mixing per-student/per-participant expenditure is a known cause of the earlier calibration failure. | **AUTHOR-REPORTED** (target mislabelled) | Same as B-06; state per-student definition; the 662k/192k figures are not in the committed benchmark record. |
| B-08 | Table 2 "Published Target" and "Source" columns attribute 32.1 pp / 3.4× / 662k / 192k to "SeoulStart" and claim published/observed status | `GATE2_BENCHMARK_REGISTRY.csv` rows `KR_gap_q5_q1_participation`, `KR_spend_ratio_q5_q1`: derived targets, source not located, and `KR_part_target_76_5` is explicitly diagnostic-only. `SeoulStart` is a secondary web summary, not a statistical source. | **CONTRADICTED** | Rebuild the table with the registry: primary source + survey year + population + denominator per row; derived targets marked as targets; remove the "published/observed" language. |
| B-09 | "Participation stood at 78.5 % in 2023 and 75.7 % in 2025" (Introduction ¶1) | Registry has 2024 = 80.0 % and 2025 = 75.7 %; 78.5 % (2023) is not in the registry. Citation is `SBS News`/`SeoulStart`. | **AUTHOR-REPORTED** | Correct to the registry values with the KEDI survey citation; do not use news summaries for calibration targets. |
| B-10 | HK benchmarks 53.8 % (Grade 9) / 71.8 % (Grade 12), 2011/12 survey (abstract, Table 2, Introduction) | Registry `HK_part_g9_2011_12`, `HK_part_g12_2011_12`: **"citation to be verified in G2-A; not yet supplied"**; Grade-12 is a HELD-OUT moment (same survey as Grade 9 — declare dependence, not independent validation). | **AUTHOR-REPORTED** | Add the primary survey citation, year, population, denominator; state that Grade 12 is held out and dependent on Grade 9, not independent validation. |

### 2.2 Counterfactual tables

| ID | Claim | Artifact | Status | Required change |
|---|---|---|---|---|
| B-11 | Table 3: Hong Kong 7-arm counterfactual table (K–12/G9/G12 rates, Q5−Q1 gap/spend ratio, spend index, elite Q5 share) | 420 self-reported JSON only; matches docx exactly; no runnable runner. | **AUTHOR-REPORTED** | Regenerate all tables from the frozen canonical spec after Gate-2 calibration; until then label author-reported. |
| B-12 | Table 4: South Korea 7-arm counterfactual table | same | **AUTHOR-REPORTED** | Same as B-11. |
| B-13 | Figure 2 ("counterfactual policy impact on spend"), Figure 3 ("seat-expansion paradox"), Figure 4 ("trade-off frontier"), Figure 1 (calibration) | four PNGs were extracted and visually match the handoff numbers (`RECONCILIATION.md`), but were **not regenerated** from any reproduced generation; the 540 run has 18 arms, not the 14 in the figures. | **AUTHOR-REPORTED** | Regenerate every figure from the canonical result file; do not present 420-generation charts beside 540-generation text. |

### 2.3 The three "findings" and the conclusion

| ID | Claim | Artifact | Status | Required change |
|---|---|---|---|---|
| B-14 | **Finding 1**: a +50 % tutoring tax "backfires on both total spending (+4.8 % HK; +7.4 % KR) and equity", raising Q5 elite share to 34.2 % / 26.0 % (abstract, Results "Finding 1") | Pre-repair 540 **does** reproduce the direction (HK spend 107.42; elite 52.43 vs 46.36; KR 106.46; elite 41.75 vs 36.12). **Repaired engine reverses it**: HK spend 96.49 (< 100), elite 24.67 (< 25.01); KR spend 96.88, elite 21.57 (< 22.13). The direction was produced by the D2 expected-probability mispricing. | **CONTRADICTED** (as a structural law) | Rewrite as a specification-dependent result. Report pre-repair (backfires) and repaired (does not backfire) side by side; do not call it a law. |
| B-15 | **Finding 1b**: the Q5/Q1 spend ratio "jumps" from 11.83× to 16.85× (HK) and 3.19× to 4.13× (KR) | 420 only. Repaired 540: HK 2.47 → 2.63 (up); KR 2.11 → 1.98 (**down**) — mixed, not a jump. Pre-repair 540: HK 39.81 → 90.33, KR 18.01 → 25.72. | **CONTRADICTED** (in both jurisdictions) | Same as B-14; report per-jurisdiction; note the KR direction flips. |
| B-16 | **Finding 1c**: Q5 elite admission share rises 30.0 % → 34.2 % (HK) and 24.6 % → 26.0 % (KR) | 420 only; pre-repair 540 reproduces (52.43 vs 46.36; 41.75 vs 36.12); repaired 540 reverses (24.67 vs 25.01; 21.57 vs 22.13). | **CONTRADICTED** (as a structural law) | Same as B-14. |
| B-17 | **Finding 2**: expanding elite seats raises Grade-12 participation — KR CF2a 71.8 % → 82.0 % (+10.2 pp), CF2b 99.6 %; HK CF2b 97.1 % (abstract, Results "Finding 2") | Direction reproduced: pre-repair 540 HK G12 72.37 → 75.66 (CF2a) / 85.65 (CF2b), KR 73.69 → 79.08 / 95.58; repaired 540 HK 49.30 → 52.39 / 56.44, KR 36.00 → 41.18 / 54.93. **Magnitudes are generation-specific and not reproduced.** | **REPRODUCED SIMULATION** (direction only) | Keep only direction, labelled conditional simulation; replace 420 magnitudes with the reproduced 540 values and state they are uncalibrated. |
| B-18 | **Finding 2b**: seat expansion raises total spend (+73.8 % HK; +22.3 % KR for CF2b; +17.4 % / +5.9 % for CF2a) | Direction reproduced: pre-repair 540 HK 149.30, KR 128.00; repaired 540 HK 131.76, KR 156.76 (all > 100). Magnitudes differ. | **REPRODUCED SIMULATION** (direction only) | Same as B-17: 540 values, conditional label. |
| B-19 | **Finding 2c**: seat expansion "does improve admission equity — lowering Q5 elite share from 30.0 % to 24.8 % (HK) and 24.6 % to 21.6 % (KR)" | Pre-repair 540: HK 46.36 → 33.62 (CF2b), KR 36.12 → 22.01 (falls). **Repaired 540: HK 25.01 → 22.99 (falls) but KR 22.13 → 22.27 (CF2a, rises) / 22.13 (CF2b, flat)** — no KR equity gain. | **CONTRADICTED** | Restrict to Hong Kong; report KR as null. |
| B-20 | **Finding 2d**: the model "directly explains" / "reproduces" the 2024 Korean medical-seat shock; because marginal returns scale with P(1−P) "peaking at S = 0.50" (abstract, Results, Figure 3 note, Discussion) | A simulation cannot reproduce a historical event. The 2024 episode is not a clean natural experiment (2,000 proposed vs ~1,500 finalised; 2024 spend KRW 29.2 tn, 2025 ~27.5 tn — a decline; CSAT repeaters 161,784 is a single-year coincidence). The archived "100 % seat-expansion paradox" that motivated the P(1−P) story is **CONTRADICTED** as an S-grid truncation artefact; the corrected exact-PL surface is an **inverted-U ending at 0** (positive-gradient share 52 %, not 100 %). | **CONTRADICTED** | Rewrite as "an illustrative mechanism that is *consistent with* the episode"; remove "reproduces", "directly explains", "proves". Add the 2024/2025 data limitations. Do not cite a P(1−P) peak at S=0.50 as a theoretical fact — it is an assumption of this model. |
| B-21 | **Finding 3**: "Binding effort caps / curfews (CF1b) are the only single lever that moves both systems into the win-win quadrant" (spend 82.1 / 74.1; elite 25.1 % / 22.9 %) | Pre-repair 540 reproduces: CF1b spend 67.39 (HK) / 76.42 (KR) < 80; elite 41.96 / 26.39 below baselines — the only passing arm. **Repaired engine: CF1b fails spend** (HK 97.21, KR 99.25 ≥ 80); CF3b and CF4a pass. | **CONTRADICTED** | Delete the "only CF1b" ranking; report the pre-repair and repaired verdicts together; no arm is established under an uncalibrated spec. |
| B-22 | **Finding 3b / abstract / conclusion**: "Only pairing wage compression (ΔV ↓) with effort caps or seat expansion reaches the win-win frontier"; "Even deeper progress ... requires combining ΔV compression with effort caps or targeted seat expansion" | The manuscript's own 14-arm tables contain **no combined arms** (no CF4a/CF4b rows), so the claim has no supporting table. The later 540 reproduction **falsified it pre-repair** (CF4a fails HK equity 48.64 > 46.36; CF4b fails spend 90.88/88.04). On the repaired engine **CF4a passes both** (HK 70.58/23.44; KR 72.48/21.47) and CF3b passes. The 420-port legacy V1 also passes CF4a in both. Three generations give three verdicts. | **CONTRADICTED** (as an established conclusion) | Remove the "only pairing" claim. Add a specification-dependence note; the combined-policy result is **not established** in any direction until the canonical spec is calibrated (Gate 2) and re-run (Gate 3). |
| B-23 | **Finding 3c**: pure wage compression delivers the deepest spend cuts but "Q5 elite capture rises modestly (to 36.3 % HK and 27.5 % KR under CF3b)" | Pre-repair 540 reproduces (HK 59.02 vs 46.36; KR 47.66 vs 36.12). **Repaired engine reverses**: HK 23.64 vs 25.01; KR 21.48 vs 22.13 (falls). | **CONTRADICTED** (as a structural law) | Rewrite as D2-artefact-dependent; report the repaired direction. |
| B-24 | **Finding 3d**: effort caps broaden participation (K–12 51.1 % HK / 86.0 % KR under CF1b) | 420 only. Pre-repair 540: HK 59.07 → 65.06, KR 57.44 → 63.15 (big rise). **Repaired: HK 61.92 → 61.98, KR 58.38 → 58.46 (flat).** The participation broadening is a D2 artefact. | **CONTRADICTED** | Delete the participation-broadening claim; the repaired engine shows essentially flat participation with contest effort down 98–99 %. |
| B-25 | "Every single policy lever produces qualitatively identical directional dynamics in both economies"; "the underlying Tullock contest mechanics yield the exact same policy hierarchy" (Results ¶, Discussion ¶3) | False across the evidence: pre-repair CF4a fails HK but passes KR; repaired CF2a raises KR elite share but lowers HK; repaired tax lowers spend in both but raises the HK ratio and lowers the KR ratio; 420 vs 540 vs repaired hierarchies differ. | **CONTRADICTED** | Delete; report jurisdiction-specific and spec-specific verdicts. |
| B-26 | **Conclusion**: "Calibrated across 420 matched simulation runs, our comparative structural model demonstrates why ..." (Conclusion ¶1; abstract) | The 420 run was **not reproduced (AUTHOR-REPORTED / UNVERIFIED)**; the reproduced 540 run does not recover the calibration (participation and grade-12 far off target) and its policy signs reverse after repair. "Demonstrates" is unsupported. | **CONTRADICTED** | Rewrite the conclusion as a conditional simulation with explicit generation/spec labels; remove "demonstrates" and "calibrated". |

### 2.4 Empirical context, assumptions and provenance

| ID | Claim | Artifact | Status | Required change |
|---|---|---|---|---|
| B-27 | 2024 Korean medical-seat episode: announced 2,000 seats; private-education expenditure KRW 29.2 tn; CSAT repeaters 161,784 (31.0 % of applicants) (Introduction ¶1, Finding 2, Discussion) | `arXiv:2608.27980` (unreviewed preprint) + news summaries. Review §6/`REVIEW_RESPONSE_2026-11-25.md`: proposed 2,000, **finalised ~1,500**; 2024 spend KRW 29.2 tn, **2025 ~27.5 tn**. No primary statistical source deposited. | **AUTHOR-REPORTED** | Add proposed-vs-finalised, the 2025 decline, primary source, and the single-year coincidence caveat; remove causal/reproduction language (see B-20). |
| B-28 | "27 % of surveyed parents cite private education costs as a direct driver of Korea's record-low fertility" (Introduction ¶1) | News source (`SBS News`); no survey citation, denominator, or year. | **AUTHOR-REPORTED** | Cite the survey; if unavailable, delete. |
| B-29 | "Consistent with universal K–12 schooling, Hong Kong's simulated K–12 liquidity dropout rate is 0.00 %" (Table 2, Results ¶1) | This is true **by construction** in the model (`fail="track"`, no dropout channel for non-winners), not a calibration achievement. | **AUTHOR-REPORTED** (tautological) | State that it follows from `fail="track"` by design; do not present as a calibration match. |
| B-30 | "Simulated elementary-school tutoring rate 74.8 % sits below the simulated Grade-9 rate 89.3 %, whereas published Korean surveys show elementary ~86 %" (Results "honest divergences") | 420 self-reported JSON only; the "published ~86 %" has no committed citation/year/denominator. | **AUTHOR-REPORTED** | Cite the survey; label the divergence as model-scope (pure exam-contest demand), which it already does. |
| B-31 | "Hong Kong's simulated pure-contest Q5/Q1 spend ratio (11.83×) is steeper than mixed-motive household surveys" (Results "honest divergences") | 420 only; no source artifact found. | **AUTHOR-REPORTED** | Mark AUTHOR-REPORTED / UNVERIFIED; no reproduced value exists. |
| B-32 | "30 matched stochastic seeds ... eliminates Monte Carlo sampling noise from cross-policy comparisons" (Method) | The 540 runner does use matched seeds and the reproduced run is seed-matched; but 30 seeds do not eliminate sampling uncertainty, and the manuscript reports ±95 % CIs from those seeds. | **AUTHOR-REPORTED** | Replace "eliminates Monte Carlo sampling noise" with "reduces common random-number noise across arms; seed uncertainty is reported as ±95 % CI". |
| B-33 | Review finding §4: "the 540 design lost the Korean calibration" (gap 68.36 vs 32.1; ratio 18.01 vs 3.4; participation differs) — cited in `REVIEW_RESPONSE_2026-11-25.md` §4 and repeated as a parameterisation failure | Pre-repair 540 values are real, **but** the Gate-1 migration shows the gap/ratio collapse is driven by the D2 contest-probability-consistency defect: after repair, with **no re-estimation**, gap 68.36 → **29.71** (target 32.1) and ratio 18.01 → **2.11** (target 3.4). Contest prep was 92–94 % of pre-repair K–12 spend; expected/realised was 2.41×/1.96× pre-repair and exactly 1.0000 after. | **CONTRADICTED** (as a parameterisation failure) | Rewrite §4: the pre-repair gap/ratio failure is largely a **code defect artefact**, not evidence that the 540 parameterisation is wrong. The residual deviations (29.71 vs 32.1; 2.11 vs 3.4) are the genuine calibration task. |
| B-34 | Review-response rebuttal (implicit in the paper's calibration claim): the 540 design **is** calibrated / recovers the benchmarks | Repaired 540: KR K–12 **58.38 %** vs 76.5 target; HK G12 **49.30 %** and KR G12 **36.00 %** vs a 71.8 target; residual gap/ratio off target. Participation is **not** recovered on any generation. | **CONTRADICTED** | Do not claim the 540 is calibrated. State: gap/ratio nearly recovered post-repair; participation and grade-12 participation remain genuine failures requiring Gate-2 calibration. |

### 2.5 The reproduced CF4 / Win-Win record (context the manuscript must absorb)

| ID | Claim | Artifact | Status | Required change |
|---|---|---|---|---|
| B-35 | Pre-repair 540 CF4 verdict: CF4a fails HK equity (48.64 % > 46.36 %), CF4b fails spend (90.88/88.04), **only CF1b passes** | `results/audit/commander/hk_korea_540_commander_independent_2026-11-25.json`; `code/REPRODUCTION_CF4_2026-11-25.md`; `GATE0_VERIFICATION.md`; `papers/.../README.md` | **REPRODUCED SIMULATION** (historical pre-repair result) | Report as the pre-repair generation; preserve it; do not generalise. |
| B-36 | Repaired-engine 540 CF4a is Win-Win in **both** jurisdictions (HK 70.58 spend / 23.44 elite vs baseline 25.01; KR 72.48 / 21.47 vs 22.13) | `docs/audit/GATE1_MIGRATION_TABLE.md`; `GATE1_REPORT.md`; repaired JSON (sha256 `455649da…`) | **REPRODUCED SIMULATION** (conditional, uncalibrated) | Report alongside B-35. This is the single most important correction to the paper's combined-policy claim. |
| B-37 | Repaired-engine CF4b still fails spend (HK 89.98; KR 105.54 ≥ 80) | same | **REPRODUCED SIMULATION** (conditional) | Report. |
| B-38 | Repaired-engine CF3b (ΔV −50 %) is Win-Win (HK 70.88 / 23.64; KR 72.55 / 21.48) and CF1b is **not** (97.21 / 99.25) | same | **REPRODUCED SIMULATION** (conditional) | Report; delete the "only CF1b" and "wage compression is regressive" claims. |
| B-39 | **CF4 verdict is specification-dependent**: 420-port legacy V1 → CF4a passes both; 540 pre-repair → CF4a fails HK; 540 repaired → CF4a passes both | `docs/audit/harvest/HARVEST.md` §4b (420-port V1, AUTHOR-REPORTED/PRE-REPAIR/UNCALIBRATED); `GATE1_MIGRATION_TABLE.md`; `GATE0`/`REPRODUCTION_CF4` | **REPRODUCED SIMULATION** (the spec-dependence fact) | State explicitly that the combined-policy conclusion is **spec-dependent and not established**; no policy recommendation may rest on it. |
| B-40 | **Provenance of the reproduced 540** (correction to the "missing Paper B scripts" framing): the 540 scripts/data are in hand and reproduced | `~/neon-boot/pulled/gemini-bundles/hk_korea_exact_bundle.zip` sha256 `e9cc02c2…be4e` (runner `dd0b1d8d…`, `core.py 618bd6dd…`, `tutoring.py b2d213b6…`, patch); `hk_korea_contest_code_bundle.zip` `da5cd1ee…e47f` (+ reference `851bb1df…`); `ALL_ATLAS_WORK_2026_11_25.zip` `f602ede3…4f74`; reproduced in Gate 0, rerun on the repaired engine (`455649da…`). The **420** design is the only Paper B artefact that is genuinely missing. | **REPRODUCED SIMULATION** | Cite this provenance for every 540 number; never describe the Paper B scripts/data as missing. The 420 tables remain AUTHOR-REPORTED (B-01). |

## 3. Status summary (Paper B)

| Status | Count | Claim IDs |
|---|---|---|
| VERIFIED EMPIRICAL | 0 | — |
| REPRODUCED SIMULATION | 8 | B-17, B-18, B-35, B-36, B-37, B-38, B-39, B-40 |
| VALIDATED SIMULATION | 0 | — |
| AUTHOR-REPORTED | 18 | B-01, B-02, B-03, B-04, B-05, B-06, B-07, B-09, B-10, B-11, B-12, B-13, B-27, B-28, B-29, B-30, B-31, B-32 |
| CONTRADICTED | 14 | B-08, B-14, B-15, B-16, B-19, B-20, B-21, B-22, B-23, B-24, B-25, B-26, B-33, B-34 |
| UNRESOLVED | 0 | — |

*(Counts in the AUTHOR-REPORTED and CONTRADICTED rows include every ID listed; the totals are 40 adjudicated rows.)*

## 4. The two findings the programme must absorb

### 4.1 The D2 calibration artefact — the review's §4 is half wrong and the paper's rebuttal is half wrong

The audit's decomposition (`GATE1_MIGRATION_TABLE.md`; `GATE1_REPORT.md` §5) is decisive:

* Pre-repair, households' **expected** admission probability was **2.41×** (KR G12: 0.292 vs 0.121) and **1.96×**
  (HK G12: 0.455 vs 0.232) the **realised** Plackett–Luce probability.
* Contest preparation was **92–94 %** of pre-repair K–12 household spending in the 540 config.
* After the D2 repair, expected/realised = **1.0000** per gate; contest effort collapses 98–99 %
  (2.192 → 0.042 HK; 1.711 → 0.016 KR); participation is essentially unchanged (59.07 → 61.92; 57.44 → 58.38).
* With **no re-estimation**, the KR gap moves 68.36 → **29.71 pp** (target 32.1) and the ratio 18.01 → **2.11×**
  (target 3.4).

Therefore: the review's inference that the 540 parameterisation "lost the Korean calibration" is **largely a code
defect artefact** (B-33). But the paper cannot claim the 540 is calibrated (B-34): participation (58.4 % vs 76.5 %)
and grade-12 participation (49.3 % / 36.0 % vs 71.8 %) remain badly off, and the residual gap/ratio are still
outside their bands. Both sides of the review exchange were partly wrong. **This is a programme-level finding, not
a paper-level one** (also in `AUDIT_VERDICT.md`).

### 4.2 The CF4 specification dependence — three generations, three verdicts

| generation | CF4a verdict | CF1b verdict | CF3b verdict |
|---|---|---|---|
| 420-port legacy V1 (AUTHOR-REPORTED/PRE-REPAIR/UNCALIBRATED) | **passes both** | n/a | n/a |
| 540 pre-repair (REPRODUCED SIMULATION) | **fails HK equity**, passes KR | **passes** (only arm) | fails |
| 540 repaired (REPRODUCED SIMULATION, uncalibrated) | **passes both** | fails spend | **passes** |

Three defensible-looking generations produce three different policy conclusions because of (i) generation
differences and (ii) the D2 defect. The manuscript's "only pairing compression with caps/seats reaches the
win-win frontier" and the review's "only CF1b passes" are **both** generation-specific. No policy conclusion is
established. The programme must report all three and refuse to rank them until the canonical spec is calibrated
(Gate 2) and re-run (Gate 3).

## 5. Required corrections (summary; detail in `MANUSCRIPT_ERRATA.md`)

1. **Abstract:** rewrite entirely. Delete "Calibrated baselines closely match"; delete "two structural laws"; delete
   "only pairing wage compression with effort caps or seat expansion reaches the win-win frontier"; replace with an
   explicit author-reported/conditional-simulation statement and the three-generation caveat.
2. **Title:** "Why Tutoring Taxes Backfire and Expanding Elite Seats Fuels the Arms Race" asserts two laws that are
   contradicted or spec-dependent under the repaired engine. Retitle to a conditional/mechanism framing, or drop
   the causal-certainty claims.
3. **Table 2:** rebuild from `GATE2_BENCHMARK_REGISTRY.csv`; mark 32.1 pp and 3.4× as derived targets; mark 76.5 %
   as diagnostic-only; add 2024 = 80.0 %, 2025 = 75.7 %; add citation/year/population/denominator columns.
4. **Tables 3–4 and Figures 1–4:** label AUTHOR-REPORTED / 420 generation; do not present beside 540 text. Either
   deposit the 420 runner or regenerate everything after Gate 2.
5. **Findings 1–3:** rewrite as specification-dependent. Report, for each arm, pre-repair 540 (with the D2 label),
   repaired 540 (uncalibrated), and — if available — the 420 author-reported generation. Delete "backfires",
   "only", "reproduces", "exact same policy hierarchy", "demonstrates".
6. **Medical-seat episode:** rewrite as motivating context with proposed-vs-finalised, 2024/2025 spend, preprint
   status, and no "reproduces/directly explains".
7. **Conclusion:** remove "calibrated across 420 matched simulation runs ... demonstrates". Replace with a
   conditional-simulation statement and an explicit list of what is not established.

## 6. Publishability verdict

**Not publishable as a calibrated comparative structural study.** Every causal/counterfactual headline is either
(A) from a non-reproducible 420 generation, (B) a D2 artefact, or (C) spec-dependent to the point of sign reversal.
The manuscript's tables are not the reproduced run, and the reproduced run is not calibrated.

**Only defensible future form:** a **methods/negative paper** — "Specification dependence and
expected-probability consistency in structural models of shadow education: why a contest-model policy ranking is
not identified by the current evidence" — reporting the 540 pre-repair vs repaired migration, the three-generation
CF4 flip, and the corrected-Tullock surface (inverted-U, not a 100 % paradox). That paper is honest and genuinely
useful, but it is a different paper and it depends on Gate-2 calibration results that do not yet exist.

**Do not submit the current draft.**
