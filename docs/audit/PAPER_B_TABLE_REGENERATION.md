# PAPER B — TABLE REGENERATION FROM THE REPAIRED 540

**Adjudicator:** `paper-adjudicator` (independent). **Date:** 2026-11-25.
**Purpose (Lead order, Phase 2):** regenerate every Paper B table that depends on the HK/Korea runs from the
repaired-engine 540, and mark every number that changes; the old numbers stay visible as prior.
> **Framing (operator decision, 2026-11-25).** The docx tables are the **AUTHOR-REPORTED BASELINE**. The repaired
> 540 is the **NEW GENERATION** (pre-registered, hashed, uncalibrated). This report shows both columns plus the
> pre-repair generation; it never silently replaces the baseline. Two-column comparison template:
> `docs/audit/PAPER_A_BASELINE_VS_NEWGEN_TEMPLATE.md` (§B, same convention).
**Sources (hashes re-derived for this report):**

| source | path | sha256 | status |
|---|---|---|---|
| **repaired-engine 540 (primary)** | `results/audit/commander/hk_korea_540_REPAIRED_box98baf6b_2026-11-25.json` | `455649daf2a1e3367820004c3338deb41236991814887c295b6e7a2bb634ec21` | REPRODUCED SIMULATION, uncalibrated |
| pre-repair 540 (prior) | `results/audit/commander/hk_korea_540_commander_independent_2026-11-25.json` | `722c370bfc00a339174bf3135f12389dbc53d87a7f607639814ebf43056eaf54` | REPRODUCED SIMULATION, pre-repair |
| migration table (cross-check) | `docs/audit/GATE1_MIGRATION_TABLE.md` | — | REPRODUCED SIMULATION |
| 420 generation (docx table source) | `papers/shadow-education-contest/code/results/verified_results_2026_11_25.json` | `b14e28162b1c7f1effeb01f9d07b4fbe72f3125f3350229f20ed1531e052b1de` | AUTHOR-REPORTED |
| machine-readable regeneration | `results/audit/paper_b_540_regenerated_tables.csv` | `da40a2eee350001530e673094cb4d167cc7e4c5eddd3512015e3c93ea728c5c1` | this report's data |

**Design labels used below:**

* **420** = the manuscript's own generation (14 arms × 30 seeds, `N=400`, `T=70`). **AUTHOR-REPORTED; not
  reproducible** — no runnable 420-era runner exists; the docx tables match the self-reported JSON cell-for-cell.
* **540-PRE** = reproduced 540 (`N=300`, `T=46`, 18 arms × 30 seeds) on the **pre-repair** engine. REPRODUCED
  SIMULATION.
* **540-REP** = the same 540 config on the **repaired** engine (`98baf6b`), sha256 `455649da…`. REPRODUCED
  SIMULATION, **UNCALIBRATED**. This is the primary source for the regenerated tables.

**Critical provenance caveat (from the Canonical-Spec freeze).** `docs/audit/canonical_spec.json` freezes
**V540-FREEZE** with `GATE_SPECS` = **KR-TRACKED primary / KR-SINGLE sensitivity**, engine pin `98baf6b`. The
`455649da…` run predates that freeze and used the **legacy 540 gate list** (GATE1_REPORT §5). The tables below are
therefore **repaired-engine + legacy 540 gate list**, not the frozen-spec tables. A frozen-spec 540 run is a
**new Gate-2 job** that has not been executed; do not call these tables "canonical-spec" tables.

**What the 540 does not contain.** No Grade-9 participation series, no `N=400`/`T=70` design, and no 14-arm set
(the 540 has 18 arms and adds CF4a/CF4b). G9 cells cannot be regenerated; the 420 design cannot be regenerated at
all. Every regenerated cell is 540-REP unless marked.

---

## 1. Regenerated Table 3-equivalent — HONG KONG (repaired-engine 540, uncalibrated)

`Total Spend Index` baseline = 100.0. `Win-Win` = pre-stated criterion: spend index < 80 **and** elite Q5 share
below the same-jurisdiction 540-REP baseline (25.01 %), both jurisdictions.

| Arm | Spend index (420 → 540-PRE → **540-REP**) | K–12 rate % | G12 rate % | Q5−Q1 gap pp | Q5/Q1 ratio | Elite Q5 % | Δspend pts | Δelite pp | Win-Win (540-REP) |
|---|---|---|---|---|---|---|---|---|---|
| Baseline | 100.0 → 100.0 → **100.0** | **61.92** (420: 40.0) | **49.30** (420: 71.6) | **34.76** (420: 52.8) | **2.47** (420: 11.83) | **25.01** (420: 30.0) | — | — | — |
| CF1a +50 % tax | 104.8 → 107.42 → **96.49** | 61.36 | 42.60 | 35.21 | 2.63 | **24.67** (420: 34.2) | **−3.51** | **−0.34** | **FALSE** |
| CF1b −50 % cap | 82.1 → 67.39 → **97.21** | 61.98 | 50.60 | 34.61 | 2.26 | 23.72 (420: 25.1) | −2.79 | −1.29 | **FALSE** (spend ≥ 80) |
| CF2a S=0.28 | 117.4 → 110.29 → **109.25** | 65.81 | 52.39 | 32.63 | 2.24 | 24.84 (420: 28.6) | +9.25 | −0.17 | FALSE |
| CF2b S=0.50 | 173.8 → 149.30 → **131.76** | 75.05 | 56.44 | 25.33 | 1.72 | 22.99 (420: 24.8) | +31.76 | −2.02 | FALSE |
| CF3a ΔV −30 % | 73.1 → 76.98 → **82.44** | 54.15 | 42.72 | 36.68 | 2.75 | **24.56** (420: 33.7) | −17.56 | **−0.45** | FALSE (spend ≥ 80) |
| CF3b ΔV −50 % | 52.8 → 59.11 → **70.88** | 48.53 | 38.67 | 36.37 | 2.81 | **23.64** (420: 36.3) | −29.12 | **−1.37** | **TRUE** |
| CF4a ΔV−50 %+cap | — → 43.78 → **70.58** | 48.58 | 39.17 | 36.40 | 2.76 | **23.44** | −29.42 | **−1.57** | **TRUE** |
| CF4b ΔV−50 %+seats | — → 90.88 → **89.98** | 57.87 | 45.64 | 34.47 | 2.42 | 23.11 | −10.02 | −1.90 | FALSE (spend ≥ 80) |

## 2. Regenerated Table 4-equivalent — SOUTH KOREA (repaired-engine 540, uncalibrated)

540-REP baseline elite Q5 = 22.13 %. Win-Win criterion as above.

| Arm | Spend index (420 → 540-PRE → **540-REP**) | K–12 rate % | G12 rate % | Q5−Q1 gap pp | Q5/Q1 ratio | Elite Q5 % | Δspend pts | Δelite pp | Win-Win (540-REP) |
|---|---|---|---|---|---|---|---|---|---|
| Baseline | 100.0 → 100.0 → **100.0** | **58.38** (420: 76.5) | **36.00** (420: 71.8) | **29.71** (420: 34.1; target 32.1) | **2.11** (420: 3.19; target 3.4) | **22.13** (420: 24.6) | — | — | — |
| CF1a +50 % tax | 107.4 → 106.46 → **96.88** | 58.04 | 32.32 | 28.91 | 1.98 | **21.57** (420: 26.0) | **−3.12** | **−0.56** | **FALSE** |
| CF1b −50 % cap | 74.1 → 76.42 → **99.25** | 58.46 | 36.53 | 29.72 | 2.06 | 22.00 (420: 22.9) | −0.75 | −0.13 | **FALSE** (spend ≥ 80) |
| CF2a S=0.16 | 105.9 → 107.17 → **111.57** | 62.81 | 41.18 | 28.09 | 2.07 | **22.27** (420: 23.7) | +11.57 | **+0.14** | FALSE |
| CF2b S=0.40 | 122.3 → 128.00 → **156.76** | 75.97 | 54.93 | 16.23 | 1.61 | **22.13** (420: 21.6) | +56.76 | **0.00** | FALSE |
| CF3a ΔV −30 % | 74.8 → 76.63 → **83.42** | 50.44 | 32.30 | 31.06 | 2.19 | **21.69** (420: 25.8) | −16.58 | **−0.44** | FALSE |
| CF3b ΔV −50 % | 54.9 → 57.36 → **72.55** | 44.57 | 30.45 | 30.85 | 2.29 | **21.48** (420: 27.5) | −27.45 | **−0.65** | **TRUE** |
| CF4a ΔV−50 %+cap | — → 46.50 → **72.48** | 44.58 | 30.55 | 30.92 | 2.28 | **21.47** | −27.52 | **−0.66** | **TRUE** |
| CF4b ΔV−50 %+seats | — → 88.04 → **105.54** | 59.05 | 42.93 | 28.68 | 2.06 | 22.09 | +5.54 | −0.04 | FALSE (spend ≥ 80) |

## 3. What changes against the docx tables — cell by cell

The manuscript's Tables 3–4 are the **420** column above. Every one of the following cells must change or be
relabelled; none of these are cosmetic.

| docx table cell | 420 (as printed) | 540-PRE (reproduced) | 540-REP (repaired, uncalibrated) | Required action |
|---|---|---|---|---|
| HK baseline elite Q5 | 30.0 % | 46.36 % | **25.01 %** | must be relabelled by generation; 30.0 is author-reported |
| KR baseline elite Q5 | 24.6 % | 36.12 % | **22.13 %** | same |
| HK baseline K–12 | 40.0 % | 59.07 % | **61.92 %** | same |
| KR baseline K–12 | 76.5 % | 57.44 % | **58.38 %** | **calibration claim fails**: no runnable generation recovers 76.5 % |
| HK baseline G12 | 71.6 % | 72.37 % | **49.30 %** | repaired engine does not recover 71.8 % |
| KR baseline G12 | 71.8 % | 73.69 % | **36.00 %** | same |
| HK baseline gap / ratio | +52.8 pp / 11.83× | 70.63 pp / 39.81× | **34.76 pp / 2.47×** | same |
| KR baseline gap / ratio | +34.1 pp / 3.19× | 68.36 pp / 18.01× | **29.71 pp / 2.11×** | repaired gap is 2.4 pp below the 32.1 target; ratio over-corrected below 3.4 |
| HK CF1a spend | 104.8 | 107.42 | **96.49** | **sign reverses**: tax lowers spend on the repaired engine |
| HK CF1a elite | 34.2 % | 52.43 % | **24.67 %** (below 25.01 baseline) | **sign reverses** |
| KR CF1a spend | 107.4 | 106.46 | **96.88** | sign reverses |
| KR CF1a elite | 26.0 % | 41.75 % | **21.57 %** (below 22.13) | sign reverses |
| HK CF1b spend | 82.1 | 67.39 | **97.21** | **fails spend criterion** (was a pass) |
| KR CF1b spend | 74.1 | 76.42 | **99.25** | **fails** (was a pass) |
| HK CF3b elite | 36.3 % | 59.02 % | **23.64 %** (below 25.01) | **sign reverses** (was regressive) |
| KR CF3b elite | 27.5 % | 47.66 % | **21.48 %** (below 22.13) | **sign reverses** |
| KR CF2a G12 | 82.0 % (71.8 +10.2) | 79.08 % | **41.18 %** | magnitude not reproduced |
| HK CF2b G12 | 97.1 % | 85.65 % | **56.44 %** | magnitude not reproduced |
| KR CF4a CF4b | absent from Tables 3–4 | CF4a KR passes, HK fails; CF4b fails | **CF4a passes both; CF4b fails spend** | add the combined arms; report the flip |

## 4. The regenerated CF4 / Win-Win verdict (the correction that matters most)

Pre-stated criterion: spend index < 80 **and** elite Q5 share below the same-jurisdiction baseline, **both**
jurisdictions.

| arm | 420 | 540-PRE | 540-REP | verdict across generations |
|---|---|---|---|---|
| CF1b (cap −50 %) | (420 table: spend 82.1 / 74.1, elite 25.1 / 22.9 — not evaluated as Win-Win) | **TRUE (only arm)** | **FALSE** (spend 97.21 / 99.25) | flips |
| CF3b (ΔV −50 %) | (not evaluated) | FALSE | **TRUE** (HK 70.88/23.64; KR 72.55/21.48) | flips |
| **CF4a (ΔV −50 % + cap)** | (not in table) | **FALSE** (HK elite 48.64 > 46.36) | **TRUE** (HK 70.58/23.44; KR 72.48/21.47) | **flips** |
| CF4b (ΔV −50 % + seats) | (not in table) | FALSE (spend 90.88/88.04) | FALSE (spend 89.98/105.54) | fails all |
| CF1a, CF2a, CF2b, CF3a | — | FALSE | FALSE | unchanged |

**Consequence for the manuscript:** the claim "only pairing wage compression with caps/seat expansion reaches the
win-win frontier" and the review-record claim "only CF1b passes" are **both generation artefacts**. On the repaired
engine, two single/composite arms (CF3b, CF4a) pass and the previously-passing arm (CF1b) fails. No ranking is
established under an uncalibrated spec.

## 5. What CANNOT be regenerated from the 540

| cannot regenerate | why | source that would be needed |
|---|---|---|
| Grade-9 participation (all Table 3/4 cells) | 540 JSON reports no grade-9 series | a runner that emits G9 participation |
| the `N=400`, `T=70` design | 540 is `N=300`, `T=46` | the 420-era runner (missing) |
| the 14-arm table including the 420 calibration match | 540 has 18 arms and a different parameter set | 420 runner/data (missing) |
| the "published benchmark" comparisons (53.8/71.8/76.5/32.1/3.4) | G2-A citation gate: all four dropped/UNRESOLVED — no traceable source in the manuscript's references (`G2A_CITATION_VERIFICATION.md`) | primary KEDI/HK survey sources |
| a frozen-canonical-spec table (KR-TRACKED) | `455649da…` used the legacy 540 gate list | a new GATE_SPECS 540 run after Gate-2 calibration |

## 6. Exact instruction to the authors

Replace Tables 3 and 4 with **two labelled panels**: (a) `AUTHOR-REPORTED 420 generation` (the current cells,
verbatim, with the 420 label) and (b) `REPRODUCED SIMULATION 540 generation` (the regenerated cells above, with
both pre-repair and repaired columns, and **UNCALIBRATED** in the title). Delete any sentence that treats a single
generation's sign as a law. Add CF4a/CF4b rows. Do not put a 420 number beside a 540 number without an explicit
column label.

The machine-readable version of every regenerated cell is
`results/audit/paper_b_540_regenerated_tables.csv` (sha256 `da40a2ee…c5c1`).
